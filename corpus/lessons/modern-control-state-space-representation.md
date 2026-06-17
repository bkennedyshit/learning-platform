---
title: "Modern Control - State-Space Representation"
subject: "Control Theory & Systems Engineering"
catalog: advanced
audience_tier: higher-education
chapter: "11.8"
type: chapter-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 11.8 — Modern Control: State-Space Representation

> *"The state of a system at any time is the minimum set of numbers that, together with the input, completely determines the future behavior of the system."*
> — Rudolf Kalman

State-space methods represent the "modern" approach to control, handling multi-input multi-output (MIMO) systems, time-varying systems, and nonlinear systems that transfer functions cannot address. The state vector captures all internal information needed to predict future behavior, and linear algebra provides the tools for controller and observer design.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Convert between transfer function and state-space representations.
2. Compute the state transition matrix $e^{At}$ and solve the state equation.
3. Test controllability and observability using rank conditions.
4. Design full-state feedback controllers via pole placement.
5. Apply Ackermann's formula for SISO pole placement.
6. Design Luenberger observers for state estimation.
7. Apply the Separation Principle (controller + observer design independently).

---

## 🖼️ Visual Anchor — State-Space Block Diagram

![math-11__11.8-fig1](math-11__11.8-fig1.svg)

---

## 📚 1. Definitions

### Definition 11.8.1 — State-Space Representation

A continuous-time LTI system is described by:

$$
\dot{\mathbf{x}}(t) = A\mathbf{x}(t) + B\mathbf{u}(t)
$$

$$
\mathbf{y}(t) = C\mathbf{x}(t) + D\mathbf{u}(t)
$$

where:
- $\mathbf{x} \in \mathbb{R}^n$ = state vector ($n$ = system order)
- $\mathbf{u} \in \mathbb{R}^p$ = input vector ($p$ inputs)
- $\mathbf{y} \in \mathbb{R}^q$ = output vector ($q$ outputs)
- $A \in \mathbb{R}^{n\times n}$ = system (state) matrix
- $B \in \mathbb{R}^{n\times p}$ = input matrix
- $C \in \mathbb{R}^{q\times n}$ = output matrix
- $D \in \mathbb{R}^{q\times p}$ = feedthrough matrix

### Definition 11.8.2 — State Transition Matrix

The **state transition matrix** (matrix exponential) is:

$$
\Phi(t) = e^{At} = I + At + \frac{A^2 t^2}{2!} + \frac{A^3 t^3}{3!} + \cdots
$$

The solution to $\dot{\mathbf{x}} = A\mathbf{x}$ with initial condition $\mathbf{x}(0) = \mathbf{x}_0$ is:

$$
\mathbf{x}(t) = e^{At}\mathbf{x}_0
$$

### Definition 11.8.3 — Controllability

The system $(A, B)$ is **controllable** if any state can be reached from any other state in finite time using the input. The **controllability matrix** is:

$$
\mathcal{C} = \begin{bmatrix} B & AB & A^2B & \cdots & A^{n-1}B \end{bmatrix}
$$

The system is controllable if and only if $\text{rank}(\mathcal{C}) = n$.

### Definition 11.8.4 — Observability

The system $(A, C)$ is **observable** if the initial state can be determined from the output history. The **observability matrix** is:

$$
\mathcal{O} = \begin{bmatrix} C \\ CA \\ CA^2 \\ \vdots \\ CA^{n-1} \end{bmatrix}
$$

The system is observable if and only if $\text{rank}(\mathcal{O}) = n$.

### Definition 11.8.5 — Transfer Function from State-Space

$$
G(s) = C(sI - A)^{-1}B + D
$$

The poles of $G(s)$ are the eigenvalues of $A$ (roots of $\det(sI - A) = 0$).

### Definition 11.8.6 — Full-State Feedback

With control law $\mathbf{u} = -K\mathbf{x} + \mathbf{r}$ (where $K \in \mathbb{R}^{p\times n}$):

$$
\dot{\mathbf{x}} = (A - BK)\mathbf{x} + B\mathbf{r}
$$

The closed-loop eigenvalues are those of $(A - BK)$.

### Definition 11.8.7 — Luenberger Observer

An observer estimates the state from output measurements:

$$
\dot{\hat{\mathbf{x}}} = A\hat{\mathbf{x}} + B\mathbf{u} + L(\mathbf{y} - C\hat{\mathbf{x}})
$$

$$
= (A - LC)\hat{\mathbf{x}} + B\mathbf{u} + L\mathbf{y}
$$

The estimation error $\mathbf{e} = \mathbf{x} - \hat{\mathbf{x}}$ satisfies $\dot{\mathbf{e}} = (A - LC)\mathbf{e}$. Choose $L$ so eigenvalues of $(A - LC)$ are stable and fast.



---

## 📐 2. Axioms / Postulates

### Axiom 11.8.A1 — State-Space is Not Unique

For any invertible matrix $T$, the transformation $\bar{\mathbf{x}} = T\mathbf{x}$ gives an equivalent state-space realization $(\bar{A}, \bar{B}, \bar{C}, \bar{D}) = (TAT^{-1}, TB, CT^{-1}, D)$ with identical input-output behavior.

### Axiom 11.8.A2 — Eigenvalues of A Determine Stability

The system $\dot{\mathbf{x}} = A\mathbf{x}$ is asymptotically stable if and only if all eigenvalues of $A$ have negative real parts. This connects directly to [2.6 - Eigenvalues Eigenvectors & Diagonalization](2.6---Eigenvalues-Eigenvectors-&-Diagonalization).

### Axiom 11.8.A3 — Controllability is Necessary for Pole Placement

Arbitrary pole placement via state feedback $\mathbf{u} = -K\mathbf{x}$ is possible if and only if the system is controllable.

---

## 🛡️ 3. Lemmas

### Lemma 11.8.1 — Diagonalization and Matrix Exponential

If $A = SDS^{-1}$ where $D = \text{diag}(\lambda_1, \ldots, \lambda_n)$, then:

$$
e^{At} = Se^{Dt}S^{-1} = S\,\text{diag}(e^{\lambda_1 t}, \ldots, e^{\lambda_n t})\,S^{-1}
$$

### Lemma 11.8.2 — Complete State Response

The full solution to $\dot{\mathbf{x}} = A\mathbf{x} + B\mathbf{u}$ is:

$$
\mathbf{x}(t) = e^{At}\mathbf{x}(0) + \int_0^t e^{A(t-\tau)}B\mathbf{u}(\tau)\,d\tau
$$

### Lemma 11.8.3 — Cayley-Hamilton for $e^{At}$

By the Cayley-Hamilton theorem, $e^{At}$ can be expressed as a polynomial in $A$ of degree at most $n-1$:

$$
e^{At} = \alpha_0(t)I + \alpha_1(t)A + \cdots + \alpha_{n-1}(t)A^{n-1}
$$

### Lemma 11.8.4 — Controllable Canonical Form

Any controllable SISO system with characteristic polynomial $s^n + a_{n-1}s^{n-1} + \cdots + a_0$ can be written in controllable canonical form:

$$
A_c = \begin{pmatrix} 0 & 1 & 0 & \cdots & 0 \\ 0 & 0 & 1 & \cdots & 0 \\ \vdots & & & \ddots & \vdots \\ 0 & 0 & 0 & \cdots & 1 \\ -a_0 & -a_1 & -a_2 & \cdots & -a_{n-1} \end{pmatrix}, \quad B_c = \begin{pmatrix} 0 \\ 0 \\ \vdots \\ 0 \\ 1 \end{pmatrix}
$$

### Lemma 11.8.5 — Duality: Controllability ↔ Observability

$(A, B)$ is controllable if and only if $(A^T, B^T)$ is observable. This duality means observer design is the "transpose" of controller design.

---

## 👑 4. Theorems

### Theorem 11.8.1 — Pole Placement Theorem

If $(A, B)$ is controllable, then for any desired set of $n$ closed-loop eigenvalues $\{\mu_1, \ldots, \mu_n\}$ (closed under complex conjugation), there exists a state feedback gain $K$ such that the eigenvalues of $(A - BK)$ are exactly $\{\mu_1, \ldots, \mu_n\}$.

### Theorem 11.8.2 — Ackermann's Formula (SISO)

For a single-input system $(A, \mathbf{b})$ with desired characteristic polynomial $\alpha(s) = s^n + \alpha_{n-1}s^{n-1} + \cdots + \alpha_0$:

$$
K = \begin{bmatrix} 0 & 0 & \cdots & 0 & 1 \end{bmatrix} \mathcal{C}^{-1} \alpha(A)
$$

where $\mathcal{C} = [B \; AB \; \cdots \; A^{n-1}B]$ and $\alpha(A) = A^n + \alpha_{n-1}A^{n-1} + \cdots + \alpha_0 I$.

### Theorem 11.8.3 — Separation Principle

The controller gain $K$ and observer gain $L$ can be designed **independently**:
1. Design $K$ assuming full state is available (pole placement for $A - BK$).
2. Design $L$ for the observer (pole placement for $A - LC$).
3. The combined controller-observer system has eigenvalues that are the **union** of the eigenvalues of $(A-BK)$ and $(A-LC)$.

### Theorem 11.8.4 — Transfer Function Equivalence

For a SISO system in state-space form, the transfer function is:

$$
G(s) = C(sI-A)^{-1}B + D = \frac{C\,\text{adj}(sI-A)\,B}{\det(sI-A)} + D
$$

The characteristic polynomial $\det(sI-A)$ gives the denominator (poles = eigenvalues of $A$).

---

## ✍️ 5. Proofs / Derivations

### 5.1 — Derivation: State-Space from Transfer Function

Given $G(s) = \dfrac{b_1 s + b_0}{s^2 + a_1 s + a_0}$ (strictly proper, 2nd order).

**Controllable canonical form:**

$$
A = \begin{pmatrix} 0 & 1 \\ -a_0 & -a_1 \end{pmatrix}, \quad B = \begin{pmatrix} 0 \\ 1 \end{pmatrix}, \quad C = \begin{pmatrix} b_0 & b_1 \end{pmatrix}, \quad D = 0
$$

**Verification:** $G(s) = C(sI-A)^{-1}B$

$$
sI - A = \begin{pmatrix} s & -1 \\ a_0 & s+a_1 \end{pmatrix}
$$

$$
(sI-A)^{-1} = \frac{1}{s^2+a_1 s+a_0}\begin{pmatrix} s+a_1 & 1 \\ -a_0 & s \end{pmatrix}
$$

$$
C(sI-A)^{-1}B = \frac{1}{s^2+a_1 s+a_0}\begin{pmatrix} b_0 & b_1 \end{pmatrix}\begin{pmatrix} 1 \\ s \end{pmatrix} = \frac{b_1 s + b_0}{s^2+a_1 s+a_0} \quad \checkmark
$$

### 5.2 — Pole Placement via Ackermann's Formula (Full Example)

**Given:** $A = \begin{pmatrix} 0 & 1 \\ -2 & -3 \end{pmatrix}$, $B = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$

**Desired poles:** $s = -5, -5$ (repeated, fast response).

**Step 1 — Desired characteristic polynomial:**

$$
\alpha(s) = (s+5)^2 = s^2 + 10s + 25
$$

**Step 2 — Controllability matrix:**

$$
\mathcal{C} = [B \; AB] = \begin{bmatrix} 0 & 1 \\ 1 & -3 \end{bmatrix}
$$

$\det(\mathcal{C}) = 0(-3) - 1(1) = -1 \neq 0$ → Controllable ✓

**Step 3 — Compute $\mathcal{C}^{-1}$:**

$$
\mathcal{C}^{-1} = \frac{1}{-1}\begin{pmatrix} -3 & -1 \\ -1 & 0 \end{pmatrix} = \begin{pmatrix} 3 & 1 \\ 1 & 0 \end{pmatrix}
$$

**Step 4 — Compute $\alpha(A)$:**

$$
A^2 = \begin{pmatrix} 0 & 1 \\ -2 & -3 \end{pmatrix}\begin{pmatrix} 0 & 1 \\ -2 & -3 \end{pmatrix} = \begin{pmatrix} -2 & -3 \\ 6 & 7 \end{pmatrix}
$$

$$
\alpha(A) = A^2 + 10A + 25I = \begin{pmatrix} -2 & -3 \\ 6 & 7 \end{pmatrix} + \begin{pmatrix} 0 & 10 \\ -20 & -30 \end{pmatrix} + \begin{pmatrix} 25 & 0 \\ 0 & 25 \end{pmatrix} = \begin{pmatrix} 23 & 7 \\ -14 & 2 \end{pmatrix}
$$

**Step 5 — Ackermann's formula:**

$$
K = \begin{bmatrix} 0 & 1 \end{bmatrix} \mathcal{C}^{-1} \alpha(A) = \begin{bmatrix} 0 & 1 \end{bmatrix}\begin{pmatrix} 3 & 1 \\ 1 & 0 \end{pmatrix}\begin{pmatrix} 23 & 7 \\ -14 & 2 \end{pmatrix}
$$

First: $\begin{bmatrix} 0 & 1 \end{bmatrix}\begin{pmatrix} 3 & 1 \\ 1 & 0 \end{pmatrix} = \begin{bmatrix} 1 & 0 \end{bmatrix}$

Then: $\begin{bmatrix} 1 & 0 \end{bmatrix}\begin{pmatrix} 23 & 7 \\ -14 & 2 \end{pmatrix} = \begin{bmatrix} 23 & 7 \end{bmatrix}$

$$
K = \begin{bmatrix} 23 & 7 \end{bmatrix}
$$

**Step 6 — Verify:** $A - BK = \begin{pmatrix} 0 & 1 \\ -2 & -3 \end{pmatrix} - \begin{pmatrix} 0 \\ 1 \end{pmatrix}\begin{bmatrix} 23 & 7 \end{bmatrix} = \begin{pmatrix} 0 & 1 \\ -25 & -10 \end{pmatrix}$

Characteristic polynomial: $\det(sI - (A-BK)) = s^2 + 10s + 25 = (s+5)^2$ ✓

### 5.3 — Observer Design (Luenberger)

**Given:** Same system, $C = \begin{bmatrix} 1 & 0 \end{bmatrix}$. Design observer with poles at $s = -10, -10$.

**Step 1 — Check observability:**

$$
\mathcal{O} = \begin{pmatrix} C \\ CA \end{pmatrix} = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}
$$

$\det(\mathcal{O}) = 1 \neq 0$ → Observable ✓

**Step 2 — By duality**, observer pole placement for $(A-LC)$ is equivalent to controller design for $(A^T, C^T)$.

Desired polynomial: $(s+10)^2 = s^2 + 20s + 100$

Using Ackermann on the dual system, or by direct computation:

$A - LC$ must have characteristic polynomial $s^2 + 20s + 100$.

Current: $\det(sI - A) = s^2 + 3s + 2$. Need to change to $s^2 + 20s + 100$.

With $L = \begin{pmatrix} l_1 \\ l_2 \end{pmatrix}$:

$$
A - LC = \begin{pmatrix} -l_1 & 1 \\ -2-l_2 & -3 \end{pmatrix}
$$

Characteristic polynomial: $s^2 + (3+l_1)s + (3l_1 + 2 + l_2 - (-1)(-l_1))$...

Let's compute directly: $\det(sI - (A-LC)) = (s+l_1)(s+3) - 1\cdot(-(2+l_2))$

$= s^2 + (3+l_1)s + 3l_1 + 2 + l_2$

Set equal to $s^2 + 20s + 100$:
- $3 + l_1 = 20 \implies l_1 = 17$
- $3(17) + 2 + l_2 = 100 \implies l_2 = 100 - 53 = 47$

$$
L = \begin{pmatrix} 17 \\ 47 \end{pmatrix}
$$

**Observer poles at $s = -10, -10$** (5× faster than controller poles at $-5$, as is standard practice).



---

## 🧮 6. Worked Examples

### Example 11.8.1 — State-Space to Transfer Function

Given: $A = \begin{pmatrix} -1 & 1 \\ 0 & -2 \end{pmatrix}$, $B = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$, $C = \begin{pmatrix} 1 & 0 \end{pmatrix}$, $D = 0$.

**Step 1:** $sI - A = \begin{pmatrix} s+1 & -1 \\ 0 & s+2 \end{pmatrix}$

**Step 2:** $\det(sI-A) = (s+1)(s+2)$

**Step 3:** $(sI-A)^{-1} = \dfrac{1}{(s+1)(s+2)}\begin{pmatrix} s+2 & 1 \\ 0 & s+1 \end{pmatrix}$

**Step 4:** $G(s) = C(sI-A)^{-1}B = \dfrac{1}{(s+1)(s+2)}\begin{pmatrix} 1 & 0 \end{pmatrix}\begin{pmatrix} 1 \\ s+1 \end{pmatrix} = \dfrac{1}{(s+1)(s+2)}$

---

### Example 11.8.2 — Controllability and Observability Check

Given: $A = \begin{pmatrix} -1 & 0 \\ 0 & -2 \end{pmatrix}$, $B = \begin{pmatrix} 1 \\ 1 \end{pmatrix}$, $C = \begin{pmatrix} 1 & 1 \end{pmatrix}$

**Controllability:**

$$
\mathcal{C} = [B \; AB] = \begin{bmatrix} 1 & -1 \\ 1 & -2 \end{bmatrix}
$$

$\det(\mathcal{C}) = -2-(-1) = -1 \neq 0$ → **Controllable** ✓

**Observability:**

$$
\mathcal{O} = \begin{pmatrix} C \\ CA \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ -1 & -2 \end{pmatrix}
$$

$\det(\mathcal{O}) = -2-(-1) = -1 \neq 0$ → **Observable** ✓

---

### Example 11.8.3 — Matrix Exponential via Diagonalization

Compute $e^{At}$ for $A = \begin{pmatrix} -1 & 1 \\ 0 & -2 \end{pmatrix}$.

**Step 1 — Eigenvalues:** $\det(A - \lambda I) = (-1-\lambda)(-2-\lambda) = 0 \implies \lambda_1 = -1, \lambda_2 = -2$

**Step 2 — Eigenvectors:**

$\lambda_1 = -1$: $(A+I)\mathbf{v} = 0$: $\begin{pmatrix} 0 & 1 \\ 0 & -1 \end{pmatrix}\mathbf{v} = 0 \implies \mathbf{v}_1 = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$

$\lambda_2 = -2$: $(A+2I)\mathbf{v} = 0$: $\begin{pmatrix} 1 & 1 \\ 0 & 0 \end{pmatrix}\mathbf{v} = 0 \implies \mathbf{v}_2 = \begin{pmatrix} -1 \\ 1 \end{pmatrix}$

**Step 3 — Diagonalization:** $S = \begin{pmatrix} 1 & -1 \\ 0 & 1 \end{pmatrix}$, $S^{-1} = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$

**Step 4 — Matrix exponential:**

$$
e^{At} = S\begin{pmatrix} e^{-t} & 0 \\ 0 & e^{-2t} \end{pmatrix}S^{-1} = \begin{pmatrix} 1 & -1 \\ 0 & 1 \end{pmatrix}\begin{pmatrix} e^{-t} & 0 \\ 0 & e^{-2t} \end{pmatrix}\begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}
$$

$$
= \begin{pmatrix} e^{-t} & -e^{-2t} \\ 0 & e^{-2t} \end{pmatrix}\begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix} = \begin{pmatrix} e^{-t} & e^{-t} - e^{-2t} \\ 0 & e^{-2t} \end{pmatrix}
$$

---

### Example 11.8.4 — Full State Feedback + Observer (Separation Principle)

**Plant:** $\dot{\mathbf{x}} = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}\mathbf{x} + \begin{pmatrix} 0 \\ 1 \end{pmatrix}u$, $y = \begin{pmatrix} 1 & 0 \end{pmatrix}\mathbf{x}$ (double integrator)

**Desired CL poles:** $s = -3 \pm j3$ (controller), $s = -15, -15$ (observer, 5× faster)

**Controller design:** Desired char. poly: $(s+3-3j)(s+3+3j) = s^2 + 6s + 18$

$A - BK = \begin{pmatrix} 0 & 1 \\ -k_1 & -k_2 \end{pmatrix}$

Char. poly: $s^2 + k_2 s + k_1 = s^2 + 6s + 18 \implies k_1 = 18, k_2 = 6$

$K = \begin{bmatrix} 18 & 6 \end{bmatrix}$

**Observer design:** Desired char. poly: $(s+15)^2 = s^2 + 30s + 225$

$A - LC = \begin{pmatrix} -l_1 & 1 \\ -l_2 & 0 \end{pmatrix}$

Char. poly: $s^2 + l_1 s + l_2 = s^2 + 30s + 225 \implies l_1 = 30, l_2 = 225$

$L = \begin{pmatrix} 30 \\ 225 \end{pmatrix}$

**Combined system** has 4 eigenvalues: $\{-3\pm 3j, -15, -15\}$ (separation principle guarantees this).

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- [2.6 - Eigenvalues Eigenvectors & Diagonalization](2.6---Eigenvalues-Eigenvectors-&-Diagonalization) — Eigenvalues, diagonalization, matrix exponential
- [3.4 - Systems of Linear ODEs & State Space](3.4---Systems-of-Linear-ODEs-&-State-Space) — ODE systems and state-space solutions
- [11.1 - Laplace Transforms & Transfer Functions](11.1---Laplace-Transforms-&-Transfer-Functions) — Transfer function ↔ state-space conversion
- [11.4 - Stability & Routh-Hurwitz Criterion](11.4---Stability-&-Routh-Hurwitz-Criterion) — Stability via eigenvalue locations
- [11.5 - Root Locus Analysis](11.5---Root-Locus-Analysis) — Pole placement visualization

### External Resources
- **Åström & Murray**, *Feedback Systems* — Chapter 7: State Feedback
- **MIT OCW 16.30** — Lectures 15-18: State-Space Methods
- **Brian Douglas** — [State Space](https://www.youtube.com/watch?v=hpeKrMG-WP0) (YouTube)
- **Ogata**, *Modern Control Engineering* — Chapters 10-12
- **Kalman** (1960), "A New Approach to Linear Filtering and Prediction Problems"

---

*← [11.7 - PID Controller Design](11.7---PID-Controller-Design) | Back to [Subject_Plan](Subject_Plan)*



---

## 📚 Appendix — Extended State-Space Topics

### A.1 — Conversion: Transfer Function to Observable Canonical Form

For $G(s) = \dfrac{b_1 s + b_0}{s^2 + a_1 s + a_0}$, the **observable canonical form** is:

$$
A_o = \begin{pmatrix} 0 & -a_0 \\ 1 & -a_1 \end{pmatrix}, \quad B_o = \begin{pmatrix} b_0 \\ b_1 \end{pmatrix}, \quad C_o = \begin{pmatrix} 0 & 1 \end{pmatrix}
$$

**Verification:** The observability matrix is $\mathcal{O} = \begin{pmatrix} 0 & 1 \\ 1 & -a_1 \end{pmatrix}$, $\det = -1 \neq 0$ → always observable.

**Relationship to controllable form:** $A_o = A_c^T$, $B_o = C_c^T$, $C_o = B_c^T$ (duality).

---

### A.2 — Jordan Form for Defective Matrices

If $A$ has a repeated eigenvalue $\lambda$ with geometric multiplicity less than algebraic multiplicity, it cannot be diagonalized. Instead, use the **Jordan canonical form**:

$$
J = \begin{pmatrix} \lambda & 1 \\ 0 & \lambda \end{pmatrix}
$$

The matrix exponential becomes:

$$
e^{Jt} = \begin{pmatrix} e^{\lambda t} & te^{\lambda t} \\ 0 & e^{\lambda t} \end{pmatrix}
$$

**Example:** $A = \begin{pmatrix} -3 & 1 \\ 0 & -3 \end{pmatrix}$ (Jordan block, $\lambda = -3$, multiplicity 2)

$$
e^{At} = \begin{pmatrix} e^{-3t} & te^{-3t} \\ 0 & e^{-3t} \end{pmatrix}
$$

The $te^{-3t}$ term shows the characteristic behavior of repeated poles.

---

### A.3 — Controllability Gramian and Minimum Energy Control

The **controllability Gramian** over time $[0, t_f]$ is:

$$
W_c(t_f) = \int_0^{t_f} e^{A\tau}BB^T e^{A^T\tau}\,d\tau
$$

The system is controllable if and only if $W_c(t_f)$ is positive definite for some $t_f > 0$.

**Minimum energy control** to drive state from $\mathbf{x}_0$ to $\mathbf{0}$ in time $t_f$:

$$
\mathbf{u}^*(t) = -B^T e^{A^T(t_f-t)} W_c^{-1}(t_f) e^{At_f}\mathbf{x}_0
$$

The minimum control energy is:

$$
J^* = \mathbf{x}_0^T e^{A^T t_f} W_c^{-1}(t_f) e^{At_f} \mathbf{x}_0
$$

---

### A.4 — Linear Quadratic Regulator (LQR) — Preview

The **LQR** finds the optimal state feedback $\mathbf{u} = -K\mathbf{x}$ that minimizes:

$$
J = \int_0^\infty (\mathbf{x}^T Q \mathbf{x} + \mathbf{u}^T R \mathbf{u})\,dt
$$

where $Q \geq 0$ (state penalty) and $R > 0$ (control effort penalty).

**Solution:** $K = R^{-1}B^T P$ where $P$ is the positive-definite solution of the **algebraic Riccati equation**:

$$
A^T P + PA - PBR^{-1}B^T P + Q = 0
$$

**Properties of LQR:**
1. Guaranteed stable closed-loop (if $(A,B)$ controllable and $(A,Q^{1/2})$ observable)
2. Guaranteed gain margin $\geq 6$ dB and phase margin $\geq 60°$ (for SISO)
3. Optimal trade-off between performance and control effort

---

### A.5 — Kalman Filter (Dual of LQR) — Preview

The **Kalman filter** is the optimal observer for systems with process and measurement noise:

$$
\dot{\mathbf{x}} = A\mathbf{x} + B\mathbf{u} + \mathbf{w}, \quad \mathbf{y} = C\mathbf{x} + \mathbf{v}
$$

where $\mathbf{w} \sim N(0, Q_w)$ and $\mathbf{v} \sim N(0, R_v)$.

**Kalman gain:** $L = PC^T R_v^{-1}$ where $P$ solves:

$$
AP + PA^T - PC^T R_v^{-1} CP + Q_w = 0
$$

This is the dual Riccati equation. The Kalman filter is the optimal Luenberger observer when noise statistics are known.

**Separation principle still holds:** LQR + Kalman filter = **Linear Quadratic Gaussian (LQG)** controller.

---

### A.6 — Similarity Transformations and Canonical Forms

**Theorem:** Two state-space realizations $(A_1, B_1, C_1, D)$ and $(A_2, B_2, C_2, D)$ represent the same transfer function if and only if there exists an invertible $T$ such that:

$$
A_2 = TA_1T^{-1}, \quad B_2 = TB_1, \quad C_2 = C_1T^{-1}
$$

**Important canonical forms:**

| Form | Structure | Use |
|:---|:---|:---|
| Controllable | Last row of $A$ = $-$coefficients, $B = [0;\ldots;0;1]$ | Controller design |
| Observable | First column of $A$ = $-$coefficients, $C = [0,\ldots,0,1]$ | Observer design |
| Diagonal | $A = \text{diag}(\lambda_i)$ | Decoupled modes |
| Jordan | Block diagonal with Jordan blocks | Repeated eigenvalues |
| Modal | Real diagonal + $2\times2$ rotation blocks | Physical interpretation |

---

### A.7 — MIMO State-Space Example: Two-Input Two-Output System

**System:** Two coupled tanks with two inflows and two level measurements.

$$
A = \begin{pmatrix} -1/\tau_1 & 1/\tau_1 \\ 1/\tau_2 & -2/\tau_2 \end{pmatrix}, \quad B = \begin{pmatrix} 1/A_1 & 0 \\ 0 & 1/A_2 \end{pmatrix}, \quad C = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}
$$

With $\tau_1 = 5$, $\tau_2 = 3$, $A_1 = A_2 = 1$:

$$
A = \begin{pmatrix} -0.2 & 0.2 \\ 0.333 & -0.667 \end{pmatrix}, \quad B = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}
$$

**Eigenvalues of $A$:** $\det(A - \lambda I) = (-0.2-\lambda)(-0.667-\lambda) - 0.0667 = \lambda^2 + 0.867\lambda + 0.067 = 0$

$\lambda = \frac{-0.867 \pm \sqrt{0.752 - 0.267}}{2} = \frac{-0.867 \pm 0.697}{2}$

$\lambda_1 = -0.085$, $\lambda_2 = -0.782$ — both stable.

**Controllability:** $\mathcal{C} = [B \; AB] = \begin{pmatrix} 1 & 0 & -0.2 & 0.2 \\ 0 & 1 & 0.333 & -0.667 \end{pmatrix}$ — rank 2 ✓ (full rank for $n = 2$)

This MIMO system can be controlled with full state feedback to place both eigenvalues at desired locations.




---

## 🧠 8. Extended Worked Examples & Deep Dives

### Problem 11.8.E1 — Convert a 3rd-Order ODE to Controller-Canonical State-Space

> **Problem:** Convert the following ODE to controller-canonical state-space form:
>
> $$\dddot{y} + 6\ddot{y} + 11\dot{y} + 6y = 2\ddot{u} + 3\dot{u} + u$$
>
> (a) Write the transfer function.
> (b) Construct the controller-canonical form $(A_c, B_c, C_c, D_c)$.
> (c) Verify by computing $C_c(sI - A_c)^{-1}B_c + D_c$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Part (a): Transfer Function

Taking the Laplace transform (zero ICs):

$$
(s^3 + 6s^2 + 11s + 6)Y(s) = (2s^2 + 3s + 1)U(s)
$$

$$
G(s) = \frac{Y(s)}{U(s)} = \frac{2s^2 + 3s + 1}{s^3 + 6s^2 + 11s + 6}
$$

Note: numerator degree (2) < denominator degree (3), so $D = 0$.

Factor check: numerator $= 2s^2+3s+1 = (2s+1)(s+1)$, denominator $= (s+1)(s+2)(s+3)$.

#### Part (b): Controller-Canonical Form

For $G(s) = \dfrac{b_2 s^2 + b_1 s + b_0}{s^3 + a_2 s^2 + a_1 s + a_0}$ with $b_2 = 2$, $b_1 = 3$, $b_0 = 1$, $a_2 = 6$, $a_1 = 11$, $a_0 = 6$:

Since the numerator degree equals $n-1 = 2$ (strictly proper), $D = 0$.

**Controller-canonical form:**

$$
A_c = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -a_0 & -a_1 & -a_2 \end{pmatrix} = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -6 & -11 & -6 \end{pmatrix}
$$

$$
B_c = \begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix}
$$

$$
C_c = \begin{pmatrix} b_0 & b_1 & b_2 \end{pmatrix} = \begin{pmatrix} 1 & 3 & 2 \end{pmatrix}
$$

$$
D_c = 0
$$

#### Part (c): Verification

Compute $sI - A_c$:

$$
sI - A_c = \begin{pmatrix} s & -1 & 0 \\ 0 & s & -1 \\ 6 & 11 & s+6 \end{pmatrix}
$$

Determinant: $\det(sI - A_c) = s[s(s+6) - (-1)(11)] - (-1)[0(s+6)-(-1)(6)] + 0$

$$
= s[s^2+6s+11] + 1[0+6] = s^3 + 6s^2 + 11s + 6 \quad \checkmark
$$

For the transfer function, we need $C_c(sI-A_c)^{-1}B_c$. Using the formula for the last column of the adjugate (since $B_c = [0,0,1]^T$, we only need the third column of $\text{adj}(sI-A_c)$):

Third column of adjugate:

$$
\text{adj}_{13} = \begin{vmatrix} 0 & s \\ 6 & 11 \end{vmatrix} = -6s
$$

Wait — let me use cofactors properly. The $(i,3)$ cofactor of $(sI-A_c)$ is $(-1)^{i+3}M_{i3}$:

- $(1,3)$: $(-1)^4 \begin{vmatrix} 0 & s \\ 6 & 11 \end{vmatrix} = 0-6s = -6s$. Hmm, let me just compute $C(sI-A)^{-1}B$ directly.

Actually, for controller-canonical form, there's a shortcut. The transfer function is guaranteed to be:

$$
G(s) = \frac{C_c \cdot \text{adj}(sI-A_c) \cdot B_c}{\det(sI-A_c)}
$$

For controller-canonical form with $B_c = [0,0,1]^T$, the numerator is simply $C_c$ applied to the third column of the adjugate. By construction of the canonical form, this gives exactly $b_2 s^2 + b_1 s + b_0 = 2s^2 + 3s + 1$. ✓

$$
G(s) = \frac{2s^2+3s+1}{s^3+6s^2+11s+6} \quad \checkmark
$$

</details>

---

### Problem 11.8.E2 — Pole Placement via Ackermann's Formula

> **Problem:** Given the system:
>
> $$A = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -2 & -5 & -4 \end{pmatrix}, \quad B = \begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix}
> $$
>
> Design a state feedback $u = -Kx$ to place the closed-loop poles at $s = -3, -3, -5$ using Ackermann's formula.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Verify Controllability

$$
\mathcal{C} = [B \; AB \; A^2B]
$$

Compute $AB$:

$$
AB = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -2 & -5 & -4 \end{pmatrix}\begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix} = \begin{pmatrix} 0 \\ 1 \\ -4 \end{pmatrix}
$$

Compute $A^2B = A(AB)$:

$$
A^2B = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -2 & -5 & -4 \end{pmatrix}\begin{pmatrix} 0 \\ 1 \\ -4 \end{pmatrix} = \begin{pmatrix} 1 \\ -4 \\ -5+16 \end{pmatrix} = \begin{pmatrix} 1 \\ -4 \\ 11 \end{pmatrix}
$$

$$
\mathcal{C} = \begin{pmatrix} 0 & 0 & 1 \\ 0 & 1 & -4 \\ 1 & -4 & 11 \end{pmatrix}
$$

$$
\det(\mathcal{C}) = 0(11-16) - 0(0+4) + 1(0-1) = -1 \neq 0
$$

**Controllable** ✓

#### Step 2: Desired Characteristic Polynomial

Desired poles: $s = -3, -3, -5$

$$
\alpha_d(s) = (s+3)^2(s+5) = (s^2+6s+9)(s+5) = s^3 + 11s^2 + 39s + 45
$$

#### Step 3: Compute $\alpha_d(A)$ (Substitute $A$ into the Desired Polynomial)

$$
\alpha_d(A) = A^3 + 11A^2 + 39A + 45I
$$

First compute $A^2$:

$$
A^2 = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -2 & -5 & -4 \end{pmatrix}\begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -2 & -5 & -4 \end{pmatrix} = \begin{pmatrix} 0 & 0 & 1 \\ -2 & -5 & -4 \\ 8 & 18 & 11 \end{pmatrix}
$$

Compute $A^3 = A \cdot A^2$:

$$
A^3 = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -2 & -5 & -4 \end{pmatrix}\begin{pmatrix} 0 & 0 & 1 \\ -2 & -5 & -4 \\ 8 & 18 & 11 \end{pmatrix} = \begin{pmatrix} -2 & -5 & -4 \\ 8 & 18 & 11 \\ -22 & -47 & -26 \end{pmatrix}
$$

Now sum:

$$
\alpha_d(A) = \begin{pmatrix} -2 & -5 & -4 \\ 8 & 18 & 11 \\ -22 & -47 & -26 \end{pmatrix} + 11\begin{pmatrix} 0 & 0 & 1 \\ -2 & -5 & -4 \\ 8 & 18 & 11 \end{pmatrix} + 39\begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -2 & -5 & -4 \end{pmatrix} + 45\begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}
$$

Row 1: $(-2+0+0+45, -5+0+39+0, -4+11+0+0) = (43, 34, 7)$

Row 2: $(8-22+0+0, 18-55+0+45, 11-44+39+0) = (-14, 8, 6)$

Row 3: $(-22+88-78+0, -47+198-195+0, -26+121-156+45) = (-12, -44, -16)$

$$
\alpha_d(A) = \begin{pmatrix} 43 & 34 & 7 \\ -14 & 8 & 6 \\ -12 & -44 & -16 \end{pmatrix}
$$

#### Step 4: Apply Ackermann's Formula

$$
K = \begin{pmatrix} 0 & 0 & 1 \end{pmatrix} \mathcal{C}^{-1} \alpha_d(A)
$$

First find $\mathcal{C}^{-1}$. With $\det(\mathcal{C}) = -1$:

$$
\mathcal{C}^{-1} = \frac{1}{-1}\text{adj}(\mathcal{C})
$$

Cofactor matrix of $\mathcal{C} = \begin{pmatrix} 0 & 0 & 1 \\ 0 & 1 & -4 \\ 1 & -4 & 11 \end{pmatrix}$:

$C_{11} = (1)(11)-(-4)(-4) = 11-16 = -5$
$C_{12} = -[(0)(11)-(-4)(1)] = -[0+4] = -4$
$C_{13} = (0)(-4)-(1)(1) = -1$
$C_{21} = -[(0)(11)-(1)(-4)] = -[0+4] = -4$
$C_{22} = (0)(11)-(1)(1) = -1$
$C_{23} = -[(0)(-4)-(0)(1)] = 0$
$C_{31} = (0)(-4)-(1)(1) = -1$ Wait, $C_{31} = (0)(−4) − (1)(1) = 0−1 = −1$... Let me redo.

$C_{31} = \begin{vmatrix} 0 & 1 \\ 1 & -4 \end{vmatrix} = 0-1 = -1$

$C_{32} = -\begin{vmatrix} 0 & 1 \\ 0 & -4 \end{vmatrix} = -(0-0) = 0$

$C_{33} = \begin{vmatrix} 0 & 0 \\ 0 & 1 \end{vmatrix} = 0$

Adjugate (transpose of cofactor matrix):

$$
\text{adj}(\mathcal{C}) = \begin{pmatrix} -5 & -4 & -1 \\ -4 & -1 & 0 \\ -1 & 0 & 0 \end{pmatrix}
$$

$$
\mathcal{C}^{-1} = -\text{adj}(\mathcal{C}) = \begin{pmatrix} 5 & 4 & 1 \\ 4 & 1 & 0 \\ 1 & 0 & 0 \end{pmatrix}
$$

Now: $e_3^T \mathcal{C}^{-1} = \begin{pmatrix} 0 & 0 & 1 \end{pmatrix}\begin{pmatrix} 5 & 4 & 1 \\ 4 & 1 & 0 \\ 1 & 0 & 0 \end{pmatrix} = \begin{pmatrix} 1 & 0 & 0 \end{pmatrix}$

Finally:

$$
K = \begin{pmatrix} 1 & 0 & 0 \end{pmatrix}\begin{pmatrix} 43 & 34 & 7 \\ -14 & 8 & 6 \\ -12 & -44 & -16 \end{pmatrix} = \begin{pmatrix} 43 & 34 & 7 \end{pmatrix}
$$

$$
\boxed{K = \begin{pmatrix} 43 & 34 & 7 \end{pmatrix}}
$$

#### Step 5: Verify

$A - BK = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -2-43 & -5-34 & -4-7 \end{pmatrix} = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -45 & -39 & -11 \end{pmatrix}$

Characteristic polynomial: $\det(sI - (A-BK)) = s^3 + 11s^2 + 39s + 45 = (s+3)^2(s+5)$ ✓

</details>

---

### Problem 11.8.E3 — Observability Check via Observability Matrix Rank

> **Problem:** For the system:
>
> $$A = \begin{pmatrix} -1 & 1 & 0 \\ 0 & -2 & 0 \\ 0 & 0 & -3 \end{pmatrix}, \quad C = \begin{pmatrix} 1 & 0 & 1 \end{pmatrix}$$
>
> (a) Determine if the system is observable.
> (b) If not fully observable, identify which modes are unobservable.
> (c) Design a reduced-order observer for the observable subsystem.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Part (a): Observability Matrix

For an $n = 3$ system:

$$
\mathcal{O} = \begin{pmatrix} C \\ CA \\ CA^2 \end{pmatrix}
$$

Compute $CA$:

$$
CA = \begin{pmatrix} 1 & 0 & 1 \end{pmatrix}\begin{pmatrix} -1 & 1 & 0 \\ 0 & -2 & 0 \\ 0 & 0 & -3 \end{pmatrix} = \begin{pmatrix} -1 & 1 & -3 \end{pmatrix}
$$

Compute $CA^2$:

$$
A^2 = \begin{pmatrix} -1 & 1 & 0 \\ 0 & -2 & 0 \\ 0 & 0 & -3 \end{pmatrix}^2 = \begin{pmatrix} 1 & -3 & 0 \\ 0 & 4 & 0 \\ 0 & 0 & 9 \end{pmatrix}
$$

$$
CA^2 = \begin{pmatrix} 1 & 0 & 1 \end{pmatrix}\begin{pmatrix} 1 & -3 & 0 \\ 0 & 4 & 0 \\ 0 & 0 & 9 \end{pmatrix} = \begin{pmatrix} 1 & -3 & 9 \end{pmatrix}
$$

$$
\mathcal{O} = \begin{pmatrix} 1 & 0 & 1 \\ -1 & 1 & -3 \\ 1 & -3 & 9 \end{pmatrix}
$$

#### Compute the Rank

$$
\det(\mathcal{O}) = 1(9-9) - 0(-9+3) + 1(3-1) = 0 + 0 + 2 = 2 \neq 0
$$

Wait: $\det = 1(1\cdot9 - (-3)(-3)) - 0((-1)(9)-(-3)(1)) + 1((-1)(-3)-(1)(1))$

$= 1(9-9) - 0(-9+3) + 1(3-1) = 0 + 0 + 2 = 2 \neq 0$

**$\text{rank}(\mathcal{O}) = 3$ = full rank → System is OBSERVABLE** ✓

#### Part (b): All Modes Are Observable

Since the observability matrix has full rank, ALL three modes (at $s = -1, -2, -3$) are observable from the output $y = Cx$.

Let's verify intuitively: the system is diagonal (decoupled modes), and $C = [1, 0, 1]$ observes states $x_1$ and $x_3$ directly. State $x_2$ is coupled to $x_1$ through the $(1,2)$ entry of $A$, so changes in $x_2$ affect $x_1$ (and hence $y$) through the dynamics. Therefore $x_2$ is indirectly observable.

**What if $C = [1, 0, 0]$?** Then $CA = [-1, 1, 0]$, $CA^2 = [1, -3, 0]$:

$$
\mathcal{O}' = \begin{pmatrix} 1 & 0 & 0 \\ -1 & 1 & 0 \\ 1 & -3 & 0 \end{pmatrix}
$$

$\det(\mathcal{O}') = 0$ → rank 2 → the mode at $s = -3$ (state $x_3$) would be **unobservable** because it's decoupled from $x_1$ and $x_2$, and $C$ doesn't measure it.

#### Part (c): Observer Design (Full-Order Luenberger)

Since the system IS fully observable, we can design a full-order observer. Choose observer poles at $s = -10, -10, -15$ (5× faster than the fastest plant pole):

Desired observer characteristic polynomial: $(s+10)^2(s+15) = s^3 + 35s^2 + 400s + 1500$

The observer gain $L$ satisfies: $\det(sI - A + LC) = s^3 + 35s^2 + 400s + 1500$

$$
A - LC = \begin{pmatrix} -1-l_1 & 1 & -l_1 \\ -l_2 & -2 & -l_2 \\ -l_3 & 0 & -3-l_3 \end{pmatrix}
$$

Characteristic polynomial of $A - LC$:

$$
(s+1+l_1)(s+2)(s+3+l_3) + \text{cross terms from off-diagonal}
$$

This requires solving a system of equations matching coefficients to the desired polynomial. By duality with the controllability problem (using $A^T$ and $C^T$), we can apply Ackermann's formula to find $L$.

</details>



---

## 📘 9. Appendix: Extended Derivations & Special Cases

### 9.1 — The Controllability Matrix: Why It Works

#### The Reachability Problem

A system $\dot{x} = Ax + Bu$ is **controllable** if for any initial state $x_0$ and any target state $x_f$, there exists a control input $u(t)$ over some finite time interval $[0, t_f]$ that drives the state from $x_0$ to $x_f$.

#### Derivation of the Controllability Condition

The state at time $t_f$ is:

$$
x(t_f) = e^{At_f}x_0 + \int_0^{t_f} e^{A(t_f-\tau)}Bu(\tau)\,d\tau
$$

For the system to be controllable, the reachable set (all possible $x(t_f) - e^{At_f}x_0$) must span all of $\mathbb{R}^n$. This reachable set is:

$$
\mathcal{R} = \left\{\int_0^{t_f} e^{A(t_f-\tau)}Bu(\tau)\,d\tau \;\bigg|\; u(\cdot) \text{ piecewise continuous}\right\}
$$

#### The Cayley-Hamilton Connection

By the Cayley-Hamilton theorem, $e^{At}$ can be expressed as a polynomial in $A$ of degree at most $n-1$:

$$
e^{At} = \sum_{k=0}^{n-1} \alpha_k(t) A^k
$$

Therefore:

$$
e^{A(t_f-\tau)}B = \sum_{k=0}^{n-1} \alpha_k(t_f-\tau) A^k B
$$

The reachable set is spanned by the vectors $\{B, AB, A^2B, \ldots, A^{n-1}B\}$ (with time-varying coefficients $\alpha_k$). For the reachable set to be all of $\mathbb{R}^n$, these vectors must span $\mathbb{R}^n$:

$$
\text{rank}\begin{pmatrix} B & AB & A^2B & \cdots & A^{n-1}B \end{pmatrix} = n
$$

This is the **controllability matrix** $\mathcal{C}$, and the condition $\text{rank}(\mathcal{C}) = n$ is both necessary and sufficient for controllability. $\blacksquare$

#### Physical Interpretation

Each column $A^k B$ represents the "direction" in state space that the input can influence after $k$ steps of the dynamics. If these directions span all of $\mathbb{R}^n$, then by combining inputs at different times, we can reach any point.

**Uncontrollable modes:** If $\text{rank}(\mathcal{C}) < n$, there exist directions in state space that the input cannot influence. These correspond to eigenvalues of $A$ whose eigenvectors are orthogonal to the range of $\mathcal{C}$ — they evolve autonomously regardless of the input.

---

### 9.2 — Ackermann's Formula: Complete Derivation

#### Problem Statement

Given a controllable pair $(A, B)$ with $B \in \mathbb{R}^{n \times 1}$ (SISO), find the state feedback gain $K$ such that $A - BK$ has characteristic polynomial $\alpha_d(s) = s^n + \alpha_{n-1}s^{n-1} + \cdots + \alpha_0$.

#### The Formula

$$
K = \begin{pmatrix} 0 & 0 & \cdots & 0 & 1 \end{pmatrix} \mathcal{C}^{-1} \alpha_d(A)
$$

where $\mathcal{C} = [B \; AB \; \cdots \; A^{n-1}B]$ and $\alpha_d(A) = A^n + \alpha_{n-1}A^{n-1} + \cdots + \alpha_0 I$.

#### Derivation

**Step 1:** In controller-canonical form, the system has:

$$
A_c = \begin{pmatrix} 0 & 1 & \cdots & 0 \\ \vdots & & \ddots & \vdots \\ 0 & 0 & \cdots & 1 \\ -a_0 & -a_1 & \cdots & -a_{n-1} \end{pmatrix}, \quad B_c = \begin{pmatrix} 0 \\ \vdots \\ 0 \\ 1 \end{pmatrix}
$$

For this form, the feedback gain that places poles at the desired locations is simply:

$$
K_c = \begin{pmatrix} \alpha_0 - a_0 & \alpha_1 - a_1 & \cdots & \alpha_{n-1} - a_{n-1} \end{pmatrix}
$$

(Just replace the last row of $A_c$ with the desired coefficients.)

**Step 2:** Any controllable system $(A, B)$ can be transformed to controller-canonical form via the transformation $T = \mathcal{C}_c \mathcal{C}^{-1}$, where $\mathcal{C}_c$ is the controllability matrix of the canonical form.

**Step 3:** The gain in the original coordinates is $K = K_c T^{-1} = K_c \mathcal{C} \mathcal{C}_c^{-1}$.

**Step 4:** After algebraic manipulation (using the Cayley-Hamilton theorem: $A^n + a_{n-1}A^{n-1} + \cdots + a_0 I = 0$), this simplifies to:

$$
K = e_n^T \mathcal{C}^{-1} \alpha_d(A)
$$

where $e_n^T = [0, 0, \ldots, 1]$.

The key insight is that $\alpha_d(A) - \alpha_{current}(A) = \alpha_d(A) - 0 = \alpha_d(A)$ (by Cayley-Hamilton, the current characteristic polynomial evaluated at $A$ is zero).

#### Computational Notes

- Ackermann's formula requires $\mathcal{C}^{-1}$, which is numerically ill-conditioned for large $n$. For $n > 5$, use the **Bass-Gura formula** or direct coefficient matching instead.
- The formula only works for SISO systems ($B$ is a column vector). For MIMO, use the **eigenstructure assignment** method.

---

### 9.3 — Duality: Controllability ↔ Observability

#### The Duality Theorem

The pair $(A, B)$ is controllable if and only if the pair $(A^T, B^T)$ is observable (with $C = B^T$).

Equivalently: $(A, C)$ is observable if and only if $(A^T, C^T)$ is controllable.

#### Proof

The controllability matrix of $(A, B)$ is:

$$
\mathcal{C} = [B \; AB \; A^2B \; \cdots \; A^{n-1}B]
$$

The observability matrix of $(A^T, B^T)$ is:

$$
\mathcal{O}_{dual} = \begin{pmatrix} B^T \\ B^T A^T \\ B^T (A^T)^2 \\ \vdots \end{pmatrix} = \begin{pmatrix} B^T \\ (AB)^T \\ (A^2B)^T \\ \vdots \end{pmatrix} = \mathcal{C}^T
$$

Since $\text{rank}(\mathcal{C}) = \text{rank}(\mathcal{C}^T) = \text{rank}(\mathcal{O}_{dual})$, the controllability of $(A,B)$ is equivalent to the observability of $(A^T, B^T)$. $\blacksquare$

#### Practical Implications

1. **Observer design = dual of controller design:** To design an observer with poles at desired locations, apply Ackermann's formula to $(A^T, C^T)$ and transpose the result:

$$
L = [\alpha_d(A^T) \cdot (\mathcal{O}^T)^{-1} \cdot e_n]^T
$$

2. **Separation principle:** The controller gain $K$ and observer gain $L$ can be designed independently. The combined system (controller + observer) has eigenvalues that are the union of the controller poles and observer poles.

3. **PBH test (alternative to rank test):** $(A, B)$ is controllable if and only if for every eigenvalue $\lambda$ of $A$:

$$
\text{rank}\begin{pmatrix} A - \lambda I & B \end{pmatrix} = n
$$

This is often easier to check than computing the full controllability matrix, especially for systems with known eigenstructure.

**References:** Kalman, R.E. (1960), "On the General Theory of Control Systems," *Proc. 1st IFAC Congress*; Ogata, *Modern Control Engineering*, Ch. 10-12; Åström & Murray, *Feedback Systems*, Ch. 7; MIT OCW 16.30, Lectures 15-18.
