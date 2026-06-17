# XPRIZE / Hacker.fund Hackathon — Gap Analysis & Plan

Working doc. Status as of 2026-06-10. Nothing here is built unless marked ✅.

---

## 1. Snapshot

- **Window:** revenue scored by month May–Aug 2026. Effective runway today → **~11 weeks (now to Aug 31).**
- **Primary category:** Education & Human Potential.
- **Monetized wedge:** adult professional / coding tracks (fastest credit cards; K-12 is a summer gamble).
- **Possible 2nd submission:** Professional Services Access (interview/career prep angle) — only if it's cheap to split. Decide later.
- **Brand:** moving axon → **Mneme Labs** (Mneme = muse of memory; fits a learning product).
- **Our edge:** existing corpus (900+ lessons), a working content-commerce pattern (bmx4beginners: how-to → product → connected site), bulk AI content production, live shop/Stripe on axon, and the dev skillset to ship the AI layer. Most of the ~12k entrants won't produce a dollar of real revenue.

### Three hard gates (pass/fail-ish)
1. **New project only.** Corpus + scaffolding pre-exist and are owned by Bill → declare as pre-existing assets; the *business + AI-operated layer* is the new work built in-window. The learning app itself was built during the period.
2. **Gemini API:** ≥1 LLM call in the **deployed app** at runtime (dev tools like Antigravity/Codex do NOT count — building with them ≠ the running product calling Gemini).
3. **Real arms-length revenue** by Aug 31; related-party / pre-existing-customer revenue reported separately.

---

## 2. Requirement-by-requirement gap table

| Requirement | What it demands | Where we are | Gap → Action |
|---|---|---|---|
| New project / IP | Built in-window; explain pre-existing work; own all IP | Learning app built in-window ✅; corpus pre-exists (owned) | Write the "pre-existing work" disclosure paragraph |
| Category | Pick one | Education (primary) | Lock it; optional 2nd entry decision |
| **Gemini in deployed app** | ≥1 runtime Gemini call serving users | `llm-adapter` has a `hosted` slot, no Gemini wired; tutor is mocked on frontend | Wire 1 feature (tutor answer) to Gemini API in prod |
| Google Cloud product | Project runs on ≥1 GCP product | None yet | Gemini API / Vertex satisfies this via the above |
| Repo | Public, or private + shared w/ testing@devpost.com & judging@hacker.fund | Local only; learning app has a `.git` | Private repo per project; add the two judge emails |
| Live testing access | Deployed, free, creds if private | Nothing deployed | Vercel the site + app(s); seed test creds |
| Text description | How it meets reqs + category relevance | — | Draft from this doc |
| Demo video | <3 min, public YouTube, shows it running | — | Film once flagship is live; repurpose into shorts |
| **Revenue evidence** | Total + by month (May/Jun/Jul/Aug) + costs + marketing spend (even if $0) | axon shop/Stripe live (per Bill, unverified) | Confirm Stripe live; route Mneme offer through it; keep monthly export |
| **User evidence** | # users, who they are, testimonials; related-party shown separately | None yet | Capture signups + collect testimonials; segregate audience-sourced |
| **Product-running evidence** | Agent execution logs, API usage, dashboards — "playbooks running continuously" | The old AI ops (inbox/email check) was pulled over Azure cost | Rebuild ops as cron-fired + logged (see §4) |
| Corporate ID | If an org | Bill has entities? | Provide if entering as org |

---

## 3. Judging criteria → what scores

Equal weight, all three:
- **Business Viability** → real revenue in-window + sustainable model. *Risk #1: arms-length revenue in 11 weeks.*
- **AI-Native Operations** → AI runs the business, in prod, executing decisions, with logs. *Our differentiator if we capture evidence.*
- **Category Impact** → the product meaningfully moves the needle in Education.

---

## 4. The AI-Native Operations layer (the "AI-ran business")

**Definition that counts:** AI doing the company's operational work + decisions, on a recurring schedule, with logs. NOT AI-in-the-product.

**Cost-safe architecture (fixes the Azure-bill problem):**
- Scheduled jobs (cron / Cloud Scheduler) that **wake → do task → call API → write a log line → sleep.**
- Pay-per-call models, not always-on compute. "Continuously" = *recurring*, not 24/7.
- Tooling is agnostic (GPT / Antigravity / open-source) — the ops layer does NOT have to be Gemini; only the in-app gate does.

**Playbooks to run (pick 2, keep humans approving):**
1. **Support agent** — reads inbox, drafts/sends replies, escalates edge cases. (Bill had this; rebuild on cron.)
2. **Content/marketing agent** — generates video descriptions, shorts metadata, landing copy; queues posts.
3. *(Optional)* **Content-ops agent** — reads the subject-gap manifest, decides next lesson/product to produce, drafts it for approval.

**Dropped:** Stripe "agent" — webhooks + receipts already automate this; no agent needed.

**Evidence to instrument from day one:** timestamped log per run (what fired, what it decided, what it did) → screenshot-able dashboard.

---

## 5. Human vs AI split (this IS the required narrative)

| Function | AI does | Human (Bill) does |
|---|---|---|
| Content production | Generates lessons, descriptions, repurposes long→shorts | Records demos, approves, text-based edits |
| Support | Reads/drafts/sends, escalates | Handles escalations |
| Marketing | Drafts + schedules posts across accounts | Strategy, on-camera |
| Product (in-app) | Tutor answers via Gemini, grading | Curriculum design |
| Payments | Stripe webhooks (automated, not "AI") | Refund/edge calls |
| Decisions logged | What to produce next, support triage | Final approvals |

---

## 6. Build / launch sequence (critical path only)

1. **Repos:** private repo per project, add judge emails.
2. **Deploy:** Vercel the site + flagship app → satisfies live-testing access. Get indexed (SEO = slow compounding, not counted on for in-window revenue).
3. **Gemini gate:** wire tutor answer → Gemini API in prod (clears API + GCP gates).
4. **Revenue funnel:** Mneme adult-tracks offer → axon shop (Stripe) live → confirm a real purchase path.
5. **Ops playbooks:** rebuild support + content/marketing as cron-fired + logged.
6. **Evidence capture:** logging/dashboard wired before launch, not after.
7. **Content engine:** hammer how-to + product content on AI/LinkedIn/YT/FB/IG (Bill's lane). Target: clients July→Aug.
8. **Submission assets:** video, narrative (from §5), revenue export, user evidence.

---

## 7. Open decisions (for next conversation)

- **How many apps to submit/deploy?** More = more content, but each must stay live + testable for judges, and each adds maintenance. *Recommendation: one flagship gets the full treatment (Gemini + revenue + ops); others stay lighter content pieces, not separate submissions, unless trivially cheap.*
- **Second submission (Professional Services)?** Only if it's a cheap split of the same machine.
- **Discord layer** — include now or park? Could count as user/community evidence; park unless it's near-free to stand up.
- **Final name** — Mneme Labs vs alternative.
- **Entering as individual or org** (corporate ID requirement).
- **Confirm:** is axon's Stripe shop currently taking live payments? (Decides real runway.) — Bill to verify.

---

## 8. Biggest risks (ranked)

1. **Arms-length revenue in 11 weeks** — the whole thing hinges here. Content engine is the only realistic lever in time.
2. **Evidence discipline** — if ops aren't logged, AI-Native Operations score collapses regardless of what's running.
3. **Focus/fragmentation** — quarantine the from-scratch LLM build and brand polish away from the contest critical path; they're content B-roll, not revenue.
