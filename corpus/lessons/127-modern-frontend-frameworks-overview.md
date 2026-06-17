---
title: "12.7 — Modern Frontend Frameworks Overview"
subject: "JavaScript"
catalog: advanced
audience_tier: higher-education
chapter: "12.7"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 12.7 — Modern Frontend Frameworks Overview

> *"The best framework is the one your team ships with."* — **Theo Browne** (t3.gg)

> *"Frameworks are not about the framework. They're about the mental model they give you for thinking about UI."* — **Rich Harris**, creator of Svelte

This chapter is a **comparative overview**, not a deep dive. The goal is to give you informed opinions about the framework landscape so you can choose wisely for your projects. For deep implementation knowledge, see [Track 08 App Architectures](Track-08-App-Architectures) — specifically [22.1 - React & Next.js - Functional Components & Hooks](22.1---React-&-Next.js---Functional-Components-&-Hooks) for React.

---

## 🎯 Learning Objectives

1. **Explain the three reactivity paradigms** — Virtual DOM diffing, fine-grained signals, and compile-time reactivity.
2. **Compare React, Vue, Svelte, and Solid** on DX, performance, ecosystem, and hiring.
3. **Identify the signals pattern** and why it's converging across frameworks.
4. **Choose a framework** for a given project type with technical justification.
5. **Understand meta-frameworks** — Next.js, Nuxt, SvelteKit, SolidStart — and why they exist.

---

## 🖼️ Visual Anchor — Framework Reactivity Models

![js__5.7-fig1](js__5.7-fig1.svg)

---

## 📚 1. The Three Reactivity Paradigms

### Paradigm A: Virtual DOM Diffing (React)

```
State Change → Re-render entire component tree (virtual) → Diff old vs new VDOM → Patch real DOM
```

- **How:** Components are functions that return a virtual DOM tree. On state change, React re-runs the function, diffs the new tree against the old one, and applies minimal DOM patches.
- **Pros:** Simple mental model ("UI = f(state)"), predictable, huge ecosystem.
- **Cons:** Diffing has overhead; requires memoization (`useMemo`, `React.memo`) for performance; re-renders propagate down the tree.

### Paradigm B: Fine-Grained Reactivity / Signals (Solid, Vue 3)

```
State Change → Only the specific DOM nodes that depend on that state update
```

- **How:** Reactive primitives (signals/refs) track which DOM nodes read them. When a signal changes, only those specific nodes update — no diffing, no re-rendering of components.
- **Pros:** Surgical updates, no unnecessary work, no memoization needed.
- **Cons:** Different mental model (components run once, not on every update); less ecosystem maturity (Solid).

### Paradigm C: Compile-Time Reactivity (Svelte)

```
State Change → Compiler-generated update code runs → Direct DOM mutations
```

- **How:** The Svelte compiler analyzes your code at build time and generates imperative DOM update instructions. No runtime framework needed.
- **Pros:** Smallest bundle size, fastest initial load, most intuitive syntax.
- **Cons:** Compiler magic can be opaque; debugging compiled output is harder; smaller ecosystem.

---

## 📚 2. Framework Comparison

### React (2013, Meta)

```jsx
import { useState, useEffect } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    document.title = `Count: ${count}`;
  }, [count]);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount((c) => c + 1)}>+1</button>
    </div>
  );
}
```

| Aspect | Assessment |
|--------|-----------|
| **Reactivity** | Virtual DOM diffing, hooks for state |
| **Syntax** | JSX (JavaScript + HTML) |
| **Bundle size** | ~45KB (React + ReactDOM) |
| **Learning curve** | Medium (hooks rules, closures, memoization) |
| **Ecosystem** | 🏆 Largest — libraries for everything |
| **Jobs** | 🏆 Most demand by far |
| **Meta-framework** | Next.js (Vercel) |
| **Best for** | Large teams, complex apps, maximum hiring pool |

### Vue 3 (2014/2020, Evan You)

```vue
<script setup>
import { ref, watchEffect } from "vue";

const count = ref(0);

watchEffect(() => {
  document.title = `Count: ${count.value}`;
});
</script>

<template>
  <div>
    <p>Count: {{ count }}</p>
    <button @click="count++">+1</button>
  </div>
</template>
```

| Aspect | Assessment |
|--------|-----------|
| **Reactivity** | Proxy-based fine-grained (Composition API) |
| **Syntax** | SFC (Single File Components) — template + script + style |
| **Bundle size** | ~33KB |
| **Learning curve** | Low-Medium (Options API easy; Composition API = React-like) |
| **Ecosystem** | Large — Pinia, Vue Router, Vuetify |
| **Jobs** | Strong (especially outside US) |
| **Meta-framework** | Nuxt |
| **Best for** | Progressive adoption, teams wanting structure without rigidity |

### Svelte 5 (2016/2024, Rich Harris)

```svelte
<script>
  let count = $state(0);

  $effect(() => {
    document.title = `Count: ${count}`;
  });
</script>

<div>
  <p>Count: {count}</p>
  <button onclick={() => count++}>+1</button>
</div>
```

| Aspect | Assessment |
|--------|-----------|
| **Reactivity** | Compile-time + runes (Svelte 5 signals) |
| **Syntax** | Enhanced HTML (closest to vanilla) |
| **Bundle size** | ~2KB runtime + compiled output |
| **Learning curve** | 🏆 Lowest — feels like writing HTML/JS |
| **Ecosystem** | Growing — smaller than React/Vue |
| **Jobs** | Niche but growing |
| **Meta-framework** | SvelteKit |
| **Best for** | Small-medium apps, performance-critical, solo devs |

### Solid (2018, Ryan Carniato)

```jsx
import { createSignal, createEffect } from "solid-js";

function Counter() {
  const [count, setCount] = createSignal(0);

  createEffect(() => {
    document.title = `Count: ${count()}`;
  });

  return (
    <div>
      <p>Count: {count()}</p>
      <button onClick={() => setCount((c) => c + 1)}>+1</button>
    </div>
  );
}
```

| Aspect | Assessment |
|--------|-----------|
| **Reactivity** | Fine-grained signals (no VDOM) |
| **Syntax** | JSX (looks like React, works differently) |
| **Bundle size** | ~7KB |
| **Learning curve** | Medium (React-like syntax but different rules) |
| **Ecosystem** | Small but quality |
| **Jobs** | Rare (but growing) |
| **Meta-framework** | SolidStart |
| **Best for** | Performance-critical apps, React devs wanting better perf |

---

## 📚 3. The Signals Convergence

In 2024–2026, the JavaScript ecosystem is converging on **signals** as the reactivity primitive:

| Framework | Signal Implementation |
|-----------|----------------------|
| Solid | `createSignal()` (original pioneer) |
| Vue 3 | `ref()` / `reactive()` (Proxy-based) |
| Svelte 5 | `$state` rune (compiler-assisted) |
| Angular 16+ | `signal()` (added 2023) |
| Preact | `@preact/signals` |
| React | ❌ Still VDOM (but exploring) |
| TC39 Proposal | `Signal` (stage 1 — may become native JS) |

### What Is a Signal?

A signal is a reactive primitive that:
1. Holds a value
2. Tracks who reads it (subscribers/effects)
3. Notifies subscribers when the value changes

```javascript
// Conceptual implementation
function createSignal(initialValue) {
  let value = initialValue;
  const subscribers = new Set();

  function read() {
    // Track the current running effect as a subscriber
    if (currentEffect) subscribers.add(currentEffect);
    return value;
  }

  function write(newValue) {
    value = newValue;
    // Notify all subscribers
    subscribers.forEach((effect) => effect());
  }

  return [read, write];
}
```

**Why signals win:** They provide surgical DOM updates without the overhead of VDOM diffing or the complexity of manual subscriptions. The framework knows *exactly* which DOM nodes depend on which state.

---

## 📚 4. Meta-Frameworks — Why They Exist

A "meta-framework" adds server-side rendering (SSR), routing, data fetching, and deployment on top of a UI framework:

| UI Framework | Meta-Framework | Key Features |
|-------------|----------------|--------------|
| React | **Next.js** | App Router, RSC, ISR, Edge |
| Vue | **Nuxt** | Auto-imports, file routing, Nitro server |
| Svelte | **SvelteKit** | File routing, adapters, form actions |
| Solid | **SolidStart** | File routing, server functions |

**Why not just use React/Vue/Svelte alone?**
- **SEO** — SPAs are invisible to search engines without SSR
- **Performance** — Server rendering gives faster First Contentful Paint
- **DX** — File-based routing, automatic code splitting, built-in API routes
- **Deployment** — Adapters for Vercel, Cloudflare, AWS, etc.

---

## 📚 5. Decision Framework — Choosing a Framework

### For Your Projects (Bill's Context)

| Project | Recommended | Why |
|---------|-------------|-----|
| **AI Mobile IDE** (SaaS) | React + Next.js | Largest ecosystem, best for complex apps, most hirable |
| **BMX Clip Cutter** | Svelte + SvelteKit | Performance-critical video UI, small bundle |
| **NEPA-AI Tools** | React + Next.js | Enterprise clients expect React, SEO matters |
| **Personal portfolio** | Svelte or Astro | Simple, fast, minimal JS shipped |
| **Real-time dashboard** | Solid or Vue | Fine-grained updates for live data |
| **Learning/prototyping** | Svelte | Lowest friction, closest to vanilla JS |

### General Decision Tree

```
Need maximum hiring pool / ecosystem?
  → React + Next.js

Need best performance with minimal bundle?
  → Svelte + SvelteKit

Coming from React, want better perf without new syntax?
  → Solid + SolidStart

Want progressive adoption (add to existing site)?
  → Vue 3 (or Svelte with custom elements)

Building a content site (blog, docs, marketing)?
  → Astro (uses any framework for interactive islands)
```

---

## 📚 6. Performance Comparison (Benchmarks)

Based on [js-framework-benchmark](https://github.com/nicknisi/js-framework-benchmark) (2024 data):

| Metric | Solid | Svelte 5 | Vue 3 | React 18 |
|--------|-------|-----------|-------|----------|
| Create 1000 rows | 🏆 Fastest | Fast | Fast | Slowest |
| Update every 10th row | 🏆 Fastest | Fast | Fast | Slow |
| Swap rows | 🏆 Fastest | Fast | Medium | Slow |
| Startup time | 🏆 Fastest | Fast | Medium | Slowest |
| Memory usage | 🏆 Lowest | Low | Medium | Highest |
| Bundle size (hello world) | 7KB | 3KB | 33KB | 45KB |

**Important caveat:** Benchmarks measure synthetic scenarios. In real apps, the bottleneck is usually network I/O, not framework overhead. Choose based on DX, ecosystem, and team familiarity — not benchmarks alone.

---

## 📚 7. The "Islands" Architecture (Astro, Fresh)

A newer pattern that's gaining traction for content-heavy sites:

```
┌─────────────────────────────────────────────┐
│  Static HTML (server-rendered, zero JS)      │
│                                              │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐ │
│  │ React   │    │ Svelte  │    │ Vue     │ │
│  │ Island  │    │ Island  │    │ Island  │ │
│  │ (hydra- │    │ (hydra- │    │ (hydra- │ │
│  │  ted)   │    │  ted)   │    │  ted)   │ │
│  └─────────┘    └─────────┘    └─────────┘ │
│                                              │
│  Static HTML continues...                    │
└─────────────────────────────────────────────┘
```

- **Astro** — Build with any framework, ship zero JS by default, hydrate only interactive components
- **Fresh** (Deno) — Islands architecture with Preact
- **Qwik** — Resumability (no hydration cost at all)

---

## 🏋️ 8. Exercises

### Exercise 5.7.1 — Build the Same App in Two Frameworks

Build a todo app with:
- Add/remove/toggle items
- Filter (all/active/completed)
- Persist to localStorage

Build it in React AND Svelte. Compare: lines of code, bundle size, development experience.

### Exercise 5.7.2 — Framework Evaluation Matrix

For one of your SaaS projects, create a decision matrix scoring React, Vue, Svelte, and Solid on:
- Ecosystem maturity (libraries you need)
- Team scalability (hiring)
- Performance requirements
- Time to MVP
- Long-term maintenance

### Exercise 5.7.3 — Signals from Scratch

Implement a minimal signals system (~50 lines) that supports:
- `createSignal(value)` → `[getter, setter]`
- `createEffect(fn)` — auto-tracks signal dependencies
- `createMemo(fn)` — cached derived value

---

## 🔗 Cross-References

- **Deep React dive:** [22.1 - React & Next.js - Functional Components & Hooks](22.1---React-&-Next.js---Functional-Components-&-Hooks) — Full chapter on React internals, hooks, and Next.js.
- **Previous:** [12.6 - DOM & Browser APIs](12.6---DOM-&-Browser-APIs) — Frameworks abstract over these raw APIs.
- **Next:** [12.8 - Modern Backend - Node, Bun, Express, Fastify, Hono](12.8---Modern-Backend---Node,-Bun,-Express,-Fastify,-Hono) — The server side of full-stack JS.
- **TypeScript:** [13 - TypeScript](13---TypeScript) — All modern frameworks have first-class TS support.
- **Build tools:** [12.5 - Modules & Build Systems](12.5---Modules-&-Build-Systems) — Vite powers Svelte, Vue, Solid, and React dev servers.

---

## 📖 Further Reading

- [Theo Browne — "Which Framework Should You Use?"](https://www.youtube.com/watch?v=860d8usGC0o) — Opinionated ecosystem analysis
- [Rich Harris — "Rethinking Reactivity"](https://www.youtube.com/watch?v=AdNJ3fydeao) — Why Svelte exists
- [Ryan Carniato — "A Hands-on Introduction to Fine-Grained Reactivity"](https://dev.to/ryansolid/a-hands-on-introduction-to-fine-grained-reactivity-3ndf)
- [JS Framework Benchmark](https://krausest.github.io/js-framework-benchmark/) — Live performance comparisons
- [State of JS 2024](https://stateofjs.com) — Developer satisfaction and usage surveys



---

## 🏗️ 8. Extended Worked Examples & Deep Dives

### 8.1 — Framework Comparison Decision Matrix

#### Quantitative Comparison (2025 Data)

| Criterion | React 19 | Vue 3.5 | Svelte 5 | SolidJS 1.9 | Angular 18 |
|-----------|----------|---------|-----------|-------------|------------|
| **Bundle size (min+gz)** | 44KB | 33KB | 2KB (compiled) | 7KB | 90KB |
| **Startup time (TTI)** | Medium | Fast | Fastest | Fast | Slow |
| **Update perf (1000 rows)** | Good | Good | Excellent | Excellent | Good |
| **Memory usage** | Higher (vDOM) | Medium | Low | Low | Higher |
| **Learning curve** | Medium | Low | Low | Medium | High |
| **TypeScript DX** | Good | Excellent | Good | Excellent | Excellent |
| **Ecosystem size** | Massive | Large | Growing | Small | Large |
| **Job market** | Dominant | Strong (Asia/EU) | Growing | Niche | Enterprise |
| **SSR story** | Next.js, Remix | Nuxt | SvelteKit | SolidStart | Angular Universal |
| **Mobile** | React Native | Capacitor | Capacitor | — | Ionic |
| **Reactivity model** | Re-render (vDOM diff) | Proxy-based fine-grained | Compiler-based signals | Fine-grained signals | Zone.js → Signals |

#### Decision Flowchart

```
START: What are you building?
│
├─ Enterprise app with large team?
│  └─ Angular (opinionated, batteries-included)
│     OR React (if team prefers flexibility)
│
├─ Startup / SaaS product?
│  ├─ Need largest talent pool? → React + Next.js
│  ├─ Want best DX + performance? → Svelte + SvelteKit
│  └─ Want React-like but faster? → SolidJS + SolidStart
│
├─ Content-heavy site (blog, docs, marketing)?
│  └─ Astro (use any framework for interactive islands)
│
├─ Highly interactive dashboard / data-viz?
│  ├─ Need fine-grained updates? → SolidJS or Svelte
│  └─ Need ecosystem (charts, tables)? → React
│
├─ Mobile app?
│  ├─ Cross-platform native? → React Native
│  ├─ Web-based mobile? → Any + Capacitor
│  └─ Flutter-like? → Consider Flutter (not JS)
│
└─ Learning / personal project?
   └─ Try Svelte or SolidJS (modern patterns, less boilerplate)
      Then learn React (job market reality)
```

---

### 8.2 — React Server Components Mental Model

React Server Components (RSC) split your component tree into **Server Components** (run on server, zero JS shipped) and **Client Components** (run on both, hydrated on client).

#### The Mental Model

```
┌─────────────────────────────────────────────────────────────────┐
│                    REACT SERVER COMPONENTS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SERVER (Node.js / Edge)              CLIENT (Browser)           │
│  ─────────────────────                ──────────────────         │
│                                                                  │
│  ┌─────────────────────┐                                        │
│  │  Server Component    │  → Renders to HTML + RSC payload      │
│  │  (async, DB access,  │  → Ships ZERO JavaScript             │
│  │   file system, etc.) │  → Cannot use useState, useEffect    │
│  │                      │  → Cannot use event handlers         │
│  │  async function Page │  → CAN use: await, fs, db, env vars  │
│  └──────────┬───────────┘                                       │
│             │ renders                                            │
│             ▼                                                    │
│  ┌─────────────────────┐     ┌─────────────────────────────┐   │
│  │  Client Component    │────▶│  Hydrated on client          │   │
│  │  "use client"        │     │  useState, useEffect work    │   │
│  │                      │     │  Event handlers work         │   │
│  │  Interactive parts   │     │  JS bundle shipped           │   │
│  └─────────────────────┘     └─────────────────────────────┘   │
│                                                                  │
│  RULE: Server Components can import Client Components            │
│  RULE: Client Components CANNOT import Server Components         │
│  RULE: You can PASS Server Components as children to Client      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### Practical Example

```js
// app/page.tsx — Server Component (default in Next.js App Router)
// This runs ONLY on the server. Zero JS shipped to client.
import { db } from "@/lib/database";
import { ProductGrid } from "./ProductGrid"; // Client Component
import { formatPrice } from "@/lib/utils";

export default async function ProductsPage() {
  // Direct database access! No API route needed.
  const products = await db.product.findMany({
    where: { active: true },
    orderBy: { createdAt: "desc" },
  });

  return (
    <main>
      <h1>Products ({products.length})</h1>
      {/* Pass server-fetched data to client component */}
      <ProductGrid
        products={products.map(p => ({
          id: p.id,
          name: p.name,
          price: formatPrice(p.price),
          image: p.imageUrl,
        }))}
      />
    </main>
  );
}
```

```js
// app/ProductGrid.tsx — Client Component (interactive)
"use client"; // This directive marks it as a Client Component

import { useState, useTransition } from "react";
import { addToCart } from "./actions"; // Server Action

export function ProductGrid({ products }) {
  const [filter, setFilter] = useState("");
  const [isPending, startTransition] = useTransition();

  const filtered = products.filter(p =>
    p.name.toLowerCase().includes(filter.toLowerCase())
  );

  async function handleAddToCart(productId) {
    startTransition(async () => {
      await addToCart(productId); // Calls server action
    });
  }

  return (
    <div>
      <input
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        placeholder="Search products..."
      />
      <div className="grid">
        {filtered.map(product => (
          <div key={product.id} className="card">
            <img src={product.image} alt={product.name} />
            <h3>{product.name}</h3>
            <p>{product.price}</p>
            <button
              onClick={() => handleAddToCart(product.id)}
              disabled={isPending}
            >
              {isPending ? "Adding..." : "Add to Cart"}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
```

```js
// app/actions.ts — Server Action (runs on server, called from client)
"use server";

import { db } from "@/lib/database";
import { revalidatePath } from "next/cache";

export async function addToCart(productId) {
  const session = await getSession();
  await db.cart.create({
    data: { userId: session.userId, productId, quantity: 1 },
  });
  revalidatePath("/cart"); // Invalidate cache, trigger re-render
}
```

---

### 8.3 — Vue Vapor Mode (Compilation Without Virtual DOM)

Vue Vapor Mode (experimental, Vue 3.5+) compiles templates to direct DOM operations — no virtual DOM diffing at runtime.

```js
// Standard Vue (virtual DOM):
// Template → render function → creates vNodes → diffs → patches DOM

// Vapor Mode:
// Template → compiled to direct DOM manipulation code
// No vNode creation, no diffing algorithm, no runtime overhead

// What the compiler generates (conceptual):
// Input template:
// <div>
//   <h1>{{ title }}</h1>
//   <p v-if="show">{{ message }}</p>
//   <button @click="count++">{{ count }}</button>
// </div>

// Vapor output (simplified):
function setup() {
  const title = ref("Hello");
  const show = ref(true);
  const message = ref("World");
  const count = ref(0);

  // Direct DOM creation (no vDOM)
  const div = document.createElement("div");
  const h1 = document.createElement("h1");
  const button = document.createElement("button");

  div.appendChild(h1);
  div.appendChild(button);

  // Fine-grained reactivity: only update what changed
  watchEffect(() => {
    h1.textContent = title.value;
  });

  watchEffect(() => {
    button.textContent = count.value;
  });

  // Conditional rendering without vDOM diff
  let pElement = null;
  watchEffect(() => {
    if (show.value) {
      if (!pElement) {
        pElement = document.createElement("p");
        div.insertBefore(pElement, button);
      }
      pElement.textContent = message.value;
    } else if (pElement) {
      pElement.remove();
      pElement = null;
    }
  });

  button.addEventListener("click", () => count.value++);

  return div;
}
```

#### Performance Implications

| Metric | Vue (vDOM) | Vue Vapor | Improvement |
|--------|-----------|-----------|-------------|
| Bundle size | ~33KB | ~6KB | -82% |
| Memory per component | Higher (vNodes) | Minimal | -70% |
| Update speed (1 prop) | O(tree) diff | O(1) direct | 10-50x |
| Initial render | Create vNodes + patch | Direct DOM | 2-3x |
| Best for | Complex UIs, large trees | Many small components | — |

---

### 8.4 — SolidJS Reactivity: Signals, Effects, and Memos

SolidJS uses **fine-grained reactivity** — no virtual DOM, no component re-renders. Only the exact DOM nodes that depend on changed data update.

```js
import { createSignal, createEffect, createMemo, onCleanup, batch } from "solid-js";
import { render } from "solid-js/web";

function Counter() {
  // Signal: reactive primitive (getter + setter)
  const [count, setCount] = createSignal(0);
  const [name, setName] = createSignal("Bill");

  // Memo: cached derived value (only recomputes when dependencies change)
  const doubled = createMemo(() => count() * 2);
  const message = createMemo(() => `${name()} clicked ${count()} times`);

  // Effect: side effect that auto-tracks dependencies
  createEffect(() => {
    console.log(`Count is now: ${count()}`);
    // Automatically re-runs when count() changes
    // Does NOT re-run when name() changes (not accessed here)
  });

  // Cleanup function (like useEffect cleanup)
  createEffect(() => {
    const interval = setInterval(() => console.log("tick"), 1000);
    onCleanup(() => clearInterval(interval));
  });

  return (
    <div>
      {/* This text node updates directly — no component re-render! */}
      <h1>{message()}</h1>
      <p>Doubled: {doubled()}</p>
      <button onClick={() => setCount(c => c + 1)}>
        Increment
      </button>
      <input
        value={name()}
        onInput={(e) => setName(e.target.value)}
      />
    </div>
  );
}

// KEY DIFFERENCE FROM REACT:
// In React: setCount(1) → entire Counter function re-runs → vDOM diff → patch
// In Solid: setCount(1) → ONLY the text node showing count updates
// The Counter function runs ONCE (setup), never again!

render(() => <Counter />, document.getElementById("root"));
```

#### How Solid's Reactivity Works Under the Hood

```js
// Simplified reactive system (what Solid does internally)
let currentObserver = null;

function createSignal(initialValue) {
  let value = initialValue;
  const subscribers = new Set();

  function getter() {
    // Track: record that current effect depends on this signal
    if (currentObserver) {
      subscribers.add(currentObserver);
    }
    return value;
  }

  function setter(newValue) {
    if (typeof newValue === "function") {
      newValue = newValue(value);
    }
    if (value !== newValue) {
      value = newValue;
      // Trigger: notify all effects that depend on this signal
      for (const subscriber of [...subscribers]) {
        subscriber();
      }
    }
  }

  return [getter, setter];
}

function createEffect(fn) {
  function execute() {
    currentObserver = execute; // Set ourselves as the current observer
    fn();                      // Run the effect (signals will track us)
    currentObserver = null;    // Clear
  }
  execute(); // Run immediately to establish subscriptions
}

// This is the core of ALL signal-based frameworks:
// Solid, Vue 3 (Composition API), Preact Signals, Angular Signals, Svelte 5 runes
```

---

### 8.5 — Framework Performance: Benchmark Analysis

```js
// JS Framework Benchmark — key operations measured:

// 1. Create 1,000 rows
// 2. Replace all 1,000 rows
// 3. Partial update (every 10th row)
// 4. Select row (highlight)
// 5. Swap rows
// 6. Remove row
// 7. Create 10,000 rows
// 8. Append 1,000 rows
// 9. Clear all rows
// 10. Startup time
// 11. Memory allocation

// Typical results (geometric mean, lower is better):
// 1.00 = vanilla JS baseline

// Framework          | Perf Score | Bundle | Memory
// -------------------|-----------|--------|--------
// Vanilla JS         | 1.00      | 0KB    | Low
// SolidJS            | 1.05      | 7KB    | Low
// Svelte 5           | 1.08      | 2KB*   | Low
// Vue Vapor          | 1.10      | 6KB    | Low
// Preact + Signals   | 1.15      | 4KB    | Low
// Vue 3              | 1.25      | 33KB   | Medium
// React 19           | 1.40      | 44KB   | Higher
// Angular 18         | 1.45      | 90KB   | Higher

// * Svelte's 2KB is the runtime; component code adds to bundle
// These numbers are from krausest.github.io/js-framework-benchmark

// WHY signal-based frameworks are faster:
// 1. No virtual DOM creation (no object allocation per render)
// 2. No diffing algorithm (O(n) tree walk eliminated)
// 3. Surgical DOM updates (only changed nodes touched)
// 4. Less GC pressure (fewer short-lived objects)
```

#### When Virtual DOM Wins

```
Virtual DOM advantages:
1. Predictable performance ceiling (never catastrophically slow)
2. Easy to reason about (render = f(state), always consistent)
3. Enables time-slicing (React Concurrent Mode — pause/resume rendering)
4. Cross-platform (React Native renders to native views, not DOM)
5. Server rendering is natural (render to string)

Fine-grained reactivity advantages:
1. Better best-case performance (surgical updates)
2. Lower memory usage (no vNode tree in memory)
3. Smaller bundle (no diffing algorithm shipped)
4. More predictable performance (no surprise re-renders)
5. Better for real-time UIs (dashboards, games, animations)

The tradeoff:
- vDOM: O(tree_size) per update, but consistent and predictable
- Signals: O(changed_nodes) per update, but subscription management overhead
- For most apps: the difference is imperceptible to users
- Choose based on: ecosystem, team familiarity, specific requirements
```




---

## 📎 9. Appendix: Extended Derivations & Special Cases

### 9.1 — Virtual DOM vs Fine-Grained Reactivity: The Math

#### Virtual DOM Cost Model

```
For a component tree with N nodes:

RENDER COST = create_vnode × N_rendered + diff × N_compared + patch × N_changed

Where:
- N_rendered: nodes whose render function runs (component + children)
- N_compared: nodes the diff algorithm must compare (usually = N_rendered)
- N_changed: nodes that actually need DOM updates

Example: Update 1 text node in a list of 1000 items
- React (no memo): N_rendered = 1000, N_compared = 1000, N_changed = 1
  Cost: 1000 × create_vnode + 1000 × diff + 1 × patch
  
- React (with memo): N_rendered = 1, N_compared = 1, N_changed = 1
  Cost: 1 × create_vnode + 1 × diff + 1 × patch
  (But: developer must manually add React.memo/useMemo)

- React (Compiler, React 19+): Auto-memoizes, approaches optimal
  Cost: ~1 × create_vnode + ~1 × diff + 1 × patch
```

#### Fine-Grained Reactivity Cost Model

```
For a reactive system with S signals and E effects:

UPDATE COST = notify × S_changed + execute × E_dependent + patch × N_changed

Where:
- S_changed: number of signals that changed
- E_dependent: effects subscribed to those signals
- N_changed: DOM nodes to update (usually = E_dependent)

Example: Update 1 text node in a list of 1000 items
- SolidJS: S_changed = 1, E_dependent = 1, N_changed = 1
  Cost: 1 × notify + 1 × execute + 1 × patch
  (Optimal! No wasted work regardless of tree size)

SUBSCRIPTION OVERHEAD:
- Memory: O(S × E_avg) for subscription tracking
- Setup: O(N) initial subscription creation
- Teardown: O(subscriptions) when components unmount

For LARGE trees with FEW updates: signals win decisively
For SMALL trees with MANY updates: difference is negligible
For BULK updates (replace entire list): vDOM can be competitive
```

#### Reconciliation Algorithm Complexity

```
React's reconciliation (simplified):
1. Same type? → Update props, recurse into children
2. Different type? → Unmount old, mount new
3. Lists? → Use keys for O(n) matching (without keys: O(n²))

Complexity:
- Best case: O(n) where n = tree depth (no changes)
- Typical: O(m) where m = number of changed subtrees
- Worst case: O(n) full tree walk (every node changed)

The "key" optimization for lists:
- Without keys: [A, B, C] → [B, C, A] = unmount A, B, C; mount B, C, A (6 ops)
- With keys: [A, B, C] → [B, C, A] = move A to end (1 op)
- React uses a single-pass left-to-right algorithm
- Vue uses a two-pointer algorithm (slightly better for edge cases)
```

---

### 9.2 — Hydration vs Streaming SSR

#### Traditional SSR + Hydration

```
SERVER                              CLIENT
──────                              ──────
1. Render components to HTML        4. Download HTML (fast FCP!)
2. Serialize state                  5. Download JS bundle
3. Send complete HTML               6. Parse + execute JS
                                    7. HYDRATION:
                                       - Walk DOM tree
                                       - Attach event listeners
                                       - Reconcile server HTML with client vDOM
                                       - Make page interactive (TTI)

Timeline:
[─── Server Render ───][─── Network ───][─── Download JS ───][─── Hydrate ───]
                                         ↑ FCP                                ↑ TTI
                                         (visible but                         (interactive)
                                          not interactive)

Problem: "Uncanny Valley" — page LOOKS ready but doesn't respond to clicks
Duration: can be 2-5 seconds on slow devices!
```

#### Streaming SSR (React 18+)

```
SERVER                              CLIENT
──────                              ──────
1. Start rendering                  3. Receive HTML chunks progressively
2. Stream HTML as components        4. Display content as it arrives
   finish rendering                 5. Hydrate components as their JS loads
   (don't wait for slow ones!)         (selective/progressive hydration)

Timeline:
[─ Fast components ─][─── Slow component ───]
        ↓                      ↓
[─ Stream HTML ─────][─ Suspense fallback ─][─ Stream slow content ─]
        ↓                                           ↓
[─ Hydrate fast ─]                          [─ Hydrate slow ─]
  ↑ Interactive!                              ↑ Fully interactive

Benefits:
- TTFB is faster (don't wait for slowest component)
- Progressive display (users see content sooner)
- Selective hydration (interact with fast parts while slow parts load)
- Suspense boundaries define streaming chunks
```

```js
// Next.js App Router — Streaming with Suspense
import { Suspense } from "react";

export default function Page() {
  return (
    <main>
      {/* This renders immediately */}
      <Header />

      {/* This streams in when ready */}
      <Suspense fallback={<ProductsSkeleton />}>
        <ProductList /> {/* async component — may take 2s */}
      </Suspense>

      {/* This also streams independently */}
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews /> {/* async component — may take 3s */}
      </Suspense>

      {/* This renders immediately */}
      <Footer />
    </main>
  );
}

// The HTML streams as:
// 1. <header> + <skeleton1> + <skeleton2> + <footer> (instant)
// 2. <script> replaces skeleton1 with ProductList content (2s later)
// 3. <script> replaces skeleton2 with Reviews content (3s later)
```

#### Partial Hydration / Islands Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  ISLANDS ARCHITECTURE (Astro, Fresh, Eleventy)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Static HTML (no JS)     Interactive Island     Static HTML      │
│  ┌──────────────────┐   ┌─────────────────┐   ┌────────────┐  │
│  │  <header>         │   │  <SearchBar>     │   │  <article>  │  │
│  │  <nav>            │   │  (React/Vue/     │   │  <p>...</p> │  │
│  │  <h1>Title</h1>   │   │   Svelte/Solid)  │   │  <p>...</p> │  │
│  │                   │   │  JS: 5KB         │   │             │  │
│  └──────────────────┘   └─────────────────┘   └────────────┘  │
│                                                                  │
│  Static HTML             Interactive Island     Static HTML      │
│  ┌──────────────────┐   ┌─────────────────┐   ┌────────────┐  │
│  │  <section>        │   │  <AddToCart>     │   │  <footer>   │  │
│  │  <img>            │   │  JS: 3KB         │   │  <links>    │  │
│  │  <p>description   │   │                  │   │             │  │
│  └──────────────────┘   └─────────────────┘   └────────────┘  │
│                                                                  │
│  Total JS shipped: 8KB (only interactive parts)                 │
│  vs SPA: 200KB+ (entire framework + all components)             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

```js
// Astro — Islands architecture
// src/pages/index.astro
---
import Header from "../components/Header.astro"; // Zero JS
import SearchBar from "../components/SearchBar.tsx"; // React island
import ProductCard from "../components/ProductCard.astro"; // Zero JS
import AddToCart from "../components/AddToCart.svelte"; // Svelte island
---

<html>
  <body>
    <Header />

    <!-- Hydrate on page load -->
    <SearchBar client:load />

    <!-- Hydrate when visible (lazy) -->
    <AddToCart client:visible />

    <!-- Hydrate on idle (requestIdleCallback) -->
    <Newsletter client:idle />

    <!-- Hydrate on media query match -->
    <MobileMenu client:media="(max-width: 768px)" />

    <!-- Never hydrate (render HTML only, even if it's a React component) -->
    <StaticChart client:only="react" />

    <!-- Static components — zero JS -->
    <ProductCard />
    <Footer />
  </body>
</html>
```

---

### 9.3 — React Compiler (React Forget)

```js
// React Compiler (shipping with React 19) auto-memoizes components
// You no longer need: useMemo, useCallback, React.memo (in most cases)

// BEFORE (manual memoization):
function TodoList({ todos, filter }) {
  const filteredTodos = useMemo(
    () => todos.filter(t => t.status === filter),
    [todos, filter]
  );

  const handleToggle = useCallback(
    (id) => dispatch({ type: "toggle", id }),
    [dispatch]
  );

  return filteredTodos.map(todo => (
    <TodoItem key={todo.id} todo={todo} onToggle={handleToggle} />
  ));
}

const TodoItem = React.memo(function TodoItem({ todo, onToggle }) {
  return <li onClick={() => onToggle(todo.id)}>{todo.text}</li>;
});

// AFTER (React Compiler handles it automatically):
function TodoList({ todos, filter }) {
  const filteredTodos = todos.filter(t => t.status === filter);

  const handleToggle = (id) => dispatch({ type: "toggle", id });

  return filteredTodos.map(todo => (
    <TodoItem key={todo.id} todo={todo} onToggle={handleToggle} />
  ));
}

function TodoItem({ todo, onToggle }) {
  return <li onClick={() => onToggle(todo.id)}>{todo.text}</li>;
}

// The compiler analyzes data flow and inserts memoization automatically
// It understands: which values change between renders, which are stable
// Result: same performance as hand-optimized code, zero developer effort
```

---

### 9.4 — Svelte 5 Runes (The New Reactivity)

```js
// Svelte 5 replaces stores and $: with "runes" — explicit reactivity primitives

// $state — reactive state (like signals)
let count = $state(0);
let user = $state({ name: "Bill", age: 30 });

// $derived — computed values (like memos)
let doubled = $derived(count * 2);
let greeting = $derived(`Hello, ${user.name}!`);

// $effect — side effects (like createEffect in Solid)
$effect(() => {
  console.log(`Count changed to: ${count}`);
  // Auto-tracks dependencies — re-runs when count changes
});

// $props — component props
// Button.svelte
let { label, onClick, disabled = false } = $props();

// Deep reactivity (Svelte 5 uses Proxies like Vue)
let todos = $state([
  { text: "Learn Svelte 5", done: false },
  { text: "Build app", done: false },
]);

// Mutations are reactive! (unlike React where you need new references)
todos.push({ text: "Deploy", done: false }); // Triggers update!
todos[0].done = true; // Triggers update!

// $state.frozen — opt out of deep reactivity (for large immutable data)
let largeDataset = $state.frozen(fetchedData);
// Mutations won't be tracked — must replace entirely to trigger update
```

---

### 9.5 — Angular Signals & Zoneless Change Detection

```ts
// Angular 18+ — Signals replace Zone.js for change detection
import { signal, computed, effect } from "@angular/core";

@Component({
  selector: "app-counter",
  // Zoneless: Angular only updates when signals change
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <h1>{{ count() }}</h1>
    <p>Doubled: {{ doubled() }}</p>
    <button (click)="increment()">+1</button>
  `,
})
export class CounterComponent {
  count = signal(0);
  doubled = computed(() => this.count() * 2);

  constructor() {
    effect(() => {
      console.log(`Count: ${this.count()}`);
    });
  }

  increment() {
    this.count.update(c => c + 1);
    // OR: this.count.set(this.count() + 1);
  }
}

// Why signals replace Zone.js:
// Zone.js: patches ALL async APIs (setTimeout, Promise, fetch, etc.)
//          → triggers change detection on EVERY async operation
//          → checks ENTIRE component tree for changes
//          → expensive for large apps!
//
// Signals: only components reading changed signals re-render
//          → no monkey-patching of browser APIs
//          → surgical updates (like Solid/Vue)
//          → smaller bundle (no zone.js ~13KB)
```

---

*Last updated: 2026-05-24*
