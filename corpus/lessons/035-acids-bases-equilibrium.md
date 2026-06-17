---
title: "03.5 — Acids, Bases & Equilibrium"
subject: "Chemistry"
catalog: advanced
audience_tier: higher-education
chapter: "03.5"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 03.5 — Acids, Bases & Equilibrium

> *"The equilibrium constant is the partition function ratio — nothing more, nothing less."* — Statistical mechanics perspective

> *"An acid is a proton donor; a base is a proton acceptor."* — Brønsted & Lowry, 1923

Chemical equilibrium is where thermodynamics meets chemistry most directly. The equilibrium constant $K$ is not an empirical number — it's derivable from the molecular partition functions you computed in [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy). This chapter connects that statistical mechanics foundation to the practical chemistry of acids, bases, buffers, and solubility.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Derive the equilibrium constant $K$ from the partition function ratio (statistical mechanics route).
2. Write equilibrium expressions and calculate $K$ from concentration data.
3. Apply Le Chatelier's principle to predict equilibrium shifts.
4. Calculate pH of strong acids/bases, weak acids/bases, and buffer solutions.
5. Derive and apply the Henderson-Hasselbalch equation.
6. Solve solubility equilibrium problems ($K_{sp}$).
7. Perform ICE table calculations for any equilibrium system.

---

## 🖼️ Visual Anchor — Equilibrium as Free Energy Minimum

![chem-03__fig3](chem-03__fig3.svg)

---

## 📚 1. Definitions

### Definition 03.5.1 — Chemical Equilibrium

A dynamic state where the forward and reverse reaction rates are equal, so macroscopic concentrations remain constant. NOT a static state — reactions continue in both directions.

### Definition 03.5.2 — Equilibrium Constant ($K$)

For the reaction $aA + bB \rightleftharpoons cC + dD$:

$$
K = \frac{[C]^c[D]^d}{[A]^a[B]^b} \quad \text{(at equilibrium)}
$$

$K$ depends only on temperature (not on initial concentrations).

### Definition 03.5.3 — Reaction Quotient ($Q$)

Same expression as $K$, but evaluated at ANY point (not necessarily equilibrium):

$$
Q = \frac{[C]^c[D]^d}{[A]^a[B]^b} \quad \text{(at any time)}
$$

- $Q < K$: reaction proceeds forward
- $Q = K$: at equilibrium
- $Q > K$: reaction proceeds in reverse

### Definition 03.5.4 — Brønsted-Lowry Acid and Base

- **Acid:** proton (H⁺) donor
- **Base:** proton acceptor
- **Conjugate acid-base pair:** differ by one proton (e.g., CH₃COOH / CH₃COO⁻)

### Definition 03.5.5 — pH and pOH

$$
\text{pH} = -\log_{10}[H^+], \quad \text{pOH} = -\log_{10}[OH^-], \quad \text{pH} + \text{pOH} = 14 \text{ (at 25°C)}
$$

### Definition 03.5.6 — $K_a$ and $K_b$ (Acid/Base Dissociation Constants)

For a weak acid HA: $\text{HA} \rightleftharpoons \text{H}^+ + \text{A}^-$

$$
K_a = \frac{[\text{H}^+][\text{A}^-]}{[\text{HA}]}
$$

For a weak base B: $\text{B} + \text{H}_2\text{O} \rightleftharpoons \text{BH}^+ + \text{OH}^-$

$$
K_b = \frac{[\text{BH}^+][\text{OH}^-]}{[\text{B}]}
$$

Relationship: $K_a \times K_b = K_w = 1.0 \times 10^{-14}$ (at 25°C).

### Definition 03.5.7 — Buffer Solution

A solution that resists pH changes upon addition of small amounts of acid or base. Contains a weak acid and its conjugate base (or weak base and conjugate acid) in comparable concentrations.

### Definition 03.5.8 — Solubility Product ($K_{sp}$)

For a sparingly soluble salt $M_mA_n \rightleftharpoons mM^{n+} + nA^{m-}$:

$$
K_{sp} = [M^{n+}]^m[A^{m-}]^n
$$

---

## 📐 2. Mathematical Foundations

### 2.1 Deriving $K$ from the Partition Function (The Statistical Mechanics Route)

For the gas-phase reaction $A \rightleftharpoons B$, the equilibrium condition minimizes the Gibbs free energy. From [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy):

$$
\mu_A = \mu_A^\circ + RT\ln\frac{P_A}{P^\circ}, \quad \mu_B = \mu_B^\circ + RT\ln\frac{P_B}{P^\circ}
$$

At equilibrium: $\mu_A = \mu_B$, so:

$$
\mu_B^\circ - \mu_A^\circ = -RT\ln\frac{P_B}{P_A} = -RT\ln K_P
$$

The standard chemical potential is related to the molecular partition function:

$$
\mu^\circ = -RT\ln\frac{q^\circ}{N_A}
$$

where $q^\circ$ is the molecular partition function at standard pressure. Therefore:

$$
K = \frac{q_B^\circ/N_A}{q_A^\circ/N_A}\,e^{-\Delta\epsilon_0/(k_BT)} = \frac{q_B^\circ}{q_A^\circ}\,e^{-\Delta\epsilon_0/(k_BT)}
$$

**The equilibrium constant IS the ratio of partition functions** (weighted by the ground-state energy difference). This is the deepest understanding of equilibrium — it's just the Boltzmann distribution applied to molecular species.

### 2.2 The Relationship $\Delta G^\circ = -RT\ln K$

From the derivation above:

$$
\Delta G^\circ = -RT\ln K
$$

| $\Delta G^\circ$ | $K$ | Meaning |
|---|---|---|
| $\ll 0$ | $\gg 1$ | Products strongly favored |
| $= 0$ | $= 1$ | Neither favored |
| $\gg 0$ | $\ll 1$ | Reactants strongly favored |

### 2.3 The Henderson-Hasselbalch Equation

For a buffer (weak acid HA with conjugate base A⁻):

Starting from $K_a = \frac{[\text{H}^+][\text{A}^-]}{[\text{HA}]}$:

$$
[\text{H}^+] = K_a\frac{[\text{HA}]}{[\text{A}^-]}
$$

Taking $-\log_{10}$:

$$
\boxed{\text{pH} = \text{p}K_a + \log\frac{[\text{A}^-]}{[\text{HA}]}}
$$

When $[\text{A}^-] = [\text{HA}]$: pH = p$K_a$ (the buffer's optimal pH).

### 2.4 ICE Table Method

For any equilibrium problem:

| | Reactant | Product |
|---|---|---|
| **I**nitial | $C_0$ | 0 |
| **C**hange | $-x$ | $+x$ |
| **E**quilibrium | $C_0 - x$ | $x$ |

Substitute into the $K$ expression and solve for $x$.

### 2.5 The Quadratic Formula in Equilibrium

For a weak acid HA with initial concentration $C_0$:

$$
K_a = \frac{x^2}{C_0 - x}
$$

If $x \ll C_0$ (the 5% approximation): $x \approx \sqrt{K_a C_0}$.

Otherwise, solve the full quadratic: $x^2 + K_a x - K_a C_0 = 0$.

$$
x = \frac{-K_a + \sqrt{K_a^2 + 4K_a C_0}}{2}
$$

---

## 🔬 3. Chemical Mechanisms

### 3.1 Le Chatelier's Principle

When a system at equilibrium is disturbed, it shifts to partially counteract the disturbance:

| Disturbance | Shift Direction | Explanation |
|---|---|---|
| Add reactant | → (toward products) | System consumes added reactant |
| Remove product | → (toward products) | System makes more product |
| Increase pressure | Toward fewer moles of gas | Reduces total moles to lower pressure |
| Increase temperature | Toward endothermic direction | Absorbs added heat |
| Add catalyst | No shift | Speeds both directions equally |

**The statistical mechanics explanation:** Le Chatelier's principle is just the system re-minimizing $G$ after a perturbation. Adding reactant increases $Q$ below $K$, so the forward reaction is thermodynamically favored until $Q = K$ again.

### 3.2 Strong vs Weak Acids/Bases

**Strong acids** (HCl, HNO₃, H₂SO₄, HBr, HI, HClO₄): dissociate completely. pH = $-\log C_0$.

**Weak acids** (CH₃COOH, HF, H₂CO₃): partially dissociate. Must solve equilibrium.

**Strong bases** (NaOH, KOH, Ca(OH)₂): dissociate completely. pOH = $-\log C_0$.

**Weak bases** (NH₃, amines): partially accept protons. Must solve equilibrium.

### 3.3 Polyprotic Acids

Acids with multiple ionizable protons (H₂SO₄, H₃PO₄, H₂CO₃) have successive $K_a$ values:

$$
K_{a1} \gg K_{a2} \gg K_{a3}
$$

Each successive proton is harder to remove (the anion holds remaining protons more tightly). For pH calculations, usually only $K_{a1}$ matters significantly.

---

## ✍️ 4. Worked Examples

### Example 03.5.1 — pH of a Weak Acid

**Problem:** Calculate the pH of 0.100 M acetic acid ($K_a = 1.8 \times 10^{-5}$).

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Write the equilibrium.

$$
\text{CH}_3\text{COOH} \rightleftharpoons \text{H}^+ + \text{CH}_3\text{COO}^-
$$

**Step 2:** ICE table.

| | CH₃COOH | H⁺ | CH₃COO⁻ |
|---|---|---|---|
| I | 0.100 | 0 | 0 |
| C | $-x$ | $+x$ | $+x$ |
| E | $0.100 - x$ | $x$ | $x$ |

**Step 3:** Substitute into $K_a$.

$$
1.8 \times 10^{-5} = \frac{x^2}{0.100 - x}
$$

**Step 4:** Try the 5% approximation ($x \ll 0.100$):

$$
x \approx \sqrt{1.8 \times 10^{-5} \times 0.100} = \sqrt{1.8 \times 10^{-6}} = 1.34 \times 10^{-3}
$$

Check: $x/C_0 = 1.34\%$ < 5%. ✓ Approximation valid.

**Step 5:** Calculate pH.

$$
\text{pH} = -\log(1.34 \times 10^{-3}) = 2.87
$$

**Comparison:** A strong acid at 0.100 M would have pH = 1.00. The weak acid is much less acidic because only 1.3% of molecules dissociate.

</details>

---

### Example 03.5.2 — Buffer pH and Buffer Capacity

**Problem:** A buffer is made from 0.200 M CH₃COOH and 0.150 M CH₃COONa ($K_a = 1.8 \times 10^{-5}$). (a) Calculate the pH. (b) What happens when 0.010 mol HCl is added to 1.00 L of this buffer?

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Part (a):** Henderson-Hasselbalch.

$$
\text{pH} = \text{p}K_a + \log\frac{[\text{A}^-]}{[\text{HA}]} = 4.74 + \log\frac{0.150}{0.200} = 4.74 + (-0.125) = 4.62
$$

**Part (b):** Adding 0.010 mol HCl to 1.00 L.

The HCl reacts with the conjugate base: $\text{H}^+ + \text{CH}_3\text{COO}^- \to \text{CH}_3\text{COOH}$

New concentrations:
- $[\text{A}^-] = 0.150 - 0.010 = 0.140$ M
- $[\text{HA}] = 0.200 + 0.010 = 0.210$ M

New pH:

$$
\text{pH} = 4.74 + \log\frac{0.140}{0.210} = 4.74 + (-0.176) = 4.56
$$

**pH change:** $4.62 - 4.56 = 0.06$ units. Tiny!

**Without buffer:** Adding 0.010 mol HCl to 1.00 L of pure water would give pH = 2.00 (a change of 5 units). The buffer resists the pH change by converting A⁻ to HA, consuming the added H⁺.

</details>

---

### Example 03.5.3 — Solubility Equilibrium

**Problem:** Calculate the molar solubility of PbCl₂ ($K_{sp} = 1.7 \times 10^{-5}$) in (a) pure water and (b) 0.10 M NaCl solution.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Part (a): Pure water.**

$$
\text{PbCl}_2 \rightleftharpoons \text{Pb}^{2+} + 2\text{Cl}^-
$$

Let solubility = $s$. Then $[\text{Pb}^{2+}] = s$ and $[\text{Cl}^-] = 2s$.

$$
K_{sp} = s(2s)^2 = 4s^3 = 1.7 \times 10^{-5}
$$

$$
s = \left(\frac{1.7 \times 10^{-5}}{4}\right)^{1/3} = (4.25 \times 10^{-6})^{1/3} = 0.016 \text{ M}
$$

**Part (b): In 0.10 M NaCl (common ion effect).**

Now $[\text{Cl}^-] = 2s + 0.10 \approx 0.10$ (since $s$ will be small).

$$
K_{sp} = s(0.10)^2 = 0.010\,s = 1.7 \times 10^{-5}
$$

$$
s = \frac{1.7 \times 10^{-5}}{0.010} = 1.7 \times 10^{-3} \text{ M}
$$

**The common ion effect:** Solubility decreased from 0.016 M to 0.0017 M — a factor of ~10. The presence of Cl⁻ from NaCl shifts the equilibrium LEFT (Le Chatelier), suppressing dissolution.

</details>

---

### Example 03.5.4 — Deriving $K$ from Partition Functions

**Problem:** For the gas-phase reaction $\text{H}_2 \rightleftharpoons 2\text{H}$ at 3000 K, estimate $K$ given that the dissociation energy is $D_0 = 432$ kJ/mol and the ratio of partition functions per unit volume is $q_H^2/q_{H_2} \approx 10^{-3}$ at this temperature.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** The statistical mechanics expression for $K$:

$$
K = \frac{(q_H^\circ)^2}{q_{H_2}^\circ}\,e^{-D_0/(RT)}
$$

**Step 2:** Calculate the Boltzmann factor.

$$
\frac{D_0}{RT} = \frac{432000}{8.314 \times 3000} = 17.3
$$

$$
e^{-17.3} = 3.0 \times 10^{-8}
$$

**Step 3:** Combine with partition function ratio.

$$
K \approx 10^{-3} \times 3.0 \times 10^{-8} = 3 \times 10^{-11}
$$

**Interpretation:** Even at 3000 K, $K$ is tiny — H₂ barely dissociates. The bond energy is so large that the Boltzmann factor overwhelms the entropy gain from dissociation (more translational states for 2 atoms vs 1 molecule).

At higher temperatures, the exponential factor grows and eventually $K \gt  1$ (H₂ fully dissociates in stellar atmospheres at ~5000+ K).

</details>

---

## 🧠 5. Connections to Other Tracks

| This Chapter | Connects To | How |
|---|---|---|
| $K$ from partition functions | [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy) | $K = q_{\text{prod}}/q_{\text{react}} \times e^{-\Delta\epsilon_0/k_BT}$ |
| $\Delta G^\circ = -RT\ln K$ | [5.3 - Thermodynamic Potentials & Maxwell Relations](5.3---Thermodynamic-Potentials-&-Maxwell-Relations) | Free energy minimization |
| Le Chatelier | [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy) | Re-minimizing $G$ after perturbation |
| pH calculations | [1.1 - Foundations of Calculus & Real Analysis](1.1---Foundations-of-Calculus-&-Real-Analysis) | Logarithms, quadratic formula |
| Buffer chemistry | [03.8 - Biochemistry & Modern Topics](03.8---Biochemistry-&-Modern-Topics) | Biological pH regulation |
| Solubility | [03.6 - Electrochemistry & Redox](03.6---Electrochemistry-&-Redox) | Precipitation in electrochemistry |

---

## ⚠️ 6. Common Misconceptions & Where Most Students Fail

### ❌ Misconception 1: "Equilibrium means equal concentrations"

**The truth:** Equilibrium means equal RATES (forward = reverse), not equal concentrations. If $K = 10^6$, products dominate overwhelmingly at equilibrium. If $K = 10^{-6}$, reactants dominate.

### ❌ Misconception 2: "A large $K$ means the reaction is fast"

**The truth:** $K$ tells you WHERE equilibrium lies (thermodynamics). It says nothing about HOW FAST you get there (kinetics). Diamond → graphite has $K \gg 1$ but takes geological time.

### ❌ Misconception 3: "pH 7 is always neutral"

**The truth:** pH 7 is neutral only at 25°C (where $K_w = 10^{-14}$). At 37°C (body temperature), $K_w = 2.4 \times 10^{-14}$, so neutral pH = 6.8. At 100°C, neutral pH ≈ 6.14.

### ❌ Misconception 4: "You can't have pH < 0 or pH > 14"

**The truth:** pH is just $-\log[\text{H}^+]$. Concentrated HCl (12 M) has $[\text{H}^+] \approx 12$ M, giving pH ≈ $-1.1$. Concentrated NaOH can give pH > 14. The 0–14 scale is just the range for dilute aqueous solutions.

### ❌ Misconception 5: "The 5% approximation always works for weak acids"

**The truth:** It fails when $K_a$ is large relative to $C_0$ (dilute weak acid or moderately strong acid). Always CHECK: if $x/C_0 > 5\%$, use the quadratic formula. For very dilute solutions, you may even need to include the autoionization of water.

### 💪 The Pep Talk

Equilibrium is where most students feel chemistry becomes "too much math." ICE tables, quadratics, logarithms, multiple equilibria... it feels overwhelming. But here's the secret: **every equilibrium problem is the same algorithm.**

1. Write the balanced equation
2. Write the $K$ expression
3. Set up the ICE table
4. Substitute and solve

That's it. The "hard" part is just algebra — and you've been doing harder algebra in linear algebra and differential equations for months. The chemistry is just choosing which $K$ expression to write.

And remember: $K$ is not a magic number. It's the partition function ratio. It's the Boltzmann distribution applied to molecules. You already understand WHY equilibrium exists — now you're just learning to calculate with it.

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy) — Statistical derivation of $K$
- [03.4 - Thermodynamics & Kinetics](03.4---Thermodynamics-&-Kinetics) — $\Delta G^\circ = -RT\ln K$
- [03.6 - Electrochemistry & Redox](03.6---Electrochemistry-&-Redox) — Nernst equation uses equilibrium concepts
- [03.8 - Biochemistry & Modern Topics](03.8---Biochemistry-&-Modern-Topics) — Biological buffers and enzyme kinetics

### External References
- **MIT 5.111 OCW** — Lectures 21–26: Equilibrium and acid-base chemistry
- **Khan Academy** — [Chemical equilibrium](https://www.khanacademy.org/science/chemistry/chemical-equilibrium) and [Acids and bases](https://www.khanacademy.org/science/chemistry/acids-and-bases-topic)
- **Crash Course Chemistry** — Episodes 28–33: Equilibrium, acids, bases
- **Atkins, P.** — *Physical Chemistry*, Chapters 5–6 (equilibrium)

---

## 🔬 8. Advanced Derivations — Equilibrium Mastery

### 8.1 — Henderson-Hasselbalch: Full Derivation and Limitations

**Starting point:** The acid dissociation equilibrium:

$$
\text{HA} \rightleftharpoons \text{H}^+ + \text{A}^-
$$

$$
K_a = \frac{[\text{H}^+][\text{A}^-]}{[\text{HA}]}
$$

**Step 1:** Solve for $[\text{H}^+]$:

$$
[\text{H}^+] = K_a\frac{[\text{HA}]}{[\text{A}^-]}
$$

**Step 2:** Take $-\log_{10}$ of both sides:

$$
-\log[\text{H}^+] = -\log K_a - \log\frac{[\text{HA}]}{[\text{A}^-]}
$$

$$
\text{pH} = \text{p}K_a - \log\frac{[\text{HA}]}{[\text{A}^-]} = \text{p}K_a + \log\frac{[\text{A}^-]}{[\text{HA}]}
$$

**This is the Henderson-Hasselbalch equation:**

$$
\boxed{\text{pH} = \text{p}K_a + \log\frac{[\text{A}^-]}{[\text{HA}]}}
$$

**Assumptions (when it's valid):**
1. The solution is a buffer (both HA and A⁻ present in significant amounts).
2. $[\text{A}^-]$ and $[\text{HA}]$ are not significantly changed by the equilibrium (i.e., $x \ll C$).
3. Water autoionization is negligible compared to buffer concentrations.

**When Henderson-Hasselbalch FAILS:**
- Very dilute buffers ($C < 10^{-3}\,\text{M}$): water autoionization matters
- pH far from pKa ($|$pH $-$ pKa$| > 2$): one species is negligible
- Very strong acids/bases: complete dissociation, no equilibrium

**The exact equation** (no approximations):

$$
[\text{H}^+]^3 + (K_a + C_b)[\text{H}^+]^2 + (K_a C_b - K_a C_a - K_w)[\text{H}^+] - K_a K_w = 0
$$

where $C_a$ = analytical concentration of acid, $C_b$ = analytical concentration of conjugate base. This cubic always has one physically meaningful root.

### 8.2 — Buffer Capacity: Quantitative Treatment

**Buffer capacity** $\beta$ measures how much strong acid or base a buffer can absorb per unit pH change:

$$
\beta = \frac{dC_b}{d(\text{pH})} = -\frac{dC_a}{d(\text{pH})}
$$

where $C_b$ = moles of strong base added per liter.

**Derivation:**

From the proton balance for a buffer with total concentration $C = [\text{HA}] + [\text{A}^-]$:

$$
C_b = [\text{A}^-] + [\text{OH}^-] - [\text{H}^+] = \frac{CK_a}{[\text{H}^+] + K_a} + \frac{K_w}{[\text{H}^+]} - [\text{H}^+]
$$

Differentiating with respect to pH (using $d[\text{H}^+] = -2.303[\text{H}^+]\,d(\text{pH})$):

$$
\beta = 2.303\left[\frac{CK_a[\text{H}^+]}{([\text{H}^+] + K_a)^2} + [\text{H}^+] + \frac{K_w}{[\text{H}^+]}\right]
$$

**Simplification for a good buffer** (middle term dominates):

$$
\beta \approx 2.303\,C\,\frac{K_a[\text{H}^+]}{([\text{H}^+] + K_a)^2} = 2.303\,C\,\alpha(1-\alpha)
$$

where $\alpha = [\text{A}^-]/C$ is the fraction dissociated.

**Maximum buffer capacity** occurs at pH = pKa (where $\alpha = 0.5$):

$$
\beta_{\max} = 2.303 \times C \times 0.25 = 0.576\,C
$$

**Practical rule:** A buffer is effective within pH = pKa ± 1 (where $\beta > 0.1\,\beta_{\max}$).

**Worked Example — Phosphate buffer for biological work:**

Design a buffer at pH 7.4 using the H₂PO₄⁻/HPO₄²⁻ system ($\text{p}K_{a2} = 7.21$).

$$
\text{pH} = 7.21 + \log\frac{[\text{HPO}_4^{2-}]}{[\text{H}_2\text{PO}_4^-]}
$$

$$
7.4 = 7.21 + \log\frac{[\text{HPO}_4^{2-}]}{[\text{H}_2\text{PO}_4^-]}
$$

$$
\log\frac{[\text{HPO}_4^{2-}]}{[\text{H}_2\text{PO}_4^-]} = 0.19 \Rightarrow \frac{[\text{HPO}_4^{2-}]}{[\text{H}_2\text{PO}_4^-]} = 1.55
$$

For a 0.1 M total phosphate buffer: $[\text{HPO}_4^{2-}] = 0.061\,\text{M}$, $[\text{H}_2\text{PO}_4^-] = 0.039\,\text{M}$.

Buffer capacity: $\beta = 2.303 \times 0.1 \times \frac{1.55}{(1 + 1.55)^2} = 0.055\,\text{mol/(L·pH unit)}$

This means adding 0.055 mol of HCl to 1 L of this buffer changes pH by only 1 unit.

### 8.3 — ICE Tables: The Systematic Method for Any Equilibrium

**ICE = Initial, Change, Equilibrium.** This is the universal method for solving equilibrium problems.

**Worked Example — Weak acid dissociation:**

Calculate the pH of 0.250 M formic acid ($K_a = 1.8 \times 10^{-4}$).

|  | HCOOH | H⁺ | HCOO⁻ |
|---|---|---|---|
| **I** | 0.250 | 0 | 0 |
| **C** | $-x$ | $+x$ | $+x$ |
| **E** | $0.250 - x$ | $x$ | $x$ |

$$
K_a = \frac{x^2}{0.250 - x} = 1.8 \times 10^{-4}
$$

**Check if approximation valid:** $C/K_a = 0.250/(1.8 \times 10^{-4}) = 1389 > 400$ ✓ (can neglect $x$ in denominator)

$$
x^2 \approx 1.8 \times 10^{-4} \times 0.250 = 4.5 \times 10^{-5}
$$

$$
x = 6.71 \times 10^{-3}\,\text{M}
$$

**Verify:** $x/C = 6.71 \times 10^{-3}/0.250 = 2.7\%$ — less than 5%, approximation valid.

$$
\text{pH} = -\log(6.71 \times 10^{-3}) = 2.17
$$

**When the approximation fails** ($C/K_a < 400$): Use the quadratic formula:

$$
x^2 + K_a x - K_a C = 0
$$

$$
x = \frac{-K_a + \sqrt{K_a^2 + 4K_a C}}{2}
$$

### 8.4 — Titration of Polyprotic Acids: Complete Analysis

**Sulfuric acid (H₂SO₄):** $K_{a1} \to \infty$ (strong first dissociation), $K_{a2} = 1.2 \times 10^{-2}$

The first proton is completely donated. The second proton is a weak acid:

$$
\text{HSO}_4^- \rightleftharpoons \text{H}^+ + \text{SO}_4^{2-}, \quad K_{a2} = 0.012
$$

For 0.100 M H₂SO₄: After first dissociation, $[\text{H}^+] = 0.100\,\text{M}$ and $[\text{HSO}_4^-] = 0.100\,\text{M}$.

ICE for second dissociation:

|  | HSO₄⁻ | H⁺ | SO₄²⁻ |
|---|---|---|---|
| **I** | 0.100 | 0.100 | 0 |
| **C** | $-x$ | $+x$ | $+x$ |
| **E** | $0.100-x$ | $0.100+x$ | $x$ |

$$
0.012 = \frac{(0.100 + x)(x)}{0.100 - x}
$$

Solving (quadratic needed since $K_{a2}$ is not small compared to $C$):

$$
x^2 + 0.112x - 0.0012 = 0
$$

$$
x = \frac{-0.112 + \sqrt{0.01254 + 0.0048}}{2} = \frac{-0.112 + 0.131}{2} = 0.0099
$$

$$
[\text{H}^+] = 0.100 + 0.0099 = 0.110\,\text{M}, \quad \text{pH} = 0.96
$$

**Key insight:** The second dissociation of H₂SO₄ contributes only ~10% more H⁺. For dilute H₂SO₄ ($< 0.01\,\text{M}$), the second dissociation becomes more significant.

### 8.5 — Pourbaix Diagrams: Electrochemistry Meets Acid-Base

A **Pourbaix diagram** (E-pH diagram) maps the thermodynamically stable species of an element as a function of both electrode potential $E$ and pH. It combines:
- Acid-base equilibria (horizontal boundaries — pH-dependent, E-independent)
- Redox equilibria (vertical boundaries — E-dependent, pH-independent)
- Combined equilibria (diagonal boundaries — both E and pH dependent)

**Construction for Iron (Fe):**

**Boundary 1:** Fe²⁺/Fe (reduction, pH-independent):

$$
\text{Fe}^{2+} + 2e^- \to \text{Fe}(s), \quad E^\circ = -0.44\,\text{V}
$$

$$
E = -0.44 + \frac{0.0592}{2}\log[\text{Fe}^{2+}]
$$

At $[\text{Fe}^{2+}] = 10^{-6}\,\text{M}$: $E = -0.44 + 0.0296\log(10^{-6}) = -0.62\,\text{V}$ (horizontal line)

**Boundary 2:** Fe²⁺/Fe(OH)₂ (precipitation, E-independent):

$$
\text{Fe}^{2+} + 2\text{OH}^- \to \text{Fe(OH)}_2, \quad K_{sp} = 4.87 \times 10^{-17}
$$

At $[\text{Fe}^{2+}] = 10^{-6}\,\text{M}$:

$$
[\text{OH}^-] = \sqrt{\frac{K_{sp}}{[\text{Fe}^{2+}]}} = \sqrt{\frac{4.87 \times 10^{-17}}{10^{-6}}} = 2.21 \times 10^{-5.5}
$$

$$
\text{pOH} = 5.5, \quad \text{pH} = 8.5 \quad \text{(vertical line)}
$$

**Boundary 3:** Fe²⁺/Fe³⁺ (redox, pH-independent):

$$
\text{Fe}^{3+} + e^- \to \text{Fe}^{2+}, \quad E^\circ = +0.77\,\text{V}
$$

**Boundary 4:** Fe³⁺/Fe(OH)₃ (combined — diagonal):

$$
\text{Fe(OH)}_3 + 3\text{H}^+ + e^- \to \text{Fe}^{2+} + 3\text{H}_2\text{O}
$$

$$
E = E^\circ - \frac{0.0592}{1}(3\,\text{pH}) = 1.06 - 0.178\,\text{pH}
$$

**Reading the diagram:**
- Below the Fe/Fe²⁺ line: metallic iron is stable (immunity zone — no corrosion)
- In the Fe²⁺ region: iron dissolves (corrosion zone)
- In the Fe(OH)₂/Fe(OH)₃ region: protective oxide forms (passivation zone)

**Practical application:** Pourbaix diagrams tell engineers:
- At what pH and potential iron corrodes (and how to prevent it)
- Why stainless steel is "stainless" (Cr₂O₃ passivation layer is stable over a wide E-pH range)
- How to design cathodic protection systems

Cross-link: [03.6 - Electrochemistry & Redox](03.6---Electrochemistry-&-Redox) for the Nernst equation used in boundary calculations.

### 8.6 — Complex-Ion Equilibria: Formation Constants

Metal ions in solution form coordination complexes with ligands. The stability is quantified by **formation constants** $K_f$ (also called stability constants).

**Stepwise formation:**

$$
\text{Cu}^{2+} + \text{NH}_3 \rightleftharpoons [\text{Cu(NH}_3)]^{2+}, \quad K_1 = 2.0 \times 10^4
$$

$$
[\text{Cu(NH}_3)]^{2+} + \text{NH}_3 \rightleftharpoons [\text{Cu(NH}_3)_2]^{2+}, \quad K_2 = 4.7 \times 10^3
$$

$$
[\text{Cu(NH}_3)_2]^{2+} + \text{NH}_3 \rightleftharpoons [\text{Cu(NH}_3)_3]^{2+}, \quad K_3 = 1.1 \times 10^3
$$

$$
[\text{Cu(NH}_3)_3]^{2+} + \text{NH}_3 \rightleftharpoons [\text{Cu(NH}_3)_4]^{2+}, \quad K_4 = 2.0 \times 10^2
$$

**Overall formation constant:**

$$
\beta_4 = K_1 K_2 K_3 K_4 = 2.0 \times 10^4 \times 4.7 \times 10^3 \times 1.1 \times 10^3 \times 2.0 \times 10^2 = 2.1 \times 10^{13}
$$

**Trend:** $K_1 > K_2 > K_3 > K_4$ (statistical effect — fewer available coordination sites + steric crowding).

**Application — dissolving insoluble salts:**

AgCl is insoluble ($K_{sp} = 1.8 \times 10^{-10}$), but dissolves in excess NH₃:

$$
\text{AgCl}(s) + 2\text{NH}_3 \rightleftharpoons [\text{Ag(NH}_3)_2]^+ + \text{Cl}^-
$$

$$
K = K_{sp} \times \beta_2 = 1.8 \times 10^{-10} \times 1.1 \times 10^7 = 2.0 \times 10^{-3}
$$

At $[\text{NH}_3] = 1.0\,\text{M}$: $[\text{Ag}^+]_{\text{total}} = K \times [\text{NH}_3]^2 / [\text{Cl}^-] \approx 0.045\,\text{M}$ — AgCl dissolves!

This is why adding NH₃ to a AgCl precipitate dissolves it — the complex formation pulls the dissolution equilibrium forward (Le Chatelier).

> [!tip] Cross-link to Track 15 (Biology)
> Buffer systems are critical in biology: blood pH (7.35–7.45) is maintained by the bicarbonate buffer, phosphate buffer, and protein buffers. Enzyme activity depends critically on pH — most enzymes have a narrow pH optimum. See [02 - Biology](02---Biology) for the physiological integration.

## 📎 9. Appendix — Deep Dives & Mastery Challenges

### Appendix A — The Exact Solution for Weak Acid pH (No Approximations)

For a weak acid HA at concentration $C$ with dissociation constant $K_a$, the exact proton balance is:

$$
[\text{H}^+] = [\text{A}^-] + [\text{OH}^-]
$$

Combined with $K_a = [\text{H}^+][\text{A}^-]/[\text{HA}]$ and $[\text{HA}] + [\text{A}^-] = C$:

$$
[\text{H}^+]^3 + K_a[\text{H}^+]^2 - (K_w + K_a C)[\text{H}^+] - K_a K_w = 0
$$

```python
import numpy as np

def exact_weak_acid_pH(C, Ka, Kw=1e-14):
    """
    Solve the exact cubic equation for weak acid pH.
    No approximations — works for any concentration and Ka.
    """
    # Coefficients of cubic: x^3 + a*x^2 + b*x + c = 0
    # where x = [H+]
    coeffs = [1, Ka, -(Kw + Ka*C), -Ka*Kw]
    roots = np.roots(coeffs)
    
    # Find the real, positive root
    real_roots = roots[np.isreal(roots)].real
    positive_roots = real_roots[real_roots > 0]
    H_plus = positive_roots[0]
    
    return -np.log10(H_plus)

# Test cases
print("=== Exact pH calculations ===")
print(f"0.1 M acetic acid (Ka=1.8e-5): pH = {exact_weak_acid_pH(0.1, 1.8e-5):.4f}")
print(f"1e-7 M acetic acid (very dilute): pH = {exact_weak_acid_pH(1e-7, 1.8e-5):.4f}")
print(f"0.1 M HF (Ka=6.8e-4): pH = {exact_weak_acid_pH(0.1, 6.8e-4):.4f}")
print(f"1e-8 M HCl (ultra-dilute strong acid): pH = {exact_weak_acid_pH(1e-8, 1e10):.4f}")
# Note: ultra-dilute strong acid gives pH < 7 but > 6 (water contributes!)

# Compare with Henderson-Hasselbalch approximation
C = 0.001  # 1 mM - borderline case
Ka = 1.8e-5
pH_exact = exact_weak_acid_pH(C, Ka)
pH_approx = -np.log10(np.sqrt(Ka * C))  # Simple approximation
print(f"\n1 mM acetic acid:")
print(f"  Exact: pH = {pH_exact:.4f}")
print(f"  Approx (sqrt(Ka*C)): pH = {pH_approx:.4f}")
print(f"  Error: {abs(pH_exact - pH_approx):.4f} pH units")
```

### Appendix B — Alpha (α) Diagrams: Speciation as a Function of pH

For a diprotic acid H₂A with $K_{a1}$ and $K_{a2}$, the fraction of each species at any pH:

$$
\alpha_0 = \frac{[\text{H}_2\text{A}]}{C_T} = \frac{[\text{H}^+]^2}{[\text{H}^+]^2 + K_{a1}[\text{H}^+] + K_{a1}K_{a2}}
$$

$$
\alpha_1 = \frac{[\text{HA}^-]}{C_T} = \frac{K_{a1}[\text{H}^+]}{[\text{H}^+]^2 + K_{a1}[\text{H}^+] + K_{a1}K_{a2}}
$$

$$
\alpha_2 = \frac{[\text{A}^{2-}]}{C_T} = \frac{K_{a1}K_{a2}}{[\text{H}^+]^2 + K_{a1}[\text{H}^+] + K_{a1}K_{a2}}
$$

where $C_T = [\text{H}_2\text{A}] + [\text{HA}^-] + [\text{A}^{2-}]$ is the total analytical concentration.

**Key features of α diagrams:**
- At pH = pKa1: $\alpha_0 = \alpha_1 = 0.5$ (crossover point)
- At pH = pKa2: $\alpha_1 = \alpha_2 = 0.5$ (second crossover)
- Each species dominates in its pH range: H₂A below pKa1, HA⁻ between pKa1 and pKa2, A²⁻ above pKa2

**General formula for polyprotic acid** H_nA with $n$ dissociation constants:

$$
\alpha_j = \frac{\prod_{i=1}^j K_{ai} \cdot [\text{H}^+]^{n-j}}{\sum_{k=0}^n \prod_{i=1}^k K_{ai} \cdot [\text{H}^+]^{n-k}}
$$

### Appendix C — The Relationship Between $K$, $\Delta G°$, and the Partition Function

The equilibrium constant connects three levels of description:

**Macroscopic (thermodynamics):**

$$
\Delta G^\circ = -RT\ln K
$$

**Microscopic (statistical mechanics):**

$$
K = \frac{\prod_{\text{products}} (q_i^\circ/N_A)^{\nu_i}}{\prod_{\text{reactants}} (q_j^\circ/N_A)^{\nu_j}}\,e^{-\Delta E_0/(k_BT)}
$$

where $\Delta E_0$ is the difference in zero-point energies (from [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy)).

**Molecular (quantum mechanics):**

The partition functions $q_i$ encode all molecular energy levels — translational, rotational, vibrational, electronic — which come from solving the Schrödinger equation for each molecule.

**The van't Hoff equation** (temperature dependence of $K$):

$$
\frac{d\ln K}{dT} = \frac{\Delta H^\circ}{RT^2}
$$

**Integrated form (assuming $\Delta H^\circ$ constant):**

$$
\ln\frac{K_2}{K_1} = \frac{\Delta H^\circ}{R}\left(\frac{1}{T_1} - \frac{1}{T_2}\right)
$$

**Worked Example:** The Haber process: $\Delta H^\circ = -92.2\,\text{kJ/mol}$. At 298 K, $K = 6.0 \times 10^5$. Find $K$ at 700 K:

$$
\ln\frac{K_{700}}{6.0 \times 10^5} = \frac{-92200}{8.314}\left(\frac{1}{298} - \frac{1}{700}\right) = -11090 \times 1.93 \times 10^{-3} = -21.4
$$

$$
K_{700} = 6.0 \times 10^5 \times e^{-21.4} = 6.0 \times 10^5 \times 5.0 \times 10^{-10} = 3.0 \times 10^{-4}
$$

The equilibrium shifts dramatically toward reactants at high temperature — this is why the Haber process needs a catalyst (to achieve reasonable rates at moderate temperatures where $K$ is still favorable).

### Appendix D — Solubility Equilibria and the Common Ion Effect

**Solubility product:**

$$
\text{AgCl}(s) \rightleftharpoons \text{Ag}^+(aq) + \text{Cl}^-(aq), \quad K_{sp} = [\text{Ag}^+][\text{Cl}^-] = 1.8 \times 10^{-10}
$$

**In pure water:** $s = \sqrt{K_{sp}} = 1.34 \times 10^{-5}\,\text{M}$

**Common ion effect — in 0.10 M NaCl:**

$$
K_{sp} = [\text{Ag}^+](0.10 + s) \approx [\text{Ag}^+] \times 0.10
$$

$$
[\text{Ag}^+] = \frac{1.8 \times 10^{-10}}{0.10} = 1.8 \times 10^{-9}\,\text{M}
$$

Solubility decreased by a factor of ~7500! This is Le Chatelier in action — adding Cl⁻ shifts the dissolution equilibrium left.

**pH-dependent solubility:**

For metal hydroxides like Fe(OH)₃ ($K_{sp} = 2.8 \times 10^{-39}$):

$$
s = \frac{K_{sp}}{[\text{OH}^-]^3} = \frac{K_{sp} \times [\text{H}^+]^3}{K_w^3}
$$

At pH 7: $s = 2.8 \times 10^{-39}/(10^{-7})^3 = 2.8 \times 10^{-18}\,\text{M}$ (essentially zero)

At pH 3: $s = 2.8 \times 10^{-39} \times (10^{-3})^3/(10^{-14})^3 = 2.8 \times 10^{-39} \times 10^{33} = 2.8 \times 10^{-6}\,\text{M}$ (slightly soluble)

This is why acid rain dissolves iron from rocks and why water treatment plants control pH carefully.

> [!danger] 🧠 Common Misconceptions — Section 8 & 9 Summary
> 
> **❌ "Henderson-Hasselbalch always works"**
> **Truth:** It fails for very dilute solutions, very strong acids/bases, and when pH is far from pKa. The exact cubic equation is always correct. H-H is an approximation valid only in the buffer region.
> 
> **❌ "A buffer at pH = pKa is always the best buffer"**
> **Truth:** Maximum buffer capacity occurs at pH = pKa, but the BEST buffer for your application is one whose pKa is closest to your target pH. A phosphate buffer (pKa2 = 7.21) is better for pH 7.4 than an acetate buffer (pKa = 4.74) even though acetate has higher capacity at its own pKa.
> 
> **❌ "Le Chatelier's principle is a law"**
> **Truth:** Le Chatelier is a qualitative rule of thumb, not a fundamental law. It can be misleading in complex systems (e.g., adding an inert gas at constant volume doesn't shift equilibrium, despite "increasing pressure"). The real criterion is always ΔG: the system moves toward the state of minimum Gibbs free energy.
> 
> **❌ "Ksp tells you if something is soluble or insoluble"**
> **Truth:** Ksp tells you the MAXIMUM ion concentrations at equilibrium. Whether a salt is "soluble" depends on context — AgCl is "insoluble" in water but dissolves readily in ammonia solution (complex formation). Solubility is not a fixed property; it depends on the entire solution composition.
> 
> **❌ "Strong acids completely dissociate, period"**
> **Truth:** In concentrated solutions (>1 M), even "strong" acids like HCl show incomplete dissociation due to ion pairing. And H₂SO₄ is strong only for its FIRST proton — the second dissociation (Ka2 = 0.012) is weak. "Strong" is an approximation valid for dilute solutions.
> 
> **❌ "pH can't be negative or above 14"**
> **Truth:** pH = -log[H⁺]. For 10 M HCl: pH ≈ -1. For 10 M NaOH: pH ≈ 15. The 0-14 range is just the range for dilute aqueous solutions at 25°C. Concentrated acids and bases routinely have pH outside this range.

---

*Previous: [03.4 - Thermodynamics & Kinetics](03.4---Thermodynamics-&-Kinetics) | Next: [03.6 - Electrochemistry & Redox](03.6---Electrochemistry-&-Redox)*
