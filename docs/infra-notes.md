# Infrastructure & Database Requirements

Updated 2026-06-18. Principle: minimal footprint, spend nothing you don't need yet.

## The box
- **Old MacBook Pro (Lubuntu) = the database server.** Its job: run Postgres to **collect clients/leads and persist app data**, so we DON'T pay for a cloud DB (Supabase keeps pausing) until it's economically worth it.
- Can also run Ollama (free local tutor) on the side. NOT for content/filming.
- Expose publicly when needed via Cloudflare Tunnel (free, no static IP). VPS only when revenue justifies 24/7.

## What we actually need a database for

### Tier 1 — NEEDED NOW: lead/client collection (serves ALL sites)
One small Postgres, one shared schema, used by every site (learning sites, nepa-ai, bmx4beginners, the sandblasting lead-gen site, the shop). The immediate value: capture the leads you're already generating (e.g., the $18k sandblasting lead).
- **contacts** — id, email, name, phone, source_site, message, tags[], created_at
  (every inbound lead/inquiry from any site; `source_site` tells them apart)
- **subscribers** — id, email, source_site, status (active/unsub), created_at
  (newsletter / "notify me" / waitlist)
- **quote_requests** — id, contact_id, service, details (job size, location), status, created_at
  (service sites like sandblasting — turns a form into a tracked lead)

That's it for now. Three tables cover lead capture across the whole portfolio.

### Tier 2 — learning-app, once it has real users (schema mostly already exists in services/api/migrations)
- **users** — id, email, password_hash, created_at
- **progress** — user_id, lesson_slug, subject_slug, stage (read/listen/write/code/handwrite), completed_at
- **grasp_scores** — user_id, lesson_slug, score, flagged_for_review
- **reviews** — user_id, lesson_slug, due_at, interval (spaced repetition)
- **subscriptions** — user_id, stripe_customer_id, plan, status (for paid tracks)
- (optional) **tutor_logs** — user_id, lesson_slug, question, answer, created_at

### Tier 3 — commerce / shop (axon/mneme)
- Stripe is the source of truth. Mirror only what you query: **orders** (stripe_id, customer email, product, amount, status, created_at). Most of this can come from Stripe webhooks → contacts/orders.

### Per-project summary
| Project | DB need |
|---|---|
| content-site | Tier 1 only (email capture / notify-me). Otherwise static. |
| learning-app | Tier 1 + Tier 2 (accounts, progress, reviews, subscriptions). The real DB consumer. |
| spatial-calculator | ~None. Stateless. (Optional: save expressions → could reuse Tier 1.) |
| other sites (nepa-ai, bmx4beginners, sandblasting, shop) | Tier 1 (contacts/quotes/subscribers) + Tier 3 for the shop. |

## Takeaway
The MacBook Postgres should stand up **Tier 1 first** — it immediately serves every site (including the sandblasting lead) for $0. Tier 2 plugs in when the learning-app gets real users (schema already drafted in `services/api/migrations`). One box, multiple schemas, no cloud bill.

## Status (today)
- Monorepo pushed: github.com/bkennedyshit/learning-platform (private).
- content-site production build verified (640 lessons + 80 subjects, fully static).
- Tutor: provider-switchable (local Ollama / Gemini), retry on transient errors.
- Gemini: pay outstanding bill + small budget → unblocks paid tier.
