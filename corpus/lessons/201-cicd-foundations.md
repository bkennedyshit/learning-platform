---
title: "20.1 — CI/CD Foundations"
subject: "DevOps & SRE"
catalog: advanced
audience_tier: higher-education
chapter: "20.1"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 20.1 — CI/CD Foundations

> *"If it isn't in CI, it doesn't exist. If it isn't reproducible, it doesn't ship."*

This chapter is the **assembly line**. Every other chapter in this track assumes you have one. CI (Continuous Integration) merges and verifies; CD (Continuous Delivery / Deployment) gets the verified artifact in front of users. Modern CI/CD also signs the artifact, attests its provenance, and gates promotion on observability — supply-chain hardening is no longer optional.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Describe the canonical CI/CD pipeline stages: commit → lint+test → build → scan → sign+attest → push → deploy (canary→full) → observe → rollback.
2. Author a multi-stage pipeline in **GitHub Actions**, **GitLab CI**, and (briefly) **CircleCI**.
3. Apply caching, matrix builds, and reusable workflows correctly.
4. Pick a monorepo strategy — **Nx**, **Turborepo**, or **Bazel** — based on team and workload shape.
5. Add supply-chain hardening: **Sigstore / Cosign** signatures, **SBOM** (Syft) generation, **SLSA** provenance attestation.
6. Connect pipeline outcomes to **DORA metrics** (deployment frequency, lead time, change failure rate, MTTR).

---

## 🖼️ Visual Anchor

![dev-20__fig1](dev-20__fig1.svg)

---

## 📚 1. The Canonical Pipeline

### Definition 20.1.1 — CI/CD Pipeline

A directed graph of stages, each with inputs (artifacts, secrets, source) and outputs (artifacts, signatures, status), executed automatically on a defined trigger (push, PR, tag, schedule).

The ten canonical stages:

| # | Stage | Goal |
|---|---|---|
| 1 | Commit | Trigger on PR or merge to a tracked branch |
| 2 | Lint + Test | Static analysis + unit / integration tests + coverage gate |
| 3 | Build | Compile / bundle / containerize. Cache aggressively. |
| 4 | Scan | SAST (SonarQube, Semgrep) · SCA (Trivy, Grype) · secret scanning (Gitleaks) |
| 5 | **Sign + Attest** | **Sigstore Cosign signature + SBOM (Syft) + SLSA provenance.** This is the supply-chain hardening step — it lives at the centre of the SVG. |
| 6 | Push Artifact | OCI registry (GHCR, ECR, GAR, Harbor) |
| 7 | Deploy Canary | Small slice of traffic |
| 8 | Deploy Full | 100% / blue-green completion |
| 9 | Observe | Read SLO + error-budget burn rate (see [20.5 - SLOs, SLAs, Error Budgets & Incident Response](20.5---SLOs,-SLAs,-Error-Budgets-&-Incident-Response)) |
| 10 | Rollback | If burn rate exceeds threshold, automatic revert |

If any stage 4–9 fails, you go back to stage 10 — the rollback path is **always** wired up.

---

## 📐 2. GitHub Actions Worked Example

```yaml
# .github/workflows/ci.yml
name: ci
on:
  push: { branches: [main] }
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        py: ["3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.py }}
          cache: "pip"
      - run: pip install -e .[test]
      - run: pytest --cov=src --cov-fail-under=85

  build-and-sign:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      id-token: write   # required for keyless Sigstore signing
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with: { registry: ghcr.io, username: ${{ github.actor }}, password: ${{ secrets.GITHUB_TOKEN }} }
      - uses: docker/build-push-action@v6
        id: build
        with: { push: true, tags: "ghcr.io/${{ github.repository }}:${{ github.sha }}", cache-from: "type=gha", cache-to: "type=gha,mode=max" }
      - uses: anchore/sbom-action@v0
        with: { image: "ghcr.io/${{ github.repository }}:${{ github.sha }}", format: spdx-json }
      - uses: sigstore/cosign-installer@v3
      - run: cosign sign --yes "ghcr.io/${{ github.repository }}@${{ steps.build.outputs.digest }}"
```

Notes:
- `id-token: write` enables **keyless** signing — Sigstore uses the GitHub OIDC token; you never manage a private key.
- `cache: "pip"` and `type=gha` buildx cache make repeat runs ~10× faster.
- `matrix.py` runs three Python versions in parallel.

---

## 🧱 3. Monorepo Build Orchestration

When the repo grows past one service, naive CI rebuilds everything on every change. The fix is a build graph that reruns only what's affected.

| Tool | Languages / scope | Strength | Trade-off |
|---|---|---|---|
| **Nx** | TS-first; Python, Go, Rust plugins | Best DX, dashboard, plugin ecosystem | Strongest in JS/TS world |
| **Turborepo** | TS / JS | Light, fast, Vercel-backed | Limited beyond JS/TS |
| **Bazel** | Polyglot, hermetic | Google-grade scale, remote cache | Steep learning curve, BUILD-file boilerplate |
| **Pants 2** | Polyglot, Python-strong | Ergonomic Python monorepos | Smaller ecosystem |
| **Buck2** | Polyglot, Rust-strong | Meta-grade scale | New, sparse docs |

**Decision heuristic:** Pure JS/TS → Turborepo. Mixed JS/TS-leaning with strong DX needs → Nx. Polyglot at >100 engineers and reproducibility-critical → Bazel.

---

## 🛡️ 4. Supply-Chain Hardening: Sign, SBOM, Attest

Three artefacts attach to every container image you ship:

1. **Cosign signature** — proves *who* built it. Stored alongside the image in the OCI registry; verifiable transparency log entry on Rekor.
2. **SBOM (Software Bill of Materials)** — lists *what's inside* (every dependency, version, license). Generated by Syft in SPDX or CycloneDX format.
3. **SLSA provenance attestation** — describes *how* it was built (source repo, commit, builder identity, parameters). [SLSA v1.0](https://slsa.dev/spec/v1.0/) defines build-integrity levels 1–3.

Verification at deploy time (Kubernetes admission controller using Kyverno or Sigstore policy-controller):

```yaml
# Example Kyverno policy snippet (conceptual)
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: { name: require-image-signature }
spec:
  validationFailureAction: enforce
  rules:
  - name: check-signature
    match: { resources: { kinds: [Pod] } }
    verifyImages:
    - imageReferences: ["ghcr.io/myorg/*"]
      attestors:
      - entries:
        - keyless:
            issuer: https://token.actions.githubusercontent.com
            subject: "https://github.com/myorg/*"
```

Result: an image that wasn't built by your GitHub Actions identity literally cannot run in the cluster.

---

## 📊 5. DORA Metrics — How Pipelines Connect to Outcomes

DORA's "Four Keys" measure software-delivery performance (paraphrased from [DORA — A history of DORA's software delivery metrics](https://dora.dev/insights/dora-metrics-history/), rephrased for compliance):

| Metric | What it measures | Elite-level (DORA) |
|---|---|---|
| **Deployment Frequency** | How often you ship to prod | Multiple per day |
| **Lead Time for Changes** | Commit → production | Less than one day |
| **Change Failure Rate** | % of deploys causing incidents | 0–15% |
| **MTTR (Time to Restore)** | Outage → recovery | Under one hour |

A fifth metric, *reliability*, was added to capture operational health beyond release mechanics. Caveat for 2026: when AI generates a large fraction of committed code, deployment frequency and lead time can mislead — the AI commits don't represent the same human throughput, so MTTR + change failure rate become more diagnostic. (paraphrased from [Larridin — DORA Metrics 2026 Guide](https://larridin.com/developer-productivity-hub/dora-metrics-explained-complete-guide-2026), rephrased for compliance)

---

## 🛠️ 6. Worked Example — A Monorepo with Nx + Affected Builds

**Goal:** in a JS/TS monorepo with three apps (web, api, worker) and four libs, only the projects affected by a PR get rebuilt and tested.

```bash
# package.json scripts
{
  "test:affected":  "nx affected --target=test  --base=origin/main",
  "build:affected": "nx affected --target=build --base=origin/main",
  "lint:affected":  "nx affected --target=lint  --base=origin/main"
}
```

```yaml
# .github/workflows/monorepo.yml (excerpt)
- run: pnpm install --frozen-lockfile
- run: pnpm exec nx-cloud start-ci-run    # Nx Cloud distributed cache
- run: pnpm test:affected
- run: pnpm build:affected
- run: pnpm exec nx-cloud stop-all-agents
```

The **distributed cache** is the magic — when teammate A built `lib/auth` on their laptop or in CI, teammate B's CI gets a cache hit instead of rebuilding it. Same model in Turborepo Remote Cache and Bazel Remote Cache.

---

## 🔗 7. Cross-links & Further Reading

### Internal
- [20.2 - Infrastructure as Code](20.2---Infrastructure-as-Code) — what the pipeline deploys *to*
- [20.3 - Containers & Orchestration](20.3---Containers-&-Orchestration) — what the build artifact *is*
- [20.5 - SLOs, SLAs, Error Budgets & Incident Response](20.5---SLOs,-SLAs,-Error-Budgets-&-Incident-Response) — what gates promotion
- [20.7 - Deployment Strategies](20.7---Deployment-Strategies) — canary, blue-green, feature flags
- [Subject_Plan](Subject_Plan) — supply-chain attacks (SolarWinds, xz)
- [1.8 - Git & Version Control](1.8---Git-&-Version-Control) — branching strategies

### External
- [GitHub Actions docs](https://docs.github.com/en/actions)
- [GitLab CI/CD docs](https://docs.gitlab.com/ee/ci/)
- [CircleCI docs](https://circleci.com/docs/)
- [Sigstore](https://www.sigstore.dev/) · [Cosign](https://docs.sigstore.dev/cosign/overview/)
- [SLSA](https://slsa.dev/) · [in-toto](https://in-toto.io/)
- [Nx](https://nx.dev/) · [Turborepo](https://turbo.build/) · [Bazel](https://bazel.build/) · [Pants 2](https://www.pantsbuild.org/) · [Buck2](https://buck2.build/)
- [DORA research](https://dora.dev/research/)
- [Roadmap.sh — DevOps Roadmap](https://roadmap.sh/devops)

---

## ⚠️ 8. Common Misconceptions

- **"CI is just running tests."** CI's purpose is `merge confidently`. Tests are one signal; lint, type-check, security scan, SBOM, and signature are equally part of the bar.
- **"Cosign needs a key vault."** Keyless signing via OIDC is the default for OSS and most CI; you don't need to manage long-lived keys.
- **"Matrix builds are free."** They multiply cost linearly — be deliberate about which axes (OS × runtime version × arch) actually need coverage.
- **"Caching is automatic."** Cache keys are hand-crafted; a wrong key either misses every time (wasteful) or hits stale (broken). Lock files are usually the right key.
- **"Faster CI is always better."** Past a threshold, fast CI without good observability and automated rollback creates faster outages. Pair speed with stages 9–10.

---

*Next: [20.2 - Infrastructure as Code](20.2---Infrastructure-as-Code) — Where the cluster, the network, and the database all become code.*
