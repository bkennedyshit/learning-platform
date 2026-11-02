# Learning Agent Framework Handoff

**Audit and handoff date:** August 31, 2026
**Intended Kiro implementation start:** August 31, 2026
**Repository:** `C:\Users\billk\projects\learning-platform`
**Live acquisition site:** `https://learning.nepa-ai.com`

## Executive decision

This is another mostly-built product. “Approximately 89% done” is a fair description of the amount of product material and domain implementation already present, but not of end-to-end integration. The remaining work is disproportionately important: the public catalog, curriculum, learner UI, and learning services exist, while the persistent AI learning framework that connects them does not.

Do not rebuild the learning platform. Finish it by adding an OpenClaw-like, learning-specific agent runtime around the working domain services.

The live content site is a valuable and independently deployable SEO/acquisition surface. Preserve its routes, canonical URLs, metadata, sitemap, static generation, and performance. The learning agent belongs behind or beside that site; it should not replace the public catalog renderer.

## Verified state on August 31, 2026

### Working product assets

- The live site presents 81 subjects and 640 lessons.
- The content generator produces the same 81 subjects and 640 lessons from the local corpus.
- The learner application builds 731 routes, including all lesson and subject pages.
- The public site has canonical URLs, sitemap generation, robots metadata, structured lesson data, Vercel Analytics, and Speed Insights.
- Lessons render Markdown, KaTeX, Mermaid, and copied image/SVG assets.
- The learner app implements the Read → Listen → Write → Code → Handwrite modality loop.
- Four interactive math tools are present: calculus, gradient descent, matrix, and probability.
- A server-side tutor route calls either local Ollama or Gemini and grounds a response in the current lesson text.
- The API package contains real implementations for authentication, authorization, progress, mastery/grasp assessment, spaced repetition, learning paths, practice selection, RAG, tutoring, TTS caching, affiliate attribution, and child/privacy compliance.
- The provider-neutral LLM adapter supports OpenAI-compatible local or hosted completion and embeddings.
- Corpus ingestion, object storage, pgvector-oriented retrieval, and database migrations exist.

### Validation run

- Content-site tests: **4 passed**.
- LLM-adapter tests: **6 passed**.
- API/domain tests: **33 passed**.
- Learning-app production build: **passed**.
- Static route generation: **731 routes**.

### Existing uncommitted work to preserve

- Modified `.gitignore`.
- Untracked `docs/content-site-image-hosting.md`.

Inspect those diffs before changing overlapping files. They predate this handoff.

## What is actually missing

The current tutor is a grounded request/response endpoint. It is useful, but it is not an agent framework comparable to OpenClaw.

Missing framework capabilities:

- A plan → act → observe → adapt agent loop.
- Typed, discoverable learning tools with validated inputs and outputs.
- Durable learner sessions and memory.
- A learner model containing mastery, misconceptions, goals, preferences, and accommodations.
- Teaching skills and workflow templates.
- Background jobs with progress, cancellation, retry, and result artifacts.
- Approval boundaries for consequential actions.
- Plugin/provider lifecycle and capability discovery.
- Structured traces explaining which evidence and tools drove a tutor decision.
- A safe artifact system for diagrams, notes, flashcards, assessments, and study plans.
- A production HTTP surface connecting the existing API services to the learner app.
- End-to-end tests proving that learning state changes after a real tutoring workflow.

The work is integration and orchestration, not curriculum generation or a frontend rewrite.

## Target product

The target is a persistent learning partner, not a generic chatbot embedded beside a lesson.

```text
Public SEO catalog (static and independently deployable)
                         |
                         v
Interactive learner app and educator console
                         |
                         v
Learning agent runtime
  model routing | sessions | skills | tools | jobs | approvals | traces
                         |
       +-----------------+------------------+
       |                 |                  |
       v                 v                  v
 Curriculum/RAG    Learner state       Learning artifacts
 lessons/search    progress/mastery    SVGs/notes/cards/plans
                         |
                         v
 Practice | assessment | review scheduler | TTS | calculators
```

Creative Claw/OpenClaw is the runtime reference. Reuse stable runtime contracts where practical, but keep learning storage, policies, UI, deployments, and domain tools separate from the creative product.

## Required implementation work

### P0 — define the learning-agent contract

Create a versioned contract for:

- Agent sessions and conversation turns.
- Typed tool definitions and tool results.
- Plans and plan revisions.
- Background jobs and progress events.
- Artifacts and provenance.
- Approval requests and decisions.
- Structured errors and retryability.
- Trace events and redaction.

The contract must work with local Ollama, hosted OpenAI-compatible providers, and Gemini without embedding provider-specific payloads into learning tools.

Acceptance test: one deterministic fake model and one real configured model can execute the same typed two-tool learning workflow and produce equivalent trace structure.

### P0 — expose the existing learning services

Add a supported HTTP/service layer around the real code in `services/api`. Do not duplicate progress, RAG, practice, or tutor logic in Next.js route handlers.

Initial tool surface:

- `curriculum.search`
- `curriculum.get_lesson`
- `curriculum.get_prerequisites`
- `learner.get_state`
- `learner.record_stage`
- `learner.record_goal`
- `practice.get_next`
- `practice.submit`
- `assessment.evaluate`
- `review.get_due`
- `review.schedule`
- `tutor.explain`
- `tutor.hint`
- `tutor.ask_socratic`
- `study_plan.create`
- `study_plan.advance`
- `visual.create`
- `visual.revise`
- `visual.present`
- `artifact.save`

Requirements:

- Validate every input and output against a versioned schema.
- Enforce account ownership and educator/learner roles server-side.
- Cite lesson and passage identifiers in grounded answers.
- Make state-changing tools idempotent where possible.
- Never let the model directly issue SQL or arbitrary filesystem paths.
- Separate read-only tools from state-changing or educator-controlled tools.

Acceptance test: an authenticated learner can begin a lesson, request an explanation, complete practice, receive an assessment, and get a scheduled review through the tool surface.

### P0 — implement durable learner memory

The agent needs domain memory, not an unlimited transcript dump.

Persist:

- Current goals and active learning paths.
- Per-concept mastery and confidence.
- Known misconceptions with supporting attempts.
- Completed modality stages.
- Due reviews and review history.
- Preferred explanation depth and modality.
- Accessibility/accommodation settings.
- Learner-created notes, diagrams, flashcards, and plans.
- A compact session summary with source references.

Do not store hidden model reasoning. Store observable decisions, tool calls, evidence, learner answers, assessments, and concise summaries.

Acceptance test: after restart, the agent recalls the learner's goal and demonstrated misconception, selects an appropriate review, and can show the records that caused that choice.

### P0 — add the adaptive teaching loop

Implement an explicit, inspectable workflow:

1. Read the learner goal and current state.
2. Retrieve the relevant lesson and prerequisite evidence.
3. Choose a teaching strategy.
4. Explain using text, a diagram, an example, or a calculator.
5. Ask the learner to do something observable.
6. Assess the response against grounded criteria.
7. Correct a misconception or advance the lesson.
8. Update mastery and schedule review.
9. Present what changed and why.

The agent should support at least these teaching skills:

- Socratic questioning.
- Worked example followed by faded guidance.
- Analogy with explicit limits.
- Visual explanation.
- Retrieval practice.
- Error diagnosis.
- Spaced review.
- Teach-back/Feynman check.

Acceptance test: a learner who answers incorrectly receives a misconception-targeted intervention and a new check, while a correct learner advances without unnecessary repetition.

### P0 — make lesson visuals first-class artifacts

The application already copies static SVG assets and renders Mermaid. The next step is to let the learning agent create and present visuals during a lesson, similar to the way the GPT application can produce an SVG and show it directly in the conversation.

Supported visual types should initially include:

- SVG concept diagrams.
- Mermaid flowcharts, sequences, state diagrams, and graphs.
- Coordinate plots and labeled geometric figures.
- Timelines, process diagrams, comparison maps, and system architecture diagrams.
- Small interactive visualizations backed by an allowlisted renderer.

Visual artifact contract:

```ts
interface LearningVisualArtifact {
  id: string;
  version: number;
  kind: "svg" | "mermaid" | "plot" | "interactive";
  title: string;
  description: string;
  altText: string;
  source: string;
  sanitizedSource: string;
  lessonIds: string[];
  conceptIds: string[];
  createdBy: "learner" | "educator" | "agent";
  provider?: string;
  createdAt: string;
}
```

Required experience:

- The tutor can decide that a visual would improve an explanation.
- The visual appears inline beside the tutor response.
- The learner can expand it into a focused presentation view.
- The learner can ask the tutor to revise a label, layout, example, or level of detail.
- The learner can inspect the source, download SVG or PNG, and save it to notes.
- An educator can review and publish an approved visual into a lesson.
- Published visuals remain static assets so they retain SEO and load-performance benefits.
- Every visual has a title, meaningful alt text, lesson/concept references, and provenance.

Security requirements:

- Never insert raw model-authored SVG or HTML through `dangerouslySetInnerHTML`.
- Sanitize SVG server-side and again at the rendering boundary.
- Reject scripts, event attributes, `foreignObject`, external resource references, unsafe links, animation abuse, and oversized/pathological documents.
- Use a strict element/attribute allowlist and enforce dimensions, `viewBox`, node count, path complexity, and byte limits.
- Render untrusted interactive artifacts in a sandboxed frame with a restrictive CSP.
- Change model-authored Mermaid rendering away from `securityLevel: "loose"`; use a strict configuration and validated source.
- Generate a raster fallback/thumbnail for sharing and failure cases.
- Keep the original model output for audit only; present the sanitized artifact.

Current warning: both lesson applications render generated HTML through `dangerouslySetInnerHTML`, and Mermaid currently uses `securityLevel: "loose"`. The current corpus is treated as reviewed/trusted input. Do not route agent-generated lesson content through that path until the sanitization boundary is implemented and tested.

Acceptance test: the tutor creates and displays a valid labeled SVG for a real lesson, revises it after learner feedback, saves it as an artifact, exports SVG and PNG, and rejects a malicious SVG fixture without executing or fetching anything.

### P1 — integrate the agent into the learner application

Replace the narrow tutor panel behavior with a session-aware learning workspace while preserving distraction-free reading.

Required UI:

- Conversation with streamed text and artifact cards.
- Current goal and lesson context.
- Visible plan with current step.
- Tool activity summarized in learner-friendly language.
- Inline visual, note, flashcard, and assessment artifacts.
- “Why this next?” explanation linked to mastery evidence.
- Progress, cancel, retry, and recoverable errors.
- Explicit confirmation for changing a goal, submitting graded work, publishing, sharing, or contacting an educator.
- A focused visual presentation mode.
- Resume across browser and service restarts.

Do not require an agent call to read an indexed lesson. Static pages must continue working when the agent provider is unavailable.

### P1 — connect the production data path

- Start Postgres/pgvector and object storage from the documented infrastructure.
- Run migrations in a clean environment.
- Ingest the normalized corpus with production-size embeddings.
- Expose health and readiness separately.
- Connect accounts, learning state, RAG, practice, and artifact storage.
- Replace the duplicate thin tutor route with the agent/service API after parity is proven.
- Keep a local, self-hosted quickstart that does not require paid APIs.

Acceptance test: a clean local installation ingests a small fixture corpus, creates a learner, completes the adaptive teaching loop, restarts, and resumes with the same state and artifacts.

### P1 — create an educator review and publishing loop

The agent may propose new lesson visuals, examples, practice questions, and corrections. It must not silently publish them to the SEO catalog.

Workflow:

1. Agent creates a versioned draft with citations and provenance.
2. Automated checks validate structure, links, math, SVG safety, accessibility, and duplicate content.
3. Educator sees a semantic diff and rendered preview.
4. Educator approves, requests revision, or rejects.
5. Approved content enters the corpus through a normal reviewed commit.
6. Static site build validates routes, metadata, and assets before deployment.

Acceptance test: an educator approves an agent-generated diagram into a fixture lesson, the static build includes it, and the previous lesson version remains recoverable.

## Protect the SEO asset

The public content site must stay boring, fast, and reliable even while the learning agent evolves.

- Preserve existing lesson and subject URLs.
- Preserve canonical metadata, sitemap, robots rules, and structured lesson data.
- Keep primary lesson content in server-rendered/static HTML.
- Do not hide content behind authentication or client-only agent rendering.
- Do not rewrite published lessons per visitor.
- Keep agent sessions out of crawlable URLs.
- Use reviewed, static visual artifacts for published pages.
- Add redirects and regression tests before changing any slug.
- Measure Core Web Vitals and static build size after visual changes.
- Feature-flag the agent independently from the catalog.

The content site acquires learners. The learner app retains and teaches them. The agent framework personalizes the experience. Those are cooperating layers, not one deployment blob.

## Creator-style learning workflows to ship

### Explain this visually

Learner selects a paragraph and asks, “Show me this.” The agent retrieves the lesson context, creates a diagram, presents it inline, asks one comprehension question, and saves the accepted visual to learner notes.

### Diagnose and repair a misconception

The learner submits a wrong answer. The agent identifies the likely misconception from grounded criteria, selects a teaching strategy, generates a focused visual or worked example, retests with a changed problem, and updates mastery.

### Build my study plan

The agent combines the learner goal, prerequisite graph, available time, current mastery, and due reviews into an editable plan. Each session advances the plan based on observed results rather than a fixed calendar alone.

### Turn a lesson into a review package

The agent creates a concise summary, concept map, flashcards, practice set, and spaced-review schedule. Every item cites the source lesson and can be revised or removed.

### Explore with a calculator

The agent passes a lesson-derived expression or matrix to an allowlisted calculator, presents the interactive result, asks the learner to make a prediction, then compares the prediction with the visualization.

## Kiro execution order

1. Write the versioned session/tool/job/artifact contract and fixtures.
2. Wrap one read-only curriculum service and one state-changing learner service as typed tools.
3. Implement deterministic agent-loop tests with a fake model.
4. Add authenticated sessions, trace events, approval boundaries, and learner memory.
5. Complete one vertical adaptive-teaching workflow without visuals.
6. Implement the sanitized visual-artifact service and malicious fixture suite.
7. Present SVG/Mermaid artifacts in the tutor UI with revision and save actions.
8. Connect Postgres, pgvector, object storage, and corpus ingestion.
9. Add provider integration and streaming after deterministic behavior is stable.
10. Implement educator review/publish and protect the static SEO build with regression tests.
11. Ship the five workflows above as reusable teaching skills.
12. Add a consolidated release command and make its report honest about live-provider/model skips.

Every milestone must leave a working end-to-end slice. Avoid implementing the entire runtime, database, UI, and artifact system in isolation before proving one learner workflow.

## Required validation

Create a root release command that reports **pass**, **fail**, **supported skip**, and **not configured** for:

- Formatting, lint, type checking, and unit tests.
- Static content generation and route-count regression.
- Canonical URL, sitemap, robots, and structured-data checks.
- Agent-loop and typed-tool contract tests.
- Auth, ownership, role, consent, and minor-safety tests.
- Learner-memory restart/resume tests.
- RAG citation and refusal tests.
- Practice → assessment → mastery → review integration.
- Local provider and hosted-provider adapters.
- Background job progress and cancellation.
- SVG/Mermaid sanitization and CSP tests.
- Visual screenshot/render checks at mobile and desktop sizes.
- Educator draft/review/publish workflow.
- Clean local bootstrap with a small fixture corpus.

Do not count a mocked answer as a live-provider test, and do not count an SVG source string as a rendered visual test.

## Guardrails

- Preserve the live acquisition site and its URL equity.
- Keep the no-paid-API local path functional.
- Never expose provider keys to browser code or model context.
- Never expose one learner's records to another learner or educator without authorization.
- Never store hidden chain-of-thought; store concise decisions, evidence, and tool activity.
- Never let the model publish directly to the corpus or public site.
- Never execute arbitrary model-authored HTML, SVG, JavaScript, shell commands, or SQL.
- Treat child safety, consent, deletion, audit, and educator visibility as runtime requirements rather than later policy work.
- Keep learning outcomes inspectable: every recommendation should point to learner evidence and curriculum sources.

## Definition of done

The learning platform is ready for a serious product test when:

- The public 640-lesson catalog remains live, crawlable, and regression-tested.
- A learner can authenticate and set a durable goal.
- The agent can inspect curriculum and learner state through typed tools.
- It can execute the adaptive teaching loop and explain its next action.
- Progress, mastery, misconception, and review state survive restart.
- The tutor can safely create, display, revise, save, and export SVG/Mermaid learning visuals.
- Published visuals require educator approval and preserve static SEO delivery.
- Local Ollama works without paid credentials; configured hosted providers use server-side credentials only.
- Failures, cancellation, approvals, and trace history are visible and recoverable.
- A clean environment passes the consolidated release report without unexplained skips.

At that point the project is no longer a large catalog with an AI chat panel. It is an OpenClaw-like learning framework backed by a real curriculum and a live acquisition engine.
