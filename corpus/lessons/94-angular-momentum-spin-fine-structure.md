---
title: "Angular Momentum Spin Fine Structure"
subject: "Quantum Mechanics & Quantum Field Theory"
catalog: advanced
audience_tier: higher-education
chapter: "9.4"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 9.4 — Angular Momentum, Spin & Fine Structure

> *"The electron has a spin angular momentum that does not correspond to any spatial motion of the electron. It is an intrinsic property, like its charge or mass."* — Wolfgang Pauli

Angular momentum in quantum mechanics is far richer than its classical counterpart. Orbital angular momentum $\hat{\mathbf{L}}$ arises from spatial motion and is quantized in integer units. But nature also provides **spin** — an intrinsic angular momentum with no classical analogue, quantized in half-integer units for fermions. This chapter develops the full algebraic theory of angular momentum using ladder operators, solves the spin-1/2 eigenvalue problem explicitly, introduces addition of angular momenta (Clebsch-Gordan coefficients), and derives the hydrogen fine structure.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Derive the angular momentum commutation relations $[\hat{J}_i, \hat{J}_j] = i\hbar\epsilon_{ijk}\hat{J}_k$.
2. Construct the ladder operators $\hat{J}_\pm$ and derive the eigenvalue spectrum $j(j+1)\hbar^2$, $m\hbar$.
3. Solve the spin-1/2 eigenvalue problem and construct the Pauli matrices.
4. Compute expectation values and probabilities for spin measurements along arbitrary axes.
5. Add angular momenta using Clebsch-Gordan coefficients.
6. Derive the hydrogen fine structure (spin-orbit coupling).

---

## 🖼️ Visual Anchor — The Bloch Sphere & Spin Precession

![math-09__9.4-fig1](math-09__9.4-fig1.svg)

---

## 📚 1. Definitions

### Definition 9.4.1 — Angular Momentum Operators

The **angular momentum operators** $\hat{J}_x, \hat{J}_y, \hat{J}_z$ satisfy the fundamental commutation relations:

$$
[\hat{J}_i, \hat{J}_j] = i\hbar\,\epsilon_{ijk}\,\hat{J}_k,
$$

where $\epsilon_{ijk}$ is the Levi-Civita symbol. Explicitly:

$$
[\hat{J}_x, \hat{J}_y] = i\hbar\hat{J}_z, \quad [\hat{J}_y, \hat{J}_z] = i\hbar\hat{J}_x, \quad [\hat{J}_z, \hat{J}_x] = i\hbar\hat{J}_y.
$$

### Definition 9.4.2 — Total Angular Momentum Squared

$$
\hat{J}^2 = \hat{J}_x^2 + \hat{J}_y^2 + \hat{J}_z^2.
$$

This commutes with all components: $[\hat{J}^2, \hat{J}_i] = 0$ for $i = x, y, z$.

### Definition 9.4.3 — Ladder Operators

$$
\hat{J}_+ = \hat{J}_x + i\hat{J}_y, \qquad \hat{J}_- = \hat{J}_x - i\hat{J}_y.
$$

Key commutators: $[\hat{J}_z, \hat{J}_\pm] = \pm\hbar\hat{J}_\pm$ and $[\hat{J}_+, \hat{J}_-] = 2\hbar\hat{J}_z$.

### Definition 9.4.4 — Orbital Angular Momentum

For a particle with position $\hat{\mathbf{r}}$ and momentum $\hat{\mathbf{p}}$:

$$
\hat{\mathbf{L}} = \hat{\mathbf{r}} \times \hat{\mathbf{p}}, \quad \hat{L}_z = -i\hbar\frac{\partial}{\partial\phi}.
$$

Eigenvalues: $\ell = 0, 1, 2, \ldots$ (integers only) and $m = -\ell, \ldots, +\ell$.

### Definition 9.4.5 — Spin Angular Momentum

**Spin** $\hat{\mathbf{S}}$ is an intrinsic angular momentum with no classical analogue. For spin-$s$ particles:

$$
\hat{S}^2\vert s, m_s\rangle = s(s+1)\hbar^2\vert s, m_s\rangle, \quad \hat{S}_z\vert s, m_s\rangle = m_s\hbar\vert s, m_s\rangle.
$$

Electrons have $s = 1/2$, so $m_s = \pm 1/2$.

### Definition 9.4.6 — Pauli Matrices

The spin-1/2 operators are $\hat{S}_i = \frac{\hbar}{2}\sigma_i$ where:

$$
\sigma_x = \begin{pmatrix}0&1\\1&0\end{pmatrix}, \quad \sigma_y = \begin{pmatrix}0&-i\\i&0\end{pmatrix}, \quad \sigma_z = \begin{pmatrix}1&0\\0&-1\end{pmatrix}.
$$

### Definition 9.4.7 — Spin-Orbit Coupling

The **spin-orbit interaction** Hamiltonian is:

$$
\hat{H}_{SO} = \frac{1}{2m_e^2 c^2}\frac{1}{r}\frac{dV}{dr}\hat{\mathbf{L}}\cdot\hat{\mathbf{S}}.
$$

For hydrogen: $\hat{\mathbf{L}}\cdot\hat{\mathbf{S}} = \frac{1}{2}(\hat{J}^2 - \hat{L}^2 - \hat{S}^2)$.




---

## 📐 2. Axioms / Postulates

### Postulate 9.4.P1 — Angular Momentum Algebra

Any set of three Hermitian operators satisfying $[\hat{J}_i, \hat{J}_j] = i\hbar\epsilon_{ijk}\hat{J}_k$ constitutes an angular momentum. The algebra alone determines the eigenvalue spectrum — no reference to spatial coordinates is needed.

### Postulate 9.4.P2 — Spin Hypothesis

Elementary particles possess an intrinsic angular momentum (spin) that is not associated with spatial degrees of freedom. Fermions (electrons, quarks) have half-integer spin; bosons (photons, gluons) have integer spin.

### Postulate 9.4.P3 — Addition of Angular Momenta

When two angular momenta $\hat{\mathbf{J}}_1$ and $\hat{\mathbf{J}}_2$ are combined, the total $\hat{\mathbf{J}} = \hat{\mathbf{J}}_1 + \hat{\mathbf{J}}_2$ has quantum numbers $j$ ranging from $|j_1 - j_2|$ to $j_1 + j_2$ in integer steps.

---

## 🛡️ 3. Lemmas

### Lemma 9.4.1 — $[\hat{J}^2, \hat{J}_z] = 0$

**Proof.**

$$
[\hat{J}^2, \hat{J}_z] = [\hat{J}_x^2 + \hat{J}_y^2 + \hat{J}_z^2, \hat{J}_z] = [\hat{J}_x^2, \hat{J}_z] + [\hat{J}_y^2, \hat{J}_z] + 0.
$$

Using $[\hat{A}^2, \hat{B}] = \hat{A}[\hat{A},\hat{B}] + [\hat{A},\hat{B}]\hat{A}$:

$$
[\hat{J}_x^2, \hat{J}_z] = \hat{J}_x[\hat{J}_x, \hat{J}_z] + [\hat{J}_x, \hat{J}_z]\hat{J}_x = \hat{J}_x(-i\hbar\hat{J}_y) + (-i\hbar\hat{J}_y)\hat{J}_x = -i\hbar(\hat{J}_x\hat{J}_y + \hat{J}_y\hat{J}_x).
$$

$$
[\hat{J}_y^2, \hat{J}_z] = \hat{J}_y[\hat{J}_y, \hat{J}_z] + [\hat{J}_y, \hat{J}_z]\hat{J}_y = \hat{J}_y(i\hbar\hat{J}_x) + (i\hbar\hat{J}_x)\hat{J}_y = i\hbar(\hat{J}_y\hat{J}_x + \hat{J}_x\hat{J}_y).
$$

Adding: $[\hat{J}^2, \hat{J}_z] = -i\hbar(\hat{J}_x\hat{J}_y + \hat{J}_y\hat{J}_x) + i\hbar(\hat{J}_y\hat{J}_x + \hat{J}_x\hat{J}_y) = 0$. $\blacksquare$

### Lemma 9.4.2 — $\hat{J}^2$ in Terms of Ladder Operators

$$
\hat{J}^2 = \hat{J}_-\hat{J}_+ + \hat{J}_z^2 + \hbar\hat{J}_z = \hat{J}_+\hat{J}_- + \hat{J}_z^2 - \hbar\hat{J}_z.
$$

**Proof.**

$$
\hat{J}_+\hat{J}_- = (\hat{J}_x + i\hat{J}_y)(\hat{J}_x - i\hat{J}_y) = \hat{J}_x^2 + \hat{J}_y^2 - i[\hat{J}_x, \hat{J}_y] = \hat{J}_x^2 + \hat{J}_y^2 + \hbar\hat{J}_z.
$$

Therefore: $\hat{J}^2 = \hat{J}_x^2 + \hat{J}_y^2 + \hat{J}_z^2 = \hat{J}_+\hat{J}_- - \hbar\hat{J}_z + \hat{J}_z^2$. $\blacksquare$

### Lemma 9.4.3 — Action of $\hat{J}_\pm$ on $\vert j, m\rangle$

$$
\hat{J}_\pm\vert j, m\rangle = \hbar\sqrt{j(j+1) - m(m\pm 1)}\,\vert j, m\pm 1\rangle.
$$

**Proof.** Compute $\|\hat{J}_+\vert j,m\rangle\|^2 = \langle j,m\vert\hat{J}_-\hat{J}_+\vert j,m\rangle$.

Using Lemma 9.4.2: $\hat{J}_-\hat{J}_+ = \hat{J}^2 - \hat{J}_z^2 - \hbar\hat{J}_z$.

$$
= \langle j,m\vert(\hat{J}^2 - \hat{J}_z^2 - \hbar\hat{J}_z)\vert j,m\rangle = \hbar^2[j(j+1) - m^2 - m] = \hbar^2[j(j+1) - m(m+1)].
$$

Therefore $\hat{J}_+\vert j,m\rangle = \hbar\sqrt{j(j+1) - m(m+1)}\,\vert j, m+1\rangle$. $\blacksquare$

### Lemma 9.4.4 — Pauli Matrix Identities

$$
\sigma_i\sigma_j = \delta_{ij}I + i\epsilon_{ijk}\sigma_k, \qquad (\vec{\sigma}\cdot\vec{a})(\vec{\sigma}\cdot\vec{b}) = (\vec{a}\cdot\vec{b})I + i\vec{\sigma}\cdot(\vec{a}\times\vec{b}).
$$

**Proof of the first identity:** Verify for each pair. For $i = j$: $\sigma_i^2 = I$ (direct computation). For $i \neq j$: $\sigma_x\sigma_y = i\sigma_z$ (computed in Example 9.2.1), and cyclic permutations. This matches $\delta_{ij}I + i\epsilon_{ijk}\sigma_k$. $\blacksquare$

---

## 👑 4. Theorems

### Theorem 9.4.1 — Eigenvalue Spectrum of Angular Momentum

The simultaneous eigenstates $\vert j, m\rangle$ of $\hat{J}^2$ and $\hat{J}_z$ satisfy:

$$
\hat{J}^2\vert j, m\rangle = j(j+1)\hbar^2\vert j, m\rangle, \qquad \hat{J}_z\vert j, m\rangle = m\hbar\vert j, m\rangle,
$$

where $j = 0, \frac{1}{2}, 1, \frac{3}{2}, 2, \ldots$ and $m = -j, -j+1, \ldots, j-1, j$.

### Theorem 9.4.2 — Addition of Angular Momenta

For $\hat{\mathbf{J}} = \hat{\mathbf{J}}_1 + \hat{\mathbf{J}}_2$, the coupled basis $\vert j, m\rangle$ relates to the uncoupled basis $\vert j_1, m_1; j_2, m_2\rangle$ via Clebsch-Gordan coefficients:

$$
\vert j, m\rangle = \sum_{m_1 + m_2 = m} \langle j_1, m_1; j_2, m_2 \vert j, m\rangle\,\vert j_1, m_1; j_2, m_2\rangle.
$$

The total quantum number ranges: $j = |j_1 - j_2|, |j_1 - j_2| + 1, \ldots, j_1 + j_2$.

### Theorem 9.4.3 — Hydrogen Fine Structure

The first-order energy correction from spin-orbit coupling for hydrogen is:

$$
E_{SO} = \frac{E_n^2}{m_e c^2}\frac{n[j(j+1) - \ell(\ell+1) - 3/4]}{2\ell(\ell+1/2)(\ell+1)},
$$

where $j = \ell \pm 1/2$. Combined with the relativistic kinetic energy correction, the total fine structure is:

$$
E_{fs} = -\frac{E_n^2}{2m_e c^2}\left(\frac{4n}{j + 1/2} - 3\right).
$$

---

## ✍️ 5. Proofs / Derivations

### 5.1 Derivation of the Angular Momentum Eigenvalue Spectrum

**Step 1:** Let $\vert j, m\rangle$ be a simultaneous eigenstate of $\hat{J}^2$ and $\hat{J}_z$:

$$
\hat{J}^2\vert j, m\rangle = \lambda\hbar^2\vert j, m\rangle, \quad \hat{J}_z\vert j, m\rangle = m\hbar\vert j, m\rangle.
$$

**Step 2:** Since $\hat{J}^2 = \hat{J}_x^2 + \hat{J}_y^2 + \hat{J}_z^2$ and $\hat{J}_x^2, \hat{J}_y^2 \geq 0$:

$$
\lambda\hbar^2 \geq m^2\hbar^2 \implies \lambda \geq m^2.
$$

So $m$ is bounded: $-\sqrt{\lambda} \leq m \leq \sqrt{\lambda}$.

**Step 3:** $\hat{J}_+$ raises $m$ by 1 (from $[\hat{J}_z, \hat{J}_+] = \hbar\hat{J}_+$). Since $m$ is bounded above, there exists $m_{\max}$ such that:

$$
\hat{J}_+\vert j, m_{\max}\rangle = 0.
$$

**Step 4:** Apply $\hat{J}_-\hat{J}_+$ to this state:

$$
\hat{J}_-\hat{J}_+\vert j, m_{\max}\rangle = (\hat{J}^2 - \hat{J}_z^2 - \hbar\hat{J}_z)\vert j, m_{\max}\rangle = (\lambda - m_{\max}^2 - m_{\max})\hbar^2\vert j, m_{\max}\rangle = 0.
$$

Therefore: $\lambda = m_{\max}(m_{\max} + 1)$.

**Step 5:** Similarly, there exists $m_{\min}$ with $\hat{J}_-\vert j, m_{\min}\rangle = 0$, giving $\lambda = m_{\min}(m_{\min} - 1)$.

**Step 6:** From $m_{\max}(m_{\max}+1) = m_{\min}(m_{\min}-1)$:

$$
m_{\max}^2 + m_{\max} = m_{\min}^2 - m_{\min} \implies (m_{\max} + m_{\min})(m_{\max} - m_{\min} + 1) = 0.
$$

Since $m_{\max} \geq m_{\min}$, the second factor is positive, so $m_{\min} = -m_{\max}$.

**Step 7:** Define $j \equiv m_{\max}$. Then $m$ ranges from $-j$ to $+j$ in integer steps. Since $m_{\max} - m_{\min} = 2j$ must be a non-negative integer:

$$
j = 0, \frac{1}{2}, 1, \frac{3}{2}, 2, \ldots
$$

And $\lambda = j(j+1)$. $\blacksquare$

### 5.2 Solving the Spin-1/2 Eigenvalue Problem

**Problem:** Find the eigenvalues and eigenvectors of $\hat{S}_n = \hat{\mathbf{S}}\cdot\hat{n}$ where $\hat{n} = (\sin\theta\cos\phi, \sin\theta\sin\phi, \cos\theta)$.

**Step 1:** Write the matrix:

$$
\hat{S}_n = \frac{\hbar}{2}(\sigma_x\sin\theta\cos\phi + \sigma_y\sin\theta\sin\phi + \sigma_z\cos\theta).
$$

$$
= \frac{\hbar}{2}\begin{pmatrix}\cos\theta & \sin\theta\,e^{-i\phi} \\ \sin\theta\,e^{i\phi} & -\cos\theta\end{pmatrix}.
$$

**Step 2:** The eigenvalues are $\pm\hbar/2$ (since $\hat{S}_n$ is related to $\hat{S}_z$ by a rotation, and rotations preserve eigenvalues).

**Step 3:** Find the eigenvector for $+\hbar/2$. Solve $(\hat{S}_n - \frac{\hbar}{2}I)\vert\chi\rangle = 0$:

$$
\begin{pmatrix}\cos\theta - 1 & \sin\theta\,e^{-i\phi} \\ \sin\theta\,e^{i\phi} & -\cos\theta - 1\end{pmatrix}\begin{pmatrix}a\\b\end{pmatrix} = 0.
$$

From the first row: $(\cos\theta - 1)a + \sin\theta\,e^{-i\phi}b = 0$.

Using $\cos\theta - 1 = -2\sin^2(\theta/2)$ and $\sin\theta = 2\sin(\theta/2)\cos(\theta/2)$:

$$
-2\sin^2(\theta/2)\,a + 2\sin(\theta/2)\cos(\theta/2)\,e^{-i\phi}b = 0.
$$

$$
a = \frac{\cos(\theta/2)}{\sin(\theta/2)}e^{-i\phi}b = \cot(\theta/2)\,e^{-i\phi}b.
$$

Choosing $b = \sin(\theta/2)\,e^{i\phi}$ gives $a = \cos(\theta/2)$:

$$
\vert +\rangle_n = \begin{pmatrix}\cos(\theta/2) \\ e^{i\phi}\sin(\theta/2)\end{pmatrix}.
$$

**Step 4:** The spin-down eigenstate (orthogonal):

$$
\vert -\rangle_n = \begin{pmatrix}-e^{-i\phi}\sin(\theta/2) \\ \cos(\theta/2)\end{pmatrix}.
$$

**Verification:** For $\theta = 0$ (z-axis): $\vert +\rangle_z = \binom{1}{0}$. For $\theta = \pi/2, \phi = 0$ (x-axis): $\vert +\rangle_x = \frac{1}{\sqrt{2}}\binom{1}{1}$. ✓

### 5.3 Derivation of $\hat{\mathbf{L}}\cdot\hat{\mathbf{S}}$ Eigenvalues

**Step 1:** Define $\hat{\mathbf{J}} = \hat{\mathbf{L}} + \hat{\mathbf{S}}$. Then:

$$
\hat{J}^2 = (\hat{\mathbf{L}} + \hat{\mathbf{S}})^2 = \hat{L}^2 + \hat{S}^2 + 2\hat{\mathbf{L}}\cdot\hat{\mathbf{S}}.
$$

**Step 2:** Solve for $\hat{\mathbf{L}}\cdot\hat{\mathbf{S}}$:

$$
\hat{\mathbf{L}}\cdot\hat{\mathbf{S}} = \frac{1}{2}(\hat{J}^2 - \hat{L}^2 - \hat{S}^2).
$$

**Step 3:** Eigenvalues in the $\vert j, m_j, \ell, s\rangle$ basis:

$$
\langle\hat{\mathbf{L}}\cdot\hat{\mathbf{S}}\rangle = \frac{\hbar^2}{2}[j(j+1) - \ell(\ell+1) - s(s+1)].
$$

For $s = 1/2$: $j = \ell + 1/2$ or $j = \ell - 1/2$.

- $j = \ell + 1/2$: $\langle\hat{\mathbf{L}}\cdot\hat{\mathbf{S}}\rangle = \frac{\hbar^2}{2}\ell$.
- $j = \ell - 1/2$: $\langle\hat{\mathbf{L}}\cdot\hat{\mathbf{S}}\rangle = -\frac{\hbar^2}{2}(\ell + 1)$.

$\blacksquare$




---

## 🧮 6. Worked Examples

### Example 9.4.1 — Spin-1/2 Measurement Probabilities

**Problem:** An electron is in the state $\vert\psi\rangle = \frac{1}{\sqrt{3}}\vert\uparrow\rangle + \sqrt{\frac{2}{3}}\vert\downarrow\rangle$. Find the probability of measuring $S_x = +\hbar/2$.

**Solution:**

**Step 1:** The $S_x$ eigenstates are:

$$
\vert +\rangle_x = \frac{1}{\sqrt{2}}\begin{pmatrix}1\\1\end{pmatrix}, \quad \vert -\rangle_x = \frac{1}{\sqrt{2}}\begin{pmatrix}1\\-1\end{pmatrix}.
$$

**Step 2:** Compute the probability amplitude:

$$
{}_x\langle +\vert\psi\rangle = \frac{1}{\sqrt{2}}\begin{pmatrix}1&1\end{pmatrix}\begin{pmatrix}1/\sqrt{3}\\\sqrt{2/3}\end{pmatrix} = \frac{1}{\sqrt{2}}\left(\frac{1}{\sqrt{3}} + \sqrt{\frac{2}{3}}\right) = \frac{1}{\sqrt{2}}\cdot\frac{1+\sqrt{2}}{\sqrt{3}}.
$$

**Step 3:** Probability:

$$
P(S_x = +\hbar/2) = |{}_x\langle +\vert\psi\rangle|^2 = \frac{1}{2}\cdot\frac{(1+\sqrt{2})^2}{3} = \frac{3 + 2\sqrt{2}}{6} \approx 0.971.
$$

---

### Example 9.4.2 — Adding Two Spin-1/2 Particles

**Problem:** Two electrons have spins $\hat{\mathbf{S}}_1$ and $\hat{\mathbf{S}}_2$ (both $s = 1/2$). Find the total spin states $\vert S, M\rangle$.

**Solution:**

**Step 1:** The total spin $S$ ranges from $|s_1 - s_2| = 0$ to $s_1 + s_2 = 1$. So $S = 0$ (singlet) or $S = 1$ (triplet).

**Step 2:** The **triplet** states ($S = 1$, symmetric):

$$
\vert 1, 1\rangle = \vert\uparrow\uparrow\rangle,
$$

$$
\vert 1, 0\rangle = \frac{1}{\sqrt{2}}(\vert\uparrow\downarrow\rangle + \vert\downarrow\uparrow\rangle),
$$

$$
\vert 1, -1\rangle = \vert\downarrow\downarrow\rangle.
$$

**Step 3:** The **singlet** state ($S = 0$, antisymmetric):

$$
\vert 0, 0\rangle = \frac{1}{\sqrt{2}}(\vert\uparrow\downarrow\rangle - \vert\downarrow\uparrow\rangle).
$$

**Step 4:** Verify using $\hat{S}^2 = (\hat{\mathbf{S}}_1 + \hat{\mathbf{S}}_2)^2 = \hat{S}_1^2 + \hat{S}_2^2 + 2\hat{\mathbf{S}}_1\cdot\hat{\mathbf{S}}_2$:

For the singlet: $\hat{\mathbf{S}}_1\cdot\hat{\mathbf{S}}_2\vert 0,0\rangle = \frac{1}{2}(S(S+1) - s_1(s_1+1) - s_2(s_2+1))\hbar^2\vert 0,0\rangle = \frac{1}{2}(0 - 3/4 - 3/4)\hbar^2 = -\frac{3}{4}\hbar^2$.

For the triplet: $\hat{\mathbf{S}}_1\cdot\hat{\mathbf{S}}_2 = \frac{1}{2}(2 - 3/4 - 3/4)\hbar^2 = \frac{1}{4}\hbar^2$. ✓

---

### Example 9.4.3 — Expectation Value of $\hat{S}_x$ in a General Spin State

**Problem:** For $\vert\psi\rangle = \cos(\theta/2)\vert\uparrow\rangle + e^{i\phi}\sin(\theta/2)\vert\downarrow\rangle$, compute $\langle\hat{S}_x\rangle$, $\langle\hat{S}_y\rangle$, $\langle\hat{S}_z\rangle$.

**Solution:**

$$
\langle\hat{S}_z\rangle = \frac{\hbar}{2}\left(\cos^2(\theta/2) - \sin^2(\theta/2)\right) = \frac{\hbar}{2}\cos\theta.
$$

$$
\langle\hat{S}_x\rangle = \frac{\hbar}{2}\langle\psi\vert\sigma_x\vert\psi\rangle = \frac{\hbar}{2}\begin{pmatrix}\cos(\theta/2) & e^{-i\phi}\sin(\theta/2)\end{pmatrix}\begin{pmatrix}0&1\\1&0\end{pmatrix}\begin{pmatrix}\cos(\theta/2)\\e^{i\phi}\sin(\theta/2)\end{pmatrix}.
$$

$$
= \frac{\hbar}{2}\begin{pmatrix}\cos(\theta/2) & e^{-i\phi}\sin(\theta/2)\end{pmatrix}\begin{pmatrix}e^{i\phi}\sin(\theta/2)\\\cos(\theta/2)\end{pmatrix}.
$$

$$
= \frac{\hbar}{2}\left(e^{i\phi}\cos(\theta/2)\sin(\theta/2) + e^{-i\phi}\sin(\theta/2)\cos(\theta/2)\right) = \frac{\hbar}{2}\sin\theta\cos\phi.
$$

Similarly: $\langle\hat{S}_y\rangle = \frac{\hbar}{2}\sin\theta\sin\phi$.

**Result:** $\langle\hat{\mathbf{S}}\rangle = \frac{\hbar}{2}(\sin\theta\cos\phi, \sin\theta\sin\phi, \cos\theta) = \frac{\hbar}{2}\hat{n}$.

The expectation value of the spin vector points along the Bloch sphere direction $(\theta, \phi)$. ✓

---

### Example 9.4.4 — Hydrogen Fine Structure for the 2p State

**Problem:** Compute the fine-structure splitting of the hydrogen $n = 2$, $\ell = 1$ level.

**Solution:**

**Step 1:** For $\ell = 1$, $s = 1/2$: $j = 3/2$ or $j = 1/2$.

**Step 2:** The fine-structure formula:

$$
E_{fs} = -\frac{E_n^2}{2m_e c^2}\left(\frac{4n}{j+1/2} - 3\right).
$$

For $n = 2$, $E_2 = -13.6/4 = -3.4$ eV:

$$
\frac{E_2^2}{2m_e c^2} = \frac{(3.4)^2}{2 \times 511000} \text{ eV} = 1.13 \times 10^{-5} \text{ eV}.
$$

**Step 3:** For $j = 3/2$: $\frac{4\cdot2}{3/2+1/2} - 3 = \frac{8}{2} - 3 = 1$. So $E_{fs}(j=3/2) = -1.13 \times 10^{-5}$ eV.

For $j = 1/2$: $\frac{4\cdot2}{1/2+1/2} - 3 = 8 - 3 = 5$. So $E_{fs}(j=1/2) = -5.66 \times 10^{-5}$ eV.

**Step 4:** The splitting:

$$
\Delta E = E_{fs}(j=3/2) - E_{fs}(j=1/2) = 4.53 \times 10^{-5} \text{ eV} \approx 0.45 \text{ cm}^{-1}.
$$

This is the famous hydrogen fine-structure doublet, observable spectroscopically.

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- [2.6 - Eigenvalues Eigenvectors & Diagonalization](2.6---Eigenvalues-Eigenvectors-&-Diagonalization) — Spin matrices are diagonalized to find measurement outcomes
- [2.7 - Inner Product Spaces & Orthogonality](2.7---Inner-Product-Spaces-&-Orthogonality) — Orthogonality of angular momentum eigenstates
- [9.2 - Hilbert Space & Bra-Ket Formalism](9.2---Hilbert-Space-&-Bra-Ket-Formalism) — Abstract operator algebra
- [9.3 - The 1D Infinite Square Well & Harmonic Oscillator](9.3---The-1D-Infinite-Square-Well-&-Harmonic-Oscillator) — Ladder operator technique generalized here
- [9.5 - Time-Independent Perturbation Theory](9.5---Time-Independent-Perturbation-Theory) — Fine structure as a perturbation
- [9.6 - Relativistic QM - Klein-Gordon & Dirac Equations](9.6---Relativistic-QM---Klein-Gordon-&-Dirac-Equations) — Spin emerges naturally from the Dirac equation

### External References
- **Griffiths, D.J.** *Introduction to Quantum Mechanics* — Chapter 4 (angular momentum, spin, addition).
- **Susskind, L.** *Quantum Mechanics: The Theoretical Minimum* — Lectures on spin and entanglement.
- **Sakurai, J.J.** *Modern Quantum Mechanics* — Chapter 3 (definitive treatment of angular momentum).
- **Tong, D.** [QFT Notes](https://www.damtp.cam.ac.uk/user/tong/qft.html) — Spinor representations.

---

*Next: [9.5 - Time-Independent Perturbation Theory](9.5---Time-Independent-Perturbation-Theory) — Systematic approximation methods.*




---

## ✍️ Additional Proofs

### 5.4 Proof: Pauli Matrices Satisfy the Angular Momentum Algebra

**Goal:** Verify $[\sigma_i, \sigma_j] = 2i\epsilon_{ijk}\sigma_k$ (which gives $[\hat{S}_i, \hat{S}_j] = i\hbar\epsilon_{ijk}\hat{S}_k$).

**$[\sigma_x, \sigma_y]$:**

$$
\sigma_x\sigma_y = \begin{pmatrix}0&1\\1&0\end{pmatrix}\begin{pmatrix}0&-i\\i&0\end{pmatrix} = \begin{pmatrix}i&0\\0&-i\end{pmatrix} = i\sigma_z.
$$

$$
\sigma_y\sigma_x = \begin{pmatrix}0&-i\\i&0\end{pmatrix}\begin{pmatrix}0&1\\1&0\end{pmatrix} = \begin{pmatrix}-i&0\\0&i\end{pmatrix} = -i\sigma_z.
$$

$$
[\sigma_x, \sigma_y] = i\sigma_z - (-i\sigma_z) = 2i\sigma_z. \quad \checkmark
$$

**$[\sigma_y, \sigma_z]$:**

$$
\sigma_y\sigma_z = \begin{pmatrix}0&-i\\i&0\end{pmatrix}\begin{pmatrix}1&0\\0&-1\end{pmatrix} = \begin{pmatrix}0&i\\i&0\end{pmatrix} = i\sigma_x.
$$

$$
\sigma_z\sigma_y = \begin{pmatrix}1&0\\0&-1\end{pmatrix}\begin{pmatrix}0&-i\\i&0\end{pmatrix} = \begin{pmatrix}0&-i\\-i&0\end{pmatrix} = -i\sigma_x.
$$

$$
[\sigma_y, \sigma_z] = 2i\sigma_x. \quad \checkmark
$$

**$[\sigma_z, \sigma_x]$:**

$$
\sigma_z\sigma_x = \begin{pmatrix}1&0\\0&-1\end{pmatrix}\begin{pmatrix}0&1\\1&0\end{pmatrix} = \begin{pmatrix}0&1\\-1&0\end{pmatrix} = i\sigma_y.
$$

$$
\sigma_x\sigma_z = \begin{pmatrix}0&1\\1&0\end{pmatrix}\begin{pmatrix}1&0\\0&-1\end{pmatrix} = \begin{pmatrix}0&-1\\1&0\end{pmatrix} = -i\sigma_y.
$$

$$
[\sigma_z, \sigma_x] = 2i\sigma_y. \quad \checkmark \quad \blacksquare
$$

### 5.5 Derivation: $\hat{J}^2$ Eigenvalue from Ladder Operators

**Step 1:** We have $\hat{J}^2 = \hat{J}_+\hat{J}_- + \hat{J}_z^2 - \hbar\hat{J}_z$ (Lemma 9.4.2).

**Step 2:** Act on the top state $\vert j, j\rangle$ where $\hat{J}_+\vert j, j\rangle = 0$:

$$
\hat{J}^2\vert j, j\rangle = (0 + j^2\hbar^2 + j\hbar^2 - j\hbar\cdot\hbar)\vert j, j\rangle.
$$

Wait — let me use the correct form: $\hat{J}^2 = \hat{J}_-\hat{J}_+ + \hat{J}_z^2 + \hbar\hat{J}_z$.

Since $\hat{J}_+\vert j, j\rangle = 0$:

$$
\hat{J}^2\vert j, j\rangle = (0 + j^2\hbar^2 + j\hbar^2)\vert j, j\rangle = j(j+1)\hbar^2\vert j, j\rangle. \quad \blacksquare
$$

### 5.6 Clebsch-Gordan Decomposition: $\frac{1}{2} \otimes \frac{1}{2} = 1 \oplus 0$

**Step 1:** Start with the highest-weight state: $\vert 1, 1\rangle = \vert\uparrow\uparrow\rangle$ (the only state with $M = 1$).

**Step 2:** Apply $\hat{J}_- = \hat{J}_{1-} + \hat{J}_{2-}$ to get $\vert 1, 0\rangle$:

$$
\hat{J}_-\vert 1, 1\rangle = \hbar\sqrt{1(1+1) - 1(1-1)}\vert 1, 0\rangle = \hbar\sqrt{2}\vert 1, 0\rangle.
$$

$$
(\hat{J}_{1-} + \hat{J}_{2-})\vert\uparrow\uparrow\rangle = \hbar(\vert\downarrow\uparrow\rangle + \vert\uparrow\downarrow\rangle).
$$

Therefore: $\vert 1, 0\rangle = \frac{1}{\sqrt{2}}(\vert\uparrow\downarrow\rangle + \vert\downarrow\uparrow\rangle)$.

**Step 3:** Apply $\hat{J}_-$ again to get $\vert 1, -1\rangle$:

$$
\hat{J}_-\vert 1, 0\rangle = \hbar\sqrt{2}\vert 1, -1\rangle.
$$

$$
(\hat{J}_{1-}+\hat{J}_{2-})\frac{1}{\sqrt{2}}(\vert\uparrow\downarrow\rangle + \vert\downarrow\uparrow\rangle) = \frac{\hbar}{\sqrt{2}}(\vert\downarrow\downarrow\rangle + \vert\downarrow\downarrow\rangle) = \frac{2\hbar}{\sqrt{2}}\vert\downarrow\downarrow\rangle = \hbar\sqrt{2}\vert\downarrow\downarrow\rangle.
$$

Therefore: $\vert 1, -1\rangle = \vert\downarrow\downarrow\rangle$. ✓

**Step 4:** The singlet $\vert 0, 0\rangle$ is orthogonal to $\vert 1, 0\rangle$ in the $M = 0$ subspace:

$$
\vert 0, 0\rangle = \frac{1}{\sqrt{2}}(\vert\uparrow\downarrow\rangle - \vert\downarrow\uparrow\rangle). \quad \blacksquare
$$

### 5.7 Spin Precession in a Magnetic Field

**Problem:** An electron with spin state $\vert\psi(0)\rangle = \vert +\rangle_x$ is placed in a uniform field $\mathbf{B} = B\hat{z}$. Find $\vert\psi(t)\rangle$.

**Step 1:** The Hamiltonian is $\hat{H} = -\gamma\hat{\mathbf{S}}\cdot\mathbf{B} = -\gamma B\hat{S}_z = \frac{\omega_0}{2}\hbar\sigma_z$ where $\omega_0 = eB/(mc)$ (Larmor frequency).

**Step 2:** Express initial state in $S_z$ basis: $\vert +\rangle_x = \frac{1}{\sqrt{2}}(\vert\uparrow\rangle + \vert\downarrow\rangle)$.

**Step 3:** Time evolution:

$$
\vert\psi(t)\rangle = \frac{1}{\sqrt{2}}(e^{-i\omega_0 t/2}\vert\uparrow\rangle + e^{+i\omega_0 t/2}\vert\downarrow\rangle).
$$

**Step 4:** Expectation values:

$$
\langle S_x\rangle = \frac{\hbar}{2}\cos(\omega_0 t), \quad \langle S_y\rangle = -\frac{\hbar}{2}\sin(\omega_0 t), \quad \langle S_z\rangle = 0.
$$

The spin precesses about the $z$-axis at the Larmor frequency — exactly as predicted classically for a magnetic moment in a field. $\blacksquare$




---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — Angular Momentum Ladder Operator Algebra: $\hat{L}_+, \hat{L}_-, \hat{L}^2$

**Problem:** Starting from $[\hat{L}_i, \hat{L}_j] = i\hbar\epsilon_{ijk}\hat{L}_k$, derive the action of $\hat{L}_\pm$ on $\vert l, m\rangle$ and find the normalization constants.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Define Ladder Operators

$$
\hat{L}_+ = \hat{L}_x + i\hat{L}_y, \qquad \hat{L}_- = \hat{L}_x - i\hat{L}_y.
$$

#### Step 2: Compute $[\hat{L}_z, \hat{L}_+]$

$$
[\hat{L}_z, \hat{L}_+] = [\hat{L}_z, \hat{L}_x + i\hat{L}_y] = [\hat{L}_z, \hat{L}_x] + i[\hat{L}_z, \hat{L}_y].
$$

From the fundamental commutation relations: $[\hat{L}_z, \hat{L}_x] = i\hbar\hat{L}_y$ and $[\hat{L}_z, \hat{L}_y] = -i\hbar\hat{L}_x$.

$$
[\hat{L}_z, \hat{L}_+] = i\hbar\hat{L}_y + i(-i\hbar\hat{L}_x) = i\hbar\hat{L}_y + \hbar\hat{L}_x = \hbar(\hat{L}_x + i\hat{L}_y) = +\hbar\hat{L}_+.
$$

Similarly: $[\hat{L}_z, \hat{L}_-] = -\hbar\hat{L}_-$.

#### Step 3: $\hat{L}_+$ Raises $m$ by One Unit

If $\hat{L}_z\vert l,m\rangle = m\hbar\vert l,m\rangle$, then:

$$
\hat{L}_z(\hat{L}_+\vert l,m\rangle) = (\hat{L}_+\hat{L}_z + \hbar\hat{L}_+)\vert l,m\rangle = (m\hbar + \hbar)\hat{L}_+\vert l,m\rangle = (m+1)\hbar\,\hat{L}_+\vert l,m\rangle.
$$

So $\hat{L}_+\vert l,m\rangle \propto \vert l, m+1\rangle$.

#### Step 4: Compute $[\hat{L}_+, \hat{L}_-]$

$$
[\hat{L}_+, \hat{L}_-] = [\hat{L}_x + i\hat{L}_y, \hat{L}_x - i\hat{L}_y].
$$

$$
= [\hat{L}_x, \hat{L}_x] - i[\hat{L}_x, \hat{L}_y] + i[\hat{L}_y, \hat{L}_x] - i^2[\hat{L}_y, \hat{L}_y].
$$

$$
= 0 - i(i\hbar\hat{L}_z) + i(-i\hbar\hat{L}_z) + 0 = \hbar\hat{L}_z + \hbar\hat{L}_z = 2\hbar\hat{L}_z.
$$

#### Step 5: Express $\hat{L}^2$ Using Ladder Operators

$$
\hat{L}_-\hat{L}_+ = (\hat{L}_x - i\hat{L}_y)(\hat{L}_x + i\hat{L}_y) = \hat{L}_x^2 + i\hat{L}_x\hat{L}_y - i\hat{L}_y\hat{L}_x + \hat{L}_y^2.
$$

$$
= \hat{L}_x^2 + \hat{L}_y^2 + i[\hat{L}_x, \hat{L}_y] = (\hat{L}^2 - \hat{L}_z^2) + i(i\hbar\hat{L}_z) = \hat{L}^2 - \hat{L}_z^2 - \hbar\hat{L}_z.
$$

Therefore:

$$
\hat{L}^2 = \hat{L}_-\hat{L}_+ + \hat{L}_z^2 + \hbar\hat{L}_z = \hat{L}_+\hat{L}_- + \hat{L}_z^2 - \hbar\hat{L}_z.
$$

#### Step 6: Normalization of $\hat{L}_+\vert l,m\rangle$

$$
\|\hat{L}_+\vert l,m\rangle\|^2 = \langle l,m\vert\hat{L}_-\hat{L}_+\vert l,m\rangle = \langle l,m\vert(\hat{L}^2 - \hat{L}_z^2 - \hbar\hat{L}_z)\vert l,m\rangle.
$$

$$
= \hbar^2[l(l+1) - m^2 - m] = \hbar^2[l(l+1) - m(m+1)].
$$

Therefore:

$$
\boxed{\hat{L}_+\vert l,m\rangle = \hbar\sqrt{l(l+1) - m(m+1)}\,\vert l, m+1\rangle.}
$$

$$
\boxed{\hat{L}_-\vert l,m\rangle = \hbar\sqrt{l(l+1) - m(m-1)}\,\vert l, m-1\rangle.}
$$

#### Step 7: Verify Termination

At $m = l$: $\hat{L}_+\vert l,l\rangle = \hbar\sqrt{l(l+1) - l(l+1)}\vert l,l+1\rangle = 0$. ✓

At $m = -l$: $\hat{L}_-\vert l,-l\rangle = \hbar\sqrt{l(l+1) - (-l)(-l-1)}\vert l,-l-1\rangle = \hbar\sqrt{l(l+1) - l(l+1)} = 0$. ✓ $\blacksquare$

</details>

### Example 8.2 — Spin-1/2 Measurement Probabilities: Stern-Gerlach

**Problem:** A spin-1/2 particle is prepared in the state $\vert +\rangle_z$ (spin-up along $z$). It passes through a Stern-Gerlach apparatus oriented along the direction $\hat{n} = \sin\theta\cos\phi\,\hat{x} + \sin\theta\sin\phi\,\hat{y} + \cos\theta\,\hat{z}$. Find the probabilities of measuring spin-up and spin-down along $\hat{n}$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: The Spin Operator Along $\hat{n}$

$$
\hat{S}_n = \hat{\mathbf{S}}\cdot\hat{n} = S_x\sin\theta\cos\phi + S_y\sin\theta\sin\phi + S_z\cos\theta.
$$

In matrix form ($\hat{S}_i = \frac{\hbar}{2}\sigma_i$):

$$
\hat{S}_n = \frac{\hbar}{2}\begin{pmatrix}\cos\theta & \sin\theta\,e^{-i\phi}\\ \sin\theta\,e^{i\phi} & -\cos\theta\end{pmatrix}.
$$

#### Step 2: Find Eigenstates of $\hat{S}_n$

For eigenvalue $+\hbar/2$: solve $(\hat{S}_n - \frac{\hbar}{2}I)\vert\chi\rangle = 0$:

$$
\begin{pmatrix}\cos\theta - 1 & \sin\theta\,e^{-i\phi}\\ \sin\theta\,e^{i\phi} & -\cos\theta - 1\end{pmatrix}\begin{pmatrix}a\\b\end{pmatrix} = 0.
$$

From the first row: $(\cos\theta - 1)a + \sin\theta\,e^{-i\phi}b = 0$.

Using $\cos\theta - 1 = -2\sin^2(\theta/2)$ and $\sin\theta = 2\sin(\theta/2)\cos(\theta/2)$:

$$
-2\sin^2(\theta/2)\,a + 2\sin(\theta/2)\cos(\theta/2)\,e^{-i\phi}b = 0.
$$

$$
a = \frac{\cos(\theta/2)}{\sin(\theta/2)}\,e^{-i\phi}b \cdot \frac{\sin(\theta/2)}{\sin(\theta/2)} = \frac{\cos(\theta/2)e^{-i\phi}b}{\sin(\theta/2)}.
$$

Wait — more carefully: dividing by $-2\sin(\theta/2)$:

$$
\sin(\theta/2)\,a = \cos(\theta/2)\,e^{-i\phi}b.
$$

Choose $b = \sin(\theta/2)\,e^{i\phi}$, then $a = \cos(\theta/2)$. Normalized:

$$
\vert +\rangle_n = \cos(\theta/2)\vert +\rangle_z + \sin(\theta/2)\,e^{i\phi}\vert -\rangle_z.
$$

For eigenvalue $-\hbar/2$:

$$
\vert -\rangle_n = -\sin(\theta/2)\,e^{-i\phi}\vert +\rangle_z + \cos(\theta/2)\vert -\rangle_z.
$$

Wait — let's use the standard convention. The orthogonal state is:

$$
\vert -\rangle_n = \sin(\theta/2)\vert +\rangle_z - \cos(\theta/2)\,e^{i\phi}\vert -\rangle_z.
$$

Actually, the standard result (Sakurai §1.4) is:

$$
\vert +\rangle_n = \cos\frac{\theta}{2}\vert +\rangle_z + \sin\frac{\theta}{2}\,e^{i\phi}\vert -\rangle_z,
$$

$$
\vert -\rangle_n = \sin\frac{\theta}{2}\vert +\rangle_z - \cos\frac{\theta}{2}\,e^{i\phi}\vert -\rangle_z.
$$

#### Step 3: Compute Probabilities

The initial state is $\vert\psi\rangle = \vert +\rangle_z$. Project onto the eigenstates of $\hat{S}_n$:

$$
P(+\hat{n}) = |\langle +_n\vert +_z\rangle|^2 = |\cos(\theta/2)|^2 = \cos^2(\theta/2).
$$

$$
P(-\hat{n}) = |\langle -_n\vert +_z\rangle|^2 = |\sin(\theta/2)|^2 = \sin^2(\theta/2).
$$

#### Step 4: Verify and Interpret

Check: $P(+) + P(-) = \cos^2(\theta/2) + \sin^2(\theta/2) = 1$. ✓

Special cases:
- $\theta = 0$ (measure along $z$): $P(+) = 1$, $P(-) = 0$. ✓
- $\theta = \pi/2$ (measure along $x$ or $y$): $P(+) = P(-) = 1/2$.
- $\theta = \pi$ (measure along $-z$): $P(+) = 0$, $P(-) = 1$. ✓

The result is independent of $\phi$ — only the angle between the spin direction and measurement axis matters for probabilities. $\blacksquare$

</details>



### Example 8.3 — Addition of Angular Momenta: $j_1 = 1/2 \oplus j_2 = 1/2$ via Clebsch-Gordan

**Problem:** Two spin-1/2 particles are coupled. Decompose the product space into irreducible representations and find all Clebsch-Gordan coefficients explicitly.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Identify the Product Space

The product space is $\mathcal{H}_{1/2} \otimes \mathcal{H}_{1/2}$, dimension $2 \times 2 = 4$. The uncoupled basis is:

$$
\vert\uparrow\uparrow\rangle, \quad \vert\uparrow\downarrow\rangle, \quad \vert\downarrow\uparrow\rangle, \quad \vert\downarrow\downarrow\rangle.
$$

By the addition rule: $j = j_1 + j_2, j_1 + j_2 - 1, \ldots, |j_1 - j_2| = 1, 0$.

So the coupled basis has a **triplet** ($j = 1$, three states) and a **singlet** ($j = 0$, one state). Total: $3 + 1 = 4$. ✓

#### Step 2: The Stretched State $\vert 1, 1\rangle$

The maximum $m$ state is unique:

$$
\vert 1, 1\rangle = \vert\uparrow\uparrow\rangle.
$$

(Only one way to get $m = m_1 + m_2 = 1/2 + 1/2 = 1$.)

#### Step 3: Apply $\hat{J}_- = \hat{J}_{1-} + \hat{J}_{2-}$ to Get $\vert 1, 0\rangle$

Left side:

$$
\hat{J}_-\vert 1, 1\rangle = \hbar\sqrt{1(1+1) - 1(1-1)}\,\vert 1, 0\rangle = \hbar\sqrt{2}\,\vert 1, 0\rangle.
$$

Right side:

$$
(\hat{J}_{1-} + \hat{J}_{2-})\vert\uparrow\uparrow\rangle = \hbar\sqrt{\tfrac{1}{2}\cdot\tfrac{3}{2} - \tfrac{1}{2}(-\tfrac{1}{2})}\vert\downarrow\uparrow\rangle + \hbar\sqrt{\tfrac{1}{2}\cdot\tfrac{3}{2} - \tfrac{1}{2}(-\tfrac{1}{2})}\vert\uparrow\downarrow\rangle.
$$

$$
= \hbar\cdot 1\cdot\vert\downarrow\uparrow\rangle + \hbar\cdot 1\cdot\vert\uparrow\downarrow\rangle.
$$

Equating: $\hbar\sqrt{2}\vert 1,0\rangle = \hbar(\vert\downarrow\uparrow\rangle + \vert\uparrow\downarrow\rangle)$.

$$
\boxed{\vert 1, 0\rangle = \frac{1}{\sqrt{2}}(\vert\uparrow\downarrow\rangle + \vert\downarrow\uparrow\rangle).}
$$

#### Step 4: Apply $\hat{J}_-$ Again to Get $\vert 1, -1\rangle$

$$
\hat{J}_-\vert 1, 0\rangle = \hbar\sqrt{1(2) - 0(-1)}\vert 1,-1\rangle = \hbar\sqrt{2}\vert 1,-1\rangle.
$$

$$
(\hat{J}_{1-} + \hat{J}_{2-})\frac{1}{\sqrt{2}}(\vert\uparrow\downarrow\rangle + \vert\downarrow\uparrow\rangle).
$$

$$
= \frac{1}{\sqrt{2}}\left[\hat{J}_{1-}\vert\uparrow\downarrow\rangle + \hat{J}_{2-}\vert\uparrow\downarrow\rangle + \hat{J}_{1-}\vert\downarrow\uparrow\rangle + \hat{J}_{2-}\vert\downarrow\uparrow\rangle\right].
$$

$$
= \frac{1}{\sqrt{2}}\left[\hbar\vert\downarrow\downarrow\rangle + 0 + 0 + \hbar\vert\downarrow\downarrow\rangle\right] = \frac{2\hbar}{\sqrt{2}}\vert\downarrow\downarrow\rangle = \hbar\sqrt{2}\vert\downarrow\downarrow\rangle.
$$

Therefore: $\vert 1, -1\rangle = \vert\downarrow\downarrow\rangle$. ✓

#### Step 5: The Singlet State $\vert 0, 0\rangle$

This must be orthogonal to $\vert 1, 0\rangle$ in the $m = 0$ subspace (spanned by $\vert\uparrow\downarrow\rangle$ and $\vert\downarrow\uparrow\rangle$):

$$
\boxed{\vert 0, 0\rangle = \frac{1}{\sqrt{2}}(\vert\uparrow\downarrow\rangle - \vert\downarrow\uparrow\rangle).}
$$

#### Step 6: Verify $\hat{J}^2\vert 0,0\rangle = 0$

$$
\hat{J}^2 = \hat{J}_1^2 + \hat{J}_2^2 + 2\hat{\mathbf{J}}_1\cdot\hat{\mathbf{J}}_2 = \hat{J}_1^2 + \hat{J}_2^2 + 2\hat{J}_{1z}\hat{J}_{2z} + \hat{J}_{1+}\hat{J}_{2-} + \hat{J}_{1-}\hat{J}_{2+}.
$$

Apply to $\vert 0,0\rangle = \frac{1}{\sqrt{2}}(\vert\uparrow\downarrow\rangle - \vert\downarrow\uparrow\rangle)$:

$\hat{J}_1^2 + \hat{J}_2^2$ gives $\frac{3}{4}\hbar^2 + \frac{3}{4}\hbar^2 = \frac{3}{2}\hbar^2$ on each term.

$2\hat{J}_{1z}\hat{J}_{2z}$: on $\vert\uparrow\downarrow\rangle$ gives $2(\hbar/2)(-\hbar/2) = -\hbar^2/2$; on $\vert\downarrow\uparrow\rangle$ gives $2(-\hbar/2)(\hbar/2) = -\hbar^2/2$.

$\hat{J}_{1+}\hat{J}_{2-}\vert\uparrow\downarrow\rangle = 0$ (can't raise first spin); $\hat{J}_{1+}\hat{J}_{2-}\vert\downarrow\uparrow\rangle = \hbar^2\vert\uparrow\downarrow\rangle$.

$\hat{J}_{1-}\hat{J}_{2+}\vert\uparrow\downarrow\rangle = \hbar^2\vert\downarrow\uparrow\rangle$; $\hat{J}_{1-}\hat{J}_{2+}\vert\downarrow\uparrow\rangle = 0$.

Collecting on $\vert 0,0\rangle = \frac{1}{\sqrt{2}}(\vert\uparrow\downarrow\rangle - \vert\downarrow\uparrow\rangle)$:

$$
\hat{J}^2\vert 0,0\rangle = \frac{1}{\sqrt{2}}\left[(\tfrac{3}{2}\hbar^2 - \tfrac{1}{2}\hbar^2)\vert\uparrow\downarrow\rangle + \hbar^2\vert\downarrow\uparrow\rangle - (\tfrac{3}{2}\hbar^2 - \tfrac{1}{2}\hbar^2)\vert\downarrow\uparrow\rangle - \hbar^2\vert\uparrow\downarrow\rangle\right].
$$

$$
= \frac{1}{\sqrt{2}}\left[\hbar^2\vert\uparrow\downarrow\rangle + \hbar^2\vert\downarrow\uparrow\rangle - \hbar^2\vert\downarrow\uparrow\rangle - \hbar^2\vert\uparrow\downarrow\rangle\right] = 0. \quad \checkmark \; \blacksquare
$$

</details>

### Example 8.4 — Fine-Structure Correction to Hydrogen $2P$ Level

**Problem:** Compute the fine-structure energy correction to the $n = 2$, $l = 1$ level of hydrogen, including both the relativistic kinetic energy correction and the spin-orbit coupling.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: The Fine-Structure Hamiltonian

The fine-structure correction has two parts:

$$
\hat{H}_{\text{fs}} = \hat{H}_{\text{rel}} + \hat{H}_{\text{SO}},
$$

where:

$$
\hat{H}_{\text{rel}} = -\frac{\hat{p}^4}{8m^3c^2} \quad \text{(relativistic kinetic energy correction)},
$$

$$
\hat{H}_{\text{SO}} = \frac{e^2}{8\pi\epsilon_0}\frac{1}{m^2c^2r^3}\hat{\mathbf{L}}\cdot\hat{\mathbf{S}} \quad \text{(spin-orbit coupling)}.
$$

#### Step 2: Combined Fine-Structure Formula (Griffiths Result)

The combined first-order correction for hydrogen is:

$$
E_{\text{fs}}^{(1)} = -\frac{E_n^2}{2mc^2}\left(\frac{4n}{j + 1/2} - 3\right),
$$

where $E_n = -13.6\,\text{eV}/n^2$ is the unperturbed energy.

#### Step 3: Apply to $n = 2$, $l = 1$

For $l = 1$ and $s = 1/2$, the possible total angular momentum values are $j = l + s = 3/2$ and $j = l - s = 1/2$.

**Case 1: $j = 3/2$ (the $2P_{3/2}$ state)**

$$
E_{\text{fs}}^{(1)} = -\frac{E_2^2}{2mc^2}\left(\frac{4\cdot 2}{3/2 + 1/2} - 3\right) = -\frac{E_2^2}{2mc^2}\left(\frac{8}{2} - 3\right) = -\frac{E_2^2}{2mc^2}\cdot 1.
$$

**Case 2: $j = 1/2$ (the $2P_{1/2}$ state)**

$$
E_{\text{fs}}^{(1)} = -\frac{E_2^2}{2mc^2}\left(\frac{8}{1} - 3\right) = -\frac{E_2^2}{2mc^2}\cdot 5.
$$

#### Step 4: Numerical Values

$E_2 = -13.6/4 = -3.4$ eV. $mc^2 = 0.511 \times 10^6$ eV.

$$
\frac{E_2^2}{2mc^2} = \frac{(3.4)^2}{2 \times 511000} = \frac{11.56}{1.022 \times 10^6} = 1.131 \times 10^{-5}\;\text{eV}.
$$

- $2P_{3/2}$: $\Delta E = -1.131 \times 10^{-5}$ eV.
- $2P_{1/2}$: $\Delta E = -5.655 \times 10^{-5}$ eV.

#### Step 5: The Fine-Structure Splitting

$$
\Delta E_{\text{fs}}(2P_{3/2} - 2P_{1/2}) = (5 - 1)\cdot\frac{E_2^2}{2mc^2} = 4\cdot 1.131\times 10^{-5} = 4.52 \times 10^{-5}\;\text{eV}.
$$

This corresponds to a wavelength splitting of about $0.016$ nm — observable in high-resolution spectroscopy.

Note: The $2S_{1/2}$ and $2P_{1/2}$ states have the same $j = 1/2$ and thus the same fine-structure energy in this approximation. Their splitting (the **Lamb shift**, $\sim 4.4 \times 10^{-6}$ eV) requires QED radiative corrections. $\blacksquare$

</details>



---

## 📘 9. Appendix: Extended Derivations & Special Cases

### Appendix 9.1 — The Wigner-Eckart Theorem: Statement and Sketch Proof

The Wigner-Eckart theorem is one of the most powerful results in angular momentum theory. It states that the matrix elements of any irreducible tensor operator between angular momentum eigenstates are determined (up to a single reduced matrix element) by geometry alone.

**Statement:** Let $\hat{T}^{(k)}_q$ be a rank-$k$ irreducible spherical tensor operator (i.e., it transforms under rotations like $\vert k, q\rangle$). Then:

$$
\langle j', m'\vert\hat{T}^{(k)}_q\vert j, m\rangle = \langle j', m'\vert j, m; k, q\rangle\,\frac{\langle j'\|\hat{T}^{(k)}\|j\rangle}{\sqrt{2j'+1}},
$$

where:
- $\langle j', m'\vert j, m; k, q\rangle$ is a Clebsch-Gordan coefficient (purely geometric — depends only on the angular momentum quantum numbers).
- $\langle j'\|\hat{T}^{(k)}\|j\rangle$ is the **reduced matrix element** (contains all the dynamics — independent of $m, m', q$).

**Selection rules** follow immediately from the CG coefficient:
1. $m' = m + q$ (conservation of $z$-component).
2. $|j - k| \leq j' \leq j + k$ (triangle inequality).

**Sketch proof:**

*Step 1:* Define what it means for $\hat{T}^{(k)}_q$ to be an irreducible tensor operator:

$$
[\hat{J}_z, \hat{T}^{(k)}_q] = \hbar q\,\hat{T}^{(k)}_q, \qquad [\hat{J}_\pm, \hat{T}^{(k)}_q] = \hbar\sqrt{k(k+1) - q(q\pm 1)}\,\hat{T}^{(k)}_{q\pm 1}.
$$

*Step 2:* The state $\hat{T}^{(k)}_q\vert j, m\rangle$ transforms under rotations like the tensor product $\vert k, q\rangle \otimes \vert j, m\rangle$. By the addition theorem, this decomposes into irreducible representations with $j'$ ranging from $|j-k|$ to $j+k$.

*Step 3:* The overlap $\langle j', m'\vert\hat{T}^{(k)}_q\vert j, m\rangle$ is therefore proportional to the CG coefficient $\langle j, m; k, q\vert j', m'\rangle$, with a proportionality constant that cannot depend on $m, m', q$ (since the CG coefficient already accounts for all the $m$-dependence).

**Applications:**
- **Electric dipole selection rules:** $\hat{r}$ is a rank-1 tensor, so $\Delta l = \pm 1$, $\Delta m = 0, \pm 1$.
- **Magnetic moment:** $\langle j, m\vert\hat{\mu}_z\vert j, m\rangle = g_j m\mu_B$ follows from Wigner-Eckart applied to the rank-1 operator $\hat{\mu}$.
- **Quadrupole transitions:** rank-2 tensor, so $\Delta l = 0, \pm 2$.

**References:** Sakurai §3.11; Griffiths QM §6.5 (for the projection theorem corollary); Tong QM notes.

---

### Appendix 9.2 — Spin-Orbit Coupling from the Dirac Equation (Non-Relativistic Limit Preview)

The spin-orbit interaction $\hat{H}_{\text{SO}} \propto \hat{\mathbf{L}}\cdot\hat{\mathbf{S}}/r^3$ appears "magically" in non-relativistic quantum mechanics. Its true origin is the non-relativistic limit of the Dirac equation (covered fully in [9.6 - Relativistic QM - Klein-Gordon & Dirac Equations](9.6---Relativistic-QM---Klein-Gordon-&-Dirac-Equations)).

**The physical picture:** In the electron's rest frame, the nucleus orbits the electron, creating a magnetic field:

$$
\mathbf{B}_{\text{eff}} = -\frac{\mathbf{v} \times \mathbf{E}}{c^2} = \frac{1}{m_e c^2}\frac{1}{r}\frac{dV}{dr}\hat{\mathbf{L}}.
$$

The electron's magnetic moment $\boldsymbol{\mu} = -g_s\mu_B\hat{\mathbf{S}}/\hbar$ interacts with this field:

$$
\hat{H}_{\text{SO}} = -\boldsymbol{\mu}\cdot\mathbf{B}_{\text{eff}} = \frac{1}{2m_e^2 c^2}\frac{1}{r}\frac{dV}{dr}\hat{\mathbf{L}}\cdot\hat{\mathbf{S}}.
$$

(The factor of 1/2 is the Thomas precession correction — a relativistic kinematic effect.)

**From the Dirac equation:** The Foldy-Wouthuysen transformation (see [9.6 - Relativistic QM - Klein-Gordon & Dirac Equations](9.6---Relativistic-QM---Klein-Gordon-&-Dirac-Equations), Appendix) systematically extracts the non-relativistic limit of the Dirac equation to order $(v/c)^2$:

$$
\hat{H}_{\text{Pauli}} = mc^2 + \frac{\hat{p}^2}{2m} + V - \frac{\hat{p}^4}{8m^3c^2} + \frac{1}{2m^2c^2}\frac{1}{r}\frac{dV}{dr}\hat{\mathbf{L}}\cdot\hat{\mathbf{S}} + \frac{\hbar^2}{8m^2c^2}\nabla^2 V.
$$

The three correction terms are:
1. Relativistic kinetic energy correction ($-\hat{p}^4/8m^3c^2$).
2. Spin-orbit coupling (the $\hat{\mathbf{L}}\cdot\hat{\mathbf{S}}$ term).
3. Darwin term ($\propto \nabla^2 V$, non-zero only for $s$-states in hydrogen where $\psi(0) \neq 0$).

All three together give the fine-structure formula used in Example 8.4.

**References:** Sakurai §3.2, §7.4; Griffiths QM §6.3; Peskin & Schroeder §3.5.

