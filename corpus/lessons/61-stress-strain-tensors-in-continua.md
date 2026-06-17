---
title: "Stress Strain Tensors In Continua"
subject: "Fluid Dynamics & Continuum Mechanics"
catalog: advanced
audience_tier: higher-education
chapter: "6.1"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 6.1 — Stress & Strain Tensors in Continua

> *"The internal forces in a continuous medium are not described by a single vector but by a tensor — a mathematical object that encodes how force is transmitted across every possible surface through every point."* — Augustin-Louis Cauchy, *Exercices de Mathématiques* (1828).

The foundation of all continuum mechanics — whether solid elasticity, viscous fluid flow, or plasma dynamics — rests on two second-order tensor fields: the **stress tensor** $\sigma_{ij}$ and the **strain tensor** $\varepsilon_{ij}$. The stress tensor tells us the force per unit area acting on any internal surface; the strain tensor tells us how the material deforms. Together they form the constitutive bridge between applied loads and material response. This chapter constructs both tensors from first principles, proves Cauchy's fundamental theorem, and derives the strain-rate tensor that will power the Navier-Stokes equations in Chapter 6.4.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Define the traction vector $\mathbf{t}^{(\hat{n})}$ on an arbitrary internal surface and explain its dependence on the surface normal $\hat{n}$.
2. Construct the Cauchy stress tensor $\sigma_{ij}$ and prove that traction is linear in the normal: $t_i = \sigma_{ij} n_j$.
3. Prove the symmetry of the stress tensor ($\sigma_{ij} = \sigma_{ji}$) from conservation of angular momentum.
4. Decompose the stress tensor into hydrostatic (pressure) and deviatoric components.
5. Define the infinitesimal strain tensor $\varepsilon_{ij}$ from the displacement gradient.
6. Decompose the velocity gradient tensor into the symmetric strain-rate tensor $S_{ij}$ and the antisymmetric vorticity tensor $\Omega_{ij}$.
7. Compute principal stresses and principal directions via eigenvalue problems.
8. State and apply the generalized Hooke's law for linear elastic isotropic materials.

---

## 🖼️ Visual Anchor — Cauchy Stress Tetrahedron

The Cauchy tetrahedron argument: an infinitesimal tetrahedron with three faces aligned to coordinate planes and one oblique face with normal $\hat{n}$. Force balance on this element proves that the traction vector on any surface is a linear function of the normal.

![math-06__6.1-fig1](math-06__6.1-fig1.svg)

---

## 📚 1. Definitions

### Definition 6.1.1 — Body and Configuration

A **body** $\mathcal{B}$ is a collection of material particles. A **configuration** is a smooth, injective mapping $\boldsymbol{\chi}: \mathcal{B} \to \mathbb{R}^3$ that assigns to each particle $X \in \mathcal{B}$ a position $\mathbf{x} = \boldsymbol{\chi}(X, t)$ in physical space at time $t$.

The **reference configuration** $\boldsymbol{\chi}_0$ maps particles to their positions at $t = 0$: $\mathbf{X} = \boldsymbol{\chi}_0(X)$. The **current configuration** gives positions at time $t$: $\mathbf{x} = \boldsymbol{\chi}(X, t)$.

### Definition 6.1.2 — Displacement Field

The **displacement field** $\mathbf{u}$ measures how far each material point has moved from its reference position:

$$
\mathbf{u}(\mathbf{X}, t) = \mathbf{x}(\mathbf{X}, t) - \mathbf{X}.
$$

In component form: $u_i = x_i - X_i$.

### Definition 6.1.3 — Deformation Gradient Tensor

The **deformation gradient** $\mathbf{F}$ is the Jacobian of the current configuration with respect to the reference configuration:

$$
F_{iJ} = \frac{\partial x_i}{\partial X_J}.
$$

This is a two-point tensor (lowercase index in current configuration, uppercase in reference). It maps infinitesimal material line elements from reference to current: $d\mathbf{x} = \mathbf{F}\,d\mathbf{X}$.

The determinant $J = \det \mathbf{F} > 0$ measures local volume change: $dV = J\,dV_0$.

### Definition 6.1.4 — Traction Vector (Stress Vector)

Consider an internal surface $\mathcal{S}$ within the body with outward unit normal $\hat{n}$ at a point $\mathbf{x}$. The **traction vector** $\mathbf{t}^{(\hat{n})}(\mathbf{x})$ is defined as the force per unit area exerted by the material on the positive side of $\mathcal{S}$ upon the material on the negative side:

$$
\mathbf{t}^{(\hat{n})}(\mathbf{x}) = \lim_{\Delta A \to 0} \frac{\Delta \mathbf{F}}{\Delta A},
$$

where $\Delta \mathbf{F}$ is the resultant contact force on the surface element $\Delta A$ centered at $\mathbf{x}$.

**Critical observation:** The traction depends not only on position $\mathbf{x}$ but also on the orientation $\hat{n}$ of the surface — there are infinitely many possible tractions at a single point, one for each direction $\hat{n}$.

### Definition 6.1.5 — Cauchy Stress Tensor

The **Cauchy stress tensor** $\boldsymbol{\sigma}$ is the second-order tensor field that maps the unit normal $\hat{n}$ of any internal surface to the traction vector on that surface:

$$
t_i^{(\hat{n})} = \sigma_{ij}\, n_j.
$$

In matrix notation: $\mathbf{t}^{(\hat{n})} = \boldsymbol{\sigma} \cdot \hat{n}$.

The component $\sigma_{ij}$ represents the force per unit area in the $i$-direction acting on a surface whose outward normal points in the $j$-direction. The nine components organize as:

$$
\boldsymbol{\sigma} = \begin{pmatrix} \sigma_{11} & \sigma_{12} & \sigma_{13} \\ \sigma_{21} & \sigma_{22} & \sigma_{23} \\ \sigma_{31} & \sigma_{32} & \sigma_{33} \end{pmatrix}.
$$

Diagonal components ($\sigma_{11}, \sigma_{22}, \sigma_{33}$) are **normal stresses**. Off-diagonal components ($\sigma_{12}, \sigma_{13}$, etc.) are **shear stresses**.

### Definition 6.1.6 — Infinitesimal Strain Tensor

For small deformations ($|\nabla \mathbf{u}| \ll 1$), the **infinitesimal strain tensor** is the symmetric part of the displacement gradient:

$$
\varepsilon_{ij} = \frac{1}{2}\left(\frac{\partial u_i}{\partial x_j} + \frac{\partial u_j}{\partial x_i}\right).
$$

This linearization neglects the quadratic term $\frac{1}{2}\frac{\partial u_k}{\partial x_i}\frac{\partial u_k}{\partial x_j}$ present in the full Green-Lagrange strain tensor.

**Physical meaning of components:**
- Diagonal: $\varepsilon_{11}$ = fractional elongation in the $x_1$-direction.
- Off-diagonal: $2\varepsilon_{12}$ = decrease in the angle between material lines initially along $x_1$ and $x_2$ (engineering shear strain $\gamma_{12}$).

### Definition 6.1.7 — Velocity Gradient Tensor

In fluid mechanics, we work with the **velocity gradient tensor** $L_{ij}$:

$$
L_{ij} = \frac{\partial v_i}{\partial x_j},
$$

where $\mathbf{v}(\mathbf{x}, t)$ is the Eulerian velocity field.

### Definition 6.1.8 — Strain-Rate Tensor and Vorticity Tensor

The velocity gradient decomposes uniquely into symmetric and antisymmetric parts:

$$
L_{ij} = S_{ij} + \Omega_{ij},
$$

where the **strain-rate tensor** (rate of deformation tensor) is:

$$
S_{ij} = \frac{1}{2}\left(\frac{\partial v_i}{\partial x_j} + \frac{\partial v_j}{\partial x_i}\right) = \frac{1}{2}(L_{ij} + L_{ji}),
$$

and the **vorticity tensor** (spin tensor) is:

$$
\Omega_{ij} = \frac{1}{2}\left(\frac{\partial v_i}{\partial x_j} - \frac{\partial v_j}{\partial x_i}\right) = \frac{1}{2}(L_{ij} - L_{ji}).
$$

The vorticity tensor is related to the vorticity vector $\boldsymbol{\omega} = \nabla \times \mathbf{v}$ by $\Omega_{ij} = -\frac{1}{2}\epsilon_{ijk}\omega_k$, where $\epsilon_{ijk}$ is the Levi-Civita symbol (see [1.6 - Vector Fields, Div & Curl](1.6---Vector-Fields,-Div-&-Curl) and [2.4 - Eigenvalues & Eigenvectors](2.4---Eigenvalues-&-Eigenvectors)).

### Definition 6.1.9 — Hydrostatic Pressure and Deviatoric Stress

Any stress tensor decomposes into a **hydrostatic** (spherical) part and a **deviatoric** part:

$$
\sigma_{ij} = -p\,\delta_{ij} + \tau_{ij},
$$

where the **mechanical pressure** is:

$$
p = -\frac{1}{3}\sigma_{kk} = -\frac{1}{3}(\sigma_{11} + \sigma_{22} + \sigma_{33}),
$$

and the **deviatoric stress tensor** $\tau_{ij}$ is trace-free: $\tau_{kk} = 0$.

In a fluid at rest, $\tau_{ij} = 0$ and $\sigma_{ij} = -p\,\delta_{ij}$ (Pascal's law: pressure acts equally in all directions).

### Definition 6.1.10 — Principal Stresses and Principal Directions

The **principal stresses** $\sigma_1, \sigma_2, \sigma_3$ are the eigenvalues of the stress tensor $\boldsymbol{\sigma}$. The corresponding eigenvectors $\hat{n}^{(1)}, \hat{n}^{(2)}, \hat{n}^{(3)}$ are the **principal directions**. On surfaces normal to principal directions, the traction is purely normal (no shear):

$$
\sigma_{ij} n_j^{(k)} = \sigma_k\, n_i^{(k)} \quad (\text{no sum on } k).
$$

Since $\boldsymbol{\sigma}$ is real and symmetric, the principal stresses are real and the principal directions are mutually orthogonal (Spectral Theorem, see [2.4 - Eigenvalues & Eigenvectors](2.4---Eigenvalues-&-Eigenvectors)).




---

## 📐 2. Axioms / Postulates

### Axiom 6.1.A — Cauchy's Postulate (Existence of Stress)

At every point $\mathbf{x}$ in a body and for every unit normal $\hat{n}$, there exists a traction vector $\mathbf{t}^{(\hat{n})}(\mathbf{x})$ that depends continuously on both $\mathbf{x}$ and $\hat{n}$. Furthermore, by Newton's Third Law:

$$
\mathbf{t}^{(-\hat{n})}(\mathbf{x}) = -\mathbf{t}^{(\hat{n})}(\mathbf{x}).
$$

This action-reaction principle on internal surfaces is the starting point for Cauchy's theorem.

### Axiom 6.1.B — Conservation of Linear Momentum (Euler's First Law)

For any sub-body $\mathcal{P}$ occupying volume $V$ with boundary surface $\partial V$:

$$
\frac{d}{dt}\int_V \rho\, \mathbf{v}\, dV = \int_V \rho\, \mathbf{b}\, dV + \oint_{\partial V} \mathbf{t}^{(\hat{n})}\, dA,
$$

where $\rho$ is mass density, $\mathbf{v}$ is velocity, and $\mathbf{b}$ is body force per unit mass (e.g., gravity $\mathbf{b} = \mathbf{g}$).

### Axiom 6.1.C — Conservation of Angular Momentum (Euler's Second Law)

For any sub-body $\mathcal{P}$:

$$
\frac{d}{dt}\int_V \mathbf{x} \times (\rho\, \mathbf{v})\, dV = \int_V \mathbf{x} \times (\rho\, \mathbf{b})\, dV + \oint_{\partial V} \mathbf{x} \times \mathbf{t}^{(\hat{n})}\, dA.
$$

This axiom, combined with the stress tensor representation, forces the symmetry $\sigma_{ij} = \sigma_{ji}$ (in the absence of body couples).

### Axiom 6.1.D — Continuum Hypothesis

The material is modeled as a continuous distribution of matter — all field quantities ($\rho$, $\mathbf{v}$, $\boldsymbol{\sigma}$, $\boldsymbol{\varepsilon}$) are smooth (at least $C^1$) functions of position and time. This breaks down at molecular scales (mean free path $\sim 10^{-7}$ m for gases at STP) but holds for all macroscopic engineering applications.

---

## 🛡️ 3. Lemmas

### Lemma 6.1.1 — Cauchy's Lemma (Traction is Linear in $\hat{n}$)

**Statement.** The traction vector $\mathbf{t}^{(\hat{n})}$ at a point $\mathbf{x}$ depends linearly on the unit normal $\hat{n}$. That is, there exists a second-order tensor $\boldsymbol{\sigma}(\mathbf{x})$ such that:

$$
t_i^{(\hat{n})} = \sigma_{ij}\, n_j.
$$

**Proof.** Consider an infinitesimal tetrahedron at point $\mathbf{x}$ with three faces perpendicular to the coordinate axes (areas $\Delta A_1, \Delta A_2, \Delta A_3$) and one oblique face with outward normal $\hat{n}$ and area $\Delta A$.

**Step 1: Geometric relation between face areas.**

The area of each coordinate face equals the projection of the oblique face onto the corresponding coordinate plane:

$$
\Delta A_j = \Delta A \cdot n_j, \quad j = 1, 2, 3.
$$

This follows from the fact that the outward normal to the $j$-th coordinate face (pointing inward to the tetrahedron) is $-\hat{e}_j$, and the volume of the tetrahedron is $V = \frac{1}{3}h \cdot \Delta A$ where $h$ is the perpendicular height from the opposite vertex to the oblique face.

**Step 2: Force balance on the tetrahedron.**

Apply Newton's second law (Axiom 6.1.B) to the tetrahedron. The forces are:
- Traction on the oblique face: $\mathbf{t}^{(\hat{n})} \Delta A$
- Traction on the $j$-th coordinate face: $\mathbf{t}^{(-\hat{e}_j)} \Delta A_j = -\mathbf{t}^{(\hat{e}_j)} \Delta A_j$ (by Axiom 6.1.A)
- Body force: $\rho \mathbf{b}\, V$
- Inertial term: $\rho \mathbf{a}\, V$

The momentum equation gives:

$$
\mathbf{t}^{(\hat{n})} \Delta A - \sum_{j=1}^{3} \mathbf{t}^{(\hat{e}_j)} \Delta A_j + \rho \mathbf{b}\, V = \rho \mathbf{a}\, V.
$$

**Step 3: Take the limit as the tetrahedron shrinks to zero.**

Since $V \propto h^3$ and $\Delta A \propto h^2$, the ratio $V / \Delta A \propto h \to 0$ as the tetrahedron shrinks. Therefore the body force and inertial terms vanish relative to the surface terms:

$$
\mathbf{t}^{(\hat{n})} \Delta A = \sum_{j=1}^{3} \mathbf{t}^{(\hat{e}_j)} \Delta A_j.
$$

**Step 4: Substitute the geometric relation $\Delta A_j = n_j \Delta A$.**

$$
\mathbf{t}^{(\hat{n})} = \sum_{j=1}^{3} \mathbf{t}^{(\hat{e}_j)} n_j.
$$

**Step 5: Define the stress tensor components.**

Define $\sigma_{ij} \equiv [\mathbf{t}^{(\hat{e}_j)}]_i$ — the $i$-th component of the traction on the face with normal $\hat{e}_j$. Then:

$$
t_i^{(\hat{n})} = \sum_{j=1}^{3} \sigma_{ij}\, n_j = \sigma_{ij}\, n_j. \quad \blacksquare
$$

### Lemma 6.1.2 — Symmetry of the Stress Tensor

**Statement.** In the absence of distributed body couples, the Cauchy stress tensor is symmetric:

$$
\sigma_{ij} = \sigma_{ji}.
$$

**Proof.** Apply conservation of angular momentum (Axiom 6.1.C) to an infinitesimal rectangular parallelepiped with sides $\delta x_1, \delta x_2, \delta x_3$ centered at $\mathbf{x}$.

**Step 1: Compute the torque about the $x_3$-axis from surface tractions.**

Consider the moment about the center due to shear stresses on faces perpendicular to $x_1$ and $x_2$:

- Face at $x_1 + \delta x_1/2$ (area $\delta x_2 \delta x_3$): force in $x_2$-direction is $\sigma_{21}(x_1 + \delta x_1/2) \cdot \delta x_2 \delta x_3$, moment arm $\delta x_1/2$.
- Face at $x_1 - \delta x_1/2$: force in $x_2$-direction is $-\sigma_{21}(x_1 - \delta x_1/2) \cdot \delta x_2 \delta x_3$, moment arm $-\delta x_1/2$.
- Face at $x_2 + \delta x_2/2$ (area $\delta x_1 \delta x_3$): force in $x_1$-direction is $\sigma_{12}(x_2 + \delta x_2/2) \cdot \delta x_1 \delta x_3$, moment arm $\delta x_2/2$.
- Face at $x_2 - \delta x_2/2$: force in $x_1$-direction is $-\sigma_{12}(x_2 - \delta x_2/2) \cdot \delta x_1 \delta x_3$, moment arm $-\delta x_2/2$.

**Step 2: Net torque about $x_3$-axis.**

The net torque (positive counterclockwise) is:

$$
M_3 = \sigma_{21}\, \delta x_1 \delta x_2 \delta x_3 - \sigma_{12}\, \delta x_1 \delta x_2 \delta x_3 + O(\delta x^4).
$$

**Step 3: Angular momentum rate.**

The moment of inertia of the element scales as $I \propto \rho\, \delta x^5$ and the angular acceleration is finite, so:

$$
I \dot{\omega}_3 \propto \rho\, \delta x^5 \cdot \dot{\omega}_3.
$$

**Step 4: Divide by volume $\delta x_1 \delta x_2 \delta x_3$ and take $\delta x \to 0$.**

$$
\sigma_{21} - \sigma_{12} = \lim_{\delta x \to 0} \frac{\rho\, \delta x^5 \cdot \dot{\omega}_3}{\delta x^3} = 0.
$$

Therefore $\sigma_{21} = \sigma_{12}$. By identical arguments for the other pairs:

$$
\sigma_{ij} = \sigma_{ji}. \quad \blacksquare
$$

### Lemma 6.1.3 — Decomposition of Any Second-Order Tensor

**Statement.** Any second-order tensor $T_{ij}$ decomposes uniquely into a symmetric part and an antisymmetric part:

$$
T_{ij} = \underbrace{\frac{1}{2}(T_{ij} + T_{ji})}_{\text{symmetric}} + \underbrace{\frac{1}{2}(T_{ij} - T_{ji})}_{\text{antisymmetric}}.
$$

**Proof.** Define $S_{ij} = \frac{1}{2}(T_{ij} + T_{ji})$ and $A_{ij} = \frac{1}{2}(T_{ij} - T_{ji})$.

Verify symmetry: $S_{ji} = \frac{1}{2}(T_{ji} + T_{ij}) = S_{ij}$. ✓

Verify antisymmetry: $A_{ji} = \frac{1}{2}(T_{ji} - T_{ij}) = -A_{ij}$. ✓

Verify sum: $S_{ij} + A_{ij} = \frac{1}{2}(T_{ij} + T_{ji}) + \frac{1}{2}(T_{ij} - T_{ji}) = T_{ij}$. ✓

Uniqueness: Suppose $T_{ij} = S'_{ij} + A'_{ij}$ with $S'$ symmetric and $A'$ antisymmetric. Then $S_{ij} - S'_{ij} = A'_{ij} - A_{ij}$. The left side is symmetric, the right side is antisymmetric. A tensor that is both symmetric and antisymmetric must be zero. Hence $S' = S$ and $A' = A$. $\blacksquare$




---

## 👑 4. Theorems

### Theorem 6.1.1 — Cauchy's Equation of Motion (Local Momentum Balance)

If the stress field $\sigma_{ij}$ is continuously differentiable, then conservation of linear momentum (Axiom 6.1.B) localizes to:

$$
\rho\, a_i = \frac{\partial \sigma_{ij}}{\partial x_j} + \rho\, b_i,
$$

or in vector notation:

$$
\rho\, \mathbf{a} = \nabla \cdot \boldsymbol{\sigma} + \rho\, \mathbf{b},
$$

where $\mathbf{a} = \frac{D\mathbf{v}}{Dt}$ is the material acceleration and $(\nabla \cdot \boldsymbol{\sigma})_i = \partial_j \sigma_{ij}$.

### Theorem 6.1.2 — Generalized Hooke's Law (Linear Elastic Isotropic Solid)

For a linear elastic isotropic material, the constitutive relation between stress and strain is:

$$
\sigma_{ij} = \lambda\, \varepsilon_{kk}\, \delta_{ij} + 2\mu\, \varepsilon_{ij},
$$

where $\lambda$ and $\mu$ are the **Lamé parameters**. Equivalently:

$$
\varepsilon_{ij} = \frac{1}{2\mu}\sigma_{ij} - \frac{\lambda}{2\mu(3\lambda + 2\mu)}\sigma_{kk}\,\delta_{ij}.
$$

The Lamé parameters relate to Young's modulus $E$ and Poisson's ratio $\nu$ by:

$$
\mu = \frac{E}{2(1+\nu)}, \qquad \lambda = \frac{E\nu}{(1+\nu)(1-2\nu)}.
$$

### Theorem 6.1.3 — Newtonian Constitutive Law (Viscous Fluid)

For a Newtonian viscous fluid, the stress tensor is:

$$
\sigma_{ij} = -p\,\delta_{ij} + 2\mu\, S_{ij} + \lambda\, S_{kk}\, \delta_{ij},
$$

where $p$ is the thermodynamic pressure, $\mu$ is the dynamic viscosity, $\lambda$ is the second (bulk) viscosity coefficient, and $S_{ij}$ is the strain-rate tensor. Under the **Stokes hypothesis** ($\lambda = -\frac{2}{3}\mu$), this becomes:

$$
\sigma_{ij} = -p\,\delta_{ij} + 2\mu\left(S_{ij} - \frac{1}{3}S_{kk}\,\delta_{ij}\right).
$$

This constitutive law is the bridge from Cauchy's equation to the Navier-Stokes equations (Chapter [6.4 - Viscous Fluids - The Navier-Stokes Equations](6.4---Viscous-Fluids---The-Navier-Stokes-Equations)).

### Theorem 6.1.4 — Principal Stress Theorem (Spectral Decomposition)

Since $\boldsymbol{\sigma}$ is real and symmetric, it possesses three real eigenvalues $\sigma_1 \geq \sigma_2 \geq \sigma_3$ (the principal stresses) and three mutually orthogonal eigenvectors $\hat{n}^{(1)}, \hat{n}^{(2)}, \hat{n}^{(3)}$ (the principal directions). In the principal coordinate system:

$$
\boldsymbol{\sigma} = \begin{pmatrix} \sigma_1 & 0 & 0 \\ 0 & \sigma_2 & 0 \\ 0 & 0 & \sigma_3 \end{pmatrix}.
$$

The maximum shear stress occurs on planes at 45° to the principal directions and equals:

$$
\tau_{\max} = \frac{\sigma_1 - \sigma_3}{2}.
$$

---

## ✍️ 5. Proofs / Derivations

### Proof 5.1 — Derivation of Cauchy's Equation of Motion (Theorem 6.1.1)

**Goal:** Localize the integral momentum balance to obtain the PDE $\rho a_i = \partial_j \sigma_{ij} + \rho b_i$.

**Step 1: Start from the integral form (Axiom 6.1.B).**

$$
\frac{d}{dt}\int_V \rho\, v_i\, dV = \int_V \rho\, b_i\, dV + \oint_{\partial V} t_i^{(\hat{n})}\, dA.
$$

**Step 2: Apply Cauchy's Lemma (Lemma 6.1.1) to the surface integral.**

$$
\oint_{\partial V} t_i^{(\hat{n})}\, dA = \oint_{\partial V} \sigma_{ij}\, n_j\, dA.
$$

**Step 3: Apply the Divergence Theorem (see [1.7 - Green's Stokes' and Divergence Theorems](1.7---Green's-Stokes'-and-Divergence-Theorems)).**

$$
\oint_{\partial V} \sigma_{ij}\, n_j\, dA = \int_V \frac{\partial \sigma_{ij}}{\partial x_j}\, dV.
$$

**Step 4: Evaluate the left-hand side using the Reynolds Transport Theorem.**

For a material volume (moving with the fluid), the Reynolds Transport Theorem gives:

$$
\frac{d}{dt}\int_V \rho\, v_i\, dV = \int_V \rho\, \frac{Dv_i}{Dt}\, dV = \int_V \rho\, a_i\, dV,
$$

where we used conservation of mass ($\frac{D\rho}{Dt} + \rho\, \nabla \cdot \mathbf{v} = 0$, see [6.2 - Mass Conservation - The Continuity Equation](6.2---Mass-Conservation---The-Continuity-Equation)).

**Step 5: Combine all terms under a single volume integral.**

$$
\int_V \rho\, a_i\, dV = \int_V \frac{\partial \sigma_{ij}}{\partial x_j}\, dV + \int_V \rho\, b_i\, dV.
$$

$$
\int_V \left(\rho\, a_i - \frac{\partial \sigma_{ij}}{\partial x_j} - \rho\, b_i\right) dV = 0.
$$

**Step 6: Localization.**

Since this holds for *every* sub-volume $V$ (by the arbitrariness of the control volume) and the integrand is continuous, the integrand must vanish identically:

$$
\rho\, a_i = \frac{\partial \sigma_{ij}}{\partial x_j} + \rho\, b_i. \quad \blacksquare
$$

### Proof 5.2 — Derivation of the Strain Tensor from the Deformation Gradient

**Goal:** Show that the infinitesimal strain tensor $\varepsilon_{ij}$ measures the change in squared length of material line elements.

**Step 1: Consider two nearby material points.**

In the reference configuration, let two points be separated by $d\mathbf{X}$. In the current configuration, they are separated by $d\mathbf{x} = \mathbf{F}\, d\mathbf{X}$.

**Step 2: Compute the change in squared length.**

$$
|d\mathbf{x}|^2 - |d\mathbf{X}|^2 = dx_i\, dx_i - dX_I\, dX_I.
$$

Using $dx_i = F_{iJ}\, dX_J$:

$$
dx_i\, dx_i = F_{iJ}\, dX_J\, F_{iK}\, dX_K = F_{iJ}\, F_{iK}\, dX_J\, dX_K = C_{JK}\, dX_J\, dX_K,
$$

where $C_{JK} = F_{iJ}\, F_{iK}$ is the **right Cauchy-Green deformation tensor**.

**Step 3: Express in terms of displacement.**

Since $F_{iJ} = \delta_{iJ} + \frac{\partial u_i}{\partial X_J}$, define $H_{iJ} = \frac{\partial u_i}{\partial X_J}$ so that $F_{iJ} = \delta_{iJ} + H_{iJ}$.

$$
C_{JK} = (\delta_{iJ} + H_{iJ})(\delta_{iK} + H_{iK}) = \delta_{JK} + H_{JK} + H_{KJ} + H_{iJ}\, H_{iK}.
$$

Wait — we must be careful with indices. Since $C_{JK} = F_{iJ} F_{iK}$:

$$
C_{JK} = (\delta_{iJ} + H_{iJ})(\delta_{iK} + H_{iK}) = \delta_{JK} + H_{KJ} + H_{JK} + H_{iJ} H_{iK}.
$$

Actually, expanding term by term:
- $\delta_{iJ}\delta_{iK} = \delta_{JK}$
- $\delta_{iJ} H_{iK} = H_{JK}$
- $H_{iJ}\delta_{iK} = H_{KJ}$
- $H_{iJ} H_{iK}$ = quadratic term

So:

$$
C_{JK} = \delta_{JK} + H_{JK} + H_{KJ} + H_{iJ} H_{iK}.
$$

**Step 4: Define the Green-Lagrange strain tensor.**

$$
|d\mathbf{x}|^2 - |d\mathbf{X}|^2 = (C_{JK} - \delta_{JK})\, dX_J\, dX_K = 2E_{JK}\, dX_J\, dX_K,
$$

where:

$$
E_{JK} = \frac{1}{2}(C_{JK} - \delta_{JK}) = \frac{1}{2}(H_{JK} + H_{KJ} + H_{iJ} H_{iK}).
$$

**Step 5: Linearize for small deformations.**

When $|H_{iJ}| \ll 1$, the quadratic term $H_{iJ} H_{iK}$ is negligible compared to the linear terms. In this regime, the distinction between reference and current coordinates vanishes ($X_J \approx x_j$), and:

$$
E_{JK} \approx \varepsilon_{jk} = \frac{1}{2}\left(\frac{\partial u_j}{\partial x_k} + \frac{\partial u_k}{\partial x_j}\right). \quad \blacksquare
$$

### Proof 5.3 — Derivation of the Newtonian Constitutive Law (Theorem 6.1.3)

**Goal:** Derive $\sigma_{ij} = -p\delta_{ij} + 2\mu S_{ij} + \lambda S_{kk}\delta_{ij}$ from physical assumptions.

**Step 1: State the assumptions for a Newtonian fluid.**

1. The stress depends linearly on the strain rate: $\tau_{ij} = C_{ijkl}\, S_{kl}$ (where $\tau_{ij} = \sigma_{ij} + p\delta_{ij}$ is the viscous stress).
2. The fluid is isotropic: the constitutive tensor $C_{ijkl}$ must be an isotropic fourth-order tensor.

**Step 2: Most general isotropic fourth-order tensor.**

The most general isotropic fourth-order tensor in 3D is (see [2.1 - Vectors, Spans & Linear Independence](2.1---Vectors,-Spans-&-Linear-Independence)):

$$
C_{ijkl} = \lambda\, \delta_{ij}\, \delta_{kl} + \mu\, (\delta_{ik}\, \delta_{jl} + \delta_{il}\, \delta_{jk}) + \gamma\, (\delta_{ik}\, \delta_{jl} - \delta_{il}\, \delta_{jk}).
$$

**Step 3: Apply symmetry of stress and strain rate.**

Since $\sigma_{ij} = \sigma_{ji}$ (Lemma 6.1.2) and $S_{kl} = S_{lk}$ (by definition), we need $C_{ijkl} = C_{jikl}$. The antisymmetric part $\gamma(\delta_{ik}\delta_{jl} - \delta_{il}\delta_{jk})$ gives:

$$
C_{jikl}^{(\gamma)} = \gamma(\delta_{jk}\delta_{il} - \delta_{jl}\delta_{ik}) = -\gamma(\delta_{ik}\delta_{jl} - \delta_{il}\delta_{jk}) = -C_{ijkl}^{(\gamma)}.
$$

For $C_{ijkl} = C_{jikl}$, we need $C_{ijkl}^{(\gamma)} = -C_{ijkl}^{(\gamma)}$, which forces $\gamma = 0$.

**Step 4: Write the final constitutive relation.**

$$
\tau_{ij} = \lambda\, \delta_{ij}\, \delta_{kl}\, S_{kl} + \mu\, (\delta_{ik}\, \delta_{jl} + \delta_{il}\, \delta_{jk})\, S_{kl}.
$$

Contract the indices:
- First term: $\lambda\, \delta_{ij}\, S_{kk}$ (trace of strain rate).
- Second term: $\mu\, (S_{ij} + S_{ji}) = 2\mu\, S_{ij}$ (since $S_{ij} = S_{ji}$).

Therefore:

$$
\sigma_{ij} = -p\,\delta_{ij} + \lambda\, S_{kk}\, \delta_{ij} + 2\mu\, S_{ij}. \quad \blacksquare
$$




---

## 🧮 6. Worked Examples

### Example 6.1.1 — Traction on an Inclined Plane

**Problem.** Given the stress tensor at a point:

$$
\boldsymbol{\sigma} = \begin{pmatrix} 50 & 30 & 0 \\ 30 & -20 & 0 \\ 0 & 0 & 10 \end{pmatrix} \text{ MPa},
$$

find the traction vector on a plane with unit normal $\hat{n} = \frac{1}{\sqrt{2}}(1, 1, 0)$.

**Solution.**

**Step 1:** Apply Cauchy's formula $t_i = \sigma_{ij} n_j$.

$$
n_1 = \frac{1}{\sqrt{2}}, \quad n_2 = \frac{1}{\sqrt{2}}, \quad n_3 = 0.
$$

**Step 2:** Compute each component of the traction vector.

$$
t_1 = \sigma_{11} n_1 + \sigma_{12} n_2 + \sigma_{13} n_3 = 50 \cdot \frac{1}{\sqrt{2}} + 30 \cdot \frac{1}{\sqrt{2}} + 0 = \frac{80}{\sqrt{2}} = 40\sqrt{2} \approx 56.57 \text{ MPa}.
$$

$$
t_2 = \sigma_{21} n_1 + \sigma_{22} n_2 + \sigma_{23} n_3 = 30 \cdot \frac{1}{\sqrt{2}} + (-20) \cdot \frac{1}{\sqrt{2}} + 0 = \frac{10}{\sqrt{2}} = 5\sqrt{2} \approx 7.07 \text{ MPa}.
$$

$$
t_3 = \sigma_{31} n_1 + \sigma_{32} n_2 + \sigma_{33} n_3 = 0 + 0 + 0 = 0 \text{ MPa}.
$$

**Step 3:** The traction vector is $\mathbf{t}^{(\hat{n})} = (40\sqrt{2},\; 5\sqrt{2},\; 0)$ MPa.

**Step 4:** Decompose into normal and shear components.

Normal stress: $\sigma_n = \mathbf{t} \cdot \hat{n} = 40\sqrt{2} \cdot \frac{1}{\sqrt{2}} + 5\sqrt{2} \cdot \frac{1}{\sqrt{2}} + 0 = 40 + 5 = 45$ MPa.

Shear stress magnitude: $\tau = \sqrt{|\mathbf{t}|^2 - \sigma_n^2}$.

$$
|\mathbf{t}|^2 = (40\sqrt{2})^2 + (5\sqrt{2})^2 = 3200 + 50 = 3250.
$$

$$
\tau = \sqrt{3250 - 2025} = \sqrt{1225} = 35 \text{ MPa}.
$$

---

### Example 6.1.2 — Principal Stresses of a 2D Stress State

**Problem.** Find the principal stresses and principal directions for the plane stress state:

$$
\boldsymbol{\sigma} = \begin{pmatrix} 80 & 40 \\ 40 & -20 \end{pmatrix} \text{ MPa}.
$$

**Solution.**

**Step 1:** The principal stresses are eigenvalues of $\boldsymbol{\sigma}$. Solve $\det(\boldsymbol{\sigma} - \sigma_p \mathbf{I}) = 0$.

$$
\det \begin{pmatrix} 80 - \sigma_p & 40 \\ 40 & -20 - \sigma_p \end{pmatrix} = 0.
$$

**Step 2:** Expand the determinant.

$$
(80 - \sigma_p)(-20 - \sigma_p) - (40)(40) = 0.
$$

$$
-1600 - 80\sigma_p + 20\sigma_p + \sigma_p^2 - 1600 = 0.
$$

$$
\sigma_p^2 - 60\sigma_p - 3200 = 0.
$$

**Step 3:** Apply the quadratic formula.

$$
\sigma_p = \frac{60 \pm \sqrt{3600 + 12800}}{2} = \frac{60 \pm \sqrt{16400}}{2} = \frac{60 \pm 20\sqrt{41}}{2} = 30 \pm 10\sqrt{41}.
$$

Numerically: $\sqrt{41} \approx 6.403$, so:

$$
\sigma_1 = 30 + 64.03 = 94.03 \text{ MPa}, \qquad \sigma_2 = 30 - 64.03 = -34.03 \text{ MPa}.
$$

**Step 4:** Find the principal direction for $\sigma_1 = 30 + 10\sqrt{41}$.

$$
(80 - \sigma_1) n_1 + 40\, n_2 = 0 \implies n_2 = -\frac{80 - \sigma_1}{40} n_1 = \frac{\sigma_1 - 80}{40} n_1 = \frac{10\sqrt{41} - 50}{40} n_1.
$$

The principal angle $\theta_p$ satisfies:

$$
\tan(2\theta_p) = \frac{2\sigma_{12}}{\sigma_{11} - \sigma_{22}} = \frac{2(40)}{80 - (-20)} = \frac{80}{100} = 0.8.
$$

$$
2\theta_p = \arctan(0.8) = 38.66°, \qquad \theta_p = 19.33°.
$$

**Step 5:** Maximum shear stress:

$$
\tau_{\max} = \frac{\sigma_1 - \sigma_2}{2} = \frac{(30 + 10\sqrt{41}) - (30 - 10\sqrt{41})}{2} = 10\sqrt{41} \approx 64.03 \text{ MPa}.
$$

---

### Example 6.1.3 — Strain-Rate Tensor for a Simple Shear Flow

**Problem.** A fluid has velocity field $\mathbf{v} = (\dot{\gamma}\, y,\; 0,\; 0)$ where $\dot{\gamma}$ is a constant shear rate. Compute the velocity gradient tensor, strain-rate tensor, and vorticity tensor.

**Solution.**

**Step 1:** Compute the velocity gradient $L_{ij} = \partial v_i / \partial x_j$.

$$
\mathbf{L} = \begin{pmatrix} \partial v_1/\partial x & \partial v_1/\partial y & \partial v_1/\partial z \\ \partial v_2/\partial x & \partial v_2/\partial y & \partial v_2/\partial z \\ \partial v_3/\partial x & \partial v_3/\partial y & \partial v_3/\partial z \end{pmatrix} = \begin{pmatrix} 0 & \dot{\gamma} & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}.
$$

**Step 2:** Compute the strain-rate tensor $S_{ij} = \frac{1}{2}(L_{ij} + L_{ji})$.

$$
\mathbf{S} = \frac{1}{2}\begin{pmatrix} 0+0 & \dot{\gamma}+0 & 0+0 \\ 0+\dot{\gamma} & 0+0 & 0+0 \\ 0+0 & 0+0 & 0+0 \end{pmatrix} = \begin{pmatrix} 0 & \dot{\gamma}/2 & 0 \\ \dot{\gamma}/2 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}.
$$

**Step 3:** Compute the vorticity tensor $\Omega_{ij} = \frac{1}{2}(L_{ij} - L_{ji})$.

$$
\boldsymbol{\Omega} = \frac{1}{2}\begin{pmatrix} 0-0 & \dot{\gamma}-0 & 0-0 \\ 0-\dot{\gamma} & 0-0 & 0-0 \\ 0-0 & 0-0 & 0-0 \end{pmatrix} = \begin{pmatrix} 0 & \dot{\gamma}/2 & 0 \\ -\dot{\gamma}/2 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}.
$$

**Step 4:** Verify $\mathbf{L} = \mathbf{S} + \boldsymbol{\Omega}$:

$$
\mathbf{S} + \boldsymbol{\Omega} = \begin{pmatrix} 0 & \dot{\gamma}/2 + \dot{\gamma}/2 & 0 \\ \dot{\gamma}/2 - \dot{\gamma}/2 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix} = \begin{pmatrix} 0 & \dot{\gamma} & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix} = \mathbf{L}. \quad \checkmark
$$

**Step 5:** The vorticity vector $\boldsymbol{\omega} = \nabla \times \mathbf{v}$:

$$
\omega_3 = \frac{\partial v_2}{\partial x} - \frac{\partial v_1}{\partial y} = 0 - \dot{\gamma} = -\dot{\gamma}.
$$

So $\boldsymbol{\omega} = (0, 0, -\dot{\gamma})$. The fluid element both deforms (strain rate) and rotates (vorticity) simultaneously.

---

### Example 6.1.4 — Hydrostatic and Deviatoric Decomposition

**Problem.** Decompose the stress tensor

$$
\boldsymbol{\sigma} = \begin{pmatrix} 100 & 20 & 0 \\ 20 & 60 & 0 \\ 0 & 0 & -30 \end{pmatrix} \text{ kPa}
$$

into hydrostatic and deviatoric parts.

**Solution.**

**Step 1:** Compute the mechanical pressure.

$$
p = -\frac{1}{3}\sigma_{kk} = -\frac{1}{3}(100 + 60 + (-30)) = -\frac{130}{3} \approx -43.33 \text{ kPa}.
$$

(Negative pressure means net tension.)

**Step 2:** The hydrostatic stress tensor is:

$$
\sigma_{ij}^{(\text{hyd})} = -p\,\delta_{ij} = \frac{130}{3}\begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix} \approx \begin{pmatrix} 43.33 & 0 & 0 \\ 0 & 43.33 & 0 \\ 0 & 0 & 43.33 \end{pmatrix} \text{ kPa}.
$$

**Step 3:** The deviatoric stress tensor is:

$$
\tau_{ij} = \sigma_{ij} - \sigma_{ij}^{(\text{hyd})} = \begin{pmatrix} 100 - 43.33 & 20 & 0 \\ 20 & 60 - 43.33 & 0 \\ 0 & 0 & -30 - 43.33 \end{pmatrix} = \begin{pmatrix} 56.67 & 20 & 0 \\ 20 & 16.67 & 0 \\ 0 & 0 & -73.33 \end{pmatrix} \text{ kPa}.
$$

**Step 4:** Verify trace-free: $56.67 + 16.67 + (-73.33) = 0.01 \approx 0$. ✓ (Exact: $\frac{170}{3} + \frac{50}{3} + \frac{-220}{3} = 0$.)

---

### Example 6.1.5 — Viscous Stress in Poiseuille Flow

**Problem.** For fully-developed Poiseuille flow in a pipe of radius $R$ with velocity $v_z(r) = \frac{G}{4\mu}(R^2 - r^2)$ (where $G = -dP/dz$), compute the viscous stress tensor and the wall shear stress.

**Solution.**

**Step 1:** In cylindrical coordinates $(r, \theta, z)$, the only non-zero velocity component is $v_z(r)$. The strain-rate tensor components:

$$
S_{rz} = S_{zr} = \frac{1}{2}\frac{\partial v_z}{\partial r} = \frac{1}{2} \cdot \frac{G}{4\mu}(-2r) = -\frac{Gr}{4\mu}.
$$

All other $S_{ij} = 0$ (since $v_r = v_\theta = 0$ and $v_z$ depends only on $r$).

**Step 2:** The viscous stress (Newtonian fluid):

$$
\tau_{rz} = 2\mu\, S_{rz} = 2\mu \cdot \left(-\frac{Gr}{4\mu}\right) = -\frac{Gr}{2}.
$$

The negative sign indicates the shear acts in the $-z$ direction on a surface with outward normal in the $+r$ direction (the fluid near the wall retards the faster fluid near the center).

**Step 3:** Wall shear stress at $r = R$:

$$
\tau_w = |\tau_{rz}(R)| = \frac{GR}{2}.
$$

**Step 4:** The total stress tensor at radius $r$:

$$
\sigma_{rz} = \tau_{rz} = -\frac{Gr}{2}, \qquad \sigma_{zz} = -p(z), \qquad \sigma_{rr} = \sigma_{\theta\theta} = -p(r).
$$

The pressure varies linearly in $z$: $p(z) = p_0 - Gz$, confirming the driving pressure gradient.

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- **Prerequisites:** [1.6 - Vector Fields, Div & Curl](1.6---Vector-Fields,-Div-&-Curl) (divergence theorem used in Proof 5.1), [2.4 - Eigenvalues & Eigenvectors](2.4---Eigenvalues-&-Eigenvectors) (principal stress computation), [2.1 - Vectors, Spans & Linear Independence](2.1---Vectors,-Spans-&-Linear-Independence) (tensor algebra)
- **Next chapter:** [6.2 - Mass Conservation - The Continuity Equation](6.2---Mass-Conservation---The-Continuity-Equation) (uses Cauchy's equation framework)
- **Applications:** [6.4 - Viscous Fluids - The Navier-Stokes Equations](6.4---Viscous-Fluids---The-Navier-Stokes-Equations) (Newtonian constitutive law feeds directly into N-S), [6.3 - Inviscid Fluids - Euler's Equation](6.3---Inviscid-Fluids---Euler's-Equation) (stress = $-p\delta_{ij}$ special case)

### External Resources
- Kundu, P.K. & Cohen, I.M., *Fluid Mechanics*, 6th ed., Ch. 2–4 (stress and strain in fluids).
- Malvern, L.E., *Introduction to the Mechanics of a Continuous Medium*, Prentice-Hall (1969) — the definitive reference for continuum kinematics.
- Gurtin, M.E., *An Introduction to Continuum Mechanics*, Academic Press (1981) — mathematically rigorous treatment.
- MIT OCW 2.002 — Mechanics and Materials II (stress/strain tensor lectures).




---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — Principal Stresses and Directions for a Given Cauchy Stress Tensor

**Problem.** The state of stress at a point in a loaded body is given by the Cauchy stress tensor (in MPa):

$$
\boldsymbol{\sigma} = \begin{pmatrix} 50 & 30 & 0 \\ 30 & -20 & 0 \\ 0 & 0 & 10 \end{pmatrix}.
$$

Find the three principal stresses $\sigma_1 \geq \sigma_2 \geq \sigma_3$ and the corresponding principal directions.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Set Up the Eigenvalue Problem

The principal stresses are the eigenvalues of $\boldsymbol{\sigma}$. We solve:

$$
\det(\boldsymbol{\sigma} - \lambda \mathbf{I}) = 0.
$$

Writing this out:

$$
\det \begin{pmatrix} 50 - \lambda & 30 & 0 \\ 30 & -20 - \lambda & 0 \\ 0 & 0 & 10 - \lambda \end{pmatrix} = 0.
$$

#### Step 2: Expand the Determinant

Since the third row has two zeros, expand along the third row (or equivalently, note the block-diagonal structure). The $(3,3)$ cofactor gives:

$$
(10 - \lambda)\det\begin{pmatrix} 50 - \lambda & 30 \\ 30 & -20 - \lambda \end{pmatrix} = 0.
$$

This factors into two problems:
- Either $\lambda = 10$, or
- $\det\begin{pmatrix} 50 - \lambda & 30 \\ 30 & -20 - \lambda \end{pmatrix} = 0$.

#### Step 3: Solve the 2×2 Characteristic Equation

$$
(50 - \lambda)(-20 - \lambda) - (30)(30) = 0.
$$

Expand the product:

$$
-1000 - 50\lambda + 20\lambda + \lambda^2 - 900 = 0.
$$

$$
\lambda^2 - 30\lambda - 1900 = 0.
$$

#### Step 4: Apply the Quadratic Formula

$$
\lambda = \frac{30 \pm \sqrt{900 + 7600}}{2} = \frac{30 \pm \sqrt{8500}}{2} = \frac{30 \pm 92.20}{2}.
$$

Therefore:

$$
\lambda_1 = \frac{30 + 92.20}{2} = 61.10 \;\text{MPa}, \qquad \lambda_2 = \frac{30 - 92.20}{2} = -31.10 \;\text{MPa}.
$$

#### Step 5: Order the Principal Stresses

$$
\sigma_1 = 61.10 \;\text{MPa}, \qquad \sigma_2 = 10 \;\text{MPa}, \qquad \sigma_3 = -31.10 \;\text{MPa}.
$$

#### Step 6: Find the Principal Direction for $\sigma_1 = 61.10$ MPa

Solve $(\boldsymbol{\sigma} - 61.10\,\mathbf{I})\mathbf{n} = \mathbf{0}$:

$$
\begin{pmatrix} -11.10 & 30 & 0 \\ 30 & -81.10 & 0 \\ 0 & 0 & -51.10 \end{pmatrix} \begin{pmatrix} n_1 \\ n_2 \\ n_3 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \\ 0 \end{pmatrix}.
$$

From row 3: $-51.10\, n_3 = 0 \implies n_3 = 0$.

From row 1: $-11.10\, n_1 + 30\, n_2 = 0 \implies n_1 = \frac{30}{11.10}\, n_2 = 2.703\, n_2$.

Normalize: $|\mathbf{n}|^2 = n_1^2 + n_2^2 = (2.703)^2 n_2^2 + n_2^2 = 8.306\, n_2^2 = 1$.

$$
n_2 = \frac{1}{\sqrt{8.306}} = 0.347, \qquad n_1 = 2.703 \times 0.347 = 0.938.
$$

**Principal direction 1:** $\hat{\mathbf{n}}_1 = (0.938,\; 0.347,\; 0)$.

#### Step 7: Find the Principal Direction for $\sigma_3 = -31.10$ MPa

Solve $(\boldsymbol{\sigma} + 31.10\,\mathbf{I})\mathbf{n} = \mathbf{0}$:

$$
\begin{pmatrix} 81.10 & 30 & 0 \\ 30 & 11.10 & 0 \\ 0 & 0 & 41.10 \end{pmatrix} \begin{pmatrix} n_1 \\ n_2 \\ n_3 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \\ 0 \end{pmatrix}.
$$

From row 3: $n_3 = 0$. From row 1: $81.10\, n_1 + 30\, n_2 = 0 \implies n_1 = -0.370\, n_2$.

Normalize: $n_1^2 + n_2^2 = (0.370)^2 n_2^2 + n_2^2 = 1.137\, n_2^2 = 1$.

$$
n_2 = 0.938, \qquad n_1 = -0.347.
$$

**Principal direction 3:** $\hat{\mathbf{n}}_3 = (-0.347,\; 0.938,\; 0)$.

#### Step 8: Principal Direction for $\sigma_2 = 10$ MPa

Since the stress tensor is block-diagonal with the $z$-component decoupled:

**Principal direction 2:** $\hat{\mathbf{n}}_2 = (0,\; 0,\; 1)$.

#### Step 9: Verification

Check orthogonality: $\hat{\mathbf{n}}_1 \cdot \hat{\mathbf{n}}_3 = (0.938)(-0.347) + (0.347)(0.938) + 0 = -0.325 + 0.325 = 0$. ✓

Check trace invariant: $\sigma_1 + \sigma_2 + \sigma_3 = 61.10 + 10 - 31.10 = 40 = 50 + (-20) + 10 = \text{tr}(\boldsymbol{\sigma})$. ✓

**Final Answer:**

$$
\sigma_1 = 61.10\;\text{MPa},\quad \sigma_2 = 10\;\text{MPa},\quad \sigma_3 = -31.10\;\text{MPa}.
$$

</details>

### Example 8.2 — Deviatoric and Hydrostatic Decomposition

**Problem.** Decompose the stress tensor

$$
\boldsymbol{\sigma} = \begin{pmatrix} 100 & 40 & 0 \\ 40 & 60 & 30 \\ 0 & 30 & -20 \end{pmatrix} \;\text{MPa}
$$

into its hydrostatic (spherical) and deviatoric parts. Compute the von Mises equivalent stress.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Compute the Mean (Hydrostatic) Stress

The hydrostatic stress is one-third of the trace:

$$
p = \frac{1}{3}\text{tr}(\boldsymbol{\sigma}) = \frac{1}{3}(\sigma_{11} + \sigma_{22} + \sigma_{33}) = \frac{1}{3}(100 + 60 + (-20)) = \frac{140}{3} = 46.67\;\text{MPa}.
$$

#### Step 2: Write the Hydrostatic Stress Tensor

$$
\boldsymbol{\sigma}^{\text{hyd}} = p\,\mathbf{I} = 46.67 \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix} = \begin{pmatrix} 46.67 & 0 & 0 \\ 0 & 46.67 & 0 \\ 0 & 0 & 46.67 \end{pmatrix}\;\text{MPa}.
$$

#### Step 3: Compute the Deviatoric Stress Tensor

$$
\boldsymbol{\sigma}' = \boldsymbol{\sigma} - \boldsymbol{\sigma}^{\text{hyd}} = \begin{pmatrix} 100 - 46.67 & 40 & 0 \\ 40 & 60 - 46.67 & 30 \\ 0 & 30 & -20 - 46.67 \end{pmatrix}.
$$

$$
\boldsymbol{\sigma}' = \begin{pmatrix} 53.33 & 40 & 0 \\ 40 & 13.33 & 30 \\ 0 & 30 & -66.67 \end{pmatrix}\;\text{MPa}.
$$

#### Step 4: Verify the Deviatoric Tensor is Trace-Free

$$
\text{tr}(\boldsymbol{\sigma}') = 53.33 + 13.33 + (-66.67) = 0. \quad \checkmark
$$

#### Step 5: Compute the Second Invariant $J_2$ of the Deviatoric Tensor

The second invariant of the deviatoric stress is:

$$
J_2 = \frac{1}{2}\sigma'_{ij}\sigma'_{ij} = \frac{1}{2}\left[\sigma'^2_{11} + \sigma'^2_{22} + \sigma'^2_{33} + 2\sigma'^2_{12} + 2\sigma'^2_{13} + 2\sigma'^2_{23}\right].
$$

Substituting:

$$
J_2 = \frac{1}{2}\left[(53.33)^2 + (13.33)^2 + (-66.67)^2 + 2(40)^2 + 2(0)^2 + 2(30)^2\right].
$$

$$
= \frac{1}{2}\left[2844.1 + 177.7 + 4444.9 + 3200 + 0 + 1800\right] = \frac{1}{2}(12466.7) = 6233.3\;\text{MPa}^2.
$$

#### Step 6: Compute the von Mises Equivalent Stress

$$
\sigma_{\text{vM}} = \sqrt{3J_2} = \sqrt{3 \times 6233.3} = \sqrt{18700} = 136.8\;\text{MPa}.
$$

#### Step 7: Physical Interpretation

- The **hydrostatic part** ($p = 46.67$ MPa) causes volumetric compression/expansion — it does not cause yielding in ductile metals (pressure-independent yielding).
- The **deviatoric part** drives shape distortion and is responsible for plastic yielding. The von Mises criterion states that yielding occurs when $\sigma_{\text{vM}} \geq \sigma_Y$ (the yield stress).
- If this material has $\sigma_Y = 250$ MPa, the safety factor is $250/136.8 = 1.83$ — the material is safe.

**Final Answer:**

$$
\boldsymbol{\sigma}' = \begin{pmatrix} 53.33 & 40 & 0 \\ 40 & 13.33 & 30 \\ 0 & 30 & -66.67 \end{pmatrix}\;\text{MPa}, \qquad \sigma_{\text{vM}} = 136.8\;\text{MPa}.
$$

</details>

---

## 📘 9. Appendix: Extended Derivations & Special Cases

### 9.1 Cauchy's Tetrahedron Argument — Proof That Stress is a Tensor

The fundamental result of continuum mechanics is that the traction vector $\mathbf{t}$ on any surface through a point depends *linearly* on the unit normal $\hat{\mathbf{n}}$ to that surface: $t_i = \sigma_{ij} n_j$. This is not obvious — it requires proof. The proof is Cauchy's tetrahedron argument (1823).

**Setup.** Consider a material point $P$ inside a continuum. Construct an infinitesimal tetrahedron with three faces aligned with the coordinate planes ($x_1 x_2$, $x_2 x_3$, $x_1 x_3$) and one oblique face with outward unit normal $\hat{\mathbf{n}} = (n_1, n_2, n_3)$.

Let:
- $A$ = area of the oblique face
- $A_i$ = area of the face perpendicular to the $x_i$-axis

**Geometric relation.** By projecting the oblique face onto each coordinate plane:

$$
A_i = A\, n_i \quad (i = 1, 2, 3).
$$

This is the key geometric fact: the area of each coordinate face equals the oblique area times the corresponding direction cosine.

**Force balance.** Apply Newton's second law to the tetrahedron of volume $V = \frac{1}{3}Ah$ (where $h$ is the height from the oblique face to the opposite vertex):

$$
\mathbf{t}(\hat{\mathbf{n}})\, A - \sum_{i=1}^{3} \mathbf{t}(-\hat{\mathbf{e}}_i)\, A_i + \rho \mathbf{b}\, V = \rho \mathbf{a}\, V.
$$

Here $\mathbf{t}(-\hat{\mathbf{e}}_i)$ is the traction on the face with inward normal $-\hat{\mathbf{e}}_i$ (the coordinate faces have inward normals relative to the tetrahedron).

**The shrinking limit.** As the tetrahedron shrinks to zero ($h \to 0$), the volume $V \propto h^3$ shrinks faster than the areas $A \propto h^2$. Therefore the body force and inertia terms (proportional to $V$) become negligible compared to the surface traction terms (proportional to $A$). Dividing by $A$:

$$
\mathbf{t}(\hat{\mathbf{n}}) = \sum_{i=1}^{3} \mathbf{t}(\hat{\mathbf{e}}_i)\, n_i.
$$

(We used Newton's third law: $\mathbf{t}(-\hat{\mathbf{e}}_i) = -\mathbf{t}(\hat{\mathbf{e}}_i)$.)

**Defining the stress tensor.** Define $\sigma_{ji} \equiv$ the $j$-th component of the traction vector on the face with normal $\hat{\mathbf{e}}_i$:

$$
[\mathbf{t}(\hat{\mathbf{e}}_i)]_j = \sigma_{ji}.
$$

Then the result becomes, in component form:

$$
t_j(\hat{\mathbf{n}}) = \sigma_{ji}\, n_i = \sigma_{j1} n_1 + \sigma_{j2} n_2 + \sigma_{j3} n_3.
$$

This is **Cauchy's stress theorem**: the traction on any plane is a linear function of the normal, and the coefficients form a second-order tensor $\sigma_{ij}$. The linearity is not assumed — it is *derived* from Newton's laws in the limit of vanishing volume.

**Why this matters.** Without this result, we would need to specify the traction for every possible surface orientation independently — an infinite amount of information. Cauchy's theorem reduces this to just 9 numbers (6 independent, by symmetry) at each point. This is what makes continuum mechanics tractable.

**References:** Malvern (1969), §5.3; Gurtin (1981), §14; Kundu & Cohen, Ch. 2.

---
