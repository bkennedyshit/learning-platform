---
title: "3d Math Fundamentals"
subject: "VR & 3D Engineering"
catalog: advanced
audience_tier: higher-education
chapter: "28.1"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 28.1 — 3D Math Fundamentals

> *"The purpose of computing is insight, not numbers."* — Richard Hamming

Every pixel rendered on screen is the product of a chain of matrix multiplications that transform geometry from the artist's local coordinate frame through world space, camera space, and finally into the 2D image plane. This chapter builds the complete mathematical machinery of 3D transformations from first principles: homogeneous coordinates, Translation-Rotation-Scale (TRS) matrices, coordinate space hierarchies, and perspective projection. Mastery of these fundamentals is the prerequisite for everything that follows in this track.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Represent 3D points and directions in **homogeneous coordinates** and explain why the fourth component $w$ distinguishes them.
2. Construct **Translation**, **Rotation**, and **Scale** matrices in 4×4 form and compose them in correct order.
3. Derive the **rotation matrices** $R_x(\theta)$, $R_y(\theta)$, $R_z(\theta)$ from first principles using trigonometric identities.
4. Transform geometry through the full coordinate-space pipeline: **Object → World → View → Clip → NDC → Screen**.
5. Derive the **perspective projection matrix** from similar triangles and the view frustum parameters.
6. Compute the **orthographic projection matrix** and contrast it with perspective.
7. Apply **inverse transformations** to convert between coordinate spaces bidirectionally.
8. Implement all transformations in Python+NumPy and verify against engine implementations.

---

## 🖼️ Visual Anchor — The Coordinate Space Pipeline

![track-09__9.1-fig1](track-09__9.1-fig1.svg)

---

## 📚 1. Definitions

### Definition 28.1.1 — Homogeneous Coordinates

A point $\mathbf{p} = (x, y, z)$ in 3D Euclidean space is represented in **homogeneous coordinates** as the 4-vector:

$$
\tilde{\mathbf{p}} = \begin{pmatrix} x \\ y \\ z \\ 1 \end{pmatrix}
$$

A direction vector $\mathbf{d} = (d_x, d_y, d_z)$ is represented with $w = 0$:

$$
\tilde{\mathbf{d}} = \begin{pmatrix} d_x \\ d_y \\ d_z \\ 0 \end{pmatrix}
$$

The distinction is critical: translations affect points ($w=1$) but not directions ($w=0$). Any homogeneous vector with $w \neq 0$ maps back to Euclidean space via $\mathbf{p} = (x/w,\; y/w,\; z/w)$.

### Definition 28.1.2 — Translation Matrix

The 4×4 **translation matrix** that displaces a point by $(t_x, t_y, t_z)$:

$$
T(t_x, t_y, t_z) = \begin{pmatrix} 1 & 0 & 0 & t_x \\ 0 & 1 & 0 & t_y \\ 0 & 0 & 1 & t_z \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

Verification: $T \tilde{\mathbf{p}} = (x + t_x,\; y + t_y,\; z + t_z,\; 1)^T$. For a direction vector: $T \tilde{\mathbf{d}} = (d_x,\; d_y,\; d_z,\; 0)^T$ — unchanged, as required.

### Definition 28.1.3 — Uniform and Non-Uniform Scale Matrices

The **scale matrix** with factors $(s_x, s_y, s_z)$:

$$
S(s_x, s_y, s_z) = \begin{pmatrix} s_x & 0 & 0 & 0 \\ 0 & s_y & 0 & 0 \\ 0 & 0 & s_z & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

When $s_x = s_y = s_z = s$, this is **uniform scaling**. When the factors differ, it is **non-uniform scaling** (which distorts angles and can break normal vectors — see Definition 28.1.8).

### Definition 28.1.4 — Rotation Matrices About Principal Axes

Rotation by angle $\theta$ about the $x$-axis (right-hand rule):

$$
R_x(\theta) = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & \cos\theta & -\sin\theta & 0 \\ 0 & \sin\theta & \cos\theta & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

Rotation by angle $\theta$ about the $y$-axis:

$$
R_y(\theta) = \begin{pmatrix} \cos\theta & 0 & \sin\theta & 0 \\ 0 & 1 & 0 & 0 \\ -\sin\theta & 0 & \cos\theta & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

Rotation by angle $\theta$ about the $z$-axis:

$$
R_z(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta & 0 & 0 \\ \sin\theta & \cos\theta & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

Note: $R_y$ has the sine terms "flipped" relative to $R_x$ and $R_z$. This arises because the cyclic ordering $(x \to y \to z \to x)$ means the $y$-axis rotation permutes $(z, x)$ rather than $(x, y)$.

### Definition 28.1.5 — The TRS Composition (Model Matrix)

The **model matrix** $M$ that places an object in world space is composed as:

$$
M = T \cdot R \cdot S
$$

Order matters: scale first (in object space), then rotate, then translate. In column-major convention (OpenGL), the rightmost matrix is applied first to the vertex:

$$
\mathbf{v}_{\text{world}} = T \cdot R \cdot S \cdot \mathbf{v}_{\text{local}}
$$

### Definition 28.1.6 — View (Camera) Matrix

The **view matrix** $V$ transforms world-space coordinates into camera-space coordinates. Given camera position $\mathbf{e}$, forward direction $\hat{\mathbf{f}}$, up direction $\hat{\mathbf{u}}$, and right direction $\hat{\mathbf{r}} = \hat{\mathbf{f}} \times \hat{\mathbf{u}}$:

$$
V = \begin{pmatrix} r_x & r_y & r_z & -\mathbf{r} \cdot \mathbf{e} \\ u_x & u_y & u_z & -\mathbf{u} \cdot \mathbf{e} \\ -f_x & -f_y & -f_z & \mathbf{f} \cdot \mathbf{e} \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

This is the inverse of the camera's own model matrix: $V = M_{\text{camera}}^{-1}$. The negation of $\hat{\mathbf{f}}$ in row 3 reflects the convention that the camera looks down $-z$ in view space (OpenGL convention).

### Definition 28.1.7 — Perspective Projection Matrix

For a symmetric frustum with vertical field-of-view $\text{fov}_y$, aspect ratio $a = w/h$, near plane $n$, and far plane $f$:

$$
P_{\text{persp}} = \begin{pmatrix} \frac{1}{a \tan(\text{fov}_y/2)} & 0 & 0 & 0 \\ 0 & \frac{1}{\tan(\text{fov}_y/2)} & 0 & 0 \\ 0 & 0 & \frac{-(f+n)}{f-n} & \frac{-2fn}{f-n} \\ 0 & 0 & -1 & 0 \end{pmatrix}
$$

After multiplication, the resulting $w$-component equals $-z_{\text{view}}$, enabling the perspective divide that produces foreshortening.

### Definition 28.1.8 — Normal Matrix (Inverse-Transpose)

When a model matrix $M$ contains non-uniform scaling, surface normals must be transformed by the **normal matrix**:

$$
N = (M^{-1})^T = (M^T)^{-1}
$$

This ensures normals remain perpendicular to the surface after transformation. If $M$ is orthogonal (pure rotation), then $N = M$ since $(R^{-1})^T = (R^T)^T = R$.

### Definition 28.1.9 — Orthographic Projection Matrix

For an orthographic view volume with bounds $[l, r] \times [b, t] \times [n, f]$:

$$
P_{\text{ortho}} = \begin{pmatrix} \frac{2}{r-l} & 0 & 0 & -\frac{r+l}{r-l} \\ 0 & \frac{2}{t-b} & 0 & -\frac{t+b}{t-b} \\ 0 & 0 & \frac{-2}{f-n} & -\frac{f+n}{f-n} \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

Unlike perspective projection, $w$ remains 1 — there is no foreshortening. Parallel lines remain parallel.



---

## 📐 2. Axioms / Postulates

### Axiom 28.1.A1 — Right-Hand Rule Convention

We adopt the **right-handed coordinate system** throughout this track (matching OpenGL, Blender, and glTF conventions):
- $\hat{\mathbf{x}} \times \hat{\mathbf{y}} = \hat{\mathbf{z}}$
- Positive rotation about an axis follows the right-hand curl rule.

Note: Unity uses a left-handed system ($\hat{\mathbf{x}} \times \hat{\mathbf{y}} = -\hat{\mathbf{z}}$); Unreal uses left-handed with $Z$-up. Conversion between handedness requires negating one axis or flipping winding order.

### Axiom 28.1.A2 — Column-Major Matrix Convention

Vectors are **column vectors**. Transformation matrices multiply on the left:

$$
\mathbf{v}' = M \cdot \mathbf{v}
$$

Composition reads right-to-left: $M_3 \cdot M_2 \cdot M_1 \cdot \mathbf{v}$ applies $M_1$ first, then $M_2$, then $M_3$. This matches OpenGL, GLSL, and most mathematical literature. DirectX/HLSL uses row-major (row vectors, multiply on the right) — the matrices are transposed.

### Axiom 28.1.A3 — Affine Transformations Preserve Collinearity

All transformations in the TRS pipeline are **affine**: they map lines to lines, planes to planes, and preserve parallelism (though not necessarily distances or angles). The 4×4 homogeneous matrix with bottom row $(0, 0, 0, 1)$ encodes exactly the affine group.

### Axiom 28.1.A4 — Projective Transformations Preserve Incidence

The perspective projection matrix is a **projective** (not affine) transformation. It maps lines to lines but does not preserve parallelism — parallel lines converge at vanishing points. The bottom row $(0, 0, -1, 0)$ causes $w$ to vary, enabling the perspective divide.

---

## 🛡️ 3. Lemmas

### Lemma 28.1.1 — Inverse of a Translation Matrix

$$
T(t_x, t_y, t_z)^{-1} = T(-t_x, -t_y, -t_z)
$$

**Proof.** Compute the product directly:

$$
T(\mathbf{t}) \cdot T(-\mathbf{t}) = \begin{pmatrix} 1 & 0 & 0 & t_x \\ 0 & 1 & 0 & t_y \\ 0 & 0 & 1 & t_z \\ 0 & 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} 1 & 0 & 0 & -t_x \\ 0 & 1 & 0 & -t_y \\ 0 & 0 & 1 & -t_z \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

The upper-left 3×3 block is $I \cdot I = I$. The translation column becomes:

$$
\begin{pmatrix} t_x + 1 \cdot (-t_x) \\ t_y + 1 \cdot (-t_y) \\ t_z + 1 \cdot (-t_z) \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \\ 0 \end{pmatrix}
$$

Therefore $T(\mathbf{t}) \cdot T(-\mathbf{t}) = I_4$. $\blacksquare$

### Lemma 28.1.2 — Inverse of a Scale Matrix

For $s_x, s_y, s_z \neq 0$:

$$
S(s_x, s_y, s_z)^{-1} = S\left(\frac{1}{s_x}, \frac{1}{s_y}, \frac{1}{s_z}\right)
$$

**Proof.** $S$ is diagonal. The product of two diagonal matrices is diagonal with entries being the products of corresponding diagonal entries:

$$
s_x \cdot \frac{1}{s_x} = 1, \quad s_y \cdot \frac{1}{s_y} = 1, \quad s_z \cdot \frac{1}{s_z} = 1, \quad 1 \cdot 1 = 1
$$

Hence $S \cdot S^{-1} = I_4$. $\blacksquare$

### Lemma 28.1.3 — Rotation Matrices Are Orthogonal

For any rotation matrix $R$:

$$
R^T R = I, \quad \det(R) = +1, \quad R^{-1} = R^T
$$

**Proof.** Consider $R_z(\theta)$. The columns are:

$$
\mathbf{c}_1 = (\cos\theta, \sin\theta, 0, 0)^T, \quad \mathbf{c}_2 = (-\sin\theta, \cos\theta, 0, 0)^T, \quad \mathbf{c}_3 = (0,0,1,0)^T, \quad \mathbf{c}_4 = (0,0,0,1)^T
$$

Check orthonormality:

$$
\mathbf{c}_1 \cdot \mathbf{c}_1 = \cos^2\theta + \sin^2\theta = 1
$$

$$
\mathbf{c}_2 \cdot \mathbf{c}_2 = \sin^2\theta + \cos^2\theta = 1
$$

$$
\mathbf{c}_1 \cdot \mathbf{c}_2 = \cos\theta(-\sin\theta) + \sin\theta(\cos\theta) = -\cos\theta\sin\theta + \sin\theta\cos\theta = 0
$$

All other dot products between distinct columns are zero by inspection (one column has non-zero entries only in positions where the other has zeros). Therefore $R_z^T R_z = I$.

For the determinant: $\det(R_z) = \cos^2\theta + \sin^2\theta = 1$ (expanding the 2×2 block). The same argument applies to $R_x$ and $R_y$ by symmetry. $\blacksquare$

### Lemma 28.1.4 — Inverse of a TRS Composition

Given $M = T \cdot R \cdot S$, the inverse is:

$$
M^{-1} = S^{-1} \cdot R^{-1} \cdot T^{-1} = S^{-1} \cdot R^T \cdot T(-\mathbf{t})
$$

**Proof.** By the "socks and shoes" property of matrix inverses (see [2.3 - Matrix Operations & Inverses](2.3---Matrix-Operations-&-Inverses)):

$$
(ABC)^{-1} = C^{-1} B^{-1} A^{-1}
$$

Applying this with $A = T$, $B = R$, $C = S$:

$$
M^{-1} = S^{-1} \cdot R^{-1} \cdot T^{-1}
$$

Substituting the results from Lemmas 9.1.1–9.1.3:

$$
M^{-1} = S(1/s_x, 1/s_y, 1/s_z) \cdot R^T \cdot T(-t_x, -t_y, -t_z)
$$

$\blacksquare$

### Lemma 28.1.5 — The Normal Matrix Preserves Perpendicularity

If $\mathbf{n}$ is a surface normal and $\mathbf{t}$ is a tangent vector at the same point, then after transformation by $M$ (for tangents) and $N = (M^{-1})^T$ (for normals), the transformed vectors remain perpendicular.

**Proof.** We require $\mathbf{n}'^T \mathbf{t}' = 0$ where $\mathbf{t}' = M\mathbf{t}$ and $\mathbf{n}' = N\mathbf{n}$.

$$
\mathbf{n}'^T \mathbf{t}' = (N\mathbf{n})^T (M\mathbf{t}) = \mathbf{n}^T N^T M \mathbf{t}
$$

Substituting $N = (M^{-1})^T$:

$$
N^T = ((M^{-1})^T)^T = M^{-1}
$$

Therefore:

$$
\mathbf{n}^T N^T M \mathbf{t} = \mathbf{n}^T M^{-1} M \mathbf{t} = \mathbf{n}^T I \mathbf{t} = \mathbf{n}^T \mathbf{t} = 0
$$

The last equality holds because $\mathbf{n} \perp \mathbf{t}$ in the original space. $\blacksquare$



---

## 👑 4. Theorems

### Theorem 28.1.1 — Perspective Projection from Similar Triangles

Given a point $(x, y, z)$ in view space (camera at origin, looking down $-z$), its projection onto the near plane at distance $n$ is:

$$
x_{\text{proj}} = \frac{n \cdot x}{-z}, \quad y_{\text{proj}} = \frac{n \cdot y}{-z}
$$

This is the mathematical basis of perspective foreshortening: objects farther from the camera ($|z|$ larger) project to smaller screen coordinates.

### Theorem 28.1.2 — Depth Non-Linearity in Perspective

The perspective projection matrix maps $z_{\text{view}}$ to $z_{\text{ndc}}$ via:

$$
z_{\text{ndc}} = \frac{-(f+n)z_{\text{view}} - 2fn}{(f-n)(-z_{\text{view}})} = \frac{f+n}{f-n} + \frac{2fn}{(f-n) \cdot z_{\text{view}}}
$$

This mapping is **non-linear** (hyperbolic in $z_{\text{view}}$). Depth precision is concentrated near the near plane and becomes sparse near the far plane. This causes **z-fighting** for distant geometry.

### Theorem 28.1.3 — Composition of Rotations Is a Rotation (Euler's Rotation Theorem)

Any composition of rotations about axes through a common fixed point is equivalent to a single rotation about some axis through that point. Formally: the set of 3×3 rotation matrices forms the **Special Orthogonal Group** $SO(3)$, which is closed under multiplication.

### Theorem 28.1.4 — Rodrigues' Rotation Formula

Rotation of vector $\mathbf{v}$ by angle $\theta$ about unit axis $\hat{\mathbf{k}}$:

$$
\mathbf{v}' = \mathbf{v}\cos\theta + (\hat{\mathbf{k}} \times \mathbf{v})\sin\theta + \hat{\mathbf{k}}(\hat{\mathbf{k}} \cdot \mathbf{v})(1 - \cos\theta)
$$

### Theorem 28.1.5 — The View Matrix Is the Inverse Camera Transform

If the camera has world-space position $\mathbf{e}$ and orientation given by orthonormal basis $\{\hat{\mathbf{r}}, \hat{\mathbf{u}}, -\hat{\mathbf{f}}\}$, then:

$$
V = \begin{pmatrix} R_{\text{cam}}^T & -R_{\text{cam}}^T \mathbf{e} \\ \mathbf{0}^T & 1 \end{pmatrix} = (T(\mathbf{e}) \cdot R_{\text{cam}})^{-1}
$$

---

## ✍️ 5. Proofs / Derivations

### 5.1 Derivation of the Perspective Projection Matrix

**Goal:** Derive Definition 28.1.7 from first principles.

**Step 1: Similar triangles for $x$ and $y$.**

Consider a point $P = (x, y, z)$ in view space where the camera is at the origin looking down $-z$. The near plane is at $z = -n$. By similar triangles between the camera-to-point ray and the near plane:

$$
\frac{x_{\text{proj}}}{n} = \frac{x}{-z} \implies x_{\text{proj}} = \frac{n \cdot x}{-z}
$$

$$
\frac{y_{\text{proj}}}{n} = \frac{y}{-z} \implies y_{\text{proj}} = \frac{n \cdot y}{-z}
$$

**Step 2: Encode the division by $-z$ in the $w$ component.**

We want a matrix $P$ such that after the perspective divide ($\div w$), we recover the projected coordinates. Set the fourth row of $P$ to $(0, 0, -1, 0)$ so that:

$$
w_{\text{clip}} = -z_{\text{view}}
$$

Then after dividing by $w$:

$$
x_{\text{ndc}} = \frac{x_{\text{clip}}}{w_{\text{clip}}} = \frac{x_{\text{clip}}}{-z}
$$

**Step 3: Map $x_{\text{proj}}$ to $[-1, 1]$ (NDC).**

The near plane spans $x \in [-n \tan(\text{fov}_x/2),\; n \tan(\text{fov}_x/2)]$. To map to $[-1, 1]$:

$$
x_{\text{ndc}} = \frac{x_{\text{proj}}}{n \tan(\text{fov}_x/2)} = \frac{x}{-z \cdot \tan(\text{fov}_x/2)}
$$

Since $\text{fov}_x = 2\arctan(a \cdot \tan(\text{fov}_y/2))$ where $a$ is the aspect ratio:

$$
x_{\text{ndc}} = \frac{x}{-z \cdot a \cdot \tan(\text{fov}_y/2)}
$$

For this to equal $x_{\text{clip}} / w_{\text{clip}} = x_{\text{clip}} / (-z)$, we need:

$$
x_{\text{clip}} = \frac{x}{a \cdot \tan(\text{fov}_y/2)}
$$

So the $(1,1)$ entry of $P$ is $\frac{1}{a \cdot \tan(\text{fov}_y/2)}$.

**Step 4: Similarly for $y$:**

$$
y_{\text{ndc}} = \frac{y}{-z \cdot \tan(\text{fov}_y/2)} \implies y_{\text{clip}} = \frac{y}{\tan(\text{fov}_y/2)}
$$

So the $(2,2)$ entry is $\frac{1}{\tan(\text{fov}_y/2)}$.

**Step 5: Map $z$ to $[-1, 1]$ (depth).**

We need a mapping $z_{\text{view}} \in [-n, -f] \mapsto z_{\text{ndc}} \in [-1, 1]$. After the perspective divide:

$$
z_{\text{ndc}} = \frac{z_{\text{clip}}}{w_{\text{clip}}} = \frac{Az + B}{-z}
$$

where $A$ and $B$ are the $(3,3)$ and $(3,4)$ entries of $P$. Apply boundary conditions:

At $z = -n$: $z_{\text{ndc}} = -1$:

$$
\frac{A(-n) + B}{-(-n)} = -1 \implies \frac{-An + B}{n} = -1 \implies -An + B = -n \tag{i}
$$

At $z = -f$: $z_{\text{ndc}} = 1$:

$$
\frac{A(-f) + B}{-(-f)} = 1 \implies \frac{-Af + B}{f} = 1 \implies -Af + B = f \tag{ii}
$$

**Step 6: Solve the system.**

Subtract (i) from (ii):

$$
-Af + B - (-An + B) = f - (-n)
$$

$$
-Af + An = f + n
$$

$$
A(n - f) = f + n
$$

$$
A = \frac{-(f + n)}{f - n}
$$

Substitute back into (i):

$$
-\frac{-(f+n)}{f-n} \cdot n + B = -n
$$

$$
\frac{n(f+n)}{f-n} + B = -n
$$

$$
B = -n - \frac{n(f+n)}{f-n} = \frac{-n(f-n) - n(f+n)}{f-n} = \frac{-nf + n^2 - nf - n^2}{f-n} = \frac{-2nf}{f-n}
$$

**Step 7: Assemble the matrix.**

$$
P_{\text{persp}} = \begin{pmatrix} \frac{1}{a\tan(\text{fov}_y/2)} & 0 & 0 & 0 \\ 0 & \frac{1}{\tan(\text{fov}_y/2)} & 0 & 0 \\ 0 & 0 & \frac{-(f+n)}{f-n} & \frac{-2fn}{f-n} \\ 0 & 0 & -1 & 0 \end{pmatrix}
$$

$\blacksquare$

### 5.2 Derivation of Rodrigues' Rotation Formula

**Goal:** Derive Theorem 28.1.4.

**Setup:** Rotate vector $\mathbf{v}$ by angle $\theta$ about unit axis $\hat{\mathbf{k}}$.

**Step 1: Decompose $\mathbf{v}$ into parallel and perpendicular components.**

$$
\mathbf{v}_\parallel = (\hat{\mathbf{k}} \cdot \mathbf{v})\hat{\mathbf{k}}
$$

$$
\mathbf{v}_\perp = \mathbf{v} - \mathbf{v}_\parallel = \mathbf{v} - (\hat{\mathbf{k}} \cdot \mathbf{v})\hat{\mathbf{k}}
$$

**Step 2: The parallel component is unchanged by rotation about $\hat{\mathbf{k}}$:**

$$
\mathbf{v}'_\parallel = \mathbf{v}_\parallel
$$

**Step 3: Construct an orthonormal basis in the plane perpendicular to $\hat{\mathbf{k}}$.**

Let $\mathbf{w} = \hat{\mathbf{k}} \times \mathbf{v}$. Note that $|\mathbf{w}| = |\hat{\mathbf{k}}||\mathbf{v}|\sin\alpha = |\mathbf{v}_\perp|$ where $\alpha$ is the angle between $\hat{\mathbf{k}}$ and $\mathbf{v}$.

The vectors $\mathbf{v}_\perp$ and $\mathbf{w}$ are orthogonal and have the same magnitude $|\mathbf{v}_\perp|$. They form a 2D basis in the rotation plane.

**Step 4: Rotate $\mathbf{v}_\perp$ by $\theta$ in the plane:**

$$
\mathbf{v}'_\perp = \mathbf{v}_\perp \cos\theta + \mathbf{w} \sin\theta
$$

$$
= (\mathbf{v} - (\hat{\mathbf{k}} \cdot \mathbf{v})\hat{\mathbf{k}})\cos\theta + (\hat{\mathbf{k}} \times \mathbf{v})\sin\theta
$$

**Step 5: Combine parallel and perpendicular:**

$$
\mathbf{v}' = \mathbf{v}'_\parallel + \mathbf{v}'_\perp
$$

$$
= (\hat{\mathbf{k}} \cdot \mathbf{v})\hat{\mathbf{k}} + (\mathbf{v} - (\hat{\mathbf{k}} \cdot \mathbf{v})\hat{\mathbf{k}})\cos\theta + (\hat{\mathbf{k}} \times \mathbf{v})\sin\theta
$$

$$
= (\hat{\mathbf{k}} \cdot \mathbf{v})\hat{\mathbf{k}}(1 - \cos\theta) + \mathbf{v}\cos\theta + (\hat{\mathbf{k}} \times \mathbf{v})\sin\theta
$$

Rearranging:

$$
\mathbf{v}' = \mathbf{v}\cos\theta + (\hat{\mathbf{k}} \times \mathbf{v})\sin\theta + \hat{\mathbf{k}}(\hat{\mathbf{k}} \cdot \mathbf{v})(1 - \cos\theta)
$$

$\blacksquare$

### 5.3 Derivation of the View Matrix (LookAt)

**Goal:** Derive Definition 28.1.6.

**Given:** Camera at position $\mathbf{e}$, looking at target $\mathbf{t}$, with world-up hint $\hat{\mathbf{u}}_{\text{world}}$.

**Step 1: Compute the camera's local axes.**

Forward (into the screen in OpenGL):

$$
\hat{\mathbf{f}} = \frac{\mathbf{t} - \mathbf{e}}{|\mathbf{t} - \mathbf{e}|}
$$

Right:

$$
\hat{\mathbf{r}} = \frac{\hat{\mathbf{f}} \times \hat{\mathbf{u}}_{\text{world}}}{|\hat{\mathbf{f}} \times \hat{\mathbf{u}}_{\text{world}}|}
$$

True up (orthogonal to both):

$$
\hat{\mathbf{u}} = \hat{\mathbf{r}} \times \hat{\mathbf{f}}
$$

**Step 2: The camera's model matrix places it in world space:**

$$
M_{\text{cam}} = \begin{pmatrix} r_x & u_x & -f_x & e_x \\ r_y & u_y & -f_y & e_y \\ r_z & u_z & -f_z & e_z \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

(Columns are the camera's right, up, and backward directions, plus position.)

**Step 3: The view matrix is the inverse.**

Since the upper-left 3×3 is orthogonal (call it $R$), and the translation is $\mathbf{e}$:

$$
M_{\text{cam}}^{-1} = \begin{pmatrix} R^T & -R^T\mathbf{e} \\ \mathbf{0}^T & 1 \end{pmatrix}
$$

Writing out $R^T$ (rows become the camera axes):

$$
V = \begin{pmatrix} r_x & r_y & r_z & -(r_x e_x + r_y e_y + r_z e_z) \\ u_x & u_y & u_z & -(u_x e_x + u_y e_y + u_z e_z) \\ -f_x & -f_y & -f_z & f_x e_x + f_y e_y + f_z e_z \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

Which matches Definition 28.1.6 with dot-product notation: $-\hat{\mathbf{r}} \cdot \mathbf{e}$, $-\hat{\mathbf{u}} \cdot \mathbf{e}$, $\hat{\mathbf{f}} \cdot \mathbf{e}$. $\blacksquare$



---

## 💻 6. Code Examples

### 6.1 Python+NumPy: Building TRS Matrices

```python
import numpy as np

def translation_matrix(tx: float, ty: float, tz: float) -> np.ndarray:
    """4x4 translation matrix (column-major convention)."""
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ], dtype=np.float64)

def scale_matrix(sx: float, sy: float, sz: float) -> np.ndarray:
    """4x4 scale matrix."""
    return np.diag([sx, sy, sz, 1.0])

def rotation_x(theta: float) -> np.ndarray:
    """4x4 rotation about X-axis, angle in radians."""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [1, 0,  0, 0],
        [0, c, -s, 0],
        [0, s,  c, 0],
        [0, 0,  0, 1]
    ], dtype=np.float64)

def rotation_y(theta: float) -> np.ndarray:
    """4x4 rotation about Y-axis, angle in radians."""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [ c, 0, s, 0],
        [ 0, 1, 0, 0],
        [-s, 0, c, 0],
        [ 0, 0, 0, 1]
    ], dtype=np.float64)

def rotation_z(theta: float) -> np.ndarray:
    """4x4 rotation about Z-axis, angle in radians."""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, -s, 0, 0],
        [s,  c, 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1]
    ], dtype=np.float64)

def perspective_matrix(fov_y: float, aspect: float, near: float, far: float) -> np.ndarray:
    """OpenGL-style perspective projection matrix."""
    t = np.tan(fov_y / 2.0)
    return np.array([
        [1/(aspect*t), 0,    0,                        0],
        [0,            1/t,  0,                        0],
        [0,            0,    -(far+near)/(far-near),  -2*far*near/(far-near)],
        [0,            0,    -1,                       0]
    ], dtype=np.float64)

# Example: compose TRS and transform a vertex
T = translation_matrix(3, 0, -5)
R = rotation_y(np.radians(45))
S = scale_matrix(2, 2, 2)
M = T @ R @ S  # Model matrix

v_local = np.array([1, 0, 0, 1])  # point in object space
v_world = M @ v_local
print(f"World position: {v_world[:3]}")
```

### 6.2 Unity C#: TRS Matrix Construction

```csharp
using UnityEngine;

public class TRSDemo : MonoBehaviour
{
    void Start()
    {
        // Unity's Matrix4x4.TRS composes Translation * Rotation * Scale
        Vector3 position = new Vector3(3f, 0f, -5f);
        Quaternion rotation = Quaternion.Euler(0f, 45f, 0f);
        Vector3 scale = new Vector3(2f, 2f, 2f);

        Matrix4x4 modelMatrix = Matrix4x4.TRS(position, rotation, scale);

        // Transform a local-space point to world space
        Vector3 localPoint = new Vector3(1f, 0f, 0f);
        Vector3 worldPoint = modelMatrix.MultiplyPoint3x4(localPoint);
        Debug.Log($"World position: {worldPoint}");

        // The view matrix is the inverse of the camera's TRS
        Matrix4x4 viewMatrix = Camera.main.worldToCameraMatrix;

        // Full MVP chain
        Matrix4x4 projMatrix = Camera.main.projectionMatrix;
        Matrix4x4 mvp = projMatrix * viewMatrix * modelMatrix;

        Vector4 clipPos = mvp * new Vector4(localPoint.x, localPoint.y, localPoint.z, 1f);
        Vector3 ndc = new Vector3(clipPos.x / clipPos.w, clipPos.y / clipPos.w, clipPos.z / clipPos.w);
        Debug.Log($"NDC: {ndc}");
    }
}
```

### 6.3 GLSL Vertex Shader: MVP Transform

```glsl
#version 330 core

layout(location = 0) in vec3 aPosition;
layout(location = 1) in vec3 aNormal;

uniform mat4 u_Model;
uniform mat4 u_View;
uniform mat4 u_Projection;
uniform mat3 u_NormalMatrix; // = transpose(inverse(mat3(u_Model)))

out vec3 v_WorldPos;
out vec3 v_WorldNormal;

void main()
{
    vec4 worldPos = u_Model * vec4(aPosition, 1.0);
    v_WorldPos = worldPos.xyz;

    // Normal matrix handles non-uniform scale correctly
    v_WorldNormal = normalize(u_NormalMatrix * aNormal);

    gl_Position = u_Projection * u_View * worldPos;
}
```

---

## 🧮 7. Worked Examples

### Example 28.1.1 — Composing a Model Matrix

**Problem:** An object is scaled by $(2, 1, 3)$, rotated $90°$ about the $y$-axis, then translated to $(5, 0, -10)$. Find the model matrix $M$ and the world-space position of the local vertex $\mathbf{v} = (1, 0, 0)$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Construct $S$:

$$
S = \begin{pmatrix} 2 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 3 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

**Step 2:** Construct $R_y(90°)$ with $\cos 90° = 0$, $\sin 90° = 1$:

$$
R_y = \begin{pmatrix} 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ -1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

**Step 3:** Construct $T$:

$$
T = \begin{pmatrix} 1 & 0 & 0 & 5 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & -10 \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

**Step 4:** Compute $M = T \cdot R_y \cdot S$:

First, $R_y \cdot S$:

$$
R_y \cdot S = \begin{pmatrix} 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ -1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} 2 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 3 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix} = \begin{pmatrix} 0 & 0 & 3 & 0 \\ 0 & 1 & 0 & 0 \\ -2 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

Then $T \cdot (R_y \cdot S)$:

$$
M = \begin{pmatrix} 0 & 0 & 3 & 5 \\ 0 & 1 & 0 & 0 \\ -2 & 0 & 0 & -10 \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

**Step 5:** Transform the vertex:

$$
\mathbf{v}_{\text{world}} = M \begin{pmatrix} 1 \\ 0 \\ 0 \\ 1 \end{pmatrix} = \begin{pmatrix} 0(1) + 0(0) + 3(0) + 5 \\ 0(1) + 1(0) + 0(0) + 0 \\ -2(1) + 0(0) + 0(0) + (-10) \\ 1 \end{pmatrix} = \begin{pmatrix} 5 \\ 0 \\ -12 \\ 1 \end{pmatrix}
$$

The vertex is at world position $(5, 0, -12)$.

</details>

### Example 28.1.2 — Perspective Projection of a Point

**Problem:** A point is at view-space position $(3, 2, -8)$. The camera has $\text{fov}_y = 60°$, aspect ratio $16:9$, near $= 0.1$, far $= 100$. Find the NDC coordinates.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Compute projection matrix parameters.

$$
\tan(\text{fov}_y / 2) = \tan(30°) = \frac{1}{\sqrt{3}} \approx 0.5774
$$

$$
P_{11} = \frac{1}{a \cdot \tan(30°)} = \frac{1}{(16/9)(1/\sqrt{3})} = \frac{9\sqrt{3}}{16} \approx 0.9743
$$

$$
P_{22} = \frac{1}{\tan(30°)} = \sqrt{3} \approx 1.7321
$$

$$
P_{33} = \frac{-(100 + 0.1)}{100 - 0.1} = \frac{-100.1}{99.9} \approx -1.0020
$$

$$
P_{34} = \frac{-2(100)(0.1)}{99.9} = \frac{-20}{99.9} \approx -0.2002
$$

**Step 2:** Multiply $P \cdot \mathbf{v}$:

$$
\mathbf{v}_{\text{clip}} = \begin{pmatrix} 0.9743 & 0 & 0 & 0 \\ 0 & 1.7321 & 0 & 0 \\ 0 & 0 & -1.0020 & -0.2002 \\ 0 & 0 & -1 & 0 \end{pmatrix} \begin{pmatrix} 3 \\ 2 \\ -8 \\ 1 \end{pmatrix}
$$

$$
x_{\text{clip}} = 0.9743 \times 3 = 2.9229
$$

$$
y_{\text{clip}} = 1.7321 \times 2 = 3.4641
$$

$$
z_{\text{clip}} = (-1.0020)(-8) + (-0.2002)(1) = 8.0160 - 0.2002 = 7.8158
$$

$$
w_{\text{clip}} = (-1)(-8) + 0 = 8
$$

**Step 3:** Perspective divide:

$$
x_{\text{ndc}} = \frac{2.9229}{8} = 0.3654
$$

$$
y_{\text{ndc}} = \frac{3.4641}{8} = 0.4330
$$

$$
z_{\text{ndc}} = \frac{7.8158}{8} = 0.9770
$$

The point is within the NDC cube $[-1, 1]^3$ (visible). Its depth $z_{\text{ndc}} = 0.977$ is close to 1 (the far plane), confirming it is relatively distant.

</details>

### Example 28.1.3 — Computing the Normal Matrix

**Problem:** A model matrix has non-uniform scale $(1, 2, 1)$ and rotation $R_z(45°)$. Compute the normal matrix and transform the normal $\hat{\mathbf{n}} = (0, 1, 0)$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Build $M = R_z(45°) \cdot S(1, 2, 1)$ (ignoring translation for normals):

$$
R_z(45°) = \begin{pmatrix} \frac{\sqrt{2}}{2} & -\frac{\sqrt{2}}{2} & 0 \\ \frac{\sqrt{2}}{2} & \frac{\sqrt{2}}{2} & 0 \\ 0 & 0 & 1 \end{pmatrix}, \quad S = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 1 \end{pmatrix}
$$

$$
M_{3\times3} = R_z \cdot S = \begin{pmatrix} \frac{\sqrt{2}}{2} & -\sqrt{2} & 0 \\ \frac{\sqrt{2}}{2} & \sqrt{2} & 0 \\ 0 & 0 & 1 \end{pmatrix}
$$

**Step 2:** Compute $M^{-1}$. Since $M = R \cdot S$, $M^{-1} = S^{-1} R^T$:

$$
S^{-1} = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1/2 & 0 \\ 0 & 0 & 1 \end{pmatrix}, \quad R^T = \begin{pmatrix} \frac{\sqrt{2}}{2} & \frac{\sqrt{2}}{2} & 0 \\ -\frac{\sqrt{2}}{2} & \frac{\sqrt{2}}{2} & 0 \\ 0 & 0 & 1 \end{pmatrix}
$$

$$
M^{-1} = S^{-1} R^T = \begin{pmatrix} \frac{\sqrt{2}}{2} & \frac{\sqrt{2}}{2} & 0 \\ -\frac{\sqrt{2}}{4} & \frac{\sqrt{2}}{4} & 0 \\ 0 & 0 & 1 \end{pmatrix}
$$

**Step 3:** Normal matrix $N = (M^{-1})^T$:

$$
N = \begin{pmatrix} \frac{\sqrt{2}}{2} & -\frac{\sqrt{2}}{4} & 0 \\ \frac{\sqrt{2}}{2} & \frac{\sqrt{2}}{4} & 0 \\ 0 & 0 & 1 \end{pmatrix}
$$

**Step 4:** Transform the normal:

$$
\mathbf{n}' = N \begin{pmatrix} 0 \\ 1 \\ 0 \end{pmatrix} = \begin{pmatrix} -\frac{\sqrt{2}}{4} \\ \frac{\sqrt{2}}{4} \\ 0 \end{pmatrix}
$$

**Step 5:** Normalize:

$$
|\mathbf{n}'| = \sqrt{\frac{2}{16} + \frac{2}{16}} = \sqrt{\frac{1}{4}} = \frac{1}{2}
$$

$$
\hat{\mathbf{n}}' = \begin{pmatrix} -\frac{\sqrt{2}}{2} \\ \frac{\sqrt{2}}{2} \\ 0 \end{pmatrix}
$$

The normal has rotated and is no longer aligned with the $y$-axis due to the non-uniform scale.

</details>

### Example 28.1.4 — View Matrix from Camera Parameters

**Problem:** Camera at $\mathbf{e} = (0, 5, 10)$, looking at target $\mathbf{t} = (0, 0, 0)$, world up $= (0, 1, 0)$. Compute the view matrix.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Forward direction:

$$
\hat{\mathbf{f}} = \frac{\mathbf{t} - \mathbf{e}}{|\mathbf{t} - \mathbf{e}|} = \frac{(0, -5, -10)}{|(0, -5, -10)|} = \frac{(0, -5, -10)}{\sqrt{0 + 25 + 100}} = \frac{(0, -5, -10)}{\sqrt{125}} = (0, -\frac{1}{\sqrt{5}}, -\frac{2}{\sqrt{5}})
$$

**Step 2:** Right direction:

$$
\hat{\mathbf{r}} = \frac{\hat{\mathbf{f}} \times \hat{\mathbf{u}}_{\text{world}}}{|\hat{\mathbf{f}} \times \hat{\mathbf{u}}_{\text{world}}|}
$$

$$
\hat{\mathbf{f}} \times (0,1,0) = \begin{vmatrix} \hat{\mathbf{i}} & \hat{\mathbf{j}} & \hat{\mathbf{k}} \\ 0 & -1/\sqrt{5} & -2/\sqrt{5} \\ 0 & 1 & 0 \end{vmatrix} = \left(\frac{-2}{\sqrt{5}} \cdot 0 - 0 \cdot 1,\; 0 \cdot 0 - 0 \cdot \frac{-2}{\sqrt{5}},\; 0 \cdot 1 - \frac{-1}{\sqrt{5}} \cdot 0\right)
$$

Wait — let me recompute carefully:

$$
\hat{\mathbf{f}} \times (0,1,0) = (f_y \cdot 0 - f_z \cdot 1,\; f_z \cdot 0 - f_x \cdot 0,\; f_x \cdot 1 - f_y \cdot 0)
$$

$$
= (-f_z - 0 \cdot 1,\; 0,\; 0) \quad \text{... using } \mathbf{a} \times \mathbf{b} = (a_2 b_3 - a_3 b_2, a_3 b_1 - a_1 b_3, a_1 b_2 - a_2 b_1)
$$

$$
= \left((-1/\sqrt{5})(0) - (-2/\sqrt{5})(1),\; (-2/\sqrt{5})(0) - (0)(0),\; (0)(1) - (-1/\sqrt{5})(0)\right)
$$

$$
= (2/\sqrt{5},\; 0,\; 0)
$$

Normalizing: $\hat{\mathbf{r}} = (1, 0, 0)$.

**Step 3:** True up:

$$
\hat{\mathbf{u}} = \hat{\mathbf{r}} \times \hat{\mathbf{f}} = (1, 0, 0) \times (0, -1/\sqrt{5}, -2/\sqrt{5})
$$

$$
= (0 \cdot (-2/\sqrt{5}) - 0 \cdot (-1/\sqrt{5}),\; 0 \cdot 0 - 1 \cdot (-2/\sqrt{5}),\; 1 \cdot (-1/\sqrt{5}) - 0 \cdot 0)
$$

$$
= (0,\; 2/\sqrt{5},\; -1/\sqrt{5})
$$

**Step 4:** Assemble view matrix:

$$
V = \begin{pmatrix} 1 & 0 & 0 & -(1)(0) - (0)(5) - (0)(10) \\ 0 & 2/\sqrt{5} & -1/\sqrt{5} & -(0)(0) - (2/\sqrt{5})(5) - (-1/\sqrt{5})(10) \\ 0 & 1/\sqrt{5} & 2/\sqrt{5} & -(0)(0) - (-1/\sqrt{5})(5) - (-2/\sqrt{5})(10) \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

Computing the translation column (row 3 uses $-\hat{\mathbf{f}}$):

- Row 1: $-\hat{\mathbf{r}} \cdot \mathbf{e} = -(1 \cdot 0 + 0 \cdot 5 + 0 \cdot 10) = 0$
- Row 2: $-\hat{\mathbf{u}} \cdot \mathbf{e} = -(0 \cdot 0 + \frac{2}{\sqrt{5}} \cdot 5 + \frac{-1}{\sqrt{5}} \cdot 10) = -(\frac{10}{\sqrt{5}} - \frac{10}{\sqrt{5}}) = 0$
- Row 3: $\hat{\mathbf{f}} \cdot \mathbf{e} = 0 \cdot 0 + (-\frac{1}{\sqrt{5}})(5) + (-\frac{2}{\sqrt{5}})(10) = -\frac{5}{\sqrt{5}} - \frac{20}{\sqrt{5}} = -\frac{25}{\sqrt{5}} = -5\sqrt{5}$

$$
V = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 2/\sqrt{5} & -1/\sqrt{5} & 0 \\ 0 & 1/\sqrt{5} & 2/\sqrt{5} & -5\sqrt{5} \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

The camera is $\sqrt{125} = 5\sqrt{5} \approx 11.18$ units from the origin, which appears as the $z$-translation in view space.

</details>



---

## 🔗 8. Cross-links & Further Reading

### Internal Links
- **Next chapter:** [28.2 - Quaternions & Rotations](28.2---Quaternions-&-Rotations) — extends rotation representation beyond Euler angles
- **Linear Algebra foundations:** [2.4 - Linear Transformations & Change of Basis](2.4---Linear-Transformations-&-Change-of-Basis) — the mathematical framework for all coordinate space changes
- **Matrix operations:** [2.3 - Matrix Operations & Inverses](2.3---Matrix-Operations-&-Inverses) — inverse computation, transpose properties
- **Determinants:** [2.5 - Determinants & Cramer's Rule](2.5---Determinants-&-Cramer's-Rule) — why $\det(R) = 1$ for rotations
- **Eigenvalues:** [2.6 - Eigenvalues Eigenvectors & Diagonalization](2.6---Eigenvalues-Eigenvectors-&-Diagonalization) — rotation axes as eigenvectors of rotation matrices
- **Vector calculus:** [1.4 - Vector Calculus](1.4---Vector-Calculus) — cross products, dot products used in view matrix construction
- **Multiple integrals:** [1.5 - Multiple Integrals & Jacobians](1.5---Multiple-Integrals-&-Jacobians) — Jacobian determinants relate to the normal matrix

### External Resources
- **Real-Time Rendering** (Akenine-Möller, Haines, Hoffman) — Chapter 4: Transforms
- **Mathematics for 3D Game Programming and Computer Graphics** (Lengyel) — Chapters 2–5
- **Fundamentals of Computer Graphics** (Marschner & Shirley) — Chapter 7: Viewing
- **OpenGL Programming Guide** (Red Book) — Chapter 5: Viewing Transformations
- **3Blue1Brown: Essence of Linear Algebra** — visual intuition for matrix transformations

### Practice
- [9.1_3d_math.py](9.1_3d_math.py) — randomized TRS and projection drill problems

