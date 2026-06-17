// Automated smoke test for the running apps. No manual clicking.
// Requires both dev servers up: content-site :4100, learning-app :4200.
//
// Run:  node scripts/smoke-test.mjs

import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");
const { subjects, lessons } = JSON.parse(
  readFileSync(path.join(root, "apps/content-site/src/generated/content.json"), "utf8")
);

const CONTENT = "http://localhost:4100";
const APP = "http://localhost:4200";

// Sample: first lesson of the first 10 subjects + a few math/diagram lessons.
const sampleSlugs = [
  ...subjects.slice(0, 10).map((s) => s.lessons[0]?.slug).filter(Boolean),
  "12-single-variable-differentiation",
  "two-body-problem-keplers-laws",
  "214-networking-dns-cdn",
].filter((v, i, a) => v && a.indexOf(v) === i);

let pass = 0;
let fail = 0;
const failures = [];

async function check(label, url, mustContain = []) {
  const norm = (s) => s.toLowerCase().replace(/[^a-z0-9]/g, "");
  try {
    const r = await fetch(url);
    const body = await r.text();
    const nbody = norm(body);
    const okStatus = r.status === 200;
    const missing = mustContain.filter((m) => !body.includes(m) && !nbody.includes(norm(m)));
    if (okStatus && missing.length === 0) {
      pass++;
    } else {
      fail++;
      failures.push(`${label} [${url}] status=${r.status} missing=${JSON.stringify(missing)}`);
    }
  } catch (e) {
    fail++;
    failures.push(`${label} [${url}] ERROR ${e.message}`);
  }
}

console.log("Running smoke test...\n");

// --- content-site ---
await check("content home", `${CONTENT}/`, ["subjects", "lessons"]);
await check("content subject", `${CONTENT}/subject/${subjects[0].slug}`, [subjects[0].name]);
for (const slug of sampleSlugs) {
  const l = lessons[slug];
  if (!l) continue;
  await check(`content lesson ${slug}`, `${CONTENT}/${slug}`, ["lesson-content", l.title]);
}

// --- learning-app ---
await check("app landing", `${APP}/`, ["Start Learning"]);
await check("app catalog", `${APP}/learn`, [subjects[0].name]);
for (const slug of sampleSlugs) {
  const l = lessons[slug];
  if (!l) continue;
  await check(`app lesson ${slug}`, `${APP}/learn/${l.subjectSlug}/${slug}`, [
    "Continue to Next Step",
    l.title,
  ]);
}

// --- tutor endpoint (works with or without a Gemini key) ---
let tutorNote = "";
try {
  const r = await fetch(`${APP}/api/tutor`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      question: "What is the main idea of this lesson?",
      lessonTitle: "Limits & Continuity",
      lessonText: "A limit is the value a function approaches as the input approaches a point.",
    }),
  });
  const data = await r.json();
  if (data.grounded) {
    pass++;
    tutorNote = `tutor: LIVE (grounded answer, ${String(data.answer).length} chars)`;
  } else {
    tutorNote = `tutor: reachable but not configured — set GEMINI_API_KEY ("${String(data.answer).slice(0, 60)}...")`;
    pass++;
  }
} catch (e) {
  fail++;
  tutorNote = `tutor: ERROR ${e.message}`;
}

console.log(`\n=== Smoke Test Results ===`);
console.log(`PASS: ${pass}`);
console.log(`FAIL: ${fail}`);
console.log(tutorNote);
if (failures.length) {
  console.log(`\n--- Failures ---`);
  failures.forEach((f) => console.log("  " + f));
}
process.exit(fail > 0 ? 1 : 0);
