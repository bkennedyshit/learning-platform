---
title: "README — 21 - Cloud Platforms"
subject: "Cloud Platforms"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: subject-readme
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# 21 - Cloud Platforms — Subject Hub

> One-page subject hub. Lists chapters, source reading materials, **video / picture references stored outside the repo (linked by URL)**, and placeholders for generated study aids.
> Master practice guide: [HOW_TO_USE_PRACTICE](HOW_TO_USE_PRACTICE).

> **Asset storage convention.**
> - **SVG diagrams** (small, theme-responsive, in-vault) → `../_svgs/cloud__<chapter>-fig<n>.svg` and embedded inline via `![cloud__28.x-figN](cloud__28.x-figN.svg)`.
> - **Pictures, screenshots, dashboards, video walkthroughs** are NOT committed to this repo. They live on YouTube, vendor docs, GitHub, or in your local "C:/Obsidian Vault/Bill's Vault/_assets/" sidecar (gitignored). Reference them by **URL**.

---

## 🚀 Quick start

From a terminal in this folder:

```bash
cd "C:/Obsidian Vault/Bill's Vault/05-Knowledge_Foundation/09 - Learning/21 - Cloud Platforms"
# Drill scripts to be added — Terraform plans, Infracost runs, IAM-policy lints
# python "_practice/scripts/<chapter>_<topic>.py" --count 8 --seed 42
```

---

## 📜 Chapter index

- [21.1 - The Cloud Provider Landscape 2026](21.1---The-Cloud-Provider-Landscape-2026)
- [21.2 - Compute Primitives](21.2---Compute-Primitives)
- [21.3 - Storage & Databases](21.3---Storage-&-Databases)
- [21.4 - Networking, DNS & CDN](21.4---Networking,-DNS-&-CDN)
- [21.5 - Identity, IAM & Org Structure](21.5---Identity,-IAM-&-Org-Structure)
- [21.6 - Cost Optimization](21.6---Cost-Optimization)
- [21.7 - Multi-Cloud, Edge & Vendor Lock-In](21.7---Multi-Cloud,-Edge-&-Vendor-Lock-In)
- [21.8 - The Indie & Solo Cloud Stack](21.8---The-Indie-&-Solo-Cloud-Stack)

---

## 🎬 Video & Picture References (external — open in browser)

> These are the open-source / pro-grade media that supplement the chapter notes. Pictures and videos are **not** stored in this repo; they live on YouTube, vendor docs, CNCF, GitHub, etc.

### 📺 Video Channels & Playlists

| Channel / Course | Track Use | Link |
|---|---|---|
| **AWS re:Invent (free recordings)** | Architecture, services, cost-optimization | [youtube.com/@AWSEventsChannel](https://www.youtube.com/@AWSEventsChannel) |
| **Google Cloud Next** | GCP services, BigQuery, AI, Anthos | [youtube.com/@googlecloudtech](https://www.youtube.com/@googlecloudtech) |
| **Microsoft Ignite / Build** | Azure, Entra, AKS | [youtube.com/@microsoftdeveloper](https://www.youtube.com/@microsoftdeveloper) |
| **Cloudflare TV** | Workers, R2, D1, Tunnel demos | [cloudflare.tv](https://cloudflare.tv/) |
| **Fly.io blog walkthroughs** | Container deploys, scale-to-zero patterns | [fly.io/blog](https://fly.io/blog/) |
| **DevOps Toolkit (Viktor Farcic)** | Multi-cloud, Kubernetes, IaC | [youtube.com/@DevOpsToolkit](https://www.youtube.com/@DevOpsToolkit) |
| **Hussein Nasser — Backend Engineering** | Networking deep dives | [youtube.com/@hnasr](https://www.youtube.com/@hnasr) |
| **Marcel Dempers (That DevOps Guy)** | Practical k8s, observability, multi-cloud | [youtube.com/@MarcelDempers](https://www.youtube.com/@MarcelDempers) |
| **CNCF YouTube** | KubeCon, OpenTelemetry, Linkerd, etc. | [youtube.com/@cncf](https://www.youtube.com/@cncf) |
| **FinOps Foundation YouTube** | Crawl/Walk/Run maturity sessions | [youtube.com/@FinOpsFoundation](https://www.youtube.com/@FinOpsFoundation) |

### 🖼️ Picture / Diagram Reference Sources

| Source | What it gives you | Link |
|---|---|---|
| **AWS Architecture Center diagrams** | Reference architectures across every service | [aws.amazon.com/architecture](https://aws.amazon.com/architecture/) |
| **GCP Architecture Center diagrams** | Decision-frame visuals + reference designs | [cloud.google.com/architecture](https://cloud.google.com/architecture) |
| **Azure Architecture Center diagrams** | Service-by-service reference designs | [learn.microsoft.com/azure/architecture](https://learn.microsoft.com/en-us/azure/architecture/) |
| **CNCF Cloud Native Landscape** | The interactive who-is-who of cloud-native software | [landscape.cncf.io](https://landscape.cncf.io/) |
| **Cloudflare reference docs (figures)** | Workers · R2 · D1 · Tunnel architecture diagrams | [developers.cloudflare.com](https://developers.cloudflare.com/) |
| **FinOps Foundation framework** | Crawl/Walk/Run maturity diagrams | [finops.org/framework](https://www.finops.org/framework/) |

### 📚 Open-Source / Free Books & References

| Title | Author / Provider | Link |
|---|---|---|
| AWS Well-Architected Framework | AWS | [aws.amazon.com/architecture/well-architected](https://aws.amazon.com/architecture/well-architected/) |
| GCP Architecture Framework | GCP | [cloud.google.com/architecture/framework](https://cloud.google.com/architecture/framework) |
| Microsoft Cloud Adoption Framework | Microsoft | [learn.microsoft.com/azure/cloud-adoption-framework](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/) |
| The Twelve-Factor App | Adam Wiggins / Heroku | [12factor.net](https://12factor.net/) |
| FinOps Foundation Framework | FinOps Foundation | [finops.org](https://www.finops.org/) |
| Awesome Cloud (curated list) | community | [github.com/JStumpp/awesome-cloud](https://github.com/JStumpp/awesome-cloud) |
| Awesome Self-Hosted | community | [github.com/awesome-selfhosted/awesome-selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted) |
| Roadmap.sh AWS / Cloudflare / DevOps | community | [roadmap.sh/aws](https://roadmap.sh/aws) |

### 🛠️ Free / Indie Tooling Worth Knowing

- **Infracost** — IaC cost prediction in PRs ([infracost.io](https://www.infracost.io/))
- **OpenCost** — CNCF k8s cost allocation ([opencost.io](https://www.opencost.io/))
- **Vantage** — multi-cloud cost dashboard (free tier)
- **Tailscale** — WireGuard mesh VPN (100 devices free)
- **Cloudflare Tunnel** — zero-trust ingress without exposing ports
- **k9s** — terminal UI for Kubernetes
- **lazydocker** — terminal UI for Docker
- **flyctl** — Fly.io CLI, ridiculously simple
- **wrangler** — Cloudflare Workers CLI

---

## 🧰 Generated study aids

### 🎙️ Audio overviews & podcasts (NotebookLM)
- [ ] TODO: paste the NotebookLM "Audio Overview" link

### 🧠 Mind maps
- [ ] TODO: NotebookLM mind-map URL or screenshot

### ❓ Quizzes
- [ ] TODO: NotebookLM-generated quiz

### 📊 Reports & summaries
- [ ] TODO: NotebookLM "Briefing Doc" or "Study Guide"

### 🃏 Flash cards
- [ ] TODO: deck export (Anki, Obsidian SR) — IAM policy snippets, service-name mnemonics, FinOps terms

### 🎬 Video overviews
- [ ] TODO: YouTube / Loom personal recording — your own deploy walkthrough on the Indie stack

### 📋 Data tables
- [ ] TODO: comparison matrix (AWS vs GCP vs Azure vs Cloudflare vs Fly vs Hetzner — feature × price)

---

## 🔗 Cross-links

- Syllabus & curriculum mindmap: [Subject_Plan](Subject_Plan)
- Visual roadmap: [LEARNING_PATH](LEARNING_PATH)
- The meta-playbook this track expands: [BUILDING_AT_SCALE](BUILDING_AT_SCALE) (especially §9)
- Containers foundation: [1.9 - Docker & Containers](1.9---Docker-&-Containers)
- Networks foundation: [1.11 - Computer Networks Essentials](1.11---Computer-Networks-Essentials)
- Distributed-systems foundation: [1.16 - Distributed Systems & Multi-GPU Training](1.16---Distributed-Systems-&-Multi-GPU-Training)
- Sister track — security posture: [Subject_Plan](Subject_Plan)
- Sister track — operating layer: [Subject_Plan](Subject_Plan)
- Sister track — architectural layer: [Subject_Plan](Subject_Plan)
- AI / GPU cloud feeder: [Subject_Plan](Subject_Plan)
- Master Learning index: [00 - 09 - Learning Index](00---09---Learning-Index)
- Master practice guide: [HOW_TO_USE_PRACTICE](HOW_TO_USE_PRACTICE)

---

*Compliance note: every external reference in this hub and its chapters is paraphrased/summarized; no source is reproduced verbatim beyond short attributed phrases. Pricing and feature claims are time-stamped to mid-2026 and should be re-checked at the vendor source before relying on them.*
