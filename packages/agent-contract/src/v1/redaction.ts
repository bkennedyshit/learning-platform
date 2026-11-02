/**
 * Trace redaction. Traces record observable activity, but must never leak
 * secrets or raw learner PII into stored/rendered trace data.
 */

export const DEFAULT_REDACTED_KEYS = [
  "password",
  "passwordhash",
  "token",
  "apikey",
  "api_key",
  "authorization",
  "cookie",
  "secret",
  "email",
  "birthdate",
  "ssn"
] as const;

const REDACTION_MARKER = "[redacted]";

export interface RedactionOptions {
  redactedKeys?: readonly string[];
  maxDepth?: number;
  maxStringLength?: number;
}

/**
 * Returns a deep copy of `value` with sensitive keys masked. Never mutates the
 * input. Circular references and over-deep structures are truncated.
 */
export function redactValue(value: unknown, options: RedactionOptions = {}): unknown {
  const redactedKeys = (options.redactedKeys ?? DEFAULT_REDACTED_KEYS).map((k) => k.toLowerCase());
  const maxDepth = options.maxDepth ?? 8;
  const maxStringLength = options.maxStringLength ?? 2000;
  const seen = new WeakSet<object>();

  const walk = (input: unknown, depth: number): unknown => {
    if (depth > maxDepth) {
      return REDACTION_MARKER;
    }
    if (typeof input === "string") {
      return input.length > maxStringLength ? `${input.slice(0, maxStringLength)}…` : input;
    }
    if (input === null || typeof input !== "object") {
      return input;
    }
    if (seen.has(input)) {
      return REDACTION_MARKER;
    }
    seen.add(input);

    if (Array.isArray(input)) {
      return input.map((item) => walk(item, depth + 1));
    }

    const output: Record<string, unknown> = {};
    for (const [key, val] of Object.entries(input as Record<string, unknown>)) {
      if (redactedKeys.includes(key.toLowerCase())) {
        output[key] = REDACTION_MARKER;
      } else {
        output[key] = walk(val, depth + 1);
      }
    }
    return output;
  };

  return walk(value, 0);
}

export function redactData(
  data: Record<string, unknown> | undefined,
  options: RedactionOptions = {}
): Record<string, unknown> | undefined {
  if (!data) {
    return undefined;
  }
  return redactValue(data, options) as Record<string, unknown>;
}
