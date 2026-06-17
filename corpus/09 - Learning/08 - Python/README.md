---
date: 2026-05-24
type: subject-readme
tags: [practice, refresher, drills, source-materials, study-aids]
title: "README — 01- Python"
---

# 01- Python — Subject Hub

> One-page subject hub. Lists chapters, drill commands, source reading
> materials, and placeholders for generated study aids (NotebookLM artifacts:
> audio overviews, mind maps, quizzes, flash cards, etc.).
> Master practice guide: [[../HOW_TO_USE_PRACTICE|HOW_TO_USE_PRACTICE]].

---

## 🚀 Quick start

From a terminal in this folder:

```bash
cd "C:/Obsidian Vault/Bill's Vault/05-Knowledge_Foundation/09 - Learning/01- Python"
python "_practice/scripts/<chapter>_<topic>.py" --count 8 --seed 42
```

Output lands at `_practice/<chapter>_drills.md`. Open in Obsidian Reading
view, do the problems on paper, click **Show solution** to verify.

---

## 📜 Chapter index

- [[08.1 - Setup, Tooling & Project Structure]]
- [[08.10 - Operating Systems Essentials]]
- [[08.11 - Computer Networks Essentials]]
- [[08.12 - Computer Architecture - Performance Intuition]]
- [[08.13 - Algorithms & Data Structures in Python]]
- [[08.14 - Concurrency Models & Patterns]]
- [[08.15 - GPU Computing & CUDA Foundations]]
- [[08.16 - Distributed Systems & Multi-GPU Training]]
- [[08.2 - Core Language - Syntax, Types, Control Flow & Functions]]
- [[08.3 - OOP, Data Models & Pythonic Idioms]]
- [[08.4 - Concurrency - asyncio, threading, multiprocessing & the GIL]]
- [[08.5 - Testing, Debugging & Logging]]
- [[08.6 - The Standard Library & Ecosystem Tour]]
- [[08.7 - Shell, Terminal & Cross-Platform CLI]]
- [[08.8 - Git & Version Control]]
- [[08.9 - Docker & Containers]]
- [[Python Reference & Cheatsheets]]

---

## 🎯 Drill scripts

| Script | Chapter | Sample command |
|---|---|---|
| 1.10_os_essentials.py | [[08.10 - Operating Systems Essentials]] | `python "_practice/scripts/1.10_os_essentials.py" --count 8 --seed 42` |
| 1.11_networks.py | [[08.11 - Computer Networks Essentials]] | `python "_practice/scripts/1.11_networks.py" --count 8 --seed 42` |
| 1.13_algorithms.py | [[08.13 - Algorithms & Data Structures in Python]] | `python "_practice/scripts/1.13_algorithms.py" --count 8 --seed 42` |
| 1.15_gpu_cuda.py | [[08.15 - GPU Computing & CUDA Foundations]] | `python "_practice/scripts/1.15_gpu_cuda.py" --count 8 --seed 42` |
| 1.1_setup_tooling.py | [[08.1 - Setup, Tooling & Project Structure]] | `python "_practice/scripts/1.1_setup_tooling.py" --count 8 --seed 42` |
| 1.7_shell_cli.py | [[08.7 - Shell, Terminal & Cross-Platform CLI]] | `python "_practice/scripts/1.7_shell_cli.py" --count 8 --seed 42` |
| 1.8_git_vcs.py | [[08.8 - Git & Version Control]] | `python "_practice/scripts/1.8_git_vcs.py" --count 8 --seed 42` |
| 1.9_docker.py | [[08.9 - Docker & Containers]] | `python "_practice/scripts/1.9_docker.py" --count 8 --seed 42` |

---

## 📚 Source materials & references

_Pulled verbatim from `Subject_Plan.md §2 — Premium Free Learning Catalog`. Source of truth is the Subject_Plan; this section is a convenience copy._

### Phase 1: Language Mastery

| Chapter | Primary Resource | Supplementary |
|---------|-----------------|---------------|
| 08.1 Setup & Tooling | [Real Python: Python Development Environment](https://realpython.com/effective-python-environment/) | Poetry docs, pyproject.toml PEP 621 |
| 08.2 Core Language | **Fluent Python** (Luciano Ramalho, 2nd ed.) Ch. 1-7 | [Python docs: Data Model](https://docs.python.org/3/reference/datamodel.html) |
| 08.3 OOP & Data Models | **Fluent Python** Ch. 8-16 | Raymond Hettinger talks (PyCon) |
| 08.4 Concurrency | **Fluent Python** Ch. 19-21 | [Real Python: Async IO](https://realpython.com/async-io-python/) |
| 08.5 Testing | **Python Testing with pytest** (Brian Okken) | [pytest docs](https://docs.pytest.org/) |
| 08.6 Standard Library | [Python Module of the Week](https://pymotw.com/3/) | Official stdlib docs |

### Phase 2: Developer Infrastructure

| Chapter | Primary Resource | Supplementary |
|---------|-----------------|---------------|
| 08.7 Shell & CLI | **The Linux Command Line** (William Shotts, free) | Brian Kernighan: *UNIX: A History and a Memoir* |
| 08.8 Git | [Pro Git](https://git-scm.com/book/en/v2) (Scott Chacon, free) | [Think Like a Git](https://think-like-a-git.net/) |
| 08.9 Docker | [Docker docs: Get Started](https://docs.docker.com/get-started/) | **Docker Deep Dive** (Nigel Poulton) |
| 08.10 OS | **Operating Systems: Three Easy Pieces** (Arpaci-Dusseau, free) | MIT 6.828 xv6 labs |
| 08.11 Networks | **Computer Networking: A Top-Down Approach** (Kurose & Ross) | Beej's Guide to Network Programming (free) |
| 08.12 Architecture | **Computer Systems: A Programmer's Perspective** (Bryant & O'Hallaron) | [What Every Programmer Should Know About Memory](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf) |

### Phase 3: Algorithms & Concurrency

| Chapter | Primary Resource | Supplementary |
|---------|-----------------|---------------|
| 08.13 Algorithms & DS | **Introduction to Algorithms** (CLRS, 4th ed.) | MIT 6.006 (Erik Demaine lectures, free on OCW) |
| 08.14 Concurrency Patterns | **Concurrency in Python** (David Beazley talks) | [Trio docs](https://trio.readthedocs.io/) for structured concurrency |

### Phase 4: GPU & Distributed

| Chapter | Primary Resource | Supplementary |
|---------|-----------------|---------------|
| 08.15 GPU & CUDA | [NVIDIA CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/) | [Numba docs](https://numba.readthedocs.io/), CuPy |
| 08.16 Distributed | [PyTorch Distributed Overview](https://pytorch.org/tutorials/beginner/dist_overview.html) | ZeRO paper (Rajbhandari et al.), FSDP tutorial |

---

---

## 🧰 Generated study aids

> **Status:** placeholder. Drop links to NotebookLM-generated artifacts here as
> you create them. Each subsection currently has a single TODO bullet — replace
> or append `[[wikilinks]]` and external URLs once the artifact exists.

### 🎙️ Audio overviews & podcasts (NotebookLM)

- [ ] TODO: paste the NotebookLM "Audio Overview" link or attach the `.mp3`/`.m4a` file

### 🧠 Mind maps

- [ ] TODO: NotebookLM mind-map URL or screenshot

### ❓ Quizzes

- [ ] TODO: NotebookLM-generated quiz (paste questions or link)

### 📊 Reports & summaries

- [ ] TODO: NotebookLM "Briefing Doc" or "Study Guide" output

### 🃏 Flash cards

- [ ] TODO: deck export (Anki, Obsidian SR, NotebookLM cards)

### 🎬 Video overviews

- [ ] TODO: YouTube / loom / personal recording link

### 📋 Data tables

- [ ] TODO: structured data extracted from the chapters (CSV / Markdown table)

---

## 🔗 Cross-links

- Syllabus & curriculum mindmap: [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/08 - Python/Subject_Plan]]
- Master Learning index: [[00 - 09 - Learning Index]]
- Master practice guide: [[../HOW_TO_USE_PRACTICE]]
- Practice GUI app vision: [[../00 - Dev_Tools/PRACTICE_GUI_APP_VISION]]
