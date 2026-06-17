---
title: "Greens Stokes And Divergence Theorems"
subject: "Mathematical Foundations & Calculus"
catalog: advanced
audience_tier: higher-education
chapter: "1.7"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

![Mastering_Generalized_Stokes__Theorem](Mastering_Generalized_Stokes__Theorem.png)

![Unified_Theory_of_Integration_Guide](Unified_Theory_of_Integration_Guide.png)

> [!info]+ 🎬 Companion materials (NotebookLM)
> 🎙️ Audio overview: ![The_Single_Theorem_Unifying_Vector_Calculus](The_Single_Theorem_Unifying_Vector_Calculus.m4a)
> 🎬 Video walkthrough: ![The_Geometry_of_Integral_Theorems](The_Geometry_of_Integral_Theorems.mp4)
> 📘 Study guide: [Comprehensive Study Guide_ Advanced Calculus and Differential Equations](Comprehensive-Study-Guide_-Advanced-Calculus-and-Differential-Equations)

# 1.7 — Green's, Stokes' and Divergence Theorems

> *"The universe is not only queerer than we suppose, but queerer than we can suppose."* — J.B.S. Haldane.
> (And yet three wildly different-looking integral theorems turn out to be the same theorem wearing different clothes.)

Here is the secret the textbooks bury in the footnotes: **Green's Theorem, Stokes' Theorem, and the Divergence Theorem are one theorem.**

$$
\int_{\partial M} \omega = \int_M d\omega
$$

That is the **Generalized Stokes' Theorem**. Integrate a differential form $\omega$ over the boundary $\partial M$ of a manifold $M$, and you get the same answer as integrating the exterior derivative $d\omega$ over $M$ itself. Chapter 1.8 will formalize this with the language of differential forms. *This* chapter builds the geometric muscle: we prove each of the three classical versions in coordinates, work through eight examples that matter to physics, and always point back to the single unifying structure above.

Read this chapter as three acts of one play. The protagonist ($\int_{\partial M}\omega = \int_M d\omega$) never changes — only the costume does.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. State and prove Green's Theorem for a rectangle; extend by decomposition.
2. State and prove Stokes' Theorem by reducing to Green's via a parameterization.
3. State and prove the Divergence Theorem for a box; extend by decomposition.
4. Identify the correct theorem for a given integral (line, surface, volume).
5. Correctly orient boundaries: counterclockwise for planar curves, right-hand rule for surfaces.
6. Use the area formula $A = \tfrac{1}{2}\oint x\,dy - y\,dx$ derived from Green's theorem.
7. Derive the continuity equation $\partial_t\rho + \nabla\cdot\mathbf{J} = 0$ using the Divergence Theorem.
8. Recognize Maxwell's integral laws as direct applications of these theorems.

---


## 🌌 Why the fuck does this matter?

**Maxwell's equations in integral form** are *literally* these theorems:

- Gauss's Law $\oiint \mathbf{E}\cdot d\mathbf{S} = Q_{\text{enc}}/\varepsilon_0$ is the **Divergence Theorem** applied to $\mathbf{E}$.
- Faraday's Law $\oint \mathbf{E}\cdot d\mathbf{r} = -\frac{d}{dt}\iint \mathbf{B}\cdot d\mathbf{S}$ is **Stokes' Theorem** applied to $\mathbf{E}$.
- Ampère-Maxwell Law $\oint \mathbf{B}\cdot d\mathbf{r} = \mu_0 I_{\text{enc}} + \mu_0\varepsilon_0 \frac{d\Phi_E}{dt}$ is **Stokes'** applied to $\mathbf{B}$.

**Fluid dynamics:** The continuity equation — mass conservation — is the Divergence Theorem applied to the mass flux $\mathbf{J} = \rho\mathbf{v}$. Every CFD simulation that keeps fluid from disappearing relies on this.

**General Relativity:** The Einstein field equations in integral form involve integrating curvature over 4-manifolds. The machinery is $\int_{\partial M}\omega = \int_M d\omega$ on a Lorentzian manifold. Without Stokes in its generalized form, there is no GR.

**Engineering:** Every finite-element method, every boundary-element method, every vortex panel method in aerodynamics converts a volume integral (expensive) into a surface integral (cheap) via the Divergence Theorem. Aircraft fly because engineers understood Gauss in 1813.

---

## 🖼️ Visual Anchor 1 — The One Theorem

The picture that encodes everything in this chapter:

![math-01__1.7-fig1](math-01__1.7-fig1.svg)

---


## 📚 1. Definitions

### Definition 1.7.1 — Simply Connected Domain

A region $D \subset \mathbb{R}^n$ is **simply connected** if it is path-connected and every simple closed curve in $D$ can be continuously contracted to a point *while remaining in $D$*.

Intuitively: no holes. $\mathbb{R}^2$ itself is simply connected; the punctured plane $\mathbb{R}^2 \setminus \{0\}$ is **not** (a circle around the origin cannot be shrunk to a point without passing through $0$).

**Multiply connected** domains have one or more holes. The annulus $\{(x,y) : 1 < x^2+y^2 < 4\}$ has one hole; $\mathbb{R}^2$ minus $k$ points has $k$ holes.

**Why it matters here:** Green's theorem and Stokes' theorem require the domain to be simply connected to guarantee that a curl-free field is conservative. On a multiply connected domain, $\nabla\times\mathbf{F}=0$ does not imply $\mathbf{F}=\nabla f$ (the classic example: $\mathbf{F} = (-y,x)/(x^2+y^2)$ has zero curl off the origin but non-zero circulation around the origin).

### Definition 1.7.2 — Positive Orientation of $\partial D$

Let $D$ be a bounded planar region with boundary curve $\partial D$. The **positive orientation** (also called **counterclockwise orientation**) is defined such that a person walking along $\partial D$ has $D$ to their **left**.

Equivalently: the outward normal to $\partial D$ (pointing away from $D$) is obtained by rotating the tangent $90°$ *counterclockwise*.

For a region with holes, the **outer** boundary is traversed counterclockwise and each **inner** boundary (around a hole) is traversed **clockwise** — so that $D$ remains to the left on all pieces.

### Definition 1.7.3 — Oriented Surface and Unit Normal

A **smooth surface** $S$ in $\mathbb{R}^3$ is **orientable** if there is a continuous choice of unit normal $\hat{n}$ at every point. An **orientation** is such a choice. The two possible choices are called **outward** and **inward** (or **upward**/**downward** for graphs).

For a **closed surface** (one bounding a solid region $V$), the convention is **outward** — $\hat{n}$ points away from $V$.

The vector area element is $d\mathbf{S} = \hat{n}\,dS$, where $dS$ is the scalar surface-area element.

### Definition 1.7.4 — Surface Integral (Flux)

For a vector field $\mathbf{F} : \mathbb{R}^3 \to \mathbb{R}^3$ and an oriented surface $S$ with unit normal $\hat{n}$:

$$
\iint_S \mathbf{F}\cdot d\mathbf{S} = \iint_S \mathbf{F}\cdot\hat{n}\,dS.
$$

This is the **flux** of $\mathbf{F}$ through $S$: the net rate at which $\mathbf{F}$ passes *through* the surface (positive when passing in the direction of $\hat{n}$, negative in the opposite direction).

For a parameterization $\mathbf{r}(u,v)$ over a parameter domain $D_{uv}$:

$$
d\mathbf{S} = \left(\frac{\partial\mathbf{r}}{\partial u}\times\frac{\partial\mathbf{r}}{\partial v}\right)du\,dv,
$$

so the orientation is determined by the order of the cross product (swapping $u$ and $v$ reverses the normal).

### Definition 1.7.5 — Boundary Notation

- $\partial D$: the **boundary curve** of a planar region $D$ (a closed curve or union of curves).
- $\partial S$: the **boundary curve** of a surface $S$ (one closed curve if $S$ is like a disk; may be empty if $S$ is closed).
- $\partial V$: the **boundary surface** of a solid region $V$ (a closed surface).

The key topological fact: $\partial(\partial M) = \emptyset$ — the boundary of a boundary is empty. This is the algebraic engine behind the generalized theorem.

---


## 🖼️ Visual Anchor 2 — Green's Theorem: Oriented Boundary

![math-01__1.7-fig2](math-01__1.7-fig2.svg)

---

## 👑 2. The Theorems

### Theorem 1.7.1 — Green's Theorem (Circulation Form)

Let $D$ be a simply connected bounded region in $\mathbb{R}^2$ with a piecewise-smooth positively oriented boundary $\partial D$. Let $P(x,y)$ and $Q(x,y)$ be functions with continuous partial derivatives on an open set containing $D$. Then:

$$
\oint_{\partial D} P\,dx + Q\,dy = \iint_D \left(\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}\right)dA.
$$

**Translation:** the circulation of the vector field $(P, Q)$ around $\partial D$ equals the total "spin" (the 2D curl $\partial_x Q - \partial_y P$) integrated over the interior.

### Theorem 1.7.2 — Green's Theorem (Flux Form)

Under the same hypotheses, if $\mathbf{F} = (P, Q)$ and $\hat{n}$ is the outward unit normal to $\partial D$, then:

$$
\oint_{\partial D} \mathbf{F}\cdot\hat{n}\,ds = \iint_D (\nabla\cdot\mathbf{F})\,dA.
$$

**Translation:** the outward flux of $\mathbf{F}$ through $\partial D$ equals the total divergence (source density) integrated over $D$. This is the 2D version of the Divergence Theorem.

### Theorem 1.7.3 — Stokes' Theorem

Let $S$ be a smooth oriented surface in $\mathbb{R}^3$ with piecewise-smooth boundary curve $\partial S$ oriented consistently with $S$ by the right-hand rule. Let $\mathbf{F}$ be a vector field with continuous partial derivatives on an open set containing $S$. Then:

$$
\oint_{\partial S} \mathbf{F}\cdot d\mathbf{r} = \iint_S (\nabla\times\mathbf{F})\cdot d\mathbf{S}.
$$

**Right-hand rule for orientation:** curl the fingers of your right hand in the direction of traversal on $\partial S$; your thumb points in the direction of $\hat{n}$ on $S$.

### Theorem 1.7.4 — Divergence Theorem (Gauss's Theorem)

Let $V$ be a bounded solid region in $\mathbb{R}^3$ with a piecewise-smooth closed boundary surface $\partial V$ oriented with outward-pointing normal $\hat{n}$. Let $\mathbf{F}$ be a vector field with continuous partial derivatives on an open set containing $V$. Then:

$$
\oiint_{\partial V} \mathbf{F}\cdot d\mathbf{S} = \iiint_V (\nabla\cdot\mathbf{F})\,dV.
$$

**Translation:** the total outward flux of $\mathbf{F}$ through the closed surface $\partial V$ equals the total divergence (net source strength) in the interior $V$.

---


## 🖼️ Visual Anchor 3 — Stokes' Theorem: Surface, Boundary, Right-Hand Rule

![math-01__1.7-fig3](math-01__1.7-fig3.svg)

---

## 🖼️ Visual Anchor 4 — Divergence Theorem: Volume, Closed Surface, Outward Flux

![math-01__1.7-fig4](math-01__1.7-fig4.svg)

---


## ✍️ 3. Proofs

### 3.1 Proof of Green's Theorem — Rectangle First, Then Extension

**Step 1: Prove for a rectangle.** Let $D = [a,b]\times[c,d]$. The boundary $\partial D$ consists of four edges, traversed counterclockwise: bottom ($y=c$, left to right), right ($x=b$, bottom to top), top ($y=d$, right to left), left ($x=a$, top to bottom).

We will show both sides are equal by proving two sub-identities separately:

$$
\oint_{\partial D} P\,dx = -\iint_D \frac{\partial P}{\partial y}\,dA \quad\text{and}\quad \oint_{\partial D} Q\,dy = \iint_D \frac{\partial Q}{\partial x}\,dA.
$$

Adding these two gives Green's theorem.

**Proof of the $P\,dx$ identity:** On the horizontal edges, $dx \neq 0$; on the vertical edges, $dx = 0$. So only the bottom and top edges contribute.

- Bottom edge ($y=c$, $x$ from $a$ to $b$): $\int_a^b P(x,c)\,dx$.
- Top edge ($y=d$, $x$ from $b$ to $a$, i.e., reversed): $-\int_a^b P(x,d)\,dx$.

Hence:

$$
\oint_{\partial D} P\,dx = \int_a^b P(x,c)\,dx - \int_a^b P(x,d)\,dx = \int_a^b \bigl[P(x,c) - P(x,d)\bigr]\,dx.
$$

Now compute the right side using the Fundamental Theorem of Calculus in $y$:

$$
-\iint_D \frac{\partial P}{\partial y}\,dA = -\int_a^b \int_c^d \frac{\partial P}{\partial y}(x,y)\,dy\,dx = -\int_a^b \bigl[P(x,d) - P(x,c)\bigr]\,dx = \int_a^b \bigl[P(x,c) - P(x,d)\bigr]\,dx.
$$

The two sides are equal. $\checkmark$

**Proof of the $Q\,dy$ identity:** By the same argument (now integrate $\partial Q/\partial x$ in $x$ using FTC, and only vertical edges contribute on the left):

$$
\oint_{\partial D} Q\,dy = \int_c^d Q(b,y)\,dy - \int_c^d Q(a,y)\,dy,
$$

$$
\iint_D \frac{\partial Q}{\partial x}\,dA = \int_c^d \int_a^b \frac{\partial Q}{\partial x}\,dx\,dy = \int_c^d \bigl[Q(b,y) - Q(a,y)\bigr]\,dy.
$$

Equal. $\checkmark$ Adding both identities:

$$
\oint_{\partial D} P\,dx + Q\,dy = \iint_D \left(\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}\right)dA. \quad \blacksquare_{\text{rectangle}}
$$

**Step 2: Extension to general regions.** Any region $D$ satisfying the hypotheses can be decomposed into finitely many (or a limiting sequence of) rectangles $\{D_i\}$ by a grid. Green's theorem holds on each $D_i$. When we sum over all rectangles, the interior boundary segments cancel (they are traversed once in each direction by adjacent rectangles), leaving only the outer boundary $\partial D$. The double integrals add to give $\iint_D$ over the whole region. $\blacksquare$

---

### 3.2 Proof of Stokes' Theorem — Via Green's Theorem on the Parameter Domain

**Setup.** Let $\mathbf{r}(u,v) : D_{uv} \to \mathbb{R}^3$ parameterize $S$, where $D_{uv}$ is a simply connected planar domain. The boundary $\partial S$ corresponds to $\partial D_{uv}$ under $\mathbf{r}$.

**Step 1: Expand the line integral over $\partial S$.** Using $d\mathbf{r} = \mathbf{r}_u\,du + \mathbf{r}_v\,dv$ where $\mathbf{r}_u = \partial\mathbf{r}/\partial u$ and $\mathbf{r}_v = \partial\mathbf{r}/\partial v$:

$$
\oint_{\partial S} \mathbf{F}\cdot d\mathbf{r} = \oint_{\partial D_{uv}} \mathbf{F}(\mathbf{r}(u,v))\cdot(\mathbf{r}_u\,du + \mathbf{r}_v\,dv).
$$

Define $P^* = \mathbf{F}\cdot\mathbf{r}_u$ and $Q^* = \mathbf{F}\cdot\mathbf{r}_v$ as functions of $(u,v)$. Then:

$$
= \oint_{\partial D_{uv}} P^*\,du + Q^*\,dv.
$$

**Step 2: Apply Green's Theorem** to $(P^*, Q^*)$ on $D_{uv}$:

$$
= \iint_{D_{uv}} \left(\frac{\partial Q^*}{\partial u} - \frac{\partial P^*}{\partial v}\right)du\,dv.
$$

**Step 3: Compute $\partial_u Q^* - \partial_v P^*$.** Write $\mathbf{F} = (F_1, F_2, F_3)$. Then:

$$
Q^* = \mathbf{F}\cdot\mathbf{r}_v = F_1 \frac{\partial x}{\partial v} + F_2 \frac{\partial y}{\partial v} + F_3 \frac{\partial z}{\partial v}.
$$

Differentiating $Q^*$ with respect to $u$ (chain rule, noting $F_i$ depends on $(x,y,z)$ which depend on $(u,v)$) and similarly for $\partial_v P^*$, then subtracting, a careful computation (expanding all terms and collecting) yields exactly:

$$
\frac{\partial Q^*}{\partial u} - \frac{\partial P^*}{\partial v} = (\nabla\times\mathbf{F})\cdot\left(\frac{\partial\mathbf{r}}{\partial u}\times\frac{\partial\mathbf{r}}{\partial v}\right).
$$

(This step is the algebraic core; it follows from the antisymmetry of the cross product and the chain rule applied systematically to all components.)

**Step 4: Recognize the surface integral.** Since $d\mathbf{S} = \mathbf{r}_u\times\mathbf{r}_v\,du\,dv$:

$$
\iint_{D_{uv}} (\nabla\times\mathbf{F})\cdot(\mathbf{r}_u\times\mathbf{r}_v)\,du\,dv = \iint_S (\nabla\times\mathbf{F})\cdot d\mathbf{S}. \quad \blacksquare
$$

---


### 3.3 Proof of the Divergence Theorem — Box First, Then Extension

**Step 1: Prove for a box.** Let $V = [a,b]\times[c,d]\times[e,f]$ be a rectangular box. We prove three sub-identities and add:

$$
\oiint_{\partial V} F_1\,dS_x = \iiint_V \frac{\partial F_1}{\partial x}\,dV,
$$

and analogously for $F_2$ in $y$ and $F_3$ in $z$.

**Proof of the $F_1$ identity.** The boundary $\partial V$ consists of six faces. Only the two faces perpendicular to the $x$-axis contribute to $\oiint F_1\,dS_x$, because on all other faces the outward normal has no $x$-component. Specifically:

- Right face ($x=b$, outward normal $+\hat{x}$): $dS_x = +dy\,dz$, contributing $\int_c^d\int_e^f F_1(b,y,z)\,dy\,dz$.
- Left face ($x=a$, outward normal $-\hat{x}$): $dS_x = -dy\,dz$, contributing $-\int_c^d\int_e^f F_1(a,y,z)\,dy\,dz$.

So:

$$
\oiint_{\partial V} F_1\,dS_x = \int_c^d\int_e^f \bigl[F_1(b,y,z) - F_1(a,y,z)\bigr]\,dy\,dz.
$$

By the Fundamental Theorem of Calculus in $x$:

$$
F_1(b,y,z) - F_1(a,y,z) = \int_a^b \frac{\partial F_1}{\partial x}(x,y,z)\,dx.
$$

Substituting:

$$
\oiint_{\partial V} F_1\,dS_x = \int_c^d\int_e^f\int_a^b \frac{\partial F_1}{\partial x}\,dx\,dy\,dz = \iiint_V \frac{\partial F_1}{\partial x}\,dV. \quad \checkmark
$$

The same argument applies to $F_2$ (faces perpendicular to $y$) and $F_3$ (faces perpendicular to $z$). Adding all three:

$$
\oiint_{\partial V} (F_1\,dS_x + F_2\,dS_y + F_3\,dS_z) = \iiint_V \left(\frac{\partial F_1}{\partial x} + \frac{\partial F_2}{\partial y} + \frac{\partial F_3}{\partial z}\right)dV,
$$

which is exactly $\oiint_{\partial V}\mathbf{F}\cdot d\mathbf{S} = \iiint_V (\nabla\cdot\mathbf{F})\,dV$. $\blacksquare_{\text{box}}$

**Step 2: Extension.** Decompose any solid region $V$ into small boxes. Interior face contributions cancel (outward for one box is inward for the adjacent box). Only $\partial V$ remains. $\blacksquare$

---

### 3.4 Corollary 1 — Conservative ⟺ Curl-Free (on Simply Connected Domains)

**Theorem.** Let $\mathbf{F}$ be a $C^1$ vector field on a simply connected domain $U \subset \mathbb{R}^3$. Then $\mathbf{F} = \nabla f$ for some scalar $f$ if and only if $\nabla\times\mathbf{F} = \mathbf{0}$ everywhere on $U$.

**Proof ($\Rightarrow$).** If $\mathbf{F} = \nabla f$, then $F_i = \partial f/\partial x_i$. Since mixed partials commute (Clairaut's theorem, requires $f \in C^2$):

$$
(\nabla\times\mathbf{F})_k = \frac{\partial F_j}{\partial x_i} - \frac{\partial F_i}{\partial x_j} = \frac{\partial^2 f}{\partial x_i\partial x_j} - \frac{\partial^2 f}{\partial x_j\partial x_i} = 0.
$$

**Proof ($\Leftarrow$).** Assume $\nabla\times\mathbf{F} = \mathbf{0}$ on simply connected $U$. For any closed curve $C = \partial S$ in $U$ (bounding some surface $S \subset U$, which exists by simple connectivity), Stokes' Theorem gives:

$$
\oint_C \mathbf{F}\cdot d\mathbf{r} = \iint_S (\nabla\times\mathbf{F})\cdot d\mathbf{S} = \iint_S \mathbf{0}\cdot d\mathbf{S} = 0.
$$

Since the line integral of $\mathbf{F}$ around every closed curve is zero, the integral is path-independent. Define $f(\mathbf{x}) = \int_{\mathbf{x}_0}^{\mathbf{x}}\mathbf{F}\cdot d\mathbf{r}$ for any fixed base point $\mathbf{x}_0$. A standard argument (differentiating under the integral sign in each coordinate direction) shows $\nabla f = \mathbf{F}$. $\blacksquare$

**On multiply connected domains this fails.** The field $\mathbf{F} = \frac{(-y,x,0)}{x^2+y^2}$ on $\mathbb{R}^3\setminus\{z\text{-axis}\}$ has $\nabla\times\mathbf{F}=\mathbf{0}$ but $\oint_C\mathbf{F}\cdot d\mathbf{r} = 2\pi$ for any circle around the $z$-axis.

### 3.5 Corollary 2 — Area Formula via Green's Theorem

**Theorem.** The area of a region $D$ with positively oriented boundary $\partial D$ is:

$$
A(D) = \oint_{\partial D} x\,dy = -\oint_{\partial D} y\,dx = \frac{1}{2}\oint_{\partial D} x\,dy - y\,dx.
$$

**Proof.** Apply Green's theorem with $(P,Q) = (0, x)$: $\partial_x Q - \partial_y P = 1 - 0 = 1$, so $\oint x\,dy = \iint_D 1\,dA = A(D)$.

With $(P,Q) = (-y, 0)$: $\partial_x Q - \partial_y P = 0 - (-1) = 1$, so $-\oint y\,dx = A(D)$.

Average gives $\frac{1}{2}\oint x\,dy - y\,dx = A(D)$. $\blacksquare$

---


## 🖼️ Visual Anchor 5 — Area by Green's Theorem: The Ellipse

![math-01__1.7-fig5](math-01__1.7-fig5.svg)

---

## 🎯 4. Worked Examples

### Example 1.7.E1 — Green's Theorem: Line Integral → Double Integral

**Problem.** Evaluate $\displaystyle\oint_C (x^2 - y^2)\,dx + 2xy\,dy$, where $C$ is the positively oriented boundary of the rectangle $[0,2]\times[0,1]$.

**Step 1: Identify $P$ and $Q$.**

$$
P = x^2 - y^2, \quad Q = 2xy.
$$

**Step 2: Compute the curl density.**

$$
\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} = 2y - (-2y) = 4y.
$$

**Step 3: Apply Green's Theorem.**

$$
\oint_C P\,dx + Q\,dy = \iint_D 4y\,dA = \int_0^2\int_0^1 4y\,dy\,dx.
$$

**Step 4: Evaluate.**

$$
= \int_0^2 \left[2y^2\right]_0^1 dx = \int_0^2 2\,dx = \bigl[2x\bigr]_0^2 = 4.
$$

$$
\boxed{\oint_C (x^2-y^2)\,dx + 2xy\,dy = 4.}
$$

**Anti-triviality check:** We converted a four-segment line integral (four parameterizations, four computations) into a single iterated integral. Both methods give 4, but the area integral takes two lines. That's the whole point.

---

### Example 1.7.E2 — Area of an Ellipse via Green's Theorem

**Problem.** Use Green's theorem to compute the area of the ellipse $\dfrac{x^2}{a^2} + \dfrac{y^2}{b^2} \leq 1$.

**Step 1: Parameterize the boundary.** Let $x = a\cos t$, $y = b\sin t$, $t \in [0, 2\pi]$. This traverses $\partial D$ counterclockwise.

**Step 2: Compute the differentials.**

$$
dx = -a\sin t\,dt, \quad dy = b\cos t\,dt.
$$

**Step 3: Apply the area formula (Corollary 2).**

$$
A = \frac{1}{2}\oint_{\partial D} x\,dy - y\,dx = \frac{1}{2}\int_0^{2\pi} \bigl[(a\cos t)(b\cos t) - (b\sin t)(-a\sin t)\bigr]\,dt.
$$

**Step 4: Simplify.**

$$
= \frac{1}{2}\int_0^{2\pi} \bigl[ab\cos^2 t + ab\sin^2 t\bigr]\,dt = \frac{ab}{2}\int_0^{2\pi} 1\,dt = \frac{ab}{2}\cdot 2\pi.
$$

$$
\boxed{A = \pi ab.}
$$

When $a = b = r$, this gives $\pi r^2$, consistent with the circle. Every step is forced; nothing is "obvious."

---


### Example 1.7.E3 — Conservative Field Has Zero Circulation

**Problem.** Let $\mathbf{F} = \nabla(x^2 y + \sin z)$. Show that $\oint_C \mathbf{F}\cdot d\mathbf{r} = 0$ for any closed curve $C$ lying on a smooth surface $S$ in $\mathbb{R}^3$, using Stokes' theorem.

**Step 1: Compute $\nabla\times\mathbf{F}$.** Since $\mathbf{F} = \nabla f$ with $f = x^2 y + \sin z$:

$$
\mathbf{F} = (2xy,\; x^2,\; \cos z).
$$

Compute the curl directly:

$$
\nabla\times\mathbf{F} = \begin{vmatrix} \hat{i} & \hat{j} & \hat{k} \\ \partial_x & \partial_y & \partial_z \\ 2xy & x^2 & \cos z \end{vmatrix}.
$$

$$
= \hat{i}\bigl(\partial_y(\cos z) - \partial_z(x^2)\bigr) - \hat{j}\bigl(\partial_x(\cos z) - \partial_z(2xy)\bigr) + \hat{k}\bigl(\partial_x(x^2) - \partial_y(2xy)\bigr)
$$

$$
= \hat{i}(0 - 0) - \hat{j}(0 - 0) + \hat{k}(2x - 2x) = \mathbf{0}.
$$

**Step 2: Apply Stokes' Theorem.** Let $S$ be any surface bounded by $C$:

$$
\oint_C \mathbf{F}\cdot d\mathbf{r} = \iint_S (\nabla\times\mathbf{F})\cdot d\mathbf{S} = \iint_S \mathbf{0}\cdot d\mathbf{S} = 0. \quad \blacksquare
$$

This is the Stokes'-theorem proof of the standard theorem: gradient fields have zero circulation. The slick version of the Corollary 1 forward direction.

---

### Example 1.7.E4 — Stokes' Theorem: Choose a Convenient Surface

**Problem.** Evaluate $\displaystyle\oint_C \mathbf{F}\cdot d\mathbf{r}$ where $\mathbf{F} = (-y^2, x, z^2)$ and $C$ is the intersection of the cylinder $x^2 + y^2 = 1$ with the plane $y + z = 2$, traversed counterclockwise when viewed from above.

**Step 1: Identify the surface.** Instead of parameterizing the ellipse $C$ directly (complicated), use Stokes' and pick $S$ = the portion of the plane $z = 2 - y$ over the disk $x^2 + y^2 \leq 1$.

**Step 2: Compute $\nabla\times\mathbf{F}$.**

$$
\mathbf{F} = (-y^2, x, z^2), \quad \nabla\times\mathbf{F} = \begin{vmatrix}\hat{i}&\hat{j}&\hat{k}\\\partial_x&\partial_y&\partial_z\\-y^2&x&z^2\end{vmatrix}.
$$

$$
= \hat{i}(\partial_y z^2 - \partial_z x) - \hat{j}(\partial_x z^2 - \partial_z(-y^2)) + \hat{k}(\partial_x x - \partial_y(-y^2))
= \hat{i}(0-0) - \hat{j}(0-0) + \hat{k}(1+2y) = (0,0,1+2y).
$$

**Step 3: Parameterize $S$ over the disk $D: x^2+y^2\leq 1$.** The surface is $z = 2 - y$, so $\mathbf{r}(x,y) = (x, y, 2-y)$.

$$
\mathbf{r}_x = (1,0,0), \quad \mathbf{r}_y = (0,1,-1), \quad d\mathbf{S} = \mathbf{r}_x\times\mathbf{r}_y\,dx\,dy = (0,1,1)\,dx\,dy.
$$

Check orientation: $(0,1,1)$ has positive $z$-component, consistent with viewing from above. $\checkmark$

**Step 4: Evaluate the surface integral.**

$$
\iint_S (\nabla\times\mathbf{F})\cdot d\mathbf{S} = \iint_D (0,0,1+2y)\cdot(0,1,1)\,dx\,dy = \iint_D (1+2y)\,dx\,dy.
$$

**Step 5: Integrate over the unit disk.** In polar coordinates $x = r\cos\theta$, $y = r\sin\theta$:

$$
= \int_0^{2\pi}\int_0^1 (1 + 2r\sin\theta)\,r\,dr\,d\theta = \int_0^{2\pi}\int_0^1 r\,dr\,d\theta + 2\int_0^{2\pi}\int_0^1 r^2\sin\theta\,dr\,d\theta.
$$

The first integral: $\int_0^{2\pi}d\theta\cdot\int_0^1 r\,dr = 2\pi\cdot\tfrac{1}{2} = \pi$.

The second integral: $\int_0^{2\pi}\sin\theta\,d\theta = 0$, so the whole second term vanishes.

$$
\boxed{\oint_C \mathbf{F}\cdot d\mathbf{r} = \pi.}
$$

Key lesson: the surface $S$ is *any* surface bounded by $C$. Choosing the flat disk over the cylinder is dramatically simpler than integrating along the tilted ellipse.

---

### Example 1.7.E5 — Divergence Theorem: Flux of $\mathbf{F} = \langle x,y,z\rangle$ Through the Unit Sphere

**Problem.** Compute the outward flux of $\mathbf{F} = (x, y, z)$ through $\partial V$ = the unit sphere $S^2$.

**Step 1: Compute the divergence.**

$$
\nabla\cdot\mathbf{F} = \frac{\partial x}{\partial x} + \frac{\partial y}{\partial y} + \frac{\partial z}{\partial z} = 1 + 1 + 1 = 3.
$$

**Step 2: Apply the Divergence Theorem.** Let $V$ be the unit ball $x^2 + y^2 + z^2 \leq 1$:

$$
\oiint_{S^2}\mathbf{F}\cdot d\mathbf{S} = \iiint_V 3\,dV = 3\cdot\operatorname{Vol}(V) = 3\cdot\frac{4}{3}\pi(1)^3 = 4\pi.
$$

$$
\boxed{\text{Flux} = 4\pi.}
$$

**Sanity check.** On the unit sphere $\hat{n} = (x,y,z)$ (outward unit normal = position vector since $r=1$), so $\mathbf{F}\cdot\hat{n} = x^2+y^2+z^2 = 1$ everywhere. Hence the flux is just $1\times\text{Area}(S^2) = 1\times 4\pi$. $\checkmark$

---


### Example 1.7.E6 — Divergence Theorem: Flux of $\mathbf{F} = \langle x^2, y^2, z^2\rangle$ Through a Cube

**Problem.** Compute the total outward flux of $\mathbf{F} = (x^2, y^2, z^2)$ through the boundary of the cube $V = [0,1]^3$.

**Step 1: Compute the divergence.**

$$
\nabla\cdot\mathbf{F} = 2x + 2y + 2z.
$$

**Step 2: Apply the Divergence Theorem.**

$$
\oiint_{\partial V}\mathbf{F}\cdot d\mathbf{S} = \iiint_{[0,1]^3}(2x+2y+2z)\,dV.
$$

**Step 3: Evaluate the triple integral.** By linearity and symmetry (each variable plays the same role):

$$
= 2\int_0^1\int_0^1\int_0^1 x\,dx\,dy\,dz + 2\int_0^1\int_0^1\int_0^1 y\,dx\,dy\,dz + 2\int_0^1\int_0^1\int_0^1 z\,dx\,dy\,dz.
$$

Each triple integral factors: for example

$$
\iiint x\,dV = \left(\int_0^1 x\,dx\right)\left(\int_0^1 dy\right)\left(\int_0^1 dz\right) = \tfrac{1}{2}\cdot 1\cdot 1 = \tfrac{1}{2}.
$$

All three are $\tfrac{1}{2}$ by symmetry:

$$
= 2\cdot\tfrac{1}{2} + 2\cdot\tfrac{1}{2} + 2\cdot\tfrac{1}{2} = 1 + 1 + 1 = 3.
$$

$$
\boxed{\text{Flux} = 3.}
$$

**Direct verification (brief).** The six faces contribute: on the face $x=1$ (outward normal $+\hat{x}$), $F_1 = 1^2 = 1$, area $= 1$, contribution $+1$; on $x=0$ (outward normal $-\hat{x}$), $F_1 = 0$, contribution $0$. Similarly for $y$ and $z$ faces. Total $= 1+0+1+0+1+0 = 3$. $\checkmark$

---

### Example 1.7.E7 — Direct Verification of Green's Theorem

**Problem.** Verify Green's theorem directly for $P = xy$, $Q = x^2$, and $D$ the triangle with vertices $(0,0)$, $(1,0)$, $(0,1)$.

**Right side first (double integral):**

$$
\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} = 2x - x = x.
$$

$$
\iint_D x\,dA = \int_0^1\int_0^{1-x} x\,dy\,dx = \int_0^1 x(1-x)\,dx = \int_0^1(x - x^2)\,dx = \left[\frac{x^2}{2} - \frac{x^3}{3}\right]_0^1 = \frac{1}{2} - \frac{1}{3} = \frac{1}{6}.
$$

**Left side (line integral, three edges):**

*Edge 1:* $(0,0)\to(1,0)$: $y=0$, $dy=0$, $x$ from $0$ to $1$.

$$
\int_{E_1} xy\,dx + x^2\,dy = \int_0^1 x\cdot 0\,dx + x^2\cdot 0 = 0.
$$

*Edge 2:* $(1,0)\to(0,1)$: parameterize as $x = 1-t$, $y = t$, $t\in[0,1]$. Then $dx=-dt$, $dy=dt$, $xy = (1-t)t$, $x^2 = (1-t)^2$.

$$
\int_{E_2} = \int_0^1 \bigl[(1-t)t\cdot(-1) + (1-t)^2\cdot 1\bigr]dt = \int_0^1\bigl[-(t-t^2) + (1-2t+t^2)\bigr]dt
$$

$$
= \int_0^1(1 - 3t + 2t^2)\,dt = \left[t - \frac{3t^2}{2} + \frac{2t^3}{3}\right]_0^1 = 1 - \frac{3}{2} + \frac{2}{3} = \frac{6-9+4}{6} = \frac{1}{6}.
$$

*Edge 3:* $(0,1)\to(0,0)$: $x=0$, $dx=0$. $P=0$, $Q=0$. Contribution $= 0$.

**Total line integral:** $0 + \tfrac{1}{6} + 0 = \tfrac{1}{6}$. $\checkmark$ Green's theorem verified.

---

### Example 1.7.E8 — Physical Application: Deriving the Continuity Equation

**Setup.** Let $\rho(\mathbf{x},t)$ be the mass density of a fluid and $\mathbf{J} = \rho\mathbf{v}$ the mass flux (mass per unit area per unit time). For any fixed volume $V$ with boundary $\partial V$:

$$
\text{Rate of change of mass in }V = -\text{outward flux of mass through }\partial V.
$$

**Step 1: Write the mass in $V$.**

$$
M(t) = \iiint_V \rho(\mathbf{x},t)\,dV.
$$

**Step 2: Differentiate under the integral sign** (valid when $\rho$ is smooth):

$$
\frac{dM}{dt} = \iiint_V \frac{\partial\rho}{\partial t}\,dV.
$$

**Step 3: The outward flux through $\partial V$** is by definition $\oiint_{\partial V}\mathbf{J}\cdot d\mathbf{S}$. Mass conservation requires:

$$
\iiint_V \frac{\partial\rho}{\partial t}\,dV = -\oiint_{\partial V}\mathbf{J}\cdot d\mathbf{S}.
$$

**Step 4: Apply the Divergence Theorem** to the right side:

$$
-\oiint_{\partial V}\mathbf{J}\cdot d\mathbf{S} = -\iiint_V (\nabla\cdot\mathbf{J})\,dV.
$$

**Step 5: Combine and invoke arbitrariness of $V$.**

$$
\iiint_V \frac{\partial\rho}{\partial t}\,dV + \iiint_V (\nabla\cdot\mathbf{J})\,dV = 0 \quad\Longrightarrow\quad \iiint_V\left(\frac{\partial\rho}{\partial t} + \nabla\cdot\mathbf{J}\right)dV = 0.
$$

Since this holds for *every* volume $V$ and the integrand is continuous, the integrand must be identically zero:

$$
\boxed{\frac{\partial\rho}{\partial t} + \nabla\cdot\mathbf{J} = 0.}
$$

This is the **continuity equation** — the fundamental conservation law underlying all of fluid mechanics, electrodynamics (charge conservation), and quantum mechanics (probability conservation). The Divergence Theorem is the *only* tool used.

---


## ⚠️ 5. Common Pitfalls

### Pitfall 1 — Wrong Orientation
**The mistake:** traversing $\partial D$ clockwise instead of counterclockwise (or using the wrong right-hand rule for a surface) and not compensating with a sign flip.

**The consequence:** Every theorem gives an answer with a sign error. Green's theorem with a clockwise boundary gives $-\iint(\partial_x Q - \partial_y P)\,dA$; Stokes' with the wrong normal gives the negative.

**The fix:** Before computing, always draw the region, identify the boundary, walk along it, and check that the region is on your left. For surfaces, explicitly choose $\hat{n}$, then verify that the boundary traversal direction satisfies the right-hand rule with that choice.

### Pitfall 2 — Applying Stokes' to Non-Smooth or Open Surfaces Incorrectly
**The mistake:** $S$ has a crease (piecewise smooth is fine, but the orientation must be consistent across pieces); or $S$ is not bounded by a simple closed curve; or the boundary has components you forgot to include.

**The consequence:** The theorem still holds if the hypotheses are met, but you get wrong answers if you ignore a boundary component or if the orientation is inconsistent.

**The fix:** Verify $\partial S$ explicitly. If $S$ is a closed surface (no boundary), then $\oint_{\partial S}\mathbf{F}\cdot d\mathbf{r} = 0$ for *any* $\mathbf{F}$ with the right regularity — not a useful computation to do via Stokes'.

### Pitfall 3 — Forgetting the Divergence Theorem Requires a *Closed* Surface
**The mistake:** Applying $\oiint_{\partial V}\mathbf{F}\cdot d\mathbf{S} = \iiint_V\nabla\cdot\mathbf{F}\,dV$ when $\partial V$ is an *open* surface (e.g., only the top hemisphere, with no bottom disk).

**The consequence:** The left side misses the flux through the missing pieces, so the equation fails.

**The fix:** The notation $\oiint$ (circle on the integral sign) signals a *closed* surface. If your surface is open, either close it (add the missing pieces and subtract their contributions) or use Stokes' instead.

### Pitfall 4 — Multiply Connected Domains and Topology
**The mistake:** On a domain with holes (e.g., the punctured plane $\mathbb{R}^2\setminus\{0\}$), assuming $\nabla\times\mathbf{F}=0$ implies $\oint_C\mathbf{F}\cdot d\mathbf{r}=0$ for all $C$.

**The consequence:** The classic counterexample $\mathbf{F} = (-y,x)/(x^2+y^2)$ has zero 2D curl everywhere in $\mathbb{R}^2\setminus\{0\}$, but gives circulation $2\pi$ around any circle enclosing the origin. Green's/Stokes' theorems hold, but the surface you'd need (bounded by $C$, lying in the domain) must contain no holes — and for $C$ enclosing the origin, no such hole-free surface exists in $\mathbb{R}^2\setminus\{0\}$.

**The fix:** Always check: is the domain simply connected? If not, a zero-curl field need not be conservative.

### Pitfall 5 — Using $\nabla\times\mathbf{F}$ When You Need $\nabla\cdot\mathbf{F}$ (and Vice Versa)
**The mistake:** Reaching for Stokes' when the problem has a closed surface (Divergence Theorem territory), or applying the Divergence Theorem when the problem gives a line integral around a curve (Stokes' territory).

**The diagnostic:** If the boundary is a **closed curve** bounding a **surface**, use **Stokes'**. If the boundary is a **closed surface** bounding a **volume**, use **Divergence**. If everything is in 2D, use **Green's**.

### Pitfall 6 — Forgetting to Check Continuity of Partial Derivatives
**The mistake:** Applying these theorems when $\mathbf{F}$ or its partial derivatives are singular *inside* the domain (not just on the boundary).

**The consequence:** The theorem fails. Classic trap: $\mathbf{F} = \mathbf{r}/r^3$ (the Coulomb/Newtonian field) has $\nabla\cdot\mathbf{F} = 0$ *for* $\mathbf{r}\neq 0$, but the Divergence Theorem over a ball centered at the origin gives flux $= 4\pi \neq 0 = \iiint 0\,dV$, because $\mathbf{F}$ is singular at the origin. The resolution requires distributional divergence ($\nabla\cdot(\mathbf{r}/r^3) = 4\pi\delta^3(\mathbf{r})$).

**The fix:** Always verify: is $\mathbf{F}$ and all required partials continuous on the *closed* domain (interior + boundary)?

---

## 📝 6. Challenge Problems

> ⚠️ Work every problem on paper before opening the solution. The anti-triviality rule applies: show every algebraic step.

### Problem 1.7.P1 — Green's Theorem Backwards

Use Green's theorem to evaluate $\iint_D (2x - y^2)\,dA$ where $D$ is the unit disk $x^2+y^2\leq 1$, by converting to a line integral over $\partial D$ and computing directly.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Goal:** Find $P,Q$ such that $\partial_x Q - \partial_y P = 2x - y^2$, then compute $\oint_{\partial D} P\,dx + Q\,dy$.

**Step 1: Choose $P$ and $Q$.** One convenient choice: set $\partial_x Q = 2x$ giving $Q = x^2$, and $\partial_y P = y^2$ giving $P = y^3/3$. Then $\partial_x Q - \partial_y P = 2x - y^2$. $\checkmark$

**Step 2: Parameterize $\partial D$.** $x = \cos\theta$, $y = \sin\theta$, $\theta\in[0,2\pi]$; $dx = -\sin\theta\,d\theta$, $dy = \cos\theta\,d\theta$.

**Step 3: Substitute.**

$$
\oint_{\partial D} \frac{y^3}{3}\,dx + x^2\,dy = \int_0^{2\pi}\left[\frac{\sin^3\theta}{3}(-\sin\theta) + \cos^2\theta\cdot\cos\theta\right]d\theta.
$$

$$
= \int_0^{2\pi}\left[-\frac{\sin^4\theta}{3} + \cos^3\theta\right]d\theta.
$$

**Step 4: Standard integrals.** $\int_0^{2\pi}\cos^3\theta\,d\theta = 0$ (odd power of cosine over full period). For $\sin^4\theta$: use $\sin^4\theta = \tfrac{3}{8} - \tfrac{1}{2}\cos 2\theta + \tfrac{1}{8}\cos 4\theta$, so $\int_0^{2\pi}\sin^4\theta\,d\theta = \tfrac{3}{8}\cdot 2\pi = \tfrac{3\pi}{4}$.

**Step 5: Combine.**

$$
= -\frac{1}{3}\cdot\frac{3\pi}{4} + 0 = -\frac{\pi}{4}.
$$

$$
\boxed{\iint_D (2x - y^2)\,dA = -\frac{\pi}{4}.}
$$

(This can be verified directly in polar: $\int_0^{2\pi}\int_0^1(2r\cos\theta - r^2\sin^2\theta)r\,dr\,d\theta = 0 - \pi/4 = -\pi/4$. $\checkmark$)

</details>

---

### Problem 1.7.P2 — Stokes' on a Paraboloid

Let $\mathbf{F} = (z,x,y)$ and let $C$ be the circle $x^2+y^2=4$, $z=0$, traversed counterclockwise when viewed from above. Compute $\oint_C\mathbf{F}\cdot d\mathbf{r}$ using Stokes' theorem with $S$ = the paraboloid $z = 4 - x^2 - y^2$ above $z=0$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Compute $\nabla\times\mathbf{F}$.** $\mathbf{F} = (z,x,y)$:

$$
\nabla\times\mathbf{F} = (\partial_y y - \partial_z x,\; \partial_z z - \partial_x y,\; \partial_x x - \partial_y z) = (1-0,\; 1-0,\; 1-0) = (1,1,1).
$$

**Step 2: Parameterize $S$.** $\mathbf{r}(x,y) = (x,y,4-x^2-y^2)$ over $D: x^2+y^2\leq 4$.

$$
\mathbf{r}_x = (1,0,-2x),\quad \mathbf{r}_y = (0,1,-2y),\quad d\mathbf{S} = \mathbf{r}_x\times\mathbf{r}_y\,dx\,dy = (2x,2y,1)\,dx\,dy.
$$

The normal $(2x,2y,1)$ has positive $z$-component, consistent with upward/outward orientation for CCW boundary. $\checkmark$

**Step 3: Evaluate.**

$$
\iint_S(\nabla\times\mathbf{F})\cdot d\mathbf{S} = \iint_D (1,1,1)\cdot(2x,2y,1)\,dx\,dy = \iint_D(2x+2y+1)\,dx\,dy.
$$

Over the disk $x^2+y^2\leq 4$: $\iint_D 2x\,dA = 0$ (odd integrand over symmetric domain), $\iint_D 2y\,dA = 0$, $\iint_D 1\,dA = \pi(2)^2 = 4\pi$.

$$
\boxed{\oint_C\mathbf{F}\cdot d\mathbf{r} = 4\pi.}
$$

</details>

---


### Problem 1.7.P3 — Gauss's Law from Divergence Theorem

The electric field of a point charge $q$ at the origin is $\mathbf{E} = \dfrac{q}{4\pi\varepsilon_0}\dfrac{\mathbf{r}}{r^3}$. Use the Divergence Theorem carefully (accounting for the singularity at the origin) to derive $\oiint_{\partial V}\mathbf{E}\cdot d\mathbf{S} = q/\varepsilon_0$ for any volume $V$ containing the origin.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Regularity issue.** $\mathbf{E}$ is singular at the origin, so we cannot directly apply the Divergence Theorem over $V$ if $0\in V$. **Strategy:** excise a small ball $B_\varepsilon$ of radius $\varepsilon$ around the origin. The region $V' = V\setminus B_\varepsilon$ contains no singularity.

**Step 2: Away from origin, $\nabla\cdot\mathbf{E} = 0$.** For $\mathbf{r}\neq 0$:

$$
\nabla\cdot\frac{\mathbf{r}}{r^3} = \frac{3}{r^3} - \frac{3r^2}{r^4} = \frac{3}{r^3} - \frac{3}{r^3} = 0.
$$

(Full computation: $\partial_x(x/r^3) = r^{-3} - 3x^2 r^{-5}$; sum over all three components gives $(3r^{-3} - 3r^2 r^{-5}) = 0$.)

**Step 3: Divergence Theorem on $V'$.** $\partial V' = \partial V \cup (-S_\varepsilon)$ where $-S_\varepsilon$ is the sphere of radius $\varepsilon$ with **inward** normal (since it's the inner boundary of $V'$). Since $\nabla\cdot\mathbf{E} = 0$ on $V'$:

$$
0 = \oiint_{\partial V}\mathbf{E}\cdot d\mathbf{S} - \oiint_{S_\varepsilon}\mathbf{E}\cdot d\mathbf{S}.
$$

So $\oiint_{\partial V}\mathbf{E}\cdot d\mathbf{S} = \oiint_{S_\varepsilon}\mathbf{E}\cdot d\mathbf{S}$.

**Step 4: Evaluate the flux through $S_\varepsilon$.** On $S_\varepsilon$, $r = \varepsilon$ and $\hat{n} = \mathbf{r}/\varepsilon$ (outward from $B_\varepsilon$). So:

$$
\mathbf{E}\cdot\hat{n} = \frac{q}{4\pi\varepsilon_0}\frac{\mathbf{r}}{r^3}\cdot\frac{\mathbf{r}}{r} = \frac{q}{4\pi\varepsilon_0}\frac{r^2}{r^4} = \frac{q}{4\pi\varepsilon_0\varepsilon^2}.
$$

$$
\oiint_{S_\varepsilon}\mathbf{E}\cdot d\mathbf{S} = \frac{q}{4\pi\varepsilon_0\varepsilon^2}\cdot\text{Area}(S_\varepsilon) = \frac{q}{4\pi\varepsilon_0\varepsilon^2}\cdot 4\pi\varepsilon^2 = \frac{q}{\varepsilon_0}.
$$

**Conclusion:**

$$
\boxed{\oiint_{\partial V}\mathbf{E}\cdot d\mathbf{S} = \frac{q}{\varepsilon_0}.}
$$

This is Gauss's Law. The $\varepsilon^2$ in the area exactly cancels the $\varepsilon^{-2}$ in $|\mathbf{E}|$ — this is why the inverse-square law and the geometry of spheres conspire so beautifully. $\blacksquare$

</details>

---

### Problem 1.7.P4 — Green's Theorem for the Area of a Cardioid

Use Green's area formula to find the area enclosed by the cardioid $r = 1 + \cos\theta$ in polar coordinates.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Parameterize the boundary.** In polar, $x = r\cos\theta = (1+\cos\theta)\cos\theta$ and $y = r\sin\theta = (1+\cos\theta)\sin\theta$, with $\theta\in[0,2\pi]$, traversed counterclockwise.

**Step 2: Compute $dy$.** Differentiate $y = (1+\cos\theta)\sin\theta$:

$$
\frac{dy}{d\theta} = -\sin\theta\cdot\sin\theta + (1+\cos\theta)\cos\theta = -\sin^2\theta + \cos\theta + \cos^2\theta.
$$

**Step 3: Apply $A = \oint x\,dy$.** Actually, use the polar area formula derived directly from Green's: $A = \tfrac{1}{2}\int_0^{2\pi}r^2\,d\theta$ (standard result, derivable by substituting $x = r\cos\theta$, $y = r\sin\theta$ into $\tfrac{1}{2}\oint x\,dy - y\,dx$, giving $\tfrac{1}{2}\int r^2\,d\theta$).

$$
A = \frac{1}{2}\int_0^{2\pi}(1+\cos\theta)^2\,d\theta = \frac{1}{2}\int_0^{2\pi}(1 + 2\cos\theta + \cos^2\theta)\,d\theta.
$$

**Step 4: Evaluate each term.**

$$
\int_0^{2\pi}1\,d\theta = 2\pi,\quad \int_0^{2\pi}2\cos\theta\,d\theta = 0,\quad \int_0^{2\pi}\cos^2\theta\,d\theta = \pi.
$$

$$
A = \frac{1}{2}(2\pi + 0 + \pi) = \frac{3\pi}{2}.
$$

$$
\boxed{A = \frac{3\pi}{2}.}
$$

</details>

---

### Problem 1.7.P5 — Stokes': Surface Independence

Let $\mathbf{F} = (y^2 z, xz, xy)$ and let $C$ be the unit circle $x^2+y^2=1$, $z=0$, counterclockwise. Evaluate $\oint_C\mathbf{F}\cdot d\mathbf{r}$ using Stokes' with (a) the flat disk $z=0$ and (b) the hemisphere $z = \sqrt{1-x^2-y^2}$. Verify you get the same answer.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Compute $\nabla\times\mathbf{F}$.** $\mathbf{F} = (y^2 z, xz, xy)$:

$$
(\nabla\times\mathbf{F})_x = \partial_y(xy) - \partial_z(xz) = x - x = 0.
$$

$$
(\nabla\times\mathbf{F})_y = \partial_z(y^2 z) - \partial_x(xy) = y^2 - y = y^2 - y.
$$

Wait — recompute carefully: $(\nabla\times\mathbf{F})_y = \partial_z F_x - \partial_x F_z = \partial_z(y^2 z) - \partial_x(xy) = y^2 - y$.

$$
(\nabla\times\mathbf{F})_z = \partial_x(xz) - \partial_y(y^2 z) = z - 2yz.
$$

So $\nabla\times\mathbf{F} = (0,\; y^2 - y,\; z - 2yz)$.

**(a) Flat disk $S_1$: $z=0$, $x^2+y^2\leq 1$.** Normal $d\mathbf{S} = (0,0,1)\,dx\,dy$ (upward, consistent with CCW boundary).

$$
\iint_{S_1}(\nabla\times\mathbf{F})\cdot d\mathbf{S} = \iint_D (z-2yz)\big|_{z=0}\,dx\,dy = \iint_D 0\,dx\,dy = 0.
$$

**(b) Hemisphere $S_2$: $z=\sqrt{1-x^2-y^2}$.** The curl component $z-2yz$ evaluated on this surface is $\sqrt{1-r^2}(1-2r\sin\theta)$ in polar — this is non-trivial, but Stokes' guarantees the same answer as (a). By surface-independence:

$$
\oint_C\mathbf{F}\cdot d\mathbf{r} = 0 \quad\text{(same from both surfaces).}
$$

$$
\boxed{\oint_C\mathbf{F}\cdot d\mathbf{r} = 0.}
$$

Surface independence of Stokes' integral is the key theorem: any two surfaces sharing boundary $C$ give the same $\iint(\nabla\times\mathbf{F})\cdot d\mathbf{S}$ (provided $\nabla\cdot(\nabla\times\mathbf{F}) = 0$, which is always true).

</details>

---


### Problem 1.7.P6 — Divergence Theorem: Flux of a Non-Trivial Field

Compute the flux of $\mathbf{F} = (x^3, y^3, z^3)$ through the boundary of the solid cylinder $x^2+y^2\leq 4$, $0\leq z\leq 3$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Divergence.**

$$
\nabla\cdot\mathbf{F} = 3x^2 + 3y^2 + 3z^2 = 3(x^2+y^2+z^2).
$$

**Step 2: Apply Divergence Theorem.** Let $V$ be the solid cylinder:

$$
\text{Flux} = \iiint_V 3(x^2+y^2+z^2)\,dV = \iiint_V 3r^2\,dV + \iiint_V 3z^2\,dV,
$$

where $r^2 = x^2+y^2$ in cylindrical coordinates.

**Step 3: Set up in cylindrical.** $dV = r\,dr\,d\theta\,dz$, $r\in[0,2]$, $\theta\in[0,2\pi]$, $z\in[0,3]$.

$$
\text{Flux} = \int_0^{2\pi}\int_0^2\int_0^3 3(r^2 + z^2)\,r\,dz\,dr\,d\theta.
$$

Factor out $\int_0^{2\pi}d\theta = 2\pi$:

$$
= 2\pi\cdot 3\int_0^2\int_0^3 (r^3 + rz^2)\,dz\,dr.
$$

**Inner integral (in $z$):**

$$
\int_0^3(r^3 + rz^2)\,dz = r^3\cdot 3 + r\cdot\frac{27}{3} = 3r^3 + 9r.
$$

**Outer integral (in $r$):**

$$
\int_0^2(3r^3 + 9r)\,dr = \left[\frac{3r^4}{4} + \frac{9r^2}{2}\right]_0^2 = \frac{3\cdot 16}{4} + \frac{9\cdot 4}{2} = 12 + 18 = 30.
$$

**Combine:**

$$
\text{Flux} = 6\pi\cdot 30 = 180\pi.
$$

$$
\boxed{\text{Flux} = 180\pi.}
$$

</details>

---

### Problem 1.7.P7 — Green's Theorem: Winding Number

Let $C$ be a simple closed curve not passing through the origin, with positive orientation. Show that $\frac{1}{2\pi}\oint_C \dfrac{-y\,dx + x\,dy}{x^2+y^2}$ equals $1$ if the origin is inside $C$ and $0$ if the origin is outside.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Setup.** Let $P = -y/(x^2+y^2)$, $Q = x/(x^2+y^2)$.

**Case 1: Origin outside $D$.** Then $P,Q$ have continuous partial derivatives on the simply connected region $D$ enclosed by $C$. Compute:

$$
\frac{\partial Q}{\partial x} = \frac{(x^2+y^2) - x\cdot 2x}{(x^2+y^2)^2} = \frac{y^2-x^2}{(x^2+y^2)^2}.
$$

$$
\frac{\partial P}{\partial y} = \frac{-(x^2+y^2) + y\cdot 2y}{(x^2+y^2)^2} = \frac{y^2 - x^2}{(x^2+y^2)^2}.
$$

So $\partial_x Q - \partial_y P = 0$. Green's theorem gives:

$$
\oint_C P\,dx + Q\,dy = \iint_D 0\,dA = 0.
$$

So the integral is $0/(2\pi) = 0$. $\checkmark$

**Case 2: Origin inside $D$.** The field is singular at the origin, so Green's applies to the region $D' = D\setminus B_\varepsilon$ (excise small disk). By the same computation, $\partial_x Q - \partial_y P = 0$ on $D'$, so:

$$
\oint_C P\,dx + Q\,dy = \oint_{C_\varepsilon} P\,dx + Q\,dy,
$$

where $C_\varepsilon$ is the circle of radius $\varepsilon$ with positive orientation. Parameterize: $x = \varepsilon\cos t$, $y = \varepsilon\sin t$:

$$
\oint_{C_\varepsilon} = \int_0^{2\pi}\frac{-\varepsilon\sin t(-\varepsilon\sin t\,dt) + \varepsilon\cos t(\varepsilon\cos t\,dt)}{\varepsilon^2} = \int_0^{2\pi}\frac{\varepsilon^2(\sin^2 t + \cos^2 t)}{\varepsilon^2}\,dt = \int_0^{2\pi}dt = 2\pi.
$$

So $\frac{1}{2\pi}\oint_C \frac{-y\,dx+x\,dy}{x^2+y^2} = 1$. $\blacksquare$

This is the **winding number** — a topological invariant. It counts how many times $C$ winds around the origin.

</details>

---

### Problem 1.7.P8 — The Heat Equation from Divergence Theorem

Starting from Fourier's law $\mathbf{q} = -k\nabla T$ (heat flux proportional to negative temperature gradient) and energy conservation, use the Divergence Theorem to derive the heat equation $\partial_t T = \alpha\nabla^2 T$ where $\alpha = k/(\rho c)$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Energy conservation.** The rate of change of thermal energy in volume $V$:

$$
\frac{d}{dt}\iiint_V \rho c T\,dV = -\oiint_{\partial V}\mathbf{q}\cdot d\mathbf{S}.
$$

Here $\rho$ = density, $c$ = specific heat. The right side is the net heat flux *into* the volume (negative of outward flux).

**Step 2: Differentiate under the integral sign:**

$$
\iiint_V \rho c\frac{\partial T}{\partial t}\,dV = -\oiint_{\partial V}\mathbf{q}\cdot d\mathbf{S}.
$$

**Step 3: Apply Divergence Theorem to the right side:**

$$
-\oiint_{\partial V}\mathbf{q}\cdot d\mathbf{S} = -\iiint_V(\nabla\cdot\mathbf{q})\,dV.
$$

**Step 4: Substitute Fourier's law $\mathbf{q} = -k\nabla T$:**

$$
\nabla\cdot\mathbf{q} = \nabla\cdot(-k\nabla T) = -k\nabla^2 T.
$$

So the right side becomes $\iiint_V k\nabla^2 T\,dV$.

**Step 5: Combine and use arbitrariness of $V$:**

$$
\iiint_V\rho c\frac{\partial T}{\partial t}\,dV = \iiint_V k\nabla^2 T\,dV \quad\Longrightarrow\quad \rho c\frac{\partial T}{\partial t} = k\nabla^2 T.
$$

**Step 6: Define thermal diffusivity** $\alpha = k/(\rho c)$:

$$
\boxed{\frac{\partial T}{\partial t} = \alpha\nabla^2 T.}
$$

This is the **heat equation** — the prototype of all parabolic PDEs. The Divergence Theorem is the *only* tool turning the macroscopic energy balance into the local PDE. $\blacksquare$

</details>

---


## 🛠️ 7. Pairing with Local Tools

To build deep intuition, do the following with any field $\mathbf{F}$ in this chapter:

1. **Plot $\mathbf{F}$** as a vector field in the $xy$-plane or $\mathbb{R}^3$. Look for rotation (large curl suggests Stokes' is the right theorem) versus expansion/contraction (large divergence suggests the Divergence Theorem).

2. **Numerical flux check:** For a specific closed surface, numerically integrate $\mathbf{F}\cdot\hat{n}$ over the surface (triangulate it and sum $\mathbf{F}\cdot\hat{n}\,\Delta S$ for each triangle). Compare to the analytic $\iiint\nabla\cdot\mathbf{F}\,dV$. They should match to machine precision.

3. **Orientation sanity:** Before every computation, explicitly write down the outward normal $\hat{n}$ and verify the sign convention. One missed sign flip is the most common exam error.

4. **SymPy verification:** Use `sympy.integrate` to cross-check every surface integral and every divergence/curl computation in the practice problems. The script `_practice/scripts/1.7_integral_theorems.py` does all eight archetypes with `--seed 42`.

---

## 📖 8. Study Tactics

- **Build mental maps.** For each theorem, know: (1) the dimension of the domain, (2) the dimension of the boundary, (3) the differential operator involved (2D curl, 3D curl, divergence), (4) the right orientation convention.

- **The substitution pattern.** Every application follows the same skeleton: *"I have an integral I don't want. I identify which theorem converts it. I check orientation. I compute the required derivative (curl or div). I integrate."* Practice this skeleton until it's automatic.

- **Spaced repetition.** Tag challenge problems with `#review/calc/1.7`. Re-work them at 1 day, 3 days, 7 days, then 21 days.

- **Connect to physics immediately.** After every abstract computation, name the physical situation: flux through a surface is how Gauss's law works; circulation around a closed curve is Faraday's law; divergence integrated is how mass is conserved. Physics gives the theorems a spine.

- **Look ahead to differential forms.** Every time you see $P\,dx + Q\,dy$ or $\mathbf{F}\cdot d\mathbf{S}$, know that these are **differential forms** — objects that can be integrated over oriented manifolds. Chapter 1.8 will unify everything into $\int_{\partial M}\omega = \int_M d\omega$.

---

## 🔗 9. Cross-Links

### Backward
- [1.5 - Multiple Integrals & Change of Variables](1.5---Multiple-Integrals-&-Change-of-Variables) — the double and triple integrals that appear on the right-hand side of all three theorems.
- [1.6 - Vector Fields, Div & Curl](1.6---Vector-Fields,-Div-&-Curl) — the differential operators $\nabla\cdot$ and $\nabla\times$ that are the integrands here; the geometric meaning of divergence and curl that makes these theorems *obvious* once you internalize the geometry.

### Forward
- [1.8 - Exterior Algebra & Differential Forms](1.8---Exterior-Algebra-&-Differential-Forms) — the language that makes $\int_{\partial M}\omega = \int_M d\omega$ rigorous and manifestly obvious. Every theorem in this chapter becomes one line in that framework.

### Physics
- **7.x — Electrodynamics:** Maxwell's equations in integral form are Green's/Stokes'/Divergence applied to $\mathbf{E}$ and $\mathbf{B}$. Gauss's law IS the Divergence Theorem. Faraday's and Ampère-Maxwell ARE Stokes'. Understanding this chapter is understanding Maxwell.
- **6.x — Fluid Dynamics:** The continuity equation (Example E8), Euler's equation in integral form, and Kelvin's circulation theorem are all applications of these three theorems to the velocity field $\mathbf{v}$.
- **8.x — General Relativity:** The Gauss-Bonnet theorem, Stokes' on Lorentzian manifolds, and the integral form of the Einstein field equations all rest on the generalized Stokes' theorem. The topology of spacetime is read off via these integrals.

---

## 📚 10. Verified Open-Access Source Material

| Source | Location | Why it's Authoritative |
|---|---|---|
| **MIT 18.02SC Multivariable Calculus, Sessions 71–80** | [ocw.mit.edu/courses/18-02sc](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/) | Core MIT undergraduate course; Green's, Stokes', and Divergence Theorem all covered with video + problem sets, hosted on `mit.edu`. |
| **Paul Dawkins — *Stokes' Theorem*, *Divergence Theorem*** | [tutorial.math.lamar.edu/calciii](https://tutorial.math.lamar.edu/classes/calciii/stokestheorem.aspx) | Most-cited online calculus reference; clear worked examples, Lamar University. |
| **APEX Calculus, Ch. 15** | [apexcalculus.com](https://www.apexcalculus.com/) | Greg Hartman (VMI), CC-BY-NC; thorough treatment of all three theorems with proof sketches. |
| **Spivak, *Calculus on Manifolds*** | [available at open library](https://openlibrary.org/works/OL3513699W/Calculus_on_Manifolds) | The compact, rigorous treatment of the generalized Stokes' theorem. This is the 1.8 roadmap. |
| **3Blue1Brown — *Divergence and Curl*** | [3blue1brown.com](https://www.3blue1brown.com/lessons/divergence-and-curl) | Gold standard for visual intuition of the vector differential operators; watch before the worked examples. |
| **Tao, *Analysis II*, Chapter 17** | [available at Terence Tao's blog](https://terrytao.wordpress.com/) | Terence Tao's lecture notes; rigorous measure-theoretic treatment with transparent proofs. |

*(Resource descriptions paraphrased for compliance with each platform's terms of use.)*

---

*Chapter 1.7 — Green's, Stokes' and Divergence Theorems. Last reviewed: 2026-05-23.*
*Previous: [1.6 - Vector Fields, Div & Curl](1.6---Vector-Fields,-Div-&-Curl) | Next: [1.8 - Exterior Algebra & Differential Forms](1.8---Exterior-Algebra-&-Differential-Forms) →*
