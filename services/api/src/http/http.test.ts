import assert from "node:assert/strict";
import test from "node:test";
import { createApp, type CreateAppOverrides } from "./app.js";
import { createFetchHandler } from "./handler.js";
import { InMemoryLearnerMemory } from "../agent/memory/index.js";
import { sequentialIdFactory } from "../agent/support.js";

const SECRET = "0123456789abcdef0123456789abcdef";

interface Harness {
  handler: (req: Request) => Promise<Response>;
  setNow: (iso: string) => void;
}

function harness(configOverrides: Partial<CreateAppOverrides["config"]> = {}): Harness {
  const clockRef = { now: new Date("2026-09-01T12:00:00.000Z").getTime() };
  const overrides: CreateAppOverrides = {
    memory: new InMemoryLearnerMemory(),
    idFactory: sequentialIdFactory(),
    clock: () => new Date(clockRef.now),
    config: {
      sessionSecret: SECRET,
      allowDevAuth: true,
      secureCookie: true,
      sessionTtlMs: 1000 * 60 * 60,
      ...configOverrides
    }
  };
  const app = createApp(overrides);
  return {
    handler: createFetchHandler(app),
    setNow: (iso) => {
      clockRef.now = new Date(iso).getTime();
    }
  };
}

function req(path: string, init: RequestInit = {}): Request {
  return new Request(`http://localhost${path}`, init);
}

function cookieToken(res: Response): string {
  const setCookie = res.headers.get("set-cookie") ?? "";
  const token = setCookie.split(";")[0]?.split("=")[1];
  assert.ok(token, "expected a session cookie");
  return token;
}

async function devLogin(h: Harness, principal: Record<string, unknown> = {}): Promise<string> {
  const res = await h.handler(
    req("/v1/auth/dev-session", { method: "POST", body: JSON.stringify(principal) })
  );
  assert.equal(res.status, 200);
  return cookieToken(res);
}

test("healthz and readyz require no authentication", async () => {
  const h = harness();
  const health = await h.handler(req("/healthz"));
  assert.equal(health.status, 200);
  assert.deepEqual(await health.json(), { status: "ok" });
  const ready = await h.handler(req("/readyz"));
  assert.equal(ready.status, 200);
});

test("dev-session is gated by ALLOW_DEV_AUTH", async () => {
  const disabled = harness({ allowDevAuth: false });
  const denied = await disabled.handler(req("/v1/auth/dev-session", { method: "POST", body: "{}" }));
  assert.equal(denied.status, 403);

  const enabled = harness({ allowDevAuth: true });
  const ok = await enabled.handler(req("/v1/auth/dev-session", { method: "POST", body: "{}" }));
  assert.equal(ok.status, 200);
  assert.ok(ok.headers.get("set-cookie"));
});

test("non-health routes reject missing or tampered tokens", async () => {
  const h = harness();
  const noAuth = await h.handler(req("/v1/auth/session"));
  assert.equal(noAuth.status, 401);

  const token = await devLogin(h);
  const tampered = await h.handler(req("/v1/auth/session", { headers: { cookie: `learning_session=${token}x` } }));
  assert.equal(tampered.status, 401);

  const valid = await h.handler(req("/v1/auth/session", { headers: { cookie: `learning_session=${token}` } }));
  assert.equal(valid.status, 200);
});

test("bearer tokens authenticate the same as cookies", async () => {
  const h = harness();
  const token = await devLogin(h);
  const res = await h.handler(req("/v1/auth/session", { headers: { authorization: `Bearer ${token}` } }));
  assert.equal(res.status, 200);
  const body = (await res.json()) as { principal: { accountId: string } };
  assert.equal(body.principal.accountId, "dev-learner");
});

test("sessions expire after the configured TTL", async () => {
  const h = harness({ sessionTtlMs: 1000 * 60 }); // 1 minute
  const token = await devLogin(h);

  const beforeExpiry = await h.handler(req("/v1/auth/session", { headers: { cookie: `learning_session=${token}` } }));
  assert.equal(beforeExpiry.status, 200);

  h.setNow("2026-09-01T13:00:00.000Z"); // well past TTL
  const afterExpiry = await h.handler(req("/v1/auth/session", { headers: { cookie: `learning_session=${token}` } }));
  assert.equal(afterExpiry.status, 401);
});

test("cross-account session access is rejected", async () => {
  const h = harness();
  const tokenA = await devLogin(h, { accountId: "learner-a" });
  const created = await h.handler(
    req("/v1/agent/sessions", {
      method: "POST",
      headers: { cookie: `learning_session=${tokenA}`, "content-type": "application/json" },
      body: JSON.stringify({ goal: { description: "Master eigenvalues" } })
    })
  );
  assert.equal(created.status, 201);
  const { session } = (await created.json()) as { session: { id: string } };

  const tokenB = await devLogin(h, { accountId: "learner-b" });
  const forbidden = await h.handler(
    req(`/v1/agent/sessions/${session.id}`, { headers: { cookie: `learning_session=${tokenB}` } })
  );
  assert.equal(forbidden.status, 403);

  const owner = await h.handler(
    req(`/v1/agent/sessions/${session.id}`, { headers: { cookie: `learning_session=${tokenA}` } })
  );
  assert.equal(owner.status, 200);
});

test("tool policy denies educator-only tools to a learner", async () => {
  const h = harness();
  const token = await devLogin(h, { accountId: "learner-a", role: "b2c_learner" });
  const created = await h.handler(
    req("/v1/agent/sessions", {
      method: "POST",
      headers: { cookie: `learning_session=${token}`, "content-type": "application/json" },
      body: "{}"
    })
  );
  const { session } = (await created.json()) as { session: { id: string } };

  const res = await h.handler(
    req("/v1/tools/educator.publish_artifact", {
      method: "POST",
      headers: { cookie: `learning_session=${token}`, "content-type": "application/json" },
      body: JSON.stringify({ sessionId: session.id, input: { artifactId: "a1", version: 1 } })
    })
  );
  assert.equal(res.status, 200);
  const { result } = (await res.json()) as { result: { ok: boolean; error?: { code: string } } };
  assert.equal(result.ok, false);
  assert.equal(result.error?.code, "policy_denied");
});

test("a turn runs the registry/runtime and returns plan, tool activity, and a reply", async () => {
  const h = harness();
  const token = await devLogin(h, { accountId: "learner-a" });
  const created = await h.handler(
    req("/v1/agent/sessions", {
      method: "POST",
      headers: { cookie: `learning_session=${token}`, "content-type": "application/json" },
      body: JSON.stringify({ lessonId: "lesson-eigenvalues" })
    })
  );
  const { session } = (await created.json()) as { session: { id: string } };

  const turn = await h.handler(
    req(`/v1/agent/sessions/${session.id}/turns`, {
      method: "POST",
      headers: { cookie: `learning_session=${token}`, "content-type": "application/json" },
      body: JSON.stringify({ message: "What is an eigenvalue?", lessonId: "lesson-eigenvalues" })
    })
  );
  assert.equal(turn.status, 200);
  const data = (await turn.json()) as {
    plan: { steps: unknown[] };
    toolSummaries: Array<{ toolName: string; ok: boolean }>;
    turns: Array<{ author: string; content: string }>;
    whyNext: string;
    citations: unknown[];
  };
  assert.ok(data.plan.steps.length > 0);
  assert.ok(data.toolSummaries.some((s) => s.toolName === "tutor.explain" && s.ok));
  assert.ok(data.turns.some((t) => t.author === "agent" && t.content.length > 0));
  assert.ok(data.whyNext.length > 0);
  assert.ok(data.citations.length > 0);
});

test("request bodies over the size limit are rejected", async () => {
  const h = harness({ maxBodyBytes: 64 });
  const token = await devLogin(h);
  const big = JSON.stringify({ goal: { description: "x".repeat(200) } });
  const res = await h.handler(
    req("/v1/agent/sessions", {
      method: "POST",
      headers: { cookie: `learning_session=${token}`, "content-type": "application/json" },
      body: big
    })
  );
  assert.equal(res.status, 413);
});
