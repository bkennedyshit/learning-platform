import assert from "node:assert/strict";
import test from "node:test";
import { normalizeGraspScore } from "./grasp.js";
import { advancePathOnLessonCompletion } from "./paths.js";
import { computeNextReview } from "./reviews.js";
import { getNextStage, getStageOrder, isLessonComplete } from "./stages.js";

test("stage order includes code only for programming subjects", () => {
  assert.deepEqual(getStageOrder(true), ["read", "listen", "write", "code", "handwrite"]);
  assert.deepEqual(getStageOrder(false), ["read", "listen", "write", "handwrite"]);
  assert.equal(getNextStage("write", true), "code");
  assert.equal(getNextStage("write", false), "handwrite");
});

test("lesson completion requires all applicable stages", () => {
  assert.equal(isLessonComplete(new Set(["read", "listen", "write", "handwrite"]), false), true);
  assert.equal(isLessonComplete(new Set(["read", "listen", "write", "handwrite"]), true), false);
  assert.equal(isLessonComplete(new Set(["read", "listen", "write", "code", "handwrite"]), true), true);
});

test("grasp score is rounded, clamped, floored, and flagged consistently", () => {
  assert.deepEqual(normalizeGraspScore(-10), { score: 25, flaggedForReview: true });
  assert.deepEqual(normalizeGraspScore(62.6), { score: 63, flaggedForReview: true });
  assert.deepEqual(normalizeGraspScore(70), { score: 70, flaggedForReview: false });
  assert.deepEqual(normalizeGraspScore(120), { score: 100, flaggedForReview: false });
});

test("review schedule gives shorter intervals for lower scores", () => {
  const now = new Date("2026-06-03T00:00:00.000Z");
  const prior = new Date("2026-05-30T00:00:00.000Z");

  assert.equal(computeNextReview({ score: 65, lastReviewedAt: prior, now }).intervalDays, 1);
  assert.equal(computeNextReview({ score: 75, lastReviewedAt: prior, now }).intervalDays, 6);
  assert.equal(computeNextReview({ score: 95, lastReviewedAt: prior, now }).intervalDays, 9);
});

test("path advance is monotonic and reports completion ratio", () => {
  assert.deepEqual(
    advancePathOnLessonCompletion({
      currentPosition: 0,
      completedCount: 0,
      totalItems: 4
    }),
    {
      currentPosition: 1,
      completedCount: 1,
      totalItems: 4,
      completionRatio: 0.25
    }
  );
});
