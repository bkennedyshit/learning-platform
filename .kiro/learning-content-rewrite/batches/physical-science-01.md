# Batch record: physical-science-01

- **batch_id:** physical-science-01
- **subject:** Physical Science K-8 (`/subject/physical-science-k-8`)
- **base commit:** `94380ac` (Early Numeracy batch `early-numeracy-01`)
- **date:** 2026-10-18
- **source files:** `corpus/lessons/app-041-…app-048-*.md` (generated `content.json` is gitignored and rebuilt by `generate-content.mjs`)
- **selection:** the 8 lessons with `subject: "Physical Science K-8"` and `type: chapter` in `corpus/lessons/`, all `template` / `scaffold`; confirmed against the pre-edit manifest (8 lessons, 0 indexable, hub gated, each 352–358 gate words). `app-04-physical-science-k-8-subject-plan.md` (`type: subject-plan`), `app-04-physical-science-k-8-learning-path.md`, and `readme-04-physical-science-k-8.md` are excluded by the generator and were not edited.

## Lessons

Gate words = the generator's `wordCount` (rendered HTML text with `<math>` stripped).

| Slug | Title (unchanged) | Plan grade band | Old gate words | New gate words | Examples / misconceptions / practice | Before | After |
|---|---|---|---|---|---|---|---|
| `app-041-forces-motion-foundations` | APP-04.1 — Forces & Motion — Foundations | K-2 | 356 | 1634 | 3 / 5 / 7 | noindex (scaffold) | indexable |
| `app-042-energy-forms-transfers` | APP-04.2 — Energy — Forms & Transfers | 3-5 | 356 | 1869 | 4 / 5 / 7 | noindex (scaffold) | indexable |
| `app-043-waves-light-sound` | APP-04.3 — Waves — Light & Sound | 4-6 | 356 | 2013 | 4 / 6 / 8 | noindex (scaffold) | indexable |
| `app-044-matter-properties-states` | APP-04.4 — Matter — Properties & States | 4-6 | 356 | 1845 | 3 / 6 / 7 | noindex (scaffold) | indexable |
| `app-045-forces-motion-newtons-laws` | APP-04.5 — Forces & Motion — Newtons Laws | 7-8 | 358 | 1866 | 4 / 6 / 8 | noindex (scaffold) | indexable |
| `app-046-atoms-elements-the-periodic-table` | APP-04.6 — Atoms, Elements & the Periodic Table | 7-8 | 358 | 1770 | 4 / 6 / 7 | noindex (scaffold) | indexable |
| `app-047-chemical-reactions` | APP-04.7 — Chemical Reactions | 8 | 352 | 2120 | 4 / 6 / 7 | noindex (scaffold) | indexable |
| `app-048-electricity-magnetism` | APP-04.8 — Electricity & Magnetism | 7-8 | 352 | 2022 | 4 / 6 / 8 | noindex (scaffold) | indexable |

Preserved for every lesson: slug, title, `subject: "Physical Science K-8"`, `catalog: k12`, `audience_tier: 9-12`, `chapter` (4.1–4.8), `type: chapter`, `open_source`, prev/next chain (`app-041` → … → `app-048`). Only the frontmatter `objectives` list changed (same schema; 4 objectives each; verified with `services/corpus-ingestion/src/frontmatter.ts`).

**Title note (not changed):** the existing 4.5 title is `Newtons Laws` without an apostrophe. A first draft used `Newton's Laws`; the QA metadata diff caught it and the title, H1, and every link label were restored to the existing `Newtons Laws`. Correcting the apostrophe would be a separate title change (it would alter the page `<title>` and the hub listing; the slug would not change).

**Metadata note (not changed):** as with Early Numeracy, `audience_tier` is `9-12` on all 8 lessons although the plan places them in K-8. It was preserved as instructed.

**Audience design:** grade bands come from the chapter outline in `app-04-physical-science-k-8-subject-plan.md` and are stated in each lesson. 4.1–4.4 (K-2 to 4-6) use short learner-facing sentences plus `> **Adult note:**` boxes with materials; 4.5–4.8 (grades 7-8) address the student directly and use equations with units. Every lesson has prerequisites with links, 4 observable objectives, a core explanation with vocabulary and boundaries, worked examples with intermediate steps and a check, topic-specific misconceptions, practice with a collapsible answer key and self-check, a `> **Safety note:**` box, a "Where this fits" section with hub/prev/next/related links, and sources. Plan items that would require claims I could not verify were not asserted: no NGSS performance-expectation codes (nextgenscience.org returned HTTP 403), and the plan's "the 10 most important elements" became a table explicitly labeled "a convenience list for the lessons that follow, not an official ranking."

**Activities and results:** activities are labeled "Activity to try," "Illustrative example," "Illustrative procedure," or "Prediction, not a recorded result." No lesson states that an experiment was performed or reports measured outcomes. The baking soda/vinegar open-vs-sealed container example is framed as what conservation of mass predicts. Hazardous reactions in the 4.7 type table (HgO, HCl, AgNO₃, Pb(NO₃)₂) are labeled "for reading only." Safety notes cover: rolling objects and small magnets (4.1); drop heights and hot appliances (4.2); never looking at the Sun, lasers, volume, and going indoors at thunder (4.3, NWS and NASA sources); adult handling of hot water and not handling dry ice (4.4); safe falling-ball tests (4.5); not handling reactive elements (4.6); goggles, small amounts, no capped bottles, never mixing household cleaners (4.7); low-voltage cells only, no outlets, no short circuits, and button-battery ingestion with the Poison Control source (4.8).

Cross-subject links (all existing indexable routes, each read to confirm scope): `app-023-multiplication-division`, `app-026-decimals-place-value`, `app-027-measurement-data` (Early Numeracy); `131-ratios-rates-proportions`, `132-the-number-system`, `135-equations-inequalities` (Pre-Algebra); `121-statics-equilibrium` (free-body diagrams; Newton's first law postulate); `41-newtonian-dynamics-conservation-laws`; `031-atomic-structure-the-periodic-table`; `033-stoichiometry-reactions` (mole, balancing); `301-electrical-fundamentals-charge-current-voltage-ohm-kirchhoff`. A draft link from 4.7 to 13.2 for "least common multiples" was replaced with 2.3 after 13.2 was found not to cover LCM. Other files that mention these lessons (`10-learning-app-material-readme.md`, `readme-04-physical-science-k-8.md`, `subject-gap-manifest.md`) are non-lesson documents excluded by the generator and were not edited.

## Corpus delta

| Metric | Before | After |
|---|---|---|
| Indexable lessons | 475 | 483 |
| Gated lessons | 165 (placeholder 40, scaffold 125) | 157 (placeholder 40, scaffold 117) |
| Indexable subject hubs | 60 of 81 | 61 of 81 (`physical-science-k-8` promoted, 8/8 lessons) |
| Sitemap URLs (prerendered) | 538 | 547 (+8 lessons, +1 hub) |

Manifest diff (pre-edit regeneration vs. this batch): only the 8 Physical Science lesson entries and the `physical-science-k-8` subject entry changed; 640 lessons before and after. Local links routed to hubs dropped 596 → 572 because the scaffold's `Subject_Plan`/`README`/`LEARNING_PATH` links (3 × 8) were removed.

## Evidence sources

All 70 unique external URLs rendered in the 8 lessons were fetched on 2026-10-18 and returned HTTP 200 with the matching page title. Material claims were checked against fetched page text:

- **Forces and motion:** inertia definition and friction (OpenStax *Physics* 4.2); $F_{\text{net}} = ma$, 1 N = 1 kg·m/s² (4.3); third law "equal in magnitude but opposite in direction," swimmer-and-wall example, normal force, tension (4.4); free-body diagrams, net force, contact vs. field forces (4.1); speed as a scalar rate (2.2); acceleration in m/s² (3.1); horizontal and vertical projectile motions independent when air resistance is ignored (5.3); static/kinetic friction opposes relative motion (5.4); $F = mg$ with $g = 9.8$ m/s² (7.2).
- **Energy:** potential vs. kinetic and the forms of each; "energy is neither created nor destroyed"; efficiency (EIA *Energy Explained*); $W = fd$ in joules (OpenStax 9.1); $KE = \tfrac12 mv^2$, $PE = mgh$ (9.2); six simple machines, IMA = effort arm / resistance arm, a wedge is two inclined planes (9.3); energy flows from hotter to colder (11.2).
- **Waves:** "waves transfer energy … but they do not necessarily transfer any mass," medium, transverse/longitudinal, compression waves (13.1); $v_w = f\lambda$ (13.2); speed-of-sound table — air at 0 °C 331 m/s, fresh water 1,480 m/s (14.1); amplitude–loudness and the ear (14.2); EM waves travel across empty space (15.1); law of reflection (16.1); refraction as bending at a boundary (16.2); $c$ = 299,792,458 m/s exact (NIST CODATA); spectrum order and visible range ~380–700 nm (NASA); thunder ~5 s per mile and "within striking distance" (NWS); not looking directly at the Sun (NASA eclipse safety).
- **Matter:** states; plasma in stars and lightning; elements, compounds, homogeneous/heterogeneous mixtures (OpenStax *Chemistry 2e* 1.2); physical vs. chemical properties and changes (1.3); density = mass/volume and Table 1.4 densities ice 0.92, water 1.0, iron 7.9, copper 9.0 g/cm³ (1.4); dry ice sublimation and frost as deposition (10.3); water ≈ 1 g/cm³ (USGS); filtration, evaporation, distillation (CK-12/LibreTexts 2.10); vapor bubbles in boiling (LibreTexts 13.9).
- **Atoms:** particle charges/masses (electron ≈ 0.00055 amu, ~1,800 per proton), nucleus holds most mass, atomic number defines the element, $A - Z$ = neutrons, isotopes, average atomic mass (*Chemistry 2e* 2.3); ordered by atomic number, seven periods and 18 groups, metals/nonmetals/metalloids, Li/Na/K grouping, hydrogen as a unique nonmetal (2.5); valence electrons as outer-shell electrons (6.4); ions by electron gain/loss, group 17 gains one electron (2.6); symbols and atomic numbers (NIST periodic table).
- **Reactions:** atoms neither created nor destroyed (*Chemistry 2e* 2.1); coefficients and the balanced methane equation with its atom table (4.1); NaCl + AgNO₃ → AgCl precipitate, combustion, baking soda + acid releases CO₂ (4.2); four visual clues (LibreTexts 2.18); never change subscripts (11.3); definitions and examples for combination (4Al + 3O₂ → 2Al₂O₃), decomposition (2HgO → 2Hg + O₂), combustion, single replacement, double replacement (yellow PbI₂ precipitate) (11.4–11.9).
- **Electricity and magnetism:** two kinds of charge, like repel, glass/silk, conservation of charge, conductors/insulators, polarization (OpenStax *Physics* 18.1); $V = IR$, ohmic/nonohmic, resistance rises at high temperature (19.1); series: same current, resistances add, voltages add (19.2); parallel: same voltage, equivalent resistance below the smallest (19.3); like poles repel, field lines, Earth's magnetic south pole near the geographic North Pole, iron/cobalt/nickel ferromagnetic, Oersted, solenoid field ∝ loops × current (20.1); motors convert electrical energy to mechanical (20.2); Faraday and Henry, 1831 (20.3); button batteries (National Capital Poison Center).

Not verified and therefore not claimed: NGSS pages (HTTP 403); NASA Glenn Newton's-laws pages (`newton2g`/`newton3g` 404, others empty); CK-12 FlexBook (JavaScript-only). Removed during review because no fetched source supported them: a year for Oersted's discovery, "an iron core strengthens an electromagnet," "group 1 metals react strongly with water / potassium more vigorously than lithium," "a white AgCl precipitate," and "baking soda and vinegar get colder." Not asserted for the same reason: that household wiring is parallel.

Common instructional knowledge used without a separate citation: magnets do not attract aluminum, copper, or gold; a screw is an inclined plane wrapped around a post; one newton is roughly the weight of a small apple (1 N ÷ 9.8 m/s² ≈ 0.102 kg); the shell filling 2, 8, 8 for Z ≤ 20, labeled in the lesson as a simplified model.

## Calculation checks

Every worked-example and answer-key value was re-evaluated with Python 3 (`fractions.Fraction` for exact ratios, a small formula parser for atom counts) in a throwaway script (deleted after use): speed comparisons (4.1); lever and ramp IMA, ideal forces, hand distances, and work equality (4.2); thunder distance in miles and meters, $\lambda = v/f$ cases, reflection angles, light-to-sound speed ratio (~9.06 × 10⁵, "nearly a million") (4.3); all volumes, displacement volumes, and densities (4.4); net forces, accelerations, weights, masses, and the 12 N → 20 N proportion (4.5); shell arrangements for Na, Cl, Mg; neutron counts; valence counts; the 10-element atomic-number table; atom counts for H₂O, CO₂, Ca(OH)₂, NH₃, C₆H₁₂O₆, Al₂(SO₄)₃ (4.6); atom balance of all 17 chemical equations in the lesson and answer key, and the Mg/O₂/MgO mass bookkeeping with rounded atomic masses (4.7); Ohm's-law, series, and parallel values including the 5 Ω equivalent and the 4× current ratio (4.8). 105 checks, 0 failures.

## Affiliate review

No affiliate links, resource cards, or commercial references were added. `AffiliateOffer`/`AffiliateDisclosure` and resource pages are untouched. External links are to government, university, and nonprofit educational sources only (OpenStax, NIST, NASA, NWS, EIA, USGS, LibreTexts/CK-12, PhET, National Capital Poison Center). The resource table in the subject plan (Khan Academy, Mystery Science, Crash Course, etc.) was not copied into the lessons.

## Validation

| Check | Result |
|---|---|
| `node scripts/generate-content.mjs` (content-site) | pass; 483 indexable / 157 noindex; internal-link assertion pass |
| `node scripts/generate-content.mjs` (learning-app) | pass (640 lessons, 81 subjects) |
| Ingestion frontmatter parser (`parseLessonMarkdown`, via `node --experimental-strip-types`) on all 8 files vs. `94380ac` | pass; every non-objective field identical; 4 objectives each |
| Manifest metadata diff vs. pre-edit regeneration | title, subject, subjectSlug, catalog, audienceTier, chapter, prev/next, openSource identical for all 8 (after the 4.5 title restore) |
| Scaffold/TODO residue scan (manifest HTML + prerendered HTML) | 0 hits for `System Overlay`, `foundational building block`, `Ready for expansion`, `TODO`, `Visual Anchor`, `Subject_Plan`, `LEARNING_PATH`; no `katex-error`; no stray unrendered `$` |
| Internal links | 62 lesson-body links in the manifest (0 unresolved); 139 links (23 unique routes) in the rendered 8 pages + hub, 0 unresolved against the 731 prerendered routes |
| External source links | 70 unique, all HTTP 200 |
| Rendered robots meta | 8 batch pages + `/subject/physical-science-k-8`: no robots meta (indexable), canonical set; negative control `/app-051-foundations-of-american-democracy`: `noindex, follow`, absent from sitemap |
| Rendered hub | links all 8 lessons, no "In development" section |
| Prerendered `sitemap.xml` | 547 URLs; all 8 lessons + hub present |
| `pnpm test` (content-site) | 47/47 pass (4 new Physical Science batch tests, including Safety note, Sources, and prev/next link assertions) |
| `pnpm check` (content-site, learning-app) | pass |
| `pnpm build` (content-site) | pass |
| `pnpm lint` (content-site) | 4 errors, 5 warnings, identical to the pre-existing set recorded in earlier batches (`page.tsx`, `tools/calculus`, `tools/matrix`, `tools/probability`, `AffiliateOffer.tsx`, `generate-content.mjs`); `eslint` on the modified test file is clean |
| `pnpm test` (corpus-ingestion) | not run: same pre-existing `TS2307 Cannot find module '@learning-platform/corpus-types'` build blocker recorded in algebra-ii-01; unrelated to this batch |

## Production observation (previous batch)

On 2026-10-18, before this batch was pushed, `https://learning.nepa-ai.com/sitemap.xml` served 538 URLs including `/subject/early-numeracy-k-5`, and `/app-021-number-sense-counting` rendered without a robots `noindex` and without scaffold text. Early Numeracy batch `94380ac` has therefore propagated. `/app-041-forces-motion-foundations` was still `noindex, follow` with scaffold text and `/subject/physical-science-k-8` was absent from the sitemap, as expected before this batch deploys.

## Not in this batch

- `audience_tier: 9-12` and the 4.5 `Newtons Laws` title were preserved, not corrected (see notes above).
- Obsidian mirror copies under `corpus/10 - Learning App Material/Subjects/` were not edited; the generators and ingestion read `corpus/lessons/` only.
- The external backlog CSV/MD (outside this repository) was not modified; it should be regenerated to show these 8 rows (and the 48 earlier rows) as `ok`.
- Search Console indexing requests have not been made.
