import { ProviderConfigurationError } from "./errors.js";
import type { ProviderConfig, ProviderKind } from "./types.js";

export interface ProviderEnv {
  LLM_PROVIDER?: string;
  LLM_BASE_URL?: string;
  LLM_API_KEY?: string;
  LLM_COMPLETION_MODEL?: string;
  LLM_EMBEDDING_MODEL?: string;
  CODEX_CLI_PATH?: string;
  CODEX_WORKING_DIRECTORY?: string;
  CODEX_TIMEOUT_MS?: string;
  /** Gemini-specific API key. Falls back to LLM_API_KEY when unset. */
  GEMINI_API_KEY?: string;
}

/** Default Gemini REST endpoint (Generative Language API, v1beta). */
export const GEMINI_DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com/v1beta";
export const GEMINI_DEFAULT_COMPLETION_MODEL = "gemini-2.0-flash";
export const GEMINI_DEFAULT_EMBEDDING_MODEL = "text-embedding-004";

export function loadProviderConfig(env: ProviderEnv = process.env): ProviderConfig {
  const kind = parseProviderKind(env.LLM_PROVIDER ?? "stub");

  if (kind === "stub") {
    return { kind };
  }

  if (kind === "gemini") {
    // Gemini has a native REST surface. The base URL is optional (defaults to
    // Google's public endpoint) so that the only required secret is the API key,
    // which is read server-side and never exposed to the browser or model tools.
    return {
      kind,
      baseUrl: env.LLM_BASE_URL || GEMINI_DEFAULT_BASE_URL,
      apiKey: requireEnv(env.GEMINI_API_KEY ?? env.LLM_API_KEY, "GEMINI_API_KEY"),
      completionModel: env.LLM_COMPLETION_MODEL ?? GEMINI_DEFAULT_COMPLETION_MODEL,
      embeddingModel: env.LLM_EMBEDDING_MODEL ?? GEMINI_DEFAULT_EMBEDDING_MODEL
    };
  }

  if (kind === "codex") {
    return {
      kind,
      completionModel: env.LLM_COMPLETION_MODEL ?? "gpt-5.5",
      command: env.CODEX_CLI_PATH || "codex",
      workingDirectory: env.CODEX_WORKING_DIRECTORY,
      timeoutMs: parsePositiveInteger(env.CODEX_TIMEOUT_MS, 120_000)
    };
  }

  return {
    kind,
    baseUrl: requireEnv(env.LLM_BASE_URL, "LLM_BASE_URL"),
    apiKey: env.LLM_API_KEY,
    completionModel: env.LLM_COMPLETION_MODEL ?? "gpt-4.1-mini",
    embeddingModel: env.LLM_EMBEDDING_MODEL ?? "text-embedding-3-small"
  };
}

function parseProviderKind(value: string): ProviderKind {
  if (
    value === "local" ||
    value === "hosted" ||
    value === "gemini" ||
    value === "codex" ||
    value === "stub"
  ) {
    return value;
  }

  throw new ProviderConfigurationError(`Unsupported LLM_PROVIDER: ${value}`);
}

function parsePositiveInteger(value: string | undefined, fallback: number): number {
  if (!value) return fallback;
  const parsed = Number(value);
  if (!Number.isSafeInteger(parsed) || parsed <= 0) {
    throw new ProviderConfigurationError("CODEX_TIMEOUT_MS must be a positive integer.");
  }
  return parsed;
}

function requireEnv(value: string | undefined, key: string): string {
  if (!value) {
    throw new ProviderConfigurationError(`${key} is required.`);
  }

  return value;
}
