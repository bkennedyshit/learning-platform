---
title: "Quantum Statistics Bose Einstein Fermi Dirac"
subject: "Thermodynamics & Statistical Mechanics"
catalog: advanced
audience_tier: higher-education
chapter: "5.8"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 5.8 — Quantum Statistics: Bose-Einstein & Fermi-Dirac

> *"The atoms in a gas at sufficiently low temperature will all condense into the lowest energy state — a new state of matter."* — Satyendra Nath Bose & Albert Einstein (1924–25)

At low temperatures or high densities, quantum effects become dominant: identical particles are fundamentally indistinguishable, and the Pauli exclusion principle (for fermions) or bosonic bunching radically alters the statistical distribution. This chapter derives the Fermi-Dirac and Bose-Einstein distributions from the grand canonical ensemble, applies them to photon gases (blackbody radiation), phonons (Debye model), conduction electrons (Fermi gas), and Bose-Einstein condensation.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Distinguish bosons from fermions and state the spin-statistics theorem.
2. Derive the Fermi-Dirac and Bose-Einstein distribution functions from the grand canonical ensemble.
3. Apply the Planck distribution to derive the Stefan-Boltzmann law and Wien's displacement law.
4. Compute the Fermi energy, Fermi temperature, and electronic heat capacity of metals.
5. Derive the Debye model for phonon heat capacity ($C_V \propto T^3$ at low $T$).
6. Describe Bose-Einstein condensation and compute the critical temperature $T_c$.
7. Identify the classical (Maxwell-Boltzmann) limit of both quantum distributions.

---

## 🖼️ Visual Anchor — Fermi-Dirac Distribution at Various Temperatures

![math-05__5.8-fig1](math-05__5.8-fig1.svg)

---

## 📚 1. Definitions

### Definition 5.8.1 — Bosons and Fermions

- **Bosons:** Particles with integer spin ($s = 0, 1, 2, \ldots$). Wave function symmetric under particle exchange. No limit on occupation number. Examples: photons, phonons, $^4$He, gluons.
- **Fermions:** Particles with half-integer spin ($s = 1/2, 3/2, \ldots$). Wave function antisymmetric under exchange. Maximum occupation $n_i = 1$ (Pauli exclusion). Examples: electrons, protons, neutrons, $^3$He.

### Definition 5.8.2 — Quantum Distribution Functions

**Fermi-Dirac** (fermions):

$$
\langle n_i\rangle_{\text{FD}} = \frac{1}{e^{(\epsilon_i - \mu)/(k_BT)} + 1}
$$

**Bose-Einstein** (bosons):

$$
\langle n_i\rangle_{\text{BE}} = \frac{1}{e^{(\epsilon_i - \mu)/(k_BT)} - 1}
$$

In both cases, $\mu$ is the chemical potential determined by the constraint $\sum_i \langle n_i\rangle = N$.

### Definition 5.8.3 — Fermi Energy and Fermi Temperature

The **Fermi energy** $\epsilon_F$ is the chemical potential at $T = 0$:

$$
\epsilon_F = \frac{\hbar^2}{2m}\left(\frac{3\pi^2 N}{V}\right)^{2/3}
$$

The **Fermi temperature**: $T_F = \epsilon_F/k_B$. For metals, $T_F \sim 10^4$–$10^5\,\text{K}$.

### Definition 5.8.4 — Density of States

For free particles in 3D (spin degeneracy $g_s$):

$$
g(\epsilon) = \frac{g_s V}{4\pi^2}\left(\frac{2m}{\hbar^2}\right)^{3/2}\sqrt{\epsilon}
$$

For photons ($g_s = 2$ polarizations, $\epsilon = \hbar\omega = hc/\lambda$):

$$
g(\omega) = \frac{V\omega^2}{\pi^2 c^3}
$$

### Definition 5.8.5 — Bose-Einstein Condensation Temperature

$$
T_c = \frac{2\pi\hbar^2}{mk_B}\left(\frac{n}{\zeta(3/2)}\right)^{2/3}
$$

where $\zeta(3/2) \approx 2.612$ and $n = N/V$.

---

## 📐 2. Axioms / Postulates

### Postulate 5.8.P1 — Spin-Statistics Theorem

Particles with integer spin obey Bose-Einstein statistics; particles with half-integer spin obey Fermi-Dirac statistics. This is a consequence of relativistic quantum field theory (proved by Pauli, 1940).

### Postulate 5.8.P2 — Grand Canonical Ensemble

For systems with variable particle number, the grand partition function is:

$$
\mathcal{Z} = \sum_{N=0}^\infty e^{\beta\mu N} Z_N = \prod_i \sum_{n_i} e^{-\beta(\epsilon_i - \mu)n_i}
$$

where $n_i = 0, 1$ for fermions and $n_i = 0, 1, 2, \ldots$ for bosons.

---

## 🛡️ 3. Lemmas

### Lemma 5.8.1 — Grand Canonical Derivation of Fermi-Dirac

For a single fermionic state $i$ with energy $\epsilon_i$, occupation $n_i \in \{0, 1\}$:

$$
\mathcal{Z}_i = \sum_{n_i=0}^1 e^{-\beta(\epsilon_i-\mu)n_i} = 1 + e^{-\beta(\epsilon_i-\mu)}
$$

$$
\langle n_i\rangle = -\frac{1}{\beta}\frac{\partial\ln\mathcal{Z}_i}{\partial\epsilon_i} = \frac{e^{-\beta(\epsilon_i-\mu)}}{1 + e^{-\beta(\epsilon_i-\mu)}} = \frac{1}{e^{\beta(\epsilon_i-\mu)} + 1} \quad \blacksquare
$$

### Lemma 5.8.2 — Grand Canonical Derivation of Bose-Einstein

For a single bosonic state $i$, $n_i = 0, 1, 2, \ldots$:

$$
\mathcal{Z}_i = \sum_{n_i=0}^\infty e^{-\beta(\epsilon_i-\mu)n_i} = \frac{1}{1 - e^{-\beta(\epsilon_i-\mu)}}
$$

(geometric series, converges for $\epsilon_i > \mu$).

$$
\langle n_i\rangle = \frac{1}{\beta}\frac{\partial\ln\mathcal{Z}_i}{\partial\mu} = \frac{e^{-\beta(\epsilon_i-\mu)}}{1 - e^{-\beta(\epsilon_i-\mu)}} = \frac{1}{e^{\beta(\epsilon_i-\mu)} - 1} \quad \blacksquare
$$

### Lemma 5.8.3 — Classical Limit

When $e^{\beta(\epsilon_i - \mu)} \gg 1$ (high $T$, low density), both distributions reduce to:

$$
\langle n_i\rangle \approx e^{-\beta(\epsilon_i - \mu)} = e^{\beta\mu}e^{-\beta\epsilon_i}
$$

This is the Maxwell-Boltzmann distribution (classical limit). The condition is $n\lambda^3 \ll 1$ (thermal de Broglie wavelength much smaller than inter-particle spacing).

---

## 👑 4. Theorems

### Theorem 5.8.1 — Planck Distribution (Blackbody Radiation)

Photons have $\mu = 0$ (number not conserved). The mean occupation of mode with frequency $\omega$:

$$
\langle n(\omega)\rangle = \frac{1}{e^{\hbar\omega/(k_BT)} - 1}
$$

Energy density per unit frequency:

$$
u(\omega) = \frac{\hbar\omega^3}{\pi^2 c^3}\frac{1}{e^{\hbar\omega/(k_BT)} - 1}
$$

### Theorem 5.8.2 — Stefan-Boltzmann Law

Total radiated power per unit area:

$$
j = \sigma T^4, \quad \sigma = \frac{\pi^2 k_B^4}{60\hbar^3 c^2} = 5.67\times10^{-8}\,\text{W/(m}^2\text{K}^4\text{)}
$$

### Theorem 5.8.3 — Debye $T^3$ Law

At low temperatures ($T \ll \Theta_D$), the phonon heat capacity:

$$
C_V = \frac{12\pi^4}{5}Nk_B\left(\frac{T}{\Theta_D}\right)^3
$$

where $\Theta_D = \hbar\omega_D/k_B$ is the Debye temperature.

### Theorem 5.8.4 — Fermi Gas Ground State Energy

At $T = 0$, the total energy of $N$ fermions:

$$
E_0 = \frac{3}{5}N\epsilon_F
$$

### Theorem 5.8.5 — Electronic Heat Capacity

At $T \ll T_F$:

$$
C_V^{\text{el}} = \frac{\pi^2}{2}Nk_B\frac{T}{T_F} = \gamma T
$$

(linear in $T$, much smaller than the classical $\frac{3}{2}Nk_B$).

---

## ✍️ 5. Proofs / Derivations

### 5.1 Derivation of the Fermi Energy

At $T = 0$, the Fermi-Dirac distribution becomes a step function: $\langle n\rangle = 1$ for $\epsilon < \epsilon_F$ and $\langle n\rangle = 0$ for $\epsilon > \epsilon_F$.

Total number of particles (spin-1/2 fermions, $g_s = 2$):

$$
N = \int_0^{\epsilon_F} g(\epsilon)\,d\epsilon = \frac{V}{2\pi^2}\left(\frac{2m}{\hbar^2}\right)^{3/2}\int_0^{\epsilon_F}\sqrt{\epsilon}\,d\epsilon
$$

$$
= \frac{V}{2\pi^2}\left(\frac{2m}{\hbar^2}\right)^{3/2}\cdot\frac{2}{3}\epsilon_F^{3/2}
$$

$$
= \frac{V}{3\pi^2}\left(\frac{2m\epsilon_F}{\hbar^2}\right)^{3/2}
$$

Solve for $\epsilon_F$:

$$
\epsilon_F = \frac{\hbar^2}{2m}\left(\frac{3\pi^2 N}{V}\right)^{2/3} \quad \blacksquare
$$

### 5.2 Derivation of the Stefan-Boltzmann Law

Total energy density:

$$
u = \int_0^\infty u(\omega)\,d\omega = \frac{\hbar}{\pi^2 c^3}\int_0^\infty\frac{\omega^3}{e^{\hbar\omega/(k_BT)}-1}\,d\omega
$$

Substitute $x = \hbar\omega/(k_BT)$, $d\omega = (k_BT/\hbar)\,dx$:

$$
u = \frac{\hbar}{\pi^2 c^3}\left(\frac{k_BT}{\hbar}\right)^4\int_0^\infty\frac{x^3}{e^x - 1}\,dx
$$

The integral $\int_0^\infty x^3/(e^x-1)\,dx = \Gamma(4)\zeta(4) = 6 \cdot \pi^4/90 = \pi^4/15$.

$$
u = \frac{k_B^4 T^4}{\pi^2 c^3 \hbar^3}\cdot\frac{\pi^4}{15} = \frac{\pi^2 k_B^4}{15\hbar^3 c^3}T^4
$$

The radiated power per unit area (Stefan-Boltzmann): $j = cu/4 = \sigma T^4$ with:

$$
\sigma = \frac{\pi^2 k_B^4}{60\hbar^3 c^2} \quad \blacksquare
$$

### 5.3 Derivation of Ground State Energy $E_0 = \frac{3}{5}N\epsilon_F$

$$
E_0 = \int_0^{\epsilon_F}\epsilon\,g(\epsilon)\,d\epsilon = \frac{V}{2\pi^2}\left(\frac{2m}{\hbar^2}\right)^{3/2}\int_0^{\epsilon_F}\epsilon^{3/2}\,d\epsilon
$$

$$
= \frac{V}{2\pi^2}\left(\frac{2m}{\hbar^2}\right)^{3/2}\cdot\frac{2}{5}\epsilon_F^{5/2}
$$

Compare with $N = \frac{V}{3\pi^2}(2m\epsilon_F/\hbar^2)^{3/2}$:

$$
\frac{E_0}{N} = \frac{\frac{2}{5}\epsilon_F^{5/2} \cdot \frac{V}{2\pi^2}(2m/\hbar^2)^{3/2}}{\frac{V}{3\pi^2}(2m/\hbar^2)^{3/2}\epsilon_F^{3/2}} = \frac{2/5}{2/3}\epsilon_F = \frac{3}{5}\epsilon_F
$$

$$
E_0 = \frac{3}{5}N\epsilon_F \quad \blacksquare
$$

### 5.4 Derivation of Electronic Heat Capacity (Sommerfeld Expansion)

At $T \ll T_F$, only electrons within $\sim k_BT$ of $\epsilon_F$ are thermally excited. The fraction of excited electrons is $\sim T/T_F$, each gaining energy $\sim k_BT$:

$$
\Delta E \sim N\frac{T}{T_F}\cdot k_BT = Nk_B\frac{T^2}{T_F}
$$

$$
C_V = \frac{\partial\Delta E}{\partial T} \sim Nk_B\frac{T}{T_F}
$$

The exact Sommerfeld expansion gives:

$$
C_V = \frac{\pi^2}{2}Nk_B\frac{T}{T_F} \quad \blacksquare
$$

---

## 🧮 6. Worked Examples

### Example 5.8.E1 — Fermi Energy of Copper

Copper: density $\rho = 8960\,\text{kg/m}^3$, atomic mass $A = 63.5\,\text{g/mol}$, one conduction electron per atom.

$$
n = \frac{\rho N_A}{A} = \frac{8960 \times 6.022\times10^{23}}{0.0635} = 8.49\times10^{28}\,\text{m}^{-3}
$$

$$
\epsilon_F = \frac{\hbar^2}{2m_e}(3\pi^2 n)^{2/3} = \frac{(1.055\times10^{-34})^2}{2\times9.109\times10^{-31}}(3\pi^2\times8.49\times10^{28})^{2/3}
$$

$$
= \frac{1.113\times10^{-68}}{1.822\times10^{-30}}\times(2.51\times10^{30})^{2/3} = 6.11\times10^{-39}\times1.85\times10^{20} = 1.13\times10^{-18}\,\text{J} = 7.04\,\text{eV}
$$

$$
T_F = \epsilon_F/k_B = 1.13\times10^{-18}/1.381\times10^{-23} = 81{,}800\,\text{K}
$$

At room temperature ($T = 300\,\text{K}$): $T/T_F = 0.0037$, so the electron gas is highly degenerate.

### Example 5.8.E2 — Planck Distribution: Peak Frequency (Wien's Law)

Find the frequency $\omega_{\max}$ at which $u(\omega)$ is maximum.

Set $du/d\omega = 0$. Let $x = \hbar\omega/(k_BT)$:

$$
\frac{d}{dx}\frac{x^3}{e^x - 1} = 0 \implies 3x^2(e^x-1) - x^3 e^x = 0 \implies 3(e^x-1) = xe^x
$$

$$
3 - 3e^{-x} = x \implies x \approx 2.822 \quad \text{(numerical solution)}
$$

$$
\hbar\omega_{\max} = 2.822\,k_BT \implies \omega_{\max} = \frac{2.822\,k_BT}{\hbar}
$$

In wavelength: $\lambda_{\max}T = 2.898\times10^{-3}\,\text{m·K}$ (Wien's displacement law).

### Example 5.8.E3 — BEC Critical Temperature for Rubidium

$^{87}$Rb atoms ($m = 87 \times 1.66\times10^{-27}\,\text{kg}$) at density $n = 2.5\times10^{18}\,\text{m}^{-3}$:

$$
T_c = \frac{2\pi\hbar^2}{mk_B}\left(\frac{n}{2.612}\right)^{2/3}
$$

$$
= \frac{2\pi(1.055\times10^{-34})^2}{1.44\times10^{-25}\times1.381\times10^{-23}}\left(\frac{2.5\times10^{18}}{2.612}\right)^{2/3}
$$

$$
= \frac{7.00\times10^{-68}}{1.99\times10^{-48}}\times(9.57\times10^{17})^{2/3} = 3.52\times10^{-20}\times9.72\times10^{11} = 170\,\text{nK}
$$

Experimental BEC in Rb-87 was achieved at $\sim 170\,\text{nK}$ (Cornell & Wieman, 1995). $\checkmark$

---

## 🔗 7. Cross-links & Further Reading

### Internal Cross-links
- Classical statistics (MB limit): [5.7 - Maxwell-Boltzmann Distribution & Kinetic Theory](5.7---Maxwell-Boltzmann-Distribution-&-Kinetic-Theory)
- Partition function formalism: [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy)
- Canonical ensemble: [5.5 - Classical Statistical Mechanics - Microstates & Ensembles](5.5---Classical-Statistical-Mechanics---Microstates-&-Ensembles)
- Quantum mechanics foundations: [9.1 - Wave-Particle Duality & the Schrödinger Equation](9.1---Wave-Particle-Duality-&-the-Schrödinger-Equation)
- Eigenvalues (energy levels): [2.6 - Eigenvalues Eigenvectors & Diagonalization](2.6---Eigenvalues-Eigenvectors-&-Diagonalization)

### Authoritative Sources
- **Kittel & Kroemer**, *Thermal Physics*, Ch. 7 (Fermi gas), Ch. 4 (Planck distribution)
- **Pathria & Beale**, *Statistical Mechanics*, Ch. 6–7
- **Landau & Lifshitz**, *Statistical Physics Part 1*, Ch. 5 (Fermi/Bose)
- **Cornell & Wieman** (2002), Nobel Lecture on BEC
- [MIT OCW 8.333](https://ocw.mit.edu/courses/8-333-statistical-mechanics-i-statistical-mechanics-of-particles-fall-2013/)


---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — Photon Bose-Einstein Distribution → Planck Radiation Law

**Problem.** Starting from the Bose-Einstein distribution for photons (with $\mu = 0$), derive the Planck spectral energy density $u(\omega)$ and show it reduces to the Rayleigh-Jeans law at low frequencies and Wien's law at high frequencies.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Photon Occupation Number

Photons are bosons with zero chemical potential ($\mu = 0$ because photon number is not conserved — they are freely created and absorbed). The mean occupation number of a mode with frequency $\omega$ is:

$$
\langle n(\omega)\rangle = \frac{1}{e^{\beta\hbar\omega} - 1} = \frac{1}{e^{\hbar\omega/(k_BT)} - 1}
$$

#### Step 2: Density of States for Photons

In a cavity of volume $V$, the number of electromagnetic modes with frequency between $\omega$ and $\omega + d\omega$ is:

$$
g(\omega)\,d\omega = \frac{V\omega^2}{\pi^2 c^3}\,d\omega
$$

The factor of 2 for polarization is included. Derivation: the wavevector magnitude is $k = \omega/c$. The number of modes in a shell $dk$ in $k$-space is $V \cdot 4\pi k^2\,dk/(2\pi)^3 \times 2$ (factor 2 for polarization):

$$
g(\omega)\,d\omega = V\frac{4\pi(\omega/c)^2}{(2\pi)^3}\cdot\frac{2}{c}\,d\omega = \frac{V\omega^2}{\pi^2 c^3}\,d\omega
$$

#### Step 3: Spectral Energy Density

Each mode carries energy $\hbar\omega$ times its occupation number. The energy per unit volume per unit frequency:

$$
u(\omega) = \frac{1}{V}g(\omega)\cdot\hbar\omega\cdot\langle n(\omega)\rangle = \frac{\omega^2}{\pi^2 c^3}\cdot\frac{\hbar\omega}{e^{\hbar\omega/(k_BT)} - 1}
$$

$$
\boxed{u(\omega) = \frac{\hbar\omega^3}{\pi^2 c^3}\cdot\frac{1}{e^{\hbar\omega/(k_BT)} - 1}} \quad \text{(Planck's law)}
$$

#### Step 4: Limiting Cases

**Low frequency (Rayleigh-Jeans):** $\hbar\omega \ll k_BT$, so $e^{\hbar\omega/(k_BT)} \approx 1 + \hbar\omega/(k_BT)$:

$$
u(\omega) \approx \frac{\hbar\omega^3}{\pi^2 c^3}\cdot\frac{k_BT}{\hbar\omega} = \frac{\omega^2 k_BT}{\pi^2 c^3}
$$

This is the **Rayleigh-Jeans law** — the classical result that gives $k_BT$ per mode (equipartition). It diverges as $\omega \to \infty$ (the "ultraviolet catastrophe"), which historically motivated Planck's quantum hypothesis.

**High frequency (Wien):** $\hbar\omega \gg k_BT$, so $e^{\hbar\omega/(k_BT)} \gg 1$:

$$
u(\omega) \approx \frac{\hbar\omega^3}{\pi^2 c^3}e^{-\hbar\omega/(k_BT)}
$$

This is **Wien's law** — an exponential cutoff that prevents the ultraviolet catastrophe.

#### Step 5: Total Energy (Stefan-Boltzmann Law)

$$
u_{\text{total}} = \int_0^\infty u(\omega)\,d\omega = \frac{\hbar}{\pi^2 c^3}\int_0^\infty\frac{\omega^3}{e^{\hbar\omega/(k_BT)} - 1}\,d\omega
$$

Substitute $x = \hbar\omega/(k_BT)$:

$$
= \frac{\hbar}{\pi^2 c^3}\left(\frac{k_BT}{\hbar}\right)^4\int_0^\infty\frac{x^3}{e^x - 1}\,dx = \frac{(k_BT)^4}{\pi^2 c^3\hbar^3}\cdot\frac{\pi^4}{15}
$$

$$
u_{\text{total}} = \frac{\pi^2 k_B^4}{15\hbar^3 c^3}T^4 = aT^4
$$

where $a = \pi^2 k_B^4/(15\hbar^3 c^3)$ is the radiation constant. The Stefan-Boltzmann law $j = \sigma T^4$ (radiated power per area) follows with $\sigma = ac/4$.

</details>

---

### Example 8.2 — Fermi-Dirac Distribution → Fermi Energy and Fermi Temperature

**Problem.** For a free electron gas in a metal: (a) Derive the density of states $g(\epsilon)$. (b) At $T = 0$, derive the Fermi energy $\epsilon_F$ in terms of electron density $n$. (c) Compute the Fermi temperature for aluminum ($n = 18.1\times10^{28}\,\text{m}^{-3}$).

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Part (a): Density of States

For free electrons (mass $m_e$) in volume $V$, the energy levels are:

$$
\epsilon = \frac{\hbar^2 k^2}{2m_e}, \qquad k = |\mathbf{k}|
$$

The number of states with wavevector magnitude between $k$ and $k + dk$:

$$
\text{states} = V\frac{4\pi k^2\,dk}{(2\pi)^3}\times 2 = \frac{Vk^2\,dk}{\pi^2}
$$

(Factor 2 for spin-1/2 degeneracy.)

Convert to energy: $k = \sqrt{2m_e\epsilon}/\hbar$, $dk = \frac{1}{\hbar}\sqrt{\frac{m_e}{2\epsilon}}\,d\epsilon$:

$$
g(\epsilon)\,d\epsilon = \frac{V}{\pi^2}\cdot\frac{2m_e\epsilon}{\hbar^2}\cdot\frac{1}{\hbar}\sqrt{\frac{m_e}{2\epsilon}}\,d\epsilon = \frac{V}{2\pi^2}\left(\frac{2m_e}{\hbar^2}\right)^{3/2}\sqrt{\epsilon}\,d\epsilon
$$

$$
\boxed{g(\epsilon) = \frac{V}{2\pi^2}\left(\frac{2m_e}{\hbar^2}\right)^{3/2}\sqrt{\epsilon}}
$$

The density of states grows as $\sqrt{\epsilon}$ — a consequence of the 3D parabolic dispersion relation.

#### Part (b): Fermi Energy at $T = 0$

At $T = 0$, the Fermi-Dirac distribution becomes a step function:

$$
f(\epsilon) = \begin{cases} 1 & \epsilon \lt  \epsilon_F \\ 0 & \epsilon \gt  \epsilon_F \end{cases}
$$

All states below $\epsilon_F$ are filled; all above are empty. The total number of electrons:

$$
N = \int_0^{\epsilon_F} g(\epsilon)\,d\epsilon = \frac{V}{2\pi^2}\left(\frac{2m_e}{\hbar^2}\right)^{3/2}\int_0^{\epsilon_F}\sqrt{\epsilon}\,d\epsilon
$$

$$
= \frac{V}{2\pi^2}\left(\frac{2m_e}{\hbar^2}\right)^{3/2}\cdot\frac{2}{3}\epsilon_F^{3/2}
$$

Solving for $\epsilon_F$ with $n = N/V$:

$$
n = \frac{1}{3\pi^2}\left(\frac{2m_e}{\hbar^2}\right)^{3/2}\epsilon_F^{3/2}
$$

$$
\epsilon_F^{3/2} = 3\pi^2 n\left(\frac{\hbar^2}{2m_e}\right)^{3/2}
$$

$$
\boxed{\epsilon_F = \frac{\hbar^2}{2m_e}(3\pi^2 n)^{2/3}}
$$

#### Part (c): Aluminum

With $n = 18.1\times10^{28}\,\text{m}^{-3}$:

$$
3\pi^2 n = 3\pi^2 \times 18.1\times10^{28} = 5.36\times10^{30}\,\text{m}^{-3}
$$

$$
(3\pi^2 n)^{2/3} = (5.36\times10^{30})^{2/3} = (5.36)^{2/3}\times10^{20} = 3.06\times10^{20}\,\text{m}^{-2}
$$

$$
\epsilon_F = \frac{(1.055\times10^{-34})^2}{2\times9.109\times10^{-31}}\times3.06\times10^{20} = \frac{1.113\times10^{-68}}{1.822\times10^{-30}}\times3.06\times10^{20}
$$

$$
= 6.11\times10^{-39}\times3.06\times10^{20} = 1.87\times10^{-18}\,\text{J} = 11.7\,\text{eV}
$$

$$
T_F = \frac{\epsilon_F}{k_B} = \frac{1.87\times10^{-18}}{1.381\times10^{-23}} = 135{,}000\,\text{K}
$$

At room temperature: $T/T_F = 300/135000 = 0.0022$. The electron gas in aluminum is extremely degenerate — quantum effects completely dominate.

</details>

---

### Example 8.3 — Degenerate Electron Gas in Metals: Ground State Energy and Pressure

**Problem.** For a free electron gas at $T = 0$: (a) Derive the total ground-state energy $E_0$. (b) Derive the degeneracy pressure. (c) Estimate the bulk modulus of a metal from electron degeneracy pressure alone.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Part (a): Ground-State Energy

At $T = 0$, all states up to $\epsilon_F$ are occupied:

$$
E_0 = \int_0^{\epsilon_F}\epsilon\,g(\epsilon)\,d\epsilon = \frac{V}{2\pi^2}\left(\frac{2m_e}{\hbar^2}\right)^{3/2}\int_0^{\epsilon_F}\epsilon^{3/2}\,d\epsilon
$$

$$
= \frac{V}{2\pi^2}\left(\frac{2m_e}{\hbar^2}\right)^{3/2}\cdot\frac{2}{5}\epsilon_F^{5/2}
$$

Using $N = \frac{V}{3\pi^2}\left(\frac{2m_e}{\hbar^2}\right)^{3/2}\epsilon_F^{3/2}$, we can write:

$$
\frac{V}{2\pi^2}\left(\frac{2m_e}{\hbar^2}\right)^{3/2} = \frac{3N}{2\epsilon_F^{3/2}}
$$

Therefore:

$$
E_0 = \frac{3N}{2\epsilon_F^{3/2}}\cdot\frac{2}{5}\epsilon_F^{5/2} = \frac{3}{5}N\epsilon_F
$$

$$
\boxed{E_0 = \frac{3}{5}N\epsilon_F}
$$

The average energy per electron at $T = 0$ is $\frac{3}{5}\epsilon_F$ — NOT zero! Even at absolute zero, the electrons have enormous kinetic energy due to the Pauli exclusion principle forcing them into higher energy states.

#### Part (b): Degeneracy Pressure

The pressure at $T = 0$:

$$
P = -\left(\frac{\partial E_0}{\partial V}\right)_N
$$

Since $\epsilon_F = \frac{\hbar^2}{2m_e}(3\pi^2 N/V)^{2/3} \propto V^{-2/3}$:

$$
E_0 = \frac{3}{5}N\cdot\frac{\hbar^2}{2m_e}(3\pi^2)^{2/3}\left(\frac{N}{V}\right)^{2/3} \propto V^{-2/3}
$$

$$
\frac{\partial E_0}{\partial V} = E_0\cdot\left(-\frac{2}{3V}\right) = -\frac{2E_0}{3V}
$$

$$
P = -\left(-\frac{2E_0}{3V}\right) = \frac{2E_0}{3V} = \frac{2}{3}\cdot\frac{3}{5}n\epsilon_F = \frac{2}{5}n\epsilon_F
$$

$$
\boxed{P_{\text{deg}} = \frac{2}{5}n\epsilon_F = \frac{(3\pi^2)^{2/3}\hbar^2}{5m_e}n^{5/3}}
$$

This is the **electron degeneracy pressure** — it exists even at $T = 0$ and is what prevents white dwarf stars from gravitational collapse.

#### Part (c): Bulk Modulus

The bulk modulus $B = -V(\partial P/\partial V)_N$. Since $P \propto n^{5/3} \propto V^{-5/3}$:

$$
\frac{\partial P}{\partial V} = P\cdot\left(-\frac{5}{3V}\right)
$$

$$
B = -V\cdot P\cdot\left(-\frac{5}{3V}\right) = \frac{5P}{3} = \frac{5}{3}\cdot\frac{2}{5}n\epsilon_F = \frac{2}{3}n\epsilon_F
$$

For copper ($n = 8.49\times10^{28}\,\text{m}^{-3}$, $\epsilon_F = 7.04\,\text{eV} = 1.13\times10^{-18}\,\text{J}$):

$$
B = \frac{2}{3}\times8.49\times10^{28}\times1.13\times10^{-18} = 6.4\times10^{10}\,\text{Pa} = 64\,\text{GPa}
$$

Experimental bulk modulus of copper: $B = 140\,\text{GPa}$. The electron degeneracy pressure accounts for roughly half — the rest comes from ion-ion interactions and electron-ion bonding. This is remarkably good for such a simple model.

</details>

---

### Example 8.4 — Bose-Einstein Condensation: Critical Temperature and Condensate Fraction

**Problem.** For an ideal Bose gas of $N$ particles (mass $m$, spin 0) in volume $V$: (a) Derive the critical temperature $T_c$ for BEC. (b) Find the condensate fraction $N_0/N$ as a function of $T/T_c$ for $T < T_c$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Part (a): Critical Temperature

The total number of particles in excited states ($\epsilon \gt  0$) is:

$$
N_{\text{ex}} = \int_0^\infty \frac{g(\epsilon)}{e^{(\epsilon-\mu)/(k_BT)} - 1}\,d\epsilon
$$

For a 3D free particle: $g(\epsilon) = \frac{V}{4\pi^2}\left(\frac{2m}{\hbar^2}\right)^{3/2}\sqrt{\epsilon}$ (no spin factor for spin-0).

BEC occurs when $\mu \to 0^-$ (chemical potential reaches the ground state energy). At $T = T_c$, all $N$ particles are just barely accommodated in excited states with $\mu = 0$:

$$
N = \frac{V}{4\pi^2}\left(\frac{2m}{\hbar^2}\right)^{3/2}\int_0^\infty\frac{\sqrt{\epsilon}}{e^{\epsilon/(k_BT_c)} - 1}\,d\epsilon
$$

Substitute $x = \epsilon/(k_BT_c)$:

$$
N = \frac{V}{4\pi^2}\left(\frac{2mk_BT_c}{\hbar^2}\right)^{3/2}\int_0^\infty\frac{\sqrt{x}}{e^x - 1}\,dx
$$

The integral is $\int_0^\infty x^{1/2}/(e^x-1)\,dx = \Gamma(3/2)\zeta(3/2) = \frac{\sqrt{\pi}}{2}\times 2.612$:

$$
N = \frac{V}{4\pi^2}\left(\frac{2mk_BT_c}{\hbar^2}\right)^{3/2}\cdot\frac{\sqrt{\pi}}{2}\cdot\zeta(3/2)
$$

Simplifying with $\lambda_c = h/\sqrt{2\pi mk_BT_c}$ (thermal wavelength at $T_c$):

$$
n = N/V = \frac{\zeta(3/2)}{\lambda_c^3}
$$

Solving for $T_c$:

$$
\lambda_c^3 = \frac{\zeta(3/2)}{n} \implies \frac{h^3}{(2\pi mk_BT_c)^{3/2}} = \frac{\zeta(3/2)}{n}
$$

$$
\boxed{T_c = \frac{2\pi\hbar^2}{mk_B}\left(\frac{n}{\zeta(3/2)}\right)^{2/3}} \quad \text{where } \zeta(3/2) \approx 2.612
$$

**Physical interpretation:** BEC occurs when the thermal de Broglie wavelength $\lambda$ becomes comparable to the inter-particle spacing $n^{-1/3}$: $n\lambda^3 \sim \zeta(3/2) \sim 1$. At this point, the wave packets of individual particles overlap and quantum coherence effects become macroscopic.

#### Part (b): Condensate Fraction Below $T_c$

For $T \lt  T_c$, the chemical potential remains pinned at $\mu = 0$ (to within $O(1/N)$). The number of particles in excited states scales as:

$$
N_{\text{ex}}(T) = N\left(\frac{T}{T_c}\right)^{3/2}
$$

(This follows because $N_{\text{ex}} \propto T^{3/2}$ from the integral, and $N_{\text{ex}}(T_c) = N$ by definition.)

The number in the ground state (the condensate):

$$
N_0 = N - N_{\text{ex}} = N\left[1 - \left(\frac{T}{T_c}\right)^{3/2}\right]
$$

$$
\boxed{\frac{N_0}{N} = 1 - \left(\frac{T}{T_c}\right)^{3/2}} \quad (T \leq T_c)
$$

At $T = 0$: $N_0/N = 1$ (all particles in ground state). At $T = T_c$: $N_0/N = 0$ (condensate vanishes). The transition is continuous (second-order phase transition).

</details>



---

## 📘 9. Appendix: Extended Derivations & Special Cases

### Appendix 9.1 — The Sommerfeld Expansion: Low-Temperature Properties of Fermi Systems

The Sommerfeld expansion is a systematic method for computing thermodynamic properties of a Fermi gas at low temperatures ($T \ll T_F$). It exploits the fact that the Fermi-Dirac distribution is nearly a step function, with deviations confined to a narrow window of width $\sim k_BT$ around $\epsilon_F$.

**The general problem.** We need to evaluate integrals of the form:

$$
I = \int_0^\infty \phi(\epsilon)\,f(\epsilon)\,d\epsilon = \int_0^\infty \frac{\phi(\epsilon)}{e^{(\epsilon-\mu)/(k_BT)} + 1}\,d\epsilon
$$

where $\phi(\epsilon)$ is a smooth function (e.g., $g(\epsilon)$ or $\epsilon\,g(\epsilon)$).

**Step 1: Integration by parts.** Define $\Phi(\epsilon) = \int_0^\epsilon \phi(\epsilon')\,d\epsilon'$. Then:

$$
I = -\int_0^\infty \Phi(\epsilon)\frac{\partial f}{\partial\epsilon}\,d\epsilon
$$

The key insight: $-\partial f/\partial\epsilon$ is a sharply peaked function centered at $\epsilon = \mu$ with width $\sim k_BT$. It acts like a broadened delta function.

**Step 2: Taylor expand $\Phi(\epsilon)$ around $\epsilon = \mu$.**

$$
\Phi(\epsilon) = \Phi(\mu) + (\epsilon-\mu)\Phi'(\mu) + \frac{(\epsilon-\mu)^2}{2}\Phi''(\mu) + \cdots
$$

$$
= \Phi(\mu) + (\epsilon-\mu)\phi(\mu) + \frac{(\epsilon-\mu)^2}{2}\phi'(\mu) + \cdots
$$

**Step 3: Evaluate the moments.** Substitute $x = (\epsilon-\mu)/(k_BT)$:

$$
-\frac{\partial f}{\partial\epsilon} = \frac{1}{k_BT}\frac{e^x}{(e^x+1)^2}
$$

The moments are:

$$
\int_{-\infty}^{\infty} x^n \frac{e^x}{(e^x+1)^2}\,dx = \begin{cases} 1 & n=0 \\ 0 & n=1 \text{ (odd)} \\ \pi^2/3 & n=2 \\ 0 & n=3 \text{ (odd)} \\ 7\pi^4/15 & n=4 \end{cases}
$$

**Step 4: The Sommerfeld expansion.**

$$
\boxed{I = \int_0^\mu \phi(\epsilon)\,d\epsilon + \frac{\pi^2}{6}(k_BT)^2\phi'(\mu) + \frac{7\pi^4}{360}(k_BT)^4\phi''(\mu) + O(T^6)}
$$

**Application: Electronic heat capacity.**

The total energy is $E = \int_0^\infty \epsilon\,g(\epsilon)\,f(\epsilon)\,d\epsilon$. With $\phi(\epsilon) = \epsilon\,g(\epsilon)$:

$$
E = \int_0^\mu \epsilon\,g(\epsilon)\,d\epsilon + \frac{\pi^2}{6}(k_BT)^2[\mu g(\mu) + g(\mu)] + \cdots
$$

To leading order, $\mu \approx \epsilon_F$ (the chemical potential shifts only at order $T^2$):

$$
E \approx E_0 + \frac{\pi^2}{6}(k_BT)^2 g(\epsilon_F)\epsilon_F + \frac{\pi^2}{6}(k_BT)^2 g(\epsilon_F)
$$

Actually, the careful calculation gives:

$$
E = E_0 + \frac{\pi^2}{6}(k_BT)^2 g(\epsilon_F) + O(T^4)
$$

where $E_0 = \frac{3}{5}N\epsilon_F$ is the ground-state energy. The heat capacity:

$$
C_V = \frac{\partial E}{\partial T} = \frac{\pi^2}{3}k_B^2 T\,g(\epsilon_F)
$$

For the free electron gas, $g(\epsilon_F) = 3N/(2\epsilon_F)$:

$$
\boxed{C_V = \frac{\pi^2}{2}Nk_B\frac{T}{T_F} = \gamma T}
$$

where $\gamma = \pi^2 Nk_B/(2T_F)$ is the Sommerfeld coefficient. This linear-$T$ electronic heat capacity is the dominant contribution at very low temperatures (below a few Kelvin), where the phonon $T^3$ contribution is negligible.

**Experimental verification:** The total low-$T$ heat capacity of metals is:

$$
C_V = \gamma T + AT^3
$$

Plotting $C_V/T$ vs $T^2$ gives a straight line with intercept $\gamma$ (electronic) and slope $A$ (phononic). This is one of the most precise confirmations of Fermi-Dirac statistics.

**Chemical potential shift:** The Sommerfeld expansion also gives:

$$
\mu(T) = \epsilon_F\left[1 - \frac{\pi^2}{12}\left(\frac{T}{T_F}\right)^2 + O(T^4)\right]
$$

The chemical potential decreases slightly with temperature as thermal excitations spread electrons above $\epsilon_F$.

**Reference:** Kittel & Kroemer, *Thermal Physics*, Ch. 7; Ashcroft & Mermin, *Solid State Physics*, Ch. 2; David Tong, *Statistical Mechanics* Notes §5.

---

### Appendix 9.2 — Black-Body Radiation: From Planck to Stefan-Boltzmann

The theory of black-body radiation was the historical birthplace of quantum mechanics. Here we collect the key results derived from the photon Bose-Einstein distribution.

**The fundamental quantities:**

1. **Spectral energy density** (energy per volume per frequency):

$$
u(\nu) = \frac{8\pi h\nu^3}{c^3}\cdot\frac{1}{e^{h\nu/(k_BT)} - 1}
$$

or in terms of angular frequency $\omega = 2\pi\nu$:

$$
u(\omega) = \frac{\hbar\omega^3}{\pi^2 c^3}\cdot\frac{1}{e^{\hbar\omega/(k_BT)} - 1}
$$

2. **Total energy density** (Stefan-Boltzmann):

$$
u = \int_0^\infty u(\omega)\,d\omega = \frac{\pi^2 k_B^4}{15\hbar^3 c^3}T^4 = aT^4
$$

where $a = 4\sigma/c$ and $\sigma = 5.67\times10^{-8}\,\text{W/(m}^2\text{·K}^4)$ is the Stefan-Boltzmann constant.

3. **Wien's displacement law** (peak of $u(\omega)$):

$$
\hbar\omega_{\max} = 2.822\,k_BT
$$

In wavelength: $\lambda_{\max}T = 2.898\times10^{-3}\,\text{m·K}$.

4. **Radiation pressure:**

$$
P = \frac{u}{3} = \frac{a T^4}{3}
$$

(The factor 1/3 comes from the isotropic angular distribution of photons.)

5. **Entropy of radiation:**

$$
S = \frac{4}{3}aVT^3
$$

(From $dU = TdS - PdV$ with $U = aVT^4$ and $P = aT^4/3$.)

6. **Photon number density:**

$$
n_\gamma = \frac{2\zeta(3)}{\pi^2}\left(\frac{k_BT}{\hbar c}\right)^3 \approx 20.3\left(\frac{T}{1\,\text{K}}\right)^3\,\text{cm}^{-3}
$$

**Cosmic Microwave Background:** The CMB is a nearly perfect black body at $T = 2.725\,\text{K}$, giving $n_\gamma \approx 411\,\text{photons/cm}^3$ and $u \approx 4.2\times10^{-14}\,\text{J/m}^3$. Wien's law gives $\lambda_{\max} = 1.06\,\text{mm}$ (microwave).

**Reference:** Planck, "On the Law of Distribution of Energy in the Normal Spectrum" (1901); Kittel & Kroemer, *Thermal Physics*, Ch. 4; Pathria & Beale, Ch. 7.

---

### Appendix 9.3 — White Dwarfs and Neutron Stars: Astrophysical Applications of Quantum Statistics

The degeneracy pressure of fermions (electrons or neutrons) supports compact stellar remnants against gravitational collapse. This is a dramatic macroscopic manifestation of the Pauli exclusion principle.

**White dwarfs (electron degeneracy):**

A white dwarf is supported by electron degeneracy pressure. The condition for hydrostatic equilibrium:

$$
\frac{dP}{dr} = -\frac{G M(r)\rho}{r^2}
$$

For a non-relativistic degenerate electron gas: $P \propto n_e^{5/3} \propto \rho^{5/3}$. Dimensional analysis gives the mass-radius relation:

$$
R \propto M^{-1/3}
$$

More massive white dwarfs are SMALLER (unlike normal stars). This is because higher mass requires higher central density, which means higher Fermi energy and more compact packing.

**The Chandrasekhar limit:** When $\epsilon_F \sim m_e c^2$ (electrons become relativistic), the equation of state softens to $P \propto n_e^{4/3} \propto \rho^{4/3}$. In this regime, the star can no longer support itself above a critical mass:

$$
M_{\text{Ch}} \approx 1.44\,M_\odot\left(\frac{2}{A/Z}\right)^2
$$

where $A/Z$ is the mass-to-charge ratio of the ions (= 2 for carbon/oxygen white dwarfs). Above this mass, the white dwarf collapses to a neutron star or black hole.

**Neutron stars (neutron degeneracy):**

When a white dwarf exceeds the Chandrasekhar limit, electrons are captured by protons ($e^- + p \to n + \nu_e$), converting the star to neutrons. The neutron degeneracy pressure then supports the star. Since $m_n \approx 1836\,m_e$, the Fermi energy for the same density is much lower, and the star is much more compact:

$$
R_{\text{NS}} \sim 10\,\text{km}, \qquad \rho \sim 10^{17}\,\text{kg/m}^3
$$

The maximum mass for a neutron star (Tolman-Oppenheimer-Volkoff limit) is $\sim 2$–$3\,M_\odot$, above which collapse to a black hole is inevitable.

**The deep connection:** These astrophysical objects are macroscopic quantum systems. A white dwarf is essentially a giant atom — a Fermi gas at zero temperature (since $T \sim 10^7\,\text{K} \ll T_F \sim 10^9\,\text{K}$). The structure of the universe on the largest scales is determined by the Pauli exclusion principle operating on the smallest scales.

**Reference:** Chandrasekhar, "The Maximum Mass of Ideal White Dwarfs" (1931); Kittel & Kroemer, *Thermal Physics*, Ch. 7; Shapiro & Teukolsky, *Black Holes, White Dwarfs, and Neutron Stars*.

---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

*Previous: [5.7 - Maxwell-Boltzmann Distribution & Kinetic Theory](5.7---Maxwell-Boltzmann-Distribution-&-Kinetic-Theory) | Next: [5.9 - Advanced Topics](5.9---Advanced-Topics)*
