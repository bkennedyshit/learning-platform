import { createSessionSigner, type SessionSigner, type SessionClock } from "../auth/session.js";
import { createLearningAgent, type LearningAgentDeps } from "../agent/index.js";
import { PublicationOutbox } from "../agent/publication/index.js";
import { FileLearnerMemory } from "../agent/memory/fileStore.js";
import type { LearnerMemory } from "../agent/memory/index.js";
import { VerticalFixture } from "../agent/tools/fixture.js";
import { loadCatalogIntoFixture } from "../agent/tools/catalog.js";
import { createLlmAgentModel, type AgentModel } from "../agent/model.js";
import { systemClock, uuidIdFactory, type Clock, type IdFactory } from "../agent/support.js";
import { loadProviderConfig, createLLMProviderAdapter } from "@learning-platform/llm-adapter";
import { loadHttpConfig, type HttpConfig } from "./config.js";
import type { RunTurnInput } from "./runTurn.js";

/**
 * Produces the {@link AgentModel} used to drive a turn. When a hosted/local
 * provider is configured the runtime is driven by the provider; otherwise the
 * deterministic scripted model is used. Provider payloads never leak into tools.
 */
export type AgentModelFactory = (input: RunTurnInput) => AgentModel;

export interface App {
  config: HttpConfig;
  memory: LearnerMemory;
  signer: SessionSigner;
  agent: LearningAgentDeps;
  clock: Clock;
  idFactory: IdFactory;
  /** Optional provider-driven model factory; absent means deterministic scripted planning. */
  agentModelFactory?: AgentModelFactory;
}

export interface CreateAppOverrides {
  config?: Partial<HttpConfig>;
  memory?: LearnerMemory;
  clock?: Clock;
  idFactory?: IdFactory;
  /** Inject a model factory (tests) to prove provider-driven parity deterministically. */
  agentModelFactory?: AgentModelFactory;
}

const DEFAULTS = {
  agentDataDir: "",
  agentCatalogPath: "",
  agentPublicationOutbox: "",
  sessionSecret: "",
  allowDevAuth: false,
  secureCookie: true,
  sessionTtlMs: 1000 * 60 * 60 * 12,
  corsOrigins: [] as string[],
  maxBodyBytes: 256 * 1024,
  port: 8787
} satisfies HttpConfig;

/**
 * Build a fully-wired application. Memory is FileLearnerMemory rooted ONLY in
 * `AGENT_DATA_DIR` (model-supplied paths never reach it). When `AGENT_CATALOG_PATH`
 * is configured the fixture is grounded in the full generated catalog. Tests
 * inject an in-memory store and a deterministic clock/id factory via
 * {@link CreateAppOverrides}, supplying an inline `config.sessionSecret` so no
 * environment is required.
 */
export function createApp(overrides: CreateAppOverrides = {}): App {
  // If a caller supplies an inline secret, treat overrides as authoritative and
  // skip environment loading (used by tests). Otherwise load from the env.
  const inlineTestConfig = Boolean(overrides.config?.sessionSecret);
  const config: HttpConfig = inlineTestConfig
    ? { ...DEFAULTS, ...overrides.config }
    : { ...loadHttpConfig(), ...overrides.config };

  const clock = overrides.clock ?? systemClock;
  const idFactory = overrides.idFactory ?? uuidIdFactory;
  const memory = overrides.memory ?? new FileLearnerMemory({ root: config.agentDataDir });

  const signerClock: SessionClock = () => clock();
  const signer = createSessionSigner({
    secret: config.sessionSecret,
    clock: signerClock,
    ttlMs: config.sessionTtlMs,
    secureCookie: config.secureCookie
  });

  // Ground the agent in the full catalog when configured; otherwise the two
  // seed lessons remain available. Loading is loud on misconfiguration.
  const fixture = new VerticalFixture();
  if (config.agentCatalogPath) {
    loadCatalogIntoFixture(fixture, config.agentCatalogPath);
  }

  const publicationOutbox = config.agentPublicationOutbox
    ? new PublicationOutbox(config.agentPublicationOutbox)
    : undefined;

  const agent = createLearningAgent({
    memory,
    clock,
    idFactory,
    fixture,
    ...(publicationOutbox ? { publicationOutbox } : {})
  });

  const agentModelFactory = resolveAgentModelFactory(overrides, inlineTestConfig);

  return {
    config,
    memory,
    signer,
    agent,
    clock,
    idFactory,
    ...(agentModelFactory ? { agentModelFactory } : {})
  };
}

/**
 * Decide how turns are driven. An injected factory (tests) always wins. When a
 * hosted/local provider is configured we build a provider-driven model. If the
 * provider is absent or misconfigured we fail SAFELY to deterministic scripted
 * planning rather than throwing — we never pretend a live provider ran.
 */
function resolveAgentModelFactory(
  overrides: CreateAppOverrides,
  inlineTestConfig: boolean
): AgentModelFactory | undefined {
  if (overrides.agentModelFactory) {
    return overrides.agentModelFactory;
  }
  // Tests supplying an inline secret must stay deterministic unless they inject
  // a factory explicitly.
  if (inlineTestConfig) {
    return undefined;
  }
  try {
    const providerConfig = loadProviderConfig();
    if (
      providerConfig.kind === "local" ||
      providerConfig.kind === "hosted" ||
      providerConfig.kind === "gemini" ||
      providerConfig.kind === "codex"
    ) {
      const adapter = createLLMProviderAdapter(providerConfig);
      const model = createLlmAgentModel(adapter, providerConfig.kind);
      return () => model;
    }
  } catch {
    // Missing/invalid provider config → deterministic scripted planning.
    return undefined;
  }
  return undefined;
}

let singleton: App | undefined;

/** Process-wide singleton application. */
export function getApp(): App {
  if (!singleton) {
    singleton = createApp();
  }
  return singleton;
}
