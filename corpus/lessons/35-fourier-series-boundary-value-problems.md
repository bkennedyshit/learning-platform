---
title: "Fourier Series Boundary Value Problems"
subject: "Ordinary & Partial Differential Equations"
catalog: advanced
audience_tier: higher-education
chapter: "3.5"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 3.5 — Fourier Series & Boundary Value Problems

> *"Fourier's theorem is not only one of the most beautiful results of modern analysis, but it may be said to furnish an indispensable instrument in the treatment of nearly every recondite question in modern physics."* — Lord Kelvin

Fourier series decompose periodic functions into sums of sines and cosines — the natural eigenfunctions of the second-derivative operator with periodic boundary conditions. This chapter develops the theory from Sturm-Liouville eigenvalue problems, proves convergence, and establishes the orthogonality relations that make coefficient computation possible. These tools are essential prerequisites for solving PDEs via separation of variables in [3.7 - The Heat & Wave PDEs - Separation of Variables](3.7---The-Heat-&-Wave-PDEs---Separation-of-Variables).

---

## 🎯 Learning Objectives

1. State and prove the orthogonality of $\{\sin(n\pi x/L), \cos(n\pi x/L)\}$ on $[-L, L]$.
2. Derive the Euler-Fourier formulas for $a_n$ and $b_n$.
3. Compute Fourier series for piecewise-smooth functions.
4. Distinguish Fourier sine series, cosine series, and full series (odd/even extensions).
5. State the Sturm-Liouville eigenvalue problem and its spectral properties.
6. Apply Parseval's theorem to relate function norms to coefficient norms.
7. Understand pointwise and $L^2$ convergence of Fourier series.

---

## 🖼️ Visual Anchor — Fourier Harmonics Converging to Square Wave

![math-03__3.5-fig1](math-03__3.5-fig1.svg)

---

## 📚 1. Definitions

### Definition 3.5.1 — Fourier Series

The **Fourier series** of a function $f(x)$ on $[-L, L]$ is:

$$
f(x) \sim \frac{a_0}{2} + \sum_{n=1}^{\infty}\left[a_n\cos\frac{n\pi x}{L} + b_n\sin\frac{n\pi x}{L}\right],
$$

where the **Fourier coefficients** are:

$$
a_n = \frac{1}{L}\int_{-L}^{L} f(x)\cos\frac{n\pi x}{L}\,dx, \quad b_n = \frac{1}{L}\int_{-L}^{L} f(x)\sin\frac{n\pi x}{L}\,dx.
$$

### Definition 3.5.2 — Sturm-Liouville Problem

A **Sturm-Liouville eigenvalue problem** is:

$$
\frac{d}{dx}\left[p(x)\frac{dy}{dx}\right] + [q(x) + \lambda w(x)]y = 0, \quad x \in [a,b],
$$

with boundary conditions at $x = a$ and $x = b$, where $p(x) > 0$, $w(x) > 0$ (weight function).

### Definition 3.5.3 — Orthogonality (with Weight)

Functions $\phi_m$ and $\phi_n$ are **orthogonal** with respect to weight $w(x)$ on $[a,b]$ if:

$$
\langle\phi_m, \phi_n\rangle_w = \int_a^b \phi_m(x)\,\phi_n(x)\,w(x)\,dx = 0 \quad (m \neq n).
$$

### Definition 3.5.4 — Parseval's Theorem

For $f \in L^2[-L,L]$ with Fourier coefficients $a_n, b_n$:

$$
\frac{1}{L}\int_{-L}^{L}|f(x)|^2\,dx = \frac{a_0^2}{2} + \sum_{n=1}^{\infty}(a_n^2 + b_n^2).
$$

---

## 📐 2. Axioms / Postulates

**Postulate 3.5.P1 (Completeness of Trigonometric System):** The set $\{1, \cos(n\pi x/L), \sin(n\pi x/L)\}_{n=1}^{\infty}$ is complete in $L^2[-L,L]$: every square-integrable function can be approximated arbitrarily well in the $L^2$ norm.

**Postulate 3.5.P2 (Dirichlet Conditions):** If $f$ is piecewise smooth on $[-L,L]$, the Fourier series converges pointwise to $\frac{1}{2}[f(x^+) + f(x^-)]$ at every point.

---

## 🛡️ 3. Lemmas

### Lemma 3.5.1 — Orthogonality of Sine and Cosine

On $[-L, L]$:

$$
\int_{-L}^{L}\cos\frac{m\pi x}{L}\cos\frac{n\pi x}{L}\,dx = \begin{cases}0 & m\neq n\\L & m = n \neq 0\\2L & m = n = 0\end{cases}
$$

$$
\int_{-L}^{L}\sin\frac{m\pi x}{L}\sin\frac{n\pi x}{L}\,dx = \begin{cases}0 & m\neq n\\L & m = n\end{cases}
$$

$$
\int_{-L}^{L}\cos\frac{m\pi x}{L}\sin\frac{n\pi x}{L}\,dx = 0 \quad \forall m, n.
$$

**Proof (cos-cos case, $m \neq n$).** Use the product-to-sum identity:

$$
\cos A\cos B = \frac{1}{2}[\cos(A-B) + \cos(A+B)].
$$

$$
\int_{-L}^{L}\cos\frac{m\pi x}{L}\cos\frac{n\pi x}{L}\,dx = \frac{1}{2}\int_{-L}^{L}\left[\cos\frac{(m-n)\pi x}{L} + \cos\frac{(m+n)\pi x}{L}\right]dx.
$$

Each integral evaluates to $\frac{L}{(m\pm n)\pi}\sin\frac{(m\pm n)\pi x}{L}\Big|_{-L}^{L} = 0$ since $\sin(k\pi) = 0$ for integer $k$. $\blacksquare$

---

## 👑 4. Theorems

### Theorem 3.5.1 — Euler-Fourier Coefficient Derivation

The Fourier coefficients are uniquely determined by the orthogonality relations. Specifically, multiplying $f(x) = \frac{a_0}{2} + \sum a_n\cos + \sum b_n\sin$ by $\cos(m\pi x/L)$ and integrating term-by-term yields $a_m$ due to orthogonality.

### Theorem 3.5.2 — Sturm-Liouville Spectral Theorem

The eigenvalues $\lambda_1 < \lambda_2 < \cdots$ of a regular Sturm-Liouville problem are real, countably infinite, and $\lambda_n \to \infty$. The eigenfunctions $\{\phi_n\}$ form a complete orthogonal set in $L^2_w[a,b]$.

---

## ✍️ 5. Proofs / Derivations

### 5.1 Derivation of Fourier Coefficients

**Step 1.** Assume $f(x) = \frac{a_0}{2} + \sum_{n=1}^{\infty}[a_n\cos(n\pi x/L) + b_n\sin(n\pi x/L)]$.

**Step 2.** To find $a_m$ ($m \geq 1$), multiply both sides by $\cos(m\pi x/L)$ and integrate over $[-L,L]$:

$$
\int_{-L}^{L}f(x)\cos\frac{m\pi x}{L}\,dx = \frac{a_0}{2}\underbrace{\int_{-L}^{L}\cos\frac{m\pi x}{L}\,dx}_{=0} + \sum_{n=1}^{\infty}a_n\underbrace{\int_{-L}^{L}\cos\frac{n\pi x}{L}\cos\frac{m\pi x}{L}\,dx}_{=L\delta_{mn}} + \sum_{n=1}^{\infty}b_n\underbrace{\int_{-L}^{L}\sin\frac{n\pi x}{L}\cos\frac{m\pi x}{L}\,dx}_{=0}.
$$

**Step 3.** All terms vanish except $n = m$:

$$
\int_{-L}^{L}f(x)\cos\frac{m\pi x}{L}\,dx = a_m \cdot L \implies a_m = \frac{1}{L}\int_{-L}^{L}f(x)\cos\frac{m\pi x}{L}\,dx. \quad \blacksquare
$$

---

## 🧮 6. Worked Examples

### Example 3.5.E1 — Fourier Series of a Square Wave

Find the Fourier series of $f(x) = \begin{cases}1 & 0 < x < \pi\\-1 & -\pi < x < 0\end{cases}$ on $[-\pi, \pi]$.

**Step 1.** $f$ is odd, so $a_n = 0$ for all $n \geq 0$.

**Step 2.** Compute $b_n$:

$$
b_n = \frac{1}{\pi}\int_{-\pi}^{\pi}f(x)\sin(nx)\,dx = \frac{2}{\pi}\int_0^{\pi}\sin(nx)\,dx = \frac{2}{\pi}\left[-\frac{\cos(nx)}{n}\right]_0^{\pi}.
$$

$$
= \frac{2}{\pi}\cdot\frac{1-\cos(n\pi)}{n} = \frac{2}{n\pi}[1-(-1)^n] = \begin{cases}\frac{4}{n\pi} & n\text{ odd}\\0 & n\text{ even}\end{cases}.
$$

**Step 3.** Fourier series:

$$
f(x) = \frac{4}{\pi}\sum_{k=0}^{\infty}\frac{\sin((2k+1)x)}{2k+1} = \frac{4}{\pi}\left[\sin x + \frac{\sin 3x}{3} + \frac{\sin 5x}{5} + \cdots\right].
$$

---

### Example 3.5.E2 — Fourier Cosine Series (Even Extension)

Find the Fourier cosine series of $f(x) = x$ on $[0, L]$.

**Step 1.** $a_0 = \frac{2}{L}\int_0^L x\,dx = \frac{2}{L}\cdot\frac{L^2}{2} = L$.

**Step 2.** For $n \geq 1$, integrate by parts with $u = x$, $dv = \cos(n\pi x/L)\,dx$:

$$
a_n = \frac{2}{L}\int_0^L x\cos\frac{n\pi x}{L}\,dx = \frac{2}{L}\left[\frac{xL}{n\pi}\sin\frac{n\pi x}{L}\Big|_0^L - \frac{L}{n\pi}\int_0^L\sin\frac{n\pi x}{L}\,dx\right].
$$

The boundary term vanishes ($\sin(n\pi) = 0$). The remaining integral:

$$
= \frac{2}{L}\cdot\left(-\frac{L}{n\pi}\right)\left[\frac{-L}{n\pi}\cos\frac{n\pi x}{L}\right]_0^L = \frac{2L}{n^2\pi^2}[\cos(n\pi) - 1] = \frac{2L}{n^2\pi^2}[(-1)^n - 1].
$$

So $a_n = 0$ for even $n$, and $a_n = -\frac{4L}{n^2\pi^2}$ for odd $n$.

---

### Example 3.5.E3 — Parseval's Identity Application

Using the square wave from E1, apply Parseval's theorem to evaluate $\sum_{k=0}^{\infty}\frac{1}{(2k+1)^2}$.

**Step 1.** $\frac{1}{\pi}\int_{-\pi}^{\pi}|f(x)|^2\,dx = \frac{1}{\pi}\cdot 2\pi = 2$.

**Step 2.** Parseval: $2 = \sum_{n=1}^{\infty}b_n^2 = \sum_{k=0}^{\infty}\frac{16}{(2k+1)^2\pi^2}$.

**Step 3.** Solve: $\sum_{k=0}^{\infty}\frac{1}{(2k+1)^2} = \frac{2\pi^2}{16} = \frac{\pi^2}{8}$.

This is the famous result: $1 + \frac{1}{9} + \frac{1}{25} + \frac{1}{49} + \cdots = \frac{\pi^2}{8}$.

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- [3.7 - The Heat & Wave PDEs - Separation of Variables](3.7---The-Heat-&-Wave-PDEs---Separation-of-Variables) — Fourier series provide the solution coefficients
- [3.2 - Second-Order Linear Homogeneous ODEs](3.2---Second-Order-Linear-Homogeneous-ODEs) — Sturm-Liouville is the eigenvalue problem for differential operators
- [2.6 - Eigenvalues Eigenvectors & Diagonalization](2.6---Eigenvalues-Eigenvectors-&-Diagonalization) — finite-dimensional analogue of spectral decomposition

### External References
- **MIT OCW 18.03SC**, Unit on Fourier Series
- **Jiří Lebl**, *Notes on Diffy Qs*, Ch. 4 (Fourier Series and PDEs)
- **3Blue1Brown**, "But what is a Fourier series?" (exceptional visual intuition)
- **Elias Stein & Rami Shakarchi**, *Fourier Analysis* (Princeton Lectures in Analysis, Vol. 1)

---



---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — Fourier Series of the Sawtooth Wave

Find the Fourier series of $f(x) = x$ on $(-\pi, \pi)$ with period $2\pi$.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Determine symmetry

$f(x) = x$ is an **odd function** ($f(-x) = -x = -f(x)$). Therefore all cosine coefficients vanish: $a_0 = 0$ and $a_n = 0$ for all $n$.

#### Step 2: Compute the sine coefficients

$$
b_n = \frac{1}{\pi}\int_{-\pi}^{\pi} x\sin(nx)\,dx.
$$

Since $x\sin(nx)$ is even (odd × odd = even):

$$
b_n = \frac{2}{\pi}\int_0^{\pi} x\sin(nx)\,dx.
$$

#### Step 3: Integration by parts

Let $u = x$, $dv = \sin(nx)\,dx$. Then $du = dx$, $v = -\cos(nx)/n$.

$$
\int_0^{\pi} x\sin(nx)\,dx = \left[-\frac{x\cos(nx)}{n}\right]_0^{\pi} + \frac{1}{n}\int_0^{\pi}\cos(nx)\,dx.
$$

$$
= -\frac{\pi\cos(n\pi)}{n} + \frac{1}{n}\left[\frac{\sin(nx)}{n}\right]_0^{\pi} = -\frac{\pi(-1)^n}{n} + 0.
$$

#### Step 4: Assemble the coefficient

$$
b_n = \frac{2}{\pi} \cdot \left(-\frac{\pi(-1)^n}{n}\right) = \frac{-2(-1)^n}{n} = \frac{2(-1)^{n+1}}{n}.
$$

**Final Answer:**

$$
f(x) = x = \sum_{n=1}^{\infty} \frac{2(-1)^{n+1}}{n}\sin(nx) = 2\left(\sin x - \frac{\sin 2x}{2} + \frac{\sin 3x}{3} - \cdots\right).
$$

**Parseval check:** $\frac{1}{\pi}\int_{-\pi}^{\pi}x^2\,dx = \frac{2\pi^2}{3}$. And $\sum b_n^2 = 4\sum \frac{1}{n^2} = 4 \cdot \frac{\pi^2}{6} = \frac{2\pi^2}{3}$. ✓

</details>

### Example 8.2 — Half-Range Cosine Expansion (Heat Equation Initial Condition)

A rod of length $L = 1$ has initial temperature $f(x) = x(1-x)$ for $0 \leq x \leq 1$. Find the half-range cosine expansion (needed for insulated-end boundary conditions).

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: The half-range cosine series formula

$$
f(x) = \frac{a_0}{2} + \sum_{n=1}^{\infty} a_n \cos(n\pi x), \quad a_n = 2\int_0^1 f(x)\cos(n\pi x)\,dx.
$$

#### Step 2: Compute $a_0$

$$
a_0 = 2\int_0^1 x(1-x)\,dx = 2\int_0^1 (x - x^2)\,dx = 2\left[\frac{x^2}{2} - \frac{x^3}{3}\right]_0^1 = 2\left(\frac{1}{2} - \frac{1}{3}\right) = 2 \cdot \frac{1}{6} = \frac{1}{3}.
$$

#### Step 3: Compute $a_n$ for $n \geq 1$

$$
a_n = 2\int_0^1 (x - x^2)\cos(n\pi x)\,dx = 2\left[\int_0^1 x\cos(n\pi x)\,dx - \int_0^1 x^2\cos(n\pi x)\,dx\right].
$$

**First integral** — by parts with $u = x$, $dv = \cos(n\pi x)\,dx$:

$$
\int_0^1 x\cos(n\pi x)\,dx = \left[\frac{x\sin(n\pi x)}{n\pi}\right]_0^1 - \frac{1}{n\pi}\int_0^1 \sin(n\pi x)\,dx.
$$

$$
= 0 + \frac{1}{n\pi}\left[\frac{\cos(n\pi x)}{n\pi}\right]_0^1 = \frac{1}{n^2\pi^2}[\cos(n\pi) - 1] = \frac{(-1)^n - 1}{n^2\pi^2}.
$$

**Second integral** — by parts twice with $u = x^2$:

$$
\int_0^1 x^2\cos(n\pi x)\,dx = \left[\frac{x^2\sin(n\pi x)}{n\pi}\right]_0^1 - \frac{2}{n\pi}\int_0^1 x\sin(n\pi x)\,dx.
$$

The boundary term vanishes. For $\int_0^1 x\sin(n\pi x)\,dx$, integrate by parts again:

$$
\int_0^1 x\sin(n\pi x)\,dx = \left[-\frac{x\cos(n\pi x)}{n\pi}\right]_0^1 + \frac{1}{n\pi}\int_0^1\cos(n\pi x)\,dx = -\frac{(-1)^n}{n\pi} + 0 = \frac{-(-1)^n}{n\pi}.
$$

So:

$$
\int_0^1 x^2\cos(n\pi x)\,dx = -\frac{2}{n\pi}\cdot\frac{-(-1)^n}{n\pi} = \frac{2(-1)^n}{n^2\pi^2}.
$$

#### Step 4: Combine

$$
a_n = 2\left[\frac{(-1)^n - 1}{n^2\pi^2} - \frac{2(-1)^n}{n^2\pi^2}\right] = \frac{2}{n^2\pi^2}\left[(-1)^n - 1 - 2(-1)^n\right] = \frac{2}{n^2\pi^2}\left[-(-1)^n - 1\right].
$$

$$
a_n = \frac{-2[1 + (-1)^n]}{n^2\pi^2}.
$$

When $n$ is odd: $1 + (-1)^n = 0$, so $a_n = 0$.

When $n$ is even ($n = 2m$): $1 + 1 = 2$, so $a_{2m} = \frac{-4}{(2m)^2\pi^2} = \frac{-1}{m^2\pi^2}$.

**Final Answer:**

$$
x(1-x) = \frac{1}{6} - \frac{1}{\pi^2}\sum_{m=1}^{\infty}\frac{\cos(2m\pi x)}{m^2} = \frac{1}{6} - \frac{1}{\pi^2}\left(\cos 2\pi x + \frac{\cos 4\pi x}{4} + \frac{\cos 6\pi x}{9} + \cdots\right).
$$

Setting $x = 0$: $0 = \frac{1}{6} - \frac{1}{\pi^2}\sum_{m=1}^{\infty}\frac{1}{m^2}$, giving $\sum \frac{1}{m^2} = \frac{\pi^2}{6}$ (Basel problem). ✓

</details>

### Example 8.3 — Sturm–Liouville Eigenvalue Problem with Mixed BCs

Solve the eigenvalue problem:

$$
y'' + \lambda y = 0, \quad y(0) = 0, \quad y'(L) = 0.
$$

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Case $\lambda \lt  0$ (write $\lambda = -\mu^2$, $\mu \gt  0$)

$y'' - \mu^2 y = 0 \implies y = C_1 e^{\mu x} + C_2 e^{-\mu x}$ (or equivalently $A\cosh\mu x + B\sinh\mu x$).

BC $y(0) = 0$: $A = 0$, so $y = B\sinh\mu x$.

BC $y'(L) = 0$: $y' = B\mu\cosh\mu x$, so $B\mu\cosh(\mu L) = 0$. Since $\cosh \gt  0$ always and $\mu \gt  0$, we need $B = 0$. Trivial solution only.

#### Step 2: Case $\lambda = 0$

$y'' = 0 \implies y = Ax + B$. BC $y(0) = 0$: $B = 0$. BC $y'(L) = 0$: $A = 0$. Trivial.

#### Step 3: Case $\lambda \gt  0$ (write $\lambda = \mu^2$, $\mu \gt  0$)

$y = A\cos\mu x + B\sin\mu x$.

BC $y(0) = 0$: $A = 0$, so $y = B\sin\mu x$.

BC $y'(L) = 0$: $y' = B\mu\cos\mu x$, so $B\mu\cos(\mu L) = 0$. For nontrivial $B \neq 0$:

$$
\cos(\mu L) = 0 \implies \mu L = \frac{(2n-1)\pi}{2}, \quad n = 1, 2, 3, \ldots
$$

#### Step 4: Eigenvalues and eigenfunctions

$$
\mu_n = \frac{(2n-1)\pi}{2L}.
$$

**Final Answer:**

$$
\lambda_n = \mu_n^2 = \frac{(2n-1)^2\pi^2}{4L^2}, \qquad y_n(x) = \sin\left(\frac{(2n-1)\pi x}{2L}\right), \quad n = 1, 2, 3, \ldots
$$

These eigenfunctions are orthogonal on $[0, L]$ with weight 1:

$$
\int_0^L \sin\frac{(2n-1)\pi x}{2L}\sin\frac{(2m-1)\pi x}{2L}\,dx = \frac{L}{2}\delta_{nm}.
$$

**Physical interpretation:** This BVP models a vibrating string fixed at $x = 0$ (Dirichlet) and free at $x = L$ (Neumann). The eigenfrequencies are odd multiples of the fundamental — only odd harmonics are present (like a clarinet).

</details>

### Example 8.4 — Complex Fourier Series and Frequency Spectrum

Find the complex Fourier series of the periodic pulse train: $f(t) = 1$ for $|t| < d$ and $f(t) = 0$ for $d < |t| < T/2$, with period $T$.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Complex Fourier coefficient formula

$$
c_n = \frac{1}{T}\int_{-T/2}^{T/2} f(t)\,e^{-in\omega_0 t}\,dt, \quad \omega_0 = \frac{2\pi}{T}.
$$

Since $f(t) = 1$ only on $(-d, d)$:

$$
c_n = \frac{1}{T}\int_{-d}^{d} e^{-in\omega_0 t}\,dt.
$$

#### Step 2: Evaluate the integral

For $n \neq 0$:

$$
c_n = \frac{1}{T}\left[\frac{e^{-in\omega_0 t}}{-in\omega_0}\right]_{-d}^{d} = \frac{1}{T}\cdot\frac{e^{-in\omega_0 d} - e^{in\omega_0 d}}{-in\omega_0}.
$$

$$
= \frac{1}{T}\cdot\frac{-2i\sin(n\omega_0 d)}{-in\omega_0} = \frac{2\sin(n\omega_0 d)}{n\omega_0 T} = \frac{2\sin(n\omega_0 d)}{2n\pi} = \frac{\sin(n\omega_0 d)}{n\pi}.
$$

For $n = 0$: $c_0 = \frac{1}{T}\int_{-d}^d 1\,dt = \frac{2d}{T}$.

#### Step 3: Express using the sinc function

Define $\text{sinc}(x) = \sin(\pi x)/(\pi x)$. Then with $\omega_0 d = 2\pi d/T$:

$$
c_n = \frac{2d}{T}\cdot\frac{\sin(n\pi \cdot 2d/T)}{n\pi \cdot 2d/T} = \frac{2d}{T}\,\text{sinc}\left(\frac{2nd}{T}\right).
$$

**Final Answer:**

$$
f(t) = \sum_{n=-\infty}^{\infty} c_n\,e^{in\omega_0 t}, \quad c_n = \frac{2d}{T}\,\text{sinc}\left(\frac{2nd}{T}\right).
$$

The frequency spectrum $|c_n|$ has the characteristic sinc envelope, with zeros at $n = T/(2d), 2T/(2d), \ldots$ The narrower the pulse ($d \to 0$), the wider the spectrum — this is the time-frequency uncertainty principle.

</details>



---

## 📘 9. Appendix: Extended Derivations & Special Cases

### 9.1 Pointwise Convergence of Fourier Series — Dirichlet's Theorem

The question of when and how a Fourier series converges to its generating function is subtle. The fundamental result is:

**Theorem (Dirichlet, 1829).** Let $f$ be a periodic function with period $2L$ that is piecewise smooth on $[-L, L]$ (meaning $f$ and $f'$ are piecewise continuous with at most finitely many jump discontinuities). Then the Fourier series of $f$ converges at every point $x$ to:

$$
\frac{f(x^+) + f(x^-)}{2},
$$

where $f(x^+) = \lim_{t \to x^+} f(t)$ and $f(x^-) = \lim_{t \to x^-} f(t)$.

**Consequences:**
1. At points where $f$ is continuous, the series converges to $f(x)$.
2. At jump discontinuities, the series converges to the midpoint of the jump.
3. At the endpoints of the interval (where the periodic extension may have a jump), the series converges to the average of the left and right limits.

**The Gibbs phenomenon.** Near a jump discontinuity of height $h$, the partial sums $S_N(x)$ overshoot by approximately $9\%$ of the jump height:

$$
\max_{x \text{ near jump}} |S_N(x) - f(x)| \to \frac{h}{\pi}\int_0^{\pi}\frac{\sin t}{t}\,dt - \frac{h}{2} \approx 0.0895\,h.
$$

This overshoot does NOT diminish as $N \to \infty$ — it merely becomes narrower. The Gibbs phenomenon is intrinsic to pointwise convergence of Fourier series at discontinuities.

**Uniform convergence.** If $f$ is continuous and periodic with a piecewise continuous derivative, then the Fourier series converges uniformly (no Gibbs phenomenon). The rate of convergence depends on smoothness: if $f \in C^k$, then $|a_n|, |b_n| = O(1/n^{k+1})$.

**$L^2$ convergence (Parseval).** Regardless of pointwise behavior, the Fourier series always converges in the $L^2$ norm:

$$
\lim_{N\to\infty}\int_{-L}^{L}\left|f(x) - S_N(x)\right|^2 dx = 0.
$$

This is the content of the Riesz–Fischer theorem: $L^2[-L,L]$ is a complete Hilbert space with the Fourier basis as an orthonormal basis.

*Reference: Stein & Shakarchi, Fourier Analysis (Princeton, 2003), Ch. 2; MIT OCW 18.03, supplementary notes on convergence.*

### 9.2 Parseval's Theorem and Spectral Energy

**Theorem (Parseval/Plancherel).** If $f$ has Fourier coefficients $a_0, a_n, b_n$, then:

$$
\frac{1}{L}\int_{-L}^{L}|f(x)|^2\,dx = \frac{a_0^2}{2} + \sum_{n=1}^{\infty}(a_n^2 + b_n^2).
$$

In complex form with $c_n$:

$$
\frac{1}{2L}\int_{-L}^{L}|f(x)|^2\,dx = \sum_{n=-\infty}^{\infty}|c_n|^2.
$$

**Physical interpretation.** The left side is the average power (or energy per period) of the signal $f$. The right side decomposes this into contributions from each harmonic. The quantity $|c_n|^2$ is the **power spectral density** at frequency $n\omega_0$ — it tells you how much energy lives at each frequency.

**Proof sketch.** Start from $\|f - S_N\|^2 \geq 0$ (Bessel's inequality), expand, and use orthogonality:

$$
\int|f|^2\,dx - 2\sum_{n} |c_n|^2 \cdot 2L + \sum_n |c_n|^2 \cdot 2L \geq 0.
$$

The completeness of the Fourier basis (every $L^2$ function can be approximated arbitrarily well) upgrades Bessel's inequality to equality — this is Parseval's theorem.

**Application: Evaluating series.** From the Fourier series of $f(x) = x$ on $(-\pi, \pi)$ (Example 8.1), Parseval gives:

$$
\frac{1}{\pi}\int_{-\pi}^{\pi}x^2\,dx = \sum_{n=1}^{\infty}\frac{4}{n^2} \implies \frac{2\pi^2}{3} = 4\sum\frac{1}{n^2} \implies \sum_{n=1}^{\infty}\frac{1}{n^2} = \frac{\pi^2}{6}.
$$

This is Euler's solution to the Basel problem via Fourier analysis.

*Reference: Jiří Lebl, Notes on Diffy Qs, §4.3; Strang, Computational Science and Engineering, §4.2.*

### 9.3 Sturm–Liouville Theory — The General Eigenvalue Framework

The Fourier sine/cosine eigenfunctions are special cases of a much broader theory. A **regular Sturm–Liouville problem** has the form:

$$
\frac{d}{dx}\left[p(x)\frac{dy}{dx}\right] + q(x)y + \lambda w(x)y = 0, \quad a < x < b,
$$

with boundary conditions $\alpha_1 y(a) + \alpha_2 y'(a) = 0$ and $\beta_1 y(b) + \beta_2 y'(b) = 0$, where $p(x) > 0$, $w(x) > 0$ (the weight function) on $[a, b]$.

**Fundamental results:**
1. **Discrete spectrum.** There exist countably many eigenvalues $\lambda_1 < \lambda_2 < \lambda_3 < \cdots$ with $\lambda_n \to \infty$.
2. **Orthogonality.** Eigenfunctions $y_m, y_n$ corresponding to distinct eigenvalues are orthogonal with respect to the weight $w$:

$$
\int_a^b y_m(x)\,y_n(x)\,w(x)\,dx = 0 \quad (m \neq n).
$$

3. **Completeness.** The eigenfunctions form a complete orthogonal basis for $L^2_w[a,b]$: any piecewise smooth function can be expanded as $f(x) = \sum c_n y_n(x)$ with $c_n = \frac{\langle f, y_n \rangle_w}{\|y_n\|_w^2}$.

4. **Oscillation theorem.** The $n$th eigenfunction $y_n$ has exactly $n-1$ zeros in the open interval $(a, b)$.

**Examples of Sturm–Liouville problems:**

| Equation | Weight $w$ | Eigenfunctions | Context |
|---|---|---|---|
| $y'' + \lambda y = 0$ | 1 | $\sin(n\pi x/L)$ | Vibrating string |
| $(1-x^2)y'' - 2xy' + \lambda y = 0$ | 1 | Legendre polynomials $P_n(x)$ | Spherical harmonics |
| $xy'' + y' + \lambda xy = 0$ | 1 | Bessel functions $J_0(\sqrt{\lambda}\,x)$ | Circular membrane |
| $e^{-x^2}y'' - 2xe^{-x^2}y' + \lambda e^{-x^2}y = 0$ | $e^{-x^2}$ | Hermite polynomials | Quantum harmonic oscillator |

The Sturm–Liouville framework unifies all these "special function" eigenvalue problems under a single abstract theory. It is the infinite-dimensional analogue of the spectral theorem for symmetric matrices: the differential operator $\mathcal{L}[y] = -(py')'/w + q/w$ is self-adjoint with respect to the $w$-weighted inner product, and its eigenfunctions diagonalize it.

*Reference: Haberman, Applied Partial Differential Equations (Pearson, 2013), Ch. 5; MIT OCW 18.303, Lecture notes on Sturm–Liouville theory.*

---



### 9.4 The Fourier Transform as the Limit of Fourier Series

As the period $T \to \infty$, the Fourier series transitions into the Fourier transform. This limiting process illuminates the relationship between discrete and continuous spectra.

**Setup.** For a function $f$ with period $2L$, the complex Fourier series is:

$$
f(x) = \sum_{n=-\infty}^{\infty}c_n\,e^{in\pi x/L}, \quad c_n = \frac{1}{2L}\int_{-L}^{L}f(x)\,e^{-in\pi x/L}\,dx.
$$

Define $\omega_n = n\pi/L$ (discrete frequencies) and $\Delta\omega = \pi/L$ (frequency spacing). Then:

$$
f(x) = \sum_{n=-\infty}^{\infty}\left(\frac{1}{2\pi}\int_{-L}^{L}f(y)\,e^{-i\omega_n y}\,dy\right)e^{i\omega_n x}\,\Delta\omega.
$$

**Take $L \to \infty$.** The sum becomes a Riemann integral over $\omega$, and the inner integral extends to $(-\infty, \infty)$:

$$
f(x) = \frac{1}{2\pi}\int_{-\infty}^{\infty}\left(\int_{-\infty}^{\infty}f(y)\,e^{-i\omega y}\,dy\right)e^{i\omega x}\,d\omega.
$$

Defining $\hat{f}(\omega) = \int_{-\infty}^{\infty}f(x)e^{-i\omega x}\,dx$ (the Fourier transform), we get the inversion formula:

$$
f(x) = \frac{1}{2\pi}\int_{-\infty}^{\infty}\hat{f}(\omega)\,e^{i\omega x}\,d\omega.
$$

**Physical interpretation of the transition:**
- **Periodic functions** (Fourier series): discrete spectrum, energy concentrated at harmonics $n\omega_0$.
- **Non-periodic, $L^1$ functions** (Fourier transform): continuous spectrum, energy distributed over all frequencies.
- **The Parseval/Plancherel theorem** generalizes: $\int|f(x)|^2\,dx = \frac{1}{2\pi}\int|\hat{f}(\omega)|^2\,d\omega$.

This transition is fundamental in signal processing: a periodic signal has a line spectrum (discrete frequencies), while a transient signal has a continuous spectrum. The Fourier series coefficients $c_n$ become the spectral density $\hat{f}(\omega)$.

*Reference: Stein & Shakarchi, Fourier Analysis (Princeton, 2003), Ch. 5; Strang, Computational Science and Engineering, §4.1.*

### 9.5 Bessel's Inequality and Completeness

**Bessel's inequality** states that for any $f \in L^2[-L, L]$ and any orthonormal system $\{\phi_n\}$:

$$
\sum_{n=1}^{N}|\langle f, \phi_n\rangle|^2 \leq \|f\|^2 \quad \text{for all } N.
$$

This says the "energy" captured by the first $N$ Fourier modes never exceeds the total energy of $f$.

**Proof.** Let $S_N = \sum_{n=1}^N c_n\phi_n$ with $c_n = \langle f, \phi_n\rangle$. Then:

$$
0 \leq \|f - S_N\|^2 = \|f\|^2 - 2\text{Re}\langle f, S_N\rangle + \|S_N\|^2 = \|f\|^2 - 2\sum|c_n|^2 + \sum|c_n|^2 = \|f\|^2 - \sum_{n=1}^N|c_n|^2.
$$

Therefore $\sum|c_n|^2 \leq \|f\|^2$. $\blacksquare$

**Completeness** means Bessel's inequality becomes an equality (Parseval's identity):

$$
\sum_{n=1}^{\infty}|c_n|^2 = \|f\|^2.
$$

Equivalently: $\|f - S_N\| \to 0$ as $N \to \infty$ (the partial sums converge to $f$ in the $L^2$ norm). A complete orthonormal system is called an **orthonormal basis** for $L^2$.

The trigonometric system $\{1/\sqrt{2L}, \cos(n\pi x/L)/\sqrt{L}, \sin(n\pi x/L)/\sqrt{L}\}$ is complete in $L^2[-L,L]$ — this is the deep content of Fourier analysis, proved via the Stone–Weierstrass theorem or the theory of self-adjoint operators.

*Reference: Kreyszig, Introductory Functional Analysis with Applications (Wiley, 1978), §3.5; Stein & Shakarchi, Ch. 3.*

---



### 9.6 Gibbs Phenomenon — Quantitative Analysis

At a jump discontinuity of height $h$, the $N$th partial sum of the Fourier series overshoots by a fixed percentage that does not diminish as $N \to \infty$.

**Quantitative result.** Near a jump at $x = x_0$ where $f(x_0^+) - f(x_0^-) = h$, the maximum of $S_N(x)$ approaches:

$$
S_N^{\max} \to \frac{f(x_0^+) + f(x_0^-)}{2} + \frac{h}{2}\left(\frac{2}{\pi}\int_0^{\pi}\frac{\sin t}{t}\,dt - 1\right) \approx \frac{f(x_0^+) + f(x_0^-)}{2} + 0.0895\,h.
$$

The integral $\text{Si}(\pi) = \int_0^{\pi}\frac{\sin t}{t}\,dt \approx 1.8519$, giving the overshoot factor $(2\text{Si}(\pi)/\pi - 1)/2 \approx 8.95\%$ of the jump height.

**Practical implications:**
- In signal processing, Gibbs ringing causes artifacts near sharp transitions (edges in images, transients in audio).
- **Sigma factors** (Lanczos, Fejér) multiply the Fourier coefficients by a window function that suppresses the overshoot at the cost of slightly reduced resolution.
- The Fejér means $\sigma_N = \frac{1}{N}\sum_{k=0}^{N-1}S_k$ converge uniformly to $f$ at continuity points and to the midpoint at jumps — without any overshoot.

*Reference: Jerri, The Gibbs Phenomenon in Fourier Analysis (Springer, 1998); Stein & Shakarchi, Fourier Analysis, §2.4.*

---



### 9.7 Discrete Fourier Transform and the FFT Connection

The **Discrete Fourier Transform (DFT)** is the computational workhorse that evaluates Fourier coefficients numerically. For $N$ equally-spaced samples $f_0, f_1, \ldots, f_{N-1}$:

$$
\hat{f}_k = \sum_{j=0}^{N-1} f_j\,e^{-2\pi ijk/N}, \quad k = 0, 1, \ldots, N-1.
$$

The inverse is $f_j = \frac{1}{N}\sum_{k=0}^{N-1}\hat{f}_k\,e^{2\pi ijk/N}$.

The **Fast Fourier Transform (FFT)** computes the DFT in $O(N\log N)$ operations instead of $O(N^2)$ — one of the most important algorithms in scientific computing. It exploits the recursive structure: a DFT of size $N$ splits into two DFTs of size $N/2$ (Cooley–Tukey, 1965).

The DFT approximates the continuous Fourier coefficients: $\hat{f}_k \approx N\,c_k$ where $c_k$ is the $k$th complex Fourier coefficient. The approximation is exact for band-limited functions sampled above the Nyquist rate ($N > 2f_{\max}$) — this is the Shannon sampling theorem.

*Reference: Strang, Computational Science and Engineering, §4.3; Oppenheim & Schafer, Discrete-Time Signal Processing, Ch. 8.*

---
