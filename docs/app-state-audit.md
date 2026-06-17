# Learning Platform — State Audit (2026-06-12)

Read-only audit across all layers. Bottom line: **most code is genuinely real and well-written, but nothing is connected end-to-end, and a few specific things are broken.** It's an integration job, not a rebuild.

---

## What's REAL (better than expected)

- **Backend domain logic** (`services/api/src`): auth (argon2id, HMAC sessions, RBAC), learning (stages, grasp, spaced repetition, paths), practice (selector cascade), rag (pgvector cosine search), tutor (grounded Q&A), affiliate, compliance (COPPA/RLS) — all real, with unit tests.
- **DB schema** (`migrations/`): production-quality — 18+ tables, pgvector, IVFFlat index, RLS policies, COPPA triggers.
- **Ingestion pipeline** (`services/corpus-ingestion`): parse → chunk → embed → upload assets → upsert. Architecturally complete.
- **Corpus content**: ~500+ genuine lessons (many 30–60KB of serious material).
- **spatial-calculator**: FULLY FUNCTIONAL 3D visualizer (live controls, WebXR detection, postMessage protocol). The only finished front end.
- **packages**: corpus-types, object-storage (S3+local), llm-adapter — all built.

## What's BROKEN or DISCONNECTED

### 1. Frontmatter corruption (ROOT CAUSE, highest priority)
`services/corpus-ingestion/src/fix-titles.ts` prepended a stub frontmatter block to **all 946 files**, so every file now starts with:
```yaml
subject: "unknown"
catalog: "k12"
audience_tier: "9-12"
```
The **real** Obsidian metadata (correct subject, tier, chapter) still exists as a *second* YAML block underneath, but `frontmatter.ts` only reads the first block. Result: every lesson looks like subject="unknown". This alone would make ingestion collide on `UNIQUE(subject_id, slug)` and produce one giant "unknown" subject.

### 2. No HTTP server
`services/api/src/index.ts` is just re-exports. There is **no Express/Fastify/Hono, no routes, no listener.** The API is a library; the front ends have nothing to call. (Also: tts, affiliate, compliance aren't even exported from index.ts.)

### 3. Front ends hardcoded / orphaned
- **content-site**: renders from a hardcoded 2-lesson array in `src/lib/manifest.ts`. No corpus/DB/API connection.
- **learning-app**: home page is a marketing landing with **dead buttons** (no handlers). The real experience (`Shell`, `ModalityLoop`, `TutorPanel`, `PathNavigation`) is coded but **orphaned** — never routed. TutorPanel uses a `setTimeout` mock.
- **educator-console**: works, but on ephemeral in-memory mocks (resets on reload).

### 4. Infra not running
Docker Desktop is down → no Postgres/pgvector, no MinIO. Pipeline can't run.

### 5. Smaller gaps
- `corpus/catalogs.json` and `corpus/paths.json` referenced by ingest but **don't exist**.
- Migrations jump 0001 → 0004 (0002/0003 missing).
- Stub embeddings are 8-dim; schema expects `vector(1536)`.
- **No Gemini provider** in llm-adapter — only OpenAI-compatible (`local`/`hosted`). Contest requires a Gemini call.
- problem-generator: only algebra + arithmetic, deterministic (every learner gets the same problem).
- TTS: mock provider returns a 4-byte fake MP3 (caching/storage logic is real).

---

## The gap in one line

```
946 lessons on disk → [frontmatter corrupt] → ingestion can't run (no Docker, garbage metadata)
   → DB empty → API has no HTTP layer → apps read hardcoded stubs / dead landings
```

## Per-area verdicts

| Area | Verdict |
|---|---|
| content-site | SCAFFOLD (2 hardcoded lessons) |
| learning-app | SCAFFOLD (dead landing, real components orphaned) |
| educator-console | PARTIAL (works on in-memory mocks) |
| spatial-calculator | FUNCTIONAL |
| api domain logic | REAL but not served over HTTP |
| api HTTP server | MISSING |
| ingestion pipeline | REAL but blocked by frontmatter + infra |
| problem-generator | PARTIAL (2 subjects, deterministic) |
| tts | PARTIAL (mock provider) |
| corpus content | REAL (~500+ lessons) but metadata corrupted |
| infra (Postgres/MinIO) | NOT RUNNING |
| llm-adapter Gemini | MISSING (OpenAI-compatible only) |

---

## Recommended sequencing

**Track 1 — Fast visible win (no DB needed):**
1. Fix the frontmatter (read the real second block, or re-run the Obsidian adapter without `fix-titles`).
2. Build a corpus→static-content generator so content-site shows all ~50 subjects / real lessons.

**Track 2 — Make the learning-app actually work (heavier):**
3. Add an HTTP server to `services/api` (Hono/Fastify) exposing the real modules.
4. Bring up Docker (Postgres+pgvector, MinIO); fix embeddings dim + missing catalogs.json/paths.json; run ingestion.
5. Route the orphaned components (Shell/ModalityLoop/TutorPanel) and wire them to the API.

**Track 3 — Contest gates (parallel):**
6. Add a real Gemini provider to llm-adapter; wire one in-app call (tutor).
7. Expand problem-generator beyond 2 deterministic subjects.

Frontmatter fix is the keystone — it unblocks both the fast site win and the real ingestion.
