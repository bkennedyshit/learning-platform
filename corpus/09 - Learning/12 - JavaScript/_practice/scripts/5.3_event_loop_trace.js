/**
 * 5.3_event_loop_trace.js — Practice script for Chapter 5.3
 * Event loop execution order exercises.
 *
 * INSTRUCTIONS: Before running, predict the output order for each exercise.
 * Then run to verify your predictions.
 *
 * Usage:
 *   node 5.3_event_loop_trace.js
 *   bun 5.3_event_loop_trace.js
 */

function separator(title) {
  console.log("\n" + "═".repeat(50));
  console.log(`  ${title}`);
  console.log("═".repeat(50));
}

// ============================================================
// EXERCISE 1: Basic microtask vs macrotask ordering
// ============================================================
async function exercise1() {
  separator("Exercise 1: Basic ordering");
  console.log("  PREDICT: What order will these print?\n");

  console.log("1");
  setTimeout(() => console.log("2"), 0);
  Promise.resolve().then(() => console.log("3"));
  queueMicrotask(() => console.log("4"));
  console.log("5");

  // Wait for all tasks to complete
  await new Promise((r) => setTimeout(r, 50));
  console.log("\n  ANSWER: 1, 5, 3, 4, 2");
  console.log("  WHY: Sync first (1,5), then microtasks (3,4), then macrotask (2)");
}

// ============================================================
// EXERCISE 2: Nested microtasks
// ============================================================
async function exercise2() {
  separator("Exercise 2: Nested microtasks");
  console.log("  PREDICT: What order?\n");

  Promise.resolve().then(() => {
    console.log("A");
    Promise.resolve().then(() => console.log("B"));
  });
  Promise.resolve().then(() => console.log("C"));
  setTimeout(() => console.log("D"), 0);

  await new Promise((r) => setTimeout(r, 50));
  console.log("\n  ANSWER: A, C, B, D");
  console.log("  WHY: Microtasks A and C queued first. A runs, queues B.");
  console.log("        C runs. B runs (still draining microtasks). Then macrotask D.");
}

// ============================================================
// EXERCISE 3: async/await desugaring
// ============================================================
async function exercise3() {
  separator("Exercise 3: async/await");
  console.log("  PREDICT: What order?\n");

  async function foo() {
    console.log("foo-1");
    await Promise.resolve();
    console.log("foo-2");
  }

  console.log("start");
  foo();
  console.log("end");

  await new Promise((r) => setTimeout(r, 50));
  console.log("\n  ANSWER: start, foo-1, end, foo-2");
  console.log("  WHY: 'start' sync. foo() runs sync until await.");
  console.log("        'foo-1' prints. await suspends foo. 'end' prints.");
  console.log("        Microtask resumes foo → 'foo-2'.");
}

// ============================================================
// EXERCISE 4: setTimeout(0) vs Promise vs queueMicrotask
// ============================================================
async function exercise4() {
  separator("Exercise 4: Mixed async primitives");
  console.log("  PREDICT: What order?\n");

  setTimeout(() => console.log("timeout-1"), 0);
  setTimeout(() => console.log("timeout-2"), 0);

  Promise.resolve()
    .then(() => console.log("promise-1"))
    .then(() => console.log("promise-2"));

  queueMicrotask(() => {
    console.log("microtask-1");
    queueMicrotask(() => console.log("microtask-2"));
  });

  console.log("sync");

  await new Promise((r) => setTimeout(r, 50));
  console.log("\n  ANSWER: sync, promise-1, microtask-1, promise-2, microtask-2, timeout-1, timeout-2");
  console.log("  WHY: Sync first. Then drain ALL microtasks (including newly queued ones).");
  console.log("        promise-1 and microtask-1 are in initial queue.");
  console.log("        promise-1 queues promise-2. microtask-1 queues microtask-2.");
  console.log("        All microtasks drain before any macrotask.");
}

// ============================================================
// EXERCISE 5: The tricky one — async function return
// ============================================================
async function exercise5() {
  separator("Exercise 5: async return values");
  console.log("  PREDICT: What order?\n");

  async function getNumber() {
    console.log("inside-getNumber");
    return 42;
  }

  console.log("before");
  const p = getNumber();
  console.log("after");
  p.then((n) => console.log("resolved:", n));
  console.log("end");

  await new Promise((r) => setTimeout(r, 50));
  console.log("\n  ANSWER: before, inside-getNumber, after, end, resolved: 42");
  console.log("  WHY: getNumber() runs synchronously until it returns.");
  console.log("        The return value is wrapped in a resolved Promise.");
  console.log("        .then() callback is a microtask — runs after sync code.");
}

// ============================================================
// EXERCISE 6: Promise.all timing
// ============================================================
async function exercise6() {
  separator("Exercise 6: Promise.all vs sequential");

  const delay = (ms, label) =>
    new Promise((resolve) => {
      setTimeout(() => {
        console.log(`  ${label} resolved (${ms}ms)`);
        resolve(label);
      }, ms);
    });

  console.log("  Sequential (one after another):");
  const seqStart = Date.now();
  await delay(100, "A");
  await delay(100, "B");
  await delay(100, "C");
  console.log(`  Sequential total: ${Date.now() - seqStart}ms\n`);

  console.log("  Parallel (Promise.all):");
  const parStart = Date.now();
  await Promise.all([delay(100, "X"), delay(100, "Y"), delay(100, "Z")]);
  console.log(`  Parallel total: ${Date.now() - parStart}ms`);
  console.log("\n  KEY INSIGHT: Promise.all runs all promises concurrently!");
}

// ============================================================
// Run all exercises in sequence
// ============================================================
async function main() {
  console.log("🔄 Event Loop Trace Exercises");
  console.log("   Predict each output BEFORE looking at the answer!");

  await exercise1();
  await exercise2();
  await exercise3();
  await exercise4();
  await exercise5();
  await exercise6();

  separator("COMPLETE");
  console.log("  If you got all 6 right, you understand the event loop! 🎉\n");
}

main();
