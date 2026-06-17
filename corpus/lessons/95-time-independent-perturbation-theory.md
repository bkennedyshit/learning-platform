---
title: "Time Independent Perturbation Theory"
subject: "Quantum Mechanics & Quantum Field Theory"
catalog: advanced
audience_tier: higher-education
chapter: "9.5"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 9.5 — Time-Independent Perturbation Theory

> *"The art of doing physics is the art of neglecting what is negligible and then correcting for it systematically."* — Richard Feynman

Most quantum systems cannot be solved exactly. Perturbation theory provides a systematic expansion in powers of a small parameter $\lambda$, building corrections to known solutions order by order. This chapter develops non-degenerate and degenerate perturbation theory, derives explicit formulas for energy and state corrections through second order, and applies them to real physical systems: the Stark effect, spin-orbit coupling, and anharmonic oscillators.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Set up the perturbation expansion $\hat{H} = \hat{H}_0 + \lambda\hat{H}'$ and identify the small parameter.
2. Derive first- and second-order energy corrections for non-degenerate states.
3. Derive the first-order state correction and interpret it physically.
4. Handle degenerate perturbation theory by diagonalizing $\hat{H}'$ within the degenerate subspace.
5. Apply perturbation theory to the anharmonic oscillator, Stark effect, and Zeeman effect.
6. State the variational principle and use it to bound ground-state energies.

---

## 🖼️ Visual Anchor — Perturbation Series Convergence

![math-09__9.5-fig1](math-09__9.5-fig1.svg)

---

## 📚 1. Definitions

### Definition 9.5.1 — Perturbation Expansion

The Hamiltonian is split as:

$$
\hat{H} = \hat{H}_0 + \lambda\hat{H}',
$$

where $\hat{H}_0$ is exactly solvable with known eigenstates $\vert n^{(0)}\rangle$ and eigenvalues $E_n^{(0)}$, and $\lambda\hat{H}'$ is a "small" perturbation ($\lambda \in [0,1]$ is a bookkeeping parameter).

### Definition 9.5.2 — Order-by-Order Expansion

We expand energies and states in powers of $\lambda$:

$$
E_n = E_n^{(0)} + \lambda E_n^{(1)} + \lambda^2 E_n^{(2)} + \cdots
$$

$$
\vert n\rangle = \vert n^{(0)}\rangle + \lambda\vert n^{(1)}\rangle + \lambda^2\vert n^{(2)}\rangle + \cdots
$$

### Definition 9.5.3 — Matrix Element of the Perturbation

$$
H'_{mn} = \langle m^{(0)}\vert\hat{H}'\vert n^{(0)}\rangle.
$$

### Definition 9.5.4 — Degenerate Subspace

A set of unperturbed states $\{\vert n_1^{(0)}\rangle, \ldots, \vert n_k^{(0)}\rangle\}$ sharing the same energy $E^{(0)}$ forms a **degenerate subspace**. Standard perturbation theory fails here because denominators $E_n^{(0)} - E_m^{(0)} = 0$.

### Definition 9.5.5 — Variational Principle

For any normalized trial state $\vert\tilde{\psi}\rangle$:

$$
E_{\text{gs}} \leq \langle\tilde{\psi}\vert\hat{H}\vert\tilde{\psi}\rangle.
$$

The ground-state energy is bounded above by the expectation value of $\hat{H}$ in any trial state.




---

## 📐 2. Axioms / Postulates

### Postulate 9.5.P1 — Analyticity of the Perturbation Series

We assume the eigenvalues and eigenstates are analytic functions of $\lambda$ in a neighborhood of $\lambda = 0$. This guarantees the Taylor expansion converges for sufficiently small $\lambda$.

### Postulate 9.5.P2 — Non-Degeneracy Condition

For non-degenerate perturbation theory, we require $E_n^{(0)} \neq E_m^{(0)}$ for all $m \neq n$. When this fails, we must use degenerate perturbation theory.

### Postulate 9.5.P3 — Intermediate Normalization

We adopt the convention $\langle n^{(0)}\vert n\rangle = 1$ (not $\langle n\vert n\rangle = 1$). This simplifies the algebra and implies $\langle n^{(0)}\vert n^{(k)}\rangle = 0$ for $k \geq 1$.

---

## 🛡️ 3. Lemmas

### Lemma 9.5.1 — First-Order Energy Correction

$$
E_n^{(1)} = \langle n^{(0)}\vert\hat{H}'\vert n^{(0)}\rangle = H'_{nn}.
$$

**Proof.** The eigenvalue equation at order $\lambda^1$:

$$
\hat{H}_0\vert n^{(1)}\rangle + \hat{H}'\vert n^{(0)}\rangle = E_n^{(0)}\vert n^{(1)}\rangle + E_n^{(1)}\vert n^{(0)}\rangle.
$$

Project onto $\langle n^{(0)}\vert$:

$$
\langle n^{(0)}\vert\hat{H}_0\vert n^{(1)}\rangle + \langle n^{(0)}\vert\hat{H}'\vert n^{(0)}\rangle = E_n^{(0)}\langle n^{(0)}\vert n^{(1)}\rangle + E_n^{(1)}.
$$

Since $\hat{H}_0$ is Hermitian: $\langle n^{(0)}\vert\hat{H}_0 = E_n^{(0)}\langle n^{(0)}\vert$. The first and third terms cancel (using intermediate normalization $\langle n^{(0)}\vert n^{(1)}\rangle = 0$):

$$
E_n^{(1)} = \langle n^{(0)}\vert\hat{H}'\vert n^{(0)}\rangle. \quad \blacksquare
$$

### Lemma 9.5.2 — First-Order State Correction

$$
\vert n^{(1)}\rangle = \sum_{m \neq n}\frac{\langle m^{(0)}\vert\hat{H}'\vert n^{(0)}\rangle}{E_n^{(0)} - E_m^{(0)}}\vert m^{(0)}\rangle = \sum_{m \neq n}\frac{H'_{mn}}{E_n^{(0)} - E_m^{(0)}}\vert m^{(0)}\rangle.
$$

**Proof.** From the first-order equation, project onto $\langle m^{(0)}\vert$ with $m \neq n$:

$$
E_m^{(0)}\langle m^{(0)}\vert n^{(1)}\rangle + H'_{mn} = E_n^{(0)}\langle m^{(0)}\vert n^{(1)}\rangle.
$$

$$
\langle m^{(0)}\vert n^{(1)}\rangle = \frac{H'_{mn}}{E_n^{(0)} - E_m^{(0)}}. \quad \blacksquare
$$

### Lemma 9.5.3 — Second-Order Energy Correction

$$
E_n^{(2)} = \sum_{m \neq n}\frac{|H'_{mn}|^2}{E_n^{(0)} - E_m^{(0)}}.
$$

**Proof.** The second-order eigenvalue equation projected onto $\langle n^{(0)}\vert$:

$$
E_n^{(2)} = \langle n^{(0)}\vert\hat{H}'\vert n^{(1)}\rangle.
$$

Substitute the expression for $\vert n^{(1)}\rangle$:

$$
= \sum_{m \neq n}\frac{H'_{mn}}{E_n^{(0)} - E_m^{(0)}}\langle n^{(0)}\vert\hat{H}'\vert m^{(0)}\rangle = \sum_{m \neq n}\frac{H'_{nm}H'_{mn}}{E_n^{(0)} - E_m^{(0)}} = \sum_{m \neq n}\frac{|H'_{mn}|^2}{E_n^{(0)} - E_m^{(0)}}.
$$

(Using $H'_{nm} = (H'_{mn})^*$ since $\hat{H}'$ is Hermitian.) $\blacksquare$

**Key observation:** The second-order correction always **lowers** the ground-state energy (all denominators are negative for $n = 0$, $m > 0$).

### Lemma 9.5.4 — Degenerate Perturbation Theory Recipe

When states $\vert n_1^{(0)}\rangle, \ldots, \vert n_k^{(0)}\rangle$ are degenerate with energy $E^{(0)}$:

1. Construct the $k \times k$ matrix $W_{ij} = \langle n_i^{(0)}\vert\hat{H}'\vert n_j^{(0)}\rangle$.
2. Diagonalize $W$: eigenvalues are the first-order corrections $E^{(1)}_\alpha$.
3. The "good" zeroth-order states are the eigenvectors of $W$.




---

## 👑 4. Theorems

### Theorem 9.5.1 — Non-Degenerate Perturbation Theory (Complete to Second Order)

For a non-degenerate state $\vert n^{(0)}\rangle$:

$$
E_n = E_n^{(0)} + H'_{nn} + \sum_{m \neq n}\frac{|H'_{mn}|^2}{E_n^{(0)} - E_m^{(0)}} + O(\lambda^3).
$$

$$
\vert n\rangle = \vert n^{(0)}\rangle + \sum_{m \neq n}\frac{H'_{mn}}{E_n^{(0)} - E_m^{(0)}}\vert m^{(0)}\rangle + O(\lambda^2).
$$

### Theorem 9.5.2 — Variational Theorem

For any normalized $\vert\tilde{\psi}\rangle$: $\langle\tilde{\psi}\vert\hat{H}\vert\tilde{\psi}\rangle \geq E_0$ (the true ground-state energy). Equality holds iff $\vert\tilde{\psi}\rangle$ is the exact ground state.

### Theorem 9.5.3 — Level Repulsion (No-Crossing Rule)

In non-degenerate perturbation theory, the second-order correction pushes energy levels apart: the ground state is pushed down, excited states are pushed up by nearby levels. Levels of the same symmetry cannot cross as a parameter is varied (von Neumann-Wigner theorem).

---

## ✍️ 5. Proofs / Derivations

### 5.1 Full Derivation of Non-Degenerate Perturbation Theory

**Setup:** $\hat{H}\vert n\rangle = E_n\vert n\rangle$ with $\hat{H} = \hat{H}_0 + \lambda\hat{H}'$.

**Step 1:** Expand: $E_n = \sum_k \lambda^k E_n^{(k)}$, $\vert n\rangle = \sum_k \lambda^k\vert n^{(k)}\rangle$.

**Step 2:** Substitute into $\hat{H}\vert n\rangle = E_n\vert n\rangle$ and collect powers of $\lambda$:

**Order $\lambda^0$:** $\hat{H}_0\vert n^{(0)}\rangle = E_n^{(0)}\vert n^{(0)}\rangle$. (Satisfied by assumption.)

**Order $\lambda^1$:**

$$
\hat{H}_0\vert n^{(1)}\rangle + \hat{H}'\vert n^{(0)}\rangle = E_n^{(0)}\vert n^{(1)}\rangle + E_n^{(1)}\vert n^{(0)}\rangle. \tag{1}
$$

**Order $\lambda^2$:**

$$
\hat{H}_0\vert n^{(2)}\rangle + \hat{H}'\vert n^{(1)}\rangle = E_n^{(0)}\vert n^{(2)}\rangle + E_n^{(1)}\vert n^{(1)}\rangle + E_n^{(2)}\vert n^{(0)}\rangle. \tag{2}
$$

**Step 3:** Project (1) onto $\langle n^{(0)}\vert$: gives $E_n^{(1)} = H'_{nn}$ (Lemma 9.5.1).

**Step 4:** Project (1) onto $\langle m^{(0)}\vert$ ($m \neq n$): gives $\vert n^{(1)}\rangle$ (Lemma 9.5.2).

**Step 5:** Project (2) onto $\langle n^{(0)}\vert$:

$$
\underbrace{\langle n^{(0)}\vert\hat{H}_0\vert n^{(2)}\rangle}_{E_n^{(0)}\langle n^{(0)}\vert n^{(2)}\rangle} + \langle n^{(0)}\vert\hat{H}'\vert n^{(1)}\rangle = \underbrace{E_n^{(0)}\langle n^{(0)}\vert n^{(2)}\rangle}_{\text{cancels}} + E_n^{(1)}\underbrace{\langle n^{(0)}\vert n^{(1)}\rangle}_{0} + E_n^{(2)}.
$$

Therefore: $E_n^{(2)} = \langle n^{(0)}\vert\hat{H}'\vert n^{(1)}\rangle = \sum_{m\neq n}\frac{|H'_{mn}|^2}{E_n^{(0)} - E_m^{(0)}}$. $\blacksquare$

### 5.2 Anharmonic Oscillator: First-Order Correction to $\hat{H}' = \lambda x^4$

**Problem:** $\hat{H}_0 = \hbar\omega(\hat{a}^\dagger\hat{a} + 1/2)$, $\hat{H}' = \lambda\hat{x}^4$. Find $E_n^{(1)}$.

**Step 1:** Express $\hat{x}^4$ in terms of ladder operators. With $\hat{x} = \sqrt{\frac{\hbar}{2m\omega}}(\hat{a} + \hat{a}^\dagger)$:

$$
\hat{x}^4 = \left(\frac{\hbar}{2m\omega}\right)^2(\hat{a} + \hat{a}^\dagger)^4.
$$

**Step 2:** Expand $(\hat{a} + \hat{a}^\dagger)^4$. We need $\langle n\vert(\hat{a} + \hat{a}^\dagger)^4\vert n\rangle$.

Using the normal-ordering technique or direct computation:

$$
(\hat{a} + \hat{a}^\dagger)^2 = \hat{a}^2 + \hat{a}\hat{a}^\dagger + \hat{a}^\dagger\hat{a} + (\hat{a}^\dagger)^2 = \hat{a}^2 + (2\hat{N}+1) + (\hat{a}^\dagger)^2.
$$

$$
(\hat{a} + \hat{a}^\dagger)^4 = [(\hat{a} + \hat{a}^\dagger)^2]^2.
$$

The diagonal matrix element $\langle n\vert(\hat{a}+\hat{a}^\dagger)^4\vert n\rangle$ only gets contributions from terms with equal numbers of $\hat{a}$ and $\hat{a}^\dagger$. These are:

$$
\hat{a}^2(\hat{a}^\dagger)^2 + \hat{a}\hat{a}^\dagger\hat{a}\hat{a}^\dagger + \hat{a}\hat{a}^\dagger(\hat{a}^\dagger)\hat{a} + \hat{a}^\dagger\hat{a}\hat{a}\hat{a}^\dagger + \hat{a}^\dagger\hat{a}\hat{a}^\dagger\hat{a} + (\hat{a}^\dagger)^2\hat{a}^2.
$$

After careful evaluation using $\hat{a}\vert n\rangle = \sqrt{n}\vert n-1\rangle$:

$$
\langle n\vert(\hat{a}+\hat{a}^\dagger)^4\vert n\rangle = 6n^2 + 6n + 3.
$$

**Step 3:** Therefore:

$$
E_n^{(1)} = \lambda\left(\frac{\hbar}{2m\omega}\right)^2(6n^2 + 6n + 3) = \frac{3\lambda\hbar^2}{4m^2\omega^2}(2n^2 + 2n + 1).
$$

For the ground state ($n = 0$): $E_0^{(1)} = \frac{3\lambda\hbar^2}{4m^2\omega^2}$.

### 5.3 Proof of the Variational Theorem

**Step 1:** Expand the trial state in the exact eigenbasis: $\vert\tilde{\psi}\rangle = \sum_n c_n\vert n\rangle$ with $\sum_n|c_n|^2 = 1$.

**Step 2:** Compute the expectation value:

$$
\langle\tilde{\psi}\vert\hat{H}\vert\tilde{\psi}\rangle = \sum_n |c_n|^2 E_n.
$$

**Step 3:** Since $E_n \geq E_0$ for all $n$:

$$
\sum_n |c_n|^2 E_n \geq \sum_n |c_n|^2 E_0 = E_0\sum_n|c_n|^2 = E_0. \quad \blacksquare
$$

### 5.4 Degenerate Perturbation Theory: The 2D Harmonic Oscillator

**Problem:** $\hat{H}_0$ has a 2-fold degenerate first excited level: $\vert 1,0\rangle$ and $\vert 0,1\rangle$ both have $E^{(0)} = 2\hbar\omega$. Add perturbation $\hat{H}' = \lambda m\omega^2 xy$.

**Step 1:** Construct the $W$ matrix:

$$
W = \begin{pmatrix} \langle 1,0\vert\hat{H}'\vert 1,0\rangle & \langle 1,0\vert\hat{H}'\vert 0,1\rangle \\ \langle 0,1\vert\hat{H}'\vert 1,0\rangle & \langle 0,1\vert\hat{H}'\vert 0,1\rangle \end{pmatrix}.
$$

**Step 2:** Using $\hat{x} = \sqrt{\frac{\hbar}{2m\omega}}(\hat{a}_x + \hat{a}_x^\dagger)$ and similarly for $\hat{y}$:

$$
\hat{x}\hat{y} = \frac{\hbar}{2m\omega}(\hat{a}_x + \hat{a}_x^\dagger)(\hat{a}_y + \hat{a}_y^\dagger).
$$

The diagonal elements vanish: $\langle 1,0\vert\hat{x}\hat{y}\vert 1,0\rangle = 0$ (parity argument).

The off-diagonal: $\langle 1,0\vert\hat{x}\hat{y}\vert 0,1\rangle = \frac{\hbar}{2m\omega}\langle 1,0\vert\hat{a}_x^\dagger\hat{a}_y\vert 0,1\rangle = \frac{\hbar}{2m\omega}\cdot 1 = \frac{\hbar}{2m\omega}$.

**Step 3:** $W = \frac{\lambda\hbar\omega}{2}\begin{pmatrix}0&1\\1&0\end{pmatrix}$.

Eigenvalues: $E^{(1)} = \pm\frac{\lambda\hbar\omega}{2}$.

The degeneracy is **lifted** by the perturbation. The "good" states are $\frac{1}{\sqrt{2}}(\vert 1,0\rangle \pm \vert 0,1\rangle)$.




---

## 🧮 6. Worked Examples

### Example 9.5.1 — Ground-State Energy of Helium (Variational Method)

**Problem:** Estimate the ground-state energy of helium using the trial wave function $\psi(\mathbf{r}_1, \mathbf{r}_2) = \frac{Z_{\text{eff}}^3}{\pi a_0^3}e^{-Z_{\text{eff}}(r_1+r_2)/a_0}$ with $Z_{\text{eff}}$ as variational parameter.

**Solution:**

**Step 1:** The Hamiltonian: $\hat{H} = -\frac{\hbar^2}{2m}(\nabla_1^2 + \nabla_2^2) - \frac{2e^2}{r_1} - \frac{2e^2}{r_2} + \frac{e^2}{|\mathbf{r}_1 - \mathbf{r}_2|}$.

**Step 2:** With the hydrogen-like trial function (effective charge $Z_{\text{eff}}$):

$$
\langle\hat{H}\rangle = 2\left[\frac{Z_{\text{eff}}^2}{2} - 2Z_{\text{eff}}\right]\cdot\frac{e^2}{a_0} + \frac{5Z_{\text{eff}}}{8}\cdot\frac{e^2}{a_0}.
$$

(In Rydberg units with $e^2/a_0 = 27.2$ eV.)

$$
= \left(Z_{\text{eff}}^2 - 4Z_{\text{eff}} + \frac{5Z_{\text{eff}}}{8}\right)\cdot 27.2 \text{ eV} = \left(Z_{\text{eff}}^2 - \frac{27Z_{\text{eff}}}{8}\right)\cdot 27.2 \text{ eV}.
$$

**Step 3:** Minimize: $\frac{d}{dZ_{\text{eff}}}(Z_{\text{eff}}^2 - 27Z_{\text{eff}}/8) = 2Z_{\text{eff}} - 27/8 = 0$, giving $Z_{\text{eff}} = 27/16 = 1.6875$.

**Step 4:** Substitute back:

$$
E_{\min} = \left(\frac{27^2}{16^2} - \frac{27^2}{8\cdot16}\right)\cdot 27.2 = -\frac{27^2}{2\cdot16^2}\cdot 27.2 = -\frac{729}{512}\cdot 27.2 = -77.5 \text{ eV}.
$$

Experimental value: $-78.98$ eV. The variational estimate is within 2%!

---

### Example 9.5.2 — Linear Stark Effect in Hydrogen ($n = 2$)

**Problem:** Apply an electric field $\mathcal{E}$ along $z$ to hydrogen. Find the first-order energy splitting of the $n = 2$ level.

**Solution:**

**Step 1:** The perturbation is $\hat{H}' = e\mathcal{E}z = e\mathcal{E}r\cos\theta$.

**Step 2:** The $n = 2$ level is 4-fold degenerate: $\vert 2,0,0\rangle$, $\vert 2,1,0\rangle$, $\vert 2,1,1\rangle$, $\vert 2,1,-1\rangle$.

**Step 3:** Selection rules: $\hat{H}' \propto r\cos\theta \propto rY_1^0$. Matrix elements are non-zero only if $\Delta\ell = \pm 1$ and $\Delta m = 0$.

The only non-zero matrix element is:

$$
W_{12} = \langle 2,0,0\vert e\mathcal{E}r\cos\theta\vert 2,1,0\rangle = -3e\mathcal{E}a_0.
$$

**Step 4:** The $W$ matrix in the $\{\vert 2,0,0\rangle, \vert 2,1,0\rangle\}$ subspace:

$$
W = \begin{pmatrix}0 & -3e\mathcal{E}a_0 \\ -3e\mathcal{E}a_0 & 0\end{pmatrix}.
$$

Eigenvalues: $E^{(1)} = \pm 3e\mathcal{E}a_0$.

**Step 5:** The states $\vert 2,1,\pm1\rangle$ are unaffected at first order (their matrix elements vanish).

The $n = 2$ level splits into three: $E_2 + 3e\mathcal{E}a_0$, $E_2$, $E_2 - 3e\mathcal{E}a_0$.

---

### Example 9.5.3 — Second-Order Correction for the Ground State with $\hat{H}' = \lambda\hat{x}^2$ Perturbation on the Oscillator

**Problem:** For $\hat{H}_0 = \hbar\omega(\hat{N}+1/2)$ and $\hat{H}' = \frac{1}{2}m\epsilon\omega^2\hat{x}^2$ (a small frequency shift), compute $E_0^{(2)}$.

**Solution:**

**Step 1:** This is actually exactly solvable: $\hat{H} = \frac{1}{2}m\omega^2(1+\epsilon)\hat{x}^2 + \frac{\hat{p}^2}{2m}$, so $\omega' = \omega\sqrt{1+\epsilon} \approx \omega(1+\epsilon/2)$ and $E_0 = \frac{1}{2}\hbar\omega' \approx \frac{1}{2}\hbar\omega(1+\epsilon/2)$.

**Step 2:** Via perturbation theory: $\hat{H}' = \frac{\epsilon}{2}m\omega^2\hat{x}^2 = \frac{\epsilon\hbar\omega}{4}(\hat{a}+\hat{a}^\dagger)^2$.

First order: $E_0^{(1)} = \frac{\epsilon\hbar\omega}{4}\langle 0\vert(\hat{a}+\hat{a}^\dagger)^2\vert 0\rangle = \frac{\epsilon\hbar\omega}{4}\cdot 1 = \frac{\epsilon\hbar\omega}{4}$.

**Step 3:** Second order: need $\langle m\vert\hat{H}'\vert 0\rangle$ for $m \neq 0$.

$(\hat{a}+\hat{a}^\dagger)^2\vert 0\rangle = (\hat{a}^2 + \hat{a}\hat{a}^\dagger + \hat{a}^\dagger\hat{a} + (\hat{a}^\dagger)^2)\vert 0\rangle = 0 + \vert 0\rangle + 0 + \sqrt{2}\vert 2\rangle$.

So $H'_{20} = \frac{\epsilon\hbar\omega}{4}\sqrt{2}$ and all other $H'_{m0} = 0$ for $m \neq 0, 2$.

$$
E_0^{(2)} = \frac{|H'_{20}|^2}{E_0^{(0)} - E_2^{(0)}} = \frac{(\epsilon\hbar\omega/4)^2\cdot 2}{\frac{1}{2}\hbar\omega - \frac{5}{2}\hbar\omega} = \frac{\epsilon^2\hbar^2\omega^2/8}{-2\hbar\omega} = -\frac{\epsilon^2\hbar\omega}{16}.
$$

**Step 4:** Total: $E_0 \approx \frac{\hbar\omega}{2} + \frac{\epsilon\hbar\omega}{4} - \frac{\epsilon^2\hbar\omega}{16} = \frac{\hbar\omega}{2}(1 + \epsilon/2 - \epsilon^2/8)$.

Compare exact: $\frac{\hbar\omega}{2}\sqrt{1+\epsilon} \approx \frac{\hbar\omega}{2}(1 + \epsilon/2 - \epsilon^2/8)$. ✓ Perfect agreement!

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- [2.6 - Eigenvalues Eigenvectors & Diagonalization](2.6---Eigenvalues-Eigenvectors-&-Diagonalization) — Degenerate PT requires diagonalizing $W$ in the degenerate subspace
- [9.3 - The 1D Infinite Square Well & Harmonic Oscillator](9.3---The-1D-Infinite-Square-Well-&-Harmonic-Oscillator) — Unperturbed systems used as $\hat{H}_0$
- [9.4 - Angular Momentum, Spin & Fine Structure](9.4---Angular-Momentum,-Spin-&-Fine-Structure) — Fine structure derived via PT
- [9.6 - Relativistic QM - Klein-Gordon & Dirac Equations](9.6---Relativistic-QM---Klein-Gordon-&-Dirac-Equations) — Relativistic corrections as perturbations

### External References
- **Griffiths, D.J.** *Introduction to Quantum Mechanics* — Chapter 7 (perturbation theory).
- **Sakurai, J.J.** *Modern Quantum Mechanics* — Chapter 5 (approximation methods).
- **Susskind, L.** *Quantum Mechanics: The Theoretical Minimum* — Perturbation theory lectures.

---

*Next: [9.6 - Relativistic QM - Klein-Gordon & Dirac Equations](9.6---Relativistic-QM---Klein-Gordon-&-Dirac-Equations) — When particles move near the speed of light.*




---

## ✍️ Additional Derivations

### 5.5 Complete Second-Order Calculation: Ground State of Quartic Oscillator

**Problem:** For $\hat{H} = \hbar\omega(\hat{N}+1/2) + \lambda\hat{x}^4$, compute $E_0$ through second order.

**Step 1:** First order (from Section 5.2): $E_0^{(1)} = \frac{3\lambda\hbar^2}{4m^2\omega^2}$.

**Step 2:** For second order, need $\langle m\vert\hat{x}^4\vert 0\rangle$ for $m \neq 0$.

From the expansion $\hat{x}^4\vert 0\rangle = \left(\frac{\hbar}{2m\omega}\right)^2(\hat{a}+\hat{a}^\dagger)^4\vert 0\rangle$:

The non-zero components are:
- $\vert 0\rangle$ component: coefficient 3 (already used for $E^{(1)}$)
- $\vert 2\rangle$ component: $(\hat{a}+\hat{a}^\dagger)^4\vert 0\rangle$ has $\vert 2\rangle$ coefficient $= 6\sqrt{2}$... 

Let me compute carefully. $(\hat{a}+\hat{a}^\dagger)^4\vert 0\rangle$:

First: $(\hat{a}+\hat{a}^\dagger)\vert 0\rangle = \vert 1\rangle$.

Second: $(\hat{a}+\hat{a}^\dagger)\vert 1\rangle = \vert 0\rangle + \sqrt{2}\vert 2\rangle$.

Third: $(\hat{a}+\hat{a}^\dagger)(\vert 0\rangle + \sqrt{2}\vert 2\rangle) = \vert 1\rangle + \sqrt{2}(\sqrt{2}\vert 1\rangle + \sqrt{3}\vert 3\rangle) = 3\vert 1\rangle + \sqrt{6}\vert 3\rangle$.

Fourth: $(\hat{a}+\hat{a}^\dagger)(3\vert 1\rangle + \sqrt{6}\vert 3\rangle) = 3(\vert 0\rangle + \sqrt{2}\vert 2\rangle) + \sqrt{6}(\sqrt{3}\vert 2\rangle + 2\vert 4\rangle)$.

$$
= 3\vert 0\rangle + (3\sqrt{2} + \sqrt{18})\vert 2\rangle + 2\sqrt{6}\vert 4\rangle = 3\vert 0\rangle + 6\sqrt{2}\vert 2\rangle + 2\sqrt{6}\vert 4\rangle.
$$

**Step 3:** Therefore:

$$
H'_{20} = \lambda\left(\frac{\hbar}{2m\omega}\right)^2 \cdot 6\sqrt{2}, \quad H'_{40} = \lambda\left(\frac{\hbar}{2m\omega}\right)^2 \cdot 2\sqrt{6}.
$$

**Step 4:** Second-order correction:

$$
E_0^{(2)} = \frac{|H'_{20}|^2}{E_0^{(0)}-E_2^{(0)}} + \frac{|H'_{40}|^2}{E_0^{(0)}-E_4^{(0)}}.
$$

$$
= \frac{\lambda^2(\hbar/2m\omega)^4 \cdot 72}{-2\hbar\omega} + \frac{\lambda^2(\hbar/2m\omega)^4 \cdot 24}{-4\hbar\omega}.
$$

$$
= -\lambda^2\frac{\hbar^4}{16m^4\omega^4}\left(\frac{72}{2\hbar\omega} + \frac{24}{4\hbar\omega}\right) = -\lambda^2\frac{\hbar^3}{16m^4\omega^5}(36 + 6) = -\frac{42\lambda^2\hbar^3}{16m^4\omega^5} = -\frac{21\lambda^2\hbar^3}{8m^4\omega^5}.
$$

**Step 5:** Total energy through second order:

$$
E_0 = \frac{\hbar\omega}{2} + \frac{3\lambda\hbar^2}{4m^2\omega^2} - \frac{21\lambda^2\hbar^3}{8m^4\omega^5} + O(\lambda^3).
$$

The negative second-order correction confirms the variational principle: perturbation theory systematically lowers the energy estimate. $\blacksquare$

### 5.6 The Quadratic Stark Effect (Ground State of Hydrogen)

**Problem:** Compute the second-order energy shift of the hydrogen ground state in an electric field $\mathcal{E}$.

**Step 1:** The perturbation is $\hat{H}' = e\mathcal{E}z = e\mathcal{E}r\cos\theta$. The ground state $\vert 1,0,0\rangle$ is non-degenerate.

**Step 2:** First order: $E_1^{(1)} = \langle 1,0,0\vert e\mathcal{E}r\cos\theta\vert 1,0,0\rangle = 0$ (parity: the integrand is odd under $\theta \to \pi - \theta$).

**Step 3:** Second order:

$$
E_1^{(2)} = \sum_{n\ell m \neq 100}\frac{|\langle n,\ell,m\vert e\mathcal{E}r\cos\theta\vert 1,0,0\rangle|^2}{E_1 - E_n}.
$$

Selection rules ($r\cos\theta \propto rY_1^0$): $\Delta\ell = \pm 1$, $\Delta m = 0$. So only $\ell = 1$, $m = 0$ states contribute.

**Step 4:** The dominant contribution comes from $n = 2$:

$$
\langle 2,1,0\vert r\cos\theta\vert 1,0,0\rangle = -\frac{2^7}{3^5}\sqrt{2}\,a_0 \approx -0.745\,a_0.
$$

**Step 5:** The exact result (summing over all $n$ including continuum):

$$
E_1^{(2)} = -\frac{9}{4}a_0^3\mathcal{E}^2 = -\frac{1}{2}\alpha_d\mathcal{E}^2,
$$

where $\alpha_d = \frac{9}{2}a_0^3$ is the static polarizability of hydrogen. The energy shift is quadratic in $\mathcal{E}$ — hence "quadratic Stark effect." $\blacksquare$




---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — First-Order Perturbation: Anharmonic Oscillator $V_1 = \lambda x^4$

**Problem:** The harmonic oscillator Hamiltonian $\hat{H}_0 = \hbar\omega(\hat{a}^\dagger\hat{a} + 1/2)$ is perturbed by $\hat{H}' = \lambda\hat{x}^4$. Compute the first-order energy correction to the ground state.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Express $\hat{x}^4$ in Terms of Ladder Operators

$$
\hat{x} = \sqrt{\frac{\hbar}{2m\omega}}(\hat{a} + \hat{a}^\dagger) \equiv x_0(\hat{a} + \hat{a}^\dagger),
$$

where $x_0 = \sqrt{\hbar/(2m\omega)}$.

$$
\hat{x}^4 = x_0^4(\hat{a} + \hat{a}^\dagger)^4.
$$

#### Step 2: Expand $(\hat{a} + \hat{a}^\dagger)^4$

We need $\langle 0\vert(\hat{a} + \hat{a}^\dagger)^4\vert 0\rangle$. Use the fact that $\hat{a}\vert 0\rangle = 0$ and $\langle 0\vert\hat{a}^\dagger = 0$.

Only terms with equal numbers of $\hat{a}$ and $\hat{a}^\dagger$ survive (to return to $\vert 0\rangle$). The non-zero pairings from $(\hat{a} + \hat{a}^\dagger)^4$ are those with exactly 2 $\hat{a}$'s and 2 $\hat{a}^\dagger$'s.

Enumerate all orderings of $\hat{a}\hat{a}\hat{a}^\dagger\hat{a}^\dagger$ that give non-zero $\langle 0\vert\cdots\vert 0\rangle$:

The six distinct orderings of 2 $a$'s and 2 $a^\dagger$'s from the 4th power are found by choosing which 2 of the 4 positions are $\hat{a}^\dagger$: $\binom{4}{2} = 6$ terms.

But it's easier to compute directly. Write $\hat{A} = \hat{a} + \hat{a}^\dagger$:

$$
\hat{A}^2 = \hat{a}^2 + \hat{a}\hat{a}^\dagger + \hat{a}^\dagger\hat{a} + (\hat{a}^\dagger)^2 = \hat{a}^2 + (2\hat{N} + 1) + (\hat{a}^\dagger)^2.
$$

$$
\hat{A}^4 = (\hat{A}^2)^2.
$$

#### Step 3: Compute $\langle 0\vert\hat{A}^4\vert 0\rangle$ Directly

Method: compute $\hat{A}^2\vert 0\rangle$ first.

$$
\hat{A}\vert 0\rangle = (\hat{a} + \hat{a}^\dagger)\vert 0\rangle = 0 + \vert 1\rangle = \vert 1\rangle.
$$

$$
\hat{A}^2\vert 0\rangle = \hat{A}\vert 1\rangle = (\hat{a} + \hat{a}^\dagger)\vert 1\rangle = \sqrt{1}\vert 0\rangle + \sqrt{2}\vert 2\rangle = \vert 0\rangle + \sqrt{2}\vert 2\rangle.
$$

$$
\hat{A}^3\vert 0\rangle = \hat{A}(\vert 0\rangle + \sqrt{2}\vert 2\rangle) = \vert 1\rangle + \sqrt{2}(\sqrt{2}\vert 1\rangle + \sqrt{3}\vert 3\rangle) = 3\vert 1\rangle + \sqrt{6}\vert 3\rangle.
$$

$$
\hat{A}^4\vert 0\rangle = \hat{A}(3\vert 1\rangle + \sqrt{6}\vert 3\rangle) = 3(\vert 0\rangle + \sqrt{2}\vert 2\rangle) + \sqrt{6}(\sqrt{3}\vert 2\rangle + 2\vert 4\rangle).
$$

$$
= 3\vert 0\rangle + 3\sqrt{2}\vert 2\rangle + \sqrt{18}\vert 2\rangle + 2\sqrt{6}\vert 4\rangle = 3\vert 0\rangle + (3\sqrt{2} + 3\sqrt{2})\vert 2\rangle + 2\sqrt{6}\vert 4\rangle.
$$

$$
= 3\vert 0\rangle + 6\sqrt{2}\vert 2\rangle + 2\sqrt{6}\vert 4\rangle.
$$

Wait — let me recompute: $\sqrt{6}\cdot\sqrt{3} = \sqrt{18} = 3\sqrt{2}$. So:

$$
\hat{A}^4\vert 0\rangle = 3\vert 0\rangle + (3\sqrt{2} + 3\sqrt{2})\vert 2\rangle + 2\sqrt{6}\vert 4\rangle = 3\vert 0\rangle + 6\sqrt{2}\vert 2\rangle + 2\sqrt{6}\vert 4\rangle.
$$

Hmm, let me recheck: $3\sqrt{2} + \sqrt{18} = 3\sqrt{2} + 3\sqrt{2} = 6\sqrt{2}$. ✓

#### Step 4: Extract the Ground-State Expectation Value

$$
\langle 0\vert\hat{A}^4\vert 0\rangle = 3\langle 0\vert 0\rangle + 6\sqrt{2}\langle 0\vert 2\rangle + 2\sqrt{6}\langle 0\vert 4\rangle = 3.
$$

#### Step 5: First-Order Energy Correction

$$
E_0^{(1)} = \langle 0\vert\hat{H}'\vert 0\rangle = \lambda x_0^4\langle 0\vert\hat{A}^4\vert 0\rangle = \lambda\left(\frac{\hbar}{2m\omega}\right)^2\cdot 3 = \frac{3\lambda\hbar^2}{4m^2\omega^2}.
$$

$$
\boxed{E_0^{(1)} = \frac{3\lambda\hbar^2}{4m^2\omega^2}.}
$$

**Physical check:** The correction is positive (the $x^4$ term raises the potential everywhere), and scales as $\lambda\hbar^2/(m\omega)^2$ — the natural energy scale times the perturbation strength. $\blacksquare$

</details>

### Example 8.2 — Degenerate Perturbation Theory: Two-State System

**Problem:** A two-level system has unperturbed Hamiltonian $\hat{H}_0$ with degenerate eigenvalue $E^{(0)}$ and eigenstates $\vert 1\rangle, \vert 2\rangle$. The perturbation matrix in this subspace is:

$$
W = \begin{pmatrix} W_{11} & W_{12} \\ W_{21} & W_{22} \end{pmatrix}, \quad W_{ij} = \langle i\vert\hat{H}'\vert j\rangle.
$$

Find the first-order energy corrections and the "good" zeroth-order states.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: The Secular Equation

In degenerate perturbation theory, we must diagonalize $W$ within the degenerate subspace. The first-order corrections are eigenvalues of $W$:

$$
\det(W - E^{(1)}I) = 0.
$$

$$
\det\begin{pmatrix} W_{11} - E^{(1)} & W_{12} \\ W_{21} & W_{22} - E^{(1)} \end{pmatrix} = 0.
$$

$$
(W_{11} - E^{(1)})(W_{22} - E^{(1)}) - W_{12}W_{21} = 0.
$$

#### Step 2: Solve the Quadratic

$$
(E^{(1)})^2 - (W_{11} + W_{22})E^{(1)} + (W_{11}W_{22} - |W_{12}|^2) = 0.
$$

(Using $W_{21} = W_{12}^*$ for Hermitian $\hat{H}'$.)

$$
E^{(1)}_\pm = \frac{(W_{11} + W_{22})}{2} \pm \sqrt{\left(\frac{W_{11} - W_{22}}{2}\right)^2 + |W_{12}|^2}.
$$

#### Step 3: The "Good" States

The eigenvectors of $W$ are the correct zeroth-order states:

$$
\vert\pm\rangle = \cos\theta\,\vert 1\rangle + e^{i\phi}\sin\theta\,\vert 2\rangle,
$$

where $\tan(2\theta) = \frac{2|W_{12}|}{W_{11} - W_{22}}$ and $\phi = \arg(W_{12})$.

#### Step 4: Special Case — Equal Diagonal Elements ($W_{11} = W_{22} \equiv W_d$)

$$
E^{(1)}_\pm = W_d \pm |W_{12}|.
$$

The good states are $\vert\pm\rangle = \frac{1}{\sqrt{2}}(\vert 1\rangle \pm e^{i\phi}\vert 2\rangle)$.

The degeneracy is lifted by $2|W_{12}|$ — the off-diagonal coupling splits the levels symmetrically.

#### Step 5: Physical Example — Ammonia Molecule

The NH₃ molecule has two degenerate configurations (nitrogen above/below the H₃ plane). The tunneling matrix element $W_{12}$ splits these into symmetric and antisymmetric states separated by $\sim 24$ GHz — the basis of the ammonia maser. $\blacksquare$

</details>



### Example 8.3 — Second-Order Ground-State Energy Shift for the Anharmonic Oscillator

**Problem:** For the same perturbation $\hat{H}' = \lambda x^4$ on the harmonic oscillator, compute the second-order correction $E_0^{(2)}$ to the ground-state energy.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: The Second-Order Formula

$$
E_0^{(2)} = \sum_{n \neq 0}\frac{|\langle n\vert\hat{H}'\vert 0\rangle|^2}{E_0^{(0)} - E_n^{(0)}} = \sum_{n \neq 0}\frac{|\langle n\vert\lambda x_0^4\hat{A}^4\vert 0\rangle|^2}{\frac{1}{2}\hbar\omega - (n + \frac{1}{2})\hbar\omega}.
$$

$$
= -\frac{\lambda^2 x_0^8}{\hbar\omega}\sum_{n \neq 0}\frac{|\langle n\vert\hat{A}^4\vert 0\rangle|^2}{n}.
$$

#### Step 2: Identify Non-Zero Matrix Elements

From Example 8.1, we computed $\hat{A}^4\vert 0\rangle = 3\vert 0\rangle + 6\sqrt{2}\vert 2\rangle + 2\sqrt{6}\vert 4\rangle$.

So the non-zero overlaps with $n \neq 0$ are:

$$
\langle 2\vert\hat{A}^4\vert 0\rangle = 6\sqrt{2}, \qquad \langle 4\vert\hat{A}^4\vert 0\rangle = 2\sqrt{6}.
$$

#### Step 3: Compute the Sum

$$
E_0^{(2)} = -\frac{\lambda^2 x_0^8}{\hbar\omega}\left[\frac{(6\sqrt{2})^2}{2} + \frac{(2\sqrt{6})^2}{4}\right] = -\frac{\lambda^2 x_0^8}{\hbar\omega}\left[\frac{72}{2} + \frac{24}{4}\right].
$$

$$
= -\frac{\lambda^2 x_0^8}{\hbar\omega}[36 + 6] = -\frac{42\lambda^2 x_0^8}{\hbar\omega}.
$$

#### Step 4: Substitute $x_0^8$

$$
x_0^8 = \left(\frac{\hbar}{2m\omega}\right)^4 = \frac{\hbar^4}{16m^4\omega^4}.
$$

$$
\boxed{E_0^{(2)} = -\frac{42\lambda^2\hbar^4}{16m^4\omega^4\cdot\hbar\omega} = -\frac{21\lambda^2\hbar^3}{8m^4\omega^5}.}
$$

**Physical interpretation:** The second-order correction is negative (as it must be for the ground state — second-order always lowers the ground-state energy). It scales as $\lambda^2$, confirming it's a genuine second-order effect. $\blacksquare$

</details>

### Example 8.4 — The Stark Effect on the Hydrogen Ground State

**Problem:** A hydrogen atom in its ground state ($1s$) is placed in a uniform electric field $\mathbf{E} = E_0\hat{z}$. The perturbation is $\hat{H}' = eE_0 z = eE_0 r\cos\theta$. Show that the first-order correction vanishes and compute the second-order correction (quadratic Stark effect).

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: First-Order Correction

$$
E_1^{(1)} = \langle 1s\vert eE_0 r\cos\theta\vert 1s\rangle = eE_0\langle 1s\vert r\cos\theta\vert 1s\rangle.
$$

The ground state $\psi_{100} = \frac{1}{\sqrt{\pi}a_0^{3/2}}e^{-r/a_0}$ has $l = 0$, so it's spherically symmetric.

The angular integral:

$$
\int Y_0^0(\cos\theta)Y_1^0(\cos\theta)(Y_0^0)^*\,d\Omega \propto \int_0^\pi \cos\theta\sin\theta\,d\theta = 0.
$$

More directly: $\cos\theta$ is odd under parity ($\hat{\Pi}: \theta \to \pi - \theta$), while $\vert 1s\rangle$ has even parity ($(-1)^l = 1$). So $\langle 1s\vert z\vert 1s\rangle = 0$.

$$
E_1^{(1)} = 0.
$$

#### Step 2: Second-Order Correction

$$
E_1^{(2)} = \sum_{n \neq 1}\frac{|\langle n,l,m\vert eE_0 r\cos\theta\vert 1,0,0\rangle|^2}{E_1 - E_n}.
$$

**Selection rules from the angular integral:** $\cos\theta = \sqrt{\frac{4\pi}{3}}Y_1^0$, so:

$$
\int (Y_l^m)^* Y_1^0 Y_0^0\,d\Omega \neq 0 \quad \text{only if } l = 1, m = 0.
$$

So only $\vert n, 1, 0\rangle$ states contribute.

#### Step 3: The Dominant Matrix Element ($n = 2$)

$$
\langle 2,1,0\vert r\cos\theta\vert 1,0,0\rangle = \int_0^\infty R_{21}(r)\,r\,R_{10}(r)\,r^2\,dr \cdot \int (Y_1^0)^*\cos\theta\,Y_0^0\,d\Omega.
$$

The angular integral: $\int (Y_1^0)^*\sqrt{\frac{4\pi}{3}}Y_1^0 Y_0^0\,d\Omega = \sqrt{\frac{4\pi}{3}}\cdot\frac{1}{\sqrt{4\pi}}\int|Y_1^0|^2 d\Omega = \frac{1}{\sqrt{3}}$.

The radial integral with $R_{10} = 2a_0^{-3/2}e^{-r/a_0}$ and $R_{21} = \frac{1}{\sqrt{24}}a_0^{-3/2}\frac{r}{a_0}e^{-r/(2a_0)}$:

$$
\int_0^\infty R_{21}\,r\,R_{10}\,r^2\,dr = \frac{2}{\sqrt{24}a_0^4}\int_0^\infty r^4 e^{-3r/(2a_0)}\,dr.
$$

Using $\int_0^\infty r^n e^{-\alpha r}dr = n!/\alpha^{n+1}$ with $n = 4$, $\alpha = 3/(2a_0)$:

$$
= \frac{2}{\sqrt{24}a_0^4}\cdot\frac{4!}{(3/(2a_0))^5} = \frac{2}{\sqrt{24}a_0^4}\cdot\frac{24\cdot 32a_0^5}{243} = \frac{2\cdot 24\cdot 32\,a_0}{243\sqrt{24}}.
$$

$$
= \frac{2\cdot\sqrt{24}\cdot 32\,a_0}{243} = \frac{64\sqrt{24}\,a_0}{243}.
$$

Hmm — let me use the known result. The exact calculation gives:

$$
|\langle 2,1,0\vert r\cos\theta\vert 1,0,0\rangle|^2 = \frac{2^{15}}{3^{10}}a_0^2 \approx 0.555\,a_0^2.
$$

#### Step 4: The Full Second-Order Result (Including All $n$)

The exact result (summing over all intermediate states including the continuum) is:

$$
E_1^{(2)} = -\frac{9}{4}a_0^3 E_0^2 \cdot 4\pi\epsilon_0 = -\frac{9}{4}\frac{e^2 a_0^2 E_0^2}{E_1}.
$$

Wait — the standard result is:

$$
\boxed{E_1^{(2)} = -\frac{9}{4}a_0^3(4\pi\epsilon_0)E_0^2 = -\frac{1}{2}\alpha_1 E_0^2,}
$$

where $\alpha_1 = \frac{9}{2}a_0^3(4\pi\epsilon_0) = \frac{9}{2}\cdot 4\pi\epsilon_0 a_0^3$ is the ground-state polarizability of hydrogen.

Numerically: $\alpha_1/(4\pi\epsilon_0) = 4.5\,a_0^3 = 0.667 \times 10^{-30}$ m³.

**Physical interpretation:** The energy shift is quadratic in $E_0$ (hence "quadratic Stark effect") because the ground state has no permanent dipole moment. The field induces a dipole $\mathbf{d} = \alpha_1\mathbf{E}$, and the energy is $-\frac{1}{2}\alpha_1 E_0^2$. $\blacksquare$

</details>

---

## 📘 9. Appendix: Extended Derivations & Special Cases

### Appendix 9.1 — Brillouin-Wigner Perturbation Theory

Standard Rayleigh-Schrödinger perturbation theory (RSPT) expands both energies and states order-by-order. **Brillouin-Wigner perturbation theory** (BWPT) provides an alternative that sums certain classes of diagrams to all orders, at the cost of having the exact energy appear on both sides of the equation.

**Derivation:** Start from the exact Schrödinger equation $(\hat{H}_0 + \hat{V})\vert\psi_n\rangle = E_n\vert\psi_n\rangle$.

Define the projection operators: $\hat{P} = \vert\phi_n\rangle\langle\phi_n\vert$ (onto the unperturbed state) and $\hat{Q} = 1 - \hat{P}$.

Project the Schrödinger equation onto $\hat{Q}$:

$$
\hat{Q}(\hat{H}_0 + \hat{V})\vert\psi_n\rangle = E_n\hat{Q}\vert\psi_n\rangle.
$$

$$
\hat{Q}\hat{H}_0\hat{Q}\vert\psi_n\rangle + \hat{Q}\hat{V}\vert\psi_n\rangle = E_n\hat{Q}\vert\psi_n\rangle.
$$

(Using $\hat{Q}\hat{H}_0\hat{P} = 0$ since $\hat{H}_0\vert\phi_n\rangle = E_n^{(0)}\vert\phi_n\rangle$ and $\hat{Q}\vert\phi_n\rangle = 0$.)

Solve for $\hat{Q}\vert\psi_n\rangle$:

$$
\hat{Q}\vert\psi_n\rangle = \frac{\hat{Q}}{E_n - \hat{H}_0}\hat{V}\vert\psi_n\rangle = \hat{G}_0(E_n)\hat{V}\vert\psi_n\rangle,
$$

where $\hat{G}_0(E) = \hat{Q}/(E - \hat{H}_0)$ is the reduced Green's function.

Now project onto $\hat{P}$: $E_n = E_n^{(0)} + \langle\phi_n\vert\hat{V}\vert\psi_n\rangle$.

Substitute $\vert\psi_n\rangle = \vert\phi_n\rangle + \hat{G}_0(E_n)\hat{V}\vert\psi_n\rangle$ iteratively:

$$
E_n = E_n^{(0)} + \langle\phi_n\vert\hat{V}\vert\phi_n\rangle + \langle\phi_n\vert\hat{V}\hat{G}_0(E_n)\hat{V}\vert\phi_n\rangle + \langle\phi_n\vert\hat{V}\hat{G}_0(E_n)\hat{V}\hat{G}_0(E_n)\hat{V}\vert\phi_n\rangle + \cdots
$$

**Key difference from RSPT:** The denominators contain the **exact** energy $E_n$ rather than $E_n^{(0)}$:

$$
E_n = E_n^{(0)} + V_{nn} + \sum_{k \neq n}\frac{|V_{nk}|^2}{E_n - E_k^{(0)}} + \sum_{k,l \neq n}\frac{V_{nk}V_{kl}V_{ln}}{(E_n - E_k^{(0)})(E_n - E_l^{(0)})} + \cdots
$$

This is an implicit equation for $E_n$ (it appears on both sides). It can be solved self-consistently or expanded to recover RSPT order by order.

**Advantages of BWPT:**
1. Each term is individually size-extensive for single-reference problems.
2. Partial resummation captures some higher-order effects.
3. Natural framework for coupled-cluster theory in quantum chemistry.

**Disadvantage:** Not size-consistent for multi-reference problems without modification.

**References:** Brillouin, L. (1932) *J. Phys. Radium* **3**, 373; Wigner, E. (1935) *Math. u. Naturw. Anz. Ungar. Akad. Wiss.* **53**, 477; Szabo & Ostlund, *Modern Quantum Chemistry* §6.

