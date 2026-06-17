import assert from "node:assert/strict";
import test from "node:test";
import { createStubAdapter } from "@learning-platform/llm-adapter/testing";
import { createRagRetrievalService } from "./retrieval.js";

test("retrieval returns cited passages above threshold", async () => {
  const queries: Array<{ text: string; values?: readonly unknown[] }> = [];
  const service = createRagRetrievalService(
    {
      async query(text, values) {
        queries.push({ text, values });
        return {
          rows: [
            {
              text: "A linear equation keeps both sides balanced.",
              lesson_id: "lesson-1",
              chunk_id: "chunk-1",
              score: 0.91
            }
          ],
          rowCount: 1,
          command: "",
          oid: 0,
          fields: []
        };
      }
    },
    createStubAdapter({ embeddingDimensions: 3 })
  );

  const result = await service.retrieve({ query: "what is a linear equation?", k: 3 });

  assert.equal(result.passages.length, 1);
  assert.deepEqual(result.lessonRefs, ["lesson-1"]);
  assert.deepEqual(queries[0]?.values?.[1], 3);
});

test("retrieval returns empty when all rows fall below threshold", async () => {
  const service = createRagRetrievalService(
    {
      async query() {
        return {
          rows: [
            {
              text: "Unrelated",
              lesson_id: "lesson-1",
              chunk_id: "chunk-1",
              score: 0.2
            }
          ],
          rowCount: 1,
          command: "",
          oid: 0,
          fields: []
        };
      }
    },
    createStubAdapter({ embeddingDimensions: 3 })
  );

  assert.deepEqual(await service.retrieve({ query: "outside", minimumScore: 0.8 }), {
    passages: [],
    lessonRefs: []
  });
});

test("retrieval can bias search to the current lesson subject", async () => {
  const queries: Array<{ text: string; values?: readonly unknown[] }> = [];
  const service = createRagRetrievalService(
    {
      async query(text, values) {
        queries.push({ text, values });
        return { rows: [], rowCount: 0, command: "", oid: 0, fields: [] };
      }
    },
    createStubAdapter({ embeddingDimensions: 2 })
  );

  await service.retrieve({ query: "slope", lessonId: "11111111-1111-1111-1111-111111111111" });

  assert.match(queries[0]?.text ?? "", /OR l\.subject_id/);
  assert.equal(queries[0]?.values?.[1], "11111111-1111-1111-1111-111111111111");
});
