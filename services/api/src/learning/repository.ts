import type { Pool } from "pg";
import type { ModalityStage } from "./stages.js";

export interface ProgressRow {
  account_id: string;
  lesson_id: string;
  stage: ModalityStage;
  completed_at: Date;
}

export interface GraspScoreRow {
  id: string;
  account_id: string;
  lesson_id: string;
  score: number;
  flagged_for_review: boolean;
  created_at: Date;
}

export interface ReviewScheduleRow {
  account_id: string;
  lesson_id: string;
  next_review_date: Date;
  interval_days: number;
  last_score: number;
  updated_at: Date;
}

export interface PathEnrollmentRow {
  id: string;
  account_id: string;
  path_id: string;
  current_position: number;
  completed_count: number;
  created_at: Date;
  updated_at: Date;
}

export class LearningRepository {
  constructor(private readonly pool: Pool) {}

  async recordStageCompletion(
    accountId: string,
    lessonId: string,
    stage: ModalityStage
  ): Promise<void> {
    await this.pool.query(
      `
      INSERT INTO progress (account_id, lesson_id, stage)
      VALUES ($1, $2, $3)
      ON CONFLICT (account_id, lesson_id, stage) DO NOTHING
      `,
      [accountId, lessonId, stage]
    );
  }

  async getCompletedStages(accountId: string, lessonId: string): Promise<Set<ModalityStage>> {
    const result = await this.pool.query<{ stage: ModalityStage }>(
      `SELECT stage FROM progress WHERE account_id = $1 AND lesson_id = $2`,
      [accountId, lessonId]
    );
    return new Set(result.rows.map((r) => r.stage));
  }

  async getResumePoint(accountId: string): Promise<{ lessonId: string; stage: ModalityStage } | undefined> {
    const result = await this.pool.query<{ lesson_id: string; stage: ModalityStage }>(
      `
      SELECT lesson_id, stage
      FROM progress
      WHERE account_id = $1
      ORDER BY completed_at DESC
      LIMIT 1
      `,
      [accountId]
    );
    const row = result.rows[0];
    return row ? { lessonId: row.lesson_id, stage: row.stage } : undefined;
  }

  async getSubjectSummary(accountId: string, subjectId: string): Promise<{ completedCount: number; inProgressCount: number }> {
    // A lesson is complete if all applicable stages are done.
    // Wait, it might be simpler to compute this on the fly in the service layer if we pull progress per lesson, 
    // but SQL can also do it. Let's just pull all stages for lessons in this subject for this account.
    const result = await this.pool.query<{ lesson_id: string; stages: ModalityStage[] }>(
      `
      SELECT p.lesson_id, array_agg(p.stage) as stages
      FROM progress p
      JOIN lessons l ON l.id = p.lesson_id
      WHERE p.account_id = $1 AND l.subject_id = $2
      GROUP BY p.lesson_id
      `,
      [accountId, subjectId]
    );
    
    // We will evaluate completed/inProgress in the service layer because it needs to know if the subject is programming.
    return { completedCount: 0, inProgressCount: 0 }; // Service will compute
  }

  async getSubjectProgressRows(accountId: string, subjectId: string): Promise<Array<{ lesson_id: string; stages: ModalityStage[] }>> {
    const result = await this.pool.query<{ lesson_id: string; stages: ModalityStage[] }>(
      `
      SELECT p.lesson_id, array_agg(p.stage) as stages
      FROM progress p
      JOIN lessons l ON l.id = p.lesson_id
      WHERE p.account_id = $1 AND l.subject_id = $2
      GROUP BY p.lesson_id
      `,
      [accountId, subjectId]
    );
    return result.rows;
  }

  async recordGraspScore(
    accountId: string,
    lessonId: string,
    score: number,
    flaggedForReview: boolean
  ): Promise<void> {
    await this.pool.query(
      `
      INSERT INTO grasp_scores (account_id, lesson_id, score, flagged_for_review)
      VALUES ($1, $2, $3, $4)
      `,
      [accountId, lessonId, score, flaggedForReview]
    );
  }

  async getLatestReviewSchedule(accountId: string, lessonId: string): Promise<ReviewScheduleRow | undefined> {
    const result = await this.pool.query<ReviewScheduleRow>(
      `
      SELECT account_id, lesson_id, next_review_date, interval_days, last_score, updated_at
      FROM review_schedules
      WHERE account_id = $1 AND lesson_id = $2
      `,
      [accountId, lessonId]
    );
    return result.rows[0];
  }

  async upsertReviewSchedule(
    accountId: string,
    lessonId: string,
    nextReviewDate: Date,
    intervalDays: number,
    lastScore: number
  ): Promise<void> {
    await this.pool.query(
      `
      INSERT INTO review_schedules (account_id, lesson_id, next_review_date, interval_days, last_score)
      VALUES ($1, $2, $3, $4, $5)
      ON CONFLICT (account_id, lesson_id)
      DO UPDATE SET
        next_review_date = EXCLUDED.next_review_date,
        interval_days = EXCLUDED.interval_days,
        last_score = EXCLUDED.last_score,
        updated_at = now()
      `,
      [accountId, lessonId, nextReviewDate, intervalDays, lastScore]
    );
  }

  async getDueReviews(accountId: string, limit: number = 50): Promise<ReviewScheduleRow[]> {
    const result = await this.pool.query<ReviewScheduleRow>(
      `
      SELECT account_id, lesson_id, next_review_date, interval_days, last_score, updated_at
      FROM review_schedules
      WHERE account_id = $1 AND next_review_date <= now()
      ORDER BY next_review_date ASC
      LIMIT $2
      `,
      [accountId, limit]
    );
    return result.rows;
  }

  async enrollInPath(accountId: string, pathId: string): Promise<PathEnrollmentRow> {
    const result = await this.pool.query<PathEnrollmentRow>(
      `
      INSERT INTO path_enrollments (account_id, path_id, current_position, completed_count)
      VALUES ($1, $2, 0, 0)
      ON CONFLICT (account_id, path_id) DO UPDATE SET updated_at = now()
      RETURNING id, account_id, path_id, current_position, completed_count, created_at, updated_at
      `,
      [accountId, pathId]
    );
    return result.rows[0]!;
  }

  async getPathEnrollment(accountId: string, pathId: string): Promise<PathEnrollmentRow | undefined> {
    const result = await this.pool.query<PathEnrollmentRow>(
      `
      SELECT id, account_id, path_id, current_position, completed_count, created_at, updated_at
      FROM path_enrollments
      WHERE account_id = $1 AND path_id = $2
      `,
      [accountId, pathId]
    );
    return result.rows[0];
  }

  async updatePathEnrollment(
    accountId: string,
    pathId: string,
    currentPosition: number,
    completedCount: number
  ): Promise<void> {
    await this.pool.query(
      `
      UPDATE path_enrollments
      SET current_position = $1, completed_count = $2, updated_at = now()
      WHERE account_id = $3 AND path_id = $4
      `,
      [currentPosition, completedCount, accountId, pathId]
    );
  }

  async getPathItemCount(pathId: string): Promise<number> {
    const result = await this.pool.query<{ count: string }>(
      `SELECT count(*) FROM path_items WHERE path_id = $1`,
      [pathId]
    );
    return parseInt(result.rows[0]?.count ?? "0", 10);
  }

  async getLessonAtPosition(pathId: string, position: number): Promise<string | undefined> {
    const result = await this.pool.query<{ lesson_id: string }>(
      `
      SELECT lesson_id 
      FROM path_items 
      WHERE path_id = $1 AND position = $2 AND kind = 'lesson'
      `,
      [pathId, position]
    );
    return result.rows[0]?.lesson_id;
  }
}
