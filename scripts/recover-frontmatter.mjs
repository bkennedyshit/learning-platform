// Recover corrupted corpus frontmatter.
//
// Background: fix-titles.ts prepended a bogus stub frontmatter block
// (subject:"unknown") on top of the real Obsidian metadata block because its
// LF-only regex never matched the CRLF files. This script drops the stub block,
// lifts the real metadata from the second block, and writes ONE clean LF block
// that is both site- and ingestion-parser safe.
//
// Usage:
//   node scripts/recover-frontmatter.mjs            (dry run, writes nothing)
//   node scripts/recover-frontmatter.mjs --apply    (rewrites files in place)

import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const lessonsDir = path.resolve(__dirname, "../corpus/lessons");
const APPLY = process.argv.includes("--apply");

function scalar(block, key) {
  const m = new RegExp(`^${key}:[ \\t]*(.+)$`, "m").exec(block);
  if (!m) return undefined;
  let v = m[1].trim();
  // strip surrounding quotes
  v = v.replace(/^["']|["']$/g, "").trim();
  return v.length ? v : undefined;
}

function deriveTier(catalog) {
  return catalog === "advanced" ? "higher-education" : "9-12";
}

function yamlQuote(s) {
  return `"${String(s).replace(/"/g, '\\"')}"`;
}

function splitBlocks(raw) {
  const c = raw.replace(/\r\n/g, "\n");
  if (!c.startsWith("---\n")) return { ok: false, reason: "no-frontmatter", body: c };
  const b1end = c.indexOf("\n---\n", 4);
  if (b1end === -1) return { ok: false, reason: "unterminated-block1", body: c };
  const block1 = c.slice(4, b1end);
  const rest = c.slice(b1end + 5);
  if (rest.startsWith("---\n")) {
    const b2end = rest.indexOf("\n---\n", 4);
    if (b2end === -1) return { ok: false, reason: "unterminated-block2", body: c };
    return { ok: true, double: true, block1, block2: rest.slice(4, b2end), body: rest.slice(b2end + 5) };
  }
  return { ok: true, double: false, block1, block2: null, body: rest };
}

function buildClean({ title, subject, catalog, tier, chapter, type }, body) {
  const lines = [
    `title: ${yamlQuote(title)}`,
    `subject: ${yamlQuote(subject)}`,
    `catalog: ${catalog}`,
    `audience_tier: ${tier}`,
    `chapter: ${yamlQuote(chapter)}`,
  ];
  if (type) lines.push(`type: ${type}`);
  lines.push(`objectives:`, `  - "Understand the concepts"`, `  - "Apply the theory"`, `open_source: true`);
  return `---\n${lines.join("\n")}\n---\n\n${body.replace(/^\n+/, "")}`;
}

function titleFromFilename(file) {
  return file
    .replace(/\.md$/, "")
    .replace(/^\d+(-\d+)?-/, "")
    .split("-")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

const stats = {
  total: 0,
  recovered: 0,
  alreadyClean: 0,
  noSubject: [],
  anomalies: [],
};
const subjects = new Map();
const types = new Map();
const samples = [];

const files = (await readdir(lessonsDir)).filter((f) => f.endsWith(".md")).sort();

for (const file of files) {
  stats.total += 1;
  const filePath = path.join(lessonsDir, file);
  const raw = await readFile(filePath, "utf8");
  const parsed = splitBlocks(raw);

  if (!parsed.ok) {
    stats.anomalies.push(`${file}: ${parsed.reason}`);
    continue;
  }

  // Source of truth: the real block. Block2 when double; otherwise block1.
  const real = parsed.double ? parsed.block2 : parsed.block1;

  const subject = scalar(real, "subject");
  const catalog = scalar(real, "catalog") === "advanced" ? "advanced" : "k12";
  const title = scalar(real, "title") || titleFromFilename(file);
  const chapter = scalar(real, "chapter") || "Chapter 1";
  const type = scalar(real, "type");
  const tier = deriveTier(catalog);

  if (!subject || subject.toLowerCase() === "unknown") {
    stats.noSubject.push(file);
    continue;
  }

  if (!parsed.double) {
    // Single clean block already (or fix-titles edited in place). Count and skip rewrite.
    stats.alreadyClean += 1;
  } else {
    stats.recovered += 1;
  }

  subjects.set(subject, (subjects.get(subject) || 0) + 1);
  if (type) types.set(type, (types.get(type) || 0) + 1);

  const cleaned = buildClean({ title, subject, catalog, tier, chapter, type }, parsed.body);

  if (samples.length < 3 && parsed.double) {
    samples.push({ file, before: raw.replace(/\r\n/g, "\n").slice(0, 320), after: cleaned.slice(0, 320) });
  }

  if (APPLY) {
    await writeFile(filePath, cleaned, "utf8");
  }
}

console.log(`\n=== Frontmatter Recovery ${APPLY ? "(APPLIED)" : "(DRY RUN)"} ===`);
console.log(`Total .md files:        ${stats.total}`);
console.log(`Double-block recovered: ${stats.recovered}`);
console.log(`Single-block (skipped): ${stats.alreadyClean}`);
console.log(`No subject recoverable: ${stats.noSubject.length}`);
console.log(`Anomalies:              ${stats.anomalies.length}`);

console.log(`\n--- Recovered subjects (${subjects.size}) ---`);
for (const [s, n] of [...subjects.entries()].sort((a, b) => b[1] - a[1])) {
  console.log(`  ${String(n).padStart(4)}  ${s}`);
}

console.log(`\n--- Content types ---`);
for (const [t, n] of [...types.entries()].sort((a, b) => b[1] - a[1])) {
  console.log(`  ${String(n).padStart(4)}  ${t}`);
}

if (stats.noSubject.length) {
  console.log(`\n--- Files with no recoverable subject (first 20) ---`);
  console.log(stats.noSubject.slice(0, 20).map((f) => `  ${f}`).join("\n"));
}
if (stats.anomalies.length) {
  console.log(`\n--- Anomalies (first 20) ---`);
  console.log(stats.anomalies.slice(0, 20).map((f) => `  ${f}`).join("\n"));
}

console.log(`\n--- Sample before/after (truncated) ---`);
for (const s of samples) {
  console.log(`\n### ${s.file}\nBEFORE:\n${s.before}\n...\nAFTER:\n${s.after}\n...`);
}

if (!APPLY) console.log(`\nDry run only. Re-run with --apply to write changes.`);
