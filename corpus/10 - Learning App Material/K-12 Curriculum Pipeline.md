---
date: 2026-05-29
title: "K-12 Curriculum Pipeline"
tags: [K-12, curriculum, pipeline, grade-bands, standards-alignment]
type: master-index
status: living-document
---

# 🏫 K-12 Curriculum Pipeline

> Master index mapping every grade band → required subjects → vault status → app delivery plan.

*Cross-reference: [[Subject Gap Manifest]] · [[Bill's Vault/05-Knowledge_Foundation/10 - Learning App Material/README]] · [[Grade Band Pipelines/K-5 Early Elementary Pipeline]] · [[Grade Band Pipelines/6-8 Middle School Pipeline]] · [[Grade Band Pipelines/9-12 High School Pipeline]] · [[Grade Band Pipelines/Higher Education Pipeline]]*

---

## Overview

The United States K-12 system spans **13 grade levels** (K through 12), covering roughly ages 5–18. For the platform, we map these into **four grade bands** with distinct pedagogical approaches:

| Band | Grades | Ages | Pedagogical approach | Vault status |
|------|--------|------|---------------------|-------------|
| **Early Elementary** | K–5 | 5–11 | Phonics, numeracy, discovery-based science, narrative social studies | 🔴 Needs full build |
| **Middle School** | 6–8 | 11–14 | Structured problem-solving, disciplinary thinking, first formal algebra | 🟡 Pipelines built |
| **High School** | 9–12 | 14–18 | Departmental subjects, AP tracks, standardized test prep | 🟡 Pipelines built |
| **Higher Ed / Early College** | 13+ | 17–22 | University-level intro courses, research methods, professional skills | ✅ Mostly in `09 - Learning` |

---

## Core Subject Domains

Every K-12 system revolves around six core domains. The vault must cover all six at every grade band:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  DOMAIN 1: MATHEMATICS                                                    │
│  K-2: Counting/Number Sense → 3-5: Operations/Fractions →               │
│  6-8: Pre-Algebra/Algebra I/Geometry → 9-12: Algebra II/Pre-Calc/Stats  │
│  College: Calculus/Linear Algebra (already in 09-Learning Track 01)      │
├─────────────────────────────────────────────────────────────────────────┤
│  DOMAIN 2: ENGLISH LANGUAGE ARTS (ELA)                                   │
│  K-5: Phonics/Reading/Writing → 6-8: Literature/Composition →           │
│  9-12: AP English Literature / AP Language & Composition                 │
│  College: Research Writing / Academic Literacy                           │
├─────────────────────────────────────────────────────────────────────────┤
│  DOMAIN 3: SCIENCE                                                        │
│  K-5: Intro Science → 6-8: Life/Earth/Physical Science →                │
│  9-12: Biology/Chemistry/Physics/Earth Science/AP tracks                 │
│  College: Anatomy, Neuroscience, AI/ML, etc. (in 09-Learning)           │
├─────────────────────────────────────────────────────────────────────────┤
│  DOMAIN 4: SOCIAL STUDIES / HISTORY                                      │
│  K-5: Community/Family/US Geography → 6-8: World History/Civics →       │
│  9-12: US History/World History/AP Gov/Economics                         │
│  College: Political Science, Sociology, Economics (partial in 09)       │
├─────────────────────────────────────────────────────────────────────────┤
│  DOMAIN 5: WORLD LANGUAGES                                               │
│  K-8: Language exposure → 9-12: Spanish/French/Mandarin to B1+          │
│  College: Full language tracks (in 09-Learning Tracks 36-43)            │
├─────────────────────────────────────────────────────────────────────────┤
│  DOMAIN 6: COMPUTER SCIENCE / TECHNOLOGY                                 │
│  K-8: Digital literacy → 9-12: AP CS Principles/AP CS A                 │
│  College: Full CS stack (in 09-Learning Tracks 08-23)                   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Grade-by-Grade Subject Map

### K–2 (Ages 5–8) — Foundational Literacy & Numeracy

| Subject | Standard | Vault subject | Status |
|---------|----------|--------------|--------|
| Early Literacy (phonics, decoding, sight words) | CCSS ELA K-2 | Track 53 — Early Literacy & Writing | 🔴 Planned |
| Early Numeracy (counting, addition, subtraction) | CCSS Math K-2 | Track 57 — Early Numeracy | 🔴 Planned |
| Intro to Science (life, earth, physical concepts) | NGSS K-2 | Track 58 — Life Science K-8 | 🔴 Planned |
| Social Studies (family, community, maps) | C3 Framework | Track 55 — Geography (partial) | 🔴 Planned |

### 3–5 (Ages 8–11) — Building Knowledge

| Subject | Standard | Vault subject | Status |
|---------|----------|--------------|--------|
| Reading Comprehension & Writing | CCSS ELA 3-5 | Track 53 | 🔴 Planned |
| Arithmetic, Fractions, Decimals | CCSS Math 3-5 | Track 57 | 🔴 Planned |
| Earth Science / Life Science | NGSS 3-5 | Tracks 52, 58 | 🟡 Earth Science built |
| US Geography & World Cultures | C3 Framework | Track 55 | 🔴 Planned |

### 6–8 (Ages 11–14) — Middle School

| Subject | Standard | Vault subject | Status |
|---------|----------|--------------|--------|
| Pre-Algebra | CCSS Math 6-8 | **Track 13 — Pre-Algebra** | ✅ Subject_Plan built |
| Algebra I | CCSS Math 8 | **Track 14 — Algebra I** | ✅ Subject_Plan built |
| Geometry | CCSS Math 7-8 | **Track 15 — Geometry** | ✅ Subject_Plan built |
| Life Science (cells, genetics, evolution) | NGSS MS-LS | Track 58 — Life Science | 🔴 Planned |
| Earth & Space Science | NGSS MS-ESS | **Track 21 — Earth Science** | ✅ Subject_Plan built |
| Physical Science | NGSS MS-PS | Track 59 — Physical Science | 🔴 Planned |
| World History | C3/NCSS | **Track 18 — World History** | ✅ Subject_Plan built |
| Civics & Geography | C3 Framework | Tracks 54, 55 | 🔴 Planned |
| ELA 6-8 | CCSS ELA 6-8 | Track 38 — English | 🟡 Subject_Plan exists |
| World Language I | ACTFL | Tracks 36, 41, 56 | ✅ Spanish, French, Mandarin |
| CS Fundamentals | CSTA K-12 | Track 08 — Python | ✅ Built |

### 9–12 (Ages 14–18) — High School

| Subject | Standard | Vault subject | Status |
|---------|----------|--------------|--------|
| Algebra II | CCSS Math | **Track 16 — Algebra II/Pre-Calc** | ✅ Subject_Plan built |
| Pre-Calculus | CCSS Math | Track 16 (same) | ✅ |
| Calculus (AP Calc AB/BC) | College Board AP | Track 01 — Math (full calc) | ✅ Built |
| Statistics (AP Stats) | College Board AP | **Track 17 — Statistics** | ✅ Subject_Plan built |
| Biology (AP Bio) | NGSS HS-LS | Track 02 — Biology | ✅ Built |
| Chemistry (AP Chem) | NGSS HS-PS | Track 03 — Chemistry | ✅ Built |
| Physics (AP Physics 1/2/C) | NGSS HS-PS | Track 01 (Physics) | ✅ Built |
| Anatomy & Physiology | State standards | Track 40 — Anatomy | ✅ Built |
| Earth Science / Environmental | NGSS HS-ESS | Track 21 + Track 67 | 🟡 Earth Sci built |
| US History (AP US History) | College Board | **Track 19 — US History** | ✅ Subject_Plan built |
| World History (AP World History) | College Board | **Track 18 — World History** | ✅ Subject_Plan built |
| US Government (AP Gov) | College Board | Track 54 — Civics | 🔴 Planned |
| Economics (AP Micro/Macro) | College Board | **Track 20 — Economics** | ✅ Subject_Plan built |
| AP English Language | College Board | Track 38 — English | 🟡 Subject_Plan |
| AP English Literature | College Board | Track 38 — English | 🟡 Subject_Plan |
| Spanish I-IV / AP Spanish | ACTFL / AP | Track 36 — Spanish | ✅ Built |
| French I-IV / AP French | ACTFL / AP | Track 41 — French | ✅ Built |
| AP CS Principles | College Board | Track 08 — Python | ✅ Built |
| AP CS A (Java) | College Board | Track 65 — AP CS A | 🔴 Planned |
| AP Psychology | College Board | Track 06 — Behavioral Psych | ✅ Partial |

### Higher Education Entry (Ages 17–22)

| Subject | Course equivalent | Vault subject | Status |
|---------|-----------------|--------------|--------|
| Calculus I/II/III | Math 101-301 | Track 01 | ✅ Built |
| Linear Algebra | Math 310 | Track 01 | ✅ Built |
| Statistics & Probability | Stats 101 | Track 17 | ✅ Subject_Plan |
| General Biology | Bio 101 | Track 02 | ✅ Built |
| General Chemistry | Chem 101 | Track 03 | ✅ Built |
| Anatomy & Physiology | Bio 201 | Track 40 | ✅ Built |
| Intro Programming (Python) | CS 101 | Track 08 | ✅ Built |
| Data Structures & Algorithms | CS 201 | Track 08/19 | ✅ Built |
| Intro to AI/ML | CS 401 | Track 23 | ✅ Built |
| Intro Economics (Micro + Macro) | Econ 101/102 | Track 20 | ✅ Subject_Plan |
| Intro Psychology | Psych 101 | Track 68 | 🔴 Planned |
| Intro Sociology | Soc 101 | Track 69 | 🔴 Planned |
| Academic Writing / Research | Comp 101 | Track 72 | 🔴 Planned |
| Spanish I-IV | Lang 101-402 | Track 36 | ✅ Built |
| French I-IV | Lang 101-402 | Track 41 | ✅ Built |
| Mandarin I-IV | Lang 101-402 | Track 22 | ✅ Subject_Plan |

---

## Standards Alignment Reference

The platform aligns to four major standards frameworks:

| Framework | Full name | Applies to | Key source |
|-----------|----------|-----------|-----------|
| **CCSS** | Common Core State Standards | Math + ELA, K-12 | [corestandards.org](http://www.corestandards.org/) |
| **NGSS** | Next Generation Science Standards | Science, K-12 | [nextgenscience.org](https://www.nextgenscience.org/) |
| **C3** | College, Career, and Civic Life Framework | Social Studies, K-12 | [socialstudies.org/c3](https://www.socialstudies.org/c3) |
| **College Board AP** | Advanced Placement course frameworks | Grades 9-12 | [apcentral.collegeboard.org](https://apcentral.collegeboard.org/) |
| **ACTFL** | American Council on Teaching of Foreign Languages | World Languages K-12 | [actfl.org](https://www.actfl.org/) |
| **CSTA** | Computer Science Teachers Association Standards | CS K-12 | [csteachers.org](https://csteachers.org/page/standards) |

---

## Navigation

- [[Grade Band Pipelines/K-5 Early Elementary Pipeline]] — Full K-5 subject detail
- [[Grade Band Pipelines/6-8 Middle School Pipeline]] — Full 6-8 subject detail
- [[Grade Band Pipelines/9-12 High School Pipeline]] — Full 9-12 subject detail
- [[Grade Band Pipelines/Higher Education Pipeline]] — College entry courses
- [[Subject Gap Manifest]] — Prioritized build list
- [[App Pipeline Architecture]] — Technical delivery spec
