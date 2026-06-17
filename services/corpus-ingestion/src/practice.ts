import type { PracticeProblemTier } from "@learning-platform/corpus-types";

export interface AuthoredPracticeProblem {
  id: string;
  subjectId: string;
  lessonId?: string;
  tier: PracticeProblemTier;
  prompt: string;
  solution: string;
}

export function parsePracticeBankJson(json: string, subjectId: string): AuthoredPracticeProblem[] {
  const parsed = JSON.parse(json);
  if (!Array.isArray(parsed)) {
    throw new Error("Practice bank JSON must be an array");
  }

  return parsed.map((item: any, index: number) => {
    if (!item.id || typeof item.id !== "string") {
      throw new Error(`Problem at index ${index} is missing an id`);
    }
    if (!item.tier || typeof item.tier !== "string") {
      throw new Error(`Problem ${item.id} is missing a tier`);
    }
    if (!item.prompt || typeof item.prompt !== "string") {
      throw new Error(`Problem ${item.id} is missing a prompt`);
    }
    if (!item.solution || typeof item.solution !== "string") {
      throw new Error(`Problem ${item.id} is missing a solution`);
    }

    return {
      id: item.id,
      subjectId,
      lessonId: typeof item.lessonId === "string" ? item.lessonId : undefined,
      tier: item.tier as PracticeProblemTier,
      prompt: item.prompt,
      solution: item.solution
    };
  });
}
