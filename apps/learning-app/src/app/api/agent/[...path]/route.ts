import { NextRequest } from "next/server";
import { extractSetCookies } from "../../../../lib/setCookie";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// The learner app never talks to model providers directly. It proxies agent
// requests to the authenticated backend (AGENT_API_URL), forwarding only the
// session cookie / bearer token and returning any Set-Cookie unchanged. No
// provider credentials are ever read here or exposed to the browser.
const AGENT_API_URL = process.env.AGENT_API_URL || "http://localhost:8787";

async function proxy(req: NextRequest, path: string[]): Promise<Response> {
  const suffix = path.join("/");
  const search = req.nextUrl.search;
  const target = `${AGENT_API_URL.replace(/\/$/, "")}/${suffix}${search}`;

  const headers = new Headers();
  const cookie = req.headers.get("cookie");
  if (cookie) headers.set("cookie", cookie);
  const auth = req.headers.get("authorization");
  if (auth) headers.set("authorization", auth);
  const contentType = req.headers.get("content-type");
  if (contentType) headers.set("content-type", contentType);
  const origin = req.headers.get("origin");
  if (origin) headers.set("origin", origin);

  const method = req.method.toUpperCase();
  const hasBody = method !== "GET" && method !== "HEAD";
  const body = hasBody ? await req.text() : undefined;

  let upstream: Response;
  try {
    upstream = await fetch(target, {
      method,
      headers,
      ...(body !== undefined && body.length > 0 ? { body } : {}),
      redirect: "manual"
    });
  } catch {
    return Response.json(
      { error: { code: "agent_unavailable", message: "The learning agent service is unavailable.", retryable: true } },
      { status: 503 }
    );
  }

  const respHeaders = new Headers();
  const upstreamType = upstream.headers.get("content-type");
  if (upstreamType) respHeaders.set("content-type", upstreamType);
  for (const c of extractSetCookies(upstream.headers)) {
    respHeaders.append("set-cookie", c);
  }

  const payload = await upstream.arrayBuffer();
  return new Response(payload, { status: upstream.status, headers: respHeaders });
}

interface Ctx {
  params: Promise<{ path?: string[] }>;
}

async function handle(req: NextRequest, ctx: Ctx): Promise<Response> {
  const { path } = await ctx.params;
  return proxy(req, path ?? []);
}

export const GET = handle;
export const POST = handle;
export const PUT = handle;
export const PATCH = handle;
export const DELETE = handle;
