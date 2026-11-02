/**
 * Consolidated release verification (Task D/E/G).
 *
 * Runs every required stage, prints ONE honest report using the four statuses
 * (pass / fail / supported skip / not_configured), and exits nonzero only when a
 * stage actually failed. It never labels a mocked/unit result as a live pass:
 * provider live checks call real endpoints and are `not_configured` without
 * credentials; DB integration is `not_configured` without an explicit flag; and
 * visual render is a `supported skip` unless browser tooling is already present
 * (this script never installs Playwright to fake a pass).
 *
 *   pnpm release
 *   node scripts/release.mjs
 */

import { spawnSync } from "node:child_process";
import { existsSync, readFileSync, readdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  STATUS,
  EXPECTED_ROUTES,
  makeStage,
  providerStage,
  routeRegressionStage,
  renderReport
} from "./release-report.mjs";
import { runFixtureChecks, catalogCounts } from "./validate-release-fixtures.mjs";
import { runProviderLiveCheck } from "./check-provider.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");
const env = process.env;

const IS_WIN = process.platform === "win32";
const PNPM = IS_WIN ? "pnpm.cmd" : "pnpm";

/** Run a command, capturing output. Returns { code, out }. */
function run(cmd, args, opts = {}) {
  // Only use a shell for PATH-resolved commands (pnpm.cmd/npx). The absolute
  // node executable path can contain spaces (e.g. C:\Program Files\nodejs),
  // which a shell would mis-split — so run it without a shell.
  const useShell = opts.useShell ?? (IS_WIN && cmd !== process.execPath);
  const res = spawnSync(cmd, args, {
    cwd: opts.cwd ?? root,
    encoding: "utf8",
    shell: useShell,
    maxBuffer: 64 * 1024 * 1024,
    env
  });
  const out = `${res.stdout ?? ""}${res.stderr ?? ""}`;
  return { code: res.status ?? (res.error ? 1 : 0), out, error: res.error };
}

function tail(text, n = 12) {
  return text.split(/\r?\n/).filter(Boolean).slice(-n).join("\n");
}

/** Wrap a command run into a pass/fail stage. */
function commandStage(name, cmd, args, { cwd, evidence } = {}) {
  process.stdout.write(`\n▶ ${name}\n`);
  const { code, out, error } = run(cmd, args, { cwd });
  if (error && error.code === "ENOENT") {
    return makeStage(name, STATUS.FAIL, { detail: `command not found: ${cmd}` });
  }
  if (code === 0) {
    return makeStage(name, STATUS.PASS, { evidence: evidence ?? `${cmd} ${args.join(" ")}` });
  }
  return makeStage(name, STATUS.FAIL, { detail: `exit ${code}\n${tail(out)}` });
}

/* ------------------------------ whitespace ------------------------------ */

const WHITESPACE_EXTS = new Set([".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".json", ".css", ".yml", ".yaml"]);
const WHITESPACE_SKIP = [
  "node_modules",
  ".next",
  "dist",
  ".turbo",
  "src/generated/content.json",
  "public/lesson-assets",
  "pnpm-lock.yaml",
  "corpus/"
];

function gitFiles() {
  const tracked = run("git", ["ls-files"]).out.split(/\r?\n/).filter(Boolean);
  const untracked = run("git", ["ls-files", "--others", "--exclude-standard"]).out
    .split(/\r?\n/)
    .filter(Boolean);
  return [...new Set([...tracked, ...untracked])];
}

function whitespaceStage() {
  process.stdout.write("\n▶ whitespace (tracked+untracked)\n");
  const gitCheck = run("git", ["diff", "--check"]);
  if (gitCheck.code !== 0) {
    return makeStage("whitespace (tracked+untracked)", STATUS.FAIL, {
      detail: `git diff --check failed\n${tail(gitCheck.out)}`
    });
  }
  let files;
  try {
    files = gitFiles();
  } catch (err) {
    return makeStage("whitespace (tracked+untracked)", STATUS.FAIL, { detail: String(err) });
  }
  const offenders = [];
  for (const rel of files) {
    if (WHITESPACE_SKIP.some((s) => rel.includes(s))) continue;
    if (!WHITESPACE_EXTS.has(path.extname(rel))) continue;
    const abs = path.join(root, rel);
    if (!existsSync(abs)) continue;
    let text;
    try {
      text = readFileSync(abs, "utf8");
    } catch {
      continue;
    }
    if (text.length > 2 * 1024 * 1024) continue;
    const lines = text.split("\n");
    lines.forEach((line, idx) => {
      const noCr = line.replace(/\r$/, "");
      if (/[ \t]+$/.test(noCr)) offenders.push(`${rel}:${idx + 1}`);
    });
  }
  if (offenders.length === 0) {
    return makeStage("whitespace (tracked+untracked)", STATUS.PASS, {
      evidence: `${files.length} files scanned, no trailing whitespace`
    });
  }
  return makeStage("whitespace (tracked+untracked)", STATUS.FAIL, {
    detail: `${offenders.length} offending lines: ${offenders.slice(0, 8).join(", ")}${offenders.length > 8 ? " …" : ""}`
  });
}

/* --------------------------- agent test suites -------------------------- */

// Named suite → concrete compiled test file(s) providing the evidence. A suite
// is only counted after its real test file runs and passes; nothing is a mock.
const AGENT_SUITES = {
  "agent-contract": ["packages/agent-contract/dist/v1/contract.test.js"],
  runtime: ["services/api/dist/agent/runtime.test.js"],
  tools: ["services/api/dist/agent/tools/tools.test.js", "services/api/dist/agent/tools/catalog.test.js"],
  auth: ["services/api/dist/auth/auth.test.js"],
  "ownership": ["services/api/dist/http/http.test.js", "services/api/dist/agent/pgTenancy.test.js"],
  consent: ["services/api/dist/compliance/compliance.test.js"],
  "memory-restart": ["services/api/dist/agent/memory/memory.test.js"],
  RAG: ["services/api/dist/rag/rag.test.js"],
  "practice-assessment-review": [
    "services/api/dist/practice/practice.test.js",
    "services/api/dist/learning/learning.test.js",
    "services/api/dist/agent/workflows/teaching.test.js"
  ],
  "jobs-cancel": ["services/api/dist/agent/runtime.test.js"],
  sanitizer: ["services/api/dist/agent/artifacts/sanitizer.test.js"],
  approval: [
    "services/api/dist/agent/approval/approval.test.js",
    "services/api/dist/agent/publication/outbox.test.js"
  ]
};

function agentSuitesStage() {
  const name = "agent suites (contract/runtime/tools/auth/ownership/consent/memory/RAG/practice/jobs-cancel/sanitizer/approval)";
  process.stdout.write(`\n▶ ${name}\n`);
  const files = [...new Set(Object.values(AGENT_SUITES).flat())];
  const missing = files.filter((f) => !existsSync(path.join(root, f)));
  if (missing.length > 0) {
    return makeStage(name, STATUS.FAIL, {
      detail: `compiled suites missing (build did not run?): ${missing.slice(0, 4).join(", ")}`
    });
  }
  const { code, out } = run(process.execPath, ["--test", ...files]);
  if (code === 0) {
    const named = Object.keys(AGENT_SUITES).join(", ");
    return makeStage(name, STATUS.PASS, { evidence: `real suites: ${named}` });
  }
  return makeStage(name, STATUS.FAIL, { detail: `exit ${code}\n${tail(out)}` });
}

/* --------------------------- route regression --------------------------- */

function learningAppRouteCounts() {
  const nextDir = path.join(root, "apps/learning-app/.next");
  const contentPath = path.join(root, "apps/learning-app/src/generated/content.json");
  const { subjects, lessons } = catalogCounts(contentPath);
  const prerender = JSON.parse(readFileSync(path.join(nextDir, "prerender-manifest.json"), "utf8"));
  const prerendered = Object.keys(prerender.routes ?? {}).length;
  const appPaths = JSON.parse(readFileSync(path.join(nextDir, "app-path-routes-manifest.json"), "utf8"));
  const apiRoutes = Object.values(appPaths).filter((p) => String(p).startsWith("/api/")).length;
  return { subjects, lessons, routes: prerendered + apiRoutes };
}

function learningAppBuildAndRoutesStages() {
  const build = commandStage(
    "learning-app build",
    PNPM,
    ["--filter", "@learning-platform/learning-app", "build"]
  );
  const stages = [build];
  if (build.status !== STATUS.PASS) {
    stages.push(
      makeStage("learning-app route regression (81/640/731)", STATUS.FAIL, {
        detail: "skipped route count because the build failed"
      })
    );
    return stages;
  }
  try {
    const counts = learningAppRouteCounts();
    stages.push(routeRegressionStage("learning-app route regression (81/640/731)", counts, EXPECTED_ROUTES));
  } catch (err) {
    stages.push(
      makeStage("learning-app route regression (81/640/731)", STATUS.FAIL, { detail: String(err) })
    );
  }
  return stages;
}

/* ------------------------------ integration ----------------------------- */

function dbIntegrationStage() {
  const name = "clean Postgres/bootstrap integration";
  const enabled = env.RUN_DB_INTEGRATION === "1" || env.RUN_DB_INTEGRATION === "true";
  if (!enabled) {
    return makeStage(name, STATUS.NOT_CONFIGURED, {
      detail: "set RUN_DB_INTEGRATION=1 and provide DATABASE_URL + Docker to run"
    });
  }
  if (!env.DATABASE_URL) {
    return makeStage(name, STATUS.NOT_CONFIGURED, { detail: "DATABASE_URL is not set" });
  }
  // Real bootstrap: build + migrate against the configured database.
  const migrate = commandStage(name, PNPM, ["--filter", "@learning-platform/api", "migrate"]);
  return makeStage(name, migrate.status, { detail: migrate.detail, evidence: migrate.evidence });
}

function visualRenderStage() {
  const name = "mobile+desktop visual render";
  const hasPlaywright =
    existsSync(path.join(root, "node_modules/@playwright/test")) ||
    existsSync(path.join(root, "node_modules/playwright"));
  const enabled = env.RELEASE_VISUAL === "1" || env.RELEASE_VISUAL === "true";
  if (!hasPlaywright) {
    return makeStage(name, STATUS.NOT_CONFIGURED, {
      detail: "browser tooling (Playwright) not installed; not installing it to fake a pass"
    });
  }
  if (!enabled) {
    return makeStage(name, STATUS.SKIP, { detail: "Playwright present; set RELEASE_VISUAL=1 to run" });
  }
  const spec = path.join(root, "apps/learning-app/e2e/learning-loop.spec.ts");
  if (!existsSync(spec)) {
    return makeStage(name, STATUS.SKIP, { detail: "no visual spec found" });
  }
  const res = commandStage(name, "npx", ["playwright", "test", "e2e"], {
    cwd: path.join(root, "apps/learning-app")
  });
  return res;
}

/* -------------------------------- main ---------------------------------- */

async function main() {
  const stages = [];

  // 0. Status-logic self-test — the report machinery must be trustworthy.
  stages.push(
    commandStage("release report status-logic tests", process.execPath, [
      "--test",
      "scripts/release-report.test.mjs"
    ])
  );

  // 1. Deterministic source/catalog/SEO/security invariants.
  process.stdout.write("\n▶ release fixture invariants\n");
  const fixtures = runFixtureChecks();
  const failedFixtures = fixtures.filter((f) => !f.ok);
  stages.push(
    failedFixtures.length === 0
      ? makeStage("release fixture invariants", STATUS.PASS, {
          evidence: `${fixtures.length} invariants (catalog 81/640, SEO, security)`
        })
      : makeStage("release fixture invariants", STATUS.FAIL, {
          detail: failedFixtures.map((f) => `${f.name}: ${f.detail}`).join("; ")
        })
  );

  // 2. Whitespace hygiene (tracked + untracked).
  stages.push(whitespaceStage());

  // 3. Lint, typecheck, unit tests (real).
  stages.push(commandStage("lint", PNPM, ["lint"]));
  stages.push(commandStage("typecheck", PNPM, ["check"]));
  stages.push(commandStage("real unit tests", PNPM, ["test"]));

  // 4. Named agent suites with concrete evidence (built by the unit-test step).
  stages.push(agentSuitesStage());

  // 5. Content-site build.
  stages.push(commandStage("content-site build", PNPM, ["--filter", "@learning-platform/content-site", "build"]));

  // 6. Learning-app build + 81/640/731 route regression.
  stages.push(...learningAppBuildAndRoutesStages());

  // 7. SEO tests (concrete content-site suite: sitemap/robots/canonical/structured data).
  stages.push(
    commandStage("SEO tests (sitemap/robots/canonical)", PNPM, [
      "--filter",
      "@learning-platform/content-site",
      "test"
    ])
  );

  // 8. Provider live checks — real calls only when explicitly configured.
  for (const kind of ["local", "hosted", "gemini"]) {
    process.stdout.write(`\n▶ ${kind} provider live check\n`);
    let outcome;
    try {
      outcome = await runProviderLiveCheck(kind, env);
    } catch (err) {
      outcome = { status: "fail", reason: String(err) };
    }
    stages.push(providerStage(`${kind} provider live check`, kind, env, outcome));
  }

  // 9. Clean Postgres/bootstrap integration.
  stages.push(dbIntegrationStage());

  // 10. Mobile + desktop visual render.
  stages.push(visualRenderStage());

  const report = renderReport(stages, { title: "Learning Platform Release Report" });
  console.log(report.text);
  process.exit(report.exitCode);
}

main().catch((err) => {
  console.error("Release runner crashed:", err);
  process.exit(1);
});
