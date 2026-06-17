---
title: "10 - Learning App Material: README"
subject: "Learning App Material"
catalog: k12
audience_tier: 9-12
chapter: "Chapter 1"
type: readme
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# 📱 10 — Learning App Material

> **This folder is the platform engineering half of the learning app.**
> The other half — the actual curriculum content Bill is studying — lives in [`09 - Learning`](00---09---Learning-Index).

---

## The Two Halves — Clearly Defined

| Folder | What it is | Who it's for |
|--------|-----------|-------------|
| `05-Knowledge_Foundation/09 - Learning/` | **Bill's personal study vault.** Anatomy, French, Italian, Latin, Neuroscience, AI/ML, Math, Physics, etc. — what Bill is cramming into his head right now. Eventually these notes graduate into `05-Knowledge_Foundation/` proper as "what I know." | Bill |
| `05-Knowledge_Foundation/10 - Learning App Material/` | **The app platform build.** K-12 curriculum design, grade band pipelines, subject specs, app architecture, test prep alignment — everything needed to ship a learning platform for students from K through early college. | The app / other learners |

> Note on `09 - Learning` tracks 44-56: Pre-Algebra, Algebra I, Geometry, Statistics, World History, US History, Economics, Earth Science, and Mandarin are in `09 - Learning` because **Bill may study those too** — they're his vault. The app-side equivalents live here in `10` under `Subjects/01-12`. The content overlaps; the ownership is different.

---

## What's in This Folder

```
10 - Learning App Material/
├── README.md                          ← You are here
├── K-12 Curriculum Pipeline.md        ← Master grade-band → subject → status map
├── Subject Gap Manifest.md            ← What's missing, priority order, tracking table
├── App Pipeline Architecture.md       ← Technical spec: vault → platform (ingestion, API, data model)
│
├── Subjects/                          ← App-side subject specs (not Bill's personal study)
│   ├── 01 - Early Literacy & Writing      ← K-5 phonics, reading, writing
│   ├── 02 - Early Numeracy K-5            ← K-5 math (counting through fractions/decimals)
│   ├── 03 - Life Science K-8              ← NGSS life science K-8
│   ├── 04 - Physical Science K-8          ← NGSS physical science K-8
│   ├── 05 - Civics & Government           ← AP Gov + state civics requirement
│   ├── 06 - Geography                     ← Physical + human geography grades 6-9
│   ├── 07 - Art History                   ← AP Art History, visual literacy
│   ├── 08 - Music Theory                  ← AP Music Theory, notation through counterpoint
│   ├── 09 - Intro Psychology              ← AP Psychology, college intro
│   ├── 10 - Intro Sociology               ← College intro sociology, CLEP
│   ├── 11 - Discrete Mathematics          ← CS foundation: logic, graphs, combinatorics
│   └── 12 - Research Writing              ← Academic literacy, citation, AP Lang FRQ
│
├── Grade Band Pipelines/
│   ├── K-5 Early Elementary Pipeline.md
│   ├── 6-8 Middle School Pipeline.md
│   ├── 9-12 High School Pipeline.md
│   └── Higher Education Pipeline.md
│
└── Standardized Test Prep/
    ├── AP Subject Alignments.md
    └── SAT Math Pipeline.md
```

---

## Subject Directory (App Tracks 01–12)

Each subject has: `Subject_Plan.md` (full curriculum + free resource catalog), `LEARNING_PATH.md`, `README.md`, and 8 chapter stubs.

| # | Subject | Grade band | AP / Standard | Status |
|---|---------|-----------|--------------|--------|
| 01 | [Early Literacy & Writing]() | K-5 | CCSS ELA K-5 | 🟡 Subject_Plan + stubs |
| 02 | [Early Numeracy K-5]() | K-5 | CCSS Math K-5 | 🟡 Subject_Plan + stubs |
| 03 | [Life Science K-8]() | K-8 | NGSS LS | 🟡 Subject_Plan + stubs |
| 04 | [Physical Science K-8]() | K-8 | NGSS PS | 🟡 Subject_Plan + stubs |
| 05 | [Civics & Government]() | 8-12 | AP US Gov | 🟡 Subject_Plan + stubs |
| 06 | [Geography]() | 6-9 | C3 Geo Standards | 🟡 Subject_Plan + stubs |
| 07 | [Art History]() | 9-12 | AP Art History | 🟡 Subject_Plan + stubs |
| 08 | [Music Theory]() | 9-12 | AP Music Theory | 🟡 Subject_Plan + stubs |
| 09 | [Intro Psychology]() | 12/college | AP Psychology | 🟡 Subject_Plan + stubs |
| 10 | [Intro Sociology]() | 12/college | CLEP Sociology | 🟡 Subject_Plan + stubs |
| 11 | [Discrete Mathematics]() | 11-12/college | CSTA CS Level 3 | 🟡 Subject_Plan + stubs |
| 12 | [Research Writing & Academic Literacy]() | 11-12/college | CCSS W 11-12 | 🟡 Subject_Plan + stubs |

---

## App Content Already in `09 - Learning` (Cross-Referenced Here)

These subjects are in Bill's personal study vault AND serve as app curriculum. The `09 - Learning` versions are the content source; this folder references them:

| 09-Learning track | Subject | Grade band | AP / Coverage |
|------------------|---------|-----------|--------------|
| Track 13 | Pre-Algebra | 6-8 | — |
| Track 14 | Algebra I | 8-9 | — |
| Track 15 | Geometry | 9-10 | — |
| Track 16 | Algebra II & Pre-Calculus | 10-11 | AP Calculus prep |
| Track 17 | Statistics & Probability | 11-12 | AP Statistics ✅ |
| Track 18 | World History | 9-10 | AP World History ✅ |
| Track 19 | US History | 11 | AP US History ✅ |
| Track 20 | Economics | 12 | AP Micro + Macro ✅ |
| Track 21 | Earth Science | 6-9 | NGSS Earth Science |
| Track 22 | Mandarin Chinese | All | HSK 1-4 |
| Track 40 | Anatomy | 11-12/college | A&P ✅ |
| Track 41 | French | 9-adult | AP French ✅ |
| Track 42 | Italian | 9-adult | ACTFL |
| Track 43 | Latin | 9-adult | AP Latin ✅ |
| Track 36 | Spanish | 9-adult | AP Spanish ✅ |
| Track 02 | Biology | 9-12 | AP Biology ✅ |
| Track 03 | Chemistry | 9-12 | AP Chemistry ✅ |

---

## The Platform Vision (One Paragraph)

> **Bill's Vault Platform** is the only free, open-source, curriculum-grade learning system that covers K-12 through early college with the rigor of a university textbook, the resource curation of a research librarian, and the active recall tooling of a professional tutor — across 50+ subjects. The curriculum content lives in `09 - Learning`. This folder builds the delivery layer.

Full product brief: [LEARNING_PLATFORM_VISION.md](LEARNING_PLATFORM_VISION)

---

## Build Tiers

| Tier | What | Cost | Time |
|------|------|------|------|
| **1 — Static Site MVP** | Vault markdown → Astro static site; full-text search; zero hosting | $0 | 6-8 weeks |
| **2 — Interactive** | In-browser drill runner (Pyodide); progress tracking (Supabase) | Minimal | +3-4 months |
| **3 — Full Platform** | Auth; adaptive paths; AI companion (RAG); educator dashboard; Flutter mobile | SaaS infra | +6-12 months |
