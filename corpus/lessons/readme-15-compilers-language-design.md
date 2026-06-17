---
title: "README — 15 - Compilers & Language Design"
subject: "Compilers & Language Design"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: subject-readme
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# 15 - Compilers & Language Design — Subject Hub

> One-page subject hub. Lists chapters, source reading materials, **video / picture references stored outside the repo (linked by URL)**, and placeholders for generated study aids.
> Master practice guide: [HOW_TO_USE_PRACTICE](HOW_TO_USE_PRACTICE).

> **Asset storage convention.**
> - **SVG diagrams** (small, theme-responsive, in-vault) → `../_svgs/comp__<chapter>-fig<n>.svg` and embedded inline via `![comp__29.x-figN](comp__29.x-figN.svg)`.
> - **Pictures, screenshots, videos, course recordings** are NOT committed to this repo. They live on YouTube, official docs, GitHub, or in your local "C:/Obsidian Vault/Bill's Vault/_assets/" sidecar (gitignored). Reference them by **URL** in this README and chapter notes.

---

## 🚀 Quick start

```bash
# Install Python tools for exploring compiler concepts
pip install lark-parser astpretty asttokens mypy

# Explore CPython bytecode on any expression:
python3 -c "import dis; dis.dis(lambda x, y: x + y * 2)"

# Inspect the AST of a Python file:
python3 -c "import ast, astpretty; astpretty.pprint(ast.parse('x = 3 + y * 2'))"

# Emit LLVM IR for a C function (requires clang):
echo 'int add(int x, int y) { return x + y; }' | clang -O2 -emit-llvm -S -x c - -o -
```

---

## 📜 Chapter index

- [15.1 - Lexers & Tokenization](15.1---Lexers-&-Tokenization)
- [15.2 - Parsers & Grammars](15.2---Parsers-&-Grammars)
- [15.3 - Abstract Syntax Trees & Semantic Analysis](15.3---Abstract-Syntax-Trees-&-Semantic-Analysis)
- [15.4 - Type Systems & Type Checking](15.4---Type-Systems-&-Type-Checking)
- [15.5 - Intermediate Representations & IR Design](15.5---Intermediate-Representations-&-IR-Design)
- [15.6 - Code Generation & Backends](15.6---Code-Generation-&-Backends)
- [15.7 - Optimization Passes](15.7---Optimization-Passes)
- [15.8 - Virtual Machines, Bytecode & JIT](15.8---Virtual-Machines,-Bytecode-&-JIT)

---

## 🎬 Video & Picture References (external — open in browser)

> These are the open-source / pro-grade media that supplement the chapter notes. Pictures and videos are **not** stored in this repo; they live on YouTube, official docs, GitHub, etc.

### 📺 Video Channels & Playlists

| Channel / Course | Track Use | Link |
|---|---|---|
| **Stanford CS143 — Compilers (Coursera)** | Full formal compiler course, lecture videos | [online.stanford.edu/courses/cs143-compilers](https://online.stanford.edu/courses/cs143-compilers) |
| **LLVM Kaleidoscope Tutorial** | Build a JIT compiler from scratch with LLVM | [llvm.org/docs/tutorial](https://llvm.org/docs/tutorial/) |
| **Cornell CS 6120 — Advanced Compilers** | Open lectures: SSA, dataflow, optimization | [cs.cornell.edu/courses/cs6120](https://www.cs.cornell.edu/courses/cs6120/2020fa/) |
| **Matt Godbolt — What Has My Compiler Done for Me Lately?** | x86-64 code generation, Compiler Explorer | [youtube.com/watch?v=bSkpMdDe4g4](https://www.youtube.com/watch?v=bSkpMdDe4g4) |
| **Robert Nystrom — Crafting Interpreters (audiobook/walkthrough)** | Visual walkthroughs of Crafting Interpreters | [craftinginterpreters.com](https://craftinginterpreters.com/) |
| **Compiler Explorer (godbolt.org)** | Live: see assembly output for any language | [godbolt.org](https://godbolt.org/) |
| **V8 blog (v8.dev)** | JIT tiers, TurboFan, Maglev, Sparkplug | [v8.dev/blog](https://v8.dev/blog) |
| **Tsoding — Writing a Compiler** | Practical compiler implementation streams | [@TsodingDaily](https://www.youtube.com/@TsodingDaily) |
| **Low Level Learning** | x86-64 assembly, calling conventions | [@LowLevelLearning](https://www.youtube.com/@LowLevelLearning) |
| **Andreas Kling — SerenityOS compiler work** | Real compiler engineering, Jakt language | [@awesomekling](https://www.youtube.com/@awesomekling) |

### 🖼️ Picture / Diagram Reference Sources

| Source | What it gives you | Link |
|---|---|---|
| **Crafting Interpreters diagrams** | AST, VM, bytecode visualisations | [craftinginterpreters.com](https://craftinginterpreters.com/) |
| **LLVM project documentation** | IR diagrams, pass pipeline | [llvm.org/docs](https://llvm.org/docs/) |
| **Wikipedia — Compiler pipeline** | Classic stages diagram | [en.wikipedia.org/wiki/Compiler](https://en.wikipedia.org/wiki/Compiler) |
| **tree-sitter playground** | Interactive parse tree visualiser | [tree-sitter.github.io/tree-sitter/playground](https://tree-sitter.github.io/tree-sitter/playground) |
| **AST Explorer (astexplorer.net)** | Live AST for JS/TS/Python/Go/CSS | [astexplorer.net](https://astexplorer.net/) |
| **Compiler Explorer (godbolt.org)** | Source → assembly with highlighting | [godbolt.org](https://godbolt.org/) |
| **Python dis module docs** | CPython bytecode reference | [docs.python.org/3/library/dis.html](https://docs.python.org/3/library/dis.html) |

### 📚 Open-Source / Free Books

| Title | Author / Provider | Link |
|---|---|---|
| Crafting Interpreters (full text, CC BY-NC-ND) | Robert Nystrom | [craftinginterpreters.com](https://craftinginterpreters.com/) |
| Write You a Haskell (CC BY) | Stephen Diehl | [dev.stephendiehl.com/fun/](http://dev.stephendiehl.com/fun/) |
| An Incremental Approach to Compiler Construction | Abdulaziz Ghuloum | [scheme2006.cs.uchicago.edu/11-ghuloum.pdf](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf) |
| LLVM Language Reference Manual | LLVM project | [llvm.org/docs/LangRef.html](https://llvm.org/docs/LangRef.html) |
| LLVM Kaleidoscope Tutorial | LLVM project | [llvm.org/docs/tutorial](https://llvm.org/docs/tutorial/) |
| Bril — Teaching IR | Cornell / Adrian Sampson | [capra.cs.cornell.edu/bril](https://capra.cs.cornell.edu/bril/) |
| CS 6120 (Cornell) lecture notes | Adrian Sampson | [cs.cornell.edu/courses/cs6120](https://www.cs.cornell.edu/courses/cs6120/2020fa/) |

---

## 🔭 2026 Industry Snapshot

> Sources rephrased for compliance — never more than 30 consecutive words from any single source.

| Area | 2026 Reality | Primary sources |
|---|---|---|
| Python JIT | CPython 3.13 ships an experimental copy-and-patch JIT (PEP 744); the specializing adaptive interpreter (CEVAL) from 3.11 is now mature and rewrites hot instructions in-place. | [peps.python.org/pep-0744](https://peps.python.org/pep-0744/), [peps.python.org/pep-0659](https://peps.python.org/pep-0659/) |
| TypeScript type system | TS 5.x has improved control-flow narrowing, isolated declarations for parallel builds, and ongoing work toward sound structural typing in strict mode. | [devblogs.microsoft.com/typescript](https://devblogs.microsoft.com/typescript/) |
| LLVM / MLIR | MLIR (Multi-Level IR) is the 2025–2026 architectural direction: reusable IR dialects for ML (MHLO/TOSA), hardware (LLHD), and WebAssembly (Wasm dialect). | [mlir.llvm.org](https://mlir.llvm.org/) |
| Rust compiler | Polonius borrow checker (Datalog-based, fixes NLL false-positives) is rolling out. MIR optimizations expanding. Cranelift backend available for fast debug builds. | [blog.rust-lang.org](https://blog.rust-lang.org/2024/06/26/polonius-update.html) |
| WebAssembly | Wasm 2.0 adds GC types, tail calls, multi-memory. WASI + component model targeting edge and AI inference. | [webassembly.org/roadmap](https://webassembly.org/roadmap/) |
| Tree-sitter / tooling | Dominant approach for language-aware editor / AI tooling. Used by Neovim, GitHub, Helix, Cursor. Incremental, error-tolerant, query-based. | [tree-sitter.github.io](https://tree-sitter.github.io/) |
| V8 JIT tiers | Sparkplug (baseline, fast compile, no opt) → Maglev (mid-tier, SSA-based) → TurboFan (optimizing, sea-of-nodes IR) is the stable 2024+ pipeline. | [v8.dev/blog](https://v8.dev/blog) |

---

## 🧰 Generated study aids

### 🎙️ Audio overviews & podcasts (NotebookLM)
- [ ] TODO: paste the NotebookLM "Audio Overview" link

### 🧠 Mind maps
- [ ] TODO: NotebookLM mind-map URL or screenshot

### ❓ Quizzes
- [ ] TODO: NotebookLM-generated quiz (NFA/DFA, HM inference, LLVM IR, calling conventions)

### 📊 Reports & summaries
- [ ] TODO: NotebookLM "Briefing Doc" or "Study Guide"

### 🃏 Flash cards
- [ ] TODO: deck export (Thompson construction steps; HM rules; x86-64 argument registers; GC strategies; JIT tiers)

### 🎬 Video overviews
- [ ] TODO: Loom / personal recording walking the full compiler pipeline

### 📋 Data tables
- [ ] TODO: comparison matrices (LL vs LR vs Pratt; stack VM vs register VM; GC strategies; JIT compilation tiers)

---

## 🔗 Cross-links

- Syllabus & curriculum mindmap: [Subject_Plan](Subject_Plan)
- Visual roadmap: [LEARNING_PATH](LEARNING_PATH)
- Python internals: [1.4 - Concurrency - asyncio, threading, multiprocessing & the GIL](1.4---Concurrency---asyncio,-threading,-multiprocessing-&-the-GIL)
- C++ templates & codegen: [Subject_Plan](Subject_Plan)
- Rust borrow checker: [Subject_Plan](Subject_Plan)
- TypeScript type system: [Subject_Plan](Subject_Plan)
- AI/ML code-analysis tooling: [Subject_Plan](Subject_Plan)
- Game Dev scripting VMs: [Subject_Plan](Subject_Plan)
- System Design (IR design ≈ API design): [Subject_Plan](Subject_Plan)
- Master Learning index: [00 - 09 - Learning Index](00---09---Learning-Index)
- Master practice guide: [HOW_TO_USE_PRACTICE](HOW_TO_USE_PRACTICE)
