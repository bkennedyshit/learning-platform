---
title: "8.2 — Minkowski Spacetime & 4-Vectors"
subject: "Special & General Relativity"
catalog: advanced
audience_tier: higher-education
chapter: "8.2"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 8.2 — Minkowski Spacetime & 4-Vectors

> *"Henceforth space by itself, and time by itself, are doomed to fade away into mere shadows, and only a kind of union of the two will preserve an independent reality."*
> — Hermann Minkowski, Address to the 80th Assembly of German Natural Scientists and Physicians (1908)

Chapter 8.1 derived the Lorentz transformation as the unique linear map preserving the speed of light. Now we reveal the **geometric** structure underlying these transformations: spacetime is not merely a set of coordinates — it is a **pseudo-Riemannian manifold** equipped with the Minkowski metric $\eta_{\mu\nu}$. The Lorentz group is simply the **isometry group** of this metric, just as rotations are the isometry group of the Euclidean metric.

This geometric viewpoint — thinking of physics in terms of **4-vectors** that transform covariantly — is the language of modern theoretical physics. Every physical quantity (momentum, force, current, electromagnetic field) has a natural 4-vector or 4-tensor formulation that makes Lorentz invariance **manifest**.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Define Minkowski spacetime as a 4-dimensional pseudo-Riemannian manifold with metric signature $(-,+,+,+)$.
2. Write the metric tensor $\eta_{\mu\nu}$ and use it to raise/lower indices on 4-vectors.
3. Distinguish contravariant ($V^\mu$) and covariant ($V_\mu$) components and transform between them.
4. Construct the 4-velocity $U^\mu$, 4-momentum $p^\mu$, and 4-acceleration $a^\mu$ from first principles.
5. Prove that $U^\mu U_\mu = -c^2$ and $p^\mu p_\mu = -m^2 c^2$ (mass-shell condition).
6. Derive the energy-momentum relation $E^2 = (pc)^2 + (mc^2)^2$.
7. Compute inner products of 4-vectors and verify Lorentz invariance.
8. Express the electromagnetic field as the Faraday 2-form $F_{\mu\nu}$ (antisymmetric tensor).

---

## 🖼️ Visual Anchor — Minkowski Metric & Index Gymnastics

![math-08__8.2-fig1](math-08__8.2-fig1.svg)

The diagram shows the fundamental operation of **index gymnastics** in Minkowski spacetime: the metric $\eta_{\mu\nu}$ lowers indices (contravariant → covariant), its inverse $\eta^{\mu\nu}$ raises them. The sign flip in the time component ($V_0 = -V^0$) is the hallmark of the $(-,+,+,+)$ signature.

---

## 📚 1. Definitions

### Definition 8.2.1 — Minkowski Spacetime

**Minkowski spacetime** $(\mathbb{R}^4, \eta)$ is the 4-dimensional real vector space $\mathbb{R}^4$ equipped with the **Minkowski metric** (a non-degenerate symmetric bilinear form of signature $(-,+,+,+)$):

$$
\eta_{\mu\nu} = \text{diag}(-1, +1, +1, +1) = \begin{pmatrix} -1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

The **line element** (infinitesimal interval) is:

$$
ds^2 = \eta_{\mu\nu}\, dx^\mu\, dx^\nu = -c^2 dt^2 + dx^2 + dy^2 + dz^2
$$

**Convention note:** We use the "mostly plus" or "particle physics" convention $(-,+,+,+)$. The "mostly minus" or "GR" convention $(+,-,-,-)$ is also common (used by MTW). Physical results are convention-independent.

### Definition 8.2.2 — Contravariant and Covariant 4-Vectors

A **contravariant 4-vector** $V^\mu$ (upper index) transforms under Lorentz transformations as:

$$
V'^\mu = \Lambda^\mu{}_\nu V^\nu
$$

A **covariant 4-vector** (1-form) $V_\mu$ (lower index) transforms as:

$$
V'_\mu = (\Lambda^{-1})^\nu{}_\mu V_\nu
$$

The metric **lowers** indices:

$$
V_\mu = \eta_{\mu\nu} V^\nu
$$

Explicitly: $V_0 = \eta_{0\nu}V^\nu = -V^0$, $V_i = \eta_{i\nu}V^\nu = V^i$ for $i = 1,2,3$.

The inverse metric **raises** indices:

$$
V^\mu = \eta^{\mu\nu} V_\nu
$$

where $\eta^{\mu\nu} = \text{diag}(-1,+1,+1,+1) = \eta_{\mu\nu}$ (the Minkowski metric is its own inverse).

### Definition 8.2.3 — Lorentz-Invariant Inner Product

The **inner product** (scalar product) of two 4-vectors $A^\mu$ and $B^\mu$ is:

$$
A \cdot B = \eta_{\mu\nu} A^\mu B^\nu = A_\mu B^\mu = A^\mu B_\mu
$$

Expanded:

$$
A \cdot B = -A^0 B^0 + A^1 B^1 + A^2 B^2 + A^3 B^3
$$

This is **Lorentz-invariant**: $A' \cdot B' = A \cdot B$ in all inertial frames.

**Key difference from Euclidean:** The inner product is **indefinite** — it can be positive, negative, or zero even for non-zero vectors.

### Definition 8.2.4 — The 4-Position Vector

The **4-position** of an event is:

$$
x^\mu = (x^0, x^1, x^2, x^3) = (ct, x, y, z)
$$

Its covariant form:

$$
x_\mu = \eta_{\mu\nu} x^\nu = (-ct, x, y, z)
$$

The invariant "length squared":

$$
x_\mu x^\mu = -c^2 t^2 + x^2 + y^2 + z^2 = s^2
$$

### Definition 8.2.5 — The 4-Velocity

For a massive particle with worldline $x^\mu(\tau)$ parametrized by proper time $\tau$, the **4-velocity** is:

$$
U^\mu = \frac{dx^\mu}{d\tau}
$$

Since $d\tau = dt/\gamma$, we have $d/d\tau = \gamma\, d/dt$:

$$
U^\mu = \gamma \frac{dx^\mu}{dt} = \gamma(c, v_x, v_y, v_z) = (\gamma c, \gamma \mathbf{v})
$$

where $\mathbf{v} = d\mathbf{x}/dt$ is the ordinary 3-velocity.

### Definition 8.2.6 — The 4-Momentum

The **4-momentum** of a particle with rest mass $m$ is:

$$
p^\mu = m U^\mu = m\gamma(c, \mathbf{v}) = \left(\frac{E}{c}, \mathbf{p}\right)
$$

where:
- $E = \gamma mc^2$ is the **relativistic energy** (total energy including rest energy)
- $\mathbf{p} = \gamma m\mathbf{v}$ is the **relativistic 3-momentum**

The covariant form:

$$
p_\mu = \left(-\frac{E}{c}, \mathbf{p}\right)
$$

### Definition 8.2.7 — The 4-Acceleration

The **4-acceleration** is:

$$
a^\mu = \frac{dU^\mu}{d\tau} = \frac{d^2 x^\mu}{d\tau^2}
$$

It is always **orthogonal** to the 4-velocity: $a_\mu U^\mu = 0$ (proved in Theorem 8.2.3).

### Definition 8.2.8 — The 4-Wavevector

For a plane wave with angular frequency $\omega$ and wave vector $\mathbf{k}$:

$$
k^\mu = \left(\frac{\omega}{c}, \mathbf{k}\right)
$$

The phase $\phi = k_\mu x^\mu = -\omega t + \mathbf{k} \cdot \mathbf{x}$ is a Lorentz scalar.

For light: $k_\mu k^\mu = -\omega^2/c^2 + |\mathbf{k}|^2 = 0$ (null vector, since $\omega = c|\mathbf{k}|$).

### Definition 8.2.9 — The Electromagnetic Field Tensor (Faraday Tensor)

The electromagnetic field is encoded in an **antisymmetric $(0,2)$-tensor** $F_{\mu\nu} = -F_{\nu\mu}$:

$$
F_{\mu\nu} = \begin{pmatrix} 0 & E_x/c & E_y/c & E_z/c \\ -E_x/c & 0 & B_z & -B_y \\ -E_y/c & -B_z & 0 & B_x \\ -E_z/c & B_y & -B_x & 0 \end{pmatrix}
$$

This unifies the electric and magnetic fields into a single geometric object. Under Lorentz transformations, $\mathbf{E}$ and $\mathbf{B}$ mix — they are not independent physical entities but components of $F_{\mu\nu}$.




---

## 📐 2. Axioms / Postulates

### Axiom 8.2.1 — Metric Structure of Spacetime

Spacetime is a 4-dimensional affine space equipped with a **non-degenerate, symmetric bilinear form** $\eta$ of signature $(-,+,+,+)$. This metric determines:
- Causal structure (timelike/spacelike/null separation)
- Proper time along worldlines
- The invariant inner product of 4-vectors

### Axiom 8.2.2 — Lorentz Covariance of Physical Laws

All fundamental physical laws must be expressible as **tensor equations** — equations between objects that transform covariantly under the Lorentz group. If a tensor equation holds in one inertial frame, it holds in all inertial frames.

**Consequence:** To check if a proposed law is relativistically valid, write it in 4-vector/tensor notation. If both sides transform identically, the law is automatically Lorentz-covariant.

### Axiom 8.2.3 — Conservation of 4-Momentum

In any isolated system, the total 4-momentum is conserved:

$$
\sum_{\text{initial}} p^\mu_i = \sum_{\text{final}} p^\mu_f
$$

This single equation encodes **both** conservation of energy ($\mu = 0$) and conservation of 3-momentum ($\mu = 1,2,3$).

---

## 🛡️ 3. Lemmas

### Lemma 8.2.1 — The Metric Preserves Under Lorentz Transformations

**Statement:** A Lorentz transformation $\Lambda^\mu{}_\nu$ satisfies:

$$
\eta_{\mu\nu} = \eta_{\alpha\beta}\, \Lambda^\alpha{}_\mu\, \Lambda^\beta{}_\nu
$$

or in matrix notation: $\Lambda^T \eta \Lambda = \eta$.

**Proof:** The defining property of a Lorentz transformation is that it preserves the spacetime interval. For any two 4-vectors $A^\mu$, $B^\mu$:

$$
\eta_{\mu\nu} A'^\mu B'^\nu = \eta_{\mu\nu} A^\mu B^\nu
$$

Substitute $A'^\mu = \Lambda^\mu{}_\alpha A^\alpha$ and $B'^\nu = \Lambda^\nu{}_\beta B^\beta$:

$$
\eta_{\mu\nu} \Lambda^\mu{}_\alpha \Lambda^\nu{}_\beta A^\alpha B^\beta = \eta_{\alpha\beta} A^\alpha B^\beta
$$

Since this holds for **all** $A^\alpha$ and $B^\beta$:

$$
\eta_{\mu\nu} \Lambda^\mu{}_\alpha \Lambda^\nu{}_\beta = \eta_{\alpha\beta}
$$

Relabeling indices: $\eta_{\alpha\beta} \Lambda^\alpha{}_\mu \Lambda^\beta{}_\nu = \eta_{\mu\nu}$. $\blacksquare$

### Lemma 8.2.2 — Index Lowering/Raising is Consistent

**Statement:** Lowering then raising an index returns the original vector: $\eta^{\mu\alpha}\eta_{\alpha\nu} = \delta^\mu{}_\nu$.

**Proof:** Direct computation. Since $\eta^{\mu\alpha} = \text{diag}(-1,1,1,1)$ and $\eta_{\alpha\nu} = \text{diag}(-1,1,1,1)$:

$$
\eta^{\mu\alpha}\eta_{\alpha\nu} = \sum_{\alpha=0}^{3} \eta^{\mu\alpha}\eta_{\alpha\nu}
$$

For $\mu = \nu = 0$: $\eta^{00}\eta_{00} = (-1)(-1) = 1 = \delta^0{}_0$. ✓

For $\mu = \nu = i$ (spatial): $\eta^{ii}\eta_{ii} = (1)(1) = 1 = \delta^i{}_i$. ✓

For $\mu \neq \nu$: all cross terms vanish because $\eta$ is diagonal. ✓

Therefore $\eta^{\mu\alpha}\eta_{\alpha\nu} = \delta^\mu{}_\nu$. $\blacksquare$

### Lemma 8.2.3 — Proper Time as Arc Length

**Statement:** The proper time along a timelike worldline $x^\mu(\lambda)$ is:

$$
\tau = \int \frac{1}{c}\sqrt{-\eta_{\mu\nu}\frac{dx^\mu}{d\lambda}\frac{dx^\nu}{d\lambda}}\, d\lambda
$$

This is independent of the parametrization $\lambda$.

**Proof:** Under reparametrization $\lambda \to \tilde{\lambda}(\lambda)$:

$$
\frac{dx^\mu}{d\tilde{\lambda}} = \frac{dx^\mu}{d\lambda}\frac{d\lambda}{d\tilde{\lambda}}
$$

$$
\sqrt{-\eta_{\mu\nu}\frac{dx^\mu}{d\tilde{\lambda}}\frac{dx^\nu}{d\tilde{\lambda}}}\, d\tilde{\lambda} = \sqrt{-\eta_{\mu\nu}\frac{dx^\mu}{d\lambda}\frac{dx^\nu}{d\lambda}}\left|\frac{d\lambda}{d\tilde{\lambda}}\right| d\tilde{\lambda}
$$

$$
= \sqrt{-\eta_{\mu\nu}\frac{dx^\mu}{d\lambda}\frac{dx^\nu}{d\lambda}}\, d\lambda
$$

The integrand is invariant. $\blacksquare$

---

## 👑 4. Theorems

### Theorem 8.2.1 — Mass-Shell Condition (Energy-Momentum Relation)

**Statement:** For a particle of rest mass $m$:

$$
p_\mu p^\mu = -m^2 c^2
$$

Equivalently:

$$
E^2 = (pc)^2 + (mc^2)^2
$$

where $E = \gamma mc^2$ and $p = |\mathbf{p}| = \gamma mv$.

### Theorem 8.2.2 — Normalization of the 4-Velocity

**Statement:** The 4-velocity of any massive particle satisfies:

$$
U_\mu U^\mu = \eta_{\mu\nu} U^\mu U^\nu = -c^2
$$

This is a **constant** — independent of the particle's speed.

### Theorem 8.2.3 — Orthogonality of 4-Acceleration and 4-Velocity

**Statement:** $a_\mu U^\mu = 0$ — the 4-acceleration is always spacelike and perpendicular to the 4-velocity.

### Theorem 8.2.4 — Invariant Mass in Collisions

**Statement:** For a system of particles, the **invariant mass** $M$ of the system is defined by:

$$
-M^2 c^2 = \left(\sum_i p^\mu_i\right)\left(\sum_j p_{j\mu}\right) = P_\mu P^\mu
$$

where $P^\mu = \sum_i p^\mu_i$ is the total 4-momentum. $M$ is Lorentz-invariant and is conserved in isolated systems.

### Theorem 8.2.5 — Photon 4-Momentum

**Statement:** A photon ($m = 0$) has 4-momentum:

$$
p^\mu = \left(\frac{E}{c}, \mathbf{p}\right) = \frac{E}{c}(1, \hat{n})
$$

where $\hat{n}$ is the unit vector in the direction of propagation. The mass-shell condition gives $p_\mu p^\mu = 0$ (null vector), consistent with $E = pc$.

---

## ✍️ 5. Proofs / Derivations

### Proof 8.2.1 — Normalization of the 4-Velocity

**Claim:** $U_\mu U^\mu = -c^2$.

**Step 1:** Write $U^\mu = \gamma(c, v_x, v_y, v_z)$.

**Step 2:** Compute the invariant:

$$
U_\mu U^\mu = \eta_{\mu\nu} U^\mu U^\nu = -(U^0)^2 + (U^1)^2 + (U^2)^2 + (U^3)^2
$$

**Step 3:** Substitute:

$$
= -(\gamma c)^2 + (\gamma v_x)^2 + (\gamma v_y)^2 + (\gamma v_z)^2
$$

$$
= \gamma^2(-c^2 + v_x^2 + v_y^2 + v_z^2)
$$

$$
= \gamma^2(-c^2 + v^2)
$$

**Step 4:** Factor:

$$
= \gamma^2 \cdot c^2\left(-1 + \frac{v^2}{c^2}\right) = \gamma^2 c^2(-(1 - \beta^2))
$$

**Step 5:** Use $\gamma^2 = 1/(1-\beta^2)$:

$$
= \frac{c^2}{1-\beta^2} \cdot (-(1-\beta^2)) = -c^2
$$

$$
\boxed{U_\mu U^\mu = -c^2} \qquad \blacksquare
$$

**Physical meaning:** The 4-velocity is a **unit timelike vector** (in units where $c = 1$, it has "length" $-1$). As the particle speeds up, the spatial components grow but the time component grows to compensate, keeping the norm fixed.

---

### Proof 8.2.2 — Energy-Momentum Relation (Mass-Shell Condition)

**Claim:** $p_\mu p^\mu = -m^2 c^2$, equivalently $E^2 = p^2 c^2 + m^2 c^4$.

**Step 1:** Since $p^\mu = mU^\mu$:

$$
p_\mu p^\mu = m^2 U_\mu U^\mu = m^2(-c^2) = -m^2 c^2
$$

**Step 2:** Expand in components:

$$
p_\mu p^\mu = -(p^0)^2 + |\mathbf{p}|^2 = -\frac{E^2}{c^2} + p^2
$$

**Step 3:** Set equal:

$$
-\frac{E^2}{c^2} + p^2 = -m^2 c^2
$$

**Step 4:** Rearrange:

$$
\frac{E^2}{c^2} = p^2 + m^2 c^2
$$

$$
\boxed{E^2 = (pc)^2 + (mc^2)^2}
$$

**Special cases:**
- At rest ($p = 0$): $E = mc^2$ (Einstein's famous equation)
- Massless ($m = 0$): $E = pc$ (photons)
- Ultra-relativistic ($p \gg mc$): $E \approx pc$ $\blacksquare$

---

### Proof 8.2.3 — Orthogonality of 4-Acceleration and 4-Velocity

**Claim:** $a_\mu U^\mu = 0$.

**Step 1:** Start from $U_\mu U^\mu = -c^2$ (constant).

**Step 2:** Differentiate both sides with respect to proper time $\tau$:

$$
\frac{d}{d\tau}(U_\mu U^\mu) = \frac{d}{d\tau}(-c^2) = 0
$$

**Step 3:** Apply the product rule (the metric $\eta_{\mu\nu}$ is constant):

$$
\frac{dU_\mu}{d\tau} U^\mu + U_\mu \frac{dU^\mu}{d\tau} = 0
$$

**Step 4:** Both terms are the same scalar (rename dummy indices):

$$
2\, U_\mu \frac{dU^\mu}{d\tau} = 0
$$

**Step 5:** Recognize $a^\mu = dU^\mu/d\tau$:

$$
U_\mu a^\mu = 0 \qquad \blacksquare
$$

**Consequence:** In the instantaneous rest frame ($U^\mu = (c, 0, 0, 0)$), orthogonality gives $a^0 = 0$, so the 4-acceleration is purely spatial: $a^\mu = (0, \mathbf{a}_{\text{proper}})$. The magnitude $a_\mu a^\mu = |\mathbf{a}_{\text{proper}}|^2 > 0$ is a positive Lorentz scalar — the 4-acceleration is always **spacelike**.

---

### Proof 8.2.4 — Lorentz Transformation of the Faraday Tensor

**Claim:** Under a Lorentz boost along $x$ with velocity $v$, the electric and magnetic fields transform as:

$$
E'_x = E_x, \qquad B'_x = B_x
$$

$$
E'_y = \gamma(E_y - vB_z), \qquad B'_y = \gamma(B_y + vE_z/c^2)
$$

$$
E'_z = \gamma(E_z + vB_y), \qquad B'_z = \gamma(B_z - vE_y/c^2)
$$

**Step 1:** The Faraday tensor transforms as a rank-2 covariant tensor:

$$
F'_{\mu\nu} = \Lambda^\alpha{}_\mu \Lambda^\beta{}_\nu F_{\alpha\beta}
$$

Wait — since $F_{\mu\nu}$ has lower indices, it transforms with the inverse:

$$
F'_{\mu\nu} = (\Lambda^{-1})^\alpha{}_\mu (\Lambda^{-1})^\beta{}_\nu F_{\alpha\beta}
$$

Actually, for a $(0,2)$-tensor with both indices down:

$$
F'_{\mu\nu} = (\Lambda^{-1})^\alpha{}_\mu (\Lambda^{-1})^\beta{}_\nu F_{\alpha\beta}
$$

But it is equivalent (and simpler) to use the mixed form. Let us use the contravariant form $F^{\mu\nu} = \eta^{\mu\alpha}\eta^{\nu\beta}F_{\alpha\beta}$:

$$
F'^{\mu\nu} = \Lambda^\mu{}_\alpha \Lambda^\nu{}_\beta F^{\alpha\beta}
$$

**Step 2:** For the boost along $x$: $\Lambda^0{}_0 = \gamma$, $\Lambda^0{}_1 = -\beta\gamma$, $\Lambda^1{}_0 = -\beta\gamma$, $\Lambda^1{}_1 = \gamma$, $\Lambda^2{}_2 = \Lambda^3{}_3 = 1$.

**Step 3:** Compute $F'^{01} = E'_x/c$:

$$
F'^{01} = \Lambda^0{}_\alpha \Lambda^1{}_\beta F^{\alpha\beta}
$$

The non-zero contributions come from $(\alpha,\beta) \in \{(0,1),(1,0)\}$ (since $\Lambda^0$ only has components for $\alpha = 0,1$ and $\Lambda^1$ only for $\beta = 0,1$):

$$
= \Lambda^0{}_0 \Lambda^1{}_1 F^{01} + \Lambda^0{}_1 \Lambda^1{}_0 F^{10}
$$

$$
= \gamma \cdot \gamma \cdot F^{01} + (-\beta\gamma)(-\beta\gamma) F^{10}
$$

Since $F^{10} = -F^{01}$:

$$
= \gamma^2 F^{01} - \beta^2\gamma^2 F^{01} = \gamma^2(1-\beta^2)F^{01} = F^{01}
$$

Therefore $E'_x = E_x$. ✓ (Parallel component unchanged.)

**Step 4:** Compute $F'^{02} = E'_y/c$:

$$
F'^{02} = \Lambda^0{}_\alpha \Lambda^2{}_\beta F^{\alpha\beta} = \Lambda^0{}_\alpha \delta^2_\beta F^{\alpha\beta} = \Lambda^0{}_\alpha F^{\alpha 2}
$$

$$
= \Lambda^0{}_0 F^{02} + \Lambda^0{}_1 F^{12} = \gamma F^{02} + (-\beta\gamma) F^{12}
$$

$$
= \gamma \frac{E_y}{c} - \beta\gamma B_z
$$

Therefore:

$$
\frac{E'_y}{c} = \gamma\left(\frac{E_y}{c} - \beta B_z\right) \implies E'_y = \gamma(E_y - vB_z) \qquad \blacksquare
$$

The remaining components follow by analogous calculations.




---

## 🧮 6. Worked Examples

### Example 8.2.1 — Energy-Momentum of a Relativistic Proton

**Problem:** A proton ($m_p = 938.3$ MeV/$c^2$) has kinetic energy $K = 2000$ MeV. Find: (a) total energy $E$, (b) momentum $p$, (c) velocity $\beta$, (d) Lorentz factor $\gamma$.

**Solution:**

**(a) Total energy:**

$$
E = K + mc^2 = 2000 + 938.3 = 2938.3\,\text{MeV}
$$

**(b) Momentum** from the mass-shell condition:

$$
E^2 = (pc)^2 + (mc^2)^2
$$

$$
(pc)^2 = E^2 - (mc^2)^2 = (2938.3)^2 - (938.3)^2
$$

$$
= 8{,}633{,}606 - 880{,}407 = 7{,}753{,}199\,\text{MeV}^2
$$

$$
pc = \sqrt{7{,}753{,}199} = 2784.5\,\text{MeV}
$$

$$
p = 2784.5\,\text{MeV}/c
$$

**(c) Velocity:**

$$
\beta = \frac{pc}{E} = \frac{2784.5}{2938.3} = 0.9477
$$

**(d) Lorentz factor:**

$$
\gamma = \frac{E}{mc^2} = \frac{2938.3}{938.3} = 3.131
$$

**Verification:** $\gamma = 1/\sqrt{1-\beta^2} = 1/\sqrt{1-0.898} = 1/\sqrt{0.102} = 3.13$ ✓

---

### Example 8.2.2 — Invariant Mass of a Two-Photon System

**Problem:** Two photons travel in opposite directions, each with energy $E_\gamma = 500$ MeV. Find the invariant mass of the system.

**Solution:**

**Step 1:** Write the 4-momenta. Photon 1 travels in $+x$, photon 2 in $-x$:

$$
p_1^\mu = \frac{E_\gamma}{c}(1, 1, 0, 0), \qquad p_2^\mu = \frac{E_\gamma}{c}(1, -1, 0, 0)
$$

**Step 2:** Total 4-momentum:

$$
P^\mu = p_1^\mu + p_2^\mu = \frac{E_\gamma}{c}(2, 0, 0, 0) = \frac{2E_\gamma}{c}(1, 0, 0, 0)
$$

**Step 3:** Invariant mass:

$$
-M^2 c^2 = P_\mu P^\mu = \eta_{\mu\nu}P^\mu P^\nu = -\left(\frac{2E_\gamma}{c}\right)^2 \cdot c^2 \cdot 1 = -(2E_\gamma)^2/c^2 \cdot c^2
$$

Wait, let's be careful with units. Using $c = 1$ units:

$$
P^\mu = (2E_\gamma, 0, 0, 0)
$$

$$
P_\mu P^\mu = -(2E_\gamma)^2 + 0 = -(2E_\gamma)^2
$$

$$
-M^2 = -(2E_\gamma)^2 \implies M = 2E_\gamma = 1000\,\text{MeV}/c^2
$$

**Result:** The invariant mass is $M = 1000$ MeV/$c^2$, even though each individual photon is massless! The system has mass because the photons have non-zero relative momentum.

**Physical interpretation:** This is exactly the process $e^+e^- \to \gamma\gamma$ in reverse — two photons can create a particle-antiparticle pair if their invariant mass exceeds $2m_e c^2$.

---

### Example 8.2.3 — 4-Velocity Transformation Under a Boost

**Problem:** A particle moves at $\mathbf{v} = (0.6c, 0, 0)$ in frame $S$. Frame $S'$ moves at $V = 0.8c$ along $x$ relative to $S$. Find the 4-velocity in both frames and verify $U_\mu U^\mu = -c^2$ in both.

**Solution:**

**In frame $S$:**

$$
\gamma_v = \frac{1}{\sqrt{1 - 0.36}} = \frac{1}{0.8} = 1.25
$$

$$
U^\mu = \gamma_v(c, v_x, 0, 0) = (1.25c, 0.75c, 0, 0)
$$

Check: $U_\mu U^\mu = -(1.25c)^2 + (0.75c)^2 = c^2(-1.5625 + 0.5625) = -c^2$ ✓

**Boost to frame $S'$** ($V = 0.8c$, $\beta_V = 0.8$, $\gamma_V = 5/3$):

$$
U'^0 = \gamma_V(U^0 - \beta_V U^1) = \frac{5}{3}(1.25c - 0.8 \times 0.75c) = \frac{5}{3}(1.25c - 0.6c) = \frac{5}{3}(0.65c) = \frac{13}{12}c \cdot \frac{20}{13}
$$

Let me redo this carefully:

$$
U'^0 = \frac{5}{3}(1.25c - 0.8 \times 0.75c) = \frac{5}{3}(1.25 - 0.60)c = \frac{5}{3} \times 0.65c = \frac{3.25}{3}c = \frac{13}{12}c
$$

$$
U'^1 = \gamma_V(U^1 - \beta_V U^0) = \frac{5}{3}(0.75c - 0.8 \times 1.25c) = \frac{5}{3}(0.75 - 1.00)c = \frac{5}{3}(-0.25c) = -\frac{5}{12}c
$$

Check in $S'$: $U'_\mu U'^\mu = -(13/12)^2 c^2 + (5/12)^2 c^2 = c^2[-(169/144) + (25/144)] = c^2(-144/144) = -c^2$ ✓

The velocity in $S'$: $v'_x = U'^1/U'^0 \cdot c = (-5/12)/(13/12) \cdot c = -5c/13 \approx -0.385c$.

This matches velocity addition: $v'_x = (0.6c - 0.8c)/(1 - 0.6 \times 0.8) = -0.2c/0.52 = -5c/13$ ✓

---

### Example 8.2.4 — Compton Scattering Kinematics

**Problem:** A photon of energy $E_\gamma$ scatters off an electron at rest. Derive the Compton formula for the scattered photon energy $E'_\gamma$ as a function of scattering angle $\theta$.

**Solution:**

**Step 1:** Initial 4-momenta (using $c = 1$):

$$
p^\mu_\gamma = (E_\gamma, E_\gamma, 0, 0) \quad \text{(photon along } x\text{)}
$$

$$
p^\mu_e = (m_e, 0, 0, 0) \quad \text{(electron at rest)}
$$

**Step 2:** Final 4-momenta:

$$
p'^\mu_\gamma = (E'_\gamma, E'_\gamma\cos\theta, E'_\gamma\sin\theta, 0)
$$

$$
p'^\mu_e = (E'_e, \mathbf{p}'_e) \quad \text{(unknown)}
$$

**Step 3:** Conservation: $p_\gamma + p_e = p'_\gamma + p'_e$, so $p'_e = p_\gamma + p_e - p'_\gamma$.

**Step 4:** Square both sides using $p'_{e\mu}p'^{\mu}_e = -m_e^2$:

$$
(p_\gamma + p_e - p'_\gamma)_\mu(p_\gamma + p_e - p'_\gamma)^\mu = -m_e^2
$$

**Step 5:** Expand (using $p_\gamma^2 = 0$, $p_e^2 = -m_e^2$, $p'^2_\gamma = 0$):

$$
p_\gamma^2 + p_e^2 + p'^2_\gamma + 2p_\gamma \cdot p_e - 2p_\gamma \cdot p'_\gamma - 2p_e \cdot p'_\gamma = -m_e^2
$$

$$
0 + (-m_e^2) + 0 + 2p_\gamma \cdot p_e - 2p_\gamma \cdot p'_\gamma - 2p_e \cdot p'_\gamma = -m_e^2
$$

$$
2p_\gamma \cdot p_e - 2p_\gamma \cdot p'_\gamma - 2p_e \cdot p'_\gamma = 0
$$

**Step 6:** Compute each inner product:

$$
p_\gamma \cdot p_e = -E_\gamma m_e + 0 = -E_\gamma m_e
$$

$$
p_\gamma \cdot p'_\gamma = -E_\gamma E'_\gamma + E_\gamma E'_\gamma\cos\theta = -E_\gamma E'_\gamma(1 - \cos\theta)
$$

$$
p_e \cdot p'_\gamma = -m_e E'_\gamma
$$

**Step 7:** Substitute:

$$
2(-E_\gamma m_e) - 2(-E_\gamma E'_\gamma(1-\cos\theta)) - 2(-m_e E'_\gamma) = 0
$$

$$
-2E_\gamma m_e + 2E_\gamma E'_\gamma(1-\cos\theta) + 2m_e E'_\gamma = 0
$$

**Step 8:** Divide by $2E_\gamma E'_\gamma$:

$$
-\frac{m_e}{E'_\gamma} + (1-\cos\theta) + \frac{m_e}{E_\gamma} = 0
$$

$$
\frac{m_e}{E'_\gamma} - \frac{m_e}{E_\gamma} = 1 - \cos\theta
$$

$$
\frac{1}{E'_\gamma} - \frac{1}{E_\gamma} = \frac{1-\cos\theta}{m_e}
$$

Restoring $c$: replace $m_e \to m_e c^2$:

$$
\boxed{\frac{1}{E'_\gamma} - \frac{1}{E_\gamma} = \frac{1 - \cos\theta}{m_e c^2}}
$$

In terms of wavelength ($E = hc/\lambda$):

$$
\lambda' - \lambda = \frac{h}{m_e c}(1 - \cos\theta) = \lambda_C(1 - \cos\theta)
$$

where $\lambda_C = h/(m_e c) = 2.43 \times 10^{-12}$ m is the **Compton wavelength**.

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- **Previous:** [8.1 - Special Relativity Postulates & Lorentz Boosts](8.1---Special-Relativity-Postulates-&-Lorentz-Boosts)
- **Next:** [8.3 - Covariant Relativistic Dynamics](8.3---Covariant-Relativistic-Dynamics)
- **Tensor foundations:** [2.8 - SVD & Tensors](2.8---SVD-&-Tensors) — Einstein summation, index notation
- **Differential forms:** [1.8 - Exterior Algebra & Differential Forms](1.8---Exterior-Algebra-&-Differential-Forms) — $F_{\mu\nu}$ as a 2-form
- **Electrodynamics:** [7.7 - Relativistic Electrodynamics & Four-Vectors](7.7---Relativistic-Electrodynamics-&-Four-Vectors) — full covariant Maxwell theory

### External References
1. **Carroll, S.** (1997). *Lecture Notes on General Relativity*, arXiv:gr-qc/9712019. §1.2–1.4: Vectors, dual vectors, tensors.
2. **Susskind, L. & Friedman, A.** (2017). *Special Relativity and Classical Field Theory: The Theoretical Minimum*. Basic Books.
3. **Jackson, J.D.** (1999). *Classical Electrodynamics* (3rd ed.). Wiley. Chapter 11: Special Theory of Relativity.
4. **Misner, Thorne & Wheeler** (1973). *Gravitation*. Chapter 2: Foundations of Special Relativistic Physics.
5. **Rindler, W.** (2006). *Relativity: Special, General, and Cosmological* (2nd ed.). Oxford University Press.

---

*Next: [8.3 - Covariant Relativistic Dynamics](8.3---Covariant-Relativistic-Dynamics) →*



---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.2.E1 — Light-Cone Coordinates and Null Decomposition

**Problem:** Define light-cone coordinates $u = ct - x$, $v = ct + x$ in 2D Minkowski space. (a) Express the metric in these coordinates. (b) Classify intervals using $(u, v)$. (c) Show that a Lorentz boost becomes a simple rescaling.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**(a) Metric in light-cone coordinates.**

Start from the 2D Minkowski line element:

$$
ds^2 = -c^2 dt^2 + dx^2
$$

Express $ct$ and $x$ in terms of $u, v$:

$$
ct = \frac{v + u}{2}, \qquad x = \frac{v - u}{2}
$$

Compute differentials:

$$
c\,dt = \frac{dv + du}{2}, \qquad dx = \frac{dv - du}{2}
$$

Substitute:

$$
ds^2 = -\left(\frac{dv + du}{2}\right)^2 + \left(\frac{dv - du}{2}\right)^2
$$

$$
= -\frac{1}{4}(dv^2 + 2\,du\,dv + du^2) + \frac{1}{4}(dv^2 - 2\,du\,dv + du^2)
$$

$$
= \frac{1}{4}(-dv^2 - 2\,du\,dv - du^2 + dv^2 - 2\,du\,dv + du^2)
$$

$$
= \frac{1}{4}(-4\,du\,dv) = -du\,dv
$$

$$
\boxed{ds^2 = -du\,dv}
$$

The metric tensor in $(u,v)$ coordinates:

$$
g_{\mu\nu} = \begin{pmatrix} 0 & -1/2 \\ -1/2 & 0 \end{pmatrix}, \qquad g^{\mu\nu} = \begin{pmatrix} 0 & -2 \\ -2 & 0 \end{pmatrix}
$$

**(b) Interval classification:**

$$
ds^2 = -du\,dv = -\Delta u\,\Delta v
$$

- **Timelike** ($ds^2 \lt  0$): $\Delta u\,\Delta v \gt  0$ (both positive or both negative)
- **Spacelike** ($ds^2 \gt  0$): $\Delta u\,\Delta v \lt  0$ (opposite signs)
- **Null** ($ds^2 = 0$): $\Delta u = 0$ or $\Delta v = 0$ (one coordinate constant)

Null rays are simply lines of constant $u$ (right-moving light: $ct - x = \text{const}$) or constant $v$ (left-moving light: $ct + x = \text{const}$).

**(c) Lorentz boost as rescaling.**

Under a boost with rapidity $\phi$:

$$
ct' = ct\cosh\phi - x\sinh\phi, \qquad x' = -ct\sinh\phi + x\cosh\phi
$$

Compute $u' = ct' - x'$:

$$
u' = ct(\cosh\phi + \sinh\phi) - x(\sinh\phi + \cosh\phi) = e^\phi(ct - x) = e^\phi u
$$

Compute $v' = ct' + x'$:

$$
v' = ct(\cosh\phi - \sinh\phi) + x(-\sinh\phi + \cosh\phi) = e^{-\phi}(ct + x) = e^{-\phi} v
$$

$$
\boxed{u' = e^\phi u, \qquad v' = e^{-\phi} v}
$$

A Lorentz boost is a **rescaling** of light-cone coordinates! The product $u'v' = uv$ is invariant (as it must be, since $ds^2 = -du\,dv$). This makes light-cone coordinates extremely powerful for analyzing null rays and causal structure.

</details>

---

### Example 8.2.E2 — Spacelike, Timelike, and Null: Complete Classification

**Problem:** For each pair of events, compute $s^2$, classify the interval, and state the physical consequence:

(i) $A = (0,0,0,0)$, $B = (5, 3, 0, 0)$ (units: meters)

(ii) $A = (0,0,0,0)$, $B = (3, 5, 0, 0)$

(iii) $A = (0,0,0,0)$, $B = (4, 3, 2, \sqrt{3})$

<details>
<summary>🔍 View Step-by-Step Solution</summary>

Using signature $(-,+,+,+)$: $s^2 = -(c\Delta t)^2 + (\Delta x)^2 + (\Delta y)^2 + (\Delta z)^2 = -(\Delta x^0)^2 + |\Delta\mathbf{x}|^2$.

**(i)** $\Delta x^\mu = (5, 3, 0, 0)$:

$$
s^2 = -(5)^2 + (3)^2 + 0 + 0 = -25 + 9 = -16\,\text{m}^2
$$

**Timelike** ($s^2 \lt  0$). Physical consequences:
- A causal signal can connect A and B.
- There exists a frame where both events occur at the same spatial location (the rest frame of an observer traveling from A to B).
- The proper time between events: $\Delta\tau = \sqrt{-s^2}/c = 4/c$ meters of time $= 4$ m$/c$.
- No frame exists where A and B are simultaneous.

**(ii)** $\Delta x^\mu = (3, 5, 0, 0)$:

$$
s^2 = -(3)^2 + (5)^2 = -9 + 25 = 16\,\text{m}^2
$$

**Spacelike** ($s^2 \gt  0$). Physical consequences:
- No causal signal can connect A and B (would require $v \gt  c$).
- There exists a frame where both events are simultaneous.
- The proper distance: $\Delta\ell = \sqrt{s^2} = 4$ m.
- The time-ordering of A and B is frame-dependent.

**(iii)** $\Delta x^\mu = (4, 3, 2, \sqrt{3})$:

$$
s^2 = -(4)^2 + (3)^2 + (2)^2 + (\sqrt{3})^2 = -16 + 9 + 4 + 3 = 0
$$

**Null** (lightlike, $s^2 = 0$). Physical consequences:
- A light signal connects A and B exactly.
- The proper time along the path is zero: $\Delta\tau = 0$.
- No frame exists where the events are simultaneous or co-located (except in the degenerate limit $v \to c$).
- The spatial distance equals the time distance: $|\Delta\mathbf{x}| = c|\Delta t|$, i.e., $\sqrt{9+4+3} = 4$ ✓.

</details>

---

### Example 8.2.E3 — Orthogonality of 4-Velocity and 4-Acceleration

**Problem:** Prove that the 4-acceleration $a^\mu = dU^\mu/d\tau$ is always orthogonal to the 4-velocity $U^\mu$ in Minkowski spacetime: $\eta_{\mu\nu}U^\mu a^\nu = 0$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Start from the normalization condition of 4-velocity.

The 4-velocity satisfies $U_\mu U^\mu = -c^2$ (with signature $(-,+,+,+)$). This is a constant — it holds for all proper time $\tau$.

**Step 2:** Differentiate both sides with respect to proper time $\tau$:

$$
\frac{d}{d\tau}(U_\mu U^\mu) = \frac{d}{d\tau}(-c^2) = 0
$$

**Step 3:** Apply the product rule. Since $\eta_{\mu\nu}$ is constant (flat spacetime):

$$
\frac{d}{d\tau}(\eta_{\mu\nu}U^\mu U^\nu) = \eta_{\mu\nu}\frac{dU^\mu}{d\tau}U^\nu + \eta_{\mu\nu}U^\mu\frac{dU^\nu}{d\tau} = 0
$$

**Step 4:** Recognize $dU^\mu/d\tau = a^\mu$ (the 4-acceleration):

$$
\eta_{\mu\nu}a^\mu U^\nu + \eta_{\mu\nu}U^\mu a^\nu = 0
$$

Both terms are the same scalar (just relabeling dummy indices $\mu \leftrightarrow \nu$):

$$
2\,\eta_{\mu\nu}U^\mu a^\nu = 0
$$

$$
\boxed{U_\mu a^\mu = U \cdot a = 0}
$$

**Step 5: Physical interpretation.**

In the instantaneous rest frame of the particle, $U^\mu = (c, 0, 0, 0)$. The orthogonality condition gives:

$$
U_\mu a^\mu = -c\, a^0 + 0 = 0 \implies a^0 = 0
$$

So in the rest frame, the 4-acceleration is purely spatial: $a^\mu = (0, \mathbf{a}_{\text{proper}})$. The magnitude $a_\mu a^\mu = |\mathbf{a}_{\text{proper}}|^2 \gt  0$ is the square of the proper acceleration felt by the particle (what an accelerometer reads).

This orthogonality is the relativistic generalization of the fact that, for uniform circular motion, the acceleration is perpendicular to the velocity. In relativity, it holds for **all** motion — the 4-velocity and 4-acceleration are always Minkowski-orthogonal.

</details>

---

## 📘 9. Appendix: Extended Derivations & Special Cases

### Appendix 9.1 — Proof: Invariance of $g_{\mu\nu}U^\mu U^\nu = -c^2$

The normalization $U_\mu U^\mu = -c^2$ is not a convention — it is a direct consequence of the definition of 4-velocity and the invariance of proper time.

**Definition.** The 4-velocity is:

$$
U^\mu = \frac{dx^\mu}{d\tau}
$$

where $\tau$ is proper time along the worldline.

**Step 1:** The proper time interval is defined by:

$$
c^2 d\tau^2 = -ds^2 = -\eta_{\mu\nu}dx^\mu dx^\nu
$$

**Step 2:** Divide both sides by $d\tau^2$:

$$
c^2 = -\eta_{\mu\nu}\frac{dx^\mu}{d\tau}\frac{dx^\nu}{d\tau} = -\eta_{\mu\nu}U^\mu U^\nu
$$

$$
\boxed{\eta_{\mu\nu}U^\mu U^\nu = -c^2}
$$

This holds in **every** inertial frame because both $\eta_{\mu\nu}$ and $U^\mu$ transform covariantly — the contraction is a Lorentz scalar.

**Explicit verification.** In the particle's rest frame: $U^\mu = (c, 0, 0, 0)$, so $\eta_{\mu\nu}U^\mu U^\nu = -c^2$. Under a boost to a frame where the particle moves at $\mathbf{v}$: $U^\mu = \gamma(c, \mathbf{v})$, so:

$$
\eta_{\mu\nu}U^\mu U^\nu = -\gamma^2 c^2 + \gamma^2 v^2 = -\gamma^2 c^2(1 - v^2/c^2) = -\gamma^2 c^2 / \gamma^2 = -c^2 \quad \checkmark
$$

**Why this matters:** The constraint $U \cdot U = -c^2$ means the 4-velocity lives on a **hyperboloid** in Minkowski space (the "mass shell" for a unit-mass particle). The space of all possible 4-velocities is the 3-dimensional hyperbolic space $H^3$ — the velocity space of special relativity is hyperbolic, not Euclidean.

---

### Appendix 9.2 — The Energy-Momentum 4-Vector: Invariant Mass as a Lorentz Scalar

The 4-momentum $p^\mu = mU^\mu = m\gamma(c, \mathbf{v}) = (E/c, \mathbf{p})$ satisfies:

$$
p_\mu p^\mu = -m^2 c^2
$$

This is the **mass-shell condition** — the relativistic energy-momentum relation:

$$
-\frac{E^2}{c^2} + |\mathbf{p}|^2 = -m^2 c^2 \implies E^2 = (pc)^2 + (mc^2)^2
$$

**For a system of particles**, the total 4-momentum is $P^\mu = \sum_i p_i^\mu$. The invariant mass of the system is:

$$
M^2 c^2 = -P_\mu P^\mu = -\left(\sum_i p_i^\mu\right)\left(\sum_j p_{j\mu}\right)
$$

This is **not** the sum of individual masses — it includes the kinetic energy of relative motion and interaction energy. For example, a proton has mass 938.3 MeV/$c^2$, but its constituent quarks have masses totaling only ~10 MeV/$c^2$. The remaining 99% of the proton's mass comes from the kinetic and binding energy of the quarks and gluons, all captured in the invariant mass of the system.

**Threshold calculations.** For particle production $a + b \to c_1 + c_2 + \cdots + c_n$ with particle $b$ at rest:

$$
P^\mu_{\text{total}} = p_a^\mu + p_b^\mu = (E_a/c + m_b c,\; \mathbf{p}_a)
$$

$$
-P_\mu P^\mu = (E_a + m_b c^2)^2/c^2 - |\mathbf{p}_a|^2 = 2E_a m_b + (m_a^2 + m_b^2)c^2
$$

At threshold, all products are at rest in the CM frame: $-P_\mu P^\mu = M_f^2 c^2$ where $M_f = \sum_i m_{c_i}$. This gives the threshold energy formula used in collider physics.

**References:** Carroll §1.4; Landau & Lifshitz, *Classical Theory of Fields* §9–10; MTW §5.

