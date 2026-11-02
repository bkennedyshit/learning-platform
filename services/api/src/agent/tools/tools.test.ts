import assert from "node:assert/strict";
import test from "node:test";
import type { Principal } from "@learning-platform/agent-contract";
import { createLearningAgent } from "../index.js";
import { InMemoryLearnerMemory } from "../memory/index.js";
import { createToolContext } from "../toolRegistry.js";
import { sequentialIdFactory, steppedClock } from "../support.js";
import { DOMAIN_TOOL_NAMES } from "./domainTools.js";

const learner: Principal = { accountId: "learner1", role: "b2c_learner" };
const educator: Principal = { accountId: "educator1", role: "educator", organizationId: "org1" };

function harness(principal: Principal = learner) {
  const memory = new InMemoryLearnerMemory();
  const clock = steppedClock("2026-09-01T12:00:00.000Z");
  const idFactory = sequentialIdFactory();
  const agent = createLearningAgent({ memory, clock, idFactory });
  const ctx = createToolContext({
    principal,
    memory,
    fixture: agent.fixture,
    sessionId: "session1",
    clock,
    idFactory
  });
  return { memory, agent, ctx };
}

test("all exact handoff tool names are registered with the three categories present", () => {
  const { agent } = harness();
  const names = new Set(agent.registry.list().map((d) => d.name));
  for (const expected of DOMAIN_TOOL_NAMES) {
    assert.ok(names.has(expected), `missing tool ${expected}`);
  }
  assert.ok(agent.registry.listByCategory("read").length > 0);
  assert.ok(agent.registry.listByCategory("state_change").length > 0);
  assert.ok(agent.registry.listByCategory("educator").length > 0);
});

test("invalid input is rejected with a structured invalid_input error", async () => {
  const { agent, ctx } = harness();
  const result = await agent.registry.invoke("curriculum.search", { k: 3 }, ctx);
  assert.equal(result.ok, false);
  assert.equal(result.error?.code, "invalid_input");
});

test("output is validated against the declared schema", async () => {
  const { agent, ctx } = harness();
  const result = await agent.registry.invoke("curriculum.get_lesson", { lessonId: "lesson-eigenvalues" }, ctx);
  assert.equal(result.ok, true);
  const output = result.output as { id: string; title: string };
  assert.equal(output.id, "lesson-eigenvalues");
});

test("recorded goal is retrievable through learner.get_state", async () => {
  const { agent, ctx } = harness();
  const rec = await agent.registry.invoke(
    "learner.record_goal",
    { description: "Master eigenvalues", targetConceptIds: ["eigenvalues"] },
    ctx
  );
  assert.equal(rec.ok, true);
  const state = await agent.registry.invoke("learner.get_state", {}, ctx);
  const output = state.output as { goals: Array<{ description: string }> };
  assert.equal(output.goals[0]?.description, "Master eigenvalues");
});

test("ownership: a learner cannot read another learner's state", async () => {
  const { agent, ctx } = harness();
  const result = await agent.registry.invoke("learner.get_state", { accountId: "someone-else" }, ctx);
  assert.equal(result.ok, false);
  assert.equal(result.error?.code, "policy_denied");
});

test("role: a learner may not invoke an educator-category tool", async () => {
  const { agent, ctx } = harness(learner);
  const result = await agent.registry.invoke(
    "educator.publish_artifact",
    { artifactId: "artifact_x", version: 1 },
    ctx
  );
  assert.equal(result.ok, false);
  assert.equal(result.error?.code, "policy_denied");
});

test("idempotent state change replays the prior output for the same key", async () => {
  const { agent, ctx } = harness();
  const first = await agent.registry.invoke(
    "learner.record_goal",
    { description: "Goal A", targetConceptIds: [] },
    ctx,
    "key-1"
  );
  const second = await agent.registry.invoke(
    "learner.record_goal",
    { description: "Goal A", targetConceptIds: [] },
    ctx,
    "key-1"
  );
  const firstGoal = (first.output as { goal: { id: string } }).goal;
  const secondGoal = (second.output as { goal: { id: string } }).goal;
  assert.equal(firstGoal.id, secondGoal.id, "same idempotency key must yield the same goal id");
});

test("educator can publish only after an approved publish request", async () => {
  const memory = new InMemoryLearnerMemory();
  const clock = steppedClock("2026-09-01T12:00:00.000Z");
  const idFactory = sequentialIdFactory();
  const agent = createLearningAgent({ memory, clock, idFactory });

  // Agent creates an svg artifact on the learner's behalf.
  const learnerCtx = createToolContext({
    principal: learner,
    memory,
    fixture: agent.fixture,
    sessionId: "s1",
    clock,
    idFactory
  });
  const created = await agent.registry.invoke(
    "visual.create",
    {
      kind: "svg",
      title: "Diagonal matrix",
      altText: "A 2x2 diagonal matrix",
      source: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect width="10" height="10"/></svg>',
      lessonIds: ["lesson-eigenvalues"],
      conceptIds: ["eigenvalues"]
    },
    learnerCtx
  );
  assert.equal(created.ok, true);
  const artifactId = (created.output as { id: string; version: number }).id;

  const educatorCtx = createToolContext({
    principal: educator,
    memory,
    fixture: agent.fixture,
    sessionId: "s1",
    clock,
    idFactory
  });

  // Publishing before approval must fail.
  const blocked = await agent.registry.invoke(
    "educator.publish_artifact",
    { artifactId, version: 1 },
    educatorCtx
  );
  assert.equal(blocked.ok, false);
  assert.equal(blocked.error?.code, "not_approved");

  // Draft → approve → publish.
  const draft = await agent.approvals.draft({
    artifactId,
    action: "publish",
    requestedBy: "agent",
    version: 1,
    provenance: { createdBy: "agent" }
  });
  await agent.approvals.approve(educator, draft.id, "looks correct");

  const published = await agent.registry.invoke(
    "educator.publish_artifact",
    { artifactId, version: 1 },
    educatorCtx
  );
  assert.equal(published.ok, true);
});
