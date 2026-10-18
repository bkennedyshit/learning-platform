# Batch record: pre-algebra-01

- **batch_id:** pre-algebra-01
- **subject:** Pre-Algebra (`/subject/pre-algebra`)
- **base commit:** `07d5f38` (Geometry batch `geometry-01`)
- **date:** 2026-10-18
- **source files:** `corpus/lessons/131-…138-*.md` (generated `content.json` is gitignored and rebuilt by `generate-content.mjs`)
- **selection:** the 8 lessons with `subject: "Pre-Algebra"` in `corpus/lessons/`, all `template` / `scaffold`; confirmed against the manifest (8 lessons, 0 indexable, hub gated). `13-pre-algebra-subject-plan.md` is `type: subject-plan`, excluded by the generator, and was not edited. The similarly numbered TypeScript lessons (`131-setup-compilation-…`, `132-type-system-…`, etc.) belong to another subject and were not touched.

## Lessons

Gate words = the generator's `wordCount` (rendered HTML text, includes KaTeX glyph text). Prose words = source body with `$…$` / `$$…$$` math removed, measured during batch QA.

| Slug | Title (unchanged) | Old gate words | New gate words | New prose words | Examples / misconceptions / practice | Before | After |
|---|---|---|---|---|---|---|---|
| `131-ratios-rates-proportions` | 13.1 - Ratios, Rates & Proportions | 354 | 1638 | 1241 | 6 / 6 / 8 | noindex (scaffold) | indexable |
| `132-the-number-system` | 13.2 - The Number System | 354 | 1519 | 1028 | 5 / 6 / 8 | noindex (scaffold) | indexable |
| `133-fractions-decimals-percent` | 13.3 - Fractions, Decimals & Percent | 354 | 1505 | 880 | 6 / 6 / 8 | noindex (scaffold) | indexable |
| `134-expressions-variables` | 13.4 - Expressions & Variables | 352 | 1421 | 952 | 5 / 6 / 8 | noindex (scaffold) | indexable |
| `135-equations-inequalities` | 13.5 - Equations & Inequalities | 352 | 1573 | 1109 | 7 / 6 / 8 | noindex (scaffold) | indexable |
| `136-geometry-foundations` | 13.6 - Geometry Foundations | 352 | 1766 | 1291 | 5 / 6 / 8 | noindex (scaffold) | indexable |
| `137-statistics-data` | 13.7 - Statistics & Data | 352 | 1719 | 1403 | 4 / 6 / 8 | noindex (scaffold) | indexable |
| `138-probability-intro` | 13.8 - Probability Intro | 352 | 1603 | 1160 | 5 / 6 / 8 | noindex (scaffold) | indexable |

Preserved for every lesson: slug, title, `subject: "Pre-Algebra"`, `catalog: k12`, `audience_tier: 9-12`, `chapter` (13.1–13.8), `type: chapter`, `open_source`, prev/next chain. Only the frontmatter `objectives` list changed (same schema; verified with `services/corpus-ingestion/src/frontmatter.ts`). Each lesson has prerequisites, observable objectives, core explanation with the reasoning behind each rule (zero pairs and the sign-rule pattern for integers, the 2-and-5 denominator test for terminating decimals, cut-and-rearrange derivations of area formulas, the reversal rule for inequalities), worked examples, misconceptions/boundary cases, practice with a collapsible answer key and self-check method, a "Where this fits" section with hub/prev/next/related links, and sources. Lesson scope follows the chapter outline in `13-pre-algebra-subject-plan.md`.

Cross-subject links added (all existing public routes): Algebra I 14.1/14.2/14.3/14.5/14.7/14.8 (`/subject/algebra-i`); Geometry 15.1/15.5/15.6/15.8; `171-exploring-data-1-variable`, `174-probability`, and `/subject/statistics-and-probability` (still gated; routes valid; the lessons describe that course as "still being written"). An early draft linked the gated scaffold `app-024-fractions-concepts-operations` as a review resource; that link was removed because the target does not yet teach the topic.

## Corpus delta

| Metric | Before | After |
|---|---|---|
| Indexable lessons | 451 | 459 |
| Gated lessons | 189 (placeholder 40, scaffold 149) | 181 (placeholder 40, scaffold 141) |
| Indexable subject hubs | 57 of 81 | 58 of 81 (`pre-algebra` promoted, 8/8 lessons) |
| Sitemap URLs | 511 | 520 (+8 lessons, +1 hub) |

Manifest diff (regenerated from `07d5f38` sources vs. this batch): only the 8 Pre-Algebra lesson entries and the `pre-algebra` subject entry changed; 640 lessons before and after. Local links routed to hubs dropped 668 → 644 because the scaffold's `Subject_Plan`/`README`/`LEARNING_PATH` links were removed.

## Evidence sources

All 46 unique URLs cited in the lessons were fetched on 2026-10-18 and returned HTTP 200 with the matching page title. Topic coverage was spot-checked in the fetched page text where a lesson leans on a specific claim (e.g. the $1.5 \cdot \text{IQR}$ "potential outlier" rule in *Introductory Statistics* 2.3, reflections in *Contemporary Mathematics* 10.5, cones in *Prealgebra* 9.6). *Contemporary Mathematics* 10.7 does not cover pyramids, so the pyramid one-third result is cited to Euclid XII.7; *Introductory Statistics* does not cover MAD, so MAD is cited to Illustrative Mathematics.

- OpenStax, *Prealgebra 2e*: [2.1](https://openstax.org/books/prealgebra-2e/pages/2-1-use-the-language-of-algebra), [2.2](https://openstax.org/books/prealgebra-2e/pages/2-2-evaluate-simplify-and-translate-expressions), [3.1](https://openstax.org/books/prealgebra-2e/pages/3-1-introduction-to-integers), [3.2](https://openstax.org/books/prealgebra-2e/pages/3-2-add-integers), [3.3](https://openstax.org/books/prealgebra-2e/pages/3-3-subtract-integers), [3.4](https://openstax.org/books/prealgebra-2e/pages/3-4-multiply-and-divide-integers), [4.2](https://openstax.org/books/prealgebra-2e/pages/4-2-multiply-and-divide-fractions), [4.3](https://openstax.org/books/prealgebra-2e/pages/4-3-multiply-and-divide-mixed-numbers-and-complex-fractions), [4.5](https://openstax.org/books/prealgebra-2e/pages/4-5-add-and-subtract-fractions-with-different-denominators), [4.6](https://openstax.org/books/prealgebra-2e/pages/4-6-add-and-subtract-mixed-numbers), [5.3](https://openstax.org/books/prealgebra-2e/pages/5-3-decimals-and-fractions), [5.5](https://openstax.org/books/prealgebra-2e/pages/5-5-averages-and-probability), [5.6](https://openstax.org/books/prealgebra-2e/pages/5-6-ratios-and-rate), [6.1](https://openstax.org/books/prealgebra-2e/pages/6-1-understand-percent), [6.2](https://openstax.org/books/prealgebra-2e/pages/6-2-solve-general-applications-of-percent), [6.4](https://openstax.org/books/prealgebra-2e/pages/6-4-solve-simple-interest-applications), [6.5](https://openstax.org/books/prealgebra-2e/pages/6-5-solve-proportions-and-their-applications), [7.1](https://openstax.org/books/prealgebra-2e/pages/7-1-rational-and-irrational-numbers), [7.3](https://openstax.org/books/prealgebra-2e/pages/7-3-distributive-property), [8.1](https://openstax.org/books/prealgebra-2e/pages/8-1-solve-equations-using-the-subtraction-and-addition-properties-of-equality), [8.2](https://openstax.org/books/prealgebra-2e/pages/8-2-solve-equations-using-the-division-and-multiplication-properties-of-equality), [8.3](https://openstax.org/books/prealgebra-2e/pages/8-3-solve-equations-with-variables-and-constants-on-both-sides), [8.4](https://openstax.org/books/prealgebra-2e/pages/8-4-solve-equations-with-fraction-or-decimal-coefficients), [9.4](https://openstax.org/books/prealgebra-2e/pages/9-4-use-properties-of-rectangles-triangles-and-trapezoids), [9.5](https://openstax.org/books/prealgebra-2e/pages/9-5-solve-geometry-applications-circles-and-irregular-figures), [9.6](https://openstax.org/books/prealgebra-2e/pages/9-6-solve-geometry-applications-volume-and-surface-area), [10.5](https://openstax.org/books/prealgebra-2e/pages/10-5-integer-exponents-and-scientific-notation), [10.6](https://openstax.org/books/prealgebra-2e/pages/10-6-introduction-to-factoring-polynomials), [11.1](https://openstax.org/books/prealgebra-2e/pages/11-1-use-the-rectangular-coordinate-system)
- OpenStax, *Elementary Algebra 2e*: [2.4](https://openstax.org/books/elementary-algebra-2e/pages/2-4-use-a-general-strategy-to-solve-linear-equations), [2.7](https://openstax.org/books/elementary-algebra-2e/pages/2-7-solve-linear-inequalities)
- OpenStax, *Intermediate Algebra 2e*: [2.6](https://openstax.org/books/intermediate-algebra-2e/pages/2-6-solve-compound-inequalities)
- OpenStax, *Introductory Statistics 2e*: [1.2](https://openstax.org/books/introductory-statistics-2e/pages/1-2-data-sampling-and-variation-in-data-and-sampling), [2.2](https://openstax.org/books/introductory-statistics-2e/pages/2-2-histograms-frequency-polygons-and-time-series-graphs), [2.3](https://openstax.org/books/introductory-statistics-2e/pages/2-3-measures-of-the-location-of-the-data), [2.4](https://openstax.org/books/introductory-statistics-2e/pages/2-4-box-plots), [2.5](https://openstax.org/books/introductory-statistics-2e/pages/2-5-measures-of-the-center-of-the-data), [2.7](https://openstax.org/books/introductory-statistics-2e/pages/2-7-measures-of-the-spread-of-the-data), [3.1](https://openstax.org/books/introductory-statistics-2e/pages/3-1-terminology), [3.2](https://openstax.org/books/introductory-statistics-2e/pages/3-2-independent-and-mutually-exclusive-events), [3.5](https://openstax.org/books/introductory-statistics-2e/pages/3-5-tree-and-venn-diagrams)
- OpenStax, *Contemporary Mathematics*: [7.1](https://openstax.org/books/contemporary-mathematics/pages/7-1-the-multiplication-rule-for-counting), [10.5](https://openstax.org/books/contemporary-mathematics/pages/10-5-tessellations), [10.7](https://openstax.org/books/contemporary-mathematics/pages/10-7-volume-and-surface-area)
- Illustrative Mathematics (Kendall Hunt), Grade 6, Unit 8, [Lesson 11: Variability and MAD](https://im.kendallhunt.com/MS/students/1/8/11/index.html)
- Euclid, *Elements*, ed. D. E. Joyce (Clark University), [Proposition XII.7](https://mathcs.clarku.edu/~djoyce/java/elements/bookXII/propXII7.html)

Each lesson links its own subset inline under "Sources". Results derived in the lesson rather than cited: the sign-rule pattern argument, the 2-and-5 test for terminating decimals (from $10^n = 2^n 5^n$), the repeating-decimal-to-fraction method, the cut-and-rearrange area derivations, and the trapezoid split check. Quartiles use the "median of each half, excluding the overall median when $n$ is odd" convention, and the lesson states that software conventions vary.

## Calculation checks

Every worked-example and answer-key value was re-evaluated in a throwaway Node script (deleted after use): ratio simplifications and GCFs; unit rates; constant-of-proportionality tables and the non-proportional $y = 3x + 2$ table; map/floor-plan scales; percent change in both directions and the $+30\%/-30\%$ counterexample; simple interest and totals; integer sums, differences, products, quotients, powers ($(-2)^4$ vs. $-2^4$), distances, and the two ordering tasks; all fraction and mixed-number operations, decimal conversions, $0.\overline{36} = \tfrac{4}{11}$, and scientific-notation products/quotients; expression evaluation, distribution, combining like terms, and GCF factoring (each checked at several variable values); every equation solution substituted back, identity/contradiction cases tested at sample values, and every inequality checked at its boundary and on both sides; areas, circumferences (exact and rounded), prism and pyramid volumes/surface areas, slant height, grid distances and reflections; mean, median, mode, quartiles, IQR, fences, histogram bin counts, and MAD (with the signed-deviation-sum check) for every data set; theoretical probabilities by exhaustive enumeration of two-dice and three-coin sample spaces, counting-principle products, and with/without-replacement draws (also enumerated). 244 checks, 0 failures.

Prices, marbles, homework minutes, scores, the dive, the temperature reading, the spinner and thumbtack trials, the window, the garden, and the rental/savings scenarios are labeled "illustrative" in the lesson text; no measured or platform results are claimed. No curriculum standards codes were cited.

## Affiliate review

No affiliate links, resource cards, or commercial references were added. `AffiliateOffer`/`AffiliateDisclosure` and resource pages are untouched. The external links in the subject plan (Khan Academy, AoPS store, etc.) were not copied into the lessons.

## Validation

| Check | Result |
|---|---|
| `node scripts/generate-content.mjs` (content-site) | pass; internal-link assertion pass |
| `node scripts/generate-content.mjs` (learning-app) | pass (640 lessons, 81 subjects) |
| Ingestion frontmatter parser (`parseLessonMarkdown`, via `node --experimental-strip-types`) on all 8 files | pass; title/subject/catalog/tier/chapter/type preserved, 4 objectives each |
| Frontmatter diff vs. `07d5f38` | only `objectives` changed in all 8 files |
| Scaffold/TODO residue scan (manifest HTML + prerendered HTML) | 0 hits; no `katex-error`; currency `\$` renders as literal `$` with no stray math |
| Internal links | 59 lesson-body links in the manifest and 157 links (26 unique routes) in the rendered batch pages + hub; 0 unresolved |
| External source links | 46 unique, all HTTP 200 |
| Rendered robots meta | 8 batch pages + `/subject/pre-algebra`: none (indexable), canonical set; negative control `/171-exploring-data-1-variable`: `noindex, follow` |
| Rendered hub | links all 8 lessons, no "In development" section |
| Prerendered `sitemap.xml` | 520 URLs; all 8 lessons + hub present; gated `171-exploring-data-1-variable` and `/subject/statistics-and-probability` absent |
| `pnpm test` (content-site) | 35/35 pass (4 new Pre-Algebra batch tests) |
| `pnpm check` (content-site, learning-app) | pass |
| `pnpm build` (content-site) | pass |
| `pnpm lint` (content-site) | 4 errors, 5 warnings, identical to the pre-existing set recorded in earlier batches (`page.tsx`, `tools/calculus`, `tools/matrix`, `tools/probability`, `AffiliateOffer.tsx`, `generate-content.mjs`); the modified test file lints clean |
| `pnpm test` (corpus-ingestion) | not run: same pre-existing `TS2307 Cannot find module '@learning-platform/corpus-types'` build blocker recorded in algebra-ii-01; unrelated to this batch |

## Production observation (previous batch)

On 2026-10-18, `https://learning.nepa-ai.com/sitemap.xml` served 511 URLs including `/subject/geometry` and `/151-foundations-of-geometry`; `/151-foundations-of-geometry` and `/subject/geometry` rendered without a robots `noindex` and without scaffold text. Geometry batch `07d5f38` has therefore propagated. `/131-ratios-rates-proportions` was still `noindex, follow` with scaffold text, as expected before this batch deploys.

## Not in this batch

- Obsidian mirror copies under `corpus/10 - Learning App Material/Subjects/` were not edited; the generators and ingestion read `corpus/lessons/` only.
- The external backlog CSV/MD (outside this repository) was not modified; it should be regenerated to show these 8 rows (and the 24 Algebra I/II/Geometry rows) as `ok`.
- Search Console indexing requests have not been made.
