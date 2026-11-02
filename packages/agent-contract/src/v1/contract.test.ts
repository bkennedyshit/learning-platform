import assert from "node:assert/strict";
import test from "node:test";
import {
  CONTRACT_VERSION,
  parseAgentSession,
  parseArtifact,
  parseToolCall,
  redactValue,
  validate,
  validateAgentSession,
  validateApprovalRequest,
  validateArtifact,
  validateJob,
  validatePlan,
  validateToolDefinition,
  validateTraceEvent,
  type SchemaNode
} from "./index.js";

test("contract version is v1", () => {
  assert.equal(CONTRACT_VERSION, "v1");
});

test("valid agent session parses; invalid role rejected", () => {
  const session = {
    id: "s1",
    accountId: "acc1",
    role: "b2c_learner",
    status: "active",
    createdAt: "2026-09-01T12:00:00.000Z",
    updatedAt: "2026-09-01T12:00:00.000Z"
  };
  assert.equal(validateAgentSession(session).ok, true);
  assert.doesNotThrow(() => parseAgentSession(session));

  const bad = validateAgentSession({ ...session, role: "wizard" });
  assert.equal(bad.ok, false);
  assert.ok(bad.errors.some((e) => e.path === "$.role"));
});

test("unknown/hidden-reasoning properties are rejected (no chain-of-thought)", () => {
  const trace = {
    id: "t1",
    sessionId: "s1",
    seq: 0,
    type: "decision",
    at: "2026-09-01T12:00:00.000Z",
    summary: "Chose retrieval practice because mastery is low.",
    reasoning: "secret hidden chain of thought"
  };
  const result = validateTraceEvent(trace);
  assert.equal(result.ok, false);
  assert.ok(result.errors.some((e) => e.path === "$.reasoning" && e.message === "unexpected property"));
});

test("trace event without hidden fields validates", () => {
  assert.equal(
    validateTraceEvent({
      id: "t1",
      sessionId: "s1",
      seq: 1,
      type: "tool_call",
      at: "2026-09-01T12:00:00.000Z",
      summary: "curriculum.search"
    }).ok,
    true
  );
});

test("tool definition requires schemas and valid category", () => {
  const def = {
    name: "curriculum.search",
    category: "read",
    description: "search",
    inputSchema: { type: "object", properties: {} },
    outputSchema: { type: "object", properties: {} }
  };
  assert.equal(validateToolDefinition(def).ok, true);
  assert.equal(validateToolDefinition({ ...def, category: "delete_everything" }).ok, false);
});

test("tool input schema round-trips through the generic validator", () => {
  const inputSchema: SchemaNode = {
    type: "object",
    required: ["query"],
    properties: { query: { type: "string", minLength: 1 }, k: { type: "number", integer: true, min: 1 } }
  };
  assert.equal(validate(inputSchema, { query: "vectors", k: 5 }).ok, true);
  assert.equal(validate(inputSchema, { query: "", k: 5 }).ok, false);
  assert.equal(validate(inputSchema, { k: 5 }).ok, false);
  assert.equal(validate(inputSchema, { query: "vectors", k: 1.5 }).ok, false);
});

test("tool call accepts arbitrary input payloads but requires identifiers", () => {
  assert.doesNotThrow(() =>
    parseToolCall({
      id: "c1",
      sessionId: "s1",
      toolName: "practice.submit",
      input: { answer: 42, nested: { anything: true } },
      createdAt: "2026-09-01T12:00:00.000Z"
    })
  );
  assert.throws(() =>
    parseToolCall({ id: "c1", toolName: "x", input: {}, createdAt: "2026-09-01T12:00:00.000Z" })
  );
});

test("plan, job, approval schemas enforce bounds", () => {
  assert.equal(
    validatePlan({
      id: "p1",
      sessionId: "s1",
      goal: "learn eigenvalues",
      revision: 0,
      steps: [{ id: "st1", description: "retrieve", status: "pending" }],
      createdAt: "2026-09-01T12:00:00.000Z"
    }).ok,
    true
  );

  assert.equal(
    validateJob({
      id: "j1",
      sessionId: "s1",
      kind: "build_review_package",
      status: "running",
      progress: 1.5,
      createdAt: "2026-09-01T12:00:00.000Z",
      updatedAt: "2026-09-01T12:00:00.000Z"
    }).ok,
    false,
    "progress above 1 must fail"
  );

  assert.equal(
    validateApprovalRequest({
      id: "a1",
      action: "publish",
      status: "draft",
      artifactId: "art1",
      requestedBy: "agent",
      version: 1,
      createdAt: "2026-09-01T12:00:00.000Z"
    }).ok,
    true
  );
});

test("artifact schema enforces version >= 1 and known kinds", () => {
  const artifact = {
    id: "art1",
    version: 1,
    kind: "svg",
    title: "Unit circle",
    description: "",
    altText: "A labeled unit circle",
    source: "<svg/>",
    sanitizedSource: "<svg/>",
    lessonIds: ["l1"],
    conceptIds: ["trig"],
    createdBy: "agent",
    createdAt: "2026-09-01T12:00:00.000Z"
  };
  assert.doesNotThrow(() => parseArtifact(artifact));
  assert.equal(validateArtifact({ ...artifact, version: 0 }).ok, false);
  assert.equal(validateArtifact({ ...artifact, kind: "gif" }).ok, false);
});

test("redaction masks secret keys and preserves structure", () => {
  const redacted = redactValue({
    email: "a@b.com",
    decision: "advance",
    nested: { apiKey: "sk-123", note: "ok" }
  }) as Record<string, unknown>;
  assert.equal(redacted.email, "[redacted]");
  assert.equal(redacted.decision, "advance");
  assert.deepEqual(redacted.nested, { apiKey: "[redacted]", note: "ok" });
});
