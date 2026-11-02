import assert from "node:assert/strict";
import test from "node:test";
import { loadProviderConfig, GEMINI_DEFAULT_BASE_URL } from "./config.js";
import { ProviderConfigurationError, ProviderUnavailableError } from "./errors.js";
import { createLLMProviderAdapter } from "./factory.js";
import { createGeminiAdapter } from "./gemini.js";
import { createCodexCliAdapter } from "./codexCli.js";
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

test("loads Codex CLI provider from environment", () => {
  assert.deepEqual(
    loadProviderConfig({
      LLM_PROVIDER: "codex",
      LLM_COMPLETION_MODEL: "gpt-5.5",
      CODEX_CLI_PATH: "codex-test",
      CODEX_WORKING_DIRECTORY: "C:\\tmp",
      CODEX_TIMEOUT_MS: "45000"
    }),
    {
      kind: "codex",
      completionModel: "gpt-5.5",
      command: "codex-test",
      workingDirectory: "C:\\tmp",
      timeoutMs: 45000
    }
  );
});

test("Codex CLI adapter uses the injected runner and rejects embeddings", async () => {
  let prompt = "";
  const adapter = createCodexCliAdapter({
    model: "gpt-5.5",
    runner: async (value) => {
      prompt = value;
      return '{"kind":"finish","rationaleSummary":"done"}';
    }
  });
  const completion = await adapter.complete({
    messages: [
      { role: "system", content: "Return JSON." },
      { role: "user", content: "Finish." }
    ]
  });
  assert.equal(completion.model, "gpt-5.5");
  assert.match(prompt, /SYSTEM:\nReturn JSON\./);
  assert.match(prompt, /USER:\nFinish\./);
  await assert.rejects(() => adapter.embed({ texts: ["x"] }), ProviderUnavailableError);
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

test("loads gemini provider with defaults and GEMINI_API_KEY", () => {
  assert.deepEqual(
    loadProviderConfig({ LLM_PROVIDER: "gemini", GEMINI_API_KEY: "gkey" }),
    {
      kind: "gemini",
      baseUrl: GEMINI_DEFAULT_BASE_URL,
      apiKey: "gkey",
      completionModel: "gemini-2.0-flash",
      embeddingModel: "text-embedding-004"
    }
  );
});

test("gemini provider requires an API key", () => {
  assert.throws(() => loadProviderConfig({ LLM_PROVIDER: "gemini" }), ProviderConfigurationError);
});

test("gemini provider falls back to LLM_API_KEY and honors model overrides", () => {
  assert.deepEqual(
    loadProviderConfig({
      LLM_PROVIDER: "gemini",
      LLM_API_KEY: "shared",
      LLM_COMPLETION_MODEL: "gemini-1.5-pro",
      LLM_EMBEDDING_MODEL: "text-embedding-005"
    }),
    {
      kind: "gemini",
      baseUrl: GEMINI_DEFAULT_BASE_URL,
      apiKey: "shared",
      completionModel: "gemini-1.5-pro",
      embeddingModel: "text-embedding-005"
    }
  );
});

test("gemini adapter maps generateContent + batchEmbedContents and sends header auth", async () => {
  const seen: Array<{ url: string; body: any; apiKeyHeader?: string; hasKeyInUrl: boolean }> = [];
  const fetchImpl: typeof fetch = async (input, init) => {
    const url = String(input);
    const headers = new Headers(init?.headers as HeadersInit);
    seen.push({
      url,
      body: JSON.parse(String(init?.body)),
      apiKeyHeader: headers.get("x-goog-api-key") ?? undefined,
      hasKeyInUrl: url.includes("secret-key")
    });
    if (url.includes(":generateContent")) {
      return Response.json({
        candidates: [{ content: { role: "model", parts: [{ text: "Hello " }, { text: "world" }] } }]
      });
    }
    return Response.json({
      embeddings: [{ values: [0.1, 0.2] }, { values: [0.3, 0.4] }]
    });
  };

  const adapter = createGeminiAdapter({
    baseUrl: GEMINI_DEFAULT_BASE_URL,
    apiKey: "secret-key",
    completionModel: "gemini-2.0-flash",
    embeddingModel: "text-embedding-004",
    fetchImpl
  });

  const completion = await adapter.complete({
    messages: [
      { role: "system", content: "Be brief." },
      { role: "user", content: "Hi" }
    ]
  });
  assert.deepEqual(completion, { content: "Hello world", model: "gemini-2.0-flash" });

  const embeddings = await adapter.embed({ texts: ["one", "two"] });
  assert.deepEqual(embeddings, [
    [0.1, 0.2],
    [0.3, 0.4]
  ]);

  // System prompt routed to systemInstruction; no secret ever placed in a URL.
  const gen = seen.find((s) => s.url.includes(":generateContent"))!;
  assert.equal(gen.apiKeyHeader, "secret-key");
  assert.equal(gen.hasKeyInUrl, false);
  assert.deepEqual(gen.body.systemInstruction, { parts: [{ text: "Be brief." }] });
  assert.equal(gen.body.contents.length, 1);
  assert.equal(gen.body.contents[0].role, "user");

  const emb = seen.find((s) => s.url.includes(":batchEmbedContents"))!;
  assert.equal(emb.apiKeyHeader, "secret-key");
  assert.equal(emb.body.requests.length, 2);
});

test("gemini adapter rejects an empty completion", async () => {
  const adapter = createGeminiAdapter({
    baseUrl: GEMINI_DEFAULT_BASE_URL,
    apiKey: "k",
    completionModel: "gemini-2.0-flash",
    embeddingModel: "text-embedding-004",
    fetchImpl: async () => Response.json({ candidates: [{ content: { parts: [] } }] })
  });
  await assert.rejects(
    () => adapter.complete({ messages: [{ role: "user", content: "hi" }] }),
    ProviderUnavailableError
  );
});

test("gemini adapter rejects a blocked prompt", async () => {
  const adapter = createGeminiAdapter({
    baseUrl: GEMINI_DEFAULT_BASE_URL,
    apiKey: "k",
    completionModel: "gemini-2.0-flash",
    embeddingModel: "text-embedding-004",
    fetchImpl: async () => Response.json({ promptFeedback: { blockReason: "SAFETY" } })
  });
  await assert.rejects(
    () => adapter.complete({ messages: [{ role: "user", content: "hi" }] }),
    ProviderUnavailableError
  );
});

test("gemini adapter rejects a mismatched embedding count", async () => {
  const adapter = createGeminiAdapter({
    baseUrl: GEMINI_DEFAULT_BASE_URL,
    apiKey: "k",
    completionModel: "gemini-2.0-flash",
    embeddingModel: "text-embedding-004",
    fetchImpl: async () => Response.json({ embeddings: [{ values: [0.1] }] })
  });
  await assert.rejects(() => adapter.embed({ texts: ["a", "b"] }), ProviderUnavailableError);
});

test("gemini adapter surfaces network failure as ProviderUnavailableError", async () => {
  const adapter = createGeminiAdapter({
    baseUrl: GEMINI_DEFAULT_BASE_URL,
    apiKey: "k",
    completionModel: "gemini-2.0-flash",
    embeddingModel: "text-embedding-004",
    fetchImpl: async () => {
      throw new Error("offline");
    }
  });
  await assert.rejects(
    () => adapter.complete({ messages: [{ role: "user", content: "hi" }] }),
    ProviderUnavailableError
  );
});

test("factory builds a gemini adapter from config", () => {
  const adapter = createLLMProviderAdapter({
    kind: "gemini",
    baseUrl: GEMINI_DEFAULT_BASE_URL,
    apiKey: "k",
    completionModel: "gemini-2.0-flash",
    embeddingModel: "text-embedding-004"
  });
  assert.equal(typeof adapter.complete, "function");
  assert.equal(typeof adapter.embed, "function");
});
