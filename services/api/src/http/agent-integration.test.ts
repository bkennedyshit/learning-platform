import assert from "node:assert/strict";
import test from "node:test";
import { mkdtempSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import type { Artifact, Citation, TraceEvent } from "@learning-platform/agent-contract";
import { createApp, type CreateAppOverrides } from "./app.js";
import { createFetchHandler } from "./handler.js";
import { InMemoryLearnerMemory } from "../agent/memory/index.js";
import { sequentialIdFactory } from "../agent/support.js";
import { ScriptedFakeModel, type AgentModelAction } from "../agent/model.js";

const SECRET = "0123456789abcdef0123456789abcdef";

function makeHandler(overrides: CreateAppOverrides = {}) {
  const clockRef = { now: new Date("2026-09-01T12:00:00.000Z").getTime() };
  const app = createApp({
    memory: new InMemoryLearnerMemory(),
    idFactory: sequentialIdFactory(),
    clock: () => new Date(clockRef.now),
    ...overrides,
    config: { sessionSecret: SECRET, allowDevAuth: true, ...(overrides.config ?? {}) }
  });
  return createFetchHandler(app);
}

function req(path: string, init: RequestInit = {}): Request {
  return new Request(`http://localhost${path}`, init);
}

async function devLogin(handler: (r: Request) => Promise<Response>): Promise<string> {
  const res = await handler(req("/v1/auth/dev-session", { method: "POST", body: "{}" }));
  const setCookie = res.headers.get("set-cookie") ?? "";
  return setCookie.split(";")[0]?.split("=")[1] ?? "";
}

async function startSession(
  handler: (r: Request) => Promise<Response>,
  token: string,
  lessonId?: string
): Promise<string> {
  const res = await handler(
    req("/v1/agent/sessions", {
      method: "POST",
      headers: { cookie: `learning_session=${token}`, "content-type": "application/json" },
      body: JSON.stringify(lessonId ? { lessonId } : {})
    })
  );
  const { session } = (await res.json()) as { session: { id: string } };
  return session.id;
}

function writeMiniCatalog(): { file: string; cleanup: () => void } {
  const dir = mkdtempSync(path.join(tmpdir(), "catalog-http-"));
  const file = path.join(dir, "content.json");
  writeFileSync(
    file,
    JSON.stringify({
      subjects: [],
      lessons: {
        "calvin-cycle": {
          slug: "calvin-cycle",
          title: "The Calvin Cycle",
          subject: "Biology",
          subjectSlug: "biology",
          html: "<p>The Calvin cycle fixes carbon dioxide into glucose using ATP and NADPH.</p>",
          prevSlug: null,
          nextSlug: null
        }
      }
    }),
    "utf8"
  );
  return { file, cleanup: () => rmSync(dir, { recursive: true, force: true }) };
}

test("a turn grounds citations in a real (non-seed) catalog slug", async () => {
  const { file, cleanup } = writeMiniCatalog();
  try {
    const handler = makeHandler({ config: { sessionSecret: SECRET, allowDevAuth: true, agentCatalogPath: file } });
    const token = await devLogin(handler);
    const sessionId = await startSession(handler, token, "calvin-cycle");

    const turn = await handler(
      req(`/v1/agent/sessions/${sessionId}/turns`, {
        method: "POST",
        headers: { cookie: `learning_session=${token}`, "content-type": "application/json" },
        body: JSON.stringify({ message: "Explain how the Calvin cycle fixes carbon", lessonId: "calvin-cycle" })
      })
    );
    assert.equal(turn.status, 200);
    const data = (await turn.json()) as {
      citations: Citation[];
      toolSummaries: Array<{ toolName: string; ok: boolean }>;
    };
    assert.ok(data.toolSummaries.some((s) => s.toolName === "tutor.explain" && s.ok));
    assert.ok(data.citations.length > 0, "expected grounded citations");
    assert.ok(data.citations.every((c) => c.lessonId === "calvin-cycle"));
  } finally {
    cleanup();
  }
});

test("a visual request produces a sanitized SVG artifact with export metadata", async () => {
  const handler = makeHandler();
  const token = await devLogin(handler);
  const sessionId = await startSession(handler, token, "lesson-eigenvalues");

  const turn = await handler(
    req(`/v1/agent/sessions/${sessionId}/turns`, {
      method: "POST",
      headers: { cookie: `learning_session=${token}`, "content-type": "application/json" },
      body: JSON.stringify({
        message: "Can you draw me a diagram of eigenvalues?",
        lessonId: "lesson-eigenvalues",
        conceptId: "eigenvalues"
      })
    })
  );
  assert.equal(turn.status, 200);
  const data = (await turn.json()) as {
    artifacts: Artifact[];
    toolSummaries: Array<{ toolName: string; ok: boolean }>;
    turns: Array<{ author: string; artifactIds?: string[] }>;
  };
  assert.ok(data.toolSummaries.some((s) => s.toolName === "visual.create" && s.ok));
  assert.equal(data.artifacts.length, 1);
  const artifact = data.artifacts[0]!;
  assert.equal(artifact.kind, "svg");
  assert.ok(artifact.sanitizedSource.startsWith("<svg"), "artifact must carry the sanitized SVG");
  assert.ok(artifact.sanitizedSource.includes("<title>"), "SVG must be accessible with a title");
  assert.ok(artifact.exports?.some((e) => e.format === "svg" && !e.fallback));
  assert.ok(artifact.exports?.some((e) => e.format === "png"));
  assert.ok(artifact.conceptIds.includes("eigenvalues"));
  const agentTurn = data.turns.find((t) => t.author === "agent");
  assert.ok(agentTurn?.artifactIds?.includes(artifact.id));
});

test("an injected provider-style model yields the same trace shape as scripted planning", async () => {
  async function traceTypesFor(overrides: CreateAppOverrides): Promise<string[]> {
    const handler = makeHandler(overrides);
    const token = await devLogin(handler);
    const sessionId = await startSession(handler, token, "lesson-eigenvalues");
    await handler(
      req(`/v1/agent/sessions/${sessionId}/turns`, {
        method: "POST",
        headers: { cookie: `learning_session=${token}`, "content-type": "application/json" },
        body: JSON.stringify({ message: "What is an eigenvalue?", lessonId: "lesson-eigenvalues" })
      })
    );
    const sessionRes = await handler(
      req(`/v1/agent/sessions/${sessionId}`, { headers: { cookie: `learning_session=${token}` } })
    );
    const { traces } = (await sessionRes.json()) as { traces: TraceEvent[] };
    return traces.map((t) => t.type);
  }

  // Deterministic scripted default.
  const scripted = await traceTypesFor({});

  // A fake AgentModel driving the identical typed tool sequence (as a hosted or
  // local provider would once it returns these actions). Provider payloads never
  // enter tools — the model only emits tool names + validated inputs.
  const providerScript: AgentModelAction[] = [
    {
      kind: "tool",
      toolName: "curriculum.get_lesson",
      input: { lessonId: "lesson-eigenvalues" },
      rationaleSummary: "Load the lesson the learner is reading for grounding."
    },
    {
      kind: "tool",
      toolName: "tutor.explain",
      input: { lessonId: "lesson-eigenvalues", question: "What is an eigenvalue?" },
      rationaleSummary: "Ground an explanation in the lesson passages."
    },
    {
      kind: "tool",
      toolName: "curriculum.search",
      input: { query: "What is an eigenvalue?", lessonId: "lesson-eigenvalues" },
      rationaleSummary: "Retrieve supporting passages for the question."
    },
    { kind: "finish", rationaleSummary: "Gathered grounding; responding to the learner." }
  ];
  const fakeModel = new ScriptedFakeModel(providerScript, "fake-provider");
  const provider = await traceTypesFor({ agentModelFactory: () => fakeModel });

  assert.deepEqual(provider, scripted, "provider-driven trace shape must match scripted planning");
});
