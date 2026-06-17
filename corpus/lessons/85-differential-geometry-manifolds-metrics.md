---
title: "8.5 — Differential Geometry: Manifolds & Metrics"
subject: "Special & General Relativity"
catalog: advanced
audience_tier: higher-education
chapter: "8.5"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

I star
*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 8.5 — Differential Geometry: Manifolds & Metrics

> *"I am now occupied with a new paper on the hypotheses which lie at the foundation of geometry."*
> — Bernhard Riemann, letter to his father (1854)

General Relativity is, at its mathematical core, the theory of a **pseudo-Riemannian manifold** — a smooth space equipped with a metric tensor that determines distances, angles, and curvature. Before we can write Einstein's field equations, we must master the language of differential geometry: manifolds, tangent spaces, metrics, and tensor fields.

This chapter provides the geometric foundations. We define what a manifold is, construct tangent and cotangent spaces, introduce the metric tensor as the fundamental object encoding gravitational physics, and compute line elements for physically important spacetimes.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Define a smooth manifold and explain why spacetime requires this structure.
2. Construct the tangent space $T_pM$ and cotangent space $T^*_pM$ at a point.
3. Define tensor fields on manifolds and their transformation laws under coordinate changes.
4. Write the metric tensor $g_{\mu\nu}$ and compute the line element $ds^2$.
5. Compute the inverse metric $g^{\mu\nu}$ and use it to raise/lower indices.
6. Write the Schwarzschild, FLRW, and Kerr metrics in standard coordinates.
7. Compute proper distances and proper times from the metric.
8. Identify coordinate singularities vs. physical singularities.

---

## 🖼️ Visual Anchor — Manifold, Tangent Space & Metric

![math-08__8.5-fig1](math-08__8.5-fig1.svg)

---

## 📚 1. Definitions

### Definition 8.5.1 — Topological Manifold

An **$n$-dimensional topological manifold** $M$ is a topological space that is:
1. **Hausdorff** (distinct points have disjoint neighborhoods)
2. **Second-countable** (has a countable basis for its topology)
3. **Locally Euclidean** — every point $p \in M$ has a neighborhood $U$ homeomorphic to an open subset of $\mathbb{R}^n$

The homeomorphism $\phi: U \to \mathbb{R}^n$ is called a **coordinate chart**. A collection of charts covering all of $M$ is an **atlas**.

### Definition 8.5.2 — Smooth Manifold

A topological manifold is **smooth** ($C^\infty$) if, wherever two charts $(U, \phi)$ and $(V, \psi)$ overlap, the **transition map** $\psi \circ \phi^{-1}: \phi(U\cap V) \to \psi(U\cap V)$ is a smooth ($C^\infty$) map between open subsets of $\mathbb{R}^n$.

Spacetime is modeled as a 4-dimensional smooth manifold.

### Definition 8.5.3 — Tangent Vector (Geometric Definition)

A **tangent vector** at $p \in M$ is a derivation on the algebra of smooth functions at $p$: a linear map $V: C^\infty(M) \to \mathbb{R}$ satisfying the Leibniz rule:

$$
V(fg) = f(p)\, V(g) + g(p)\, V(f)
$$

In coordinates $(x^1, \ldots, x^n)$, the tangent vectors $\partial/\partial x^\mu|_p$ form a basis for the tangent space $T_pM$. Any tangent vector can be written:

$$
V = V^\mu \frac{\partial}{\partial x^\mu}\bigg|_p
$$

### Definition 8.5.4 — Cotangent Space and 1-Forms

The **cotangent space** $T^*_pM$ is the dual of $T_pM$ — the space of linear maps $\omega: T_pM \to \mathbb{R}$. Its basis is $\{dx^\mu\}$, dual to $\{\partial/\partial x^\nu\}$:

$$
dx^\mu\left(\frac{\partial}{\partial x^\nu}\right) = \delta^\mu{}_\nu
$$

A general 1-form: $\omega = \omega_\mu\, dx^\mu$.

### Definition 8.5.5 — Tensor Field

A **$(p,q)$-tensor field** on $M$ assigns to each point $p$ a multilinear map:

$$
T: \underbrace{T^*_pM \times \cdots \times T^*_pM}_{p} \times \underbrace{T_pM \times \cdots \times T_pM}_{q} \to \mathbb{R}
$$

In coordinates:

$$
T = T^{\mu_1\cdots\mu_p}{}_{\nu_1\cdots\nu_q}\, \frac{\partial}{\partial x^{\mu_1}} \otimes \cdots \otimes \frac{\partial}{\partial x^{\mu_p}} \otimes dx^{\nu_1} \otimes \cdots \otimes dx^{\nu_q}
$$

Under coordinate change $x^\mu \to x'^\mu$:

$$
T'^{\mu_1\cdots\mu_p}{}_{\nu_1\cdots\nu_q} = \frac{\partial x'^{\mu_1}}{\partial x^{\alpha_1}} \cdots \frac{\partial x'^{\mu_p}}{\partial x^{\alpha_p}} \frac{\partial x^{\beta_1}}{\partial x'^{\nu_1}} \cdots \frac{\partial x^{\beta_q}}{\partial x'^{\nu_q}} T^{\alpha_1\cdots\alpha_p}{}_{\beta_1\cdots\beta_q}
$$

### Definition 8.5.6 — The Metric Tensor

The **metric tensor** $g$ is a symmetric, non-degenerate $(0,2)$-tensor field:

$$
g = g_{\mu\nu}(x)\, dx^\mu \otimes dx^\nu
$$

Properties:
- **Symmetric:** $g_{\mu\nu} = g_{\nu\mu}$
- **Non-degenerate:** $\det(g_{\mu\nu}) \neq 0$ everywhere
- **Signature:** For spacetime, signature $(-,+,+,+)$ (Lorentzian/pseudo-Riemannian)

The **line element**:

$$
ds^2 = g_{\mu\nu}\, dx^\mu\, dx^\nu
$$

### Definition 8.5.7 — Inverse Metric

The **inverse metric** $g^{\mu\nu}$ is defined by:

$$
g^{\mu\alpha}g_{\alpha\nu} = \delta^\mu{}_\nu
$$

It is used to raise indices: $V^\mu = g^{\mu\nu}V_\nu$.

### Definition 8.5.8 — Important Spacetime Metrics

**Schwarzschild metric** (static, spherically symmetric vacuum):

$$
ds^2 = -\left(1 - \frac{r_s}{r}\right)c^2 dt^2 + \left(1 - \frac{r_s}{r}\right)^{-1}dr^2 + r^2(d\theta^2 + \sin^2\theta\, d\phi^2)
$$

where $r_s = 2GM/c^2$ is the Schwarzschild radius.

**FLRW metric** (homogeneous, isotropic, expanding universe):

$$
ds^2 = -c^2 dt^2 + a(t)^2\left[\frac{dr^2}{1-kr^2} + r^2(d\theta^2 + \sin^2\theta\, d\phi^2)\right]
$$

where $a(t)$ is the scale factor and $k \in \{-1, 0, +1\}$ is the spatial curvature.

**Kerr metric** (rotating black hole, Boyer-Lindquist coordinates):

$$
ds^2 = -\left(1 - \frac{r_s r}{\Sigma}\right)c^2 dt^2 - \frac{2r_s r a \sin^2\theta}{\Sigma}\, c\, dt\, d\phi + \frac{\Sigma}{\Delta}dr^2 + \Sigma\, d\theta^2 + \frac{A\sin^2\theta}{\Sigma}d\phi^2
$$

where $\Sigma = r^2 + a^2\cos^2\theta$, $\Delta = r^2 - r_s r + a^2$, $A = (r^2+a^2)^2 - a^2\Delta\sin^2\theta$, and $a = J/(Mc)$ is the spin parameter.




---

## 📐 2. Axioms / Postulates

### Axiom 8.5.1 — Spacetime is a 4D Smooth Manifold

Physical spacetime is modeled as a connected, 4-dimensional, smooth, Hausdorff manifold $M$ equipped with a Lorentzian metric $g_{\mu\nu}$ of signature $(-,+,+,+)$.

### Axiom 8.5.2 — The Metric Encodes All Gravitational Information

The metric tensor $g_{\mu\nu}(x)$ is the fundamental dynamical variable of General Relativity. From it, one can derive:
- Christoffel symbols (connection) → how vectors parallel-transport
- Riemann tensor (curvature) → tidal forces
- Geodesics → free-fall trajectories
- Causal structure → light cones at every point

### Axiom 8.5.3 — Coordinate Independence

Physical observables (proper time, proper distance, curvature scalars) are independent of the coordinate system used to compute them. Only **scalar** quantities formed from tensors are directly measurable.

---

## 🛡️ 3. Lemmas

### Lemma 8.5.1 — Transformation Law for the Metric

**Statement:** Under coordinate change $x^\mu \to x'^\mu(x)$:

$$
g'_{\mu\nu}(x') = \frac{\partial x^\alpha}{\partial x'^\mu}\frac{\partial x^\beta}{\partial x'^\nu} g_{\alpha\beta}(x)
$$

**Proof:** The line element $ds^2$ is a scalar (invariant):

$$
ds^2 = g_{\alpha\beta}\, dx^\alpha\, dx^\beta = g'_{\mu\nu}\, dx'^\mu\, dx'^\nu
$$

Since $dx^\alpha = (\partial x^\alpha/\partial x'^\mu)\, dx'^\mu$:

$$
g_{\alpha\beta}\frac{\partial x^\alpha}{\partial x'^\mu}\frac{\partial x^\beta}{\partial x'^\nu}dx'^\mu dx'^\nu = g'_{\mu\nu}\, dx'^\mu\, dx'^\nu
$$

Since this holds for all $dx'^\mu$:

$$
g'_{\mu\nu} = \frac{\partial x^\alpha}{\partial x'^\mu}\frac{\partial x^\beta}{\partial x'^\nu} g_{\alpha\beta} \qquad \blacksquare
$$

### Lemma 8.5.2 — Local Flatness (Existence of Normal Coordinates)

**Statement:** At any point $p$ on a pseudo-Riemannian manifold, there exist coordinates (Riemann normal coordinates) such that:

$$
g_{\mu\nu}(p) = \eta_{\mu\nu}, \qquad \partial_\alpha g_{\mu\nu}(p) = 0
$$

However, in general $\partial_\alpha\partial_\beta g_{\mu\nu}(p) \neq 0$ (these encode curvature).

**Proof sketch:** $g_{\mu\nu}(p) = \eta_{\mu\nu}$ can be achieved by a linear transformation (diagonalize the symmetric matrix). The condition $\partial_\alpha g_{\mu\nu}(p) = 0$ provides $4 \times 10 = 40$ equations for the $4 \times 10 = 40$ free parameters in the second-order Taylor coefficients of the coordinate transformation. The system is exactly determined. The remaining $\partial_\alpha\partial_\beta g_{\mu\nu}$ (20 independent components in 4D, after symmetries) cannot be set to zero — they form the Riemann tensor. $\blacksquare$

### Lemma 8.5.3 — Determinant of the Metric and Volume Element

**Statement:** The invariant volume element on a pseudo-Riemannian manifold is:

$$
d\mathcal{V} = \sqrt{-g}\, d^4x
$$

where $g = \det(g_{\mu\nu})$ (negative for Lorentzian signature).

**Proof:** Under $x \to x'$: $g' = g \cdot (\det J)^{-2}$ where $J^\mu{}_\nu = \partial x'^\mu/\partial x^\nu$. Also $d^4x' = |\det J|\, d^4x$. Therefore $\sqrt{-g'}\, d^4x' = \sqrt{-g}\, d^4x$. $\blacksquare$

---

## 👑 4. Theorems

### Theorem 8.5.1 — Proper Time from the Metric

**Statement:** The proper time along a timelike worldline $x^\mu(\lambda)$ is:

$$
\Delta\tau = \int_{\lambda_1}^{\lambda_2} \frac{1}{c}\sqrt{-g_{\mu\nu}\frac{dx^\mu}{d\lambda}\frac{dx^\nu}{d\lambda}}\, d\lambda
$$

### Theorem 8.5.2 — Proper Distance

**Statement:** The proper spatial distance along a spacelike curve at constant time is:

$$
\Delta\ell = \int \sqrt{g_{ij}\, dx^i\, dx^j}
$$

For the Schwarzschild metric, the proper radial distance between $r_1$ and $r_2$ is:

$$
\Delta\ell = \int_{r_1}^{r_2} \frac{dr}{\sqrt{1 - r_s/r}} > r_2 - r_1
$$

(proper distance exceeds coordinate distance due to spatial curvature).

### Theorem 8.5.3 — Killing Vectors and Conserved Quantities

**Statement:** If the metric is independent of a coordinate $x^\alpha$ (i.e., $\partial g_{\mu\nu}/\partial x^\alpha = 0$), then $\xi^\mu = \delta^\mu_\alpha$ is a **Killing vector** and the quantity:

$$
p_\alpha = g_{\alpha\mu}\frac{dx^\mu}{d\tau}
$$

is conserved along geodesics. For the Schwarzschild metric:
- $\partial_t g_{\mu\nu} = 0$ → energy $E = -p_t$ is conserved
- $\partial_\phi g_{\mu\nu} = 0$ → angular momentum $L = p_\phi$ is conserved




---

## ✍️ 5. Proofs / Derivations

### Proof 8.5.1 — Computing the Inverse Schwarzschild Metric

**Setup:** The Schwarzschild metric in coordinates $(t, r, \theta, \phi)$:

$$
g_{\mu\nu} = \text{diag}\left(-\left(1-\frac{r_s}{r}\right)c^2,\, \left(1-\frac{r_s}{r}\right)^{-1},\, r^2,\, r^2\sin^2\theta\right)
$$

**Step 1:** For a diagonal metric, the inverse is simply the reciprocal of each diagonal element:

$$
g^{\mu\nu} = \text{diag}\left(-\frac{1}{(1-r_s/r)c^2},\, \left(1-\frac{r_s}{r}\right),\, \frac{1}{r^2},\, \frac{1}{r^2\sin^2\theta}\right)
$$

**Step 2:** Verify $g^{\mu\alpha}g_{\alpha\nu} = \delta^\mu{}_\nu$:

$$
g^{00}g_{00} = \frac{-1}{(1-r_s/r)c^2} \times (-(1-r_s/r)c^2) = 1 = \delta^0{}_0 \quad \checkmark
$$

$$
g^{11}g_{11} = (1-r_s/r) \times (1-r_s/r)^{-1} = 1 = \delta^1{}_1 \quad \checkmark
$$

**Step 3:** The determinant:

$$
g = \det(g_{\mu\nu}) = -(1-r_s/r)c^2 \times (1-r_s/r)^{-1} \times r^2 \times r^2\sin^2\theta = -c^2 r^4\sin^2\theta
$$

$$
\sqrt{-g} = cr^2\sin\theta \qquad \blacksquare
$$

---

### Proof 8.5.2 — Proper Time for a Static Observer in Schwarzschild Spacetime

**Setup:** A static observer sits at fixed $(r, \theta, \phi)$ — i.e., $dr = d\theta = d\phi = 0$.

**Step 1:** The line element reduces to:

$$
ds^2 = -\left(1 - \frac{r_s}{r}\right)c^2 dt^2
$$

**Step 2:** Proper time $d\tau = \sqrt{-ds^2}/c$:

$$
d\tau = \sqrt{1 - \frac{r_s}{r}}\, dt
$$

**Step 3:** Integrate:

$$
\Delta\tau = \sqrt{1 - \frac{r_s}{r}}\, \Delta t
$$

Since $\sqrt{1 - r_s/r} < 1$ for $r > r_s$: proper time elapses **slower** than coordinate time. As $r \to r_s$: $\Delta\tau \to 0$ — time "freezes" at the event horizon (as seen by a distant observer). $\blacksquare$

---

### Proof 8.5.3 — Embedding Diagram: Proper Radial Distance

**Setup:** Compute the proper distance from $r_s$ to some radius $R$ in the Schwarzschild geometry (at fixed $t$, $\theta$, $\phi$).

**Step 1:** The spatial line element (equatorial slice, $\theta = \pi/2$, $d\theta = d\phi = 0$):

$$
d\ell^2 = \frac{dr^2}{1 - r_s/r}
$$

**Step 2:** Integrate:

$$
\ell = \int_{r_s}^{R} \frac{dr}{\sqrt{1 - r_s/r}} = \int_{r_s}^{R} \sqrt{\frac{r}{r - r_s}}\, dr
$$

**Step 3:** Substitute $u = r - r_s$, $r = u + r_s$, $dr = du$:

$$
\ell = \int_0^{R-r_s} \sqrt{\frac{u + r_s}{u}}\, du = \int_0^{R-r_s} \sqrt{1 + \frac{r_s}{u}}\, du
$$

**Step 4:** For $R \gg r_s$, approximate: $\ell \approx R - r_s + r_s\ln(R/r_s - 1) + \cdots > R - r_s$.

The proper distance always exceeds the coordinate distance — this is the "stretching" of space near a black hole visualized in embedding diagrams. $\blacksquare$

---

## 🧮 6. Worked Examples

### Example 8.5.1 — Line Element on a 2-Sphere

**Problem:** Write the metric on the unit 2-sphere $S^2$ in spherical coordinates $(\theta, \phi)$ and compute the distance between the north pole and a point at colatitude $\theta_0$.

**Solution:**

The line element on $S^2$ (radius $R$):

$$
ds^2 = R^2(d\theta^2 + \sin^2\theta\, d\phi^2)
$$

Metric tensor: $g_{\theta\theta} = R^2$, $g_{\phi\phi} = R^2\sin^2\theta$, $g_{\theta\phi} = 0$.

Distance from north pole ($\theta = 0$) to $\theta = \theta_0$ along a meridian ($d\phi = 0$):

$$
\ell = \int_0^{\theta_0} \sqrt{g_{\theta\theta}}\, d\theta = \int_0^{\theta_0} R\, d\theta = R\theta_0
$$

For the equator ($\theta_0 = \pi/2$): $\ell = \pi R/2$. For the south pole ($\theta_0 = \pi$): $\ell = \pi R$ (half the circumference).

Circumference at colatitude $\theta_0$: $C = \int_0^{2\pi}\sqrt{g_{\phi\phi}}\, d\phi = 2\pi R\sin\theta_0$.

---

### Example 8.5.2 — Schwarzschild Metric: Coordinate vs. Physical Singularity

**Problem:** The Schwarzschild metric has apparent singularities at $r = 0$ and $r = r_s$. Determine which is a true (curvature) singularity and which is merely a coordinate artifact.

**Solution:**

**Test:** Compute a curvature scalar. The Kretschner scalar is:

$$
K = R_{\mu\nu\alpha\beta}R^{\mu\nu\alpha\beta} = \frac{48 G^2 M^2}{c^4 r^6} = \frac{12 r_s^2}{r^6}
$$

At $r = r_s$: $K = 12/r_s^4$ — **finite**. This is a coordinate singularity (removable by changing to Eddington-Finkelstein or Kruskal-Szekeres coordinates).

At $r = 0$: $K \to \infty$ — **true physical singularity**. Tidal forces diverge; geodesics terminate. This cannot be removed by any coordinate transformation.

---

### Example 8.5.3 — FLRW Metric: Hubble's Law from the Metric

**Problem:** For a flat ($k=0$) FLRW universe with scale factor $a(t)$, derive Hubble's law $v = H_0 d$ for nearby galaxies.

**Solution:**

**Step 1:** The metric: $ds^2 = -c^2 dt^2 + a(t)^2(dr^2 + r^2 d\Omega^2)$.

**Step 2:** A comoving galaxy has fixed coordinate $r$. Its physical distance:

$$
d(t) = a(t) \cdot r
$$

**Step 3:** The recession velocity:

$$
v = \dot{d} = \dot{a}\, r = \frac{\dot{a}}{a}\, (a\, r) = H(t)\, d(t)
$$

where $H(t) = \dot{a}/a$ is the **Hubble parameter**. At the present time: $v = H_0 d$. $\blacksquare$

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- **Previous:** [8.4 - Equivalence Principle & Curved Spacetime](8.4---Equivalence-Principle-&-Curved-Spacetime)
- **Next:** [8.6 - Covariant Derivative & Christoffel Symbols](8.6---Covariant-Derivative-&-Christoffel-Symbols)
- **Differential forms on manifolds:** [1.8 - Exterior Algebra & Differential Forms](1.8---Exterior-Algebra-&-Differential-Forms)
- **Tensor algebra:** [2.8 - SVD & Tensors](2.8---SVD-&-Tensors)
- **Curvature:** [8.7 - Geodesics & Curvature - Riemann & Ricci Tensors](8.7---Geodesics-&-Curvature---Riemann-&-Ricci-Tensors)

### External References
1. **Carroll, S.** (1997). arXiv:gr-qc/9712019. Chapter 2: Manifolds.
2. **Wald, R.M.** (1984). *General Relativity*. University of Chicago Press. Chapters 2–3.
3. **Misner, Thorne & Wheeler** (1973). *Gravitation*. Chapters 8–13.
4. **Nakahara, M.** (2003). *Geometry, Topology and Physics* (2nd ed.). CRC Press.
5. **Susskind, L.** *The Theoretical Minimum: General Relativity*. Lectures 4–5.

---

*Next: [8.6 - Covariant Derivative & Christoffel Symbols](8.6---Covariant-Derivative-&-Christoffel-Symbols) →*



---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.5.E1 — Metric of the 2-Sphere from Embedding in $\mathbb{R}^3$

**Problem:** Derive the metric (first fundamental form) of the 2-sphere $S^2$ of radius $R$ by embedding it in Euclidean $\mathbb{R}^3$ with coordinates $(\theta, \phi)$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Embedding map.**

The 2-sphere of radius $R$ is embedded in $\mathbb{R}^3$ via:

$$
x = R\sin\theta\cos\phi, \qquad y = R\sin\theta\sin\phi, \qquad z = R\cos\theta
$$

where $\theta \in [0, \pi]$ (polar angle) and $\phi \in [0, 2\pi)$ (azimuthal angle).

**Step 2: Compute differentials.**

$$
dx = R\cos\theta\cos\phi\,d\theta - R\sin\theta\sin\phi\,d\phi
$$

$$
dy = R\cos\theta\sin\phi\,d\theta + R\sin\theta\cos\phi\,d\phi
$$

$$
dz = -R\sin\theta\,d\theta
$$

**Step 3: Compute the induced metric $ds^2 = dx^2 + dy^2 + dz^2$.**

$$
dx^2 = R^2\cos^2\theta\cos^2\phi\,d\theta^2 - 2R^2\cos\theta\sin\theta\cos\phi\sin\phi\,d\theta\,d\phi + R^2\sin^2\theta\sin^2\phi\,d\phi^2
$$

$$
dy^2 = R^2\cos^2\theta\sin^2\phi\,d\theta^2 + 2R^2\cos\theta\sin\theta\sin\phi\cos\phi\,d\theta\,d\phi + R^2\sin^2\theta\cos^2\phi\,d\phi^2
$$

$$
dz^2 = R^2\sin^2\theta\,d\theta^2
$$

**Step 4: Add all three.**

The cross terms ($d\theta\,d\phi$) cancel:

$$
-2R^2\cos\theta\sin\theta\cos\phi\sin\phi + 2R^2\cos\theta\sin\theta\sin\phi\cos\phi = 0
$$

The $d\theta^2$ terms:

$$
R^2\cos^2\theta(\cos^2\phi + \sin^2\phi) + R^2\sin^2\theta = R^2(\cos^2\theta + \sin^2\theta) = R^2
$$

The $d\phi^2$ terms:

$$
R^2\sin^2\theta(\sin^2\phi + \cos^2\phi) = R^2\sin^2\theta
$$

**Step 5: Final metric.**

$$
\boxed{ds^2 = R^2\,d\theta^2 + R^2\sin^2\theta\,d\phi^2}
$$

The metric tensor in matrix form:

$$
g_{ab} = \begin{pmatrix} R^2 & 0 \\ 0 & R^2\sin^2\theta \end{pmatrix}
$$

**Properties:**
- Determinant: $\det g = R^4\sin^2\theta$, so $\sqrt{\det g} = R^2\sin\theta$ (the area element is $dA = R^2\sin\theta\,d\theta\,d\phi$).
- Total area: $A = \int_0^{2\pi}\int_0^\pi R^2\sin\theta\,d\theta\,d\phi = 4\pi R^2$. ✓
- The metric is singular at $\theta = 0, \pi$ (coordinate singularity at poles — the azimuthal angle is undefined there).

For the unit sphere ($R = 1$): $ds^2 = d\theta^2 + \sin^2\theta\,d\phi^2$.

</details>

---

### Example 8.5.E2 — FLRW Cosmological Metric: Components and Interpretation

**Problem:** Write down the Friedmann-Lemaître-Robertson-Walker (FLRW) metric for a homogeneous, isotropic universe. Identify the metric components and compute the spatial volume element.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: The FLRW line element.**

The most general metric consistent with spatial homogeneity and isotropy is:

$$
ds^2 = -c^2\,dt^2 + a(t)^2\left[\frac{dr^2}{1 - kr^2} + r^2\,d\theta^2 + r^2\sin^2\theta\,d\phi^2\right]
$$

where:
- $a(t)$ is the **scale factor** (dimensionless, normalized to $a(t_0) = 1$ today)
- $k \in \{-1, 0, +1\}$ is the **spatial curvature** parameter:
  - $k = +1$: closed universe (positive curvature, 3-sphere topology)
  - $k = 0$: flat universe (Euclidean spatial sections)
  - $k = -1$: open universe (negative curvature, hyperbolic spatial sections)
- $r$ is a dimensionless comoving radial coordinate

**Step 2: Metric components.**

Reading off $g_{\mu\nu}$ with coordinates $(x^0, x^1, x^2, x^3) = (ct, r, \theta, \phi)$:

$$
g_{00} = -1, \qquad g_{11} = \frac{a(t)^2}{1 - kr^2}, \qquad g_{22} = a(t)^2 r^2, \qquad g_{33} = a(t)^2 r^2\sin^2\theta
$$

All off-diagonal components vanish: $g_{\mu\nu} = 0$ for $\mu \neq \nu$.

**Step 3: Inverse metric.**

$$
g^{00} = -1, \qquad g^{11} = \frac{1-kr^2}{a^2}, \qquad g^{22} = \frac{1}{a^2 r^2}, \qquad g^{33} = \frac{1}{a^2 r^2\sin^2\theta}
$$

**Step 4: Determinant and volume element.**

$$
\det(g_{\mu\nu}) = (-1)\cdot\frac{a^2}{1-kr^2}\cdot a^2 r^2 \cdot a^2 r^2\sin^2\theta = -\frac{a^6 r^4\sin^2\theta}{1-kr^2}
$$

$$
\sqrt{-g} = \frac{a^3 r^2\sin\theta}{\sqrt{1-kr^2}}
$$

The invariant 4-volume element:

$$
d^4V = \sqrt{-g}\,d(ct)\,dr\,d\theta\,d\phi = \frac{a^3 r^2\sin\theta}{\sqrt{1-kr^2}}\,c\,dt\,dr\,d\theta\,d\phi
$$

The spatial 3-volume element (at fixed $t$):

$$
dV_3 = \frac{a^3 r^2\sin\theta}{\sqrt{1-kr^2}}\,dr\,d\theta\,d\phi
$$

**Step 5: Physical interpretation.**

- The **proper distance** between two comoving observers at $r_1$ and $r_2$ (at fixed $t$, $\theta$, $\phi$):

$$
d_{\text{proper}}(t) = a(t)\int_{r_1}^{r_2}\frac{dr}{\sqrt{1-kr^2}}
$$

This grows with time as $a(t)$ increases — the expansion of the universe.

- The **Hubble parameter**: $H(t) = \dot{a}/a$. The recession velocity of a galaxy at proper distance $d$ is $v = Hd$ (Hubble's law).

- For $k = 0$ (flat): the spatial metric is just $a^2(dr^2 + r^2 d\Omega^2)$ — Euclidean space scaled by $a(t)$.

</details>

---

### Example 8.5.E3 — Flat Torus Metric and Periodic Identification

**Problem:** Construct the metric of a flat 2-torus $T^2$ by periodic identification of a rectangle $[0, L_1] \times [0, L_2]$. Show that the torus is flat (zero curvature) despite being compact.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Construction.**

Start with the Euclidean plane $\mathbb{R}^2$ with metric:

$$
ds^2 = dx^2 + dy^2
$$

Identify points: $(x, y) \sim (x + L_1, y) \sim (x, y + L_2)$.

The resulting space is the flat torus $T^2 = \mathbb{R}^2 / (L_1\mathbb{Z} \times L_2\mathbb{Z})$.

**Step 2: Metric in angular coordinates.**

Define $\phi_1 = 2\pi x/L_1 \in [0, 2\pi)$ and $\phi_2 = 2\pi y/L_2 \in [0, 2\pi)$:

$$
dx = \frac{L_1}{2\pi}d\phi_1, \qquad dy = \frac{L_2}{2\pi}d\phi_2
$$

$$
ds^2 = \left(\frac{L_1}{2\pi}\right)^2 d\phi_1^2 + \left(\frac{L_2}{2\pi}\right)^2 d\phi_2^2
$$

Define $R_1 = L_1/(2\pi)$ and $R_2 = L_2/(2\pi)$:

$$
\boxed{ds^2 = R_1^2\,d\phi_1^2 + R_2^2\,d\phi_2^2}
$$

The metric tensor:

$$
g_{ab} = \begin{pmatrix} R_1^2 & 0 \\ 0 & R_2^2 \end{pmatrix}
$$

**Step 3: Show flatness.**

All metric components are **constants** — they do not depend on the coordinates $(\phi_1, \phi_2)$. Therefore all partial derivatives of $g_{ab}$ vanish:

$$
\partial_c g_{ab} = 0 \quad \forall\, a, b, c
$$

The Christoffel symbols:

$$
\Gamma^a_{bc} = \frac{1}{2}g^{ad}(\partial_b g_{dc} + \partial_c g_{db} - \partial_d g_{bc}) = 0
$$

The Riemann tensor:

$$
R^a{}_{bcd} = \partial_c\Gamma^a_{bd} - \partial_d\Gamma^a_{bc} + \Gamma^a_{ce}\Gamma^e_{bd} - \Gamma^a_{de}\Gamma^e_{bc} = 0
$$

The torus is **intrinsically flat** — zero Gaussian curvature everywhere.

**Step 4: Topology vs. geometry.**

The flat torus is compact (finite area $A = L_1 L_2 = 4\pi^2 R_1 R_2$) but has zero curvature. This shows that **curvature is a local property** while compactness is global (topological). The Gauss-Bonnet theorem for the torus gives:

$$
\int_{T^2} K\,dA = 2\pi\chi(T^2) = 2\pi \times 0 = 0
$$

where $\chi(T^2) = 0$ is the Euler characteristic of the torus. This is consistent with $K = 0$ everywhere.

**Contrast with the 2-sphere:** The sphere has $K = 1/R^2 \gt  0$ everywhere and $\chi(S^2) = 2$, so $\int K\,dA = 4\pi$. The sphere cannot be made flat — its topology forces positive curvature somewhere.

**Note:** The flat torus cannot be isometrically embedded in $\mathbb{R}^3$ without distortion (the "donut" shape of a torus in $\mathbb{R}^3$ has non-zero curvature). It can be embedded in $\mathbb{R}^4$ as $(\cos\phi_1, \sin\phi_1, \cos\phi_2, \sin\phi_2)$ with the induced flat metric.

</details>

---

### Example 8.5.E4 — Line Element in Cylindrical and Spherical Coordinates

**Problem:** Starting from the flat Euclidean metric $ds^2 = dx^2 + dy^2 + dz^2$, derive the line element in (a) cylindrical coordinates $(\rho, \phi, z)$ and (b) spherical coordinates $(r, \theta, \phi)$ by computing the pullback.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**(a) Cylindrical coordinates:** $x = \rho\cos\phi$, $y = \rho\sin\phi$, $z = z$.

**Compute differentials:**

$$
dx = \cos\phi\,d\rho - \rho\sin\phi\,d\phi
$$

$$
dy = \sin\phi\,d\rho + \rho\cos\phi\,d\phi
$$

$$
dz = dz
$$

**Compute $ds^2 = dx^2 + dy^2 + dz^2$:**

$$
dx^2 = \cos^2\phi\,d\rho^2 - 2\rho\sin\phi\cos\phi\,d\rho\,d\phi + \rho^2\sin^2\phi\,d\phi^2
$$

$$
dy^2 = \sin^2\phi\,d\rho^2 + 2\rho\sin\phi\cos\phi\,d\rho\,d\phi + \rho^2\cos^2\phi\,d\phi^2
$$

Adding $dx^2 + dy^2$: cross terms cancel, $\cos^2\phi + \sin^2\phi = 1$:

$$
dx^2 + dy^2 = d\rho^2 + \rho^2\,d\phi^2
$$

$$
\boxed{ds^2_{\text{cyl}} = d\rho^2 + \rho^2\,d\phi^2 + dz^2}
$$

Metric tensor: $g_{ab} = \text{diag}(1, \rho^2, 1)$.

**(b) Spherical coordinates:** $x = r\sin\theta\cos\phi$, $y = r\sin\theta\sin\phi$, $z = r\cos\theta$.

**Compute differentials:**

$$
dx = \sin\theta\cos\phi\,dr + r\cos\theta\cos\phi\,d\theta - r\sin\theta\sin\phi\,d\phi
$$

$$
dy = \sin\theta\sin\phi\,dr + r\cos\theta\sin\phi\,d\theta + r\sin\theta\cos\phi\,d\phi
$$

$$
dz = \cos\theta\,dr - r\sin\theta\,d\theta
$$

**Compute $ds^2$** (collecting by basis 2-forms):

$d r^2$ coefficient: $\sin^2\theta\cos^2\phi + \sin^2\theta\sin^2\phi + \cos^2\theta = \sin^2\theta + \cos^2\theta = 1$

$d\theta^2$ coefficient: $r^2\cos^2\theta\cos^2\phi + r^2\cos^2\theta\sin^2\phi + r^2\sin^2\theta = r^2(\cos^2\theta + \sin^2\theta) = r^2$

$d\phi^2$ coefficient: $r^2\sin^2\theta\sin^2\phi + r^2\sin^2\theta\cos^2\phi + 0 = r^2\sin^2\theta$

Cross terms ($dr\,d\theta$, $dr\,d\phi$, $d\theta\,d\phi$): all cancel by orthogonality of trigonometric functions.

$$
\boxed{ds^2_{\text{sph}} = dr^2 + r^2\,d\theta^2 + r^2\sin^2\theta\,d\phi^2}
$$

Metric tensor: $g_{ab} = \text{diag}(1, r^2, r^2\sin^2\theta)$.

**Volume elements:**

- Cylindrical: $\sqrt{\det g} = \rho$, so $dV = \rho\,d\rho\,d\phi\,dz$
- Spherical: $\sqrt{\det g} = r^2\sin\theta$, so $dV = r^2\sin\theta\,dr\,d\theta\,d\phi$

Both are the familiar results from multivariable calculus, now derived systematically from the metric tensor.

</details>




---

## 📘 9. Appendix: Extended Derivations & Special Cases

### Appendix 9.1 — Tangent Space and Dual Space (Cotangent Space)

**The tangent space $T_pM$** at a point $p$ on a manifold $M$ is the vector space of all tangent vectors at $p$. In coordinates $\{x^\mu\}$, a basis for $T_pM$ is the set of partial derivative operators:

$$
\left\{\frac{\partial}{\partial x^0}\bigg|_p,\; \frac{\partial}{\partial x^1}\bigg|_p,\; \frac{\partial}{\partial x^2}\bigg|_p,\; \frac{\partial}{\partial x^3}\bigg|_p\right\} = \{e_\mu\} = \{\partial_\mu\}
$$

A tangent vector $V \in T_pM$ is:

$$
V = V^\mu\partial_\mu = V^\mu\frac{\partial}{\partial x^\mu}
$$

**Why partial derivatives?** A tangent vector is defined as a **directional derivative operator** on smooth functions. Given a curve $\gamma(\lambda)$ through $p = \gamma(0)$, the tangent vector is:

$$
V[f] = \frac{d}{d\lambda}f(\gamma(\lambda))\bigg|_{\lambda=0} = \frac{dx^\mu}{d\lambda}\frac{\partial f}{\partial x^\mu} = V^\mu\partial_\mu f
$$

This is coordinate-independent: under a change of coordinates $x^\mu \to x'^\nu$:

$$
V = V^\mu\partial_\mu = V^\mu\frac{\partial x'^\nu}{\partial x^\mu}\frac{\partial}{\partial x'^\nu} = V'^\nu\partial'_\nu
$$

with $V'^\nu = V^\mu\frac{\partial x'^\nu}{\partial x^\mu}$ — the contravariant transformation law.

**The cotangent (dual) space $T^*_pM$** is the space of linear maps $\omega: T_pM \to \mathbb{R}$. Its natural basis is the set of differentials $\{dx^\mu\}$, defined by:

$$
dx^\mu(\partial_\nu) = \delta^\mu_\nu
$$

A covector (1-form) $\omega \in T^*_pM$ is:

$$
\omega = \omega_\mu\,dx^\mu
$$

The pairing between a vector and a covector:

$$
\omega(V) = \omega_\mu V^\mu
$$

This is a scalar — invariant under coordinate changes.

**The metric as a map between $T_pM$ and $T^*_pM$.** The metric tensor $g_{\mu\nu}$ provides an isomorphism:

$$
\text{Lowering: } V_\mu = g_{\mu\nu}V^\nu \quad (T_pM \to T^*_pM)
$$

$$
\text{Raising: } \omega^\mu = g^{\mu\nu}\omega_\nu \quad (T^*_pM \to T_pM)
$$

This is why in Euclidean space (where $g_{\mu\nu} = \delta_{\mu\nu}$) we don't distinguish vectors from covectors — the metric is the identity map. In curved spacetime or non-Cartesian coordinates, the distinction is essential.

---

### Appendix 9.2 — Pushforward and Pullback Maps

Given a smooth map $\phi: M \to N$ between manifolds, there are two natural induced maps on tensors:

**Pushforward $\phi_*: T_pM \to T_{\phi(p)}N$** (maps vectors forward):

For $V \in T_pM$ and $f: N \to \mathbb{R}$:

$$
(\phi_* V)[f] = V[f \circ \phi]
$$

In coordinates ($x^\mu$ on $M$, $y^\alpha$ on $N$):

$$
(\phi_* V)^\alpha = \frac{\partial y^\alpha}{\partial x^\mu}V^\mu
$$

The pushforward is the **Jacobian matrix** acting on vectors.

**Pullback $\phi^*: T^*_{\phi(p)}N \to T^*_pM$** (maps covectors backward):

For $\omega \in T^*_{\phi(p)}N$ and $V \in T_pM$:

$$
(\phi^*\omega)(V) = \omega(\phi_* V)
$$

In coordinates:

$$
(\phi^*\omega)_\mu = \frac{\partial y^\alpha}{\partial x^\mu}\omega_\alpha
$$

**Pullback of differential forms.** The pullback extends naturally to $k$-forms:

$$
\phi^*(dy^\alpha \wedge dy^\beta) = \phi^*(dy^\alpha) \wedge \phi^*(dy^\beta) = \left(\frac{\partial y^\alpha}{\partial x^\mu}dx^\mu\right) \wedge \left(\frac{\partial y^\beta}{\partial x^\nu}dx^\nu\right)
$$

This is exactly the change-of-variables formula. For a 2-form $\omega = \frac{1}{2}\omega_{\alpha\beta}\,dy^\alpha\wedge dy^\beta$:

$$
(\phi^*\omega)_{\mu\nu} = \frac{\partial y^\alpha}{\partial x^\mu}\frac{\partial y^\beta}{\partial x^\nu}\omega_{\alpha\beta}
$$

**The induced metric (pullback of the metric).** When $\phi: M \to N$ is an embedding (e.g., a surface in $\mathbb{R}^3$), the induced metric on $M$ is the pullback of the ambient metric:

$$
(\phi^* g)_{\mu\nu} = \frac{\partial y^\alpha}{\partial x^\mu}\frac{\partial y^\beta}{\partial x^\nu}g_{\alpha\beta}
$$

This is precisely what we computed in Example 8.5.E1 when deriving the 2-sphere metric from the Euclidean metric of $\mathbb{R}^3$.

**Key properties:**
- Pullback commutes with exterior derivative: $\phi^*(d\omega) = d(\phi^*\omega)$
- Pullback commutes with wedge product: $\phi^*(\alpha\wedge\beta) = \phi^*\alpha\wedge\phi^*\beta$
- Pushforward does NOT generally exist for covectors (only for vectors along the map)
- Pullback does NOT generally exist for vectors (only for forms)

**References:** Carroll §2.3; Wald §3.1; Nakahara, *Geometry, Topology and Physics* Ch. 5; Tu, *An Introduction to Manifolds* Ch. 3.

