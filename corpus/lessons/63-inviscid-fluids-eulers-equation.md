---
title: "Inviscid Fluids Eulers Equation"
subject: "Fluid Dynamics & Continuum Mechanics"
catalog: advanced
audience_tier: higher-education
chapter: "6.3"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 6.3 — Inviscid Fluids: Euler's Equation

> *"The equations which I am going to establish contain not only the laws of equilibrium of fluids, but also those of their motion. They embrace the whole theory of the motion of fluids."* — Leonhard Euler, *Mémoires de l'Académie des Sciences de Berlin* (1757).

When viscous effects are negligible — far from solid boundaries, at high Reynolds numbers, or in idealized theoretical analysis — the stress tensor reduces to pure pressure: $\sigma_{ij} = -p\,\delta_{ij}$. Substituting this into Cauchy's equation of motion yields **Euler's equation**, the fundamental momentum equation for inviscid flow. From it springs Bernoulli's theorem, the theory of sound waves, and the entire framework of potential flow. This chapter derives Euler's equation, proves Bernoulli's theorem in its various forms, and establishes Kelvin's circulation theorem showing that inviscid flow preserves vorticity.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Derive Euler's equation from Cauchy's equation by setting viscous stress to zero.
2. Write Euler's equation in both conservative and convective forms.
3. Derive and apply Bernoulli's equation along a streamline for steady flow.
4. Prove the strong form of Bernoulli's theorem for irrotational flow.
5. State and prove Kelvin's Circulation Theorem for inviscid barotropic flow.
6. Apply Euler's equation to compute pressure fields given velocity fields.
7. Derive the linearized acoustic wave equation from Euler + continuity.

---

## 🖼️ Visual Anchor — Streamlines and Pressure in a Converging Nozzle

Euler's equation in action: as streamlines converge (velocity increases), pressure decreases — the visual manifestation of Bernoulli's principle.

![math-06__6.3-fig1](math-06__6.3-fig1.svg)

---

## 📚 1. Definitions

### Definition 6.3.1 — Inviscid Fluid (Ideal Fluid)

An **inviscid fluid** (or ideal fluid, or perfect fluid) is one in which the stress tensor takes the purely hydrostatic form:

$$
\sigma_{ij} = -p\, \delta_{ij},
$$

where $p(\mathbf{x}, t)$ is the pressure field. There are no shear stresses — the deviatoric stress $\tau_{ij} = 0$.

### Definition 6.3.2 — Barotropic Fluid

A fluid is **barotropic** if the density is a function of pressure alone: $\rho = \rho(p)$. Equivalently, there exists a function $P(p)$ (the pressure function) such that:

$$
\frac{\nabla p}{\rho} = \nabla P, \qquad P(p) = \int \frac{dp'}{\rho(p')}.
$$

Special cases: incompressible fluid ($\rho = \text{const}$, $P = p/\rho$) and isentropic ideal gas ($p = K\rho^\gamma$).

### Definition 6.3.3 — Circulation

The **circulation** $\Gamma$ around a closed curve $C$ is the line integral of velocity:

$$
\Gamma = \oint_C \mathbf{v} \cdot d\mathbf{r}.
$$

By Stokes' theorem (see [1.7 - Green's Stokes' and Divergence Theorems](1.7---Green's-Stokes'-and-Divergence-Theorems)):

$$
\Gamma = \int_S (\nabla \times \mathbf{v}) \cdot \hat{n}\, dA = \int_S \boldsymbol{\omega} \cdot \hat{n}\, dA,
$$

where $S$ is any surface bounded by $C$ and $\boldsymbol{\omega} = \nabla \times \mathbf{v}$ is the vorticity.

### Definition 6.3.4 — Stagnation (Total) Pressure

The **stagnation pressure** $p_0$ is the pressure a fluid would reach if brought isentropically to rest:

$$
p_0 = p + \frac{1}{2}\rho v^2 \quad (\text{incompressible}).
$$

For compressible flow: $p_0 = p\left(1 + \frac{\gamma - 1}{2}M^2\right)^{\gamma/(\gamma-1)}$ (see [6.8 - Compressible Flow & Shock Waves](6.8---Compressible-Flow-&-Shock-Waves)).




---

## 📐 2. Axioms / Postulates

### Axiom 6.3.A — Inviscid Stress Hypothesis

For an inviscid fluid, the only surface force is pressure acting normal to every surface element. The constitutive assumption is:

$$
\mathbf{t}^{(\hat{n})} = -p\, \hat{n} \quad \Longleftrightarrow \quad \sigma_{ij} = -p\, \delta_{ij}.
$$

### Axiom 6.3.B — Conservation of Momentum (Newton's Second Law for Continua)

Inherited from [6.1 - Stress & Strain Tensors in Continua](6.1---Stress-&-Strain-Tensors-in-Continua), Axiom 6.1.B: the rate of change of momentum of any material volume equals the sum of body forces and surface forces.

### Axiom 6.3.C — Barotropic or Constant-Density Assumption

For Bernoulli's theorem and Kelvin's theorem, we assume either:
- Incompressible: $\rho = \text{const}$, or
- Barotropic: $\rho = \rho(p)$ (density depends only on pressure, not on temperature independently).

---

## 🛡️ 3. Lemmas

### Lemma 6.3.1 — Lamb's Vector Identity

For any differentiable velocity field $\mathbf{v}$:

$$
(\mathbf{v} \cdot \nabla)\mathbf{v} = \nabla\left(\frac{v^2}{2}\right) + \boldsymbol{\omega} \times \mathbf{v},
$$

where $v^2 = \mathbf{v} \cdot \mathbf{v}$ and $\boldsymbol{\omega} = \nabla \times \mathbf{v}$.

**Proof.** Work in index notation. The $i$-th component of the left side is $v_j \partial_j v_i$.

**Step 1:** Compute $[\nabla(v^2/2)]_i = \frac{1}{2}\partial_i(v_j v_j) = v_j \partial_i v_j$.

**Step 2:** Compute $[\boldsymbol{\omega} \times \mathbf{v}]_i = \epsilon_{ijk}\omega_j v_k = \epsilon_{ijk}(\epsilon_{jlm}\partial_l v_m) v_k$.

Using the identity $\epsilon_{ijk}\epsilon_{jlm} = \delta_{il}\delta_{km} - \delta_{im}\delta_{kl}$:

$$
[\boldsymbol{\omega} \times \mathbf{v}]_i = (\delta_{il}\delta_{km} - \delta_{im}\delta_{kl})\partial_l v_m\, v_k = v_k \partial_i v_k - v_k \partial_k v_i.
$$

**Step 3:** Therefore:

$$
[\nabla(v^2/2)]_i + [\boldsymbol{\omega} \times \mathbf{v}]_i = v_j \partial_i v_j + v_k \partial_i v_k - v_k \partial_k v_i.
$$

Wait — let us be more careful. We have:

$$
[\nabla(v^2/2)]_i + [\boldsymbol{\omega} \times \mathbf{v}]_i = v_j \partial_i v_j + v_k \partial_i v_k - v_k \partial_k v_i.
$$

That gives $2v_j \partial_i v_j - v_k \partial_k v_i$, which is not what we want. Let us redo this correctly.

**Step 2 (corrected):** $[\boldsymbol{\omega} \times \mathbf{v}]_i = \epsilon_{ijk}\omega_j v_k$.

With $\omega_j = \epsilon_{jlm}\partial_l v_m$:

$$
[\boldsymbol{\omega} \times \mathbf{v}]_i = \epsilon_{ijk}\epsilon_{jlm}\partial_l v_m\, v_k.
$$

Use $\epsilon_{ijk}\epsilon_{jlm} = \delta_{il}\delta_{km} - \delta_{im}\delta_{kl}$ (note: the contraction is on the first index of the second epsilon):

Actually, the correct identity for $\epsilon_{ijk}\epsilon_{jlm}$ requires care with index positions. We use:

$$
\epsilon_{ijk}\epsilon_{jlm} = \delta_{il}\delta_{km} - \delta_{im}\delta_{kl}.
$$

So:

$$
[\boldsymbol{\omega} \times \mathbf{v}]_i = (\delta_{il}\delta_{km} - \delta_{im}\delta_{kl})\,(\partial_l v_m)\, v_k = (\partial_i v_k)\, v_k - (\partial_k v_i)\, v_k.
$$

$$
= v_k\, \partial_i v_k - v_k\, \partial_k v_i.
$$

**Step 3:** Now add $\nabla(v^2/2)$:

$$
[\nabla(v^2/2) + \boldsymbol{\omega} \times \mathbf{v}]_i = v_j\, \partial_i v_j + v_k\, \partial_i v_k - v_k\, \partial_k v_i.
$$

But $v_j \partial_i v_j = v_k \partial_i v_k$ (just relabeling dummy index), so this equals $2v_k \partial_i v_k - v_k \partial_k v_i$. That is incorrect.

**Correct approach:** We want to show $v_j \partial_j v_i = v_j \partial_i v_j + \epsilon_{ijk}\omega_j v_k$... No. The identity states:

$$
(\mathbf{v} \cdot \nabla)\mathbf{v} = \nabla\left(\frac{v^2}{2}\right) + \boldsymbol{\omega} \times \mathbf{v}.
$$

Rearranging: $\nabla(v^2/2) = (\mathbf{v} \cdot \nabla)\mathbf{v} - \boldsymbol{\omega} \times \mathbf{v}$.

In components: $v_j \partial_i v_j = v_j \partial_j v_i + [(\nabla \times \mathbf{v}) \times \mathbf{v}]_i$... Let us use the standard vector identity directly.

**Standard proof:** Start from the identity $\nabla(\mathbf{a} \cdot \mathbf{b}) = (\mathbf{a} \cdot \nabla)\mathbf{b} + (\mathbf{b} \cdot \nabla)\mathbf{a} + \mathbf{a} \times (\nabla \times \mathbf{b}) + \mathbf{b} \times (\nabla \times \mathbf{a})$.

Set $\mathbf{a} = \mathbf{b} = \mathbf{v}$:

$$
\nabla(v^2) = 2(\mathbf{v} \cdot \nabla)\mathbf{v} + 2\mathbf{v} \times (\nabla \times \mathbf{v}).
$$

Therefore:

$$
(\mathbf{v} \cdot \nabla)\mathbf{v} = \frac{1}{2}\nabla(v^2) - \mathbf{v} \times \boldsymbol{\omega} = \nabla\left(\frac{v^2}{2}\right) + \boldsymbol{\omega} \times \mathbf{v}. \quad \blacksquare
$$

(Using $-\mathbf{v} \times \boldsymbol{\omega} = \boldsymbol{\omega} \times \mathbf{v}$.)

### Lemma 6.3.2 — Material Derivative of a Line Integral (Kelvin's Lemma)

For a material curve $C(t)$ moving with the fluid:

$$
\frac{d}{dt}\oint_{C(t)} \mathbf{v} \cdot d\mathbf{r} = \oint_{C(t)} \frac{D\mathbf{v}}{Dt} \cdot d\mathbf{r} + \oint_{C(t)} \mathbf{v} \cdot d\left(\frac{D\mathbf{r}}{Dt}\right).
$$

The second integral vanishes because $\frac{D\mathbf{r}}{Dt} = \mathbf{v}$, so $\mathbf{v} \cdot d\mathbf{v} = d(v^2/2)$, and the integral of an exact differential around a closed loop is zero:

$$
\oint_{C(t)} \mathbf{v} \cdot d\mathbf{v} = \oint_{C(t)} d\left(\frac{v^2}{2}\right) = 0.
$$

Therefore:

$$
\frac{d\Gamma}{dt} = \oint_{C(t)} \frac{D\mathbf{v}}{Dt} \cdot d\mathbf{r}. \quad \blacksquare
$$

---

## 👑 4. Theorems

### Theorem 6.3.1 — Euler's Equation of Motion

For an inviscid fluid with body force $\mathbf{b}$ per unit mass:

$$
\frac{D\mathbf{v}}{Dt} = -\frac{1}{\rho}\nabla p + \mathbf{b},
$$

or equivalently:

$$
\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v} = -\frac{1}{\rho}\nabla p + \mathbf{b}.
$$

In index notation:

$$
\frac{\partial v_i}{\partial t} + v_j \frac{\partial v_i}{\partial x_j} = -\frac{1}{\rho}\frac{\partial p}{\partial x_i} + b_i.
$$

### Theorem 6.3.2 — Bernoulli's Equation (Along a Streamline, Steady Incompressible)

For steady ($\partial/\partial t = 0$), incompressible ($\rho = \text{const}$), inviscid flow with gravity $\mathbf{b} = -g\hat{z}$:

$$
p + \frac{1}{2}\rho v^2 + \rho g z = \text{const along a streamline}.
$$

### Theorem 6.3.3 — Strong Bernoulli (Irrotational Flow)

If the flow is additionally irrotational ($\boldsymbol{\omega} = \nabla \times \mathbf{v} = 0$), then the Bernoulli constant is the same on *every* streamline:

$$
p + \frac{1}{2}\rho v^2 + \rho g z = C \quad \text{everywhere in the flow}.
$$

### Theorem 6.3.4 — Kelvin's Circulation Theorem

For an inviscid, barotropic fluid with only conservative body forces ($\mathbf{b} = -\nabla \Phi$), the circulation around any material loop is conserved:

$$
\frac{d\Gamma}{dt} = \frac{d}{dt}\oint_{C(t)} \mathbf{v} \cdot d\mathbf{r} = 0.
$$

**Consequence:** If the flow starts irrotational, it remains irrotational for all time (in the absence of viscosity).

---

## ✍️ 5. Proofs / Derivations

### Proof 5.1 — Derivation of Euler's Equation (Theorem 6.3.1)

**Goal:** From Cauchy's equation $\rho a_i = \partial_j \sigma_{ij} + \rho b_i$ with $\sigma_{ij} = -p\delta_{ij}$, derive Euler's equation.

**Step 1: Compute $\partial_j \sigma_{ij}$ for the inviscid stress.**

$$
\frac{\partial \sigma_{ij}}{\partial x_j} = \frac{\partial (-p\, \delta_{ij})}{\partial x_j} = -\delta_{ij}\frac{\partial p}{\partial x_j} = -\frac{\partial p}{\partial x_i}.
$$

(The Kronecker delta selects $j = i$ in the summation.)

**Step 2: Substitute into Cauchy's equation.**

$$
\rho\, a_i = -\frac{\partial p}{\partial x_i} + \rho\, b_i.
$$

**Step 3: Divide by $\rho$ and write in vector form.**

$$
\frac{Dv_i}{Dt} = -\frac{1}{\rho}\frac{\partial p}{\partial x_i} + b_i \quad \Longleftrightarrow \quad \frac{D\mathbf{v}}{Dt} = -\frac{\nabla p}{\rho} + \mathbf{b}. \quad \blacksquare
$$

### Proof 5.2 — Derivation of Bernoulli's Equation (Theorem 6.3.2)

**Goal:** For steady, incompressible, inviscid flow with gravity, show $p + \frac{1}{2}\rho v^2 + \rho gz = \text{const}$ along streamlines.

**Step 1: Write Euler's equation for steady flow ($\partial \mathbf{v}/\partial t = 0$) with $\mathbf{b} = -g\hat{z}$.**

$$
(\mathbf{v} \cdot \nabla)\mathbf{v} = -\frac{1}{\rho}\nabla p - g\hat{z}.
$$

**Step 2: Apply Lamb's identity (Lemma 6.3.1).**

$$
\nabla\left(\frac{v^2}{2}\right) + \boldsymbol{\omega} \times \mathbf{v} = -\frac{1}{\rho}\nabla p - \nabla(gz).
$$

**Step 3: Rearrange.**

$$
\nabla\left(\frac{v^2}{2} + \frac{p}{\rho} + gz\right) = -\boldsymbol{\omega} \times \mathbf{v}.
$$

**Step 4: Take the dot product with $\mathbf{v}$ (project along a streamline).**

$$
\mathbf{v} \cdot \nabla\left(\frac{v^2}{2} + \frac{p}{\rho} + gz\right) = -\mathbf{v} \cdot (\boldsymbol{\omega} \times \mathbf{v}).
$$

The right side is zero because $\boldsymbol{\omega} \times \mathbf{v}$ is perpendicular to $\mathbf{v}$:

$$
\mathbf{v} \cdot (\boldsymbol{\omega} \times \mathbf{v}) = 0 \quad (\text{scalar triple product with two identical vectors}).
$$

**Step 5: Interpret the result.**

$\mathbf{v} \cdot \nabla B = 0$ means the directional derivative of $B = \frac{v^2}{2} + \frac{p}{\rho} + gz$ in the direction of flow is zero. Therefore $B$ is constant along streamlines:

$$
p + \frac{1}{2}\rho v^2 + \rho g z = \text{const along each streamline}. \quad \blacksquare
$$

### Proof 5.3 — Strong Bernoulli for Irrotational Flow (Theorem 6.3.3)

**Goal:** If $\boldsymbol{\omega} = 0$, the Bernoulli constant is uniform across all streamlines.

**Step 1:** From Step 3 of Proof 5.2:

$$
\nabla\left(\frac{v^2}{2} + \frac{p}{\rho} + gz\right) = -\boldsymbol{\omega} \times \mathbf{v}.
$$

**Step 2:** If $\boldsymbol{\omega} = 0$, the right side vanishes:

$$
\nabla\left(\frac{v^2}{2} + \frac{p}{\rho} + gz\right) = \mathbf{0}.
$$

**Step 3:** A function whose gradient is zero everywhere (in a connected domain) is constant:

$$
\frac{v^2}{2} + \frac{p}{\rho} + gz = C \quad \text{(same constant everywhere)}. \quad \blacksquare
$$

### Proof 5.4 — Kelvin's Circulation Theorem (Theorem 6.3.4)

**Goal:** Show $d\Gamma/dt = 0$ for inviscid barotropic flow with conservative body forces.

**Step 1: Apply Lemma 6.3.2.**

$$
\frac{d\Gamma}{dt} = \oint_{C(t)} \frac{D\mathbf{v}}{Dt} \cdot d\mathbf{r}.
$$

**Step 2: Substitute Euler's equation.**

$$
\frac{D\mathbf{v}}{Dt} = -\frac{\nabla p}{\rho} + \mathbf{b} = -\nabla P - \nabla \Phi,
$$

where $P = \int dp'/\rho(p')$ (barotropic pressure function) and $\mathbf{b} = -\nabla \Phi$ (conservative body force).

**Step 3: Substitute into the circulation integral.**

$$
\frac{d\Gamma}{dt} = \oint_{C(t)} (-\nabla P - \nabla \Phi) \cdot d\mathbf{r} = -\oint_{C(t)} \nabla(P + \Phi) \cdot d\mathbf{r}.
$$

**Step 4: The line integral of a gradient around a closed loop vanishes.**

$$
\oint_{C(t)} \nabla(P + \Phi) \cdot d\mathbf{r} = 0,
$$

because $P + \Phi$ is single-valued (the loop returns to its starting point).

**Step 5: Conclude.**

$$
\frac{d\Gamma}{dt} = 0. \quad \blacksquare
$$




---

## 🧮 6. Worked Examples

### Example 6.3.1 — Pressure Field for a Vortex Flow

**Problem.** A 2D irrotational vortex has velocity $v_\theta = \Gamma/(2\pi r)$, $v_r = 0$ in cylindrical coordinates. Find the pressure field $p(r)$ assuming incompressible flow with no gravity.

**Solution.**

**Step 1:** For steady, irrotational, incompressible flow, apply the strong Bernoulli equation:

$$
p + \frac{1}{2}\rho v^2 = p_\infty + 0 \quad (\text{taking } v \to 0 \text{ as } r \to \infty).
$$

**Step 2:** The speed at radius $r$ is $v = v_\theta = \frac{\Gamma}{2\pi r}$.

**Step 3:** Substitute:

$$
p(r) = p_\infty - \frac{1}{2}\rho\left(\frac{\Gamma}{2\pi r}\right)^2 = p_\infty - \frac{\rho \Gamma^2}{8\pi^2 r^2}.
$$

**Step 4:** Verify via the radial Euler equation. In cylindrical coordinates, the radial momentum equation for $v_r = 0$:

$$
-\frac{v_\theta^2}{r} = -\frac{1}{\rho}\frac{\partial p}{\partial r}.
$$

$$
\frac{\partial p}{\partial r} = \frac{\rho v_\theta^2}{r} = \frac{\rho \Gamma^2}{4\pi^2 r^3}.
$$

Integrate: $p(r) = -\frac{\rho \Gamma^2}{8\pi^2 r^2} + C$. Setting $p(\infty) = p_\infty$ gives $C = p_\infty$. ✓

---

### Example 6.3.2 — Pitot Tube (Stagnation Pressure Measurement)

**Problem.** A Pitot tube in an airstream measures stagnation pressure $p_0 = 102{,}500$ Pa. A static port measures $p = 101{,}325$ Pa. Air density is $\rho = 1.225$ kg/m³. Find the airspeed.

**Solution.**

**Step 1:** Apply Bernoulli between the free stream and the stagnation point:

$$
p + \frac{1}{2}\rho v^2 = p_0.
$$

**Step 2:** Solve for $v$:

$$
v = \sqrt{\frac{2(p_0 - p)}{\rho}} = \sqrt{\frac{2(102500 - 101325)}{1.225}} = \sqrt{\frac{2 \times 1175}{1.225}} = \sqrt{1918.4} \approx 43.8 \;\text{m/s}.
$$

**Step 3:** Convert to more familiar units: $43.8$ m/s $\approx 157.7$ km/h $\approx 85.2$ knots.

**Step 4:** Check Mach number: $M = v/c \approx 43.8/343 \approx 0.128$. Since $M < 0.3$, the incompressible Bernoulli equation is valid.

---

### Example 6.3.3 — Torricelli's Theorem (Draining Tank)

**Problem.** A large open tank filled with water to height $h$ above a small orifice at the bottom. Find the exit velocity.

**Solution.**

**Step 1:** Apply Bernoulli between the free surface (point 1) and the orifice (point 2).

At point 1: $v_1 \approx 0$ (large tank), $p_1 = p_{\text{atm}}$, $z_1 = h$.
At point 2: $v_2 = ?$, $p_2 = p_{\text{atm}}$ (free jet), $z_2 = 0$.

**Step 2:** Bernoulli's equation:

$$
p_{\text{atm}} + 0 + \rho g h = p_{\text{atm}} + \frac{1}{2}\rho v_2^2 + 0.
$$

**Step 3:** Cancel $p_{\text{atm}}$ and solve:

$$
\rho g h = \frac{1}{2}\rho v_2^2 \implies v_2 = \sqrt{2gh}.
$$

This is **Torricelli's theorem** — the exit velocity equals the free-fall velocity from height $h$.

---

### Example 6.3.4 — Unsteady Euler: Pressure in an Accelerating Fluid Column

**Problem.** A vertical column of incompressible fluid (density $\rho$, height $L$) is accelerated upward with acceleration $a$. Find the pressure difference between bottom and top.

**Solution.**

**Step 1:** Apply Euler's equation in the vertical ($z$) direction with $\mathbf{b} = -g\hat{z}$:

$$
\rho\frac{Dv_z}{Dt} = -\frac{\partial p}{\partial z} - \rho g.
$$

**Step 2:** The fluid accelerates uniformly: $\frac{Dv_z}{Dt} = a$ (given). The flow is uniform in space, so $(\mathbf{v} \cdot \nabla)v_z = 0$ and $\frac{Dv_z}{Dt} = \frac{\partial v_z}{\partial t} = a$.

**Step 3:** Therefore:

$$
\frac{\partial p}{\partial z} = -\rho(g + a).
$$

**Step 4:** Integrate from bottom ($z = 0$) to top ($z = L$):

$$
p_{\text{top}} - p_{\text{bottom}} = -\rho(g + a)L.
$$

$$
\Delta p = p_{\text{bottom}} - p_{\text{top}} = \rho(g + a)L.
$$

The effective gravity is $g + a$ — the fluid "feels" heavier when accelerated upward.

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- **Prerequisites:** [6.1 - Stress & Strain Tensors in Continua](6.1---Stress-&-Strain-Tensors-in-Continua) (Cauchy's equation), [6.2 - Mass Conservation - The Continuity Equation](6.2---Mass-Conservation---The-Continuity-Equation) (continuity), [1.6 - Vector Fields, Div & Curl](1.6---Vector-Fields,-Div-&-Curl) (curl, divergence), [1.7 - Green's Stokes' and Divergence Theorems](1.7---Green's-Stokes'-and-Divergence-Theorems) (Stokes' theorem for circulation)
- **Extensions:** [6.4 - Viscous Fluids - The Navier-Stokes Equations](6.4---Viscous-Fluids---The-Navier-Stokes-Equations) (adds viscous terms), [6.6 - Vorticity & Potential Flow](6.6---Vorticity-&-Potential-Flow) (irrotational flow theory), [6.8 - Compressible Flow & Shock Waves](6.8---Compressible-Flow-&-Shock-Waves) (compressible Euler)
- **Applications:** [4.3 - Conservation Laws & Symmetry (Noether's Theorem)](4.3---Conservation-Laws-&-Symmetry-(Noether's-Theorem)) (Lagrangian mechanics connection)

### External Resources
- Euler, L., "Principes généraux du mouvement des fluides" (1757) — the original paper.
- Batchelor, G.K., *An Introduction to Fluid Dynamics*, Ch. 3 — Equations of Motion for Inviscid Flow.
- Landau & Lifshitz, *Fluid Mechanics*, §2 — Ideal Fluids (the most elegant derivation).
- NCFMF Film: *Pressure Fields and Fluid Acceleration* — visual demonstration of Euler's equation.




---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — Steady-State Bernoulli on a Venturi Meter

**Problem.** A horizontal Venturi meter carries water ($\rho = 998$ kg/m³). The pipe diameter is $D_1 = 0.20$ m and the throat diameter is $D_2 = 0.10$ m. A differential manometer reads a pressure difference of $\Delta p = p_1 - p_2 = 30{,}000$ Pa between the upstream section and the throat. Find the volumetric flow rate $Q$.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: State Bernoulli's Equation

For steady, incompressible, inviscid flow along a horizontal streamline:

$$
p_1 + \frac{1}{2}\rho v_1^2 = p_2 + \frac{1}{2}\rho v_2^2.
$$

(The $\rho g z$ terms cancel since the pipe is horizontal.)

#### Step 2: Apply Continuity

$$
A_1 v_1 = A_2 v_2 \implies v_1 = v_2 \frac{A_2}{A_1} = v_2 \left(\frac{D_2}{D_1}\right)^2 = v_2 \left(\frac{0.10}{0.20}\right)^2 = \frac{v_2}{4}.
$$

#### Step 3: Substitute into Bernoulli

$$
p_1 - p_2 = \frac{1}{2}\rho(v_2^2 - v_1^2) = \frac{1}{2}\rho\left(v_2^2 - \frac{v_2^2}{16}\right) = \frac{1}{2}\rho v_2^2\left(\frac{15}{16}\right).
$$

#### Step 4: Solve for $v_2$

$$
v_2^2 = \frac{2 \Delta p}{\rho} \cdot \frac{16}{15} = \frac{2 \times 30000}{998} \cdot \frac{16}{15} = 60.12 \times 1.0667 = 64.13\;\text{m}^2/\text{s}^2.
$$

$$
v_2 = \sqrt{64.13} = 8.008\;\text{m/s}.
$$

#### Step 5: Compute the Volumetric Flow Rate

$$
Q = A_2 v_2 = \frac{\pi (0.10)^2}{4} \times 8.008 = 7.854 \times 10^{-3} \times 8.008 = 0.0629\;\text{m}^3/\text{s}.
$$

#### Step 6: Express in General Form (Venturi Equation)

The general Venturi formula is:

$$
Q = A_2 \sqrt{\frac{2\Delta p}{\rho(1 - \beta^4)}},
$$

where $\beta = D_2/D_1 = 0.5$. Check: $1 - \beta^4 = 1 - 0.0625 = 0.9375$, and:

$$
Q = 7.854 \times 10^{-3} \sqrt{\frac{2 \times 30000}{998 \times 0.9375}} = 7.854 \times 10^{-3} \sqrt{64.13} = 7.854 \times 10^{-3} \times 8.008 = 0.0629\;\text{m}^3/\text{s}. \quad \checkmark
$$

**Final Answer:**

$$
Q = 0.0629\;\text{m}^3/\text{s} = 62.9\;\text{L/s}.
$$

</details>

### Example 8.2 — Unsteady Bernoulli for an Accelerating Pipe Flow

**Problem.** A horizontal pipe of length $L = 5$ m and constant cross-section connects two large reservoirs. At $t = 0$, a valve is opened and the pressure difference between the reservoirs is $\Delta p = p_1 - p_2 = 50{,}000$ Pa. Using the unsteady Bernoulli equation, find the fluid acceleration and the time to reach 90% of the steady-state velocity. Assume inviscid, incompressible flow with $\rho = 1000$ kg/m³.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: State the Unsteady Bernoulli Equation

For irrotational, incompressible flow, the unsteady Bernoulli equation along a streamline from point 1 to point 2 is:

$$
\frac{\partial \phi}{\partial t}\bigg|_1^2 + \frac{p_2 - p_1}{\rho} + \frac{1}{2}(v_2^2 - v_1^2) + g(z_2 - z_1) = 0.
$$

For a pipe of constant cross-section, $v_1 = v_2 = v(t)$ (uniform velocity), and the pipe is horizontal ($z_1 = z_2$). The unsteady term becomes:

$$
\frac{\partial \phi}{\partial t}\bigg|_1^2 = \int_1^2 \frac{\partial v}{\partial t}\, ds = \frac{dv}{dt} \cdot L,
$$

since $v$ is uniform along the pipe and $\partial v/\partial t = dv/dt$ (no spatial variation).

#### Step 2: Simplified Unsteady Bernoulli

$$
\rho L \frac{dv}{dt} = p_1 - p_2 = \Delta p.
$$

This is simply Newton's second law for the fluid column: mass per unit area $= \rho L$, force per unit area $= \Delta p$.

#### Step 3: Solve for Acceleration

$$
\frac{dv}{dt} = \frac{\Delta p}{\rho L} = \frac{50000}{1000 \times 5} = 10\;\text{m/s}^2.
$$

The acceleration is constant (in this inviscid model), so the velocity grows linearly:

$$
v(t) = \frac{\Delta p}{\rho L}\, t = 10t.
$$

#### Step 4: Determine the Steady-State Velocity

In reality, the flow reaches a steady state when viscous losses balance the pressure difference. For an inviscid model, there is no steady state — the velocity grows without bound. This reveals the limitation of the inviscid assumption.

For a real pipe with friction factor $f$ and diameter $D$, the steady-state velocity satisfies:

$$
\Delta p = f \frac{L}{D} \frac{1}{2}\rho v_\infty^2 \implies v_\infty = \sqrt{\frac{2D\,\Delta p}{f L \rho}}.
$$

With $D = 0.05$ m and $f = 0.02$ (turbulent):

$$
v_\infty = \sqrt{\frac{2 \times 0.05 \times 50000}{0.02 \times 5 \times 1000}} = \sqrt{\frac{5000}{100}} = \sqrt{50} = 7.07\;\text{m/s}.
$$

#### Step 5: Time to 90% of Steady State (with Friction)

Including friction, the equation of motion becomes:

$$
\rho L \frac{dv}{dt} = \Delta p - f\frac{L}{D}\frac{1}{2}\rho v^2.
$$

Let $a_0 = \Delta p/(\rho L) = 10$ m/s² and $k = f/(2D) = 0.02/(2 \times 0.05) = 0.2$ m⁻¹. Then:

$$
\frac{dv}{dt} = a_0 - k v^2 = a_0\left(1 - \frac{v^2}{v_\infty^2}\right),
$$

where $v_\infty = \sqrt{a_0/k} = \sqrt{10/0.2} = \sqrt{50} = 7.07$ m/s. ✓

This is a separable ODE:

$$
\frac{dv}{1 - v^2/v_\infty^2} = a_0\, dt.
$$

$$
\int_0^v \frac{dv'}{1 - (v'/v_\infty)^2} = a_0 t.
$$

Using partial fractions: $\frac{1}{1-u^2} = \frac{1}{2}\left(\frac{1}{1-u} + \frac{1}{1+u}\right)$ with $u = v'/v_\infty$:

$$
v_\infty \cdot \frac{1}{2}\ln\frac{1 + v/v_\infty}{1 - v/v_\infty} = a_0 t.
$$

$$
v(t) = v_\infty \tanh\left(\frac{a_0 t}{v_\infty}\right).
$$

#### Step 6: Time to Reach $v = 0.9 v_\infty$

$$
0.9 = \tanh\left(\frac{a_0 t_{90}}{v_\infty}\right) \implies \frac{a_0 t_{90}}{v_\infty} = \text{arctanh}(0.9) = \frac{1}{2}\ln\frac{1.9}{0.1} = \frac{1}{2}\ln 19 = 1.472.
$$

$$
t_{90} = \frac{1.472 \times v_\infty}{a_0} = \frac{1.472 \times 7.07}{10} = 1.04\;\text{s}.
$$

**Final Answer:**

$$
\frac{dv}{dt}\bigg|_{t=0} = 10\;\text{m/s}^2, \qquad t_{90\%} = 1.04\;\text{s}.
$$

</details>

### Example 8.3 — Pressure Distribution on a Curved Streamline (Cyclostrophic Balance)

**Problem.** Air ($\rho = 1.2$ kg/m³) flows in a horizontal plane with purely circular streamlines (a free vortex) with tangential velocity $v_\theta = \Gamma/(2\pi r)$ where $\Gamma = 100$ m²/s. Find the radial pressure gradient and the pressure difference between $r = 50$ m and $r = 200$ m.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Euler's Equation in the Radial Direction (Normal to Streamline)

For steady flow along curved streamlines, the component of Euler's equation normal to the streamline (pointing toward the center of curvature) is:

$$
\frac{\partial p}{\partial r} = \frac{\rho v_\theta^2}{r}.
$$

This is the **cyclostrophic balance**: the centripetal acceleration $v_\theta^2/r$ is balanced by the radial pressure gradient.

#### Step 2: Substitute the Free Vortex Profile

$$
v_\theta = \frac{\Gamma}{2\pi r} \implies v_\theta^2 = \frac{\Gamma^2}{4\pi^2 r^2}.
$$

$$
\frac{\partial p}{\partial r} = \frac{\rho}{r} \cdot \frac{\Gamma^2}{4\pi^2 r^2} = \frac{\rho \Gamma^2}{4\pi^2 r^3}.
$$

#### Step 3: Integrate to Find Pressure Difference

$$
p(r_2) - p(r_1) = \int_{r_1}^{r_2} \frac{\rho \Gamma^2}{4\pi^2 r^3}\, dr = \frac{\rho \Gamma^2}{4\pi^2}\left[-\frac{1}{2r^2}\right]_{r_1}^{r_2} = \frac{\rho \Gamma^2}{8\pi^2}\left(\frac{1}{r_1^2} - \frac{1}{r_2^2}\right).
$$

#### Step 4: Substitute Numerical Values

With $r_1 = 50$ m, $r_2 = 200$ m, $\Gamma = 100$ m²/s, $\rho = 1.2$ kg/m³:

$$
p(200) - p(50) = \frac{1.2 \times 10000}{8\pi^2}\left(\frac{1}{2500} - \frac{1}{40000}\right).
$$

$$
= \frac{12000}{78.96}\left(4 \times 10^{-4} - 2.5 \times 10^{-5}\right) = 151.9 \times 3.75 \times 10^{-4} = 0.0570\;\text{Pa} \cdot \frac{1000}{1}.
$$

Let me redo this carefully:

$$
\frac{\rho \Gamma^2}{8\pi^2} = \frac{1.2 \times (100)^2}{8 \times 9.8696} = \frac{12000}{78.957} = 151.98\;\text{Pa·m}^2.
$$

$$
\frac{1}{r_1^2} - \frac{1}{r_2^2} = \frac{1}{2500} - \frac{1}{40000} = 0.0004 - 0.000025 = 3.75 \times 10^{-4}\;\text{m}^{-2}.
$$

$$
\Delta p = 151.98 \times 3.75 \times 10^{-4} = 0.057\;\text{Pa}.
$$

This is extremely small because the air density is low and the radii are large. For a tornado with $\Gamma = 10{,}000$ m²/s at $r = 50$ m:

$$
\Delta p \propto \Gamma^2 \implies \Delta p_{\text{tornado}} = 0.057 \times (100)^2 = 570\;\text{Pa} \approx 5.7\;\text{mbar}.
$$

At smaller radii (e.g., $r_1 = 5$ m), the pressure drop is much larger — this is why tornadoes have such low core pressures.

#### Step 5: Verify with Bernoulli

Along a streamline (which is a circle at constant $r$), Bernoulli gives $p + \frac{1}{2}\rho v_\theta^2 = \text{const}$ only if we move along the streamline — but since $v_\theta$ is constant on a circle, $p$ is also constant on each streamline. Between streamlines, we must use the radial Euler equation (which we did). Alternatively, Bernoulli between two points on different streamlines of an irrotational flow:

$$
p + \frac{1}{2}\rho v^2 = \text{const everywhere (for irrotational flow)}.
$$

The free vortex IS irrotational ($\nabla \times \mathbf{v} = 0$ for $r \gt  0$), so:

$$
p_1 + \frac{1}{2}\rho v_1^2 = p_2 + \frac{1}{2}\rho v_2^2.
$$

$$
p_2 - p_1 = \frac{1}{2}\rho(v_1^2 - v_2^2) = \frac{\rho \Gamma^2}{8\pi^2}\left(\frac{1}{r_1^2} - \frac{1}{r_2^2}\right). \quad \checkmark
$$

**Final Answer:**

$$
\frac{\partial p}{\partial r} = \frac{\rho \Gamma^2}{4\pi^2 r^3}, \qquad \Delta p = p(200) - p(50) = 0.057\;\text{Pa}.
$$

</details>

### Example 8.4 — Steady Bernoulli with Gravity: Siphon Flow

**Problem.** A siphon draws water from a reservoir. The inlet is at depth $h_1 = 0.5$ m below the surface, the crest of the siphon is at height $h_c = 2.0$ m above the surface, and the outlet is at $h_2 = 3.0$ m below the surface. Find (a) the exit velocity, (b) the pressure at the crest, and (c) the maximum allowable crest height before cavitation (vapor pressure $p_v = 2.34$ kPa at 20°C).

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Exit Velocity (Bernoulli from Surface to Outlet)

Take the free surface as datum ($z = 0$). At the surface: $v_1 \approx 0$, $p_1 = p_{\text{atm}}$, $z_1 = 0$. At the outlet: $v_2 = ?$, $p_2 = p_{\text{atm}}$ (free jet), $z_2 = -h_2 = -3.0$ m.

$$
p_{\text{atm}} + 0 + 0 = p_{\text{atm}} + \frac{1}{2}\rho v_2^2 + \rho g(-3.0).
$$

$$
0 = \frac{1}{2}\rho v_2^2 - \rho g(3.0) \implies v_2 = \sqrt{2g \times 3.0} = \sqrt{2 \times 9.81 \times 3.0} = \sqrt{58.86} = 7.67\;\text{m/s}.
$$

#### Step 2: Pressure at the Crest (Bernoulli from Surface to Crest)

At the crest: $v_c = v_2$ (constant cross-section siphon), $z_c = +2.0$ m.

$$
p_{\text{atm}} + 0 + 0 = p_c + \frac{1}{2}\rho v_c^2 + \rho g(2.0).
$$

$$
p_c = p_{\text{atm}} - \frac{1}{2}\rho v_c^2 - \rho g(2.0).
$$

$$
p_c = 101325 - \frac{1}{2}(1000)(7.67)^2 - 1000 \times 9.81 \times 2.0.
$$

$$
= 101325 - 29415 - 19620 = 52290\;\text{Pa} = 52.3\;\text{kPa}.
$$

#### Step 3: Maximum Crest Height Before Cavitation

Cavitation occurs when $p_c \leq p_v = 2340$ Pa. Set $p_c = p_v$:

$$
p_v = p_{\text{atm}} - \frac{1}{2}\rho v_c^2 - \rho g h_{c,\max}.
$$

$$
\rho g h_{c,\max} = p_{\text{atm}} - p_v - \frac{1}{2}\rho v_c^2.
$$

But $v_c$ depends on the total height difference $H = h_c + h_2$ (from crest to outlet): actually, $v_c = v_2 = \sqrt{2g(h_c + h_2 - h_c)} = \sqrt{2g \cdot h_2}$... 

Wait — let me reconsider. The exit velocity depends on the height difference between the free surface and the outlet, not the crest height. So $v_2 = \sqrt{2g \times 3.0}$ regardless of crest height (as long as the siphon is running). Then:

$$
h_{c,\max} = \frac{p_{\text{atm}} - p_v}{\rho g} - \frac{v_2^2}{2g} = \frac{101325 - 2340}{1000 \times 9.81} - \frac{58.86}{2 \times 9.81}.
$$

$$
= \frac{98985}{9810} - 3.0 = 10.09 - 3.0 = 7.09\;\text{m}.
$$

So the crest can be at most about 7.1 m above the free surface before cavitation breaks the siphon.

**Final Answer:**

$$
v_2 = 7.67\;\text{m/s}, \quad p_c = 52.3\;\text{kPa}, \quad h_{c,\max} = 7.09\;\text{m}.
$$

</details>

---

## 📘 9. Appendix: Extended Derivations & Special Cases

### 9.1 Derivation of Bernoulli's Equation from Euler's Equation Along a Streamline

Bernoulli's equation is not an independent law — it is a *consequence* of Euler's equation integrated along a streamline. Here we derive it rigorously.

**Starting point: Euler's equation for inviscid flow.**

$$
\rho\frac{\partial \mathbf{v}}{\partial t} + \rho(\mathbf{v} \cdot \nabla)\mathbf{v} = -\nabla p + \rho \mathbf{g}.
$$

With $\mathbf{g} = -g\hat{z} = -\nabla(gz)$, rewrite:

$$
\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v} = -\frac{1}{\rho}\nabla p - \nabla(gz).
$$

**Step 1: Use the vector identity for the convective term.**

$$
(\mathbf{v} \cdot \nabla)\mathbf{v} = \nabla\left(\frac{v^2}{2}\right) - \mathbf{v} \times (\nabla \times \mathbf{v}) = \nabla\left(\frac{v^2}{2}\right) - \mathbf{v} \times \boldsymbol{\omega},
$$

where $\boldsymbol{\omega} = \nabla \times \mathbf{v}$ is the vorticity and $v^2 = \mathbf{v} \cdot \mathbf{v}$.

**Step 2: Substitute into Euler's equation.**

$$
\frac{\partial \mathbf{v}}{\partial t} + \nabla\left(\frac{v^2}{2}\right) - \mathbf{v} \times \boldsymbol{\omega} = -\frac{1}{\rho}\nabla p - \nabla(gz).
$$

**Step 3: Take the dot product with $d\mathbf{s}$ along a streamline.**

A streamline is a curve everywhere tangent to $\mathbf{v}$, so $d\mathbf{s} = \hat{\mathbf{s}}\, ds$ where $\hat{\mathbf{s}} = \mathbf{v}/|\mathbf{v}|$. The key observation: $(\mathbf{v} \times \boldsymbol{\omega}) \cdot \mathbf{v} = 0$ (a cross product is always perpendicular to both factors). Therefore:

$$
(\mathbf{v} \times \boldsymbol{\omega}) \cdot d\mathbf{s} = (\mathbf{v} \times \boldsymbol{\omega}) \cdot \hat{\mathbf{s}}\, ds = 0.
$$

The vorticity term vanishes when projected along the streamline!

**Step 4: Project the remaining terms.**

$$
\frac{\partial \mathbf{v}}{\partial t} \cdot d\mathbf{s} + \nabla\left(\frac{v^2}{2}\right) \cdot d\mathbf{s} = -\frac{1}{\rho}\nabla p \cdot d\mathbf{s} - \nabla(gz) \cdot d\mathbf{s}.
$$

Each gradient dotted with $d\mathbf{s}$ is a directional derivative along the streamline, i.e., $\nabla f \cdot d\mathbf{s} = df$:

$$
\frac{\partial \mathbf{v}}{\partial t} \cdot d\mathbf{s} + d\left(\frac{v^2}{2}\right) = -\frac{dp}{\rho} - d(gz).
$$

**Step 5: Integrate along the streamline from point 1 to point 2.**

$$
\int_1^2 \frac{\partial \mathbf{v}}{\partial t} \cdot d\mathbf{s} + \frac{v_2^2}{2} - \frac{v_1^2}{2} = -\int_1^2 \frac{dp}{\rho} - g(z_2 - z_1).
$$

**Step 6: Specialize to steady, incompressible flow.**

For steady flow: $\partial \mathbf{v}/\partial t = 0$. For incompressible flow: $\rho = \text{const}$, so $\int dp/\rho = (p_2 - p_1)/\rho$. The result is:

$$
\frac{v_2^2}{2} - \frac{v_1^2}{2} = -\frac{p_2 - p_1}{\rho} - g(z_2 - z_1).
$$

Rearranging:

$$
p_1 + \frac{1}{2}\rho v_1^2 + \rho g z_1 = p_2 + \frac{1}{2}\rho v_2^2 + \rho g z_2.
$$

This is **Bernoulli's equation** — valid along a streamline for steady, incompressible, inviscid flow.

**Critical observations:**
1. The derivation works along a streamline because the $\mathbf{v} \times \boldsymbol{\omega}$ term vanishes. For irrotational flow ($\boldsymbol{\omega} = 0$), this term vanishes everywhere, and Bernoulli holds between *any* two points (not just along a streamline).
2. The equation is an energy equation: $p/\rho$ is pressure energy per unit mass (flow work), $v^2/2$ is kinetic energy, $gz$ is potential energy. Their sum is constant along a streamline.
3. For compressible flow, replace $p/\rho$ with $\int dp/\rho$ (which requires a thermodynamic relation like isentropic: $p/\rho^\gamma = \text{const}$).

### 9.2 Kelvin's Circulation Theorem from Euler's Equation

**Theorem (Kelvin, 1869).** In an inviscid, barotropic fluid with conservative body forces, the circulation $\Gamma = \oint_C \mathbf{v} \cdot d\mathbf{l}$ around any material loop $C(t)$ is constant in time:

$$
\frac{D\Gamma}{Dt} = 0.
$$

**Proof from Euler's equation.**

**Step 1:** Write the circulation as an integral over a material loop parameterized by a label $s$:

$$
\Gamma(t) = \oint_{C(t)} \mathbf{v} \cdot d\mathbf{l} = \oint v_i\, dx_i.
$$

**Step 2:** Take the material derivative. Since the loop moves with the fluid:

$$
\frac{D\Gamma}{Dt} = \oint \frac{Dv_i}{Dt}\, dx_i + \oint v_i\, \frac{D(dx_i)}{Dt}.
$$

**Step 3:** Evaluate the second integral. For a material element, $D(dx_i)/Dt = dv_i$ (the velocity difference between neighboring material points). Therefore:

$$
\oint v_i\, dv_i = \oint d\left(\frac{v^2}{2}\right) = 0,
$$

since the integral of an exact differential around a closed loop vanishes.

**Step 4:** Evaluate the first integral using Euler's equation. From $\rho Dv_i/Dt = -\partial p/\partial x_i + \rho b_i$ (where $\mathbf{b} = -\nabla\Phi$ is conservative):

$$
\frac{Dv_i}{Dt} = -\frac{1}{\rho}\frac{\partial p}{\partial x_i} - \frac{\partial \Phi}{\partial x_i}.
$$

$$
\oint \frac{Dv_i}{Dt}\, dx_i = -\oint \frac{1}{\rho}\frac{\partial p}{\partial x_i}\, dx_i - \oint \frac{\partial \Phi}{\partial x_i}\, dx_i = -\oint \frac{dp}{\rho} - \oint d\Phi.
$$

The second integral vanishes (exact differential around a closed loop). For the first: if the fluid is **barotropic** ($\rho = \rho(p)$ only), then $dp/\rho = dP$ where $P = \int dp/\rho$ is a function of $p$ alone. Therefore $\oint dp/\rho = \oint dP = 0$.

**Step 5:** Combining:

$$
\frac{D\Gamma}{Dt} = 0 + 0 = 0. \quad \blacksquare
$$

**Physical meaning:** Vorticity cannot be created or destroyed in the interior of an inviscid, barotropic fluid with conservative body forces. Vorticity can only be generated at boundaries (where the inviscid assumption breaks down) or by baroclinic effects ($\nabla\rho \times \nabla p \neq 0$, as in atmospheric fronts).

**References:** Batchelor, §5.3; Kundu & Cohen, §5.5; Landau & Lifshitz, *Fluid Mechanics*, §8.

---
