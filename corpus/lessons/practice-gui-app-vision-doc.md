---
title: "Practice GUI App — Vision Doc"
subject: "Dev_Tools"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: vision-doc
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# Practice GUI App — Vision Doc

> **Status:** Planning. Not yet implemented. Captured so the idea doesn't get lost while we focus on content.

## The pitch (one paragraph)

Bundle the existing Qt/C++ calculators (`MatrixCommander`, `CalculusVisualizer`, `ProbabilityStudio`) **together** with a Vite-based web frontend that calls the per-chapter Python+SymPy drill generators, all packaged as a **single distributable learning app**. The audience isn't Bill — it's any student or curious learner who wants to:

- Click a topic → get a fresh randomized problem with full step-by-step solution.
- See the relevant calculator open side-by-side (e.g., choose "Eigenvalues" → MatrixCommander launches with a sample matrix loaded).
- Optionally check their hand-written work via SymPy in the backend.

This turns the curriculum from "Bill's private Obsidian vault" into "a sharable / sellable learning product."

---

## Why this matters

1. **Scaling beyond Bill.** The current setup (`python <script>.py --count N`) is fine for someone fluent in CLIs. For a broader audience, a button is friendlier.
2. **The calculators are already built.** The Qt/C++ tools at `[00 - Learning_Tools](00---Learning_Tools)` are powerful but live in isolation. Pairing each with the relevant practice generator unlocks them.
3. **Zero-cost content engine.** SymPy generates infinite, verified problems. With a UI on top, you have a Khan-Academy-style problem firehose with no manual content authoring required.
4. **Distinct product story.** Most "math practice" apps are static problem banks. This one would (a) generate fresh problems on demand, (b) open a real calculator alongside, (c) ship the Pearson-grade textbook chapters as the reference layer.

---

## Three-layer architecture (sketch)

```
┌─────────────────────────────────────────────────────────────┐
│  Frontend  —  Vite + React + TailwindCSS                    │
│  • Topic picker (tree of subjects → chapters)               │
│  • Problem display (renders the same Markdown the           │
│    drill scripts already produce, via a markdown lib)       │
│  • "New problem" / "Show solution" / "Open calculator"      │
└─────────────────────────────────────────────────────────────┘
                       │ HTTP / IPC
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Backend  —  FastAPI (Python)                               │
│  • Imports the drill scripts as modules                     │
│  • Endpoint: GET /drill/{chapter}?count=1&seed=N            │
│       → returns the same markdown the scripts generate      │
│  • Endpoint: POST /verify  (student submits work,           │
│       SymPy checks symbolic equivalence)                    │
└─────────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Calculator Sidecars  —  existing Qt/C++ tools              │
│  • MatrixCommander, CalculusVisualizer, ProbabilityStudio   │
│  • Launched as separate processes via OS shell exec         │
│  • Optionally pre-load a matrix / function from the         │
│    current problem (deeplink protocol e.g. matrix://)       │
└─────────────────────────────────────────────────────────────┘
```

### Packaging options (pick one when ready)

| Option | Pros | Cons |
|---|---|---|
| **Tauri** wrapping the Vite frontend, Python backend as sidecar | Tiny binary, native menus, cross-platform | Tauri+Python sidecar plumbing is fiddly |
| **Electron** + Python sidecar | Most familiar, lots of examples | Bigger binary, slower startup |
| **PyWebView** (Python-native) | One language, tiny dependencies | Less polished than Tauri/Electron |
| **Web-only** (host on a VPS) | Easiest to ship, share links | Requires hosting; calculators can't launch on user's machine |

For a v1, **Tauri** is the strongest fit because it preserves the offline-first feel of Obsidian + native calculators.

---

## What the user flow looks like

1. **Launch app.** Sidebar shows the same curriculum structure as the Obsidian vault (`07 Math/Physics → 02 Linear Algebra → 2.6 Eigenvalues`).
2. **Click a chapter.** Right pane shows the textbook chapter (rendered Markdown from the `.md` file, including the inline SVG visual anchor).
3. **Click "Drill me."** Frontend calls `/drill/2.6?count=1` → backend invokes `2.6_eigenvalues.py:build_problem_set(count=1)` → returns a single problem in markdown.
4. **User solves on paper / a scratch pad.** Optional: scratch pad has a built-in MathJax editor.
5. **User clicks "Open MatrixCommander."** App shells out to `MatrixCommander.exe` and passes the problem's matrix as an argv.
6. **User clicks "Show solution."** The `<details>` block expands; user verifies their work.
7. **(Stretch goal) "Verify mine."** User pastes their final answer; FastAPI calls SymPy to check symbolic equivalence vs the script's `Problem.solution_md`.

---

## What we'd reuse from the existing build

- **Drill scripts** — already `argparse`/CLI but they expose `build_problem_set(count, rng)` and `render_markdown(problems, seed)` as plain functions. The FastAPI backend just imports them. Zero rewriting.
- **Markdown renderer** — Vite + a markdown-it plugin with KaTeX renders the existing chapter `.md` files **as-is**, including SVG and `<details>` blocks.
- **Subject_Plans + chapter notes** — used as the textbook reference pane.
- **`generate_readmes.py`** pattern — same idea (walk subjects, emit a manifest) becomes the sidebar tree generator.

---

## Concrete v1 scope (when you're ready to build)

1. **Single subject pilot:** wire up just `02 - Linear Algebra & Matrix Theory` end-to-end. Eight chapters, eight scripts, one calculator (MatrixCommander).
2. **FastAPI backend** with two endpoints: `/drill/{chapter}` and `/chapter/{chapter}` (returns the markdown).
3. **Vite + React frontend** with three panes: sidebar tree / textbook view / drill view.
4. **No verify-my-answer yet.** Just generate + show solution.
5. **Tauri wrap** for distribution.

Estimated time-to-pilot: **2–3 focused weekends** for someone already comfortable with React + Python.

---

## Concrete v2 scope (later)

- Verify-my-answer endpoint (`POST /verify` with SymPy symbolic equivalence).
- Spaced-repetition scheduler in the app (so the SR plugin isn't required).
- Export problem sets to PDF (for printable practice sheets).
- Calculator sidecar deep-linking (matrix://, function://, …).
- Full curriculum coverage (all 7 tracks).
- Account / progress sync (optional cloud-backed).

---

## Why we're NOT building this now

- The CLI + Obsidian workflow already works for Bill (the primary user).
- Per-subject README files (just shipped) cover the "I forgot how to run this" refresher need.
- Content is the bottleneck, not delivery — the curriculum is still being expanded.

When the curriculum is feature-complete enough, the GUI is the natural next layer.

---

## Cross-links

- Master practice howto: [HOW_TO_USE_PRACTICE](HOW_TO_USE_PRACTICE)
- Master Learning Index: [00 - 09 - Learning Index](00---09---Learning-Index)
- Existing calculator suite vision: [CALCULATOR_SUITE_VISION](CALCULATOR_SUITE_VISION)
- Existing build instructions: [BUILD_INSTRUCTIONS_TLDR](BUILD_INSTRUCTIONS_TLDR)

---

*Vision-doc author: Bill (captured via session 2026-05-24).*
