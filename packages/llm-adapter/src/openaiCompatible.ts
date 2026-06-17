import { ProviderUnavailableError } from "./errors.js";
import type {
  CompletionChunk,
  CompletionRequest,
  CompletionResult,
  EmbeddingRequest,
  LLMProviderAdapter
} from "./types.js";

export interface OpenAICompatibleConfig {
  baseUrl: string;
  apiKey?: string;
  completionModel: string;
  embeddingModel: string;
  fetchImpl?: typeof fetch;
}

interface ChatCompletionResponse {
  model?: string;
  choices?: Array<{
    message?: {
      content?: string;
    };
  }>;
}

interface EmbeddingResponse {
  data?: Array<{
    embedding?: number[];
  }>;
}

export function createOpenAICompatibleAdapter(config: OpenAICompatibleConfig): LLMProviderAdapter {
  const fetcher = config.fetchImpl ?? fetch;
  const baseUrl = config.baseUrl.replace(/\/$/, "");

  return {
    async complete(request) {
      const response = await postJson<ChatCompletionResponse>(
        fetcher,
        `${baseUrl}/chat/completions`,
        config.apiKey,
        {
          model: config.completionModel,
          messages: request.messages,
          temperature: request.temperature ?? 0.2,
          max_tokens: request.maxTokens
        }
      );

      const content = response.choices?.[0]?.message?.content;
      if (!content) {
        throw new ProviderUnavailableError("The provider returned an empty completion.");
      }

      return {
        content,
        model: response.model ?? config.completionModel
      };
    },

    async *stream(request): AsyncIterable<CompletionChunk> {
      const completion = await this.complete(request);
      yield {
        contentDelta: completion.content,
        done: false
      };
      yield {
        contentDelta: "",
        done: true
      };
    },

    async embed(request: EmbeddingRequest) {
      const response = await postJson<EmbeddingResponse>(
        fetcher,
        `${baseUrl}/embeddings`,
        config.apiKey,
        {
          model: config.embeddingModel,
          input: request.texts
        }
      );

      const embeddings = response.data?.map((item) => item.embedding);
      if (!embeddings || embeddings.some((embedding) => !embedding)) {
        throw new ProviderUnavailableError("The provider returned invalid embeddings.");
      }

      return embeddings as number[][];
    }
  };
}

async function postJson<T>(
  fetcher: typeof fetch,
  url: string,
  apiKey: string | undefined,
  body: unknown
): Promise<T> {
  let response: Response;

  try {
    response = await fetcher(url, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        ...(apiKey ? { authorization: `Bearer ${apiKey}` } : {})
      },
      body: JSON.stringify(body)
    });
  } catch (error) {
    throw new ProviderUnavailableError(
      error instanceof Error ? error.message : "The provider request failed."
    );
  }

  if (!response.ok) {
    throw new ProviderUnavailableError(`The provider returned HTTP ${response.status}.`);
  }

  return (await response.json()) as T;
}
