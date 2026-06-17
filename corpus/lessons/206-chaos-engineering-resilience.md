---
title: "20.6 — Chaos Engineering & Resilience"
subject: "DevOps & SRE"
catalog: advanced
audience_tier: higher-education
chapter: "20.6"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 20.6 — Chaos Engineering & Resilience

> *"Chaos engineering is not breaking things. It's discovering what's already broken — before your customers do."*

This chapter is the **stress test**. With an SLO ([20.5 - SLOs, SLAs, Error Budgets & Incident Response](20.5---SLOs,-SLAs,-Error-Budgets-&-Incident-Response)) and observability ([20.4 - Observability - Logs, Metrics, Traces](20.4---Observability---Logs,-Metrics,-Traces)) in place, you can now do the most counter-intuitively useful thing in production engineering: deliberately inject failure to verify that your system survives it.

---

## 🎯 Learning Objectives

1. State the **chaos engineering loop**: define steady state → form a hypothesis → choose blast radius → inject the fault → revert → analyze.
2. Pick a tool — **LitmusChaos** (CNCF), **Chaos Mesh** (CNCF), **Gremlin** (commercial), **AWS Fault Injection Service** — and know when each fits.
3. Run a **game day**: a scheduled, scoped, witnessed failure injection.
4. Apply the resilience patterns: **timeouts**, **retries with jitter**, **circuit breakers**, **bulkheads**, **load shedding**, **graceful degradation**.
5. Distinguish **chaos engineering** from **load testing** ([20.7 - Deployment Strategies](20.7---Deployment-Strategies) uses both for canary analysis).

---

## 🖼️ Visual Anchor

> *Picture / video reference (external):*
> - 📺 [LitmusChaos docs](https://docs.litmuschaos.io/)
> - 📺 [Gremlin — What is fault injection?](https://www.gremlin.com/blog/what-is-fault-injection)
> - 📺 [bitslovers — AWS Fault Injection Simulator](https://www.bitslovers.com/aws-fault-injection-simulator-chaos-engineering/)
> - 📺 [AWS — Well-Architected REL12-BP04 Test resiliency using chaos engineering](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_testing_resiliency_failure_injection_resiliency.html)

---

## 📚 1. The Loop

The canonical chaos-engineering experiment, paraphrased from the [Principles of Chaos Engineering](https://principlesofchaos.org/) and the [Gremlin learning material on fault injection](https://www.gremlin.com/blog/what-is-fault-injection) (rephrased for compliance):

1. **Define steady state.** What does "normal" look like in metrics — error rate, p95, queue depth, throughput?
2. **Form a hypothesis.** "If we drop 50% of packets to the cache for 60 seconds, error rate stays under 0.5%."
3. **Choose blast radius.** Smallest possible scope that lets you test the hypothesis. One pod, one AZ, one tenant, off-peak.
4. **Inject the fault** — and have the **revert button** ready before you start.
5. **Watch the metrics.** Does steady state hold?
6. **Revert** the experiment.
7. **Analyze.** Hypothesis confirmed? Surprise? File action items.

If your hypothesis fails, congratulations — you found a bug *before* a customer did.

---

## 🛠️ 2. Tooling Comparison

| Tool | Where it runs | Best for | License |
|---|---|---|---|
| **LitmusChaos** | Kubernetes-native, ChaosHub of experiments | OSS Kubernetes chaos at scale | Apache 2.0 (CNCF) |
| **Chaos Mesh** | Kubernetes-native | Lower-level fault primitives, PingCAP-incubated | Apache 2.0 (CNCF) |
| **Gremlin** | Cloud SaaS, agent-on-host | Commercial, mature, multi-platform | Commercial |
| **AWS Fault Injection Service (FIS)** | AWS console / API | Cloud-resource faults (EC2 stop, EBS pause, RDS failover) | AWS service |
| **Steadybit** | SaaS + agents | Modern, Reliability Hub | Commercial |
| **Chaos Toolkit** | CLI + Python | Generic, scriptable, vendor-agnostic | Apache 2.0 |

The chaos-engineering steady-state-then-fault loop is the same approach most platforms use: define normal, hypothesize the system stays normal under fault, inject in a controlled and reversible way, and analyze. (paraphrased from [bitslovers — AWS Fault Injection Simulator](https://www.bitslovers.com/aws-fault-injection-simulator-chaos-engineering/), rephrased for compliance)

---

## ☸️ 3. LitmusChaos — A Worked Pod Kill

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata: { name: orders-pod-kill, namespace: orders }
spec:
  appinfo:
    appns: orders
    applabel: "app=orders-api"
    appkind: deployment
  chaosServiceAccount: litmus-admin
  experiments:
  - name: pod-delete
    spec:
      components:
        env:
        - name: TOTAL_CHAOS_DURATION
          value: "60"
        - name: CHAOS_INTERVAL
          value: "10"
        - name: FORCE
          value: "false"
        - name: PODS_AFFECTED_PERCENTAGE
          value: "20"
```

This kills 20% of `orders-api` pods at 10-second intervals over 60 seconds. The "probes" feature lets Litmus watch your SLI and abort if it dips below threshold. Always pair with an upstream load generator ([k6](https://k6.io/), [Locust](https://locust.io/)) so you can actually measure user-perceptible impact.

---

## 🌐 4. AWS Fault Injection Service (FIS)

For non-Kubernetes / cloud-resource chaos. FIS is AWS's managed chaos service, integrated with IAM, CloudWatch alarms, and SSM. Action types include `aws:ec2:stop-instances`, `aws:rds:reboot-db-instances`, `aws:network:disrupt-connectivity`, and Lambda fault injection. (paraphrased from [reintech — AWS FIS vs Gremlin](https://reintech.io/blog/aws-fault-injection-service-vs-gremlin-comparison) and [aws — FIS network resilience for Fargate](https://aws.amazon.com/blogs/containers/testing-network-resilience-of-aws-fargate-workloads-on-amazon-ecs-using-aws-fault-injection-service/), rephrased for compliance)

A typical FIS experiment template stops a fraction of EC2 instances for N minutes, with a CloudWatch alarm as a stop condition — the experiment auto-aborts if the alarm fires.

---

## 🎮 5. Game Days

A **game day** is a scheduled, witnessed, scoped chaos experiment, run as a team exercise. Format:

| Step | Detail |
|---|---|
| 1. Pre-brief | Hypothesis + blast radius + revert plan + comms plan, on a shared doc |
| 2. Roles | IC, ops lead, scribe, observers (see [20.5 - SLOs, SLAs, Error Budgets & Incident Response](20.5---SLOs,-SLAs,-Error-Budgets-&-Incident-Response)) |
| 3. Inject | Tool of choice; one fault at a time |
| 4. Observe | Watch dashboards; everyone sees the same screen |
| 5. Revert | First, always |
| 6. Debrief | Hypothesis result, surprises, action items, on the same doc |

Most teams *never* run chaos engineering — the gap from Netflix to your team isn't tooling complexity, it's organisational permission to deliberately break things and learn from it. (paraphrased from [webcoderspeed — Chaos Engineering in Practice](https://webcoderspeed.com/blog/scaling/chaos-engineering-practice), rephrased for compliance)

---

## 🛡️ 6. Resilience Patterns Worth Knowing

| Pattern | Idea | Library example |
|---|---|---|
| **Timeout** | Cap how long we wait | Every HTTP client — set it explicitly |
| **Retry with exponential backoff + jitter** | Don't synchronize retries | tenacity (Python), resilience4j (Java) |
| **Circuit breaker** | Open the circuit after N failures, fall back; half-open to probe | resilience4j, Polly (.NET), gobreaker |
| **Bulkhead** | Isolate resource pools so one slow dep doesn't drown others | Separate thread pools / connection pools per dependency |
| **Load shedding** | Drop low-priority work under overload | Adaptive concurrency limits (Netflix concurrency-limits) |
| **Graceful degradation** | Serve stale cache / reduced feature when dep is down | Application-level fallback paths |
| **Hedged requests** | Send a duplicate after p95, take the first to return | Common in low-latency systems |

These are specific patterns; chaos engineering verifies they actually work under fire.

---

## 🛠️ 7. Worked Example — A First Game Day

**Hypothesis:** "If the primary Redis cache becomes 50% packet-lossy for 5 minutes, error rate on `orders-api` stays under 1% (well within our 99.9% SLO)."

**Blast radius:** Single staging-prod-like cluster, off-peak Saturday morning.

**Steady state:** error rate < 0.1%, p95 < 250 ms, sustained 200 RPS from k6.

**Tools:** Litmus `network-chaos` experiment for packet loss + k6 generating load + Grafana for the panel everyone watches.

**Revert button:** Litmus auto-aborts at 6 minutes; manual abort if p95 > 1.5 s for 60 s straight.

**Result outcomes you might see:**
- ✅ Circuit breaker opens; cache calls fall back to DB; error rate stays low. *Hypothesis confirmed.*
- ❌ Retry storm; DB saturates; error rate spikes to 12%. *Action item: cap retries + bulkhead the cache pool.*

Either way, you learned something *before* it happened in production.

---

## 🔗 8. Cross-links & Further Reading

### Internal
- [20.5 - SLOs, SLAs, Error Budgets & Incident Response](20.5---SLOs,-SLAs,-Error-Budgets-&-Incident-Response) — the SLI you read during the experiment
- [20.4 - Observability - Logs, Metrics, Traces](20.4---Observability---Logs,-Metrics,-Traces) — the dashboards you watch
- [20.7 - Deployment Strategies](20.7---Deployment-Strategies) — canary analysis is mini-chaos on a single deploy
- [Subject_Plan](Subject_Plan) — circuit breakers, bulkheads, etc.

### External
- [Principles of Chaos Engineering](https://principlesofchaos.org/)
- [LitmusChaos docs](https://docs.litmuschaos.io/) · [Chaos Mesh docs](https://chaos-mesh.org/docs/)
- [Gremlin — fault injection](https://www.gremlin.com/blog/what-is-fault-injection) · [Gremlin — Getting started with Chaos Engineering on AWS](https://www.gremlin.com/aws)
- [AWS Fault Injection Service](https://aws.amazon.com/fis/) · [AWS — DORA scenario testing with FIS](https://aws.amazon.com/blogs/industries/dora-scenario-testing-with-aws-fault-injection-service)
- [bitslovers — AWS FIS chaos engineering](https://www.bitslovers.com/aws-fault-injection-simulator-chaos-engineering/)
- [Steadybit](https://www.steadybit.com/) · [Chaos Toolkit](https://chaostoolkit.org/)
- [Netflix — Simian Army (historical)](https://github.com/Netflix/SimianArmy)

---

## ⚠️ 9. Common Misconceptions

- **"Chaos engineering is for huge companies."** The smaller you are, the cheaper a single failure mode is to fix. Start with one pod kill in staging.
- **"Run chaos in prod from day one."** No — start in staging or a prod-shadow environment. Move to prod **after** you've earned the operational confidence (clear blast radius, reliable revert, observability).
- **"It's the same as load testing."** Load testing increases volume; chaos engineering injects qualitatively different conditions (latency, partition, lost packets, instance termination). Use both.
- **"Retries are always good."** Untuned retries amplify outages. Always pair retries with jitter, caps, and a circuit breaker.
- **"If the experiment finds nothing, it failed."** A confirmed hypothesis is signal — your system survives the fault. That's a passing test result, not a wasted day.

---

*Next: [20.7 - Deployment Strategies](20.7---Deployment-Strategies) — Where you ship safely under the resilience you just verified.*
