---
title: "App Pipeline Architecture"
subject: "Learning App Material"
catalog: k12
audience_tier: 9-12
chapter: "Chapter 1"
type: technical-spec
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# ⚙️ App Pipeline Architecture

> Technical spec for how vault markdown → web platform. This is the engineering blueprint for Tier 1 (MVP) through Tier 3 (full platform).

*Cross-reference: [README](README) · [LEARNING_PLATFORM_VISION.md](LEARNING_PLATFORM_VISION)*

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        THE VAULT (Source of Truth)                       │
│  /05-Knowledge_Foundation/09 - Learning/                                 │
│  Markdown + YAML frontmatter + Mermaid + LaTeX + wikilinks              │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │  Git push triggers build
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      INGESTION PIPELINE (CI/CD)                          │
│  GitHub Actions workflow → runs vault-to-mdx transformer                │
│  Outputs: MDX files + search index + subject graph JSON                 │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │
                    ┌──────────┴───────────┐
                    ▼                      ▼
┌───────────────────────────┐  ┌──────────────────────────────────────────┐
│   STATIC SITE (Tier 1)    │  │  INTERACTIVE API (Tier 2+)               │
│   Astro / Next.js         │  │  FastAPI / Cloudflare Workers            │
│   Pagefind search         │  │  Drill runner endpoint                   │
│   Zero hosting cost       │  │  Progress tracking (Supabase)            │
│   Cloudflare Pages        │  │  Pyodide client-side Python              │
└───────────────────────────┘  └──────────────────────────────────────────┘
                    │                      │
                    └──────────┬───────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         LEARNER LAYER (Tier 3)                           │
│  Auth (Supabase Auth) + Progress DB + AI Study Companion                │
│  Flutter mobile app + Educator dashboard                                │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Tier 1: Static Site MVP

### Goal
Turn the vault into a fully navigable, searchable public website. Zero cost. Deploy in 6-8 weeks.

### Ingestion Pipeline

**Step 1 — Wikilink resolution**
```python
# vault_to_mdx.py — core transformer
import re, pathlib, json

def resolve_wikilinks(content: str, slug_map: dict) -> str:
    """
    Convert [Note Name](Note-Name) and [Display Text](Note-Name) to relative MDX links.
    [README](README)
      → <Link href="/subjects/anatomy">Anatomy</Link>
    """
    pattern = r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]'
    def replace(m):
        target = m.group(1).strip()
        display = m.group(2) or target.split('/')[-1]
        slug = slug_map.get(target, '#')
        return f'[{display}]({slug})'
    return re.sub(pattern, replace, content)
```

**Step 2 — Frontmatter extraction**
Every vault note has YAML frontmatter. Extract into a typed Subject / Chapter / Drill object:
```typescript
interface VaultNote {
  path: string;           // relative to vault root
  slug: string;           // URL-safe path
  frontmatter: {
    title: string;
    date: string;
    tags: string[];
    type: 'subject-plan' | 'chapter' | 'readme' | 'learning-path' | 'manifest';
    subject?: string;     // e.g. "40 - Anatomy"
    chapter?: string;     // e.g. "40.4"
    status: 'draft' | 'complete' | 'planning';
  };
  content: string;        // raw markdown
  mdx: string;           // transformed MDX
}
```

**Step 3 — Math rendering**
- LaTeX `$$...$$` blocks → KaTeX server-side rendering
- Inline `$...$` → KaTeX inline
- Library: `katex` npm package; render at build time for zero client-side latency

**Step 4 — Diagram rendering**
- Mermaid fenced blocks → SVG via `@mermaid-js/mermaid-core` at build time
- Inline `<svg>` blocks → pass through unchanged (already Obsidian-safe)

**Step 5 — Search index**
- Tool: [Pagefind](https://pagefind.app/) — static site search; runs on the built output
- Indexes: title, frontmatter tags, full content
- Produces: binary index files served from CDN alongside static pages
- Config: weight title > tags > body; filter by subject, grade-band, type

**Step 6 — Subject graph JSON**
```json
{
  "subjects": [
    {
      "id": "anatomy",
      "track": 40,
      "title": "40 - Anatomy",
      "gradeBands": ["9-12", "higher-ed"],
      "prerequisites": ["biology", "chemistry"],
      "chapters": ["40.1", "40.2", "40.3", "40.4", "40.5", "40.6", "40.7", "40.8"],
      "status": "complete",
      "resourceCount": 12
    }
  ],
  "edges": [
    {"from": "biology", "to": "anatomy", "type": "prerequisite"},
    {"from": "anatomy", "to": "neuroscience", "type": "enables"}
  ]
}
```
This graph powers the **subject roadmap visualization** and the **prerequisite checker**.

### File Structure (Output)

```
dist/
├── index.html                    ← Subject browser grid
├── subjects/
│   ├── index.html                ← All subjects
│   ├── anatomy/
│   │   ├── index.html            ← Anatomy README (hub)
│   │   ├── syllabus/index.html   ← Subject_Plan
│   │   ├── path/index.html       ← LEARNING_PATH
│   │   └── chapters/
│   │       ├── 40-1/index.html
│   │       ├── 40-2/index.html
│   │       └── ...
│   └── ...
├── resources/index.html          ← Aggregated free resource catalog
├── search/index.html             ← Search UI (Pagefind)
├── grades/
│   ├── k-5/index.html
│   ├── 6-8/index.html
│   ├── 9-12/index.html
│   └── college/index.html
└── _pagefind/                    ← Pagefind search index
```

### Tech Stack (Tier 1)

| Layer | Choice | Why |
|-------|--------|-----|
| Site generator | **Astro** | Islands architecture; zero JS by default; MDX native; fastest static site perf |
| Markdown → MDX | `@astrojs/mdx` | Native Astro integration |
| Math | **KaTeX** (`katex`) | Server-side render; no client JS required |
| Diagrams | `mermaid` + `rehype-mermaid` | Build-time SVG; no runtime dependency |
| Search | **Pagefind** | Static binary; zero server; instant full-text search |
| Hosting | **Cloudflare Pages** | Free; global CDN; instant deploys on push |
| CI/CD | **GitHub Actions** | Free for public repos; triggers on push to main |

**Total cost: $0.** No servers. No database. No auth. Just a CDN.

---

## Tier 2: Interactive Layer

### New Capabilities
- In-browser drill runner (executes Python drill scripts via Pyodide/WebAssembly)
- Progress tracking (mark chapter as Read / In Progress / Complete)
- Subject roadmap visualization (interactive prerequisite graph)
- Vocabulary flashcard mode (extract `<details>` recall prompts as SR cards)

### Drill Runner Architecture

**Option A — Pyodide (preferred for Tier 2)**
```
User clicks "Run Drill" → loads Pyodide (Python in WASM) → executes drill script in browser
No server required. Works offline after initial WASM load (~8MB).
```

**Option B — Cloudflare Worker**
```
User clicks "Run Drill" → POST /api/drill {subject, chapter, count, seed, mode}
→ Cloudflare Worker runs Python via subprocess or JS port of drill logic
→ Returns JSON array of {question, answer, hint} objects
```

Prefer Pyodide for Tier 2 to keep server costs at zero. Switch to Worker API in Tier 3 when multi-user load requires it.

### Progress Tracking Schema (Supabase)

```sql
-- Tier 2: anonymous sessions only (no auth yet)
CREATE TABLE learner_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_token TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE chapter_progress (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID REFERENCES learner_sessions(id),
  subject_slug TEXT NOT NULL,      -- e.g. 'anatomy'
  chapter_id TEXT NOT NULL,        -- e.g. '40.4'
  status TEXT CHECK (status IN ('not_started', 'in_progress', 'complete')),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(session_id, subject_slug, chapter_id)
);

CREATE TABLE drill_attempts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID REFERENCES learner_sessions(id),
  subject_slug TEXT NOT NULL,
  drill_script TEXT NOT NULL,
  mode TEXT NOT NULL,
  seed INTEGER NOT NULL,
  score INTEGER,                    -- optional, if self-graded
  completed_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Tier 3: Full Platform

### New Capabilities
- Full user accounts (email + OAuth via Supabase Auth)
- Adaptive learning paths (next-chapter recommendation based on chapter completion + drill scores)
- AI Study Companion (RAG pipeline: chapter markdown → vector DB → question answering)
- Educator dashboard (assign chapters, track cohort progress, generate drill reports)
- Flutter mobile app (offline-first, daily drill notifications, Anki-style SR mode)

### AI Study Companion Architecture (RAG)

```
Chapter markdown files
  → chunk by section (H2/H3 headers)
  → embed with text-embedding-3-small (OpenAI) or nomic-embed-text (local)
  → store in pgvector (Supabase extension)
        ↓
User asks: "Explain the brachial plexus"
  → embed query
  → cosine similarity search → retrieve top-5 chunks from anatomy/40.4
  → construct prompt: [SYSTEM: You are a tutor. Use only this context: {chunks}]
  → stream response via GPT-4o or Claude 3.5 Sonnet
  → display inline in chapter reader
```

**Key constraint:** The AI companion must be grounded to chapter content only — it should not introduce content not in the vault. This is enforced by the system prompt and strict RAG (no web retrieval).

### Platform Data Model (Full)

```typescript
// Core entities

interface Subject {
  id: string;              // 'anatomy'
  track: number;           // 40
  title: string;           // '40 - Anatomy'
  gradeBands: GradeBand[];
  prerequisites: string[]; // subject ids
  tags: string[];
  status: 'complete' | 'partial' | 'stub';
  chapterCount: number;
  hasDrills: boolean;
}

interface Chapter {
  id: string;              // '40.4'
  subjectId: string;       // 'anatomy'
  title: string;
  content: string;         // MDX
  status: 'complete' | 'draft';
  recallPrompts: string[]; // extracted from <details> blocks
  crossLinks: string[];    // outbound wikilinks resolved to subject/chapter IDs
  readingTimeMinutes: number;
}

interface DrillSet {
  id: string;
  subjectId: string;
  chapterId?: string;
  scriptPath: string;      // path to Python drill script
  modes: string[];         // e.g. ['conjugation', 'si_clauses', 'subjunctive']
  defaultCount: number;
}

interface LearnerProgress {
  learnerId: string;
  subjectId: string;
  chapterId: string;
  status: 'not_started' | 'in_progress' | 'complete';
  recallScore?: number;    // 0-100, from self-assessed recall prompts
  lastVisited: Date;
  drillAttempts: number;
}

interface Educator {
  id: string;
  name: string;
  email: string;
  cohortIds: string[];
}

interface Cohort {
  id: string;
  educatorId: string;
  name: string;
  gradeBand: GradeBand;
  assignedSubjects: string[];
  learnerIds: string[];
}
```

---

## Content Ingestion Spec

### Vault File → Platform Object Mapping

| Vault file pattern | Platform object | Key fields extracted |
|-------------------|----------------|---------------------|
| `*/Subject_Plan.md` | `Subject` | title, tags, gradeBands, prerequisites (from cross-links), resourceCatalog |
| `*/LEARNING_PATH.md` | `LearningPath` | phases, timeEstimates, prerequisites, dailyHabits |
| `*/<chapter_id> - <title>.md` | `Chapter` | title, content, status, recallPrompts, crossLinks |
| `*/_practice/scripts/*.py` | `DrillSet` | modes (from argparse choices), scriptPath |
| `*/README.md` | `SubjectHub` | quick navigation, cross-links, milestones |

### Frontmatter Required Fields

For a chapter to be ingested correctly, it must have:
```yaml
---
title: "Chapter title"
tags: [subject-tag, ...]
type: chapter                  # required: chapter | subject-plan | learning-path | readme
subject: "40 - Anatomy"        # required for chapters
chapter: 40.4                  # required for chapters
status: complete | draft        # required
---
```

### Automated Quality Checks (CI)

GitHub Actions runs these checks on every push:
```yaml
# .github/workflows/vault-quality.yml
- name: Check frontmatter
  run: python scripts/check_frontmatter.py
  # Fails if: type missing, status missing, chapter notes lack chapter field

- name: Resolve wikilinks
  run: python scripts/resolve_wikilinks.py --check
  # Fails if: wikilink targets a file that doesn't exist

- name: Test drill scripts
  run: python scripts/run_all_drills.py --count 3 --seed 42
  # Fails if: any drill script raises an exception

- name: Build search index
  run: npx pagefind --site dist
  # Fails if: build fails or index is empty
```

---

## Deployment Pipeline

```
Developer pushes to main
        │
        ▼
GitHub Actions:
  1. Run quality checks (frontmatter, wikilinks, drills)
  2. Run vault-to-mdx transformer
  3. Build Astro static site
  4. Run Pagefind indexer on built output
  5. Deploy to Cloudflare Pages
        │
        ▼
Cloudflare Pages:
  - Atomic deploy (old version live until new version ready)
  - Global CDN distribution
  - Preview URLs for PRs
        │
        ▼
Users hit the site with sub-100ms response times worldwide (CDN edge)
```

**Total deploy time target:** <3 minutes from push to live.

---

## MVP Checklist (Tier 1 Launch)

- [ ] `vault-to-mdx.py` transformer: wikilinks + frontmatter + LaTeX + Mermaid
- [ ] Astro project scaffold with layout components
- [ ] Subject browser page (grid of all 43+ subjects with grade band filter)
- [ ] Chapter reader page (MDX rendering + sidebar nav + recall prompt toggle)
- [ ] Search integration (Pagefind)
- [ ] Resource catalog page (aggregated from all Subject_Plan §2 sections)
- [ ] Grade band filter pages (/grades/k-5, /grades/6-8, /grades/9-12, /grades/college)
- [ ] Subject prerequisite visualization (static SVG graph from subject-graph.json)
- [ ] GitHub Actions CI/CD pipeline
- [ ] Cloudflare Pages deployment
- [ ] Custom domain setup (optional for MVP)
- [ ] README.md with instructions for contributors

**Estimated: 1 engineer × 6-8 weeks**
