---
title: "18.4 — Cryptography for Developers"
subject: "Cybersecurity"
catalog: advanced
audience_tier: higher-education
chapter: "18.4"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 18.4 — Cryptography for Developers

> *"You don't 'use' cryptography. You compose vetted primitives in vetted ways. The hard part is choosing — and not panicking when 'post-quantum' shows up in your CIO's slide deck."*

This chapter is the developer's working knowledge of cryptography circa 2026: which primitives to reach for, which libraries to use, how to store passwords, how to sign artifacts, and how to begin the post-quantum migration that NIST has now codified.

The headline 2026 facts: NIST has finalized three post-quantum algorithms — **CRYSTALS-Kyber** for key encapsulation, and **CRYSTALS-Dilithium**, **FALCON**, and **SPHINCS+** for signatures. NIST plans to deprecate quantum-vulnerable algorithms by 2035, and major providers (Cloudflare, Google, Apple) already run hybrid PQC in production for handshake key exchange. (paraphrased from [federalnewsnetwork.com PQC 2026](https://federalnewsnetwork.com/it-modernization/2026/05/risk-compliance-exchange-2026-nists-bill-newhouse-john-hopkins-apls-prathibha-rama-on-prepping-for-pqc-world/) · [itecsonline.com PQC complete guide 2026](https://itecsonline.com/post/post-quantum-cryptography-complete-guide-2026))

> Source rephrased for compliance: [federalnewsnetwork.com](https://federalnewsnetwork.com/it-modernization/2026/05/risk-compliance-exchange-2026-nists-bill-newhouse-john-hopkins-apls-prathibha-rama-on-prepping-for-pqc-world/) · [itecsonline.com](https://itecsonline.com/post/post-quantum-cryptography-complete-guide-2026).

---

## 🎯 Learning Objectives

1. Choose between symmetric, asymmetric, and hash-based primitives based on the task.
2. Pick parameters for AES-GCM / ChaCha20-Poly1305 / Argon2id / Ed25519 without inventing new ones.
3. Explain when to reach for **libsodium**, **age**, **cosign**, and **rage**.
4. Manage keys: rotation, derivation (HKDF), KMS-backed envelope encryption.
5. Begin a post-quantum migration plan with hybrid handshakes and crypto agility.
6. Recognize and refuse anti-patterns (ECB mode, MD5, hard-coded keys, JWT `alg=none`).

---

## 🖼️ Visual Anchor

> *Picture / video reference (external):*
> - 📺 [libsodium documentation](https://doc.libsodium.org/)
> - 📺 [age — modern file encryption](https://age-encryption.org/)
> - 📺 [Cosign + Sigstore](https://docs.sigstore.dev/cosign/overview/)
> - 📺 [NIST PQC standards](https://csrc.nist.gov/projects/post-quantum-cryptography)
> - 📺 [Cryptography Engineering excerpts](https://www.schneier.com/books/cryptography-engineering/)

![sec-18__fig1](sec-18__fig1.svg)
*Fig 1: Public Key Cryptography Data Flow*

---

## 📚 1. The Three Families

| Family | Primitives | Use for |
|---|---|---|
| **Symmetric encryption** | AES-256-GCM, AES-256-GCM-SIV, ChaCha20-Poly1305, XChaCha20-Poly1305 | Encrypt-at-rest, large data streams |
| **Asymmetric (public-key)** | RSA-OAEP, RSA-PSS, ECDH (X25519), ECDSA (P-256), Ed25519 | Key exchange, signatures, identity |
| **Hashing & MAC** | SHA-256/512, BLAKE2/3, HMAC, Argon2id, scrypt, bcrypt | Integrity, password hashing, key derivation |

Defaults you should adopt today:

```
Encrypt small data       → libsodium secretbox (XChaCha20-Poly1305)
Encrypt files            → age (https://age-encryption.org/)
Encrypt at rest in cloud → cloud KMS envelope encryption (DEK + KEK)
Sign messages            → Ed25519
Sign artifacts           → Cosign (Sigstore) — see 18.5
Hash passwords           → Argon2id
Derive keys              → HKDF-SHA-256 (or SHA-512)
TLS                      → TLS 1.3 with X25519 + ChaCha20-Poly1305 (or AES-GCM)
```

---

## 🔐 2. Symmetric Encryption — Pick AEAD or Lose

Always use an **AEAD** mode (Authenticated Encryption with Associated Data). AEAD gives you confidentiality + integrity in one call. ECB and unauthenticated CBC/CTR are footguns.

### Modern choices
- **AES-256-GCM** — fast on hardware with AES-NI; nonce must be unique per key (96-bit, never reuse).
- **AES-256-GCM-SIV** — nonce-misuse-resistant (slightly slower; safer for resumed/streamed contexts).
- **ChaCha20-Poly1305 / XChaCha20-Poly1305** — software-fast, constant-time without hardware support; XChaCha gives you a 192-bit nonce, removing the unique-nonce sword.

```python
# pyca/cryptography — AES-GCM
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
key   = AESGCM.generate_key(bit_length=256)   # 32 bytes
aead  = AESGCM(key)
nonce = os.urandom(12)                        # MUST be unique per key
ct    = aead.encrypt(nonce, plaintext, associated_data=b"v1|tenant=42")
pt    = aead.decrypt(nonce, ct,        associated_data=b"v1|tenant=42")
```

The `associated_data` channel binds context (tenant, version, purpose) so a ciphertext from one context cannot be replayed into another.

---

## ✍️ 3. Asymmetric — Signing & Key Exchange

| Need | Pick |
|---|---|
| Signature, modern | **Ed25519** (deterministic, fast, small) |
| Signature, FIPS / legacy | ECDSA P-256 |
| Signature, legacy compat | RSA-PSS (NEVER PKCS#1 v1.5) |
| Key exchange | **X25519** (ECDH on Curve25519) |

Ed25519 is the boring-good default. Don't roll your own. The 2026 elephant is **post-quantum** — see §6.

---

## 🧂 4. Password Hashing — Argon2id, Always

A password hash is *intentionally slow* and uses memory to defeat GPUs/ASICs. Argon2id is the OWASP-recommended winner of the Password Hashing Competition.

```python
# argon2-cffi — Argon2id parameters circa 2026
from argon2 import PasswordHasher

ph = PasswordHasher(
    type='id',          # Argon2id
    time_cost=3,        # iterations; raise until ~250–500ms per hash on prod hardware
    memory_cost=64*1024,# 64 MiB; raise as RAM budgets allow
    parallelism=2,      # threads
    hash_len=32,
    salt_len=16,
)

stored = ph.hash("correct horse battery staple")
ph.verify(stored, "correct horse battery staple")
```

Calibrate `time_cost` and `memory_cost` to your hardware. Re-hash on login when params change. **Never** use MD5, SHA-1, or unsalted SHA-256 for passwords.

---

## 🗝️ 5. Key Management

Keys deserve as much rigor as code:

- **Don't store keys in env files** — use cloud KMS (AWS KMS, GCP Cloud KMS, Azure Key Vault), HashiCorp Vault, or Doppler.
- **Envelope encryption** — encrypt data with a per-record DEK, encrypt the DEK with a KEK in KMS, store ciphertext + wrapped DEK side-by-side. Rotation = re-wrap, not re-encrypt every record.
- **Derivation** — start from a master secret and derive purpose-bound subkeys with HKDF.
- **Rotation** — every key has an owner, an algorithm, an expiry, and a planned rotation. Track in an inventory.

```text
HKDF-SHA-256(master, info=b"tenant=42|purpose=email-encrypt|v=2") → subkey_v2
```

---

## 🛰️ 6. The Post-Quantum Migration

Cryptographically Relevant Quantum Computers (CRQCs) would break RSA / ECDSA / ECDH via Shor's algorithm. Symmetric primitives merely halve in effective bit-strength via Grover (use AES-256, not AES-128).

NIST's standards landscape (paraphrased from [federalnewsnetwork.com PQC](https://federalnewsnetwork.com/it-modernization/2026/05/risk-compliance-exchange-2026-nists-bill-newhouse-john-hopkins-apls-prathibha-rama-on-prepping-for-pqc-world/) · [itecsonline.com](https://itecsonline.com/post/post-quantum-cryptography-complete-guide-2026)):

| Standard | Replaces | Use |
|---|---|---|
| **CRYSTALS-Kyber** (ML-KEM) | RSA / ECDH key exchange | Lattice KEM |
| **CRYSTALS-Dilithium** (ML-DSA) | RSA / ECDSA signatures | Lattice signatures (general) |
| **FALCON** (FN-DSA) | RSA / ECDSA signatures | Smaller signatures, structured-lattice |
| **SPHINCS+** (SLH-DSA) | RSA / ECDSA signatures | Hash-based, conservative fallback |

> Source rephrased for compliance: [federalnewsnetwork.com](https://federalnewsnetwork.com/it-modernization/2026/05/risk-compliance-exchange-2026-nists-bill-newhouse-john-hopkins-apls-prathibha-rama-on-prepping-for-pqc-world/) · [itecsonline.com](https://itecsonline.com/post/post-quantum-cryptography-complete-guide-2026).

### Migration playbook (start now)
1. **Inventory** — list every place crypto is used (TLS, JWTs, signing, secrets, S/MIME, code-signing).
2. **Crypto agility** — abstract algorithm choice behind a config. No string `"RS256"` literals scattered across the codebase.
3. **Hybrid handshakes** — adopt TLS 1.3 with hybrid X25519+Kyber where supported. Cloudflare and Chrome have shipped this.
4. **Long-lived data** — re-encrypt data that must remain confidential past 2035 (the "harvest now, decrypt later" risk).
5. **Code-signing** — plan to re-issue with Dilithium or hybrid before the deprecation window closes.

---

## 🛠️ 7. Worked Example — End-to-End Encrypted Backup with `age`

Goal: a single binary that produces a tenant-scoped, recipient-encrypted backup blob without operator key material on the host.

```bash
# Generate a recipient keypair on the receiving operator's laptop:
age-keygen -o operator.key
# operator.pub printed — share publicly

# On the host (no secret material needed):
sqlite3 /var/lib/app.db .dump | age -r "$(cat operator.pub)" > backup-2026-05-26.age

# Restore on the operator laptop:
age -d -i operator.key backup-2026-05-26.age | sqlite3 restored.db
```

Why this is good:
- Server holds **no decryption key** — only a public key. A compromise of the server leaks ciphertext only.
- `age` uses X25519 + ChaCha20-Poly1305 — modern AEAD, strong key exchange.
- Multiple recipients (`-r recip1.pub -r recip2.pub`) compose naturally — operator + escrow + DR site, each independently revocable.
- Trivial to wrap in CI / cron.

For artifact signing the analogous tool is **Cosign** — see [18.5 - Secure SDLC & Supply Chain](18.5---Secure-SDLC-&-Supply-Chain).

---

## 🔗 8. Cross-links & Further Reading

### Internal
- [18.2 - OWASP Top 10 2025 Deep Dive](18.2---OWASP-Top-10-2025-Deep-Dive) — A02 Cryptographic Failures
- [18.3 - Authentication, Authorization & Identity](18.3---Authentication,-Authorization-&-Identity) — JWT signing, WebAuthn primitives
- [18.5 - Secure SDLC & Supply Chain](18.5---Secure-SDLC-&-Supply-Chain) — Cosign + Sigstore
- [18.6 - Network Security](18.6---Network-Security) — TLS 1.3 + hybrid PQC handshakes

### External
- [libsodium documentation](https://doc.libsodium.org/) — the recommended general-purpose library
- [age](https://age-encryption.org/) and [rage](https://github.com/str4d/rage) — modern file encryption
- [pyca/cryptography](https://cryptography.io/) — Python's vetted library
- [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [Latacora — "Cryptographic right answers"](https://www.latacora.com/blog/2018/04/03/cryptographic-right-answers/) — opinionated, accurate
- [federalnewsnetwork.com — PQC 2026 panel summary](https://federalnewsnetwork.com/it-modernization/2026/05/risk-compliance-exchange-2026-nists-bill-newhouse-john-hopkins-apls-prathibha-rama-on-prepping-for-pqc-world/)
- [itecsonline.com — Post-Quantum Complete Guide 2026](https://itecsonline.com/post/post-quantum-cryptography-complete-guide-2026)

---

## ⚠️ 9. Common Misconceptions

- **"AES is broken because of quantum."** Symmetric primitives only lose half their effective bit-strength. AES-256 remains conservative even post-CRQC.
- **"Bigger RSA = safer."** RSA-4096 still falls to Shor's. Hybrid + post-quantum is the path; stronger classical params buy you only marginal time.
- **"I should write my own crypto for performance."** Almost never true and almost always disastrous. Stick to libsodium / cryptography / OpenSSL / BoringSSL.
- **"Storing the key in the env var is fine."** Env vars leak through process listings, crash logs, and CI traces. KMS or Vault, every time.
- **"Argon2 is overkill."** It is the new default. bcrypt is acceptable; PBKDF2 only when forced. MD5 / SHA-1 are outright wrong.

---

*Next: [18.5 - Secure SDLC & Supply Chain](18.5---Secure-SDLC-&-Supply-Chain) — where these primitives live in your build pipeline.*
