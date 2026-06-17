---
title: "Subject Gap Manifest"
subject: "Learning App Material"
catalog: k12
audience_tier: 9-12
chapter: "Chapter 1"
type: manifest
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# 📋 Subject Gap Manifest

> What's built, what's missing, and what to build next. Updated whenever a subject is completed.

*Cross-reference: [README](README) · [K-12 Curriculum Pipeline](K-12-Curriculum-Pipeline) · [09 - Learning Index](00---09---Learning-Index)*

---

## How Content Is Organized

**Two locations, two purposes:**

1. **`09 - Learning/`** — Bill's personal study curriculum. Any subject here is something Bill is learning or may learn. Also serves as app content. Tracks 01–56.

2. **`10 - Learning App Material/Subjects/`** — App-only subjects not in Bill's personal study list. Numbered APP-01 through APP-12 (and growing). Subjects here fill K-12 gaps that wouldn't be in Bill's personal vault.

---

## ✅ Built — `09 - Learning` (App-Ready)

| Track | Subject | Grade band | Depth |
|-------|---------|-----------|-------|
| 01 | Math & Physics (12 sub-subjects, 94 chapters) | 11-grad | ✅ Full |
| 02 | Biology | 9-12 | ✅ Full 8 chapters |
| 03 | Chemistry | 9-12 | ✅ Full 8 chapters |
| 05 | Neuroscience | College | ✅ Full |
| 06 | Behavioral Psychology & RL | College | ✅ Full |
| 08 | Python | 9-college | ✅ Full 16 chapters |
| 40 | Anatomy | 11-college | ✅ Full 8 chapters |
| 41 | French | 9-adult | ✅ Full 8 chapters |
| 42 | Italian | 9-adult | ✅ Full 8 chapters |
| 43 | Latin | 9-adult | ✅ Full 8 chapters |
| 36 | Spanish | 9-adult | ✅ Full |
| 44 | Pre-Algebra | 6-8 | 🟡 Subject_Plan + stubs |
| 45 | Algebra I | 8-9 | 🟡 Subject_Plan + stubs |
| 46 | Geometry | 9-10 | 🟡 Subject_Plan + stubs |
| 47 | Algebra II & Pre-Calculus | 10-11 | 🟡 Subject_Plan + stubs |
| 48 | Statistics & Probability | 11-12 | 🟡 Subject_Plan + stubs |
| 49 | World History | 9-10 | 🟡 Subject_Plan + stubs |
| 50 | US History | 11 | 🟡 Subject_Plan + stubs |
| 51 | Economics | 12 | 🟡 Subject_Plan + stubs |
| 52 | Earth Science | 6-9 | 🟡 Subject_Plan + stubs |
| 56 | Mandarin Chinese | All | 🟡 Subject_Plan + stubs |

---

## ✅ Built — `10 - Learning App Material/Subjects/` (App-Only)

These are subjects that belong on the platform but aren't in Bill's personal study list.

| APP # | Subject | Grade band | AP / Standard | Depth |
|-------|---------|-----------|--------------|-------|
| APP-01 | Early Literacy & Writing | K-5 | CCSS ELA K-5 | 🟡 Subject_Plan + 8 stubs |
| APP-02 | Early Numeracy K-5 | K-5 | CCSS Math K-5 | 🟡 Subject_Plan + 8 stubs |
| APP-03 | Life Science K-8 | K-8 | NGSS LS | 🟡 Subject_Plan + 8 stubs |
| APP-04 | Physical Science K-8 | K-8 | NGSS PS | 🟡 Subject_Plan + 8 stubs |
| APP-05 | Civics & Government | 8-12 | AP US Gov | 🟡 Subject_Plan + 8 stubs |
| APP-06 | Geography | 6-9 | C3 Geo | 🟡 Subject_Plan + 8 stubs |
| APP-07 | Art History | 9-12 | AP Art History | 🟡 Subject_Plan + 8 stubs |
| APP-08 | Music Theory | 9-12 | AP Music Theory | 🟡 Subject_Plan + 8 stubs |
| APP-09 | Intro Psychology | 12/college | AP Psychology | 🟡 Subject_Plan + 8 stubs |
| APP-10 | Intro Sociology | 12/college | CLEP Sociology | 🟡 Subject_Plan + 8 stubs |
| APP-11 | Discrete Mathematics | 11-12/college | CSTA CS L3 | 🟡 Subject_Plan + 8 stubs |
| APP-12 | Research Writing & Academic Literacy | 11-12/college | CCSS W 11-12 | 🟡 Subject_Plan + 8 stubs |

---

## 🔴 Still Missing — Priority 1 (Blocks Full K-12 Coverage)

These are needed before the platform can claim complete K-12 coverage:

| APP # | Subject | Grade band | Why blocking | Est. build |
|-------|---------|-----------|-------------|-----------|
| APP-13 | **Early Social Studies K-5** | K-5 | Community/family/US geography — required in all state K-5 standards | 1 week |
| APP-14 | **AP Computer Science A (Java)** | 10-12 | Most-taken CS AP exam; Track 08 covers concepts but in Python not Java | 2 weeks |
| APP-15 | **AP Environmental Science** | 11-12 | Track 21 covers ~65%; needs Units 4-7 (land use, energy, pollution) | 1 week |
| APP-16 | **Health & Human Development** | 6-12 | Required in most states; nutrition, mental health, relationships | 1 week |

---

## 🟡 Missing — Priority 2 (Important but Not Blocking)

| APP # | Subject | Grade band | Notes |
|-------|---------|-----------|-------|
| APP-17 | Portuguese | 9-adult | 250M speakers; 3rd Romance language after Spanish/French |
| APP-18 | Ancient Greek | College | Natural follow-on from Latin; same case-system architecture |
| APP-19 | AP Statistics (expanded drill set) | 11-12 | Track 17 has Subject_Plan; needs Python drill scripts for all 8 chapters |
| APP-20 | US Government Expanded | 11-12 | APP-05 covers AP Gov; this adds state/local government for non-AP learners |

---

## 🟢 Missing — Priority 3 (Future)

| APP # | Subject | Notes |
|-------|---------|-------|
| APP-21 | Medieval Latin | Extension of Track 43; Augustine, Aquinas, Dante's Latin works |
| APP-22 | Graphic Design & Visual Communication | Design literacy for the digital age |
| APP-23 | Financial Literacy | Personal finance; investing; taxes — complements Track 20 Economics |
| APP-24 | Logic & Philosophy | Introduction to formal logic and philosophical argument |

---

## Build Priority Order

```
CURRENT SPRINT (done):
  ✅ APP-01 through APP-12 — all Subject_Plans + stubs

NEXT SPRINT:
  APP-13 Early Social Studies K-5  ← completes K-5 social studies
  APP-14 AP CS A (Java)            ← closes the biggest AP CS gap
  APP-15 AP Environmental Science  ← extends Track 21

FUTURE:
  Portuguese, Ancient Greek
  Financial Literacy
  Expanded drill scripts for all 09-Learning stubs (44-56)
```

---

## Tracking Legend

| Symbol | Meaning |
|--------|---------|
| ✅ Full | Subject_Plan + LEARNING_PATH + 8 full expanded chapters + practice scripts |
| 🟡 Subject_Plan + stubs | Subject_Plan (complete) + LEARNING_PATH + README + 8 chapter stubs (content TBD) |
| 🔴 Planned | Identified in gap manifest; not yet started |
