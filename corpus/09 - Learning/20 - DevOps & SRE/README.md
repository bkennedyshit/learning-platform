---
date: 2026-05-26
type: subject-readme
tags: [practice, refresher, drills, source-materials, study-aids, devops, sre, ci-cd, kubernetes, observability, slo, finops]
title: "README — 20 - DevOps & SRE"
---

# 20 - DevOps & SRE — Subject Hub

> One-page subject hub. Lists chapters, source reading materials, **video / picture references stored outside the repo (linked by URL)**, and placeholders for generated study aids.
> Master practice guide: [[../HOW_TO_USE_PRACTICE|HOW_TO_USE_PRACTICE]].

> **Asset storage convention.**
> - **SVG diagrams** (small, theme-responsive, in-vault) → `../_svgs/devops__<chapter>-fig<n>.svg` and embedded inline via `![[devops__26.x-figN.svg]]`.
> - **Pictures, screenshots, videos, course recordings** are NOT committed to this repo. They live on YouTube, official docs, GitHub, etc. Reference them by **URL** in this README and in chapter notes.

---

## 🚀 Quick start

From a terminal in this folder:

```bash
cd "C:/Obsidian Vault/Bill's Vault/05-Knowledge_Foundation/09 - Learning/20 - DevOps & SRE"
# (Drill scripts to be added — k6 load tests, OpenTelemetry instrumentation samples,
#  Argo CD app-of-apps templates, error-budget calculators)
```

---

## 📜 Chapter index

- [[20.1 - CI-CD Foundations]]
- [[20.2 - Infrastructure as Code]]
- [[20.3 - Containers & Orchestration]]
- [[20.4 - Observability - Logs, Metrics, Traces]]
- [[20.5 - SLOs, SLAs, Error Budgets & Incident Response]]
- [[20.6 - Chaos Engineering & Resilience]]
- [[20.7 - Deployment Strategies]]
- [[20.8 - Cost & Capacity Engineering - FinOps]]

---

## 🎬 Video & Picture References (external — open in browser)

> These are the open-source / pro-grade media that supplement the chapter notes. Pictures and videos are **not** stored in this repo; they live on YouTube, official docs, GitHub, etc.

### 📺 Video Channels & Playlists

| Channel / Course | Track Use | Link |
|---|---|---|
| **TechWorld with Nana** | DevOps + Kubernetes from zero | [@TechWorldwithNana](https://www.youtube.com/@TechWorldwithNana) |
| **DevOps Toolkit (Viktor Farcic)** | Cloud-native deep dives, opinionated | [@DevOpsToolkit](https://www.youtube.com/@DevOpsToolkit) |
| **Anton Putra — Mastering Monitoring** | Observability + benchmarks | [@AntonPutra](https://www.youtube.com/@AntonPutra) |
| **CNCF (KubeCon recordings, free)** | Conference talks at the source | [@cncf](https://www.youtube.com/@cncf) |
| **Honeycomb's o11ycast** | Observability podcast | [honeycomb.io/blog/o11ycast](https://www.honeycomb.io/blog/category/o11ycast) |
| **Google SRE Classroom (talks)** | Original SRE practice from the source | [sre.google/resources](https://sre.google/resources/) |
| **Bret Fisher — Docker / Kubernetes** | Practical container ops | [@BretFisher](https://www.youtube.com/@BretFisher) |
| **That DevOps Guy (MarcelDempers)** | Hands-on tooling walkthroughs | [@MarcelDempers](https://www.youtube.com/@MarcelDempers) |

### 🖼️ Picture / Diagram Reference Sources

| Source | What it gives you | Link |
|---|---|---|
| **Google SRE Book figures** | SLI/SLO/burn-rate diagrams | [sre.google/sre-book](https://sre.google/sre-book/table-of-contents/) |
| **OpenTelemetry architecture diagrams** | Collector, exporters, semantic conventions | [opentelemetry.io/docs](https://opentelemetry.io/docs/) |
| **Argo CD architecture** | Reconciliation loop visuals | [argo-cd.readthedocs.io/en/stable/operator-manual/architecture](https://argo-cd.readthedocs.io/en/stable/operator-manual/architecture/) |
| **CNCF Landscape** | The complete cloud-native ecosystem chart | [landscape.cncf.io](https://landscape.cncf.io/) |
| **DORA reports figures** | Performance distribution, capability charts | [dora.dev/research](https://dora.dev/research/) |

### 📚 Open-Source / Free Books

| Title | Author / Provider | Link |
|---|---|---|
| **Site Reliability Engineering** (the SRE Book) | Google | [sre.google/sre-book](https://sre.google/sre-book/table-of-contents/) |
| **The Site Reliability Workbook** | Google | [sre.google/workbook](https://sre.google/workbook/table-of-contents/) |
| **Building Secure & Reliable Systems** | Google | [sre.google/books/building-secure-reliable-systems](https://sre.google/books/building-secure-reliable-systems/) |
| **Seeking SRE** (collection) | various; O'Reilly (free chapters) | [O'Reilly](https://www.oreilly.com/library/view/seeking-sre/9781491978856/) |
| **Implementing Service Level Objectives** (Alex Hidalgo) | O'Reilly (paid book; sample chapters free; Alex's free talks are on YouTube) | [Alex Hidalgo on YouTube](https://www.youtube.com/results?search_query=alex+hidalgo+slo) |
| **Chaos Engineering: System Resiliency in Practice** | O'Reilly (free PDF often available via vendors) | [Gremlin learning hub](https://www.gremlin.com/community/) |
| **OpenTelemetry docs** | OpenTelemetry / CNCF | [opentelemetry.io/docs](https://opentelemetry.io/docs/) |
| **Prometheus docs** | Prometheus / CNCF | [prometheus.io/docs](https://prometheus.io/docs/introduction/overview/) |
| **Argo CD docs** | Argo / CNCF | [argo-cd.readthedocs.io](https://argo-cd.readthedocs.io/) |
| **Flux docs** | Flux / CNCF | [fluxcd.io/flux](https://fluxcd.io/flux/) |
| **OpenTofu docs** | Linux Foundation | [opentofu.org/docs](https://opentofu.org/docs/) |
| **FinOps Framework** | FinOps Foundation | [finops.org/framework](https://www.finops.org/framework/) |
| **Awesome Sysadmin** | community | [github.com/awesome-foss/awesome-sysadmin](https://github.com/awesome-foss/awesome-sysadmin) |
| **Roadmap.sh DevOps Roadmap** | community | [roadmap.sh/devops](https://roadmap.sh/devops) |

### 🛠️ Open-Source Tools — quick reference

- **Pipelines**: GitHub Actions, GitLab CI, CircleCI, Jenkins, Tekton, Drone, Buildkite
- **Build orchestration**: Nx, Turborepo, Bazel, Pants, Buck2
- **IaC**: OpenTofu, Terraform, Pulumi, Ansible, Crossplane, Chef, Puppet
- **Containers / orchestration**: Docker, containerd, Podman, Kubernetes (k3s, k0s, EKS, GKE, AKS), Nomad
- **Service mesh**: Istio, Linkerd, Cilium Service Mesh, Kuma
- **Packaging**: Helm, Kustomize, Carvel
- **GitOps**: Argo CD, Flux, Jenkins X
- **Observability**: OpenTelemetry, Prometheus, Grafana, Loki, Tempo, Mimir, Jaeger, SigNoz, Sentry, Honeycomb, Better Stack
- **Incident**: PagerDuty, Opsgenie, Squadcast, Rootly, FireHydrant, incident.io
- **Chaos**: LitmusChaos, Gremlin, Chaos Mesh, AWS Fault Injection Service, Steadybit
- **Progressive delivery**: Argo Rollouts, Flagger
- **Feature flags**: LaunchDarkly, Flagsmith, Unleash, OpenFeature, Statsig, GrowthBook
- **Load testing**: k6, Locust, Gatling, JMeter, Vegeta
- **Supply chain**: Sigstore / Cosign, SLSA, in-toto, Syft, Grype, Trivy
- **FinOps**: OpenCost, Kubecost, Vantage, CloudHealth, Cloudability, CAST AI, Sedai, Usage.ai
- **Developer portals**: Backstage, Port, Cortex, OpsLevel, Humanitec
- **Autoscaling**: HPA, VPA, KEDA, Karpenter, Cluster Autoscaler

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
- [ ] TODO: deck export (Anki, Obsidian SR)

### 🎬 Video overviews
- [ ] TODO: YouTube / Loom personal recording walking through your error-budget policy

### 📋 Data tables
- [ ] TODO: comparison matrix (Argo CD vs Flux, OpenTofu vs Terraform, Kubernetes vs serverless)

---

## 🔗 Cross-links

- Syllabus & curriculum mindmap: [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/20 - DevOps & SRE/Subject_Plan]]
- Visual roadmap: [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/20 - DevOps & SRE/LEARNING_PATH]]
- Git fluency prerequisite: [[../01- Python/1.8 - Git & Version Control]]
- Docker prerequisite: [[../01- Python/1.9 - Docker & Containers]]
- OS / Networking prereqs: [[../01- Python/1.10 - Operating Systems Essentials]] · [[../01- Python/1.11 - Computer Networks Essentials]]
- Distributed systems prereq: [[../01- Python/1.16 - Distributed Systems & Multi-GPU Training]]
- Cybersecurity (parallel track): [[../18 - Cybersecurity/Subject_Plan]]
- System design (parallel track): [[../19 - System Design & Distributed Architecture/Subject_Plan]]
- Cloud platforms (parallel track): [[../21 - Cloud Platforms/Subject_Plan]]
- Building at scale: [[../BUILDING_AT_SCALE]]
- Master Learning index: [[00 - 09 - Learning Index]]
- Master practice guide: [[../HOW_TO_USE_PRACTICE]]
