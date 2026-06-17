---
title: "12.5 — Bending of Beams & Shear Stress"
subject: "Solid Mechanics & Materials Science"
catalog: advanced
audience_tier: higher-education
chapter: "12.5"
type: chapter-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 12.5 — Bending of Beams & Shear Stress

> *"The theory of the bending of beams is one of the most important and most frequently applied theories in the whole of engineering science."*
> — **Stephen Timoshenko**, *History of Strength of Materials*

When transverse loads act on a beam, internal bending moments and shear forces develop. The bending moment produces **normal stresses** that vary linearly through the cross-section (tension on one side, compression on the other), while the shear force produces **shear stresses** with a parabolic distribution. This chapter derives both from first principles.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Construct **shear force** and **bending moment diagrams** (SFD/BMD).
2. Derive and apply the **flexure formula** $\sigma = -My/I$.
3. Compute the **moment of inertia** $I$ for common cross-sections.
4. Derive and apply the **shear formula** $\tau = VQ/(Ib)$.
5. Locate the **neutral axis** and understand its significance.
6. Derive the **Euler-Bernoulli beam equation** $EI\,d^4v/dx^4 = w(x)$.
7. Solve beam deflection problems by double integration.

---

## 🖼️ Visual Anchor — Beam Bending Stress Distribution

![math-12__12.5-fig1](math-12__12.5-fig1.svg)




---

## 📚 1. Definitions

### Definition 12.5.1 — Shear Force and Bending Moment

At any cross-section of a beam, the internal resultants are:

- **Shear force** $V(x)$: the resultant transverse force on the cut face.
- **Bending moment** $M(x)$: the resultant couple (moment) on the cut face.

Sign convention (positive): $V$ acts downward on the left face; $M$ causes the beam to "smile" (concave up, sagging).

### Definition 12.5.2 — Load-Shear-Moment Relations

$$
\frac{dV}{dx} = -w(x), \quad \frac{dM}{dx} = V(x)
$$

Combined:

$$
\frac{d^2M}{dx^2} = -w(x)
$$

where $w(x)$ is the distributed load intensity (positive upward).

### Definition 12.5.3 — Second Moment of Area (Moment of Inertia)

The **second moment of area** about the neutral axis:

$$
I = \int_A y^2\,dA
$$

| Cross-Section | $I$ |
|:---|:---|
| Rectangle $b \times h$ | $\frac{bh^3}{12}$ |
| Circle radius $c$ | $\frac{\pi c^4}{4}$ |
| Hollow circle | $\frac{\pi}{4}(c_o^4 - c_i^4)$ |
| I-beam (approx.) | $\frac{b_f h^3}{12} - \frac{(b_f - t_w)(h - 2t_f)^3}{12}$ |

### Definition 12.5.4 — Section Modulus

The **section modulus** $S$ relates maximum bending stress to moment:

$$
S = \frac{I}{c} \quad \implies \quad \sigma_{\max} = \frac{M}{S}
$$

where $c$ is the distance from the neutral axis to the extreme fiber.

### Definition 12.5.5 — First Moment of Area (for Shear)

The **first moment** $Q$ of the area above (or below) the point where shear stress is computed:

$$
Q = \int_{A'} y\,dA = \bar{y}' A'
$$

where $A'$ is the area above the cut and $\bar{y}'$ is its centroidal distance from the neutral axis.

### Definition 12.5.6 — Neutral Axis

The **neutral axis** is the line in the cross-section where bending stress is zero ($\sigma = 0$). For symmetric sections under pure bending, it passes through the centroid.

### Definition 12.5.7 — Radius of Curvature

The **radius of curvature** $\rho$ of the deflected beam:

$$
\frac{1}{\rho} = \kappa = \frac{M}{EI}
$$

For small deflections: $\kappa \approx v''(x) = d^2v/dx^2$.




---

## 📐 2. Axioms / Postulates

### Postulate 12.5.P1 — Bernoulli-Euler Hypothesis

Plane cross-sections perpendicular to the beam axis remain **plane** and **perpendicular** to the deformed axis after bending. This implies:
- Normal strain varies **linearly** with distance from the neutral axis.
- Shear deformation is neglected (valid for slender beams: $L/h > 10$).

### Postulate 12.5.P2 — Small Deflection Assumption

Beam deflections are small compared to the span: $v \ll L$. This allows:

$$
\kappa = \frac{1}{\rho} \approx \frac{d^2v}{dx^2}
$$

(The exact curvature $\kappa = v''/(1+v'^2)^{3/2}$ simplifies when $v' \ll 1$.)

### Postulate 12.5.P3 — Material is Linear Elastic

Stress is proportional to strain: $\sigma = E\varepsilon$. Combined with the linear strain distribution, this gives a linear stress distribution.

---

## 🛡️ 3. Lemmas

### Lemma 12.5.1 — Linear Strain Distribution from Geometry

<details>
<summary>🔍 Derivation</summary>

Consider a beam element of length $dx$ that bends through angle $d\theta$. The radius of curvature is $\rho$.

At the neutral axis: no change in length (by definition).

At distance $y$ above the neutral axis, the fiber has length:

$$
ds = (\rho - y)\,d\theta
$$

Original length: $dx = \rho\,d\theta$.

Strain at distance $y$:

$$
\varepsilon = \frac{ds - dx}{dx} = \frac{(\rho - y)d\theta - \rho\,d\theta}{\rho\,d\theta} = \frac{-y}{\rho} = -\kappa y
$$

The strain varies **linearly** with $y$, and is zero at $y = 0$ (neutral axis). $\blacksquare$

</details>

### Lemma 12.5.2 — Neutral Axis Passes Through Centroid

<details>
<summary>🔍 Proof</summary>

For pure bending (no axial force), the resultant normal force on the cross-section must be zero:

$$
\int_A \sigma\,dA = 0
$$

Substituting $\sigma = -E\kappa y$:

$$
-E\kappa \int_A y\,dA = 0
$$

Since $E \neq 0$ and $\kappa \neq 0$:

$$
\int_A y\,dA = 0
$$

This is the definition of the centroidal axis. Therefore the neutral axis passes through the centroid. $\blacksquare$

</details>

### Lemma 12.5.3 — Derivation of the Flexure Formula

<details>
<summary>🔍 Full Derivation</summary>

The resultant moment of the stress distribution must equal the internal bending moment $M$:

$$
M = -\int_A y \cdot \sigma\,dA
$$

(Negative sign: positive $M$ causes compression at $y \gt  0$ in our convention.)

Substituting $\sigma = -E\kappa y$:

$$
M = -\int_A y(-E\kappa y)\,dA = E\kappa \int_A y^2\,dA = EI\kappa
$$

Therefore:

$$
\kappa = \frac{M}{EI}
$$

And the stress:

$$
\sigma = -E\kappa y = -\frac{My}{I}
$$

This is the **flexure formula**. Maximum stress occurs at the extreme fibers ($y = \pm c$):

$$
\sigma_{\max} = \frac{Mc}{I} = \frac{M}{S}
$$

$\blacksquare$

</details>

### Lemma 12.5.4 — Derivation of the Shear Formula

<details>
<summary>🔍 Full Derivation</summary>

Consider a beam element between $x$ and $x + dx$. The bending moment changes from $M$ to $M + dM$.

Isolate the portion of the cross-section above a horizontal plane at distance $y_1$ from the neutral axis. The area of this portion is $A'$.

**Horizontal equilibrium** of this isolated block:

The difference in normal force between the two faces:

$$
dF = \int_{A'} (\sigma_{x+dx} - \sigma_x)\,dA = \int_{A'} \frac{-dM \cdot y}{I}\,dA = \frac{-dM}{I}\int_{A'} y\,dA = \frac{-dM}{I} \cdot Q
$$

where $Q = \int_{A'} y\,dA$ is the first moment of area $A'$ about the neutral axis.

This force difference is balanced by shear stress $\tau$ on the horizontal plane of width $b$ and length $dx$:

$$
\tau \cdot b \cdot dx = \frac{dM}{I} \cdot Q
$$

Since $dM/dx = V$:

$$
\tau = \frac{V \cdot Q}{I \cdot b}
$$

This is the **shear formula**. $\blacksquare$

</details>




---

## 👑 4. Theorems

### Theorem 12.5.1 — Flexure Formula

For a beam in pure bending with moment $M$ about the neutral axis:

$$
\sigma(y) = -\frac{My}{I}
$$

where $y$ is measured from the neutral axis (positive upward) and $I$ is the second moment of area about the neutral axis.

### Theorem 12.5.2 — Shear Formula

The transverse shear stress at a point in the cross-section:

$$
\tau = \frac{VQ}{Ib}
$$

where $V$ = shear force, $Q$ = first moment of the area beyond the point, $I$ = moment of inertia, $b$ = width at the point.

### Theorem 12.5.3 — Euler-Bernoulli Beam Equation

The governing differential equation for beam deflection:

$$
EI\frac{d^4v}{dx^4} = w(x)
$$

Or equivalently:

$$
EI\frac{d^2v}{dx^2} = M(x)
$$

### Theorem 12.5.4 — Parallel Axis Theorem

The moment of inertia about any axis parallel to the centroidal axis:

$$
I = I_c + Ad^2
$$

where $I_c$ is the centroidal moment of inertia, $A$ is the area, and $d$ is the distance between axes.

---

## ✍️ 5. Proofs / Derivations

### 5.1 Derivation: Euler-Bernoulli Beam Equation

<details>
<summary>🔍 Full Derivation</summary>

Starting from the moment-curvature relation:

$$
M(x) = EI\kappa = EI\frac{d^2v}{dx^2}
$$

Differentiate once:

$$
\frac{dM}{dx} = EI\frac{d^3v}{dx^3} = V(x)
$$

Differentiate again:

$$
\frac{dV}{dx} = EI\frac{d^4v}{dx^4} = -w(x) \cdot (-1) = w(x)
$$

(Sign depends on convention; with $w$ positive downward and using $dV/dx = -w$):

$$
EI\frac{d^4v}{dx^4} = w(x)
$$

**Boundary conditions:**
- Simply supported: $v = 0$, $M = EIv'' = 0$ at supports
- Fixed (clamped): $v = 0$, $v' = 0$ at wall
- Free end: $M = EIv'' = 0$, $V = EIv''' = 0$

$\blacksquare$

</details>

### 5.2 Derivation: Maximum Shear Stress in a Rectangular Section

<details>
<summary>🔍 Full Derivation</summary>

For a rectangular cross-section $b \times h$, with neutral axis at mid-height:

$I = bh^3/12$.

At distance $y_1$ from the neutral axis, the area above is:

$$
A' = b\left(\frac{h}{2} - y_1\right)
$$

Its centroid is at:

$$
\bar{y}' = \frac{1}{2}\left(\frac{h}{2} + y_1\right)
$$

First moment:

$$
Q = A' \cdot \bar{y}' = b\left(\frac{h}{2} - y_1\right) \cdot \frac{1}{2}\left(\frac{h}{2} + y_1\right) = \frac{b}{2}\left(\frac{h^2}{4} - y_1^2\right)
$$

Shear stress:

$$
\tau(y_1) = \frac{VQ}{Ib} = \frac{V \cdot \frac{b}{2}\left(\frac{h^2}{4} - y_1^2\right)}{\frac{bh^3}{12} \cdot b} = \frac{6V}{bh^3}\left(\frac{h^2}{4} - y_1^2\right)
$$

**Maximum** at $y_1 = 0$ (neutral axis):

$$
\tau_{\max} = \frac{6V}{bh^3} \cdot \frac{h^2}{4} = \frac{3V}{2bh} = \frac{3V}{2A}
$$

The maximum shear stress in a rectangular beam is **1.5 times** the average shear stress $V/A$. $\blacksquare$

</details>

### 5.3 Derivation: Cantilever Beam Deflection by Double Integration

<details>
<summary>🔍 Full Derivation</summary>

**Problem:** Cantilever beam of length $L$, fixed at $x = 0$, point load $P$ at free end $x = L$.

**Moment equation:** $M(x) = -P(L - x)$ (using free-body of right portion).

**Differential equation:**

$$
EI\frac{d^2v}{dx^2} = M(x) = -P(L - x) = -PL + Px
$$

**First integration:**

$$
EI\frac{dv}{dx} = -PLx + \frac{Px^2}{2} + C_1
$$

**Boundary condition:** At $x = 0$ (fixed end), $dv/dx = 0$:

$$
0 = 0 + 0 + C_1 \implies C_1 = 0
$$

**Second integration:**

$$
EIv = -\frac{PLx^2}{2} + \frac{Px^3}{6} + C_2
$$

**Boundary condition:** At $x = 0$, $v = 0$:

$$
0 = 0 + 0 + C_2 \implies C_2 = 0
$$

**Deflection equation:**

$$
v(x) = \frac{P}{6EI}(x^3 - 3Lx^2) = \frac{Px^2}{6EI}(x - 3L)
$$

**Maximum deflection** at $x = L$:

$$
v_{\max} = \frac{P}{6EI}(L^3 - 3L^3) = \frac{-PL^3}{3EI}
$$

The negative sign indicates downward deflection. Magnitude: $\delta_{\max} = PL^3/(3EI)$. $\blacksquare$

</details>




---

## 🧮 6. Worked Examples

### Example 12.5.1 — Maximum Bending Stress in a Simply-Supported Beam

**Given:** A simply-supported beam of length $L = 4$ m carries a concentrated load $P = 20$ kN at midspan. The cross-section is rectangular: $b = 100$ mm, $h = 250$ mm.

**Find:** Maximum bending stress.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Maximum bending moment.**

For a simply-supported beam with midspan load:

$$
M_{\max} = \frac{PL}{4} = \frac{20 \times 4}{4} = 20 \text{ kN·m}
$$

**Step 2: Moment of inertia.**

$$
I = \frac{bh^3}{12} = \frac{0.1 \times 0.25^3}{12} = \frac{0.1 \times 0.015625}{12} = 1.302 \times 10^{-4} \text{ m}^4
$$

**Step 3: Maximum bending stress.**

$$
\sigma_{\max} = \frac{Mc}{I} = \frac{20 \times 10^3 \times 0.125}{1.302 \times 10^{-4}} = \frac{2500}{1.302 \times 10^{-4}} = 19.2 \text{ MPa}
$$

</details>

---

### Example 12.5.2 — Shear Stress Distribution in a T-Beam

**Given:** A T-beam with flange $200 \times 30$ mm and web $30 \times 170$ mm (total height 200 mm). Shear force $V = 50$ kN.

**Find:** Maximum shear stress and its location.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Locate centroid (from bottom).**

$$
A_{\text{flange}} = 200 \times 30 = 6000 \text{ mm}^2, \quad \bar{y}_f = 200 - 15 = 185 \text{ mm}
$$

$$
A_{\text{web}} = 30 \times 170 = 5100 \text{ mm}^2, \quad \bar{y}_w = 170/2 = 85 \text{ mm}
$$

$$
\bar{y} = \frac{6000(185) + 5100(85)}{6000 + 5100} = \frac{1{,}110{,}000 + 433{,}500}{11{,}100} = \frac{1{,}543{,}500}{11{,}100} = 139.1 \text{ mm from bottom}
$$

**Step 2: Moment of inertia about centroidal axis (parallel axis theorem).**

$$
I_f = \frac{200 \times 30^3}{12} + 6000(185 - 139.1)^2 = 450{,}000 + 6000(45.9)^2 = 450{,}000 + 12{,}640{,}860 = 13{,}090{,}860 \text{ mm}^4
$$

$$
I_w = \frac{30 \times 170^3}{12} + 5100(139.1 - 85)^2 = 12{,}282{,}500 + 5100(54.1)^2 = 12{,}282{,}500 + 14{,}923{,}041 = 27{,}205{,}541 \text{ mm}^4
$$

$$
I = 13{,}090{,}860 + 27{,}205{,}541 = 40{,}296{,}401 \text{ mm}^4 = 4.03 \times 10^{-5} \text{ m}^4
$$

**Step 3: Maximum shear stress (at neutral axis).**

$Q$ at the neutral axis (area below NA, $\bar{y} = 139.1$ mm from bottom):

$$
Q = 30 \times 139.1 \times \frac{139.1}{2} = 30 \times 139.1 \times 69.55 = 290{,}200 \text{ mm}^3
$$

Width at NA: $b = 30$ mm (web).

$$
\tau_{\max} = \frac{VQ}{Ib} = \frac{50{,}000 \times 290{,}200 \times 10^{-9}}{4.03 \times 10^{-5} \times 0.030} = \frac{14.51 \times 10^{-3}}{1.209 \times 10^{-6}} = 12.0 \text{ MPa}
$$

Maximum shear stress occurs at the **neutral axis** in the web.

</details>

---

### Example 12.5.3 — Cantilever Beam Deflection Under Uniform Load

**Given:** A cantilever beam (steel, $E = 200$ GPa) of length $L = 3$ m with rectangular section $50 \times 150$ mm carries uniform load $w = 8$ kN/m.

**Find:** Maximum deflection and slope at the free end.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Moment of inertia.**

$$
I = \frac{bh^3}{12} = \frac{0.05 \times 0.15^3}{12} = \frac{0.05 \times 3.375 \times 10^{-3}}{12} = 1.406 \times 10^{-5} \text{ m}^4
$$

**Step 2: Standard formulas for cantilever with uniform load.**

Maximum deflection (at free end):

$$
\delta_{\max} = \frac{wL^4}{8EI} = \frac{8000 \times 3^4}{8 \times 200 \times 10^9 \times 1.406 \times 10^{-5}}
$$

$$
= \frac{8000 \times 81}{22{,}500{,}000} = \frac{648{,}000}{22{,}500{,}000} = 0.0288 \text{ m} = 28.8 \text{ mm}
$$

Maximum slope (at free end):

$$
\theta_{\max} = \frac{wL^3}{6EI} = \frac{8000 \times 27}{6 \times 200 \times 10^9 \times 1.406 \times 10^{-5}} = \frac{216{,}000}{16{,}872{,}000} = 0.0128 \text{ rad} = 0.734°
$$

</details>

---

### Example 12.5.4 — Composite Beam (Two Materials)

**Given:** A beam is made of wood ($E_w = 12$ GPa) with a steel plate ($E_s = 200$ GPa) bonded to the bottom. Wood: $100 \times 200$ mm. Steel plate: $100 \times 10$ mm. Bending moment $M = 5$ kN·m.

**Find:** Maximum stress in each material using the transformed-section method.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Modular ratio.**

$$
n = \frac{E_s}{E_w} = \frac{200}{12} = 16.67
$$

**Step 2: Transform steel to equivalent wood.**

Transformed steel width: $b_s' = n \times 100 = 1667$ mm.

**Step 3: Locate centroid of transformed section (from bottom of steel).**

$$
A_w = 100 \times 200 = 20{,}000 \text{ mm}^2, \quad \bar{y}_w = 10 + 100 = 110 \text{ mm}
$$

$$
A_s' = 1667 \times 10 = 16{,}670 \text{ mm}^2, \quad \bar{y}_s = 5 \text{ mm}
$$

$$
\bar{y} = \frac{20000(110) + 16670(5)}{20000 + 16670} = \frac{2{,}200{,}000 + 83{,}350}{36{,}670} = 62.3 \text{ mm from bottom}
$$

**Step 4: Transformed moment of inertia.**

$$
I_w = \frac{100 \times 200^3}{12} + 20000(110 - 62.3)^2 = 66.67 \times 10^6 + 20000(47.7)^2 = 66.67 \times 10^6 + 45.5 \times 10^6 = 112.2 \times 10^6 \text{ mm}^4
$$

$$
I_s' = \frac{1667 \times 10^3}{12} + 16670(62.3 - 5)^2 = 139{,}000 + 16670(57.3)^2 = 139{,}000 + 54.7 \times 10^6 = 54.8 \times 10^6 \text{ mm}^4
$$

$$
I_T = 112.2 \times 10^6 + 54.8 \times 10^6 = 167.0 \times 10^6 \text{ mm}^4
$$

**Step 5: Stresses.**

Top of wood ($y = 210 - 62.3 = 147.7$ mm from NA):

$$
\sigma_{w,\text{top}} = \frac{My}{I_T} = \frac{5 \times 10^6 \times 147.7}{167.0 \times 10^6} = 4.42 \text{ MPa}
$$

Bottom of steel ($y = -62.3$ mm from NA):

$$
\sigma_{s,\text{bot}} = n \cdot \frac{M \cdot 62.3}{I_T} = 16.67 \times \frac{5 \times 10^6 \times 62.3}{167.0 \times 10^6} = 16.67 \times 1.865 = 31.1 \text{ MPa}
$$

</details>

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- **Previous:** [12.4 - Axial Loading & Torsion](12.4---Axial-Loading-&-Torsion) — Axial and torsional loading modes
- **Next:** [12.6 - Principal Stresses - Mohr's Circle](12.6---Principal-Stresses---Mohr's-Circle) — Combining bending and shear stresses
- **Statics:** [12.1 - Statics & Equilibrium](12.1---Statics-&-Equilibrium) — Support reactions needed for SFD/BMD
- **Calculus:** [1.3 - Integration Techniques](1.3---Integration-Techniques) — Integration for deflection curves

### External Resources
- 📖 **Hibbeler, R.C.** *Mechanics of Materials*, 10th ed. — Chapters 6 (Bending) & 7 (Transverse Shear).
- 🎬 **StructureFree** — [Beam Bending Playlist](https://www.youtube.com/playlist?list=PL44E9FA04BCEE07C6)
- 🎬 **MIT OCW 2.001** — Beam theory lectures
- 📖 **Gere & Goodno** — *Mechanics of Materials*, 9th ed. — Chapters 5–6.

---

## 📎 Appendix: Additional Theory & Examples

### A.1 Shear Force and Bending Moment Diagram Construction

**Procedure for SFD/BMD:**

1. Compute all support reactions.
2. Starting from the left end, move rightward:
   - At concentrated loads: $V$ jumps by the load magnitude.
   - Under distributed loads: $V$ changes linearly (for uniform $w$) or parabolically.
   - $M$ is the integral of $V$: linear under constant $V$, parabolic under linear $V$.
3. At concentrated moments: $M$ jumps by the moment magnitude.

**Key relationships:**
- $V = 0$ at points of maximum $M$ (for continuous loading).
- Area under SFD between two points = change in $M$ between those points.
- Slope of BMD at any point = value of $V$ at that point.

### A.2 Beam Deflection Formulas (Common Cases)

| Loading | $\delta_{\max}$ | Location |
|:---|:---|:---|
| SS, midspan $P$ | $\frac{PL^3}{48EI}$ | Midspan |
| SS, uniform $w$ | $\frac{5wL^4}{384EI}$ | Midspan |
| Cantilever, tip $P$ | $\frac{PL^3}{3EI}$ | Free end |
| Cantilever, uniform $w$ | $\frac{wL^4}{8EI}$ | Free end |
| Cantilever, tip moment $M_0$ | $\frac{M_0 L^2}{2EI}$ | Free end |

### A.3 Derivation: Simply-Supported Beam with Uniform Load (Double Integration)

<details>
<summary>🔍 Full Derivation</summary>

**Setup:** SS beam, length $L$, uniform load $w$ (downward). Reactions: $A_y = B_y = wL/2$.

**Moment equation** (taking free body from left):

$$
M(x) = \frac{wL}{2}x - \frac{wx^2}{2} = \frac{w}{2}(Lx - x^2)
$$

**Differential equation:**

$$
EI\frac{d^2v}{dx^2} = M(x) = \frac{w}{2}(Lx - x^2)
$$

**First integration:**

$$
EI\frac{dv}{dx} = \frac{w}{2}\left(\frac{Lx^2}{2} - \frac{x^3}{3}\right) + C_1
$$

**Second integration:**

$$
EIv = \frac{w}{2}\left(\frac{Lx^3}{6} - \frac{x^4}{12}\right) + C_1 x + C_2
$$

**Boundary conditions:**
- $v(0) = 0$: $C_2 = 0$
- $v(L) = 0$: $\frac{w}{2}\left(\frac{L^4}{6} - \frac{L^4}{12}\right) + C_1 L = 0$

$$
\frac{w}{2} \cdot \frac{L^4}{12} + C_1 L = 0 \implies C_1 = -\frac{wL^3}{24}
$$

**Deflection equation:**

$$
v(x) = \frac{w}{24EI}\left(2Lx^3 - x^4 - L^3 x\right) = \frac{wx}{24EI}(L^3 - 2Lx^2 + x^3)
$$

**Maximum deflection** at $x = L/2$:

$$
v_{\max} = \frac{w(L/2)}{24EI}\left(L^3 - 2L\frac{L^2}{4} + \frac{L^3}{8}\right) = \frac{wL}{48EI}\left(L^3 - \frac{L^3}{2} + \frac{L^3}{8}\right)
$$

$$
= \frac{wL}{48EI} \cdot \frac{5L^3}{8} = \frac{5wL^4}{384EI}
$$

$\blacksquare$

</details>

### A.4 Example: Moment of Inertia of a Composite Section

**Given:** An I-beam with flanges $200 \times 20$ mm (top and bottom) and web $20 \times 260$ mm (total height = 300 mm).

**Find:** Moment of inertia about the centroidal axis.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

By symmetry, the centroid is at mid-height ($\bar{y} = 150$ mm from bottom).

**Web:** $I_w = \frac{20 \times 260^3}{12} = 29{,}293{,}333$ mm⁴

**Top flange:** $I_{f,t} = \frac{200 \times 20^3}{12} + (200 \times 20)(150 - 10)^2 = 133{,}333 + 4000 \times 19600 = 133{,}333 + 78{,}400{,}000 = 78{,}533{,}333$ mm⁴

**Bottom flange:** Same as top by symmetry: $I_{f,b} = 78{,}533{,}333$ mm⁴

**Total:**

$$
I = 29{,}293{,}333 + 78{,}533{,}333 + 78{,}533{,}333 = 186{,}360{,}000 \text{ mm}^4 = 1.864 \times 10^{-4} \text{ m}^4
$$

**Section modulus:** $S = I/c = 186{,}360{,}000/150 = 1{,}242{,}400$ mm³

</details>

---

*Next: [12.6 - Principal Stresses - Mohr's Circle](12.6---Principal-Stresses---Mohr's-Circle) →*


---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — Composite Beam (Steel + Concrete) via Transformed Section

**Given:** A reinforced concrete beam has a rectangular concrete section $b = 300$ mm, $h = 500$ mm ($E_c = 25$ GPa). Two steel reinforcing bars (total area $A_s = 1500$ mm²) are placed at $d = 450$ mm from the top ($E_s = 200$ GPa). The beam carries a bending moment $M = 120$ kN·m. Assume concrete carries no tension (cracked section analysis).

**Find:** (a) Neutral axis depth. (b) Maximum compressive stress in concrete. (c) Stress in steel reinforcement.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Modular ratio.**

$$
n = \frac{E_s}{E_c} = \frac{200}{25} = 8
$$

Transform steel to equivalent concrete: $A_s' = nA_s = 8 \times 1500 = 12{,}000$ mm².

**Step 2: Locate neutral axis (cracked section — concrete below NA is ignored).**

Let $c$ = depth of NA from the top (compression zone depth). The concrete compression zone is $b \times c = 300c$ mm². The transformed steel is at depth $d = 450$ mm.

First moment of areas about the NA (setting compression area moment = tension area moment):

$$
\frac{bc^2}{2} = nA_s(d - c)
$$

$$
\frac{300c^2}{2} = 12000(450 - c)
$$

$$
150c^2 = 5{,}400{,}000 - 12000c
$$

$$
150c^2 + 12000c - 5{,}400{,}000 = 0
$$

$$
c^2 + 80c - 36{,}000 = 0
$$

Quadratic formula:

$$
c = \frac{-80 + \sqrt{6400 + 144000}}{2} = \frac{-80 + \sqrt{150400}}{2} = \frac{-80 + 387.9}{2} = 153.9 \text{ mm}
$$

**Step 3: Moment of inertia of cracked transformed section about NA.**

$$
I_{cr} = \frac{bc^3}{3} + nA_s(d-c)^2
$$

$$
= \frac{300(153.9)^3}{3} + 12000(450 - 153.9)^2
$$

$$
= \frac{300 \times 3{,}647{,}000}{3} + 12000(296.1)^2
$$

$$
= 364{,}700{,}000 + 12000 \times 87{,}675 = 364.7 \times 10^6 + 1052.1 \times 10^6 = 1416.8 \times 10^6 \text{ mm}^4
$$

**Step 4: Stresses.**

Maximum concrete stress (at top, $y = c$ from NA):

$$
\sigma_{c,\max} = \frac{Mc}{I_{cr}} = \frac{120 \times 10^6 \times 153.9}{1416.8 \times 10^6} = 13.0 \text{ MPa (compression)}
$$

Steel stress (at $y = d - c = 296.1$ mm from NA, multiply by $n$):

$$
\sigma_s = n \cdot \frac{M(d-c)}{I_{cr}} = 8 \times \frac{120 \times 10^6 \times 296.1}{1416.8 \times 10^6} = 8 \times 25.1 = 200.6 \text{ MPa (tension)}
$$

**Check:** Typical allowable: $\sigma_c \leq 0.45f_c' \approx 13.5$ MPa for 30 MPa concrete ✓; $\sigma_s \leq 0.6f_y \approx 250$ MPa for Grade 420 steel ✓.

*Reference: Gere & Goodno, Mechanics of Materials, §6.4; ACI 318.*

</details>

### Example 8.2 — Cantilever with Distributed + Point Load: Deflection by Double Integration

**Given:** A cantilever beam (fixed at $A$, free at $B$) of length $L = 3$ m carries: uniform load $w = 10$ kN/m over the entire span AND a point load $P = 15$ kN at the free end. $EI = 40{,}000$ kN·m².

**Find:** (a) Deflection at the free end. (b) Slope at the free end. (c) Location and magnitude of maximum deflection (which is at the free end for a cantilever).

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Moment equation (measuring $x$ from the fixed end $A$).**

At a section distance $x$ from $A$, the moment (using the free-body of the right portion, or equivalently from the left with known reactions):

Reactions at $A$: $V_A = wL + P = 10(3) + 15 = 45$ kN, $M_A = wL^2/2 + PL = 10(9)/2 + 15(3) = 45 + 45 = 90$ kN·m.

$$
M(x) = -M_A + V_A x - \frac{wx^2}{2} = -90 + 45x - 5x^2
$$

**Step 2: Differential equation $EI\,v'' = M(x)$.**

$$
EI\frac{d^2v}{dx^2} = -90 + 45x - 5x^2
$$

**Step 3: First integration (slope).**

$$
EI\frac{dv}{dx} = -90x + \frac{45x^2}{2} - \frac{5x^3}{3} + C_1
$$

BC: $v'(0) = 0$ (fixed end): $C_1 = 0$.

$$
EI\,v'(x) = -90x + 22.5x^2 - \frac{5x^3}{3}
$$

**Step 4: Second integration (deflection).**

$$
EI\,v(x) = -45x^2 + 7.5x^3 - \frac{5x^4}{12} + C_2
$$

BC: $v(0) = 0$ (fixed end): $C_2 = 0$.

$$
EI\,v(x) = -45x^2 + 7.5x^3 - \frac{5x^4}{12}
$$

**Step 5: Evaluate at free end ($x = L = 3$ m).**

$$
EI\,v(3) = -45(9) + 7.5(27) - \frac{5(81)}{12} = -405 + 202.5 - 33.75 = -236.25 \text{ kN·m}^3
$$

$$
v(3) = \frac{-236.25}{40000} = -5.91 \times 10^{-3} \text{ m} = -5.91 \text{ mm (downward)}
$$

Slope at free end:

$$
EI\,v'(3) = -90(3) + 22.5(9) - \frac{5(27)}{3} = -270 + 202.5 - 45 = -112.5 \text{ kN·m}^2
$$

$$
v'(3) = \frac{-112.5}{40000} = -2.81 \times 10^{-3} \text{ rad} = -0.161°
$$

**Verification by superposition:**

$$
\delta_{\text{tip}} = \frac{wL^4}{8EI} + \frac{PL^3}{3EI} = \frac{10(81)}{8(40000)} + \frac{15(27)}{3(40000)} = \frac{810}{320000} + \frac{405}{120000}
$$

$$
= 2.531 \times 10^{-3} + 3.375 \times 10^{-3} = 5.91 \times 10^{-3} \text{ m} \quad \checkmark
$$

*Reference: Hibbeler, Mechanics of Materials, 10th ed., §12.2.*

</details>

### Example 8.3 — Shear Stress in an I-Beam Web

**Given:** A W310×60 steel I-beam (approximate dimensions: flange $b_f = 200$ mm, $t_f = 15$ mm; web $h_w = 280$ mm, $t_w = 10$ mm; total depth $d = 310$ mm). Shear force $V = 200$ kN.

**Find:** (a) Shear stress distribution in the web. (b) Maximum shear stress. (c) Percentage of shear carried by the web.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Moment of inertia (about centroidal axis).**

$$
I = \frac{b_f d^3}{12} - \frac{(b_f - t_w)h_w^3}{12} = \frac{200(310)^3}{12} - \frac{190(280)^3}{12}
$$

$$
= \frac{200 \times 29{,}791{,}000}{12} - \frac{190 \times 21{,}952{,}000}{12}
$$

$$
= 496{,}517{,}000 - 347{,}573{,}000 = 148{,}944{,}000 \text{ mm}^4 \approx 1.489 \times 10^8 \text{ mm}^4
$$

**Step 2: First moment $Q$ at the neutral axis (maximum $Q$).**

$Q_{\text{NA}}$ = first moment of area above the NA about the NA:

$$
Q_{\text{NA}} = b_f t_f\left(\frac{d}{2} - \frac{t_f}{2}\right) + t_w\left(\frac{h_w}{2}\right)\left(\frac{h_w/2}{2}\right)
$$

$$
= 200(15)(155 - 7.5) + 10(140)(70)
$$

$$
= 200(15)(147.5) + 10(140)(70) = 442{,}500 + 98{,}000 = 540{,}500 \text{ mm}^3
$$

**Step 3: Maximum shear stress (at NA).**

$$
\tau_{\max} = \frac{VQ_{\text{NA}}}{It_w} = \frac{200{,}000 \times 540{,}500}{1.489 \times 10^8 \times 10} = \frac{1.081 \times 10^{11}}{1.489 \times 10^9} = 72.6 \text{ MPa}
$$

**Step 4: Shear stress at flange-web junction.**

$Q$ at the junction (just the flange area above):

$$
Q_{\text{junction}} = b_f t_f\left(\frac{d}{2} - \frac{t_f}{2}\right) = 200(15)(147.5) = 442{,}500 \text{ mm}^3
$$

$$
\tau_{\text{junction}} = \frac{VQ_{\text{junction}}}{It_w} = \frac{200{,}000 \times 442{,}500}{1.489 \times 10^8 \times 10} = 59.5 \text{ MPa}
$$

The shear stress in the web varies parabolically from $59.5$ MPa at the flange junction to $72.6$ MPa at the NA.

**Step 5: Percentage of shear carried by web.**

Average web shear stress $\approx (\tau_{\text{junction}} + \tau_{\max})/2 = (59.5 + 72.6)/2 = 66.1$ MPa.

$$
V_{\text{web}} \approx \tau_{\text{avg}} \times h_w \times t_w = 66.1 \times 280 \times 10 = 185{,}000 \text{ N} = 185 \text{ kN}
$$

$$
\frac{V_{\text{web}}}{V} = \frac{185}{200} = 92.5\%
$$

The web carries over 90% of the transverse shear — this is why I-beams are efficient.

*Reference: Hibbeler, Mechanics of Materials, 10th ed., §7.2; Gere, §5.8.*

</details>



---

## 📘 9. Appendix: Extended Derivations & Special Cases

### Appendix 9.1 — Derivation of the Euler-Bernoulli Beam Equation

**Goal:** Derive $EI\frac{d^4v}{dx^4} = q(x)$ from kinematics, constitutive law, and equilibrium.

**Step 1: Kinematic assumption (Euler-Bernoulli hypothesis).**

Plane sections remain plane and perpendicular to the deformed neutral axis. For small deflections, the axial strain at distance $y$ from the neutral axis:

$$
\varepsilon_{xx}(x,y) = -y\kappa(x) = -y\frac{d^2v}{dx^2}
$$

where $\kappa = 1/R \approx v''$ is the curvature (for small slopes $v' \ll 1$).

**Step 2: Constitutive law (Hooke's law).**

$$
\sigma_{xx} = E\varepsilon_{xx} = -Ey\frac{d^2v}{dx^2}
$$

**Step 3: Resultant moment from stress distribution.**

$$
M(x) = -\int_A \sigma_{xx} \cdot y \, dA = -\int_A \left(-Ey\frac{d^2v}{dx^2}\right)y \, dA = E\frac{d^2v}{dx^2}\int_A y^2 \, dA
$$

$$
M = EI\frac{d^2v}{dx^2}
$$

This is the **moment-curvature relation**.

**Step 4: Equilibrium of a beam element.**

For a beam element of length $dx$ under distributed load $q(x)$ (force/length, positive upward):

Force equilibrium: $\frac{dV}{dx} = -q(x)$

Moment equilibrium: $\frac{dM}{dx} = V(x)$

**Step 5: Combine.**

$$
\frac{d^2M}{dx^2} = \frac{dV}{dx} = -q(x)
$$

Substituting $M = EIv''$:

$$
\frac{d^2}{dx^2}\left(EI\frac{d^2v}{dx^2}\right) = -q(x)
$$

For constant $EI$:

$$
\boxed{EI\frac{d^4v}{dx^4} = -q(x)}
$$

(Sign convention: $q$ positive upward, $v$ positive upward.)

**Boundary conditions (4 needed for 4th-order ODE):**

| Support | Conditions |
|:---|:---|
| Fixed end | $v = 0$, $v' = 0$ |
| Simply supported | $v = 0$, $M = EIv'' = 0$ |
| Free end | $M = EIv'' = 0$, $V = EIv''' = 0$ |

$\blacksquare$

*Reference: Timoshenko, Strength of Materials, Part I, §4; Hibbeler, §12.1.*

### Appendix 9.2 — Castigliano's Second Theorem for Beam Deflections

**Statement:** For a linearly elastic structure, the displacement $\delta_i$ at the point and in the direction of an applied force $P_i$ equals the partial derivative of the total strain energy with respect to that force:

$$
\delta_i = \frac{\partial U}{\partial P_i}
$$

For rotation at a point where moment $M_i$ is applied:

$$
\theta_i = \frac{\partial U}{\partial M_i}
$$

**Strain energy in bending:**

$$
U = \int_0^L \frac{M(x)^2}{2EI}\,dx
$$

Therefore:

$$
\delta_i = \frac{\partial U}{\partial P_i} = \int_0^L \frac{M(x)}{EI}\frac{\partial M}{\partial P_i}\,dx
$$

**Application: Deflection of a simply-supported beam with midspan load $P$.**

Moment equation (left half, $0 \leq x \leq L/2$): $M(x) = \frac{P}{2}x$

$$
\frac{\partial M}{\partial P} = \frac{x}{2}
$$

By symmetry, integrate over left half and double:

$$
\delta = 2\int_0^{L/2}\frac{M}{EI}\frac{\partial M}{\partial P}\,dx = 2\int_0^{L/2}\frac{(Px/2)(x/2)}{EI}\,dx = \frac{P}{2EI}\int_0^{L/2}x^2\,dx
$$

$$
= \frac{P}{2EI}\cdot\frac{(L/2)^3}{3} = \frac{P}{2EI}\cdot\frac{L^3}{24} = \frac{PL^3}{48EI}
$$

This matches the standard formula. ✓

**Dummy load method:** To find deflection at a point where no load exists, apply a fictitious ("dummy") force $Q$ at that point, compute $\partial M/\partial Q$, then set $Q = 0$ after differentiation.

*Reference: Gere & Goodno, Mechanics of Materials, §9.9; Hibbeler, §14.6.*

### Appendix 9.3 — Shear Stress Distribution Derivation (General Cross-Section)

**Goal:** Derive the shear formula $\tau = VQ/(Ib)$ from equilibrium of a beam element.

**Setup:** Consider a beam element between $x$ and $x + dx$. The bending moment changes from $M$ to $M + dM$ (where $dM = V\,dx$). The bending stress on the left face at height $y$: $\sigma = My/I$. On the right face: $\sigma + d\sigma = (M+dM)y/I$.

**Step 1: Isolate a horizontal slice** above height $y_1$ (from $y_1$ to the top at $c$).

The net horizontal force on this slice due to the change in bending stress:

$$
dF = \int_{y_1}^{c} d\sigma \cdot b(y)\,dy = \int_{y_1}^{c}\frac{dM}{I}y\,b(y)\,dy = \frac{dM}{I}\int_{y_1}^{c}y\,b(y)\,dy = \frac{dM}{I}\cdot Q
$$

where $Q = \int_{y_1}^{c}y\,b(y)\,dy$ is the first moment of the area above $y_1$ about the neutral axis.

**Step 2: This horizontal force is balanced by shear stress on the bottom face of the slice.**

$$
\tau \cdot b(y_1) \cdot dx = dF = \frac{dM}{I}Q = \frac{V\,dx}{I}Q
$$

$$
\boxed{\tau(y_1) = \frac{VQ}{Ib(y_1)}}
$$

$\blacksquare$

**Key observations:**
- $\tau$ is maximum where $Q/b$ is maximum (usually at the neutral axis).
- For rectangular sections: $\tau_{\max} = \frac{3V}{2A}$ (50% above average shear stress $V/A$).
- For circular sections: $\tau_{\max} = \frac{4V}{3A}$ (33% above average).
- The formula assumes $\tau$ is uniform across the width $b$ at height $y_1$ — accurate for thin webs, approximate for wide flanges.

*Reference: Timoshenko, Strength of Materials, Part I, §4.5; Hibbeler, §7.2.*
