---
title: "03.6 — Electrochemistry & Redox"
subject: "Chemistry"
catalog: advanced
audience_tier: higher-education
chapter: "03.6"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 03.6 — Electrochemistry & Redox

> *"Electricity is but yet a new agent for the arts and manufactures, and, doubtless, generations unborn will discover that it has powers which we never dreamt of."* — Michael Faraday

Electrochemistry is the bridge between chemical energy and electrical energy. Every battery, every fuel cell, every corrosion process, and every electroplating operation is governed by the same thermodynamic principle: $\Delta G = -nFE$. This chapter connects the Gibbs free energy you derived in Track 05 to measurable cell voltages.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Assign oxidation states and identify oxidation/reduction in any reaction.
2. Balance redox equations using the half-reaction method (acidic and basic solutions).
3. Calculate standard cell potential $E^\circ_{\text{cell}}$ from standard reduction potentials.
4. Apply the Nernst equation to calculate cell potential under non-standard conditions.
5. Connect $\Delta G$, $K$, and $E^\circ$: the thermodynamic triangle.
6. Distinguish galvanic (spontaneous) from electrolytic (non-spontaneous) cells.
7. Apply Faraday's laws of electrolysis for quantitative calculations.
8. Explain battery chemistry (Li-ion, lead-acid) and corrosion mechanisms.

---

## 🖼️ Visual Anchor — The Thermodynamic Triangle

![chem__16.6-fig1](chem__16.6-fig1.svg)

---

## 📚 1. Definitions

### Definition 03.6.1 — Oxidation and Reduction

- **Oxidation:** Loss of electrons (increase in oxidation state). OIL.
- **Reduction:** Gain of electrons (decrease in oxidation state). RIG.
- **Mnemonic:** OIL RIG (Oxidation Is Loss, Reduction Is Gain).

### Definition 03.6.2 — Standard Reduction Potential ($E^\circ$)

The voltage of a half-reaction measured against the Standard Hydrogen Electrode (SHE) at standard conditions (25°C, 1 M, 1 atm).

$$
\text{SHE: } 2\text{H}^+(1\text{ M}) + 2e^- \to \text{H}_2(1\text{ atm}), \quad E^\circ = 0.000 \text{ V}
$$

### Definition 03.6.3 — Standard Cell Potential

$$
E^\circ_{\text{cell}} = E^\circ_{\text{cathode}} - E^\circ_{\text{anode}}
$$

(Cathode = reduction; Anode = oxidation.)

### Definition 03.6.4 — Faraday's Constant

$$
F = N_A \times e = 96485 \text{ C/mol}
$$

The charge of one mole of electrons.

### Definition 03.6.5 — Galvanic (Voltaic) Cell

A cell that converts chemical energy to electrical energy spontaneously ($\Delta G < 0$, $E_{\text{cell}} > 0$).

### Definition 03.6.6 — Electrolytic Cell

A cell that uses external electrical energy to drive a non-spontaneous reaction ($\Delta G > 0$, requires applied voltage > $E_{\text{cell}}$).

---

## 📐 2. Mathematical Foundations

### 2.1 The Fundamental Relationship: $\Delta G = -nFE$

The maximum non-expansion work from a reaction equals the Gibbs free energy change:

$$
\boxed{\Delta G = -nFE_{\text{cell}}}
$$

where $n$ = moles of electrons transferred.

At standard conditions: $\Delta G^\circ = -nFE^\circ_{\text{cell}}$.

**Derivation:** Electrical work = charge × voltage = $nF \times E$. Since $\Delta G = w_{\text{max}}$ (at constant $T, P$) and work done BY the system is negative:

$$
\Delta G = -w_{\text{elec}} = -nFE
$$

### 2.2 The Nernst Equation

Combining $\Delta G = \Delta G^\circ + RT\ln Q$ with $\Delta G = -nFE$:

$$
-nFE = -nFE^\circ + RT\ln Q
$$

$$
\boxed{E = E^\circ - \frac{RT}{nF}\ln Q = E^\circ - \frac{0.0592}{n}\log Q \quad \text{(at 25°C)}}
$$

At equilibrium ($E = 0$, $Q = K$):

$$
E^\circ = \frac{RT}{nF}\ln K = \frac{0.0592}{n}\log K
$$

### 2.3 The Thermodynamic Triangle

$$
\Delta G^\circ = -nFE^\circ = -RT\ln K
$$

| Known | Find $E^\circ$ | Find $K$ | Find $\Delta G^\circ$ |
|---|---|---|---|
| $E^\circ$ | — | $K = e^{nFE^\circ/(RT)}$ | $\Delta G^\circ = -nFE^\circ$ |
| $K$ | $E^\circ = \frac{RT}{nF}\ln K$ | — | $\Delta G^\circ = -RT\ln K$ |
| $\Delta G^\circ$ | $E^\circ = -\Delta G^\circ/(nF)$ | $K = e^{-\Delta G^\circ/(RT)}$ | — |

### 2.4 Faraday's Laws of Electrolysis

**First Law:** Mass deposited ∝ charge passed.

$$
m = \frac{MIt}{nF}
$$

where $M$ = molar mass, $I$ = current (A), $t$ = time (s), $n$ = electrons per formula unit.

**Second Law:** For the same charge, masses deposited are proportional to equivalent weights ($M/n$).

### 2.5 Concentration Cells

A cell where both half-cells have the same reaction but different concentrations:

$$
E = \frac{RT}{nF}\ln\frac{[\text{concentrated}]}{[\text{dilute}]}
$$

The cell generates voltage from the entropy of mixing — a direct manifestation of the second law.

---

## 🔬 3. Chemical Mechanisms

### 3.1 Galvanic Cell Operation (Daniell Cell Example)

**Anode (oxidation):** $\text{Zn}(s) \to \text{Zn}^{2+}(aq) + 2e^-$ ($E^\circ = -0.76$ V)

**Cathode (reduction):** $\text{Cu}^{2+}(aq) + 2e^- \to \text{Cu}(s)$ ($E^\circ = +0.34$ V)

**Overall:** $\text{Zn}(s) + \text{Cu}^{2+}(aq) \to \text{Zn}^{2+}(aq) + \text{Cu}(s)$

$$
E^\circ_{\text{cell}} = 0.34 - (-0.76) = 1.10 \text{ V}
$$

- Electrons flow through external circuit from Zn to Cu
- Salt bridge maintains electrical neutrality (ions migrate)
- Zn electrode dissolves; Cu deposits on Cu electrode

### 3.2 Battery Chemistry

**Lead-Acid Battery** (car battery):
- Anode: $\text{Pb} + \text{SO}_4^{2-} \to \text{PbSO}_4 + 2e^-$
- Cathode: $\text{PbO}_2 + 4\text{H}^+ + \text{SO}_4^{2-} + 2e^- \to \text{PbSO}_4 + 2\text{H}_2\text{O}$
- $E^\circ = 2.05$ V per cell; 6 cells = 12.3 V

**Lithium-Ion Battery**:
- Anode: $\text{LiC}_6 \to \text{C}_6 + \text{Li}^+ + e^-$ (Li intercalated in graphite)
- Cathode: $\text{Li}_{1-x}\text{CoO}_2 + x\text{Li}^+ + xe^- \to \text{LiCoO}_2$
- $E \approx 3.7$ V; high energy density

### 3.3 Corrosion

Iron corrosion is an electrochemical process:
- Anodic region: $\text{Fe} \to \text{Fe}^{2+} + 2e^-$ (iron dissolves)
- Cathodic region: $\text{O}_2 + 2\text{H}_2\text{O} + 4e^- \to 4\text{OH}^-$ (oxygen reduction)
- $\text{Fe}^{2+} + 2\text{OH}^- \to \text{Fe(OH)}_2 \to \text{Fe}_2\text{O}_3$ (rust)

**Prevention:** Galvanization (Zn coating acts as sacrificial anode), cathodic protection, paint barriers.

---

## ✍️ 4. Worked Examples

### Example 03.6.1 — Calculating Cell Potential and $\Delta G$

**Problem:** Calculate $E^\circ_{\text{cell}}$, $\Delta G^\circ$, and $K$ for: $2\text{Ag}^+(aq) + \text{Cu}(s) \to 2\text{Ag}(s) + \text{Cu}^{2+}(aq)$

Given: $E^\circ(\text{Ag}^+/\text{Ag}) = +0.80$ V, $E^\circ(\text{Cu}^{2+}/\text{Cu}) = +0.34$ V.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Identify cathode and anode.
- Ag⁺ is reduced → cathode: $E^\circ = +0.80$ V
- Cu is oxidized → anode: $E^\circ = +0.34$ V

**Step 2:** Calculate $E^\circ_{\text{cell}}$.

$$
E^\circ_{\text{cell}} = E^\circ_{\text{cathode}} - E^\circ_{\text{anode}} = 0.80 - 0.34 = +0.46 \text{ V}
$$

Positive → spontaneous. ✓

**Step 3:** Calculate $\Delta G^\circ$ ($n = 2$ electrons transferred).

$$
\Delta G^\circ = -nFE^\circ = -2(96485)(0.46) = -88,800 \text{ J/mol} = -88.8 \text{ kJ/mol}
$$

**Step 4:** Calculate $K$.

$$
\ln K = \frac{nFE^\circ}{RT} = \frac{2(96485)(0.46)}{8.314(298)} = 35.8
$$

$$
K = e^{35.8} = 3.5 \times 10^{15}
$$

**Interpretation:** Enormously large $K$ — reaction goes essentially to completion. This is why copper dissolves in silver nitrate solution (a classic demo).

</details>

---

### Example 03.6.2 — Nernst Equation Application

**Problem:** Calculate the cell potential for the Daniell cell when $[\text{Zn}^{2+}] = 0.10$ M and $[\text{Cu}^{2+}] = 2.0$ M.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Write the overall reaction and $Q$.

$$
\text{Zn}(s) + \text{Cu}^{2+}(aq) \to \text{Zn}^{2+}(aq) + \text{Cu}(s)
$$

$$
Q = \frac{[\text{Zn}^{2+}]}{[\text{Cu}^{2+}]} = \frac{0.10}{2.0} = 0.050
$$

(Solids don't appear in $Q$.)

**Step 2:** Apply Nernst equation ($n = 2$, $E^\circ = 1.10$ V).

$$
E = E^\circ - \frac{0.0592}{n}\log Q = 1.10 - \frac{0.0592}{2}\log(0.050)
$$

$$
= 1.10 - 0.0296 \times (-1.301) = 1.10 + 0.039 = 1.14 \text{ V}
$$

**Interpretation:** The cell voltage is HIGHER than standard because $Q \lt  1$ (Le Chatelier: low product concentration drives the reaction forward more strongly).

</details>

---

### Example 03.6.3 — Electrolysis Calculation

**Problem:** How long must a current of 3.00 A flow to deposit 5.00 g of copper from a CuSO₄ solution?

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Write the cathode half-reaction.

$$
\text{Cu}^{2+} + 2e^- \to \text{Cu}(s) \quad (n = 2)
$$

**Step 2:** Calculate moles of Cu.

$$
n_{\text{Cu}} = \frac{5.00}{63.55} = 0.0787 \text{ mol}
$$

**Step 3:** Calculate moles of electrons needed.

$$
n_{e^-} = 2 \times 0.0787 = 0.1574 \text{ mol}
$$

**Step 4:** Calculate charge.

$$
Q = n_{e^-} \times F = 0.1574 \times 96485 = 15,190 \text{ C}
$$

**Step 5:** Calculate time.

$$
t = \frac{Q}{I} = \frac{15190}{3.00} = 5063 \text{ s} = 84.4 \text{ min}
$$

</details>

---

## 🧠 5. Connections to Other Tracks

| This Chapter | Connects To | How |
|---|---|---|
| $\Delta G = -nFE$ | [5.3 - Thermodynamic Potentials & Maxwell Relations](5.3---Thermodynamic-Potentials-&-Maxwell-Relations) | Gibbs free energy as maximum work |
| Nernst equation | [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy) | $\Delta G = \Delta G^\circ + RT\ln Q$ |
| Battery chemistry | [03.8 - Biochemistry & Modern Topics](03.8---Biochemistry-&-Modern-Topics) | Materials science, Li-ion design |
| Faraday's laws | [7.1 - Electrostatics & Coulomb's Law](7.1---Electrostatics-&-Coulomb's-Law) | Charge and current |
| Corrosion | [03.2 - Chemical Bonding - Ionic, Covalent, Metallic & Intermolecular](03.2---Chemical-Bonding---Ionic,-Covalent,-Metallic-&-Intermolecular) | Metallic bonding and reactivity |

---

## ⚠️ 6. Common Misconceptions & Where Most Students Fail

### ❌ Misconception 1: "Multiply $E^\circ$ by the stoichiometric coefficient"

**The truth:** Standard reduction potentials are INTENSIVE properties — they don't change when you multiply the half-reaction. $E^\circ(\text{Ag}^+/\text{Ag}) = +0.80$ V whether you write $\text{Ag}^+ + e^- \to \text{Ag}$ or $2\text{Ag}^+ + 2e^- \to 2\text{Ag}$. Only $\Delta G$ (extensive) gets multiplied.

### ❌ Misconception 2: "The anode is always negative"

**The truth:** In a galvanic cell, the anode is negative (electrons flow away from it). In an electrolytic cell, the anode is POSITIVE (connected to the positive terminal of the power supply). The definition of anode (oxidation occurs) doesn't change — but the sign convention does.

### ❌ Misconception 3: "A positive $E^\circ$ means the reaction always happens"

**The truth:** $E^\circ > 0$ means the reaction is spontaneous under STANDARD conditions. Under non-standard conditions, use the Nernst equation — $E$ can be negative even if $E^\circ$ is positive (when $Q > K$).

### ❌ Misconception 4: "Electrolysis can make any reaction happen"

**The truth:** Electrolysis can drive non-spontaneous reactions, but you need to supply at least $|E_{\text{cell}}|$ volts PLUS overpotential (extra voltage needed to overcome kinetic barriers at the electrode surface). Real electrolysis always requires more voltage than thermodynamics predicts.

### 💪 The Pep Talk

Electrochemistry intimidates students because it combines redox chemistry (which is already confusing) with electrical circuits (which feel like physics, not chemistry). But the core idea is beautifully simple:

**Chemical reactions can do electrical work. Electrical work can drive chemical reactions.**

The quantitative link is one equation: $\Delta G = -nFE$. Everything else — Nernst equation, Faraday's laws, cell notation — is just applying this one relationship in different contexts. You already understand $\Delta G$ from thermodynamics. Now you're just measuring it with a voltmeter instead of a calorimeter.

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- [5.3 - Thermodynamic Potentials & Maxwell Relations](5.3---Thermodynamic-Potentials-&-Maxwell-Relations) — Gibbs free energy
- [03.5 - Acids, Bases & Equilibrium](03.5---Acids,-Bases-&-Equilibrium) — $K$ and $\Delta G^\circ$
- [03.3 - Stoichiometry & Reactions](03.3---Stoichiometry-&-Reactions) — Redox balancing
- [03.8 - Biochemistry & Modern Topics](03.8---Biochemistry-&-Modern-Topics) — Battery materials, fuel cells

### External References
- **MIT 5.111 OCW** — Lectures 27–30: Electrochemistry
- **Khan Academy** — [Electrochemistry](https://www.khanacademy.org/science/chemistry/oxidation-reduction)
- **Crash Course Chemistry** — Episodes 36–37: Electrochemistry
- **Atkins, P.** — *Physical Chemistry*, Chapter 6 (electrochemistry)

---

## 🔬 8. Advanced Derivations — Electrochemistry from Thermodynamics

### 8.1 — The Nernst Equation: Full Derivation

**Starting point:** The relationship between Gibbs free energy and cell potential:

$$
\Delta G = -nFE
$$

where $n$ = moles of electrons transferred, $F = 96485\,\text{C/mol}$ (Faraday's constant), $E$ = cell potential.

**For non-standard conditions**, the reaction quotient $Q$ modifies $\Delta G$:

$$
\Delta G = \Delta G^\circ + RT\ln Q
$$

**Substituting** $\Delta G = -nFE$ and $\Delta G^\circ = -nFE^\circ$:

$$
-nFE = -nFE^\circ + RT\ln Q
$$

**Dividing by $-nF$:**

$$
\boxed{E = E^\circ - \frac{RT}{nF}\ln Q}
$$

**At 25°C**, converting to $\log_{10}$:

$$
E = E^\circ - \frac{0.05916}{n}\log Q
$$

**At equilibrium** ($E = 0$, $Q = K$):

$$
0 = E^\circ - \frac{RT}{nF}\ln K
$$

$$
\ln K = \frac{nFE^\circ}{RT} \quad \Rightarrow \quad E^\circ = \frac{RT}{nF}\ln K = \frac{0.05916}{n}\log K
$$

This connects electrochemistry to equilibrium: a positive $E^\circ$ means $K > 1$ (products favored).

**The thermodynamic triangle:**

$$
\Delta G^\circ = -nFE^\circ = -RT\ln K
$$

| Known | Find $\Delta G^\circ$ | Find $K$ | Find $E^\circ$ |
|---|---|---|---|
| $E^\circ$ | $-nFE^\circ$ | $10^{nE^\circ/0.05916}$ | — |
| $K$ | $-RT\ln K$ | — | $(RT/nF)\ln K$ |
| $\Delta G^\circ$ | — | $e^{-\Delta G^\circ/(RT)}$ | $-\Delta G^\circ/(nF)$ |

### 8.2 — Standard Reduction Potentials: Reading the Table

**The convention:** All half-reactions are written as reductions:

$$
\text{Oxidized form} + ne^- \to \text{Reduced form}, \quad E^\circ_{\text{red}}
$$

**Selected standard reduction potentials (25°C):**

| Half-reaction | $E^\circ$ (V) |
|---|---|
| $\text{F}_2 + 2e^- \to 2\text{F}^-$ | +2.87 |
| $\text{Au}^{3+} + 3e^- \to \text{Au}$ | +1.50 |
| $\text{Cl}_2 + 2e^- \to 2\text{Cl}^-$ | +1.36 |
| $\text{O}_2 + 4\text{H}^+ + 4e^- \to 2\text{H}_2\text{O}$ | +1.23 |
| $\text{Ag}^+ + e^- \to \text{Ag}$ | +0.80 |
| $\text{Cu}^{2+} + 2e^- \to \text{Cu}$ | +0.34 |
| $2\text{H}^+ + 2e^- \to \text{H}_2$ | 0.00 (reference) |
| $\text{Pb}^{2+} + 2e^- \to \text{Pb}$ | -0.13 |
| $\text{Ni}^{2+} + 2e^- \to \text{Ni}$ | -0.26 |
| $\text{Fe}^{2+} + 2e^- \to \text{Fe}$ | -0.44 |
| $\text{Zn}^{2+} + 2e^- \to \text{Zn}$ | -0.76 |
| $\text{Al}^{3+} + 3e^- \to \text{Al}$ | -1.66 |
| $\text{Mg}^{2+} + 2e^- \to \text{Mg}$ | -2.37 |
| $\text{Na}^+ + e^- \to \text{Na}$ | -2.71 |
| $\text{Li}^+ + e^- \to \text{Li}$ | -3.04 |

**How to use the table:**

1. The species with MORE POSITIVE $E^\circ$ is reduced (cathode).
2. The species with MORE NEGATIVE $E^\circ$ is oxidized (anode) — reverse its half-reaction.
3. Cell potential: $E^\circ_{\text{cell}} = E^\circ_{\text{cathode}} - E^\circ_{\text{anode}}$

**Important:** When reversing a half-reaction, change the SIGN of $E^\circ$ but do NOT multiply by the number of electrons. $E^\circ$ is an intensive property (energy per electron).

**Worked Example — Daniell Cell:**

$$
\text{Zn}(s) + \text{Cu}^{2+}(aq) \to \text{Zn}^{2+}(aq) + \text{Cu}(s)
$$

$$
E^\circ_{\text{cell}} = E^\circ_{\text{Cu}^{2+}/\text{Cu}} - E^\circ_{\text{Zn}^{2+}/\text{Zn}} = 0.34 - (-0.76) = 1.10\,\text{V}
$$

$$
\Delta G^\circ = -nFE^\circ = -2 \times 96485 \times 1.10 = -212\,\text{kJ/mol}
$$

$$
K = 10^{nE^\circ/0.05916} = 10^{2 \times 1.10/0.05916} = 10^{37.2} \approx 1.6 \times 10^{37}
$$

The reaction is overwhelmingly favorable — zinc spontaneously reduces copper ions.

### 8.3 — Electrolysis: Faraday's Laws

**Faraday's First Law:** The mass of substance deposited at an electrode is proportional to the charge passed:

$$
m = \frac{Q \cdot M}{n \cdot F} = \frac{I \cdot t \cdot M}{n \cdot F}
$$

where $Q = It$ (charge = current × time), $M$ = molar mass, $n$ = electrons per formula unit.

**Faraday's Second Law:** For the same charge, the masses of different substances deposited are proportional to their equivalent weights ($M/n$).

**Worked Example — Electroplating with copper:**

How long must 2.00 A flow to deposit 5.00 g of Cu from CuSO₄ solution?

$$
\text{Cu}^{2+} + 2e^- \to \text{Cu}
$$

$$
t = \frac{m \cdot n \cdot F}{I \cdot M} = \frac{5.00 \times 2 \times 96485}{2.00 \times 63.55} = 7590\,\text{s} = 2.11\,\text{hours}
$$

**Worked Example — Electrolysis of water:**

At 2.00 A, how much H₂ and O₂ are produced in 1 hour?

At cathode: $2\text{H}^+ + 2e^- \to \text{H}_2$ ($n = 2$ per H₂)
At anode: $2\text{H}_2\text{O} \to \text{O}_2 + 4\text{H}^+ + 4e^-$ ($n = 4$ per O₂)

Charge: $Q = 2.00 \times 3600 = 7200\,\text{C}$

$$
n(\text{H}_2) = \frac{Q}{nF} = \frac{7200}{2 \times 96485} = 0.0373\,\text{mol} = 0.0752\,\text{g}
$$

$$
n(\text{O}_2) = \frac{7200}{4 \times 96485} = 0.0187\,\text{mol} = 0.598\,\text{g}
$$

Volume at STP: $V(\text{H}_2) = 0.0373 \times 22.4 = 0.836\,\text{L}$

### 8.4 — Battery Chemistry: From Lead-Acid to Lithium-Ion

#### Lead-Acid Battery (car battery)

**Discharge reactions:**

Anode: $\text{Pb}(s) + \text{SO}_4^{2-} \to \text{PbSO}_4(s) + 2e^-$, $E^\circ = +0.36\,\text{V}$

Cathode: $\text{PbO}_2(s) + \text{SO}_4^{2-} + 4\text{H}^+ + 2e^- \to \text{PbSO}_4(s) + 2\text{H}_2\text{O}$, $E^\circ = +1.69\,\text{V}$

Overall: $E^\circ_{\text{cell}} = 1.69 + 0.36 = 2.05\,\text{V}$ (6 cells in series → 12V battery)

**Energy density:** ~35 Wh/kg (low — lead is heavy)

#### Lithium-Ion Battery

**Discharge reactions:**

Anode: $\text{Li}_x\text{C}_6 \to x\text{Li}^+ + xe^- + \text{C}_6$ (lithium deintercalates from graphite)

Cathode: $\text{Li}_{1-x}\text{CoO}_2 + x\text{Li}^+ + xe^- \to \text{LiCoO}_2$ (lithium intercalates into cobalt oxide)

**Cell voltage:** ~3.7 V (nearly double lead-acid per cell)

**Energy density:** ~250 Wh/kg (7× lead-acid)

**Why lithium?**
1. Most negative standard reduction potential ($E^\circ = -3.04\,\text{V}$) → highest cell voltage
2. Lightest metal ($M = 6.94\,\text{g/mol}$) → highest energy per unit mass
3. Small ionic radius → fast diffusion in solid electrodes

#### Solid-State Batteries (next generation)

Replace liquid electrolyte with solid ceramic (e.g., Li₇La₃Zr₂O₁₂ — "LLZO"):
- No flammable liquid → safer
- Enables lithium metal anode → ~500 Wh/kg theoretical
- Challenge: solid-solid interface resistance

#### Sodium-Ion Batteries (emerging)

Replace Li with Na:
- Na is 1000× more abundant than Li (cheaper)
- Slightly lower voltage (~3.2 V) and energy density (~160 Wh/kg)
- Suitable for grid storage where weight doesn't matter

### 8.5 — Corrosion Electrochemistry

**Corrosion is an electrochemical process** — the metal acts as both anode and cathode simultaneously (a "short-circuited" galvanic cell on the metal surface).

**Iron corrosion in neutral aerated water:**

Anodic sites: $\text{Fe} \to \text{Fe}^{2+} + 2e^-$, $E^\circ = -0.44\,\text{V}$

Cathodic sites: $\text{O}_2 + 2\text{H}_2\text{O} + 4e^- \to 4\text{OH}^-$, $E^\circ = +0.40\,\text{V}$

Overall: $E^\circ_{\text{cell}} = 0.40 - (-0.44) = 0.84\,\text{V}$ (thermodynamically very favorable)

The Fe²⁺ and OH⁻ combine: $\text{Fe}^{2+} + 2\text{OH}^- \to \text{Fe(OH)}_2 \to \text{Fe}_2\text{O}_3\cdot x\text{H}_2\text{O}$ (rust)

**Corrosion prevention methods:**

| Method | Mechanism | Example |
|---|---|---|
| Barrier coating | Prevent O₂/H₂O contact | Paint, polymer coating |
| Cathodic protection | Make iron the cathode | Sacrificial Zn anode (galvanizing) |
| Passivation | Form protective oxide | Stainless steel (Cr₂O₃ layer) |
| Inhibitors | Adsorb on surface, block reaction | Chromate, phosphate treatments |
| Alloying | Change electrode potential | Stainless steel (Cr, Ni additions) |

**Galvanic series in seawater** (practical corrosion ranking):

Most noble (cathodic): Pt > Au > Ti > 316SS > Ni > Cu > Sn > Pb > 304SS > Fe > Al > Zn > Mg

When two metals are in electrical contact in an electrolyte, the more active (anodic) metal corrodes preferentially. This is why zinc-coated (galvanized) steel is protected — zinc corrodes sacrificially.

> [!tip] Cross-link to Track 05
> The Nernst equation is a direct consequence of $\Delta G = \Delta G^\circ + RT\ln Q$ from [5.3 - Thermodynamic Potentials & Maxwell Relations](5.3---Thermodynamic-Potentials-&-Maxwell-Relations). The connection $\Delta G = -nFE$ comes from equating electrical work ($W = qE = nFE$) with the maximum non-expansion work ($W_{\max} = -\Delta G$). Electrochemistry IS thermodynamics measured in volts instead of joules.

## 📎 9. Appendix — Deep Dives & Mastery Challenges

### Appendix A — Tafel Kinetics: Electrode Reaction Rates

The **Tafel equation** describes how current density depends on overpotential (deviation from equilibrium potential):

$$
\eta = a + b\log|j|
$$

where $\eta = E - E_{\text{eq}}$ is the overpotential, $j$ is current density (A/cm²), and $a$, $b$ are Tafel constants.

**Derivation from the Butler-Volmer equation:**

The fundamental equation of electrode kinetics:

$$
j = j_0\left[\exp\left(\frac{\alpha_a F\eta}{RT}\right) - \exp\left(-\frac{\alpha_c F\eta}{RT}\right)\right]
$$

where:
- $j_0$ = exchange current density (rate at equilibrium — both directions equal)
- $\alpha_a, \alpha_c$ = anodic and cathodic transfer coefficients ($\alpha_a + \alpha_c = 1$ for a single-electron step)
- $\eta$ = overpotential

**At large overpotentials** ($|\eta| > 50\,\text{mV}$), one exponential dominates:

For anodic ($\eta > 0$):

$$
j \approx j_0\exp\left(\frac{\alpha_a F\eta}{RT}\right)
$$

$$
\eta = \frac{RT}{\alpha_a F}\ln\frac{j}{j_0} = \frac{2.303RT}{\alpha_a F}\log\frac{j}{j_0}
$$

The **Tafel slope** $b = 2.303RT/(\alpha_a F) \approx 120\,\text{mV/decade}$ (for $\alpha_a = 0.5$ at 25°C).

**Physical meaning:**
- Small $j_0$ → large overpotential needed → slow electrode kinetics (e.g., O₂ evolution on Pt)
- Large $j_0$ → small overpotential → fast kinetics (e.g., H₂/H⁺ on Pt)

**Practical importance:** The overpotential is "wasted" energy in electrolysis and batteries. Minimizing it (by choosing better catalysts with higher $j_0$) improves energy efficiency.

| Reaction | Electrode | $j_0$ (A/cm²) | Tafel slope (mV/dec) |
|---|---|---|---|
| H₂ evolution | Pt | $10^{-3}$ | 30 |
| H₂ evolution | Fe | $10^{-6}$ | 120 |
| H₂ evolution | Hg | $10^{-12}$ | 120 |
| O₂ evolution | Pt | $10^{-9}$ | 120 |
| O₂ reduction | Pt | $10^{-10}$ | 120 |

**Why hydrogen overpotential matters:** Mercury has extremely low $j_0$ for H₂ evolution. This means you can electrolyze NaCl solution on a mercury cathode and get Na(amalgam) instead of H₂ — the basis of the chlor-alkali process (now largely replaced by membrane cells for environmental reasons).

### Appendix B — Fuel Cells: Electrochemistry for Energy

A fuel cell converts chemical energy directly to electricity (like a battery that never runs out — fuel is continuously supplied).

**Hydrogen fuel cell (PEM — Proton Exchange Membrane):**

Anode: $\text{H}_2 \to 2\text{H}^+ + 2e^-$

Cathode: $\frac{1}{2}\text{O}_2 + 2\text{H}^+ + 2e^- \to \text{H}_2\text{O}$

Overall: $\text{H}_2 + \frac{1}{2}\text{O}_2 \to \text{H}_2\text{O}$, $E^\circ = 1.23\,\text{V}$

**Theoretical efficiency:**

$$
\eta_{\text{max}} = \frac{\Delta G}{\Delta H} = \frac{-237.1}{-285.8} = 83\%
$$

Compare to Carnot limit for a heat engine at the same temperatures: $\eta_{\text{Carnot}} = 1 - T_c/T_h \approx 40\text{–}60\%$. Fuel cells can exceed Carnot efficiency because they're not heat engines.

**Actual efficiency:** ~50–60% (losses from overpotential, ohmic resistance, mass transport).

**The oxygen reduction reaction (ORR)** is the bottleneck — it has very slow kinetics (low $j_0$) even on platinum. This is why fuel cell catalysts are expensive and why ORR catalyst research is a major field.

### Appendix C — Concentration Cells and Membrane Potentials

**A concentration cell** has identical electrodes but different concentrations:

$$
\text{Ag}|\text{Ag}^+(c_1)||\text{Ag}^+(c_2)|\text{Ag}
$$

$$
E = \frac{RT}{nF}\ln\frac{c_2}{c_1} = \frac{0.05916}{1}\log\frac{c_2}{c_1}
$$

If $c_2 > c_1$: $E > 0$ (spontaneous — system drives toward equal concentrations).

**Biological application — the Nernst potential:**

Cell membranes are selectively permeable. The equilibrium potential for ion $X$ across a membrane:

$$
E_X = \frac{RT}{z_X F}\ln\frac{[X]_{\text{outside}}}{[X]_{\text{inside}}}
$$

For K⁺ in a neuron: $[K^+]_{\text{out}} = 5\,\text{mM}$, $[K^+]_{\text{in}} = 140\,\text{mM}$:

$$
E_K = \frac{0.05916}{1}\log\frac{5}{140} = -0.05916 \times 1.45 = -86\,\text{mV}
$$

This is close to the resting membrane potential (~-70 mV), confirming that K⁺ permeability dominates at rest. See [02 - Biology](02---Biology) for the full Goldman equation with multiple ions.

### Appendix D — Electrochemical Energy Storage Comparison

| Technology | Voltage (V) | Energy Density (Wh/kg) | Cycle Life | Cost ($/kWh) | Application |
|---|---|---|---|---|---|
| Lead-acid | 2.0 | 35 | 500 | 100 | Car starting, UPS |
| NiMH | 1.2 | 80 | 1000 | 300 | Hybrid vehicles |
| Li-ion (NMC) | 3.7 | 250 | 1000 | 150 | Phones, EVs |
| Li-ion (LFP) | 3.2 | 160 | 3000 | 120 | EVs, grid storage |
| Na-ion | 3.1 | 160 | 2000 | 80 | Grid storage |
| Solid-state Li | 3.8 | 400+ | 1000+ | 200+ | Future EVs |
| Li-S | 2.1 | 500+ | 500 | — | Research |
| Zn-air | 1.6 | 400 | 100 | 50 | Hearing aids |
| Flow (vanadium) | 1.4 | 25 | 10000+ | 300 | Grid storage |

**The energy density hierarchy explained by electrochemistry:**
- Higher voltage → more energy per electron (Li has the most negative $E^\circ$)
- Lighter elements → more electrons per gram (Li: 3860 mAh/g theoretical vs Pb: 259 mAh/g)
- Stable electrolyte window → can use full voltage range without decomposition

```python
import numpy as np

def nernst(E_standard, n, Q, T=298.15):
    """Calculate cell potential using Nernst equation."""
    F = 96485  # C/mol
    R = 8.314  # J/(mol*K)
    return E_standard - (R * T) / (n * F) * np.log(Q)

def faraday_mass(I, t, M, n):
    """Calculate mass deposited by electrolysis (Faraday's law)."""
    F = 96485
    return I * t * M / (n * F)

def battery_energy(voltage, capacity_Ah, mass_kg):
    """Calculate specific energy of a battery."""
    return voltage * capacity_Ah / mass_kg  # Wh/kg

# Example: How does Daniell cell voltage change as reaction proceeds?
E_std = 1.10  # V
# As Zn dissolves and Cu deposits: [Zn2+] increases, [Cu2+] decreases
ratios = np.logspace(-3, 3, 100)  # [Zn2+]/[Cu2+]
E_values = nernst(E_std, 2, ratios)

print("Daniell Cell voltage vs. concentration ratio:")
print(f"  [Zn2+]/[Cu2+] = 0.001: E = {nernst(E_std, 2, 0.001):.4f} V")
print(f"  [Zn2+]/[Cu2+] = 1.0:   E = {nernst(E_std, 2, 1.0):.4f} V")
print(f"  [Zn2+]/[Cu2+] = 1000:  E = {nernst(E_std, 2, 1000):.4f} V")
print(f"  At equilibrium (E=0):   Q = 10^(2*1.10/0.05916) = {10**(2*1.10/0.05916):.2e}")
```

> [!danger] 🧠 Common Misconceptions — Section 8 & 9 Summary
> 
> **❌ "Electrons flow from anode to cathode through the solution"**
> **Truth:** Electrons flow through the EXTERNAL circuit (wire) from anode to cathode. In solution, current is carried by IONS (cations move toward cathode, anions toward anode). The salt bridge completes the circuit by allowing ion migration.
> 
> **❌ "You multiply E° by the number of electrons when combining half-reactions"**
> **Truth:** NEVER multiply E° by n. Cell potential is an intensive property (energy per electron, like voltage). Only ΔG° (= -nFE°) is extensive. When combining half-reactions, add the ΔG° values, then convert back to E°.
> 
> **❌ "Electrolysis is just the reverse of a galvanic cell"**
> **Truth:** Electrolysis requires MORE voltage than E°cell due to overpotential (activation barriers at electrodes). Water electrolysis needs ~1.8 V in practice, not the theoretical 1.23 V. The extra 0.6 V is wasted as heat.
> 
> **❌ "Lithium-ion batteries contain lithium metal"**
> **Truth:** Standard Li-ion batteries contain NO metallic lithium. Li exists as Li⁺ ions intercalated in graphite (anode) or metal oxide (cathode). Lithium METAL anodes are a different (next-gen) technology with safety challenges.
> 
> **❌ "Corrosion only happens in salt water"**
> **Truth:** Any aqueous environment with dissolved oxygen causes iron corrosion. Pure water, acidic rain, even humid air. Salt accelerates corrosion by increasing solution conductivity (ions carry current between anodic and cathodic sites), but it's not required.
> 
> **❌ "A more negative E° means a stronger reducing agent"**
> **Truth:** This IS correct — but students often confuse the direction. A species with very negative E° (like Li, -3.04 V) is easily OXIDIZED (loses electrons easily) → strong reducing agent. A species with very positive E° (like F₂, +2.87 V) is easily REDUCED (gains electrons easily) → strong oxidizing agent.

---

*Previous: [03.5 - Acids, Bases & Equilibrium](03.5---Acids,-Bases-&-Equilibrium) | Next: [03.7 - Organic Chemistry Foundations](03.7---Organic-Chemistry-Foundations)*
