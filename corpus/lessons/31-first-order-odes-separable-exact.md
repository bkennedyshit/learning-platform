---
title: "First Order Odes Separable Exact"
subject: "Ordinary & Partial Differential Equations"
catalog: advanced
audience_tier: higher-education
chapter: "3.1"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 3.1 — First-Order ODEs: Separable & Exact

> *"The art of solving a differential equation lies in recognizing its type — for each type admits its own key."* — V. I. Arnold

A first-order ordinary differential equation relates a function $y(x)$ to its first derivative $y'(x)$. This chapter develops the two most fundamental solution techniques: **separation of variables** (when the equation factors into a product of functions of $x$ alone and $y$ alone) and **exact equations** (when the left-hand side is already the total differential of some potential function). We also develop the **integrating factor** method that converts non-exact equations into exact ones.

---

## 🎯 Learning Objectives

1. Classify a first-order ODE as separable, exact, linear, or none of these.
2. Solve separable ODEs by isolating variables and integrating both sides.
3. Test exactness via the condition $\partial M/\partial y = \partial N/\partial x$.
4. Reconstruct the potential function $F(x,y)$ for exact equations.
5. Derive and apply integrating factors $\mu(x)$ or $\mu(y)$ to convert non-exact equations to exact form.
6. Solve first-order linear ODEs $y' + P(x)y = Q(x)$ using the integrating factor $e^{\int P\,dx}$.
7. Verify solutions by substitution back into the original ODE.

---


## 🖼️ Visual Anchor — Slope Field & Solution Curves

![math-03__3.1-fig1](math-03__3.1-fig1.svg)

---


## 📚 1. Definitions

### Definition 3.1.1 — Ordinary Differential Equation (ODE)

An **ordinary differential equation** of order $n$ is an equation of the form:

$$
F\bigl(x,\, y,\, y',\, y'',\, \ldots,\, y^{(n)}\bigr) = 0,
$$

where $y = y(x)$ is the unknown function of a single independent variable $x$, and $y^{(k)}$ denotes the $k$-th derivative $d^k y / dx^k$. A **first-order** ODE has $n = 1$:

$$
F(x, y, y') = 0 \quad \text{or equivalently} \quad y' = f(x, y).
$$

### Definition 3.1.2 — Solution and General Solution

A function $\phi(x)$ defined on an interval $I$ is a **solution** of $y' = f(x,y)$ on $I$ if $\phi'(x) = f(x, \phi(x))$ for all $x \in I$. The **general solution** is the family of all solutions, typically parameterized by an arbitrary constant $C$. An **initial value problem (IVP)** specifies $y(x_0) = y_0$, which determines $C$ uniquely (under Picard-Lindelöf conditions).

### Definition 3.1.3 — Separable Equation

A first-order ODE is **separable** if it can be written in the form:

$$
\frac{dy}{dx} = g(x) \cdot h(y),
$$

so that the variables can be separated:

$$
\frac{1}{h(y)}\,dy = g(x)\,dx.
$$

Integration of both sides yields the implicit solution.

### Definition 3.1.4 — Exact Equation

A first-order ODE written in differential form:

$$
M(x,y)\,dx + N(x,y)\,dy = 0
$$

is **exact** if there exists a function $F(x,y)$ (called the **potential function**) such that:

$$
\frac{\partial F}{\partial x} = M(x,y), \qquad \frac{\partial F}{\partial y} = N(x,y).
$$

The solution is then $F(x,y) = C$ (a level curve of $F$).

### Definition 3.1.5 — Integrating Factor

An **integrating factor** $\mu$ is a function (of $x$, $y$, or both) such that multiplying the equation $M\,dx + N\,dy = 0$ by $\mu$ renders it exact:

$$
\frac{\partial(\mu M)}{\partial y} = \frac{\partial(\mu N)}{\partial x}.
$$

### Definition 3.1.6 — First-Order Linear ODE

A first-order ODE is **linear** if it has the form:

$$
\frac{dy}{dx} + P(x)\,y = Q(x).
$$

The integrating factor is $\mu(x) = e^{\int P(x)\,dx}$, and the general solution is:

$$
y(x) = \frac{1}{\mu(x)}\left[\int \mu(x)\,Q(x)\,dx + C\right].
$$

---


## 📐 2. Axioms / Postulates

**Postulate 3.1.P1 (Continuity of $f$):** We assume $f(x,y)$ is continuous on a rectangular region $R = \{(x,y) : |x - x_0| \leq a,\, |y - y_0| \leq b\}$. This guarantees the existence of at least one solution through $(x_0, y_0)$.

**Postulate 3.1.P2 (Lipschitz Condition):** If additionally $\partial f / \partial y$ exists and is continuous on $R$, then the solution through $(x_0, y_0)$ is **unique**. This is the Picard-Lindelöf existence-uniqueness guarantee.

**Postulate 3.1.P3 (Equality of Mixed Partials):** For $C^2$ functions $F(x,y)$, Clairaut's theorem guarantees $\frac{\partial^2 F}{\partial x \partial y} = \frac{\partial^2 F}{\partial y \partial x}$. This underpins the exactness test.

---

## 🛡️ 3. Lemmas

### Lemma 3.1.1 — Exactness Test

The equation $M(x,y)\,dx + N(x,y)\,dy = 0$ is exact on a simply connected domain if and only if:

$$
\frac{\partial M}{\partial y} = \frac{\partial N}{\partial x}.
$$

**Proof.** ($\Rightarrow$) If the equation is exact, there exists $F$ with $F_x = M$ and $F_y = N$. By Clairaut's theorem (Postulate 3.1.P3):

$$
\frac{\partial M}{\partial y} = \frac{\partial^2 F}{\partial y \partial x} = \frac{\partial^2 F}{\partial x \partial y} = \frac{\partial N}{\partial x}.
$$

($\Leftarrow$) Conversely, assume $M_y = N_x$ on a simply connected domain $D$. Define:

$$
F(x,y) = \int_{x_0}^{x} M(t, y)\,dt + g(y),
$$

where $g(y)$ is to be determined. Then $F_x = M$ by the Fundamental Theorem of Calculus. We need $F_y = N$:

$$
F_y = \int_{x_0}^{x} \frac{\partial M}{\partial y}(t,y)\,dt + g'(y) = \int_{x_0}^{x} \frac{\partial N}{\partial x}(t,y)\,dt + g'(y).
$$

Evaluate the integral using the Fundamental Theorem:

$$
F_y = N(x,y) - N(x_0, y) + g'(y).
$$

Setting $F_y = N(x,y)$ requires $g'(y) = N(x_0, y)$, which is a function of $y$ alone. Integrate to get $g(y) = \int N(x_0, y)\,dy$. This completes the construction of $F$. $\blacksquare$

### Lemma 3.1.2 — Integrating Factor for $\mu = \mu(x)$ Only

If $\frac{M_y - N_x}{N}$ is a function of $x$ alone, say $\frac{M_y - N_x}{N} = \psi(x)$, then:

$$
\mu(x) = e^{\int \psi(x)\,dx}
$$

is an integrating factor that makes $\mu M\,dx + \mu N\,dy = 0$ exact.

**Proof.** We require $\frac{\partial(\mu M)}{\partial y} = \frac{\partial(\mu N)}{\partial x}$. Since $\mu = \mu(x)$ depends only on $x$:

$$
\mu \frac{\partial M}{\partial y} = \mu' N + \mu \frac{\partial N}{\partial x}.
$$

Rearranging:

$$
\mu(M_y - N_x) = \mu' N \implies \frac{\mu'}{\mu} = \frac{M_y - N_x}{N} = \psi(x).
$$

This is a separable ODE in $\mu$:

$$
\frac{d\mu}{\mu} = \psi(x)\,dx \implies \ln|\mu| = \int \psi(x)\,dx \implies \mu(x) = e^{\int \psi(x)\,dx}. \quad \blacksquare
$$

### Lemma 3.1.3 — Integrating Factor for $\mu = \mu(y)$ Only

If $\frac{N_x - M_y}{M}$ is a function of $y$ alone, say $\frac{N_x - M_y}{M} = \phi(y)$, then:

$$
\mu(y) = e^{\int \phi(y)\,dy}
$$

is an integrating factor.

**Proof.** Analogous to Lemma 3.1.2. We require $\frac{\partial(\mu M)}{\partial y} = \frac{\partial(\mu N)}{\partial x}$. Since $\mu = \mu(y)$:

$$
\mu' M + \mu M_y = \mu N_x.
$$

Rearranging: $\frac{\mu'}{\mu} = \frac{N_x - M_y}{M} = \phi(y)$, giving $\mu(y) = e^{\int \phi(y)\,dy}$. $\blacksquare$

---


## 👑 4. Theorems

### Theorem 3.1.1 — Picard-Lindelöf Existence and Uniqueness

Let $f(x,y)$ be continuous on a rectangle $R = \{(x,y) : |x-x_0| \leq a,\, |y-y_0| \leq b\}$ and let $f$ satisfy a Lipschitz condition in $y$:

$$
|f(x, y_1) - f(x, y_2)| \leq L|y_1 - y_2| \quad \forall (x,y_1),(x,y_2) \in R.
$$

Then the initial value problem $y' = f(x,y)$, $y(x_0) = y_0$ has a **unique** solution $y = \phi(x)$ on some interval $|x - x_0| \leq h$ where $h = \min(a, b/M)$ and $M = \max_R |f|$.

### Theorem 3.1.2 — Solution of Separable Equations

If $\frac{dy}{dx} = g(x)h(y)$ with $h(y_0) \neq 0$, then the unique local solution satisfying $y(x_0) = y_0$ is given implicitly by:

$$
\int_{y_0}^{y} \frac{ds}{h(s)} = \int_{x_0}^{x} g(t)\,dt.
$$

### Theorem 3.1.3 — Solution of Exact Equations

If $M\,dx + N\,dy = 0$ is exact (i.e., $M_y = N_x$), then the general solution is $F(x,y) = C$ where:

$$
F(x,y) = \int M(x,y)\,dx + g(y), \quad g'(y) = N(x,y) - \frac{\partial}{\partial y}\int M(x,y)\,dx.
$$

### Theorem 3.1.4 — General Solution of First-Order Linear ODE

The general solution of $y' + P(x)y = Q(x)$ is:

$$
y(x) = e^{-\int P(x)\,dx}\left[\int e^{\int P(x)\,dx} Q(x)\,dx + C\right].
$$

Equivalently, with integrating factor $\mu(x) = e^{\int P(x)\,dx}$:

$$
\frac{d}{dx}\bigl[\mu(x)\,y\bigr] = \mu(x)\,Q(x).
$$

---


## ✍️ 5. Proofs / Derivations

### 5.1 Derivation of the Linear ODE Integrating Factor (Theorem 3.1.4)

Starting from:

$$
\frac{dy}{dx} + P(x)\,y = Q(x). \tag{1}
$$

**Step 1.** Multiply both sides by an unknown function $\mu(x)$:

$$
\mu(x)\frac{dy}{dx} + \mu(x)P(x)\,y = \mu(x)Q(x). \tag{2}
$$

**Step 2.** We want the left side to be the derivative of a product $\frac{d}{dx}[\mu(x)\,y]$. By the product rule:

$$
\frac{d}{dx}[\mu(x)\,y] = \mu(x)\frac{dy}{dx} + \mu'(x)\,y. \tag{3}
$$

**Step 3.** Comparing (2) and (3), we need:

$$
\mu'(x) = \mu(x)\,P(x). \tag{4}
$$

**Step 4.** Equation (4) is itself a separable ODE. Separate variables:

$$
\frac{d\mu}{\mu} = P(x)\,dx.
$$

**Step 5.** Integrate both sides:

$$
\int \frac{d\mu}{\mu} = \int P(x)\,dx \implies \ln|\mu| = \int P(x)\,dx.
$$

**Step 6.** Exponentiate (we may take the positive root since we only need one integrating factor):

$$
\mu(x) = e^{\int P(x)\,dx}. \tag{5}
$$

**Step 7.** With this $\mu$, equation (2) becomes:

$$
\frac{d}{dx}\bigl[\mu(x)\,y\bigr] = \mu(x)\,Q(x).
$$

**Step 8.** Integrate both sides with respect to $x$:

$$
\mu(x)\,y = \int \mu(x)\,Q(x)\,dx + C.
$$

**Step 9.** Solve for $y$:

$$
y(x) = \frac{1}{\mu(x)}\left[\int \mu(x)\,Q(x)\,dx + C\right] = e^{-\int P\,dx}\left[\int e^{\int P\,dx}\,Q(x)\,dx + C\right]. \quad \blacksquare
$$

### 5.2 Proof of Theorem 3.1.2 (Separable Equations)

Given $\frac{dy}{dx} = g(x)\,h(y)$ with $h(y_0) \neq 0$.

**Step 1.** Divide both sides by $h(y)$ (valid near $y_0$ since $h(y_0) \neq 0$ and $h$ is continuous):

$$
\frac{1}{h(y)}\frac{dy}{dx} = g(x).
$$

**Step 2.** Recognize the left side as $\frac{d}{dx}\left[H(y(x))\right]$ where $H(y) = \int_{y_0}^{y} \frac{ds}{h(s)}$ (by the chain rule):

$$
\frac{d}{dx}H(y(x)) = H'(y)\cdot y'(x) = \frac{1}{h(y)}\cdot y'(x).
$$

**Step 3.** Integrate both sides from $x_0$ to $x$:

$$
H(y(x)) - H(y(x_0)) = \int_{x_0}^{x} g(t)\,dt.
$$

**Step 4.** Since $H(y_0) = \int_{y_0}^{y_0} \frac{ds}{h(s)} = 0$:

$$
\int_{y_0}^{y} \frac{ds}{h(s)} = \int_{x_0}^{x} g(t)\,dt. \quad \blacksquare
$$

### 5.3 Proof of Theorem 3.1.3 (Exact Equation Solution Construction)

Given $M\,dx + N\,dy = 0$ with $M_y = N_x$.

**Step 1.** We seek $F(x,y)$ with $F_x = M$ and $F_y = N$. Integrate the first condition with respect to $x$:

$$
F(x,y) = \int M(x,y)\,dx + g(y), \tag{6}
$$

where $g(y)$ is an arbitrary function of $y$ (the "constant" of integration with respect to $x$).

**Step 2.** Differentiate (6) with respect to $y$:

$$
F_y = \frac{\partial}{\partial y}\int M(x,y)\,dx + g'(y).
$$

**Step 3.** Set $F_y = N$:

$$
g'(y) = N(x,y) - \frac{\partial}{\partial y}\int M(x,y)\,dx. \tag{7}
$$

**Step 4.** We must verify that the right side of (7) depends only on $y$ (not on $x$). Differentiate the right side with respect to $x$:

$$
\frac{\partial N}{\partial x} - \frac{\partial}{\partial x}\frac{\partial}{\partial y}\int M\,dx = N_x - M_y = 0,
$$

by the exactness condition. Therefore the right side of (7) is indeed a function of $y$ alone.

**Step 5.** Integrate (7) to find $g(y)$, completing the construction of $F$. The general solution is $F(x,y) = C$. $\blacksquare$

---


## 🧮 6. Worked Examples

### Example 3.1.E1 — Separable Equation (Basic)

**Solve:** $\frac{dy}{dx} = \frac{x^2}{y}$, with $y(0) = 2$.

**Step 1.** Identify as separable: $g(x) = x^2$, $h(y) = 1/y$.

**Step 2.** Separate variables:

$$
y\,dy = x^2\,dx.
$$

**Step 3.** Integrate both sides:

$$
\int y\,dy = \int x^2\,dx \implies \frac{y^2}{2} = \frac{x^3}{3} + C.
$$

**Step 4.** Apply initial condition $y(0) = 2$:

$$
\frac{(2)^2}{2} = \frac{0^3}{3} + C \implies 2 = C.
$$

**Step 5.** Write the explicit solution (taking positive root since $y(0) = 2 > 0$):

$$
\frac{y^2}{2} = \frac{x^3}{3} + 2 \implies y^2 = \frac{2x^3}{3} + 4 \implies y = \sqrt{\frac{2x^3}{3} + 4}.
$$

**Verification:** $y' = \frac{1}{2}\left(\frac{2x^3}{3}+4\right)^{-1/2}\cdot 2x^2 = \frac{x^2}{y}$. ✓

---

### Example 3.1.E2 — Exact Equation

**Solve:** $(2xy + 3)\,dx + (x^2 + 4y)\,dy = 0$.

**Step 1.** Identify $M = 2xy + 3$ and $N = x^2 + 4y$.

**Step 2.** Test exactness:

$$
\frac{\partial M}{\partial y} = 2x, \qquad \frac{\partial N}{\partial x} = 2x.
$$

Since $M_y = N_x = 2x$, the equation is exact.

**Step 3.** Find $F(x,y)$ with $F_x = M = 2xy + 3$. Integrate with respect to $x$:

$$
F(x,y) = \int (2xy + 3)\,dx = x^2 y + 3x + g(y).
$$

**Step 4.** Determine $g(y)$ from $F_y = N$:

$$
F_y = x^2 + g'(y) = x^2 + 4y \implies g'(y) = 4y \implies g(y) = 2y^2.
$$

**Step 5.** The general solution is:

$$
F(x,y) = x^2 y + 3x + 2y^2 = C.
$$

**Verification:** $dF = (2xy+3)\,dx + (x^2+4y)\,dy = 0$. ✓

---

### Example 3.1.E3 — Non-Exact Made Exact via Integrating Factor

**Solve:** $(y^2 + y)\,dx + (xy + 2x)\,dy = 0$.

**Step 1.** Identify $M = y^2 + y$, $N = xy + 2x = x(y+2)$.

**Step 2.** Test exactness:

$$
M_y = 2y + 1, \qquad N_x = y + 2.
$$

Since $M_y \neq N_x$, the equation is not exact.

**Step 3.** Check if $\frac{M_y - N_x}{N}$ depends only on $x$:

$$
\frac{M_y - N_x}{N} = \frac{(2y+1) - (y+2)}{x(y+2)} = \frac{y - 1}{x(y+2)}.
$$

This depends on both $x$ and $y$, so try the other form.

**Step 4.** Check if $\frac{N_x - M_y}{M}$ depends only on $y$:

$$
\frac{N_x - M_y}{M} = \frac{(y+2) - (2y+1)}{y^2+y} = \frac{1-y}{y(y+1)} = \frac{-(y-1)}{y(y+1)}.
$$

This still depends on $y$ in a non-trivial way. Let us use partial fractions:

$$
\frac{-(y-1)}{y(y+1)} = \frac{A}{y} + \frac{B}{y+1}.
$$

Multiply through by $y(y+1)$: $-(y-1) = A(y+1) + By$. Set $y=0$: $1 = A$. Set $y=-1$: $2 = -B$, so $B = -2$.

$$
\frac{N_x - M_y}{M} = \frac{1}{y} - \frac{2}{y+1}.
$$

This is a function of $y$ alone. The integrating factor is:

$$
\mu(y) = e^{\int\left(\frac{1}{y} - \frac{2}{y+1}\right)dy} = e^{\ln|y| - 2\ln|y+1|} = \frac{y}{(y+1)^2}.
$$

**Step 5.** Multiply the original equation by $\mu(y) = \frac{y}{(y+1)^2}$:

$$
\tilde{M} = \frac{y(y^2+y)}{(y+1)^2} = \frac{y^2(y+1)}{(y+1)^2} = \frac{y^2}{y+1}.
$$

$$
\tilde{N} = \frac{y \cdot x(y+2)}{(y+1)^2} = \frac{xy(y+2)}{(y+1)^2}.
$$

**Step 6.** Verify exactness of $\tilde{M}\,dx + \tilde{N}\,dy = 0$:

$$
\frac{\partial \tilde{M}}{\partial y} = \frac{2y(y+1) - y^2}{(y+1)^2} = \frac{y^2 + 2y}{(y+1)^2} = \frac{y(y+2)}{(y+1)^2}.
$$

$$
\frac{\partial \tilde{N}}{\partial x} = \frac{y(y+2)}{(y+1)^2}.
$$

Confirmed: $\tilde{M}_y = \tilde{N}_x$. ✓

**Step 7.** Find $F$ with $F_x = \tilde{M} = \frac{y^2}{y+1}$:

$$
F(x,y) = \int \frac{y^2}{y+1}\,dx = \frac{x\,y^2}{y+1} + g(y).
$$

**Step 8.** Determine $g(y)$ from $F_y = \tilde{N}$:

$$
F_y = \frac{2xy(y+1) - xy^2}{(y+1)^2} + g'(y) = \frac{xy(y+2)}{(y+1)^2} + g'(y).
$$

Setting $F_y = \tilde{N} = \frac{xy(y+2)}{(y+1)^2}$ gives $g'(y) = 0$, so $g(y) = 0$.

**General solution:**

$$
\frac{xy^2}{y+1} = C.
$$

---

### Example 3.1.E4 — First-Order Linear ODE

**Solve:** $y' + \frac{2}{x}y = x^3$, with $y(1) = 5$.

**Step 1.** Identify $P(x) = 2/x$ and $Q(x) = x^3$.

**Step 2.** Compute the integrating factor:

$$
\mu(x) = e^{\int \frac{2}{x}\,dx} = e^{2\ln|x|} = x^2.
$$

**Step 3.** Multiply the ODE by $\mu = x^2$:

$$
x^2 y' + 2x\,y = x^5.
$$

**Step 4.** Recognize the left side as $\frac{d}{dx}[x^2 y]$:

$$
\frac{d}{dx}[x^2 y] = x^5.
$$

**Step 5.** Integrate both sides:

$$
x^2 y = \int x^5\,dx = \frac{x^6}{6} + C.
$$

**Step 6.** Solve for $y$:

$$
y = \frac{x^4}{6} + \frac{C}{x^2}.
$$

**Step 7.** Apply $y(1) = 5$:

$$
5 = \frac{1}{6} + C \implies C = \frac{29}{6}.
$$

**Final solution:**

$$
y(x) = \frac{x^4}{6} + \frac{29}{6x^2}.
$$

**Verification:** $y' = \frac{4x^3}{6} - \frac{58}{6x^3} = \frac{2x^3}{3} - \frac{29}{3x^3}$. Then $y' + \frac{2}{x}y = \frac{2x^3}{3} - \frac{29}{3x^3} + \frac{2}{x}\left(\frac{x^4}{6} + \frac{29}{6x^2}\right) = \frac{2x^3}{3} - \frac{29}{3x^3} + \frac{x^3}{3} + \frac{29}{3x^3} = x^3$. ✓

---

### Example 3.1.E5 — Separable with Logarithmic Integration

**Solve:** $\frac{dy}{dx} = \frac{y\ln y}{x}$, with $y(1) = e$.

**Step 1.** Separate: $\frac{dy}{y\ln y} = \frac{dx}{x}$.

**Step 2.** For the left side, substitute $u = \ln y$, $du = dy/y$:

$$
\int \frac{dy}{y\ln y} = \int \frac{du}{u} = \ln|u| = \ln|\ln y|.
$$

**Step 3.** Integrate the right side: $\int \frac{dx}{x} = \ln|x| + C_1$.

**Step 4.** Combine:

$$
\ln|\ln y| = \ln|x| + C_1 \implies |\ln y| = e^{C_1}|x| = A|x|,
$$

where $A = e^{C_1} > 0$.

**Step 5.** Apply $y(1) = e$: $\ln(e) = 1$, so $|\ln y| = A|x|$ gives $1 = A \cdot 1$, hence $A = 1$.

**Step 6.** Since $y(1) = e > 1$, we have $\ln y > 0$ near $x = 1$, so $\ln y = x$ (taking positive branch).

**Final solution:**

$$
y = e^x.
$$

**Verification:** $y' = e^x$ and $\frac{y\ln y}{x} = \frac{e^x \cdot x}{x} = e^x$. ✓

---


## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- [3.2 - Second-Order Linear Homogeneous ODEs](3.2---Second-Order-Linear-Homogeneous-ODEs) — extends to higher-order equations
- [3.3 - Nonhomogeneous ODEs & Undetermined Coefficients](3.3---Nonhomogeneous-ODEs-&-Undetermined-Coefficients) — builds on the integrating factor concept
- [3.6 - Laplace Transforms](3.6---Laplace-Transforms) — alternative solution method for linear ODEs
- [1.4 - Integration Techniques](1.4---Integration-Techniques) — prerequisite integration skills (Subject 01)
- [2.6 - Eigenvalues Eigenvectors & Diagonalization](2.6---Eigenvalues-Eigenvectors-&-Diagonalization) — eigenvalues appear in ODE characteristic equations

### External References
- **Jiří Lebl**, *Notes on Diffy Qs*, Ch. 1 — [jirka.org/diffyqs](https://www.jirka.org/diffyqs/)
- **MIT OCW 18.03SC** — Differential Equations, Unit I: First-Order ODEs — [ocw.mit.edu](https://ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011/)
- **William F. Trench**, *Elementary Differential Equations*, Ch. 2 — [digitalcommons.trinity.edu](https://digitalcommons.trinity.edu/mono/9/)
- **3Blue1Brown** — Differential Equations playlist (visual intuition for slope fields and flows)
- **V. I. Arnold**, *Ordinary Differential Equations* (Springer, 1992) — rigorous geometric approach

---



---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — RC Circuit Discharge with Time-Varying Source

A series RC circuit has resistance $R = 2\,\text{k}\Omega$, capacitance $C = 0.5\,\text{mF}$, and is driven by a source $V(t) = 10e^{-t}$ V. The voltage across the capacitor satisfies:

$$
\frac{dv}{dt} + \frac{1}{RC}v = \frac{1}{RC}V(t).
$$

Find $v(t)$ given $v(0) = 0$.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Identify parameters

The time constant is $\tau = RC = 2000 \times 0.0005 = 1$ s. So the ODE becomes:

$$
\frac{dv}{dt} + v = 10e^{-t}.
$$

This is a first-order linear ODE of the form $v' + P(t)v = Q(t)$ with $P(t) = 1$ and $Q(t) = 10e^{-t}$.

#### Step 2: Compute the integrating factor

$$
\mu(t) = e^{\int 1\,dt} = e^{t}.
$$

#### Step 3: Multiply through by $\mu(t) = e^t$

$$
e^t \frac{dv}{dt} + e^t v = 10e^{-t} \cdot e^t = 10.
$$

The left side is the derivative of $e^t v$:

$$
\frac{d}{dt}\left[e^t v\right] = 10.
$$

#### Step 4: Integrate both sides

$$
e^t v = \int 10\,dt = 10t + C.
$$

#### Step 5: Solve for $v(t)$

$$
v(t) = 10t\,e^{-t} + Ce^{-t}.
$$

#### Step 6: Apply initial condition $v(0) = 0$

$$
0 = 10(0)e^{0} + Ce^{0} = C.
$$

So $C = 0$.

**Final Answer:**

$$
v(t) = 10t\,e^{-t} \text{ V}.
$$

**Physical interpretation:** The capacitor voltage rises from zero, reaches a maximum at $t = 1$ s (where $v_{\max} = 10e^{-1} \approx 3.68$ V), then decays to zero as both the source and the stored energy dissipate.

</details>

### Example 8.2 — Mixing Tank with Variable Inflow Concentration

A 200-liter tank initially contains pure water. Brine with concentration $c_{\text{in}}(t) = 3 + \sin(t)$ g/L flows in at 5 L/min. The well-stirred mixture flows out at 5 L/min. Find the amount of salt $A(t)$ in the tank.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Set up the balance equation

Rate in $= c_{\text{in}}(t) \times 5 = 5(3 + \sin t) = 15 + 5\sin t$ g/min.

Rate out $= \frac{A(t)}{200} \times 5 = \frac{A}{40}$ g/min.

The ODE is:

$$
\frac{dA}{dt} = 15 + 5\sin t - \frac{A}{40}.
$$

Rewrite in standard linear form:

$$
\frac{dA}{dt} + \frac{1}{40}A = 15 + 5\sin t.
$$

#### Step 2: Compute the integrating factor

$$
\mu(t) = e^{\int \frac{1}{40}\,dt} = e^{t/40}.
$$

#### Step 3: Multiply through by $e^{t/40}$

$$
\frac{d}{dt}\left[e^{t/40} A\right] = (15 + 5\sin t)\,e^{t/40}.
$$

#### Step 4: Integrate the right side

Split into two integrals:

$$
e^{t/40} A = 15\int e^{t/40}\,dt + 5\int e^{t/40}\sin t\,dt.
$$

**First integral:**

$$
15\int e^{t/40}\,dt = 15 \cdot 40\,e^{t/40} = 600\,e^{t/40}.
$$

**Second integral** (integration by parts twice): We need $\int e^{t/40}\sin t\,dt$. Let $a = 1/40$. Using the standard formula:

$$
\int e^{at}\sin t\,dt = \frac{e^{at}(a\sin t - \cos t)}{a^2 + 1}.
$$

With $a = 1/40$, $a^2 + 1 = 1/1600 + 1 = 1601/1600$:

$$
\int e^{t/40}\sin t\,dt = \frac{e^{t/40}\left(\frac{1}{40}\sin t - \cos t\right)}{\frac{1601}{1600}} = \frac{1600\,e^{t/40}\left(\frac{\sin t}{40} - \cos t\right)}{1601}.
$$

Simplify:

$$
= \frac{e^{t/40}(40\sin t - 1600\cos t)}{1601 \cdot 40} \cdot 1600 = \frac{e^{t/40}(40\sin t - 1600\cos t)}{1601}.
$$

So the second integral contributes:

$$
5 \cdot \frac{e^{t/40}(40\sin t - 1600\cos t)}{1601} = \frac{e^{t/40}(200\sin t - 8000\cos t)}{1601}.
$$

#### Step 5: Combine and solve for $A(t)$

$$
e^{t/40} A = 600\,e^{t/40} + \frac{e^{t/40}(200\sin t - 8000\cos t)}{1601} + C.
$$

Divide by $e^{t/40}$:

$$
A(t) = 600 + \frac{200\sin t - 8000\cos t}{1601} + Ce^{-t/40}.
$$

#### Step 6: Apply $A(0) = 0$ (pure water initially)

$$
0 = 600 + \frac{0 - 8000}{1601} + C = 600 - \frac{8000}{1601} + C.
$$

$$
C = -600 + \frac{8000}{1601} = \frac{-600 \cdot 1601 + 8000}{1601} = \frac{-960600 + 8000}{1601} = \frac{-952600}{1601}.
$$

**Final Answer:**

$$
A(t) = 600 + \frac{200\sin t - 8000\cos t}{1601} - \frac{952600}{1601}\,e^{-t/40} \text{ grams}.
$$

As $t \to \infty$, the transient dies out and $A(t) \to 600 + \frac{200\sin t - 8000\cos t}{1601}$, oscillating around the steady-state value of 600 g (which corresponds to a concentration of 3 g/L matching the average inflow).

</details>

### Example 8.3 — Bernoulli Equation from Population Dynamics

The logistic growth model $\frac{dP}{dt} = rP - kP^2$ (with $r = 2$, $k = 0.01$, $P(0) = 10$) is a Bernoulli equation. Solve it by the substitution $v = P^{1-n}$.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Identify the Bernoulli form

The equation $P' = 2P - 0.01P^2$ can be written as:

$$
P' - 2P = -0.01P^2.
$$

This is Bernoulli with $n = 2$, $P(x) = -2$ (the coefficient of $P$), and $Q(x) = -0.01$.

#### Step 2: Apply the Bernoulli substitution

Let $v = P^{1-n} = P^{-1} = 1/P$. Then:

$$
\frac{dv}{dt} = -P^{-2}\frac{dP}{dt}.
$$

Divide the original ODE by $P^2$:

$$
P^{-2}P' - 2P^{-1} = -0.01.
$$

Since $P^{-2}P' = -v'$:

$$
-v' - 2v = -0.01.
$$

Multiply by $-1$:

$$
v' + 2v = 0.01.
$$

#### Step 3: Solve the resulting linear ODE

Integrating factor: $\mu = e^{2t}$.

$$
\frac{d}{dt}[e^{2t}v] = 0.01\,e^{2t}.
$$

Integrate:

$$
e^{2t}v = 0.01 \cdot \frac{e^{2t}}{2} + C = 0.005\,e^{2t} + C.
$$

$$
v(t) = 0.005 + Ce^{-2t}.
$$

#### Step 4: Back-substitute $v = 1/P$

$$
\frac{1}{P(t)} = 0.005 + Ce^{-2t}.
$$

#### Step 5: Apply $P(0) = 10$

$$
\frac{1}{10} = 0.005 + C \implies C = 0.1 - 0.005 = 0.095.
$$

#### Step 6: Write the final solution

$$
\frac{1}{P(t)} = 0.005 + 0.095\,e^{-2t} = \frac{1 + 19e^{-2t}}{200}.
$$

**Final Answer:**

$$
P(t) = \frac{200}{1 + 19e^{-2t}}.
$$

**Verification:** As $t \to \infty$, $P \to 200 = r/k$, the carrying capacity. At $t = 0$: $P(0) = 200/20 = 10$. ✓

The inflection point (fastest growth) occurs when $P = K/2 = 100$, i.e., when $1 + 19e^{-2t} = 2$, giving $t = \frac{\ln 19}{2} \approx 1.47$.

</details>

---

## 📘 9. Appendix: Extended Derivations & Special Cases

### 9.1 Integrating Factors Depending on $xy$ — The General Theory

The standard integrating factor technique for $M\,dx + N\,dy = 0$ seeks $\mu$ depending on $x$ alone or $y$ alone. But some equations admit integrating factors of the form $\mu = \mu(xy)$, $\mu = \mu(x/y)$, or $\mu = \mu(x^m y^n)$. Here we derive the condition for $\mu = \mu(xy)$.

**Setup.** Suppose $\mu(xy)$ makes $\mu M\,dx + \mu N\,dy = 0$ exact. The exactness condition is:

$$
\frac{\partial}{\partial y}[\mu(xy) M] = \frac{\partial}{\partial x}[\mu(xy) N].
$$

Expanding using the chain rule (let $w = xy$, so $\partial w/\partial y = x$ and $\partial w/\partial x = y$):

$$
\mu'(xy) \cdot x \cdot M + \mu(xy) \cdot M_y = \mu'(xy) \cdot y \cdot N + \mu(xy) \cdot N_x.
$$

Rearranging:

$$
\mu'(xy)[xM - yN] = \mu(xy)[N_x - M_y].
$$

Dividing by $\mu(xy)$:

$$
\frac{\mu'(xy)}{\mu(xy)} = \frac{N_x - M_y}{xM - yN}.
$$

The left side is $\frac{d}{dw}[\ln \mu(w)]$ evaluated at $w = xy$. For this to be a valid ODE in $w = xy$ alone, the right side must be expressible purely as a function of $xy$:

$$
\frac{N_x - M_y}{xM - yN} = h(xy) \quad \text{(must depend only on the product } xy\text{)}.
$$

If this condition holds, then:

$$
\ln \mu = \int h(w)\,dw \implies \mu(xy) = e^{\int h(xy)\,d(xy)}.
$$

**Example application.** Consider $(3xy + y^2)\,dx + (x^2 + xy)\,dy = 0$. Here $M = 3xy + y^2$, $N = x^2 + xy$, $M_y = 3x + 2y$, $N_x = 2x + y$. So $N_x - M_y = (2x+y) - (3x+2y) = -x - y$. And $xM - yN = x(3xy+y^2) - y(x^2+xy) = 3x^2y + xy^2 - x^2y - xy^2 = 2x^2y$. Thus:

$$
\frac{N_x - M_y}{xM - yN} = \frac{-(x+y)}{2x^2 y}.
$$

This does not simplify to a function of $xy$ alone, so $\mu(xy)$ does not work for this particular equation. One must try other forms (e.g., $\mu = x^m y^n$) or verify that $\mu(x)$ or $\mu(y)$ works instead.

**When it does work** (e.g., $(y + xy^2)\,dx + (x + x^2y)\,dy = 0$): $M_y - N_x = (1+2xy) - (1+2xy) = 0$, so this is already exact — no integrating factor needed. A more instructive case: $(2y)\,dx + (3x)\,dy = 0$ with $M_y = 2$, $N_x = 3$, $xM - yN = 2xy - 3xy = -xy$, giving $(N_x - M_y)/(xM - yN) = 1/(-xy) = -1/(xy)$. This is indeed a function of $xy$! Setting $w = xy$: $\mu'/\mu = -1/w$, so $\mu = 1/w = 1/(xy)$. Multiplying: $(2/x)\,dx + (3/y)\,dy = 0$, which integrates to $2\ln|x| + 3\ln|y| = C$.

*Reference: V. I. Arnold, Ordinary Differential Equations (Springer, 1992), §2.7; Lebl's Diffy Qs, §1.6.*

### 9.2 Existence and Uniqueness: The Picard–Lindelöf Theorem

The fundamental question for any IVP $y' = f(t, y)$, $y(t_0) = y_0$ is: does a solution exist, and is it unique? The answer is given by the Picard–Lindelöf theorem (also called the Cauchy–Lipschitz theorem).

**Theorem (Picard–Lindelöf).** Let $f(t, y)$ be continuous on a rectangle $R = \{(t,y) : |t - t_0| \leq a,\, |y - y_0| \leq b\}$ and satisfy a Lipschitz condition in $y$:

$$
|f(t, y_1) - f(t, y_2)| \leq L|y_1 - y_2| \quad \forall (t, y_1), (t, y_2) \in R,
$$

for some constant $L > 0$. Then there exists a unique solution $y(t)$ to the IVP on the interval $|t - t_0| \leq \min(a, b/M)$, where $M = \max_R |f(t,y)|$.

**Proof sketch (Picard iteration).** Define the sequence:

$$
y_0(t) = y_0, \qquad y_{n+1}(t) = y_0 + \int_{t_0}^{t} f(s, y_n(s))\,ds.
$$

One shows:
1. Each $y_n$ is well-defined and continuous on $|t - t_0| \leq \alpha = \min(a, b/M)$.
2. The differences $|y_{n+1}(t) - y_n(t)| \leq \frac{ML^n|t-t_0|^{n+1}}{(n+1)!}$ (proved by induction using the Lipschitz condition).
3. The series $y_0 + \sum_{n=0}^{\infty}(y_{n+1} - y_n)$ converges uniformly by comparison with $e^{L|t-t_0|}$ (the Weierstrass M-test).
4. The limit $y(t) = \lim_{n\to\infty} y_n(t)$ satisfies the integral equation $y(t) = y_0 + \int_{t_0}^t f(s, y(s))\,ds$, hence the ODE.
5. Uniqueness follows from Gronwall's inequality: if $y$ and $z$ are two solutions, then $|y(t) - z(t)| \leq L\int_{t_0}^t |y(s) - z(s)|\,ds$, which by Gronwall gives $|y - z| \equiv 0$.

**Why this matters for first-order ODEs.** The theorem guarantees that separable, exact, and linear equations (where $f$ and $\partial f/\partial y$ are continuous) have unique solutions through every point in their domain. It also explains why solutions can fail to be unique at points where the Lipschitz condition breaks down — for example, $y' = \sqrt{|y|}$ at $y = 0$ (where $\partial f/\partial y = 1/(2\sqrt{|y|}) \to \infty$) admits both $y \equiv 0$ and $y = (t/2)^2$ as solutions through the origin.

**Practical criterion.** If $\partial f/\partial y$ exists and is continuous on $R$, then $f$ is automatically Lipschitz in $y$ on $R$ (with $L = \max_R |\partial f/\partial y|$). So for most textbook problems, checking continuity of $f$ and $f_y$ suffices.

*Reference: Jiří Lebl, Notes on Diffy Qs, §1.2; MIT OCW 18.03, Lecture 1 supplementary notes.*

---
