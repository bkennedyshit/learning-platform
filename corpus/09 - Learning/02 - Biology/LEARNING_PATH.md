---
date: 2026-05-24
title: "Track 02 — Biology: Learning Path"
mission: Structured progression through college biology with curated free resources and milestone checkpoints
status: active
tags: [biology, learning-path, curriculum, resources, milestones]
type: learning-path
---

*Back to [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/02 - Biology/Subject_Plan]] | Part of [[09 - Learning Index]]*

# Track 02 — Biology: Learning Path

> *"The capacity to blunder slightly is the real marvel of DNA. Without this special attribute, we would still be anaerobic bacteria."*
> — **Lewis Thomas**, *The Medusa and the Snail* (1979)

---

## 🗺️ Full Dependency Graph

```mermaid
mindmap
  root((Track 15: Biology))
    Phase 1: Molecular Foundations
      02.1 Cell Biology
        Membrane structure
        Organelle function
        Enzyme kinetics
        ATP & metabolism
      02.3 Central Dogma
        DNA replication
        Transcription
        RNA processing
        Translation
        Post-translational mods
      02.2 Genetics
        Mendel's laws
        Punnett squares
        Linkage mapping
        Epistasis & pleiotropy
    Phase 2: Evolution & Populations
      02.4 Evolution
        Natural selection
        Hardy-Weinberg
        Genetic drift
        Molecular evolution
        Neutral theory
      02.5 Ecology
        Energy flow
        Trophic cascades
        Population dynamics
        Island biogeography
        Biodiversity metrics
    Phase 3: Organismal Biology
      02.6 Anatomy & Physiology
        Musculoskeletal
        Cardiovascular
        Respiratory
        Endocrine
        Nervous → Track 11
      02.7 Immunology
        Innate immunity
        Adaptive immunity
        V(D)J recombination
        Vaccines
        Autoimmunity
    Phase 4: Frontier
      02.8 Modern Biology
        CRISPR-Cas9
        Prime editing
        Gene drives
        Synthetic biology
        mRNA therapeutics
```

---

## 📅 Weekly Schedule (8-Week Plan)

### Week 1–2: Molecular Foundations

| Day | Activity | Resource | Time |
|:---:|:---|:---|:---:|
| 1 | Read 02.1 §1–2 (Definitions + Mechanisms) | This vault + Khan Academy | 90 min |
| 2 | Read 02.1 §3–4 (Michaelis-Menten + Examples) | MIT 7.012 Lecture 2–3 | 90 min |
| 3 | Read 02.3 §1–2 (Central Dogma mechanisms) | Alberts Ch. 6–7 / Khan | 120 min |
| 4 | Read 02.3 §3–4 (Info theory + Worked examples) | MIT 7.012 Lecture 6–8 | 90 min |
| 5 | Practice: Run `15.3_central_dogma.py` drills | Terminal | 60 min |
| 6 | Read 02.1 §5–7 (AI connections, health, cross-links) | This vault | 60 min |
| 7 | Review + Anki cards | Spaced repetition | 45 min |
| 8 | Read 02.2 §1–2 (Genetics definitions + mechanisms) | Khan + Bozeman | 90 min |
| 9 | Read 02.2 §3–4 (Probability models + Punnett drills) | MIT 7.013 Lecture 4–6 | 90 min |
| 10 | Practice: Run `15.2_genetics.py` Punnett generators | Terminal | 60 min |
| 11 | Read 02.2 §5–7 (AI, health, cross-links) | This vault | 60 min |
| 12 | Milestone quiz: Molecular foundations | Self-test | 45 min |

**Milestone 1 Checkpoint:** Can you trace a gene from DNA → mRNA → protein, predict offspring ratios for a dihybrid cross, and sketch Michaelis-Menten kinetics?

---

### Week 3–4: Evolution & Ecology

| Day | Activity | Resource | Time |
|:---:|:---|:---|:---:|
| 13 | Read 02.4 §1–2 (Evolution mechanisms) | Darwin + MIT 7.014 Lec 1–3 | 120 min |
| 14 | Read 02.4 §3 (Hardy-Weinberg derivation, dN/dS) | This vault + Khan | 90 min |
| 15 | Read 02.4 §4 (Worked examples: allele frequencies) | MIT 7.014 problem sets | 90 min |
| 16 | Practice: Run `15.4_evolution.py` Hardy-Weinberg drills | Terminal | 60 min |
| 17 | Read 02.4 §5–7 (Genetic algorithms, cross-links) | This vault | 60 min |
| 18 | Read 02.5 §1–2 (Ecology mechanisms) | Bozeman + Khan | 90 min |
| 19 | Read 02.5 §3 (Lotka-Volterra, Shannon diversity) | MIT 7.014 Lec 8–10 | 90 min |
| 20 | Read 02.5 §4 (Ecosystem energy budgets) | This vault | 90 min |
| 21 | Practice: Run `15.5_ecology.py` population sims | Terminal | 60 min |
| 22 | Read 02.5 §5–7 (Procgen ecosystems, cross-links) | This vault | 60 min |
| 23 | Milestone quiz: Evolution & Ecology | Self-test | 45 min |

**Milestone 2 Checkpoint:** Can you derive Hardy-Weinberg equilibrium, calculate allele frequency changes under selection, solve Lotka-Volterra predator-prey dynamics, and explain how genetic algorithms mirror natural selection?

---

### Week 5–6: Organismal Biology

| Day | Activity | Resource | Time |
|:---:|:---|:---|:---:|
| 24 | Read 02.6 §1–2 (Anatomy systems overview) | Khan + Crash Course | 120 min |
| 25 | Read 02.6 §3–4 (Hill equation, cardiac output) | This vault | 90 min |
| 26 | Read 02.6 §5–7 (BMX biomechanics, Track 13 links) | This vault | 60 min |
| 27 | Read 02.7 §1–2 (Innate + adaptive immunity) | Khan + NIH iBiology | 120 min |
| 28 | Read 02.7 §3 (V(D)J combinatorics, clonal selection) | MIT 7.012 Lec 18–20 | 90 min |
| 29 | Read 02.7 §4 (Vaccine mechanisms worked examples) | This vault + NIH | 90 min |
| 30 | Practice: Run `15.7_immunology.py` drills | Terminal | 60 min |
| 31 | Read 02.7 §5–7 (Adversarial ML, health, cross-links) | This vault | 60 min |
| 32 | Milestone quiz: Organismal biology | Self-test | 45 min |

**Milestone 3 Checkpoint:** Can you trace blood flow through the heart, explain V(D)J recombination diversity, compare mRNA vs viral-vector vaccines, and connect immune recognition to anomaly detection in ML?

---

### Week 7–8: Frontier Biology & Integration

| Day | Activity | Resource | Time |
|:---:|:---|:---|:---:|
| 33 | Read 02.8 §1–2 (CRISPR mechanism, prime editing) | Doudna lectures + NIH iBiology | 120 min |
| 34 | Read 02.8 §3–4 (Gene drives, synthetic bio examples) | Nature free articles | 90 min |
| 35 | Read 02.8 §5–7 (ML for protein design, cross-links) | This vault | 60 min |
| 36 | Integration: Build concept map connecting all 8 chapters | Obsidian canvas | 90 min |
| 37 | Practice: Full problem set (all scripts, --count 10 each) | Terminal | 90 min |
| 38 | Review weak areas identified by practice scores | Targeted re-read | 90 min |
| 39 | Final milestone: Comprehensive self-test | All chapters | 60 min |

**Milestone 4 Checkpoint:** Can you explain CRISPR-Cas9 mechanism step-by-step, design a gene drive for a target organism, describe how AlphaFold uses evolutionary data, and connect synthetic biology to software engineering principles?

---

## 📚 Curated Free Resources (Verified)

### Video Lecture Series

| Series | Instructor | Platform | Best For |
|:---|:---|:---|:---|
| MIT 7.012 (Fall 2004) | Eric Lander, Robert Weinberg | MIT OCW | Molecular bio, genetics |
| MIT 7.013 (Spring 2018) | Hazel Sive, Tyler Jacks | MIT OCW | Genetics depth |
| MIT 7.014 (Spring 2005) | Graham Walker, Penny Chisholm | MIT OCW | Ecology, evolution |
| Khan Academy Biology | Sal Khan et al. | khanacademy.org | All topics, practice |
| Bozeman Science AP Bio | Paul Andersen | YouTube | Concise explanations |
| Crash Course Biology | Hank Green | YouTube | Engaging overview |
| NIH iBiology | Various researchers | ibiology.org | Cutting-edge research |
| HHMI BioInteractive | Various | biointeractive.org | Evolution, genetics |
| iBiology CRISPR Series | Jennifer Doudna, Feng Zhang | ibiology.org | CRISPR mechanism |

### Textbooks (Reference)

| Title | Authors | Best For |
|:---|:---|:---|
| Campbell's Biology (14th) | Urry, Cain, Wasserman | Comprehensive reference |
| Molecular Biology of the Cell | Alberts et al. | Molecular depth |
| Genetics: From Genes to Genomes | Hartwell et al. | Genetics problems |
| Evolutionary Analysis | Herron, Freeman | Evolution + pop gen |
| Ecology (Cain, Bowman, Hacker) | — | Quantitative ecology |
| Janeway's Immunobiology | Murphy, Weaver | Immunology gold standard |

### Interactive Tools

| Tool | URL | Use |
|:---|:---|:---|
| NCBI BLAST | blast.ncbi.nlm.nih.gov | Sequence alignment |
| UniProt | uniprot.org | Protein database |
| PDB (Protein Data Bank) | rcsb.org | 3D protein structures |
| PhyloT | phylot.biobyte.de | Phylogenetic trees |
| Hardy-Weinberg Sim | radford.edu/~rsheehy/Gen_flash/popgen/ | Population genetics |

---

## 🎯 Competency Milestones

### Level 1: Molecular Literacy (After 15.1–02.3)
- [ ] Diagram a eukaryotic cell with all major organelles and their functions
- [ ] Trace central dogma: DNA → pre-mRNA → mature mRNA → polypeptide → folded protein
- [ ] Solve Michaelis-Menten problems (find Km, Vmax from data)
- [ ] Predict offspring phenotype ratios for mono/dihybrid crosses
- [ ] Calculate map distances from recombination frequencies

### Level 2: Evolutionary Thinking (After 15.4–02.5)
- [ ] Derive Hardy-Weinberg from first principles
- [ ] Calculate allele frequency change under selection (Δp per generation)
- [ ] Solve Lotka-Volterra predator-prey systems numerically
- [ ] Compute Shannon diversity index for a community
- [ ] Explain neutral theory vs selectionism debate

### Level 3: Systems Biology (After 15.6–02.7)
- [ ] Trace blood flow through all four heart chambers
- [ ] Calculate cardiac output from stroke volume and heart rate
- [ ] Explain V(D)J recombination and calculate theoretical TCR diversity
- [ ] Compare mechanisms of mRNA, viral-vector, and inactivated vaccines
- [ ] Connect immune system pattern recognition to ML anomaly detection

### Level 4: Frontier Fluency (After 02.8)
- [ ] Explain CRISPR-Cas9 mechanism including PAM recognition and DSB repair
- [ ] Describe prime editing vs base editing vs HDR
- [ ] Design a theoretical gene drive and identify ecological risks
- [ ] Explain how AlphaFold leverages MSA (multiple sequence alignment)
- [ ] Connect BioBricks/synthetic biology to software modularity

---

## 🔄 Spaced Repetition Integration

Practice scripts in `_practice/scripts/` generate fresh problems on each run:

```bash
# Generate 20 genetics problems
python "_practice/scripts/15.2_genetics.py" --count 20 --seed 42

# Generate Hardy-Weinberg drills
python "_practice/scripts/15.4_evolution.py" --count 15

# Generate ecology population dynamics
python "_practice/scripts/15.5_ecology.py" --count 12

# Generate immunology diversity calculations
python "_practice/scripts/15.7_immunology.py" --count 10
```

Output files land in `_practice/` with frontmatter tagged for Obsidian's SR plugin.

---

## Related Notes
- [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/02 - Biology/Subject_Plan]] - Shared curriculum/biology focus
- [[02.1 - Cell Biology & Molecular Foundations]] - Same Biology folder
- [[02.2 - Genetics & Inheritance]] - Same Biology folder
- [[02.3 - DNA, RNA & Protein Synthesis]] - Same Biology folder
- [[02.4 - Evolution & Natural Selection]] - Same Biology folder
