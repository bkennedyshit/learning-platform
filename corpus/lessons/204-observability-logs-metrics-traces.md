---
title: "20.4 — Observability — Logs, Metrics, Traces"
subject: "DevOps & SRE"
catalog: advanced
audience_tier: higher-education
chapter: "20.4"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 20.4 — Observability — Logs, Metrics, Traces

> *"Monitoring tells you what's wrong. Observability lets you ask why — without shipping new code."*

This chapter is the **nervous system** of the track. You can't run an SLO ([20.5 - SLOs, SLAs, Error Budgets & Incident Response](20.5---SLOs,-SLAs,-Error-Budgets-&-Incident-Response)), you can't run a chaos experiment ([20.6 - Chaos Engineering & Resilience](20.6---Chaos-Engineering-&-Resilience)), and you can't run a canary ([20.7 - Deployment Strategies](20.7---Deployment-Strategies)) without it. The 2026 reality: **OpenTelemetry graduated from CNCF in May 2026** and is now the de-facto vendor-neutral standard for traces, metrics, and logs — with new GenAI semantic conventions that make LLM and agent calls first-class spans.

---

## 🎯 Learning Objectives

1. Distinguish the three pillars: **logs**, **metrics**, **traces** — and the fourth, **events / continuous profiling**.
2. Instrument a service with **OpenTelemetry** (auto and manual) and export to a Collector.
3. Run **Prometheus** + **Grafana** for metrics, **Loki** for logs, **Tempo** for traces — the all-Grafana OSS stack.
4. Read PromQL and write a recording rule.
5. Apply **structured logging** consistently with trace correlation.
6. Define the **Four Golden Signals** (latency, traffic, errors, saturation) and the **RED** / **USE** methods.
7. Apply the new **OpenTelemetry GenAI semantic conventions** to trace LLM calls, tool calls, and agent reasoning steps.

---

## 🖼️ Visual Anchor

![dev-20__fig3](dev-20__fig3.svg)

> *Picture / video reference (external):*
> - 📺 [opentelemetry.io — GenAI Observability blog](https://opentelemetry.io/blog/2026/genai-observability/)
> - 📺 [CNCF — OpenTelemetry graduation announcement](https://www.cncf.io/announcements/2026/05/21/cloud-native-computing-foundation-announces-opentelemetrys-graduation-solidifying-status-as-the-de-facto-observability-standard/)
> - 📺 [Grafana Labs — OSS stack overview](https://grafana.com/oss/)
> - 📺 [Anton Putra — Mastering Monitoring](https://www.youtube.com/@AntonPutra)
> - 📺 [Honeycomb — o11ycast](https://www.honeycomb.io/blog/category/o11ycast)

---

## 📚 1. The Three Pillars (and the Fourth)

### Definition 20.4.1 — Logs
Discrete, time-stamped, often unstructured (or semi-structured) text emitted by an application. **Always make them structured** (JSON / logfmt) with at minimum: timestamp, level, message, trace_id, span_id, service.

### Definition 20.4.2 — Metrics
Numerical measurements aggregated over time, with labels. Core types: **counter** (monotonic), **gauge** (point-in-time), **histogram** (distribution), **summary** (quantiles).

### Definition 20.4.3 — Traces
A trace is a tree of **spans**, each span representing one unit of work (HTTP handler, DB query, RPC call). Spans have a `trace_id`, `span_id`, `parent_span_id`, start/end timestamps, and attributes.

### The fourth pillar
**Continuous profiling** (Pyroscope, Parca, Polar Signals) — flame graphs sampled in production, attributable per service/version. Increasingly first-class in 2026.

---

## 🌐 2. OpenTelemetry — The CNCF Graduated Standard

OpenTelemetry was accepted into CNCF in May 2019 and reached **Graduated** maturity in May 2026 — only the second project to reach graduation by spec/implementation breadth across signals. (paraphrased from [cncf.io — OpenTelemetry project page](https://www.cncf.io/projects/opentelemetry/) and [cncf.io — OpenTelemetry graduation](https://www.cncf.io/announcements/2026/05/21/cloud-native-computing-foundation-announces-opentelemetrys-graduation-solidifying-status-as-the-de-facto-observability-standard/), rephrased for compliance)

What it gives you:
- **SDKs** for ~14 languages (Python, JS/TS, Go, Java, .NET, Ruby, Rust, etc.)
- **Auto-instrumentation** for popular frameworks (FastAPI, Express, Spring, Django, Flask, ASP.NET)
- **Collector** — a vendor-neutral agent that receives OTLP and exports to any backend (Jaeger, Tempo, Honeycomb, Datadog, New Relic, SigNoz, Better Stack)
- **Semantic conventions** — agreed attribute names so dashboards portable across vendors

### Minimal Python instrumentation

```python
# pyproject.toml deps: opentelemetry-distro, opentelemetry-exporter-otlp
# .env: OTEL_SERVICE_NAME=orders-api OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
import opentelemetry.instrumentation.auto_instrumentation  # noqa: F401  (imported for side-effects)

from fastapi import FastAPI
from opentelemetry import trace
tracer = trace.get_tracer(__name__)

app = FastAPI()

@app.post("/orders")
async def create_order(payload: dict):
    with tracer.start_as_current_span("validate-order", attributes={"order.user_id": payload["user_id"]}):
        ...
    with tracer.start_as_current_span("persist-order"):
        ...
    return {"ok": True}
```

Run with `opentelemetry-instrument uvicorn app:app` and FastAPI, requests, SQLAlchemy, and Redis are auto-instrumented.

---

## 🤖 3. GenAI Observability — The 2026 Frontier

OpenTelemetry's **GenAI semantic conventions** turn LLM calls into proper traces. Each LLM invocation becomes a span with attributes for the model name, prompt/response (or hashes), token counts, finish reason, and cost. For agentic systems, each tool call, retrieval step, and LLM call becomes a child span — yielding a full trace of the reasoning chain. (paraphrased from [uptrace.dev — OpenTelemetry for AI Systems 2026](http://uptrace.dev/blog/opentelemetry-ai-systems), [greptime — OTel GenAI semantic conventions](https://greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions), and [opentelemetry.io — GenAI Observability](https://opentelemetry.io/blog/2026/genai-observability/), rephrased for compliance)

Why this matters: a slow LLM endpoint, a retrieval that returned the wrong chunks, or a tool that loops are all now visible in the same trace UI as your HTTP handler. See [10.5 - Transformer Architectures & LLMs](10.5---Transformer-Architectures-&-LLMs) for the model side.

---

## 🔥 4. Prometheus + Grafana + Loki + Tempo

The all-Grafana-OSS stack:
- **Prometheus** — pull-based metrics with PromQL.
- **Loki** — log aggregator that uses Prometheus-style label indexing (cheap; queries are filter-then-text-search, not full-text inverted index).
- **Tempo** — trace backend; integrates with Grafana for trace search and span links.
- **Mimir** — long-term, horizontally-scalable Prometheus storage.
- **Grafana** — the dashboards + alerts UI.

### A useful PromQL query

```promql
# 95th percentile request latency for the orders-api over the last 5m
histogram_quantile(0.95,
  sum(rate(http_server_duration_seconds_bucket{service="orders-api"}[5m]))
  by (le, route))
```

### Recording rule (precomputed, used for SLOs)

```yaml
groups:
- name: orders-api.recording
  interval: 30s
  rules:
  - record: orders_api:availability:ratio_rate5m
    expr: |
      sum(rate(http_server_requests_total{service="orders-api", status!~"5.."}[5m]))
      /
      sum(rate(http_server_requests_total{service="orders-api"}[5m]))
```

That recording rule becomes the SLI for an availability SLO in [20.5 - SLOs, SLAs, Error Budgets & Incident Response](20.5---SLOs,-SLAs,-Error-Budgets-&-Incident-Response).

---

## 🟡 5. The Four Golden Signals + RED + USE

From the SRE Book:

| Signal | What you measure |
|---|---|
| **Latency** | Distribution of request times (p50, p95, p99) |
| **Traffic** | Request rate / QPS |
| **Errors** | Rate or ratio of failed requests |
| **Saturation** | How "full" the service is (CPU, memory, queue depth) |

**RED** (Tom Wilkie) is a service-centric subset: **R**ate, **E**rrors, **D**uration. **USE** (Brendan Gregg) is a resource-centric counterpart: **U**tilization, **S**aturation, **E**rrors. Use RED for services, USE for hosts/queues/disks.

(paraphrased from the [Google SRE Book — Monitoring Distributed Systems chapter](https://sre.google/sre-book/monitoring-distributed-systems/), rephrased for compliance)

---

## 📝 6. Structured Logging Discipline

Bad:
```
2026-05-26 14:02:11 INFO Order created for user 42
```

Good:
```json
{"ts":"2026-05-26T14:02:11Z","level":"info","msg":"order created","user_id":42,"order_id":"abc","trace_id":"3f...","span_id":"a1..."}
```

Three rules:
1. **Always JSON** in production (or logfmt). Loki / Datadog / Splunk treat structured fields as labels.
2. **Always include `trace_id` + `span_id`** so a log line links to its trace.
3. **Don't log secrets.** Never log full prompts/responses if they contain user PII; hash or redact.

---

## 🛠️ 7. Worked Example — End-to-End Trace of an LLM-backed Endpoint

A FastAPI endpoint calls a vector DB, then an LLM via the OpenAI SDK. After OTel auto-instrumentation + GenAI semantic conventions, the trace tree looks like:

```
POST /chat                                          [400 ms]
├─ vector-db.query "embed_then_search"              [ 60 ms]
│  └─ http POST /embed                              [ 18 ms]
├─ gen_ai.chat "gpt-4o"                             [310 ms]
│  ├─ gen_ai.tool_call "lookup_account"             [ 22 ms]
│  └─ gen_ai.tool_call "fetch_invoices"             [ 70 ms]
└─ db.query "SELECT * FROM messages …"              [ 12 ms]
```

In Grafana Tempo (or Honeycomb / SigNoz / Uptrace) you can click any span, see its attributes (model name, prompt token count, retrieval k), and pivot to the correlated logs (Loki) and metrics (Prometheus) for the same `trace_id`. That's observability — *ask why without shipping new code*.

---

## 🔗 8. Cross-links & Further Reading

### Internal
- [20.5 - SLOs, SLAs, Error Budgets & Incident Response](20.5---SLOs,-SLAs,-Error-Budgets-&-Incident-Response) — what you build *with* metrics
- [20.6 - Chaos Engineering & Resilience](20.6---Chaos-Engineering-&-Resilience) — what you observe *during* a fault injection
- [20.7 - Deployment Strategies](20.7---Deployment-Strategies) — canary analysis reads from here
- [20.8 - Cost & Capacity Engineering - FinOps](20.8---Cost-&-Capacity-Engineering---FinOps) — observability has its own cost curve
- [10.5 - Transformer Architectures & LLMs](10.5---Transformer-Architectures-&-LLMs) — the LLM side of GenAI observability

### External
- [OpenTelemetry docs](https://opentelemetry.io/docs/)
- [OpenTelemetry GenAI Observability blog](https://opentelemetry.io/blog/2026/genai-observability/)
- [Prometheus docs](https://prometheus.io/docs/) · [PromQL primer](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Grafana Loki](https://grafana.com/oss/loki/) · [Tempo](https://grafana.com/oss/tempo/) · [Mimir](https://grafana.com/oss/mimir/)
- [SigNoz](https://signoz.io/) · [Sentry](https://sentry.io/) · [Honeycomb](https://www.honeycomb.io/)
- [Better Stack](https://betterstack.com/) · [Uptrace](https://uptrace.dev/)
- [Pyroscope](https://pyroscope.io/) · [Parca](https://www.parca.dev/) (continuous profiling)
- [Greptime — OTel GenAI semantic conventions](https://greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions)
- [Future AGI — What is LLM Observability? 2026 Stack Guide](https://futureagi.com/blog/what-is-llm-observability/)

---

## ⚠️ 9. Common Misconceptions

- **"Logs are enough."** Logs don't aggregate efficiently and can't answer "is the p95 worse than yesterday." Use all three pillars.
- **"More cardinality is better."** High-cardinality labels (user_id, request_id) blow up Prometheus memory. Use traces + exemplars for that, not labels.
- **"Sampling traces loses information."** Tail-based sampling (keep all error or slow traces) keeps the value while cutting cost ~99%.
- **"Auto-instrumentation is enough."** It captures HTTP/DB/RPC edges, but business-meaningful spans ("validate order", "score fraud") require manual instrumentation.
- **"Datadog/Splunk lock me out of OTel."** Both ingest OTLP today. Sending OTel through a Collector means you can swap backends without changing app code.
- **"OpenTelemetry's GenAI conventions are immature."** They graduated alongside the project and are already implemented by major LLM SDKs and observability vendors. (paraphrased from [opentelemetry.io — GenAI Observability](https://opentelemetry.io/blog/2026/genai-observability/), rephrased for compliance)

---

*Next: [20.5 - SLOs, SLAs, Error Budgets & Incident Response](20.5---SLOs,-SLAs,-Error-Budgets-&-Incident-Response) — Where these signals become a contract.*
