# Batch record: algebra-i-01

- **batch_id:** algebra-i-01 (pilot)
- **subject:** Algebra I (`/subject/algebra-i`)
- **base commit:** `193fcc2`
- **date:** 2026-10-18
- **source files:** `corpus/lessons/141-…148-*.md` (generated `content.json` is gitignored and rebuilt by `generate-content.mjs`)

## Lessons

Gate words = the generator's `wordCount` (rendered HTML text, includes KaTeX glyph text). Prose words = body text with `$…$` math removed, measured during batch QA.

| Slug | Old gate words | New gate words | New prose words | Before | After |
|---|---|---|---|---|---|
| `141-the-language-of-algebra` | 356 | 1369 | 969 | noindex (scaffold) | indexable |
| `142-linear-equations` | 352 | 1305 | 958 | noindex (scaffold) | indexable |
| `143-linear-inequalities` | 352 | 1270 | 906 | noindex (scaffold) | indexable |
| `144-functions-relations` | 352 | 1335 | 844 | noindex (scaffold) | indexable |
| `145-linear-functions-graphing` | 354 | 1282 | 850 | noindex (scaffold) | indexable |
| `146-systems-of-equations` | 354 | 1373 | 979 | noindex (scaffold) | indexable |
| `147-exponents-polynomials` | 352 | 1371 | 728 | noindex (scaffold) | indexable |
| `148-factoring-quadratics` | 352 | 1556 | 885 | noindex (scaffold) | indexable |

Preserved for every lesson: slug, title, `subject`, `catalog: k12`, `audience_tier: 9-12`, `chapter` (14.1–14.8), `type: chapter`, `open_source`, prev/next chain. Frontmatter `objectives` were replaced with specific, observable objectives (same list schema; parsed by `services/corpus-ingestion/src/frontmatter.ts`).

## Corpus delta

| Metric | Before | After |
|---|---|---|
| Indexable lessons | 427 | 435 |
| Gated lessons | 213 (placeholder 40, scaffold 173) | 205 (placeholder 40, scaffold 165) |
| Indexable subject hubs | 54 of 81 | 55 of 81 (`algebra-i` promoted, 8/8 lessons) |
| Sitemap URLs | 484 | 493 (+8 lessons, +1 hub) |

Manifest diff: only the 8 Algebra I lesson entries and the `algebra-i` subject entry changed.

## Evidence sources

All URLs fetched on 2026-10-18 and confirmed HTTP 200 with the matching section title.

- OpenStax, *Elementary Algebra 2e*: [1.2](https://openstax.org/books/elementary-algebra-2e/pages/1-2-use-the-language-of-algebra), [1.8](https://openstax.org/books/elementary-algebra-2e/pages/1-8-the-real-numbers), [1.9](https://openstax.org/books/elementary-algebra-2e/pages/1-9-properties-of-real-numbers), [2.3](https://openstax.org/books/elementary-algebra-2e/pages/2-3-solve-equations-with-variables-and-constants-on-both-sides), [2.4](https://openstax.org/books/elementary-algebra-2e/pages/2-4-use-a-general-strategy-to-solve-linear-equations), [2.6](https://openstax.org/books/elementary-algebra-2e/pages/2-6-solve-a-formula-for-a-specific-variable), [2.7](https://openstax.org/books/elementary-algebra-2e/pages/2-7-solve-linear-inequalities), [4.4](https://openstax.org/books/elementary-algebra-2e/pages/4-4-understand-slope-of-a-line), [4.5](https://openstax.org/books/elementary-algebra-2e/pages/4-5-use-the-slope-intercept-form-of-an-equation-of-a-line), [4.6](https://openstax.org/books/elementary-algebra-2e/pages/4-6-find-the-equation-of-a-line), [5.1](https://openstax.org/books/elementary-algebra-2e/pages/5-1-solve-systems-of-equations-by-graphing), [5.2](https://openstax.org/books/elementary-algebra-2e/pages/5-2-solving-systems-of-equations-by-substitution), [5.3](https://openstax.org/books/elementary-algebra-2e/pages/5-3-solve-systems-of-equations-by-elimination), [5.4](https://openstax.org/books/elementary-algebra-2e/pages/5-4-solve-applications-with-systems-of-equations), [6.1](https://openstax.org/books/elementary-algebra-2e/pages/6-1-add-and-subtract-polynomials), [6.2](https://openstax.org/books/elementary-algebra-2e/pages/6-2-use-multiplication-properties-of-exponents), [6.3](https://openstax.org/books/elementary-algebra-2e/pages/6-3-multiply-polynomials), [6.4](https://openstax.org/books/elementary-algebra-2e/pages/6-4-special-products), [6.7](https://openstax.org/books/elementary-algebra-2e/pages/6-7-integer-exponents-and-scientific-notation), [7.1](https://openstax.org/books/elementary-algebra-2e/pages/7-1-greatest-common-factor-and-factor-by-grouping), [7.2](https://openstax.org/books/elementary-algebra-2e/pages/7-2-factor-trinomials-of-the-form-x2-bx-c), [7.4](https://openstax.org/books/elementary-algebra-2e/pages/7-4-factor-special-products), [7.6](https://openstax.org/books/elementary-algebra-2e/pages/7-6-quadratic-equations), [10.3](https://openstax.org/books/elementary-algebra-2e/pages/10-3-solve-quadratic-equations-using-the-quadratic-formula), [10.5](https://openstax.org/books/elementary-algebra-2e/pages/10-5-graphing-quadratic-equations-in-two-variables)
- OpenStax, *Intermediate Algebra 2e*: [2.6](https://openstax.org/books/intermediate-algebra-2e/pages/2-6-solve-compound-inequalities), [2.7](https://openstax.org/books/intermediate-algebra-2e/pages/2-7-solve-absolute-value-inequalities), [3.5](https://openstax.org/books/intermediate-algebra-2e/pages/3-5-relations-and-functions), [3.6](https://openstax.org/books/intermediate-algebra-2e/pages/3-6-graphs-of-functions)

Each lesson also links its own subset inline under "Sources".

## Calculation checks

Every worked example and answer-key value was re-evaluated numerically (substitution into the original equation/expression, polynomial identities checked at several x-values, quadratic-formula roots substituted back, scientific-notation products computed). All 68 checks passed. Word-problem prices and quantities are labeled "illustrative" in the lesson text; no measured or platform results are claimed. No curriculum standards codes were cited.

## Affiliate review

No affiliate links, resource cards, or commercial references were added. `AffiliateOffer`/`AffiliateDisclosure` and resource pages are untouched.

## Validation

| Check | Result |
|---|---|
| `node scripts/generate-content.mjs` (content-site) | pass; internal-link assertion pass |
| `node scripts/generate-content.mjs` (learning-app) | pass |
| Ingestion frontmatter parser on all 8 files | pass |
| Scaffold/TODO residue scan (source + rendered HTML) | 0 hits |
| Internal links in rendered batch pages | 113 checked, 0 unresolved |
| External source links | 29 unique, all HTTP 200 |
| Rendered robots meta | batch pages + `/subject/algebra-i`: none (indexable); `/161-polynomial-functions`, `/subject/geometry`: `noindex, follow` |
| Rendered hub | 8 lessons under "Lessons", no "In development" section |
| `pnpm test` (content-site) | 23/23 pass (4 new Algebra I batch tests) |
| `pnpm check` (content-site, learning-app) | pass |
| `pnpm build` (content-site) | pass (734 static pages); one earlier attempt hit a transient Next.js worker crash (exit 3221226505) and passed unchanged on rerun |
| `pnpm lint` (content-site) | 4 errors, 5 warnings, all pre-existing in files not touched by this batch (`app/page.tsx`, `tools/calculus`, `tools/matrix`, `tools/probability`, `AffiliateOffer.tsx`, `generate-content.mjs`); the modified test file lints clean |

## Not in this batch

- Obsidian mirror copies under `corpus/10 - Learning App Material/Subjects/14 - Algebra I/` were not edited; the generators and ingestion read `corpus/lessons/` only.
- The external backlog CSV (`indexing-reports/learning-lesson-backlog-2026-10-17.csv`) was not modified; it should be regenerated to show these 8 rows as `ok`.
- Search Console indexing requests have not been made.
