---
title: "Dimensionless Numbers Reynolds Froude"
subject: "Fluid Dynamics & Continuum Mechanics"
catalog: advanced
audience_tier: higher-education
chapter: "6.5"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 6.5 — Dimensionless Numbers: Reynolds & Froude

> *"The theory of dimensions is the most powerful tool in the physicist's workshop — it can extract the essential physics from a problem before a single equation is solved."* — P.W. Bridgman, *Dimensional Analysis* (1922).

Dimensional analysis is the art of extracting physical insight from the requirement that equations must be dimensionally consistent. The Buckingham Pi theorem guarantees that any physical relationship can be rewritten in terms of dimensionless groups — and these groups reveal which forces dominate, when flows are similar, and how to scale laboratory models to full-size systems. This chapter develops the theory systematically, derives the key dimensionless numbers of fluid mechanics, and shows how they emerge from non-dimensionalizing the governing equations.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. State and prove the Buckingham Pi theorem.
2. Apply the method of repeating variables to construct dimensionless groups.
3. Derive the Reynolds number from the ratio of inertial to viscous forces.
4. Derive the Froude number from the ratio of inertial to gravitational forces.
5. Identify and interpret Mach, Weber, Strouhal, Euler, and Péclet numbers.
6. Apply dynamic similarity to scale model experiments.
7. Non-dimensionalize the N-S equations and identify all governing parameters.

---

## 🖼️ Visual Anchor — Flow Regime Map (Re vs. Geometry)

A visual map showing how the Reynolds number determines flow character: creeping flow, laminar, transitional, and turbulent regimes for different geometries.

![math-06__6.5-fig1](math-06__6.5-fig1.svg)

---

## 📚 1. Definitions

### Definition 6.5.1 — Dimensional Homogeneity

A physical equation is **dimensionally homogeneous** if every additive term has the same dimensions. This is a necessary (but not sufficient) condition for physical correctness.

### Definition 6.5.2 — Fundamental Dimensions

In mechanics, the three fundamental (independent) dimensions are:
- **M** — Mass
- **L** — Length  
- **T** — Time

For problems involving heat transfer, add **Θ** (Temperature). For electromagnetism, add **I** (Current).

### Definition 6.5.3 — Dimensionless Group (Pi Group)

A **dimensionless group** $\Pi$ is a product of physical variables raised to powers such that the resulting combination has no dimensions:

$$
\Pi = q_1^{a_1} q_2^{a_2} \cdots q_n^{a_n}, \quad [\Pi] = M^0 L^0 T^0.
$$

### Definition 6.5.4 — Reynolds Number

The **Reynolds number** is the ratio of inertial forces to viscous forces:

$$
\text{Re} = \frac{\rho U L}{\mu} = \frac{UL}{\nu},
$$

where $U$ is a characteristic velocity, $L$ is a characteristic length, $\rho$ is density, $\mu$ is dynamic viscosity, and $\nu = \mu/\rho$ is kinematic viscosity.

**Physical interpretation:** Re $\gg 1$ means inertia dominates (inviscid behavior, potential for turbulence). Re $\ll 1$ means viscosity dominates (creeping/Stokes flow, reversible, no turbulence).

### Definition 6.5.5 — Froude Number

The **Froude number** is the ratio of inertial forces to gravitational forces:

$$
\text{Fr} = \frac{U}{\sqrt{gL}},
$$

where $g$ is gravitational acceleration. It governs free-surface flows (waves, ship hulls, open channels).

### Definition 6.5.6 — Mach Number

The **Mach number** is the ratio of flow speed to the speed of sound:

$$
M = \frac{U}{c},
$$

where $c = \sqrt{\gamma R T / M_w}$ for an ideal gas. $M < 0.3$: incompressible. $M > 1$: supersonic (see [6.8 - Compressible Flow & Shock Waves](6.8---Compressible-Flow-&-Shock-Waves)).

### Definition 6.5.7 — Strouhal Number

The **Strouhal number** characterizes oscillating flows:

$$
\text{St} = \frac{fL}{U},
$$

where $f$ is the frequency of vortex shedding or oscillation. For a cylinder: $\text{St} \approx 0.2$ over a wide range of Re.

### Definition 6.5.8 — Weber Number

The **Weber number** is the ratio of inertial forces to surface tension forces:

$$
\text{We} = \frac{\rho U^2 L}{\sigma},
$$

where $\sigma$ is surface tension. Governs droplet breakup, bubble dynamics, and capillary flows.

### Definition 6.5.9 — Dynamic Similarity

Two flows are **dynamically similar** if they are geometrically similar (same shape) and all relevant dimensionless numbers are equal. Dynamically similar flows have identical dimensionless velocity, pressure, and force fields.




---

## 📐 2. Axioms / Postulates

### Axiom 6.5.A — Principle of Dimensional Homogeneity

Every term in a valid physical equation must have the same dimensions. No physical law can depend on the choice of unit system.

### Axiom 6.5.B — Completeness of Variable List

The Buckingham Pi theorem requires that the list of relevant variables be *complete* — it must include every quantity that affects the phenomenon. Missing a variable (e.g., forgetting surface tension in a capillary problem) yields incorrect dimensionless groups.

---

## 🛡️ 3. Lemmas

### Lemma 6.5.1 — Rank of the Dimensional Matrix

Given $n$ physical variables with dimensions expressible in terms of $k$ fundamental dimensions, the **dimensional matrix** $\mathbf{D}$ is the $k \times n$ matrix whose $(i,j)$ entry is the exponent of the $i$-th fundamental dimension in the $j$-th variable. The number of independent dimensionless groups is:

$$
p = n - r,
$$

where $r = \text{rank}(\mathbf{D}) \leq k$.

**Proof.** The dimensionless groups correspond to vectors $\mathbf{a} = (a_1, \ldots, a_n)^T$ in the null space of $\mathbf{D}$: $\mathbf{D}\mathbf{a} = \mathbf{0}$. By the rank-nullity theorem (see [2.3 - Null Space, Column Space & Rank](2.3---Null-Space,-Column-Space-&-Rank)):

$$
\dim(\text{null}(\mathbf{D})) = n - \text{rank}(\mathbf{D}) = n - r. \quad \blacksquare
$$

### Lemma 6.5.2 — Independence of Pi Groups

The $p = n - r$ dimensionless groups $\Pi_1, \ldots, \Pi_p$ constructed by the method of repeating variables are functionally independent (no $\Pi_i$ can be expressed as a product of powers of the others).

---

## 👑 4. Theorems

### Theorem 6.5.1 — Buckingham Pi Theorem

**Statement.** If a physical process involves $n$ dimensional variables $q_1, q_2, \ldots, q_n$ related by a dimensionally homogeneous equation $f(q_1, \ldots, q_n) = 0$, and these variables are expressible in terms of $k$ fundamental dimensions with dimensional matrix of rank $r$, then the relationship can be rewritten as:

$$
F(\Pi_1, \Pi_2, \ldots, \Pi_p) = 0, \quad p = n - r,
$$

where $\Pi_1, \ldots, \Pi_p$ are independent dimensionless groups formed from the original variables.

### Theorem 6.5.2 — Reynolds Number from N-S Non-Dimensionalization

Non-dimensionalizing the incompressible Navier-Stokes equations with characteristic scales $L$, $U$, $\rho$ yields:

$$
\frac{\partial \mathbf{v}^*}{\partial t^*} + (\mathbf{v}^* \cdot \nabla^*)\mathbf{v}^* = -\nabla^* p^* + \frac{1}{\text{Re}}\nabla^{*2}\mathbf{v}^*,
$$

where $\text{Re} = UL/\nu$ is the sole governing parameter for flows without gravity or other forces.

### Theorem 6.5.3 — Complete Non-Dimensionalization with Gravity

Including gravity $\mathbf{b} = -g\hat{z}$:

$$
\frac{\partial \mathbf{v}^*}{\partial t^*} + (\mathbf{v}^* \cdot \nabla^*)\mathbf{v}^* = -\nabla^* p^* + \frac{1}{\text{Re}}\nabla^{*2}\mathbf{v}^* + \frac{1}{\text{Fr}^2}\hat{z}^*,
$$

where $\text{Fr} = U/\sqrt{gL}$ is the Froude number.

---

## ✍️ 5. Proofs / Derivations

### Proof 5.1 — Proof of the Buckingham Pi Theorem (Theorem 6.5.1)

**Goal:** Show that $n$ variables with dimensional matrix of rank $r$ yield $p = n - r$ independent dimensionless groups.

**Step 1: Formulate the dimensional constraint.**

A dimensionless combination $\Pi = q_1^{a_1} q_2^{a_2} \cdots q_n^{a_n}$ requires:

$$
[q_1]^{a_1} [q_2]^{a_2} \cdots [q_n]^{a_n} = M^0 L^0 T^0.
$$

Writing $[q_j] = M^{d_{1j}} L^{d_{2j}} T^{d_{3j}}$ (entries of the dimensional matrix $\mathbf{D}$):

$$
\sum_{j=1}^n d_{ij}\, a_j = 0, \quad i = 1, \ldots, k.
$$

This is the linear system $\mathbf{D}\mathbf{a} = \mathbf{0}$.

**Step 2: Apply the rank-nullity theorem.**

The solution space (null space of $\mathbf{D}$) has dimension $n - r$ where $r = \text{rank}(\mathbf{D})$.

**Step 3: Each basis vector of the null space corresponds to one independent dimensionless group.**

Choose $n - r$ linearly independent solutions $\mathbf{a}^{(1)}, \ldots, \mathbf{a}^{(p)}$. Each defines a $\Pi_i = \prod_j q_j^{a_j^{(i)}}$.

**Step 4: The original relationship $f(q_1, \ldots, q_n) = 0$ can be rewritten.**

Since the physics cannot depend on the choice of units, the function $f$ must be expressible purely in terms of the dimensionless combinations. Therefore there exists $F$ such that $F(\Pi_1, \ldots, \Pi_p) = 0$. $\blacksquare$

### Proof 5.2 — Derivation of Reynolds Number as Force Ratio

**Goal:** Show Re = (inertial force)/(viscous force).

**Step 1: Estimate the inertial (convective) term in N-S.**

$$
\rho(\mathbf{v} \cdot \nabla)\mathbf{v} \sim \rho \cdot U \cdot \frac{U}{L} = \frac{\rho U^2}{L}.
$$

**Step 2: Estimate the viscous term.**

$$
\mu \nabla^2 \mathbf{v} \sim \mu \cdot \frac{U}{L^2}.
$$

**Step 3: Form the ratio.**

$$
\frac{\text{Inertial}}{\text{Viscous}} = \frac{\rho U^2 / L}{\mu U / L^2} = \frac{\rho U L}{\mu} = \text{Re}. \quad \blacksquare
$$

### Proof 5.3 — Method of Repeating Variables (Constructive Algorithm)

**Goal:** Provide the step-by-step algorithm for constructing Pi groups.

**Step 1: List all $n$ variables and their dimensions.**

Write the dimensional matrix $\mathbf{D}$ (rows = fundamental dimensions, columns = variables).

**Step 2: Determine the rank $r$ of $\mathbf{D}$.**

Compute $r = \text{rank}(\mathbf{D})$ (usually $r = k$ unless variables are dimensionally dependent).

**Step 3: Choose $r$ "repeating variables."**

Select $r$ variables that:
- Span all $k$ fundamental dimensions (their $r \times r$ submatrix has full rank).
- Do NOT include the "output" variable (the quantity you want to express).
- Typically choose: a length, a velocity, and a density (for mechanics problems).

**Step 4: Form each Pi group.**

For each of the remaining $p = n - r$ variables $q_j$, form:

$$
\Pi_j = q_j \cdot (x_1)^{a_1} (x_2)^{a_2} \cdots (x_r)^{a_r},
$$

where $x_1, \ldots, x_r$ are the repeating variables. Solve for exponents $a_1, \ldots, a_r$ by requiring $[\Pi_j] = M^0 L^0 T^0$.

**Step 5: Write the functional relationship.**

$$
\Pi_1 = f(\Pi_2, \Pi_3, \ldots, \Pi_p). \quad \blacksquare
$$

### Proof 5.4 — Derivation of Froude Number as Force Ratio

**Goal:** Show Fr = $U/\sqrt{gL}$ from the ratio of inertial to gravitational forces.

**Step 1: Inertial force per unit volume:** $\rho U^2 / L$.

**Step 2: Gravitational force per unit volume:** $\rho g$.

**Step 3: Ratio:**

$$
\frac{\text{Inertial}}{\text{Gravitational}} = \frac{\rho U^2 / L}{\rho g} = \frac{U^2}{gL} = \text{Fr}^2.
$$

Therefore $\text{Fr} = U/\sqrt{gL}$. $\blacksquare$

---

## 🧮 6. Worked Examples

### Example 6.5.1 — Drag on a Sphere (Buckingham Pi)

**Problem.** The drag force $F_D$ on a smooth sphere depends on: diameter $D$, velocity $U$, fluid density $\rho$, and viscosity $\mu$. Find the dimensionless relationship.

**Solution.**

**Step 1:** List variables: $F_D, D, U, \rho, \mu$. So $n = 5$.

**Step 2:** Fundamental dimensions: M, L, T. So $k = 3$.

**Step 3:** Dimensional matrix:

| | $F_D$ | $D$ | $U$ | $\rho$ | $\mu$ |
|---|---|---|---|---|---|
| M | 1 | 0 | 0 | 1 | 1 |
| L | 1 | 1 | 1 | -3 | -1 |
| T | -2 | 0 | -1 | 0 | -1 |

**Step 4:** Rank of matrix = 3 (the $3 \times 3$ submatrix from $D, U, \rho$ has det $\neq 0$). So $p = 5 - 3 = 2$ dimensionless groups.

**Step 5:** Choose repeating variables: $D, U, \rho$. Form $\Pi_1$ from $F_D$:

$$
\Pi_1 = F_D \cdot D^a U^b \rho^c.
$$

Require $[\Pi_1] = M^0 L^0 T^0$:
- M: $1 + c = 0 \implies c = -1$
- T: $-2 - b = 0 \implies b = -2$
- L: $1 + a + b - 3c = 1 + a - 2 + 3 = 0 \implies a = -2$

$$
\Pi_1 = \frac{F_D}{\rho U^2 D^2} = C_D \quad (\text{drag coefficient}).
$$

**Step 6:** Form $\Pi_2$ from $\mu$:

$$
\Pi_2 = \mu \cdot D^a U^b \rho^c.
$$

- M: $1 + c = 0 \implies c = -1$
- T: $-1 - b = 0 \implies b = -1$
- L: $-1 + a + b - 3c = -1 + a - 1 + 3 = 0 \implies a = -1$

$$
\Pi_2 = \frac{\mu}{\rho U D} = \frac{1}{\text{Re}}.
$$

**Step 7:** The dimensionless relationship is $C_D = f(\text{Re})$. For Stokes flow (Re $\ll 1$): $C_D = 24/\text{Re}$, giving $F_D = 3\pi \mu U D$ (Stokes drag).

---

### Example 6.5.2 — Model Ship Testing (Froude Similarity)

**Problem.** A 1:50 scale model of a ship is tested in a towing tank. The full-scale ship travels at 10 m/s. What model speed ensures Froude similarity? If the model drag is 5 N, what is the full-scale drag?

**Solution.**

**Step 1:** Froude similarity requires $\text{Fr}_m = \text{Fr}_p$:

$$
\frac{U_m}{\sqrt{g L_m}} = \frac{U_p}{\sqrt{g L_p}}.
$$

**Step 2:** Solve for model speed:

$$
U_m = U_p \sqrt{\frac{L_m}{L_p}} = 10 \sqrt{\frac{1}{50}} = \frac{10}{\sqrt{50}} = \frac{10}{7.07} \approx 1.41 \;\text{m/s}.
$$

**Step 3:** For wave drag (Froude-dominated), the force coefficient $C_F = F/(\rho U^2 L^2)$ is the same:

$$
\frac{F_p}{\rho_p U_p^2 L_p^2} = \frac{F_m}{\rho_m U_m^2 L_m^2}.
$$

**Step 4:** With same fluid ($\rho_p = \rho_m$):

$$
F_p = F_m \cdot \frac{U_p^2 L_p^2}{U_m^2 L_m^2} = F_m \cdot \frac{U_p^2}{U_m^2} \cdot \left(\frac{L_p}{L_m}\right)^2.
$$

Since $U_p/U_m = \sqrt{L_p/L_m} = \sqrt{50}$:

$$
F_p = 5 \cdot 50 \cdot 50^2 = 5 \cdot 50^3... 
$$

Wait — let us use the standard Froude scaling. With $\lambda = L_p/L_m = 50$:

$$
F_p = F_m \cdot \lambda^3 = 5 \times 50^3 = 5 \times 125{,}000 = 625{,}000 \;\text{N} = 625 \;\text{kN}.
$$

(This uses the fact that for Froude similarity with same fluid, forces scale as $\lambda^3$.)

---

### Example 6.5.3 — Reynolds Number for Various Flows

**Problem.** Compute Re for: (a) blood flow in an artery ($D = 3$ mm, $U = 0.3$ m/s, $\nu = 3.3 \times 10^{-6}$ m²/s), (b) a Boeing 747 ($L = 60$ m, $U = 250$ m/s, $\nu = 1.5 \times 10^{-5}$ m²/s), (c) a bacterium swimming ($L = 2\;\mu$m, $U = 30\;\mu$m/s, $\nu = 10^{-6}$ m²/s).

**Solution.**

(a) $\text{Re} = \frac{0.3 \times 0.003}{3.3 \times 10^{-6}} = \frac{9 \times 10^{-4}}{3.3 \times 10^{-6}} \approx 273$. Laminar flow.

(b) $\text{Re} = \frac{250 \times 60}{1.5 \times 10^{-5}} = \frac{15000}{1.5 \times 10^{-5}} = 10^9$. Fully turbulent.

(c) $\text{Re} = \frac{30 \times 10^{-6} \times 2 \times 10^{-6}}{10^{-6}} = 6 \times 10^{-5}$. Extreme Stokes flow — inertia is completely irrelevant. The bacterium lives in a world of pure viscosity.

---

### Example 6.5.4 — Dimensional Analysis of Pipe Pressure Drop

**Problem.** The pressure drop $\Delta p$ in a pipe depends on: length $L$, diameter $D$, velocity $U$, density $\rho$, viscosity $\mu$, and roughness height $\epsilon$. Find the dimensionless form.

**Solution.**

**Step 1:** $n = 7$ variables, $k = 3$ dimensions (M, L, T), rank $r = 3$. So $p = 4$ Pi groups.

**Step 2:** Choose repeating variables $D, U, \rho$. The four Pi groups are:

$$
\Pi_1 = \frac{\Delta p}{\rho U^2}, \quad \Pi_2 = \frac{L}{D}, \quad \Pi_3 = \frac{\rho U D}{\mu} = \text{Re}, \quad \Pi_4 = \frac{\epsilon}{D}.
$$

**Step 3:** The relationship is:

$$
\frac{\Delta p}{\rho U^2} = f\left(\frac{L}{D},\; \text{Re},\; \frac{\epsilon}{D}\right).
$$

In practice, this is written as the Darcy-Weisbach equation:

$$
\Delta p = f_D \cdot \frac{L}{D} \cdot \frac{\rho U^2}{2},
$$

where the friction factor $f_D = f_D(\text{Re}, \epsilon/D)$ is given by the Moody chart.

---

### Example 6.5.5 — Complete Non-Dimensionalization of N-S with Multiple Effects

**Problem.** Non-dimensionalize the N-S equations for flow with gravity, surface tension (Weber number), and unsteady effects (Strouhal number). Identify all dimensionless groups.

**Solution.**

**Step 1:** The dimensional N-S equations with gravity and surface tension boundary condition:

$$
\rho\left(\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v}\right) = -\nabla p + \mu \nabla^2 \mathbf{v} + \rho \mathbf{g}.
$$

**Step 2:** Choose scales: $L$ (length), $U$ (velocity), $T_c = L/U$ (convective time), $P_c = \rho U^2$ (pressure).

Define: $\mathbf{x}^* = \mathbf{x}/L$, $t^* = t/(L/U)$, $\mathbf{v}^* = \mathbf{v}/U$, $p^* = p/(\rho U^2)$.

**Step 3:** Substitute and divide by $\rho U^2/L$:

$$
\underbrace{\frac{\partial \mathbf{v}^*}{\partial t^*}}_{\text{St}} + (\mathbf{v}^* \cdot \nabla^*)\mathbf{v}^* = -\nabla^* p^* + \frac{1}{\text{Re}}\nabla^{*2}\mathbf{v}^* + \frac{1}{\text{Fr}^2}\hat{g}^*.
$$

**Step 4:** At a free surface, the surface tension boundary condition introduces:

$$
[p^*] = \frac{1}{\text{We}}\kappa^* L,
$$

where $\text{We} = \rho U^2 L / \sigma$ is the Weber number and $\kappa^*$ is the dimensionless curvature.

**Step 5:** If the problem has an imposed frequency $f$ (e.g., oscillating boundary), define $T_c = 1/f$ instead, giving Strouhal number $\text{St} = fL/U$ as a separate parameter:

$$
\text{St}\frac{\partial \mathbf{v}^*}{\partial t^*} + (\mathbf{v}^* \cdot \nabla^*)\mathbf{v}^* = -\nabla^* p^* + \frac{1}{\text{Re}}\nabla^{*2}\mathbf{v}^* + \frac{1}{\text{Fr}^2}\hat{g}^*.
$$

**Step 6:** Summary of dimensionless groups:

| Number | Definition | Ratio |
|--------|-----------|-------|
| Re | $\rho UL/\mu$ | Inertia / Viscosity |
| Fr | $U/\sqrt{gL}$ | Inertia / Gravity |
| We | $\rho U^2 L/\sigma$ | Inertia / Surface tension |
| St | $fL/U$ | Unsteady / Convective |
| Eu | $\Delta p/(\rho U^2)$ | Pressure / Inertia |
| Ma | $U/c$ | Flow speed / Sound speed |

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- **Prerequisites:** [2.3 - Null Space, Column Space & Rank](2.3---Null-Space,-Column-Space-&-Rank) (rank-nullity theorem for Buckingham Pi), [6.4 - Viscous Fluids - The Navier-Stokes Equations](6.4---Viscous-Fluids---The-Navier-Stokes-Equations) (non-dimensionalization)
- **Applications:** [6.7 - Boundary Layer Theory - Blasius Solution](6.7---Boundary-Layer-Theory---Blasius-Solution) (Re determines boundary layer thickness), [6.8 - Compressible Flow & Shock Waves](6.8---Compressible-Flow-&-Shock-Waves) (Mach number), [6.6 - Vorticity & Potential Flow](6.6---Vorticity-&-Potential-Flow) (high-Re inviscid approximation)
- **Related:** [4.2 - Lagrangian Mechanics & Generalized Coordinates](4.2---Lagrangian-Mechanics-&-Generalized-Coordinates) (scaling symmetries)

### External Resources
- Buckingham, E., "On physically similar systems" (1914), *Physical Review* — the original Pi theorem paper.
- Bridgman, P.W., *Dimensional Analysis*, Yale University Press (1922).
- Barenblatt, G.I., *Scaling, Self-Similarity, and Intermediate Asymptotics*, Cambridge (1996).
- NCFMF Film: *Turbulence* — visual demonstration of Reynolds number effects.



---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — Drag on a Sphere: Scaling with Reynolds Number

**Problem.** The drag force $F_D$ on a smooth sphere of diameter $D$ in a uniform flow of velocity $U$ depends on $\rho$, $\mu$, $D$, and $U$. (a) Use dimensional analysis to show that $C_D = F_D/(\frac{1}{2}\rho U^2 A)$ depends only on Re. (b) Compute the drag force on a sphere of $D = 0.1$ m in water ($\rho = 998$ kg/m³, $\mu = 1.0 \times 10^{-3}$ Pa·s) at $U = 0.5$ m/s, given that $C_D \approx 0.44$ at the corresponding Re.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: List the Variables and Their Dimensions

| Variable | Symbol | Dimensions |
|----------|--------|-----------|
| Drag force | $F_D$ | $[MLT^{-2}]$ |
| Fluid density | $\rho$ | $[ML^{-3}]$ |
| Dynamic viscosity | $\mu$ | $[ML^{-1}T^{-1}]$ |
| Sphere diameter | $D$ | $[L]$ |
| Flow velocity | $U$ | $[LT^{-1}]$ |

Total variables: $n = 5$. Fundamental dimensions: $k = 3$ (M, L, T).

#### Step 2: Apply the Buckingham Pi Theorem

Number of independent dimensionless groups: $n - k = 5 - 3 = 2$.

Choose repeating variables: $\rho$, $U$, $D$ (they span all three dimensions independently).

#### Step 3: Form $\Pi_1$ Containing $F_D$

$$
\Pi_1 = F_D \cdot \rho^a U^b D^c.
$$

Dimensional equation: $[MLT^{-2}][ML^{-3}]^a[LT^{-1}]^b[L]^c = [M^0 L^0 T^0]$.

- M: $1 + a = 0 \implies a = -1$.
- T: $-2 - b = 0 \implies b = -2$.
- L: $1 - 3a + b + c = 0 \implies 1 + 3 - 2 + c = 0 \implies c = -2$.

$$
\Pi_1 = \frac{F_D}{\rho U^2 D^2}.
$$

This is proportional to the drag coefficient: $C_D = F_D / (\frac{1}{2}\rho U^2 \cdot \frac{\pi D^2}{4}) = \frac{8}{\pi}\Pi_1$.

#### Step 4: Form $\Pi_2$ Containing $\mu$

$$
\Pi_2 = \mu \cdot \rho^a U^b D^c.
$$

- M: $1 + a = 0 \implies a = -1$.
- T: $-1 - b = 0 \implies b = -1$.
- L: $-1 - 3a + b + c = 0 \implies -1 + 3 - 1 + c = 0 \implies c = -1$.

$$
\Pi_2 = \frac{\mu}{\rho U D} = \frac{1}{\text{Re}}.
$$

#### Step 5: Functional Relationship

$$
\Pi_1 = f(\Pi_2) \implies C_D = C_D(\text{Re}).
$$

The drag coefficient depends *only* on the Reynolds number — this is the principle of dynamic similarity.

#### Step 6: Numerical Computation

$$
\text{Re} = \frac{\rho U D}{\mu} = \frac{998 \times 0.5 \times 0.1}{1.0 \times 10^{-3}} = 49{,}900 \approx 5 \times 10^4.
$$

At $\text{Re} \approx 5 \times 10^4$, the empirical drag coefficient for a smooth sphere is $C_D \approx 0.44$ (Newton's regime).

$$
F_D = C_D \cdot \frac{1}{2}\rho U^2 \cdot \frac{\pi D^2}{4} = 0.44 \times \frac{1}{2}(998)(0.5)^2 \times \frac{\pi(0.1)^2}{4}.
$$

$$
= 0.44 \times 124.75 \times 7.854 \times 10^{-3} = 0.44 \times 0.9796 = 0.431\;\text{N}.
$$

**Final Answer:**

$$
C_D = C_D(\text{Re})\;\text{only}, \qquad F_D = 0.43\;\text{N at Re} = 5 \times 10^4.
$$

</details>

### Example 8.2 — Buckingham Pi Theorem: Pressure Drop in a Pipe

**Problem.** The pressure drop $\Delta p$ per unit length in a pipe depends on: pipe diameter $D$, fluid density $\rho$, fluid viscosity $\mu$, mean velocity $V$, and pipe roughness height $\epsilon$. Use the Buckingham Pi theorem to derive the functional form of the Darcy-Weisbach equation.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: List Variables and Dimensions

| Variable | Symbol | Dimensions |
|----------|--------|-----------|
| Pressure drop/length | $\Delta p / L$ | $[ML^{-2}T^{-2}]$ |
| Pipe diameter | $D$ | $[L]$ |
| Density | $\rho$ | $[ML^{-3}]$ |
| Viscosity | $\mu$ | $[ML^{-1}T^{-1}]$ |
| Mean velocity | $V$ | $[LT^{-1}]$ |
| Roughness | $\epsilon$ | $[L]$ |

Total: $n = 6$. Fundamental dimensions: $k = 3$. Dimensionless groups: $n - k = 3$.

#### Step 2: Choose Repeating Variables

Choose $\rho$, $V$, $D$ (they are dimensionally independent: $\rho$ provides M, $V$ provides T, $D$ provides L).

#### Step 3: Form $\Pi_1$ with $\Delta p/L$

$$
\Pi_1 = \frac{\Delta p}{L} \cdot \rho^a V^b D^c.
$$

$[ML^{-2}T^{-2}][ML^{-3}]^a[LT^{-1}]^b[L]^c = M^0 L^0 T^0$:

- M: $1 + a = 0 \implies a = -1$.
- T: $-2 - b = 0 \implies b = -2$.
- L: $-2 - 3a + b + c = 0 \implies -2 + 3 - 2 + c = 0 \implies c = 1$.

$$
\Pi_1 = \frac{(\Delta p/L) \cdot D}{\rho V^2}.
$$

#### Step 4: Form $\Pi_2$ with $\mu$

$$
\Pi_2 = \mu \cdot \rho^a V^b D^c = \frac{\mu}{\rho V D} = \frac{1}{\text{Re}}.
$$

(Same as before.)

#### Step 5: Form $\Pi_3$ with $\epsilon$

$$
\Pi_3 = \epsilon \cdot \rho^a V^b D^c.
$$

Since $\epsilon$ has dimensions $[L]$ only: $a = 0$, $b = 0$, $c = -1$.

$$
\Pi_3 = \frac{\epsilon}{D} \quad \text{(relative roughness)}.
$$

#### Step 6: Functional Relationship

$$
\Pi_1 = \Phi(\Pi_2, \Pi_3) \implies \frac{(\Delta p/L) D}{\rho V^2} = \Phi\left(\text{Re},\; \frac{\epsilon}{D}\right).
$$

Rearranging and defining the Darcy friction factor $f = 8\Pi_1$:

$$
\frac{\Delta p}{L} = f \cdot \frac{\rho V^2}{2D}, \qquad f = f\left(\text{Re},\; \frac{\epsilon}{D}\right).
$$

This is the **Darcy-Weisbach equation**. The function $f(\text{Re}, \epsilon/D)$ is given by the Moody chart (Colebrook equation for turbulent flow, $f = 64/\text{Re}$ for laminar flow).

**Final Answer:**

$$
\Delta p = f \frac{L}{D}\frac{\rho V^2}{2}, \qquad f = f\left(\text{Re},\; \frac{\epsilon}{D}\right).
$$

</details>

### Example 8.3 — Froude Number Scaling for Ship Model Testing

**Problem.** A ship model at 1:50 scale is tested in a towing tank. The full-scale ship travels at 15 knots. (a) At what speed should the model be towed to achieve Froude similarity? (b) If the model drag is measured as 2.5 N, what is the full-scale wave drag (assuming Froude scaling applies to the wave-making component)?

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Froude Number Definition

$$
\text{Fr} = \frac{V}{\sqrt{gL}}.
$$

For dynamic similarity of gravity-dominated flows (wave making), the model and prototype must have the same Froude number:

$$
\text{Fr}_m = \text{Fr}_p \implies \frac{V_m}{\sqrt{g L_m}} = \frac{V_p}{\sqrt{g L_p}}.
$$

#### Step 2: Model Speed

The scale ratio is $\lambda = L_p/L_m = 50$. Therefore:

$$
V_m = V_p \sqrt{\frac{L_m}{L_p}} = V_p \cdot \frac{1}{\sqrt{\lambda}} = 15 \times \frac{1}{\sqrt{50}} = \frac{15}{7.071} = 2.12\;\text{knots}.
$$

Convert: $2.12$ knots $= 2.12 \times 0.5144 = 1.09$ m/s.

#### Step 3: Force Scaling

The drag coefficient is:

$$
C_D = \frac{F_D}{\frac{1}{2}\rho V^2 L^2}.
$$

For Froude similarity ($C_D$ same for model and prototype, same fluid):

$$
\frac{F_p}{F_m} = \frac{\rho_p V_p^2 L_p^2}{\rho_m V_m^2 L_m^2}.
$$

With same fluid ($\rho_p = \rho_m$) and $V_p/V_m = \sqrt{\lambda}$:

$$
\frac{F_p}{F_m} = \frac{V_p^2}{V_m^2} \cdot \frac{L_p^2}{L_m^2} = \lambda \cdot \lambda^2 = \lambda^3.
$$

#### Step 4: Full-Scale Wave Drag

$$
F_p = F_m \cdot \lambda^3 = 2.5 \times 50^3 = 2.5 \times 125{,}000 = 312{,}500\;\text{N} = 312.5\;\text{kN}.
$$

#### Step 5: Discussion — The Reynolds Number Problem

At Froude similarity, the model Reynolds number is:

$$
\frac{\text{Re}_m}{\text{Re}_p} = \frac{V_m L_m}{V_p L_p} = \frac{1}{\sqrt{\lambda}} \cdot \frac{1}{\lambda} = \frac{1}{\lambda^{3/2}} = \frac{1}{50^{3/2}} = \frac{1}{354}.
$$

The model Re is 354 times smaller than the prototype Re. This means viscous (frictional) drag does not scale correctly — only the wave-making drag follows Froude scaling. In practice, naval architects separate total drag into wave drag (Froude-scaled) and frictional drag (computed from flat-plate correlations at the correct Re).

**Final Answer:**

$$
V_m = 2.12\;\text{knots}, \qquad F_{p,\text{wave}} = 312.5\;\text{kN}.
$$

</details>

### Example 8.4 — Mach Number Scaling and Compressibility Corrections

**Problem.** An aircraft wing has a lift coefficient $C_L = 0.5$ at low speed (incompressible). Using the Prandtl-Glauert compressibility correction, find the effective $C_L$ at Mach 0.7. At what Mach number does the correction predict $C_L \to \infty$ (critical Mach number concept)?

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Prandtl-Glauert Rule

For thin airfoils in subsonic compressible flow, the pressure coefficient (and hence lift coefficient) is related to the incompressible value by:

$$
C_{L,\text{comp}} = \frac{C_{L,\text{inc}}}{\sqrt{1 - M^2}}.
$$

This correction arises from the linearized compressible potential equation and is valid for $M \lt  M_{\text{cr}}$ (before shocks form).

#### Step 2: Compute $C_L$ at $M = 0.7$

$$
C_L(M=0.7) = \frac{0.5}{\sqrt{1 - 0.49}} = \frac{0.5}{\sqrt{0.51}} = \frac{0.5}{0.714} = 0.700.
$$

The compressibility effect increases the lift coefficient by 40%.

#### Step 3: Critical Mach Number

The Prandtl-Glauert correction diverges when $1 - M^2 \to 0$, i.e., $M \to 1$. However, the *practical* critical Mach number $M_{\text{cr}}$ is defined as the freestream Mach number at which the local flow first reaches $M = 1$ somewhere on the airfoil (typically the suction peak).

Using the pressure coefficient at the minimum-pressure point $C_{p,\min}$ (incompressible), the critical condition is:

$$
C_{p,\min,\text{comp}} = \frac{C_{p,\min,\text{inc}}}{\sqrt{1 - M_{\text{cr}}^2}} = C_{p,\text{sonic}},
$$

where $C_{p,\text{sonic}}$ is the pressure coefficient corresponding to local $M = 1$:

$$
C_{p,\text{sonic}} = \frac{2}{\gamma M_{\text{cr}}^2}\left[\left(\frac{2 + (\gamma-1)M_{\text{cr}}^2}{\gamma+1}\right)^{\gamma/(\gamma-1)} - 1\right].
$$

This transcendental equation must be solved numerically for $M_{\text{cr}}$ given $C_{p,\min,\text{inc}}$.

#### Step 4: Limitations

The Prandtl-Glauert rule breaks down:
- Near $M = 1$ (transonic regime — nonlinear effects dominate).
- For thick airfoils or high angles of attack.
- When shocks are present (the linearization assumption fails).

More accurate rules: Kármán-Tsien (accounts for local Mach number variation), Laitone's rule.

**Final Answer:**

$$
C_L(M=0.7) = 0.700, \qquad \text{Prandtl-Glauert diverges as } M \to 1.
$$

</details>

---

## 📘 9. Appendix: Extended Derivations & Special Cases

### 9.1 The Buckingham Pi Theorem — Proof Outline

**Theorem (Buckingham, 1914).** If a physical law relates $n$ dimensional variables $q_1, q_2, \ldots, q_n$ and these variables involve $k$ independent fundamental dimensions, then the law can be expressed as a relationship among $n - k$ independent dimensionless groups $\Pi_1, \Pi_2, \ldots, \Pi_{n-k}$.

**Proof outline.**

**Step 1: Dimensional homogeneity.** Any valid physical law $f(q_1, \ldots, q_n) = 0$ must be dimensionally homogeneous — it cannot change under a change of units. This is the principle of dimensional homogeneity (Fourier, 1822).

**Step 2: Represent dimensions as a matrix.** Write the dimensional exponents of each variable in terms of the fundamental dimensions $M, L, T, \ldots$ as a matrix $\mathbf{D}$ of size $k \times n$:

$$
D_{ij} = \text{exponent of the } i\text{-th fundamental dimension in variable } q_j.
$$

**Step 3: Rank of the dimensional matrix.** Let $r = \text{rank}(\mathbf{D}) \leq k$. (Usually $r = k$, but not always — e.g., if all variables involve only $L$ and $T$ but not $M$, then $r < k$.)

**Step 4: Null space.** A dimensionless group $\Pi = q_1^{a_1} q_2^{a_2} \cdots q_n^{a_n}$ requires:

$$
\mathbf{D} \mathbf{a} = \mathbf{0}, \qquad \mathbf{a} = (a_1, \ldots, a_n)^T.
$$

The set of all such exponent vectors $\mathbf{a}$ is the null space of $\mathbf{D}$. By the rank-nullity theorem of linear algebra:

$$
\dim(\text{null}(\mathbf{D})) = n - r = n - k \quad (\text{when } r = k).
$$

**Step 5: Basis for the null space.** Any basis $\{\mathbf{a}^{(1)}, \ldots, \mathbf{a}^{(n-k)}\}$ of the null space gives $n - k$ independent dimensionless groups $\Pi_1, \ldots, \Pi_{n-k}$.

**Step 6: Rewrite the physical law.** Since the original law is dimensionally homogeneous, it can be expressed entirely in terms of these dimensionless groups:

$$
f(q_1, \ldots, q_n) = 0 \iff \Phi(\Pi_1, \ldots, \Pi_{n-k}) = 0.
$$

The proof of this last step uses the implicit function theorem and the fact that a dimensionally homogeneous function is invariant under scaling of units. $\blacksquare$

**Key subtleties:**
1. The choice of repeating variables determines *which* $\Pi$-groups you get, but any valid set spans the same space of dimensionless combinations.
2. If $r < k$ (some fundamental dimensions don't appear independently), use $r$ instead of $k$.
3. The theorem tells you the *number* of dimensionless groups and guarantees their existence, but does not tell you the *form* of the function $\Phi$ — that requires experiment or theory.

**Connection to linear algebra:** The Buckingham Pi theorem is, at its core, the rank-nullity theorem applied to the dimensional matrix. This is why [2.3 - Null Space, Column Space & Rank](2.3---Null-Space,-Column-Space-&-Rank) is a prerequisite.

**References:** Buckingham (1914), *Physical Review*; Bridgman, *Dimensional Analysis* (1922); Barenblatt, *Scaling* (1996), Ch. 1.

### 9.2 Complete Similarity vs. Partial Similarity — When Full Scaling is Impossible

In many engineering problems, achieving simultaneous equality of all relevant dimensionless numbers is physically impossible. This is the problem of **incomplete similarity**.

**Example: Ship hydrodynamics.** A ship's drag depends on both Re (viscous effects) and Fr (wave making). For a model at scale $\lambda$:

- Froude similarity requires: $V_m = V_p / \sqrt{\lambda}$.
- Reynolds similarity requires: $V_m = V_p \cdot \lambda$ (if same fluid).

These are contradictory for $\lambda > 1$. You cannot satisfy both simultaneously with the same fluid.

**Resolution: Froude's hypothesis.** Decompose the total drag into:

$$
C_D = C_{D,\text{friction}}(\text{Re}) + C_{D,\text{wave}}(\text{Fr}).
$$

Test the model at Froude similarity (correct wave drag), then correct the frictional drag using flat-plate correlations (ITTC 1957 line) at the correct prototype Re.

**Example: Wind tunnel testing of aircraft.** Full-scale Re for a commercial aircraft is $\sim 10^7$. A 1:10 model in a standard wind tunnel at the same speed has Re reduced by factor 10. Solutions:
- Pressurized wind tunnels (increase $\rho$, hence Re).
- Cryogenic wind tunnels (decrease $\mu$ by cooling the gas).
- Heavy gas tunnels (use SF₆ or R-134a with higher $\rho/\mu$).

**The lesson:** Dimensional analysis identifies *what* must be matched, but engineering judgment determines *how* to handle the inevitable compromises when full similarity is unachievable.

**References:** Newman, *Marine Hydrodynamics* (1977), Ch. 4; Anderson, *Fundamentals of Aerodynamics*, Ch. 1.

---
