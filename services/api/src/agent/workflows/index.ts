import type { Artifact } from "@learning-platform/agent-contract";
import { safeEvaluate } from "./calculator.js";
import {
  callTool,
  runAdaptiveTeaching,
  type AdaptiveTeachingInput,
  type AdaptiveTeachingResult,
  type WorkflowDeps
} from "./teaching.js";

export * from "./teaching.js";
export * from "./calculator.js";

/** The five reusable teaching workflows shipped by the framework. */
export const WORKFLOW_NAMES = [
  "explain_visually",
  "diagnose_and_repair",
  "build_study_plan",
  "lesson_to_review_package",
  "explore_with_calculator"
] as const;
export type WorkflowName = (typeof WORKFLOW_NAMES)[number];

/* --------------------------- explain visually --------------------------- */

export interface ExplainVisuallyInput {
  lessonId: string;
  conceptId: string;
  title: string;
  altText: string;
  svgSource: string;
}

export interface ExplainVisuallyResult {
  explanation: { content: string; grounded: boolean };
  artifact: Artifact;
  comprehensionQuestion: string;
  saved: boolean;
}

export async function explainVisually(
  deps: WorkflowDeps,
  input: ExplainVisuallyInput
): Promise<ExplainVisuallyResult> {
  const explanation = await callTool<{ content: string; grounded: boolean }>(deps, "tutor.explain", {
    lessonId: input.lessonId
  });
  const artifact = await callTool<Artifact>(deps, "visual.create", {
    kind: "svg",
    title: input.title,
    altText: input.altText,
    source: input.svgSource,
    lessonIds: [input.lessonId],
    conceptIds: [input.conceptId]
  });
  await callTool<Artifact>(deps, "visual.present", { artifactId: artifact.id });
  const question = await callTool<{ question: string }>(deps, "tutor.ask_socratic", {
    conceptId: input.conceptId
  });
  const saved = await callTool<{ saved: boolean }>(deps, "artifact.save", { artifactId: artifact.id });
  return { explanation, artifact, comprehensionQuestion: question.question, saved: saved.saved };
}

/* ----------------------- diagnose and repair --------------------------- */

export async function diagnoseAndRepair(
  deps: WorkflowDeps,
  input: AdaptiveTeachingInput
): Promise<AdaptiveTeachingResult> {
  return runAdaptiveTeaching(deps, input);
}

/* --------------------------- build study plan --------------------------- */

export interface BuildStudyPlanInput {
  goalDescription: string;
  title: string;
  lessonIds: string[];
  targetConceptIds?: string[];
}

export interface BuildStudyPlanResult {
  goal: { id: string; description: string };
  artifactId: string;
  steps: Array<{ lessonId: string; order: number; done: boolean }>;
}

export async function buildStudyPlan(
  deps: WorkflowDeps,
  input: BuildStudyPlanInput
): Promise<BuildStudyPlanResult> {
  const goalResult = await callTool<{ goal: { id: string; description: string } }>(deps, "learner.record_goal", {
    description: input.goalDescription,
    targetConceptIds: input.targetConceptIds ?? []
  });
  const plan = await callTool<{ artifactId: string; steps: BuildStudyPlanResult["steps"] }>(
    deps,
    "study_plan.create",
    { title: input.title, lessonIds: input.lessonIds }
  );
  return { goal: goalResult.goal, artifactId: plan.artifactId, steps: plan.steps };
}

/* --------------------- lesson to review package ------------------------- */

export interface LessonToReviewPackageInput {
  lessonId: string;
  conceptId: string;
  summary: string;
  flashcards: Array<{ front: string; back: string }>;
  masteryScore: number;
}

export interface LessonToReviewPackageResult {
  summaryArtifactId: string;
  flashcardArtifactId: string;
  review: { conceptId: string; dueAt: string; intervalDays: number };
}

export async function lessonToReviewPackage(
  deps: WorkflowDeps,
  input: LessonToReviewPackageInput
): Promise<LessonToReviewPackageResult> {
  const summary = await callTool<Artifact>(deps, "visual.create", {
    kind: "note",
    title: `Summary: ${input.lessonId}`,
    altText: `Summary of ${input.lessonId}`,
    source: input.summary,
    lessonIds: [input.lessonId],
    conceptIds: [input.conceptId]
  });
  const flashcards = await callTool<Artifact>(deps, "visual.create", {
    kind: "flashcard",
    title: `Flashcards: ${input.lessonId}`,
    altText: `Flashcards for ${input.lessonId}`,
    source: JSON.stringify({ cards: input.flashcards }),
    lessonIds: [input.lessonId],
    conceptIds: [input.conceptId]
  });
  const review = await callTool<{ conceptId: string; dueAt: string; intervalDays: number }>(
    deps,
    "review.schedule",
    { conceptId: input.conceptId, lessonId: input.lessonId, score: input.masteryScore }
  );
  return { summaryArtifactId: summary.id, flashcardArtifactId: flashcards.id, review };
}

/* ------------------------ explore with calculator ----------------------- */

export interface ExploreWithCalculatorInput {
  expression: string;
  prediction: number;
  tolerance?: number;
}

export interface ExploreWithCalculatorResult {
  expression: string;
  result: number;
  prediction: number;
  matchesPrediction: boolean;
}

export function exploreWithCalculator(input: ExploreWithCalculatorInput): ExploreWithCalculatorResult {
  const result = safeEvaluate(input.expression);
  const tolerance = input.tolerance ?? 1e-9;
  return {
    expression: input.expression,
    result,
    prediction: input.prediction,
    matchesPrediction: Math.abs(result - input.prediction) <= tolerance
  };
}
