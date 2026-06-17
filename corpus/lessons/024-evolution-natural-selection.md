---
title: "02.4 — Evolution & Natural Selection"
subject: "Biology"
catalog: advanced
audience_tier: higher-education
chapter: "2.4"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 02.4 — Evolution & Natural Selection

> *"There is grandeur in this view of life, with its several powers, having been originally breathed into a few forms or into one; and that, whilst this planet has gone cycling on according to the fixed law of gravity, from so simple a beginning endless forms most beautiful and most wonderful have been, and are being, evolved."*
> — **Charles Darwin**, *On the Origin of Species* (1859)

Evolution is the unifying theory of biology — the framework that connects molecular genetics to ecology, anatomy to behavior, and deep time to present diversity. This chapter covers both classical Darwinian evolution and modern molecular evolution, including population genetics (Hardy-Weinberg), the neutral theory, and quantitative measures of selection at the DNA level. For the AI-minded: evolution is the original optimization algorithm — natural selection is gradient descent on a fitness landscape, and genetic drift is stochastic noise in the update rule.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. State the four conditions for evolution by natural selection.
2. Derive Hardy-Weinberg equilibrium from first principles and list its assumptions.
3. Calculate allele frequency changes under selection, mutation, migration, and drift.
4. Distinguish directional, stabilizing, and disruptive selection with fitness curves.
5. Explain Kimura's neutral theory and its predictions for molecular evolution.
6. Calculate dN/dS ratios and interpret them as evidence for selection type.
7. Apply the molecular clock to estimate divergence times.
8. Connect evolutionary mechanisms to genetic algorithms and evolutionary strategies in AI.

---

## 🖼️ Visual Anchor — Hardy-Weinberg Equilibrium

![bio__15.4-fig1](bio__15.4-fig1.svg)

---

## 📚 1. Definitions

### Definition 02.4.1 — Evolution

**Evolution** is the change in allele frequencies in a population over generations. Mechanisms:

| Mechanism | Effect on Variation | Directional? |
|:---|:---|:---|
| Natural selection | Reduces (removes unfit) | Yes (toward higher fitness) |
| Genetic drift | Reduces (random loss) | No (stochastic) |
| Mutation | Increases (new alleles) | No (random) |
| Gene flow (migration) | Homogenizes populations | No (equalizing) |
| Sexual selection | Can increase or decrease | Yes (toward preferred traits) |

### Definition 02.4.2 — Natural Selection (Four Conditions)

Natural selection occurs when:
1. **Variation** exists in the population (phenotypic differences)
2. **Heritability**: Variation is at least partly genetic
3. **Differential fitness**: Some variants survive/reproduce better
4. **Overproduction**: More offspring produced than can survive

Result: Alleles associated with higher fitness increase in frequency.

### Definition 02.4.3 — Fitness ($w$)

**Fitness** is the relative reproductive success of a genotype:

$$
w_i = \frac{\text{reproductive output of genotype } i}{\text{reproductive output of best genotype}}
$$

- $w = 1$: Maximum fitness (reference genotype)
- $w = 0$: Lethal (no reproduction)
- **Selection coefficient**: $s = 1 - w$ (measures disadvantage)

### Definition 02.4.4 — Hardy-Weinberg Equilibrium

In an idealized population (no evolution), genotype frequencies are predictable from allele frequencies:

For two alleles (A with frequency $p$, a with frequency $q = 1-p$):

$$
\text{Genotype frequencies: } p^2 (\text{AA}) + 2pq (\text{Aa}) + q^2 (\text{aa}) = 1
$$

**Assumptions** (violations = evolution):
1. No selection (all genotypes equally fit)
2. No mutation
3. No migration (closed population)
4. Infinite population size (no drift)
5. Random mating (no assortative mating)

### Definition 02.4.5 — Genetic Drift

**Genetic drift** is random change in allele frequencies due to finite population size. Key properties:
- Magnitude inversely proportional to population size: $\text{Var}(\Delta p) = \frac{pq}{2N_e}$
- Eventually fixes or loses alleles (reduces diversity)
- Dominates over selection when $|s| < 1/(2N_e)$ (effectively neutral)
- **Effective population size** ($N_e$): The size of an ideal population with the same drift rate

### Definition 02.4.6 — Neutral Theory (Kimura, 1968)

The **neutral theory of molecular evolution** proposes that most evolutionary change at the molecular level is due to random drift of selectively neutral (or nearly neutral) mutations, not positive selection.

Key predictions:
- Rate of neutral substitution = mutation rate ($k = \mu$), independent of population size
- Molecular clock: Substitutions accumulate linearly with time
- Polymorphism within species ∝ $4N_e\mu$ (for diploids)

### Definition 02.4.7 — dN/dS Ratio (ω)

The ratio of nonsynonymous to synonymous substitution rates:

$$
\omega = \frac{d_N}{d_S} = \frac{\text{rate of amino acid-changing substitutions}}{\text{rate of silent substitutions}}
$$

Interpretation:
- $\omega < 1$: **Purifying selection** (amino acid changes are deleterious → removed)
- $\omega = 1$: **Neutral evolution** (no selection on protein sequence)
- $\omega > 1$: **Positive selection** (amino acid changes are advantageous → fixed faster than neutral)

Most genes: $\omega \approx 0.1$–0.3 (strong purifying selection). Genes under positive selection (e.g., immune genes, reproductive proteins): $\omega > 1$ at specific sites.



---

## 🔬 2. Biological Mechanisms

### 2.1 — Modes of Natural Selection

**Directional selection:** One extreme phenotype favored → mean shifts.
- Example: Antibiotic resistance (resistant allele frequency increases under drug pressure)
- Industrial melanism in peppered moths (dark morphs favored on soot-covered trees)

**Stabilizing selection:** Intermediate phenotype favored → variance decreases.
- Example: Human birth weight (~3.5 kg optimal; too small = premature complications, too large = delivery complications)
- Most quantitative traits under stabilizing selection most of the time

**Disruptive selection:** Both extremes favored over intermediate → variance increases → potential speciation.
- Example: African seedcracker finches (large bills for hard seeds, small bills for soft seeds; intermediate bills inefficient for both)

**Balancing selection:** Multiple alleles maintained in population:
- **Heterozygote advantage** (overdominance): Sickle-cell trait (HbAS) — heterozygotes resistant to malaria AND avoid sickle-cell disease
- **Frequency-dependent selection**: Rare morphs have advantage (e.g., predator search image)
- **Spatially varying selection**: Different alleles favored in different environments

### 2.2 — Speciation Mechanisms

**Allopatric speciation** (geographic isolation):

$$
\text{Population} \xrightarrow{\text{barrier}} \text{Pop A} + \text{Pop B} \xrightarrow{\text{drift + selection}} \text{Species A} + \text{Species B}
$$

**Sympatric speciation** (same geographic area):
- Polyploidy (instant speciation in plants — autopolyploidy or allopolyploidy)
- Ecological specialization + assortative mating
- Example: Apple maggot fly (Rhagoletis) — host race formation on apple vs hawthorn

**Reproductive isolation mechanisms:**
- Pre-zygotic: Temporal, behavioral, mechanical, gametic isolation
- Post-zygotic: Hybrid inviability, hybrid sterility, hybrid breakdown

### 2.3 — Molecular Evolution

**The molecular clock hypothesis:**
- Neutral substitutions accumulate at a constant rate per generation
- Rate calibrated by fossil record → estimate divergence times

$$
t = \frac{d}{2r}
$$

where $t$ = divergence time, $d$ = genetic distance (substitutions per site), $r$ = substitution rate per site per year, factor of 2 because both lineages accumulate changes.

**Synonymous vs nonsynonymous substitutions:**
- Synonymous (dS): Mostly neutral → accumulate at mutation rate → molecular clock
- Nonsynonymous (dN): Subject to selection → rate depends on selective constraint

### 2.4 — Phylogenetics

**Phylogenetic tree construction methods:**
1. **Distance-based** (UPGMA, Neighbor-Joining): Use pairwise genetic distances
2. **Maximum parsimony**: Find tree requiring fewest evolutionary changes
3. **Maximum likelihood**: Find tree that maximizes probability of observed data given evolutionary model
4. **Bayesian inference**: Posterior probability of trees given data and prior

**Homology types:**
- **Orthologs**: Same gene in different species (diverged by speciation) — usually same function
- **Paralogs**: Duplicated genes within a species (diverged by duplication) — often different function
- **Xenologs**: Genes acquired by horizontal transfer

---

## 📐 3. Mathematical Models

### 3.1 — Hardy-Weinberg Derivation

**Setup:** Diploid population, one locus, two alleles (A, a) with frequencies $p$ and $q = 1-p$.

**Derivation from random mating:**

Under random mating, gamete union is random. Probability of each genotype in offspring:

$$
P(\text{AA}) = P(\text{A from mom}) \times P(\text{A from dad}) = p \times p = p^2
$$

$$
P(\text{Aa}) = P(\text{A from mom}) \times P(\text{a from dad}) + P(\text{a from mom}) \times P(\text{A from dad}) = pq + qp = 2pq
$$

$$
P(\text{aa}) = q \times q = q^2
$$

**Verify:** $p^2 + 2pq + q^2 = (p + q)^2 = 1^2 = 1$ ✓

**Key result:** Allele frequencies don't change across generations under HW assumptions:

$$
p' = \text{freq(A) in next gen} = p^2 + \frac{1}{2}(2pq) = p^2 + pq = p(p + q) = p
$$

Equilibrium is reached in **one generation** of random mating (for autosomal loci).

### 3.2 — Selection Model (One Locus, Two Alleles)

Genotype fitnesses: $w_{AA} = 1$, $w_{Aa} = 1 - hs$, $w_{aa} = 1 - s$

where $h$ = dominance coefficient (h=0: A fully dominant; h=1: a fully dominant; h=0.5: additive).

**Mean fitness:**

$$
\bar{w} = p^2 w_{AA} + 2pq \cdot w_{Aa} + q^2 w_{aa}
$$

**Allele frequency change per generation:**

$$
\Delta p = \frac{pq[p \cdot (w_{AA} - w_{Aa}) + q \cdot (w_{Aa} - w_{aa})]}{2\bar{w}}
$$

For additive selection ($h = 0.5$, so $w_{Aa} = 1 - s/2$):

$$
\Delta p = \frac{spq(p - q + 1)}{2\bar{w}} \approx \frac{spq}{2} \quad \text{(when } s \text{ is small)}
$$

**Time to fixation** (approximate, for advantageous allele starting at frequency $p_0$):

$$
t \approx \frac{2}{s} \ln\left(\frac{1}{p_0}\right) + \frac{2}{s} \ln\left(\frac{1}{s}\right)
$$

### 3.3 — Genetic Drift (Wright-Fisher Model)

In a population of $N$ diploid individuals ($2N$ gene copies):

$$
P(k \text{ copies of A next gen} | \text{current freq } p) = \binom{2N}{k} p^k (1-p)^{2N-k}
$$

**Variance in allele frequency per generation:**

$$
\text{Var}(\Delta p) = \frac{p(1-p)}{2N_e}
$$

**Probability of fixation** of a new neutral mutation:

$$
P_{\text{fix}} = \frac{1}{2N}
$$

**Probability of fixation** of a beneficial mutation (Haldane, 1927):

$$
P_{\text{fix}} \approx 2s \quad \text{(for } s \ll 1 \text{, diploid)}
$$

**Rate of neutral substitution:**
- New mutations per generation: $2N\mu$
- Probability each fixes: $1/(2N)$
- Rate of substitution: $k = 2N\mu \times \frac{1}{2N} = \mu$

This elegant result means the neutral substitution rate equals the mutation rate, independent of population size.

### 3.4 — Coalescent Theory

Looking backward in time, lineages **coalesce** (share a common ancestor). For $n$ lineages in a population of $N_e$:

$$
P(\text{coalescence of any pair in one generation}) = \frac{\binom{n}{2}}{2N_e} = \frac{n(n-1)}{4N_e}
$$

**Expected time to coalescence** of $n$ lineages to $n-1$:

$$
E[T_n] = \frac{4N_e}{n(n-1)}
$$

**Total expected time** to most recent common ancestor (MRCA) for $n$ samples:

$$
E[T_{\text{MRCA}}] = \sum_{k=2}^{n} \frac{4N_e}{k(k-1)} = 4N_e\left(1 - \frac{1}{n}\right)
$$

For $n \rightarrow \infty$: $E[T_{\text{MRCA}}] \rightarrow 4N_e$ generations.

### 3.5 — dN/dS Calculation

Given aligned coding sequences from two species:

$$
d_N = -\frac{3}{4}\ln\left(1 - \frac{4}{3} \cdot p_N\right) \quad \text{(Jukes-Cantor correction)}
$$

$$
d_S = -\frac{3}{4}\ln\left(1 - \frac{4}{3} \cdot p_S\right)
$$

where $p_N$ = proportion of nonsynonymous differences, $p_S$ = proportion of synonymous differences.

The Jukes-Cantor correction accounts for multiple substitutions at the same site (back-mutations, parallel mutations).

---

## ✍️ 4. Worked Examples

<details>
<summary>🔍 Worked Example 02.4.1 — Hardy-Weinberg: Carrier Frequency</summary>

**Problem:** Cystic fibrosis (autosomal recessive) affects 1 in 2,500 Caucasians. Calculate the carrier frequency.

**Step 1:** Disease frequency = $q^2 = 1/2500 = 0.0004$

**Step 2:** Allele frequency: $q = \sqrt{0.0004} = 0.02$

**Step 3:** $p = 1 - q = 0.98$

**Step 4:** Carrier frequency: $2pq = 2(0.98)(0.02) = 0.0392 \approx 1 \text{ in } 25$

**Interpretation:** About 4% of Caucasians are CF carriers — far more common than the disease itself. This is why genetic counseling matters for recessive conditions.

</details>

<details>
<summary>🔍 Worked Example 02.4.2 — Selection: Allele Frequency Change</summary>

**Problem:** A recessive lethal allele (aa is lethal, $s = 1$, $h = 0$) has current frequency $q = 0.1$. Calculate $q$ after one generation of selection.

**Step 1:** Fitnesses: $w_{AA} = 1$, $w_{Aa} = 1$ (h=0, so heterozygote unaffected), $w_{aa} = 0$.

**Step 2:** After selection, genotype frequencies (before normalization):
- AA: $p^2 \times 1 = (0.9)^2 = 0.81$
- Aa: $2pq \times 1 = 2(0.9)(0.1) = 0.18$
- aa: $q^2 \times 0 = 0$ (all die)

**Step 3:** Mean fitness: $\bar{w} = 0.81 + 0.18 + 0 = 0.99$

**Step 4:** New allele frequency:

$$
q' = \frac{q^2 \times 0 + \frac{1}{2}(2pq \times 1)}{\bar{w}} = \frac{0 + 0.09}{0.99} = 0.0909
$$

**Step 5:** General formula for recessive lethal:

$$
q' = \frac{q}{1 + q}
$$

Verify: $q' = 0.1/(1 + 0.1) = 0.1/1.1 = 0.0909$ ✓

**Step 6:** After $t$ generations: $q_t = \frac{q_0}{1 + tq_0}$

Time to halve frequency: $q_t = q_0/2$ → $t = 1/q_0 = 10$ generations.

Note: Selection against recessives becomes very slow at low frequencies (most copies hidden in heterozygotes).

</details>

<details>
<summary>🔍 Worked Example 02.4.3 — Heterozygote Advantage (Sickle Cell)</summary>

**Problem:** In a malaria-endemic region, fitnesses are: $w_{AA} = 0.88$ (malaria susceptible), $w_{AS} = 1.0$ (resistant, no disease), $w_{SS} = 0.14$ (sickle-cell disease). Find the equilibrium frequency of the S allele.

**Step 1:** At equilibrium with heterozygote advantage, $\Delta p = 0$ when:

$$
\hat{q} = \frac{s_1}{s_1 + s_2}
$$

where $s_1 = 1 - w_{AA} = 0.12$ and $s_2 = 1 - w_{SS} = 0.86$.

**Step 2:**

$$
\hat{q} = \frac{0.12}{0.12 + 0.86} = \frac{0.12}{0.98} = 0.122
$$

**Step 3:** Predicted equilibrium: ~12% S allele frequency. Observed in West Africa: ~10–20%. ✓

**Step 4:** Disease frequency at equilibrium: $q^2 = (0.122)^2 = 0.015$ (1.5% have sickle-cell disease — the "cost" of malaria protection).

</details>

<details>
<summary>🔍 Worked Example 02.4.4 — Molecular Clock Divergence Time</summary>

**Problem:** Cytochrome c differs by 13 amino acids between humans and dogs. The substitution rate for cytochrome c is ~$2.2 \times 10^{-9}$ substitutions/site/year. Cytochrome c has 104 residues. Estimate divergence time.

**Step 1:** Genetic distance (substitutions per site):

$$
d = \frac{13}{104} = 0.125 \text{ substitutions/site}
$$

**Step 2:** Apply Poisson correction (for multiple hits):

$$
d_{\text{corrected}} = -\ln(1 - d) = -\ln(0.875) = 0.134
$$

**Step 3:** Divergence time (both lineages accumulate changes):

$$
t = \frac{d_{\text{corrected}}}{2r} = \frac{0.134}{2 \times 2.2 \times 10^{-9}} = \frac{0.134}{4.4 \times 10^{-9}} = 30.4 \text{ million years}
$$

**Step 4:** Fossil record estimate for human-dog divergence: ~85–100 Mya. The discrepancy suggests cytochrome c evolves slower in some lineages (generation time effect) or the rate calibration needs adjustment. More sophisticated models (relaxed molecular clock) account for rate variation.

</details>

<details>
<summary>🔍 Worked Example 02.4.5 — dN/dS Interpretation</summary>

**Problem:** Comparing human and mouse orthologs:
- Gene A: dN = 0.02, dS = 0.45 → ω = 0.044
- Gene B: dN = 0.35, dS = 0.40 → ω = 0.875
- Gene C: dN = 0.85, dS = 0.42 → ω = 2.02

Interpret each.

**Gene A (ω = 0.044):** Strong purifying selection. Only 4.4% of amino acid changes are tolerated compared to neutral expectation. This gene is highly constrained — likely essential with little tolerance for change (e.g., histone H4, ribosomal proteins).

**Gene B (ω = 0.875):** Near-neutral evolution. Most amino acid changes are tolerated. Could be a gene with relaxed constraint (pseudogene-like) or one where many sites are neutral but a few are constrained (averaging effect).

**Gene C (ω = 2.02):** Positive selection. Amino acid changes are fixed faster than neutral expectation — adaptive evolution is driving protein divergence. Typical of immune genes (MHC, defensins), reproductive proteins (zona pellucida), or genes in evolutionary arms races (host-pathogen interactions).

**Caveat:** Whole-gene ω averages over all sites. Site-specific models (e.g., PAML) can identify individual codons under positive selection even when whole-gene ω < 1.

</details>



---

## 🧠 5. Connections to AI / Computing

### 5.1 — Genetic Algorithms: Evolution as Optimization

| Evolutionary Concept | GA Implementation |
|:---|:---|
| Population of organisms | Population of candidate solutions |
| Genome (DNA sequence) | Parameter vector / bitstring |
| Fitness (survival + reproduction) | Objective function value |
| Natural selection | Selection operator (tournament, roulette) |
| Crossover (meiotic recombination) | Crossover operator (single-point, uniform, BLX-α) |
| Mutation (point, insertion, deletion) | Mutation operator (Gaussian noise, bit flip) |
| Genetic drift (finite population) | Stochastic selection noise |
| Speciation (reproductive isolation) | Niching / fitness sharing |
| Epistasis (gene interactions) | Non-separable fitness landscape |

**GA pseudocode mapping to biology:**
```
initialize_population()          # Abiogenesis
while not converged:
    evaluate_fitness(population)  # Natural selection pressure
    parents = select(population)  # Differential reproduction
    offspring = crossover(parents) # Meiosis + fertilization
    offspring = mutate(offspring)  # DNA replication errors
    population = replace(population, offspring)  # Generational turnover
```

### 5.2 — Evolutionary Strategies (ES) and CMA-ES

**CMA-ES** (Covariance Matrix Adaptation Evolution Strategy) is the state-of-the-art for continuous optimization:
- Maintains a multivariate Gaussian distribution over solutions
- Adapts the covariance matrix (= learning correlations between parameters = learning linkage)
- The covariance matrix is the ES analog of **linkage disequilibrium** in population genetics

**OpenAI's use of ES:** Evolution Strategies as a Scalable Alternative to Reinforcement Learning (Salimans et al., 2017) — used ES to train Atari agents, competitive with policy gradient methods.

### 5.3 — Fitness Landscapes → Loss Landscapes

| Evolution | Deep Learning |
|:---|:---|
| Fitness landscape | Negative loss landscape |
| Adaptive peak | Local minimum of loss |
| Valley crossing (drift through low fitness) | Escaping local minima (learning rate, noise) |
| Neutral networks (connected neutral genotypes) | Flat regions in loss landscape |
| Epistasis (rugged landscape) | Non-convex loss surface |
| Red Queen dynamics (co-evolution) | Adversarial training (GANs) |

### 5.4 — Neutral Theory → Lottery Ticket Hypothesis

Kimura's insight that most molecular changes are neutral has a deep parallel:
- **Neutral theory**: Most mutations don't affect fitness → fixed by drift
- **Lottery ticket hypothesis** (Frankle & Carlin, 2019): Most weights in a neural network don't matter → can be pruned without affecting performance

Both suggest that the "functional" fraction of the system is much smaller than the total — most of the genome/network is either neutral or redundant.

### 5.5 — Coevolution → GANs and Multi-Agent RL

Biological coevolution (predator-prey arms races, host-parasite dynamics) maps directly to:
- **GANs**: Generator and discriminator coevolve — each improves in response to the other
- **Multi-agent RL**: Agents in competitive environments drive each other's improvement
- **Red Queen effect**: You must keep evolving just to maintain relative fitness (no stable optimum)

---

## 🏃 6. Personal Health Connections

### 6.1 — Evolution of Athletic Traits

Human athletic diversity reflects evolutionary history:
- **Sprint/power traits** (ACTN3 R allele, fast-twitch fibers): Ancestral state, selected for hunting/escape
- **Endurance traits** (ACTN3 X allele, slow-twitch): Derived state, possibly selected for persistence hunting in early Homo
- **Altitude adaptation** (EPAS1 in Tibetans): Recent positive selection (~3,000 years) for high-altitude performance

**Implications for training:** Your genetic profile reflects evolutionary pressures on your ancestors. Training optimizes within your genetic potential — you can't train away your fiber type ratio, but you can maximize each fiber type's performance.

### 6.2 — Evolutionary Medicine

Understanding evolution improves health decisions:
- **Antibiotic resistance**: Bacterial evolution under selection pressure → use antibiotics judiciously
- **Cancer as evolution**: Tumor cells evolve under selection (immune evasion, drug resistance)
- **Mismatch diseases**: Our genome evolved for ancestral environments → modern diet/lifestyle creates mismatches (obesity, autoimmunity, myopia)
- **Pathogen virulence evolution**: Virulence evolves based on transmission mode (airborne → less virulent; vector-borne → more virulent)

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- [02.2 - Genetics & Inheritance](02.2---Genetics-&-Inheritance) — Mendelian genetics as the mechanism of inheritance
- [02.3 - DNA, RNA & Protein Synthesis](02.3---DNA,-RNA-&-Protein-Synthesis) — Mutations in DNA provide raw material for evolution
- [02.5 - Ecology & Ecosystems](02.5---Ecology-&-Ecosystems) — Ecological context of natural selection
- [02.8 - Modern Biology - Genomics, CRISPR, Synthetic Biology](02.8---Modern-Biology---Genomics,-CRISPR,-Synthetic-Biology) — Directed evolution and synthetic biology
- [05.2 - Action Potentials & Ion Channels](05.2---Action-Potentials-&-Ion-Channels) — Ion channel evolution and channelopathies

### Authoritative Sources
1. **Darwin, C.** (1859). *On the Origin of Species*. Free at darwin-online.org.uk.
2. **Kimura, M.** (1983). *The Neutral Theory of Molecular Evolution*. Cambridge University Press.
3. **Futuyma, D. & Kirkpatrick, M.** — *Evolution*, 4th ed. Comprehensive modern textbook.
4. **MIT 7.014 OCW** — Evolution and ecology lectures.
5. **Khan Academy** — [Evolution](https://www.khanacademy.org/science/biology/her/evolution-and-natural-selection)
6. **HHMI BioInteractive** — Evolution collection (great visualizations).
7. **Nei, M. & Kumar, S.** — *Molecular Evolution and Phylogenetics*. Oxford University Press.



---

## 🔬 8. Extended Worked Examples & Deep Dives

### 8.1 — Full Population Genetics with Selection Coefficients

**The General Selection Model (Diploid, One Locus, Two Alleles):**

Define fitness values relative to the heterozygote:

| Genotype | $AA$ | $Aa$ | $aa$ |
|:---|:---:|:---:|:---:|
| Fitness | $1 - s_1$ | $1$ | $1 - s_2$ |
| Frequency | $p^2$ | $2pq$ | $q^2$ |

where $s_1, s_2 > 0$ means both homozygotes are less fit than the heterozygote (overdominance).

**Mean Population Fitness:**

$$
\bar{w} = p^2(1-s_1) + 2pq(1) + q^2(1-s_2) = 1 - s_1 p^2 - s_2 q^2
$$

**Allele Frequency Dynamics:**

The frequency of allele $A$ after one generation of selection:

$$
p' = \frac{p^2(1-s_1) + pq}{\bar{w}} = \frac{p[p(1-s_1) + q]}{\bar{w}}
$$

Change per generation:

$$
\Delta p = \frac{pq[s_2 q - s_1 p]}{\bar{w}}
$$

**Equilibrium Analysis ($\Delta p = 0$):**

Setting $\Delta p = 0$ (excluding trivial solutions $p = 0$ or $q = 0$):

$$
s_2 q = s_1 p \implies s_2(1-p) = s_1 p \implies \hat{p} = \frac{s_2}{s_1 + s_2}
$$

**Stability Analysis:**

$$
\frac{d(\Delta p)}{dp}\bigg|_{\hat{p}} < 0 \implies \text{stable equilibrium (overdominance)}
$$

$$
\frac{d(\Delta p)}{dp}\bigg|_{\hat{p}} > 0 \implies \text{unstable equilibrium (underdominance)}
$$

For overdominance ($s_1, s_2 > 0$): the internal equilibrium is **stable** — both alleles are maintained.
For underdominance ($s_1, s_2 < 0$): the internal equilibrium is **unstable** — population goes to fixation of whichever allele starts above $\hat{p}$.

**Worked Example: MHC Diversity (Overdominance)**

Major Histocompatibility Complex alleles show extreme polymorphism (>10,000 alleles at HLA-B in humans). Heterozygotes present a wider range of pathogen peptides:

$s_1 = 0.02$ (AA homozygote disadvantage), $s_2 = 0.03$ (aa homozygote disadvantage):

$$
\hat{p} = \frac{0.03}{0.02 + 0.03} = 0.60
$$

Both alleles maintained at 60%/40% — explaining the extraordinary MHC diversity observed across vertebrates.

---

### 8.2 — Founder Effects and Genetic Bottlenecks: Quantitative Analysis

**Founder Effect: Sampling from a Source Population**

When $k$ individuals colonize a new habitat from a population with allele frequency $p$:

$$
E[\hat{p}] = p \quad \text{(unbiased)}
$$

$$
\text{Var}(\hat{p}) = \frac{p(1-p)}{2k} \quad \text{(sampling variance)}
$$

**Example: Afrikaner Population**

The Afrikaner population descended from ~2,000 Dutch settlers (17th century). For a recessive disease allele with $p = 0.01$ in the Netherlands:

$$
\text{SD}(\hat{p}) = \sqrt{\frac{0.01 \times 0.99}{2 \times 2000}} = \sqrt{2.48 \times 10^{-6}} = 0.0016
$$

95% CI for founder frequency: $0.01 \pm 0.003$. But if by chance the founders had $p = 0.02$ (within 2 SD), the disease frequency in descendants would be 4× higher — explaining elevated frequencies of variegate porphyria, familial hypercholesterolemia, and Fanconi anemia in Afrikaners.

**Serial Founder Effects (Out-of-Africa Model):**

Human genetic diversity decreases with distance from Africa due to serial bottlenecks:

$$
H_{\text{expected}} = H_0 \prod_{i=1}^{n} \left(1 - \frac{1}{2N_{e,i}}\right)
$$

Each bottleneck of effective size $N_{e,i}$ reduces heterozygosity by $1/(2N_{e,i})$.

Observed pattern: African populations have ~20% more genetic diversity than non-African populations, consistent with a founding bottleneck of ~1,000–10,000 individuals leaving Africa ~70,000 years ago.

---

### 8.3 — Molecular Clock Calibration

**The Molecular Clock Hypothesis (Zuckerkandl & Pauling, 1965):**

Neutral mutations accumulate at a constant rate per unit time, allowing divergence times to be estimated from sequence differences.

**Derivation:**

For neutral mutations, the substitution rate equals the mutation rate:

$$
k = 2N\mu \times \frac{1}{2N} = \mu
$$

(New mutations arise at rate $2N\mu$ per generation; each has fixation probability $1/(2N)$.)

**Calibration:**

Given a fossil-calibrated divergence time $T_{\text{cal}}$ and observed substitutions $d_{\text{cal}}$:

$$
r = \frac{d_{\text{cal}}}{2 T_{\text{cal}}} \quad \text{(substitutions per site per year)}
$$

The factor of 2 accounts for divergence along both lineages since the common ancestor.

**Worked Example: Human-Chimpanzee Divergence**

Observed synonymous substitution rate: $d_S = 0.012$ substitutions/site
Fossil calibration (human-chimp split): $T = 6$–7 Mya

$$
r_S = \frac{0.012}{2 \times 6.5 \times 10^6} = 9.2 \times 10^{-10} \text{ substitutions/site/year}
$$

Per generation (assuming 25 years/generation):

$$
\mu = r_S \times 25 = 2.3 \times 10^{-8} \text{ per site per generation}
$$

This matches direct measurements from parent-offspring sequencing (~1.2 × 10⁻⁸ per site per generation for all mutations, with synonymous sites accumulating faster due to lack of constraint).

**Rate Variation and the Relaxed Clock:**

The strict molecular clock is violated because:
- Generation time effects (shorter generations → more mutations per year)
- Metabolic rate effects (higher metabolism → more oxidative DNA damage)
- Population size effects (smaller $N_e$ → more slightly deleterious fixations)

Modern methods use **relaxed clock models** that allow rate variation across branches:

$$
r_i \sim \text{LogNormal}(\mu_r, \sigma_r^2) \quad \text{(uncorrelated relaxed clock)}
$$

$$
r_i | r_{\text{parent}} \sim \text{LogNormal}(\ln r_{\text{parent}}, \sigma^2) \quad \text{(autocorrelated clock)}
$$

---

### 8.4 — Phylogenetic Inference: Maximum Likelihood and Bayesian Methods

**Maximum Likelihood Phylogenetics:**

Given aligned sequences $D$ and a tree topology $\tau$ with branch lengths $\mathbf{b}$:

$$
L(\tau, \mathbf{b} | D) = P(D | \tau, \mathbf{b}) = \prod_{\text{sites}} P(D_{\text{site}} | \tau, \mathbf{b})
$$

For each site, the likelihood is computed using Felsenstein's pruning algorithm (dynamic programming on the tree):

$$
L_k(s) = \left[\sum_{x} P(x|s, t_L) \cdot L_L(x)\right] \times \left[\sum_{y} P(y|s, t_R) \cdot L_R(y)\right]
$$

where $L_k(s)$ = partial likelihood at node $k$ in state $s$, and $P(x|s,t)$ is the transition probability from state $s$ to $x$ over branch length $t$.

**Substitution Models:**

The Jukes-Cantor (JC69) model (simplest):

$$
P(j|i, t) = \begin{cases}
\frac{1}{4} + \frac{3}{4}e^{-4\mu t/3} & \text{if } i = j \\
\frac{1}{4} - \frac{1}{4}e^{-4\mu t/3} & \text{if } i \neq j
\end{cases}
$$

JC69 distance correction:

$$
d = -\frac{3}{4} \ln\left(1 - \frac{4}{3}p\right)
$$

where $p$ = observed proportion of differences. This corrects for multiple substitutions at the same site.

**Bayesian Phylogenetics (MrBayes, BEAST):**

$$
P(\tau, \mathbf{b}, \theta | D) = \frac{P(D | \tau, \mathbf{b}, \theta) \cdot P(\tau) \cdot P(\mathbf{b}) \cdot P(\theta)}{P(D)}
$$

Sampled via Markov Chain Monte Carlo (MCMC):
- Propose new tree topologies (NNI, SPR moves)
- Propose new branch lengths
- Accept/reject via Metropolis-Hastings ratio

**Posterior probability of a clade** = fraction of MCMC samples containing that clade.

```python
import numpy as np

def jukes_cantor_distance(seq1, seq2):
    """Calculate JC69-corrected evolutionary distance."""
    assert len(seq1) == len(seq2)
    differences = sum(1 for a, b in zip(seq1, seq2) if a != b)
    p = differences / len(seq1)  # Observed proportion different
    
    if p >= 0.75:
        return float('inf')  # Saturated — cannot estimate
    
    d = -0.75 * np.log(1 - (4/3) * p)
    variance = p * (1 - p) / (len(seq1) * (1 - (4/3)*p)**2)
    
    return d, np.sqrt(variance)

def upgma_tree(distance_matrix, names):
    """Simple UPGMA clustering for phylogenetic tree construction."""
    n = len(names)
    clusters = [[i] for i in range(n)]
    cluster_names = list(names)
    heights = [0.0] * n
    D = distance_matrix.copy()
    
    tree_str = ""
    while len(clusters) > 1:
        # Find minimum distance
        min_d = float('inf')
        for i in range(len(D)):
            for j in range(i+1, len(D)):
                if D[i,j] < min_d:
                    min_d = D[i,j]
                    mi, mj = i, j
        
        # Merge clusters
        new_height = min_d / 2
        new_name = f"({cluster_names[mi]}:{new_height-heights[mi]:.4f},{cluster_names[mj]}:{new_height-heights[mj]:.4f})"
        
        # Update distance matrix (average linkage)
        new_row = np.zeros(len(D) - 1)
        idx = 0
        for k in range(len(D)):
            if k != mi and k != mj:
                ni, nj = len(clusters[mi]), len(clusters[mj])
                new_row[idx] = (D[mi,k]*ni + D[mj,k]*nj) / (ni + nj)
                idx += 1
        
        # Remove merged clusters, add new one
        keep = [k for k in range(len(D)) if k != mi and k != mj]
        D_new = D[np.ix_(keep, keep)]
        D = np.zeros((len(D_new)+1, len(D_new)+1))
        D[:len(D_new), :len(D_new)] = D_new
        D[-1, :len(D_new)] = new_row[:len(D_new)]
        D[:len(D_new), -1] = new_row[:len(D_new)]
        
        new_cluster = clusters[mi] + clusters[mj]
        clusters = [clusters[k] for k in keep] + [new_cluster]
        cluster_names = [cluster_names[k] for k in keep] + [new_name]
        heights = [heights[k] for k in keep] + [new_height]
    
    return cluster_names[0]

# Example: distance matrix for 4 species
D = np.array([
    [0, 0.05, 0.10, 0.15],
    [0.05, 0, 0.08, 0.14],
    [0.10, 0.08, 0, 0.12],
    [0.15, 0.14, 0.12, 0]
])
tree = upgma_tree(D, ['Human', 'Chimp', 'Gorilla', 'Orangutan'])
print(f"UPGMA tree: {tree}")
```

---

### 8.5 — dN/dS Ratios: Detecting Selection at the Molecular Level

The ratio of nonsynonymous ($d_N$) to synonymous ($d_S$) substitution rates reveals the type of selection acting on a protein-coding gene:

$$
\omega = \frac{d_N}{d_S}
$$

| $\omega$ value | Interpretation | Example |
|:---:|:---|:---|
| $\omega \ll 1$ | Purifying selection (constraint) | Histones ($\omega \approx 0.01$) |
| $\omega \approx 1$ | Neutral evolution | Pseudogenes |
| $\omega \gg 1$ | Positive selection (adaptive) | MHC, viral surface proteins |

**Worked Example: Influenza Hemagglutinin**

Antigenic sites on influenza HA show $\omega = 2.5$–5.0 (strong positive selection for immune evasion), while structural core residues show $\omega = 0.05$–0.1 (strong purifying selection for protein stability).

**Site-Specific Models (Yang & Nielsen, 2002):**

Rather than assuming uniform $\omega$ across the gene, fit a mixture of site classes:

$$
P(\omega | \text{data}) = \sum_{k} \pi_k \cdot P(\text{data} | \omega_k)
$$

Model M8 (positive selection): $\omega$ drawn from Beta distribution + discrete class with $\omega > 1$

Likelihood ratio test: $2\Delta\ell = 2[\ell(M8) - \ell(M7)]$ compared to $\chi^2$ distribution.




---

## 🧠 9. Appendix: Theoretical Foundations & AI Bridges

### 9.1 — Genetic Algorithms: Evolution as Optimization

**Cross-link [10.7 - Evolutionary Computation & Genetic Algorithms](10.7---Evolutionary-Computation-&-Genetic-Algorithms)**

Genetic algorithms (GAs) are direct computational implementations of Darwinian evolution. The mapping between biology and computation is precise:

**The Evolutionary Optimization Framework:**

$$
\mathbf{x}^* = \arg\max_{\mathbf{x} \in \mathcal{X}} f(\mathbf{x})
$$

where $f$ is the fitness function and $\mathcal{X}$ is the search space.

**Selection Pressure and Tournament Size:**

Tournament selection with size $k$ creates selection pressure:

$$
P(\text{best individual selected}) = 1 - \left(1 - \frac{1}{N}\right)^k \approx \frac{k}{N} \text{ for small } k/N
$$

The selection intensity $I$ (expected fitness of selected parents in standard deviations above mean):
- Tournament size 2: $I \approx 0.56$
- Tournament size 5: $I \approx 1.16$
- Tournament size 10: $I \approx 1.54$

Higher selection intensity → faster convergence but higher risk of premature convergence (loss of diversity).

**Biological Parallel:** This maps directly to the strength of natural selection. Strong selection (large $s$) fixes beneficial alleles faster but reduces standing variation — the exploration-exploitation tradeoff.

---

### 9.2 — Multi-Objective Evolution: NSGA-II

**Cross-link [10.7 - Evolutionary Computation](10.7---Evolutionary-Computation)**

Real organisms optimize multiple conflicting objectives simultaneously. NSGA-II (Non-dominated Sorting Genetic Algorithm II, Deb et al., 2002) handles this elegantly.

**Pareto Dominance:**

Solution $\mathbf{a}$ dominates $\mathbf{b}$ ($\mathbf{a} \prec \mathbf{b}$) if:

$$
\forall i: f_i(\mathbf{a}) \leq f_i(\mathbf{b}) \quad \text{AND} \quad \exists j: f_j(\mathbf{a}) < f_j(\mathbf{b})
$$

**NSGA-II Algorithm:**

1. **Non-dominated sorting**: Rank population into fronts $F_1, F_2, \ldots$
   - $F_1$ = Pareto front (non-dominated solutions)
   - $F_2$ = non-dominated after removing $F_1$, etc.

2. **Crowding distance**: Within each front, prefer solutions in sparse regions:

$$
d_i = \sum_{m=1}^{M} \frac{f_m^{i+1} - f_m^{i-1}}{f_m^{\max} - f_m^{\min}}
$$

3. **Selection**: Prefer (a) lower rank, then (b) higher crowding distance

**Biological Examples of Multi-Objective Tradeoffs:**

| Objective 1 | Objective 2 | Organism | Pareto Front |
|:---|:---|:---|:---|
| Speed | Endurance | Mammals | Cheetah (speed) ↔ Wolf (endurance) |
| Offspring number | Offspring size | Fish | Cod (millions tiny) ↔ Shark (few large) |
| Growth rate | Stress tolerance | Bacteria | Fast growers ↔ Persisters |
| Immune strength | Autoimmune risk | Vertebrates | Strong defense ↔ Self-tolerance |

```python
import numpy as np

def nsga2_selection(population, objectives, pop_size):
    """
    NSGA-II selection: non-dominated sorting + crowding distance.
    
    population: list of solutions
    objectives: (n_solutions, n_objectives) array of fitness values (minimize)
    """
    n = len(population)
    n_obj = objectives.shape[1]
    
    # Step 1: Non-dominated sorting
    domination_count = np.zeros(n, dtype=int)
    dominated_set = [[] for _ in range(n)]
    fronts = []()
    
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            # Does i dominate j?
            if all(objectives[i] <= objectives[j]) and any(objectives[i] < objectives[j]):
                dominated_set[i].append(j)
            elif all(objectives[j] <= objectives[i]) and any(objectives[j] < objectives[i]):
                domination_count[i] += 1
        
        if domination_count[i] == 0:
            fronts[0].append(i)
    
    # Build subsequent fronts
    k = 0
    while fronts[k]:
        next_front = []
        for i in fronts[k]:
            for j in dominated_set[i]:
                domination_count[j] -= 1
                if domination_count[j] == 0:
                    next_front.append(j)
        k += 1
        fronts.append(next_front)
    
    fronts = [f for f in fronts if f]  # Remove empty
    
    # Step 2: Crowding distance within each front
    crowding = np.zeros(n)
    for front in fronts:
        if len(front) <= 2:
            crowding[front] = float('inf')
            continue
        for m in range(n_obj):
            sorted_idx = sorted(front, key=lambda x: objectives[x, m])
            crowding[sorted_idx[0]] = float('inf')
            crowding[sorted_idx[-1]] = float('inf')
            obj_range = objectives[sorted_idx[-1], m] - objectives[sorted_idx[0], m]
            if obj_range == 0:
                continue
            for i in range(1, len(sorted_idx)-1):
                crowding[sorted_idx[i]] += (
                    objectives[sorted_idx[i+1], m] - objectives[sorted_idx[i-1], m]
                ) / obj_range
    
    # Step 3: Select top pop_size by (rank, crowding distance)
    selected = []
    for front in fronts:
        if len(selected) + len(front) <= pop_size:
            selected.extend(front)
        else:
            remaining = pop_size - len(selected)
            front_sorted = sorted(front, key=lambda x: -crowding[x])
            selected.extend(front_sorted[:remaining])
            break
    
    return selected

# Example: optimize neural network for accuracy vs. model size
# objectives = np.column_stack([1-accuracy, model_params])
# selected = nsga2_selection(population, objectives, pop_size=50)
```

---

### 9.3 — Fitness Landscapes and Loss Surfaces: A Unified View

**Sewall Wright's Adaptive Landscape (1932):**

The fitness landscape maps genotype space to fitness:

$$
W: \{0,1\}^L \rightarrow \mathbb{R}^+
$$

where $L$ = genome length. Evolution is a population moving on this landscape under the forces of selection (climbing) and drift (random walks).

**Deep Learning Loss Surfaces:**

The loss landscape maps parameter space to loss:

$$
\mathcal{L}: \mathbb{R}^d \rightarrow \mathbb{R}^+
$$

where $d$ = number of parameters. Training is gradient descent on this landscape.

**Structural Parallels:**

| Property | Fitness Landscape | Loss Surface |
|:---|:---|:---|
| Dimensionality | $L$ (genome length, ~10⁹ for humans) | $d$ (parameters, ~10⁹ for GPT-3) |
| Navigation | Selection + drift + mutation | SGD + noise + learning rate |
| Local optima | Evolutionary dead ends | Training plateaus |
| Saddle points | Neutral ridges | Common in high-$d$ |
| Ruggedness | Epistasis (gene interactions) | Non-linearity (layer interactions) |
| Escape mechanism | Genetic drift, recombination | Learning rate warmup, noise |

**Key Insight (Choromanska et al., 2015):** In high-dimensional spaces, most critical points are saddle points, not local minima. The loss values of local minima concentrate near the global minimum. This explains why SGD works despite non-convexity — and why evolution can find good solutions despite vast genotype spaces.

---

### 9.4 — Neutral Networks and Robustness

**Neutral Networks (Schuster et al., 1994):**

In sequence space, a **neutral network** is the set of all sequences that fold into the same RNA secondary structure (or produce the same phenotype):

$$
\mathcal{N}_\phi = \{\mathbf{s} \in \{A,C,G,U\}^L : \text{structure}(\mathbf{s}) = \phi\}
$$

Properties:
- Neutral networks are **extensive** (span a large fraction of sequence space)
- They are **connected** (any two sequences in the network can be reached by single-point mutations through the network)
- Different neutral networks are **interwoven** (close in sequence space)

**Evolutionary Implications:**

1. **Neutral drift** explores the neutral network without fitness cost
2. This exploration brings the population to the **boundary** of other neutral networks
3. When the environment changes, the population is pre-adapted to access new phenotypes

**AI Parallel — Flat Minima in Deep Learning:**

Flat minima in loss landscapes are analogous to large neutral networks:
- Solutions in flat minima generalize better (Hochreiter & Schmidhuber, 1997)
- SGD with large learning rates preferentially finds flat minima (noise helps escape sharp minima)
- This is analogous to genetic drift preferentially sampling large neutral networks

$$
P(\text{population on network } \mathcal{N}) \propto |\mathcal{N}| \quad \text{(larger networks are more likely to be occupied)}
$$

---

### 9.5 — Evolutionary Game Theory: The Replicator Equation

**The Replicator Equation:**

For $n$ strategies with frequencies $x_i$ and payoff matrix $A$:

$$
\dot{x}_i = x_i \left[(A\mathbf{x})_i - \mathbf{x}^T A \mathbf{x}\right]
$$

This says: strategy $i$ grows if its fitness $(A\mathbf{x})_i$ exceeds the population mean fitness $\mathbf{x}^T A \mathbf{x}$.

**Hawk-Dove Game:**

$$
A = \begin{pmatrix} (V-C)/2 & V \\ 0 & V/2 \end{pmatrix}
$$

where $V$ = resource value, $C$ = cost of fighting.

If $C > V$: ESS (Evolutionarily Stable Strategy) is a mixed population with fraction $V/C$ Hawks.

**Connection to Reinforcement Learning:**

The replicator equation is equivalent to the **multiplicative weights update** algorithm in online learning:

$$
w_i^{t+1} = w_i^t \cdot (1 + \eta \cdot r_i^t)
$$

where $r_i^t$ is the reward for strategy $i$ at time $t$. This connects evolutionary dynamics directly to multi-agent RL and bandit algorithms.

> **Cross-link [10.7 - Reinforcement Learning](10.7---Reinforcement-Learning):** Evolutionary game theory provides the theoretical foundation for multi-agent RL. Nash equilibria in games correspond to evolutionary stable strategies; the replicator dynamic is the continuous-time limit of policy gradient methods in self-play.

---

### 9.6 — Phylogenomics and the Tree of Life: Computational Challenges

**The Combinatorial Explosion:**

The number of possible unrooted binary trees for $n$ taxa:

$$
N_{\text{trees}} = \frac{(2n-5)!}{2^{n-3}(n-3)!}
$$

| Taxa | Trees |
|:---:|:---:|
| 4 | 3 |
| 10 | 2,027,025 |
| 20 | 2.2 × 10²⁰ |
| 50 | 2.8 × 10⁷⁶ |
| 100 | ~10¹⁸² |

For 100 species, exhaustive search is impossible — heuristic methods (hill-climbing, MCMC) are essential.

**Incomplete Lineage Sorting (ILS):**

Gene trees can differ from the species tree due to ancestral polymorphism:

$$
P(\text{gene tree} \neq \text{species tree}) = \frac{2}{3} e^{-t/(2N_e)}
$$

where $t$ = time between speciation events (in generations). For rapid radiations ($t \ll 2N_e$), most gene trees disagree with the species tree — requiring coalescent-based methods (ASTRAL, *BEAST) for accurate species tree inference.

> **AI Bridge:** Phylogenetic tree search is a combinatorial optimization problem structurally similar to **neural architecture search** — both explore exponentially large discrete spaces using heuristic methods. Bayesian phylogenetics (MCMC on tree space) parallels Bayesian neural network inference (MCMC on weight space).

