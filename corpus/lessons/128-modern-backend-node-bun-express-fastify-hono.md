---
title: "12.8 — Modern Backend: Node, Bun, Express, Fastify, Hono"
subject: "JavaScript"
catalog: advanced
audience_tier: higher-education
chapter: "12.8"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 12.8 — Modern Backend: Node, Bun, Express, Fastify, Hono

> *"Express was the right framework for 2010. It's 2026. We can do better."* — **Yusuke Wada**, creator of Hono

> *"The edge is not a place. It's a philosophy: run code as close to the user as possible."* — **Sunil Pai**, Cloudflare Workers team

JavaScript on the server has evolved dramatically. Express (2010) defined the middleware pattern that every framework since has adopted, but it's showing its age — no native async/await support, no TypeScript, no schema validation, no edge runtime compatibility. Modern alternatives like **Fastify** and **Hono** keep the middleware mental model while adding type safety, validation, and multi-runtime support.

This chapter builds your server-side JavaScript skills from Express fundamentals through modern alternatives to edge deployment.

---

## 🎯 Learning Objectives

1. **Explain the middleware pattern** and implement custom middleware.
2. **Build REST APIs** with Express, Fastify, and Hono.
3. **Implement proper error handling** with centralized error middleware.
4. **Add request validation** using schema-based approaches (Zod, TypeBox).
5. **Use Node.js Streams** for efficient data processing.
6. **Deploy to edge runtimes** (Cloudflare Workers, Vercel Edge).
7. **Choose the right framework** for a given project's constraints.

---

## 🖼️ Visual Anchor — Backend Framework Architecture

![js__5.8-fig1](js__5.8-fig1.svg)

---

## 📚 1. The Middleware Pattern

### Definition 12.8.1 — Middleware

Middleware is a function that sits between the request and the response, forming a **pipeline**:

```
Request → [Logger] → [Auth] → [Validate] → [Handler] → Response
              │          │          │            │
              ▼          ▼          ▼            ▼
           Log req    Check JWT  Validate    Business
           timing     token      body/params  logic
```

Every middleware can:
1. **Execute code** (logging, timing, parsing)
2. **Modify** the request or response objects
3. **End the request-response cycle** (send a response)
4. **Call the next middleware** in the stack

```javascript
// Generic middleware signature (Express-style)
function middleware(req, res, next) {
  // Do something
  next(); // Pass to next middleware
}

// Hono/Fastify style (modern — async, no callback)
async function middleware(c, next) {
  // Before handler
  const start = Date.now();
  await next();
  // After handler
  const duration = Date.now() - start;
  c.header("X-Response-Time", `${duration}ms`);
}
```

---

## 📚 2. Express — The Foundation (Legacy but Ubiquitous)

### Definition 12.8.2 — Express Basics

```javascript
import express from "express";

const app = express();

// Built-in middleware
app.use(express.json());        // Parse JSON bodies
app.use(express.urlencoded({ extended: true })); // Parse form data

// Custom middleware
app.use((req, res, next) => {
  req.requestTime = Date.now();
  console.log(`${req.method} ${req.url}`);
  next();
});

// Routes
app.get("/api/users", async (req, res) => {
  const users = await db.users.findAll();
  res.json(users);
});

app.get("/api/users/:id", async (req, res) => {
  const user = await db.users.findById(req.params.id);
  if (!user) return res.status(404).json({ error: "Not found" });
  res.json(user);
});

app.post("/api/users", async (req, res) => {
  const { name, email } = req.body;
  const user = await db.users.create({ name, email });
  res.status(201).json(user);
});

// Error handling middleware (4 params = error handler)
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.status ?? 500).json({
    error: err.message ?? "Internal Server Error",
  });
});

app.listen(3000, () => console.log("Server running on :3000"));
```

### Express Limitations (Why We Need Alternatives)

| Issue | Impact |
|-------|--------|
| No native async error handling | Must wrap every handler in try/catch or use `express-async-errors` |
| No TypeScript support | Types are community-maintained, often incomplete |
| No built-in validation | Need `express-validator`, `joi`, or `zod` manually |
| No schema-based serialization | Can't auto-generate OpenAPI docs |
| Callback-based internals | Performance ceiling vs modern alternatives |
| No edge runtime support | Can't deploy to Cloudflare Workers, Deno Deploy |

---

## 📚 3. Fastify — The Performance King

### Definition 12.8.3 — Fastify Architecture

**Fastify** (2016) is designed for speed and developer experience:

```javascript
import Fastify from "fastify";

const app = Fastify({
  logger: true, // Built-in Pino logger (structured JSON)
});

// Schema-based validation + serialization (fastest approach)
const getUserSchema = {
  params: {
    type: "object",
    properties: {
      id: { type: "string", format: "uuid" },
    },
    required: ["id"],
  },
  response: {
    200: {
      type: "object",
      properties: {
        id: { type: "string" },
        name: { type: "string" },
        email: { type: "string", format: "email" },
        createdAt: { type: "string", format: "date-time" },
      },
    },
  },
};

app.get("/api/users/:id", { schema: getUserSchema }, async (request, reply) => {
  const { id } = request.params; // Already validated!
  const user = await db.users.findById(id);
  if (!user) {
    reply.code(404);
    return { error: "User not found" };
  }
  return user; // Auto-serialized per response schema (faster than JSON.stringify)
});

// Plugins (encapsulated middleware)
app.register(import("@fastify/cors"), { origin: true });
app.register(import("@fastify/helmet"));
app.register(import("@fastify/rate-limit"), { max: 100, timeWindow: "1 minute" });

// Hooks (lifecycle events)
app.addHook("onRequest", async (request, reply) => {
  // Auth check
  const token = request.headers.authorization?.replace("Bearer ", "");
  if (!token) {
    reply.code(401);
    return reply.send({ error: "Unauthorized" });
  }
  request.user = await verifyToken(token);
});

await app.listen({ port: 3000, host: "0.0.0.0" });
```

### Why Fastify Is Fast

1. **Schema-based serialization** — Compiles JSON schemas into optimized serialization functions (faster than `JSON.stringify`)
2. **Radix tree router** — O(log n) route matching vs Express's linear scan
3. **Plugin encapsulation** — Plugins are isolated, preventing middleware bloat
4. **Pino logger** — 5x faster than Winston/Morgan

---

## 📚 4. Hono — The Edge-First Framework

### Definition 12.8.4 — Hono Architecture

**Hono** (2022, Yusuke Wada) is a tiny (~14KB), ultrafast framework that runs on ANY JavaScript runtime:

```javascript
import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";
import { validator } from "hono/validator";
import { jwt } from "hono/jwt";
import { zValidator } from "@hono/zod-validator";
import { z } from "zod";

const app = new Hono();

// Built-in middleware
app.use("*", logger());
app.use("*", cors());

// JWT auth for /api routes
app.use("/api/*", jwt({ secret: process.env.JWT_SECRET }));

// Zod validation
const createUserSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
  role: z.enum(["admin", "user"]).default("user"),
});

app.post("/api/users", zValidator("json", createUserSchema), async (c) => {
  const data = c.req.valid("json"); // Fully typed and validated!
  const user = await db.users.create(data);
  return c.json(user, 201);
});

app.get("/api/users/:id", async (c) => {
  const id = c.req.param("id");
  const user = await db.users.findById(id);
  if (!user) return c.json({ error: "Not found" }, 404);
  return c.json(user);
});

// Grouped routes
const admin = new Hono();
admin.use("*", adminOnly); // Custom middleware
admin.get("/stats", async (c) => {
  return c.json(await getStats());
});
app.route("/admin", admin);

// Works on ANY runtime
export default app; // Cloudflare Workers
// OR: serve(app, { port: 3000 }); // Node.js
// OR: Bun.serve({ fetch: app.fetch }); // Bun
```

### Hono's Multi-Runtime Support

```javascript
// Deploy the SAME code to different runtimes:

// Node.js
import { serve } from "@hono/node-server";
serve(app, { port: 3000 });

// Bun
export default { port: 3000, fetch: app.fetch };

// Cloudflare Workers
export default app;

// Deno
Deno.serve(app.fetch);

// AWS Lambda
import { handle } from "hono/aws-lambda";
export const handler = handle(app);

// Vercel Edge
export const config = { runtime: "edge" };
export default app;
```

### Why Hono for 2026

| Feature | Hono | Express | Fastify |
|---------|------|---------|---------|
| Bundle size | 14KB | 200KB+ | 300KB+ |
| Multi-runtime | ✅ All | ❌ Node only | ⚠️ Node mainly |
| TypeScript | ✅ Native | ⚠️ @types | ✅ Native |
| Validation | ✅ Built-in + Zod | ❌ Manual | ✅ JSON Schema |
| Edge deploy | ✅ First-class | ❌ No | ⚠️ Limited |
| Performance | 🏆 Fastest | Slowest | Fast |
| Ecosystem | Growing | 🏆 Largest | Large |

---

## 📚 5. Middleware Patterns (Universal)

### Authentication Middleware

```javascript
// Hono example (same pattern applies to Express/Fastify)
import { verify } from "hono/jwt";

function authMiddleware(secret) {
  return async (c, next) => {
    const header = c.req.header("Authorization");
    if (!header?.startsWith("Bearer ")) {
      return c.json({ error: "Missing token" }, 401);
    }

    try {
      const token = header.slice(7);
      const payload = await verify(token, secret);
      c.set("user", payload); // Attach to context
      await next();
    } catch {
      return c.json({ error: "Invalid token" }, 401);
    }
  };
}

app.use("/api/*", authMiddleware(process.env.JWT_SECRET));
```

### Rate Limiting

```javascript
function rateLimit({ windowMs = 60000, max = 100 } = {}) {
  const hits = new Map();

  return async (c, next) => {
    const key = c.req.header("x-forwarded-for") ?? "unknown";
    const now = Date.now();
    const record = hits.get(key) ?? { count: 0, resetAt: now + windowMs };

    if (now > record.resetAt) {
      record.count = 0;
      record.resetAt = now + windowMs;
    }

    record.count++;
    hits.set(key, record);

    if (record.count > max) {
      c.header("Retry-After", String(Math.ceil((record.resetAt - now) / 1000)));
      return c.json({ error: "Too many requests" }, 429);
    }

    c.header("X-RateLimit-Remaining", String(max - record.count));
    await next();
  };
}
```

### Error Handling

```javascript
// Centralized error handler (Hono)
app.onError((err, c) => {
  console.error(`${c.req.method} ${c.req.url}:`, err);

  if (err instanceof z.ZodError) {
    return c.json({ error: "Validation failed", details: err.errors }, 400);
  }

  if (err.status) {
    return c.json({ error: err.message }, err.status);
  }

  return c.json({ error: "Internal Server Error" }, 500);
});

// Custom error classes
class AppError extends Error {
  constructor(message, status = 500) {
    super(message);
    this.status = status;
  }
}

class NotFoundError extends AppError {
  constructor(resource = "Resource") {
    super(`${resource} not found`, 404);
  }
}
```

---

## 📚 6. Node.js Streams

### Definition 12.8.5 — Streaming Data

Streams process data in chunks without loading everything into memory:

```javascript
import { createReadStream, createWriteStream } from "node:fs";
import { pipeline } from "node:stream/promises";
import { createGzip } from "node:zlib";
import { Transform } from "node:stream";

// Pipe file through gzip compression
await pipeline(
  createReadStream("large-file.json"),
  createGzip(),
  createWriteStream("large-file.json.gz")
);

// Custom transform stream
const upperCase = new Transform({
  transform(chunk, encoding, callback) {
    callback(null, chunk.toString().toUpperCase());
  },
});

// Streaming HTTP response (Hono)
app.get("/api/export", async (c) => {
  const stream = new ReadableStream({
    async start(controller) {
      const cursor = db.users.findCursor();
      for await (const user of cursor) {
        controller.enqueue(JSON.stringify(user) + "\n");
      }
      controller.close();
    },
  });

  return new Response(stream, {
    headers: { "Content-Type": "application/x-ndjson" },
  });
});
```

### Server-Sent Events (SSE)

```javascript
// SSE for real-time updates (simpler than WebSockets for one-way)
app.get("/api/events", async (c) => {
  const stream = new ReadableStream({
    start(controller) {
      const encoder = new TextEncoder();

      const interval = setInterval(() => {
        const data = JSON.stringify({ time: Date.now(), value: Math.random() });
        controller.enqueue(encoder.encode(`data: ${data}\n\n`));
      }, 1000);

      // Cleanup on client disconnect
      c.req.raw.signal.addEventListener("abort", () => {
        clearInterval(interval);
        controller.close();
      });
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  });
});

// Client-side consumption
const events = new EventSource("/api/events");
events.onmessage = (e) => console.log(JSON.parse(e.data));
```

---

## 📚 7. Database Integration Patterns

```javascript
// Using Drizzle ORM (type-safe, lightweight)
import { drizzle } from "drizzle-orm/node-postgres";
import { pgTable, text, timestamp, uuid } from "drizzle-orm/pg-core";
import { eq } from "drizzle-orm";

// Schema definition
const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  name: text("name").notNull(),
  email: text("email").notNull().unique(),
  createdAt: timestamp("created_at").defaultNow(),
});

// Usage in route handler
app.get("/api/users", async (c) => {
  const allUsers = await db.select().from(users);
  return c.json(allUsers);
});

app.get("/api/users/:id", async (c) => {
  const [user] = await db
    .select()
    .from(users)
    .where(eq(users.id, c.req.param("id")));
  if (!user) return c.json({ error: "Not found" }, 404);
  return c.json(user);
});
```

---

## 📚 8. Edge Runtimes & Deployment

### Definition 12.8.6 — What Is "The Edge"?

Edge runtimes run your code in data centers close to users worldwide (CDN nodes). They use V8 isolates — lightweight sandboxes that start in <5ms:

```
Traditional Server:          Edge Runtime:
┌─────────┐                  ┌─────────┐ ┌─────────┐ ┌─────────┐
│ US-East │ ← all traffic    │ US-East │ │ EU-West │ │ AP-South│
│ Server  │                  │  Edge   │ │  Edge   │ │  Edge   │
└─────────┘                  └─────────┘ └─────────┘ └─────────┘
                                    ↑          ↑          ↑
                              US users    EU users    Asia users
                              (~20ms)     (~20ms)     (~20ms)
```

### Cloudflare Workers Deployment

```javascript
// wrangler.toml
// name = "my-api"
// main = "src/index.ts"
// compatibility_date = "2024-01-01"

// src/index.ts
import { Hono } from "hono";

const app = new Hono();

app.get("/", (c) => c.json({ message: "Hello from the edge!" }));
app.get("/api/geo", (c) => {
  // Cloudflare provides geo data automatically
  return c.json({
    country: c.req.header("cf-ipcountry"),
    city: c.req.raw.cf?.city,
  });
});

export default app;
```

```bash
# Deploy
npx wrangler deploy
# Your API is now running in 300+ cities worldwide
```

### Edge Limitations

| ✅ Can Do | ❌ Cannot Do |
|-----------|-------------|
| HTTP requests (fetch) | Long-running processes |
| KV storage | Traditional databases (directly) |
| Durable Objects | File system access |
| WebSockets | Native Node.js modules |
| Crypto operations | Unlimited CPU time (usually 10-50ms limit) |

---

## 📚 9. Framework Comparison — When to Use What

| Scenario | Framework | Why |
|----------|-----------|-----|
| Legacy project maintenance | **Express** | Already there, huge middleware ecosystem |
| High-performance API | **Fastify** | Schema serialization, Pino logging |
| Edge deployment | **Hono** | Multi-runtime, tiny bundle |
| Full-stack app | **Next.js API routes** | Co-located with frontend |
| Microservices | **Hono** or **Fastify** | Small footprint, fast startup |
| Real-time (WebSockets) | **Bun** + **Hono** | Bun's native WS is fastest |
| Rapid prototyping | **Hono** + **Bun** | Zero config, TS native |

---

## 🏋️ 10. Exercises

### Exercise 5.8.1 — Build a REST API with Hono

Create a complete CRUD API for a "notes" resource:
1. `GET /api/notes` — list all (with pagination)
2. `POST /api/notes` — create (with Zod validation)
3. `GET /api/notes/:id` — get one
4. `PATCH /api/notes/:id` — update
5. `DELETE /api/notes/:id` — delete
6. Add auth middleware, rate limiting, and error handling

### Exercise 5.8.2 — Streaming Response

Build an endpoint that:
1. Accepts a large CSV file upload
2. Processes it row-by-row using streams (don't load into memory)
3. Returns processed results as NDJSON stream

### Exercise 5.8.3 — Deploy to the Edge

1. Create a Hono app with 3 endpoints
2. Deploy to Cloudflare Workers using Wrangler
3. Add a KV store for caching
4. Measure response times from different geographic locations

---

## 🔗 Cross-References

- **Previous:** [12.7 - Modern Frontend Frameworks Overview](12.7---Modern-Frontend-Frameworks-Overview) — The frontend that consumes these APIs.
- **Async patterns:** [12.3 - Async - Promises, Async_Await, Event Loop](12.3---Async---Promises,-Async_Await,-Event-Loop) — All server code is async.
- **Modules:** [12.5 - Modules & Build Systems](12.5---Modules-&-Build-Systems) — Server-side ESM vs CJS considerations.
- **TypeScript:** [13 - TypeScript](13---TypeScript) — Hono and Fastify have excellent TS support; type your APIs.
- **React full-stack:** [22.1 - React & Next.js - Functional Components & Hooks](22.1---React-&-Next.js---Functional-Components-&-Hooks) — Next.js API routes and Server Actions.

---

## 📖 Further Reading

- [Hono Documentation](https://hono.dev) — Official docs, guides, and middleware catalog
- [Fastify Documentation](https://fastify.dev) — Guides, plugins, and benchmarks
- [Cloudflare Workers Docs](https://developers.cloudflare.com/workers/) — Edge runtime reference
- [Bun HTTP Documentation](https://bun.sh/docs/api/http) — Bun's native HTTP server
- [Node.js Streams Guide](https://nodejs.org/en/docs/guides/backpressuring-in-streams) — Official streams documentation



---

## 🏗️ 8. Extended Worked Examples & Deep Dives

### 8.1 — Hono RPC: Type-Safe Routing

Hono's RPC feature provides end-to-end type safety between server routes and client calls — no code generation needed.

```ts
// server.ts — Define typed routes with Hono
import { Hono } from "hono";
import { zValidator } from "@hono/zod-validator";
import { z } from "zod";

// Define validation schemas
const createUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  role: z.enum(["admin", "user", "moderator"]),
});

const querySchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  search: z.string().optional(),
});

// Create typed routes
const app = new Hono()
  .get("/api/users", zValidator("query", querySchema), async (c) => {
    const { page, limit, search } = c.req.valid("query");
    const users = await db.user.findMany({
      where: search ? { name: { contains: search } } : undefined,
      skip: (page - 1) * limit,
      take: limit,
    });
    return c.json({
      users,
      pagination: { page, limit, total: await db.user.count() },
    });
  })
  .get("/api/users/:id", async (c) => {
    const id = c.req.param("id");
    const user = await db.user.findUnique({ where: { id } });
    if (!user) return c.json({ error: "Not found" }, 404);
    return c.json({ user });
  })
  .post("/api/users", zValidator("json", createUserSchema), async (c) => {
    const data = c.req.valid("json");
    const user = await db.user.create({ data });
    return c.json({ user }, 201);
  })
  .delete("/api/users/:id", async (c) => {
    const id = c.req.param("id");
    await db.user.delete({ where: { id } });
    return c.json({ success: true });
  });

// Export the type for client usage
export type AppType = typeof app;
export default app;
```

```ts
// client.ts — Type-safe client (zero code generation!)
import { hc } from "hono/client";
import type { AppType } from "./server";

// Create typed client
const client = hc<AppType>("http://localhost:3000");

// Full autocomplete and type checking!
const response = await client.api.users.$get({
  query: { page: 1, limit: 10, search: "Bill" },
});
// response type is inferred from server's c.json() return type

const data = await response.json();
// data.users is typed as User[]
// data.pagination is typed as { page: number, limit: number, total: number }

// Create user — body is type-checked against Zod schema
const createResponse = await client.api.users.$post({
  json: {
    name: "Alice",
    email: "alice@example.com",
    role: "admin", // Autocomplete: "admin" | "user" | "moderator"
  },
});

// Path parameters are type-safe too
const userResponse = await client.api.users[":id"].$get({
  param: { id: "user-123" },
});

// DELETE
await client.api.users[":id"].$delete({
  param: { id: "user-123" },
});
```

#### Hono Middleware Stack

```ts
import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";
import { prettyJSON } from "hono/pretty-json";
import { secureHeaders } from "hono/secure-headers";
import { rateLimiter } from "hono-rate-limiter";
import { jwt } from "hono/jwt";

const app = new Hono();

// Global middleware
app.use("*", logger());
app.use("*", secureHeaders());
app.use("*", cors({ origin: ["https://myapp.com"], credentials: true }));
app.use("*", prettyJSON());

// Rate limiting
app.use("/api/*", rateLimiter({
  windowMs: 60 * 1000,  // 1 minute
  limit: 100,            // 100 requests per window
  keyGenerator: (c) => c.req.header("x-forwarded-for") || "unknown",
}));

// Auth middleware (specific routes)
app.use("/api/admin/*", jwt({ secret: process.env.JWT_SECRET }));

// Multi-runtime deployment
// Hono runs on: Cloudflare Workers, Deno, Bun, Node.js, AWS Lambda, Vercel
export default app; // Cloudflare Workers / Bun
// export default { fetch: app.fetch }; // Alternative export
```

---

### 8.2 — Fastify Schema Validation & Serialization

Fastify uses JSON Schema for both validation AND serialization (response shaping), making it significantly faster than Express.

```ts
import Fastify from "fastify";

const fastify = Fastify({
  logger: true,
  ajv: {
    customOptions: {
      removeAdditional: "all", // Strip unknown properties
      coerceTypes: true,       // Coerce "123" → 123
      allErrors: true,         // Report all validation errors
    },
  },
});

// Route with full schema (request + response)
fastify.route({
  method: "POST",
  url: "/api/users",
  schema: {
    // Request validation
    body: {
      type: "object",
      required: ["name", "email"],
      properties: {
        name: { type: "string", minLength: 1, maxLength: 100 },
        email: { type: "string", format: "email" },
        age: { type: "integer", minimum: 0, maximum: 150 },
        tags: {
          type: "array",
          items: { type: "string" },
          maxItems: 10,
        },
      },
      additionalProperties: false,
    },
    querystring: {
      type: "object",
      properties: {
        notify: { type: "boolean", default: false },
      },
    },
    params: {
      type: "object",
      properties: {
        orgId: { type: "string", format: "uuid" },
      },
    },
    // Response serialization (FAST — uses fast-json-stringify)
    response: {
      201: {
        type: "object",
        properties: {
          id: { type: "string" },
          name: { type: "string" },
          email: { type: "string" },
          createdAt: { type: "string", format: "date-time" },
        },
        // Properties NOT listed here are STRIPPED from response
        // This prevents accidental data leaks (passwords, internal fields)
      },
      400: {
        type: "object",
        properties: {
          error: { type: "string" },
          details: { type: "array", items: { type: "object" } },
        },
      },
    },
  },
  handler: async (request, reply) => {
    const { name, email, age, tags } = request.body;
    const { notify } = request.query;

    const user = await db.user.create({
      data: { name, email, age, tags },
    });

    if (notify) {
      await sendWelcomeEmail(user.email);
    }

    // Response is automatically serialized using fast-json-stringify
    // 2-5x faster than JSON.stringify for known schemas!
    reply.code(201).send(user);
  },
});

// Why Fastify's serialization is faster:
// JSON.stringify: must inspect every property at runtime
// fast-json-stringify: generates a specialized serializer from schema at startup
// The generated function knows exactly what properties exist and their types
// Result: ~30,000 serializations/sec vs ~12,000 with JSON.stringify
```

#### Fastify Plugin System

```ts
// Encapsulated plugins (isolated scope)
import fp from "fastify-plugin";

// Database plugin
const dbPlugin = fp(async (fastify, opts) => {
  const pool = new Pool(opts.connectionString);

  // Decorate fastify instance
  fastify.decorate("db", pool);

  // Cleanup on shutdown
  fastify.addHook("onClose", async () => {
    await pool.end();
  });
});

// Auth plugin
const authPlugin = fp(async (fastify) => {
  fastify.decorateRequest("user", null);

  fastify.addHook("preHandler", async (request, reply) => {
    const token = request.headers.authorization?.replace("Bearer ", "");
    if (!token) return; // Optional auth

    try {
      request.user = await verifyJWT(token);
    } catch {
      reply.code(401).send({ error: "Invalid token" });
    }
  });
});

// Register plugins
fastify.register(dbPlugin, { connectionString: process.env.DATABASE_URL });
fastify.register(authPlugin);

// Route-level hooks
fastify.addHook("onRequest", async (request) => {
  request.startTime = performance.now();
});

fastify.addHook("onResponse", async (request, reply) => {
  const duration = performance.now() - request.startTime;
  fastify.log.info({ duration, status: reply.statusCode }, "Request completed");
});
```

---

### 8.3 — Drizzle vs Prisma vs Kysely: ORM Comparison

#### Drizzle ORM (SQL-like, type-safe, zero overhead)

```ts
import { drizzle } from "drizzle-orm/node-postgres";
import { pgTable, serial, text, integer, timestamp, boolean } from "drizzle-orm/pg-core";
import { eq, and, gt, like, sql } from "drizzle-orm";

// Schema definition (doubles as type source)
export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  email: text("email").notNull().unique(),
  age: integer("age"),
  active: boolean("active").default(true),
  createdAt: timestamp("created_at").defaultNow(),
});

export const posts = pgTable("posts", {
  id: serial("id").primaryKey(),
  title: text("title").notNull(),
  content: text("content"),
  authorId: integer("author_id").references(() => users.id),
  publishedAt: timestamp("published_at"),
});

const db = drizzle(pool);

// Queries look like SQL but are fully type-safe
const activeUsers = await db
  .select()
  .from(users)
  .where(and(eq(users.active, true), gt(users.age, 18)));
// Type: { id: number, name: string, email: string, age: number | null, ... }[]

// Joins
const usersWithPosts = await db
  .select({
    userName: users.name,
    postTitle: posts.title,
    publishedAt: posts.publishedAt,
  })
  .from(users)
  .leftJoin(posts, eq(users.id, posts.authorId))
  .where(like(users.name, "%Bill%"));

// Insert
const [newUser] = await db
  .insert(users)
  .values({ name: "Alice", email: "alice@example.com", age: 28 })
  .returning();

// Raw SQL escape hatch (still type-safe)
const result = await db.execute(
  sql`SELECT * FROM users WHERE age > ${minAge} LIMIT ${limit}`
);
```

#### Prisma (Schema-first, great DX, heavier runtime)

```ts
// prisma/schema.prisma
// model User {
//   id        Int      @id @default(autoincrement())
//   name      String
//   email     String   @unique
//   age       Int?
//   active    Boolean  @default(true)
//   posts     Post[]
//   createdAt DateTime @default(now())
// }

import { PrismaClient } from "@prisma/client";
const prisma = new PrismaClient();

// Prisma's query API (more abstracted from SQL)
const activeUsers = await prisma.user.findMany({
  where: { active: true, age: { gt: 18 } },
  include: { posts: { where: { publishedAt: { not: null } } } },
  orderBy: { createdAt: "desc" },
  take: 20,
});
// Type includes nested posts!

// Transactions
const [user, post] = await prisma.$transaction([
  prisma.user.create({ data: { name: "Bob", email: "bob@example.com" } }),
  prisma.post.create({ data: { title: "Hello", authorId: 1 } }),
]);
```

#### Kysely (Query builder, zero abstraction, maximum control)

```ts
import { Kysely, PostgresDialect } from "kysely";

interface Database {
  users: { id: number; name: string; email: string; age: number | null };
  posts: { id: number; title: string; author_id: number };
}

const db = new Kysely<Database>({ dialect: new PostgresDialect({ pool }) });

// Pure SQL query builder (no ORM magic)
const users = await db
  .selectFrom("users")
  .select(["id", "name", "email"])
  .where("age", ">", 18)
  .where("name", "like", "%Bill%")
  .orderBy("name", "asc")
  .limit(20)
  .execute();

// Complex queries are natural
const stats = await db
  .selectFrom("users")
  .innerJoin("posts", "posts.author_id", "users.id")
  .select([
    "users.name",
    db.fn.count("posts.id").as("post_count"),
  ])
  .groupBy("users.name")
  .having(db.fn.count("posts.id"), ">", 5)
  .execute();
```

#### Comparison Matrix

| Feature | Drizzle | Prisma | Kysely |
|---------|---------|--------|--------|
| **Approach** | SQL-like ORM | Schema-first ORM | Query builder |
| **Bundle size** | ~50KB | ~2MB (engine) | ~30KB |
| **Cold start** | Fast | Slow (engine init) | Fast |
| **Type safety** | Excellent | Excellent | Excellent |
| **Raw SQL** | Easy escape hatch | `$queryRaw` | Native |
| **Migrations** | Built-in (push/generate) | Built-in (migrate) | Separate tool |
| **Relations** | Manual joins | Automatic includes | Manual joins |
| **Learning curve** | Low (know SQL = know Drizzle) | Medium | Low |
| **Serverless** | ✅ Great | ⚠️ Cold start issues | ✅ Great |
| **Edge runtime** | ✅ | ❌ (needs engine) | ✅ |
| **Best for** | Performance-critical, serverless | Rapid prototyping, complex relations | SQL experts, maximum control |

---

### 8.4 — Serverless Cold-Start Mitigation

```ts
// Problem: First request to a serverless function is slow
// Lambda cold start: 100ms-2s depending on runtime + bundle size
// Causes: container init, runtime boot, code download, module loading

// Strategy 1: Minimize bundle size
// Use esbuild/tsup to bundle + tree-shake
// Target: < 5MB zipped for fast download from S3

// Strategy 2: Lazy initialization
let dbPool; // Module-level (persists across warm invocations)

export async function handler(event) {
  // Initialize on first call, reuse on subsequent calls
  if (!dbPool) {
    dbPool = new Pool({ connectionString: process.env.DATABASE_URL });
  }

  const result = await dbPool.query("SELECT 1");
  return { statusCode: 200, body: JSON.stringify(result.rows) };
}

// Strategy 3: Provisioned concurrency (AWS Lambda)
// Keep N instances warm at all times
// Cost: ~$15/month per provisioned instance

// Strategy 4: Use lighter runtimes
// Node.js cold start: ~300ms
// Bun cold start: ~50ms (if supported)
// Rust/Go cold start: ~10ms

// Strategy 5: Edge functions (Cloudflare Workers, Vercel Edge)
// V8 isolates instead of containers
// Cold start: ~5ms (no container, no OS boot)
// Limitation: no Node.js APIs, limited execution time

// Hono on Cloudflare Workers (near-zero cold start)
import { Hono } from "hono";

const app = new Hono();

app.get("/api/users", async (c) => {
  // D1 (Cloudflare's edge SQLite) — no connection overhead
  const { results } = await c.env.DB.prepare(
    "SELECT * FROM users WHERE active = 1 LIMIT 20"
  ).all();

  return c.json(results);
});

export default app;
```

```yaml
# wrangler.toml — Cloudflare Workers config
name = "my-api"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[vars]
ENVIRONMENT = "production"

[d1_databases](d1_databases)
binding = "DB"
database_name = "my-app-db"
database_id = "xxxx-xxxx-xxxx"

[kv_namespaces](kv_namespaces)
binding = "CACHE"
id = "xxxx"
```

---

### 8.5 — Streaming Responses & Server-Sent Events

```ts
// Hono — Server-Sent Events (SSE)
import { Hono } from "hono";
import { streamSSE } from "hono/streaming";

const app = new Hono();

app.get("/api/events", (c) => {
  return streamSSE(c, async (stream) => {
    let id = 0;

    while (true) {
      const data = await getLatestData();

      await stream.writeSSE({
        data: JSON.stringify(data),
        event: "update",
        id: String(id++),
      });

      await stream.sleep(1000); // Send every second
    }
  });
});

// Fastify — Streaming NDJSON response
fastify.get("/api/export", async (request, reply) => {
  reply.raw.writeHead(200, {
    "Content-Type": "application/x-ndjson",
    "Transfer-Encoding": "chunked",
  });

  const cursor = db.collection("users").find().cursor();

  for await (const doc of cursor) {
    reply.raw.write(JSON.stringify(doc) + "\n");
  }

  reply.raw.end();
});

// Node.js native — ReadableStream response
import { Readable } from "node:stream";

app.get("/api/stream", (req, res) => {
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");

  const stream = new Readable({
    read() {},
  });

  stream.pipe(res);

  // Push data periodically
  const interval = setInterval(() => {
    const data = JSON.stringify({ time: Date.now(), value: Math.random() });
    stream.push(`data: ${data}\n\n`);
  }, 100);

  // Cleanup on disconnect
  req.on("close", () => {
    clearInterval(interval);
    stream.destroy();
  });
});
```




---

## 📎 9. Appendix: Extended Derivations & Special Cases

### 9.1 — HTTP/3 + QUIC for Node.js

HTTP/3 uses QUIC (UDP-based) instead of TCP, eliminating head-of-line blocking and reducing connection setup time.

```
┌─────────────────────────────────────────────────────────────────┐
│                    HTTP VERSION COMPARISON                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  HTTP/1.1 (TCP)                                                 │
│  ─────────────                                                   │
│  • 1 request per TCP connection (or pipelining, rarely used)    │
│  • Head-of-line blocking: slow response blocks all after it     │
│  • Workaround: open 6 parallel connections per domain           │
│  • Connection setup: TCP handshake (1 RTT) + TLS (1-2 RTT)     │
│  • Total: 2-3 RTT before first byte                            │
│                                                                  │
│  HTTP/2 (TCP, multiplexed)                                      │
│  ─────────────────────────                                       │
│  • Multiple streams over 1 TCP connection                       │
│  • Binary framing (more efficient than text)                    │
│  • Header compression (HPACK)                                   │
│  • Server push (deprecated in most browsers)                    │
│  • BUT: TCP-level head-of-line blocking still exists!           │
│    (1 lost packet blocks ALL streams until retransmitted)       │
│  • Connection setup: still TCP + TLS = 2-3 RTT                 │
│                                                                  │
│  HTTP/3 (QUIC / UDP)                                            │
│  ────────────────────                                            │
│  • QUIC = UDP + built-in TLS 1.3 + multiplexing                │
│  • NO head-of-line blocking (streams are independent)           │
│  • Lost packet only affects its own stream                      │
│  • 0-RTT connection resumption (for repeat visitors)            │
│  • 1-RTT for new connections (TLS built into QUIC handshake)   │
│  • Connection migration (switch WiFi→cellular without drop)     │
│  • Better for lossy networks (mobile, satellite)                │
│                                                                  │
│  Latency comparison (new connection):                           │
│  HTTP/1.1: 3 RTT (TCP + TLS + request)                         │
│  HTTP/2:   2 RTT (TCP + TLS combined + request)                │
│  HTTP/3:   1 RTT (QUIC handshake includes TLS + request)       │
│  HTTP/3 (0-RTT): 0 RTT (resumed connection, immediate data)    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### Node.js HTTP/3 Support

```ts
// Node.js has experimental QUIC/HTTP3 support (--experimental-quic)
// For production, use a reverse proxy (Caddy, nginx with quic, Cloudflare)

// Caddy — automatic HTTP/3 with zero config
// Caddyfile:
// myapi.com {
//   reverse_proxy localhost:3000
// }
// Caddy automatically enables HTTP/3, manages TLS certs, etc.

// For direct Node.js HTTP/3 (experimental):
import { createQuicSocket } from "node:net";

// More practical: use HTTP/2 in Node.js (stable, well-supported)
import { createSecureServer } from "node:http2";
import { readFileSync } from "node:fs";

const server = createSecureServer({
  key: readFileSync("server.key"),
  cert: readFileSync("server.crt"),
  allowHTTP1: true, // Fallback for clients that don't support H2
});

server.on("stream", (stream, headers) => {
  const path = headers[":path"];
  const method = headers[":method"];

  // HTTP/2 server push (send resources before client requests them)
  if (path === "/index.html") {
    // Push CSS before client parses HTML and discovers it needs CSS
    const pushStream = stream.pushStream({ ":path": "/styles.css" }, (err, push) => {
      if (err) return;
      push.respond({ ":status": 200, "content-type": "text/css" });
      push.end(readFileSync("./public/styles.css"));
    });
  }

  stream.respond({ ":status": 200, "content-type": "text/html" });
  stream.end(readFileSync("./public/index.html"));
});

server.listen(443);
```

---

### 9.2 — uWebSockets.js vs Node's http Module: Benchmark Deep Dive

uWebSockets.js is a C++ HTTP/WebSocket server with Node.js bindings. It's the fastest HTTP server available in the Node.js ecosystem.

#### Architecture Comparison

```
Node.js http module:
  JavaScript → libuv (C) → OS kernel
  Event loop: libuv's epoll/kqueue wrapper
  Parsing: llhttp (C, but called from JS via bindings)
  Allocation: V8's garbage-collected heap

uWebSockets.js:
  C++ (uSockets) → OS kernel directly
  Event loop: custom epoll/kqueue (no libuv overhead)
  Parsing: custom HTTP parser (C++)
  Allocation: manual memory management (no GC pressure)
  Node.js: thin binding layer only for JS callback dispatch

Bun's HTTP server:
  Zig → OS kernel (io_uring on Linux)
  Event loop: custom (no libuv)
  Parsing: custom (Zig)
  Allocation: manual + arena allocators
```

#### Benchmark Results

```bash
# Test: Simple JSON response, 100 concurrent connections, 10 seconds
# Hardware: AMD Ryzen 9 5900X, 32GB RAM, Linux 6.1

# Node.js http module
# wrk -t4 -c100 -d10s http://localhost:3000
#   Requests/sec: 82,000
#   Latency avg: 1.2ms
#   Memory: ~80MB RSS

# Fastify (Node.js)
#   Requests/sec: 65,000
#   Latency avg: 1.5ms
#   Memory: ~90MB RSS

# Hono on Node.js
#   Requests/sec: 70,000
#   Latency avg: 1.4ms
#   Memory: ~85MB RSS

# uWebSockets.js
#   Requests/sec: 450,000
#   Latency avg: 0.2ms
#   Memory: ~20MB RSS

# Bun.serve()
#   Requests/sec: 180,000
#   Latency avg: 0.5ms
#   Memory: ~30MB RSS

# Hono on Bun
#   Requests/sec: 160,000
#   Latency avg: 0.6ms
#   Memory: ~35MB RSS

# Deno.serve()
#   Requests/sec: 120,000
#   Latency avg: 0.8ms
#   Memory: ~45MB RSS
```

#### uWebSockets.js Usage

```ts
import uWS from "uWebSockets.js";

const app = uWS.App();

app.get("/api/users", (res, req) => {
  // IMPORTANT: res is NOT a Node.js response object!
  // It's a raw C++ binding — different API
  res.writeHeader("Content-Type", "application/json");
  res.end(JSON.stringify({ users: [] }));
});

// WebSocket with uWS (handles millions of connections)
app.ws("/ws", {
  compression: uWS.SHARED_COMPRESSOR,
  maxPayloadLength: 16 * 1024,
  idleTimeout: 120,

  open: (ws) => {
    ws.subscribe("broadcast");
    console.log("Client connected");
  },

  message: (ws, message, isBinary) => {
    // Echo to all subscribers
    ws.publish("broadcast", message, isBinary);
  },

  close: (ws, code, message) => {
    console.log("Client disconnected");
  },
});

app.listen(3000, (token) => {
  if (token) console.log("Listening on port 3000");
});

// When to use uWebSockets.js:
// ✅ Real-time apps with 100K+ concurrent WebSocket connections
// ✅ High-throughput APIs (>100K req/s needed)
// ✅ Low-latency requirements (sub-millisecond)
// ❌ Standard CRUD APIs (Fastify/Hono are fast enough, better DX)
// ❌ When you need Express/Fastify middleware ecosystem
// ❌ When developer experience matters more than raw speed
```

---

### 9.3 — Database Connection Pooling Strategies

```ts
// Connection pooling is CRITICAL for serverless and high-throughput servers

// Problem without pooling:
// Each request: connect (50ms) → query (5ms) → disconnect
// With 1000 req/s: 1000 connections opened/closed per second!
// Database max_connections exhausted → errors

// Solution: Connection pool (reuse connections)
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,              // Maximum connections in pool
  min: 5,               // Minimum idle connections
  idleTimeoutMillis: 30000,  // Close idle connections after 30s
  connectionTimeoutMillis: 5000, // Error if can't connect in 5s
  maxUses: 7500,        // Close connection after N uses (prevent leaks)
});

// Serverless-specific: external connection pooler
// PgBouncer, Supabase Pooler, Neon's serverless driver

// Neon serverless driver (HTTP-based, no persistent connections)
import { neon } from "@neondatabase/serverless";

const sql = neon(process.env.DATABASE_URL);

// Each query is a single HTTP request (no connection to manage!)
const users = await sql`SELECT * FROM users WHERE active = true`;

// Drizzle + Neon (best of both worlds)
import { drizzle } from "drizzle-orm/neon-http";
import { neon } from "@neondatabase/serverless";

const client = neon(process.env.DATABASE_URL);
const db = drizzle(client);

// Pool sizing formula:
// max_connections = (num_cores * 2) + effective_spindle_count
// For SSD: max_connections ≈ num_cores * 2 + 1
// For serverless: use external pooler (PgBouncer) with transaction mode
```

---

### 9.4 — Authentication Patterns for APIs

```ts
// JWT + Refresh Token pattern (Hono example)
import { Hono } from "hono";
import { sign, verify } from "hono/jwt";
import { setCookie, getCookie } from "hono/cookie";

const app = new Hono();

// Login: issue access token + refresh token
app.post("/auth/login", async (c) => {
  const { email, password } = await c.req.json();
  const user = await verifyCredentials(email, password);
  if (!user) return c.json({ error: "Invalid credentials" }, 401);

  // Short-lived access token (15 min)
  const accessToken = await sign(
    { sub: user.id, role: user.role, exp: Math.floor(Date.now() / 1000) + 900 },
    process.env.JWT_SECRET
  );

  // Long-lived refresh token (7 days) — stored in httpOnly cookie
  const refreshToken = await sign(
    { sub: user.id, type: "refresh", exp: Math.floor(Date.now() / 1000) + 604800 },
    process.env.REFRESH_SECRET
  );

  // Store refresh token hash in DB (for revocation)
  await db.refreshToken.create({
    data: { userId: user.id, tokenHash: hash(refreshToken), expiresAt: new Date(Date.now() + 604800000) },
  });

  setCookie(c, "refresh_token", refreshToken, {
    httpOnly: true,
    secure: true,
    sameSite: "Strict",
    maxAge: 604800,
    path: "/auth/refresh",
  });

  return c.json({ accessToken, user: { id: user.id, name: user.name, role: user.role } });
});

// Refresh: exchange refresh token for new access token
app.post("/auth/refresh", async (c) => {
  const refreshToken = getCookie(c, "refresh_token");
  if (!refreshToken) return c.json({ error: "No refresh token" }, 401);

  try {
    const payload = await verify(refreshToken, process.env.REFRESH_SECRET);

    // Check if token is revoked
    const stored = await db.refreshToken.findFirst({
      where: { userId: payload.sub, tokenHash: hash(refreshToken) },
    });
    if (!stored) return c.json({ error: "Token revoked" }, 401);

    // Issue new access token
    const accessToken = await sign(
      { sub: payload.sub, role: (await db.user.findUnique({ where: { id: payload.sub } })).role,
        exp: Math.floor(Date.now() / 1000) + 900 },
      process.env.JWT_SECRET
    );

    return c.json({ accessToken });
  } catch {
    return c.json({ error: "Invalid refresh token" }, 401);
  }
});

// Protected route middleware
async function requireAuth(c, next) {
  const authHeader = c.req.header("Authorization");
  if (!authHeader?.startsWith("Bearer ")) {
    return c.json({ error: "Missing token" }, 401);
  }

  try {
    const payload = await verify(authHeader.slice(7), process.env.JWT_SECRET);
    c.set("user", payload);
    await next();
  } catch {
    return c.json({ error: "Invalid or expired token" }, 401);
  }
}

app.get("/api/profile", requireAuth, async (c) => {
  const user = c.get("user");
  return c.json({ userId: user.sub, role: user.role });
});
```

---

### 9.5 — Graceful Shutdown & Health Checks

```ts
// Production Node.js server — proper lifecycle management
import Fastify from "fastify";

const fastify = Fastify({ logger: true });

// Health check endpoints
fastify.get("/health", async () => ({ status: "ok", uptime: process.uptime() }));

fastify.get("/ready", async () => {
  // Check all dependencies
  const checks = await Promise.allSettled([
    db.query("SELECT 1"),
    redis.ping(),
    fetch(process.env.EXTERNAL_API_URL + "/health"),
  ]);

  const allHealthy = checks.every(c => c.status === "fulfilled");
  if (!allHealthy) {
    throw { statusCode: 503, message: "Not ready" };
  }
  return { status: "ready", checks: checks.map(c => c.status) };
});

// Graceful shutdown
let isShuttingDown = false;

async function gracefulShutdown(signal) {
  if (isShuttingDown) return;
  isShuttingDown = true;

  fastify.log.info(`Received ${signal}. Starting graceful shutdown...`);

  // 1. Stop accepting new connections
  await fastify.close();

  // 2. Wait for in-flight requests to complete (with timeout)
  const shutdownTimeout = setTimeout(() => {
    fastify.log.error("Shutdown timeout — forcing exit");
    process.exit(1);
  }, 30000); // 30s max

  // 3. Close database connections
  await db.end();
  await redis.quit();

  // 4. Flush logs/metrics
  await logger.flush();

  clearTimeout(shutdownTimeout);
  fastify.log.info("Graceful shutdown complete");
  process.exit(0);
}

// Listen for termination signals
process.on("SIGTERM", () => gracefulShutdown("SIGTERM")); // Kubernetes/Docker
process.on("SIGINT", () => gracefulShutdown("SIGINT"));   // Ctrl+C

// Kubernetes readiness: return 503 during shutdown
fastify.addHook("onRequest", async (request, reply) => {
  if (isShuttingDown) {
    reply.code(503).send({ error: "Server is shutting down" });
  }
});

// Start server
await fastify.listen({ port: 3000, host: "0.0.0.0" });
```

```yaml
# Kubernetes deployment with health checks
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: api
          image: myapp:latest
          ports:
            - containerPort: 3000
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 5
          lifecycle:
            preStop:
              exec:
                command: ["sh", "-c", "sleep 5"]
          terminationGracePeriodSeconds: 30
```

---

*Last updated: 2026-05-24*
