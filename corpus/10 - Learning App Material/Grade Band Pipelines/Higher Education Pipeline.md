---
date: 2026-05-29
title: "Higher Education Pipeline"
tags: [higher-education, college, university, pipeline, curriculum, early-college]
type: pipeline
grade-band: higher-ed
status: active
---

# 🎓 Higher Education Pipeline

> Early college / university entry-level subjects. Most of the heavy lifting is already done in `09 - Learning`. This document maps college intro courses to vault tracks and identifies remaining gaps.

*Back to [[K-12 Curriculum Pipeline]] · [[Bill's Vault/README]]*

---

## The Higher Ed Premise

The vault's `09 - Learning` directory was designed for **adult self-directed learners** — which means it's already pitched at early-college to graduate level. The higher-ed pipeline has less to build and more to **organize and surface:**

1. **Map college course names → vault tracks** (so a college student can find the right content)
2. **Identify true gaps** (intro courses that have no vault equivalent)
3. **Build the "intro" versions** of graduate-level tracks for learners arriving with no background
4. **Add standardized test prep** (SAT, ACT, AP) as an on-ramp layer

---

## College Course → Vault Track Mapping

### Mathematics

| Course | Credits | Vault track | Coverage |
|--------|---------|------------|---------|
| Pre-Calculus / College Algebra | 3 | Track 16 — Algebra II/Pre-Calc | ✅ Full |
| Calculus I (Differential) | 4 | Track 01 — Math (Calculus chapters) | ✅ Full |
| Calculus II (Integral) | 4 | Track 01 | ✅ Full |
| Calculus III (Multivariable) | 4 | Track 01 | ✅ Full |
| Linear Algebra | 3 | Track 01 | ✅ Full |
| Differential Equations | 3 | Track 01 | ✅ Full |
| Probability & Statistics | 3 | Track 17 | ✅ Full Subject_Plan |
| Discrete Mathematics | 3 | Track 70 (planned) | 🔴 Gap |
| Abstract Algebra | 3 | Track 01 (partial) | 🟡 Partial |

### Natural Sciences

| Course | Credits | Vault track | Coverage |
|--------|---------|------------|---------|
| General Biology I & II | 4+4 | Track 02 — Biology | ✅ Full |
| General Chemistry I & II | 4+4 | Track 03 — Chemistry | ✅ Full |
| Physics I & II (Mechanics/E&M) | 4+4 | Track 01 — Physics | ✅ Full |
| Anatomy & Physiology I & II | 4+4 | Track 40 — Anatomy | ✅ Full |
| Earth Science / Environmental | 3 | Track 21 | ✅ Subject_Plan |
| Neuroscience (Intro) | 3 | Track 05 | ✅ Full |
| Biochemistry | 3 | Track 03 (partial) + Track 02 | 🟡 Partial |
| Cell Biology | 3 | Track 02 | ✅ Partial |

### Computer Science & Engineering

| Course | Credits | Vault track | Coverage |
|--------|---------|------------|---------|
| Intro to Programming (Python) | 3 | Track 08 — Python | ✅ Full |
| Data Structures & Algorithms | 3 | Track 08 (chapters 8.4-8.5) + Track 19 | ✅ Covered |
| Computer Architecture & OS | 3 | Track 08 (chapter 8.3) | ✅ Covered |
| Databases | 3 | Track 14 — SQL + Track 16 | ✅ Full |
| Networks & Web | 3 | Track 17 — Networking | ✅ Full |
| Software Engineering / System Design | 3 | Track 19 | ✅ Full |
| Machine Learning | 3 | Track 23 — AI & ML | ✅ Full |
| Theory of Computation | 3 | Track 15 — Compilers (partial) | 🟡 Partial |

### Social Sciences & Humanities

| Course | Credits | Vault track | Coverage |
|--------|---------|------------|---------|
| Intro Microeconomics | 3 | Track 20 | ✅ Subject_Plan |
| Intro Macroeconomics | 3 | Track 20 | ✅ Subject_Plan |
| Intro Psychology | 3 | Track 68 (planned) | 🔴 Gap |
| Intro Sociology | 3 | Track 69 (planned) | 🔴 Gap |
| US History / World History | 3 | Tracks 50 / 49 | ✅ Subject_Plan |
| Political Science | 3 | Track 54 — Civics (planned) | 🔴 Gap |
| Philosophy | 3 | Track 07 — Philosophy of Mind | ✅ Partial |
| Research Writing / Composition | 3 | Track 72 (planned) | 🔴 Gap |

### World Languages

| Course | Credits | Vault track | Coverage |
|--------|---------|------------|---------|
| Spanish 101-402 | 3×4 | Track 36 | ✅ Full A1-B2 |
| French 101-402 | 3×4 | Track 41 | ✅ Full A1-B2 |
| Italian 101-302 | 3×3 | Track 42 | ✅ Full A1-B1 |
| Latin 101-302 | 3×3 | Track 43 | ✅ Full beginner-advanced reader |
| Mandarin 101-302 | 3×3 | Track 22 | ✅ Subject_Plan |
| Japanese 101-302 | 3×3 | Track 37 | ✅ Subject_Plan |

---

## Standardized Test Prep Integration

### SAT / ACT

The SAT and ACT are the primary college entrance exams in the US. The platform's K-12 content directly supports test prep — no separate test-prep track needed. Alignment:

| Test section | Vault tracks that cover it |
|-------------|--------------------------|
| SAT Math (Algebra, Advanced Math, Problem-Solving) | Tracks 44, 45, 46, 47, 48 |
| SAT Reading & Writing (grammar, rhetoric, evidence) | Track 38 — English |
| ACT English | Track 38 |
| ACT Math | Tracks 44-48 |
| ACT Science (data interpretation, experiments) | Track 17 — Statistics + any science track |
| ACT Reading | Track 38 |

**Test prep strategy built into the platform:**
- Each chapter that covers SAT/ACT-tested content gets an `sat_act_relevance` frontmatter tag
- A dedicated `/prep/sat` and `/prep/act` page on the platform aggregates all relevant chapters with difficulty ratings
- Drill scripts can be configured to SAT-style multiple-choice with answer explanation format

### AP Exam Alignment

Each high school subject in the vault is built to AP depth. The [[Standardized Test Prep/AP Subject Alignments]] document maps every AP course to the specific vault chapters that cover it.

**Platform feature (Tier 2+):** An "AP Mode" toggle on any subject filters the content to exactly what appears on that AP exam, with the FRQ (free-response) format modeled in the drill scripts.

---

## What Higher Ed Students Actually Need from the Platform

Based on research into college student learning challenges:

1. **Prerequisite gap filling** — "I'm in Calc II but my algebra is weak." The platform's prerequisite graph lets students quickly identify and patch gaps.

2. **Just-in-time review** — "My midterm is in 3 days." The LEARNING_PATH files in each subject tell students exactly which chapters to prioritize.

3. **Free textbook alternative** — Most college students spend $200-400/semester on textbooks. Every vault subject links to free, peer-reviewed alternatives (OpenStax, MIT OCW, etc.).

4. **Drill practice on demand** — Practice problem sets that generate new questions. No more "I've seen all the even-numbered problems."

5. **Cross-subject connections** — College courses feel isolated. The vault's wikilink graph shows students how Statistics connects to AI/ML, how Chemistry connects to Biology, how Latin connects to French.

---

## The "Early College" Track

For students 16-18 who are ahead of their grade band, the platform offers an **Early College Track** — a curated path that skips the K-12 review and goes directly to college-level content:

```
Early College Track:
  Math:      Track 16 (Pre-Calc) → Track 01 (Calc I/II/III/LA)
  Science:   Track 02 (Bio) + Track 03 (Chem) + Track 01 (Physics)
  CS:        Track 08 (Python) → Track 23 (AI/ML)
  Languages: Any Track 36-43 or 56 at B1+ level
  Writing:   Track 38 (English) → Track 72 (Research Writing, when built)
  Econ:      Track 20 (Micro + Macro)
```

Completing this track is equivalent to a strong community college first year.

*Previous: [[9-12 High School Pipeline]]*
