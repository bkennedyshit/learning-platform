export interface ReviewScheduleInput {
  score: number;
  lastReviewedAt?: Date;
  now?: Date;
}

export interface ReviewScheduleResult {
  nextReviewDate: Date;
  intervalDays: number;
}

export function computeNextReview(input: ReviewScheduleInput): ReviewScheduleResult {
  const now = input.now ?? new Date();
  const daysSinceLastReview = input.lastReviewedAt
    ? Math.max(0, daysBetween(input.lastReviewedAt, now))
    : 0;

  const intervalDays = computeIntervalDays(input.score, daysSinceLastReview);
  const nextReviewDate = new Date(now);
  nextReviewDate.setUTCDate(nextReviewDate.getUTCDate() + intervalDays);

  return { nextReviewDate, intervalDays };
}

function computeIntervalDays(score: number, daysSinceLastReview: number): number {
  if (score < 70) {
    return 1;
  }

  if (score < 85) {
    return Math.max(2, Math.ceil(daysSinceLastReview * 1.5));
  }

  return Math.max(4, Math.ceil(daysSinceLastReview * 2.2));
}

function daysBetween(start: Date, end: Date): number {
  const millisecondsPerDay = 24 * 60 * 60 * 1000;
  return Math.floor((end.getTime() - start.getTime()) / millisecondsPerDay);
}
