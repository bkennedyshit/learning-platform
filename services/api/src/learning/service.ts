import type { LLMProviderAdapter } from "@learning-platform/llm-adapter";
import type { LearningRepository, ReviewScheduleRow } from "./repository.js";
import { normalizeGraspScore } from "./grasp.js";
import { computeNextReview } from "./reviews.js";
import { advancePathOnLessonCompletion } from "./paths.js";
import { isLessonComplete, type ModalityStage } from "./stages.js";

export interface SubjectSummary {
  completedCount: number;
  inProgressCount: number;
}

export interface PathEnrollmentDetails {
  currentPosition: number;
  completedCount: number;
  totalItems: number;
  completionRatio: number;
  nextLessonId?: string;
}

export class LearningService {
  constructor(
    private readonly repo: LearningRepository,
    private readonly llmAdapter: LLMProviderAdapter
  ) {}

  // 8.1 Progress Tracker
  async recordStageCompletion(
    accountId: string,
    lessonId: string,
    stage: ModalityStage,
    isProgrammingSubject: boolean,
    pathId?: string
  ): Promise<void> {
    await this.repo.recordStageCompletion(accountId, lessonId, stage);

    // Check if lesson is now complete
    const completedStages = await this.repo.getCompletedStages(accountId, lessonId);
    if (isLessonComplete(completedStages, isProgrammingSubject)) {
      if (pathId) {
        // Advance path position if enrolled and this is the active path lesson.
        const enrollment = await this.repo.getPathEnrollment(accountId, pathId);
        if (enrollment) {
          const expectedLessonId = await this.repo.getLessonAtPosition(pathId, enrollment.current_position);
          if (expectedLessonId === lessonId) {
            const totalItems = await this.repo.getPathItemCount(pathId);
            const advanceResult = advancePathOnLessonCompletion({
              currentPosition: enrollment.current_position,
              completedCount: enrollment.completed_count,
              totalItems
            });
            await this.repo.updatePathEnrollment(
              accountId,
              pathId,
              advanceResult.currentPosition,
              advanceResult.completedCount
            );
          }
        }
      }
    }
  }

  async getResumePoint(accountId: string) {
    return await this.repo.getResumePoint(accountId);
  }

  async getSubjectSummary(accountId: string, subjectId: string, isProgrammingSubject: boolean): Promise<SubjectSummary> {
    const rows = await this.repo.getSubjectProgressRows(accountId, subjectId);
    let completedCount = 0;
    let inProgressCount = 0;

    for (const row of rows) {
      if (isLessonComplete(new Set(row.stages), isProgrammingSubject)) {
        completedCount++;
      } else {
        inProgressCount++;
      }
    }

    return { completedCount, inProgressCount };
  }

  // 8.2 Grasp Assessor & 8.3 Spaced Repetition Scheduler
  async assessGrasp(
    accountId: string,
    lessonId: string,
    response: string,
    expectedAnswer: string
  ): Promise<{ score: number; flaggedForReview: boolean }> {
    // evaluate Write/Code responses against corpus-derived expected answers
    const completion = await this.llmAdapter.complete({
      messages: [
        {
          role: "system",
          content: "You are an automated grader. Evaluate the learner's response against the expected answer. Output only a number between 0 and 100 representing their grasp of the concept."
        },
        {
          role: "user",
          content: `Expected Answer: ${expectedAnswer}\n\nLearner Response: ${response}`
        }
      ],
      temperature: 0.1
    });

    const rawScore = parseInt(completion.content.trim(), 10) || 0;
    const assessment = normalizeGraspScore(rawScore);

    await this.repo.recordGraspScore(accountId, lessonId, assessment.score, assessment.flaggedForReview);

    // 8.3 Spaced Repetition Scheduler
    const lastSchedule = await this.repo.getLatestReviewSchedule(accountId, lessonId);
    const lastReviewedAt = lastSchedule ? lastSchedule.updated_at : undefined;
    
    const reviewResult = computeNextReview({
      score: assessment.score,
      lastReviewedAt
    });

    await this.repo.upsertReviewSchedule(
      accountId,
      lessonId,
      reviewResult.nextReviewDate,
      reviewResult.intervalDays,
      assessment.score
    );

    return assessment;
  }

  // 8.3 Expose the due queue earliest-first
  async getDueReviews(accountId: string): Promise<ReviewScheduleRow[]> {
    return await this.repo.getDueReviews(accountId);
  }

  // 8.4 Path Enrollment service
  async enrollInPath(accountId: string, pathId: string): Promise<PathEnrollmentDetails> {
    const enrollment = await this.repo.enrollInPath(accountId, pathId);
    const totalItems = await this.repo.getPathItemCount(pathId);
    const nextLessonId = await this.repo.getLessonAtPosition(pathId, enrollment.current_position);

    return {
      currentPosition: enrollment.current_position,
      completedCount: enrollment.completed_count,
      totalItems,
      completionRatio: totalItems > 0 ? enrollment.completed_count / totalItems : 0,
      nextLessonId
    };
  }

  async getPathEnrollment(accountId: string, pathId: string): Promise<PathEnrollmentDetails | undefined> {
    const enrollment = await this.repo.getPathEnrollment(accountId, pathId);
    if (!enrollment) {
      return undefined;
    }
    const totalItems = await this.repo.getPathItemCount(pathId);
    const nextLessonId = await this.repo.getLessonAtPosition(pathId, enrollment.current_position);

    return {
      currentPosition: enrollment.current_position,
      completedCount: enrollment.completed_count,
      totalItems,
      completionRatio: totalItems > 0 ? enrollment.completed_count / totalItems : 0,
      nextLessonId
    };
  }
}
