---
title: "13.1 — Setup, Compilation & Project Structure"
subject: "TypeScript"
catalog: advanced
audience_tier: higher-education
chapter: "13.1"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 13.1 — Setup, Compilation & Project Structure

> *"Strict mode is not a punishment. It's a gift. Every error it catches at compile time is a bug you'll never ship to production."* — **Ryan Cavanaugh**, TypeScript Engineering Lead

You already know how to write JavaScript. TypeScript adds a compilation step that catches errors before your code ever runs. This chapter gets your environment configured correctly from day one — because a misconfigured `tsconfig.json` will silently let bugs through, defeating the entire purpose.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Install TypeScript via multiple runtimes (Node/npm, Bun, Deno) and explain the tradeoffs.
2. Configure `tsconfig.json` with strict mode and understand every flag that matters.
3. Explain the TypeScript compilation pipeline: source → AST → type-checking → emit.
4. Set up a monorepo with shared types using `pnpm workspaces` + `tsconfig` project references.
5. Configure ESLint + Prettier for TypeScript with zero-config presets.
6. Use the TypeScript Playground and VS Code IntelliSense as learning tools.

---

## 🖼️ Visual Anchor — TypeScript Compilation Pipeline

![ts__6.1-fig1](ts__6.1-fig1.svg)

---

## 📚 1. Concepts & Definitions

### Definition 13.1.1 — TypeScript

TypeScript is a **statically-typed superset of JavaScript** created by Anders Hejlsberg at Microsoft (2012). Every valid JavaScript file is valid TypeScript — TS adds optional type annotations that are checked at compile time and then **erased** (they produce no runtime code).

**Key insight for Python devs:** Think of TypeScript as what you'd get if `mypy` were mandatory, built into the language, and the type system were 10x more powerful. Python's type hints are optional and checked by external tools. TypeScript's types are checked by the compiler itself.

### Definition 13.1.2 — The Compiler (`tsc`)

`tsc` is the TypeScript compiler. It does three things:
1. **Parses** `.ts`/`.tsx` files into an Abstract Syntax Tree (AST)
2. **Type-checks** the AST against your type annotations and inferred types
3. **Emits** JavaScript (`.js`) files with all type annotations stripped

```bash
# Compile a single file
tsc hello.ts          # → hello.js

# Compile a project (uses tsconfig.json)
tsc                   # → outputs to outDir

# Type-check only (no emit) — fast CI check
tsc --noEmit
```

### Definition 13.1.3 — `tsconfig.json`

The project configuration file. Controls what gets compiled, how strict the type-checking is, and what JavaScript version to target. This is your most important file.

### Definition 13.1.4 — Strict Mode

`"strict": true` enables ALL strict type-checking flags simultaneously. It's a meta-flag that turns on:

| Flag | What it does |
|------|-------------|
| `strictNullChecks` | `null` and `undefined` are not assignable to other types |
| `strictFunctionTypes` | Function parameter types are checked contravariantly |
| `strictBindCallApply` | `bind`, `call`, `apply` are correctly typed |
| `strictPropertyInitialization` | Class properties must be initialized |
| `noImplicitAny` | Error on expressions with implied `any` type |
| `noImplicitThis` | Error on `this` with implied `any` type |
| `alwaysStrict` | Emit `"use strict"` in every file |
| `useUnknownInCatchVariables` | `catch(e)` gives `e: unknown` not `e: any` |

**Non-negotiable rule:** Always use `"strict": true`. Starting without it and adding it later is painful — you'll have hundreds of errors to fix. Start strict, stay strict.

### Definition 13.1.5 — Type Erasure

TypeScript types exist **only at compile time**. After compilation, all type annotations, interfaces, and type aliases are completely removed. The runtime JavaScript has zero knowledge of your types.

```ts
// TypeScript source
function greet(name: string): string {
  return `Hello, ${name}`;
}

// Compiled JavaScript (types erased)
function greet(name) {
  return `Hello, ${name}`;
}
```

This means:
- You cannot check types at runtime (no `instanceof` for interfaces)
- Types have zero performance cost at runtime
- You need runtime validation (Zod, Valibot) for external data (API responses, user input)

### Definition 13.1.6 — Declaration Files (`.d.ts`)

Declaration files contain **only type information** — no implementation. They're how TypeScript understands JavaScript libraries that weren't written in TypeScript.

```ts
// lodash.d.ts (simplified)
declare function chunk<T>(array: T[], size: number): T[][];
declare function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): T;
```

The `@types/*` packages on npm (e.g., `@types/node`, `@types/react`) are community-maintained declaration files.

---

## 🧩 2. Mental Models

### Model 6.1.1 — TypeScript as a Linter on Steroids

Don't think of TypeScript as a different language. Think of it as **JavaScript + the world's most sophisticated linter**. The linter (type checker) runs at compile time, catches bugs, and then gets out of the way — your shipped code is plain JavaScript.

```
Python analogy:
  Python + mypy --strict ≈ TypeScript (but TS is mandatory, not optional)
  
  Python: runtime errors when types mismatch
  TypeScript: compile-time errors when types mismatch
  JavaScript: runtime errors... eventually... maybe... in production
```

### Model 6.1.2 — The Three Runtimes

TypeScript doesn't run directly. It needs a runtime. You have three choices:

| Runtime | How TS runs | Speed | Ecosystem |
|---------|------------|-------|-----------|
| **Node.js** | Compile with `tsc` → run `.js` with `node` | Standard | Largest (npm) |
| **Bun** | Runs `.ts` directly (strips types, no check) | Fastest | npm-compatible |
| **Deno** | Runs `.ts` directly (type-checks built-in) | Fast | npm + deno.land |

**Recommendation:** Install all three. Use **Bun** for fast iteration during development. Use **tsc --noEmit** for type-checking in CI. Use **Node** for production (most battle-tested).

### Model 6.1.3 — Project References = Python Packages

In Python, you split code into packages with `__init__.py`. In TypeScript monorepos, you split code into **project references** — each sub-project has its own `tsconfig.json` and can be compiled independently.

```
monorepo/
├── packages/
│   ├── shared/          ← shared types & utilities
│   │   ├── src/
│   │   └── tsconfig.json
│   ├── frontend/        ← React app
│   │   ├── src/
│   │   └── tsconfig.json  (references: [shared])
│   └── backend/         ← API server
│       ├── src/
│       └── tsconfig.json  (references: [shared])
├── tsconfig.json        ← root (references all packages)
└── pnpm-workspace.yaml
```

---

## 🔑 3. Mechanics

### 3.1 — Installation

```bash
# Option A: Node.js + npm (traditional)
npm init -y
npm install -D typescript @types/node
npx tsc --init                    # generates tsconfig.json

# Option B: Bun (modern, fast)
bun init                          # creates tsconfig.json automatically
# Bun runs .ts files directly — no compile step needed for dev

# Option C: Deno (batteries-included)
deno init                         # creates deno.json
# Deno runs .ts natively with built-in type checking
```

### 3.2 — The Production `tsconfig.json`

```jsonc
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    // ─── Type Checking (THE IMPORTANT PART) ───────────────────
    "strict": true,                    // ALL strict checks ON
    "noUncheckedIndexedAccess": true,  // array[i] returns T | undefined
    "noUnusedLocals": true,            // error on unused variables
    "noUnusedParameters": true,        // error on unused params
    "exactOptionalPropertyTypes": true,// undefined ≠ missing property
    "noFallthroughCasesInSwitch": true,// must break/return in switch

    // ─── Module System ────────────────────────────────────────
    "module": "ESNext",                // use ES modules
    "moduleResolution": "bundler",     // modern resolution (Node16+ or bundler)
    "resolveJsonModule": true,         // import JSON files
    "esModuleInterop": true,           // CJS/ESM interop
    "isolatedModules": true,           // required for bundlers (Vite, esbuild)
    "verbatimModuleSyntax": true,      // explicit import/export type

    // ─── Emit ─────────────────────────────────────────────────
    "target": "ES2022",                // modern JS output
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "outDir": "./dist",
    "declaration": true,               // emit .d.ts files
    "declarationMap": true,            // source maps for .d.ts
    "sourceMap": true,                 // .js.map for debugging

    // ─── Path Aliases ─────────────────────────────────────────
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]               // import from "@/utils/foo"
    },

    // ─── Interop ──────────────────────────────────────────────
    "skipLibCheck": true,              // skip checking node_modules .d.ts
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*.ts", "src/**/*.tsx"],
  "exclude": ["node_modules", "dist"]
}
```

### 3.3 — Key Flags Explained (The Ones That Matter)

**`noUncheckedIndexedAccess`** — The most underrated flag:

```ts
const arr = [1, 2, 3];

// Without noUncheckedIndexedAccess:
const val = arr[5]; // type: number (LIE — it's undefined!)

// With noUncheckedIndexedAccess:
const val = arr[5]; // type: number | undefined (TRUTH)
if (val !== undefined) {
  console.log(val * 2); // Now safe
}
```

**`verbatimModuleSyntax`** — Forces explicit type imports:

```ts
// Must use `import type` for type-only imports
import type { User } from "./types";  // ✅ erased at compile time
import { createUser } from "./users"; // ✅ kept at runtime

// Without this flag, TS guesses — and sometimes guesses wrong
import { User } from "./types";       // ❌ error with verbatimModuleSyntax
```

### 3.4 — Project Structure (Single App)

```
my-app/
├── src/
│   ├── index.ts           ← entry point
│   ├── types/
│   │   └── index.ts       ← shared type definitions
│   ├── utils/
│   │   └── validation.ts
│   ├── services/
│   │   └── api.ts
│   └── __tests__/
│       └── validation.test.ts
├── tsconfig.json
├── package.json
├── .eslintrc.cjs
└── .prettierrc
```

### 3.5 — Monorepo Structure (pnpm Workspaces)

```yaml
# pnpm-workspace.yaml
packages:
  - "packages/*"
  - "apps/*"
```

```
monorepo/
├── apps/
│   ├── web/                    ← Next.js frontend
│   │   ├── src/
│   │   ├── tsconfig.json       ← extends ../../tsconfig.base.json
│   │   └── package.json
│   └── api/                    ← Hono backend
│       ├── src/
│       ├── tsconfig.json
│       └── package.json
├── packages/
│   ├── shared/                 ← shared types & utils
│   │   ├── src/
│   │   │   ├── types.ts
│   │   │   └── index.ts
│   │   ├── tsconfig.json
│   │   └── package.json        ← "name": "@myapp/shared"
│   └── ui/                     ← shared UI components
│       ├── src/
│       ├── tsconfig.json
│       └── package.json        ← "name": "@myapp/ui"
├── tsconfig.base.json          ← shared compiler options
├── pnpm-workspace.yaml
├── turbo.json                  ← Turborepo task orchestration
└── package.json                ← root scripts
```

Root `tsconfig.base.json`:
```jsonc
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  }
}
```

Package `tsconfig.json` extends it:
```jsonc
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*.ts"],
  "references": [
    { "path": "../shared" }
  ]
}
```

### 3.6 — ESLint + Prettier Setup

```bash
# Install (using pnpm)
pnpm add -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
pnpm add -D prettier eslint-config-prettier
```

Minimal `.eslintrc.cjs`:
```js
module.exports = {
  root: true,
  parser: "@typescript-eslint/parser",
  parserOptions: {
    project: "./tsconfig.json",
  },
  plugins: ["@typescript-eslint"],
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/strict-type-checked",
    "plugin:@typescript-eslint/stylistic-type-checked",
    "prettier", // must be last — disables formatting rules
  ],
  rules: {
    "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
    "@typescript-eslint/consistent-type-imports": "error",
  },
};
```

### 3.7 — VS Code Configuration

Essential extensions:
- **TypeScript** (built-in) — IntelliSense, go-to-definition, rename
- **Pretty TypeScript Errors** — human-readable error messages
- **Error Lens** — inline error display
- **ESLint** — linting integration

`.vscode/settings.json`:
```jsonc
{
  "typescript.preferences.importModuleSpecifier": "non-relative",
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "explicit"
  }
}
```

---

## 💻 4. Code Patterns & Examples

### Pattern 6.1.1 — Your First TypeScript File

```ts
// src/index.ts
// TypeScript infers types when possible, but explicit annotations
// serve as documentation and catch mistakes at boundaries.

// Explicit parameter types, inferred return type
function add(a: number, b: number) {
  return a + b; // TS infers return type: number
}

// Explicit return type (recommended for exported functions)
export function greet(name: string): string {
  return `Hello, ${name}!`;
}

// Object type with interface
interface User {
  id: number;
  name: string;
  email: string;
  createdAt: Date;
}

// Function using the interface
function formatUser(user: User): string {
  return `${user.name} (${user.email})`;
}

// Arrays
const numbers: number[] = [1, 2, 3];
const users: User[] = [];

// Type error examples (uncomment to see errors):
// add("1", 2);           // Error: Argument of type 'string' is not assignable to 'number'
// greet(42);             // Error: Argument of type 'number' is not assignable to 'string'
// const bad: User = {};  // Error: Missing properties: id, name, email, createdAt
```

### Pattern 6.1.2 — Running TypeScript (Three Ways)

```bash
# Method 1: tsc + node (traditional)
npx tsc src/index.ts --outDir dist
node dist/index.js

# Method 2: Bun (instant, no compile step)
bun run src/index.ts

# Method 3: tsx (Node wrapper, fast)
npx tsx src/index.ts

# Method 4: Deno
deno run src/index.ts
```

### Pattern 6.1.3 — Scripts in `package.json`

```jsonc
{
  "scripts": {
    "dev": "tsx watch src/index.ts",       // hot-reload during development
    "build": "tsc",                         // compile for production
    "start": "node dist/index.js",          // run compiled output
    "check": "tsc --noEmit",                // type-check only (CI)
    "lint": "eslint src/ --ext .ts,.tsx",
    "format": "prettier --write src/"
  }
}
```

### Pattern 6.1.4 — Path Aliases in Practice

```ts
// Without path aliases (fragile, ugly)
import { validateEmail } from "../../../utils/validation";
import type { User } from "../../../types";

// With path aliases (@/* → src/*)
import { validateEmail } from "@/utils/validation";
import type { User } from "@/types";
```

Note: Path aliases in `tsconfig.json` only tell the **type checker** about the mapping. Your bundler (Vite, webpack) or runtime (tsx, Bun) also needs to know. Vite handles this automatically via `vite-tsconfig-paths`.

---

## 🧮 5. Worked Examples

### Example 13.1.1 — Set Up a New Project from Scratch

**Task:** Create a TypeScript project with strict mode, path aliases, and a basic folder structure.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```bash
# 1. Create project directory
mkdir my-ts-project && cd my-ts-project

# 2. Initialize package.json
pnpm init

# 3. Install TypeScript and Node types
pnpm add -D typescript @types/node tsx

# 4. Generate tsconfig.json
npx tsc --init

# 5. Create folder structure
mkdir -p src/{types,utils,services,__tests__}
touch src/index.ts src/types/index.ts
```

Then replace the generated `tsconfig.json` with the production config from Section 3.2.

Create `src/index.ts`:
```ts
import type { AppConfig } from "@/types";

const config: AppConfig = {
  port: 3000,
  env: "development",
};

console.log(`Starting server on port ${config.port}`);
```

Create `src/types/index.ts`:
```ts
export interface AppConfig {
  port: number;
  env: "development" | "production" | "test";
}
```

Add scripts to `package.json`:
```jsonc
{
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "check": "tsc --noEmit"
  }
}
```

Test it:
```bash
pnpm check   # should pass with no errors
pnpm dev     # should print "Starting server on port 3000"
```

</details>

### Example 13.1.2 — Configure a Monorepo with Shared Types

**Task:** Set up a pnpm monorepo where a `shared` package exports types used by both `web` and `api` apps.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```bash
# 1. Create structure
mkdir my-monorepo && cd my-monorepo
pnpm init

# 2. Create workspace config
cat > pnpm-workspace.yaml << 'EOF'
packages:
  - "packages/*"
  - "apps/*"
EOF

# 3. Create shared package
mkdir -p packages/shared/src
cd packages/shared
pnpm init
# Edit package.json: "name": "@myapp/shared"
```

`packages/shared/src/types.ts`:
```ts
export interface User {
  id: string;
  email: string;
  name: string;
  role: "admin" | "user" | "guest";
}

export interface ApiResponse<T> {
  data: T;
  error: string | null;
  timestamp: number;
}
```

`packages/shared/src/index.ts`:
```ts
export type { User, ApiResponse } from "./types";
```

`packages/shared/tsconfig.json`:
```jsonc
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*.ts"]
}
```

`packages/shared/package.json`:
```jsonc
{
  "name": "@myapp/shared",
  "version": "0.0.1",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "scripts": {
    "build": "tsc"
  }
}
```

Now in `apps/api/src/index.ts`:
```ts
import type { User, ApiResponse } from "@myapp/shared";

function getUser(id: string): ApiResponse<User> {
  return {
    data: { id, email: "bill@example.com", name: "Bill", role: "admin" },
    error: null,
    timestamp: Date.now(),
  };
}
```

Install the workspace dependency:
```bash
cd apps/api
pnpm add @myapp/shared --workspace
```

</details>

### Example 13.1.3 — Migrate a JavaScript File to TypeScript

**Task:** Take an existing `.js` file and convert it to strict TypeScript.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

Original `utils.js`:
```js
function fetchUser(id) {
  return fetch(`/api/users/${id}`)
    .then(res => res.json())
    .then(data => ({
      name: data.name,
      email: data.email,
      isActive: data.status === "active"
    }));
}

function formatCurrency(amount, currency) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: currency || "USD"
  }).format(amount);
}
```

Converted `utils.ts`:
```ts
// Step 1: Define the shapes of data
interface UserApiResponse {
  name: string;
  email: string;
  status: "active" | "inactive" | "suspended";
}

interface FormattedUser {
  name: string;
  email: string;
  isActive: boolean;
}

// Step 2: Add parameter and return types
async function fetchUser(id: string): Promise<FormattedUser> {
  const res = await fetch(`/api/users/${id}`);

  if (!res.ok) {
    throw new Error(`Failed to fetch user ${id}: ${res.status}`);
  }

  const data: UserApiResponse = await res.json();

  return {
    name: data.name,
    email: data.email,
    isActive: data.status === "active",
  };
}

// Step 3: Use union types for constrained parameters
type CurrencyCode = "USD" | "EUR" | "GBP" | "CAD";

function formatCurrency(amount: number, currency: CurrencyCode = "USD"): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
  }).format(amount);
}

export { fetchUser, formatCurrency };
export type { FormattedUser, CurrencyCode };
```

Key changes:
1. Added explicit types for all parameters and return values
2. Used `async/await` instead of `.then()` chains (cleaner with TS)
3. Added error handling (strict mode forces you to think about failure cases)
4. Used union types (`CurrencyCode`) instead of bare `string`
5. Separated type exports with `export type`

</details>

---

## ⚠️ 6. Gotchas & Anti-Patterns

### Gotcha 6.1.1 — Starting Without Strict Mode

```ts
// tsconfig.json with "strict": false (DON'T DO THIS)
function processUser(user) {  // user is implicitly 'any' — no type safety!
  return user.name.toUpperCase(); // No error even if user is null
}
// This defeats the entire purpose of TypeScript.
```

**Fix:** Always `"strict": true`. If migrating a large JS codebase, use `// @ts-expect-error` on specific lines rather than disabling strict globally.

### Gotcha 6.1.2 — Confusing `tsc` Emit with Bundler Emit

```bash
# Common mistake: using tsc as your build tool for a web app
tsc  # Produces individual .js files — NOT a bundle!

# What you actually want for web apps:
vite build    # Uses esbuild/Rollup to bundle, tsc only for type-checking
```

**Rule of thumb:**
- **Libraries:** Use `tsc` to emit (produces `.js` + `.d.ts`)
- **Applications:** Use a bundler (Vite, esbuild) to emit; use `tsc --noEmit` for type-checking only

### Gotcha 6.1.3 — `any` Leaking Through `@types` Packages

Some `@types/*` packages have loose types. Even with strict mode, `any` can sneak in:

```ts
import express from "express";

app.get("/users", (req, res) => {
  const id = req.query.id; // type: string | ParsedQs | ... | undefined
  // But req.body is 'any' by default in Express!
  const name = req.body.name; // No error — body is any!
});
```

**Fix:** Use Zod/Valibot to validate `req.body` at runtime, or use Fastify/Hono which have built-in schema validation with type inference.

### Gotcha 6.1.4 — Path Aliases Without Bundler Support

```jsonc
// tsconfig.json
{ "paths": { "@/*": ["./src/*"] } }
```

This tells `tsc` about the alias, but:
- `node` doesn't understand `@/` imports
- You need `tsx` (which reads tsconfig paths) or a bundler plugin

**Fix:** Use `tsx` for development, and ensure your bundler has path resolution configured (Vite does this automatically with `vite-tsconfig-paths`).

### Gotcha 6.1.5 — `skipLibCheck: true` Hiding Real Errors

`skipLibCheck` skips type-checking `.d.ts` files in `node_modules`. This speeds up compilation but can hide errors in your own `.d.ts` files or in packages with broken types.

**Recommendation:** Keep `skipLibCheck: true` (the speed gain is worth it), but if you get mysterious runtime errors, temporarily set it to `false` to check if a dependency has type issues.

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- **Next chapter:** [13.2 - Type System - Primitives, Unions, Intersections, Generics](13.2---Type-System---Primitives,-Unions,-Intersections,-Generics)
- **Modules deep-dive:** [13.6 - Modules & Build Systems](13.6---Modules-&-Build-Systems)
- **Python comparison:** [08.3 - OOP, Data Models & Pythonic Idioms](08.3---OOP,-Data-Models-&-Pythonic-Idioms) — structural typing parallels

### External Resources
- [TypeScript Handbook — tsconfig Reference](https://www.typescriptlang.org/tsconfig)
- [Total TypeScript — Project Setup](https://www.totaltypescript.com/tutorials/beginners-typescript)
- [Matt Pocock — TSConfig Cheat Sheet](https://www.totaltypescript.com/tsconfig-cheat-sheet)
- [Turborepo — Getting Started](https://turbo.build/repo/docs)
- [pnpm Workspaces](https://pnpm.io/workspaces)

---

*Last updated: 2026-05-24*



---

## 🏗️ 8. Monorepo Architecture & Advanced Build Tooling

### 8.1 — Turborepo + tsconfig Project References

A production monorepo combines **Turborepo** for task orchestration with **TypeScript project references** for incremental type-checking. This gives you both fast builds and correct cross-package type safety.

#### The Project References Graph

TypeScript project references (`composite: true` + `references: [...]`) create a DAG (directed acyclic graph) of compilation units. The compiler can:
1. Skip re-checking packages whose inputs haven't changed
2. Use `.d.ts` outputs from referenced projects instead of re-parsing source
3. Detect circular dependencies at configuration time

```json
// tsconfig.base.json (root)
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "composite": true,
    "incremental": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "forceConsistentCasingInFileNames": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

```json
// packages/shared/tsconfig.json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src",
    "tsBuildInfoFile": "./dist/.tsbuildinfo"
  },
  "include": ["src/**/*.ts"]
}
```

```json
// apps/api/tsconfig.json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src",
    "tsBuildInfoFile": "./dist/.tsbuildinfo"
  },
  "include": ["src/**/*.ts"],
  "references": [
    { "path": "../../packages/shared" },
    { "path": "../../packages/db" }
  ]
}
```

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["tsconfig.base.json"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"],
      "inputs": ["src/**/*.ts", "tsconfig.json"]
    },
    "check": {
      "dependsOn": ["^build"],
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "outputs": []
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    }
  }
}
```

#### How Turborepo Cache Hashing Works

Turborepo computes a hash for each task based on:
1. **File inputs** — all files matching the `inputs` glob (defaults to all tracked files)
2. **Environment variables** — any listed in `globalEnv` or task-level `env`
3. **Dependency task outputs** — hashes of upstream `^build` outputs
4. **Lock file state** — changes to `pnpm-lock.yaml` invalidate all caches
5. **Framework inference** — Turbo auto-detects Next.js, Vite, etc. and adds relevant env vars

```bash
# First run: builds everything
turbo build
# ✅ packages/shared: cache miss — building
# ✅ packages/db: cache miss — building
# ✅ apps/api: cache miss — building

# Second run (no changes): instant
turbo build
# ✅ packages/shared: cache hit — replaying output
# ✅ packages/db: cache hit — replaying output
# ✅ apps/api: cache hit — replaying output
# Total: 47ms (vs 12s uncached)
```

#### Remote Caching

```bash
# Enable Vercel Remote Cache (team-wide)
npx turbo login
npx turbo link

# Now CI and all team members share the same cache
# If Alice built packages/shared, Bob gets a cache hit instantly
```

### 8.2 — Build Tool Benchmarks: tsup vs tsc vs swc vs esbuild

| Tool | What It Does | Speed (1000 files) | Output | Type Checking |
|------|-------------|--------------------|---------|----|
| `tsc` | Official compiler | ~8-12s | `.js` + `.d.ts` | ✅ Full |
| `esbuild` | Go-based bundler | ~0.1-0.3s | Bundle | ❌ None |
| `swc` | Rust-based compiler | ~0.2-0.5s | `.js` files | ❌ None |
| `tsup` | esbuild wrapper | ~0.3-0.8s | Bundle + `.d.ts` | ⚠️ DTS only |

#### When to Use Each

**`tsc` — Libraries that need `.d.ts` generation with full fidelity:**
```json
{
  "scripts": {
    "build": "tsc --project tsconfig.build.json",
    "check": "tsc --noEmit"
  }
}
```

**`tsup` — Libraries that need fast builds + bundled output:**
```ts
// tsup.config.ts
import { defineConfig } from "tsup";

export default defineConfig({
  entry: ["src/index.ts"],
  format: ["esm", "cjs"],
  dts: true,
  splitting: true,
  sourcemap: true,
  clean: true,
  treeshake: true,
  minify: false,
  target: "es2022",
  outDir: "dist",
  external: ["react", "react-dom"],
});
```

**`esbuild` — Applications where you only need JS output (type-check separately):**
```ts
// build.mjs
import { build } from "esbuild";

await build({
  entryPoints: ["src/index.ts"],
  bundle: true,
  platform: "node",
  target: "node20",
  outfile: "dist/index.js",
  format: "esm",
  sourcemap: true,
  external: ["better-sqlite3"], // native modules can't be bundled
});
```

**`swc` — Drop-in replacement for `tsc` emit when you want per-file output fast:**
```json
// .swcrc
{
  "$schema": "https://json.schemastore.org/swcrc",
  "jsc": {
    "parser": { "syntax": "typescript", "decorators": true },
    "target": "es2022"
  },
  "module": { "type": "es6" }
}
```

### 8.3 — ESLint Flat Config (eslint.config.ts)

ESLint 9+ uses the "flat config" format. The old `.eslintrc.*` files are deprecated.

```ts
// eslint.config.ts
import eslint from "@eslint/js";
import tseslint from "typescript-eslint";
import prettier from "eslint-config-prettier";

export default tseslint.config(
  // Global ignores
  { ignores: ["**/dist/**", "**/node_modules/**", "**/*.js"] },

  // Base JS rules
  eslint.configs.recommended,

  // TypeScript rules (type-aware)
  ...tseslint.configs.strictTypeChecked,
  ...tseslint.configs.stylisticTypeChecked,

  // TypeScript parser options
  {
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },

  // Custom rule overrides
  {
    rules: {
      "@typescript-eslint/no-unused-vars": [
        "error",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_" },
      ],
      "@typescript-eslint/consistent-type-imports": [
        "error",
        { prefer: "type-imports", fixStyle: "inline-type-imports" },
      ],
      "@typescript-eslint/no-misused-promises": [
        "error",
        { checksVoidReturn: { attributes: false } },
      ],
      "@typescript-eslint/restrict-template-expressions": [
        "error",
        { allowNumber: true },
      ],
    },
  },

  // Disable formatting rules (let Prettier handle it)
  prettier,
);
```

### 8.4 — Biome: The All-in-One Alternative

Biome is a Rust-based tool that replaces ESLint + Prettier in a single binary. It's 10-100x faster.

```json
// biome.json
{
  "$schema": "https://biomejs.dev/schemas/1.9.0/schema.json",
  "organizeImports": { "enabled": true },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "complexity": {
        "noExcessiveCognitiveComplexity": { "level": "warn", "options": { "maxAllowedComplexity": 15 } }
      },
      "correctness": {
        "noUnusedVariables": "error",
        "noUnusedImports": "error",
        "useExhaustiveDependencies": "warn"
      },
      "style": {
        "noNonNullAssertion": "warn",
        "useConst": "error"
      },
      "suspicious": {
        "noExplicitAny": "error"
      }
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "double",
      "semicolons": "always",
      "trailingCommas": "all"
    }
  }
}
```

```bash
# Biome vs ESLint+Prettier benchmark (real project, 500 files):
# biome check .          → 45ms
# eslint . && prettier . → 4200ms
# That's ~93x faster.
```

**When to choose Biome over ESLint:**
- You don't need type-aware lint rules (Biome doesn't run `tsc`)
- You want zero-config speed
- You're starting a new project and don't need ESLint plugin ecosystem

**When to stick with ESLint:**
- You need `@typescript-eslint` type-aware rules (e.g., `no-floating-promises`)
- You rely on framework-specific plugins (eslint-plugin-react-hooks, etc.)
- Your team has extensive custom ESLint rules

---

## 📎 9. Appendix — Deep Dives & Theory

### Appendix A — Project References Graph Computation

TypeScript's `--build` mode (`tsc -b`) performs a topological sort of the project reference graph before compilation. Understanding this algorithm helps you structure monorepos for maximum parallelism.

#### The Algorithm

```ts
// Simplified representation of tsc -b's internal logic
interface ProjectNode {
  path: string;
  references: ProjectNode[];
  buildInfo: BuildInfo | null;
  needsRebuild: boolean;
}

function topologicalBuild(root: ProjectNode): void {
  const visited = new Set<string>();
  const building = new Set<string>();

  function visit(node: ProjectNode): void {
    if (visited.has(node.path)) return;
    if (building.has(node.path)) {
      throw new Error(`Circular reference detected: ${node.path}`);
    }

    building.add(node.path);

    // Build dependencies first (DFS post-order)
    for (const ref of node.references) {
      visit(ref);
    }

    building.delete(node.path);
    visited.add(node.path);

    if (node.needsRebuild) {
      compileProject(node);
    }
  }

  visit(root);
}
```

#### Staleness Detection

The `.tsbuildinfo` file stores:
1. **File version hashes** — SHA of each input file at last successful build
2. **Semantic diagnostics** — cached type errors (avoids re-checking unchanged files)
3. **Emit signatures** — hash of the public API surface (`.d.ts` output)

A project is "stale" if:
- Any input file's hash differs from the stored hash
- Any referenced project's emit signature changed (API surface changed)
- The `tsconfig.json` itself changed

```bash
# Force rebuild everything (clears .tsbuildinfo)
tsc -b --force

# Verbose mode shows what's being rebuilt and why
tsc -b --verbose
# Project 'packages/shared' is up to date because newest input 'src/types.ts'
#   is older than output 'dist/types.d.ts'
# Project 'apps/api' is out of date because output 'dist/index.js'
#   is older than input 'src/routes/users.ts'
```

### Appendix B — Incremental Build Cache Internals

#### The `.tsbuildinfo` File Structure

```json
{
  "program": {
    "fileNames": [
      "../../node_modules/typescript/lib/lib.es2022.d.ts",
      "./src/index.ts",
      "./src/utils/helpers.ts"
    ],
    "fileInfos": [
      { "version": "abc123", "affectsGlobalScope": true },
      { "version": "def456", "signature": "ghi789" },
      { "version": "jkl012", "signature": "mno345" }
    ],
    "options": {
      "strict": true,
      "target": 9,
      "module": 99
    },
    "semanticDiagnosticsPerFile": [], [], [](],-[],-[)
  },
  "version": "5.5.0"
}
```

Key fields:
- **`version`** — hash of the file content (determines if re-parse is needed)
- **`signature`** — hash of the file's public API (determines if dependents need re-check)
- **`semanticDiagnosticsPerFile`** — cached errors per file (empty = no errors)

#### Why `signature` Matters

If you change the *implementation* of a function but not its *type signature*, only that file gets re-emitted. Downstream dependents don't need re-checking because the `.d.ts` output (the "signature") hasn't changed.

```ts
// packages/shared/src/math.ts

// BEFORE:
export function add(a: number, b: number): number {
  return a + b;
}

// AFTER (implementation change only — signature unchanged):
export function add(a: number, b: number): number {
  console.log(`Adding ${a} + ${b}`);
  return a + b;
}
// Result: Only packages/shared rebuilds. apps/api gets cache hit.

// AFTER (signature change — return type widened):
export function add(a: number, b: number): number | null {
  if (a < 0) return null;
  return a + b;
}
// Result: packages/shared rebuilds AND apps/api must re-check
// (because the .d.ts changed)
```

### Appendix C — Complete Monorepo Scaffold

```bash
# Full production monorepo setup script
mkdir my-platform && cd my-platform
pnpm init
corepack enable

# Workspace configuration
cat > pnpm-workspace.yaml << 'EOF'
packages:
  - "packages/*"
  - "apps/*"
  - "tools/*"
EOF

# Turborepo
pnpm add -Dw turbo

# Shared dev dependencies (hoisted to root)
pnpm add -Dw typescript @types/node vitest
pnpm add -Dw @biomejs/biome  # or eslint + prettier

# Create packages
mkdir -p packages/{shared,db,ui}/src
mkdir -p apps/{api,web}/src
mkdir -p tools/scripts

# Each package gets its own package.json + tsconfig.json
# The root tsconfig.json only has "references" (no compilerOptions)
```

```json
// Root tsconfig.json (solution-style)
{
  "files": [],
  "references": [
    { "path": "packages/shared" },
    { "path": "packages/db" },
    { "path": "packages/ui" },
    { "path": "apps/api" },
    { "path": "apps/web" }
  ]
}
```

### Appendix D — Compiler Flag Decision Matrix

| Flag | Default | Recommended | Why |
|------|---------|-------------|-----|
| `strict` | `false` | `true` | Enables all strict checks at once |
| `noUncheckedIndexedAccess` | `false` | `true` | Array/object index returns `T \| undefined` |
| `exactOptionalPropertyTypes` | `false` | `true` | Distinguishes `undefined` from "missing" |
| `verbatimModuleSyntax` | `false` | `true` | Forces `import type` for type-only imports |
| `isolatedModules` | `false` | `true` | Required for esbuild/swc/Babel compatibility |
| `moduleResolution` | varies | `"bundler"` | Modern resolution for Vite/webpack projects |
| `module` | varies | `"ESNext"` | Emit ESM; let bundler handle the rest |
| `target` | `"ES3"` | `"ES2022"` | Match your minimum runtime (Node 18+) |
| `declaration` | `false` | `true` (libs) | Generate `.d.ts` for consumers |
| `declarationMap` | `false` | `true` (libs) | "Go to definition" jumps to `.ts` source |
| `sourceMap` | `false` | `true` | Debuggable stack traces |
| `incremental` | `false` | `true` | Faster rebuilds via `.tsbuildinfo` |
| `composite` | `false` | `true` (monorepo) | Required for project references |
| `skipLibCheck` | `false` | `true` | Skip checking `node_modules` `.d.ts` files |

---

*Last updated: 2026-05-24*
