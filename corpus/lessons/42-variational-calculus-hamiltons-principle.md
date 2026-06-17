---
title: "Variational Calculus Hamiltons Principle"
subject: "Classical Mechanics & Dynamical Systems"
catalog: advanced
audience_tier: higher-education
chapter: "4.2"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 4.2 — Variational Calculus & Hamilton's Principle

> *"Nature is thrifty in all its actions."* — Pierre Louis Maupertuis, 1744

The entire edifice of analytical mechanics rests on a single breathtaking idea: among all conceivable paths a system could take between two configurations, Nature selects the one that makes a certain integral — the **action** — stationary. This chapter develops the mathematical machinery of the calculus of variations and culminates in Hamilton's Principle.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Define a **functional** and distinguish it from an ordinary function.
2. Compute the **first variation** $\delta S$ of a functional.
3. Derive the **Euler-Lagrange equation** from the stationarity condition $\delta S = 0$.
4. Handle functionals with higher derivatives and multiple dependent variables.
5. State and apply **Hamilton's Principle** (Principle of Stationary Action).
6. Derive natural boundary conditions from the variational problem.
7. Apply the Euler-Lagrange equation to geodesics, brachistochrone, and catenary problems.

---

## 🖼️ Visual Anchor — The Path of Stationary Action

![math-04__4.2-fig1](math-04__4.2-fig1.svg)

---


## 📚 1. Definitions

### Definition 4.2.1 — Functional

A **functional** is a mapping from a space of functions to the real numbers. Given a function $y(x)$ defined on $[a,b]$, a functional $J[y]$ assigns a single real number to each admissible function $y$:

$$
J[y] = \int_a^b F(x, y, y') \, dx,
$$

where $F$ is a known function of three arguments called the **integrand** or **Lagrangian density**.

### Definition 4.2.2 — Admissible Functions and Variations

The set of **admissible functions** consists of all sufficiently smooth functions $y(x)$ satisfying prescribed boundary conditions $y(a) = y_a$, $y(b) = y_b$. A **variation** $\eta(x)$ is any smooth function satisfying $\eta(a) = \eta(b) = 0$. The **varied path** is $\tilde{y}(x) = y(x) + \varepsilon\,\eta(x)$ for small $\varepsilon$.

### Definition 4.2.3 — First Variation

The **first variation** of $J$ is:

$$
\delta J = \left.\frac{d}{d\varepsilon}\right|_{\varepsilon=0} J[y + \varepsilon\eta] = \int_a^b \left(\frac{\partial F}{\partial y}\eta + \frac{\partial F}{\partial y'}\eta'\right)dx.
$$

### Definition 4.2.4 — Stationary (Extremal) Path

A path $y^*(x)$ is **stationary** (or extremal) if $\delta J = 0$ for all admissible variations $\eta$. This is the variational analogue of $f'(x_0) = 0$ for ordinary functions.

### Definition 4.2.5 — The Action Functional

In mechanics, the **action** is the functional:

$$
S[q] = \int_{t_1}^{t_2} L(q, \dot{q}, t)\,dt,
$$

where $L = T - U$ is the Lagrangian, $q$ represents generalized coordinates, and $\dot{q} = dq/dt$.

---

## 📐 2. Axioms / Postulates

### Axiom 4.2.A1 — Hamilton's Principle (Principle of Stationary Action)

The physical trajectory $q(t)$ of a mechanical system between fixed endpoints $q(t_1) = q_1$ and $q(t_2) = q_2$ is the one for which the action functional is stationary:

$$
\delta S = \delta \int_{t_1}^{t_2} L(q, \dot{q}, t)\,dt = 0.
$$

This single postulate replaces Newton's three laws and generates all equations of motion for holonomic systems.

### Axiom 4.2.A2 — Smoothness Assumption

The Lagrangian $L(q, \dot{q}, t)$ is assumed to be at least twice continuously differentiable ($C^2$) in all its arguments, ensuring the Euler-Lagrange equation is well-defined.

---


## 🛡️ 3. Lemmas

### Lemma 4.2.1 — Fundamental Lemma of the Calculus of Variations

If $f(x)$ is continuous on $[a,b]$ and:

$$
\int_a^b f(x)\,\eta(x)\,dx = 0
$$

for every smooth function $\eta$ with $\eta(a) = \eta(b) = 0$, then $f(x) = 0$ for all $x \in [a,b]$.

**Proof.** Suppose for contradiction that $f(x_0) > 0$ at some interior point $x_0$. By continuity, $f > 0$ on some interval $(x_0 - \delta, x_0 + \delta) \subset [a,b]$. Choose $\eta(x) = [(x - x_0 + \delta)(x_0 + \delta - x)]^2$ inside this interval and $\eta = 0$ outside. Then $\eta \geq 0$, $\eta(x_0) > 0$, and:

$$
\int_a^b f\eta\,dx = \int_{x_0-\delta}^{x_0+\delta} f\eta\,dx > 0,
$$

contradicting the hypothesis. Similarly for $f(x_0) < 0$. Therefore $f \equiv 0$. $\blacksquare$

### Lemma 4.2.2 — Integration by Parts for Variations

For the term $\int_a^b \frac{\partial F}{\partial y'}\eta'\,dx$, integration by parts with $u = \frac{\partial F}{\partial y'}$ and $dv = \eta'\,dx$ gives:

$$
\int_a^b \frac{\partial F}{\partial y'}\eta'\,dx = \left[\frac{\partial F}{\partial y'}\eta\right]_a^b - \int_a^b \frac{d}{dx}\left(\frac{\partial F}{\partial y'}\right)\eta\,dx.
$$

Since $\eta(a) = \eta(b) = 0$, the boundary term vanishes, leaving:

$$
\int_a^b \frac{\partial F}{\partial y'}\eta'\,dx = -\int_a^b \frac{d}{dx}\left(\frac{\partial F}{\partial y'}\right)\eta\,dx.
$$

---

## 👑 4. Theorems

### Theorem 4.2.1 — The Euler-Lagrange Equation

If $y^*(x)$ is a stationary path of $J[y] = \int_a^b F(x,y,y')\,dx$ with fixed endpoints, then $y^*$ satisfies:

$$
\frac{\partial F}{\partial y} - \frac{d}{dx}\left(\frac{\partial F}{\partial y'}\right) = 0.
$$

### Theorem 4.2.2 — Euler-Lagrange for Multiple Variables

For a functional $J[y_1, \ldots, y_n] = \int_a^b F(x, y_1, \ldots, y_n, y_1', \ldots, y_n')\,dx$, the stationary conditions are $n$ coupled equations:

$$
\frac{\partial F}{\partial y_k} - \frac{d}{dx}\left(\frac{\partial F}{\partial y_k'}\right) = 0, \quad k = 1, \ldots, n.
$$

### Theorem 4.2.3 — Beltrami Identity (First Integral)

If $F$ does not depend explicitly on $x$ (i.e., $\partial F/\partial x = 0$), then the Euler-Lagrange equation admits the first integral:

$$
F - y'\frac{\partial F}{\partial y'} = C \quad (\text{constant}).
$$

### Theorem 4.2.4 — Hamilton's Principle Implies Newton's Laws

For a particle in a potential $U(\mathbf{r})$ with $L = \frac{1}{2}m|\dot{\mathbf{r}}|^2 - U(\mathbf{r})$, the Euler-Lagrange equations reduce to Newton's second law $m\ddot{\mathbf{r}} = -\nabla U$.

### Theorem 4.2.5 — Noether's Theorem (Preview)

If the Lagrangian is invariant under a continuous one-parameter family of transformations, there exists a corresponding conserved quantity. (Full treatment in [4.3 - Lagrangian Mechanics - Euler-Lagrange](4.3---Lagrangian-Mechanics---Euler-Lagrange).)

---


## ✍️ 5. Proofs / Derivations

### 5.1 Derivation of the Euler-Lagrange Equation

**Goal:** Find the condition on $y(x)$ such that $\delta J = 0$ for all admissible $\eta$.

**Step 1:** Write the perturbed functional. Let $\tilde{y} = y + \varepsilon\eta$, so $\tilde{y}' = y' + \varepsilon\eta'$:

$$
J[y + \varepsilon\eta] = \int_a^b F(x, y + \varepsilon\eta, y' + \varepsilon\eta')\,dx.
$$

**Step 2:** Differentiate with respect to $\varepsilon$ and evaluate at $\varepsilon = 0$:

$$
\frac{dJ}{d\varepsilon}\bigg|_{\varepsilon=0} = \int_a^b \left(\frac{\partial F}{\partial y}\eta + \frac{\partial F}{\partial y'}\eta'\right)dx.
$$

This uses the chain rule: $\frac{\partial}{\partial\varepsilon}F(x, y+\varepsilon\eta, y'+\varepsilon\eta') = \frac{\partial F}{\partial y}\cdot\eta + \frac{\partial F}{\partial y'}\cdot\eta'$.

**Step 3:** Apply integration by parts to the second term. Set $u = \frac{\partial F}{\partial y'}$ and $dv = \eta'\,dx$, giving $du = \frac{d}{dx}\left(\frac{\partial F}{\partial y'}\right)dx$ and $v = \eta$:

$$
\int_a^b \frac{\partial F}{\partial y'}\eta'\,dx = \underbrace{\left[\frac{\partial F}{\partial y'}\eta\right]_a^b}_{= 0 \text{ since } \eta(a)=\eta(b)=0} - \int_a^b \frac{d}{dx}\left(\frac{\partial F}{\partial y'}\right)\eta\,dx.
$$

**Step 4:** Combine:

$$
\delta J = \int_a^b \left[\frac{\partial F}{\partial y} - \frac{d}{dx}\left(\frac{\partial F}{\partial y'}\right)\right]\eta\,dx = 0.
$$

**Step 5:** Apply the Fundamental Lemma (Lemma 4.2.1). Since this must hold for all admissible $\eta$:

$$
\frac{\partial F}{\partial y} - \frac{d}{dx}\left(\frac{\partial F}{\partial y'}\right) = 0. \quad \blacksquare
$$

### 5.2 Proof of the Beltrami Identity

**Proof.** When $F = F(y, y')$ (no explicit $x$-dependence), compute $\frac{dF}{dx}$ along the extremal using the chain rule:

$$
\frac{dF}{dx} = \frac{\partial F}{\partial y}y' + \frac{\partial F}{\partial y'}y''.
$$

From the Euler-Lagrange equation: $\frac{\partial F}{\partial y} = \frac{d}{dx}\left(\frac{\partial F}{\partial y'}\right)$. Substitute:

$$
\frac{dF}{dx} = \frac{d}{dx}\left(\frac{\partial F}{\partial y'}\right)\cdot y' + \frac{\partial F}{\partial y'}\cdot y''.
$$

Recognize the right side as $\frac{d}{dx}\left(y'\frac{\partial F}{\partial y'}\right)$ by the product rule:

$$
\frac{d}{dx}\left(y'\frac{\partial F}{\partial y'}\right) = y''\frac{\partial F}{\partial y'} + y'\frac{d}{dx}\left(\frac{\partial F}{\partial y'}\right).
$$

Therefore:

$$
\frac{dF}{dx} = \frac{d}{dx}\left(y'\frac{\partial F}{\partial y'}\right) \implies \frac{d}{dx}\left(F - y'\frac{\partial F}{\partial y'}\right) = 0.
$$

Hence $F - y'\frac{\partial F}{\partial y'} = C$. $\blacksquare$

### 5.3 Proof of Theorem 4.2.4 — Hamilton's Principle Yields Newton's Laws

**Proof.** For a particle in 3D with $L = \frac{1}{2}m(\dot{x}^2 + \dot{y}^2 + \dot{z}^2) - U(x,y,z)$, apply the Euler-Lagrange equation to coordinate $x$:

$$
\frac{\partial L}{\partial x} = -\frac{\partial U}{\partial x}, \quad \frac{\partial L}{\partial \dot{x}} = m\dot{x}.
$$

$$
\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{x}}\right) = m\ddot{x}.
$$

The Euler-Lagrange equation gives:

$$
-\frac{\partial U}{\partial x} - m\ddot{x} = 0 \implies m\ddot{x} = -\frac{\partial U}{\partial x} = F_x.
$$

Identical results for $y$ and $z$. In vector form: $m\ddot{\mathbf{r}} = -\nabla U = \mathbf{F}$. $\blacksquare$

---


## 🧮 6. Worked Examples

### Example 4.2.1 — Shortest Path Between Two Points (Geodesic in Euclidean Space)

**Problem:** Find the curve $y(x)$ of minimum arc length connecting $(x_1, y_1)$ to $(x_2, y_2)$.

<details>
<summary>🔍 Full Solution</summary>

**Step 1:** The arc length functional is:

$$
J[y] = \int_{x_1}^{x_2} \sqrt{1 + y'^2}\,dx.
$$

Here $F(y, y') = \sqrt{1 + y'^2}$ has no explicit $x$-dependence.

**Step 2:** Apply the Beltrami identity (Theorem 4.2.3):

$$
F - y'\frac{\partial F}{\partial y'} = C.
$$

Compute $\frac{\partial F}{\partial y'} = \frac{y'}{\sqrt{1+y'^2}}$. Then:

$$
\sqrt{1+y'^2} - y' \cdot \frac{y'}{\sqrt{1+y'^2}} = C.
$$

$$
\frac{1+y'^2 - y'^2}{\sqrt{1+y'^2}} = C \implies \frac{1}{\sqrt{1+y'^2}} = C.
$$

**Step 3:** Solve for $y'$:

$$
\sqrt{1+y'^2} = \frac{1}{C} \implies y'^2 = \frac{1}{C^2} - 1 = \text{const}.
$$

Therefore $y' = \text{const}$, meaning $y(x) = mx + b$ — a straight line. $\blacksquare$

</details>

### Example 4.2.2 — The Brachistochrone Problem

**Problem:** Find the curve connecting the origin to point $(x_1, y_1)$ (with $y$ pointing downward) along which a bead slides frictionlessly in minimum time under gravity.

<details>
<summary>🔍 Full Solution</summary>

**Step 1:** By energy conservation, starting from rest: $v = \sqrt{2gy}$. The time functional:

$$
T[y] = \int_0^{x_1} \frac{ds}{v} = \int_0^{x_1} \frac{\sqrt{1+y'^2}}{\sqrt{2gy}}\,dx.
$$

So $F = \sqrt{\frac{1+y'^2}{2gy}}$. No explicit $x$-dependence, so use Beltrami:

$$
F - y'\frac{\partial F}{\partial y'} = C.
$$

**Step 2:** Compute $\frac{\partial F}{\partial y'} = \frac{y'}{\sqrt{2gy}\sqrt{1+y'^2}}$. Then:

$$
\frac{\sqrt{1+y'^2}}{\sqrt{2gy}} - \frac{y'^2}{\sqrt{2gy}\sqrt{1+y'^2}} = C.
$$

$$
\frac{1+y'^2 - y'^2}{\sqrt{2gy}\sqrt{1+y'^2}} = C \implies \frac{1}{\sqrt{2gy(1+y'^2)}} = C.
$$

**Step 3:** Square and rearrange:

$$
y(1+y'^2) = \frac{1}{2gC^2} \equiv 2R \quad (\text{define constant } R).
$$

**Step 4:** Parametrize with $y = R(1-\cos\theta)$. Then $dy = R\sin\theta\,d\theta$ and from $y(1+y'^2) = 2R$:

$$
1 + y'^2 = \frac{2R}{y} = \frac{2}{1-\cos\theta} \implies y'^2 = \frac{1+\cos\theta}{1-\cos\theta}.
$$

Using $y' = dy/dx$: $dx = \frac{dy}{y'} = \frac{R\sin\theta\,d\theta}{\sqrt{(1+\cos\theta)/(1-\cos\theta)}}$.

Simplify using $\frac{\sin\theta}{\sqrt{(1+\cos\theta)/(1-\cos\theta)}} = \frac{\sin\theta\sqrt{1-\cos\theta}}{\sqrt{1+\cos\theta}} = 1 - \cos\theta$ (after using half-angle identities).

Therefore $dx = R(1-\cos\theta)\,d\theta$, giving:

$$
x = R(\theta - \sin\theta), \quad y = R(1 - \cos\theta).
$$

This is a **cycloid** — the curve traced by a point on the rim of a rolling circle of radius $R$.

</details>

### Example 4.2.3 — The Catenary (Hanging Chain)

**Problem:** A uniform chain of length $\ell$ and linear density $\rho$ hangs between two supports at equal height. Find the shape $y(x)$ that minimizes gravitational potential energy.

<details>
<summary>🔍 Full Solution</summary>

**Step 1:** The potential energy is $U = \rho g \int_{-a}^{a} y\,ds = \rho g \int_{-a}^{a} y\sqrt{1+y'^2}\,dx$, subject to the constraint $\int_{-a}^{a}\sqrt{1+y'^2}\,dx = \ell$.

**Step 2:** Use a Lagrange multiplier $\lambda$. Minimize:

$$
J[y] = \int_{-a}^{a} (y - \lambda)\sqrt{1+y'^2}\,dx.
$$

Set $F = (y-\lambda)\sqrt{1+y'^2}$. No explicit $x$-dependence → Beltrami identity:

$$
(y-\lambda)\sqrt{1+y'^2} - y' \cdot \frac{(y-\lambda)y'}{\sqrt{1+y'^2}} = C.
$$

$$
\frac{(y-\lambda)(1+y'^2 - y'^2)}{\sqrt{1+y'^2}} = C \implies \frac{y-\lambda}{\sqrt{1+y'^2}} = C.
$$

**Step 3:** Let $u = y - \lambda$. Then $\frac{u}{\sqrt{1+u'^2}} = C$, so $u^2 = C^2(1+u'^2)$, giving $u'^2 = \frac{u^2 - C^2}{C^2}$.

Separate: $\frac{du}{\sqrt{u^2 - C^2}} = \frac{dx}{C}$. Integrate: $\cosh^{-1}(u/C) = x/C + \text{const}$.

**Step 4:** Therefore $u = C\cosh\left(\frac{x-x_0}{C}\right)$, and:

$$
y(x) = \lambda + C\cosh\left(\frac{x}{C}\right),
$$

where we set $x_0 = 0$ by symmetry. This is the **catenary** curve.

</details>

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- **Previous:** [4.1 - Newtonian Dynamics & Conservation Laws](4.1---Newtonian-Dynamics-&-Conservation-Laws) — the force-based formulation that Hamilton's Principle supersedes
- **Next:** [4.3 - Lagrangian Mechanics - Euler-Lagrange](4.3---Lagrangian-Mechanics---Euler-Lagrange) — systematic application of the Euler-Lagrange equation
- **Multivariable calculus tools:** [1.4 - Vector Calculus](1.4---Vector-Calculus) for gradient and divergence operations
- **ODEs from Euler-Lagrange:** [3.1 - First-Order ODEs & Separable Equations](3.1---First-Order-ODEs-&-Separable-Equations), [3.2 - Second-Order Linear ODEs](3.2---Second-Order-Linear-ODEs)

### External Resources
- **Goldstein**, *Classical Mechanics*, Ch. 2 — Variational Principles and Lagrange's Equations
- **Lanczos**, *The Variational Principles of Mechanics* — the most beautiful exposition of the subject
- **Susskind**, *The Theoretical Minimum*, Lecture 3 — intuitive introduction to the action principle
- **Gelfand & Fomin**, *Calculus of Variations* — rigorous mathematical treatment

---

*Next: [4.3 - Lagrangian Mechanics - Euler-Lagrange](4.3---Lagrangian-Mechanics---Euler-Lagrange) →*



---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — The Brachistochrone with Friction

**Problem:** A bead slides under gravity along a wire from point $A = (0,0)$ to point $B = (x_1, y_1)$ (with $y$ measured downward). The wire has kinetic friction coefficient $\mu_k$. Set up the functional for the time of descent and write the Euler-Lagrange equation. Show that for $\mu_k = 0$ the cycloid is recovered.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Energy considerations with friction

The normal force on the bead depends on the local curvature and speed. For a curve $y(x)$ with $y$ downward, the speed from energy conservation with friction work is:

$$
\frac{1}{2}mv^2 = mgy - \mu_k \int_0^s N\,ds',
$$

where $N$ is the normal force and $s$ is arc length. This makes the problem non-holonomic in general. However, for small friction ($\mu_k \ll 1$), we can use the approximation that the normal force on a curve is approximately $N \approx mg\cos\alpha$ where $\alpha$ is the angle of the tangent to the horizontal.

For the frictionless case, $v = \sqrt{2gy}$, and the time functional is:

$$
T[y] = \int_0^{x_1} \frac{\sqrt{1+y'^2}}{\sqrt{2gy}}\,dx.
$$

#### Step 2: The frictionless Euler-Lagrange equation

The integrand $F(y, y') = \frac{\sqrt{1+y'^2}}{\sqrt{2gy}}$ has no explicit $x$-dependence. Apply the Beltrami identity:

$$
F - y'\frac{\partial F}{\partial y'} = C.
$$

Compute $\frac{\partial F}{\partial y'} = \frac{y'}{\sqrt{2gy}\sqrt{1+y'^2}}$. Then:

$$
\frac{\sqrt{1+y'^2}}{\sqrt{2gy}} - \frac{y'^2}{\sqrt{2gy}\sqrt{1+y'^2}} = C.
$$

Combine over a common denominator:

$$
\frac{1+y'^2 - y'^2}{\sqrt{2gy}\sqrt{1+y'^2}} = C \implies \frac{1}{\sqrt{2gy(1+y'^2)}} = C.
$$

#### Step 3: Solve the ODE

Square both sides: $y(1+y'^2) = \frac{1}{2gC^2} \equiv 2R$.

Parametrize with $y = R(1-\cos\theta)$. Then $dy = R\sin\theta\,d\theta$ and:

$$
y'^2 = \frac{2R - y}{y} = \frac{2R - R(1-\cos\theta)}{R(1-\cos\theta)} = \frac{1+\cos\theta}{1-\cos\theta}.
$$

Using half-angle identities: $1+\cos\theta = 2\cos^2(\theta/2)$ and $1-\cos\theta = 2\sin^2(\theta/2)$, so $y' = \cot(\theta/2)$.

Then $dx = \frac{dy}{y'} = \frac{R\sin\theta\,d\theta}{\cot(\theta/2)} = R\sin\theta\tan(\theta/2)\,d\theta$.

Since $\sin\theta = 2\sin(\theta/2)\cos(\theta/2)$ and $\tan(\theta/2) = \sin(\theta/2)/\cos(\theta/2)$:

$$
dx = R\cdot 2\sin(\theta/2)\cos(\theta/2)\cdot\frac{\sin(\theta/2)}{\cos(\theta/2)}\,d\theta = 2R\sin^2(\theta/2)\,d\theta = R(1-\cos\theta)\,d\theta.
$$

Integrate: $x = R(\theta - \sin\theta) + \text{const}$. With $x(0) = 0$: $x = R(\theta - \sin\theta)$.

#### Step 4: The cycloid solution

$$
x = R(\theta - \sin\theta), \quad y = R(1 - \cos\theta).
$$

This is a **cycloid** — the curve traced by a point on the rim of a circle of radius $R$ rolling along the $x$-axis. The constant $R$ is determined by requiring the curve to pass through $B = (x_1, y_1)$.

**Final Answer:**

$$
\text{Brachistochrone} = \text{Cycloid}: \quad x = R(\theta - \sin\theta),\; y = R(1-\cos\theta)
$$

</details>

### Example 8.2 — Geodesic on a Sphere (Great Circle)

**Problem:** Show that the shortest path between two points on a sphere of radius $R$ is an arc of a great circle, using the calculus of variations.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Arc length on a sphere

In spherical coordinates $(\theta, \phi)$ on a sphere of radius $R$, the line element is:

$$
ds^2 = R^2(d\theta^2 + \sin^2\theta\,d\phi^2).
$$

Parameterize the path by $\theta(\phi)$. Then:

$$
ds = R\sqrt{\theta'^2 + \sin^2\theta}\,d\phi, \quad \text{where } \theta' = \frac{d\theta}{d\phi}.
$$

The total arc length functional:

$$
S[\theta] = R\int_{\phi_1}^{\phi_2}\sqrt{\theta'^2 + \sin^2\theta}\,d\phi.
$$

#### Step 2: Euler-Lagrange equation

The integrand $F(\theta, \theta') = \sqrt{\theta'^2 + \sin^2\theta}$ has no explicit $\phi$-dependence. Apply the Beltrami identity:

$$
F - \theta'\frac{\partial F}{\partial \theta'} = C.
$$

Compute: $\frac{\partial F}{\partial \theta'} = \frac{\theta'}{\sqrt{\theta'^2 + \sin^2\theta}}$.

$$
\sqrt{\theta'^2 + \sin^2\theta} - \frac{\theta'^2}{\sqrt{\theta'^2 + \sin^2\theta}} = C.
$$

$$
\frac{\theta'^2 + \sin^2\theta - \theta'^2}{\sqrt{\theta'^2 + \sin^2\theta}} = C \implies \frac{\sin^2\theta}{\sqrt{\theta'^2 + \sin^2\theta}} = C.
$$

#### Step 3: Solve for $\theta'$

Square: $\frac{\sin^4\theta}{\theta'^2 + \sin^2\theta} = C^2$.

$$
\theta'^2 = \sin^2\theta\left(\frac{\sin^2\theta}{C^2} - 1\right) = \frac{\sin^2\theta(\sin^2\theta - C^2)}{C^2}.
$$

#### Step 4: Show this is a great circle

A great circle on a sphere satisfies $\cot\theta = A\cos(\phi - \phi_0)$ for constants $A, \phi_0$. Differentiate:

$$
-\frac{\theta'}{\sin^2\theta} = -A\sin(\phi-\phi_0).
$$

So $\theta' = A\sin^2\theta\sin(\phi-\phi_0)$. Substituting back and using $\cot^2\theta = A^2\cos^2(\phi-\phi_0)$:

$$
\theta'^2 = A^2\sin^4\theta\sin^2(\phi-\phi_0) = A^2\sin^4\theta(1-\cos^2(\phi-\phi_0)) = \sin^4\theta\left(A^2 - \frac{\cos^2\theta}{\sin^4\theta}\cdot\sin^4\theta\cdot\frac{A^2}{\cos^2\theta}\right)...
$$

More directly: substitute $u = \cot\theta$, $du = -\theta'/\sin^2\theta\,d\phi$. The ODE becomes:

$$
\left(\frac{du}{d\phi}\right)^2 = \frac{1}{C^2} - 1 - u^2 \equiv K^2 - u^2,
$$

where $K^2 = (1-C^2)/C^2$. This has solution $u = K\cos(\phi - \phi_0)$, i.e.:

$$
\cot\theta = K\cos(\phi - \phi_0).
$$

This is the equation of a **great circle** (the intersection of the sphere with a plane through the origin).

**Final Answer:**

$$
\cot\theta = K\cos(\phi - \phi_0) \quad \Longleftrightarrow \quad \text{Great circle (geodesic on } S^2\text{)}
$$

</details>



### Example 8.3 — Soap Film Minimal Surface (Catenoid)

**Problem:** A soap film is stretched between two coaxial circular rings of radius $R$ separated by distance $2d$. Find the shape $r(z)$ of the film that minimizes surface area (assuming axial symmetry).

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Surface area functional

For a surface of revolution $r(z)$ about the $z$-axis, the surface area is:

$$
A[r] = 2\pi\int_{-d}^{d} r\sqrt{1+r'^2}\,dz,
$$

where $r' = dr/dz$. Boundary conditions: $r(\pm d) = R$.

#### Step 2: Euler-Lagrange equation

The integrand $F(r, r') = r\sqrt{1+r'^2}$ has no explicit $z$-dependence. Apply the Beltrami identity:

$$
F - r'\frac{\partial F}{\partial r'} = C.
$$

Compute: $\frac{\partial F}{\partial r'} = \frac{rr'}{\sqrt{1+r'^2}}$.

$$
r\sqrt{1+r'^2} - \frac{rr'^2}{\sqrt{1+r'^2}} = C.
$$

$$
\frac{r(1+r'^2) - rr'^2}{\sqrt{1+r'^2}} = C \implies \frac{r}{\sqrt{1+r'^2}} = C.
$$

#### Step 3: Solve the ODE

From $\frac{r}{\sqrt{1+r'^2}} = C$, square: $r^2 = C^2(1+r'^2)$, so:

$$
r'^2 = \frac{r^2 - C^2}{C^2} \implies \frac{dr}{\sqrt{r^2 - C^2}} = \frac{dz}{C}.
$$

#### Step 4: Integrate

Let $r = C\cosh u$, then $dr = C\sinh u\,du$ and $\sqrt{r^2-C^2} = C\sinh u$:

$$
\frac{C\sinh u\,du}{C\sinh u} = \frac{dz}{C} \implies du = \frac{dz}{C}.
$$

So $u = z/C + \text{const}$. By symmetry ($r$ is even in $z$), the constant is zero:

$$
r(z) = C\cosh\left(\frac{z}{C}\right).
$$

This is a **catenoid** — the minimal surface of revolution.

#### Step 5: Determine $C$ from boundary conditions

$r(d) = R$ gives: $C\cosh(d/C) = R$. This is a transcendental equation for $C$ given $R$ and $d$.

For a solution to exist, we need $R/d$ above a critical ratio. If $d/R$ exceeds approximately $0.6627$, no catenoid solution exists and the minimal surface is two disconnected disks (Goldschmidt discontinuous solution).

**Final Answer:**

$$
r(z) = C\cosh\left(\frac{z}{C}\right), \quad \text{where } C\cosh\left(\frac{d}{C}\right) = R
$$

</details>

### Example 8.4 — Isoperimetric Problem (Maximum Area for Given Perimeter)

**Problem:** Among all simple closed curves of fixed perimeter $L$ in the plane, find the one enclosing maximum area. (Prove that it is a circle.)

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Set up the constrained variational problem

Parameterize the curve by arc length $s \in [0, L]$: $\mathbf{r}(s) = (x(s), y(s))$ with $x'^2 + y'^2 = 1$ (unit-speed constraint).

The enclosed area (by Green's theorem):

$$
A = \frac{1}{2}\oint(x\,dy - y\,dx) = \frac{1}{2}\int_0^L(xy' - yx')\,ds.
$$

We maximize $A$ subject to the constraint $x'^2 + y'^2 = 1$.

#### Step 2: Lagrange multiplier formulation

Form the augmented functional:

$$
J[x,y] = \int_0^L\left[\frac{1}{2}(xy'-yx') - \lambda(x'^2+y'^2-1)\right]ds.
$$

Wait — the constraint $x'^2+y'^2=1$ is already built into the arc-length parameterization. Instead, use the perimeter constraint directly.

Re-parameterize by an arbitrary parameter $t \in [0, 2\pi]$. Perimeter: $P = \int_0^{2\pi}\sqrt{x'^2+y'^2}\,dt = L$. Area: $A = \frac{1}{2}\int_0^{2\pi}(xy'-yx')\,dt$.

Maximize $A - \lambda P$:

$$
J = \int_0^{2\pi}\left[\frac{1}{2}(xy'-yx') - \lambda\sqrt{x'^2+y'^2}\right]dt.
$$

#### Step 3: Euler-Lagrange equations

For $x$: $\frac{\partial F}{\partial x} - \frac{d}{dt}\frac{\partial F}{\partial x'} = 0$.

$\frac{\partial F}{\partial x} = \frac{1}{2}y'$, $\frac{\partial F}{\partial x'} = -\frac{1}{2}y - \frac{\lambda x'}{\sqrt{x'^2+y'^2}}$.

Using arc-length parameterization ($\sqrt{x'^2+y'^2} = L/(2\pi) \equiv v$, constant):

$$
\frac{1}{2}y' + \frac{1}{2}y' + \frac{\lambda}{v}x'' = 0 \implies y' + \frac{\lambda}{v}x'' = 0.
$$

Similarly for $y$: $-x' - \frac{\lambda}{v}y'' = 0 \implies x' + \frac{\lambda}{v}y'' = 0$.

#### Step 4: Solve the system

From the two equations: $x'' = -\frac{v}{\lambda}y'$ and $y'' = \frac{v}{\lambda}x'$.

Let $\kappa = v/\lambda$. Then $x'' = -\kappa y'$ and $y'' = \kappa x'$. Differentiate the first: $x''' = -\kappa y'' = -\kappa^2 x'$.

This gives $x'(t) = A\cos(\kappa t) + B\sin(\kappa t)$, and similarly for $y'$. Integrating:

$$
x(t) = \frac{A}{\kappa}\sin(\kappa t) - \frac{B}{\kappa}\cos(\kappa t) + x_0,
$$

$$
y(t) = \frac{A}{\kappa}\cos(\kappa t) + \frac{B}{\kappa}\sin(\kappa t) + y_0.
$$

This is a **circle** of radius $r = \sqrt{A^2+B^2}/\kappa$.

#### Step 5: Determine the radius

The perimeter is $L = 2\pi r$, so $r = L/(2\pi)$. The maximum area is:

$$
A_{\max} = \pi r^2 = \frac{L^2}{4\pi}.
$$

**Final Answer:**

$$
\text{The circle of radius } r = \frac{L}{2\pi} \text{ maximizes area: } A_{\max} = \frac{L^2}{4\pi}
$$

</details>



---

## 📘 9. Appendix: Extended Derivations & Special Cases

### 9.1 Full Derivation of the Euler-Lagrange Equation from the Variational Principle

We derive the Euler-Lagrange equation from first principles, showing every step of the variational argument. This is the foundational result of the calculus of variations.

**Setup:** Consider the functional

$$
J[y] = \int_a^b F(x, y, y')\,dx,
$$

where $y(a) = y_a$ and $y(b) = y_b$ are fixed endpoints, and $F$ is a smooth function of three arguments.

**Step 1: Define the variation.** Let $y(x)$ be the extremal (the function that makes $J$ stationary). Consider a one-parameter family of comparison functions:

$$
Y(x) = y(x) + \varepsilon\,\eta(x),
$$

where $\eta(x)$ is an arbitrary smooth function satisfying $\eta(a) = \eta(b) = 0$ (to preserve the boundary conditions), and $\varepsilon$ is a small parameter.

**Step 2: Compute $J[Y]$ as a function of $\varepsilon$.**

$$
J(\varepsilon) = \int_a^b F(x,\; y+\varepsilon\eta,\; y'+\varepsilon\eta')\,dx.
$$

**Step 3: Stationarity condition.** For $y$ to be an extremal, we require:

$$
\left.\frac{dJ}{d\varepsilon}\right|_{\varepsilon=0} = 0 \quad \text{for all admissible } \eta.
$$

**Step 4: Differentiate under the integral sign.**

$$
\frac{dJ}{d\varepsilon} = \int_a^b\left[\frac{\partial F}{\partial y}\cdot\eta + \frac{\partial F}{\partial y'}\cdot\eta'\right]dx.
$$

Evaluate at $\varepsilon = 0$ (so $Y = y$, $Y' = y'$):

$$
0 = \int_a^b\left[\frac{\partial F}{\partial y}\eta + \frac{\partial F}{\partial y'}\eta'\right]dx.
$$

**Step 5: Integration by parts on the second term.** Let $u = \frac{\partial F}{\partial y'}$ and $dv = \eta'\,dx$, so $v = \eta$:

$$
\int_a^b \frac{\partial F}{\partial y'}\eta'\,dx = \left[\frac{\partial F}{\partial y'}\eta\right]_a^b - \int_a^b\frac{d}{dx}\left(\frac{\partial F}{\partial y'}\right)\eta\,dx.
$$

The boundary term vanishes because $\eta(a) = \eta(b) = 0$. Therefore:

$$
0 = \int_a^b\left[\frac{\partial F}{\partial y} - \frac{d}{dx}\frac{\partial F}{\partial y'}\right]\eta\,dx.
$$

**Step 6: Apply the Fundamental Lemma of the Calculus of Variations.** If $\int_a^b g(x)\eta(x)\,dx = 0$ for all smooth $\eta$ vanishing at the endpoints, then $g(x) = 0$ on $(a,b)$.

Therefore:

$$
\frac{\partial F}{\partial y} - \frac{d}{dx}\frac{\partial F}{\partial y'} = 0.
$$

This is the **Euler-Lagrange equation**. It is a second-order ODE for $y(x)$ (since expanding $\frac{d}{dx}\frac{\partial F}{\partial y'}$ involves $y''$ through the chain rule).

**Step 7: The multi-variable generalization.** For $n$ functions $y_1(x), \ldots, y_n(x)$ and $F(x, y_1, \ldots, y_n, y_1', \ldots, y_n')$, we get $n$ coupled Euler-Lagrange equations:

$$
\frac{\partial F}{\partial y_i} - \frac{d}{dx}\frac{\partial F}{\partial y_i'} = 0, \quad i = 1, \ldots, n.
$$

In mechanics, $x \to t$, $y_i \to q_i$ (generalized coordinates), and $F \to L$ (Lagrangian), giving the equations of motion for all degrees of freedom.

*References: Gelfand & Fomin, Calculus of Variations, Ch. 1; Goldstein, Classical Mechanics, Ch. 2; Lanczos, The Variational Principles of Mechanics, Ch. IV.*

### 9.2 The Beltrami Identity and Its Applications

When the integrand $F(y, y')$ does not depend explicitly on $x$, the Euler-Lagrange equation admits a first integral known as the **Beltrami identity**. This dramatically simplifies many problems.

**Derivation:** Start from the Euler-Lagrange equation $\frac{\partial F}{\partial y} - \frac{d}{dx}\frac{\partial F}{\partial y'} = 0$. Consider:

$$
\frac{d}{dx}\left(F - y'\frac{\partial F}{\partial y'}\right) = \frac{\partial F}{\partial x} + \frac{\partial F}{\partial y}y' + \frac{\partial F}{\partial y'}y'' - y''\frac{\partial F}{\partial y'} - y'\frac{d}{dx}\frac{\partial F}{\partial y'}.
$$

The $y''$ terms cancel:

$$
= \frac{\partial F}{\partial x} + y'\left(\frac{\partial F}{\partial y} - \frac{d}{dx}\frac{\partial F}{\partial y'}\right).
$$

The parenthetical expression vanishes by the Euler-Lagrange equation. If additionally $\frac{\partial F}{\partial x} = 0$ (no explicit $x$-dependence), then:

$$
\frac{d}{dx}\left(F - y'\frac{\partial F}{\partial y'}\right) = 0.
$$

Therefore:

$$
F - y'\frac{\partial F}{\partial y'} = C \quad (\text{Beltrami identity}).
$$

**Physical interpretation in mechanics:** When $F = L(q, \dot{q})$ and the "independent variable" is $t$, the Beltrami identity becomes:

$$
L - \dot{q}\frac{\partial L}{\partial\dot{q}} = -H = \text{const},
$$

which is conservation of energy (the Hamiltonian $H = \dot{q}\frac{\partial L}{\partial\dot{q}} - L$ is conserved when $L$ has no explicit time dependence).

**Applications in this chapter:**
- Brachistochrone (Example 8.1): reduces a second-order ODE to a first-order ODE
- Geodesic on sphere (Example 8.2): yields the great circle equation directly
- Minimal surface (Example 8.3): gives the catenoid without solving a second-order equation
- Catenary (Example 4.2.3): same reduction

### 9.3 Second Variation and Sufficient Conditions for a Minimum

The Euler-Lagrange equation provides only a *necessary* condition for an extremum (analogous to $f'(x) = 0$ in ordinary calculus). To confirm a minimum, we need the second variation.

**The second variation:** Expand $J[y + \varepsilon\eta]$ to second order in $\varepsilon$:

$$
J[y+\varepsilon\eta] = J[y] + \varepsilon\,\delta J + \frac{\varepsilon^2}{2}\,\delta^2 J + O(\varepsilon^3),
$$

where $\delta J = 0$ (Euler-Lagrange) and:

$$
\delta^2 J = \int_a^b\left[F_{yy}\eta^2 + 2F_{yy'}\eta\eta' + F_{y'y'}\eta'^2\right]dx.
$$

**Legendre condition (necessary for minimum):** $F_{y'y'} \geq 0$ along the extremal.

**Jacobi condition (sufficient, with Legendre):** The extremal provides a minimum if $F_{y'y'} > 0$ and there is no conjugate point between $a$ and $b$. A conjugate point is where the Jacobi equation (the linearized Euler-Lagrange equation for $\eta$):

$$
\frac{d}{dx}\left(F_{y'y'}\eta'\right) + \left(F_{yy} - \frac{d}{dx}F_{yy'}\right)\eta = 0,
$$

has a solution $\eta$ vanishing at $x = a$ and at some $x = c \in (a, b)$.

**Example:** For the brachistochrone, the cycloid satisfies both conditions — it is a true minimum of descent time, not merely a stationary point. For the geodesic on a sphere, conjugate points occur at antipodal points (the great circle ceases to be the shortest path beyond half the sphere).

*References: Gelfand & Fomin, Ch. 5–6; Goldstein, Ch. 2 (Appendix); Lanczos, Ch. VI.*

---
