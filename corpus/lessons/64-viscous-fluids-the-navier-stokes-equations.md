---
title: "Viscous Fluids The Navier Stokes Equations"
subject: "Fluid Dynamics & Continuum Mechanics"
catalog: advanced
audience_tier: higher-education
chapter: "6.4"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 6.4 — Viscous Fluids: The Navier-Stokes Equations

> *"I am an old man now, and when I die and go to heaven there are two matters on which I hope for enlightenment. One is quantum electrodynamics, and the other is the turbulent motion of fluids. And about the former I am rather optimistic."* — Horace Lamb (attributed), ca. 1932.

The Navier-Stokes equations are the crown jewel of classical fluid mechanics — they describe the motion of every viscous fluid from honey dripping off a spoon to the turbulent wake behind a jumbo jet. Obtained by inserting the Newtonian constitutive law into Cauchy's equation of motion, they form a system of nonlinear partial differential equations whose mathematical properties remain one of the great unsolved problems (a Clay Millennium Prize problem). This chapter derives the equations, solves them exactly for canonical geometries, and establishes the mathematical structure that underlies all of computational fluid dynamics.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Derive the incompressible Navier-Stokes equations from Cauchy's equation + Newtonian constitutive law.
2. Identify and interpret each term: unsteady, convective, pressure gradient, viscous diffusion, body force.
3. Solve the N-S equations exactly for plane Couette flow, plane Poiseuille flow, and pipe Poiseuille flow.
4. Derive the Stokes (creeping flow) equations by dropping the nonlinear convective term.
5. Non-dimensionalize the N-S equations and identify the Reynolds number as the governing parameter.
6. State the boundary conditions (no-slip, no-penetration) and their physical justification.
7. Compute drag forces and flow rates from exact solutions.

---

## 🖼️ Visual Anchor — Parabolic Velocity Profile (Poiseuille Flow)

The classic parabolic velocity profile between two parallel plates: zero velocity at the walls (no-slip), maximum at the centerline, driven by a constant pressure gradient.

![math-06__6.4-fig1](math-06__6.4-fig1.svg)

---

## 📚 1. Definitions

### Definition 6.4.1 — Dynamic Viscosity

The **dynamic viscosity** $\mu$ (units: Pa·s = kg/(m·s)) is the proportionality constant in Newton's law of viscosity relating shear stress to strain rate:

$$
\tau = \mu\, \frac{\partial u}{\partial y}.
$$

For a Newtonian fluid, $\mu$ is independent of the strain rate (but may depend on temperature and pressure).

### Definition 6.4.2 — Kinematic Viscosity

The **kinematic viscosity** $\nu$ is the ratio of dynamic viscosity to density:

$$
\nu = \frac{\mu}{\rho} \quad [\text{m}^2/\text{s}].
$$

It appears naturally when dividing the N-S equations by $\rho$, and represents the diffusivity of momentum (analogous to thermal diffusivity $\alpha$ for heat).

### Definition 6.4.3 — The Laplacian of a Vector Field

The **vector Laplacian** $\nabla^2 \mathbf{v}$ in Cartesian coordinates is:

$$
(\nabla^2 \mathbf{v})_i = \nabla^2 v_i = \frac{\partial^2 v_i}{\partial x_j \partial x_j} = \frac{\partial^2 v_i}{\partial x^2} + \frac{\partial^2 v_i}{\partial y^2} + \frac{\partial^2 v_i}{\partial z^2}.
$$

This is the viscous diffusion operator — it smooths out velocity gradients.

### Definition 6.4.4 — No-Slip Boundary Condition

At a solid wall, the fluid velocity equals the wall velocity:

$$
\mathbf{v}_{\text{fluid}}\big|_{\text{wall}} = \mathbf{v}_{\text{wall}}.
$$

For a stationary wall: $\mathbf{v} = \mathbf{0}$ at the wall. This is an empirical fact confirmed by molecular dynamics — fluid molecules adhere to solid surfaces.

### Definition 6.4.5 — Couette Flow

**Couette flow** is the steady, fully-developed, viscous flow between two infinite parallel plates where one plate moves and the other is stationary (or both move). The flow is driven by the moving boundary, not by a pressure gradient.

### Definition 6.4.6 — Poiseuille Flow

**Poiseuille flow** (or Hagen-Poiseuille flow in a pipe) is the steady, fully-developed, viscous flow driven by a constant pressure gradient between stationary walls. The velocity profile is parabolic.




---

## 📐 2. Axioms / Postulates

### Axiom 6.4.A — Newtonian Fluid Hypothesis

The viscous stress is linearly proportional to the strain rate (Theorem 6.1.3):

$$
\sigma_{ij} = -p\,\delta_{ij} + 2\mu\, S_{ij} + \lambda\, S_{kk}\, \delta_{ij}.
$$

### Axiom 6.4.B — Incompressibility

For the incompressible Navier-Stokes equations, we assume $\nabla \cdot \mathbf{v} = 0$ (constant density along particle paths). This eliminates the bulk viscosity term since $S_{kk} = \nabla \cdot \mathbf{v} = 0$.

### Axiom 6.4.C — No-Slip at Solid Boundaries

Fluid velocity matches wall velocity at all solid surfaces (Definition 6.4.4). This boundary condition, combined with the N-S equations, determines the solution uniquely for well-posed problems.

---

## 🛡️ 3. Lemmas

### Lemma 6.4.1 — Divergence of the Viscous Stress for Incompressible Newtonian Fluid

**Statement.** For an incompressible Newtonian fluid ($\nabla \cdot \mathbf{v} = 0$, $\mu = \text{const}$):

$$
\frac{\partial \tau_{ij}}{\partial x_j} = \mu\, \nabla^2 v_i,
$$

where $\tau_{ij} = 2\mu S_{ij}$ is the deviatoric (viscous) stress.

**Proof.**

**Step 1:** Write the viscous stress explicitly.

$$
\tau_{ij} = 2\mu\, S_{ij} = \mu\left(\frac{\partial v_i}{\partial x_j} + \frac{\partial v_j}{\partial x_i}\right).
$$

**Step 2:** Take the divergence (differentiate with respect to $x_j$).

$$
\frac{\partial \tau_{ij}}{\partial x_j} = \mu\left(\frac{\partial^2 v_i}{\partial x_j \partial x_j} + \frac{\partial^2 v_j}{\partial x_i \partial x_j}\right) = \mu\left(\nabla^2 v_i + \frac{\partial}{\partial x_i}\frac{\partial v_j}{\partial x_j}\right).
$$

**Step 3:** Apply incompressibility: $\frac{\partial v_j}{\partial x_j} = \nabla \cdot \mathbf{v} = 0$.

$$
\frac{\partial \tau_{ij}}{\partial x_j} = \mu\, \nabla^2 v_i + \mu\, \frac{\partial}{\partial x_i}(0) = \mu\, \nabla^2 v_i. \quad \blacksquare
$$

### Lemma 6.4.2 — Uniqueness of Stokes Flow

**Statement.** For the Stokes equations ($\text{Re} \to 0$) in a bounded domain with prescribed boundary velocities, the solution $(\mathbf{v}, p)$ is unique (up to an additive constant in $p$).

**Proof sketch.** Suppose two solutions $(\mathbf{v}_1, p_1)$ and $(\mathbf{v}_2, p_2)$ satisfy the same boundary conditions. Their difference $\mathbf{w} = \mathbf{v}_1 - \mathbf{v}_2$ satisfies $\nabla^2 \mathbf{w} = \nabla q$ (where $q = (p_1 - p_2)/\mu$) with $\mathbf{w} = 0$ on the boundary. Taking the inner product with $\mathbf{w}$ and integrating by parts shows $\int |\nabla \mathbf{w}|^2 dV = 0$, forcing $\mathbf{w} = 0$. $\blacksquare$

---

## 👑 4. Theorems

### Theorem 6.4.1 — The Incompressible Navier-Stokes Equations

For an incompressible Newtonian fluid with constant viscosity:

$$
\rho\left(\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v}\right) = -\nabla p + \mu\, \nabla^2 \mathbf{v} + \rho\, \mathbf{b},
$$

together with the incompressibility constraint:

$$
\nabla \cdot \mathbf{v} = 0.
$$

In index notation:

$$
\rho\left(\frac{\partial v_i}{\partial t} + v_j \frac{\partial v_i}{\partial x_j}\right) = -\frac{\partial p}{\partial x_i} + \mu\, \frac{\partial^2 v_i}{\partial x_j \partial x_j} + \rho\, b_i.
$$

**Term-by-term interpretation:**
- $\rho \frac{\partial v_i}{\partial t}$: local (unsteady) acceleration
- $\rho\, v_j \partial_j v_i$: convective (nonlinear) acceleration
- $-\partial_i p$: pressure gradient force
- $\mu\, \partial_j \partial_j v_i$: viscous diffusion of momentum
- $\rho\, b_i$: body force (gravity, electromagnetic, etc.)

### Theorem 6.4.2 — Plane Couette Flow Solution

For steady flow between two parallel plates at $y = 0$ (stationary) and $y = h$ (moving at speed $U$) with no pressure gradient:

$$
u(y) = U\frac{y}{h}.
$$

The velocity profile is linear. The shear stress is uniform: $\tau = \mu U/h$.

### Theorem 6.4.3 — Plane Poiseuille Flow Solution

For steady flow between two stationary parallel plates at $y = 0$ and $y = h$ driven by pressure gradient $G = -dP/dx > 0$:

$$
u(y) = \frac{G}{2\mu}\, y(h - y).
$$

Maximum velocity at centerline: $u_{\max} = \frac{Gh^2}{8\mu}$. Volume flow rate per unit width: $Q = \frac{Gh^3}{12\mu}$.

### Theorem 6.4.4 — Hagen-Poiseuille Flow (Pipe Flow)

For steady flow in a circular pipe of radius $R$ driven by axial pressure gradient $G = -dP/dz > 0$:

$$
v_z(r) = \frac{G}{4\mu}(R^2 - r^2).
$$

Volume flow rate: $Q = \frac{\pi G R^4}{8\mu}$ (Hagen-Poiseuille law). This is the $R^4$ dependence — doubling the pipe radius increases flow rate by a factor of 16.

---

## ✍️ 5. Proofs / Derivations

### Proof 5.1 — Derivation of the Incompressible Navier-Stokes Equations (Theorem 6.4.1)

**Goal:** From Cauchy's equation + Newtonian constitutive law + incompressibility, derive the N-S equations.

**Step 1: Start from Cauchy's equation of motion (Theorem 6.1.1).**

$$
\rho\, \frac{Dv_i}{Dt} = \frac{\partial \sigma_{ij}}{\partial x_j} + \rho\, b_i.
$$

**Step 2: Substitute the Newtonian constitutive law (Axiom 6.4.A) with incompressibility ($S_{kk} = 0$).**

$$
\sigma_{ij} = -p\, \delta_{ij} + 2\mu\, S_{ij}.
$$

**Step 3: Compute the divergence of the stress tensor.**

$$
\frac{\partial \sigma_{ij}}{\partial x_j} = -\frac{\partial p}{\partial x_i}\underbrace{\frac{\partial \delta_{ij}}{\partial x_j}}_{=0 \text{ (but actually } \partial_j(p\delta_{ij}) = \partial_i p)} + \frac{\partial (2\mu S_{ij})}{\partial x_j}.
$$

More carefully:

$$
\frac{\partial \sigma_{ij}}{\partial x_j} = \frac{\partial}{\partial x_j}(-p\delta_{ij} + 2\mu S_{ij}) = -\frac{\partial p}{\partial x_j}\delta_{ij} + 2\mu\frac{\partial S_{ij}}{\partial x_j} = -\frac{\partial p}{\partial x_i} + 2\mu\frac{\partial S_{ij}}{\partial x_j}.
$$

**Step 4: Apply Lemma 6.4.1.**

$$
2\mu\frac{\partial S_{ij}}{\partial x_j} = \mu\, \nabla^2 v_i.
$$

(Note: $\frac{\partial (2\mu S_{ij})}{\partial x_j} = \mu \frac{\partial}{\partial x_j}\left(\frac{\partial v_i}{\partial x_j} + \frac{\partial v_j}{\partial x_i}\right) = \mu(\nabla^2 v_i + \partial_i(\nabla \cdot \mathbf{v})) = \mu \nabla^2 v_i$.)

**Step 5: Assemble the final equation.**

$$
\rho\, \frac{Dv_i}{Dt} = -\frac{\partial p}{\partial x_i} + \mu\, \nabla^2 v_i + \rho\, b_i.
$$

Expanding the material derivative:

$$
\rho\left(\frac{\partial v_i}{\partial t} + v_j\frac{\partial v_i}{\partial x_j}\right) = -\frac{\partial p}{\partial x_i} + \mu\, \frac{\partial^2 v_i}{\partial x_j \partial x_j} + \rho\, b_i. \quad \blacksquare
$$

### Proof 5.2 — Plane Poiseuille Flow (Theorem 6.4.3)

**Goal:** Solve the N-S equations for steady flow between parallel plates.

**Step 1: State assumptions.**
- Steady: $\partial/\partial t = 0$.
- Fully developed: $\partial u/\partial x = 0$ (velocity does not change along the flow direction).
- 2D: $w = 0$, $\partial/\partial z = 0$.
- No body force in $x$: $b_x = 0$.

**Step 2: Apply continuity ($\nabla \cdot \mathbf{v} = 0$).**

$$
\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} = 0.
$$

Since $\partial u/\partial x = 0$ (fully developed), we get $\partial v/\partial y = 0$. Combined with the no-penetration condition $v = 0$ at the walls, this gives $v = 0$ everywhere.

**Step 3: Simplify the $x$-momentum equation.**

$$
\rho\left(\underbrace{\frac{\partial u}{\partial t}}_{0} + \underbrace{u\frac{\partial u}{\partial x}}_{0} + \underbrace{v\frac{\partial u}{\partial y}}_{0}\right) = -\frac{\partial p}{\partial x} + \mu\left(\underbrace{\frac{\partial^2 u}{\partial x^2}}_{0} + \frac{\partial^2 u}{\partial y^2}\right).
$$

This reduces to:

$$
0 = -\frac{\partial p}{\partial x} + \mu\frac{\partial^2 u}{\partial y^2}.
$$

**Step 4: Simplify the $y$-momentum equation.**

$$
0 = -\frac{\partial p}{\partial y} \quad \implies \quad p = p(x) \text{ only}.
$$

**Step 5: Since $u = u(y)$ only and $p = p(x)$ only, the equation $\mu \frac{d^2 u}{dy^2} = \frac{dp}{dx}$ has left side depending only on $y$ and right side only on $x$. Both must equal a constant.**

Let $\frac{dp}{dx} = -G$ (constant, with $G > 0$ for flow in the $+x$ direction).

$$
\mu\frac{d^2 u}{dy^2} = -G.
$$

**Step 6: Integrate twice.**

First integration:

$$
\mu\frac{du}{dy} = -Gy + C_1.
$$

Second integration:

$$
\mu\, u = -\frac{G}{2}y^2 + C_1 y + C_2.
$$

**Step 7: Apply boundary conditions.**

At $y = 0$: $u(0) = 0 \implies C_2 = 0$.
At $y = h$: $u(h) = 0 \implies -\frac{G}{2}h^2 + C_1 h = 0 \implies C_1 = \frac{Gh}{2}$.

**Step 8: Final solution.**

$$
u(y) = \frac{G}{2\mu}\left(-y^2 + hy\right) = \frac{G}{2\mu}\, y(h - y). \quad \blacksquare
$$

### Proof 5.3 — Hagen-Poiseuille Flow in a Pipe (Theorem 6.4.4)

**Goal:** Solve for axial velocity $v_z(r)$ in a circular pipe.

**Step 1: Use cylindrical coordinates $(r, \theta, z)$. Assumptions: steady, fully developed ($\partial/\partial z = 0$ for velocity), axisymmetric ($\partial/\partial \theta = 0$), $v_r = v_\theta = 0$.**

**Step 2: Continuity gives $\partial v_z/\partial z = 0$ (already assumed).**

**Step 3: The $z$-momentum N-S equation in cylindrical coordinates:**

$$
0 = -\frac{\partial p}{\partial z} + \mu\left(\frac{1}{r}\frac{\partial}{\partial r}\left(r\frac{\partial v_z}{\partial r}\right)\right).
$$

**Step 4: Let $-\frac{\partial p}{\partial z} = G$ (constant). Then:**

$$
\frac{1}{r}\frac{d}{dr}\left(r\frac{dv_z}{dr}\right) = -\frac{G}{\mu}.
$$

**Step 5: Multiply both sides by $r$:**

$$
\frac{d}{dr}\left(r\frac{dv_z}{dr}\right) = -\frac{G}{\mu}\, r.
$$

**Step 6: First integration:**

$$
r\frac{dv_z}{dr} = -\frac{G}{2\mu}\, r^2 + A.
$$

**Step 7: Divide by $r$:**

$$
\frac{dv_z}{dr} = -\frac{G}{2\mu}\, r + \frac{A}{r}.
$$

**Step 8: Regularity at $r = 0$ requires $A = 0$ (otherwise $dv_z/dr \to \infty$ at the centerline).**

$$
\frac{dv_z}{dr} = -\frac{G}{2\mu}\, r.
$$

**Step 9: Second integration:**

$$
v_z = -\frac{G}{4\mu}\, r^2 + B.
$$

**Step 10: No-slip at $r = R$: $v_z(R) = 0 \implies B = \frac{GR^2}{4\mu}$.**

$$
v_z(r) = \frac{G}{4\mu}(R^2 - r^2). \quad \blacksquare
$$

**Step 11: Volume flow rate.**

$$
Q = \int_0^R \int_0^{2\pi} v_z(r)\, r\, d\theta\, dr = 2\pi \int_0^R \frac{G}{4\mu}(R^2 - r^2)\, r\, dr.
$$

$$
= \frac{\pi G}{2\mu}\int_0^R (R^2 r - r^3)\, dr = \frac{\pi G}{2\mu}\left[\frac{R^2 r^2}{2} - \frac{r^4}{4}\right]_0^R = \frac{\pi G}{2\mu}\left(\frac{R^4}{2} - \frac{R^4}{4}\right) = \frac{\pi G R^4}{8\mu}.
$$




---

## 🧮 6. Worked Examples

### Example 6.4.1 — Couette Flow with Pressure Gradient (Combined Couette-Poiseuille)

**Problem.** Fluid flows between two parallel plates at $y = 0$ (stationary) and $y = h$ (moving at speed $U$). A pressure gradient $G = -dp/dx$ is also applied. Find $u(y)$.

**Solution.**

**Step 1:** The governing equation is the same as Poiseuille:

$$
\mu\frac{d^2 u}{dy^2} = -G.
$$

**Step 2:** General solution: $u(y) = -\frac{G}{2\mu}y^2 + C_1 y + C_2$.

**Step 3:** Boundary conditions:
- $u(0) = 0 \implies C_2 = 0$.
- $u(h) = U \implies -\frac{G}{2\mu}h^2 + C_1 h = U \implies C_1 = \frac{U}{h} + \frac{Gh}{2\mu}$.

**Step 4:** Final solution:

$$
u(y) = \frac{U y}{h} + \frac{G}{2\mu}\, y(h - y).
$$

The first term is the Couette (linear) contribution; the second is the Poiseuille (parabolic) contribution. The two effects superpose linearly because the N-S equations are linear for this geometry.

---

### Example 6.4.2 — Wall Shear Stress and Drag in Pipe Flow

**Problem.** Oil ($\mu = 0.5$ Pa·s, $\rho = 900$ kg/m³) flows through a pipe of radius $R = 0.05$ m and length $L = 10$ m with pressure drop $\Delta p = 200$ kPa. Find: (a) centerline velocity, (b) volume flow rate, (c) wall shear stress, (d) Reynolds number.

**Solution.**

**Step 1:** Pressure gradient: $G = \Delta p / L = 200{,}000 / 10 = 20{,}000$ Pa/m.

**Step 2:** (a) Centerline velocity ($r = 0$):

$$
v_{\max} = \frac{GR^2}{4\mu} = \frac{20000 \times 0.05^2}{4 \times 0.5} = \frac{20000 \times 0.0025}{2} = \frac{50}{2} = 25 \;\text{m/s}.
$$

**Step 3:** (b) Volume flow rate:

$$
Q = \frac{\pi G R^4}{8\mu} = \frac{\pi \times 20000 \times (0.05)^4}{8 \times 0.5} = \frac{\pi \times 20000 \times 6.25 \times 10^{-6}}{4} = \frac{0.3927}{4} \approx 0.0982 \;\text{m}^3/\text{s}.
$$

Wait — let us recompute: $(0.05)^4 = 6.25 \times 10^{-6}$.

$$
Q = \frac{\pi \times 20000 \times 6.25 \times 10^{-6}}{4} = \frac{\pi \times 0.125}{4} = \frac{0.3927}{4} = 0.0982 \;\text{m}^3/\text{s}.
$$

**Step 4:** (c) Wall shear stress:

$$
\tau_w = \mu\left|\frac{dv_z}{dr}\right|_{r=R} = \mu \cdot \frac{GR}{2\mu} = \frac{GR}{2} = \frac{20000 \times 0.05}{2} = 500 \;\text{Pa}.
$$

**Step 5:** (d) Reynolds number. Mean velocity: $\bar{v} = v_{\max}/2 = 12.5$ m/s.

$$
\text{Re} = \frac{\rho \bar{v} D}{\mu} = \frac{900 \times 12.5 \times 0.1}{0.5} = \frac{1125}{0.5} = 2250.
$$

Since Re $\approx 2250$, this is near the laminar-turbulent transition (Re $\approx 2300$ for pipe flow). The Poiseuille solution is marginally valid.

---

### Example 6.4.3 — Stokes' First Problem (Suddenly Accelerated Plate)

**Problem.** An infinite flat plate at $y = 0$ is suddenly set in motion at $t = 0$ with velocity $U$ in the $x$-direction. The fluid above ($y > 0$) is initially at rest. Find $u(y, t)$.

**Solution.**

**Step 1:** The N-S equation reduces to the diffusion equation (no pressure gradient, no convection for this 1D unsteady problem):

$$
\frac{\partial u}{\partial t} = \nu\frac{\partial^2 u}{\partial y^2}.
$$

**Step 2:** Boundary and initial conditions:
- $u(0, t) = U$ for $t > 0$ (plate velocity).
- $u(y, 0) = 0$ for $y > 0$ (fluid initially at rest).
- $u(\infty, t) = 0$ (far-field undisturbed).

**Step 3:** Seek a similarity solution. Define $\eta = \frac{y}{2\sqrt{\nu t}}$ (the diffusion similarity variable).

Let $u = U\, f(\eta)$. Then:

$$
\frac{\partial u}{\partial t} = U f'(\eta)\frac{\partial \eta}{\partial t} = U f'(\eta)\left(-\frac{y}{4\sqrt{\nu}\, t^{3/2}}\right) = -U f'(\eta)\frac{\eta}{2t}.
$$

$$
\frac{\partial^2 u}{\partial y^2} = U f''(\eta)\left(\frac{1}{2\sqrt{\nu t}}\right)^2 = \frac{U f''(\eta)}{4\nu t}.
$$

**Step 4:** Substitute into the PDE:

$$
-U f' \frac{\eta}{2t} = \nu \cdot \frac{U f''}{4\nu t} = \frac{U f''}{4t}.
$$

Multiply by $4t/U$:

$$
-2\eta f' = f'' \quad \implies \quad f'' + 2\eta f' = 0.
$$

**Step 5:** Solve the ODE. Let $g = f'$: $g' + 2\eta g = 0 \implies g = A e^{-\eta^2}$.

$$
f(\eta) = A\int_0^\eta e^{-s^2}\, ds + B.
$$

**Step 6:** Apply boundary conditions.
- $f(0) = 1$ (plate): $B = 1$.
- $f(\infty) = 0$: $A \cdot \frac{\sqrt{\pi}}{2} + 1 = 0 \implies A = -\frac{2}{\sqrt{\pi}}$.

**Step 7:** Final solution:

$$
u(y, t) = U\left[1 - \text{erf}\left(\frac{y}{2\sqrt{\nu t}}\right)\right] = U\, \text{erfc}\left(\frac{y}{2\sqrt{\nu t}}\right).
$$

The momentum diffuses into the fluid with a penetration depth $\delta \sim \sqrt{\nu t}$ — the same scaling as heat diffusion.

---

### Example 6.4.4 — Non-Dimensionalization of the N-S Equations

**Problem.** Non-dimensionalize the incompressible N-S equations using characteristic length $L$, velocity $U$, and show the Reynolds number emerges.

**Solution.**

**Step 1:** Define dimensionless variables:

$$
\mathbf{x}^* = \frac{\mathbf{x}}{L}, \quad \mathbf{v}^* = \frac{\mathbf{v}}{U}, \quad t^* = \frac{tU}{L}, \quad p^* = \frac{p}{\rho U^2}.
$$

**Step 2:** Express derivatives in terms of dimensionless variables:

$$
\frac{\partial}{\partial x_i} = \frac{1}{L}\frac{\partial}{\partial x_i^*}, \quad \frac{\partial}{\partial t} = \frac{U}{L}\frac{\partial}{\partial t^*}.
$$

**Step 3:** Substitute into the N-S equations. The $i$-th component:

$$
\rho\left(\frac{U^2}{L}\frac{\partial v_i^*}{\partial t^*} + \frac{U^2}{L} v_j^* \frac{\partial v_i^*}{\partial x_j^*}\right) = -\frac{\rho U^2}{L}\frac{\partial p^*}{\partial x_i^*} + \mu\frac{U}{L^2}\frac{\partial^2 v_i^*}{\partial x_j^* \partial x_j^*}.
$$

**Step 4:** Divide through by $\rho U^2 / L$:

$$
\frac{\partial v_i^*}{\partial t^*} + v_j^* \frac{\partial v_i^*}{\partial x_j^*} = -\frac{\partial p^*}{\partial x_i^*} + \frac{\mu}{\rho U L}\frac{\partial^2 v_i^*}{\partial x_j^* \partial x_j^*}.
$$

**Step 5:** Identify the Reynolds number:

$$
\text{Re} = \frac{\rho U L}{\mu} = \frac{UL}{\nu}.
$$

The dimensionless N-S equations are:

$$
\frac{\partial \mathbf{v}^*}{\partial t^*} + (\mathbf{v}^* \cdot \nabla^*)\mathbf{v}^* = -\nabla^* p^* + \frac{1}{\text{Re}}\, \nabla^{*2} \mathbf{v}^*.
$$

The Reynolds number is the *only* parameter — geometrically similar flows at the same Re are dynamically identical.

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- **Prerequisites:** [6.1 - Stress & Strain Tensors in Continua](6.1---Stress-&-Strain-Tensors-in-Continua) (Newtonian constitutive law), [6.2 - Mass Conservation - The Continuity Equation](6.2---Mass-Conservation---The-Continuity-Equation) (incompressibility), [6.3 - Inviscid Fluids - Euler's Equation](6.3---Inviscid-Fluids---Euler's-Equation) (inviscid limit)
- **Next:** [6.5 - Dimensionless Numbers - Reynolds & Froude](6.5---Dimensionless-Numbers---Reynolds-&-Froude) (systematic dimensional analysis), [6.7 - Boundary Layer Theory - Blasius Solution](6.7---Boundary-Layer-Theory---Blasius-Solution) (viscous effects near walls)
- **Mathematical tools:** [3.2 - Second-Order Linear ODEs](3.2---Second-Order-Linear-ODEs) (Poiseuille ODE), [3.4 - The Heat & Diffusion Equation](3.4---The-Heat-&-Diffusion-Equation) (Stokes' first problem is a diffusion equation)

### External Resources
- Navier, C.L.M.H., "Mémoire sur les lois du mouvement des fluides" (1822) — the original derivation.
- Stokes, G.G., "On the theories of the internal friction of fluids in motion" (1845).
- Batchelor, *An Introduction to Fluid Dynamics*, Ch. 4 — Flow of a Uniform Incompressible Viscous Fluid.
- Clay Mathematics Institute — Navier-Stokes Millennium Prize Problem statement.
- NCFMF Film: *Low Reynolds Number Flows* — beautiful demonstrations of Stokes flow reversibility.




---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — Couette Flow: Linear Velocity Profile Derivation

**Problem.** Two infinite parallel plates are separated by a gap $h$. The bottom plate is stationary and the top plate moves at velocity $U$ in the $x$-direction. The fluid between them has viscosity $\mu$ and density $\rho$. There is no applied pressure gradient. Derive the velocity profile, shear stress, and volumetric flow rate per unit width.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Simplifying Assumptions

- Steady flow: $\partial/\partial t = 0$.
- Fully developed: $\partial/\partial x = 0$ (no streamwise variation).
- Two-dimensional: $\partial/\partial z = 0$, $w = 0$.
- Incompressible: $\nabla \cdot \mathbf{v} = 0$.
- No pressure gradient: $\partial p/\partial x = 0$.

#### Step 2: Continuity Equation

$$
\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} = 0.
$$

Since $\partial u/\partial x = 0$ (fully developed), we get $\partial v/\partial y = 0$. Combined with the boundary condition $v = 0$ at both walls, this gives $v = 0$ everywhere.

#### Step 3: $x$-Momentum (Navier-Stokes)

$$
\rho\left(\frac{\partial u}{\partial t} + u\frac{\partial u}{\partial x} + v\frac{\partial u}{\partial y}\right) = -\frac{\partial p}{\partial x} + \mu\left(\frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2}\right).
$$

Apply all simplifications ($\partial/\partial t = 0$, $\partial u/\partial x = 0$, $v = 0$, $\partial p/\partial x = 0$, $\partial^2 u/\partial x^2 = 0$):

$$
0 = \mu \frac{\partial^2 u}{\partial y^2}.
$$

#### Step 4: Solve the ODE

$$
\frac{d^2 u}{dy^2} = 0 \implies \frac{du}{dy} = C_1 \implies u(y) = C_1 y + C_2.
$$

#### Step 5: Apply Boundary Conditions

- At $y = 0$ (bottom plate, stationary): $u(0) = 0 \implies C_2 = 0$.
- At $y = h$ (top plate, moving): $u(h) = U \implies C_1 h = U \implies C_1 = U/h$.

#### Step 6: Final Velocity Profile

$$
u(y) = U\frac{y}{h}.
$$

This is a linear profile — the simplest possible viscous flow.

#### Step 7: Shear Stress

$$
\tau_{xy} = \mu \frac{du}{dy} = \mu \frac{U}{h} = \text{const}.
$$

The shear stress is uniform throughout the fluid — there is no net viscous force on any fluid element (consistent with zero pressure gradient and zero acceleration).

#### Step 8: Volumetric Flow Rate per Unit Width

$$
q = \int_0^h u(y)\, dy = \int_0^h \frac{Uy}{h}\, dy = \frac{U}{h}\left[\frac{y^2}{2}\right]_0^h = \frac{Uh}{2}.
$$

#### Step 9: Force on the Plates

The force per unit area on the top plate (exerted by the fluid) is $\tau_w = \mu U/h$ in the $-x$ direction (resisting the motion). The force on the bottom plate is $\mu U/h$ in the $+x$ direction. The power required to drive the top plate is $P = \tau_w \cdot U = \mu U^2/h$ per unit area.

**Final Answer:**

$$
u(y) = \frac{Uy}{h}, \qquad \tau = \frac{\mu U}{h}, \qquad q = \frac{Uh}{2}.
$$

</details>

### Example 8.2 — Poiseuille Flow: Parabolic Profile and Flow Rate

**Problem.** Incompressible fluid flows through a circular pipe of radius $R$ under a constant pressure gradient $G = -dp/dz > 0$. Derive the velocity profile $v_z(r)$, the maximum velocity, the volumetric flow rate $Q$, and the wall shear stress.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Governing Equation in Cylindrical Coordinates

For steady, fully developed, axisymmetric flow ($v_r = v_\theta = 0$, $\partial/\partial z = 0$ for velocity, $\partial/\partial\theta = 0$):

The $z$-momentum N-S equation in cylindrical coordinates reduces to:

$$
0 = -\frac{\partial p}{\partial z} + \mu\left(\frac{1}{r}\frac{\partial}{\partial r}\left(r\frac{\partial v_z}{\partial r}\right)\right).
$$

With $-\partial p/\partial z = G$ (constant):

$$
\frac{1}{r}\frac{d}{dr}\left(r\frac{dv_z}{dr}\right) = -\frac{G}{\mu}.
$$

#### Step 2: First Integration

Multiply both sides by $r$:

$$
\frac{d}{dr}\left(r\frac{dv_z}{dr}\right) = -\frac{G}{\mu}\, r.
$$

Integrate with respect to $r$:

$$
r\frac{dv_z}{dr} = -\frac{G}{2\mu}\, r^2 + C_1.
$$

#### Step 3: Apply Regularity at $r = 0$

At the centerline $r = 0$, the velocity must be finite and the shear stress $\tau_{rz} = \mu\, dv_z/dr$ must be zero (by symmetry). From the equation above, as $r \to 0$: the left side $\to 0$, so $C_1 = 0$.

$$
\frac{dv_z}{dr} = -\frac{G}{2\mu}\, r.
$$

#### Step 4: Second Integration

$$
v_z(r) = -\frac{G}{4\mu}\, r^2 + C_2.
$$

#### Step 5: Apply No-Slip at $r = R$

$$
v_z(R) = 0 \implies C_2 = \frac{G R^2}{4\mu}.
$$

#### Step 6: Final Velocity Profile

$$
v_z(r) = \frac{G}{4\mu}(R^2 - r^2) = v_{\max}\left(1 - \frac{r^2}{R^2}\right),
$$

where $v_{\max} = GR^2/(4\mu)$ is the centerline velocity.

#### Step 7: Volumetric Flow Rate

$$
Q = \int_0^R v_z(r) \cdot 2\pi r\, dr = 2\pi \int_0^R \frac{G}{4\mu}(R^2 - r^2)\, r\, dr.
$$

$$
= \frac{\pi G}{2\mu}\int_0^R (R^2 r - r^3)\, dr = \frac{\pi G}{2\mu}\left[\frac{R^2 r^2}{2} - \frac{r^4}{4}\right]_0^R = \frac{\pi G}{2\mu}\left(\frac{R^4}{2} - \frac{R^4}{4}\right) = \frac{\pi G R^4}{8\mu}.
$$

This is the **Hagen-Poiseuille law**:

$$
Q = \frac{\pi R^4}{8\mu}\left(-\frac{dp}{dz}\right) = \frac{\pi R^4 \Delta p}{8\mu L}.
$$

#### Step 8: Mean Velocity and Relation to Maximum

$$
\bar{v} = \frac{Q}{\pi R^2} = \frac{G R^2}{8\mu} = \frac{v_{\max}}{2}.
$$

The mean velocity is exactly half the centerline velocity for Poiseuille flow.

#### Step 9: Wall Shear Stress

$$
\tau_w = \mu\left|\frac{dv_z}{dr}\right|_{r=R} = \mu \cdot \frac{G R}{2\mu} = \frac{GR}{2} = \frac{R\,\Delta p}{2L}.
$$

**Final Answer:**

$$
v_z(r) = \frac{GR^2}{4\mu}\left(1 - \frac{r^2}{R^2}\right), \quad Q = \frac{\pi G R^4}{8\mu}, \quad \tau_w = \frac{GR}{2}.
$$

</details>

### Example 8.3 — Combined Couette-Poiseuille Flow

**Problem.** Between two parallel plates separated by distance $h$, the top plate moves at speed $U$ and there is also an applied pressure gradient $G = -dp/dx > 0$. Derive the general velocity profile and find the condition for backflow near the stationary plate.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Governing Equation

Same simplifications as Couette flow, but now $\partial p/\partial x = -G \neq 0$:

$$
\mu \frac{d^2 u}{dy^2} = \frac{\partial p}{\partial x} = -G.
$$

#### Step 2: General Solution

$$
\frac{d^2 u}{dy^2} = -\frac{G}{\mu} \implies u(y) = -\frac{G}{2\mu}y^2 + C_1 y + C_2.
$$

#### Step 3: Boundary Conditions

- $u(0) = 0$: $C_2 = 0$.
- $u(h) = U$: $-\frac{G}{2\mu}h^2 + C_1 h = U \implies C_1 = \frac{U}{h} + \frac{Gh}{2\mu}$.

#### Step 4: Final Profile

$$
u(y) = \frac{Uy}{h} + \frac{G}{2\mu}y(h - y).
$$

The first term is the Couette (linear) contribution; the second is the Poiseuille (parabolic) contribution. Define the dimensionless pressure gradient parameter:

$$
P = -\frac{Gh^2}{2\mu U}.
$$

Then in dimensionless form ($\eta = y/h$, $u^* = u/U$):

$$
u^* = \eta - P\,\eta(1 - \eta) = \eta(1 + P) - P\eta^2.
$$

Wait — let me be careful with signs. With $G = -dp/dx \gt  0$ (favorable pressure gradient):

$$
u(y) = \frac{Uy}{h} + \frac{G}{2\mu}y(h-y).
$$

Define $P = Gh^2/(2\mu U)$ (positive for favorable gradient). Then:

$$
u^* = \eta + P\,\eta(1-\eta) = \eta(1 + P - P\eta).
$$

#### Step 5: Condition for Backflow

Backflow occurs when $u \lt  0$ somewhere. Check the velocity gradient at $y = 0$:

$$
\frac{du}{dy}\bigg|_{y=0} = \frac{U}{h} + \frac{Gh}{2\mu} - \frac{G \cdot 0}{\mu} = \frac{U}{h} + \frac{Gh}{2\mu}.
$$

For an *adverse* pressure gradient ($G \lt  0$, i.e., $dp/dx \gt  0$), define $|G| = -G$:

$$
u(y) = \frac{Uy}{h} - \frac{|G|}{2\mu}y(h-y).
$$

The slope at $y = 0$ is:

$$
\frac{du}{dy}\bigg|_0 = \frac{U}{h} - \frac{|G|h}{2\mu}.
$$

Backflow occurs when this slope is negative:

$$
\frac{U}{h} \lt  \frac{|G|h}{2\mu} \implies |G| \gt  \frac{2\mu U}{h^2}.
$$

In terms of the dimensionless parameter $P_{\text{adv}} = |G|h^2/(2\mu U)$: backflow occurs when $P_{\text{adv}} \gt  1$.

**Final Answer:**

$$
u(y) = \frac{Uy}{h} + \frac{G}{2\mu}y(h-y), \qquad \text{Backflow when } \frac{|G|h^2}{2\mu U} \gt  1.
$$

</details>

---

## 📘 9. Appendix: Extended Derivations & Special Cases

### 9.1 Dimensional Analysis of the Navier-Stokes Equations — The Non-Dimensional Form

The incompressible Navier-Stokes equations contain dimensional quantities ($\rho$, $\mu$, characteristic length $L$, velocity $U$). Non-dimensionalization reveals that the *only* governing parameter for geometrically similar flows is the Reynolds number.

**Step 1: Define dimensionless variables.**

$$
\mathbf{x}^* = \frac{\mathbf{x}}{L}, \quad t^* = \frac{tU}{L}, \quad \mathbf{v}^* = \frac{\mathbf{v}}{U}, \quad p^* = \frac{p - p_\infty}{\rho U^2}.
$$

**Step 2: Transform derivatives.**

$$
\frac{\partial}{\partial x_i} = \frac{1}{L}\frac{\partial}{\partial x_i^*}, \qquad \frac{\partial}{\partial t} = \frac{U}{L}\frac{\partial}{\partial t^*}.
$$

**Step 3: Substitute into the dimensional N-S equations.**

The dimensional form:

$$
\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v} = -\frac{1}{\rho}\nabla p + \nu \nabla^2 \mathbf{v}.
$$

Substituting $\mathbf{v} = U\mathbf{v}^*$, $\nabla = (1/L)\nabla^*$, $\partial/\partial t = (U/L)\partial/\partial t^*$, $p = \rho U^2 p^* + p_\infty$:

$$
\frac{U^2}{L}\frac{\partial \mathbf{v}^*}{\partial t^*} + \frac{U^2}{L}(\mathbf{v}^* \cdot \nabla^*)\mathbf{v}^* = -\frac{U^2}{L}\nabla^* p^* + \frac{\nu U}{L^2}\nabla^{*2}\mathbf{v}^*.
$$

**Step 4: Divide by $U^2/L$.**

$$
\frac{\partial \mathbf{v}^*}{\partial t^*} + (\mathbf{v}^* \cdot \nabla^*)\mathbf{v}^* = -\nabla^* p^* + \frac{\nu}{UL}\nabla^{*2}\mathbf{v}^*.
$$

**Step 5: Identify the Reynolds number.**

$$
\text{Re} = \frac{UL}{\nu} \implies \frac{\nu}{UL} = \frac{1}{\text{Re}}.
$$

The non-dimensional Navier-Stokes equations are:

$$
\frac{\partial \mathbf{v}^*}{\partial t^*} + (\mathbf{v}^* \cdot \nabla^*)\mathbf{v}^* = -\nabla^* p^* + \frac{1}{\text{Re}}\nabla^{*2}\mathbf{v}^*.
$$

**Physical consequences:**
- Two flows with the same geometry and the same Re are dynamically similar — they have identical dimensionless velocity and pressure fields.
- At $\text{Re} \to \infty$: the viscous term vanishes → Euler's equation (inviscid limit).
- At $\text{Re} \to 0$: the inertial terms are negligible → Stokes (creeping) flow.
- The transition from laminar to turbulent flow occurs at a critical Re that depends only on geometry.

**References:** Batchelor, §6.2; Kundu & Cohen, §4.11; Landau & Lifshitz, §19.

---
