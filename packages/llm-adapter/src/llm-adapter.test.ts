import assert from "node:assert/strict";
import test from "node:test";
import { loadProviderConfig } from "./config.js";
import { ProviderUnavailableError } from "./errors.js";
import { createLLMProviderAdapter } from "./factory.js";
import { createOpenAICompatibleAdapter } from "./openaiCompatible.js";
import { createStubAdapter } from "./stub.js";

test("loads stub provider by default", () => {
  assert.deepEqual(loadProviderConfig({}), { kind: "stub" });
});

test("loads hosted provider from environment", () => {
  assert.deepEqual(
    loadProviderConfig({
      LLM_PROVIDER: "hosted",
      LLM_BASE_URL: "https://example.test/v1",
      LLM_API_KEY: "secret",
      LLM_COMPLETION_MODEL: "chat-model",
      LLM_EMBEDDING_MODEL: "embed-model"
    }),
    {
      kind: "hosted",
      baseUrl: "https://example.test/v1",
      apiKey: "secret",
      completionModel: "chat-model",
      embeddingModel: "embed-model"
    }
  );
});

test("stub adapter returns deterministic completions and embeddings", async () => {
  const adapter = createStubAdapter({ completionText: "ok", embeddingDimensions: 4 });

  assert.deepEqual(await adapter.complete({ messages: [{ role: "user", content: "hi" }] }), {
    content: "ok",
    model: "stub"
  });
  assert.deepEqual(await adapter.embed({ texts: ["abc"] }), [[0.133333, 0.166667, 0.2, 0.133333]]);
});

test("factory creates configured adapters", async () => {
  const adapter = createLLMProviderAdapter({ kind: "stub" });
  assert.equal((await adapter.complete({ messages: [] })).model, "stub");
});

test("OpenAI-compatible adapter maps completion and embeddings", async () => {
  const requests: unknown[] = [];
  const fetchImpl: typeof fetch = async (_input, init) => {
    requests.push(JSON.parse(String(init?.body)));

    if (String(_input).endsWith("/chat/completions")) {
      return Response.json({
        model: "chat-model",
        choices: [{ message: { content: "answer" } }]
      });
    }

    return Response.json({
      data: [{ embedding: [0.1, 0.2] }, { embedding: [0.3, 0.4] }]
    });
  };

  const adapter = createOpenAICompatibleAdapter({
    baseUrl: "https://provider.test/v1/",
    apiKey: "secret",
    completionModel: "chat-model",
    embeddingModel: "embed-model",
    fetchImpl
  });

  assert.deepEqual(await adapter.complete({ messages: [{ role: "user", content: "hi" }] }), {
    content: "answer",
    model: "chat-model"
  });
  assert.deepEqual(await adapter.embed({ texts: ["one", "two"] }), [
    [0.1, 0.2],
    [0.3, 0.4]
  ]);
  assert.equal(requests.length, 2);
});

test("OpenAI-compatible adapter throws ProviderUnavailableError on network failure", async () => {
  const adapter = createOpenAICompatibleAdapter({
    baseUrl: "https://provider.test/v1",
    completionModel: "chat-model",
    embeddingModel: "embed-model",
    fetchImpl: async () => {
      throw new Error("offline");
    }
  });

  await assert.rejects(
    () => adapter.complete({ messages: [{ role: "user", content: "hi" }] }),
    ProviderUnavailableError
  );
});
