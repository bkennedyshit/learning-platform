export type PracticeProblemTier = "easy" | "medium" | "hard" | "exam";

export interface PracticeProblem {
  id?: string;
  subjectId: string;
  lessonId?: string;
  tier: PracticeProblemTier;
  prompt: string;
  solution: string;
  source: "authored" | "generated";
}

export interface PracticeProblemRequest {
  subjectId: string;
  subjectSlug: string;
  tier: PracticeProblemTier;
  lessonId?: string;
  generatorSupported: boolean;
  excludeProblemIds?: readonly string[];
}

export interface PracticeProblemRepository {
  findAuthoredProblem(request: PracticeProblemRequest): Promise<PracticeProblem | undefined>;
  findGeneratedProblem(request: PracticeProblemRequest): Promise<PracticeProblem | undefined>;
  saveGeneratedProblem(problem: PracticeProblem): Promise<PracticeProblem>;
}

export interface ProblemGeneratorClient {
  generate(request: {
    subject: string;
    tier: PracticeProblemTier;
  }): Promise<{
    problem: string;
    solution: string;
  }>;
}
