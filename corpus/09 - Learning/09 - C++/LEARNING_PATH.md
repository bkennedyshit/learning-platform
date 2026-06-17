---
date: 2026-05-24
title: "Track 02 — C++ Learning Path"
mission: "Hand-curated progression from Python programmer to proficient modern C++ developer targeting game engines and systems programming"
status: active
tags: [cpp, learning-path, progression, prerequisites, game-dev]
type: learning-path
track: 2
---

*Back to [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/09 - C++/Subject_Plan]] | [[09 - Learning Index]]*

# 🛤️ Track 02 — C++ Learning Path

> *"The first thing I'd do is make sure I was really comfortable with the basics before moving on. You can't build a skyscraper on a weak foundation."* — John Carmack

---

## 📋 Prerequisites

Before starting this track, you should have:

| Requirement | Where to Get It | Status |
|-------------|----------------|--------|
| Python fluency (variables, functions, OOP, modules) | [[Track 01 Python]] — Chapters 1.1–1.3 | ✅ |
| Basic understanding of how computers execute code | [[1.12 - Computer Architecture & How Code Becomes Execution]] | ✅ |
| Comfort with a terminal/command line | Daily usage | ✅ |
| Any text editor or IDE (VS Code recommended) | Already installed | ✅ |

**Not required but helpful:**
- Prior exposure to any compiled language (Java, C#, Rust)
- Basic understanding of hexadecimal and binary

---

## 🗺️ The Path

### Phase 1: Foundation (Weeks 1–4)

```
┌─────────────────────────────────────────────────────────┐
│  09.1 Setup & Toolchain                                  │
│  ├── Install compiler (MSVC/Clang/GCC)                  │
│  ├── Configure CMake + Ninja                            │
│  ├── Set up clangd in VS Code                           │
│  └── First "Hello, World" → compile → run → debug       │
│                         ↓                                │
│  09.2 Core Language                                      │
│  ├── Type system (int, float, auto, const)              │
│  ├── Pointers & references (the big mental shift)       │
│  ├── Stack vs heap memory                               │
│  └── Value categories (lvalue, rvalue, xvalue)          │
│                         ↓                                │
│  09.3 OOP & Templates                                    │
│  ├── Classes, constructors, destructors                 │
│  ├── RAII (the #1 C++ idiom)                            │
│  ├── Inheritance & virtual dispatch                     │
│  └── Templates (generics on steroids)                   │
└─────────────────────────────────────────────────────────┘
```

**Milestone:** You can write a multi-file C++ project with classes, templates, and proper resource management. You understand why `new`/`delete` are almost never used in modern C++.

---

### Phase 2: Modern Idioms (Weeks 5–8)

```
┌─────────────────────────────────────────────────────────┐
│  09.4 Modern C++ (Smart Pointers, Move, Lambdas)         │
│  ├── unique_ptr, shared_ptr, weak_ptr                   │
│  ├── Move semantics & perfect forwarding                │
│  ├── Lambdas & std::function                            │
│  └── Concepts & constraints (C++20)                     │
│                         ↓                                │
│  09.5 STL Deep Dive                                      │
│  ├── Containers (vector, map, unordered_map, array)     │
│  ├── Algorithms (sort, transform, accumulate)           │
│  ├── Iterators & iterator categories                    │
│  └── Ranges & views (C++20/23)                          │
└─────────────────────────────────────────────────────────┘
```

**Milestone:** You write idiomatic modern C++ — no raw `new`/`delete`, heavy use of STL algorithms, range-based pipelines, and expressive lambdas.

---

### Phase 3: Systems & Performance (Weeks 9–12)

```
┌─────────────────────────────────────────────────────────┐
│  09.6 Concurrency                                        │
│  ├── std::thread, std::jthread                          │
│  ├── Mutexes, atomics, memory ordering                  │
│  ├── std::async & futures                               │
│  └── Coroutines (co_await, co_yield)                    │
│                         ↓                                │
│  09.7 Performance                                        │
│  ├── Cache lines & memory layout                        │
│  ├── SIMD intrinsics                                    │
│  ├── SoA vs AoS                                        │
│  └── Profiling & benchmarking                           │
│                         ↓                                │
│  09.8 Game Dev with C++                                  │
│  ├── Unreal Engine C++ (UObject, UPROPERTY, etc.)       │
│  ├── Blueprint/C++ interop                              │
│  ├── Entity Component Systems                           │
│  └── Data-Oriented Design                               │
└─────────────────────────────────────────────────────────┘
```

**Milestone:** You can write performant, concurrent C++ and understand Unreal Engine's C++ patterns well enough to build gameplay systems.

---

## 🔀 Parallel Reading Recommendations

These tracks complement your C++ learning and should be read alongside:

| Track | Why | When |
|-------|-----|------|
| [[Track 09 VR & 3D Engineering]] | Engine architecture context, rendering pipelines | During Phase 2–3 |
| [[Track 04 Game_Dev]] | Game design patterns, ECS architecture | During Phase 3 |
| [[08.4 - Concurrency - asyncio, threading, multiprocessing & the GIL]] | Compare Python's concurrency model to C++ | During Ch 09.6 |
| [[1.12 - Computer Architecture & How Code Becomes Execution]] | CPU caches, pipelines, branch prediction | During Ch 09.7 |
| [[28.5 - Game Engine Architectures - Unity & Unreal]] | High-level engine design | During Ch 09.8 |

---

## 🧠 Python → C++ Mental Model Bridges

Key conceptual translations for a Python developer:

| Python Concept | C++ Equivalent | Key Difference |
|---------------|---------------|----------------|
| `x = 42` | `int x = 42;` | C++ variables have fixed types at compile time |
| Everything is a reference | Values by default | C++ copies by default; you opt-in to references |
| `del x` / garbage collection | RAII / destructors | C++ objects clean up deterministically at scope exit |
| `list` | `std::vector` | Same concept, but you choose element type at compile time |
| `dict` | `std::unordered_map` | Hash map, but keys/values are typed |
| `class Foo:` | `class Foo { };` | C++ has access control, no GIL, manual memory layout |
| `async/await` | `co_await` (C++20) | Similar syntax, very different runtime model |
| Duck typing | Templates / Concepts | Compile-time duck typing (zero runtime cost) |
| `pip install` | vcpkg/Conan + CMake | More setup, but same idea |

---

## ✅ Completion Criteria

You've completed this track when you can:

1. [ ] Set up a CMake project from scratch with dependencies via vcpkg
2. [ ] Write RAII classes with proper rule-of-five (or rule-of-zero)
3. [ ] Use smart pointers exclusively (no raw new/delete in application code)
4. [ ] Write generic code with templates and concepts
5. [ ] Use STL algorithms and ranges fluently
6. [ ] Write correct concurrent code with atomics and mutexes
7. [ ] Profile and optimize hot loops (cache-aware, SIMD where appropriate)
8. [ ] Create an Unreal Engine C++ class that interacts with Blueprints
9. [ ] Explain the difference between `std::move`, `std::forward`, and copying
10. [ ] Read and understand CppCon talks without pausing every 30 seconds

---

## 📎 Quick Reference Appendices

For rapid syntax lookup during exercises, use the existing cheatsheets:
- [[C++ Pointers & Memory Management]] — Raw pointer mechanics refresher
- [[C++ Basics for Game Dev]] — Condensed game-dev C++ syntax

---

*Last updated: 2026-05-24*

---

## Related Notes
- [[09.8 - Game Dev with C++ - Unreal Engine & Custom Engine Patterns]] - Shared game-dev/cpp focus
- [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/09 - C++/Subject_Plan]] - Shared game-dev/cpp focus
- [[09.1 - Setup, Build Systems & Toolchain]] - Same C++ folder
