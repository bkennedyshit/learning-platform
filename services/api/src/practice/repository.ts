import type { QueryResultRow } from "pg";
import type { PracticeProblem, PracticeProblemRepository, PracticeProblemRequest } from "./types.js";

export interface PracticeQueryable {
  query(text: string, values?: readonly unknown[]): Promise<{ rows: QueryResultRow[] }>;
}

interface PracticeProblemRow extends QueryResultRow {
  id: string;
  subject_id: string;
  lesson_id: string | null;
  tier: PracticeProblem["tier"];
  prompt: string;
  solution: string;
  source: PracticeProblem["source"];
}

export function createPostgresPracticeProblemRepository(db: PracticeQueryable): PracticeProblemRepository {
  return {
    async findAuthoredProblem(request) {
      return findProblemBySource(db, request, "authored");
    },

    async findGeneratedProblem(request) {
      return findProblemBySource(db, request, "generated");
    },

    async saveGeneratedProblem(problem) {
      const result = await db.query(
        `
          INSERT INTO practice_problems (subject_id, lesson_id, tier, prompt, solution, source, source_hash)
          VALUES ($1, $2, $3, $4, $5, 'generated', encode(digest($4, 'sha256'), 'hex'))
          RETURNING id::text, subject_id::text, lesson_id::text, tier, prompt, solution, source
        `,
        [
          problem.subjectId,
          problem.lessonId ?? null,
          problem.tier,
          problem.prompt,
          problem.solution
        ]
      );

      const row = result.rows[0] as PracticeProblemRow | undefined;
      if (!row) {
        throw new Error("Generated problem insert did not return a row.");
      }

      return mapProblem(row);
    }
  };
}

async function findProblemBySource(
  db: PracticeQueryable,
  request: PracticeProblemRequest,
  source: PracticeProblem["source"]
): Promise<PracticeProblem | undefined> {
  const result = await db.query(
    `
      SELECT id::text, subject_id::text, lesson_id::text, tier, prompt, solution, source
      FROM practice_problems
      WHERE subject_id = $1::uuid
        AND tier = $2
        AND source = $3
        AND ($4::uuid IS NULL OR lesson_id = $4::uuid OR lesson_id IS NULL)
        AND NOT (id::text = ANY($5::text[]))
      ORDER BY lesson_id NULLS LAST, created_at ASC
      LIMIT 1
    `,
    [
      request.subjectId,
      request.tier,
      source,
      request.lessonId ?? null,
      [...(request.excludeProblemIds ?? [])]
    ]
  );

  const row = result.rows[0] as PracticeProblemRow | undefined;
  return row ? mapProblem(row) : undefined;
}

function mapProblem(row: PracticeProblemRow): PracticeProblem {
  return {
    id: row.id,
    subjectId: row.subject_id,
    ...(row.lesson_id ? { lessonId: row.lesson_id } : {}),
    tier: row.tier,
    prompt: row.prompt,
    solution: row.solution,
    source: row.source
  };
}
