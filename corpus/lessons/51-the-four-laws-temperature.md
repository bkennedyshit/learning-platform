---
title: "The Four Laws Temperature"
subject: "Thermodynamics & Statistical Mechanics"
catalog: advanced
audience_tier: higher-education
chapter: "5.1"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 5.1 — The Four Laws & Temperature

> *"A theory is the more impressive the greater the simplicity of its premises, the more different kinds of things it relates, and the more extended its area of applicability."* — Albert Einstein

The four laws of thermodynamics constitute the axiomatic foundation upon which all of thermal physics rests. They define temperature (Zeroth Law), energy conservation in thermal processes (First Law), the arrow of time and irreversibility (Second Law), and the unattainability of absolute zero (Third Law). This chapter develops each law with full mathematical rigor, establishing the conceptual bedrock for entropy, heat engines, and statistical mechanics in subsequent chapters.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. State the Zeroth Law and derive the existence of temperature as a state function from the transitivity of thermal equilibrium.
2. Write the First Law in differential form $dU = \delta Q - \delta W$ and distinguish exact from inexact differentials.
3. Compute work $W = \int P\,dV$ for quasi-static processes (isobaric, isothermal, adiabatic).
4. State the Second Law in both Kelvin-Planck and Clausius formulations and prove their logical equivalence.
5. State the Third Law (Nernst heat theorem) and derive its consequence that $C_V \to 0$ as $T \to 0$.
6. Define empirical and absolute (thermodynamic) temperature scales and show their equivalence via Carnot's theorem.
7. Distinguish between state functions and path-dependent quantities using the mathematical criterion of exact differentials.

---

## 🖼️ Visual Anchor — The Four Laws Tower

![math-05__5.1-fig1](math-05__5.1-fig1.svg)

---

## 📚 1. Definitions

### Definition 5.1.1 — Thermodynamic System

A **thermodynamic system** is a macroscopic body (or collection of bodies) delineated by a boundary from its **surroundings**. The system plus surroundings constitute the **universe** (in the thermodynamic sense). Systems are classified as:

- **Isolated:** No exchange of energy or matter with surroundings ($\delta Q = 0$, $\delta W = 0$, $dN = 0$).
- **Closed:** Exchange of energy but not matter ($dN = 0$).
- **Open:** Exchange of both energy and matter.

### Definition 5.1.2 — Thermodynamic Equilibrium

A system is in **thermodynamic equilibrium** when it simultaneously satisfies:

1. **Thermal equilibrium:** No net heat flow between subsystems (uniform $T$).
2. **Mechanical equilibrium:** No unbalanced forces (uniform $P$).
3. **Chemical equilibrium:** No net chemical reactions or diffusion (uniform $\mu$).

### Definition 5.1.3 — State Function vs. Path Function

A **state function** $f$ depends only on the current equilibrium state of the system, not on the history of how that state was reached. Mathematically, its differential $df$ is **exact**: for any two states $A$ and $B$,

$$
\int_A^B df = f(B) - f(A)
$$

independent of path. Examples: $U$, $S$, $T$, $P$, $V$.

A **path function** (process quantity) depends on the specific process. Its differential $\delta Q$ or $\delta W$ is **inexact** — the integral depends on the path taken in state space.

### Definition 5.1.4 — Exact Differential Criterion

A differential $\delta F = M(x,y)\,dx + N(x,y)\,dy$ is exact if and only if:

$$
\frac{\partial M}{\partial y}\bigg|_x = \frac{\partial N}{\partial x}\bigg|_y
$$

This is a direct consequence of Clairaut's theorem on the equality of mixed partial derivatives for $C^2$ functions (see [1.4 - Multivariable Calculus & Vector Analysis](1.4---Multivariable-Calculus-&-Vector-Analysis)).

### Definition 5.1.5 — Quasi-Static Process

A **quasi-static** (or quasi-equilibrium) process proceeds sufficiently slowly that the system passes through a continuous sequence of equilibrium states. Only for quasi-static processes can we write:

$$
\delta W = P\,dV
$$

where $P$ is the system pressure. For non-quasi-static processes, $\delta W \neq P\,dV$ in general.

### Definition 5.1.6 — Heat Capacity

The **heat capacity** at constant volume and constant pressure:

$$
C_V = \left(\frac{\partial U}{\partial T}\right)_V, \qquad C_P = \left(\frac{\partial H}{\partial T}\right)_P
$$

where $H = U + PV$ is the enthalpy. For an ideal gas, $C_P - C_V = nR$ (proved in §5 below).


---

## 📐 2. Axioms / Postulates

### Axiom 5.1.A1 — The Zeroth Law of Thermodynamics

If system $A$ is in thermal equilibrium with system $B$, and system $B$ is in thermal equilibrium with system $C$, then system $A$ is in thermal equilibrium with system $C$.

$$
(A \sim B) \wedge (B \sim C) \implies A \sim C
$$

where $\sim$ denotes "is in thermal equilibrium with." This transitivity relation partitions all thermodynamic systems into equivalence classes. The **temperature** $T$ is the label assigned to each equivalence class.

### Axiom 5.1.A2 — The First Law of Thermodynamics

There exists a state function $U$ (internal energy) such that for any process connecting equilibrium states:

$$
dU = \delta Q - \delta W
$$

where $\delta Q$ is the heat absorbed by the system and $\delta W$ is the work done by the system. For a quasi-static process involving only $PdV$ work:

$$
dU = \delta Q - P\,dV
$$

Equivalently: the work done in an adiabatic process ($\delta Q = 0$) between two states depends only on the initial and final states, not on the path.

### Axiom 5.1.A3 — The Second Law of Thermodynamics

**Kelvin-Planck statement:** No cyclic process exists whose sole effect is the complete conversion of heat absorbed from a single thermal reservoir into work.

**Clausius statement:** No cyclic process exists whose sole effect is the transfer of heat from a colder body to a hotter body.

### Axiom 5.1.A4 — The Third Law of Thermodynamics (Nernst Heat Theorem)

As the temperature of a system approaches absolute zero, the entropy of the system approaches a universal constant (which may be taken as zero for a perfect crystal):

$$
\lim_{T \to 0^+} S(T) = 0
$$

**Consequence:** It is impossible to reach absolute zero in a finite number of operations.

---

## 🛡️ 3. Lemmas

### Lemma 5.1.1 — Existence of Temperature from the Zeroth Law

**Claim:** The Zeroth Law implies the existence of a scalar function $T$ (empirical temperature) that is uniform throughout systems in mutual thermal equilibrium.

**Proof.** The relation "is in thermal equilibrium with" ($\sim$) is:
- **Reflexive:** Any system is in equilibrium with itself ($A \sim A$).
- **Symmetric:** If $A \sim B$ then $B \sim A$ (equilibrium is mutual).
- **Transitive:** By the Zeroth Law, $A \sim B$ and $B \sim C$ imply $A \sim C$.

Therefore $\sim$ is an equivalence relation on the set of all thermodynamic systems. By the fundamental theorem of equivalence relations, this partitions all systems into disjoint equivalence classes. We assign a real number $\theta$ (empirical temperature) to each class. Two systems are in thermal equilibrium if and only if they share the same value of $\theta$. $\blacksquare$

### Lemma 5.1.2 — Internal Energy is a State Function

**Claim:** The First Law implies $U$ is path-independent (a state function).

**Proof.** Consider two paths $\gamma_1$ and $\gamma_2$ from state $A$ to state $B$. Construct a cycle: go from $A$ to $B$ via $\gamma_1$, then return from $B$ to $A$ via $\gamma_2$ reversed. For this cycle:

$$
\oint dU = \int_{\gamma_1} dU + \int_{\gamma_2^{-}} dU = 0
$$

The First Law for a cycle states $\Delta U_{\text{cycle}} = 0$ (since $U$ returns to its initial value). Therefore:

$$
\int_{\gamma_1} dU = -\int_{\gamma_2^{-}} dU = \int_{\gamma_2} dU
$$

Since the integral is the same for any two paths, $U$ depends only on the endpoints. Hence $dU$ is exact and $U$ is a state function. $\blacksquare$

### Lemma 5.1.3 — Work in Common Quasi-Static Processes

For $n$ moles of an ideal gas ($PV = nRT$):

**Isobaric** ($P = \text{const}$):

$$
W = \int_{V_1}^{V_2} P\,dV = P(V_2 - V_1) = nR(T_2 - T_1)
$$

**Isothermal** ($T = \text{const}$):

$$
W = \int_{V_1}^{V_2} \frac{nRT}{V}\,dV = nRT \ln\frac{V_2}{V_1}
$$

**Adiabatic** ($\delta Q = 0$, with $\gamma = C_P/C_V$):

$$
PV^\gamma = \text{const} \implies W = \frac{P_1 V_1 - P_2 V_2}{\gamma - 1} = \frac{nR(T_1 - T_2)}{\gamma - 1}
$$

**Derivation of the adiabatic relation $PV^\gamma = \text{const}$:**

From the First Law with $\delta Q = 0$:

$$
dU = -P\,dV
$$

For an ideal gas, $dU = nC_V\,dT$ and $PV = nRT$, so $P = nRT/V$. Substituting:

$$
nC_V\,dT = -\frac{nRT}{V}\,dV
$$

Separate variables:

$$
\frac{dT}{T} = -\frac{R}{C_V}\frac{dV}{V}
$$

Integrate both sides:

$$
\ln T = -\frac{R}{C_V}\ln V + \text{const}
$$

$$
\ln T + (\gamma - 1)\ln V = \text{const}
$$

where we used $R/C_V = (C_P - C_V)/C_V = \gamma - 1$. Exponentiating:

$$
TV^{\gamma-1} = \text{const}
$$

Using $T = PV/(nR)$:

$$
\frac{PV}{nR} \cdot V^{\gamma-1} = \text{const} \implies PV^\gamma = \text{const} \quad \blacksquare
$$

### Lemma 5.1.4 — Equivalence of Kelvin-Planck and Clausius Statements

**Claim:** The Kelvin-Planck and Clausius statements of the Second Law are logically equivalent.

**Proof (Kelvin-Planck $\implies$ Clausius by contrapositive):**

Assume the Clausius statement is violated: there exists a device $\mathcal{R}$ that transfers heat $Q_C$ from a cold reservoir at $T_C$ to a hot reservoir at $T_H$ with no other effect. Now operate a Carnot engine between $T_H$ and $T_C$ that absorbs $Q_H$ from the hot reservoir, rejects $Q_C$ to the cold reservoir, and produces work $W = Q_H - Q_C$.

Combine $\mathcal{R}$ with the Carnot engine: the cold reservoir experiences zero net heat exchange ($Q_C$ out via $\mathcal{R}$, $Q_C$ in from engine). The composite device absorbs $Q_H - Q_C$ from the hot reservoir and converts it entirely to work $W$. This violates Kelvin-Planck.

**Proof (Clausius $\implies$ Kelvin-Planck by contrapositive):**

Assume Kelvin-Planck is violated: there exists an engine $\mathcal{E}$ that absorbs $Q_H$ from a hot reservoir and converts it entirely to work ($W = Q_H$, $Q_C = 0$). Use this work to drive a refrigerator that extracts $Q_C$ from the cold reservoir and rejects $Q_C + W = Q_C + Q_H$ to the hot reservoir.

Net effect: heat $Q_C$ is transferred from cold to hot with no work input (the work from $\mathcal{E}$ is internal). This violates Clausius. $\blacksquare$

---

## 👑 4. Theorems

### Theorem 5.1.1 — Carnot's Theorem

No heat engine operating between two thermal reservoirs at temperatures $T_H$ and $T_C$ ($T_H > T_C$) can be more efficient than a reversible (Carnot) engine operating between the same reservoirs:

$$
\eta \leq \eta_{\text{Carnot}} = 1 - \frac{T_C}{T_H}
$$

with equality if and only if the engine is reversible.

### Theorem 5.1.2 — Clausius Inequality

For any cyclic process:

$$
\oint \frac{\delta Q}{T} \leq 0
$$

with equality holding if and only if the process is reversible.

### Theorem 5.1.3 — Existence of Entropy

There exists a state function $S$ (entropy) such that for any reversible process:

$$
dS = \frac{\delta Q_{\text{rev}}}{T}
$$

For an irreversible process between the same endpoints:

$$
\Delta S > \int \frac{\delta Q_{\text{irrev}}}{T}
$$

### Theorem 5.1.4 — $C_P - C_V$ Relation for Ideal Gas

For $n$ moles of an ideal gas:

$$
C_P - C_V = nR
$$

### Theorem 5.1.5 — Third Law Consequence: Vanishing Heat Capacity

As $T \to 0$:

$$
C_V \to 0 \quad \text{and} \quad C_P \to 0
$$


---

## ✍️ 5. Proofs / Derivations

### 5.1 Proof of Carnot's Theorem

**Claim:** No engine operating between $T_H$ and $T_C$ can exceed the Carnot efficiency.

**Proof by contradiction.** Suppose an engine $\mathcal{E}$ has efficiency $\eta_{\mathcal{E}} > \eta_C$ where $\eta_C = 1 - T_C/T_H$. Let $\mathcal{E}$ absorb $Q_H$ from the hot reservoir, produce work $W = \eta_{\mathcal{E}} Q_H$, and reject $Q_C = Q_H - W$ to the cold reservoir.

Now run a Carnot engine $\mathcal{C}$ in reverse (as a refrigerator) between the same reservoirs, using work $W' = W$ to extract heat $Q_C'$ from the cold reservoir and deliver $Q_H' = Q_C' + W'$ to the hot reservoir.

For the reversed Carnot engine: $\eta_C = W'/Q_H'$, so $Q_H' = W/\eta_C$.

Since $\eta_{\mathcal{E}} > \eta_C$, we have $W = \eta_{\mathcal{E}} Q_H > \eta_C Q_H$, and:

$$
Q_H' = \frac{W}{\eta_C} = \frac{\eta_{\mathcal{E}}}{\eta_C} Q_H > Q_H
$$

The composite system (engine $\mathcal{E}$ + reversed Carnot $\mathcal{C}$) produces zero net work. The hot reservoir loses $Q_H$ and gains $Q_H' > Q_H$, so it gains net heat $Q_H' - Q_H > 0$. The cold reservoir loses net heat $Q_H' - Q_H > 0$.

Net effect: heat flows from cold to hot with no work input. This violates the Clausius statement of the Second Law. Contradiction. Therefore $\eta_{\mathcal{E}} \leq \eta_C$.

For the equality case: if $\mathcal{E}$ is itself reversible, run it in reverse and apply the same argument with roles swapped to get $\eta_C \leq \eta_{\mathcal{E}}$. Combined: $\eta_{\mathcal{E}} = \eta_C$. $\blacksquare$

### 5.2 Proof of the Clausius Inequality

**Claim:** For any cyclic process, $\oint \frac{\delta Q}{T} \leq 0$.

**Proof.** Consider an arbitrary cyclic process undergone by system $\Sigma$. At each infinitesimal stage, the system exchanges heat $\delta Q$ with a reservoir at temperature $T_R$ (the reservoir temperature at the boundary).

Replace each reservoir interaction with a Carnot engine operating between a master reservoir at temperature $T_0$ and the local reservoir at $T_R$. The Carnot engine absorbs $\delta Q_0$ from the master reservoir and delivers $\delta Q$ to the system, with:

$$
\frac{\delta Q_0}{T_0} = \frac{\delta Q}{T_R}
$$

(This follows from the Carnot efficiency relation applied to the infinitesimal engine.)

Over the full cycle, the total heat extracted from the master reservoir is:

$$
Q_0 = \oint \delta Q_0 = T_0 \oint \frac{\delta Q}{T_R}
$$

The composite system (original system $\Sigma$ + all Carnot engines) undergoes a cycle. By the Kelvin-Planck statement, the net work produced cannot exceed zero if the only heat source is the master reservoir. Since the composite extracts $Q_0$ from the master reservoir and converts it to work:

$$
Q_0 \leq 0 \implies T_0 \oint \frac{\delta Q}{T_R} \leq 0
$$

Since $T_0 > 0$:

$$
\oint \frac{\delta Q}{T_R} \leq 0 \quad \blacksquare
$$

For a reversible process, run the cycle in reverse: $\oint \frac{\delta Q_{\text{rev}}}{T} \geq 0$. Combined with the inequality: $\oint \frac{\delta Q_{\text{rev}}}{T} = 0$.

### 5.3 Derivation of Entropy as a State Function

From the Clausius inequality, for a reversible cycle:

$$
\oint \frac{\delta Q_{\text{rev}}}{T} = 0
$$

This means the integral $\int_A^B \frac{\delta Q_{\text{rev}}}{T}$ is path-independent (for reversible paths). Define:

$$
S(B) - S(A) \equiv \int_A^B \frac{\delta Q_{\text{rev}}}{T}
$$

This defines a state function $S$ (up to an additive constant). In differential form:

$$
dS = \frac{\delta Q_{\text{rev}}}{T}
$$

For an irreversible process from $A$ to $B$, consider a cycle: irreversible $A \to B$, then reversible $B \to A$:

$$
\int_A^B \frac{\delta Q_{\text{irrev}}}{T} + \int_B^A \frac{\delta Q_{\text{rev}}}{T} \leq 0
$$

$$
\int_A^B \frac{\delta Q_{\text{irrev}}}{T} - [S(B) - S(A)] \leq 0
$$

$$
S(B) - S(A) \geq \int_A^B \frac{\delta Q_{\text{irrev}}}{T} \quad \blacksquare
$$

### 5.4 Proof of $C_P - C_V = nR$ for an Ideal Gas

**Starting point:** The enthalpy $H = U + PV$. For an ideal gas, $PV = nRT$, so $H = U + nRT$.

Differentiate with respect to $T$ at constant $P$:

$$
\left(\frac{\partial H}{\partial T}\right)_P = \left(\frac{\partial U}{\partial T}\right)_P + nR
$$

The left side is $C_P$ by definition. For the right side, we need $(\partial U/\partial T)_P$.

For an ideal gas, $U$ depends only on $T$ (proved from the Joule expansion experiment and the equation of state): $U = U(T)$ only. Therefore:

$$
\left(\frac{\partial U}{\partial T}\right)_P = \frac{dU}{dT} = \left(\frac{\partial U}{\partial T}\right)_V = C_V
$$

Substituting:

$$
C_P = C_V + nR \implies C_P - C_V = nR \quad \blacksquare
$$

### 5.5 General $C_P - C_V$ Relation (Non-Ideal Systems)

For a general system, starting from $H = U + PV$:

$$
C_P - C_V = \left(\frac{\partial H}{\partial T}\right)_P - \left(\frac{\partial U}{\partial T}\right)_V
$$

Using $dU = TdS - PdV$:

$$
\left(\frac{\partial U}{\partial T}\right)_V = T\left(\frac{\partial S}{\partial T}\right)_V
$$

Using $dH = TdS + VdP$:

$$
\left(\frac{\partial H}{\partial T}\right)_P = T\left(\frac{\partial S}{\partial T}\right)_P
$$

Therefore:

$$
C_P - C_V = T\left[\left(\frac{\partial S}{\partial T}\right)_P - \left(\frac{\partial S}{\partial T}\right)_V\right]
$$

Now use the chain rule. Since $S = S(T, V)$ and $V = V(T, P)$:

$$
\left(\frac{\partial S}{\partial T}\right)_P = \left(\frac{\partial S}{\partial T}\right)_V + \left(\frac{\partial S}{\partial V}\right)_T \left(\frac{\partial V}{\partial T}\right)_P
$$

Substituting:

$$
C_P - C_V = T\left(\frac{\partial S}{\partial V}\right)_T \left(\frac{\partial V}{\partial T}\right)_P
$$

Apply the Maxwell relation from the Helmholtz free energy (see [5.3 - Thermodynamic Potentials & Maxwell Relations](5.3---Thermodynamic-Potentials-&-Maxwell-Relations)):

$$
\left(\frac{\partial S}{\partial V}\right)_T = \left(\frac{\partial P}{\partial T}\right)_V
$$

Therefore:

$$
C_P - C_V = T\left(\frac{\partial P}{\partial T}\right)_V \left(\frac{\partial V}{\partial T}\right)_P
$$

Using the cyclic relation $\left(\frac{\partial P}{\partial T}\right)_V \left(\frac{\partial T}{\partial V}\right)_P \left(\frac{\partial V}{\partial P}\right)_T = -1$:

$$
\left(\frac{\partial P}{\partial T}\right)_V = -\left(\frac{\partial V}{\partial T}\right)_P \bigg/ \left(\frac{\partial V}{\partial P}\right)_T
$$

Define the thermal expansion coefficient $\alpha = \frac{1}{V}\left(\frac{\partial V}{\partial T}\right)_P$ and isothermal compressibility $\kappa_T = -\frac{1}{V}\left(\frac{\partial V}{\partial P}\right)_T$. Then:

$$
C_P - C_V = \frac{TV\alpha^2}{\kappa_T} \quad \blacksquare
$$

For an ideal gas: $\alpha = 1/T$, $\kappa_T = 1/P$, $V = nRT/P$, giving $C_P - C_V = \frac{T \cdot (nRT/P) \cdot (1/T)^2}{1/P} = nR$. ✓

### 5.6 Proof: Third Law Implies $C_V \to 0$ as $T \to 0$

From the definition of entropy:

$$
S(T) - S(0) = \int_0^T \frac{C_V(T')}{T'}\,dT'
$$

By the Third Law, $S(0) = 0$, so:

$$
S(T) = \int_0^T \frac{C_V(T')}{T'}\,dT'
$$

For this integral to converge as $T \to 0$ (i.e., for $S$ to remain finite), we require $C_V(T)/T \to 0$ faster than $1/T$ diverges. Specifically, if $C_V \to C_0 > 0$ as $T \to 0$, then:

$$
S(T) \approx C_0 \int_0^T \frac{dT'}{T'} = C_0 \ln T \to -\infty
$$

which contradicts $S(T) \geq S(0) = 0$ for a system at positive temperature. Therefore $C_V \to 0$ as $T \to 0$.

More precisely, $C_V$ must vanish at least as fast as $T^\alpha$ for some $\alpha > 0$. Experimentally, for solids $C_V \propto T^3$ (Debye model) and for metals $C_V \propto T$ (electronic contribution) at low temperatures. $\blacksquare$

### 5.7 Derivation of the Thermodynamic Temperature Scale

**Claim:** The Carnot efficiency defines an absolute temperature scale independent of the working substance.

Consider two Carnot engines: $\mathcal{C}_1$ operating between $T_1$ (hot) and $T_2$ (cold), and $\mathcal{C}_2$ operating between $T_2$ (hot) and $T_3$ (cold), with $T_1 > T_2 > T_3$.

For $\mathcal{C}_1$: $\frac{Q_1}{Q_2} = f(T_1, T_2)$ where $f$ is some universal function (by Carnot's theorem, independent of working substance).

For $\mathcal{C}_2$: $\frac{Q_2}{Q_3} = f(T_2, T_3)$.

A composite engine operating between $T_1$ and $T_3$: $\frac{Q_1}{Q_3} = f(T_1, T_3)$.

But also $\frac{Q_1}{Q_3} = \frac{Q_1}{Q_2} \cdot \frac{Q_2}{Q_3} = f(T_1, T_2) \cdot f(T_2, T_3)$.

Therefore: $f(T_1, T_3) = f(T_1, T_2) \cdot f(T_2, T_3)$.

This functional equation has the solution $f(T_a, T_b) = \frac{g(T_a)}{g(T_b)}$ for some function $g$. Kelvin's choice: $g(T) = T$ (the thermodynamic temperature). Then:

$$
\frac{Q_H}{Q_C} = \frac{T_H}{T_C} \implies \eta = 1 - \frac{Q_C}{Q_H} = 1 - \frac{T_C}{T_H} \quad \blacksquare
$$


---

## 🧮 6. Worked Examples

### Example 5.1.E1 — Isothermal Expansion of an Ideal Gas

An ideal gas ($n = 2$ mol) expands isothermally at $T = 300\,\text{K}$ from $V_1 = 10\,\text{L}$ to $V_2 = 30\,\text{L}$. Compute the work done, heat absorbed, and change in internal energy.

**Solution:**

Since the process is isothermal and the gas is ideal, $\Delta U = 0$ (internal energy of an ideal gas depends only on $T$).

By the First Law: $\Delta U = Q - W = 0 \implies Q = W$.

The work done by the gas in an isothermal quasi-static expansion:

$$
W = \int_{V_1}^{V_2} P\,dV = \int_{V_1}^{V_2} \frac{nRT}{V}\,dV = nRT \ln\frac{V_2}{V_1}
$$

Substituting numerical values ($R = 8.314\,\text{J/(mol·K)}$):

$$
W = (2)(8.314)(300)\ln\frac{30}{10} = 4988.4 \times \ln 3 = 4988.4 \times 1.0986 = 5480\,\text{J}
$$

Therefore: $W = Q = 5480\,\text{J}$, $\Delta U = 0$.

**Physical interpretation:** All the heat absorbed from the reservoir goes directly into work against the external pressure. The gas maintains constant temperature by absorbing exactly enough heat to compensate for the energy expended as work.

---

### Example 5.1.E2 — Adiabatic Compression

A monatomic ideal gas ($\gamma = 5/3$, $n = 1$ mol) at $T_1 = 300\,\text{K}$, $V_1 = 20\,\text{L}$ is compressed adiabatically to $V_2 = 5\,\text{L}$. Find $T_2$, $P_2$, and the work done on the gas.

**Solution:**

For an adiabatic process with an ideal gas: $TV^{\gamma-1} = \text{const}$.

$$
T_1 V_1^{\gamma-1} = T_2 V_2^{\gamma-1}
$$

$$
T_2 = T_1 \left(\frac{V_1}{V_2}\right)^{\gamma-1} = 300 \left(\frac{20}{5}\right)^{2/3} = 300 \times 4^{2/3}
$$

Compute $4^{2/3} = (2^2)^{2/3} = 2^{4/3} = 2 \times 2^{1/3} = 2 \times 1.2599 = 2.5198$.

$$
T_2 = 300 \times 2.5198 = 756\,\text{K}
$$

For the pressure, use $PV^\gamma = \text{const}$ or the ideal gas law:

$$
P_2 = \frac{nRT_2}{V_2} = \frac{(1)(8.314)(756)}{0.005} = \frac{6285}{0.005} = 1.257 \times 10^6\,\text{Pa} = 12.4\,\text{atm}
$$

Work done on the gas ($\delta Q = 0$, so $W_{\text{on}} = \Delta U$):

$$
W_{\text{on}} = nC_V(T_2 - T_1) = (1)\left(\frac{3}{2} \times 8.314\right)(756 - 300) = 12.471 \times 456 = 5687\,\text{J}
$$

---

### Example 5.1.E3 — Proving $\delta Q$ is Not a State Function

Show that for an ideal gas taken from state $(T_1, V_1)$ to $(T_2, V_2)$ via two different paths, the heat exchanged differs.

**Path A:** Isothermal expansion at $T_1$ from $V_1$ to $V_2$, then isochoric heating from $T_1$ to $T_2$ at $V_2$.

**Path B:** Isochoric heating from $T_1$ to $T_2$ at $V_1$, then isothermal expansion at $T_2$ from $V_1$ to $V_2$.

**Solution:**

**Path A:**
- Step 1 (isothermal, $\Delta U = 0$): $Q_1 = W_1 = nRT_1 \ln(V_2/V_1)$
- Step 2 (isochoric, $W = 0$): $Q_2 = \Delta U = nC_V(T_2 - T_1)$
- Total: $Q_A = nRT_1 \ln(V_2/V_1) + nC_V(T_2 - T_1)$

**Path B:**
- Step 1 (isochoric, $W = 0$): $Q_1 = nC_V(T_2 - T_1)$
- Step 2 (isothermal, $\Delta U = 0$): $Q_2 = nRT_2 \ln(V_2/V_1)$
- Total: $Q_B = nC_V(T_2 - T_1) + nRT_2 \ln(V_2/V_1)$

Comparing:

$$
Q_B - Q_A = nR(T_2 - T_1)\ln\frac{V_2}{V_1} \neq 0 \quad (\text{if } T_2 \neq T_1 \text{ and } V_2 \neq V_1)
$$

Therefore $Q$ is path-dependent: $\delta Q$ is an inexact differential. Note that $\Delta U = Q - W$ is the same for both paths (as it must be for a state function):

$$
\Delta U_A = \Delta U_B = nC_V(T_2 - T_1) \quad \checkmark
$$

---

### Example 5.1.E4 — Verifying the Exact Differential Criterion

Show that $dU = C_V\,dT + \left[T\left(\frac{\partial P}{\partial T}\right)_V - P\right]dV$ is exact for a van der Waals gas.

**Solution:**

The van der Waals equation: $\left(P + \frac{a}{V^2}\right)(V - b) = RT$ (for 1 mol).

Solve for $P$: $P = \frac{RT}{V-b} - \frac{a}{V^2}$.

Compute $\left(\frac{\partial P}{\partial T}\right)_V = \frac{R}{V-b}$.

The coefficient of $dV$ in the energy differential:

$$
T\left(\frac{\partial P}{\partial T}\right)_V - P = \frac{RT}{V-b} - \left(\frac{RT}{V-b} - \frac{a}{V^2}\right) = \frac{a}{V^2}
$$

So $dU = C_V\,dT + \frac{a}{V^2}\,dV$.

Check exactness: let $M = C_V$ and $N = a/V^2$.

$$
\frac{\partial M}{\partial V}\bigg|_T = \frac{\partial C_V}{\partial V}\bigg|_T
$$

$$
\frac{\partial N}{\partial T}\bigg|_V = \frac{\partial}{\partial T}\left(\frac{a}{V^2}\right)_V = 0
$$

For exactness we need $\frac{\partial C_V}{\partial V}\big|_T = 0$. This is indeed true for a van der Waals gas (can be verified from the equation of state), confirming $dU$ is exact. $\blacksquare$

---

### Example 5.1.E5 — Entropy Change in Free Expansion

An ideal gas undergoes free expansion (Joule expansion) into vacuum, doubling its volume: $V_2 = 2V_1$. The process is adiabatic ($Q = 0$) and no work is done ($W = 0$, expansion into vacuum). Find $\Delta S$.

**Solution:**

Since $Q = 0$ and $W = 0$: $\Delta U = 0$, hence $T_2 = T_1$ (ideal gas).

The process is irreversible (not quasi-static). To compute $\Delta S$, we use a reversible path between the same initial and final states: an isothermal expansion from $V_1$ to $V_2 = 2V_1$ at temperature $T$.

$$
\Delta S = \int_1^2 \frac{\delta Q_{\text{rev}}}{T} = \frac{1}{T}\int_{V_1}^{2V_1} P\,dV = \frac{nR}{T} \cdot T \ln 2 = nR\ln 2
$$

Wait — let us be more careful. For the reversible isothermal path:

$$
\delta Q_{\text{rev}} = dU + P\,dV = 0 + P\,dV = \frac{nRT}{V}\,dV
$$

$$
\Delta S = \int_{V_1}^{2V_1} \frac{nRT/V}{T}\,dV = nR\int_{V_1}^{2V_1}\frac{dV}{V} = nR\ln 2 > 0
$$

The entropy increases even though no heat was exchanged in the actual process. This is the hallmark of irreversibility: $\Delta S_{\text{universe}} = \Delta S_{\text{system}} = nR\ln 2 > 0$ (the surroundings are unchanged). $\blacksquare$

---

## 🔗 7. Cross-links & Further Reading

### Internal Cross-links
- Entropy and the Second Law developed fully: [5.2 - Entropy & Heat Engines](5.2---Entropy-&-Heat-Engines)
- Thermodynamic potentials and Maxwell relations: [5.3 - Thermodynamic Potentials & Maxwell Relations](5.3---Thermodynamic-Potentials-&-Maxwell-Relations)
- Statistical interpretation of temperature ($\beta = 1/k_BT$): [5.5 - Classical Statistical Mechanics - Microstates & Ensembles](5.5---Classical-Statistical-Mechanics---Microstates-&-Ensembles)
- Multivariable calculus (exact differentials, chain rule): [1.4 - Multivariable Calculus & Vector Analysis](1.4---Multivariable-Calculus-&-Vector-Analysis)
- ODEs for adiabatic processes: [3.1 - First-Order ODEs & Separable Equations](3.1---First-Order-ODEs-&-Separable-Equations)

### Authoritative Sources
- **Kittel & Kroemer**, *Thermal Physics*, Ch. 1–3 (canonical treatment of temperature and entropy)
- **Callen**, *Thermodynamics and an Introduction to Thermostatistics*, Ch. 1–4 (axiomatic approach)
- **Fermi**, *Thermodynamics* (elegant, concise derivations of all four laws)
- **Susskind & Hrabovsky**, *The Theoretical Minimum: Classical Mechanics* → Statistical Mechanics lectures
- [MIT OCW 8.333](https://ocw.mit.edu/courses/8-333-statistical-mechanics-i-statistical-mechanics-of-particles-fall-2013/) — Graduate statistical mechanics



---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — Ideal Gas Thermometer Calibration

**Problem.** A constant-volume gas thermometer uses helium at low pressure. At the triple point of water ($T_{\text{tp}} = 273.16\,\text{K}$), the pressure reads $P_{\text{tp}} = 48.00\,\text{Torr}$. When placed in thermal contact with an unknown system, the pressure reads $P = 64.37\,\text{Torr}$. (a) Determine the unknown temperature. (b) Estimate the systematic error if the gas were nitrogen instead of helium, given that nitrogen's second virial coefficient at this temperature is $B(T) = -4.2\,\text{cm}^3/\text{mol}$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Part (a): Ideal Gas Thermometer Reading

The constant-volume gas thermometer defines temperature via:

$$
T = T_{\text{tp}} \cdot \lim_{P_{\text{tp}}\to 0}\frac{P}{P_{\text{tp}}}
$$

In the ideal gas limit (helium at low pressure is nearly ideal):

$$
T = 273.16\,\text{K} \times \frac{P}{P_{\text{tp}}} = 273.16 \times \frac{64.37}{48.00}
$$

Compute the ratio:

$$
\frac{64.37}{48.00} = 1.34104
$$

Therefore:

$$
T = 273.16 \times 1.34104 = 366.3\,\text{K}
$$

#### Part (b): Systematic Error from Non-Ideal Gas

For a real gas, the equation of state to first order in density is:

$$
PV = nRT\left(1 + \frac{B(T)}{V/n}\right)
$$

At constant volume, the pressure ratio $P/P_{\text{tp}}$ is not exactly $T/T_{\text{tp}}$ but includes a correction:

$$
\frac{P}{P_{\text{tp}}} = \frac{T}{T_{\text{tp}}} \cdot \frac{1 + B(T)/(V/n)}{1 + B(T_{\text{tp}})/(V/n)}
$$

For nitrogen at these conditions, $B(T) \approx -4.2\,\text{cm}^3/\text{mol}$ and $B(T_{\text{tp}}) \approx -10.5\,\text{cm}^3/\text{mol}$ (nitrogen's virial coefficient is more negative at lower temperatures).

The molar volume at the triple point: $V/n = RT_{\text{tp}}/P_{\text{tp}}$. Convert $P_{\text{tp}} = 48\,\text{Torr} = 6400\,\text{Pa}$:

$$
V/n = \frac{8.314 \times 273.16}{6400} = 355\,\text{cm}^3/\text{mol} = 3.55 \times 10^{-4}\,\text{m}^3/\text{mol}
$$

The correction factor:

$$
\frac{1 + (-4.2/355)}{1 + (-10.5/355)} = \frac{1 - 0.01183}{1 - 0.02958} = \frac{0.9882}{0.9704} = 1.0183
$$

The apparent temperature reading would be:

$$
T_{\text{apparent}} = T_{\text{true}} \times 1.0183 = 366.3 \times 1.0183 = 373.0\,\text{K}
$$

Systematic error: $\Delta T = 373.0 - 366.3 = 6.7\,\text{K}$, or about $1.8\%$.

This is why helium (with $B \approx +12\,\text{cm}^3/\text{mol}$, much smaller in magnitude) is preferred for gas thermometry — its deviations from ideality are minimal even at moderate pressures.

</details>

---

### Example 8.2 — First Law Applied to Free Expansion of an Ideal Gas

**Problem.** One mole of an ideal monatomic gas ($C_V = \frac{3}{2}R$) initially at $T_1 = 500\,\text{K}$, $V_1 = 10\,\text{L}$, $P_1 = 4.157\,\text{atm}$ undergoes free expansion into an evacuated container, reaching final volume $V_2 = 30\,\text{L}$. (a) Find $T_2$, $P_2$, $\Delta U$, $Q$, and $W$. (b) Compute $\Delta S$ for the gas. (c) Explain why this process is irreversible despite $\Delta U = 0$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Part (a): Applying the First Law

In free expansion, the gas expands into vacuum. There is no piston, no external pressure to push against:

$$
W = \int P_{\text{ext}}\,dV = \int 0\,dV = 0
$$

The container is rigid and insulated (adiabatic walls):

$$
Q = 0
$$

By the First Law:

$$
\Delta U = Q - W = 0 - 0 = 0
$$

For an ideal gas, $U = U(T)$ only (internal energy depends only on temperature). Since $\Delta U = 0$:

$$
T_2 = T_1 = 500\,\text{K}
$$

The final pressure from the ideal gas law:

$$
P_2 = \frac{nRT_2}{V_2} = \frac{(1)(0.08206)(500)}{30} = 1.368\,\text{atm}
$$

Alternatively: $P_2 = P_1 \cdot V_1/V_2 = 4.157 \times 10/30 = 1.386\,\text{atm}$.

(Small discrepancy from rounding; exact: $P_2 = P_1/3$.)

**Summary:** $T_2 = 500\,\text{K}$, $P_2 = P_1/3 = 1.386\,\text{atm}$, $\Delta U = 0$, $Q = 0$, $W = 0$.

#### Part (b): Entropy Change

The actual process is irreversible, so we cannot use $\Delta S = \int \delta Q/T$ along the actual path. Instead, we construct a reversible path between the same initial and final states.

Since $T_1 = T_2$ and $V_2 = 3V_1$, we use a reversible isothermal expansion:

$$
\Delta S = \int_{V_1}^{V_2} \frac{\delta Q_{\text{rev}}}{T}
$$

For a reversible isothermal process on an ideal gas: $\delta Q_{\text{rev}} = P\,dV = \frac{nRT}{V}\,dV$.

$$
\Delta S = \int_{V_1}^{3V_1} \frac{nRT/V}{T}\,dV = nR\int_{V_1}^{3V_1}\frac{dV}{V} = nR\ln\frac{3V_1}{V_1} = nR\ln 3
$$

$$
\Delta S = (1)(8.314)\ln 3 = 8.314 \times 1.0986 = 9.13\,\text{J/K}
$$

#### Part (c): Irreversibility

The process is irreversible because:

1. **It is not quasi-static:** The gas rushes into the vacuum — there is no sequence of equilibrium states connecting initial to final.
2. **Entropy of the universe increases:** $\Delta S_{\text{universe}} = \Delta S_{\text{gas}} + \Delta S_{\text{surroundings}} = nR\ln 3 + 0 = nR\ln 3 \gt  0$.
3. **It cannot be reversed without external work:** To compress the gas back to $V_1$ isothermally, we would need to do work $W = nRT\ln 3$ and reject heat $Q = nRT\ln 3$ to a reservoir, increasing the reservoir's entropy.

The key insight: $\Delta U = 0$ does NOT imply reversibility. Irreversibility is diagnosed by $\Delta S_{\text{universe}} \gt  0$, not by energy changes.

</details>

---

### Example 8.3 — Non-Ideal Gas (van der Waals) Isothermal Compression

**Problem.** One mole of CO₂ (van der Waals constants: $a = 3.59\,\text{L}^2\text{·atm/mol}^2$, $b = 0.0427\,\text{L/mol}$) is compressed isothermally at $T = 500\,\text{K}$ from $V_1 = 20\,\text{L}$ to $V_2 = 2\,\text{L}$. (a) Calculate the work done ON the gas. (b) Calculate $\Delta U$. (c) Calculate the heat exchanged $Q$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Part (a): Work Done on the Gas

The van der Waals equation for 1 mole:

$$
P = \frac{RT}{V - b} - \frac{a}{V^2}
$$

Work done BY the gas during compression (note $V_2 \lt  V_1$, so work done by gas is negative):

$$
W_{\text{by gas}} = \int_{V_1}^{V_2} P\,dV = \int_{20}^{2}\left(\frac{RT}{V-b} - \frac{a}{V^2}\right)dV
$$

Evaluate each integral separately:

**First integral:**

$$
\int_{20}^{2}\frac{RT}{V-b}\,dV = RT\ln\frac{V_2 - b}{V_1 - b} = (0.08206)(500)\ln\frac{2 - 0.0427}{20 - 0.0427}
$$

$$
= 41.03\ln\frac{1.9573}{19.9573} = 41.03\ln(0.09804) = 41.03 \times (-2.3226) = -95.30\,\text{L·atm}
$$

**Second integral:**

$$
\int_{20}^{2}\frac{-a}{V^2}\,dV = -a\left[-\frac{1}{V}\right]_{20}^{2} = a\left(\frac{1}{V_2} - \frac{1}{V_1}\right) \cdot (-1)
$$

Wait — let's be careful with signs:

$$
\int_{20}^{2}\left(-\frac{a}{V^2}\right)dV = -a\int_{20}^{2}\frac{dV}{V^2} = -a\left[-\frac{1}{V}\right]_{20}^{2} = -a\left(-\frac{1}{2} + \frac{1}{20}\right) = -a\left(-\frac{9}{20}\right) = \frac{9a}{20}
$$

$$
= \frac{9 \times 3.59}{20} = 1.616\,\text{L·atm}
$$

**Total work done by gas:**

$$
W_{\text{by gas}} = -95.30 + 1.616 = -93.68\,\text{L·atm}
$$

Convert to Joules: $W_{\text{by gas}} = -93.68 \times 101.325 = -9492\,\text{J}$.

**Work done ON the gas:** $W_{\text{on gas}} = -W_{\text{by gas}} = +9492\,\text{J} = 9.49\,\text{kJ}$.

#### Part (b): Internal Energy Change

For a van der Waals gas, we showed in Example 5.1.E4 that:

$$
\left(\frac{\partial U}{\partial V}\right)_T = \frac{a}{V^2}
$$

At constant temperature:

$$
\Delta U = \int_{V_1}^{V_2}\frac{a}{V^2}\,dV = a\left[-\frac{1}{V}\right]_{20}^{2} = a\left(-\frac{1}{2} + \frac{1}{20}\right) = -\frac{9a}{20}
$$

$$
\Delta U = -\frac{9 \times 3.59}{20}\,\text{L·atm} = -1.616\,\text{L·atm} = -163.7\,\text{J}
$$

Note: $\Delta U \lt  0$ because the molecules are being pushed closer together, and the attractive interactions ($a/V^2$ term) mean the potential energy decreases (becomes more negative) as volume decreases. Wait — actually let's reconsider the sign.

Going from $V_1 = 20$ to $V_2 = 2$ (compression):

$$
\Delta U = a\left(-\frac{1}{2} + \frac{1}{20}\right) = a\left(\frac{1-10}{20}\right) = -\frac{9a}{20} = -\frac{9(3.59)}{20} = -1.616\,\text{L·atm}
$$

Converting: $\Delta U = -1.616 \times 101.325 = -163.7\,\text{J}$.

Actually, this is the energy change due to intermolecular attractions. When molecules get closer, the attractive potential energy decreases (more negative), so $\Delta U \lt  0$ makes physical sense.

#### Part (c): Heat Exchanged

From the First Law: $\Delta U = Q - W_{\text{by gas}}$ (sign convention: $W$ is work done BY the system):

$$
Q = \Delta U + W_{\text{by gas}} = -163.7 + (-9492) = -9656\,\text{J} = -9.66\,\text{kJ}
$$

The negative sign means heat flows OUT of the gas. This makes sense: during isothermal compression, the gas must reject heat to maintain constant temperature. The magnitude is slightly less than for an ideal gas (which would give $Q = W_{\text{by gas}} = -9492\,\text{J}$) because the van der Waals gas releases some internal energy as molecules are pushed closer.

**Comparison with ideal gas:**
- Ideal gas: $W_{\text{on}} = nRT\ln(V_1/V_2) = (1)(8.314)(500)\ln(10) = 9572\,\text{J}$, $\Delta U = 0$, $Q = -9572\,\text{J}$.
- Van der Waals: $W_{\text{on}} = 9492\,\text{J}$, $\Delta U = -164\,\text{J}$, $Q = -9656\,\text{J}$.

The differences are small because at $T = 500\,\text{K}$ and these volumes, CO₂ is not far from ideal.

</details>

---

### Example 8.4 — Third Law: Entropy at Absolute Zero and Residual Entropy of Ice

**Problem.** (a) Using the Third Law, show that the heat capacity $C_V \to 0$ as $T \to 0$. (b) Ordinary ice (Ih) has a residual entropy of approximately $S_0 = R\ln(3/2) \approx 3.37\,\text{J/(mol·K)}$ at $T = 0$ (Pauling's estimate). Explain the origin of this residual entropy and why it does not violate the Third Law.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Part (a): $C_V \to 0$ as $T \to 0$

The Third Law states: $S(T=0) = 0$ for a perfect crystal. The entropy at temperature $T$ is:

$$
S(T) = S(0) + \int_0^T \frac{C_V}{T'}\,dT' = \int_0^T \frac{C_V}{T'}\,dT'
$$

For this integral to converge (i.e., for $S(T)$ to be finite), we need the integrand $C_V/T$ to be integrable near $T = 0$. If $C_V$ approached a nonzero constant $C_0$ as $T \to 0$, then:

$$
\int_0^T \frac{C_0}{T'}\,dT' = C_0\ln T \to -\infty \quad \text{as } T \to 0^+
$$

This would give $S(T) = -\infty$, contradicting $S(0) = 0$ (finite). Therefore $C_V$ must vanish as $T \to 0$.

More precisely, if $C_V \sim T^\alpha$ as $T \to 0$ with $\alpha \gt  0$, then:

$$
\int_0^T \frac{T'^\alpha}{T'}\,dT' = \int_0^T T'^{\alpha-1}\,dT' = \frac{T^\alpha}{\alpha} \lt  \infty
$$

This converges for any $\alpha \gt  0$. Experimentally:
- Metals: $C_V \sim \gamma T$ (electronic) $+ AT^3$ (phonon) → $\alpha = 1$.
- Insulators: $C_V \sim T^3$ (Debye) → $\alpha = 3$.

Both satisfy the Third Law requirement. $\blacksquare$

#### Part (b): Residual Entropy of Ice

**Origin:** In ice Ih, each oxygen atom is tetrahedrally coordinated with four neighbors. Along each O–O bond, there is exactly one hydrogen atom, positioned closer to one oxygen or the other. The "ice rules" (Bernal-Fowler rules) require:
1. Exactly one H on each O–O bond.
2. Exactly two H atoms close to each O (forming H₂O).

The number of configurations satisfying these constraints is not 1 (not a unique ground state), but approximately $(3/2)^N$ for $N$ molecules (Pauling, 1935).

**Pauling's counting argument:**

Each oxygen has 4 bonds. Each bond has 2 possible H positions. Total unconstrained configurations: $2^{2N}$ (since there are $2N$ bonds for $N$ molecules in the ice lattice). The constraint "exactly 2 of 4 bonds have H close" is satisfied by $\binom{4}{2} = 6$ out of $2^4 = 16$ arrangements per oxygen:

$$
\Omega \approx 2^{2N} \times \left(\frac{6}{16}\right)^N = 4^N \times \left(\frac{3}{8}\right)^N = \left(\frac{3}{2}\right)^N
$$

$$
S_0 = k_B\ln\Omega = Nk_B\ln\frac{3}{2} = R\ln\frac{3}{2} \approx 3.37\,\text{J/(mol·K)}
$$

**Why this doesn't violate the Third Law:** The Third Law applies to *perfect crystals* — systems with a unique ground state. Ice Ih is a *frustrated* system: the ice rules create an exponentially large number of energetically equivalent ground states. The system is "frozen" into one of these configurations and cannot explore the others at $T = 0$ (the relaxation time diverges). The residual entropy reflects this configurational degeneracy.

Strictly, the Nernst-Planck statement of the Third Law says $S \to 0$ for a system in *internal equilibrium*. Ice at $T = 0$ is not in true equilibrium — it is kinetically trapped. A hypothetical proton-ordered ice phase (ice XI) would have $S(0) = 0$.

</details>

---

## 📘 9. Appendix: Extended Derivations & Special Cases

### Appendix 9.1 — Zeroth Law Transitivity: A Rigorous Proof

The Zeroth Law states: *If system A is in thermal equilibrium with system C, and system B is in thermal equilibrium with system C, then A is in thermal equilibrium with B.*

This establishes thermal equilibrium as an **equivalence relation** on the set of thermodynamic systems. We prove this formally.

**Setup.** Let the state of each system be described by its independent variables. For system $i$, let the state be $(P_i, V_i)$ (or any pair of independent variables). When two systems are in thermal equilibrium, their states are constrained:

$$
F_{AC}(P_A, V_A, P_C, V_C) = 0 \quad \text{(A in equilibrium with C)}
$$

$$
F_{BC}(P_B, V_B, P_C, V_C) = 0 \quad \text{(B in equilibrium with C)}
$$

**The key step.** From the first equation, solve for $P_C$:

$$
P_C = f_{AC}(P_A, V_A, V_C)
$$

From the second equation, solve for $P_C$:

$$
P_C = f_{BC}(P_B, V_B, V_C)
$$

Since both expressions equal $P_C$:

$$
f_{AC}(P_A, V_A, V_C) = f_{BC}(P_B, V_B, V_C)
$$

**The Zeroth Law asserts** that this equation, which ostensibly involves $V_C$, must actually be independent of $V_C$. That is, the dependence on $V_C$ must cancel on both sides. This means we can write:

$$
\theta_A(P_A, V_A) = \theta_B(P_B, V_B)
$$

where $\theta$ is a function of the state variables of each system alone — this is the **empirical temperature**. The Zeroth Law guarantees the existence of a state function (temperature) that is the same for all systems in mutual thermal equilibrium.

**Equivalence relation properties:**
- **Reflexive:** Every system is in thermal equilibrium with itself. ✓
- **Symmetric:** If A is in equilibrium with B, then B is in equilibrium with A. ✓ (equilibrium is mutual)
- **Transitive:** This is precisely the Zeroth Law statement. ✓

Therefore thermal equilibrium partitions all thermodynamic systems into equivalence classes. Each class is labeled by a single number: the temperature $\theta$. $\blacksquare$

**Reference:** Callen, *Thermodynamics*, §1.3; Kittel & Kroemer, *Thermal Physics*, Ch. 1.

---

### Appendix 9.2 — Absolute Temperature Scale via Carnot's Theorem

We derive the thermodynamic (absolute) temperature scale using only the properties of reversible heat engines, independent of any working substance.

**Carnot's Theorem.** All reversible engines operating between the same two reservoirs have the same efficiency, regardless of working substance.

**Proof sketch (by contradiction).** Suppose engine $A$ (reversible) has efficiency $\eta_A > \eta_B$ of engine $B$ (also reversible). Run $B$ in reverse as a heat pump, driven by $A$. The composite device would transfer heat from cold to hot with no net work input — violating the Clausius statement of the Second Law. Therefore $\eta_A = \eta_B$ for all reversible engines. $\blacksquare$

**Constructing the absolute scale.** Since the efficiency of a reversible engine depends only on the reservoir temperatures (not the working substance), we can write:

$$
\eta_{\text{rev}} = 1 - \frac{|Q_C|}{|Q_H|} = f(\theta_H, \theta_C)
$$

where $\theta_H, \theta_C$ are the empirical temperatures of the reservoirs. Equivalently:

$$
\frac{|Q_C|}{|Q_H|} = g(\theta_H, \theta_C)
$$

**Kelvin's insight.** Consider three reservoirs at temperatures $\theta_1 > \theta_2 > \theta_3$. A reversible engine between $\theta_1$ and $\theta_3$ can be decomposed into two engines: one between $\theta_1$ and $\theta_2$, and another between $\theta_2$ and $\theta_3$:

$$
\frac{|Q_3|}{|Q_1|} = \frac{|Q_2|}{|Q_1|} \cdot \frac{|Q_3|}{|Q_2|}
$$

$$
g(\theta_1, \theta_3) = g(\theta_1, \theta_2) \cdot g(\theta_2, \theta_3)
$$

This functional equation has the unique solution (up to a monotonic rescaling):

$$
g(\theta_H, \theta_C) = \frac{\phi(\theta_C)}{\phi(\theta_H)}
$$

for some function $\phi$. We DEFINE the absolute temperature $T$ by:

$$
T \equiv \phi(\theta) \quad \text{(up to a multiplicative constant)}
$$

Then:

$$
\frac{|Q_C|}{|Q_H|} = \frac{T_C}{T_H}
$$

The multiplicative constant is fixed by assigning $T_{\text{tp}} = 273.16\,\text{K}$ to the triple point of water.

**Key consequences:**
1. The Carnot efficiency $\eta = 1 - T_C/T_H$ follows immediately.
2. $T = 0$ (absolute zero) would require $|Q_C| = 0$ — a perfect engine — which the Second Law forbids. Hence absolute zero is unattainable (Third Law).
3. The scale is independent of any material property — it is truly universal.

**Reference:** Fermi, *Thermodynamics*, Ch. 4; Susskind, *Statistical Mechanics* Lecture 2; MIT OCW 8.333 Lecture Notes.

---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

*Previous: [5.0 - Subject Overview](5.0---Subject-Overview) | Next: [5.2 - Entropy & Heat Engines](5.2---Entropy-&-Heat-Engines)*
