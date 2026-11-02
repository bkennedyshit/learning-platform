/**
 * Portable extraction of Set-Cookie values from a fetch Response's Headers.
 *
 * `Headers.getSetCookie()` is the correct API and preserves multiple cookies,
 * but it is not available on every runtime/polyfill. When it is missing we fall
 * back to `Headers.get("set-cookie")`, which returns the (possibly combined)
 * single header value. This keeps the auth cookie flowing through the proxy on
 * runtimes that lack `getSetCookie`.
 */
export function extractSetCookies(headers: Headers): string[] {
  const withGetter = headers as unknown as { getSetCookie?: () => string[] };
  if (typeof withGetter.getSetCookie === "function") {
    return withGetter.getSetCookie.call(headers) ?? [];
  }
  const single = headers.get("set-cookie");
  return single ? [single] : [];
}
