---
title: "03.4 — Thermodynamics & Kinetics"
subject: "Chemistry"
catalog: advanced
audience_tier: higher-education
chapter: "03.4"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 03.4 — Thermodynamics & Kinetics

> *"The law that entropy always increases holds, I think, the supreme position among the laws of Nature."* — Arthur Eddington

> *"The rate of a chemical reaction doubles for every 10°C rise in temperature."* — Approximate rule of thumb (derived from Arrhenius)

You already derived $F = -k_BT\ln Z$ in [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy). You proved the equipartition theorem. You computed heat capacities from partition functions. Now we apply all of that to **chemical reactions**: Will a reaction happen spontaneously? How fast will it go? These are the two fundamental questions of physical chemistry.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Calculate $\Delta H$, $\Delta S$, and $\Delta G$ for chemical reactions using Hess's law and standard formation data.
2. Derive the Arrhenius equation $k = Ae^{-E_a/(RT)}$ from the Boltzmann distribution.
3. Determine reaction order from experimental rate data.
4. Connect $\Delta G^\circ$ to the equilibrium constant: $\Delta G^\circ = -RT\ln K$.
5. Apply transition state theory to predict rate constants.
6. Explain catalysis (homogeneous, heterogeneous, enzymatic) in terms of activation energy lowering.
7. Derive the van't Hoff equation for temperature dependence of $K$.

---

## 🖼️ Visual Anchor — Energy Landscape of a Chemical Reaction

![chem-03__fig2](chem-03__fig2.svg)

---

## 📚 1. Definitions

### Definition 03.4.1 — Enthalpy ($H$)

$$
H = U + PV
$$

At constant pressure: $\Delta H = q_P$ (heat absorbed at constant pressure).

- $\Delta H < 0$: exothermic (releases heat)
- $\Delta H > 0$: endothermic (absorbs heat)

### Definition 03.4.2 — Entropy ($S$)

$$
S = k_B \ln \Omega
$$

where $\Omega$ is the number of microstates. You derived this in [5.5 - Classical Statistical Mechanics - Microstates & Ensembles](5.5---Classical-Statistical-Mechanics---Microstates-&-Ensembles).

For a reversible process: $dS = \frac{\delta q_{\text{rev}}}{T}$.

### Definition 03.4.3 — Gibbs Free Energy ($G$)

$$
G = H - TS
$$

At constant $T$ and $P$: $\Delta G = \Delta H - T\Delta S$.

- $\Delta G < 0$: spontaneous (thermodynamically favorable)
- $\Delta G = 0$: equilibrium
- $\Delta G > 0$: non-spontaneous

### Definition 03.4.4 — Standard Enthalpy of Formation ($\Delta H_f^\circ$)

The enthalpy change when 1 mole of a compound is formed from its elements in their standard states (25°C, 1 atm).

By convention: $\Delta H_f^\circ(\text{element in standard state}) = 0$.

### Definition 03.4.5 — Rate Law

$$
\text{rate} = k[A]^m[B]^n
$$

where $k$ is the rate constant, $m$ and $n$ are the reaction orders (determined experimentally, NOT from stoichiometry).

### Definition 03.4.6 — Activation Energy ($E_a$)

The minimum energy required for reactants to reach the transition state and proceed to products.

### Definition 03.4.7 — Catalyst

A substance that increases reaction rate by providing an alternative pathway with lower $E_a$, without being consumed in the overall reaction.

---

## 📐 2. Mathematical Foundations

### 2.1 Hess's Law (Enthalpy is a State Function)

$$
\Delta H_{\text{rxn}}^\circ = \sum \Delta H_f^\circ(\text{products}) - \sum \Delta H_f^\circ(\text{reactants})
$$

This works because enthalpy is a state function — path-independent. You proved this thermodynamically in Track 05.

### 2.2 The Gibbs-Helmholtz Equation

$$
\Delta G^\circ = \Delta H^\circ - T\Delta S^\circ
$$

**The statistical mechanics derivation** (from [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy)):

For a reaction A → B, the ratio of populations at equilibrium is:

$$
\frac{N_B}{N_A} = \frac{Z_B}{Z_A} = \frac{q_B}{q_A}e^{-\Delta\epsilon_0/(k_BT)}
$$

where $q$ are molecular partition functions and $\Delta\epsilon_0$ is the zero-point energy difference. Taking the log:

$$
\ln K = \ln\frac{q_B}{q_A} - \frac{\Delta\epsilon_0}{k_BT}
$$

The first term relates to $\Delta S^\circ$ (entropy from accessible states) and the second to $\Delta H^\circ$ (energy difference). This gives:

$$
\Delta G^\circ = -RT\ln K
$$

### 2.3 Deriving the Arrhenius Equation from the Boltzmann Distribution

The fraction of molecules with kinetic energy $\geq E_a$ (from the Maxwell-Boltzmann distribution you derived in [5.7 - Maxwell-Boltzmann Distribution & Kinetic Theory](5.7---Maxwell-Boltzmann-Distribution-&-Kinetic-Theory)):

$$
f(E \geq E_a) = e^{-E_a/(k_BT)}
$$

The rate constant is proportional to this fraction times a frequency factor $A$ (collision frequency × orientation factor):

$$
\boxed{k = A\,e^{-E_a/(RT)}}
$$

**Taking the logarithm:**

$$
\ln k = \ln A - \frac{E_a}{RT}
$$

Plot $\ln k$ vs $1/T$ → straight line with slope $= -E_a/R$ (Arrhenius plot).

### 2.4 Integrated Rate Laws

| Order | Rate Law | Integrated Form | Half-life | Linear Plot |
|---|---|---|---|---|
| 0 | $-d[A]/dt = k$ | $[A] = [A]_0 - kt$ | $t_{1/2} = [A]_0/(2k)$ | $[A]$ vs $t$ |
| 1 | $-d[A]/dt = k[A]$ | $\ln[A] = \ln[A]_0 - kt$ | $t_{1/2} = \ln 2/k$ | $\ln[A]$ vs $t$ |
| 2 | $-d[A]/dt = k[A]^2$ | $1/[A] = 1/[A]_0 + kt$ | $t_{1/2} = 1/(k[A]_0)$ | $1/[A]$ vs $t$ |

These are ODEs you can solve from [3.1 - First-Order ODEs & Separation of Variables](3.1---First-Order-ODEs-&-Separation-of-Variables).

### 2.5 Transition State Theory (Eyring Equation)

$$
k = \frac{k_BT}{h}\,e^{-\Delta G^\ddagger/(RT)} = \frac{k_BT}{h}\,e^{\Delta S^\ddagger/R}\,e^{-\Delta H^\ddagger/(RT)}
$$

where $\Delta G^\ddagger$, $\Delta H^\ddagger$, $\Delta S^\ddagger$ are the activation free energy, enthalpy, and entropy (properties of the transition state).

### 2.6 The van't Hoff Equation

$$
\frac{d\ln K}{dT} = \frac{\Delta H^\circ}{RT^2}
$$

Integrated (assuming $\Delta H^\circ$ is temperature-independent):

$$
\ln\frac{K_2}{K_1} = -\frac{\Delta H^\circ}{R}\left(\frac{1}{T_2} - \frac{1}{T_1}\right)
$$

---

## 🔬 3. Chemical Mechanisms

### 3.1 Reaction Coordinate Diagrams

The **reaction coordinate** traces the minimum-energy path from reactants to products through the transition state (saddle point on the potential energy surface).

- **Exothermic:** Products lower than reactants; $\Delta H < 0$
- **Endothermic:** Products higher than reactants; $\Delta H > 0$
- **Activation energy:** Height of the barrier above reactants

### 3.2 Multi-Step Reactions and the Rate-Determining Step

For a mechanism with multiple elementary steps, the overall rate is determined by the **slowest step** (rate-determining step, RDS).

**Example:** $\text{NO}_2 + \text{CO} \to \text{NO} + \text{CO}_2$ (observed rate = $k[\text{NO}_2]^2$)

Mechanism:
1. $2\text{NO}_2 \to \text{NO}_3 + \text{NO}$ (slow — RDS)
2. $\text{NO}_3 + \text{CO} \to \text{NO}_2 + \text{CO}_2$ (fast)

The rate law matches Step 1, confirming it as the RDS.

### 3.3 Catalysis Mechanisms

**Homogeneous catalysis:** Catalyst in same phase as reactants (e.g., acid catalysis in solution).

**Heterogeneous catalysis:** Catalyst in different phase (e.g., Pt surface for catalytic converter):
1. Adsorption of reactants onto surface
2. Reaction on surface (lower $E_a$ due to weakened bonds)
3. Desorption of products

**Enzymatic catalysis:** Biological catalysts that achieve enormous rate enhancements ($10^6$–$10^{17}$) through:
- Proximity and orientation effects
- Transition state stabilization
- Acid-base catalysis
- Covalent catalysis

---

## ✍️ 4. Worked Examples

### Example 03.4.1 — Calculating $\Delta G^\circ$ and Predicting Spontaneity

**Problem:** For the reaction $\text{N}_2\text{O}_4(g) \rightleftharpoons 2\text{NO}_2(g)$ at 25°C:
- $\Delta H^\circ = +57.2$ kJ/mol
- $\Delta S^\circ = +175.8$ J/(mol·K)

Is this reaction spontaneous at 25°C? At what temperature does it become spontaneous?

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Calculate $\Delta G^\circ$ at 25°C (298 K).

$$
\Delta G^\circ = \Delta H^\circ - T\Delta S^\circ = 57200 - 298(175.8) = 57200 - 52388 = +4812 \text{ J/mol}
$$

$$
\Delta G^\circ = +4.8 \text{ kJ/mol} \gt  0
$$

**Not spontaneous** at 25°C (but barely — close to equilibrium).

**Step 2:** Find the crossover temperature where $\Delta G^\circ = 0$.

$$
0 = \Delta H^\circ - T_{\text{cross}}\Delta S^\circ
$$

$$
T_{\text{cross}} = \frac{\Delta H^\circ}{\Delta S^\circ} = \frac{57200}{175.8} = 325 \text{ K} = 52°\text{C}
$$

**Step 3:** Interpretation.

Above 52°C: $\Delta G^\circ \lt  0$ → spontaneous (entropy wins).
Below 52°C: $\Delta G^\circ \gt  0$ → non-spontaneous (enthalpy wins).

This is an **entropy-driven** reaction: the positive $\Delta S$ (1 molecule → 2 molecules, more disorder) eventually overcomes the positive $\Delta H$ (endothermic) at high enough temperature.

**Physical insight from stat mech:** At higher $T$, the $T\Delta S$ term dominates because more microstates become thermally accessible. The partition function ratio $Z_{\text{products}}/Z_{\text{reactants}}$ increases with $T$ when products have more degrees of freedom.

</details>

---

### Example 03.4.2 — Arrhenius Equation: Determining Activation Energy

**Problem:** A reaction has rate constants $k_1 = 0.0521$ s⁻¹ at 25°C and $k_2 = 0.421$ s⁻¹ at 50°C. Calculate $E_a$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Use the two-point Arrhenius equation.

$$
\ln\frac{k_2}{k_1} = \frac{E_a}{R}\left(\frac{1}{T_1} - \frac{1}{T_2}\right)
$$

**Step 2:** Substitute values ($T_1 = 298$ K, $T_2 = 323$ K).

$$
\ln\frac{0.421}{0.0521} = \frac{E_a}{8.314}\left(\frac{1}{298} - \frac{1}{323}\right)
$$

$$
\ln(8.08) = \frac{E_a}{8.314}\left(3.356 \times 10^{-3} - 3.096 \times 10^{-3}\right)
$$

$$
2.089 = \frac{E_a}{8.314}(2.60 \times 10^{-4})
$$

**Step 3:** Solve for $E_a$.

$$
E_a = \frac{2.089 \times 8.314}{2.60 \times 10^{-4}} = 66,800 \text{ J/mol} = 66.8 \text{ kJ/mol}
$$

**Interpretation:** This is a typical activation energy for a reaction that proceeds at moderate rates near room temperature. The Boltzmann factor $e^{-E_a/(RT)}$ at 298 K is $e^{-66800/(8.314 \times 298)} = e^{-27.0} = 1.9 \times 10^{-12}$ — only about 1 in $10^{12}$ collisions has enough energy to react.

</details>

---

### Example 03.4.3 — Determining Reaction Order from Data

**Problem:** Given the following data for $A \to$ products, determine the reaction order and rate constant.

| Time (s) | [A] (M) |
|---|---|
| 0 | 1.000 |
| 100 | 0.500 |
| 200 | 0.333 |
| 300 | 0.250 |

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Test for zero order: plot $[A]$ vs $t$. Not linear (0.500, 0.333, 0.250 are not equally spaced).

**Step 2:** Test for first order: plot $\ln[A]$ vs $t$.
- $\ln(1.000) = 0$
- $\ln(0.500) = -0.693$
- $\ln(0.333) = -1.099$
- $\ln(0.250) = -1.386$

Differences: $-0.693, -0.406, -0.287$ — not constant. Not first order.

**Step 3:** Test for second order: plot $1/[A]$ vs $t$.
- $1/1.000 = 1.000$
- $1/0.500 = 2.000$
- $1/0.333 = 3.003$
- $1/0.250 = 4.000$

Differences: $1.000, 1.003, 0.997$ — constant! ✓

**Step 4:** **Second order.** Rate law: $-d[A]/dt = k[A]^2$.

Slope of $1/[A]$ vs $t$ = $k$:

$$
k = \frac{4.000 - 1.000}{300 - 0} = 0.0100 \text{ M}^{-1}\text{s}^{-1}
$$

**Step 5:** Verify half-life: $t_{1/2} = 1/(k[A]_0) = 1/(0.01 \times 1.0) = 100$ s. ✓ (concentration halves at $t = 100$ s).

</details>

---

## 🧠 5. Connections to Other Tracks

| This Chapter | Connects To | How |
|---|---|---|
| $\Delta G = -RT\ln K$ | [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy) | $F = -k_BT\ln Z$ applied to reaction equilibrium |
| Arrhenius equation | [5.7 - Maxwell-Boltzmann Distribution & Kinetic Theory](5.7---Maxwell-Boltzmann-Distribution-&-Kinetic-Theory) | Fraction with $E > E_a$ from Boltzmann |
| Integrated rate laws | [3.1 - First-Order ODEs & Separation of Variables](3.1---First-Order-ODEs-&-Separation-of-Variables) | Rate equations are ODEs |
| Transition state theory | [9.4 - Angular Momentum, Spin & Fine Structure](9.4---Angular-Momentum,-Spin-&-Fine-Structure) | Quantum tunneling through barriers |
| Entropy | [5.5 - Classical Statistical Mechanics - Microstates & Ensembles](5.5---Classical-Statistical-Mechanics---Microstates-&-Ensembles) | $S = k_B\ln\Omega$ |
| Catalysis | [03.8 - Biochemistry & Modern Topics](03.8---Biochemistry-&-Modern-Topics) | Enzyme kinetics, drug design |

---

## ⚠️ 6. Common Misconceptions & Where Most Students Fail

### ❌ Misconception 1: "Exothermic reactions are always spontaneous"

**The truth:** Spontaneity is determined by $\Delta G = \Delta H - T\Delta S$, NOT by $\Delta H$ alone. An exothermic reaction with a large negative $\Delta S$ can be non-spontaneous at high $T$. Example: $3\text{O}_2 \to 2\text{O}_3$ is exothermic but non-spontaneous because $\Delta S < 0$ (fewer molecules).

### ❌ Misconception 2: "Thermodynamics tells you how fast a reaction goes"

**The truth:** Thermodynamics tells you IF a reaction CAN happen ($\Delta G < 0$). Kinetics tells you how FAST. Diamond → graphite is thermodynamically favorable ($\Delta G < 0$) but kinetically so slow it never happens at room temperature. These are independent questions.

### ❌ Misconception 3: "A catalyst changes the equilibrium"

**The truth:** A catalyst speeds up BOTH forward and reverse reactions equally. It lowers $E_a$ for both directions by the same amount. The equilibrium constant $K$ is unchanged — you just reach equilibrium faster.

### ❌ Misconception 4: "Reaction order equals stoichiometric coefficient"

**The truth:** Reaction order is determined EXPERIMENTALLY. It equals the stoichiometric coefficient ONLY for elementary (single-step) reactions. For multi-step mechanisms, the overall rate law depends on the mechanism, not the balanced equation.

### ❌ Misconception 5: "Entropy always increases in a reaction"

**The truth:** The TOTAL entropy (system + surroundings) always increases for a spontaneous process. But the system's entropy can decrease if the surroundings' entropy increases more (exothermic reaction dumps heat into surroundings). This is captured by $\Delta G < 0$ at constant $T, P$.

### 💪 The Pep Talk

Chemical thermodynamics is where most students hit a wall — too many variables ($H$, $S$, $G$, $A$, $U$), too many sign conventions, too many "rules." But you have an unfair advantage: you already derived ALL of this from statistical mechanics. You KNOW that $F = -k_BT\ln Z$. You KNOW that entropy counts microstates. You KNOW the Boltzmann distribution.

Chemical thermodynamics is just Track 05 applied to molecules. The notation changes ($G$ instead of $F$ because chemists work at constant $P$, not constant $V$), but the physics is identical. You've already done the hard part.

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy) — The statistical mechanics foundation
- [5.7 - Maxwell-Boltzmann Distribution & Kinetic Theory](5.7---Maxwell-Boltzmann-Distribution-&-Kinetic-Theory) — Boltzmann → Arrhenius
- [5.3 - Thermodynamic Potentials & Maxwell Relations](5.3---Thermodynamic-Potentials-&-Maxwell-Relations) — $G$, $H$, $S$ relationships
- [3.1 - First-Order ODEs & Separation of Variables](3.1---First-Order-ODEs-&-Separation-of-Variables) — Solving rate equations
- [03.5 - Acids, Bases & Equilibrium](03.5---Acids,-Bases-&-Equilibrium) — Equilibrium applications

### External References
- **MIT 5.111 OCW** — Lectures 16–20: Thermochemistry and kinetics
- **Khan Academy** — [Thermodynamics](https://www.khanacademy.org/science/chemistry/thermodynamics-chemistry) and [Kinetics](https://www.khanacademy.org/science/chemistry/chem-kinetics)
- **Crash Course Chemistry** — Episodes 15–17: Energy, enthalpy, entropy
- **Atkins, P.** — *Physical Chemistry*, Chapters 2–3 (thermodynamics), Chapter 20 (kinetics)

---

## 🔬 8. Advanced Derivations — From Statistical Mechanics to Chemical Kinetics

### 8.1 — The Complete ΔG Derivation: Why Reactions Happen

The Gibbs free energy $G$ is the master criterion for spontaneity at constant $T$ and $P$. Here we derive $\Delta G = \Delta H - T\Delta S$ from the second law of thermodynamics.

**Starting point — the second law:**

For any spontaneous process in an isolated system:

$$
\Delta S_{\text{universe}} = \Delta S_{\text{system}} + \Delta S_{\text{surroundings}} > 0
$$

**For the surroundings** (a thermal reservoir at constant $T$):

$$
\Delta S_{\text{surr}} = -\frac{q_{\text{sys}}}{T}
$$

At constant pressure, $q_{\text{sys}} = \Delta H_{\text{sys}}$, so:

$$
\Delta S_{\text{surr}} = -\frac{\Delta H_{\text{sys}}}{T}
$$

**Substituting into the second law:**

$$
\Delta S_{\text{sys}} - \frac{\Delta H_{\text{sys}}}{T} > 0
$$

Multiply by $-T$ (flips inequality):

$$
\Delta H_{\text{sys}} - T\Delta S_{\text{sys}} < 0
$$

**Define:** $\Delta G \equiv \Delta H - T\Delta S$. Then spontaneity requires $\Delta G < 0$.

**The four thermodynamic scenarios:**

| $\Delta H$ | $\Delta S$ | $\Delta G$ | Spontaneous? |
|---|---|---|---|
| $-$ (exothermic) | $+$ (disorder increases) | Always $-$ | Always spontaneous |
| $-$ (exothermic) | $-$ (disorder decreases) | Depends on $T$ | Spontaneous at low $T$ |
| $+$ (endothermic) | $+$ (disorder increases) | Depends on $T$ | Spontaneous at high $T$ |
| $+$ (endothermic) | $-$ (disorder decreases) | Always $+$ | Never spontaneous |

**The crossover temperature:** When $\Delta G = 0$:

$$
T_{\text{crossover}} = \frac{\Delta H}{\Delta S}
$$

**Example — CaCO₃ decomposition:** $\Delta H = +178\,\text{kJ/mol}$, $\Delta S = +161\,\text{J/(mol·K)}$:

$$
T_{\text{crossover}} = \frac{178000}{161} = 1106\,\text{K} = 833°\text{C}
$$

Below 833°C: limestone is stable. Above 833°C: it decomposes to CaO + CO₂. This is why lime kilns operate at ~900°C.

### 8.2 — Equilibrium Constant from the Partition Function

This is the deepest connection between statistical mechanics and chemistry. We derive $K$ from [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy).

**For the reaction** $\nu_A A + \nu_B B \rightleftharpoons \nu_C C + \nu_D D$:

The standard Gibbs free energy of reaction:

$$
\Delta G^\circ = -RT\ln K
$$

**From statistical mechanics**, the chemical potential of species $i$ is:

$$
\mu_i = -k_BT\ln\frac{q_i}{N_i}
$$

where $q_i$ is the molecular partition function of species $i$.

**At equilibrium**, $\sum_i \nu_i \mu_i = 0$, which gives:

$$
K = \prod_i \left(\frac{q_i^\circ}{N_A}\right)^{\nu_i} = \frac{(q_C^\circ/N_A)^{\nu_C}(q_D^\circ/N_A)^{\nu_D}}{(q_A^\circ/N_A)^{\nu_A}(q_B^\circ/N_A)^{\nu_B}}
$$

where $q_i^\circ$ is the partition function evaluated at standard conditions (1 bar).

**The molecular partition function** factorizes:

$$
q = q_{\text{trans}} \cdot q_{\text{rot}} \cdot q_{\text{vib}} \cdot q_{\text{elec}}
$$

- $q_{\text{trans}} = V\left(\frac{2\pi mk_BT}{h^2}\right)^{3/2}$ — translational (from [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy))
- $q_{\text{rot}} = \frac{8\pi^2 I k_BT}{\sigma h^2}$ — rotational (linear molecule; $\sigma$ = symmetry number)
- $q_{\text{vib}} = \prod_k \frac{1}{1 - e^{-h\nu_k/(k_BT)}}$ — vibrational (product over normal modes)
- $q_{\text{elec}} = g_0 e^{-\epsilon_0/(k_BT)} + g_1 e^{-\epsilon_1/(k_BT)} + \cdots$ — electronic (usually just ground state)

**Worked Example — H₂ dissociation equilibrium:**

$$
\text{H}_2 \rightleftharpoons 2\text{H}
$$

$$
K(T) = \frac{(q_H^\circ/N_A)^2}{q_{H_2}^\circ/N_A} = \frac{q_H^2}{N_A \cdot q_{H_2}} \cdot \frac{1}{V^\circ}
$$

At $T = 3000\,\text{K}$: $K \approx 10^{-4}$ (mostly undissociated). At $T = 6000\,\text{K}$: $K \approx 10$ (mostly dissociated). The partition function approach gives quantitative predictions of equilibrium from molecular properties alone — no experimental data needed.

### 8.3 — The Arrhenius Equation from the Boltzmann Distribution

**Empirical Arrhenius equation:**

$$
k(T) = A\,e^{-E_a/(RT)}
$$

**Derivation from the Boltzmann distribution:**

For a reaction to occur, molecules must collide with energy $\geq E_a$ (the activation energy). From the Maxwell-Boltzmann distribution ([5.7 - Maxwell-Boltzmann Distribution & Kinetic Theory](5.7---Maxwell-Boltzmann-Distribution-&-Kinetic-Theory)), the fraction of molecules with kinetic energy $\geq E_a$:

$$
f(E \geq E_a) = e^{-E_a/(k_BT)}
$$

The rate constant is proportional to:
1. Collision frequency $Z$ (how often molecules meet)
2. Energy requirement $e^{-E_a/(RT)}$ (fraction with enough energy)
3. Steric factor $p$ (fraction with correct orientation)

$$
k = p \cdot Z \cdot e^{-E_a/(RT)} = A\,e^{-E_a/(RT)}
$$

where $A = pZ$ is the pre-exponential factor (frequency factor).

**Determining $E_a$ from data — the Arrhenius plot:**

Taking $\ln$ of both sides:

$$
\ln k = \ln A - \frac{E_a}{R}\cdot\frac{1}{T}
$$

Plot $\ln k$ vs. $1/T$: slope = $-E_a/R$, intercept = $\ln A$.

**Two-point form:**

$$
\ln\frac{k_2}{k_1} = \frac{E_a}{R}\left(\frac{1}{T_1} - \frac{1}{T_2}\right)
$$

**Worked Example:** A reaction has $k = 3.2 \times 10^{-3}\,\text{s}^{-1}$ at 300 K and $k = 0.47\,\text{s}^{-1}$ at 400 K.

$$
\ln\frac{0.47}{3.2 \times 10^{-3}} = \frac{E_a}{8.314}\left(\frac{1}{300} - \frac{1}{400}\right)
$$

$$
4.99 = \frac{E_a}{8.314} \times 8.33 \times 10^{-4}
$$

$$
E_a = \frac{4.99 \times 8.314}{8.33 \times 10^{-4}} = 49.8\,\text{kJ/mol}
$$

### 8.4 — Transition State Theory (Eyring Equation)

Transition state theory (TST) goes beyond Arrhenius by providing a theoretical expression for the pre-exponential factor.

**The fundamental assumption:** Reactants are in quasi-equilibrium with the transition state (activated complex):

$$
A + B \rightleftharpoons [AB]^\ddagger \to \text{Products}
$$

**The Eyring equation:**

$$
k = \frac{k_BT}{h}\,e^{-\Delta G^\ddagger/(RT)} = \frac{k_BT}{h}\,e^{\Delta S^\ddagger/R}\,e^{-\Delta H^\ddagger/(RT)}
$$

where:
- $\Delta G^\ddagger$ = Gibbs free energy of activation
- $\Delta H^\ddagger$ = enthalpy of activation ($\approx E_a - RT$ for unimolecular; $\approx E_a - 2RT$ for bimolecular)
- $\Delta S^\ddagger$ = entropy of activation (tells you about the transition state structure)
- $k_BT/h \approx 6.25 \times 10^{12}\,\text{s}^{-1}$ at 300 K (universal frequency factor)

**Derivation from statistical mechanics:**

The equilibrium constant for forming the transition state:

$$
K^\ddagger = \frac{q^\ddagger}{q_A q_B}\,e^{-\Delta E_0^\ddagger/(k_BT)}
$$

The rate of crossing the barrier (one vibrational mode of the transition state becomes a translation along the reaction coordinate):

$$
k = \frac{k_BT}{h}\,K^\ddagger = \frac{k_BT}{h}\frac{q^\ddagger}{q_A q_B}\,e^{-\Delta E_0^\ddagger/(k_BT)}
$$

**Interpreting $\Delta S^\ddagger$:**

| $\Delta S^\ddagger$ | Meaning | Example |
|---|---|---|
| Large negative | Tight, ordered transition state | Bimolecular: two molecules → one complex |
| Near zero | Similar structure to reactants | Unimolecular isomerization |
| Positive | Loose, disordered transition state | Dissociation reactions |

**Connection to Arrhenius:** Comparing $k = A\,e^{-E_a/(RT)}$ with the Eyring equation:

$$
A = \frac{k_BT}{h}\,e^{1+\Delta S^\ddagger/R}
$$

$$
E_a = \Delta H^\ddagger + nRT \quad (n = 1 \text{ for unimolecular}, n = 2 \text{ for bimolecular in gas phase})
$$

### 8.5 — Heterogeneous Catalysis: The Langmuir-Hinshelwood Mechanism

Most industrial chemistry uses heterogeneous catalysts (solid catalyst, gas/liquid reactants). The Langmuir-Hinshelwood (LH) mechanism assumes:

1. Both reactants adsorb on the catalyst surface.
2. Reaction occurs between adsorbed species.
3. Products desorb.

**The Langmuir adsorption isotherm:**

For species A adsorbing on a surface with $N$ equivalent sites:

$$
\theta_A = \frac{K_A P_A}{1 + K_A P_A + K_B P_B}
$$

where $\theta_A$ = fractional surface coverage, $K_A$ = adsorption equilibrium constant, $P_A$ = partial pressure.

**The LH rate expression** for $A + B \to \text{Products}$:

$$
r = k\,\theta_A\,\theta_B = \frac{k\,K_A K_B P_A P_B}{(1 + K_A P_A + K_B P_B)^2}
$$

**Limiting cases:**

1. **Low coverage** ($K_A P_A, K_B P_B \ll 1$): $r \approx k K_A K_B P_A P_B$ — first order in each reactant.
2. **A strongly adsorbed** ($K_A P_A \gg 1 + K_B P_B$): $r \approx k K_B P_B / (K_A P_A)$ — rate DECREASES with more A (self-poisoning).
3. **Both saturated** ($K_A P_A, K_B P_B \gg 1$): $r \approx k$ — zero order in both (surface fully covered).

**Industrial example — Haber-Bosch process:**

$$
\text{N}_2 + 3\text{H}_2 \xrightarrow{\text{Fe catalyst}} 2\text{NH}_3
$$

The rate-determining step is N₂ dissociative adsorption on the iron surface. The overall rate:

$$
r = k\,\frac{K_{N_2} P_{N_2}}{(1 + K_{N_2}^{1/2}P_{N_2}^{1/2} + K_{H_2}^{1/2}P_{H_2}^{1/2} + K_{NH_3}P_{NH_3}/P_{H_2}^{3/2})^2}
$$

This explains why:
- High pressure favors the reaction (Le Chatelier: fewer moles on product side)
- Moderate temperature is optimal (too low = slow kinetics; too high = unfavorable equilibrium)
- NH₃ must be removed continuously (product inhibition)

> [!tip] Cross-link to Track 05
> The partition function derivation of $K$ connects directly to [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy). The Boltzmann factor in Arrhenius connects to [5.7 - Maxwell-Boltzmann Distribution & Kinetic Theory](5.7---Maxwell-Boltzmann-Distribution-&-Kinetic-Theory). Chemical thermodynamics IS statistical mechanics applied to molecular systems.

## 📎 9. Appendix — Deep Dives & Mastery Challenges

### Appendix A — The Eyring Equation: Full Derivation

Starting from the canonical partition function for the transition state:

**Step 1:** The activated complex $[AB]^\ddagger$ has $3N - 1$ vibrational modes (one mode is the reaction coordinate — an unstable vibration along which the complex decomposes).

**Step 2:** Factor out the reaction-coordinate mode from $q^\ddagger$:

$$
q^\ddagger = q^\ddagger_{\text{internal}} \cdot q_{\text{RC}}
$$

For the reaction coordinate (a very loose vibration with frequency $\nu^\ddagger \to 0$):

$$
q_{\text{RC}} = \frac{k_BT}{h\nu^\ddagger}
$$

(high-temperature limit of the vibrational partition function when $h\nu^\ddagger \ll k_BT$)

**Step 3:** The rate of crossing the barrier:

$$
k_{\text{rate}} = \nu^\ddagger \cdot K^\ddagger_c
$$

where $K^\ddagger_c$ is the concentration equilibrium constant for forming the transition state (excluding the reaction coordinate mode).

**Step 4:** Substituting:

$$
K^\ddagger_c = \frac{[AB]^\ddagger}{[A][B]} = \frac{q^\ddagger_{\text{internal}}}{q_A q_B}\,e^{-\Delta E_0^\ddagger/(k_BT)} \cdot \frac{k_BT}{h\nu^\ddagger} \cdot \frac{1}{\nu^\ddagger}
$$

Wait — let's be more careful. The full equilibrium constant including the RC mode:

$$
K^\ddagger = \frac{q^\ddagger}{q_A q_B}e^{-\Delta E_0^\ddagger/(k_BT)} = \frac{q^\ddagger_{\text{int}}}{q_A q_B}\cdot\frac{k_BT}{h\nu^\ddagger}\cdot e^{-\Delta E_0^\ddagger/(k_BT)}
$$

The rate = frequency of crossing × concentration of transition state:

$$
k = \nu^\ddagger \cdot \frac{q^\ddagger_{\text{int}}}{q_A q_B}\cdot\frac{k_BT}{h\nu^\ddagger}\cdot e^{-\Delta E_0^\ddagger/(k_BT)}
$$

The $\nu^\ddagger$ cancels:

$$
\boxed{k = \frac{k_BT}{h}\cdot\frac{q^\ddagger_{\text{int}}}{q_A q_B}\cdot e^{-\Delta E_0^\ddagger/(k_BT)}}
$$

**Step 5:** Relating to thermodynamic quantities:

$$
\Delta G^\ddagger = -RT\ln K^\ddagger_{\text{int}} = \Delta H^\ddagger - T\Delta S^\ddagger
$$

$$
k = \frac{k_BT}{h}\,e^{-\Delta G^\ddagger/(RT)} = \frac{k_BT}{h}\,e^{\Delta S^\ddagger/R}\,e^{-\Delta H^\ddagger/(RT)}
$$

This is the **Eyring equation** — the most important equation in chemical kinetics theory.

**Numerical check:** At $T = 298\,\text{K}$:

$$
\frac{k_BT}{h} = \frac{1.381 \times 10^{-23} \times 298}{6.626 \times 10^{-34}} = 6.21 \times 10^{12}\,\text{s}^{-1}
$$

This is the maximum possible rate constant (when $\Delta G^\ddagger = 0$) — about $10^{13}\,\text{s}^{-1}$. Real reactions are slower because $\Delta G^\ddagger > 0$.

### Appendix B — Catalysis: How Catalysts Work at the Molecular Level

**A catalyst provides an alternative reaction pathway with lower $\Delta G^\ddagger$.**

It does NOT:
- Change $\Delta G$ of the overall reaction
- Change the equilibrium constant $K$
- Change the thermodynamics — only the kinetics

**Types of catalysis:**

| Type | Mechanism | Example |
|---|---|---|
| Homogeneous | Catalyst in same phase as reactants | Acid catalysis, enzyme catalysis |
| Heterogeneous | Catalyst in different phase (usually solid) | Haber process (Fe), catalytic converter (Pt/Pd/Rh) |
| Enzymatic | Biological protein catalyst | All metabolism |
| Autocatalytic | Product catalyzes its own formation | Combustion, prion diseases |

**The Sabatier principle:** The best catalyst binds reactants with intermediate strength.
- Too weak binding → reactants don't adsorb → no reaction
- Too strong binding → products don't desorb → catalyst poisoned
- Optimal → "volcano plot" (rate vs. binding energy is an inverted V)

This explains why platinum-group metals are excellent catalysts — they sit at the peak of the volcano plot for many reactions.

### Appendix C — Reaction Coordinate Diagrams: Quantitative Reading

**For a single-step reaction:**

$$
\text{Reactants} \xrightarrow{\Delta G^\ddagger} \text{Transition State} \xrightarrow{} \text{Products}
$$

- Forward activation energy: $E_a^f = \Delta G^\ddagger$
- Reverse activation energy: $E_a^r = \Delta G^\ddagger - \Delta G_{\text{rxn}}$
- If $\Delta G_{\text{rxn}} < 0$ (exergonic): $E_a^f < E_a^r$
- If $\Delta G_{\text{rxn}} > 0$ (endergonic): $E_a^f > E_a^r$

**For a multi-step reaction** (e.g., SN1 mechanism):

$$
\text{R-X} \xrightarrow{E_{a1}} [\text{R}^+\cdots\text{X}^-]^\ddagger \to \text{R}^+ + \text{X}^- \xrightarrow{E_{a2}} [\text{R}\cdots\text{Nu}]^\ddagger \to \text{R-Nu}
$$

- The **rate-determining step** (RDS) has the highest transition state energy.
- Intermediates are local minima (real species with finite lifetime).
- Transition states are saddle points (exist for ~1 vibrational period, $\sim 10^{-13}\,\text{s}$).

**The Hammond postulate:** For an exothermic step, the transition state resembles the reactants (early TS). For an endothermic step, the transition state resembles the products (late TS). This lets you predict TS structure from thermodynamics.

### Appendix D — Computational Kinetics: Calculating Rate Constants

```python
import numpy as np

# Eyring equation calculator
def eyring_rate(T, dH_ddagger, dS_ddagger):
    """
    Calculate rate constant from Eyring equation.
    
    Parameters:
        T: temperature (K)
        dH_ddagger: activation enthalpy (J/mol)
        dS_ddagger: activation entropy (J/(mol*K))
    
    Returns:
        k: rate constant (s^-1 for unimolecular)
    """
    kB = 1.381e-23  # Boltzmann constant (J/K)
    h = 6.626e-34   # Planck constant (J*s)
    R = 8.314       # Gas constant (J/(mol*K))
    
    k = (kB * T / h) * np.exp(dS_ddagger / R) * np.exp(-dH_ddagger / (R * T))
    return k

# Example: enzyme-catalyzed reaction
# Typical enzyme: dH‡ ~ 50 kJ/mol, dS‡ ~ -10 J/(mol*K)
T = 310  # body temperature (K)
dH = 50000  # J/mol
dS = -10    # J/(mol*K)

k_enzyme = eyring_rate(T, dH, dS)
print(f"Enzyme-catalyzed rate constant: {k_enzyme:.2e} s^-1")
print(f"Turnover time: {1/k_enzyme:.4f} s")

# Uncatalyzed: dH‡ ~ 100 kJ/mol
k_uncat = eyring_rate(T, 100000, dS)
print(f"\nUncatalyzed rate constant: {k_uncat:.2e} s^-1")
print(f"Catalytic acceleration: {k_enzyme/k_uncat:.2e} fold")

# Temperature dependence (Arrhenius plot)
T_range = np.linspace(250, 400, 50)
k_range = eyring_rate(T_range, dH, dS)

# The "rule of thumb": rate doubles every 10°C
k_300 = eyring_rate(300, dH, dS)
k_310 = eyring_rate(310, dH, dS)
print(f"\nRate ratio (310K/300K): {k_310/k_300:.2f}")
print(f"(Rule of thumb predicts ~2; actual depends on Ea)")
```

### Appendix E — The Thermodynamic Square (Born Square)

A mnemonic for Maxwell relations and thermodynamic identities:

```
        S ←――― A ―――→ V
        |               |
        |   (internal)  |
        |               |
        U               G
        |               |
        |  (external)   |
        |               |
        T ←――― H ―――→ P
```

**Reading the square:**
- Each potential (U, H, A, G) has two natural variables (adjacent corners)
- Derivatives: $\left(\frac{\partial U}{\partial S}\right)_V = T$, $\left(\frac{\partial U}{\partial V}\right)_S = -P$, etc.
- Maxwell relations: cross-derivatives of adjacent corners with sign from the diagonal

**The four Maxwell relations:**

$$
\left(\frac{\partial T}{\partial V}\right)_S = -\left(\frac{\partial P}{\partial S}\right)_V
$$

$$
\left(\frac{\partial T}{\partial P}\right)_S = \left(\frac{\partial V}{\partial S}\right)_P
$$

$$
\left(\frac{\partial S}{\partial V}\right)_T = \left(\frac{\partial P}{\partial T}\right)_V
$$

$$
\left(\frac{\partial S}{\partial P}\right)_T = -\left(\frac{\partial V}{\partial T}\right)_P
$$

These connect measurable quantities (P, V, T, heat capacities) to entropy changes — essential for computing $\Delta S$ of real processes. Full derivation in [5.3 - Thermodynamic Potentials & Maxwell Relations](5.3---Thermodynamic-Potentials-&-Maxwell-Relations).

> [!danger] 🧠 Common Misconceptions — Section 8 & 9 Summary
> 
> **❌ "Exothermic reactions are always spontaneous"**
> **Truth:** Spontaneity requires ΔG < 0, not ΔH < 0. An exothermic reaction with large negative ΔS can be non-spontaneous at high T (e.g., 3H₂ + N₂ → 2NH₃ becomes unfavorable above ~460°C despite being exothermic).
> 
> **❌ "A catalyst makes a reaction go faster by adding energy"**
> **Truth:** A catalyst lowers the activation energy by providing an alternative pathway. It doesn't add energy — it changes the mechanism. The catalyst is regenerated at the end (not consumed).
> 
> **❌ "The rate-determining step is always the slowest step"**
> **Truth:** More precisely, the RDS has the highest-energy transition state relative to the starting materials. In a multi-step mechanism, a fast step can be rate-determining if it has the highest absolute barrier.
> 
> **❌ "Equilibrium means nothing is happening"**
> **Truth:** At equilibrium, forward and reverse rates are EQUAL but non-zero. Molecules are constantly reacting in both directions. The macroscopic concentrations don't change because the rates cancel — this is dynamic equilibrium.
> 
> **❌ "The Arrhenius equation is just empirical"**
> **Truth:** It's derivable from the Boltzmann distribution (the fraction of molecules with energy ≥ Ea). The Eyring equation provides the theoretical foundation and gives physical meaning to the pre-exponential factor A.
> 
> **❌ "Temperature only affects kinetics, not thermodynamics"**
> **Truth:** Temperature affects BOTH. ΔG = ΔH - TΔS is explicitly T-dependent. The equilibrium constant K changes with temperature (van't Hoff equation). Temperature shifts both the rate AND the position of equilibrium.

---

*Previous: [03.3 - Stoichiometry & Reactions](03.3---Stoichiometry-&-Reactions) | Next: [03.5 - Acids, Bases & Equilibrium](03.5---Acids,-Bases-&-Equilibrium)*
