---
title: "09 - Learning Master Index"
subject: "Learning"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: master-index
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# 09 — Learning Master Index

> *Navigation hub for the entire Learning curriculum. Pure mathematics through theoretical physics, software architecture, spatial computing, AI/ML, neuroscience, behavioral psychology, biomechanics + HCI, programming languages, the natural sciences, and the **2026 spatial-computing arc** (3D modelling → electronics → robotics → holographics → applied VR).*

This is the canonical entry point. Every track below is its own self-contained sub-curriculum: a `Subject_Plan.md` (syllabus, mindmap, free learning catalog) plus an ordered set of textbook-grade chapter notes (Pearson/Ambrose-style: definitions → axioms → theorems → exhaustive proofs → SVG diagrams → worked examples → cross-links) plus `_practice/scripts/` SymPy / NumPy / PyTorch generators or `_examples/` annotated-code reference notes.

All chapters follow the rules in `[AGENT_MANUAL](AGENT_MANUAL)`:
- **Pearson/Ambrose Textbook Directive** — definitions, axioms, lemmas, theorems, exhaustive proofs.
- **Anti-Triviality Rule** — every algebraic, calculus, tensor-index, gradient, and code step is shown.
- **Obsidian-Safe LaTeX** — `$$` blocks padded with blank lines; `<details>` solutions with proper spacing.
- **Inline Theme-Responsive SVG** — diagrams are inline `<svg>` (never code-fenced) and use Obsidian CSS variables so they render correctly in both dark and light themes.

---

## 🗺️ Curriculum Topology

```mermaid
graph TD
    M["07 Math & Physics<br/>(12 sub-subjects, 94 chapters)"]
    M --> S["08 App Architectures<br/>(5 ch — code literacy)"]
    M --> V["09 VR & 3D Engineering<br/>(7 ch — quaternions, shaders, engines)"]
    M --> A["10 AI & ML Systems<br/>(7 ch — backprop, transformers, RLHF)"]
    M --> N["11 Neuroscience & Cognition<br/>(7 ch — bio neurons + AI parallels)"]
    M --> P["12 Behavioral Psych & RL<br/>(6 ch — Bellman, dopamine, RLHF)"]
    M --> B["13 Biomechanics & HCI<br/>(7 ch — physics + bio + sensors)"]
    A --> P
    A --> N
    N --> P
    B --> N
    B --> V

    %% 2026 spatial-computing arc (Tracks 20–24)
    V --> M3D["20 3D Modelling<br/>(8 ch — Revit · Fusion · Maya · Blender · SolidWorks)"]
    M --> EL["21 Electronics<br/>(8 ch — circuits → MCUs → motherboards)"]
    EL --> RO["22 Robotics<br/>(8 ch — kinematics · ROS 2 · SLAM · humanoids)"]
    A --> RO
    M --> HO["23 Holographics<br/>(8 ch — wave optics · CGH · light fields)"]
    V --> HO
    M3D --> VR24["24 VR Applied<br/>(8 ch — OpenXR · MR · arch-viz · business)"]
    V --> VR24
    HO --> VR24

    %% Production-engineering arc (Tracks 25–28) — fills the BUILDING_AT_SCALE gaps
    S --> SEC["25 Cybersecurity<br/>(8 ch — OWASP · WebAuthn · SLSA · LLM sec)"]
    A --> SEC
    S --> DEV["26 DevOps & SRE<br/>(8 ch — CI/CD · IaC · k8s · SLOs · FinOps)"]
    S --> SYS["27 System Design<br/>(8 ch — caching · DBs · queues · APIs · capacity)"]
    SYS --> DEV
    DEV --> CLD["28 Cloud Platforms<br/>(8 ch — AWS · GCP · Azure · Cloudflare · indie stack)"]
    SYS --> CLD
    SEC --> CLD
    RO --> SEC
    VR24 --> SYS

    %% Deep infrastructure arc (Tracks 29–33)
    CPP["02 C++"] --> COMP["29 Compilers<br/>(8 ch — lexers · AST · IR · JIT)"]
    RUST["14 Rust"] --> COMP
    SQL["07 SQL"] --> DBS["30 DB Internals<br/>(8 ch — B-trees · LSM · WAL · MVCC)"]
    COMP --> DBS
    DBS --> NET["31 Networking<br/>(8 ch — TCP · TLS · QUIC · gRPC)"]
    NET --> DSP["32 Signal Processing<br/>(8 ch — FFT · filters · audio AI)"]
    DSP --> AI_EXP["05 AI Experiments"]
    BIZ["33 Business<br/>(8 ch — GTM · fundraising · sales)"] --> Platform["02 Business_Platform"]

    %% Maybe-tier arc (Tracks 34–36)
    MECH["34 Mech Eng<br/>(8 ch — CNC · 3D print · GD&T)"] --> RO
    MUSIC["35 Music Production<br/>(8 ch — synthesis · JUCE · AI audio)"] --> DSP
    PHIL["36 Philosophy of Mind<br/>(8 ch — consciousness · qualia · AI sentience)"] --> N
```

The vertical chain follows the canonical "tower of capability" — pure math (07) underwrites every applied track. AI/ML (10) sits at the cross-roads between graphics (09), neuroscience (11), psych/RL (12), and biomechanics (13). Tracks deliberately cross-link: Track 11 ↔ 12 share the dopamine / RPE topic; Track 12 ↔ 13 share Polyvagal HRV; Track 09 ↔ 13 share rotational dynamics.

The **2026 spatial-computing arc (Tracks 20–24)** is built specifically to compound an architecture-trained learner's existing Revit / 3D skills into electronics → robotics → holographics → applied / business VR. It deliberately reuses Track 09 (math + rendering) as foundation rather than duplicating it.

The **production-engineering arc (Tracks 25–28)** fills the gaps called out in [BUILDING_AT_SCALE.md](BUILDING_AT_SCALE): cybersecurity (the part AI ghost-writes worst), DevOps/SRE (how to actually run anything in production), system design (the failure-domain decomposition vocabulary), and cloud platforms (the actual buttons). Together they turn the rest of the curriculum into something you can ship.

---

## 🎓 Status Legend

> **Status legend:** ✅ Complete — chapters at 30+ KB textbook depth · 🟢 Near-complete — all chapters at or near 30 KB · 🟡 Draft — full structure (frontmatter, SVGs, all sections, cross-links) in place but content depth pending expansion · ⏳ Planned — only Subject_Plan.md skeleton exists

---

## 📐 Track 01 — Mathematical Foundations & Theoretical Physics

> 12 sub-subjects, 94 chapters, 3.83 MB of content. The tower of physics — from limits and continuity through Einstein field equations to Schwarzschild black holes.

[→ open the full Math & Physics index](01---Math-and-Physics-Index)

| # | Subject | Status |
|---|---|---|
| 01 | [Mathematical Foundations & Calculus]() | ✅ Complete (8 chapters) |
| 02 | [Linear Algebra & Matrix Theory]() | ✅ Complete (8 chapters) |
| 03 | [Ordinary & Partial Differential Equations]() | ✅ Complete (8 chapters) |
| 04 | [Classical Mechanics & Dynamical Systems]() | ✅ Complete (8 chapters) |
| 05 | [Thermodynamics & Statistical Mechanics]() | ✅ Complete (8 chapters) |
| 06 | [Fluid Dynamics & Continuum Mechanics]() | ✅ Complete (8 chapters) |
| 07 | [Electrodynamics & Classical Field Theory]() | ✅ Complete (8 chapters) |
| 08 | [Special & General Relativity]() | ✅ Complete (8 chapters) |
| 09 | [Quantum Mechanics & Quantum Field Theory]() | ✅ Complete (8 chapters) |
| 10 | [Aerospace Engineering & Orbital Mechanics]() | ✅ Complete (7 chapters) |
| 11 | [Control Theory & Systems Engineering]() | ✅ Complete (8 chapters) |
| 12 | [Solid Mechanics & Materials Science]() | ✅ Complete (7 chapters) |

---

## 🐍 Track 08 — Python Comprehensive (NEW)

> 16 chapters, ~189 KB. Python language proper plus the developer-environment foundation (shell, Git, Docker, OS, networks) and CS topics (architecture, algorithms, concurrency, GPU/CUDA, distributed systems) that the LLM-building mission requires. Built on top of the existing cheatsheets in `00_Basics/`, `01_Control Flow/`, etc., which remain as quick-reference appendices.

[→ open the syllabus](Subject_Plan) · [→ Python learning path](LEARNING_PATH)

| # | Chapter | Status |
|---|---|---|
| 08.1 | [Setup, Tooling & Project Structure]() | 🟡 |
| 08.2 | [Core Language — Syntax, Types, Control Flow & Functions]() | 🟡 |
| 08.3 | [OOP, Data Models & Pythonic Idioms]() | 🟡 |
| 08.4 | [Concurrency — asyncio, threading, multiprocessing & the GIL]() | 🟡 |
| 08.5 | [Testing, Debugging & Logging]() | 🟡 |
| 08.6 | [The Standard Library & Ecosystem Tour]() | 🟡 |
| 08.7 | [Shell, Terminal & Cross-Platform CLI]() | 🟡 |
| 08.8 | [Git & Version Control]() | 🟡 |
| 08.9 | [Docker & Containers]() | 🟡 |
| 08.10 | [Operating Systems Essentials]() | 🟡 |
| 08.11 | [Computer Networks Essentials]() | 🟡 |
| 08.12 | [Computer Architecture — Performance Intuition]() | 🟡 |
| 08.13 | [Algorithms & Data Structures in Python]() | 🟡 |
| 08.14 | [Concurrency Models & Patterns]() | 🟡 |
| 08.15 | [GPU Computing & CUDA Foundations]() | 🟡 |
| 08.16 | [Distributed Systems & Multi-GPU Training]() | 🟡 |

**Practice / labs:** `_practice/scripts/` — environment validation scripts (08.1, 08.7, 08.8, 08.9, 08.10, 08.11, 08.15), algorithm drill generator (08.13). All chapters have hands-on labs that emit markdown reports.

---

## 🧪 Track 24 — AI Experiments (NEW)

> 7 chapters, ~126 KB. Hands-on counterpart to Track 10 (AI/ML theory). Build real things: local CUDA/PyTorch infrastructure, image generation with SDXL/ControlNet, LLM fine-tuning with QLoRA on Llama-3, RAG pipelines, agentic AI with ReAct, voice/audio with Whisper+XTTS, multimodal experiments. Every chapter is structured as: theory briefing → setup → experiment walkthrough → expected results → gotchas → variations.

[→ open the syllabus](Subject_Plan) · [→ AI Experiments learning path](LEARNING_PATH)

| # | Chapter | Status |
|---|---|---|
| 5.1 | [Local AI Infrastructure — CUDA, PyTorch & Multi-GPU Setup]() | 🟡 |
| 5.2 | [Image Generation Experiments — SDXL, ControlNet & LoRA]() | 🟡 |
| 5.3 | [LLM Fine-tuning — LoRA, QLoRA & Full Fine-tuning]() | 🟡 |
| 5.4 | [RAG Pipelines — Embeddings, Vector DBs & Retrieval]() | 🟡 |
| 5.5 | [Agentic AI — ReAct, Tool Calling & Multi-Agent Orchestration]() | 🟡 |
| 5.6 | [Voice & Audio — TTS, ASR & Voice Cloning]() | 🟡 |
| 5.7 | [Multimodal Experiments — Vision-Language & Audio-Text Bridges]() | 🟡 |

**Practice / experiments:** `_practice/scripts/` — runnable PyTorch + HuggingFace scripts targeting a single 24GB GPU. Each has `--demo` and `--config` flags and emits markdown reports.

---

## 🦀 Track 09 — C++ (Modern, Game-Dev Focused)

> 8 chapters, ~195 KB. Modern C++17/20/23 from setup → memory & pointers → OOP+templates → smart pointers/move semantics → STL → concurrency → SIMD/cache → Unreal Engine. Existing cheatsheets (`C++ Pointers & Memory Management.md`, `C++ Basics for Game Dev.md`) preserved as reference appendices.

[→ open the syllabus](Subject_Plan) · [→ C++ learning path](LEARNING_PATH)

---

## 🎯 Track 10 — C# (Unity-Flavored)

> 8 chapters, ~158 KB. Modern C# 11/12 with .NET 8. Setup → core language + LINQ → OOP/patterns → async/await → memory + Span<T> → Unity specifics (MonoBehaviour, ECS, DOTS, Burst) → multiplayer (Mirror/Photon/Netcode) → production patterns (DI, save systems, addressables). Existing `C# Basics for Unity.md` preserved.

[→ open the syllabus](Subject_Plan) · [→ C# learning path](LEARNING_PATH)

---

## 🕹️ Track 26 — Game Development Programming

> 8 chapters, ~168 KB. Engineering side of games: game loop & architecture (ECS, MVC) → gameplay programming → 2D patterns → 3D patterns → save systems → multiplayer/netcode → performance → packaging/distribution. Sister track to Track 06 (design theory) and Track 09 (VR/3D engines).

[→ open the syllabus](Subject_Plan) · [→ Game Dev learning path](LEARNING_PATH)

---

## 🟨 Track 12 — JavaScript (Modern ES2024+)

> 8 chapters, ~169 KB. Setup + runtime (Node, Bun, Deno) → core language (closures, prototypes) → async + event loop → OOP/FP patterns → modules + bundlers → DOM/Browser APIs → frontend frameworks overview → modern backend. Existing `JavaScript Essentials for Coding Tests.md` preserved.

[→ open the syllabus](Subject_Plan) · [→ JS learning path](LEARNING_PATH)

---

## 🎲 Track 25 — Game Design Theory

> 8 chapters, ~200 KB. Theory complement to Track 04. Player psychology + MDA framework → mechanics & systems → dynamics/balance/feedback loops → level design + spatial pacing → narrative + worldbuilding → aesthetics + juice + game feel → playtesting + iteration → monetization + live ops. Heavy cross-link to Tracks 11/12 for psych/neuro depth.

[→ open the syllabus](Subject_Plan) · [→ Game Design learning path](LEARNING_PATH)

---

## 🔷 Track 13 — TypeScript (Modern 5.x)

> 8 chapters, ~188 KB. Setup + tsconfig → type system (primitives, unions, generics) → advanced types (conditional, mapped, template literal) → OOP + FP patterns → async + async generators → modules + bundlers → frontend (React/Vue/Svelte/SolidJS) → backend (Node/Bun/Deno + Hono/Fastify/Express). Existing `TypeScript Essentials for Coding Tests.md` preserved.

[→ open the syllabus](Subject_Plan) · [→ TS learning path](LEARNING_PATH)

---

## 🗃️ Track 01 — SQL (Analytics & Production)

> 8 chapters, ~167 KB. Relational theory + set logic → SELECT mastery (joins, subqueries, CTEs) → aggregations + window functions → schema design + normalization → indexes + query performance → transactions + ACID → triggers/procedures/recursive CTEs → modern SQL (PostgreSQL, DuckDB, SQLAlchemy/SQLModel for Python). Existing SQL cheatsheet preserved.

[→ open the syllabus](Subject_Plan) · [→ SQL learning path](LEARNING_PATH)

---

## 💻 Track 22 — App Architectures & Frameworks

> 5 chapters, ~220 KB. Code-centric architectural literacy across React, Angular, Vite, PyQt/PySide, and Flutter/Dart. Each chapter follows the **Mental Model → Architecture Map → Boilerplate → Lifecycle Deep Dive → Gotchas → Worked Patterns** structure mandated by `Subject_Plan §3`.

[→ open the syllabus](Subject_Plan)

| # | Chapter | Status |
|---|---|---|
| 8.1 | [React & Next.js — Functional Components & Hooks]() | ✅ |
| 8.2 | [Angular — Class-based Architecture & RxJS]() | ✅ |
| 8.3 | [Vite & Modern Build Tools]() | ✅ |
| 8.4 | [PyQt6 & PySide6 — Signals, Slots & Event Loops]() | ✅ |
| 8.5 | [Flutter & Dart — Widget Tree, Isolates & Custom Painters]() | ✅ |

**Reference artifacts:** `22 - App Architectures & Frameworks/_examples/` — five annotated-starter markdown files (React+Next.js, Angular, Vite recipes, PyQt minimal apps, Flutter patterns).

---

## 🎮 Track 28 — VR & 3D Engineering

> 7 chapters, ~249 KB. From 3D math fundamentals and quaternions through the graphics rendering pipeline, GLSL/HLSL shaders, Unity/Unreal architectures, AEC-to-VR pipelines, and spatial-computing interaction design.

[→ open the syllabus](Subject_Plan)

| # | Chapter | Status |
|---|---|---|
| 9.1 | [3D Math Fundamentals]() | ✅ |
| 9.2 | [Quaternions & Rotations]() | ✅ |
| 9.3 | [Graphics Rendering Pipeline]() | ✅ |
| 9.4 | [Shader Programming — GLSL & HLSL]() | ✅ |
| 9.5 | [Game Engine Architectures — Unity & Unreal]() | ✅ |
| 9.6 | [AEC to VR Pipelines — BIM Data]() | ✅ |
| 9.7 | [Spatial Computing & Interaction Design]() | ✅ |

**Practice / code:** `_practice/scripts/` — Python generators for 3D-math drills (TRS, projection), quaternion algebra, software-rasterizer, BIM-mesh decimation; markdown reference notes for shader snippets, engine skeletons (Unity C# / Unreal C++), and WebXR/OpenXR interaction patterns.

---

## 🤖 Track 23 — AI & Machine Learning Systems

> 7 chapters, ~278 KB. The mathematics and architecture of modern AI: statistical learning, deep neural networks (backprop derived by hand), CNNs/ViTs, RNNs/LSTMs, transformer attention (computed by hand), generative models (GANs + diffusion), and reinforcement learning (Q-learning, policy gradients, RLHF, PPO).

[→ open the syllabus](Subject_Plan)

| # | Chapter | Status |
|---|---|---|
| 10.1 | [Statistical Learning & Optimization]() | ✅ |
| 10.2 | [Deep Neural Networks — Backprop & Architecture]() | ✅ |
| 10.3 | [Computer Vision — CNNs & ViTs]() | ✅ |
| 10.4 | [NLP & Recurrent Models — RNNs & LSTMs]() | ✅ |
| 10.5 | [Transformer Architectures & LLMs]() | ✅ |
| 10.6 | [Generative Models — GANs & Diffusion]() | ✅ |
| 10.7 | [Reinforcement Learning & RLHF]() | ✅ |

**Practice / code:** `_practice/scripts/` — Python+NumPy/PyTorch demos with `--demo` flag and `--count/--seed/--out` SR drill mode (optimization, scratch backprop, conv2d math, RNN/LSTM cells, scaled-dot-product attention, diffusion noise schedule, gridworld Q-learning).

---

## 🧠 Track 05 — Neuroscience & Computational Cognition

> 7 chapters, ~219 KB. The biological hardware of the brain mapped to AI architectures. Each chapter has a mandated **AI/ML Translation** section per `Subject_Plan §4.3`: Hebbian learning ↔ backprop, hemispheric lateralization ↔ MoE routing, cortical entropy ↔ LLM temperature, dopamine ↔ TD-learning.

[→ open the syllabus](Subject_Plan)

| # | Chapter | Status |
|---|---|---|
| 11.1 | [Neuroanatomy & The Cortex]() | ✅ |
| 11.2 | [Action Potentials & Ion Channels]() | ✅ |
| 11.3 | [Synaptic Plasticity & Hebbian Learning]() | ✅ |
| 11.4 | [Hemispheric Lateralization & The Corpus Callosum]() | ✅ |
| 11.5 | [The Default Mode Network & Cortical Entropy]() | ✅ |
| 11.6 | [Neuromodulators — Dopamine, Serotonin, Acetylcholine]() | ✅ |
| 11.7 | [Computational Cognition — Bio vs AI Neural Nets]() | ✅ |

**Practice / code:** Hodgkin-Huxley action-potential simulator (SciPy), STDP rule simulator, dopamine-RPE temporal-difference simulator, DMN entropy estimator, callosal-transfer reaction-time model, side-by-side Hebbian-vs-backprop comparison.

---

## 🎯 Track 06 — Behavioral Psychology & Reinforcement Learning

> 6 chapters, ~188 KB. Conditioning, dopamine reward-prediction-error, the Bellman equation and Q-learning, Polyvagal autonomic regulation, C-PTSD modeled as reinforcement learning, and RLHF. Each chapter includes a mandated **Synthesis** section showing how human-behavior parameters inform AI reward-system design.

[→ open the syllabus](Subject_Plan)

| # | Chapter | Status |
|---|---|---|
| 12.1 | [Classical & Operant Conditioning]() | ✅ |
| 12.2 | [Dopamine & Reward Prediction Error]() | ✅ |
| 12.3 | [Q-Learning & The Bellman Equation]() | ✅ |
| 12.4 | [Polyvagal Theory & Autonomic Regulation]() | ✅ |
| 12.5 | [Trauma Adaptations — C-PTSD as Reinforcement Learning]() | ✅ |
| 12.6 | [RLHF — Reinforcement Learning from Human Feedback]() | ✅ |

**Practice / code:** Rescorla-Wagner conditioning generator, TD-learning RPE simulator (matching Schultz 1997 dopamine firing patterns), Q-learning gridworld, Polyvagal state-machine simulator, trauma-policy local-minimum demo, minimal RLHF reward-model + PPO skeleton.

---

## 🏃 Track 34 — Biomechanics & Human-Computer Interface (HCI)

> 7 chapters, ~209 KB. Physics of human movement (kinematics, rotational dynamics for BMX), cardiovascular bioenergetics, autonomic-nervous-system telemetry (HRV), IMU sensor fusion, HCI design heuristics, and building bio-metric software apps (Flutter/Dart + Python). Each chapter has mandated **Biological Impact** and **Software Implementation** sections per `Subject_Plan §3`.

[→ open the syllabus](Subject_Plan)

| # | Chapter | Status |
|---|---|---|
| 13.1 | [Kinematics of Human Movement]() | ✅ |
| 13.2 | [Rotational Dynamics in Extreme Sports]() | ✅ |
| 13.3 | [Cardiovascular Bioenergetics & VO2 Max]() | ✅ |
| 13.4 | [Autonomic Nervous System Telemetry — HRV]() | ✅ |
| 13.5 | [Sensor Fusion — Accelerometers & Gyroscopes]() | ✅ |
| 13.6 | [Human-Computer Interfaces — HCI Design]() | ✅ |
| 13.7 | [Building Bio-metric Software Applications]() | ✅ |

**Practice / code:** Kinematics drills, BMX moment-of-inertia / angular-momentum problems, VO2-max estimators, HRV analyzer (RMSSD, SDNN, pNN50, LF/HF), complementary-filter and Kalman-filter sensor fusion on synthetic IMU data, HCI heuristics reference, Flutter+BLE heart-rate app skeleton.

---

## 🦀 Track 11 — Rust (Modern, Systems-Level)

> 8 chapters, ~162 KB. Setup + Cargo → ownership/borrowing/lifetimes (the centerpiece) → type system (enums, traits, generics) → error handling (Result, Option, ? operator) → concurrency (Send/Sync, async/Tokio) → memory primitives (Box/Rc/Arc/RefCell/Mutex) → idiomatic patterns + performance → production targets (WebAssembly, FFI, embedded, Bevy game dev).

[→ open the syllabus](Subject_Plan) · [→ Rust learning path](LEARNING_PATH)

---

## 🧬 Track 15 — Biology

> 8 chapters, ~169 KB. College-level (MIT 7.012-grade). Cell biology + molecular foundations → genetics + inheritance → DNA/RNA/protein synthesis → evolution + natural selection → ecology + ecosystems → anatomy + physiology → immunology + disease → modern (genomics, CRISPR, synthetic bio). Each chapter has an "AI/ML Translation" section connecting bio to neural networks, evolutionary algorithms, and AlphaFold-class models.

[→ open the syllabus](Subject_Plan) · [→ Biology learning path](LEARNING_PATH)

---

## ⚗️ Track 16 — Chemistry

> 8 chapters, ~149 KB. College-level (MIT 5.111-grade). Atomic structure (built on QM Track 09) → bonding → stoichiometry → thermo + kinetics (built on Stat Mech Track 05) → acids/bases/equilibrium → electrochemistry/redox → organic chemistry → biochemistry + computational chem (DFT, drug design, AI-for-chem). Every chapter has an explicit "Common Misconceptions / Where Most Students Fail" section addressing the cognitive blocks that derailed learners the first time.

[→ open the syllabus](Subject_Plan) · [→ Chemistry learning path](LEARNING_PATH)

---

## 📐 Tracks 13-16 — K-12 Mathematics Pipeline *(NEW)*

> Four math tracks covering grades 6-12, from the first algebra concepts through the calculus runway. Together with Track 01 (Math & Physics tower), these provide complete K-12 through university math coverage. All Subject_Plans, LEARNING_PATH files, and 8-chapter stubs created; chapters ready for content expansion.

| Track | Subject | Grade Band | Unlocks |
|-------|---------|-----------|---------|
| **44** | [44 — Pre-Algebra]() | Grades 6-8 | Algebra I |
| **45** | [45 — Algebra I]() | Grades 8-9 | Geometry + Algebra II |
| **46** | [46 — Geometry]() | Grades 9-10 | Algebra II, Proof reasoning |
| **47** | [47 — Algebra II & Pre-Calculus]() | Grades 10-11 | Track 01 Calculus |
| **48** | [48 — Statistics & Probability]() | Grades 11-12 / AP Stats | Track 23 AI/ML |

**Free resources (all free):** Khan Academy (all tracks) · OpenStax Algebra/Trig 2e · OpenStax Intro Statistics 2e · Desmos · GeoGebra · Professor Leonard (YouTube) · StatQuest (YouTube)

---

## 🌍 Tracks 17-19 — K-12 Social Studies / Humanities Pipeline *(NEW)*

> Three social studies tracks covering grades 9-12 — the full history and economics requirement for a complete K-12 humanities pipeline.

| Track | Subject | Grade Band | AP Alignment |
|-------|---------|-----------|-------------|
| **49** | [49 — World History]() | Grades 9-10 | AP World History: Modern |
| **50** | [50 — US History]() | Grade 11 | AP US History (APUSH) |
| **51** | [51 — Economics]() | Grade 12 | AP Micro + AP Macro |

**Free resources:** OpenStax Micro/Macro 3e · American Yawp (US History) · World History Encyclopedia · Heimler's History (YouTube) · ACDCLeadership (YouTube) · Crash Course History + Economics (YouTube)

---

## 🌏 Track 20 — Earth Science *(NEW)*

> Completes the natural sciences pipeline. Grades 6-9 / NGSS-aligned / foundation for AP Environmental Science.

[→ open syllabus](Subject_Plan) · [→ learning path](LEARNING_PATH)

8-chapter track: Earth systems → Plate tectonics → Rocks & minerals → Water cycle & oceans → Weather & atmosphere → Solar system & universe → Earth's history → Human impact & environmental science.

**Free resources:** CK-12 Earth Science · USGS Education · NASA Earth Observatory · NOAA Education · Crash Course Astronomy

---

## 🇨🇳 Track 21 — Mandarin Chinese *(NEW)*

> The most-studied second language globally — 100M+ learners worldwide. Zero through HSK 4 / ACTFL Intermediate-High. Category IV difficulty for English speakers; this curriculum uses the most efficient acquisition methods known.

[→ open syllabus](Subject_Plan) · [→ learning path](LEARNING_PATH)

8-chapter track: Tones & pinyin (the non-negotiable first step) → Character system & radicals → Basic grammar HSK 1-2 → Aspect markers HSK 2-3 → 把/被 & complex grammar HSK 3-4 → Character system depth → Idioms & chéngyǔ → Reading/listening immersion.

**Non-negotiable tools:** Pleco app (free dictionary + stroke order) · Anki HSK decks · DuChinese graded readers
**Free resources:** Yoyo Chinese (YouTube) · Mandarin Corner (YouTube) · ChinesePod · MDBG Dictionary · Seeing Theory (stats reference)

---

## 🔗 Learning App Material

See `[10 - Learning App Material](README)` for the platform engineering side of this curriculum — the K-12 curriculum pipeline, subject gap manifest, grade band pipelines (K-5, 6-8, 9-12, higher ed), AP subject alignments, SAT prep pipeline, and the full app pipeline architecture spec (vault → Astro static site → interactive drill layer → full platform).

---

## 🫀 Track 22 — Anatomy *(formerly Track 17)*

> 8 chapters, systems-first then regional pass. Adult-learner Human Anatomy — **systems pass** (chapters 40.2–40.7: skeletal → muscular → nervous → cardiovascular → respiratory/digestive → endocrine/urinary/reproductive) followed by a **regional + clinical pass** (chapter 40.8: head/neck, thorax, abdomen, upper limb, lower limb) — the way a clinician or surgeon actually navigates the body. Full Pearson/Ambrose textbook depth: every bone, every muscle origin/insertion/action, all 12 cranial nerves, brachial plexus, nephron, cardiac conduction system. Cross-links to [Biology](Subject_Plan), [Neuroscience](Subject_Plan), and [Biomechanics](Subject_Plan).

[→ open the syllabus](Subject_Plan) · [→ Anatomy learning path](LEARNING_PATH) · [→ subject hub](README)

| # | Chapter | Status |
|---|---|---|
| 40.1 | [Anatomical Terminology & Body Organization]() | ✅ Full |
| 40.2 | [The Skeletal System]() | ✅ Full |
| 40.3 | [The Muscular System]() | ✅ Full |
| 40.4 | [The Nervous System]() | ✅ Full |
| 40.5 | [The Cardiovascular & Lymphatic System]() | ✅ Full |
| 40.6 | [The Respiratory & Digestive Systems]() | ✅ Full |
| 40.7 | [The Endocrine, Urinary & Reproductive Systems]() | ✅ Full |
| 40.8 | [Regional & Clinical Anatomy]() | ✅ Full |

**Practice scripts:** `40 - Anatomy/_practice/scripts/` — `40.2_skeletal_drill.py` (bone + joint classification drills) · `40.4_cranial_nerve_drill.py` (all 12 cranial nerves × 5 modes)

**Free resources:** [OpenStax A&P 2e](https://openstax.org/details/books/anatomy-and-physiology-2e) · [Kenhub](https://www.kenhub.com/) · [TeachMeAnatomy](https://teachmeanatomy.info/) · [Radiopaedia](https://radiopaedia.org/) · [Zygote Body](https://www.zygotebody.com/)

---

## 🌎 Tracks 18–23 — Human Languages

> Six-language curriculum spanning Romance languages (Spanish, French, Italian), classical Latin, Japanese, and English. The Romance tracks are deliberately cross-linked — Latin is the root; Italian → French → Spanish exploit 75–90% vocabulary overlap. Japanese is the outlier: structurally alien to all others, with its own vault-native kanji database.

### Language Track Quick Reference

| Track | Folder | Target level | Status | Cross-links |
|-------|--------|-------------|--------|-------------|
| 18 | [36 - Spanish]() | B2/C1 | ⏳ Chapters planned | → French, Italian, Latin |
| 19 | [41 - French]() | B2/C1 | 🟡 41.1–41.3 full, 41.4–41.8 draft | → Spanish, Italian, Latin |
| 20 | [38 - English]() | C1/C2 | 🟡 Draft | → All languages |
| 21 | [42 - Italian]() | B2 | 🟡 42.1–42.3 full, 42.4–42.8 draft | → Spanish, French, Latin |
| 22 | [43 - Latin]() | Classical reading | 🟡 43.1 full, 43.2–43.8 draft | → French, Italian, Spanish |
| 23 | [37 - Japanese]() | JLPT N3 | ⏳ Chapters planned | Kanji database at `_kanji/` |

---

### 36 - Spanish (Track 17)

Adult-learner Spanish curriculum (A1 → B2/C1). Phonetics → nouns/articles/gender → pronouns → verbs (present, past, future, **the subjunctive**) → idioms → reading/listening immersion. **Highest ROI first Romance language** — unlocks French and Italian at accelerated pace.

[→ open syllabus](Subject_Plan) · [→ learning path](LEARNING_PATH) · [→ subject hub](README)

---

### 41 - French (Track 18) *(NEW)*

Adult-learner French (zero → B2/C1) with **Romance-transfer optimization** for English speakers with Spanish background. Front-loads phonetics (nasal vowels, liaison, elision) before grammar. Chapters 41.1–41.3 are fully expanded; 41.4–41.8 are ready for content expansion.

[→ open syllabus](Subject_Plan) · [→ learning path](LEARNING_PATH) · [→ subject hub](README)

| # | Chapter | Status |
|---|---|---|
| 41.1 | [Phonetics, Liaison & The French Sound System]() | ✅ Full |
| 41.2 | [Nouns, Articles, Gender & Adjective Agreement]() | ✅ Full |
| 41.3 | [Pronouns — Subject, Object & Reflexive]() | ✅ Full |
| 41.4 | [Verb System — Present, Imperative & Immediate Future]() | 🟡 Draft |
| 41.5 | [Past Tenses — Passé Composé, Imparfait & Plus-que-parfait]() | 🟡 Draft |
| 41.6 | [Future, Conditional & The Subjunctive]() | 🟡 Draft |
| 41.7 | [Idioms, Register & Regional Variation]() | 🟡 Draft |
| 41.8 | [Reading, Listening & Cultural Immersion]() | 🟡 Draft |

**Free resources:** [Language Transfer French](https://www.languagetransfer.org/french) · [Tex's French Grammar](https://coerll.utexas.edu/tex/) · [InnerFrench YouTube](https://www.youtube.com/@innerfrench) · [TV5MONDE](https://apprendre.tv5monde.com/en)

---

### 38 - English (Track 19)

Grammar precision → punctuation/mechanics → vocabulary roots → essay structure → argumentation → research writing → style/voice → literary analysis. Foundation track that accelerates all other language learning.

[→ open syllabus](Subject_Plan)

---

### 42 - Italian (Track 20) *(NEW)*

Adult-learner Italian (zero → B2) — **the fastest Romance language to conversational fluency.** Phonetically transparent (what you see is what you say). Chapters 42.1–42.3 fully expanded including the double-pronoun table and the unique Italian particles *ne* and *ci*. Congiuntivo is more used in everyday Italian speech than in any other Romance language.

[→ open syllabus](Subject_Plan) · [→ learning path](LEARNING_PATH) · [→ subject hub](README)

| # | Chapter | Status |
|---|---|---|
| 42.1 | [Phonetics & The Italian Sound System]() | ✅ Full |
| 42.2 | [Nouns, Articles, Gender & Adjective Agreement]() | ✅ Full |
| 42.3 | [Pronouns — Subject, Object, Reflexive & Ne/Ci]() | ✅ Full |
| 42.4 | [Verb System — Present, Imperative & Reflexive Verbs]() | 🟡 Draft |
| 42.5 | [Past Tenses — Passato Prossimo, Imperfetto & Trapassato]() | 🟡 Draft |
| 42.6 | [Future, Conditional & The Congiuntivo]() | 🟡 Draft |
| 42.7 | [Idioms, Dialects & Cultural Register]() | 🟡 Draft |
| 42.8 | [Reading, Listening & Cultural Immersion]() | 🟡 Draft |

**Free resources:** [Language Transfer Italian](https://www.languagetransfer.org/italian) · [Dreaming Italian](https://www.youtube.com/@DreamingItalian) · [Italy Made Easy](https://www.youtube.com/@ItalyMadeEasy) · [RAI Play](https://www.raiplay.it/)

---

### 43 - Latin (Track 21) *(NEW)*

Adult-learner Latin (zero → reading authentic classical prose and poetry). The case system treated as a **type system**; grammar as axiomatic. Chapter 43.1 fully expanded with reconstructed classical pronunciation, vowel quantities, and the accent rule. 43.2–43.8 structured and ready for expansion. Unlocks: ~90% of French vocabulary, ~75% of Spanish/Italian vocabulary, ~30% of English academic/technical register, Ancient Greek (parallel study).

[→ open syllabus](Subject_Plan) · [→ learning path](LEARNING_PATH) · [→ subject hub](README)

| # | Chapter | Status |
|---|---|---|
| 43.1 | [The Latin Alphabet, Pronunciation & Quantities]() | ✅ Full |
| 43.2 | [The Case System — Nouns & The 5 Declensions]() | 🟡 Draft |
| 43.3 | [Adjectives, Pronouns & Agreement]() | 🟡 Draft |
| 43.4 | [The Verb System — Present System Active & Passive]() | 🟡 Draft |
| 43.5 | [The Perfect System & Infinitives]() | 🟡 Draft |
| 43.6 | [Participles, Gerunds & The Subjunctive]() | 🟡 Draft |
| 43.7 | [Advanced Syntax — Subordinate Clauses & Rhetorical Style]() | 🟡 Draft |
| 43.8 | [Reading Latin — Caesar, Cicero, Virgil & Ovid]() | 🟡 Draft |

**Free resources:** [Perseus Digital Library](http://www.perseus.tufts.edu/) · [Wheelock's Latin](https://wheelockslatin.com/) · [ScorpioMartianus YouTube](https://www.youtube.com/@ScorpioMartianus) · [Dickinson Commentaries](https://dcc.dickinson.edu/)

---

### 37 - Japanese (Track 22)

Adult-learner Japanese (Zero → JLPT N3) with **vault-native kanji database** at `37 - Japanese/_kanji/` — per-kanji notes with KANJIDIC2 frontmatter + KanjiVG stroke-order SVGs. Subject_Plan written; chapters planned.

[→ open syllabus](Subject_Plan) · [→ learning path](LEARNING_PATH) · [→ kanji method docs](README)

---

## 🏛️ Track 20 — 3D Modelling

> 8 chapters, ~75 KB skeleton. Architecture-CAD-rooted curriculum: Revit fundamentals + advanced (adaptive components, Dynamo 3.5 with Revit 2026.1) → Fusion 360 → Maya & 3ds Max → Blender 4.4 (Geometry Nodes) → SolidWorks → Pipelines, Interop & Productization (USD, IFC, glTF, Speckle). Designed for an architecture-trained learner turning Revit + 3D skills into a productized business pipeline. Each chapter references external pictures + videos via URL; SVG hero diagrams live inline.

[→ open the syllabus](Subject_Plan) · [→ 3D Modelling learning path](LEARNING_PATH) · [→ subject hub](README)

| # | Chapter | Status |
|---|---|---|
| 20.1 | [3D Modelling Foundations & Coordinate Systems]() | 🟡 Skeleton |
| 20.2 | [Autodesk Revit Fundamentals]() | 🟡 Skeleton |
| 20.3 | [Advanced Revit — Families, Adaptive Components & Dynamo]() | 🟡 Skeleton |
| 20.4 | [Autodesk Fusion 360 — Parametric Modelling & CAM]() | 🟡 Skeleton |
| 20.5 | [Maya & 3ds Max — DCC, Animation & Arch-Viz Rendering]() | 🟡 Skeleton |
| 20.6 | [Blender — Open-Source Modelling, Geometry Nodes & Sculpting]() | 🟡 Skeleton |
| 20.7 | [SolidWorks — Mechanical CAD, Assemblies & Simulation]() | 🟡 Skeleton |
| 20.8 | [Pipelines, Interop & Productization — From Architecture to Business]() | 🟡 Skeleton |

---

## ⚡ Track 21 — Electronics

> 8 chapters, ~70 KB skeleton. Classical EE ladder: charge / Ohm / Kirchhoff → passive components (RLC) → semiconductors (BJT / MOSFET / op-amps) → digital logic + FSMs → microcontrollers (Arduino, ESP32, RP2040, STM32) → motherboards & computer architecture (CPU, RAM, PCIe, UEFI) → power electronics & motor drivers → bridge to robotics (I²C / SPI / UART / CAN, sensors, actuators). The on-ramp prerequisite for [Track 32 - Robotics](Subject_Plan).

[→ open the syllabus](Subject_Plan) · [→ Electronics learning path](LEARNING_PATH) · [→ subject hub](README)

| # | Chapter | Status |
|---|---|---|
| 21.1 | [Electrical Fundamentals]() | 🟡 Skeleton |
| 21.2 | [Passive Components]() | 🟡 Skeleton |
| 21.3 | [Semiconductors]() | 🟡 Skeleton |
| 21.4 | [Digital Logic & Boolean Algebra]() | 🟡 Skeleton |
| 21.5 | [Microcontrollers & Embedded Systems]() | 🟡 Skeleton |
| 21.6 | [Motherboards & Computer Architecture]() | 🟡 Skeleton |
| 21.7 | [Power Electronics & Motor Drivers]() | 🟡 Skeleton |
| 21.8 | [Bridge to Robotics — Buses, Sensors, Actuators]() | 🟡 Skeleton |

---

## 🤖 Track 22 — Robotics

> 8 chapters, ~80 KB skeleton. Modern robotics curriculum aligned with the **2026 humanoid inflection point** (Boston Dynamics electric Atlas in commercial production for Hyundai + Google DeepMind, Figure AI 03 deployments, Tesla Optimus Gen 3 announced for end-2026, Unitree G1, 1X NEO, Apptronik Apollo). Foundations / kinematics → FK + IK + Jacobians → sensors + perception (IMU, LiDAR, RGB-D) → actuators + motor control (FOC, ODrive, SimpleFOC) → ROS 2 (Jazzy / Humble) + DDS → SLAM + Nav2 + ORB-SLAM3 → manipulation + MoveIt 2 + VLA models (RT-2, OpenVLA, Helix, RDT-1B, GR00T) → humanoids + drones + the 2026 industry landscape.

[→ open the syllabus](Subject_Plan) · [→ Robotics learning path](LEARNING_PATH) · [→ subject hub](README)

| # | Chapter | Status |
|---|---|---|
| 22.1 | [Robotics Foundations & Kinematics]() | 🟡 Skeleton |
| 22.2 | [Forward & Inverse Kinematics]() | 🟡 Skeleton |
| 22.3 | [Sensors & Perception]() | 🟡 Skeleton |
| 22.4 | [Actuators & Motor Control]() | 🟡 Skeleton |
| 22.5 | [ROS / ROS 2 & Middleware]() | 🟡 Skeleton |
| 22.6 | [SLAM & Autonomous Navigation]() | 🟡 Skeleton |
| 22.7 | [Manipulation & Grasping]() | 🟡 Skeleton |
| 22.8 | [Humanoids, Drones & The Future of Robotics]() | 🟡 Skeleton |

---

## 🌌 Track 23 — Holographics

> 8 chapters, ~75 KB skeleton. The most physics-heavy of the spatial-computing tracks. Wave optics + Fourier optics → classical holography (Gabor, Leith-Upatnieks, Denisyuk) → Computer-Generated Holography (FFT propagators, Gerchberg-Saxton, MIT Tensor Holography, neural CGH) → Spatial Light Modulators (LCoS, DMD, 2026 metasurface SLMs) → light-field & volumetric capture (Looking Glass, Sony Spatial Reality, NeRF, 3D Gaussian Splatting) → "holographic" AR (HoloLens 2, Magic Leap 2 — the marketing-vs-physics gap) → architectural visualization holographics → the photons-to-pixels-to-product systems stack.

[→ open the syllabus](Subject_Plan) · [→ Holographics learning path](LEARNING_PATH) · [→ subject hub](README)

| # | Chapter | Status |
|---|---|---|
| 23.1 | [Optics Foundations]() | 🟡 Skeleton |
| 23.2 | [Classical Holography]() | 🟡 Skeleton |
| 23.3 | [Computer-Generated Holography (CGH + Neural CGH)]() | 🟡 Skeleton |
| 23.4 | [SLMs & Holographic Displays]() | 🟡 Skeleton |
| 23.5 | [Light-Field Displays & Volumetric Capture]() | 🟡 Skeleton |
| 23.6 | [Holographic AR — HoloLens, Magic Leap, Waveguides]() | 🟡 Skeleton |
| 23.7 | [Holography in Architecture & Engineering Visualization]() | 🟡 Skeleton |
| 23.8 | [Systems Stack — Photons → Pixels → Products]() | 🟡 Skeleton |

---

## 🥽 Track 24 — VR (Applied / Business)

> 8 chapters, ~75 KB skeleton. The applied / business capstone of the 20→21→22→23→24 chain. Deliberately complementary to [Track 28 - VR 09 - VR & 3D 3D Engineering](Subject_Plan) (which is the math + rendering foundations). Hardware ecosystems (Quest 3 / 3S, Vision Pro 2, Index 2, Pico 5) → app architectures (OpenXR, WebXR, Unity XR, Unreal XR, RealityKit) → locomotion + comfort → hand / eye / body tracking → MR + passthrough + scene understanding → architectural visualization (Revit / IFC / USD → Quest + Vision Pro) → networking + avatars + multi-user → VR as a business.

[→ open the syllabus](Subject_Plan) · [→ VR learning path](LEARNING_PATH) · [→ subject hub](README)

| # | Chapter | Status |
|---|---|---|
| 24.1 | [VR Hardware Ecosystems & Standards]() | 🟡 Skeleton |
| 24.2 | [Immersive App Architectures]() | 🟡 Skeleton |
| 24.3 | [Locomotion & Comfort Design]() | 🟡 Skeleton |
| 24.4 | [Hand, Eye & Body Tracking]() | 🟡 Skeleton |
| 24.5 | [Mixed Reality & Passthrough Pipelines]() | 🟡 Skeleton |
| 24.6 | [Architectural Visualization in VR]() | 🟡 Skeleton |
| 24.7 | [Networking, Avatars & Multi-User Spaces]() | 🟡 Skeleton |
| 24.8 | [VR as a Business]() | 🟡 Skeleton |

---

## 🛡️ Track 25 — Cybersecurity

> 8 chapters, ~140 KB skeleton. The defensible bolt-on for an AI-assisted developer: threat modeling (STRIDE / DREAD / Mozilla RRA) → OWASP Top 10:2025 deep dive → modern auth & identity (OAuth 2.1, OIDC, WebAuthn / passkeys) → cryptography for developers (AES-GCM, Ed25519, Argon2id, NIST-standardized post-quantum: ML-KEM / ML-DSA / SLH-DSA) → secure SDLC + supply chain (SAST, SCA, SBOM, Sigstore, SLSA) → network security (TLS 1.3, CSP, Zero Trust, WAF) → cloud & container security (IAM, KMS, Kubernetes Pod Security Standards, Falco) → AI security & adversarial ML (OWASP LLM Top 10:2025, prompt injection, MCP threats). Web-grounded with 2026 Veracode + AppSecSanta data showing 25–55% of AI-generated code has confirmed vulnerabilities. Directly closes the [§5 cybersecurity gap](BUILDING_AT_SCALE#-cybersecurity--the-part-ai-ghost-writes-worst).

[→ open the syllabus](Subject_Plan) · [→ Cybersecurity learning path](LEARNING_PATH) · [→ subject hub](README)

| # | Chapter | Status |
|---|---|---|
| 25.1 | [Threat Modeling Fundamentals — STRIDE / DREAD / RRA]() | 🟡 Skeleton |
| 25.2 | [OWASP Top 10:2025 Deep Dive]() | 🟡 Skeleton |
| 25.3 | [Authentication, Authorization & Identity — OAuth 2.1 / OIDC / WebAuthn]() | 🟡 Skeleton |
| 25.4 | [Cryptography for Developers — AES-GCM / Ed25519 / Argon2id / PQC]() | 🟡 Skeleton |
| 25.5 | [Secure SDLC & Supply Chain — SAST / SCA / SBOM / Sigstore / SLSA]() | 🟡 Skeleton |
| 25.6 | [Network Security — TLS 1.3 / CSP / Zero Trust / WAF]() | 🟡 Skeleton |
| 25.7 | [Cloud & Container Security — IAM / KMS / K8s PSS / Falco]() | 🟡 Skeleton |
| 25.8 | [AI Security & Adversarial ML — OWASP LLM Top 10 / Prompt Injection]() | 🟡 Skeleton |

---

## ⚙️ Track 26 — DevOps & SRE

> 8 chapters, ~135 KB skeleton. How to actually run any of this in production. CI/CD foundations (GitHub Actions, GitLab CI, monorepo build graphs) → Infrastructure as Code (Terraform vs OpenTofu post-fork, Pulumi, Crossplane) → containers & orchestration (Docker, Kubernetes, Helm, GitOps with Argo CD / Flux) → observability (OpenTelemetry, Prometheus, Grafana, Loki, Tempo — logs/metrics/traces unified) → SLOs / SLAs / error budgets / incident response (Google SRE book, blameless postmortems, PagerDuty rotations) → chaos engineering & resilience (Litmus, Gremlin, AWS FIS, circuit breakers) → deployment strategies (blue-green, canary, feature flags, Argo Rollouts) → cost & capacity engineering / FinOps (autoscaling, KEDA, spot, cost dashboards, platform-engineering trend). Directly closes the [§10 DevOps gap](BUILDING_AT_SCALE#-vault-gaps--what-tracks-i-think-we-should-add-next).

[→ open the syllabus](Subject_Plan) · [→ DevOps & SRE learning path](LEARNING_PATH) · [→ subject hub](README)

| # | Chapter | Status |
|---|---|---|
| 26.1 | [CI/CD Foundations — GitHub Actions, GitLab CI, monorepos]() | 🟡 Skeleton |
| 26.2 | [Infrastructure as Code — Terraform / OpenTofu / Pulumi / Crossplane]() | 🟡 Skeleton |
| 26.3 | [Containers & Orchestration — Docker / Kubernetes / Helm / Argo CD]() | 🟡 Skeleton |
| 26.4 | [Observability — Logs / Metrics / Traces with OpenTelemetry]() | 🟡 Skeleton |
| 26.5 | [SLOs, SLAs, Error Budgets & Incident Response]() | 🟡 Skeleton |
| 26.6 | [Chaos Engineering & Resilience]() | 🟡 Skeleton |
| 26.7 | [Deployment Strategies — Blue-Green / Canary / Feature Flags]() | 🟡 Skeleton |
| 26.8 | [Cost & Capacity Engineering — FinOps]() | 🟡 Skeleton |

---

## 🏗️ Track 27 — System Design & Distributed Architecture

> 8 chapters, ~130 KB skeleton. The failure-domain decomposition vocabulary that [BUILDING_AT_SCALE §2](BUILDING_AT_SCALE#-2-the-mental-model--split-your-app-by-failure-domain) argued for. System design fundamentals (CAP, PACELC, latency numbers, consistency models) → caching, CDNs & edge (Redis, Memcached, Cloudflare/Fastly, edge compute) → databases at scale (replicas, sharding, NewSQL, vector DBs, time-series) → message queues & event-driven architecture (Kafka vs NATS vs RabbitMQ, CQRS, Saga, transactional outbox) → API design (REST, GraphQL Federation, gRPC, OpenAPI, AsyncAPI, gateways) → microservices & service mesh (when to actually decompose, modular monolith first, Istio / Linkerd) → real-time systems (WebSockets, WebRTC, SSE, CRDTs, multiplayer patterns) → capacity planning & back-of-envelope math (k6 load testing, queueing theory, percentiles, Universal Scalability Law). Directly closes the [§10 system design gap](BUILDING_AT_SCALE#-vault-gaps--what-tracks-i-think-we-should-add-next).

[→ open the syllabus](Subject_Plan) · [→ System Design learning path](LEARNING_PATH) · [→ subject hub](README)

| # | Chapter | Status |
|---|---|---|
| 27.1 | [System Design Fundamentals — CAP, PACELC, Latency Numbers]() | 🟡 Skeleton |
| 27.2 | [Caching, CDNs & Edge]() | 🟡 Skeleton |
| 27.3 | [Databases at Scale — Replicas / Sharding / NewSQL / Vector]() | 🟡 Skeleton |
| 27.4 | [Message Queues & Event-Driven Architecture — Kafka / NATS / Saga]() | 🟡 Skeleton |
| 27.5 | [API Design — REST / GraphQL / gRPC / OpenAPI / AsyncAPI]() | 🟡 Skeleton |
| 27.6 | [Microservices & Service Mesh — When to Decompose]() | 🟡 Skeleton |
| 27.7 | [Real-Time Systems — WebSockets / WebRTC / SSE / CRDTs]() | 🟡 Skeleton |
| 27.8 | [Capacity Planning & Back-of-Envelope Math]() | 🟡 Skeleton |

---

## ☁️ Track 28 — Cloud Platforms

> 8 chapters, ~135 KB skeleton. The actual buttons you push to deploy. The 2026 cloud provider landscape (AWS / GCP / Azure hyperscaler share, Cloudflare's edge bet, Hetzner's bare-metal renaissance) → compute primitives (VMs, containers, serverless, GPU clouds — CoreWeave / Lambda Labs / RunPod) → storage & databases (object/block, managed Postgres, vector, warehouses) → networking, DNS & CDN (VPC, BGP, CDN, Tunnels, Tailscale) → identity, IAM & org structure (workload identity, SSO, multi-account / multi-project layouts) → cost optimization (FinOps, spot instances, CUDs, dashboards) → multi-cloud, edge & vendor lock-in (when multi-cloud is actually justified, edge runtimes, Cloudflare Workers vs Lambda@Edge, exit strategy) → the indie & solo cloud stack (Fly.io / Railway / Render / Cloudflare for the BUILDING_AT_SCALE §9 playbook expanded). Directly closes the [§10 cloud platforms gap](BUILDING_AT_SCALE#-vault-gaps--what-tracks-i-think-we-should-add-next).

[→ open the syllabus](Subject_Plan) · [→ Cloud Platforms learning path](LEARNING_PATH) · [→ subject hub](README)

| # | Chapter | Status |
|---|---|---|
| 28.1 | [The Cloud Provider Landscape 2026]() | 🟡 Skeleton |
| 28.2 | [Compute Primitives — VMs / Containers / Serverless / GPU]() | 🟡 Skeleton |
| 28.3 | [Storage & Databases — Object / Block / Managed Postgres / Vector]() | 🟡 Skeleton |
| 28.4 | [Networking, DNS & CDN — VPC / BGP / Tunnels / Tailscale]() | 🟡 Skeleton |
| 28.5 | [Identity, IAM & Org Structure]() | 🟡 Skeleton |
| 28.6 | [Cost Optimization — FinOps / Spot / CUDs]() | 🟡 Skeleton |
| 28.7 | [Multi-Cloud, Edge & Vendor Lock-In]() | 🟡 Skeleton |
| 28.8 | [The Indie & Solo Cloud Stack — BUILDING_AT_SCALE §9 Expanded]() | 🟡 Skeleton |

---

## 🔧 Track 29 — Compilers & Language Design

> 8 chapters, ~3,500 lines. The mechanical room beneath every language you know. Lexers → parsers → ASTs → type systems → IR → codegen → optimization → VMs & JIT. Directly powers AI tooling work (code analysis, LLM-based linters, custom DSLs).

[→ open the syllabus](Subject_Plan) · [→ Compilers learning path](LEARNING_PATH)

| # | Chapter | Status |
|---|---|---|
| 29.1 | [Lexers & Tokenization]() | 🟡 Skeleton |
| 29.2 | [Parsers & Grammars]() | 🟡 Skeleton |
| 29.3 | [Abstract Syntax Trees & Semantic Analysis]() | 🟡 Skeleton |
| 29.4 | [Type Systems & Type Checking]() | 🟡 Skeleton |
| 29.5 | [Intermediate Representations & IR Design]() | 🟡 Skeleton |
| 29.6 | [Code Generation & Backends]() | 🟡 Skeleton |
| 29.7 | [Optimization Passes]() | 🟡 Skeleton |
| 29.8 | [Virtual Machines, Bytecode & JIT]() | 🟡 Skeleton |

---

## 🗄️ Track 30 — Databases & Storage Engines

> 8 chapters. The engine room beneath every database. B-trees, LSM trees, WAL, ARIES, MVCC, query planning — everything that happens below SQL. Pairs with Track 27 (System Design) and Track 07 (SQL).

[→ open the syllabus](Subject_Plan) · [→ DB Internals learning path](LEARNING_PATH)

| # | Chapter | Status |
|---|---|---|
| 30.1 | [Storage Engine Fundamentals]() | 🟡 Skeleton |
| 30.2 | [B-Trees & Page Management]() | 🟡 Skeleton |
| 30.3 | [LSM-Trees & Write-Optimized Storage]() | 🟡 Skeleton |
| 30.4 | [Transaction Management & ACID]() | 🟡 Skeleton |
| 30.5 | [Write-Ahead Logging & Recovery]() | 🟡 Skeleton |
| 30.6 | [Concurrency Control & MVCC]() | 🟡 Skeleton |
| 30.7 | [Query Processing & Execution]() | 🟡 Skeleton |
| 30.8 | [Distributed Databases & Replication]() | 🟡 Skeleton |

---

## 🌐 Track 31 — Networking & Protocols

> 8 chapters. See the wire. TCP handshakes, TLS key exchange, HTTP/2 multiplexing, QUIC 0-RTT, WebRTC ICE, gRPC streaming, mTLS — critical for multiplayer game netcode, VR streaming, distributed AI inference.

[→ open the syllabus](Subject_Plan) · [→ Networking learning path](LEARNING_PATH)

| # | Chapter | Status |
|---|---|---|
| 31.1 | [Physical & Data Link Layer]() | 🟡 Skeleton |
| 31.2 | [IP, Routing & BGP]() | 🟡 Skeleton |
| 31.3 | [TCP & UDP Deep Dive]() | 🟡 Skeleton |
| 31.4 | [TLS, mTLS & PKI]() | 🟡 Skeleton |
| 31.5 | [HTTP/1.1, HTTP/2 & HTTP/3 (QUIC)]() | 🟡 Skeleton |
| 31.6 | [WebSockets, SSE & WebRTC]() | 🟡 Skeleton |
| 31.7 | [gRPC, Protocol Buffers & Service Mesh]() | 🟡 Skeleton |
| 31.8 | [Network Security & DDoS Mitigation]() | 🟡 Skeleton |

---

## 〜 Track 32 — Signal Processing & DSP

> 8 chapters. Bridges math/physics, audio AI (TTS/ASR), holographics, and electronics. FFT, filters, MFCCs, spectrograms — the signal chain from microphone to Whisper to holographic wavefront.

[→ open the syllabus](Subject_Plan) · [→ DSP learning path](LEARNING_PATH)

| # | Chapter | Status |
|---|---|---|
| 32.1 | [Signals, Systems & Sampling Theory]() | 🟡 Skeleton |
| 32.2 | [Fourier Series & Fourier Transform]() | 🟡 Skeleton |
| 32.3 | [Discrete Fourier Transform & FFT]() | 🟡 Skeleton |
| 32.4 | [Digital Filters — FIR & IIR]() | 🟡 Skeleton |
| 32.5 | [Audio Signal Processing & Psychoacoustics]() | 🟡 Skeleton |
| 32.6 | [Image Processing & 2D Transforms]() | 🟡 Skeleton |
| 32.7 | [Speech & Voice Processing (ASR/TTS Foundations)]() | 🟡 Skeleton |
| 32.8 | [Spectral Analysis & Applications in AI]() | 🟡 Skeleton |

---

## 💼 Track 33 — Business & Entrepreneurship

> 8 chapters. Turn the builder into the founder. Idea validation → business models → pricing → GTM → fundraising → sales → legal → scaling. For the AI tools, games, and content brand.

[→ open the syllabus](Subject_Plan) · [→ Business learning path](LEARNING_PATH)

| # | Chapter | Status |
|---|---|---|
| 33.1 | [Founder Mindset & Idea Validation]() | 🟡 Skeleton |
| 33.2 | [Business Models & Revenue Architecture]() | 🟡 Skeleton |
| 33.3 | [Pricing Strategy & Value Capture]() | 🟡 Skeleton |
| 33.4 | [Go-To-Market Strategy & Distribution]() | 🟡 Skeleton |
| 33.5 | [Fundraising, Investors & Equity]() | 🟡 Skeleton |
| 33.6 | [Sales, Negotiation & Closing]() | 🟡 Skeleton |
| 33.7 | [Legal Basics for Founders]() | 🟡 Skeleton |
| 33.8 | [Scaling Operations & Building Teams]() | 🟡 Skeleton |

---

## 🔩 Track 34 — Mechanical Engineering & Fabrication *(maybe-tier)*

> 8 chapters. Turn AET/architecture training and 3D modelling skills into physical manufacturing ability. CNC, 3D printing, GD&T, tolerancing, and the full CAD-to-fabrication pipeline.

[→ open the syllabus](Subject_Plan) · [→ Mech Eng learning path](LEARNING_PATH)

| # | Chapter | Status |
|---|---|---|
| 34.1 | [Engineering Drawing & GD&T]() | 🟡 Skeleton |
| 34.2 | [Materials Science & Selection]() | 🟡 Skeleton |
| 34.3 | [Manufacturing Processes & DFM]() | 🟡 Skeleton |
| 34.4 | [CNC Machining & G-Code]() | 🟡 Skeleton |
| 34.5 | [3D Printing & Additive Manufacturing]() | 🟡 Skeleton |
| 34.6 | [Tolerancing, Fits & Assemblies]() | 🟡 Skeleton |
| 34.7 | [FreeCAD & Parametric Modelling]() | 🟡 Skeleton |
| 34.8 | [Mechatronics & CAD-to-Fabrication Pipeline]() | 🟡 Skeleton |

---

## 🎹 Track 35 — Music Production & Sound Design *(maybe-tier)*

> 8 chapters. From BMX content audio to game soundtracks to AI-generated music. Synthesis, sampling, mixing, mastering, and building custom audio tools — bridging DSP theory (Track 32) and AI experiments (Track 05).

[→ open the syllabus](Subject_Plan) · [→ Music Production learning path](LEARNING_PATH)

| # | Chapter | Status |
|---|---|---|
| 35.1 | [Music Theory for Producers]() | 🟡 Skeleton |
| 35.2 | [Sound Design & Synthesis]() | 🟡 Skeleton |
| 35.3 | [DAW Workflow & Signal Chain]() | 🟡 Skeleton |
| 35.4 | [Sampling, Slicing & Resampling]() | 🟡 Skeleton |
| 35.5 | [Mixing Fundamentals]() | 🟡 Skeleton |
| 35.6 | [Mastering & Loudness]() | 🟡 Skeleton |
| 35.7 | [Audio Programming with JUCE & Python]() | 🟡 Skeleton |
| 35.8 | [Generative Music & AI Audio]() | 🟡 Skeleton |

---

## 🧠 Track 36 — Philosophy of Mind & Consciousness *(maybe-tier)*

> 8 chapters. The philosophical foundation for understanding whether the systems you build could ever be conscious. Bridges neuroscience (Track 11), AI theory (Track 10), and the deepest questions in science.

[→ open the syllabus](Subject_Plan) · [→ Philosophy learning path](LEARNING_PATH)

| # | Chapter | Status |
|---|---|---|
| 36.1 | [The Hard Problem of Consciousness]() | 🟡 Skeleton |
| 36.2 | [Functionalism, Physicalism & Dualism]() | 🟡 Skeleton |
| 36.3 | [Computational Theories of Mind]() | 🟡 Skeleton |
| 36.4 | [Perception, Qualia & Phenomenology]() | 🟡 Skeleton |
| 36.5 | [Free Will, Agency & Causation]() | 🟡 Skeleton |
| 36.6 | [Personal Identity & Continuity]() | 🟡 Skeleton |
| 36.7 | [AI Consciousness & Machine Sentience]() | 🟡 Skeleton |
| 36.8 | [Altered States, Dreams & Non-Ordinary Consciousness]() | 🟡 Skeleton |

---

## 📦 Total Knowledge Base

| Track | Chapters | Chapter KB |
|---|---:|---:|
| 07 Mathematical Foundations & Theoretical Physics (12 sub-subjects) | 94 | 3,339 |
| 01 Python Comprehensive | 16 | 189 |
| 02 C++ | 8 | 195 |
| 03 C# | 8 | 158 |
| 04 Game Development | 8 | 168 |
| 05 AI Experiments | 7 | 126 |
| 05 JavaScript | 8 | 169 |
| 06 Game Design | 8 | 200 |
| 06 TypeScript | 8 | 188 |
| 07 SQL | 8 | 167 |
| 08 App Architectures & Frameworks | 5 | 220 |
| 09 VR & 3D Engineering | 7 | 249 |
| 10 AI & Machine Learning Systems | 7 | 278 |
| 11 Neuroscience & Computational Cognition | 7 | 219 |
| 12 Behavioral Psychology & Reinforcement Learning | 6 | 188 |
| 13 Biomechanics & HCI | 7 | 209 |
| 14 Rust | 8 | 162 |
| 15 Biology | 8 | 169 |
| 16 Chemistry | 8 | 149 |
| 20 3D Modelling (Revit / Fusion / Maya / Blender / SolidWorks / Pipelines) | 8 | ~75 (skeleton) |
| 21 Electronics (circuits → MCUs → motherboards → robotics bridge) | 8 | ~70 (skeleton) |
| 22 Robotics (kinematics → ROS 2 → SLAM → manipulation → humanoids) | 8 | ~80 (skeleton) |
| 23 Holographics (wave optics → CGH → SLMs → light fields → AR → arch-viz) | 8 | ~75 (skeleton) |
| 24 VR Applied (Quest / Vision Pro · OpenXR · MR · arch-viz · business) | 8 | ~75 (skeleton) |
| 25 Cybersecurity (OWASP · WebAuthn · PQC · SLSA · LLM Top 10) | 8 | ~140 (skeleton) |
| 26 DevOps & SRE (CI/CD · IaC · k8s · OTel · SLOs · FinOps) | 8 | ~135 (skeleton) |
| 27 System Design & Distributed Architecture (CAP · caching · queues · APIs · capacity) | 8 | ~130 (skeleton) |
| 28 Cloud Platforms (AWS · GCP · Azure · Cloudflare · indie stack) | 8 | ~135 (skeleton) |
| 29 Compilers & Language Design (lexers · parsers · AST · IR · codegen · JIT) | 8 | ~skeleton |
| 30 Databases & Storage Engines (B-trees · LSM · WAL · MVCC · query planning) | 8 | ~skeleton |
| 31 Networking & Protocols (TCP · TLS · HTTP/2 · QUIC · WebRTC · gRPC) | 8 | ~skeleton |
| 32 Signal Processing & DSP (FFT · filters · MFCCs · audio AI · spectral) | 8 | ~skeleton |
| 33 Business & Entrepreneurship (validation · GTM · fundraising · sales · legal) | 8 | ~skeleton |
| 34 Mechanical Engineering & Fabrication *(maybe-tier)* (CNC · 3D printing · GD&T · CAD-to-fab) | 8 | ~skeleton |
| 35 Music Production & Sound Design *(maybe-tier)* (synthesis · mixing · JUCE · generative AI) | 8 | ~skeleton |
| 36 Philosophy of Mind & Consciousness *(maybe-tier)* (hard problem · functionalism · qualia · AI sentience) | 8 | ~skeleton |
| **Total** | **~349 chapters** | **~7.7 MB+ (textbook + skeleton)** |

---

## 🛠️ Tools, Conventions & Audit

- **Building Apps at Scale (AI-Era Playbook):** [BUILDING_AT_SCALE](BUILDING_AT_SCALE) — practical field guide that points across the curriculum. Reads as one developer to another (not a textbook). Covers AI's strengths/weaknesses for production code, when Docker actually pays off, the Netflix-style failure-domain pattern, the cybersecurity gap AI ghost-writes worst, a concrete 2026 indie/small-team stack, and the four production-engineering tracks (25 Cybersecurity / 26 DevOps & SRE / 27 System Design / 28 Cloud Platforms) that close the gaps it called out.
- **Practice workflow refresher:** [HOW_TO_USE_PRACTICE](HOW_TO_USE_PRACTICE) — the canonical "where does the file land, how do I run a script, what does it look like in Obsidian" doc. Each subject also has its own `README.md` listing its drill scripts with copy-paste commands.
- **Future GUI app vision:** [PRACTICE_GUI_APP_VISION](PRACTICE_GUI_APP_VISION) — Vite + FastAPI + Qt-calculator sidecars for a packaged learning product (planning stage; not yet built).
- **Verification scripts:** [verify_learning_tree.ps1](verify_learning_tree.ps1) (this directory) audits chapter counts and byte sizes across all 7 tracks. The math-only equivalent is `[verify_build.ps1](verify_build.ps1)`.
- **README regeneration:** `[generate_readmes.py](generate_readmes.py)` — re-run any time a new chapter or drill script is added; rewrites all 18 per-subject `README.md` files.
- **SVG render fix:** `[fix_svg_fences.py](fix_svg_fences.py)` — idempotent script that strips ` ```svg ` / ` ```xml ` wrappers from chapter SVGs (Obsidian doesn't render SVG inside code fences). Run it after any new chapter generation if needed.
- **Agent manual:** `[AGENT_MANUAL](AGENT_MANUAL)` — the system rules for any future content generation. Section 3.C explicitly forbids ` ```svg `/` ```xml ` fences inside chapter content.

---

## 🔀 Cross-Track Bridges

A few illustrative cross-links between tracks (the full graph is much denser):

- **Math 02.6 Eigenvalues** ↔ **VR 9.2 Quaternions** ↔ **Biomech 13.5 Sensor Fusion** ↔ **Robotics 22.1 / 22.2 Kinematics** (3D rotation algebra is the same machinery: eigenvalues / quaternions / Kalman state / SE(3))
- **Math 03.4 Systems of Linear ODEs** ↔ **Neuro 11.2 Hodgkin-Huxley** ↔ **Control 11 (Math)** ↔ **Robotics 22.4 Motor Control** (the same dynamical-systems toolbox)
- **AI 10.7 RLHF** ↔ **Psych 12.6 RLHF** ↔ **Neuro 11.6 Dopamine** ↔ **Robotics 22.7 / 22.8 VLA models** (one topic, four lenses: algorithm, behavior, biology, embodied)
- **Math 04.1 Newtonian Conservation Laws** ↔ **Math 04.7 Rigid Body** ↔ **Biomech 13.2 BMX Rotational Dynamics** (the same physics, applied to a 360 backflip)
- **VR 9.1 3D Math** ↔ **AI 10.3 CNNs** ↔ **3D Modelling 20.1 Foundations** (image plane geometry, projection, equivariance)
- **3D Modelling 20.8** ↔ **Holographics 23.7 / 23.8** ↔ **VR 24.6 / 24.8** (one unified spatial-computing-for-architects business — three delivery formats)
- **Electromagnetism (Math/Phys 07.07)** ↔ **Electronics 21.x** ↔ **Holographics 23.1 / 23.4** (Maxwell underneath all of circuits + light + modulators)
- **Electronics 21.5–21.8** ↔ **Robotics 22.3 / 22.4 / 22.5** (microcontrollers + buses are the prerequisite layer for any robotics stack)
- **Track 21.6 (Motherboards)** ↔ **Track 28.2 (Compute Primitives)** (the same hardware story — silicon up to cloud VMs / GPU clouds — viewed from electron level then from rented-by-the-hour level)
- **Track 22.5 (ROS 2 / DDS)** ↔ **Track 27.4 (Message Queues & Event-Driven Architecture)** (publish/subscribe is one pattern with two domains — robotics middleware and distributed-systems messaging share the same shape, including back-pressure, QoS, and at-least-once delivery)
- **Track 23.7 + 24.6 + 27.6 + 28.7** spatial-computing-as-a-business stack (architectural visualization → applied VR → microservice decomposition for a paid product → multi-cloud/edge delivery for global clients)
- **Track 25.5 (Secure SDLC)** ↔ **Track 26.1 (CI/CD)** ↔ **Track 26.3 (Containers)** (Sigstore / SLSA provenance, SAST/DAST gates, signed images — three lenses on the same supply-chain pipeline)
- **Track 25.7 (Cloud & Container Security)** ↔ **Track 26.3 (k8s Pod Security)** ↔ **Track 28.5 (IAM)** (least-privilege identity through three layers: workload, orchestrator, organization)
- **Track 25.8 (AI Security)** ↔ **Track 10.5 (Transformers / LLMs)** ↔ **Track 05.5 (Agentic AI)** (prompt injection, tool-call abuse, MCP threats — the security counterpart to the LLM-systems and agent-experiments tracks)
- **Track 27.1 (CAP/PACELC)** ↔ **Track 27.3 (Databases at Scale)** ↔ **Track 28.3 (Managed DBs)** (theoretical limits → architectural patterns → which managed product on which cloud actually implements them)
- **BUILDING_AT_SCALE §5–§10** ↔ **Tracks 25 / 26 / 27 / 28** (the playbook explicitly named the gaps; these four tracks fill them)

---

*Curriculum architect: Bill — Mathematical Foundations, Theoretical Physics, Applied Engineering, AI/ML, and Bio-systems. All notes are private, original derivations.*

---

## Related Notes
- [Subject_Plan](Subject_Plan) - Shared curriculum/navigation focus
- [LEARNING_PATH](LEARNING_PATH) - Same Learning folder
- [Learning for game devel](Learning-for-game-devel) - Same Learning folder
- [Math for Learning AI](Math-for-Learning-AI) - Same Learning folder
- [VR & Game Dev Learning Roadmap](VR-&-Game-Dev-Learning-Roadmap) - Same Learning folder
