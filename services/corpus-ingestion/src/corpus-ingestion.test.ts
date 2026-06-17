import assert from "node:assert/strict";
import test from "node:test";
import { createLocalObjectStorageClient } from "@learning-platform/object-storage";
import { createStubAdapter } from "@learning-platform/llm-adapter/testing";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { uploadAndRewriteSvgAssets } from "./assets.js";
import { chunkLessonBody } from "./chunking.js";
import { embedLessonChunks } from "./embedding.js";
import { parseLessonMarkdown } from "./frontmatter.js";
import { parsePracticeBankJson } from "./practice.js";
import {
  replaceCrossLinks,
  replaceLessonChunks,
  replacePracticeProblems,
  toContentManifestLesson,
  upsertLessonMetadata,
  type Queryable
} from "./repository.js";
import { validateLessonCatalogMapping } from "./validation.js";

const sampleLesson = `---
title: Linear Equations
subject: algebra
catalog: k12
audience_tier: 6-8
chapter: "Chapter 1"
previous: intro
next: slope
objectives:
  - Solve one-step equations
  - Check solutions
epigraph: "Balance matters"
cross_links: [arithmetic-review]
open_source: true
---
# Linear Equations

![Balance](balance.svg)

Keep both sides equal.
`;

test("parses lesson markdown frontmatter and body", () => {
  const parsed = parseLessonMarkdown(sampleLesson);

  assert.equal(parsed.frontmatter.title, "Linear Equations");
  assert.equal(parsed.frontmatter.subject, "algebra");
  assert.equal(parsed.frontmatter.catalog, "k12");
  assert.equal(parsed.frontmatter.audienceTier, "6-8");
  assert.deepEqual(parsed.frontmatter.objectives, ["Solve one-step equations", "Check solutions"]);
  assert.deepEqual(parsed.frontmatter.crossLinks, ["arithmetic-review"]);
  assert.equal(parsed.frontmatter.openSource, true);
  assert.match(parsed.body, /Keep both sides equal/);
});

test("validates subject-to-catalog mapping", () => {
  const parsed = parseLessonMarkdown(sampleLesson);

  assert.doesNotThrow(() =>
    validateLessonCatalogMapping(parsed, {
      getCatalogForSubject: () => "k12"
    })
  );

  assert.throws(() =>
    validateLessonCatalogMapping(parsed, {
      getCatalogForSubject: () => "advanced"
    })
  );
});

test("uploads and rewrites SVG assets", async () => {
  const root = await mkdtemp(path.join(tmpdir(), "corpus-assets-"));
  const storage = createLocalObjectStorageClient({
    rootDir: root,
    publicBaseUrl: "http://assets.test"
  });

  try {
    const result = await uploadAndRewriteSvgAssets(
      "lesson-1",
      "See ![Balance](diagrams/balance.svg).",
      {
        async readAsset(sourcePath) {
          assert.equal(sourcePath, "diagrams/balance.svg");
          return {
            bytes: new TextEncoder().encode("<svg />"),
            contentType: "image/svg+xml"
          };
        }
      },
      storage
    );

    assert.match(result.body, /http:\/\/assets\.test\/corpus-assets\/lessons\/lesson-1\/assets\/balance\.svg/);
    assert.equal(result.uploadedAssets.length, 1);
    assert.equal(
      await readFile(path.join(root, "corpus-assets", "lessons", "lesson-1", "assets", "balance.svg"), "utf8"),
      "<svg />"
    );
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test("chunks and embeds lesson body", async () => {
  const chunks = chunkLessonBody({
    lessonId: "lesson-1",
    body: "# A\n\nshort section\n\n## B\n\nanother section",
    maxCharacters: 20,
    overlapCharacters: 4
  });

  assert.ok(chunks.length >= 2);
  const embedded = await embedLessonChunks(chunks, createStubAdapter({ embeddingDimensions: 3 }));
  assert.equal(embedded[0]?.embedding.length, 3);
});

test("repository functions issue lesson, cross-link, and chunk persistence queries", async () => {
  const parsed = parseLessonMarkdown(sampleLesson);
  const queries: Array<{ text: string; values?: readonly unknown[] }> = [];
  const db: Queryable = {
    async query(text, values) {
      queries.push({ text, values });
      return { rows: [], rowCount: 0, command: "", oid: 0, fields: [] };
    }
  };

  await upsertLessonMetadata(db, {
    lessonId: "11111111-1111-1111-1111-111111111111",
    subjectId: "22222222-2222-2222-2222-222222222222",
    slug: "linear-equations",
    bodyRef: "lessons/linear-equations.md",
    lesson: parsed
  });
  await replaceCrossLinks(db, "11111111-1111-1111-1111-111111111111", [
    "33333333-3333-3333-3333-333333333333"
  ]);
  await replaceLessonChunks(db, "11111111-1111-1111-1111-111111111111", [
    {
      lessonId: "11111111-1111-1111-1111-111111111111",
      chunkIndex: 0,
      text: "chunk text",
      embedding: [0.1, 0.2, 0.3]
    }
  ]);
  await replacePracticeProblems(db, "22222222-2222-2222-2222-222222222222", [
    {
      id: "44444444-4444-4444-4444-444444444444",
      subjectId: "22222222-2222-2222-2222-222222222222",
      tier: "easy",
      prompt: "1 + 1 = ?",
      solution: "2"
    }
  ]);

  assert.equal(queries.length, 7);
  assert.match(queries[0]?.text ?? "", /INSERT INTO lessons/);
  assert.match(queries[2]?.text ?? "", /INSERT INTO cross_links/);
  assert.deepEqual(queries[4]?.values?.[3], "[0.1,0.2,0.3]");
  assert.match(queries[5]?.text ?? "", /DELETE FROM practice_problems/);
  assert.match(queries[6]?.text ?? "", /INSERT INTO practice_problems/);
});

test("content manifest lesson is emitted from normalized metadata", () => {
  const parsed = parseLessonMarkdown(sampleLesson);

  assert.deepEqual(
    toContentManifestLesson({
      lessonId: "lesson-1",
      subjectId: "subject-1",
      slug: "linear-equations",
      bodyRef: "body.md",
      lesson: parsed
    }),
    {
      id: "lesson-1",
      slug: "linear-equations",
      title: "Linear Equations",
      subject: "algebra",
      catalog: "k12",
      audienceTier: "6-8",
      openSource: true
    }
  );
});

test("parses practice bank json", () => {
  const json = `[
    {
      "id": "prob-1",
      "tier": "easy",
      "prompt": "Solve for x: x - 2 = 0",
      "solution": "x = 2"
    }
  ]`;

  const parsed = parsePracticeBankJson(json, "subject-1");

  assert.equal(parsed.length, 1);
  assert.equal(parsed[0]?.id, "prob-1");
  assert.equal(parsed[0]?.subjectId, "subject-1");
  assert.equal(parsed[0]?.tier, "easy");
  assert.equal(parsed[0]?.prompt, "Solve for x: x - 2 = 0");
  assert.equal(parsed[0]?.solution, "x = 2");
});
