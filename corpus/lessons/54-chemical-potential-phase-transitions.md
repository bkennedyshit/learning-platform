---
title: "Chemical Potential Phase Transitions"
subject: "Thermodynamics & Statistical Mechanics"
catalog: advanced
audience_tier: higher-education
chapter: "5.4"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 5.4 — Chemical Potential & Phase Transitions

> *"The conditions of equilibrium of a heterogeneous system are that the temperature, pressure, and chemical potential of each component must be uniform throughout."* — J. Willard Gibbs

The chemical potential $\mu$ governs particle exchange and phase equilibria. When combined with the Gibbs free energy, it provides the complete framework for understanding phase transitions — from the familiar liquid-gas transition to exotic critical phenomena. This chapter derives the Clausius-Clapeyron equation, classifies phase transitions by the Ehrenfest scheme, and develops the Gibbs phase rule.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Define chemical potential as $\mu = (\partial G/\partial N)_{T,P}$ and interpret it physically.
2. Derive conditions for phase equilibrium (equality of $\mu$ across phases).
3. Derive and apply the Clausius-Clapeyron equation for first-order transitions.
4. Classify phase transitions using the Ehrenfest classification.
5. Apply the Gibbs phase rule $F = C - P + 2$ to multi-component systems.
6. Analyze critical phenomena and the van der Waals equation near the critical point.
7. Compute latent heats and slope of coexistence curves.

---

## 🖼️ Visual Anchor — Phase Diagram with Critical Point

![math-05__5.4-fig1](math-05__5.4-fig1.svg)

---

## 📚 1. Definitions

### Definition 5.4.1 — Chemical Potential

The **chemical potential** $\mu$ of a single-component system is:

$$
\mu = \left(\frac{\partial G}{\partial N}\right)_{T,P} = \left(\frac{\partial U}{\partial N}\right)_{S,V} = \left(\frac{\partial F}{\partial N}\right)_{T,V} = \left(\frac{\partial H}{\partial N}\right)_{S,P}
$$

For a single-component system: $G = \mu N$, so $\mu = G/N = g$ (Gibbs free energy per particle).

### Definition 5.4.2 — Phase Equilibrium Condition

Two phases $\alpha$ and $\beta$ of the same substance are in equilibrium when:

$$
T^\alpha = T^\beta, \quad P^\alpha = P^\beta, \quad \mu^\alpha(T,P) = \mu^\beta(T,P)
$$

### Definition 5.4.3 — Latent Heat

The **latent heat** $L$ of a first-order phase transition is the heat absorbed per mole at constant $T$ and $P$:

$$
L = T\Delta s = T(s^\beta - s^\alpha)
$$

where $s$ is the molar entropy. Equivalently, $L = \Delta h$ (molar enthalpy change).

### Definition 5.4.4 — Order of Phase Transition (Ehrenfest)

A phase transition is of **$n$-th order** if the $n$-th derivative of $G$ with respect to $T$ or $P$ is the first to be discontinuous at the transition:

- **First-order:** $S = -(\partial G/\partial T)_P$ and $V = (\partial G/\partial P)_T$ are discontinuous (latent heat, volume change).
- **Second-order:** $C_P$, $\alpha$, $\kappa_T$ (second derivatives of $G$) are discontinuous, but $S$ and $V$ are continuous.

### Definition 5.4.5 — Gibbs Phase Rule

For a system with $C$ independent components and $P$ coexisting phases:

$$
F = C - P + 2
$$

where $F$ is the number of thermodynamic degrees of freedom (independently variable intensive parameters).

---

## 📐 2. Axioms / Postulates

### Postulate 5.4.P1 — Gibbs-Duhem Relation

For a single-component system at equilibrium:

$$
SdT - VdP + Nd\mu = 0
$$

or in molar form: $sdT - vdP + d\mu = 0$. This constrains the intensive variables — they cannot all vary independently.

### Postulate 5.4.P2 — Stability Conditions

A stable equilibrium phase must satisfy:

$$
C_V > 0, \quad \kappa_T > 0, \quad C_P > 0
$$

Violation of these conditions signals a phase transition or spinodal decomposition.

---

## 🛡️ 3. Lemmas

### Lemma 5.4.1 — $G = \mu N$ for Single-Component Systems

**Proof.** $G$ is extensive: $G(\lambda T, \lambda P, \lambda N) = \lambda G(T, P, N)$... Actually, $G$ is extensive in $N$ at fixed $T, P$: $G(T, P, \lambda N) = \lambda G(T, P, N)$. Differentiate with respect to $\lambda$ and set $\lambda = 1$:

$$
N\left(\frac{\partial G}{\partial N}\right)_{T,P} = G \implies G = \mu N \quad \blacksquare
$$

### Lemma 5.4.2 — Derivation of the Gibbs-Duhem Relation

From $G = \mu N$, take the total differential:

$$
dG = \mu\,dN + N\,d\mu
$$

But from the fundamental relation: $dG = -SdT + VdP + \mu\,dN$.

Equating: $-SdT + VdP + \mu\,dN = \mu\,dN + N\,d\mu$.

Cancel $\mu\,dN$:

$$
-SdT + VdP = N\,d\mu \implies SdT - VdP + Nd\mu = 0 \quad \blacksquare
$$

---

## 👑 4. Theorems

### Theorem 5.4.1 — Clausius-Clapeyron Equation

Along a first-order coexistence curve in the $P$-$T$ plane:

$$
\frac{dP}{dT} = \frac{L}{T\Delta v} = \frac{\Delta s}{\Delta v}
$$

where $L$ is the latent heat, $\Delta v = v^\beta - v^\alpha$ is the molar volume change, and $\Delta s = s^\beta - s^\alpha$.

### Theorem 5.4.2 — Clausius-Clapeyron for Liquid-Gas (Approximate)

When $v_{\text{gas}} \gg v_{\text{liquid}}$ and the gas is approximately ideal ($v_g \approx RT/P$):

$$
\frac{dP}{dT} \approx \frac{LP}{RT^2} \implies \ln\frac{P_2}{P_1} = -\frac{L}{R}\left(\frac{1}{T_2} - \frac{1}{T_1}\right)
$$

### Theorem 5.4.3 — Gibbs Phase Rule

$$
F = C - P + 2
$$

### Theorem 5.4.4 — Van der Waals Critical Point

For the van der Waals equation $(P + a/v^2)(v - b) = RT$, the critical point satisfies:

$$
T_c = \frac{8a}{27Rb}, \quad P_c = \frac{a}{27b^2}, \quad v_c = 3b
$$

---

## ✍️ 5. Proofs / Derivations

### 5.1 Derivation of the Clausius-Clapeyron Equation

At phase equilibrium: $\mu^\alpha(T, P) = \mu^\beta(T, P)$.

Along the coexistence curve, both sides remain equal as $T$ and $P$ change:

$$
d\mu^\alpha = d\mu^\beta
$$

From the Gibbs-Duhem relation in molar form ($d\mu = -sdT + vdP$):

$$
-s^\alpha dT + v^\alpha dP = -s^\beta dT + v^\beta dP
$$

Rearrange:

$$
(s^\beta - s^\alpha)dT = (v^\beta - v^\alpha)dP
$$

$$
\frac{dP}{dT} = \frac{s^\beta - s^\alpha}{v^\beta - v^\alpha} = \frac{\Delta s}{\Delta v} = \frac{L}{T\Delta v} \quad \blacksquare
$$

### 5.2 Derivation of the Van der Waals Critical Point

The van der Waals equation: $P = \frac{RT}{v-b} - \frac{a}{v^2}$.

At the critical point, the isotherm has an inflection point with horizontal tangent:

$$
\left(\frac{\partial P}{\partial v}\right)_T = 0 \quad \text{and} \quad \left(\frac{\partial^2 P}{\partial v^2}\right)_T = 0
$$

Compute the first derivative:

$$
\frac{\partial P}{\partial v}\bigg|_T = -\frac{RT}{(v-b)^2} + \frac{2a}{v^3} = 0 \tag{1}
$$

Compute the second derivative:

$$
\frac{\partial^2 P}{\partial v^2}\bigg|_T = \frac{2RT}{(v-b)^3} - \frac{6a}{v^4} = 0 \tag{2}
$$

From (1): $RT = \frac{2a(v-b)^2}{v^3}$.

From (2): $RT = \frac{3a(v-b)^3}{v^4}$.

Equate:

$$
\frac{2a(v-b)^2}{v^3} = \frac{3a(v-b)^3}{v^4}
$$

Cancel $a(v-b)^2$:

$$
\frac{2}{v^3} = \frac{3(v-b)}{v^4} \implies 2v = 3(v-b) = 3v - 3b \implies v_c = 3b
$$

Substitute back: $RT_c = \frac{2a(3b-b)^2}{(3b)^3} = \frac{2a \cdot 4b^2}{27b^3} = \frac{8a}{27b}$, so $T_c = \frac{8a}{27Rb}$.

$$
P_c = \frac{RT_c}{v_c - b} - \frac{a}{v_c^2} = \frac{8a/(27b)}{2b} - \frac{a}{9b^2} = \frac{4a}{27b^2} - \frac{3a}{27b^2} = \frac{a}{27b^2} \quad \blacksquare
$$

### 5.3 Proof of the Gibbs Phase Rule

Each phase has $C + 1$ intensive variables ($T$, $P$, and $C-1$ independent mole fractions for a $C$-component system — actually $C+2$ total: $T$, $P$, $\mu_1, \ldots, \mu_C$, but the Gibbs-Duhem relation in each phase removes one).

Total intensive variables per phase: $C + 1$ (temperature, pressure, $C-1$ composition variables).

For $P$ phases: total variables = $P(C+1)$... Let us use the standard counting:

**Variables:** $T$, $P$, and $(C-1)$ mole fractions in each of $P$ phases = $2 + P(C-1)$.

**Constraints:** Chemical potential equality across phases for each component: $\mu_i^\alpha = \mu_i^\beta = \cdots$ gives $(P-1)$ equations per component = $C(P-1)$.

**Degrees of freedom:**

$$
F = 2 + P(C-1) - C(P-1) = 2 + PC - P - CP + C = C - P + 2 \quad \blacksquare
$$

---

## 🧮 6. Worked Examples

### Example 5.4.E1 — Clausius-Clapeyron: Boiling Point of Water at Altitude

At sea level ($P_1 = 101.3\,\text{kPa}$), water boils at $T_1 = 373\,\text{K}$. At altitude where $P_2 = 80\,\text{kPa}$, find the boiling point. Use $L_{\text{vap}} = 40.7\,\text{kJ/mol}$.

**Solution:** Using the integrated Clausius-Clapeyron equation:

$$
\ln\frac{P_2}{P_1} = -\frac{L}{R}\left(\frac{1}{T_2} - \frac{1}{T_1}\right)
$$

$$
\ln\frac{80}{101.3} = -\frac{40700}{8.314}\left(\frac{1}{T_2} - \frac{1}{373}\right)
$$

$$
-0.2357 = -4894\left(\frac{1}{T_2} - 0.002681\right)
$$

$$
\frac{1}{T_2} - 0.002681 = 4.816 \times 10^{-5}
$$

$$
\frac{1}{T_2} = 0.002729 \implies T_2 = 366.4\,\text{K} = 93.4°\text{C}
$$

### Example 5.4.E2 — Gibbs Phase Rule Applications

**(a) Pure water at triple point:** $C = 1$, $P = 3$ (solid, liquid, gas). $F = 1 - 3 + 2 = 0$. Zero degrees of freedom — the triple point is a fixed point in $T$-$P$ space.

**(b) Salt water at boiling:** $C = 2$ (H₂O, NaCl), $P = 2$ (liquid, gas). $F = 2 - 2 + 2 = 2$. Two degrees of freedom — can independently vary $T$ and composition.

### Example 5.4.E3 — Latent Heat from Coexistence Curve Slope

The ice-water coexistence curve has slope $dP/dT \approx -1.35 \times 10^7\,\text{Pa/K}$ (negative because ice is less dense than water). Given $\Delta v = v_{\text{liquid}} - v_{\text{solid}} = -1.6 \times 10^{-6}\,\text{m}^3/\text{mol}$ at $T = 273\,\text{K}$:

$$
L = T\Delta v\frac{dP}{dT} = 273 \times (-1.6\times10^{-6}) \times (-1.35\times10^7) = 5900\,\text{J/mol} = 5.9\,\text{kJ/mol}
$$

Literature value: $L_{\text{fusion}} = 6.01\,\text{kJ/mol}$. ✓

---

## 🔗 7. Cross-links & Further Reading

### Internal Cross-links
- Gibbs free energy: [5.3 - Thermodynamic Potentials & Maxwell Relations](5.3---Thermodynamic-Potentials-&-Maxwell-Relations)
- Statistical mechanics of phase transitions: [5.5 - Classical Statistical Mechanics - Microstates & Ensembles](5.5---Classical-Statistical-Mechanics---Microstates-&-Ensembles)
- Partition function approach to chemical equilibrium: [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy)
- Quantum statistics and Bose-Einstein condensation (a phase transition): [5.8 - Quantum Statistics - Bose-Einstein & Fermi-Dirac](5.8---Quantum-Statistics---Bose-Einstein-&-Fermi-Dirac)
- ODEs and the Clausius-Clapeyron ODE: [3.1 - First-Order ODEs & Separable Equations](3.1---First-Order-ODEs-&-Separable-Equations)

### Authoritative Sources
- **Callen**, *Thermodynamics*, Ch. 9–10 (phase transitions, stability)
- **Landau & Lifshitz**, *Statistical Physics Part 1*, Ch. 14 (phase equilibrium)
- **Stanley**, *Introduction to Phase Transitions and Critical Phenomena*
- **Kittel & Kroemer**, *Thermal Physics*, Ch. 10


---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — Clausius-Clapeyron Applied to Water Vaporization

**Problem.** Water has a latent heat of vaporization $L = 40.7\,\text{kJ/mol}$ at $T = 373\,\text{K}$ (100°C). (a) Estimate the boiling point at the top of Mount Everest ($P = 34\,\text{kPa}$). (b) Estimate the vapor pressure of water at $T = 50°\text{C}$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Setup: The Integrated Clausius-Clapeyron Equation

Starting from the Clausius-Clapeyron equation:

$$
\frac{dP}{dT} = \frac{L}{T\Delta v} \approx \frac{L}{TV_{\text{gas}}} = \frac{LP}{RT^2}
$$

where we used $\Delta v \approx V_{\text{gas}} = RT/P$ (ideal gas approximation for vapor, neglecting liquid volume).

Separating variables:

$$
\frac{dP}{P} = \frac{L}{R}\frac{dT}{T^2}
$$

Integrating from $(T_1, P_1)$ to $(T_2, P_2)$, assuming $L$ is approximately constant:

$$
\ln\frac{P_2}{P_1} = -\frac{L}{R}\left(\frac{1}{T_2} - \frac{1}{T_1}\right)
$$

#### Part (a): Boiling Point at Everest Summit

At the boiling point, $P_{\text{vapor}} = P_{\text{atm}}$. Reference: $P_1 = 101.3\,\text{kPa}$ at $T_1 = 373\,\text{K}$.

Given $P_2 = 34\,\text{kPa}$, find $T_2$:

$$
\ln\frac{34}{101.3} = -\frac{40700}{8.314}\left(\frac{1}{T_2} - \frac{1}{373}\right)
$$

$$
\ln(0.3357) = -4894\left(\frac{1}{T_2} - 0.002681\right)
$$

$$
-1.092 = -4894\left(\frac{1}{T_2} - 0.002681\right)
$$

$$
\frac{1}{T_2} - 0.002681 = \frac{1.092}{4894} = 2.231 \times 10^{-4}
$$

$$
\frac{1}{T_2} = 0.002681 + 0.0002231 = 0.002904
$$

$$
T_2 = \frac{1}{0.002904} = 344.3\,\text{K} = 71.2°\text{C}
$$

Water boils at approximately $71°\text{C}$ at the summit of Everest. (Actual measured value: ~70°C — good agreement.)

#### Part (b): Vapor Pressure at 50°C

Reference: $P_1 = 101.3\,\text{kPa}$ at $T_1 = 373\,\text{K}$. Find $P_2$ at $T_2 = 323\,\text{K}$:

$$
\ln\frac{P_2}{101.3} = -\frac{40700}{8.314}\left(\frac{1}{323} - \frac{1}{373}\right)
$$

$$
= -4894\left(0.003096 - 0.002681\right) = -4894 \times 4.15 \times 10^{-4} = -2.031
$$

$$
\frac{P_2}{101.3} = e^{-2.031} = 0.1313
$$

$$
P_2 = 101.3 \times 0.1313 = 13.3\,\text{kPa}
$$

Literature value at 50°C: $P = 12.3\,\text{kPa}$. The ~8% discrepancy comes from assuming constant $L$ (in reality, $L$ decreases with temperature).

</details>

---

### Example 8.2 — Chemical Potential of a Mixture: Raoult's Law

**Problem.** A binary liquid mixture of benzene (A) and toluene (B) at $T = 353\,\text{K}$ has mole fraction $x_A = 0.4$ (benzene). The pure-component vapor pressures are $P_A^* = 101.3\,\text{kPa}$ and $P_B^* = 39.5\,\text{kPa}$. Assuming ideal solution behavior (Raoult's law): (a) Find the total vapor pressure. (b) Find the vapor-phase composition. (c) Derive Raoult's law from the chemical potential.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Part (a): Total Vapor Pressure (Raoult's Law)

For an ideal solution, Raoult's law states that the partial vapor pressure of each component is:

$$
P_i = x_i P_i^*
$$

where $x_i$ is the liquid-phase mole fraction and $P_i^*$ is the vapor pressure of pure component $i$.

$$
P_A = x_A P_A^* = 0.4 \times 101.3 = 40.5\,\text{kPa}
$$

$$
P_B = x_B P_B^* = 0.6 \times 39.5 = 23.7\,\text{kPa}
$$

$$
P_{\text{total}} = P_A + P_B = 40.5 + 23.7 = 64.2\,\text{kPa}
$$

#### Part (b): Vapor-Phase Composition

By Dalton's law, the vapor-phase mole fraction is:

$$
y_A = \frac{P_A}{P_{\text{total}}} = \frac{40.5}{64.2} = 0.631
$$

$$
y_B = 1 - y_A = 0.369
$$

The vapor is enriched in the more volatile component (benzene: $y_A = 0.63 \gt  x_A = 0.40$). This is the basis of distillation.

#### Part (c): Thermodynamic Derivation of Raoult's Law

**Step 1:** For a component in an ideal liquid mixture, the chemical potential is:

$$
\mu_i^{\text{liq}}(T, P, x_i) = \mu_i^{*,\text{liq}}(T, P) + RT\ln x_i
$$

where $\mu_i^{*,\text{liq}}$ is the chemical potential of pure liquid $i$. The $RT\ln x_i$ term comes from the entropy of mixing in an ideal solution.

**Step 2:** For the vapor phase (assumed ideal gas):

$$
\mu_i^{\text{vap}}(T, P_i) = \mu_i^{\circ,\text{vap}}(T) + RT\ln\frac{P_i}{P°}
$$

**Step 3:** At equilibrium, $\mu_i^{\text{liq}} = \mu_i^{\text{vap}}$. For pure component $i$ ($x_i = 1$, $P_i = P_i^*$):

$$
\mu_i^{*,\text{liq}}(T, P) = \mu_i^{\circ,\text{vap}}(T) + RT\ln\frac{P_i^*}{P°}
$$

**Step 4:** For the mixture:

$$
\mu_i^{*,\text{liq}} + RT\ln x_i = \mu_i^{\circ,\text{vap}} + RT\ln\frac{P_i}{P°}
$$

Subtract the pure-component equilibrium (Step 3):

$$
RT\ln x_i = RT\ln\frac{P_i}{P°} - RT\ln\frac{P_i^*}{P°} = RT\ln\frac{P_i}{P_i^*}
$$

$$
\ln x_i = \ln\frac{P_i}{P_i^*} \implies P_i = x_i P_i^* \quad \blacksquare
$$

Raoult's law is thus a direct consequence of the ideal solution assumption for the chemical potential.

</details>

---

### Example 8.3 — Van der Waals Critical Point: Complete Derivation

**Problem.** For the van der Waals equation $\left(P + \frac{a}{v^2}\right)(v - b) = RT$ (per mole), derive the critical constants $(T_c, P_c, v_c)$ and the universal ratio $P_c v_c/(RT_c)$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Conditions at the Critical Point

The critical point is an inflection point on the critical isotherm in the $P$-$v$ diagram. At this point, the isotherm has a horizontal tangent AND zero curvature:

$$
\left(\frac{\partial P}{\partial v}\right)_T = 0 \quad \text{(horizontal tangent)}
$$

$$
\left(\frac{\partial^2 P}{\partial v^2}\right)_T = 0 \quad \text{(inflection point)}
$$

#### Step 2: Compute the Derivatives

From $P = \frac{RT}{v-b} - \frac{a}{v^2}$:

**First derivative:**

$$
\left(\frac{\partial P}{\partial v}\right)_T = -\frac{RT}{(v-b)^2} + \frac{2a}{v^3}
$$

**Second derivative:**

$$
\left(\frac{\partial^2 P}{\partial v^2}\right)_T = \frac{2RT}{(v-b)^3} - \frac{6a}{v^4}
$$

#### Step 3: Solve the System

Setting both derivatives to zero at $(T_c, v_c)$:

$$
\frac{RT_c}{(v_c - b)^2} = \frac{2a}{v_c^3} \quad \cdots (1)
$$

$$
\frac{2RT_c}{(v_c - b)^3} = \frac{6a}{v_c^4} \quad \cdots (2)
$$

Divide equation (2) by equation (1):

$$
\frac{2}{v_c - b} = \frac{6/v_c^4}{2/v_c^3} = \frac{3}{v_c}
$$

$$
2v_c = 3(v_c - b) = 3v_c - 3b
$$

$$
\boxed{v_c = 3b}
$$

#### Step 4: Find $T_c$

Substitute $v_c = 3b$ into equation (1):

$$
\frac{RT_c}{(3b - b)^2} = \frac{2a}{(3b)^3}
$$

$$
\frac{RT_c}{4b^2} = \frac{2a}{27b^3}
$$

$$
RT_c = \frac{8a}{27b}
$$

$$
\boxed{T_c = \frac{8a}{27Rb}}
$$

#### Step 5: Find $P_c$

Substitute $v_c = 3b$ and $T_c = 8a/(27Rb)$ into the equation of state:

$$
P_c = \frac{RT_c}{v_c - b} - \frac{a}{v_c^2} = \frac{8a/(27b)}{2b} - \frac{a}{9b^2}
$$

$$
= \frac{8a}{54b^2} - \frac{a}{9b^2} = \frac{4a}{27b^2} - \frac{3a}{27b^2}
$$

$$
\boxed{P_c = \frac{a}{27b^2}}
$$

#### Step 6: Universal Ratio

$$
\frac{P_c v_c}{RT_c} = \frac{\frac{a}{27b^2} \cdot 3b}{\frac{8a}{27b}} = \frac{\frac{3a}{27b}}{\frac{8a}{27b}} = \frac{3}{8}
$$

$$
\boxed{\frac{P_c v_c}{RT_c} = \frac{3}{8} = 0.375}
$$

**Comparison with experiment:** Real gases have $P_c v_c/(RT_c)$ ranging from 0.23 (water) to 0.29 (noble gases). The van der Waals prediction of 0.375 is too high, reflecting the model's limitations. Nevertheless, the law of corresponding states (that this ratio is universal) is approximately correct.

#### Step 7: Reduced Variables

Defining $P_r = P/P_c$, $v_r = v/v_c$, $T_r = T/T_c$, the van der Waals equation becomes:

$$
\left(P_r + \frac{3}{v_r^2}\right)\left(v_r - \frac{1}{3}\right) = \frac{8T_r}{3}
$$

This is the **law of corresponding states**: all van der Waals gases obey the same equation when expressed in reduced variables. The material-specific constants $a$ and $b$ have been absorbed into the critical constants.

</details>



---

### Example 8.4 — Osmotic Pressure from Chemical Potential

**Problem.** Derive the van't Hoff equation for osmotic pressure: $\Pi V = n_s RT$, where $n_s$ is the number of moles of solute and $V$ is the volume of solution.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Setup

A semipermeable membrane separates pure solvent (left) from a solution (right). The membrane allows solvent to pass but not solute. At equilibrium, the pressure on the solution side exceeds that on the pure solvent side by the osmotic pressure $\Pi$.

#### Step 1: Equilibrium Condition

At equilibrium, the chemical potential of the solvent must be equal on both sides:

$$
\mu_{\text{solvent}}^{\text{pure}}(T, P) = \mu_{\text{solvent}}^{\text{solution}}(T, P + \Pi)
$$

#### Step 2: Chemical Potential of Solvent in Solution

For a dilute ideal solution:

$$
\mu_{\text{solvent}}^{\text{solution}}(T, P + \Pi) = \mu_{\text{solvent}}^{*}(T, P + \Pi) + RT\ln x_{\text{solvent}}
$$

where $x_{\text{solvent}} = 1 - x_s \approx 1 - n_s/n_{\text{total}}$ for dilute solutions.

#### Step 3: Pressure Dependence

$$
\mu_{\text{solvent}}^{*}(T, P + \Pi) = \mu_{\text{solvent}}^{*}(T, P) + \int_P^{P+\Pi} V_m\,dP' \approx \mu_{\text{solvent}}^{*}(T, P) + V_m\Pi
$$

where $V_m$ is the molar volume of the solvent (assumed incompressible).

#### Step 4: Combine

The equilibrium condition becomes:

$$
\mu^{*}(T, P) = \mu^{*}(T, P) + V_m\Pi + RT\ln(1 - x_s)
$$

$$
0 = V_m\Pi + RT\ln(1 - x_s)
$$

For dilute solutions, $\ln(1 - x_s) \approx -x_s$:

$$
V_m\Pi = RTx_s
$$

For a dilute solution: $x_s \approx n_s/n_{\text{solvent}}$ and $V = n_{\text{solvent}}V_m$:

$$
V_m\Pi = RT\frac{n_s}{n_{\text{solvent}}} \implies \Pi \cdot n_{\text{solvent}}V_m = n_s RT
$$

$$
\boxed{\Pi V = n_s RT}
$$

This has the same form as the ideal gas law — the solute molecules exert "osmotic pressure" analogous to gas pressure. This is van't Hoff's remarkable result (Nobel Prize, 1901).

</details>

---

## 📘 9. Appendix: Extended Derivations & Special Cases

### Appendix 9.1 — Derivation of the Gibbs Phase Rule

The Gibbs phase rule $F = C - P + 2$ determines the number of intensive degrees of freedom $F$ for a system with $C$ independent components and $P$ coexisting phases. Here we derive it from first principles.

**Step 1: Count the intensive variables.**

For a system with $C$ components and $P$ phases, the intensive state of each phase $\alpha$ is specified by:
- Temperature $T^\alpha$
- Pressure $P^\alpha$
- $C - 1$ independent mole fractions $x_1^\alpha, x_2^\alpha, \ldots, x_{C-1}^\alpha$ (the $C$-th is determined by $\sum x_i = 1$)

Total number of intensive variables: $P \times (C - 1 + 2) = P(C + 1)$.

**Step 2: Count the equilibrium constraints.**

Thermal equilibrium requires all phases at the same temperature:

$$
T^1 = T^2 = \cdots = T^P \quad \Rightarrow \quad (P - 1) \text{ equations}
$$

Mechanical equilibrium requires all phases at the same pressure:

$$
P^1 = P^2 = \cdots = P^P \quad \Rightarrow \quad (P - 1) \text{ equations}
$$

Chemical equilibrium requires the chemical potential of each component to be equal across all phases:

$$
\mu_i^1 = \mu_i^2 = \cdots = \mu_i^P \quad \text{for each } i = 1, \ldots, C
$$

This gives $C(P - 1)$ equations.

**Step 3: Total constraints.**

$$
\text{Total constraints} = (P-1) + (P-1) + C(P-1) = (C+2)(P-1)
$$

**Step 4: Degrees of freedom.**

$$
F = \text{variables} - \text{constraints} = P(C+1) - (C+2)(P-1)
$$

$$
= PC + P - CP - 2P + C + 2
$$

$$
= PC + P - CP - 2P + C + 2 = -P + C + 2
$$

$$
\boxed{F = C - P + 2}
$$

**Examples:**
- Pure water ($C=1$), single phase ($P=1$): $F = 1 - 1 + 2 = 2$. Two degrees of freedom ($T$ and $P$ can be varied independently).
- Pure water at liquid-vapor coexistence ($P=2$): $F = 1 - 2 + 2 = 1$. One degree of freedom (specifying $T$ determines $P$ via the Clausius-Clapeyron equation).
- Pure water at triple point ($P=3$): $F = 1 - 3 + 2 = 0$. Zero degrees of freedom — the triple point is a unique point in $(T, P)$ space.
- Binary alloy ($C=2$) with two solid phases and liquid ($P=3$): $F = 2 - 3 + 2 = 1$. This is the eutectic point — one degree of freedom (e.g., pressure).

**Limitations:** The phase rule assumes:
1. Only $PV$ work (no surface tension, electric fields, etc.)
2. No chemical reactions linking the components
3. Each component is present in every phase

If there are $R$ independent chemical reactions, the effective number of components is $C - R$, and the modified rule is $F = (C - R) - P + 2$.

**Reference:** Callen, *Thermodynamics*, Ch. 9; Landau & Lifshitz, *Statistical Physics Part 1*, §96.

---

### Appendix 9.2 — Landau Theory of Phase Transitions: Order Parameter Expansion

Near a continuous (second-order) phase transition, Landau proposed expanding the Gibbs free energy in powers of an order parameter $\eta$ that is zero in the disordered phase and nonzero in the ordered phase:

$$
G(T, P, \eta) = G_0(T, P) + a(T)\eta^2 + b\eta^4 + \cdots
$$

where $b > 0$ (for stability) and $a(T) = a_0(T - T_c)$ changes sign at the critical temperature.

**Equilibrium condition:** Minimize $G$ with respect to $\eta$:

$$
\frac{\partial G}{\partial \eta} = 2a\eta + 4b\eta^3 = 0
$$

$$
\eta(2a + 4b\eta^2) = 0
$$

**Solutions:**
- $\eta = 0$ (disordered phase) — always a solution.
- $\eta^2 = -a/(2b) = -a_0(T - T_c)/(2b)$ — real only for $T < T_c$.

**For $T > T_c$:** $a > 0$, so $\eta = 0$ is the minimum. Disordered phase.

**For $T < T_c$:** $a < 0$, so $\eta = 0$ is a maximum and the minima are at:

$$
\eta = \pm\sqrt{\frac{a_0(T_c - T)}{2b}} \propto (T_c - T)^{1/2}
$$

The order parameter grows as $(T_c - T)^{1/2}$ — this defines the **critical exponent** $\beta = 1/2$ in mean-field theory.

**Heat capacity jump:** The entropy $S = -\partial G/\partial T$ has a kink at $T_c$, giving a discontinuity in $C_P$:

$$
\Delta C_P = \frac{a_0^2 T_c}{2b}
$$

This is the hallmark of a second-order phase transition: no latent heat, but a jump in heat capacity.

**Limitations:** Landau theory is a mean-field approximation. Near $T_c$, fluctuations become important and modify the critical exponents (e.g., $\beta \approx 0.33$ for 3D Ising model instead of 0.5). The Ginzburg criterion determines when fluctuations dominate.

**Reference:** Landau & Lifshitz, *Statistical Physics Part 1*, Ch. 14; Stanley, *Introduction to Phase Transitions and Critical Phenomena*, Ch. 6.

---

### Appendix 9.3 — Chemical Potential and the Gibbs-Duhem Relation

The Gibbs-Duhem relation constrains the intensive variables of a thermodynamic system and is essential for understanding multicomponent equilibrium.

**Derivation.** The Gibbs free energy is an extensive function of $(T, P, n_1, \ldots, n_C)$. By Euler's theorem for homogeneous functions of degree 1:

$$
G = \sum_{i=1}^C n_i \mu_i
$$

Taking the total differential:

$$
dG = \sum_i \mu_i\,dn_i + \sum_i n_i\,d\mu_i
$$

But from the fundamental relation: $dG = -S\,dT + V\,dP + \sum_i \mu_i\,dn_i$.

Comparing:

$$
\sum_i n_i\,d\mu_i = -S\,dT + V\,dP
$$

$$
\boxed{S\,dT - V\,dP + \sum_{i=1}^C n_i\,d\mu_i = 0} \quad \text{(Gibbs-Duhem relation)}
$$

**At constant $T$ and $P$:**

$$
\sum_i n_i\,d\mu_i = 0 \quad \text{or equivalently} \quad \sum_i x_i\,d\mu_i = 0
$$

**Physical meaning:** The chemical potentials of the components in a mixture are not all independent — they are constrained by the Gibbs-Duhem relation. For a binary mixture at constant $T, P$:

$$
x_1\,d\mu_1 + x_2\,d\mu_2 = 0 \implies d\mu_2 = -\frac{x_1}{x_2}\,d\mu_1
$$

If we know how $\mu_1$ varies with composition, $\mu_2$ is completely determined. This is the basis for the Gibbs-Duhem integration method in experimental thermodynamics.

**Reference:** Callen, *Thermodynamics*, Ch. 8; Kittel & Kroemer, *Thermal Physics*, Ch. 5.

---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

*Previous: [5.3 - Thermodynamic Potentials & Maxwell Relations](5.3---Thermodynamic-Potentials-&-Maxwell-Relations) | Next: [5.5 - Classical Statistical Mechanics - Microstates & Ensembles](5.5---Classical-Statistical-Mechanics---Microstates-&-Ensembles)*



---

### Appendix 9.4 — Ehrenfest Classification of Phase Transitions

Paul Ehrenfest (1933) proposed classifying phase transitions by the order of the lowest derivative of the Gibbs free energy that is discontinuous at the transition.

**First-order transitions:** The first derivatives of $G$ are discontinuous:

$$
S = -\left(\frac{\partial G}{\partial T}\right)_P \quad \text{(discontinuous)} \implies \text{latent heat } L = T\Delta S
$$

$$
V = \left(\frac{\partial G}{\partial P}\right)_T \quad \text{(discontinuous)} \implies \text{volume change } \Delta V
$$

Examples: melting, boiling, sublimation. The Clausius-Clapeyron equation applies.

**Second-order transitions:** $G$, $S$, and $V$ are continuous, but the second derivatives are discontinuous:

$$
C_P = -T\left(\frac{\partial^2 G}{\partial T^2}\right)_P \quad \text{(discontinuous or divergent)}
$$

$$
\alpha = \frac{1}{V}\left(\frac{\partial^2 G}{\partial T\,\partial P}\right) \quad \text{(discontinuous or divergent)}
$$

$$
\kappa_T = -\frac{1}{V}\left(\frac{\partial^2 G}{\partial P^2}\right)_T \quad \text{(discontinuous or divergent)}
$$

Examples: superconducting transition (in zero field), superfluid transition in He-4 (lambda point), ferromagnetic Curie point.

**Modern view:** The Ehrenfest classification is too rigid for most real transitions. Modern theory (Landau, Wilson, renormalization group) distinguishes:
- **First-order:** Latent heat, phase coexistence, metastability.
- **Continuous (critical):** No latent heat, divergent correlation length, power-law singularities characterized by critical exponents.

The lambda transition in He-4 has $C_P$ that diverges logarithmically — it doesn't fit neatly into "second order" (which would predict a finite jump). The renormalization group framework handles these subtleties naturally.

**Reference:** Ehrenfest (1933); Landau & Lifshitz, *Statistical Physics Part 1*, Ch. 14; Stanley, *Phase Transitions and Critical Phenomena*.
