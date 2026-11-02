# Learning Platform Live-Test Finish Handoff

**Date:** September 1, 2026  
**Owner for next implementation pass:** Kiro  
**Repository:** `C:\Users\billk\projects\learning-platform`  
**Status:** The curriculum and lesson product are playable; the integrated learning-agent product is not yet ready.

> **September 3 correction:** A deeper Geometry test found systemic placeholder content, hundreds of unresolved corpus links, missing promised visuals, and unacceptable AI latency. The statement above means pages render, not that the curriculum is product-ready. Treat [the September 3 reality-gap audit](./learning-platform-reality-gap-audit-2026-09-03.md) as the current readiness assessment.

Read this with [the learning-agent framework handoff](./learning-agent-framework-handoff-2026-08-31.md). That document defines the target OpenClaw-like learning framework. This handoff records the September 1 live test and identifies the shortest route to a reliable product test.

## Preserve the current work

The worktree now contains extensive in-progress implementation across the learning app, educator console, API, LLM adapter, ingestion pipeline, release scripts, `packages/agent-contract/`, agent HTTP/service code, visual sanitization components, tests, and migrations. It also contains previously modified `.gitignore` and documentation. Treat all changes as user work. Inspect and integrate them; do not reset, discard, or rebuild them from an older audit.

## What was proven in the live app

The learning application ran at `http://localhost:4200`.

- The public product loaded and navigated correctly.
- The catalog rendered **81 subjects** and **640 lessons**.
- Subject and lesson navigation worked.
- A complete AI/ML lesson rendered its long-form content.
- The lesson showed current-path and next-lesson navigation.
- The Learning Agent workspace rendered with goal and tutor controls.
- Static lesson reading remained available when the agent was offline.
- The lesson progression control could be activated without crashing the page.

This proves the acquisition/catalog and lesson-reading layers. It does not prove the persistent adaptive learning framework.

## Release blockers found in the live test

### P0 — make the agent service part of the supported local launch

Submitting a tutor message returned `POST /api/agent/v1/agent/sessions 503`, and the UI displayed “The learning agent service is unavailable.” The frontend route exists, but the required backend was not ready or discoverable in the normal app launch.

Provide a single documented command that starts every required local component or clearly reports what is missing:

- Learning app.
- Agent/API service.
- Database and migrations.
- Corpus/RAG dependencies when required.
- Local Ollama or an explicitly configured hosted provider.
- Object/artifact storage when required.

Expose separate liveness and readiness checks. The app must distinguish service unavailable, database unavailable, provider unavailable, authentication failure, migration mismatch, and corpus not ingested.

**Acceptance test:** on a clean machine following the quickstart, one command starts the fixture environment; a learner opens a lesson, creates an agent session, receives a grounded streamed explanation, restarts the services, and resumes the same session.

### P0 — fix subject identity and routing collisions

C# and C++ both currently normalize to `/learn/c`. React logged duplicate key `c`, meaning catalog items can be duplicated or omitted and the routes cannot uniquely represent both subjects.

Use stable canonical subject identifiers and explicit slugs rather than lossy punctuation stripping. Preserve existing SEO URLs with redirects where a published URL must change. Add collision detection to content generation and route builds.

**Acceptance test:** C, C#, and C++ have distinct catalog keys and canonical routes, each route resolves its correct lessons, old published URLs redirect intentionally, and the build fails on any new duplicate slug.

### P0 — prove the adaptive learning loop, not only chat

Complete one vertical workflow through the new contracts and real services:

1. Authenticate or create a fixture learner.
2. Set a durable goal.
3. Load lesson and prerequisite evidence.
4. Ask a grounded question.
5. Present an explanation and one observable check.
6. Submit a wrong answer fixture.
7. Diagnose the misconception and select an intervention.
8. Retest with a changed problem.
9. Update mastery/progress and schedule a review.
10. Restart and explain why that review is next.

All state changes must use typed tools and produce traceable records. Do not store hidden model reasoning.

**Acceptance test:** run the workflow once with a deterministic fake model and once with one configured provider; both runs produce the same contract/trace shape and durable learner-state changes.

### P0 — finish safe inline learning visuals

The in-progress `SafeSvg`, `SafeMermaid`, PNG export, and visual-artifact work must be connected to the agent workflow and tested as rendered artifacts rather than strings.

**Acceptance test:** for a real lesson, the agent creates a labeled SVG or Mermaid visual, shows it inline with alt text, accepts a learner-requested revision, saves it to notes, exports SVG and PNG, survives reload, and rejects malicious SVG/Mermaid fixtures without script execution, external fetches, or unsafe HTML.

### P1 — verify lesson progression state

The “Continue to Next Step” control accepted a click, but the live surface did not make the new modality/state obvious enough to verify from the page. Ensure Read → Listen → Write → Code → Handwrite transitions are visible, persisted, keyboard accessible, and backed by learner-stage records rather than local-only UI state.

**Acceptance test:** complete each supported stage, reload after every transition, and verify the server-side progress record plus the visible current stage. Offline reading must continue to work.

### P1 — repair or migrate legacy lesson links

Lesson bodies contain legacy-looking relative references such as numbered markdown/chapter paths and `Subject_Plan` links. Audit the generated corpus for internal-link failures and map them to canonical application routes.

**Acceptance test:** crawl all 640 generated lessons and fail the release report for an unresolved internal lesson/subject/image link, excluding an explicit reviewed allowlist.

### P1 — fix workspace-root and browser warnings

Next.js inferred a workspace root outside the repository because of a parent `package-lock.json` alongside the repository pnpm lockfile. Configure the intended Turbopack root. Also resolve the smooth-scroll route-transition warning and keep browser console errors at zero in release tests.

### P1 — educator review and publishing

Connect agent-created visuals, examples, and practice items to the educator console as drafts with provenance, citations, semantic diff, rendered preview, approval/revision/rejection, and recoverable versions. The model must never publish directly to the SEO corpus.

## Learning workflows Kiro must ship as end-to-end tests

### Explain this visually

Select lesson text, ask “show me this,” retrieve the cited passage, generate a safe inline visual, ask one comprehension question, revise the visual on request, and save the accepted artifact to learner notes.

### Diagnose and repair a misconception

Submit an incorrect answer, identify the misconception from grounded criteria, provide a targeted explanation or worked example, retest with a changed problem, update mastery, and explain the change.

### Build my study plan

Combine the durable learner goal, prerequisites, available time, current mastery, and scheduled reviews into an editable plan. Resume and adapt it after restart.

### Turn a lesson into a review package

Create a cited summary, concept map, flashcards, practice set, and spaced-review schedule. Save each as a versioned artifact the learner can revise or delete.

### Explore with a calculator

Open an allowlisted calculator with a lesson-derived expression, ask for a prediction before showing the result, compare the prediction with the visualization, and record the learning evidence without permitting arbitrary code execution.

## Required verification command

Keep the in-progress root release scripts and make one honest report covering:

- Formatting, linting, type checking, unit tests, and production builds.
- Catalog counts and canonical-route/slug collision checks.
- Sitemap, robots, structured data, and SEO-route regression.
- Clean local bootstrap, migrations, health, and readiness.
- Agent session creation and streamed response.
- Typed-tool schemas, authorization, idempotency, and trace redaction.
- Adaptive learning loop and restart/resume.
- RAG citations and provider failure behavior.
- Progress, mastery, misconception, and review persistence.
- SVG/Mermaid sanitation, CSP, rendered visual, revision, and export tests.
- Modality-stage persistence.
- All-corpus link crawling.
- Educator draft/review/publish flow.
- Mobile and desktop browser tests with zero unexpected console errors.

Report pass, fail, supported skip, and not configured separately. A 503 with a friendly UI is graceful degradation, not a passing agent test. A generated SVG string is not a passing visual test until sanitized and rendered.

## Kiro implementation order

1. Preserve and inventory the current diff; run the in-progress release report before edits.
2. Make the local quickstart launch the agent/API dependencies and expose truthful readiness.
3. Fix C/C#/C++ canonical identities and add collision tests before further content generation.
4. Complete one durable adaptive-learning vertical slice through the new contracts.
5. Connect and verify safe visual artifacts in that slice.
6. Persist and visibly verify the modality loop.
7. Crawl and repair legacy lesson links.
8. Add educator review/publishing for visual and practice drafts.
9. Resolve Next.js root/browser warnings and make browser verification part of release.
10. Prove all five learner workflows with fixture data and one configured provider.

## Definition of ready to test

The learning platform is ready for a serious learner test when a clean local launch brings up both the lesson app and ready agent service; C, C#, and C++ resolve uniquely; a learner can complete the adaptive teaching loop with grounded citations and a safe inline visual; goals, sessions, mastery, misconceptions, modality stages, artifacts, and scheduled reviews survive restart; the static 640-lesson SEO site remains intact; and the consolidated release report has no unexplained failures or skips.
