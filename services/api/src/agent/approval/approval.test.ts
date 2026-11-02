import assert from "node:assert/strict";
import test from "node:test";
import type { Principal } from "@learning-platform/agent-contract";
import { InMemoryLearnerMemory } from "../memory/index.js";
import { sequentialIdFactory, steppedClock } from "../support.js";
import { ApprovalService } from "./service.js";

const educator: Principal = { accountId: "educator1", role: "educator" };
const learner: Principal = { accountId: "learner1", role: "b2c_learner" };

function service() {
  const memory = new InMemoryLearnerMemory();
  return new ApprovalService(memory, steppedClock("2026-09-01T12:00:00.000Z"), sequentialIdFactory());
}

test("draft → submit → approve preserves version and provenance", async () => {
  const svc = service();
  const draft = await svc.draft({
    artifactId: "art1",
    action: "publish",
    requestedBy: "agent",
    version: 3,
    provenance: { model: "scripted-fake", citations: ["lesson-eigenvalues"] }
  });
  assert.equal(draft.status, "draft");
  assert.equal(draft.version, 3);

  const submitted = await svc.submit(draft.id);
  assert.equal(submitted.status, "pending");

  const approved = await svc.approve(educator, draft.id, "correct");
  assert.equal(approved.status, "approved");
  assert.equal(approved.decidedBy, "educator1");
  assert.equal(approved.version, 3, "version preserved through decision");
  assert.deepEqual(approved.provenance, { model: "scripted-fake", citations: ["lesson-eigenvalues"] });
});

test("only educators may approve or reject", async () => {
  const svc = service();
  const draft = await svc.draft({ artifactId: "art1", action: "publish", requestedBy: "agent", version: 1 });
  await assert.rejects(() => svc.approve(learner, draft.id), /Only educators/);
  await assert.rejects(() => svc.reject(learner, draft.id, "no"), /Only educators/);
});

test("publish is blocked until an approved publish request exists for that version", async () => {
  const svc = service();
  assert.equal(await svc.isPublishable("art1", 1), false);
  await assert.rejects(() => svc.publish(educator, "art1", 1), /not approved/);

  const draft = await svc.draft({ artifactId: "art1", action: "publish", requestedBy: "agent", version: 1 });
  await svc.approve(educator, draft.id);

  assert.equal(await svc.isPublishable("art1", 1), true);
  await assert.doesNotReject(() => svc.publish(educator, "art1", 1));

  // A different version is still not publishable.
  assert.equal(await svc.isPublishable("art1", 2), false);
});

test("a rejected request cannot then be approved", async () => {
  const svc = service();
  const draft = await svc.draft({ artifactId: "art1", action: "publish", requestedBy: "agent", version: 1 });
  await svc.reject(educator, draft.id, "inaccurate");
  await assert.rejects(() => svc.approve(educator, draft.id), /already rejected/);
});
