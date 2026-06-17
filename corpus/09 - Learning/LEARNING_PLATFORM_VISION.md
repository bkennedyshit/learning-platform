---
date: 2026-05-29
title: "Learning Platform Vision — Scaling Bill's Vault to K-12 / Early College"
tags: [vision, platform, edtech, K-12, learning-system, product, scaling]
type: vision-document
status: living-document
---

# 🚀 Learning Platform Vision
## Scaling the Vault System to K-12 / Early College EdTech

*Part of [[00 - 09 - Learning Index|Learning Index]] · Companion to [[BUILDING_AT_SCALE|BUILDING_AT_SCALE.md]]*

---

> **The thesis:** Bill's Vault has independently converged on a learning architecture that beats every mainstream K-12 platform on the things that actually matter — depth, rigor, active recall integration, cross-subject linking, open-source resources, and adult-grade intellectual respect for the learner. This document is the product brief for turning that system into something millions of students can use.

---

## 1. What We've Already Built (The Proof of Concept)

Before anything else: **the vault is the prototype.** It's not a concept — it's a working system that has already produced:

| What exists | Why it matters |
|-------------|---------------|
| **43 subjects** across math, physics, biology, chemistry, anatomy, CS, AI/ML, languages, neuroscience, philosophy, game dev, VR, electronics, robotics | A K-12-to-early-college curriculum already exists — it just needs a front-end and learner onboarding |
| **Pearson/Ambrose textbook-grade chapter notes** | Every chapter follows: definitions → axioms → theorems → worked examples → common misconceptions → active recall prompts. This is the pedagogical structure used by the best universities — built into every file |
| **Python drill generators** (`_practice/scripts/`) | Algorithmic, seeded, infinitely re-runnable practice problems. No teacher needed to generate new worksheets |
| **Spaced repetition integration** (Anki, Kenhub, Bunpro, WaniKani) | SR is the highest-leverage learning technique known to cognitive science. The vault tells learners exactly which deck to use and when |
| **Free open-source resource catalogs** (every Subject_Plan §2) | Every subject maps to free, peer-reviewed, legally-available resources — OpenStax, Khan Academy, MIT OpenCourseWare, Perseus, Language Transfer, YouTube channels. Zero licensing cost |
| **Cross-subject wikilinks** | The vault treats knowledge as a graph, not a list. Biology → Anatomy → Neuroscience → Behavioral Psychology → AI is a traversable knowledge graph. This is what textbook publishers cannot replicate |
| **Six-language track with Romance-transfer optimization** | Spanish → French → Italian → Latin forms a designed acquisition path. No mainstream platform maps language learning as a graph |
| **NotebookLM audio overview integration** | Per-chapter AI audio companions already described and partially built |

**The gap between this and a shippable product is: front-end + learner onboarding + delivery mechanism.** The curriculum is done.

---

## 2. What Mainstream EdTech Gets Wrong

Understanding the competitive landscape explains exactly why this system is different:

| Platform | What it does well | What it gets catastrophically wrong |
|----------|------------------|-------------------------------------|
| **Khan Academy** | Free, accessible, decent video explanations | Gamification replaces depth; no cross-subject linking; treats learners as children regardless of age; no open-source resource integration |
| **Duolingo** | Habit formation, UI/UX | Surface-level language learning optimized for engagement metrics, not acquisition; treats languages as isolated units; no grammar depth |
| **Coursera / edX** | University-grade video content | Passive consumption; no active recall system; no drill generation; expensive at scale; no inter-course linking |
| **Khan Academy Kids / IXL / Prodigy** | K-8 engagement | Gamification as a substitute for rigor; no scaffolding from elementary → college; no open-source resource integration |
| **Quizlet** | Flashcard creation and sharing | No curriculum structure; no Pearson/Ambrose depth; no drill generation; flashcards as terminal product rather than a tool |
| **Brilliant.org** | Interactive problem-solving, beautiful UX | Proprietary content only; expensive; limited subject range; no language learning; no open-source integration |
| **AP/IB curriculum** | Standardized, college-credit bearing | Bureaucratic pace; constrained to institutional calendar; no adaptive depth; costs money; no drill generation |

**The vault system's differentiators:**
1. **Depth without gatekeeping** — MIT-grade rigor, entirely free resources
2. **Active recall built into every chapter** — not bolted on as a product feature
3. **Knowledge graph structure** — subjects explicitly cross-link; learning is non-linear
4. **Infinitely generative practice** — Python drill scripts produce new problems on demand; no worksheet library needed
5. **Respects learner intelligence** — no gamification, no patronizing UX; treats a 15-year-old who wants to understand quantum mechanics the same as an adult learner

---

## 3. The Target Learner Segments

### Segment A: Advanced K-12 Students (Grades 6–12)
- Already bored by the pace of school
- Want to go deeper than the curriculum allows
- Self-directed; respond to intellectual respect, not gamification
- Subjects most relevant: Math, Physics, Biology, Chemistry, Anatomy, History, Languages
- **Acquisition channel:** word of mouth among gifted student communities, Reddit (r/learnmath, r/languagelearning), Discord servers

### Segment B: Adult Independent Learners (18–35)
- Career changers, autodidacts, lifelong learners
- Already using Anki, Language Transfer, MIT OCW, Khan Academy piecemeal
- Need **curation + structure + cross-linking**, not more content
- **Bill's vault is already optimized for this segment** — this is the primary user
- **Acquisition channel:** productivity YouTube, Obsidian community, language learning communities

### Segment C: Early College / Community College Students
- Students who feel "behind" on foundational subjects
- Looking for supplemental study that goes deeper than their textbook
- Subjects: Calculus, Linear Algebra, Biology, Chemistry, Anatomy, Physics, Programming
- **Acquisition channel:** r/learnmath, r/premed, Discord study servers, TikTok/YouTube study content

### Segment D: Homeschool Families
- Parents who want a coherent, rigorous K-12 curriculum not tied to a specific publisher
- Need: structured subject plans, free resource catalogs, drill generators, progress tracking
- The vault's `Subject_Plan.md` + `LEARNING_PATH.md` + drill scripts is essentially a complete homeschool curriculum module
- **Acquisition channel:** homeschool networks, Facebook groups, YouTube homeschool content creators

### Segment E: Teachers / Tutors as Power Users
- Private tutors who want structured, deep subject materials to pull from
- Teachers who want drill generators to create customized worksheets
- **B2B opportunity:** license the drill generator system + curriculum structure to tutoring companies

---

## 4. The Product Architecture — Three Build Tiers

### Tier 1: Minimal Viable Product (0 → Launch, ~3–6 months)
**Goal:** Make the vault publicly accessible and navigable without Obsidian.

**What it is:** A **static site generator** that converts the vault's markdown into a beautiful, searchable, cross-linked web experience.

**Tech stack:**
- **Astro** or **Next.js** — static site generation from markdown/MDX
- **Obsidian → MDX pipeline** — convert wikilinks `[[...]]` to proper hyperlinks; render mermaid diagrams; render `<details>` blocks; render LaTeX via KaTeX
- **Pagefind** or **Algolia** — full-text + frontmatter search across all 43+ subjects
- **No database, no auth** in Tier 1 — purely static; deployable on Cloudflare Pages (free)

**Pages:**
- `/` — Subject browser (the Learning Index as a visual grid)
- `/subjects/[subject]` — Subject hub (README.md rendered)
- `/subjects/[subject]/syllabus` — Subject_Plan.md
- `/subjects/[subject]/path` — LEARNING_PATH.md
- `/subjects/[subject]/[chapter]` — Individual chapter
- `/search` — Full-text search across all content
- `/resources` — Aggregated free resource catalog across all subjects

**Cost: $0 hosting, $0 content** (everything is already built)

**Time to MVP:** One engineer, 6–8 weeks.

---

### Tier 2: Interactive Learning Layer (~6–12 months post-MVP)
**Goal:** Add the drill generator as an in-browser experience; add progress tracking.

**New features:**
- **In-browser drill runner** — the existing Python drill scripts converted to a web API (FastAPI + Pyodide for client-side execution, or a simple serverless function)
  - User selects: subject → chapter → drill type → count → seed
  - Drills render in a clean card interface
  - "Show answer" collapsible (already built as `<details>` in the vault)
- **Spaced repetition queue** — integrate with the Anki API or build a lightweight browser-based SR system using the existing `_practice/` content
- **Progress tracking** — simple: mark chapters as Read / In Progress / Complete; store in localStorage (no auth needed for Tier 2)
- **Subject roadmap visualization** — render the mermaid curriculum topology graphs as interactive SVGs with clickable nodes

**New tech:**
- **Supabase** (Postgres + Row Level Security) — lightweight backend for progress; anonymous sessions in Tier 2, full auth in Tier 3
- **Vercel** or **Cloudflare Workers** — serverless drill API
- **Pyodide** — run Python drill scripts in the browser via WebAssembly (no backend needed for drill execution)

---

### Tier 3: Full Platform (~12–24 months post-MVP)
**Goal:** Learner accounts, curriculum customization, educator tools, mobile app.

**New features:**
- **Learner accounts** — sign up, track progress across devices, set learning goals, receive personalized subject recommendations
- **Adaptive learning path** — based on quiz performance and chapter completion, the system suggests next chapters and surface prerequisite gaps
- **Educator dashboard** — teachers/tutors assign chapters, create custom drill sets, track student progress across a cohort
- **AI study companion** — per-chapter AI tutor that can answer questions about the chapter content, generate additional examples, quiz the learner Socratically (using the chapter note as context for a RAG pipeline — see [[23 - AI 10 - AI & Machine Learning Machine Learning Systems/10.5 - Transformer Architectures & LLMs|Track 10.5 Transformers]])
- **Mobile app** — Flutter/Dart (see [[22 - App Architectures & Frameworks/8.5 - Flutter & Dart - Widget Tree, Isolates & Custom Painters|Track 22.5 Flutter]]) — offline-first; download chapters for offline study; daily drill notifications
- **Community layer** — per-chapter discussion threads; peer study groups; "study buddy" matching by subject and timezone

**Business model options:**
- **Freemium:** all content free; Tier 3 features (progress sync, AI companion, educator tools) on a subscription (~$8–15/month)
- **Educator/School licensing:** per-seat or per-school license for the educator dashboard + cohort tracking
- **Homeschool bundle:** one-time purchase for the full curriculum as a downloadable vault + site license

---

## 5. Subject Coverage — K-12 Curriculum Mapping

The vault's existing subjects already cover most of a rigorous K-12 → early college curriculum. Here is the gap analysis:

### ✅ Already Built (full subjects in vault)

| Grade band | Vault subjects covering it |
|------------|--------------------------|
| **Grades 6–8 (Middle School)** | Math & Physics foundations (arithmetic → algebra → geometry entry points), Biology, Chemistry intro, English, Spanish |
| **Grades 9–10 (Early High School)** | Algebra/Pre-Calculus (Math Track), Biology, Chemistry, Physics (Classical Mechanics), English, Spanish, French |
| **Grades 11–12 (Late High School / AP-equivalent)** | Calculus, Linear Algebra, Classical Mechanics, Biology, Chemistry, Anatomy, Neuroscience, Physics (E&M, QM intro), CS (Python, C++, JavaScript), Spanish, French, Italian, Latin |
| **Early College (Freshman/Sophomore)** | Full Math & Physics tower (12 sub-subjects, 94 chapters), AI/ML, Algorithms & DS, System Design, Neuroscience, Behavioral Psychology, Biomechanics |

### 🟡 Gaps to Fill (future subjects)

| Subject | Priority | Rationale |
|---------|----------|-----------|
| **World History / US History** | High | Core K-12 requirement; no existing vault track |
| **Geography** | Medium | Pairs with language + culture tracks |
| **Economics & Personal Finance** | High | Business track exists but no personal-finance / macro intro |
| **Pre-Algebra / Algebra I/II** | High | Math track starts at Calculus — need earlier entry points for K-8 learners |
| **Geometry** | High | Separate from the existing math tower |
| **Statistics & Probability** | High | Distinct from the ML statistics chapter; needed for AP Stats, data literacy |
| **Earth Science / Environmental Science** | Medium | Completes the natural sciences |
| **Ancient Greek** | Medium | Latin track creates a natural bridge |
| **Mandarin Chinese** | High | Most-studied second language globally after English/Spanish |
| **Art History** | Low | Cultural literacy complement to humanities tracks |
| **Music Theory** | Medium | Music Production track exists (production); theory is separate |

---

## 6. The Open-Source Philosophy

**The content should remain open.** The vault's entire academic content is built on open-source materials (OpenStax, Khan Academy, MIT OCW, Perseus Digital Library, Language Transfer). Making the content proprietary would:
1. Contradict the entire ethos of the project
2. Create legal complexity (derivative works from CC-licensed sources)
3. Remove the vault's primary competitive advantage: being the best free option

**What gets monetized is the platform layer:**
- Progress tracking and sync (infrastructure cost)
- AI study companion (compute cost)
- Educator dashboard (B2B value)
- Mobile app (convenience)
- Premium drill packs and additional worked examples (content extension, not gating)

**The curriculum vault itself (all markdown files) stays open-source on GitHub.** This creates a community flywheel: teachers contribute chapters, students improve examples, subject-matter experts review content. The platform is the business; the curriculum is the commons.

---

## 7. The Technical Foundation We Already Have

Because the vault is built in Obsidian markdown with a specific, consistent structure, the engineering work for Tier 1 is mostly **pipeline work**, not content work:

```
Vault markdown files
        ↓
  [Preprocessing pipeline]
  - Convert [[wikilinks]] → relative URLs
  - Render mermaid diagrams → SVG
  - Convert LaTeX $$ blocks → KaTeX HTML
  - Parse frontmatter YAML → page metadata
  - Extract active recall <details> blocks → drill card format
  - Build cross-link graph → navigation + related pages
        ↓
  [Static site generator — Astro/Next.js]
  - Subject browser (grid of 43+ subjects)
  - Chapter reader (rendered markdown + sidebar nav)
  - Search index (Pagefind — full text + frontmatter)
  - Resource catalog (aggregated from all Subject_Plan §2 sections)
        ↓
  [Deployment — Cloudflare Pages / Vercel]
  - Zero-cost static hosting
  - Edge CDN worldwide
  - Instant deploys on git push
```

**Estimated engineering effort for Tier 1:** 1 full-stack engineer × 6–8 weeks, or 2 engineers × 3–4 weeks.

The drill scripts are already in Python with clean CLI interfaces (`--count`, `--seed`, `--mode` flags). Converting them to a FastAPI endpoint or Pyodide client-side runner is ~1–2 days per subject's drill set.

---

## 8. The Pitch — One Paragraph

> **Bill's Vault Platform** is the only free, open-source, curriculum-grade learning system that covers K-12 through early college with the rigor of a university textbook, the resource curation of a research librarian, and the active recall tooling of a professional tutor — across 43 subjects from quantum mechanics to Latin. It is not another video platform. It is not another flashcard app. It is a knowledge graph with an executable curriculum: every chapter has a syllabus, a learning path, a free resource catalog, and a drill generator that produces new practice problems on demand. The content is already built. The platform is next.

---

## 9. Immediate Next Steps

### This month (content)
- [ ] Expand 41.4–41.8 (French chapters) to full Pearson/Ambrose depth
- [ ] Expand 42.4–42.8 (Italian chapters) to full depth
- [ ] Expand 43.2–43.8 (Latin chapters) — especially the declension paradigm tables (43.2) and verb conjugation system (43.4)
- [ ] Add drill scripts for French verb conjugation (`41.4_verb_conjugation_drill.py`) and Latin declensions (`43.2_declension_drill.py`)

### This month (platform foundation)
- [ ] Set up a GitHub repo for the vault (already exists — `bkennedyshit/bills-vault`)
- [ ] Prototype the wikilink → URL conversion pipeline in Node.js or Python
- [ ] Evaluate Astro vs. Next.js for the static site (lean: Astro for content-heavy, no need for SSR)
- [ ] Deploy a prototype of the Learning Index as a web page (single page, no chapter content — just the navigation structure)

### This quarter (MVP definition)
- [ ] Define the 10 "flagship" subjects to launch with (recommendation: Math, Physics, Biology, Anatomy, Python, AI/ML, Spanish, French, English, Latin)
- [ ] Build the Obsidian → web pipeline for those 10 subjects
- [ ] Define the business model (freemium vs. open-source + services)
- [ ] Identify 3 beta users from each segment (students, adult learners, homeschool families)

---

## 10. Related Notes

- [[BUILDING_AT_SCALE|BUILDING_AT_SCALE.md]] — engineering architecture for production-grade systems; the technical foundation for Tier 2–3
- [[00 - 09 - Learning Index|Learning Master Index]] — the full curriculum that becomes the product
- [[23 - AI 10 - AI & Machine Learning Machine Learning Systems/10.5 - Transformer Architectures & LLMs|Track 10.5 Transformers]] — technical foundation for the AI study companion
- [[22 - App Architectures & Frameworks/8.5 - Flutter & Dart - Widget Tree, Isolates & Custom Painters|Track 22.5 Flutter]] — mobile app foundation
- [[19 - System Design & Distributed Architecture/Subject_Plan|Track 19 System Design]] — architecture for Tier 2–3 backend
- [[39 - Business & Entrepreneurship/Subject_Plan|Track 20 Business]] — GTM strategy, pricing, fundraising

---

*Vision document authored: 2026-05-29. This is a living document — update as the product evolves. The content proof-of-concept is complete. Ship the platform.*
