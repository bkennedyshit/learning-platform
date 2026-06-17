---
title: "Systems Of Linear Odes State Space"
subject: "Ordinary & Partial Differential Equations"
catalog: advanced
audience_tier: higher-education
chapter: "3.4"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 3.4 — Systems of Linear ODEs & State Space

> *"A single higher-order equation is merely a system in disguise — the matrix exponential reveals the geometry that scalar methods conceal."* — Vladimir Arnold

Any $n$-th order linear ODE can be rewritten as a first-order system $\mathbf{x}' = A\mathbf{x}$. This reformulation unlocks the full power of linear algebra: eigenvalues become growth/decay rates, eigenvectors become invariant directions, and the matrix exponential $e^{At}$ provides the complete solution. Phase portraits — the geometric fingerprints of 2D systems — classify all qualitative behaviors: nodes, saddles, spirals, and centers.

---

## 🎯 Learning Objectives

1. Convert an $n$-th order ODE to a first-order system $\mathbf{x}' = A\mathbf{x}$.
2. Solve $\mathbf{x}' = A\mathbf{x}$ using eigenvalues and eigenvectors of $A$.
3. Compute the matrix exponential $e^{At}$ via diagonalization.
4. Classify 2D phase portraits: stable/unstable nodes, saddle points, spirals, centers.
5. Handle defective matrices using generalized eigenvectors (Jordan chains).
6. Solve nonhomogeneous systems $\mathbf{x}' = A\mathbf{x} + \mathbf{g}(t)$ via variation of parameters.

---

## 🖼️ Visual Anchor — Phase Portrait Classification

![math-03__3.4-fig1](math-03__3.4-fig1.svg)

---


## 📚 1. Definitions

### Definition 3.4.1 — First-Order Linear System

A **first-order linear system** of ODEs is:

$$
\mathbf{x}'(t) = A(t)\,\mathbf{x}(t) + \mathbf{g}(t), \quad \mathbf{x} \in \mathbb{R}^n,
$$

where $A(t)$ is an $n\times n$ matrix. When $A$ is constant and $\mathbf{g} = \mathbf{0}$, this is the **autonomous homogeneous** system $\mathbf{x}' = A\mathbf{x}$.

### Definition 3.4.2 — State Vector and Phase Space

The vector $\mathbf{x}(t) = (x_1(t), \ldots, x_n(t))^T$ is the **state vector**. The space $\mathbb{R}^n$ in which $\mathbf{x}$ lives is the **phase space** (or state space). A trajectory $\mathbf{x}(t)$ traces a curve in phase space.

### Definition 3.4.3 — Matrix Exponential

The **matrix exponential** of $A \in M_{n\times n}(\mathbb{R})$ is:

$$
e^{At} = \sum_{k=0}^{\infty} \frac{(At)^k}{k!} = I + At + \frac{A^2 t^2}{2!} + \frac{A^3 t^3}{3!} + \cdots
$$

This series converges for all $t$ and all $A$. The solution to $\mathbf{x}' = A\mathbf{x}$, $\mathbf{x}(0) = \mathbf{x}_0$ is $\mathbf{x}(t) = e^{At}\mathbf{x}_0$.

### Definition 3.4.4 — Fundamental Matrix

A **fundamental matrix** $\Phi(t)$ for $\mathbf{x}' = A\mathbf{x}$ is an $n\times n$ matrix whose columns form a fundamental set of solutions. If $\Phi(0) = I$, then $\Phi(t) = e^{At}$.

### Definition 3.4.5 — Equilibrium Classification (2D)

For $\mathbf{x}' = A\mathbf{x}$ in $\mathbb{R}^2$ with eigenvalues $\lambda_1, \lambda_2$:
- **Stable node:** $\lambda_1, \lambda_2 < 0$ real.
- **Unstable node:** $\lambda_1, \lambda_2 > 0$ real.
- **Saddle:** $\lambda_1 < 0 < \lambda_2$ real.
- **Stable spiral:** $\lambda = \alpha \pm i\beta$ with $\alpha < 0$.
- **Unstable spiral:** $\alpha > 0$.
- **Center:** $\lambda = \pm i\beta$ (purely imaginary).

---

## 📐 2. Axioms / Postulates

**Postulate 3.4.P1:** The matrix exponential satisfies $\frac{d}{dt}e^{At} = Ae^{At}$ and $e^{A\cdot 0} = I$.

**Postulate 3.4.P2:** If $A$ is diagonalizable as $A = SDS^{-1}$, then $e^{At} = Se^{Dt}S^{-1}$ where $e^{Dt} = \text{diag}(e^{\lambda_1 t}, \ldots, e^{\lambda_n t})$.

---

## 🛡️ 3. Lemmas

### Lemma 3.4.1 — Conversion of $n$-th Order ODE to System

The $n$-th order ODE $y^{(n)} + a_{n-1}y^{(n-1)} + \cdots + a_1 y' + a_0 y = 0$ is equivalent to $\mathbf{x}' = A\mathbf{x}$ with:

$$
\mathbf{x} = \begin{pmatrix}y\\y'\\y''\\\vdots\\y^{(n-1)}\end{pmatrix}, \quad A = \begin{pmatrix}0&1&0&\cdots&0\\0&0&1&\cdots&0\\\vdots&&&\ddots&\vdots\\0&0&0&\cdots&1\\-a_0&-a_1&-a_2&\cdots&-a_{n-1}\end{pmatrix}.
$$

The characteristic polynomial of $A$ equals the characteristic equation of the original ODE.

**Proof.** Define $x_1 = y$, $x_2 = y'$, ..., $x_n = y^{(n-1)}$. Then $x_k' = x_{k+1}$ for $k < n$, and $x_n' = y^{(n)} = -a_0 x_1 - a_1 x_2 - \cdots - a_{n-1}x_n$. This gives the companion matrix $A$. Its characteristic polynomial is $\det(A - \lambda I) = (-1)^n(\lambda^n + a_{n-1}\lambda^{n-1} + \cdots + a_0)$. $\blacksquare$

### Lemma 3.4.2 — Solution via Eigenvectors

If $A$ has eigenvalue $\lambda$ with eigenvector $\mathbf{v}$, then $\mathbf{x}(t) = e^{\lambda t}\mathbf{v}$ is a solution of $\mathbf{x}' = A\mathbf{x}$.

**Proof.** $\mathbf{x}' = \lambda e^{\lambda t}\mathbf{v}$ and $A\mathbf{x} = e^{\lambda t}A\mathbf{v} = e^{\lambda t}\lambda\mathbf{v} = \lambda e^{\lambda t}\mathbf{v}$. $\blacksquare$

---

## 👑 4. Theorems

### Theorem 3.4.1 — General Solution via Eigendecomposition

If $A \in M_{n\times n}(\mathbb{R})$ has $n$ linearly independent eigenvectors $\mathbf{v}_1, \ldots, \mathbf{v}_n$ with eigenvalues $\lambda_1, \ldots, \lambda_n$, then the general solution of $\mathbf{x}' = A\mathbf{x}$ is:

$$
\mathbf{x}(t) = c_1 e^{\lambda_1 t}\mathbf{v}_1 + c_2 e^{\lambda_2 t}\mathbf{v}_2 + \cdots + c_n e^{\lambda_n t}\mathbf{v}_n.
$$

### Theorem 3.4.2 — Matrix Exponential via Diagonalization

If $A = SDS^{-1}$ with $D = \text{diag}(\lambda_1, \ldots, \lambda_n)$, then:

$$
e^{At} = S\,\text{diag}(e^{\lambda_1 t}, \ldots, e^{\lambda_n t})\,S^{-1}.
$$

### Theorem 3.4.3 — Stability Criterion

The equilibrium $\mathbf{x} = \mathbf{0}$ of $\mathbf{x}' = A\mathbf{x}$ is:
- **Asymptotically stable** iff all eigenvalues of $A$ have negative real part: $\text{Re}(\lambda_i) < 0$ for all $i$.
- **Unstable** if any eigenvalue has positive real part.
- **Marginally stable** (Lyapunov stable) if all eigenvalues have $\text{Re}(\lambda_i) \leq 0$ with those on the imaginary axis being simple.

---

## ✍️ 5. Proofs / Derivations

### 5.1 Proof of Theorem 3.4.2

**Step 1.** Since $A = SDS^{-1}$, compute $A^k = SD^kS^{-1}$ (by [Theorem 2.6.5](2.6---Eigenvalues-Eigenvectors-&-Diagonalization)).

**Step 2.** Substitute into the series definition:

$$
e^{At} = \sum_{k=0}^{\infty}\frac{(At)^k}{k!} = \sum_{k=0}^{\infty}\frac{S(Dt)^kS^{-1}}{k!} = S\left(\sum_{k=0}^{\infty}\frac{(Dt)^k}{k!}\right)S^{-1}.
$$

**Step 3.** Since $D$ is diagonal, $(Dt)^k = \text{diag}((\lambda_1 t)^k, \ldots, (\lambda_n t)^k)$, so:

$$
\sum_{k=0}^{\infty}\frac{(Dt)^k}{k!} = \text{diag}\left(\sum_{k=0}^{\infty}\frac{(\lambda_1 t)^k}{k!}, \ldots\right) = \text{diag}(e^{\lambda_1 t}, \ldots, e^{\lambda_n t}). \quad \blacksquare
$$

---

## 🧮 6. Worked Examples

### Example 3.4.E1 — 2×2 System with Distinct Real Eigenvalues

**Solve:** $\mathbf{x}' = \begin{pmatrix}1&2\\3&2\end{pmatrix}\mathbf{x}$.

**Step 1.** Eigenvalues: $\det(A-\lambda I) = (1-\lambda)(2-\lambda)-6 = \lambda^2 - 3\lambda - 4 = (\lambda-4)(\lambda+1) = 0$.

So $\lambda_1 = 4$, $\lambda_2 = -1$.

**Step 2.** Eigenvector for $\lambda_1 = 4$: $(A-4I)\mathbf{v} = 0$:

$$
\begin{pmatrix}-3&2\\3&-2\end{pmatrix}\mathbf{v} = 0 \implies \mathbf{v}_1 = \begin{pmatrix}2\\3\end{pmatrix}.
$$

**Step 3.** Eigenvector for $\lambda_2 = -1$: $(A+I)\mathbf{v} = 0$:

$$
\begin{pmatrix}2&2\\3&3\end{pmatrix}\mathbf{v} = 0 \implies \mathbf{v}_2 = \begin{pmatrix}1\\-1\end{pmatrix}.
$$

**Step 4.** General solution:

$$
\mathbf{x}(t) = c_1 e^{4t}\begin{pmatrix}2\\3\end{pmatrix} + c_2 e^{-t}\begin{pmatrix}1\\-1\end{pmatrix}.
$$

**Phase portrait:** Saddle point (one positive, one negative eigenvalue).

---

### Example 3.4.E2 — Complex Eigenvalues (Spiral)

**Solve:** $\mathbf{x}' = \begin{pmatrix}-1&-2\\2&-1\end{pmatrix}\mathbf{x}$.

**Step 1.** $\det(A-\lambda I) = (-1-\lambda)^2 + 4 = \lambda^2 + 2\lambda + 5 = 0$.

$\lambda = -1 \pm 2i$.

**Step 2.** Eigenvector for $\lambda = -1+2i$: $(A-(-1+2i)I)\mathbf{v} = 0$:

$$
\begin{pmatrix}-2i&-2\\2&-2i\end{pmatrix}\mathbf{v} = 0 \implies v_1 = i v_2.
$$

Choose $\mathbf{v} = \begin{pmatrix}i\\1\end{pmatrix} = \begin{pmatrix}0\\1\end{pmatrix} + i\begin{pmatrix}1\\0\end{pmatrix}$.

**Step 3.** Real solution from $e^{(-1+2i)t}\mathbf{v}$:

$$
\mathbf{x}(t) = e^{-t}\left[c_1\begin{pmatrix}\cos 2t\\\sin 2t - \cos 2t\end{pmatrix} + c_2\begin{pmatrix}\sin 2t\\\cos 2t + \sin 2t\end{pmatrix}\right].
$$

Wait — let us be more careful. Write $\mathbf{v} = \mathbf{a} + i\mathbf{b}$ where $\mathbf{a} = (0,1)^T$, $\mathbf{b} = (1,0)^T$.

The two real solutions are:

$$
\mathbf{x}_1 = e^{-t}(\mathbf{a}\cos 2t - \mathbf{b}\sin 2t) = e^{-t}\begin{pmatrix}-\sin 2t\\\cos 2t\end{pmatrix},
$$

$$
\mathbf{x}_2 = e^{-t}(\mathbf{a}\sin 2t + \mathbf{b}\cos 2t) = e^{-t}\begin{pmatrix}\cos 2t\\\sin 2t\end{pmatrix}.
$$

**General solution:** $\mathbf{x}(t) = c_1 e^{-t}\begin{pmatrix}-\sin 2t\\\cos 2t\end{pmatrix} + c_2 e^{-t}\begin{pmatrix}\cos 2t\\\sin 2t\end{pmatrix}$.

**Phase portrait:** Stable spiral (trajectories spiral inward since $\alpha = -1 < 0$).

---

### Example 3.4.E3 — Converting a 2nd-Order ODE to a System

Convert $y'' + 3y' + 2y = 0$ to a system and solve.

**Step 1.** Let $x_1 = y$, $x_2 = y'$. Then:

$$
\begin{pmatrix}x_1'\\x_2'\end{pmatrix} = \begin{pmatrix}0&1\\-2&-3\end{pmatrix}\begin{pmatrix}x_1\\x_2\end{pmatrix}.
$$

**Step 2.** Eigenvalues of $A$: $\lambda^2 + 3\lambda + 2 = (\lambda+1)(\lambda+2) = 0$, so $\lambda_1 = -1$, $\lambda_2 = -2$.

**Step 3.** This matches the scalar solution $y = c_1 e^{-x} + c_2 e^{-2x}$ from [3.2 - Second-Order Linear Homogeneous ODEs](3.2---Second-Order-Linear-Homogeneous-ODEs).

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- [2.6 - Eigenvalues Eigenvectors & Diagonalization](2.6---Eigenvalues-Eigenvectors-&-Diagonalization) — eigendecomposition is the core tool
- [3.2 - Second-Order Linear Homogeneous ODEs](3.2---Second-Order-Linear-Homogeneous-ODEs) — scalar equations as special case
- [3.3 - Nonhomogeneous ODEs & Undetermined Coefficients](3.3---Nonhomogeneous-ODEs-&-Undetermined-Coefficients) — forced systems
- [3.7 - The Heat & Wave PDEs - Separation of Variables](3.7---The-Heat-&-Wave-PDEs---Separation-of-Variables) — infinite-dimensional analogue

### External References
- **MIT OCW 18.03SC**, Unit III: Systems of ODEs
- **Gilbert Strang**, *Differential Equations and Linear Algebra* (Wellesley-Cambridge, 2014)
- **Steven Strogatz**, *Nonlinear Dynamics and Chaos*, Ch. 5 (phase portrait classification)
- **3Blue1Brown**, "Matrix exponents" (visual intuition for $e^{At}$)

---



---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — Predator-Prey Linearization (Lotka–Volterra Near Equilibrium)

The Lotka–Volterra system is $x' = x(3 - y)$, $y' = y(x - 2)$. Linearize about the coexistence equilibrium $(x^*, y^*) = (2, 3)$ and classify the phase portrait.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Find equilibria

Set $x' = 0$: $x(3-y) = 0 \implies x = 0$ or $y = 3$.

Set $y' = 0$: $y(x-2) = 0 \implies y = 0$ or $x = 2$.

Equilibria: $(0, 0)$ and $(2, 3)$.

#### Step 2: Compute the Jacobian matrix

Let $f(x,y) = x(3-y)$ and $g(x,y) = y(x-2)$.

$$
J = \begin{pmatrix} f_x & f_y \\ g_x & g_y \end{pmatrix} = \begin{pmatrix} 3-y & -x \\ y & x-2 \end{pmatrix}.
$$

#### Step 3: Evaluate at $(2, 3)$

$$
J\big|_{(2,3)} = \begin{pmatrix} 0 & -2 \\ 3 & 0 \end{pmatrix}.
$$

#### Step 4: Find eigenvalues

$$
\det(J - \lambda I) = \lambda^2 - (0+0)\lambda + (0 \cdot 0 - (-2)(3)) = \lambda^2 + 6 = 0.
$$

$$
\lambda = \pm i\sqrt{6}.
$$

#### Step 5: Classify the equilibrium

Pure imaginary eigenvalues $\implies$ the linearization predicts a **center** (closed orbits). The populations oscillate periodically around $(2, 3)$ with angular frequency $\omega = \sqrt{6} \approx 2.45$ rad/time.

#### Step 6: Write the linearized solution

Let $u = x - 2$, $v = y - 3$. The linearized system is:

$$
\begin{pmatrix} u' \\ v' \end{pmatrix} = \begin{pmatrix} 0 & -2 \\ 3 & 0 \end{pmatrix}\begin{pmatrix} u \\ v \end{pmatrix}.
$$

General solution:

$$
\begin{pmatrix} u \\ v \end{pmatrix} = C_1\begin{pmatrix} 2 \\ -\sqrt{6} \end{pmatrix}\cos(\sqrt{6}\,t) + C_2\begin{pmatrix} 2 \\ \sqrt{6} \end{pmatrix}\sin(\sqrt{6}\,t) \cdot \frac{1}{\sqrt{6}}.
$$

**Final Answer:**

$$
\lambda = \pm i\sqrt{6}, \quad \text{center (neutrally stable periodic orbits)}.
$$

**Note:** For the full nonlinear system, the Lotka–Volterra equations are Hamiltonian with conserved quantity $H = x - 2\ln x + y - 3\ln y$, confirming the orbits are truly closed (not just an artifact of linearization).

</details>

### Example 8.2 — Defective Matrix: Generalized Eigenvectors (Repeated Eigenvalue)

Solve the system $\mathbf{x}' = A\mathbf{x}$ where:

$$
A = \begin{pmatrix} 3 & 1 \\ 0 & 3 \end{pmatrix}, \quad \mathbf{x}(0) = \begin{pmatrix} 1 \\ 4 \end{pmatrix}.
$$

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Find eigenvalues

$$
\det(A - \lambda I) = (3-\lambda)^2 = 0 \implies \lambda = 3 \text{ (multiplicity 2)}.
$$

#### Step 2: Find eigenvectors

$(A - 3I)\mathbf{v} = \mathbf{0}$:

$$
\begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}\mathbf{v} = \mathbf{0} \implies v_2 = 0, \quad v_1 \text{ free}.
$$

Only one independent eigenvector: $\mathbf{v}_1 = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$. The matrix is **defective**.

#### Step 3: Find a generalized eigenvector

Solve $(A - 3I)\mathbf{w} = \mathbf{v}_1$:

$$
\begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}\begin{pmatrix} w_1 \\ w_2 \end{pmatrix} = \begin{pmatrix} 1 \\ 0 \end{pmatrix} \implies w_2 = 1, \quad w_1 \text{ free}.
$$

Choose $\mathbf{w} = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$.

#### Step 4: Write the general solution

$$
\mathbf{x}(t) = c_1 e^{3t}\begin{pmatrix} 1 \\ 0 \end{pmatrix} + c_2 e^{3t}\left[t\begin{pmatrix} 1 \\ 0 \end{pmatrix} + \begin{pmatrix} 0 \\ 1 \end{pmatrix}\right].
$$

$$
\mathbf{x}(t) = e^{3t}\begin{pmatrix} c_1 + c_2 t \\ c_2 \end{pmatrix}.
$$

#### Step 5: Apply initial condition

$$
\mathbf{x}(0) = \begin{pmatrix} c_1 \\ c_2 \end{pmatrix} = \begin{pmatrix} 1 \\ 4 \end{pmatrix}.
$$

**Final Answer:**

$$
\mathbf{x}(t) = e^{3t}\begin{pmatrix} 1 + 4t \\ 4 \end{pmatrix}.
$$

The phase portrait is a **degenerate (improper) node** — all trajectories approach the origin tangent to the eigenvector direction as $t \to -\infty$.

</details>

### Example 8.3 — Coupled Mass-Spring System (Two Masses, Three Springs)

Two unit masses are connected by springs: $k_1 = 1$ (wall to mass 1), $k_2 = 2$ (mass 1 to mass 2), $k_3 = 1$ (mass 2 to wall). No damping. Find the normal modes.

The equations of motion are:

$$
x_1'' = -(k_1 + k_2)x_1 + k_2 x_2 = -3x_1 + 2x_2
$$

$$
x_2'' = k_2 x_1 - (k_2 + k_3)x_2 = 2x_1 - 3x_2
$$

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Write as a matrix equation

$$
\mathbf{x}'' = -K\mathbf{x}, \quad K = \begin{pmatrix} 3 & -2 \\ -2 & 3 \end{pmatrix}.
$$

#### Step 2: Find eigenvalues of $K$

$$
\det(K - \omega^2 I) = (3-\omega^2)^2 - 4 = 0 \implies 3 - \omega^2 = \pm 2.
$$

$$
\omega_1^2 = 1, \quad \omega_2^2 = 5.
$$

So the natural frequencies are $\omega_1 = 1$ and $\omega_2 = \sqrt{5}$ rad/s.

#### Step 3: Find eigenvectors (normal modes)

For $\omega_1^2 = 1$: $(K - I)\mathbf{v} = \mathbf{0}$:

$$
\begin{pmatrix} 2 & -2 \\ -2 & 2 \end{pmatrix}\mathbf{v} = \mathbf{0} \implies \mathbf{v}_1 = \begin{pmatrix} 1 \\ 1 \end{pmatrix}.
$$

For $\omega_2^2 = 5$: $(K - 5I)\mathbf{v} = \mathbf{0}$:

$$
\begin{pmatrix} -2 & -2 \\ -2 & -2 \end{pmatrix}\mathbf{v} = \mathbf{0} \implies \mathbf{v}_2 = \begin{pmatrix} 1 \\ -1 \end{pmatrix}.
$$

#### Step 4: Interpret physically

**Mode 1** ($\omega_1 = 1$): Both masses move in phase $(1, 1)$ — the middle spring is unstretched. Only the outer springs contribute stiffness.

**Mode 2** ($\omega_2 = \sqrt{5}$): Masses move in antiphase $(1, -1)$ — the middle spring is maximally stretched. All springs contribute, giving higher frequency.

#### Step 5: General solution

**Final Answer:**

$$
\begin{pmatrix} x_1(t) \\ x_2(t) \end{pmatrix} = (A_1\cos t + B_1\sin t)\begin{pmatrix} 1 \\ 1 \end{pmatrix} + (A_2\cos\sqrt{5}\,t + B_2\sin\sqrt{5}\,t)\begin{pmatrix} 1 \\ -1 \end{pmatrix}.
$$

</details>

### Example 8.4 — Matrix Exponential via Diagonalization

Compute $e^{At}$ for $A = \begin{pmatrix} 1 & 2 \\ 0 & 3 \end{pmatrix}$ and solve $\mathbf{x}' = A\mathbf{x}$, $\mathbf{x}(0) = \begin{pmatrix} 5 \\ 1 \end{pmatrix}$.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Eigenvalues

$\det(A - \lambda I) = (1-\lambda)(3-\lambda) = 0 \implies \lambda_1 = 1, \lambda_2 = 3$.

#### Step 2: Eigenvectors

$\lambda_1 = 1$: $(A - I)\mathbf{v} = \begin{pmatrix} 0 & 2 \\ 0 & 2 \end{pmatrix}\mathbf{v} = \mathbf{0} \implies \mathbf{v}_1 = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$.

$\lambda_2 = 3$: $(A - 3I)\mathbf{v} = \begin{pmatrix} -2 & 2 \\ 0 & 0 \end{pmatrix}\mathbf{v} = \mathbf{0} \implies \mathbf{v}_2 = \begin{pmatrix} 1 \\ 1 \end{pmatrix}$.

#### Step 3: Diagonalize $A = PDP^{-1}$

$$
P = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}, \quad D = \begin{pmatrix} 1 & 0 \\ 0 & 3 \end{pmatrix}, \quad P^{-1} = \begin{pmatrix} 1 & -1 \\ 0 & 1 \end{pmatrix}.
$$

#### Step 4: Compute $e^{At} = Pe^{Dt}P^{-1}$

$$
e^{At} = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}\begin{pmatrix} e^t & 0 \\ 0 & e^{3t} \end{pmatrix}\begin{pmatrix} 1 & -1 \\ 0 & 1 \end{pmatrix}.
$$

Multiply the last two matrices first:

$$
\begin{pmatrix} e^t & 0 \\ 0 & e^{3t} \end{pmatrix}\begin{pmatrix} 1 & -1 \\ 0 & 1 \end{pmatrix} = \begin{pmatrix} e^t & -e^t \\ 0 & e^{3t} \end{pmatrix}.
$$

Then:

$$
e^{At} = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}\begin{pmatrix} e^t & -e^t \\ 0 & e^{3t} \end{pmatrix} = \begin{pmatrix} e^t & e^{3t} - e^t \\ 0 & e^{3t} \end{pmatrix}.
$$

#### Step 5: Solution

$$
\mathbf{x}(t) = e^{At}\mathbf{x}(0) = \begin{pmatrix} e^t & e^{3t} - e^t \\ 0 & e^{3t} \end{pmatrix}\begin{pmatrix} 5 \\ 1 \end{pmatrix} = \begin{pmatrix} 5e^t + e^{3t} - e^t \\ e^{3t} \end{pmatrix} = \begin{pmatrix} 4e^t + e^{3t} \\ e^{3t} \end{pmatrix}.
$$

**Final Answer:**

$$
\mathbf{x}(t) = \begin{pmatrix} 4e^t + e^{3t} \\ e^{3t} \end{pmatrix}.
$$

</details>



---

## 📘 9. Appendix: Extended Derivations & Special Cases

### 9.1 The Matrix Exponential — Definition, Properties, and Computation Methods

The matrix exponential $e^{At}$ is the fundamental object for solving $\mathbf{x}' = A\mathbf{x}$. We derive it from first principles and catalog computation methods.

**Definition.** For any $n \times n$ matrix $A$:

$$
e^{At} = \sum_{k=0}^{\infty} \frac{(At)^k}{k!} = I + At + \frac{A^2 t^2}{2!} + \frac{A^3 t^3}{3!} + \cdots
$$

This series converges absolutely for all $t$ and all $A$ (by comparison with $e^{\|A\|t}$).

**Key properties:**
1. $e^{A \cdot 0} = I$ (identity at $t = 0$).
2. $\frac{d}{dt}e^{At} = Ae^{At} = e^{At}A$ (differentiating term by term).
3. $e^{(A+B)t} = e^{At}e^{Bt}$ **only if** $AB = BA$ (matrices commute). In general, the Baker–Campbell–Hausdorff formula applies.
4. $(e^{At})^{-1} = e^{-At}$ (always invertible).
5. $\det(e^{At}) = e^{\text{tr}(A)t}$ (Jacobi's formula).

**Computation methods:**

**Method 1: Diagonalization.** If $A = PDP^{-1}$ with $D = \text{diag}(\lambda_1, \ldots, \lambda_n)$:

$$
e^{At} = Pe^{Dt}P^{-1} = P\,\text{diag}(e^{\lambda_1 t}, \ldots, e^{\lambda_n t})\,P^{-1}.
$$

**Method 2: Jordan form.** If $A = PJP^{-1}$ where $J$ is a Jordan block $J = \lambda I + N$ ($N$ nilpotent):

$$
e^{Jt} = e^{\lambda t}\sum_{k=0}^{m-1}\frac{(Nt)^k}{k!} = e^{\lambda t}\begin{pmatrix} 1 & t & t^2/2 & \cdots \\ 0 & 1 & t & \cdots \\ \vdots & & \ddots & \\ 0 & 0 & \cdots & 1 \end{pmatrix}.
$$

**Method 3: Cayley–Hamilton.** By Cayley–Hamilton, $A$ satisfies its own characteristic polynomial of degree $n$, so $e^{At}$ can be written as a polynomial in $A$ of degree at most $n-1$:

$$
e^{At} = \alpha_0(t)I + \alpha_1(t)A + \cdots + \alpha_{n-1}(t)A^{n-1}.
$$

The coefficients $\alpha_k(t)$ are determined by requiring $e^{\lambda_i t} = \alpha_0 + \alpha_1\lambda_i + \cdots + \alpha_{n-1}\lambda_i^{n-1}$ for each eigenvalue $\lambda_i$ (with derivative conditions for repeated eigenvalues).

**Method 4: Laplace transform.** $e^{At} = \mathcal{L}^{-1}\{(sI - A)^{-1}\}$. This connects directly to the resolvent matrix and transfer function theory in control systems.

*Reference: Strang, Differential Equations and Linear Algebra, Ch. 6; MIT OCW 18.06, Lecture 23.*

### 9.2 Stability Classification via Eigenvalues — The Complete Taxonomy

For the autonomous system $\mathbf{x}' = A\mathbf{x}$ with $A \in \mathbb{R}^{2\times 2}$, the equilibrium at the origin is classified entirely by the eigenvalues $\lambda_1, \lambda_2$. Let $\tau = \text{tr}(A) = \lambda_1 + \lambda_2$ and $\Delta = \det(A) = \lambda_1 \lambda_2$.

| Condition | Eigenvalues | Phase Portrait | Stability |
|---|---|---|---|
| $\Delta < 0$ | Real, opposite sign | **Saddle point** | Unstable |
| $\Delta > 0$, $\tau^2 > 4\Delta$, $\tau < 0$ | Real, both negative | **Stable node** | Asymptotically stable |
| $\Delta > 0$, $\tau^2 > 4\Delta$, $\tau > 0$ | Real, both positive | **Unstable node** | Unstable |
| $\Delta > 0$, $\tau^2 < 4\Delta$, $\tau < 0$ | Complex, negative real part | **Stable spiral** | Asymptotically stable |
| $\Delta > 0$, $\tau^2 < 4\Delta$, $\tau > 0$ | Complex, positive real part | **Unstable spiral** | Unstable |
| $\Delta > 0$, $\tau = 0$ | Pure imaginary | **Center** | Stable (not asymptotically) |
| $\Delta > 0$, $\tau^2 = 4\Delta$, $\tau < 0$ | Repeated negative | **Degenerate/star node** | Asymptotically stable |
| $\Delta = 0$ | At least one zero eigenvalue | **Non-isolated equilibria** | Unstable (line of fixed points) |

**The trace-determinant plane.** The parabola $\tau^2 = 4\Delta$ separates nodes from spirals. The $\tau$-axis ($\Delta = 0$) separates saddles from nodes/spirals. The $\Delta$-axis ($\tau = 0$) separates stable from unstable. This gives a complete "map" of all possible 2D linear phase portraits.

**Structural stability.** Centers ($\tau = 0$, $\Delta > 0$) are structurally unstable — any perturbation of $A$ that makes $\tau \neq 0$ converts the center into a spiral. This is why linearization at a center does not determine the nonlinear behavior (the Lotka–Volterra system is a special case where a conserved quantity guarantees the center persists).

*Reference: Steven Strogatz, Nonlinear Dynamics and Chaos (Westview, 2015), §5.2; Hirsch, Smale & Devaney, Differential Equations, Dynamical Systems, and an Introduction to Chaos, Ch. 3.*

### 9.3 The Cayley–Hamilton Theorem and Minimal Polynomial in ODE Solutions

The Cayley–Hamilton theorem states that every square matrix satisfies its own characteristic polynomial: if $p(\lambda) = \det(A - \lambda I) = \lambda^n + c_{n-1}\lambda^{n-1} + \cdots + c_0$, then $p(A) = A^n + c_{n-1}A^{n-1} + \cdots + c_0 I = 0$.

**Application to $e^{At}$.** Since $A^n$ can be expressed as a linear combination of $I, A, \ldots, A^{n-1}$, and similarly for all higher powers, the infinite series $e^{At} = \sum (At)^k/k!$ collapses to a polynomial of degree at most $n-1$ in $A$ (with time-dependent coefficients).

**For a $2 \times 2$ matrix:** $e^{At} = \alpha_0(t)I + \alpha_1(t)A$, where:

- If eigenvalues are distinct ($\lambda_1 \neq \lambda_2$): $\alpha_0 = \frac{\lambda_1 e^{\lambda_2 t} - \lambda_2 e^{\lambda_1 t}}{\lambda_1 - \lambda_2}$, $\alpha_1 = \frac{e^{\lambda_1 t} - e^{\lambda_2 t}}{\lambda_1 - \lambda_2}$.
- If eigenvalue is repeated ($\lambda_1 = \lambda_2 = \lambda$): $\alpha_0 = (1 - \lambda t)e^{\lambda t}$, $\alpha_1 = te^{\lambda t}$.

This provides a direct formula for $e^{At}$ without computing eigenvectors or Jordan forms — particularly useful for $2 \times 2$ systems in exams.

**The minimal polynomial** $m(\lambda)$ divides the characteristic polynomial and is the lowest-degree monic polynomial satisfying $m(A) = 0$. Its roots are the same as those of $p(\lambda)$, but with possibly lower multiplicities. The minimal polynomial determines the Jordan structure: if $m(\lambda) = (\lambda - \lambda_i)^{k_i}$, then the largest Jordan block for $\lambda_i$ has size $k_i$.

*Reference: Strang, Linear Algebra and Its Applications, §6.4; MIT OCW 18.06, Lecture 22.*

---



### 9.4 Nonlinear Systems: Linearization and the Hartman–Grobman Theorem

For a nonlinear autonomous system $\mathbf{x}' = \mathbf{f}(\mathbf{x})$ with equilibrium at $\mathbf{x}^*$ (where $\mathbf{f}(\mathbf{x}^*) = \mathbf{0}$), the linearization $\mathbf{y}' = A\mathbf{y}$ (with $A = D\mathbf{f}(\mathbf{x}^*)$, the Jacobian) captures the local behavior — but only under certain conditions.

**Theorem (Hartman–Grobman, 1960).** If the equilibrium $\mathbf{x}^*$ is **hyperbolic** (all eigenvalues of $A$ have nonzero real part), then there exists a homeomorphism (continuous bijection with continuous inverse) between the phase portrait of the nonlinear system near $\mathbf{x}^*$ and the phase portrait of the linearization. In particular:
- Stable nodes/spirals of the linearization correspond to stable nodes/spirals of the nonlinear system.
- Unstable nodes/spirals correspond to unstable nodes/spirals.
- Saddle points correspond to saddle points.

**When linearization fails.** If $A$ has eigenvalues on the imaginary axis (non-hyperbolic equilibrium), the linearization does NOT determine the nonlinear behavior:
- A linear center ($\lambda = \pm i\beta$) could become a stable spiral, unstable spiral, or remain a center in the nonlinear system. Higher-order terms decide.
- Example: $x' = -y + x(x^2+y^2)$, $y' = x + y(x^2+y^2)$ has a center at the linearization but is actually an unstable spiral (the cubic terms pump energy in).

**Lyapunov's indirect method.** If all eigenvalues of $A$ have $\text{Re}(\lambda_i) < 0$, then $\mathbf{x}^*$ is asymptotically stable for the full nonlinear system (regardless of higher-order terms). If any eigenvalue has $\text{Re}(\lambda_i) > 0$, the equilibrium is unstable. This is the practical stability test used in control engineering.

*Reference: Strogatz, Nonlinear Dynamics and Chaos (Westview, 2015), §6.3; Perko, Differential Equations and Dynamical Systems (Springer, 2001), §2.8.*

---



### 9.5 Controllability and Observability — The Kalman Criteria

For the linear system $\mathbf{x}' = A\mathbf{x} + B\mathbf{u}$ (with input $\mathbf{u}$) and output $\mathbf{y} = C\mathbf{x}$, two fundamental questions arise in control theory:

**Controllability:** Can we steer the state from any initial condition to any target state using the input $\mathbf{u}(t)$?

**Theorem (Kalman, 1960).** The system $(A, B)$ is controllable if and only if the **controllability matrix**:

$$
\mathcal{C} = \begin{pmatrix} B & AB & A^2B & \cdots & A^{n-1}B \end{pmatrix}
$$

has full rank (rank $= n$, the state dimension).

**Observability:** Can we determine the full state $\mathbf{x}(t)$ from measurements of the output $\mathbf{y}(t)$ alone?

**Theorem (Kalman).** The system $(A, C)$ is observable if and only if the **observability matrix**:

$$
\mathcal{O} = \begin{pmatrix} C \\ CA \\ CA^2 \\ \vdots \\ CA^{n-1} \end{pmatrix}
$$

has full rank.

**Connection to ODE theory.** For the scalar ODE $y^{(n)} + a_{n-1}y^{(n-1)} + \cdots + a_0 y = u(t)$ written in companion form, the controllability matrix is always full rank (the companion form is always controllable). This is why any single-input single-output ODE can be driven to any desired state — a fact that is not obvious from the scalar equation alone.

**Duality.** $(A, B)$ is controllable if and only if $(A^T, B^T)$ is observable. This duality connects state feedback design (pole placement) with observer design (state estimation) — the separation principle of modern control theory.

*Reference: Kailath, Linear Systems (Prentice Hall, 1980), Ch. 2; MIT OCW 6.241, Lecture notes on state-space control.*

---
