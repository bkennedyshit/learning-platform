---
title: "19.5 — API Design"
subject: "System Design & Distributed Architecture"
catalog: advanced
audience_tier: higher-education
chapter: "19.5"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 19.5 — API Design

> *"Your API is a legal-weight contract with your consumers. Every field is a promise. Every status code is a promise. You only get to break a promise loudly, with a version bump and a deprecation calendar."*

By 2026 the API conversation is settled enough that *picking* is straightforward — REST for most things, gRPC for internal microservice calls, GraphQL Federation for cross-team graphs, AsyncAPI for events. What's hard is **contract design**: versioning, errors, idempotency, rate limits, and the gateway in front of it all.

---

## 🎯 Learning Objectives

1. Compare **REST**, **GraphQL**, **gRPC**, **tRPC**, and **AsyncAPI** by workload.
2. Author an **OpenAPI 3.1** spec from scratch with proper components, security, and examples.
3. Apply **GraphQL Federation** (Apollo Federation, WunderGraph) to compose subgraphs.
4. Use **gRPC + protobuf** with **Buf** for schema evolution + breaking-change detection.
5. Choose a **versioning strategy**: URI, header, content negotiation, or deprecation calendar.
6. Implement **rate limiting** (fixed-window, sliding-window, token bucket, leaky bucket) and **idempotency keys**.
7. Pick a **2026 API gateway**: Kong, Tyk, Apigee, Zuplo, AWS API Gateway, or build-on-Envoy.

---

## 🖼️ Visual Anchor

> *Picture / video reference (external — open in browser):*
> - 📺 [OpenAPI 3.1 specification](https://spec.openapis.org/oas/v3.1.0)
> - 📺 [WunderGraph blog — Federation, gRPC, REST decisions](https://wundergraph.com/blog/graphql-vs-federation-vs-trpc-vs-rest-vs-grpc-vs-asyncapi-vs-webhooks)
> - 📺 [Buf (gRPC tooling) docs](https://buf.build/docs/)
> - 📺 [Stripe API reference (gold-standard examples)](https://docs.stripe.com/api)

---

## 📚 1. The 2026 API Decision Matrix

> REST remains the default for ~80% of business APIs. GraphQL wins for complex frontends with multiple data needs. gRPC dominates internal microservice communication. The biggest 2026 trend is AI-powered API gateways that auto-generate documentation, handle rate limiting, and detect anomalies. — paraphrased from [optimum-web — API Development Services 2026](https://www.optimum-web.com/blog/api-development-services-2026-rest-graphql-grpc-guide). Content rephrased for compliance.

> GraphQL's main value is enabling Federation and cross-team API collaboration, not micro-optimizing payloads. Monolithic GraphQL APIs don't justify their complexity today; tRPC works for monoliths and GraphQL Federation for enterprise-scale graphs. — paraphrased from [WunderGraph — six-year GraphQL recap](https://wundergraph.com/blog/six-year-graphql-recap). Content rephrased for compliance.

| Style | Strengths | Weaknesses | Default for |
|---|---|---|---|
| **REST + JSON** | Cacheable, ubiquitous, HTTP-native, easy to debug | Chatty for nested data, weak typing | Most public APIs and 80% of business APIs |
| **GraphQL Federation** | Cross-team graphs, single endpoint, evolvable | Complexity, caching, N+1 risk | Enterprise BFF, multi-team org-wide graphs |
| **gRPC + protobuf** | Compact, fast, strongly typed, streaming | Harder to debug, browsers need gRPC-Web/Connect | Internal microservice ↔ microservice |
| **tRPC** | End-to-end typesafe TS in monorepos | TS-only, monolith-friendly | TS monorepo internal APIs |
| **AsyncAPI** | Spec for event-driven APIs (Kafka, NATS) | Tooling still maturing | Event/message contracts |
| **WebHooks** | Push from server → consumer | Hard to secure + retry correctly | Provider → subscriber events |

---

## 📚 2. REST Maturity & OpenAPI 3.1

The Richardson Maturity Model:
1. Level 0 — One URI, one verb (RPC over HTTP)
2. Level 1 — Multiple resources
3. Level 2 — Proper HTTP verbs + status codes
4. Level 3 — HATEOAS (hypermedia controls)

Level 2 is the realistic 2026 target. Level 3 is rarely worth the complexity.

**OpenAPI 3.1** is the canonical schema; it aligns with **JSON Schema 2020-12**. Generate clients (typed SDKs), mock servers, validators, and docs from one source.

```yaml
openapi: 3.1.0
info: { title: Orders API, version: 1.4.2 }
paths:
  /orders/{id}:
    get:
      operationId: getOrder
      parameters:
        - in: path
          name: id
          required: true
          schema: { type: string, format: uuid }
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Order' }
```

---

## 📚 3. GraphQL Federation

> WunderGraph compiles Subgraph SDLs to gRPC services with built-in support for data loading, eliminating N+1 problems. — paraphrased from [WunderGraph — Federation over gRPC](https://wundergraph.com/blog/graphql-federation-over-grpc). Content rephrased for compliance.

The 2026 federation pattern:
1. Each team owns a **subgraph** (e.g. `users`, `orders`, `products`).
2. A **router** (Apollo Router, WunderGraph Cosmo, GraphQL Mesh) composes them into a **supergraph**.
3. Frontend issues a single query against the supergraph; router fans out to subgraphs and assembles the response.

**Persisted queries** + **trusted documents** make GraphQL safe to expose: clients send a hash, server looks up the actual query — eliminates query-injection/cost attacks.

---

## 📚 4. gRPC + Protobuf with Buf

```proto
syntax = "proto3";
package orders.v1;

service OrderService {
  rpc GetOrder(GetOrderRequest) returns (Order);
  rpc StreamOrderEvents(StreamRequest) returns (stream OrderEvent);
}

message GetOrderRequest {
  string id = 1;
}

message Order {
  string id = 1;
  int64 cents = 2;
  reserved 3; // do not reuse
  string currency = 4;
}
```

**[Buf](https://buf.build/)** adds:
- Lint rules (style + correctness).
- **Breaking-change detection** in CI.
- Schema registry (push/pull versioned modules).
- Code gen for Go/Java/Python/TS/Swift/etc.

For browsers: **Connect** (from the Buf team) gives you HTTP/JSON + gRPC + gRPC-Web from one protobuf definition.

---

## 📚 5. Versioning Strategies

| Strategy | Example | Pros | Cons |
|---|---|---|---|
| **URI version** | `/v1/orders`, `/v2/orders` | Simple, cache-friendly | Duplication; clients must change URLs |
| **Accept header** | `Accept: application/vnd.acme.v2+json` | URLs stable | Harder to inspect / debug |
| **Query parameter** | `?api-version=2026-05-01` | Easy | Less semantic |
| **Date-based** (Stripe) | `Stripe-Version: 2026-04-30` | Per-customer pin; deprecation calendar | More server-side state |

**Stripe-style date-versioning** is the gold standard for paid public APIs: customers pin a date, get bug fixes for free, and explicitly opt in to breaking changes by bumping the date.

---

## 📚 6. Rate Limiting

| Algorithm | How |
|---|---|
| **Fixed window** | N requests per minute slot. Simple but bursty at boundaries. |
| **Sliding window log** | Store timestamps; count those within window. Accurate but memory-heavy. |
| **Sliding window counter** | Approximate sliding window with two adjacent fixed windows. |
| **Token bucket** | Refill tokens at rate R; each request consumes one. Allows bursts up to bucket size. |
| **Leaky bucket** | Smooth output rate. Good for downstream protection. |

Standard headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 73
X-RateLimit-Reset: 1716700800
Retry-After: 30
```

Plus the [draft IETF `RateLimit` headers](https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/) which standardize the above.

---

## 📚 7. API Gateways in 2026

| Gateway | Strengths |
|---|---|
| **Kong** | Largest plugin ecosystem, OSS + enterprise, Envoy-based options |
| **Tyk** | Developer-portal-first, OSS-friendly |
| **Apigee** | Google, enterprise heritage, deep analytics |
| **Zuplo** | Programmable JS/TS gateway, Cloudflare-Workers-style edge model |
| **AWS API Gateway** | Tight AWS integration; pay-per-request |
| **Envoy + custom control plane** | Build-your-own when off-the-shelf doesn't fit |

The 2026 trend is **AI-augmented gateways** that auto-classify endpoints, surface anomalies, and generate docs from observed traffic — same source as above.

---

## 🛠️ 8. Worked Example — Designing the Public Orders API

**Goal:** publish `Orders v1` to external developers with a 12-month deprecation guarantee.

**Step 1 — Pick the style.** External, browser-friendly, cache-friendly → **REST + OpenAPI 3.1**.

**Step 2 — Author OpenAPI.** Versioned at `/v1/orders`. All payloads referenced in `components/schemas`. Required examples in every operation.

**Step 3 — Idempotency keys** on `POST /v1/orders`. Server stores `(key → response)` for 24 h.

**Step 4 — Rate limit** at gateway (Kong) with token-bucket: 100 req/min per API key, 1000 req/min per org.

**Step 5 — Versioning calendar.** New version every quarter at most; old versions live 12 months past sunset announcement; deprecation visible in `Sunset` HTTP header.

**Step 6 — gRPC mirror for internal services.** Same domain types, defined in protobuf, generated alongside OpenAPI from a shared IDL.

**Step 7 — AsyncAPI for `order.events`** topic — partner integrators can subscribe via webhooks (REST) or Kafka credentials (AsyncAPI).

**Result:** one domain model, three contracts (REST/OpenAPI, gRPC/protobuf, AsyncAPI), all generated from a single source — the discipline that lets the API last a decade.

---

## 🔗 9. Cross-links & Further Reading

### Internal
- [19.4 - Message Queues & Event-Driven Architecture](19.4---Message-Queues-&-Event-Driven-Architecture) — AsyncAPI is the contract layer for those topics
- [19.6 - Microservices & Service Mesh](19.6---Microservices-&-Service-Mesh) — gRPC + mTLS via mesh
- [19.2 - Caching, CDNs & Edge](19.2---Caching,-CDNs-&-Edge) — `Cache-Control` is part of every REST API
- [Subject_Plan](Subject_Plan) — auth, mTLS, signed webhooks
- [Subject_Plan](Subject_Plan) — rolling out a versioned API

### External
- [OpenAPI 3.1 specification](https://spec.openapis.org/oas/v3.1.0)
- [AsyncAPI](https://www.asyncapi.com/)
- [Buf docs](https://buf.build/docs/)
- [Connect (Buf RPC framework)](https://connectrpc.com/)
- [WunderGraph — when to use Federation vs tRPC vs REST vs gRPC](https://wundergraph.com/blog/graphql-vs-federation-vs-trpc-vs-rest-vs-grpc-vs-asyncapi-vs-webhooks)
- [WunderGraph — Six-year GraphQL recap](https://wundergraph.com/blog/six-year-graphql-recap)
- [Stripe API reference](https://docs.stripe.com/api) — the "study this" target
- [Kong](https://konghq.com/) · [Tyk](https://tyk.io/) · [Apigee](https://cloud.google.com/apigee) · [Zuplo](https://zuplo.com/)

---

## ⚠️ 10. Common Misconceptions

- **"GraphQL replaces REST."** Not in 2026. They coexist; Federation is the GraphQL story that earns its keep.
- **"gRPC works in browsers natively."** Use **gRPC-Web** or **Connect**; raw gRPC requires HTTP/2 trailers most CDNs strip.
- **"OpenAPI is documentation."** It's a *contract*. Generate clients and validators from it; treat docs as a *side effect*.
- **"Rate limiting is per-IP."** Per-API-key + per-org, with separate quotas, is the production answer; per-IP is for unauthenticated scrapers.
- **"Versioning is optional if you communicate."** It's only optional if you don't have customers.

---

*Next: [19.6 - Microservices & Service Mesh](19.6---Microservices-&-Service-Mesh) — When (and only when) to decompose.*
