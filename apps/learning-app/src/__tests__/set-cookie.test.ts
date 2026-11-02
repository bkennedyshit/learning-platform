import { describe, it, expect } from "vitest";
import { extractSetCookies } from "../lib/setCookie";

describe("extractSetCookies", () => {
  it("uses getSetCookie when available (preserving multiple cookies)", () => {
    const headers = {
      getSetCookie: () => ["a=1", "b=2"],
      get: () => null
    } as unknown as Headers;
    expect(extractSetCookies(headers)).toEqual(["a=1", "b=2"]);
  });

  it("falls back to get('set-cookie') when getSetCookie is unavailable", () => {
    const headers = {
      get: (k: string) => (k.toLowerCase() === "set-cookie" ? "learning_session=abc; Path=/" : null)
    } as unknown as Headers;
    expect(extractSetCookies(headers)).toEqual(["learning_session=abc; Path=/"]);
  });

  it("returns an empty array when there is no Set-Cookie header", () => {
    const headers = { get: () => null } as unknown as Headers;
    expect(extractSetCookies(headers)).toEqual([]);
  });
});
