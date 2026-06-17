---
title: "Multivariable Limits Partial Derivatives"
subject: "Mathematical Foundations & Calculus"
catalog: advanced
audience_tier: higher-education
chapter: "1.4"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 1.4 — Multivariable Limits & Partial Derivatives

> *"The calculus of several variables is the same as that of one variable, except that it is much more so."* — John L. Kelley

Every law of physics lives in more than one dimension. Temperature in a room is $T(x,y,z,t)$. The electric potential is $\phi(x,y,z)$. The wave function is $\psi(\mathbf{r},t)$. Entropy is $S(U,V,N)$. None of these are one-variable functions; every derivative that appears in Maxwell's equations, in the Schrödinger equation, in the Einstein field equations, is a **partial derivative**. This chapter builds the rigorous foundation: what does it mean for a function of several variables to have a limit, to be continuous, to be differentiable — and how do these ideas connect to the geometry of surfaces and the physics of fields?

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Evaluate limits of multivariable functions and prove non-existence via path arguments.
2. State and verify the formal $\varepsilon$–$\delta$ definition in $\mathbb{R}^n$.
3. Compute all first- and higher-order partial derivatives, including mixed partials.
4. State and apply Clairaut's theorem ($f_{xy} = f_{yx}$).
5. Distinguish between "partials exist" and "differentiable" — and give a counterexample.
6. Compute gradients, directional derivatives, and tangent planes.
7. Apply the multivariable chain rule and implicit differentiation.
8. Use the Hessian to classify critical points.

---


## 🔥 Why the Fuck Does This Matter?

Single-variable calculus studies curves. Multivariable calculus studies **everything else**. The three pillars of classical physics — mechanics, electrodynamics, thermodynamics — are all formulated as systems of partial differential equations in multiple variables:

- **Thermodynamics** is built on functions like internal energy $U(S,V,N)$ and the partial-derivative relations $({\partial U}/{\partial S})_V = T$, $({\partial U}/{\partial V})_S = -P$. The Maxwell relations of thermodynamics are just Clairaut's theorem applied to thermodynamic potentials.
- **Maxwell's equations** are $\nabla \cdot \mathbf{E} = \rho/\varepsilon_0$, $\nabla \times \mathbf{B} = \mu_0 \mathbf{J} + \mu_0\varepsilon_0 \partial_t \mathbf{E}$ — the divergence and curl are built from partial derivatives of fields $\mathbf{E}(x,y,z,t)$ and $\mathbf{B}(x,y,z,t)$.
- **General Relativity** uses the metric tensor $g_{\mu\nu}(x^\alpha)$, and the curvature is built from second-order partial derivatives of $g$.
- **Quantum mechanics**: the Schrödinger equation $i\hbar \partial_t \psi = \hat{H}\psi$ is a PDE in $\psi(x,y,z,t)$.

Master partial derivatives and limits in $\mathbb{R}^n$ here, and every physics chapter in this vault becomes accessible. Skip this and you will spend the rest of your life hitting walls of notation you cannot parse.

---

## 🖼️ Visual Anchor — 3D Surface with Level Curves

A function $z = f(x,y)$ defines a **surface** in three-dimensional space. The **level curves** (contours) are the intersections of horizontal planes $z = c$ with the surface — the topographic map of the function's landscape.

![math-01__1.4-fig1](math-01__1.4-fig1.svg)

The surface *is* the function. The level curves *are* all inputs that produce the same output. The gradient $\nabla f$ at any point points **perpendicular to the level curve** through that point and in the direction of steepest ascent on the surface.

---


## 📚 1. Definitions

### Definition 1.4.1 — Functions of Several Variables

A **function of two variables** is a rule $f : D \to \mathbb{R}$ where the **domain** $D \subseteq \mathbb{R}^2$ is a subset of the plane. For each point $(x,y) \in D$, $f$ assigns a unique real number $f(x,y)$, the **output** or **value** of $f$ at $(x,y)$. The **range** is $\{f(x,y) : (x,y) \in D\} \subseteq \mathbb{R}$. The **graph** of $f$ is the surface

$$
\{(x,y,z) \in \mathbb{R}^3 : z = f(x,y),\; (x,y) \in D\}.
$$

For functions of $n$ variables, $f : D \to \mathbb{R}$ with $D \subseteq \mathbb{R}^n$; the input is a vector $\mathbf{x} = (x_1, \ldots, x_n)$.

### Definition 1.4.2 — Level Curves and Contour Plots

For a constant $c$ in the range of $f$, the **level curve** (or **contour line**) at height $c$ is

$$
\mathcal{C}_c = \{(x,y) \in D : f(x,y) = c\}.
$$

The collection $\{\mathcal{C}_c\}$ for various values of $c$ is the **contour plot** of $f$. Densely packed contour lines indicate steep terrain (rapid change); widely spaced lines indicate gentle terrain. The level "curves" of a function of three variables are **level surfaces** (e.g., equipotential surfaces in electrostatics).

### Definition 1.4.3 — Multivariable Limit (Formal $\varepsilon$–$\delta$)

Let $f : D \to \mathbb{R}$ with $D \subseteq \mathbb{R}^2$, and let $(a,b)$ be a limit point of $D$. We say

$$
\lim_{(x,y)\to(a,b)} f(x,y) = L
$$

iff for every $\varepsilon > 0$ there exists $\delta > 0$ such that for all $(x,y) \in D$:

$$
0 < \|(x,y) - (a,b)\| < \delta \;\Longrightarrow\; |f(x,y) - L| < \varepsilon.
$$

Here $\|(x,y)-(a,b)\| = \sqrt{(x-a)^2 + (y-b)^2}$ is the Euclidean distance in the plane.

**Critical upgrade from 1D.** In one variable, there are only two directions to approach $a$: left and right. In two variables, there are **infinitely many paths** approaching $(a,b)$: straight lines at any angle, parabolas, spirals, etc. The limit exists only if **all paths yield the same value**. This makes disproving multivariable limits much easier — exhibit any two paths that disagree — and proving them harder.

### Definition 1.4.4 — Continuity at a Point

A function $f(x,y)$ is **continuous at $(a,b)$** iff:

1. $f(a,b)$ is defined.
2. $\lim_{(x,y)\to(a,b)} f(x,y)$ exists.
3. $\lim_{(x,y)\to(a,b)} f(x,y) = f(a,b)$.

$f$ is **continuous on an open set $D$** if it is continuous at every point of $D$. Polynomials in $x,y$; trigonometric functions of $x,y$; exponentials; and all their compositions are continuous on their natural domains.

### Definition 1.4.5 — Partial Derivative

Let $f(x,y)$ be defined on an open set containing $(a,b)$. The **partial derivative of $f$ with respect to $x$ at $(a,b)$** is

$$
\frac{\partial f}{\partial x}(a,b) = f_x(a,b) = \lim_{h \to 0} \frac{f(a+h, b) - f(a,b)}{h},
$$

provided this limit exists. Geometrically: slice the surface $z = f(x,y)$ with the plane $y = b$ and take the ordinary derivative of the resulting 1D curve with respect to $x$. Similarly,

$$
\frac{\partial f}{\partial y}(a,b) = f_y(a,b) = \lim_{k \to 0} \frac{f(a, b+k) - f(a,b)}{k}.
$$

**Computational rule:** to compute $\partial f / \partial x$, treat $y$ as a constant and differentiate with respect to $x$ using all single-variable rules. Likewise for $\partial f / \partial y$.

### Definition 1.4.6 — Higher-Order and Mixed Partial Derivatives

The **second partial derivatives** of $f$ are:

$$
f_{xx} = \frac{\partial^2 f}{\partial x^2} = \frac{\partial}{\partial x}\!\left(\frac{\partial f}{\partial x}\right), \qquad
f_{yy} = \frac{\partial^2 f}{\partial y^2} = \frac{\partial}{\partial y}\!\left(\frac{\partial f}{\partial y}\right).
$$

The **mixed partial derivatives** are:

$$
f_{xy} = \frac{\partial^2 f}{\partial y\, \partial x} = \frac{\partial}{\partial y}\!\left(\frac{\partial f}{\partial x}\right), \qquad
f_{yx} = \frac{\partial^2 f}{\partial x\, \partial y} = \frac{\partial}{\partial x}\!\left(\frac{\partial f}{\partial y}\right).
$$

**Notation warning.** In $\frac{\partial^2 f}{\partial y\, \partial x}$, differentiation is performed **right to left**: differentiate with respect to $x$ first, then with respect to $y$. In subscript notation $f_{xy}$, differentiation is performed **left to right**: differentiate with respect to $x$ first, then $y$. These conventions are opposite; context determines which is in use. Most textbooks use subscript left-to-right; many physics texts use the Leibniz right-to-left. In this vault: **subscripts go left to right** ($f_{xy}$ means "$x$ first, then $y$").

---


### Definition 1.4.7 — Differentiability in $\mathbb{R}^n$

This is the most important and most misunderstood definition in multivariable calculus.

A function $f(x,y)$ is **differentiable at $(a,b)$** iff there exist real numbers $A$ and $B$ (which will turn out to be $f_x(a,b)$ and $f_y(a,b)$) such that

$$
\lim_{(\Delta x, \Delta y)\to(0,0)} \frac{f(a+\Delta x,\, b+\Delta y) - f(a,b) - A\,\Delta x - B\,\Delta y}{\sqrt{(\Delta x)^2 + (\Delta y)^2}} = 0.
$$

In words: $f$ is differentiable at $(a,b)$ iff $f$ can be **well-approximated by a linear function** near $(a,b)$, with the error going to zero *faster than the displacement*. This is strictly stronger than merely having partial derivatives.

The **linearization** (tangent-plane approximation) of $f$ at $(a,b)$ is

$$
L(x,y) = f(a,b) + f_x(a,b)(x-a) + f_y(a,b)(y-b).
$$

The **total differential** is

$$
df = f_x\,dx + f_y\,dy.
$$

### Definition 1.4.8 — Gradient

The **gradient** of $f$ at $(a,b)$ is the vector of all first partial derivatives:

$$
\nabla f(a,b) = \left\langle f_x(a,b),\; f_y(a,b) \right\rangle = f_x\,\hat{\mathbf{i}} + f_y\,\hat{\mathbf{j}}.
$$

For $f : \mathbb{R}^n \to \mathbb{R}$:

$$
\nabla f = \left\langle \frac{\partial f}{\partial x_1},\; \frac{\partial f}{\partial x_2},\; \ldots,\; \frac{\partial f}{\partial x_n} \right\rangle.
$$

### Definition 1.4.9 — Directional Derivative

The **directional derivative of $f$ at $(a,b)$ in the direction of a unit vector $\hat{\mathbf{u}} = \langle u_1, u_2 \rangle$** ($\|\hat{\mathbf{u}}\| = 1$) is

$$
D_{\hat{\mathbf{u}}} f(a,b) = \lim_{t \to 0} \frac{f(a + tu_1,\, b + tu_2) - f(a,b)}{t}.
$$

If $f$ is differentiable at $(a,b)$, this simplifies to:

$$
D_{\hat{\mathbf{u}}} f(a,b) = \nabla f(a,b) \cdot \hat{\mathbf{u}} = f_x u_1 + f_y u_2.
$$

**The unit-vector requirement is non-negotiable.** If $\mathbf{v}$ is not a unit vector, $D_{\mathbf{v}} f \neq \nabla f \cdot \mathbf{v}$ in general — see Common Pitfalls §11.

---

## 📐 2. Axioms / Postulates

The following are foundational properties of $\mathbb{R}^n$ and its topology assumed without proof at this level.

### Axiom 1.4.A — Completeness of $\mathbb{R}^n$

Every Cauchy sequence in $\mathbb{R}^n$ converges to a point in $\mathbb{R}^n$ (completeness under the Euclidean norm). This underlies all limit arguments.

### Axiom 1.4.B — Equivalence of Norms in $\mathbb{R}^n$

All norms on $\mathbb{R}^n$ are equivalent: there exist constants $c_1, c_2 > 0$ such that $c_1 \|\cdot\|_1 \leq \|\cdot\|_2 \leq c_2 \|\cdot\|_1$ for any two norms. Hence the notion of convergence (and limit) is independent of which norm we use.

### Axiom 1.4.C — The Cauchy-Schwarz Inequality

For any vectors $\mathbf{u}, \mathbf{v} \in \mathbb{R}^n$:

$$
|\mathbf{u} \cdot \mathbf{v}| \leq \|\mathbf{u}\|\,\|\mathbf{v}\|,
$$

with equality iff $\mathbf{u}$ and $\mathbf{v}$ are parallel ($\mathbf{u} = \lambda \mathbf{v}$ for some $\lambda \in \mathbb{R}$). This is the linchpin of the steepest-ascent theorem.

---


## 🛡️ 3. Lemmas

### Lemma 1.4.1 — Uniqueness of the Multivariable Limit

If $\lim_{(x,y)\to(a,b)} f(x,y) = L_1$ and $\lim_{(x,y)\to(a,b)} f(x,y) = L_2$, then $L_1 = L_2$.

**Proof.** Identical in structure to the 1D uniqueness proof (Lemma 1.1.1). Set $\varepsilon = \frac{1}{2}|L_1 - L_2|$ and use the triangle inequality. The multivariable distance $\|(x,y)-(a,b)\|$ plays the role of $|x-a|$. $\blacksquare$

### Lemma 1.4.2 — Path Criterion (Necessary Condition for Existence)

If $\lim_{(x,y)\to(a,b)} f(x,y) = L$ exists, then for **every** continuous curve $\gamma : (-\epsilon, \epsilon) \to \mathbb{R}^2$ with $\gamma(0) = (a,b)$ and $\gamma(t) \neq (a,b)$ for $t \neq 0$:

$$
\lim_{t \to 0} f(\gamma(t)) = L.
$$

**Proof.** Fix such a curve $\gamma$. Given $\varepsilon > 0$, let $\delta > 0$ be the value furnished by the limit definition. Since $\gamma$ is continuous at $0$ and $\gamma(0) = (a,b)$, there exists $\eta > 0$ such that $|t| < \eta \Rightarrow \|\gamma(t) - (a,b)\| < \delta$. Hence for $0 < |t| < \eta$, we have $0 < \|\gamma(t)-(a,b)\| < \delta$, so $|f(\gamma(t)) - L| < \varepsilon$. Since $\varepsilon$ was arbitrary, $\lim_{t\to 0} f(\gamma(t)) = L$. $\blacksquare$

**Contrapositive (the workhorse for disproofs):** If two paths through $(a,b)$ give different limiting values, the limit does not exist.

### Lemma 1.4.3 — The Increment Lemma

If $f$ is differentiable at $(a,b)$ in the sense of Definition 1.4.7, then

$$
f(a+\Delta x,\, b+\Delta y) - f(a,b) = f_x(a,b)\,\Delta x + f_y(a,b)\,\Delta y + \varepsilon_1\,\Delta x + \varepsilon_2\,\Delta y,
$$

where $\varepsilon_1, \varepsilon_2 \to 0$ as $(\Delta x, \Delta y) \to (0,0)$.

**Proof sketch.** Let $r = \sqrt{(\Delta x)^2+(\Delta y)^2}$. Differentiability means the error $E = f(a+\Delta x, b+\Delta y) - f(a,b) - f_x \Delta x - f_y \Delta y$ satisfies $E/r \to 0$. Define $\varepsilon_1 = (E\,\Delta x)/r^2$ and $\varepsilon_2 = (E\,\Delta y)/r^2$ when $r > 0$, and $0$ otherwise. Since $|\Delta x|/r \leq 1$ and $|\Delta y|/r \leq 1$, we get $|\varepsilon_1| \leq |E|/r \to 0$ and $|\varepsilon_2| \leq |E|/r \to 0$. $\blacksquare$

---

## 👑 4. Major Theorems

### Theorem 1.4.1 — Differentiable $\Rightarrow$ Continuous

If $f$ is differentiable at $(a,b)$, then $f$ is continuous at $(a,b)$.

### Theorem 1.4.2 — Continuous Partials $\Rightarrow$ Differentiable

If $f_x$ and $f_y$ both exist in an open neighborhood of $(a,b)$ and are **continuous at $(a,b)$**, then $f$ is differentiable at $(a,b)$.

### Theorem 1.4.3 — Clairaut's Theorem (Equality of Mixed Partials)

If $f_{xy}$ and $f_{yx}$ both exist in an open neighborhood of $(a,b)$ and are **continuous at $(a,b)$**, then

$$
f_{xy}(a,b) = f_{yx}(a,b).
$$

### Theorem 1.4.4 — Multivariable Chain Rule

Let $f(x,y)$ be differentiable, and let $x = x(t)$, $y = y(t)$ be differentiable functions of $t$. Then $F(t) = f(x(t), y(t))$ is differentiable and

$$
\frac{dF}{dt} = \frac{\partial f}{\partial x}\frac{dx}{dt} + \frac{\partial f}{\partial y}\frac{dy}{dt} = \nabla f \cdot \frac{d\mathbf{r}}{dt}.
$$

More generally, if $\mathbf{x} = \mathbf{x}(\mathbf{s})$ maps $\mathbb{R}^m \to \mathbb{R}^n$ and $f : \mathbb{R}^n \to \mathbb{R}$, then $\partial f / \partial s_i = \sum_j (\partial f/\partial x_j)(\partial x_j/\partial s_i)$.

### Theorem 1.4.5 — Gradient Points in Direction of Steepest Ascent

If $f$ is differentiable at $(a,b)$ with $\nabla f(a,b) \neq \mathbf{0}$, then:

- The maximum value of $D_{\hat{\mathbf{u}}} f(a,b)$ over all unit vectors $\hat{\mathbf{u}}$ is $\|\nabla f(a,b)\|$.
- This maximum is attained when $\hat{\mathbf{u}} = \nabla f(a,b) / \|\nabla f(a,b)\|$ (direction of gradient).
- The gradient is **perpendicular to every level curve** through $(a,b)$.

---


## ✍️ 5. Proofs / Derivations

### 5.1 — Proof: Path Dependence Kills the Limit (Theorem 1.4.1 Counterexample Setup)

**Claim.** $\displaystyle\lim_{(x,y)\to(0,0)} \frac{xy}{x^2+y^2}$ does not exist.

**Setup.** Suppose for contradiction that the limit exists and equals $L$.

**Path 1 — Along the $x$-axis: $y = 0$, $x \to 0$.**

Restrict to points $(x, 0)$ with $x \neq 0$:

$$
f(x, 0) = \frac{x \cdot 0}{x^2 + 0^2} = \frac{0}{x^2} = 0.
$$

So $\lim_{x \to 0} f(x,0) = 0$. By Lemma 1.4.2, if the limit $L$ exists, $L = 0$.

**Path 2 — Along the diagonal: $y = x$, $x \to 0$.**

Restrict to points $(x, x)$ with $x \neq 0$:

$$
f(x, x) = \frac{x \cdot x}{x^2 + x^2} = \frac{x^2}{2x^2} = \frac{1}{2}.
$$

So $\lim_{x \to 0} f(x,x) = \frac{1}{2}$. By Lemma 1.4.2, if the limit $L$ exists, $L = \frac{1}{2}$.

**Contradiction.** We derived $L = 0$ and $L = \frac{1}{2}$. Since $0 \neq \frac{1}{2}$, and limits are unique (Lemma 1.4.1), the limit cannot exist. $\blacksquare$

**General pattern.** Approach along $y = mx$:

$$
f(x, mx) = \frac{x \cdot mx}{x^2 + m^2x^2} = \frac{mx^2}{(1+m^2)x^2} = \frac{m}{1+m^2}.
$$

This value depends on $m$ — a different answer for every slope. Even uncountably many paths disagree with each other. The limit is comprehensively non-existent.

---

### 5.2 — Proof: Partials Exist $\not\Rightarrow$ Differentiable

**The counterexample.** Define

$$
f(x,y) = \begin{cases} \dfrac{xy}{\sqrt{x^2+y^2}} & (x,y) \neq (0,0) \\[6pt] 0 & (x,y) = (0,0) \end{cases}
$$

**Step 1: Both partial derivatives exist at the origin.**

$$
f_x(0,0) = \lim_{h \to 0} \frac{f(h,0) - f(0,0)}{h} = \lim_{h \to 0} \frac{\frac{h \cdot 0}{\sqrt{h^2+0}} - 0}{h} = \lim_{h \to 0} \frac{0}{h} = 0.
$$

Similarly, $f_y(0,0) = 0$.

**Step 2: Check the differentiability condition.**

If $f$ were differentiable at $(0,0)$ with $f_x = f_y = 0$, the linearization $L(x,y) = 0$ would satisfy

$$
\lim_{(x,y)\to(0,0)} \frac{f(x,y) - 0}{\sqrt{x^2+y^2}} = 0.
$$

But compute this ratio for $(x,y) \neq (0,0)$:

$$
\frac{f(x,y)}{\sqrt{x^2+y^2}} = \frac{xy/({\sqrt{x^2+y^2}})}{\sqrt{x^2+y^2}} = \frac{xy}{x^2+y^2}.
$$

We just proved above (§5.1 with this exact expression) that this limit **does not exist** (it equals $m/(1+m^2)$ along $y = mx$, which varies with $m$). Therefore the differentiability condition fails.

**Conclusion.** $f_x(0,0)$ and $f_y(0,0)$ both exist and equal $0$, but $f$ is NOT differentiable at $(0,0)$. The existence of partial derivatives is strictly weaker than differentiability. $\blacksquare$

---

### 5.3 — Proof: Differentiable $\Rightarrow$ Continuous (Theorem 1.4.1)

**Assume** $f$ is differentiable at $(a,b)$, i.e., by the Increment Lemma (1.4.3):

$$
f(a+\Delta x, b+\Delta y) - f(a,b) = f_x\,\Delta x + f_y\,\Delta y + \varepsilon_1\,\Delta x + \varepsilon_2\,\Delta y,
$$

where $\varepsilon_1, \varepsilon_2 \to 0$ as $(\Delta x, \Delta y) \to (0,0)$.

**Show continuity.** We need $\lim_{(\Delta x,\Delta y)\to(0,0)} [f(a+\Delta x, b+\Delta y) - f(a,b)] = 0$.

Let $r = \sqrt{(\Delta x)^2 + (\Delta y)^2}$. Then $|\Delta x| \leq r$ and $|\Delta y| \leq r$. So:

$$
|f(a+\Delta x, b+\Delta y) - f(a,b)| \leq |f_x||\Delta x| + |f_y||\Delta y| + |\varepsilon_1||\Delta x| + |\varepsilon_2||\Delta y|
$$

$$
\leq (|f_x| + |f_y| + |\varepsilon_1| + |\varepsilon_2|) \cdot r.
$$

As $r \to 0$: the factor $r \to 0$, and $\varepsilon_1, \varepsilon_2 \to 0$ while $|f_x|$ and $|f_y|$ are fixed finite constants. Hence the entire right side tends to $0$. Therefore:

$$
\lim_{(\Delta x,\Delta y)\to(0,0)} [f(a+\Delta x, b+\Delta y) - f(a,b)] = 0,
$$

which is precisely the statement that $f$ is continuous at $(a,b)$. $\blacksquare$

---

### 5.4 — Proof Sketch: Continuous Partials $\Rightarrow$ Differentiable (Theorem 1.4.2)

**Strategy.** Write the increment $f(a+\Delta x, b+\Delta y) - f(a,b)$ as a telescoping sum and apply the Mean Value Theorem twice.

**Step 1: Telescope.**

$$
f(a+\Delta x, b+\Delta y) - f(a,b) = \underbrace{[f(a+\Delta x, b+\Delta y) - f(a, b+\Delta y)]}_{\text{vary }x} + \underbrace{[f(a, b+\Delta y) - f(a,b)]}_{\text{vary }y}.
$$

**Step 2: Apply MVT to each bracket.** Applying the single-variable MVT to $g_1(x) = f(x, b+\Delta y)$ on $[a, a+\Delta x]$: there exists $c_1$ between $a$ and $a+\Delta x$ such that

$$
f(a+\Delta x, b+\Delta y) - f(a, b+\Delta y) = f_x(c_1, b+\Delta y)\,\Delta x.
$$

Applying MVT to $g_2(y) = f(a,y)$ on $[b, b+\Delta y]$: there exists $c_2$ between $b$ and $b+\Delta y$ such that

$$
f(a, b+\Delta y) - f(a,b) = f_y(a, c_2)\,\Delta y.
$$

**Step 3: Write the increment.**

$$
f(a+\Delta x, b+\Delta y) - f(a,b) = f_x(c_1, b+\Delta y)\,\Delta x + f_y(a, c_2)\,\Delta y.
$$

**Step 4: Rewrite using continuity of partials.** Since $f_x$ is continuous at $(a,b)$ and $(c_1, b+\Delta y) \to (a,b)$ as $(\Delta x, \Delta y) \to (0,0)$:

$$
f_x(c_1, b+\Delta y) = f_x(a,b) + \varepsilon_1, \quad \text{where } \varepsilon_1 \to 0.
$$

Similarly, $f_y(a,c_2) = f_y(a,b) + \varepsilon_2$ with $\varepsilon_2 \to 0$.

**Step 5: Substitute.**

$$
f(a+\Delta x, b+\Delta y) - f(a,b) = f_x(a,b)\,\Delta x + f_y(a,b)\,\Delta y + \varepsilon_1\,\Delta x + \varepsilon_2\,\Delta y.
$$

This is exactly the Increment Lemma form, confirming differentiability (since $\varepsilon_1 \Delta x / r \leq |\varepsilon_1| \to 0$ and similarly for the other term). $\blacksquare$

---


### 5.5 — Proof of Clairaut's Theorem (Theorem 1.4.3)

**Setup.** We want to show $f_{xy}(a,b) = f_{yx}(a,b)$ assuming both mixed partials are continuous at $(a,b)$.

**Key construct.** Define the two-variable difference

$$
\Delta(h,k) = f(a+h, b+k) - f(a+h, b) - f(a, b+k) + f(a,b).
$$

We will evaluate $\Delta(h,k)$ in two ways and compare.

**Way 1 — Vary $x$ first.** Define $\phi(x) = f(x, b+k) - f(x, b)$. Then $\Delta(h,k) = \phi(a+h) - \phi(a)$. By the MVT applied to $\phi$ on $[a, a+h]$: there exists $\theta_1 \in (0,1)$ such that

$$
\Delta(h,k) = h\,\phi'(a + \theta_1 h) = h\,[f_x(a+\theta_1 h, b+k) - f_x(a+\theta_1 h, b)].
$$

Apply the MVT a second time to $g(y) = f_x(a+\theta_1 h, y)$ on $[b, b+k]$: there exists $\theta_2 \in (0,1)$ such that

$$
\Delta(h,k) = h\,k\, f_{xy}(a+\theta_1 h,\, b+\theta_2 k).
$$

**Way 2 — Vary $y$ first.** Define $\psi(y) = f(a+h, y) - f(a, y)$. Then $\Delta(h,k) = \psi(b+k) - \psi(b)$. By the MVT: there exists $\sigma_1 \in (0,1)$ such that

$$
\Delta(h,k) = k\,\psi'(b+\sigma_1 k) = k\,[f_y(a+h, b+\sigma_1 k) - f_y(a, b+\sigma_1 k)].
$$

MVT again on $[a, a+h]$: there exists $\sigma_2 \in (0,1)$ such that

$$
\Delta(h,k) = h\,k\, f_{yx}(a + \sigma_2 h,\, b+\sigma_1 k).
$$

**Equate.** Both expressions equal $\Delta(h,k)$, so (for $hk \neq 0$):

$$
f_{xy}(a+\theta_1 h, b+\theta_2 k) = f_{yx}(a+\sigma_2 h, b+\sigma_1 k).
$$

**Take $h, k \to 0$.** The points $(a+\theta_1 h, b+\theta_2 k) \to (a,b)$ and $(a+\sigma_2 h, b+\sigma_1 k) \to (a,b)$. By continuity of $f_{xy}$ and $f_{yx}$ at $(a,b)$:

$$
f_{xy}(a,b) = f_{yx}(a,b). \quad \blacksquare
$$

---

### 5.6 — Proof of the Multivariable Chain Rule (Theorem 1.4.4)

**Setup.** $f(x,y)$ differentiable; $x = x(t)$, $y = y(t)$ differentiable. Write $F(t) = f(x(t), y(t))$.

**Step 1: Increment.** For a small increment $\Delta t$, let $\Delta x = x(t+\Delta t) - x(t)$ and $\Delta y = y(t+\Delta t) - y(t)$. By the Increment Lemma (1.4.3) applied to $f$:

$$
\Delta F = f_x\,\Delta x + f_y\,\Delta y + \varepsilon_1\,\Delta x + \varepsilon_2\,\Delta y,
$$

where $\varepsilon_1, \varepsilon_2 \to 0$ as $(\Delta x, \Delta y) \to (0,0)$.

**Step 2: Divide by $\Delta t$ (assuming $\Delta t \neq 0$).**

$$
\frac{\Delta F}{\Delta t} = f_x \frac{\Delta x}{\Delta t} + f_y \frac{\Delta y}{\Delta t} + \varepsilon_1 \frac{\Delta x}{\Delta t} + \varepsilon_2 \frac{\Delta y}{\Delta t}.
$$

**Step 3: Take $\Delta t \to 0$.**

- $\Delta x / \Delta t \to x'(t) = \dot x$ and $\Delta y / \Delta t \to y'(t) = \dot y$ (by differentiability of $x$ and $y$).
- As $\Delta t \to 0$, $\Delta x \to 0$ and $\Delta y \to 0$ (since $x$ and $y$ are continuous), so $(\Delta x, \Delta y) \to (0,0)$, hence $\varepsilon_1, \varepsilon_2 \to 0$.
- The error terms: $\varepsilon_1 \,(\Delta x/\Delta t) \to 0 \cdot \dot x = 0$ and similarly for $\varepsilon_2$.

**Step 4: Conclusion.**

$$
\frac{dF}{dt} = f_x \dot x + f_y \dot y = \frac{\partial f}{\partial x}\frac{dx}{dt} + \frac{\partial f}{\partial y}\frac{dy}{dt}. \quad \blacksquare
$$

---

### 5.7 — Proof: Gradient Points in Direction of Steepest Ascent (Theorem 1.4.5)

**Setup.** Let $\hat{\mathbf{u}} = \langle u_1, u_2 \rangle$ be any unit vector ($\|\hat{\mathbf{u}}\| = 1$). The directional derivative is

$$
D_{\hat{\mathbf{u}}} f = \nabla f \cdot \hat{\mathbf{u}} = \|\nabla f\|\,\|\hat{\mathbf{u}}\|\cos\theta = \|\nabla f\|\cos\theta,
$$

where $\theta$ is the angle between $\nabla f$ and $\hat{\mathbf{u}}$. (Here we used the Cauchy-Schwarz definition of dot product, Axiom 1.4.C.)

**Maximum value.** $\cos\theta$ is maximized at $\theta = 0$, giving

$$
\max_{\|\hat{\mathbf{u}}\|=1} D_{\hat{\mathbf{u}}} f = \|\nabla f\| \cdot 1 = \|\nabla f\|.
$$

This maximum is achieved when $\hat{\mathbf{u}}$ is parallel to $\nabla f$, i.e., $\hat{\mathbf{u}} = \nabla f / \|\nabla f\|$.

**Perpendicularity to level curves.** Let $\mathcal{C}$ be the level curve $f(x,y) = c$ through $(a,b)$, parameterized by $\mathbf{r}(t) = (x(t), y(t))$ with $\mathbf{r}(0) = (a,b)$. Then $f(x(t), y(t)) = c$ for all $t$. Differentiate both sides with respect to $t$ using the chain rule:

$$
\frac{\partial f}{\partial x}\dot x + \frac{\partial f}{\partial y}\dot y = 0 \;\Longrightarrow\; \nabla f \cdot \dot{\mathbf{r}} = 0.
$$

So $\nabla f$ is perpendicular to the tangent vector $\dot{\mathbf{r}}$ of every level curve at $(a,b)$. $\blacksquare$

---


## 🖼️ SVG 2 — Multivariable $\varepsilon$–$\delta$: Disk and Slab

The $\varepsilon$–$\delta$ picture in two variables: a **disk of radius $\delta$** in the $xy$-plane around $(a,b)$, and an **$\varepsilon$-slab** around $L$ on the $z$-axis. The limit says: every function value over the disk falls within the slab.

![math-01__1.4-fig2](math-01__1.4-fig2.svg)

---

## 🎯 6. Worked Examples

### Example 1.4.E1 — Limit via Polar Coordinates

**Evaluate** $\displaystyle\lim_{(x,y)\to(0,0)} \frac{x^2 y}{x^2+y^2}$.

**Step 1: Substitute polar coordinates.** Let $x = r\cos\theta$ and $y = r\sin\theta$, where $r = \sqrt{x^2+y^2} \geq 0$. Then $(x,y) \to (0,0)$ iff $r \to 0^+$.

**Step 2: Rewrite the expression.**

$$
\frac{x^2 y}{x^2 + y^2} = \frac{r^2\cos^2\theta \cdot r\sin\theta}{r^2} = r\cos^2\theta\,\sin\theta.
$$

**Step 3: Bound using trigonometric estimates.** For all $\theta$: $|\cos^2\theta| \leq 1$ and $|\sin\theta| \leq 1$, so

$$
\left|r\cos^2\theta\,\sin\theta\right| \leq r \cdot 1 \cdot 1 = r.
$$

**Step 4: Squeeze.** Since $-r \leq r\cos^2\theta\sin\theta \leq r$ and $r \to 0$:

$$
\lim_{r\to 0^+} r\cos^2\theta\,\sin\theta = 0 \quad \text{uniformly in } \theta.
$$

**Step 5: Conclude.**

$$
\boxed{\lim_{(x,y)\to(0,0)} \frac{x^2 y}{x^2+y^2} = 0.}
$$

The key check: the bound $r$ is **independent of $\theta$**, so the convergence is uniform over all approach directions. This is what makes polar coordinates a valid proof technique for such limits.

---

### Example 1.4.E2 — Showing a Limit Does NOT Exist

**Show** $\displaystyle\lim_{(x,y)\to(0,0)} \frac{xy}{x^2+y^2}$ does not exist.

**Path 1 — Along $y = 0$:**

$$
f(x,0) = \frac{x \cdot 0}{x^2 + 0} = 0 \;\xrightarrow{x\to 0}\; 0.
$$

**Path 2 — Along $y = x$:**

$$
f(x,x) = \frac{x \cdot x}{x^2 + x^2} = \frac{x^2}{2x^2} = \frac{1}{2} \;\xrightarrow{x\to 0}\; \frac{1}{2}.
$$

Since $0 \neq \frac{1}{2}$, by Lemma 1.4.2 the limit does not exist. $\blacksquare$

(For full details, see the complete proof in §5.1.)

---

### Example 1.4.E3 — All First and Second Partials, Verifying Clairaut

**Compute all first and second partial derivatives of $f(x,y) = x^2 y + \sin(xy)$. Verify Clairaut's theorem.**

**First partials.**

Treat $y$ as constant for $f_x$:

$$
f_x = \frac{\partial}{\partial x}\left[x^2 y + \sin(xy)\right] = 2xy + \cos(xy) \cdot y = 2xy + y\cos(xy).
$$

Treat $x$ as constant for $f_y$:

$$
f_y = \frac{\partial}{\partial y}\left[x^2 y + \sin(xy)\right] = x^2 + \cos(xy) \cdot x = x^2 + x\cos(xy).
$$

**Second pure partials.**

Differentiate $f_x = 2xy + y\cos(xy)$ with respect to $x$:

$$
f_{xx} = \frac{\partial}{\partial x}[2xy + y\cos(xy)] = 2y + y \cdot (-\sin(xy)) \cdot y = 2y - y^2\sin(xy).
$$

Differentiate $f_y = x^2 + x\cos(xy)$ with respect to $y$:

$$
f_{yy} = \frac{\partial}{\partial y}[x^2 + x\cos(xy)] = 0 + x \cdot (-\sin(xy)) \cdot x = -x^2\sin(xy).
$$

**Mixed partial $f_{xy}$** (differentiate $f_x$ with respect to $y$):

$$
f_{xy} = \frac{\partial}{\partial y}[2xy + y\cos(xy)] = 2x + \cos(xy) + y\cdot(-\sin(xy))\cdot x = 2x + \cos(xy) - xy\sin(xy).
$$

**Mixed partial $f_{yx}$** (differentiate $f_y$ with respect to $x$):

$$
f_{yx} = \frac{\partial}{\partial x}[x^2 + x\cos(xy)] = 2x + \cos(xy) + x\cdot(-\sin(xy))\cdot y = 2x + \cos(xy) - xy\sin(xy).
$$

**Clairaut check.** Both mixed partials equal $2x + \cos(xy) - xy\sin(xy)$. Since $\sin$ and $\cos$ are continuous everywhere, Clairaut's theorem applies and indeed $f_{xy} = f_{yx}$. $\checkmark$

---

### Example 1.4.E4 — Tangent Plane

**Find the equation of the tangent plane to $z = x^2 + y^2$ at the point $(1, 1, 2)$.**

**Step 1: Compute partial derivatives.**

$$
f_x = \frac{\partial}{\partial x}(x^2 + y^2) = 2x, \qquad f_y = \frac{\partial}{\partial y}(x^2 + y^2) = 2y.
$$

**Step 2: Evaluate at $(1,1)$.**

$$
f_x(1,1) = 2(1) = 2, \qquad f_y(1,1) = 2(1) = 2.
$$

**Step 3: Tangent plane equation.** Using the linearization formula $z = f(a,b) + f_x(a,b)(x-a) + f_y(a,b)(y-b)$:

$$
z = 2 + 2(x-1) + 2(y-1) = 2 + 2x - 2 + 2y - 2 = 2x + 2y - 2.
$$

$$
\boxed{z = 2x + 2y - 2.}
$$

**Verification.** At $(1,1)$: $z = 2(1) + 2(1) - 2 = 2$. Correct. The surface value there is $1^2 + 1^2 = 2$. Correct. $\checkmark$

---

### Example 1.4.E5 — Gradient and Directional Derivative

**Compute the gradient of $f(x,y) = e^{xy}$ at $(1,0)$, and find $D_{\hat{\mathbf{u}}} f(1,0)$ along $\mathbf{u} = (1,1)/\sqrt{2}$.**

**Step 1: Partial derivatives.**

$$
f_x = \frac{\partial}{\partial x}e^{xy} = ye^{xy}, \qquad f_y = \frac{\partial}{\partial y}e^{xy} = xe^{xy}.
$$

**Step 2: Evaluate at $(1,0)$.**

$$
f_x(1,0) = 0 \cdot e^{0} = 0, \qquad f_y(1,0) = 1 \cdot e^{0} = 1.
$$

**Step 3: Gradient.**

$$
\nabla f(1,0) = \langle 0, 1 \rangle.
$$

**Step 4: Verify $\hat{\mathbf{u}}$ is a unit vector.**

$$
\|\hat{\mathbf{u}}\| = \left\|\left\langle\frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}}\right\rangle\right\| = \sqrt{\frac{1}{2} + \frac{1}{2}} = 1. \checkmark
$$

**Step 5: Directional derivative.**

$$
D_{\hat{\mathbf{u}}} f(1,0) = \nabla f(1,0) \cdot \hat{\mathbf{u}} = \langle 0, 1\rangle \cdot \left\langle\frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}}\right\rangle = 0 \cdot \frac{1}{\sqrt{2}} + 1 \cdot \frac{1}{\sqrt{2}} = \frac{1}{\sqrt{2}}.
$$

$$
\boxed{D_{\hat{\mathbf{u}}} f(1,0) = \frac{1}{\sqrt{2}} = \frac{\sqrt{2}}{2}.}
$$

---


### Example 1.4.E6 — Multivariable Chain Rule

**Compute $dF/dt$ for $F(t) = f(x(t), y(t))$ where $f(x,y) = x^2 + y^2$, $x(t) = \cos t$, $y(t) = \sin t$.**

**Method 1 — Direct substitution, then differentiate.**

$$
F(t) = \cos^2 t + \sin^2 t = 1.
$$

$$
\frac{dF}{dt} = 0.
$$

**Method 2 — Chain rule (as a check).**

$$
\frac{\partial f}{\partial x} = 2x, \quad \frac{\partial f}{\partial y} = 2y, \quad \frac{dx}{dt} = -\sin t, \quad \frac{dy}{dt} = \cos t.
$$

$$
\frac{dF}{dt} = \frac{\partial f}{\partial x}\frac{dx}{dt} + \frac{\partial f}{\partial y}\frac{dy}{dt} = 2x(-\sin t) + 2y(\cos t).
$$

Substitute $x = \cos t$, $y = \sin t$:

$$
= 2\cos t(-\sin t) + 2\sin t(\cos t) = -2\cos t\sin t + 2\sin t\cos t = 0.
$$

Both methods agree: $dF/dt = 0$. Of course — $f(x,y) = x^2+y^2$ measures distance from the origin squared, and $(\cos t, \sin t)$ traces the unit circle — constant distance! $\checkmark$

---

### Example 1.4.E7 — Implicit Partial Differentiation

**From the constraint $x^2 + y^2 + z^2 = 1$, find $\partial z / \partial x$.**

**Setup.** Define $F(x,y,z) = x^2 + y^2 + z^2 - 1 = 0$. We view $z$ implicitly as a function $z = z(x,y)$ in a neighborhood of a point where $\partial F/\partial z \neq 0$.

**Differentiate both sides with respect to $x$**, treating $y$ as constant and $z = z(x,y)$:

$$
\frac{\partial}{\partial x}(x^2 + y^2 + z^2 - 1) = 0.
$$

$$
2x + 0 + 2z \frac{\partial z}{\partial x} = 0.
$$

**Solve for $\partial z / \partial x$:**

$$
\frac{\partial z}{\partial x} = -\frac{x}{z}.
$$

This is valid wherever $z \neq 0$. Note the partial derivative of a function defined implicitly has a clean form.

**General formula.** For any $F(x,y,z) = 0$:

$$
\frac{\partial z}{\partial x} = -\frac{\partial F/\partial x}{\partial F/\partial z} = -\frac{F_x}{F_z}.
$$

**Proof of the general formula.** Differentiate $F(x,y,z(x,y)) = 0$ with respect to $x$ via chain rule:

$$
F_x \cdot 1 + F_y \cdot 0 + F_z \cdot \frac{\partial z}{\partial x} = 0 \;\Longrightarrow\; \frac{\partial z}{\partial x} = -\frac{F_x}{F_z}.
$$

For our example: $F_x = 2x$, $F_z = 2z$, so $\partial z / \partial x = -2x/(2z) = -x/z$. $\checkmark$

---

### Example 1.4.E8 — Second Derivative Test and the Hessian

**Classify the critical point of $f(x,y) = x^2 - y^2$.**

**Step 1: Find critical points.** Set both partials to zero:

$$
f_x = 2x = 0 \;\Rightarrow\; x = 0, \qquad f_y = -2y = 0 \;\Rightarrow\; y = 0.
$$

The only critical point is $(0,0)$.

**Step 2: Compute the second partials.**

$$
f_{xx} = 2, \qquad f_{yy} = -2, \qquad f_{xy} = 0.
$$

**Step 3: Form the Hessian determinant (the discriminant).**

$$
D = f_{xx}\,f_{yy} - (f_{xy})^2 = (2)(-2) - 0^2 = -4.
$$

**Step 4: Apply the second derivative test.**

- $D < 0$: **saddle point**.
- $D > 0$ and $f_{xx} > 0$: local minimum.
- $D > 0$ and $f_{xx} < 0$: local maximum.
- $D = 0$: test inconclusive.

Here $D = -4 < 0$, so $(0,0)$ is a **saddle point** of $f(x,y) = x^2 - y^2$.

**Geometric intuition.** Along the $x$-axis, $f(x,0) = x^2$ is a upward parabola (local min in this direction). Along the $y$-axis, $f(0,y) = -y^2$ is a downward parabola (local max in this direction). The surface looks like a hyperbolic paraboloid (a "saddle" or "Pringle"). $\checkmark$

---


## 🖼️ SVG 3 — Two Paths to the Origin (DNE Counterexample)

Two curves approaching the origin along $y = 0$ (limit $= 0$) and $y = x$ (limit $= 1/2$), demonstrating that $\lim_{(x,y)\to(0,0)} xy/(x^2+y^2)$ does not exist.

![math-01__1.4-fig3](math-01__1.4-fig3.svg)

---

## 🖼️ SVG 4 — Gradient Vector Field and Level Curves

The gradient $\nabla f$ is always perpendicular to the level curves. Here the level curves of $f(x,y) = x^2 + y^2$ (circles) are shown alongside gradient vectors pointing radially outward (the direction of steepest ascent from the origin).

![math-01__1.4-fig4](math-01__1.4-fig4.svg)

---


## 🖼️ SVG 5 — Tangent Plane Touching a Surface

The tangent plane at $(1,1,2)$ to $z = x^2 + y^2$: the plane $z = 2x + 2y - 2$ kissing the paraboloid at exactly one point.

![math-01__1.4-fig5](math-01__1.4-fig5.svg)

---

## 📝 7. Challenge Problems

> ⚠️ Write each solution completely by hand before opening the spoiler. Every step must be shown.

### Problem 1.4.P1 — Polar Limit

Evaluate $\displaystyle\lim_{(x,y)\to(0,0)} \frac{x^3 + y^3}{x^2 + y^2}$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Substitute polar coordinates.** Set $x = r\cos\theta$, $y = r\sin\theta$, so $r \to 0^+$ as $(x,y) \to (0,0)$.

**Step 2: Rewrite.**

$$
\frac{x^3 + y^3}{x^2 + y^2} = \frac{r^3\cos^3\theta + r^3\sin^3\theta}{r^2} = r(\cos^3\theta + \sin^3\theta).
$$

**Step 3: Bound.** For all $\theta$: $|\cos^3\theta| \leq 1$ and $|\sin^3\theta| \leq 1$, so $|\cos^3\theta + \sin^3\theta| \leq 2$. Therefore:

$$
|r(\cos^3\theta + \sin^3\theta)| \leq 2r.
$$

**Step 4: Squeeze.** Since $-2r \leq r(\cos^3\theta + \sin^3\theta) \leq 2r$ and $2r \to 0$ as $r \to 0$, by the Squeeze Theorem:

$$
\lim_{(x,y)\to(0,0)} \frac{x^3+y^3}{x^2+y^2} = 0.
$$

Note: the bound $2r$ is **independent of $\theta$**, confirming uniform convergence over all paths. $\blacksquare$

</details>

---

### Problem 1.4.P2 — Three-Path Argument

Show that $\displaystyle\lim_{(x,y)\to(0,0)} \frac{x^2 y^2}{x^4 + y^4}$ does not exist.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Path 1 — Along $y = 0$:**

$$
f(x, 0) = \frac{x^2 \cdot 0}{x^4 + 0} = 0 \;\to\; 0.
$$

**Path 2 — Along $y = x$:**

$$
f(x,x) = \frac{x^2 \cdot x^2}{x^4 + x^4} = \frac{x^4}{2x^4} = \frac{1}{2} \;\to\; \frac{1}{2}.
$$

Since $0 \neq \frac{1}{2}$, the limit does not exist by Lemma 1.4.2. $\blacksquare$

**Bonus insight.** Along $y = mx$:

$$
f(x, mx) = \frac{x^2 \cdot m^2 x^2}{x^4 + m^4 x^4} = \frac{m^2}{1 + m^4}.
$$

This depends on $m$: at $m=1$, it gives $1/2$; at $m=0$, it gives $0$. Every slope gives a different answer.

</details>

---

### Problem 1.4.P3 — Full Second-Partial Computation

Let $f(x,y) = \ln(x^2 + y^2 + 1)$. Compute all four second partial derivatives $f_{xx}$, $f_{yy}$, $f_{xy}$, $f_{yx}$ and verify Clairaut.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**First partials.** Let $u = x^2 + y^2 + 1$:

$$
f_x = \frac{1}{u} \cdot 2x = \frac{2x}{x^2+y^2+1}, \qquad f_y = \frac{2y}{x^2+y^2+1}.
$$

**Second pure partials.** Differentiate $f_x = 2x/(x^2+y^2+1)$ with respect to $x$ using the quotient rule:

$$
f_{xx} = \frac{2(x^2+y^2+1) - 2x \cdot 2x}{(x^2+y^2+1)^2} = \frac{2y^2 + 2 - 2x^2}{(x^2+y^2+1)^2}.
$$

Similarly:

$$
f_{yy} = \frac{2x^2 + 2 - 2y^2}{(x^2+y^2+1)^2}.
$$

**Mixed partials.** Differentiate $f_x = 2x/(x^2+y^2+1)$ with respect to $y$:

$$
f_{xy} = \frac{0 \cdot (x^2+y^2+1) - 2x \cdot 2y}{(x^2+y^2+1)^2} = \frac{-4xy}{(x^2+y^2+1)^2}.
$$

Differentiate $f_y = 2y/(x^2+y^2+1)$ with respect to $x$:

$$
f_{yx} = \frac{0 \cdot (x^2+y^2+1) - 2y \cdot 2x}{(x^2+y^2+1)^2} = \frac{-4xy}{(x^2+y^2+1)^2}.
$$

**Clairaut check:** $f_{xy} = f_{yx} = -4xy/(x^2+y^2+1)^2$. $\checkmark$

</details>

---

### Problem 1.4.P4 — Directional Derivative and Steepest Ascent

Let $f(x,y) = x^2 y - y^3$. At the point $(2, 1)$:
(a) Find $\nabla f(2,1)$.
(b) Find the direction of steepest ascent and the maximum rate of increase.
(c) Find $D_{\hat{\mathbf{u}}} f(2,1)$ in the direction $\hat{\mathbf{u}} = \langle 3/5, 4/5 \rangle$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Part (a): Gradient.**

$$
f_x = 2xy, \qquad f_y = x^2 - 3y^2.
$$

At $(2,1)$: $f_x(2,1) = 2(2)(1) = 4$, $f_y(2,1) = 4 - 3 = 1$.

$$
\nabla f(2,1) = \langle 4, 1 \rangle.
$$

**Part (b): Steepest ascent.**

Direction: $\hat{\mathbf{g}} = \langle 4, 1\rangle / \|\langle 4, 1\rangle\| = \langle 4, 1\rangle / \sqrt{17}$.

Maximum rate: $\|\nabla f(2,1)\| = \sqrt{4^2 + 1^2} = \sqrt{17}$.

**Part (c): Directional derivative.** First verify $\hat{\mathbf{u}}$ is a unit vector: $\|\langle 3/5, 4/5\rangle\| = \sqrt{9/25 + 16/25} = 1$. $\checkmark$

$$
D_{\hat{\mathbf{u}}} f(2,1) = \nabla f(2,1) \cdot \hat{\mathbf{u}} = \langle 4,1\rangle \cdot \langle 3/5, 4/5\rangle = \frac{12}{5} + \frac{4}{5} = \frac{16}{5}.
$$

</details>

---


### Problem 1.4.P5 — Chain Rule for a Two-Parameter Map

Let $f(x,y) = e^{x^2+y^2}$, $x(s,t) = s\cos t$, $y(s,t) = s\sin t$. Find $\partial F/\partial s$ and $\partial F/\partial t$ where $F(s,t) = f(x(s,t), y(s,t))$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Partial derivatives of $f$:**

$$
f_x = 2x e^{x^2+y^2}, \qquad f_y = 2y e^{x^2+y^2}.
$$

**Partial derivatives of $x$ and $y$:**

$$
\frac{\partial x}{\partial s} = \cos t, \quad \frac{\partial x}{\partial t} = -s\sin t, \quad \frac{\partial y}{\partial s} = \sin t, \quad \frac{\partial y}{\partial t} = s\cos t.
$$

**Chain rule for $\partial F/\partial s$:**

$$
\frac{\partial F}{\partial s} = f_x \frac{\partial x}{\partial s} + f_y \frac{\partial y}{\partial s} = 2x e^{x^2+y^2}\cos t + 2y e^{x^2+y^2}\sin t.
$$

Substitute $x = s\cos t$, $y = s\sin t$, and note $x^2 + y^2 = s^2$:

$$
= 2s\cos^2 t\, e^{s^2} + 2s\sin^2 t\, e^{s^2} = 2s(\cos^2 t + \sin^2 t)\,e^{s^2} = 2s\,e^{s^2}.
$$

**Chain rule for $\partial F/\partial t$:**

$$
\frac{\partial F}{\partial t} = f_x \frac{\partial x}{\partial t} + f_y \frac{\partial y}{\partial t} = 2x e^{s^2}(-s\sin t) + 2y e^{s^2}(s\cos t).
$$

$$
= -2s^2\cos t\sin t\,e^{s^2} + 2s^2\sin t\cos t\,e^{s^2} = 0.
$$

This makes sense! $f = e^{x^2+y^2} = e^{s^2}$ is independent of $t$, so $\partial F/\partial t = 0$. $\checkmark$

</details>

---

### Problem 1.4.P6 — Implicit Differentiation (Two Variables)

Let $F(x,y) = x^3 + y^3 - 3xy = 0$ (the folium of Descartes). Find $dy/dx$ using implicit differentiation. Evaluate at $(3/2, 3/2)$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Differentiate both sides with respect to $x$** (viewing $y$ as a function of $x$):

$$
\frac{d}{dx}(x^3 + y^3 - 3xy) = 0.
$$

$$
3x^2 + 3y^2\frac{dy}{dx} - 3\left(y + x\frac{dy}{dx}\right) = 0.
$$

**Step 2: Expand and group.**

$$
3x^2 + 3y^2\frac{dy}{dx} - 3y - 3x\frac{dy}{dx} = 0.
$$

$$
(3y^2 - 3x)\frac{dy}{dx} = 3y - 3x^2.
$$

**Step 3: Solve.**

$$
\frac{dy}{dx} = \frac{3y - 3x^2}{3y^2 - 3x} = \frac{y - x^2}{y^2 - x}.
$$

**Step 4: Evaluate at $(3/2, 3/2)$:**

$$
\frac{dy}{dx}\bigg|_{(3/2,3/2)} = \frac{3/2 - (3/2)^2}{(3/2)^2 - 3/2} = \frac{3/2 - 9/4}{9/4 - 3/2} = \frac{-3/4}{3/4} = -1.
$$

At the point $(3/2, 3/2)$ on the folium, the tangent has slope $-1$.

</details>

---

### Problem 1.4.P7 — Critical Points via Second Derivative Test

Find and classify all critical points of $f(x,y) = x^3 - 3x + y^2 - 4y$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Find critical points.** Set $f_x = f_y = 0$:

$$
f_x = 3x^2 - 3 = 0 \;\Rightarrow\; x^2 = 1 \;\Rightarrow\; x = \pm 1.
$$

$$
f_y = 2y - 4 = 0 \;\Rightarrow\; y = 2.
$$

Critical points: $(1, 2)$ and $(-1, 2)$.

**Step 2: Second partials.**

$$
f_{xx} = 6x, \qquad f_{yy} = 2, \qquad f_{xy} = 0.
$$

**Step 3: Hessian discriminant at each point.**

At $(1, 2)$: $f_{xx} = 6$, $f_{yy} = 2$, $f_{xy} = 0$.

$$
D = f_{xx}f_{yy} - f_{xy}^2 = (6)(2) - 0 = 12 \gt  0.
$$

Since $D \gt  0$ and $f_{xx} = 6 \gt  0$: **local minimum** at $(1, 2)$.

At $(-1, 2)$: $f_{xx} = -6$, $f_{yy} = 2$, $f_{xy} = 0$.

$$
D = (-6)(2) - 0 = -12 \lt  0.
$$

Since $D \lt  0$: **saddle point** at $(-1, 2)$.

**Step 4: Function values.**

$$
f(1,2) = 1 - 3 + 4 - 8 = -6, \qquad f(-1,2) = -1 + 3 + 4 - 8 = -2.
$$

</details>

---

### Problem 1.4.P8 — Tangent Plane to an Implicit Surface

Find the tangent plane to the surface $x^2 + 2y^2 + 3z^2 = 6$ at the point $(1, 1, 1)$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Define $F(x,y,z) = x^2 + 2y^2 + 3z^2 - 6$.** The surface is the level set $F = 0$.

**Step 2: Compute the gradient of $F$ (the normal vector to the surface).**

$$
\nabla F = \langle F_x, F_y, F_z\rangle = \langle 2x, 4y, 6z\rangle.
$$

**Step 3: Evaluate at $(1,1,1)$.**

$$
\nabla F(1,1,1) = \langle 2, 4, 6\rangle.
$$

**Step 4: Tangent plane equation.** The tangent plane at $(x_0, y_0, z_0)$ to $F = 0$ has normal $\nabla F(x_0,y_0,z_0)$:

$$
F_x(x - x_0) + F_y(y - y_0) + F_z(z - z_0) = 0.
$$

$$
2(x-1) + 4(y-1) + 6(z-1) = 0.
$$

$$
2x + 4y + 6z = 12 \;\;\Longrightarrow\;\; x + 2y + 3z = 6.
$$

**Verification:** At $(1,1,1)$: $1 + 2 + 3 = 6$. $\checkmark$

</details>

---


## ⚠️ 8. Common Pitfalls

### Pitfall 1 — "Both partials exist ⟹ Differentiable"

**The classic error.** Students compute $f_x(0,0)$ and $f_y(0,0)$, find they exist, and declare $f$ differentiable. This is **wrong**.

Differentiability (Definition 1.4.7) requires the linear approximation to be accurate to *better than first order* — the existence of two directional derivatives (along coordinate axes) does not constrain what happens in any other direction. The counterexample in §5.2 shows explicitly: both partials at the origin are $0$, yet the function is not differentiable there because the ratio $f(x,y)/\|(x,y)\|$ has no limit.

**The correct hierarchy:**

$$
\text{Continuous partials} \;\Rightarrow\; \text{Differentiable} \;\Rightarrow\; \text{Continuous} \;\Rightarrow\; \text{Partials exist.}
$$

None of the reverse implications hold in general.

### Pitfall 2 — "Two Paths Agree ⟹ Limit Exists"

Checking path 1 and path 2 and getting the same value does **not** prove the limit exists. You need either a formal $\varepsilon$–$\delta$ proof or a polar-coordinate squeeze argument that is uniform in $\theta$. Two paths agreeing is necessary but not sufficient. There exist functions where every *straight line* path gives the same limit, yet the limit does not exist (because a parabolic path gives a different value — cf. $f(x,y) = xy^2/(x^2+y^4)$ along $y=x$ vs. $x = y^2$).

### Pitfall 3 — Directional Derivative Without a Unit Vector

**The formula $D_{\mathbf{v}} f = \nabla f \cdot \mathbf{v}$ requires $\|\mathbf{v}\| = 1$.**

If $\mathbf{v} = \langle 3, 4\rangle$ (which has $\|\mathbf{v}\| = 5 \neq 1$), the correct directional derivative in that direction is

$$
D_{\hat{\mathbf{v}}} f = \nabla f \cdot \frac{\mathbf{v}}{\|\mathbf{v}\|} = \nabla f \cdot \left\langle\frac{3}{5}, \frac{4}{5}\right\rangle.
$$

Using $\nabla f \cdot \langle 3, 4\rangle$ gives a value 5 times too large. In physics, the directional derivative is a rate of change per unit length; the unit-vector requirement enforces the "per unit length" part.

### Pitfall 4 — Confusing $\partial z/\partial x$ with $dz/dx$

$\partial z/\partial x$ holds other variables **constant**. $dz/dx$ is the total derivative — it accounts for how $z$ changes through all its variables. For $z = f(x, y(x))$ where $y$ also depends on $x$:

$$
\frac{dz}{dx} = \frac{\partial f}{\partial x} + \frac{\partial f}{\partial y}\frac{dy}{dx} \neq \frac{\partial f}{\partial x} = \frac{\partial z}{\partial x}.
$$

In thermodynamics this distinction is critical: $({\partial U}/{\partial T})_V$ (partial, constant $V$) $\neq$ $({\partial U}/{\partial T})_P$ (partial, constant $P$). They can differ dramatically.

### Pitfall 5 — Sign Errors in the Hessian Test

The discriminant is $D = f_{xx}f_{yy} - (f_{xy})^2$. Common errors:

- **Computing $D = f_{xx}f_{yy} - f_{xy}^2$ then testing $f_{xx}$, but using $f_{yy}$ by mistake** (for local min/max, check the sign of $f_{xx}$, not $f_{yy}$; they have the same sign when $D>0$ anyway, but always cite $f_{xx}$).
- **Forgetting to square $f_{xy}$**: writing $D = f_{xx}f_{yy} - f_{xy}$ (missing the square).
- **Applying the test when $D = 0$**: the test is inconclusive in this case; further analysis is needed.

### Pitfall 6 — Notation Reversal for Mixed Partials

Some textbooks define $f_{xy}$ as "differentiate with respect to $y$ then $x$" (Leibniz order) while others define it as "differentiate with respect to $x$ then $y$" (subscript order). This vault uses **subscript = left-to-right** ($f_{xy}$ means $x$ first). When reading other sources, always check which convention is used before computing.

---

## 🔗 9. Cross-Links

**Backward (these chapters build this one):**
- [1.1 - Limits & Continuity](1.1---Limits-&-Continuity) — the multivariable limit is a direct generalization of the 1D $\varepsilon$–$\delta$ definition. Every technique from 1.1 (squeeze, path method) appears here.
- [1.2 - Single-Variable Differentiation](1.2---Single-Variable-Differentiation) — partial derivatives are literally 1D derivatives with the other variable held fixed. The chain rule here is the same principle as the single-variable chain rule.

**Forward (this chapter feeds these):**
- [1.5 - Multiple Integrals & Jacobians](1.5---Multiple-Integrals-&-Jacobians) — the Jacobian determinant is built from partial derivatives; the change-of-variables formula requires differentiability.
- [1.6 - Vector Fields, Div & Curl](1.6---Vector-Fields,-Div-&-Curl) — div and curl are defined in terms of partial derivatives of vector-valued functions; the gradient $\nabla f$ is the prototype of a vector field.
- [1.8 - Exterior Algebra & Differential Forms](1.8---Exterior-Algebra-&-Differential-Forms) — the total differential $df = f_x\,dx + f_y\,dy$ is a differential 1-form; this chapter is the conceptual foundation for that entire framework.

**Physics connections:**
- [5.x Thermodynamics](5.x-Thermodynamics) — all of thermodynamics is multivariable calculus. The Maxwell relations ARE Clairaut's theorem: $(\partial T/\partial V)_S = -(\partial P/\partial S)_V$ because $\partial^2 U/\partial S\partial V = \partial^2 U/\partial V\partial S$.
- [7.x Maxwell's Equations](7.x-Maxwell's-Equations) — $\nabla \cdot \mathbf{E}$, $\nabla \times \mathbf{B}$: every term is a partial derivative of a field.
- [8.x Spacetime Gradients in GR](8.x-Spacetime-Gradients-in-GR) — the covariant derivative $\nabla_\mu$ generalizes the gradient to curved spacetime. The flat-space gradient you learn here is the special-relativistic limit.

---

## 🛠️ 10. Pairing with `CalculusVisualizer`

To deepen intuition for this chapter:

1. **3D surface plotting**: Input $f(x,y) = e^{-(x^2+y^2)}$ (Gaussian), display the surface, and overlay level curves. Watch how the gradient vectors align perpendicularly to the contours.
2. **Partial derivative slices**: Hold $y = y_0$ fixed and watch the intersection curve. The tangent slope at $x = x_0$ is exactly $f_x(x_0, y_0)$. Vary $y_0$ to see how $f_x$ changes.
3. **Limit paths**: For $f = xy/(x^2+y^2)$, plot $f$ restricted to a family of lines $y = mx$ and see the value $m/(1+m^2)$ change as $m$ varies.
4. **Tangent plane**: Display the paraboloid $z = x^2+y^2$ and overlay the tangent plane at a movable point. Drag the point and watch the plane update.

---

## 📖 11. Verified Open-Access Sources

All resources verified for authorship, hosting, and adoption.

| Resource | Author/Institution | What it covers |
|---|---|---|
| [MIT 18.02SC — Multivariable Calculus](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/) | MIT OCW, Denis Auroux | Limits, partial derivatives, gradient, chain rule — full lecture notes + problem sets |
| [*Calculus* Vol. 3 — Gilbert Strang, MIT](https://ocw.mit.edu/resources/res-18-001-calculus-online-textbook-spring-2005/) | Gilbert Strang (MIT, 18.01/18.02 for 30 years) | Ch. 11–13: multivariable calculus, complete with proofs |
| [APEX Calculus Vol. 3](https://www.apexcalculus.com/) | Gregory Hartman et al. (open-source, adopted at 100+ institutions) | Chapters 12–13: limits, partial derivatives, gradient, chain rule |
| [Paul's Online Calculus III Notes](https://tutorial.math.lamar.edu/Classes/CalcIII/CalcIII.aspx) | Paul Dawkins (Lamar University) | Accessible but rigorous; covers every topic in this chapter with worked examples |
| [Khan Academy — Multivariable Calculus](https://www.khanacademy.org/math/multivariable-calculus) | Khan Academy (Grant Sanderson guest contributor) | Visual intuition; strong on gradient, directional derivatives, level curves |

---

## 🧠 12. Study Tactics

1. **Limits: always try two paths first**, not to prove existence but to quickly detect non-existence. Only after confirming all paths seem to agree should you reach for polar coordinates or $\varepsilon$–$\delta$.

2. **Partials are just 1D derivatives.** When computing $f_x$, cover $y$ with your thumb. You're computing $d/dx$ of a function of $x$ alone.

3. **Differentiability is the hard condition.** Every time you see "differentiable" in a theorem hypothesis, remember it means the linear approximation is accurate — not just that partials exist.

4. **The Hessian test has a memory aid:** "$D > 0$ means definite; $D < 0$ means indefinite (saddle). Sign of $f_{xx}$ tells min vs max."

5. **Chain rule for all directions.** Before computing $\partial F/\partial s$ in a chain rule problem, draw the dependency diagram: $F \to f \to x,y \to s$. Sum over all intermediate variables.

6. **Clairaut is almost always true.** In practice, if your mixed partials disagree, you've made an arithmetic error. Clairaut's theorem says they must agree whenever the mixed partials are continuous — which they almost always are for textbook functions.

---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

*Previous: [1.3 - Single-Variable Integration](1.3---Single-Variable-Integration) | Next: [1.5 - Multiple Integrals & Jacobians](1.5---Multiple-Integrals-&-Jacobians)*
