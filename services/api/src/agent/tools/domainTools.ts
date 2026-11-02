import {
  artifactSchema,
  type Artifact,
  type SchemaNode
} from "@learning-platform/agent-contract";
import { computeNextReview } from "../../learning/reviews.js";
import { getStageOrder, isLessonComplete, type ModalityStage } from "../../learning/stages.js";
import type { ArtifactService } from "../artifacts/index.js";
import type { ApprovalService } from "../approval/index.js";
import type { PublicationOutbox, PublicationOutboxError } from "../publication/index.js";
import { assertAccountAccess, isEducator } from "../policy.js";
import type { AgentTool, ToolContext } from "../toolRegistry.js";
import { ToolError } from "../toolRegistry.js";
import type {
  Attempt,
  ConceptMastery,
  Goal,
  Misconception,
  ReviewRecord
} from "../memory/index.js";

const clamp01 = (n: number): number => Math.min(1, Math.max(0, n));

/* ------------------------------- schemas -------------------------------- */

const s = {
  str: { type: "string", minLength: 1 } as SchemaNode,
  optStr: { type: "string" } as SchemaNode,
  strArr: { type: "array", items: { type: "string", minLength: 1 } } as SchemaNode,
  bool: { type: "boolean" } as SchemaNode,
  int: { type: "number", integer: true, min: 0 } as SchemaNode,
  ratio: { type: "number", min: 0, max: 1 } as SchemaNode
};

function obj(
  properties: Record<string, SchemaNode>,
  required: string[],
  additionalProperties = false
): SchemaNode {
  return { type: "object", properties, required, additionalProperties };
}

/* --------------------------- curriculum tools --------------------------- */

function curriculumSearch(): AgentTool {
  return {
    definition: {
      name: "curriculum.search",
      category: "read",
      description: "Search lesson passages and return grounded citations.",
      inputSchema: obj({ query: s.str, lessonId: s.str, k: s.int }, ["query"]),
      outputSchema: obj(
        {
          passages: {
            type: "array",
            items: obj({ lessonId: s.str, passageId: s.str, text: s.optStr, score: { type: "number" } }, [
              "lessonId",
              "passageId",
              "text",
              "score"
            ])
          },
          lessonRefs: s.strArr
        },
        ["passages", "lessonRefs"]
      )
    },
    async execute(input: { query: string; lessonId?: string; k?: number }, ctx: ToolContext) {
      const hits = ctx.fixture.search(input.query, input.lessonId).slice(0, input.k ?? 8);
      return {
        passages: hits,
        lessonRefs: [...new Set(hits.map((h) => h.lessonId))]
      };
    }
  };
}

function curriculumGetLesson(): AgentTool {
  return {
    definition: {
      name: "curriculum.get_lesson",
      category: "read",
      description: "Fetch a lesson by id.",
      inputSchema: obj({ lessonId: s.str }, ["lessonId"]),
      outputSchema: obj(
        {
          id: s.str,
          subjectId: s.str,
          slug: s.str,
          title: s.str,
          body: s.optStr,
          conceptIds: s.strArr,
          prerequisiteLessonIds: s.strArr,
          isProgrammingSubject: s.bool
        },
        ["id", "subjectId", "slug", "title", "body", "conceptIds", "prerequisiteLessonIds", "isProgrammingSubject"]
      )
    },
    async execute(input: { lessonId: string }, ctx: ToolContext) {
      const lesson = ctx.fixture.getLesson(input.lessonId);
      if (!lesson) {
        throw new ToolError("not_found", `Lesson ${input.lessonId} not found`);
      }
      return {
        id: lesson.id,
        subjectId: lesson.subjectId,
        slug: lesson.slug,
        title: lesson.title,
        body: lesson.body,
        conceptIds: lesson.conceptIds,
        prerequisiteLessonIds: lesson.prerequisiteLessonIds,
        isProgrammingSubject: lesson.isProgrammingSubject
      };
    }
  };
}

function curriculumGetPrerequisites(): AgentTool {
  return {
    definition: {
      name: "curriculum.get_prerequisites",
      category: "read",
      description: "List prerequisite lessons for a lesson.",
      inputSchema: obj({ lessonId: s.str }, ["lessonId"]),
      outputSchema: obj(
        { prerequisites: { type: "array", items: obj({ id: s.str, title: s.str }, ["id", "title"]) } },
        ["prerequisites"]
      )
    },
    async execute(input: { lessonId: string }, ctx: ToolContext) {
      return {
        prerequisites: ctx.fixture.getPrerequisites(input.lessonId).map((l) => ({ id: l.id, title: l.title }))
      };
    }
  };
}

/* ----------------------------- learner tools ---------------------------- */

function learnerGetState(): AgentTool {
  return {
    definition: {
      name: "learner.get_state",
      category: "read",
      description: "Read the learner's goals, mastery, misconceptions, and preferences.",
      inputSchema: obj({ accountId: s.str }, []),
      outputSchema: obj(
        {
          goals: {
            type: "array",
            items: obj({ id: s.str, description: s.str, status: s.str, targetConceptIds: s.strArr }, [
              "id",
              "description",
              "status",
              "targetConceptIds"
            ])
          },
          mastery: {
            type: "array",
            items: obj({ conceptId: s.str, mastery: s.ratio, confidence: s.ratio }, [
              "conceptId",
              "mastery",
              "confidence"
            ])
          },
          openMisconceptions: {
            type: "array",
            items: obj({ id: s.str, conceptId: s.str, description: s.str }, ["id", "conceptId", "description"])
          },
          dueReviewCount: s.int,
          preferences: obj(
            { explanationDepth: s.str, preferredModality: s.str, accommodations: s.strArr },
            ["explanationDepth", "preferredModality", "accommodations"]
          )
        },
        ["goals", "mastery", "openMisconceptions", "dueReviewCount"]
      )
    },
    async execute(input: { accountId?: string }, ctx: ToolContext) {
      const accountId = input.accountId ?? ctx.principal.accountId;
      assertAccountAccess(ctx.principal, accountId);
      const goals = await ctx.memory.getActiveGoals(accountId);
      const mastery = await ctx.memory.listMastery(accountId);
      const misconceptions = await ctx.memory.getOpenMisconceptions(accountId);
      const due = await ctx.memory.getDueReviews(accountId, ctx.clock());
      const prefs = await ctx.memory.getPreferences(accountId);
      return {
        goals: goals.map((g) => ({
          id: g.id,
          description: g.description,
          status: g.status,
          targetConceptIds: g.targetConceptIds
        })),
        mastery: mastery.map((m) => ({ conceptId: m.conceptId, mastery: m.mastery, confidence: m.confidence })),
        openMisconceptions: misconceptions.map((m) => ({
          id: m.id,
          conceptId: m.conceptId,
          description: m.description
        })),
        dueReviewCount: due.length,
        ...(prefs
          ? {
              preferences: {
                explanationDepth: prefs.explanationDepth,
                preferredModality: prefs.preferredModality,
                accommodations: prefs.accommodations
              }
            }
          : {})
      };
    }
  };
}

function learnerRecordStage(): AgentTool {
  return {
    definition: {
      name: "learner.record_stage",
      category: "state_change",
      description: "Record completion of a modality stage for a lesson.",
      idempotent: true,
      inputSchema: obj(
        { lessonId: s.str, stage: { type: "string", enum: ["read", "listen", "write", "code", "handwrite"] } },
        ["lessonId", "stage"]
      ),
      outputSchema: obj({ recorded: s.bool, completedStages: s.strArr, lessonComplete: s.bool }, [
        "recorded",
        "completedStages",
        "lessonComplete"
      ])
    },
    async execute(input: { lessonId: string; stage: ModalityStage }, ctx: ToolContext) {
      const accountId = ctx.principal.accountId;
      await ctx.memory.recordStage({
        accountId,
        lessonId: input.lessonId,
        stage: input.stage,
        completedAt: ctx.clock().toISOString()
      });
      const completed = await ctx.memory.getCompletedStages(accountId, input.lessonId);
      const lesson = ctx.fixture.getLesson(input.lessonId);
      const isProgramming = lesson?.isProgrammingSubject ?? false;
      return {
        recorded: true,
        completedStages: getStageOrder(isProgramming).filter((st) => completed.includes(st)),
        lessonComplete: isLessonComplete(new Set(completed), isProgramming)
      };
    }
  };
}

function learnerRecordGoal(): AgentTool {
  return {
    definition: {
      name: "learner.record_goal",
      category: "state_change",
      description: "Record or update a durable learning goal.",
      idempotent: true,
      inputSchema: obj({ description: s.str, targetConceptIds: s.strArr }, ["description"]),
      outputSchema: obj(
        {
          goal: obj({ id: s.str, description: s.str, status: s.str, targetConceptIds: s.strArr }, [
            "id",
            "description",
            "status",
            "targetConceptIds"
          ])
        },
        ["goal"]
      )
    },
    async execute(input: { description: string; targetConceptIds?: string[] }, ctx: ToolContext) {
      const now = ctx.clock().toISOString();
      const goal: Goal = {
        id: ctx.idFactory("goal"),
        accountId: ctx.principal.accountId,
        description: input.description,
        targetConceptIds: input.targetConceptIds ?? [],
        status: "active",
        createdAt: now,
        updatedAt: now
      };
      await ctx.memory.upsertGoal(goal);
      return {
        goal: {
          id: goal.id,
          description: goal.description,
          status: goal.status,
          targetConceptIds: goal.targetConceptIds
        }
      };
    }
  };
}

/* ---------------------------- practice tools ---------------------------- */

function practiceGetNext(): AgentTool {
  return {
    definition: {
      name: "practice.get_next",
      category: "read",
      description: "Select the next practice problem for a lesson.",
      inputSchema: obj({ lessonId: s.str, excludeProblemIds: s.strArr }, ["lessonId"]),
      outputSchema: obj(
        {
          available: s.bool,
          problem: obj({ id: s.str, prompt: s.str, tier: s.str, conceptId: s.str }, [
            "id",
            "prompt",
            "tier",
            "conceptId"
          ])
        },
        ["available"]
      )
    },
    async execute(input: { lessonId: string; excludeProblemIds?: string[] }, ctx: ToolContext) {
      const problem = ctx.fixture.getNextProblem(input.lessonId, input.excludeProblemIds ?? []);
      if (!problem) {
        return { available: false };
      }
      return {
        available: true,
        problem: { id: problem.id, prompt: problem.prompt, tier: problem.tier, conceptId: problem.conceptId }
      };
    }
  };
}

function practiceSubmit(): AgentTool {
  return {
    definition: {
      name: "practice.submit",
      category: "state_change",
      description: "Submit an answer to a practice problem; records the attempt and any misconception.",
      inputSchema: obj({ problemId: s.str, answer: s.optStr }, ["problemId", "answer"]),
      outputSchema: obj(
        {
          attemptId: s.str,
          correct: s.bool,
          score: s.ratio,
          misconception: obj({ conceptId: s.str, description: s.str }, ["conceptId", "description"])
        },
        ["attemptId", "correct", "score"]
      )
    },
    async execute(input: { problemId: string; answer: string }, ctx: ToolContext) {
      const problem = ctx.fixture.getProblem(input.problemId);
      if (!problem) {
        throw new ToolError("not_found", `Problem ${input.problemId} not found`);
      }
      const evaluation = ctx.fixture.evaluate(input.problemId, input.answer);
      const attempt: Attempt = {
        id: ctx.idFactory("attempt"),
        accountId: ctx.principal.accountId,
        conceptId: problem.conceptId,
        lessonId: problem.lessonId,
        prompt: problem.prompt,
        response: input.answer,
        correct: evaluation.correct,
        score: evaluation.score,
        at: ctx.clock().toISOString()
      };
      await ctx.memory.recordAttempt(attempt);

      if (evaluation.misconception) {
        const now = ctx.clock().toISOString();
        const misconception: Misconception = {
          id: ctx.idFactory("misconception"),
          accountId: ctx.principal.accountId,
          conceptId: evaluation.misconception.conceptId,
          description: evaluation.misconception.description,
          evidenceAttemptIds: [attempt.id],
          status: "open",
          createdAt: now,
          updatedAt: now
        };
        await ctx.memory.upsertMisconception(misconception);
        return {
          attemptId: attempt.id,
          correct: evaluation.correct,
          score: evaluation.score,
          misconception: { conceptId: misconception.conceptId, description: misconception.description }
        };
      }

      return { attemptId: attempt.id, correct: evaluation.correct, score: evaluation.score };
    }
  };
}

/* --------------------------- assessment tool ---------------------------- */

function assessmentEvaluate(): AgentTool {
  return {
    definition: {
      name: "assessment.evaluate",
      category: "state_change",
      description: "Update concept mastery from a recorded attempt and resolve fixed misconceptions.",
      inputSchema: obj({ attemptId: s.str }, ["attemptId"]),
      outputSchema: obj(
        {
          conceptId: s.str,
          mastery: s.ratio,
          confidence: s.ratio,
          resolvedMisconceptionIds: s.strArr
        },
        ["conceptId", "mastery", "confidence", "resolvedMisconceptionIds"]
      )
    },
    async execute(input: { attemptId: string }, ctx: ToolContext) {
      const attempt = await ctx.memory.getAttempt(input.attemptId);
      if (!attempt) {
        throw new ToolError("not_found", `Attempt ${input.attemptId} not found`);
      }
      assertAccountAccess(ctx.principal, attempt.accountId);
      const prior = await ctx.memory.getMastery(attempt.accountId, attempt.conceptId);
      const priorMastery = prior?.mastery ?? 0.2;
      const priorConfidence = prior?.confidence ?? 0.2;
      const target = attempt.correct ? 1 : 0;
      const mastery = clamp01(priorMastery * 0.6 + target * 0.4);
      const confidence = clamp01(priorConfidence + 0.15);
      const record: ConceptMastery = {
        accountId: attempt.accountId,
        conceptId: attempt.conceptId,
        mastery,
        confidence,
        updatedAt: ctx.clock().toISOString()
      };
      await ctx.memory.setMastery(record);

      const resolvedMisconceptionIds: string[] = [];
      if (attempt.correct) {
        const open = await ctx.memory.getOpenMisconceptions(attempt.accountId);
        for (const m of open.filter((x) => x.conceptId === attempt.conceptId)) {
          await ctx.memory.upsertMisconception({ ...m, status: "resolved", updatedAt: ctx.clock().toISOString() });
          resolvedMisconceptionIds.push(m.id);
        }
      }
      return { conceptId: attempt.conceptId, mastery, confidence, resolvedMisconceptionIds };
    }
  };
}

/* ------------------------------ review tools ---------------------------- */

function reviewGetDue(): AgentTool {
  return {
    definition: {
      name: "review.get_due",
      category: "read",
      description: "List reviews due for the learner.",
      inputSchema: obj({ accountId: s.str }, []),
      outputSchema: obj(
        {
          due: {
            type: "array",
            items: obj(
              { conceptId: s.str, lessonId: s.str, dueAt: s.str, intervalDays: { type: "number" }, lastScore: { type: "number" } },
              ["conceptId", "dueAt", "intervalDays", "lastScore"]
            )
          }
        },
        ["due"]
      )
    },
    async execute(input: { accountId?: string }, ctx: ToolContext) {
      const accountId = input.accountId ?? ctx.principal.accountId;
      assertAccountAccess(ctx.principal, accountId);
      const due = await ctx.memory.getDueReviews(accountId, ctx.clock());
      return {
        due: due.map((r) => ({
          conceptId: r.conceptId,
          ...(r.lessonId ? { lessonId: r.lessonId } : {}),
          dueAt: r.dueAt,
          intervalDays: r.intervalDays,
          lastScore: r.lastScore
        }))
      };
    }
  };
}

function reviewSchedule(): AgentTool {
  return {
    definition: {
      name: "review.schedule",
      category: "state_change",
      description: "Schedule the next spaced review for a concept based on a score (0..1).",
      idempotent: true,
      inputSchema: obj({ conceptId: s.str, lessonId: s.str, score: s.ratio }, ["conceptId", "score"]),
      outputSchema: obj(
        { conceptId: s.str, dueAt: s.str, intervalDays: { type: "number" }, lastScore: { type: "number" } },
        ["conceptId", "dueAt", "intervalDays", "lastScore"]
      )
    },
    async execute(input: { conceptId: string; lessonId?: string; score: number }, ctx: ToolContext) {
      const accountId = ctx.principal.accountId;
      const now = ctx.clock();
      const existing = await ctx.memory.getDueReviews(accountId, new Date(8640000000000000));
      const prior = existing.find((r) => r.conceptId === input.conceptId);
      const { nextReviewDate, intervalDays } = computeNextReview({
        score: Math.round(input.score * 100),
        ...(prior?.lastReviewedAt ? { lastReviewedAt: new Date(prior.lastReviewedAt) } : {}),
        now
      });
      const record: ReviewRecord = {
        accountId,
        conceptId: input.conceptId,
        ...(input.lessonId ? { lessonId: input.lessonId } : {}),
        dueAt: nextReviewDate.toISOString(),
        intervalDays,
        lastScore: input.score,
        lastReviewedAt: now.toISOString(),
        history: [...(prior?.history ?? []), { at: now.toISOString(), score: input.score }]
      };
      await ctx.memory.upsertReview(record);
      return { conceptId: record.conceptId, dueAt: record.dueAt, intervalDays, lastScore: input.score };
    }
  };
}

/* ------------------------------ tutor tools ----------------------------- */

function groundedCitations(ctx: ToolContext, query: string, lessonId?: string) {
  const hits = ctx.fixture.search(query, lessonId).slice(0, 3);
  return hits.map((h) => ({ lessonId: h.lessonId, passageId: h.passageId, text: h.text }));
}

function tutorExplain(): AgentTool {
  return {
    definition: {
      name: "tutor.explain",
      category: "read",
      description: "Produce a grounded explanation citing lesson passages.",
      inputSchema: obj({ lessonId: s.str, question: s.optStr }, ["lessonId"]),
      outputSchema: obj(
        {
          content: s.str,
          citations: {
            type: "array",
            items: obj({ lessonId: s.str, passageId: s.str }, ["lessonId", "passageId"])
          },
          grounded: s.bool
        },
        ["content", "citations", "grounded"]
      )
    },
    async execute(input: { lessonId: string; question?: string }, ctx: ToolContext) {
      const lesson = ctx.fixture.getLesson(input.lessonId);
      if (!lesson) {
        throw new ToolError("not_found", `Lesson ${input.lessonId} not found`);
      }
      const cites = groundedCitations(ctx, input.question ?? lesson.title, input.lessonId);
      if (cites.length === 0) {
        return {
          content: "The available lessons do not cover that yet.",
          citations: [],
          grounded: false
        };
      }
      const content = `${lesson.title}: ${cites.map((c) => c.text).join(" ")}`;
      return {
        content,
        citations: cites.map((c) => ({ lessonId: c.lessonId, passageId: c.passageId })),
        grounded: true
      };
    }
  };
}

function tutorHint(): AgentTool {
  return {
    definition: {
      name: "tutor.hint",
      category: "read",
      description: "Give a hint for a practice problem without revealing the answer.",
      inputSchema: obj({ problemId: s.str }, ["problemId"]),
      outputSchema: obj({ hint: s.str }, ["hint"])
    },
    async execute(input: { problemId: string }, ctx: ToolContext) {
      const problem = ctx.fixture.getProblem(input.problemId);
      if (!problem) {
        throw new ToolError("not_found", `Problem ${input.problemId} not found`);
      }
      const concept = ctx.fixture.getConcept(problem.conceptId);
      return { hint: `Recall: ${concept?.summary ?? "the key definition"} Focus on what the definition requires.` };
    }
  };
}

function tutorAskSocratic(): AgentTool {
  return {
    definition: {
      name: "tutor.ask_socratic",
      category: "read",
      description: "Pose a Socratic question about a concept.",
      inputSchema: obj({ conceptId: s.str }, ["conceptId"]),
      outputSchema: obj({ question: s.str }, ["question"])
    },
    async execute(input: { conceptId: string }, ctx: ToolContext) {
      const concept = ctx.fixture.getConcept(input.conceptId);
      const name = concept?.name ?? input.conceptId;
      return { question: `In your own words, what must be true for ${name} to hold, and why?` };
    }
  };
}

/* --------------------------- study plan tools --------------------------- */

interface StudyPlanStep {
  lessonId: string;
  order: number;
  done: boolean;
}

function studyPlanCreate(artifacts: ArtifactService): AgentTool {
  return {
    definition: {
      name: "study_plan.create",
      category: "state_change",
      description: "Create a study plan artifact from an ordered list of lessons.",
      inputSchema: obj({ title: s.str, lessonIds: s.strArr }, ["title", "lessonIds"]),
      outputSchema: obj(
        {
          artifactId: s.str,
          steps: { type: "array", items: obj({ lessonId: s.str, order: s.int, done: s.bool }, ["lessonId", "order", "done"]) }
        },
        ["artifactId", "steps"]
      )
    },
    async execute(input: { title: string; lessonIds: string[] }, ctx: ToolContext) {
      const steps: StudyPlanStep[] = input.lessonIds.map((lessonId, order) => ({ lessonId, order, done: false }));
      const artifact = await artifacts.create({
        kind: "study_plan",
        title: input.title,
        altText: `Study plan: ${input.title}`,
        description: "Ordered study plan",
        source: JSON.stringify({ steps }),
        lessonIds: input.lessonIds,
        conceptIds: [],
        createdBy: isEducator(ctx.principal) ? "educator" : "learner"
      });
      return { artifactId: artifact.id, steps };
    }
  };
}

function studyPlanAdvance(artifacts: ArtifactService): AgentTool {
  return {
    definition: {
      name: "study_plan.advance",
      category: "state_change",
      description: "Mark a lesson complete in a study plan and return the next lesson.",
      inputSchema: obj({ artifactId: s.str, completedLessonId: s.str }, ["artifactId", "completedLessonId"]),
      outputSchema: obj({ nextLessonId: s.str, remaining: s.int, done: s.bool }, ["remaining", "done"])
    },
    async execute(input: { artifactId: string; completedLessonId: string }, ctx: ToolContext) {
      const artifact = await ctx.memory.getArtifact(input.artifactId);
      if (!artifact) {
        throw new ToolError("not_found", `Study plan ${input.artifactId} not found`);
      }
      const parsed = JSON.parse(artifact.source) as { steps: StudyPlanStep[] };
      const steps = parsed.steps.map((step) =>
        step.lessonId === input.completedLessonId ? { ...step, done: true } : step
      );
      await artifacts.revise({
        artifactId: input.artifactId,
        source: JSON.stringify({ steps }),
        revisedBy: isEducator(ctx.principal) ? "educator" : "learner"
      });
      const next = steps.find((step) => !step.done);
      const remaining = steps.filter((step) => !step.done).length;
      return {
        ...(next ? { nextLessonId: next.lessonId } : {}),
        remaining,
        done: remaining === 0
      };
    }
  };
}

/* ----------------------------- visual tools ----------------------------- */

function visualCreate(artifacts: ArtifactService): AgentTool {
  return {
    definition: {
      name: "visual.create",
      category: "state_change",
      description: "Create and sanitize a visual artifact (SVG or Mermaid).",
      inputSchema: obj(
        {
          kind: { type: "string", enum: ["svg", "mermaid", "plot", "interactive"] },
          title: s.str,
          altText: s.str,
          description: s.optStr,
          source: s.str,
          lessonIds: s.strArr,
          conceptIds: s.strArr
        },
        ["kind", "title", "altText", "source"]
      ),
      outputSchema: artifactSchema
    },
    async execute(
      input: {
        kind: Artifact["kind"];
        title: string;
        altText: string;
        description?: string;
        source: string;
        lessonIds?: string[];
        conceptIds?: string[];
      },
      ctx: ToolContext
    ) {
      try {
        return await artifacts.create({
          kind: input.kind,
          title: input.title,
          altText: input.altText,
          ...(input.description !== undefined ? { description: input.description } : {}),
          source: input.source,
          lessonIds: input.lessonIds ?? [],
          conceptIds: input.conceptIds ?? [],
          createdBy: "agent"
        });
      } catch (err) {
        const violations = (err as { violations?: string[] }).violations;
        throw new ToolError("artifact_unsafe", (err as Error).message, false, violations ? { violations } : undefined);
      }
    }
  };
}

function visualRevise(artifacts: ArtifactService): AgentTool {
  return {
    definition: {
      name: "visual.revise",
      category: "state_change",
      description: "Revise a visual artifact, producing a new sanitized version.",
      inputSchema: obj(
        { artifactId: s.str, source: s.optStr, title: s.optStr, altText: s.optStr, description: s.optStr },
        ["artifactId"]
      ),
      outputSchema: artifactSchema
    },
    async execute(
      input: { artifactId: string; source?: string; title?: string; altText?: string; description?: string },
      _ctx: ToolContext
    ) {
      try {
        return await artifacts.revise({
          artifactId: input.artifactId,
          ...(input.source !== undefined ? { source: input.source } : {}),
          ...(input.title !== undefined ? { title: input.title } : {}),
          ...(input.altText !== undefined ? { altText: input.altText } : {}),
          ...(input.description !== undefined ? { description: input.description } : {}),
          revisedBy: "agent"
        });
      } catch (err) {
        const violations = (err as { violations?: string[] }).violations;
        throw new ToolError("artifact_unsafe", (err as Error).message, false, violations ? { violations } : undefined);
      }
    }
  };
}

function visualPresent(artifacts: ArtifactService): AgentTool {
  return {
    definition: {
      name: "visual.present",
      category: "read",
      description: "Return the sanitized artifact and export metadata for presentation.",
      inputSchema: obj({ artifactId: s.str }, ["artifactId"]),
      outputSchema: artifactSchema
    },
    async execute(input: { artifactId: string }, _ctx: ToolContext) {
      return artifacts.present(input.artifactId);
    }
  };
}

function artifactSave(): AgentTool {
  return {
    definition: {
      name: "artifact.save",
      category: "state_change",
      description: "Persist an artifact to the learner's saved items.",
      idempotent: true,
      inputSchema: obj({ artifactId: s.str }, ["artifactId"]),
      outputSchema: obj({ saved: s.bool, artifactId: s.str }, ["saved", "artifactId"])
    },
    async execute(input: { artifactId: string }, ctx: ToolContext) {
      const artifact = await ctx.memory.getArtifact(input.artifactId);
      if (!artifact) {
        throw new ToolError("not_found", `Artifact ${input.artifactId} not found`);
      }
      await ctx.memory.saveArtifact(artifact);
      return { saved: true, artifactId: artifact.id };
    }
  };
}

/* ----------------------------- educator tool --------------------------- */

/**
 * Publish semantics are deliberately honest. The core guardrail is preserved:
 * model/agent code never writes to the public corpus. Approval alone does NOT
 * make an artifact public.
 *
 *  - No configured sink → status `approved_for_reviewed_commit`, published:false.
 *    A human performs the normal reviewed commit / static build to publish.
 *  - Configured outbox → the sanitized artifact + provenance/approval/version is
 *    written atomically to an internal reviewed-draft outbox and the status is
 *    `queuedForPublish`, published:false. A later reviewed commit / static build
 *    consumes the outbox. It is still not public.
 */
function educatorPublishArtifact(approvals: ApprovalService, outbox?: PublicationOutbox): AgentTool {
  return {
    definition: {
      name: "educator.publish_artifact",
      category: "educator",
      description:
        "Mark an educator-approved artifact version as ready for the reviewed publication pipeline. " +
        "Does not publish to the public corpus directly; a reviewed commit/static build performs that.",
      requiredRole: "educator",
      inputSchema: obj({ artifactId: s.str, version: { type: "number", integer: true, min: 1 } }, [
        "artifactId",
        "version"
      ]),
      outputSchema: obj(
        {
          published: s.bool,
          status: {
            type: "string",
            enum: ["approved_for_reviewed_commit", "queuedForPublish"]
          } as SchemaNode,
          artifactId: s.str,
          version: s.int,
          outbox: {
            type: "object",
            properties: { packageId: s.str, relativePath: s.str },
            required: ["packageId", "relativePath"]
          } as SchemaNode,
          detail: s.optStr
        },
        ["published", "status", "artifactId", "version"]
      )
    },
    async execute(input: { artifactId: string; version: number }, ctx: ToolContext) {
      // Enforces educator role AND an approved publish request for this exact
      // version. Throws (not_approved) otherwise.
      await approvals.publish(ctx.principal, input.artifactId, input.version);

      if (!outbox) {
        return {
          published: false,
          status: "approved_for_reviewed_commit",
          artifactId: input.artifactId,
          version: input.version,
          detail:
            "Approved for the reviewed publication pipeline. A normal reviewed commit / static build must publish it; it is not yet public."
        };
      }

      const artifact = await ctx.memory.getArtifact(input.artifactId);
      if (!artifact) {
        throw new ToolError("not_found", `Artifact ${input.artifactId} not found`);
      }
      if (artifact.version !== input.version) {
        throw new ToolError(
          "invalid_input",
          `Approved version ${input.version} does not match current artifact version ${artifact.version}.`
        );
      }
      const approval = await approvals.getApprovedPublish(input.artifactId, input.version);
      if (!approval) {
        // Should be unreachable after approvals.publish, but fail loud not silent.
        throw new ToolError("not_approved", "No approved publish request found for this version.");
      }

      try {
        const result = await outbox.writeReviewedDraft({
          artifact,
          approval,
          now: ctx.clock().toISOString()
        });
        return {
          published: false,
          status: "queuedForPublish",
          artifactId: input.artifactId,
          version: input.version,
          outbox: { packageId: result.packageId, relativePath: result.relativePath },
          detail:
            "An immutable reviewed draft package was written to the internal publication outbox. It becomes public only after a reviewed commit / static build consumes it."
        };
      } catch (err) {
        const code = (err as PublicationOutboxError).code;
        if (code === "exists") {
          // The version was already queued; report truthfully and idempotently.
          return {
            published: false,
            status: "queuedForPublish",
            artifactId: input.artifactId,
            version: input.version,
            detail: "A reviewed draft package for this exact version was already queued in the outbox."
          };
        }
        throw new ToolError("publication_failed", (err as Error).message, false);
      }
    }
  };
}

/** All domain tools with their exact handoff names. */
export function createDomainTools(
  artifacts: ArtifactService,
  approvals?: ApprovalService,
  outbox?: PublicationOutbox
): AgentTool[] {
  const tools = [
    curriculumSearch(),
    curriculumGetLesson(),
    curriculumGetPrerequisites(),
    learnerGetState(),
    learnerRecordStage(),
    learnerRecordGoal(),
    practiceGetNext(),
    practiceSubmit(),
    assessmentEvaluate(),
    reviewGetDue(),
    reviewSchedule(),
    tutorExplain(),
    tutorHint(),
    tutorAskSocratic(),
    studyPlanCreate(artifacts),
    studyPlanAdvance(artifacts),
    visualCreate(artifacts),
    visualRevise(artifacts),
    visualPresent(artifacts),
    artifactSave()
  ];
  if (approvals) {
    tools.push(educatorPublishArtifact(approvals, outbox));
  }
  return tools;
}

export const DOMAIN_TOOL_NAMES = [
  "curriculum.search",
  "curriculum.get_lesson",
  "curriculum.get_prerequisites",
  "learner.get_state",
  "learner.record_stage",
  "learner.record_goal",
  "practice.get_next",
  "practice.submit",
  "assessment.evaluate",
  "review.get_due",
  "review.schedule",
  "tutor.explain",
  "tutor.hint",
  "tutor.ask_socratic",
  "study_plan.create",
  "study_plan.advance",
  "visual.create",
  "visual.revise",
  "visual.present",
  "artifact.save"
] as const;
