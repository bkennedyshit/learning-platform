---
title: "Single Variable Differentiation"
subject: "Mathematical Foundations & Calculus"
catalog: advanced
audience_tier: higher-education
chapter: "1.2"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

 
*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

![Single-Variable_Differentiation_Infographic](Single-Variable_Differentiation_Infographic.png)

# 1.2 — Single-Variable Differentiation

> *"To every action there is always opposed an equal reaction."* — Newton, *Principia*. Differentiation is the mathematical machinery that lets us compute that reaction in the first place: instantaneous rate of change, the slope of motion, the kinematic spine of every physical theory you'll ever care about.

Chapter 1.1 taught you how to make sense of a limit. This chapter asks one specific question of every function in sight: *how fast is it changing right here, right now?* The answer is the **derivative** — and once you have it, virtually every quantitative question in physics, engineering, optimization, machine learning, and economics either is a derivative, contains a derivative, or is an integral of a derivative.

We will build the derivative from the limit definition (twice — both flavors), prove every standard differentiation rule, develop the four cornerstone theorems (Fermat, Rolle, MVT, Taylor), and grind through a deliberate ladder of worked examples and challenge problems.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. State and apply both forms of the derivative as a limit, $\lim_{h\to 0}\frac{f(a+h)-f(a)}{h}$ and $\lim_{x\to a}\frac{f(x)-f(a)}{x-a}$.
2. Prove **differentiability $\Rightarrow$ continuity** and produce the canonical counterexample for the converse.
3. Prove the **product, quotient, and chain rules** by direct $\varepsilon$–$\delta$ / limit manipulation.
4. Derive $\frac{d}{dx}\sin x = \cos x$ from the cornerstone limit $\sin\theta/\theta \to 1$ inherited from Chapter 1.1.
5. Apply implicit and logarithmic differentiation to functions like $x^x$ and $x^2 + y^2 = r^2$.
6. State and use **Fermat's, Rolle's, the Mean Value Theorem, L'Hôpital's Rule, and Taylor's Theorem** with the Lagrange remainder.
7. Compute Taylor polynomials and bound their error.
8. Solve canonical optimization, related-rates, and Newton's-method problems.
9. Recognize and unfreeze the seven indeterminate forms (four base + three exponential) using L'Hôpital and the $\exp(g\ln f)$ trick.

---


## 🤔 Why the fuck does this matter?

A short blunt rant before we dive in. Every physical law you'll meet for the rest of your life is differential in nature:

- **Newtonian mechanics**: $F = m\ddot{x}$ — second derivative of position w.r.t. time.
- **Heat flow**: $\partial_t u = \alpha\,\partial_x^2 u$ — derivatives in space and time.
- **Maxwell's equations**: $\nabla \times \mathbf{E} = -\partial_t\mathbf{B}$ — curl is just a packaged set of partial derivatives.
- **Schrödinger's equation**: $i\hbar\,\partial_t\Psi = \hat{H}\Psi$ — derivative again.
- **Backpropagation in a neural network**: gradient descent on a loss function. Pure derivatives, top to bottom.

If you can't differentiate confidently, none of the higher-level subjects in this vault will land. So we're going to build this from the limit up, prove every rule, and then practice until the algebra becomes a reflex. No skipped steps. No "by inspection." We do the work.

---

## 🖼️ Visual Anchor — Secant Lines Become a Tangent

The single canonical picture: take a curve $y = f(x)$, pick a point $(a, f(a))$, and draw secants to nearby points $(a+h, f(a+h))$. As $h \to 0$, the secant slopes converge to the slope of the **tangent line**, and that limiting slope is the **derivative** $f'(a)$.

![math-01__1.2-fig1](math-01__1.2-fig1.svg)

The orange curve is $f$. The three dashed grey lines are secants from $P=(a,f(a))$ to nearby points; as the second point slides toward $P$, the secant pivots around $P$ and limits to the gold **tangent line** whose slope is $f'(a)$. The derivative *is* that limiting slope.

---


## 📚 1. Definitions

### Definition 1.2.1 — The Derivative (Limit Form, "h-form")

Let $f$ be defined on an open interval containing $a$. The **derivative of $f$ at $a$** is

$$
f'(a) \;=\; \lim_{h \to 0} \frac{f(a + h) - f(a)}{h},
$$

provided the limit exists (in the sense of [Definition 1.1.2](1.1---Limits-&-Continuity)). We say $f$ is **differentiable at $a$** when this limit exists and is finite. The numerator $f(a+h) - f(a)$ is the **rise**, the denominator $h$ is the **run**, and their quotient is the **slope of the secant** from $(a, f(a))$ to $(a+h, f(a+h))$.

### Definition 1.2.2 — The Derivative ("x-form" / Newton Quotient)

Equivalently, with the substitution $x = a + h$ (so $h = x - a$ and $h \to 0 \Leftrightarrow x \to a$):

$$
f'(a) \;=\; \lim_{x \to a} \frac{f(x) - f(a)}{x - a}.
$$

The two forms are algebraically identical; pick whichever is convenient for the problem at hand. The h-form is usually cleaner for general manipulation; the x-form is often cleaner for proving limits in piecewise or factored situations.

### Definition 1.2.3 — One-Sided Derivatives

The **right-hand derivative** at $a$ is

$$
f'_+(a) = \lim_{h \to 0^+} \frac{f(a+h) - f(a)}{h},
$$

and the **left-hand derivative** is

$$
f'_-(a) = \lim_{h \to 0^-} \frac{f(a+h) - f(a)}{h}.
$$

$f$ is differentiable at $a$ iff both one-sided derivatives exist *and are equal*. (Direct corollary of the two-sided $\Leftrightarrow$ one-sided agreement theorem from §1.1.)

### Definition 1.2.4 — The Derivative as a Function

When $f$ is differentiable at every point of an open set $U$, the function $f' : U \to \mathbb{R}$ defined by $x \mapsto f'(x)$ is itself a function. We use any of the following notations interchangeably:

$$
f'(x) \;\equiv\; \frac{df}{dx} \;\equiv\; \frac{d}{dx}f(x) \;\equiv\; D_x f \;\equiv\; \dot{f}(x) \;\text{(physics, } x \text{ a time variable)}.
$$

### Definition 1.2.5 — Higher-Order Derivatives

Recursively, $f^{(0)} = f$ and $f^{(n+1)} = (f^{(n)})'$ wherever the right-hand side exists. Specific names:

| Order | Notation | Physical meaning (with $f = $ position) |
|---|---|---|
| 1 | $f'$, $df/dx$ | velocity |
| 2 | $f''$, $d^2 f/dx^2$ | acceleration |
| 3 | $f'''$, $d^3 f/dx^3$ | jerk |
| 4 | $f^{(4)}$ | snap (a.k.a. jounce) |

### Definition 1.2.6 — Smoothness Classes

A function $f$ is **of class $C^k$ on $U$** (written $f \in C^k(U)$) if $f^{(0)}, f^{(1)}, \dots, f^{(k)}$ all exist and are continuous on $U$. The intersection $C^\infty(U) = \bigcap_{k \geq 0} C^k(U)$ is the class of **smooth** functions: those with continuous derivatives of every order. Polynomials, $\sin, \cos, e^x$ are all in $C^\infty(\mathbb{R})$. **Analytic** functions are stricter: they additionally must equal their Taylor series in a neighborhood of every point. Every analytic function is smooth, but the reverse fails — see Example E5 below for the canonical counterexample.

### Definition 1.2.7 — The Differential

Once $f'(a)$ exists, the **differential** of $f$ at $a$ is the linear function

$$
df_a : \mathbb{R} \to \mathbb{R}, \qquad df_a(\Delta x) = f'(a)\,\Delta x.
$$

In Leibniz's notation $dy = f'(a)\,dx$, where $dx$ and $dy$ are *linear infinitesimal increments along the tangent line*, **not** literal infinitesimal numbers. The notation is convenient and physically suggestive but should be read as syntax for a linear map, not as a magical small quantity. (More on this pitfall in §11.)

### Definition 1.2.8 — Critical Point

A point $c \in \operatorname{dom} f$ is a **critical point** of $f$ if either $f'(c) = 0$ or $f'(c)$ does not exist. Local extrema in the interior of an interval can occur **only** at critical points (Fermat's Theorem, §4).

---


## 📐 2. Axioms / Postulates

Differentiation inherits its underlying machinery from Chapter 1.1. The axioms we use here are the same:

### Axiom 1.2.A — Completeness of $\mathbb{R}$ (Carried Forward from 1.1.A)

Every non-empty subset of $\mathbb{R}$ that is bounded above admits a supremum in $\mathbb{R}$. We invoke this directly in the proof of the **Extreme Value Theorem** (which Fermat's Theorem in §4 silently quotes) and in **Rolle's Theorem**.

### Axiom 1.2.B — Archimedean Property (1.1.B)

For every $x > 0$, there exists $n \in \mathbb{N}$ with $1/n < x$. This is the structural fact that makes $h \to 0$ meaningful: we can always squeeze $h$ smaller than any prescribed positive number.

### Postulate 1.2.C — Limit Existence is the Definitional Floor

We accept Definition 1.1.2 (the formal $\varepsilon$–$\delta$ limit) as the foundation. Every theorem in this chapter that opens with "*if $f$ is differentiable*…" is implicitly assuming the existence of a specific limit, and every $\varepsilon$–$\delta$ trick from Chapter 1.1 (algebra of limits, squeeze, composition continuity) is fair game.

These three axioms / postulates carry the rest of the chapter on their backs.

---

## 🛡️ 3. Lemmas (Differentiation Rules)

Throughout this section assume $f$ and $g$ are differentiable at $a$, and let $c \in \mathbb{R}$ be a constant. Each lemma is stated cleanly here; the full proofs appear in §5.

### Lemma 1.2.1 — Constant Rule

If $f(x) = c$ for all $x$, then $f'(x) = 0$.

### Lemma 1.2.2 — Power Rule

For any $n \in \mathbb{Z}$ (and indeed any $n \in \mathbb{R}$ with appropriate domain restrictions):

$$
\frac{d}{dx}\,x^n = n\,x^{n-1}.
$$

(Proved for $n \in \mathbb{N}$ in §5.2 by binomial expansion. The integer-negative case follows from the quotient rule, the rational case from implicit differentiation, and the real case from logarithmic differentiation. We close every loop in §5.2 and §6.)

### Lemma 1.2.3 — Sum / Difference Rule

$(f \pm g)'(a) = f'(a) \pm g'(a)$.

### Lemma 1.2.4 — Constant-Multiple Rule

$(c f)'(a) = c\,f'(a)$.

### Lemma 1.2.5 — Product Rule (Leibniz Rule)

$$
(fg)'(a) = f'(a)\,g(a) + f(a)\,g'(a).
$$

### Lemma 1.2.6 — Quotient Rule

If $g(a) \neq 0$:

$$
\left(\frac{f}{g}\right)'(a) = \frac{f'(a)\,g(a) - f(a)\,g'(a)}{[g(a)]^2}.
$$

### Lemma 1.2.7 — Chain Rule

If $g$ is differentiable at $a$ and $f$ is differentiable at $g(a)$:

$$
(f \circ g)'(a) = f'(g(a)) \cdot g'(a).
$$

### Lemma 1.2.8 — Trigonometric Derivatives

| Function | Derivative |
|---|---|
| $\sin x$ | $\cos x$ |
| $\cos x$ | $-\sin x$ |
| $\tan x$ | $\sec^2 x$ |
| $\sec x$ | $\sec x \tan x$ |
| $\csc x$ | $-\csc x \cot x$ |
| $\cot x$ | $-\csc^2 x$ |

The first one is proved from the cornerstone limit $\sin\theta/\theta \to 1$ in §5.4; the rest follow from quotient/product rules applied to ratios of $\sin$ and $\cos$.

### Lemma 1.2.9 — Exponential and Logarithm

$$
\frac{d}{dx}\,e^x = e^x, \qquad \frac{d}{dx}\,\ln x = \frac{1}{x} \;(x > 0), \qquad \frac{d}{dx}\,a^x = a^x \ln a, \qquad \frac{d}{dx}\,\log_a x = \frac{1}{x \ln a}.
$$

### Lemma 1.2.10 — Inverse Function Theorem (Single-Variable)

If $f$ is differentiable on an open interval, $f'(a) \neq 0$, and $f$ is invertible in a neighborhood of $a$, then $f^{-1}$ is differentiable at $b = f(a)$ with

$$
(f^{-1})'(b) = \frac{1}{f'(a)} = \frac{1}{f'(f^{-1}(b))}.
$$

### Lemma 1.2.11 — Inverse Trigonometric Derivatives

| Function | Derivative |
|---|---|
| $\arcsin x$ | $1/\sqrt{1 - x^2}$ |
| $\arccos x$ | $-1/\sqrt{1 - x^2}$ |
| $\arctan x$ | $1/(1 + x^2)$ |
| $\operatorname{arccot} x$ | $-1/(1 + x^2)$ |
| $\operatorname{arcsec} x$ | $1/(\lvert x\rvert\sqrt{x^2 - 1})$ |
| $\operatorname{arccsc} x$ | $-1/(\lvert x\rvert\sqrt{x^2 - 1})$ |

Each follows from the Inverse Function Theorem combined with a Pythagorean identity. We work out $\arcsin$ in §6.

---


## 👑 4. Major Theorems

### Theorem 1.2.1 — Differentiability Implies Continuity

If $f$ is differentiable at $a$, then $f$ is continuous at $a$.

**Caveat (the converse fails).** Continuity does *not* imply differentiability. The standard counterexample is $f(x) = |x|$, which is continuous everywhere but has $f'_+(0) = 1$ and $f'_-(0) = -1$, so $f'(0)$ does not exist. (Proved in §5.1.)

### Theorem 1.2.2 — Fermat's Theorem (Interior Extrema $\Rightarrow$ $f' = 0$)

If $f$ has a local extremum (maximum or minimum) at an interior point $c$ of its domain, *and $f$ is differentiable at $c$*, then $f'(c) = 0$.

This is one direction only. $f'(c) = 0$ does *not* guarantee a local extremum (e.g., $f(x) = x^3$ has $f'(0) = 0$ but $0$ is neither a max nor min — it's an inflection point).

### Theorem 1.2.3 — Rolle's Theorem

Let $f$ be:

1. continuous on $[a, b]$,
2. differentiable on $(a, b)$,
3. and satisfy $f(a) = f(b)$.

Then there exists $c \in (a, b)$ with $f'(c) = 0$.

### Theorem 1.2.4 — Mean Value Theorem (MVT, Lagrange's Form)

Let $f$ be continuous on $[a, b]$ and differentiable on $(a, b)$. Then there exists $c \in (a, b)$ such that

$$
f'(c) = \frac{f(b) - f(a)}{b - a}.
$$

Geometrically: somewhere strictly between $a$ and $b$, the tangent to the curve is parallel to the secant from $(a, f(a))$ to $(b, f(b))$.

### Theorem 1.2.5 — Cauchy Mean Value Theorem (Generalized MVT)

Let $f, g$ be continuous on $[a, b]$ and differentiable on $(a, b)$. Then there exists $c \in (a, b)$ with

$$
[f(b) - f(a)]\,g'(c) \;=\; [g(b) - g(a)]\,f'(c).
$$

If additionally $g'(x) \neq 0$ on $(a, b)$ (which forces $g(b) \neq g(a)$ by Rolle), this can be rearranged as

$$
\frac{f(b) - f(a)}{g(b) - g(a)} = \frac{f'(c)}{g'(c)}.
$$

This is the lemma that makes L'Hôpital's Rule work.

### Theorem 1.2.6 — L'Hôpital's Rule (0/0 form)

Let $f, g$ be differentiable on an open interval $(a, b)$, with $g'(x) \neq 0$ there. If

$$
\lim_{x \to a^+} f(x) = \lim_{x \to a^+} g(x) = 0
\quad \text{and} \quad
\lim_{x \to a^+} \frac{f'(x)}{g'(x)} = L \in \mathbb{R} \cup \{\pm\infty\},
$$

then

$$
\lim_{x \to a^+} \frac{f(x)}{g(x)} = L.
$$

Identical statements hold for $x \to a^-$, $x \to a$ (two-sided), $x \to \infty$, $x \to -\infty$, and for the $\infty/\infty$ form (where the assumption $f, g \to 0$ is replaced by $|f|, |g| \to \infty$).

### Theorem 1.2.7 — Taylor's Theorem (Lagrange Remainder)

Let $n \geq 0$, let $f \in C^n([a, b])$, and assume $f^{(n+1)}$ exists on $(a, b)$. For each $x \in (a, b]$ there exists $\xi$ strictly between $a$ and $x$ such that

$$
f(x) = \underbrace{\sum_{k=0}^{n} \frac{f^{(k)}(a)}{k!}\,(x - a)^k}_{\text{Taylor polynomial } T_n(x;a)} \;+\; \underbrace{\frac{f^{(n+1)}(\xi)}{(n+1)!}\,(x - a)^{n+1}}_{\text{Lagrange remainder } R_n(x;a)}.
$$

The remainder bounds the error of approximating $f$ by its degree-$n$ Taylor polynomial centered at $a$.

### Theorem 1.2.8 — Increasing/Decreasing Test (a.k.a. Monotonicity Theorem)

Let $f$ be continuous on $[a, b]$ and differentiable on $(a, b)$.

- If $f'(x) > 0$ for all $x \in (a, b)$, then $f$ is strictly increasing on $[a, b]$.
- If $f'(x) < 0$ for all $x \in (a, b)$, then $f$ is strictly decreasing on $[a, b]$.
- If $f'(x) = 0$ for all $x \in (a, b)$, then $f$ is constant on $[a, b]$.

This is a direct consequence of MVT applied between any two points $x_1 < x_2$ in the interval.

---


## ✍️ 5. Proofs / Derivations

### 5.1 Proof of Differentiability $\Rightarrow$ Continuity (Theorem 1.2.1)

**Claim.** If $f$ is differentiable at $a$, then $\lim_{x \to a} f(x) = f(a)$.

**Setup.** For $x \neq a$ in $\operatorname{dom} f$, write the algebraic identity

$$
f(x) - f(a) = \frac{f(x) - f(a)}{x - a} \cdot (x - a).
$$

This is just multiply-and-divide by $(x - a)$, valid because $x \neq a$.

**Take the limit on both sides as $x \to a$.** Apply the [product limit law (L6)](1.1---Limits-&-Continuity#3-lemmas-limit-laws):

$$
\lim_{x \to a} \big[f(x) - f(a)\big] \;=\; \left[\lim_{x \to a} \frac{f(x) - f(a)}{x - a}\right] \cdot \left[\lim_{x \to a} (x - a)\right].
$$

The first factor is $f'(a)$ by Definition 1.2.2 (and *exists* because $f$ is differentiable at $a$ — this is the only place we use the hypothesis). The second factor is $0$ because $x - a$ is a polynomial, hence continuous at $a$ with value $0$.

**Multiply.** Any finite real number times $0$ is $0$:

$$
\lim_{x \to a} [f(x) - f(a)] = f'(a) \cdot 0 = 0.
$$

**Conclude.** Since $f(a)$ is a constant, $\lim_{x \to a} f(a) = f(a)$. By the Sum Limit Law (L3):

$$
\lim_{x \to a} f(x) = \lim_{x \to a} \big[(f(x) - f(a)) + f(a)\big] = 0 + f(a) = f(a).
$$

That is exactly the third clause of [Definition 1.1.5](1.1---Limits-&-Continuity#1-definitions) for continuity at $a$, plus the trivially-met clauses 1 and 2 (the limit exists and $f(a)$ is defined). $\blacksquare$

**Counterexample for the converse (canonical).** $f(x) = |x|$ is continuous on $\mathbb{R}$ (a standard $\varepsilon$–$\delta$ proof: take $\delta = \varepsilon$). But:

$$
f'_+(0) = \lim_{h \to 0^+} \frac{|h| - |0|}{h} = \lim_{h \to 0^+} \frac{h}{h} = 1,
$$

$$
f'_-(0) = \lim_{h \to 0^-} \frac{|h| - |0|}{h} = \lim_{h \to 0^-} \frac{-h}{h} = -1.
$$

The two one-sided derivatives disagree; by Definition 1.2.3, $f'(0)$ does not exist. So continuity is strictly weaker than differentiability.

---

### 5.2 Proof of the Power Rule for $n \in \mathbb{N}$ (Lemma 1.2.2)

**Claim.** For $n \in \mathbb{N}$, $\frac{d}{dx}\,x^n = n\,x^{n-1}$.

**Proof via the binomial theorem.** Apply Definition 1.2.1 to $f(x) = x^n$:

$$
f'(x) = \lim_{h \to 0} \frac{(x + h)^n - x^n}{h}.
$$

Expand $(x + h)^n$ using the binomial theorem:

$$
(x + h)^n = \sum_{k=0}^{n} \binom{n}{k} x^{n-k} h^k = x^n + n\,x^{n-1}\,h + \binom{n}{2} x^{n-2} h^2 + \cdots + h^n.
$$

Subtract $x^n$ from both sides:

$$
(x + h)^n - x^n = n\,x^{n-1}\,h + \binom{n}{2} x^{n-2} h^2 + \cdots + h^n.
$$

Every term on the right has at least one factor of $h$, so we can divide by $h$ (valid because the limit's quantification is $h \neq 0$):

$$
\frac{(x + h)^n - x^n}{h} = n\,x^{n-1} + \binom{n}{2} x^{n-2}\, h + \binom{n}{3} x^{n-3}\, h^2 + \cdots + h^{n-1}.
$$

Now take the limit as $h \to 0$. Every term except the first contains at least one factor of $h$, so each of those terms is a polynomial in $h$ with no constant term — they all vanish as $h \to 0$:

$$
f'(x) = n\,x^{n-1} + 0 + 0 + \cdots + 0 = n\,x^{n-1}. \qquad \blacksquare
$$

**Extending to negative integers.** For $n < 0$ write $x^n = 1/x^{|n|}$ and apply the quotient rule (Lemma 1.2.6) once we prove it. Result: $\frac{d}{dx} x^{-m} = -m\,x^{-m-1}$. (See Worked Example E1 below.)

**Extending to rationals and reals.** For $n = p/q$ with $q$ odd, write $y = x^{p/q}$, raise both sides to the $q$ and use implicit differentiation (§6 / Example E2). For arbitrary real $n$, use logarithmic differentiation: $\ln(x^n) = n \ln x$, differentiate, recover. The identity $\frac{d}{dx}x^n = n x^{n-1}$ holds for any real $n$ on the domain where $x^n$ is defined.

---

### 5.3 Proof of the Product Rule (Lemma 1.2.5)

**Claim.** $(fg)'(a) = f'(a)\,g(a) + f(a)\,g'(a)$.

**Strategy.** The "add and subtract a clever zero" trick — exactly the same pattern as the proof of the [Limit Sum Law](1.1---Limits-&-Continuity#5-2-proof-of-limit-law-l3-sum-law) but multiplicative.

**Set up the difference quotient.** By Definition 1.2.1 applied to the product $fg$:

$$
(fg)'(a) = \lim_{h \to 0} \frac{(fg)(a + h) - (fg)(a)}{h} = \lim_{h \to 0} \frac{f(a+h)\,g(a+h) - f(a)\,g(a)}{h}.
$$

**The clever zero.** Add and subtract $f(a+h)\,g(a)$ in the numerator:

$$
f(a+h)\,g(a+h) - f(a)\,g(a) = \big[f(a+h)\,g(a+h) - f(a+h)\,g(a)\big] + \big[f(a+h)\,g(a) - f(a)\,g(a)\big].
$$

Factor each bracket:

$$
= f(a+h)\,\big[g(a+h) - g(a)\big] + g(a)\,\big[f(a+h) - f(a)\big].
$$

**Divide by $h$:**

$$
\frac{(fg)(a+h) - (fg)(a)}{h} = f(a+h) \cdot \frac{g(a+h) - g(a)}{h} + g(a) \cdot \frac{f(a+h) - f(a)}{h}.
$$

**Take the limit $h \to 0$.** Apply the Sum Law and Product Law (L3, L6) from §1.1. Note three pieces:

1. $\displaystyle\lim_{h \to 0} f(a + h) = f(a)$ — because $f$ is differentiable at $a$, hence continuous at $a$ by Theorem 1.2.1. **This is the precise spot where we use the differentiability $\Rightarrow$ continuity result.**
2. $\displaystyle\lim_{h \to 0} \frac{g(a+h) - g(a)}{h} = g'(a)$ — by Definition 1.2.1 for $g$.
3. $\displaystyle\lim_{h \to 0} \frac{f(a+h) - f(a)}{h} = f'(a)$ — by Definition 1.2.1 for $f$.
4. $g(a)$ is a constant, so its limit is itself.

Multiply and add:

$$
(fg)'(a) = f(a) \cdot g'(a) + g(a) \cdot f'(a) = f'(a)\,g(a) + f(a)\,g'(a). \qquad \blacksquare
$$

**Common student error.** People expect $(fg)' = f' g'$. That's wrong — see why? You cannot pull out a $1/h$ across a *product* of two changes; you have to bridge with one factor changing while the other is held momentarily fixed. The clever zero is that bridge.

---


### 5.4 Proof of the Quotient Rule (Lemma 1.2.6) via Product Rule

**Claim.** If $g(a) \neq 0$, $\displaystyle\left(\frac{f}{g}\right)'(a) = \frac{f'(a)\,g(a) - f(a)\,g'(a)}{[g(a)]^2}$.

**Step 1 — Reciprocal rule first.** Compute $\frac{d}{dx}\left[\frac{1}{g(x)}\right]$ at $a$, using Definition 1.2.1:

$$
\left(\frac{1}{g}\right)'(a) = \lim_{h \to 0} \frac{1}{h}\left[\frac{1}{g(a+h)} - \frac{1}{g(a)}\right] = \lim_{h \to 0} \frac{1}{h} \cdot \frac{g(a) - g(a+h)}{g(a+h)\,g(a)}.
$$

Pull out the negative sign:

$$
= \lim_{h \to 0} \left[-\frac{g(a+h) - g(a)}{h}\right] \cdot \frac{1}{g(a+h)\,g(a)}.
$$

The first factor tends to $-g'(a)$. The second factor tends to $\frac{1}{g(a) \cdot g(a)} = \frac{1}{[g(a)]^2}$ (using continuity of $g$ at $a$, Theorem 1.2.1). Hence

$$
\left(\frac{1}{g}\right)'(a) = -\frac{g'(a)}{[g(a)]^2}.
$$

**Step 2 — Apply the product rule.** Write $f/g = f \cdot (1/g)$. The product rule (Lemma 1.2.5) gives

$$
\left(\frac{f}{g}\right)'(a) = f'(a) \cdot \frac{1}{g(a)} + f(a) \cdot \left(-\frac{g'(a)}{[g(a)]^2}\right).
$$

**Step 3 — Common denominator.** Multiply the first term's numerator and denominator by $g(a)$ to give them a common denominator $[g(a)]^2$:

$$
= \frac{f'(a)\,g(a)}{[g(a)]^2} - \frac{f(a)\,g'(a)}{[g(a)]^2} = \frac{f'(a)\,g(a) - f(a)\,g'(a)}{[g(a)]^2}. \qquad \blacksquare
$$

---

### 5.5 Proof of the Chain Rule (Lemma 1.2.7)

**Claim.** If $g$ is differentiable at $a$ and $f$ is differentiable at $b := g(a)$, then $f \circ g$ is differentiable at $a$ and $(f \circ g)'(a) = f'(g(a))\,g'(a)$.

**The naive proof and its bug.** It is *tempting* to write

$$
\frac{f(g(a+h)) - f(g(a))}{h} = \frac{f(g(a+h)) - f(g(a))}{g(a+h) - g(a)} \cdot \frac{g(a+h) - g(a)}{h}
$$

and take the limit. The right-hand denominator $g(a+h) - g(a)$ may be **zero** for $h$ arbitrarily close to $0$ (e.g., constant $g$ on a neighborhood, or oscillating $g$). Division by zero is undefined; the manipulation is *not generally valid*. We need a fix.

**Fix: Carathéodory's bridging function.** Define a helper function $\varphi$ by

$$
\varphi(y) = \begin{cases} \dfrac{f(y) - f(b)}{y - b}, & y \neq b \\[6pt] f'(b), & y = b. \end{cases}
$$

By Definition 1.2.2 applied to $f$ at $b$, $\lim_{y \to b} \varphi(y) = f'(b) = \varphi(b)$. So **$\varphi$ is continuous at $b$.** By construction we also have, for *every* $y$ in the domain (including $y = b$, where both sides are $0$):

$$
f(y) - f(b) = \varphi(y) \cdot (y - b). \tag{$\star$}
$$

(Plug in $y = b$: LHS $= 0$, RHS $= f'(b) \cdot 0 = 0$. ✓ For $y \neq b$, multiply both sides of the definition by $y - b$.)

**Apply ($\star$) with $y = g(a + h)$ and $b = g(a)$:**

$$
f(g(a + h)) - f(g(a)) = \varphi(g(a + h)) \cdot \big[g(a + h) - g(a)\big].
$$

This identity is valid for **every** $h$ in a neighborhood of $0$, including those $h$ where $g(a+h) = g(a)$ — in which case both sides are $0$. Crisis averted.

**Divide by $h$:**

$$
\frac{f(g(a+h)) - f(g(a))}{h} = \varphi(g(a + h)) \cdot \frac{g(a + h) - g(a)}{h}.
$$

**Take the limit as $h \to 0$.** Two pieces:

1. The factor $\dfrac{g(a+h) - g(a)}{h} \to g'(a)$, by Definition 1.2.1 for $g$.
2. The factor $\varphi(g(a + h)) \to \varphi(g(a)) = \varphi(b) = f'(b) = f'(g(a))$. Why? Because $g$ is differentiable at $a$, hence continuous at $a$ (Theorem 1.2.1), so $g(a + h) \to g(a) = b$ as $h \to 0$. And $\varphi$ is continuous at $b$ as shown. Use the [composition limit law (L10)](1.1---Limits-&-Continuity#3-lemmas-limit-laws).

By the Product Limit Law:

$$
(f \circ g)'(a) = \lim_{h \to 0} \frac{f(g(a+h)) - f(g(a))}{h} = f'(g(a)) \cdot g'(a). \qquad \blacksquare
$$

**Why the bridging function works.** Identity ($\star$) packages the "almost-Newton-quotient" into a single continuous object, sidestepping the division-by-zero hazard. This is the **Carathéodory characterization of the derivative** and it generalizes cleanly to multivariable and Banach-space settings.

---

### 5.6 Proof that $\frac{d}{dx}\sin x = \cos x$

**Claim.** $\frac{d}{dx}\sin x = \cos x$ for all $x \in \mathbb{R}$.

**Step 1 — Apply the definition.**

$$
\frac{d}{dx}\sin x = \lim_{h \to 0} \frac{\sin(x + h) - \sin x}{h}.
$$

**Step 2 — Sum-of-angles identity.** Use $\sin(A + B) = \sin A \cos B + \cos A \sin B$ with $A = x$, $B = h$:

$$
\sin(x + h) = \sin x \cos h + \cos x \sin h.
$$

Substitute:

$$
\frac{\sin(x + h) - \sin x}{h} = \frac{\sin x \cos h + \cos x \sin h - \sin x}{h} = \frac{\sin x (\cos h - 1) + \cos x \sin h}{h}.
$$

**Step 3 — Split the fraction.** Distribute the denominator:

$$
= \sin x \cdot \frac{\cos h - 1}{h} + \cos x \cdot \frac{\sin h}{h}.
$$

**Step 4 — Two cornerstone limits.** Both come from Chapter 1.1:

(a) [$\displaystyle\lim_{h \to 0} \frac{\sin h}{h} = 1$](1.1---Limits-&-Continuity#example-1-1-e4-the-trigonometric-cornerstone) (proved in §1.1 by squeezing with the unit circle).

(b) $\displaystyle\lim_{h \to 0} \frac{\cos h - 1}{h} = 0$. Derivation: multiply by the conjugate:

$$
\frac{\cos h - 1}{h} \cdot \frac{\cos h + 1}{\cos h + 1} = \frac{\cos^2 h - 1}{h(\cos h + 1)} = \frac{-\sin^2 h}{h(\cos h + 1)}.
$$

Split:

$$
= -\frac{\sin h}{h} \cdot \frac{\sin h}{\cos h + 1}.
$$

As $h \to 0$: the first factor $\to 1$ (cornerstone limit), the second factor $\to \frac{0}{1 + 1} = 0$. Product law gives $\to -1 \cdot 0 = 0$. ✓

**Step 5 — Plug both limits in.** Use the Sum and Product Limit Laws:

$$
\frac{d}{dx}\sin x = \sin x \cdot 0 + \cos x \cdot 1 = \cos x. \qquad \blacksquare
$$

**Cosine.** By symmetry (or by chain rule with $\cos x = \sin(\pi/2 - x)$):

$$
\frac{d}{dx}\cos x = -\sin x.
$$

---

### 5.7 Proof of the Derivative of $\ln x$ via Inverse Function Theorem

**Claim.** $\frac{d}{dx}\ln x = \frac{1}{x}$ for $x > 0$.

We use the Inverse Function Theorem (Lemma 1.2.10) along with the *defining* property of the exponential: $\frac{d}{dx}e^x = e^x$ (which we'll derive in §5.8).

**Setup.** Let $y = \ln x$. Then $x = e^y$. Treat $\ln$ as the inverse function of $\exp$ on $(0, \infty) \to \mathbb{R}$.

**Apply the Inverse Function Theorem.** With $f = \exp$, $f^{-1} = \ln$, $f'(y) = e^y \neq 0$ for all $y$:

$$
(\ln)'(x) = \frac{1}{f'(f^{-1}(x))} = \frac{1}{e^{\ln x}} = \frac{1}{x}. \qquad \blacksquare
$$

**Alternative proof via the limit definition.** Use the limit-defining property $e = \lim_{n \to \infty}(1 + 1/n)^n$, which generalizes to $\lim_{u \to 0}(1 + u)^{1/u} = e$. Then:

$$
\frac{d}{dx}\ln x = \lim_{h \to 0} \frac{\ln(x + h) - \ln x}{h} = \lim_{h \to 0} \frac{1}{h} \ln\left(\frac{x + h}{x}\right) = \lim_{h \to 0} \frac{1}{h} \ln\left(1 + \frac{h}{x}\right).
$$

Substitute $u = h/x$, so $h = u x$ and $1/h = 1/(u x)$, and $h \to 0 \Leftrightarrow u \to 0$:

$$
= \lim_{u \to 0} \frac{1}{u x} \ln(1 + u) = \frac{1}{x} \cdot \lim_{u \to 0} \ln\big[(1 + u)^{1/u}\big] = \frac{1}{x} \cdot \ln e = \frac{1}{x}. \qquad \blacksquare
$$

(Pulled the $1/u$ inside the log as an exponent in the second-to-last step, and used continuity of $\ln$ at $e$.)

---

### 5.8 Proof of $\frac{d}{dx} e^x = e^x$

**Strategy.** The relation $\frac{d}{dx}\ln x = 1/x$ from §5.7 was derived assuming we already had $\frac{d}{dx}e^x = e^x$. Let's break the circularity by using the limit-of-power definition of $e$ to derive $\frac{d}{dx}e^x$ from scratch.

**Setup.** Define $f(x) = e^x$. Apply Definition 1.2.1:

$$
f'(x) = \lim_{h \to 0}\frac{e^{x+h} - e^x}{h} = \lim_{h \to 0}\frac{e^x(e^h - 1)}{h} = e^x \cdot \lim_{h \to 0}\frac{e^h - 1}{h}.
$$

The limit $\lim_{h \to 0}(e^h - 1)/h$ is independent of $x$; call it $K$. We need $K = 1$.

**Compute $K$.** Substitute $u = e^h - 1$, so $e^h = 1 + u$, $h = \ln(1 + u)$, and $h \to 0 \Leftrightarrow u \to 0$:

$$
K = \lim_{u \to 0} \frac{u}{\ln(1 + u)} = \frac{1}{\lim_{u \to 0} \frac{\ln(1+u)}{u}}.
$$

The inner limit is, by the same computation in §5.7, $\ln e = 1$. Hence $K = 1/1 = 1$.

**Therefore** $f'(x) = e^x \cdot 1 = e^x$. $\blacksquare$

(For full rigor, one defines $e^x$ either as the inverse of $\ln x := \int_1^x dt/t$ or as the unique solution of $y' = y$ with $y(0) = 1$. Both definitions make $\frac{d}{dx}e^x = e^x$ tautological. The argument above is the standard "cookbook calculus" version that pivots through the limit definition of $e$.)

---

### 5.9 Proof of Fermat's Theorem (1.2.2)

**Claim.** Suppose $f$ has a local maximum at the interior point $c$ and $f$ is differentiable at $c$. Then $f'(c) = 0$. (Local minimum case is symmetric — apply the argument to $-f$.)

**Setup.** "Local max at interior point $c$" means there is some $\delta_0 > 0$ with $(c - \delta_0, c + \delta_0) \subset \operatorname{dom} f$ and $f(x) \leq f(c)$ for all $x \in (c - \delta_0, c + \delta_0)$.

**Right-hand difference quotient.** For $h \in (0, \delta_0)$:

$$
\frac{f(c + h) - f(c)}{h} \leq 0
$$

because the numerator is $\leq 0$ (local max) and the denominator $h > 0$. Take the limit $h \to 0^+$ — limits preserve weak inequalities (a standard fact from Chapter 1.1):

$$
f'_+(c) = \lim_{h \to 0^+} \frac{f(c + h) - f(c)}{h} \leq 0.
$$

**Left-hand difference quotient.** For $h \in (-\delta_0, 0)$, the numerator is still $\leq 0$ but the denominator $h < 0$, so the *quotient* is $\geq 0$:

$$
\frac{f(c + h) - f(c)}{h} \geq 0 \quad \Longrightarrow \quad f'_-(c) = \lim_{h \to 0^-} \frac{f(c + h) - f(c)}{h} \geq 0.
$$

**Combine.** Differentiability at $c$ forces $f'_+(c) = f'_-(c) = f'(c)$ (Definition 1.2.3). So we have one number that is both $\leq 0$ and $\geq 0$. The only such number is $0$:

$$
f'(c) = 0. \qquad \blacksquare
$$

**Important caveat.** The hypothesis "$c$ is an interior point" is essential. At an endpoint of an interval, only one one-sided derivative is defined and the other inequality drops out. E.g., $f(x) = x$ on $[0, 1]$ has its max at $c = 1$ but $f'(1) = 1 \neq 0$.

---


### 5.10 Proof of Rolle's Theorem (1.2.3)

**Claim.** $f$ continuous on $[a, b]$, differentiable on $(a, b)$, $f(a) = f(b)$ $\Rightarrow$ there exists $c \in (a, b)$ with $f'(c) = 0$.

**Apply the Extreme Value Theorem** ([Theorem 1.1.3](1.1---Limits-&-Continuity#1-1-3-extreme-value-theorem-evt)). Since $f$ is continuous on the closed bounded interval $[a, b]$, $f$ attains a global max $M$ at some $c_M \in [a, b]$ and a global min $m$ at some $c_m \in [a, b]$.

**Case 1: $M = m$.** Then $f$ is constant on $[a, b]$, so $f'(x) = 0$ for every $x \in (a, b)$. Pick any $c$ in the interior. Done.

**Case 2: $M > m$.** Then *at least one of* $M$ or $m$ is attained at an interior point — because if both extrema were only at the endpoints $a$ and $b$, then $f(a) = f(b)$ would force $M = f(a) = f(b) = m$, contradicting $M > m$. Say WLOG $c_M \in (a, b)$.

Since $f$ has a local maximum at the interior point $c_M$ (it's a *global* max, hence trivially a local max), and $f$ is differentiable on $(a, b)$ in particular at $c_M$, **Fermat's Theorem (1.2.2)** gives $f'(c_M) = 0$. Take $c = c_M \in (a, b)$. $\blacksquare$

---

### 5.11 Proof of the Mean Value Theorem (1.2.4) from Rolle's Theorem

**Claim.** $f$ continuous on $[a, b]$, differentiable on $(a, b)$ $\Rightarrow$ $\exists c \in (a, b)$ with $f'(c) = \frac{f(b) - f(a)}{b - a}$.

**Strategy.** Subtract off the secant line so we can apply Rolle.

**Define an auxiliary function.** Let $L(x)$ be the secant line through $(a, f(a))$ and $(b, f(b))$:

$$
L(x) = f(a) + \frac{f(b) - f(a)}{b - a}\,(x - a).
$$

Define

$$
g(x) = f(x) - L(x).
$$

**Verify Rolle's hypotheses for $g$.**

1. $g$ is continuous on $[a, b]$ — sum of continuous functions ($f$ continuous by hypothesis; $L$ is linear, hence continuous).
2. $g$ is differentiable on $(a, b)$ — sum of differentiable functions.
3. $g(a) = f(a) - L(a) = f(a) - f(a) = 0$. And $g(b) = f(b) - L(b) = f(b) - [f(a) + (f(b) - f(a))] = 0$. So $g(a) = g(b)$.

**Apply Rolle (1.2.3).** There exists $c \in (a, b)$ with $g'(c) = 0$. Compute:

$$
g'(x) = f'(x) - L'(x) = f'(x) - \frac{f(b) - f(a)}{b - a}.
$$

Setting $g'(c) = 0$:

$$
f'(c) = \frac{f(b) - f(a)}{b - a}. \qquad \blacksquare
$$

---

### 5.12 Proof of L'Hôpital's Rule (1.2.6) — 0/0 Case

**Setup.** $f, g$ differentiable on $(a, b)$, $g'(x) \neq 0$ on $(a, b)$, $\lim_{x \to a^+} f(x) = \lim_{x \to a^+} g(x) = 0$, and $\lim_{x \to a^+} f'(x)/g'(x) = L$.

**Extension to closed left endpoint.** Extend $f, g$ to $a$ by defining $f(a) = g(a) = 0$. Then $f, g$ are continuous at $a$ from the right (the value matches the limit, [Definition 1.1.5](1.1---Limits-&-Continuity#1-definitions)).

**Apply Cauchy's MVT (Theorem 1.2.5)** on $[a, x]$ for any $x \in (a, b)$. Since $f, g$ are continuous on $[a, x]$ and differentiable on $(a, x)$ with $g' \neq 0$, there exists $c_x \in (a, x)$ with

$$
\frac{f(x) - f(a)}{g(x) - g(a)} = \frac{f'(c_x)}{g'(c_x)}.
$$

Substitute $f(a) = g(a) = 0$:

$$
\frac{f(x)}{g(x)} = \frac{f'(c_x)}{g'(c_x)}.
$$

**Squeeze the inner point.** As $x \to a^+$, the intermediate point $c_x$ satisfies $a < c_x < x$, so $c_x \to a^+$ as well. Take the limit:

$$
\lim_{x \to a^+} \frac{f(x)}{g(x)} = \lim_{x \to a^+} \frac{f'(c_x)}{g'(c_x)} = \lim_{c \to a^+} \frac{f'(c)}{g'(c)} = L. \qquad \blacksquare
$$

The $\infty/\infty$ case requires a slightly different but conceptually similar argument; see Rudin's *Principles of Mathematical Analysis*, Theorem 5.13, for the full version.

---

### 5.13 Proof Sketch of Taylor's Theorem with Lagrange Remainder (1.2.7)

**Strategy.** Generalize Rolle by inserting a polynomial that matches $f$ to $n$-th order at $a$.

**Setup.** Fix $x \in (a, b]$. Define the Taylor polynomial of degree $n$ centered at $a$:

$$
T_n(t) = \sum_{k=0}^{n} \frac{f^{(k)}(a)}{k!}(t - a)^k.
$$

We want to find a point $\xi$ between $a$ and $x$ such that $f(x) - T_n(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!}(x - a)^{n+1}$.

**Define the auxiliary function.** Choose a constant $K$ so that the equation holds at $t = x$ — i.e., set

$$
K = \frac{f(x) - T_n(x)}{(x - a)^{n+1}},
$$

provided $x \neq a$. Define

$$
\Phi(t) = f(t) - T_n(t) - K (t - a)^{n+1}.
$$

**Compute $\Phi$ at the endpoints.** By construction $\Phi(x) = 0$. At $t = a$, every term in $T_n(t)$ at $t = a$ contributes $f^{(k)}(a)/k! \cdot 0^k$, leaving only $T_n(a) = f(a)$. Also $(a - a)^{n+1} = 0$. So $\Phi(a) = f(a) - f(a) - K \cdot 0 = 0$.

**Differentiate $\Phi$.** Notice that $T_n^{(k)}(a) = f^{(k)}(a)$ for $k = 0, 1, \dots, n$ (this is the matching property of the Taylor polynomial). So $\Phi^{(k)}(a) = 0$ for $k = 0, 1, \dots, n$.

**Iterate Rolle's Theorem.** $\Phi(a) = \Phi(x) = 0$, so by Rolle there exists $\xi_1 \in (a, x)$ with $\Phi'(\xi_1) = 0$. But also $\Phi'(a) = 0$ (matching property), so on $[a, \xi_1]$ Rolle gives $\xi_2 \in (a, \xi_1)$ with $\Phi''(\xi_2) = 0$. Continuing inductively, after $n + 1$ applications of Rolle we obtain $\xi := \xi_{n+1} \in (a, x)$ with

$$
\Phi^{(n+1)}(\xi) = 0.
$$

**Compute $\Phi^{(n+1)}$.** $T_n$ is a polynomial of degree $n$, so $T_n^{(n+1)} \equiv 0$. And $\frac{d^{n+1}}{dt^{n+1}}(t - a)^{n+1} = (n+1)!$. Hence

$$
\Phi^{(n+1)}(t) = f^{(n+1)}(t) - 0 - K \cdot (n+1)!.
$$

Set this to zero at $t = \xi$:

$$
f^{(n+1)}(\xi) = K \cdot (n+1)!.
$$

**Solve for $K$ and unwind.** Substituting back into the definition of $K$:

$$
\frac{f(x) - T_n(x)}{(x - a)^{n+1}} = \frac{f^{(n+1)}(\xi)}{(n+1)!},
$$

which rearranges to

$$
f(x) = T_n(x) + \frac{f^{(n+1)}(\xi)}{(n+1)!}(x - a)^{n+1}. \qquad \blacksquare
$$

The remainder is exactly the Lagrange form. The proof sketch is standard; see [proofwiki.org's Cauchy MVT version](https://proofwiki.org/wiki/Taylor's_Theorem/One_Variable/Proof_by_Cauchy_Mean_Value_Theorem) for an alternative derivation that uses Cauchy MVT directly on a clever pair of functions.

---


## 🖼️ Visual Anchor — The Mean Value Theorem

The MVT says: somewhere strictly between $a$ and $b$, the **tangent line** is parallel to the **secant** through $(a, f(a))$ and $(b, f(b))$.

![math-01__1.2-fig2](math-01__1.2-fig2.svg)

The orange curve is $f$. The dashed gold line is the secant; the solid gold line is the tangent at the MVT-guaranteed point $c$. They have the same slope — that's the entire content of MVT.

---

## 🎯 6. Worked Examples

### Example 1.2.E1 — The Power Rule for a Negative Exponent

Compute $\frac{d}{dx}\left[x^{-3}\right]$ via the limit definition (and verify it matches $-3 x^{-4}$).

**Step 1 — Apply the definition.**

$$
\frac{d}{dx}\big[x^{-3}\big] = \lim_{h \to 0}\frac{(x+h)^{-3} - x^{-3}}{h} = \lim_{h \to 0}\frac{1}{h}\left[\frac{1}{(x+h)^3} - \frac{1}{x^3}\right].
$$

**Step 2 — Common denominator.**

$$
\frac{1}{(x+h)^3} - \frac{1}{x^3} = \frac{x^3 - (x+h)^3}{(x+h)^3\,x^3}.
$$

**Step 3 — Expand the cube.** $(x+h)^3 = x^3 + 3 x^2 h + 3 x h^2 + h^3$, so

$$
x^3 - (x+h)^3 = -3 x^2 h - 3 x h^2 - h^3 = -h\,(3 x^2 + 3 x h + h^2).
$$

**Step 4 — Divide by $h$.**

$$
\frac{1}{h}\left[\frac{x^3 - (x+h)^3}{(x+h)^3 x^3}\right] = \frac{-(3 x^2 + 3 x h + h^2)}{(x+h)^3 x^3}.
$$

**Step 5 — Take the limit $h \to 0$.** Numerator $\to -3 x^2$, denominator $\to x^3 \cdot x^3 = x^6$:

$$
\frac{d}{dx}\big[x^{-3}\big] = \frac{-3 x^2}{x^6} = -3 x^{-4}. \qquad \checkmark
$$

Matches the power rule with $n = -3$: $n x^{n-1} = -3 x^{-4}$.

### Example 1.2.E2 — Implicit Differentiation of an Ellipse

Find $\frac{dy}{dx}$ on the ellipse $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$ (with $a, b > 0$).

**Step 1 — Differentiate both sides with respect to $x$.** The LHS contains $y$, which is implicitly a function of $x$, so use the chain rule on $y^2$:

$$
\frac{d}{dx}\left[\frac{x^2}{a^2}\right] + \frac{d}{dx}\left[\frac{y^2}{b^2}\right] = \frac{d}{dx}[1].
$$

$$
\frac{2x}{a^2} + \frac{2y}{b^2} \cdot \frac{dy}{dx} = 0.
$$

The second term comes from $\frac{d}{dx}\big[y^2\big] = 2y \cdot \frac{dy}{dx}$ via the chain rule (Lemma 1.2.7) with the outer function $u^2$ and inner $u = y(x)$.

**Step 2 — Solve for $dy/dx$.**

$$
\frac{2y}{b^2}\,\frac{dy}{dx} = -\frac{2x}{a^2}.
$$

$$
\frac{dy}{dx} = -\frac{2x}{a^2} \cdot \frac{b^2}{2y} = -\frac{b^2 x}{a^2 y}.
$$

**Step 3 — Sanity check.** At the rightmost point $(a, 0)$: $dy/dx \to \pm\infty$ (vertical tangent — geometrically correct). At $(0, b)$: $dy/dx = 0$ (horizontal tangent at the top). ✓

$$
\boxed{\frac{dy}{dx} = -\frac{b^2 x}{a^2 y} \quad (y \neq 0)}.
$$

### Example 1.2.E3 — Related Rates: The Sliding Ladder

A 13-foot ladder leans against a vertical wall. The bottom of the ladder slides away from the wall at $\frac{dx}{dt} = 2$ ft/s. How fast is the top sliding *down* the wall when the bottom is 5 ft from the wall?

**Step 1 — Set up the geometry.** Let $x(t)$ = distance from the wall to the foot of the ladder, $y(t)$ = height of the ladder's top on the wall. The ladder length is constant at 13 ft, so by Pythagoras:

$$
x(t)^2 + y(t)^2 = 13^2 = 169.
$$

**Step 2 — Differentiate with respect to time $t$.**

$$
\frac{d}{dt}\big[x^2 + y^2\big] = \frac{d}{dt}[169] \quad\Longrightarrow\quad 2x\,\frac{dx}{dt} + 2y\,\frac{dy}{dt} = 0.
$$

**Step 3 — Solve for $dy/dt$.**

$$
\frac{dy}{dt} = -\frac{x}{y}\,\frac{dx}{dt}.
$$

**Step 4 — Plug in numbers at the instant of interest.** When $x = 5$, the wall-height is $y = \sqrt{169 - 25} = \sqrt{144} = 12$ ft. With $dx/dt = 2$ ft/s:

$$
\frac{dy}{dt} = -\frac{5}{12} \cdot 2 = -\frac{10}{12} = -\frac{5}{6}\;\text{ft/s}.
$$

**Step 5 — Interpret.** The negative sign means $y$ is *decreasing* — the top is sliding down. Magnitude: $5/6 \approx 0.833$ ft/s, or about 10 inches per second.

$$
\boxed{\frac{dy}{dt} = -\tfrac{5}{6}\;\text{ft/s (top sliding down)}}.
$$

### Example 1.2.E4 — L'Hôpital on $(\sin x - x)/x^3$

Evaluate $\displaystyle\lim_{x \to 0}\frac{\sin x - x}{x^3}$.

**Step 1 — Diagnose.** Direct sub: $(0 - 0)/0 = 0/0$. Indeterminate.

**Step 2 — First L'Hôpital.** Differentiate top and bottom:

$$
\lim_{x \to 0}\frac{\cos x - 1}{3 x^2}.
$$

Sub: $(1 - 1)/0 = 0/0$. Still indeterminate. Apply L'Hôpital again — but first **check the hypothesis**: $f' = \cos x - 1$ and $g' = 3 x^2$ are differentiable on a punctured neighborhood of $0$, $g'' = 6x \neq 0$ for $x \neq 0$, and both top and bottom go to $0$. ✓

**Step 3 — Second L'Hôpital.**

$$
\lim_{x \to 0}\frac{-\sin x}{6 x}.
$$

Sub: $0/0$. Apply once more (or use the cornerstone limit directly).

**Step 4 — Use cornerstone limit.** $\sin x / x \to 1$, so

$$
\frac{-\sin x}{6 x} = -\frac{1}{6} \cdot \frac{\sin x}{x} \;\longrightarrow\; -\frac{1}{6} \cdot 1 = -\frac{1}{6}.
$$

(Or equivalently a third L'Hôpital: top differentiates to $-\cos x \to -1$, bottom to $6 \to 6$, so the limit is $-1/6$.)

$$
\boxed{\lim_{x \to 0}\frac{\sin x - x}{x^3} = -\frac{1}{6}}.
$$

**Cross-check via Taylor.** $\sin x = x - x^3/6 + O(x^5)$, so $\sin x - x = -x^3/6 + O(x^5)$, and dividing by $x^3$ gives $-1/6 + O(x^2) \to -1/6$. ✓


### Example 1.2.E5 — Taylor Polynomial of $e^x$ Around 0

Find the Taylor polynomial $T_4(x)$ of $f(x) = e^x$ centered at $a = 0$, and bound the error for $x \in [-1, 1]$.

**Step 1 — Compute derivatives.** $f^{(k)}(x) = e^x$ for every $k \geq 0$. Therefore $f^{(k)}(0) = e^0 = 1$ for all $k$.

**Step 2 — Assemble the Taylor polynomial.**

$$
T_n(x) = \sum_{k=0}^{n}\frac{f^{(k)}(0)}{k!}x^k = \sum_{k=0}^{n}\frac{x^k}{k!}.
$$

For $n = 4$:

$$
T_4(x) = 1 + x + \frac{x^2}{2} + \frac{x^3}{6} + \frac{x^4}{24}.
$$

**Step 3 — Apply the Lagrange remainder bound.** By Theorem 1.2.7, for some $\xi$ between $0$ and $x$:

$$
R_4(x) = \frac{f^{(5)}(\xi)}{5!}x^5 = \frac{e^\xi}{120}x^5.
$$

For $x \in [-1, 1]$, $\xi \in (-1, 1)$ and $e^\xi \leq e^1 = e < 2.72$. Therefore

$$
|R_4(x)| \leq \frac{e}{120} \cdot |x|^5 \leq \frac{2.72}{120} \cdot 1 \approx 0.0227.
$$

**Step 4 — Evaluate at $x = 1$.** $T_4(1) = 1 + 1 + 0.5 + 0.1\overline{6} + 0.041\overline{6} = 2.708\overline{3}$. True value $e \approx 2.71828$. Error $\approx 0.00994$, which is well below the $0.0227$ bound. ✓

$$
\boxed{T_4(x) = 1 + x + \tfrac{x^2}{2} + \tfrac{x^3}{6} + \tfrac{x^4}{24}, \qquad |R_4(x)| \leq \tfrac{e}{120}|x|^5.}
$$

### Example 1.2.E6 — Optimization: Maximum of $f(x) = x e^{-x^2/2}$ on $[-3, 3]$

This is the unnormalized Gaussian density times $x$ — a useful building block in probability.

**Step 1 — Compute the derivative.** Use the product rule:

$$
f'(x) = \frac{d}{dx}[x] \cdot e^{-x^2/2} + x \cdot \frac{d}{dx}\big[e^{-x^2/2}\big].
$$

The second piece needs the chain rule: $\frac{d}{dx}\big[e^{-x^2/2}\big] = e^{-x^2/2} \cdot (-x) = -x\,e^{-x^2/2}$.

$$
f'(x) = e^{-x^2/2} + x(-x e^{-x^2/2}) = e^{-x^2/2}(1 - x^2).
$$

**Step 2 — Find critical points.** $f'(x) = 0$ requires $1 - x^2 = 0$ (since $e^{-x^2/2} > 0$ always). Hence $x = \pm 1$.

**Step 3 — Evaluate $f$ at critical points and endpoints.**

| $x$ | $f(x) = x e^{-x^2/2}$ |
|---|---|
| $-3$ | $-3 e^{-4.5} \approx -0.0333$ |
| $-1$ | $-e^{-1/2} \approx -0.6065$ |
| $+1$ | $+e^{-1/2} \approx +0.6065$ |
| $+3$ | $+3 e^{-4.5} \approx +0.0333$ |

**Step 4 — Identify global extrema on the closed interval $[-3, 3]$.** The Extreme Value Theorem guarantees they exist (continuous function on compact interval). Comparing the four values: max at $x = 1$ with value $e^{-1/2}$, min at $x = -1$ with value $-e^{-1/2}$.

$$
\boxed{\max_{[-3,3]} f = e^{-1/2} \;(\text{at } x = 1), \quad \min_{[-3,3]} f = -e^{-1/2} \;(\text{at } x = -1).}
$$

**Sanity check.** $f$ is odd: $f(-x) = -f(x)$. So extrema must be symmetric, which they are. ✓

### Example 1.2.E7 — Newton's Method, One Step on $\sqrt{2}$

Newton's iteration for finding a root of $g(x) = 0$ is

$$
x_{n+1} = x_n - \frac{g(x_n)}{g'(x_n)}.
$$

Use it to approximate $\sqrt{2}$ as a root of $g(x) = x^2 - 2$ starting from $x_0 = 1.5$.

**Step 1 — Compute $g'$.** $g'(x) = 2x$.

**Step 2 — Apply the iteration once.**

$$
x_1 = x_0 - \frac{g(x_0)}{g'(x_0)} = 1.5 - \frac{(1.5)^2 - 2}{2 \cdot 1.5} = 1.5 - \frac{2.25 - 2}{3} = 1.5 - \frac{0.25}{3} = 1.5 - 0.0833\overline{3} = 1.41\overline{6}.
$$

**Step 3 — Compare to $\sqrt{2}$.** $\sqrt{2} \approx 1.41421$. The error $|x_1 - \sqrt{2}| \approx 0.00245$ — already 3 correct digits after one iteration starting from $1.5$. (Newton's method converges quadratically near a simple root.)

**Step 4 — Geometric interpretation.** The iteration draws the tangent line to $y = g(x)$ at $x_0$ and finds where that tangent crosses the $x$-axis. That intercept is $x_1$. Repeat from $x_1$ to get $x_2$, etc.

$$
\boxed{x_1 = 17/12 \approx 1.41\overline{6}}.
$$

### Example 1.2.E8 — Logarithmic Differentiation of $x^x$

Find $\frac{d}{dx}\big[x^x\big]$ for $x > 0$.

**The trap.** This is **not** $x \cdot x^{x - 1} = x^x$ (would-be application of the power rule — but the exponent is itself $x$, not a constant) and **not** $x^x \ln x$ (would-be exponential rule — but the base is itself $x$, not a constant). Both rules fail because *both* base and exponent are variable.

**Step 1 — Take logs.** Let $y = x^x$, so $\ln y = x \ln x$.

**Step 2 — Differentiate both sides w.r.t. $x$.** LHS uses the chain rule (we don't yet know what $y'$ is — we'll solve for it):

$$
\frac{1}{y}\,\frac{dy}{dx} = \frac{d}{dx}\big[x \ln x\big] = 1 \cdot \ln x + x \cdot \frac{1}{x} = \ln x + 1.
$$

(Used product rule on $x \ln x$.)

**Step 3 — Solve for $dy/dx$.**

$$
\frac{dy}{dx} = y \cdot (\ln x + 1) = x^x (\ln x + 1).
$$

**Cross-check via $a^b = e^{b \ln a}$.** Write $x^x = e^{x \ln x}$ and apply chain rule:

$$
\frac{d}{dx}e^{x \ln x} = e^{x \ln x} \cdot \frac{d}{dx}[x \ln x] = e^{x \ln x} (\ln x + 1) = x^x (\ln x + 1). \quad \checkmark
$$

$$
\boxed{\frac{d}{dx}\big[x^x\big] = x^x (\ln x + 1) \quad (x > 0)}.
$$

**Where is this derivative zero?** $x^x > 0$ always (for $x > 0$), so $dy/dx = 0 \Leftrightarrow \ln x + 1 = 0 \Leftrightarrow x = e^{-1} = 1/e$. That gives the global minimum of $x^x$ on $(0, \infty)$: $f(1/e) = (1/e)^{1/e} \approx 0.6922$.

### Example 1.2.E9 — Inverse Function Theorem on $\arcsin$

Derive $\frac{d}{dx}\arcsin x = \frac{1}{\sqrt{1 - x^2}}$ from scratch.

**Step 1 — Setup.** Let $y = \arcsin x$ for $x \in (-1, 1)$, so $y \in (-\pi/2, \pi/2)$ and $\sin y = x$.

**Step 2 — Differentiate both sides w.r.t. $x$ (implicit).**

$$
\cos y \cdot \frac{dy}{dx} = 1 \quad \Longrightarrow \quad \frac{dy}{dx} = \frac{1}{\cos y}.
$$

**Step 3 — Express $\cos y$ in terms of $x$.** Use the Pythagorean identity $\sin^2 y + \cos^2 y = 1$:

$$
\cos^2 y = 1 - \sin^2 y = 1 - x^2.
$$

On $y \in (-\pi/2, \pi/2)$, $\cos y > 0$, so $\cos y = +\sqrt{1 - x^2}$ (positive root).

**Step 4 — Conclude.**

$$
\frac{d}{dx}\arcsin x = \frac{1}{\sqrt{1 - x^2}} \quad \text{for } x \in (-1, 1). \qquad \blacksquare
$$

**Note on the boundary.** At $x = \pm 1$, $\sqrt{1 - x^2} = 0$ and the derivative blows up — corresponding to the *vertical tangents* of the $\arcsin$ graph at its boundary.

---


## 🖼️ Visual Anchor — Linearization (Local Linear Approximation)

For $x$ near $a$, the tangent line is the *best* linear approximation to $f$. The error grows quadratically, not linearly. Formally: $f(x) = f(a) + f'(a)(x - a) + R$, where $|R| = O((x-a)^2)$ as $x \to a$.

![math-01__1.2-fig3](math-01__1.2-fig3.svg)

The shaded region is the gap between $f$ (orange) and its tangent line $L$ (gold dashed). Crucially, that gap shrinks **quadratically** as $h \to 0$, so the tangent line is good not just as a coarse approximation but as a *first-order* one — error vanishes faster than the input perturbation.

---

## 🖼️ Visual Anchor — Newton's Method Iteration

![math-01__1.2-fig4](math-01__1.2-fig4.svg)

Each iteration draws the tangent at the current $x_n$, finds where it crosses the $x$-axis, and uses that as the next $x_{n+1}$. Near a simple root, the error squares each step — quadratic convergence.

---


## 🖼️ Visual Anchor — Taylor Polynomials Approaching $e^x$

![math-01__1.2-fig5](math-01__1.2-fig5.svg)

Each successively higher Taylor polynomial hugs $e^x$ over a wider interval. By degree 5 the visual difference is invisible at this scale on $[-1, 2]$. The Lagrange remainder bound from §5.13 quantifies that closeness exactly.

---

## 🌌 7. Indeterminate Forms Revisited (with L'Hôpital and the Exponential Trick)

Chapter 1.1 listed the four base indeterminate forms. With the derivative now in hand, we can attack all seven systematically.

### 7.1 The Seven Indeterminate Forms

| Form | Example | Tactic |
|---|---|---|
| $0/0$ | $\sin x / x$ | L'Hôpital, factoring, conjugate, Taylor |
| $\infty/\infty$ | $x / e^x$ as $x \to \infty$ | L'Hôpital, divide-by-leading-term |
| $0 \cdot \infty$ | $x \ln x$ as $x \to 0^+$ | Rewrite as $\ln x / (1/x)$ then L'Hôpital |
| $\infty - \infty$ | $\sec x - \tan x$ as $x \to \pi/2^-$ | Common denominator $\to 0/0$ |
| $0^0$ | $x^x$ as $x \to 0^+$ | Take logs, use $\exp(\lim g \ln f)$ |
| $\infty^0$ | $x^{1/x}$ as $x \to \infty$ | Take logs |
| $1^\infty$ | $(1 + 1/x)^x$ as $x \to \infty$ | Take logs |

### 7.2 The Exponential Trick

For any indeterminate form of type $f^g$ where $f \to 0, 1, \text{or } \infty$ and $g$ does something pathological, transform via

$$
f^g = e^{g \ln f}.
$$

The exponential is continuous (so we can pull the limit inside), reducing the problem to evaluating $\lim g \ln f$, which is one of the four base forms.

**Worked Example — $\lim_{x \to \infty}\big(1 + 1/x\big)^x$ (the definition of $e$).**

**Step 1 — Take logs.** Let $L = \lim_{x \to \infty}\big(1 + 1/x\big)^x$. Then

$$
\ln L = \lim_{x \to \infty} x\,\ln\!\left(1 + \frac{1}{x}\right).
$$

This is now $\infty \cdot 0$ (since $\ln(1 + 0) = 0$ and $x \to \infty$). Indeterminate, but **base-form** indeterminate.

**Step 2 — Rewrite as $0/0$.** Substitute $u = 1/x$ so $x = 1/u$ and $u \to 0^+$:

$$
\ln L = \lim_{u \to 0^+} \frac{\ln(1 + u)}{u}.
$$

**Step 3 — L'Hôpital.** Top differentiates to $1/(1+u)$, bottom to $1$:

$$
\ln L = \lim_{u \to 0^+} \frac{1/(1+u)}{1} = \frac{1}{1} = 1.
$$

**Step 4 — Exponentiate.** Continuity of $e^x$ means $L = e^{\ln L} = e^1 = e$.

$$
\boxed{\lim_{x \to \infty}\!\left(1 + \tfrac{1}{x}\right)^{x} = e}.
$$

### 7.3 When L'Hôpital Does **Not** Apply

L'Hôpital is **only** valid when:

1. The limit is genuinely $0/0$ or $\infty/\infty$ at the limit point.
2. Both $f$ and $g$ are differentiable in a punctured neighborhood.
3. $g'(x) \neq 0$ in that neighborhood.
4. The new limit $\lim f'/g'$ exists (as a real number or $\pm\infty$).

If you mechanically L'Hôpital a non-indeterminate form, you'll get a **wrong answer**. Example: $\lim_{x \to 0}\dfrac{x + 1}{x^2 + 1} = \dfrac{1}{1} = 1$ by direct substitution. Mechanically applying L'Hôpital would give $\lim 1/(2x) = \infty$, which is wrong because the original limit was *not* indeterminate. Always check the form first.

---


## ⚠️ 8. Common Pitfalls (Sand Traps for the Unwary)

Six errors that account for ≈80% of mistakes in introductory differential calculus. Memorize them; they will save you in every exam and every late-night debugging session.

### 8.1 Forgetting the Inner Derivative in the Chain Rule

Compute $\frac{d}{dx}\sin(x^2)$. Wrong answer: $\cos(x^2)$. Right answer: $\cos(x^2) \cdot 2x = 2x\cos(x^2)$.

Pattern: when the argument of a function is itself a non-trivial function of $x$, you owe a multiplicative factor of the inner derivative. Mantra: **outer derivative at inner, times inner derivative.** Even simpler check: if the inside isn't literally `x`, you're chaining.

### 8.2 Confusing $f' > 0$ with $f$ Increasing at a Point

The increasing/decreasing test (Theorem 1.2.8) requires $f' > 0$ on an *interval*, not at a single point. A function can have $f'(x_0) > 0$ at one point yet **fail to be monotonic on any neighborhood of $x_0$**. The classical counterexample is

$$
f(x) = \begin{cases} x/2 + x^2 \sin(1/x), & x \neq 0 \\ 0, & x = 0 \end{cases}
$$

which has $f'(0) = 1/2 > 0$ but oscillates infinitely often near $0$ — *not* monotonic on any neighborhood of $0$.

Statement to remember: positivity of $f'$ at a *single* point gives you nothing. You need the whole interval.

### 8.3 Applying L'Hôpital When the Form Is Not 0/0 or $\infty/\infty$

See §7.3. If the limit is not indeterminate, L'Hôpital can output garbage. Always diagnose the form **before** differentiating.

A subtler trap: the limit $\lim_{x \to 0}\frac{\sin x}{1 + \cos x} = 0/2 = 0$. Mechanically L'Hôpitaling gives $\lim \cos x / (-\sin x) = 1/0$, which is $\pm\infty$. Both numerator and denominator must independently approach the same indeterminate flavor.

### 8.4 Differentiating Only One Side of an Implicit Equation

Working with $x^2 + y^2 = 25$ (a circle), some students write $\frac{d}{dx}[x^2] + \frac{d}{dx}[y^2] = 0$ and produce $2x + 2y = 0$, forgetting that $y$ depends on $x$. The correct expansion is

$$
2x + 2y \cdot \frac{dy}{dx} = 0,
$$

via the chain rule on the second term. **Every** $y$-dependent expression generates a multiplicative $dy/dx$ when differentiated w.r.t. $x$.

### 8.5 Treating $dx$ as a Literal Infinitesimal

Notation like $dy = f'(x)\,dx$ is *suggestive* but mathematically formalized only as a linear map (Definition 1.2.7) or as a one-form (Chapter 1.8). You **cannot** "cancel $dx$" between $dy/dx$ and an integral $\int dx$ as if they were ordinary algebraic objects. Operations that *look* like canceling differentials (e.g., $u$-substitution, separation of variables for ODEs) are valid because of the chain rule and the Fundamental Theorem of Calculus, not because $dx$ is a literal small number.

If you want infinitesimals to actually exist as numbers, you have to leave standard analysis and work in non-standard analysis (Robinson 1961). Worth knowing it exists; not worth using in this curriculum.

### 8.6 Confusing $\frac{d}{dx}\big[f(x)\big]^n$ with $n[f(x)]^{n-1}$

$\frac{d}{dx}\big[(x^2 + 1)^7\big]$ is *not* $7(x^2 + 1)^6$. It's $7(x^2 + 1)^6 \cdot 2x$ via the chain rule. The power rule applied to a constant base is shorthand for "outer power $\times$ inner derivative" once the inner is non-trivial. Same family of mistake as 8.1; calling it out separately because students blow this every time.

### 8.7 Bonus — Sign Errors on the Quotient Rule

The quotient rule has a *minus* sign in the numerator and the **first** term is $f'g$, not $g f'$ swapped. Mnemonic: *"low d-high minus high d-low, square the bottom and away you go"* — i.e., $\frac{f}{g} \to \frac{g f' - f g'}{g^2}$. The minus sign makes the rule non-symmetric in $f$ and $g$, unlike the product rule.

---

## 🛠️ 9. Pairing with `CalculusVisualizer`

To turn algebra into intuition, use the local C++ tool [CalculusVisualizer](CalculusVisualizer) for the following loops:

1. **Secant-to-tangent convergence.** Pick $f(x) = x^3$, $a = 1$. Plot the secant from $(1, 1)$ to $(1 + h, (1+h)^3)$ for $h = 0.5, 0.1, 0.01, 0.001$. Confirm the secant slopes $(((1+h)^3 - 1)/h)$ converge to $3$. (And $f'(1) = 3 \cdot 1^2 = 3$. ✓)
2. **MVT verification.** For $f(x) = x^3 - x$ on $[0, 2]$, compute the secant slope $(f(2) - f(0))/2 = 6/2 = 3$. Solve $f'(c) = 3 c^2 - 1 = 3$ symbolically: $c = \sqrt{4/3} \approx 1.155$. Plot the curve, the secant, and verify the tangent at $c$ is parallel to the secant. (It is.)
3. **Newton's method visualization.** Animate Newton iterations on $g(x) = x^2 - 2$ starting from $x_0 = 1.5$. Watch $x_1 = 17/12 \approx 1.4167$, $x_2 \approx 1.4142157$, $x_3 \approx 1.41421356$ — quadratic doubling of correct digits per step.
4. **Taylor approximation overlay.** Overplot $f(x) = e^x$ with $T_1, T_2, T_3, T_4$ on $[-2, 2]$. Notice the visual error region grow with $|x|$ at fixed $n$, and shrink with $n$ at fixed $|x|$. Tabulate the actual error against the Lagrange bound from Example E5.

This empirical-symbolic feedback loop is how you internalize the theorems.

---

## 📓 10. Study Tactics

A few honest tactics that work for the long game.

1. **Re-derive the rules from scratch.** Don't memorize the product/quotient/chain rules — re-derive each on a blank sheet at the start of each study session for a week. After week one they'll feel like multiplication tables.
2. **Use the SymPy practice script.** [`scripts/1.2_differentiation.py`](1.2_differentiation.py) generates fresh randomized drill problems with verified solutions every time you run it. Tag rep cards with `#review/calc/1.2` for spaced repetition.
3. **Run two flavors of every limit.** When you compute a limit using L'Hôpital, also compute it using Taylor expansion. The two methods should agree; if they don't, find the bug in your work. This catches a huge fraction of student errors.
4. **Do all eight worked examples by hand before reading the solutions.** Pretend the spoiler is locked. Write out every algebraic step. Then compare.
5. **Build derivative reflexes via timed sets.** Set a 60-second timer. Differentiate a list of 20 pre-prepared expressions. Aim for ≤ 3 seconds per expression on basic compositions. Speed isn't elegance, but it is fluency.
6. **Connect to physics early.** Each time you compute a derivative, ask: "If this were $f(t) =$ position, what is $f'$? $f''$?" Even when the function is artificial, training yourself to think kinematically pays off in [Chapter 4.1](4.1---Newtonian-Mechanics-&-Kinematics).

---


## 📝 11. Hand-Written Challenge Problems

> ⚠️ Solve every problem on paper before peeking at the spoiler. Write out **every** step. The pain is the point.

### Problem 1.2.P1 — Derivative from First Principles

Use Definition 1.2.1 to compute $f'(x)$ for $f(x) = \dfrac{1}{x + 3}$. Do not use the quotient rule.

<details>

<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Set up the difference quotient.

$$
f'(x) = \lim_{h \to 0}\frac{f(x + h) - f(x)}{h} = \lim_{h \to 0}\frac{1}{h}\left[\frac{1}{x + h + 3} - \frac{1}{x + 3}\right].
$$

#### Step 2: Common denominator inside the brackets.

$$
\frac{1}{x + h + 3} - \frac{1}{x + 3} = \frac{(x + 3) - (x + h + 3)}{(x + h + 3)(x + 3)} = \frac{-h}{(x + h + 3)(x + 3)}.
$$

#### Step 3: Divide by $h$ and simplify.

$$
\frac{1}{h} \cdot \frac{-h}{(x + h + 3)(x + 3)} = \frac{-1}{(x + h + 3)(x + 3)}.
$$

(Cancellation valid because $h \neq 0$ in the limit.)

#### Step 4: Take the limit.

$$
f'(x) = \lim_{h \to 0}\frac{-1}{(x + h + 3)(x + 3)} = \frac{-1}{(x + 3)^2}.
$$

#### Step 5: Cross-check with the power rule.

$f(x) = (x + 3)^{-1}$, so the chain rule plus the power rule gives $f'(x) = -1 \cdot (x + 3)^{-2} \cdot 1 = -1/(x+3)^2$. ✓

**Final answer:**

$$
\boxed{f'(x) = -\frac{1}{(x + 3)^2}.}
$$

</details>

### Problem 1.2.P2 — Chain Rule on a Triple Composition

Compute $\frac{dy}{dx}$ where $y = \sin\!\big(\cos(x^2 + 1)\big)$.

<details>

<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Identify the composition layers.

Outer: $\sin(\cdot)$. Middle: $\cos(\cdot)$. Inner: $x^2 + 1$.

#### Step 2: Apply the chain rule three times.

$$
\frac{dy}{dx} = \cos\!\big(\cos(x^2 + 1)\big) \cdot \frac{d}{dx}\!\left[\cos(x^2 + 1)\right].
$$

#### Step 3: Differentiate the middle layer.

$$
\frac{d}{dx}\!\left[\cos(x^2 + 1)\right] = -\sin(x^2 + 1) \cdot \frac{d}{dx}[x^2 + 1] = -\sin(x^2 + 1) \cdot 2x.
$$

#### Step 4: Multiply everything together.

$$
\frac{dy}{dx} = \cos\!\big(\cos(x^2 + 1)\big) \cdot \big[-2x\,\sin(x^2 + 1)\big].
$$

#### Step 5: Tidy up.

$$
\boxed{\frac{dy}{dx} = -2x\,\sin(x^2 + 1)\,\cos\!\big(\cos(x^2 + 1)\big).}
$$

</details>

### Problem 1.2.P3 — Implicit Differentiation on $x^3 + y^3 = 6xy$ (Folium of Descartes)

Find the slope of the tangent at the point $(3, 3)$ on the folium $x^3 + y^3 = 6xy$.

<details>

<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Verify the point is on the curve.

$3^3 + 3^3 = 27 + 27 = 54$, and $6 \cdot 3 \cdot 3 = 54$. ✓

#### Step 2: Differentiate both sides w.r.t. $x$.

Treating $y = y(x)$ implicitly:

$$
\frac{d}{dx}[x^3] + \frac{d}{dx}[y^3] = \frac{d}{dx}[6xy].
$$

LHS: $3x^2 + 3y^2 \cdot \dfrac{dy}{dx}$ (chain rule on $y^3$).

RHS via product rule: $6 \cdot 1 \cdot y + 6x \cdot \dfrac{dy}{dx} = 6y + 6x\,\dfrac{dy}{dx}$.

#### Step 3: Assemble and isolate $dy/dx$.

$$
3x^2 + 3y^2\,\frac{dy}{dx} = 6y + 6x\,\frac{dy}{dx}.
$$

Group $dy/dx$ terms on one side:

$$
3y^2\,\frac{dy}{dx} - 6x\,\frac{dy}{dx} = 6y - 3x^2.
$$

$$
\frac{dy}{dx}\,(3y^2 - 6x) = 6y - 3x^2 \quad \Longrightarrow \quad \frac{dy}{dx} = \frac{6y - 3x^2}{3y^2 - 6x} = \frac{2y - x^2}{y^2 - 2x}.
$$

#### Step 4: Plug in $(3, 3)$.

$$
\frac{dy}{dx}\bigg|_{(3,3)} = \frac{2 \cdot 3 - 3^2}{3^2 - 2 \cdot 3} = \frac{6 - 9}{9 - 6} = \frac{-3}{3} = -1.
$$

**Final answer:** $\boxed{-1}$. The tangent at $(3, 3)$ has slope $-1$ — this is the famous self-symmetric folium tangent.

</details>

### Problem 1.2.P4 — Indeterminate Form $0 \cdot \infty$

Evaluate $\displaystyle\lim_{x \to 0^+} x \ln x$.

<details>

<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Diagnose.

As $x \to 0^+$, $x \to 0$ and $\ln x \to -\infty$. Form is $0 \cdot (-\infty)$ — indeterminate.

#### Step 2: Convert to a 0/0 or $\infty/\infty$ form.

Write $x \ln x = \dfrac{\ln x}{1/x}$. As $x \to 0^+$: numerator $\to -\infty$, denominator $\to +\infty$. So the form is $\infty/\infty$ ✓ (modulo signs — L'Hôpital handles negative $\infty$ identically).

#### Step 3: Apply L'Hôpital.

$$
\lim_{x \to 0^+}\frac{\ln x}{1/x} = \lim_{x \to 0^+}\frac{1/x}{-1/x^2} = \lim_{x \to 0^+}\frac{1}{x} \cdot \frac{-x^2}{1} = \lim_{x \to 0^+}(-x) = 0.
$$

**Final answer:**

$$
\boxed{\lim_{x \to 0^+} x \ln x = 0.}
$$

(Useful corollary: $x^x = e^{x \ln x} \to e^0 = 1$ as $x \to 0^+$. So $0^0$ is naturally extended to $1$ in the calculus context, even though $0^0$ is formally indeterminate.)

</details>

### Problem 1.2.P5 — Optimization: The Soda Can

A cylindrical can of fixed volume $V = 355$ cm³ (≈ 12 oz) has surface area $S = 2\pi r^2 + 2\pi r h$ (top + bottom + side). Find the radius $r$ that minimizes $S$.

<details>

<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Express $S$ as a single-variable function.

Volume constraint: $\pi r^2 h = V$, so $h = V/(\pi r^2)$. Substitute:

$$
S(r) = 2\pi r^2 + 2\pi r \cdot \frac{V}{\pi r^2} = 2\pi r^2 + \frac{2V}{r}.
$$

Domain: $r \gt  0$.

#### Step 2: Differentiate and find critical points.

$$
S'(r) = 4\pi r - \frac{2V}{r^2}.
$$

Set $S'(r) = 0$:

$$
4\pi r = \frac{2V}{r^2} \quad \Longrightarrow \quad 4\pi r^3 = 2V \quad \Longrightarrow \quad r^3 = \frac{V}{2\pi} \quad \Longrightarrow \quad r = \sqrt[3]{V/(2\pi)}.
$$

#### Step 3: Confirm minimum via second-derivative test.

$$
S''(r) = 4\pi + \frac{4V}{r^3}.
$$

For $r \gt  0$, $S''(r) \gt  0$ — strictly convex on $(0, \infty)$. The unique critical point is a global minimum.

#### Step 4: Plug in $V = 355$.

$$
r^* = \sqrt[3]{355/(2\pi)} = \sqrt[3]{355/6.2832} \approx \sqrt[3]{56.5} \approx 3.84\;\text{cm}.
$$

#### Step 5: Compute optimal height.

$$
h^* = \frac{355}{\pi (3.84)^2} = \frac{355}{\pi \cdot 14.74} \approx \frac{355}{46.31} \approx 7.67\;\text{cm}.
$$

Note $h^* = 2 r^*$ — the optimal can is exactly twice as tall as it is wide. (Real soda cans are taller for ergonomic reasons, not surface-area reasons.)

**Final answer:**

$$
\boxed{r^* = \sqrt[3]{V/(2\pi)} \approx 3.84\;\text{cm}, \quad h^* = 2 r^* \approx 7.67\;\text{cm}.}
$$

</details>


### Problem 1.2.P6 — MVT Application: Bounding $\sin$

Use the Mean Value Theorem to prove that $|\sin x - \sin y| \leq |x - y|$ for all real $x, y$.

<details>

<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Trivial case.

If $x = y$, both sides are $0$ and the inequality holds.

#### Step 2: Assume WLOG $x \neq y$. Apply MVT to $f(t) = \sin t$ on $[\min(x, y), \max(x, y)]$.

$f$ is continuous and differentiable on all of $\mathbb{R}$, so MVT (Theorem 1.2.4) applies on any closed interval. There exists some $c$ strictly between $x$ and $y$ with

$$
\frac{\sin x - \sin y}{x - y} = f'(c) = \cos c.
$$

#### Step 3: Take absolute values.

$$
\left|\frac{\sin x - \sin y}{x - y}\right| = |\cos c|.
$$

Since $|\cos c| \leq 1$ for every real $c$:

$$
\left|\frac{\sin x - \sin y}{x - y}\right| \leq 1.
$$

#### Step 4: Multiply both sides by $|x - y| \gt  0$.

$$
|\sin x - \sin y| \leq |x - y|. \qquad \blacksquare
$$

This says **sine is 1-Lipschitz**, a fact used everywhere from numerical analysis to dynamical systems.

</details>

### Problem 1.2.P7 — Higher-Order Taylor: $\ln(1 + x)$ to Order 4

Find $T_4(x)$, the degree-4 Taylor polynomial of $f(x) = \ln(1 + x)$ centered at $a = 0$, and bound $|R_4(x)|$ for $x \in [0, 1/2]$.

<details>

<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Compute derivatives at $a = 0$.

| $k$ | $f^{(k)}(x)$ | $f^{(k)}(0)$ |
|---|---|---|
| 0 | $\ln(1 + x)$ | $\ln 1 = 0$ |
| 1 | $1/(1 + x)$ | $1$ |
| 2 | $-1/(1 + x)^2$ | $-1$ |
| 3 | $2/(1 + x)^3$ | $2$ |
| 4 | $-6/(1 + x)^4$ | $-6$ |
| 5 | $24/(1 + x)^5$ | $24$ at $x = 0$ |

Pattern: $f^{(k)}(x) = (-1)^{k-1}(k - 1)!/(1 + x)^k$ for $k \geq 1$.

#### Step 2: Assemble $T_4$.

$$
T_4(x) = \sum_{k=1}^{4}\frac{f^{(k)}(0)}{k!}x^k = \frac{1}{1!}x + \frac{-1}{2!}x^2 + \frac{2}{3!}x^3 + \frac{-6}{4!}x^4
$$

$$
= x - \frac{x^2}{2} + \frac{x^3}{3} - \frac{x^4}{4}.
$$

#### Step 3: Apply the Lagrange remainder.

$$
R_4(x) = \frac{f^{(5)}(\xi)}{5!}x^5 = \frac{24/(1+\xi)^5}{120}x^5 = \frac{x^5}{5(1+\xi)^5}
$$

for some $\xi \in (0, x)$.

#### Step 4: Bound $|R_4|$ on $[0, 1/2]$.

For $\xi \in [0, 1/2]$, $(1 + \xi)^5 \geq 1$, so

$$
|R_4(x)| \leq \frac{|x|^5}{5} \leq \frac{(1/2)^5}{5} = \frac{1/32}{5} = \frac{1}{160} = 0.00625.
$$

**Final answer:**

$$
\boxed{T_4(x) = x - \tfrac{x^2}{2} + \tfrac{x^3}{3} - \tfrac{x^4}{4}, \qquad |R_4(x)| \leq \tfrac{1}{160} \approx 6.25 \times 10^{-3} \text{ on } [0, 1/2].}
$$

#### Cross-check at $x = 1/2$.

$T_4(0.5) = 0.5 - 0.125 + 0.04167 - 0.015625 = 0.40104$. True value $\ln(1.5) \approx 0.40546$. Error $\approx 0.0044 \lt  0.00625$. ✓

</details>

### Problem 1.2.P8 — A $1^\infty$ Indeterminate Form

Evaluate $\displaystyle\lim_{x \to 0}\big(1 + 3x\big)^{2/x}$.

<details>

<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Diagnose.

Base $\to 1$, exponent $\to \pm\infty$. Form is $1^\infty$ — indeterminate.

#### Step 2: Take logs.

Let $L = \lim_{x \to 0}(1 + 3x)^{2/x}$. Then

$$
\ln L = \lim_{x \to 0} \frac{2}{x}\ln(1 + 3x).
$$

Form: $0/0 \cdot$ (a constant 2) — really $2 \cdot \lim \ln(1 + 3x)/x$, with the limit factor being $0/0$.

#### Step 3: Apply L'Hôpital to $\ln(1 + 3x)/x$.

Top differentiates to $3/(1 + 3x)$, bottom to $1$:

$$
\lim_{x \to 0}\frac{\ln(1 + 3x)}{x} = \lim_{x \to 0}\frac{3/(1 + 3x)}{1} = \frac{3}{1} = 3.
$$

#### Step 4: Multiply.

$$
\ln L = 2 \cdot 3 = 6.
$$

#### Step 5: Exponentiate (by continuity of $\exp$).

$$
L = e^6.
$$

**Final answer:**

$$
\boxed{\lim_{x \to 0}(1 + 3x)^{2/x} = e^6.}
$$

#### Cross-check via known formula.

$(1 + ax)^{b/x} \to e^{ab}$ as $x \to 0$ (a generalization of $e = \lim(1 + 1/x)^x$). With $a = 3, b = 2$: $e^{ab} = e^6$. ✓

</details>

### Problem 1.2.P9 — Critical Points and Classification

For $f(x) = x^4 - 4x^3 + 4x^2$, find all critical points and classify each as local max, local min, or neither using the second-derivative test.

<details>

<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Compute $f'$.

$$
f'(x) = 4x^3 - 12 x^2 + 8 x = 4x(x^2 - 3x + 2) = 4x(x - 1)(x - 2).
$$

#### Step 2: Set $f' = 0$.

$$
4x(x - 1)(x - 2) = 0 \quad \Longrightarrow \quad x \in \{0, 1, 2\}.
$$

These are the critical points. (Defined everywhere, no nonexistent-derivative points.)

#### Step 3: Compute $f''$.

$$
f''(x) = 12 x^2 - 24 x + 8.
$$

#### Step 4: Evaluate $f''$ at each critical point.

| $x$ | $f''(x)$ | Classification |
|---|---|---|
| $0$ | $0 - 0 + 8 = 8 \gt  0$ | local minimum |
| $1$ | $12 - 24 + 8 = -4 \lt  0$ | local maximum |
| $2$ | $48 - 48 + 8 = 8 \gt  0$ | local minimum |

#### Step 5: Compute $f$ at each.

$f(0) = 0$, $f(1) = 1 - 4 + 4 = 1$, $f(2) = 16 - 32 + 16 = 0$.

So we have **two equal local minima** at $(0, 0)$ and $(2, 0)$, and a **local max** at $(1, 1)$ between them. The function is a quartic "double well." (Useful in physics — Landau-Ginzburg potentials and the like.)

**Final answer:**

$$
\boxed{\text{Local mins at } x = 0, 2 \text{ (both with value } 0\text{); local max at } x = 1 \text{ (value 1).}}
$$

</details>

### Problem 1.2.P10 — Newton's Method on a Pathological Start

Apply Newton's method to $g(x) = x^3 - 2x + 2$ starting from $x_0 = 0$. What happens?

<details>

<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Compute $g'(x)$.

$g'(x) = 3 x^2 - 2$.

#### Step 2: First iteration.

$$
x_1 = x_0 - \frac{g(x_0)}{g'(x_0)} = 0 - \frac{0 - 0 + 2}{0 - 2} = 0 - \frac{2}{-2} = 0 - (-1) = 1.
$$

#### Step 3: Second iteration.

$g(1) = 1 - 2 + 2 = 1$. $g'(1) = 3 - 2 = 1$.

$$
x_2 = 1 - \frac{1}{1} = 0.
$$

#### Step 4: Third iteration.

We're back to $x = 0$. So $x_3 = 1$, $x_4 = 0$, $x_5 = 1$, …

#### Step 5: Diagnosis.

The iteration **cycles** between $0$ and $1$ forever, never converging. This is a famous pathological orbit. (The cubic $g$ has exactly one real root, near $x \approx -1.769$, but the iteration starting at $0$ never reaches it because the tangent geometry traps the iterate in a 2-cycle.)

**Final answer:** Newton's method diverges from $x_0 = 0$ via a 2-cycle $\{0, 1\}$. **Lesson:** Newton's method is *locally* quadratically convergent near a simple root, but *global* convergence requires a starting point in the basin of attraction. Bad starts can cycle, diverge, or land on points where $g'(x_n) = 0$ (which would force division by zero).

</details>

---


## 🔗 12. Cross-Links to the Knowledge Web

- **Backward references:** every limit identity used here (cornerstone $\sin\theta/\theta \to 1$, the $\varepsilon$-$\delta$ definition, limit laws, continuity, EVT) was developed in [1.1 - Limits & Continuity](1.1---Limits-&-Continuity). Re-read §1.1.5–§1.1.6 if any of the proofs feel rushed.
- **Forward references:** the **Fundamental Theorem of Calculus** in [1.3 - Single-Variable Integration](1.3---Single-Variable-Integration) inverts differentiation — every antiderivative of a continuous function on $[a, b]$ differs from $\int_a^x f(t)\,dt$ by at most a constant. The **Mean Value Theorem proved here** is the structural cousin of the **MVT for integrals** in 1.3.
- **Multivariable generalization:** [1.4 - Multivariable Limits & Partial Derivatives](1.4---Multivariable-Limits-&-Partial-Derivatives) generalizes the limit-of-difference-quotient definition to partial derivatives $\partial f/\partial x_i$, gradients $\nabla f$, and total derivatives (Jacobians). The chain rule of §5.5 generalizes to a matrix product of Jacobians.
- **Differential equations:** every ODE in [3.1 - First-Order ODEs Separable & Exact](3.1---First-Order-ODEs-Separable-&-Exact) is an equation involving derivatives. Every solution technique in chapters 3.x ultimately reduces to clever applications of the differentiation rules proved here plus integration.
- **Physics — Kinematics:** in [4.1 - Newtonian Mechanics & Kinematics](4.1---Newtonian-Mechanics-&-Kinematics), **velocity** is $\dot{x} = dx/dt$ and **acceleration** is $\ddot{x} = d^2 x/dt^2$. Newton's second law $F = m\,\ddot{x}$ is a second-order ODE that you'll solve using the techniques here plus integration.
- **Optimization & Machine Learning:** **gradient descent** (used to train every modern neural network) is just iterated negative-gradient steps — *the* application of differentiation outside pure math. Once you have multivariable Chapter 1.4, you'll see this in glorious detail.
- **Numerical analysis:** **Newton's method** (Example E7, Problem P10) is the prototype root-finder. Its descendants — Newton-Raphson, secant method, Halley's method, Householder's methods — all live downstream of the chain rule and Taylor's theorem.
- **Probability:** any density function $p(x)$ has a CDF $F(x) = \int p$ such that $p = F'$. Computing densities from CDFs is *literally* differentiation.

---

## 📚 13. Verified Open-Access Source Material

| Source | Location | Why it's Authoritative |
|---|---|---|
| **MIT 18.01SC, Unit 1 — Differentiation** | [ocw.mit.edu/courses/18-01sc](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/unit-1-differentiation/) | Canonical MIT undergraduate calculus, with full lecture notes and problem sets, hosted on `mit.edu`. Daniel Kleitman et al. |
| **Strang, *Calculus* (3rd ed., free PDF), Ch. 2-4** | [Strang on OCW](https://ocw.mit.edu/ans7870/textbooks/Strang/stranginstruct.htm) | Author taught 18.01/18.06 at MIT for 50+ years; textbook in classroom use since 1991. |
| **APEX Calculus, Ch. 2 — Derivatives** | [apexcalculus.com](https://www.apexcalculus.com/) | Greg Hartman (VMI), CC-BY-NC; widely adopted at U.S. universities; matches the rigor expected here. |
| **Paul Dawkins — *Calculus I, Derivatives*** | [tutorial.math.lamar.edu/calci](https://tutorial.math.lamar.edu/Classes/CalcI/DerivativeIntro.aspx) | Lamar University faculty notes; the most-cited online calculus reference of the past two decades. |
| **3Blue1Brown — *Essence of Calculus*, Chapters 2–7** | [3blue1brown.com/lessons/essence-of-calculus](https://www.3blue1brown.com/lessons/essence-of-calculus) | Grant Sanderson; gold-standard visual intuition for the derivative, chain rule, and Taylor series. Watch *after* working through the algebra below. |
| **LibreTexts — *Mean Value Theorem & L'Hôpital*** | [math.libretexts.org](https://math.libretexts.org/Bookshelves/Calculus/Calculus_(OpenStax)/04:_Applications_of_Derivatives) | Mirror of the OpenStax Calculus chapter on derivative applications; extensive worked examples. |
| **ProofWiki — *Taylor's Theorem (one variable)*** | [proofwiki.org](https://proofwiki.org/wiki/Taylor's_Theorem/One_Variable/Proof_by_Cauchy_Mean_Value_Theorem) | Curated proof database; all proofs come with full inline references. |
| **Wikipedia — *Chain Rule*** | [en.wikipedia.org/wiki/Chain_rule](https://en.wikipedia.org/wiki/Chain_rule) | Curated cross-referenced summary including Carathéodory's bridging-function approach used in §5.5. |

*(Resource summaries above were paraphrased for licensing compliance with each platform's terms of use.)*

---

*Chapter 1.2 — Single-Variable Differentiation. Last reviewed: 2026-05-23. Next chapter: [1.3 - Single-Variable Integration](1.3---Single-Variable-Integration) →*
