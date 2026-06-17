---
title: "20.3 — Containers & Orchestration"
subject: "DevOps & SRE"
catalog: advanced
audience_tier: higher-education
chapter: "20.3"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 20.3 — Containers & Orchestration

> *"The cluster is the computer."* — Borg / Kubernetes lineage (paraphrased)

This chapter is the **runtime** under everything else in the track. You containerize with Docker, schedule with Kubernetes, package with Helm or Kustomize, and reconcile with GitOps (Argo CD or Flux). The 2026 reality: GitOps is the default operating model — both Argo CD and Flux reached CNCF Graduated status, and the only debate is which controller fits your team.

---

## 🎯 Learning Objectives

1. Build a small, secure container image (multi-stage, distroless or scratch base, non-root).
2. Read and write the core Kubernetes objects: Pod, Deployment, StatefulSet, Service, Ingress, ConfigMap, Secret, NetworkPolicy.
3. Pick a Kubernetes flavour: **k3s** / **k0s** (edge / dev), **kind** (local), **EKS** / **GKE** / **AKS** (managed), or DIY kubeadm.
4. Package with **Helm** vs **Kustomize** — and know when to combine them.
5. Pick **Argo CD** vs **Flux** — both CNCF Graduated in 2026 — based on team needs.
6. Compare **Istio**, **Linkerd**, and **Cilium Service Mesh** — when you actually need a mesh.

---

## 🖼️ Visual Anchor

![dev-20__fig2](dev-20__fig2.svg)

> *Picture / video reference (external):*
> - 📺 [Kubernetes official tutorials](https://kubernetes.io/docs/tutorials/)
> - 📺 [TechWorld with Nana — Kubernetes Tutorial for Beginners](https://www.youtube.com/@TechWorldwithNana)
> - 📺 [Argo CD docs — Architecture](https://argo-cd.readthedocs.io/en/stable/operator-manual/architecture/)
> - 📺 [Flux docs — Components](https://fluxcd.io/flux/components/)
> - 📺 [Bret Fisher — Docker Mastery](https://www.youtube.com/@BretFisher)

---

## 📚 1. The Container

### Definition 20.3.1 — Container

An isolated process tree on a host kernel, using **cgroups** (resource limits) and **namespaces** (PID, NET, MNT, IPC, UTS, USER) to look like its own machine. Packaged as a layered image in OCI format.

### Multi-stage Dockerfile (Python)

```dockerfile
# Stage 1: build dependencies
FROM python:3.13-slim AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && uv sync --frozen

# Stage 2: runtime
FROM gcr.io/distroless/python3-debian12:nonroot
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY src ./src
ENV PATH="/app/.venv/bin:${PATH}"
USER nonroot
ENTRYPOINT ["python", "-m", "src.main"]
```

Wins: distroless = no shell, no package manager, no CVE surface; non-root = no privilege escalation; multi-stage = small final image (often <100 MB).

---

## ☸️ 2. Kubernetes Core Objects

| Object | What it does |
|---|---|
| **Pod** | One or more containers with shared network/IPC; the unit Kubernetes schedules |
| **Deployment** | Declarative pod replicas + rolling updates |
| **StatefulSet** | Pods with stable identities + persistent volumes (databases, caches) |
| **DaemonSet** | One pod per node (log shippers, agents) |
| **Job / CronJob** | Run-to-completion / scheduled tasks |
| **Service** | Stable virtual IP for a set of pods (ClusterIP, NodePort, LoadBalancer) |
| **Ingress / Gateway** | HTTP(S) routing into the cluster |
| **ConfigMap / Secret** | Non-secret / secret config injected as files or env vars |
| **NetworkPolicy** | Pod-level firewall rules |
| **HorizontalPodAutoscaler / VerticalPodAutoscaler** | Replica / resource autoscaling |

### Minimal Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: web }
spec:
  replicas: 3
  selector: { matchLabels: { app: web } }
  template:
    metadata: { labels: { app: web } }
    spec:
      containers:
      - name: web
        image: ghcr.io/myorg/web:1.4.2
        ports: [{ containerPort: 8080 }]
        resources:
          requests: { cpu: "100m", memory: "128Mi" }
          limits:   { cpu: "500m", memory: "256Mi" }
        readinessProbe:
          httpGet: { path: /healthz, port: 8080 }
        livenessProbe:
          httpGet: { path: /healthz, port: 8080 }
```

---

## 🎛️ 3. Flavours of Kubernetes

| Flavour | Best for | Trade-off |
|---|---|---|
| **kind / minikube** | Local dev | Toy scale |
| **k3s / k0s** | Edge, IoT, single-node prod, homelab | Smaller community footprint |
| **EKS / GKE / AKS** | Managed prod on cloud | Vendor lock-in for control plane |
| **kubeadm + bare metal** | On-prem prod | You own all the operations |
| **OpenShift (Red Hat)** | Enterprise prod | License cost |
| **Rancher / SUSE Rancher** | Multi-cluster mgmt | Extra layer |

---

## 📦 4. Helm vs Kustomize

| Tool | Model | Strength | Weakness |
|---|---|---|---|
| **Helm** | Templated charts (Go templates → YAML) | Reusable packages; versioned releases; huge public chart catalog | Templates can be hard to read; debugging brittle |
| **Kustomize** | Overlays (base + patches) | Pure YAML; no templating; easy to read | No package distribution out of the box |
| **Combined** | Helm chart rendered, then patched with Kustomize | Best of both | More moving pieces |

**Decision heuristic:** Distributing a tool to others → Helm. In-house env layering (dev / staging / prod) → Kustomize. Most platform teams do both.

---

## 🔁 5. GitOps — Argo CD vs Flux

GitOps reconciles cluster state from a Git repo. You don't `kubectl apply` — you push a commit and a controller converges the cluster. Both leading tools are CNCF Graduated. (paraphrased from [oneuptime — ArgoCD vs FluxCD in 2026](https://oneuptime.com/blog/post/2026-02-26-argocd-vs-fluxcd-2026/view) and [tasrieit — ArgoCD vs Flux 2026](https://tasrieit.com/blog/argocd-vs-flux-gitops-comparison-2026), rephrased for compliance)

| Dimension | Argo CD | Flux |
|---|---|---|
| **Model** | Single application with rich UI + topology graph | Set of Kubernetes-native controllers, almost no UI |
| **Onboarding** | Easier — point-and-click in dashboard | CLI-first, GitOps purist |
| **Multi-cluster** | One Argo CD manages many clusters | One Flux per cluster (typically) |
| **Image automation** | Separate Argo CD Image Updater component | Native to Flux |
| **Helm / Kustomize** | First-class | First-class |
| **2 AM ops experience** | Strong — visual reconciliation graph | Strong — Kubernetes-native, controller logs |

(table summary paraphrased from [computingforgeeks — Flux CD vs ArgoCD](https://computingforgeeks.com/flux-vs-argocd-multi-cluster/), [bitslovers — Flux CD GitOps Beyond ArgoCD on EKS](https://www.bitslovers.com/flux-cd-gitops-beyond-argocd-eks/), and [jacar.es — Flux CD vs ArgoCD](https://jacar.es/en/flux-cd-comparativa/), rephrased for compliance)

> **Heuristic:** Platform team running many clusters with non-platform users who need a UI → Argo CD. Small infra-savvy team that lives in YAML and wants image automation built in → Flux.

### Argo CD Application example

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata: { name: web, namespace: argocd }
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/manifests.git
    targetRevision: main
    path: envs/prod/web
  destination:
    server: https://kubernetes.default.svc
    namespace: web
  syncPolicy:
    automated: { prune: true, selfHeal: true }
    syncOptions: ["ApplyOutOfSyncOnly=true"]
```

---

## 🕸️ 6. Service Mesh — Do You Actually Need One?

A service mesh adds: mTLS between services, retries / timeouts / circuit breakers, fine-grained traffic shifting, telemetry. Cost: more moving parts, more debugging.

| Mesh | Highlights |
|---|---|
| **Istio** | Most features, biggest community, heaviest |
| **Linkerd** | Rust data plane, fast, simple |
| **Cilium Service Mesh** | eBPF-based, fewer sidecars |
| **Kuma** | Universal (k8s + VMs), Kong-backed |

**Heuristic:** Don't introduce a mesh for fewer than ~10 services or before you have observability ([20.4 - Observability - Logs, Metrics, Traces](20.4---Observability---Logs,-Metrics,-Traces)). If you adopt one, prefer Linkerd or Cilium for simplicity unless you need Istio's full traffic-shaping vocabulary.

---

## 🛠️ 7. Worked Example — Container → Cluster via GitOps

1. **Build + sign + push** image (see [20.1 - CI-CD Foundations](20.1---CI-CD-Foundations)) → `ghcr.io/myorg/web@sha256:...`
2. **Bump manifest**: a separate `manifests` repo's `envs/prod/web/kustomization.yaml` pins the new SHA via `images:` block. The CI from step 1 opens a PR to that repo.
3. **Merge** the manifest PR.
4. **Argo CD detects the change**, validates against signature policy (Cosign verification), syncs the Deployment.
5. **Rollout** uses Argo Rollouts ([20.7 - Deployment Strategies](20.7---Deployment-Strategies)) for canary.
6. **Observe** SLO burn rate ([20.5 - SLOs, SLAs, Error Budgets & Incident Response](20.5---SLOs,-SLAs,-Error-Budgets-&-Incident-Response)); auto-revert if burn fast.

The application repo never has cluster credentials. The manifests repo has the cluster's source-of-truth. The cluster pulls from Git — never the other way around.

---

## 🔗 8. Cross-links & Further Reading

### Internal
- [20.1 - CI-CD Foundations](20.1---CI-CD-Foundations) — image build and signing
- [20.2 - Infrastructure as Code](20.2---Infrastructure-as-Code) — Terraform/Crossplane provisioning the cluster
- [20.4 - Observability - Logs, Metrics, Traces](20.4---Observability---Logs,-Metrics,-Traces) — what gets emitted from these pods
- [20.7 - Deployment Strategies](20.7---Deployment-Strategies) — Argo Rollouts canary / blue-green
- [1.9 - Docker & Containers](1.9---Docker-&-Containers) — container fundamentals
- [1.10 - Operating Systems Essentials](1.10---Operating-Systems-Essentials) — cgroups + namespaces

### External
- [Kubernetes docs](https://kubernetes.io/docs/)
- [Helm](https://helm.sh/) · [Kustomize](https://kustomize.io/)
- [Argo CD docs](https://argo-cd.readthedocs.io/) · [Flux docs](https://fluxcd.io/flux/)
- [k3s](https://k3s.io/) · [k0s](https://k0sproject.io/)
- [Linkerd](https://linkerd.io/) · [Istio](https://istio.io/) · [Cilium Service Mesh](https://cilium.io/)
- [atmosly — GitOps for Kubernetes Implementation Guide 2025](https://atmosly.com/blog/gitops-for-kubernetes-implementation-guide-2025)
- [reintech — Which GitOps Tool to Choose in 2026](https://reintech.io/blog/argocd-vs-flux-which-gitops-tool-should-you-choose-in-2026)

---

## ⚠️ 9. Common Misconceptions

- **"Kubernetes is the only orchestrator."** Nomad, ECS, and even good ol' systemd + cloud LBs all run real production. Choose by workload shape and team capacity.
- **"You need a service mesh from day one."** No. Most apps need ingress + good app-level retries. Add mesh when traffic-shaping or mTLS becomes the bottleneck.
- **"GitOps means kubectl is forbidden."** It means the cluster is reconciled *to* Git. Break-glass kubectl is fine — just commit it back into Git or accept the controller will revert it (selfHeal).
- **"Argo CD is better than Flux."** Both are CNCF Graduated. They optimize for different teams; neither is universally better. (paraphrased from [tasrieit — ArgoCD vs Flux 2026](https://tasrieit.com/blog/argocd-vs-flux-gitops-comparison-2026), rephrased for compliance)
- **"Distroless is for paranoid people."** It removes thousands of lines of attack surface and shrinks images. It's a default, not an extreme.

---

*Next: [20.4 - Observability - Logs, Metrics, Traces](20.4---Observability---Logs,-Metrics,-Traces) — What's actually happening inside those pods.*
