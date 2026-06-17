---
title: "Orbital Maneuvers — Hohmann Transfers"
subject: "Aerospace Engineering & Orbital Mechanics"
catalog: advanced
audience_tier: higher-education
chapter: "10.3"
type: chapter-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 10.3 — Orbital Maneuvers: Hohmann Transfers

> *"For a successful technology, reality must take precedence over public relations, for Nature cannot be fooled."*
> — **Richard Feynman**, Rogers Commission Report (1986)

Orbital maneuvers are the bread and butter of mission design. The Hohmann transfer — a two-impulse maneuver using a coplanar transfer ellipse — is the most fuel-efficient two-burn coplanar transfer between circular orbits. This chapter derives the complete ΔV equations, extends to bi-elliptic transfers, plane changes, and phasing maneuvers, providing the quantitative tools needed for mission planning.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Compute ΔV for a **Hohmann transfer** between two circular orbits.
2. Determine the **transfer time** for a Hohmann maneuver.
3. Analyze when a **bi-elliptic transfer** is more efficient than Hohmann.
4. Calculate ΔV for **simple plane changes** and **combined maneuvers**.
5. Compute the **phase angle** required for orbital rendezvous.
6. Apply the **general coplanar transfer** equations for non-circular initial/final orbits.

---

## 🖼️ Visual Anchor — Hohmann Transfer Geometry

![math-10__10.3-fig1](math-10__10.3-fig1.svg)

---

## 📚 1. Definitions

### Definition 10.3.1 — Impulsive Maneuver (Delta-V)

An **impulsive maneuver** is an idealized instantaneous change in velocity $\Delta\mathbf{V}$ applied to a spacecraft. The position remains unchanged; only the velocity vector changes:

$$
\mathbf{v}^+ = \mathbf{v}^- + \Delta\mathbf{V}
$$

The magnitude $\Delta V = |\Delta\mathbf{V}|$ is the primary metric for propellant cost (via the rocket equation, Chapter 10.4).

### Definition 10.3.2 — Hohmann Transfer

A **Hohmann transfer** is a two-impulse coplanar maneuver between two circular orbits using a transfer ellipse that is tangent to both orbits:
- **Burn 1** at periapsis of the transfer ellipse (departure orbit)
- **Burn 2** at apoapsis of the transfer ellipse (arrival orbit)

The transfer ellipse has semi-major axis:

$$
a_t = \frac{r_1 + r_2}{2}
$$

### Definition 10.3.3 — Bi-Elliptic Transfer

A **bi-elliptic transfer** uses three impulses and two transfer ellipses, with an intermediate apoapsis $r_b > r_2$:
1. Burn at $r_1$ to enter first transfer ellipse (apoapsis at $r_b$)
2. Burn at $r_b$ to enter second transfer ellipse (periapsis at $r_2$)
3. Burn at $r_2$ to circularize

### Definition 10.3.4 — Simple Plane Change

A **simple plane change** rotates the orbital plane by angle $\Delta i$ without changing the orbit size. The ΔV is applied perpendicular to the velocity at the node:

$$
\Delta V = 2v\sin\frac{\Delta i}{2}
$$

### Definition 10.3.5 — Combined Plane Change and Transfer

A **combined maneuver** performs both altitude change and plane change simultaneously at one or both burns, reducing total ΔV compared to performing them separately.

### Definition 10.3.6 — Phase Angle for Rendezvous

The **phase angle** $\phi$ is the angular lead that the target must have ahead of the chaser at the time of the transfer initiation, such that the target arrives at the rendezvous point exactly when the chaser does:

$$
\phi = \pi\left(1 - \frac{1}{2^{3/2}}\left(\frac{r_1 + r_2}{r_2}\right)^{3/2}\right) \quad \text{(for Hohmann to outer orbit)}
$$

More generally: $\phi = \omega_{\text{target}} \cdot t_{\text{transfer}}$ subtracted from $\pi$.




---

## 📐 2. Axioms / Postulates

### Axiom 10.3.A1 — Impulsive Thrust Approximation

Thrust is applied instantaneously (burn time $\ll$ orbital period). This is valid when the thrust-to-weight ratio is high (chemical rockets). For low-thrust propulsion (ion engines), continuous thrust models are required instead.

### Axiom 10.3.A2 — Coplanar Orbits

For Hohmann and bi-elliptic transfers, the initial and final orbits lie in the same plane. Plane changes are treated separately or combined.

### Axiom 10.3.A3 — Two-Body Dynamics During Coast

Between burns, the spacecraft follows a Keplerian orbit (no perturbations). The transfer ellipse obeys the same two-body equations derived in Chapter 10.1.

### Axiom 10.3.A4 — Tangential Burns for Hohmann

Both burns in a Hohmann transfer are applied tangentially (along the velocity vector). This maximizes the change in orbital energy for a given ΔV magnitude.

---

## 🛡️ 3. Lemmas

### Lemma 10.3.1 — Velocity on a Circular Orbit

The speed on a circular orbit of radius $r$ is:

$$
v_c = \sqrt{\frac{\mu}{r}}
$$

### Lemma 10.3.2 — Velocity at Periapsis/Apoapsis of an Ellipse

For an ellipse with semi-major axis $a$:

At periapsis ($r = r_p$):

$$
v_p = \sqrt{\mu\left(\frac{2}{r_p} - \frac{1}{a}\right)} = \sqrt{\frac{2\mu r_a}{r_p(r_p + r_a)}}
$$

At apoapsis ($r = r_a$):

$$
v_a = \sqrt{\mu\left(\frac{2}{r_a} - \frac{1}{a}\right)} = \sqrt{\frac{2\mu r_p}{r_a(r_p + r_a)}}
$$

<details>
<summary>🔍 Derivation</summary>

Using Vis-Viva with $a = (r_p + r_a)/2$:

$$
v_p^2 = \mu\left(\frac{2}{r_p} - \frac{2}{r_p + r_a}\right) = \frac{2\mu}{r_p}\left(1 - \frac{r_p}{r_p + r_a}\right) = \frac{2\mu}{r_p}\cdot\frac{r_a}{r_p + r_a} = \frac{2\mu r_a}{r_p(r_p + r_a)}
$$

Similarly for $v_a$. $\blacksquare$

</details>

### Lemma 10.3.3 — Transfer Ellipse Parameters

For a Hohmann transfer from circular orbit $r_1$ to circular orbit $r_2$ ($r_2 > r_1$):

- Semi-major axis: $a_t = (r_1 + r_2)/2$
- Periapsis: $r_p = r_1$ (tangent to inner orbit)
- Apoapsis: $r_a = r_2$ (tangent to outer orbit)
- Eccentricity: $e_t = (r_2 - r_1)/(r_2 + r_1)$

### Lemma 10.3.4 — Optimality of Tangential Burns

**Statement:** For a given ΔV magnitude, a tangential burn (along the velocity vector) produces the maximum change in specific orbital energy.

<details>
<summary>🔍 Proof</summary>

The specific energy is $\varepsilon = v^2/2 - \mu/r$. After an impulsive burn:

$$
\Delta\varepsilon = \frac{|\mathbf{v} + \Delta\mathbf{V}|^2}{2} - \frac{v^2}{2} = \mathbf{v}\cdot\Delta\mathbf{V} + \frac{|\Delta\mathbf{V}|^2}{2}
$$

For fixed $|\Delta\mathbf{V}| = \Delta V$, the term $\mathbf{v}\cdot\Delta\mathbf{V} = v\,\Delta V\cos\alpha$ is maximized when $\alpha = 0$ (tangential burn):

$$
\Delta\varepsilon_{\max} = v\,\Delta V + \frac{\Delta V^2}{2}
$$

$\blacksquare$

</details>

### Lemma 10.3.5 — Hohmann Transfer Time

The transfer time (half the period of the transfer ellipse) is:

$$
t_H = \frac{T_t}{2} = \pi\sqrt{\frac{a_t^3}{\mu}} = \pi\sqrt{\frac{(r_1+r_2)^3}{8\mu}}
$$




---

## 👑 4. Theorems

### Theorem 10.3.1 — Hohmann Transfer ΔV Equations

For a Hohmann transfer from circular orbit of radius $r_1$ to circular orbit of radius $r_2$ ($r_2 > r_1$):

**First burn** (at $r_1$, prograde):

$$
\Delta V_1 = v_{t,p} - v_{c,1} = \sqrt{\frac{2\mu r_2}{r_1(r_1+r_2)}} - \sqrt{\frac{\mu}{r_1}} = \sqrt{\frac{\mu}{r_1}}\left(\sqrt{\frac{2r_2}{r_1+r_2}} - 1\right)
$$

**Second burn** (at $r_2$, prograde):

$$
\Delta V_2 = v_{c,2} - v_{t,a} = \sqrt{\frac{\mu}{r_2}} - \sqrt{\frac{2\mu r_1}{r_2(r_1+r_2)}} = \sqrt{\frac{\mu}{r_2}}\left(1 - \sqrt{\frac{2r_1}{r_1+r_2}}\right)
$$

**Total ΔV:**

$$
\Delta V_{\text{total}} = \Delta V_1 + \Delta V_2
$$

### Theorem 10.3.2 — Hohmann Transfer is Optimal (for $r_2/r_1 < 11.94$)

The Hohmann transfer is the minimum-ΔV two-impulse coplanar transfer between two circular orbits when the radius ratio satisfies $r_2/r_1 < 11.94$. Beyond this ratio, the bi-elliptic transfer becomes more efficient.

### Theorem 10.3.3 — Bi-Elliptic Transfer ΔV

For a bi-elliptic transfer from $r_1$ to $r_2$ via intermediate apoapsis $r_b$:

$$
\Delta V_1 = \sqrt{\frac{2\mu r_b}{r_1(r_1+r_b)}} - \sqrt{\frac{\mu}{r_1}}
$$

$$
\Delta V_2 = \sqrt{\frac{2\mu r_2}{r_b(r_2+r_b)}} - \sqrt{\frac{2\mu r_1}{r_b(r_1+r_b)}}
$$

$$
\Delta V_3 = \sqrt{\frac{\mu}{r_2}} - \sqrt{\frac{2\mu r_b}{r_2(r_2+r_b)}}
$$

Note: $\Delta V_2$ is applied at $r_b$ and may be retrograde (reducing apoapsis from $r_b$ to $r_2$ if $r_b > r_2$).

### Theorem 10.3.4 — Simple Plane Change ΔV

To rotate the orbital plane by angle $\Delta i$ at a point where the orbital speed is $v$:

$$
\Delta V = 2v\sin\frac{\Delta i}{2}
$$

This is minimized by performing the plane change where $v$ is smallest (at apoapsis for elliptical orbits).

### Theorem 10.3.5 — Combined Altitude and Plane Change

When combining a Hohmann transfer with a plane change at the second burn (at apoapsis of transfer):

$$
\Delta V_2 = \sqrt{v_{c,2}^2 + v_{t,a}^2 - 2v_{c,2}\,v_{t,a}\cos\Delta i}
$$

This uses the law of cosines on the velocity triangle. The combined ΔV is always less than the sum of separate altitude-change and plane-change ΔVs.

### Theorem 10.3.6 — Phase Angle for Hohmann Rendezvous

For a Hohmann transfer from inner orbit $r_1$ to rendezvous with a target on outer orbit $r_2$:

The required phase angle (target ahead of chaser) at departure:

$$
\phi = \pi - \omega_2 \cdot t_H = \pi - \frac{2\pi}{T_2}\cdot\pi\sqrt{\frac{a_t^3}{\mu}}
$$

$$
= \pi\left(1 - \sqrt{\frac{(r_1+r_2)^3}{8r_2^3}}\right)
$$

The wait time between launch windows:

$$
t_{\text{wait}} = \frac{2\pi - \Delta\phi}{|\omega_1 - \omega_2|}
$$

where $\Delta\phi$ is the phase angle error at the missed window.

---

## ✍️ 5. Proofs / Derivations

### 5.1 Complete Derivation of Hohmann Transfer ΔV₁

**Goal:** Derive $\Delta V_1 = \sqrt{\frac{\mu}{r_1}}\left(\sqrt{\frac{2r_2}{r_1+r_2}} - 1\right)$.

**Step 1:** The spacecraft starts on a circular orbit of radius $r_1$ with velocity:

$$
v_{c,1} = \sqrt{\frac{\mu}{r_1}}
$$

**Step 2:** After burn 1, the spacecraft is at periapsis of the transfer ellipse. The transfer ellipse has:
- Periapsis: $r_p = r_1$
- Apoapsis: $r_a = r_2$
- Semi-major axis: $a_t = (r_1 + r_2)/2$

**Step 3:** Apply Vis-Viva at periapsis of the transfer ellipse:

$$
v_{t,p} = \sqrt{\mu\left(\frac{2}{r_1} - \frac{1}{a_t}\right)} = \sqrt{\mu\left(\frac{2}{r_1} - \frac{2}{r_1+r_2}\right)}
$$

**Step 4:** Simplify the bracket:

$$
\frac{2}{r_1} - \frac{2}{r_1+r_2} = \frac{2(r_1+r_2) - 2r_1}{r_1(r_1+r_2)} = \frac{2r_2}{r_1(r_1+r_2)}
$$

**Step 5:** Therefore:

$$
v_{t,p} = \sqrt{\frac{2\mu r_2}{r_1(r_1+r_2)}}
$$

**Step 6:** The ΔV is the difference (both velocities are tangential and in the same direction):

$$
\Delta V_1 = v_{t,p} - v_{c,1} = \sqrt{\frac{2\mu r_2}{r_1(r_1+r_2)}} - \sqrt{\frac{\mu}{r_1}}
$$

**Step 7:** Factor out $\sqrt{\mu/r_1}$:

$$
\Delta V_1 = \sqrt{\frac{\mu}{r_1}}\left(\sqrt{\frac{2r_2}{r_1+r_2}} - 1\right)
$$

$\blacksquare$

### 5.2 Complete Derivation of Hohmann Transfer ΔV₂

**Goal:** Derive $\Delta V_2 = \sqrt{\frac{\mu}{r_2}}\left(1 - \sqrt{\frac{2r_1}{r_1+r_2}}\right)$.

**Step 1:** At apoapsis of the transfer ellipse ($r = r_2$), the velocity is:

$$
v_{t,a} = \sqrt{\mu\left(\frac{2}{r_2} - \frac{2}{r_1+r_2}\right)} = \sqrt{\frac{2\mu r_1}{r_2(r_1+r_2)}}
$$

(Following the same algebra as 5.1 with $r_1 \leftrightarrow r_2$ in the numerator.)

**Step 2:** The target circular orbit velocity at $r_2$ is:

$$
v_{c,2} = \sqrt{\frac{\mu}{r_2}}
$$

**Step 3:** Since $v_{t,a} < v_{c,2}$ (the spacecraft arrives too slowly), a prograde burn is needed:

$$
\Delta V_2 = v_{c,2} - v_{t,a} = \sqrt{\frac{\mu}{r_2}} - \sqrt{\frac{2\mu r_1}{r_2(r_1+r_2)}}
$$

$$
= \sqrt{\frac{\mu}{r_2}}\left(1 - \sqrt{\frac{2r_1}{r_1+r_2}}\right)
$$

$\blacksquare$

### 5.3 Derivation of the Plane Change ΔV

**Goal:** Derive $\Delta V = 2v\sin(\Delta i/2)$.

**Step 1:** Before the maneuver, velocity is $\mathbf{v}^-$ with magnitude $v$. After, velocity is $\mathbf{v}^+$ with the same magnitude $v$ (pure rotation, no altitude change).

**Step 2:** The angle between $\mathbf{v}^-$ and $\mathbf{v}^+$ is $\Delta i$ (the plane change angle).

**Step 3:** By the law of cosines on the velocity triangle:

$$
|\Delta\mathbf{V}|^2 = |\mathbf{v}^-|^2 + |\mathbf{v}^+|^2 - 2|\mathbf{v}^-||\mathbf{v}^+|\cos\Delta i
$$

$$
= v^2 + v^2 - 2v^2\cos\Delta i = 2v^2(1 - \cos\Delta i)
$$

**Step 4:** Use the identity $1 - \cos\alpha = 2\sin^2(\alpha/2)$:

$$
\Delta V^2 = 2v^2 \cdot 2\sin^2\frac{\Delta i}{2} = 4v^2\sin^2\frac{\Delta i}{2}
$$

$$
\Delta V = 2v\sin\frac{\Delta i}{2}
$$

$\blacksquare$

### 5.4 Derivation of Combined Maneuver ΔV (Law of Cosines)

**Goal:** When combining altitude change and plane change at a single burn.

**Step 1:** At the burn point, the initial velocity is $v_1$ (on the transfer orbit) and the desired final velocity is $v_2$ (on the target orbit), with angle $\Delta i$ between them.

**Step 2:** The required ΔV is the third side of the velocity triangle:

$$
\Delta V = \sqrt{v_1^2 + v_2^2 - 2v_1 v_2\cos\Delta i}
$$

**Step 3:** Compare with doing them separately:
- Altitude change alone: $|v_2 - v_1|$
- Plane change alone: $2v_2\sin(\Delta i/2)$
- Sum: $|v_2 - v_1| + 2v_2\sin(\Delta i/2)$

The combined ΔV is always less than or equal to this sum (triangle inequality). The savings are greatest when the plane change is performed at the highest altitude (lowest velocity). $\blacksquare$

### 5.5 Derivation of the Bi-Elliptic Crossover Ratio

**Goal:** Find the radius ratio $r_2/r_1$ above which bi-elliptic (with $r_b \to \infty$) beats Hohmann.

**Step 1:** For the limiting bi-elliptic case ($r_b \to \infty$), the first and third burns approach escape/capture:

$$
\Delta V_1^{BE} = v_{\text{esc},1} - v_{c,1} = (\sqrt{2} - 1)\sqrt{\frac{\mu}{r_1}}
$$

$$
\Delta V_3^{BE} = v_{\text{esc},2} - v_{c,2} = (\sqrt{2} - 1)\sqrt{\frac{\mu}{r_2}}
$$

$$
\Delta V_2^{BE} \to 0 \text{ (at infinity)}
$$

$$
\Delta V_{\text{total}}^{BE} = (\sqrt{2}-1)\left(\sqrt{\frac{\mu}{r_1}} + \sqrt{\frac{\mu}{r_2}}\right)
$$

**Step 2:** Set equal to Hohmann total ΔV and solve for $R = r_2/r_1$. Let $k = \sqrt{R}$:

$$
(\sqrt{2}-1)\sqrt{\frac{\mu}{r_1}}\left(1 + \frac{1}{k}\right) = \sqrt{\frac{\mu}{r_1}}\left[\sqrt{\frac{2R}{1+R}} - 1 + \frac{1}{k}\left(1 - \sqrt{\frac{2}{1+R}}\right)\right]
$$

Numerical solution yields $R = r_2/r_1 \approx 11.94$.

For $r_2/r_1 > 11.94$: bi-elliptic is more efficient (in ΔV, not time).
For $r_2/r_1 < 11.94$: Hohmann is more efficient.

$\blacksquare$




---

## 🧮 6. Worked Examples

### Example 10.3.1 — LEO to GEO Hohmann Transfer

**Given:** LEO altitude $h_1 = 300$ km, GEO altitude $h_2 = 35{,}786$ km. $R_E = 6371$ km, $\mu = 398{,}600.4$ km³/s².

**Find:** $\Delta V_1$, $\Delta V_2$, total $\Delta V$, and transfer time.

**Solution:**

Step 1: Orbital radii:

$$
r_1 = 6371 + 300 = 6671 \text{ km}, \quad r_2 = 6371 + 35786 = 42157 \text{ km}
$$

Step 2: Circular velocities:

$$
v_{c,1} = \sqrt{\frac{398600.4}{6671}} = \sqrt{59.75} = 7.730 \text{ km/s}
$$

$$
v_{c,2} = \sqrt{\frac{398600.4}{42157}} = \sqrt{9.455} = 3.075 \text{ km/s}
$$

Step 3: Transfer ellipse semi-major axis:

$$
a_t = \frac{r_1 + r_2}{2} = \frac{6671 + 42157}{2} = 24414 \text{ km}
$$

Step 4: First burn:

$$
\Delta V_1 = \sqrt{\frac{\mu}{r_1}}\left(\sqrt{\frac{2r_2}{r_1+r_2}} - 1\right) = 7.730\left(\sqrt{\frac{2 \times 42157}{48828}} - 1\right)
$$

$$
= 7.730\left(\sqrt{1.7268} - 1\right) = 7.730(1.3141 - 1) = 7.730 \times 0.3141 = 2.428 \text{ km/s}
$$

Step 5: Second burn:

$$
\Delta V_2 = \sqrt{\frac{\mu}{r_2}}\left(1 - \sqrt{\frac{2r_1}{r_1+r_2}}\right) = 3.075\left(1 - \sqrt{\frac{2 \times 6671}{48828}}\right)
$$

$$
= 3.075\left(1 - \sqrt{0.2732}\right) = 3.075(1 - 0.5227) = 3.075 \times 0.4773 = 1.468 \text{ km/s}
$$

Step 6: Total ΔV:

$$
\Delta V_{\text{total}} = 2.428 + 1.468 = 3.896 \text{ km/s}
$$

Step 7: Transfer time:

$$
t_H = \pi\sqrt{\frac{a_t^3}{\mu}} = \pi\sqrt{\frac{(24414)^3}{398600.4}} = \pi\sqrt{\frac{1.456\times10^{13}}{398600.4}} = \pi\sqrt{3.653\times10^7}
$$

$$
= \pi \times 6044 = 18{,}987 \text{ s} = 5.27 \text{ hours}
$$

---

### Example 10.3.2 — Bi-Elliptic vs. Hohmann (Large Ratio)

**Given:** Transfer from $r_1 = 7000$ km to $r_2 = 105{,}000$ km ($r_2/r_1 = 15 > 11.94$). Intermediate apoapsis $r_b = 210{,}000$ km. $\mu = 398{,}600.4$ km³/s².

**Find:** Compare total ΔV for Hohmann and bi-elliptic.

**Solution — Hohmann:**

$$
\Delta V_1^H = \sqrt{\frac{398600.4}{7000}}\left(\sqrt{\frac{2\times105000}{112000}} - 1\right) = 7.547\left(\sqrt{1.875} - 1\right) = 7.547(0.3693) = 2.787 \text{ km/s}
$$

$$
\Delta V_2^H = \sqrt{\frac{398600.4}{105000}}\left(1 - \sqrt{\frac{2\times7000}{112000}}\right) = 1.948\left(1 - 0.3536\right) = 1.948(0.6464) = 1.259 \text{ km/s}
$$

$$
\Delta V_{\text{Hohmann}} = 2.787 + 1.259 = 4.046 \text{ km/s}
$$

**Solution — Bi-elliptic:**

First transfer: $r_1 = 7000$, apoapsis $r_b = 210000$, $a_1 = 108500$ km:

$$
\Delta V_1^{BE} = \sqrt{\frac{2\mu \cdot r_b}{r_1(r_1+r_b)}} - \sqrt{\frac{\mu}{r_1}} = \sqrt{\frac{2(398600.4)(210000)}{7000(217000)}} - 7.547
$$

$$
= \sqrt{\frac{1.674\times10^{11}}{1.519\times10^9}} - 7.547 = \sqrt{110.2} - 7.547 = 10.497 - 7.547 = 2.950 \text{ km/s}
$$

Second transfer at $r_b$: need velocity on first ellipse at $r_b$ and velocity on second ellipse at $r_b$:

$$
v_{b,1} = \sqrt{\frac{2\mu r_1}{r_b(r_1+r_b)}} = \sqrt{\frac{2(398600.4)(7000)}{210000(217000)}} = \sqrt{\frac{5.580\times10^9}{4.557\times10^{10}}} = \sqrt{0.1224} = 0.3499 \text{ km/s}
$$

Second ellipse: $r_b = 210000$ (apoapsis), $r_2 = 105000$ (periapsis), $a_2 = 157500$ km:

$$
v_{b,2} = \sqrt{\frac{2\mu r_2}{r_b(r_2+r_b)}} = \sqrt{\frac{2(398600.4)(105000)}{210000(315000)}} = \sqrt{\frac{8.371\times10^{10}}{6.615\times10^{10}}} = \sqrt{1.265} = 1.125 \text{ km/s}
$$

$$
\Delta V_2^{BE} = |v_{b,2} - v_{b,1}| = |1.125 - 0.3499| = 0.775 \text{ km/s}
$$

Third burn at $r_2$: circularize from second transfer ellipse:

$$
v_{p,2} = \sqrt{\frac{2\mu r_b}{r_2(r_2+r_b)}} = \sqrt{\frac{2(398600.4)(210000)}{105000(315000)}} = \sqrt{\frac{1.674\times10^{11}}{3.308\times10^{10}}} = \sqrt{5.061} = 2.250 \text{ km/s}
$$

$$
v_{c,2} = \sqrt{\frac{398600.4}{105000}} = 1.948 \text{ km/s}
$$

$$
\Delta V_3^{BE} = v_{p,2} - v_{c,2} = 2.250 - 1.948 = 0.302 \text{ km/s}
$$

$$
\Delta V_{\text{bi-elliptic}} = 2.950 + 0.775 + 0.302 = 4.027 \text{ km/s}
$$

**Comparison:** Bi-elliptic saves $4.046 - 4.027 = 0.019$ km/s (0.5%). The savings are small but real for $r_2/r_1 = 15$. The trade-off is much longer transfer time.

---

### Example 10.3.3 — GEO Insertion with 28.5° Plane Change

**Given:** Spacecraft in GTO (perigee 300 km, apogee 35,786 km, $i = 28.5°$). Perform combined circularization and plane change at apogee.

**Find:** ΔV for combined maneuver vs. separate maneuvers.

**Solution:**

Step 1: Velocities at apogee. $r_a = 42157$ km, $r_p = 6671$ km, $a_t = 24414$ km.

$$
v_{t,a} = \sqrt{398600.4\left(\frac{2}{42157} - \frac{1}{24414}\right)} = \sqrt{398600.4(4.744\times10^{-5} - 4.096\times10^{-5})}
$$

$$
= \sqrt{398600.4 \times 6.48\times10^{-6}} = \sqrt{2.583} = 1.607 \text{ km/s}
$$

$$
v_{c,\text{GEO}} = 3.075 \text{ km/s}
$$

Step 2: Combined maneuver (law of cosines with $\Delta i = 28.5°$):

$$
\Delta V_{\text{combined}} = \sqrt{v_{t,a}^2 + v_{c}^2 - 2v_{t,a}v_c\cos\Delta i}
$$

$$
= \sqrt{1.607^2 + 3.075^2 - 2(1.607)(3.075)\cos28.5°}
$$

$$
= \sqrt{2.582 + 9.456 - 9.882 \times 0.8788} = \sqrt{2.582 + 9.456 - 8.684} = \sqrt{3.354} = 1.832 \text{ km/s}
$$

Step 3: Separate maneuvers:
- Circularize: $\Delta V_{\text{circ}} = 3.075 - 1.607 = 1.468$ km/s
- Plane change at GEO: $\Delta V_{\text{plane}} = 2(3.075)\sin(14.25°) = 6.15 \times 0.2462 = 1.514$ km/s
- Total separate: $1.468 + 1.514 = 2.982$ km/s

**Savings:** $2.982 - 1.832 = 1.150$ km/s (38.6% reduction!). Combined maneuvers are dramatically more efficient.

---

### Example 10.3.4 — Phasing Maneuver for Rendezvous

**Given:** Chaser and target both in circular orbit at $r = 7000$ km. Target is $\phi_0 = 20°$ ahead of chaser. $\mu = 398{,}600.4$ km³/s².

**Find:** Design a phasing orbit to rendezvous in one revolution of the phasing orbit.

**Solution:**

Step 1: Angular velocity on the circular orbit:

$$
\omega = \sqrt{\frac{\mu}{r^3}} = \sqrt{\frac{398600.4}{7000^3}} = \sqrt{\frac{398600.4}{3.43\times10^{11}}} = 1.078\times10^{-3} \text{ rad/s}
$$

Step 2: The chaser must travel $360° + 20° = 380°$ in the time the target travels $360°$.

Target period: $T = 2\pi/\omega = 5828$ s.

Step 3: Phasing orbit period (chaser must complete 380° = $380/360 \times T_{\text{phase}}$ in time $T$):

Actually, the chaser completes one full revolution of its phasing orbit in time $T_{\text{phase}}$, during which the target moves $\omega \cdot T_{\text{phase}}$ radians. We need:

$$
2\pi - \phi_0 = \omega \cdot T_{\text{phase}} \quad \text{(target moves this much while chaser does full loop)}
$$

Wait — let me reconsider. The chaser drops to a lower (faster) phasing orbit. After one period of the phasing orbit, the chaser returns to the original altitude. During that time, the target has moved less than one full revolution.

For the chaser to gain $\phi_0 = 20° = 0.349$ rad on the target:

$$
T_{\text{phase}} = T\left(1 - \frac{\phi_0}{2\pi}\right) = 5828\left(1 - \frac{20}{360}\right) = 5828 \times 0.9444 = 5504 \text{ s}
$$

Step 4: Phasing orbit semi-major axis:

$$
a_{\text{phase}} = \left(\frac{\mu T_{\text{phase}}^2}{4\pi^2}\right)^{1/3} = \left(\frac{398600.4 \times 5504^2}{4\pi^2}\right)^{1/3}
$$

$$
= \left(\frac{398600.4 \times 3.029\times10^7}{39.48}\right)^{1/3} = (3.059\times10^{11})^{1/3} = 6737 \text{ km}
$$

Step 5: ΔV to enter phasing orbit (Hohmann-like, with $r_1 = 7000$, periapsis of phasing orbit at $r_p = 2a_{\text{phase}} - r_1 = 13474 - 7000 = 6474$ km):

Wait — the phasing orbit has the same apoapsis as the original orbit ($r_a = 7000$ km) and a lower periapsis. So $a_{\text{phase}} = (r_p + 7000)/2 = 6737$, giving $r_p = 6474$ km.

$$
\Delta V_1 = v_{c} - v_{a,\text{phase}} = \sqrt{\frac{\mu}{7000}} - \sqrt{\frac{2\mu \cdot r_p}{7000(r_p + 7000)}}
$$

Hmm, actually the burn is retrograde (slowing down to drop periapsis):

$$
v_{a,\text{phase}} = \sqrt{\frac{2\mu r_p}{r_a(r_p+r_a)}} = \sqrt{\frac{2(398600.4)(6474)}{7000(13474)}} = \sqrt{\frac{5.161\times10^9}{9.432\times10^7}} = \sqrt{54.72} = 7.397 \text{ km/s}
$$

$$
v_c = 7.547 \text{ km/s}
$$

$$
\Delta V_1 = 7.547 - 7.397 = 0.150 \text{ km/s (retrograde)}
$$

After one phasing orbit period, the chaser returns to $r = 7000$ km and burns prograde by the same amount:

$$
\Delta V_2 = 0.150 \text{ km/s (prograde)}
$$

$$
\Delta V_{\text{total}} = 0.300 \text{ km/s}
$$

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links

- [10.1 - Two-Body Problem & Kepler's Laws](10.1---Two-Body-Problem-&-Kepler's-Laws) — Vis-Viva equation used throughout
- [10.2 - Orbital Elements & Conic Sections](10.2---Orbital-Elements-&-Conic-Sections) — Transfer orbit element computation
- [10.4 - Rocket Equation & Propulsion Systems](10.4---Rocket-Equation-&-Propulsion-Systems) — Converting ΔV to propellant mass
- [10.7 - Interplanetary Trajectories - Patched Conics](10.7---Interplanetary-Trajectories---Patched-Conics) — Hohmann applied to planetary transfers
- [4.4 - Central Forces & Keplerian Orbits](4.4---Central-Forces-&-Keplerian-Orbits) — Energy and angular momentum conservation

### Authoritative External Sources

| Source | Description |
|--------|-------------|
| Curtis, H.D. *Orbital Mechanics for Engineering Students*, Ch. 6 | Orbital maneuvers and Hohmann transfers |
| MIT OCW 16.346, Lectures 8–10 | Impulsive maneuver optimization |
| Bate, Mueller & White, Ch. 6 | Ballistic missile and satellite maneuvers |
| Vallado, Ch. 6 | Maneuver planning with perturbations |
| Prussing & Conway, *Orbital Mechanics* (Oxford, 2012) | Optimal transfer theory |




---

## 📎 Appendix — Additional Topics

### A.1 General Coplanar Transfer (Non-Circular Orbits)

For a transfer between two elliptical orbits, the ΔV at each burn is computed using the Vis-Viva equation at the burn point, accounting for the velocity direction (flight path angle):

$$
\Delta V = \sqrt{v_1^2 + v_2^2 - 2v_1 v_2\cos\Delta\gamma}
$$

where $\Delta\gamma$ is the difference in flight path angles between the initial orbit and the transfer orbit at the burn point.

### A.2 Orbit Raising with Finite Thrust (Low-Thrust Spiral)

For electric propulsion with continuous low thrust, the spacecraft spirals outward. The ΔV for a quasi-circular spiral from $r_1$ to $r_2$ is approximately:

$$
\Delta V_{\text{spiral}} \approx v_{c,1} - v_{c,2} = \sqrt{\frac{\mu}{r_1}} - \sqrt{\frac{\mu}{r_2}}
$$

This is **less** than the Hohmann ΔV, but the transfer takes much longer (weeks to months vs. hours).

### A.3 Apse Line Rotation

To rotate the apse line (argument of periapsis) by angle $\eta$ without changing $a$ or $e$, a single tangential burn at the intersection of the initial and final orbits can be used. The required true anomaly for the burn:

$$
\theta_{\text{burn}} = \frac{\pi - \eta}{2}
$$

### Example 10.3.5 — Low-Thrust Spiral vs Hohmann

**Given:** Transfer from 400 km LEO to 35,786 km GEO. $\mu = 398{,}600.4$ km³/s².

**Find:** Compare ΔV for Hohmann vs. low-thrust spiral.

**Solution:**

Hohmann (from Example 10.3.1): $\Delta V_H = 3.896$ km/s

Low-thrust spiral:

$$
\Delta V_{\text{spiral}} = v_{c,1} - v_{c,2} = \sqrt{\frac{398600.4}{6771}} - \sqrt{\frac{398600.4}{42157}} = 7.669 - 3.075 = 4.594 \text{ km/s}
$$

The spiral requires 18% more ΔV than Hohmann, but with an ion thruster ($I_{sp} = 3000$ s vs 320 s), the propellant mass is still much less:

- Hohmann (chemical, $I_{sp}=320$ s): $R = e^{3.896/3.138} = 3.46$, propellant = 71% of initial mass
- Spiral (ion, $I_{sp}=3000$ s): $R = e^{4.594/29.42} = 1.169$, propellant = 14.5% of initial mass

