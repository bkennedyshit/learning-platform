---
title: "13.6 — Modules & Build Systems"
subject: "TypeScript"
catalog: advanced
audience_tier: higher-education
chapter: "13.6"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 13.6 — Modules & Build Systems

> *"The module system is the most confusing part of the JavaScript ecosystem. ESM vs CJS, bundlers vs runtimes, .mjs vs .cjs — it's a mess. But once you understand the 'why', the 'what' becomes obvious."* — **Theo Browne** (t3.gg)

JavaScript has two module systems that don't fully interoperate. TypeScript adds a third layer of complexity with its own module resolution. This chapter cuts through the confusion and gives you a clear mental model for how modules work in 2025+.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Explain ESM vs CJS differences and why ESM is the future.
2. Configure `package.json` exports for dual ESM/CJS packages.
3. Choose the right bundler (Vite, esbuild, Rollup, webpack) for your use case.
4. Set up a monorepo with pnpm workspaces + Turborepo.
5. Publish a typed npm package with proper `exports`, `types`, and `files` fields.
6. Debug module resolution issues using `tsc --traceResolution`.

---

## 🖼️ Visual Anchor — Module Resolution Flow

![ts__6.6-fig1](ts__6.6-fig1.svg)

---

## 📚 1. Concepts & Definitions

### Definition 13.6.1 — ESM (ECMAScript Modules)

The **standard** module system, part of the JavaScript language specification:

```ts
// Named exports
export function add(a: number, b: number): number { return a + b; }
export const PI = 3.14159;
export type Vector = { x: number; y: number };

// Default export
export default class Calculator { /* ... */ }

// Import
import Calculator, { add, PI, type Vector } from "./math";
import * as math from "./math"; // Namespace import
```

Key characteristics:
- **Static** — imports/exports are determined at parse time (enables tree-shaking)
- **Async** — modules load asynchronously
- **Strict mode** by default
- Top-level `await` supported

### Definition 13.6.2 — CJS (CommonJS)

The **legacy** module system, invented for Node.js before ESM existed:

```js
// Export
module.exports = { add, PI };
// or
exports.add = function(a, b) { return a + b; };

// Import
const { add, PI } = require("./math");
const math = require("./math");
```

Key characteristics:
- **Dynamic** — `require()` can be called anywhere, conditionally
- **Synchronous** — blocks until module is loaded
- No tree-shaking (bundlers can't statically analyze)
- Still used by many npm packages and Node.js config files

### Definition 13.6.3 — Module Resolution in TypeScript

TypeScript has multiple resolution strategies:

| `moduleResolution` | When to Use | How it Resolves |
|---|---|---|
| `"bundler"` | Apps using Vite/webpack/esbuild | Follows bundler conventions (extensionless imports OK) |
| `"node16"` / `"nodenext"` | Libraries, Node.js apps | Follows Node.js ESM rules (extensions required) |
| `"node"` (legacy) | Old projects | CJS-style resolution |

```jsonc
// For apps (bundled):
{ "moduleResolution": "bundler" }

// For libraries (consumed by Node directly):
{ "moduleResolution": "node16" }
```

### Definition 13.6.4 — Package.json `exports` Field

The modern way to define what your package exposes:

```jsonc
{
  "name": "@myapp/shared",
  "type": "module",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js",
      "require": "./dist/index.cjs"
    },
    "./utils": {
      "types": "./dist/utils.d.ts",
      "import": "./dist/utils.js"
    }
  },
  "files": ["dist"]
}
```

### Definition 13.6.5 — Tree-Shaking

Dead code elimination — bundlers remove unused exports:

```ts
// math.ts exports 10 functions
export function add() { /* ... */ }
export function subtract() { /* ... */ }
// ... 8 more

// app.ts only imports one
import { add } from "./math";

// After bundling: only `add` is in the output bundle
// The other 9 functions are "shaken" out of the tree
```

Only works with ESM (static imports). CJS `require()` defeats tree-shaking.

---

## 🧩 2. Mental Models

### Model 6.6.1 — The Build Pipeline

```
Source (.ts/.tsx)
    │
    ├── tsc --noEmit ──→ Type errors (CI check)
    │
    └── Bundler (Vite/esbuild) ──→ Optimized JS bundle
            │
            ├── Tree-shaking (remove dead code)
            ├── Minification (shrink file size)
            ├── Code splitting (lazy-load routes)
            └── Asset handling (CSS, images)
```

**Key insight:** `tsc` is for type-checking. Bundlers are for building. Don't use `tsc` as your build tool for applications.

### Model 6.6.2 — Bundler Comparison

| Bundler | Speed | Config | Best For |
|---------|-------|--------|----------|
| **Vite** | ⚡⚡⚡ | Minimal | Web apps (React, Vue, Svelte) |
| **esbuild** | ⚡⚡⚡⚡ | Minimal | Libraries, simple apps |
| **Rollup** | ⚡⚡ | Moderate | Libraries (best tree-shaking) |
| **webpack** | ⚡ | Complex | Legacy apps, complex needs |
| **tsup** | ⚡⚡⚡ | Zero-config | Libraries (wraps esbuild+Rollup) |
| **Bun** | ⚡⚡⚡⚡ | Built-in | Full-stack Bun apps |

**Recommendation:** Vite for apps, tsup for libraries.

---

## 🔑 3. Mechanics

### 3.1 — Vite Configuration for TypeScript

```ts
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [
    react(),
    tsconfigPaths(), // Resolves tsconfig path aliases
  ],
  build: {
    target: "es2022",
    sourcemap: true,
  },
});
```

### 3.2 — tsup for Library Publishing

```ts
// tsup.config.ts
import { defineConfig } from "tsup";

export default defineConfig({
  entry: ["src/index.ts"],
  format: ["esm", "cjs"],  // Dual format output
  dts: true,                // Generate .d.ts
  splitting: true,
  sourcemap: true,
  clean: true,
});
```

### 3.3 — Monorepo with Turborepo

```jsonc
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],  // Build dependencies first
      "outputs": ["dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "check": {
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["build"]
    }
  }
}
```

```bash
# Run all builds in dependency order (parallel where possible)
turbo build

# Run dev servers for all apps
turbo dev

# Run type-check across all packages
turbo check
```

### 3.4 — `import type` and `verbatimModuleSyntax`

```ts
// With verbatimModuleSyntax: true (recommended)

// Type-only import — completely erased at compile time
import type { User } from "./types";

// Value import — kept in output
import { createUser } from "./users";

// Mixed — use inline type modifier
import { createUser, type User } from "./users";

// Type-only export
export type { User };

// Re-export types
export type { Config } from "./config";
```

### 3.5 — Debugging Module Resolution

```bash
# See exactly how TS resolves each import
npx tsc --traceResolution 2>&1 | grep "FAILED\|FOUND"

# Common issues:
# 1. Missing "types" in package.json exports
# 2. Wrong moduleResolution setting
# 3. Missing @types/* package
# 4. Path alias not configured in bundler
```

---

## 💻 4. Code Patterns & Examples

### Pattern 6.6.1 — Library Package Structure

```
my-library/
├── src/
│   ├── index.ts          ← Main entry (re-exports public API)
│   ├── utils.ts          ← Secondary entry point
│   └── internal.ts       ← NOT exported (internal only)
├── package.json
├── tsconfig.json
└── tsup.config.ts
```

```jsonc
// package.json
{
  "name": "my-library",
  "version": "1.0.0",
  "type": "module",
  "exports": {
    ".": { "types": "./dist/index.d.ts", "import": "./dist/index.js", "require": "./dist/index.cjs" },
    "./utils": { "types": "./dist/utils.d.ts", "import": "./dist/utils.js", "require": "./dist/utils.cjs" }
  },
  "files": ["dist"],
  "scripts": {
    "build": "tsup",
    "check": "tsc --noEmit",
    "prepublishOnly": "pnpm build"
  }
}
```

### Pattern 6.6.2 — Barrel Files (Index Re-exports)

```ts
// src/index.ts — the public API surface
export { createUser, deleteUser } from "./users";
export { createPost, updatePost } from "./posts";
export type { User, Post, Comment } from "./types";

// Consumers import from the package root:
import { createUser, type User } from "my-library";
```

**Warning:** Barrel files can hurt tree-shaking if not configured properly. Use `"sideEffects": false` in package.json.

---

## 🧮 5. Worked Examples

### Example 13.6.1 — Set Up a Full Monorepo from Scratch

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```bash
# 1. Initialize
mkdir my-monorepo && cd my-monorepo
pnpm init
echo 'packages:\n  - "packages/*"\n  - "apps/*"' > pnpm-workspace.yaml

# 2. Create shared package
mkdir -p packages/shared/src
cd packages/shared && pnpm init && cd ../..

# 3. Create web app
mkdir -p apps/web
cd apps/web && pnpm create vite . --template react-ts && cd ../..

# 4. Create API
mkdir -p apps/api/src
cd apps/api && pnpm init && cd ../..

# 5. Install Turborepo
pnpm add -D turbo -w

# 6. Add turbo.json (see Section 3.3)

# 7. Link packages
cd apps/web && pnpm add @myapp/shared --workspace
cd ../api && pnpm add @myapp/shared --workspace
```

</details>

---

## ⚠️ 6. Gotchas & Anti-Patterns

### Gotcha 6.6.1 — ESM Requires File Extensions in Node

```ts
// In Node.js with "type": "module":
import { add } from "./math";     // ❌ Error: Cannot find module
import { add } from "./math.js";  // ✅ Must include .js extension

// In bundler mode (Vite, webpack):
import { add } from "./math";     // ✅ Bundler resolves it

// This is why moduleResolution matters:
// "bundler" → no extensions needed
// "node16"  → extensions required
```

### Gotcha 6.6.2 — Circular Dependencies

```ts
// a.ts
import { B } from "./b"; // B imports from a.ts → circular!
export class A { b = new B(); }

// b.ts
import { A } from "./a";
export class B { a = new A(); } // 💥 One of these will be undefined at runtime

// Fix: extract shared types to a third file
// types.ts
export interface IA { /* ... */ }
export interface IB { /* ... */ }
```

### Gotcha 6.6.3 — `"type": "module"` Changes Everything

```jsonc
// package.json
{ "type": "module" }
// Now ALL .js files are ESM. CJS files must use .cjs extension.
// Config files (eslint, prettier) may need .cjs extension.
```

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- **Previous:** [13.5 - Async, Promises & Async Generators](13.5---Async,-Promises-&-Async-Generators)
- **Next:** [13.7 - Frontend with TypeScript - React, Vue, Svelte, SolidJS](13.7---Frontend-with-TypeScript---React,-Vue,-Svelte,-SolidJS)
- **Project setup:** [13.1 - Setup, Compilation & Project Structure](13.1---Setup,-Compilation-&-Project-Structure)
- **Backend builds:** [13.8 - Backend with TypeScript - Node, Bun, Deno, Express, Fastify, Hono](13.8---Backend-with-TypeScript---Node,-Bun,-Deno,-Express,-Fastify,-Hono)

### External Resources
- [TypeScript Module Theory](https://www.typescriptlang.org/docs/handbook/modules/theory.html)
- [Vite Documentation](https://vitejs.dev/)
- [tsup Documentation](https://tsup.egoist.dev/)
- [Turborepo Handbook](https://turbo.build/repo/docs/handbook)
- [Are We ESM Yet?](https://gist.github.com/sindresorhus/a39789f98801d908bbc7ff3ecc99d99c)

---

*Last updated: 2026-05-24*



---

## 🏗️ 8. The ESM/CJS Dual Package Problem & Monorepo Build Orchestration

### 8.1 — The ESM/CJS Dual Package Nightmare

Publishing a package that works in both ESM (`import`) and CJS (`require()`) environments is one of the hardest problems in the Node.js ecosystem. Here's the complete picture.

#### The Core Problem

```ts
// ESM consumer:
import { helper } from "my-package"; // Expects ESM entry

// CJS consumer:
const { helper } = require("my-package"); // Expects CJS entry

// They need DIFFERENT files because:
// - ESM uses `import`/`export` (static, async)
// - CJS uses `require`/`module.exports` (dynamic, sync)
// - ESM can import CJS, but CJS CANNOT require() ESM
```

#### The `package.json` `exports` Field (Conditional Exports)

```json
{
  "name": "my-package",
  "version": "1.0.0",
  "type": "module",
  "exports": {
    ".": {
      "import": {
        "types": "./dist/esm/index.d.ts",
        "default": "./dist/esm/index.js"
      },
      "require": {
        "types": "./dist/cjs/index.d.cts",
        "default": "./dist/cjs/index.cjs"
      }
    },
    "./utils": {
      "import": "./dist/esm/utils.js",
      "require": "./dist/cjs/utils.cjs"
    }
  },
  "main": "./dist/cjs/index.cjs",
  "module": "./dist/esm/index.js",
  "types": "./dist/esm/index.d.ts",
  "files": ["dist"]
}
```

#### File Extensions Matter

| Extension | Interpretation | When to Use |
|-----------|---------------|-------------|
| `.js` | Depends on nearest `package.json` `"type"` field | Default |
| `.mjs` | Always ESM | Force ESM regardless of package.json |
| `.cjs` | Always CJS | Force CJS regardless of package.json |
| `.d.ts` | Type declarations for `.js` | Default types |
| `.d.mts` | Type declarations for `.mjs` | ESM-specific types |
| `.d.cts` | Type declarations for `.cjs` | CJS-specific types |

#### The tsup Solution (Recommended)

```ts
// tsup.config.ts — generates both ESM and CJS from single source
import { defineConfig } from "tsup";

export default defineConfig({
  entry: ["src/index.ts", "src/utils.ts"],
  format: ["esm", "cjs"],
  dts: true,
  splitting: true,
  sourcemap: true,
  clean: true,
  outDir: "dist",
  // Generates:
  // dist/index.js (ESM)
  // dist/index.cjs (CJS)
  // dist/index.d.ts
  // dist/index.d.cts
});
```

#### The "Dual Package Hazard"

```ts
// DANGER: If both ESM and CJS versions are loaded in the same process,
// you get TWO copies of the module with separate state!

// esm-consumer.mjs
import { counter } from "my-package"; // Gets ESM copy
counter.increment();
console.log(counter.value); // 1

// cjs-consumer.cjs (in same process via dynamic import)
const { counter } = require("my-package"); // Gets CJS copy — DIFFERENT instance!
console.log(counter.value); // 0 (not 1!)

// Solution: use a "wrapper" pattern where CJS re-exports ESM
// dist/index.cjs:
module.exports = await import("./index.js"); // Single source of truth
```

### 8.2 — Turborepo Cache Hashing Deep Dive

Turborepo's cache is content-addressable: the hash of inputs determines whether a cached output can be reused.

#### Hash Computation Algorithm

```ts
// Pseudocode of Turborepo's hash computation
interface TaskHash {
  // 1. Package-level inputs
  packageJson: string;           // Hash of package.json
  lockfilePartial: string;       // Hash of this package's deps in lockfile
  envVars: Record<string, string>; // Declared env vars

  // 2. Task-level inputs
  inputFiles: string[];          // Hashes of files matching `inputs` glob
  taskDefinition: string;        // Hash of turbo.json task config

  // 3. Dependency chain
  upstreamHashes: string[];      // Hashes of `^dependency` task outputs

  // 4. Global inputs
  globalFiles: string[];         // Files in `globalDependencies`
  globalEnv: Record<string, string>;
}

function computeHash(task: TaskHash): string {
  return sha256(JSON.stringify(task));
}
```

#### Debugging Cache Misses

```bash
# Show what's in the hash
turbo build --dry=json | jq '.tasks[].hashOfExternalDependencies'

# Verbose output shows why cache missed
turbo build --verbosity=2

# Common cache-busting culprits:
# 1. Timestamps in generated files (use deterministic output)
# 2. Absolute paths in build output (use relative paths)
# 3. Undeclared env vars changing between runs
# 4. .env files not listed in globalDependencies
```

#### Remote Cache Configuration

```json
// turbo.json — fine-grained cache control
{
  "globalDependencies": [
    ".env",
    "tsconfig.base.json"
  ],
  "globalEnv": ["NODE_ENV", "CI"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"],
      "inputs": ["src/**", "tsconfig.json", "package.json"],
      "env": ["DATABASE_URL"],
      "cache": true
    },
    "deploy": {
      "dependsOn": ["build", "test"],
      "cache": false
    }
  }
}
```

### 8.3 — Nx vs Turborepo vs Lerna: Decision Matrix

| Feature | Turborepo | Nx | Lerna (v7+) |
|---------|-----------|-----|-------------|
| **Philosophy** | Minimal, fast | Full-featured, opinionated | Package publishing |
| **Speed** | ⚡ Very fast (Go) | ⚡ Fast (Rust daemon) | 🐢 Slower |
| **Cache** | Local + Vercel Remote | Local + Nx Cloud | Via Nx (Lerna uses Nx) |
| **Task graph** | `turbo.json` | `project.json` + plugins | `lerna.json` |
| **Affected detection** | File hash based | Git diff + dep graph | Git diff based |
| **Code generation** | ❌ None | ✅ Generators/schematics | ❌ None |
| **Plugins** | ❌ None | ✅ Rich ecosystem | ❌ None |
| **Config complexity** | Low (1 file) | Medium (multiple files) | Low |
| **Best for** | Speed-focused teams | Enterprise, Angular | OSS package publishing |
| **Learning curve** | 15 minutes | 1-2 hours | 30 minutes |

#### When to Choose Each

**Turborepo** — You want the fastest possible builds with minimal configuration. Your monorepo is primarily TypeScript/JavaScript. You don't need code generation or complex workspace plugins.

**Nx** — You have a large enterprise monorepo (50+ packages). You need affected-based testing, code generators, and deep framework integration. You're willing to invest in configuration for long-term productivity.

**Lerna** — You're publishing multiple npm packages from a monorepo. You need automated versioning and changelog generation. (Note: Lerna v7+ uses Nx under the hood for task running.)

### 8.4 — pnpm Workspaces: The Foundation

```yaml
# pnpm-workspace.yaml
packages:
  - "packages/*"
  - "apps/*"
  - "tools/*"
  - "!**/test-fixtures/**"  # Exclude patterns
```

```json
// Root package.json
{
  "name": "my-monorepo",
  "private": true,
  "scripts": {
    "build": "turbo build",
    "dev": "turbo dev",
    "lint": "turbo lint",
    "test": "turbo test",
    "check": "turbo check",
    "clean": "turbo clean && rm -rf node_modules"
  },
  "devDependencies": {
    "turbo": "^2.0.0",
    "typescript": "^5.5.0"
  },
  "packageManager": "pnpm@9.0.0",
  "engines": {
    "node": ">=20.0.0"
  }
}
```

```bash
# Workspace commands
pnpm add lodash --filter @myapp/api        # Add dep to specific package
pnpm add -D vitest --filter "./packages/*"  # Add to all packages
pnpm add @myapp/shared --filter @myapp/api --workspace  # Internal dep
pnpm run build --filter @myapp/api...       # Build api and all its deps
pnpm run test --filter "...[HEAD~1]"        # Test only changed packages
```

---

## 📎 9. Appendix — Deep Dives & Theory

### Appendix A — Node.js ESM Resolution Algorithm

When Node.js encounters an `import` statement, it follows this resolution algorithm:

```ts
// Simplified Node ESM resolution (node:module)
function resolve(specifier: string, parentURL: URL): URL {
  // 1. Built-in modules
  if (isBuiltin(specifier)) return `node:${specifier}`;

  // 2. Absolute URLs
  if (isURL(specifier)) return new URL(specifier);

  // 3. Relative paths (./foo, ../bar)
  if (specifier.startsWith(".") || specifier.startsWith("/")) {
    const resolved = new URL(specifier, parentURL);
    return resolveFile(resolved) ?? resolveDirectory(resolved);
  }

  // 4. Package specifiers (bare specifiers like "lodash")
  return resolvePackage(specifier, parentURL);
}

function resolvePackage(specifier: string, parentURL: URL): URL {
  // Walk up directory tree looking for node_modules
  const packageName = getPackageName(specifier); // "lodash" or "@scope/pkg"
  const subpath = getSubpath(specifier);         // "./utils" or ""

  // Find the package's package.json
  const pkgJson = findPackageJson(packageName, parentURL);

  // Check "exports" field (modern)
  if (pkgJson.exports) {
    return resolveExports(pkgJson, subpath, {
      conditions: ["import", "node", "default"],
    });
  }

  // Fallback: "main" field (legacy)
  return new URL(pkgJson.main ?? "index.js", pkgJsonURL);
}
```

#### The Conditions System

```json
// package.json "exports" with conditions
{
  "exports": {
    ".": {
      "node": {
        "import": "./dist/node-esm.js",
        "require": "./dist/node-cjs.cjs"
      },
      "browser": "./dist/browser.js",
      "default": "./dist/index.js"
    }
  }
}
```

Node.js evaluates conditions in order. The first matching condition wins:
1. `"node"` — running in Node.js
2. `"import"` — loaded via `import` statement
3. `"require"` — loaded via `require()`
4. `"browser"` — bundler hint (not used by Node itself)
5. `"default"` — fallback

#### Common Resolution Errors and Fixes

```bash
# Error: ERR_MODULE_NOT_FOUND
# Cause: ESM requires full file extensions
import { helper } from "./utils";     # ❌ Fails in ESM
import { helper } from "./utils.js";  # ✅ Works

# Error: ERR_REQUIRE_ESM
# Cause: Trying to require() an ESM-only package
const pkg = require("esm-only-pkg");  # ❌
const pkg = await import("esm-only-pkg"); # ✅

# Error: ERR_PACKAGE_PATH_NOT_EXPORTED
# Cause: Accessing a subpath not listed in "exports"
import { internal } from "pkg/internal"; # ❌ Not in exports map
import { public } from "pkg/public";     # ✅ Listed in exports
```

### Appendix B — Bundler Tree-Shaking Heuristics

Tree-shaking (dead code elimination) removes unused exports from the final bundle. But it's not magic — it relies on static analysis heuristics.

#### What Makes Code Tree-Shakeable

```ts
// ✅ TREE-SHAKEABLE: Named exports, pure functions, no side effects
export function add(a: number, b: number): number {
  return a + b;
}

export function multiply(a: number, b: number): number {
  return a * b;
}

// Consumer only imports `add`:
import { add } from "./math";
// Bundler removes `multiply` from the output

// ❌ NOT TREE-SHAKEABLE: Side effects at module level
console.log("Module loaded!"); // Side effect — can't remove this module

export const config = {
  debug: process.env.NODE_ENV === "development", // Side effect (reads env)
};

// ❌ NOT TREE-SHAKEABLE: Default export of object
export default {
  add: (a: number, b: number) => a + b,
  multiply: (a: number, b: number) => a * b,
};
// Bundler can't know which properties are used (dynamic access possible)
```

#### The `sideEffects` Field

```json
// package.json
{
  "sideEffects": false
}
// Tells bundlers: "Every file in this package is side-effect-free"
// Safe to remove any unused import entirely

// Or be specific:
{
  "sideEffects": [
    "*.css",
    "./src/polyfills.ts",
    "./src/register-globals.ts"
  ]
}
// Only these files have side effects; everything else is safe to tree-shake
```

#### How Bundlers Detect Side Effects

```ts
// Bundlers use these heuristics:
// 1. Top-level function calls → side effect
console.log("hi");           // ❌ Side effect
registerPlugin(myPlugin);    // ❌ Side effect

// 2. Property access on imported modules → might be side effect (getter)
import obj from "./module";
obj.value;                   // ⚠️ Could trigger a getter

// 3. IIFE → side effect
(function() { /* ... */ })(); // ❌ Side effect

// 4. Pure annotations (hint to bundler)
const result = /*#__PURE__*/ createExpensiveThing();
// If `result` is unused, bundler can remove this line

// 5. Class declarations with decorators → side effect
@Injectable()               // ❌ Decorator call = side effect
class MyService {}
```

#### Measuring Tree-Shaking Effectiveness

```bash
# Visualize bundle composition
npx vite-bundle-visualizer

# Check if a specific export is tree-shaken
# 1. Import only one thing
import { specificFunction } from "large-library";

# 2. Build and check output size
npx esbuild app.ts --bundle --analyze

# 3. Compare with importing everything
import * as lib from "large-library";
```

### Appendix C — Module Federation (Micro-Frontends)

Module Federation allows separately-built applications to share code at runtime:

```ts
// webpack.config.ts (host app)
import { ModuleFederationPlugin } from "webpack";

export default {
  plugins: [
    new ModuleFederationPlugin({
      name: "host",
      remotes: {
        // Load remote app at runtime
        checkout: "checkout@https://checkout.example.com/remoteEntry.js",
        profile: "profile@https://profile.example.com/remoteEntry.js",
      },
      shared: {
        react: { singleton: true, requiredVersion: "^18.0.0" },
        "react-dom": { singleton: true, requiredVersion: "^18.0.0" },
      },
    }),
  ],
};

// Consuming a remote module (type-safe with declaration)
// @types/checkout.d.ts
declare module "checkout/CheckoutWidget" {
  const CheckoutWidget: React.FC<{ cartId: string }>;
  export default CheckoutWidget;
}

// Usage in host app
const CheckoutWidget = React.lazy(() => import("checkout/CheckoutWidget"));
```

### Appendix D — Import Maps (Browser-Native Module Resolution)

```json
// importmap.json (served as <script type="importmap">)
{
  "imports": {
    "react": "https://esm.sh/react@18.3.0",
    "react-dom/client": "https://esm.sh/react-dom@18.3.0/client",
    "lodash/": "https://esm.sh/lodash-es@4.17.21/",
    "@myapp/shared": "/packages/shared/dist/index.js"
  },
  "scopes": {
    "/admin/": {
      "react": "https://esm.sh/react@19.0.0"
    }
  }
}
```

```ts
// Now bare specifiers work in the browser without a bundler!
import React from "react";
import { debounce } from "lodash/debounce";
import { User } from "@myapp/shared";
```

### Appendix E — Vite's Module Resolution & HMR Architecture

Vite uses a fundamentally different approach from webpack: it serves source files as native ESM during development, transforming them on-demand.

#### How Vite Dev Server Works

```ts
// 1. Browser requests: GET /src/App.tsx
// 2. Vite intercepts, transforms TSX → JS on the fly
// 3. Returns ESM with import rewrites:

// Original source:
import { useState } from "react";
import { Button } from "@/components/Button";
import styles from "./App.module.css";

// Vite transforms to:
import { useState } from "/node_modules/.vite/deps/react.js?v=abc123";
import { Button } from "/src/components/Button.tsx?t=1234567890";
import styles from "/src/App.module.css?direct";

// Key insight: node_modules are pre-bundled (esbuild) once,
// but YOUR source files are served individually (no bundling in dev!)
```

#### HMR (Hot Module Replacement) Protocol

```ts
// Vite injects HMR client code into every module:
if (import.meta.hot) {
  import.meta.hot.accept((newModule) => {
    // This module was updated — re-execute with new code
    // React Fast Refresh handles component state preservation
  });

  import.meta.hot.dispose(() => {
    // Cleanup before module is replaced (remove event listeners, etc.)
  });

  // Accept updates from specific dependencies
  import.meta.hot.accept("./utils.ts", (newUtils) => {
    // Only utils.ts changed — update reference without full reload
  });
}

// HMR boundary: if a module can't self-accept, the update
// propagates UP the import chain until it finds a boundary
// (usually the React/Vue root component)
```

#### Vite Plugin API

```ts
// vite.config.ts — custom plugin example
import { defineConfig, Plugin } from "vite";

function myPlugin(): Plugin {
  return {
    name: "my-custom-plugin",

    // Transform source code
    transform(code, id) {
      if (id.endsWith(".md")) {
        // Convert markdown to a JS module
        const html = markdownToHtml(code);
        return `export default ${JSON.stringify(html)}`;
      }
    },

    // Resolve custom import specifiers
    resolveId(source) {
      if (source === "virtual:my-module") {
        return "\0virtual:my-module"; // \0 prefix = virtual module
      }
    },

    // Provide content for virtual modules
    load(id) {
      if (id === "\0virtual:my-module") {
        return `export const buildTime = ${Date.now()}`;
      }
    },

    // Configure dev server middleware
    configureServer(server) {
      server.middlewares.use("/api/health", (req, res) => {
        res.end(JSON.stringify({ status: "ok" }));
      });
    },
  };
}

export default defineConfig({
  plugins: [myPlugin()],
});
```

### Appendix F — Package Publishing Checklist

```json
// package.json for a published library (complete example)
{
  "name": "@myorg/utils",
  "version": "1.0.0",
  "description": "Shared utility functions",
  "license": "MIT",
  "type": "module",
  "exports": {
    ".": {
      "import": {
        "types": "./dist/index.d.ts",
        "default": "./dist/index.js"
      },
      "require": {
        "types": "./dist/index.d.cts",
        "default": "./dist/index.cjs"
      }
    },
    "./math": {
      "import": {
        "types": "./dist/math.d.ts",
        "default": "./dist/math.js"
      },
      "require": {
        "types": "./dist/math.d.cts",
        "default": "./dist/math.cjs"
      }
    }
  },
  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "files": ["dist", "README.md", "LICENSE"],
  "sideEffects": false,
  "scripts": {
    "build": "tsup",
    "check": "tsc --noEmit",
    "test": "vitest run",
    "prepublishOnly": "pnpm build && pnpm check && pnpm test"
  },
  "peerDependencies": {
    "typescript": ">=5.0.0"
  },
  "engines": {
    "node": ">=18.0.0"
  },
  "publishConfig": {
    "access": "public",
    "registry": "https://registry.npmjs.org/"
  },
  "keywords": ["typescript", "utilities"],
  "repository": {
    "type": "git",
    "url": "https://github.com/myorg/utils"
  }
}
```

#### Pre-Publish Verification

```bash
# 1. Check what files will be published
npm pack --dry-run

# 2. Verify exports resolve correctly
npx publint          # Checks package.json exports field
npx arethetypeswrong # Checks TypeScript resolution for all entry points

# 3. Test in a consumer project
cd /tmp && mkdir test-consumer && cd test-consumer
npm init -y
npm install ../path-to-your-package.tgz
node -e "import('@myorg/utils').then(m => console.log(Object.keys(m)))"

# 4. Check bundle size impact
npx bundlephobia @myorg/utils
```

### Appendix G — Monorepo CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2  # Needed for turbo affected detection

      - uses: pnpm/action-setup@v4
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: "pnpm"

      - run: pnpm install --frozen-lockfile

      # Turborepo remote cache
      - run: pnpm turbo build lint check test --cache-dir=.turbo
        env:
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
          TURBO_TEAM: ${{ vars.TURBO_TEAM }}

  publish:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          registry-url: "https://registry.npmjs.org"

      - run: pnpm install --frozen-lockfile
      - run: pnpm turbo build

      # Changesets handles versioning and publishing
      - uses: changesets/action@v1
        with:
          publish: pnpm changeset publish
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

---

*Last updated: 2026-05-24*
