---
title: "12.2 — Stress & Strain Tensors"
subject: "Solid Mechanics & Materials Science"
catalog: advanced
audience_tier: higher-education
chapter: "12.2"
type: chapter-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 12.2 — Stress & Strain Tensors

> *"The concept of stress, as we understand it today, was essentially achieved by Cauchy, who introduced the idea that the state of stress at a point is completely defined by a second-order tensor."*
> — **Augustin-Louis Cauchy** (1789–1857)

When external forces act on a deformable body, internal forces develop throughout the material. **Stress** quantifies the intensity of these internal forces per unit area, while **strain** quantifies the resulting deformation. Both are second-order tensors — they transform according to specific rules under coordinate rotation, and their eigenvalues (principal values) reveal the maximum intensities and their orientations.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Define the **Cauchy stress tensor** $\boldsymbol{\sigma}$ and explain its physical meaning on an infinitesimal element.
2. Identify all **nine components** of the 3D stress tensor and their sign conventions.
3. Prove the **symmetry** of the stress tensor ($\sigma_{ij} = \sigma_{ji}$) from moment equilibrium.
4. Define **engineering strain** and the **infinitesimal strain tensor** $\boldsymbol{\varepsilon}$.
5. Decompose the stress tensor into **hydrostatic** (volumetric) and **deviatoric** parts.
6. Transform stress components under coordinate rotation using tensor transformation rules.
7. Connect stress/strain tensors to [2.6 - Eigenvalues Eigenvectors & Diagonalization](2.6---Eigenvalues-Eigenvectors-&-Diagonalization) (principal stresses as eigenvalues).

---

## 🖼️ Visual Anchor — 3D Stress Element

![math-12__12.2-fig1](math-12__12.2-fig1.svg)

---

## 📚 1. Definitions

### Definition 12.2.1 — Traction Vector (Stress Vector)

Consider an infinitesimal area element $dA$ with outward unit normal $\hat{\mathbf{n}}$ at a point inside a loaded body. The **traction vector** (stress vector) on that surface is:

$$
\mathbf{t}^{(\hat{\mathbf{n}})} = \lim_{\Delta A \to 0} \frac{\Delta \mathbf{F}}{\Delta A}
$$

where $\Delta \mathbf{F}$ is the resultant internal force on area $\Delta A$. Units: Pa = N/m².

### Definition 12.2.2 — Cauchy Stress Tensor

The **Cauchy stress tensor** $\boldsymbol{\sigma}$ is the second-order tensor that maps any unit normal $\hat{\mathbf{n}}$ to the traction vector on the corresponding surface:

$$
\mathbf{t}^{(\hat{\mathbf{n}})} = \boldsymbol{\sigma} \cdot \hat{\mathbf{n}}
$$

In index notation:

$$
t_i^{(n)} = \sigma_{ij} n_j
$$

The component $\sigma_{ij}$ represents the stress on the face with normal in the $j$-direction, acting in the $i$-direction.

In matrix form:

$$
\boldsymbol{\sigma} = \begin{pmatrix} \sigma_{xx} & \tau_{xy} & \tau_{xz} \\ \tau_{yx} & \sigma_{yy} & \tau_{yz} \\ \tau_{zx} & \tau_{zy} & \sigma_{zz} \end{pmatrix}
$$

### Definition 12.2.3 — Normal Stress and Shear Stress

For a surface with normal $\hat{\mathbf{n}}$:

- **Normal stress** $\sigma_n$: the component of $\mathbf{t}^{(\hat{\mathbf{n}})}$ parallel to $\hat{\mathbf{n}}$:

$$
\sigma_n = \mathbf{t}^{(\hat{\mathbf{n}})} \cdot \hat{\mathbf{n}} = \sigma_{ij} n_i n_j
$$

- **Shear stress** $\tau$: the component of $\mathbf{t}^{(\hat{\mathbf{n}})}$ tangent to the surface:

$$
\tau = |\mathbf{t}^{(\hat{\mathbf{n}})} - \sigma_n \hat{\mathbf{n}}| = \sqrt{|\mathbf{t}|^2 - \sigma_n^2}
$$

**Sign convention:** Positive normal stress = **tension** (pulling away from surface). Negative = **compression**.

### Definition 12.2.4 — Engineering Strain (1D)

For a bar of original length $L_0$ that deforms to length $L$:

$$
\varepsilon = \frac{\Delta L}{L_0} = \frac{L - L_0}{L_0}
$$

This is dimensionless. Positive strain = elongation; negative = contraction.

### Definition 12.2.5 — Displacement Field and Infinitesimal Strain Tensor

Let $\mathbf{u}(\mathbf{x})$ be the displacement field (how each point moves from its reference position). The **infinitesimal strain tensor** is:

$$
\varepsilon_{ij} = \frac{1}{2}\left(\frac{\partial u_i}{\partial x_j} + \frac{\partial u_j}{\partial x_i}\right)
$$

In matrix form:

$$
\boldsymbol{\varepsilon} = \begin{pmatrix} \varepsilon_{xx} & \varepsilon_{xy} & \varepsilon_{xz} \\ \varepsilon_{yx} & \varepsilon_{yy} & \varepsilon_{yz} \\ \varepsilon_{zx} & \varepsilon_{zy} & \varepsilon_{zz} \end{pmatrix}
$$

where:

$$
\varepsilon_{xx} = \frac{\partial u_x}{\partial x}, \quad \varepsilon_{yy} = \frac{\partial u_y}{\partial y}, \quad \varepsilon_{zz} = \frac{\partial u_z}{\partial z}
$$

$$
\varepsilon_{xy} = \frac{1}{2}\left(\frac{\partial u_x}{\partial y} + \frac{\partial u_y}{\partial x}\right) = \frac{\gamma_{xy}}{2}
$$

Here $\gamma_{xy}$ is the **engineering shear strain** (total angle change between originally perpendicular lines).

### Definition 12.2.6 — Volumetric Strain

The **volumetric strain** (dilatation) is the trace of the strain tensor:

$$
e = \varepsilon_{kk} = \varepsilon_{xx} + \varepsilon_{yy} + \varepsilon_{zz} = \frac{\Delta V}{V_0}
$$

### Definition 12.2.7 — Hydrostatic and Deviatoric Stress Decomposition

Any stress tensor can be decomposed as:

$$
\boldsymbol{\sigma} = \boldsymbol{\sigma}_{\text{hyd}} + \boldsymbol{\sigma}_{\text{dev}}
$$

**Hydrostatic (mean) stress:**

$$
\sigma_m = \frac{1}{3}\text{tr}(\boldsymbol{\sigma}) = \frac{\sigma_{xx} + \sigma_{yy} + \sigma_{zz}}{3}
$$

$$
\boldsymbol{\sigma}_{\text{hyd}} = \sigma_m \mathbf{I} = \begin{pmatrix} \sigma_m & 0 & 0 \\ 0 & \sigma_m & 0 \\ 0 & 0 & \sigma_m \end{pmatrix}
$$

**Deviatoric stress:**

$$
\boldsymbol{\sigma}_{\text{dev}} = \boldsymbol{\sigma} - \sigma_m \mathbf{I} = \begin{pmatrix} \sigma_{xx} - \sigma_m & \tau_{xy} & \tau_{xz} \\ \tau_{yx} & \sigma_{yy} - \sigma_m & \tau_{yz} \\ \tau_{zx} & \tau_{zy} & \sigma_{zz} - \sigma_m \end{pmatrix}
$$

The deviatoric stress drives **shape change** (distortion); the hydrostatic stress drives **volume change**.

### Definition 12.2.8 — Plane Stress

A state of **plane stress** exists when all stress components associated with one direction (say $z$) vanish:

$$
\sigma_{zz} = \tau_{xz} = \tau_{yz} = 0
$$

The stress tensor reduces to:

$$
\boldsymbol{\sigma} = \begin{pmatrix} \sigma_{xx} & \tau_{xy} \\ \tau_{xy} & \sigma_{yy} \end{pmatrix}
$$

This applies to thin plates loaded in their plane.




---

## 📐 2. Axioms / Postulates

### Postulate 12.2.P1 — Cauchy's Stress Principle

At every point in a loaded body and for every oriented surface through that point, there exists a traction vector $\mathbf{t}^{(\hat{\mathbf{n}})}$ that depends only on the position and the surface normal $\hat{\mathbf{n}}$. This traction is a linear function of $\hat{\mathbf{n}}$:

$$
\mathbf{t}^{(\hat{\mathbf{n}})} = \boldsymbol{\sigma} \cdot \hat{\mathbf{n}}
$$

### Postulate 12.2.P2 — Continuum Hypothesis

Matter is modeled as continuously distributed — no gaps, no discrete atoms at the scale of analysis. This allows the definition of stress and strain as point functions (fields).

### Postulate 12.2.P3 — Small Deformation Assumption

Deformations are small enough that:
1. The geometry of the deformed body is approximately the same as the undeformed body.
2. Higher-order terms in the strain-displacement relation are negligible.
3. Equilibrium can be written on the undeformed configuration.

### Postulate 12.2.P4 — Cauchy's Equations of Equilibrium

In the absence of acceleration (static equilibrium), the stress field must satisfy:

$$
\frac{\partial \sigma_{ij}}{\partial x_j} + b_i = 0
$$

where $b_i$ is the body force per unit volume (e.g., gravity: $b_y = -\rho g$).

In expanded form (3D):

$$
\frac{\partial \sigma_{xx}}{\partial x} + \frac{\partial \tau_{xy}}{\partial y} + \frac{\partial \tau_{xz}}{\partial z} + b_x = 0
$$

$$
\frac{\partial \tau_{yx}}{\partial x} + \frac{\partial \sigma_{yy}}{\partial y} + \frac{\partial \tau_{yz}}{\partial z} + b_y = 0
$$

$$
\frac{\partial \tau_{zx}}{\partial x} + \frac{\partial \tau_{zy}}{\partial y} + \frac{\partial \sigma_{zz}}{\partial z} + b_z = 0
$$

---

## 🛡️ 3. Lemmas

### Lemma 12.2.1 — Symmetry of the Stress Tensor

The Cauchy stress tensor is symmetric: $\sigma_{ij} = \sigma_{ji}$, i.e., $\tau_{xy} = \tau_{yx}$, $\tau_{xz} = \tau_{zx}$, $\tau_{yz} = \tau_{zy}$.

<details>
<summary>🔍 Proof from Moment Equilibrium</summary>

Consider an infinitesimal rectangular element of dimensions $dx \times dy \times dz$ centered at a point.

**Moment equilibrium about the $z$-axis** (through the center of the element):

Forces on the $x$-faces (normal in $\pm x$ direction) that contribute to $M_z$:
- Shear stress $\tau_{yx}$ acts in the $y$-direction on area $dy \cdot dz$, at moment arm $dx/2$.
- On the opposite face: $\tau_{yx}$ also acts at moment arm $dx/2$ (same direction due to sign convention on opposite faces).

Total moment from $\tau_{yx}$:

$$
M_z(\tau_{yx}) = \tau_{yx}(dy \cdot dz) \cdot \frac{dx}{2} + \tau_{yx}(dy \cdot dz) \cdot \frac{dx}{2} = \tau_{yx} \cdot dx\,dy\,dz
$$

Similarly, forces on the $y$-faces (normal in $\pm y$ direction):
- Shear stress $\tau_{xy}$ acts in the $x$-direction on area $dx \cdot dz$, at moment arm $dy/2$.

Total moment from $\tau_{xy}$ (opposite sense):

$$
M_z(\tau_{xy}) = -\tau_{xy}(dx \cdot dz) \cdot \frac{dy}{2} - \tau_{xy}(dx \cdot dz) \cdot \frac{dy}{2} = -\tau_{xy} \cdot dx\,dy\,dz
$$

Setting $\sum M_z = 0$ (no angular acceleration for infinitesimal element):

$$
\tau_{yx} \cdot dx\,dy\,dz - \tau_{xy} \cdot dx\,dy\,dz = 0
$$

$$
\tau_{yx} = \tau_{xy}
$$

By identical arguments about the $x$-axis and $y$-axis:

$$
\tau_{yz} = \tau_{zy}, \quad \tau_{xz} = \tau_{zx}
$$

Therefore $\sigma_{ij} = \sigma_{ji}$ — the stress tensor is symmetric. It has only **6 independent components** in 3D (not 9). $\blacksquare$

</details>

### Lemma 12.2.2 — Stress Transformation Under Coordinate Rotation

If we rotate the coordinate system by angle $\theta$ (2D case), the stress components in the new system $(x', y')$ are:

$$
\sigma_{x'x'} = \frac{\sigma_{xx} + \sigma_{yy}}{2} + \frac{\sigma_{xx} - \sigma_{yy}}{2}\cos 2\theta + \tau_{xy}\sin 2\theta
$$

$$
\sigma_{y'y'} = \frac{\sigma_{xx} + \sigma_{yy}}{2} - \frac{\sigma_{xx} - \sigma_{yy}}{2}\cos 2\theta - \tau_{xy}\sin 2\theta
$$

$$
\tau_{x'y'} = -\frac{\sigma_{xx} - \sigma_{yy}}{2}\sin 2\theta + \tau_{xy}\cos 2\theta
$$

<details>
<summary>🔍 Full Derivation from Tensor Transformation</summary>

The general tensor transformation rule for a second-order tensor under rotation $\mathbf{Q}$ is:

$$
\boldsymbol{\sigma}' = \mathbf{Q}\boldsymbol{\sigma}\mathbf{Q}^T
$$

For 2D rotation by angle $\theta$:

$$
\mathbf{Q} = \begin{pmatrix} \cos\theta & \sin\theta \\ -\sin\theta & \cos\theta \end{pmatrix}
$$

Compute $\boldsymbol{\sigma}' = \mathbf{Q}\boldsymbol{\sigma}\mathbf{Q}^T$:

**Step 1:** Compute $\mathbf{Q}\boldsymbol{\sigma}$:

$$
\mathbf{Q}\boldsymbol{\sigma} = \begin{pmatrix} \cos\theta & \sin\theta \\ -\sin\theta & \cos\theta \end{pmatrix} \begin{pmatrix} \sigma_{xx} & \tau_{xy} \\ \tau_{xy} & \sigma_{yy} \end{pmatrix}
$$

$$
= \begin{pmatrix} \sigma_{xx}\cos\theta + \tau_{xy}\sin\theta & \tau_{xy}\cos\theta + \sigma_{yy}\sin\theta \\ -\sigma_{xx}\sin\theta + \tau_{xy}\cos\theta & -\tau_{xy}\sin\theta + \sigma_{yy}\cos\theta \end{pmatrix}
$$

**Step 2:** Multiply by $\mathbf{Q}^T$:

$$
\mathbf{Q}^T = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}
$$

The $(1,1)$ entry of $\boldsymbol{\sigma}'$:

$$
\sigma_{x'x'} = (\sigma_{xx}\cos\theta + \tau_{xy}\sin\theta)\cos\theta + (\tau_{xy}\cos\theta + \sigma_{yy}\sin\theta)\sin\theta
$$

$$
= \sigma_{xx}\cos^2\theta + 2\tau_{xy}\sin\theta\cos\theta + \sigma_{yy}\sin^2\theta
$$

Using double-angle identities: $\cos^2\theta = \frac{1+\cos 2\theta}{2}$, $\sin^2\theta = \frac{1-\cos 2\theta}{2}$, $2\sin\theta\cos\theta = \sin 2\theta$:

$$
\sigma_{x'x'} = \sigma_{xx}\frac{1+\cos 2\theta}{2} + \sigma_{yy}\frac{1-\cos 2\theta}{2} + \tau_{xy}\sin 2\theta
$$

$$
= \frac{\sigma_{xx} + \sigma_{yy}}{2} + \frac{\sigma_{xx} - \sigma_{yy}}{2}\cos 2\theta + \tau_{xy}\sin 2\theta
$$

The $(1,2)$ entry:

$$
\tau_{x'y'} = (\sigma_{xx}\cos\theta + \tau_{xy}\sin\theta)(-\sin\theta) + (\tau_{xy}\cos\theta + \sigma_{yy}\sin\theta)\cos\theta
$$

$$
= -\sigma_{xx}\sin\theta\cos\theta + \tau_{xy}(\cos^2\theta - \sin^2\theta) + \sigma_{yy}\sin\theta\cos\theta
$$

$$
= -\frac{\sigma_{xx} - \sigma_{yy}}{2}\sin 2\theta + \tau_{xy}\cos 2\theta
$$

The $(2,2)$ entry follows by noting $\sigma_{x'x'} + \sigma_{y'y'} = \sigma_{xx} + \sigma_{yy}$ (trace is invariant):

$$
\sigma_{y'y'} = \frac{\sigma_{xx} + \sigma_{yy}}{2} - \frac{\sigma_{xx} - \sigma_{yy}}{2}\cos 2\theta - \tau_{xy}\sin 2\theta
$$

$\blacksquare$

</details>

### Lemma 12.2.3 — Strain-Displacement Relations (Derivation)

<details>
<summary>🔍 Derivation of the Infinitesimal Strain Tensor</summary>

Consider a line element $d\mathbf{x}$ in the reference configuration connecting points $P$ and $Q$. After deformation, $P$ moves to $P'$ by displacement $\mathbf{u}(P)$ and $Q$ moves to $Q'$ by displacement $\mathbf{u}(Q)$.

The deformed line element:

$$
d\mathbf{x}' = d\mathbf{x} + d\mathbf{u} = d\mathbf{x} + \frac{\partial \mathbf{u}}{\partial \mathbf{x}} d\mathbf{x} = (\mathbf{I} + \nabla\mathbf{u})d\mathbf{x}
$$

The **deformation gradient**:

$$
\mathbf{F} = \mathbf{I} + \nabla\mathbf{u}, \quad F_{ij} = \delta_{ij} + \frac{\partial u_i}{\partial x_j}
$$

The change in squared length:

$$
|d\mathbf{x}'|^2 - |d\mathbf{x}|^2 = d\mathbf{x}^T(\mathbf{F}^T\mathbf{F} - \mathbf{I})d\mathbf{x} = 2\,d\mathbf{x}^T \mathbf{E}\,d\mathbf{x}
$$

where $\mathbf{E} = \frac{1}{2}(\mathbf{F}^T\mathbf{F} - \mathbf{I})$ is the **Green-Lagrange strain tensor**.

Expanding:

$$
\mathbf{F}^T\mathbf{F} = (\mathbf{I} + \nabla\mathbf{u})^T(\mathbf{I} + \nabla\mathbf{u}) = \mathbf{I} + \nabla\mathbf{u} + (\nabla\mathbf{u})^T + (\nabla\mathbf{u})^T\nabla\mathbf{u}
$$

$$
\mathbf{E} = \frac{1}{2}\left[\nabla\mathbf{u} + (\nabla\mathbf{u})^T + (\nabla\mathbf{u})^T\nabla\mathbf{u}\right]
$$

For **small deformations** ($|\nabla\mathbf{u}| \ll 1$), the quadratic term is negligible:

$$
\boldsymbol{\varepsilon} \approx \frac{1}{2}\left[\nabla\mathbf{u} + (\nabla\mathbf{u})^T\right]
$$

$$
\varepsilon_{ij} = \frac{1}{2}\left(\frac{\partial u_i}{\partial x_j} + \frac{\partial u_j}{\partial x_i}\right)
$$

This is the **infinitesimal (engineering) strain tensor**. It is symmetric by construction. $\blacksquare$

</details>

### Lemma 12.2.4 — Compatibility Equations (2D)

The strain components cannot be chosen arbitrarily — they must be derivable from a continuous displacement field. The **Saint-Venant compatibility equation** (2D) is:

$$
\frac{\partial^2 \varepsilon_{xx}}{\partial y^2} + \frac{\partial^2 \varepsilon_{yy}}{\partial x^2} = 2\frac{\partial^2 \varepsilon_{xy}}{\partial x \partial y}
$$

<details>
<summary>🔍 Proof</summary>

From the strain-displacement relations:

$$
\varepsilon_{xx} = \frac{\partial u_x}{\partial x}, \quad \varepsilon_{yy} = \frac{\partial u_y}{\partial y}, \quad \varepsilon_{xy} = \frac{1}{2}\left(\frac{\partial u_x}{\partial y} + \frac{\partial u_y}{\partial x}\right)
$$

Compute:

$$
\frac{\partial^2 \varepsilon_{xx}}{\partial y^2} = \frac{\partial^3 u_x}{\partial x \partial y^2}
$$

$$
\frac{\partial^2 \varepsilon_{yy}}{\partial x^2} = \frac{\partial^3 u_y}{\partial y \partial x^2}
$$

$$
2\frac{\partial^2 \varepsilon_{xy}}{\partial x \partial y} = \frac{\partial^2}{\partial x \partial y}\left(\frac{\partial u_x}{\partial y} + \frac{\partial u_y}{\partial x}\right) = \frac{\partial^3 u_x}{\partial x \partial y^2} + \frac{\partial^3 u_y}{\partial y \partial x^2}
$$

Therefore:

$$
\frac{\partial^2 \varepsilon_{xx}}{\partial y^2} + \frac{\partial^2 \varepsilon_{yy}}{\partial x^2} = \frac{\partial^3 u_x}{\partial x \partial y^2} + \frac{\partial^3 u_y}{\partial y \partial x^2} = 2\frac{\partial^2 \varepsilon_{xy}}{\partial x \partial y}
$$

$\blacksquare$

</details>




---

## 👑 4. Theorems

### Theorem 12.2.1 — Cauchy's Theorem (Existence of the Stress Tensor)

At any point in a body in equilibrium, there exists a unique second-order tensor $\boldsymbol{\sigma}$ such that the traction on any surface with unit normal $\hat{\mathbf{n}}$ is given by:

$$
\mathbf{t}^{(\hat{\mathbf{n}})} = \boldsymbol{\sigma} \cdot \hat{\mathbf{n}} \quad \text{i.e.,} \quad t_i = \sigma_{ij} n_j
$$

### Theorem 12.2.2 — Principal Stresses as Eigenvalues

The **principal stresses** $\sigma_1, \sigma_2, \sigma_3$ are the eigenvalues of the stress tensor $\boldsymbol{\sigma}$. They satisfy:

$$
\det(\boldsymbol{\sigma} - \sigma \mathbf{I}) = 0
$$

which expands to the **characteristic equation**:

$$
\sigma^3 - I_1 \sigma^2 + I_2 \sigma - I_3 = 0
$$

where the **stress invariants** are:

$$
I_1 = \text{tr}(\boldsymbol{\sigma}) = \sigma_{xx} + \sigma_{yy} + \sigma_{zz}
$$

$$
I_2 = \frac{1}{2}\left[(\text{tr}\,\boldsymbol{\sigma})^2 - \text{tr}(\boldsymbol{\sigma}^2)\right] = \sigma_{xx}\sigma_{yy} + \sigma_{yy}\sigma_{zz} + \sigma_{zz}\sigma_{xx} - \tau_{xy}^2 - \tau_{yz}^2 - \tau_{zx}^2
$$

$$
I_3 = \det(\boldsymbol{\sigma})
$$

These invariants are unchanged under any rotation of coordinates (see [2.6 - Eigenvalues Eigenvectors & Diagonalization](2.6---Eigenvalues-Eigenvectors-&-Diagonalization)).

### Theorem 12.2.3 — Principal Directions Are Orthogonal

Since $\boldsymbol{\sigma}$ is real and symmetric, by the **Spectral Theorem** (Theorem 2.6.3):
1. All principal stresses are **real**.
2. Principal directions corresponding to distinct principal stresses are **mutually orthogonal**.
3. There exists an orthogonal rotation $\mathbf{Q}$ such that:

$$
\mathbf{Q}^T \boldsymbol{\sigma} \mathbf{Q} = \begin{pmatrix} \sigma_1 & 0 & 0 \\ 0 & \sigma_2 & 0 \\ 0 & 0 & \sigma_3 \end{pmatrix}
$$

On principal planes, **shear stress vanishes** — only normal stresses act.

### Theorem 12.2.4 — Maximum Shear Stress

The maximum shear stress at a point equals half the difference between the largest and smallest principal stresses:

$$
\tau_{\max} = \frac{\sigma_1 - \sigma_3}{2}
$$

(assuming $\sigma_1 \geq \sigma_2 \geq \sigma_3$). It acts on planes oriented at $45°$ to the $\sigma_1$ and $\sigma_3$ principal directions.

---

## ✍️ 5. Proofs / Derivations

### 5.1 Proof of Cauchy's Theorem (Tetrahedron Argument)

<details>
<summary>🔍 Full Proof</summary>

Consider an infinitesimal tetrahedron at point $P$ with three faces aligned with the coordinate planes and one oblique face with outward normal $\hat{\mathbf{n}} = n_x\hat{\mathbf{i}} + n_y\hat{\mathbf{j}} + n_z\hat{\mathbf{k}}$.

Let the oblique face have area $dA$. Then the areas of the coordinate faces are:
- Face ⊥ to $x$: $dA_x = n_x \, dA$
- Face ⊥ to $y$: $dA_y = n_y \, dA$
- Face ⊥ to $z$: $dA_z = n_z \, dA$

**Force balance on the tetrahedron** (body forces are $O(dV) = O(dA^{3/2})$ and vanish relative to surface forces as the tetrahedron shrinks):

$$
\mathbf{t}^{(\hat{\mathbf{n}})} dA - \mathbf{t}^{(\hat{\mathbf{i}})} dA_x - \mathbf{t}^{(\hat{\mathbf{j}})} dA_y - \mathbf{t}^{(\hat{\mathbf{k}})} dA_z = \mathbf{0}
$$

The negative signs arise because the coordinate faces have inward normals ($-\hat{\mathbf{i}}$, $-\hat{\mathbf{j}}$, $-\hat{\mathbf{k}}$) and $\mathbf{t}^{(-\hat{\mathbf{n}})} = -\mathbf{t}^{(\hat{\mathbf{n}})}$ (Newton's third law).

Substituting $dA_x = n_x\,dA$, etc., and dividing by $dA$:

$$
\mathbf{t}^{(\hat{\mathbf{n}})} = \mathbf{t}^{(\hat{\mathbf{i}})} n_x + \mathbf{t}^{(\hat{\mathbf{j}})} n_y + \mathbf{t}^{(\hat{\mathbf{k}})} n_z
$$

Define $\sigma_{ij}$ as the $i$-th component of the traction on the face with normal $\hat{\mathbf{e}}_j$:

$$
t_i^{(\hat{\mathbf{n}})} = \sigma_{i1} n_1 + \sigma_{i2} n_2 + \sigma_{i3} n_3 = \sigma_{ij} n_j
$$

This proves the existence of the stress tensor and the linear relation $\mathbf{t} = \boldsymbol{\sigma}\hat{\mathbf{n}}$. $\blacksquare$

</details>

### 5.2 Derivation: 2D Stress Transformation (Direct Equilibrium Approach)

<details>
<summary>🔍 Full Derivation</summary>

Consider a triangular element cut from a 2D stress element. The inclined face has outward normal at angle $\theta$ from the $x$-axis. Let the inclined face have area $dA$.

The areas of the other two faces:
- Vertical face (normal $= \hat{\mathbf{i}}$): $dA \cos\theta$
- Horizontal face (normal $= \hat{\mathbf{j}}$): $dA \sin\theta$

**Force equilibrium in the $x'$-direction** (normal to inclined face):

$$
\sigma_{x'} \cdot dA = \sigma_{xx}(dA\cos\theta)\cos\theta + \tau_{xy}(dA\cos\theta)\sin\theta + \sigma_{yy}(dA\sin\theta)\sin\theta + \tau_{xy}(dA\sin\theta)\cos\theta
$$

Dividing by $dA$:

$$
\sigma_{x'} = \sigma_{xx}\cos^2\theta + \sigma_{yy}\sin^2\theta + 2\tau_{xy}\sin\theta\cos\theta
$$

Using double-angle identities:

$$
\sigma_{x'} = \frac{\sigma_{xx} + \sigma_{yy}}{2} + \frac{\sigma_{xx} - \sigma_{yy}}{2}\cos 2\theta + \tau_{xy}\sin 2\theta
$$

**Force equilibrium in the $y'$-direction** (tangent to inclined face):

$$
\tau_{x'y'} \cdot dA = -\sigma_{xx}(dA\cos\theta)\sin\theta + \tau_{xy}(dA\cos\theta)\cos\theta + \sigma_{yy}(dA\sin\theta)\cos\theta - \tau_{xy}(dA\sin\theta)\sin\theta
$$

$$
\tau_{x'y'} = -(\sigma_{xx} - \sigma_{yy})\sin\theta\cos\theta + \tau_{xy}(\cos^2\theta - \sin^2\theta)
$$

$$
\tau_{x'y'} = -\frac{\sigma_{xx} - \sigma_{yy}}{2}\sin 2\theta + \tau_{xy}\cos 2\theta
$$

These are the **stress transformation equations** — the foundation of Mohr's Circle (Chapter 12.6). $\blacksquare$

</details>

### 5.3 Derivation: Principal Stresses in 2D

<details>
<summary>🔍 Full Derivation</summary>

Principal stresses occur where shear stress vanishes: $\tau_{x'y'} = 0$.

Setting the shear transformation equation to zero:

$$
-\frac{\sigma_{xx} - \sigma_{yy}}{2}\sin 2\theta_p + \tau_{xy}\cos 2\theta_p = 0
$$

$$
\tan 2\theta_p = \frac{2\tau_{xy}}{\sigma_{xx} - \sigma_{yy}}
$$

This gives two solutions $\theta_p$ separated by $90°$ (the two principal directions).

Substituting back into the normal stress equation, using:

$$
\cos 2\theta_p = \pm\frac{\sigma_{xx} - \sigma_{yy}}{2R}, \quad \sin 2\theta_p = \pm\frac{\tau_{xy}}{R}
$$

where $R = \sqrt{\left(\frac{\sigma_{xx} - \sigma_{yy}}{2}\right)^2 + \tau_{xy}^2}$:

$$
\sigma_{1,2} = \frac{\sigma_{xx} + \sigma_{yy}}{2} \pm \sqrt{\left(\frac{\sigma_{xx} - \sigma_{yy}}{2}\right)^2 + \tau_{xy}^2}
$$

This is the **principal stress formula** for plane stress. $\blacksquare$

</details>

### 5.4 Derivation: Equilibrium Equations from Force Balance on Infinitesimal Element

<details>
<summary>🔍 Full Derivation</summary>

Consider a 2D rectangular element of dimensions $dx \times dy$ with body force components $b_x$, $b_y$ (force per unit volume).

**Force balance in $x$-direction:**

On the right face ($x + dx$): $\left(\sigma_{xx} + \frac{\partial \sigma_{xx}}{\partial x}dx\right) dy$

On the left face ($x$): $-\sigma_{xx}\,dy$

On the top face ($y + dy$): $\left(\tau_{xy} + \frac{\partial \tau_{xy}}{\partial y}dy\right) dx$

On the bottom face ($y$): $-\tau_{xy}\,dx$

Body force: $b_x\,dx\,dy$

Sum = 0:

$$
\frac{\partial \sigma_{xx}}{\partial x}dx\,dy + \frac{\partial \tau_{xy}}{\partial y}dy\,dx + b_x\,dx\,dy = 0
$$

Dividing by $dx\,dy$:

$$
\frac{\partial \sigma_{xx}}{\partial x} + \frac{\partial \tau_{xy}}{\partial y} + b_x = 0
$$

Similarly for the $y$-direction:

$$
\frac{\partial \tau_{yx}}{\partial x} + \frac{\partial \sigma_{yy}}{\partial y} + b_y = 0
$$

These are **Cauchy's equilibrium equations** in 2D. $\blacksquare$

</details>




---

## 🧮 6. Worked Examples

### Example 12.2.1 — Traction Vector on an Inclined Plane

**Given:** At a point in a stressed body, the stress state is:

$$
\boldsymbol{\sigma} = \begin{pmatrix} 80 & 30 \\ 30 & -40 \end{pmatrix} \text{ MPa}
$$

A plane passes through this point with outward normal $\hat{\mathbf{n}} = \cos 60°\,\hat{\mathbf{i}} + \sin 60°\,\hat{\mathbf{j}} = (0.5, 0.866)$.

**Find:** The traction vector, normal stress, and shear stress on this plane.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Compute traction vector $\mathbf{t} = \boldsymbol{\sigma}\hat{\mathbf{n}}$.**

$$
\mathbf{t} = \begin{pmatrix} 80 & 30 \\ 30 & -40 \end{pmatrix}\begin{pmatrix} 0.5 \\ 0.866 \end{pmatrix} = \begin{pmatrix} 80(0.5) + 30(0.866) \\ 30(0.5) + (-40)(0.866) \end{pmatrix}
$$

$$
= \begin{pmatrix} 40 + 25.98 \\ 15 - 34.64 \end{pmatrix} = \begin{pmatrix} 65.98 \\ -19.64 \end{pmatrix} \text{ MPa}
$$

**Step 2: Normal stress $\sigma_n = \mathbf{t} \cdot \hat{\mathbf{n}}$.**

$$
\sigma_n = 65.98(0.5) + (-19.64)(0.866) = 32.99 - 17.01 = 15.98 \text{ MPa}
$$

**Step 3: Shear stress magnitude.**

$$
|\mathbf{t}|^2 = 65.98^2 + 19.64^2 = 4353.4 + 385.7 = 4739.1
$$

$$
\tau = \sqrt{|\mathbf{t}|^2 - \sigma_n^2} = \sqrt{4739.1 - 255.4} = \sqrt{4483.7} = 66.96 \text{ MPa}
$$

Wait — let me recheck. $\sigma_n^2 = 15.98^2 = 255.4$. $\tau = \sqrt{4739.1 - 255.4} = \sqrt{4483.7} = 66.96$ MPa.

**Verification using transformation equations** ($\theta = 60°$):

$$
\sigma_{x'} = \frac{80 + (-40)}{2} + \frac{80 - (-40)}{2}\cos 120° + 30\sin 120°
$$

$$
= 20 + 60(-0.5) + 30(0.866) = 20 - 30 + 25.98 = 15.98 \text{ MPa} \quad \checkmark
$$

</details>

---

### Example 12.2.2 — Computing Strain from a Displacement Field

**Given:** The displacement field in a 2D body is:

$$
u_x = (2x^2 + 3xy) \times 10^{-4}, \quad u_y = (x^2 - 4y^2) \times 10^{-4}
$$

**Find:** The strain components at point $(x, y) = (1, 2)$ m.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Compute partial derivatives.**

$$
\frac{\partial u_x}{\partial x} = (4x + 3y) \times 10^{-4}
$$

$$
\frac{\partial u_x}{\partial y} = 3x \times 10^{-4}
$$

$$
\frac{\partial u_y}{\partial x} = 2x \times 10^{-4}
$$

$$
\frac{\partial u_y}{\partial y} = -8y \times 10^{-4}
$$

**Step 2: Evaluate at $(1, 2)$.**

$$
\frac{\partial u_x}{\partial x}\bigg|_{(1,2)} = (4 + 6) \times 10^{-4} = 10 \times 10^{-4}
$$

$$
\frac{\partial u_x}{\partial y}\bigg|_{(1,2)} = 3 \times 10^{-4}
$$

$$
\frac{\partial u_y}{\partial x}\bigg|_{(1,2)} = 2 \times 10^{-4}
$$

$$
\frac{\partial u_y}{\partial y}\bigg|_{(1,2)} = -16 \times 10^{-4}
$$

**Step 3: Compute strain components.**

$$
\varepsilon_{xx} = \frac{\partial u_x}{\partial x} = 10 \times 10^{-4} = 1000 \,\mu\varepsilon
$$

$$
\varepsilon_{yy} = \frac{\partial u_y}{\partial y} = -16 \times 10^{-4} = -1600 \,\mu\varepsilon
$$

$$
\varepsilon_{xy} = \frac{1}{2}\left(\frac{\partial u_x}{\partial y} + \frac{\partial u_y}{\partial x}\right) = \frac{1}{2}(3 + 2) \times 10^{-4} = 2.5 \times 10^{-4} = 250 \,\mu\varepsilon
$$

**Engineering shear strain:** $\gamma_{xy} = 2\varepsilon_{xy} = 500 \,\mu\varepsilon$

**Strain tensor at $(1, 2)$:**

$$
\boldsymbol{\varepsilon} = \begin{pmatrix} 1000 & 250 \\ 250 & -1600 \end{pmatrix} \times 10^{-6}
$$

</details>

---

### Example 12.2.3 — Hydrostatic-Deviatoric Decomposition

**Given:** The stress state at a point is:

$$
\boldsymbol{\sigma} = \begin{pmatrix} 120 & -40 & 0 \\ -40 & 60 & 30 \\ 0 & 30 & -30 \end{pmatrix} \text{ MPa}
$$

**Find:** The hydrostatic stress, deviatoric stress tensor, and the three stress invariants.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Mean (hydrostatic) stress.**

$$
\sigma_m = \frac{1}{3}(\sigma_{xx} + \sigma_{yy} + \sigma_{zz}) = \frac{1}{3}(120 + 60 + (-30)) = \frac{150}{3} = 50 \text{ MPa}
$$

**Step 2: Hydrostatic stress tensor.**

$$
\boldsymbol{\sigma}_{\text{hyd}} = 50\mathbf{I} = \begin{pmatrix} 50 & 0 & 0 \\ 0 & 50 & 0 \\ 0 & 0 & 50 \end{pmatrix} \text{ MPa}
$$

**Step 3: Deviatoric stress tensor.**

$$
\boldsymbol{\sigma}_{\text{dev}} = \boldsymbol{\sigma} - \boldsymbol{\sigma}_{\text{hyd}} = \begin{pmatrix} 120-50 & -40 & 0 \\ -40 & 60-50 & 30 \\ 0 & 30 & -30-50 \end{pmatrix} = \begin{pmatrix} 70 & -40 & 0 \\ -40 & 10 & 30 \\ 0 & 30 & -80 \end{pmatrix} \text{ MPa}
$$

**Verification:** $\text{tr}(\boldsymbol{\sigma}_{\text{dev}}) = 70 + 10 + (-80) = 0$ ✓ (deviatoric tensor is always traceless).

**Step 4: Stress invariants.**

$$
I_1 = \text{tr}(\boldsymbol{\sigma}) = 120 + 60 + (-30) = 150 \text{ MPa}
$$

$$
I_2 = \sigma_{xx}\sigma_{yy} + \sigma_{yy}\sigma_{zz} + \sigma_{zz}\sigma_{xx} - \tau_{xy}^2 - \tau_{yz}^2 - \tau_{zx}^2
$$

$$
= (120)(60) + (60)(-30) + (-30)(120) - (-40)^2 - (30)^2 - 0^2
$$

$$
= 7200 - 1800 - 3600 - 1600 - 900 - 0 = -700 \text{ MPa}^2
$$

$$
I_3 = \det(\boldsymbol{\sigma})
$$

Expanding along the third row:

$$
I_3 = 0 \cdot M_{31} - 30 \cdot M_{32} + (-30) \cdot M_{33}
$$

$$
M_{32} = \det\begin{pmatrix} 120 & 0 \\ -40 & 30 \end{pmatrix} = 120(30) - 0(-40) = 3600
$$

$$
M_{33} = \det\begin{pmatrix} 120 & -40 \\ -40 & 60 \end{pmatrix} = 120(60) - (-40)(-40) = 7200 - 1600 = 5600
$$

$$
I_3 = 0 - 30(3600) + (-30)(5600) = -108000 - 168000 = -276000 \text{ MPa}^3
$$

Wait, let me recompute with proper cofactor signs. Using cofactor expansion along row 3:

$$
I_3 = 0 \cdot C_{31} + 30 \cdot C_{32} + (-30) \cdot C_{33}
$$

$C_{31} = (+1)\det\begin{pmatrix}-40 & 0 \\ 60 & 30\end{pmatrix} = -1200$

$C_{32} = (-1)\det\begin{pmatrix}120 & 0 \\ -40 & 30\end{pmatrix} = -(3600) = -3600$

$C_{33} = (+1)\det\begin{pmatrix}120 & -40 \\ -40 & 60\end{pmatrix} = 7200 - 1600 = 5600$

$$
I_3 = 0(-1200) + 30(-3600) + (-30)(5600) = 0 - 108000 - 168000 = -276000 \text{ MPa}^3
$$

**Results:**

$$
I_1 = 150 \text{ MPa}, \quad I_2 = -700 \text{ MPa}^2, \quad I_3 = -276{,}000 \text{ MPa}^3
$$

</details>

---

### Example 12.2.4 — Verifying Compatibility

**Given:** A proposed strain field:

$$
\varepsilon_{xx} = 3x^2 + 2y, \quad \varepsilon_{yy} = 2x + y^2, \quad \gamma_{xy} = 4xy + 6
$$

**Find:** Does this strain field satisfy the 2D compatibility equation?

<details>
<summary>🔍 View Step-by-Step Solution</summary>

The compatibility equation requires:

$$
\frac{\partial^2 \varepsilon_{xx}}{\partial y^2} + \frac{\partial^2 \varepsilon_{yy}}{\partial x^2} = 2\frac{\partial^2 \varepsilon_{xy}}{\partial x \partial y}
$$

Note: $\varepsilon_{xy} = \gamma_{xy}/2 = 2xy + 3$.

**Left side:**

$$
\frac{\partial^2 \varepsilon_{xx}}{\partial y^2} = \frac{\partial^2}{\partial y^2}(3x^2 + 2y) = \frac{\partial}{\partial y}(2) = 0
$$

$$
\frac{\partial^2 \varepsilon_{yy}}{\partial x^2} = \frac{\partial^2}{\partial x^2}(2x + y^2) = \frac{\partial}{\partial x}(2) = 0
$$

$$
\text{LHS} = 0 + 0 = 0
$$

**Right side:**

$$
\frac{\partial^2 \varepsilon_{xy}}{\partial x \partial y} = \frac{\partial^2}{\partial x \partial y}(2xy + 3) = \frac{\partial}{\partial x}(2x) = 2
$$

$$
\text{RHS} = 2(2) = 4
$$

**Conclusion:** $\text{LHS} = 0 \neq 4 = \text{RHS}$. The compatibility equation is **NOT satisfied**. This strain field cannot arise from a continuous displacement field — it is physically impossible.

</details>

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- **Previous:** [12.1 - Statics & Equilibrium](12.1---Statics-&-Equilibrium) — External forces that create internal stresses
- **Next:** [12.3 - Hooke's Law & Material Properties](12.3---Hooke's-Law-&-Material-Properties) — Constitutive relation linking stress to strain
- **Eigenvalue connection:** [2.6 - Eigenvalues Eigenvectors & Diagonalization](2.6---Eigenvalues-Eigenvectors-&-Diagonalization) — Principal stresses are eigenvalues of $\boldsymbol{\sigma}$
- **Tensor algebra:** [2.8 - SVD & Tensors](2.8---SVD-&-Tensors) — General tensor operations
- **Continuum mechanics:** [6.1 - Stress & Strain Tensors in Continua](6.1---Stress-&-Strain-Tensors-in-Continua) — Fluid mechanics analog

### External Resources
- 📖 **Hibbeler, R.C.** *Mechanics of Materials*, 10th ed. — Chapters 1–2, 9.
- 📖 **Timoshenko, S.P. & Goodier, J.N.** *Theory of Elasticity*, 3rd ed. — Chapters 1–3.
- 🎬 **MIT OCW 3.032** — [Mechanical Behavior of Materials](https://ocw.mit.edu/courses/3-032-mechanical-behavior-of-materials-fall-2007/) — Lectures 1–5.
- 🎬 **StructureFree** — [Stress Transformation Playlist](https://www.youtube.com/playlist?list=PL44E9FA04BCEE07C6)

---

*Next: [12.3 - Hooke's Law & Material Properties](12.3---Hooke's-Law-&-Material-Properties) →*



---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — 3D Stress Transformation via Rotation Matrix

**Given:** The stress tensor at a point is:

$$
\boldsymbol{\sigma} = \begin{pmatrix} 100 & 50 & 0 \\ 50 & -30 & 0 \\ 0 & 0 & 40 \end{pmatrix} \text{ MPa}
$$

A new coordinate system $x'y'z'$ is obtained by rotating $30°$ about the $z$-axis (i.e., $z' = z$).

**Find:** The full stress tensor in the rotated frame.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Rotation matrix for angle $\theta = 30°$ about $z$-axis.**

$$
\mathbf{Q} = \begin{pmatrix} \cos 30° & \sin 30° & 0 \\ -\sin 30° & \cos 30° & 0 \\ 0 & 0 & 1 \end{pmatrix} = \begin{pmatrix} 0.866 & 0.5 & 0 \\ -0.5 & 0.866 & 0 \\ 0 & 0 & 1 \end{pmatrix}
$$

**Step 2: Apply the tensor transformation $\boldsymbol{\sigma}' = \mathbf{Q}\boldsymbol{\sigma}\mathbf{Q}^T$.**

First compute $\boldsymbol{\sigma}\mathbf{Q}^T$:

$$
\boldsymbol{\sigma}\mathbf{Q}^T = \begin{pmatrix} 100 & 50 & 0 \\ 50 & -30 & 0 \\ 0 & 0 & 40 \end{pmatrix}\begin{pmatrix} 0.866 & -0.5 & 0 \\ 0.5 & 0.866 & 0 \\ 0 & 0 & 1 \end{pmatrix}
$$

Row 1: $(100(0.866)+50(0.5),\; 100(-0.5)+50(0.866),\; 0) = (111.6,\; -6.7,\; 0)$

Row 2: $(50(0.866)+(-30)(0.5),\; 50(-0.5)+(-30)(0.866),\; 0) = (28.3,\; -50.98,\; 0)$

Row 3: $(0,\; 0,\; 40)$

$$
\boldsymbol{\sigma}\mathbf{Q}^T = \begin{pmatrix} 111.6 & -6.7 & 0 \\ 28.3 & -50.98 & 0 \\ 0 & 0 & 40 \end{pmatrix}
$$

Now $\boldsymbol{\sigma}' = \mathbf{Q}(\boldsymbol{\sigma}\mathbf{Q}^T)$:

Row 1: $(0.866(111.6)+0.5(28.3),\; 0.866(-6.7)+0.5(-50.98),\; 0) = (96.65+14.15,\; -5.80-25.49,\; 0) = (110.8,\; -31.3,\; 0)$

Row 2: $(-0.5(111.6)+0.866(28.3),\; -0.5(-6.7)+0.866(-50.98),\; 0) = (-55.8+24.5,\; 3.35-44.15,\; 0) = (-31.3,\; -40.8,\; 0)$

Row 3: $(0,\; 0,\; 40)$

$$
\boldsymbol{\sigma}' = \begin{pmatrix} 110.8 & -31.3 & 0 \\ -31.3 & -40.8 & 0 \\ 0 & 0 & 40 \end{pmatrix} \text{ MPa}
$$

**Verification:** 

Trace invariance: $\text{tr}(\boldsymbol{\sigma}') = 110.8 + (-40.8) + 40 = 110.0$ vs. $\text{tr}(\boldsymbol{\sigma}) = 100 + (-30) + 40 = 110$. ✓

Check with 2D formula for $\sigma_{x'x'}$:

$$
\sigma_{x'} = \frac{100+(-30)}{2} + \frac{100-(-30)}{2}\cos 60° + 50\sin 60°
$$

$$
= 35 + 65(0.5) + 50(0.866) = 35 + 32.5 + 43.3 = 110.8 \text{ MPa} \quad \checkmark
$$

*Reference: Timoshenko & Goodier, Theory of Elasticity, §2.3.*

</details>


### Example 8.2 — Deviatoric vs. Hydrostatic Decomposition with Invariants

**Given:** A stress state at a point in a loaded component:

$$
\boldsymbol{\sigma} = \begin{pmatrix} 200 & -60 & 40 \\ -60 & 100 & 0 \\ 40 & 0 & -50 \end{pmatrix} \text{ MPa}
$$

**Find:** (a) Hydrostatic and deviatoric parts. (b) The second deviatoric invariant $J_2$. (c) The von Mises equivalent stress from $J_2$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Part (a): Decomposition.**

Mean stress:

$$
\sigma_m = \frac{1}{3}\text{tr}(\boldsymbol{\sigma}) = \frac{200 + 100 + (-50)}{3} = \frac{250}{3} = 83.33 \text{ MPa}
$$

Hydrostatic tensor:

$$
\boldsymbol{\sigma}_{\text{hyd}} = \sigma_m \mathbf{I} = \begin{pmatrix} 83.33 & 0 & 0 \\ 0 & 83.33 & 0 \\ 0 & 0 & 83.33 \end{pmatrix} \text{ MPa}
$$

Deviatoric tensor:

$$
\mathbf{s} = \boldsymbol{\sigma} - \boldsymbol{\sigma}_{\text{hyd}} = \begin{pmatrix} 116.67 & -60 & 40 \\ -60 & 16.67 & 0 \\ 40 & 0 & -133.33 \end{pmatrix} \text{ MPa}
$$

Check: $\text{tr}(\mathbf{s}) = 116.67 + 16.67 + (-133.33) = 0$ ✓

**Part (b): Second deviatoric invariant $J_2$.**

$$
J_2 = \frac{1}{2}s_{ij}s_{ij} = \frac{1}{2}\left(s_{11}^2 + s_{22}^2 + s_{33}^2 + 2s_{12}^2 + 2s_{23}^2 + 2s_{13}^2\right)
$$

$$
= \frac{1}{2}\left(116.67^2 + 16.67^2 + 133.33^2 + 2(60)^2 + 2(0)^2 + 2(40)^2\right)
$$

$$
= \frac{1}{2}\left(13611.9 + 277.9 + 17777.8 + 7200 + 0 + 3200\right)
$$

$$
= \frac{1}{2}(42067.6) = 21033.8 \text{ MPa}^2
$$

**Part (c): Von Mises equivalent stress.**

$$
\sigma_{\text{VM}} = \sqrt{3J_2} = \sqrt{3 \times 21033.8} = \sqrt{63101.4} = 251.2 \text{ MPa}
$$

**Alternative formula verification:**

$$
\sigma_{\text{VM}} = \sqrt{\frac{(\sigma_1-\sigma_2)^2 + (\sigma_2-\sigma_3)^2 + (\sigma_3-\sigma_1)^2}{2}}
$$

We would need principal stresses for this check (see Chapter 12.6), but the $J_2$ formula is computationally simpler when working directly with the stress tensor components.

*Reference: MIT OCW 3.032, Lecture 5; Chakrabarty, Theory of Plasticity, §1.4.*

</details>

### Example 8.3 — Compatibility Equations in 2D: Constructing a Valid Strain Field

**Given:** A proposed displacement field for a 2D body ($0 \leq x \leq 2$, $0 \leq y \leq 1$, units in meters):

$$
u(x,y) = (Ax^2y + Bxy^2) \times 10^{-3}
$$

$$
v(x,y) = (Cx^2y + Dy^3) \times 10^{-3}
$$

with constants $A = 2$, $B = 1$, $C = -1$, $D = 3$.

**Find:** (a) The strain field. (b) Verify the compatibility equation is satisfied. (c) Compute the rotation field.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Part (a): Strain components.**

$$
\varepsilon_{xx} = \frac{\partial u}{\partial x} = (2Axy + By^2) \times 10^{-3} = (4xy + y^2) \times 10^{-3}
$$

$$
\varepsilon_{yy} = \frac{\partial v}{\partial y} = (Cx^2 + 3Dy^2) \times 10^{-3} = (-x^2 + 9y^2) \times 10^{-3}
$$

$$
\gamma_{xy} = \frac{\partial u}{\partial y} + \frac{\partial v}{\partial x} = (Ax^2 + 2Bxy + 2Cxy) \times 10^{-3}
$$

$$
= (2x^2 + 2xy + (-2)xy) \times 10^{-3} = (2x^2) \times 10^{-3}
$$

Wait, let me recompute:

$$
\frac{\partial u}{\partial y} = (Ax^2 + 2Bxy) \times 10^{-3} = (2x^2 + 2xy) \times 10^{-3}
$$

$$
\frac{\partial v}{\partial x} = (2Cxy) \times 10^{-3} = (-2xy) \times 10^{-3}
$$

$$
\gamma_{xy} = (2x^2 + 2xy - 2xy) \times 10^{-3} = 2x^2 \times 10^{-3}
$$

So $\varepsilon_{xy} = \gamma_{xy}/2 = x^2 \times 10^{-3}$.

**Part (b): Compatibility check.**

The 2D compatibility equation (Saint-Venant):

$$
\frac{\partial^2 \varepsilon_{xx}}{\partial y^2} + \frac{\partial^2 \varepsilon_{yy}}{\partial x^2} = 2\frac{\partial^2 \varepsilon_{xy}}{\partial x \partial y}
$$

LHS:

$$
\frac{\partial^2 \varepsilon_{xx}}{\partial y^2} = \frac{\partial^2}{\partial y^2}(4xy + y^2) \times 10^{-3} = \frac{\partial}{\partial y}(4x + 2y) \times 10^{-3} = 2 \times 10^{-3}
$$

$$
\frac{\partial^2 \varepsilon_{yy}}{\partial x^2} = \frac{\partial^2}{\partial x^2}(-x^2 + 9y^2) \times 10^{-3} = -2 \times 10^{-3}
$$

$$
\text{LHS} = (2 - 2) \times 10^{-3} = 0
$$

RHS:

$$
2\frac{\partial^2 \varepsilon_{xy}}{\partial x \partial y} = 2\frac{\partial^2}{\partial x \partial y}(x^2) \times 10^{-3} = 2 \cdot 0 = 0
$$

$$
\text{LHS} = 0 = \text{RHS} \quad \checkmark
$$

The compatibility equation is satisfied, confirming this strain field can arise from a continuous displacement field (which we already know since we derived it from $u, v$).

**Part (c): Rotation field.**

$$
\omega_{xy} = \frac{1}{2}\left(\frac{\partial v}{\partial x} - \frac{\partial u}{\partial y}\right) = \frac{1}{2}(-2xy - 2x^2 - 2xy) \times 10^{-3}
$$

$$
= \frac{1}{2}(-2x^2 - 4xy) \times 10^{-3} = -(x^2 + 2xy) \times 10^{-3}
$$

At point $(1, 1)$: $\omega_{xy} = -(1 + 2) \times 10^{-3} = -3 \times 10^{-3}$ rad (clockwise rotation).

*Reference: Timoshenko & Goodier, Theory of Elasticity, §8 (Compatibility); Gere, Mechanics of Materials.*

</details>



---

## 📘 9. Appendix: Extended Derivations & Special Cases

### Appendix 9.1 — Proof of Cauchy Stress Tensor Symmetry ($\sigma_{ij} = \sigma_{ji}$)

**Claim:** In the absence of body couples (distributed moments), the stress tensor is symmetric.

**Proof:** Consider an infinitesimal rectangular element of dimensions $\Delta x \times \Delta y \times \Delta z$ centered at a point. Apply moment equilibrium about the $z$-axis through the center.

Forces on the faces:
- On the $+x$ face (area $\Delta y \Delta z$): shear stress $\tau_{xy}$ acts in the $+y$ direction. Force $= \tau_{xy}\Delta y\Delta z$, moment arm $= \Delta x/2$.
- On the $-x$ face: shear stress $\tau_{xy}$ acts in the $-y$ direction (by equilibrium of the face). Force $= \tau_{xy}\Delta y\Delta z$, moment arm $= \Delta x/2$. Same sense of moment.
- On the $+y$ face (area $\Delta x \Delta z$): shear stress $\tau_{yx}$ acts in the $+x$ direction. Force $= \tau_{yx}\Delta x\Delta z$, moment arm $= \Delta y/2$.
- On the $-y$ face: similarly contributes moment in the opposite sense.

Moment about $z$-axis (taking CCW positive):

$$
\sum M_z = \tau_{xy}(\Delta y\Delta z)\frac{\Delta x}{2} + \tau_{xy}(\Delta y\Delta z)\frac{\Delta x}{2} - \tau_{yx}(\Delta x\Delta z)\frac{\Delta y}{2} - \tau_{yx}(\Delta x\Delta z)\frac{\Delta y}{2}
$$

$$
= \tau_{xy}\Delta x\Delta y\Delta z - \tau_{yx}\Delta x\Delta y\Delta z
$$

Body forces and normal stresses pass through the center and contribute zero moment (or higher-order terms $\sim \Delta x^4$ that vanish as the element shrinks).

Setting $\sum M_z = 0$:

$$
(\tau_{xy} - \tau_{yx})\Delta x\Delta y\Delta z = 0
$$

Since the volume $\Delta x\Delta y\Delta z \neq 0$:

$$
\tau_{xy} = \tau_{yx}
$$

By identical arguments about the $x$ and $y$ axes:

$$
\tau_{yz} = \tau_{zy}, \quad \tau_{xz} = \tau_{zx}
$$

Therefore $\sigma_{ij} = \sigma_{ji}$ — the stress tensor is symmetric. $\blacksquare$

**Note:** This proof assumes no distributed body couples (moment per unit volume). In micropolar/Cosserat continua, body couples exist and the stress tensor can be asymmetric. For classical continuum mechanics, symmetry always holds.

**Consequence:** A symmetric $3 \times 3$ tensor has only **6 independent components** (not 9), which is why we write the stress state as $(\sigma_{xx}, \sigma_{yy}, \sigma_{zz}, \tau_{xy}, \tau_{yz}, \tau_{xz})$.

*Reference: Timoshenko & Goodier, Theory of Elasticity, §77; Malvern, Introduction to the Mechanics of a Continuous Medium, §4.3.*

### Appendix 9.2 — Saint-Venant's Principle

**Statement:** *If a system of forces acting on a small portion of the surface of an elastic body is replaced by a statically equivalent system (same resultant force and moment) acting on the same portion, then the stress field is significantly altered only in the immediate neighborhood of the loading, and at distances large compared to the loaded region, the stress fields are essentially identical.*

**Formal version (Toupin, 1965):** The difference in stress fields decays exponentially with distance from the loaded region:

$$
|\Delta\sigma_{ij}(d)| \leq C \cdot e^{-\alpha d/\ell}
$$

where $d$ is the distance from the loaded region, $\ell$ is the characteristic dimension of the loaded area, and $C, \alpha$ are constants depending on geometry.

**Practical implications:**

1. **Stress concentrations are local.** A bolt hole creates high stress only within $\sim 2$–$3$ diameters of the hole. Beyond that, the stress field is as if the hole were not there (for the same resultant load).

2. **End effects in beams.** The beam bending formula $\sigma = My/I$ is valid at cross-sections sufficiently far from the supports or load application points (typically $> 1$ beam depth away).

3. **Experimental validation.** Photoelastic experiments confirm that stress perturbations from concentrated loads decay within approximately one characteristic dimension.

**Limitations:**
- Does NOT apply to thin-walled structures (shells, plates) where the "characteristic dimension" is the thickness — perturbations can propagate much farther.
- Does NOT apply near cracks (stress singularities persist).
- Requires the replacement system to be **statically equivalent** (same $\mathbf{F}$ and $\mathbf{M}$).

**Example:** A column loaded by a concentrated force $P$ at the centroid vs. a uniform pressure $P/A$ over the cross-section. By Saint-Venant's principle, the stress field is identical beyond $\sim 1$–$2$ cross-section widths from the loaded end. Near the loaded end, the concentrated force creates much higher local stresses.

*Reference: Timoshenko & Goodier, Theory of Elasticity, §23; Barber, Elasticity, §3.1.*

### Appendix 9.3 — The Six Beltrami-Michell Compatibility Equations (3D)

In 3D elasticity, the strain compatibility conditions (ensuring a single-valued displacement field exists) combined with equilibrium and Hooke's law yield the **Beltrami-Michell equations** — six equations that the stress components must satisfy:

$$
\nabla^2 \sigma_{ij} + \frac{1}{1+\nu}\frac{\partial^2 (\sigma_{kk})}{\partial x_i \partial x_j} = -\frac{\nu}{1-\nu}\delta_{ij}\nabla^2(\sigma_{kk}) - \frac{\nu}{1-\nu}\delta_{ij}\frac{\partial F_k}{\partial x_k} - \left(\frac{\partial F_i}{\partial x_j} + \frac{\partial F_j}{\partial x_i}\right)
$$

For the case of **no body forces** ($\mathbf{F} = 0$), these simplify to:

$$
\nabla^2 \sigma_{ij} + \frac{1}{1+\nu}\frac{\partial^2 I_1}{\partial x_i \partial x_j} = 0
$$

where $I_1 = \sigma_{xx} + \sigma_{yy} + \sigma_{zz}$ is the first stress invariant.

**In 2D (plane stress, no body forces):** The compatibility reduces to the single **biharmonic equation**:

$$
\nabla^4 \phi = \frac{\partial^4 \phi}{\partial x^4} + 2\frac{\partial^4 \phi}{\partial x^2 \partial y^2} + \frac{\partial^4 \phi}{\partial y^4} = 0
$$

where $\phi(x,y)$ is the **Airy stress function** defined by:

$$
\sigma_{xx} = \frac{\partial^2 \phi}{\partial y^2}, \quad \sigma_{yy} = \frac{\partial^2 \phi}{\partial x^2}, \quad \tau_{xy} = -\frac{\partial^2 \phi}{\partial x \partial y}
$$

This automatically satisfies equilibrium, and the biharmonic condition ensures compatibility.

*Reference: Timoshenko & Goodier, Theory of Elasticity, §§26–30; Barber, Elasticity, Ch. 4.*
