import type { ModalityStage } from "../learning/index.js";

export interface TutorQuestionRequest {
  question: string;
  lessonId?: string;
}

export interface TutorAnswer {
  content: string;
  sourceLessonIds: string[];
  grounded: boolean;
}

export interface LessonStartGuidance {
  lessonId: string;
  currentStage: ModalityStage;
  nextStage?: ModalityStage;
  message: string;
}
