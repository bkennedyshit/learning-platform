# Batch record: early-numeracy-01

- **batch_id:** early-numeracy-01
- **subject:** Early Numeracy K-5 (`/subject/early-numeracy-k-5`)
- **base commit:** `3e049d0` (Statistics & Probability batch `statistics-probability-01`)
- **date:** 2026-10-18
- **source files:** `corpus/lessons/app-021-…app-028-*.md` (generated `content.json` is gitignored and rebuilt by `generate-content.mjs`)
- **selection:** the 8 lessons with `subject: "Early Numeracy K-5"` and `type: chapter` in `corpus/lessons/`, all `template` / `scaffold`; confirmed against the pre-edit manifest (8 lessons, 0 indexable, hub gated). `app-02-early-numeracy-k-5-subject-plan.md` (`type: subject-plan`), `app-02-early-numeracy-k-5-learning-path.md`, and `readme-02-early-numeracy-k-5.md` are excluded by the generator and were not edited.

## Lessons

Gate words = the generator's `wordCount` (rendered HTML text, includes KaTeX glyph text). Prose words = source body with `$…$` / `$$…$$` math removed, measured during batch QA.

| Slug | Title (unchanged) | Old gate words | New gate words | New prose words | Examples / misconceptions / practice | Before | After |
|---|---|---|---|---|---|---|---|
| `app-021-number-sense-counting` | APP-02.1 — Number Sense & Counting | 354 | 1744 | 1804 | 3 / 6 / 7 | noindex (scaffold) | indexable |
| `app-022-addition-subtraction` | APP-02.2 — Addition & Subtraction | 352 | 1567 | 1632 | 3 / 5 / 7 | noindex (scaffold) | indexable |
| `app-023-multiplication-division` | APP-02.3 — Multiplication & Division | 352 | 1594 | 1598 | 3 / 5 / 8 | noindex (scaffold) | indexable |
| `app-024-fractions-concepts-operations` | APP-02.4 — Fractions — Concepts & Operations | 356 | 1733 | 1363 | 3 / 5 / 7 | noindex (scaffold) | indexable |
| `app-025-fractions-advanced-operations` | APP-02.5 — Fractions — Advanced Operations | 356 | 1795 | 1347 | 3 / 5 / 9 | noindex (scaffold) | indexable |
| `app-026-decimals-place-value` | APP-02.6 — Decimals & Place Value | 354 | 1484 | 1468 | 3 / 5 / 8 | noindex (scaffold) | indexable |
| `app-027-measurement-data` | APP-02.7 — Measurement & Data | 352 | 1674 | 1643 | 3 / 5 / 7 | noindex (scaffold) | indexable |
| `app-028-geometry-coordinate-plane` | APP-02.8 — Geometry & Coordinate Plane | 354 | 1725 | 1807 | 3 / 5 / 7 | noindex (scaffold) | indexable |

Preserved for every lesson: slug, title, `subject: "Early Numeracy K-5"`, `catalog: k12`, `audience_tier: 9-12`, `chapter` (2.1–2.8), `type: chapter`, `open_source`, prev/next chain (`app-021` → … → `app-028`). Only the frontmatter `objectives` list changed (same schema; verified with `services/corpus-ingestion/src/frontmatter.ts`).

**Metadata note (not changed):** the existing `audience_tier` for all 8 lessons is `9-12`, although the content is K-5. The task required preserving the tier, so it was left as-is; correcting it would be a separate schema/metadata decision (the tier vocabulary and any consumers of it should be checked first).

**Audience design:** each lesson addresses the learner directly in short sentences and adds `> **Adult note:**` boxes for the parent/tutor/teacher (materials, what to watch for). Every lesson has: prerequisites with links, 4 observable objectives, concrete manipulatives or everyday models (counters, ten frames, bundled sticks, base-ten blocks, arrays on grid paper, fraction strips, number lines, hundreds grids, coins, rulers, unit squares/cubes, paper folding, coordinate grids), worked examples with intermediate steps and a check, age-appropriate misconceptions/boundary cases, practice with a collapsible answer key and an "Adult self-check", a "Where this fits" section with hub/prev/next/related links, and sources. Scope follows the chapter outline in `app-02-early-numeracy-k-5-subject-plan.md`. Topics in that outline that the CCSS places after grade 5 are labeled as previews instead of being taught as grade-level work: general fraction ÷ fraction (grade 6, previewed in 2.5), scientific notation (2.6, "taught in later grades"), and four-quadrant graphing (grade 6, previewed in 2.8 with links to 13.2/13.6). Multiplication facts are taught to 10 × 10 (the CCSS grade 3 expectation is all products of two one-digit numbers); the plan's "0-12" was not asserted.

Cross-subject links (all existing indexable routes): `132-the-number-system`, `133-fractions-decimals-percent`, `136-geometry-foundations`, `137-statistics-data`, `151-foundations-of-geometry`. Each linked lesson was read to confirm it covers what the link text says (e.g. 13.3 has the reciprocal rule; 13.6 plots points in all four quadrants; 13.2 extends the number line to negatives). No other lesson in the corpus referred to Early Numeracy, so no other files needed editing.

## Corpus delta

| Metric | Before | After |
|---|---|---|
| Indexable lessons | 467 | 475 |
| Gated lessons | 173 (placeholder 40, scaffold 133) | 165 (placeholder 40, scaffold 125) |
| Indexable subject hubs | 59 of 81 | 60 of 81 (`early-numeracy-k-5` promoted, 8/8 lessons) |
| Sitemap URLs (prerendered) | 529 | 538 (+8 lessons, +1 hub) |

Manifest diff (pre-edit regeneration vs. this batch): only the 8 Early Numeracy lesson entries and the `early-numeracy-k-5` subject entry changed; 640 lessons before and after. Local links routed to hubs dropped 620 → 596 because the scaffold's `Subject_Plan`/`README`/`LEARNING_PATH` links were removed.

## Evidence sources

All 54 unique URLs cited in the 8 lessons were fetched on 2026-10-18 and returned HTTP 200 with the matching page title (19 Common Core State Standards Initiative domain pages, 19 OpenStax *Prealgebra 2e* sections, and 16 *Mathematics for Elementary Teachers* chapters). Standards are cited only as domain pages; **no standards codes are used in the lessons**. Statements about grade placement were checked against the fetched page text: counting to 100 by ones and tens and counting up to 20 objects (K.CC); decomposing numbers ≤ 10 into pairs (K.OA); count to 120, tens and ones, compare with >, =, < (1.NBT); story types and the meaning of the equal sign (1.OA); add/subtract within 1,000 (2.NBT); one-digit products from memory and properties as strategies (3.OA); fractions on a number line, whole numbers as fractions, grade 3 denominators (3.NF); like denominators, mixed numbers, decimal notation for tenths/hundredths, "unlike denominators in general is not a requirement at this grade" (4.NF); ten times the place to the right, ≤ 1,000,000 (4.NBT); unlike denominators, fraction as division, scaling, dividing unit fractions (5.NF); powers of ten with exponents, decimals to thousandths (5.NBT); measuring with two units, picture/bar graphs (2.MD); tiling, perimeter, same perimeter/different area (3.MD); conversion tables, line plots in ½, ¼, ⅛ (4.MD); unit cubes, V = l × w × h, additive volume (5.MD); quadrilateral subcategories (3.G); parallel/perpendicular, lines of symmetry (4.G); first-quadrant graphing and the hierarchy of figures (5.G); fraction ÷ fraction and four quadrants (6.NS). Content claims spot-checked in OpenStax: division by zero is undefined (7.4); remainder notation "R" (1.5); ordered pair (x, y) and quadrants (11.1); tenths place vs. tens place (5.1); U.S. and metric equivalences including 5,280 ft/mi, 16 oz/lb, 4 qt/gal, 2 pt/qt, 2 c/pt, 1,000 m/km, 100 cm/m, 1,000 mL/L (7.5); trapezoid defined as two parallel sides and two that are not (9.4). In Manes: triangle classification by sides and angles, line of symmetry as mirror-image halves, polyhedron faces/edges/vertices, and the quotative ("how many groups of 3 in 18") meaning of division.

Not verified and therefore not claimed: Illustrative Mathematics K-5 lesson pages (the public preview page loaded but lesson URLs were not confirmed), OpenLearn (HTTP 403 from this environment), and NCTM position statements (not needed). The trapezoid note in 2.8 states only that textbooks do not all use the same definition and tells the adult to follow the learner's curriculum; no alternative definition is attributed to a named source. No developmental-age claims (e.g. "children can subitize N by age X") are made; subitizing is defined, not benchmarked.

- Common Core State Standards Initiative: [K.CC](https://www.thecorestandards.org/Math/Content/K/CC/), [K.OA](https://www.thecorestandards.org/Math/Content/K/OA/), [1.OA](https://www.thecorestandards.org/Math/Content/1/OA/), [1.NBT](https://www.thecorestandards.org/Math/Content/1/NBT/), [2.NBT](https://www.thecorestandards.org/Math/Content/2/NBT/), [2.MD](https://www.thecorestandards.org/Math/Content/2/MD/), [3.OA](https://www.thecorestandards.org/Math/Content/3/OA/), [3.NF](https://www.thecorestandards.org/Math/Content/3/NF/), [3.MD](https://www.thecorestandards.org/Math/Content/3/MD/), [3.G](https://www.thecorestandards.org/Math/Content/3/G/), [4.NBT](https://www.thecorestandards.org/Math/Content/4/NBT/), [4.NF](https://www.thecorestandards.org/Math/Content/4/NF/), [4.MD](https://www.thecorestandards.org/Math/Content/4/MD/), [4.G](https://www.thecorestandards.org/Math/Content/4/G/), [5.NBT](https://www.thecorestandards.org/Math/Content/5/NBT/), [5.NF](https://www.thecorestandards.org/Math/Content/5/NF/), [5.MD](https://www.thecorestandards.org/Math/Content/5/MD/), [5.G](https://www.thecorestandards.org/Math/Content/5/G/), [6.NS](https://www.thecorestandards.org/Math/Content/6/NS/) (domain pages; labels here are page names, not cited standard codes)
- OpenStax, *Prealgebra 2e*: [1.1](https://openstax.org/books/prealgebra-2e/pages/1-1-introduction-to-whole-numbers), [1.2](https://openstax.org/books/prealgebra-2e/pages/1-2-add-whole-numbers), [1.3](https://openstax.org/books/prealgebra-2e/pages/1-3-subtract-whole-numbers), [1.4](https://openstax.org/books/prealgebra-2e/pages/1-4-multiply-whole-numbers), [1.5](https://openstax.org/books/prealgebra-2e/pages/1-5-divide-whole-numbers), [4.1](https://openstax.org/books/prealgebra-2e/pages/4-1-visualize-fractions), [4.2](https://openstax.org/books/prealgebra-2e/pages/4-2-multiply-and-divide-fractions), [4.4](https://openstax.org/books/prealgebra-2e/pages/4-4-add-and-subtract-fractions-with-common-denominators), [4.5](https://openstax.org/books/prealgebra-2e/pages/4-5-add-and-subtract-fractions-with-different-denominators), [4.6](https://openstax.org/books/prealgebra-2e/pages/4-6-add-and-subtract-mixed-numbers), [5.1](https://openstax.org/books/prealgebra-2e/pages/5-1-decimals), [5.2](https://openstax.org/books/prealgebra-2e/pages/5-2-decimal-operations), [7.2](https://openstax.org/books/prealgebra-2e/pages/7-2-commutative-and-associative-properties), [7.3](https://openstax.org/books/prealgebra-2e/pages/7-3-distributive-property), [7.4](https://openstax.org/books/prealgebra-2e/pages/7-4-properties-of-identity-inverses-and-zero), [7.5](https://openstax.org/books/prealgebra-2e/pages/7-5-systems-of-measurement), [9.4](https://openstax.org/books/prealgebra-2e/pages/9-4-use-properties-of-rectangles-triangles-and-trapezoids), [9.6](https://openstax.org/books/prealgebra-2e/pages/9-6-solve-geometry-applications-volume-and-surface-area), [11.1](https://openstax.org/books/prealgebra-2e/pages/11-1-use-the-rectangular-coordinate-system)
- Michelle Manes, *Mathematics for Elementary Teachers* (University of Hawaiʻi Pressbooks): [Dots and Boxes](https://pressbooks.oer.hawaii.edu/mathforelementaryteachers/chapter/dots-and-boxes/), [Addition: Dots and Boxes](https://pressbooks.oer.hawaii.edu/mathforelementaryteachers/chapter/addition-dots-and-boxes/), [Subtraction: Dots and Boxes](https://pressbooks.oer.hawaii.edu/mathforelementaryteachers/chapter/subtraction-dots-and-boxes/), [Division Explorations](https://pressbooks.oer.hawaii.edu/mathforelementaryteachers/chapter/division-explorations/), [Properties of Operations](https://pressbooks.oer.hawaii.edu/mathforelementaryteachers/chapter/properties-of-operations/), [Area Model for Multiplication](https://pressbooks.oer.hawaii.edu/mathforelementaryteachers/chapter/area-model-for-multiplication/), [What is a Fraction?](https://pressbooks.oer.hawaii.edu/mathforelementaryteachers/chapter/what-is-a-fraction/), [The Key Fraction Rule](https://pressbooks.oer.hawaii.edu/mathforelementaryteachers/chapter/the-key-fraction-rule/), [Adding and Subtracting Fractions](https://pressbooks.oer.hawaii.edu/mathforelementaryteachers/chapter/adding-and-subtracting-fractions/), [Multiplying Fractions](https://pressbooks.oer.hawaii.edu/mathforelementaryteachers/chapter/multiplying-fractions/), [Dividing Fractions: Meaning](https://pressbooks.oer.hawaii.edu/mathforelementaryteachers/chapter/dividing-fractions-meaning/), [Decimals](https://pressbooks.oer.hawaii.edu/mathforelementaryteachers/chapter/decimals/), [Operations on Decimals](https://pressbooks.oer.hawaii.edu/mathforelementaryteachers/chapter/operations-on-decimals/), [Triangles and Quadrilaterals](https://pressbooks.oer.hawaii.edu/mathforelementaryteachers/chapter/triangles-and-quadrilaterals/), [Symmetry](https://pressbooks.oer.hawaii.edu/mathforelementaryteachers/chapter/symmetry/), [Platonic Solids](https://pressbooks.oer.hawaii.edu/mathforelementaryteachers/chapter/platonic-solids/)

Each lesson links its own subset inline under "Sources". Results derived in the lessons rather than cited: the make-a-ten and near-doubles decompositions, regrouping steps, the 6 × 7 and 7 × 8 distributive splits, the × 9 pattern, why 6 ÷ 0 has no answer, splitting parts to make equivalent fractions, the area-model explanation of fraction multiplication, $3 \div \tfrac14 = 3 \times 4$ as a pattern preview, digit shifts for × / ÷ powers of ten, and V − E + F = 2 used only as a counting check for the four listed polyhedra.

## Calculation checks

Every worked-example and answer-key value was re-evaluated with Python 3.13 (`fractions.Fraction` for exact fraction/decimal arithmetic) in a throwaway script (deleted after use): counts, skip-count sequences, comparisons and number bonds (2.1); fact strategies, 47 + 38, 403 − 158, 365 + 278, 500 − 237, the 52 − 27 error case, true/false equations, and story answers (2.2); all products, quotients, remainders (14 ÷ 4, 23 ÷ 4, 17 ÷ 5) and distributive splits (2.3); every equivalence, comparison, like-denominator sum/difference, and mixed-number conversion (2.4); unlike-denominator sums/differences, mixed-number subtraction with back-check, fraction × whole, fraction × fraction, scaling, unit-fraction divisions, and fraction-to-decimal conversions (2.5); expanded forms, decimal comparisons and ordering, decimal sums/differences, and every power-of-ten product/quotient (2.6); perimeters, areas, the 12 m fence rectangles, volumes, unit conversions, line-plot range and sum, picture-graph scale, and all factor pairs of 36 with perimeters (2.7); face/edge/vertex counts with V − E + F, coordinate moves, distances, and the ABCD rectangle's perimeter/area (2.8). 153 checks, 0 failures.

All stories and data sets (shells, birds, marbles, stickers, crayons, muffins, the car trip, the recipe, the walks, the ribbon, the rice, the garden bed, the pencil and water bottle, the fence, the pencils' lengths, plant heights, the apple picture graph, the map grid) are labeled "illustrative" in the lesson text. No measured, platform, or study results are claimed. The lessons do not describe any Learning App feature.

## Affiliate review

No affiliate links, resource cards, or commercial references were added. `AffiliateOffer`/`AffiliateDisclosure` and resource pages are untouched. The external resource list in the subject plan (Khan Academy, Zearn, Dreambox, etc.) was not copied into the lessons.

## Validation

| Check | Result |
|---|---|
| `node scripts/generate-content.mjs` (content-site) | pass; internal-link assertion pass |
| `node scripts/generate-content.mjs` (learning-app) | pass (640 lessons, 81 subjects) |
| Ingestion frontmatter parser (`parseLessonMarkdown`, via `node --experimental-strip-types`) on all 8 files vs. `3e049d0` | pass; every non-objective field identical; 4 objectives each |
| Scaffold/TODO residue scan (manifest HTML + prerendered HTML) | 0 hits for `System Overlay`, `foundational building block`, `Ready for expansion`, `TODO`, `Visual Anchor`, `Subject_Plan`; no `katex-error`; no stray unrendered `$` |
| Internal links | 57 lesson-body links in the manifest (0 unresolved) and 146 links (15 unique routes) in the rendered 8 pages + hub; 0 unresolved against the 731 prerendered routes |
| External source links | 54 unique, all HTTP 200 |
| Rendered robots meta | 8 batch pages + `/subject/early-numeracy-k-5`: none (indexable), canonical set; negative control `/app-031-living-vs-non-living-basic-needs`: `noindex, follow` |
| Rendered hub | links all 8 lessons, no "In development" section |
| Prerendered `sitemap.xml` | 538 URLs; all 8 lessons + hub present; negative control absent |
| `pnpm test` (content-site) | 43/43 pass (4 new Early Numeracy batch tests, including an "Adult note" assertion) |
| `pnpm check` (content-site, learning-app) | pass |
| `pnpm build` (content-site) | pass |
| `pnpm lint` (content-site) | 4 errors, 5 warnings, identical to the pre-existing set recorded in earlier batches (`page.tsx`, `tools/calculus`, `tools/matrix`, `tools/probability`, `AffiliateOffer.tsx`, `generate-content.mjs`); the modified test file lints clean |
| `pnpm test` (corpus-ingestion) | not run: same pre-existing `TS2307 Cannot find module '@learning-platform/corpus-types'` build blocker recorded in algebra-ii-01; unrelated to this batch |

## Production observation (previous batch)

On 2026-10-18, before this batch was pushed, `https://learning.nepa-ai.com/sitemap.xml` served 529 URLs including `/subject/statistics-and-probability`, and `/171-exploring-data-1-variable` rendered without a robots `noindex` and without scaffold text. Statistics & Probability batch `3e049d0` has therefore propagated. `/app-021-number-sense-counting` was still `noindex, follow` with scaffold text and `/subject/early-numeracy-k-5` was absent from the sitemap, as expected before this batch deploys.

## Not in this batch

- `audience_tier: 9-12` on the Early Numeracy lessons was preserved, not corrected (see metadata note).
- Obsidian mirror copies under `corpus/10 - Learning App Material/Subjects/` were not edited; the generators and ingestion read `corpus/lessons/` only.
- The external backlog CSV/MD (outside this repository) was not modified; it should be regenerated to show these 8 rows (and the 40 earlier math rows) as `ok`.
- Search Console indexing requests have not been made.
