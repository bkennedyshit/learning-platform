---
title: "18.7 — Cloud & Container Security"
subject: "Cybersecurity"
catalog: advanced
audience_tier: higher-education
chapter: "18.7"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 18.7 — Cloud & Container Security

> *"The cluster is your data center now. Treat every namespace like a tenant, every pod like an untrusted workload, and every IAM policy like an audit finding waiting to happen."*

This chapter makes the runtime hostile to attackers and friendly to operators. It covers cloud IAM, secrets, Kubernetes RBAC + the Pod Security Standards that replaced PodSecurityPolicy, NetworkPolicies, image scanning, and runtime detection with Falco.

The 2026 baseline: Kubernetes Pod Security Standards (Privileged / Baseline / Restricted) are the canonical replacement for PSP — which was removed in k8s 1.25 — and are enforced via namespace labels (`pod-security.kubernetes.io/enforce: restricted`). (paraphrased from [kubernetes.io PSS](https://kubernetes.io/docs/concepts/security/pod-security-standards/) · [reintech.io](https://reintech.io/blog/kubernetes-security-best-practices-pod-security-standards-2026))

> Source rephrased for compliance: [kubernetes.io/docs/concepts/security/pod-security-standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/) · [reintech.io](https://reintech.io/blog/kubernetes-security-best-practices-pod-security-standards-2026).

---

## 🎯 Learning Objectives

1. Apply IAM least-privilege using identity federation rather than long-lived keys.
2. Move every secret out of `.env` files and into Vault / Doppler / cloud KMS.
3. Configure Kubernetes RBAC: ServiceAccounts, Roles, RoleBindings, namespace boundaries.
4. Choose and enforce a **Pod Security Standard** profile (Restricted by default).
5. Author **NetworkPolicies** that default-deny and allow-list specific ingress/egress.
6. Scan container images at build (Trivy/Grype) and admission (Sigstore policy controller).
7. Detect runtime threats with **Falco** rules; integrate with on-call.

---

## 🖼️ Visual Anchor

> *Picture / video reference (external):*
> - 📺 [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
> - 📺 [Falco runtime threat detection](https://falco.org/docs/)
> - 📺 [Kyverno policy library](https://kyverno.io/policies/)
> - 📺 [HashiCorp Vault learn](https://developer.hashicorp.com/vault/tutorials)
> - 📺 [Reintech — K8s security best practices 2026](https://reintech.io/blog/kubernetes-security-best-practices-pod-security-standards-2026)

---

## 📚 1. Cloud IAM — Identity, Federation, Least Privilege

The single highest-value rule: **no long-lived access keys**. Use:
- **GitHub Actions OIDC** to AWS / GCP / Azure for CI deploys (zero stored secrets).
- **Workload Identity** (GKE) or **IRSA** (EKS) or **Azure AD Workload Identity** to scope per-pod credentials.
- Per-environment, per-service IAM roles — never a "default" role used by everything.

```hcl
# Terraform — AWS IRSA: pod gets a scoped role via OIDC, no static keys
resource "aws_iam_role" "payments" {
  name = "eks-payments"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = { Federated = aws_iam_openid_connect_provider.eks.arn },
      Action = "sts:AssumeRoleWithWebIdentity",
      Condition = {
        StringEquals = {
          "${replace(aws_iam_openid_connect_provider.eks.url, "https://", "")}:sub" = "system:serviceaccount:payments:payments-sa"
          "${replace(aws_iam_openid_connect_provider.eks.url, "https://", "")}:aud" = "sts.amazonaws.com"
        }
      }
    }]
  })
}
```

Audit with **Access Analyzer** / **IAM Recommender** monthly. Anything wider than necessary is a finding.

---

## 🔐 2. Secrets Management

| Tool | Sweet spot |
|---|---|
| **HashiCorp Vault (OSS)** | Self-hosted, dynamic secrets, transit engine, multi-cloud |
| **Doppler** | SaaS, dev-friendly UX |
| **Cloud KMS** (AWS / GCP / Azure) | Native, integrates with everything in that cloud |
| **External Secrets Operator** (k8s) | Sync secrets from any of the above into k8s Secrets |
| **age / SOPS** | "secrets in git" with KMS-backed encryption |

Rules:
- Never commit secrets — even briefly. Use **gitleaks** or **TruffleHog** in pre-commit.
- Prefer **dynamic secrets** (Vault DB engine issuing short-lived creds) over static passwords.
- Rotate KEKs annually; rotate dynamic creds on every issuance.
- Track every secret read in audit logs.

---

## ☸️ 3. Kubernetes RBAC

The model: a `ServiceAccount` (identity) is bound to a `Role` (permissions in a namespace) or `ClusterRole` (cluster-wide) via a `RoleBinding` / `ClusterRoleBinding`.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata: { name: payments-sa, namespace: payments }
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata: { name: payments-role, namespace: payments }
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list"]
  - apiGroups: ["batch"]
    resources: ["jobs"]
    verbs: ["create"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata: { name: payments-rb, namespace: payments }
subjects:
  - kind: ServiceAccount
    name: payments-sa
    namespace: payments
roleRef:
  kind: Role
  name: payments-role
  apiGroup: rbac.authorization.k8s.io
```

Audit with `kubectl auth can-i --as=system:serviceaccount:payments:payments-sa --list`. Avoid `cluster-admin` like fire.

---

## 🛡️ 4. Pod Security Standards (PSS)

PSS replaced PodSecurityPolicy in k8s 1.25. Three profiles, enforced per-namespace:

| Profile | What it allows | Use when |
|---|---|---|
| **Privileged** | Anything | Cluster components only |
| **Baseline** | No privilege escalation, but allows hostPath etc. | Legacy workloads |
| **Restricted** | Strict — non-root, dropped caps, seccomp, no hostPath | **Default** for app workloads |

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: payments
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/audit: restricted
```

Restricted requires every pod to declare `securityContext.runAsNonRoot: true`, drop all Linux capabilities, set `seccompProfile.type: RuntimeDefault`, and avoid host namespaces. (paraphrased from [kubernetes.io PSS](https://kubernetes.io/docs/concepts/security/pod-security-standards/) · [reintech.io](https://reintech.io/blog/kubernetes-security-best-practices-pod-security-standards-2026))

> Source rephrased for compliance: [kubernetes.io/docs/concepts/security/pod-security-standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/).

```yaml
# A Restricted-conformant pod
apiVersion: v1
kind: Pod
metadata: { name: payments, namespace: payments }
spec:
  serviceAccountName: payments-sa
  securityContext:
    runAsNonRoot: true
    runAsUser: 10001
    fsGroup: 10001
    seccompProfile: { type: RuntimeDefault }
  containers:
    - name: app
      image: ghcr.io/me/payments:v1.2.3
      imagePullPolicy: IfNotPresent
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities: { drop: ["ALL"] }
      resources:
        requests: { cpu: "100m", memory: "128Mi" }
        limits:   { cpu: "500m", memory: "512Mi" }
```

For deeper policy (image-signed, no latest tags, no privileged), layer **Kyverno** or **OPA Gatekeeper**.

---

## 🌐 5. NetworkPolicies — Default Deny East-West

By default Kubernetes pods can talk to *every other pod*. Reverse that:

```yaml
# Default-deny ingress + egress in a namespace
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: default-deny, namespace: payments }
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
---
# Allow only the orders namespace to reach payments:9000
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: allow-orders-to-payments, namespace: payments }
spec:
  podSelector: { matchLabels: { app: payments } }
  policyTypes: [Ingress]
  ingress:
    - from:
        - namespaceSelector: { matchLabels: { name: orders } }
          podSelector:       { matchLabels: { app: orders } }
      ports:
        - port: 9000
          protocol: TCP
```

NetworkPolicies pair with **service-mesh mTLS** (see [18.6 - Network Security](18.6---Network-Security)) — L3/L4 reachability + L7 identity. Use both.

---

## 🩻 6. Image Scanning — Build + Admission

Build-time: Trivy / Grype on every image. Admission-time: only allow images signed by your CI workflow (Cosign + Kyverno policy from [18.5 - Secure SDLC & Supply Chain](18.5---Secure-SDLC-&-Supply-Chain)).

Image-hardening checklist:
- Distroless or scratch base where possible.
- Non-root user, read-only rootfs.
- Reproducible builds (deterministic timestamps).
- Pin base image by digest, not tag.
- No build secrets baked in (use BuildKit `--secret`).
- Multi-stage builds — final stage has no toolchain.

---

## 🦅 7. Runtime Detection — Falco

Falco is a CNCF project that watches kernel syscalls and matches them against rules:

```yaml
# Custom Falco rule: a shell spawned in payments pod = page on-call
- rule: Shell in payments pod
  desc: Detect interactive shell in payments
  condition: spawned_process and container and proc.name in (bash, sh, zsh)
            and k8s.ns.name = "payments"
  output: "Shell in payments pod (user=%user.name proc=%proc.name container=%container.id)"
  priority: CRITICAL
  tags: [container, shell, mitre_execution]
```

Send Falco events to your SIEM and alert on critical priority. This is the layer that catches what passed every other control.

---

## 🛠️ 8. Worked Example — Locking Down a New Namespace

```bash
# 1) Create namespace with PSS Restricted enforced
kubectl create namespace payments
kubectl label  namespace payments pod-security.kubernetes.io/enforce=restricted

# 2) Apply default-deny NetworkPolicy
kubectl apply -n payments -f default-deny.yaml

# 3) Bind ServiceAccount + minimal Role
kubectl apply -n payments -f payments-sa.yaml -f payments-role.yaml -f payments-rb.yaml

# 4) Sync secrets from Vault via External Secrets Operator
kubectl apply -n payments -f vault-secretstore.yaml -f payments-externalsecret.yaml

# 5) Deploy with mesh + image-signing policy enforced
kubectl apply -n payments -f deployment.yaml

# 6) Falco watches; alerts route to PagerDuty
helm upgrade --install falco falcosecurity/falco -n falco --create-namespace \
  --set falcosidekick.enabled=true \
  --set falcosidekick.config.pagerduty.routingKey=$PD_KEY
```

This sequence implements least-privilege identity, encrypted secrets, default-deny networking, signed-image admission, and runtime detection — the five controls that defend ~90% of cluster compromise scenarios.

---

## 🔗 9. Cross-links & Further Reading

### Internal
- [18.5 - Secure SDLC & Supply Chain](18.5---Secure-SDLC-&-Supply-Chain) — admission controllers + signed images
- [18.6 - Network Security](18.6---Network-Security) — service-mesh mTLS layer above NetworkPolicies
- [18.4 - Cryptography for Developers](18.4---Cryptography-for-Developers) — KMS-backed envelope encryption
- [1.9 - Docker & Containers](1.9---Docker-&-Containers) — container basics
- [1.10 - Operating Systems Essentials](1.10---Operating-Systems-Essentials) — namespaces, capabilities
- [Subject_Plan](Subject_Plan) — sibling track
- [Subject_Plan](Subject_Plan) — sibling track

### External
- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [Kyverno policy library](https://kyverno.io/policies/) and [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/)
- [Falco docs](https://falco.org/docs/) and [Falco rules](https://github.com/falcosecurity/rules)
- [HashiCorp Vault tutorials](https://developer.hashicorp.com/vault/tutorials)
- [External Secrets Operator](https://external-secrets.io/)
- [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Google Cloud Workload Identity](https://cloud.google.com/kubernetes-engine/docs/concepts/workload-identity)
- [Reintech — K8s PSS 2026](https://reintech.io/blog/kubernetes-security-best-practices-pod-security-standards-2026)

---

## ⚠️ 10. Common Misconceptions

- **"My cluster is private, so I'm fine."** Pod-to-pod is wide open by default — NetworkPolicies are required.
- **"PSP is fine."** PSP was removed in k8s 1.25. Migrate to PSS + Kyverno/Gatekeeper.
- **"Cloud roles solve everything."** They handle pod → cloud-API auth; they don't help intra-cluster (use mesh + NetworkPolicies).
- **"Distroless = secure."** Distroless reduces attack surface; you still need scanning, runtime detection, and least-priv at the app layer.
- **"Falco rules are noise."** Tune them to your workloads — quiet Falco is useful Falco; noisy Falco gets ignored.

---

*Next: [18.8 - AI Security & Adversarial ML](18.8---AI-Security-&-Adversarial-ML) — the new attack surface that ties this whole track back to BUILDING_AT_SCALE §5.*
