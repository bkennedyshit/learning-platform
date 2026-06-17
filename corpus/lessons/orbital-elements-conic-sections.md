---
title: "Orbital Elements & Conic Sections"
subject: "Aerospace Engineering & Orbital Mechanics"
catalog: advanced
audience_tier: higher-education
chapter: "10.2"
type: chapter-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 10.2 — Orbital Elements & Conic Sections

> *"The rocket worked perfectly, except for landing on the wrong planet."*
> — **Wernher von Braun** (attributed), on the V-2 program

A Keplerian orbit is fully determined by six parameters — the **classical orbital elements** (COEs). These encode the orbit's size, shape, orientation in 3D space, and the body's position along the orbit at a reference epoch. This chapter develops the complete geometry of conic sections, defines each orbital element with geometric precision, and derives the algorithms for converting between Cartesian state vectors $(\mathbf{r}, \mathbf{v})$ and the orbital element set $(a, e, i, \Omega, \omega, \nu)$.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Identify and sketch the four conic sections (circle, ellipse, parabola, hyperbola) and their geometric parameters.
2. Define all six classical orbital elements $(a, e, i, \Omega, \omega, \nu)$ with precise geometric meaning.
3. Convert from state vectors $(\mathbf{r}, \mathbf{v})$ to orbital elements (the **state-to-elements** algorithm).
4. Convert from orbital elements back to state vectors (the **elements-to-state** algorithm).
5. Handle special cases: circular orbits ($e = 0$), equatorial orbits ($i = 0$), and circular-equatorial orbits.
6. Relate the true anomaly $\nu$, eccentric anomaly $E$, and mean anomaly $M$ via Kepler's equation.

---

## 🖼️ Visual Anchor — Classical Orbital Elements in 3D

![math-10__10.2-fig1](math-10__10.2-fig1.svg)

---

## 📚 1. Definitions

### Definition 10.2.1 — Conic Sections

A **conic section** is the locus of points $P$ such that the ratio of the distance from $P$ to a fixed point (focus $F$) to the distance from $P$ to a fixed line (directrix $\ell$) is constant. This ratio is the eccentricity $e$:

$$
\frac{|PF|}{|P\ell|} = e
$$

The four types:
- **Circle** ($e = 0$): All points equidistant from center
- **Ellipse** ($0 < e < 1$): Closed curve, two foci
- **Parabola** ($e = 1$): Open curve, one focus
- **Hyperbola** ($e > 1$): Two branches, two foci

### Definition 10.2.2 — Ellipse Geometry

An ellipse with semi-major axis $a$ and semi-minor axis $b$ satisfies:

$$
\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1
$$

Key relationships:
- Linear eccentricity: $c = ae = \sqrt{a^2 - b^2}$ (focus-to-center distance)
- Semi-minor axis: $b = a\sqrt{1-e^2}$
- Semi-latus rectum: $p = a(1-e^2) = b^2/a$
- Periapsis: $r_p = a(1-e)$
- Apoapsis: $r_a = a(1+e)$
- Area: $A = \pi ab = \pi a^2\sqrt{1-e^2}$

### Definition 10.2.3 — Hyperbola Geometry

A hyperbola with semi-transverse axis $a$ and semi-conjugate axis $b$ satisfies:

$$
\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1
$$

Key relationships:
- $c = ae = \sqrt{a^2 + b^2}$ (focus-to-center distance)
- $b = a\sqrt{e^2 - 1}$
- Semi-latus rectum: $p = a(e^2 - 1)$
- Periapsis: $r_p = a(e - 1)$ (note: for hyperbola, $a$ is taken negative in energy formulas, or positive with sign conventions adjusted)
- Asymptote half-angle: $\beta = \arccos(1/e)$
- Turn angle: $\delta = 2\beta - \pi = 2\arcsin(1/e)$

**Convention:** In astrodynamics, for hyperbolic orbits we often define $a > 0$ and write $\varepsilon = +\mu/(2a)$ (positive energy), with $r_p = a(e-1)$.

### Definition 10.2.4 — The Six Classical Orbital Elements (COEs)

The **classical orbital elements** (also called Keplerian elements) are:

| Element | Symbol | Description | Range |
|---------|--------|-------------|-------|
| Semi-major axis | $a$ | Size of orbit | $a > 0$ (ellipse), $a < 0$ (hyperbola) |
| Eccentricity | $e$ | Shape of orbit | $e \geq 0$ |
| Inclination | $i$ | Tilt of orbital plane relative to reference plane | $0° \leq i \leq 180°$ |
| Right Ascension of Ascending Node | $\Omega$ | Orientation of node line in reference plane | $0° \leq \Omega < 360°$ |
| Argument of Periapsis | $\omega$ | Orientation of orbit within orbital plane | $0° \leq \omega < 360°$ |
| True Anomaly | $\nu$ (or $\theta$) | Position of body along orbit | $0° \leq \nu < 360°$ |

The first two $(a, e)$ define the orbit's **size and shape**. The next three $(i, \Omega, \omega)$ define the orbit's **orientation in 3D space**. The last $(\nu)$ specifies the body's **position** at the epoch.

### Definition 10.2.5 — Inclination

The **inclination** $i$ is the angle between the orbital angular momentum vector $\mathbf{h}$ and the reference pole $\hat{\mathbf{Z}}$ (typically Earth's north pole):

$$
\cos i = \frac{\mathbf{h} \cdot \hat{\mathbf{Z}}}{|\mathbf{h}|} = \frac{h_Z}{h}
$$

- $i = 0°$: Equatorial prograde orbit
- $0° < i < 90°$: Prograde (eastward) orbit
- $i = 90°$: Polar orbit
- $90° < i < 180°$: Retrograde (westward) orbit

### Definition 10.2.6 — Node Line and RAAN

The **line of nodes** is the intersection of the orbital plane with the reference plane. The **ascending node** is where the orbiting body crosses the reference plane moving from south to north.

The **node vector** is:

$$
\mathbf{n} = \hat{\mathbf{Z}} \times \mathbf{h}
$$

The **Right Ascension of the Ascending Node** (RAAN) $\Omega$ is the angle from the reference direction $\hat{\mathbf{X}}$ (vernal equinox) to the ascending node, measured eastward in the reference plane:

$$
\cos\Omega = \frac{n_X}{|\mathbf{n}|}, \quad \text{with quadrant from } n_Y
$$

### Definition 10.2.7 — Argument of Periapsis

The **argument of periapsis** $\omega$ is the angle in the orbital plane from the ascending node to the periapsis point, measured in the direction of orbital motion:

$$
\cos\omega = \frac{\mathbf{n} \cdot \mathbf{e}}{|\mathbf{n}||\mathbf{e}|}, \quad \text{with quadrant from } e_Z
$$

### Definition 10.2.8 — True Anomaly

The **true anomaly** $\nu$ is the angle in the orbital plane from periapsis to the current position, measured in the direction of motion:

$$
\cos\nu = \frac{\mathbf{e} \cdot \mathbf{r}}{|\mathbf{e}||\mathbf{r}|}, \quad \text{with quadrant from } \mathbf{r} \cdot \mathbf{v}
$$

If $\mathbf{r} \cdot \mathbf{v} \geq 0$, the body is moving away from periapsis ($0° \leq \nu \leq 180°$).
If $\mathbf{r} \cdot \mathbf{v} < 0$, the body is approaching periapsis ($180° < \nu < 360°$).

### Definition 10.2.9 — Eccentric Anomaly

The **eccentric anomaly** $E$ is an auxiliary angle defined geometrically via the circumscribed circle of the orbit ellipse. It relates to true anomaly by:

$$
\tan\frac{\nu}{2} = \sqrt{\frac{1+e}{1-e}}\tan\frac{E}{2}
$$

And to the radius:

$$
r = a(1 - e\cos E)
$$

### Definition 10.2.10 — Mean Anomaly and Kepler's Equation

The **mean anomaly** $M$ is a uniformly increasing angle proportional to time:

$$
M = n(t - t_p)
$$

where $n = \sqrt{\mu/a^3} = 2\pi/T$ is the **mean motion** and $t_p$ is the time of periapsis passage.

**Kepler's Equation** relates mean anomaly to eccentric anomaly:

$$
M = E - e\sin E
$$

This transcendental equation must be solved iteratively (Newton-Raphson) for $E$ given $M$.

### Definition 10.2.11 — Perifocal Coordinate Frame

The **perifocal frame** $(\hat{\mathbf{p}}, \hat{\mathbf{q}}, \hat{\mathbf{w}})$ is centered at the focus with:
- $\hat{\mathbf{p}}$: pointing toward periapsis (along eccentricity vector)
- $\hat{\mathbf{w}}$: along the angular momentum vector $\hat{\mathbf{h}}$
- $\hat{\mathbf{q}} = \hat{\mathbf{w}} \times \hat{\mathbf{p}}$: completing the right-hand system

In this frame, the position and velocity are:

$$
\mathbf{r}_{pqw} = \begin{pmatrix} r\cos\nu \\ r\sin\nu \\ 0 \end{pmatrix}, \quad \mathbf{v}_{pqw} = \frac{\mu}{h}\begin{pmatrix} -\sin\nu \\ e + \cos\nu \\ 0 \end{pmatrix}
$$




---

## 📐 2. Axioms / Postulates

### Axiom 10.2.A1 — Uniqueness of Keplerian Orbit

Given a gravitational parameter $\mu$ and a state vector $(\mathbf{r}, \mathbf{v})$ at any instant, the Keplerian orbit is uniquely determined. Equivalently, six independent parameters suffice to specify the orbit and position.

### Axiom 10.2.A2 — Inertial Reference Frame

The classical orbital elements are defined with respect to a fixed inertial reference frame. For Earth-orbiting satellites, the standard is the **Earth-Centered Inertial (ECI)** frame:
- Origin: Earth's center of mass
- $\hat{\mathbf{X}}$: Vernal equinox direction (♈)
- $\hat{\mathbf{Z}}$: Earth's north pole (angular momentum of Earth's rotation)
- $\hat{\mathbf{Y}} = \hat{\mathbf{Z}} \times \hat{\mathbf{X}}$: Completing right-hand system

### Axiom 10.2.A3 — Two-Body Assumption

The classical orbital elements are constant (except $\nu$, which varies with time) only under the pure two-body assumption. Perturbations (J2, drag, third-body, solar radiation pressure) cause secular and periodic variations in all elements.

---

## 🛡️ 3. Lemmas

### Lemma 10.2.1 — State Vector to Orbital Elements Algorithm

**Statement:** Given position $\mathbf{r}$ and velocity $\mathbf{v}$ in the ECI frame, the classical orbital elements are computed as follows:

<details>
<summary>🔍 Complete Algorithm</summary>

**Step 1:** Compute distance and speed:

$$
r = |\mathbf{r}|, \quad v = |\mathbf{v}|
$$

**Step 2:** Compute specific angular momentum:

$$
\mathbf{h} = \mathbf{r} \times \mathbf{v}, \quad h = |\mathbf{h}|
$$

**Step 3:** Compute node vector:

$$
\mathbf{n} = \hat{\mathbf{Z}} \times \mathbf{h} = (-h_Y, h_X, 0), \quad n = |\mathbf{n}|
$$

**Step 4:** Compute eccentricity vector:

$$
\mathbf{e} = \frac{1}{\mu}\left[(v^2 - \frac{\mu}{r})\mathbf{r} - (\mathbf{r}\cdot\mathbf{v})\mathbf{v}\right]
$$

$$
e = |\mathbf{e}|
$$

**Step 5:** Compute specific energy and semi-major axis:

$$
\varepsilon = \frac{v^2}{2} - \frac{\mu}{r}
$$

$$
a = -\frac{\mu}{2\varepsilon} \quad (e \neq 1)
$$

For parabolic orbits ($e = 1$): $a$ is undefined; use $p = h^2/\mu$ instead.

**Step 6:** Compute inclination:

$$
i = \arccos\left(\frac{h_Z}{h}\right)
$$

**Step 7:** Compute RAAN:

$$
\Omega = \arccos\left(\frac{n_X}{n}\right)
$$

If $n_Y \lt  0$: $\Omega = 360° - \Omega$.

**Step 8:** Compute argument of periapsis:

$$
\omega = \arccos\left(\frac{\mathbf{n}\cdot\mathbf{e}}{ne}\right)
$$

If $e_Z \lt  0$: $\omega = 360° - \omega$.

**Step 9:** Compute true anomaly:

$$
\nu = \arccos\left(\frac{\mathbf{e}\cdot\mathbf{r}}{er}\right)
$$

If $\mathbf{r}\cdot\mathbf{v} \lt  0$: $\nu = 360° - \nu$.

</details>

### Lemma 10.2.2 — Orbital Elements to State Vector Algorithm

**Statement:** Given $(a, e, i, \Omega, \omega, \nu)$ and $\mu$, reconstruct $(\mathbf{r}, \mathbf{v})$ in ECI.

<details>
<summary>🔍 Complete Algorithm</summary>

**Step 1:** Compute orbital parameters:

$$
p = a(1-e^2), \quad r = \frac{p}{1+e\cos\nu}, \quad h = \sqrt{\mu p}
$$

**Step 2:** Position and velocity in perifocal frame:

$$
\mathbf{r}_{pqw} = \begin{pmatrix} r\cos\nu \\ r\sin\nu \\ 0 \end{pmatrix}
$$

$$
\mathbf{v}_{pqw} = \frac{\mu}{h}\begin{pmatrix} -\sin\nu \\ e + \cos\nu \\ 0 \end{pmatrix}
$$

**Step 3:** Rotation matrix from perifocal to ECI (3-1-3 Euler rotation by $-\Omega$, $-i$, $-\omega$):

$$
[Q]_{pqw \to ECI} = R_3(-\Omega)\,R_1(-i)\,R_3(-\omega)
$$

Explicitly:

$$
Q = \begin{pmatrix}
\cos\Omega\cos\omega - \sin\Omega\sin\omega\cos i & -\cos\Omega\sin\omega - \sin\Omega\cos\omega\cos i & \sin\Omega\sin i \\
\sin\Omega\cos\omega + \cos\Omega\sin\omega\cos i & -\sin\Omega\sin\omega + \cos\Omega\cos\omega\cos i & -\cos\Omega\sin i \\
\sin\omega\sin i & \cos\omega\sin i & \cos i
\end{pmatrix}
$$

**Step 4:** Transform to ECI:

$$
\mathbf{r}_{ECI} = Q\,\mathbf{r}_{pqw}, \quad \mathbf{v}_{ECI} = Q\,\mathbf{v}_{pqw}
$$

</details>

### Lemma 10.2.3 — Kepler's Equation Solution (Newton-Raphson)

**Statement:** Given mean anomaly $M$ and eccentricity $e$, solve $M = E - e\sin E$ for eccentric anomaly $E$ using Newton-Raphson iteration:

$$
E_{n+1} = E_n - \frac{E_n - e\sin E_n - M}{1 - e\cos E_n}
$$

<details>
<summary>🔍 Convergence Analysis</summary>

**Initial guess:** $E_0 = M$ (good for $e \lt  0.8$). For high eccentricity, use $E_0 = \pi$.

**Convergence:** The function $f(E) = E - e\sin E - M$ has derivative $f'(E) = 1 - e\cos E \gt  0$ for $e \lt  1$. Since $f$ is monotonically increasing and smooth, Newton-Raphson converges quadratically from any initial guess.

**Iteration count:** Typically 3–5 iterations suffice for machine precision ($|f(E)| \lt  10^{-12}$).

**Example:** $M = 3.6029$ rad, $e = 0.37255$.

| Iteration | $E_n$ (rad) | $f(E_n)$ |
|:---------:|:-----------:|:---------:|
| 0 | 3.6029 | −0.1413 |
| 1 | 3.7488 | 0.00156 |
| 2 | 3.7471 | $2.0 \times 10^{-7}$ |
| 3 | 3.7471 | $\lt  10^{-14}$ |

</details>

### Lemma 10.2.4 — True Anomaly from Eccentric Anomaly

**Statement:** The relationship between true anomaly $\nu$ and eccentric anomaly $E$ is:

$$
\tan\frac{\nu}{2} = \sqrt{\frac{1+e}{1-e}}\tan\frac{E}{2}
$$

<details>
<summary>🔍 Derivation</summary>

From the orbit equation: $r = a(1-e\cos E)$ and $r = \frac{a(1-e^2)}{1+e\cos\nu}$.

Equating:

$$
a(1-e\cos E) = \frac{a(1-e^2)}{1+e\cos\nu}
$$

$$
(1-e\cos E)(1+e\cos\nu) = 1-e^2
$$

$$
1 + e\cos\nu - e\cos E - e^2\cos E\cos\nu = 1 - e^2
$$

$$
e\cos\nu - e\cos E - e^2\cos E\cos\nu + e^2 = 0
$$

$$
\cos\nu(1 - e\cos E) = \cos E - e
$$

$$
\cos\nu = \frac{\cos E - e}{1 - e\cos E}
$$

Using the half-angle identity $\cos\alpha = \frac{1-\tan^2(\alpha/2)}{1+\tan^2(\alpha/2)}$:

$$
\frac{1-\tan^2(\nu/2)}{1+\tan^2(\nu/2)} = \frac{\frac{1-\tan^2(E/2)}{1+\tan^2(E/2)} - e}{1 - e\frac{1-\tan^2(E/2)}{1+\tan^2(E/2)}}
$$

Let $t = \tan(E/2)$. Numerator of RHS:

$$
\frac{1-t^2 - e(1+t^2)}{1+t^2} = \frac{(1-e) - (1+e)t^2}{1+t^2}
$$

Denominator of RHS:

$$
\frac{(1+t^2) - e(1-t^2)}{1+t^2} = \frac{(1-e) + (1+e)t^2}{1+t^2}
$$

So:

$$
\frac{1-\tan^2(\nu/2)}{1+\tan^2(\nu/2)} = \frac{(1-e) - (1+e)t^2}{(1-e) + (1+e)t^2}
$$

Comparing with the half-angle form, we identify:

$$
\tan^2(\nu/2) = \frac{(1+e)t^2}{1-e} = \frac{1+e}{1-e}\tan^2(E/2)
$$

$$
\tan\frac{\nu}{2} = \sqrt{\frac{1+e}{1-e}}\tan\frac{E}{2}
$$

$\blacksquare$

</details>

### Lemma 10.2.5 — Velocity Components in Perifocal Frame

**Statement:** In the perifocal frame, the velocity components are:

$$
\dot{r}_p = -\frac{\mu}{h}\sin\nu, \quad \dot{r}_q = \frac{\mu}{h}(e + \cos\nu)
$$

<details>
<summary>🔍 Derivation</summary>

Position in perifocal frame: $\mathbf{r} = r\cos\nu\,\hat{\mathbf{p}} + r\sin\nu\,\hat{\mathbf{q}}$.

Differentiate with respect to time:

$$
\mathbf{v} = (\dot{r}\cos\nu - r\dot\nu\sin\nu)\hat{\mathbf{p}} + (\dot{r}\sin\nu + r\dot\nu\cos\nu)\hat{\mathbf{q}}
$$

From $h = r^2\dot\nu$: $\dot\nu = h/r^2$.

From $r = p/(1+e\cos\nu)$: $\dot{r} = \frac{pe\sin\nu\,\dot\nu}{(1+e\cos\nu)^2} = \frac{e\sin\nu \cdot h}{r^2} \cdot \frac{r^2}{p} \cdot \frac{1}{1+e\cos\nu}$...

More directly, differentiate $r(1+e\cos\nu) = p$:

$$
\dot{r}(1+e\cos\nu) + r(-e\sin\nu)\dot\nu = 0
$$

$$
\dot{r} = \frac{re\sin\nu\,\dot\nu}{1+e\cos\nu} = \frac{re\sin\nu}{1+e\cos\nu}\cdot\frac{h}{r^2} = \frac{e\sin\nu \cdot h}{r(1+e\cos\nu)} = \frac{\mu e\sin\nu}{h}
$$

(using $r(1+e\cos\nu) = p = h^2/\mu$, so $h/[r(1+e\cos\nu)] = h/(h^2/\mu) = \mu/h$).

Now the velocity components:

$$
v_p = \dot{r}\cos\nu - r\dot\nu\sin\nu = \frac{\mu e\sin\nu\cos\nu}{h} - \frac{h\sin\nu}{r}
$$

$$
= \frac{\mu e\sin\nu\cos\nu}{h} - \frac{\mu(1+e\cos\nu)\sin\nu}{h} = \frac{\mu\sin\nu}{h}[e\cos\nu - 1 - e\cos\nu] = -\frac{\mu\sin\nu}{h}
$$

$$
v_q = \dot{r}\sin\nu + r\dot\nu\cos\nu = \frac{\mu e\sin^2\nu}{h} + \frac{h\cos\nu}{r}
$$

$$
= \frac{\mu e\sin^2\nu}{h} + \frac{\mu(1+e\cos\nu)\cos\nu}{h} = \frac{\mu}{h}[e\sin^2\nu + \cos\nu + e\cos^2\nu]
$$

$$
= \frac{\mu}{h}[e(\sin^2\nu + \cos^2\nu) + \cos\nu] = \frac{\mu}{h}(e + \cos\nu)
$$

Therefore:

$$
\mathbf{v}_{pqw} = \frac{\mu}{h}\begin{pmatrix}-\sin\nu \\ e + \cos\nu \\ 0\end{pmatrix}
$$

$\blacksquare$

</details>




---

## 👑 4. Theorems

### Theorem 10.2.1 — Orbit Equation as Conic Section

The polar equation $r = \frac{p}{1+e\cos\nu}$ with focus at the origin represents:
- An **ellipse** when $0 \leq e < 1$ (bound orbit, $\varepsilon < 0$)
- A **parabola** when $e = 1$ (marginally unbound, $\varepsilon = 0$)
- A **hyperbola** when $e > 1$ (unbound, $\varepsilon > 0$)

The semi-latus rectum $p = h^2/\mu$ is always positive for physical orbits.

### Theorem 10.2.2 — Relationship Between Energy, Angular Momentum, and Eccentricity

$$
e = \sqrt{1 + \frac{2\varepsilon h^2}{\mu^2}}
$$

This connects the orbit shape (eccentricity) to the two fundamental integrals of motion (energy and angular momentum).

### Theorem 10.2.3 — Flight Path Angle

The **flight path angle** $\gamma$ (angle between velocity vector and local horizontal) satisfies:

$$
\tan\gamma = \frac{v_r}{v_\perp} = \frac{e\sin\nu}{1 + e\cos\nu}
$$

where $v_r = \dot{r} = \frac{\mu e\sin\nu}{h}$ is the radial velocity and $v_\perp = r\dot\nu = \frac{h}{r} = \frac{\mu(1+e\cos\nu)}{h}$ is the transverse velocity.

### Theorem 10.2.4 — Kepler's Equation (Time-Position Relationship)

For an elliptical orbit, the time $t$ since periapsis passage is related to position through:

$$
M = n(t - t_p) = E - e\sin E
$$

where $n = \sqrt{\mu/a^3}$ is the mean motion and $E$ is the eccentric anomaly related to $\nu$ by:

$$
\cos\nu = \frac{\cos E - e}{1 - e\cos E}, \quad \cos E = \frac{e + \cos\nu}{1 + e\cos\nu}
$$

### Theorem 10.2.5 — Hyperbolic Kepler's Equation

For a hyperbolic orbit ($e > 1$), the time relationship uses the **hyperbolic anomaly** $F$:

$$
M_h = e\sinh F - F
$$

where $M_h = n_h(t - t_p)$ with $n_h = \sqrt{\mu/(-a)^3}$ (using $a < 0$ for hyperbolas in this convention, or $n_h = \sqrt{\mu/a^3}$ with $a > 0$ representing the semi-transverse axis).

The relationship to true anomaly:

$$
\tanh\frac{F}{2} = \sqrt{\frac{e-1}{e+1}}\tan\frac{\nu}{2}
$$

### Theorem 10.2.6 — Rotation Matrix Decomposition

The transformation from perifocal to ECI frame is a sequence of three rotations:

$$
[Q]_{pqw \to ECI} = R_3(-\Omega)\,R_1(-i)\,R_3(-\omega)
$$

This is a 3-1-3 Euler angle sequence. The inverse (ECI to perifocal) is:

$$
[Q]_{ECI \to pqw} = R_3(\omega)\,R_1(i)\,R_3(\Omega)
$$

---

## ✍️ 5. Proofs / Derivations

### 5.1 Derivation of the Eccentricity Vector Formula

**Goal:** Derive $\mathbf{e} = \frac{1}{\mu}\left[(v^2 - \frac{\mu}{r})\mathbf{r} - (\mathbf{r}\cdot\mathbf{v})\mathbf{v}\right]$ from the Laplace-Runge-Lenz definition.

**Step 1:** Start from the definition $\mathbf{e} = \frac{\mathbf{v}\times\mathbf{h}}{\mu} - \hat{\mathbf{r}}$.

**Step 2:** Expand $\mathbf{v}\times\mathbf{h} = \mathbf{v}\times(\mathbf{r}\times\mathbf{v})$.

Apply the BAC-CAB identity: $\mathbf{A}\times(\mathbf{B}\times\mathbf{C}) = \mathbf{B}(\mathbf{A}\cdot\mathbf{C}) - \mathbf{C}(\mathbf{A}\cdot\mathbf{B})$:

$$
\mathbf{v}\times(\mathbf{r}\times\mathbf{v}) = \mathbf{r}(\mathbf{v}\cdot\mathbf{v}) - \mathbf{v}(\mathbf{v}\cdot\mathbf{r}) = v^2\mathbf{r} - (\mathbf{r}\cdot\mathbf{v})\mathbf{v}
$$

**Step 3:** Substitute back:

$$
\mathbf{e} = \frac{v^2\mathbf{r} - (\mathbf{r}\cdot\mathbf{v})\mathbf{v}}{\mu} - \frac{\mathbf{r}}{r}
$$

$$
= \frac{1}{\mu}\left[v^2\mathbf{r} - (\mathbf{r}\cdot\mathbf{v})\mathbf{v} - \frac{\mu}{r}\mathbf{r}\right]
$$

$$
= \frac{1}{\mu}\left[\left(v^2 - \frac{\mu}{r}\right)\mathbf{r} - (\mathbf{r}\cdot\mathbf{v})\mathbf{v}\right]
$$

$\blacksquare$

### 5.2 Derivation of the Rotation Matrix (Perifocal → ECI)

**Goal:** Construct the direction cosine matrix $Q$ that transforms vectors from the perifocal frame to ECI.

**Step 1:** The perifocal frame is obtained from ECI by three successive rotations:
1. Rotate about $\hat{\mathbf{Z}}$ by angle $\Omega$ (align $\hat{\mathbf{X}}$ with node line)
2. Rotate about the new $\hat{\mathbf{X}}'$ by angle $i$ (tilt to orbital plane)
3. Rotate about the new $\hat{\mathbf{Z}}''$ by angle $\omega$ (align with periapsis)

So: $[Q]_{ECI \to pqw} = R_3(\omega)\,R_1(i)\,R_3(\Omega)$

**Step 2:** The individual rotation matrices are:

$$
R_3(\alpha) = \begin{pmatrix}\cos\alpha & \sin\alpha & 0 \\ -\sin\alpha & \cos\alpha & 0 \\ 0 & 0 & 1\end{pmatrix}
$$

$$
R_1(\alpha) = \begin{pmatrix}1 & 0 & 0 \\ 0 & \cos\alpha & \sin\alpha \\ 0 & -\sin\alpha & \cos\alpha\end{pmatrix}
$$

**Step 3:** The inverse transformation (perifocal → ECI) is:

$$
[Q]_{pqw \to ECI} = [Q]_{ECI \to pqw}^T = [R_3(\Omega)]^T[R_1(i)]^T[R_3(\omega)]^T = R_3(-\Omega)\,R_1(-i)\,R_3(-\omega)
$$

**Step 4:** Multiply out explicitly. Let $c\Omega = \cos\Omega$, $s\Omega = \sin\Omega$, $ci = \cos i$, $si = \sin i$, $c\omega = \cos\omega$, $s\omega = \sin\omega$:

$$
Q_{11} = c\Omega\,c\omega - s\Omega\,s\omega\,ci
$$

$$
Q_{12} = -c\Omega\,s\omega - s\Omega\,c\omega\,ci
$$

$$
Q_{13} = s\Omega\,si
$$

$$
Q_{21} = s\Omega\,c\omega + c\Omega\,s\omega\,ci
$$

$$
Q_{22} = -s\Omega\,s\omega + c\Omega\,c\omega\,ci
$$

$$
Q_{23} = -c\Omega\,si
$$

$$
Q_{31} = s\omega\,si
$$

$$
Q_{32} = c\omega\,si
$$

$$
Q_{33} = ci
$$

$\blacksquare$

### 5.3 Proof that Eccentricity Determines Orbit Type via Energy

**Goal:** Prove $e = \sqrt{1 + \frac{2\varepsilon h^2}{\mu^2}}$.

**Step 1:** From the orbit equation, at periapsis ($\nu = 0$):

$$
r_p = \frac{p}{1+e} = \frac{h^2}{\mu(1+e)}
$$

**Step 2:** At periapsis, velocity is purely transverse: $v_p = h/r_p = \frac{\mu(1+e)}{h}$.

**Step 3:** Compute specific energy at periapsis:

$$
\varepsilon = \frac{v_p^2}{2} - \frac{\mu}{r_p} = \frac{\mu^2(1+e)^2}{2h^2} - \frac{\mu^2(1+e)}{h^2}
$$

$$
= \frac{\mu^2(1+e)}{2h^2}[(1+e) - 2] = \frac{\mu^2(1+e)(e-1)}{2h^2} = \frac{\mu^2(e^2-1)}{2h^2}
$$

**Step 4:** Solve for $e^2$:

$$
2\varepsilon h^2 = \mu^2(e^2 - 1)
$$

$$
e^2 = 1 + \frac{2\varepsilon h^2}{\mu^2}
$$

$$
e = \sqrt{1 + \frac{2\varepsilon h^2}{\mu^2}}
$$

$\blacksquare$

### 5.4 Derivation of Kepler's Equation

**Goal:** Derive $M = E - e\sin E$.

**Step 1:** From Kepler's Second Law, the area swept from periapsis to position $E$ is proportional to time:

$$
\frac{A(E)}{A_{\text{total}}} = \frac{t - t_p}{T}
$$

**Step 2:** The area swept (measured via eccentric anomaly on the auxiliary circle of radius $a$) is:

$$
A(E) = \frac{a^2}{2}(E - e\sin E)
$$

This is derived by noting that the area under the ellipse from periapsis to angle $E$ equals the area of the circular sector minus the triangle:

Area of sector (on auxiliary circle): $\frac{1}{2}a^2 E$

The triangle formed by center, projection of satellite on auxiliary circle, and focus has area: $\frac{1}{2}a \cdot ae\sin E = \frac{1}{2}a^2 e\sin E$

But we need the area swept by the radius from the focus, not the center. Using the ratio of ellipse to circle areas ($b/a$):

$$
A_{\text{ellipse sector}} = \frac{b}{a}\left[\frac{a^2 E}{2} - \frac{a^2 e\sin E}{2}\right] = \frac{ab}{2}(E - e\sin E)
$$

**Step 3:** Total ellipse area: $A_{\text{total}} = \pi ab$.

$$
\frac{t - t_p}{T} = \frac{\frac{ab}{2}(E - e\sin E)}{\pi ab} = \frac{E - e\sin E}{2\pi}
$$

**Step 4:** Define mean anomaly $M = \frac{2\pi}{T}(t - t_p) = n(t-t_p)$:

$$
M = E - e\sin E
$$

$\blacksquare$




---

## 🧮 6. Worked Examples

### Example 10.2.1 — State Vector to Orbital Elements

**Given:** A satellite has the following state vector in ECI (km, km/s):

$$
\mathbf{r} = \begin{pmatrix} -6045.0 \\ -3490.0 \\ 2500.0 \end{pmatrix}, \quad \mathbf{v} = \begin{pmatrix} -3.457 \\ 6.618 \\ 2.533 \end{pmatrix}
$$

$\mu_E = 398{,}600.4$ km³/s².

**Find:** All six classical orbital elements.

**Solution:**

Step 1: Magnitudes:

$$
r = \sqrt{6045^2 + 3490^2 + 2500^2} = \sqrt{36542025 + 12180100 + 6250000} = \sqrt{54972125} = 7414.0 \text{ km}
$$

$$
v = \sqrt{3.457^2 + 6.618^2 + 2.533^2} = \sqrt{11.95 + 43.80 + 6.42} = \sqrt{62.17} = 7.885 \text{ km/s}
$$

Step 2: Angular momentum:

$$
\mathbf{h} = \mathbf{r}\times\mathbf{v} = \begin{pmatrix}(-3490)(2.533) - (2500)(6.618) \\ (2500)(-3.457) - (-6045)(2.533) \\ (-6045)(6.618) - (-3490)(-3.457)\end{pmatrix}
$$

$$
= \begin{pmatrix}-8840.2 - 16545.0 \\ -8642.5 + 15312.0 \\ -40015.7 - 12064.8\end{pmatrix} = \begin{pmatrix}-25385.2 \\ 6669.5 \\ -52080.5\end{pmatrix}
$$

$$
h = \sqrt{25385.2^2 + 6669.5^2 + 52080.5^2} = \sqrt{644.4\times10^6 + 44.5\times10^6 + 2712.4\times10^6} = 58310 \text{ km}^2/\text{s}
$$

Step 3: Node vector $\mathbf{n} = \hat{\mathbf{Z}}\times\mathbf{h} = (0,0,1)\times\mathbf{h} = (-h_Y, h_X, 0)$:

$$
\mathbf{n} = (-6669.5, -25385.2, 0), \quad n = \sqrt{6669.5^2 + 25385.2^2} = 26247 \text{ km}^2/\text{s}
$$

Step 4: Eccentricity vector:

$$
v^2 - \mu/r = 62.17 - 398600.4/7414.0 = 62.17 - 53.76 = 8.41 \text{ km}^2/\text{s}^2
$$

$$
\mathbf{r}\cdot\mathbf{v} = (-6045)(-3.457) + (-3490)(6.618) + (2500)(2.533) = 20897.6 - 23096.8 + 6332.5 = 4133.3
$$

$$
\mathbf{e} = \frac{1}{398600.4}\left[8.41\begin{pmatrix}-6045\\-3490\\2500\end{pmatrix} - 4133.3\begin{pmatrix}-3.457\\6.618\\2.533\end{pmatrix}\right]
$$

$$
= \frac{1}{398600.4}\begin{pmatrix}-50838.5 + 14288.7\\-29351.9 - 27358.0\\21025.0 - 10469.5\end{pmatrix} = \frac{1}{398600.4}\begin{pmatrix}-36549.8\\-56709.9\\10555.5\end{pmatrix}
$$

$$
\mathbf{e} = \begin{pmatrix}-0.09171\\-0.14226\\0.02648\end{pmatrix}, \quad e = 0.1712
$$

Step 5: Energy and semi-major axis:

$$
\varepsilon = \frac{62.17}{2} - \frac{398600.4}{7414.0} = 31.085 - 53.76 = -22.68 \text{ km}^2/\text{s}^2
$$

$$
a = -\frac{398600.4}{2(-22.68)} = \frac{398600.4}{45.36} = 8787 \text{ km}
$$

Step 6: Inclination:

$$
i = \arccos\left(\frac{h_Z}{h}\right) = \arccos\left(\frac{-52080.5}{58310}\right) = \arccos(-0.8932) = 153.3°
$$

(Retrograde orbit!)

Step 7: RAAN: $\cos\Omega = n_X/n = -6669.5/26247 = -0.2541$. Since $n_Y = -25385.2 < 0$: $\Omega = 360° - \arccos(-0.2541) = 360° - 104.7° = 255.3°$.

Step 8: Argument of periapsis: $\cos\omega = \frac{\mathbf{n}\cdot\mathbf{e}}{ne} = \frac{(-6669.5)(-0.09171)+(-25385.2)(-0.14226)}{26247 \times 0.1712}$

$$
= \frac{611.6 + 3611.3}{4493.0} = \frac{4222.9}{4493.0} = 0.9399
$$

Since $e_Z = 0.02648 > 0$: $\omega = \arccos(0.9399) = 20.0°$.

Step 9: True anomaly: $\cos\nu = \frac{\mathbf{e}\cdot\mathbf{r}}{er} = \frac{(-0.09171)(-6045)+(-0.14226)(-3490)+(0.02648)(2500)}{0.1712 \times 7414.0}$

$$
= \frac{554.4 + 496.5 + 66.2}{1269.3} = \frac{1117.1}{1269.3} = 0.8801
$$

$\mathbf{r}\cdot\mathbf{v} = 4133.3 > 0$, so $\nu = \arccos(0.8801) = 28.3°$.

**Summary:**

| Element | Value |
|---------|-------|
| $a$ | 8,787 km |
| $e$ | 0.1712 |
| $i$ | 153.3° |
| $\Omega$ | 255.3° |
| $\omega$ | 20.0° |
| $\nu$ | 28.3° |

---

### Example 10.2.2 — Orbital Elements to State Vector

**Given:** $a = 10{,}000$ km, $e = 0.3$, $i = 40°$, $\Omega = 60°$, $\omega = 30°$, $\nu = 50°$. $\mu = 398{,}600.4$ km³/s².

**Find:** State vector $(\mathbf{r}, \mathbf{v})$ in ECI.

**Solution:**

Step 1: Compute parameters:

$$
p = a(1-e^2) = 10000(1-0.09) = 9100 \text{ km}
$$

$$
r = \frac{p}{1+e\cos\nu} = \frac{9100}{1+0.3\cos50°} = \frac{9100}{1+0.1928} = \frac{9100}{1.1928} = 7631 \text{ km}
$$

$$
h = \sqrt{\mu p} = \sqrt{398600.4 \times 9100} = \sqrt{3.627\times10^9} = 60225 \text{ km}^2/\text{s}
$$

Step 2: Perifocal position and velocity:

$$
\mathbf{r}_{pqw} = \begin{pmatrix}r\cos\nu \\ r\sin\nu \\ 0\end{pmatrix} = \begin{pmatrix}7631\cos50° \\ 7631\sin50° \\ 0\end{pmatrix} = \begin{pmatrix}4904.3 \\ 5846.0 \\ 0\end{pmatrix} \text{ km}
$$

$$
\mathbf{v}_{pqw} = \frac{\mu}{h}\begin{pmatrix}-\sin\nu \\ e+\cos\nu \\ 0\end{pmatrix} = \frac{398600.4}{60225}\begin{pmatrix}-\sin50° \\ 0.3+\cos50° \\ 0\end{pmatrix}
$$

$$
= 6.618\begin{pmatrix}-0.7660 \\ 0.9428 \\ 0\end{pmatrix} = \begin{pmatrix}-5.070 \\ 6.240 \\ 0\end{pmatrix} \text{ km/s}
$$

Step 3: Compute rotation matrix elements (using $\Omega=60°$, $i=40°$, $\omega=30°$):

$c\Omega = 0.5$, $s\Omega = 0.8660$, $ci = 0.7660$, $si = 0.6428$, $c\omega = 0.8660$, $s\omega = 0.5$

$$
Q_{11} = (0.5)(0.8660) - (0.8660)(0.5)(0.7660) = 0.4330 - 0.3317 = 0.1013
$$

$$
Q_{12} = -(0.5)(0.5) - (0.8660)(0.8660)(0.7660) = -0.2500 - 0.5745 = -0.8245
$$

$$
Q_{21} = (0.8660)(0.8660) + (0.5)(0.5)(0.7660) = 0.7500 + 0.1915 = 0.9415
$$

$$
Q_{22} = -(0.8660)(0.5) + (0.5)(0.8660)(0.7660) = -0.4330 + 0.3317 = -0.1013
$$

$$
Q_{31} = (0.5)(0.6428) = 0.3214, \quad Q_{32} = (0.8660)(0.6428) = 0.5567
$$

$$
Q_{13} = (0.8660)(0.6428) = 0.5567, \quad Q_{23} = -(0.5)(0.6428) = -0.3214, \quad Q_{33} = 0.7660
$$

Step 4: Transform:

$$
\mathbf{r}_{ECI} = Q\,\mathbf{r}_{pqw} = \begin{pmatrix}0.1013(4904.3) + (-0.8245)(5846.0) \\ 0.9415(4904.3) + (-0.1013)(5846.0) \\ 0.3214(4904.3) + 0.5567(5846.0)\end{pmatrix}
$$

$$
= \begin{pmatrix}496.8 - 4819.8 \\ 4617.4 - 592.2 \\ 1576.2 + 3254.5\end{pmatrix} = \begin{pmatrix}-4323.0 \\ 4025.2 \\ 4830.7\end{pmatrix} \text{ km}
$$

---

### Example 10.2.3 — Solving Kepler's Equation

**Given:** $e = 0.4$, $M = 235.4°$ = 4.1103 rad.

**Find:** True anomaly $\nu$.

**Solution:**

Step 1: Newton-Raphson for $E$. Initial guess $E_0 = M = 4.1103$ rad.

Iteration 1:

$$
f(E_0) = 4.1103 - 0.4\sin(4.1103) - 4.1103 = -0.4\sin(4.1103) = -0.4(-0.8090) = 0.3236
$$

Wait — let me redo. $f(E) = E - e\sin E - M$:

$$
f(4.1103) = 4.1103 - 0.4\sin(4.1103) - 4.1103 = -0.4(-0.8090) = 0.3236
$$

$$
f'(4.1103) = 1 - 0.4\cos(4.1103) = 1 - 0.4(-0.5878) = 1.2351
$$

$$
E_1 = 4.1103 - \frac{0.3236}{1.2351} = 4.1103 - 0.2620 = 3.8483
$$

Iteration 2:

$$
f(3.8483) = 3.8483 - 0.4\sin(3.8483) - 4.1103 = 3.8483 + 0.4(0.6442) - 4.1103 = 3.8483 + 0.2577 - 4.1103 = -0.0043
$$

$$
f'(3.8483) = 1 - 0.4\cos(3.8483) = 1 - 0.4(-0.7649) = 1.3060
$$

$$
E_2 = 3.8483 - \frac{-0.0043}{1.3060} = 3.8483 + 0.0033 = 3.8516 \text{ rad}
$$

Iteration 3: $|f(E_2)| < 10^{-6}$. Converged: $E = 3.8516$ rad = $220.6°$.

Step 2: True anomaly from $E$:

$$
\tan\frac{\nu}{2} = \sqrt{\frac{1+e}{1-e}}\tan\frac{E}{2} = \sqrt{\frac{1.4}{0.6}}\tan(110.3°) = 1.528 \times (-2.747) = -4.198
$$

$$
\frac{\nu}{2} = \arctan(-4.198) = -76.6° + 180° = 103.4° \quad (\text{since } E > \pi, \nu > \pi)
$$

$$
\nu = 206.8° = 3.610 \text{ rad}
$$

---

### Example 10.2.4 — Hyperbolic Excess Velocity

**Given:** A spacecraft approaches Earth on a hyperbolic trajectory with $v_\infty = 3.0$ km/s and periapsis altitude $h_p = 300$ km. $\mu_E = 398{,}600.4$ km³/s², $R_E = 6371$ km.

**Find:** Eccentricity $e$, semi-major axis $a$, and velocity at periapsis $v_p$.

**Solution:**

Step 1: Periapsis radius: $r_p = R_E + h_p = 6671$ km.

Step 2: Semi-major axis (hyperbolic, using $\varepsilon = v_\infty^2/2$):

$$
\varepsilon = \frac{v_\infty^2}{2} = \frac{9.0}{2} = 4.5 \text{ km}^2/\text{s}^2
$$

$$
a = -\frac{\mu}{2\varepsilon} = -\frac{398600.4}{9.0} = -44{,}289 \text{ km}
$$

(Negative for hyperbola in the energy convention.)

Step 3: Eccentricity from $r_p = |a|(e-1)$:

$$
e = 1 + \frac{r_p}{|a|} = 1 + \frac{6671}{44289} = 1.1506
$$

Step 4: Velocity at periapsis (Vis-Viva):

$$
v_p = \sqrt{\mu\left(\frac{2}{r_p} - \frac{1}{a}\right)} = \sqrt{398600.4\left(\frac{2}{6671} + \frac{1}{44289}\right)}
$$

$$
= \sqrt{398600.4(2.997\times10^{-4} + 2.258\times10^{-5})} = \sqrt{398600.4 \times 3.223\times10^{-4}}
$$

$$
= \sqrt{128.5} = 11.34 \text{ km/s}
$$

**Check:** $v_p^2 = v_\infty^2 + v_{\text{esc}}^2 = 9.0 + 2\mu/r_p = 9.0 + 119.5 = 128.5$ km²/s². ✓

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links

- [10.1 - Two-Body Problem & Kepler's Laws](10.1---Two-Body-Problem-&-Kepler's-Laws) — Derivation of the orbit equation used here
- [10.3 - Orbital Maneuvers - Hohmann Transfers](10.3---Orbital-Maneuvers---Hohmann-Transfers) — Applying orbital elements to maneuver planning
- [4.4 - Central Forces & Keplerian Orbits](4.4---Central-Forces-&-Keplerian-Orbits) — Classical mechanics foundation
- [2.6 - Eigenvalues Eigenvectors & Diagonalization](2.6---Eigenvalues-Eigenvectors-&-Diagonalization) — Rotation matrices and coordinate transformations
- [10.7 - Interplanetary Trajectories - Patched Conics](10.7---Interplanetary-Trajectories---Patched-Conics) — Hyperbolic elements for planetary encounters

### Authoritative External Sources

| Source | Description |
|--------|-------------|
| Curtis, H.D. *Orbital Mechanics for Engineering Students*, Ch. 4 | Orbital elements and coordinate transformations |
| Bate, Mueller & White, *Fundamentals of Astrodynamics*, Ch. 2 | Conic sections and orbit determination |
| MIT OCW 16.346, Lecture 3–5 | State vector ↔ elements algorithms |
| Vallado, D.A. *Fundamentals of Astrodynamics*, Ch. 2–3 | Comprehensive treatment with special cases |
| Battin, R.H. *An Introduction to the Mathematics and Methods of Astrodynamics* | Advanced mathematical treatment |

