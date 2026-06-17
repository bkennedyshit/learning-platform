import assert from "node:assert/strict";
import test from "node:test";
import { createStubAdapter } from "@learning-platform/llm-adapter/testing";
import { createTutorOrchestrator } from "./orchestrator.js";

test("tutor refuses when retrieval returns no passages", async () => {
  const tutor = createTutorOrchestrator(
    {
      async retrieve() {
        return { passages: [], lessonRefs: [] };
      }
    },
    createStubAdapter({ completionText: "should not be used" })
  );

  const answer = await tutor.answerQuestion({ question: "invent a new topic" });

  assert.equal(answer.grounded, false);
  assert.deepEqual(answer.sourceLessonIds, []);
  assert.match(answer.content, /available lessons/);
});

test("tutor answers with source lesson ids when passages are retrieved", async () => {
  const tutor = createTutorOrchestrator(
    {
      async retrieve() {
        return {
          passages: [
            {
              text: "Linear equations keep both sides balanced.",
              lessonId: "lesson-1",
              chunkId: "chunk-1",
              score: 0.9
            }
          ],
          lessonRefs: ["lesson-1"]
        };
      }
    },
    createStubAdapter({ completionText: "A linear equation keeps both sides balanced." })
  );

  assert.deepEqual(await tutor.answerQuestion({ question: "What is a linear equation?" }), {
    content: "A linear equation keeps both sides balanced.",
    sourceLessonIds: ["lesson-1"],
    grounded: true
  });
});

test("tutor gives plain lesson-start and stage-advance guidance", () => {
  const tutor = createTutorOrchestrator(
    {
      async retrieve() {
        return { passages: [], lessonRefs: [] };
      }
    },
    createStubAdapter()
  );

  assert.deepEqual(tutor.startLesson("lesson-1", false), {
    lessonId: "lesson-1",
    currentStage: "read",
    nextStage: "listen",
    message: "Start by reading the lesson. When you are done, move to listening."
  });
  assert.equal(tutor.advanceStage("write", true).currentStage, "code");
  assert.equal(tutor.advanceStage("write", false).currentStage, "handwrite");
});
