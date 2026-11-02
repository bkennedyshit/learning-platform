import type {
  AgentSession,
  Artifact,
  Citation,
  ConversationTurn,
  Plan,
  PlanStep,
  Principal,
  ToolResult
} from "@learning-platform/agent-contract";
import { runAgent } from "../agent/runtime.js";
import { createToolContext } from "../agent/toolRegistry.js";
import { TraceRecorder } from "../agent/trace.js";
import { ScriptedFakeModel, type AgentModelAction } from "../agent/model.js";
import type { App } from "./app.js";

export interface RunTurnInput {
  principal: Principal;
  session: AgentSession;
  message: string;
  lessonId?: string;
  conceptId?: string;
}

export interface ToolActivity {
  toolName: string;
  ok: boolean;
  summary: string;
}

export interface TurnResponse {
  session: AgentSession;
  turns: ConversationTurn[];
  plan: Plan;
  currentStep?: PlanStep;
  toolSummaries: ToolActivity[];
  citations: Citation[];
  artifacts: Artifact[];
  whyNext: string;
}

/** Detects a learner request for a visual/diagram/drawing/"show me" artifact. */
const VISUAL_INTENT = /\b(visual(?:ize|ise)?|diagram|draw|sketch|illustrat|show me|picture|graph it|chart)\b/i;

export function wantsVisual(message: string): boolean {
  return VISUAL_INTENT.test(message);
}

/**
 * Build a deterministic, valid, accessible SVG tied to a lesson/concept. It is
 * intentionally simple (title + desc + labeled rect/text) so it always passes
 * the server-side sanitizer allowlist and renders identically across runs.
 */
export function buildDeterministicSvg(title: string): string {
  const safeTitle = title.replace(/[<>&"]/g, "").slice(0, 80) || "Concept";
  return [
    '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="180" viewBox="0 0 320 180" role="img" ',
    `aria-label="Concept diagram for ${safeTitle}">`,
    `<title>${safeTitle}</title>`,
    `<desc>A labeled concept diagram illustrating ${safeTitle}.</desc>`,
    '<rect x="8" y="8" width="304" height="164" rx="12" fill="#f4f7fb" stroke="#3b5bdb" stroke-width="2"/>',
    '<circle cx="80" cy="90" r="34" fill="#dbe4ff" stroke="#3b5bdb" stroke-width="2"/>',
    '<line x1="114" y1="90" x2="210" y2="90" stroke="#3b5bdb" stroke-width="2"/>',
    '<rect x="210" y="62" width="90" height="56" rx="8" fill="#dbe4ff" stroke="#3b5bdb" stroke-width="2"/>',
    `<text x="160" y="150" text-anchor="middle" font-size="14" font-family="sans-serif" fill="#1a1a1a">${safeTitle}</text>`,
    "</svg>"
  ].join("");
}

/**
 * Build a deterministic, provider-free plan for a learner turn. This does NOT
 * duplicate any domain logic: it only names which existing typed tools to run
 * for the message. When a provider is configured the same runtime can be driven
 * by an {@link import("../agent/model.js").AgentModel} instead.
 */
function buildTurnScript(input: RunTurnInput): AgentModelAction[] {
  const script: AgentModelAction[] = [];
  if (input.lessonId) {
    script.push({
      kind: "tool",
      toolName: "curriculum.get_lesson",
      input: { lessonId: input.lessonId },
      rationaleSummary: "Load the lesson the learner is reading for grounding."
    });
    script.push({
      kind: "tool",
      toolName: "tutor.explain",
      input: { lessonId: input.lessonId, question: input.message },
      rationaleSummary: "Ground an explanation in the lesson passages."
    });
  }
  script.push({
    kind: "tool",
    toolName: "curriculum.search",
    input: { query: input.message, ...(input.lessonId ? { lessonId: input.lessonId } : {}) },
    rationaleSummary: "Retrieve supporting passages for the question."
  });
  if (wantsVisual(input.message)) {
    const title = input.conceptId ?? input.lessonId ?? "concept";
    script.push({
      kind: "tool",
      toolName: "visual.create",
      input: {
        kind: "svg",
        title: `Diagram: ${title}`,
        altText: `Concept diagram for ${title}`,
        description: `Auto-generated concept diagram tied to ${title}.`,
        source: buildDeterministicSvg(title),
        ...(input.lessonId ? { lessonIds: [input.lessonId] } : { lessonIds: [] }),
        ...(input.conceptId ? { conceptIds: [input.conceptId] } : { conceptIds: [] })
      },
      rationaleSummary: "Create a labeled visual because the learner asked to see it."
    });
  }
  script.push({ kind: "finish", rationaleSummary: "Gathered grounding; responding to the learner." });
  return script;
}

function isArtifactShaped(value: unknown): value is Artifact {
  return (
    !!value &&
    typeof value === "object" &&
    typeof (value as Artifact).id === "string" &&
    typeof (value as Artifact).sanitizedSource === "string" &&
    typeof (value as Artifact).kind === "string"
  );
}

function collectCitations(results: ToolResult[]): Citation[] {
  const seen = new Set<string>();
  const citations: Citation[] = [];
  const add = (lessonId?: unknown, passageId?: unknown) => {
    if (typeof lessonId !== "string") return;
    const key = `${lessonId}:${typeof passageId === "string" ? passageId : ""}`;
    if (seen.has(key)) return;
    seen.add(key);
    citations.push(typeof passageId === "string" ? { lessonId, passageId } : { lessonId });
  };
  for (const r of results) {
    if (!r.ok || !r.output || typeof r.output !== "object") continue;
    const out = r.output as Record<string, unknown>;
    if (Array.isArray(out.citations)) {
      for (const c of out.citations as Array<Record<string, unknown>>) {
        add(c.lessonId, c.passageId);
      }
    }
    if (Array.isArray(out.results)) {
      for (const c of out.results as Array<Record<string, unknown>>) {
        add(c.lessonId, c.passageId);
      }
    }
    if (Array.isArray(out.passages)) {
      for (const c of out.passages as Array<Record<string, unknown>>) {
        add(c.lessonId, c.passageId);
      }
    }
  }
  return citations;
}

function agentReplyContent(results: ToolResult[], fallback: string): string {
  const explain = results.find((r) => r.toolName === "tutor.explain" && r.ok);
  const content = explain?.output && (explain.output as { content?: unknown }).content;
  if (typeof content === "string" && content.trim().length > 0) {
    return content;
  }
  return fallback;
}

/**
 * Run one conversation turn: append the learner message, drive the typed
 * registry/runtime, append the agent reply, and return the plan, current step,
 * learner-friendly tool activity, citations, artifacts, and a "why this next"
 * explanation grounded in what actually ran.
 */
export async function runTurn(app: App, input: RunTurnInput): Promise<TurnResponse> {
  const { memory, agent, clock, idFactory } = app;
  const sessionId = input.session.id;

  const existing = await memory.getTurns(sessionId);
  const learnerTurn: ConversationTurn = {
    id: idFactory("turn"),
    sessionId,
    index: existing.length,
    author: "learner",
    content: input.message,
    createdAt: clock().toISOString()
  };
  await memory.appendTurn(learnerTurn);

  const trace = new TraceRecorder(sessionId, memory, clock, idFactory);
  const ctx = createToolContext({
    principal: input.principal,
    memory,
    fixture: agent.fixture,
    sessionId,
    clock,
    idFactory,
    trace
  });

  const goal = input.session.summary ?? input.message;
  // Provider-driven when a model factory is configured; otherwise deterministic
  // scripted planning. Both drive the identical typed runtime and trace shape.
  const model = app.agentModelFactory ? app.agentModelFactory(input) : new ScriptedFakeModel(buildTurnScript(input));
  const run = await runAgent({
    goal,
    model,
    registry: agent.registry,
    ctx,
    modelContext: {
      learnerMessage: input.message,
      ...(input.lessonId ? { lessonId: input.lessonId } : {}),
      ...(input.conceptId ? { conceptId: input.conceptId } : {})
    }
  });

  const toolSummaries: ToolActivity[] = run.observations.map((o) => ({
    toolName: o.toolName,
    ok: o.ok,
    summary: friendlySummary(o.toolName, o.ok)
  }));

  const citations = collectCitations(run.toolResults);

  const artifacts: Artifact[] = [];
  for (const r of run.toolResults) {
    if (r.ok && isArtifactShaped(r.output)) {
      artifacts.push(r.output);
    }
  }

  const okTools = run.toolResults.filter((r) => r.ok).map((r) => r.toolName);
  const whyNext =
    okTools.length > 0
      ? `I ran ${okTools.join(", ")} to ground my answer in your lesson before replying.`
      : "I could not reach the curriculum tools, so I answered from your question directly.";

  const providerResponse = run.finalAction?.response?.trim();
  const replyContent =
    providerResponse ||
    agentReplyContent(
      run.toolResults,
      "I could not ground this in the lesson right now, but here is what I can help with — try asking about a specific concept."
    );

  const agentTurn: ConversationTurn = {
    id: idFactory("turn"),
    sessionId,
    index: existing.length + 1,
    author: "agent",
    content: replyContent,
    createdAt: clock().toISOString(),
    ...(artifacts.length ? { artifactIds: artifacts.map((a) => a.id) } : {}),
    ...(citations.length ? { citations } : {})
  };
  await memory.appendTurn(agentTurn);

  const updatedSession: AgentSession = {
    ...input.session,
    ...(input.lessonId ? { lessonId: input.lessonId } : {}),
    updatedAt: clock().toISOString()
  };
  await memory.saveSession(updatedSession);
  await memory.setSessionSummary({
    sessionId,
    accountId: input.principal.accountId,
    summary: replyContent.slice(0, 280),
    sourceLessonIds: citations.map((c) => c.lessonId),
    updatedAt: clock().toISOString()
  });

  const currentStep = run.plan.steps[run.plan.steps.length - 1];

  return {
    session: updatedSession,
    turns: [...existing, learnerTurn, agentTurn],
    plan: run.plan,
    ...(currentStep ? { currentStep } : {}),
    toolSummaries,
    citations,
    artifacts,
    whyNext
  };
}

function friendlySummary(toolName: string, ok: boolean): string {
  const label: Record<string, string> = {
    "curriculum.get_lesson": "Read the current lesson",
    "curriculum.search": "Searched the lesson for relevant passages",
    "tutor.explain": "Prepared a grounded explanation",
    "tutor.hint": "Prepared a hint",
    "tutor.ask_socratic": "Prepared a guiding question",
    "practice.get_next": "Selected a practice problem",
    "practice.submit": "Checked your answer",
    "assessment.evaluate": "Updated your mastery estimate",
    "review.schedule": "Scheduled a spaced review",
    "visual.create": "Created a labeled visual",
    "visual.revise": "Revised the visual",
    "visual.present": "Prepared the visual for display"
  };
  const base = label[toolName] ?? toolName;
  return ok ? base : `${base} (unavailable)`;
}
