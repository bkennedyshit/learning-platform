import { createServer, type IncomingMessage, type Server, type ServerResponse } from "node:http";
import { pathToFileURL } from "node:url";
import { createFetchHandler } from "./handler.js";
import { getApp, type App } from "./app.js";

/**
 * Adapt a Node {@link IncomingMessage} to a WHATWG {@link Request} so the same
 * fetch-style handler serves both the real server and unit tests.
 */
async function toFetchRequest(req: IncomingMessage): Promise<Request> {
  const host = req.headers.host ?? "localhost";
  const url = `http://${host}${req.url ?? "/"}`;
  const method = req.method ?? "GET";

  const headers = new Headers();
  for (const [key, value] of Object.entries(req.headers)) {
    if (value === undefined) continue;
    headers.set(key, Array.isArray(value) ? value.join(", ") : value);
  }

  let body: Buffer | undefined;
  if (method !== "GET" && method !== "HEAD") {
    const chunks: Buffer[] = [];
    for await (const chunk of req) {
      chunks.push(chunk as Buffer);
    }
    body = Buffer.concat(chunks);
  }

  return new Request(url, {
    method,
    headers,
    ...(body && body.length > 0 ? { body: new Uint8Array(body) } : {})
  });
}

async function writeResponse(res: ServerResponse, response: Response): Promise<void> {
  const headers: Record<string, string | string[]> = {};
  response.headers.forEach((value, key) => {
    if (key.toLowerCase() === "set-cookie") return;
    headers[key] = value;
  });
  const setCookies =
    typeof response.headers.getSetCookie === "function" ? response.headers.getSetCookie() : [];
  if (setCookies.length > 0) {
    headers["set-cookie"] = setCookies;
  }
  res.writeHead(response.status, headers);
  const text = await response.text();
  res.end(text);
}

export function createNodeServer(app: App): Server {
  const handler = createFetchHandler(app);
  return createServer((req, res) => {
    void (async () => {
      try {
        const request = await toFetchRequest(req);
        const response = await handler(request);
        await writeResponse(res, response);
      } catch (err) {
        res.writeHead(500, { "content-type": "application/json" });
        res.end(
          JSON.stringify({
            error: { code: "internal_error", message: err instanceof Error ? err.message : "error", retryable: true }
          })
        );
      }
    })();
  });
}

export function startServer(app: App = getApp()): Server {
  const server = createNodeServer(app);
  server.listen(app.config.port, () => {
    // eslint-disable-next-line no-console
    console.log(`learning-agent API listening on :${app.config.port}`);
  });
  return server;
}

// Start when executed directly (pnpm start -> node dist/http/server.js).
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  startServer();
}
