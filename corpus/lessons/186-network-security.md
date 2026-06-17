---
title: "18.6 — Network Security"
subject: "Cybersecurity"
catalog: advanced
audience_tier: higher-education
chapter: "18.6"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 18.6 — Network Security

> *"The perimeter is dead. Every request is hostile until proven otherwise."*

Network security in 2026 is no longer "a firewall plus VPN." It is layered: TLS 1.3 with PQC-ready handshakes, browser-side controls (CSP / HSTS / SameSite), zero-trust identity at the edge, mTLS between services, and rate-limit / WAF / DDoS scrubbing in front. This chapter installs the defaults you should never deviate from without a reason.

---

## 🎯 Learning Objectives

1. Configure TLS 1.3 end-to-end with HSTS preload.
2. Author a strict, nonce-based **Content Security Policy**.
3. Set sane CORS, cookie, and SameSite policies.
4. Design rate-limiting that defends both abuse and cost.
5. Place a WAF and tune its rules without breaking real traffic.
6. Stand up zero-trust access (BeyondCorp model) for internal apps.
7. Configure service-mesh mTLS for east-west traffic.
8. Defend against L3/L4 DDoS via upstream scrubbing.

---

## 🖼️ Visual Anchor

> *Picture / video reference (external):*
> - 📺 [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
> - 📺 [Cloudflare Learning Center](https://www.cloudflare.com/learning/)
> - 📺 [Istio security overview](https://istio.io/latest/docs/concepts/security/)
> - 📺 [Google BeyondCorp papers](https://cloud.google.com/beyondcorp)

![sec-18__fig2](sec-18__fig2.svg)
*Fig 2: Man-in-the-Middle Attack Flow*

![sec-18__fig4](sec-18__fig4.svg)
*Fig 4: Web Application Firewall (WAF) blocking malicious traffic*

---

## 📚 1. TLS 1.3 — The Floor, Not the Ceiling

TLS 1.3 dropped weak primitives (RC4, 3DES, MD5, SHA-1, RSA key transport, static DH) and slimmed the handshake. Modern config (Mozilla "intermediate" / "modern" baseline):

- Cipher suites: `TLS_AES_256_GCM_SHA384`, `TLS_CHACHA20_POLY1305_SHA256`, `TLS_AES_128_GCM_SHA256`.
- Key exchange: X25519 (now hybrid X25519+Kyber where supported — see [18.4 - Cryptography for Developers](18.4---Cryptography-for-Developers)).
- Certificates: ECDSA P-256 (Ed25519 once your stack supports it).
- ALPN: `h2` and `http/1.1`.
- OCSP stapling on, session tickets rotated.

**HSTS** with preload tells browsers to *only* visit your domain over HTTPS:

```http
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
```

Submit to the [HSTS preload list](https://hstspreload.org/) once you're confident no plaintext path remains.

---

## 🛡️ 2. Content Security Policy — Nonce-Based, Strict

A loose CSP is worse than none — false reassurance. Aim for **strict** CSP with per-request nonces:

```http
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'nonce-rAnDoM' 'strict-dynamic';
  style-src 'self' 'nonce-rAnDoM';
  img-src   'self' data: https:;
  connect-src 'self' https://api.example.com;
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';
  upgrade-insecure-requests;
  report-to csp-endpoint;
```

`'strict-dynamic'` lets a nonce'd script load further scripts without listing each one. Pair with **Trusted Types** (`require-trusted-types-for 'script'`) to kill DOM-XSS sinks.

Other browser-side headers worth setting:

```http
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
X-Content-Type-Options: nosniff
```

---

## 🍪 3. Cookies & CORS Done Right

Session cookies:

```
Set-Cookie: __Host-session=...; Secure; HttpOnly; Path=/; SameSite=Strict; Max-Age=3600
```

The `__Host-` prefix forbids `Domain=` and requires `Path=/` + `Secure`, eliminating cookie-tossing classes of attacks.

CORS: default to `Access-Control-Allow-Origin` matching a strict allow-list, never `*` for credentialed requests. **Never** reflect the `Origin` header without checking it against the allow-list — a classic mistake.

---

## 🚦 4. Rate Limiting & Abuse Cost

Rate limits defend three things at once: brute force, scraping, and **bill-shock**. Put them in three places:

- **Edge** — global, per-IP, per-route (CDN/WAF: Cloudflare, AWS WAF, Akamai).
- **App gateway** — per-API-key, per-tenant, per-feature.
- **App** — per-user, per-action, with token-bucket or leaky-bucket semantics.

```nginx
# Token-bucket example with nginx
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
location /login {
    limit_req zone=login burst=10 nodelay;
}
```

For LLM-backed endpoints add a **cost limit** in addition to a rate limit (tokens-per-minute per tenant) — see [18.8 - AI Security & Adversarial ML](18.8---AI-Security-&-Adversarial-ML).

---

## 🪖 5. Web Application Firewall

A WAF inspects request semantics for known bad shapes (SQLi, XSS, RCE patterns, OWASP CRS rule set). Use one — Cloudflare, AWS WAF, Azure Front Door, or open-source ModSecurity + OWASP CRS. Tune by:
1. Run in **detect** mode for two weeks; collect false-positive baseline.
2. Whitelist known-safe paths (file uploads, large bodies).
3. Promote to **block**; monitor 4xx spike.
4. Add per-route custom rules for your specific abuse patterns.

WAFs do not replace input validation — they buy you time and dampen background noise.

---

## 🌐 6. Zero Trust (BeyondCorp Model)

The core idea: **identity + device posture is the perimeter**, not the network. Every request, from anywhere, is authenticated + authorized as if it came from the public internet. The Google BeyondCorp papers describe the original implementation; modern incarnations include Cloudflare Access, Tailscale, and AWS Verified Access.

Concrete shifts when adopting it:

- VPNs become a fallback, not a primary control.
- Internal apps gain SSO + device posture checks at the proxy.
- Trust evaluation considers user, device, time, location, and behavioral signals — not just an IP.

---

## 🕸️ 7. Service-Mesh mTLS — East-West Defense

Inside the cluster, every service-to-service call presents a workload identity (SPIFFE/SPIRE) and a short-lived cert that the mesh rotates automatically. The mesh refuses unauthenticated traffic; an attacker who lands a pod still cannot call Payments without a valid identity.

```yaml
# Linkerd: mTLS is on by default; enforce with a policy
apiVersion: policy.linkerd.io/v1beta1
kind: Server
metadata: { name: payments-grpc, namespace: payments }
spec:
  podSelector: { matchLabels: { app: payments } }
  port: 9000
  proxyProtocol: gRPC
---
apiVersion: policy.linkerd.io/v1beta1
kind: AuthorizationPolicy
metadata: { name: payments-auth, namespace: payments }
spec:
  targetRef: { kind: Server, name: payments-grpc }
  requiredAuthenticationRefs:
    - kind: MeshTLSAuthentication
      name: orders-only
```

This composes with **NetworkPolicies** at L3/L4 (see [18.7 - Cloud & Container Security](18.7---Cloud-&-Container-Security)) — defense in depth, not OR.

---

## 🌪️ 8. DDoS Mitigation

L3/L4 floods are an ISP / CDN problem. Three levers:
- **Anycast scrubbing** at a provider (Cloudflare, AWS Shield Advanced, Google Cloud Armor).
- **Auto-scaling** for elastic capacity.
- **Connection limits** + **cookie-challenge** at the edge to filter dumb bot floods.

L7 (application) DDoS is the harder problem — high-cost endpoints (search, AI, exports) need *cost* limits in addition to *rate* limits.

---

## 🛠️ 9. Worked Example — Hardening an Existing Web App in One Afternoon

1. Move all traffic to **HTTPS-only**; redirect 301 from HTTP. Add **HSTS** (`max-age=63072000; includeSubDomains; preload`) once you're sure.
2. Generate a **Mozilla Modern** TLS profile via [Mozilla SSL Config Generator](https://ssl-config.mozilla.org/) and apply to the load balancer.
3. Add the **header set** above (CSP nonce-based, Trusted Types, Referrer-Policy, Permissions-Policy, X-Content-Type-Options).
4. Convert any session cookie to `__Host-` + `Secure` + `HttpOnly` + `SameSite=Strict`.
5. Lock CORS to a specific allow-list per environment.
6. Add **edge rate limit** at the CDN: 100 req/min/IP general, 10 req/min/IP for `/login`, `/signup`, `/forgot`.
7. Deploy **WAF** in detect mode; promote to block in a week.
8. Submit to **HSTS preload** once stable.
9. Confirm with `testssl.sh` (TLS), [Mozilla Observatory](https://observatory.mozilla.org/) (HTTP headers), and [Security Headers](https://securityheaders.com/).

Roughly four hours of work that pushes most automated scanners off your service.

---

## 🔗 10. Cross-links & Further Reading

### Internal
- [18.4 - Cryptography for Developers](18.4---Cryptography-for-Developers) — TLS primitives + PQC migration
- [18.7 - Cloud & Container Security](18.7---Cloud-&-Container-Security) — NetworkPolicies and runtime
- [1.11 - Computer Networks Essentials](1.11---Computer-Networks-Essentials) — TCP/IP foundations
- [Subject_Plan](Subject_Plan) — sibling track on operations
- [Subject_Plan](Subject_Plan) — sibling track on architecture

### External
- [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
- [Mozilla SSL Config Generator](https://ssl-config.mozilla.org/)
- [HSTS Preload list](https://hstspreload.org/)
- [Mozilla Observatory](https://observatory.mozilla.org/)
- [Security Headers](https://securityheaders.com/)
- [OWASP CSP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
- [Cloudflare Learning Center](https://www.cloudflare.com/learning/)
- [Istio security](https://istio.io/latest/docs/concepts/security/) and [Linkerd policy](https://linkerd.io/2/features/server-policy/)
- [Google BeyondCorp](https://cloud.google.com/beyondcorp)

---

## ⚠️ 11. Common Misconceptions

- **"TLS handles everything."** TLS protects the wire; it does not protect against XSS, CSRF, SSRF, IDOR, or supply-chain. It's a floor.
- **"`unsafe-inline` in CSP is fine 'for now'."** Inline scripts are exactly what XSS exploits. Use nonces or hashes.
- **"`Access-Control-Allow-Origin: *` is convenient."** Convenient — and forbidden when `Access-Control-Allow-Credentials: true`. Use an allow-list.
- **"VPN = secure."** A VPN authenticates the *device* once; zero-trust authenticates *every request*.
- **"DDoS is just bigger pipes."** L7 attacks (search-heavy, AI-heavy endpoints) require cost-aware rate limiting, not just bandwidth.

---

*Next: [18.7 - Cloud & Container Security](18.7---Cloud-&-Container-Security) — controls inside the cluster.*
