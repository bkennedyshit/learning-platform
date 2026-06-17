---
title: "Game Development — Learning Path"
subject: "Game Dev"
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

# 🎮 Game Development — Learning Path

---

## 📋 Prerequisites

Before starting this track, you should have:

| Requirement | Where to Get It | Why |
|-------------|----------------|-----|
| Python fundamentals | [08.1 - Setup, Tooling & Project Structure](08.1---Setup,-Tooling-&-Project-Structure) through [08.3 - OOP, Data Models & Pythonic Idioms](08.3---OOP,-Data-Models-&-Pythonic-Idioms) | Prototyping, scripting, practice scripts |
| C# basics | Track 03 C# | Unity development |
| C++ basics | Track 02 C++ | Unreal Engine, performance-critical code |
| Linear algebra | [2.1](2.1) through [2.4](2.4) (math) | Transforms, physics, camera math |
| Basic 3D math | [28.1 - 3D Math Fundamentals](28.1---3D-Math-Fundamentals) | Vectors, matrices, coordinate systems |
| Data structures | [08.13 - Algorithms & Data Structures in Python](08.13---Algorithms-&-Data-Structures-in-Python) | AI, spatial partitioning, pathfinding |

**Optional but helpful:**
- Quaternions ([28.2 - Quaternions & Rotations](28.2---Quaternions-&-Rotations)) — essential for 3D chapters
- Networking fundamentals ([08.11 - Computer Networks Essentials](08.11---Computer-Networks-Essentials)) — essential for Ch. 26.6
- Architecture background (you have this) — spatial thinking transfers directly

---

## 🛤️ Recommended Chapter Order

### Phase 1: Foundations (Weeks 1–2)

| # | Chapter | Time | Key Outcome |
|---|---------|------|-------------|
| 1 | **26.1 — Game Loop & Architecture** | 8–10 hrs | Understand how engines tick, ECS vs MonoBehaviour, subsystem orchestration |
| 2 | **26.2 — Gameplay Programming** | 10–12 hrs | Implement FSMs, behavior trees, input systems, basic AI |

**Parallel work:** Start Track 06 Game Design (game feel, player psychology, MDA framework). Design thinking informs every implementation decision.

### Phase 2: Spatial Systems (Weeks 3–4)

| # | Chapter | Time | Key Outcome |
|---|---------|------|-------------|
| 3 | **26.3 — 2D Game Patterns** | 8–10 hrs | Sprites, tilemaps, 2D physics — build a Stardew-style prototype |
| 4 | **26.4 — 3D Game Patterns** | 12–15 hrs | Transforms, skeletal animation, 3D physics, raycasting |

**Parallel work:** If building a farming sim, prototype tile systems in Godot/Unity during 4.3. For VR projects, deep-dive 26.4 with [28.5 - Game Engine Architectures - Unity & Unreal](28.5---Game-Engine-Architectures---Unity-&-Unreal).

### Phase 3: Persistence & Connectivity (Weeks 5–6)

| # | Chapter | Time | Key Outcome |
|---|---------|------|-------------|
| 5 | **26.5 — Save Systems & Serialization** | 6–8 hrs | Design save architectures, handle versioning, implement slot systems |
| 6 | **26.6 — Multiplayer & Networking** | 15–20 hrs | Client-server, rollback netcode, lag compensation, snapshot interpolation |

**Note:** Chapter 26.6 is the densest chapter. Budget extra time. If your immediate project is single-player (Stardew-like), you can defer this and come back.

### Phase 4: Polish & Ship (Weeks 7–8)

| # | Chapter | Time | Key Outcome |
|---|---------|------|-------------|
| 7 | **26.7 — Performance & Optimization** | 10–12 hrs | Profiling workflows, memory optimization, GPU bottleneck identification |
| 8 | **26.8 — Building, Packaging & Distribution** | 6–8 hrs | Platform builds, CI/CD, store submission, patching |

---

## ⏱️ Total Time Estimate

| Pace | Total Hours | Calendar Time |
|------|-------------|---------------|
| Intensive (4 hrs/day) | 75–95 hrs | 4–5 weeks |
| Steady (2 hrs/day) | 75–95 hrs | 7–8 weeks |
| Weekend warrior (8 hrs/week) | 75–95 hrs | 10–12 weeks |

---

## 🔀 Alternative Orderings

### "Ship a Stardew Clone ASAP" Path
26.1 → 26.3 → 26.2 → 26.5 → 26.7 → 26.8 (skip 26.4 and 26.6 initially)

### "VR-First" Path
26.1 → 26.4 → 26.2 → 26.7 → 26.6 → 26.8 (skip 26.3, lean on Track 09)

### "Multiplayer Game Jam" Path
26.1 → 26.2 → 26.6 → 26.7 → 26.8 (networking early, polish later)

---

## 🔗 What to Do Alongside

| Track | Why | When |
|-------|-----|------|
| **Track 06 — Game Design** | Design informs implementation. MDA framework, game feel, balance | Start with Phase 1 |
| **Track 09 — VR & 3D Engineering** | Deep 3D math, shaders, engine internals | During Phase 2 (26.4) |
| **Track 01 — Python** (Ch. 1.13–1.14) | Algorithms for AI, concurrency for servers | During Phase 2–3 |
| **Math Track 04** — Classical Mechanics | Physics intuition for realistic game physics | During 4.3/4.4 |

---

## 🚀 What Comes Next

After completing this track:

| Next Step | Description |
|-----------|-------------|
| **Track 09 — VR & 3D Engineering** (advanced) | Shader programming, rendering pipeline, spatial computing |
| **Track 06 — Game Design** (advanced) | Narrative design, economy balancing, UX research |
| **Track 10 — AI & ML Systems** | ML-driven NPCs, procedural content generation |
| **Ship a game** | Apply everything. Scope small. Finish it. |

---

## 📝 Study Tips for This Track

1. **Build while you learn.** Every chapter should produce runnable code. Don't just read — implement.
2. **Use multiple engines.** Understanding patterns across Unity/Unreal/Godot makes you engine-agnostic.
3. **Profile before optimizing.** Chapter 26.7 exists for a reason — premature optimization kills projects.
4. **Scope ruthlessly.** Your architecture background means you'll want to over-engineer. Fight that instinct for game jams.
5. **Play games analytically.** When you play, ask "how did they implement this?" Reverse-engineer mechanics.

---

## Related Notes
- [26.1 - Game Loop & Architecture](26.1---Game-Loop-&-Architecture) - Same Game Dev folder
- [26.2 - Gameplay Programming - Input, State, AI](26.2---Gameplay-Programming---Input,-State,-AI) - Same Game Dev folder
- [26.3 - 2D Game Patterns - Sprites, Tilemaps, Physics](26.3---2D-Game-Patterns---Sprites,-Tilemaps,-Physics) - Same Game Dev folder
- [26.4 - 3D Game Patterns - Transforms, Animation, Physics](26.4---3D-Game-Patterns---Transforms,-Animation,-Physics) - Same Game Dev folder
- [26.5 - Save Systems & Serialization](26.5---Save-Systems-&-Serialization) - Same Game Dev folder
