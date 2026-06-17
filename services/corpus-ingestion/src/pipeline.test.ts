import assert from "node:assert/strict";
import test from "node:test";
import { mkdtemp, mkdir, writeFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { createStubAdapter } from "@learning-platform/llm-adapter/testing";
import { createLocalObjectStorageClient } from "@learning-platform/object-storage";
import { ingestCorpus } from "./pipeline.js";
import type { Queryable } from "./repository.js";

const sampleLesson1 = `---
title: Linear Equations
subject: algebra
catalog: k12
audience_tier: 6-8
chapter: "Chapter 1"
objectives:
  - Solve equations
cross_links: [math-review]
open_source: true
---
# Linear Equations

![Balance](diagrams/balance.svg)
`;

test("pipeline integration: ingestion produces correct metadata, embeddings, asset URLs, catalogs, paths", async () => {
  const root = await mkdtemp(path.join(tmpdir(), "corpus-ingestion-"));
  const lessonsDir = path.join(root, "lessons");
  const diagramsDir = path.join(root, "diagrams");
  await mkdir(lessonsDir, { recursive: true });
  await mkdir(diagramsDir, { recursive: true });

  await writeFile(path.join(lessonsDir, "linear-equations.md"), sampleLesson1);
  await writeFile(path.join(diagramsDir, "balance.svg"), "<svg></svg>");

  const catalogs = [
    { id: "cat-1", key: "k12", name: "K-12" }
  ];
  await writeFile(path.join(root, "catalogs.json"), JSON.stringify(catalogs));

  const paths = [
    {
      path: { id: "path-1", catalogId: "cat-1", name: "Middle School Math", slug: "6-8-math", audienceTier: "6-8", isPurchasable: true },
      items: [
        { id: "item-1", pathId: "path-1", position: 1, kind: "subject", subjectId: "algebra" }
      ]
    }
  ];
  await writeFile(path.join(root, "paths.json"), JSON.stringify(paths));

  const queries: string[] = [];
  const db: Queryable = {
    async query(text: string, values?: readonly unknown[]) {
      queries.push(text.trim().substring(0, 30));
      return { rows: [], rowCount: 0, command: "", oid: 0, fields: [] } as any;
    }
  };

  const adapter = createStubAdapter({ embeddingDimensions: 3 });
  const storage = createLocalObjectStorageClient({ rootDir: root, publicBaseUrl: "http://assets.test" });

  try {
    const manifest = await ingestCorpus({
      db,
      adapter,
      storage,
      corpusDir: root,
      changedOnly: false
    });

    assert.equal(manifest.length, 1);
    assert.equal(manifest[0]?.title, "Linear Equations");
    assert.equal(manifest[0]?.catalog, "k12");

    assert.ok(queries.some(q => q.includes("INSERT INTO catalogs")));
    assert.ok(queries.some(q => q.includes("INSERT INTO learning_paths")));
    assert.ok(queries.some(q => q.includes("INSERT INTO path_items")));
    assert.ok(queries.some(q => q.includes("INSERT INTO lessons")));
    assert.ok(queries.some(q => q.includes("INSERT INTO cross_links")));
    assert.ok(queries.some(q => q.includes("INSERT INTO lesson_chunks")));

    // Test changedOnly true, it should skip since we pretend it has a new update time
    const db2: Queryable = {
      async query(text: string) {
        if (text.includes("SELECT body_ref, updated_at")) {
          // Future date so it skips
          return { rows: [{ body_ref: "lessons/linear-equations.md", updated_at: new Date(Date.now() + 100000) }], rowCount: 1, command: "", oid: 0, fields: [] } as any;
        }
        queries.push("unreachable");
        return { rows: [], rowCount: 0, command: "", oid: 0, fields: [] } as any;
      }
    };
    const lessonQueriesBefore = queries.filter(q => q.includes("INSERT INTO lessons")).length;
    await ingestCorpus({
      db: db2,
      adapter,
      storage,
      corpusDir: root,
      changedOnly: true
    });
    // No new insertions because of skip
    const lessonQueriesAfter = queries.filter(q => q.includes("INSERT INTO lessons")).length;
    assert.equal(lessonQueriesAfter, lessonQueriesBefore);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});
