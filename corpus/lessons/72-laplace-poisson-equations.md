---
title: "Laplace Poisson Equations"
subject: "Electrodynamics & Classical Field Theory"
catalog: advanced
audience_tier: higher-education
chapter: "7.2"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 7.2 — Laplace & Poisson Equations

> *"The theory of the potential is the most beautiful branch of mathematical physics."* — Oliver Heaviside
>
> *"The solution of Laplace's equation is the bread and butter of electrostatics."* — David J. Griffiths, *Introduction to Electrodynamics*

Having established in [7.1 - Electrostatics - Gauss's Law & Potential](7.1---Electrostatics---Gauss's-Law-&-Potential) that the electrostatic potential satisfies $\nabla^2\phi = -\rho/\varepsilon_0$ (Poisson's equation) and $\nabla^2\phi = 0$ in charge-free regions (Laplace's equation), we now develop the mathematical machinery to **solve** these equations subject to boundary conditions. This chapter covers separation of variables in Cartesian, spherical, and cylindrical coordinates, the method of images, multipole expansions, and Green's functions — the complete toolkit for electrostatic boundary value problems.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. State and prove the uniqueness theorems for solutions to Laplace's and Poisson's equations.
2. Apply separation of variables in Cartesian coordinates to solve Laplace's equation in rectangular geometries.
3. Apply separation of variables in spherical coordinates, deriving Legendre polynomials as the angular solutions.
4. Use the method of images to solve problems with grounded conducting planes and spheres.
5. Derive and apply the multipole expansion of the potential for localized charge distributions.
6. Construct the Green's function for the Laplacian and use it to solve Poisson's equation.
7. Verify solutions satisfy both the PDE and all boundary conditions.

---

## 🖼️ Visual Anchor — Equipotential Surfaces of a Conducting Sphere

![math-07__7.2-fig1](math-07__7.2-fig1.svg)

**Interpretation:** The equipotential surfaces of a charged conductor are concentric (for a sphere). The electric field lines are everywhere perpendicular to equipotentials. On the conductor surface, $\phi = V_0$ is constant (Dirichlet boundary condition). Laplace's equation $\nabla^2\phi = 0$ governs the potential in the exterior region.

---

## 📚 1. Definitions

### Definition 7.2.1 — Laplace's Equation

A scalar function $\phi(\mathbf{r})$ satisfies **Laplace's equation** if:

$$
\nabla^2\phi = 0
$$

In Cartesian coordinates: $\frac{\partial^2\phi}{\partial x^2} + \frac{\partial^2\phi}{\partial y^2} + \frac{\partial^2\phi}{\partial z^2} = 0$.

In spherical coordinates $(r,\theta,\phi)$:

$$
\frac{1}{r^2}\frac{\partial}{\partial r}\left(r^2\frac{\partial\phi}{\partial r}\right) + \frac{1}{r^2\sin\theta}\frac{\partial}{\partial\theta}\left(\sin\theta\frac{\partial\phi}{\partial\theta}\right) + \frac{1}{r^2\sin^2\theta}\frac{\partial^2\phi}{\partial\varphi^2} = 0
$$

In cylindrical coordinates $(s,\varphi,z)$:

$$
\frac{1}{s}\frac{\partial}{\partial s}\left(s\frac{\partial\phi}{\partial s}\right) + \frac{1}{s^2}\frac{\partial^2\phi}{\partial\varphi^2} + \frac{\partial^2\phi}{\partial z^2} = 0
$$

Solutions to Laplace's equation are called **harmonic functions**.

### Definition 7.2.2 — Poisson's Equation

$$
\nabla^2\phi = f(\mathbf{r})
$$

In electrostatics, $f = -\rho/\varepsilon_0$. Poisson's equation is the inhomogeneous generalization of Laplace's equation.

### Definition 7.2.3 — Boundary Conditions

A well-posed boundary value problem requires specifying conditions on the boundary $\partial V$ of the domain:

| Type | Name | Specification | Physical Example |
|:---|:---|:---|:---|
| **Dirichlet** | First kind | $\phi\big|_{\partial V} = f(\mathbf{r})$ | Conductor held at voltage $V_0$ |
| **Neumann** | Second kind | $\frac{\partial\phi}{\partial n}\big|_{\partial V} = g(\mathbf{r})$ | Specified surface charge $\sigma = -\varepsilon_0\partial\phi/\partial n$ |
| **Robin** | Third kind (mixed) | $\alpha\phi + \beta\frac{\partial\phi}{\partial n}\big|_{\partial V} = h(\mathbf{r})$ | Impedance boundary |

Here $\partial/\partial n$ denotes the outward normal derivative.

### Definition 7.2.4 — Green's Function for the Laplacian

The **Green's function** $G(\mathbf{r}, \mathbf{r}')$ satisfies:

$$
\nabla^2 G(\mathbf{r}, \mathbf{r}') = -4\pi\,\delta^3(\mathbf{r} - \mathbf{r}')
$$

with appropriate boundary conditions. The free-space Green's function is:

$$
G_0(\mathbf{r}, \mathbf{r}') = \frac{1}{|\mathbf{r} - \mathbf{r}'|}
$$

The solution to Poisson's equation $\nabla^2\phi = -\rho/\varepsilon_0$ is then:

$$
\phi(\mathbf{r}) = \frac{1}{4\pi\varepsilon_0}\int_V \frac{\rho(\mathbf{r}')}{|\mathbf{r}-\mathbf{r}'|}\,d\tau'
$$

### Definition 7.2.5 — Legendre Polynomials

The **Legendre polynomials** $P_l(x)$ are solutions to Legendre's equation:

$$
\frac{d}{dx}\left[(1-x^2)\frac{dP_l}{dx}\right] + l(l+1)P_l = 0
$$

They arise naturally in the angular part of Laplace's equation in spherical coordinates. The first several are:

$$
P_0(x) = 1, \quad P_1(x) = x, \quad P_2(x) = \frac{1}{2}(3x^2-1), \quad P_3(x) = \frac{1}{2}(5x^3-3x)
$$

**Orthogonality:**

$$
\int_{-1}^{1} P_l(x)\,P_{l'}(x)\,dx = \frac{2}{2l+1}\,\delta_{ll'}
$$

### Definition 7.2.6 — Spherical Harmonics

The **spherical harmonics** $Y_l^m(\theta,\varphi)$ are the complete angular solutions to Laplace's equation in spherical coordinates:

$$
Y_l^m(\theta,\varphi) = \sqrt{\frac{2l+1}{4\pi}\frac{(l-m)!}{(l+m)!}}\,P_l^m(\cos\theta)\,e^{im\varphi}
$$

where $P_l^m$ are the associated Legendre functions. They satisfy:

$$
\int Y_l^m\,(Y_{l'}^{m'})^*\,d\Omega = \delta_{ll'}\delta_{mm'}
$$

### Definition 7.2.7 — Multipole Expansion

For a localized charge distribution, the potential at large distances can be expanded as:

$$
\phi(\mathbf{r}) = \frac{1}{4\pi\varepsilon_0}\sum_{l=0}^{\infty}\frac{1}{r^{l+1}}\int (r')^l\,P_l(\cos\alpha)\,\rho(\mathbf{r}')\,d\tau'
$$

where $\alpha$ is the angle between $\mathbf{r}$ and $\mathbf{r}'$. The terms are:
- $l = 0$: **Monopole** (total charge $Q$)
- $l = 1$: **Dipole** (dipole moment $\mathbf{p}$)
- $l = 2$: **Quadrupole** (quadrupole tensor $Q_{ij}$)

### Definition 7.2.8 — Image Charge

An **image charge** is a fictitious charge placed outside the region of interest such that the combined potential of the real and image charges satisfies the boundary conditions on a conductor. The method works because:
1. The image charge is outside the domain, so it does not alter the source term $\rho$ inside.
2. Uniqueness guarantees that if the boundary conditions are satisfied, the solution is correct.




---

## 📐 2. Axioms / Postulates

### Axiom 7.2.1 — Well-Posedness of Electrostatic BVPs

A boundary value problem for Laplace's or Poisson's equation is **well-posed** (in the sense of Hadamard) if:
1. A solution **exists**.
2. The solution is **unique** (given appropriate boundary conditions).
3. The solution **depends continuously** on the boundary data (stability).

For electrostatics, Dirichlet or Neumann conditions on a closed boundary surface guarantee well-posedness.

### Axiom 7.2.2 — Conductors in Electrostatic Equilibrium

A conductor in electrostatic equilibrium satisfies:
1. $\mathbf{E} = 0$ everywhere inside the conductor.
2. $\rho = 0$ inside; all excess charge resides on the surface.
3. The surface is an equipotential: $\phi = \text{const}$ on the conductor.
4. $\mathbf{E}$ is perpendicular to the surface just outside: $\mathbf{E} = (\sigma/\varepsilon_0)\hat{\mathbf{n}}$.

These follow from the requirement that charges are free to move until equilibrium is reached.

### Axiom 7.2.3 — Completeness of Orthogonal Function Sets

The eigenfunctions arising from separation of variables (sines/cosines, Legendre polynomials, Bessel functions, spherical harmonics) form **complete orthogonal sets** on their respective domains. Any sufficiently well-behaved function can be expanded in these bases.

---

## 🛡️ 3. Lemmas

### Lemma 7.2.1 — Mean Value Property of Harmonic Functions

**Statement:** If $\phi$ satisfies $\nabla^2\phi = 0$ in a domain containing a sphere of radius $R$ centered at $\mathbf{r}_0$, then:

$$
\phi(\mathbf{r}_0) = \frac{1}{4\pi R^2}\oint_{S_R} \phi\,da
$$

The value at the center equals the average over any surrounding sphere.

<details>
<summary>🔍 Proof of Lemma 7.2.1</summary>

**Step 1:** Consider the identity (from Green's second identity, proven in [1.7 - Green's Stokes' and Divergence Theorems](1.7---Green's-Stokes'-and-Divergence-Theorems)):

$$
\int_V \left(\phi\,\nabla^2\psi - \psi\,\nabla^2\phi\right)d\tau = \oint_S \left(\phi\frac{\partial\psi}{\partial n} - \psi\frac{\partial\phi}{\partial n}\right)da
$$

**Step 2:** Let $\psi = 1/|\mathbf{r} - \mathbf{r}_0|$ (the free-space Green's function centered at $\mathbf{r}_0$). Then $\nabla^2\psi = -4\pi\delta^3(\mathbf{r}-\mathbf{r}_0)$.

**Step 3:** Since $\nabla^2\phi = 0$ in the domain, the volume integral becomes:

$$
\int_V \phi\cdot(-4\pi\delta^3(\mathbf{r}-\mathbf{r}_0))\,d\tau - 0 = -4\pi\phi(\mathbf{r}_0)
$$

**Step 4:** On the sphere $S_R$, $|\mathbf{r}-\mathbf{r}_0| = R$ is constant, so $\psi = 1/R$ and $\frac{\partial\psi}{\partial n} = -1/R^2$ (the outward normal derivative of $1/|\mathbf{r}-\mathbf{r}_0|$ on a sphere centered at $\mathbf{r}_0$).

**Step 5:** The surface integral becomes:

$$
\oint_{S_R}\left(\phi\cdot\left(-\frac{1}{R^2}\right) - \frac{1}{R}\frac{\partial\phi}{\partial n}\right)da = -\frac{1}{R^2}\oint_{S_R}\phi\,da - \frac{1}{R}\oint_{S_R}\frac{\partial\phi}{\partial n}\,da
$$

**Step 6:** By the Divergence Theorem, $\oint_{S_R}\frac{\partial\phi}{\partial n}\,da = \int_V\nabla^2\phi\,d\tau = 0$ (since $\phi$ is harmonic).

**Step 7:** Equating volume and surface integrals:

$$
-4\pi\phi(\mathbf{r}_0) = -\frac{1}{R^2}\oint_{S_R}\phi\,da
$$

$$
\phi(\mathbf{r}_0) = \frac{1}{4\pi R^2}\oint_{S_R}\phi\,da
$$

$\blacksquare$

</details>

### Lemma 7.2.2 — Maximum/Minimum Principle

**Statement:** A harmonic function $\phi$ (satisfying $\nabla^2\phi = 0$) in a bounded domain $V$ attains its maximum and minimum values **only on the boundary** $\partial V$, never in the interior (unless $\phi$ is constant).

<details>
<summary>🔍 Proof of Lemma 7.2.2</summary>

**Step 1:** Suppose $\phi$ attains a maximum at an interior point $\mathbf{r}_0 \in V$. Then $\phi(\mathbf{r}_0) \geq \phi(\mathbf{r})$ for all $\mathbf{r}$ in some neighborhood.

**Step 2:** By the mean value property (Lemma 7.2.1), for any sphere of radius $R$ centered at $\mathbf{r}_0$ contained in $V$:

$$
\phi(\mathbf{r}_0) = \frac{1}{4\pi R^2}\oint_{S_R}\phi\,da
$$

**Step 3:** Since $\phi(\mathbf{r}) \leq \phi(\mathbf{r}_0)$ on $S_R$, the average cannot exceed $\phi(\mathbf{r}_0)$. But the average equals $\phi(\mathbf{r}_0)$. This is possible only if $\phi(\mathbf{r}) = \phi(\mathbf{r}_0)$ everywhere on $S_R$.

**Step 4:** Since $R$ is arbitrary (as long as the sphere fits in $V$), $\phi$ must be constant throughout the connected component containing $\mathbf{r}_0$.

**Step 5:** Therefore, if $\phi$ is not constant, it cannot attain its maximum in the interior. The same argument applies to the minimum (consider $-\phi$). $\blacksquare$

</details>

### Lemma 7.2.3 — Green's First and Second Identities

**Statement (First Identity):** For scalar fields $\phi$ and $\psi$ in volume $V$ bounded by $S$:

$$
\int_V (\phi\,\nabla^2\psi + \nabla\phi\cdot\nabla\psi)\,d\tau = \oint_S \phi\frac{\partial\psi}{\partial n}\,da
$$

**Statement (Second Identity):**

$$
\int_V (\phi\,\nabla^2\psi - \psi\,\nabla^2\phi)\,d\tau = \oint_S \left(\phi\frac{\partial\psi}{\partial n} - \psi\frac{\partial\phi}{\partial n}\right)da
$$

These are direct consequences of the Divergence Theorem applied to $\phi\nabla\psi$ and $\phi\nabla\psi - \psi\nabla\phi$ respectively (see [1.7 - Green's Stokes' and Divergence Theorems](1.7---Green's-Stokes'-and-Divergence-Theorems) for the full derivation).

### Lemma 7.2.4 — Separation of Variables Produces Complete Solutions

**Statement:** If the domain geometry matches a coordinate system in which Laplace's equation separates, then the general solution is a sum (or integral) of product solutions, and this sum is complete — it can represent any solution satisfying the given boundary conditions.

For Cartesian coordinates, the separated solutions are products of exponentials and trigonometric functions. For spherical coordinates, they are $r^l P_l^m(\cos\theta)e^{im\varphi}$ and $r^{-(l+1)}P_l^m(\cos\theta)e^{im\varphi}$.




---

## 👑 4. Theorems

### Theorem 7.2.1 — First Uniqueness Theorem

The solution to Laplace's equation in a volume $V$ is uniquely determined if $\phi$ is specified on the boundary surface $S$ (Dirichlet condition).

### Theorem 7.2.2 — Second Uniqueness Theorem

In a volume $V$ surrounded by conductors and containing a specified charge density $\rho$, the electric field is uniquely determined if the **total charge** on each conductor is given.

### Theorem 7.2.3 — Separation of Variables in Spherical Coordinates

The general solution to Laplace's equation with azimuthal symmetry (no $\varphi$-dependence) is:

$$
\phi(r,\theta) = \sum_{l=0}^{\infty}\left(A_l\,r^l + \frac{B_l}{r^{l+1}}\right)P_l(\cos\theta)
$$

where $A_l$ and $B_l$ are determined by boundary conditions.

### Theorem 7.2.4 — The Addition Theorem for $1/|\mathbf{r}-\mathbf{r}'|$

$$
\frac{1}{|\mathbf{r}-\mathbf{r}'|} = \sum_{l=0}^{\infty}\frac{r_<^l}{r_>^{l+1}}\,P_l(\cos\gamma)
$$

where $r_< = \min(r,r')$, $r_> = \max(r,r')$, and $\gamma$ is the angle between $\mathbf{r}$ and $\mathbf{r}'$.

### Theorem 7.2.5 — Method of Images for a Grounded Plane

A point charge $q$ at distance $d$ above an infinite grounded conducting plane is equivalent (in the region above the plane) to the original charge plus an image charge $-q$ at distance $d$ below the plane.

### Theorem 7.2.6 — Method of Images for a Grounded Sphere

A point charge $q$ at distance $a$ from the center of a grounded conducting sphere of radius $R$ (with $a > R$) is equivalent to the original charge plus an image charge $q' = -qR/a$ located at distance $b = R^2/a$ from the center (inside the sphere, along the line from center to $q$).

---

## ✍️ 5. Proofs / Derivations

### Derivation 7.2.1 — First Uniqueness Theorem

<details>
<summary>🔍 Complete Proof</summary>

**Goal:** Prove that if $\phi_1$ and $\phi_2$ both satisfy $\nabla^2\phi = 0$ in $V$ with $\phi_1 = \phi_2 = f$ on $\partial V$, then $\phi_1 = \phi_2$ throughout $V$.

**Step 1:** Define $\phi_3 \equiv \phi_1 - \phi_2$. Then:

$$
\nabla^2\phi_3 = \nabla^2\phi_1 - \nabla^2\phi_2 = 0 - 0 = 0
$$

So $\phi_3$ is harmonic in $V$.

**Step 2:** On the boundary: $\phi_3\big|_{\partial V} = \phi_1\big|_{\partial V} - \phi_2\big|_{\partial V} = f - f = 0$.

**Step 3:** By the Maximum/Minimum Principle (Lemma 7.2.2), $\phi_3$ attains its maximum and minimum on $\partial V$. Since $\phi_3 = 0$ on $\partial V$:

$$
\max_V \phi_3 = \min_V \phi_3 = 0
$$

**Step 4:** Therefore $\phi_3 = 0$ everywhere in $V$, which means $\phi_1 = \phi_2$. $\blacksquare$

**Alternative proof using energy:** Apply Green's first identity with $\phi = \psi = \phi_3$:

$$
\int_V (|\nabla\phi_3|^2 + \phi_3\,\nabla^2\phi_3)\,d\tau = \oint_S \phi_3\frac{\partial\phi_3}{\partial n}\,da
$$

Since $\nabla^2\phi_3 = 0$ and $\phi_3 = 0$ on $S$:

$$
\int_V |\nabla\phi_3|^2\,d\tau = 0
$$

Since the integrand is non-negative and continuous, $\nabla\phi_3 = 0$ everywhere, so $\phi_3 = \text{const}$. Combined with $\phi_3 = 0$ on the boundary, $\phi_3 = 0$ everywhere. $\blacksquare$

</details>

### Derivation 7.2.2 — Separation of Variables in Cartesian Coordinates

<details>
<summary>🔍 Complete Derivation</summary>

**Problem:** Solve $\nabla^2\phi = 0$ in a rectangular box $0 \leq x \leq a$, $0 \leq y \leq b$, $0 \leq z \leq c$ with $\phi = 0$ on five faces and $\phi(x,y,c) = V_0(x,y)$ on the top face.

**Step 1:** Assume a product solution $\phi(x,y,z) = X(x)\,Y(y)\,Z(z)$. Substituting into $\nabla^2\phi = 0$:

$$
X''YZ + XY''Z + XYZ'' = 0
$$

**Step 2:** Divide by $XYZ$:

$$
\frac{X''}{X} + \frac{Y''}{Y} + \frac{Z''}{Z} = 0
$$

**Step 3:** Each term depends on a different variable, so each must be constant. Set:

$$
\frac{X''}{X} = -k_x^2, \quad \frac{Y''}{Y} = -k_y^2, \quad \frac{Z''}{Z} = k_x^2 + k_y^2 \equiv \gamma^2
$$

(The signs are chosen to satisfy boundary conditions: $X$ and $Y$ must vanish at both ends, requiring oscillatory solutions.)

**Step 4:** Solve the $X$ equation with $X(0) = X(a) = 0$:

$$
X'' + k_x^2 X = 0 \implies X(x) = \sin(k_x x), \quad k_x = \frac{n\pi}{a}, \quad n = 1,2,3,\ldots
$$

**Step 5:** Similarly for $Y$ with $Y(0) = Y(b) = 0$:

$$
Y(y) = \sin(k_y y), \quad k_y = \frac{m\pi}{b}, \quad m = 1,2,3,\ldots
$$

**Step 6:** The $Z$ equation with $Z(0) = 0$ (bottom face):

$$
Z'' - \gamma^2 Z = 0, \quad \gamma = \pi\sqrt{\frac{n^2}{a^2}+\frac{m^2}{b^2}}
$$

$$
Z(z) = \sinh(\gamma_{nm} z)
$$

**Step 7:** The general solution is:

$$
\phi(x,y,z) = \sum_{n=1}^{\infty}\sum_{m=1}^{\infty} C_{nm}\sin\left(\frac{n\pi x}{a}\right)\sin\left(\frac{m\pi y}{b}\right)\sinh(\gamma_{nm} z)
$$

**Step 8:** Apply the top boundary condition $\phi(x,y,c) = V_0(x,y)$:

$$
V_0(x,y) = \sum_{n,m} C_{nm}\sinh(\gamma_{nm} c)\sin\left(\frac{n\pi x}{a}\right)\sin\left(\frac{m\pi y}{b}\right)
$$

**Step 9:** By orthogonality of the sine functions, multiply both sides by $\sin(n'\pi x/a)\sin(m'\pi y/b)$ and integrate:

$$
C_{nm}\sinh(\gamma_{nm}c) = \frac{4}{ab}\int_0^a\int_0^b V_0(x,y)\sin\left(\frac{n\pi x}{a}\right)\sin\left(\frac{m\pi y}{b}\right)dx\,dy
$$

$\blacksquare$

</details>

### Derivation 7.2.3 — Separation of Variables in Spherical Coordinates

<details>
<summary>🔍 Complete Derivation</summary>

**Step 1:** Write Laplace's equation in spherical coordinates (azimuthal symmetry, $\partial/\partial\varphi = 0$):

$$
\frac{1}{r^2}\frac{\partial}{\partial r}\left(r^2\frac{\partial\phi}{\partial r}\right) + \frac{1}{r^2\sin\theta}\frac{\partial}{\partial\theta}\left(\sin\theta\frac{\partial\phi}{\partial\theta}\right) = 0
$$

**Step 2:** Assume $\phi(r,\theta) = R(r)\,\Theta(\theta)$. Substitute and multiply by $r^2/(R\Theta)$:

$$
\frac{1}{R}\frac{d}{dr}\left(r^2\frac{dR}{dr}\right) + \frac{1}{\Theta\sin\theta}\frac{d}{d\theta}\left(\sin\theta\frac{d\Theta}{d\theta}\right) = 0
$$

**Step 3:** The first term depends only on $r$, the second only on $\theta$. Each must be a constant. Set:

$$
\frac{1}{R}\frac{d}{dr}\left(r^2\frac{dR}{dr}\right) = l(l+1)
$$

$$
\frac{1}{\Theta\sin\theta}\frac{d}{d\theta}\left(\sin\theta\frac{d\Theta}{d\theta}\right) = -l(l+1)
$$

**Step 4 (Radial equation):** The equation $\frac{d}{dr}(r^2 R') = l(l+1)R$ has the general solution:

$$
R(r) = A\,r^l + B\,r^{-(l+1)}
$$

To verify: if $R = r^l$, then $r^2 R' = lr^{l+1}$, and $\frac{d}{dr}(lr^{l+1}) = l(l+1)r^l = l(l+1)R$. ✓

**Step 5 (Angular equation):** Substitute $x = \cos\theta$, so $\frac{d}{d\theta} = -\sin\theta\frac{d}{dx}$. The equation becomes:

$$
\frac{d}{dx}\left[(1-x^2)\frac{d\Theta}{dx}\right] + l(l+1)\Theta = 0
$$

This is **Legendre's equation**. The solutions regular at $x = \pm 1$ (i.e., $\theta = 0, \pi$) are the Legendre polynomials $P_l(x) = P_l(\cos\theta)$, with $l = 0, 1, 2, \ldots$

**Step 6:** The general azimuthally symmetric solution is:

$$
\phi(r,\theta) = \sum_{l=0}^{\infty}\left(A_l\,r^l + \frac{B_l}{r^{l+1}}\right)P_l(\cos\theta)
$$

$\blacksquare$

</details>

### Derivation 7.2.4 — Method of Images: Point Charge Above Grounded Plane

<details>
<summary>🔍 Complete Derivation</summary>

**Setup:** A point charge $+q$ is at position $(0, 0, d)$ above an infinite grounded conducting plane at $z = 0$. Find $\phi$ for $z \gt  0$.

**Step 1:** The boundary condition is $\phi(x,y,0) = 0$ for all $(x,y)$.

**Step 2:** Place an image charge $-q$ at $(0, 0, -d)$ (the mirror position below the plane). The potential in the region $z \gt  0$ is:

$$
\phi(\mathbf{r}) = \frac{1}{4\pi\varepsilon_0}\left[\frac{q}{\sqrt{x^2+y^2+(z-d)^2}} - \frac{q}{\sqrt{x^2+y^2+(z+d)^2}}\right]
$$

**Step 3 (Verify boundary condition):** At $z = 0$:

$$
\phi(x,y,0) = \frac{q}{4\pi\varepsilon_0}\left[\frac{1}{\sqrt{x^2+y^2+d^2}} - \frac{1}{\sqrt{x^2+y^2+d^2}}\right] = 0 \quad \checkmark
$$

**Step 4 (Verify Poisson's equation):** In the region $z \gt  0$, the image charge at $z = -d$ contributes no source term. The only source is the real charge at $(0,0,d)$:

$$
\nabla^2\phi = -\frac{q}{\varepsilon_0}\delta^3(\mathbf{r} - d\hat{\mathbf{z}}) \quad \checkmark
$$

**Step 5:** By the uniqueness theorem (Theorem 7.2.1), this is THE solution.

**Step 6 (Induced surface charge):** The surface charge on the conductor is:

$$
\sigma = -\varepsilon_0\frac{\partial\phi}{\partial z}\bigg|_{z=0}
$$

Computing:

$$
\frac{\partial\phi}{\partial z}\bigg|_{z=0} = \frac{q}{4\pi\varepsilon_0}\left[\frac{-(0-d)}{(x^2+y^2+d^2)^{3/2}} - \frac{-(0+d)}{(x^2+y^2+d^2)^{3/2}}\right]
$$

$$
= \frac{q}{4\pi\varepsilon_0}\cdot\frac{2d}{(x^2+y^2+d^2)^{3/2}} = \frac{qd}{2\pi\varepsilon_0(x^2+y^2+d^2)^{3/2}}
$$

Wait — let us be more careful with signs. Define $s^2 = x^2 + y^2$:

$$
\frac{\partial}{\partial z}\left[\frac{1}{\sqrt{s^2+(z-d)^2}}\right]_{z=0} = \frac{-(0-d)}{(s^2+d^2)^{3/2}} = \frac{d}{(s^2+d^2)^{3/2}}
$$

$$
\frac{\partial}{\partial z}\left[\frac{-1}{\sqrt{s^2+(z+d)^2}}\right]_{z=0} = \frac{(0+d)}{(s^2+d^2)^{3/2}} = \frac{d}{(s^2+d^2)^{3/2}}
$$

Wait — let me redo this systematically. For the term $+q/\sqrt{s^2+(z-d)^2}$:

$$
\frac{\partial}{\partial z}\frac{1}{\sqrt{s^2+(z-d)^2}} = -\frac{z-d}{(s^2+(z-d)^2)^{3/2}}
$$

At $z=0$: $= -\frac{-d}{(s^2+d^2)^{3/2}} = \frac{d}{(s^2+d^2)^{3/2}}$

For the term $-q/\sqrt{s^2+(z+d)^2}$:

$$
\frac{\partial}{\partial z}\frac{-1}{\sqrt{s^2+(z+d)^2}} = \frac{z+d}{(s^2+(z+d)^2)^{3/2}}
$$

At $z=0$: $= \frac{d}{(s^2+d^2)^{3/2}}$

**Step 7:** Total:

$$
\frac{\partial\phi}{\partial z}\bigg|_{z=0} = \frac{q}{4\pi\varepsilon_0}\cdot\frac{2d}{(s^2+d^2)^{3/2}}
$$

Wait — this gives a positive normal derivative, meaning $\mathbf{E}$ points upward at the surface. But the induced charge should be negative (attracted to $+q$). The issue is the sign convention: $\sigma = -\varepsilon_0\frac{\partial\phi}{\partial n}$ where $\hat{n}$ points **into** the conductor (downward, $-\hat{z}$). Using $\hat{n} = +\hat{z}$ (outward from conductor into the region of interest):

$$
\sigma = -\varepsilon_0\frac{\partial\phi}{\partial z}\bigg|_{z=0^+}
$$

Hmm, let me use the standard result. The electric field just above the surface is $E_z = -\partial\phi/\partial z$. The surface charge is $\sigma = \varepsilon_0 E_z|_{\text{above}} = -\varepsilon_0\partial\phi/\partial z|_{z=0^+}$:

$$
\sigma = -\varepsilon_0\cdot\frac{q}{4\pi\varepsilon_0}\cdot\frac{2d}{(s^2+d^2)^{3/2}} = -\frac{qd}{2\pi(s^2+d^2)^{3/2}}
$$

**Step 8 (Total induced charge):** Integrate over the plane:

$$
Q_{\text{ind}} = \int_0^\infty \sigma\cdot 2\pi s\,ds = -qd\int_0^\infty \frac{s\,ds}{(s^2+d^2)^{3/2}}
$$

Substitute $u = s^2 + d^2$:

$$
= -qd\left[-\frac{1}{\sqrt{s^2+d^2}}\right]_0^\infty = -qd\left(0 - \left(-\frac{1}{d}\right)\right) = -q
$$

The total induced charge equals $-q$, as expected from Gauss's Law. $\blacksquare$

</details>

### Derivation 7.2.5 — Multipole Expansion

<details>
<summary>🔍 Complete Derivation</summary>

**Goal:** Expand $\phi(\mathbf{r}) = \frac{1}{4\pi\varepsilon_0}\int\frac{\rho(\mathbf{r}')}{|\mathbf{r}-\mathbf{r}'|}d\tau'$ for $r \gg r'$ (far from the source).

**Step 1:** Use the addition theorem (Theorem 7.2.4):

$$
\frac{1}{|\mathbf{r}-\mathbf{r}'|} = \sum_{l=0}^{\infty}\frac{(r')^l}{r^{l+1}}P_l(\cos\alpha)
$$

where $\alpha$ is the angle between $\mathbf{r}$ and $\mathbf{r}'$ (valid for $r \gt  r'$).

**Step 2:** Substitute into the potential:

$$
\phi(\mathbf{r}) = \frac{1}{4\pi\varepsilon_0}\sum_{l=0}^{\infty}\frac{1}{r^{l+1}}\int(r')^l P_l(\cos\alpha)\,\rho(\mathbf{r}')\,d\tau'
$$

**Step 3 (Monopole term, $l=0$):** $P_0 = 1$, so:

$$
\phi_{\text{mono}} = \frac{1}{4\pi\varepsilon_0}\frac{1}{r}\int\rho(\mathbf{r}')\,d\tau' = \frac{Q}{4\pi\varepsilon_0 r}
$$

where $Q$ is the total charge.

**Step 4 (Dipole term, $l=1$):** $P_1(\cos\alpha) = \cos\alpha = \hat{\mathbf{r}}\cdot\hat{\mathbf{r}}'$, so:

$$
\phi_{\text{dip}} = \frac{1}{4\pi\varepsilon_0}\frac{1}{r^2}\int r'\cos\alpha\,\rho(\mathbf{r}')\,d\tau' = \frac{1}{4\pi\varepsilon_0}\frac{\hat{\mathbf{r}}\cdot\mathbf{p}}{r^2}
$$

where $\mathbf{p} = \int\mathbf{r}'\rho(\mathbf{r}')d\tau'$ is the dipole moment.

**Step 5 (Quadrupole term, $l=2$):** $P_2(\cos\alpha) = \frac{1}{2}(3\cos^2\alpha - 1)$:

$$
\phi_{\text{quad}} = \frac{1}{4\pi\varepsilon_0}\frac{1}{r^3}\int\frac{(r')^2}{2}(3\cos^2\alpha - 1)\,\rho(\mathbf{r}')\,d\tau'
$$

This can be written in terms of the traceless quadrupole tensor $Q_{ij} = \int(3r_i'r_j' - r'^2\delta_{ij})\rho\,d\tau'$:

$$
\phi_{\text{quad}} = \frac{1}{4\pi\varepsilon_0}\frac{1}{4r^3}\sum_{i,j}\hat{r}_i\hat{r}_j\,Q_{ij}
$$

$\blacksquare$

</details>




---

## 🧮 6. Worked Examples

### Example 7.2.1 — Conducting Sphere in a Uniform Field

**Problem:** An uncharged conducting sphere of radius $R$ is placed in a uniform external electric field $\mathbf{E}_0 = E_0\hat{\mathbf{z}}$. Find the potential everywhere outside the sphere.

<details>
<summary>🔍 Complete Solution</summary>

**Step 1 (Boundary conditions):**
- At $r = R$: $\phi = 0$ (grounded sphere, or equivalently, choose the zero of potential on the sphere).
- As $r \to \infty$: $\phi \to -E_0 z = -E_0 r\cos\theta$.

**Step 2 (General solution):** With azimuthal symmetry:

$$
\phi(r,\theta) = \sum_{l=0}^{\infty}\left(A_l r^l + \frac{B_l}{r^{l+1}}\right)P_l(\cos\theta)
$$

**Step 3 (Apply far-field condition):** As $r \to \infty$, $\phi \to -E_0 r\cos\theta = -E_0 r P_1(\cos\theta)$. This requires $A_1 = -E_0$ and $A_l = 0$ for $l \neq 1$ (since $B_l/r^{l+1} \to 0$).

**Step 4 (Apply boundary condition at $r = R$):** $\phi(R,\theta) = 0$ for all $\theta$:

$$
0 = \sum_{l=0}^{\infty}\left(A_l R^l + \frac{B_l}{R^{l+1}}\right)P_l(\cos\theta)
$$

By orthogonality of Legendre polynomials, each coefficient must vanish:

$$
A_l R^l + \frac{B_l}{R^{l+1}} = 0 \quad \text{for all } l
$$

**Step 5:** For $l = 1$: $-E_0 R + B_1/R^2 = 0 \implies B_1 = E_0 R^3$.

For $l \neq 1$: $A_l = 0$, so $B_l = 0$.

**Step 6 (Final solution):**

$$
\phi(r,\theta) = -E_0 r\cos\theta + \frac{E_0 R^3}{r^2}\cos\theta = -E_0\cos\theta\left(r - \frac{R^3}{r^2}\right)
$$

**Step 7 (Interpretation):** The first term is the applied uniform field. The second term is a dipole field with effective dipole moment $\mathbf{p} = 4\pi\varepsilon_0 R^3 E_0\hat{\mathbf{z}}$. The sphere acquires an induced dipole moment proportional to the applied field.

**Step 8 (Surface charge):**

$$
\sigma(\theta) = -\varepsilon_0\frac{\partial\phi}{\partial r}\bigg|_{r=R} = -\varepsilon_0\left(-E_0\cos\theta - \frac{2E_0 R^3\cos\theta}{R^3}\right) = 3\varepsilon_0 E_0\cos\theta
$$

The charge is positive on the hemisphere facing the field and negative on the opposite side.

</details>

---

### Example 7.2.2 — Image Charge for a Grounded Sphere

**Problem:** A point charge $q$ is at distance $a$ from the center of a grounded conducting sphere of radius $R$ ($a > R$). Find the potential outside the sphere and the force on $q$.

<details>
<summary>🔍 Complete Solution</summary>

**Step 1 (Image charge):** By Theorem 7.2.6, place an image charge $q' = -qR/a$ at distance $b = R^2/a$ from the center, along the line from center to $q$.

**Step 2 (Verify boundary condition):** Place the center at the origin and $q$ at $(a, 0, 0)$. The image is at $(R^2/a, 0, 0)$. For a point $P$ on the sphere at distance $R$ from center:

Let $r_1 = |P - (a,0,0)|$ and $r_2 = |P - (R^2/a, 0, 0)|$.

By the geometric property of inversion: for any point $P$ on the sphere of radius $R$,

$$
\frac{r_1}{r_2} = \frac{a}{R}
$$

**Step 3:** The potential at $P$ is:

$$
\phi(P) = \frac{1}{4\pi\varepsilon_0}\left(\frac{q}{r_1} + \frac{q'}{r_2}\right) = \frac{1}{4\pi\varepsilon_0}\left(\frac{q}{r_1} - \frac{qR}{a\,r_2}\right)
$$

Using $r_1/r_2 = a/R$, i.e., $r_1 = (a/R)r_2$:

$$
\phi(P) = \frac{q}{4\pi\varepsilon_0 r_2}\left(\frac{R}{a} - \frac{R}{a}\right) = 0 \quad \checkmark
$$

**Step 4 (Force on $q$):** The force is the Coulomb attraction between $q$ and its image $q'$, separated by distance $a - b = a - R^2/a$:

$$
F = \frac{1}{4\pi\varepsilon_0}\frac{q\cdot q'}{(a-b)^2} = -\frac{1}{4\pi\varepsilon_0}\frac{q^2 R a}{(a^2-R^2)^2}
$$

The negative sign indicates attraction toward the sphere.

**Step 5 (Induced charge):** The total induced charge on the sphere equals the image charge: $Q_{\text{ind}} = q' = -qR/a$.

</details>

---

### Example 7.2.3 — Separation of Variables: Hemisphere at Potential $V_0$

**Problem:** A spherical shell of radius $R$ has its upper hemisphere ($0 \leq \theta < \pi/2$) at potential $V_0$ and its lower hemisphere ($\pi/2 < \theta \leq \pi$) at potential $-V_0$. Find $\phi(r,\theta)$ for $r > R$.

<details>
<summary>🔍 Complete Solution</summary>

**Step 1:** For $r \gt  R$, the solution must vanish at infinity, so $A_l = 0$:

$$
\phi(r,\theta) = \sum_{l=0}^{\infty}\frac{B_l}{r^{l+1}}P_l(\cos\theta)
$$

**Step 2 (Boundary condition at $r = R$):**

$$
\phi(R,\theta) = \sum_{l=0}^{\infty}\frac{B_l}{R^{l+1}}P_l(\cos\theta) = \begin{cases} V_0 & 0 \leq \theta \lt  \pi/2 \\ -V_0 & \pi/2 \lt  \theta \leq \pi \end{cases}
$$

**Step 3 (Find coefficients):** Multiply by $P_{l'}(\cos\theta)\sin\theta$ and integrate from $0$ to $\pi$:

$$
\frac{B_l}{R^{l+1}}\cdot\frac{2}{2l+1} = V_0\int_0^{\pi/2}P_l(\cos\theta)\sin\theta\,d\theta - V_0\int_{\pi/2}^{\pi}P_l(\cos\theta)\sin\theta\,d\theta
$$

**Step 4:** Substitute $x = \cos\theta$:

$$
\frac{B_l}{R^{l+1}}\cdot\frac{2}{2l+1} = V_0\int_0^1 P_l(x)\,dx - V_0\int_{-1}^0 P_l(x)\,dx = V_0\int_0^1 P_l(x)\,dx + V_0\int_0^1 P_l(-x)\,dx
$$

Wait — let me be careful. With $x = \cos\theta$, $dx = -\sin\theta\,d\theta$:

$$
\int_0^{\pi/2}P_l(\cos\theta)\sin\theta\,d\theta = \int_1^0 P_l(x)(-dx) = \int_0^1 P_l(x)\,dx
$$

$$
\int_{\pi/2}^{\pi}P_l(\cos\theta)\sin\theta\,d\theta = \int_0^{-1}P_l(x)(-dx) = \int_{-1}^0 P_l(x)\,dx
$$

So:

$$
\frac{2B_l}{(2l+1)R^{l+1}} = V_0\left[\int_0^1 P_l(x)\,dx - \int_{-1}^0 P_l(x)\,dx\right]
$$

**Step 5:** Since $P_l(-x) = (-1)^l P_l(x)$:

$$
\int_{-1}^0 P_l(x)\,dx = \int_0^1 P_l(-x)\,dx = (-1)^l\int_0^1 P_l(x)\,dx
$$

Therefore:

$$
\frac{2B_l}{(2l+1)R^{l+1}} = V_0[1 - (-1)^l]\int_0^1 P_l(x)\,dx
$$

**Step 6:** The factor $[1-(-1)^l]$ vanishes for even $l$ and equals $2$ for odd $l$. Only odd-$l$ terms survive (as expected from the antisymmetry of the boundary condition).

**Step 7:** For odd $l$, using known integrals of Legendre polynomials:

$$
\int_0^1 P_1(x)\,dx = \frac{1}{2}, \quad \int_0^1 P_3(x)\,dx = -\frac{1}{8}, \quad \int_0^1 P_5(x)\,dx = \frac{1}{16}
$$

**Step 8:** The first few coefficients:

$$
B_1 = \frac{3}{2}V_0 R^2, \quad B_3 = -\frac{7}{8}V_0 R^4, \quad B_5 = \frac{11}{16}V_0 R^6
$$

**Step 9 (Final answer):**

$$
\phi(r,\theta) = V_0\left[\frac{3}{2}\frac{R^2}{r^2}P_1(\cos\theta) - \frac{7}{8}\frac{R^4}{r^4}P_3(\cos\theta) + \frac{11}{16}\frac{R^6}{r^6}P_5(\cos\theta) - \cdots\right]
$$

At large $r$, the dominant term is the dipole: $\phi \approx \frac{3V_0 R^2}{2r^2}\cos\theta$.

</details>

---

### Example 7.2.4 — Green's Function Solution for a Grounded Sphere

**Problem:** Using the Green's function method, express the potential inside a grounded sphere of radius $R$ with interior charge density $\rho(\mathbf{r}')$.

<details>
<summary>🔍 Complete Solution</summary>

**Step 1:** The Green's function for the interior of a sphere with Dirichlet boundary condition $G|_{r'=R} = 0$ is:

$$
G(\mathbf{r},\mathbf{r}') = \frac{1}{|\mathbf{r}-\mathbf{r}'|} - \frac{R/r'}{|\mathbf{r} - (R^2/r'^2)\mathbf{r}'|}
$$

The second term is the image contribution (an image at the inverted point $(R^2/r')\hat{\mathbf{r}}'$).

**Step 2:** The solution to Poisson's equation with $\phi|_{r=R} = 0$ is:

$$
\phi(\mathbf{r}) = \frac{1}{4\pi\varepsilon_0}\int_V G(\mathbf{r},\mathbf{r}')\,\rho(\mathbf{r}')\,d\tau'
$$

**Step 3:** If instead the boundary condition is $\phi|_{r=R} = V(\theta,\varphi)$ (non-zero), add the homogeneous solution:

$$
\phi(\mathbf{r}) = \frac{1}{4\pi\varepsilon_0}\int_V G(\mathbf{r},\mathbf{r}')\rho(\mathbf{r}')d\tau' - \frac{1}{4\pi}\oint_S V(\mathbf{r}')\frac{\partial G}{\partial n'}\,da'
$$

**Step 4:** The normal derivative of $G$ on the sphere evaluates to:

$$
\frac{\partial G}{\partial n'}\bigg|_{r'=R} = -\frac{\partial G}{\partial r'}\bigg|_{r'=R} = -\frac{R^2 - r^2}{R(r^2 + R^2 - 2rR\cos\gamma)^{3/2}}
$$

where $\gamma$ is the angle between $\mathbf{r}$ and $\mathbf{r}'$.

**Step 5:** For the case $\rho = 0$ (no interior charges), this gives the **Poisson integral formula**:

$$
\phi(\mathbf{r}) = \frac{R^2 - r^2}{4\pi R}\oint_S \frac{V(\mathbf{r}')}{(r^2+R^2-2rR\cos\gamma)^{3/2}}\,da'
$$

This expresses the interior potential entirely in terms of the boundary values — a remarkable result.

</details>

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links

| Topic | Link | Relevance |
|:---|:---|:---|
| Electrostatic foundations | [7.1 - Electrostatics - Gauss's Law & Potential](7.1---Electrostatics---Gauss's-Law-&-Potential) | Derives Poisson's equation from Gauss's Law |
| Integral theorems | [1.7 - Green's Stokes' and Divergence Theorems](1.7---Green's-Stokes'-and-Divergence-Theorems) | Green's identities used in uniqueness proofs |
| ODEs and PDEs | [3.2 - Second-Order Linear ODEs](3.2---Second-Order-Linear-ODEs) | Legendre, Bessel equations are special cases |
| Magnetostatic BVPs | [7.3 - Magnetostatics - Biot-Savart & Ampere's Law](7.3---Magnetostatics---Biot-Savart-&-Ampere's-Law) | Analogous boundary value problems for $\mathbf{A}$ |
| Gauge theory | [7.6 - Potential Formulations & Gauge Transformations](7.6---Potential-Formulations-&-Gauge-Transformations) | Generalization of potential methods |

### Authoritative External Resources

1. **Griffiths, D.J.** — *Introduction to Electrodynamics*, 4th ed., Chapter 3. Complete treatment of separation of variables and multipole expansion.
2. **Jackson, J.D.** — *Classical Electrodynamics*, 3rd ed., Chapters 2–3. The definitive graduate treatment of boundary value problems.
3. **Arfken, Weber & Harris** — *Mathematical Methods for Physicists*, 7th ed. Comprehensive coverage of special functions (Legendre, Bessel, spherical harmonics).
4. **MIT OCW 8.07** — [Electromagnetism II](https://ocw.mit.edu/courses/8-07-electromagnetism-ii-fall-2012/). Advanced boundary value problems.

### Key Equations Summary

| Name | Equation | Number |
|:---|:---|:---|
| Laplace's equation | $\nabla^2\phi = 0$ | (7.2.1) |
| Poisson's equation | $\nabla^2\phi = -\rho/\varepsilon_0$ | (7.2.2) |
| Spherical separation | $\phi = \sum(A_l r^l + B_l r^{-(l+1)})P_l(\cos\theta)$ | (7.2.3) |
| Addition theorem | $1/|\mathbf{r}-\mathbf{r}'| = \sum r_<^l/r_>^{l+1}\,P_l(\cos\gamma)$ | (7.2.4) |
| Image charge (plane) | $q' = -q$ at mirror position | (7.2.5) |
| Image charge (sphere) | $q' = -qR/a$ at $b = R^2/a$ | (7.2.6) |
| Multipole expansion | $\phi = \frac{1}{4\pi\varepsilon_0}\sum\frac{1}{r^{l+1}}\int(r')^l P_l\rho\,d\tau'$ | (7.2.7) |

