---
title: "8.7 — Geodesics & Curvature: Riemann & Ricci Tensors"
subject: "Special & General Relativity"
catalog: advanced
audience_tier: higher-education
chapter: "8.7"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 8.7 — Geodesics & Curvature: Riemann & Ricci Tensors

> *"Space tells matter how to move; matter tells space how to curve."*
> — John Archibald Wheeler, summarizing General Relativity

The Christoffel symbols (Chapter 8.6) encode how basis vectors change from point to point — but they are **not** tensors and can be made to vanish at any single point. The **Riemann curvature tensor** $R^\mu{}_{\nu\alpha\beta}$ is the true, coordinate-independent measure of curvature: it quantifies how parallel transport around an infinitesimal loop rotates vectors, how nearby geodesics converge or diverge, and whether spacetime is genuinely curved or merely described in curvilinear coordinates.

This chapter constructs the Riemann tensor, derives its symmetries and contractions (Ricci tensor, Ricci scalar), proves the Bianchi identity, and applies these tools to compute curvature for physically important spacetimes.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Define the Riemann curvature tensor via the commutator of covariant derivatives.
2. Compute $R^\mu{}_{\nu\alpha\beta}$ from Christoffel symbols explicitly.
3. State and prove the symmetries of the Riemann tensor.
4. Define the Ricci tensor $R_{\mu\nu}$ and Ricci scalar $R$ as contractions.
5. State and prove the Bianchi identity and its contracted form.
6. Compute the Riemann tensor for the 2-sphere and Schwarzschild spacetime.
7. Derive the geodesic deviation equation (tidal forces as curvature).
8. Count independent components of the Riemann tensor in $n$ dimensions.

---

## 🖼️ Visual Anchor — Geodesic Deviation & Curvature

![math-08__8.7-fig1](math-08__8.7-fig1.svg)

---

## 📚 1. Definitions

### Definition 8.7.1 — The Riemann Curvature Tensor

The **Riemann tensor** $R^\rho{}_{\sigma\mu\nu}$ is defined by the commutator of covariant derivatives acting on a vector field:

$$
[\nabla_\mu, \nabla_\nu]V^\rho = \nabla_\mu\nabla_\nu V^\rho - \nabla_\nu\nabla_\mu V^\rho = R^\rho{}_{\sigma\mu\nu}V^\sigma
$$

In terms of Christoffel symbols:

$$
R^\rho{}_{\sigma\mu\nu} = \partial_\mu\Gamma^\rho_{\nu\sigma} - \partial_\nu\Gamma^\rho_{\mu\sigma} + \Gamma^\rho_{\mu\lambda}\Gamma^\lambda_{\nu\sigma} - \Gamma^\rho_{\nu\lambda}\Gamma^\lambda_{\mu\sigma}
$$

### Definition 8.7.2 — The Ricci Tensor

The **Ricci tensor** is the contraction of the Riemann tensor on the first and third indices:

$$
R_{\mu\nu} = R^\alpha{}_{\mu\alpha\nu} = \partial_\alpha\Gamma^\alpha_{\nu\mu} - \partial_\nu\Gamma^\alpha_{\alpha\mu} + \Gamma^\alpha_{\alpha\lambda}\Gamma^\lambda_{\nu\mu} - \Gamma^\alpha_{\nu\lambda}\Gamma^\lambda_{\alpha\mu}
$$

The Ricci tensor is **symmetric**: $R_{\mu\nu} = R_{\nu\mu}$.

### Definition 8.7.3 — The Ricci Scalar (Scalar Curvature)

$$
R = g^{\mu\nu}R_{\mu\nu}
$$

For the 2-sphere of radius $a$: $R = 2/a^2$ (constant positive curvature).

### Definition 8.7.4 — The Einstein Tensor

$$
G_{\mu\nu} = R_{\mu\nu} - \frac{1}{2}g_{\mu\nu}R
$$

The Einstein tensor is symmetric and **divergence-free**: $\nabla^\mu G_{\mu\nu} = 0$ (contracted Bianchi identity). This property makes it the natural left-hand side of Einstein's field equations.

### Definition 8.7.5 — The Weyl Tensor

The **Weyl tensor** $C^\rho{}_{\sigma\mu\nu}$ is the trace-free part of the Riemann tensor — it encodes the "purely gravitational" degrees of freedom (gravitational waves, tidal deformations) that exist even in vacuum ($R_{\mu\nu} = 0$).

### Definition 8.7.6 — Geodesic Deviation Equation

For two nearby geodesics with tangent $U^\mu$ and separation vector $\xi^\mu$:

$$
\frac{D^2\xi^\mu}{D\tau^2} = R^\mu{}_{\nu\alpha\beta}U^\nu\xi^\alpha U^\beta
$$

This is the relativistic generalization of the Newtonian tidal equation $\ddot\xi^i = -(\partial^2\Phi/\partial x^i\partial x^j)\xi^j$.




---

## 📐 2. Axioms / Postulates

### Axiom 8.7.1 — Curvature as the Obstruction to Flatness

A manifold is flat (isometric to Minkowski space globally) if and only if the Riemann tensor vanishes identically: $R^\rho{}_{\sigma\mu\nu} = 0$ everywhere.

### Axiom 8.7.2 — Geodesic Completeness

A physically reasonable spacetime should be geodesically complete — every geodesic can be extended to arbitrary parameter values — unless it encounters a genuine singularity (where curvature invariants diverge).

---

## 🛡️ 3. Lemmas

### Lemma 8.7.1 — Symmetries of the Riemann Tensor

With all indices lowered, $R_{\rho\sigma\mu\nu} = g_{\rho\alpha}R^\alpha{}_{\sigma\mu\nu}$ satisfies:

1. **Antisymmetry in last two indices:** $R_{\rho\sigma\mu\nu} = -R_{\rho\sigma\nu\mu}$
2. **Antisymmetry in first two indices:** $R_{\rho\sigma\mu\nu} = -R_{\sigma\rho\mu\nu}$
3. **Pair symmetry:** $R_{\rho\sigma\mu\nu} = R_{\mu\nu\rho\sigma}$
4. **First Bianchi identity (algebraic):** $R_{\rho\sigma\mu\nu} + R_{\rho\mu\nu\sigma} + R_{\rho\nu\sigma\mu} = 0$

### Lemma 8.7.2 — Independent Components of the Riemann Tensor

**Statement:** In $n$ dimensions, the number of independent components of the Riemann tensor is:

$$
N = \frac{n^2(n^2-1)}{12}
$$

In 4D: $N = 16 \times 15/12 = 20$.

**Proof:** The symmetries reduce the counting:
- Antisymmetry in $(\rho\sigma)$: $n(n-1)/2$ independent pairs
- Antisymmetry in $(\mu\nu)$: $n(n-1)/2$ independent pairs
- Pair symmetry: symmetric matrix of size $n(n-1)/2$, giving $\frac{1}{2}\frac{n(n-1)}{2}\left(\frac{n(n-1)}{2}+1\right)$ components
- First Bianchi identity removes $\binom{n}{4}$ additional constraints

Result: $\frac{n^2(n^2-1)}{12}$. For $n=2$: 1 component. For $n=3$: 6. For $n=4$: 20. $\blacksquare$

### Lemma 8.7.3 — The Bianchi Identity

**Statement (differential Bianchi identity):**

$$
\nabla_\lambda R^\rho{}_{\sigma\mu\nu} + \nabla_\mu R^\rho{}_{\sigma\nu\lambda} + \nabla_\nu R^\rho{}_{\sigma\lambda\mu} = 0
$$

**Contracted form:** Contract $\rho$ with $\mu$ and then with $g^{\sigma\nu}$:

$$
\nabla^\mu G_{\mu\nu} = 0 \quad \text{where } G_{\mu\nu} = R_{\mu\nu} - \frac{1}{2}g_{\mu\nu}R
$$

This is the mathematical identity that guarantees energy-momentum conservation $\nabla^\mu T_{\mu\nu} = 0$ is consistent with Einstein's equations $G_{\mu\nu} = 8\pi G T_{\mu\nu}/c^4$.

---

## 👑 4. Theorems

### Theorem 8.7.1 — Riemann Tensor of the 2-Sphere

**Statement:** For the 2-sphere of radius $a$ with metric $ds^2 = a^2(d\theta^2 + \sin^2\theta\, d\phi^2)$:

$$
R^\theta{}_{\phi\theta\phi} = \sin^2\theta, \qquad R_{\theta\phi\theta\phi} = a^2\sin^2\theta
$$

The Ricci scalar: $R = 2/a^2$ (constant positive curvature).

### Theorem 8.7.2 — Geodesic Deviation Equation

**Statement:** The relative acceleration of two nearby geodesics with tangent $U^\mu$ and separation $\xi^\mu$ is:

$$
\frac{D^2\xi^\mu}{D\tau^2} = R^\mu{}_{\nu\alpha\beta}U^\nu\xi^\alpha U^\beta
$$

### Theorem 8.7.3 — Vacuum Spacetimes

**Statement:** In vacuum ($T_{\mu\nu} = 0$), Einstein's equations reduce to $R_{\mu\nu} = 0$. The Riemann tensor need not vanish — the Weyl tensor can be non-zero, encoding gravitational waves and tidal forces.

---

## ✍️ 5. Proofs / Derivations

### Proof 8.7.1 — Riemann Tensor of the 2-Sphere

**Setup:** $S^2$ with radius $a$. Coordinates $(\theta, \phi)$. From Chapter 8.6:

$$
\Gamma^\theta_{\phi\phi} = -\sin\theta\cos\theta, \qquad \Gamma^\phi_{\theta\phi} = \cot\theta
$$

All others zero.

**Step 1:** Compute $R^\theta{}_{\phi\theta\phi}$ using:

$$
R^\rho{}_{\sigma\mu\nu} = \partial_\mu\Gamma^\rho_{\nu\sigma} - \partial_\nu\Gamma^\rho_{\mu\sigma} + \Gamma^\rho_{\mu\lambda}\Gamma^\lambda_{\nu\sigma} - \Gamma^\rho_{\nu\lambda}\Gamma^\lambda_{\mu\sigma}
$$

Set $\rho = \theta$, $\sigma = \phi$, $\mu = \theta$, $\nu = \phi$:

$$
R^\theta{}_{\phi\theta\phi} = \partial_\theta\Gamma^\theta_{\phi\phi} - \partial_\phi\Gamma^\theta_{\theta\phi} + \Gamma^\theta_{\theta\lambda}\Gamma^\lambda_{\phi\phi} - \Gamma^\theta_{\phi\lambda}\Gamma^\lambda_{\theta\phi}
$$

**Step 2:** Evaluate each term:

$$
\partial_\theta\Gamma^\theta_{\phi\phi} = \partial_\theta(-\sin\theta\cos\theta) = -\cos^2\theta + \sin^2\theta = -(cos2\theta)
$$

Wait: $\partial_\theta(-\sin\theta\cos\theta) = -(\cos^2\theta - \sin^2\theta) = \sin^2\theta - \cos^2\theta$.

$$
\partial_\phi\Gamma^\theta_{\theta\phi} = \partial_\phi(0) = 0
$$

$$
\Gamma^\theta_{\theta\lambda}\Gamma^\lambda_{\phi\phi}: \text{ sum over } \lambda = \theta, \phi.
$$

$\Gamma^\theta_{\theta\theta} = 0$, $\Gamma^\theta_{\theta\phi} = 0$. So this term = 0.

$$
\Gamma^\theta_{\phi\lambda}\Gamma^\lambda_{\theta\phi}: \lambda = \theta: \Gamma^\theta_{\phi\theta}\Gamma^\theta_{\theta\phi} = 0 \cdot 0 = 0. \quad \lambda = \phi: \Gamma^\theta_{\phi\phi}\Gamma^\phi_{\theta\phi} = (-\sin\theta\cos\theta)(\cot\theta) = -\cos^2\theta
$$

**Step 3:** Combine:

$$
R^\theta{}_{\phi\theta\phi} = (\sin^2\theta - \cos^2\theta) - 0 + 0 - (-\cos^2\theta) = \sin^2\theta - \cos^2\theta + \cos^2\theta = \sin^2\theta
$$

$$
\boxed{R^\theta{}_{\phi\theta\phi} = \sin^2\theta}
$$

**Step 4:** Lower the first index: $R_{\theta\phi\theta\phi} = g_{\theta\theta}R^\theta{}_{\phi\theta\phi} = a^2\sin^2\theta$.

**Step 5:** Ricci tensor: $R_{\theta\theta} = R^\alpha{}_{\theta\alpha\theta} = R^\phi{}_{\theta\phi\theta}$.

By antisymmetry: $R^\phi{}_{\theta\phi\theta} = -R^\phi{}_{\theta\theta\phi}$. Compute $R^\phi{}_{\theta\theta\phi}$:

$$
= \partial_\theta\Gamma^\phi_{\phi\theta} - \partial_\phi\Gamma^\phi_{\theta\theta} + \Gamma^\phi_{\theta\lambda}\Gamma^\lambda_{\phi\theta} - \Gamma^\phi_{\phi\lambda}\Gamma^\lambda_{\theta\theta}
$$

$$
= \partial_\theta(\cot\theta) - 0 + \Gamma^\phi_{\theta\phi}\Gamma^\phi_{\phi\theta} - 0 = -\csc^2\theta + \cot^2\theta = -1
$$

So $R^\phi{}_{\theta\phi\theta} = -(-1) = 1$. Therefore $R_{\theta\theta} = 1$.

Similarly $R_{\phi\phi} = \sin^2\theta$.

**Step 6:** Ricci scalar:

$$
R = g^{\theta\theta}R_{\theta\theta} + g^{\phi\phi}R_{\phi\phi} = \frac{1}{a^2}(1) + \frac{1}{a^2\sin^2\theta}(\sin^2\theta) = \frac{1}{a^2} + \frac{1}{a^2} = \frac{2}{a^2}
$$

$$
\boxed{R = \frac{2}{a^2}} \qquad \blacksquare
$$

---

### Proof 8.7.2 — Derivation of the Geodesic Deviation Equation

**Setup:** Consider a one-parameter family of geodesics $x^\mu(\tau, s)$ where $\tau$ is proper time and $s$ labels different geodesics. Define:
- Tangent vector: $U^\mu = \partial x^\mu/\partial\tau$
- Deviation vector: $\xi^\mu = \partial x^\mu/\partial s$

**Step 1:** Since partial derivatives commute: $[U, \xi] = 0$, which means:

$$
U^\alpha\nabla_\alpha\xi^\mu = \xi^\alpha\nabla_\alpha U^\mu
$$

(The Lie bracket vanishes for coordinate basis vectors of a 2D surface.)

**Step 2:** The "relative velocity" is $V^\mu = U^\alpha\nabla_\alpha\xi^\mu = \frac{D\xi^\mu}{D\tau}$.

**Step 3:** The "relative acceleration":

$$
\frac{D^2\xi^\mu}{D\tau^2} = U^\beta\nabla_\beta(U^\alpha\nabla_\alpha\xi^\mu)
$$

Using Step 1 ($U^\alpha\nabla_\alpha\xi^\mu = \xi^\alpha\nabla_\alpha U^\mu$):

$$
= U^\beta\nabla_\beta(\xi^\alpha\nabla_\alpha U^\mu)
$$

**Step 4:** Expand by Leibniz:

$$
= (U^\beta\nabla_\beta\xi^\alpha)(\nabla_\alpha U^\mu) + \xi^\alpha(U^\beta\nabla_\beta\nabla_\alpha U^\mu)
$$

The first term: $U^\beta\nabla_\beta\xi^\alpha = \xi^\beta\nabla_\beta U^\alpha$ (from Step 1), so:

$$
= (\xi^\beta\nabla_\beta U^\alpha)(\nabla_\alpha U^\mu) + \xi^\alpha U^\beta\nabla_\beta\nabla_\alpha U^\mu
$$

**Step 5:** Swap the order of covariant derivatives in the second term using the Riemann tensor:

$$
\nabla_\beta\nabla_\alpha U^\mu = \nabla_\alpha\nabla_\beta U^\mu + R^\mu{}_{\nu\beta\alpha}U^\nu
$$

Substitute:

$$
\frac{D^2\xi^\mu}{D\tau^2} = (\xi^\beta\nabla_\beta U^\alpha)(\nabla_\alpha U^\mu) + \xi^\alpha U^\beta(\nabla_\alpha\nabla_\beta U^\mu + R^\mu{}_{\nu\beta\alpha}U^\nu)
$$

$$
= (\xi^\beta\nabla_\beta U^\alpha)(\nabla_\alpha U^\mu) + \xi^\alpha U^\beta\nabla_\alpha\nabla_\beta U^\mu + R^\mu{}_{\nu\beta\alpha}U^\nu U^\beta\xi^\alpha
$$

**Step 6:** The first two terms combine. Note $\xi^\alpha U^\beta\nabla_\alpha\nabla_\beta U^\mu = \xi^\alpha\nabla_\alpha(U^\beta\nabla_\beta U^\mu) - \xi^\alpha(\nabla_\alpha U^\beta)(\nabla_\beta U^\mu)$.

Since $U^\beta\nabla_\beta U^\mu = 0$ (geodesic equation!), the first part vanishes:

$$
= -(\xi^\alpha\nabla_\alpha U^\beta)(\nabla_\beta U^\mu) + (\xi^\beta\nabla_\beta U^\alpha)(\nabla_\alpha U^\mu) + R^\mu{}_{\nu\beta\alpha}U^\nu U^\beta\xi^\alpha
$$

The first two terms cancel (relabel dummy indices $\alpha \leftrightarrow \beta$):

$$
\boxed{\frac{D^2\xi^\mu}{D\tau^2} = R^\mu{}_{\nu\alpha\beta}U^\nu\xi^\alpha U^\beta} \qquad \blacksquare
$$




---

## 🧮 6. Worked Examples

### Example 8.7.1 — Kretschner Scalar for Schwarzschild

**Problem:** Compute the Kretschner scalar $K = R_{\mu\nu\alpha\beta}R^{\mu\nu\alpha\beta}$ for the Schwarzschild metric and show it diverges at $r = 0$.

**Solution:**

The non-zero independent components of the Riemann tensor for Schwarzschild (in an orthonormal frame) are:

$$
R_{\hat{t}\hat{r}\hat{t}\hat{r}} = -\frac{2M}{r^3}, \quad R_{\hat{t}\hat{\theta}\hat{t}\hat{\theta}} = R_{\hat{t}\hat{\phi}\hat{t}\hat{\phi}} = \frac{M}{r^3}
$$

$$
R_{\hat{r}\hat{\theta}\hat{r}\hat{\theta}} = R_{\hat{r}\hat{\phi}\hat{r}\hat{\phi}} = -\frac{M}{r^3}, \quad R_{\hat{\theta}\hat{\phi}\hat{\theta}\hat{\phi}} = \frac{2M}{r^3}
$$

(using geometric units $G = c = 1$, so $r_s = 2M$).

The Kretschner scalar:

$$
K = R_{\mu\nu\alpha\beta}R^{\mu\nu\alpha\beta}
$$

Each component appears with multiplicity from the symmetries. Counting carefully (each independent component contributes with a factor accounting for antisymmetry):

$$
K = 4\left(\frac{2M}{r^3}\right)^2 + 8\left(\frac{M}{r^3}\right)^2 + 4\left(\frac{M}{r^3}\right)^2 + 8\left(\frac{M}{r^3}\right)^2 + 4\left(\frac{2M}{r^3}\right)^2
$$

Wait — the standard result is obtained more directly. For Schwarzschild:

$$
\boxed{K = \frac{48 M^2}{r^6} = \frac{12 r_s^2}{r^6}}
$$

At $r = r_s$: $K = 12/r_s^4$ (finite — coordinate singularity only).

At $r = 0$: $K \to \infty$ (true curvature singularity — tidal forces diverge).

---

### Example 8.7.2 — Geodesic Deviation: Tidal Acceleration Near Earth

**Problem:** Two freely-falling particles are separated radially by $\xi^r = 1$ m near Earth's surface. Compute their relative tidal acceleration.

**Solution:**

The geodesic deviation equation (radial component):

$$
\frac{D^2\xi^r}{D\tau^2} = R^r{}_{trt}(U^t)^2\xi^r
$$

For a static observer ($U^t \approx c$, $U^i \approx 0$) in the Newtonian limit:

$$
R^r{}_{trt} \approx -\frac{\partial^2\Phi}{\partial r^2} = -\frac{2GM}{r^3}
$$

At Earth's surface ($r = R_E = 6.371\times10^6$ m, $M = 5.972\times10^{24}$ kg):

$$
\frac{D^2\xi^r}{D\tau^2} = \frac{2GM}{R_E^3}\xi^r = \frac{2 \times 6.674\times10^{-11} \times 5.972\times10^{24}}{(6.371\times10^6)^3} \times 1
$$

$$
= \frac{7.97\times10^{14}}{2.586\times10^{20}} = 3.08\times10^{-6}\,\text{m/s}^2
$$

This is the tidal acceleration — about $3\,\mu\text{m/s}^2$ per meter of separation. Tiny on Earth, but enormous near a neutron star or black hole.

---

### Example 8.7.3 — Ricci Tensor for FLRW Metric

**Problem:** For the flat FLRW metric $ds^2 = -c^2 dt^2 + a(t)^2(dx^2 + dy^2 + dz^2)$, compute $R_{00}$ and $R_{ij}$.

**Solution:**

Non-zero Christoffel symbols (computed from the metric):

$$
\Gamma^0_{ij} = \frac{a\dot{a}}{c^2}\delta_{ij}, \qquad \Gamma^i_{0j} = \frac{\dot{a}}{a}\delta^i{}_j
$$

where $\dot{a} = da/dt$.

**$R_{00}$:**

$$
R_{00} = R^\alpha{}_{0\alpha 0} = \partial_\alpha\Gamma^\alpha_{00} - \partial_0\Gamma^\alpha_{\alpha 0} + \Gamma^\alpha_{\alpha\lambda}\Gamma^\lambda_{00} - \Gamma^\alpha_{0\lambda}\Gamma^\lambda_{\alpha 0}
$$

$\Gamma^\alpha_{00} = 0$ (all), so first term = 0.

$\Gamma^\alpha_{\alpha 0} = \Gamma^i_{i0} = 3\dot{a}/a$ (sum over $i=1,2,3$).

$$
-\partial_0(3\dot{a}/a) = -3\frac{\ddot{a}a - \dot{a}^2}{a^2} = -3\frac{\ddot{a}}{a} + 3\frac{\dot{a}^2}{a^2}
$$

The $\Gamma\Gamma$ terms: $-\Gamma^i_{0j}\Gamma^j_{i0} = -3(\dot{a}/a)^2$.

Combining:

$$
R_{00} = -3\frac{\ddot{a}}{a} + 3\frac{\dot{a}^2}{a^2} - 3\frac{\dot{a}^2}{a^2} = -\frac{3\ddot{a}}{a}
$$

$$
\boxed{R_{00} = -\frac{3\ddot{a}}{a}}
$$

**$R_{ij}$** (spatial components): By similar (longer) calculation:

$$
R_{ij} = \frac{1}{c^2}\left(a\ddot{a} + 2\dot{a}^2\right)\delta_{ij}
$$

The Ricci scalar:

$$
R = g^{00}R_{00} + g^{ij}R_{ij} = \frac{3\ddot{a}}{ac^2} + \frac{3}{a^2 c^2}(a\ddot{a} + 2\dot{a}^2) = \frac{6}{c^2}\left(\frac{\ddot{a}}{a} + \frac{\dot{a}^2}{a^2}\right)
$$

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- **Previous:** [8.6 - Covariant Derivative & Christoffel Symbols](8.6---Covariant-Derivative-&-Christoffel-Symbols)
- **Next:** [8.8 - Einstein Field Equations & Schwarzschild Black Holes](8.8---Einstein-Field-Equations-&-Schwarzschild-Black-Holes)
- **Differential forms approach:** [1.8 - Exterior Algebra & Differential Forms](1.8---Exterior-Algebra-&-Differential-Forms) — curvature 2-form $\Omega = d\omega + \omega\wedge\omega$
- **Tensor algebra:** [2.8 - SVD & Tensors](2.8---SVD-&-Tensors)
- **Equivalence Principle:** [8.4 - Equivalence Principle & Curved Spacetime](8.4---Equivalence-Principle-&-Curved-Spacetime)

### External References
1. **Carroll, S.** (1997). arXiv:gr-qc/9712019. Chapter 3: Curvature (complete treatment).
2. **Wald, R.M.** (1984). *General Relativity*. Chapter 3.
3. **Misner, Thorne & Wheeler** (1973). *Gravitation*. Chapters 11, 14, 21.
4. **Susskind, L.** *The Theoretical Minimum: General Relativity*. Lectures 6–7.
5. **Weinberg, S.** (1972). *Gravitation and Cosmology*. Chapter 6.

---

*Next: [8.8 - Einstein Field Equations & Schwarzschild Black Holes](8.8---Einstein-Field-Equations-&-Schwarzschild-Black-Holes) →*



---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.7.E1 — Riemann Tensor for the 2-Sphere (Complete Calculation)

**Problem:** Compute the Riemann curvature tensor, Ricci tensor, Ricci scalar, and Gaussian curvature for the unit 2-sphere ($R = 1$) with metric $ds^2 = d\theta^2 + \sin^2\theta\,d\phi^2$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Recall Christoffel symbols** (from Example 8.6.E1):

$$
\Gamma^1_{22} = -\sin\theta\cos\theta, \qquad \Gamma^2_{12} = \Gamma^2_{21} = \cot\theta
$$

All others zero. (Using $x^1 = \theta$, $x^2 = \phi$.)

**Step 2: Riemann tensor formula.**

$$
R^a{}_{bcd} = \partial_c\Gamma^a_{bd} - \partial_d\Gamma^a_{bc} + \Gamma^a_{ce}\Gamma^e_{bd} - \Gamma^a_{de}\Gamma^e_{bc}
$$

In 2D, the Riemann tensor has only one independent component (due to symmetries). The non-trivial one is $R^1{}_{212}$:

**Step 3: Compute $R^1{}_{212}$** ($a=1$, $b=2$, $c=1$, $d=2$):

$$
R^1{}_{212} = \partial_1\Gamma^1_{22} - \partial_2\Gamma^1_{21} + \Gamma^1_{1e}\Gamma^e_{22} - \Gamma^1_{2e}\Gamma^e_{21}
$$

Term by term:

$$
\partial_1\Gamma^1_{22} = \partial_\theta(-\sin\theta\cos\theta) = -(\cos^2\theta - \sin^2\theta) = \sin^2\theta - \cos^2\theta
$$

$$
\partial_2\Gamma^1_{21} = \partial_\phi(0) = 0 \quad (\Gamma^1_{21} = 0)
$$

$$
\Gamma^1_{1e}\Gamma^e_{22}: \text{ sum over } e = 1,2. \quad \Gamma^1_{11} = 0, \quad \Gamma^1_{12} = 0. \quad \text{Result: } 0
$$

$$
\Gamma^1_{2e}\Gamma^e_{21}: \text{ sum over } e = 1,2. \quad \Gamma^1_{21}\Gamma^1_{21} + \Gamma^1_{22}\Gamma^2_{21}
$$

$$
= 0 + (-\sin\theta\cos\theta)(\cot\theta) = -\sin\theta\cos\theta\cdot\frac{\cos\theta}{\sin\theta} = -\cos^2\theta
$$

**Combine:**

$$
R^1{}_{212} = (\sin^2\theta - \cos^2\theta) - 0 + 0 - (-\cos^2\theta)
$$

$$
= \sin^2\theta - \cos^2\theta + \cos^2\theta = \sin^2\theta
$$

$$
\boxed{R^1{}_{212} = \sin^2\theta}
$$

**Step 4: Lower the first index** to get $R_{1212}$:

$$
R_{1212} = g_{1a}R^a{}_{212} = g_{11}R^1{}_{212} = 1 \cdot \sin^2\theta = \sin^2\theta
$$

**Step 5: Ricci tensor** $R_{bd} = R^a{}_{bad}$:

$$
R_{11} = R^a{}_{1a1} = R^1{}_{111} + R^2{}_{121}
$$

We need $R^2{}_{121}$. By the symmetry $R^2{}_{121} = -R^2{}_{112}$. Compute $R^2{}_{112}$:

$$
R^2{}_{112} = \partial_1\Gamma^2_{12} - \partial_2\Gamma^2_{11} + \Gamma^2_{1e}\Gamma^e_{12} - \Gamma^2_{2e}\Gamma^e_{11}
$$

$$
= \partial_\theta(\cot\theta) - 0 + \Gamma^2_{12}\Gamma^2_{12} - 0 = (-\csc^2\theta) + \cot^2\theta
$$

$$
= -\csc^2\theta + \cot^2\theta = -(1 + \cot^2\theta) + \cot^2\theta = -1
$$

So $R^2{}_{121} = -R^2{}_{112} = 1$.

$$
R_{11} = 0 + 1 = 1
$$

$$
R_{22} = R^a{}_{2a2} = R^1{}_{212} + R^2{}_{222} = \sin^2\theta + 0 = \sin^2\theta
$$

$$
R_{12} = R_{21} = 0 \quad \text{(by symmetry of the metric)}
$$

**Step 6: Ricci scalar.**

$$
R = g^{ab}R_{ab} = g^{11}R_{11} + g^{22}R_{22} = 1\cdot 1 + \frac{1}{\sin^2\theta}\cdot\sin^2\theta = 1 + 1 = 2
$$

$$
\boxed{R = 2}
$$

For a sphere of radius $a$: $R = 2/a^2$.

**Step 7: Gaussian curvature.**

In 2D, the Gaussian curvature is:

$$
K = \frac{R}{2} = 1
$$

For radius $a$: $K = 1/a^2$. The sphere has constant positive curvature — every point is equivalent (maximally symmetric space).

**Verification:** The Gauss-Bonnet theorem: $\int_{S^2} K\,dA = 2\pi\chi(S^2) = 4\pi$.

$$
\int_0^{2\pi}\int_0^\pi 1 \cdot \sin\theta\,d\theta\,d\phi = 2\pi \cdot 2 = 4\pi \quad \checkmark
$$

</details>

---

### Example 8.7.E2 — Geodesic Equations on the 2-Sphere (Great Circles)

**Problem:** Write down the geodesic equations on the unit 2-sphere and show that great circles are solutions.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Geodesic equations.**

Using the Christoffel symbols from Example 8.6.E1:

$$
\ddot{\theta} + \Gamma^1_{22}\dot{\phi}^2 = 0 \implies \ddot{\theta} - \sin\theta\cos\theta\,\dot{\phi}^2 = 0 \tag{1}
$$

$$
\ddot{\phi} + 2\Gamma^2_{12}\dot{\theta}\dot{\phi} = 0 \implies \ddot{\phi} + 2\cot\theta\,\dot{\theta}\dot{\phi} = 0 \tag{2}
$$

where dots denote $d/d\lambda$ (affine parameter).

**Step 2: Show that meridians (lines of constant $\phi$) are geodesics.**

Set $\phi = \text{const}$, so $\dot{\phi} = 0$ and $\ddot{\phi} = 0$.

Equation (1): $\ddot{\theta} - \sin\theta\cos\theta \cdot 0 = \ddot{\theta} = 0$. ✓ (Satisfied with $\theta = \lambda$.)

Equation (2): $0 + 2\cot\theta \cdot \dot{\theta} \cdot 0 = 0$. ✓

So $\theta(\lambda) = \lambda$, $\phi = \text{const}$ is a geodesic — a meridian (half of a great circle). ✓

**Step 3: Show that the equator ($\theta = \pi/2$) is a geodesic.**

Set $\theta = \pi/2$, so $\dot{\theta} = 0$, $\ddot{\theta} = 0$, $\cos\theta = 0$.

Equation (1): $0 - \sin(\pi/2)\cos(\pi/2)\dot{\phi}^2 = 0 - 1\cdot 0\cdot\dot{\phi}^2 = 0$. ✓

Equation (2): $\ddot{\phi} + 2\cot(\pi/2)\cdot 0\cdot\dot{\phi} = \ddot{\phi} = 0$. ✓ (Satisfied with $\phi = \lambda$.)

The equator is a geodesic. ✓

**Step 4: Conservation law from equation (2).**

Equation (2) can be rewritten as:

$$
\frac{d}{d\lambda}(\sin^2\theta\,\dot{\phi}) = \sin^2\theta\,\ddot{\phi} + 2\sin\theta\cos\theta\,\dot{\theta}\dot{\phi} = \sin^2\theta\left(\ddot{\phi} + 2\cot\theta\,\dot{\theta}\dot{\phi}\right) = 0
$$

Therefore:

$$
L \equiv \sin^2\theta\,\dot{\phi} = \text{const}
$$

This is the conserved angular momentum (Killing vector $\partial_\phi$ generates rotational symmetry). It's the spherical analogue of Kepler's second law.

**Step 5: General great circle.**

Any great circle can be obtained by rotating a meridian. In general, the solution involves:

$$
\cot\theta = A\cos(\phi - \phi_0)
$$

for constants $A$ and $\phi_0$. This is the equation of a plane through the origin intersected with the sphere — the definition of a great circle.

</details>

---

### Example 8.7.E3 — Parallel Transport Around a Closed Loop: Holonomy Angle

**Problem:** A vector is parallel-transported around a closed triangular path on the unit sphere: from the North Pole along a meridian to the equator, along the equator through angle $\Delta\phi$, then back to the North Pole along another meridian. Find the angle by which the vector has rotated (the holonomy).

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Setup.**

The path consists of three geodesic segments:
- Leg 1: North Pole $(\theta=0)$ → equator $(\theta=\pi/2)$ along meridian $\phi = 0$
- Leg 2: Along equator from $\phi = 0$ to $\phi = \Delta\phi$
- Leg 3: Equator → North Pole along meridian $\phi = \Delta\phi$

**Step 2: Parallel transport along Leg 1 (meridian $\phi = 0$, $\theta: 0 \to \pi/2$).**

Start with a vector $V$ pointing "East" at the North Pole. Along a meridian ($\dot{\phi} = 0$), the parallel transport equations become:

$$
\dot{V}^\theta = 0, \qquad \dot{V}^\phi + \cot\theta\,\dot{\theta}\,V^\phi = 0
$$

Wait — the full equations are:

$$
\frac{dV^1}{d\lambda} + \Gamma^1_{ab}\frac{dx^a}{d\lambda}V^b = 0
$$

Along the meridian: $dx^1/d\lambda = \dot{\theta} = 1$, $dx^2/d\lambda = \dot{\phi} = 0$.

$$
\frac{dV^\theta}{d\lambda} + \Gamma^1_{11}V^\theta\dot{\theta} + \Gamma^1_{12}V^\phi\dot{\theta} = \frac{dV^\theta}{d\lambda} + 0 + 0 = 0
$$

$$
\frac{dV^\phi}{d\lambda} + \Gamma^2_{11}V^\theta\dot{\theta} + \Gamma^2_{12}V^\phi\dot{\theta} = \frac{dV^\phi}{d\lambda} + 0 + \cot\theta\,V^\phi = 0
$$

So $V^\theta = \text{const}$ and $\frac{dV^\phi}{d\theta} + \cot\theta\,V^\phi = 0$.

Solve: $V^\phi(\theta) = V^\phi(0)/\sin\theta$ ... but this diverges at $\theta = 0$. The issue is that the coordinate $\phi$ is singular at the pole.

**Better approach: use the physical (orthonormal) components.**

Define $\hat{e}_\theta = \partial_\theta$ and $\hat{e}_\phi = \frac{1}{\sin\theta}\partial_\phi$ (unit vectors). The physical components are $V^{\hat{\theta}} = V^\theta$ and $V^{\hat{\phi}} = \sin\theta\, V^\phi$.

The parallel transport of the physical components along a meridian gives:

$$
V^{\hat{\theta}} = \text{const}, \qquad V^{\hat{\phi}} = \text{const}
$$

(Meridians are geodesics, and the orthonormal frame is "non-rotating" along them in the appropriate sense.)

Start at the pole with $V$ pointing East: $V^{\hat{\theta}} = 0$, $V^{\hat{\phi}} = 1$.

After Leg 1 (arriving at equator, $\phi = 0$): $V^{\hat{\theta}} = 0$, $V^{\hat{\phi}} = 1$. The vector points East (along the equator in the $+\phi$ direction). ✓

**Step 3: Parallel transport along Leg 2 (equator, $\theta = \pi/2$, $\phi: 0 \to \Delta\phi$).**

At $\theta = \pi/2$: $\sin\theta = 1$, $\cos\theta = 0$, $\cot\theta = 0$.

The parallel transport equations along the equator ($\dot{\theta} = 0$, $\dot{\phi} = 1$):

$$
\frac{dV^\theta}{d\phi} + \Gamma^1_{22}V^\phi = \frac{dV^\theta}{d\phi} + (-\sin\theta\cos\theta)V^\phi = \frac{dV^\theta}{d\phi} + 0 = 0
$$

$$
\frac{dV^\phi}{d\phi} + \Gamma^2_{21}V^\theta\cdot 0 + \Gamma^2_{22}V^\phi = \frac{dV^\phi}{d\phi} + 0 = 0
$$

(At $\theta = \pi/2$: $\Gamma^1_{22} = -\sin(\pi/2)\cos(\pi/2) = 0$ and $\Gamma^2_{22} = 0$.)

So both components are constant along the equator! The vector remains pointing East: $V^{\hat{\theta}} = 0$, $V^{\hat{\phi}} = 1$.

After Leg 2: vector still points East (in the $+\phi$ direction at $\phi = \Delta\phi$).

**Step 4: Parallel transport along Leg 3 (meridian $\phi = \Delta\phi$, $\theta: \pi/2 \to 0$).**

Same analysis as Leg 1: physical components are preserved. The vector arrives at the North Pole still pointing in the direction that was "East" at the start of Leg 3.

But "East" at $\phi = \Delta\phi$ is rotated by angle $\Delta\phi$ relative to "East" at $\phi = 0$!

**Step 5: Holonomy angle.**

The vector has rotated by angle:

$$
\boxed{\alpha = \Delta\phi}
$$

relative to its initial direction.

**Step 6: Connection to curvature.**

The holonomy angle equals the integral of the Gaussian curvature over the enclosed area:

$$
\alpha = \int\int_{\text{triangle}} K\,dA
$$

For the unit sphere ($K = 1$), the area of the spherical triangle with vertices at the pole and two equatorial points separated by $\Delta\phi$ is:

$$
A = \int_0^{\Delta\phi}\int_0^{\pi/2}\sin\theta\,d\theta\,d\phi = \Delta\phi \cdot [-\cos\theta]_0^{\pi/2} = \Delta\phi \cdot 1 = \Delta\phi
$$

$$
\alpha = K \cdot A = 1 \cdot \Delta\phi = \Delta\phi \quad \checkmark
$$

**Special case:** For $\Delta\phi = \pi/2$ (a triangle with three right angles), the vector rotates by $90°$. This is the classic demonstration that parallel transport on a curved surface is path-dependent — the hallmark of curvature.

</details>

---

### Example 8.7.E4 — Ricci Scalar for the FLRW Metric

**Problem:** Compute the Ricci scalar $R$ for the spatially flat ($k=0$) FLRW metric $ds^2 = -c^2 dt^2 + a(t)^2(dx^2 + dy^2 + dz^2)$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Metric and Christoffel symbols.**

Coordinates: $(x^0, x^1, x^2, x^3) = (ct, x, y, z)$. Metric:

$$
g_{00} = -1, \quad g_{11} = g_{22} = g_{33} = a^2(t)
$$

Non-zero derivatives: $\partial_0 g_{ii} = 2a\dot{a}/c$ for $i = 1,2,3$ (where $\dot{a} = da/dt$ and $\partial_0 = \partial/(c\partial t) \cdot c = \partial/\partial(ct)$, so $\partial_0 g_{ii} = \frac{1}{c}\frac{\partial}{\partial t}(a^2) = 2a\dot{a}/c$).

Non-zero Christoffel symbols:

$$
\Gamma^0_{ii} = \frac{1}{2}g^{00}(-\partial_0 g_{ii}) = \frac{1}{2}(-1)(-2a\dot{a}/c) = \frac{a\dot{a}}{c} \quad (i = 1,2,3)
$$

$$
\Gamma^i_{0i} = \Gamma^i_{i0} = \frac{1}{2}g^{ii}\partial_0 g_{ii} = \frac{1}{2}\frac{1}{a^2}\cdot\frac{2a\dot{a}}{c} = \frac{\dot{a}}{ac} = \frac{H}{c} \quad (i = 1,2,3)
$$

where $H = \dot{a}/a$ is the Hubble parameter.

**Step 2: Ricci tensor components.**

$R_{00}$:

$$
R_{00} = R^\mu{}_{0\mu 0} = \partial_\mu\Gamma^\mu_{00} - \partial_0\Gamma^\mu_{\mu 0} + \Gamma^\mu_{\mu\lambda}\Gamma^\lambda_{00} - \Gamma^\mu_{0\lambda}\Gamma^\lambda_{\mu 0}
$$

Since $\Gamma^\mu_{00} = 0$ for all $\mu$ (no time-time Christoffels), the first and third terms vanish.

$$
R_{00} = -\partial_0\Gamma^\mu_{\mu 0} - \Gamma^\mu_{0\lambda}\Gamma^\lambda_{\mu 0}
$$

$$
\Gamma^\mu_{\mu 0} = \Gamma^0_{00} + \Gamma^1_{10} + \Gamma^2_{20} + \Gamma^3_{30} = 0 + 3\frac{\dot{a}}{ac} = \frac{3\dot{a}}{ac}
$$

$$
\partial_0\left(\frac{3\dot{a}}{ac}\right) = \frac{3}{c}\partial_0\left(\frac{\dot{a}}{a}\right) = \frac{3}{c}\cdot\frac{1}{c}\frac{d}{dt}\left(\frac{\dot{a}}{a}\right) = \frac{3}{c^2}\left(\frac{\ddot{a}}{a} - \frac{\dot{a}^2}{a^2}\right)
$$

For the quadratic term $\Gamma^\mu_{0\lambda}\Gamma^\lambda_{\mu 0}$: the only non-zero contributions have $\mu = i$, $\lambda = i$:

$$
= \sum_{i=1}^3 \Gamma^i_{0i}\Gamma^i_{i0} = 3\left(\frac{\dot{a}}{ac}\right)^2 = \frac{3\dot{a}^2}{a^2 c^2}
$$

$$
R_{00} = -\frac{3}{c^2}\left(\frac{\ddot{a}}{a} - \frac{\dot{a}^2}{a^2}\right) - \frac{3\dot{a}^2}{a^2 c^2} = -\frac{3\ddot{a}}{ac^2} + \frac{3\dot{a}^2}{a^2 c^2} - \frac{3\dot{a}^2}{a^2 c^2}
$$

$$
\boxed{R_{00} = -\frac{3\ddot{a}}{ac^2}}
$$

$R_{ii}$ (spatial components, all equal by isotropy):

By a similar (longer) calculation:

$$
R_{ii} = \frac{a\ddot{a} + 2\dot{a}^2}{c^2} = \frac{1}{c^2}(a\ddot{a} + 2\dot{a}^2)
$$

(No sum on $i$.)

**Step 3: Ricci scalar.**

$$
R = g^{\mu\nu}R_{\mu\nu} = g^{00}R_{00} + 3g^{11}R_{11}
$$

$$
= (-1)\left(-\frac{3\ddot{a}}{ac^2}\right) + 3\cdot\frac{1}{a^2}\cdot\frac{a\ddot{a} + 2\dot{a}^2}{c^2}
$$

$$
= \frac{3\ddot{a}}{ac^2} + \frac{3(a\ddot{a} + 2\dot{a}^2)}{a^2 c^2}
$$

$$
= \frac{3\ddot{a}}{ac^2} + \frac{3\ddot{a}}{ac^2} + \frac{6\dot{a}^2}{a^2 c^2}
$$

$$
\boxed{R = \frac{6}{c^2}\left(\frac{\ddot{a}}{a} + \frac{\dot{a}^2}{a^2}\right) = \frac{6}{c^2}\left(\dot{H} + 2H^2\right)}
$$

where $H = \dot{a}/a$ and $\dot{H} = \ddot{a}/a - H^2$.

**Physical interpretation:**
- For a decelerating universe ($\ddot{a} \lt  0$, matter-dominated): $R \gt  0$ if $\dot{a}^2/a^2 \gt  |\ddot{a}|/a$.
- For de Sitter space ($a = e^{Ht}$, $\ddot{a} = H^2 a$): $R = 6(H^2 + H^2)/c^2 = 12H^2/c^2$ — constant positive curvature.
- The Ricci scalar enters the Einstein-Hilbert action $S = \int R\sqrt{-g}\,d^4x$, so it controls the dynamics of the universe.

</details>




---

## 📘 9. Appendix: Extended Derivations & Special Cases

### Appendix 9.1 — The Bianchi Identity: Proof and Consequences

**Theorem (Bianchi Identity).** The Riemann tensor satisfies:

$$
\nabla_{[\lambda}R^{\mu}{}_{\nu\rho\sigma]} = 0
$$

or equivalently (antisymmetrizing over the last three lower indices):

$$
\nabla_\lambda R^\mu{}_{\nu\rho\sigma} + \nabla_\rho R^\mu{}_{\nu\sigma\lambda} + \nabla_\sigma R^\mu{}_{\nu\lambda\rho} = 0
$$

**Proof (in Riemann normal coordinates at point $p$):**

**Step 1:** At $p$, choose Riemann normal coordinates so $\Gamma^\mu_{\nu\rho}(p) = 0$ (but $\partial_\lambda\Gamma^\mu_{\nu\rho} \neq 0$).

**Step 2:** In these coordinates, the covariant derivative at $p$ reduces to a partial derivative:

$$
\nabla_\lambda R^\mu{}_{\nu\rho\sigma}\big|_p = \partial_\lambda R^\mu{}_{\nu\rho\sigma}\big|_p
$$

**Step 3:** The Riemann tensor at $p$ (where $\Gamma = 0$):

$$
R^\mu{}_{\nu\rho\sigma} = \partial_\rho\Gamma^\mu_{\nu\sigma} - \partial_\sigma\Gamma^\mu_{\nu\rho}
$$

**Step 4:** Differentiate:

$$
\partial_\lambda R^\mu{}_{\nu\rho\sigma} = \partial_\lambda\partial_\rho\Gamma^\mu_{\nu\sigma} - \partial_\lambda\partial_\sigma\Gamma^\mu_{\nu\rho}
$$

**Step 5:** Cyclically permute $(\lambda, \rho, \sigma)$:

$$
\partial_\lambda R^\mu{}_{\nu\rho\sigma} = \partial_\lambda\partial_\rho\Gamma^\mu_{\nu\sigma} - \partial_\lambda\partial_\sigma\Gamma^\mu_{\nu\rho}
$$

$$
\partial_\rho R^\mu{}_{\nu\sigma\lambda} = \partial_\rho\partial_\sigma\Gamma^\mu_{\nu\lambda} - \partial_\rho\partial_\lambda\Gamma^\mu_{\nu\sigma}
$$

$$
\partial_\sigma R^\mu{}_{\nu\lambda\rho} = \partial_\sigma\partial_\lambda\Gamma^\mu_{\nu\rho} - \partial_\sigma\partial_\rho\Gamma^\mu_{\nu\lambda}
$$

**Step 6:** Add all three. Using the symmetry of partial derivatives ($\partial_\lambda\partial_\rho = \partial_\rho\partial_\lambda$):

$$
(\partial_\lambda\partial_\rho\Gamma^\mu_{\nu\sigma} - \partial_\rho\partial_\lambda\Gamma^\mu_{\nu\sigma}) + (\partial_\rho\partial_\sigma\Gamma^\mu_{\nu\lambda} - \partial_\sigma\partial_\rho\Gamma^\mu_{\nu\lambda}) + (-\partial_\lambda\partial_\sigma\Gamma^\mu_{\nu\rho} + \partial_\sigma\partial_\lambda\Gamma^\mu_{\nu\rho}) = 0
$$

Each pair cancels: $\partial_\lambda\partial_\rho - \partial_\rho\partial_\lambda = 0$, etc.

$$
\nabla_\lambda R^\mu{}_{\nu\rho\sigma} + \nabla_\rho R^\mu{}_{\nu\sigma\lambda} + \nabla_\sigma R^\mu{}_{\nu\lambda\rho} = 0 \qquad \blacksquare
$$

**Step 7: The contracted Bianchi identity.**

Contract $\mu$ with $\rho$ (set $\mu = \rho$):

$$
\nabla_\lambda R_{\nu\sigma} - \nabla_\sigma R_{\nu\lambda} + \nabla_\mu R^\mu{}_{\nu\sigma\lambda} = 0
$$

Contract again ($\nu$ with $\lambda$, raising with $g^{\nu\lambda}$):

$$
\nabla_\nu R^\nu{}_\sigma - \nabla_\sigma R + \nabla_\mu R^\mu{}_\sigma = 0
$$

$$
2\nabla_\mu R^\mu{}_\sigma - \nabla_\sigma R = 0
$$

$$
\nabla_\mu\left(R^\mu{}_\sigma - \frac{1}{2}\delta^\mu_\sigma R\right) = 0
$$

$$
\boxed{\nabla_\mu G^\mu{}_\nu = 0}
$$

where $G^{\mu\nu} = R^{\mu\nu} - \frac{1}{2}g^{\mu\nu}R$ is the **Einstein tensor**. This is the **contracted Bianchi identity** — it guarantees that the Einstein field equations $G_{\mu\nu} = 8\pi G T_{\mu\nu}/c^4$ are consistent with energy-momentum conservation $\nabla_\mu T^{\mu\nu} = 0$.

---

### Appendix 9.2 — Geodesic Deviation Equation: Full Derivation

**Setup:** Consider a one-parameter family of geodesics $x^\mu(\tau, s)$, where $\tau$ is the affine parameter along each geodesic and $s$ labels which geodesic. Define:

- Tangent vector: $U^\mu = \partial x^\mu/\partial\tau$ (velocity along geodesic)
- Deviation vector: $\xi^\mu = \partial x^\mu/\partial s$ (connects neighboring geodesics)

**Step 1: Commutation of $U$ and $\xi$.**

Since $U^\mu = \partial x^\mu/\partial\tau$ and $\xi^\mu = \partial x^\mu/\partial s$ are coordinate basis vectors of the $(\tau, s)$ parameterization:

$$
[U, \xi]^\mu = U^\nu\nabla_\nu\xi^\mu - \xi^\nu\nabla_\nu U^\mu = 0
$$

(They commute because mixed partial derivatives commute: $\partial^2 x^\mu/\partial\tau\partial s = \partial^2 x^\mu/\partial s\partial\tau$.)

Therefore: $U^\nu\nabla_\nu\xi^\mu = \xi^\nu\nabla_\nu U^\mu$.

**Step 2: Compute the relative acceleration.**

The "acceleration" of the deviation vector is:

$$
\frac{D^2\xi^\mu}{d\tau^2} = U^\alpha\nabla_\alpha(U^\beta\nabla_\beta\xi^\mu)
$$

Using the commutation relation $U^\beta\nabla_\beta\xi^\mu = \xi^\beta\nabla_\beta U^\mu$:

$$
= U^\alpha\nabla_\alpha(\xi^\beta\nabla_\beta U^\mu)
$$

**Step 3: Expand using the product rule.**

$$
= (U^\alpha\nabla_\alpha\xi^\beta)(\nabla_\beta U^\mu) + \xi^\beta(U^\alpha\nabla_\alpha\nabla_\beta U^\mu)
$$

The first term: $U^\alpha\nabla_\alpha\xi^\beta = \xi^\alpha\nabla_\alpha U^\beta$ (commutation), so:

$$
= (\xi^\alpha\nabla_\alpha U^\beta)(\nabla_\beta U^\mu) + \xi^\beta U^\alpha\nabla_\alpha\nabla_\beta U^\mu
$$

**Step 4: Use the Riemann tensor to swap covariant derivatives.**

The commutator of covariant derivatives on a vector:

$$
[\nabla_\alpha, \nabla_\beta]U^\mu = R^\mu{}_{\nu\alpha\beta}U^\nu
$$

So: $\nabla_\alpha\nabla_\beta U^\mu = \nabla_\beta\nabla_\alpha U^\mu + R^\mu{}_{\nu\alpha\beta}U^\nu$.

Substitute:

$$
\xi^\beta U^\alpha\nabla_\alpha\nabla_\beta U^\mu = \xi^\beta U^\alpha(\nabla_\beta\nabla_\alpha U^\mu + R^\mu{}_{\nu\alpha\beta}U^\nu)
$$

$$
= \xi^\beta U^\alpha\nabla_\beta\nabla_\alpha U^\mu + R^\mu{}_{\nu\alpha\beta}U^\alpha U^\nu\xi^\beta
$$

**Step 5: Use the geodesic equation $U^\alpha\nabla_\alpha U^\mu = 0$.**

The term $\xi^\beta\nabla_\beta(U^\alpha\nabla_\alpha U^\mu) = 0$. Expanding:

$$
(\xi^\beta\nabla_\beta U^\alpha)(\nabla_\alpha U^\mu) + \xi^\beta U^\alpha\nabla_\beta\nabla_\alpha U^\mu = 0
$$

So: $\xi^\beta U^\alpha\nabla_\beta\nabla_\alpha U^\mu = -(\xi^\beta\nabla_\beta U^\alpha)(\nabla_\alpha U^\mu)$.

**Step 6: Combine.**

$$
\frac{D^2\xi^\mu}{d\tau^2} = (\xi^\alpha\nabla_\alpha U^\beta)(\nabla_\beta U^\mu) - (\xi^\beta\nabla_\beta U^\alpha)(\nabla_\alpha U^\mu) + R^\mu{}_{\nu\alpha\beta}U^\alpha U^\nu\xi^\beta
$$

The first two terms cancel (relabel dummy indices $\alpha \leftrightarrow \beta$ in the second):

$$
\frac{D^2\xi^\mu}{d\tau^2} = R^\mu{}_{\nu\alpha\beta}U^\nu\xi^\alpha U^\beta
$$

Rearranging indices using the symmetries of Riemann ($R^\mu{}_{\nu\alpha\beta} = -R^\mu{}_{\nu\beta\alpha}$):

$$
\boxed{\frac{D^2\xi^\mu}{d\tau^2} = -R^\mu{}_{\nu\alpha\beta}U^\nu\xi^\alpha U^\beta}
$$

This is the **geodesic deviation equation** (also called the **Jacobi equation**). It says: the relative acceleration of nearby freely falling particles is proportional to the Riemann curvature tensor. This is the precise mathematical statement that **tidal forces = curvature**.

**References:** Carroll §3.10; Wald §3.3; MTW §11.5; Hartle Ch. 21.

