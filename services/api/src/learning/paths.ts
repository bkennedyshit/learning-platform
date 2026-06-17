export interface PathProgress {
  currentPosition: number;
  completedCount: number;
  totalItems: number;
}

export interface PathAdvanceResult extends PathProgress {
  completionRatio: number;
}

export function advancePathOnLessonCompletion(progress: PathProgress): PathAdvanceResult {
  const completedCount = Math.min(progress.totalItems, progress.completedCount + 1);
  const currentPosition = Math.min(progress.totalItems, progress.currentPosition + 1);

  if (currentPosition < progress.currentPosition) {
    throw new Error("Path position cannot move backwards.");
  }

  return {
    currentPosition,
    completedCount,
    totalItems: progress.totalItems,
    completionRatio: computePathCompletion(completedCount, progress.totalItems)
  };
}

export function computePathCompletion(completedCount: number, totalItems: number): number {
  if (totalItems <= 0) {
    return 0;
  }

  return Math.min(1, Math.max(0, completedCount / totalItems));
}
