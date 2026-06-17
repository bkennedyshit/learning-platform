import { SESSION_COOKIE_NAME, type SessionSigner } from "./session.js";
import type { Principal } from "./types.js";

export interface SessionEndpointRequest {
  headers: {
    cookie?: string | readonly string[];
  };
}

export type SessionEndpointResponse =
  | {
      status: 200;
      body: {
        principal: Principal;
      };
    }
  | {
      status: 401;
      body: {
        error: "Unauthenticated.";
      };
    };

export function createSessionEndpoint(sessionSigner: SessionSigner) {
  return {
    current(request: SessionEndpointRequest): SessionEndpointResponse {
      const token = readCookieValue(request.headers.cookie, SESSION_COOKIE_NAME);
      const principal = token ? sessionSigner.verify(token) : undefined;

      if (!principal) {
        return {
          status: 401,
          body: { error: "Unauthenticated." }
        };
      }

      return {
        status: 200,
        body: { principal }
      };
    }
  };
}

function readCookieValue(
  cookieHeader: string | readonly string[] | undefined,
  name: string
): string | undefined {
  const header = typeof cookieHeader === "string" ? cookieHeader : cookieHeader?.join("; ");
  if (!header) {
    return undefined;
  }

  for (const part of header.split(";")) {
    const trimmed = part.trim();
    const separatorIndex = trimmed.indexOf("=");
    if (separatorIndex === -1) {
      continue;
    }

    const cookieName = trimmed.slice(0, separatorIndex);
    if (cookieName === name) {
      return trimmed.slice(separatorIndex + 1);
    }
  }

  return undefined;
}
