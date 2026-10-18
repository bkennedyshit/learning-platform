# Requirements: Learning Curriculum Content Rewrite

## Introduction

The Learning content corpus contains 640 lessons shared by the public Content Site and the in-development Learning App. The technical indexing repair is complete, but 213 lessons remain noindexed because they are generic scaffolds or explicit stubs. This spec defines the editorial rewrite program that turns those lessons into legitimate instructional material without reintroducing thin content, fabricated claims, broken links, or inappropriate affiliate promotion.

The program is intentionally batch-based. A lesson is not promoted because a word counter reaches 500; it is promoted only when it teaches the named topic, provides usable practice, and passes the existing content-site index gate.

## Inventory baseline

- 640 lessons total.
- 427 finished/indexable lessons.
- 173 generic scaffold/template lessons.
- 40 explicit stubs/TODO lessons.
- 213 lessons requiring work.
- 27 subject hubs with no finished lessons and therefore currently gated.
- Existing SEO/indexing worktree commit: `193fcc2`.

## Glossary

- **Lesson**: an authored instructional unit in the shared Corpus.
- **Rewrite_Batch**: 5–10 lessons from one subject or closely related subject family, reviewed and deployed together.
- **Content_Gate**: the existing generator logic that determines whether a lesson is indexable and included in the sitemap.
- **Subject_Hub**: the page that introduces a subject and links its lessons.
- **Affiliate_Resource**: a contextual commercial recommendation shown outside the core exercise/lesson flow and covered by the site's disclosure.
- **Evidence_Record**: source links, calculations, code checks, or editorial notes supporting claims made in a lesson.

## Requirements

### Requirement 1: Preserve the shared corpus and URL contract

**User Story:** As the platform operator, I want rewritten lessons to remain compatible with the shared corpus and existing links, so that the Content Site and Learning App continue to use one source of truth.

#### Acceptance Criteria

1. THE rewrite program SHALL preserve each lesson's existing slug unless a separately tested redirect is added.
2. THE rewrite program SHALL preserve the existing lesson schema, subject mapping, audience tier, chapter ordering, previous/next links, and generated-content pipeline.
3. WHEN a lesson is rewritten, THE generated manifest SHALL remain valid for every consuming surface.
4. THE rewrite program SHALL not hand-edit generated output as the primary content source.
5. THE rewrite program SHALL not modify unrelated uncommitted work in the dirty main checkout.

### Requirement 2: Meet the instructional quality threshold

**User Story:** As a learner, I want a lesson to actually teach its topic rather than display reusable filler, so that I can understand and practice the skill.

#### Acceptance Criteria

1. EACH completed lesson SHALL contain at least 500 words of topic-specific instruction, excluding repeated navigation and boilerplate.
2. EACH completed lesson SHALL define the named concept in language appropriate to its audience tier.
3. EACH completed lesson SHALL include specific learning objectives that are observable and not merely a restatement of the title.
4. EACH completed lesson SHALL include at least two worked examples, demonstrations, or source analyses appropriate to the subject.
5. EACH completed lesson SHALL include at least two topic-specific misconceptions, failure modes, or boundary conditions.
6. EACH completed lesson SHALL include at least three practice tasks and an answer key, rubric, or self-check method.
7. EACH completed lesson SHALL explain prerequisites and provide a concrete next step.
8. A lesson SHALL NOT be considered complete while it contains scaffold phrases such as `The foundational building block of this unit`, `System Overlay`, `Ready for expansion`, or unresolved `TODO` markers.

### Requirement 3: Maintain factual validity and evidence

**User Story:** As a learner and platform operator, I want lessons to contain accurate information that can be audited, so that the site does not trade SEO growth for misinformation.

#### Acceptance Criteria

1. Claims about formulas, code behavior, historical events, scientific mechanisms, health, finance, safety, or standards SHALL be checked against an authoritative source or a reproducible calculation.
2. Each batch SHALL retain an evidence record containing the authoritative sources used for claims that are not common instructional knowledge.
3. The program SHALL NOT invent studies, statistics, quotations, experiments, client results, certifications, credentials, or product testing.
4. Illustrative examples SHALL be labeled as examples and SHALL NOT be presented as measured platform results.
5. Code examples SHALL be syntax-checked or executed when practical; failures SHALL be corrected or explicitly described.
6. Health, finance, legal, and safety lessons SHALL include appropriate educational framing and SHALL NOT provide individualized professional advice.

### Requirement 4: Support learner navigation and the application

**User Story:** As a learner moving through a subject path, I want each lesson to connect to the surrounding curriculum, so that the public site and in-development application reinforce one another.

#### Acceptance Criteria

1. EACH completed lesson SHALL link to its Subject_Hub.
2. EACH completed lesson SHALL link to a valid previous, next, or related lesson when one exists.
3. EACH Subject_Hub SHALL list finished lessons before unfinished lessons and SHALL not imply that unfinished lessons are complete.
4. EACH Rewrite_Batch SHALL verify that all internal lesson links resolve to valid public routes.
5. The rewrite SHALL not describe unfinished Learning App features as available.
6. Content intended for the Learner App SHALL remain compatible with the Read → Listen → Write → Code → Handwrite modality loop where applicable.

### Requirement 5: Keep index promotion automatic and honest

**User Story:** As a site operator, I want weak lessons kept out of search until they are ready, so that unfinished content does not dilute the site's quality signals.

#### Acceptance Criteria

1. Lessons that fail the Content_Gate SHALL render `noindex, follow` and SHALL be excluded from the sitemap.
2. A lesson that meets the editorial standard SHALL become indexable through the existing gate without a manual robots or sitemap edit.
3. Each batch SHALL record before/after counts for indexable lessons, gated lessons, Subject_Hubs, and sitemap URLs.
4. The program SHALL never add fabricated publication or modification dates to make a lesson appear fresh.
5. The program SHALL not request indexing for lessons that still fail the gate.

### Requirement 6: Affiliate and commercial-content boundaries

**User Story:** As a learner, I want the lesson to remain useful rather than becoming an ad, and as the operator, I want affiliate revenue to remain compliant.

#### Acceptance Criteria

1. Affiliate links SHALL appear only where the resource directly extends the lesson's subject or project.
2. Affiliate links SHALL not appear inside exercises, answer keys, navigation controls, or the core learning loop.
3. Every affiliate placement SHALL use the site's registered merchant data and required `sponsored`/`nofollow` attributes.
4. Every monetized page SHALL show a clear affiliate disclosure near the commercial placement and link to the site's full disclosure policy.
5. The program SHALL not add pending, unapproved, stale, or invented affiliate URLs.
6. Affiliate recommendations SHALL not influence factual conclusions or lesson assessment.

### Requirement 7: Batch review and deployment safety

**User Story:** As the operator, I want each batch validated before release, so that one rewrite cannot break the corpus, app, sitemap, or SEO redirects.

#### Acceptance Criteria

1. Each Rewrite_Batch SHALL contain 5–10 lessons except for an explicitly documented smaller final batch.
2. Each batch SHALL pass word-count, scaffold-residue, link-resolution, schema, and index-gate checks.
3. Each batch SHALL pass the Content Site tests, typecheck, production build, and relevant lint checks before deployment.
4. Pre-existing unrelated failures SHALL be reported separately and SHALL not be hidden by weakening checks.
5. Commits SHALL stage only files belonging to the batch and its generated outputs.
6. A deployment report SHALL include slugs, old/new word counts, sources, indexability delta, verification commands, commit hash, and deployment result.

### Requirement 8: Curriculum completion tracking

**User Story:** As the operator, I want a durable backlog, so that 213 rewrites can be completed systematically instead of being regenerated inconsistently.

#### Acceptance Criteria

1. The backlog SHALL list every lesson's subject, slug, word count, gate status, and rewrite status.
2. The backlog SHALL group work by Subject_Hub and identify subjects with zero finished lessons.
3. Completed lessons SHALL record the batch, evidence sources, validation result, and deployment commit.
4. A subject SHALL be considered restored only when its hub and the required finished lessons pass the Content_Gate and link checks.
5. The completion report SHALL distinguish rewritten, intentionally retired, still gated, and awaiting review lessons.
