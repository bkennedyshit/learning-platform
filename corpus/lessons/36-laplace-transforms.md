---
title: "Laplace Transforms"
subject: "Ordinary & Partial Differential Equations"
catalog: advanced
audience_tier: higher-education
chapter: "3.6"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 3.6 — Laplace Transforms

> *"The Laplace transform converts differential equations into algebraic equations — calculus becomes algebra, and initial conditions are built in from the start."* — MIT OCW 18.03

The Laplace transform $\mathcal{L}\{f(t)\} = F(s)$ maps functions of time into functions of a complex frequency variable $s$. Differentiation becomes multiplication by $s$, convolution becomes multiplication, and discontinuous forcing (step functions, impulses) is handled effortlessly. This chapter develops the transform, its properties, the inverse transform via partial fractions, and applications to IVPs and transfer functions.

---

## 🎯 Learning Objectives

1. Define the Laplace transform and state its region of convergence.
2. Compute transforms of elementary functions: $e^{at}$, $t^n$, $\sin\omega t$, $\cos\omega t$.
3. Apply the differentiation property: $\mathcal{L}\{f'\} = sF(s) - f(0)$.
4. Use the $s$-shifting and $t$-shifting theorems.
5. Compute inverse Laplace transforms via partial fraction decomposition.
6. Solve IVPs by transforming, solving algebraically, and inverting.
7. Apply the convolution theorem: $\mathcal{L}\{f*g\} = F(s)G(s)$.
8. Handle Heaviside step functions and Dirac delta forcing.

---

## 🖼️ Visual Anchor — Time Domain to $s$-Domain Pipeline

![math-03__3.6-fig1](math-03__3.6-fig1.svg)

---

## 📚 1. Definitions

### Definition 3.6.1 — Laplace Transform

The **Laplace transform** of $f(t)$ (defined for $t \geq 0$) is:

$$
F(s) = \mathcal{L}\{f(t)\} = \int_0^{\infty} e^{-st}f(t)\,dt,
$$

provided the integral converges for $\text{Re}(s) > \sigma_0$ (the abscissa of convergence).

### Definition 3.6.2 — Inverse Laplace Transform

The **inverse Laplace transform** recovers $f(t)$ from $F(s)$:

$$
f(t) = \mathcal{L}^{-1}\{F(s)\} = \frac{1}{2\pi i}\int_{\gamma-i\infty}^{\gamma+i\infty}e^{st}F(s)\,ds,
$$

where $\gamma > \sigma_0$. In practice, we use partial fractions and a table of known transforms.

### Definition 3.6.3 — Convolution

The **convolution** of $f$ and $g$ is:

$$
(f * g)(t) = \int_0^t f(\tau)\,g(t-\tau)\,d\tau.
$$

### Definition 3.6.4 — Transfer Function

For a linear system $ay'' + by' + cy = g(t)$ with zero initial conditions, the **transfer function** is:

$$
H(s) = \frac{1}{as^2 + bs + c}.
$$

The output transform is $Y(s) = H(s)\cdot G(s)$.

---

## 📐 2. Axioms / Postulates

**Postulate 3.6.P1 (Linearity):** $\mathcal{L}\{\alpha f + \beta g\} = \alpha F(s) + \beta G(s)$.

**Postulate 3.6.P2 (Uniqueness — Lerch's Theorem):** If $F(s) = G(s)$ for all $s$ in a half-plane, then $f(t) = g(t)$ almost everywhere for $t > 0$.

---

## 🛡️ 3. Lemmas

### Lemma 3.6.1 — Fundamental Transform Table

| $f(t)$ | $F(s) = \mathcal{L}\{f\}$ | Region |
|---------|---------------------------|--------|
| $1$ | $1/s$ | $s > 0$ |
| $t^n$ | $n!/s^{n+1}$ | $s > 0$ |
| $e^{at}$ | $1/(s-a)$ | $s > a$ |
| $\sin\omega t$ | $\omega/(s^2+\omega^2)$ | $s > 0$ |
| $\cos\omega t$ | $s/(s^2+\omega^2)$ | $s > 0$ |
| $e^{at}\sin\omega t$ | $\omega/((s-a)^2+\omega^2)$ | $s > a$ |
| $t^n e^{at}$ | $n!/(s-a)^{n+1}$ | $s > a$ |
| $\delta(t)$ | $1$ | all $s$ |
| $u(t-a)$ | $e^{-as}/s$ | $s > 0$ |

### Lemma 3.6.2 — Differentiation Property

$$
\mathcal{L}\{f'(t)\} = sF(s) - f(0), \qquad \mathcal{L}\{f''(t)\} = s^2F(s) - sf(0) - f'(0).
$$

**Proof.** Integrate by parts: $\int_0^\infty e^{-st}f'(t)\,dt = [e^{-st}f(t)]_0^\infty + s\int_0^\infty e^{-st}f(t)\,dt = -f(0) + sF(s)$. $\blacksquare$

### Lemma 3.6.3 — $s$-Shifting (First Shifting Theorem)

$$
\mathcal{L}\{e^{at}f(t)\} = F(s-a).
$$

### Lemma 3.6.4 — $t$-Shifting (Second Shifting Theorem)

$$
\mathcal{L}\{u(t-a)f(t-a)\} = e^{-as}F(s),
$$

where $u(t-a)$ is the Heaviside step function.

---

## 👑 4. Theorems

### Theorem 3.6.1 — Convolution Theorem

$$
\mathcal{L}\{f * g\} = F(s)\cdot G(s).
$$

### Theorem 3.6.2 — Solving IVPs via Laplace Transform

For $ay'' + by' + cy = g(t)$, $y(0) = y_0$, $y'(0) = y_0'$:

$$
(as^2 + bs + c)Y(s) = G(s) + a[sy_0 + y_0'] + by_0.
$$

Solve for $Y(s)$, then invert: $y(t) = \mathcal{L}^{-1}\{Y(s)\}$.

---

## ✍️ 5. Proofs / Derivations

### 5.1 Proof of Convolution Theorem

**Step 1.** Compute $\mathcal{L}\{f*g\}$:

$$
\mathcal{L}\{f*g\} = \int_0^\infty e^{-st}\left[\int_0^t f(\tau)g(t-\tau)\,d\tau\right]dt.
$$

**Step 2.** Switch order of integration (Fubini). The region is $0 \leq \tau \leq t < \infty$, equivalently $0 \leq \tau < \infty$, $\tau \leq t < \infty$:

$$
= \int_0^\infty f(\tau)\left[\int_\tau^\infty e^{-st}g(t-\tau)\,dt\right]d\tau.
$$

**Step 3.** Substitute $u = t - \tau$ in the inner integral ($t = u + \tau$, $dt = du$):

$$
= \int_0^\infty f(\tau)\left[\int_0^\infty e^{-s(u+\tau)}g(u)\,du\right]d\tau = \int_0^\infty f(\tau)e^{-s\tau}\,d\tau \cdot \int_0^\infty g(u)e^{-su}\,du.
$$

$$
= F(s)\cdot G(s). \quad \blacksquare
$$

---

## 🧮 6. Worked Examples

### Example 3.6.E1 — Basic IVP

**Solve:** $y'' + 3y' + 2y = 0$, $y(0) = 1$, $y'(0) = 0$.

**Step 1.** Transform: $(s^2 + 3s + 2)Y = s + 3$ (using $y(0)=1$, $y'(0)=0$).

**Step 2.** $Y(s) = \frac{s+3}{(s+1)(s+2)}$.

**Step 3.** Partial fractions: $\frac{s+3}{(s+1)(s+2)} = \frac{A}{s+1} + \frac{B}{s+2}$.

$s = -1$: $A = \frac{-1+3}{-1+2} = 2$. $s = -2$: $B = \frac{-2+3}{-2+1} = -1$.

**Step 4.** Invert: $y(t) = 2e^{-t} - e^{-2t}$.

---

### Example 3.6.E2 — Forced System with Step Function

**Solve:** $y'' + y = u(t-\pi)$, $y(0) = 0$, $y'(0) = 1$.

**Step 1.** Transform: $(s^2+1)Y = 1 + \frac{e^{-\pi s}}{s}$.

**Step 2.** $Y = \frac{1}{s^2+1} + \frac{e^{-\pi s}}{s(s^2+1)}$.

**Step 3.** Partial fractions for $\frac{1}{s(s^2+1)} = \frac{1}{s} - \frac{s}{s^2+1}$.

**Step 4.** Invert using $t$-shifting:

$$
y(t) = \sin t + u(t-\pi)[1 - \cos(t-\pi)].
$$

Since $\cos(t-\pi) = -\cos t$: $y(t) = \sin t + u(t-\pi)(1+\cos t)$.

---

### Example 3.6.E3 — Convolution

**Find** $\mathcal{L}^{-1}\left\{\frac{1}{(s+1)(s+2)}\right\}$ using convolution.

$F(s) = \frac{1}{s+1}$, $G(s) = \frac{1}{s+2}$. So $f = e^{-t}$, $g = e^{-2t}$.

$$
(f*g)(t) = \int_0^t e^{-\tau}e^{-2(t-\tau)}\,d\tau = e^{-2t}\int_0^t e^{\tau}\,d\tau = e^{-2t}(e^t - 1) = e^{-t} - e^{-2t}.
$$

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- [3.2 - Second-Order Linear Homogeneous ODEs](3.2---Second-Order-Linear-Homogeneous-ODEs) — characteristic equation appears as denominator of $Y(s)$
- [3.3 - Nonhomogeneous ODEs & Undetermined Coefficients](3.3---Nonhomogeneous-ODEs-&-Undetermined-Coefficients) — Laplace is an alternative to undetermined coefficients
- [3.5 - Fourier Series & Boundary Value Problems](3.5---Fourier-Series-&-Boundary-Value-Problems) — Fourier transform is the imaginary-axis restriction of Laplace

### External References
- **MIT OCW 18.03SC**, Unit on Laplace Transforms
- **Jiří Lebl**, *Notes on Diffy Qs*, Ch. 6
- **Alan V. Oppenheim**, *Signals and Systems* (for transfer function perspective)

---



---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — Second-Order IVP with Discontinuous Forcing (Heaviside Step)

Solve $y'' + 4y = u(t-\pi) \cdot \sin(t)$, with $y(0) = 0$, $y'(0) = 1$, where $u(t-\pi)$ is the unit step function.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Take the Laplace transform of both sides

$$
\mathcal{L}\{y''\} + 4\mathcal{L}\{y\} = \mathcal{L}\{u(t-\pi)\sin t\}.
$$

Using $\mathcal{L}\{y''\} = s^2Y - sy(0) - y'(0) = s^2Y - 1$:

$$
s^2Y - 1 + 4Y = \mathcal{L}\{u(t-\pi)\sin t\}.
$$

#### Step 2: Handle the right side using the second shifting theorem

Write $\sin t = -\sin(t - \pi)$ (since $\sin(t) = -\sin(t-\pi)$). Actually, let's use the direct formula. For $u(t-a)f(t)$:

$$
\mathcal{L}\{u(t-\pi)\sin t\} = e^{-\pi s}\mathcal{L}\{\sin(t+\pi)\} = e^{-\pi s}\mathcal{L}\{-\sin t\} = \frac{-e^{-\pi s}}{s^2+1}.
$$

#### Step 3: Solve for $Y(s)$

$$
(s^2 + 4)Y = 1 - \frac{e^{-\pi s}}{s^2+1}.
$$

$$
Y(s) = \frac{1}{s^2+4} - \frac{e^{-\pi s}}{(s^2+1)(s^2+4)}.
$$

#### Step 4: Partial fractions on the second term

$$
\frac{1}{(s^2+1)(s^2+4)} = \frac{A s + B}{s^2+1} + \frac{Cs + D}{s^2+4}.
$$

Multiply through: $1 = (As+B)(s^2+4) + (Cs+D)(s^2+1)$.

Set $s^2 = -1$: $1 = (As+B)(3)$, so comparing: $B \cdot 3 = 1 \implies B = 1/3$, $A = 0$.

Set $s^2 = -4$: $1 = (Cs+D)(-3)$, so $D = -1/3$, $C = 0$.

$$
\frac{1}{(s^2+1)(s^2+4)} = \frac{1/3}{s^2+1} - \frac{1/3}{s^2+4}.
$$

#### Step 5: Invert term by term

First term: $\mathcal{L}^{-1}\left\{\frac{1}{s^2+4}\right\} = \frac{1}{2}\sin 2t$.

Second term (with time shift $e^{-\pi s}$): Let $g(t) = \frac{1}{3}\sin t - \frac{1}{6}\sin 2t$. Then:

$$
\mathcal{L}^{-1}\left\{\frac{e^{-\pi s}}{(s^2+1)(s^2+4)}\right\} = u(t-\pi)\,g(t-\pi).
$$

Compute $g(t-\pi) = \frac{1}{3}\sin(t-\pi) - \frac{1}{6}\sin 2(t-\pi) = -\frac{1}{3}\sin t - \frac{1}{6}\sin 2t$.

**Final Answer:**

$$
y(t) = \frac{1}{2}\sin 2t + u(t-\pi)\left(\frac{1}{3}\sin t + \frac{1}{6}\sin 2t\right).
$$

For $t \lt  \pi$: $y = \frac{1}{2}\sin 2t$ (free oscillation). For $t \gt  \pi$: the forcing kicks in and adds a beat pattern.

</details>

### Example 8.2 — Solving a System of ODEs via Laplace Transforms

Solve the coupled system:

$$
x' = 2x - 3y, \quad y' = x - 2y, \quad x(0) = 1, \quad y(0) = 0.
$$

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Transform both equations

$$
sX - 1 = 2X - 3Y \implies (s-2)X + 3Y = 1. \tag{i}
$$

$$
sY - 0 = X - 2Y \implies -X + (s+2)Y = 0. \tag{ii}
$$

#### Step 2: Solve the algebraic system

From (ii): $X = (s+2)Y$.

Substitute into (i): $(s-2)(s+2)Y + 3Y = 1 \implies (s^2 - 4 + 3)Y = 1 \implies (s^2 - 1)Y = 1$.

$$
Y(s) = \frac{1}{s^2-1} = \frac{1}{(s-1)(s+1)}.
$$

$$
X(s) = (s+2)Y = \frac{s+2}{(s-1)(s+1)}.
$$

#### Step 3: Partial fractions for $Y$

$$
\frac{1}{(s-1)(s+1)} = \frac{1/2}{s-1} - \frac{1/2}{s+1}.
$$

$$
y(t) = \frac{1}{2}e^t - \frac{1}{2}e^{-t} = \sinh t.
$$

#### Step 4: Partial fractions for $X$

$$
\frac{s+2}{(s-1)(s+1)} = \frac{A}{s-1} + \frac{B}{s+1}.
$$

$A = \frac{1+2}{1+1} = \frac{3}{2}$, $B = \frac{-1+2}{-1-1} = -\frac{1}{2}$.

$$
x(t) = \frac{3}{2}e^t - \frac{1}{2}e^{-t}.
$$

**Final Answer:**

$$
x(t) = \frac{3}{2}e^t - \frac{1}{2}e^{-t}, \qquad y(t) = \frac{1}{2}e^t - \frac{1}{2}e^{-t}.
$$

**Verification:** $x' = \frac{3}{2}e^t + \frac{1}{2}e^{-t}$. And $2x - 3y = 3e^t - e^{-t} - \frac{3}{2}e^t + \frac{3}{2}e^{-t} = \frac{3}{2}e^t + \frac{1}{2}e^{-t}$. ✓

</details>

### Example 8.3 — Impulse Response: Delta Function Forcing

A damped oscillator $y'' + 2y' + 5y = \delta(t-1)$ with $y(0) = 0$, $y'(0) = 0$. Find $y(t)$.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Laplace transform

$$
s^2Y + 2sY + 5Y = e^{-s} \implies Y(s) = \frac{e^{-s}}{s^2 + 2s + 5}.
$$

#### Step 2: Complete the square in the denominator

$$
s^2 + 2s + 5 = (s+1)^2 + 4.
$$

So $Y(s) = \frac{e^{-s}}{(s+1)^2 + 4}$.

#### Step 3: Identify the inverse transform

Without the shift: $\mathcal{L}^{-1}\left\{\frac{1}{(s+1)^2+4}\right\} = \frac{1}{2}e^{-t}\sin 2t$.

With the time shift $e^{-s}$ (delay by 1):

$$
y(t) = u(t-1) \cdot \frac{1}{2}e^{-(t-1)}\sin 2(t-1).
$$

**Final Answer:**

$$
y(t) = \begin{cases} 0 & t \lt  1, \\ \frac{1}{2}e^{-(t-1)}\sin 2(t-1) & t \geq 1. \end{cases}
$$

This is the **impulse response** (Green's function) of the system, delayed to $t = 1$. The system is quiescent until the impulse arrives, then rings at the damped frequency $\omega_d = 2$ rad/s with exponential decay rate $\alpha = 1$.

</details>

### Example 8.4 — Convolution Integral: Solving an Integro-Differential Equation

Solve $y(t) + 2\int_0^t e^{-(t-\tau)}y(\tau)\,d\tau = e^{-t}$.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Recognize the convolution structure

The integral $\int_0^t e^{-(t-\tau)}y(\tau)\,d\tau = (e^{-t} * y)(t)$ is a convolution.

#### Step 2: Take the Laplace transform

$$
Y(s) + 2\,\mathcal{L}\{e^{-t}\} \cdot Y(s) = \mathcal{L}\{e^{-t}\}.
$$

Using the convolution theorem $\mathcal{L}\{f*g\} = F(s)G(s)$:

$$
Y(s) + \frac{2}{s+1}Y(s) = \frac{1}{s+1}.
$$

#### Step 3: Solve for $Y(s)$

$$
Y(s)\left(1 + \frac{2}{s+1}\right) = \frac{1}{s+1}.
$$

$$
Y(s) \cdot \frac{s+1+2}{s+1} = \frac{1}{s+1} \implies Y(s) \cdot \frac{s+3}{s+1} = \frac{1}{s+1}.
$$

$$
Y(s) = \frac{1}{s+3}.
$$

#### Step 4: Invert

**Final Answer:**

$$
y(t) = e^{-3t}.
$$

**Verification:** $e^{-3t} + 2\int_0^t e^{-(t-\tau)}e^{-3\tau}\,d\tau = e^{-3t} + 2e^{-t}\int_0^t e^{-2\tau}\,d\tau = e^{-3t} + 2e^{-t}\cdot\frac{1-e^{-2t}}{2} = e^{-3t} + e^{-t} - e^{-3t} = e^{-t}$. ✓

</details>



### Example 8.5 — Transfer Function and Bode Plot Interpretation

For the system $y'' + 3y' + 2y = f(t)$, find the transfer function $H(s)$ and determine the steady-state response to $f(t) = 5\cos(4t)$.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Transfer function

With zero initial conditions, $\mathcal{L}\{y\} = H(s)\mathcal{L}\{f\}$ where:

$$
H(s) = \frac{1}{s^2 + 3s + 2} = \frac{1}{(s+1)(s+2)}.
$$

#### Step 2: Frequency response at $\omega = 4$

Evaluate $H(j\omega)$ at $\omega = 4$ (substitute $s = 4i$):

$$
H(4i) = \frac{1}{(4i)^2 + 3(4i) + 2} = \frac{1}{-16 + 12i + 2} = \frac{1}{-14 + 12i}.
$$

#### Step 3: Compute magnitude and phase

$$
|H(4i)| = \frac{1}{\sqrt{196 + 144}} = \frac{1}{\sqrt{340}} = \frac{1}{2\sqrt{85}} \approx 0.0543.
$$

$$
\angle H(4i) = -\arctan\frac{12}{-14} = -(\pi - \arctan\frac{12}{14}) = -(180° - 40.6°) = -139.4°.
$$

(Since the real part is negative and imaginary part is positive, the angle is in the second quadrant: $\angle = \pi - \arctan(12/14) \approx 2.43$ rad. With the negative sign convention for the transfer function response: $\phi = -\pi + \arctan(6/7) \approx -2.43$ rad.)

#### Step 4: Steady-state output

For input $5\cos(4t)$, the steady-state output is:

$$
y_{ss}(t) = 5|H(4i)|\cos(4t + \angle H(4i)) = \frac{5}{2\sqrt{85}}\cos(4t - 2.43).
$$

**Final Answer:**

$$
y_{ss}(t) \approx 0.271\cos(4t - 139.4°).
$$

The system attenuates the input by a factor of ~18 (about $-25$ dB) and introduces a phase lag of $139.4°$. This is characteristic of a second-order low-pass filter driven well above its natural frequencies ($\omega_n = \sqrt{2} \approx 1.41$ rad/s).

</details>

---

## 📘 9. Appendix: Extended Derivations & Special Cases

### 9.1 Derivation of $\mathcal{L}\{t^n\}$ by Induction on Integration by Parts

We derive the transform $\mathcal{L}\{t^n\} = n!/s^{n+1}$ rigorously using repeated integration by parts.

**Base case ($n = 0$):**

$$
\mathcal{L}\{1\} = \int_0^{\infty} e^{-st}\,dt = \left[-\frac{e^{-st}}{s}\right]_0^{\infty} = \frac{1}{s}, \quad s > 0.
$$

**Inductive step.** Assume $\mathcal{L}\{t^{n-1}\} = (n-1)!/s^n$. Compute $\mathcal{L}\{t^n\}$ by integration by parts with $u = t^n$, $dv = e^{-st}\,dt$:

$$
\mathcal{L}\{t^n\} = \int_0^{\infty} t^n e^{-st}\,dt = \left[-\frac{t^n e^{-st}}{s}\right]_0^{\infty} + \frac{n}{s}\int_0^{\infty} t^{n-1}e^{-st}\,dt.
$$

The boundary term vanishes: at $t = 0$, $t^n = 0$; at $t = \infty$, $t^n e^{-st} \to 0$ for $s > 0$ (exponential dominates polynomial). Therefore:

$$
\mathcal{L}\{t^n\} = \frac{n}{s}\mathcal{L}\{t^{n-1}\} = \frac{n}{s}\cdot\frac{(n-1)!}{s^n} = \frac{n!}{s^{n+1}}.
$$

**Alternative derivation via the $s$-derivative property.** Since $\mathcal{L}\{t\,f(t)\} = -F'(s)$, we have:

$$
\mathcal{L}\{t^n\} = (-1)^n \frac{d^n}{ds^n}\mathcal{L}\{1\} = (-1)^n \frac{d^n}{ds^n}\left(\frac{1}{s}\right) = (-1)^n \cdot \frac{(-1)^n n!}{s^{n+1}} = \frac{n!}{s^{n+1}}.
$$

This uses $\frac{d^n}{ds^n}(s^{-1}) = (-1)^n n!\,s^{-(n+1)}$, which follows from the power rule for derivatives applied $n$ times.

**Connection to the Gamma function.** For non-integer $\alpha > -1$:

$$
\mathcal{L}\{t^{\alpha}\} = \int_0^{\infty} t^{\alpha}e^{-st}\,dt = \frac{\Gamma(\alpha+1)}{s^{\alpha+1}},
$$

where $\Gamma(\alpha+1) = \int_0^{\infty} u^{\alpha}e^{-u}\,du$ (substituting $u = st$). For integer $\alpha = n$, $\Gamma(n+1) = n!$, recovering our formula. This extension allows Laplace transforms of fractional powers like $t^{1/2}$: $\mathcal{L}\{t^{1/2}\} = \Gamma(3/2)/s^{3/2} = \frac{\sqrt{\pi}}{2s^{3/2}}$.

*Reference: Jiří Lebl, Notes on Diffy Qs, §6.1; Schiff, The Laplace Transform: Theory and Applications (Springer, 1999), Ch. 1.*



### 9.2 The Convolution Theorem — Proof and Applications

**Theorem.** If $F(s) = \mathcal{L}\{f\}$ and $G(s) = \mathcal{L}\{g\}$, then:

$$
\mathcal{L}\{(f * g)(t)\} = F(s)\cdot G(s), \quad \text{where } (f*g)(t) = \int_0^t f(\tau)\,g(t-\tau)\,d\tau.
$$

**Proof.** Start from the product $F(s)G(s)$:

$$
F(s)G(s) = \left(\int_0^{\infty}f(\tau)e^{-s\tau}\,d\tau\right)\left(\int_0^{\infty}g(\sigma)e^{-s\sigma}\,d\sigma\right) = \int_0^{\infty}\int_0^{\infty}f(\tau)g(\sigma)e^{-s(\tau+\sigma)}\,d\tau\,d\sigma.
$$

Substitute $t = \tau + \sigma$ (so $\sigma = t - \tau$, $d\sigma = dt$). The region $\tau \geq 0$, $\sigma \geq 0$ becomes $t \geq 0$, $0 \leq \tau \leq t$:

$$
= \int_0^{\infty}\left(\int_0^t f(\tau)g(t-\tau)\,d\tau\right)e^{-st}\,dt = \int_0^{\infty}(f*g)(t)\,e^{-st}\,dt = \mathcal{L}\{f*g\}.
$$

The change of variables is justified by Fubini's theorem (absolute convergence of the double integral for $\text{Re}(s)$ sufficiently large).

**Key applications:**

1. **Inverse transforms of products.** $\mathcal{L}^{-1}\{F(s)G(s)\} = f * g$. This avoids partial fractions when factors are complicated.

2. **Integral equations.** Equations of the form $y(t) = f(t) + \int_0^t k(t-\tau)y(\tau)\,d\tau$ (Volterra equations of the second kind) transform to $Y = F + K \cdot Y$, giving $Y = F/(1-K)$.

3. **Duhamel's principle.** The solution to $Ly = g(t)$ with zero ICs is $y = h * g$ where $h$ is the impulse response ($Lh = \delta$). This is the Laplace-domain statement: $Y(s) = H(s)G(s)$.

**Commutativity and associativity.** Convolution is commutative ($f*g = g*f$), associative ($(f*g)*h = f*(g*h)$), and distributive over addition. The identity element is $\delta(t)$: $f * \delta = f$. These algebraic properties make the set of causal functions (with convolution as multiplication) into a commutative ring — the operational calculus of Heaviside.

*Reference: MIT OCW 18.03SC, Lecture on Convolution; Oppenheim & Willsky, Signals and Systems, §2.4.*

### 9.3 The Bromwich Inversion Integral and Analytic Continuation

The formal inverse Laplace transform is given by the **Bromwich integral** (also called the Mellin inversion formula):

$$
f(t) = \mathcal{L}^{-1}\{F(s)\} = \frac{1}{2\pi i}\int_{\gamma - i\infty}^{\gamma + i\infty} F(s)\,e^{st}\,ds,
$$

where $\gamma$ is any real number greater than the real part of all singularities of $F(s)$ (i.e., the contour lies in the region of convergence).

**Why this works (heuristic).** The Laplace transform is essentially a Fourier transform of $f(t)e^{-\gamma t}$ (evaluated along the vertical line $\text{Re}(s) = \gamma$). The Bromwich integral is the inverse Fourier transform, shifted back.

**Practical evaluation via residues.** For rational $F(s) = P(s)/Q(s)$ with $\deg P < \deg Q$, close the Bromwich contour with a large semicircle in the left half-plane (for $t > 0$, Jordan's lemma guarantees the semicircular arc contributes zero). Then by the residue theorem:

$$
f(t) = \sum_k \text{Res}_{s=s_k}\left[F(s)e^{st}\right],
$$

where the sum is over all poles $s_k$ of $F(s)$.

**Example.** $F(s) = \frac{1}{(s-1)(s-2)}$. Poles at $s = 1, 2$.

$$
\text{Res}_{s=1} = \frac{e^t}{1-2} = -e^t, \qquad \text{Res}_{s=2} = \frac{e^{2t}}{2-1} = e^{2t}.
$$

$$
f(t) = -e^t + e^{2t} = e^{2t} - e^t.
$$

This matches the partial fractions result: $\frac{1}{(s-1)(s-2)} = \frac{-1}{s-1} + \frac{1}{s-2}$.

**Branch cuts.** When $F(s)$ has branch points (e.g., $F(s) = 1/\sqrt{s}$), the Bromwich contour must be deformed around the branch cut. This leads to integral representations of the inverse transform rather than simple residue sums. For $F(s) = 1/\sqrt{s}$: $f(t) = 1/\sqrt{\pi t}$ (derived via the Hankel contour).

**Region of convergence (ROC).** The Laplace transform $F(s) = \int_0^{\infty}f(t)e^{-st}\,dt$ converges absolutely for $\text{Re}(s) > \sigma_0$ (the abscissa of convergence). Different functions can have the same $F(s)$ formula but different ROCs — the ROC disambiguates. For causal (one-sided) transforms, the ROC is always a right half-plane.

*Reference: Schiff, The Laplace Transform (Springer, 1999), Ch. 4; Arfken & Weber, Mathematical Methods for Physicists, §15.12.*

---



### 9.4 The Initial and Final Value Theorems

Two powerful results allow extraction of limiting behavior directly from $F(s)$ without inverting:

**Initial Value Theorem.** If $f(t)$ and $f'(t)$ are both Laplace-transformable, then:

$$
\lim_{t \to 0^+} f(t) = \lim_{s \to \infty} sF(s).
$$

**Proof.** From $\mathcal{L}\{f'\} = sF(s) - f(0^+)$:

$$
\int_0^{\infty}f'(t)e^{-st}\,dt = sF(s) - f(0^+).
$$

As $s \to \infty$, the left side $\to 0$ (dominated convergence, since $e^{-st} \to 0$ for $t > 0$). Therefore $\lim_{s\to\infty}sF(s) = f(0^+)$.

**Final Value Theorem.** If $f(t)$ has a finite limit as $t \to \infty$ and all poles of $sF(s)$ have negative real parts (except possibly a simple pole at $s = 0$), then:

$$
\lim_{t \to \infty} f(t) = \lim_{s \to 0} sF(s).
$$

**Proof.** From $\mathcal{L}\{f'\} = sF(s) - f(0^+)$:

$$
\int_0^{\infty}f'(t)e^{-st}\,dt = sF(s) - f(0^+).
$$

As $s \to 0^+$: $\int_0^{\infty}f'(t)\,dt = f(\infty) - f(0^+)$. Therefore $f(\infty) - f(0^+) = \lim_{s\to 0}sF(s) - f(0^+)$, giving $f(\infty) = \lim_{s\to 0}sF(s)$.

**Application (control systems).** For a unity-feedback system with open-loop transfer function $G(s)$, the steady-state error to a unit step input is:

$$
e_{ss} = \lim_{s\to 0}s\cdot\frac{1}{1+G(s)}\cdot\frac{1}{s} = \frac{1}{1+G(0)} = \frac{1}{1+K_p},
$$

where $K_p = G(0)$ is the position error constant. This is the foundation of steady-state error analysis in control theory.

**Caution.** The Final Value Theorem gives WRONG answers if $sF(s)$ has poles with $\text{Re}(s) \geq 0$ (other than at $s = 0$). For example, $F(s) = 1/(s^2+1)$ gives $f(t) = \sin t$, which has no limit as $t \to \infty$. Blindly applying FVT: $\lim_{s\to 0}s/(s^2+1) = 0$ — incorrect (the limit doesn't exist). Always check the pole condition first.

*Reference: Oppenheim & Willsky, Signals and Systems (Prentice Hall, 1997), §9.7; Franklin, Powell & Emami-Naeini, Feedback Control of Dynamic Systems, §3.3.*

### 9.5 Laplace Transform Solution of PDEs — The Heat Equation on a Semi-Infinite Rod

The Laplace transform can solve PDEs by transforming in the time variable, reducing the PDE to an ODE in space.

**Problem.** Solve $u_t = u_{xx}$ for $x > 0$, $t > 0$, with $u(x,0) = 0$ and $u(0,t) = 1$ (sudden heating at the boundary).

**Step 1: Transform in $t$.** Let $U(x,s) = \mathcal{L}\{u(x,t)\}$. Then $\mathcal{L}\{u_t\} = sU - u(x,0) = sU$ and $\mathcal{L}\{u_{xx}\} = U_{xx}$ (since $x$ is not the transform variable).

The PDE becomes the ODE:

$$
sU = U_{xx} \implies U_{xx} - sU = 0.
$$

**Step 2: Solve the ODE.** General solution: $U(x,s) = Ae^{\sqrt{s}\,x} + Be^{-\sqrt{s}\,x}$.

Boundedness as $x \to \infty$ requires $A = 0$ (taking $\text{Re}(\sqrt{s}) > 0$).

BC at $x = 0$: $U(0,s) = \mathcal{L}\{1\} = 1/s$. So $B = 1/s$.

$$
U(x,s) = \frac{1}{s}e^{-\sqrt{s}\,x}.
$$

**Step 3: Invert.** Using the known transform pair $\mathcal{L}^{-1}\{e^{-a\sqrt{s}}/s\} = \text{erfc}(a/(2\sqrt{t}))$:

$$
u(x,t) = \text{erfc}\left(\frac{x}{2\sqrt{t}}\right) = 1 - \text{erf}\left(\frac{x}{2\sqrt{t}}\right).
$$

This is the classic **error function solution** for heat conduction into a semi-infinite solid. The thermal penetration depth grows as $\delta \sim \sqrt{t}$ — the hallmark of diffusive processes.

*Reference: Carslaw & Jaeger, Conduction of Heat in Solids (Oxford, 1959), §2.5; Lebl, Notes on Diffy Qs, §6.4.*

---



### 9.6 Table of Common Laplace Transform Pairs — Derivations

The following transforms are used constantly. We derive the non-obvious ones.

**$\mathcal{L}\{\cos(\omega t)\} = s/(s^2 + \omega^2)$:**

Using Euler's formula: $\cos\omega t = \text{Re}(e^{i\omega t})$. Since $\mathcal{L}\{e^{i\omega t}\} = 1/(s - i\omega)$:

$$
\mathcal{L}\{\cos\omega t\} = \text{Re}\frac{1}{s-i\omega} = \text{Re}\frac{s+i\omega}{s^2+\omega^2} = \frac{s}{s^2+\omega^2}.
$$

**$\mathcal{L}\{t^n e^{at}\} = n!/(s-a)^{n+1}$:**

By the first shifting theorem: $\mathcal{L}\{e^{at}f(t)\} = F(s-a)$. With $f(t) = t^n$, $F(s) = n!/s^{n+1}$:

$$
\mathcal{L}\{t^n e^{at}\} = \frac{n!}{(s-a)^{n+1}}.
$$

**$\mathcal{L}\{t\sin\omega t\} = 2\omega s/(s^2+\omega^2)^2$:**

Using the $s$-derivative property $\mathcal{L}\{tf(t)\} = -F'(s)$ with $f = \sin\omega t$, $F = \omega/(s^2+\omega^2)$:

$$
-F'(s) = -\omega\cdot\frac{-2s}{(s^2+\omega^2)^2} = \frac{2\omega s}{(s^2+\omega^2)^2}.
$$

**$\mathcal{L}\{\text{erfc}(a/(2\sqrt{t}))\} = e^{-a\sqrt{s}}/s$ (for $a > 0$):**

This is derived by solving the heat equation on a semi-infinite rod (see §9.5) and reading off the transform pair. It can also be verified by direct integration using the substitution $\tau = a/(2\sqrt{t})$ and properties of the complementary error function.

**$\mathcal{L}\{J_0(\omega t)\} = 1/\sqrt{s^2 + \omega^2}$:**

Where $J_0$ is the Bessel function of the first kind. This is derived from the integral representation $J_0(t) = \frac{1}{\pi}\int_0^{\pi}\cos(t\sin\theta)\,d\theta$ and interchanging the order of integration with the Laplace integral. The result involves the generating function for Bessel functions.

These pairs, combined with the shifting theorems and convolution, suffice to solve the vast majority of engineering ODE/PDE problems via Laplace transforms.

*Reference: Spiegel, Schaum's Outline of Laplace Transforms (McGraw-Hill, 1965); Schiff, The Laplace Transform (Springer, 1999), Appendix.*

---



### 9.7 The $s$-Domain and Stability: Pole-Zero Analysis

The transfer function $H(s) = N(s)/D(s)$ encodes the complete input-output behavior of a linear time-invariant system. Its poles (roots of $D(s)$) and zeros (roots of $N(s)$) determine stability, frequency response, and transient behavior.

**Stability criterion.** A system is BIBO (bounded-input, bounded-output) stable if and only if all poles of $H(s)$ lie in the open left half-plane: $\text{Re}(s_k) < 0$ for all poles $s_k$.

**Pole locations and time-domain behavior:**
- Real pole at $s = -a$ ($a > 0$): exponential decay $e^{-at}$ with time constant $\tau = 1/a$.
- Complex conjugate poles at $s = -\sigma \pm j\omega_d$: damped oscillation $e^{-\sigma t}\cos(\omega_d t + \phi)$.
- Pole on imaginary axis $s = \pm j\omega$: sustained oscillation (marginally stable).
- Pole in right half-plane: exponential growth (unstable).

**The Routh–Hurwitz criterion** determines whether all roots of a polynomial have negative real parts without actually computing the roots — essential for stability analysis of high-order systems where factoring is impractical.

For a third-order system $s^3 + as^2 + bs + c = 0$: all roots have $\text{Re}(s) < 0$ if and only if $a > 0$, $c > 0$, and $ab > c$.

*Reference: Franklin, Powell & Emami-Naeini, Feedback Control of Dynamic Systems (Pearson, 2019), Ch. 3; Ogata, Modern Control Engineering, §5.5.*

---
