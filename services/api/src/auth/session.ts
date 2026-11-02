import { createHmac, randomBytes, timingSafeEqual } from "node:crypto";
import { isPrincipal, type Principal } from "./types.js";

export const SESSION_COOKIE_NAME = "learning_session";

/** Default session lifetime: 12 hours. */
export const DEFAULT_SESSION_TTL_MS = 1000 * 60 * 60 * 12;

/** Injectable clock so signing/verification are deterministic under test. */
export type SessionClock = () => Date;

export interface SessionClaims {
  principal: Principal;
  /** ISO timestamp the token was issued. */
  issuedAt: string;
  /** ISO timestamp after which the token is invalid. */
  expiresAt: string;
}

export interface SessionSignerOptions {
  secret: string;
  /** Injectable clock (defaults to system time). */
  clock?: SessionClock;
  /** Token lifetime in milliseconds (defaults to {@link DEFAULT_SESSION_TTL_MS}). */
  ttlMs?: number;
  /**
   * When false, the cookie is emitted without the `Secure` attribute so it can
   * be used over plain http in a local self-hosted quickstart. Defaults to true.
   */
  secureCookie?: boolean;
}

export interface SessionSigner {
  sign(principal: Principal): string;
  /** Returns the principal for a valid, unexpired, untampered token. */
  verify(token: string): Principal | undefined;
  /** Returns the full claims (principal + issuedAt/expiresAt) for a valid token. */
  verifyClaims(token: string): SessionClaims | undefined;
  toCookie(token: string): string;
}

/**
 * HMAC-signed session tokens. Backwards compatible: `createSessionSigner(secret)`
 * still works, and tokens now embed `issuedAt`/`expiresAt` claims that are
 * enforced against an injectable clock. Legacy bare-principal tokens (no expiry)
 * continue to verify so existing sessions are not invalidated by the upgrade.
 */
export function createSessionSigner(options: string | SessionSignerOptions): SessionSigner {
  const opts = typeof options === "string" ? { secret: options } : options;
  const secret = opts.secret;
  if (secret.length < 32) {
    throw new Error("Session secret must be at least 32 characters.");
  }
  const clock = opts.clock ?? (() => new Date());
  const ttlMs = opts.ttlMs ?? DEFAULT_SESSION_TTL_MS;
  const secureCookie = opts.secureCookie ?? true;

  const signer: SessionSigner = {
    sign(principal) {
      const issued = clock();
      const claims: SessionClaims = {
        principal,
        issuedAt: issued.toISOString(),
        expiresAt: new Date(issued.getTime() + ttlMs).toISOString()
      };
      const payload = base64UrlEncode(JSON.stringify(claims));
      const nonce = randomBytes(16).toString("base64url");
      const unsigned = `${payload}.${nonce}`;
      return `${unsigned}.${signValue(unsigned, secret)}`;
    },

    verifyClaims(token) {
      const parts = token.split(".");
      if (parts.length !== 3) {
        return undefined;
      }
      const [payload, nonce, signature] = parts;
      if (!payload || !nonce || !signature) {
        return undefined;
      }
      const unsigned = `${payload}.${nonce}`;
      if (!safeEqual(signature, signValue(unsigned, secret))) {
        return undefined;
      }

      let parsed: unknown;
      try {
        parsed = JSON.parse(Buffer.from(payload, "base64url").toString("utf8"));
      } catch {
        return undefined;
      }

      // New envelope form: { principal, issuedAt, expiresAt }.
      if (parsed && typeof parsed === "object" && "principal" in parsed) {
        const claims = parsed as SessionClaims;
        if (!isPrincipal(claims.principal)) {
          return undefined;
        }
        if (typeof claims.expiresAt === "string") {
          const exp = Date.parse(claims.expiresAt);
          if (Number.isFinite(exp) && exp <= clock().getTime()) {
            return undefined;
          }
        }
        return {
          principal: claims.principal,
          issuedAt: typeof claims.issuedAt === "string" ? claims.issuedAt : clock().toISOString(),
          expiresAt:
            typeof claims.expiresAt === "string"
              ? claims.expiresAt
              : new Date(clock().getTime() + ttlMs).toISOString()
        };
      }

      // Legacy bare-principal form (pre-upgrade tokens have no expiry).
      if (isPrincipal(parsed)) {
        const now = clock();
        return {
          principal: parsed,
          issuedAt: now.toISOString(),
          expiresAt: new Date(now.getTime() + ttlMs).toISOString()
        };
      }
      return undefined;
    },

    verify(token) {
      return signer.verifyClaims(token)?.principal;
    },

    toCookie(token) {
      const attrs = ["HttpOnly"];
      if (secureCookie) {
        attrs.push("Secure");
      }
      attrs.push("SameSite=Lax", "Path=/");
      return `${SESSION_COOKIE_NAME}=${token}; ${attrs.join("; ")}`;
    }
  };

  return signer;
}

function signValue(value: string, secret: string): string {
  return createHmac("sha256", secret).update(value).digest("base64url");
}

function base64UrlEncode(value: string): string {
  return Buffer.from(value, "utf8").toString("base64url");
}

function safeEqual(actual: string, expected: string): boolean {
  const actualBuffer = Buffer.from(actual);
  const expectedBuffer = Buffer.from(expected);

  return actualBuffer.length === expectedBuffer.length && timingSafeEqual(actualBuffer, expectedBuffer);
}
