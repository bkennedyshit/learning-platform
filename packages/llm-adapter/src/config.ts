import { ProviderConfigurationError } from "./errors.js";
import type { ProviderConfig, ProviderKind } from "./types.js";

export interface ProviderEnv {
  LLM_PROVIDER?: string;
  LLM_BASE_URL?: string;
  LLM_API_KEY?: string;
  LLM_COMPLETION_MODEL?: string;
  LLM_EMBEDDING_MODEL?: string;
}

export function loadProviderConfig(env: ProviderEnv = process.env): ProviderConfig {
  const kind = parseProviderKind(env.LLM_PROVIDER ?? "stub");

  if (kind === "stub") {
    return { kind };
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
  if (value === "local" || value === "hosted" || value === "stub") {
    return value;
  }

  throw new ProviderConfigurationError(`Unsupported LLM_PROVIDER: ${value}`);
}

function requireEnv(value: string | undefined, key: string): string {
  if (!value) {
    throw new ProviderConfigurationError(`${key} is required.`);
  }

  return value;
}
