/**
 * Live provider checker (Task E).
 *
 * Runs ONLY when a provider is explicitly configured, and when it runs it makes
 * a REAL call to both completion and embedding through the provider-neutral
 * adapter. It never fabricates a pass: a missing key/endpoint yields
 * `not_configured`, and a real network/validation failure yields `fail`.
 *
 * Usage (CLI):  node scripts/check-provider.mjs <local|hosted|gemini>
 * Or import { runProviderLiveCheck } for use inside the release report.
 */

import { classifyProviderConfig } from "./release-report.mjs";

/**
 * Build a concrete llm-adapter ProviderConfig from release env for a given kind.
 * Returns undefined when not configured.
 */
export function buildProviderConfig(kind, env = process.env) {
  const { configured } = classifyProviderConfig(kind, env);
  if (!configured) return undefined;

  if (kind === "local") {
    return {
      kind: "local",
      baseUrl: env.RELEASE_LOCAL_LLM_BASE_URL.trim(),
      apiKey: env.RELEASE_LOCAL_LLM_API_KEY?.trim() || undefined,
      completionModel: env.RELEASE_LOCAL_LLM_COMPLETION_MODEL?.trim() || "llama3.1",
      embeddingModel: env.RELEASE_LOCAL_LLM_EMBEDDING_MODEL?.trim() || "nomic-embed-text"
    };
  }
  if (kind === "hosted") {
    return {
      kind: "hosted",
      baseUrl: env.RELEASE_HOSTED_LLM_BASE_URL.trim(),
      apiKey: env.RELEASE_HOSTED_LLM_API_KEY.trim(),
      completionModel: env.RELEASE_HOSTED_LLM_COMPLETION_MODEL?.trim() || "gpt-4o-mini",
      embeddingModel: env.RELEASE_HOSTED_LLM_EMBEDDING_MODEL?.trim() || "text-embedding-3-small"
    };
  }
  if (kind === "gemini") {
    return {
      kind: "gemini",
      baseUrl:
        env.RELEASE_GEMINI_BASE_URL?.trim() || "https://generativelanguage.googleapis.com/v1beta",
      apiKey: (env.GEMINI_API_KEY || env.RELEASE_GEMINI_API_KEY).trim(),
      completionModel: env.RELEASE_GEMINI_COMPLETION_MODEL?.trim() || "gemini-2.0-flash",
      embeddingModel: env.RELEASE_GEMINI_EMBEDDING_MODEL?.trim() || "text-embedding-004"
    };
  }
  return undefined;
}

/**
 * Run the live check. Resolves to a structured outcome consumed by
 * `providerStage`. Only reports `pass` when BOTH a real completion and a real
 * embedding succeed (`live: true`).
 */
export async function runProviderLiveCheck(kind, env = process.env) {
  const { configured, reason } = classifyProviderConfig(kind, env);
  if (!configured) {
    return { status: "not_configured", reason };
  }

  let createLLMProviderAdapter;
  try {
    ({ createLLMProviderAdapter } = await import("@learning-platform/llm-adapter"));
  } catch (err) {
    return { status: "fail", reason: `llm-adapter not built: ${err?.message ?? err}` };
  }

  const config = buildProviderConfig(kind, env);
  if (!config) {
    return { status: "not_configured", reason: "provider configuration incomplete" };
  }

  let adapter;
  try {
    adapter = createLLMProviderAdapter(config);
  } catch (err) {
    return { status: "fail", reason: `adapter construction failed: ${err?.message ?? err}` };
  }

  let completion = false;
  let embedding = false;
  try {
    const result = await adapter.complete({
      messages: [{ role: "user", content: "Reply with the single word: ok" }],
      temperature: 0,
      maxTokens: 16
    });
    completion = typeof result?.content === "string" && result.content.length > 0;
  } catch (err) {
    return { status: "fail", reason: `completion failed: ${err?.message ?? err}`, completion: false };
  }
  try {
    const vectors = await adapter.embed({ texts: ["release live check"] });
    embedding = Array.isArray(vectors) && Array.isArray(vectors[0]) && vectors[0].length > 0;
  } catch (err) {
    return { status: "fail", reason: `embedding failed: ${err?.message ?? err}`, completion, embedding: false };
  }

  if (completion && embedding) {
    return {
      status: "pass",
      live: true,
      completion,
      embedding,
      evidence: `${kind} completion (${config.completionModel}) + embedding (${config.embeddingModel})`
    };
  }
  return { status: "fail", reason: "completion or embedding returned empty output", completion, embedding };
}

// CLI entrypoint.
if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith("check-provider.mjs")) {
  const kind = process.argv[2];
  if (!["local", "hosted", "gemini"].includes(kind)) {
    console.error("Usage: node scripts/check-provider.mjs <local|hosted|gemini>");
    process.exit(2);
  }
  runProviderLiveCheck(kind).then((outcome) => {
    console.log(JSON.stringify(outcome, null, 2));
    // not_configured is an explicit, non-failing state.
    process.exit(outcome.status === "fail" ? 1 : 0);
  });
}
