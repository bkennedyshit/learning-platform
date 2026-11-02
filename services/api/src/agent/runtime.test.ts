import assert from "node:assert/strict";
import test from "node:test";
import type { Principal } from "@learning-platform/agent-contract";
import { createLearningAgent } from "./index.js";
import { InMemoryLearnerMemory } from "./memory/index.js";
import { createToolContext } from "./toolRegistry.js";
import { ScriptedFakeModel, type AgentModelAction } from "./model.js";
import { runAgent } from "./runtime.js";
import { TraceRecorder } from "./trace.js";
import { JobManager, JobCancelledError } from "./jobs.js";
import { sequentialIdFactory, steppedClock } from "./support.js";

const learner: Principal = { accountId: "learner1", role: "b2c_learner" };

function harness() {
  const memory = new InMemoryLearnerMemory();
  const clock = steppedClock("2026-09-01T12:00:00.000Z");
  const idFactory = sequentialIdFactory();
  const agent = createLearningAgent({ memory, clock, idFactory });
  const trace = new TraceRecorder("session1", memory, clock, idFactory);
  const ctx = createToolContext({
    principal: learner,
    memory,
    fixture: agent.fixture,
    sessionId: "session1",
    clock,
    idFactory,
    trace
  });
  return { memory, agent, ctx };
}

test("scripted model drives a plan-act-observe-adapt run that changes learner state", async () => {
  const { memory, agent, ctx } = harness();
  const script: AgentModelAction[] = [
    { kind: "tool", toolName: "curriculum.get_lesson", input: { lessonId: "lesson-eigenvalues" }, rationaleSummary: "Load the lesson." },
    { kind: "tool", toolName: "learner.record_goal", input: { description: "Master eigenvalues", targetConceptIds: ["eigenvalues"] }, rationaleSummary: "Set a durable goal." },
    { kind: "finish", rationaleSummary: "Goal recorded and lesson loaded." }
  ];
  const result = await runAgent({ goal: "Master eigenvalues", model: new ScriptedFakeModel(script), registry: agent.registry, ctx });

  assert.equal(result.finished, true);
  assert.equal(result.toolResults.length, 2);
  assert.ok(result.toolResults.every((r) => r.ok));

  const goals = await memory.getActiveGoals("learner1");
  assert.equal(goals[0]?.description, "Master eigenvalues");

  const plan = await memory.getPlan(result.plan.id);
  assert.equal(plan?.steps.length, 2);
  assert.ok(plan?.steps.every((s) => s.status === "done"));
});

test("trace records observable decisions and tool activity without hidden reasoning", async () => {
  const { memory, agent, ctx } = harness();
  const script: AgentModelAction[] = [
    { kind: "tool", toolName: "curriculum.search", input: { query: "eigenvalue" }, rationaleSummary: "Find grounding passages." },
    { kind: "finish", rationaleSummary: "Enough context gathered." }
  ];
  await runAgent({ goal: "explain eigenvalues", model: new ScriptedFakeModel(script), registry: agent.registry, ctx });

  const traces = await memory.getTraces("session1");
  const types = traces.map((t) => t.type);
  assert.ok(types.includes("plan_created"));
  assert.ok(types.includes("decision"));
  assert.ok(types.includes("tool_call"));
  assert.ok(types.includes("tool_result"));
  assert.ok(types.includes("observation"));
  // No trace event may carry a hidden reasoning field.
  for (const t of traces) {
    assert.ok(!("reasoning" in t));
    if (t.data) {
      assert.ok(!("reasoning" in t.data));
    }
  }
});

test("failed tool calls surface as structured errors and mark the plan step failed", async () => {
  const { agent, ctx } = harness();
  const script: AgentModelAction[] = [
    { kind: "tool", toolName: "curriculum.get_lesson", input: { lessonId: "missing" }, rationaleSummary: "Attempt to load a missing lesson." },
    { kind: "finish", rationaleSummary: "Stop after error." }
  ];
  const result = await runAgent({ goal: "x", model: new ScriptedFakeModel(script), registry: agent.registry, ctx });
  assert.equal(result.toolResults[0]?.ok, false);
  assert.equal(result.toolResults[0]?.error?.code, "not_found");
  assert.equal(result.plan.steps[0]?.status, "failed");
});

test("job manager reports progress and reaches succeeded", async () => {
  const manager = new JobManager(steppedClock("2026-09-01T12:00:00.000Z"), sequentialIdFactory());
  const handle = manager.start({
    sessionId: "s1",
    kind: "build_review_package",
    worker: async ({ reportProgress }) => {
      await reportProgress(0.5, "halfway");
      await reportProgress(1, "done");
      return ["artifact_1"];
    }
  });
  const job = await handle.done;
  assert.equal(job.status, "succeeded");
  assert.deepEqual(job.resultArtifactIds, ["artifact_1"]);
  assert.ok(manager.getEvents(handle.jobId).length >= 2);
});

test("job manager cancels a cooperative worker", async () => {
  const manager = new JobManager(steppedClock("2026-09-01T12:00:00.000Z"), sequentialIdFactory());
  const handle = manager.start({
    sessionId: "s1",
    kind: "long_job",
    worker: async ({ reportProgress }) => {
      await reportProgress(0.2);
      // Cancelled between progress reports; next report throws.
      await reportProgress(0.4);
      return ["never"];
    }
  });
  manager.cancel(handle.jobId);
  const job = await handle.done;
  assert.equal(job.status, "cancelled");
});

test("JobCancelledError is exported for callers", () => {
  assert.equal(new JobCancelledError().name, "JobCancelledError");
});
