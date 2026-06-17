---
title: "18.5 — Secure SDLC & Supply Chain"
subject: "Cybersecurity"
catalog: advanced
audience_tier: higher-education
chapter: "18.5"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 18.5 — Secure SDLC & Supply Chain

> *"You are the supply chain. Every dependency, every container layer, every CI runner is a piece of it. The 2025 version of the OWASP Top 10 made that official."*

OWASP Top 10:2025 promotes **Software Supply Chain Failures** to **A03** as a first-class category. The supply-chain stack as it stabilized in 2026 is roughly: SBOM (CycloneDX or SPDX) + Sigstore (Cosign + Fulcio + Rekor) for keyless signing + SLSA L2/L3 build provenance — and most non-trivial OSS projects now ship at least signed releases. (paraphrased from [docs.sigstore.dev](https://docs.sigstore.dev/) · [slsa.dev](https://slsa.dev/) · [github.com/sigstore/cosign](https://github.com/sigstore/cosign) · [liquibase.com](https://www.liquibase.com/blog/docker-supply-chain-security))

> Source rephrased for compliance: [docs.sigstore.dev](https://docs.sigstore.dev/) · [slsa.dev](https://slsa.dev/) · [github.com/sigstore/cosign](https://github.com/sigstore/cosign) · [liquibase.com](https://www.liquibase.com/blog/docker-supply-chain-security).

---

## 🎯 Learning Objectives

1. Distinguish SAST, DAST, IAST, and SCA, and assemble a CI baseline that runs all four.
2. Generate a CycloneDX or SPDX **SBOM** for any artifact you ship.
3. Sign and verify container images with **Cosign** (Sigstore), including OIDC-based keyless signing.
4. Read and produce a **SLSA** provenance attestation; pick a target level (L1–L4).
5. Defend against **dependency confusion** and **typosquatting**.
6. Make **reproducible builds** the default for the artifacts that matter.
7. Build a security-debt budget: track time-to-patch, vuln density, and signed-percentage as KPIs.

---

## 🖼️ Visual Anchor

> *Picture / video reference (external):*
> - 📺 [Sigstore — Cosign overview](https://docs.sigstore.dev/cosign/overview/)
> - 📺 [SLSA framework](https://slsa.dev/)
> - 📺 [CycloneDX SBOM](https://cyclonedx.org/)
> - 📺 [GitHub Security Lab — CodeQL](https://www.youtube.com/@GitHubSecurityLab)
> - 📺 [Liquibase — Docker supply-chain security 2026](https://www.liquibase.com/blog/docker-supply-chain-security)

---

## 📚 1. The Toolkit Layers

| Layer | What it does | Tools |
|---|---|---|
| **SAST** (Static App Security Testing) | Reads source code, finds vulnerable patterns | Semgrep, CodeQL, SonarQube, Bandit |
| **SCA** (Software Composition Analysis) | Cross-references dependencies vs CVE feeds | Snyk, Trivy, Dependabot, Renovate |
| **DAST** (Dynamic App Security Testing) | Hits a running app with attacks | OWASP ZAP, Burp Suite, Nuclei |
| **IAST** (Interactive AST) | Instruments running app + traffic | Contrast, Datadog ASM |
| **SBOM** | Inventory of components in a build | Syft, CycloneDX CLI, SPDX |
| **Signing & provenance** | Tamper-evidence on artifacts | Cosign, Sigstore, in-toto, SLSA |
| **Policy & admission** | Enforce signed/SBOM rules at deploy | Kyverno, OPA Gatekeeper, Sigstore policy controller |

A "good enough" CI in 2026 runs **at minimum**: Semgrep + Trivy + Dependabot/Renovate + Syft + Cosign + a nightly ZAP baseline, gated by a Kyverno admission policy at the cluster.

---

## 🧬 2. SAST — Catch Vulnerabilities At Author Time

```yaml
# .github/workflows/semgrep.yml
name: Semgrep
on: [pull_request]
jobs:
  semgrep:
    runs-on: ubuntu-latest
    container: returntocorp/semgrep
    steps:
      - uses: actions/checkout@v4
      - run: semgrep ci --config=p/owasp-top-ten --config=p/secrets --config=p/python
```

Semgrep's `p/owasp-top-ten` rule pack catches Top-10-shaped patterns (SQLi sinks, command-injection sinks, weak crypto). CodeQL goes deeper for taint analysis. Run **at every PR** and gate on critical findings.

---

## 🧪 3. SCA — Patch Faster Than the Internet

```yaml
# .github/workflows/trivy.yml
name: Trivy
on: [push, schedule]
jobs:
  trivy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aquasecurity/trivy-action@master
        with:
          scan-type: fs
          severity: CRITICAL,HIGH
          exit-code: 1
```

Pair with **Renovate** or **Dependabot** to auto-PR upgrades. Track **time-to-patch** as a leading indicator — a 90-day MTTP is a board-level red flag in 2026.

---

## 📑 4. SBOM — Know What's In The Box

A **Software Bill of Materials** lists every component, version, license, and (ideally) hash. Two open formats:
- **CycloneDX** (OWASP) — security-and-supply-chain native, easy in CI.
- **SPDX** (Linux Foundation, ISO/IEC 5962) — license-and-compliance native, regulatory favorite.

```bash
# Generate CycloneDX SBOM from a directory or a container image
syft packages /workspace        -o cyclonedx-json > sbom.json
syft packages registry:my/img:1 -o cyclonedx-json > image-sbom.json
```

Ship the SBOM **with** the artifact (as an OCI attestation, GitHub release asset, or SLSA in-toto layout). When the next `log4shell` lands, you grep your SBOMs in seconds, not weeks.

---

## 🖋️ 5. Sigstore + Cosign — Keyless Signing

Sigstore's three pieces (paraphrased from [docs.sigstore.dev](https://docs.sigstore.dev/) · [github.com/sigstore/cosign](https://github.com/sigstore/cosign)):

- **Cosign** — the signing CLI for container images, blobs, and OCI artifacts.
- **Fulcio** — a free CA that issues short-lived certificates after OIDC identity verification (GitHub Actions OIDC, Google, Microsoft, etc.).
- **Rekor** — a public append-only transparency log of every signature.

> Source rephrased for compliance: [docs.sigstore.dev](https://docs.sigstore.dev/) · [github.com/sigstore/cosign](https://github.com/sigstore/cosign).

The big idea: you **never store a long-lived signing key**. Your CI authenticates via OIDC, Fulcio mints a short-lived cert tied to that identity, you sign, the entry hits Rekor, and verifiers check both the cert and the log.

```yaml
# Sign a container image keylessly from GitHub Actions
- uses: sigstore/cosign-installer@v3
- run: cosign sign --yes ghcr.io/me/app@${{ steps.build.outputs.digest }}

# Verify, asserting the signing identity = your CI workflow
- run: |
    cosign verify ghcr.io/me/app@${{ steps.deploy.outputs.digest }} \
      --certificate-identity-regexp 'https://github.com/me/app/.github/workflows/release.yml@refs/tags/v.*' \
      --certificate-oidc-issuer 'https://token.actions.githubusercontent.com'
```

---

## 📜 6. SLSA — Build Provenance Levels

**SLSA** (Supply-chain Levels for Software Artifacts) defines four levels of build trust (L1 = "you have a build script," L4 = hermetic, reviewed, two-party). For most teams in 2026, **SLSA L3** (signed provenance from a tamper-evident, isolated builder like GitHub Actions hosted runners with the official slsa-github-generator) is the realistic target.

A SLSA provenance attestation answers: *which source revision, by which builder, with which dependencies, produced this exact artifact hash?* Verifiers can then refuse unknown provenance at admission time.

---

## 🪤 7. Dependency Confusion & Typosquatting

- **Dependency confusion** — your private package `@acme/internal-utils` collides with a public `@acme/internal-utils` an attacker uploads to the registry; the registry resolves to the *higher* version, which is the public one. Defense: scope-protect, configure your package manager to refuse public fallback, register your scope publicly.
- **Typosquatting** — `reqeusts`, `colourama`, `python-dateutil2`. Defense: SBOM diffing, block-list rules in Renovate / Snyk, automated lockfile review.

Both are A03 patterns — see [18.2 - OWASP Top 10 2025 Deep Dive](18.2---OWASP-Top-10-2025-Deep-Dive).

---

## 🧱 8. Reproducible Builds

If two builders, given the same source + inputs, produce **byte-identical** artifacts, then: provenance can be re-verified by anyone, supply-chain attacks become detectable, and you can ship the same binary from a build farm and a customer's air-gapped CI. Practical levers: pinned base images, fixed `SOURCE_DATE_EPOCH`, deterministic compilers, and removing nondeterministic timestamps from outputs.

---

## 🛠️ 9. Worked Example — A Complete Ship-It Pipeline

```yaml
# .github/workflows/release.yml (excerpt)
permissions:
  contents: read
  id-token: write    # required for Sigstore keyless signing
  packages: write

jobs:
  build-and-sign:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # 1) SAST + SCA
      - run: semgrep ci --config=p/owasp-top-ten
      - uses: aquasecurity/trivy-action@master
        with: { scan-type: fs, severity: CRITICAL,HIGH, exit-code: 1 }

      # 2) Build container
      - id: build
        uses: docker/build-push-action@v6
        with: { push: true, tags: ghcr.io/me/app:${{ github.sha }} }

      # 3) SBOM
      - run: syft packages ghcr.io/me/app:${{ github.sha }} -o cyclonedx-json > sbom.json

      # 4) Cosign sign + attach SBOM as attestation
      - uses: sigstore/cosign-installer@v3
      - run: |
          cosign sign --yes ghcr.io/me/app@${{ steps.build.outputs.digest }}
          cosign attest --predicate sbom.json --type cyclonedx \
            --yes ghcr.io/me/app@${{ steps.build.outputs.digest }}

      # 5) SLSA provenance
      - uses: slsa-framework/slsa-github-generator/.github/workflows/generator_container_slsa3.yml@v2
        with:
          image: ghcr.io/me/app
          digest: ${{ steps.build.outputs.digest }}

  deploy:
    needs: build-and-sign
    runs-on: ubuntu-latest
    steps:
      # 6) Verify in CD before rolling out
      - uses: sigstore/cosign-installer@v3
      - run: |
          cosign verify ghcr.io/me/app@${{ needs.build-and-sign.outputs.digest }} \
            --certificate-identity-regexp 'https://github.com/me/app/.+' \
            --certificate-oidc-issuer 'https://token.actions.githubusercontent.com'
          cosign verify-attestation ghcr.io/me/app@${{ needs.build-and-sign.outputs.digest }} \
            --type cyclonedx --certificate-identity-regexp '...' --certificate-oidc-issuer '...'
```

The cluster's **Kyverno** policy then refuses any image not signed by `me/app`'s release workflow:

```yaml
apiVersion: kyverno.io/v2beta1
kind: ClusterPolicy
metadata: { name: require-signed-images }
spec:
  validationFailureAction: Enforce
  rules:
    - name: verify-cosign
      match: { any: [ { resources: { kinds: [Pod] } } ] }
      verifyImages:
        - imageReferences: [ "ghcr.io/me/*" ]
          attestors:
            - entries:
                - keyless:
                    issuer: "https://token.actions.githubusercontent.com"
                    subject: "https://github.com/me/app/.github/workflows/release.yml@refs/tags/v*"
```

This single pipeline closes A03, A06, A08 from [18.2 - OWASP Top 10 2025 Deep Dive](18.2---OWASP-Top-10-2025-Deep-Dive) simultaneously.

---

## 🔗 10. Cross-links & Further Reading

### Internal
- [18.2 - OWASP Top 10 2025 Deep Dive](18.2---OWASP-Top-10-2025-Deep-Dive) — A03, A06, A08
- [18.4 - Cryptography for Developers](18.4---Cryptography-for-Developers) — the signatures behind Cosign
- [18.7 - Cloud & Container Security](18.7---Cloud-&-Container-Security) — admission control and runtime
- [Subject_Plan](Subject_Plan) — CI/CD pipelines (sibling track)

### External
- [Sigstore documentation](https://docs.sigstore.dev/)
- [Cosign GitHub repo](https://github.com/sigstore/cosign)
- [SLSA framework](https://slsa.dev/)
- [CycloneDX](https://cyclonedx.org/) and [SPDX](https://spdx.dev/)
- [Syft](https://github.com/anchore/syft) and [Grype](https://github.com/anchore/grype)
- [Semgrep](https://semgrep.dev/) and [CodeQL](https://codeql.github.com/)
- [Trivy](https://trivy.dev/) and [Snyk](https://snyk.io/)
- [Liquibase — Docker supply-chain 2026](https://www.liquibase.com/blog/docker-supply-chain-security)
- [Kyverno](https://kyverno.io/) and [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/)

---

## ⚠️ 11. Common Misconceptions

- **"SCA is enough."** SCA finds known CVEs in dependencies; it misses logic bugs (SAST) and config bugs (DAST/IaC scan).
- **"We don't ship containers, so SBOM doesn't apply."** Anything with a `package.json` / `requirements.txt` / `go.mod` benefits from an SBOM.
- **"Keyless signing is less secure."** Tying signatures to a short-lived OIDC identity + transparency log is *more* secure than a stored long-lived key that could leak.
- **"SLSA is a vendor checklist."** It is a build-trust gradient. Even SLSA L1 is better than nothing; aim L3 in CI.
- **"Reproducible builds are unrealistic."** Many big projects (Bitcoin Core, Tor Browser, Debian) ship them. The path is incremental.

---

*Next: [18.6 - Network Security](18.6---Network-Security) — TLS 1.3, CSP, zero trust, and the network-layer half of supply chain.*
