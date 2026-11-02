import type {
  AgentSession,
  ApprovalAction,
  Principal
} from "@learning-platform/agent-contract";
import { SESSION_COOKIE_NAME } from "../auth/session.js";
import type { Goal } from "../agent/memory/index.js";
import { createToolContext } from "../agent/toolRegistry.js";
import { TraceRecorder } from "../agent/trace.js";
import type { App } from "./app.js";
import {
  badRequest,
  forbidden,
  HttpError,
  methodNotAllowed,
  notFound,
  payloadTooLarge,
  unauthenticated
} from "./errors.js";
import { runTurn } from "./runTurn.js";

const HEALTH_PATHS = new Set(["/healthz", "/readyz"]);

export type FetchHandler = (request: Request) => Promise<Response>;

/** Build a fetch-style handler bound to an {@link App}. Easy to test with global Request/Response. */
export function createFetchHandler(app: App): FetchHandler {
  return async (request: Request): Promise<Response> => {
    const url = new URL(request.url);
    const cors = corsHeadersFor(app, request);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors });
    }

    try {
      const body = await route(app, request, url);
      return json(body.status, body.data, { ...cors, ...(body.headers ?? {}) });
    } catch (err) {
      if (err instanceof HttpError) {
        return json(err.status, { error: err.toStructured() }, cors);
      }
      const message = err instanceof Error ? err.message : "Internal error.";
      return json(500, { error: { code: "internal_error", message, retryable: true } }, cors);
    }
  };
}

interface RouteResult {
  status: number;
  data: unknown;
  headers?: Record<string, string>;
}

async function route(app: App, request: Request, url: URL): Promise<RouteResult> {
  const { pathname } = url;
  const method = request.method.toUpperCase();

  // Health/readiness are the only unauthenticated routes.
  if (pathname === "/healthz") {
    return { status: 200, data: { status: "ok" } };
  }
  if (pathname === "/readyz") {
    return { status: 200, data: { status: "ready" } };
  }
  if (HEALTH_PATHS.has(pathname)) {
    return { status: 200, data: { status: "ok" } };
  }

  // Dev-session is gated but does not require a prior session.
  if (pathname === "/v1/auth/dev-session") {
    return devSession(app, request, method);
  }

  // Everything else requires a valid signed session.
  const principal = requirePrincipal(app, request);

  if (pathname === "/v1/auth/session" && method === "GET") {
    return { status: 200, data: { principal } };
  }

  if (pathname === "/v1/agent/sessions" && method === "POST") {
    return createOrResumeSession(app, request, principal);
  }

  const sessionTurns = pathname.match(/^\/v1\/agent\/sessions\/([^/]+)\/turns$/);
  if (sessionTurns) {
    if (method !== "POST") throw methodNotAllowed();
    return postTurn(app, request, principal, decodeURIComponent(sessionTurns[1] ?? ""));
  }

  const sessionGet = pathname.match(/^\/v1\/agent\/sessions\/([^/]+)$/);
  if (sessionGet) {
    if (method !== "GET") throw methodNotAllowed();
    return getSession(app, principal, decodeURIComponent(sessionGet[1] ?? ""));
  }

  const toolCall = pathname.match(/^\/v1\/tools\/([^/]+)$/);
  if (toolCall) {
    if (method !== "POST") throw methodNotAllowed();
    return dispatchTool(app, request, principal, decodeURIComponent(toolCall[1] ?? ""));
  }

  const jobCancel = pathname.match(/^\/v1\/agent\/jobs\/([^/]+)\/cancel$/);
  if (jobCancel) {
    if (method !== "POST") throw methodNotAllowed();
    return cancelJob(app, principal, decodeURIComponent(jobCancel[1] ?? ""));
  }

  const jobGet = pathname.match(/^\/v1\/agent\/jobs\/([^/]+)$/);
  if (jobGet) {
    if (method !== "GET") throw methodNotAllowed();
    return getJob(app, principal, decodeURIComponent(jobGet[1] ?? ""));
  }

  if (pathname === "/v1/agent/approvals" && method === "POST") {
    return requestApproval(app, request, principal);
  }

  const approvalDecision = pathname.match(/^\/v1\/agent\/approvals\/([^/]+)\/decision$/);
  if (approvalDecision) {
    if (method !== "POST") throw methodNotAllowed();
    return decideApproval(app, request, principal, decodeURIComponent(approvalDecision[1] ?? ""));
  }

  throw notFound(`No route for ${method} ${pathname}`);
}

/* ------------------------------- handlers ------------------------------- */

async function devSession(app: App, request: Request, method: string): Promise<RouteResult> {
  if (method !== "POST") throw methodNotAllowed();
  if (!app.config.allowDevAuth) {
    throw forbidden("Dev authentication is disabled. Set ALLOW_DEV_AUTH=true to enable it.");
  }
  const body = await readJson<{ accountId?: string; role?: Principal["role"]; organizationId?: string }>(
    app,
    request
  );
  const principal: Principal = {
    accountId: body.accountId?.trim() || "dev-learner",
    role: body.role ?? "b2c_learner",
    ...(body.organizationId ? { organizationId: body.organizationId } : {})
  };
  const token = app.signer.sign(principal);
  return {
    status: 200,
    data: { principal, token },
    headers: { "set-cookie": app.signer.toCookie(token) }
  };
}

async function createOrResumeSession(app: App, request: Request, principal: Principal): Promise<RouteResult> {
  const body = await readJson<{
    sessionId?: string;
    lessonId?: string;
    goal?: { description: string; targetConceptIds?: string[] };
  }>(app, request);

  if (body.sessionId) {
    const existing = await app.memory.getSession(body.sessionId);
    if (existing) {
      assertSessionOwner(principal, existing);
      return { status: 200, data: { session: existing, resumed: true } };
    }
  }

  const now = app.clock().toISOString();
  let goal: Goal | undefined;
  if (body.goal?.description) {
    goal = await app.memory.upsertGoal({
      id: app.idFactory("goal"),
      accountId: principal.accountId,
      description: body.goal.description,
      targetConceptIds: body.goal.targetConceptIds ?? [],
      status: "active",
      createdAt: now,
      updatedAt: now
    });
  }

  const session: AgentSession = {
    id: app.idFactory("session"),
    accountId: principal.accountId,
    role: principal.role,
    status: "active",
    ...(goal ? { goalId: goal.id } : {}),
    ...(body.lessonId ? { lessonId: body.lessonId } : {}),
    createdAt: now,
    updatedAt: now
  };
  await app.memory.saveSession(session);
  return { status: 201, data: { session, resumed: false, ...(goal ? { goal } : {}) } };
}

async function getSession(app: App, principal: Principal, sessionId: string): Promise<RouteResult> {
  const session = await requireOwnedSession(app, principal, sessionId);
  const [turns, traces, summary] = await Promise.all([
    app.memory.getTurns(sessionId),
    app.memory.getTraces(sessionId),
    app.memory.getSessionSummary(sessionId)
  ]);
  return { status: 200, data: { session, turns, traces, summary: summary ?? null } };
}

async function postTurn(app: App, request: Request, principal: Principal, sessionId: string): Promise<RouteResult> {
  const session = await requireOwnedSession(app, principal, sessionId);
  const body = await readJson<{ message?: string; lessonId?: string; conceptId?: string }>(app, request);
  const message = body.message?.trim();
  if (!message) {
    throw badRequest("A non-empty `message` is required.");
  }
  const result = await runTurn(app, {
    principal,
    session,
    message,
    ...(body.lessonId ? { lessonId: body.lessonId } : {}),
    ...(body.conceptId ? { conceptId: body.conceptId } : {})
  });
  return { status: 200, data: result };
}

async function dispatchTool(app: App, request: Request, principal: Principal, name: string): Promise<RouteResult> {
  const body = await readJson<{ sessionId?: string; input?: unknown; idempotencyKey?: string }>(app, request);
  if (!body.sessionId) {
    throw badRequest("`sessionId` is required to invoke a tool.");
  }
  const session = await requireOwnedSession(app, principal, body.sessionId);
  const trace = new TraceRecorder(session.id, app.memory, app.clock, app.idFactory);
  const ctx = createToolContext({
    principal,
    memory: app.memory,
    fixture: app.agent.fixture,
    sessionId: session.id,
    clock: app.clock,
    idFactory: app.idFactory,
    trace
  });
  const result = await app.agent.registry.invoke(name, body.input, ctx, body.idempotencyKey);
  // Policy denials surface as a structured tool error, not an HTTP error, so the
  // caller still receives the ToolResult shape. Status stays 200.
  return { status: 200, data: { result } };
}

async function getJob(app: App, principal: Principal, jobId: string): Promise<RouteResult> {
  const job = app.agent.jobs.get(jobId);
  if (!job) throw notFound(`Job ${jobId} not found.`);
  await requireOwnedSession(app, principal, job.sessionId);
  return { status: 200, data: { job, events: app.agent.jobs.getEvents(jobId) } };
}

async function cancelJob(app: App, principal: Principal, jobId: string): Promise<RouteResult> {
  const job = app.agent.jobs.get(jobId);
  if (!job) throw notFound(`Job ${jobId} not found.`);
  await requireOwnedSession(app, principal, job.sessionId);
  app.agent.jobs.cancel(jobId);
  return { status: 200, data: { job: app.agent.jobs.get(jobId) } };
}

async function requestApproval(app: App, request: Request, principal: Principal): Promise<RouteResult> {
  const body = await readJson<{
    artifactId?: string;
    action?: ApprovalAction;
    version?: number;
    sessionId?: string;
  }>(app, request);
  if (!body.artifactId || !body.action || typeof body.version !== "number") {
    throw badRequest("`artifactId`, `action`, and numeric `version` are required.");
  }
  if (body.sessionId) {
    await requireOwnedSession(app, principal, body.sessionId);
  }
  const draft = await app.agent.approvals.draft({
    artifactId: body.artifactId,
    action: body.action,
    requestedBy: principal.accountId,
    version: body.version,
    ...(body.sessionId ? { sessionId: body.sessionId } : {})
  });
  const submitted = await app.agent.approvals.submit(draft.id);
  return { status: 201, data: { approval: submitted } };
}

async function decideApproval(
  app: App,
  request: Request,
  principal: Principal,
  approvalId: string
): Promise<RouteResult> {
  const body = await readJson<{ decision?: "approve" | "reject"; reason?: string }>(app, request);
  if (body.decision === "approve") {
    const approval = await app.agent.approvals.approve(principal, approvalId, body.reason);
    return { status: 200, data: { approval } };
  }
  if (body.decision === "reject") {
    if (!body.reason) throw badRequest("A `reason` is required to reject an approval.");
    const approval = await app.agent.approvals.reject(principal, approvalId, body.reason);
    return { status: 200, data: { approval } };
  }
  throw badRequest('`decision` must be "approve" or "reject".');
}

/* ------------------------------- helpers -------------------------------- */

function requirePrincipal(app: App, request: Request): Principal {
  const token = readToken(request);
  const principal = token ? app.signer.verify(token) : undefined;
  if (!principal) {
    throw unauthenticated();
  }
  return principal;
}

/** Accept either a signed session cookie or an `Authorization: Bearer` token. */
function readToken(request: Request): string | undefined {
  const auth = request.headers.get("authorization");
  if (auth && /^Bearer\s+/i.test(auth)) {
    return auth.replace(/^Bearer\s+/i, "").trim() || undefined;
  }
  const cookie = request.headers.get("cookie");
  return readCookieValue(cookie, SESSION_COOKIE_NAME);
}

function readCookieValue(cookieHeader: string | null, name: string): string | undefined {
  if (!cookieHeader) return undefined;
  for (const part of cookieHeader.split(";")) {
    const trimmed = part.trim();
    const eq = trimmed.indexOf("=");
    if (eq === -1) continue;
    if (trimmed.slice(0, eq) === name) {
      return trimmed.slice(eq + 1);
    }
  }
  return undefined;
}

async function requireOwnedSession(app: App, principal: Principal, sessionId: string): Promise<AgentSession> {
  const session = await app.memory.getSession(sessionId);
  if (!session) {
    throw notFound(`Session ${sessionId} not found.`);
  }
  assertSessionOwner(principal, session);
  return session;
}

/** Reject cross-account session access. Educators may read within their org. */
function assertSessionOwner(principal: Principal, session: AgentSession): void {
  if (session.accountId === principal.accountId) return;
  const educatorRoles = new Set(["educator", "org_admin", "platform_admin"]);
  if (
    educatorRoles.has(principal.role) &&
    principal.organizationId !== undefined &&
    principal.organizationId === (session as { organizationId?: string }).organizationId
  ) {
    return;
  }
  throw forbidden("You may not access another account's session.");
}

async function readJson<T>(app: App, request: Request): Promise<T> {
  const declared = request.headers.get("content-length");
  if (declared && Number(declared) > app.config.maxBodyBytes) {
    throw payloadTooLarge();
  }
  const text = await request.text();
  if (Buffer.byteLength(text, "utf8") > app.config.maxBodyBytes) {
    throw payloadTooLarge();
  }
  if (text.trim().length === 0) {
    return {} as T;
  }
  try {
    return JSON.parse(text) as T;
  } catch {
    throw badRequest("Request body must be valid JSON.");
  }
}

function corsHeadersFor(app: App, request: Request): Record<string, string> {
  const origin = request.headers.get("origin");
  if (!origin || app.config.corsOrigins.length === 0 || !app.config.corsOrigins.includes(origin)) {
    return {};
  }
  return {
    "access-control-allow-origin": origin,
    "access-control-allow-credentials": "true",
    "access-control-allow-methods": "GET,POST,OPTIONS",
    "access-control-allow-headers": "content-type,authorization",
    vary: "Origin"
  };
}

function json(status: number, data: unknown, headers: Record<string, string> = {}): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json", ...headers }
  });
}
