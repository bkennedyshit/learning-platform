---
title: "Newtonian Dynamics Conservation Laws"
subject: "Classical Mechanics & Dynamical Systems"
catalog: advanced
audience_tier: higher-education
chapter: "4.1"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 4.1 — Newtonian Dynamics & Conservation Laws

> *"If I have seen further, it is by standing on the shoulders of Giants."* — Isaac Newton, 1675

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. State Newton's three laws of motion in their most general (momentum) form.
2. Derive the work-energy theorem from Newton's second law.
3. Prove conservation of linear momentum from translational symmetry.
4. Prove conservation of angular momentum from rotational symmetry.
5. Prove conservation of mechanical energy for conservative forces.
6. Apply these conservation laws to solve multi-body collision and orbital problems.
7. Distinguish conservative from non-conservative forces using the curl criterion.
8. Formulate equations of motion in Cartesian, polar, and curvilinear coordinates.

---


## 🖼️ Visual Anchor — Forces, Momentum & Energy Conservation

![math-04__4.1-fig1](math-04__4.1-fig1.svg)

---


## 📚 1. Definitions

### Definition 4.1.1 — Inertial Reference Frame

An **inertial reference frame** is a coordinate system in which a body subject to zero net force moves with constant velocity (including zero). Newton's laws hold in their standard form only within inertial frames. Any frame moving at constant velocity relative to an inertial frame is itself inertial.

### Definition 4.1.2 — Linear Momentum

The **linear momentum** of a particle of mass $m$ moving with velocity $\mathbf{v}$ is:

$$
\mathbf{p} = m\mathbf{v}.
$$

For a system of $N$ particles, the total momentum is $\mathbf{P} = \sum_{i=1}^{N} m_i \mathbf{v}_i$.

### Definition 4.1.3 — Force

A **force** $\mathbf{F}$ is the time rate of change of momentum:

$$
\mathbf{F} = \frac{d\mathbf{p}}{dt} = \frac{d(m\mathbf{v})}{dt}.
$$

For constant mass, this reduces to $\mathbf{F} = m\mathbf{a}$ where $\mathbf{a} = d\mathbf{v}/dt$ is the acceleration.

### Definition 4.1.4 — Angular Momentum

The **angular momentum** of a particle about a point $O$ is:

$$
\mathbf{L} = \mathbf{r} \times \mathbf{p} = \mathbf{r} \times m\mathbf{v},
$$

where $\mathbf{r}$ is the position vector from $O$ to the particle.

### Definition 4.1.5 — Torque

The **torque** (moment of force) about point $O$ is:

$$
\boldsymbol{\tau} = \mathbf{r} \times \mathbf{F}.
$$

### Definition 4.1.6 — Kinetic Energy

The **kinetic energy** of a particle is:

$$
T = \frac{1}{2}m|\mathbf{v}|^2 = \frac{|\mathbf{p}|^2}{2m}.
$$

### Definition 4.1.7 — Conservative Force and Potential Energy

A force $\mathbf{F}$ is **conservative** if there exists a scalar field $U(\mathbf{r})$ (the potential energy) such that:

$$
\mathbf{F} = -\nabla U = -\left(\frac{\partial U}{\partial x}\hat{\mathbf{x}} + \frac{\partial U}{\partial y}\hat{\mathbf{y}} + \frac{\partial U}{\partial z}\hat{\mathbf{z}}\right).
$$

Equivalently, $\mathbf{F}$ is conservative if and only if $\nabla \times \mathbf{F} = \mathbf{0}$ everywhere in a simply-connected domain.

### Definition 4.1.8 — Work

The **work** done by force $\mathbf{F}$ along a path $\mathcal{C}$ from $A$ to $B$ is:

$$
W_{A\to B} = \int_{\mathcal{C}} \mathbf{F} \cdot d\mathbf{r}.
$$

For a conservative force: $W_{A\to B} = U(A) - U(B) = -\Delta U$.

### Definition 4.1.9 — Center of Mass

For a system of $N$ particles with total mass $M = \sum_i m_i$:

$$
\mathbf{R}_{\text{cm}} = \frac{1}{M}\sum_{i=1}^{N} m_i \mathbf{r}_i.
$$

---


## 📐 2. Axioms / Postulates

### Axiom 4.1.A1 — Newton's First Law (Law of Inertia)

In an inertial reference frame, a body remains at rest or in uniform rectilinear motion unless acted upon by a net external force. Mathematically:

$$
\mathbf{F}_{\text{net}} = \mathbf{0} \implies \frac{d\mathbf{v}}{dt} = \mathbf{0} \implies \mathbf{v} = \text{const}.
$$

This law defines the existence of inertial frames and establishes that force is required to change the state of motion.

### Axiom 4.1.A2 — Newton's Second Law (Equation of Motion)

In an inertial frame, the net force on a body equals the time rate of change of its momentum:

$$
\mathbf{F}_{\text{net}} = \frac{d\mathbf{p}}{dt} = \frac{d(m\mathbf{v})}{dt}.
$$

For constant mass: $\mathbf{F}_{\text{net}} = m\mathbf{a}$. This is a second-order ODE for the position $\mathbf{r}(t)$.

### Axiom 4.1.A3 — Newton's Third Law (Action-Reaction)

If body $A$ exerts a force $\mathbf{F}_{AB}$ on body $B$, then body $B$ exerts a force $\mathbf{F}_{BA}$ on body $A$ such that:

$$
\mathbf{F}_{AB} = -\mathbf{F}_{BA}.
$$

The forces are equal in magnitude, opposite in direction, and act along the line connecting the two bodies (strong form). This guarantees conservation of total momentum for isolated systems.

### Axiom 4.1.A4 — Superposition of Forces

When multiple forces act on a body, the net force is the vector sum:

$$
\mathbf{F}_{\text{net}} = \sum_{i=1}^{N} \mathbf{F}_i.
$$

Forces combine linearly; there is no "saturation" or nonlinear coupling at the Newtonian level.

---


## 🛡️ 3. Lemmas

### Lemma 4.1.1 — Torque as Rate of Change of Angular Momentum

For a particle of constant mass:

$$
\boldsymbol{\tau} = \frac{d\mathbf{L}}{dt}.
$$

**Proof.** Compute the time derivative of $\mathbf{L} = \mathbf{r} \times \mathbf{p}$ using the product rule for cross products:

$$
\frac{d\mathbf{L}}{dt} = \frac{d\mathbf{r}}{dt} \times \mathbf{p} + \mathbf{r} \times \frac{d\mathbf{p}}{dt}.
$$

The first term: $\frac{d\mathbf{r}}{dt} \times \mathbf{p} = \mathbf{v} \times m\mathbf{v} = m(\mathbf{v} \times \mathbf{v}) = \mathbf{0}$ since the cross product of any vector with itself vanishes.

The second term: $\mathbf{r} \times \frac{d\mathbf{p}}{dt} = \mathbf{r} \times \mathbf{F} = \boldsymbol{\tau}$.

Therefore $\frac{d\mathbf{L}}{dt} = \boldsymbol{\tau}$. $\blacksquare$

### Lemma 4.1.2 — Work-Energy Relation (Differential Form)

The differential work done by the net force equals the differential change in kinetic energy:

$$
\mathbf{F}_{\text{net}} \cdot d\mathbf{r} = dT.
$$

**Proof.** Start from $\mathbf{F}_{\text{net}} = m\mathbf{a} = m\frac{d\mathbf{v}}{dt}$. Dot both sides with $d\mathbf{r} = \mathbf{v}\,dt$:

$$
\mathbf{F}_{\text{net}} \cdot d\mathbf{r} = m\frac{d\mathbf{v}}{dt} \cdot \mathbf{v}\,dt = m\,\mathbf{v} \cdot d\mathbf{v}.
$$

Now expand $d(|\mathbf{v}|^2) = d(\mathbf{v}\cdot\mathbf{v}) = 2\,\mathbf{v}\cdot d\mathbf{v}$, so $\mathbf{v}\cdot d\mathbf{v} = \frac{1}{2}d(v^2)$. Therefore:

$$
\mathbf{F}_{\text{net}} \cdot d\mathbf{r} = m \cdot \frac{1}{2}d(v^2) = d\left(\frac{1}{2}mv^2\right) = dT. \quad \blacksquare
$$

### Lemma 4.1.3 — Center of Mass Motion

The center of mass of a system moves as if all external forces act on a single particle of mass $M$ located at $\mathbf{R}_{\text{cm}}$:

$$
M\ddot{\mathbf{R}}_{\text{cm}} = \mathbf{F}_{\text{ext}}.
$$

**Proof.** Sum Newton's second law over all particles: $\sum_i \mathbf{F}_i = \sum_i m_i \ddot{\mathbf{r}}_i$. The left side splits into external and internal forces. By Newton's third law, internal forces cancel pairwise: $\sum_{i\neq j}\mathbf{F}_{ij} = \mathbf{0}$. The right side: $\sum_i m_i \ddot{\mathbf{r}}_i = M\ddot{\mathbf{R}}_{\text{cm}}$ by definition of center of mass. $\blacksquare$

### Lemma 4.1.4 — Curl-Free Implies Path Independence

If $\nabla \times \mathbf{F} = \mathbf{0}$ in a simply-connected domain, then $\oint_{\mathcal{C}} \mathbf{F}\cdot d\mathbf{r} = 0$ for every closed curve $\mathcal{C}$, and there exists a scalar potential $U$ with $\mathbf{F} = -\nabla U$.

**Proof.** By Stokes' theorem: $\oint_{\mathcal{C}} \mathbf{F}\cdot d\mathbf{r} = \iint_S (\nabla\times\mathbf{F})\cdot d\mathbf{S} = 0$ for any surface $S$ bounded by $\mathcal{C}$. Path independence follows: for any two paths from $A$ to $B$, the integrals are equal. Define $U(\mathbf{r}) = -\int_{\mathbf{r}_0}^{\mathbf{r}} \mathbf{F}\cdot d\mathbf{r}'$ (path-independent). Then $\mathbf{F} = -\nabla U$. $\blacksquare$

---


## 👑 4. Theorems

### Theorem 4.1.1 — Conservation of Linear Momentum

If the net external force on a system of particles is zero, the total linear momentum is conserved:

$$
\mathbf{F}_{\text{ext}} = \mathbf{0} \implies \mathbf{P} = \sum_{i} m_i \mathbf{v}_i = \text{const}.
$$

### Theorem 4.1.2 — Conservation of Angular Momentum

If the net external torque on a system about a point $O$ is zero, the total angular momentum about $O$ is conserved:

$$
\boldsymbol{\tau}_{\text{ext}} = \mathbf{0} \implies \mathbf{L} = \sum_{i} \mathbf{r}_i \times m_i\mathbf{v}_i = \text{const}.
$$

### Theorem 4.1.3 — Conservation of Mechanical Energy

If all forces acting on a system are conservative (derivable from potentials), the total mechanical energy is conserved:

$$
E = T + U = \text{const}, \quad \text{where } T = \sum_i \frac{1}{2}m_i v_i^2, \quad U = \sum_i U_i(\mathbf{r}_i) + \sum_{i<j} U_{ij}(|\mathbf{r}_i - \mathbf{r}_j|).
$$

### Theorem 4.1.4 — Work-Energy Theorem (Integral Form)

The net work done on a particle as it moves from $A$ to $B$ equals the change in kinetic energy:

$$
W_{\text{net}} = \int_A^B \mathbf{F}_{\text{net}} \cdot d\mathbf{r} = T_B - T_A = \Delta T.
$$

### Theorem 4.1.5 — Virial Theorem (Time-Averaged)

For a bounded system of particles with positions $\mathbf{r}_i$ and forces $\mathbf{F}_i$, the time-averaged kinetic energy satisfies:

$$
\langle T \rangle = -\frac{1}{2}\left\langle \sum_i \mathbf{F}_i \cdot \mathbf{r}_i \right\rangle.
$$

For power-law potentials $U \propto r^n$: $\langle T \rangle = \frac{n}{2}\langle U \rangle$. For gravity ($n=-1$): $\langle T \rangle = -\frac{1}{2}\langle U \rangle$.

---


## ✍️ 5. Proofs / Derivations

### 5.1 Proof of Theorem 4.1.1 — Conservation of Linear Momentum

**Proof.** Consider a system of $N$ particles. Newton's second law for particle $i$:

$$
\frac{d\mathbf{p}_i}{dt} = \mathbf{F}_i^{\text{ext}} + \sum_{j \neq i} \mathbf{F}_{ji},
$$

where $\mathbf{F}_{ji}$ is the internal force on $i$ due to $j$. Sum over all particles:

$$
\frac{d}{dt}\sum_{i=1}^N \mathbf{p}_i = \sum_{i=1}^N \mathbf{F}_i^{\text{ext}} + \sum_{i=1}^N \sum_{j \neq i} \mathbf{F}_{ji}.
$$

By Newton's third law, $\mathbf{F}_{ji} = -\mathbf{F}_{ij}$. In the double sum, each pair $(i,j)$ contributes $\mathbf{F}_{ji} + \mathbf{F}_{ij} = \mathbf{0}$. Therefore:

$$
\frac{d\mathbf{P}}{dt} = \mathbf{F}_{\text{ext}}.
$$

If $\mathbf{F}_{\text{ext}} = \mathbf{0}$, then $\frac{d\mathbf{P}}{dt} = \mathbf{0}$, so $\mathbf{P} = \text{const}$. $\blacksquare$

### 5.2 Proof of Theorem 4.1.2 — Conservation of Angular Momentum

**Proof.** The total angular momentum is $\mathbf{L} = \sum_i \mathbf{r}_i \times \mathbf{p}_i$. Differentiate:

$$
\frac{d\mathbf{L}}{dt} = \sum_i \left(\dot{\mathbf{r}}_i \times \mathbf{p}_i + \mathbf{r}_i \times \dot{\mathbf{p}}_i\right).
$$

The first term in each summand: $\dot{\mathbf{r}}_i \times \mathbf{p}_i = \mathbf{v}_i \times m_i\mathbf{v}_i = m_i(\mathbf{v}_i \times \mathbf{v}_i) = \mathbf{0}$.

The second term: $\mathbf{r}_i \times \dot{\mathbf{p}}_i = \mathbf{r}_i \times \left(\mathbf{F}_i^{\text{ext}} + \sum_{j\neq i}\mathbf{F}_{ji}\right)$.

So:

$$
\frac{d\mathbf{L}}{dt} = \sum_i \mathbf{r}_i \times \mathbf{F}_i^{\text{ext}} + \sum_i \sum_{j\neq i} \mathbf{r}_i \times \mathbf{F}_{ji}.
$$

The first sum is $\boldsymbol{\tau}_{\text{ext}}$. For the double sum, pair the terms $(i,j)$ and $(j,i)$:

$$
\mathbf{r}_i \times \mathbf{F}_{ji} + \mathbf{r}_j \times \mathbf{F}_{ij} = \mathbf{r}_i \times \mathbf{F}_{ji} + \mathbf{r}_j \times (-\mathbf{F}_{ji}) = (\mathbf{r}_i - \mathbf{r}_j) \times \mathbf{F}_{ji}.
$$

Under the strong form of Newton's third law, $\mathbf{F}_{ji}$ acts along $(\mathbf{r}_i - \mathbf{r}_j)$, so $(\mathbf{r}_i - \mathbf{r}_j) \times \mathbf{F}_{ji} = \mathbf{0}$. Therefore:

$$
\frac{d\mathbf{L}}{dt} = \boldsymbol{\tau}_{\text{ext}}.
$$

If $\boldsymbol{\tau}_{\text{ext}} = \mathbf{0}$, then $\mathbf{L} = \text{const}$. $\blacksquare$

### 5.3 Proof of Theorem 4.1.3 — Conservation of Mechanical Energy

**Proof.** For a single particle under a conservative force $\mathbf{F} = -\nabla U$:

$$
\frac{dT}{dt} = \mathbf{F} \cdot \mathbf{v} = (-\nabla U) \cdot \mathbf{v}.
$$

The time derivative of potential energy along the particle's trajectory, using the chain rule:

$$
\frac{dU}{dt} = \frac{\partial U}{\partial x}\frac{dx}{dt} + \frac{\partial U}{\partial y}\frac{dy}{dt} + \frac{\partial U}{\partial z}\frac{dz}{dt} = \nabla U \cdot \mathbf{v}.
$$

Therefore:

$$
\frac{dT}{dt} = -\nabla U \cdot \mathbf{v} = -\frac{dU}{dt}.
$$

Rearranging:

$$
\frac{d}{dt}(T + U) = 0 \implies E = T + U = \text{const}. \quad \blacksquare
$$

### 5.4 Proof of Theorem 4.1.4 — Work-Energy Theorem

**Proof.** Integrate Lemma 4.1.2 along the path from $A$ to $B$:

$$
W_{\text{net}} = \int_A^B \mathbf{F}_{\text{net}} \cdot d\mathbf{r} = \int_A^B dT = T_B - T_A. \quad \blacksquare
$$

### 5.5 Derivation of the Virial Theorem

**Proof.** Define the virial function $G = \sum_i \mathbf{p}_i \cdot \mathbf{r}_i$. Differentiate:

$$
\frac{dG}{dt} = \sum_i \dot{\mathbf{p}}_i \cdot \mathbf{r}_i + \sum_i \mathbf{p}_i \cdot \dot{\mathbf{r}}_i.
$$

The second sum: $\sum_i \mathbf{p}_i \cdot \dot{\mathbf{r}}_i = \sum_i m_i \mathbf{v}_i \cdot \mathbf{v}_i = \sum_i m_i v_i^2 = 2T$.

The first sum: $\sum_i \dot{\mathbf{p}}_i \cdot \mathbf{r}_i = \sum_i \mathbf{F}_i \cdot \mathbf{r}_i$.

So $\frac{dG}{dt} = 2T + \sum_i \mathbf{F}_i \cdot \mathbf{r}_i$.

Time-average over a period $\tau$:

$$
\frac{1}{\tau}\int_0^\tau \frac{dG}{dt}\,dt = \frac{G(\tau) - G(0)}{\tau} = 2\langle T\rangle + \left\langle\sum_i \mathbf{F}_i \cdot \mathbf{r}_i\right\rangle.
$$

For a bounded system, $G$ remains finite, so as $\tau \to \infty$ the left side vanishes:

$$
0 = 2\langle T\rangle + \left\langle\sum_i \mathbf{F}_i \cdot \mathbf{r}_i\right\rangle \implies \langle T\rangle = -\frac{1}{2}\left\langle\sum_i \mathbf{F}_i \cdot \mathbf{r}_i\right\rangle. \quad \blacksquare
$$

### 5.6 Derivation — Equations of Motion in Polar Coordinates

Starting from Cartesian coordinates $(x,y)$ with $x = r\cos\theta$, $y = r\sin\theta$:

**Velocity components.** Differentiate:

$$
\dot{x} = \dot{r}\cos\theta - r\dot\theta\sin\theta, \quad \dot{y} = \dot{r}\sin\theta + r\dot\theta\cos\theta.
$$

The unit vectors in polar coordinates are $\hat{\mathbf{r}} = (\cos\theta, \sin\theta)$ and $\hat{\boldsymbol{\theta}} = (-\sin\theta, \cos\theta)$. Therefore:

$$
\mathbf{v} = \dot{r}\hat{\mathbf{r}} + r\dot\theta\,\hat{\boldsymbol{\theta}}.
$$

**Acceleration components.** Differentiate $\mathbf{v}$, noting $\frac{d\hat{\mathbf{r}}}{dt} = \dot\theta\,\hat{\boldsymbol{\theta}}$ and $\frac{d\hat{\boldsymbol{\theta}}}{dt} = -\dot\theta\,\hat{\mathbf{r}}$:

$$
\mathbf{a} = \frac{d}{dt}\left(\dot{r}\hat{\mathbf{r}} + r\dot\theta\,\hat{\boldsymbol{\theta}}\right).
$$

Expand using the product rule on each term:

$$
\mathbf{a} = \ddot{r}\hat{\mathbf{r}} + \dot{r}\dot\theta\,\hat{\boldsymbol{\theta}} + \dot{r}\dot\theta\,\hat{\boldsymbol{\theta}} + r\ddot\theta\,\hat{\boldsymbol{\theta}} + r\dot\theta(-\dot\theta\,\hat{\mathbf{r}}).
$$

Collecting radial ($\hat{\mathbf{r}}$) and tangential ($\hat{\boldsymbol{\theta}}$) components:

$$
\mathbf{a} = \left(\ddot{r} - r\dot\theta^2\right)\hat{\mathbf{r}} + \left(r\ddot\theta + 2\dot{r}\dot\theta\right)\hat{\boldsymbol{\theta}}.
$$

Newton's second law in polar form: $F_r = m(\ddot{r} - r\dot\theta^2)$ and $F_\theta = m(r\ddot\theta + 2\dot{r}\dot\theta)$.

Note: $F_\theta = m \cdot \frac{1}{r}\frac{d}{dt}(r^2\dot\theta)$, connecting directly to angular momentum $L = mr^2\dot\theta$.

---


## 🧮 6. Worked Examples

### Example 4.1.1 — Elastic Collision in One Dimension

**Problem:** A ball of mass $m_1 = 2\text{ kg}$ moving at $v_1 = 5\text{ m/s}$ collides elastically with a stationary ball of mass $m_2 = 3\text{ kg}$. Find the final velocities $v_1'$ and $v_2'$.

<details>
<summary>🔍 Full Solution</summary>

**Step 1: Conservation of momentum.**

$$
m_1 v_1 + m_2 \cdot 0 = m_1 v_1' + m_2 v_2'
$$

$$
2(5) = 2v_1' + 3v_2' \implies 10 = 2v_1' + 3v_2'. \tag{1}
$$

**Step 2: Conservation of kinetic energy (elastic collision).**

$$
\frac{1}{2}m_1 v_1^2 = \frac{1}{2}m_1 v_1'^2 + \frac{1}{2}m_2 v_2'^2
$$

$$
2(25) = 2v_1'^2 + 3v_2'^2 \implies 50 = 2v_1'^2 + 3v_2'^2. \tag{2}
$$

**Step 3: Use the relative velocity relation for elastic collisions.**

For a 1D elastic collision, the relative velocity reverses: $v_1 - v_2 = -(v_1' - v_2')$. Since $v_2 = 0$:

$$
5 = v_2' - v_1'. \tag{3}
$$

**Step 4: Solve the system.** From (3): $v_1' = v_2' - 5$. Substitute into (1):

$$
10 = 2(v_2' - 5) + 3v_2' = 2v_2' - 10 + 3v_2' = 5v_2' - 10.
$$

$$
5v_2' = 20 \implies v_2' = 4 \text{ m/s}.
$$

$$
v_1' = 4 - 5 = -1 \text{ m/s}.
$$

**Step 5: Verify.** Momentum: $2(-1) + 3(4) = -2 + 12 = 10$ ✓. Energy: $2(1) + 3(16) = 2 + 48 = 50$ ✓.

**Result:** $v_1' = -1$ m/s (bounces back), $v_2' = 4$ m/s (moves forward).

</details>

### Example 4.1.2 — Atwood Machine

**Problem:** Two masses $m_1 > m_2$ are connected by a massless, inextensible string over a frictionless pulley. Find the acceleration $a$ and string tension $T$.

<details>
<summary>🔍 Full Solution</summary>

**Step 1: Free body diagrams.** For mass $m_1$ (heavier, accelerates down): $m_1 g - T = m_1 a$. For mass $m_2$ (lighter, accelerates up): $T - m_2 g = m_2 a$.

**Step 2: Add the two equations to eliminate $T$:**

$$
m_1 g - T + T - m_2 g = m_1 a + m_2 a
$$

$$
(m_1 - m_2)g = (m_1 + m_2)a.
$$

**Step 3: Solve for acceleration:**

$$
a = \frac{(m_1 - m_2)}{(m_1 + m_2)}g.
$$

**Step 4: Solve for tension.** Substitute $a$ back into the equation for $m_2$:

$$
T = m_2(g + a) = m_2 g\left(1 + \frac{m_1 - m_2}{m_1 + m_2}\right) = m_2 g \cdot \frac{2m_1}{m_1 + m_2} = \frac{2m_1 m_2 g}{m_1 + m_2}.
$$

**Step 5: Check limiting cases.**
- $m_1 = m_2$: $a = 0$, $T = mg$ (static equilibrium) ✓.
- $m_1 \gg m_2$: $a \to g$, $T \to 2m_2 g$ (light mass accelerates at $g$) ✓.

</details>

### Example 4.1.3 — Projectile with Air Resistance

**Problem:** A particle of mass $m$ is launched vertically upward with speed $v_0$ in a medium with linear drag $\mathbf{F}_{\text{drag}} = -b\mathbf{v}$. Find $v(t)$ during ascent.

<details>
<summary>🔍 Full Solution</summary>

**Step 1: Equation of motion.** Taking upward as positive during ascent ($v \gt  0$):

$$
m\frac{dv}{dt} = -mg - bv.
$$

Both gravity and drag oppose the upward motion.

**Step 2: Separate variables.**

$$
\frac{dv}{-mg - bv} = \frac{dt}{m}.
$$

Let $u = mg + bv$, then $du = b\,dv$, so $dv = du/b$:

$$
\frac{du}{-u \cdot b} = \frac{dt}{m} \implies \frac{du}{u} = -\frac{b}{m}dt.
$$

**Step 3: Integrate both sides.** With initial condition $v(0) = v_0$, so $u(0) = mg + bv_0$:

$$
\ln\left(\frac{u}{u_0}\right) = -\frac{b}{m}t \implies u = u_0 \, e^{-bt/m}.
$$

$$
mg + bv = (mg + bv_0)e^{-bt/m}.
$$

**Step 4: Solve for $v(t)$:**

$$
v(t) = \frac{(mg + bv_0)e^{-bt/m} - mg}{b} = \left(v_0 + \frac{mg}{b}\right)e^{-bt/m} - \frac{mg}{b}.
$$

Define the terminal speed $v_T = mg/b$:

$$
v(t) = (v_0 + v_T)e^{-gt/v_T} - v_T.
$$

**Step 5: Find time to reach maximum height.** Set $v = 0$:

$$
(v_0 + v_T)e^{-gt^*/v_T} = v_T \implies t^* = \frac{v_T}{g}\ln\left(\frac{v_0 + v_T}{v_T}\right).
$$

</details>

### Example 4.1.4 — Two-Body Central Force Reduction

**Problem:** Show that the two-body gravitational problem reduces to an equivalent one-body problem with reduced mass $\mu$.

<details>
<summary>🔍 Full Solution</summary>

**Step 1: Equations of motion for two bodies.**

$$
m_1 \ddot{\mathbf{r}}_1 = \mathbf{F}_{12}, \quad m_2 \ddot{\mathbf{r}}_2 = \mathbf{F}_{21} = -\mathbf{F}_{12}.
$$

**Step 2: Define relative coordinate $\mathbf{r} = \mathbf{r}_1 - \mathbf{r}_2$ and center of mass $\mathbf{R} = \frac{m_1\mathbf{r}_1 + m_2\mathbf{r}_2}{M}$.**

From Step 1: $\ddot{\mathbf{r}}_1 = \mathbf{F}_{12}/m_1$ and $\ddot{\mathbf{r}}_2 = -\mathbf{F}_{12}/m_2$.

**Step 3: Compute $\ddot{\mathbf{r}}$:**

$$
\ddot{\mathbf{r}} = \ddot{\mathbf{r}}_1 - \ddot{\mathbf{r}}_2 = \frac{\mathbf{F}_{12}}{m_1} + \frac{\mathbf{F}_{12}}{m_2} = \mathbf{F}_{12}\left(\frac{1}{m_1} + \frac{1}{m_2}\right) = \frac{\mathbf{F}_{12}}{\mu},
$$

where the **reduced mass** is:

$$
\mu = \frac{m_1 m_2}{m_1 + m_2}.
$$

**Step 4: Equivalent one-body equation:**

$$
\mu\ddot{\mathbf{r}} = \mathbf{F}_{12}(\mathbf{r}).
$$

This is the equation of motion for a single particle of mass $\mu$ at position $\mathbf{r}$ under force $\mathbf{F}_{12}$. The center of mass moves freely: $M\ddot{\mathbf{R}} = \mathbf{0}$ (no external forces).

</details>

---


## 🔗 7. Cross-links & Further Reading

### Internal Links
- **Next chapter:** [4.2 - Variational Calculus & Hamilton's Principle](4.2---Variational-Calculus-&-Hamilton's-Principle) — reformulates mechanics via the action principle
- **Polar coordinates & curvilinear systems:** [1.4 - Vector Calculus](1.4---Vector-Calculus) for gradient, divergence, curl in general coordinates
- **Eigenvalue methods for coupled oscillators:** [2.6 - Eigenvalues Eigenvectors & Diagonalization](2.6---Eigenvalues-Eigenvectors-&-Diagonalization) — normal mode analysis requires solving $\det(K - \omega^2 M) = 0$
- **Differential equations of motion:** [3.1 - First-Order ODEs & Separable Equations](3.1---First-Order-ODEs-&-Separable-Equations) for solving $m\dot{v} = F(v,t)$
- **Central forces (detailed):** [4.4 - Central Forces & Keplerian Orbits](4.4---Central-Forces-&-Keplerian-Orbits)

### External Resources
- **Leonard Susskind**, *The Theoretical Minimum: Classical Mechanics* (Stanford lectures) — physical intuition for states and phase space
- **Herbert Goldstein**, *Classical Mechanics*, Ch. 1 — the definitive graduate treatment of Newtonian mechanics
- **Feynman Lectures on Physics**, Vol. I, Ch. 9–15 — masterful conceptual exposition of Newton's laws
- **MIT OCW 8.01** — Walter Lewin's demonstrations of conservation laws

---

*Next: [4.2 - Variational Calculus & Hamilton's Principle](4.2---Variational-Calculus-&-Hamilton's-Principle) →*



---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — Two-Dimensional Elastic Collision (Billiard Problem)

**Problem:** A billiard ball of mass $m$ moving at speed $v_0$ along the $x$-axis strikes an identical stationary ball. After the collision, the first ball deflects at angle $\theta_1 = 30°$ above the $x$-axis. Find the speeds and direction of both balls after the collision, assuming a perfectly elastic collision.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Set up conservation equations

Since the masses are equal ($m_1 = m_2 = m$), we can divide through by $m$. Let $v_1'$ and $v_2'$ be the final speeds, with $\theta_1 = 30°$ and $\theta_2$ the deflection angle of ball 2 below the $x$-axis.

**Conservation of $x$-momentum:**

$$
v_0 = v_1'\cos\theta_1 + v_2'\cos\theta_2.
$$

**Conservation of $y$-momentum:**

$$
0 = v_1'\sin\theta_1 - v_2'\sin\theta_2.
$$

**Conservation of kinetic energy (elastic):**

$$
v_0^2 = v_1'^2 + v_2'^2.
$$

#### Step 2: Use the equal-mass elastic collision theorem

For equal-mass elastic collisions, there is a powerful geometric result: the final velocity vectors are perpendicular, i.e., $\theta_1 + \theta_2 = 90°$. 

**Proof:** Square the momentum equation $\mathbf{v}_0 = \mathbf{v}_1' + \mathbf{v}_2'$:

$$
v_0^2 = v_1'^2 + v_2'^2 + 2\mathbf{v}_1'\cdot\mathbf{v}_2'.
$$

But energy conservation gives $v_0^2 = v_1'^2 + v_2'^2$. Therefore:

$$
2\mathbf{v}_1'\cdot\mathbf{v}_2' = 0 \implies \mathbf{v}_1' \perp \mathbf{v}_2'.
$$

So $\theta_2 = 90° - 30° = 60°$.

#### Step 3: Solve for the speeds

From $y$-momentum: $v_1'\sin 30° = v_2'\sin 60°$, so:

$$
v_1'\cdot\frac{1}{2} = v_2'\cdot\frac{\sqrt{3}}{2} \implies v_1' = \sqrt{3}\,v_2'.
$$

Substitute into energy conservation:

$$
v_0^2 = 3v_2'^2 + v_2'^2 = 4v_2'^2 \implies v_2' = \frac{v_0}{2}.
$$

$$
v_1' = \sqrt{3}\cdot\frac{v_0}{2} = \frac{\sqrt{3}}{2}v_0.
$$

#### Step 4: Verify with $x$-momentum

$$
v_1'\cos 30° + v_2'\cos 60° = \frac{\sqrt{3}}{2}v_0\cdot\frac{\sqrt{3}}{2} + \frac{v_0}{2}\cdot\frac{1}{2} = \frac{3v_0}{4} + \frac{v_0}{4} = v_0. \quad \checkmark
$$

**Final Answer:**

$$
v_1' = \frac{\sqrt{3}}{2}v_0 \approx 0.866\,v_0 \text{ at } 30° \text{ above } x\text{-axis}
$$

$$
v_2' = \frac{v_0}{2} \text{ at } 60° \text{ below } x\text{-axis}
$$

</details>

### Example 8.2 — Variable-Mass Rocket (Tsiolkovsky Equation)

**Problem:** A rocket of initial mass $M_0$ (including fuel) expels exhaust at constant speed $v_e$ relative to the rocket. Derive the rocket equation and find the final speed when the fuel mass fraction is $f = m_{\text{fuel}}/M_0 = 0.9$ (starting from rest in free space, no gravity).

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Set up the momentum balance

At time $t$, the rocket has mass $M(t)$ and velocity $v(t)$. In a small time $dt$, it ejects mass $|dM|$ (note $dM \lt  0$) at velocity $(v - v_e)$ in the lab frame.

**Total momentum before:** $M v$.

**Total momentum after:** $(M + dM)(v + dv) + |dM|(v - v_e)$.

Since $|dM| = -dM$, the momentum after is:

$$
(M + dM)(v + dv) + (-dM)(v - v_e).
$$

#### Step 2: Apply conservation of momentum (no external forces)

$$
Mv = (M + dM)(v + dv) - dM(v - v_e).
$$

Expand the right side:

$$
= Mv + M\,dv + v\,dM + dM\,dv - v\,dM + v_e\,dM.
$$

Cancel $Mv$ from both sides and drop the second-order term $dM\,dv$:

$$
0 = M\,dv + v_e\,dM.
$$

#### Step 3: Separate and integrate

$$
dv = -v_e\frac{dM}{M}.
$$

Integrate from initial state $(v = 0, M = M_0)$ to final state $(v = v_f, M = M_f)$:

$$
\int_0^{v_f} dv = -v_e\int_{M_0}^{M_f}\frac{dM}{M}.
$$

$$
v_f = -v_e\left[\ln M\right]_{M_0}^{M_f} = -v_e(\ln M_f - \ln M_0) = v_e\ln\frac{M_0}{M_f}.
$$

This is the **Tsiolkovsky rocket equation**:

$$
\Delta v = v_e \ln\frac{M_0}{M_f}.
$$

#### Step 4: Numerical evaluation

With fuel fraction $f = 0.9$: $M_f = M_0(1-f) = 0.1\,M_0$. Therefore:

$$
v_f = v_e\ln\frac{M_0}{0.1\,M_0} = v_e\ln 10 \approx 2.303\,v_e.
$$

For a chemical rocket with $v_e \approx 3000$ m/s: $v_f \approx 6909$ m/s.

#### Step 5: Physical interpretation

The logarithmic dependence is devastating for space travel — to double $\Delta v$, you must square the mass ratio. This is the fundamental reason multi-stage rockets are necessary (see [10.3](10.3) for Hohmann transfer $\Delta v$ requirements).

**Final Answer:**

$$
\Delta v = v_e \ln\frac{M_0}{M_f} = v_e\ln 10 \approx 2.303\,v_e
$$

</details>

### Example 8.3 — Work-Energy Theorem with Position-Dependent Force

**Problem:** A particle of mass $m$ moves along the $x$-axis under a force $F(x) = F_0(1 - x/L)$ for $0 \leq x \leq L$, starting from rest at $x = 0$. Find the speed at $x = L$ and the maximum speed.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Apply the work-energy theorem

$$
W = \int_0^x F(x')\,dx' = \Delta KE = \frac{1}{2}mv^2 - 0.
$$

$$
\frac{1}{2}mv^2 = \int_0^x F_0\left(1 - \frac{x'}{L}\right)dx' = F_0\left[x' - \frac{x'^2}{2L}\right]_0^x = F_0\left(x - \frac{x^2}{2L}\right).
$$

Therefore:

$$
v(x) = \sqrt{\frac{2F_0}{m}\left(x - \frac{x^2}{2L}\right)}.
$$

#### Step 2: Speed at $x = L$

$$
v(L) = \sqrt{\frac{2F_0}{m}\left(L - \frac{L^2}{2L}\right)} = \sqrt{\frac{2F_0}{m}\cdot\frac{L}{2}} = \sqrt{\frac{F_0 L}{m}}.
$$

#### Step 3: Find maximum speed

The speed is maximized when $v^2(x)$ is maximized, i.e., when $\frac{d}{dx}\left(x - \frac{x^2}{2L}\right) = 0$:

$$
1 - \frac{x}{L} = 0 \implies x = L.
$$

Wait — this gives $x = L$, but let's check the second derivative: $-1/L \lt  0$, confirming a maximum. However, note that $F(L) = 0$, so the force vanishes at $x = L$. The particle accelerates throughout $[0, L]$ (since $F \gt  0$ for $x \lt  L$), reaching maximum speed exactly at $x = L$.

Alternatively, maximum speed occurs where $F = 0$ (acceleration changes sign), which is at $x = L$. So:

$$
v_{\max} = v(L) = \sqrt{\frac{F_0 L}{m}}.
$$

#### Step 4: Verify dimensions

$[F_0 L/m] = \text{N}\cdot\text{m}/\text{kg} = \text{m}^2/\text{s}^2$. Taking the square root gives m/s. ✓

**Final Answer:**

$$
v_{\max} = v(L) = \sqrt{\frac{F_0 L}{m}}
$$

</details>

### Example 8.4 — Inelastic Collision and Energy Loss (Ballistic Pendulum)

**Problem:** A bullet of mass $m = 10$ g traveling at $v_0 = 400$ m/s embeds in a wooden block of mass $M = 2$ kg suspended as a pendulum. Find (a) the velocity immediately after impact, (b) the maximum height the block rises, and (c) the fraction of kinetic energy lost.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Perfectly inelastic collision (momentum conservation)

During the collision, external forces (gravity, string tension) act over a negligibly short time interval, so impulse from them is negligible. Momentum is conserved:

$$
mv_0 = (m + M)V.
$$

$$
V = \frac{mv_0}{m+M} = \frac{0.010 \times 400}{0.010 + 2.0} = \frac{4.0}{2.01} = 1.99 \text{ m/s}.
$$

#### Step 2: Maximum height (energy conservation after collision)

After the collision, the bullet+block system swings upward. Now energy is conserved (no non-conservative forces during the swing):

$$
\frac{1}{2}(m+M)V^2 = (m+M)gh.
$$

$$
h = \frac{V^2}{2g} = \frac{(1.99)^2}{2(9.81)} = \frac{3.96}{19.62} = 0.202 \text{ m} \approx 20.2 \text{ cm}.
$$

#### Step 3: Energy loss fraction

Initial KE: $K_i = \frac{1}{2}mv_0^2 = \frac{1}{2}(0.010)(400)^2 = 800$ J.

Final KE (just after collision): $K_f = \frac{1}{2}(m+M)V^2 = \frac{1}{2}(2.01)(1.99)^2 = 3.98$ J.

Fraction lost:

$$
\frac{K_i - K_f}{K_i} = \frac{800 - 3.98}{800} = 0.995 = 99.5\%.
$$

#### Step 4: General formula for energy loss in perfectly inelastic collision

$$
\frac{\Delta K}{K_i} = \frac{M}{m + M}.
$$

Check: $\frac{2.0}{2.01} = 0.995$. ✓

This dramatic energy loss (converted to heat, deformation, sound) is why inelastic collisions are so different from elastic ones.

**Final Answer:**

$$
V = 1.99 \text{ m/s}, \quad h = 20.2 \text{ cm}, \quad \text{Energy lost} = 99.5\%
$$

</details>

---

## 📘 9. Appendix: Extended Derivations & Special Cases

### 9.1 Derivation of the Impulse-Momentum Theorem from Newton's Second Law

The impulse-momentum theorem is the integrated form of Newton's second law. We derive it carefully, showing how it applies to both constant and variable forces.

**Starting point:** Newton's second law in its most general form:

$$
\mathbf{F}_{\text{net}} = \frac{d\mathbf{p}}{dt},
$$

where $\mathbf{p} = m\mathbf{v}$ (for constant mass).

**Step 1: Integrate both sides over a time interval $[t_1, t_2]$:**

$$
\int_{t_1}^{t_2} \mathbf{F}_{\text{net}}\,dt = \int_{t_1}^{t_2} \frac{d\mathbf{p}}{dt}\,dt.
$$

**Step 2: The right side is a perfect differential:**

$$
\int_{t_1}^{t_2} \frac{d\mathbf{p}}{dt}\,dt = \mathbf{p}(t_2) - \mathbf{p}(t_1) = \Delta\mathbf{p}.
$$

**Step 3: Define the impulse:**

$$
\mathbf{J} \equiv \int_{t_1}^{t_2} \mathbf{F}_{\text{net}}\,dt = \Delta\mathbf{p}.
$$

This is the **impulse-momentum theorem**: the net impulse equals the change in momentum.

**Special case — constant force:** If $\mathbf{F}_{\text{net}}$ is constant over $[t_1, t_2]$:

$$
\mathbf{J} = \mathbf{F}_{\text{net}}\cdot\Delta t = \Delta\mathbf{p}.
$$

**Special case — collision (variable force, short duration):** During a collision lasting time $\Delta t$, the force $F(t)$ may be enormous but brief. The average force is:

$$
\bar{F} = \frac{1}{\Delta t}\int_{t_1}^{t_2} F\,dt = \frac{\Delta p}{\Delta t}.
$$

This is why airbags work: by increasing $\Delta t$, they reduce $\bar{F}$ for the same $\Delta p$.

**Connection to the work-energy theorem:** While impulse-momentum relates force and time to momentum change, the work-energy theorem relates force and displacement to energy change:

$$
W = \int \mathbf{F}\cdot d\mathbf{r} = \Delta KE.
$$

These are complementary tools: use impulse-momentum when you know the time of interaction; use work-energy when you know the displacement. For collisions where internal forces are unknown, momentum conservation (from impulse-momentum applied to the system) is typically the only viable approach.

*References: Goldstein §1.1; Feynman Lectures Vol. I, Ch. 9–10; MIT 8.01 Lecture 15.*

### 9.2 The Work-Energy Theorem: Rigorous Derivation for Variable Mass

For a system with variable mass (e.g., a rocket or a conveyor belt), the naive $F = ma$ form breaks down. Here we derive the correct generalization.

**Setup:** A body of mass $M(t)$ moves with velocity $\mathbf{v}(t)$. Mass is ejected at rate $\dot{M} < 0$ with velocity $\mathbf{u}$ relative to the body (so absolute velocity of ejecta is $\mathbf{v} + \mathbf{u}$, where $\mathbf{u}$ points backward).

**Step 1: Momentum of the system at time $t$:**

$$
\mathbf{p}(t) = M(t)\mathbf{v}(t).
$$

At time $t + dt$: the body has mass $M + dM$ (with $dM < 0$) and velocity $\mathbf{v} + d\mathbf{v}$. The ejected mass $(-dM)$ has velocity $\mathbf{v} + \mathbf{u}$.

**Step 2: Apply Newton's second law to the total system:**

$$
\mathbf{F}_{\text{ext}}\,dt = d\mathbf{p}_{\text{total}} = [(M+dM)(\mathbf{v}+d\mathbf{v}) + (-dM)(\mathbf{v}+\mathbf{u})] - M\mathbf{v}.
$$

Expand and drop second-order terms:

$$
\mathbf{F}_{\text{ext}}\,dt = M\,d\mathbf{v} + \mathbf{v}\,dM + d\mathbf{v}\,dM - \mathbf{v}\,dM - \mathbf{u}\,dM \approx M\,d\mathbf{v} - \mathbf{u}\,dM.
$$

**Step 3: The variable-mass equation of motion (Meshchersky equation):**

$$
M\frac{d\mathbf{v}}{dt} = \mathbf{F}_{\text{ext}} + \mathbf{u}\frac{dM}{dt} = \mathbf{F}_{\text{ext}} - v_e\frac{dM}{dt}\hat{\mathbf{v}},
$$

where $v_e = |\mathbf{u}|$ is the exhaust speed and the thrust force is $\mathbf{F}_{\text{thrust}} = -\mathbf{u}\dot{M} = v_e|\dot{M}|\hat{\mathbf{v}}$.

**Step 4: Work-energy for variable mass.** Dot both sides with $\mathbf{v}\,dt = d\mathbf{r}$:

$$
M\mathbf{v}\cdot d\mathbf{v} = \mathbf{F}_{\text{ext}}\cdot d\mathbf{r} + \mathbf{u}\cdot\mathbf{v}\,dM.
$$

The left side is $d(\frac{1}{2}Mv^2) - \frac{1}{2}v^2\,dM$. This shows that the standard work-energy theorem $dK = \mathbf{F}\cdot d\mathbf{r}$ must be modified for variable-mass systems — the kinetic energy of the ejected mass must be accounted for separately.

*References: Goldstein §1.6; Susskind, The Theoretical Minimum, Lecture 2; MIT 8.01 Problem Set 9.*

---
