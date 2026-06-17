import { ProviderConfigurationError } from "./errors.js";
import { createOpenAICompatibleAdapter } from "./openaiCompatible.js";
import { createStubAdapter } from "./stub.js";
import type { LLMProviderAdapter, ProviderConfig } from "./types.js";

export function createLLMProviderAdapter(config: ProviderConfig): LLMProviderAdapter {
  if (config.kind === "stub") {
    return createStubAdapter();
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
