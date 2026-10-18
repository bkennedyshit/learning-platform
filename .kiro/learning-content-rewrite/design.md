# Design: Learning Curriculum Content Rewrite

## Overview

This feature is an editorial and validation pipeline layered on top of the existing Learning Platform corpus generator. It does not create a second content system and does not bypass the existing index-promotion gate.

The pipeline is:

```text
Backlog CSV
  -> subject Rewrite_Batch
  -> source lesson rewrite
  -> evidence record
  -> corpus generator
  -> manifest validation
  -> rendered lesson QA
  -> Content Site build
  -> sitemap/robots verification
  -> reviewed deployment
```

The Learning App is still in development. The rewrite must therefore author content that is useful to the public Content Site and structurally compatible with the Learner App, while never promising a UI or modality feature that does not exist in production.

## Repository safety

The clean SEO worktree is:

`C:\Users\billk\projects\learning-platform-seo`

The main checkout at:

`C:\Users\billk\projects\learning-platform`

contains unrelated uncommitted work. It is not an input for destructive operations. Agents must not reset, stash, clean, or commit that checkout.

The rewrite specification and batch artifacts belong under `.kiro/learning-content-rewrite/` in the clean worktree. The existing indexing work remains under `.kiro/learning-platform/`.

## Data flow

### Source content

Lesson source remains in the repository's existing corpus/content directories and continues through the existing generator. Each source lesson retains its slug, title, subject, audience tier, chapter, previous/next relationships, and cross-links.

### Backlog

The current generated backlog is:

- `learning-lesson-backlog-2026-10-17.csv`
- `LEARNING-LESSON-BACKLOG-2026-10-17.md`

Each batch selects lessons from that backlog and creates a batch record containing:

```text
batch_id
subject(s)
lesson slugs
old word counts
new word counts
authoritative sources
code/calculation checks
affiliate review result
index-gate result
build/test result
commit/deployment
```

### Content gate

The existing generator determines whether a lesson is indexable. The rewrite process supplies better source content; it does not manually flip a lesson's SEO state.

A lesson remains gated when it is a stub, contains scaffold markers, uses the generic template, lacks enough real content, or fails another existing validation. A passing lesson receives normal indexable metadata and enters the sitemap through generated output.

## Lesson authoring contract

Every lesson rewrite should be written against the following contract:

1. **Orientation:** title, audience, prerequisites, and why the topic matters.
2. **Objectives:** 2–5 measurable outcomes.
3. **Core explanation:** precise definitions, notation, vocabulary, and boundaries.
4. **Worked instruction:** at least two examples with intermediate reasoning.
5. **Misconceptions:** topic-specific errors and corrections.
6. **Practice:** at least three tasks with answers, hints, or a rubric.
7. **Transfer:** one application or connection to a related topic.
8. **Navigation:** subject hub, previous/next, and related lesson links.

Subject-specific adaptations:

- **Mathematics:** show substitutions, transformations, units, domain restrictions, and answer verification.
- **Science:** distinguish observation, hypothesis, model, mechanism, variables, and evidence; do not invent lab results.
- **Programming:** include runnable snippets, inputs/outputs, error handling, complexity or tradeoffs where relevant, and version-sensitive notes.
- **History/civics:** distinguish primary evidence, interpretation, chronology, and uncertainty; link authoritative sources.
- **Writing/literacy:** include a worked passage, revision decisions, practice prompt, and rubric.
- **Languages:** include examples, pronunciation/grammar constraints, exercises, and answer keys.
- **Music/art/design:** include concrete analysis, notation/visual vocabulary, a demonstration, and a practice task.
- **Business/finance/health:** use educational framing, current sources, and explicit limitations.

## Batch sequencing

### Phase 0: pilot

- Algebra I: 8 lessons.
- Goal: prove the authoring schema, examples, answer-key format, gate behavior, and rendered output.

### Phase 1: connected foundational subjects

- Algebra II & Pre-Calculus.
- Geometry.
- Pre-Algebra.
- Statistics & Probability.
- Early Numeracy K-5.

### Phase 2: science and literacy foundations

- Physical Science K-8.
- Earth Science.
- Life Science K-8.
- Early Literacy & Writing.
- Research Writing & Academic Literacy.
- Writing Craft & Rhetoric.

### Phase 3: humanities and social sciences

- Civics & Government.
- US History.
- World History.
- Geography.
- Art History.
- Ethics & Philosophy.
- History of Science & Ideas.

### Phase 4: learner development and applied subjects

- Intro Psychology.
- Intro Sociology.
- Performance Biology & Neuroscience of Learning.
- Economics.
- Finance & Investing.
- Music Theory.
- Mandarin Chinese.

A batch should normally contain 5–10 lessons and should not mix unrelated subjects unless the batch exists specifically to repair a shared prerequisite path.

## Evidence strategy

Source quality is determined by subject:

- Mathematics and computer science: university open course materials, official language/runtime documentation, standards bodies, and reproducible calculations.
- Science and health: government agencies, NIH/CDC/NASA/NOAA, university departments, and peer-reviewed material where a claim depends on research.
- History/civics: archives, museums, government or educational institutions, and primary sources.
- Languages: official dictionaries, language academies, university language resources, and established educational references.
- Finance: government regulators and consumer-education sources; no individualized recommendations.

Sources should be linked inline where they support a material claim. The batch evidence record should also preserve the source list independently of prose so later reviewers can audit it.

## Affiliate design

The affiliate system belongs to the resource layer, not the exercise layer:

```text
lesson explanation -> practice -> answer key -> next learning step -> optional resource card
```

A resource card may recommend an approved book, course, tool, or project component only when it directly follows from the lesson. It must use the registered affiliate merchant, display the disclosure, and carry the required link attributes. No affiliate placement should appear beside an answer or imply that buying a product improves a learner's score.

## Validation architecture

For each batch, run:

```text
1. source schema validation
2. word-count and scaffold scan
3. evidence/source inventory check
4. internal-link resolution
5. subject-hub and prev/next validation
6. generated-manifest validation
7. noindex/sitemap assertion
8. unit tests
9. typecheck
10. production build
11. rendered HTML spot checks
12. deployment smoke checks
```

The build must verify both positive and negative cases:

- rewritten lesson: indexable, canonical, present in sitemap;
- unfinished lesson: noindex, follow, absent from sitemap;
- invalid internal link: build/test failure;
- wrong subject or tier: ingestion failure;
- missing answer/practice content: batch QA failure.

## Failure handling

- If a source claim cannot be verified, remove it, qualify it, or mark the lesson for review; do not guess.
- If a lesson cannot honestly reach 500 useful words, leave it gated and record why.
- If a subject's lessons depend on missing prerequisites, rewrite the prerequisite batch first.
- If a build fails from unrelated pre-existing code, document it separately and do not weaken the test.
- If generated output differs beyond the expected batch delta, stop before commit.

## Rollback and deployment

Each batch is one focused commit. The commit includes source content and only the generated files required by the repository. Deployment occurs only after all batch checks pass. A failed deployment or bad content batch is reverted by deploying the previous commit; lesson slugs remain stable so rollback does not create URL churn.
