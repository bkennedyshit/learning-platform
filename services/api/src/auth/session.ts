import { createHmac, randomBytes, timingSafeEqual } from "node:crypto";
import { isPrincipal, type Principal } from "./types.js";

export const SESSION_COOKIE_NAME = "learning_session";

export interface SessionSigner {
  sign(principal: Principal): string;
  verify(token: string): Principal | undefined;
  toCookie(token: string): string;
}

export function createSessionSigner(secret: string): SessionSigner {
  if (secret.length < 32) {
    throw new Error("Session secret must be at least 32 characters.");
  }

  return {
    sign(principal) {
      const payload = base64UrlEncode(JSON.stringify(principal));
      const nonce = randomBytes(16).toString("base64url");
      const unsigned = `${payload}.${nonce}`;
      return `${unsigned}.${signValue(unsigned, secret)}`;
    },

    verify(token) {
      const parts = token.split(".");
      if (parts.length !== 3) {
        return undefined;
      }

      const [payload, nonce, signature] = parts;
      if (!payload || !nonce || !signature) {
        return undefined;
      }

      const unsigned = `${payload}.${nonce}`;
      const expected = signValue(unsigned, secret);

      if (!safeEqual(signature, expected)) {
        return undefined;
      }

      try {
        const principal = JSON.parse(Buffer.from(payload, "base64url").toString("utf8")) as unknown;
        return isPrincipal(principal) ? principal : undefined;
      } catch {
        return undefined;
      }
    },

    toCookie(token) {
      return `${SESSION_COOKIE_NAME}=${token}; HttpOnly; Secure; SameSite=Lax; Path=/`;
    }
  };
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
