---
title: "03.3 — Stoichiometry & Reactions"
subject: "Chemistry"
catalog: advanced
audience_tier: higher-education
chapter: "03.3"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 03.3 — Stoichiometry & Reactions

> *"Nothing is lost, nothing is created, everything is transformed."* — Antoine Lavoisier, 1789

Stoichiometry is the quantitative backbone of chemistry — the accounting system that tells you exactly how much of each substance reacts and how much product forms. It's fundamentally dimensional analysis with one key conversion factor: the mole. If you can do unit conversions, you can do stoichiometry.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Convert between mass, moles, and number of particles using Avogadro's number and molar mass.
2. Balance chemical equations by inspection and by the half-reaction method (for redox).
3. Identify limiting reagents and calculate theoretical yield.
4. Calculate percent yield and percent composition.
5. Classify reactions by type: synthesis, decomposition, single replacement, double replacement, combustion, acid-base, redox.
6. Perform solution stoichiometry (molarity, dilution, titration calculations).
7. Apply stoichiometry to gas-phase reactions using the ideal gas law.

---

## 🖼️ Visual Anchor — The Stoichiometry Roadmap

![chem__16.3-fig1](chem__16.3-fig1.svg)

---

## 📚 1. Definitions

### Definition 03.3.1 — The Mole

One **mole** of any substance contains exactly $N_A = 6.022 \times 10^{23}$ entities (atoms, molecules, ions, etc.). This is **Avogadro's number**.

$$
n = \frac{N}{N_A} = \frac{m}{M}
$$

where $n$ = moles, $N$ = number of particles, $m$ = mass (g), $M$ = molar mass (g/mol).

### Definition 03.3.2 — Molar Mass ($M$)

The mass of one mole of a substance, numerically equal to the atomic/molecular weight in g/mol.

Example: H₂O has $M = 2(1.008) + 03.00 = 18.02$ g/mol.

### Definition 03.3.3 — Stoichiometric Coefficients

The integers in a balanced equation that give the mole ratios of reactants and products.

$$
2\text{H}_2 + \text{O}_2 \to 2\text{H}_2\text{O}
$$

Ratio: 2 mol H₂ : 1 mol O₂ : 2 mol H₂O.

### Definition 03.3.4 — Limiting Reagent

The reactant that is completely consumed first, determining the maximum amount of product (theoretical yield).

### Definition 03.3.5 — Percent Yield

$$
\%\text{ yield} = \frac{\text{actual yield}}{\text{theoretical yield}} \times 100\%
$$

### Definition 03.3.6 — Molarity ($M$ or $c$)

$$
c = \frac{n_{\text{solute}}}{V_{\text{solution}}} \quad \text{(mol/L)}
$$

### Definition 03.3.7 — Oxidation State

The hypothetical charge an atom would have if all bonds were completely ionic. Rules:
1. Free elements: 0
2. Monatomic ions: equal to charge
3. H: +1 (except metal hydrides: −1)
4. O: −2 (except peroxides: −1)
5. Sum of oxidation states = overall charge

---

## 📐 2. Mathematical Foundations

### 2.1 Dimensional Analysis Framework

Every stoichiometry problem is a chain of unit conversions:

$$
\text{Given} \xrightarrow{\text{conversion factor 1}} \text{moles of A} \xrightarrow{\text{mole ratio}} \text{moles of B} \xrightarrow{\text{conversion factor 2}} \text{Answer}
$$

**The mole ratio comes from the balanced equation.** This is the ONLY step that requires chemistry knowledge; everything else is arithmetic.

### 2.2 Balancing Equations: The Linear Algebra Approach

A chemical equation $\sum_i \nu_i A_i = 0$ (with products positive, reactants negative) must satisfy atom conservation. For each element $j$:

$$
\sum_i \nu_i \cdot a_{ij} = 0
$$

where $a_{ij}$ = number of atoms of element $j$ in species $i$. This is a homogeneous linear system $\mathbf{A}\boldsymbol{\nu} = \mathbf{0}$ — solvable by the null space methods from [2.3 - Systems of Linear Equations & Row Reduction](2.3---Systems-of-Linear-Equations-&-Row-Reduction).

**Example:** Balance $\text{Fe}_2\text{O}_3 + \text{CO} \to \text{Fe} + \text{CO}_2$

Let coefficients be $a, b, c, d$:
- Fe: $2a = c$
- O: $3a + b = 2d$
- C: $b = d$

From C: $d = b$. From Fe: $c = 2a$. From O: $3a + b = 2b \Rightarrow b = 3a$.

Set $a = 1$: $b = 3, c = 2, d = 3$.

$$
\text{Fe}_2\text{O}_3 + 3\text{CO} \to 2\text{Fe} + 3\text{CO}_2
$$

### 2.3 The Ideal Gas Law in Stoichiometry

$$
PV = nRT, \quad R = 0.08206 \text{ L·atm/(mol·K)} = 8.314 \text{ J/(mol·K)}
$$

At STP (0°C, 1 atm): 1 mol of any ideal gas occupies 22.4 L.

### 2.4 Dilution Equation

$$
c_1 V_1 = c_2 V_2
$$

(Moles of solute are conserved when diluting.)

---

## 🔬 3. Chemical Mechanisms

### 3.1 Reaction Classification

| Type | General Form | Example |
|---|---|---|
| Synthesis | A + B → AB | 2Na + Cl₂ → 2NaCl |
| Decomposition | AB → A + B | 2H₂O₂ → 2H₂O + O₂ |
| Single replacement | A + BC → AC + B | Zn + CuSO₄ → ZnSO₄ + Cu |
| Double replacement | AB + CD → AD + CB | AgNO₃ + NaCl → AgCl↓ + NaNO₃ |
| Combustion | CₓHᵧ + O₂ → CO₂ + H₂O | CH₄ + 2O₂ → CO₂ + 2H₂O |
| Acid-base | HA + BOH → BA + H₂O | HCl + NaOH → NaCl + H₂O |

### 3.2 Balancing Redox Equations: Half-Reaction Method

**Step 1:** Assign oxidation states. Identify what's oxidized and what's reduced.

**Step 2:** Write separate half-reactions.

**Step 3:** Balance atoms (other than O and H first, then O with H₂O, then H with H⁺).

**Step 4:** Balance charge with electrons.

**Step 5:** Multiply half-reactions so electrons cancel.

**Step 6:** Add half-reactions and simplify.

**In basic solution:** After Step 6, add OH⁻ to both sides to neutralize H⁺ → H₂O.

### 3.3 The Activity Series

Metals ranked by reactivity (ability to be oxidized):

$$
\text{Li} > \text{K} > \text{Ca} > \text{Na} > \text{Mg} > \text{Al} > \text{Zn} > \text{Fe} > \text{Ni} > \text{Sn} > \text{Pb} > \text{H} > \text{Cu} > \text{Ag} > \text{Au}
$$

A metal can displace any metal BELOW it from solution.

---

## ✍️ 4. Worked Examples

### Example 03.3.1 — Limiting Reagent and Theoretical Yield

**Problem:** 10.0 g of aluminum reacts with 35.0 g of chlorine gas. How many grams of AlCl₃ can be produced?

$$
2\text{Al} + 3\text{Cl}_2 \to 2\text{AlCl}_3
$$

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Convert to moles.

$$
n_{\text{Al}} = \frac{10.0 \text{ g}}{26.98 \text{ g/mol}} = 0.3707 \text{ mol}
$$

$$
n_{\text{Cl}_2} = \frac{35.0 \text{ g}}{70.90 \text{ g/mol}} = 0.4936 \text{ mol}
$$

**Step 2:** Determine limiting reagent using mole ratios.

From the equation: 2 mol Al requires 3 mol Cl₂.

Al needs: $0.3707 \times \frac{3}{2} = 0.5561$ mol Cl₂. We only have 0.4936 mol Cl₂.

Cl₂ needs: $0.4936 \times \frac{2}{3} = 0.3291$ mol Al. We have 0.3707 mol Al.

**Cl₂ is the limiting reagent** (we don't have enough of it).

**Step 3:** Calculate theoretical yield from limiting reagent.

$$
n_{\text{AlCl}_3} = 0.4936 \text{ mol Cl}_2 \times \frac{2 \text{ mol AlCl}_3}{3 \text{ mol Cl}_2} = 0.3291 \text{ mol}
$$

$$
m_{\text{AlCl}_3} = 0.3291 \text{ mol} \times 133.34 \text{ g/mol} = 43.9 \text{ g}
$$

**Step 4:** Calculate excess Al remaining.

Al consumed: $0.3291$ mol. Al remaining: $0.3707 - 0.3291 = 0.0416$ mol = 1.12 g.

</details>

---

### Example 03.3.2 — Balancing a Redox Equation in Acidic Solution

**Problem:** Balance: $\text{MnO}_4^- + \text{Fe}^{2+} \to \text{Mn}^{2+} + \text{Fe}^{3+}$ (acidic solution).

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Assign oxidation states.
- Mn in MnO₄⁻: +7 → Mn²⁺: +2 (reduced, gains 5e⁻)
- Fe²⁺: +2 → Fe³⁺: +3 (oxidized, loses 1e⁻)

**Step 2:** Write half-reactions.

Reduction: $\text{MnO}_4^- \to \text{Mn}^{2+}$

Oxidation: $\text{Fe}^{2+} \to \text{Fe}^{3+}$

**Step 3:** Balance reduction half-reaction.

Balance O with H₂O: $\text{MnO}_4^- \to \text{Mn}^{2+} + 4\text{H}_2\text{O}$

Balance H with H⁺: $8\text{H}^+ + \text{MnO}_4^- \to \text{Mn}^{2+} + 4\text{H}_2\text{O}$

Balance charge with e⁻: Left = $8(+1) + (-1) = +7$. Right = $+2$. Need 5e⁻ on left.

$$
5e^- + 8\text{H}^+ + \text{MnO}_4^- \to \text{Mn}^{2+} + 4\text{H}_2\text{O}
$$

**Step 4:** Balance oxidation half-reaction.

$$
\text{Fe}^{2+} \to \text{Fe}^{3+} + e^-
$$

**Step 5:** Multiply to equalize electrons.

Multiply oxidation by 5:

$$
5\text{Fe}^{2+} \to 5\text{Fe}^{3+} + 5e^-
$$

**Step 6:** Add half-reactions.

$$
\boxed{5\text{Fe}^{2+} + 8\text{H}^+ + \text{MnO}_4^- \to 5\text{Fe}^{3+} + \text{Mn}^{2+} + 4\text{H}_2\text{O}}
$$

**Verify:** Atoms balanced ✓. Charge: Left = $5(2) + 8(1) + (-1) = +17$. Right = $5(3) + 2 + 0 = +17$. ✓

</details>

---

### Example 03.3.3 — Solution Stoichiometry: Titration

**Problem:** 25.00 mL of an unknown HCl solution requires 18.75 mL of 0.1000 M NaOH to reach the equivalence point. What is the molarity of the HCl?

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Write the balanced equation.

$$
\text{HCl} + \text{NaOH} \to \text{NaCl} + \text{H}_2\text{O}
$$

Mole ratio: 1:1.

**Step 2:** Calculate moles of NaOH used.

$$
n_{\text{NaOH}} = c \times V = 0.1000 \text{ mol/L} \times 0.01875 \text{ L} = 1.875 \times 10^{-3} \text{ mol}
$$

**Step 3:** From 1:1 ratio: $n_{\text{HCl}} = 1.875 \times 10^{-3}$ mol.

**Step 4:** Calculate molarity of HCl.

$$
c_{\text{HCl}} = \frac{1.875 \times 10^{-3} \text{ mol}}{0.02500 \text{ L}} = 0.07500 \text{ M}
$$

</details>

---

### Example 03.3.4 — Gas Stoichiometry

**Problem:** What volume of O₂ at 25°C and 1.00 atm is needed to completely combust 5.00 g of propane (C₃H₈)?

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Balanced equation.

$$
\text{C}_3\text{H}_8 + 5\text{O}_2 \to 3\text{CO}_2 + 4\text{H}_2\text{O}
$$

**Step 2:** Moles of propane.

$$
n_{\text{C}_3\text{H}_8} = \frac{5.00}{44.10} = 0.1134 \text{ mol}
$$

**Step 3:** Moles of O₂ needed.

$$
n_{\text{O}_2} = 0.1134 \times 5 = 0.5670 \text{ mol}
$$

**Step 4:** Volume from ideal gas law.

$$
V = \frac{nRT}{P} = \frac{0.5670 \times 0.08206 \times 298.15}{1.00} = 13.9 \text{ L}
$$

</details>

---

## 🧠 5. Connections to Other Tracks

| This Chapter | Connects To | How |
|---|---|---|
| Balancing equations (null space) | [2.3 - Systems of Linear Equations & Row Reduction](2.3---Systems-of-Linear-Equations-&-Row-Reduction) | Atom balance is a homogeneous linear system |
| Ideal gas law | [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy) | $PV = Nk_BT$ derived from partition function |
| Dimensional analysis | [4.1 - Newton's Laws & Kinematics](4.1---Newton's-Laws-&-Kinematics) | Same unit-conversion methodology |
| Redox reactions | [03.6 - Electrochemistry & Redox](03.6---Electrochemistry-&-Redox) | Quantitative electrochemistry |
| Reaction types | [03.4 - Thermodynamics & Kinetics](03.4---Thermodynamics-&-Kinetics) | Energy changes in reactions |

---

## ⚠️ 6. Common Misconceptions & Where Most Students Fail

### ❌ Misconception 1: "The mole is just a big number"

**The truth:** The mole is a BRIDGE between the atomic scale (where we count atoms) and the lab scale (where we weigh grams). It's the conversion factor between amu and grams: 1 mol of atoms with mass $M$ amu weighs exactly $M$ grams. That's not a coincidence — it's the definition.

### ❌ Misconception 2: "Coefficients tell you the number of grams"

**The truth:** Coefficients give MOLE ratios, not mass ratios. $2\text{H}_2 + \text{O}_2 \to 2\text{H}_2\text{O}$ means 2 moles H₂ (4 g) + 1 mole O₂ (32 g) → 2 moles H₂O (36 g). The mass ratio is 4:32:36, NOT 2:1:2.

### ❌ Misconception 3: "The bigger amount is always the excess reagent"

**The truth:** You must compare moles RELATIVE TO THE STOICHIOMETRIC RATIO. 100 g of Al (3.7 mol) vs 100 g of Cl₂ (1.4 mol) — Al looks like more, but the reaction needs 3 mol Cl₂ per 2 mol Al, so Cl₂ is actually limiting.

### ❌ Misconception 4: "Balancing equations is just trial and error"

**The truth:** It's a systematic linear algebra problem. For complex equations (especially redox), the half-reaction method is algorithmic — follow the steps and you'll always get the answer. No guessing required.

### ❌ Misconception 5: "Percent yield should always be 100%"

**The truth:** Real reactions rarely achieve 100% yield due to: side reactions, incomplete reactions (equilibrium), loss during purification, and measurement errors. A 70% yield is often considered good in organic synthesis.

### 💪 The Pep Talk

Stoichiometry is the chapter where many students first feel overwhelmed — not because it's conceptually hard, but because it requires careful, systematic work. Every stoichiometry problem is the same algorithm:

1. Write the balanced equation
2. Convert given → moles
3. Use mole ratio
4. Convert moles → answer

If you can do dimensional analysis (and you can — you've been doing it in physics), you can do stoichiometry. The only new thing is the mole concept. Master that, and this chapter is straightforward.

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- [03.2 - Chemical Bonding - Ionic, Covalent, Metallic & Intermolecular](03.2---Chemical-Bonding---Ionic,-Covalent,-Metallic-&-Intermolecular) — Bond types determine reaction products
- [03.4 - Thermodynamics & Kinetics](03.4---Thermodynamics-&-Kinetics) — Energy and rate of reactions
- [03.6 - Electrochemistry & Redox](03.6---Electrochemistry-&-Redox) — Quantitative redox chemistry
- [2.3 - Systems of Linear Equations & Row Reduction](2.3---Systems-of-Linear-Equations-&-Row-Reduction) — Balancing as linear algebra

### External References
- **MIT 5.111 OCW** — Lectures 13–15: Stoichiometry and reactions
- **Khan Academy** — [Stoichiometry](https://www.khanacademy.org/science/chemistry/chemical-reactions-stoichiome)
- **Crash Course Chemistry** — Episodes 6–8: The mole, stoichiometry
- **NileRed** — Practical demonstrations of reaction types

---

## 🔬 8. Advanced Derivations — Quantitative Reaction Analysis

### 8.1 — Balancing Redox Reactions by the Half-Reaction Method

The half-reaction method is the only systematic way to balance complex redox equations. It separates oxidation and reduction, balances each independently, then combines them.

**The Algorithm (in acidic solution):**

1. Identify what's oxidized and what's reduced (assign oxidation states).
2. Write separate half-reactions.
3. Balance atoms OTHER than O and H.
4. Balance O by adding H₂O.
5. Balance H by adding H⁺.
6. Balance charge by adding electrons (e⁻).
7. Multiply half-reactions so electrons cancel.
8. Add half-reactions and simplify.

**For basic solution:** After step 8, add OH⁻ to both sides to neutralize all H⁺ → H₂O.

**Worked Example — Permanganate oxidizes iron(II) in acidic solution:**

$$
\text{MnO}_4^- + \text{Fe}^{2+} \to \text{Mn}^{2+} + \text{Fe}^{3+}
$$

**Step 1:** Mn goes from +7 to +2 (reduced, gains 5e⁻). Fe goes from +2 to +3 (oxidized, loses 1e⁻).

**Step 2 — Reduction half-reaction:**

$$
\text{MnO}_4^- \to \text{Mn}^{2+}
$$

**Step 3:** Mn already balanced.

**Step 4:** Balance O with H₂O:

$$
\text{MnO}_4^- \to \text{Mn}^{2+} + 4\text{H}_2\text{O}
$$

**Step 5:** Balance H with H⁺:

$$
\text{MnO}_4^- + 8\text{H}^+ \to \text{Mn}^{2+} + 4\text{H}_2\text{O}
$$

**Step 6:** Balance charge with e⁻. Left side: $(-1) + (+8) = +7$. Right side: $+2$. Need 5e⁻ on left:

$$
\text{MnO}_4^- + 8\text{H}^+ + 5e^- \to \text{Mn}^{2+} + 4\text{H}_2\text{O}
$$

**Step 2 — Oxidation half-reaction:**

$$
\text{Fe}^{2+} \to \text{Fe}^{3+} + e^-
$$

**Step 7:** Multiply oxidation by 5:

$$
5\text{Fe}^{2+} \to 5\text{Fe}^{3+} + 5e^-
$$

**Step 8:** Add:

$$
\text{MnO}_4^- + 8\text{H}^+ + 5\text{Fe}^{2+} \to \text{Mn}^{2+} + 4\text{H}_2\text{O} + 5\text{Fe}^{3+}
$$

**Verification:** Atoms: 1 Mn ✓, 4 O ✓, 8 H ✓, 5 Fe ✓. Charge: left = $-1 + 8 + 10 = +17$; right = $+2 + 0 + 15 = +17$ ✓.

**Worked Example 2 — Dichromate in acidic solution (harder):**

$$
\text{Cr}_2\text{O}_7^{2-} + \text{C}_2\text{H}_5\text{OH} \to \text{Cr}^{3+} + \text{CO}_2
$$

**Reduction:** $\text{Cr}_2\text{O}_7^{2-} + 14\text{H}^+ + 6e^- \to 2\text{Cr}^{3+} + 7\text{H}_2\text{O}$

**Oxidation:** Ethanol to CO₂. Carbon goes from $-2$ (in C₂H₅OH, average) to $+4$ (in CO₂). Each C loses 6e⁻, so 2 carbons lose 12e⁻:

$$
\text{C}_2\text{H}_5\text{OH} + 3\text{H}_2\text{O} \to 2\text{CO}_2 + 12\text{H}^+ + 12e^-
$$

**Combine:** Multiply reduction by 2 (to get 12e⁻):

$$
2\text{Cr}_2\text{O}_7^{2-} + 28\text{H}^+ + 12e^- \to 4\text{Cr}^{3+} + 14\text{H}_2\text{O}
$$

**Add:**

$$
2\text{Cr}_2\text{O}_7^{2-} + \text{C}_2\text{H}_5\text{OH} + 16\text{H}^+ \to 4\text{Cr}^{3+} + 2\text{CO}_2 + 11\text{H}_2\text{O}
$$

### 8.2 — Limiting Reagent Analysis: Systematic Method

**The algorithm:**

1. Convert all given quantities to moles.
2. Divide each reactant's moles by its stoichiometric coefficient.
3. The smallest ratio identifies the limiting reagent.
4. Use the limiting reagent to calculate product amounts.

**Worked Example — Thermite reaction:**

$$
2\text{Al} + \text{Fe}_2\text{O}_3 \to \text{Al}_2\text{O}_3 + 2\text{Fe}
$$

Given: 10.0 g Al and 30.0 g Fe₂O₃.

**Step 1:** Convert to moles:
- $n(\text{Al}) = \frac{10.0}{26.98} = 0.3707\,\text{mol}$
- $n(\text{Fe}_2\text{O}_3) = \frac{30.0}{159.69} = 0.1879\,\text{mol}$

**Step 2:** Divide by coefficients:
- Al: $\frac{0.3707}{2} = 0.1854$
- Fe₂O₃: $\frac{0.1879}{1} = 0.1879$

**Step 3:** Al has the smaller ratio → Al is the limiting reagent.

**Step 4:** Products formed:
- $n(\text{Fe}) = 0.3707\,\text{mol}$ (same coefficient as Al)
- $m(\text{Fe}) = 0.3707 \times 55.85 = 20.7\,\text{g}$

**Excess Fe₂O₃ remaining:**
- Fe₂O₃ consumed: $0.3707/2 = 0.1854\,\text{mol}$
- Fe₂O₃ remaining: $0.1879 - 0.1854 = 0.0025\,\text{mol} = 0.40\,\text{g}$

**Percent yield:** If the actual yield of Fe is 18.5 g:

$$
\%\text{yield} = \frac{18.5}{20.7} \times 100\% = 89.4\%
$$

### 8.3 — Titration Curves: Weak Acid + Strong Base (Complete Derivation)

Consider titrating $V_0 = 50.0\,\text{mL}$ of $C_a = 0.100\,\text{M}$ acetic acid ($K_a = 1.8 \times 10^{-5}$) with $C_b = 0.100\,\text{M}$ NaOH.

**The master equation** (charge balance + mass balance + equilibrium):

At any point during the titration, the pH is determined by the fraction of acid neutralized $f = V_b C_b / (V_0 C_a)$:

**Region 1: Before any base added ($f = 0$)**

Weak acid equilibrium:

$$
K_a = \frac{x^2}{C_a - x} \approx \frac{x^2}{C_a}
$$

$$
[\text{H}^+] = x = \sqrt{K_a C_a} = \sqrt{1.8 \times 10^{-5} \times 0.100} = 1.34 \times 10^{-3}
$$

$$
\text{pH} = -\log(1.34 \times 10^{-3}) = 2.87
$$

**Region 2: Buffer region ($0 < f < 1$)**

Henderson-Hasselbalch applies (see [03.5 - Acids, Bases & Equilibrium](03.5---Acids,-Bases-&-Equilibrium)):

$$
\text{pH} = \text{p}K_a + \log\frac{[\text{A}^-]}{[\text{HA}]} = \text{p}K_a + \log\frac{f}{1-f}
$$

At half-equivalence ($f = 0.5$): $\text{pH} = \text{p}K_a = 4.74$

**Region 3: Equivalence point ($f = 1$)**

All HA converted to A⁻. The conjugate base hydrolyzes:

$$
K_b = \frac{K_w}{K_a} = \frac{1.0 \times 10^{-14}}{1.8 \times 10^{-5}} = 5.56 \times 10^{-10}
$$

$$
[\text{OH}^-] = \sqrt{K_b \cdot C_{\text{salt}}} = \sqrt{5.56 \times 10^{-10} \times 0.0500} = 5.27 \times 10^{-6}
$$

$$
\text{pOH} = 5.28, \quad \text{pH} = 8.72
$$

**Key point:** The equivalence pH is NOT 7.00 for a weak acid/strong base titration. It's basic because the conjugate base (acetate) hydrolyzes.

**Region 4: Beyond equivalence ($f > 1$)**

Excess strong base dominates:

$$
[\text{OH}^-] = \frac{(V_b - V_{\text{eq}})C_b}{V_0 + V_b}
$$

**Choosing the indicator:** The indicator must change color at the equivalence pH. For this titration (pH 8.72 at equivalence), use phenolphthalein (range 8.2–10.0). Methyl orange (range 3.1–4.4) would change color too early.

### 8.4 — Gas Law Problems: From Ideal to Real

**The Ideal Gas Law** (a limiting case of statistical mechanics — see [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy)):

$$
PV = nRT
$$

**Derivation from the partition function:**

For $N$ non-interacting particles in volume $V$:

$$
Z_N = \frac{V^N}{N!\lambda^{3N}}, \quad F = -k_BT\ln Z_N
$$

$$
P = -\frac{\partial F}{\partial V}\bigg|_T = \frac{Nk_BT}{V} = \frac{nRT}{V}
$$

The ideal gas law is not an empirical observation — it's a theorem of statistical mechanics for non-interacting particles.

**The van der Waals equation (real gases):**

$$
\left(P + \frac{an^2}{V^2}\right)(V - nb) = nRT
$$

- $a$ = intermolecular attraction parameter (reduces pressure)
- $b$ = excluded volume per mole (molecules have finite size)

**Worked Example — Compressibility of CO₂:**

At $T = 500\,\text{K}$, $P = 100\,\text{atm}$, $n = 1\,\text{mol}$. For CO₂: $a = 3.59\,\text{L}^2\text{atm/mol}^2$, $b = 0.0427\,\text{L/mol}$.

Ideal gas: $V = nRT/P = (1)(0.08206)(500)/100 = 0.410\,\text{L}$

Van der Waals (iterative): Start with $V_0 = 0.410\,\text{L}$:

$$
P = \frac{nRT}{V - nb} - \frac{an^2}{V^2} = \frac{(1)(0.08206)(500)}{0.410 - 0.0427} - \frac{3.59}{0.410^2} = 111.7 - 21.4 = 90.3\,\text{atm}
$$

This gives only 90.3 atm, not 100. Iterate with smaller $V$ until convergence → $V \approx 0.366\,\text{L}$.

**Compressibility factor:** $Z = PV/(nRT) = 100 \times 0.366/(1 \times 0.08206 \times 500) = 0.892$

$Z < 1$ means attractive forces dominate (molecules are closer together than ideal). $Z > 1$ means repulsive forces dominate (at very high pressures).

### 8.5 — Dimensional Analysis as a Formal Problem-Solving Tool

Dimensional analysis is not just "checking units" — it's a systematic method for solving problems even when you don't remember the formula.

**The Buckingham Pi Theorem:** Any physically meaningful equation involving $n$ variables with $k$ independent dimensions can be rewritten in terms of $n - k$ dimensionless groups.

**Application to chemistry — deriving the ideal gas law from dimensions:**

Variables: $P$ [force/area = ML⁻¹T⁻²], $V$ [L³], $n$ [mol], $T$ [Θ], $R$ [ML²T⁻²Θ⁻¹mol⁻¹]

5 variables, 5 dimensions (M, L, T, Θ, mol) → but $R$ contains all dimensions, so we get 1 dimensionless group:

$$
\Pi = \frac{PV}{nRT}
$$

For an ideal gas, $\Pi = 1$. The compressibility factor $Z = PV/(nRT)$ measures deviation from ideality.

**Practical dimensional analysis for unit conversions:**

**Problem:** Convert 2.50 atm to pascals.

$$
2.50\,\text{atm} \times \frac{101325\,\text{Pa}}{1\,\text{atm}} = 253313\,\text{Pa} = 253\,\text{kPa}
$$

**Problem:** How many molecules in 5.00 g of glucose (C₆H₁₂O₆)?

$$
5.00\,\text{g} \times \frac{1\,\text{mol}}{180.16\,\text{g}} \times \frac{6.022 \times 10^{23}\,\text{molecules}}{1\,\text{mol}} = 1.67 \times 10^{22}\,\text{molecules}
$$

**The "railroad tracks" method:** Write conversion factors as fractions with units that cancel. Every step must have units that make dimensional sense. If your answer has wrong units, your calculation is wrong — guaranteed.

### 8.6 — Significant Figures: The Rules and Why They Exist

**The rules:**

1. **Multiplication/division:** Result has the same number of sig figs as the input with FEWEST sig figs.
2. **Addition/subtraction:** Result has the same number of DECIMAL PLACES as the input with fewest decimal places.
3. **Exact numbers** (counting, defined conversions) have infinite sig figs.
4. **Logarithms:** The number of decimal places in the log equals the number of sig figs in the original number. (pH 4.74 has 2 sig figs in the concentration: $[\text{H}^+] = 1.8 \times 10^{-5}$)

**Why sig figs matter in lab calculations:**

If you weigh 2.504 g on a balance (±0.001 g), your mass has 4 sig figs. If you dissolve it in 100 mL from a graduated cylinder (±1 mL), your volume has 3 sig figs. Your concentration:

$$
C = \frac{2.504\,\text{g}}{100\,\text{mL}} = 0.0250\,\text{g/mL} \quad \text{(3 sig figs)}
$$

NOT 0.02504 — that implies precision you don't have.

**Propagation of uncertainty (the rigorous version):**

For $f(x, y, z, \ldots)$:

$$
\sigma_f = \sqrt{\left(\frac{\partial f}{\partial x}\right)^2\sigma_x^2 + \left(\frac{\partial f}{\partial y}\right)^2\sigma_y^2 + \left(\frac{\partial f}{\partial z}\right)^2\sigma_z^2 + \cdots}
$$

For multiplication: $\sigma_f/f = \sqrt{(\sigma_x/x)^2 + (\sigma_y/y)^2}$ (relative errors add in quadrature).

## 📎 9. Appendix — Deep Dives & Mastery Challenges

### Appendix A — Balancing as Linear Algebra

Chemical equation balancing is a system of linear equations — exactly the row reduction from [2.3 - Systems of Linear Equations & Row Reduction](2.3---Systems-of-Linear-Equations-&-Row-Reduction).

**Example:** Balance $a\text{C}_3\text{H}_8 + b\text{O}_2 \to c\text{CO}_2 + d\text{H}_2\text{O}$

Set up atom-balance equations:
- C: $3a = c$
- H: $8a = 2d$
- O: $2b = 2c + d$

Three equations, four unknowns → one free parameter. Set $a = 1$:
- $c = 3$
- $d = 4$
- $2b = 6 + 4 = 10 \Rightarrow b = 5$

**Result:** $\text{C}_3\text{H}_8 + 5\text{O}_2 \to 3\text{CO}_2 + 4\text{H}_2\text{O}$

**For complex reactions**, the matrix method is essential:

$$
\begin{pmatrix} 3 & 0 & -1 & 0 \\ 8 & 0 & 0 & -2 \\ 0 & 2 & -2 & -1 \end{pmatrix} \begin{pmatrix} a \\ b \\ c \\ d \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \\ 0 \end{pmatrix}
$$

Row reduce to find the null space → the balancing coefficients.

```python
import numpy as np
from scipy.linalg import null_space

# Balance: a*C3H8 + b*O2 -> c*CO2 + d*H2O
# Atom matrix: rows = elements (C, H, O), columns = species
# Convention: reactants positive, products negative
atom_matrix = np.array([
    [3, 0, -1, 0],   # Carbon
    [8, 0, 0, -2],   # Hydrogen
    [0, 2, -2, -1],  # Oxygen
], dtype=float)

# Find null space
ns = null_space(atom_matrix)
# Normalize to smallest integers
coeffs = ns[:, 0]
coeffs = coeffs / min(abs(coeffs[coeffs != 0]))
# Round to integers
coeffs = np.round(coeffs).astype(int)
print(f"Balanced: {coeffs[0]}C3H8 + {coeffs[1]}O2 -> {coeffs[2]}CO2 + {coeffs[3]}H2O")

# More complex example: balance permanganate + oxalate in acid
# a*MnO4- + b*C2O4^2- + c*H+ -> d*Mn2+ + e*CO2 + f*H2O
atom_matrix2 = np.array([
    [1, 0, 0, -1, 0, 0],   # Mn
    [4, 4, 0, 0, -2, -1],  # O
    [0, 2, 0, 0, -1, 0],   # C
    [0, 0, 1, 0, 0, -2],   # H
    [-1, -2, 1, 2, 0, 0],  # Charge
], dtype=float)

ns2 = null_space(atom_matrix2)
coeffs2 = ns2[:, 0]
coeffs2 = coeffs2 / min(abs(coeffs2[coeffs2 != 0]))
coeffs2 = np.abs(np.round(coeffs2)).astype(int)
print(f"Balanced: {coeffs2[0]}MnO4- + {coeffs2[1]}C2O4^2- + {coeffs2[2]}H+ -> "
      f"{coeffs2[3]}Mn2+ + {coeffs2[4]}CO2 + {coeffs2[5]}H2O")
```

### Appendix B — Titration Curves for Polyprotic Acids

Polyprotic acids (H₂SO₄, H₃PO₄, H₂CO₃) have multiple equivalence points. Each deprotonation has its own $K_a$.

**Phosphoric acid (H₃PO₄):** $K_{a1} = 7.5 \times 10^{-3}$, $K_{a2} = 6.2 \times 10^{-8}$, $K_{a3} = 4.8 \times 10^{-13}$

**Key points on the titration curve:**

| Point | $f$ (fraction neutralized) | pH | Species present |
|---|---|---|---|
| Start | 0 | 1.6 | H₃PO₄ dominant |
| 1st half-equiv | 0.5 | $\text{p}K_{a1} = 2.12$ | H₃PO₄ = H₂PO₄⁻ |
| 1st equiv | 1.0 | $\frac{\text{p}K_{a1} + \text{p}K_{a2}}{2} = 4.67$ | H₂PO₄⁻ dominant |
| 2nd half-equiv | 1.5 | $\text{p}K_{a2} = 7.21$ | H₂PO₄⁻ = HPO₄²⁻ |
| 2nd equiv | 2.0 | $\frac{\text{p}K_{a2} + \text{p}K_{a3}}{2} = 9.77$ | HPO₄²⁻ dominant |
| 3rd half-equiv | 2.5 | $\text{p}K_{a3} = 12.32$ | HPO₄²⁻ = PO₄³⁻ |
| 3rd equiv | 3.0 | ~12.5 | PO₄³⁻ dominant |

**The isoelectric point formula:** At an equivalence point for an amphoteric species (like H₂PO₄⁻):

$$
\text{pH} = \frac{\text{p}K_{a1} + \text{p}K_{a2}}{2}
$$

This is exact when $K_{a1} \gg K_w/C$ and $K_{a2} \ll C$ (usually satisfied for reasonable concentrations).

**Practical application — blood buffer:** The H₂CO₃/HCO₃⁻ system buffers blood at pH 7.4. Since $\text{p}K_{a1}(\text{H}_2\text{CO}_3) = 6.35$:

$$
\text{pH} = 6.35 + \log\frac{[\text{HCO}_3^-]}{[\text{H}_2\text{CO}_3]} = 6.35 + \log\frac{24\,\text{mM}}{1.2\,\text{mM}} = 6.35 + 1.30 = 7.65
$$

(The actual blood pH of 7.4 accounts for the open system — CO₂ is exhaled, shifting equilibrium. See [03.5 - Acids, Bases & Equilibrium](03.5---Acids,-Bases-&-Equilibrium) and [02 - Biology](02---Biology) for the full physiological picture.)

### Appendix C — Gas Law Derivations and Special Cases

**Dalton's Law from the partition function:**

For a mixture of ideal gases, the total partition function factorizes:

$$
Z_{\text{total}} = Z_A \cdot Z_B \cdot Z_C \cdots
$$

Since $P = k_BT(\partial\ln Z/\partial V)_T$, and $\ln Z_{\text{total}} = \ln Z_A + \ln Z_B + \cdots$:

$$
P_{\text{total}} = P_A + P_B + P_C + \cdots
$$

Each partial pressure $P_i = n_i RT/V$ — Dalton's Law emerges from statistical independence of non-interacting species.

**Graham's Law of Effusion:**

Rate of effusion $\propto$ average molecular speed $\propto 1/\sqrt{M}$:

$$
\frac{\text{Rate}_1}{\text{Rate}_2} = \sqrt{\frac{M_2}{M_1}}
$$

**Derivation from Maxwell-Boltzmann** (cross-link [5.7 - Maxwell-Boltzmann Distribution & Kinetic Theory](5.7---Maxwell-Boltzmann-Distribution-&-Kinetic-Theory)):

The flux of molecules hitting a wall (effusion rate) is:

$$
\Phi = \frac{n\langle v\rangle}{4} = \frac{n}{4}\sqrt{\frac{8k_BT}{\pi m}}
$$

For two gases at the same $T$ and $P$ (same $n$):

$$
\frac{\Phi_1}{\Phi_2} = \frac{\sqrt{1/m_1}}{\sqrt{1/m_2}} = \sqrt{\frac{m_2}{m_1}} = \sqrt{\frac{M_2}{M_1}}
$$

**Application — Uranium enrichment:** UF₆ with ²³⁵U effuses faster than UF₆ with ²³⁸U:

$$
\frac{\text{Rate}(^{235}\text{UF}_6)}{\text{Rate}(^{238}\text{UF}_6)} = \sqrt{\frac{352}{349}} = 1.0043
$$

Only 0.43% enrichment per stage — thousands of stages needed for weapons-grade uranium. This is why nuclear proliferation is hard.

### Appendix D — Reaction Types: A Complete Classification

| Type | Definition | Example | Driving Force |
|---|---|---|---|
| Combination | A + B → AB | 2Mg + O₂ → 2MgO | Bond formation (ΔH < 0) |
| Decomposition | AB → A + B | 2H₂O₂ → 2H₂O + O₂ | Entropy increase (ΔS > 0) |
| Single replacement | A + BC → AC + B | Zn + CuSO₄ → ZnSO₄ + Cu | Activity series (ΔG < 0) |
| Double replacement | AB + CD → AD + CB | AgNO₃ + NaCl → AgCl↓ + NaNO₃ | Precipitate/gas/water formation |
| Combustion | Fuel + O₂ → CO₂ + H₂O | CH₄ + 2O₂ → CO₂ + 2H₂O | Large negative ΔG |
| Acid-base | HA + BOH → BA + H₂O | HCl + NaOH → NaCl + H₂O | Water formation (K = 10¹⁴) |
| Redox | Electron transfer | 2Fe + 3Cl₂ → 2FeCl₃ | Electronegativity difference |

**The thermodynamic unification:** ALL reactions proceed because $\Delta G < 0$. The "driving forces" listed above are just common ways that $\Delta G$ becomes negative (see [03.4 - Thermodynamics & Kinetics](03.4---Thermodynamics-&-Kinetics)).

> [!danger] 🧠 Common Misconceptions — Section 8 & 9 Summary
> 
> **❌ "Balancing equations is just trial and error"**
> **Truth:** Balancing is solving a system of linear equations. The half-reaction method for redox is an algorithm — follow the steps and you'll always get the right answer. No guessing required.
> 
> **❌ "The limiting reagent is whichever you have less of"**
> **Truth:** The limiting reagent is whichever runs out first GIVEN THE STOICHIOMETRY. 10 mol of A can be limiting even if you only have 1 mol of B, if the equation requires 20 mol of A per mol of B.
> 
> **❌ "At the equivalence point, pH = 7"**
> **Truth:** pH = 7 at equivalence ONLY for strong acid + strong base. For weak acid + strong base, pH > 7 (conjugate base hydrolyzes). For strong acid + weak base, pH < 7. The equivalence point is where moles of acid = moles of base, NOT where pH is neutral.
> 
> **❌ "The ideal gas law always works"**
> **Truth:** It fails at high pressure (molecules have volume) and low temperature (intermolecular attractions matter). The compressibility factor Z = PV/(nRT) quantifies the deviation. For CO₂ at 100 atm, Z ≈ 0.2 — the ideal gas law is off by 80%.
> 
> **❌ "Significant figures are just about counting digits"**
> **Truth:** Sig figs encode measurement uncertainty. They're a simplified version of error propagation. In research, you'd use full uncertainty analysis (standard deviations, confidence intervals). Sig figs are the minimum acceptable treatment.
> 
> **❌ "You need to memorize all reaction types"**
> **Truth:** All reactions are driven by ΔG < 0. If you understand thermodynamics (Chapter 03.4), you can PREDICT whether a reaction occurs without memorizing categories. The categories are just patterns humans noticed — the underlying physics is always free energy minimization.

---

*Previous: [03.2 - Chemical Bonding - Ionic, Covalent, Metallic & Intermolecular](03.2---Chemical-Bonding---Ionic,-Covalent,-Metallic-&-Intermolecular) | Next: [03.4 - Thermodynamics & Kinetics](03.4---Thermodynamics-&-Kinetics)*
