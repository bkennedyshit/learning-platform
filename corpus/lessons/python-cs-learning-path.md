---
title: "Python & CS — Learning Path"
subject: "Python"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: learning-path
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 🛤️ Python & CS — Learning Path

> This document is **hand-curated** and should remain stable. Do not auto-regenerate on README sync.

---

## 📋 Prerequisites

Before starting this track, you should have:

1. **A working Python 3.11+ installation** — verify with `python --version`
2. **Basic programming intuition** — you know what variables, loops, and functions are (your JS background covers this)
3. **A text editor you're comfortable in** — VS Code recommended; chapter 08.1 will formalize the setup
4. **Math track in progress** — Chapters 1.1–08.8 (Calculus) provide the foundation for algorithm analysis; Linear Algebra (2.x) feeds directly into GPU computing

You do NOT need:
- Prior Python experience (though your existing cheatsheets show you've started)
- Linux experience (chapter 08.7 covers this; you're on Windows and that's fine)
- CS degree knowledge (we build it here)

---

## 📖 Recommended Chapter Order

### Phase 1: Language Mastery (Weeks 1–4)

| Order | Chapter | Rationale |
|-------|---------|-----------|
| 1 | [08.1 - Setup, Tooling & Project Structure](08.1---Setup,-Tooling-&-Project-Structure) | Foundation — can't build without tools |
| 2 | [08.2 - Core Language - Syntax, Types, Control Flow & Functions](08.2---Core-Language---Syntax,-Types,-Control-Flow-&-Functions) | The language itself — everything else builds on this |
| 3 | [08.3 - OOP, Data Models & Pythonic Idioms](08.3---OOP,-Data-Models-&-Pythonic-Idioms) | Python's object model is unique; understanding `__dunder__` methods unlocks the language |
| 4 | [08.4 - Concurrency - asyncio, threading, multiprocessing & the GIL](08.4---Concurrency---asyncio,-threading,-multiprocessing-&-the-GIL) | Early exposure — you'll need async for any modern Python work |
| 5 | [08.5 - Testing, Debugging & Logging](08.5---Testing,-Debugging-&-Logging) | Before you write more code, learn to verify it |
| 6 | [08.6 - The Standard Library & Ecosystem Tour](08.6---The-Standard-Library-&-Ecosystem-Tour) | Know what's already built before you pip install |

**Phase 1 deliverable:** A CLI tool or API client (500+ lines) with full pytest coverage, async I/O, and structured logging.

### Phase 2: Developer Infrastructure (Weeks 5–8)

| Order | Chapter | Rationale |
|-------|---------|-----------|
| 7 | [08.7 - Shell, Terminal & Cross-Platform CLI](08.7---Shell,-Terminal-&-Cross-Platform-CLI) | You need shell fluency for everything that follows |
| 8 | [08.8 - Git & Version Control](08.8---Git-&-Version-Control) | Version control is non-negotiable for professional work |
| 9 | [08.9 - Docker & Containers](08.9---Docker-&-Containers) | Reproducible environments — critical for ML pipelines |
| 10 | [08.10 - Operating Systems Essentials](08.10---Operating-Systems-Essentials) | Understand what's under your Python process |
| 11 | [08.11 - Computer Networks Essentials](08.11---Computer-Networks-Essentials) | HTTP, TCP, DNS — the substrate of distributed systems |
| 12 | [08.12 - Computer Architecture - Performance Intuition](08.12---Computer-Architecture---Performance-Intuition) | Cache lines, branch prediction, SIMD — why some Python is 100x slower |

**Phase 2 deliverable:** A Dockerized Python microservice with CI/CD pipeline, proper networking, and performance profiling.

### Phase 3: Algorithms & Advanced Concurrency (Weeks 9–12)

| Order | Chapter | Rationale |
|-------|---------|-----------|
| 13 | [08.13 - Algorithms & Data Structures in Python](08.13---Algorithms-&-Data-Structures-in-Python) | The interview gate AND the foundation for ML optimization |
| 14 | [08.14 - Concurrency Models & Patterns](08.14---Concurrency-Models-&-Patterns) | Deep dive — actor models, CSP, lock-free structures for production systems |

**Phase 3 deliverable:** Solve 50+ LeetCode mediums; implement a concurrent data pipeline with backpressure.

### Phase 4: GPU & Distributed (Weeks 13–16)

| Order | Chapter | Rationale |
|-------|---------|-----------|
| 15 | [08.15 - GPU Computing & CUDA Foundations](08.15---GPU-Computing-&-CUDA-Foundations) | The hardware that trains LLMs — understand it at the kernel level |
| 16 | [08.16 - Distributed Systems & Multi-GPU Training](08.16---Distributed-Systems-&-Multi-GPU-Training) | Scale from 1 GPU to a cluster — FSDP, ZeRO, NCCL |

**Phase 4 deliverable:** Train a small transformer model across multiple GPUs with custom CUDA kernels for key operations.

---

## ⏱️ Estimated Time Per Phase

| Phase | Hours/Week | Weeks | Total Hours | Notes |
|-------|-----------|-------|-------------|-------|
| 1 | 12–15 | 4 | 50–60 | Heavy coding practice |
| 2 | 10–12 | 4 | 40–48 | More reading + lab work |
| 3 | 15–18 | 4 | 60–72 | Algorithm grinding is time-intensive |
| 4 | 12–15 | 4 | 50–60 | Hardware access needed |
| **Total** | | **16** | **200–240** | |

---

## 🔀 What to Do Alongside (Parallel Work)

| While doing... | Also work on... | Why |
|----------------|-----------------|-----|
| Phase 1 (Python core) | Math Track: Calculus (Ch. 1.1–08.8) | Big-O analysis needs limits; optimization needs derivatives |
| Phase 2 (Infrastructure) | Math Track: Linear Algebra (Ch. 2.1–2.4) | Matrix intuition before GPU chapter |
| Phase 3 (Algorithms) | Math Track: Linear Algebra (Ch. 2.5–2.8) | Eigenvalues, SVD directly used in ML algorithms |
| Phase 4 (GPU/Distributed) | AI/ML Track: [23.5 - Transformer Architectures & LLMs](23.5---Transformer-Architectures-&-LLMs) | Apply GPU knowledge to actual model training |

---

## ➡️ What Comes Next

After completing this Python & CS track:

1. **AI/ML Track** (Track 10) — You now have the Python, math, and systems knowledge to build and train models
2. **Game Dev Track** — Python for prototyping (Pygame, Godot scripting), then C++/Rust for performance-critical paths
3. **Professional Python** — Django/FastAPI for web services, or ML Engineering roles
4. **Systems Programming** — If you want to go deeper: Rust or C for the parts Python can't reach

---

## 🚫 What This Track Does NOT Cover

- **Web frameworks** (Django, Flask, FastAPI) — separate track; this is foundations
- **Data science libraries** (pandas, matplotlib) — covered in AI/ML track
- **Mobile development** — separate track
- **Frontend** — you already have JS/CSS/HTML foundations

These are intentional omissions, not gaps. The goal is **deep systems understanding**, not breadth-first survey.

---

## Related Notes
- [Subject_Plan](Subject_Plan) - Shared curriculum/python focus
