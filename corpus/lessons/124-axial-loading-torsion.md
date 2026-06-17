---
title: "12.4 — Axial Loading & Torsion"
subject: "Solid Mechanics & Materials Science"
catalog: advanced
audience_tier: higher-education
chapter: "12.4"
type: chapter-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 12.4 — Axial Loading & Torsion

> *"The resistance which a solid offers to a change of form depends not only on the nature of the material but also on the shape and dimensions of the body."*
> — **Stephen Timoshenko** (1878–1972), *Strength of Materials*

This chapter applies the stress-strain framework to two fundamental loading modes: **axial** (tension/compression along the member axis) and **torsion** (twisting about the longitudinal axis). Both produce uniform or linearly varying stress distributions that can be solved in closed form.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Compute axial deformation $\delta = PL/(AE)$ for prismatic and non-prismatic members.
2. Solve statically indeterminate axial problems using compatibility equations.
3. Analyze thermal deformation and thermal stresses in constrained members.
4. Derive the **torsion formula** $\tau = T\rho/J$ for circular shafts.
5. Compute the **angle of twist** $\phi = TL/(GJ)$.
6. Solve power transmission problems ($P = T\omega$).
7. Handle composite and stepped shafts under torsion.

---

## 🖼️ Visual Anchor — Torsion of a Circular Shaft

![math-12__12.4-fig1](math-12__12.4-fig1.svg)

---

## 📚 1. Definitions

### Definition 12.4.1 — Axial Deformation

For a prismatic member of length $L$, cross-sectional area $A$, and Young's modulus $E$, subjected to constant axial force $P$:

$$
\delta = \frac{PL}{AE}
$$

For a member with varying force $P(x)$, area $A(x)$, or modulus $E(x)$:

$$
\delta = \int_0^L \frac{P(x)}{A(x)E(x)}\,dx
$$

### Definition 12.4.2 — Thermal Deformation

A free member subjected to temperature change $\Delta T$ undergoes thermal strain:

$$
\varepsilon_T = \alpha \Delta T
$$

$$
\delta_T = \alpha \Delta T \cdot L
$$

where $\alpha$ is the **coefficient of thermal expansion** (1/°C or 1/°F).

### Definition 12.4.3 — Polar Moment of Inertia

The **polar moment of inertia** $J$ of a cross-section about its centroidal axis:

$$
J = \int_A \rho^2\,dA
$$

For a **solid circular** cross-section of radius $c$:

$$
J = \frac{\pi c^4}{2} = \frac{\pi d^4}{32}
$$

For a **hollow circular** cross-section (outer radius $c_o$, inner radius $c_i$):

$$
J = \frac{\pi}{2}(c_o^4 - c_i^4)
$$

### Definition 12.4.4 — Shear Stress in Torsion

For a circular shaft under torque $T$, the shear stress at radial distance $\rho$ from the center:

$$
\tau = \frac{T\rho}{J}
$$

Maximum shear stress occurs at the outer surface ($\rho = c$):

$$
\tau_{\max} = \frac{Tc}{J}
$$

### Definition 12.4.5 — Angle of Twist

The total angle of twist for a shaft of length $L$ under constant torque $T$:

$$
\phi = \frac{TL}{GJ}
$$

For varying torque $T(x)$:

$$
\phi = \int_0^L \frac{T(x)}{G(x)J(x)}\,dx
$$

### Definition 12.4.6 — Power Transmission

The relationship between transmitted power $P$, torque $T$, and angular velocity $\omega$:

$$
P = T\omega = T \cdot 2\pi f
$$

where $f$ is the frequency of rotation (rev/s) and $\omega$ is in rad/s.

---

## 📐 2. Axioms / Postulates

### Postulate 12.4.P1 — Plane Sections Remain Plane (Axial)

Cross-sections that are plane and perpendicular to the axis before loading remain plane and perpendicular after loading (for axial loads applied at the centroid).

### Postulate 12.4.P2 — Plane Sections Remain Plane (Torsion)

For circular shafts under torsion, cross-sections remain plane and rotate as rigid disks. Radial lines remain straight. This is **exact** for circular sections and approximate for non-circular sections.

### Postulate 12.4.P3 — Saint-Venant's Principle

The stress distribution at points sufficiently far from the point of load application is independent of the exact manner of loading — only the resultant force and moment matter. "Sufficiently far" ≈ one characteristic dimension of the cross-section.

### Postulate 12.4.P4 — Homogeneous Material

The material properties ($E$, $G$) are uniform throughout the member. For composite members, each segment is treated separately with its own properties.

### Postulate 12.4.P5 — No Buckling (Axial Compression)

For compression members, the axial load must remain below the critical buckling load (Euler's formula):

$$
P_{\text{cr}} = \frac{\pi^2 EI}{(KL)^2}
$$

where $K$ is the effective length factor. This chapter assumes all compression members are short enough to avoid buckling.

---

## 🛡️ 3. Lemmas

### Lemma 12.4.1 — Compatibility for Statically Indeterminate Axial Members

When a member is constrained at both ends (or has more supports than needed for equilibrium), the problem is statically indeterminate. The additional equation comes from **geometric compatibility** — the total deformation must be consistent with the constraints.

**Example:** A bar fixed at both ends with temperature change:

$$
\delta_{\text{total}} = \delta_{\text{thermal}} + \delta_{\text{force}} = 0
$$

$$
\alpha \Delta T \cdot L + \frac{FL}{AE} = 0 \implies F = -\alpha \Delta T \cdot AE
$$

### Lemma 12.4.2 — Shear Strain in Torsion (Geometric Derivation)

<details>
<summary>🔍 Derivation</summary>

Consider a shaft element of length $dx$. Under torque $T$, the free end rotates by $d\phi$ relative to the fixed end.

A line on the surface (originally parallel to the axis) now makes angle $\gamma$ with the axis:

$$
\gamma = \frac{\rho\,d\phi}{dx}
$$

At the outer surface ($\rho = c$):

$$
\gamma_{\max} = \frac{c\,d\phi}{dx}
$$

From Hooke's Law in shear: $\tau = G\gamma$:

$$
\tau = G\rho\frac{d\phi}{dx}
$$

This shows shear stress varies **linearly** with radius (zero at center, maximum at surface). $\blacksquare$

</details>

### Lemma 12.4.3 — Derivation of the Torsion Formula

<details>
<summary>🔍 Full Derivation</summary>

**Step 1:** The resultant torque from the shear stress distribution must equal the applied torque $T$:

$$
T = \int_A \tau \cdot \rho\,dA = \int_A G\frac{d\phi}{dx}\rho^2\,dA = G\frac{d\phi}{dx}\int_A \rho^2\,dA
$$

$$
T = GJ\frac{d\phi}{dx}
$$

**Step 2:** Solve for $d\phi/dx$:

$$
\frac{d\phi}{dx} = \frac{T}{GJ}
$$

**Step 3:** Substitute back into the shear stress expression:

$$
\tau = G\rho\frac{d\phi}{dx} = G\rho\frac{T}{GJ} = \frac{T\rho}{J}
$$

**Step 4:** For constant $T$, $G$, $J$ along the length, integrate:

$$
\phi = \int_0^L \frac{d\phi}{dx}\,dx = \frac{TL}{GJ}
$$

$\blacksquare$

</details>

---

## 👑 4. Theorems

### Theorem 12.4.1 — Axial Deformation Formula

For a prismatic bar under constant axial load $P$:

$$
\delta = \frac{PL}{AE}
$$

This is the direct consequence of combining $\sigma = P/A$, $\varepsilon = \sigma/E$, and $\delta = \varepsilon L$.

### Theorem 12.4.2 — Torsion Formula for Circular Shafts

$$
\tau = \frac{T\rho}{J}, \quad \tau_{\max} = \frac{Tc}{J}, \quad \phi = \frac{TL}{GJ}
$$

### Theorem 12.4.3 — Superposition for Multi-Segment Shafts

For a shaft with $n$ segments of different properties or torques:

$$
\phi_{\text{total}} = \sum_{i=1}^n \frac{T_i L_i}{G_i J_i}
$$

### Theorem 12.4.4 — Elastic Strain Energy in Axial Loading

$$
U = \frac{P^2 L}{2AE} = \frac{1}{2}P\delta = \frac{AE\delta^2}{2L}
$$

For variable loading:

$$
U = \int_0^L \frac{[N(x)]^2}{2A(x)E(x)}\,dx
$$

### Theorem 12.4.5 — Elastic Strain Energy in Torsion

$$
U = \frac{T^2 L}{2GJ} = \frac{1}{2}T\phi = \frac{GJ\phi^2}{2L}
$$

For variable torque:

$$
U = \int_0^L \frac{[T(x)]^2}{2G(x)J(x)}\,dx
$$

### Theorem 12.4.6 — Castigliano's Theorem (Preview)

The displacement at the point of application of a force $P$ in the direction of $P$:

$$
\delta = \frac{\partial U}{\partial P}
$$

Similarly for rotation due to torque: $\phi = \frac{\partial U}{\partial T}$.

This powerful energy method will be extended in later courses to solve indeterminate structures.

---

## ✍️ 5. Proofs / Derivations

### 5.1 Derivation: Axial Deformation from First Principles

<details>
<summary>🔍 Full Derivation</summary>

Consider an infinitesimal element of length $dx$ at position $x$ along a bar.

**Internal force:** $N(x)$ (from equilibrium of a free-body cut).

**Stress:** $\sigma(x) = N(x)/A(x)$

**Strain:** $\varepsilon(x) = \sigma(x)/E(x) = N(x)/[A(x)E(x)]$

**Deformation of element:** $d\delta = \varepsilon(x)\,dx = \frac{N(x)}{A(x)E(x)}\,dx$

**Total deformation:**

$$
\delta = \int_0^L \frac{N(x)}{A(x)E(x)}\,dx
$$

For constant $N = P$, $A$, $E$:

$$
\delta = \frac{P}{AE}\int_0^L dx = \frac{PL}{AE}
$$

$\blacksquare$

</details>

### 5.2 Derivation: Thermal Stress in a Constrained Bar

<details>
<summary>🔍 Full Derivation</summary>

A bar of length $L$, area $A$, modulus $E$, and thermal expansion coefficient $\alpha$ is fixed at both ends. Temperature increases by $\Delta T$.

**Compatibility:** Total deformation = 0 (both ends fixed):

$$
\delta_{\text{thermal}} + \delta_{\text{mechanical}} = 0
$$

$$
\alpha \Delta T \cdot L + \frac{FL}{AE} = 0
$$

Solving for the reaction force $F$:

$$
F = -\alpha \Delta T \cdot AE
$$

The negative sign indicates **compression** (the bar wants to expand but is prevented).

**Thermal stress:**

$$
\sigma = \frac{F}{A} = -\alpha \Delta T \cdot E
$$

Note: This is independent of length $L$ and area $A$! $\blacksquare$

</details>

### 5.3 Derivation: Statically Indeterminate Axial Bar (Two Materials)

<details>
<summary>🔍 Full Derivation</summary>

Consider a rigid plate supported by two bars: Bar 1 (steel, $A_1$, $E_1$, $L_1$) and Bar 2 (aluminum, $A_2$, $E_2$, $L_2$). A load $P$ is applied to the rigid plate.

**Equilibrium:**

$$
F_1 + F_2 = P
$$

**Compatibility** (both bars deform equally since plate is rigid):

$$
\delta_1 = \delta_2 \implies \frac{F_1 L_1}{A_1 E_1} = \frac{F_2 L_2}{A_2 E_2}
$$

**Solving:**

$$
F_1 = F_2 \cdot \frac{A_1 E_1 L_2}{A_2 E_2 L_1}
$$

Let $k = \frac{A_1 E_1 L_2}{A_2 E_2 L_1}$ (stiffness ratio):

$$
F_2(k + 1) = P \implies F_2 = \frac{P}{1+k}, \quad F_1 = \frac{kP}{1+k}
$$

The stiffer bar carries more load. $\blacksquare$

</details>

### 5.4 Derivation: Torsion of a Thin-Walled Tube (Bredt's Formula)

<details>
<summary>🔍 Full Derivation</summary>

For a thin-walled closed section of arbitrary shape, consider a small element of the wall with thickness $t$ and arc length $ds$.

**Shear flow** $q = \tau \cdot t$ is constant around the cross-section (from equilibrium of a longitudinal element):

$$
q = \tau t = \text{constant}
$$

**Moment equivalence:** The torque equals the moment of the shear flow about any point:

$$
T = \oint q \cdot r_\perp\,ds = q \oint r_\perp\,ds = q \cdot 2A_m
$$

where $A_m$ is the area enclosed by the median line (since $\oint r_\perp\,ds = 2A_m$ by the geometric interpretation of the integral as twice the enclosed area).

Therefore:

$$
q = \frac{T}{2A_m}, \quad \tau = \frac{T}{2A_m t}
$$

**Angle of twist** (from strain energy equivalence):

$$
\phi = \frac{TL}{4A_m^2 G}\oint \frac{ds}{t}
$$

For uniform thickness: $\phi = \frac{TLs}{4A_m^2 Gt}$ where $s$ is the perimeter. $\blacksquare$

</details>

---

## 🧮 6. Worked Examples

### Example 12.4.1 — Stepped Bar Under Axial Load

**Given:** A bar consists of two segments:
- Segment 1: $L_1 = 0.5$ m, $A_1 = 800$ mm², $E_1 = 200$ GPa (steel)
- Segment 2: $L_2 = 0.8$ m, $A_2 = 1200$ mm², $E_2 = 70$ GPa (aluminum)

An axial tensile force $P = 40$ kN is applied at the junction.

**Find:** Total elongation.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

Both segments carry the same force $P = 40$ kN.

$$
\delta_1 = \frac{PL_1}{A_1 E_1} = \frac{40 \times 10^3 \times 0.5}{800 \times 10^{-6} \times 200 \times 10^9} = \frac{20000}{160000} = 0.125 \text{ mm}
$$

$$
\delta_2 = \frac{PL_2}{A_2 E_2} = \frac{40 \times 10^3 \times 0.8}{1200 \times 10^{-6} \times 70 \times 10^9} = \frac{32000}{84000} = 0.381 \text{ mm}
$$

$$
\delta_{\text{total}} = \delta_1 + \delta_2 = 0.125 + 0.381 = 0.506 \text{ mm}
$$

</details>

---

### Example 12.4.2 — Angle of Twist for a Hollow Shaft

**Given:** A hollow steel shaft ($G = 80$ GPa) with outer diameter $d_o = 100$ mm and inner diameter $d_i = 60$ mm, length $L = 1.5$ m, transmits a torque $T = 8$ kN·m.

**Find:** Maximum shear stress and angle of twist.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Polar moment of inertia.**

$$
J = \frac{\pi}{32}(d_o^4 - d_i^4) = \frac{\pi}{32}(0.1^4 - 0.06^4)
$$

$$
= \frac{\pi}{32}(10^{-4} \times (10000 - 1296) \times 10^{-4})
$$

Let me compute in mm: $J = \frac{\pi}{32}(100^4 - 60^4) = \frac{\pi}{32}(10^8 - 1.296 \times 10^7) = \frac{\pi}{32}(8.704 \times 10^7)$

$$
J = \frac{\pi \times 8.704 \times 10^7}{32} = 8.545 \times 10^6 \text{ mm}^4 = 8.545 \times 10^{-6} \text{ m}^4
$$

**Step 2: Maximum shear stress.**

$$
\tau_{\max} = \frac{Tc}{J} = \frac{8000 \times 0.05}{8.545 \times 10^{-6}} = \frac{400}{8.545 \times 10^{-6}} = 46.8 \times 10^6 \text{ Pa} = 46.8 \text{ MPa}
$$

**Step 3: Angle of twist.**

$$
\phi = \frac{TL}{GJ} = \frac{8000 \times 1.5}{80 \times 10^9 \times 8.545 \times 10^{-6}} = \frac{12000}{683600} = 0.01755 \text{ rad}
$$

$$
\phi = 0.01755 \times \frac{180°}{\pi} = 1.006°
$$

</details>

---

### Example 12.4.3 — Power Transmission Design

**Given:** A solid steel shaft ($G = 80$ GPa, allowable $\tau_{\text{allow}} = 60$ MPa) must transmit 150 kW at 600 rpm.

**Find:** Minimum required shaft diameter.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Convert power to torque.**

$$
\omega = 600 \times \frac{2\pi}{60} = 62.83 \text{ rad/s}
$$

$$
T = \frac{P}{\omega} = \frac{150 \times 10^3}{62.83} = 2387 \text{ N·m}
$$

**Step 2: Apply torsion formula.**

For a solid shaft: $J = \pi c^4/2$ and $\tau_{\max} = Tc/J = 2T/(\pi c^3)$.

$$
\tau_{\text{allow}} = \frac{2T}{\pi c^3}
$$

$$
c^3 = \frac{2T}{\pi \tau_{\text{allow}}} = \frac{2 \times 2387}{\pi \times 60 \times 10^6} = \frac{4774}{188.5 \times 10^6} = 25.32 \times 10^{-6} \text{ m}^3
$$

$$
c = (25.32 \times 10^{-6})^{1/3} = 0.02937 \text{ m} = 29.37 \text{ mm}
$$

**Minimum diameter:**

$$
d = 2c = 58.7 \text{ mm}
$$

Round up to standard size: $d = 60$ mm.

</details>

---

### Example 12.4.4 — Statically Indeterminate Shaft

**Given:** A shaft is fixed at both ends $A$ and $B$ (length $L$). A torque $T_0$ is applied at distance $a$ from $A$ (and $b = L - a$ from $B$). The shaft has uniform $G$ and $J$.

**Find:** Reactions $T_A$ and $T_B$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Equilibrium (1 equation, 2 unknowns → indeterminate).**

$$
\sum T = 0: \quad T_A + T_B = T_0
$$

**Step 2: Compatibility — total angle of twist = 0 (both ends fixed).**

$$
\phi_{A \to C} + \phi_{C \to B} = 0
$$

Segment $AC$ (length $a$, torque $T_A$):

$$
\phi_{AC} = \frac{T_A \cdot a}{GJ}
$$

Segment $CB$ (length $b$, torque $T_A - T_0 = -T_B$):

$$
\phi_{CB} = \frac{-T_B \cdot b}{GJ}
$$

Setting $\phi_{AC} + \phi_{CB} = 0$:

$$
\frac{T_A a}{GJ} - \frac{T_B b}{GJ} = 0 \implies T_A a = T_B b
$$

**Step 3: Solve simultaneously.**

From equilibrium: $T_B = T_0 - T_A$.

$$
T_A a = (T_0 - T_A)b = T_0 b - T_A b
$$

$$
T_A(a + b) = T_0 b \implies T_A = \frac{T_0 b}{L}
$$

$$
T_B = \frac{T_0 a}{L}
$$

The reactions are inversely proportional to the distances — the closer support takes more torque.

</details>

---

### Example 12.4.5 — Strain Energy Method for Axial Deformation

**Given:** A tapered rod has diameter varying linearly from $d_1 = 40$ mm at $x = 0$ to $d_2 = 20$ mm at $x = L = 1$ m. Material: steel ($E = 200$ GPa). Axial load $P = 30$ kN.

**Find:** Total elongation using the integral formula.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Express diameter as function of $x$.**

$$
d(x) = d_1 + (d_2 - d_1)\frac{x}{L} = 40 - 20\frac{x}{1} = (40 - 20x) \text{ mm}
$$

$$
r(x) = \frac{d(x)}{2} = (20 - 10x) \text{ mm} = (0.02 - 0.01x) \text{ m}
$$

$$
A(x) = \pi r(x)^2 = \pi(0.02 - 0.01x)^2
$$

**Step 2: Integrate.**

$$
\delta = \int_0^1 \frac{P}{A(x)E}\,dx = \frac{P}{\pi E}\int_0^1 \frac{dx}{(0.02 - 0.01x)^2}
$$

Let $u = 0.02 - 0.01x$, $du = -0.01\,dx$:

When $x = 0$: $u = 0.02$. When $x = 1$: $u = 0.01$.

$$
\delta = \frac{P}{\pi E} \cdot \frac{1}{-0.01}\int_{0.02}^{0.01} \frac{du}{u^2} = \frac{P}{\pi E} \cdot \frac{1}{0.01}\int_{0.01}^{0.02} \frac{du}{u^2}
$$

$$
= \frac{P}{0.01\pi E}\left[-\frac{1}{u}\right]_{0.01}^{0.02} = \frac{P}{0.01\pi E}\left(-\frac{1}{0.02} + \frac{1}{0.01}\right)
$$

$$
= \frac{P}{0.01\pi E}(100 - 50) = \frac{50P}{0.01\pi E} = \frac{5000P}{\pi E}
$$

$$
= \frac{5000 \times 30000}{\pi \times 200 \times 10^9} = \frac{1.5 \times 10^8}{6.283 \times 10^{11}} = 2.39 \times 10^{-4} \text{ m} = 0.239 \text{ mm}
$$

**Verification using the conical bar formula:** $\delta = \frac{PL}{\pi E r_1 r_2} = \frac{30000 \times 1}{\pi \times 200\times10^9 \times 0.02 \times 0.01} = \frac{30000}{1.257\times10^8} = 0.239$ mm ✓

</details>

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- **Previous:** [12.3 - Hooke's Law & Material Properties](12.3---Hooke's-Law-&-Material-Properties) — Constitutive law used here
- **Next:** [12.5 - Bending of Beams & Shear Stress](12.5---Bending-of-Beams-&-Shear-Stress) — Bending as the next loading mode
- **Statics prerequisite:** [12.1 - Statics & Equilibrium](12.1---Statics-&-Equilibrium) — Internal force diagrams
- **Stress tensors:** [12.2 - Stress & Strain Tensors](12.2---Stress-&-Strain-Tensors) — Stress state in torsion is pure shear

### External Resources
- 📖 **Hibbeler, R.C.** *Mechanics of Materials*, 10th ed. — Chapters 4 (Axial Load) & 5 (Torsion).
- 🎬 **StructureFree** — [Axial Deformation](https://www.youtube.com/playlist?list=PL44E9FA04BCEE07C6) & [Torsion](https://www.youtube.com/playlist?list=PL44E9FA04BCEE07C6)
- 🎬 **Jeff Hanson** — [Mechanics of Materials: Torsion](https://www.youtube.com/watch?v=1YTKedLQOa0)

---

## 📎 Appendix: Additional Derivations

### A.1 Non-Uniform Axial Loading (Tapered Bar)

Consider a conical bar with radius varying linearly from $r_1$ at $x = 0$ to $r_2$ at $x = L$:

$$
r(x) = r_1 + (r_2 - r_1)\frac{x}{L}
$$

$$
A(x) = \pi r(x)^2 = \pi\left[r_1 + (r_2 - r_1)\frac{x}{L}\right]^2
$$

The deformation under constant axial load $P$:

$$
\delta = \int_0^L \frac{P}{A(x)E}\,dx = \frac{P}{\pi E}\int_0^L \frac{dx}{\left[r_1 + (r_2-r_1)\frac{x}{L}\right]^2}
$$

Let $u = r_1 + (r_2-r_1)x/L$, then $du = (r_2-r_1)/L\,dx$:

$$
\delta = \frac{P}{\pi E} \cdot \frac{L}{r_2-r_1}\int_{r_1}^{r_2} \frac{du}{u^2} = \frac{PL}{\pi E(r_2-r_1)}\left[-\frac{1}{u}\right]_{r_1}^{r_2}
$$

$$
= \frac{PL}{\pi E(r_2-r_1)}\left(\frac{1}{r_1} - \frac{1}{r_2}\right) = \frac{PL}{\pi E(r_2-r_1)} \cdot \frac{r_2-r_1}{r_1 r_2} = \frac{PL}{\pi E r_1 r_2}
$$

**Result:** $\delta = \frac{PL}{\pi E r_1 r_2}$ for a conical bar.

### A.2 Stress Concentrations in Axial Members

At geometric discontinuities (holes, notches, fillets), the actual maximum stress exceeds the nominal stress by a **stress concentration factor** $K_t$:

$$
\sigma_{\max} = K_t \cdot \sigma_{\text{nom}} = K_t \cdot \frac{P}{A_{\text{net}}}
$$

Typical values:
- Circular hole in flat bar: $K_t \approx 3.0$ (for small hole relative to width)
- Semicircular notch: $K_t \approx 3.0$
- Shoulder fillet ($r/d = 0.1$): $K_t \approx 1.8$

### A.3 Torsion of Non-Circular Sections

The torsion formula $\tau = T\rho/J$ is **exact only for circular sections**. For non-circular sections:

**Rectangular section** ($a \times b$, $a > b$):

$$
\tau_{\max} = \frac{T}{\alpha a b^2}, \quad \phi = \frac{TL}{\beta a b^3 G}
$$

| $a/b$ | $\alpha$ | $\beta$ |
|:---|:---|:---|
| 1.0 | 0.208 | 0.141 |
| 1.5 | 0.231 | 0.196 |
| 2.0 | 0.246 | 0.229 |
| 3.0 | 0.267 | 0.263 |
| ∞ | 0.333 | 0.333 |

**Thin-walled closed section** (Bredt's formula):

$$
\tau = \frac{T}{2A_m t}, \quad \phi = \frac{TL}{4A_m^2 G}\oint \frac{ds}{t}
$$

where $A_m$ is the area enclosed by the median line and $t$ is the wall thickness.

### A.4 Example: Composite Shaft (Two Materials)

**Given:** A composite shaft consists of a solid aluminum core ($d_{\text{Al}} = 40$ mm, $G_{\text{Al}} = 27$ GPa) surrounded by a steel tube ($d_i = 40$ mm, $d_o = 60$ mm, $G_{\text{St}} = 80$ GPa). Both are bonded together. Total torque $T = 3$ kN·m.

**Find:** Torque carried by each material and maximum shear stress in each.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Compatibility:** Both materials twist by the same angle:

$$
\phi_{\text{Al}} = \phi_{\text{St}} \implies \frac{T_{\text{Al}}}{G_{\text{Al}}J_{\text{Al}}} = \frac{T_{\text{St}}}{G_{\text{St}}J_{\text{St}}}
$$

**Polar moments:**

$$
J_{\text{Al}} = \frac{\pi(0.02)^4}{2} = 2.513 \times 10^{-7} \text{ m}^4
$$

$$
J_{\text{St}} = \frac{\pi}{2}(0.03^4 - 0.02^4) = \frac{\pi}{2}(8.1 \times 10^{-7} - 1.6 \times 10^{-7}) = 1.021 \times 10^{-6} \text{ m}^4
$$

**Stiffness ratio:**

$$
\frac{T_{\text{Al}}}{T_{\text{St}}} = \frac{G_{\text{Al}}J_{\text{Al}}}{G_{\text{St}}J_{\text{St}}} = \frac{27 \times 10^9 \times 2.513 \times 10^{-7}}{80 \times 10^9 \times 1.021 \times 10^{-6}} = \frac{6.785}{81.68} = 0.0831
$$

**Equilibrium:** $T_{\text{Al}} + T_{\text{St}} = 3000$ N·m

$$
0.0831\,T_{\text{St}} + T_{\text{St}} = 3000 \implies T_{\text{St}} = \frac{3000}{1.0831} = 2770 \text{ N·m}
$$

$$
T_{\text{Al}} = 3000 - 2770 = 230 \text{ N·m}
$$

**Maximum shear stresses:**

$$
\tau_{\text{Al}} = \frac{T_{\text{Al}} \cdot c_{\text{Al}}}{J_{\text{Al}}} = \frac{230 \times 0.02}{2.513 \times 10^{-7}} = 18.3 \text{ MPa}
$$

$$
\tau_{\text{St}} = \frac{T_{\text{St}} \cdot c_{\text{St}}}{J_{\text{St}}} = \frac{2770 \times 0.03}{1.021 \times 10^{-6}} = 81.4 \text{ MPa}
$$

The steel carries most of the torque due to its much higher stiffness ($GJ$).

</details>

---

*Next: [12.5 - Bending of Beams & Shear Stress](12.5---Bending-of-Beams-&-Shear-Stress) →*



---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — Stepped Composite Shaft Under Torque (Compatibility)

**Given:** A shaft consists of two segments rigidly connected: Segment 1 (steel, $G_s = 80$ GPa, solid, $d_1 = 60$ mm, $L_1 = 0.8$ m) and Segment 2 (aluminum, $G_a = 27$ GPa, hollow, $d_o = 80$ mm, $d_i = 40$ mm, $L_2 = 1.2$ m). The shaft is fixed at both ends. An external torque $T_0 = 5$ kN·m is applied at the junction.

**Find:** (a) Reactive torques at each wall. (b) Maximum shear stress in each segment. (c) Angle of twist at the junction.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Polar moments of inertia.**

$$
J_1 = \frac{\pi d_1^4}{32} = \frac{\pi(0.06)^4}{32} = \frac{\pi \times 1.296 \times 10^{-5}}{32} = 1.272 \times 10^{-6} \text{ m}^4
$$

$$
J_2 = \frac{\pi}{32}(d_o^4 - d_i^4) = \frac{\pi}{32}(0.08^4 - 0.04^4) = \frac{\pi}{32}(4.096 \times 10^{-6} - 2.56 \times 10^{-7})
$$

$$
= \frac{\pi}{32}(3.84 \times 10^{-6}) = 3.77 \times 10^{-7} \text{ m}^4
$$

Wait — let me recompute: $0.08^4 = 4.096 \times 10^{-5}$? No: $0.08^4 = (8 \times 10^{-2})^4 = 4096 \times 10^{-8} = 4.096 \times 10^{-5}$. And $0.04^4 = 256 \times 10^{-8} = 2.56 \times 10^{-6}$.

$$
J_2 = \frac{\pi}{32}(4.096 \times 10^{-5} - 2.56 \times 10^{-6}) = \frac{\pi}{32}(3.84 \times 10^{-5}) = 3.77 \times 10^{-6} \text{ m}^4
$$

**Step 2: Equilibrium.**

$$
T_A + T_B = T_0 = 5000 \text{ N·m} \tag{1}
$$

(One equation, two unknowns → statically indeterminate, degree 1.)

**Step 3: Compatibility — angle of twist at junction must be consistent.**

Since both ends are fixed, the total twist from $A$ to $B$ is zero. Segment 1 carries torque $T_A$ and segment 2 carries torque $T_B$ (with appropriate signs):

$$
\phi_1 + \phi_2 = 0
$$

$$
\frac{T_A L_1}{G_s J_1} - \frac{T_B L_2}{G_a J_2} = 0
$$

(Sign: if $T_A$ twists segment 1 clockwise, $T_B$ must twist segment 2 counterclockwise for zero net twist.)

Actually, with both ends fixed and torque at junction: segment 1 carries $T_A$ and segment 2 carries $T_B = T_0 - T_A$, both twisting the junction in the same direction. The compatibility is:

$$
\phi_{\text{junction}} = \frac{T_A L_1}{G_s J_1} = \frac{T_B L_2}{G_a J_2}
$$

(Both segments twist the junction by the same angle.)

$$
\frac{T_A \times 0.8}{80 \times 10^9 \times 1.272 \times 10^{-6}} = \frac{T_B \times 1.2}{27 \times 10^9 \times 3.77 \times 10^{-6}}
$$

$$
\frac{0.8\,T_A}{101{,}760} = \frac{1.2\,T_B}{101{,}790}
$$

$$
\frac{T_A}{127{,}200} = \frac{T_B}{84{,}825}
$$

$$
T_A = \frac{127{,}200}{84{,}825}\,T_B = 1.500\,T_B
$$

From (1): $1.5T_B + T_B = 5000 \implies T_B = 2000$ N·m, $T_A = 3000$ N·m.

**Step 4: Maximum shear stresses.**

$$
\tau_{1,\max} = \frac{T_A c_1}{J_1} = \frac{3000 \times 0.03}{1.272 \times 10^{-6}} = \frac{90}{1.272 \times 10^{-6}} = 70.8 \text{ MPa}
$$

$$
\tau_{2,\max} = \frac{T_B c_2}{J_2} = \frac{2000 \times 0.04}{3.77 \times 10^{-6}} = \frac{80}{3.77 \times 10^{-6}} = 21.2 \text{ MPa}
$$

**Step 5: Angle of twist at junction.**

$$
\phi = \frac{T_A L_1}{G_s J_1} = \frac{3000 \times 0.8}{80 \times 10^9 \times 1.272 \times 10^{-6}} = \frac{2400}{101{,}760} = 0.0236 \text{ rad} = 1.35°
$$

*Reference: Hibbeler, Mechanics of Materials, 10th ed., §5.7.*

</details>

### Example 8.2 — Thermal Stress in a Constrained Bar

**Given:** A steel bar ($E = 200$ GPa, $\alpha = 12 \times 10^{-6}$ /°C, $A = 1000$ mm²) of length $L = 2$ m is fixed between two rigid walls at $20°$C. The temperature is raised to $80°$C. A gap of $\delta_{\text{gap}} = 0.5$ mm exists at one end before heating.

**Find:** (a) The stress in the bar after heating. (b) The temperature at which the bar first contacts the wall.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Part (b) first: Contact temperature.**

Free thermal expansion: $\delta_T = \alpha \Delta T \cdot L$

Contact occurs when $\delta_T = \delta_{\text{gap}}$:

$$
\alpha \Delta T_{\text{contact}} \cdot L = 0.5 \times 10^{-3}
$$

$$
\Delta T_{\text{contact}} = \frac{0.5 \times 10^{-3}}{12 \times 10^{-6} \times 2} = \frac{0.5 \times 10^{-3}}{24 \times 10^{-6}} = 20.83°\text{C}
$$

$$
T_{\text{contact}} = 20 + 20.83 = 40.83°\text{C}
$$

**Part (a): Stress after heating to 80°C.**

After contact, further temperature rise $\Delta T' = 80 - 40.83 = 39.17°$C is resisted by the walls.

Compatibility: total deformation = 0 (walls are rigid, gap already closed):

$$
\delta_{\text{thermal}} - \delta_{\text{mechanical}} = 0
$$

$$
\alpha \Delta T' L = \frac{PL}{AE}
$$

$$
P = \alpha \Delta T' \cdot AE = 12 \times 10^{-6} \times 39.17 \times 1000 \times 10^{-6} \times 200 \times 10^9
$$

$$
= 12 \times 10^{-6} \times 39.17 \times 200{,}000 = 94.0 \text{ kN}
$$

$$
\sigma = \frac{P}{A} = \frac{94{,}000}{1000 \times 10^{-6}} = 94.0 \text{ MPa (compression)}
$$

**Alternative (direct formula):**

$$
\sigma = -E\alpha\Delta T' = -200 \times 10^3 \times 12 \times 10^{-6} \times 39.17 = -94.0 \text{ MPa}
$$

Negative sign confirms compression (bar wants to expand but is restrained).

*Reference: Hibbeler, Mechanics of Materials, 10th ed., §4.6; Gere, §2.6.*

</details>

### Example 8.3 — Thin-Walled Torsion: Bredt's Formula

**Given:** A thin-walled box section (rectangular tube) with outer dimensions $b = 100$ mm, $h = 60$ mm. Wall thickness: top and bottom $t_1 = 4$ mm, sides $t_2 = 3$ mm. Applied torque $T = 2$ kN·m. Length $L = 1.5$ m, $G = 80$ GPa.

**Find:** (a) Shear stress in each wall. (b) Angle of twist.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Part (a): Shear stress via Bredt's formula.**

The enclosed area (measured to the median line):

$$
A_m = (b - t_2)(h - t_1) = (100 - 3)(60 - 4) = 97 \times 56 = 5432 \text{ mm}^2
$$

(More precisely, using centerline dimensions: width $= 100 - 3 = 97$ mm, height $= 60 - 4 = 56$ mm.)

Bredt's formula for shear flow:

$$
q = \frac{T}{2A_m} = \frac{2 \times 10^6 \text{ N·mm}}{2 \times 5432} = 184.1 \text{ N/mm}
$$

Shear stress in each wall:

$$
\tau_{\text{top/bottom}} = \frac{q}{t_1} = \frac{184.1}{4} = 46.0 \text{ MPa}
$$

$$
\tau_{\text{sides}} = \frac{q}{t_2} = \frac{184.1}{3} = 61.4 \text{ MPa}
$$

The **thinner walls carry higher shear stress** — a critical design consideration.

**Part (b): Angle of twist.**

$$
\phi = \frac{TL}{4A_m^2 G}\oint \frac{ds}{t}
$$

The line integral around the median perimeter:

$$
\oint \frac{ds}{t} = \frac{2 \times 97}{4} + \frac{2 \times 56}{3} = \frac{194}{4} + \frac{112}{3} = 48.5 + 37.33 = 85.83 \text{ mm}^{-1}
$$

Wait — units: $ds$ is in mm, $t$ is in mm, so $ds/t$ is dimensionless per mm... Actually $\oint ds/t$ has units of mm/mm = dimensionless? No: $ds$ has units of length (mm), $t$ has units of length (mm), so $ds/t$ is dimensionless and the integral has units of... Let me be careful.

$\oint \frac{ds}{t}$: integrate $1/t$ along the perimeter. Top: length $97$ mm at $t = 4$ mm → $97/4 = 24.25$. Bottom: same → $24.25$. Left side: $56$ mm at $t = 3$ mm → $56/3 = 18.67$. Right side: same → $18.67$.

$$
\oint \frac{ds}{t} = 2(24.25) + 2(18.67) = 48.5 + 37.33 = 85.83
$$

(dimensionless, since mm/mm)

$$
\phi = \frac{2 \times 10^6 \times 1500}{4 \times 5432^2 \times 80 \times 10^3} \times 85.83
$$

Wait — let me keep consistent units (N, mm, MPa):

$T = 2 \times 10^6$ N·mm, $L = 1500$ mm, $G = 80 \times 10^3$ MPa = $80{,}000$ N/mm².

$$
\phi = \frac{TL}{4A_m^2 G}\oint \frac{ds}{t} = \frac{2 \times 10^6 \times 1500}{4 \times (5432)^2 \times 80000} \times 85.83
$$

$$
= \frac{3 \times 10^9}{4 \times 29{,}506{,}624 \times 80000} \times 85.83
$$

$$
= \frac{3 \times 10^9}{9.442 \times 10^{12}} \times 85.83 = 3.178 \times 10^{-4} \times 85.83 = 0.0273 \text{ rad} = 1.56°
$$

*Reference: Timoshenko, Strength of Materials, Part II, §6; Hibbeler, §5.8.*

</details>

### Example 8.4 — Statically Indeterminate Axial Bar with Thermal Loading

**Given:** A composite bar consists of a steel core ($A_s = 600$ mm², $E_s = 200$ GPa, $\alpha_s = 12 \times 10^{-6}$/°C) surrounded by an aluminum sleeve ($A_a = 900$ mm², $E_a = 70$ GPa, $\alpha_a = 23 \times 10^{-6}$/°C). Both are rigidly attached at the ends (same length $L = 500$ mm). Temperature increases by $\Delta T = 50°$C.

**Find:** Stresses in each material and the elongation of the assembly.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Free thermal expansions (if unconstrained).**

$$
\delta_{s,\text{free}} = \alpha_s \Delta T \cdot L = 12 \times 10^{-6} \times 50 \times 500 = 0.300 \text{ mm}
$$

$$
\delta_{a,\text{free}} = \alpha_a \Delta T \cdot L = 23 \times 10^{-6} \times 50 \times 500 = 0.575 \text{ mm}
$$

Aluminum wants to expand more → it will be in **compression**; steel will be in **tension**.

**Step 2: Compatibility — both must have the same final length.**

$$
\delta_s = \delta_a = \delta \quad \text{(same elongation)}
$$

$$
\delta = \alpha_s \Delta T L + \frac{P_s L}{A_s E_s} = \alpha_a \Delta T L - \frac{P_a L}{A_a E_a}
$$

(Steel is pulled in tension by force $P_s$; aluminum is pushed in compression by force $P_a$.)

**Step 3: Equilibrium — no external force on the assembly.**

$$
P_s = P_a = P \quad \text{(internal force, equal and opposite)}
$$

Steel tension = aluminum compression (the assembly is self-equilibrating).

**Step 4: Solve for $P$.**

$$
\alpha_s \Delta T L + \frac{PL}{A_s E_s} = \alpha_a \Delta T L - \frac{PL}{A_a E_a}
$$

$$
\frac{P}{A_s E_s} + \frac{P}{A_a E_a} = (\alpha_a - \alpha_s)\Delta T
$$

$$
P\left(\frac{1}{600 \times 10^{-6} \times 200 \times 10^9} + \frac{1}{900 \times 10^{-6} \times 70 \times 10^9}\right) = (23 - 12) \times 10^{-6} \times 50
$$

$$
P\left(\frac{1}{120{,}000} + \frac{1}{63{,}000}\right) = 5.5 \times 10^{-4}
$$

(Units: $P$ in N, denominators in N)

$$
P(8.333 \times 10^{-6} + 15.873 \times 10^{-6}) = 5.5 \times 10^{-4}
$$

$$
P \times 24.206 \times 10^{-6} = 5.5 \times 10^{-4}
$$

$$
P = \frac{5.5 \times 10^{-4}}{24.206 \times 10^{-6}} = 22{,}720 \text{ N} = 22.72 \text{ kN}
$$

**Step 5: Stresses.**

$$
\sigma_s = \frac{P}{A_s} = \frac{22720}{600 \times 10^{-6}} = 37.9 \text{ MPa (tension)}
$$

$$
\sigma_a = \frac{P}{A_a} = \frac{22720}{900 \times 10^{-6}} = 25.2 \text{ MPa (compression)}
$$

**Step 6: Elongation.**

$$
\delta = \alpha_s \Delta T L + \frac{PL}{A_s E_s} = 0.300 + \frac{22720 \times 500}{120{,}000{,}000} = 0.300 + 0.0947 = 0.395 \text{ mm}
$$

**Verification:** $\delta = \alpha_a \Delta T L - \frac{PL}{A_a E_a} = 0.575 - \frac{22720 \times 500}{63{,}000{,}000} = 0.575 - 0.180 = 0.395$ mm ✓

*Reference: Hibbeler, Mechanics of Materials, 10th ed., §4.6; Gere, §2.7.*

</details>



---

## 📘 9. Appendix: Extended Derivations & Special Cases

### Appendix 9.1 — Derivation of the Torsion Formula $\tau = T\rho/J$ from Kinematics

**Goal:** Derive the shear stress distribution in a circular shaft under pure torsion from first principles.

**Assumptions:**
1. Cross-sections remain plane (no warping) — valid only for circular sections.
2. Cross-sections rotate as rigid disks (radii remain straight).
3. Material is linear elastic and isotropic.

**Step 1: Kinematics (deformation geometry).**

Consider a shaft of length $L$ with a small element at radius $\rho$ from the center. When the shaft twists by angle $\phi$ over length $L$, the element at radius $\rho$ displaces tangentially by:

$$
\delta = \rho\phi
$$

The shear strain (angle of distortion) of the element:

$$
\gamma = \frac{\delta}{L} = \frac{\rho\phi}{L} = \rho\frac{d\phi}{dz}
$$

where $d\phi/dz$ is the rate of twist (constant for uniform torque).

**Key observation:** Shear strain varies **linearly** with radius $\rho$. This is purely geometric — no material law used yet.

**Step 2: Constitutive law (Hooke's law in shear).**

$$
\tau = G\gamma = G\rho\frac{d\phi}{dz}
$$

Shear stress also varies linearly with $\rho$, zero at center, maximum at surface.

**Step 3: Equilibrium (relate stress to applied torque).**

The torque produced by the shear stress distribution over the cross-section:

$$
T = \int_A \tau \cdot \rho \, dA = \int_A G\frac{d\phi}{dz}\rho^2 \, dA = G\frac{d\phi}{dz}\int_A \rho^2 \, dA
$$

The integral $\int_A \rho^2 \, dA$ is the **polar moment of inertia** $J$:

$$
T = GJ\frac{d\phi}{dz}
$$

**Step 4: Solve for stress.**

From Step 2: $\tau = G\rho\frac{d\phi}{dz}$. From Step 3: $\frac{d\phi}{dz} = \frac{T}{GJ}$.

$$
\boxed{\tau = \frac{T\rho}{J}}
$$

And the angle of twist over length $L$:

$$
\phi = \frac{TL}{GJ}
$$

$\blacksquare$

**Why this fails for non-circular sections:** Assumption 1 (plane sections remain plane) is violated. Non-circular sections **warp** out of plane under torsion. The warping creates axial displacements that invalidate the linear $\gamma(\rho)$ relationship. Saint-Venant's torsion theory handles this using a warping function $\psi(x,y)$.

*Reference: Timoshenko, Strength of Materials, Part I, §3.1; Hibbeler, §5.2.*

### Appendix 9.2 — Non-Circular Torsion: Saint-Venant's Warping Function

For a prismatic bar of arbitrary cross-section under pure torsion, Saint-Venant showed that the displacement field takes the form:

$$
u_x = -\theta z \cdot y, \quad u_y = \theta z \cdot x, \quad u_z = \theta\psi(x,y)
$$

where $\theta = d\phi/dz$ is the rate of twist and $\psi(x,y)$ is the **warping function** satisfying:

$$
\nabla^2\psi = 0 \quad \text{(Laplace's equation in the cross-section)}
$$

with boundary condition on the cross-section boundary $\partial\Omega$:

$$
\frac{\partial\psi}{\partial n} = y\frac{dx}{ds} - x\frac{dy}{ds} \quad \text{(on } \partial\Omega\text{)}
$$

The shear stresses are:

$$
\tau_{xz} = G\theta\left(\frac{\partial\psi}{\partial x} - y\right), \quad \tau_{yz} = G\theta\left(\frac{\partial\psi}{\partial y} + x\right)
$$

The torque:

$$
T = G\theta J_{\text{eff}} \quad \text{where } J_{\text{eff}} = \int_A\left[x^2 + y^2 + x\frac{\partial\psi}{\partial y} - y\frac{\partial\psi}{\partial x}\right]dA
$$

**For a circular section:** $\psi = 0$ (no warping), and $J_{\text{eff}} = J = \pi c^4/2$. The standard formula is recovered.

**For an elliptical section** ($x^2/a^2 + y^2/b^2 = 1$):

$$
\psi = -\frac{a^2 - b^2}{a^2 + b^2}xy
$$

$$
J_{\text{eff}} = \frac{\pi a^3 b^3}{a^2 + b^2}
$$

$$
\tau_{\max} = \frac{2T}{\pi a b^2} \quad \text{(at the ends of the minor axis, NOT the major axis)}
$$

This counterintuitive result — maximum stress at the point **closest** to the center — is a hallmark of non-circular torsion.

**For a thin rectangular section** ($a \gg b$):

$$
J_{\text{eff}} \approx \frac{1}{3}ab^3, \quad \tau_{\max} \approx \frac{3T}{ab^2}
$$

*Reference: Timoshenko & Goodier, Theory of Elasticity, Ch. 10; Boresi & Schmidt, Advanced Mechanics of Materials, §6.4.*
