# Batch record: statistics-probability-01

- **batch_id:** statistics-probability-01
- **subject:** Statistics & Probability (`/subject/statistics-and-probability`)
- **base commit:** `d388ba3` (Pre-Algebra batch `pre-algebra-01`)
- **date:** 2026-10-18
- **source files:** `corpus/lessons/171-…178-*.md` (generated `content.json` is gitignored and rebuilt by `generate-content.mjs`)
- **selection:** the 8 lessons with `subject: "Statistics & Probability"` and `type: chapter` in `corpus/lessons/`, all `template` / `scaffold`; confirmed against the manifest (8 lessons, 0 indexable, hub gated). `17-statistics-probability-subject-plan.md` (`type: subject-plan`), `readme-17-statistics-probability.md`, and `statistics-and-probability-learning-path.md` are excluded by the generator and were not edited. Other subjects' `17x-*` files (networking) were not touched.

## Lessons

Gate words = the generator's `wordCount` (rendered HTML text, includes KaTeX glyph text). Prose words = source body with `$…$` / `$$…$$` math removed, measured during batch QA.

| Slug | Title (unchanged) | Old gate words | New gate words | New prose words | Examples / misconceptions / practice | Before | After |
|---|---|---|---|---|---|---|---|
| `171-exploring-data-1-variable` | 17.1 - Exploring Data (1-Variable) | 354 | 1820 | 1452 | 3 / 6 / 7 | noindex (scaffold) | indexable |
| `172-exploring-data-2-variable` | 17.2 - Exploring Data (2-Variable) | 354 | 1726 | 1220 | 3 / 6 / 7 | noindex (scaffold) | indexable |
| `173-sampling-experimental-design` | 17.3 - Sampling & Experimental Design | 354 | 1858 | 1781 | 3 / 5 / 7 | noindex (scaffold) | indexable |
| `174-probability` | 17.4 - Probability | 350 | 1621 | 1133 | 3 / 5 / 7 | noindex (scaffold) | indexable |
| `175-discrete-random-variables` | 17.5 - Discrete Random Variables | 354 | 1646 | 1034 | 3 / 6 / 7 | noindex (scaffold) | indexable |
| `176-normal-distribution-sampling-distributions` | 17.6 - Normal Distribution & Sampling Distributions | 356 | 1584 | 1152 | 4 / 5 / 7 | noindex (scaffold) | indexable |
| `177-confidence-intervals` | 17.7 - Confidence Intervals | 352 | 1886 | 1457 | 4 / 6 / 7 | noindex (scaffold) | indexable |
| `178-significance-tests` | 17.8 - Significance Tests | 352 | 2186 | 1576 | 3 / 6 / 7 | noindex (scaffold) | indexable |

Preserved for every lesson: slug, title, `subject: "Statistics & Probability"`, `catalog: k12`, `audience_tier: 9-12`, `chapter` (17.1–17.8), `type: chapter`, `open_source`, prev/next chain. Only the frontmatter `objectives` list changed (same schema; verified with `services/corpus-ingestion/src/frontmatter.ts`). Each lesson has prerequisites, observable objectives, a core explanation with the reasoning behind each formula (why deviations are squared and why $n - 1$; $r$ as an average product of z-scores; why $\sigma/\sqrt{n}$; why the binomial coefficient appears; the test-statistic template), worked examples with intermediate calculations, misconceptions/boundary cases, practice with a collapsible answer key and self-check method, a "Where this fits" section with hub/prev/next/related links, and sources. Lesson scope follows the chapter outline in `17-statistics-probability-subject-plan.md`.

Cross-subject links (all existing indexable routes): `137-statistics-data`, `138-probability-intro`, `145-linear-functions-graphing`, `167-sequences-series-the-binomial-theorem`, `231-statistical-learning-optimization` (17.2 only; that lesson uses MSE loss/linear regression).

Related edit outside the 8 files: `137-statistics-data.md` and `138-probability-intro.md` each had one sentence calling the Statistics & Probability course "still being written". That would be false after this batch (Req 4.3), so the clause was replaced with a short description of what the course adds. No other change to those files; both stay indexable.

## Corpus delta

| Metric | Before | After |
|---|---|---|
| Indexable lessons | 459 | 467 |
| Gated lessons | 181 (placeholder 40, scaffold 141) | 173 (placeholder 40, scaffold 133) |
| Indexable subject hubs | 58 of 81 | 59 of 81 (`statistics-and-probability` promoted, 8/8 lessons) |
| Sitemap URLs | 520 | 529 (+8 lessons, +1 hub) |

Manifest diff (pre-edit regeneration vs. this batch): only the 8 Statistics & Probability lesson entries, the `statistics-and-probability` subject entry, and the `wordCount`/`html` of `137-statistics-data` and `138-probability-intro` changed; 640 lessons before and after. Local links routed to hubs dropped 644 → 620 because the scaffold's `Subject_Plan`/`README`/`LEARNING_PATH` links were removed.

## Evidence sources

All 44 unique URLs cited in the 8 lessons were fetched on 2026-10-18 and returned HTTP 200 with the matching page title (35 OpenStax, 9 NIST). Topic coverage was spot-checked in the fetched page text where a lesson cites a page for a specific point: stratified sampling (1.2), blinding (1.4), influential points (12.6), "first success" geometric definition (4.4), the $n \ge 30$ CLT guideline (7.1), sample-size calculation (8.3), Welch degrees of freedom (10.1), fences/outliers (NIST box plot), IQR (NIST measures of scale), residual plots (NIST 4.4.4), and p-values (NIST 7.1.3.1). Two guessed OpenStax slugs (9.3, 9.4) returned 404 and were replaced with the correct slugs before citing. The ASA p-value statement was considered but not cited because its PDF text could not be verified in this environment.

- OpenStax, *Introductory Statistics 2e*: [1.2](https://openstax.org/books/introductory-statistics-2e/pages/1-2-data-sampling-and-variation-in-data-and-sampling), [1.4](https://openstax.org/books/introductory-statistics-2e/pages/1-4-experimental-design-and-ethics), [2.1](https://openstax.org/books/introductory-statistics-2e/pages/2-1-stem-and-leaf-graphs-stemplots-line-graphs-and-bar-graphs), [2.3](https://openstax.org/books/introductory-statistics-2e/pages/2-3-measures-of-the-location-of-the-data), [2.4](https://openstax.org/books/introductory-statistics-2e/pages/2-4-box-plots), [2.6](https://openstax.org/books/introductory-statistics-2e/pages/2-6-skewness-and-the-mean-median-and-mode), [2.7](https://openstax.org/books/introductory-statistics-2e/pages/2-7-measures-of-the-spread-of-the-data), [3.1](https://openstax.org/books/introductory-statistics-2e/pages/3-1-terminology), [3.2](https://openstax.org/books/introductory-statistics-2e/pages/3-2-independent-and-mutually-exclusive-events), [3.3](https://openstax.org/books/introductory-statistics-2e/pages/3-3-two-basic-rules-of-probability), [3.4](https://openstax.org/books/introductory-statistics-2e/pages/3-4-contingency-tables), [3.5](https://openstax.org/books/introductory-statistics-2e/pages/3-5-tree-and-venn-diagrams), [4.1](https://openstax.org/books/introductory-statistics-2e/pages/4-1-probability-distribution-function-pdf-for-a-discrete-random-variable), [4.2](https://openstax.org/books/introductory-statistics-2e/pages/4-2-mean-or-expected-value-and-standard-deviation), [4.3](https://openstax.org/books/introductory-statistics-2e/pages/4-3-binomial-distribution), [4.4](https://openstax.org/books/introductory-statistics-2e/pages/4-4-geometric-distribution), [6.1](https://openstax.org/books/introductory-statistics-2e/pages/6-1-the-standard-normal-distribution), [6.2](https://openstax.org/books/introductory-statistics-2e/pages/6-2-using-the-normal-distribution), [7.1](https://openstax.org/books/introductory-statistics-2e/pages/7-1-the-central-limit-theorem-for-sample-means-averages), [7.3](https://openstax.org/books/introductory-statistics-2e/pages/7-3-using-the-central-limit-theorem), [8.1](https://openstax.org/books/introductory-statistics-2e/pages/8-1-a-single-population-mean-using-the-normal-distribution), [8.2](https://openstax.org/books/introductory-statistics-2e/pages/8-2-a-single-population-mean-using-the-student-t-distribution), [8.3](https://openstax.org/books/introductory-statistics-2e/pages/8-3-a-population-proportion), [9.1](https://openstax.org/books/introductory-statistics-2e/pages/9-1-null-and-alternative-hypotheses), [9.2](https://openstax.org/books/introductory-statistics-2e/pages/9-2-outcomes-and-the-type-i-and-type-ii-errors), [9.4](https://openstax.org/books/introductory-statistics-2e/pages/9-4-rare-events-the-sample-decision-and-conclusion), [9.5](https://openstax.org/books/introductory-statistics-2e/pages/9-5-additional-information-and-full-hypothesis-test-examples), [10.1](https://openstax.org/books/introductory-statistics-2e/pages/10-1-two-population-means-with-unknown-standard-deviations), [10.4](https://openstax.org/books/introductory-statistics-2e/pages/10-4-matched-or-paired-samples), [11.2](https://openstax.org/books/introductory-statistics-2e/pages/11-2-goodness-of-fit-test), [11.3](https://openstax.org/books/introductory-statistics-2e/pages/11-3-test-of-independence), [12.1](https://openstax.org/books/introductory-statistics-2e/pages/12-1-linear-equations), [12.2](https://openstax.org/books/introductory-statistics-2e/pages/12-2-scatter-plots), [12.3](https://openstax.org/books/introductory-statistics-2e/pages/12-3-the-regression-equation), [12.6](https://openstax.org/books/introductory-statistics-2e/pages/12-6-outliers)
- NIST/SEMATECH *e-Handbook of Statistical Methods*: [1.3.3.7 Box Plot](https://www.itl.nist.gov/div898/handbook/eda/section3/boxplot.htm), [1.3.5.6 Measures of Scale](https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm), [1.3.6.6.1 Normal Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3661.htm), [1.3.6.6.6 Chi-Square Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3666.htm), [1.3.6.6.18 Binomial Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda366i.htm), [1.3.6.7.2 Critical Values of the Student's t Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3672.htm), [4.4.4 How can I tell if a model fits my data?](https://www.itl.nist.gov/div898/handbook/pmd/section4/pmd44.htm), [7.1.3.1 Critical values and p values](https://www.itl.nist.gov/div898/handbook/prc/section1/prc131.htm), [7.1.4 What are confidence intervals?](https://www.itl.nist.gov/div898/handbook/prc/section1/prc14.htm)

Each lesson links its own subset inline under "Sources". Results derived in the lesson rather than cited: deviations summing to zero, least-squares residuals summing to zero, $r = 0$ for the symmetric parabola, the mutually-exclusive-implies-dependent argument, $P(X > k) = (1-p)^k$ for the geometric, and the approximate (not exact) test/interval duality for proportions. Quartiles use the same "median of each half, excluding the overall median when $n$ is odd" convention as 13.7, and 17.1 states that software conventions vary. Normal, $t$, and chi-square values are given to the precision a standard table or calculator gives.

## Calculation checks

Every worked-example and answer-key value was re-evaluated with Python 3.13 / SciPy 1.15.3 / NumPy 2.2.6 in throwaway scripts (deleted after use): means, sample and population variances/SDs, quartiles, IQRs, fences, and resistance comparisons for each data set; unit-conversion effects on center/spread; regression slopes, intercepts, $r$, $r^2$, every residual, the influential-point refit, the z-score product table, and the summary-statistic line; stratified allocations and systematic-sample endpoints; marginal/joint/conditional probabilities, the independence check, Bayes' posterior and its natural-frequency counts, "at least one" and without-replacement products; distribution means/variances, linear transformation and sum rules, binomial and geometric pmf/cdf/mean/SD; normal probabilities, percentiles, empirical-rule areas, CLT and $\hat p$ probabilities; $z^*$/$t^*$ critical values, every interval endpoint (including the Welch df $\approx 43.0$ and the conservative-df interval), and sample-size results including that $n = 1067$ misses and $n = 1068$ meets the $0.03$ target; z, t, paired-t, and chi-square statistics and p-values, the exact binomial p-value ($\approx 0.057$) contrasted with the z-test p-value ($\approx 0.0455$), and the power example ($\approx 0.64$). 220 checks, 0 failures.

All data sets and scenarios (study hours, test scores, temperatures, commute times, batteries, bottles, polls, the screening test, the raffle, the team's goals, the free-throw shooter, the coin, the die, the spinner) are labeled "illustrative" in the lesson text; the screening-test example explicitly says its rates are not data for any real test. No measured, platform, or study results are claimed, and no curriculum standards codes were cited. The lessons describe calculator functions generically and do not describe any Learning App feature.

## Affiliate review

No affiliate links, resource cards, or commercial references were added. `AffiliateOffer`/`AffiliateDisclosure` and resource pages are untouched. The external links in the subject plan (Khan Academy, StatQuest, StatKey, etc.) were not copied into the lessons.

## Validation

| Check | Result |
|---|---|
| `node scripts/generate-content.mjs` (content-site) | pass; internal-link assertion pass |
| `node scripts/generate-content.mjs` (learning-app) | pass (640 lessons, 81 subjects) |
| Ingestion frontmatter parser (`parseLessonMarkdown`, via `node --experimental-strip-types`) on all 8 files | pass; title/subject/catalog/tier/chapter preserved, 4 objectives each |
| Frontmatter diff vs. `d388ba3` | only `objectives` changed in all 8 files |
| Scaffold/TODO residue scan (manifest HTML + prerendered HTML) | 0 hits; no `katex-error`; no stray unrendered `$` |
| Internal links | 49 lesson-body links in the manifest (0 unresolved) and 205 links (26 unique routes) in the rendered batch pages + hub + 13.7/13.8; 0 unresolved page routes |
| External source links | 44 unique, all HTTP 200 |
| Rendered robots meta | 8 batch pages + `/subject/statistics-and-probability`: none (indexable), canonical set; negative control `/app-024-fractions-concepts-operations`: `noindex, follow` |
| Rendered hub | links all 8 lessons, no "In development" section |
| Prerendered `sitemap.xml` | 529 URLs; all 8 lessons + hub present; negative control absent |
| `pnpm test` (content-site) | 39/39 pass (4 new Statistics & Probability batch tests) |
| `pnpm check` (content-site, learning-app) | pass |
| `pnpm build` (content-site) | pass |
| `pnpm lint` (content-site) | 4 errors, 5 warnings, identical to the pre-existing set recorded in earlier batches (`page.tsx`, `tools/calculus`, `tools/matrix`, `tools/probability`, `AffiliateOffer.tsx`, `generate-content.mjs`); the modified test file lints clean |
| `pnpm test` (corpus-ingestion) | not run: same pre-existing `TS2307 Cannot find module '@learning-platform/corpus-types'` build blocker recorded in algebra-ii-01; unrelated to this batch |

## Production observation (previous batch)

On 2026-10-18, before this batch was pushed, `https://learning.nepa-ai.com/sitemap.xml` served 520 URLs including `/subject/pre-algebra`; `/131-ratios-rates-proportions` rendered without a robots `noindex` and without scaffold text. Pre-Algebra batch `d388ba3` has therefore propagated. `/171-exploring-data-1-variable` was still `noindex, follow` with scaffold text and `/subject/statistics-and-probability` was absent from the sitemap, as expected before this batch deploys.

## Not in this batch

- Obsidian mirror copies under `corpus/10 - Learning App Material/Subjects/` were not edited; the generators and ingestion read `corpus/lessons/` only.
- The external backlog CSV/MD (outside this repository) was not modified; it should be regenerated to show these 8 rows (and the 32 earlier math rows) as `ok`.
- Search Console indexing requests have not been made.
