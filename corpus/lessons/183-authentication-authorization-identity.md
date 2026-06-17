---
title: "18.3 — Authentication, Authorization & Identity"
subject: "Cybersecurity"
catalog: advanced
audience_tier: higher-education
chapter: "18.3"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 18.3 — Authentication, Authorization & Identity

> *"Authentication answers 'who are you?'. Authorization answers 'what can you do?'. Identity is the discipline of getting both right at scale, for humans, machines, and now agents."*

Identity in 2026 is going through three shifts at once: passwords are dying (passkeys are mainstream), bearer tokens are losing ground to **DPoP / mTLS-bound tokens**, and a brand-new actor — the **AI agent** — needs scoped, observable, revocable credentials of its own.

The numbers behind the passkey shift: the FIDO Alliance's State of Passkeys 2026 report describes roughly 5 billion passkeys in active use, consumer awareness near 90%, and adoption around 75% among consumers who recognize them. NIST's SP 800-63-4 has retired SMS one-time-passcodes from acceptable AAL2 authenticators. (paraphrased from [fidoalliance.org](https://fidoalliance.org/the-state-of-passkeys-2026-global-consumer-and-workforce-report/) · [guptadeepak.com passwordless guide](https://guptadeepak.com/ciam-compass/guides/passwordless-authentication/))

> Source rephrased for compliance: [fidoalliance.org](https://fidoalliance.org/the-state-of-passkeys-2026-global-consumer-and-workforce-report/) · [guptadeepak.com](https://guptadeepak.com/ciam-compass/guides/passwordless-authentication/).

---

## 🎯 Learning Objectives

1. Distinguish authentication, authorization, and identity-federation.
2. Choose the right OAuth 2.1 flow (Authorization-Code-with-PKCE, Client-Credentials, Device-Code) for a given app.
3. Implement OpenID Connect on top of OAuth 2.1 and validate ID tokens correctly.
4. Decide between JWT and server-side sessions for a given use case.
5. Set up mTLS for service-to-service authentication.
6. Ship a passkey / WebAuthn registration + assertion flow.
7. Pick a managed identity provider (Clerk, Auth0, Supabase Auth, WorkOS) and integrate it.
8. Treat AI agents as identities — scoped tokens, audit logs, revocation.

---

## 🖼️ Visual Anchor

> *Picture / video reference (external):*
> - 📺 [OAuth 2.1 specification](https://oauth.net/2.1/)
> - 📺 [WebAuthn specification](https://www.w3.org/TR/webauthn-3/)
> - 📺 [FIDO Alliance — State of Passkeys 2026](https://fidoalliance.org/the-state-of-passkeys-2026-global-consumer-and-workforce-report/)
> - 📺 [NIST SP 800-63-4 Digital Identity Guidelines](https://pages.nist.gov/800-63-4/)
> - 📺 [PortSwigger — OAuth 2.0 attacks (Academy)](https://portswigger.net/web-security/oauth)

---

## 📚 1. Definitions That Matter

| Term | Meaning |
|---|---|
| **Authentication (AuthN)** | Proof of identity — "the bearer is the user" |
| **Authorization (AuthZ)** | Permission decision — "this user may perform this action on this resource" |
| **Federation** | Trusting another system's authentication claims (SSO, social login, SAML, OIDC) |
| **Assurance Level (NIST 800-63-4)** | IAL = enrollment proofing; AAL = authentication strength; FAL = federation strength |
| **Credential** | Something the user has/knows/is — password, passkey, OTP, certificate |
| **Token** | A short-lived bearer or sender-constrained artifact representing an authenticated session |
| **Identity provider (IdP)** | The service that issues identity claims (Auth0, Okta, Entra ID, Google, Apple) |

---

## 🔁 2. OAuth 2.1 in Practice

OAuth 2.1 consolidates the OAuth 2.0 ecosystem and bakes in modern advice. Key changes from 2.0:

- **PKCE is mandatory** for all auth-code flows (public + confidential clients).
- **Implicit flow is removed.**
- **Resource Owner Password Credentials grant is removed.**
- **Refresh-token rotation** is the default expectation.
- Bearer tokens **must not** be passed in URL query strings.

The flows you actually use:

| Flow | When |
|---|---|
| Authorization Code + PKCE | Web apps, SPAs, mobile apps (almost always this) |
| Client Credentials | Service-to-service when no user is involved |
| Device Code | TVs, CLIs, IoT — devices without browsers |
| Refresh Token (rotated) | Renewing an access token |

OIDC sits on top of OAuth 2.1 and adds an **ID token** (a signed JWT describing the user). The ID token is for *your* app; the access token is for *resource servers*.

---

## 🪪 3. JWT vs Server-Side Sessions

| Property | JWT | Session |
|---|---|---|
| Storage | Client | Server |
| Revocation | Hard (need denylist + short TTL) | Easy (delete server row) |
| Scaling | Trivial | Needs sticky / shared store |
| Best for | Cross-service authn, machine-to-machine | Browser apps with single backend |

**JWT pitfalls** (almost all of these are A07 in [18.2 - OWASP Top 10 2025 Deep Dive](18.2---OWASP-Top-10-2025-Deep-Dive)):
- Accepting `"alg": "none"`.
- Confusing `RS256` and `HS256` (RSA pubkey fed as HMAC secret = forge anything).
- Not validating `aud`, `iss`, `exp`, `nbf`.
- Storing access tokens in `localStorage` (XSS-readable). Prefer **HTTP-only, Secure, SameSite=Strict** cookies for browser sessions.

The 2026 best practice is **DPoP** (Demonstrating Proof of Possession) or **mTLS-bound tokens** to stop bearer-token replay.

---

## 🔒 4. mTLS for Service-to-Service

In zero-trust architectures (see [18.6 - Network Security](18.6---Network-Security)), *every* service-to-service call presents a client certificate. The mesh (Istio, Linkerd) issues short-lived workload identities (SPIFFE/SPIRE), rotates them automatically, and refuses unauthenticated traffic by default.

```yaml
# Istio PeerAuthentication: enforce STRICT mTLS in a namespace
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: payments
spec:
  mtls:
    mode: STRICT
```

This kills entire bug classes: an attacker who lands in your network *cannot* call the payments service without a valid workload cert.

---

## 🗝️ 5. Passkeys / WebAuthn

A **passkey** is a FIDO2 credential — a public/private keypair where the private key lives on a hardware authenticator (TPM, secure enclave, security key) and *never* leaves the device. It is phishing-resistant by design (the relying party id is bound into the assertion).

### Registration (excerpt)
```js
const cred = await navigator.credentials.create({
  publicKey: {
    rp:   { id: "example.com", name: "Example" },
    user: { id: userIdBytes, name: email, displayName: name },
    challenge: serverChallenge,
    pubKeyCredParams: [{ type: "public-key", alg: -7 }, { type: "public-key", alg: -257 }],
    authenticatorSelection: {
      residentKey: "required",
      userVerification: "required"
    },
    attestation: "none"
  }
});
// Send cred.id + cred.response.attestationObject to your server, verify, store credentialId+publicKey.
```

### Why it kills phishing
The browser refuses to sign for a domain that doesn't match `rp.id`. There is no shared secret to phish. SMS OTP — long the default fallback — is no longer accepted as adequate AAL2 per NIST SP 800-63-4. (paraphrased from [pages.nist.gov/800-63-4](https://pages.nist.gov/800-63-4/) · [guptadeepak.com](https://guptadeepak.com/ciam-compass/guides/passwordless-authentication/))

> Source rephrased for compliance: [pages.nist.gov/800-63-4](https://pages.nist.gov/800-63-4/).

---

## 🛠️ 6. Managed Providers — Buy vs Build

For most products in 2026, **buy**. The matrix:

| Provider | Sweet spot | Free tier | Notes |
|---|---|---|---|
| **Clerk** | Modern web/mobile dev experience, drop-in components | Generous | Best DX, Next.js / React-first |
| **Auth0** (Okta) | Enterprise SSO, large feature surface | Limited | Bulletproof, can be expensive at scale |
| **Supabase Auth** | Bundled with Postgres + RLS | Generous | Best when DB and auth share a story |
| **WorkOS** | Enterprise SSO/SCIM you sell into B2B | Free for SSO | Add it when your first enterprise asks for SAML |
| **Entra ID (Azure AD)** | Microsoft 365 shops | Bundled | Default if your customers live in Microsoft |
| **Google Identity Platform / Firebase Auth** | Google-cloud apps, mobile | Generous | Quick start, less custom flexibility |

The cost of rolling your own includes lockouts, password resets, MFA logistics, breach notifications, abuse handling, and deliverability. None of those are in your competitive moat.

---

## 🤖 7. AI Agents as Identities

A 2026-only shift: every autonomous agent (Slack bot, support agent, IDE assistant) needs **its own identity** with a scoped role, an audit trail, and a revocation control. Treat agents like service accounts:
- Issue them short-lived credentials (OAuth client_credentials with narrow scopes).
- Bind tool calls to a tenant context — see [18.8 - AI Security & Adversarial ML](18.8---AI-Security-&-Adversarial-ML).
- Log every tool call with a tamper-evident audit trail (A09 in [18.2 - OWASP Top 10 2025 Deep Dive](18.2---OWASP-Top-10-2025-Deep-Dive)).
- Revoke on anomaly — agents should be cheaper to kill than humans.

---

## 🧪 8. Worked Example — Adding Passkeys to an Existing Email/Password App

1. **Library** — install `@simplewebauthn/server` (Node) or `webauthn-rs` (Rust) or `py_webauthn` (Python). Don't hand-roll.
2. **DB** — add a `webauthn_credentials` table: `(id, user_id, credential_id, public_key, counter, transports, created_at, last_used_at, name)`.
3. **Registration endpoint** — generate a challenge, store it in a short-lived server cache keyed on session, send `PublicKeyCredentialCreationOptions`. On callback, verify attestation, persist the credential.
4. **Login endpoint** — generate a challenge, send `PublicKeyCredentialRequestOptions` (with `allowCredentials` from DB), verify on callback. Increment counter — a regression is a clone signal.
5. **UX** — keep email/password as fallback for at-most a year. Surface passkey enrollment after first login. Do not allow downgrading from passkey-only without recovery.
6. **Recovery** — passkeys + email magic-link backup OR passkeys + multiple device enrollments. Avoid SMS-only recovery.
7. **Telemetry** — track passkey-vs-password ratio per release; aim for 50%+ within a quarter for active users.

The result: phishing-resistant authn, no password storage, no SMS bills, and AAL2 compliance.

---

## 🔗 9. Cross-links & Further Reading

### Internal
- [18.2 - OWASP Top 10 2025 Deep Dive](18.2---OWASP-Top-10-2025-Deep-Dive) — A07 deep links here
- [18.4 - Cryptography for Developers](18.4---Cryptography-for-Developers) — JWT signing + the primitives behind WebAuthn
- [18.6 - Network Security](18.6---Network-Security) — mTLS in service mesh
- [18.7 - Cloud & Container Security](18.7---Cloud-&-Container-Security) — workload identity (SPIFFE/SPIRE)
- [18.8 - AI Security & Adversarial ML](18.8---AI-Security-&-Adversarial-ML) — agent identity model

### External
- [OAuth 2.1 spec](https://oauth.net/2.1/)
- [OIDC core](https://openid.net/specs/openid-connect-core-1_0.html)
- [WebAuthn Level 3](https://www.w3.org/TR/webauthn-3/)
- [FIDO Alliance learn](https://fidoalliance.org/learn-passkeys/)
- [NIST SP 800-63-4](https://pages.nist.gov/800-63-4/)
- [Clerk docs](https://clerk.com/docs)
- [Auth0 docs](https://auth0.com/docs)
- [Supabase Auth docs](https://supabase.com/docs/guides/auth)
- [WorkOS docs](https://workos.com/docs)
- [PortSwigger OAuth labs](https://portswigger.net/web-security/oauth)
- [SPIFFE/SPIRE](https://spiffe.io/) — workload identity

---

## ⚠️ 10. Common Misconceptions

- **"JWTs are stateless so I never need to revoke."** Reality: short TTLs + a denylist + refresh-token rotation are how you simulate revocation. Long-lived JWTs are a footgun.
- **"Passkeys are just MFA."** Passkeys can be **single-factor and phishing-resistant** — they replace passwords + SMS OTP, not just one of them.
- **"OIDC and OAuth are interchangeable."** OAuth gives you an *access token* for an API. OIDC gives you an *ID token* for your app. Use the right one.
- **"SAML is dead."** SAML still wins enterprise SSO for legacy IT. WorkOS and Auth0 abstract it; you don't have to like it, you do have to support it.
- **"`localStorage` is fine for tokens."** It is XSS-readable. Use HTTP-only cookies + SameSite=Strict + CSRF tokens, or move to mTLS-/DPoP-bound tokens.

---

*Next: [18.4 - Cryptography for Developers](18.4---Cryptography-for-Developers) — the primitives that make all of the above possible.*
