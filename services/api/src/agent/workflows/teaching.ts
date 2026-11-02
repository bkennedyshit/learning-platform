import type { ToolContext, ToolRegistry } from "../toolRegistry.js";

export interface WorkflowDeps {
  registry: ToolRegistry;
  ctx: ToolContext;
}

/** Invoke a tool and return its typed output, throwing on failure. */
export async function callTool<T>(
  { registry, ctx }: WorkflowDeps,
  name: string,
  input: unknown,
  idempotencyKey?: string
): Promise<T> {
  const result = await registry.invoke(name, input, ctx, idempotencyKey);
  if (!result.ok) {
    throw new Error(`${name} failed: ${result.error?.code ?? "error"} ${result.error?.message ?? ""}`.trim());
  }
  return result.output as T;
}

export interface AdaptiveTeachingInput {
  lessonId: string;
  answer: string;
  problemId?: string;
}

export interface AdaptiveTeachingResult {
  explanation: { content: string; citations: Array<{ lessonId: string; passageId: string }>; grounded: boolean };
  problemId: string;
  conceptId: string;
  correct: boolean;
  misconception?: { conceptId: string; description: string };
  intervention?: { hint: string; socratic: string; reteach: string };
  retestRequested: boolean;
  masteryAfter: number;
  review: { conceptId: string; dueAt: string; intervalDays: number };
}

/**
 * Adaptive teaching loop: teach → test → diagnose → reteach → schedule review.
 *
 * A wrong answer triggers a misconception-targeted intervention and requests a
 * fresh check; a correct answer advances without unnecessary repetition. All
 * effects flow through the typed tool registry (policy + validation enforced).
 */
export async function runAdaptiveTeaching(
  deps: WorkflowDeps,
  input: AdaptiveTeachingInput
): Promise<AdaptiveTeachingResult> {
  // 1. TEACH — grounded explanation.
  const explanation = await callTool<AdaptiveTeachingResult["explanation"]>(deps, "tutor.explain", {
    lessonId: input.lessonId
  });

  // 2. TEST — select a problem.
  const next = await callTool<{ available: boolean; problem?: { id: string; conceptId: string } }>(
    deps,
    "practice.get_next",
    { lessonId: input.lessonId }
  );
  if (!next.available || !next.problem) {
    throw new Error(`No practice problem available for lesson ${input.lessonId}`);
  }
  const problemId = input.problemId ?? next.problem.id;
  const conceptId = next.problem.conceptId;

  // 3. Submit the observable answer.
  const submission = await callTool<{
    attemptId: string;
    correct: boolean;
    score: number;
    misconception?: { conceptId: string; description: string };
  }>(deps, "practice.submit", { problemId, answer: input.answer });

  // 4. DIAGNOSE + RETEACH on failure only.
  let intervention: AdaptiveTeachingResult["intervention"];
  let retestRequested = false;
  if (!submission.correct) {
    const hint = await callTool<{ hint: string }>(deps, "tutor.hint", { problemId });
    const socratic = await callTool<{ question: string }>(deps, "tutor.ask_socratic", { conceptId });
    const reteach = await callTool<{ content: string }>(deps, "tutor.explain", {
      lessonId: input.lessonId,
      question: submission.misconception?.description ?? "clarify the core definition"
    });
    intervention = { hint: hint.hint, socratic: socratic.question, reteach: reteach.content };
    retestRequested = true;
  }

  // 5. Update mastery from the attempt.
  const assessment = await callTool<{ conceptId: string; mastery: number }>(deps, "assessment.evaluate", {
    attemptId: submission.attemptId
  });

  // 6. Schedule the next spaced review.
  const review = await callTool<{ conceptId: string; dueAt: string; intervalDays: number }>(
    deps,
    "review.schedule",
    { conceptId, lessonId: input.lessonId, score: assessment.mastery }
  );

  return {
    explanation,
    problemId,
    conceptId,
    correct: submission.correct,
    ...(submission.misconception ? { misconception: submission.misconception } : {}),
    ...(intervention ? { intervention } : {}),
    retestRequested,
    masteryAfter: assessment.mastery,
    review
  };
}
