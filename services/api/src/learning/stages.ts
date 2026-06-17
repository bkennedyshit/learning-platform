export type ModalityStage = "read" | "listen" | "write" | "code" | "handwrite";

export const programmingStageOrder: readonly ModalityStage[] = [
  "read",
  "listen",
  "write",
  "code",
  "handwrite"
];

export const nonProgrammingStageOrder: readonly ModalityStage[] = [
  "read",
  "listen",
  "write",
  "handwrite"
];

export function getStageOrder(isProgrammingSubject: boolean): readonly ModalityStage[] {
  return isProgrammingSubject ? programmingStageOrder : nonProgrammingStageOrder;
}

export function getNextStage(
  currentStage: ModalityStage,
  isProgrammingSubject: boolean
): ModalityStage | undefined {
  const order = getStageOrder(isProgrammingSubject);
  const index = order.indexOf(currentStage);

  if (index === -1) {
    throw new Error(`Unknown stage: ${currentStage}`);
  }

  return order[index + 1];
}

export function isLessonComplete(
  completedStages: ReadonlySet<ModalityStage>,
  isProgrammingSubject: boolean
): boolean {
  return getStageOrder(isProgrammingSubject).every((stage) => completedStages.has(stage));
}
