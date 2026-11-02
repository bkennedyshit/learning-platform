export interface CompletionMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

export interface CompletionRequest {
  messages: readonly CompletionMessage[];
  temperature?: number;
  maxTokens?: number;
}

export interface CompletionResult {
  content: string;
  model: string;
}

export interface CompletionChunk {
  contentDelta: string;
  done: boolean;
}

export interface EmbeddingRequest {
  texts: readonly string[];
}

export interface LLMProviderAdapter {
  complete(request: CompletionRequest): Promise<CompletionResult>;
  stream(request: CompletionRequest): AsyncIterable<CompletionChunk>;
  embed(request: EmbeddingRequest): Promise<number[][]>;
}

export type ProviderKind = "local" | "hosted" | "gemini" | "codex" | "stub";

export interface ProviderConfig {
  kind: ProviderKind;
  baseUrl?: string;
  apiKey?: string;
  completionModel?: string;
  embeddingModel?: string;
  /** Optional executable used by the ChatGPT-authenticated Codex CLI provider. */
  command?: string;
  /** Optional isolated working directory for Codex CLI calls. */
  workingDirectory?: string;
  /** Maximum duration of one Codex CLI completion. */
  timeoutMs?: number;
}
