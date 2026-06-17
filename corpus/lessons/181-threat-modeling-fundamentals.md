---
title: "18.1 — Threat Modeling Fundamentals"
subject: "Cybersecurity"
catalog: advanced
audience_tier: higher-education
chapter: "18.1"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 18.1 — Threat Modeling Fundamentals

> *"Threat modeling is the security practice that returns the highest leverage per hour. Everything else is downstream."*
> — paraphrased from Adam Shostack, *Threat Modeling: Designing for Security*

Every other chapter in this track teaches you **how** to defend something specific. This chapter teaches you the question that comes first: **what are we defending, against whom, and where would they hit us?** Skip this and the rest becomes whack-a-mole. Internalize it and OWASP Top 10, cryptography choices, and AI safety controls all click into place — they are *answers* to threat-model questions, not abstract checklists.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Define the four pillars of any threat model (assets, adversaries, attack surface, attacks) and produce a one-page threat model from a verbal feature description.
2. Draw a Data Flow Diagram (DFD) with explicit **trust boundaries** and run **STRIDE per element** across it.
3. Score a finding with **DREAD** and explain the trade-offs vs **Mozilla's Rapid Risk Assessment (RRA)**.
4. Build an **attack tree** for a chosen system goal and reason about pruning by likelihood and cost.
5. Translate a user story into an **abuse case** ("as an attacker, I want to…").
6. Recognize where threat modeling lives in the SDLC — and how to keep it alive after the first whiteboard session.

---

## 🖼️ Visual Anchor

![cyber__25.1-fig1](cyber__25.1-fig1.svg)

---

## 📚 1. The Four Pillars

Every threat model answers four questions:

| Pillar | Question | Output |
|---|---|---|
| **Assets** | What are we defending? | A ranked list — data, secrets, availability, reputation, money, model weights |
| **Adversaries** | Who would attack and why? | Personas: script kiddie, criminal, insider, nation-state, autonomous AI agent |
| **Attack surface** | Where can they reach us? | DFD with trust boundaries; entry points and exit points |
| **Attacks** | How would they actually do it? | Per-element STRIDE, attack trees, abuse cases |

The most common failure mode is jumping straight to "attacks" without spending time on **assets** and **adversaries**. A threat model that defends model weights against a script kiddie protects very little; one that defends model weights against a competitor with a corrupt insider protects the business.

---

## 📐 2. Data Flow Diagrams + STRIDE Per Element

### Definition 18.1.1 — Trust Boundary
A **trust boundary** is a line on the diagram across which authority changes — typically a network segment, a process boundary, a tenant boundary, or a privilege transition. Every data flow that crosses a trust boundary deserves explicit STRIDE analysis.

### STRIDE Categories

| Letter | Threat | Property violated | Typical mitigation |
|---|---|---|---|
| **S** | **S**poofing | Authentication | Strong identity (passkeys, mTLS, signed tokens) |
| **T** | **T**ampering | Integrity | Signing, hashing, integrity-protected channels |
| **R** | **R**epudiation | Non-repudiation | Append-only audit logs, signed actions |
| **I** | **I**nformation Disclosure | Confidentiality | Encryption, least-privilege, output filtering |
| **D** | **D**enial of Service | Availability | Rate limits, quotas, autoscaling, isolation |
| **E** | **E**levation of Privilege | Authorization | Authz checks, capability-based design, sandboxing |

### STRIDE-per-Element Template

For each element on the DFD (process, data store, data flow, external entity), ask which STRIDE letters apply. A typical assignment:

| Element | Applicable threats |
|---|---|
| External entity | S, R |
| Process | S, T, R, I, D, E |
| Data store | T, I, D, R |
| Data flow | T, I, D |

The result is a finite, auditable list of threats — not a vibes-based "I think we should encrypt some stuff."

---

## 🌳 3. Attack Trees

An **attack tree** is a goal-rooted tree where children are sub-goals or pre-conditions and leaves are atomic actions. Internal nodes are AND or OR gates.

```
GOAL: Read another tenant's customer records
├─ OR: Bypass authorization at API
│   ├─ AND: Find IDOR endpoint  +  Guess tenant_id
│   └─ AND: Forge JWT  +  Server doesn't verify signature
├─ OR: Read database directly
│   ├─ AND: Compromise read replica creds  +  Network reachability
│   └─ AND: SQL injection on shared report  +  No row-level security
└─ OR: Exfiltrate via LLM
    └─ AND: Prompt-inject support agent  +  Agent has cross-tenant tools
```

Score each path by `(probability × impact) / cost-to-attacker` and prune ruthlessly. The remaining branches are your defensive priorities.

---

## 🔬 4. DREAD vs Mozilla Rapid Risk Assessment

### DREAD
A 1–10 score per dimension, summed or averaged:

| Dimension | Question |
|---|---|
| **D**amage | How bad if it happens? |
| **R**eproducibility | How reliably can it be repeated? |
| **E**xploitability | How hard to actually pull off? |
| **A**ffected users | What % of users blast radius? |
| **D**iscoverability | How easy to find? |

DREAD is fast but subjective. Use it for early triage, not regulatory reporting.

### Mozilla Rapid Risk Assessment (RRA)
A 30-minute structured interview producing a **risk level** per CIA dimension. Output: a one-page table that maps to a recommendation level (low / medium / high / critical) and a `ServiceData` classification (public / internal / confidential / restricted). Mozilla publishes RRA as part of its [Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security).

> *RRA is what you run for every new service before shipping; STRIDE is what you run for every new feature.*

---

## ⚔️ 5. Abuse Cases

Every user story has an **abuse case** twin:

| User story | Abuse case |
|---|---|
| As a customer, I want to upload a profile picture | As an attacker, I want to upload a polyglot file that runs as JS or HTML when served back |
| As a customer, I want to share a public link to my doc | As an attacker, I want to enumerate IDs and bulk-download other tenants' "public" docs |
| As a developer, I want to invite an LLM agent to read my email | As an attacker, I want indirect prompt injection embedded in an email to exfiltrate other inbox content |

Capture these in the same backlog as the user stories. Implement the mitigations as **acceptance criteria**, not as separate "security tasks" that get deferred.

---

## 🛠️ 6. Worked Example — Threat Model for a Multi-Tenant SaaS Customer-Support Bot

A common 2026 product: an LLM-backed support agent with read access to a customer's tickets and write access to internal Slack channels.

### Step 1 — Assets
Customer tickets (confidential), Slack history (confidential), the model API key (high impact if leaked), tenant isolation guarantee (reputational).

### Step 2 — Adversaries
External attacker probing public endpoints, malicious end-user submitting crafted tickets, malicious *email sender* whose content the agent will read (indirect prompt injection vector), curious internal employee.

### Step 3 — DFD with trust boundaries
```
[Customer Browser] --tls--> | API Gateway | --rpc--> [Agent Orchestrator] --tools--> [Ticket DB]
                                        \--tools--> [Slack API]
                                        \--llm-->  [Provider API]
```
Trust boundaries: browser↔gateway, gateway↔orchestrator (tenant context attached), orchestrator↔external tools (Slack, provider).

### Step 4 — STRIDE per element (excerpt)
- **Process: Agent Orchestrator** — **E**: agent invokes a Slack tool with the *wrong* tenant context → enforce tenant binding on every tool call. **I**: agent leaks one tenant's data into another tenant's response → output filter + per-call tenant assertion. **T**: indirect prompt injection from a crafted ticket → input policy + tool-allowlist + safe-mode rails.
- **Data flow: Provider API** — **I**: provider logs prompts that contain customer PII → data-processing addendum + redact PII before send.
- **Data store: Ticket DB** — **T/I**: SQL injection via a search field → parameterized queries + row-level security.

### Step 5 — DREAD score (one finding)
*Indirect prompt injection via a forwarded email* — D=8, R=9, E=7, A=10, D=6 → **avg 8.0**, critical priority.

### Step 6 — Mitigation map back to OWASP / ASVS
- Tenant binding → ASVS V4.1 (access control).
- Output filter for cross-tenant leakage → custom control + LLM02 (Sensitive Info Disclosure).
- Tool-allowlist & safe-mode → LLM01 (Prompt Injection) mitigation.
- Parameterized queries → A03:2021 → still applicable; OWASP Top 10:2025 keeps Injection in scope. (paraphrased from [owasp.org/Top10](https://owasp.org/Top10/))

> Source rephrased for compliance: [owasp.org/Top10](https://owasp.org/Top10/).

This single threat-model exercise gives you a concrete, finite, prioritized list of work items — instead of "we should think about security."

---

## 🔗 7. Cross-links & Further Reading

### Internal
- [18.2 - OWASP Top 10 2025 Deep Dive](18.2---OWASP-Top-10-2025-Deep-Dive) — controls catalogue mapped from threats
- [18.8 - AI Security & Adversarial ML](18.8---AI-Security-&-Adversarial-ML) — threat modeling for LLM systems
- [1.10 - Operating Systems Essentials](1.10---Operating-Systems-Essentials) — privilege boundaries are trust boundaries
- [1.11 - Computer Networks Essentials](1.11---Computer-Networks-Essentials) — network trust boundaries
- [BUILDING_AT_SCALE](BUILDING_AT_SCALE) §5 — why this matters at scale

### External
- [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security) — RRA + baselines
- [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)
- [Microsoft STRIDE — original whitepaper](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
- [MITRE ATT&CK](https://attack.mitre.org/) — adversary technique reference
- [MITRE D3FEND](https://d3fend.mitre.org/) — defender's mirror of ATT&CK
- [OWASP Top 10:2025](https://owasp.org/Top10/) — the controls catalogue we'll lean on next chapter
- *Threat Modeling: Designing for Security* — Adam Shostack (Wiley, paid book)

---

## ⚠️ 8. Common Misconceptions

- **"Threat modeling is a one-time deliverable."** It is a living artifact. Every architectural change deserves a delta. Treat it like an ADR.
- **"STRIDE is for Microsoft shops."** STRIDE is a memorable taxonomy; it is tool-agnostic and works on AWS, GCP, on-prem, and LLM systems alike.
- **"DREAD numbers are objective."** They are not — they are calibration aids. Two engineers should compare scores and surface disagreement, not average their gut feelings.
- **"We don't need a model — our framework handles security."** Frameworks defend the layers they own. Your business logic, your tenant model, and your AI tools are not in any framework's threat model.
- **"AI changes everything; old threat-modeling is obsolete."** The opposite. AI multiplies attack surface — STRIDE on every tool call, and every retrieval source, is more important than ever.

---

*Next: [18.2 - OWASP Top 10 2025 Deep Dive](18.2---OWASP-Top-10-2025-Deep-Dive) — the controls catalogue that maps directly back to threats.*
