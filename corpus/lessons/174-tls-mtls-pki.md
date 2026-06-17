---
title: "17.4 — TLS, mTLS & PKI"
subject: "Networking & Protocols"
catalog: advanced
audience_tier: higher-education
chapter: "17.4"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 17.4 — TLS, mTLS & PKI

> *"TLS 1.3 is one of the most elegant pieces of engineering in the Internet's history. Every round trip removed, every weak cipher eliminated, every feature added only if it improves security. There's no fat."*

TLS (Transport Layer Security) is the cryptographic wrapper that makes the open Internet safe for private communication. Without it, anyone on the network path could read or modify your traffic. TLS 1.3 (RFC 8446, 2018) is a dramatic improvement over its predecessors — 1-RTT handshake, no insecure cipher suites, forward secrecy by default. This chapter walks through every byte.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Narrate every message in a **TLS 1.3 1-RTT handshake** including what keys are derived at each step.
2. Explain **ECDHE key exchange** — why forward secrecy is achieved even if the server's long-term key later leaks.
3. Trace the **HKDF key schedule** from shared secret to traffic keys.
4. Verify a **certificate chain**: leaf → intermediate → root, including SAN, validity period, and revocation checks.
5. Explain **TLS 1.3 0-RTT resumption** using PSK and its replay attack risk.
6. Explain **mTLS (mutual TLS)** and why it's required for zero-trust service mesh architectures.
7. Compare TLS 1.2 and TLS 1.3 and explain why TLS 1.2 is being deprecated.

---

## 🖼️ Visual Anchor

![net-17__fig4](net-17__fig4.svg)

---

## 📚 1. TLS 1.3 — 1-RTT Handshake

### 1.1 Why TLS 1.3 is a 1-RTT Protocol

TLS 1.2 required **2 RTTs** before sending application data (1 RTT for TCP, 2 for TLS = 3 RTTs total). TLS 1.3 achieves **1 RTT** for TLS by combining the server's Finished message and Certificate into the same flight as the ServerHello.

```
Client                                              Server
  │                                                   │
  │                    ClientHello                    │
  │  ─────────────────────────────────────────────►  │
  │  supported_versions=[TLS1.3]                     │
  │  cipher_suites=[TLS_AES_128_GCM_SHA256, ...]     │
  │  key_share[ECDH public key (X25519)]              │
  │  supported_groups=[x25519, secp256r1]             │
  │  session_ticket? (for 0-RTT)                     │
  │                                                   │
  │                    ServerHello                    │
  │  ◄─────────────────────────────────────────────  │
  │  chosen cipher: TLS_AES_128_GCM_SHA256           │
  │  key_share[ECDH public key] ← server's pub key   │
  │   ─── DERIVE Handshake Keys here ───             │
  │                                                   │
  │              {EncryptedExtensions}                │
  │  ◄─────────────────────────────────────────────  │
  │  [all remaining messages are ENCRYPTED]           │
  │                                                   │
  │                  {Certificate}                    │
  │  ◄─────────────────────────────────────────────  │
  │  server's X.509 cert + intermediate chain        │
  │                                                   │
  │              {CertificateVerify}                  │
  │  ◄─────────────────────────────────────────────  │
  │  sig = sign(handshake_transcript, server_privkey) │
  │                                                   │
  │                   {Finished}                      │
  │  ◄─────────────────────────────────────────────  │
  │  HMAC of full handshake transcript               │
  │   ─── Client verifies cert + Finished ───        │
  │                                                   │
  │                   {Finished}                      │
  │  ─────────────────────────────────────────────►  │
  │  Client's HMAC                                   │
  │   ─── DERIVE Application Traffic Keys ───        │
  │                                                   │
  │             [Application Data — AEAD]             │
  │  ◄───────────────────────────────────────────── ►│
```

**Total cost**: TCP handshake (1 RTT) + TLS (1 RTT) = 2 RTTs before application data. TLS 1.2 was 3 RTTs.

### 1.2 What Happens on ClientHello

The ClientHello contains:
- **`supported_versions`**: Client declares TLS 1.3 support. Negotiation backward-compat is handled here.
- **`cipher_suites`**: Supported AEAD ciphers. TLS 1.3 removed RSA key exchange and all weak ciphers; the valid options are:
  - `TLS_AES_128_GCM_SHA256`
  - `TLS_AES_256_GCM_SHA384`
  - `TLS_CHACHA20_POLY1305_SHA256`
- **`key_share`**: Client's ephemeral ECDH public key (Diffie-Hellman parameters). Multiple groups can be offered (X25519 preferred; P-256 fallback).
- **`server_name`** (SNI extension): The hostname the client wants — allows one server IP to host many TLS domains.

### 1.3 ECDHE Key Exchange and Forward Secrecy

ECDHE (Elliptic Curve Diffie-Hellman Ephemeral) is the key exchange mechanism in TLS 1.3.

**How it works** (simplified):
1. Client generates ephemeral key pair `(priv_c, pub_c)` on curve X25519
2. Server generates ephemeral key pair `(priv_s, pub_s)` on curve X25519
3. Client sends `pub_c` in ClientHello
4. Server sends `pub_s` in ServerHello
5. Both sides compute the **shared secret**: `Z = ECDH(priv_c, pub_s) = ECDH(priv_s, pub_c)` (Diffie-Hellman property)

**Forward secrecy**: The ephemeral keys are discarded after the handshake. Even if an attacker records the encrypted traffic and later steals the server's long-term certificate private key, they cannot decrypt old sessions — because the ECDHE private keys that derived the session keys are gone.

TLS 1.2 allowed RSA key exchange (no forward secrecy) and DHE (forward-secret but weaker). TLS 1.3 mandates ECDHE or DHE — RSA key exchange is removed entirely.

### 1.4 Key Derivation — HKDF Key Schedule

TLS 1.3 uses HKDF (HMAC-based Key Derivation Function, RFC 5869) to derive all keys from the ECDHE shared secret:

```
HKDF-Extract(0, 0) → Early Secret
  ↓ + early data (0-RTT) if PSK used
HKDF-Extract(Early Secret, ECDHE_shared_secret) → Handshake Secret
  ├── HKDF-Expand → client_handshake_traffic_secret
  └── HKDF-Expand → server_handshake_traffic_secret
       ↓ used to encrypt {Certificate}, {Finished}
HKDF-Extract(Handshake Secret, 0) → Master Secret
  ├── HKDF-Expand → client_application_traffic_secret
  └── HKDF-Expand → server_application_traffic_secret
       ↓ used for application data
  └── HKDF-Expand → exporter_master_secret (for QUIC, etc.)
  └── HKDF-Expand → resumption_master_secret (for session tickets)
```

Each derived secret is then expanded with HKDF-Expand-Label to produce the actual AES keys and IVs used for AEAD encryption.

---

## 📚 2. Certificate Chain and PKI

### 2.1 X.509 Certificate Structure

An X.509 certificate (RFC 5280) binds a public key to an identity:

```
Certificate {
  Version: v3
  SerialNumber: 123456789
  SignatureAlgorithm: ecdsa-with-SHA256
  Issuer: CN=DigiCert TLS RSA SHA256 2020 CA1, O=DigiCert Inc
  Validity: {
    notBefore: 2025-01-01T00:00:00Z
    notAfter:  2026-01-01T00:00:00Z
  }
  Subject: CN=api.example.com
  SubjectPublicKeyInfo: {algorithm: id-ecPublicKey, key: ...}
  Extensions: {
    SubjectAltName: [DNS:api.example.com, DNS:www.example.com]
    KeyUsage: Digital Signature
    ExtendedKeyUsage: TLS Web Server Authentication
    BasicConstraints: CA:FALSE
    CRLDistributionPoints: http://crl.digicert.com/...
    AuthorityInfoAccess: OCSP http://ocsp.digicert.com/
  }
  Signature: (signed by issuer's private key)
}
```

**Key fields**:
- **SAN (SubjectAltName)**: The hostnames this cert is valid for. **CN is deprecated for validation; SAN is authoritative.** Wildcard `*.example.com` matches one level (not `a.b.example.com`).
- **BasicConstraints CA:FALSE**: Leaf cert — cannot sign other certs.
- **Validity period**: Let's Encrypt certs are 90 days; commercial CAs typically 1 year. CAs will be limited to 47 days starting Sept 2026 per CA/Browser Forum ballot.

### 2.2 Certificate Chain of Trust

```
Root CA (self-signed, in OS/browser trust store)
    └── signs Intermediate CA cert
              └── signs Leaf/End-Entity cert
                        └── used in TLS handshake
```

**Why intermediates?** The Root CA's private key is kept offline in a hardware security module (HSM) in a physically secured facility. Day-to-day certificate signing uses the intermediate CA, whose key is online but more contained. If the intermediate is compromised, it can be revoked without revoking the root.

**Verification steps** (client performs on receiving Certificate message):
1. Build the chain from leaf to a trusted root
2. Verify each signature: `sig(leaf)` was made by intermediate's private key (verify with intermediate's public key)
3. Verify `sig(intermediate)` with root's public key
4. Root is in the OS/browser trust store? (Mozilla NSS, Windows CryptoAPI, macOS Security framework)
5. Validity period: `notBefore ≤ now ≤ notAfter`
6. SAN matches the hostname in the SNI extension
7. Revocation check: OCSP stapling (server includes signed OCSP response) or CRL

### 2.3 OCSP and Certificate Revocation

**OCSP (Online Certificate Status Protocol)**: The client can query the CA's OCSP responder at the URL in the certificate to check if it's been revoked.

**OCSP Stapling**: The server proactively fetches a signed OCSP response from the CA and includes it in the TLS handshake. This:
- Eliminates the client's OCSP round-trip (saves ~100ms RTT)
- Preserves privacy (client doesn't reveal which certificates it's checking to the CA)
- Is required for **CT (Certificate Transparency)** compliance

---

## 📚 3. TLS 1.3 — 0-RTT Resumption

### 3.1 PSK and Session Tickets

After a TLS 1.3 session completes, the server may send a **NewSessionTicket** message:

```
Server → Client: NewSessionTicket {
  ticket_lifetime: 86400  (valid 24 hours)
  ticket_nonce: ...
  ticket: [encrypted blob; only server can decrypt]
}
```

The client stores this ticket. On the next connection to the same server:

```
Client → Server: ClientHello {
  pre_shared_key: [session ticket from previous connection]
  early_data: [application data — 0-RTT]
  ...
}
```

The server decrypts the ticket, recovers the PSK (pre-shared key), and can decrypt the early data **before** completing the handshake.

**Result**: Application data arrives at the server in the **first ClientHello packet** — 0-RTT.

### 3.2 Replay Attack Risk

0-RTT early data is not protected against **replay attacks**. If a network attacker records the ClientHello+early data, they can re-send it to the server later. The server receives what looks like a legitimate request.

This is only safe for **idempotent, non-mutating** requests (e.g., `GET` with read-only semantics). Never use 0-RTT for:
- Payment transactions
- State-mutating API calls
- Authentication actions

Servers control this with `max_early_data_size` and can disable 0-RTT entirely. HTTP/3 and QUIC also inherit this constraint for their 0-RTT data.

---

## 📚 4. mTLS — Mutual TLS

### 4.1 Standard TLS vs mTLS

In **standard TLS**, only the server presents a certificate. The client trusts the server (based on the certificate chain), but the server doesn't cryptographically verify the client's identity.

In **mTLS (mutual TLS)**, both sides present certificates:

```
Standard TLS:
  Client: presents nothing
  Server: presents cert → client verifies
  Result: client trusts server; server trusts any client

mTLS:
  Client: presents cert → server verifies
  Server: presents cert → client verifies
  Result: both sides cryptographically verified
```

**mTLS handshake additions**:
After `{Certificate}` and `{CertificateVerify}` from the server, the server also sends a `CertificateRequest`. The client responds with its own `{Certificate}` and `{CertificateVerify}`.

### 4.2 mTLS in Service Mesh

In a microservices architecture with Istio or Linkerd, **every service gets an X.509 certificate** (SPIFFE SVID — Secure Production Identity Framework for Everyone), and every service-to-service call uses mTLS:

```
Service A (Envoy proxy) ──mTLS──► Service B (Envoy proxy)
  cert: spiffe://cluster.local/ns/default/sa/service-a
  cert: spiffe://cluster.local/ns/default/sa/service-b
```

Benefits:
- **Zero-trust networking**: Even inside the cluster, every connection is authenticated and encrypted
- **No secret management in app code**: The sidecar proxy handles certs; apps just make plain TCP connections to `localhost:15001`
- **Certificate rotation**: The control plane (Istiod/Linkerd) automatically rotates workload certs (typically 24h TTL)
- **Policy enforcement**: Istio AuthorizationPolicy can allow `ServiceA` to call `ServiceB` but deny `ServiceC` — at the mTLS identity level

### 4.3 SPIFFE SVID

SPIFFE (Secure Production Identity Framework for Everyone, a CNCF project) standardizes workload identity:

- **SVID** (SPIFFE Verifiable Identity Document): An X.509 cert with a URI SAN of the form `spiffe://<trust-domain>/<workload-specific-path>`
- Example: `spiffe://prod.example.com/ns/payments/sa/checkout-service`
- No IP addresses, no hostnames — identity is tied to the workload's role, not its location

---

## 📚 5. TLS 1.2 vs TLS 1.3

| Feature | TLS 1.2 | TLS 1.3 |
|---|---|---|
| Handshake RTTs | 2 | 1 |
| Key exchange | RSA (no FS), DHE, ECDHE | ECDHE or DHE only (RSA removed) |
| Forward secrecy | Optional | Mandatory |
| Cipher suites | Many (including RC4, 3DES, CBC) | Only 5 AEAD suites |
| Certificate in clear | Yes (before ChangeCipherSpec) | No (encrypted from ServerHello) |
| Downgrade protection | Weak | Strong (version negotiation in `supported_versions`) |
| 0-RTT | No (TLS False Start ≠ same) | Yes (PSK early data) |
| SNI encryption | No | Encrypted ClientHello (ECH, optional) |

**TLS 1.2 deprecation**: RFC 8996 (2021) deprecates TLS 1.0 and 1.1. PCI DSS 4.0 requires TLS 1.2+ for payment card systems. Many CDNs and browsers now default to TLS 1.2 minimum; TLS 1.3 preferred.

---

## 🛠️ 6. Worked Example — Inspecting a TLS 1.3 Handshake

```bash
# Connect to a server and observe TLS 1.3 negotiation
openssl s_client -connect cloudflare.com:443 -tls1_3 -state 2>&1 | head -40
# SSL_connect:before SSL initialization
# SSL_connect:SSLv3/TLS write client hello
# SSL_connect:SSLv3/TLS read server hello
# SSL_connect:TLSv1.3 read encrypted extensions
# SSL_connect:TLSv1.3 read certificate
# SSL_connect:TLSv1.3 read server certificate verify
# SSL_connect:TLSv1.3 read finished
# SSL_connect:SSLv3/TLS write change cipher spec
# SSL_connect:TLSv1.3 write client certificate verify
# SSL_connect:SSLv3/TLS write finished

# View the certificate chain
openssl s_client -connect cloudflare.com:443 -showcerts < /dev/null 2>/dev/null | \
  openssl x509 -noout -text | grep -E "Subject:|Issuer:|SAN|Not"

# Verify a certificate chain manually
openssl verify -CAfile root.pem -untrusted intermediate.pem leaf.pem
```

Use [tls13.xargs.org](https://tls13.xargs.org/) for a byte-by-byte interactive walkthrough of a real TLS 1.3 connection — it shows exactly what each byte means in every handshake message.

---

## ⚠️ 7. Common Misconceptions

- **"HTTPS means the site is trustworthy."** HTTPS means the connection is encrypted and the certificate's domain matches. It says nothing about whether the site owner is trustworthy or whether the content is legitimate. Phishing sites use valid TLS certs.
- **"TLS is slow."** TLS 1.3 adds ~0.5–1ms on LAN, ~20–50ms WAN (RTT + crypto). The crypto itself (AES-GCM-128 with hardware acceleration) processes at 10+ Gbit/s on modern CPUs. The latency is the round trip, not the cipher.
- **"Self-signed certificates are fine for internal services."** They eliminate eavesdropping but don't provide authentication unless the client explicitly trusts the cert. In a service mesh, use SPIFFE/SPIRE for proper workload identity instead.
- **"Certificate pinning is always good."** Pinning (hardcoding a cert or public key in an app) prevents MITM but causes outages when the cert rotates without updating the pin. Use SPIFFE for service mesh; use HPKP header (deprecated) or CT monitoring for public sites.
- **"0-RTT is safe for POST requests."** It is not. Only use 0-RTT for idempotent reads.

---

## 🔗 8. Cross-Links & Further Reading

### Internal
- [17.3 - TCP & UDP Deep Dive](17.3---TCP-&-UDP-Deep-Dive) — TLS runs over TCP (adds 1 RTT to TCP's 1 RTT)
- [3 (QUIC)](3-(QUIC)) — QUIC has TLS 1.3 built-in
- [17.7 - gRPC, Protocol Buffers & Service Mesh](17.7---gRPC,-Protocol-Buffers-&-Service-Mesh) — mTLS in Istio/Linkerd
- [Subject_Plan](Subject_Plan) — PKI security, certificate attacks, CT

### External
- [RFC 8446 — TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446)
- [tls13.xargs.org — Byte-level TLS 1.3 walkthrough](https://tls13.xargs.org/)
- [Cloudflare — A Detailed Look at RFC 8446 (TLS 1.3)](https://blog.cloudflare.com/rfc-8446-aka-tls-1-3/)
- [The Illustrated TLS 1.3 Connection (xargs.org)](https://tls13.xargs.org/)
- [SPIFFE/SPIRE documentation](https://spiffe.io/)
- [Let's Encrypt — Certificate Authority overview](https://letsencrypt.org/how-it-works/)
- [Practical Networking — TLS series](https://www.practicalnetworking.net/)
- [Hussein Nasser — TLS 1.3 deep dive (YouTube)](https://www.youtube.com/@hnasr)

---

*Next: [3 (QUIC)](3-(QUIC)) — The application protocols that run over TLS.*
