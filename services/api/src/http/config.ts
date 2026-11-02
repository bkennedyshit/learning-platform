import path from "node:path";
import { DEFAULT_SESSION_TTL_MS } from "../auth/session.js";

export interface HttpConfig {
  /** Absolute directory that roots FileLearnerMemory. Required in production. */
  agentDataDir: string;
  /**
   * Absolute path to the generated catalog manifest (`content.json`). When set,
   * the agent grounds turns in the full catalog instead of only the seed
   * fixture. Service configuration only — never model/UI input.
   */
  agentCatalogPath: string;
  /**
   * Optional absolute directory for the internal reviewed-draft publication
   * outbox. When set, educator publish queues an immutable reviewed package
   * here; a reviewed commit / static build later consumes it. Never public.
   */
  agentPublicationOutbox: string;
  /** HMAC secret for signing session tokens (>= 32 chars). */
  sessionSecret: string;
  /** When true, POST /v1/auth/dev-session issues sessions without a password. */
  allowDevAuth: boolean;
  /** Emit the `Secure` cookie attribute (disable for local http). */
  secureCookie: boolean;
  /** Session lifetime in ms. */
  sessionTtlMs: number;
  /** Allowlisted CORS origins; empty disables CORS. */
  corsOrigins: string[];
  /** Maximum accepted request body size in bytes. */
  maxBodyBytes: number;
  /** TCP port for the node:http server. */
  port: number;
}

const DEFAULT_MAX_BODY_BYTES = 256 * 1024;

/**
 * Load HTTP configuration from the environment. Throws early for missing
 * production-critical values (data dir, session secret) so misconfiguration is
 * loud rather than silently insecure.
 */
export function loadHttpConfig(env: NodeJS.ProcessEnv = process.env): HttpConfig {
  const agentDataDir = env.AGENT_DATA_DIR?.trim();
  if (!agentDataDir) {
    throw new Error("AGENT_DATA_DIR is required (absolute directory that roots learner memory).");
  }
  const sessionSecret = env.AGENT_SESSION_SECRET?.trim();
  if (!sessionSecret || sessionSecret.length < 32) {
    throw new Error("AGENT_SESSION_SECRET is required and must be at least 32 characters.");
  }

  const corsOrigins = (env.AGENT_CORS_ORIGINS ?? "")
    .split(",")
    .map((o) => o.trim())
    .filter(Boolean);

  const agentCatalogPath = env.AGENT_CATALOG_PATH?.trim() ?? "";
  if (agentCatalogPath && !isAbsolutePath(agentCatalogPath)) {
    throw new Error("AGENT_CATALOG_PATH must be an absolute path when set.");
  }

  const agentPublicationOutbox = env.AGENT_PUBLICATION_OUTBOX?.trim() ?? "";
  if (agentPublicationOutbox && !isAbsolutePath(agentPublicationOutbox)) {
    throw new Error("AGENT_PUBLICATION_OUTBOX must be an absolute path when set.");
  }

  return {
    agentDataDir,
    agentCatalogPath,
    agentPublicationOutbox,
    sessionSecret,
    allowDevAuth: env.ALLOW_DEV_AUTH === "true",
    secureCookie: env.AGENT_INSECURE_COOKIES !== "true",
    sessionTtlMs: env.AGENT_SESSION_TTL_MS ? Number(env.AGENT_SESSION_TTL_MS) : DEFAULT_SESSION_TTL_MS,
    corsOrigins,
    maxBodyBytes: env.AGENT_MAX_BODY_BYTES ? Number(env.AGENT_MAX_BODY_BYTES) : DEFAULT_MAX_BODY_BYTES,
    port: env.PORT ? Number(env.PORT) : 8787
  };
}

/**
 * Absolute-path check that accepts both POSIX (`/srv/...`) and Windows
 * (`C:\...`) roots regardless of the host OS, so config is portable across
 * deployment targets.
 */
function isAbsolutePath(value: string): boolean {
  return path.isAbsolute(value) || /^([a-zA-Z]:[\\/]|\\\\)/.test(value) || value.startsWith("/");
}
