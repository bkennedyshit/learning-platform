# Batch record: algebra-ii-01

- **batch_id:** algebra-ii-01
- **subject:** Algebra II & Pre-Calculus (`/subject/algebra-ii-and-pre-calculus`)
- **base commit:** `c67c1bf` (Algebra I batch `algebra-i-01`)
- **date:** 2026-10-18
- **source files:** `corpus/lessons/161-…168-*.md` (generated `content.json` is gitignored and rebuilt by `generate-content.mjs`)
- **selection:** the 8 rows for subject `algebra-ii-and-pre-calculus` in `indexing-reports/learning-lesson-backlog-2026-10-17.csv`, all `template` / `scaffold`; confirmed against the manifest (8 lessons, 0 indexable, hub gated).

## Lessons

Gate words = the generator's `wordCount` (rendered HTML text, includes KaTeX glyph text). Prose words = source body with `$…$` / `$$…$$` math removed, measured during batch QA.

| Slug | Title (unchanged) | Old gate words | New gate words | New prose words | Examples / misconceptions / practice | Before | After |
|---|---|---|---|---|---|---|---|
| `161-polynomial-functions` | 16.1 - Polynomial Functions | 352 | 1822 | 1209 | 4 / 5 / 7 | noindex (scaffold) | indexable |
| `162-rational-functions` | 16.2 - Rational Functions | 352 | 1614 | 997 | 4 / 4 / 7 | noindex (scaffold) | indexable |
| `163-exponential-logarithmic-functions` | 16.3 - Exponential & Logarithmic Functions | 354 | 1580 | 943 | 5 / 5 / 8 | noindex (scaffold) | indexable |
| `164-trigonometry-the-unit-circle` | 16.4 - Trigonometry — The Unit Circle | 358 | 1598 | 924 | 5 / 5 / 8 | noindex (scaffold) | indexable |
| `165-trig-identities-equations` | 16.5 - Trig Identities & Equations | 354 | 1828 | 939 | 5 / 5 / 9 | noindex (scaffold) | indexable |
| `166-conic-sections` | 16.6 - Conic Sections | 352 | 1828 | 1077 | 5 / 5 / 7 | noindex (scaffold) | indexable |
| `167-sequences-series-the-binomial-theorem` | 16.7 - Sequences, Series & the Binomial Theorem | 358 | 1574 | 857 | 6 / 6 / 9 | noindex (scaffold) | indexable |
| `168-limits-introduction-to-calculus` | 16.8 - Limits & Introduction to Calculus | 356 | 1878 | 1204 | 6 / 5 / 9 | noindex (scaffold) | indexable |

Preserved for every lesson: slug, title (including the em dash in 16.4), `subject`, `catalog: k12`, `audience_tier: 9-12`, `chapter` (16.1–16.8), `type: chapter`, `open_source`, prev/next chain. Only the frontmatter `objectives` list changed (same schema; parsed by `services/corpus-ingestion/src/frontmatter.ts`). Each lesson has prerequisites, objectives, core explanation, worked examples, misconceptions/boundary cases, practice with a collapsible answer key and self-check method, a "Where this fits" section with hub/prev/next/related links, and sources.

Cross-subject links added (all existing public routes): Algebra I lessons 14.4/14.5/14.7/14.8, Geometry `156-right-triangles-trigonometry` (still gated, route valid), `31-first-order-odes-separable-exact`, `orbital-elements-conic-sections`, `11-limits-continuity`, `12-single-variable-differentiation`.

## Corpus delta

| Metric | Before | After |
|---|---|---|
| Indexable lessons | 435 | 443 |
| Gated lessons | 205 (placeholder 40, scaffold 165) | 197 (placeholder 40, scaffold 157) |
| Indexable subject hubs | 55 of 81 | 56 of 81 (`algebra-ii-and-pre-calculus` promoted, 8/8 lessons) |
| Sitemap URLs | 493 | 502 (+8 lessons, +1 hub) |

Manifest diff: only the 8 Algebra II & Pre-Calculus lesson entries and the `algebra-ii-and-pre-calculus` subject entry changed. Local links routed to hubs dropped 716 → 692 because the scaffold's `Subject_Plan`/`README` links were removed.

## Evidence sources

All 36 URLs fetched on 2026-10-18 and confirmed HTTP 200 with the matching section title.

- OpenStax, *Precalculus 2e*: [3.3](https://openstax.org/books/precalculus-2e/pages/3-3-power-functions-and-polynomial-functions), [3.4](https://openstax.org/books/precalculus-2e/pages/3-4-graphs-of-polynomial-functions), [3.5](https://openstax.org/books/precalculus-2e/pages/3-5-dividing-polynomials), [3.6](https://openstax.org/books/precalculus-2e/pages/3-6-zeros-of-polynomial-functions), [3.7](https://openstax.org/books/precalculus-2e/pages/3-7-rational-functions), [4.1](https://openstax.org/books/precalculus-2e/pages/4-1-exponential-functions), [4.3](https://openstax.org/books/precalculus-2e/pages/4-3-logarithmic-functions), [4.5](https://openstax.org/books/precalculus-2e/pages/4-5-logarithmic-properties), [4.6](https://openstax.org/books/precalculus-2e/pages/4-6-exponential-and-logarithmic-equations), [4.7](https://openstax.org/books/precalculus-2e/pages/4-7-exponential-and-logarithmic-models), [5.1](https://openstax.org/books/precalculus-2e/pages/5-1-angles), [5.2](https://openstax.org/books/precalculus-2e/pages/5-2-unit-circle-sine-and-cosine-functions), [5.3](https://openstax.org/books/precalculus-2e/pages/5-3-the-other-trigonometric-functions), [7.1](https://openstax.org/books/precalculus-2e/pages/7-1-solving-trigonometric-equations-with-identities), [7.2](https://openstax.org/books/precalculus-2e/pages/7-2-sum-and-difference-identities), [7.3](https://openstax.org/books/precalculus-2e/pages/7-3-double-angle-half-angle-and-reduction-formulas), [7.5](https://openstax.org/books/precalculus-2e/pages/7-5-solving-trigonometric-equations), [8.1](https://openstax.org/books/precalculus-2e/pages/8-1-non-right-triangles-law-of-sines), [8.2](https://openstax.org/books/precalculus-2e/pages/8-2-non-right-triangles-law-of-cosines), [8.6](https://openstax.org/books/precalculus-2e/pages/8-6-parametric-equations), [9.4](https://openstax.org/books/precalculus-2e/pages/9-4-partial-fractions), [10.1](https://openstax.org/books/precalculus-2e/pages/10-1-the-ellipse), [10.2](https://openstax.org/books/precalculus-2e/pages/10-2-the-hyperbola), [10.3](https://openstax.org/books/precalculus-2e/pages/10-3-the-parabola), [10.4](https://openstax.org/books/precalculus-2e/pages/10-4-rotation-of-axes), [11.1](https://openstax.org/books/precalculus-2e/pages/11-1-sequences-and-their-notations), [11.2](https://openstax.org/books/precalculus-2e/pages/11-2-arithmetic-sequences), [11.3](https://openstax.org/books/precalculus-2e/pages/11-3-geometric-sequences), [11.4](https://openstax.org/books/precalculus-2e/pages/11-4-series-and-their-notations), [11.6](https://openstax.org/books/precalculus-2e/pages/11-6-binomial-theorem), [12.1](https://openstax.org/books/precalculus-2e/pages/12-1-finding-limits-numerical-and-graphical-approaches), [12.2](https://openstax.org/books/precalculus-2e/pages/12-2-finding-limits-properties-of-limits), [12.3](https://openstax.org/books/precalculus-2e/pages/12-3-continuity), [12.4](https://openstax.org/books/precalculus-2e/pages/12-4-derivatives)
- OpenStax, *Intermediate Algebra 2e*: [11.1 Distance and Midpoint Formulas; Circles](https://openstax.org/books/intermediate-algebra-2e/pages/11-1-distance-and-midpoint-formulas-circles)
- MIT OpenCourseWare: [18.01SC Single Variable Calculus, Fall 2010](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/)

Each lesson links its own subset inline under "Sources".

## Calculation checks

Every worked-example and answer-key value was re-evaluated numerically in a throwaway Node script: polynomial factorizations and synthetic-division quotients/remainders checked at several x-values; rational-function holes, intercepts, slant asymptotes and partial fractions checked by substitution; logarithm/exponential solutions substituted back and compound-interest/half-life values recomputed; all unit-circle values, double-angle values, identities, and trig-equation roots evaluated; Law of Sines/Cosines triangle closed back to the given side; conic points substituted into the original general form and focal-sum/focus–directrix properties checked; sequence sums computed term by term and binomial expansions checked at sample points; limits checked numerically from both sides and derivative quotients at small h. 233 checks, 0 failures.

Interest rates, half-lives, populations, wheel and antenna dimensions are labeled "illustrative" in the lesson text; no measured or platform results are claimed. No curriculum standards codes were cited.

## Affiliate review

No affiliate links, resource cards, or commercial references were added. `AffiliateOffer`/`AffiliateDisclosure` and resource pages are untouched.

## Validation

| Check | Result |
|---|---|
| `node scripts/generate-content.mjs` (content-site) | pass; internal-link assertion pass |
| `node scripts/generate-content.mjs` (learning-app) | pass (640 lessons, 81 subjects) |
| Ingestion frontmatter parser (`parseLessonMarkdown`, via `node --experimental-strip-types`) on all 8 files | pass; title/subject/catalog/tier/chapter preserved, 4–5 objectives each |
| Scaffold/TODO residue scan (source + rendered HTML) | 0 hits; no `katex-error` in batch HTML |
| Internal links in rendered batch pages + hub | 155 checked, 0 unresolved |
| External source links | 36 unique, all HTTP 200 |
| Rendered robots meta | 8 batch pages + `/subject/algebra-ii-and-pre-calculus`: none (indexable), canonical set; negative controls `/151-foundations-of-geometry`, `/subject/geometry`: `noindex, follow` |
| Rendered hub | links all 8 lessons, no "In development" section |
| Prerendered `sitemap.xml` | 502 URLs; all 8 lessons + hub present; gated Geometry lesson absent |
| `pnpm test` (content-site) | 27/27 pass (4 new Algebra II batch tests) |
| `pnpm check` (content-site, learning-app) | pass |
| `pnpm build` (content-site) | pass |
| `pnpm lint` (content-site) | 4 errors, 5 warnings, identical to the pre-existing set recorded in algebra-i-01 (`app/page.tsx`, `tools/calculus`, `tools/matrix`, `tools/probability`, `AffiliateOffer.tsx`, `generate-content.mjs`); the modified test file lints clean |
| `pnpm test` (corpus-ingestion) | not run: its `build` step fails before tests with pre-existing `TS2307 Cannot find module '@learning-platform/corpus-types'` (workspace package not built in this worktree); unrelated to this batch |

## Not in this batch

- Obsidian mirror copies under `corpus/10 - Learning App Material/Subjects/16 - Algebra II & Pre-Calculus/` were not edited; the generators and ingestion read `corpus/lessons/` only.
- The external backlog CSV/MD (`websites/Local Sites/indexing-reports/`, outside this repository) was not modified; it should be regenerated to show these 8 rows (and the 8 Algebra I rows) as `ok`.
- Search Console indexing requests have not been made; production deployment has not been verified from this worktree.
