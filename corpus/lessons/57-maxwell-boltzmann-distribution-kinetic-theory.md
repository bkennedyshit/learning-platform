---
title: "Maxwell Boltzmann Distribution Kinetic Theory"
subject: "Thermodynamics & Statistical Mechanics"
catalog: advanced
audience_tier: higher-education
chapter: "5.7"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 5.7 — Maxwell-Boltzmann Distribution & Kinetic Theory

> *"The second law of thermodynamics has the same degree of truth as the statement that if you throw a tumblerful of water into the sea, you cannot get the same tumblerful of water out again."* — James Clerk Maxwell

The Maxwell-Boltzmann distribution describes the statistical distribution of molecular speeds in a gas at thermal equilibrium. Combined with kinetic theory, it provides a microscopic derivation of pressure, temperature, transport coefficients (viscosity, thermal conductivity, diffusion), and the mean free path. This chapter derives the distribution from first principles, computes all characteristic speeds, and develops the kinetic theory of transport.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Derive the Maxwell-Boltzmann speed distribution from the canonical ensemble.
2. Compute the most probable speed $v_p$, mean speed $\langle v\rangle$, and RMS speed $v_{\text{rms}}$.
3. Derive the ideal gas law $PV = Nk_BT$ from kinetic theory (molecular bombardment).
4. Compute the mean free path $\ell$ and collision frequency.
5. Derive transport coefficients (viscosity $\eta$, thermal conductivity $\kappa$, diffusion $D$).
6. Apply the distribution to effusion and molecular beams.

---

## 🖼️ Visual Anchor — Maxwell-Boltzmann Speed Distribution

![math-05__5.7-fig1](math-05__5.7-fig1.svg)

---

## 📚 1. Definitions

### Definition 5.7.1 — Maxwell-Boltzmann Speed Distribution

The probability that a molecule has speed between $v$ and $v + dv$:

$$
f(v)\,dv = 4\pi\left(\frac{m}{2\pi k_BT}\right)^{3/2} v^2 e^{-mv^2/(2k_BT)}\,dv
$$

### Definition 5.7.2 — Characteristic Speeds

$$
v_p = \sqrt{\frac{2k_BT}{m}} \quad \text{(most probable)}
$$

$$
\langle v\rangle = \sqrt{\frac{8k_BT}{\pi m}} \quad \text{(mean)}
$$

$$
v_{\text{rms}} = \sqrt{\langle v^2\rangle} = \sqrt{\frac{3k_BT}{m}} \quad \text{(root-mean-square)}
$$

Note: $v_p < \langle v\rangle < v_{\text{rms}}$ always.

### Definition 5.7.3 — Mean Free Path

$$
\ell = \frac{1}{\sqrt{2}\,n\sigma}
$$

where $n = N/V$ is the number density and $\sigma = \pi d^2$ is the collision cross-section for hard spheres of diameter $d$.

### Definition 5.7.4 — Collision Frequency

$$
\nu = \frac{\langle v\rangle}{\ell} = \sqrt{2}\,n\sigma\langle v\rangle
$$

---

## 📐 2. Axioms / Postulates

### Postulate 5.7.P1 — Molecular Chaos (Stosszahlansatz)

The velocities of colliding molecules are uncorrelated before collision. This assumption underlies the Boltzmann transport equation and the derivation of the $H$-theorem.

### Postulate 5.7.P2 — Isotropy

In equilibrium, there is no preferred direction: the velocity distribution is isotropic. The probability of velocity $\mathbf{v}$ depends only on $|\mathbf{v}| = v$.

---

## 🛡️ 3. Lemmas

### Lemma 5.7.1 — Gaussian Integrals (Reference)

$$
I_n = \int_0^\infty x^n e^{-ax^2}\,dx
$$

$$
I_0 = \frac{1}{2}\sqrt{\frac{\pi}{a}}, \quad I_1 = \frac{1}{2a}, \quad I_2 = \frac{1}{4}\sqrt{\frac{\pi}{a^3}}, \quad I_3 = \frac{1}{2a^2}, \quad I_4 = \frac{3}{8}\sqrt{\frac{\pi}{a^5}}
$$

General: $I_{2n} = \frac{(2n-1)!!}{2^{n+1}}\sqrt{\frac{\pi}{a^{2n+1}}}$, $I_{2n+1} = \frac{n!}{2a^{n+1}}$.

### Lemma 5.7.2 — Velocity Component Distribution

Each component $v_x$ follows a 1D Gaussian (normal) distribution:

$$
g(v_x) = \sqrt{\frac{m}{2\pi k_BT}}\exp\left(-\frac{mv_x^2}{2k_BT}\right)
$$

with $\langle v_x\rangle = 0$ and $\langle v_x^2\rangle = k_BT/m$.

---

## 👑 4. Theorems

### Theorem 5.7.1 — Derivation of the Speed Distribution

The 3D velocity distribution factorizes: $f(\mathbf{v}) = g(v_x)g(v_y)g(v_z)$. Converting to spherical coordinates in velocity space ($d^3v = 4\pi v^2\,dv$) yields the Maxwell-Boltzmann speed distribution.

### Theorem 5.7.2 — Kinetic Theory Derivation of Pressure

$$
P = \frac{1}{3}nm\langle v^2\rangle = \frac{1}{3}\rho\langle v^2\rangle = nk_BT
$$

### Theorem 5.7.3 — Effusion Rate

The rate at which molecules escape through a small hole of area $A$:

$$
\Phi = \frac{1}{4}n\langle v\rangle A
$$

---

## ✍️ 5. Proofs / Derivations

### 5.1 Derivation of the Maxwell-Boltzmann Distribution

From the canonical ensemble, the probability of a single molecule having velocity $\mathbf{v}$ is:

$$
P(\mathbf{v})\,d^3v \propto e^{-\beta \cdot mv^2/2}\,d^3v = e^{-mv^2/(2k_BT)}\,d^3v
$$

Normalize: $\int P(\mathbf{v})\,d^3v = 1$.

$$
\int_{-\infty}^\infty\int_{-\infty}^\infty\int_{-\infty}^\infty C\,e^{-m(v_x^2+v_y^2+v_z^2)/(2k_BT)}\,dv_x\,dv_y\,dv_z = 1
$$

The integral factorizes: $C \cdot \left(\sqrt{\frac{2\pi k_BT}{m}}\right)^3 = 1$, so $C = \left(\frac{m}{2\pi k_BT}\right)^{3/2}$.

Convert to speed: $d^3v = 4\pi v^2\,dv$ (spherical shell in velocity space):

$$
f(v)\,dv = 4\pi\left(\frac{m}{2\pi k_BT}\right)^{3/2}v^2 e^{-mv^2/(2k_BT)}\,dv \quad \blacksquare
$$

### 5.2 Computation of Characteristic Speeds

**Most probable speed $v_p$:** Set $df/dv = 0$.

$$
\frac{d}{dv}\left[v^2 e^{-mv^2/(2k_BT)}\right] = 2v\,e^{-mv^2/(2k_BT)} + v^2\left(-\frac{mv}{k_BT}\right)e^{-mv^2/(2k_BT)} = 0
$$

$$
v\,e^{-mv^2/(2k_BT)}\left[2 - \frac{mv^2}{k_BT}\right] = 0
$$

Non-trivial solution: $2 - mv_p^2/(k_BT) = 0 \implies v_p = \sqrt{2k_BT/m}$. $\blacksquare$

**Mean speed $\langle v\rangle$:** Using $a = m/(2k_BT)$:

$$
\langle v\rangle = 4\pi\left(\frac{m}{2\pi k_BT}\right)^{3/2}\int_0^\infty v^3 e^{-av^2}\,dv = 4\pi\left(\frac{a}{\pi}\right)^{3/2} \cdot \frac{1}{2a^2}
$$

$$
= 4\pi \cdot \frac{a^{3/2}}{\pi^{3/2}} \cdot \frac{1}{2a^2} = \frac{4\pi}{2\pi^{3/2}\sqrt{a}} = \frac{2}{\sqrt{\pi a}} = \sqrt{\frac{8k_BT}{\pi m}} \quad \blacksquare
$$

**RMS speed:** $\langle v^2\rangle = 4\pi(a/\pi)^{3/2}\int_0^\infty v^4 e^{-av^2}\,dv = 4\pi(a/\pi)^{3/2}\cdot\frac{3}{8}\sqrt{\pi/a^5} = \frac{3}{2a} = \frac{3k_BT}{m}$.

$v_{\text{rms}} = \sqrt{3k_BT/m}$. $\blacksquare$

### 5.3 Kinetic Theory Derivation of Pressure

Consider molecules hitting a wall perpendicular to the $x$-axis. A molecule with $v_x > 0$ hitting the wall transfers momentum $2mv_x$ per collision.

Number of molecules hitting area $A$ in time $dt$ with $v_x$ in $[v_x, v_x + dv_x]$:

$$
dN = n \cdot A \cdot v_x\,dt \cdot g(v_x)\,dv_x \quad (v_x > 0)
$$

Total force = total momentum transfer per unit time per unit area:

$$
P = \int_0^\infty (2mv_x) \cdot n v_x \cdot g(v_x)\,dv_x = 2mn\int_0^\infty v_x^2 g(v_x)\,dv_x
$$

Since $g(v_x)$ is symmetric: $\int_0^\infty v_x^2 g(v_x)\,dv_x = \frac{1}{2}\langle v_x^2\rangle = \frac{k_BT}{2m}$.

$$
P = 2mn \cdot \frac{k_BT}{2m} = nk_BT \quad \blacksquare
$$

### 5.4 Derivation of Mean Free Path

Consider a molecule moving with speed $v$ through a gas of stationary targets (number density $n$, cross-section $\sigma$). In time $dt$, it sweeps out a cylinder of volume $\sigma v\,dt$ and collides with $n\sigma v\,dt$ molecules.

Collision rate: $\nu_0 = n\sigma v$.

Accounting for the motion of target molecules (relative speed $v_{\text{rel}} = \sqrt{2}\,v$ for identical molecules from the Maxwell distribution):

$$
\nu = n\sigma\sqrt{2}\,\langle v\rangle
$$

Mean free path:

$$
\ell = \frac{\langle v\rangle}{\nu} = \frac{1}{\sqrt{2}\,n\sigma} \quad \blacksquare
$$

---

## 🧮 6. Worked Examples

### Example 5.7.E1 — Characteristic Speeds of N₂ at Room Temperature

For $\text{N}_2$ ($m = 28 \times 1.66\times10^{-27}\,\text{kg} = 4.65\times10^{-26}\,\text{kg}$) at $T = 300\,\text{K}$:

$$
v_p = \sqrt{\frac{2 \times 1.381\times10^{-23} \times 300}{4.65\times10^{-26}}} = \sqrt{\frac{8.286\times10^{-21}}{4.65\times10^{-26}}} = \sqrt{1.782\times10^5} = 422\,\text{m/s}
$$

$$
\langle v\rangle = \sqrt{\frac{8}{\pi}} \cdot \frac{v_p}{\sqrt{2}} = v_p\sqrt{\frac{4}{\pi}} = 422 \times 1.128 = 476\,\text{m/s}
$$

$$
v_{\text{rms}} = v_p\sqrt{\frac{3}{2}} = 422 \times 1.225 = 517\,\text{m/s}
$$

### Example 5.7.E2 — Mean Free Path at STP

For $\text{N}_2$ at STP ($T = 273\,\text{K}$, $P = 101.3\,\text{kPa}$), molecular diameter $d = 3.7\times10^{-10}\,\text{m}$:

$$
n = \frac{P}{k_BT} = \frac{101300}{1.381\times10^{-23}\times273} = 2.69\times10^{25}\,\text{m}^{-3}
$$

$$
\sigma = \pi d^2 = \pi(3.7\times10^{-10})^2 = 4.30\times10^{-19}\,\text{m}^2
$$

$$
\ell = \frac{1}{\sqrt{2}\times2.69\times10^{25}\times4.30\times10^{-19}} = \frac{1}{1.636\times10^7} = 6.1\times10^{-8}\,\text{m} = 61\,\text{nm}
$$

### Example 5.7.E3 — Effusion: Molecular Beam Flux

A container of He gas ($m = 6.64\times10^{-27}\,\text{kg}$) at $T = 500\,\text{K}$, $P = 1\,\text{Pa}$ has a pinhole of area $A = 10^{-6}\,\text{m}^2$. Find the effusion rate.

$$
n = P/(k_BT) = 1/(1.381\times10^{-23}\times500) = 1.45\times10^{20}\,\text{m}^{-3}
$$

$$
\langle v\rangle = \sqrt{8k_BT/(\pi m)} = \sqrt{\frac{8\times1.381\times10^{-23}\times500}{\pi\times6.64\times10^{-27}}} = \sqrt{2.65\times10^6} = 1628\,\text{m/s}
$$

$$
\Phi = \frac{1}{4}n\langle v\rangle A = \frac{1}{4}\times1.45\times10^{20}\times1628\times10^{-6} = 5.9\times10^{16}\,\text{molecules/s}
$$

---

## 🔗 7. Cross-links & Further Reading

### Internal Cross-links
- Partition function derivation of velocity distribution: [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy)
- Quantum corrections at low $T$: [5.8 - Quantum Statistics - Bose-Einstein & Fermi-Dirac](5.8---Quantum-Statistics---Bose-Einstein-&-Fermi-Dirac)
- Boltzmann distribution: [5.5 - Classical Statistical Mechanics - Microstates & Ensembles](5.5---Classical-Statistical-Mechanics---Microstates-&-Ensembles)
- Gaussian integrals: [1.2 - Integration Techniques & Applications](1.2---Integration-Techniques-&-Applications)
- Fluid dynamics applications: [6.1 - Fluid Statics & Kinematics](6.1---Fluid-Statics-&-Kinematics)

### Authoritative Sources
- **Maxwell, J.C.** (1860), "Illustrations of the Dynamical Theory of Gases"
- **Reif**, *Fundamentals*, Ch. 7 (kinetic theory)
- **Kittel & Kroemer**, *Thermal Physics*, Ch. 14
- **Chapman & Cowling**, *The Mathematical Theory of Non-Uniform Gases*


---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — Derive the Maxwell-Boltzmann Speed Distribution from the Velocity Distribution

**Problem.** Starting from the Maxwell-Boltzmann velocity distribution $f(\mathbf{v}) = \left(\frac{m}{2\pi k_BT}\right)^{3/2}\exp\left(-\frac{mv^2}{2k_BT}\right)$, derive the speed distribution $f(v)$ by integrating over all directions.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: The Velocity Distribution in 3D

The probability of finding a molecule with velocity in the range $[\mathbf{v}, \mathbf{v} + d\mathbf{v}]$ is:

$$
P(\mathbf{v})\,d^3v = \left(\frac{m}{2\pi k_BT}\right)^{3/2}\exp\left(-\frac{m(v_x^2 + v_y^2 + v_z^2)}{2k_BT}\right)dv_x\,dv_y\,dv_z
$$

This is a product of three independent Gaussian distributions (one for each component), reflecting the isotropy of the equilibrium state.

#### Step 2: Convert to Spherical Coordinates in Velocity Space

In spherical coordinates: $d^3v = v^2\sin\theta\,dv\,d\theta\,d\phi$ where $v = |\mathbf{v}| = \sqrt{v_x^2 + v_y^2 + v_z^2}$.

The speed distribution $f(v)\,dv$ is the probability of finding a molecule with speed between $v$ and $v + dv$, regardless of direction. Integrate over all angles:

$$
f(v)\,dv = \left(\frac{m}{2\pi k_BT}\right)^{3/2}\exp\left(-\frac{mv^2}{2k_BT}\right)\left[\int_0^\pi\sin\theta\,d\theta\int_0^{2\pi}d\phi\right]v^2\,dv
$$

#### Step 3: Evaluate the Angular Integrals

$$
\int_0^\pi\sin\theta\,d\theta = [-\cos\theta]_0^\pi = -(-1) + 1 = 2
$$

$$
\int_0^{2\pi}d\phi = 2\pi
$$

Total solid angle: $4\pi$ (as expected — the surface area of a unit sphere).

#### Step 4: The Speed Distribution

$$
\boxed{f(v) = 4\pi\left(\frac{m}{2\pi k_BT}\right)^{3/2}v^2\exp\left(-\frac{mv^2}{2k_BT}\right)}
$$

The factor $4\pi v^2$ is the "density of states" in velocity space — it counts how many velocity vectors have magnitude between $v$ and $v + dv$. This factor is responsible for the distribution going to zero at $v = 0$ (despite the Boltzmann factor being maximum there) and creates the characteristic peak.

#### Step 5: Verify Normalization

$$
\int_0^\infty f(v)\,dv = 4\pi\left(\frac{m}{2\pi k_BT}\right)^{3/2}\int_0^\infty v^2 e^{-mv^2/(2k_BT)}\,dv
$$

Using the Gaussian integral $\int_0^\infty x^2 e^{-ax^2}\,dx = \frac{\sqrt{\pi}}{4a^{3/2}}$ with $a = m/(2k_BT)$:

$$
= 4\pi\left(\frac{m}{2\pi k_BT}\right)^{3/2}\cdot\frac{\sqrt{\pi}}{4}\left(\frac{2k_BT}{m}\right)^{3/2} = 4\pi\cdot\frac{1}{(2\pi)^{3/2}}\cdot\frac{\sqrt{\pi}}{4}\cdot(2\pi)^{3/2}\cdot\frac{1}{\pi} = 1 \quad \checkmark
$$

</details>

---

### Example 8.2 — Mean Speed, RMS Speed, and Most Probable Speed

**Problem.** For the Maxwell-Boltzmann speed distribution, derive exact expressions for: (a) the most probable speed $v_p$, (b) the mean speed $\langle v\rangle$, (c) the root-mean-square speed $v_{\text{rms}}$. Show that $v_p < \langle v\rangle < v_{\text{rms}}$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

Define $\alpha = m/(2k_BT)$ for convenience. Then $f(v) = 4\pi\left(\frac{\alpha}{\pi}\right)^{3/2}v^2 e^{-\alpha v^2}$.

#### Part (a): Most Probable Speed $v_p$

Set $df/dv = 0$:

$$
\frac{d}{dv}[v^2 e^{-\alpha v^2}] = 2v e^{-\alpha v^2} + v^2(-2\alpha v)e^{-\alpha v^2} = 0
$$

$$
2v e^{-\alpha v^2}[1 - \alpha v^2] = 0
$$

Non-trivial solution: $\alpha v_p^2 = 1$:

$$
\boxed{v_p = \sqrt{\frac{1}{\alpha}} = \sqrt{\frac{2k_BT}{m}}}
$$

#### Part (b): Mean Speed $\langle v\rangle$

$$
\langle v\rangle = \int_0^\infty v\,f(v)\,dv = 4\pi\left(\frac{\alpha}{\pi}\right)^{3/2}\int_0^\infty v^3 e^{-\alpha v^2}\,dv
$$

Use the integral $\int_0^\infty v^3 e^{-\alpha v^2}\,dv = \frac{1}{2\alpha^2}$:

$$
\langle v\rangle = 4\pi\left(\frac{\alpha}{\pi}\right)^{3/2}\cdot\frac{1}{2\alpha^2} = 4\pi\cdot\frac{\alpha^{3/2}}{\pi^{3/2}}\cdot\frac{1}{2\alpha^2} = \frac{4\pi}{2\pi^{3/2}\alpha^{1/2}} = \frac{2}{\sqrt{\pi\alpha}}
$$

$$
\boxed{\langle v\rangle = \sqrt{\frac{8k_BT}{\pi m}} = \frac{2}{\sqrt{\pi}}v_p \approx 1.128\,v_p}
$$

#### Part (c): RMS Speed $v_{\text{rms}}$

$$
\langle v^2\rangle = \int_0^\infty v^2\,f(v)\,dv = 4\pi\left(\frac{\alpha}{\pi}\right)^{3/2}\int_0^\infty v^4 e^{-\alpha v^2}\,dv
$$

Use the integral $\int_0^\infty v^4 e^{-\alpha v^2}\,dv = \frac{3\sqrt{\pi}}{8\alpha^{5/2}}$:

$$
\langle v^2\rangle = 4\pi\cdot\frac{\alpha^{3/2}}{\pi^{3/2}}\cdot\frac{3\sqrt{\pi}}{8\alpha^{5/2}} = \frac{4\pi\cdot 3}{8\pi\alpha} = \frac{3}{2\alpha} = \frac{3k_BT}{m}
$$

$$
\boxed{v_{\text{rms}} = \sqrt{\langle v^2\rangle} = \sqrt{\frac{3k_BT}{m}} = \sqrt{\frac{3}{2}}\,v_p \approx 1.225\,v_p}
$$

#### Summary and Ordering

$$
v_p : \langle v\rangle : v_{\text{rms}} = 1 : \frac{2}{\sqrt{\pi}} : \sqrt{\frac{3}{2}} = 1 : 1.128 : 1.225
$$

$$
v_p \lt  \langle v\rangle \lt  v_{\text{rms}} \quad \checkmark
$$

The ordering reflects the asymmetry (right-skewness) of the speed distribution: the long high-speed tail pulls the mean above the mode, and the RMS (which weights high speeds more heavily via $v^2$) is pulled even higher.

**Physical check:** For N₂ at 300 K ($m = 4.65\times10^{-26}\,\text{kg}$):
- $v_p = \sqrt{2(1.381\times10^{-23})(300)/(4.65\times10^{-26})} = 422\,\text{m/s}$
- $\langle v\rangle = 476\,\text{m/s}$
- $v_{\text{rms}} = 517\,\text{m/s}$

</details>

---

### Example 8.3 — Effusion Rate and the Velocity Distribution of Escaping Molecules

**Problem.** A container of ideal gas at temperature $T$ has a small hole of area $A$ (diameter $\ll$ mean free path). (a) Derive the effusion rate (molecules per second). (b) Show that the escaping molecules have a different speed distribution than the bulk gas, with $\langle v\rangle_{\text{eff}} = \frac{3\pi}{8}\langle v\rangle_{\text{bulk}}$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Part (a): Effusion Rate

Consider molecules approaching the hole from the left. A molecule with velocity component $v_x \gt  0$ (moving toward the hole) will escape if it reaches the hole within time $dt$.

The flux (molecules per unit area per unit time) hitting the wall is:

$$
\Phi = n\langle v_x\rangle_{v_x \gt  0}
$$

where $n$ is the number density and the average is over molecules moving toward the wall only.

For the Maxwell-Boltzmann distribution, the $x$-component distribution is:

$$
g(v_x) = \sqrt{\frac{m}{2\pi k_BT}}\exp\left(-\frac{mv_x^2}{2k_BT}\right)
$$

The average of $v_x$ over positive values only:

$$
\langle v_x\rangle_{v_x \gt  0} = \frac{\int_0^\infty v_x\,g(v_x)\,dv_x}{\int_0^\infty g(v_x)\,dv_x}
$$

Numerator: $\int_0^\infty v_x\sqrt{\frac{m}{2\pi k_BT}}e^{-mv_x^2/(2k_BT)}\,dv_x = \sqrt{\frac{m}{2\pi k_BT}}\cdot\frac{k_BT}{m} = \sqrt{\frac{k_BT}{2\pi m}}$

Denominator: $\int_0^\infty g(v_x)\,dv_x = 1/2$ (half the normalized distribution).

But actually, the flux is simply:

$$
\Phi = n\int_0^\infty v_x\,g(v_x)\,dv_x = n\sqrt{\frac{k_BT}{2\pi m}} = \frac{n\langle v\rangle}{4}
$$

where we used $\langle v\rangle = \sqrt{8k_BT/(\pi m)}$, so $\sqrt{k_BT/(2\pi m)} = \langle v\rangle/4$.

The effusion rate (molecules per second through area $A$):

$$
\boxed{\dot{N} = \Phi A = \frac{1}{4}n\langle v\rangle A}
$$

#### Part (b): Speed Distribution of Escaping Molecules

The probability that an escaping molecule has speed $v$ is proportional to $v \cdot f(v)$ (faster molecules hit the wall more often):

$$
f_{\text{eff}}(v) \propto v\cdot f(v) \propto v^3 e^{-mv^2/(2k_BT)}
$$

Normalizing: $\int_0^\infty v^3 e^{-\alpha v^2}\,dv = 1/(2\alpha^2)$, so:

$$
f_{\text{eff}}(v) = 2\alpha^2 v^3 e^{-\alpha v^2} = \frac{m^2}{2(k_BT)^2}v^3\exp\left(-\frac{mv^2}{2k_BT}\right)
$$

The mean speed of escaping molecules:

$$
\langle v\rangle_{\text{eff}} = \int_0^\infty v\,f_{\text{eff}}(v)\,dv = 2\alpha^2\int_0^\infty v^4 e^{-\alpha v^2}\,dv = 2\alpha^2\cdot\frac{3\sqrt{\pi}}{8\alpha^{5/2}} = \frac{3\sqrt{\pi}}{4\sqrt{\alpha}}
$$

$$
= \frac{3\sqrt{\pi}}{4}\sqrt{\frac{2k_BT}{m}} = \frac{3\sqrt{\pi}}{4}v_p = \frac{3\pi}{8}\cdot\frac{2v_p}{\sqrt{\pi}} \cdot \frac{\sqrt{\pi}}{2}
$$

Let me compute this more carefully:

$$
\langle v\rangle_{\text{eff}} = \frac{3\sqrt{\pi}}{4\sqrt{\alpha}} = \frac{3\sqrt{\pi}}{4}\sqrt{\frac{2k_BT}{m}}
$$

Compare with $\langle v\rangle_{\text{bulk}} = \sqrt{\frac{8k_BT}{\pi m}} = 2\sqrt{\frac{2k_BT}{\pi m}}$:

$$
\frac{\langle v\rangle_{\text{eff}}}{\langle v\rangle_{\text{bulk}}} = \frac{\frac{3\sqrt{\pi}}{4}\sqrt{\frac{2k_BT}{m}}}{2\sqrt{\frac{2k_BT}{\pi m}}} = \frac{3\sqrt{\pi}/4}{2/\sqrt{\pi}} = \frac{3\pi}{8}
$$

$$
\boxed{\langle v\rangle_{\text{eff}} = \frac{3\pi}{8}\langle v\rangle_{\text{bulk}} \approx 1.18\,\langle v\rangle_{\text{bulk}}}
$$

The escaping molecules are on average 18% faster than the bulk. This makes physical sense: faster molecules hit the wall more frequently and are therefore over-represented in the effusing beam.

**Consequence:** Effusion preferentially removes fast (high-energy) molecules, cooling the remaining gas. This is the principle behind evaporative cooling.

</details>

---

### Example 8.4 — Energy Distribution and the Boltzmann Factor

**Problem.** Derive the distribution of molecular kinetic energies $g(\epsilon)$ from the speed distribution. Show that $g(\epsilon) \propto \sqrt{\epsilon}\,e^{-\epsilon/(k_BT)}$ and compute $\langle\epsilon\rangle$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Change of Variables

The kinetic energy is $\epsilon = \frac{1}{2}mv^2$, so $v = \sqrt{2\epsilon/m}$ and $dv = \frac{1}{2}\sqrt{\frac{2}{m\epsilon}}\,d\epsilon = \frac{d\epsilon}{\sqrt{2m\epsilon}}$.

The energy distribution $g(\epsilon)\,d\epsilon = f(v)\,dv$:

$$
g(\epsilon) = f(v)\frac{dv}{d\epsilon} = 4\pi\left(\frac{m}{2\pi k_BT}\right)^{3/2}\cdot\frac{2\epsilon}{m}\cdot e^{-\epsilon/(k_BT)}\cdot\frac{1}{\sqrt{2m\epsilon}}
$$

$$
= 4\pi\left(\frac{m}{2\pi k_BT}\right)^{3/2}\cdot\frac{2\epsilon}{m}\cdot\frac{1}{\sqrt{2m\epsilon}}\cdot e^{-\epsilon/(k_BT)}
$$

$$
= 4\pi\left(\frac{m}{2\pi k_BT}\right)^{3/2}\cdot\frac{2\sqrt{\epsilon}}{m\sqrt{2m}}\cdot e^{-\epsilon/(k_BT)}
$$

Simplifying:

$$
= 4\pi\cdot\frac{m^{3/2}}{(2\pi k_BT)^{3/2}}\cdot\frac{2\sqrt{\epsilon}}{m^{3/2}\sqrt{2}}\cdot e^{-\epsilon/(k_BT)} = \frac{4\pi\cdot 2}{(2\pi k_BT)^{3/2}\sqrt{2}}\sqrt{\epsilon}\,e^{-\epsilon/(k_BT)}
$$

$$
= \frac{2\pi}{(\pi k_BT)^{3/2}}\sqrt{\epsilon}\,e^{-\epsilon/(k_BT)}
$$

$$
\boxed{g(\epsilon) = \frac{2\pi}{(\pi k_BT)^{3/2}}\sqrt{\epsilon}\,e^{-\epsilon/(k_BT)}}
$$

#### Step 2: Compute $\langle\epsilon\rangle$

$$
\langle\epsilon\rangle = \int_0^\infty \epsilon\,g(\epsilon)\,d\epsilon = \frac{2\pi}{(\pi k_BT)^{3/2}}\int_0^\infty \epsilon^{3/2}e^{-\epsilon/(k_BT)}\,d\epsilon
$$

Substitute $u = \epsilon/(k_BT)$: $d\epsilon = k_BT\,du$:

$$
= \frac{2\pi}{(\pi k_BT)^{3/2}}\cdot(k_BT)^{5/2}\int_0^\infty u^{3/2}e^{-u}\,du = \frac{2\pi(k_BT)^{5/2}}{(\pi k_BT)^{3/2}}\cdot\Gamma(5/2)
$$

$$
= \frac{2(k_BT)}{\sqrt{\pi}}\cdot\frac{3\sqrt{\pi}}{4} = \frac{3}{2}k_BT
$$

$$
\boxed{\langle\epsilon\rangle = \frac{3}{2}k_BT}
$$

This is the equipartition result: $\frac{1}{2}k_BT$ per translational degree of freedom, times 3 dimensions.

</details>



---

## 📘 9. Appendix: Extended Derivations & Special Cases

### Appendix 9.1 — Derivation of Pressure from Kinetic Theory: $P = \frac{1}{3}nm\langle v^2\rangle$

This is one of the most beautiful results in physics: the macroscopic pressure of a gas derived from the microscopic collisions of individual molecules with the container walls.

**Setup.** Consider an ideal gas of $N$ molecules, each of mass $m$, in a cubic container of side $L$ (volume $V = L^3$). We compute the force exerted on one wall (say, the wall at $x = L$) by molecular impacts.

**Step 1: Force from a single molecule.**

Consider a molecule with $x$-component of velocity $v_x > 0$ approaching the wall at $x = L$. Upon elastic collision with the wall, $v_x \to -v_x$ (the $y$ and $z$ components are unchanged).

Change in momentum per collision:

$$
\Delta p_x = (-mv_x) - (mv_x) = -2mv_x
$$

The momentum transferred TO the wall per collision is $+2mv_x$.

**Step 2: Collision frequency for one molecule.**

The molecule travels a distance $2L$ between successive collisions with the same wall (it must cross the box and return). Time between collisions:

$$
\Delta t = \frac{2L}{v_x}
$$

Force exerted on the wall by this one molecule (time-averaged):

$$
F_1 = \frac{\Delta p_{\text{wall}}}{\Delta t} = \frac{2mv_x}{2L/v_x} = \frac{mv_x^2}{L}
$$

**Step 3: Total force from all molecules.**

Sum over all $N$ molecules:

$$
F = \sum_{i=1}^N \frac{mv_{x,i}^2}{L} = \frac{Nm\langle v_x^2\rangle}{L}
$$

where $\langle v_x^2\rangle = \frac{1}{N}\sum_i v_{x,i}^2$ is the average of $v_x^2$ over all molecules.

**Step 4: Relate $\langle v_x^2\rangle$ to $\langle v^2\rangle$.**

By isotropy (no preferred direction): $\langle v_x^2\rangle = \langle v_y^2\rangle = \langle v_z^2\rangle$.

Since $v^2 = v_x^2 + v_y^2 + v_z^2$:

$$
\langle v^2\rangle = \langle v_x^2\rangle + \langle v_y^2\rangle + \langle v_z^2\rangle = 3\langle v_x^2\rangle
$$

$$
\langle v_x^2\rangle = \frac{1}{3}\langle v^2\rangle
$$

**Step 5: Pressure.**

$$
P = \frac{F}{A} = \frac{F}{L^2} = \frac{Nm\langle v_x^2\rangle}{L \cdot L^2} = \frac{Nm\langle v_x^2\rangle}{V} = \frac{Nm}{3V}\langle v^2\rangle
$$

With number density $n = N/V$:

$$
\boxed{P = \frac{1}{3}nm\langle v^2\rangle = \frac{1}{3}\rho\langle v^2\rangle}
$$

where $\rho = nm$ is the mass density.

**Step 6: Connection to temperature.**

From the ideal gas law: $P = nk_BT$. Equating:

$$
nk_BT = \frac{1}{3}nm\langle v^2\rangle \implies \frac{1}{2}m\langle v^2\rangle = \frac{3}{2}k_BT
$$

This is the **equipartition theorem** for translational kinetic energy: each of the 3 translational degrees of freedom carries average energy $\frac{1}{2}k_BT$.

**Historical note:** This derivation was first given by Daniel Bernoulli (1738), over a century before Maxwell and Boltzmann developed the full kinetic theory. It was largely ignored because the atomic hypothesis was not yet accepted.

**Reference:** Maxwell, "Illustrations of the Dynamical Theory of Gases" (1860); Reif, *Fundamentals*, Ch. 7; Kittel & Kroemer, *Thermal Physics*, Ch. 14.

---

### Appendix 9.2 — Transport Properties from Kinetic Theory: Viscosity, Thermal Conductivity, and Diffusion

Kinetic theory predicts not only equilibrium properties (pressure, temperature) but also transport coefficients. All three major transport properties share the same structure:

$$
\text{Transport coefficient} \sim \frac{1}{3}\langle v\rangle\,\ell\,(\text{relevant density})
$$

where $\ell$ is the mean free path and $\langle v\rangle$ is the mean molecular speed.

**Viscosity $\eta$** (momentum transport):

Consider a gas with a velocity gradient $du_x/dy$ (bulk flow in $x$-direction varying in $y$). Molecules crossing a plane at $y = y_0$ carry momentum from their last collision (at distance $\sim \ell$):

$$
\text{Momentum flux} = \frac{1}{3}nm\langle v\rangle\ell\frac{du_x}{dy}
$$

$$
\boxed{\eta = \frac{1}{3}nm\langle v\rangle\ell = \frac{1}{3}\rho\langle v\rangle\ell}
$$

Since $\ell = 1/(\sqrt{2}n\sigma)$ and $\langle v\rangle \propto \sqrt{T}$:

$$
\eta = \frac{m\langle v\rangle}{3\sqrt{2}\sigma} \propto \frac{\sqrt{mT}}{\sigma}
$$

Key prediction: $\eta$ is **independent of pressure** (at moderate pressures). This counterintuitive result (confirmed by Maxwell experimentally) occurs because increasing $n$ increases the number of momentum carriers but decreases $\ell$ proportionally.

**Thermal conductivity $\kappa$** (energy transport):

$$
\boxed{\kappa = \frac{1}{3}nC_V^{\text{mol}}\langle v\rangle\ell = \frac{1}{3}\rho c_V\langle v\rangle\ell}
$$

where $c_V$ is the specific heat per unit mass.

**Diffusion coefficient $D$** (mass transport):

$$
\boxed{D = \frac{1}{3}\langle v\rangle\ell}
$$

**Relations between transport coefficients:**

$$
\eta = \rho D, \qquad \kappa = \rho c_V D = c_V\eta
$$

These relations (with numerical prefactors of order unity) are confirmed experimentally and represent one of the great triumphs of kinetic theory.

**Reference:** Chapman & Cowling, *The Mathematical Theory of Non-Uniform Gases*; Reif, *Fundamentals*, Ch. 12; David Tong, *Kinetic Theory* Notes.

---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

*Previous: [5.6 - The Partition Function & Free Energy](5.6---The-Partition-Function-&-Free-Energy) | Next: [5.8 - Quantum Statistics - Bose-Einstein & Fermi-Dirac](5.8---Quantum-Statistics---Bose-Einstein-&-Fermi-Dirac)*



---

### Appendix 9.3 — Equipartition Theorem: Statement, Proof, and Breakdown

The equipartition theorem is the bridge between microscopic degrees of freedom and macroscopic heat capacity. Here we state it precisely and identify when it fails.

**Theorem (Equipartition).** For a classical system in thermal equilibrium at temperature $T$, each quadratic term in the Hamiltonian contributes $\frac{1}{2}k_BT$ to the average energy.

**Proof.** Consider a single quadratic term $\epsilon = \alpha q^2$ (where $q$ is a generalized coordinate or momentum and $\alpha$ is a constant). The thermal average:

$$
\langle\alpha q^2\rangle = \frac{\int_{-\infty}^{\infty}\alpha q^2\,e^{-\beta\alpha q^2}\,dq}{\int_{-\infty}^{\infty}e^{-\beta\alpha q^2}\,dq}
$$

The numerator: $\alpha\int q^2 e^{-\beta\alpha q^2}\,dq = \alpha\cdot\frac{\sqrt{\pi}}{2(\beta\alpha)^{3/2}} = \frac{\sqrt{\pi}}{2\beta\sqrt{\beta\alpha}}$.

The denominator: $\int e^{-\beta\alpha q^2}\,dq = \sqrt{\pi/(\beta\alpha)}$.

$$
\langle\alpha q^2\rangle = \frac{\sqrt{\pi}/(2\beta\sqrt{\beta\alpha})}{\sqrt{\pi/(\beta\alpha)}} = \frac{1}{2\beta} = \frac{1}{2}k_BT \quad \blacksquare
$$

**Applications:**
- Monatomic ideal gas: $H = \sum_i p_i^2/(2m)$ — 3 quadratic terms per particle → $\langle E\rangle = \frac{3}{2}Nk_BT$, $C_V = \frac{3}{2}Nk_B$.
- Diatomic gas (high $T$): 3 translational + 2 rotational + 2 vibrational (1 KE + 1 PE) = 7 quadratic terms → $C_V = \frac{7}{2}Nk_B$.
- Harmonic solid: 3 KE + 3 PE per atom = 6 quadratic terms → $C_V = 3Nk_B$ (Dulong-Petit).

**When equipartition fails (quantum freeze-out):**

Equipartition requires $k_BT \gg \Delta\epsilon$ (the energy level spacing). When $k_BT \lesssim \Delta\epsilon$, the degree of freedom "freezes out":

- **Vibrations** freeze out below $T \sim \Theta_{\text{vib}} = \hbar\omega/(k_B) \sim 1000$–$5000\,\text{K}$ for molecules.
- **Rotations** freeze out below $T \sim \Theta_{\text{rot}} = \hbar^2/(2Ik_B) \sim 2$–$100\,\text{K}$ for molecules.
- **Electronic excitations** freeze out below $T \sim 10^4\,\text{K}$ (typical electronic energy gaps).

This explains the temperature dependence of $C_V$ for diatomic gases: $\frac{3}{2}R$ at low $T$ (translation only), $\frac{5}{2}R$ at moderate $T$ (+ rotation), $\frac{7}{2}R$ at high $T$ (+ vibration). The transitions between these plateaus are smooth, governed by the quantum partition functions for each degree of freedom.

**Reference:** Kittel & Kroemer, *Thermal Physics*, Ch. 3; Reif, *Fundamentals*, Ch. 7; Susskind, *Statistical Mechanics* Lecture 5.
