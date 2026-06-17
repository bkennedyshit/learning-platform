/**
 * 5.1_runtime_check.js — Practice script for Chapter 5.1
 * Detects the current JavaScript runtime and available ES2024+ features.
 *
 * Usage:
 *   node 5.1_runtime_check.js
 *   bun 5.1_runtime_check.js
 *   deno run 5.1_runtime_check.js
 */

function detectRuntime() {
  if (typeof Bun !== "undefined") return { name: "Bun", version: Bun.version };
  if (typeof Deno !== "undefined") return { name: "Deno", version: Deno.version.deno };
  if (typeof process !== "undefined" && process.versions?.node)
    return { name: "Node.js", version: process.versions.node };
  if (typeof window !== "undefined") return { name: "Browser", version: navigator.userAgent };
  return { name: "Unknown", version: "?" };
}

function checkFeatures() {
  const features = [
    ["structuredClone", typeof structuredClone === "function"],
    ["Object.groupBy", typeof Object.groupBy === "function"],
    ["Array.fromAsync", typeof Array.fromAsync === "function"],
    ["Promise.withResolvers", typeof Promise.withResolvers === "function"],
    ["Top-level await", true], // If this file runs, TLA works
    ["Optional chaining (?.) ", (() => { const o = {}; return o?.x?.y === undefined; })()],
    ["Nullish coalescing (??)", (() => { const x = null; return (x ?? 42) === 42; })()],
    ["Private class fields (#)", (() => { try { eval("class T { #x = 1; }"); return true; } catch { return false; } })()],
    ["Array.prototype.at()", typeof [].at === "function"],
    ["String.prototype.replaceAll()", typeof "".replaceAll === "function"],
    ["Array.prototype.toSorted()", typeof [].toSorted === "function"],
    ["Array.prototype.toReversed()", typeof [].toReversed === "function"],
  ];
  return features;
}

// --- Main ---
const runtime = detectRuntime();
console.log(`\n🚀 Runtime Detected: ${runtime.name} v${runtime.version}\n`);
console.log("━".repeat(50));
console.log("  ES2024+ Feature Support");
console.log("━".repeat(50));

const features = checkFeatures();
const maxLen = Math.max(...features.map(([name]) => name.length));

for (const [name, supported] of features) {
  const icon = supported ? "✅" : "❌";
  console.log(`  ${icon} ${name.padEnd(maxLen + 2)}${supported ? "Available" : "NOT available"}`);
}

console.log("━".repeat(50));
const supported = features.filter(([, s]) => s).length;
console.log(`\n  Score: ${supported}/${features.length} features available\n`);
