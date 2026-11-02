import type {
  AgentSession,
  Artifact,
  Citation,
  ConversationTurn,
  Plan,
  PlanStep
} from "@learning-platform/agent-contract";

export const AGENT_BASE = "/api/agent";

export interface ToolActivity {
  toolName: string;
  ok: boolean;
  summary: string;
}

export interface TurnView {
  session?: AgentSession;
  turns: ConversationTurn[];
  plan?: Plan;
  currentStep?: PlanStep;
  toolSummaries: ToolActivity[];
  citations: Citation[];
  artifacts: Artifact[];
  whyNext: string;
}

/**
 * Normalize an untrusted turn/session response into a stable shape with safe
 * defaults. Pure and dependency-free so it is unit-testable without the network.
 */
export function normalizeTurnResponse(raw: unknown): TurnView {
  const r = (raw ?? {}) as Record<string, unknown>;
  const turns = Array.isArray(r.turns) ? (r.turns as ConversationTurn[]) : [];
  const toolSummaries = Array.isArray(r.toolSummaries)
    ? (r.toolSummaries as unknown[]).filter(isToolActivity)
    : [];
  const citations = Array.isArray(r.citations)
    ? (r.citations as unknown[]).filter(isCitation)
    : [];
  const artifacts = Array.isArray(r.artifacts)
    ? (r.artifacts as unknown[]).filter(isArtifact)
    : [];
  const plan = isPlan(r.plan) ? r.plan : undefined;
  const currentStep = isPlanStep(r.currentStep) ? r.currentStep : undefined;

  return {
    ...(isSession(r.session) ? { session: r.session } : {}),
    turns,
    ...(plan ? { plan } : {}),
    ...(currentStep ? { currentStep } : {}),
    toolSummaries,
    citations,
    artifacts,
    whyNext: typeof r.whyNext === "string" ? r.whyNext : ""
  };
}

function isToolActivity(v: unknown): v is ToolActivity {
  return !!v && typeof v === "object" && typeof (v as ToolActivity).toolName === "string";
}
function isCitation(v: unknown): v is Citation {
  return !!v && typeof v === "object" && typeof (v as Citation).lessonId === "string";
}
function isArtifact(v: unknown): v is Artifact {
  return (
    !!v &&
    typeof v === "object" &&
    typeof (v as Artifact).id === "string" &&
    typeof (v as Artifact).kind === "string"
  );
}
function isPlan(v: unknown): v is Plan {
  return !!v && typeof v === "object" && Array.isArray((v as Plan).steps);
}
function isPlanStep(v: unknown): v is PlanStep {
  return !!v && typeof v === "object" && typeof (v as PlanStep).description === "string";
}
function isSession(v: unknown): v is AgentSession {
  return !!v && typeof v === "object" && typeof (v as AgentSession).id === "string";
}

export interface ApiResult<T> {
  ok: boolean;
  data?: T;
  error?: string;
  status: number;
  /** True when the request was cancelled via an AbortSignal. */
  aborted?: boolean;
}

async function call<T>(path: string, init: RequestInit): Promise<ApiResult<T>> {
  try {
    const res = await fetch(`${AGENT_BASE}${path}`, {
      ...init,
      headers: { "content-type": "application/json", ...(init.headers ?? {}) }
    });
    const status = res.status;
    let body: unknown = undefined;
    try {
      body = await res.json();
    } catch {
      /* non-JSON */
    }
    if (!res.ok) {
      const message =
        (body as { error?: { message?: string } })?.error?.message ?? `Request failed (${status}).`;
      return { ok: false, error: message, status };
    }
    return { ok: true, data: body as T, status };
  } catch (err) {
    // An aborted fetch is a caller-initiated cancellation, not a service outage.
    if (err instanceof DOMException && err.name === "AbortError") {
      return { ok: false, error: "Cancelled.", status: 0, aborted: true };
    }
    return { ok: false, error: "The learning agent is unavailable right now.", status: 0 };
  }
}

export function ensureDevSession(principal: Record<string, unknown> = {}): Promise<ApiResult<unknown>> {
  return call("/v1/auth/dev-session", { method: "POST", body: JSON.stringify(principal) });
}

export interface CreateSessionInput {
  sessionId?: string;
  lessonId?: string;
  goal?: { description: string; targetConceptIds?: string[] };
}

export function createOrResumeSession(
  input: CreateSessionInput
): Promise<ApiResult<{ session: AgentSession; resumed: boolean }>> {
  return call("/v1/agent/sessions", { method: "POST", body: JSON.stringify(input) });
}

export function sendTurn(
  sessionId: string,
  input: { message: string; lessonId?: string; conceptId?: string },
  signal?: AbortSignal
): Promise<ApiResult<TurnView>> {
  return call(`/v1/agent/sessions/${encodeURIComponent(sessionId)}/turns`, {
    method: "POST",
    body: JSON.stringify(input),
    ...(signal ? { signal } : {})
  });
}
