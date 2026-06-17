---
title: "SAT Math Pipeline"
subject: "Standardized Test Prep"
catalog: k12
audience_tier: 9-12
chapter: "Chapter 1"
type: pipeline
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# 📊 SAT Math Pipeline

> Mapping the SAT Math section to vault content. Every skill tested on the SAT Math has a corresponding vault chapter.

*Back to [AP Subject Alignments](AP-Subject-Alignments) · [README](README)*

---

## SAT Math Structure (2024 Digital SAT)

The Digital SAT Math section: **44 questions, 70 minutes, 2 modules.**

### Domain 1: Algebra (35% of test — ~15 questions)

| Skill | Vault chapter | Priority |
|-------|-------------|---------|
| Linear equations in one variable | [45.2 - Linear Equations](45.2---Linear-Equations) | 🔴 High |
| Linear equations in two variables | [45.5 - Linear Functions & Graphing](45.5---Linear-Functions-&-Graphing) | 🔴 High |
| Linear inequalities | [45.3 - Linear Inequalities](45.3---Linear-Inequalities) | 🔴 High |
| Systems of linear equations | [45.6 - Systems of Equations](45.6---Systems-of-Equations) | 🔴 High |
| Linear functions (interpreting slope/intercept) | [45.5 - Linear Functions & Graphing](45.5---Linear-Functions-&-Graphing) | 🔴 High |
| Absolute value equations | [45.3 - Linear Inequalities](45.3---Linear-Inequalities) | 🟡 Medium |

### Domain 2: Advanced Math (35% of test — ~15 questions)

| Skill | Vault chapter | Priority |
|-------|-------------|---------|
| Quadratic functions and equations | [45.8 - Factoring & Quadratics](45.8---Factoring-&-Quadratics) | 🔴 High |
| Exponential functions | [47.3 - Exponential & Logarithmic Functions](47.3---Exponential-&-Logarithmic-Functions) | 🔴 High |
| Polynomial operations | [47.1 - Polynomial Functions](47.1---Polynomial-Functions) | 🟡 Medium |
| Rational expressions | [47.2 - Rational Functions](47.2---Rational-Functions) | 🟡 Medium |
| Radical equations | [47.1 - Polynomial Functions](47.1---Polynomial-Functions) | 🟡 Medium |
| Nonlinear relationships (graphs) | [45.4 - Functions & Relations](45.4---Functions-&-Relations) | 🔴 High |
| Systems with nonlinear equations | [45.6 - Systems of Equations](45.6---Systems-of-Equations) | 🟡 Medium |

### Domain 3: Problem-Solving & Data Analysis (15% of test — ~7 questions)

| Skill | Vault chapter | Priority |
|-------|-------------|---------|
| Ratios, rates, proportions | [44.1 - Ratios, Rates & Proportions](44.1---Ratios,-Rates-&-Proportions) | 🔴 High |
| Percentages | [44.3 - Fractions, Decimals & Percent](44.3---Fractions,-Decimals-&-Percent) | 🔴 High |
| Unit conversion | [44.1 - Ratios, Rates & Proportions](44.1---Ratios,-Rates-&-Proportions) | 🟡 Medium |
| Table/graph interpretation | [48.1 - Exploring Data (1-Variable)](48.1---Exploring-Data-(1-Variable)) | 🔴 High |
| Scatterplots and linear models | [48.2 - Exploring Data (2-Variable)](48.2---Exploring-Data-(2-Variable)) | 🔴 High |
| Probability and statistics | [48.4 - Probability](48.4---Probability) | 🟡 Medium |
| Evaluating statistical claims | [48.3 - Sampling & Experimental Design](48.3---Sampling-&-Experimental-Design) | 🟡 Medium |

### Domain 4: Geometry & Trigonometry (15% of test — ~7 questions)

| Skill | Vault chapter | Priority |
|-------|-------------|---------|
| Area and volume formulas | [46.8 - Area, Volume & Coordinate Geometry](46.8---Area,-Volume-&-Coordinate-Geometry) | 🔴 High |
| Lines, angles, triangles | [46.4 - Triangles](46.4---Triangles) | 🔴 High |
| Right triangles and trigonometry | [46.6 - Right Triangles & Trigonometry](46.6---Right-Triangles-&-Trigonometry) | 🔴 High |
| Circles | [46.7 - Circles](46.7---Circles) | 🟡 Medium |
| Coordinate geometry | [46.8 - Area, Volume & Coordinate Geometry](46.8---Area,-Volume-&-Coordinate-Geometry) | 🟡 Medium |

---

## SAT Math Study Path by Score Goal

### Target 500 (50th percentile) — ~4 weeks
Focus on: Tracks 44 (Pre-Algebra) + 45 (Algebra I chapters 45.1-45.6) only.

### Target 600 (75th percentile) — ~8 weeks
Complete: Track 14 + Track 15 chapters 46.4, 46.6, 46.8 + Track 17 chapters 48.1-48.2.

### Target 700 (93rd percentile) — ~14 weeks
Complete: Tracks 44, 45, 46 + Track 16 chapters 47.1-47.3 + Track 17 chapters 48.1-48.4.

### Target 780+ (99th percentile) — ~20 weeks
Complete all tracks 44-48 + all Track 16 chapters. Deep problem-solving practice using AoPS materials.

---

## Drill Script Integration

The vault's Python drill scripts can generate SAT-style multiple choice:

```bash
# Pre-Algebra: ratios and proportions
python "13 - Pre-Algebra/_practice/scripts/44_drill.py" --mode sat --count 10

# Algebra I: linear equations and systems
python "14 - Algebra I/_practice/scripts/45_drill.py" --mode sat --timed

# Statistics: data interpretation
python "17 - Statistics & Probability/_practice/scripts/48_drill.py" --mode sat_data
```

*(Scripts planned for Tier 2 development — drill script stubs in each subject's `_practice/scripts/` folder)*
