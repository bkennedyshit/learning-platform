/**
 * Idempotency for state-changing tool calls. A repeated call with the same
 * (toolName, idempotencyKey) returns the previously recorded output instead of
 * re-applying the effect.
 */
export interface IdempotencyStore {
  get(toolName: string, key: string): Promise<unknown | undefined>;
  set(toolName: string, key: string, output: unknown): Promise<void>;
}

export class InMemoryIdempotencyStore implements IdempotencyStore {
  private readonly records = new Map<string, unknown>();

  private compositeKey(toolName: string, key: string): string {
    return `${toolName}::${key}`;
  }

  async get(toolName: string, key: string): Promise<unknown | undefined> {
    return this.records.get(this.compositeKey(toolName, key));
  }

  async set(toolName: string, key: string, output: unknown): Promise<void> {
    this.records.set(this.compositeKey(toolName, key), output);
  }
}
