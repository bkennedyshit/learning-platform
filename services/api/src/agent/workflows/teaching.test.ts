import assert from "node:assert/strict";
import test from "node:test";
import type { Principal } from "@learning-platform/agent-contract";
import { createLearningAgent } from "../index.js";
import { InMemoryLearnerMemory } from "../memory/index.js";
import { createToolContext } from "../toolRegistry.js";
import { sequentialIdFactory, steppedClock } from "../support.js";
import {
  WORKFLOW_NAMES,
  buildStudyPlan,
  explainVisually,
  exploreWithCalculator,
  runAdaptiveTeaching,
  type WorkflowDeps
} from "./index.js";

const learner: Principal = { accountId: "learner1", role: "b2c_learner" };

function deps(): { deps: WorkflowDeps; memory: InMemoryLearnerMemory } {
  const memory = new InMemoryLearnerMemory();
  const clock = steppedClock("2026-09-01T12:00:00.000Z");
  const idFactory = sequentialIdFactory();
  const agent = createLearningAgent({ memory, clock, idFactory });
  const ctx = createToolContext({
    principal: learner,
    memory,
    fixture: agent.fixture,
    sessionId: "session1",
    clock,
    idFactory
  });
  return { deps: { registry: agent.registry, ctx }, memory };
}

test("all five reusable workflow names are declared", () => {
  assert.deepEqual([...WORKFLOW_NAMES], [
    "explain_visually",
    "diagnose_and_repair",
    "build_study_plan",
    "lesson_to_review_package",
    "explore_with_calculator"
  ]);
});

test("adaptive teaching: a WRONG answer triggers a misconception-targeted intervention and a retest", async () => {
  const { deps: d, memory } = deps();
  const result = await runAdaptiveTeaching(d, { lessonId: "lesson-eigenvalues", answer: "0,0" });

  assert.equal(result.correct, false);
  assert.ok(result.misconception, "expected a diagnosed misconception");
  assert.ok(result.intervention, "expected an intervention on a wrong answer");
  assert.equal(result.retestRequested, true);
  assert.ok(result.intervention?.hint.length);
  assert.ok(result.intervention?.socratic.length);

  const open = await memory.getOpenMisconceptions("learner1");
  assert.equal(open.length, 1);
  assert.equal(open[0]?.conceptId, "eigenvalues");
});

test("adaptive teaching: a CORRECT answer advances without repetition and resolves misconceptions", async () => {
  const { deps: d, memory } = deps();
  const result = await runAdaptiveTeaching(d, { lessonId: "lesson-eigenvalues", answer: "2,3" });

  assert.equal(result.correct, true);
  assert.equal(result.retestRequested, false);
  assert.equal(result.intervention, undefined);
  assert.ok(result.masteryAfter > 0.3, "mastery should increase on a correct answer");
  assert.ok(result.review.dueAt.length > 0);

  const mastery = await memory.getMastery("learner1", "eigenvalues");
  assert.ok((mastery?.mastery ?? 0) > 0.3);
});

test("explain visually creates a sanitized svg artifact, presents it, and saves it", async () => {
  const { deps: d } = deps();
  const result = await explainVisually(d, {
    lessonId: "lesson-eigenvalues",
    conceptId: "eigenvalues",
    title: "Eigenvector direction",
    altText: "A vector unchanged in direction after transformation",
    svgSource:
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><line x1="10" y1="90" x2="90" y2="10" stroke="black"/></svg>'
  });
  assert.equal(result.artifact.kind, "svg");
  assert.ok(result.artifact.sanitizedSource.includes("<line"));
  assert.ok(result.artifact.exports?.some((e) => e.format === "png" && e.fallback));
  assert.ok(result.artifact.exports?.some((e) => e.format === "svg" && !e.fallback));
  assert.equal(result.saved, true);
  assert.ok(result.comprehensionQuestion.length > 0);
});

test("build study plan records a goal and an ordered plan", async () => {
  const { deps: d, memory } = deps();
  const result = await buildStudyPlan(d, {
    goalDescription: "Understand eigenvalues",
    title: "Linear algebra path",
    lessonIds: ["lesson-matrix-multiplication", "lesson-eigenvalues"],
    targetConceptIds: ["eigenvalues"]
  });
  assert.equal(result.steps.length, 2);
  assert.equal(result.steps[0]?.order, 0);
  const goals = await memory.getActiveGoals("learner1");
  assert.equal(goals.length, 1);
});

test("explore with calculator evaluates safely and compares against a prediction", () => {
  const ok = exploreWithCalculator({ expression: "2 * (3 + 4)", prediction: 14 });
  assert.equal(ok.result, 14);
  assert.equal(ok.matchesPrediction, true);

  const miss = exploreWithCalculator({ expression: "10 / 2 - 1", prediction: 5 });
  assert.equal(miss.result, 4);
  assert.equal(miss.matchesPrediction, false);

  assert.throws(() => exploreWithCalculator({ expression: "process.exit(1)", prediction: 0 }));
});
