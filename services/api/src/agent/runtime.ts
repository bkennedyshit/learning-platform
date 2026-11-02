import type { Plan, PlanStep, ToolResult } from "@learning-platform/agent-contract";
import type { AgentModel, ModelObservation } from "./model.js";
import type { ToolContext, ToolRegistry } from "./toolRegistry.js";

export interface RunAgentInput {
  goal: string;
  model: AgentModel;
  registry: ToolRegistry;
  ctx: ToolContext;
  maxSteps?: number;
  modelContext?: {
    learnerMessage?: string;
    lessonId?: string;
    conceptId?: string;
  };
}

export interface RunAgentResult {
  finished: boolean;
  plan: Plan;
  toolResults: ToolResult[];
  observations: ModelObservation[];
  finalAction?: import("./model.js").AgentModelAction;
}

function summarizeResult(result: ToolResult): string {
  if (result.ok) {
    return `${result.toolName} ok`;
  }
  return `${result.toolName} error: ${result.error?.code ?? "unknown"}`;
}

/**
 * Deterministic plan → act → observe → adapt loop. Each step asks the model for
 * one action, records an observable decision, invokes the chosen tool through
 * the registry (which enforces policy, validation, idempotency), observes the
 * result, and adapts the plan. The loop is bounded by {@link RunAgentInput.maxSteps}.
 */
export async function runAgent(input: RunAgentInput): Promise<RunAgentResult> {
  const { goal, model, registry, ctx } = input;
  const maxSteps = input.maxSteps ?? 12;

  const plan: Plan = {
    id: ctx.idFactory("plan"),
    sessionId: ctx.sessionId,
    goal,
    revision: 0,
    steps: [],
    createdAt: ctx.clock().toISOString()
  };
  await ctx.trace?.emit("plan_created", `Plan for goal: ${goal}`, { goal });

  const toolCatalog = registry.list();
  const observations: ModelObservation[] = [];
  const toolResults: ToolResult[] = [];
  let finished = false;
  let finalAction: import("./model.js").AgentModelAction | undefined;

  for (let step = 0; step < maxSteps; step++) {
    const action = await model.planStep({
      goal,
      step,
      toolCatalog,
      observations,
      ...(input.modelContext ? { context: input.modelContext } : {})
    });
    await ctx.trace?.emit("decision", action.rationaleSummary, {
      kind: action.kind,
      ...(action.toolName ? { toolName: action.toolName } : {})
    });

    if (action.kind === "finish" || !action.toolName) {
      finished = true;
      finalAction = action;
      break;
    }

    const planStep: PlanStep = {
      id: ctx.idFactory("step"),
      description: action.rationaleSummary,
      status: "active",
      toolName: action.toolName
    };
    plan.steps.push(planStep);
    plan.revision += 1;

    const result = await registry.invoke(action.toolName, action.input, ctx, action.idempotencyKey);
    toolResults.push(result);

    const observation: ModelObservation = {
      toolName: result.toolName,
      ok: result.ok,
      summary: summarizeResult(result),
      output: result.output
    };
    observations.push(observation);
    await ctx.trace?.emit("observation", observation.summary, { ok: result.ok });

    // adapt: mark the step done or failed for the next iteration.
    planStep.status = result.ok ? "done" : "failed";
    await ctx.trace?.emit("plan_revised", `Plan revision ${plan.revision}`, {
      revision: plan.revision,
      lastStepStatus: planStep.status
    });
  }

  await ctx.memory.savePlan(plan);
  return {
    finished,
    plan,
    toolResults,
    observations,
    ...(finalAction ? { finalAction } : {})
  };
}
