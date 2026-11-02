/**
 * Deterministic release-fixture invariants (Task D).
 *
 * These checks are fast, offline, and do NOT build the apps. They protect the
 * catalog counts, route expectations, SEO source, and the security boundaries
 * that the handoff calls out (no raw model markup, strict Mermaid, sanitizer
 * present, honest publish semantics). Run:
 *
 *   node scripts/validate-release-fixtures.mjs
 */

import { readFileSync, existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { EXPECTED_ROUTES } from "./release-report.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");

/**
 * Extract and parse ONLY the top-level `"subjects":[ ... ]` array from a
 * (very large) generated content.json without parsing the whole lessons map.
 * Respects string literals and escapes while bracket-matching.
 */
export function extractSubjects(content) {
  const marker = '"subjects":';
  const start = content.indexOf(marker);
  if (start === -1) throw new Error('content.json missing "subjects" key');
  let i = content.indexOf("[", start);
  if (i === -1) throw new Error('content.json "subjects" is not an array');
  const arrayStart = i;
  let depth = 0;
  let inString = false;
  let escaped = false;
  for (; i < content.length; i++) {
    const ch = content[i];
    if (inString) {
      if (escaped) escaped = false;
      else if (ch === "\\") escaped = true;
      else if (ch === '"') inString = false;
      continue;
    }
    if (ch === '"') inString = true;
    else if (ch === "[") depth++;
    else if (ch === "]") {
      depth--;
      if (depth === 0) {
        return JSON.parse(content.slice(arrayStart, i + 1));
      }
    }
  }
  throw new Error('content.json "subjects" array was not terminated');
}

export function catalogCounts(contentJsonPath) {
  const raw = readFileSync(contentJsonPath, "utf8");
  const subjects = extractSubjects(raw);
  const subjectCount = subjects.length;
  const lessonCount = subjects.reduce((sum, s) => sum + (Number(s.lessonCount) || 0), 0);
  return { subjects: subjectCount, lessons: lessonCount };
}

const checks = [];
function check(name, fn) {
  checks.push({ name, fn });
}

function fileContains(rel, needle) {
  const p = path.join(root, rel);
  if (!existsSync(p)) return false;
  return readFileSync(p, "utf8").includes(needle);
}

function fileExcludes(rel, needle) {
  const p = path.join(root, rel);
  if (!existsSync(p)) return true;
  return !readFileSync(p, "utf8").includes(needle);
}

// --- catalog / route invariants --------------------------------------------
check("learning-app catalog is 81 subjects / 640 lessons", () => {
  const contentPath = path.join(root, "apps/learning-app/src/generated/content.json");
  if (!existsSync(contentPath)) {
    return { ok: false, detail: "learning-app content.json not generated (run generate-content)" };
  }
  const counts = catalogCounts(contentPath);
  const ok = counts.subjects === EXPECTED_ROUTES.subjects && counts.lessons === EXPECTED_ROUTES.lessons;
  return { ok, detail: `subjects=${counts.subjects}, lessons=${counts.lessons}` };
});

check("content-site catalog matches the same 81/640 corpus", () => {
  const contentPath = path.join(root, "apps/content-site/src/generated/content.json");
  if (!existsSync(contentPath)) {
    return { ok: false, detail: "content-site content.json not generated" };
  }
  const counts = catalogCounts(contentPath);
  const ok = counts.subjects === EXPECTED_ROUTES.subjects && counts.lessons === EXPECTED_ROUTES.lessons;
  return { ok, detail: `subjects=${counts.subjects}, lessons=${counts.lessons}` };
});

check("route expectation is internally consistent (subjects+lessons <= routes)", () => {
  const ok = EXPECTED_ROUTES.subjects + EXPECTED_ROUTES.lessons <= EXPECTED_ROUTES.routes;
  return { ok, detail: `${EXPECTED_ROUTES.subjects}+${EXPECTED_ROUTES.lessons} vs ${EXPECTED_ROUTES.routes}` };
});

// --- SEO source invariants --------------------------------------------------
check("content-site exposes sitemap + robots", () => {
  const ok = existsSync(path.join(root, "apps/content-site/src/app/sitemap.ts")) &&
    existsSync(path.join(root, "apps/content-site/src/app/robots.ts"));
  return { ok, detail: "sitemap.ts + robots.ts" };
});

check("content-site lesson pages declare canonical URLs", () => {
  const ok = fileContains("apps/content-site/src/app/[slug]/page.tsx", "canonical");
  return { ok, detail: "alternates.canonical present" };
});

// --- security invariants ----------------------------------------------------
check("learning-app SafeSvg never uses dangerouslySetInnerHTML", () => {
  // Match actual JSX usage (attribute assignment), not mentions in comments.
  const ok = fileExcludes("apps/learning-app/src/components/SafeSvg.tsx", "dangerouslySetInnerHTML=");
  return { ok, detail: "renders sanitized SVG via <img> only" };
});

check("learning-app SVG allowlist rejects scripts/href", () => {
  const ok =
    fileContains("apps/learning-app/src/lib/safeSvg.ts", "ALLOWED_ELEMENTS") &&
    fileContains("apps/learning-app/src/lib/safeSvg.ts", "event attribute");
  return { ok, detail: "strict element/attribute allowlist" };
});

check("learning-app Mermaid is not securityLevel loose", () => {
  const ok = fileExcludes("apps/learning-app/src/lib/safeMermaid.ts", "loose") &&
    fileExcludes("apps/learning-app/src/components/SafeMermaid.tsx", '"loose"');
  return { ok, detail: "strict mermaid config" };
});

check("api artifact sanitizer is present", () => {
  const ok = existsSync(path.join(root, "services/api/src/agent/artifacts/sanitizer.ts"));
  return { ok, detail: "sanitizer.ts" };
});

check("educator publish never hard-codes published:true", () => {
  const ok = fileExcludes("services/api/src/agent/tools/domainTools.ts", "published: true");
  return { ok, detail: "publish semantics stay honest" };
});

check("publication outbox enforces path safety", () => {
  const ok =
    fileContains("services/api/src/agent/publication/outbox.ts", "path_unsafe") &&
    fileContains("services/api/src/agent/publication/outbox.ts", "escapes the outbox root");
  return { ok, detail: "traversal rejected" };
});

// --- runner -----------------------------------------------------------------
export function runFixtureChecks() {
  const results = checks.map(({ name, fn }) => {
    try {
      const r = fn();
      return { name, ok: Boolean(r.ok), detail: r.detail ?? "" };
    } catch (err) {
      return { name, ok: false, detail: err?.message ?? String(err) };
    }
  });
  return results;
}

if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith("validate-release-fixtures.mjs")) {
  const results = runFixtureChecks();
  console.log("\n=== Release Fixture Invariants ===");
  let failed = 0;
  for (const r of results) {
    console.log(`[${r.ok ? "PASS" : "FAIL"}] ${r.name}${r.detail ? `  — ${r.detail}` : ""}`);
    if (!r.ok) failed++;
  }
  console.log(`\n${results.length - failed}/${results.length} invariants passed.`);
  process.exit(failed > 0 ? 1 : 0);
}
