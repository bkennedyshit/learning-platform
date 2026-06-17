---
title: "README — 18 - Cybersecurity"
subject: "Cybersecurity"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: subject-readme
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# 18 - Cybersecurity — Subject Hub

> One-page subject hub. Lists chapters, source reading materials, **video / picture references stored outside the repo (linked by URL)**, and placeholders for generated study aids.
> Master practice guide: [HOW_TO_USE_PRACTICE](HOW_TO_USE_PRACTICE).

> **Asset storage convention.**
> - **SVG diagrams** (small, theme-responsive, in-vault) → `../_svgs/cyber__<chapter>-fig<n>.svg` and embedded inline via `![cyber__25.x-figN](cyber__25.x-figN.svg)`.
> - **Pictures, screenshots, videos, course recordings** are NOT committed to this repo. They live on YouTube, official docs, OWASP, NIST, or in your local `_assets/` sidecar (gitignored). Reference them by **URL** in this README and in chapter notes.

---

## 🚀 Quick start

From a terminal in this folder:

```bash
cd "C:/Obsidian Vault/Bill's Vault/05-Knowledge_Foundation/09 - Learning/18 - Cybersecurity"
# (Drill scripts to be added — Semgrep custom rules, prompt-injection harness, OWASP test fixtures)
python "_practice/scripts/<chapter>_<topic>.py" --count 8 --seed 42
```

---

## 📜 Chapter index

- [18.1 - Threat Modeling Fundamentals](18.1---Threat-Modeling-Fundamentals)
- [18.2 - OWASP Top 10 2025 Deep Dive](18.2---OWASP-Top-10-2025-Deep-Dive)
- [18.3 - Authentication, Authorization & Identity](18.3---Authentication,-Authorization-&-Identity)
- [18.4 - Cryptography for Developers](18.4---Cryptography-for-Developers)
- [18.5 - Secure SDLC & Supply Chain](18.5---Secure-SDLC-&-Supply-Chain)
- [18.6 - Network Security](18.6---Network-Security)
- [18.7 - Cloud & Container Security](18.7---Cloud-&-Container-Security)
- [18.8 - AI Security & Adversarial ML](18.8---AI-Security-&-Adversarial-ML)

---

## 🎬 Video & Picture References (external — open in browser)

> These are the open-source / pro-grade media that supplement the chapter notes. Pictures and videos are **not** stored in this repo; they live on YouTube, official docs, GitHub, etc.

### 📺 Video Channels & Playlists

| Channel / Course | Track Use | Link |
|---|---|---|
| **PortSwigger Web Security Academy** | Hands-on labs for every Top 10 category | [portswigger.net/web-security](https://portswigger.net/web-security) |
| **LiveOverflow** | Practical offensive security, CTF, browser exploits | [@LiveOverflow](https://www.youtube.com/@LiveOverflow) |
| **John Hammond** | CTF + malware analysis + practical pentest | [@_JohnHammond](https://www.youtube.com/@_JohnHammond) |
| **IppSec** | Walkthroughs of HackTheBox boxes — how attackers think | [@ippsec](https://www.youtube.com/@ippsec) |
| **Computerphile — Crypto playlist** | Friendly cryptography explanations | [@Computerphile](https://www.youtube.com/@Computerphile) |
| **Black Hat USA / DEF CON archives** | Industry-leading research talks (free recordings) | [black-hat archive](https://www.youtube.com/c/BlackHatOfficialYT) · [DEF CON](https://www.youtube.com/@DEFCONConference) |
| **NahamSec** | Bug-bounty methodology and recon | [@NahamSec](https://www.youtube.com/@NahamSec) |
| **STÖK** | Bug-bounty operations and tooling | [@STOKfredrik](https://www.youtube.com/@STOKfredrik) |
| **Stanford CS155 video archive** | Computer & Network Security course recordings | [web.stanford.edu/class/cs155](http://web.stanford.edu/class/cs155/) |
| **OWASP Foundation YouTube** | OWASP project talks, AppSecEU/USA recordings | [@OWASPFoundation](https://www.youtube.com/@OWASPFoundation) |
| **GitHub Security Lab** | CodeQL queries, supply-chain talks | [@GitHubSecurityLab](https://www.youtube.com/@GitHubSecurityLab) |
| **Sigstore Community Meetings** | Signing pipelines in production | [docs.sigstore.dev/community](https://docs.sigstore.dev/community/) |

### 🖼️ Picture / Diagram Reference Sources

| Source | What it gives you | Link |
|---|---|---|
| **OWASP Top 10:2025 figures** | The official A01–A10 visualization | [owasp.org/Top10](https://owasp.org/Top10/) |
| **OWASP LLM Top 10 figures** | LLM01–LLM10 risk diagrams | [owasp.org LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) |
| **MITRE ATT&CK matrix** | The visual adversary technique map | [attack.mitre.org](https://attack.mitre.org/) |
| **MITRE D3FEND matrix** | Defender countermeasures, mirrored to ATT&CK | [d3fend.mitre.org](https://d3fend.mitre.org/) |
| **NIST SP 800-63 figures** | Identity assurance levels (IAL/AAL/FAL) diagrams | [pages.nist.gov/800-63-4](https://pages.nist.gov/800-63-4/) |
| **Sigstore architecture** | Cosign + Fulcio + Rekor flow | [docs.sigstore.dev](https://docs.sigstore.dev/) |
| **SLSA framework levels** | L1 → L4 build provenance diagrams | [slsa.dev](https://slsa.dev/) |
| **K8s Pod Security Standards** | Privileged / Baseline / Restricted comparison | [kubernetes.io PSS](https://kubernetes.io/docs/concepts/security/pod-security-standards/) |
| **OAuth 2.1 / OIDC flow diagrams** | All grant flows visualized | [oauth.net/2.1](https://oauth.net/2.1/) |

### 📚 Open-Source / Free Books

| Title | Author / Provider | Link |
|---|---|---|
| Security Engineering, 3rd ed. | Ross Anderson (free PDF) | [cl.cam.ac.uk/~rja14/book.html](https://www.cl.cam.ac.uk/~rja14/book.html) |
| OWASP Top 10:2025 | OWASP | [owasp.org/Top10](https://owasp.org/Top10/) |
| OWASP ASVS | OWASP | [owasp.org ASVS](https://owasp.org/www-project-application-security-verification-standard/) |
| OWASP LLM Top 10 | OWASP | [owasp.org LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) |
| OWASP Cheat Sheet Series | OWASP | [cheatsheetseries.owasp.org](https://cheatsheetseries.owasp.org/) |
| Mozilla Web Security Guidelines | Mozilla | [infosec.mozilla.org/guidelines/web_security](https://infosec.mozilla.org/guidelines/web_security) |
| NIST SP 800-63-4 Digital Identity | NIST | [pages.nist.gov/800-63-4](https://pages.nist.gov/800-63-4/) |
| NIST PQC standards portal | NIST | [csrc.nist.gov/projects/post-quantum-cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography) |
| Sigstore docs | Linux Foundation | [docs.sigstore.dev](https://docs.sigstore.dev/) |
| SLSA framework | OpenSSF | [slsa.dev](https://slsa.dev/) |
| CycloneDX SBOM spec | OWASP | [cyclonedx.org](https://cyclonedx.org/) |
| CISA Known Exploited Vulnerabilities | CISA | [cisa.gov KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) |
| Awesome AppSec | Paragon Initiative | [github.com/paragonie/awesome-appsec](https://github.com/paragonie/awesome-appsec) |
| Stanford CS155 | Stanford | [web.stanford.edu/class/cs155](http://web.stanford.edu/class/cs155/) |
| MIT 6.5660 / 6.858 | MIT OCW | [ocw.mit.edu](https://ocw.mit.edu/) |
| HackerOne Hacktivity | HackerOne | [hackerone.com/hacktivity](https://hackerone.com/hacktivity) |
| Have I Been Pwned | Troy Hunt | [haveibeenpwned.com](https://haveibeenpwned.com/) |
| Krebs on Security | Brian Krebs | [krebsonsecurity.com](https://krebsonsecurity.com/) |

---

## 🌐 2026 Industry Snapshot

| Signal | What it says | Source |
|---|---|---|
| OWASP Top 10:2025 adds **A03 Software Supply Chain Failures** and **A10 Mishandling of Exceptional Conditions**; SSRF folded into A01 | Backed by 589 CWEs and ~175k CVE records | [owasp.org/Top10](https://owasp.org/Top10/) · [reflectiz blog](https://www.reflectiz.com/blog/owasp-top-ten-2025/) |
| ~45% of AI-generated code carries known vulns | 150+ LLMs evaluated by Veracode | [veracode.com](https://www.veracode.com/blog/spring-2026-genai-code-security/) |
| 25.7% of AI samples have ≥1 confirmed OWASP Top-10 issue | GPT-5.2, Claude Opus 4.6, Gemini 2.5 Pro, DeepSeek V3, Llama 4 Maverick, Grok 4 | [appsecsanta.com](https://appsecsanta.com/research/ai-code-security-study-2026) |
| OWASP LLM Top 10 (2025/2026) ranks Prompt Injection as LLM01 | Sensitive Information Disclosure as LLM02, Supply Chain LLM03, Data Poisoning LLM04 | [owasp.org LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) · [repello.ai](https://repello.ai/blog/owasp-llm-top-10-2026) |
| ~5 billion passkeys in active use, ~90% consumer awareness, ~75% enabled | FIDO Alliance State of Passkeys 2026 | [fidoalliance.org](https://fidoalliance.org/the-state-of-passkeys-2026-global-consumer-and-workforce-report/) |
| NIST has finalized 3 PQC algorithms (Kyber for KEM; Dilithium / FALCON / SPHINCS+ for signatures) | Deprecation of quantum-vulnerable algorithms targeted by 2035 | [federalnewsnetwork.com](https://federalnewsnetwork.com/it-modernization/2026/05/risk-compliance-exchange-2026-nists-bill-newhouse-john-hopkins-apls-prathibha-rama-on-prepping-for-pqc-world/) · [itecsonline.com](https://itecsonline.com/post/post-quantum-cryptography-complete-guide-2026) |
| K8s Pod Security Standards (Privileged / Baseline / Restricted) replace deprecated PSP from k8s 1.25 | Enforced via namespace labels | [kubernetes.io PSS](https://kubernetes.io/docs/concepts/security/pod-security-standards/) · [reintech.io](https://reintech.io/blog/kubernetes-security-best-practices-pod-security-standards-2026) |
| Industry adopting **SLSA L3 + SBOM + signed images** as the supply-chain baseline | Sigstore = Cosign + Fulcio + Rekor; SBOM via CycloneDX/SPDX | [docs.sigstore.dev](https://docs.sigstore.dev/) · [slsa.dev](https://slsa.dev/) · [liquibase.com](https://www.liquibase.com/blog/docker-supply-chain-security) |

> Source rephrased for compliance: see links above; statistics paraphrased from each report's published headline.

---

## 🧰 Generated study aids

### 🎙️ Audio overviews & podcasts (NotebookLM)
- [ ] TODO: paste the NotebookLM "Audio Overview" link

### 🧠 Mind maps
- [ ] TODO: NotebookLM mind-map URL or screenshot

### ❓ Quizzes
- [ ] TODO: NotebookLM-generated quiz on OWASP Top 10:2025 + LLM Top 10

### 📊 Reports & summaries
- [ ] TODO: NotebookLM "Briefing Doc" or "Study Guide"

### 🃏 Flash cards
- [ ] TODO: deck export (Anki, Obsidian SR) — A01–A10 + LLM01–LLM10

### 🎬 Video overviews
- [ ] TODO: YouTube / Loom personal recording walking through your own threat model

### 📋 Data tables
- [ ] TODO: comparison matrix (managed identity providers — Auth0 vs Clerk vs Supabase Auth vs WorkOS)

---

## 🔗 Cross-links

- Syllabus & curriculum mindmap: [Subject_Plan](Subject_Plan)
- Visual roadmap: [LEARNING_PATH](LEARNING_PATH)
- Foundational meta-playbook: [BUILDING_AT_SCALE](BUILDING_AT_SCALE)
- Python prerequisite: [Subject_Plan](Subject_Plan)
- Docker & containers: [1.9 - Docker & Containers](1.9---Docker-&-Containers)
- OS essentials: [1.10 - Operating Systems Essentials](1.10---Operating-Systems-Essentials)
- Networks essentials: [1.11 - Computer Networks Essentials](1.11---Computer-Networks-Essentials)
- Distributed systems: [1.16 - Distributed Systems & Multi-GPU Training](1.16---Distributed-Systems-&-Multi-GPU-Training)
- SQL: [Subject_Plan](Subject_Plan)
- AI/ML systems: [Subject_Plan](Subject_Plan)
- Transformers / LLMs: [10.5 - Transformer Architectures & LLMs](10.5---Transformer-Architectures-&-LLMs)
- DevOps & SRE (sibling): [Subject_Plan](Subject_Plan)
- System Design (sibling): [Subject_Plan](Subject_Plan)
- Cloud Platforms (sibling): [Subject_Plan](Subject_Plan)
- Master Learning index: [00 - 09 - Learning Index](00---09---Learning-Index)
- Master practice guide: [HOW_TO_USE_PRACTICE](HOW_TO_USE_PRACTICE)
