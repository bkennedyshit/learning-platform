import type { QueryResult, QueryResultRow } from "pg";
import type { EmbeddedLessonChunk } from "./embedding.js";
import type { ParsedLessonMarkdown } from "./frontmatter.js";
import type { AuthoredPracticeProblem } from "./practice.js";
import type { Catalog, LearningPath, PathItem } from "@learning-platform/corpus-types";

export interface Queryable {
  query<T extends QueryResultRow = QueryResultRow>(
    text: string,
    values?: readonly unknown[]
  ): Promise<QueryResult<T>>;
}

export interface LessonUpsertInput {
  lessonId: string;
  subjectId: string;
  slug: string;
  bodyRef: string;
  lesson: ParsedLessonMarkdown;
}

export interface ContentManifestLesson {
  id: string;
  slug: string;
  title: string;
  subject: string;
  catalog: string;
  audienceTier: string;
  openSource: boolean;
}

export async function upsertLessonMetadata(db: Queryable, input: LessonUpsertInput): Promise<void> {
  const { frontmatter } = input.lesson;

  await db.query(
    `
      INSERT INTO lessons (
        id,
        subject_id,
        audience_tier,
        slug,
        chapter,
        title,
        epigraph,
        objectives,
        body_ref,
        open_source,
        updated_at
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, now())
      ON CONFLICT (subject_id, slug)
      DO UPDATE SET
        audience_tier = EXCLUDED.audience_tier,
        chapter = EXCLUDED.chapter,
        title = EXCLUDED.title,
        epigraph = EXCLUDED.epigraph,
        objectives = EXCLUDED.objectives,
        body_ref = EXCLUDED.body_ref,
        open_source = EXCLUDED.open_source,
        updated_at = now()
    `,
    [
      input.lessonId,
      input.subjectId,
      frontmatter.audienceTier,
      input.slug,
      frontmatter.chapter,
      frontmatter.title,
      frontmatter.epigraph ?? null,
      frontmatter.objectives,
      input.bodyRef,
      frontmatter.openSource
    ]
  );
}

export async function replaceCrossLinks(
  db: Queryable,
  lessonId: string,
  targetLessonIds: readonly string[]
): Promise<void> {
  await db.query("DELETE FROM cross_links WHERE lesson_id = $1", [lessonId]);

  for (const targetLessonId of targetLessonIds) {
    await db.query(
      `
        INSERT INTO cross_links (lesson_id, target_lesson_id)
        VALUES ($1, $2)
        ON CONFLICT DO NOTHING
      `,
      [lessonId, targetLessonId]
    );
  }
}

export async function replaceLessonChunks(
  db: Queryable,
  lessonId: string,
  chunks: readonly EmbeddedLessonChunk[]
): Promise<void> {
  await db.query("DELETE FROM lesson_chunks WHERE lesson_id = $1", [lessonId]);

  for (const chunk of chunks) {
    await db.query(
      `
        INSERT INTO lesson_chunks (lesson_id, chunk_index, text, embedding)
        VALUES ($1, $2, $3, $4::vector)
      `,
      [lessonId, chunk.chunkIndex, chunk.text, vectorLiteral(chunk.embedding)]
    );
  }
}

export async function replacePracticeProblems(
  db: Queryable,
  subjectId: string,
  problems: readonly AuthoredPracticeProblem[]
): Promise<void> {
  await db.query("DELETE FROM practice_problems WHERE subject_id = $1 AND source = 'authored'", [subjectId]);

  for (const problem of problems) {
    await db.query(
      `
        INSERT INTO practice_problems (id, subject_id, lesson_id, tier, prompt, solution, source)
        VALUES ($1, $2, $3, $4, $5, $6, 'authored')
      `,
      [problem.id, subjectId, problem.lessonId ?? null, problem.tier, problem.prompt, problem.solution]
    );
  }
}

export function toContentManifestLesson(input: LessonUpsertInput): ContentManifestLesson {
  return {
    id: input.lessonId,
    slug: input.slug,
    title: input.lesson.frontmatter.title,
    subject: input.lesson.frontmatter.subject,
    catalog: input.lesson.frontmatter.catalog,
    audienceTier: input.lesson.frontmatter.audienceTier,
    openSource: input.lesson.frontmatter.openSource
  };
}

function vectorLiteral(embedding: readonly number[]): string {
  return `[${embedding.join(",")}]`;
}

export async function upsertCatalog(db: Queryable, catalog: Catalog): Promise<void> {
  await db.query(
    `
      INSERT INTO catalogs (id, key, name, description)
      VALUES ($1, $2, $3, $4)
      ON CONFLICT (id) DO UPDATE SET
        key = EXCLUDED.key,
        name = EXCLUDED.name,
        description = EXCLUDED.description
    `,
    [catalog.id, catalog.key, catalog.name, catalog.description ?? null]
  );
}

export async function upsertLearningPath(db: Queryable, path: LearningPath): Promise<void> {
  await db.query(
    `
      INSERT INTO learning_paths (id, catalog_id, name, slug, audience_tier, is_purchasable)
      VALUES ($1, $2, $3, $4, $5, $6)
      ON CONFLICT (id) DO UPDATE SET
        catalog_id = EXCLUDED.catalog_id,
        name = EXCLUDED.name,
        slug = EXCLUDED.slug,
        audience_tier = EXCLUDED.audience_tier,
        is_purchasable = EXCLUDED.is_purchasable
    `,
    [path.id, path.catalogId, path.name, path.slug, path.audienceTier, path.isPurchasable]
  );
}

export async function replacePathItems(db: Queryable, pathId: string, items: readonly PathItem[]): Promise<void> {
  await db.query("DELETE FROM path_items WHERE path_id = $1", [pathId]);

  for (const item of items) {
    await db.query(
      `
        INSERT INTO path_items (id, path_id, position, kind, subject_id, lesson_id)
        VALUES ($1, $2, $3, $4, $5, $6)
      `,
      [item.id, pathId, item.position, item.kind, item.subjectId ?? null, item.lessonId ?? null]
    );
  }
}
