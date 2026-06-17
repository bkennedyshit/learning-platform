---
title: "Classical Statistical Mechanics Microstates Ensembles"
subject: "Thermodynamics & Statistical Mechanics"
catalog: advanced
audience_tier: higher-education
chapter: "5.5"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 5.5 — Classical Statistical Mechanics: Microstates & Ensembles

> *"If we wish to find in rational mechanics an a priori foundation for the principles of thermodynamics, we must seek mechanical definitions of temperature and entropy."* — J. Willard Gibbs

Statistical mechanics bridges the microscopic world of atoms and molecules to the macroscopic observables of thermodynamics. The fundamental postulate — equal a priori probabilities — combined with the concept of ensembles, allows us to derive all of thermodynamics from the mechanics of $N \sim 10^{23}$ particles. This chapter develops the microcanonical and canonical ensembles, derives Boltzmann's entropy formula, and establishes the statistical interpretation of temperature.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Define microstates, macrostates, and the phase space $\Gamma$ for classical systems.
2. State and justify the fundamental postulate of equal a priori probabilities.
3. Derive Boltzmann's entropy formula $S = k_B \ln \Omega$ from the microcanonical ensemble.
4. Construct the canonical ensemble and derive the Boltzmann distribution $P_i \propto e^{-\beta E_i}$.
5. Define and distinguish microcanonical, canonical, and grand canonical ensembles.
6. Derive the statistical definition of temperature: $1/T = (\partial S/\partial E)_V$.
7. Apply Stirling's approximation in combinatorial calculations.

---

## 🖼️ Visual Anchor — Phase Space & Microstates

![math-05__5.5-fig1](math-05__5.5-fig1.svg)

---

## 📚 1. Definitions

### Definition 5.5.1 — Microstate

A **microstate** is a complete specification of the microscopic state of a system. For $N$ classical particles in 3D, a microstate is a point in the $6N$-dimensional phase space $\Gamma$:

$$
(\mathbf{q}, \mathbf{p}) = (q_1, \ldots, q_{3N}, p_1, \ldots, p_{3N}) \in \Gamma
$$

### Definition 5.5.2 — Macrostate

A **macrostate** is specified by a small number of macroscopic observables (e.g., $E$, $V$, $N$). Many microstates correspond to the same macrostate.

### Definition 5.5.3 — Multiplicity (Number of Microstates)

The **multiplicity** $\Omega(E, V, N)$ is the number of microstates accessible to a system with energy in $[E, E+\delta E]$, volume $V$, and $N$ particles. In the classical continuum:

$$
\Omega(E) = \frac{1}{N! h^{3N}} \int_{E \leq H \leq E+\delta E} d^{3N}q\,d^{3N}p
$$

The factor $1/N!$ accounts for indistinguishability of identical particles (Gibbs factor); $h^{3N}$ provides the correct dimensionless count (quantum cell size).

### Definition 5.5.4 — Boltzmann Entropy

$$
S = k_B \ln \Omega
$$

where $k_B = 1.381 \times 10^{-23}\,\text{J/K}$ is Boltzmann's constant.

### Definition 5.5.5 — Ensemble

An **ensemble** is a (conceptual) collection of a very large number of copies of the system, each in a different microstate consistent with the macroscopic constraints:

- **Microcanonical** (NVE): isolated system, fixed $E$, $V$, $N$.
- **Canonical** (NVT): system in thermal contact with heat bath at temperature $T$.
- **Grand Canonical** ($\mu$VT): system exchanges both energy and particles with a reservoir.

### Definition 5.5.6 — Statistical Temperature

$$
\frac{1}{T} = \left(\frac{\partial S}{\partial E}\right)_{V,N} = \frac{k_B}{\Omega}\frac{\partial \Omega}{\partial E}
$$

---

## 📐 2. Axioms / Postulates

### Postulate 5.5.P1 — Equal A Priori Probabilities (Fundamental Postulate)

For an isolated system in equilibrium, all accessible microstates (those consistent with the macroscopic constraints $E$, $V$, $N$) are equally probable.

### Postulate 5.5.P2 — Ergodic Hypothesis

Over sufficiently long times, the time average of any observable equals its ensemble average:

$$
\overline{A}_{\text{time}} = \langle A \rangle_{\text{ensemble}}
$$

---

## 🛡️ 3. Lemmas

### Lemma 5.5.1 — Stirling's Approximation (Full Derivation)

For large $N$:

$$
\ln N! \approx N\ln N - N + \frac{1}{2}\ln(2\pi N)
$$

**Derivation.** Start from the exact expression:

$$
\ln N! = \sum_{k=1}^N \ln k \approx \int_1^N \ln x\,dx
$$

Evaluate the integral by parts. Let $u = \ln x$, $dv = dx$:

$$
\int_1^N \ln x\,dx = [x\ln x]_1^N - \int_1^N dx = N\ln N - N + 1
$$

For large $N$, the $+1$ is negligible: $\ln N! \approx N\ln N - N$.

The more precise form including the $\frac{1}{2}\ln(2\pi N)$ correction comes from the Euler-Maclaurin formula or from Stirling's series via the Gamma function:

$$
N! = \Gamma(N+1) \approx \sqrt{2\pi N}\left(\frac{N}{e}\right)^N
$$

Taking logarithms: $\ln N! \approx N\ln N - N + \frac{1}{2}\ln(2\pi N)$. $\blacksquare$

### Lemma 5.5.2 — Multiplicity of an Ideal Gas

For $N$ non-interacting particles in volume $V$ with total energy $E$ (kinetic only):

$$
\Omega(E, V, N) = \frac{V^N}{N! h^{3N}} \cdot \frac{(2\pi m E)^{3N/2}}{\frac{3N}{2}!} \cdot \frac{\delta E}{E}
$$

**Derivation sketch.** The momentum constraint $\sum_{i=1}^{3N} p_i^2/(2m) = E$ defines a hypersphere of radius $R = \sqrt{2mE}$ in $3N$-dimensional momentum space. The surface area of a $d$-dimensional sphere of radius $R$ is:

$$
A_d(R) = \frac{2\pi^{d/2}}{\Gamma(d/2)} R^{d-1}
$$

With $d = 3N$: the volume of the thin shell of thickness $\delta p$ corresponding to $\delta E$:

$$
\text{shell volume} = A_{3N}(R) \cdot \delta p = \frac{2\pi^{3N/2}}{\Gamma(3N/2)}(2mE)^{(3N-1)/2} \cdot \frac{m\,\delta E}{\sqrt{2mE}}
$$

The spatial integral contributes $V^N$. Combining with the $1/(N!h^{3N})$ factor gives the result. $\blacksquare$

### Lemma 5.5.3 — Sackur-Tetrode Equation

The entropy of an ideal monatomic gas:

$$
S = Nk_B\left[\ln\frac{V}{N}\left(\frac{4\pi m E}{3Nh^2}\right)^{3/2} + \frac{5}{2}\right]
$$

This follows from $S = k_B\ln\Omega$ using Stirling's approximation on the multiplicity formula. $\blacksquare$

---

## 👑 4. Theorems

### Theorem 5.5.1 — Boltzmann Distribution (Canonical Ensemble)

A system in thermal equilibrium with a heat bath at temperature $T$ has probability of being in microstate $i$ with energy $E_i$:

$$
P_i = \frac{e^{-\beta E_i}}{Z}, \quad \beta = \frac{1}{k_B T}, \quad Z = \sum_i e^{-\beta E_i}
$$

### Theorem 5.5.2 — Entropy Maximization Determines Equilibrium

Among all probability distributions $\{P_i\}$ consistent with the constraints, the equilibrium distribution maximizes the Gibbs entropy:

$$
S = -k_B \sum_i P_i \ln P_i
$$

### Theorem 5.5.3 — Thermal Equilibrium from Entropy Maximization

Two systems $A$ and $B$ in thermal contact reach equilibrium when $\partial S_{\text{total}}/\partial E_A = 0$, which gives:

$$
\frac{1}{T_A} = \frac{1}{T_B} \implies T_A = T_B
$$

---

## ✍️ 5. Proofs / Derivations

### 5.1 Derivation of the Boltzmann Distribution via Lagrange Multipliers

**Setup:** System $\mathcal{S}$ in contact with a heat bath. We seek the probability distribution $\{P_i\}$ that maximizes the entropy $S = -k_B\sum_i P_i\ln P_i$ subject to:

1. Normalization: $\sum_i P_i = 1$
2. Fixed average energy: $\sum_i P_i E_i = \langle E \rangle = U$

**Method of Lagrange multipliers.** Maximize:

$$
\mathcal{L} = -k_B\sum_i P_i\ln P_i - \alpha\left(\sum_i P_i - 1\right) - \beta'\left(\sum_i P_i E_i - U\right)
$$

Take $\partial\mathcal{L}/\partial P_j = 0$:

$$
-k_B(\ln P_j + 1) - \alpha - \beta' E_j = 0
$$

$$
\ln P_j = -1 - \frac{\alpha}{k_B} - \frac{\beta'}{k_B} E_j
$$

$$
P_j = \exp\left(-1 - \frac{\alpha}{k_B}\right) \exp\left(-\frac{\beta'}{k_B} E_j\right)
$$

Define $\beta = \beta'/k_B$ and absorb the first exponential into the normalization constant $1/Z$:

$$
P_j = \frac{1}{Z}e^{-\beta E_j}, \quad Z = \sum_i e^{-\beta E_i}
$$

**Identifying $\beta$:** Compare with thermodynamics. The entropy becomes:

$$
S = -k_B\sum_i P_i\ln P_i = -k_B\sum_i P_i(-\beta E_i - \ln Z) = k_B\beta U + k_B\ln Z
$$

From $F = U - TS$: $F = U - T(k_B\beta U + k_B\ln Z) = U(1 - k_BT\beta) - k_BT\ln Z$.

For consistency with $F = -k_BT\ln Z$ (proved in [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy)), we need $1 - k_BT\beta = 0$:

$$
\beta = \frac{1}{k_BT} \quad \blacksquare
$$

### 5.2 Derivation of Statistical Temperature

Consider two systems $A$ and $B$ forming an isolated composite with total energy $E = E_A + E_B$.

Total multiplicity: $\Omega_{\text{total}}(E_A) = \Omega_A(E_A) \cdot \Omega_B(E - E_A)$.

At equilibrium, $\Omega_{\text{total}}$ is maximized. Take the derivative with respect to $E_A$ and set to zero:

$$
\frac{\partial}{\partial E_A}[\Omega_A(E_A)\Omega_B(E-E_A)] = 0
$$

$$
\Omega_B\frac{\partial\Omega_A}{\partial E_A} + \Omega_A\frac{\partial\Omega_B}{\partial E_A} = 0
$$

$$
\Omega_B\frac{\partial\Omega_A}{\partial E_A} - \Omega_A\frac{\partial\Omega_B}{\partial E_B} = 0
$$

Divide by $\Omega_A\Omega_B$:

$$
\frac{1}{\Omega_A}\frac{\partial\Omega_A}{\partial E_A} = \frac{1}{\Omega_B}\frac{\partial\Omega_B}{\partial E_B}
$$

$$
\frac{\partial\ln\Omega_A}{\partial E_A} = \frac{\partial\ln\Omega_B}{\partial E_B}
$$

$$
\frac{\partial S_A}{\partial E_A} = \frac{\partial S_B}{\partial E_B}
$$

Define $1/T \equiv (\partial S/\partial E)_{V,N}$. Equilibrium requires $T_A = T_B$. $\blacksquare$

### 5.3 Entropy of Ideal Gas: Full Sackur-Tetrode Derivation

Starting from the multiplicity (Lemma 5.5.2), take the logarithm and apply Stirling:

$$
S = k_B\ln\Omega = k_B\left[N\ln V - \ln(N!) - 3N\ln h + \frac{3N}{2}\ln(2\pi mE) - \ln\left(\frac{3N}{2}!\right) + \ln\frac{\delta E}{E}\right]
$$

Apply Stirling ($\ln N! \approx N\ln N - N$):

$$
\ln(N!) \approx N\ln N - N
$$

$$
\ln\left(\frac{3N}{2}!\right) \approx \frac{3N}{2}\ln\frac{3N}{2} - \frac{3N}{2}
$$

Substituting and collecting terms (dropping the $\ln(\delta E/E)$ term which is negligible for large $N$):

$$
S = k_B\left[N\ln V - N\ln N + N + \frac{3N}{2}\ln(2\pi mE) - \frac{3N}{2}\ln\frac{3N}{2} + \frac{3N}{2} - 3N\ln h\right]
$$

$$
= Nk_B\left[\ln\frac{V}{N} + \frac{3}{2}\ln\frac{2\pi mE}{3N/2} + \frac{5}{2} - 3\ln h\right]
$$

$$
= Nk_B\left[\ln\frac{V}{N}\left(\frac{4\pi mE}{3Nh^2}\right)^{3/2} + \frac{5}{2}\right] \quad \blacksquare
$$

---

## 🧮 6. Worked Examples

### Example 5.5.E1 — Two-State System Multiplicity

A system of $N = 100$ non-interacting spins, each with energy $\pm\epsilon$ in a magnetic field. If total energy $E = -20\epsilon$ (i.e., 60 spins up, 40 spins down), find $\Omega$ and $S$.

**Solution:** Let $n_\uparrow$ = number of up spins (energy $-\epsilon$), $n_\downarrow = N - n_\uparrow$ (energy $+\epsilon$).

Total energy: $E = -n_\uparrow\epsilon + n_\downarrow\epsilon = -(2n_\uparrow - N)\epsilon$.

Given $E = -20\epsilon$: $2n_\uparrow - 100 = 20$, so $n_\uparrow = 60$, $n_\downarrow = 40$.

$$
\Omega = \binom{N}{n_\uparrow} = \binom{100}{60} = \frac{100!}{60!\,40!}
$$

Using Stirling: $\ln\Omega \approx 100\ln 100 - 60\ln 60 - 40\ln 40 - (100 - 60 - 40) = 100\ln 100 - 60\ln 60 - 40\ln 40$

$= 100(4.605) - 60(4.094) - 40(3.689) = 460.5 - 245.6 - 147.6 = 67.3$

$$
S = k_B\ln\Omega \approx 67.3\,k_B = 9.29 \times 10^{-22}\,\text{J/K}
$$

### Example 5.5.E2 — Statistical Temperature of Two-State System

For the spin system above, compute the temperature.

**Solution:** $S = k_B\ln\binom{N}{n_\uparrow}$. Using Stirling:

$$
S \approx k_B[N\ln N - n_\uparrow\ln n_\uparrow - (N-n_\uparrow)\ln(N-n_\uparrow)]
$$

With $E = -(2n_\uparrow - N)\epsilon$, so $n_\uparrow = (N - E/\epsilon)/2$:

$$
\frac{1}{T} = \frac{\partial S}{\partial E} = \frac{\partial S}{\partial n_\uparrow}\frac{\partial n_\uparrow}{\partial E}
$$

$$
\frac{\partial S}{\partial n_\uparrow} = k_B[-\ln n_\uparrow - 1 + \ln(N-n_\uparrow) + 1] = k_B\ln\frac{N-n_\uparrow}{n_\uparrow}
$$

$$
\frac{\partial n_\uparrow}{\partial E} = -\frac{1}{2\epsilon}
$$

$$
\frac{1}{T} = -\frac{k_B}{2\epsilon}\ln\frac{N-n_\uparrow}{n_\uparrow} = -\frac{k_B}{2\epsilon}\ln\frac{40}{60} = \frac{k_B}{2\epsilon}\ln\frac{3}{2}
$$

$$
T = \frac{2\epsilon}{k_B\ln(3/2)} = \frac{2\epsilon}{0.405\,k_B} = \frac{4.94\epsilon}{k_B}
$$

### Example 5.5.E3 — Ideal Gas Temperature from Sackur-Tetrode

From the Sackur-Tetrode equation, verify $E = \frac{3}{2}Nk_BT$.

**Solution:**

$$
\frac{1}{T} = \left(\frac{\partial S}{\partial E}\right)_V = Nk_B \cdot \frac{3}{2} \cdot \frac{1}{E} = \frac{3Nk_B}{2E}
$$

$$
T = \frac{2E}{3Nk_B} \implies E = \frac{3}{2}Nk_BT \quad \checkmark
$$

This recovers the equipartition theorem for a monatomic ideal gas.

---

## 🔗 7. Cross-links & Further Reading

### Internal Cross-links
- Entropy (thermodynamic definition): [5.2 - Entropy & Heat Engines](5.2---Entropy-&-Heat-Engines)
- Partition function (canonical ensemble formalism): [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy)
- Maxwell-Boltzmann distribution: [5.7 - Maxwell-Boltzmann Distribution & Kinetic Theory](5.7---Maxwell-Boltzmann-Distribution-&-Kinetic-Theory)
- Quantum statistics (indistinguishability): [5.8 - Quantum Statistics - Bose-Einstein & Fermi-Dirac](5.8---Quantum-Statistics---Bose-Einstein-&-Fermi-Dirac)
- Combinatorics and Stirling: [1.1 - Foundations of Calculus & Real Analysis](1.1---Foundations-of-Calculus-&-Real-Analysis)
- Linear algebra of phase space: [2.1 - Vectors Spans & Linear Independence](2.1---Vectors-Spans-&-Linear-Independence)

### Authoritative Sources
- **Susskind**, *Statistical Mechanics* (Stanford Theoretical Minimum lectures)
- **Kittel & Kroemer**, *Thermal Physics*, Ch. 1–2
- **Reif**, *Fundamentals of Statistical and Thermal Physics*, Ch. 2–3
- **Pathria & Beale**, *Statistical Mechanics*, Ch. 1–2
- [MIT OCW 8.333](https://ocw.mit.edu/courses/8-333-statistical-mechanics-i-statistical-mechanics-of-particles-fall-2013/)


---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — Counting Microstates: Distinguishable vs. Indistinguishable Particles

**Problem.** $N = 4$ particles are distributed among $M = 3$ energy levels ($\epsilon_0 = 0$, $\epsilon_1 = \epsilon$, $\epsilon_2 = 2\epsilon$) with total energy $E = 4\epsilon$. Count the number of microstates for: (a) distinguishable particles, (b) indistinguishable (bosonic) particles.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Find All Macrostates

A macrostate is specified by the occupation numbers $(n_0, n_1, n_2)$ with constraints:
- $n_0 + n_1 + n_2 = N = 4$
- $0 \cdot n_0 + 1 \cdot n_1 + 2 \cdot n_2 = 4$ (in units of $\epsilon$)

Enumerate all solutions:

| $n_0$ | $n_1$ | $n_2$ | Check: $n_1 + 2n_2 = 4$? |
|--------|--------|--------|---------------------------|
| 0 | 0 | 2 | $0 + 4 = 4$ ✓ but $n_0+n_1+n_2 = 2 \neq 4$ ✗ |
| 0 | 4 | 0 | $4 + 0 = 4$ ✓, sum = 4 ✓ |
| 1 | 2 | 1 | $2 + 2 = 4$ ✓, sum = 4 ✓ |
| 2 | 0 | 2 | $0 + 4 = 4$ ✓, sum = 4 ✓ |
| 0 | 2 | 1 | sum = 3 ✗ |

Let me be more systematic. With $n_2 = 0, 1, 2$:

- $n_2 = 0$: $n_1 = 4$, $n_0 = 0$. Macrostate: $(0, 4, 0)$.
- $n_2 = 1$: $n_1 = 2$, $n_0 = 1$. Macrostate: $(1, 2, 1)$.
- $n_2 = 2$: $n_1 = 0$, $n_0 = 2$. Macrostate: $(2, 0, 2)$.

These are the only three macrostates.

#### Part (a): Distinguishable Particles

For distinguishable particles, the number of microstates for a given macrostate $(n_0, n_1, n_2)$ is the multinomial coefficient:

$$
W = \frac{N!}{n_0!\,n_1!\,n_2!}
$$

- $(0, 4, 0)$: $W = \frac{4!}{0!\,4!\,0!} = 1$
- $(1, 2, 1)$: $W = \frac{4!}{1!\,2!\,1!} = \frac{24}{2} = 12$
- $(2, 0, 2)$: $W = \frac{4!}{2!\,0!\,2!} = \frac{24}{4} = 6$

**Total microstates (distinguishable):** $\Omega_{\text{dist}} = 1 + 12 + 6 = 19$

#### Part (b): Indistinguishable (Bosonic) Particles

For indistinguishable particles, swapping particles between the same level doesn't create a new microstate. Each macrostate corresponds to exactly ONE microstate (since the particles within each level are identical):

- $(0, 4, 0)$: 1 microstate
- $(1, 2, 1)$: 1 microstate
- $(2, 0, 2)$: 1 microstate

**Total microstates (indistinguishable bosons):** $\Omega_{\text{indist}} = 3$

#### Comparison and Physical Significance

$$
\frac{\Omega_{\text{dist}}}{\Omega_{\text{indist}}} = \frac{19}{3} \approx 6.3
$$

For large $N$, this ratio grows as $\sim N!$ (the Gibbs factor), which is why the $1/N!$ correction in the partition function is essential for indistinguishable particles. Without it, the entropy would not be extensive (Gibbs paradox).

</details>

---

### Example 8.2 — Stirling's Approximation: Full Derivation and Error Analysis

**Problem.** (a) Derive Stirling's approximation $\ln N! \approx N\ln N - N$ from the integral representation. (b) Derive the more precise form $N! \approx \sqrt{2\pi N}\left(\frac{N}{e}\right)^N$. (c) Estimate the relative error for $N = 100$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Part (a): Basic Stirling's Approximation

Start from the exact representation:

$$
\ln N! = \ln(1 \cdot 2 \cdot 3 \cdots N) = \sum_{k=1}^N \ln k
$$

Approximate the sum by an integral (valid for large $N$):

$$
\sum_{k=1}^N \ln k \approx \int_1^N \ln x\,dx
$$

Evaluate the integral by parts. Let $u = \ln x$, $dv = dx$:

$$
\int_1^N \ln x\,dx = [x\ln x - x]_1^N = N\ln N - N - (1\cdot 0 - 1) = N\ln N - N + 1
$$

For large $N$, the $+1$ is negligible:

$$
\boxed{\ln N! \approx N\ln N - N} \quad \text{(Stirling's approximation, leading order)}
$$

#### Part (b): Next-Order Correction (Laplace's Method)

The factorial has the integral representation (Gamma function):

$$
N! = \Gamma(N+1) = \int_0^\infty x^N e^{-x}\,dx
$$

Substitute $x = N + N^{1/2}t$ (expand around the maximum of the integrand at $x = N$):

Actually, the cleaner approach uses the substitution $x = Ny$:

$$
N! = \int_0^\infty (Ny)^N e^{-Ny}\,N\,dy = N^{N+1}\int_0^\infty y^N e^{-Ny}\,dy
$$

The integrand $f(y) = y^N e^{-Ny} = e^{N\ln y - Ny}$ has a maximum where:

$$
\frac{d}{dy}(N\ln y - Ny) = \frac{N}{y} - N = 0 \implies y_0 = 1
$$

Expand around $y = 1$: let $y = 1 + t/\sqrt{N}$:

$$
N\ln y - Ny = N\ln\left(1 + \frac{t}{\sqrt{N}}\right) - N\left(1 + \frac{t}{\sqrt{N}}\right)
$$

$$
\approx N\left(\frac{t}{\sqrt{N}} - \frac{t^2}{2N}\right) - N - \sqrt{N}\,t = \sqrt{N}\,t - \frac{t^2}{2} - N - \sqrt{N}\,t = -N - \frac{t^2}{2}
$$

Therefore:

$$
N! \approx N^{N+1}\int_{-\infty}^{\infty} e^{-N - t^2/2}\frac{dt}{\sqrt{N}} = N^{N+1}\cdot e^{-N}\cdot\frac{1}{\sqrt{N}}\cdot\sqrt{2\pi}
$$

$$
= \sqrt{2\pi N}\cdot N^N\cdot e^{-N} = \sqrt{2\pi N}\left(\frac{N}{e}\right)^N
$$

$$
\boxed{N! \approx \sqrt{2\pi N}\left(\frac{N}{e}\right)^N} \quad \text{(Stirling's formula with prefactor)}
$$

Taking the logarithm:

$$
\ln N! \approx N\ln N - N + \frac{1}{2}\ln(2\pi N)
$$

#### Part (c): Error Estimate for $N = 100$

Exact: $\ln(100!) = \sum_{k=1}^{100}\ln k = 363.739$ (computed numerically).

Basic Stirling: $100\ln 100 - 100 = 100(4.6052) - 100 = 360.52$. Error: $3.22/363.74 = 0.88\%$.

With prefactor: $360.52 + \frac{1}{2}\ln(200\pi) = 360.52 + \frac{1}{2}(6.4457) = 360.52 + 3.22 = 363.74$. Error: $\lt  0.001\%$.

For statistical mechanics applications where $N \sim 10^{23}$, the basic approximation is extraordinarily accurate — the relative error is $O(\ln N/N) \sim 10^{-22}$.

</details>

---

### Example 8.3 — Microcanonical Ensemble: Ideal Gas in a Box

**Problem.** Derive the entropy of an ideal gas of $N$ identical particles in volume $V$ with total energy $E$ using the microcanonical ensemble (counting accessible microstates in phase space). Recover the Sackur-Tetrode equation.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Phase Space Volume

For $N$ particles in 3D, the phase space has $6N$ dimensions: $(q_1, \ldots, q_{3N}, p_1, \ldots, p_{3N})$.

The position integrals: each particle is confined to volume $V$, so $\int d^{3N}q = V^N$.

The momentum constraint: total kinetic energy $E = \sum_{i=1}^{3N} p_i^2/(2m)$. The accessible momenta lie on the surface of a $3N$-dimensional sphere of radius $R = \sqrt{2mE}$:

$$
\sum_{i=1}^{3N} p_i^2 = 2mE
$$

#### Step 2: Volume of a Hypersphere

The volume of a $d$-dimensional sphere of radius $R$ is:

$$
V_d(R) = \frac{\pi^{d/2}}{\Gamma(d/2 + 1)}R^d
$$

For $d = 3N$:

$$
V_{3N}(R) = \frac{\pi^{3N/2}}{\Gamma(3N/2 + 1)}(2mE)^{3N/2}
$$

The number of microstates with energy $\leq E$:

$$
\Phi(E) = \frac{1}{N!h^{3N}}V^N \cdot V_{3N}(\sqrt{2mE})
$$

The $1/N!$ accounts for indistinguishability; $h^{3N}$ is the phase space cell size (quantum mechanical).

#### Step 3: Entropy via Boltzmann

Using $S = k_B\ln\Omega$ where $\Omega = \partial\Phi/\partial E \cdot \delta E$ (density of states times energy shell thickness). For large $N$, $\ln\Omega \approx \ln\Phi$ (the volume and surface area of a high-dimensional sphere have the same logarithm to leading order):

$$
S = k_B\ln\Phi = k_B\left[-\ln N! - 3N\ln h + N\ln V + \frac{3N}{2}\ln(2mE) + \ln\frac{\pi^{3N/2}}{\Gamma(3N/2+1)}\right]
$$

Using Stirling on $\ln N! \approx N\ln N - N$ and $\ln\Gamma(3N/2+1) \approx \frac{3N}{2}\ln\frac{3N}{2} - \frac{3N}{2}$:

$$
S = Nk_B\left[\ln V - \ln N + \frac{3}{2}\ln(2mE) - \frac{3}{2}\ln\frac{3N}{2} + \frac{3}{2}\ln\pi - 3\ln h + \frac{5}{2}\right]
$$

Simplify using $E = \frac{3}{2}Nk_BT$:

$$
\frac{2mE}{3N} = \frac{2m \cdot \frac{3}{2}Nk_BT}{3N} = mk_BT
$$

$$
S = Nk_B\left[\ln\frac{V}{N} + \frac{3}{2}\ln\frac{2\pi mk_BT}{h^2} + \frac{5}{2}\right]
$$

Define the thermal de Broglie wavelength $\lambda = h/\sqrt{2\pi mk_BT}$:

$$
\boxed{S = Nk_B\left[\ln\frac{V}{N\lambda^3} + \frac{5}{2}\right]} \quad \text{(Sackur-Tetrode equation)}
$$

#### Verification

- **Extensivity:** $S(2N, 2V, 2E) = 2S(N, V, E)$. ✓ (The $V/N$ ratio ensures this — without the $1/N!$ factor, we'd get $\ln V$ instead of $\ln(V/N)$, violating extensivity. This is the resolution of the Gibbs paradox.)
- **Temperature:** $1/T = (\partial S/\partial E)_V = Nk_B \cdot \frac{3}{2} \cdot \frac{1}{E}$, giving $E = \frac{3}{2}Nk_BT$. ✓
- **Pressure:** $P/T = (\partial S/\partial V)_E = Nk_B/V$, giving $PV = Nk_BT$. ✓

</details>

---

### Example 8.4 — The Gibbs Paradox and Its Resolution

**Problem.** (a) Show that without the $1/N!$ factor, the entropy of mixing two identical ideal gases gives $\Delta S_{\text{mix}} > 0$ (paradox). (b) Show that including $1/N!$ resolves the paradox.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Part (a): The Paradox

Consider two containers, each with $N$ particles of the SAME ideal gas at the same $T$ and $P$, with volumes $V$ each. Remove the partition.

**Without the $1/N!$ correction**, the entropy would be (using the "incorrect" formula $S = Nk_B\ln V + \text{terms independent of } V$):

Before: $S_{\text{before}} = 2 \times Nk_B\ln V + \cdots = 2Nk_B\ln V + \cdots$

After (2N particles in volume 2V): $S_{\text{after}} = 2Nk_B\ln(2V) + \cdots$

$$
\Delta S = 2Nk_B\ln(2V) - 2Nk_B\ln V = 2Nk_B\ln 2 \gt  0
$$

This is absurd: removing a partition between two containers of the SAME gas at the same $T, P$ is a trivially reversible process (just put the partition back). There should be no entropy change.

#### Part (b): Resolution with $1/N!$

With the correct Sackur-Tetrode formula: $S = Nk_B\ln(V/N) + \cdots$

Before: $S_{\text{before}} = 2 \times Nk_B\ln(V/N) + \cdots$

After (2N particles in 2V): $S_{\text{after}} = 2Nk_B\ln(2V/(2N)) + \cdots = 2Nk_B\ln(V/N) + \cdots$

$$
\Delta S = 0 \quad \checkmark
$$

The $1/N!$ factor, which accounts for the indistinguishability of identical particles, makes the entropy properly extensive and resolves the Gibbs paradox.

**For DIFFERENT gases** (e.g., $N$ molecules of A in one container, $N$ molecules of B in the other), the particles ARE distinguishable (A from B), and the entropy of mixing is genuinely:

$$
\Delta S_{\text{mix}} = 2Nk_B\ln 2
$$

This is a real, measurable entropy increase — the gases spontaneously mix and work would be required to separate them again.

</details>



---

## 📘 9. Appendix: Extended Derivations & Special Cases

### Appendix 9.1 — The Ergodic Hypothesis and Ensemble Averaging

The ergodic hypothesis is the foundational assumption that connects statistical mechanics (ensemble averages) to experimental measurements (time averages). Here we state it precisely and discuss its implications.

**Statement of the Ergodic Hypothesis:**

For an isolated system in equilibrium, the time average of any macroscopic observable $A$ equals its microcanonical ensemble average:

$$
\langle A \rangle_{\text{time}} \equiv \lim_{\tau\to\infty}\frac{1}{\tau}\int_0^\tau A(\mathbf{q}(t), \mathbf{p}(t))\,dt = \langle A \rangle_{\text{ensemble}} \equiv \frac{1}{\Omega}\sum_{\text{microstates}} A_i
$$

**Physical meaning:** As the system evolves in time, its trajectory in phase space eventually visits all accessible microstates (those consistent with the macroscopic constraints $E$, $V$, $N$) with equal probability. "Equal probability" is the key assumption — it is the **fundamental postulate of statistical mechanics** (also called the postulate of equal a priori probabilities).

**Why is this non-trivial?** Consider a system of $N \sim 10^{23}$ particles. The phase space has $6N \sim 10^{24}$ dimensions. The energy surface $H = E$ is a $(6N-1)$-dimensional manifold. The ergodic hypothesis asserts that the system's trajectory densely covers this entire manifold — it doesn't get "stuck" in some subregion.

**When does ergodicity fail?**

1. **Integrable systems:** A system with $N$ degrees of freedom and $N$ conserved quantities (integrals of motion) is confined to an $N$-dimensional torus in $2N$-dimensional phase space — it cannot explore the full energy surface. Example: $N$ uncoupled harmonic oscillators.

2. **Glasses and metastable states:** A glass is "stuck" in a local energy minimum and cannot explore the full configuration space on experimental timescales. The system is ergodic in principle (given infinite time) but not in practice.

3. **KAM theorem:** For weakly perturbed integrable systems, some invariant tori survive (KAM tori), creating barriers in phase space. Ergodicity is broken for trajectories on these tori.

**Practical resolution:** For most physical systems with many degrees of freedom and generic (non-integrable) interactions, ergodicity holds to excellent approximation. The key is that interactions between particles cause "mixing" in phase space — trajectories diverge exponentially (chaos), ensuring rapid exploration of the energy surface.

**The mixing hierarchy:**

$$
\text{Ergodic} \subset \text{Mixing} \subset \text{K-systems} \subset \text{Bernoulli systems}
$$

- **Ergodic:** Time averages = ensemble averages.
- **Mixing:** Correlations decay to zero: $\langle A(t)B(0)\rangle \to \langle A\rangle\langle B\rangle$ as $t \to \infty$.
- **K-systems (Kolmogorov):** Positive Lyapunov exponents — exponential sensitivity to initial conditions.
- **Bernoulli:** Strongest form of randomness — equivalent to independent coin flips.

Most interacting many-body systems are at least mixing, which is sufficient for statistical mechanics.

**Connection to the Second Law:** If a system is ergodic, then starting from any initial microstate, it will eventually reach the macrostate with the largest number of microstates (maximum entropy). The Second Law is thus a consequence of ergodicity plus the overwhelming dominance of the equilibrium macrostate in phase space volume.

**Reference:** Susskind, *Statistical Mechanics* Lectures 1–2; Pathria & Beale, *Statistical Mechanics*, Ch. 2; Khinchin, *Mathematical Foundations of Statistical Mechanics*.

---

### Appendix 9.2 — Equivalence of Ensembles in the Thermodynamic Limit

A remarkable result of statistical mechanics is that the microcanonical, canonical, and grand canonical ensembles give identical predictions for macroscopic observables in the thermodynamic limit ($N \to \infty$, $V \to \infty$, $N/V = \text{const}$).

**The key insight: energy fluctuations are negligible.**

In the canonical ensemble, the energy fluctuates. The relative fluctuation is:

$$
\frac{\sigma_E}{\langle E\rangle} = \frac{\sqrt{\langle(\Delta E)^2\rangle}}{\langle E\rangle} = \frac{\sqrt{k_BT^2 C_V}}{\langle E\rangle}
$$

For an ideal gas: $\langle E\rangle = \frac{3}{2}Nk_BT$ and $C_V = \frac{3}{2}Nk_B$:

$$
\frac{\sigma_E}{\langle E\rangle} = \frac{\sqrt{k_BT^2 \cdot \frac{3}{2}Nk_B}}{\frac{3}{2}Nk_BT} = \frac{T\sqrt{\frac{3}{2}Nk_B^2}}{\frac{3}{2}Nk_BT} = \frac{\sqrt{3/(2N)}\cdot k_BT}{\frac{3}{2}k_BT} = \sqrt{\frac{2}{3N}}
$$

For $N = 10^{23}$: $\sigma_E/\langle E\rangle \sim 10^{-12}$. The energy distribution is so sharply peaked that the canonical ensemble (which allows energy fluctuations) gives the same results as the microcanonical ensemble (which fixes energy exactly).

**Formal statement:** Let $f(E)$ be any smooth function of energy. Then:

$$
\langle f(E)\rangle_{\text{canonical}} = f(\langle E\rangle_{\text{canonical}}) + O(1/N)
$$

In the thermodynamic limit, the canonical average of $f(E)$ equals $f$ evaluated at the mean energy — which is the microcanonical value.

**When do ensembles differ?** At phase transitions (especially first-order), the energy distribution can become bimodal, and the ensembles may give different predictions for finite systems. In the thermodynamic limit, they still agree on equilibrium properties, but the canonical ensemble can describe phase coexistence more naturally.

**Practical consequence:** We are free to use whichever ensemble is most convenient for calculation:
- **Microcanonical** ($E$, $V$, $N$ fixed): conceptually fundamental, but often hard to compute.
- **Canonical** ($T$, $V$, $N$ fixed): most common; the partition function $Z$ is usually tractable.
- **Grand canonical** ($T$, $V$, $\mu$ fixed): essential for quantum gases and open systems.

**Reference:** Kittel & Kroemer, *Thermal Physics*, Ch. 3; Pathria & Beale, *Statistical Mechanics*, Ch. 3–4; David Tong, *Statistical Mechanics* Notes §3.

---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

*Previous: [5.4 - Chemical Potential & Phase Transitions](5.4---Chemical-Potential-&-Phase-Transitions) | Next: [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy)*
