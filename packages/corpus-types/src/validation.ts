import type { PathItem } from "./index.js";

export function assertPathItemsAreContiguous(items: readonly PathItem[]): void {
  const sorted = [...items].sort((a, b) => a.position - b.position);

  for (let index = 0; index < sorted.length; index += 1) {
    const item = sorted[index];
    if (!item || item.position !== index) {
      throw new Error(`Learning path positions must be contiguous from 0. Missing position ${index}.`);
    }
  }
}

export function assertPathItemReferencesExactlyOneTarget(item: PathItem): void {
  const targetCount = Number(Boolean(item.subjectId)) + Number(Boolean(item.lessonId));

  if (targetCount !== 1) {
    throw new Error("A path item must reference exactly one subject or lesson.");
  }

  if (item.kind === "subject" && !item.subjectId) {
    throw new Error("A subject path item must include subjectId.");
  }

  if (item.kind === "lesson" && !item.lessonId) {
    throw new Error("A lesson path item must include lessonId.");
  }
}
