export interface GraspAssessment {
  score: number;
  flaggedForReview: boolean;
}

export function normalizeGraspScore(rawScore: number): GraspAssessment {
  const clamped = Math.min(100, Math.max(0, Math.round(rawScore)));
  const score = Math.max(25, clamped);

  return {
    score,
    flaggedForReview: score < 70
  };
}
