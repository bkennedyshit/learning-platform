import type {
  CompletionChunk,
  CompletionRequest,
  CompletionResult,
  EmbeddingRequest,
  LLMProviderAdapter
} from "./types.js";

export interface StubAdapterConfig {
  completionText?: string;
  embeddingDimensions?: number;
}

export function createStubAdapter(config: StubAdapterConfig = {}): LLMProviderAdapter {
  const completionText = config.completionText ?? "Stubbed grounded answer.";
  const dimensions = config.embeddingDimensions ?? 8;

  return {
    async complete(_request: CompletionRequest): Promise<CompletionResult> {
      return {
        content: completionText,
        model: "stub"
      };
    },

    async *stream(_request: CompletionRequest): AsyncIterable<CompletionChunk> {
      yield {
        contentDelta: completionText,
        done: false
      };
      yield {
        contentDelta: "",
        done: true
      };
    },

    async embed(request: EmbeddingRequest): Promise<number[][]> {
      return request.texts.map((text) => stableEmbedding(text, dimensions));
    }
  };
}

function stableEmbedding(text: string, dimensions: number): number[] {
  const values = Array.from({ length: dimensions }, (_, index) => {
    const charCode = text.charCodeAt(index % Math.max(1, text.length)) || 0;
    return Number(((charCode % 31) / 30).toFixed(6));
  });

  return values;
}
