# Batch record: geometry-01

- **batch_id:** geometry-01
- **subject:** Geometry (`/subject/geometry`)
- **base commit:** `f5f0f2a` (Algebra II & Pre-Calculus batch `algebra-ii-01`)
- **date:** 2026-10-18
- **source files:** `corpus/lessons/151-…158-*.md` (generated `content.json` is gitignored and rebuilt by `generate-content.mjs`)
- **selection:** the 8 rows for subject `geometry` in `indexing-reports/learning-lesson-backlog-2026-10-17.csv`, all `template` / `scaffold`; confirmed against the manifest (8 lessons, 0 indexable, hub gated). `15-geometry-subject-plan.md` is `type: subject-plan`, excluded by the generator, and was not edited.

## Lessons

Gate words = the generator's `wordCount` (rendered HTML text, includes KaTeX glyph text). Prose words = source body with `$…$` / `$$…$$` math removed, measured during batch QA.

| Slug | Title (unchanged) | Old gate words | New gate words | New prose words | Examples / misconceptions / practice | Before | After |
|---|---|---|---|---|---|---|---|
| `151-foundations-of-geometry` | 15.1 - Foundations of Geometry | 354 | 1852 | 1262 | 5 / 6 / 7 | noindex (scaffold) | indexable |
| `152-reasoning-proof` | 15.2 - Reasoning & Proof | 352 | 1714 | 1423 | 6 / 6 / 7 | noindex (scaffold) | indexable |
| `153-parallel-perpendicular-lines` | 15.3 - Parallel & Perpendicular Lines | 354 | 1823 | 1344 | 5 / 6 / 7 | noindex (scaffold) | indexable |
| `154-triangles` | 15.4 - Triangles | 350 | 1833 | 1397 | 6 / 6 / 7 | noindex (scaffold) | indexable |
| `155-similarity-proportions` | 15.5 - Similarity & Proportions | 352 | 1688 | 1148 | 5 / 6 / 8 | noindex (scaffold) | indexable |
| `156-right-triangles-trigonometry` | 15.6 - Right Triangles & Trigonometry | 354 | 1706 | 1125 | 6 / 7 / 8 | noindex (scaffold) | indexable |
| `157-circles` | 15.7 - Circles | 350 | 1791 | 1327 | 6 / 7 / 8 | noindex (scaffold) | indexable |
| `158-area-volume-coordinate-geometry` | 15.8 - Area, Volume & Coordinate Geometry | 356 | 1982 | 1311 | 7 / 7 / 8 | noindex (scaffold) | indexable |

Preserved for every lesson: slug, title, `subject: Geometry`, `catalog: k12`, `audience_tier: 9-12`, `chapter` (15.1–15.8), `type: chapter`, `open_source`, prev/next chain. Only the frontmatter `objectives` list changed (same schema; verified with `services/corpus-ingestion/src/frontmatter.ts`). Each lesson has prerequisites, objectives, definitions/core explanation with the geometric reasoning behind each result (proof sketches for the triangle sum, inscribed angle, and Pythagorean theorems; visual derivations of area formulas and Cavalieri's principle), worked examples, misconceptions/boundary cases, practice with a collapsible answer key and self-check method, a "Where this fits" section with hub/prev/next/related links, and sources. Lesson scope follows the chapter outline in `15-geometry-subject-plan.md`.

Cross-subject links added (all existing public routes): Algebra I 14.2/14.5/14.6/14.8; Algebra II 16.4/16.5/16.6; `131-ratios-rates-proportions`, `app-111-propositional-logic`, `app-112-predicate-logic-proof-techniques` (still gated, routes valid); `24-linear-transformations-change-of-basis`, `13-single-variable-integration`.

## Corpus delta

| Metric | Before | After |
|---|---|---|
| Indexable lessons | 443 | 451 |
| Gated lessons | 197 (placeholder 40, scaffold 157) | 189 (placeholder 40, scaffold 149) |
| Indexable subject hubs | 56 of 81 | 57 of 81 (`geometry` promoted, 8/8 lessons) |
| Sitemap URLs | 502 | 511 (+8 lessons, +1 hub) |

Manifest diff: only the 8 Geometry lesson entries and the `geometry` subject entry changed; 640 lessons before and after. Local links routed to hubs dropped 692 → 668 because the scaffold's `Subject_Plan`/`README` links were removed.

## Evidence sources

All 40 URLs fetched on 2026-10-18 and confirmed HTTP 200 with the matching page title. OpenStax has no dedicated high-school Geometry text, so OpenStax *Contemporary Mathematics* ch. 2 (logic) and ch. 10 (geometry) are supplemented by other OpenStax titles and by D. E. Joyce's edition of Euclid's *Elements* (Clark University) for the classical theorems.

- OpenStax, *Contemporary Mathematics*: [2.1](https://openstax.org/books/contemporary-mathematics/pages/2-1-statements-and-quantifiers), [2.4](https://openstax.org/books/contemporary-mathematics/pages/2-4-truth-tables-for-the-conditional-and-biconditional), [2.5](https://openstax.org/books/contemporary-mathematics/pages/2-5-equivalent-statements), [2.7](https://openstax.org/books/contemporary-mathematics/pages/2-7-logical-arguments), [10.1](https://openstax.org/books/contemporary-mathematics/pages/10-1-points-lines-and-planes), [10.2](https://openstax.org/books/contemporary-mathematics/pages/10-2-angles), [10.3](https://openstax.org/books/contemporary-mathematics/pages/10-3-triangles), [10.4](https://openstax.org/books/contemporary-mathematics/pages/10-4-polygons-perimeter-and-circumference), [10.5](https://openstax.org/books/contemporary-mathematics/pages/10-5-tessellations), [10.6](https://openstax.org/books/contemporary-mathematics/pages/10-6-area), [10.7](https://openstax.org/books/contemporary-mathematics/pages/10-7-volume-and-surface-area), [10.8](https://openstax.org/books/contemporary-mathematics/pages/10-8-right-triangle-trigonometry)
- OpenStax, *Intermediate Algebra 2e*: [3.2](https://openstax.org/books/intermediate-algebra-2e/pages/3-2-slope-of-a-line), [3.3](https://openstax.org/books/intermediate-algebra-2e/pages/3-3-find-the-equation-of-a-line), [11.1](https://openstax.org/books/intermediate-algebra-2e/pages/11-1-distance-and-midpoint-formulas-circles)
- OpenStax, *Prealgebra 2e*: [9.3](https://openstax.org/books/prealgebra-2e/pages/9-3-use-properties-of-angles-triangles-and-the-pythagorean-theorem), [9.6](https://openstax.org/books/prealgebra-2e/pages/9-6-solve-geometry-applications-volume-and-surface-area) (cone and sphere formulas, which 10.7 does not cover)
- OpenStax, *Algebra and Trigonometry 2e*: [7.2](https://openstax.org/books/algebra-and-trigonometry-2e/pages/7-2-right-triangle-trigonometry)
- Euclid, *Elements*, ed. D. E. Joyce: [Book I defs/postulates](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/bookI.html); Props. [I.5](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/propI5.html), [I.15](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/propI15.html), [I.20](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/propI20.html), [I.27](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/propI27.html), [I.28](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/propI28.html), [I.29](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/propI29.html), [I.32](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/propI32.html), [I.47](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/propI47.html), [I.48](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/propI48.html), [III.3](https://mathcs.clarku.edu/~djoyce/java/elements/bookIII/propIII3.html), [III.18](https://mathcs.clarku.edu/~djoyce/java/elements/bookIII/propIII18.html), [III.20](https://mathcs.clarku.edu/~djoyce/java/elements/bookIII/propIII20.html), [III.21](https://mathcs.clarku.edu/~djoyce/java/elements/bookIII/propIII21.html), [III.31](https://mathcs.clarku.edu/~djoyce/java/elements/bookIII/propIII31.html), [III.35](https://mathcs.clarku.edu/~djoyce/java/elements/bookIII/propIII35.html), [III.36](https://mathcs.clarku.edu/~djoyce/java/elements/bookIII/propIII36.html), [VI.2](https://mathcs.clarku.edu/~djoyce/java/elements/bookVI/propVI2.html), [VI.4](https://mathcs.clarku.edu/~djoyce/java/elements/bookVI/propVI4.html), [VI.19](https://mathcs.clarku.edu/~djoyce/java/elements/bookVI/propVI19.html), [XII.7](https://mathcs.clarku.edu/~djoyce/java/elements/bookXII/propXII7.html), [XII.10](https://mathcs.clarku.edu/~djoyce/java/elements/bookXII/propXII10.html)

Each lesson links its own subset inline under "Sources". Results not stated in these sources are derived in the lesson itself rather than cited: HL congruence (reduced to SSS via the Pythagorean theorem), the SSA counterexample (solved explicitly), the point-to-line distance formula (checked against the perpendicular-foot construction), the shoelace formula (checked by triangle decomposition), and the triangle midsegment theorem (special case of the side-splitter/SAS similarity).

## Calculation checks

Every worked-example and answer-key value was re-evaluated in a throwaway Node script (deleted after use): segment/angle equations substituted back; distances, midpoints and missing endpoints recomputed; $n^2 - n + 41$ tested prime for $n = 1…40$ and composite at $41$; slopes, perpendicular feet, and point-to-line distances computed both ways; triangle angle sums, triangle inequalities, centroid 2:1 ratio and right-triangle circumcenter distances; both SSA solutions $t = 5\sqrt3 \pm \sqrt{11}$ checked to give $BC = 6$; similarity ratios, side-splitter lengths, dilation images, map scale and $k^2$ areas; Pythagorean results, special-triangle lengths, all trig values and inverse-trig angles in degree mode (plus the radian-mode warning value); arc lengths, sector areas, power-of-a-point products, and completed-square circle equations compared with the general form at sample points; shoelace areas, solid volumes/surface areas, a general-parallelogram diagonal midpoint check, rotation images and preserved side lengths, and the practice square. 97 checks, 0 failures.

Shadow, building, cliff, ladder, and window measurements are labeled "illustrative" in the lesson text; no measured or platform results are claimed. No curriculum standards codes were cited.

## Affiliate review

No affiliate links, resource cards, or commercial references were added. `AffiliateOffer`/`AffiliateDisclosure` and resource pages are untouched.

## Validation

| Check | Result |
|---|---|
| `node scripts/generate-content.mjs` (content-site) | pass; internal-link assertion pass |
| `node scripts/generate-content.mjs` (learning-app) | pass (640 lessons, 81 subjects) |
| Ingestion frontmatter parser (`parseLessonMarkdown`, via `node --experimental-strip-types`) on all 8 files | pass; title/subject/catalog/tier/chapter preserved, 4 objectives each |
| Frontmatter diff vs. `f5f0f2a` | only `objectives` changed in all 8 files |
| Scaffold/TODO residue scan (source + rendered HTML) | 0 hits; no `katex-error` in batch HTML; no unrendered `$` |
| Internal links | 65 lesson-body links in the manifest and 145 links in the rendered batch pages + hub; 0 unresolved |
| External source links | 40 unique, all HTTP 200 |
| Rendered robots meta | 8 batch pages + `/subject/geometry`: none (indexable), canonical set; negative controls `/131-ratios-rates-proportions`, `/subject/pre-algebra`: `noindex, follow` |
| Rendered hub | links all 8 lessons, no "In development" section |
| Prerendered `sitemap.xml` | 511 URLs; all 8 lessons + hub present; gated Pre-Algebra lesson and hub absent |
| `pnpm test` (content-site) | 31/31 pass (4 new Geometry batch tests) |
| `pnpm check` (content-site, learning-app) | pass |
| `pnpm build` (content-site) | pass |
| `pnpm lint` (content-site) | 4 errors, 5 warnings, identical to the pre-existing set recorded in algebra-i-01/algebra-ii-01; the modified test file lints clean |
| `pnpm test` (corpus-ingestion) | not run: same pre-existing `TS2307 Cannot find module '@learning-platform/corpus-types'` build blocker recorded in algebra-ii-01; unrelated to this batch |

## Not in this batch

- Obsidian mirror copies under `corpus/10 - Learning App Material/Subjects/15 - Geometry/` were not edited; the generators and ingestion read `corpus/lessons/` only.
- The external backlog CSV/MD (`websites/Local Sites/indexing-reports/`, outside this repository) was not modified; it should be regenerated to show these 8 rows (and the 16 Algebra I/II rows) as `ok`.
- The Early Numeracy lesson `app-028-geometry-coordinate-plane` belongs to a different subject and was not touched.
- Search Console indexing requests have not been made; production deployment has not been verified from this worktree.
