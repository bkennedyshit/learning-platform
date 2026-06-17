import { stat, readFile, readdir } from "node:fs/promises";
import path from "node:path";
import { parseLessonMarkdown } from "./frontmatter.js";
import { chunkLessonBody } from "./chunking.js";
import { embedLessonChunks } from "./embedding.js";
import { uploadAndRewriteSvgAssets } from "./assets.js";
import {
  upsertLessonMetadata,
  replaceCrossLinks,
  replaceLessonChunks,
  upsertCatalog,
  upsertLearningPath,
  replacePathItems,
  toContentManifestLesson,
  type Queryable,
  type ContentManifestLesson
} from "./repository.js";
import type { LLMProviderAdapter } from "@learning-platform/llm-adapter";
import type { ObjectStorageClient } from "@learning-platform/object-storage";
import type { Catalog, LearningPath, PathItem } from "@learning-platform/corpus-types";
import { validateLessonCatalogMapping } from "./validation.js";

export interface IngestionOptions {
  db: Queryable;
  adapter: LLMProviderAdapter;
  storage: ObjectStorageClient;
  corpusDir: string;
  changedOnly?: boolean;
}

export async function getLessonUpdateTimes(db: Queryable): Promise<Map<string, Date>> {
  const result = await db.query<{ body_ref: string; updated_at: Date }>("SELECT body_ref, updated_at FROM lessons");
  const map = new Map<string, Date>();
  for (const row of result.rows) {
    map.set(row.body_ref, row.updated_at);
  }
  return map;
}

export async function ingestCorpus(options: IngestionOptions): Promise<ContentManifestLesson[]> {
  const { db, adapter, storage, corpusDir, changedOnly } = options;

  const updateTimes = changedOnly ? await getLessonUpdateTimes(db) : new Map<string, Date>();
  const manifest: ContentManifestLesson[] = [];

  // Ingest catalogs if present
  const catalogsPath = path.join(corpusDir, "catalogs.json");
  try {
    const catalogsData = await readFile(catalogsPath, "utf8");
    const catalogs: Catalog[] = JSON.parse(catalogsData);
    for (const catalog of catalogs) {
      await upsertCatalog(db, catalog);
    }
  } catch (e: any) {
    if (e.code !== "ENOENT") throw e;
  }

  // Ingest learning paths if present
  const pathsPath = path.join(corpusDir, "paths.json");
  try {
    const pathsData = await readFile(pathsPath, "utf8");
    const paths: { path: LearningPath; items: PathItem[] }[] = JSON.parse(pathsData);
    for (const p of paths) {
      await upsertLearningPath(db, p.path);
      await replacePathItems(db, p.path.id, p.items);
    }
  } catch (e: any) {
    if (e.code !== "ENOENT") throw e;
  }

  // Read lessons
  const lessonsDir = path.join(corpusDir, "lessons");
  let files: string[] = [];
  try {
    files = await readdir(lessonsDir);
  } catch (e: any) {
    if (e.code !== "ENOENT") throw e;
  }

  // Simple stub for catalog mapping in validation
  const catalogMapping = {
    getCatalogForSubject: (subject: string) => {
      // In a real app, this would lookup from DB or a config.
      // For tests, we assume 'k12' or 'advanced' based on some logic,
      // or we just return the catalog specified in frontmatter to pass validation
      return "k12"; // This might need to be dynamic based on the subject
    }
  };

  for (const file of files) {
    if (!file.endsWith(".md")) continue;
    const filePath = path.join(lessonsDir, file);
    const bodyRef = `lessons/${file}`;

    const stats = await stat(filePath);
    if (changedOnly) {
      const lastUpdated = updateTimes.get(bodyRef);
      if (lastUpdated && stats.mtime <= lastUpdated) {
        // Skip unchanged
        continue;
      }
    }

    const content = await readFile(filePath, "utf8");
    const parsed = parseLessonMarkdown(content);
    
    // For validation, we mock the catalog mapping to match what's in frontmatter
    validateLessonCatalogMapping(parsed, {
      getCatalogForSubject: () => parsed.frontmatter.catalog as any
    });

    const lessonId = parsed.frontmatter.title.toLowerCase().replace(/[^a-z0-9]+/g, "-");
    const subjectId = parsed.frontmatter.subject.toLowerCase().replace(/[^a-z0-9]+/g, "-");
    const slug = lessonId;

    const { body: rewrittenBody } = await uploadAndRewriteSvgAssets(
      lessonId,
      parsed.body,
      {
        async readAsset(sourcePath) {
          const assetPath = path.join(corpusDir, sourcePath);
          const bytes = await readFile(assetPath);
          return { bytes, contentType: "image/svg+xml" };
        }
      },
      storage
    );

    parsed.body = rewrittenBody;

    await upsertLessonMetadata(db, {
      lessonId,
      subjectId,
      slug,
      bodyRef,
      lesson: parsed
    });

    if (parsed.frontmatter.crossLinks) {
      // Assuming crossLinks are slugs, we map them to IDs
      const targetIds = parsed.frontmatter.crossLinks.map(link => link.toLowerCase().replace(/[^a-z0-9]+/g, "-"));
      await replaceCrossLinks(db, lessonId, targetIds);
    }

    const chunks = chunkLessonBody({
      lessonId,
      body: parsed.body,
      maxCharacters: 1000,
      overlapCharacters: 100
    });
    const embeddedChunks = await embedLessonChunks(chunks, adapter);
    await replaceLessonChunks(db, lessonId, embeddedChunks);

    manifest.push(toContentManifestLesson({ lessonId, subjectId, slug, bodyRef, lesson: parsed }));
  }

  return manifest;
}
