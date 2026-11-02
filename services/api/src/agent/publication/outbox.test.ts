import assert from "node:assert/strict";
import test from "node:test";
import { mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import type { Artifact, ApprovalRequest, Principal } from "@learning-platform/agent-contract";
import { PublicationOutbox, PublicationOutboxError, toFilenameSafe } from "./outbox.js";
import { createLearningAgent } from "../index.js";
import { InMemoryLearnerMemory } from "../memory/index.js";
import { createToolContext } from "../toolRegistry.js";
import { sequentialIdFactory, steppedClock } from "../support.js";

function artifact(id: string, version: number): Artifact {
  return {
    id,
    version,
    kind: "svg",
    title: "Diagonal matrix",
    description: "A diagram",
    altText: "A 2x2 diagonal matrix",
    source: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect width="10" height="10"/></svg>',
    sanitizedSource:
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect width="10" height="10"/></svg>',
    lessonIds: ["lesson-eigenvalues"],
    conceptIds: ["eigenvalues"],
    createdBy: "agent",
    createdAt: "2026-09-01T12:00:00.000Z"
  };
}

function approval(artifactId: string, version: number): ApprovalRequest {
  return {
    id: "approval_0001",
    action: "publish",
    status: "approved",
    artifactId,
    requestedBy: "agent",
    version,
    createdAt: "2026-09-01T12:00:00.000Z",
    decidedBy: "educator1",
    decidedAt: "2026-09-01T12:01:00.000Z",
    provenance: { model: "scripted-fake" }
  };
}

async function withOutbox(fn: (outbox: PublicationOutbox, dir: string) => Promise<void>): Promise<void> {
  const dir = await mkdtemp(path.join(tmpdir(), "outbox-"));
  try {
    await fn(new PublicationOutbox(dir), dir);
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
}

test("filename-safe token strips separators and leading dots", () => {
  assert.equal(toFilenameSafe("artifact_abc-123"), "artifact_abc-123");
  assert.equal(toFilenameSafe("../../etc/passwd"), "_.._etc_passwd");
  assert.equal(toFilenameSafe("...hidden"), "hidden");
});

test("outbox requires an absolute root", () => {
  assert.throws(() => new PublicationOutbox("relative/dir"), PublicationOutboxError);
});

test("approved artifact is written atomically as an immutable, not-public package", async () => {
  await withOutbox(async (outbox) => {
    const result = await outbox.writeReviewedDraft({
      artifact: artifact("artifact_x", 1),
      approval: approval("artifact_x", 1),
      now: "2026-09-01T12:02:00.000Z"
    });
    assert.match(result.relativePath, /^artifact_x__v1\.json$/);

    const pkg = await outbox.readReviewedDraft("artifact_x", 1);
    assert.ok(pkg);
    assert.equal(pkg?.published, false);
    assert.equal(pkg?.artifact.sanitizedSource.includes("<svg"), true);
    assert.equal(pkg?.approval.decidedBy, "educator1");
    assert.deepEqual(pkg?.approval.provenance, { model: "scripted-fake" });
    assert.equal(pkg?.metadata.title, "Diagonal matrix");
  });
});

test("writing the same version twice is refused (immutable); prior version stays recoverable", async () => {
  await withOutbox(async (outbox) => {
    await outbox.writeReviewedDraft({
      artifact: artifact("artifact_x", 1),
      approval: approval("artifact_x", 1),
      now: "2026-09-01T12:02:00.000Z"
    });
    // Re-writing the same version must not clobber the immutable package.
    await assert.rejects(
      () =>
        outbox.writeReviewedDraft({
          artifact: artifact("artifact_x", 1),
          approval: approval("artifact_x", 1),
          now: "2026-09-01T12:03:00.000Z"
        }),
      (err: unknown) => err instanceof PublicationOutboxError && err.code === "exists"
    );

    // A new version writes alongside, and the prior version remains recoverable.
    await outbox.writeReviewedDraft({
      artifact: artifact("artifact_x", 2),
      approval: approval("artifact_x", 2),
      now: "2026-09-01T12:04:00.000Z"
    });
    const v1 = await outbox.readReviewedDraft("artifact_x", 1);
    const v2 = await outbox.readReviewedDraft("artifact_x", 2);
    assert.equal(v1?.version, 1);
    assert.equal(v2?.version, 2);
    assert.deepEqual(await outbox.list(), ["artifact_x__v1.json", "artifact_x__v2.json"]);
  });
});

test("path traversal in artifact id is rejected", async () => {
  await withOutbox(async (outbox) => {
    await assert.rejects(
      () =>
        outbox.writeReviewedDraft({
          artifact: artifact("../escape", 1),
          approval: approval("../escape", 1),
          now: "2026-09-01T12:02:00.000Z"
        }),
      (err: unknown) => err instanceof PublicationOutboxError && err.code === "path_unsafe"
    );
    await assert.rejects(
      () =>
        outbox.writeReviewedDraft({
          artifact: artifact("a/b", 1),
          approval: approval("a/b", 1),
          now: "2026-09-01T12:02:00.000Z"
        }),
      (err: unknown) => err instanceof PublicationOutboxError && err.code === "path_unsafe"
    );
  });
});

test("an unapproved approval record cannot be written", async () => {
  await withOutbox(async (outbox) => {
    const pending = { ...approval("artifact_x", 1), status: "pending" as const };
    await assert.rejects(
      () => outbox.writeReviewedDraft({ artifact: artifact("artifact_x", 1), approval: pending, now: "t" }),
      (err: unknown) => err instanceof PublicationOutboxError && err.code === "invalid"
    );
  });
});

/* ------------------------- educator tool integration ------------------- */

const learner: Principal = { accountId: "learner1", role: "b2c_learner" };
const educator: Principal = { accountId: "educator1", role: "educator", organizationId: "org1" };

function harness(outbox?: PublicationOutbox) {
  const memory = new InMemoryLearnerMemory();
  const clock = steppedClock("2026-09-01T12:00:00.000Z");
  const idFactory = sequentialIdFactory();
  const agent = createLearningAgent({
    memory,
    clock,
    idFactory,
    ...(outbox ? { publicationOutbox: outbox } : {})
  });
  const mkCtx = (principal: Principal) =>
    createToolContext({ principal, memory, fixture: agent.fixture, sessionId: "s1", clock, idFactory });
  return { agent, mkCtx };
}

async function createAndApprove(agent: ReturnType<typeof harness>["agent"], mkCtx: ReturnType<typeof harness>["mkCtx"]) {
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
    mkCtx(learner)
  );
  const artifactId = (created.output as { id: string }).id;
  const draft = await agent.approvals.draft({
    artifactId,
    action: "publish",
    requestedBy: "agent",
    version: 1
  });
  await agent.approvals.approve(educator, draft.id, "looks correct");
  return artifactId;
}

test("publish before approval reports not_approved and never claims published", async () => {
  const { agent, mkCtx } = harness();
  const created = await agent.registry.invoke(
    "visual.create",
    {
      kind: "svg",
      title: "T",
      altText: "alt",
      source: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect width="10" height="10"/></svg>',
      lessonIds: ["lesson-eigenvalues"],
      conceptIds: ["eigenvalues"]
    },
    mkCtx(learner)
  );
  const artifactId = (created.output as { id: string }).id;
  const blocked = await agent.registry.invoke(
    "educator.publish_artifact",
    { artifactId, version: 1 },
    mkCtx(educator)
  );
  assert.equal(blocked.ok, false);
  assert.equal(blocked.error?.code, "not_approved");
});

test("without an outbox, approved publish returns approved_for_reviewed_commit and published:false", async () => {
  const { agent, mkCtx } = harness();
  const artifactId = await createAndApprove(agent, mkCtx);
  const res = await agent.registry.invoke("educator.publish_artifact", { artifactId, version: 1 }, mkCtx(educator));
  assert.equal(res.ok, true);
  const out = res.output as { published: boolean; status: string };
  assert.equal(out.published, false);
  assert.equal(out.status, "approved_for_reviewed_commit");
});

test("with an outbox, approved publish queues an immutable package and stays published:false", async () => {
  await withOutbox(async (outbox) => {
    const { agent, mkCtx } = harness(outbox);
    const artifactId = await createAndApprove(agent, mkCtx);
    const res = await agent.registry.invoke("educator.publish_artifact", { artifactId, version: 1 }, mkCtx(educator));
    assert.equal(res.ok, true);
    const out = res.output as { published: boolean; status: string; outbox?: { packageId: string } };
    assert.equal(out.published, false);
    assert.equal(out.status, "queuedForPublish");
    assert.ok(out.outbox?.packageId);

    const pkg = await outbox.readReviewedDraft(artifactId, 1);
    assert.equal(pkg?.published, false);
    assert.equal(pkg?.artifact.id, artifactId);
  });
});
