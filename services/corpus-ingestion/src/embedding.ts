import type { LLMProviderAdapter } from "@learning-platform/llm-adapter";
import type { PreparedLessonChunk } from "./chunking.js";

export interface EmbeddedLessonChunk extends PreparedLessonChunk {
  embedding: number[];
}

export async function embedLessonChunks(
  chunks: readonly PreparedLessonChunk[],
  adapter: LLMProviderAdapter
): Promise<EmbeddedLessonChunk[]> {
  const embeddings = await adapter.embed({ texts: chunks.map((chunk) => chunk.text) });

  return chunks.map((chunk, index) => ({
    ...chunk,
    embedding: embeddings[index] ?? []
  }));
}
