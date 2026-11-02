---
title: "Learning platform reality-gap audit"
summary: "Measured September 3, 2026 assessment of the work between the current application and a test-ready adaptive learning product"
---

# Learning Platform Reality-Gap Audit

**Audit date:** September 3, 2026  
**Repository:** `C:\Users\billk\projects\learning-platform`  
**Audience:** Product owner and Kiro implementation agent  
**Status:** Not ready for a serious learner test  
**Supersedes optimistic interpretations of:** “89% done,” “640 lessons,” and “playable”

## Executive conclusion

This is not a small finishing pass. The repository contains a large amount of useful infrastructure, generated content, domain logic, and UI code, but the learner-facing product is substantially behind the apparent route and test counts.

The current application can render a catalog and lesson pages, start authenticated agent sessions, call typed tools, and produce an AI response. That is meaningful engineering progress. It does not mean the curriculum is complete, the links work, the AI is consistently grounded, or the adaptive-learning workflow exists as a coherent experience.

The remaining work consists of at least four major programs:

1. Curriculum content remediation and quality control.
2. URL, navigation, asset, and generation-pipeline correctness.
3. AI runtime performance and grounding architecture.
4. Actual learner-product integration across goals, instruction, practice, assessment, mastery, review, and artifacts.

Do not describe this as 89% product-complete. Route count and code coverage are not product-completion metrics.

## Evidence from the September 3 live test

### Geometry fails on the first lesson

The first Geometry lesson, `15.1 - Foundations of Geometry`, exposes three raw corpus links:

- `Subject_Plan` resolves to `/learn/geometry/Subject_Plan` and returns 404.
- `LEARNING_PATH` resolves to `/learn/geometry/LEARNING_PATH` and returns 404.
- `README` resolves to `/learn/geometry/README` and returns 404.

The source documents exist, and generated lesson-like slugs also exist:

- `15-geometry-subject-plan`
- `geometry-learning-path`
- `readme-15-geometry`

The ingestion/rendering pipeline preserves raw relative Markdown destinations instead of resolving source-document identity to canonical application routes.

The lesson also promises a “Visual Anchor” and says that a central visual schema appears below, but no actual Geometry visual is present. This creates a visibly blank or unfinished teaching moment on the first page a Geometry learner opens.

### Geometry content is generic scaffolding

The tested `15.3 - Parallel & Perpendicular Lines` lesson includes generic language such as:

- “Primary Element”
- “System Overlay”
- “The representation must match the underlying standard”
- “Outcome = Scaffold + Active Practice”
- A supposed “Obsidian CSS-variable bound interactive SVG” that is not presented as a real subject diagram

This is template scaffolding with a Geometry title, not a substantive lesson on parallel and perpendicular lines. It does not adequately teach definitions, angle relationships, transversals, slope criteria, constructions, proofs, examples, or misconceptions.

### Measured catalog-wide warning signs

A direct scan of the generated learning-app manifest found:

| Finding | Occurrences |
| --- | ---: |
| Generic template opening (“The foundation of all learning is active, visual interaction…”) | 173 |
| Explicit `TODO: Expand using the Pearson/Ambrose structure` placeholder | 40 |
| Raw `Subject_Plan` links | 378 |
| Raw `LEARNING_PATH` links | 181 |
| Raw `README` links | 179 |

These counts are string-level warning signals, not a complete pedagogical audit. They are already sufficient to prove that the problem is systemic.

The catalog claim of 640 lessons currently means 640 generated lesson routes. It does not mean 640 reviewed, substantive, correctly linked, visually complete lessons.

### Known catalog identity failure

C# and C++ both normalize to the slug/key `c`. This produces a React duplicate-key warning and creates ambiguous catalog routes. It proves the generation pipeline lacks a mandatory identity-collision gate.

## AI status and performance

### What now works

On September 3, a server-side Codex CLI provider was added so the local learning agent can reuse the machine's existing ChatGPT-authenticated `codex login` session without placing tokens in browser code.

The live path was proven:

```text
lesson UI
  -> local dev-session authentication
  -> learning-agent HTTP API
  -> typed learning-agent runtime
  -> ChatGPT-authenticated Codex CLI
  -> typed curriculum tool
  -> learner-facing response
```

A grounded AI/ML response completed successfully with three passage citations. The provider and API test suites also passed.

### Why it is slow

Measured live turns:

- One model decision with no tool execution: approximately **14.3 seconds**.
- One grounded Geometry turn requiring a tool decision and final answer: approximately **33.1 seconds**.
- One grounded AI/ML turn: approximately **35.5 seconds**.

The main cause is architectural. Every agent reasoning step launches a new ephemeral `codex exec` process. A common turn therefore performs:

1. Start Codex and load its context.
2. Ask which tool to call.
3. Execute the local typed tool.
4. Start a second fresh Codex process.
5. Send the observation and request the learner-facing answer.

The tool schemas are resent, and observations may contain a large lesson body. This produces sequential cold-start and prompt-processing costs. Friendly loading copy cannot fix this.

### Grounding is incomplete

The Geometry prompt “help me learn” called `curriculum.get_lesson`, then Codex supplied a plausible explanation about slopes. The underlying lesson was mostly generic scaffolding, and the resulting turn had no citations. The model filled curricular gaps from its general knowledge.

That may produce factually correct sentences, but it is not the promised inspectable, curriculum-grounded learning system. A confident response must not conceal weak source material.

## Why the existing tests overstate readiness

The codebase has substantial passing unit and integration coverage. Those tests establish that contracts, authorization rules, sanitizers, memory stores, tools, and deterministic fixture workflows behave as coded.

They do not currently establish:

- That every published lesson contains substantive subject instruction.
- That every internal link resolves.
- That each promised visual exists and teaches the stated concept.
- That citations appear whenever model output uses lesson evidence.
- That an entire real learner journey changes durable mastery state.
- That the agent performs acceptably under interactive latency expectations.
- That 640 routes represent 640 publishable lessons.
- That a child, learner, parent, or educator can understand the current workflow.

The release report must separate code health, content health, workflow health, provider health, and performance health.

## Actual work remaining

### Workstream A — curriculum inventory and publication states

Create an explicit status for every curriculum item:

- `outline`
- `placeholder`
- `draft`
- `reviewed`
- `published`
- `retired`

Only reviewed/published lessons should appear as normal learner-ready content. Draft and placeholder material must either be hidden from the public learner catalog or visibly labeled and excluded from completion claims.

Build a machine-readable inventory that reports, per subject:

- Total files and generated routes.
- Status distribution.
- Word/content depth.
- Placeholder/template signatures.
- Learning objectives.
- Worked examples.
- Practice and answer material.
- Visual requirements and present assets.
- Internal/external citations.
- Reviewer and review date.

**Gate:** the application must never derive “lesson complete” from file existence alone.

### Workstream B — content remediation

Review and rewrite placeholder/template lessons by subject, starting with the first learner-visible path in each catalog.

Each published lesson needs:

- Accurate subject-specific objectives.
- Definitions and conceptual model.
- At least one meaningful visual where the lesson promises one.
- Multiple worked examples at the intended grade level.
- Practice with answers or assessment criteria.
- Common misconceptions and corrective guidance.
- Prerequisite and next-step relationships.
- Source/citation review where relevant.
- Accessibility and reading-level review.

Geometry alone requires a subject-matter pass across eight lessons, not a global replacement of a few template phrases.

### Workstream C — canonical content identity and link resolution

Implement a build-time content graph with stable IDs for subjects, lessons, plans, supporting documents, assets, and concepts.

The ingestion pipeline must:

- Parse Markdown links before HTML rendering.
- Resolve relative source paths against the source file.
- Map the target file to a canonical content ID and application URL.
- Preserve heading fragments.
- Distinguish learner pages from authoring/support documents.
- Rewrite or remove authoring-only links from published lessons.
- Reject ambiguous IDs and slugs.
- Emit redirects when an already-published URL changes.

**Gate:** crawl every generated page and fail on unexpected 404s, empty destinations, broken fragments, missing images, unsafe schemes, or links to authoring-only files.

### Workstream D — visual curriculum

There are two separate visual requirements:

1. Reviewed static visuals belonging to published lessons.
2. Agent-generated personalized visuals created during tutoring.

Do not use a generic box-and-arrow placeholder to satisfy either requirement.

For reviewed lesson visuals:

- Create a visual brief per concept.
- Produce subject-accurate SVG/canvas/image assets.
- Add title, alt text, caption, and source metadata.
- Render-test at mobile and desktop sizes.
- Verify contrast, labels, math, and relationships.

For agent visuals:

- Ground the visual in the active lesson and learner question.
- Sanitize it before display.
- Allow revision, expansion, save, and export.
- Preserve provenance and lesson/concept references.
- Never silently publish it into the static corpus.

### Workstream E — fast tutoring path

Ordinary lesson questions should not require multiple cold agent processes.

Implement a fast path:

1. The server already knows the active lesson ID.
2. Retrieve the lesson and relevant passages deterministically in-process.
3. Make one model call with the learner message, bounded passages, learner state, and response contract.
4. Return the streamed explanation, citations, and check question.

Reserve multi-step agent planning for requests that truly require practice generation, assessment, state changes, artifact creation, study planning, or educator approval.

Replace per-step `codex exec` with a persistent authenticated Codex app-server/client session or another supported persistent provider boundary. Reuse model/provider readiness and conversation state without exposing credentials.

**Initial performance gates:**

- Local UI/session setup: under 500 ms after warm startup.
- First visible response signal: under 2 seconds.
- Warm simple grounded tutor answer: target under 8 seconds.
- No duplicated full-catalog or full-lesson payload on every reasoning step.
- Cancellation must terminate the active provider request and release resources.

### Workstream F — real adaptive-learning experience

The learner currently sees a long document and a side-panel conversation. The backend contains pieces for more, but the visible product does not yet deliver the loop.

Ship one coherent vertical journey:

1. Learner selects or states a goal.
2. System assesses relevant prerequisites.
3. Lesson presents a focused concept, not the entire giant document at once.
4. Tutor explains with text and/or an actual visual.
5. Learner performs an observable task.
6. System assesses the response against criteria.
7. Tutor diagnoses and repairs a misconception or advances.
8. Mastery and evidence update visibly.
9. A review is scheduled.
10. The experience resumes correctly after browser and service restart.

Read, Listen, Write, Code, and Handwrite must be meaningful learning activities with persisted evidence—not merely a button advancing local presentation state.

### Workstream G — product UX and trust

The interface must expose enough state for the learner to understand what is happening without reading developer terminology:

- Current goal and concept.
- Current activity and expected action.
- Source/citation relationship.
- Progress and mastery evidence.
- Agent working/progress state.
- Retry, cancellation, and recoverable failure.
- Draft/placeholder lesson labeling.
- Why the recommended next step was selected.

Remove raw corpus filenames, authoring links, template terminology, and developer-only concepts from learner-visible content.

## Correct execution order for Kiro

1. Preserve the current dirty worktree and run a baseline release report.
2. Add content publication states and remove placeholders from learner-ready claims.
3. Implement the canonical content graph, slug-collision failure, and link resolver.
4. Add the complete generated-site crawl and missing-visual checks.
5. Repair the eight Geometry lessons as the first quality benchmark.
6. Implement the single-call grounded tutoring fast path.
7. Replace repeated Codex CLI cold starts with a persistent authenticated provider session.
8. Require citations for lesson-grounded model output and expose weak/no-grounding states.
9. Complete one adaptive-learning vertical journey in Geometry.
10. Expand content remediation and workflow testing subject by subject.

Do not spend the next pass adding more catalog routes, models, tools, or dashboards. Reduce false completeness and prove one excellent learning path first.

## Corrected readiness model

Track readiness in independent dimensions instead of one percentage:

| Dimension | Current evidence | Test-ready requirement |
| --- | --- | --- |
| Route/render infrastructure | Strong: 81 subjects and 640 lesson routes render | Clean build and crawl with zero unintended failures |
| Curriculum completeness | Weak: at least 173 template signatures and 40 explicit placeholders | Every exposed lesson reviewed or clearly marked draft |
| Navigation integrity | Weak: hundreds of raw support-document links; first Geometry lesson has three 404s | Canonical link graph and zero unexplained internal 404s |
| Visual instruction | Weak: lessons promise visuals that are absent or generic | Reviewed subject visuals plus safe personalized artifacts |
| Agent authentication | Working locally through ChatGPT-authenticated Codex CLI | Supported startup, health reporting, secure credential boundary |
| Agent grounding | Partial: one cited response; Geometry can answer without citations from weak content | Bounded sources, mandatory evidence state, grounding tests |
| Agent performance | Poor: approximately 14–35 seconds per tested turn | Streaming and warm grounded response within product targets |
| Adaptive learning loop | Mostly backend contracts and fixtures | One visible, durable, restart-safe learner journey |
| Educator governance | Implementation pieces exist | Reviewed draft-to-publish workflow proven in UI |

## Definition of a credible next milestone

Do not call the entire platform ready. Call the next milestone complete only when:

- Geometry's eight exposed lessons are substantive and reviewed.
- Every Geometry internal link and asset passes an automated crawl.
- Each promised Geometry visual actually renders and teaches the intended concept.
- C, C#, and C++ resolve to distinct stable routes.
- A learner completes one Geometry concept through explanation, visual, practice, misconception repair, mastery update, and scheduled review.
- That workflow resumes after restart and shows its evidence.
- The ordinary grounded tutor path avoids repeated CLI cold starts and meets the published latency target.
- The release report distinguishes code, content, navigation, visuals, workflow, provider, and performance status.

Only after that vertical slice is excellent should the same process expand across the remaining subjects. This is a substantial product-completion program, not a cosmetic cleanup.

## Scope for the next Kiro session

The next session is not expected to finish the entire 81-subject corpus. Its job is to turn the Geometry path into the reference implementation and install gates that stop unfinished material from being mistaken for finished product.

### Required deliverables

- A preserved baseline report for the current dirty worktree.
- Explicit publication status in generated curriculum data and learner-visible draft labeling or filtering.
- Stable, collision-checked subject identities for C, C#, and C++.
- Canonical link rewriting plus an automated generated-page/link/asset crawl.
- Eight repaired Geometry lessons with real instruction, examples, practice, misconceptions, and rendered visuals.
- A one-model-call grounded tutoring path for normal lesson questions, with citations and clear weak-grounding behavior.
- One durable Geometry learning loop covering explanation, practice, incorrect-answer repair, mastery evidence, scheduled review, and restart/resume.
- A final report listing pass, fail, supported skip, and not configured separately.

### Work that may follow after the reference slice

- Applying the Geometry content-quality process to the other 80 subjects.
- Large-scale educator review and publication of draft lessons.
- Broader artifact types and authoring workflows beyond the proven visual/practice slice.
- Performance tuning beyond the initial warm-response target.
- Production deployment, multi-user operations, analytics, and billing.

## Copy/paste implementation brief for Kiro

> Work in `C:\Users\billk\projects\learning-platform`. Preserve every existing modification and untracked file; do not reset or replace the dirty worktree. Read `docs/learning-platform-reality-gap-audit-2026-09-03.md`, `docs/kiro-live-test-finish-handoff-2026-09-01.md`, and `docs/learning-agent-framework-handoff-2026-08-31.md` before editing. First run and save an honest baseline report. Then implement the September 3 execution order, using Geometry's eight lessons as the reference-quality vertical slice. Prioritize publication states, canonical IDs and link resolution, generated-page crawling, real Geometry content and visuals, a single-call grounded tutoring path, mandatory evidence state, and one durable misconception-to-mastery workflow. Preserve the existing SEO surface, but do not count placeholder routes as finished lessons. Verify in the real browser at desktop and mobile sizes, inspect console and network failures, restart the services to prove persistence, and return a report that separates code health, content health, navigation, visuals, workflow, provider, and latency. Do not describe the platform as ready merely because builds and unit tests pass.

## Handoff decision

As of **September 3, 2026**, the app is suitable for engineering and fixture testing, but not yet for a serious learner trial. The next credible handoff is a tested Geometry reference path with systemic integrity gates—not another catalog-size or test-count milestone.
