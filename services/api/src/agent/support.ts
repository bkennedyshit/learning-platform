import { randomUUID } from "node:crypto";

/** Injectable clock for deterministic tests. */
export type Clock = () => Date;

/** Injectable id factory for deterministic tests. */
export type IdFactory = (prefix?: string) => string;

export const systemClock: Clock = () => new Date();

export const uuidIdFactory: IdFactory = (prefix) => (prefix ? `${prefix}_${randomUUID()}` : randomUUID());

/** Deterministic monotonically-increasing id factory for tests. */
export function sequentialIdFactory(seed = 0): IdFactory {
  let counter = seed;
  return (prefix = "id") => `${prefix}_${(counter += 1).toString().padStart(4, "0")}`;
}

/** Deterministic fixed-step clock for tests. */
export function steppedClock(startIso: string, stepMs = 1000): Clock {
  let current = new Date(startIso).getTime();
  return () => {
    const value = new Date(current);
    current += stepMs;
    return value;
  };
}
