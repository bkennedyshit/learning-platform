---
date: 2026-05-26
title: "Practice GUI App — v1.1 Multi-Subject"
tags: [learning, dev-tools]
status: reference
type: index
---

# Practice GUI App — v1.1 Multi-Subject

A Vite+React+TypeScript+Tailwind frontend paired with a FastAPI Python backend that turns the **entire Learning curriculum** into an interactive study tool: browse chapter notes with rendered LaTeX and SVGs across 7 tracks / 18 subjects / 133 chapters, then generate fresh randomized drill problems on demand.

---

## Quick Start (two terminals)

**Terminal 1 — Backend:**

```bash
cd backend
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

> Run from the `practice-gui-app/` directory (not from inside `backend/`), so the module import path resolves correctly.

**Terminal 2 — Frontend:**

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**.

### Environment Variable

| Variable | Default | Purpose |
|---|---|---|
| `LEARNING_ROOT` | `C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\09 - Learning` | Root of the curriculum tree |

Override to point at a different vault location:
```bash
set LEARNING_ROOT=D:\MyVault\09 - Learning
```

---

## Architecture

The backend **dynamically discovers** all subjects by walking the `LEARNING_ROOT` file tree at startup:

1. `07 - Math and Physics/` → each child directory with a `Subject_Plan.md` becomes a math subject (`math-01` through `math-12`).
2. `08` through `13` → each is a single-subject track (`track-08` through `track-13`).
3. Chapters are discovered by globbing `*.md` files matching the `X.Y - Title.md` pattern.
4. Drill scripts are matched by finding `_practice/scripts/X.Y_*.py` files.

**Adding a new subject = create folder + chapters + scripts → restart backend → done.** No code changes needed.

The FastAPI backend imports drill scripts as Python modules (via `importlib.util`), calls their `build_problem_set()` / `render_markdown()` functions, and returns generated markdown over HTTP. The Vite frontend renders that markdown using `react-markdown` with KaTeX for LaTeX and a custom remark plugin for Obsidian-style SVG wikilinks.

---

## Sidebar UX

The sidebar displays a collapsible tree:

- **Track headings** (7 total) — click to expand/collapse
- **Subjects** within each track — click to load chapter list inline
- **Chapters** — click to view in the middle pane

Math & Physics is expanded by default (12 subjects, 94 chapters). Other tracks collapse to save space.

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/tracks` | Curriculum tree (tracks → subjects with chapter counts) |
| GET | `/api/subject/{id}` | Full subject metadata + chapter list |
| GET | `/api/chapter/{id}/{num}` | Chapter markdown + frontmatter |
| POST | `/api/drill` | Generate drill problems `{subject_id, chapter_num, count, seed}` |
| GET | `/svgs/{id}/{filename}` | Serve SVG diagrams per-subject |
| POST | `/api/refresh` | Force re-discovery (dev utility) |

---

## Out of Scope (v2+)

- Tauri packaging for distribution
- Calculator sidecar launching (MatrixCommander)
- Verify-my-answer endpoint (SymPy symbolic equivalence checking)
- Spaced-repetition scheduler

---

## File Tree

```
practice-gui-app/
├── README.md
├── .gitignore
├── backend/
│   ├── main.py              # FastAPI app + multi-subject endpoints + CORS
│   ├── drill_runner.py      # importlib-based script loader (unchanged)
│   ├── chapter_reader.py    # Dynamic curriculum discovery module
│   └── requirements.txt
└── frontend/
    ├── package.json
    ├── tsconfig.json
    ├── tsconfig.node.json
    ├── vite.config.ts        # Proxy /api + /svgs -> backend
    ├── tailwind.config.js
    ├── postcss.config.js
    ├── index.html
    └── src/
        ├── main.tsx
        ├── App.tsx           # Three-pane grid layout + multi-subject state
        ├── api.ts            # fetch wrappers (tracks, subject, chapter, drill)
        ├── types.ts          # Track, Subject, Chapter types
        ├── components/
        │   ├── Sidebar.tsx         # Hierarchical collapsible tree
        │   ├── ChapterView.tsx     # Chapter reader (subject-aware)
        │   ├── DrillPane.tsx       # Drill generator (subject-aware)
        │   └── MarkdownRenderer.tsx # Markdown + KaTeX + SVG wikilinks
        ├── plugins/
        │   └── remarkObsidianSvgWikilink.ts  # Factory: (subjectId) => plugin
        └── styles/
            └── index.css
```
