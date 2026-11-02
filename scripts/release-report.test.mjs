import assert from "node:assert/strict";
import test from "node:test";
import {
  STATUS,
  EXPECTED_ROUTES,
  makeStage,
  classifyProviderConfig,
  providerStage,
  routeRegressionStage,
  summarize,
  renderReport
} from "./release-report.mjs";

test("makeStage rejects unknown statuses (a typo can never become a pass)", () => {
  assert.throws(() => makeStage("x", "passed"), /Unknown stage status/);
  assert.throws(() => makeStage("", STATUS.PASS), /Stage name is required/);
});

test("classifyProviderConfig: missing config is never configured", () => {
  assert.equal(classifyProviderConfig("local", {}).configured, false);
  assert.equal(classifyProviderConfig("hosted", {}).configured, false);
  assert.equal(classifyProviderConfig("hosted", { RELEASE_HOSTED_LLM_BASE_URL: "u" }).configured, false);
  assert.equal(classifyProviderConfig("gemini", {}).configured, false);
});

test("classifyProviderConfig: complete config is configured", () => {
  assert.equal(classifyProviderConfig("local", { RELEASE_LOCAL_LLM_BASE_URL: "http://x" }).configured, true);
  assert.equal(
    classifyProviderConfig("hosted", { RELEASE_HOSTED_LLM_BASE_URL: "u", RELEASE_HOSTED_LLM_API_KEY: "k" })
      .configured,
    true
  );
  assert.equal(classifyProviderConfig("gemini", { GEMINI_API_KEY: "k" }).configured, true);
});

test("providerStage: unconfigured provider reports not_configured, never pass", () => {
  const stage = providerStage("gemini live", "gemini", {}, { status: "pass", live: true, completion: true, embedding: true });
  assert.equal(stage.status, STATUS.NOT_CONFIGURED);
});

test("providerStage: configured but non-live outcome cannot be a pass", () => {
  const env = { GEMINI_API_KEY: "k" };
  // Claims pass but did not actually run live / omitted embedding.
  const notLive = providerStage("gemini live", "gemini", env, { status: "pass", live: false, completion: true, embedding: true });
  assert.equal(notLive.status, STATUS.FAIL);
  const noEmbedding = providerStage("gemini live", "gemini", env, { status: "pass", live: true, completion: true, embedding: false });
  assert.equal(noEmbedding.status, STATUS.FAIL);
});

test("providerStage: a genuine live completion+embedding is a pass", () => {
  const stage = providerStage(
    "gemini live",
    "gemini",
    { GEMINI_API_KEY: "k" },
    { status: "pass", live: true, completion: true, embedding: true, evidence: "ok" }
  );
  assert.equal(stage.status, STATUS.PASS);
  assert.equal(stage.live, true);
});

test("providerStage: a configured live failure reports fail", () => {
  const stage = providerStage("gemini live", "gemini", { GEMINI_API_KEY: "k" }, { status: "fail", reason: "HTTP 500" });
  assert.equal(stage.status, STATUS.FAIL);
});

test("routeRegressionStage: exact 81/640/731 passes, drift fails", () => {
  assert.equal(routeRegressionStage("routes", { ...EXPECTED_ROUTES }).status, STATUS.PASS);
  assert.equal(routeRegressionStage("routes", { subjects: 80, lessons: 640, routes: 731 }).status, STATUS.FAIL);
  assert.equal(routeRegressionStage("routes", { subjects: 81, lessons: 640, routes: 730 }).status, STATUS.FAIL);
});

test("summarize: nonzero exit only when at least one stage failed", () => {
  const passing = summarize([
    makeStage("a", STATUS.PASS),
    makeStage("b", STATUS.SKIP),
    makeStage("c", STATUS.NOT_CONFIGURED)
  ]);
  assert.equal(passing.exitCode, 0);
  assert.equal(passing.counts.pass, 1);
  assert.equal(passing.counts.not_configured, 1);

  const failing = summarize([makeStage("a", STATUS.PASS), makeStage("b", STATUS.FAIL)]);
  assert.equal(failing.exitCode, 1);
});

test("not_configured and skip never count toward pass and never fail the run", () => {
  const { counts, exitCode } = summarize([
    makeStage("a", STATUS.NOT_CONFIGURED),
    makeStage("b", STATUS.SKIP)
  ]);
  assert.equal(counts.pass, 0);
  assert.equal(exitCode, 0);
});

test("renderReport produces text and the same exit code as summarize", () => {
  const stages = [makeStage("a", STATUS.PASS, { evidence: "ok" }), makeStage("b", STATUS.NOT_CONFIGURED, { detail: "no key" })];
  const report = renderReport(stages, { title: "Test" });
  assert.match(report.text, /Test/);
  assert.match(report.text, /NOT CONFIGURED/);
  assert.equal(report.exitCode, 0);
});
