---
title: "Electrodynamics Induction Maxwells Equations"
subject: "Electrodynamics & Classical Field Theory"
catalog: advanced
audience_tier: higher-education
chapter: "7.4"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 7.4 — Electrodynamics: Induction & Maxwell's Equations

> *"A change in the magnetic field produces an electric field — this is the key to the whole of electrodynamics."* — Richard P. Feynman
>
> *"We can scarcely avoid the inference that light consists in the transverse undulations of the same medium which is the cause of electric and magnetic phenomena."* — James Clerk Maxwell, 1862

This chapter marks the transition from statics to dynamics. When fields change in time, electric and magnetic phenomena become inseparably coupled: a changing $\mathbf{B}$ induces $\mathbf{E}$ (Faraday's Law), and a changing $\mathbf{E}$ induces $\mathbf{B}$ (Maxwell's displacement current). The four Maxwell equations — the complete classical theory of electromagnetism — emerge as the synthesis of everything in Chapters 7.1–7.3, corrected for time dependence.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. State Faraday's Law in both integral and differential form and apply it to compute induced EMFs.
2. Explain Lenz's Law as a consequence of energy conservation.
3. Derive Maxwell's displacement current correction to Ampère's Law.
4. State all four Maxwell's equations in both integral and differential form.
5. Derive the continuity equation from Maxwell's equations.
6. Prove that Maxwell's equations are self-consistent (divergence of curl = 0 checks).
7. Identify the physical content of each Maxwell equation.

---

## 🖼️ Visual Anchor — Maxwell's Equations: The Complete Set

![math-07__7.4-fig1](math-07__7.4-fig1.svg)




---

## 📚 1. Definitions

### Definition 7.4.1 — Electromotive Force (EMF)

The **EMF** around a closed loop $\mathcal{C}$ is defined as the work done per unit charge by the electromagnetic force around the loop:

$$
\mathcal{E} = \oint_{\mathcal{C}} \mathbf{f}\cdot d\mathbf{l}
$$

where $\mathbf{f}$ is the force per unit charge. For a stationary loop in a time-varying magnetic field:

$$
\mathcal{E} = \oint_{\mathcal{C}} \mathbf{E}\cdot d\mathbf{l}
$$

### Definition 7.4.2 — Magnetic Flux Through a Loop

$$
\Phi_B = \int_S \mathbf{B}\cdot d\mathbf{a}
$$

where $S$ is any surface bounded by the loop $\mathcal{C}$, with orientation given by the right-hand rule.

### Definition 7.4.3 — Displacement Current Density

Maxwell's correction to Ampère's Law introduces the **displacement current density**:

$$
\mathbf{J}_d = \varepsilon_0\frac{\partial\mathbf{E}}{\partial t}
$$

This is not a real current (no charges flow), but it produces magnetic effects identical to a real current. The total "effective current" in the Ampère-Maxwell Law is $\mathbf{J} + \mathbf{J}_d$.

### Definition 7.4.4 — Maxwell's Equations (Differential Form)

The complete set of classical electromagnetic field equations in vacuum:

| # | Equation | Name | Source |
|:---|:---|:---|:---|
| I | $\nabla\cdot\mathbf{E} = \rho/\varepsilon_0$ | Gauss's Law | Electric charge |
| II | $\nabla\cdot\mathbf{B} = 0$ | Gauss's Law (magnetism) | No monopoles |
| III | $\nabla\times\mathbf{E} = -\partial\mathbf{B}/\partial t$ | Faraday's Law | Time-varying $\mathbf{B}$ |
| IV | $\nabla\times\mathbf{B} = \mu_0\mathbf{J} + \mu_0\varepsilon_0\partial\mathbf{E}/\partial t$ | Ampère-Maxwell | Current + time-varying $\mathbf{E}$ |

### Definition 7.4.5 — Maxwell's Equations (Integral Form)

| # | Equation | Theorem Used |
|:---|:---|:---|
| I | $\oint_S\mathbf{E}\cdot d\mathbf{a} = Q_{\text{enc}}/\varepsilon_0$ | Divergence Theorem |
| II | $\oint_S\mathbf{B}\cdot d\mathbf{a} = 0$ | Divergence Theorem |
| III | $\oint_{\mathcal{C}}\mathbf{E}\cdot d\mathbf{l} = -\frac{d\Phi_B}{dt}$ | Stokes' Theorem |
| IV | $\oint_{\mathcal{C}}\mathbf{B}\cdot d\mathbf{l} = \mu_0 I_{\text{enc}} + \mu_0\varepsilon_0\frac{d\Phi_E}{dt}$ | Stokes' Theorem |

### Definition 7.4.6 — Lenz's Law

The induced EMF always opposes the change in flux that produces it. Mathematically, this is encoded in the **negative sign** in Faraday's Law. If $\Phi_B$ is increasing, the induced current creates a field opposing the increase; if decreasing, the induced current supports the field.

---

## 📐 2. Axioms / Postulates

### Axiom 7.4.1 — Faraday's Law of Induction (Empirical)

A changing magnetic flux through a circuit induces an EMF:

$$
\mathcal{E} = -\frac{d\Phi_B}{dt}
$$

This was discovered experimentally by Faraday (1831) and independently by Henry. It is not derivable from electrostatics or magnetostatics — it is a new physical law.

### Axiom 7.4.2 — Maxwell's Displacement Current Hypothesis

The term $\mu_0\varepsilon_0\partial\mathbf{E}/\partial t$ must be added to Ampère's Law to ensure consistency with charge conservation. Maxwell postulated this in 1861 — it was confirmed experimentally by Hertz in 1887 through the detection of electromagnetic waves.

### Axiom 7.4.3 — Universality of Maxwell's Equations

Maxwell's equations (with the Lorentz force law) constitute the **complete** classical theory of electromagnetism. All classical electromagnetic phenomena — from static fields to radiation to optics — are consequences of these four equations plus boundary conditions.




---

## 🛡️ 3. Lemmas

### Lemma 7.4.1 — Inconsistency of Ampère's Law Without Displacement Current

**Statement:** The original Ampère's Law $\nabla\times\mathbf{B} = \mu_0\mathbf{J}$ is inconsistent with charge conservation for time-varying fields.

<details>
<summary>🔍 Proof</summary>

**Step 1:** Take the divergence of both sides of $\nabla\times\mathbf{B} = \mu_0\mathbf{J}$:

$$
\nabla\cdot(\nabla\times\mathbf{B}) = \mu_0\nabla\cdot\mathbf{J}
$$

**Step 2:** The left side is identically zero (divergence of any curl vanishes — a vector identity):

$$
0 = \mu_0\nabla\cdot\mathbf{J}
$$

**Step 3:** This requires $\nabla\cdot\mathbf{J} = 0$ always. But the continuity equation (charge conservation) states:

$$
\nabla\cdot\mathbf{J} = -\frac{\partial\rho}{\partial t}
$$

**Step 4:** For time-varying charge distributions ($\partial\rho/\partial t \neq 0$), we have $\nabla\cdot\mathbf{J} \neq 0$. This contradicts Step 2.

**Conclusion:** Ampère's Law in its original form is valid only for magnetostatics. A correction term is needed for time-dependent fields. $\blacksquare$

</details>

### Lemma 7.4.2 — The Displacement Current Restores Consistency

**Statement:** Adding $\mu_0\varepsilon_0\partial\mathbf{E}/\partial t$ to Ampère's Law makes it consistent with charge conservation.

<details>
<summary>🔍 Proof</summary>

**Step 1:** The corrected law is $\nabla\times\mathbf{B} = \mu_0\mathbf{J} + \mu_0\varepsilon_0\frac{\partial\mathbf{E}}{\partial t}$.

**Step 2:** Take the divergence:

$$
0 = \mu_0\nabla\cdot\mathbf{J} + \mu_0\varepsilon_0\frac{\partial}{\partial t}(\nabla\cdot\mathbf{E})
$$

**Step 3:** Substitute Gauss's Law $\nabla\cdot\mathbf{E} = \rho/\varepsilon_0$:

$$
0 = \mu_0\nabla\cdot\mathbf{J} + \mu_0\varepsilon_0\frac{\partial}{\partial t}\left(\frac{\rho}{\varepsilon_0}\right) = \mu_0\left(\nabla\cdot\mathbf{J} + \frac{\partial\rho}{\partial t}\right)
$$

**Step 4:** This gives exactly the continuity equation:

$$
\nabla\cdot\mathbf{J} + \frac{\partial\rho}{\partial t} = 0
$$

Consistency is restored. $\blacksquare$

</details>

---

## 👑 4. Theorems

### Theorem 7.4.1 — Faraday's Law (Differential Form)

$$
\nabla\times\mathbf{E} = -\frac{\partial\mathbf{B}}{\partial t}
$$

A time-varying magnetic field produces a curling electric field. In electrostatics, $\nabla\times\mathbf{E} = 0$; this is the generalization.

### Theorem 7.4.2 — The Ampère-Maxwell Law

$$
\nabla\times\mathbf{B} = \mu_0\mathbf{J} + \mu_0\varepsilon_0\frac{\partial\mathbf{E}}{\partial t}
$$

Both real currents and time-varying electric fields produce curling magnetic fields.

### Theorem 7.4.3 — The Continuity Equation (from Maxwell)

Maxwell's equations imply charge conservation:

$$
\frac{\partial\rho}{\partial t} + \nabla\cdot\mathbf{J} = 0
$$

This is not an independent equation — it is a consequence of the self-consistency of Maxwell's equations (proven in Lemma 7.4.2).

### Theorem 7.4.4 — Maxwell's Equations Predict Electromagnetic Waves

In vacuum ($\rho = 0$, $\mathbf{J} = 0$), Maxwell's equations combine to give wave equations for both $\mathbf{E}$ and $\mathbf{B}$:

$$
\nabla^2\mathbf{E} = \mu_0\varepsilon_0\frac{\partial^2\mathbf{E}}{\partial t^2}, \quad \nabla^2\mathbf{B} = \mu_0\varepsilon_0\frac{\partial^2\mathbf{B}}{\partial t^2}
$$

The wave speed is $c = 1/\sqrt{\mu_0\varepsilon_0} = 3\times 10^8$ m/s — the speed of light.

### Theorem 7.4.5 — Poynting's Theorem (Energy Conservation)

The rate of electromagnetic energy flow is governed by:

$$
\frac{\partial u}{\partial t} + \nabla\cdot\mathbf{S} = -\mathbf{J}\cdot\mathbf{E}
$$

where $u = \frac{1}{2}(\varepsilon_0 E^2 + B^2/\mu_0)$ is the energy density and $\mathbf{S} = \frac{1}{\mu_0}\mathbf{E}\times\mathbf{B}$ is the **Poynting vector** (energy flux, W/m²).




---

## ✍️ 5. Proofs / Derivations

### Derivation 7.4.1 — Faraday's Law (Differential from Integral)

<details>
<summary>🔍 Complete Derivation</summary>

**Step 1:** Start with Faraday's Law in integral form for a stationary loop:

$$
\oint_{\mathcal{C}}\mathbf{E}\cdot d\mathbf{l} = -\frac{d}{dt}\int_S\mathbf{B}\cdot d\mathbf{a}
$$

**Step 2:** Since the loop is stationary, bring the time derivative inside:

$$
\oint_{\mathcal{C}}\mathbf{E}\cdot d\mathbf{l} = -\int_S\frac{\partial\mathbf{B}}{\partial t}\cdot d\mathbf{a}
$$

**Step 3:** Apply Stokes' Theorem (from [1.7 - Green's Stokes' and Divergence Theorems](1.7---Green's-Stokes'-and-Divergence-Theorems)) to the left side:

$$
\int_S(\nabla\times\mathbf{E})\cdot d\mathbf{a} = -\int_S\frac{\partial\mathbf{B}}{\partial t}\cdot d\mathbf{a}
$$

**Step 4:** Since this holds for any surface $S$, the integrands must be equal:

$$
\nabla\times\mathbf{E} = -\frac{\partial\mathbf{B}}{\partial t}
$$

$\blacksquare$

</details>

### Derivation 7.4.2 — Maxwell's Displacement Current

<details>
<summary>🔍 Complete Derivation</summary>

**Goal:** Derive the displacement current term by requiring consistency with charge conservation.

**Step 1:** We need $\nabla\times\mathbf{B} = \mu_0\mathbf{J} + \mu_0\mathbf{J}_d$ where $\mathbf{J}_d$ is to be determined.

**Step 2:** Requirement: $\nabla\cdot(\nabla\times\mathbf{B}) = 0$ must hold identically. Therefore:

$$
\mu_0\nabla\cdot\mathbf{J} + \mu_0\nabla\cdot\mathbf{J}_d = 0
$$

$$
\nabla\cdot\mathbf{J}_d = -\nabla\cdot\mathbf{J} = \frac{\partial\rho}{\partial t}
$$

(using the continuity equation).

**Step 3:** From Gauss's Law: $\rho = \varepsilon_0\nabla\cdot\mathbf{E}$. Therefore:

$$
\nabla\cdot\mathbf{J}_d = \frac{\partial}{\partial t}(\varepsilon_0\nabla\cdot\mathbf{E}) = \nabla\cdot\left(\varepsilon_0\frac{\partial\mathbf{E}}{\partial t}\right)
$$

**Step 4:** The simplest choice satisfying this divergence condition:

$$
\mathbf{J}_d = \varepsilon_0\frac{\partial\mathbf{E}}{\partial t}
$$

**Step 5:** The corrected Ampère-Maxwell Law:

$$
\nabla\times\mathbf{B} = \mu_0\mathbf{J} + \mu_0\varepsilon_0\frac{\partial\mathbf{E}}{\partial t}
$$

$\blacksquare$

**Physical example:** Consider a charging capacitor. Between the plates, $\mathbf{J} = 0$ (no charges flow through the gap), but $\partial\mathbf{E}/\partial t \neq 0$ (the field is building up). The displacement current $\varepsilon_0\partial\mathbf{E}/\partial t$ in the gap equals the conduction current $I$ in the wires, ensuring that $\oint\mathbf{B}\cdot d\mathbf{l}$ gives the same answer regardless of which surface bounded by the Amperian loop we choose.

</details>

### Derivation 7.4.3 — The Electromagnetic Wave Equation

<details>
<summary>🔍 Complete Derivation</summary>

**Step 1:** Start with Maxwell's equations in vacuum ($\rho = 0$, $\mathbf{J} = 0$):

$$
\nabla\cdot\mathbf{E} = 0, \quad \nabla\cdot\mathbf{B} = 0
$$

$$
\nabla\times\mathbf{E} = -\frac{\partial\mathbf{B}}{\partial t}, \quad \nabla\times\mathbf{B} = \mu_0\varepsilon_0\frac{\partial\mathbf{E}}{\partial t}
$$

**Step 2:** Take the curl of Faraday's Law:

$$
\nabla\times(\nabla\times\mathbf{E}) = -\frac{\partial}{\partial t}(\nabla\times\mathbf{B})
$$

**Step 3:** Apply the vector identity $\nabla\times(\nabla\times\mathbf{V}) = \nabla(\nabla\cdot\mathbf{V}) - \nabla^2\mathbf{V}$:

$$
\nabla(\nabla\cdot\mathbf{E}) - \nabla^2\mathbf{E} = -\frac{\partial}{\partial t}(\nabla\times\mathbf{B})
$$

**Step 4:** Use $\nabla\cdot\mathbf{E} = 0$ (vacuum) and $\nabla\times\mathbf{B} = \mu_0\varepsilon_0\partial\mathbf{E}/\partial t$:

$$
-\nabla^2\mathbf{E} = -\mu_0\varepsilon_0\frac{\partial^2\mathbf{E}}{\partial t^2}
$$

**Step 5:** Rearranging:

$$
\nabla^2\mathbf{E} = \mu_0\varepsilon_0\frac{\partial^2\mathbf{E}}{\partial t^2}
$$

**Step 6:** This is the **wave equation** with speed $v = 1/\sqrt{\mu_0\varepsilon_0}$. Numerically:

$$
v = \frac{1}{\sqrt{(4\pi\times10^{-7})(8.854\times10^{-12})}} = 2.998\times10^8\text{ m/s} = c
$$

**Step 7:** An identical derivation starting from the curl of the Ampère-Maxwell Law gives:

$$
\nabla^2\mathbf{B} = \mu_0\varepsilon_0\frac{\partial^2\mathbf{B}}{\partial t^2}
$$

**Conclusion:** Maxwell's equations predict electromagnetic waves traveling at the speed of light. Maxwell's identification: **light is an electromagnetic wave**. $\blacksquare$

</details>

### Derivation 7.4.4 — Poynting's Theorem

<details>
<summary>🔍 Complete Derivation</summary>

**Goal:** Derive the energy conservation law for electromagnetic fields.

**Step 1:** The energy density stored in the fields is:

$$
u = \frac{1}{2}\left(\varepsilon_0 E^2 + \frac{B^2}{\mu_0}\right)
$$

Take the time derivative:

$$
\frac{\partial u}{\partial t} = \varepsilon_0\mathbf{E}\cdot\frac{\partial\mathbf{E}}{\partial t} + \frac{1}{\mu_0}\mathbf{B}\cdot\frac{\partial\mathbf{B}}{\partial t}
$$

**Step 2:** From Faraday's Law: $\frac{\partial\mathbf{B}}{\partial t} = -\nabla\times\mathbf{E}$. Substitute:

$$
\frac{1}{\mu_0}\mathbf{B}\cdot\frac{\partial\mathbf{B}}{\partial t} = -\frac{1}{\mu_0}\mathbf{B}\cdot(\nabla\times\mathbf{E})
$$

**Step 3:** From the Ampère-Maxwell Law: $\frac{\partial\mathbf{E}}{\partial t} = \frac{1}{\mu_0\varepsilon_0}(\nabla\times\mathbf{B}) - \frac{\mathbf{J}}{\varepsilon_0}$. Substitute:

$$
\varepsilon_0\mathbf{E}\cdot\frac{\partial\mathbf{E}}{\partial t} = \frac{1}{\mu_0}\mathbf{E}\cdot(\nabla\times\mathbf{B}) - \mathbf{J}\cdot\mathbf{E}
$$

**Step 4:** Combine:

$$
\frac{\partial u}{\partial t} = \frac{1}{\mu_0}[\mathbf{E}\cdot(\nabla\times\mathbf{B}) - \mathbf{B}\cdot(\nabla\times\mathbf{E})] - \mathbf{J}\cdot\mathbf{E}
$$

**Step 5:** Use the vector identity $\nabla\cdot(\mathbf{E}\times\mathbf{B}) = \mathbf{B}\cdot(\nabla\times\mathbf{E}) - \mathbf{E}\cdot(\nabla\times\mathbf{B})$:

$$
\mathbf{E}\cdot(\nabla\times\mathbf{B}) - \mathbf{B}\cdot(\nabla\times\mathbf{E}) = -\nabla\cdot(\mathbf{E}\times\mathbf{B})
$$

**Step 6:** Therefore:

$$
\frac{\partial u}{\partial t} = -\frac{1}{\mu_0}\nabla\cdot(\mathbf{E}\times\mathbf{B}) - \mathbf{J}\cdot\mathbf{E}
$$

**Step 7:** Define the **Poynting vector** $\mathbf{S} = \frac{1}{\mu_0}\mathbf{E}\times\mathbf{B}$:

$$
\frac{\partial u}{\partial t} + \nabla\cdot\mathbf{S} = -\mathbf{J}\cdot\mathbf{E}
$$

**Interpretation:**
- $\partial u/\partial t$: rate of change of field energy density
- $\nabla\cdot\mathbf{S}$: energy flux leaving the region
- $-\mathbf{J}\cdot\mathbf{E}$: work done by the field on charges (power dissipated)

In integral form (integrating over volume $V$ bounded by surface $S$):

$$
\frac{d}{dt}\int_V u\,d\tau + \oint_S\mathbf{S}\cdot d\mathbf{a} = -\int_V\mathbf{J}\cdot\mathbf{E}\,d\tau
$$

$\blacksquare$

</details>




---

## 🧮 6. Worked Examples

### Example 7.4.1 — EMF in a Rotating Loop

**Problem:** A rectangular loop of area $A$ rotates with angular velocity $\omega$ in a uniform magnetic field $\mathbf{B} = B_0\hat{\mathbf{z}}$. The loop normal makes angle $\theta = \omega t$ with $\mathbf{B}$. Find the induced EMF.

<details>
<summary>🔍 Complete Solution</summary>

**Step 1:** The magnetic flux through the loop:

$$
\Phi_B = \mathbf{B}\cdot\hat{\mathbf{n}}\,A = B_0 A\cos(\omega t)
$$

**Step 2:** Apply Faraday's Law:

$$
\mathcal{E} = -\frac{d\Phi_B}{dt} = -B_0 A\frac{d}{dt}\cos(\omega t) = B_0 A\omega\sin(\omega t)
$$

**Step 3:** The peak EMF is $\mathcal{E}_0 = B_0 A\omega$, and the EMF oscillates sinusoidally. This is the operating principle of an AC generator.

**Step 4 (Lenz's Law check):** When $\theta$ increases from $0$ (flux decreasing), the induced current creates a field to maintain the flux — consistent with the positive EMF driving current in the direction that opposes the flux decrease.

</details>

---

### Example 7.4.2 — Displacement Current in a Charging Capacitor

**Problem:** A parallel-plate capacitor with circular plates of radius $R$ is being charged by current $I$. Find the magnetic field between the plates at radius $s < R$.

<details>
<summary>🔍 Complete Solution</summary>

**Step 1:** Between the plates, $\mathbf{J} = 0$ (no conduction current). The electric field between the plates (assuming uniform):

$$
E = \frac{\sigma}{\varepsilon_0} = \frac{Q}{\varepsilon_0\pi R^2}
$$

**Step 2:** The displacement current density:

$$
J_d = \varepsilon_0\frac{\partial E}{\partial t} = \varepsilon_0\cdot\frac{1}{\varepsilon_0\pi R^2}\frac{dQ}{dt} = \frac{I}{\pi R^2}
$$

This is uniform between the plates — the displacement current density equals the conduction current density in the wires.

**Step 3:** Apply the Ampère-Maxwell Law with a circular Amperian loop of radius $s$ between the plates:

$$
\oint\mathbf{B}\cdot d\mathbf{l} = B(s)\cdot 2\pi s = \mu_0\varepsilon_0\frac{d\Phi_E}{dt}
$$

where $\Phi_E = E\cdot\pi s^2 = \frac{Q}{\varepsilon_0\pi R^2}\cdot\pi s^2 = \frac{Qs^2}{\varepsilon_0 R^2}$.

**Step 4:**

$$
\mu_0\varepsilon_0\frac{d\Phi_E}{dt} = \mu_0\varepsilon_0\cdot\frac{s^2}{\varepsilon_0 R^2}\frac{dQ}{dt} = \frac{\mu_0 Is^2}{R^2}
$$

**Step 5:** Solving:

$$
B(s) = \frac{\mu_0 Is}{2\pi R^2} \quad (s \lt  R)
$$

**Step 6 (Verification):** At $s = R$: $B = \mu_0 I/(2\pi R)$, which matches the field just outside the wire. The magnetic field is continuous across the edge of the capacitor — the displacement current seamlessly continues the magnetic effect of the conduction current.

</details>

---

### Example 7.4.3 — Self-Consistency Check: Divergence of Faraday's Law

**Problem:** Verify that Faraday's Law $\nabla\times\mathbf{E} = -\partial\mathbf{B}/\partial t$ is consistent with $\nabla\cdot\mathbf{B} = 0$.

<details>
<summary>🔍 Complete Solution</summary>

**Step 1:** Take the divergence of both sides of Faraday's Law:

$$
\nabla\cdot(\nabla\times\mathbf{E}) = -\nabla\cdot\frac{\partial\mathbf{B}}{\partial t}
$$

**Step 2:** The left side is identically zero (divergence of any curl vanishes):

$$
0 = -\frac{\partial}{\partial t}(\nabla\cdot\mathbf{B})
$$

**Step 3:** This gives $\frac{\partial}{\partial t}(\nabla\cdot\mathbf{B}) = 0$, meaning that if $\nabla\cdot\mathbf{B} = 0$ at any one time, it remains zero for all time.

**Step 4:** Since $\nabla\cdot\mathbf{B} = 0$ is imposed as an initial condition (no monopoles exist), Faraday's Law preserves this condition automatically. The equations are self-consistent. $\blacksquare$

</details>

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links

| Topic | Link | Relevance |
|:---|:---|:---|
| Electrostatics | [7.1 - Electrostatics - Gauss's Law & Potential](7.1---Electrostatics---Gauss's-Law-&-Potential) | Static limit: $\partial\mathbf{B}/\partial t = 0$ gives $\nabla\times\mathbf{E} = 0$ |
| Magnetostatics | [7.3 - Magnetostatics - Biot-Savart & Ampere's Law](7.3---Magnetostatics---Biot-Savart-&-Ampere's-Law) | Static limit: $\partial\mathbf{E}/\partial t = 0$ gives original Ampère |
| Wave propagation | [7.5 - Electromagnetic Wave Propagation & Poynting Vector](7.5---Electromagnetic-Wave-Propagation-&-Poynting-Vector) | Solutions to the wave equation |
| Potentials | [7.6 - Potential Formulations & Gauge Transformations](7.6---Potential-Formulations-&-Gauge-Transformations) | $\phi$ and $\mathbf{A}$ formulation of Maxwell |
| Integral theorems | [1.7 - Green's Stokes' and Divergence Theorems](1.7---Green's-Stokes'-and-Divergence-Theorems) | Converting between integral and differential forms |
| Relativistic form | [7.8 - The Electromagnetic Field Tensor & Gauge Fields](7.8---The-Electromagnetic-Field-Tensor-&-Gauge-Fields) | Maxwell's equations as $\partial_\mu F^{\mu\nu} = \mu_0 J^\nu$ |

### Authoritative External Resources

1. **Griffiths, D.J.** — *Introduction to Electrodynamics*, 4th ed., Chapters 7–8.
2. **Feynman, Leighton & Sands** — *The Feynman Lectures on Physics*, Vol. II, Chapters 18–22.
3. **Jackson, J.D.** — *Classical Electrodynamics*, 3rd ed., Chapter 6.
4. **MIT OCW 8.02** — Faraday's Law demonstrations and Maxwell's equations lectures.

### Key Equations Summary

| Name | Equation | Number |
|:---|:---|:---|
| Faraday's Law | $\nabla\times\mathbf{E} = -\partial\mathbf{B}/\partial t$ | (7.4.1) |
| Ampère-Maxwell | $\nabla\times\mathbf{B} = \mu_0\mathbf{J} + \mu_0\varepsilon_0\partial\mathbf{E}/\partial t$ | (7.4.2) |
| Displacement current | $\mathbf{J}_d = \varepsilon_0\partial\mathbf{E}/\partial t$ | (7.4.3) |
| Wave equation | $\nabla^2\mathbf{E} = \mu_0\varepsilon_0\partial^2\mathbf{E}/\partial t^2$ | (7.4.4) |
| Speed of light | $c = 1/\sqrt{\mu_0\varepsilon_0}$ | (7.4.5) |
| Poynting vector | $\mathbf{S} = \frac{1}{\mu_0}\mathbf{E}\times\mathbf{B}$ | (7.4.6) |
| Energy density | $u = \frac{1}{2}(\varepsilon_0 E^2 + B^2/\mu_0)$ | (7.4.7) |




---

### Derivation 7.4.5 — Mutual Inductance and Neumann Formula

<details>
<summary>🔍 Complete Derivation</summary>

**Setup:** Two loops $\mathcal{C}_1$ and $\mathcal{C}_2$ carry currents $I_1$ and $I_2$. The mutual inductance $M_{12}$ relates the flux through loop 2 due to current in loop 1.

**Step 1:** The vector potential at a point $\mathbf{r}$ due to current $I_1$ in loop 1:

$$
\mathbf{A}_1(\mathbf{r}) = \frac{\mu_0 I_1}{4\pi}\oint_{\mathcal{C}_1}\frac{d\mathbf{l}_1'}{|\mathbf{r}-\mathbf{r}_1'|}
$$

**Step 2:** The flux through loop 2:

$$
\Phi_{12} = \oint_{\mathcal{C}_2}\mathbf{A}_1\cdot d\mathbf{l}_2 = \frac{\mu_0 I_1}{4\pi}\oint_{\mathcal{C}_2}\oint_{\mathcal{C}_1}\frac{d\mathbf{l}_1'\cdot d\mathbf{l}_2}{|\mathbf{r}_2-\mathbf{r}_1'|}
$$

**Step 3:** Define $M_{12} = \Phi_{12}/I_1$:

$$
M_{12} = \frac{\mu_0}{4\pi}\oint_{\mathcal{C}_1}\oint_{\mathcal{C}_2}\frac{d\mathbf{l}_1\cdot d\mathbf{l}_2}{|\mathbf{r}_1-\mathbf{r}_2|}
$$

This is the **Neumann formula**. It is symmetric: $M_{12} = M_{21} = M$.

**Step 4:** The induced EMF in loop 2 due to changing current in loop 1:

$$
\mathcal{E}_2 = -\frac{d\Phi_{12}}{dt} = -M\frac{dI_1}{dt}
$$

$\blacksquare$

</details>

### Derivation 7.4.6 — Self-Inductance of a Solenoid

<details>
<summary>🔍 Complete Derivation</summary>

**Setup:** A solenoid of length $l$, cross-sectional area $A$, with $N$ total turns carrying current $I$.

**Step 1:** The magnetic field inside: $B = \mu_0 nI = \mu_0(N/l)I$.

**Step 2:** The flux through one turn: $\Phi_1 = BA = \mu_0(N/l)IA$.

**Step 3:** The total flux linkage (flux through all $N$ turns):

$$
\Lambda = N\Phi_1 = \frac{\mu_0 N^2 A}{l}\,I
$$

**Step 4:** The self-inductance $L = \Lambda/I$:

$$
L = \frac{\mu_0 N^2 A}{l}
$$

**Step 5:** The energy stored in the inductor:

$$
W = \frac{1}{2}LI^2 = \frac{\mu_0 N^2 A I^2}{2l}
$$

**Step 6 (Verification via field energy):**

$$
W = \frac{1}{2\mu_0}\int B^2\,d\tau = \frac{1}{2\mu_0}(\mu_0 nI)^2\cdot Al = \frac{\mu_0 n^2 I^2 Al}{2} = \frac{\mu_0 N^2 I^2 A}{2l}
$$

Both methods agree. $\blacksquare$

</details>

---

### Example 7.4.4 — Electromagnetic Momentum

**Problem:** A long solenoid (radius $R$, $n$ turns/m, current $I$) is coaxial with a cylindrical shell of radius $b > R$ carrying surface charge $\sigma$. Find the electromagnetic momentum per unit length.

<details>
<summary>🔍 Complete Solution</summary>

**Step 1:** Inside the solenoid: $\mathbf{B} = \mu_0 nI\,\hat{\mathbf{z}}$. Outside: $\mathbf{B} = 0$.

**Step 2:** The charged cylinder creates a radial electric field. By Gauss's Law, for $s \gt  b$:

$$
E_s = \frac{\sigma b}{\varepsilon_0 s} \quad (s \gt  b)
$$

For $R \lt  s \lt  b$: $E_s = 0$ (no enclosed charge in this region if the charge is only on the outer cylinder).

Wait — the charge is on the cylinder at $s = b$. For $s \lt  b$: $E = 0$ (no enclosed charge). For $s \gt  b$: $E_s = \sigma b/(\varepsilon_0 s)$.

**Step 3:** The Poynting vector $\mathbf{S} = \frac{1}{\mu_0}\mathbf{E}\times\mathbf{B}$. Since $\mathbf{B}$ is only non-zero for $s \lt  R$ and $\mathbf{E}$ is only non-zero for $s \gt  b \gt  R$, there is **no overlap** between the regions where $\mathbf{E} \neq 0$ and $\mathbf{B} \neq 0$.

**Step 4:** Therefore $\mathbf{S} = 0$ everywhere, and the electromagnetic momentum is zero.

**Step 5:** However, if the charge is on an inner cylinder at radius $a \lt  R$, then $\mathbf{E}$ exists for $s \gt  a$ and $\mathbf{B}$ exists for $s \lt  R$. In the overlap region $a \lt  s \lt  R$:

$$
\mathbf{S} = \frac{1}{\mu_0}\left(\frac{\sigma a}{\varepsilon_0 s}\hat{\mathbf{s}}\right)\times(\mu_0 nI\hat{\mathbf{z}}) = \frac{\sigma a nI}{s\varepsilon_0}(-\hat{\boldsymbol{\varphi}})
$$

Wait — $\hat{\mathbf{s}}\times\hat{\mathbf{z}} = -\hat{\boldsymbol{\varphi}}$. The momentum density $\mathbf{g} = \mathbf{S}/c^2$ circulates azimuthally. This is the "hidden momentum" problem — a beautiful subtlety of electromagnetic momentum.

</details>

---

### Example 7.4.5 — Maxwell's Equations in Matter

**Problem:** Write Maxwell's equations in linear, isotropic media with permittivity $\varepsilon$ and permeability $\mu$.

<details>
<summary>🔍 Complete Solution</summary>

**Step 1:** Define the auxiliary fields:

$$
\mathbf{D} = \varepsilon\mathbf{E}, \quad \mathbf{H} = \frac{\mathbf{B}}{\mu}
$$

**Step 2:** Maxwell's equations in matter (with free charges $\rho_f$ and free currents $\mathbf{J}_f$):

$$
\nabla\cdot\mathbf{D} = \rho_f
$$

$$
\nabla\cdot\mathbf{B} = 0
$$

$$
\nabla\times\mathbf{E} = -\frac{\partial\mathbf{B}}{\partial t}
$$

$$
\nabla\times\mathbf{H} = \mathbf{J}_f + \frac{\partial\mathbf{D}}{\partial t}
$$

**Step 3:** The wave speed in the medium:

$$
v = \frac{1}{\sqrt{\mu\varepsilon}} = \frac{c}{n}
$$

where $n = c\sqrt{\mu\varepsilon} = \sqrt{\mu_r\varepsilon_r}$ is the index of refraction.

**Step 4:** The boundary conditions at an interface (no free surface charges or currents):
- $D_\perp$ continuous → $\varepsilon_1 E_{1\perp} = \varepsilon_2 E_{2\perp}$
- $B_\perp$ continuous
- $E_\parallel$ continuous
- $H_\parallel$ continuous → $B_{1\parallel}/\mu_1 = B_{2\parallel}/\mu_2$

</details>

