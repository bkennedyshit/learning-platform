import { ProviderConfigurationError } from "./errors.js";
import { createGeminiAdapter } from "./gemini.js";
import { createCodexCliAdapter } from "./codexCli.js";
import { createOpenAICompatibleAdapter } from "./openaiCompatible.js";
import { createStubAdapter } from "./stub.js";
import type { LLMProviderAdapter, ProviderConfig } from "./types.js";

export function createLLMProviderAdapter(config: ProviderConfig): LLMProviderAdapter {
  if (config.kind === "stub") {
    return createStubAdapter();
  }

  if (config.kind === "gemini") {
    if (!config.baseUrl || !config.apiKey || !config.completionModel || !config.embeddingModel) {
      throw new ProviderConfigurationError(
        "baseUrl, apiKey, completionModel, and embeddingModel are required for the Gemini provider."
      );
    }

    return createGeminiAdapter({
      baseUrl: config.baseUrl,
      apiKey: config.apiKey,
      completionModel: config.completionModel,
      embeddingModel: config.embeddingModel
    });
  }

  if (config.kind === "codex") {
    return createCodexCliAdapter({
      command: config.command,
      model: config.completionModel,
      workingDirectory: config.workingDirectory,
      timeoutMs: config.timeoutMs
    });
  }

  if (config.kind === "local" || config.kind === "hosted") {
    if (!config.baseUrl || !config.completionModel || !config.embeddingModel) {
      throw new ProviderConfigurationError(
        "baseUrl, completionModel, and embeddingModel are required for OpenAI-compatible providers."
      );
    }

    return createOpenAICompatibleAdapter({
      baseUrl: config.baseUrl,
      apiKey: config.apiKey,
      completionModel: config.completionModel,
      embeddingModel: config.embeddingModel
    });
  }

  throw new ProviderConfigurationError("Unsupported provider kind.");
}
