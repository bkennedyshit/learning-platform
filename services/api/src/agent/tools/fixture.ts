/**
 * Deterministic in-memory vertical used by domain-tool tests and the local
 * quickstart. It mirrors the shape of the real curriculum/practice services
 * without requiring Postgres, embeddings, or a live provider.
 */

export interface FixtureLesson {
  id: string;
  subjectId: string;
  slug: string;
  title: string;
  body: string;
  conceptIds: string[];
  prerequisiteLessonIds: string[];
  passages: Array<{ id: string; text: string }>;
  isProgrammingSubject: boolean;
}

export interface FixturePracticeProblem {
  id: string;
  lessonId: string;
  conceptId: string;
  tier: "easy" | "medium" | "hard" | "exam";
  prompt: string;
  correctAnswer: string;
  /** Maps a recognizable wrong answer to a misconception label. */
  misconceptions: Array<{ answer: string; conceptId: string; description: string }>;
}

export interface FixtureConcept {
  id: string;
  name: string;
  summary: string;
}

export class VerticalFixture {
  private readonly lessons = new Map<string, FixtureLesson>();
  /** Secondary index so lessons resolve by their public catalog slug too. */
  private readonly lessonsBySlug = new Map<string, FixtureLesson>();
  private readonly problems = new Map<string, FixturePracticeProblem>();
  private readonly concepts = new Map<string, FixtureConcept>();

  constructor() {
    this.seed();
  }

  /* --------------------------- registration API --------------------------- */

  /**
   * Register (or replace) a lesson, indexing it by both its stable id and its
   * public catalog slug. This is the single supported entry point used by the
   * seed data and by the trusted {@link loadCatalogIntoFixture} loader, so real
   * catalog slugs passed by the UI resolve exactly like the seed lessons.
   */
  registerLesson(lesson: FixtureLesson): void {
    this.lessons.set(lesson.id, lesson);
    this.lessonsBySlug.set(lesson.slug, lesson);
  }

  registerConcept(concept: FixtureConcept): void {
    this.concepts.set(concept.id, concept);
  }

  registerProblem(problem: FixturePracticeProblem): void {
    this.problems.set(problem.id, problem);
  }

  /** Number of distinct registered lessons (used for validation/telemetry). */
  get lessonCount(): number {
    return this.lessons.size;
  }

  private seed(): void {
    const concepts: FixtureConcept[] = [
      { id: "matrix-multiplication", name: "Matrix multiplication", summary: "Row-by-column products of matrices." },
      {
        id: "eigenvalues",
        name: "Eigenvalues",
        summary: "Scalars λ where A·v = λ·v for a nonzero eigenvector v."
      }
    ];
    for (const c of concepts) {
      this.registerConcept(c);
    }

    const lessons: FixtureLesson[] = [
      {
        id: "lesson-matrix-multiplication",
        subjectId: "linear-algebra",
        slug: "matrix-multiplication",
        title: "Matrix Multiplication",
        body: "To multiply matrices, take dot products of rows with columns. AB is defined when A's columns match B's rows.",
        conceptIds: ["matrix-multiplication"],
        prerequisiteLessonIds: [],
        passages: [
          { id: "mm-p1", text: "AB is defined when the number of columns of A equals the number of rows of B." },
          { id: "mm-p2", text: "Entry (i,j) of AB is the dot product of row i of A with column j of B." }
        ],
        isProgrammingSubject: false
      },
      {
        id: "lesson-eigenvalues",
        subjectId: "linear-algebra",
        slug: "eigenvalues",
        title: "Eigenvalues and Eigenvectors",
        body: "An eigenvalue λ of matrix A satisfies A·v = λ·v for some nonzero vector v. Solve det(A − λI) = 0 to find eigenvalues.",
        conceptIds: ["eigenvalues"],
        prerequisiteLessonIds: ["lesson-matrix-multiplication"],
        passages: [
          { id: "eig-p1", text: "A scalar λ is an eigenvalue of A when A·v = λ·v holds for a nonzero eigenvector v." },
          { id: "eig-p2", text: "Eigenvalues are the roots of the characteristic polynomial det(A − λI) = 0." }
        ],
        isProgrammingSubject: false
      }
    ];
    for (const l of lessons) {
      this.registerLesson(l);
    }

    const problems: FixturePracticeProblem[] = [
      {
        id: "prob-eig-1",
        lessonId: "lesson-eigenvalues",
        conceptId: "eigenvalues",
        tier: "medium",
        prompt: "For A = [[2,0],[0,3]], what are the eigenvalues?",
        correctAnswer: "2,3",
        misconceptions: [
          {
            answer: "0,0",
            conceptId: "eigenvalues",
            description: "Believes diagonal-matrix eigenvalues are the off-diagonal zeros rather than the diagonal entries."
          }
        ]
      }
    ];
    for (const p of problems) {
      this.registerProblem(p);
    }
  }

  /** Resolve a lesson by its stable id or its public catalog slug. */
  getLesson(lessonIdOrSlug: string): FixtureLesson | undefined {
    return this.lessons.get(lessonIdOrSlug) ?? this.lessonsBySlug.get(lessonIdOrSlug);
  }

  getConcept(conceptId: string): FixtureConcept | undefined {
    return this.concepts.get(conceptId);
  }

  search(
    query: string,
    lessonIdOrSlug?: string
  ): Array<{ lessonId: string; passageId: string; text: string; score: number }> {
    const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    const target = lessonIdOrSlug ? this.getLesson(lessonIdOrSlug) : undefined;
    const results: Array<{ lessonId: string; passageId: string; text: string; score: number }> = [];
    for (const lesson of this.lessons.values()) {
      if (target && lesson.id !== target.id) {
        continue;
      }
      for (const passage of lesson.passages) {
        const haystack = `${lesson.title} ${passage.text}`.toLowerCase();
        const score = terms.reduce((acc, term) => (haystack.includes(term) ? acc + 1 : acc), 0) / (terms.length || 1);
        if (score > 0) {
          results.push({ lessonId: lesson.id, passageId: passage.id, text: passage.text, score });
        }
      }
    }
    return results.sort((a, b) => b.score - a.score);
  }

  getPrerequisites(lessonIdOrSlug: string): FixtureLesson[] {
    const lesson = this.getLesson(lessonIdOrSlug);
    if (!lesson) {
      return [];
    }
    return lesson.prerequisiteLessonIds
      .map((ref) => this.getLesson(ref))
      .filter((l): l is FixtureLesson => l !== undefined);
  }

  getNextProblem(lessonIdOrSlug: string, excludeIds: readonly string[] = []): FixturePracticeProblem | undefined {
    const lessonId = this.getLesson(lessonIdOrSlug)?.id ?? lessonIdOrSlug;
    for (const problem of this.problems.values()) {
      if (problem.lessonId === lessonId && !excludeIds.includes(problem.id)) {
        return problem;
      }
    }
    return undefined;
  }

  getProblem(problemId: string): FixturePracticeProblem | undefined {
    return this.problems.get(problemId);
  }

  /** Deterministic grounded evaluation of an answer against fixture criteria. */
  evaluate(problemId: string, answer: string): {
    correct: boolean;
    score: number;
    misconception?: { conceptId: string; description: string };
  } {
    const problem = this.problems.get(problemId);
    if (!problem) {
      return { correct: false, score: 0 };
    }
    const normalized = answer.replace(/\s+/g, "").toLowerCase();
    if (normalized === problem.correctAnswer.replace(/\s+/g, "").toLowerCase()) {
      return { correct: true, score: 1 };
    }
    const match = problem.misconceptions.find(
      (m) => m.answer.replace(/\s+/g, "").toLowerCase() === normalized
    );
    if (match) {
      return { correct: false, score: 0, misconception: { conceptId: match.conceptId, description: match.description } };
    }
    return { correct: false, score: 0 };
  }
}
