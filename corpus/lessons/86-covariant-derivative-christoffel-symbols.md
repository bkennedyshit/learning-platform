---
title: "8.6 — Covariant Derivative & Christoffel Symbols"
subject: "Special & General Relativity"
catalog: advanced
audience_tier: higher-education
chapter: "8.6"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 8.6 — Covariant Derivative & Christoffel Symbols

> *"The essential achievement of general relativity, namely to overcome 'rigid' space, is only indirectly connected with the introduction of a Riemannian metric. The directly relevant conceptual element is the 'displacement field' (Γ), which expresses the infinitesimal displacement of vectors."*
> — Albert Einstein (1955)

In flat spacetime, differentiating a vector field is straightforward — partial derivatives of components give another vector. On a curved manifold, this fails catastrophically: partial derivatives of tensor components do **not** transform as tensors. The cure is the **covariant derivative** $\nabla_\mu$, which adds correction terms (Christoffel symbols $\Gamma^\alpha_{\mu\nu}$) that compensate for the "twisting" of coordinate basis vectors from point to point.

This chapter derives the Christoffel symbols from the metric, proves their key properties, and shows how they enable parallel transport and the geodesic equation.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Explain why partial derivatives fail as tensor operations on curved manifolds.
2. Define the covariant derivative $\nabla_\mu$ and state its defining properties.
3. Derive the Christoffel symbols $\Gamma^\mu_{\alpha\beta}$ from the metric compatibility condition.
4. Compute Christoffel symbols explicitly for the Schwarzschild and FLRW metrics.
5. Write the covariant derivative of vectors, 1-forms, and general tensors.
6. Define parallel transport and solve the parallel transport equation.
7. Derive the geodesic equation from parallel transport of the tangent vector.

---

## 🖼️ Visual Anchor — Parallel Transport on a Curved Surface

![math-08__8.6-fig1](math-08__8.6-fig1.svg)

The diagram shows parallel transport of a vector around a closed triangle on a sphere. The vector returns **rotated** by 90° — this rotation is a direct measure of the curvature enclosed by the path. On a flat surface, parallel transport around any closed loop returns the vector unchanged.

---

## 📚 1. Definitions

### Definition 8.6.1 — The Problem with Partial Derivatives

Consider a vector field $V^\mu(x)$ on a manifold. The partial derivative $\partial_\nu V^\mu$ does **not** transform as a tensor:

$$
\partial'_\nu V'^\mu = \frac{\partial x^\beta}{\partial x'^\nu}\frac{\partial x'^\mu}{\partial x^\alpha}\partial_\beta V^\alpha + \frac{\partial^2 x'^\mu}{\partial x^\alpha\partial x^\beta}\frac{\partial x^\beta}{\partial x'^\nu}V^\alpha
$$

The second term (involving second derivatives of the coordinate transformation) spoils the tensor transformation law. We need a derivative that **cancels** this extra term.

### Definition 8.6.2 — The Covariant Derivative (Connection)

The **covariant derivative** $\nabla_\mu$ is defined by its action on a contravariant vector:

$$
\nabla_\mu V^\nu = \partial_\mu V^\nu + \Gamma^\nu_{\mu\alpha} V^\alpha
$$

and on a covariant vector (1-form):

$$
\nabla_\mu \omega_\nu = \partial_\mu \omega_\nu - \Gamma^\alpha_{\mu\nu} \omega_\alpha
$$

The $\Gamma^\nu_{\mu\alpha}$ are the **connection coefficients** (Christoffel symbols in the Levi-Civita case).

### Definition 8.6.3 — Properties of the Covariant Derivative

The covariant derivative satisfies:
1. **Linearity:** $\nabla_\mu(aT + bS) = a\nabla_\mu T + b\nabla_\mu S$
2. **Leibniz rule:** $\nabla_\mu(T \otimes S) = (\nabla_\mu T)\otimes S + T\otimes(\nabla_\mu S)$
3. **Commutes with contraction:** $\nabla_\mu(T^\alpha{}_\alpha) = (\nabla_\mu T)^\alpha{}_\alpha$
4. **Reduces to partial derivative on scalars:** $\nabla_\mu f = \partial_\mu f$

### Definition 8.6.4 — Christoffel Symbols (Levi-Civita Connection)

The unique connection that is:
- **Metric-compatible:** $\nabla_\alpha g_{\mu\nu} = 0$
- **Torsion-free:** $\Gamma^\alpha_{\mu\nu} = \Gamma^\alpha_{\nu\mu}$

is the **Levi-Civita connection**, with Christoffel symbols:

$$
\Gamma^\sigma_{\mu\nu} = \frac{1}{2}g^{\sigma\alpha}\left(\partial_\mu g_{\alpha\nu} + \partial_\nu g_{\alpha\mu} - \partial_\alpha g_{\mu\nu}\right)
$$

### Definition 8.6.5 — Covariant Derivative of a General Tensor

For a $(p,q)$-tensor $T^{\mu_1\cdots\mu_p}{}_{\nu_1\cdots\nu_q}$:

$$
\nabla_\alpha T^{\mu_1\cdots\mu_p}{}_{\nu_1\cdots\nu_q} = \partial_\alpha T^{\mu_1\cdots\mu_p}{}_{\nu_1\cdots\nu_q} + \sum_{i=1}^p \Gamma^{\mu_i}_{\alpha\beta} T^{\mu_1\cdots\beta\cdots\mu_p}{}_{\nu_1\cdots\nu_q} - \sum_{j=1}^q \Gamma^\beta_{\alpha\nu_j} T^{\mu_1\cdots\mu_p}{}_{\nu_1\cdots\beta\cdots\nu_q}
$$

Each upper index gets a $+\Gamma$ term; each lower index gets a $-\Gamma$ term.

### Definition 8.6.6 — Parallel Transport

A vector $V^\mu$ is **parallel-transported** along a curve $x^\mu(\lambda)$ with tangent $U^\mu = dx^\mu/d\lambda$ if:

$$
\nabla_U V^\mu = U^\alpha \nabla_\alpha V^\mu = \frac{dV^\mu}{d\lambda} + \Gamma^\mu_{\alpha\beta} U^\alpha V^\beta = 0
$$

This is a first-order ODE: given initial $V^\mu$ at one point, the solution is unique along the curve.




---

## 📐 2. Axioms / Postulates

### Axiom 8.6.1 — Metric Compatibility

The covariant derivative of the metric tensor vanishes:

$$
\nabla_\alpha g_{\mu\nu} = 0
$$

This ensures that inner products are preserved under parallel transport: if $V^\mu$ and $W^\mu$ are parallel-transported along a curve, then $g_{\mu\nu}V^\mu W^\nu$ is constant along that curve.

### Axiom 8.6.2 — Torsion-Free Connection

The connection is symmetric in its lower indices:

$$
\Gamma^\alpha_{\mu\nu} = \Gamma^\alpha_{\nu\mu}
$$

Equivalently, the torsion tensor $T^\alpha_{\mu\nu} = \Gamma^\alpha_{\mu\nu} - \Gamma^\alpha_{\nu\mu} = 0$. (Extensions with torsion exist — Einstein-Cartan theory — but standard GR uses the torsion-free Levi-Civita connection.)

---

## 🛡️ 3. Lemmas

### Lemma 8.6.1 — Derivation of the Christoffel Symbol Formula

**Statement:** The unique metric-compatible, torsion-free connection is:

$$
\Gamma^\sigma_{\mu\nu} = \frac{1}{2}g^{\sigma\alpha}(\partial_\mu g_{\alpha\nu} + \partial_\nu g_{\alpha\mu} - \partial_\alpha g_{\mu\nu})
$$

**Proof:**

**Step 1:** Write metric compatibility three times with cyclically permuted indices:

$$
\nabla_\mu g_{\nu\alpha} = \partial_\mu g_{\nu\alpha} - \Gamma^\beta_{\mu\nu}g_{\beta\alpha} - \Gamma^\beta_{\mu\alpha}g_{\nu\beta} = 0 \tag{i}
$$

$$
\nabla_\nu g_{\alpha\mu} = \partial_\nu g_{\alpha\mu} - \Gamma^\beta_{\nu\alpha}g_{\beta\mu} - \Gamma^\beta_{\nu\mu}g_{\alpha\beta} = 0 \tag{ii}
$$

$$
\nabla_\alpha g_{\mu\nu} = \partial_\alpha g_{\mu\nu} - \Gamma^\beta_{\alpha\mu}g_{\beta\nu} - \Gamma^\beta_{\alpha\nu}g_{\mu\beta} = 0 \tag{iii}
$$

**Step 2:** Compute (i) + (ii) − (iii):

$$
\partial_\mu g_{\nu\alpha} + \partial_\nu g_{\alpha\mu} - \partial_\alpha g_{\mu\nu}
$$

$$
- \Gamma^\beta_{\mu\nu}g_{\beta\alpha} - \Gamma^\beta_{\mu\alpha}g_{\nu\beta} - \Gamma^\beta_{\nu\alpha}g_{\beta\mu} - \Gamma^\beta_{\nu\mu}g_{\alpha\beta} + \Gamma^\beta_{\alpha\mu}g_{\beta\nu} + \Gamma^\beta_{\alpha\nu}g_{\mu\beta} = 0
$$

**Step 3:** Use symmetry $\Gamma^\beta_{\mu\nu} = \Gamma^\beta_{\nu\mu}$ (torsion-free). Group terms:

- $-\Gamma^\beta_{\mu\nu}g_{\beta\alpha} - \Gamma^\beta_{\nu\mu}g_{\alpha\beta} = -2\Gamma^\beta_{\mu\nu}g_{\alpha\beta}$ (using symmetry of both $\Gamma$ and $g$)
- $-\Gamma^\beta_{\mu\alpha}g_{\nu\beta} + \Gamma^\beta_{\alpha\mu}g_{\beta\nu} = 0$ (same term, cancels)
- $-\Gamma^\beta_{\nu\alpha}g_{\beta\mu} + \Gamma^\beta_{\alpha\nu}g_{\mu\beta} = 0$ (same term, cancels)

Therefore:

$$
\partial_\mu g_{\nu\alpha} + \partial_\nu g_{\alpha\mu} - \partial_\alpha g_{\mu\nu} - 2\Gamma^\beta_{\mu\nu}g_{\alpha\beta} = 0
$$

**Step 4:** Solve for $\Gamma$:

$$
2g_{\alpha\beta}\Gamma^\beta_{\mu\nu} = \partial_\mu g_{\nu\alpha} + \partial_\nu g_{\alpha\mu} - \partial_\alpha g_{\mu\nu}
$$

**Step 5:** Multiply by $g^{\sigma\alpha}$ (and use $g^{\sigma\alpha}g_{\alpha\beta} = \delta^\sigma_\beta$):

$$
2\Gamma^\sigma_{\mu\nu} = g^{\sigma\alpha}(\partial_\mu g_{\nu\alpha} + \partial_\nu g_{\alpha\mu} - \partial_\alpha g_{\mu\nu})
$$

$$
\boxed{\Gamma^\sigma_{\mu\nu} = \frac{1}{2}g^{\sigma\alpha}(\partial_\mu g_{\alpha\nu} + \partial_\nu g_{\alpha\mu} - \partial_\alpha g_{\mu\nu})} \qquad \blacksquare
$$

---

### Lemma 8.6.2 — Number of Independent Christoffel Symbols

**Statement:** In $n$ dimensions, the Christoffel symbols have $n^2(n+1)/2$ independent components.

**Proof:** $\Gamma^\sigma_{\mu\nu}$ has $n$ choices for $\sigma$ and (by symmetry $\mu\nu$) $n(n+1)/2$ independent pairs $(\mu,\nu)$. Total: $n \times n(n+1)/2 = n^2(n+1)/2$.

In 4D spacetime: $4 \times 4 \times 5/2 = 40$ independent Christoffel symbols. $\blacksquare$

---

## 👑 4. Theorems

### Theorem 8.6.1 — Geodesic Equation from Parallel Transport

**Statement:** A geodesic is a curve whose tangent vector is parallel-transported along itself:

$$
\nabla_U U^\mu = 0 \implies \frac{d^2x^\mu}{d\lambda^2} + \Gamma^\mu_{\alpha\beta}\frac{dx^\alpha}{d\lambda}\frac{dx^\beta}{d\lambda} = 0
$$

### Theorem 8.6.2 — Covariant Divergence and Conservation Laws

**Statement:** The covariant divergence of a vector field:

$$
\nabla_\mu V^\mu = \partial_\mu V^\mu + \Gamma^\mu_{\mu\alpha}V^\alpha = \frac{1}{\sqrt{-g}}\partial_\mu(\sqrt{-g}\, V^\mu)
$$

This compact formula is crucial for conservation laws: $\nabla_\mu T^{\mu\nu} = 0$ (energy-momentum conservation in curved spacetime).

### Theorem 8.6.3 — Contracted Christoffel Symbol

**Statement:**

$$
\Gamma^\mu_{\mu\nu} = \frac{1}{2}g^{\mu\alpha}\partial_\nu g_{\mu\alpha} = \partial_\nu \ln\sqrt{-g} = \frac{1}{\sqrt{-g}}\partial_\nu\sqrt{-g}
$$

---

## ✍️ 5. Proofs / Derivations

### Proof 8.6.1 — Christoffel Symbols for the 2-Sphere

**Setup:** Metric on $S^2$ (radius $R$): $ds^2 = R^2 d\theta^2 + R^2\sin^2\theta\, d\phi^2$.

Coordinates: $x^1 = \theta$, $x^2 = \phi$. Metric components:

$$
g_{11} = R^2, \quad g_{22} = R^2\sin^2\theta, \quad g_{12} = g_{21} = 0
$$

Inverse metric: $g^{11} = 1/R^2$, $g^{22} = 1/(R^2\sin^2\theta)$, $g^{12} = 0$.

**Step 1:** Non-zero partial derivatives of the metric:

$$
\partial_1 g_{22} = \partial_\theta(R^2\sin^2\theta) = 2R^2\sin\theta\cos\theta
$$

All other $\partial_\alpha g_{\mu\nu} = 0$ (since $g_{11} = R^2$ is constant and $g_{22}$ depends only on $\theta$).

**Step 2:** Compute $\Gamma^1_{22}$ (the only one with $\partial g_{22}$ contributing):

$$
\Gamma^1_{22} = \frac{1}{2}g^{1\alpha}(\partial_2 g_{\alpha 2} + \partial_2 g_{\alpha 2} - \partial_\alpha g_{22})
$$

Only $\alpha = 1$ contributes (diagonal metric):

$$
= \frac{1}{2}g^{11}(0 + 0 - \partial_1 g_{22}) = \frac{1}{2}\frac{1}{R^2}(-2R^2\sin\theta\cos\theta) = -\sin\theta\cos\theta
$$

**Step 3:** Compute $\Gamma^2_{12} = \Gamma^2_{21}$:

$$
\Gamma^2_{12} = \frac{1}{2}g^{2\alpha}(\partial_1 g_{\alpha 2} + \partial_2 g_{\alpha 1} - \partial_\alpha g_{12})
$$

Only $\alpha = 2$:

$$
= \frac{1}{2}g^{22}(\partial_1 g_{22} + 0 - 0) = \frac{1}{2}\frac{1}{R^2\sin^2\theta}(2R^2\sin\theta\cos\theta) = \frac{\cos\theta}{\sin\theta} = \cot\theta
$$

**Step 4:** All other Christoffel symbols vanish. Summary:

$$
\Gamma^1_{22} = -\sin\theta\cos\theta, \qquad \Gamma^2_{12} = \Gamma^2_{21} = \cot\theta
$$

All others $= 0$. $\blacksquare$

---

### Proof 8.6.2 — Christoffel Symbols for the Schwarzschild Metric

**Setup:** $ds^2 = -f(r)c^2 dt^2 + f(r)^{-1}dr^2 + r^2 d\theta^2 + r^2\sin^2\theta\, d\phi^2$ where $f(r) = 1 - r_s/r$.

Coordinates: $x^0 = t$, $x^1 = r$, $x^2 = \theta$, $x^3 = \phi$.

Metric: $g_{00} = -fc^2$, $g_{11} = f^{-1}$, $g_{22} = r^2$, $g_{33} = r^2\sin^2\theta$.

Inverse: $g^{00} = -1/(fc^2)$, $g^{11} = f$, $g^{22} = 1/r^2$, $g^{33} = 1/(r^2\sin^2\theta)$.

**Non-zero derivatives:** $\partial_r g_{00} = -f'c^2$, $\partial_r g_{11} = -f'/f^2$, $\partial_r g_{22} = 2r$, $\partial_r g_{33} = 2r\sin^2\theta$, $\partial_\theta g_{33} = 2r^2\sin\theta\cos\theta$.

Where $f' = df/dr = r_s/r^2$.

**Computing each non-zero symbol:**

$\Gamma^0_{01} = \Gamma^0_{10}$:

$$
= \frac{1}{2}g^{00}(\partial_0 g_{00} + \partial_1 g_{00} - \partial_0 g_{01}) = \frac{1}{2}\left(-\frac{1}{fc^2}\right)(0 + (-f'c^2) - 0) = \frac{f'}{2f}
$$

$$
\Gamma^0_{01} = \frac{r_s}{2r^2 f} = \frac{r_s}{2r^2(1-r_s/r)} = \frac{r_s}{2r(r-r_s)}
$$

$\Gamma^1_{00}$:

$$
= \frac{1}{2}g^{11}(\partial_0 g_{10} + \partial_0 g_{10} - \partial_1 g_{00}) = \frac{1}{2}f(0 + 0 - (-f'c^2)) = \frac{1}{2}ff'c^2
$$

$$
\Gamma^1_{00} = \frac{c^2 f f'}{2} = \frac{c^2(1-r_s/r)(r_s/r^2)}{2} = \frac{c^2 r_s(r-r_s)}{2r^3}
$$

$\Gamma^1_{11}$:

$$
= \frac{1}{2}g^{11}\partial_1 g_{11} = \frac{1}{2}f \cdot \left(-\frac{f'}{f^2}\right) = -\frac{f'}{2f} = -\frac{r_s}{2r(r-r_s)}
$$

$\Gamma^1_{22}$:

$$
= \frac{1}{2}g^{11}(0 + 0 - \partial_1 g_{22}) = \frac{1}{2}f(-2r) = -rf = -(r - r_s)
$$

$\Gamma^1_{33}$:

$$
= -\frac{1}{2}g^{11}\partial_1 g_{33} = -\frac{1}{2}f(2r\sin^2\theta) = -rf\sin^2\theta = -(r-r_s)\sin^2\theta
$$

$\Gamma^2_{12} = \Gamma^2_{21}$:

$$
= \frac{1}{2}g^{22}\partial_1 g_{22} = \frac{1}{2}\frac{1}{r^2}(2r) = \frac{1}{r}
$$

$\Gamma^2_{33}$:

$$
= -\frac{1}{2}g^{22}\partial_2 g_{33} = -\frac{1}{2}\frac{1}{r^2}(2r^2\sin\theta\cos\theta) = -\sin\theta\cos\theta
$$

$\Gamma^3_{13} = \Gamma^3_{31}$:

$$
= \frac{1}{2}g^{33}\partial_1 g_{33} = \frac{1}{2}\frac{1}{r^2\sin^2\theta}(2r\sin^2\theta) = \frac{1}{r}
$$

$\Gamma^3_{23} = \Gamma^3_{32}$:

$$
= \frac{1}{2}g^{33}\partial_2 g_{33} = \frac{1}{2}\frac{1}{r^2\sin^2\theta}(2r^2\sin\theta\cos\theta) = \cot\theta
$$

**Summary of non-zero Schwarzschild Christoffel symbols:**

| Symbol | Value |
|--------|-------|
| $\Gamma^0_{01}$ | $\frac{r_s}{2r(r-r_s)}$ |
| $\Gamma^1_{00}$ | $\frac{c^2 r_s(r-r_s)}{2r^3}$ |
| $\Gamma^1_{11}$ | $-\frac{r_s}{2r(r-r_s)}$ |
| $\Gamma^1_{22}$ | $-(r-r_s)$ |
| $\Gamma^1_{33}$ | $-(r-r_s)\sin^2\theta$ |
| $\Gamma^2_{12}$ | $1/r$ |
| $\Gamma^2_{33}$ | $-\sin\theta\cos\theta$ |
| $\Gamma^3_{13}$ | $1/r$ |
| $\Gamma^3_{23}$ | $\cot\theta$ |

$\blacksquare$




---

## 🧮 6. Worked Examples

### Example 8.6.1 — Geodesic Equation on the 2-Sphere

**Problem:** Write the geodesic equations on the unit sphere and show that great circles are solutions.

**Solution:**

Using $\Gamma^1_{22} = -\sin\theta\cos\theta$ and $\Gamma^2_{12} = \cot\theta$ (from Proof 8.6.1, with $R=1$):

$$
\ddot{\theta} + \Gamma^1_{22}\dot{\phi}^2 = 0 \implies \ddot{\theta} - \sin\theta\cos\theta\,\dot{\phi}^2 = 0
$$

$$
\ddot{\phi} + 2\Gamma^2_{12}\dot{\theta}\dot{\phi} = 0 \implies \ddot{\phi} + 2\cot\theta\,\dot{\theta}\dot{\phi} = 0
$$

**Check: meridian ($\phi = \text{const}$, $\dot\phi = 0$):**

$$
\ddot\theta = 0 \implies \theta(\lambda) = a\lambda + b
$$

This is a great circle (meridian). ✓

**Check: equator ($\theta = \pi/2$, $\dot\theta = 0$):**

$$
\ddot\phi = 0 \implies \phi(\lambda) = c\lambda + d
$$

And the $\theta$-equation: $0 - \sin(\pi/2)\cos(\pi/2)\dot\phi^2 = 0 - 0 = 0$. ✓

---

### Example 8.6.2 — Covariant Divergence in Schwarzschild Spacetime

**Problem:** Compute $\nabla_\mu V^\mu$ for a radial vector field $V^\mu = (0, V^r(r), 0, 0)$ in Schwarzschild spacetime.

**Solution:**

Using the formula $\nabla_\mu V^\mu = \frac{1}{\sqrt{-g}}\partial_\mu(\sqrt{-g}\, V^\mu)$:

From Proof 8.5.1: $\sqrt{-g} = cr^2\sin\theta$ (for Schwarzschild).

$$
\nabla_\mu V^\mu = \frac{1}{cr^2\sin\theta}\partial_r(cr^2\sin\theta \cdot V^r) = \frac{1}{r^2}\partial_r(r^2 V^r) = \frac{1}{r^2}(2rV^r + r^2 \partial_r V^r)
$$

$$
= \frac{2V^r}{r} + \partial_r V^r
$$

This is the same as the flat-space divergence in spherical coordinates — the Schwarzschild factors cancel in the divergence formula for a purely radial field.

---

### Example 8.6.3 — Parallel Transport Along the Equator

**Problem:** A vector $V^\mu = (V^\theta, V^\phi) = (1, 0)$ at $\phi = 0$ on the equator ($\theta = \pi/2$) of the unit sphere is parallel-transported along the equator to $\phi = \phi_0$. Find the resulting vector.

**Solution:**

Along the equator: $\theta = \pi/2$ (constant), parametrize by $\phi$. Tangent: $U^\mu = (0, 1)$ (i.e., $d\theta/d\phi = 0$, $d\phi/d\phi = 1$).

Parallel transport equations:

$$
\frac{dV^\theta}{d\phi} + \Gamma^\theta_{\phi\phi}(U^\phi)(V^\phi) + \Gamma^\theta_{\phi\theta}(U^\phi)(V^\theta) = 0
$$

Wait — let's be systematic. $\frac{dV^1}{d\lambda} + \Gamma^1_{\alpha\beta}U^\alpha V^\beta = 0$ with $\lambda = \phi$:

$$
\frac{dV^\theta}{d\phi} + \Gamma^\theta_{\phi\phi}\cdot 1 \cdot V^\phi = 0
$$

At $\theta = \pi/2$: $\Gamma^\theta_{\phi\phi} = -\sin(\pi/2)\cos(\pi/2) = 0$.

So $dV^\theta/d\phi = 0 \implies V^\theta = 1$ (constant). ✓

For $V^\phi$: $\frac{dV^\phi}{d\phi} + \Gamma^\phi_{\phi\theta}\cdot 1 \cdot V^\theta + \Gamma^\phi_{\phi\phi}\cdot 1 \cdot V^\phi = 0$

$\Gamma^\phi_{\phi\theta} = \cot(\pi/2) = 0$ and $\Gamma^\phi_{\phi\phi} = 0$.

So $dV^\phi/d\phi = 0 \implies V^\phi = 0$ (constant).

**Result:** On the equator, the vector $(1, 0)$ remains $(1, 0)$ — it doesn't rotate. This is because the equator is itself a geodesic (great circle), and parallel transport along a geodesic preserves the tangent vector's relationship to the curve.

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- **Previous:** [8.5 - Differential Geometry - Manifolds & Metrics](8.5---Differential-Geometry---Manifolds-&-Metrics)
- **Next:** [8.7 - Geodesics & Curvature - Riemann & Ricci Tensors](8.7---Geodesics-&-Curvature---Riemann-&-Ricci-Tensors)
- **Exterior derivative (related):** [1.8 - Exterior Algebra & Differential Forms](1.8---Exterior-Algebra-&-Differential-Forms)
- **Tensor foundations:** [2.8 - SVD & Tensors](2.8---SVD-&-Tensors)
- **Application:** [8.8 - Einstein Field Equations & Schwarzschild Black Holes](8.8---Einstein-Field-Equations-&-Schwarzschild-Black-Holes)

### External References
1. **Carroll, S.** (1997). arXiv:gr-qc/9712019. Chapter 3: Curvature (§3.1–3.3).
2. **Wald, R.M.** (1984). *General Relativity*. Chapter 3: Curvature.
3. **Misner, Thorne & Wheeler** (1973). *Gravitation*. Chapters 8–10.
4. **Susskind, L.** *The Theoretical Minimum: General Relativity*. Lectures 5–6.
5. **Schutz, B.** (2009). *A First Course in General Relativity* (2nd ed.). Cambridge. Chapter 5.

---

*Next: [8.7 - Geodesics & Curvature - Riemann & Ricci Tensors](8.7---Geodesics-&-Curvature---Riemann-&-Ricci-Tensors) →*



---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.6.E1 — Christoffel Symbols for the 2-Sphere (Complete Calculation)

**Problem:** Compute all Christoffel symbols for the unit 2-sphere with metric $g_{ab} = \text{diag}(1, \sin^2\theta)$ in coordinates $(\theta, \phi)$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Setup.** Coordinates: $x^1 = \theta$, $x^2 = \phi$. Metric:

$$
g_{11} = 1, \qquad g_{22} = \sin^2\theta, \qquad g_{12} = g_{21} = 0
$$

Inverse metric:

$$
g^{11} = 1, \qquad g^{22} = \frac{1}{\sin^2\theta}, \qquad g^{12} = g^{21} = 0
$$

The Christoffel symbol formula:

$$
\Gamma^a_{bc} = \frac{1}{2}g^{ad}(\partial_b g_{dc} + \partial_c g_{db} - \partial_d g_{bc})
$$

**Non-zero partial derivatives of the metric:**

$$
\partial_1 g_{22} = \partial_\theta(\sin^2\theta) = 2\sin\theta\cos\theta = \sin(2\theta)
$$

All other $\partial_a g_{bc} = 0$ (since $g_{11} = 1$ is constant, and $g_{22}$ depends only on $\theta = x^1$).

**Compute each symbol systematically:**

$\Gamma^1_{11}$:

$$
= \frac{1}{2}g^{11}(\partial_1 g_{11} + \partial_1 g_{11} - \partial_1 g_{11}) = \frac{1}{2}(1)(0 + 0 - 0) = 0
$$

$\Gamma^1_{12} = \Gamma^1_{21}$:

$$
= \frac{1}{2}g^{11}(\partial_1 g_{12} + \partial_2 g_{11} - \partial_1 g_{12}) = \frac{1}{2}(1)(0 + 0 - 0) = 0
$$

$\Gamma^1_{22}$:

$$
= \frac{1}{2}g^{11}(\partial_2 g_{12} + \partial_2 g_{12} - \partial_1 g_{22}) = \frac{1}{2}(1)(0 + 0 - 2\sin\theta\cos\theta)
$$

$$
\boxed{\Gamma^1_{22} = -\sin\theta\cos\theta}
$$

$\Gamma^2_{11}$:

$$
= \frac{1}{2}g^{22}(\partial_1 g_{21} + \partial_1 g_{21} - \partial_2 g_{11}) = \frac{1}{2}\frac{1}{\sin^2\theta}(0 + 0 - 0) = 0
$$

$\Gamma^2_{12} = \Gamma^2_{21}$:

$$
= \frac{1}{2}g^{22}(\partial_1 g_{22} + \partial_2 g_{21} - \partial_2 g_{12}) = \frac{1}{2}\frac{1}{\sin^2\theta}(2\sin\theta\cos\theta + 0 - 0)
$$

$$
\boxed{\Gamma^2_{12} = \Gamma^2_{21} = \frac{\cos\theta}{\sin\theta} = \cot\theta}
$$

$\Gamma^2_{22}$:

$$
= \frac{1}{2}g^{22}(\partial_2 g_{22} + \partial_2 g_{22} - \partial_2 g_{22}) = \frac{1}{2}\frac{1}{\sin^2\theta}(0 + 0 - 0) = 0
$$

**Summary table:**

| Symbol | Value |
|--------|-------|
| $\Gamma^1_{22}$ | $-\sin\theta\cos\theta$ |
| $\Gamma^2_{12} = \Gamma^2_{21}$ | $\cot\theta$ |
| All others | $0$ |

**Verification:** The geodesic equations on the 2-sphere are:

$$
\ddot{\theta} + \Gamma^1_{22}\dot{\phi}^2 = 0 \implies \ddot{\theta} - \sin\theta\cos\theta\,\dot{\phi}^2 = 0
$$

$$
\ddot{\phi} + 2\Gamma^2_{12}\dot{\theta}\dot{\phi} = 0 \implies \ddot{\phi} + 2\cot\theta\,\dot{\theta}\dot{\phi} = 0
$$

These are the equations for great circles on the sphere. ✓

</details>

---

### Example 8.6.E2 — Christoffel Symbols for the Schwarzschild Metric (Full Derivation)

**Problem:** Compute all non-zero Christoffel symbols for the Schwarzschild metric:

$$
ds^2 = -\left(1 - \frac{r_s}{r}\right)c^2\,dt^2 + \frac{dr^2}{1 - r_s/r} + r^2\,d\theta^2 + r^2\sin^2\theta\,d\phi^2
$$

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Setup.** Coordinates: $(x^0, x^1, x^2, x^3) = (ct, r, \theta, \phi)$. Define $f(r) = 1 - r_s/r$.

Metric components:

$$
g_{00} = -f, \quad g_{11} = f^{-1}, \quad g_{22} = r^2, \quad g_{33} = r^2\sin^2\theta
$$

Inverse metric:

$$
g^{00} = -f^{-1}, \quad g^{11} = f, \quad g^{22} = r^{-2}, \quad g^{33} = (r^2\sin^2\theta)^{-1}
$$

**Non-zero derivatives:**

$$
\partial_1 g_{00} = \partial_r(-f) = -f' = -\frac{r_s}{r^2}
$$

$$
\partial_1 g_{11} = \partial_r(f^{-1}) = -f^{-2}f' = -\frac{r_s}{r^2}\cdot\frac{1}{f^2} = \frac{r_s}{r^2 f^2}
$$

Wait — $f' = d/dr(1 - r_s/r) = r_s/r^2$. So $\partial_r g_{00} = -r_s/r^2$ and $\partial_r g_{11} = \partial_r(1/f) = -f'/f^2 = -r_s/(r^2 f^2)$.

Let me be more careful:

$$
\partial_1 g_{00} = \frac{\partial}{\partial r}\left(-1 + \frac{r_s}{r}\right) = -\frac{r_s}{r^2}
$$

$$
\partial_1 g_{11} = \frac{\partial}{\partial r}\left(\frac{1}{1 - r_s/r}\right) = \frac{\partial}{\partial r}\left(\frac{r}{r - r_s}\right) = \frac{(r-r_s) - r}{(r-r_s)^2} = \frac{-r_s}{(r-r_s)^2}
$$

$$
\partial_1 g_{22} = 2r, \qquad \partial_1 g_{33} = 2r\sin^2\theta
$$

$$
\partial_2 g_{33} = 2r^2\sin\theta\cos\theta
$$

**Now compute each non-zero Christoffel symbol:**

**$\Gamma^0_{01} = \Gamma^0_{10}$:**

$$
= \frac{1}{2}g^{00}(\partial_0 g_{00} + \partial_1 g_{00} - \partial_0 g_{01}) = \frac{1}{2}\left(-\frac{1}{f}\right)(0 + (-r_s/r^2) - 0)
$$

Wait — the formula is $\Gamma^0_{01} = \frac{1}{2}g^{00}(\partial_0 g_{01} + \partial_1 g_{00} - \partial_0 g_{01})$. Let me use the correct index placement:

$$
\Gamma^\alpha_{\mu\nu} = \frac{1}{2}g^{\alpha\sigma}(\partial_\mu g_{\nu\sigma} + \partial_\nu g_{\mu\sigma} - \partial_\sigma g_{\mu\nu})
$$

$\Gamma^0_{01}$: $\alpha=0$, $\mu=0$, $\nu=1$. Only $\sigma=0$ contributes (diagonal metric):

$$
= \frac{1}{2}g^{00}(\partial_0 g_{10} + \partial_1 g_{00} - \partial_0 g_{01}) = \frac{1}{2}(-f^{-1})(0 + (-r_s/r^2) - 0)
$$

$$
= \frac{1}{2}\frac{1}{f}\frac{r_s}{r^2} = \frac{r_s}{2r^2 f} = \frac{r_s}{2r(r - r_s)}
$$

$$
\boxed{\Gamma^0_{01} = \Gamma^0_{10} = \frac{r_s}{2r(r-r_s)}}
$$

**$\Gamma^1_{00}$:** $\alpha=1$, $\mu=\nu=0$. Only $\sigma=1$:

$$
= \frac{1}{2}g^{11}(\partial_0 g_{01} + \partial_0 g_{01} - \partial_1 g_{00}) = \frac{1}{2}f(0 + 0 - (-r_s/r^2))
$$

$$
= \frac{f\, r_s}{2r^2} = \frac{(1-r_s/r)\,r_s}{2r^2} = \frac{r_s(r-r_s)}{2r^3}
$$

$$
\boxed{\Gamma^1_{00} = \frac{c^2\,r_s(r-r_s)}{2r^3}}
$$

(The $c^2$ appears because $g_{00} = -f c^2$ if we keep $c$ explicit in the metric; with $x^0 = ct$ it's already absorbed.)

Actually, with coordinates $(ct, r, \theta, \phi)$ and $g_{00} = -f$: $\partial_r g_{00} = -r_s/r^2$, so:

$$
\Gamma^1_{00} = \frac{1}{2}f \cdot \frac{r_s}{r^2} = \frac{r_s(r-r_s)}{2r^3}
$$

**$\Gamma^1_{11}$:** $\alpha=1$, $\mu=\nu=1$. Only $\sigma=1$:

$$
= \frac{1}{2}g^{11}\partial_1 g_{11} = \frac{1}{2}f\left(\frac{-r_s}{(r-r_s)^2}\right) = \frac{1}{2}\frac{r-r_s}{r}\cdot\frac{-r_s}{(r-r_s)^2} = \frac{-r_s}{2r(r-r_s)}
$$

$$
\boxed{\Gamma^1_{11} = -\frac{r_s}{2r(r-r_s)}}
$$

**$\Gamma^1_{22}$:** $\alpha=1$, $\mu=\nu=2$. Only $\sigma=1$:

$$
= \frac{1}{2}g^{11}(-\partial_1 g_{22}) = \frac{1}{2}f(-2r) = -rf = -(r-r_s)
$$

$$
\boxed{\Gamma^1_{22} = -(r-r_s)}
$$

**$\Gamma^1_{33}$:** $\alpha=1$, $\mu=\nu=3$. Only $\sigma=1$:

$$
= \frac{1}{2}g^{11}(-\partial_1 g_{33}) = \frac{1}{2}f(-2r\sin^2\theta) = -(r-r_s)\sin^2\theta
$$

$$
\boxed{\Gamma^1_{33} = -(r-r_s)\sin^2\theta}
$$

**$\Gamma^2_{12} = \Gamma^2_{21}$:** $\alpha=2$, $\mu=1$, $\nu=2$. Only $\sigma=2$:

$$
= \frac{1}{2}g^{22}\partial_1 g_{22} = \frac{1}{2}\frac{1}{r^2}(2r) = \frac{1}{r}
$$

$$
\boxed{\Gamma^2_{12} = \frac{1}{r}}
$$

**$\Gamma^2_{33}$:** $\alpha=2$, $\mu=\nu=3$. Only $\sigma=2$:

$$
= \frac{1}{2}g^{22}(-\partial_2 g_{33}) = \frac{1}{2}\frac{1}{r^2}(-2r^2\sin\theta\cos\theta) = -\sin\theta\cos\theta
$$

$$
\boxed{\Gamma^2_{33} = -\sin\theta\cos\theta}
$$

**$\Gamma^3_{13} = \Gamma^3_{31}$:** $\alpha=3$, $\mu=1$, $\nu=3$. Only $\sigma=3$:

$$
= \frac{1}{2}g^{33}\partial_1 g_{33} = \frac{1}{2}\frac{1}{r^2\sin^2\theta}(2r\sin^2\theta) = \frac{1}{r}
$$

$$
\boxed{\Gamma^3_{13} = \frac{1}{r}}
$$

**$\Gamma^3_{23} = \Gamma^3_{32}$:** $\alpha=3$, $\mu=2$, $\nu=3$. Only $\sigma=3$:

$$
= \frac{1}{2}g^{33}\partial_2 g_{33} = \frac{1}{2}\frac{1}{r^2\sin^2\theta}(2r^2\sin\theta\cos\theta) = \cot\theta
$$

$$
\boxed{\Gamma^3_{23} = \cot\theta}
$$

**Complete summary:**

| Symbol | Value |
|--------|-------|
| $\Gamma^0_{01} = \Gamma^0_{10}$ | $\frac{r_s}{2r(r-r_s)}$ |
| $\Gamma^1_{00}$ | $\frac{r_s(r-r_s)}{2r^3}$ |
| $\Gamma^1_{11}$ | $-\frac{r_s}{2r(r-r_s)}$ |
| $\Gamma^1_{22}$ | $-(r-r_s)$ |
| $\Gamma^1_{33}$ | $-(r-r_s)\sin^2\theta$ |
| $\Gamma^2_{12} = \Gamma^2_{21}$ | $1/r$ |
| $\Gamma^2_{33}$ | $-\sin\theta\cos\theta$ |
| $\Gamma^3_{13} = \Gamma^3_{31}$ | $1/r$ |
| $\Gamma^3_{23} = \Gamma^3_{32}$ | $\cot\theta$ |

All other Christoffel symbols vanish.

**Note:** The angular symbols ($\Gamma^2_{12}$, $\Gamma^2_{33}$, $\Gamma^3_{13}$, $\Gamma^3_{23}$) are identical to those of flat-space spherical coordinates — they encode the coordinate effects of using spherical coordinates, not gravitational effects. The gravitational physics is entirely in $\Gamma^0_{01}$, $\Gamma^1_{00}$, $\Gamma^1_{11}$, $\Gamma^1_{22}$, $\Gamma^1_{33}$.

</details>

---

### Example 8.6.E3 — Covariant Derivative of a Vector Along a Curve

**Problem:** A vector field $V^\mu = (0, 1, 0, 0)$ (pointing radially outward) is transported along the equator ($\theta = \pi/2$, $r = R = \text{const}$) of the Schwarzschild spacetime. Compute the covariant derivative $\nabla_\phi V^\mu$ (derivative along the $\phi$-direction).

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Formula for covariant derivative along a coordinate direction.**

$$
\nabla_\nu V^\mu = \partial_\nu V^\mu + \Gamma^\mu_{\nu\alpha}V^\alpha
$$

We want $\nabla_3 V^\mu$ (derivative along $\phi = x^3$), with $V^\alpha = (0, 1, 0, 0)$ (only $V^1 = 1$ is non-zero).

**Step 2: Compute each component.**

$\nabla_3 V^0$:

$$
= \partial_3 V^0 + \Gamma^0_{3\alpha}V^\alpha = 0 + \Gamma^0_{31}V^1 = \Gamma^0_{31} \cdot 1
$$

From the Schwarzschild table: $\Gamma^0_{31} = 0$ (not in the non-zero list).

$$
\nabla_3 V^0 = 0
$$

$\nabla_3 V^1$:

$$
= \partial_3 V^1 + \Gamma^1_{3\alpha}V^\alpha = 0 + \Gamma^1_{31}V^1 = \Gamma^1_{31} \cdot 1
$$

$\Gamma^1_{31}$: not in the non-zero list (only $\Gamma^1_{33}$ is non-zero with both lower indices being 3).

$$
\nabla_3 V^1 = 0
$$

$\nabla_3 V^2$:

$$
= \partial_3 V^2 + \Gamma^2_{3\alpha}V^\alpha = 0 + \Gamma^2_{31}V^1 = \Gamma^2_{31} \cdot 1
$$

$\Gamma^2_{31}$: not in the non-zero list.

$$
\nabla_3 V^2 = 0
$$

$\nabla_3 V^3$:

$$
= \partial_3 V^3 + \Gamma^3_{3\alpha}V^\alpha = 0 + \Gamma^3_{31}V^1 = \Gamma^3_{31} \cdot 1 = \frac{1}{r}
$$

From the table: $\Gamma^3_{13} = \Gamma^3_{31} = 1/r$.

$$
\nabla_3 V^3 = \frac{1}{r}\bigg|_{r=R} = \frac{1}{R}
$$

**Step 3: Result.**

$$
\nabla_\phi V^\mu = \left(0,\; 0,\; 0,\; \frac{1}{R}\right)
$$

**Interpretation:** The radial vector, when differentiated along the $\phi$-direction, acquires a $\phi$-component. This is because the coordinate basis vectors $\partial_r$ and $\partial_\phi$ are not parallel-transported along the equator — the coordinate system itself "rotates." This is a purely geometric (coordinate) effect, present even in flat space with spherical coordinates.

**Physical meaning:** If we parallel-transport the radial vector along the equator (requiring $\nabla_\phi V^\mu = 0$), the vector must compensate by acquiring a $\phi$-component to "stay pointing in the same direction" in the curved coordinate system. The failure of $\nabla_\phi V^\mu = 0$ means the vector $V^\mu = (0,1,0,0)$ is NOT parallel-transported along the equator.

</details>




---

## 📘 9. Appendix: Extended Derivations & Special Cases

### Appendix 9.1 — Parallel Transport Equation: Full Derivation

**Problem:** Derive the parallel transport equation $\frac{DV^\mu}{d\lambda} = 0$ from the requirement that a vector maintains "constant direction" along a curve.

**Step 1: The intuitive requirement.**

A vector $V^\mu$ is "parallel transported" along a curve $x^\mu(\lambda)$ if it doesn't change direction — its covariant derivative along the curve vanishes:

$$
\frac{DV^\mu}{d\lambda} \equiv \frac{dx^\nu}{d\lambda}\nabla_\nu V^\mu = 0
$$

**Step 2: Expand the covariant derivative.**

$$
\frac{DV^\mu}{d\lambda} = \frac{dx^\nu}{d\lambda}\left(\partial_\nu V^\mu + \Gamma^\mu_{\nu\alpha}V^\alpha\right)
$$

$$
= \frac{dV^\mu}{d\lambda} + \Gamma^\mu_{\nu\alpha}\frac{dx^\nu}{d\lambda}V^\alpha = 0
$$

(using the chain rule: $\frac{dx^\nu}{d\lambda}\partial_\nu V^\mu = \frac{dV^\mu}{d\lambda}$ along the curve).

**Step 3: The parallel transport equation.**

$$
\boxed{\frac{dV^\mu}{d\lambda} + \Gamma^\mu_{\nu\alpha}\frac{dx^\nu}{d\lambda}V^\alpha = 0}
$$

This is a system of first-order ODEs for the components $V^\mu(\lambda)$ along the curve. Given initial conditions $V^\mu(0)$, the solution is unique.

**Step 4: Why this is the "right" definition.**

In flat space with Cartesian coordinates, $\Gamma^\mu_{\nu\alpha} = 0$, so parallel transport is simply $dV^\mu/d\lambda = 0$ — constant components. In curved coordinates or curved space, the Christoffel symbols compensate for the "rotation" of the coordinate basis along the curve.

**Step 5: Parallel transport preserves inner products.**

If $V^\mu$ and $W^\mu$ are both parallel-transported along a curve:

$$
\frac{d}{d\lambda}(g_{\mu\nu}V^\mu W^\nu) = (\nabla_\sigma g_{\mu\nu})\frac{dx^\sigma}{d\lambda}V^\mu W^\nu + g_{\mu\nu}\frac{DV^\mu}{d\lambda}W^\nu + g_{\mu\nu}V^\mu\frac{DW^\nu}{d\lambda}
$$

The first term vanishes by metric compatibility ($\nabla_\sigma g_{\mu\nu} = 0$), and the last two vanish by the parallel transport condition. Therefore:

$$
\frac{d}{d\lambda}(g_{\mu\nu}V^\mu W^\nu) = 0
$$

Inner products (and hence lengths and angles) are preserved under parallel transport. This is the geometric content of metric compatibility.

---

### Appendix 9.2 — Metric Compatibility: Proof that $\nabla_\rho g_{\mu\nu} = 0$

**Theorem:** The Levi-Civita connection (the unique torsion-free, metric-compatible connection) satisfies $\nabla_\rho g_{\mu\nu} = 0$.

**Proof (from the Christoffel symbol formula):**

**Step 1:** The covariant derivative of the metric:

$$
\nabla_\rho g_{\mu\nu} = \partial_\rho g_{\mu\nu} - \Gamma^\sigma_{\rho\mu}g_{\sigma\nu} - \Gamma^\sigma_{\rho\nu}g_{\mu\sigma}
$$

**Step 2:** Substitute the Christoffel symbol formula:

$$
\Gamma^\sigma_{\rho\mu} = \frac{1}{2}g^{\sigma\lambda}(\partial_\rho g_{\mu\lambda} + \partial_\mu g_{\rho\lambda} - \partial_\lambda g_{\rho\mu})
$$

**Step 3:** Compute $\Gamma^\sigma_{\rho\mu}g_{\sigma\nu}$:

$$
\Gamma^\sigma_{\rho\mu}g_{\sigma\nu} = \frac{1}{2}g^{\sigma\lambda}g_{\sigma\nu}(\partial_\rho g_{\mu\lambda} + \partial_\mu g_{\rho\lambda} - \partial_\lambda g_{\rho\mu})
$$

$$
= \frac{1}{2}\delta^\lambda_\nu(\partial_\rho g_{\mu\lambda} + \partial_\mu g_{\rho\lambda} - \partial_\lambda g_{\rho\mu})
$$

$$
= \frac{1}{2}(\partial_\rho g_{\mu\nu} + \partial_\mu g_{\rho\nu} - \partial_\nu g_{\rho\mu})
$$

**Step 4:** Similarly, $\Gamma^\sigma_{\rho\nu}g_{\mu\sigma}$:

$$
= \frac{1}{2}(\partial_\rho g_{\nu\mu} + \partial_\nu g_{\rho\mu} - \partial_\mu g_{\rho\nu})
$$

**Step 5:** Substitute into the covariant derivative:

$$
\nabla_\rho g_{\mu\nu} = \partial_\rho g_{\mu\nu} - \frac{1}{2}(\partial_\rho g_{\mu\nu} + \partial_\mu g_{\rho\nu} - \partial_\nu g_{\rho\mu}) - \frac{1}{2}(\partial_\rho g_{\nu\mu} + \partial_\nu g_{\rho\mu} - \partial_\mu g_{\rho\nu})
$$

**Step 6:** Use $g_{\mu\nu} = g_{\nu\mu}$ (symmetry) and collect terms:

$$
= \partial_\rho g_{\mu\nu} - \frac{1}{2}\partial_\rho g_{\mu\nu} - \frac{1}{2}\partial_\mu g_{\rho\nu} + \frac{1}{2}\partial_\nu g_{\rho\mu} - \frac{1}{2}\partial_\rho g_{\mu\nu} - \frac{1}{2}\partial_\nu g_{\rho\mu} + \frac{1}{2}\partial_\mu g_{\rho\nu}
$$

$$
= \partial_\rho g_{\mu\nu} - \partial_\rho g_{\mu\nu} + (-\frac{1}{2}\partial_\mu g_{\rho\nu} + \frac{1}{2}\partial_\mu g_{\rho\nu}) + (\frac{1}{2}\partial_\nu g_{\rho\mu} - \frac{1}{2}\partial_\nu g_{\rho\mu})
$$

$$
= 0 \qquad \blacksquare
$$

**Physical meaning:** Metric compatibility means that the connection "knows about" the metric — parallel transport preserves lengths and angles. This is not automatic; one could define connections that don't preserve the metric (e.g., Weyl geometry). The Levi-Civita connection is the unique connection that is both torsion-free AND metric-compatible.

**Consequence for index manipulation:** Since $\nabla_\rho g_{\mu\nu} = 0$, we can freely raise and lower indices inside covariant derivatives:

$$
\nabla_\rho(g_{\mu\nu}V^\nu) = g_{\mu\nu}\nabla_\rho V^\nu
$$

$$
\nabla_\rho V_\mu = g_{\mu\nu}\nabla_\rho V^\nu
$$

This is why we can write $\nabla_\rho V_\mu = \partial_\rho V_\mu - \Gamma^\sigma_{\rho\mu}V_\sigma$ (with a minus sign for covectors) without worrying about derivatives of the metric.

---

### Appendix 9.3 — The Geodesic Equation from Parallel Transport of the Tangent Vector

A **geodesic** is a curve whose tangent vector is parallel-transported along itself. If $U^\mu = dx^\mu/d\lambda$ is the tangent vector:

$$
\frac{DU^\mu}{d\lambda} = U^\nu\nabla_\nu U^\mu = 0
$$

Expanding:

$$
U^\nu(\partial_\nu U^\mu + \Gamma^\mu_{\nu\alpha}U^\alpha) = \frac{dU^\mu}{d\lambda} + \Gamma^\mu_{\nu\alpha}U^\nu U^\alpha = 0
$$

$$
\frac{d^2 x^\mu}{d\lambda^2} + \Gamma^\mu_{\nu\alpha}\frac{dx^\nu}{d\lambda}\frac{dx^\alpha}{d\lambda} = 0
$$

This is the **geodesic equation** — the equation of motion for a free particle in curved spacetime. It says: "go straight" (parallel-transport your velocity vector). In flat space with Cartesian coordinates ($\Gamma = 0$), this reduces to $d^2x^\mu/d\lambda^2 = 0$ — straight lines, as expected.

**References:** Carroll (arXiv:gr-qc/9712019) §3.1–3.3; Wald §3.1; MTW §8.5; Schutz §5.4.

