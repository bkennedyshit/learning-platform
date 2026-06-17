---
title: "39.7 — Legal Basics for Founders"
subject: "Business & Entrepreneurship"
catalog: advanced
audience_tier: higher-education
chapter: "39.7"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 39.7 — Legal Basics for Founders

> *"The goal is not to become a lawyer. The goal is to know enough to protect yourself, hire the right lawyers, and not sign things you don't understand."*

Legal issues are the most avoidable startup killers. A co-founder dispute without a vesting agreement, code owned by a former employer, an unclear contractor arrangement — these are landmines that detonate years after you step on them. This chapter gives you the vocabulary, the frameworks, and the checklists to stay safe.

> ⚠️ **Legal disclaimer:** This chapter is educational and informational only. It is not legal advice. For any specific legal situation — entity formation, contract review, equity structuring, IP disputes — consult a licensed attorney in your jurisdiction.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Choose between a **Delaware C-Corp and LLC** for your specific situation.
2. Explain why **IP assignment** is non-negotiable and how to implement it.
3. Understand the legal distinction between **contractor (1099) and employee (W-2)** and avoid misclassification.
4. Set up **vesting schedules** for co-founders and early employees.
5. Know what belongs in a **founder agreement** before you build anything together.
6. Understand the basic terms in a **contractor agreement** (work-for-hire, IP assignment, non-compete).
7. Create a **legal checklist** for the pre-fundraising state.

---

## 🖼️ Visual Anchor

![biz__33.7-fig1](biz__33.7-fig1.svg)

---

## 📚 1. Entity Structure — Delaware C-Corp vs LLC

### Definition 39.7.1 — Business Entity

A legal entity separates the business from you personally. Without one, you are personally liable for all debts and legal actions against the business. Forming an entity is almost always the right move before taking on customers, contractors, or investors.

### 1.1 The Main Options

| Entity type | Best for | Key characteristics |
|-------------|----------|---------------------|
| **Delaware C-Corp** | VC-backed startups, SaaS products, any company that might raise outside capital | Can issue multiple share classes; preferred by investors; Delaware courts are sophisticated; stock options (ISOs) for employees |
| **Delaware LLC** | Bootstrapped businesses, consulting, content brands, single-owner businesses | Pass-through taxation (profits taxed at personal rate); more flexible operating agreement; can't issue ISOs |
| **Wyoming LLC** | Privacy-first bootstrap (Wyoming has minimal disclosure requirements) | Similar to Delaware LLC; more privacy, less legal precedent |
| **S-Corp** | Small US businesses wanting to reduce self-employment taxes | Limited to 100 US shareholders, one class of stock; not compatible with VC investment |
| **Sole proprietorship** | Avoid — no liability protection | No protection; you are the business legally |

### 1.2 Delaware C-Corp: When and Why

If you intend to:
- Raise venture capital or angel investment
- Issue stock options to employees
- Have international founders or employees
- Eventually sell the company (acquisition)

...you **must** be a Delaware C-Corp. Investors (especially VCs) will require it. There's no "convert from LLC to C-Corp later" — it's possible but expensive and complicated.

**C-Corp taxation:** Unlike an LLC, a C-Corp is taxed at the corporate level, and dividends are taxed again at the personal level (double taxation). At startup scale, this rarely matters — you're reinvesting, not paying dividends. But it's a real cost at exit if you haven't structured correctly.

### 1.3 LLC: When It's the Right Choice

If you are:
- Building a bootstrapped SaaS (no VC plans)
- Running a consulting or productized service business
- Building a content brand (BMX YouTube, etc.)
- A solo founder with no plans to hire employees on equity

An LLC is simpler, cheaper, and more flexible. You can always form a separate C-Corp for a venture-backed product while keeping your LLC for other businesses.

### 1.4 Using Stripe Atlas for Entity Formation

Stripe Atlas forms Delaware C-Corps and LLCs for $500 + first year registered agent fee (~$100/yr). They handle:
- Filing with Delaware Secretary of State
- EIN application with the IRS
- Standard founder restricted stock agreements
- Standard IP assignment agreement

For a bootstrapped indie developer, Atlas is the fastest and cheapest route to a properly structured entity. — paraphrased from [stripe.com/atlas/guides](https://stripe.com/atlas/guides).

---

## 📚 2. IP Assignment — The Non-Negotiable

### Definition 39.7.2 — IP Assignment

An IP assignment agreement transfers intellectual property rights from a person to a company entity. Without it, IP created by founders, employees, or contractors may belong to them personally, not the company.

### 2.1 Why This Is Critical

**Scenario A (no IP assignment):** You and a co-founder build your product. You have a falling out at month 18. Your co-founder owns 50% of the IP personally (they wrote half the code). They can:
- Prevent you from using the code they wrote
- License the same codebase to a competitor
- Block an acquisition (acquirers require clean IP chain)

**Scenario B (IP assignment in place):** All code, designs, processes, and inventions are assigned to the company from day one. A departing co-founder retains equity but not IP. The company owns all the work.

### 2.2 The Three IP Assignment Documents Every Founder Needs

**1. Founder IP Assignment Agreement** (signed at company formation)
All founders assign to the company any IP they created that relates to the company's business, including any work done before the company was officially formed.

**2. Employee IP Assignment + Inventions Agreement** (signed on hire)
Every employee assigns to the company all work-related inventions and IP created during their employment. Non-compete clauses (where legal) are separate and state-specific.

**3. Contractor / Freelancer Work-for-Hire Agreement**
By US copyright law, work created by an independent contractor does **not** automatically belong to the hiring company — it belongs to the contractor. You must explicitly assign it via contract before the work begins.

### 2.3 The "Prior Employer" Trap

If any founder or key employee has a non-compete or invention assignment agreement with a previous employer, those agreements may claim rights to work created during or after that employment.

**Common scenario:** A developer leaves a big tech company (Google, Microsoft, Meta) where they signed a broad invention assignment. They build a startup on nights and weekends. The former employer's agreement may claim rights to that work.

**Fix:** Have an employment attorney review any prior employer agreements before beginning work on your startup. Some states (California, notably) have statutory protections limiting employer IP claims to work done on company time with company resources.

---

## 📚 3. Contractor vs Employee

### Definition 39.7.3 — Worker Classification

The IRS and state agencies have specific rules for classifying workers as employees (W-2) or independent contractors (1099). Misclassification is a significant legal and financial risk.

### 3.1 The Core Distinction

| Factor | Employee (W-2) | Contractor (1099) |
|--------|----------------|-------------------|
| **Control over work** | Company controls how and when work is done | Worker controls their own methods |
| **Tools & equipment** | Company provides tools | Worker uses their own tools |
| **Permanency** | Ongoing, indefinite relationship | Project-based, temporary |
| **Exclusivity** | Works only for this company | Works for multiple clients |
| **Training** | Receives company training | Brings their own expertise |
| **Benefits** | Eligible for benefits (health, 401k) | No company benefits |

No single factor is definitive — the IRS and courts look at the totality.

### 3.2 The Risk of Misclassification

If you misclassify a worker (call them a contractor but treat them like an employee), you may owe:
- Back payroll taxes (employee portion + employer portion)
- Penalties and interest
- Benefits owed retroactively
- State unemployment insurance
- Worker's compensation claims

High-profile misclassification cases (Uber drivers, gig economy workers) have made regulators aggressive. If someone works for you exclusively, full-time, with your equipment, following your processes — they're almost certainly an employee regardless of what the contract says.

### 3.3 When to Use Contractors

Contractors are appropriate for:
- Project-based work with a defined scope and end date
- Specialists brought in for specific expertise (legal, accounting, security audit)
- Part-time contributors to open-source or content work
- International workers (avoids complex employment law in foreign jurisdictions)

Always have a written contractor agreement that includes:
- Scope of work
- Deliverables and timeline
- Rate and payment terms
- IP assignment / work-for-hire clause
- Confidentiality clause
- No employment relationship acknowledgment

### 3.4 When to Make the First Hire an Employee

If someone is going to:
- Work for you full-time (>20 hrs/week consistently)
- Be your first sales, engineering, or operations hire
- Be given equity
- Have access to sensitive customer/business data

...they should be an employee. The additional cost and admin (payroll, taxes, benefits) is manageable with tools like Gusto or Rippling, and it protects both parties.

---

## 📚 4. Vesting Schedules

### Definition 39.7.4 — Vesting

Vesting is a schedule by which a person earns their equity over time. Unvested equity is forfeited if the person leaves before it vests.

### 4.1 Standard Vesting Structure

The near-universal standard:

**4-year vesting with a 1-year cliff:**
- **Year 1 (cliff):** 0% vested; if you leave before 1 year, you get nothing
- **After cliff:** 25% vests immediately, then monthly or quarterly vesting for the remaining 75% over the next 3 years
- **At year 4:** 100% vested

**Why it matters:** Vesting protects the company (and remaining founders/investors) from a co-founder who leaves at month 3 taking 50% of the equity with them.

### 4.2 Vesting for Co-Founders

Both/all co-founders should vest from day one of company formation. The most common mistake: "We trust each other — we don't need vesting." Three months later, one founder leaves and takes 50% of the company into inactive status.

**Model co-founder equity + vesting agreement (simplified):**
- 50/50 split between two founders
- 4-year vesting / 1-year cliff for both
- Repurchase right: company can buy back unvested shares at original price if founder leaves
- Acceleration clause: single-trigger (change of control) vs double-trigger (change of control + termination) acceleration — typically double-trigger protects employees; single-trigger is negotiated for founders

### 4.3 Early Employee Equity

| Stage of hire | Typical equity range | Dilution note |
|---------------|---------------------|---------------|
| Employee #1 (pre-seed) | 1.0–2.0% | On fully diluted, post-option-pool basis |
| Employee #2-5 | 0.5–1.0% | |
| Employee #10-20 (post-seed) | 0.1–0.5% | |
| VP/Director (post-seed) | 0.25–0.75% | |
| CXO (post-Series A) | 0.5–1.5% | |

*Figures are US startup benchmarks — paraphrased from Stripe Atlas equity guide and Carta compensation data.*

These are equity grants (options, typically ISOs) that vest over 4 years with a 1-year cliff.

---

## 📚 5. Founder Agreements

### 5.1 What a Founder Agreement Covers

A founder agreement (sometimes part of the company formation documents, sometimes a separate agreement) should cover:

| Topic | Why it matters |
|-------|---------------|
| **Equity split** | Clear percentage for each founder |
| **Vesting schedule** | 4/1 year standard for all founders |
| **Roles and responsibilities** | Who is CEO, CTO, etc. |
| **IP assignment** | All prior work assigned to company |
| **Decision-making authority** | Which decisions require unanimous consent |
| **Dispute resolution** | How you handle disagreements |
| **Departure terms** | Unvested equity forfeiture, transition period |
| **Compensation** | Salary expectations (even if $0 at start) |
| **Non-compete and non-solicitation** | Post-departure restrictions |

### 5.2 The Equity Split Discussion

Have this conversation explicitly before you start building. Common failure: two people assume they're equal partners; one person assumed they're getting more because "it was my idea."

**The FAST Framework for equity splits (a guideline, not a rule):**
- **F — Founder role:** Full-time vs part-time contributes differently
- **A — Agreements:** Who's putting in cash, IP, or special assets
- **S — Stage:** Who took the most risk (quit job, funded the first sprint)
- **T — Title/track record:** Senior technical founder may warrant more initially

Equal splits (50/50 for two founders, 33/33/33 for three) are common and often the right choice — they signal mutual trust and prevent resentment. Arguments against equal splits: wildly different experience levels or contributions.

---

## 📚 6. Pre-Fundraising Legal Checklist

Before approaching investors, ensure:

- [ ] **Entity formed** (Delaware C-Corp if raising; LLC if bootstrapping only)
- [ ] **EIN obtained** from IRS
- [ ] **Bank account** opened in company name
- [ ] **Founder IP Assignment Agreements** signed by all founders
- [ ] **Vesting agreements** in place for all founders with 4/1-year schedule
- [ ] **83(b) elections** filed within 30 days of restricted stock issuance (US only — this is critical; consult a lawyer)
- [ ] **Any prior employer agreements** reviewed by attorney
- [ ] **Contractor agreements** with IP assignment for any third-party work
- [ ] **Domain, trademark** (at minimum, a basic trademark search)
- [ ] **Privacy policy + Terms of Service** live on your product site

### 6.1 The 83(b) Election — The Tax Move Founders Must Not Miss

When founders receive restricted stock (unvested equity), they have 30 days to file an **83(b) election** with the IRS. This election says: "Tax me now, at the current (near-zero) value of my shares, rather than at vesting when they may be worth millions."

Without the 83(b), you're taxed as ordinary income on each tranche of shares as it vests — potentially at a much higher value and tax rate.

**This is a $0 decision today vs potentially a $1M+ tax bill later. File it.**

Most formation services (Stripe Atlas, Clerky, Gust) include this in their onboarding checklist. Do not miss the 30-day window.

---

## 🔗 7. Cross-Links & Further Reading

### Internal
- [39.5 - Fundraising, Investors & Equity](39.5---Fundraising,-Investors-&-Equity) — fundraising triggers most of the legal events in this chapter
- [39.8 - Scaling Operations & Building Teams](39.8---Scaling-Operations-&-Building-Teams) — first hire = first employee classification decision

### External
- [Stripe Atlas Guides — full series (free)](https://stripe.com/atlas/guides)
- [YC Standard Legal Documents (free templates)](https://www.ycombinator.com/documents)
- [Clerky — Formation and legal automation for startups](https://www.clerky.com/)
- [Gust Launch — Formation + compliance for startups](https://www.gust.com/)
- [Carta — Cap table + equity management](https://carta.com/)
- [Paul Graham — "How to Deal with Co-Founder Fights"](http://www.paulgraham.com/cofounders.html)
- [First Round — "Legal Advice Every Startup Needs"](https://review.firstround.com/)
- [Cooley GO — Free legal resources for startups](https://www.cooleygo.com/)

---

## ⚠️ 8. Common Misconceptions

- **"I'll incorporate when I need to."** You need to incorporate before you take any customer money, hire anyone, or write production code with a co-founder. The cost of retroactive cleanup vastly exceeds the cost of forming correctly from day one.
- **"Verbal agreements are binding."** They can be in some jurisdictions, but they're nearly impossible to enforce without documentation. Write everything down, even in email.
- **"My co-founder is my best friend — we don't need a vesting agreement."** Co-founder splits are the #1 cause of startup death after market failure. The friendship is protected by having clarity, not by avoiding the conversation.
- **"Terms of service and privacy policy are boilerplate — I can copy someone else's."** Copying TOS/PP without customization creates legal exposure. GDPR, CCPA, and other regulations have specific requirements. Use a template service (Termly, Iubenda) or have a lawyer review.
- **"I own the code I wrote before incorporating."** Until it's explicitly assigned to the company entity in a signed document, you personally own it. IP assignment retroactively covers pre-incorporation work — but only if you sign the document.
- **"Non-competes are always enforceable."** In California, non-competes are largely unenforceable. In other states, they must be "reasonable" in scope and duration. Know your state's rules before drafting or signing one.

---

*Next: [39.8 - Scaling Operations & Building Teams](39.8---Scaling-Operations-&-Building-Teams) — You've built the foundation. Now build the machine.*
