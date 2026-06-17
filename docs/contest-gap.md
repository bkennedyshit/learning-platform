# Contest Gap — Current State vs. Submission-Ready (2026-06-13)

Fast-reference for the XPRIZE/Hacker.fund entry. What's done, what's left, ranked by the hard requirements.

---

## ✅ DONE (this build window)

- **Frontmatter recovery** — 946 corpus files de-corrupted (backup at `corpus/_lessons-backup-20260612`).
- **content-site (port 4100)** — real catalog: **81 subjects / 640 lessons**, generated from corpus.
  - Math renders (KaTeX, `nonStandard` delimiters — fixed the multi-`$` desync).
  - 584 SVG/image assets resolved into `public/lesson-assets`.
  - **Mermaid diagrams render** (client-side).
  - Readable lesson typography; non-lesson files (plans/paths/readmes) excluded.
  - Tests 4/4, tsc clean.
- **learning-app (port 4200)** — functional, no longer dead:
  - Landing buttons route to `/learn`; catalog → subject → lesson.
  - Real **Modality Loop** (Read→Listen→Write→Code→Handwrite) on real content, math + Mermaid rendering, subject-scoped prev/next + progress sidebar.
  - tsc clean.
- Both apps run locally and serve real content.

---

## ❌ REMAINING — ranked by contest requirement

### Gate 1 — Gemini API in the deployed app (HARD REQUIREMENT)
- **Status: WIRED ✅ — needs an API key to go live.**
- Implemented a grounded tutor: `apps/learning-app/src/app/api/tutor/route.ts` (server-side `POST /api/tutor`) calls Gemini `generateContent`, answering **only** from the current lesson content. `TutorPanel` now calls it (real, no longer mocked) with the lesson as context.
- **To activate:** copy `apps/learning-app/.env.local.example` → `.env.local` and set `GEMINI_API_KEY` (from Google AI Studio). Verified the route responds 200; without a key it returns a graceful "not configured" message.
- This is the fast path — satisfies the Gemini gate without standing up the full Fastify+DB backend.

### Gate 2 — Uses a Google Cloud product (HARD)
- Satisfied once the tutor key is set (Gemini API call in the deployed app).

### B2E educator-console — DEFERRED (Bill's call: summer, no demand). Not touched.

### Criterion — AI-Native Operations (the "AI runs the business")
- **Status:** not built. This is the differentiator most entrants miss.
- **Do:** 2 cron-fired, logged playbooks (cheap, pay-per-call — avoid the always-on Azure-bill mistake):
  1. **Support agent** — reads inbox, drafts/sends, escalates.
  2. **Content/marketing agent** — generates lesson/video descriptions + social posts, queues for approval.
- **Capture execution logs/dashboard** from day one (required evidence).
- Stripe needs no agent (webhooks handle it).

### Criterion — Business Viability (real arms-length revenue, May–Aug 2026)
- **Status:** not wired. axon shop + Stripe exist (per Bill, verify live).
- **Do:** put a priced offer (adult coding/professional tracks) through the shop; keep monthly revenue export. Disclose related-party/pre-existing-customer revenue separately. Marketing spend can be ~$0 (content engine) — discloses well.

### Submission mechanics
- **Deploy** site + flagship app to **Vercel** (live testing access requirement).
- **Repo**: private + share with `testing@devpost.com` and `judging@hacker.fund` (or public w/ license).
- **Video** (<3 min, YouTube) showing AI live in production.
- **Narrative** (500–1000 words): human-vs-AI split (table in `xprize-hackathon-plan.md`), jobs/opportunity created, the build story.
- **Evidence**: agent logs, API usage, Stripe export, user count + testimonials.

---

## Backend (needed for the live AI tutor)
- `services/api` has real domain logic (auth/learning/practice/rag/tutor) but **no HTTP server** and **DB never populated**.
- **Do (needs Docker running):** add Fastify server + routes; `docker compose up` (pgvector + minio); run `migrate.ts`; create `corpus/catalogs.json` + `corpus/paths.json`; fix stub embeddings 8→1536; run ingestion. Then point `TutorPanel` at `/api/tutor/ask`.
- Until then: **TutorPanel is mocked** (the only remaining fake in the learning-app).

---

## Immediate next steps (fastest path to "passes Stage One + has revenue")
1. Gemini adapter + one live tutor call (clears the API gate). ← needs API HTTP layer or a thin Next route handler.
2. Deploy both apps to Vercel + private repo + judge emails.
3. Confirm Stripe live + put the adult-tracks offer up.
4. Stand up the 2 ops playbooks with logging.
5. Start the content engine (videos → shorts) driving signups.

> Shortcut option: a thin **Next.js route handler** in the learning-app calling Gemini directly for the tutor would satisfy the Gemini gate WITHOUT standing up the full Fastify+DB backend — fastest path to a compliant deployed app.
