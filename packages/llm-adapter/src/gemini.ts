import { ProviderUnavailableError } from "./errors.js";
import type {
  CompletionChunk,
  CompletionMessage,
  CompletionRequest,
  CompletionResult,
  EmbeddingRequest,
  LLMProviderAdapter
} from "./types.js";

/**
 * Native Google Gemini adapter for the Generative Language REST API. It speaks
 * Gemini's own request/response shape (`generateContent` / `embedContent`)
 * rather than an OpenAI-compatible shim, so no proxy is required.
 *
 * Security: the API key is sent server-side only, as a `x-goog-api-key` header
 * (never a query string, never reaching browser code or model tool payloads).
 * Every response is strictly validated; malformed payloads raise
 * {@link ProviderUnavailableError} instead of silently returning empty output.
 */
export interface GeminiConfig {
  baseUrl: string;
  apiKey: string;
  completionModel: string;
  embeddingModel: string;
  fetchImpl?: typeof fetch;
}

interface GeminiContentPart {
  text?: string;
}

interface GeminiCandidate {
  content?: {
    parts?: GeminiContentPart[];
    role?: string;
  };
}

interface GeminiGenerateResponse {
  candidates?: GeminiCandidate[];
  promptFeedback?: { blockReason?: string };
}

interface GeminiEmbedValues {
  values?: number[];
}

interface GeminiSingleEmbedResponse {
  embedding?: GeminiEmbedValues;
}

interface GeminiBatchEmbedResponse {
  embeddings?: GeminiEmbedValues[];
}

/** Map the neutral message roles to Gemini's `user` / `model` roles. */
function toGeminiRole(role: CompletionMessage["role"]): "user" | "model" {
  return role === "assistant" ? "model" : "user";
}

/**
 * Split messages into an optional system instruction and the conversation
 * contents. Gemini takes system prompts via a dedicated `systemInstruction`.
 */
function buildGenerateBody(request: CompletionRequest): Record<string, unknown> {
  const systemParts: GeminiContentPart[] = [];
  const contents: Array<{ role: "user" | "model"; parts: GeminiContentPart[] }> = [];

  for (const message of request.messages) {
    if (message.role === "system") {
      systemParts.push({ text: message.content });
      continue;
    }
    contents.push({ role: toGeminiRole(message.role), parts: [{ text: message.content }] });
  }

  const body: Record<string, unknown> = {
    contents,
    generationConfig: {
      temperature: request.temperature ?? 0.2,
      ...(request.maxTokens ? { maxOutputTokens: request.maxTokens } : {})
    }
  };
  if (systemParts.length > 0) {
    body.systemInstruction = { parts: systemParts };
  }
  return body;
}

export function createGeminiAdapter(config: GeminiConfig): LLMProviderAdapter {
  const fetcher = config.fetchImpl ?? fetch;
  const baseUrl = config.baseUrl.replace(/\/$/, "");

  async function post<T>(url: string, body: unknown): Promise<T> {
    let response: Response;
    try {
      response = await fetcher(url, {
        method: "POST",
        headers: {
          "content-type": "application/json",
          // Server-side only. Header auth keeps the key out of URLs/logs.
          "x-goog-api-key": config.apiKey
        },
        body: JSON.stringify(body)
      });
    } catch (error) {
      throw new ProviderUnavailableError(
        error instanceof Error ? error.message : "The Gemini request failed."
      );
    }

    if (!response.ok) {
      throw new ProviderUnavailableError(`Gemini returned HTTP ${response.status}.`);
    }

    try {
      return (await response.json()) as T;
    } catch {
      throw new ProviderUnavailableError("Gemini returned a non-JSON response.");
    }
  }

  return {
    async complete(request): Promise<CompletionResult> {
      const url = `${baseUrl}/models/${encodeURIComponent(config.completionModel)}:generateContent`;
      const response = await post<GeminiGenerateResponse>(url, buildGenerateBody(request));

      if (response.promptFeedback?.blockReason) {
        throw new ProviderUnavailableError(
          `Gemini blocked the prompt (${response.promptFeedback.blockReason}).`
        );
      }

      const parts = response.candidates?.[0]?.content?.parts;
      const content = Array.isArray(parts)
        ? parts.map((part) => part.text ?? "").join("")
        : "";
      if (!content) {
        throw new ProviderUnavailableError("Gemini returned an empty completion.");
      }

      return { content, model: config.completionModel };
    },

    async *stream(request): AsyncIterable<CompletionChunk> {
      // Deterministic single-shot streaming wrapper: fetch the full completion
      // and emit it as one chunk followed by a terminal marker. Matches the
      // OpenAI-compatible adapter's behavior for parity in the runtime.
      const completion = await this.complete(request);
      yield { contentDelta: completion.content, done: false };
      yield { contentDelta: "", done: true };
    },

    async embed(request: EmbeddingRequest): Promise<number[][]> {
      const model = `models/${config.embeddingModel}`;

      // Prefer the batch endpoint; it returns embeddings in input order.
      const url = `${baseUrl}/models/${encodeURIComponent(config.embeddingModel)}:batchEmbedContents`;
      const body = {
        requests: request.texts.map((text) => ({
          model,
          content: { parts: [{ text }] }
        }))
      };
      const response = await post<GeminiBatchEmbedResponse>(url, body);

      const embeddings = response.embeddings?.map((item) => item.values);
      if (
        !embeddings ||
        embeddings.length !== request.texts.length ||
        embeddings.some((values) => !Array.isArray(values) || values.length === 0)
      ) {
        throw new ProviderUnavailableError("Gemini returned invalid embeddings.");
      }

      return embeddings as number[][];
    }
  };
}

// Re-export the single-embed response type in case callers implement a
// non-batch path in the future; kept internal to avoid an unused symbol.
export type { GeminiSingleEmbedResponse };
