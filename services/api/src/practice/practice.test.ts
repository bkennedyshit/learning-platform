import assert from "node:assert/strict";
import test from "node:test";
import type { QueryResultRow } from "pg";
import { createPostgresPracticeProblemRepository } from "./repository.js";
import { PracticeProblemUnavailableError, createPracticeProblemSelector } from "./selector.js";
import type { PracticeProblem, PracticeProblemRepository } from "./types.js";

const request = {
  subjectId: "11111111-1111-1111-1111-111111111111",
  subjectSlug: "algebra",
  tier: "easy" as const,
  generatorSupported: true
};

test("practice selector returns authored problem before generator fallback", async () => {
  let generatorCalled = false;
  const authored: PracticeProblem = {
    id: "authored-1",
    subjectId: request.subjectId,
    tier: "easy",
    prompt: "Solve x + 1 = 2",
    solution: "x = 1",
    source: "authored"
  };

  const selector = createPracticeProblemSelector(
    {
      async findAuthoredProblem() {
        return authored;
      },
      async findGeneratedProblem() {
        return undefined;
      },
      async saveGeneratedProblem(problem) {
        return problem;
      }
    },
    {
      async generate() {
        generatorCalled = true;
        return { problem: "generated", solution: "generated" };
      }
    }
  );

  assert.equal(await selector.select(request), authored);
  assert.equal(generatorCalled, false);
});

test("practice selector uses cached generated problem before calling sidecar", async () => {
  const cached: PracticeProblem = {
    id: "generated-1",
    subjectId: request.subjectId,
    tier: "easy",
    prompt: "Generated cached",
    solution: "42",
    source: "generated"
  };
  const selector = createPracticeProblemSelector(
    {
      async findAuthoredProblem() {
        return undefined;
      },
      async findGeneratedProblem() {
        return cached;
      },
      async saveGeneratedProblem(problem) {
        return problem;
      }
    },
    {
      async generate() {
        throw new Error("should not be called");
      }
    }
  );

  assert.equal(await selector.select(request), cached);
});

test("practice selector generates and saves when no bank or cache exists", async () => {
  const selector = createPracticeProblemSelector(emptyRepository(), {
    async generate(input) {
      assert.deepEqual(input, { subject: "algebra", tier: "easy" });
      return {
        problem: "Solve 2*x = 8",
        solution: "x = 4"
      };
    }
  });

  assert.deepEqual(await selector.select(request), {
    subjectId: request.subjectId,
    tier: "easy",
    prompt: "Solve 2*x = 8",
    solution: "x = 4",
    source: "generated"
  });
});

test("practice selector rejects unsupported subjects with no authored bank", async () => {
  const selector = createPracticeProblemSelector(emptyRepository(), {
    async generate() {
      throw new Error("should not be called");
    }
  });

  await assert.rejects(
    () => selector.select({ ...request, generatorSupported: false }),
    PracticeProblemUnavailableError
  );
});

test("practice repository excludes already-seen same-tier problems", async () => {
  const lessonId = "22222222-2222-2222-2222-222222222222";
  const excludedProblemIds = ["authored-1"];
  const repository = createPostgresPracticeProblemRepository({
    async query(text, values) {
      assert.match(text, /source = \$3/);
      assert.match(text, /NOT \(id::text = ANY\(\$5::text\[\]\)\)/);
      assert.deepEqual(values, [
        request.subjectId,
        request.tier,
        "authored",
        lessonId,
        excludedProblemIds
      ]);

      return {
        rows: [
          {
            id: "authored-2",
            subject_id: request.subjectId,
            lesson_id: lessonId,
            tier: request.tier,
            prompt: "Solve x + 2 = 5",
            solution: "x = 3",
            source: "authored"
          }
        ] satisfies QueryResultRow[]
      };
    }
  });

  assert.deepEqual(
    await repository.findAuthoredProblem({
      ...request,
      lessonId,
      excludeProblemIds: excludedProblemIds
    }),
    {
      id: "authored-2",
      subjectId: request.subjectId,
      lessonId,
      tier: request.tier,
      prompt: "Solve x + 2 = 5",
      solution: "x = 3",
      source: "authored"
    }
  );
});

test("practice repository hashes generated prompts with pgcrypto digest", async () => {
  const repository = createPostgresPracticeProblemRepository({
    async query(text, values) {
      assert.match(text, /encode\(digest\(\$4, 'sha256'\), 'hex'\)/);
      assert.deepEqual(values, [
        request.subjectId,
        null,
        request.tier,
        "Generated prompt",
        "Generated solution"
      ]);

      return {
        rows: [
          {
            id: "generated-2",
            subject_id: request.subjectId,
            lesson_id: null,
            tier: request.tier,
            prompt: "Generated prompt",
            solution: "Generated solution",
            source: "generated"
          }
        ] satisfies QueryResultRow[]
      };
    }
  });

  assert.deepEqual(
    await repository.saveGeneratedProblem({
      subjectId: request.subjectId,
      tier: request.tier,
      prompt: "Generated prompt",
      solution: "Generated solution",
      source: "generated"
    }),
    {
      id: "generated-2",
      subjectId: request.subjectId,
      tier: request.tier,
      prompt: "Generated prompt",
      solution: "Generated solution",
      source: "generated"
    }
  );
});

function emptyRepository(): PracticeProblemRepository {
  return {
    async findAuthoredProblem() {
      return undefined;
    },
    async findGeneratedProblem() {
      return undefined;
    },
    async saveGeneratedProblem(problem) {
      return problem;
    }
  };
}
