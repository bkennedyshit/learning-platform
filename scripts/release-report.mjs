/**
 * Release report status logic — deterministic and dependency-free so it can be
 * unit-tested in isolation (see release-report.test.mjs).
 *
 * The four honest statuses:
 *   pass            — the stage ran and succeeded (with concrete evidence).
 *   fail            — the stage ran and failed. ONLY this yields a nonzero exit.
 *   skip            — a supported capability was intentionally not exercised.
 *   not_configured  — required credentials/endpoints/flags/tooling are absent.
 *
 * Guarantees enforced here:
 *   - Missing configuration can NEVER become `pass`.
 *   - A mocked/unit result can never be relabeled a live pass; a live stage must
 *     carry explicit `live: true` evidence to be counted as a live pass.
 *   - Exit code is nonzero if and only if at least one stage failed.
 */

export const STATUS = Object.freeze({
  PASS: "pass",
  FAIL: "fail",
  SKIP: "skip",
  NOT_CONFIGURED: "not_configured"
});

export const EXPECTED_ROUTES = Object.freeze({ subjects: 81, lessons: 640, routes: 731 });

const VALID = new Set(Object.values(STATUS));

/**
 * Build a normalized stage result. Throws on an unknown status so a typo can
 * never silently downgrade to a pass.
 */
export function makeStage(name, status, { detail = "", evidence = "", live = false } = {}) {
  if (!name || typeof name !== "string") {
    throw new Error("Stage name is required.");
  }
  if (!VALID.has(status)) {
    throw new Error(`Unknown stage status: ${String(status)}`);
  }
  return { name, status, detail, evidence, live: Boolean(live) };
}

/**
 * Classify whether a provider live-check is configured. Returns
 * `{ configured, reason }`. When not configured the only allowed report status
 * is `not_configured` — never `pass`.
 *
 * Expected env (server-side only, never bundled to the browser):
 *   local  : RELEASE_LOCAL_LLM_BASE_URL
 *   hosted : RELEASE_HOSTED_LLM_BASE_URL + RELEASE_HOSTED_LLM_API_KEY
 *   gemini : GEMINI_API_KEY (or RELEASE_GEMINI_API_KEY)
 */
export function classifyProviderConfig(kind, env = {}) {
  switch (kind) {
    case "local": {
      const baseUrl = (env.RELEASE_LOCAL_LLM_BASE_URL || "").trim();
      return baseUrl
        ? { configured: true, reason: `local endpoint ${baseUrl}` }
        : { configured: false, reason: "RELEASE_LOCAL_LLM_BASE_URL is not set" };
    }
    case "hosted": {
      const baseUrl = (env.RELEASE_HOSTED_LLM_BASE_URL || "").trim();
      const apiKey = (env.RELEASE_HOSTED_LLM_API_KEY || "").trim();
      if (!baseUrl) return { configured: false, reason: "RELEASE_HOSTED_LLM_BASE_URL is not set" };
      if (!apiKey) return { configured: false, reason: "RELEASE_HOSTED_LLM_API_KEY is not set" };
      return { configured: true, reason: `hosted endpoint ${baseUrl}` };
    }
    case "gemini": {
      const apiKey = (env.GEMINI_API_KEY || env.RELEASE_GEMINI_API_KEY || "").trim();
      return apiKey
        ? { configured: true, reason: "GEMINI_API_KEY is set" }
        : { configured: false, reason: "GEMINI_API_KEY is not set" };
    }
    default:
      return { configured: false, reason: `unknown provider kind ${String(kind)}` };
  }
}

/**
 * Turn a provider live-check outcome into a stage. Enforces that:
 *   - unconfigured → not_configured (never pass)
 *   - a pass requires an outcome that actually exercised the live provider
 *     (both completion AND embedding), signaled by `outcome.live === true`.
 */
export function providerStage(name, kind, env, outcome) {
  const { configured, reason } = classifyProviderConfig(kind, env);
  if (!configured) {
    return makeStage(name, STATUS.NOT_CONFIGURED, { detail: reason });
  }
  if (!outcome) {
    return makeStage(name, STATUS.NOT_CONFIGURED, { detail: "no live check was executed" });
  }
  if (outcome.status === "pass") {
    if (outcome.live !== true || !outcome.completion || !outcome.embedding) {
      // A configured-but-not-actually-live result must not masquerade as a pass.
      return makeStage(name, STATUS.FAIL, {
        detail: "live check did not exercise both completion and embedding"
      });
    }
    return makeStage(name, STATUS.PASS, {
      live: true,
      evidence: outcome.evidence || "completion+embedding succeeded"
    });
  }
  return makeStage(name, STATUS.FAIL, { detail: outcome.reason || "live check failed" });
}

/** Route-count regression against the known-good 81/640/731 baseline. */
export function routeRegressionStage(name, actual, expected = EXPECTED_ROUTES) {
  const mismatches = [];
  for (const key of ["subjects", "lessons", "routes"]) {
    if (actual?.[key] !== expected[key]) {
      mismatches.push(`${key}: expected ${expected[key]}, got ${actual?.[key] ?? "n/a"}`);
    }
  }
  if (mismatches.length > 0) {
    return makeStage(name, STATUS.FAIL, { detail: mismatches.join("; ") });
  }
  return makeStage(name, STATUS.PASS, {
    evidence: `subjects=${actual.subjects}, lessons=${actual.lessons}, routes=${actual.routes}`
  });
}

/** Aggregate stages into counts and a final exit code. */
export function summarize(stages) {
  const counts = { pass: 0, fail: 0, skip: 0, not_configured: 0 };
  for (const stage of stages) {
    if (!VALID.has(stage.status)) {
      throw new Error(`Unknown status in summary: ${String(stage.status)}`);
    }
    counts[stage.status] += 1;
  }
  return { counts, exitCode: counts.fail > 0 ? 1 : 0 };
}

const STATUS_LABEL = {
  pass: "PASS          ",
  fail: "FAIL          ",
  skip: "SKIP (support)",
  not_configured: "NOT CONFIGURED"
};

/** Render the consolidated, human-readable report. */
export function renderReport(stages, { title = "Release Report" } = {}) {
  const { counts, exitCode } = summarize(stages);
  const lines = [];
  lines.push(`\n=== ${title} ===`);
  for (const stage of stages) {
    const label = STATUS_LABEL[stage.status] ?? stage.status;
    const suffix = stage.detail || stage.evidence ? `  — ${stage.detail || stage.evidence}` : "";
    lines.push(`[${label}] ${stage.name}${suffix}`);
  }
  lines.push("");
  lines.push(
    `pass=${counts.pass}  fail=${counts.fail}  skip=${counts.skip}  not_configured=${counts.not_configured}`
  );
  lines.push(`exit=${exitCode}`);
  return { text: lines.join("\n"), counts, exitCode };
}
