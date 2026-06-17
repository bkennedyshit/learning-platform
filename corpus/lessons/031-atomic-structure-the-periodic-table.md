---
title: "03.1 — Atomic Structure & The Periodic Table"
subject: "Chemistry"
catalog: advanced
audience_tier: higher-education
chapter: "03.1"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 03.1 — Atomic Structure & The Periodic Table

> *"The elements, if arranged according to their atomic weights, exhibit an apparent periodicity of properties."* — Dmitri Mendeleev, 1869

> *"If you want to understand chemistry, you must first understand quantum mechanics."* — Linus Pauling

You already solved the hydrogen atom in [9.4 - Angular Momentum, Spin & Fine Structure](9.4---Angular-Momentum,-Spin-&-Fine-Structure). You know that electron states are labeled by quantum numbers $(n, \ell, m_\ell, m_s)$. This chapter takes that knowledge and builds the **entire periodic table** from it. Chemistry is not memorization — it is the logical consequence of quantum mechanics applied to multi-electron atoms.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Derive the allowed quantum numbers $(n, \ell, m_\ell, m_s)$ and explain their physical meaning.
2. Write electron configurations for any element using the Aufbau principle, Hund's rule, and the Pauli exclusion principle.
3. Explain the shape of the periodic table as a direct consequence of orbital filling order.
4. Calculate effective nuclear charge $Z_{\text{eff}}$ using Slater's rules.
5. Predict periodic trends (atomic radius, ionization energy, electronegativity, electron affinity) from $Z_{\text{eff}}$.
6. Connect orbital shapes (s, p, d, f) to the angular momentum quantum number $\ell$ from your QM studies.
7. Explain why the 4s orbital fills before 3d (the $(n + \ell)$ rule and shielding).

---

## 🖼️ Visual Anchor — Quantum Numbers to Periodic Table

![chem-03__fig1](chem-03__fig1.svg)

---

## 📚 1. Definitions

### Definition 03.1.1 — Atomic Number ($Z$)

The **atomic number** $Z$ is the number of protons in the nucleus. It uniquely identifies an element and determines its chemical properties (because it determines the number of electrons in a neutral atom).

### Definition 03.1.2 — Quantum Numbers

Each electron in an atom is described by four quantum numbers:

| Quantum Number | Symbol | Allowed Values | Physical Meaning |
|---|---|---|---|
| Principal | $n$ | $1, 2, 3, \ldots$ | Energy level (shell); determines size |
| Angular momentum | $\ell$ | $0, 1, 2, \ldots, n-1$ | Orbital shape; subshell (s, p, d, f) |
| Magnetic | $m_\ell$ | $-\ell, \ldots, 0, \ldots, +\ell$ | Orbital orientation in space |
| Spin | $m_s$ | $+\frac{1}{2}, -\frac{1}{2}$ | Intrinsic angular momentum direction |

### Definition 03.1.3 — Electron Configuration

The **electron configuration** specifies the distribution of electrons among orbitals. Notation: $n\ell^k$ where $k$ is the number of electrons in that subshell.

Example: Carbon ($Z = 6$): $1s^2\,2s^2\,2p^2$.

### Definition 03.1.4 — Effective Nuclear Charge ($Z_{\text{eff}}$)

$$
Z_{\text{eff}} = Z - \sigma
$$

where $\sigma$ is the **shielding constant** — the degree to which inner electrons screen the nuclear charge from outer electrons.

### Definition 03.1.5 — Ionization Energy (IE)

The minimum energy required to remove the most loosely bound electron from a gaseous atom:

$$
\text{IE} = E(\text{ion}) - E(\text{atom})
$$

### Definition 03.1.6 — Electronegativity ($\chi$)

A measure of an atom's ability to attract bonding electrons. Pauling scale: $\chi_F = 4.0$ (most electronegative), $\chi_{Cs} = 0.7$ (least).

### Definition 03.1.7 — Orbital Degeneracy

Orbitals with the same energy are **degenerate**. In hydrogen, all orbitals with the same $n$ are degenerate ($E_n = -13.6/n^2$ eV). In multi-electron atoms, this degeneracy is broken: $E$ depends on both $n$ and $\ell$.

---

## 📐 2. Mathematical Foundations

### 2.1 The Hydrogen Atom Solution (Review from [9.4 - Angular Momentum, Spin & Fine Structure](9.4---Angular-Momentum,-Spin-&-Fine-Structure))

The time-independent Schrödinger equation for hydrogen:

$$
\hat{H}\psi = E\psi, \quad \hat{H} = -\frac{\hbar^2}{2m_e}\nabla^2 - \frac{e^2}{4\pi\epsilon_0 r}
$$

Solutions: $\psi_{n\ell m}(r, \theta, \phi) = R_{n\ell}(r) \cdot Y_\ell^m(\theta, \phi)$

where $Y_\ell^m$ are the spherical harmonics you studied in Track 09, and $R_{n\ell}$ are the radial wavefunctions.

**Energy eigenvalues (hydrogen-like):**

$$
E_n = -\frac{Z^2 \cdot 13.6 \text{ eV}}{n^2} = -\frac{Z^2 e^4 m_e}{2\hbar^2 n^2(4\pi\epsilon_0)^2}
$$

### 2.2 Multi-Electron Atoms: The Central Field Approximation

For atoms with $N > 1$ electrons, the exact Hamiltonian is:

$$
\hat{H} = \sum_{i=1}^N \left[-\frac{\hbar^2}{2m_e}\nabla_i^2 - \frac{Ze^2}{4\pi\epsilon_0 r_i}\right] + \sum_{i<j}\frac{e^2}{4\pi\epsilon_0 r_{ij}}
$$

The electron-electron repulsion term $\sum_{i<j} e^2/(4\pi\epsilon_0 r_{ij})$ makes this unsolvable analytically. The **central field approximation** replaces the exact electron-electron interaction with an average spherically symmetric potential $V_{\text{eff}}(r)$:

$$
V_{\text{eff}}(r) \approx -\frac{Z_{\text{eff}}(r) \cdot e^2}{4\pi\epsilon_0 r}
$$

This breaks the $\ell$-degeneracy: electrons with lower $\ell$ penetrate closer to the nucleus (less shielded), so they have lower energy.

### 2.3 Slater's Rules for $Z_{\text{eff}}$

To estimate $Z_{\text{eff}}$ for an electron in a given orbital:

1. Write the electron configuration in groups: $(1s)(2s,2p)(3s,3p)(3d)(4s,4p)(4d)(4f)\ldots$
2. Electrons in groups to the RIGHT contribute $\sigma = 0$.
3. Electrons in the SAME group contribute $\sigma = 0.35$ (except 1s: $\sigma = 0.30$).
4. For $ns$ or $np$ electrons: each electron in the $(n-1)$ shell contributes $\sigma = 0.85$; each electron in shells below that contributes $\sigma = 1.00$.
5. For $nd$ or $nf$ electrons: each electron in any lower group contributes $\sigma = 1.00$.

**Example:** Oxygen ($Z = 8$), configuration $1s^2\,2s^2\,2p^4$. For a 2p electron:

$$
\sigma = 5 \times 0.35 + 2 \times 0.85 = 1.75 + 1.70 = 3.45
$$

$$
Z_{\text{eff}} = 8 - 3.45 = 4.55
$$

### 2.4 The $(n + \ell)$ Rule (Madelung's Rule)

Orbitals fill in order of increasing $(n + \ell)$. For equal $(n + \ell)$, lower $n$ fills first:

$$
1s < 2s < 2p < 3s < 3p < 4s < 3d < 4p < 5s < 4d < \ldots
$$

**Why?** Lower-$\ell$ orbitals have greater nuclear penetration (the radial wavefunction $R_{n\ell}(r)$ has more probability density near $r = 0$ for lower $\ell$), so they experience a larger $Z_{\text{eff}}$ and are stabilized.

### 2.5 Orbital Capacity

Each subshell $\ell$ contains $2\ell + 1$ orbitals (one for each $m_\ell$), each holding 2 electrons (spin up and down):

$$
\text{Max electrons in subshell } \ell = 2(2\ell + 1)
$$

| Subshell | $\ell$ | Orbitals | Max electrons |
|---|---|---|---|
| s | 0 | 1 | 2 |
| p | 1 | 3 | 6 |
| d | 2 | 5 | 10 |
| f | 3 | 7 | 14 |

**Total electrons in shell $n$:** $\sum_{\ell=0}^{n-1} 2(2\ell+1) = 2n^2$.

---

## 🔬 3. Chemical Mechanisms

### 3.1 The Three Rules of Electron Configuration

**Rule 1: Aufbau Principle** — Electrons fill orbitals from lowest energy to highest (following the $(n+\ell)$ rule).

**Rule 2: Pauli Exclusion Principle** — No two electrons in an atom can have the same set of four quantum numbers $(n, \ell, m_\ell, m_s)$. This is why each orbital holds at most 2 electrons (with opposite spins).

*Mathematical statement:* The total wavefunction of a multi-electron system must be antisymmetric under exchange of any two electrons:

$$
\Psi(\ldots, \mathbf{r}_i, \ldots, \mathbf{r}_j, \ldots) = -\Psi(\ldots, \mathbf{r}_j, \ldots, \mathbf{r}_i, \ldots)
$$

This is enforced by the Slater determinant (which you know from [2.5 - Determinants & Cramer's Rule](2.5---Determinants-&-Cramer's-Rule)):

$$
\Psi = \frac{1}{\sqrt{N!}}\begin{vmatrix} \phi_1(\mathbf{r}_1) & \phi_2(\mathbf{r}_1) & \cdots \\ \phi_1(\mathbf{r}_2) & \phi_2(\mathbf{r}_2) & \cdots \\ \vdots & & \ddots \end{vmatrix}
$$

**Rule 3: Hund's Rule** — For degenerate orbitals, electrons fill singly (with parallel spins) before pairing. This minimizes electron-electron repulsion and maximizes exchange energy.

### 3.2 Building the Periodic Table

The periodic table's structure follows directly from orbital filling:

| Block | Orbitals Filling | Elements per Period |
|---|---|---|
| s-block | $ns$ | 2 (Groups 1–2) |
| p-block | $np$ | 6 (Groups 13–18) |
| d-block | $(n-1)d$ | 10 (Groups 3–12, transition metals) |
| f-block | $(n-2)f$ | 14 (Lanthanides, Actinides) |

**Period lengths:** 2, 8, 8, 18, 18, 32, 32 — these are exactly $2n^2$ for the shells being filled.

### 3.3 Exceptions to Aufbau

Chromium ($Z = 24$): Expected $[Ar]\,3d^4\,4s^2$, actual $[Ar]\,3d^5\,4s^1$.
Copper ($Z = 29$): Expected $[Ar]\,3d^9\,4s^2$, actual $[Ar]\,3d^{10}\,4s^1$.

**Why?** Half-filled and fully-filled $d$ subshells have extra stability due to maximized exchange energy. The energy gained from exchange stabilization exceeds the energy cost of promoting one $4s$ electron to $3d$.

### 3.4 Periodic Trends and Their QM Origin

| Trend | Across a Period (→) | Down a Group (↓) | QM Explanation |
|---|---|---|---|
| Atomic radius | Decreases | Increases | $Z_{\text{eff}}$ increases → tighter orbitals; new shell → larger $n$ |
| Ionization energy | Increases | Decreases | Higher $Z_{\text{eff}}$ → harder to remove; larger $n$ → easier |
| Electronegativity | Increases | Decreases | Same as IE trend |
| Electron affinity | Generally increases | Generally decreases | Approaching noble gas config |

---

## ✍️ 4. Worked Examples

### Example 03.1.1 — Electron Configuration of Iron (Fe, $Z = 26$)

**Problem:** Write the full and condensed electron configuration of iron. Identify the number of unpaired electrons.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Apply the Aufbau principle (filling order):

$$
1s^2\,2s^2\,2p^6\,3s^2\,3p^6\,4s^2\,3d^6
$$

**Step 2:** Condensed notation using the nearest noble gas core:

$$
\text{Fe}: [Ar]\,3d^6\,4s^2
$$

**Step 3:** Apply Hund's rule to the $3d$ subshell (5 orbitals, 6 electrons):

$$
\uparrow\downarrow \quad \uparrow \quad \uparrow \quad \uparrow \quad \uparrow
$$

One orbital is doubly occupied; four have single electrons.

**Step 4:** Count unpaired electrons: **4 unpaired electrons**.

This makes iron paramagnetic (attracted to magnetic fields), which is experimentally confirmed.

**Verification:** Total electrons = $2 + 2 + 6 + 2 + 6 + 2 + 6 = 26 = Z$. ✓

</details>

---

### Example 03.1.2 — Calculating $Z_{\text{eff}}$ for a 3p Electron in Chlorine

**Problem:** Use Slater's rules to calculate $Z_{\text{eff}}$ experienced by a 3p electron in Cl ($Z = 17$).

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Write the configuration in Slater groups:

$$
(1s^2)(2s^2\,2p^6)(3s^2\,3p^5)
$$

**Step 2:** For a 3p electron, identify contributions to $\sigma$:

- Same group $(3s, 3p)$: 6 other electrons × 0.35 = 2.10
- $(n-1)$ shell $(2s, 2p)$: 8 electrons × 0.85 = 6.80
- Lower shells $(1s)$: 2 electrons × 1.00 = 2.00

**Step 3:** Calculate:

$$
\sigma = 2.10 + 6.80 + 2.00 = 10.90
$$

$$
Z_{\text{eff}} = 17 - 10.90 = 6.10
$$

**Interpretation:** A 3p electron in chlorine "sees" an effective nuclear charge of about +6.1, not the full +17. This is why chlorine has high electronegativity — $Z_{\text{eff}} = 6.10$ is large for a period 3 element, pulling electrons strongly toward the nucleus.

**Comparison:** Sodium ($Z = 11$) 3s electron: $\sigma = 0 \times 0.35 + 8 \times 0.85 + 2 \times 1.00 = 8.80$, so $Z_{\text{eff}} = 2.20$. Much weaker hold on its valence electron → easily ionized.

</details>

---

### Example 03.1.3 — Why Does the Periodic Table Have Its Shape?

**Problem:** Explain why Period 4 has 18 elements while Period 2 has only 8.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Period 2 fills the $n = 2$ shell:
- $2s$: 2 electrons
- $2p$: 6 electrons
- Total: 8 elements (Li through Ne)

**Step 2:** Period 4 fills:
- $4s$: 2 electrons (K, Ca)
- $3d$: 10 electrons (Sc through Zn — the transition metals)
- $4p$: 6 electrons (Ga through Kr)
- Total: 18 elements

**Step 3:** The $3d$ subshell becomes available because $n = 3$ allows $\ell = 0, 1, 2$. But $3d$ fills AFTER $4s$ because of the $(n + \ell)$ rule:
- $4s$: $n + \ell = 4 + 0 = 4$
- $3d$: $n + \ell = 3 + 2 = 5$

So $4s$ is lower in energy than $3d$ (due to greater nuclear penetration of the $s$ orbital).

**Step 4:** The pattern continues:
- Period 5: 18 elements ($5s + 4d + 5p$)
- Period 6: 32 elements ($6s + 4f + 5d + 6p$) — the lanthanides appear because $4f$ ($\ell = 3$) finally fills

**The deep answer:** The periodic table's shape is a direct map of the quantum numbers. Each block corresponds to an $\ell$ value, and the width of each block is $2(2\ell + 1)$: s-block = 2, p-block = 6, d-block = 10, f-block = 14.

</details>

---

### Example 03.1.4 — Predicting Ionization Energy Trends

**Problem:** Rank the following in order of increasing first ionization energy: Na, Mg, Al, Si, P.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Write configurations:
- Na: $[Ne]\,3s^1$
- Mg: $[Ne]\,3s^2$
- Al: $[Ne]\,3s^2\,3p^1$
- Si: $[Ne]\,3s^2\,3p^2$
- P: $[Ne]\,3s^2\,3p^3$

**Step 2:** General trend across Period 3: IE increases left → right (increasing $Z_{\text{eff}}$).

**Step 3:** But there's an anomaly: Al has LOWER IE than Mg.

**Why?** Mg removes a $3s$ electron (well-shielded by the full $2p$ shell). Al removes a $3p$ electron, which is higher in energy and easier to remove despite the higher $Z$.

**Step 4:** Another subtle point: P has a half-filled $3p^3$ configuration (extra stability from exchange energy), but this effect is small compared to the $Z_{\text{eff}}$ trend.

**Final ranking:** Na < Al < Mg < Si < P

**Numerical values (eV):** Na (5.14) < Al (5.99) < Mg (7.65) < Si (8.15) < P (10.49)

Note the Mg > Al reversal — this is a classic exam question that trips up students who only memorize "IE increases across a period."

</details>

---

### Example 03.1.5 — Connecting to Quantum Mechanics: Orbital Shapes

**Problem:** Using your knowledge from [9.4 - Angular Momentum, Spin & Fine Structure](9.4---Angular-Momentum,-Spin-&-Fine-Structure), explain why a $p$ orbital has a dumbbell shape while an $s$ orbital is spherical.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Recall the spherical harmonics $Y_\ell^m(\theta, \phi)$:

- $\ell = 0$ (s orbital): $Y_0^0 = \frac{1}{\sqrt{4\pi}}$ — no angular dependence → spherically symmetric.

- $\ell = 1$ (p orbitals): 
  - $Y_1^0 = \sqrt{\frac{3}{4\pi}}\cos\theta$ — the $p_z$ orbital
  - $Y_1^{\pm 1} = \mp\sqrt{\frac{3}{8\pi}}\sin\theta\,e^{\pm i\phi}$ — combine to get $p_x$ and $p_y$

**Step 2:** The probability density $|\psi|^2 \propto |Y_\ell^m|^2$:

- For $p_z$: $|Y_1^0|^2 \propto \cos^2\theta$ — maximum along $z$-axis, zero in the $xy$-plane → dumbbell shape.

**Step 3:** The angular momentum quantum number $\ell$ determines the number of angular nodes:
- $s$ ($\ell = 0$): 0 angular nodes → spherical
- $p$ ($\ell = 1$): 1 angular node (a nodal plane) → two lobes
- $d$ ($\ell = 2$): 2 angular nodes → four lobes (or donut + lobes)
- $f$ ($\ell = 3$): 3 angular nodes → complex multi-lobed shapes

**Step 4:** Total nodes = $n - 1$. Radial nodes = $n - \ell - 1$. Angular nodes = $\ell$.

For a $3p$ orbital: total nodes = 2, angular nodes = 1, radial nodes = 1. So the dumbbell has one spherical node cutting through each lobe.

**The key insight:** Orbital shapes are NOT arbitrary chemistry facts to memorize. They are the angular parts of the hydrogen wavefunction — the spherical harmonics you already studied. Chemistry just gives them names (s, p, d, f) and fills them with electrons.

</details>

---

## 🧠 5. Connections to Other Tracks

| This Chapter | Connects To | How |
|---|---|---|
| Quantum numbers $(n, \ell, m_\ell, m_s)$ | [9.4 - Angular Momentum, Spin & Fine Structure](9.4---Angular-Momentum,-Spin-&-Fine-Structure) | Orbital quantum numbers ARE angular momentum eigenvalues |
| Slater determinant | [2.5 - Determinants & Cramer's Rule](2.5---Determinants-&-Cramer's-Rule) | Antisymmetric wavefunctions use determinants |
| Spherical harmonics | [9.3 - The 1D Infinite Square Well & Harmonic Oscillator](9.3---The-1D-Infinite-Square-Well-&-Harmonic-Oscillator) | Orbital shapes are $Y_\ell^m(\theta, \phi)$ |
| Hydrogen energy levels | [9.4 - Angular Momentum, Spin & Fine Structure](9.4---Angular-Momentum,-Spin-&-Fine-Structure) | $E_n = -13.6/n^2$ eV |
| Electron-electron repulsion | [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy) | Statistical treatment of many-body systems |
| Periodic trends | [03.2 - Chemical Bonding - Ionic, Covalent, Metallic & Intermolecular](03.2---Chemical-Bonding---Ionic,-Covalent,-Metallic-&-Intermolecular) | Electronegativity drives bond type |

---

## ⚠️ 6. Common Misconceptions & Where Most Students Fail

### ❌ Misconception 1: "Electrons orbit the nucleus like planets"

**The truth:** Electrons exist as probability clouds (wavefunctions). There is no trajectory. The "orbital" is a region of space where the electron has >90% probability of being found. You already know this from QM — the wavefunction $\psi$ gives probability amplitude, not position.

**Why students fail here:** High school teaches the Bohr model (circular orbits) as if it's real. It's a useful approximation for energy levels but completely wrong about electron motion.

### ❌ Misconception 2: "Orbitals are just shapes to memorize"

**The truth:** Orbital shapes are the spherical harmonics $Y_\ell^m(\theta, \phi)$ — mathematical functions you can compute. The $p_z$ orbital is literally $\cos\theta$ times a radial function. You don't memorize shapes; you understand the math that generates them.

### ❌ Misconception 3: "4s fills before 3d because 4s has lower energy"

**The nuance:** This is approximately true for neutral atoms during filling, but once the atom is built, the 3d electrons are actually lower in energy than 4s. That's why transition metal ions lose 4s electrons FIRST (e.g., Fe²⁺ is $[Ar]\,3d^6$, not $[Ar]\,3d^4\,4s^2$).

**The real explanation:** The $(n + \ell)$ rule is an approximation. The actual orbital energies depend on $Z_{\text{eff}}$, which changes as electrons are added. It's a self-consistent problem (solved by Hartree-Fock methods).

### ❌ Misconception 4: "The periodic table is just a chart to look things up"

**The truth:** The periodic table IS quantum mechanics. Its shape, its trends, its exceptions — all follow from the Schrödinger equation applied to multi-electron atoms. Once you see this, you never need to "memorize" the table again.

### ❌ Misconception 5: "Electron configurations are arbitrary rules"

**The truth:** The Aufbau principle, Hund's rule, and Pauli exclusion are consequences of:
1. Energy minimization (Aufbau)
2. The antisymmetry requirement for fermions (Pauli) — which you proved in QM
3. Exchange energy maximization (Hund) — a quantum mechanical effect with no classical analogue

### 💪 The Pep Talk

If you failed chemistry before, it was probably because atomic structure was presented as a collection of arbitrary rules: "memorize the filling order," "memorize the exceptions," "memorize the trends." That's not chemistry — that's trivia.

Now you have the QM foundation. You KNOW why $\ell = 1$ gives a dumbbell shape (it's $\cos\theta$). You KNOW why no two electrons can share quantum numbers (antisymmetric wavefunctions). You KNOW why energy depends on $n$ and $\ell$ (shielding breaks the hydrogen degeneracy).

This time, it's not memorization. It's understanding.

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- [9.4 - Angular Momentum, Spin & Fine Structure](9.4---Angular-Momentum,-Spin-&-Fine-Structure) — The QM foundation for this chapter
- [9.3 - The 1D Infinite Square Well & Harmonic Oscillator](9.3---The-1D-Infinite-Square-Well-&-Harmonic-Oscillator) — Bound state quantization
- [2.5 - Determinants & Cramer's Rule](2.5---Determinants-&-Cramer's-Rule) — Slater determinants
- [2.6 - Eigenvalues Eigenvectors & Diagonalization](2.6---Eigenvalues-Eigenvectors-&-Diagonalization) — Eigenvalue problems in atomic physics
- [03.2 - Chemical Bonding - Ionic, Covalent, Metallic & Intermolecular](03.2---Chemical-Bonding---Ionic,-Covalent,-Metallic-&-Intermolecular) — Next chapter: what atoms do with their electrons

### External References
- **MIT 5.111 OCW** — Lectures 1–7: Atomic structure and electron configurations
- **Khan Academy** — [Quantum numbers and orbitals](https://www.khanacademy.org/science/chemistry/electronic-structure-of-atoms)
- **Crash Course Chemistry** — Episodes 2–4: The nucleus, electron configuration
- **Griffiths, D.J.** — *Introduction to Quantum Mechanics*, Chapter 5 (identical particles)
- **Atkins, P.** — *Physical Chemistry*, Chapter 7 (atomic structure)

---

## 🔬 8. Advanced Derivations — The Hydrogen Atom from Scratch

### 8.1 — The Full Hydrogen-Atom Schrödinger Equation

The hydrogen atom is the only atom with an exact analytical solution. Every concept in atomic structure — quantum numbers, orbital shapes, energy levels — emerges from solving this single equation. You encountered this in [9.4 - Angular Momentum, Spin & Fine Structure](9.4---Angular-Momentum,-Spin-&-Fine-Structure), but here we do the full derivation with every step shown, connecting it directly to chemistry.

**The time-independent Schrödinger equation for hydrogen:**

$$
\hat{H}\psi = E\psi
$$

The Hamiltonian for an electron (mass $m_e$, charge $-e$) orbiting a proton (mass $m_p$, charge $+e$):

$$
\hat{H} = -\frac{\hbar^2}{2\mu}\nabla^2 - \frac{e^2}{4\pi\epsilon_0 r}
$$

where $\mu$ is the reduced mass:

$$
\mu = \frac{m_e m_p}{m_e + m_p} \approx m_e\left(1 - \frac{m_e}{m_p}\right) \approx 0.99946\,m_e
$$

**Why reduced mass?** The two-body problem (electron + proton) reduces to a one-body problem (a particle of mass $\mu$ in a central potential). This is the same center-of-mass separation you used in classical mechanics ([4.3 - Central Force Problems & Kepler's Laws](4.3---Central-Force-Problems-&-Kepler's-Laws)).

**In spherical coordinates** $(r, \theta, \phi)$, the Laplacian is:

$$
\nabla^2 = \frac{1}{r^2}\frac{\partial}{\partial r}\left(r^2\frac{\partial}{\partial r}\right) + \frac{1}{r^2\sin\theta}\frac{\partial}{\partial\theta}\left(\sin\theta\frac{\partial}{\partial\theta}\right) + \frac{1}{r^2\sin^2\theta}\frac{\partial^2}{\partial\phi^2}
$$

The full Schrödinger equation becomes:

$$
-\frac{\hbar^2}{2\mu}\left[\frac{1}{r^2}\frac{\partial}{\partial r}\left(r^2\frac{\partial\psi}{\partial r}\right) + \frac{1}{r^2\sin\theta}\frac{\partial}{\partial\theta}\left(\sin\theta\frac{\partial\psi}{\partial\theta}\right) + \frac{1}{r^2\sin^2\theta}\frac{\partial^2\psi}{\partial\phi^2}\right] - \frac{e^2}{4\pi\epsilon_0 r}\psi = E\psi
$$

### 8.2 — Separation of Variables: $\psi(r,\theta,\phi) = R(r)\,Y(\theta,\phi)$

Because the potential $V(r) = -e^2/(4\pi\epsilon_0 r)$ depends only on $r$, we can separate the wavefunction:

$$
\psi(r, \theta, \phi) = R(r)\,\Theta(\theta)\,\Phi(\phi)
$$

**Step 1 — The $\phi$ equation:**

Substituting and dividing through, the $\phi$-dependent part separates as:

$$
\frac{d^2\Phi}{d\phi^2} = -m_\ell^2\,\Phi
$$

**Solution:**

$$
\Phi(\phi) = \frac{1}{\sqrt{2\pi}}e^{im_\ell\phi}
$$

**Boundary condition:** $\Phi(\phi + 2\pi) = \Phi(\phi)$ requires $m_\ell = 0, \pm 1, \pm 2, \ldots$ — the magnetic quantum number emerges from periodicity.

**Step 2 — The $\theta$ equation (associated Legendre):**

After separating the $\phi$ part, the $\theta$ equation becomes:

$$
\frac{1}{\sin\theta}\frac{d}{d\theta}\left(\sin\theta\frac{d\Theta}{d\theta}\right) + \left[\ell(\ell+1) - \frac{m_\ell^2}{\sin^2\theta}\right]\Theta = 0
$$

This is the **associated Legendre equation**. The solutions are the associated Legendre polynomials $P_\ell^{m_\ell}(\cos\theta)$, which exist (are finite and normalizable) only when:

- $\ell = 0, 1, 2, 3, \ldots$ (the angular momentum quantum number)
- $|m_\ell| \leq \ell$

Combined with $\Phi(\phi)$, these give the **spherical harmonics**:

$$
Y_\ell^{m_\ell}(\theta, \phi) = (-1)^{m_\ell}\sqrt{\frac{(2\ell+1)}{4\pi}\frac{(\ell - |m_\ell|)!}{(\ell + |m_\ell|)!}}\,P_\ell^{|m_\ell|}(\cos\theta)\,e^{im_\ell\phi}
$$

**First few spherical harmonics (the orbital shapes you know):**

| $\ell$ | $m_\ell$ | $Y_\ell^{m_\ell}$ | Orbital name |
|---|---|---|---|
| 0 | 0 | $\frac{1}{\sqrt{4\pi}}$ | $s$ |
| 1 | 0 | $\sqrt{\frac{3}{4\pi}}\cos\theta$ | $p_z$ |
| 1 | $\pm 1$ | $\mp\sqrt{\frac{3}{8\pi}}\sin\theta\,e^{\pm i\phi}$ | $p_x, p_y$ (linear combinations) |
| 2 | 0 | $\sqrt{\frac{5}{16\pi}}(3\cos^2\theta - 1)$ | $d_{z^2}$ |

**The chemistry connection:** When your textbook says "a $p$ orbital has a dumbbell shape," it means $|Y_1^0|^2 \propto \cos^2\theta$. The shape is not arbitrary — it's a mathematical function.

### 8.3 — The Radial Equation and Energy Quantization

After separating the angular parts, the radial equation is:

$$
-\frac{\hbar^2}{2\mu}\left[\frac{d^2 u}{dr^2} - \frac{\ell(\ell+1)}{r^2}u\right] - \frac{e^2}{4\pi\epsilon_0 r}u = Eu
$$

where $u(r) = rR(r)$ (a standard substitution that simplifies the equation).

**Introduce dimensionless variables.** Let $a_0 = \frac{4\pi\epsilon_0\hbar^2}{\mu e^2} \approx 0.529\,\text{Å}$ (the Bohr radius) and define:

$$
\rho = \frac{2r}{na_0}, \quad \kappa = \frac{1}{na_0}
$$

where $n$ will turn out to be the principal quantum number.

**The radial equation becomes:**

$$
\frac{d^2 u}{d\rho^2} = \left[\frac{\ell(\ell+1)}{\rho^2} - \frac{n}{\rho} + \frac{1}{4}\right]u
$$

**Asymptotic analysis:**

- As $\rho \to \infty$: $\frac{d^2u}{d\rho^2} \approx \frac{1}{4}u$, so $u \sim e^{-\rho/2}$ (decaying solution).
- As $\rho \to 0$: $\frac{d^2u}{d\rho^2} \approx \frac{\ell(\ell+1)}{\rho^2}u$, so $u \sim \rho^{\ell+1}$.

**Factoring out the asymptotic behavior:**

$$
u(\rho) = \rho^{\ell+1}\,e^{-\rho/2}\,L(\rho)
$$

Substituting back yields the **associated Laguerre equation** for $L(\rho)$. The solutions are the associated Laguerre polynomials $L_{n-\ell-1}^{2\ell+1}(\rho)$, which terminate (giving normalizable wavefunctions) only when:

$$
n = \ell + 1, \ell + 2, \ell + 3, \ldots
$$

This is where the constraint $\ell \leq n - 1$ comes from — it's not a rule to memorize, it's a mathematical necessity for the series to terminate.

**The energy eigenvalues:**

$$
E_n = -\frac{\mu e^4}{2(4\pi\epsilon_0)^2\hbar^2}\cdot\frac{1}{n^2} = -\frac{13.6\,\text{eV}}{n^2}
$$

**Critical observation:** The energy depends ONLY on $n$, not on $\ell$ or $m_\ell$. This is the **accidental degeneracy** of hydrogen — a consequence of the $1/r$ potential having a hidden $SO(4)$ symmetry. For multi-electron atoms, electron-electron repulsion breaks this degeneracy, making energy depend on both $n$ and $\ell$. This is why the periodic table has its structure.

### 8.4 — The Complete Hydrogen Wavefunctions

Putting it all together:

$$
\psi_{n\ell m_\ell}(r, \theta, \phi) = R_{n\ell}(r)\,Y_\ell^{m_\ell}(\theta, \phi)
$$

where:

$$
R_{n\ell}(r) = -\sqrt{\left(\frac{2}{na_0}\right)^3\frac{(n-\ell-1)!}{2n[(n+\ell)!]^3}}\,e^{-r/(na_0)}\left(\frac{2r}{na_0}\right)^\ell L_{n-\ell-1}^{2\ell+1}\left(\frac{2r}{na_0}\right)
$$

**First few radial wavefunctions:**

$$
R_{10}(r) = 2\left(\frac{1}{a_0}\right)^{3/2}e^{-r/a_0} \quad (1s)
$$

$$
R_{20}(r) = \frac{1}{2\sqrt{2}}\left(\frac{1}{a_0}\right)^{3/2}\left(2 - \frac{r}{a_0}\right)e^{-r/(2a_0)} \quad (2s)
$$

$$
R_{21}(r) = \frac{1}{2\sqrt{6}}\left(\frac{1}{a_0}\right)^{3/2}\frac{r}{a_0}\,e^{-r/(2a_0)} \quad (2p)
$$

**Verification with Python:**

```python
import numpy as np
from scipy.special import genlaguerre, sph_harm
from math import factorial

def hydrogen_radial(n, l, r, a0=0.529):
    """Compute R_nl(r) for hydrogen atom."""
    rho = 2 * r / (n * a0)
    norm = -np.sqrt((2/(n*a0))**3 * factorial(n-l-1) / (2*n*(factorial(n+l))**3))
    L = genlaguerre(n-l-1, 2*l+1)(rho)
    return norm * np.exp(-rho/2) * rho**l * L

# Verify normalization: integral of |R_nl|^2 * r^2 dr = 1
from scipy.integrate import quad
r_vals = np.linspace(0, 50, 1000)
integrand = lambda r: (hydrogen_radial(2, 1, r))**2 * r**2
result, _ = quad(integrand, 0, np.inf)
print(f"Normalization check (should be 1): {result:.6f}")
```

### 8.5 — Spin-Orbit Coupling: Where Chemistry Meets Relativity

The electron has intrinsic angular momentum (spin) with quantum number $s = 1/2$. In the electron's rest frame, the nucleus orbits the electron, creating a magnetic field. The interaction between the electron's magnetic moment and this field is **spin-orbit coupling**.

**The spin-orbit Hamiltonian:**

$$
\hat{H}_{SO} = \frac{e^2}{8\pi\epsilon_0 m_e^2 c^2}\frac{1}{r^3}\,\hat{\mathbf{L}}\cdot\hat{\mathbf{S}}
$$

**Evaluating $\hat{\mathbf{L}}\cdot\hat{\mathbf{S}}$:**

Define total angular momentum $\hat{\mathbf{J}} = \hat{\mathbf{L}} + \hat{\mathbf{S}}$. Then:

$$
\hat{\mathbf{J}}^2 = \hat{\mathbf{L}}^2 + \hat{\mathbf{S}}^2 + 2\hat{\mathbf{L}}\cdot\hat{\mathbf{S}}
$$

$$
\hat{\mathbf{L}}\cdot\hat{\mathbf{S}} = \frac{1}{2}\left(\hat{\mathbf{J}}^2 - \hat{\mathbf{L}}^2 - \hat{\mathbf{S}}^2\right)
$$

**Eigenvalues:**

$$
\langle\hat{\mathbf{L}}\cdot\hat{\mathbf{S}}\rangle = \frac{\hbar^2}{2}\left[j(j+1) - \ell(\ell+1) - s(s+1)\right]
$$

where $j = \ell \pm 1/2$ (for $\ell > 0$).

**The energy correction (first-order perturbation theory):**

$$
\Delta E_{SO} = \frac{E_n^2}{m_e c^2}\frac{n\left[j(j+1) - \ell(\ell+1) - 3/4\right]}{2\ell(\ell + 1/2)(\ell + 1)}
$$

**Chemistry consequence:** Spin-orbit coupling splits the sodium D-line into a doublet (589.0 nm and 589.6 nm). It also explains why heavy elements (Pb, Bi, Po) have unusual chemistry — relativistic effects become significant when $Z$ is large.

**The fine-structure constant** $\alpha = e^2/(4\pi\epsilon_0\hbar c) \approx 1/137$ controls the magnitude of spin-orbit splitting. The correction scales as $\alpha^2 E_n$ — small for hydrogen, but increasingly important for heavy atoms.

### 8.6 — Multi-Electron Atoms: The Hartree-Fock Method

For atoms with $N > 1$ electrons, the Schrödinger equation becomes:

$$
\hat{H} = \sum_{i=1}^N\left[-\frac{\hbar^2}{2m_e}\nabla_i^2 - \frac{Ze^2}{4\pi\epsilon_0 r_i}\right] + \sum_{i<j}\frac{e^2}{4\pi\epsilon_0|\mathbf{r}_i - \mathbf{r}_j|}
$$

The electron-electron repulsion term $\sum_{i<j}e^2/(4\pi\epsilon_0|\mathbf{r}_i - \mathbf{r}_j|)$ makes this unsolvable analytically. We need approximation methods.

**The Hartree approximation (mean-field):**

Assume each electron moves independently in an average potential created by all other electrons:

$$
\psi(\mathbf{r}_1, \mathbf{r}_2, \ldots, \mathbf{r}_N) \approx \phi_1(\mathbf{r}_1)\,\phi_2(\mathbf{r}_2)\cdots\phi_N(\mathbf{r}_N)
$$

Each orbital $\phi_i$ satisfies:

$$
\left[-\frac{\hbar^2}{2m_e}\nabla^2 - \frac{Ze^2}{4\pi\epsilon_0 r} + V_{\text{eff}}^{(i)}(r)\right]\phi_i = \epsilon_i\phi_i
$$

where the effective potential includes the average repulsion from all other electrons:

$$
V_{\text{eff}}^{(i)}(\mathbf{r}) = \sum_{j \neq i}\int\frac{e^2|\phi_j(\mathbf{r}')|^2}{4\pi\epsilon_0|\mathbf{r} - \mathbf{r}'|}\,d^3r'
$$

**The self-consistency requirement:** The potential depends on the orbitals, which depend on the potential. Solution: iterate.

1. Guess initial orbitals (e.g., hydrogen-like with $Z_{\text{eff}}$).
2. Compute $V_{\text{eff}}$ from those orbitals.
3. Solve the single-particle equations to get new orbitals.
4. Repeat until convergence (orbitals don't change between iterations).

This is the **Self-Consistent Field (SCF)** method.

**The Hartree-Fock improvement:**

The Hartree product violates the Pauli exclusion principle (it's not antisymmetric under particle exchange). The fix: replace the product with a **Slater determinant** (see [2.5 - Determinants & Cramer's Rule](2.5---Determinants-&-Cramer's-Rule)):

$$
\Psi(\mathbf{r}_1, \mathbf{r}_2, \ldots, \mathbf{r}_N) = \frac{1}{\sqrt{N!}}\begin{vmatrix}\phi_1(\mathbf{r}_1) & \phi_2(\mathbf{r}_1) & \cdots & \phi_N(\mathbf{r}_1)\\\phi_1(\mathbf{r}_2) & \phi_2(\mathbf{r}_2) & \cdots & \phi_N(\mathbf{r}_2)\\\vdots & \vdots & \ddots & \vdots\\\phi_1(\mathbf{r}_N) & \phi_2(\mathbf{r}_N) & \cdots & \phi_N(\mathbf{r}_N)\end{vmatrix}
$$

This automatically satisfies:
- **Antisymmetry:** Swapping two rows (two particles) flips the sign.
- **Pauli exclusion:** If two orbitals are identical, two columns are identical → determinant = 0.

**The Hartree-Fock equations** add an **exchange term** $K$ beyond the Coulomb repulsion $J$:

$$
\left[\hat{h} + \sum_{j}(\hat{J}_j - \hat{K}_j)\right]\phi_i = \epsilon_i\phi_i
$$

The exchange operator $\hat{K}_j$ has no classical analogue — it arises purely from the antisymmetry requirement (quantum statistics). It's responsible for **Hund's rule**: parallel spins have lower energy because the exchange term reduces electron-electron repulsion for same-spin electrons.

**What Hartree-Fock gives us:**

- Orbital energies $\epsilon_i$ that explain the filling order
- The reason why $3d$ and $4s$ are close in energy for transition metals
- Quantitative $Z_{\text{eff}}$ values (better than Slater's rules)
- ~99% of the total energy (the remaining ~1% is "correlation energy")

**What it misses:**

- Electron correlation (instantaneous electron-electron interactions beyond the mean field)
- London dispersion forces (which require correlation — see [03.2 - Chemical Bonding - Ionic, Covalent, Metallic & Intermolecular](03.2---Chemical-Bonding---Ionic,-Covalent,-Metallic-&-Intermolecular))
- Exact energies for chemical bond breaking

> [!tip] Cross-link to Track 09
> The full mathematical machinery of Hartree-Fock — variational principle, Lagrange multipliers, Roothaan equations — is developed in [9.4 - Angular Momentum, Spin & Fine Structure](9.4---Angular-Momentum,-Spin-&-Fine-Structure). Here we focus on the chemical consequences.

### 8.7 — Why the Aufbau Principle Has Exceptions

The Aufbau principle says: fill orbitals in order of increasing energy. But this "rule" has famous exceptions. Understanding WHY requires Hartree-Fock thinking.

**The standard exceptions:**

| Element | Expected | Actual | Why |
|---|---|---|---|
| Cr ($Z = 24$) | $[Ar]\,3d^4\,4s^2$ | $[Ar]\,3d^5\,4s^1$ | Half-filled $d$ shell: exchange stabilization |
| Cu ($Z = 29$) | $[Ar]\,3d^9\,4s^2$ | $[Ar]\,3d^{10}\,4s^1$ | Filled $d$ shell: no exchange penalty for pairing |
| Mo ($Z = 42$) | $[Kr]\,4d^4\,5s^2$ | $[Kr]\,4d^5\,5s^1$ | Same as Cr (half-filled $d$) |
| Ag ($Z = 47$) | $[Kr]\,4d^9\,5s^2$ | $[Kr]\,4d^{10}\,5s^1$ | Same as Cu (filled $d$) |
| Pd ($Z = 46$) | $[Kr]\,4d^8\,5s^2$ | $[Kr]\,4d^{10}\,5s^0$ | Extreme case: $d^{10}$ stability wins completely |

**The physics behind the exceptions:**

The exchange energy for $N$ electrons with parallel spin in a subshell is proportional to $N(N-1)/2$ (the number of same-spin pairs). Going from $3d^4\,4s^2$ to $3d^5\,4s^1$:

- Exchange pairs in $d$ shell: $\binom{4}{2} = 6 \to \binom{5}{2} = 10$ (gain of 4 exchange pairs)
- Cost: promoting one $4s$ electron to $3d$ (small energy cost because $3d$ and $4s$ are nearly degenerate)

When the exchange energy gain exceeds the promotion cost, the exception occurs.

**Quantitative estimate:**

The exchange integral $K_{3d,3d} \approx 0.9\,\text{eV}$ for first-row transition metals. Gaining 4 extra exchange pairs gives $\sim 3.6\,\text{eV}$ stabilization. The $4s \to 3d$ promotion energy is only $\sim 1.5\,\text{eV}$ for Cr. Net stabilization: $\sim 2.1\,\text{eV}$. The exception wins.

> [!warning] Common Misconception
> Many textbooks say "half-filled and fully-filled subshells are extra stable" as if it's a fundamental law. It's NOT — it's a consequence of exchange energy mathematics. The "stability" is just the exchange term being maximized at these configurations. Don't memorize the rule; understand the exchange integral.

### 8.8 — Periodic Trends Derived from $Z_{\text{eff}}$

All major periodic trends follow from one quantity: the effective nuclear charge $Z_{\text{eff}}$ experienced by valence electrons.

**Atomic radius:**

$$
\langle r \rangle_{n\ell} \approx \frac{n^2 a_0}{Z_{\text{eff}}}
$$

- Across a period (left → right): $Z_{\text{eff}}$ increases, $n$ constant → radius decreases.
- Down a group: $n$ increases faster than $Z_{\text{eff}}$ → radius increases.

**Ionization energy:**

$$
IE \approx \frac{Z_{\text{eff}}^2 \times 13.6\,\text{eV}}{n^2}
$$

- Across a period: $Z_{\text{eff}}$ increases → IE increases (with exceptions at Al and O due to subshell effects).
- Down a group: $n$ increases → IE decreases.

**Electronegativity (Mulliken definition):**

$$
\chi_{\text{Mulliken}} = \frac{IE + EA}{2}
$$

Both IE and EA increase with $Z_{\text{eff}}$, so electronegativity increases across a period and decreases down a group.

**Electron affinity:**

More complex — depends on whether the added electron enters a new subshell or completes one. Noble gases have negative EA (adding an electron is energetically unfavorable because it would enter the next shell with much lower $Z_{\text{eff}}$).

> [!tip] The Unifying Principle
> If you understand $Z_{\text{eff}}$ and how shielding works, you can DERIVE every periodic trend instead of memorizing them. This is the power of understanding atomic structure from quantum mechanics rather than from a list of rules.

## 📎 9. Appendix — Deep Dives & Mastery Challenges

### Appendix A — Complete Aufbau Exception Table (First 103 Elements)

Beyond Cr and Cu, there are ~20 elements with non-standard configurations. Here is the complete list for the first four transition series:

**First transition series ($3d$):**
| Element | $Z$ | Expected | Actual | Reason |
|---|---|---|---|---|
| Cr | 24 | $[Ar]3d^44s^2$ | $[Ar]3d^54s^1$ | Exchange stabilization (half-filled $d$) |
| Cu | 29 | $[Ar]3d^94s^2$ | $[Ar]3d^{10}4s^1$ | Filled $d$ shell stability |

**Second transition series ($4d$):**
| Element | $Z$ | Expected | Actual | Reason |
|---|---|---|---|---|
| Nb | 41 | $[Kr]4d^35s^2$ | $[Kr]4d^45s^1$ | Near half-filled; $4d$/$5s$ gap smaller |
| Mo | 42 | $[Kr]4d^45s^2$ | $[Kr]4d^55s^1$ | Half-filled $d$ |
| Ru | 44 | $[Kr]4d^65s^2$ | $[Kr]4d^75s^1$ | Exchange + relativistic contraction |
| Rh | 45 | $[Kr]4d^75s^2$ | $[Kr]4d^85s^1$ | Same mechanism |
| Pd | 46 | $[Kr]4d^85s^2$ | $[Kr]4d^{10}5s^0$ | Extreme: completely filled $d$, empty $s$ |
| Ag | 47 | $[Kr]4d^95s^2$ | $[Kr]4d^{10}5s^1$ | Filled $d$ |

**Third transition series ($5d$) — relativistic effects become significant:**
| Element | $Z$ | Expected | Actual | Reason |
|---|---|---|---|---|
| La | 57 | $[Xe]4f^15d^06s^2$ | $[Xe]4f^05d^16s^2$ | $5d$ slightly lower than $4f$ for La |
| Pt | 78 | $[Xe]4f^{14}5d^86s^2$ | $[Xe]4f^{14}5d^96s^1$ | Relativistic $6s$ contraction |
| Au | 79 | $[Xe]4f^{14}5d^96s^2$ | $[Xe]4f^{14}5d^{10}6s^1$ | Filled $d$ + relativistic effects |

**The relativistic explanation for heavy elements:**

For elements with $Z > 70$, the $1s$ electrons move at speeds approaching $v/c \approx Z\alpha \approx 0.5$–$0.6$. Relativistic mass increase contracts the $s$ and $p$ orbitals (they penetrate close to the nucleus), which:

1. Stabilizes $s$ and $p$ orbitals (lower energy)
2. Expands $d$ and $f$ orbitals (better shielded by contracted inner orbitals)
3. Makes gold yellow (the $5d \to 6s$ transition absorbs blue light due to relativistic level shifts)
4. Makes mercury liquid (relativistic $6s^2$ pair is so stable it resists metallic bonding)

### Appendix B — Slater's Rules: Complete Algorithm

**Step 1:** Write the electron configuration in groups: $(1s)(2s,2p)(3s,3p)(3d)(4s,4p)(4d)(4f)(5s,5p)\ldots$

**Step 2:** For an electron in group with principal quantum number $n$:

**If the electron is in an $s$ or $p$ orbital:**
- Electrons in the SAME group: each contributes $\sigma = 0.35$ (except $1s$: use 0.30)
- Electrons in the $(n-1)$ group: each contributes $\sigma = 0.85$
- Electrons in $(n-2)$ or lower groups: each contributes $\sigma = 1.00$

**If the electron is in a $d$ or $f$ orbital:**
- Electrons in the SAME group: each contributes $\sigma = 0.35$
- ALL electrons in lower groups: each contributes $\sigma = 1.00$

**Step 3:** $Z_{\text{eff}} = Z - \sigma$

**Worked example — Iron (Fe, $Z = 26$), 3d electron:**

Groups: $(1s^2)(2s^2 2p^6)(3s^2 3p^6)(3d^6)(4s^2)$

For a $3d$ electron:
- Same group ($3d$): 5 other electrons × 0.35 = 1.75
- All lower groups: $(1s^2 + 2s^2 2p^6 + 3s^2 3p^6)$ = 18 electrons × 1.00 = 18.00

$$
Z_{\text{eff}}(3d) = 26 - 1.75 - 18.00 = 6.25
$$

For a $4s$ electron:
- Same group ($4s$): 1 other electron × 0.35 = 0.35
- $(n-1)$ group ($3d$): 6 electrons × 0.85 = 5.10
- $(n-1)$ group ($3s,3p$): 8 electrons × 0.85 = 6.80
- Lower groups ($1s, 2s, 2p$): 10 electrons × 1.00 = 10.00

$$
Z_{\text{eff}}(4s) = 26 - 0.35 - 5.10 - 6.80 - 10.00 = 3.75
$$

**Interpretation:** The $3d$ electrons see a much higher effective nuclear charge (6.25) than the $4s$ electrons (3.75). This is why $3d$ electrons are more tightly bound in the ion — and why Fe²⁺ loses $4s$ electrons first, not $3d$.

### Appendix C — Computational Verification: Hartree-Fock for Helium

The simplest multi-electron atom. Exact ground-state energy: $E = -2.9037\,\text{hartree}$. Hartree-Fock gives $E_{HF} = -2.8617\,\text{hartree}$ (98.6% of exact). The difference ($0.042\,\text{hartree} = 1.14\,\text{eV}$) is the correlation energy.

```python
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar

# Variational Hartree-Fock for Helium with single Slater orbital
# Trial wavefunction: phi(r) = (zeta^3/pi)^(1/2) * exp(-zeta*r)
# Two electrons in same spatial orbital (opposite spin)

def helium_energy(zeta):
    """
    Total energy of He with trial wavefunction exp(-zeta*r).
    E = 2*T + 2*V_ne + V_ee
    T (kinetic per electron) = zeta^2 / 2
    V_ne (nuclear attraction per electron) = -Z * zeta  (Z=2 for He)
    V_ee (electron-electron repulsion) = 5*zeta/8
    """
    Z = 2
    T = zeta**2 / 2
    V_ne = -Z * zeta
    V_ee = 5 * zeta / 8
    return 2*T + 2*V_ne + V_ee

# Minimize energy with respect to zeta
result = minimize_scalar(helium_energy, bounds=(1.0, 3.0), method='bounded')
zeta_opt = result.x
E_opt = result.fun

print(f"Optimal zeta: {zeta_opt:.4f}")  # Should be 27/16 = 1.6875
print(f"Variational energy: {E_opt:.4f} hartree")  # Should be -2.8477
print(f"Exact energy: -2.9037 hartree")
print(f"Hartree-Fock limit: -2.8617 hartree")
print(f"Correlation energy: {-2.9037 - (-2.8617):.4f} hartree")
```

**Output interpretation:** The single-parameter variational calculation gives $\zeta = 27/16 = 1.6875$ and $E = -2.848\,\text{hartree}$. The optimal $\zeta < Z = 2$ because each electron partially shields the other from the nucleus — this IS the concept of effective nuclear charge, derived variationally rather than from Slater's empirical rules.

### Appendix D — From Atomic Structure to the Periodic Table: The Complete Logic Chain

Here is the complete logical chain from quantum mechanics to the periodic table, with no memorization required:

1. **Schrödinger equation** → energy levels depend on $n$ (hydrogen) or $n$ and $\ell$ (multi-electron atoms)
2. **Pauli exclusion** (antisymmetric wavefunctions) → maximum 2 electrons per orbital
3. **Orbital capacity:** $2(2\ell + 1)$ electrons per subshell → s:2, p:6, d:10, f:14
4. **Energy ordering** (from Hartree-Fock): approximately follows $(n + \ell)$ rule due to shielding
5. **Aufbau principle** → fill lowest energy first → determines electron configuration
6. **Hund's rule** (exchange energy) → maximize parallel spins within a subshell
7. **Valence electrons** determine chemistry → elements with same valence configuration have similar properties
8. **Periodic table structure:** s-block (groups 1–2), d-block (groups 3–12), p-block (groups 13–18), f-block (lanthanides/actinides)

**The table's shape is quantum mechanics made visible:**
- Width of s-block = $2(2 \times 0 + 1) = 2$ (one $s$ orbital)
- Width of p-block = $2(2 \times 1 + 1) = 6$ (three $p$ orbitals)
- Width of d-block = $2(2 \times 2 + 1) = 10$ (five $d$ orbitals)
- Width of f-block = $2(2 \times 3 + 1) = 14$ (seven $f$ orbitals)

Total: $2 + 6 + 10 + 14 = 32$ — the maximum period length.

> [!danger] 🧠 Common Misconceptions — Section 8 & 9 Summary
> 
> **❌ "The hydrogen atom solution is just for hydrogen"**
> **Truth:** Every multi-electron calculation starts from hydrogen-like orbitals. The quantum numbers, orbital shapes, and radial functions are the BUILDING BLOCKS for all of chemistry. Hartree-Fock literally uses hydrogen-like functions as its starting guess.
> 
> **❌ "Spin-orbit coupling is only for physics, not chemistry"**
> **Truth:** Spin-orbit coupling explains why lead is inert (the "inert pair effect" is relativistic), why heavy-element chemistry differs from light-element chemistry, and why certain spectroscopic transitions are forbidden. If you do any chemistry with elements below Period 4, you need this.
> 
> **❌ "Aufbau exceptions are random and must be memorized"**
> **Truth:** Every exception follows from the competition between orbital energy differences and exchange stabilization. If you can estimate the exchange integral and the promotion energy, you can PREDICT the exceptions.
> 
> **❌ "Effective nuclear charge is just an approximation"**
> **Truth:** $Z_{\text{eff}}$ is the EXACT eigenvalue of the Hartree-Fock potential experienced by a valence electron. Slater's rules are the approximation; the concept itself is rigorous.
> 
> **❌ "I failed chemistry because I'm bad at memorizing"**
> **Truth:** You failed because the course asked you to memorize consequences without teaching you the cause. Now you have the cause (quantum mechanics). The consequences follow logically. You don't need to memorize that fluorine is more electronegative than oxygen — you can CALCULATE that $Z_{\text{eff}}$ is higher for F.

---

*Previous: [LEARNING_PATH](LEARNING_PATH) | Next: [03.2 - Chemical Bonding - Ionic, Covalent, Metallic & Intermolecular](03.2---Chemical-Bonding---Ionic,-Covalent,-Metallic-&-Intermolecular)*
