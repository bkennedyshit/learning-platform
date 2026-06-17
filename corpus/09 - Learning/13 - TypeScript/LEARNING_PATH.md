---
date: 2026-05-24
title: "TypeScript — Learning Path"
mission: "Structured progression from JS-aware Python developer to job-ready TypeScript engineer"
status: active
tags: [typescript, learning-path, career, progression]
type: learning-path
track: 06
---

*Back to [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/13 - TypeScript/Subject_Plan]] | Part of [[09 - Learning Index]]*

# 🛤️ TypeScript — Learning Path

> *"The best way to learn TypeScript is to write TypeScript. The second best way is to read TypeScript error messages."* — **Matt Pocock**

---

## 📋 Prerequisites

Before starting this track, you should have:

| Prerequisite | Status Check | If Missing |
|---|---|---|
| Python comfort (functions, classes, modules) | Can you write a class with `__init__`, use list comprehensions, handle exceptions? | Complete [[08.3 - OOP, Data Models & Pythonic Idioms]] first |
| JavaScript basics (variables, functions, DOM) | Can you explain `let` vs `const`, arrow functions, `this` binding? | Refresh via [[Track 05 JavaScript]] or MDN's [JS Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide) (2–3 days) |
| Terminal/CLI comfort | Can you navigate directories, run scripts, install packages? | You're fine — you use Python daily |
| Node.js installed | `node --version` returns 20+? | Install via [fnm](https://github.com/Schniz/fnm) or [nvm-windows](https://github.com/coreybutler/nvm-windows) |

**Time investment:** ~6–8 weeks at 2 hours/day (60–75 total hours)

---

## 🗺️ The Path

### Phase 1 — Foundation (Weeks 1–2)

**Goal:** Configure projects confidently, think in types instead of runtime checks.

```
┌─────────────────────────────────────────────────────────┐
│  13.1 Setup & Project Structure          [4-5 hrs]       │
│  ├── Install TS, configure tsconfig.json                │
│  ├── Understand strict mode (why it's non-negotiable)   │
│  ├── Set up ESLint + Prettier for TS                    │
│  └── Create your first monorepo structure               │
│                                                         │
│  13.2 Type System Core                   [8-10 hrs]      │
│  ├── Primitives, literals, enums                        │
│  ├── Unions, intersections, type aliases vs interfaces  │
│  ├── Generics: constraints, defaults, inference         │
│  ├── Type guards and narrowing                          │
│  └── Utility types: Partial, Required, Pick, Omit      │
└─────────────────────────────────────────────────────────┘
```

**Milestone:** You can type a medium-complexity function with generics and the compiler catches your mistakes before runtime.

**Python parallel:** This is like going from untyped Python to fully-annotated Python with `mypy --strict` — except TS enforces it at compile time, not as an optional linter.

---

### Phase 2 — Type-Level Programming (Week 3)

**Goal:** Read and write advanced type signatures. Understand library types.

```
┌─────────────────────────────────────────────────────────┐
│  13.3 Advanced Types                     [10-12 hrs]     │
│  ├── Conditional types (extends ? true : false)         │
│  ├── infer keyword (extract types from structures)      │
│  ├── Mapped types (transform object shapes)             │
│  ├── Template literal types (string manipulation)       │
│  ├── Recursive types (JSON, nested structures)          │
│  ├── Branded/opaque types (nominal typing in TS)        │
│  └── Distributive conditional types                     │
└─────────────────────────────────────────────────────────┘
```

**Milestone:** You can solve medium type-challenges on GitHub. You can read `type-fest` source code and understand what it does.

**Python parallel:** This is like Python's `TypeVar`, `ParamSpec`, and `Protocol` — but TS takes it 10x further because the type system is Turing-complete.

---

### Phase 3 — Patterns & Async (Week 4)

**Goal:** Write idiomatic TS using both OOP and FP paradigms. Master async patterns.

```
┌─────────────────────────────────────────────────────────┐
│  13.4 OOP & FP Patterns                  [8-10 hrs]      │
│  ├── Classes, abstract classes, implements              │
│  ├── Discriminated unions (the TS way to do ADTs)       │
│  ├── FP: pipe, compose, Option/Result patterns          │
│  ├── Effect.ts introduction                             │
│  └── When to use classes vs functions vs objects        │
│                                                         │
│  13.5 Async Patterns                     [6-8 hrs]       │
│  ├── Promise<T> typing, async/await                     │
│  ├── Error handling: Result types vs try/catch          │
│  ├── Async generators and iterables                     │
│  ├── AbortController and cancellation                   │
│  └── Concurrent patterns: Promise.all, allSettled, race │
└─────────────────────────────────────────────────────────┘
```

**Milestone:** You can architect a service layer with proper error handling, typed async flows, and clean separation of concerns.

---

### Phase 4 — Build Systems & Frontend (Weeks 5–6)

**Goal:** Ship typed frontend applications with modern frameworks.

```
┌─────────────────────────────────────────────────────────┐
│  13.6 Modules & Build Systems            [5-6 hrs]       │
│  ├── ESM vs CJS (the great divide)                     │
│  ├── Bundlers: Vite, esbuild, Rollup, webpack          │
│  ├── Monorepo tooling: Turborepo, Nx, pnpm workspaces  │
│  └── Publishing typed packages                          │
│                                                         │
│  13.7 Frontend Frameworks                [10-12 hrs]     │
│  ├── React + TypeScript (hooks, generics, RSC)          │
│  ├── Vue 3 + <script setup lang="ts">                  │
│  ├── Svelte 5 runes + TypeScript                        │
│  ├── SolidJS signals + TypeScript                       │
│  └── Shared patterns: typed props, events, stores       │
└─────────────────────────────────────────────────────────┘
```

**Milestone:** You can scaffold a typed React/Next.js app from scratch, or pick up any framework's TS integration quickly.

---

### Phase 5 — Backend & Integration (Weeks 6–7)

**Goal:** Build type-safe APIs and full-stack applications.

```
┌─────────────────────────────────────────────────────────┐
│  13.8 Backend Frameworks                 [10-12 hrs]     │
│  ├── Node.js + Express (typed middleware, routes)       │
│  ├── Fastify (schema-first, fastest Node framework)    │
│  ├── Bun + Hono (modern, fast, edge-ready)             │
│  ├── Deno (permissions model, built-in TS)             │
│  ├── tRPC (end-to-end type safety)                     │
│  └── Database: Prisma, Drizzle ORM                     │
└─────────────────────────────────────────────────────────┘
```

**Milestone:** You can build a full-stack typed API with validation, error handling, and database access.

---

### Phase 6 — Interview Prep (Week 8)

**Goal:** Solve coding problems in TypeScript fluently.

```
┌─────────────────────────────────────────────────────────┐
│  Reference Appendix                                     │
│  [[TypeScript Essentials for Coding Tests]]             │
│  ├── Data structures in TS                              │
│  ├── Algorithm patterns with proper typing              │
│  ├── Common interview patterns                          │
│  └── Time/space complexity with TS idioms               │
└─────────────────────────────────────────────────────────┘
```

**Milestone:** You can solve LeetCode mediums in TypeScript within 25 minutes.

---

## 🎯 Competency Checkpoints

After each phase, verify you can do these without looking anything up:

| Phase | Can You... |
|-------|-----------|
| 1 | Write a generic function with constraints? Explain `unknown` vs `any`? |
| 2 | Write a `DeepPartial<T>` type from scratch? Explain distributive conditionals? |
| 3 | Implement a Result monad? Type an event emitter with discriminated unions? |
| 4 | Configure Vite for a TS monorepo? Explain ESM vs CJS interop issues? |
| 5 | Type a React custom hook that returns a tuple? Use `satisfies` correctly? |
| 6 | Build a typed REST API with validation? Explain tRPC's type inference? |

---

## 🔄 Daily Practice Routine (2 hrs)

| Block | Duration | Activity |
|-------|----------|----------|
| Warm-up | 15 min | 1–2 type-challenges (easy/medium) |
| Study | 45 min | Read chapter section, take notes |
| Build | 45 min | Code along, modify examples, break things |
| Review | 15 min | Re-read error messages you hit, note patterns |

---

## 🔗 Navigation

- **Subject Plan:** [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/13 - TypeScript/Subject_Plan]]
- **First Chapter:** [[13.1 - Setup, Compilation & Project Structure]]
- **Interview Prep:** [[TypeScript Essentials for Coding Tests]]
- **Related Tracks:** [[Track 05 JavaScript]] | [[22.1 - React & Next.js - Functional Components & Hooks]]

---

*Last updated: 2026-05-24*

---

## Related Notes
- [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/13 - TypeScript/Subject_Plan]] - Shared typescript/career focus
- [[13.2 - Type System - Primitives, Unions, Intersections, Generics]] - Same TypeScript folder
- [[13.3 - Advanced Types - Conditional, Mapped, Template Literal Types]] - Same TypeScript folder
