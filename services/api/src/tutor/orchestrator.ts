import type { LLMProviderAdapter } from "@learning-platform/llm-adapter";
import { getNextStage, type ModalityStage } from "../learning/index.js";
import type { RagRetrievalService } from "../rag/index.js";
import type { LessonStartGuidance, TutorAnswer, TutorQuestionRequest } from "./types.js";

const outsideMaterialMessage =
  "I do not have that in the available lessons yet. Try asking about the current lesson material.";

export interface TutorOrchestrator {
  answerQuestion(request: TutorQuestionRequest): Promise<TutorAnswer>;
  startLesson(lessonId: string, isProgrammingSubject: boolean): LessonStartGuidance;
  advanceStage(currentStage: ModalityStage, isProgrammingSubject: boolean): LessonStartGuidance;
}

export function createTutorOrchestrator(
  retrieval: RagRetrievalService,
  adapter: LLMProviderAdapter
): TutorOrchestrator {
  return {
    async answerQuestion(request) {
      const retrieved = await retrieval.retrieve({
        query: request.question,
        lessonId: request.lessonId
      });

      if (retrieved.passages.length === 0) {
        return {
          content: outsideMaterialMessage,
          sourceLessonIds: [],
          grounded: false
        };
      }

      const completion = await adapter.complete({
        messages: [
          {
            role: "system",
            content:
              "Answer only from the provided lesson passages. Use plain language. If the passages do not answer the question, say the available lessons do not cover it."
          },
          {
            role: "user",
            content: buildGroundedQuestion(request.question, retrieved.passages)
          }
        ],
        temperature: 0.1
      });

      return {
        content: completion.content,
        sourceLessonIds: retrieved.lessonRefs,
        grounded: true
      };
    },

    startLesson(lessonId, isProgrammingSubject) {
      return {
        lessonId,
        currentStage: "read",
        nextStage: getNextStage("read", isProgrammingSubject),
        message: "Start by reading the lesson. When you are done, move to listening."
      };
    },

    advanceStage(currentStage, isProgrammingSubject) {
      const nextStage = getNextStage(currentStage, isProgrammingSubject);
      return {
        lessonId: "",
        currentStage: nextStage ?? currentStage,
        nextStage: nextStage ? getNextStage(nextStage, isProgrammingSubject) : undefined,
        message: nextStage ? stageMessage(nextStage) : "You finished this lesson loop."
      };
    }
  };
}

function buildGroundedQuestion(
  question: string,
  passages: Array<{ lessonId: string; text: string }>
): string {
  const passageText = passages
    .map((passage, index) => `Passage ${index + 1} from lesson ${passage.lessonId}:\n${passage.text}`)
    .join("\n\n");

  return `${passageText}\n\nQuestion:\n${question}`;
}

function stageMessage(stage: ModalityStage): string {
  switch (stage) {
    case "listen":
      return "Now listen to the lesson audio and follow along.";
    case "write":
      return "Now answer a practice question in your own words.";
    case "code":
      return "Now try the coding step for this lesson.";
    case "handwrite":
      return "Now handwrite a short breakdown of what you learned.";
    case "read":
      return "Start by reading the lesson.";
  }
}
