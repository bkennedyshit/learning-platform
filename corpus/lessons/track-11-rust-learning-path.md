---
title: "Track 11 — Rust: Learning Path"
subject: "Rust"
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

# 🦀 Track 11 — Rust: Learning Path

---

## 📋 Prerequisites

| Requirement | Where to Get It | Why |
|-------------|----------------|-----|
| Python comfort (functions, classes, iterators) | [08.1 - Setup, Tooling & Project Structure](08.1---Setup,-Tooling-&-Project-Structure) through [08.3 - OOP, Data Models & Pythonic Idioms](08.3---OOP,-Data-Models-&-Pythonic-Idioms) | Rust's iterators and trait system map to Python's protocols |
| Skim C++ memory model | [C++ Pointers & Memory Management](C++-Pointers-&-Memory-Management) | Stack vs heap, pointers, RAII — Rust formalizes what C++ leaves implicit |
| Basic terminal/CLI fluency | [08.7 - Shell, Terminal & Cross-Platform CLI](08.7---Shell,-Terminal-&-Cross-Platform-CLI) | Cargo is CLI-first |

**You do NOT need**: C/C++ mastery, prior systems programming, or assembly knowledge.

---

## 🗺️ Progression Map

### Phase 1: Foundation (Weeks 1–4)

```
┌─────────────────────────────────────────────────────────────┐
│  WEEK 1–2: The Mental Shift                                  │
│                                                              │
│  11.1 Setup, Cargo & Project Structure                       │
│  ├── Install rustup, configure rust-analyzer                 │
│  ├── Cargo new/build/run/test/clippy                         │
│  ├── Workspace layout for multi-crate projects               │
│  └── 🏋️ Rustlings: variables, functions, primitive_types     │
│                                                              │
│  11.2 Ownership, Borrowing & Lifetimes                       │
│  ├── Move semantics (Python's rebinding on steroids)         │
│  ├── Borrowing rules: &T vs &mut T                           │
│  ├── Lifetime annotations and elision                        │
│  └── 🏋️ Rustlings: move_semantics, borrowing                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  WEEK 3–4: The Type System                                   │
│                                                              │
│  11.3 Type System — Enums, Traits & Generics                 │
│  ├── Algebraic data types (enum = tagged union)              │
│  ├── Pattern matching (match, if let, while let)             │
│  ├── Traits as interfaces + default impls                    │
│  ├── Generics + monomorphization                             │
│  └── 🏋️ Rustlings: enums, traits, generics                  │
│                                                              │
│  11.4 Error Handling — Result, Option, ? Operator            │
│  ├── No exceptions: Result<T, E> and Option<T>              │
│  ├── The ? operator (early return on error)                  │
│  ├── Custom error types with thiserror                       │
│  └── 🏋️ Rustlings: errors, options                          │
└─────────────────────────────────────────────────────────────┘
```

### Phase 2: Power (Weeks 5–8)

```
┌─────────────────────────────────────────────────────────────┐
│  WEEK 5–6: Concurrency                                       │
│                                                              │
│  11.5 Concurrency — Threads, Send/Sync, async/await & Tokio  │
│  ├── std::thread::spawn + move closures                      │
│  ├── Send/Sync marker traits (compile-time race prevention)  │
│  ├── async/await with Tokio                                  │
│  ├── Channels: mpsc, crossbeam, tokio::sync                  │
│  └── 🏋️ Build: concurrent web scraper                       │
│                                                              │
│  WEEK 7–8: Memory & Smart Pointers                           │
│                                                              │
│  11.6 Memory — Box, Rc, Arc, RefCell, Mutex                  │
│  ├── Box<T>: heap allocation + recursive types               │
│  ├── Rc<T>/Arc<T>: shared ownership                          │
│  ├── RefCell<T>/Mutex<T>: interior mutability                │
│  ├── When to use which (decision tree)                       │
│  └── 🏋️ Build: thread-safe cache with Arc<Mutex<HashMap>>   │
└─────────────────────────────────────────────────────────────┘
```

### Phase 3: Mastery (Weeks 9–12)

```
┌─────────────────────────────────────────────────────────────┐
│  WEEK 9–10: Idiomatic Rust                                   │
│                                                              │
│  11.7 Idiomatic Rust — Patterns, Anti-patterns & Performance │
│  ├── Newtype, Builder, Typestate patterns                    │
│  ├── From/Into, TryFrom/TryInto conversions                  │
│  ├── Iterator combinators (map, filter, fold, collect)       │
│  ├── "Parse, don't validate" philosophy                      │
│  ├── Zero-cost abstractions: benchmarking proof              │
│  └── 🏋️ Build: CLI tool with clap + serde                   │
│                                                              │
│  WEEK 11–12: Production Targets                              │
│                                                              │
│  11.8 Production Rust — WASM, FFI, Embedded & Bevy           │
│  ├── WebAssembly with wasm-pack + wasm-bindgen               │
│  ├── FFI: calling C from Rust, exposing Rust to Python       │
│  ├── Embedded: no_std + embedded-hal                         │
│  ├── Game dev: Bevy ECS architecture                         │
│  └── 🏋️ Build: Bevy game prototype OR WASM module           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Milestone Checkpoints

| Week | Milestone | Proof of Competence |
|------|-----------|-------------------|
| 2 | "I get ownership" | Can explain why `let s2 = s1; println!("{s1}");` fails |
| 4 | "I think in types" | Can model a domain with enums + traits, no `unwrap()` in sight |
| 6 | "Fearless concurrency" | Multi-threaded program compiles on first try |
| 8 | "I know my pointers" | Can choose between Rc/Arc/Box/RefCell without googling |
| 10 | "Idiomatic" | Code passes `clippy` with zero warnings, uses iterator chains |
| 12 | "Production" | Shipped a WASM module or Bevy prototype |

---

## 🔄 Daily Practice Rhythm

```
┌────────────────────────────────────────────┐
│  2-Hour Daily Block                         │
│                                             │
│  0:00–0:20  Rustlings exercises (warm-up)   │
│  0:20–1:00  Chapter study + code-along      │
│  1:00–1:40  Build project (apply concepts)  │
│  1:40–2:00  Review compiler errors (learn)  │
└────────────────────────────────────────────┘
```

**The compiler is your teacher.** Rust's error messages are the best in any language. Read them carefully — they often contain the fix.

---

## 🔗 Companion Tracks

| Track | Synergy |
|-------|---------|
| [26 - Game Dev](26---Game-Dev) | Bevy game dev (Chapter 11.8) |
| [09 - C++](09---C++) | Memory model context (prerequisite) |
| [08.4 - Concurrency - asyncio, threading, multiprocessing & the GIL](08.4---Concurrency---asyncio,-threading,-multiprocessing-&-the-GIL) | Python GIL contrast (Chapter 11.5) |
| [23 - AI & Machine Learning Systems](23---AI-&-Machine-Learning-Systems) | LLM inference engines in Rust |
| [08.12 - Computer Architecture - Performance Intuition](08.12---Computer-Architecture---Performance-Intuition) | Cache-friendly data layout (Chapter 11.6) |

---

## Related Notes
- [11.1 - Setup, Cargo & Project Structure](11.1---Setup,-Cargo-&-Project-Structure) - Same Rust folder
- [11.2 - Ownership, Borrowing & Lifetimes](11.2---Ownership,-Borrowing-&-Lifetimes) - Same Rust folder
- [11.3 - Type System - Enums, Traits & Generics](11.3---Type-System---Enums,-Traits-&-Generics) - Same Rust folder
- [11.4 - Error Handling - Result, Option & the Question-Mark Operator](11.4---Error-Handling---Result,-Option-&-the-Question-Mark-Operator) - Same Rust folder
- [11.5 - Concurrency - Threads, Send_Sync, async_await & Tokio](11.5---Concurrency---Threads,-Send_Sync,-async_await-&-Tokio) - Same Rust folder
