---
title: "12.3 — Async: Promises, Async/Await, Event Loop"
subject: "JavaScript"
catalog: advanced
audience_tier: higher-education
chapter: "12.3"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 12.3 — Async: Promises, Async/Await, Event Loop

> *"The event loop is the beating heart of JavaScript. If you don't understand it, you don't understand JavaScript."* — **Philip Roberts**, creator of Loupe (JSConf EU 2014)

JavaScript is **single-threaded**. It has ONE call stack, ONE thread of execution. Yet it handles thousands of concurrent network requests, timers, and user interactions without blocking. How? The **event loop** — a deceptively simple algorithm that orchestrates asynchronous execution through task queues.

This chapter derives the event loop step by step, then builds your async programming skills from callbacks through Promises to modern async/await patterns.

---

## 🎯 Learning Objectives

1. **Trace the event loop algorithm** step by step — call stack, Web APIs, microtask queue, macrotask queue.
2. **Predict execution order** for any mix of synchronous code, `setTimeout`, `Promise.then`, `queueMicrotask`, and `async/await`.
3. **Implement Promise-based APIs** using the constructor, chaining, and error propagation.
4. **Use all Promise combinators** — `all`, `allSettled`, `race`, `any` — and know when each is appropriate.
5. **Write production async code** with proper error handling, cancellation (`AbortController`), and timeout patterns.
6. **Implement async iterators** for streaming data consumption.

---

## 🖼️ Visual Anchor — The Event Loop

![js__5.3-fig1](js__5.3-fig1.svg)

---

## 📚 1. The Event Loop — Derived from First Principles

### Why Single-Threaded?

JavaScript was designed for the browser DOM. If two threads could modify the DOM simultaneously, you'd need locks, mutexes, and all the complexity of concurrent programming. Brendan Eich chose simplicity: **one thread, cooperative multitasking via an event loop**.

### Definition 12.3.1 — The Components

```
┌─────────────────────────────────────────────────────────────┐
│                    JAVASCRIPT RUNTIME                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────────────────────────┐   │
│  │  CALL STACK  │    │  WEB APIs / Runtime APIs          │   │
│  │              │    │  (setTimeout, fetch, DOM events,  │   │
│  │  main()      │    │   file I/O, network...)           │   │
│  │  fn1()       │    └──────────────┬───────────────────┘   │
│  │  fn2()       │                   │                        │
│  └──────┬───────┘                   │ callbacks ready        │
│         │                           ▼                        │
│         │         ┌─────────────────────────────────┐        │
│         │         │  MICROTASK QUEUE (Job Queue)     │        │
│         │         │  Promise.then, queueMicrotask,   │        │
│         │         │  MutationObserver, async/await    │        │
│         │         └─────────────────┬───────────────┘        │
│         │                           │                        │
│         │         ┌─────────────────────────────────┐        │
│         │         │  MACROTASK QUEUE (Task Queue)    │        │
│         │         │  setTimeout, setInterval,        │        │
│         │         │  I/O callbacks, UI rendering     │        │
│         │         └─────────────────┬───────────────┘        │
│         │                           │                        │
│         ▼                           ▼                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              EVENT LOOP ALGORITHM                      │   │
│  │  1. Execute all synchronous code (drain call stack)   │   │
│  │  2. Drain ALL microtasks (until queue empty)          │   │
│  │  3. Execute ONE macrotask                             │   │
│  │  4. Drain ALL microtasks again                        │   │
│  │  5. Render (browser only: rAF, paint, layout)         │   │
│  │  6. Go to step 3                                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Definition 12.3.2 — The Event Loop Algorithm (Pseudocode)

```javascript
while (true) {
  // 1. Pick ONE macrotask from the macrotask queue (or wait for one)
  const macrotask = macrotaskQueue.dequeue();
  execute(macrotask); // This may push microtasks

  // 2. Drain ALL microtasks
  while (microtaskQueue.length > 0) {
    const microtask = microtaskQueue.dequeue();
    execute(microtask); // This may push MORE microtasks!
  }

  // 3. Render (browser only)
  if (needsRender()) {
    runRequestAnimationFrameCallbacks();
    render();
  }
}
```

**Critical insight:** Microtasks are drained **completely** before the next macrotask. A microtask that enqueues another microtask will be processed in the same cycle. This means microtasks can starve macrotasks (and rendering!).

### Definition 12.3.3 — Microtasks vs Macrotasks

| Microtasks (higher priority) | Macrotasks (lower priority) |
|-----------------------------|-----------------------------|
| `Promise.then/catch/finally` | `setTimeout` / `setInterval` |
| `queueMicrotask()` | `setImmediate` (Node.js) |
| `MutationObserver` | I/O callbacks |
| `async/await` continuations | `requestAnimationFrame` (debated) |
| `process.nextTick` (Node.js, even higher!) | UI rendering events |

---

## 📐 2. Loupe-Style Execution Traces

### Trace 5.3.1 — The Classic Interview Question

```javascript
console.log("1");

setTimeout(() => console.log("2"), 0);

Promise.resolve().then(() => console.log("3"));

queueMicrotask(() => console.log("4"));

console.log("5");
```

**Step-by-step trace:**

| Step | Call Stack | Microtask Queue | Macrotask Queue | Output |
|------|-----------|-----------------|-----------------|--------|
| 1 | `console.log("1")` | — | — | `1` |
| 2 | `setTimeout(cb, 0)` | — | `[cb→"2"]` | — |
| 3 | `Promise.resolve().then(cb)` | `[cb→"3"]` | `[cb→"2"]` | — |
| 4 | `queueMicrotask(cb)` | `[cb→"3", cb→"4"]` | `[cb→"2"]` | — |
| 5 | `console.log("5")` | `[cb→"3", cb→"4"]` | `[cb→"2"]` | `5` |
| 6 | — (stack empty, drain microtasks) | `[cb→"4"]` | `[cb→"2"]` | `3` |
| 7 | — (continue draining) | `[]` | `[cb→"2"]` | `4` |
| 8 | — (microtasks empty, pick macrotask) | — | `[]` | `2` |

**Final output:** `1, 5, 3, 4, 2`

### Trace 5.3.2 — Nested Microtasks

```javascript
Promise.resolve().then(() => {
  console.log("A");
  Promise.resolve().then(() => console.log("B"));
});

Promise.resolve().then(() => console.log("C"));

setTimeout(() => console.log("D"), 0);
```

| Step | Action | Output |
|------|--------|--------|
| 1 | Sync done. Microtask queue: `[cb→A, cb→C]`. Macrotask: `[cb→D]` | — |
| 2 | Execute cb→A. Logs "A". Enqueues cb→B. Queue: `[cb→C, cb→B]` | `A` |
| 3 | Execute cb→C. Logs "C". Queue: `[cb→B]` | `C` |
| 4 | Execute cb→B. Logs "B". Queue: `[]` | `B` |
| 5 | Microtasks empty. Execute macrotask cb→D. | `D` |

**Final output:** `A, C, B, D`

### Trace 5.3.3 — async/await Desugaring

```javascript
async function foo() {
  console.log("foo start");
  await bar();
  console.log("foo end"); // This becomes a microtask!
}

async function bar() {
  console.log("bar");
}

console.log("script start");
foo();
console.log("script end");
```

**Key insight:** `await` splits the function. Everything after `await` is wrapped in a `.then()` callback (microtask):

```javascript
// foo() desugars to approximately:
function foo() {
  console.log("foo start");
  return bar().then(() => {
    console.log("foo end");
  });
}
```

| Step | Action | Output |
|------|--------|--------|
| 1 | `console.log("script start")` | `script start` |
| 2 | Call `foo()` → `console.log("foo start")` | `foo start` |
| 3 | Call `bar()` → `console.log("bar")` | `bar` |
| 4 | `await` suspends foo. Enqueues continuation. Return to caller. | — |
| 5 | `console.log("script end")` | `script end` |
| 6 | Stack empty. Drain microtasks: foo continuation | `foo end` |

**Final output:** `script start, foo start, bar, script end, foo end`

---

## 📚 3. Promises — The Foundation

### Definition 12.3.4 — Promise States

A Promise is a **state machine** with three states:

```
         ┌──── fulfill(value) ────→ FULFILLED
         │                           │
PENDING ─┤                           ├──→ .then(onFulfilled)
         │                           │
         └──── reject(reason) ────→ REJECTED
                                     │
                                     └──→ .catch(onRejected)
```

- **Pending** — initial state, neither fulfilled nor rejected
- **Fulfilled** — operation completed successfully
- **Rejected** — operation failed
- **Settled** — either fulfilled or rejected (final, immutable)

### Definition 12.3.5 — Promise Constructor

```javascript
const promise = new Promise((resolve, reject) => {
  // Executor runs SYNCHRONOUSLY
  const data = doSomething();
  
  if (data) {
    resolve(data);  // Transition to fulfilled
  } else {
    reject(new Error("Failed")); // Transition to rejected
  }
});
```

**Important:** The executor function runs **synchronously**. Only the `.then`/`.catch` callbacks are asynchronous (microtasks).

### Definition 12.3.6 — Promise Chaining

`.then()` always returns a NEW Promise, enabling chaining:

```javascript
fetch("/api/user/1")
  .then((response) => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json(); // Returns a Promise → next .then waits for it
  })
  .then((user) => {
    console.log(user.name);
    return fetch(`/api/posts?userId=${user.id}`);
  })
  .then((response) => response.json())
  .then((posts) => console.log(`${posts.length} posts`))
  .catch((err) => {
    // Catches ANY error in the chain above
    console.error("Pipeline failed:", err.message);
  })
  .finally(() => {
    // Runs regardless of success/failure (cleanup)
    hideLoadingSpinner();
  });
```

**Error propagation:** A rejected Promise (or thrown error) skips all `.then()` handlers until it hits a `.catch()`. This is analogous to try/catch — errors "bubble up" the chain.

---

## 📚 4. Promise Combinators

### `Promise.all()` — All must succeed

```javascript
const [users, posts, comments] = await Promise.all([
  fetch("/api/users").then((r) => r.json()),
  fetch("/api/posts").then((r) => r.json()),
  fetch("/api/comments").then((r) => r.json()),
]);
// All three requests run in PARALLEL
// If ANY rejects, the whole thing rejects immediately (fail-fast)
```

### `Promise.allSettled()` — Wait for all, regardless of outcome

```javascript
const results = await Promise.allSettled([
  fetch("/api/critical"),    // might fail
  fetch("/api/optional"),    // might fail
  fetch("/api/analytics"),   // might fail
]);

results.forEach((result, i) => {
  if (result.status === "fulfilled") {
    console.log(`Request ${i}: success`, result.value);
  } else {
    console.log(`Request ${i}: failed`, result.reason);
  }
});
// Never rejects — always resolves with array of {status, value/reason}
```

### `Promise.race()` — First to settle wins

```javascript
// Timeout pattern
function fetchWithTimeout(url, ms) {
  return Promise.race([
    fetch(url),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error("Timeout")), ms)
    ),
  ]);
}

const data = await fetchWithTimeout("/api/slow", 5000);
```

### `Promise.any()` — First to FULFILL wins

```javascript
// Try multiple CDNs, use whichever responds first
const asset = await Promise.any([
  fetch("https://cdn1.example.com/bundle.js"),
  fetch("https://cdn2.example.com/bundle.js"),
  fetch("https://cdn3.example.com/bundle.js"),
]);
// Only rejects if ALL reject (AggregateError)
```

### Combinator Comparison Table

| Combinator | Resolves when | Rejects when | Use case |
|-----------|---------------|--------------|----------|
| `all` | ALL fulfill | ANY rejects | Parallel independent requests |
| `allSettled` | ALL settle | Never | Batch operations, partial failure OK |
| `race` | First settles | First settles (if rejected) | Timeouts, fastest mirror |
| `any` | First fulfills | ALL reject | Redundant sources, fallbacks |

---

## 📚 5. async/await — Syntactic Sugar Done Right

### Definition 12.3.7 — async Functions

An `async` function always returns a Promise. `await` pauses execution until the awaited Promise settles:

```javascript
// These are equivalent:
async function getUser(id) {
  const response = await fetch(`/api/users/${id}`);
  const user = await response.json();
  return user; // Wrapped in Promise.resolve(user)
}

function getUser(id) {
  return fetch(`/api/users/${id}`)
    .then((response) => response.json());
}
```

### Error Handling with async/await

```javascript
// Pattern 1: try/catch (most common)
async function loadData() {
  try {
    const res = await fetch("/api/data");
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error("Load failed:", err.message);
    return null; // Graceful fallback
  }
}

// Pattern 2: .catch() on the await (inline)
const data = await fetch("/api/data").catch(() => null);

// Pattern 3: Go-style tuple (no try/catch nesting)
async function to(promise) {
  try {
    const result = await promise;
    return [null, result];
  } catch (err) {
    return [err, null];
  }
}

const [err, user] = await to(fetchUser(42));
if (err) {
  console.error("Failed:", err.message);
} else {
  console.log("Got user:", user.name);
}
```

### Sequential vs Parallel Execution

```javascript
// ❌ SEQUENTIAL — each awaits before starting the next (slow!)
async function sequential() {
  const users = await fetchUsers();     // 500ms
  const posts = await fetchPosts();     // 500ms
  const comments = await fetchComments(); // 500ms
  // Total: ~1500ms
}

// ✅ PARALLEL — start all, then await results
async function parallel() {
  const [users, posts, comments] = await Promise.all([
    fetchUsers(),     // 500ms ─┐
    fetchPosts(),     // 500ms ─┼─ run simultaneously
    fetchComments(),  // 500ms ─┘
  ]);
  // Total: ~500ms
}

// ✅ START EARLY, AWAIT LATE — when you need intermediate results
async function hybrid() {
  const usersPromise = fetchUsers(); // Start immediately
  const postsPromise = fetchPosts(); // Start immediately

  const users = await usersPromise;
  // Do something with users while posts might still be loading
  const filteredIds = users.filter((u) => u.active).map((u) => u.id);

  const posts = await postsPromise;
  return posts.filter((p) => filteredIds.includes(p.authorId));
}
```

---

## 📚 6. AbortController — Cancellation

```javascript
// Create a controller
const controller = new AbortController();
const { signal } = controller;

// Pass signal to fetch
const fetchPromise = fetch("/api/large-data", { signal });

// Cancel after 5 seconds
setTimeout(() => controller.abort(), 5000);

try {
  const response = await fetchPromise;
  const data = await response.json();
} catch (err) {
  if (err.name === "AbortError") {
    console.log("Request was cancelled");
  } else {
    throw err; // Re-throw non-cancellation errors
  }
}
```

### Reusable Timeout Utility

```javascript
function fetchWithTimeout(url, options = {}, timeoutMs = 5000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  return fetch(url, {
    ...options,
    signal: AbortSignal.any([
      controller.signal,
      ...(options.signal ? [options.signal] : []),
    ]),
  }).finally(() => clearTimeout(timeoutId));
}

// AbortSignal.any() (ES2024) — abort if ANY signal fires
const userController = new AbortController();
const data = await fetchWithTimeout("/api/data", {
  signal: userController.signal, // User can also cancel
}, 10000);
```

### AbortSignal.timeout() (ES2024)

```javascript
// Even simpler — built-in timeout signal
const response = await fetch("/api/data", {
  signal: AbortSignal.timeout(5000), // Auto-abort after 5s
});
```

---

## 📚 7. Async Iteration

### Definition 12.3.8 — Async Iterators

For consuming data that arrives over time (streams, paginated APIs, WebSocket messages):

```javascript
// Async generator
async function* fetchPages(baseUrl) {
  let page = 1;
  let hasMore = true;

  while (hasMore) {
    const res = await fetch(`${baseUrl}?page=${page}`);
    const data = await res.json();
    yield data.items;
    hasMore = data.hasNextPage;
    page++;
  }
}

// Consume with for-await-of
for await (const items of fetchPages("/api/products")) {
  items.forEach((item) => renderProduct(item));
}
```

### ReadableStream Consumption

```javascript
// Streaming a large response body
async function streamResponse(url) {
  const response = await fetch(url);
  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value, { stream: true });
    process.stdout.write(chunk); // Or append to DOM
  }
}
```

---

## 📚 8. Advanced Patterns

### Pattern: Retry with Exponential Backoff

```javascript
async function retry(fn, { maxAttempts = 3, baseDelay = 1000 } = {}) {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (attempt === maxAttempts) throw err;
      const delay = baseDelay * 2 ** (attempt - 1); // 1s, 2s, 4s...
      const jitter = Math.random() * delay * 0.1;   // ±10% jitter
      await new Promise((r) => setTimeout(r, delay + jitter));
      console.warn(`Attempt ${attempt} failed, retrying in ${delay}ms...`);
    }
  }
}

const data = await retry(() => fetch("/api/flaky").then((r) => r.json()));
```

### Pattern: Concurrency Limiter

```javascript
async function mapWithConcurrency(items, fn, concurrency = 5) {
  const results = [];
  const executing = new Set();

  for (const [index, item] of items.entries()) {
    const promise = fn(item, index).then((result) => {
      executing.delete(promise);
      return result;
    });
    executing.add(promise);
    results.push(promise);

    if (executing.size >= concurrency) {
      await Promise.race(executing);
    }
  }

  return Promise.all(results);
}

// Process 100 URLs, max 5 concurrent requests
const responses = await mapWithConcurrency(
  urls,
  (url) => fetch(url).then((r) => r.json()),
  5
);
```

### Pattern: Debounce with Promises

```javascript
function debounceAsync(fn, ms) {
  let timeoutId;
  let pendingResolvers = [];

  return function (...args) {
    clearTimeout(timeoutId);

    return new Promise((resolve, reject) => {
      pendingResolvers.push({ resolve, reject });

      timeoutId = setTimeout(async () => {
        const resolvers = pendingResolvers;
        pendingResolvers = [];
        try {
          const result = await fn.apply(this, args);
          resolvers.forEach(({ resolve }) => resolve(result));
        } catch (err) {
          resolvers.forEach(({ reject }) => reject(err));
        }
      }, ms);
    });
  };
}

const search = debounceAsync(
  (query) => fetch(`/api/search?q=${query}`).then((r) => r.json()),
  300
);
```

---

## 📚 9. Common Pitfalls

### Pitfall 1: Unhandled Promise Rejections

```javascript
// ❌ BAD — rejection goes unhandled
async function risky() {
  const data = await fetch("/api/might-fail"); // If this throws...
  return data.json(); // ...this line never runs, error is unhandled
}
risky(); // No .catch(), no try/catch wrapping the call

// ✅ GOOD — always handle at the call site
risky().catch(console.error);
// Or use a global handler (safety net, not primary strategy)
process.on("unhandledRejection", (err) => {
  console.error("Unhandled rejection:", err);
  process.exit(1);
});
```

### Pitfall 2: `await` in Loops (Accidental Sequential)

```javascript
// ❌ SLOW — sequential, one at a time
for (const url of urls) {
  const data = await fetch(url); // Waits for each before starting next
}

// ✅ FAST — parallel
const results = await Promise.all(urls.map((url) => fetch(url)));
```

### Pitfall 3: Forgetting `await`

```javascript
// ❌ BUG — returns a Promise, not the value
async function getUser() {
  const response = fetch("/api/user"); // Missing await!
  return response.json(); // TypeError: response.json is not a function
}

// ✅ CORRECT
async function getUser() {
  const response = await fetch("/api/user");
  return response.json();
}
```

---

## 🏋️ 10. Exercises

### Exercise 5.3.1 — Predict the Output

```javascript
async function test() {
  console.log("1");
  
  setTimeout(() => console.log("2"), 0);
  
  await Promise.resolve();
  console.log("3");
  
  setTimeout(() => console.log("4"), 0);
  
  await Promise.resolve();
  console.log("5");
}

console.log("6");
test();
console.log("7");
```

Write the exact output order and explain each step.

### Exercise 5.3.2 — Implement `Promise.all` from Scratch

```javascript
function promiseAll(promises) {
  // Your implementation here
  // Must handle: empty array, non-promise values, rejection propagation
}
```

### Exercise 5.3.3 — Build a Task Queue

Implement a task queue that processes async functions with a configurable concurrency limit:

```javascript
class TaskQueue {
  constructor(concurrency = 3) { /* ... */ }
  add(asyncFn) { /* returns Promise that resolves when task completes */ }
}

const queue = new TaskQueue(2);
queue.add(() => fetch("/api/1")); // Starts immediately
queue.add(() => fetch("/api/2")); // Starts immediately (concurrency=2)
queue.add(() => fetch("/api/3")); // Waits until one of the above finishes
```

---

## 🔗 Cross-References

- **Previous:** [12.2 - Core Language - ES2024+, Closures, Prototypes](12.2---Core-Language---ES2024+,-Closures,-Prototypes) — Closures are the mechanism that makes async callbacks work.
- **Next:** [12.4 - OOP & FP Patterns](12.4---OOP-&-FP-Patterns) — Composition patterns for organizing async logic.
- **Browser APIs:** [12.6 - DOM & Browser APIs](12.6---DOM-&-Browser-APIs) — Fetch, WebSockets, and Workers use these async patterns.
- **Backend:** [12.8 - Modern Backend - Node, Bun, Express, Fastify, Hono](12.8---Modern-Backend---Node,-Bun,-Express,-Fastify,-Hono) — Server-side async patterns (streams, middleware).
- **Python comparison:** [08.4 - Concurrency - asyncio, threading, multiprocessing & the GIL](08.4---Concurrency---asyncio,-threading,-multiprocessing-&-the-GIL) — Python's asyncio is the same concept (event loop + coroutines) with different syntax.

---

## 📖 Further Reading

- Philip Roberts, ["What the heck is the event loop anyway?"](https://www.youtube.com/watch?v=8aGhZQkoFbQ) — The definitive visual explanation (JSConf EU 2014)
- [Loupe](http://latentflip.com/loupe/) — Interactive event loop visualizer (by Philip Roberts)
- Jake Archibald, ["In The Loop"](https://www.youtube.com/watch?v=cCOL7MC4Pl0) — Deep dive into microtasks vs rendering (JSConf Asia 2018)
- Kyle Simpson, *You Don't Know JS Yet: Async & Performance* — Chapters on Promises and generators
- [MDN: Using Promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises)
- [MDN: Async/Await](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Promises)



---

## 🏗️ 8. Extended Worked Examples & Deep Dives

### 8.1 — Event Loop Microtask vs Macrotask: Complete Execution Trace

#### The Definitive Ordering Example

```js
console.log("1: Script start");                    // (1) Synchronous

setTimeout(() => console.log("2: setTimeout"), 0); // (2) → Macrotask queue

Promise.resolve()
  .then(() => console.log("3: Promise.then 1"))    // (3) → Microtask queue
  .then(() => console.log("4: Promise.then 2"));   // (4) → Microtask queue (chained)

queueMicrotask(() => console.log("5: queueMicrotask")); // (5) → Microtask queue

async function asyncFn() {
  console.log("6: async fn start");                // (6) Synchronous (before await)
  await Promise.resolve();
  console.log("7: after await");                   // (7) → Microtask queue
}
asyncFn();

console.log("8: Script end");                      // (8) Synchronous

// OUTPUT ORDER:
// 1: Script start          ← synchronous
// 6: async fn start        ← synchronous (async fn runs sync until first await)
// 8: Script end            ← synchronous
// 3: Promise.then 1        ← microtask (queued first)
// 5: queueMicrotask        ← microtask (queued second)
// 7: after await            ← microtask (await resumes as microtask)
// 4: Promise.then 2        ← microtask (chained from #3, queued after #3 runs)
// 2: setTimeout            ← macrotask (runs after ALL microtasks drain)
```

#### Step-by-Step Trace

```
CALL STACK              MICROTASK QUEUE         MACROTASK QUEUE
─────────────────────   ─────────────────────   ─────────────────────
[main()]                []                      []

→ Execute: console.log("1: Script start")
  Output: "1: Script start"

→ Execute: setTimeout(cb, 0)
  Timer API registers callback
  CALL STACK              MICROTASK QUEUE         MACROTASK QUEUE
  [main()]                []                      [setTimeout cb]

→ Execute: Promise.resolve().then(cb1).then(cb2)
  .then(cb1) queues cb1 as microtask
  .then(cb2) returns a pending promise (cb2 queued when cb1 resolves)
  CALL STACK              MICROTASK QUEUE         MACROTASK QUEUE
  [main()]                [Promise cb1]           [setTimeout cb]

→ Execute: queueMicrotask(cb)
  CALL STACK              MICROTASK QUEUE         MACROTASK QUEUE
  [main()]                [Promise cb1, qMT cb]   [setTimeout cb]

→ Execute: asyncFn()
  console.log("6: async fn start") — synchronous
  Output: "6: async fn start"
  await Promise.resolve() — suspends asyncFn, queues continuation
  CALL STACK              MICROTASK QUEUE              MACROTASK QUEUE
  [main()]                [Promise cb1, qMT cb, await] [setTimeout cb]

→ Execute: console.log("8: Script end")
  Output: "8: Script end"

→ main() completes. Call stack empty.
  EVENT LOOP: "Call stack empty → drain ALL microtasks"

→ Dequeue microtask: Promise cb1
  Output: "3: Promise.then 1"
  cb1 resolves → cb2 queued as microtask
  MICROTASK QUEUE: [qMT cb, await resume, Promise cb2]

→ Dequeue microtask: queueMicrotask cb
  Output: "5: queueMicrotask"

→ Dequeue microtask: await resume
  Output: "7: after await"

→ Dequeue microtask: Promise cb2
  Output: "4: Promise.then 2"

→ Microtask queue empty → take ONE macrotask

→ Dequeue macrotask: setTimeout cb
  Output: "2: setTimeout"
```

#### Key Rules

1. **Synchronous code always runs first** (drains the call stack completely)
2. **ALL microtasks drain before ANY macrotask** (even if microtasks queue more microtasks)
3. **Only ONE macrotask per event loop iteration** (then check microtasks again)
4. **`await` is syntactic sugar for `.then()`** — the code after `await` is a microtask
5. **Microtasks can starve macrotasks** — an infinite microtask loop blocks everything

```js
// DANGER: Infinite microtask loop blocks the event loop
function infiniteMicrotasks() {
  queueMicrotask(infiniteMicrotasks); // Never lets macrotasks run!
}
// setTimeout callbacks, I/O, rendering — ALL blocked forever
```

---

### 8.2 — Promise Combinators: allSettled vs any vs race

#### Complete Comparison

```js
const fast = () => new Promise(resolve => setTimeout(() => resolve("fast"), 100));
const slow = () => new Promise(resolve => setTimeout(() => resolve("slow"), 500));
const fail = () => new Promise((_, reject) => setTimeout(() => reject("error"), 200));

// Promise.all — ALL must succeed, fail-fast on first rejection
try {
  const results = await Promise.all([fast(), slow(), fail()]);
} catch (e) {
  console.log(e); // "error" — fails at 200ms, doesn't wait for slow()
}

// Promise.allSettled — NEVER throws, reports all outcomes
const results = await Promise.allSettled([fast(), slow(), fail()]);
// [
//   { status: "fulfilled", value: "fast" },
//   { status: "fulfilled", value: "slow" },
//   { status: "rejected", reason: "error" }
// ]
// Waits for ALL to settle (500ms total)

// Promise.race — first to SETTLE (succeed OR fail) wins
const winner = await Promise.race([fast(), slow()]);
// "fast" — first to resolve (100ms)

// But race can also reject:
try {
  await Promise.race([fail(), slow()]); // fail() settles first (200ms)
} catch (e) {
  console.log(e); // "error"
}

// Promise.any — first to SUCCEED wins (ignores rejections)
const result = await Promise.any([fail(), fast(), slow()]);
// "fast" — fail() is ignored, fast() is first success

// Promise.any only rejects if ALL promises reject:
try {
  await Promise.any([fail(), fail(), fail()]);
} catch (e) {
  console.log(e); // AggregateError: All promises were rejected
  console.log(e.errors); // ["error", "error", "error"]
}
```

#### Decision Matrix

| Combinator | Resolves When | Rejects When | Use Case |
|-----------|--------------|-------------|----------|
| `Promise.all` | ALL succeed | ANY fails (fail-fast) | Parallel fetches where all are needed |
| `Promise.allSettled` | ALL settle (never rejects) | Never | Batch operations, report partial failures |
| `Promise.race` | First settles | First settles with rejection | Timeout patterns, fastest response |
| `Promise.any` | First succeeds | ALL fail | Redundant sources, fallback chains |

#### Real-World Patterns

```js
// Pattern 1: Fetch with timeout using Promise.race
async function fetchWithTimeout(url, timeoutMs = 5000) {
  const controller = new AbortController();

  const fetchPromise = fetch(url, { signal: controller.signal });
  const timeoutPromise = new Promise((_, reject) =>
    setTimeout(() => {
      controller.abort();
      reject(new Error(`Request timed out after ${timeoutMs}ms`));
    }, timeoutMs)
  );

  return Promise.race([fetchPromise, timeoutPromise]);
}

// Pattern 2: Fastest CDN with Promise.any
async function fetchFromFastestCDN(path) {
  const cdns = [
    `https://cdn1.example.com${path}`,
    `https://cdn2.example.com${path}`,
    `https://cdn3.example.com${path}`,
  ];

  return Promise.any(cdns.map(url => fetch(url)));
  // Returns response from whichever CDN responds first
  // Only fails if ALL CDNs are down
}

// Pattern 3: Graceful degradation with Promise.allSettled
async function loadDashboard(userId) {
  const [userResult, postsResult, notificationsResult] = await Promise.allSettled([
    fetchUser(userId),
    fetchPosts(userId),
    fetchNotifications(userId),
  ]);

  return {
    user: userResult.status === "fulfilled" ? userResult.value : null,
    posts: postsResult.status === "fulfilled" ? postsResult.value : [],
    notifications: notificationsResult.status === "fulfilled"
      ? notificationsResult.value
      : [],
    errors: [userResult, postsResult, notificationsResult]
      .filter(r => r.status === "rejected")
      .map(r => r.reason),
  };
}

// Pattern 4: Concurrent with concurrency limit
async function mapWithConcurrency(items, fn, concurrency = 5) {
  const results = [];
  const executing = new Set();

  for (const [index, item] of items.entries()) {
    const promise = fn(item, index).then(result => {
      executing.delete(promise);
      return result;
    });
    executing.add(promise);
    results.push(promise);

    if (executing.size >= concurrency) {
      await Promise.race(executing);
    }
  }

  return Promise.all(results);
}

// Process 100 items, max 5 concurrent
const processed = await mapWithConcurrency(
  urls,
  async (url) => {
    const res = await fetch(url);
    return res.json();
  },
  5
);
```

---

### 8.3 — AbortController + Timeout Patterns

#### Composable Cancellation

```js
// Utility: Create a signal that aborts after a timeout
function timeoutSignal(ms) {
  // AbortSignal.timeout() is the modern way (Node 18+, all browsers)
  return AbortSignal.timeout(ms);
}

// Utility: Combine multiple signals (any abort → combined aborts)
function anySignal(signals) {
  // AbortSignal.any() — Node 20+, modern browsers
  return AbortSignal.any(signals);
}

// Production pattern: request with timeout + user cancellation
async function fetchData(url, options = {}) {
  const { timeout = 10000, signal: userSignal } = options;

  // Combine user's signal with timeout
  const signals = [AbortSignal.timeout(timeout)];
  if (userSignal) signals.push(userSignal);
  const combinedSignal = AbortSignal.any(signals);

  try {
    const response = await fetch(url, { signal: combinedSignal });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    if (error.name === "TimeoutError") {
      throw new Error(`Request to ${url} timed out after ${timeout}ms`);
    }
    if (error.name === "AbortError") {
      throw new Error(`Request to ${url} was cancelled`);
    }
    throw error;
  }
}

// Usage
const controller = new AbortController();

// User clicks "Cancel" button
cancelButton.addEventListener("click", () => controller.abort());

try {
  const data = await fetchData("/api/large-dataset", {
    timeout: 30000,
    signal: controller.signal,
  });
} catch (e) {
  console.log(e.message); // "Request was cancelled" or "timed out"
}
```

#### AbortController for Non-Fetch Operations

```js
// Cancel any async operation
async function longRunningTask(signal) {
  for (let i = 0; i < 1_000_000; i++) {
    // Check signal periodically
    if (signal.aborted) {
      throw new Error("Task cancelled");
    }

    // Do work...
    await processChunk(i);

    // Or use throwIfAborted() (cleaner)
    signal.throwIfAborted();
  }
}

// Cancel event listeners
const controller = new AbortController();

// All these listeners are removed when controller.abort() is called
element.addEventListener("click", handleClick, { signal: controller.signal });
element.addEventListener("mousemove", handleMove, { signal: controller.signal });
window.addEventListener("resize", handleResize, { signal: controller.signal });

// One call removes all listeners:
controller.abort();

// Cancel setInterval
function cancellableInterval(fn, ms, signal) {
  const id = setInterval(() => {
    if (signal.aborted) {
      clearInterval(id);
      return;
    }
    fn();
  }, ms);

  signal.addEventListener("abort", () => clearInterval(id));
  return id;
}
```

---

### 8.4 — Structured Async with AsyncIterator

#### Building an Event Stream

```js
// Convert any event emitter to an async iterator
function on(emitter, event, options = {}) {
  const { signal } = options;
  const queue = [];
  const resolvers = [];
  let done = false;

  const handler = (data) => {
    const resolver = resolvers.shift();
    if (resolver) {
      resolver({ value: data, done: false });
    } else {
      queue.push(data);
    }
  };

  emitter.on(event, handler);

  signal?.addEventListener("abort", () => {
    done = true;
    emitter.off(event, handler);
    // Resolve any pending with done
    for (const resolver of resolvers) {
      resolver({ value: undefined, done: true });
    }
    resolvers.length = 0;
  });

  return {
    [Symbol.asyncIterator]() { return this; },
    next() {
      if (done) return Promise.resolve({ value: undefined, done: true });
      const item = queue.shift();
      if (item !== undefined) {
        return Promise.resolve({ value: item, done: false });
      }
      return new Promise(resolve => resolvers.push(resolve));
    },
    return() {
      done = true;
      emitter.off(event, handler);
      return Promise.resolve({ value: undefined, done: true });
    }
  };
}

// Usage: process WebSocket messages as async iterator
const ws = new WebSocket("wss://api.example.com/stream");
const controller = new AbortController();

for await (const message of on(ws, "message", { signal: controller.signal })) {
  const data = JSON.parse(message.data);
  console.log("Received:", data);

  if (data.type === "end") break; // Triggers return()
}
```

#### Async Generator Composition (Pipeline Pattern)

```js
// Build processing pipelines with async generators
async function* readLines(stream) {
  const reader = stream.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop(); // Keep incomplete line

      for (const line of lines) {
        yield line;
      }
    }
    if (buffer) yield buffer; // Emit final line
  } finally {
    reader.releaseLock();
  }
}

async function* parseJSON(lines) {
  for await (const line of lines) {
    if (line.trim()) {
      try {
        yield JSON.parse(line);
      } catch {
        console.warn("Invalid JSON:", line);
      }
    }
  }
}

async function* filter(source, predicate) {
  for await (const item of source) {
    if (predicate(item)) yield item;
  }
}

async function* map(source, transform) {
  for await (const item of source) {
    yield transform(item);
  }
}

async function* batch(source, size) {
  let buffer = [];
  for await (const item of source) {
    buffer.push(item);
    if (buffer.length >= size) {
      yield buffer;
      buffer = [];
    }
  }
  if (buffer.length > 0) yield buffer;
}

// Compose the pipeline
const response = await fetch("/api/events/stream");

const pipeline = batch(
  map(
    filter(
      parseJSON(readLines(response.body)),
      event => event.type === "user_action"
    ),
    event => ({ ...event, processedAt: Date.now() })
  ),
  100 // Process in batches of 100
);

for await (const eventBatch of pipeline) {
  await saveToDB(eventBatch);
}
```

---

### 8.5 — Implementing Promise from Scratch

```js
// Minimal Promise/A+ compliant implementation
class MyPromise {
  #state = "pending"; // "pending" | "fulfilled" | "rejected"
  #value = undefined;
  #handlers = [];

  constructor(executor) {
    const resolve = (value) => {
      if (this.#state !== "pending") return;

      // If value is a thenable, adopt its state
      if (value && typeof value.then === "function") {
        value.then(resolve, reject);
        return;
      }

      this.#state = "fulfilled";
      this.#value = value;
      this.#processHandlers();
    };

    const reject = (reason) => {
      if (this.#state !== "pending") return;
      this.#state = "rejected";
      this.#value = reason;
      this.#processHandlers();
    };

    try {
      executor(resolve, reject);
    } catch (error) {
      reject(error);
    }
  }

  then(onFulfilled, onRejected) {
    return new MyPromise((resolve, reject) => {
      this.#handlers.push({
        onFulfilled: typeof onFulfilled === "function" ? onFulfilled : (v) => v,
        onRejected: typeof onRejected === "function" ? onRejected : (e) => { throw e; },
        resolve,
        reject,
      });

      if (this.#state !== "pending") {
        this.#processHandlers();
      }
    });
  }

  catch(onRejected) {
    return this.then(null, onRejected);
  }

  finally(onFinally) {
    return this.then(
      (value) => MyPromise.resolve(onFinally()).then(() => value),
      (reason) => MyPromise.resolve(onFinally()).then(() => { throw reason; })
    );
  }

  #processHandlers() {
    if (this.#state === "pending") return;

    // Handlers must be called asynchronously (microtask)
    queueMicrotask(() => {
      while (this.#handlers.length) {
        const { onFulfilled, onRejected, resolve, reject } = this.#handlers.shift();
        const handler = this.#state === "fulfilled" ? onFulfilled : onRejected;

        try {
          const result = handler(this.#value);
          resolve(result);
        } catch (error) {
          reject(error);
        }
      }
    });
  }

  // Static methods
  static resolve(value) {
    if (value instanceof MyPromise) return value;
    return new MyPromise(resolve => resolve(value));
  }

  static reject(reason) {
    return new MyPromise((_, reject) => reject(reason));
  }

  static all(promises) {
    return new MyPromise((resolve, reject) => {
      const results = [];
      let remaining = promises.length;
      if (remaining === 0) return resolve([]);

      promises.forEach((promise, index) => {
        MyPromise.resolve(promise).then(
          (value) => {
            results[index] = value;
            if (--remaining === 0) resolve(results);
          },
          reject
        );
      });
    });
  }

  static race(promises) {
    return new MyPromise((resolve, reject) => {
      for (const promise of promises) {
        MyPromise.resolve(promise).then(resolve, reject);
      }
    });
  }
}

// Verify it works:
const p = new MyPromise((resolve) => {
  setTimeout(() => resolve(42), 100);
});

p.then(v => v * 2)
 .then(v => console.log(v)); // 84
```




---

## 📎 9. Appendix: Extended Derivations & Special Cases

### 9.1 — V8's libuv Integration: How Node.js Implements the Event Loop

Node.js doesn't implement its own event loop — it delegates to **libuv**, a C library that provides cross-platform async I/O.

#### libuv Event Loop Phases

```
┌───────────────────────────────────────────────────────────────────┐
│                     NODE.JS EVENT LOOP (libuv)                     │
│                                                                    │
│  Each iteration ("tick") goes through these phases IN ORDER:      │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  1. TIMERS                                                   │  │
│  │     Execute callbacks from setTimeout() and setInterval()    │  │
│  │     that have expired                                        │  │
│  └──────────────────────────────┬──────────────────────────────┘  │
│                                 │                                  │
│  ┌──────────────────────────────▼──────────────────────────────┐  │
│  │  2. PENDING CALLBACKS                                        │  │
│  │     Execute I/O callbacks deferred from previous iteration   │  │
│  │     (e.g., TCP errors like ECONNREFUSED)                     │  │
│  └──────────────────────────────┬──────────────────────────────┘  │
│                                 │                                  │
│  ┌──────────────────────────────▼──────────────────────────────┐  │
│  │  3. IDLE, PREPARE                                            │  │
│  │     Internal use only (libuv housekeeping)                   │  │
│  └──────────────────────────────┬──────────────────────────────┘  │
│                                 │                                  │
│  ┌──────────────────────────────▼──────────────────────────────┐  │
│  │  4. POLL                                                     │  │
│  │     Retrieve new I/O events                                  │  │
│  │     Execute I/O callbacks (file reads, network, etc.)        │  │
│  │     Will BLOCK here if nothing else is scheduled             │  │
│  └──────────────────────────────┬──────────────────────────────┘  │
│                                 │                                  │
│  ┌──────────────────────────────▼──────────────────────────────┐  │
│  │  5. CHECK                                                    │  │
│  │     Execute setImmediate() callbacks                         │  │
│  └──────────────────────────────┬──────────────────────────────┘  │
│                                 │                                  │
│  ┌──────────────────────────────▼──────────────────────────────┐  │
│  │  6. CLOSE CALLBACKS                                          │  │
│  │     Execute close event callbacks (socket.on('close'))       │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  BETWEEN EACH PHASE: drain microtask queue (Promise.then, etc.)  │
│  BETWEEN EACH PHASE: drain process.nextTick() queue              │
│                                                                    │
└───────────────────────────────────────────────────────────────────┘
```

#### libuv Thread Pool

```
┌─────────────────────────────────────────────────────────────────┐
│  MAIN THREAD (Event Loop)                                        │
│  ─────────────────────────                                       │
│  • JavaScript execution                                          │
│  • Event loop phases                                             │
│  • Network I/O (epoll/kqueue/IOCP — non-blocking, no threads)   │
│                                                                   │
├─────────────────────────────────────────────────────────────────┤
│  THREAD POOL (default: 4 threads, max: 1024)                    │
│  ──────────────────────────────────────────                      │
│  • File system operations (fs.readFile, etc.)                   │
│  • DNS lookups (dns.lookup — NOT dns.resolve)                   │
│  • Crypto operations (crypto.pbkdf2, crypto.randomBytes)        │
│  • Compression (zlib)                                            │
│  • Some C++ addons                                               │
│                                                                   │
│  Set pool size: UV_THREADPOOL_SIZE=16 node app.js               │
│                                                                   │
│  NOTE: Network I/O does NOT use the thread pool!                │
│  TCP/UDP uses OS-level async (epoll on Linux, kqueue on macOS)  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 9.2 — setImmediate vs process.nextTick vs queueMicrotask

These three scheduling mechanisms have different priorities:

```js
// Priority order (highest to lowest):
// 1. process.nextTick()    — runs BEFORE microtasks, after current operation
// 2. queueMicrotask()      — standard microtask (same as Promise.then)
// 3. setImmediate()        — runs in CHECK phase (after I/O poll)
// 4. setTimeout(fn, 0)     — runs in TIMERS phase (next iteration)

process.nextTick(() => console.log("1: nextTick"));
queueMicrotask(() => console.log("2: queueMicrotask"));
setImmediate(() => console.log("3: setImmediate"));
setTimeout(() => console.log("4: setTimeout 0"), 0);
Promise.resolve().then(() => console.log("5: Promise.then"));

// Output:
// 1: nextTick          ← nextTick queue drains first
// 2: queueMicrotask    ← then microtask queue
// 5: Promise.then      ← Promise.then is also a microtask
// 3: setImmediate      ← CHECK phase (or setTimeout first — see below)
// 4: setTimeout 0      ← TIMERS phase

// ⚠️ setImmediate vs setTimeout(0) ordering is NON-DETERMINISTIC
// in the main module! But inside an I/O callback, setImmediate ALWAYS first:
const fs = require("fs");
fs.readFile(__filename, () => {
  setImmediate(() => console.log("setImmediate"));  // Always first
  setTimeout(() => console.log("setTimeout"), 0);   // Always second
});
```

#### When to Use Each

| API | Use Case | Danger |
|-----|----------|--------|
| `process.nextTick()` | Must run before ANY I/O or timers | Can starve I/O if recursive |
| `queueMicrotask()` | Standard async scheduling | Can starve macrotasks if recursive |
| `setImmediate()` | Run after current I/O completes | Node.js only (not in browsers) |
| `setTimeout(fn, 0)` | Cross-platform "next tick" | Minimum 1ms delay in browsers (4ms nested) |

```js
// DANGER: process.nextTick() starvation
function recursiveNextTick() {
  process.nextTick(recursiveNextTick); // I/O NEVER gets processed!
}
// This blocks the event loop more severely than a while(true) loop
// because it prevents the loop from advancing to the POLL phase

// SAFE alternative: use setImmediate for recursive scheduling
function recursiveImmediate() {
  setImmediate(recursiveImmediate); // I/O still gets processed between calls
}
```

---

### 9.3 — Async Error Handling Patterns

#### The Unhandled Rejection Problem

```js
// Node.js will CRASH on unhandled rejections (Node 15+)
// This is intentional — silent failures are worse than crashes

// Catch-all handler (last resort, not a substitute for proper handling)
process.on("unhandledRejection", (reason, promise) => {
  console.error("Unhandled Rejection:", reason);
  // Log to error tracking service
  // In production: graceful shutdown
  process.exit(1);
});

// Common mistake: forgetting to await in loops
async function processItems(items) {
  // ❌ WRONG: forEach doesn't await!
  items.forEach(async (item) => {
    await processItem(item); // Unhandled if it rejects!
  });

  // ✅ CORRECT: use for...of
  for (const item of items) {
    await processItem(item);
  }

  // ✅ CORRECT: use Promise.all for parallel
  await Promise.all(items.map(item => processItem(item)));
}
```

#### Error Boundaries Pattern

```js
// Wrap async operations with consistent error handling
class AsyncBoundary {
  #onError;
  #onSuccess;

  constructor(options = {}) {
    this.#onError = options.onError ?? console.error;
    this.#onSuccess = options.onSuccess ?? (() => {});
  }

  async run(fn) {
    try {
      const result = await fn();
      this.#onSuccess(result);
      return { ok: true, value: result };
    } catch (error) {
      this.#onError(error);
      return { ok: false, error };
    }
  }

  // Wrap a function to never throw
  wrap(fn) {
    return async (...args) => this.run(() => fn(...args));
  }
}

const boundary = new AsyncBoundary({
  onError: (err) => {
    logger.error(err);
    metrics.increment("async_errors");
  },
});

// Never throws — always returns Result
const result = await boundary.run(() => fetchUser("123"));
if (result.ok) {
  renderUser(result.value);
} else {
  renderError(result.error);
}
```

---

### 9.4 — Async Patterns: Debounce, Throttle, and Retry

```js
// Async debounce (waits for pause in calls, returns Promise)
function asyncDebounce(fn, ms) {
  let timeoutId;
  let pendingResolve;

  return function (...args) {
    return new Promise((resolve) => {
      clearTimeout(timeoutId);
      pendingResolve = resolve;

      timeoutId = setTimeout(async () => {
        const result = await fn.apply(this, args);
        pendingResolve(result);
      }, ms);
    });
  };
}

// Usage: debounced search
const debouncedSearch = asyncDebounce(async (query) => {
  const res = await fetch(`/api/search?q=${query}`);
  return res.json();
}, 300);

// Only the last call within 300ms actually executes
const results = await debouncedSearch("hello");

// Exponential backoff retry with jitter
async function retryWithBackoff(fn, options = {}) {
  const {
    maxAttempts = 5,
    baseDelay = 1000,
    maxDelay = 30000,
    jitter = true,
    retryIf = () => true, // Predicate: should we retry this error?
    onRetry = () => {},
    signal,
  } = options;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      signal?.throwIfAborted();
      return await fn(attempt);
    } catch (error) {
      if (attempt === maxAttempts) throw error;
      if (!retryIf(error)) throw error;
      signal?.throwIfAborted();

      // Exponential backoff: 1s, 2s, 4s, 8s, 16s (capped at maxDelay)
      let delay = Math.min(baseDelay * 2 ** (attempt - 1), maxDelay);

      // Add jitter (±25%) to prevent thundering herd
      if (jitter) {
        delay = delay * (0.75 + Math.random() * 0.5);
      }

      onRetry({ attempt, delay, error });
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}

// Usage
const data = await retryWithBackoff(
  async (attempt) => {
    console.log(`Attempt ${attempt}...`);
    const res = await fetch("/api/flaky");
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  },
  {
    maxAttempts: 5,
    retryIf: (err) => !err.message.includes("404"), // Don't retry 404s
    onRetry: ({ attempt, delay }) => console.log(`Retrying in ${delay}ms...`),
  }
);
```

---

### 9.5 — Web Streams API (The Future of Async Data)

```js
// ReadableStream — pull-based async data source
const stream = new ReadableStream({
  start(controller) {
    // Called once when stream is created
    controller.enqueue("Hello");
    controller.enqueue("World");
    controller.close();
  },
});

// TransformStream — process data as it flows through
const uppercase = new TransformStream({
  transform(chunk, controller) {
    controller.enqueue(chunk.toUpperCase());
  },
});

// WritableStream — consume data
const logger = new WritableStream({
  write(chunk) {
    console.log("Received:", chunk);
  },
  close() {
    console.log("Stream complete");
  },
});

// Pipe them together
await stream.pipeThrough(uppercase).pipeTo(logger);
// Output: "Received: HELLO", "Received: WORLD", "Stream complete"

// Real-world: streaming JSON parser
async function* streamJSON(response) {
  const reader = response.body
    .pipeThrough(new TextDecoderStream())
    .getReader();

  let buffer = "";
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += value;
    // Split on newlines (NDJSON format)
    const lines = buffer.split("\n");
    buffer = lines.pop();

    for (const line of lines) {
      if (line.trim()) yield JSON.parse(line);
    }
  }
  if (buffer.trim()) yield JSON.parse(buffer);
}

// Streaming fetch + processing
const response = await fetch("/api/events/stream");
for await (const event of streamJSON(response)) {
  handleEvent(event);
}
```

---

*Last updated: 2026-05-24*
