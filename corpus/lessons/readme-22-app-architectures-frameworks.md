---
title: "README — 22 - App Architectures & Frameworks"
subject: "App Architectures & Frameworks"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: subject-readme
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# 22 - App Architectures & Frameworks — Subject Hub

> One-page subject hub. Lists chapters, drill commands, source reading
> materials, and placeholders for generated study aids (NotebookLM artifacts:
> audio overviews, mind maps, quizzes, flash cards, etc.).
> Master practice guide: [HOW_TO_USE_PRACTICE](HOW_TO_USE_PRACTICE).

---

## 🚀 Quick start

From a terminal in this folder:

```bash
cd "C:/Obsidian Vault/Bill's Vault/05-Knowledge_Foundation/09 - Learning/22 - App Architectures & Frameworks"
python "_practice/scripts/<chapter>_<topic>.py" --count 8 --seed 42
```

Output lands at `_practice/<chapter>_drills.md`. Open in Obsidian Reading
view, do the problems on paper, click **Show solution** to verify.

---

## 📜 Chapter index

- [22.1 - React & Next.js - Functional Components & Hooks](22.1---React-&-Next.js---Functional-Components-&-Hooks)
- [22.2 - Angular - Class-based Architecture & RxJS](22.2---Angular---Class-based-Architecture-&-RxJS)
- [22.3 - Vite & Modern Build Tools](22.3---Vite-&-Modern-Build-Tools)
- [22.4 - PyQt6 & PySide6 - Signals, Slots & Event Loops](22.4---PyQt6-&-PySide6---Signals,-Slots-&-Event-Loops)
- [22.5 - Flutter & Dart - Widget Tree, Isolates & Custom Painters](22.5---Flutter-&-Dart---Widget-Tree,-Isolates-&-Custom-Painters)

---

## 🎯 Drill scripts

| Script | Chapter | Sample command |
|---|---|---|
| _(no drill scripts in this subject yet)_ | — | — |

---

## 📚 Source materials & references

_Pulled verbatim from `Subject_Plan.md §2 — Architectural Deep Dives`. Source of truth is the Subject_Plan; this section is a convenience copy._

### A. React & Next.js
*   **Mental Model:** UI as a pure function of state. $UI = f(state)$
*   **Key Literacies:**
    *   Virtual DOM reconciliation.
    *   Hook lifecycles (`useEffect` dependencies, `useMemo` optimizations).
    *   Server-Side Rendering (SSR) vs. Static Site Generation (SSG) in Next.js.
*   **Textbook Documentation:** Every React note must map out the component tree and data flow (Props vs. Context vs. Redux/Zustand).

### B. Angular
*   **Mental Model:** Heavyweight, opinionated MVC framework.
*   **Key Literacies:**
    *   Two-way data binding and Zones (`zone.js`).
    *   Dependency Injection (DI) hierarchy.
    *   Reactive programming via RxJS (Observables, Subjects).

### C. Desktop GUIs (PyQt)
*   **Mental Model:** Event-driven event loops with rigid widget hierarchies.
*   **Key Literacies:**
    *   The Qt Main Event Loop (`QApplication.exec_()`).
    *   Signals and Slots (Publish/Subscribe pattern for UI events).
    *   Thread management (Using `QThread` so the UI doesn't freeze).

### D. Advanced Flutter & Dart (Top 5% Level)
*   **Mental Model:** Everything is a Widget. Skia/Impeller rendering engine.
*   **Key Literacies:**
    *   RenderObject vs. Element vs. Widget tree.
    *   Isolates for heavy background processing (Dart concurrency).
    *   Advanced Custom Painters and Shaders.
    *   State Management Architecture (Riverpod vs BLoC).

---

---

## 🧰 Generated study aids

> **Status:** placeholder. Drop links to NotebookLM-generated artifacts here as
> you create them. Each subsection currently has a single TODO bullet — replace
> or append `[wikilinks](wikilinks)` and external URLs once the artifact exists.

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

- Syllabus & curriculum mindmap: [Subject_Plan](Subject_Plan)
- Master Learning index: [00 - 09 - Learning Index](00---09---Learning-Index)
- Master practice guide: [HOW_TO_USE_PRACTICE](HOW_TO_USE_PRACTICE)
- Practice GUI app vision: [PRACTICE_GUI_APP_VISION](PRACTICE_GUI_APP_VISION)
