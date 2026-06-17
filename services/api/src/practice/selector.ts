import type {
  PracticeProblem,
  PracticeProblemRepository,
  PracticeProblemRequest,
  ProblemGeneratorClient
} from "./types.js";

export class PracticeProblemUnavailableError extends Error {
  constructor(message = "No practice problem is available for this subject and tier.") {
    super(message);
    this.name = "PracticeProblemUnavailableError";
  }
}

export function createPracticeProblemSelector(
  repository: PracticeProblemRepository,
  generator: ProblemGeneratorClient
) {
  return {
    async select(request: PracticeProblemRequest): Promise<PracticeProblem> {
      const authored = await repository.findAuthoredProblem(request);
      if (authored) {
        return authored;
      }

      const cached = await repository.findGeneratedProblem(request);
      if (cached) {
        return cached;
      }

      if (!request.generatorSupported) {
        throw new PracticeProblemUnavailableError();
      }

      const generated = await generator.generate({
        subject: request.subjectSlug,
        tier: request.tier
      });

      return repository.saveGeneratedProblem({
        subjectId: request.subjectId,
        ...(request.lessonId ? { lessonId: request.lessonId } : {}),
        tier: request.tier,
        prompt: generated.problem,
        solution: generated.solution,
        source: "generated"
      });
    }
  };
}
