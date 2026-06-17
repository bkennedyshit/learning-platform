---
title: "Laplace Transforms & Transfer Functions"
subject: "Control Theory & Systems Engineering"
catalog: advanced
audience_tier: higher-education
chapter: "11.1"
type: chapter-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 11.1 — Laplace Transforms & Transfer Functions

> *"The transfer function is the DNA of a linear system — it encodes every dynamic behavior in a single rational expression of the complex variable s."*
> — Hendrik Bode

The Laplace transform converts linear ordinary differential equations with constant coefficients into algebraic equations in the complex frequency variable $s$. This algebraic representation — the **transfer function** — becomes the universal language of control engineering: it encodes poles, zeros, stability, transient behavior, and frequency response in one compact rational function. This chapter builds the machinery from the integral definition through to deriving transfer functions for physical systems.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Compute the one-sided Laplace transform of common signals (step, ramp, exponential, sinusoid, impulse).
2. Apply the differentiation, integration, shifting, and convolution properties to transform ODEs.
3. Perform partial-fraction decomposition to invert Laplace transforms back to the time domain.
4. Derive the transfer function $G(s) = Y(s)/U(s)$ from a system's differential equation.
5. Identify poles and zeros of a transfer function and interpret their physical meaning.
6. Model mechanical (spring-mass-damper) and electrical (RLC) systems as transfer functions.

---

## 🖼️ Visual Anchor — The Laplace Transform Bridge

![math-11__11.1-fig1](math-11__11.1-fig1.svg)

---

## 📚 1. Definitions

### Definition 11.1.1 — The One-Sided Laplace Transform

The **one-sided (unilateral) Laplace transform** of a function $f(t)$ defined for $t \geq 0$ is:

$$
F(s) = \mathcal{L}\{f(t)\} = \int_0^{\infty} f(t)\, e^{-st}\, dt
$$

where $s = \sigma + j\omega \in \mathbb{C}$ is the complex frequency variable. The integral converges for $\text{Re}(s) > \sigma_0$ where $\sigma_0$ is the **abscissa of convergence**.

### Definition 11.1.2 — The Inverse Laplace Transform

The **inverse Laplace transform** recovers $f(t)$ from $F(s)$:

$$
f(t) = \mathcal{L}^{-1}\{F(s)\} = \frac{1}{2\pi j} \int_{\sigma - j\infty}^{\sigma + j\infty} F(s)\, e^{st}\, ds
$$

where $\sigma$ is chosen to the right of all singularities of $F(s)$. In practice, we use partial-fraction decomposition and a table of known transform pairs rather than evaluating this contour integral directly.

### Definition 11.1.3 — Transfer Function

For a linear time-invariant (LTI) system with input $u(t)$ and output $y(t)$, the **transfer function** is defined as the ratio of the Laplace transform of the output to the Laplace transform of the input, assuming zero initial conditions:

$$
G(s) = \frac{Y(s)}{U(s)}
$$

The transfer function is a property of the system alone — independent of the specific input signal.

### Definition 11.1.4 — Poles and Zeros

Given a transfer function in factored form:

$$
G(s) = K \frac{(s - z_1)(s - z_2)\cdots(s - z_m)}{(s - p_1)(s - p_2)\cdots(s - p_n)}
$$

- **Zeros**: The values $z_1, z_2, \ldots, z_m$ where $G(z_i) = 0$ (numerator roots).
- **Poles**: The values $p_1, p_2, \ldots, p_n$ where $G(p_i) \to \infty$ (denominator roots).
- **Order**: The system order is $n$ (the degree of the denominator polynomial).
- **Proper**: $G(s)$ is proper if $m \leq n$ and strictly proper if $m < n$.

### Definition 11.1.5 — Characteristic Polynomial

The **characteristic polynomial** of a system with transfer function $G(s) = N(s)/D(s)$ is the denominator polynomial $D(s)$. Its roots are the poles of the system, which determine stability and transient behavior.

### Definition 11.1.6 — Impulse Response

The **impulse response** $g(t)$ of an LTI system is the output when the input is the Dirac delta function $\delta(t)$:

$$
g(t) = \mathcal{L}^{-1}\{G(s)\}
$$

Since $\mathcal{L}\{\delta(t)\} = 1$, we have $Y(s) = G(s) \cdot 1 = G(s)$, so the transfer function is the Laplace transform of the impulse response.

### Definition 11.1.7 — Convolution Integral

For an LTI system with impulse response $g(t)$ and input $u(t)$, the output is:

$$
y(t) = g(t) * u(t) = \int_0^t g(t - \tau)\, u(\tau)\, d\tau
$$

The Laplace transform converts this convolution into multiplication: $Y(s) = G(s) \cdot U(s)$.

---

## 📚 1.1 — Essential Laplace Transform Table

| $f(t)$, $t \geq 0$ | $F(s) = \mathcal{L}\{f(t)\}$ | Region of Convergence |
|:---|:---|:---|
| $\delta(t)$ (unit impulse) | $1$ | All $s$ |
| $u(t)$ (unit step) | $\dfrac{1}{s}$ | $\text{Re}(s) > 0$ |
| $t$ (ramp) | $\dfrac{1}{s^2}$ | $\text{Re}(s) > 0$ |
| $t^n$ | $\dfrac{n!}{s^{n+1}}$ | $\text{Re}(s) > 0$ |
| $e^{-at}$ | $\dfrac{1}{s+a}$ | $\text{Re}(s) > -a$ |
| $t\,e^{-at}$ | $\dfrac{1}{(s+a)^2}$ | $\text{Re}(s) > -a$ |
| $t^n e^{-at}$ | $\dfrac{n!}{(s+a)^{n+1}}$ | $\text{Re}(s) > -a$ |
| $\sin(\omega t)$ | $\dfrac{\omega}{s^2 + \omega^2}$ | $\text{Re}(s) > 0$ |
| $\cos(\omega t)$ | $\dfrac{s}{s^2 + \omega^2}$ | $\text{Re}(s) > 0$ |
| $e^{-at}\sin(\omega t)$ | $\dfrac{\omega}{(s+a)^2 + \omega^2}$ | $\text{Re}(s) > -a$ |
| $e^{-at}\cos(\omega t)$ | $\dfrac{s+a}{(s+a)^2 + \omega^2}$ | $\text{Re}(s) > -a$ |



## 📐 2. Axioms / Postulates

### Axiom 11.1.A1 — Linearity of the Laplace Transform

The Laplace transform is a **linear operator**. For any functions $f(t)$, $g(t)$ and constants $a$, $b$:

$$
\mathcal{L}\{a\,f(t) + b\,g(t)\} = a\,F(s) + b\,G(s)
$$

This follows directly from the linearity of integration.

### Axiom 11.1.A2 — Causality (One-Sided Transform)

We restrict attention to **causal** signals and systems: $f(t) = 0$ for $t < 0$. The one-sided Laplace transform integrates from $0$ to $\infty$, encoding the assumption that the system starts at $t = 0$.

### Axiom 11.1.A3 — LTI System Superposition

A system is **Linear Time-Invariant (LTI)** if and only if:
1. **Linearity**: If input $u_1(t) \to y_1(t)$ and $u_2(t) \to y_2(t)$, then $\alpha u_1 + \beta u_2 \to \alpha y_1 + \beta y_2$.
2. **Time-Invariance**: If $u(t) \to y(t)$, then $u(t - T) \to y(t - T)$ for any delay $T$.

Only LTI systems possess a well-defined transfer function.

### Axiom 11.1.A4 — Zero Initial Conditions for Transfer Function

The transfer function $G(s) = Y(s)/U(s)$ is defined under the assumption that **all initial conditions are zero** (the system is initially at rest). Non-zero initial conditions contribute additional terms that are handled separately.

---

## 🛡️ 3. Lemmas (Key Properties)

### Lemma 11.1.1 — Differentiation in Time

If $\mathcal{L}\{f(t)\} = F(s)$, then:

$$
\mathcal{L}\{f'(t)\} = sF(s) - f(0^-)
$$

$$
\mathcal{L}\{f''(t)\} = s^2 F(s) - sf(0^-) - f'(0^-)
$$

In general, for the $n$-th derivative:

$$
\mathcal{L}\{f^{(n)}(t)\} = s^n F(s) - s^{n-1}f(0^-) - s^{n-2}f'(0^-) - \cdots - f^{(n-1)}(0^-)
$$

<details>
<summary>🔍 Proof of First Derivative Property</summary>

Apply integration by parts to $\mathcal{L}\{f'(t)\} = \int_0^\infty f'(t) e^{-st}\,dt$.

Let $u = e^{-st}$ and $dv = f'(t)\,dt$, so $du = -s\,e^{-st}\,dt$ and $v = f(t)$.

$$
\int_0^\infty f'(t) e^{-st}\,dt = \left[f(t)e^{-st}\right]_0^\infty - \int_0^\infty f(t)(-s)e^{-st}\,dt
$$

The boundary term: as $t \to \infty$, $f(t)e^{-st} \to 0$ (for $\text{Re}(s)$ sufficiently large); at $t = 0$, we get $-f(0^-)$.

$$
= 0 - f(0^-) + s\int_0^\infty f(t)e^{-st}\,dt = sF(s) - f(0^-)
$$

$\blacksquare$

</details>

### Lemma 11.1.2 — Integration in Time

$$
\mathcal{L}\left\{\int_0^t f(\tau)\,d\tau\right\} = \frac{F(s)}{s}
$$

<details>
<summary>🔍 Proof</summary>

Let $g(t) = \int_0^t f(\tau)\,d\tau$. Then $g'(t) = f(t)$ and $g(0) = 0$.

By Lemma 11.1.1: $\mathcal{L}\{g'(t)\} = sG(s) - g(0) = sG(s)$.

But $\mathcal{L}\{g'(t)\} = \mathcal{L}\{f(t)\} = F(s)$.

Therefore $sG(s) = F(s)$, giving $G(s) = F(s)/s$. $\blacksquare$

</details>

### Lemma 11.1.3 — First Shifting Theorem (s-Domain Shift)

If $\mathcal{L}\{f(t)\} = F(s)$, then:

$$
\mathcal{L}\{e^{-at}f(t)\} = F(s + a)
$$

<details>
<summary>🔍 Proof</summary>

$$
\mathcal{L}\{e^{-at}f(t)\} = \int_0^\infty e^{-at}f(t)e^{-st}\,dt = \int_0^\infty f(t)e^{-(s+a)t}\,dt = F(s+a)
$$

$\blacksquare$

</details>

### Lemma 11.1.4 — Second Shifting Theorem (Time Delay)

If $\mathcal{L}\{f(t)\} = F(s)$, then for a time delay $T > 0$:

$$
\mathcal{L}\{f(t-T)\,u(t-T)\} = e^{-sT}F(s)
$$

where $u(t-T)$ is the unit step shifted to $t = T$.

<details>
<summary>🔍 Proof</summary>

$$
\mathcal{L}\{f(t-T)u(t-T)\} = \int_0^\infty f(t-T)u(t-T)e^{-st}\,dt = \int_T^\infty f(t-T)e^{-st}\,dt
$$

Substitute $\tau = t - T$, so $t = \tau + T$, $dt = d\tau$:

$$
= \int_0^\infty f(\tau)e^{-s(\tau+T)}\,d\tau = e^{-sT}\int_0^\infty f(\tau)e^{-s\tau}\,d\tau = e^{-sT}F(s)
$$

$\blacksquare$

</details>

### Lemma 11.1.5 — Convolution Theorem

If $\mathcal{L}\{f(t)\} = F(s)$ and $\mathcal{L}\{g(t)\} = G(s)$, then:

$$
\mathcal{L}\{f * g\} = \mathcal{L}\left\{\int_0^t f(\tau)g(t-\tau)\,d\tau\right\} = F(s) \cdot G(s)
$$

Convolution in time becomes multiplication in the $s$-domain.

### Lemma 11.1.6 — Final Value Theorem

If all poles of $sF(s)$ lie in the open left half-plane (i.e., the system is stable), then:

$$
\lim_{t \to \infty} f(t) = \lim_{s \to 0} sF(s)
$$

### Lemma 11.1.7 — Initial Value Theorem

If $f(t)$ and $f'(t)$ are both Laplace-transformable:

$$
f(0^+) = \lim_{s \to \infty} sF(s)
$$

### Lemma 11.1.8 — Differentiation in s-Domain (Multiplication by t)

$$
\mathcal{L}\{t\,f(t)\} = -\frac{dF(s)}{ds}
$$

More generally: $\mathcal{L}\{t^n f(t)\} = (-1)^n \dfrac{d^n F(s)}{ds^n}$.



---

## 👑 4. Theorems

### Theorem 11.1.1 — Transfer Function from ODE

Given an $n$-th order LTI system described by:

$$
a_n y^{(n)} + a_{n-1} y^{(n-1)} + \cdots + a_1 y' + a_0 y = b_m u^{(m)} + b_{m-1} u^{(m-1)} + \cdots + b_1 u' + b_0 u
$$

Under zero initial conditions, the transfer function is:

$$
G(s) = \frac{Y(s)}{U(s)} = \frac{b_m s^m + b_{m-1} s^{m-1} + \cdots + b_1 s + b_0}{a_n s^n + a_{n-1} s^{n-1} + \cdots + a_1 s + a_0}
$$

### Theorem 11.1.2 — Poles Determine Stability

An LTI system with transfer function $G(s)$ is:
- **BIBO Stable** if and only if all poles of $G(s)$ have strictly negative real parts (lie in the open left half-plane).
- **Marginally Stable** if poles lie on the imaginary axis with multiplicity 1 and no poles in the right half-plane.
- **Unstable** if any pole has positive real part, or if any imaginary-axis pole has multiplicity $> 1$.

### Theorem 11.1.3 — Partial Fraction Decomposition (Heaviside Cover-Up)

Let $G(s) = N(s)/D(s)$ be strictly proper ($\deg N < \deg D$) with $D(s)$ factored into distinct real poles:

$$
G(s) = \frac{N(s)}{(s - p_1)(s - p_2)\cdots(s - p_n)} = \frac{A_1}{s - p_1} + \frac{A_2}{s - p_2} + \cdots + \frac{A_n}{s - p_n}
$$

Each residue is computed by the **cover-up method**:

$$
A_k = \left[(s - p_k) G(s)\right]_{s = p_k} = \frac{N(p_k)}{\prod_{j \neq k}(p_k - p_j)}
$$

### Theorem 11.1.4 — Partial Fractions for Repeated Poles

If $G(s)$ has a pole $p$ of multiplicity $r$:

$$
G(s) = \cdots + \frac{A_1}{s-p} + \frac{A_2}{(s-p)^2} + \cdots + \frac{A_r}{(s-p)^r} + \cdots
$$

The coefficients are:

$$
A_k = \frac{1}{(r-k)!} \left[\frac{d^{r-k}}{ds^{r-k}}\left((s-p)^r G(s)\right)\right]_{s=p}
$$

### Theorem 11.1.5 — Partial Fractions for Complex Conjugate Poles

If $G(s)$ has complex poles $s = -\alpha \pm j\beta$, the corresponding partial fraction terms combine as:

$$
\frac{As + B}{(s+\alpha)^2 + \beta^2} \quad \longleftrightarrow \quad e^{-\alpha t}\left[A\cos(\beta t) + \frac{B - A\alpha}{\beta}\sin(\beta t)\right]
$$

---

## ✍️ 5. Proofs / Derivations

### 5.1 — Derivation: Laplace Transform of $e^{-at}$ from First Principles

We compute $\mathcal{L}\{e^{-at}\}$ directly from the definition:

$$
\mathcal{L}\{e^{-at}\} = \int_0^\infty e^{-at} e^{-st}\,dt = \int_0^\infty e^{-(s+a)t}\,dt
$$

Evaluate the integral:

$$
= \left[\frac{e^{-(s+a)t}}{-(s+a)}\right]_0^\infty
$$

At $t \to \infty$: $e^{-(s+a)t} \to 0$ provided $\text{Re}(s+a) > 0$, i.e., $\text{Re}(s) > -a$.

At $t = 0$: $e^0 = 1$.

$$
= 0 - \frac{1}{-(s+a)} = \frac{1}{s+a}
$$

Therefore:

$$
\mathcal{L}\{e^{-at}\} = \frac{1}{s+a}, \quad \text{Re}(s) > -a
$$

### 5.2 — Derivation: Laplace Transform of $\sin(\omega t)$

Using Euler's formula: $\sin(\omega t) = \dfrac{e^{j\omega t} - e^{-j\omega t}}{2j}$.

By linearity and the exponential transform:

$$
\mathcal{L}\{\sin(\omega t)\} = \frac{1}{2j}\left[\mathcal{L}\{e^{j\omega t}\} - \mathcal{L}\{e^{-j\omega t}\}\right]
$$

$$
= \frac{1}{2j}\left[\frac{1}{s - j\omega} - \frac{1}{s + j\omega}\right]
$$

Find common denominator:

$$
= \frac{1}{2j} \cdot \frac{(s + j\omega) - (s - j\omega)}{(s - j\omega)(s + j\omega)}
$$

$$
= \frac{1}{2j} \cdot \frac{2j\omega}{s^2 + \omega^2}
$$

$$
= \frac{\omega}{s^2 + \omega^2}
$$

### 5.3 — Derivation: Transfer Function of a Spring-Mass-Damper System

**Physical system**: Mass $m$, damping coefficient $b$, spring constant $k$. Input: applied force $f(t)$. Output: displacement $x(t)$.

**Step 1 — Newton's Second Law:**

$$
m\ddot{x}(t) + b\dot{x}(t) + kx(t) = f(t)
$$

**Step 2 — Apply Laplace transform** (zero initial conditions: $x(0) = 0$, $\dot{x}(0) = 0$):

$$
\mathcal{L}\{m\ddot{x}\} = m[s^2 X(s) - sx(0) - \dot{x}(0)] = ms^2 X(s)
$$

$$
\mathcal{L}\{b\dot{x}\} = b[sX(s) - x(0)] = bsX(s)
$$

$$
\mathcal{L}\{kx\} = kX(s)
$$

$$
\mathcal{L}\{f(t)\} = F(s)
$$

**Step 3 — Combine:**

$$
ms^2 X(s) + bsX(s) + kX(s) = F(s)
$$

$$
X(s)[ms^2 + bs + k] = F(s)
$$

**Step 4 — Form transfer function:**

$$
G(s) = \frac{X(s)}{F(s)} = \frac{1}{ms^2 + bs + k}
$$

**Step 5 — Identify poles** (using quadratic formula):

$$
s = \frac{-b \pm \sqrt{b^2 - 4mk}}{2m}
$$

- If $b^2 > 4mk$: two distinct real poles (overdamped)
- If $b^2 = 4mk$: repeated real pole (critically damped)
- If $b^2 < 4mk$: complex conjugate poles (underdamped)

### 5.4 — Derivation: Transfer Function of a Series RLC Circuit

**Physical system**: Resistor $R$, inductor $L$, capacitor $C$ in series. Input: voltage source $v_{in}(t)$. Output: voltage across capacitor $v_C(t)$.

**Step 1 — KVL around the loop:**

$$
v_{in}(t) = v_R(t) + v_L(t) + v_C(t)
$$

With current $i(t) = C\dfrac{dv_C}{dt}$:

$$
v_R = Ri = RC\frac{dv_C}{dt}, \quad v_L = L\frac{di}{dt} = LC\frac{d^2 v_C}{dt^2}
$$

**Step 2 — Substitute:**

$$
v_{in}(t) = LC\frac{d^2 v_C}{dt^2} + RC\frac{dv_C}{dt} + v_C(t)
$$

**Step 3 — Laplace transform** (zero ICs):

$$
V_{in}(s) = LCs^2 V_C(s) + RCs\,V_C(s) + V_C(s)
$$

**Step 4 — Transfer function:**

$$
G(s) = \frac{V_C(s)}{V_{in}(s)} = \frac{1}{LCs^2 + RCs + 1}
$$

Dividing numerator and denominator by $LC$:

$$
G(s) = \frac{\frac{1}{LC}}{s^2 + \frac{R}{L}s + \frac{1}{LC}} = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}
$$

where $\omega_n = \dfrac{1}{\sqrt{LC}}$ (natural frequency) and $\zeta = \dfrac{R}{2}\sqrt{\dfrac{C}{L}}$ (damping ratio).

### 5.5 — Full Partial Fraction Inversion: Second-Order System Step Response

Find $y(t)$ for a unit step input to $G(s) = \dfrac{4}{s^2 + 3s + 2}$.

**Step 1 — Factor denominator:**

$$
s^2 + 3s + 2 = (s+1)(s+2)
$$

**Step 2 — Form $Y(s)$** (step input: $U(s) = 1/s$):

$$
Y(s) = G(s) \cdot U(s) = \frac{4}{s(s+1)(s+2)}
$$

**Step 3 — Partial fraction decomposition:**

$$
\frac{4}{s(s+1)(s+2)} = \frac{A}{s} + \frac{B}{s+1} + \frac{C}{s+2}
$$

**Cover-up method:**

$$
A = \left[\frac{4}{(s+1)(s+2)}\right]_{s=0} = \frac{4}{(1)(2)} = 2
$$

$$
B = \left[\frac{4}{s(s+2)}\right]_{s=-1} = \frac{4}{(-1)(1)} = -4
$$

$$
C = \left[\frac{4}{s(s+1)}\right]_{s=-2} = \frac{4}{(-2)(-1)} = 2
$$

**Step 4 — Verify:** $\dfrac{2}{s} + \dfrac{-4}{s+1} + \dfrac{2}{s+2}$. Common denominator check:

$$
\frac{2(s+1)(s+2) - 4s(s+2) + 2s(s+1)}{s(s+1)(s+2)}
$$

Numerator: $2(s^2+3s+2) - 4(s^2+2s) + 2(s^2+s) = 2s^2+6s+4 - 4s^2-8s + 2s^2+2s = 4$. ✓

**Step 5 — Inverse Laplace transform** (term by term):

$$
y(t) = \mathcal{L}^{-1}\left\{\frac{2}{s}\right\} + \mathcal{L}^{-1}\left\{\frac{-4}{s+1}\right\} + \mathcal{L}^{-1}\left\{\frac{2}{s+2}\right\}
$$

Using $\mathcal{L}^{-1}\{1/s\} = u(t)$ and $\mathcal{L}^{-1}\{1/(s+a)\} = e^{-at}$:

$$
y(t) = 2 - 4e^{-t} + 2e^{-2t}, \quad t \geq 0
$$

**Step 6 — Verify with Final Value Theorem:**

$$
\lim_{t\to\infty} y(t) = \lim_{s\to 0} s \cdot Y(s) = \lim_{s\to 0} \frac{4}{(s+1)(s+2)} = \frac{4}{2} = 2 \quad \checkmark
$$

### 5.6 — Partial Fraction Inversion with Complex Poles

Find $y(t)$ for a unit step input to $G(s) = \dfrac{5}{s^2 + 2s + 5}$.

**Step 1 — Identify poles** via quadratic formula:

$$
s = \frac{-2 \pm \sqrt{4 - 20}}{2} = \frac{-2 \pm \sqrt{-16}}{2} = -1 \pm 2j
$$

Complex conjugate poles at $s = -1 \pm 2j$. So $\alpha = 1$, $\beta = 2$.

**Step 2 — Form $Y(s)$:**

$$
Y(s) = \frac{5}{s(s^2 + 2s + 5)}
$$

**Step 3 — Partial fractions:**

$$
\frac{5}{s(s^2 + 2s + 5)} = \frac{A}{s} + \frac{Bs + C}{s^2 + 2s + 5}
$$

Cover-up for $A$:

$$
A = \left[\frac{5}{s^2 + 2s + 5}\right]_{s=0} = \frac{5}{5} = 1
$$

Multiply both sides by $s(s^2 + 2s + 5)$:

$$
5 = A(s^2 + 2s + 5) + (Bs + C)s
$$

$$
5 = s^2 + 2s + 5 + Bs^2 + Cs
$$

$$
5 = (1+B)s^2 + (2+C)s + 5
$$

Equating coefficients:
- $s^2$: $1 + B = 0 \Rightarrow B = -1$
- $s^1$: $2 + C = 0 \Rightarrow C = -2$
- $s^0$: $5 = 5$ ✓

**Step 4 — Rewrite the complex-pole term:**

$$
Y(s) = \frac{1}{s} + \frac{-s - 2}{s^2 + 2s + 5} = \frac{1}{s} - \frac{s + 2}{(s+1)^2 + 4}
$$

Complete the square in the denominator: $s^2 + 2s + 5 = (s+1)^2 + 2^2$.

Decompose the numerator to match standard forms:

$$
\frac{s+2}{(s+1)^2 + 4} = \frac{(s+1) + 1}{(s+1)^2 + 4} = \frac{s+1}{(s+1)^2 + 4} + \frac{1}{(s+1)^2 + 4}
$$

$$
= \frac{s+1}{(s+1)^2 + 2^2} + \frac{1}{2} \cdot \frac{2}{(s+1)^2 + 2^2}
$$

**Step 5 — Inverse transform** using $\mathcal{L}^{-1}\left\{\dfrac{s+a}{(s+a)^2+\beta^2}\right\} = e^{-at}\cos(\beta t)$ and $\mathcal{L}^{-1}\left\{\dfrac{\beta}{(s+a)^2+\beta^2}\right\} = e^{-at}\sin(\beta t)$:

$$
y(t) = 1 - e^{-t}\cos(2t) - \frac{1}{2}e^{-t}\sin(2t), \quad t \geq 0
$$

**Step 6 — Verify with Final Value Theorem:**

$$
\lim_{s\to 0} sY(s) = \lim_{s\to 0} \frac{5}{s^2+2s+5} = \frac{5}{5} = 1 \quad \checkmark
$$



---

## 🧮 6. Worked Examples

### Example 11.1.1 — Transfer Function of a DC Motor

A DC motor has armature resistance $R_a$, inductance $L_a$, back-EMF constant $K_b$, torque constant $K_t$, moment of inertia $J$, and viscous friction $B$. Input: armature voltage $V_a(s)$. Output: angular velocity $\Omega(s)$.

**Electrical equation (armature circuit):**

$$
V_a(t) = R_a i_a(t) + L_a \frac{di_a}{dt} + K_b \omega(t)
$$

**Mechanical equation (rotor):**

$$
J\frac{d\omega}{dt} + B\omega(t) = K_t i_a(t)
$$

**Laplace transform (zero ICs):**

$$
V_a(s) = (R_a + L_a s)I_a(s) + K_b \Omega(s) \tag{1}
$$

$$
(Js + B)\Omega(s) = K_t I_a(s) \tag{2}
$$

**From (2):** $I_a(s) = \dfrac{(Js + B)\Omega(s)}{K_t}$

**Substitute into (1):**

$$
V_a(s) = (R_a + L_a s)\frac{(Js + B)\Omega(s)}{K_t} + K_b \Omega(s)
$$

$$
V_a(s) = \Omega(s)\left[\frac{(R_a + L_a s)(Js + B)}{K_t} + K_b\right]
$$

$$
V_a(s) = \Omega(s)\left[\frac{(R_a + L_a s)(Js + B) + K_b K_t}{K_t}\right]
$$

**Transfer function:**

$$
G(s) = \frac{\Omega(s)}{V_a(s)} = \frac{K_t}{(R_a + L_a s)(Js + B) + K_b K_t}
$$

$$
= \frac{K_t}{L_a J s^2 + (L_a B + R_a J)s + (R_a B + K_b K_t)}
$$

**Numerical example:** $R_a = 2\,\Omega$, $L_a = 0.5\,\text{H}$, $K_b = K_t = 0.1\,\text{V·s/rad}$, $J = 0.01\,\text{kg·m}^2$, $B = 0.1\,\text{N·m·s/rad}$.

$$
G(s) = \frac{0.1}{0.005s^2 + 0.07s + 0.21} = \frac{20}{s^2 + 14s + 42}
$$

Poles: $s = \dfrac{-14 \pm \sqrt{196 - 168}}{2} = \dfrac{-14 \pm \sqrt{28}}{2} = -7 \pm \sqrt{7} \approx -4.35, -9.65$

Both poles are in the left half-plane → **stable**, overdamped response.

---

### Example 11.1.2 — Inverted Pendulum Linearized Transfer Function

A pendulum of length $\ell$ and mass $m$ on a cart of mass $M$. Input: horizontal force $F$. Output: angle $\theta$ (small angle approximation).

**Linearized equation of motion** (about $\theta = 0$):

$$
(M + m)\ddot{x} - m\ell\ddot{\theta} = F
$$

$$
m\ell^2\ddot{\theta} - mg\ell\theta = m\ell\ddot{x}
$$

Taking Laplace transforms and solving for $\Theta(s)/F(s)$:

From equation 2: $m\ell^2 s^2 \Theta - mg\ell\Theta = m\ell s^2 X$

$$
\Theta(m\ell^2 s^2 - mg\ell) = m\ell s^2 X \implies X = \frac{(\ell s^2 - g)\Theta}{s^2}
$$

Substitute into equation 1: $(M+m)s^2 X - m\ell s^2 \Theta = F$

$$
(M+m)s^2 \cdot \frac{(\ell s^2 - g)\Theta}{s^2} - m\ell s^2 \Theta = F
$$

$$
(M+m)(\ell s^2 - g)\Theta - m\ell s^2 \Theta = F
$$

$$
\Theta[(M+m)\ell s^2 - (M+m)g - m\ell s^2] = F
$$

$$
\Theta[M\ell s^2 - (M+m)g] = F
$$

$$
G(s) = \frac{\Theta(s)}{F(s)} = \frac{1}{M\ell s^2 - (M+m)g}
$$

**Note:** This has a pole at $s = +\sqrt{\dfrac{(M+m)g}{M\ell}}$ in the **right half-plane** → the inverted pendulum is inherently **unstable** and requires active feedback control.

---

### Example 11.1.3 — Partial Fraction with Repeated Poles

Find $y(t) = \mathcal{L}^{-1}\left\{\dfrac{3s + 5}{(s+1)^2(s+3)}\right\}$.

**Step 1 — Set up partial fractions:**

$$
\frac{3s + 5}{(s+1)^2(s+3)} = \frac{A}{s+1} + \frac{B}{(s+1)^2} + \frac{C}{s+3}
$$

**Step 2 — Find $C$ by cover-up** (multiply by $(s+3)$, set $s = -3$):

$$
C = \left[\frac{3s+5}{(s+1)^2}\right]_{s=-3} = \frac{3(-3)+5}{(-3+1)^2} = \frac{-4}{4} = -1
$$

**Step 3 — Find $B$ by cover-up** (multiply by $(s+1)^2$, set $s = -1$):

$$
B = \left[\frac{3s+5}{s+3}\right]_{s=-1} = \frac{3(-1)+5}{-1+3} = \frac{2}{2} = 1
$$

**Step 4 — Find $A$** by differentiating $(s+1)^2 G(s)$ and evaluating at $s = -1$:

$$
(s+1)^2 G(s) = \frac{3s+5}{s+3}
$$

$$
\frac{d}{ds}\left[\frac{3s+5}{s+3}\right] = \frac{3(s+3) - (3s+5)}{(s+3)^2} = \frac{4}{(s+3)^2}
$$

$$
A = \left[\frac{4}{(s+3)^2}\right]_{s=-1} = \frac{4}{4} = 1
$$

**Step 5 — Verify:** Multiply out $\dfrac{1}{s+1} + \dfrac{1}{(s+1)^2} + \dfrac{-1}{s+3}$:

$$
= \frac{(s+1)(s+3) + (s+3) - (s+1)^2}{(s+1)^2(s+3)}
$$

Numerator: $(s^2+4s+3) + (s+3) - (s^2+2s+1) = 3s + 5$ ✓

**Step 6 — Inverse transform:**

$$
y(t) = e^{-t} + te^{-t} - e^{-3t}, \quad t \geq 0
$$

Using: $\mathcal{L}^{-1}\{1/(s+a)\} = e^{-at}$, $\mathcal{L}^{-1}\{1/(s+a)^2\} = te^{-at}$.

---

### Example 11.1.4 — Transfer Function of a Coupled Two-Tank System

Two tanks in series. Tank 1 has cross-section $A_1$, outlet resistance $R_1$. Tank 2 has cross-section $A_2$, outlet resistance $R_2$. Input: flow rate $q_{in}(t)$. Output: level $h_2(t)$.

**Mass balance equations:**

$$
A_1 \frac{dh_1}{dt} = q_{in}(t) - \frac{h_1}{R_1}
$$

$$
A_2 \frac{dh_2}{dt} = \frac{h_1}{R_1} - \frac{h_2}{R_2}
$$

**Laplace transform (zero ICs):**

$$
A_1 s H_1(s) + \frac{1}{R_1}H_1(s) = Q_{in}(s)
$$

$$
H_1(s) = \frac{R_1 Q_{in}(s)}{A_1 R_1 s + 1} = \frac{R_1}{(\tau_1 s + 1)}Q_{in}(s)
$$

where $\tau_1 = A_1 R_1$ is the time constant of Tank 1.

$$
A_2 s H_2(s) + \frac{1}{R_2}H_2(s) = \frac{1}{R_1}H_1(s)
$$

$$
H_2(s) = \frac{R_2}{(\tau_2 s + 1)} \cdot \frac{1}{R_1} H_1(s) = \frac{R_2}{R_1(\tau_2 s + 1)} \cdot \frac{R_1}{(\tau_1 s + 1)}Q_{in}(s)
$$

**Transfer function:**

$$
G(s) = \frac{H_2(s)}{Q_{in}(s)} = \frac{R_2}{(\tau_1 s + 1)(\tau_2 s + 1)}
$$

This is a **second-order system** with two real poles at $s = -1/\tau_1$ and $s = -1/\tau_2$, and DC gain $G(0) = R_2$.

---

### Example 11.1.5 — Using the Final and Initial Value Theorems

Given $Y(s) = \dfrac{10(s+2)}{s(s+1)(s+5)}$, find $y(0^+)$ and $y(\infty)$.

**Initial Value Theorem:**

$$
y(0^+) = \lim_{s\to\infty} sY(s) = \lim_{s\to\infty} \frac{10s(s+2)}{s(s+1)(s+5)} = \lim_{s\to\infty} \frac{10(s+2)}{(s+1)(s+5)}
$$

$$
= \lim_{s\to\infty} \frac{10s + 20}{s^2 + 6s + 5} = \lim_{s\to\infty} \frac{10/s + 20/s^2}{1 + 6/s + 5/s^2} = 0
$$

**Final Value Theorem** (check: all poles of $sY(s)$ at $s = -1, -5$ are in LHP ✓):

$$
y(\infty) = \lim_{s\to 0} sY(s) = \lim_{s\to 0} \frac{10(s+2)}{(s+1)(s+5)} = \frac{10(2)}{(1)(5)} = 4
$$

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- [3.6 - Laplace Transforms](3.6---Laplace-Transforms) — Extended Laplace transform theory in the ODE context
- [3.4 - Systems of Linear ODEs & State Space](3.4---Systems-of-Linear-ODEs-&-State-Space) — State-space formulation (see also [11.8 - Modern Control - State-Space Representation](11.8---Modern-Control---State-Space-Representation))
- [2.6 - Eigenvalues Eigenvectors & Diagonalization](2.6---Eigenvalues-Eigenvectors-&-Diagonalization) — Eigenvalues as system poles
- [11.2 - Block Diagrams & Feedback](11.2---Block-Diagrams-&-Feedback) — Next chapter: combining transfer functions

### External Resources
- **Åström & Murray**, *Feedback Systems* (free PDF: fbswiki.org) — Chapter 9: Frequency Domain Analysis
- **MIT OCW 16.30** — Lecture 2: Transfer Functions and Frequency Response
- **Brian Douglas** — [Transfer Functions](https://www.youtube.com/watch?v=RJleGwXA7Qo) (YouTube)
- **Ogata**, *Modern Control Engineering* — Chapter 2: Mathematical Modeling of Control Systems

---

*Next: [11.2 - Block Diagrams & Feedback](11.2---Block-Diagrams-&-Feedback) →*



---

## 🧠 8. Extended Worked Examples & Deep Dives

### Problem 11.1.E1 — Derive Transfer Function from a Spring-Mass-Damper ODE

> **Problem:** A mechanical system consists of a mass $m = 2$ kg, a viscous damper $b = 6$ N·s/m, and a spring $k = 4$ N/m. The input is an applied force $f(t)$ and the output is the displacement $x(t)$. Derive the transfer function $G(s) = X(s)/F(s)$ from first principles, identify the poles, and classify the system response.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Write the Equation of Motion (Newton's Second Law)

The free-body diagram gives forces on the mass: applied force $f(t)$, spring restoring force $-kx$, damping force $-b\dot{x}$.

$$
m\ddot{x}(t) + b\dot{x}(t) + kx(t) = f(t)
$$

Substituting numerical values:

$$
2\ddot{x}(t) + 6\dot{x}(t) + 4x(t) = f(t)
$$

#### Step 2: Apply the Laplace Transform

Assume zero initial conditions: $x(0) = 0$, $\dot{x}(0) = 0$.

Recall the differentiation property:

$$
\mathcal{L}\{\ddot{x}(t)\} = s^2 X(s) - sx(0) - \dot{x}(0) = s^2 X(s)
$$

$$
\mathcal{L}\{\dot{x}(t)\} = sX(s) - x(0) = sX(s)
$$

Transform each term:

$$
2s^2 X(s) + 6sX(s) + 4X(s) = F(s)
$$

#### Step 3: Factor and Solve for the Transfer Function

Factor out $X(s)$ on the left:

$$
X(s)\left[2s^2 + 6s + 4\right] = F(s)
$$

$$
G(s) = \frac{X(s)}{F(s)} = \frac{1}{2s^2 + 6s + 4}
$$

Divide numerator and denominator by 2 to get monic form:

$$
G(s) = \frac{1/2}{s^2 + 3s + 2}
$$

#### Step 4: Find the Poles

Factor the denominator:

$$
s^2 + 3s + 2 = (s + 1)(s + 2)
$$

Poles are at $s = -1$ and $s = -2$.

Alternatively, using the quadratic formula:

$$
s = \frac{-3 \pm \sqrt{9 - 8}}{2} = \frac{-3 \pm 1}{2}
$$

$$
s_1 = \frac{-3 + 1}{2} = -1, \quad s_2 = \frac{-3 - 1}{2} = -2
$$

#### Step 5: Classify the Response

Compare with the standard second-order form $G(s) = \dfrac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$:

From our transfer function (monic denominator): $\omega_n^2 = 2$, so $\omega_n = \sqrt{2} \approx 1.414$ rad/s.

$2\zeta\omega_n = 3$, so $\zeta = \dfrac{3}{2\sqrt{2}} = \dfrac{3}{2.828} \approx 1.06$.

Since $\zeta \gt  1$, the system is **overdamped**. Both poles are real and negative, confirming stable, non-oscillatory response.

#### Step 6: Verify with the Discriminant

$$
b^2 - 4mk = 36 - 4(2)(4) = 36 - 32 = 4 \gt  0
$$

Positive discriminant confirms two distinct real roots (overdamped). ✓

</details>

---

### Problem 11.1.E2 — Inverse Laplace via Partial Fractions of a 3rd-Order Denominator

> **Problem:** Find the inverse Laplace transform of:
>
> $$F(s) = \frac{5s + 13}{(s + 1)(s + 2)(s + 3)}$$
>
> Show every step of the partial fraction decomposition and verify the result.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Set Up Partial Fraction Form

Since all poles are distinct and real:

$$
\frac{5s + 13}{(s+1)(s+2)(s+3)} = \frac{A}{s+1} + \frac{B}{s+2} + \frac{C}{s+3}
$$

#### Step 2: Find Coefficient $A$ (Cover-Up Method)

Multiply both sides by $(s+1)$ and set $s = -1$:

$$
A = \left[\frac{5s + 13}{(s+2)(s+3)}\right]_{s=-1} = \frac{5(-1) + 13}{(-1+2)(-1+3)} = \frac{-5 + 13}{(1)(2)} = \frac{8}{2} = 4
$$

#### Step 3: Find Coefficient $B$ (Cover-Up Method)

Multiply both sides by $(s+2)$ and set $s = -2$:

$$
B = \left[\frac{5s + 13}{(s+1)(s+3)}\right]_{s=-2} = \frac{5(-2) + 13}{(-2+1)(-2+3)} = \frac{-10 + 13}{(-1)(1)} = \frac{3}{-1} = -3
$$

#### Step 4: Find Coefficient $C$ (Cover-Up Method)

Multiply both sides by $(s+3)$ and set $s = -3$:

$$
C = \left[\frac{5s + 13}{(s+1)(s+2)}\right]_{s=-3} = \frac{5(-3) + 13}{(-3+1)(-3+2)} = \frac{-15 + 13}{(-2)(-1)} = \frac{-2}{2} = -1
$$

#### Step 5: Verify the Decomposition

Recombine over common denominator:

$$
\frac{4}{s+1} + \frac{-3}{s+2} + \frac{-1}{s+3} = \frac{4(s+2)(s+3) - 3(s+1)(s+3) - 1(s+1)(s+2)}{(s+1)(s+2)(s+3)}
$$

Expand each numerator term:

- $4(s+2)(s+3) = 4(s^2 + 5s + 6) = 4s^2 + 20s + 24$
- $-3(s+1)(s+3) = -3(s^2 + 4s + 3) = -3s^2 - 12s - 9$
- $-1(s+1)(s+2) = -(s^2 + 3s + 2) = -s^2 - 3s - 2$

Sum: $(4 - 3 - 1)s^2 + (20 - 12 - 3)s + (24 - 9 - 2) = 0s^2 + 5s + 13$

$$
= 5s + 13 \quad \checkmark
$$

#### Step 6: Inverse Laplace Transform (Term by Term)

Using the standard pair $\mathcal{L}^{-1}\left\{\dfrac{1}{s+a}\right\} = e^{-at}u(t)$:

$$
f(t) = 4e^{-t} - 3e^{-2t} - e^{-3t}, \quad t \geq 0
$$

#### Step 7: Verify with Initial and Final Values

**Initial Value Theorem:**

$$
f(0^+) = \lim_{s\to\infty} sF(s) = \lim_{s\to\infty} \frac{5s^2 + 13s}{s^3 + 6s^2 + 11s + 6} = 0
$$

Check from time domain: $f(0) = 4(1) - 3(1) - 1(1) = 0$ ✓

**Final Value Theorem:**

$$
f(\infty) = \lim_{s\to 0} sF(s) = \lim_{s\to 0} \frac{s(5s+13)}{(s+1)(s+2)(s+3)} = 0
$$

Check: as $t \to \infty$, all exponentials decay to zero. ✓

</details>

---

### Problem 11.1.E3 — Final-Value and Initial-Value Theorem Applications

> **Problem:** A closed-loop system has output:
>
> $$Y(s) = \frac{12(s + 4)}{s(s^2 + 6s + 8)}$$
>
> (a) Find the steady-state value $y(\infty)$ using the Final Value Theorem.
> (b) Find the initial value $y(0^+)$ using the Initial Value Theorem.
> (c) Verify both by computing the full inverse Laplace transform.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Part (a): Final Value Theorem

First, verify applicability: all poles of $sY(s)$ must be in the LHP.

$$
sY(s) = \frac{12(s+4)}{s^2 + 6s + 8} = \frac{12(s+4)}{(s+2)(s+4)}
$$

Poles of $sY(s)$: $s = -2$ and $s = -4$ (both in LHP). ✓ FVT is applicable.

$$
y(\infty) = \lim_{s \to 0} sY(s) = \lim_{s \to 0} \frac{12(s+4)}{(s+2)(s+4)} = \frac{12(4)}{(2)(4)} = \frac{48}{8} = 6
$$

#### Part (b): Initial Value Theorem

$$
y(0^+) = \lim_{s \to \infty} sY(s) = \lim_{s \to \infty} \frac{12(s+4)}{(s+2)(s+4)}
$$

Divide numerator and denominator by $s^2$:

$$
= \lim_{s \to \infty} \frac{12(1 + 4/s)}{(1 + 2/s)(1 + 4/s)} = \frac{12(1)}{(1)(1)} = 12
$$

Wait — let me recompute. We have:

$$
sY(s) = \frac{12(s+4)}{(s+2)(s+4)} = \frac{12}{s+2}
$$

(The $(s+4)$ factors cancel!)

So:

$$
y(0^+) = \lim_{s \to \infty} \frac{12}{s+2} = 0
$$

Let me redo this more carefully. The IVT states $y(0^+) = \lim_{s\to\infty} sY(s)$:

$$
sY(s) = \frac{12s(s+4)}{s(s^2+6s+8)} = \frac{12(s+4)}{s^2+6s+8}
$$

$$
\lim_{s\to\infty} \frac{12(s+4)}{s^2+6s+8} = \lim_{s\to\infty} \frac{12/s + 48/s^2}{1 + 6/s + 8/s^2} = 0
$$

So $y(0^+) = 0$.

#### Part (c): Full Inverse Laplace Transform

Factor the denominator of $Y(s)$:

$$
Y(s) = \frac{12(s+4)}{s(s+2)(s+4)} = \frac{12}{s(s+2)}
$$

The $(s+4)$ cancels! Now decompose:

$$
\frac{12}{s(s+2)} = \frac{A}{s} + \frac{B}{s+2}
$$

Cover-up:

$$
A = \left[\frac{12}{s+2}\right]_{s=0} = \frac{12}{2} = 6
$$

$$
B = \left[\frac{12}{s}\right]_{s=-2} = \frac{12}{-2} = -6
$$

Therefore:

$$
y(t) = 6 - 6e^{-2t}, \quad t \geq 0
$$

**Verification:**

- $y(0) = 6 - 6(1) = 0$ ✓ (matches IVT)
- $y(\infty) = 6 - 0 = 6$ ✓ (matches FVT)

#### Key Insight

The pole-zero cancellation at $s = -4$ simplified the system from third-order to second-order. The cancelled mode does not appear in the output, but it still exists internally in the state-space representation. This is why transfer functions can hide internal dynamics.

</details>

---

### Problem 11.1.E4 — Inverse Laplace of a Function with Complex Poles and a Real Pole

> **Problem:** Find $y(t) = \mathcal{L}^{-1}\left\{\dfrac{10}{(s+1)(s^2 + 4s + 13)}\right\}$ showing every algebraic step.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Identify the Pole Locations

Real pole: $s = -1$

Complex poles from $s^2 + 4s + 13 = 0$:

$$
s = \frac{-4 \pm \sqrt{16 - 52}}{2} = \frac{-4 \pm \sqrt{-36}}{2} = -2 \pm 3j
$$

So the poles are at $s = -1$, $s = -2 + 3j$, $s = -2 - 3j$.

#### Step 2: Set Up Partial Fractions

$$
\frac{10}{(s+1)(s^2+4s+13)} = \frac{A}{s+1} + \frac{Bs + C}{s^2+4s+13}
$$

#### Step 3: Find $A$ by Cover-Up

$$
A = \left[\frac{10}{s^2+4s+13}\right]_{s=-1} = \frac{10}{1 - 4 + 13} = \frac{10}{10} = 1
$$

#### Step 4: Find $B$ and $C$

Multiply both sides by $(s+1)(s^2+4s+13)$:

$$
10 = A(s^2+4s+13) + (Bs+C)(s+1)
$$

Substitute $A = 1$:

$$
10 = (s^2+4s+13) + (Bs+C)(s+1)
$$

$$
10 = s^2 + 4s + 13 + Bs^2 + Bs + Cs + C
$$

$$
10 = (1+B)s^2 + (4+B+C)s + (13+C)
$$

Equate coefficients:

- $s^2$: $0 = 1 + B \implies B = -1$
- $s^1$: $0 = 4 + B + C = 4 + (-1) + C = 3 + C \implies C = -3$
- $s^0$: $10 = 13 + C = 13 + (-3) = 10$ ✓

#### Step 5: Rewrite the Complex-Pole Term

$$
Y(s) = \frac{1}{s+1} + \frac{-s - 3}{s^2 + 4s + 13}
$$

Complete the square in the denominator: $s^2 + 4s + 13 = (s+2)^2 + 9 = (s+2)^2 + 3^2$

Rewrite the numerator in terms of $(s+2)$:

$$
\frac{-s-3}{(s+2)^2 + 9} = \frac{-(s+2) - 1}{(s+2)^2 + 9}
$$

$$
= \frac{-(s+2)}{(s+2)^2 + 3^2} - \frac{1}{(s+2)^2 + 3^2}
$$

$$
= -\frac{(s+2)}{(s+2)^2 + 3^2} - \frac{1}{3} \cdot \frac{3}{(s+2)^2 + 3^2}
$$

#### Step 6: Inverse Transform Using Standard Pairs

Using:

- $\mathcal{L}^{-1}\left\{\dfrac{1}{s+a}\right\} = e^{-at}$
- $\mathcal{L}^{-1}\left\{\dfrac{s+a}{(s+a)^2+\beta^2}\right\} = e^{-at}\cos(\beta t)$
- $\mathcal{L}^{-1}\left\{\dfrac{\beta}{(s+a)^2+\beta^2}\right\} = e^{-at}\sin(\beta t)$

$$
y(t) = e^{-t} - e^{-2t}\cos(3t) - \frac{1}{3}e^{-2t}\sin(3t), \quad t \geq 0
$$

#### Step 7: Verify with Initial Value Theorem

$$
y(0^+) = \lim_{s\to\infty} sY(s) = \lim_{s\to\infty} \frac{10s}{(s+1)(s^2+4s+13)} = \lim_{s\to\infty} \frac{10}{s^2+5s+...} = 0
$$

From time domain: $y(0) = 1 - 1\cos(0) - \frac{1}{3}\sin(0) = 1 - 1 - 0 = 0$ ✓

#### Step 8: Verify with Final Value Theorem

$$
y(\infty) = \lim_{s\to 0} \frac{10}{(s+1)(s^2+4s+13)} = \frac{10}{(1)(13)} = \frac{10}{13}
$$

From time domain: as $t\to\infty$, all exponentials vanish except... wait, there's no $1/s$ factor, so $Y(s)$ has no pole at $s=0$. The FVT gives $\lim_{s\to 0} sY(s) = 0$. Let me recheck.

Actually, $y(\infty) = \lim_{s\to 0} s \cdot Y(s) = \lim_{s\to 0} \dfrac{10s}{(s+1)(s^2+4s+13)} = 0$.

From time domain: all three terms decay to zero as $t\to\infty$. ✓

</details>



---

## 📘 9. Appendix: Extended Derivations & Special Cases

### 9.1 — The Convolution Theorem and Inverse Laplace via Convolution

The **Convolution Theorem** is one of the most powerful results connecting the Laplace domain to the time domain. It states that multiplication in the $s$-domain corresponds to convolution in the time domain.

#### Statement of the Theorem

If $\mathcal{L}\{f(t)\} = F(s)$ and $\mathcal{L}\{g(t)\} = G(s)$, then:

$$
\mathcal{L}^{-1}\{F(s) \cdot G(s)\} = (f * g)(t) = \int_0^t f(\tau)\,g(t - \tau)\,d\tau
$$

#### Proof

Start with the definition of the Laplace transform of the convolution:

$$
\mathcal{L}\{(f*g)(t)\} = \int_0^\infty e^{-st}\left[\int_0^t f(\tau)g(t-\tau)\,d\tau\right]dt
$$

Switch the order of integration. The region of integration is $0 \leq \tau \leq t < \infty$, which is equivalent to $0 \leq \tau < \infty$ and $\tau \leq t < \infty$:

$$
= \int_0^\infty f(\tau)\left[\int_\tau^\infty e^{-st}g(t-\tau)\,dt\right]d\tau
$$

In the inner integral, substitute $u = t - \tau$, so $t = u + \tau$, $dt = du$. When $t = \tau$, $u = 0$; when $t \to \infty$, $u \to \infty$:

$$
= \int_0^\infty f(\tau)\left[\int_0^\infty e^{-s(u+\tau)}g(u)\,du\right]d\tau
$$

$$
= \int_0^\infty f(\tau)e^{-s\tau}\left[\int_0^\infty e^{-su}g(u)\,du\right]d\tau
$$

The inner integral is $G(s)$ (independent of $\tau$):

$$
= G(s)\int_0^\infty f(\tau)e^{-s\tau}\,d\tau = G(s) \cdot F(s)
$$

Therefore $\mathcal{L}\{f*g\} = F(s)G(s)$, which proves the theorem. $\blacksquare$

#### Application: Inverse Laplace via Convolution

When partial fractions are difficult (e.g., repeated complex poles), convolution provides an alternative route.

**Example:** Find $\mathcal{L}^{-1}\left\{\dfrac{1}{(s+1)(s+2)}\right\}$ using convolution.

Write $F(s) = \dfrac{1}{s+1}$ and $G(s) = \dfrac{1}{s+2}$, so $f(t) = e^{-t}$ and $g(t) = e^{-2t}$.

$$
\mathcal{L}^{-1}\{F(s)G(s)\} = \int_0^t e^{-\tau} \cdot e^{-2(t-\tau)}\,d\tau
$$

$$
= \int_0^t e^{-\tau} \cdot e^{-2t+2\tau}\,d\tau = e^{-2t}\int_0^t e^{\tau}\,d\tau
$$

$$
= e^{-2t}\left[e^{\tau}\right]_0^t = e^{-2t}(e^t - 1) = e^{-t} - e^{-2t}
$$

This matches the partial-fraction result: $\dfrac{1}{(s+1)(s+2)} = \dfrac{1}{s+1} - \dfrac{1}{s+2}$. ✓

#### Physical Interpretation in Control Systems

For a system with transfer function $G(s)$ and input $U(s)$:

$$
Y(s) = G(s) \cdot U(s) \implies y(t) = \int_0^t g(\tau)\,u(t-\tau)\,d\tau
$$

where $g(t) = \mathcal{L}^{-1}\{G(s)\}$ is the **impulse response**. The output at any time $t$ is the weighted sum of all past inputs, with the impulse response serving as the weighting function. This is the mathematical foundation of why the impulse response completely characterizes a linear time-invariant (LTI) system.

**References:** Ogata, *Modern Control Engineering*, §2-6; Åström & Murray, *Feedback Systems*, §9.2.

---

### 9.2 — Derivation of the Initial and Final Value Theorems

#### Final Value Theorem — Rigorous Derivation

**Theorem:** If all poles of $sF(s)$ lie in the open left half-plane (i.e., $f(t)$ has a finite limit as $t \to \infty$), then:

$$
\lim_{t\to\infty} f(t) = \lim_{s\to 0} sF(s)
$$

**Proof:** Start with the Laplace transform of the derivative:

$$
\mathcal{L}\{f'(t)\} = sF(s) - f(0^-)
$$

By definition:

$$
\int_0^\infty f'(t)e^{-st}\,dt = sF(s) - f(0^-)
$$

Take the limit as $s \to 0^+$:

$$
\lim_{s\to 0^+}\int_0^\infty f'(t)e^{-st}\,dt = \lim_{s\to 0^+}[sF(s) - f(0^-)]
$$

On the left side, as $s \to 0^+$, $e^{-st} \to 1$ for all finite $t$ (by the Dominated Convergence Theorem, valid when $f'(t)$ is absolutely integrable, which is guaranteed by the pole condition):

$$
\int_0^\infty f'(t)\,dt = \lim_{s\to 0} sF(s) - f(0^-)
$$

The left side evaluates to:

$$
\left[f(t)\right]_0^\infty = \lim_{t\to\infty} f(t) - f(0^-)
$$

Therefore:

$$
\lim_{t\to\infty} f(t) - f(0^-) = \lim_{s\to 0} sF(s) - f(0^-)
$$

$$
\boxed{\lim_{t\to\infty} f(t) = \lim_{s\to 0} sF(s)} \quad \blacksquare
$$

**When it fails:** If $sF(s)$ has poles on the $j\omega$-axis or in the RHP (e.g., $F(s) = 1/(s^2+1)$ which corresponds to $\sin(t)$), the limit $\lim_{t\to\infty} f(t)$ does not exist, and the FVT gives a meaningless result. Always check pole locations before applying.

#### Initial Value Theorem — Rigorous Derivation

**Theorem:** If $f(t)$ and $f'(t)$ are both Laplace-transformable, then:

$$
\lim_{t\to 0^+} f(t) = \lim_{s\to\infty} sF(s)
$$

**Proof:** Again start from:

$$
\int_0^\infty f'(t)e^{-st}\,dt = sF(s) - f(0^-)
$$

Take $s \to \infty$. For $t > 0$, $e^{-st} \to 0$ as $s \to \infty$. By the Dominated Convergence Theorem:

$$
\lim_{s\to\infty}\int_0^\infty f'(t)e^{-st}\,dt = 0
$$

Therefore:

$$
0 = \lim_{s\to\infty} sF(s) - f(0^+)
$$

$$
\boxed{f(0^+) = \lim_{s\to\infty} sF(s)} \quad \blacksquare
$$

**Practical note:** The IVT always works (no pole-location restriction) as long as $sF(s)$ is proper (degree of numerator ≤ degree of denominator). If $sF(s)$ is improper, the limit diverges, indicating an impulsive component at $t = 0$.

---

### 9.3 — Transfer Functions of Interconnected Systems: Impedance Analogy

The **impedance analogy** provides a systematic method to write transfer functions for electrical, mechanical, and thermal systems using a unified framework.

#### The Analogy Table

| Domain | Effort (Across) | Flow (Through) | Impedance $Z(s)$ |
|:---|:---|:---|:---|
| Electrical | Voltage $V$ | Current $I$ | $V(s)/I(s)$ |
| Mechanical (translational) | Force $F$ | Velocity $v$ | $F(s)/v(s)$ |
| Mechanical (rotational) | Torque $T$ | Angular velocity $\omega$ | $T(s)/\omega(s)$ |
| Thermal | Temperature $\theta$ | Heat flow $q$ | $\theta(s)/q(s)$ |

#### Impedances of Basic Elements

| Element | Electrical | Mechanical | Thermal |
|:---|:---|:---|:---|
| Resistive | $R$ | $b$ (damper) | $R_{th}$ |
| Capacitive | $1/(Cs)$ | $1/(ks)$ (spring: $k/s$) | $1/(C_{th}s)$ |
| Inductive | $Ls$ | $ms$ (mass) | — |

#### Systematic Procedure

1. Identify the input (effort or flow source) and output variable.
2. Replace each element with its $s$-domain impedance.
3. Apply circuit analysis techniques (voltage/current dividers, mesh/node analysis).
4. The transfer function emerges directly from the impedance network.

#### Example: Series RLC as Voltage Divider

Input: $V_{in}(s)$. Output: $V_C(s)$ (voltage across capacitor).

The three impedances in series: $Z_R = R$, $Z_L = Ls$, $Z_C = 1/(Cs)$.

By voltage divider:

$$
G(s) = \frac{V_C}{V_{in}} = \frac{Z_C}{Z_R + Z_L + Z_C} = \frac{1/(Cs)}{R + Ls + 1/(Cs)}
$$

Multiply numerator and denominator by $Cs$:

$$
G(s) = \frac{1}{LCs^2 + RCs + 1}
$$

This is identical to the result derived from KVL in Section 5.4, but obtained in one line using the impedance method.

**References:** Nise, *Control Systems Engineering*, Ch. 2; MIT OCW 16.30, Lecture 2; Brian Douglas, "Transfer Function of Electrical Systems" (YouTube).
