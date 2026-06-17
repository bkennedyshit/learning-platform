import type { LLMProviderAdapter } from "@learning-platform/llm-adapter";
import type { QueryResultRow } from "pg";
import type { RetrievalRequest, RetrievalResult, RetrievedPassage } from "./types.js";

interface PassageRow {
  text: string;
  lesson_id: string;
  chunk_id: string;
  score: number;
}

export interface RagRetrievalService {
  retrieve(request: RetrievalRequest): Promise<RetrievalResult>;
}

export interface RagQueryable {
  query(text: string, values?: readonly unknown[]): Promise<{ rows: QueryResultRow[] }>;
}

export function createRagRetrievalService(
  pool: RagQueryable,
  adapter: LLMProviderAdapter
): RagRetrievalService {
  return {
    async retrieve(request) {
      const [queryEmbedding] = await adapter.embed({ texts: [request.query] });
      if (!queryEmbedding) {
        return { passages: [], lessonRefs: [] };
      }

      const limit = request.k ?? 8;
      const minimumScore = request.minimumScore ?? 0.72;
      const rows = await searchChunks(pool, {
        queryEmbedding,
        lessonId: request.lessonId,
        limit
      });
      const passages = rows
        .filter((row) => row.score >= minimumScore)
        .map(mapPassage);

      return {
        passages,
        lessonRefs: [...new Set(passages.map((passage) => passage.lessonId))]
      };
    }
  };
}

async function searchChunks(
  pool: RagQueryable,
  input: {
    queryEmbedding: readonly number[];
    lessonId?: string;
    limit: number;
  }
): Promise<PassageRow[]> {
  const vector = vectorLiteral(input.queryEmbedding);

  if (input.lessonId) {
    const result = await pool.query(
      `
        SELECT
          lc.text,
          lc.lesson_id::text,
          lc.id::text AS chunk_id,
          1 - (lc.embedding <=> $1::vector) AS score
        FROM lesson_chunks lc
        JOIN lessons l ON l.id = lc.lesson_id
        WHERE lc.embedding IS NOT NULL
          AND (
            lc.lesson_id = $2::uuid
            OR l.subject_id = (SELECT subject_id FROM lessons WHERE id = $2::uuid)
          )
        ORDER BY lc.embedding <=> $1::vector
        LIMIT $3
      `,
      [vector, input.lessonId, input.limit]
    );
    return result.rows as PassageRow[];
  }

  const result = await pool.query(
    `
      SELECT
        text,
        lesson_id::text,
        id::text AS chunk_id,
        1 - (embedding <=> $1::vector) AS score
      FROM lesson_chunks
      WHERE embedding IS NOT NULL
      ORDER BY embedding <=> $1::vector
      LIMIT $2
    `,
    [vector, input.limit]
  );
  return result.rows as PassageRow[];
}

function mapPassage(row: PassageRow): RetrievedPassage {
  return {
    text: row.text,
    lessonId: row.lesson_id,
    chunkId: row.chunk_id,
    score: Number(row.score)
  };
}

function vectorLiteral(embedding: readonly number[]): string {
  return `[${embedding.join(",")}]`;
}
