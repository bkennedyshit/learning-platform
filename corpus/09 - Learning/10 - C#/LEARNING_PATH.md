---
date: 2026-05-24
title: "Track 03 — C# & Unity: Learning Path"
mission: "Sequenced progression from Python developer to shipping Unity games in C#"
status: active
tags: [csharp, unity, learning-path, game-dev, progression]
type: learning-path
track: 3
---

*Back to [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/10 - C#/Subject_Plan]] | Part of [[09 - Learning Index]]*

# Track 03 — C# & Unity: Learning Path

> *"The best way to learn a new language is to build something real in it — not to memorize syntax tables."* — Jon Skeet

---

## 📋 Prerequisites

| Requirement | Where to Get It | Status Check |
|-------------|-----------------|--------------|
| Python comfort (OOP, generators, decorators) | [[08.3 - OOP, Data Models & Pythonic Idioms]] | Can you write a `@dataclass` with custom `__eq__`? |
| Basic game dev concepts (game loop, ECS idea) | Track 04 — Game Development | Know what Update() vs FixedUpdate() means? |
| Git fundamentals | [[05-Knowledge_Foundation/cheatsheets/git_cheatsheet]] | Can you branch, merge, resolve conflicts? |

### Parallel Tracks (Run Alongside)
- **Track 09 — VR & 3D Engineering**: Engine internals, shader basics → feeds into 10.6 and 10.5
- **Track 07 — Math & Physics**: Linear algebra, physics sim → feeds into game math in Unity

---

## 🗺️ Progression Map

```
Phase 1: Language Foundation (Weeks 1–3)
├── 10.1 Setup & Toolchain ──────── Day 1–2 (environment ready)
├── 10.2 Types, Generics & LINQ ── Week 1–2 (core fluency)
└── 10.3 OOP & Design Patterns ─── Week 2–3 (architecture thinking)

Phase 2: Runtime Mastery (Weeks 4–5)
├── 10.4 Async/Await & Threading ── Week 4 (concurrency model)
└── 10.5 Memory & Performance ───── Week 5 (GC, struct, Span)

Phase 3: Unity Integration (Weeks 6–8)
├── 10.6 Unity Specifics ─────────── Week 6–7 (MonoBehaviour → ECS)
├── 10.7 Networking & Multiplayer ── Week 7–8 (Mirror/Photon/Netcode)
└── 10.8 Production Patterns ─────── Week 8 (DI, saves, Addressables)
```

---

## 📐 Phase 1: Language Foundation

### 10.1 — Setup, .NET Toolchain & Project Structure
**Goal:** Working dev environment, can create/build/run C# projects from CLI and Unity.

**Python → C# Bridge:**
- `pip` / `venv` → NuGet / .NET SDK
- `python script.py` → `dotnet run`
- `pyproject.toml` → `.csproj`

**Milestone:** Create a console app that reads JSON config, processes data with LINQ, outputs results. Then create a Unity project with proper folder structure.

---

### 10.2 — Core Language: Types, Generics & LINQ
**Goal:** Think in C#'s type system. Use generics and LINQ as naturally as Python list comprehensions.

**Python → C# Bridge:**
- `list[int]` → `List<int>` (but value-type aware)
- List comprehensions → LINQ `.Where().Select()`
- `*args, **kwargs` → `params`, overloads
- Duck typing → interfaces + generics with constraints
- `match/case` → C# pattern matching (more powerful)

**Milestone:** Implement a generic inventory system (`Inventory<T> where T : IStackable`) with LINQ queries for filtering, sorting, aggregation.

---

### 10.3 — OOP & Design Patterns
**Goal:** Apply SOLID and GoF patterns in game contexts. Know when inheritance helps vs. when composition wins.

**Python → C# Bridge:**
- `Protocol` → `interface`
- `@abstractmethod` → `abstract` keyword
- Mixins → interface default implementations (C# 8+)
- `__init_subclass__` → generic constraints + factory patterns

**Milestone:** Build a command pattern (undo/redo), observer pattern (event bus), and state machine for a 2D character controller.

---

## 📐 Phase 2: Runtime Mastery

### 10.4 — Async/Await & Threading
**Goal:** Understand C#'s Task-based async, how it differs from Python's asyncio, and why Unity's main thread constraint matters.

**Python → C# Bridge:**
- `asyncio.run()` → `Task.Run()` / `await`
- `async for` → `IAsyncEnumerable<T>`
- GIL (no true parallelism) → C# has real threads
- `concurrent.futures` → `Task.WhenAll`, `Parallel.ForEach`

**Milestone:** Implement async asset loading that doesn't freeze the UI, with cancellation token support.

---

### 10.5 — Memory Management & Performance
**Goal:** Write allocation-free hot paths. Understand GC generations, struct layout, and when to use `Span<T>`.

**Python → C# Bridge:**
- Everything is heap-allocated in Python → C# has stack (struct) vs heap (class)
- No manual memory concern → GC pressure matters for 60fps/90fps
- NumPy arrays → `Span<T>`, `Memory<T>`, native arrays

**Milestone:** Profile a particle system, eliminate GC allocations from the hot loop using object pooling and `stackalloc`.

---

## 📐 Phase 3: Unity Integration

### 10.6 — Unity Specifics
**Goal:** Master MonoBehaviour lifecycle, ScriptableObjects for data, and DOTS/ECS for performance-critical systems.

**Key Concepts:**
- Lifecycle ordering (Awake → Start → Update → LateUpdate)
- Coroutines as Unity's legacy async (yield return)
- ScriptableObjects as shared data containers
- ECS for 10,000+ entity simulations (farming game crops, particles)
- Job System + Burst for CPU-bound work

**Milestone:** Stardew-like farm with ScriptableObject crop definitions, ECS-driven growth simulation, coroutine-based day/night cycle.

---

### 10.7 — Networking & Multiplayer
**Goal:** Implement authoritative server with client prediction. Choose the right networking framework.

**Key Concepts:**
- Client prediction + server reconciliation
- RPC patterns (ServerRpc, ClientRpc)
- State synchronization vs. input replication
- Lag compensation (server-side rewind)
- Framework comparison: Mirror (free, mature) vs. Photon (cloud, easy) vs. Unity Netcode (official)

**Milestone:** 2-player co-op farming prototype with synchronized world state, client-predicted movement, and RPC-based interactions.

---

### 10.8 — Production Patterns
**Goal:** Ship-quality architecture. DI containers, save/load, asset management, testing.

**Key Concepts:**
- Dependency Injection (VContainer, Zenject)
- Binary/JSON save systems with versioning
- Addressable Asset System (async loading, memory management)
- Unit testing with NUnit + Unity Test Framework
- CI/CD with Unity Build Server / GameCI

**Milestone:** Complete save system that serializes farm state, loads Addressable asset bundles for seasonal content, with unit tests and automated builds.

---

## 🏁 Capstone Project

**Stardew-like 2D Farm Game** combining all tracks:
- ScriptableObject-driven crop/item database (10.6)
- ECS crop growth simulation (10.6)
- Async/await for scene loading (10.4)
- Object-pooled particle effects (10.5)
- 2-player co-op via Mirror or Netcode (10.7)
- Addressable seasonal content packs (10.8)
- Full save/load with cloud backup (10.8)

---

## ⏱️ Time Estimates

| Phase | Hours | Assumes |
|-------|-------|---------|
| Phase 1: Language Foundation | 25–35 | 1–2 hrs/day |
| Phase 2: Runtime Mastery | 15–20 | Builds on Phase 1 |
| Phase 3: Unity Integration | 30–40 | Hands-on projects |
| Capstone | 20–30 | Integrates everything |
| **Total** | **90–125** | ~8 weeks at 2 hrs/day |

---

## 🔗 Cross-References

- [[28.5 - Game Engine Architectures - Unity & Unreal]] — Engine lifecycle context
- [[08.4 - Concurrency - asyncio, threading, multiprocessing & the GIL]] — Python async comparison
- [[26.6 - Multiplayer & Networking]] — Game networking theory
- [[08.13 - Algorithms & Data Structures in Python]] — Data structure parallels
- [[C# Basics for Unity]] — Quick-reference cheatsheet

---

## 🔄 Maintenance
- **Created**: 2026-05-24
- **Last Updated**: 2026-05-24

---

## Related Notes
- [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/10 - C#/Subject_Plan]] - Shared game-dev/csharp focus
- [[Game Development Books and Courses]] - Shared game-dev/csharp focus
- [[10.1 - Setup, .NET Toolchain & Project Structure]] - Shared csharp/unity focus
- [[10.3 - OOP & Design Patterns]] - Shared csharp/unity focus
