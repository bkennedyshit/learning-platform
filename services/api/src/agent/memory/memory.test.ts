import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { FileLearnerMemory } from "./fileStore.js";
import { InMemoryLearnerMemory } from "./inMemoryStore.js";

function tempDir(): string {
  return mkdtempSync(join(tmpdir(), "learner-memory-"));
}

test("in-memory store records and reads back learner state", async () => {
  const memory = new InMemoryLearnerMemory();
  await memory.upsertGoal({
    id: "g1",
    accountId: "acc1",
    description: "Master eigenvalues",
    targetConceptIds: ["eigenvalues"],
    status: "active",
    createdAt: "2026-09-01T12:00:00.000Z",
    updatedAt: "2026-09-01T12:00:00.000Z"
  });
  const goals = await memory.getActiveGoals("acc1");
  assert.equal(goals.length, 1);
  assert.equal(goals[0]?.description, "Master eigenvalues");
});

test("durable file store resumes goal, misconception, and due review after restart", async () => {
  const dir = tempDir();
  try {
    const first = new FileLearnerMemory({ root: dir });
    await first.upsertGoal({
      id: "g1",
      accountId: "acc1",
      description: "Master eigenvalues",
      targetConceptIds: ["eigenvalues"],
      status: "active",
      createdAt: "2026-09-01T12:00:00.000Z",
      updatedAt: "2026-09-01T12:00:00.000Z"
    });
    await first.upsertMisconception({
      id: "m1",
      accountId: "acc1",
      conceptId: "eigenvalues",
      description: "Thinks diagonal eigenvalues are the zeros.",
      evidenceAttemptIds: ["a1"],
      status: "open",
      createdAt: "2026-09-01T12:00:00.000Z",
      updatedAt: "2026-09-01T12:00:00.000Z"
    });
    await first.recordAttempt({
      id: "a1",
      accountId: "acc1",
      conceptId: "eigenvalues",
      prompt: "eigenvalues of diag(2,3)?",
      response: "0,0",
      correct: false,
      score: 0,
      at: "2026-09-01T12:00:00.000Z"
    });
    await first.upsertReview({
      accountId: "acc1",
      conceptId: "eigenvalues",
      lessonId: "lesson-eigenvalues",
      dueAt: "2026-09-01T00:00:00.000Z",
      intervalDays: 1,
      lastScore: 0.4,
      history: [{ at: "2026-08-31T00:00:00.000Z", score: 0.4 }]
    });

    // Simulate a service restart: brand new instance, same directory.
    const resumed = new FileLearnerMemory({ root: dir });

    const goals = await resumed.getActiveGoals("acc1");
    assert.equal(goals[0]?.description, "Master eigenvalues");

    const misconceptions = await resumed.getOpenMisconceptions("acc1");
    assert.equal(misconceptions.length, 1);
    assert.deepEqual(misconceptions[0]?.evidenceAttemptIds, ["a1"]);

    const evidence = await resumed.getAttempt("a1");
    assert.equal(evidence?.response, "0,0");

    const due = await resumed.getDueReviews("acc1", new Date("2026-09-02T00:00:00.000Z"));
    assert.equal(due.length, 1);
    assert.equal(due[0]?.conceptId, "eigenvalues");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("file store rejects non-absolute roots and path-traversal file names", () => {
  assert.throws(() => new FileLearnerMemory({ root: "relative/dir" }));
  const dir = tempDir();
  try {
    assert.throws(() => new FileLearnerMemory({ root: dir, fileName: "../escape.json" }));
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
