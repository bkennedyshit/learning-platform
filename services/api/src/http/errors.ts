import type { StructuredError } from "@learning-platform/agent-contract";

/** An error that maps to an HTTP status and a structured error body. */
export class HttpError extends Error {
  constructor(
    readonly status: number,
    readonly code: string,
    message: string,
    readonly retryable = false,
    readonly details?: Record<string, unknown>
  ) {
    super(message);
    this.name = "HttpError";
  }

  toStructured(): StructuredError {
    return {
      code: this.code,
      message: this.message,
      retryable: this.retryable,
      ...(this.details ? { details: this.details } : {})
    };
  }
}

export const badRequest = (message: string, details?: Record<string, unknown>): HttpError =>
  new HttpError(400, "bad_request", message, false, details);
export const unauthenticated = (message = "Authentication required."): HttpError =>
  new HttpError(401, "unauthenticated", message);
export const forbidden = (message = "Access denied."): HttpError => new HttpError(403, "forbidden", message);
export const notFound = (message = "Not found."): HttpError => new HttpError(404, "not_found", message);
export const payloadTooLarge = (message = "Request body too large."): HttpError =>
  new HttpError(413, "payload_too_large", message);
export const methodNotAllowed = (message = "Method not allowed."): HttpError =>
  new HttpError(405, "method_not_allowed", message);
