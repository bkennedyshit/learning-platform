---
title: "12.3 — Hooke's Law & Material Properties"
subject: "Solid Mechanics & Materials Science"
catalog: advanced
audience_tier: higher-education
chapter: "12.3"
type: chapter-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 12.3 — Hooke's Law & Material Properties

> *"Ut tensio, sic vis — As the extension, so the force."*
> — **Robert Hooke** (1678), *De Potentia Restitutiva*

Hooke's Law is the constitutive equation that bridges the gap between stress (cause) and strain (effect) for linearly elastic materials. This chapter develops the full generalized Hooke's Law in tensor form, introduces the elastic constants that characterize material behavior, and explores the stress-strain curve beyond the elastic limit.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. State Hooke's Law in 1D, 2D (plane stress/strain), and full 3D tensor form.
2. Define and relate the elastic constants: $E$, $\nu$, $G$, $K$, $\lambda$.
3. Write the **stiffness tensor** $C_{ijkl}$ and **compliance tensor** $S_{ijkl}$ for isotropic materials.
4. Compute strains from a given 3D stress state (and vice versa) using generalized Hooke's Law.
5. Interpret the stress-strain curve: proportional limit, yield point, ultimate strength, fracture.
6. Distinguish elastic, plastic, brittle, and ductile material behavior.

---

## 🖼️ Visual Anchor — Stress-Strain Curve with Material Regions

![math-12__12.3-fig1](math-12__12.3-fig1.svg)

---

## 📚 1. Definitions

### Definition 12.3.1 — Young's Modulus (Modulus of Elasticity)

**Young's modulus** $E$ is the ratio of uniaxial stress to uniaxial strain in the linear elastic region:

$$
E = \frac{\sigma}{\varepsilon} \quad \text{[Pa]}
$$

It represents the **stiffness** of a material — resistance to elastic deformation.

| Material | $E$ (GPa) |
|:---|:---|
| Steel | 200 |
| Aluminum | 70 |
| Copper | 120 |
| Concrete | 30 |
| Wood (along grain) | 12 |
| Rubber | 0.01–0.1 |

### Definition 12.3.2 — Poisson's Ratio

**Poisson's ratio** $\nu$ is the negative ratio of transverse strain to axial strain under uniaxial loading:

$$
\nu = -\frac{\varepsilon_{\text{transverse}}}{\varepsilon_{\text{axial}}} = -\frac{\varepsilon_y}{\varepsilon_x} \quad \text{(for loading in } x\text{)}
$$

For most engineering materials: $0 < \nu < 0.5$. Typical values: steel ≈ 0.3, rubber ≈ 0.5 (incompressible), cork ≈ 0.

### Definition 12.3.3 — Shear Modulus (Modulus of Rigidity)

The **shear modulus** $G$ relates shear stress to shear strain:

$$
\tau = G\gamma
$$

For isotropic materials, $G$ is not independent:

$$
G = \frac{E}{2(1 + \nu)}
$$

### Definition 12.3.4 — Bulk Modulus

The **bulk modulus** $K$ relates hydrostatic stress to volumetric strain:

$$
K = \frac{\sigma_m}{e} = \frac{E}{3(1 - 2\nu)}
$$

where $\sigma_m$ is the mean stress and $e = \varepsilon_{kk}$ is the volumetric strain.

### Definition 12.3.5 — Lamé Constants

The **Lamé constants** $\lambda$ and $\mu$ (where $\mu = G$) parameterize the generalized Hooke's Law:

$$
\lambda = \frac{E\nu}{(1+\nu)(1-2\nu)}, \quad \mu = G = \frac{E}{2(1+\nu)}
$$

### Definition 12.3.6 — Generalized Hooke's Law (3D, Isotropic)

For a linear elastic, isotropic material:

**Stress → Strain (Compliance form):**

$$
\varepsilon_{xx} = \frac{1}{E}\left[\sigma_{xx} - \nu(\sigma_{yy} + \sigma_{zz})\right]
$$

$$
\varepsilon_{yy} = \frac{1}{E}\left[\sigma_{yy} - \nu(\sigma_{xx} + \sigma_{zz})\right]
$$

$$
\varepsilon_{zz} = \frac{1}{E}\left[\sigma_{zz} - \nu(\sigma_{xx} + \sigma_{yy})\right]
$$

$$
\gamma_{xy} = \frac{\tau_{xy}}{G}, \quad \gamma_{yz} = \frac{\tau_{yz}}{G}, \quad \gamma_{xz} = \frac{\tau_{xz}}{G}
$$

**Strain → Stress (Stiffness form, using Lamé constants):**

$$
\sigma_{ij} = \lambda \varepsilon_{kk} \delta_{ij} + 2\mu \varepsilon_{ij}
$$

Expanded:

$$
\sigma_{xx} = \lambda(\varepsilon_{xx} + \varepsilon_{yy} + \varepsilon_{zz}) + 2\mu\varepsilon_{xx}
$$

$$
\tau_{xy} = 2\mu\varepsilon_{xy} = \mu\gamma_{xy} = G\gamma_{xy}
$$

### Definition 12.3.7 — Elastic Strain Energy Density

The **strain energy density** (energy stored per unit volume) in a linearly elastic material:

$$
u = \frac{1}{2}\sigma_{ij}\varepsilon_{ij} = \frac{1}{2}\boldsymbol{\sigma}:\boldsymbol{\varepsilon}
$$

For uniaxial stress: $u = \frac{\sigma^2}{2E} = \frac{1}{2}E\varepsilon^2$.




---

## 📐 2. Axioms / Postulates

### Postulate 12.3.P1 — Linear Elasticity

Within the elastic region, stress is a **linear** function of strain. The material returns to its original shape upon unloading (no permanent deformation).

### Postulate 12.3.P2 — Isotropy

An **isotropic** material has identical mechanical properties in all directions. Its constitutive behavior is characterized by exactly **two** independent elastic constants (e.g., $E$ and $\nu$).

### Postulate 12.3.P3 — Homogeneity

Material properties are uniform throughout the body (do not vary with position).

### Postulate 12.3.P4 — Superposition

For linear elastic materials, the effects of multiple loads can be superimposed: the total stress/strain equals the sum of individual contributions.

### Postulate 12.3.P5 — Positive-Definiteness of Strain Energy

The strain energy density must be positive for any non-zero strain state:

$$
u = \frac{1}{2}C_{ijkl}\varepsilon_{ij}\varepsilon_{kl} > 0 \quad \forall\, \boldsymbol{\varepsilon} \neq \mathbf{0}
$$

This imposes thermodynamic constraints on elastic constants:

$$
E > 0, \quad -1 < \nu < 0.5, \quad G > 0, \quad K > 0
$$

---

## 🛡️ 3. Lemmas

### Lemma 12.3.1 — Relationship Between Elastic Constants

For an isotropic material, only **two** constants are independent. All others can be derived:

$$
G = \frac{E}{2(1+\nu)}
$$

$$
K = \frac{E}{3(1-2\nu)}
$$

$$
\lambda = \frac{E\nu}{(1+\nu)(1-2\nu)} = K - \frac{2G}{3}
$$

$$
E = \frac{9KG}{3K+G}, \quad \nu = \frac{3K-2G}{2(3K+G)}
$$

<details>
<summary>🔍 Derivation of $G = E/[2(1+\nu)]$</summary>

Consider a state of **pure shear**: $\sigma_{xx} = \tau$, $\sigma_{yy} = -\tau$, $\tau_{xy} = 0$ (principal stresses at 45° to the shear plane).

Alternatively, consider the element rotated 45°. In the original frame, this corresponds to $\tau_{xy} = \tau$ with $\sigma_{xx} = \sigma_{yy} = 0$.

From generalized Hooke's Law in the principal stress frame:

$$
\varepsilon_1 = \frac{1}{E}[\sigma_1 - \nu\sigma_2] = \frac{1}{E}[\tau - \nu(-\tau)] = \frac{\tau(1+\nu)}{E}
$$

$$
\varepsilon_2 = \frac{1}{E}[\sigma_2 - \nu\sigma_1] = \frac{1}{E}[-\tau - \nu\tau] = -\frac{\tau(1+\nu)}{E}
$$

The maximum shear strain (at 45° to principal directions) is:

$$
\gamma_{\max} = \varepsilon_1 - \varepsilon_2 = \frac{2\tau(1+\nu)}{E}
$$

But by definition of shear modulus: $\gamma = \tau/G$, so:

$$
\frac{\tau}{G} = \frac{2\tau(1+\nu)}{E}
$$

$$
G = \frac{E}{2(1+\nu)} \quad \blacksquare
$$

</details>

### Lemma 12.3.2 — Plane Stress Constitutive Relations

For plane stress ($\sigma_{zz} = \tau_{xz} = \tau_{yz} = 0$):

$$
\begin{pmatrix} \varepsilon_{xx} \\ \varepsilon_{yy} \\ \gamma_{xy} \end{pmatrix} = \frac{1}{E}\begin{pmatrix} 1 & -\nu & 0 \\ -\nu & 1 & 0 \\ 0 & 0 & 2(1+\nu) \end{pmatrix}\begin{pmatrix} \sigma_{xx} \\ \sigma_{yy} \\ \tau_{xy} \end{pmatrix}
$$

Inverted (stiffness form):

$$
\begin{pmatrix} \sigma_{xx} \\ \sigma_{yy} \\ \tau_{xy} \end{pmatrix} = \frac{E}{1-\nu^2}\begin{pmatrix} 1 & \nu & 0 \\ \nu & 1 & 0 \\ 0 & 0 & \frac{1-\nu}{2} \end{pmatrix}\begin{pmatrix} \varepsilon_{xx} \\ \varepsilon_{yy} \\ \gamma_{xy} \end{pmatrix}
$$

Note: Even in plane stress, $\varepsilon_{zz} \neq 0$:

$$
\varepsilon_{zz} = -\frac{\nu}{E}(\sigma_{xx} + \sigma_{yy})
$$

### Lemma 12.3.3 — Plane Strain Constitutive Relations

For plane strain ($\varepsilon_{zz} = \gamma_{xz} = \gamma_{yz} = 0$):

$$
\sigma_{zz} = \nu(\sigma_{xx} + \sigma_{yy}) \neq 0
$$

$$
\begin{pmatrix} \sigma_{xx} \\ \sigma_{yy} \\ \tau_{xy} \end{pmatrix} = \frac{E}{(1+\nu)(1-2\nu)}\begin{pmatrix} 1-\nu & \nu & 0 \\ \nu & 1-\nu & 0 \\ 0 & 0 & \frac{1-2\nu}{2} \end{pmatrix}\begin{pmatrix} \varepsilon_{xx} \\ \varepsilon_{yy} \\ \gamma_{xy} \end{pmatrix}
$$

---

## 👑 4. Theorems

### Theorem 12.3.1 — Generalized Hooke's Law (Tensor Form)

For a linear elastic material, the most general constitutive relation is:

$$
\sigma_{ij} = C_{ijkl}\,\varepsilon_{kl}
$$

where $C_{ijkl}$ is the **fourth-order stiffness tensor** with 81 components. Symmetry reduces independent components:
- $\sigma_{ij} = \sigma_{ji}$ → $C_{ijkl} = C_{jikl}$ (reduces to 54)
- $\varepsilon_{kl} = \varepsilon_{lk}$ → $C_{ijkl} = C_{ijlk}$ (reduces to 36)
- Strain energy symmetry → $C_{ijkl} = C_{klij}$ (reduces to 21)
- **Isotropy** → reduces to **2** independent constants

For isotropic materials:

$$
C_{ijkl} = \lambda\,\delta_{ij}\delta_{kl} + \mu(\delta_{ik}\delta_{jl} + \delta_{il}\delta_{jk})
$$

### Theorem 12.3.2 — Uniqueness of Elastic Solution (Kirchhoff)

For a linear elastic body with prescribed boundary conditions (tractions and/or displacements), the stress field is **unique**. If the body is also simply connected, the displacement field is unique up to rigid-body motion.

### Theorem 12.3.3 — Clapeyron's Theorem

The strain energy stored in a linear elastic body equals half the work done by external forces:

$$
U = \frac{1}{2}\int_V \sigma_{ij}\varepsilon_{ij}\,dV = \frac{1}{2}\int_S \mathbf{t} \cdot \mathbf{u}\,dS + \frac{1}{2}\int_V \mathbf{b} \cdot \mathbf{u}\,dV
$$

---

## ✍️ 5. Proofs / Derivations

### 5.1 Derivation: Generalized Hooke's Law from Strain Energy

<details>
<summary>🔍 Full Derivation</summary>

For a linear elastic material, the strain energy density is a quadratic function of strain:

$$
u(\boldsymbol{\varepsilon}) = \frac{1}{2}C_{ijkl}\varepsilon_{ij}\varepsilon_{kl}
$$

The stress is obtained by differentiating with respect to strain:

$$
\sigma_{ij} = \frac{\partial u}{\partial \varepsilon_{ij}} = C_{ijkl}\varepsilon_{kl}
$$

For an **isotropic** material, $u$ must be invariant under all rotations. The most general quadratic scalar formed from a symmetric tensor $\boldsymbol{\varepsilon}$ is:

$$
u = \frac{\lambda}{2}(\varepsilon_{kk})^2 + \mu\,\varepsilon_{ij}\varepsilon_{ij}
$$

(These are the only two independent quadratic invariants of a symmetric tensor: $(\text{tr}\,\boldsymbol{\varepsilon})^2$ and $\text{tr}(\boldsymbol{\varepsilon}^2)$.)

Differentiating:

$$
\sigma_{ij} = \frac{\partial u}{\partial \varepsilon_{ij}} = \lambda\varepsilon_{kk}\frac{\partial(\varepsilon_{mm})}{\partial \varepsilon_{ij}} + 2\mu\varepsilon_{ij}
$$

Since $\frac{\partial \varepsilon_{mm}}{\partial \varepsilon_{ij}} = \delta_{ij}$:

$$
\sigma_{ij} = \lambda\varepsilon_{kk}\delta_{ij} + 2\mu\varepsilon_{ij}
$$

This is the **Lamé form** of generalized Hooke's Law. $\blacksquare$

</details>

### 5.2 Derivation: Inverting Hooke's Law (Stress → Strain)

<details>
<summary>🔍 Full Derivation</summary>

Starting from $\sigma_{ij} = \lambda\varepsilon_{kk}\delta_{ij} + 2\mu\varepsilon_{ij}$.

**Step 1:** Take the trace ($i = j$, sum):

$$
\sigma_{kk} = \lambda\varepsilon_{mm}(3) + 2\mu\varepsilon_{kk} = (3\lambda + 2\mu)\varepsilon_{kk}
$$

$$
\varepsilon_{kk} = \frac{\sigma_{kk}}{3\lambda + 2\mu}
$$

**Step 2:** Solve for $\varepsilon_{ij}$:

$$
2\mu\varepsilon_{ij} = \sigma_{ij} - \lambda\varepsilon_{kk}\delta_{ij} = \sigma_{ij} - \frac{\lambda}{3\lambda + 2\mu}\sigma_{kk}\delta_{ij}
$$

$$
\varepsilon_{ij} = \frac{1}{2\mu}\sigma_{ij} - \frac{\lambda}{2\mu(3\lambda + 2\mu)}\sigma_{kk}\delta_{ij}
$$

**Step 3:** Express in terms of $E$ and $\nu$. Using $\mu = \frac{E}{2(1+\nu)}$ and $\lambda = \frac{E\nu}{(1+\nu)(1-2\nu)}$:

$$
\frac{1}{2\mu} = \frac{1+\nu}{E}
$$

$$
\frac{\lambda}{2\mu(3\lambda+2\mu)} = \frac{\nu}{E}
$$

(The second identity requires: $3\lambda + 2\mu = \frac{3E\nu}{(1+\nu)(1-2\nu)} + \frac{E}{1+\nu} = \frac{E(1-\nu)}{(1+\nu)(1-2\nu)} \cdot \frac{3\nu + (1-2\nu)}{1-\nu}$... Let's verify directly: $\frac{\lambda}{3\lambda+2\mu} = \frac{\nu}{1-2\nu} \cdot \frac{(1-2\nu)}{1+\nu} \cdot \frac{(1+\nu)}{1} = \nu$... Actually:

$3\lambda + 2\mu = \frac{3E\nu}{(1+\nu)(1-2\nu)} + \frac{2E}{2(1+\nu)} = \frac{3E\nu + E(1-2\nu)}{(1+\nu)(1-2\nu)} = \frac{E(3\nu + 1 - 2\nu)}{(1+\nu)(1-2\nu)} = \frac{E(1+\nu)}{(1+\nu)(1-2\nu)} = \frac{E}{1-2\nu}$

So $\frac{\lambda}{2\mu(3\lambda+2\mu)} = \frac{E\nu/[(1+\nu)(1-2\nu)]}{[E/(1+\nu)] \cdot [E/(1-2\nu)]} = \frac{E\nu}{(1+\nu)(1-2\nu)} \cdot \frac{(1+\nu)(1-2\nu)}{E^2} = \frac{\nu}{E}$.)

Therefore:

$$
\varepsilon_{ij} = \frac{1+\nu}{E}\sigma_{ij} - \frac{\nu}{E}\sigma_{kk}\delta_{ij}
$$

For $i = j = x$:

$$
\varepsilon_{xx} = \frac{1+\nu}{E}\sigma_{xx} - \frac{\nu}{E}(\sigma_{xx} + \sigma_{yy} + \sigma_{zz}) = \frac{1}{E}[\sigma_{xx} - \nu(\sigma_{yy} + \sigma_{zz})]
$$

This is the standard form. $\blacksquare$

</details>

### 5.3 Derivation: Bulk Modulus from Hydrostatic Loading

<details>
<summary>🔍 Full Derivation</summary>

Apply hydrostatic stress: $\sigma_{xx} = \sigma_{yy} = \sigma_{zz} = -p$ (pressure), all shear stresses zero.

From generalized Hooke's Law:

$$
\varepsilon_{xx} = \frac{1}{E}[-p - \nu(-p - p)] = \frac{-p}{E}(1 - 2\nu)
$$

By symmetry: $\varepsilon_{xx} = \varepsilon_{yy} = \varepsilon_{zz} = \frac{-p(1-2\nu)}{E}$.

Volumetric strain:

$$
e = \varepsilon_{xx} + \varepsilon_{yy} + \varepsilon_{zz} = \frac{-3p(1-2\nu)}{E}
$$

Bulk modulus:

$$
K = \frac{-p}{e} = \frac{-p}{\frac{-3p(1-2\nu)}{E}} = \frac{E}{3(1-2\nu)}
$$

Note: $\nu = 0.5$ gives $K \to \infty$ (incompressible material). $\blacksquare$

</details>

---

## 🧮 6. Worked Examples

### Example 12.3.1 — 3D Stress State: Computing All Strains

**Given:** A steel component ($E = 200$ GPa, $\nu = 0.3$) is subjected to:

$$
\sigma_{xx} = 100 \text{ MPa}, \quad \sigma_{yy} = -50 \text{ MPa}, \quad \sigma_{zz} = 60 \text{ MPa}
$$

$$
\tau_{xy} = 40 \text{ MPa}, \quad \tau_{yz} = 0, \quad \tau_{xz} = 0
$$

**Find:** All six strain components and the volumetric strain.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Compute $G$.**

$$
G = \frac{E}{2(1+\nu)} = \frac{200}{2(1.3)} = 76.92 \text{ GPa}
$$

**Step 2: Normal strains.**

$$
\varepsilon_{xx} = \frac{1}{E}[\sigma_{xx} - \nu(\sigma_{yy} + \sigma_{zz})] = \frac{1}{200\times10^3}[100 - 0.3(-50 + 60)]
$$

$$
= \frac{1}{200000}[100 - 0.3(10)] = \frac{100 - 3}{200000} = \frac{97}{200000} = 4.85 \times 10^{-4}
$$

$$
\varepsilon_{yy} = \frac{1}{E}[\sigma_{yy} - \nu(\sigma_{xx} + \sigma_{zz})] = \frac{1}{200000}[-50 - 0.3(100 + 60)]
$$

$$
= \frac{-50 - 48}{200000} = \frac{-98}{200000} = -4.90 \times 10^{-4}
$$

$$
\varepsilon_{zz} = \frac{1}{E}[\sigma_{zz} - \nu(\sigma_{xx} + \sigma_{yy})] = \frac{1}{200000}[60 - 0.3(100 - 50)]
$$

$$
= \frac{60 - 15}{200000} = \frac{45}{200000} = 2.25 \times 10^{-4}
$$

**Step 3: Shear strains.**

$$
\gamma_{xy} = \frac{\tau_{xy}}{G} = \frac{40}{76920} = 5.20 \times 10^{-4}
$$

$$
\gamma_{yz} = \gamma_{xz} = 0
$$

**Step 4: Volumetric strain.**

$$
e = \varepsilon_{xx} + \varepsilon_{yy} + \varepsilon_{zz} = (4.85 - 4.90 + 2.25) \times 10^{-4} = 2.20 \times 10^{-4}
$$

**Verification via bulk modulus:**

$$
K = \frac{E}{3(1-2\nu)} = \frac{200}{3(0.4)} = 166.7 \text{ GPa}
$$

$$
\sigma_m = \frac{100 - 50 + 60}{3} = 36.67 \text{ MPa}
$$

$$
e = \frac{\sigma_m}{K} = \frac{36.67}{166700} = 2.20 \times 10^{-4} \quad \checkmark
$$

</details>

---

### Example 12.3.2 — Biaxial Stress in a Pressure Vessel

**Given:** A thin-walled cylindrical pressure vessel (steel, $E = 200$ GPa, $\nu = 0.3$) with internal pressure creating:

$$
\sigma_{\text{hoop}} = \sigma_1 = 120 \text{ MPa}, \quad \sigma_{\text{axial}} = \sigma_2 = 60 \text{ MPa}, \quad \sigma_{\text{radial}} \approx 0
$$

**Find:** The hoop strain, axial strain, and radial (through-thickness) strain.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

This is plane stress with $\sigma_3 = 0$ (thin wall).

$$
\varepsilon_1 = \frac{1}{E}[\sigma_1 - \nu(\sigma_2 + \sigma_3)] = \frac{1}{200000}[120 - 0.3(60)] = \frac{120 - 18}{200000} = 5.10 \times 10^{-4}
$$

$$
\varepsilon_2 = \frac{1}{E}[\sigma_2 - \nu(\sigma_1 + \sigma_3)] = \frac{1}{200000}[60 - 0.3(120)] = \frac{60 - 36}{200000} = 1.20 \times 10^{-4}
$$

$$
\varepsilon_3 = \frac{1}{E}[\sigma_3 - \nu(\sigma_1 + \sigma_2)] = \frac{1}{200000}[0 - 0.3(180)] = \frac{-54}{200000} = -2.70 \times 10^{-4}
$$

The wall **thins** ($\varepsilon_3 \lt  0$) while the diameter and length increase.

**Volumetric strain:**

$$
e = 5.10 + 1.20 - 2.70 = 3.60 \times 10^{-4}
$$

</details>

---

### Example 12.3.3 — Determining Material Constants from Test Data

**Given:** A tensile test on an aluminum specimen yields:
- At $\sigma = 70$ MPa: $\varepsilon_{\text{axial}} = 1.0 \times 10^{-3}$, $\varepsilon_{\text{lateral}} = -0.33 \times 10^{-3}$

**Find:** $E$, $\nu$, $G$, $K$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Young's modulus:**

$$
E = \frac{\sigma}{\varepsilon_{\text{axial}}} = \frac{70}{1.0 \times 10^{-3}} = 70{,}000 \text{ MPa} = 70 \text{ GPa}
$$

**Poisson's ratio:**

$$
\nu = -\frac{\varepsilon_{\text{lateral}}}{\varepsilon_{\text{axial}}} = -\frac{-0.33 \times 10^{-3}}{1.0 \times 10^{-3}} = 0.33
$$

**Shear modulus:**

$$
G = \frac{E}{2(1+\nu)} = \frac{70}{2(1.33)} = \frac{70}{2.66} = 26.3 \text{ GPa}
$$

**Bulk modulus:**

$$
K = \frac{E}{3(1-2\nu)} = \frac{70}{3(1-0.66)} = \frac{70}{3(0.34)} = \frac{70}{1.02} = 68.6 \text{ GPa}
$$

</details>

---

### Example 12.3.4 — Strain Energy in a Loaded Bar

**Given:** A steel rod ($E = 200$ GPa) of length $L = 2$ m and cross-sectional area $A = 500$ mm² is subjected to an axial tensile force $P = 50$ kN.

**Find:** The strain energy stored in the rod.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Stress.**

$$
\sigma = \frac{P}{A} = \frac{50 \times 10^3}{500 \times 10^{-6}} = 100 \times 10^6 \text{ Pa} = 100 \text{ MPa}
$$

**Step 2: Strain energy density.**

$$
u = \frac{\sigma^2}{2E} = \frac{(100)^2}{2(200 \times 10^3)} = \frac{10000}{400000} = 0.025 \text{ MPa} = 25 \text{ kJ/m}^3
$$

**Step 3: Total strain energy.**

$$
U = u \cdot V = u \cdot A \cdot L = 25000 \times (500 \times 10^{-6}) \times 2 = 25 \text{ J}
$$

**Alternative:** $U = \frac{P^2 L}{2AE} = \frac{(50000)^2 \times 2}{2 \times 500 \times 10^{-6} \times 200 \times 10^9} = \frac{5 \times 10^9}{2 \times 10^8} = 25$ J ✓

</details>

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- **Previous:** [12.2 - Stress & Strain Tensors](12.2---Stress-&-Strain-Tensors) — Stress and strain definitions
- **Next:** [12.4 - Axial Loading & Torsion](12.4---Axial-Loading-&-Torsion) — Applying Hooke's Law to structural members
- **Tensor operations:** [2.8 - SVD & Tensors](2.8---SVD-&-Tensors) — Fourth-order tensor algebra
- **Thermodynamics:** [5.3 - First Law & Internal Energy](5.3---First-Law-&-Internal-Energy) — Energy storage in elastic deformation

### External Resources
- 📖 **Hibbeler, R.C.** *Mechanics of Materials*, 10th ed. — Chapter 3 (Mechanical Properties of Materials).
- 📖 **Timoshenko & Goodier** — *Theory of Elasticity*, Ch. 4 (Generalized Hooke's Law).
- 🎬 **MIT OCW 3.032** — [Lecture 3: Elasticity](https://ocw.mit.edu/courses/3-032-mechanical-behavior-of-materials-fall-2007/)
- 🎬 **StructureFree** — [Material Properties Playlist](https://www.youtube.com/playlist?list=PL44E9FA04BCEE07C6)

---

## 📎 Appendix: Additional Theory

### A.1 Complete Elastic Constants Conversion Table

| Known | $E$ | $\nu$ | $G$ | $K$ | $\lambda$ |
|:---|:---|:---|:---|:---|:---|
| $E, \nu$ | — | — | $\frac{E}{2(1+\nu)}$ | $\frac{E}{3(1-2\nu)}$ | $\frac{E\nu}{(1+\nu)(1-2\nu)}$ |
| $E, G$ | — | $\frac{E}{2G}-1$ | — | $\frac{EG}{3(3G-E)}$ | $\frac{G(E-2G)}{3G-E}$ |
| $K, G$ | $\frac{9KG}{3K+G}$ | $\frac{3K-2G}{2(3K+G)}$ | — | — | $K-\frac{2G}{3}$ |
| $\lambda, \mu$ | $\frac{\mu(3\lambda+2\mu)}{\lambda+\mu}$ | $\frac{\lambda}{2(\lambda+\mu)}$ | $\mu$ | $\lambda+\frac{2\mu}{3}$ | — |

### A.2 Anisotropic Materials

For **orthotropic** materials (e.g., wood, fiber composites), the stiffness matrix has 9 independent constants:

$$
\begin{pmatrix} \varepsilon_1 \\ \varepsilon_2 \\ \varepsilon_3 \\ \gamma_{23} \\ \gamma_{13} \\ \gamma_{12} \end{pmatrix} = \begin{pmatrix} 1/E_1 & -\nu_{21}/E_2 & -\nu_{31}/E_3 & 0 & 0 & 0 \\ -\nu_{12}/E_1 & 1/E_2 & -\nu_{32}/E_3 & 0 & 0 & 0 \\ -\nu_{13}/E_1 & -\nu_{23}/E_2 & 1/E_3 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1/G_{23} & 0 & 0 \\ 0 & 0 & 0 & 0 & 1/G_{13} & 0 \\ 0 & 0 & 0 & 0 & 0 & 1/G_{12} \end{pmatrix} \begin{pmatrix} \sigma_1 \\ \sigma_2 \\ \sigma_3 \\ \tau_{23} \\ \tau_{13} \\ \tau_{12} \end{pmatrix}
$$

Symmetry requires: $\nu_{ij}/E_i = \nu_{ji}/E_j$.

### A.3 Temperature Effects on Elastic Constants

Young's modulus decreases with temperature (approximately):

$$
E(T) \approx E_0\left(1 - \frac{T - T_0}{T_m}\right) \quad \text{(rough approximation)}
$$

where $T_m$ is the melting temperature. More precisely, for steel:
- At 200°C: $E \approx 190$ GPa (5% reduction)
- At 400°C: $E \approx 170$ GPa (15% reduction)
- At 600°C: $E \approx 130$ GPa (35% reduction)

### A.4 Example: Triaxial Stress State in a Confined Specimen

**Given:** A concrete cube ($E = 30$ GPa, $\nu = 0.2$) is confined in a rigid steel mold (no lateral expansion possible: $\varepsilon_{yy} = \varepsilon_{zz} = 0$). A compressive stress $\sigma_{xx} = -50$ MPa is applied.

**Find:** The lateral stresses and the axial strain.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

From generalized Hooke's Law with $\varepsilon_{yy} = 0$:

$$
0 = \frac{1}{E}[\sigma_{yy} - \nu(\sigma_{xx} + \sigma_{zz})]
$$

By symmetry ($\varepsilon_{yy} = \varepsilon_{zz} = 0$): $\sigma_{yy} = \sigma_{zz}$.

$$
0 = \sigma_{yy} - \nu(\sigma_{xx} + \sigma_{yy})
$$

$$
\sigma_{yy}(1 - \nu) = \nu\sigma_{xx}
$$

$$
\sigma_{yy} = \frac{\nu}{1-\nu}\sigma_{xx} = \frac{0.2}{0.8}(-50) = -12.5 \text{ MPa}
$$

**Axial strain:**

$$
\varepsilon_{xx} = \frac{1}{E}[\sigma_{xx} - \nu(\sigma_{yy} + \sigma_{zz})] = \frac{1}{30000}[-50 - 0.2(-12.5 - 12.5)]
$$

$$
= \frac{-50 + 5}{30000} = \frac{-45}{30000} = -1.5 \times 10^{-3}
$$

The confinement reduces the axial strain compared to unconfined: $\varepsilon_{\text{unconfined}} = -50/30000 = -1.67 \times 10^{-3}$.

**Effective modulus (confined):**

$$
E_{\text{eff}} = \frac{\sigma_{xx}}{\varepsilon_{xx}} = \frac{-50}{-1.5 \times 10^{-3}} = 33.3 \text{ GPa} \gt  E
$$

</details>

---

*Next: [12.4 - Axial Loading & Torsion](12.4---Axial-Loading-&-Torsion) →*


---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — 3D Hooke's Law via Lamé Constants

**Given:** A steel element ($E = 200$ GPa, $\nu = 0.3$) is subjected to the stress state:

$$
\sigma_{xx} = 150 \text{ MPa}, \quad \sigma_{yy} = -80 \text{ MPa}, \quad \sigma_{zz} = 50 \text{ MPa}, \quad \tau_{xy} = 60 \text{ MPa}, \quad \tau_{yz} = \tau_{xz} = 0
$$

**Find:** (a) Compute the Lamé constants $\lambda$ and $\mu$. (b) Express the strain tensor using the inverse Hooke's law in Lamé form. (c) Verify by computing strain energy density two ways.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Part (a): Lamé constants.**

$$
\mu = G = \frac{E}{2(1+\nu)} = \frac{200}{2(1.3)} = 76.92 \text{ GPa}
$$

$$
\lambda = \frac{E\nu}{(1+\nu)(1-2\nu)} = \frac{200 \times 0.3}{(1.3)(0.4)} = \frac{60}{0.52} = 115.38 \text{ GPa}
$$

**Part (b): Strain from inverse relation.**

The generalized Hooke's law in Lamé form:

$$
\sigma_{ij} = \lambda(\varepsilon_{kk})\delta_{ij} + 2\mu\varepsilon_{ij}
$$

Inverting:

$$
\varepsilon_{ij} = \frac{1}{2\mu}\sigma_{ij} - \frac{\lambda}{2\mu(3\lambda + 2\mu)}\sigma_{kk}\delta_{ij}
$$

Note that $3\lambda + 2\mu = 3(115.38) + 2(76.92) = 346.14 + 153.84 = 500$ GPa $= \frac{E(1-\nu)}{(1+\nu)(1-2\nu)} \cdot 3$... Actually, let's verify: $3\lambda + 2\mu = \frac{3E\nu}{(1+\nu)(1-2\nu)} + \frac{E}{1+\nu} = \frac{E(3\nu + 1 - 2\nu)}{(1+\nu)(1-2\nu)} = \frac{E(1+\nu)}{(1+\nu)(1-2\nu)} = \frac{E}{1-2\nu} = \frac{200}{0.4} = 500$ GPa. ✓

First invariant: $\sigma_{kk} = 150 + (-80) + 50 = 120$ MPa.

Normal strains:

$$
\varepsilon_{xx} = \frac{1}{2\mu}\sigma_{xx} - \frac{\lambda}{2\mu(3\lambda+2\mu)}\sigma_{kk}
$$

$$
= \frac{150}{2(76920)} - \frac{115.38}{2(76.92)(500)} \times 120 \times \frac{10^3}{10^3}
$$

Let me use the standard form instead (cleaner):

$$
\varepsilon_{xx} = \frac{1}{E}[\sigma_{xx} - \nu(\sigma_{yy} + \sigma_{zz})] = \frac{1}{200000}[150 - 0.3(-80+50)]
$$

$$
= \frac{150 - 0.3(-30)}{200000} = \frac{150 + 9}{200000} = \frac{159}{200000} = 7.95 \times 10^{-4}
$$

$$
\varepsilon_{yy} = \frac{1}{200000}[-80 - 0.3(150+50)] = \frac{-80 - 60}{200000} = -7.0 \times 10^{-4}
$$

$$
\varepsilon_{zz} = \frac{1}{200000}[50 - 0.3(150-80)] = \frac{50 - 21}{200000} = 1.45 \times 10^{-4}
$$

$$
\gamma_{xy} = \frac{\tau_{xy}}{G} = \frac{60}{76920} = 7.80 \times 10^{-4}
$$

$$
\gamma_{yz} = \gamma_{xz} = 0
$$

Volumetric strain: $e = 7.95 - 7.0 + 1.45 = 2.40 \times 10^{-4}$

**Part (c): Strain energy density — two methods.**

Method 1 (stress-based):

$$
u = \frac{1}{2E}\left[\sigma_{xx}^2 + \sigma_{yy}^2 + \sigma_{zz}^2 - 2\nu(\sigma_{xx}\sigma_{yy} + \sigma_{yy}\sigma_{zz} + \sigma_{zz}\sigma_{xx})\right] + \frac{1}{2G}\left[\tau_{xy}^2 + \tau_{yz}^2 + \tau_{xz}^2\right]
$$

$$
= \frac{1}{2(200000)}\left[150^2 + 80^2 + 50^2 - 2(0.3)(150(-80) + (-80)(50) + 50(150))\right] + \frac{60^2}{2(76920)}
$$

$$
= \frac{1}{400000}\left[22500 + 6400 + 2500 - 0.6(-12000 - 4000 + 7500)\right] + \frac{3600}{153840}
$$

$$
= \frac{1}{400000}\left[31400 - 0.6(-8500)\right] + 0.0234
$$

$$
= \frac{31400 + 5100}{400000} + 0.0234 = 0.09125 + 0.0234 = 0.1147 \text{ MPa} = 114.7 \text{ kJ/m}^3
$$

Method 2 (dot product):

$$
u = \frac{1}{2}\sigma_{ij}\varepsilon_{ij} = \frac{1}{2}[\sigma_{xx}\varepsilon_{xx} + \sigma_{yy}\varepsilon_{yy} + \sigma_{zz}\varepsilon_{zz} + 2\tau_{xy}\varepsilon_{xy}]
$$

$$
= \frac{1}{2}[150(7.95) + (-80)(-7.0) + 50(1.45) + 2(60)(3.90)] \times 10^{-4} \text{ (MPa)}
$$

$$
= \frac{1}{2}[1192.5 + 560 + 72.5 + 468] \times 10^{-4} = \frac{2293}{2} \times 10^{-4} = 0.1147 \text{ MPa} \quad \checkmark
$$

*Reference: Timoshenko & Goodier, Theory of Elasticity, Ch. 4; MIT OCW 3.032.*

</details>

### Example 8.2 — Relating $E$, $G$, $K$, $\nu$ Pairwise

**Given:** A material has bulk modulus $K = 160$ GPa and shear modulus $G = 75$ GPa.

**Find:** $E$, $\nu$, and the Lamé constant $\lambda$. Verify all interrelations.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Young's modulus from $K$ and $G$.**

$$
E = \frac{9KG}{3K + G} = \frac{9(160)(75)}{3(160) + 75} = \frac{108000}{480 + 75} = \frac{108000}{555} = 194.6 \text{ GPa}
$$

**Step 2: Poisson's ratio from $K$ and $G$.**

$$
\nu = \frac{3K - 2G}{2(3K + G)} = \frac{3(160) - 2(75)}{2(480 + 75)} = \frac{480 - 150}{1110} = \frac{330}{1110} = 0.297
$$

**Step 3: Lamé constant.**

$$
\lambda = K - \frac{2G}{3} = 160 - \frac{150}{3} = 160 - 50 = 110 \text{ GPa}
$$

**Verification chain:**

Check $E = 2G(1+\nu)$: $2(75)(1.297) = 194.6$ GPa ✓

Check $E = 3K(1-2\nu)$: $3(160)(1 - 0.594) = 480(0.406) = 194.9$ GPa ≈ 194.6 ✓ (rounding)

Check $\lambda = \frac{E\nu}{(1+\nu)(1-2\nu)}$: $\frac{194.6 \times 0.297}{1.297 \times 0.406} = \frac{57.8}{0.527} = 109.7 \approx 110$ GPa ✓

**Physical bounds check:**
- $\nu \gt  0$ ✓ (material contracts laterally under tension)
- $\nu \lt  0.5$ ✓ (not incompressible)
- $G \gt  0$, $K \gt  0$, $E \gt  0$ ✓ (positive definiteness of stiffness)

This material is close to steel ($E \approx 200$, $\nu \approx 0.3$).

*Reference: Hibbeler, Mechanics of Materials, 10th ed., Table on inside cover.*

</details>

### Example 8.3 — Thin-Walled Pressure Vessel: Hoop, Axial, and Volumetric Strain

**Given:** A thin-walled cylindrical pressure vessel: radius $r = 500$ mm, wall thickness $t = 10$ mm, length $L = 2$ m. Material: aluminum ($E = 70$ GPa, $\nu = 0.33$). Internal gauge pressure $p = 3$ MPa.

**Find:** (a) Hoop and axial stresses. (b) All strains. (c) Change in diameter, length, and volume.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Part (a): Stresses (thin-wall formulas, $r/t = 50 \gt  10$).**

$$
\sigma_1 = \sigma_{\text{hoop}} = \frac{pr}{t} = \frac{3 \times 500}{10} = 150 \text{ MPa}
$$

$$
\sigma_2 = \sigma_{\text{axial}} = \frac{pr}{2t} = \frac{3 \times 500}{20} = 75 \text{ MPa}
$$

$$
\sigma_3 = \sigma_{\text{radial}} \approx 0 \text{ (thin wall assumption)}
$$

Note: $\sigma_{\text{hoop}} = 2\sigma_{\text{axial}}$ always for cylindrical vessels.

**Part (b): Strains (plane stress with $\sigma_3 = 0$).**

$$
\varepsilon_1 = \frac{1}{E}(\sigma_1 - \nu\sigma_2) = \frac{1}{70000}(150 - 0.33 \times 75) = \frac{150 - 24.75}{70000} = \frac{125.25}{70000} = 1.789 \times 10^{-3}
$$

$$
\varepsilon_2 = \frac{1}{E}(\sigma_2 - \nu\sigma_1) = \frac{1}{70000}(75 - 0.33 \times 150) = \frac{75 - 49.5}{70000} = \frac{25.5}{70000} = 3.643 \times 10^{-4}
$$

$$
\varepsilon_3 = \frac{-\nu}{E}(\sigma_1 + \sigma_2) = \frac{-0.33}{70000}(225) = -1.061 \times 10^{-3}
$$

**Part (c): Dimensional changes.**

Change in diameter:

$$
\Delta d = \varepsilon_1 \cdot d = 1.789 \times 10^{-3} \times 1000 = 1.789 \text{ mm}
$$

Change in length:

$$
\Delta L = \varepsilon_2 \cdot L = 3.643 \times 10^{-4} \times 2000 = 0.729 \text{ mm}
$$

Change in wall thickness:

$$
\Delta t = \varepsilon_3 \cdot t = -1.061 \times 10^{-3} \times 10 = -0.0106 \text{ mm}
$$

**Volumetric strain** (for a thin cylinder, $V = \pi r^2 L$):

$$
\frac{\Delta V}{V} = 2\varepsilon_1 + \varepsilon_2 = 2(1.789 \times 10^{-3}) + 3.643 \times 10^{-4} = 3.942 \times 10^{-3}
$$

Original volume: $V = \pi(0.5)^2(2) = 1.571$ m³

$$
\Delta V = 3.942 \times 10^{-3} \times 1.571 = 6.19 \times 10^{-3} \text{ m}^3 = 6.19 \text{ liters}
$$

*Reference: Hibbeler, Mechanics of Materials, 10th ed., §8.1–8.2; Gere, §8.3.*

</details>



---

## 📘 9. Appendix: Extended Derivations & Special Cases

### Appendix 9.1 — Derivation of $E = 2G(1+\nu)$ from a Tensile Test

**Goal:** Show that Young's modulus, shear modulus, and Poisson's ratio are not independent for an isotropic material.

**Setup:** Consider a uniaxial tensile test with $\sigma_{xx} = \sigma$, all other stress components zero.

The strain state is:

$$
\varepsilon_{xx} = \frac{\sigma}{E}, \quad \varepsilon_{yy} = \varepsilon_{zz} = -\nu\frac{\sigma}{E}
$$

Now consider the same element rotated $45°$ about the $z$-axis. The stress transformation gives:

$$
\sigma_{x'x'} = \frac{\sigma}{2}, \quad \sigma_{y'y'} = \frac{\sigma}{2}, \quad \tau_{x'y'} = \frac{\sigma}{2}
$$

Wait — let me be precise. For rotation by $\theta = 45°$:

$$
\sigma_{x'} = \frac{\sigma_{xx} + \sigma_{yy}}{2} + \frac{\sigma_{xx} - \sigma_{yy}}{2}\cos 90° + \tau_{xy}\sin 90° = \frac{\sigma}{2} + 0 + 0 = \frac{\sigma}{2}
$$

$$
\tau_{x'y'} = -\frac{\sigma_{xx} - \sigma_{yy}}{2}\sin 90° + \tau_{xy}\cos 90° = -\frac{\sigma}{2}(1) + 0 = -\frac{\sigma}{2}
$$

So in the $45°$ frame: $\sigma_{x'} = \sigma/2$, $\sigma_{y'} = \sigma/2$, $\tau_{x'y'} = -\sigma/2$.

The shear strain in the rotated frame (from the definition of $G$):

$$
\gamma_{x'y'} = \frac{\tau_{x'y'}}{G} = \frac{-\sigma/2}{G} = \frac{-\sigma}{2G}
$$

**Alternatively**, compute $\gamma_{x'y'}$ from the strain transformation. The original strains are $\varepsilon_{xx} = \sigma/E$, $\varepsilon_{yy} = -\nu\sigma/E$, $\gamma_{xy} = 0$.

The shear strain transformation at $\theta = 45°$:

$$
\frac{\gamma_{x'y'}}{2} = -\frac{\varepsilon_{xx} - \varepsilon_{yy}}{2}\sin 90° + \frac{\gamma_{xy}}{2}\cos 90°
$$

$$
= -\frac{(\sigma/E) - (-\nu\sigma/E)}{2}(1) + 0 = -\frac{\sigma(1+\nu)}{2E}
$$

$$
\gamma_{x'y'} = -\frac{\sigma(1+\nu)}{E}
$$

**Equating the two expressions for $\gamma_{x'y'}$:**

$$
\frac{-\sigma}{2G} = -\frac{\sigma(1+\nu)}{E}
$$

$$
\frac{1}{2G} = \frac{1+\nu}{E}
$$

$$
\boxed{E = 2G(1+\nu)}
$$

$\blacksquare$

**Corollary:** Since $-1 < \nu < 0.5$ for stable materials, we have $E < 3G$ (when $\nu \to 0.5$, $G \to E/3$) and $E > 2G$ (when $\nu \to 0$, $G \to E/2$).

*Reference: Timoshenko & Goodier, Theory of Elasticity, §7; Gere, Mechanics of Materials, Appendix.*

### Appendix 9.2 — Strain Energy Density: Volumetric and Distortional Components

The total strain energy density for a linear elastic isotropic material:

$$
u = \frac{1}{2}\sigma_{ij}\varepsilon_{ij} = \frac{1}{2E}\left[\sigma_{xx}^2 + \sigma_{yy}^2 + \sigma_{zz}^2 - 2\nu(\sigma_{xx}\sigma_{yy} + \sigma_{yy}\sigma_{zz} + \sigma_{zz}\sigma_{xx}) + 2(1+\nu)(\tau_{xy}^2 + \tau_{yz}^2 + \tau_{xz}^2)\right]
$$

This can be decomposed into **volumetric** (dilatational) and **distortional** (deviatoric) parts:

$$
u = u_{\text{vol}} + u_{\text{dist}}
$$

**Volumetric component** (energy stored in volume change):

$$
u_{\text{vol}} = \frac{\sigma_m^2}{2K} = \frac{(\sigma_{xx}+\sigma_{yy}+\sigma_{zz})^2}{18K} = \frac{(1-2\nu)}{6E}(\sigma_{xx}+\sigma_{yy}+\sigma_{zz})^2
$$

**Distortional component** (energy stored in shape change):

$$
u_{\text{dist}} = u - u_{\text{vol}} = \frac{1+\nu}{6E}\left[(\sigma_{xx}-\sigma_{yy})^2 + (\sigma_{yy}-\sigma_{zz})^2 + (\sigma_{zz}-\sigma_{xx})^2 + 6(\tau_{xy}^2+\tau_{yz}^2+\tau_{xz}^2)\right]
$$

$$
= \frac{J_2}{2G} = \frac{\sigma_{\text{VM}}^2}{6G}
$$

**Key insight:** The von Mises yield criterion ($\sigma_{\text{VM}} = \sigma_Y$) is equivalent to stating that yielding occurs when the **distortional strain energy density** reaches a critical value:

$$
u_{\text{dist,yield}} = \frac{\sigma_Y^2}{6G}
$$

This is the **maximum distortion energy theory** (Huber-Hencky-von Mises).

*Reference: Chakrabarty, Theory of Plasticity, §1.3; Dowling, Mechanical Behavior of Materials, §7.3.*

### Appendix 9.3 — Bulk Modulus and the Incompressibility Limit

The bulk modulus relates hydrostatic stress to volumetric strain:

$$
K = \frac{\sigma_m}{e} = \frac{E}{3(1-2\nu)}
$$

**Physical bounds on $\nu$:**

- As $\nu \to 0.5$: $K \to \infty$ (material becomes incompressible — no volume change under any stress). Rubber ($\nu \approx 0.49$) is nearly incompressible.
- At $\nu = 0$: $K = E/3$ and $G = E/2$. Cork has $\nu \approx 0$ (no lateral expansion).
- If $\nu < 0$ (auxetic materials): the material expands laterally under tension. Some foams and metamaterials exhibit this.
- If $\nu > 0.5$: $K < 0$, meaning the material expands under hydrostatic compression — thermodynamically unstable.

**For incompressible materials** ($\nu = 0.5$ exactly):
- $K = \infty$, $\lambda = \infty$
- $E = 3G$ (only one independent constant)
- $\varepsilon_{kk} = 0$ always (isochoric deformation)
- The constitutive law becomes: $\sigma_{ij} = -p\delta_{ij} + 2G\varepsilon_{ij}$ where $p$ is a Lagrange multiplier (hydrostatic pressure determined by boundary conditions, not by strain)

This is the starting point for rubber elasticity and fluid mechanics (Newtonian fluid: $\sigma_{ij} = -p\delta_{ij} + 2\mu D_{ij}$).

*Reference: Malvern, Introduction to the Mechanics of a Continuous Medium, §6.2; MIT OCW 3.032.*
