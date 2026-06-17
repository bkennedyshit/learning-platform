---
title: "8.4 — Equivalence Principle & Curved Spacetime"
subject: "Special & General Relativity"
catalog: advanced
audience_tier: higher-education
chapter: "8.4"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 8.4 — Equivalence Principle & Curved Spacetime

> *"I was sitting in a chair in the patent office at Bern when all of a sudden a thought occurred to me: 'If a person falls freely he will not feel his own weight.' I was startled. This simple thought made a deep impression on me. It impelled me toward a theory of gravitation."*
> — Albert Einstein, recalling the "happiest thought of my life" (1907)

Special Relativity describes physics in the absence of gravity — in flat Minkowski spacetime. But gravity is the dominant force on cosmic scales. Einstein's profound insight was that gravity is not a force at all — it is the **curvature of spacetime itself**. A freely falling particle follows a geodesic (the "straightest possible path") through curved spacetime, experiencing no force.

This chapter develops the physical reasoning that leads from SR to GR: the Equivalence Principle, its immediate consequences (gravitational redshift, light bending, time dilation in gravitational fields), and the conceptual leap to curved spacetime geometry.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. State the Weak, Einstein, and Strong Equivalence Principles and distinguish between them.
2. Derive gravitational time dilation from the Equivalence Principle.
3. Derive the gravitational redshift formula $\Delta f/f = -g\Delta h/c^2$.
4. Explain why gravity must curve spacetime (tidal forces cannot be eliminated globally).
5. Distinguish between "gravitational acceleration" (eliminable) and "tidal acceleration" (intrinsic curvature).
6. Write the Newtonian limit of the metric: $g_{00} \approx -(1 + 2\Phi/c^2)$.
7. Explain the deflection of light in a gravitational field using the EP.
8. Motivate the need for differential geometry (Chapters 8.5–8.7) to describe curved spacetime.

---

## 🖼️ Visual Anchor — Einstein's Elevator & Tidal Forces

![math-08__8.4-fig1](math-08__8.4-fig1.svg)

---

## 📚 1. Definitions

### Definition 8.4.1 — Weak Equivalence Principle (WEP)

The trajectory of a freely falling test body is independent of its internal structure and composition. Equivalently: **inertial mass equals gravitational mass** for all bodies.

$$
m_{\text{inertial}} = m_{\text{gravitational}}
$$

This has been verified to extraordinary precision: Eötvös experiments achieve $|m_i - m_g|/m < 10^{-15}$.

### Definition 8.4.2 — Einstein Equivalence Principle (EEP)

1. The WEP holds.
2. The outcome of any local non-gravitational experiment is independent of the velocity of the freely-falling reference frame in which it is performed (**Local Lorentz Invariance**).
3. The outcome of any local non-gravitational experiment is independent of where and when in the universe it is performed (**Local Position Invariance**).

**Consequence:** In a sufficiently small freely-falling laboratory, the laws of physics reduce to those of Special Relativity. Gravity "disappears" locally.

### Definition 8.4.3 — Strong Equivalence Principle (SEP)

The EEP extended to include gravitational experiments and self-gravitating bodies. Even the gravitational binding energy contributes equally to inertial and gravitational mass. GR satisfies the SEP; most alternative theories of gravity do not.

### Definition 8.4.4 — Tidal Force (Geodesic Deviation)

The **tidal acceleration** between two nearby freely-falling particles separated by displacement $\xi^i$ in Newtonian gravity is:

$$
\ddot{\xi}^i = -\frac{\partial^2 \Phi}{\partial x^i \partial x^j}\xi^j
$$

where $\Phi$ is the Newtonian gravitational potential. The matrix $\partial^2\Phi/\partial x^i\partial x^j$ is the **tidal tensor** — it cannot be eliminated by any choice of reference frame. In GR, this becomes the **Riemann curvature tensor**.

### Definition 8.4.5 — Gravitational Redshift

A photon climbing out of a gravitational potential well loses energy. For a static weak gravitational field with potential $\Phi$:

$$
\frac{\Delta f}{f} = \frac{\Phi_{\text{emit}} - \Phi_{\text{obs}}}{c^2}
$$

For a uniform field of strength $g$ over height $h$:

$$
\frac{\Delta f}{f} = -\frac{gh}{c^2}
$$

(negative = redshift for upward propagation).

### Definition 8.4.6 — Newtonian Limit of the Metric

In the weak-field, slow-motion limit, the spacetime metric takes the form:

$$
ds^2 = -\left(1 + \frac{2\Phi}{c^2}\right)c^2 dt^2 + \left(1 - \frac{2\Phi}{c^2}\right)(dx^2 + dy^2 + dz^2)
$$

where $\Phi$ is the Newtonian gravitational potential ($\Phi < 0$ near a mass). The time-time component $g_{00} = -(1 + 2\Phi/c^2)$ encodes gravitational time dilation.




---

## 📐 2. Axioms / Postulates

### Postulate 8.4.1 — General Covariance

The laws of physics must be expressible in a form that is valid in **all** coordinate systems (not just inertial frames). Physical laws are written as tensor equations on a curved manifold — they are invariant under arbitrary smooth coordinate transformations.

### Postulate 8.4.2 — Gravity is Geometry

The gravitational field is not a force field on a fixed background spacetime. Instead, gravity **is** the curvature of spacetime. Matter tells spacetime how to curve; spacetime tells matter how to move.

### Postulate 8.4.3 — Free Fall is Geodesic Motion

In the absence of non-gravitational forces, a test particle follows a **geodesic** of the spacetime metric — the path that extremizes proper time. There is no "gravitational force" in GR; what we perceive as gravity is the curvature of the geodesics.

---

## 🛡️ 3. Lemmas

### Lemma 8.4.1 — Gravitational Time Dilation from the Equivalence Principle

**Statement:** A clock at gravitational potential $\Phi$ runs at rate:

$$
d\tau = dt\sqrt{1 + \frac{2\Phi}{c^2}} \approx dt\left(1 + \frac{\Phi}{c^2}\right)
$$

relative to a clock at $\Phi = 0$ (infinity).

**Proof:**

**Step 1:** By the EP, a uniform gravitational field $g$ is equivalent to an accelerating frame. Consider two clocks separated by height $h$ in a rocket accelerating at $g$.

**Step 2:** The bottom clock emits a photon upward. During the photon's travel time $\Delta t \approx h/c$, the top of the rocket has gained additional velocity $\Delta v = g \cdot h/c$.

**Step 3:** By the Doppler effect, the top clock receives the photon blueshifted by:

$$
\frac{\Delta f}{f} = \frac{\Delta v}{c} = \frac{gh}{c^2}
$$

Wait — the top is moving toward the photon (in the instantaneous rest frame at emission), so it's blueshifted. But from the perspective of the top clock, the bottom clock appears to tick **slower**.

**Step 4:** By the EP, this is identical to a gravitational field. The clock at lower potential (bottom, $\Phi_{\text{bottom}} = -gh$ relative to top) ticks slower:

$$
\frac{d\tau_{\text{bottom}}}{d\tau_{\text{top}}} = 1 - \frac{gh}{c^2} = 1 + \frac{\Phi_{\text{bottom}} - \Phi_{\text{top}}}{c^2}
$$

**Step 5:** Generalizing: relative to a clock at infinity ($\Phi = 0$):

$$
d\tau = dt\sqrt{1 + \frac{2\Phi}{c^2}} \approx dt\left(1 + \frac{\Phi}{c^2}\right) \qquad \blacksquare
$$

(The factor of 2 in the exact expression comes from the full metric; the linear approximation gives the leading-order result.)

### Lemma 8.4.2 — Light Deflection from the Equivalence Principle

**Statement:** A photon passing a mass $M$ at impact parameter $b$ is deflected by angle:

$$
\delta\phi_{\text{EP}} = \frac{2GM}{c^2 b}
$$

(This is the "Newtonian" prediction. GR gives exactly **twice** this: $\delta\phi_{\text{GR}} = 4GM/(c^2 b)$, because spatial curvature contributes equally.)

**Proof (EP argument):**

**Step 1:** In a freely-falling frame, light travels in a straight line (EP). Transform to the frame of the massive body.

**Step 2:** The freely-falling frame accelerates at $g = GM/b^2$ (at closest approach) relative to the mass.

**Step 3:** During the time the photon is near the mass ($\Delta t \approx 2b/c$), the transverse velocity acquired is:

$$
\Delta v_\perp = g \cdot \Delta t = \frac{GM}{b^2} \cdot \frac{2b}{c} = \frac{2GM}{bc}
$$

**Step 4:** The deflection angle:

$$
\delta\phi = \frac{\Delta v_\perp}{c} = \frac{2GM}{c^2 b} \qquad \blacksquare
$$

### Lemma 8.4.3 — Impossibility of a Global Inertial Frame in Curved Spacetime

**Statement:** If tidal forces are non-zero ($\partial^2\Phi/\partial x^i\partial x^j \neq 0$), no single coordinate transformation can eliminate the gravitational field everywhere simultaneously.

**Proof:** The EP guarantees we can find coordinates where $g_{\mu\nu} = \eta_{\mu\nu}$ and $\partial_\alpha g_{\mu\nu} = 0$ at a **single point** (local inertial frame). But the second derivatives $\partial_\alpha\partial_\beta g_{\mu\nu}$ encode the Riemann curvature tensor, which is a **tensor** — if it is non-zero in one frame, it is non-zero in all frames. Therefore, curvature (tidal forces) cannot be transformed away. $\blacksquare$

---

## 👑 4. Theorems

### Theorem 8.4.1 — Gravitational Redshift Formula

**Statement:** For a photon emitted at potential $\Phi_1$ and received at potential $\Phi_2$:

$$
\frac{f_2}{f_1} = \sqrt{\frac{1 + 2\Phi_1/c^2}{1 + 2\Phi_2/c^2}} \approx 1 + \frac{\Phi_1 - \Phi_2}{c^2}
$$

For the Schwarzschild metric at radius $r$ from mass $M$:

$$
\frac{f_\infty}{f_r} = \sqrt{1 - \frac{2GM}{rc^2}} = \sqrt{1 - \frac{r_s}{r}}
$$

where $r_s = 2GM/c^2$ is the Schwarzschild radius.

### Theorem 8.4.2 — Pound-Rebka Prediction

**Statement:** A photon traveling upward through height $h$ in Earth's gravitational field experiences a fractional frequency shift:

$$
\frac{\Delta f}{f} = -\frac{gh}{c^2} = -\frac{9.8 \times 22.5}{(3\times10^8)^2} = -2.46 \times 10^{-15}
$$

(for the original Pound-Rebka experiment with $h = 22.5$ m). This was confirmed in 1959 to 10% accuracy, and later to 1%.

### Theorem 8.4.3 — GPS Time Correction

**Statement:** GPS satellites at altitude $h \approx 20{,}200$ km experience two competing effects:
1. **Gravitational blueshift** (clocks run faster at higher potential): $+45.7\,\mu\text{s/day}$
2. **Velocity time dilation** (SR, clocks run slower due to orbital speed): $-7.2\,\mu\text{s/day}$

Net effect: GPS clocks run **faster** by $38.5\,\mu\text{s/day}$ relative to ground clocks. Without GR corrections, GPS would accumulate $\sim 10$ km/day of position error.

---

## ✍️ 5. Proofs / Derivations

### Proof 8.4.1 — Gravitational Redshift from Metric

**Setup:** Static metric $ds^2 = g_{00}(r)\, c^2 dt^2 + g_{rr}(r)\, dr^2 + r^2 d\Omega^2$. A photon is emitted at $r_1$ and received at $r_2$.

**Step 1:** For a static metric, the time-translation Killing vector $\xi^\mu = (1,0,0,0)$ gives a conserved quantity along geodesics:

$$
E = -g_{\mu\nu}\xi^\mu p^\nu = -g_{00}\, p^0 = \text{const along the photon path}
$$

**Step 2:** The frequency measured by a static observer at radius $r$ is:

$$
f = -\frac{p_\mu u^\mu}{h}
$$

where $u^\mu$ is the observer's 4-velocity. For a static observer: $u^\mu = (1/\sqrt{-g_{00}}, 0, 0, 0)$ (normalized so $u_\mu u^\mu = -c^2$... in our conventions with $c=1$ for this derivation).

$$
f = \frac{-g_{00}\, p^0}{\sqrt{-g_{00}}} = \frac{E}{\sqrt{-g_{00}}}
$$

**Step 3:** At emission ($r_1$) and reception ($r_2$):

$$
f_1 = \frac{E}{\sqrt{-g_{00}(r_1)}}, \qquad f_2 = \frac{E}{\sqrt{-g_{00}(r_2)}}
$$

**Step 4:** The ratio:

$$
\frac{f_2}{f_1} = \frac{\sqrt{-g_{00}(r_1)}}{\sqrt{-g_{00}(r_2)}}
$$

For the weak-field metric $g_{00} = -(1 + 2\Phi/c^2)$:

$$
\boxed{\frac{f_2}{f_1} = \sqrt{\frac{1 + 2\Phi_1/c^2}{1 + 2\Phi_2/c^2}}} \qquad \blacksquare
$$

---

### Proof 8.4.2 — Newtonian Limit: Geodesic Equation Reduces to Newton's Law

**Setup:** Weak field ($|2\Phi/c^2| \ll 1$), slow motion ($v \ll c$), static field ($\partial_t g_{\mu\nu} = 0$).

**Step 1:** The geodesic equation is:

$$
\frac{d^2 x^\mu}{d\tau^2} + \Gamma^\mu_{\alpha\beta}\frac{dx^\alpha}{d\tau}\frac{dx^\beta}{d\tau} = 0
$$

**Step 2:** For slow motion, $dx^i/d\tau \ll dx^0/d\tau = c\, dt/d\tau \approx c$ (since $\gamma \approx 1$). The dominant term in the sum is $\alpha = \beta = 0$:

$$
\frac{d^2 x^i}{d\tau^2} + \Gamma^i_{00}\left(\frac{dx^0}{d\tau}\right)^2 \approx 0
$$

$$
\frac{d^2 x^i}{d\tau^2} \approx -\Gamma^i_{00}\, c^2
$$

**Step 3:** Compute $\Gamma^i_{00}$ for the weak-field metric $g_{00} = -(1 + 2\Phi/c^2)$, $g_{ij} = \delta_{ij}(1 - 2\Phi/c^2)$:

$$
\Gamma^i_{00} = \frac{1}{2}g^{i\alpha}(\partial_0 g_{\alpha 0} + \partial_0 g_{\alpha 0} - \partial_\alpha g_{00})
$$

For a static field ($\partial_0 = 0$) and $g^{ij} \approx \delta^{ij}$:

$$
\Gamma^i_{00} = -\frac{1}{2}\delta^{ij}\partial_j g_{00} = -\frac{1}{2}\partial_i\left(-(1 + 2\Phi/c^2)\right) = \frac{1}{c^2}\partial_i\Phi
$$

**Step 4:** Substitute back (and $d\tau \approx dt$ for slow motion):

$$
\frac{d^2 x^i}{dt^2} = -c^2 \cdot \frac{1}{c^2}\partial_i\Phi = -\partial_i\Phi = -\nabla\Phi
$$

$$
\boxed{\ddot{\mathbf{x}} = -\nabla\Phi} \qquad \text{(Newton's law of gravitation)} \qquad \blacksquare
$$

This proves that GR reduces to Newtonian gravity in the appropriate limit.




---

## 🧮 6. Worked Examples

### Example 8.4.1 — GPS Satellite Clock Correction

**Problem:** A GPS satellite orbits at $r = 26{,}600$ km from Earth's center ($R_E = 6{,}371$ km) at orbital speed $v = 3.87$ km/s. Compute the daily clock drift from (a) gravitational time dilation and (b) velocity time dilation.

**Solution:**

**(a) Gravitational effect** (clock runs faster at higher potential):

$$
\frac{\Delta\tau_{\text{grav}}}{\Delta t} = \sqrt{\frac{1 - 2GM/(r_{\text{sat}}c^2)}{1 - 2GM/(R_E c^2)}} - 1 \approx \frac{GM}{c^2}\left(\frac{1}{R_E} - \frac{1}{r_{\text{sat}}}\right)
$$

$$
\frac{GM}{c^2} = \frac{6.674\times10^{-11} \times 5.972\times10^{24}}{(3\times10^8)^2} = 4.43\times10^{-3}\,\text{m}
$$

$$
\frac{1}{R_E} - \frac{1}{r_{\text{sat}}} = \frac{1}{6.371\times10^6} - \frac{1}{2.66\times10^7} = 1.570\times10^{-7} - 3.759\times10^{-8} = 1.194\times10^{-7}\,\text{m}^{-1}
$$

$$
\frac{\Delta\tau_{\text{grav}}}{\Delta t} = 4.43\times10^{-3} \times 1.194\times10^{-7} = 5.29\times10^{-10}
$$

Per day: $5.29\times10^{-10} \times 86400 = 45.7\,\mu\text{s/day}$ (satellite clock runs **faster**).

**(b) Velocity effect** (SR time dilation, clock runs slower):

$$
\frac{\Delta\tau_{\text{vel}}}{\Delta t} = \sqrt{1 - v^2/c^2} - 1 \approx -\frac{v^2}{2c^2}
$$

$$
= -\frac{(3870)^2}{2(3\times10^8)^2} = -\frac{1.498\times10^7}{1.8\times10^{17}} = -8.32\times10^{-11}
$$

Per day: $-8.32\times10^{-11} \times 86400 = -7.2\,\mu\text{s/day}$ (satellite clock runs **slower**).

**(c) Net effect:**

$$
\Delta\tau_{\text{net}} = +45.7 - 7.2 = +38.5\,\mu\text{s/day}
$$

Without correction, position error per day: $c \times 38.5\,\mu\text{s} = 3\times10^8 \times 38.5\times10^{-6} = 11.6$ km/day.

---

### Example 8.4.2 — Gravitational Redshift of a White Dwarf

**Problem:** Sirius B (white dwarf) has mass $M = 1.02 M_\odot$ and radius $R = 5{,}800$ km. Compute the gravitational redshift of light emitted from its surface.

**Solution:**

$$
z = \frac{\Delta\lambda}{\lambda} = \frac{1}{\sqrt{1 - r_s/R}} - 1 \approx \frac{r_s}{2R} \quad \text{(weak field)}
$$

Schwarzschild radius:

$$
r_s = \frac{2GM}{c^2} = \frac{2 \times 6.674\times10^{-11} \times 1.02 \times 1.989\times10^{30}}{(3\times10^8)^2}
$$

$$
= \frac{2 \times 6.674\times10^{-11} \times 2.029\times10^{30}}{9\times10^{16}} = \frac{2.707\times10^{20}}{9\times10^{16}} = 3008\,\text{m} = 3.01\,\text{km}
$$

$$
z = \frac{r_s}{2R} = \frac{3008}{2 \times 5.8\times10^6} = 2.59\times10^{-4}
$$

This corresponds to a velocity equivalent of $v = zc = 77.8$ km/s — measurable spectroscopically. (Observed value: $z \approx 3\times10^{-4}$, consistent with GR.)

---

### Example 8.4.3 — Shapiro Time Delay

**Problem:** A radar signal is sent from Earth, grazes the Sun, and reflects off a planet. Estimate the excess time delay due to spacetime curvature.

**Solution:**

The Shapiro delay for a signal passing at closest approach $r_0$ to a mass $M$:

$$
\Delta t_{\text{Shapiro}} = \frac{4GM}{c^3}\ln\left(\frac{4r_1 r_2}{r_0^2}\right)
$$

where $r_1$, $r_2$ are the distances of emitter and reflector from the mass.

For a signal grazing the Sun ($r_0 = R_\odot = 6.96\times10^8$ m), reflected off Mars at opposition ($r_2 = 2.1\times10^{11}$ m), with Earth at $r_1 = 1.5\times10^{11}$ m:

$$
\frac{4GM_\odot}{c^3} = \frac{4 \times 6.674\times10^{-11} \times 1.989\times10^{30}}{(3\times10^8)^3} = \frac{5.31\times10^{20}}{2.7\times10^{25}} = 1.97\times10^{-5}\,\text{s}
$$

$$
\ln\left(\frac{4 \times 1.5\times10^{11} \times 2.1\times10^{11}}{(6.96\times10^8)^2}\right) = \ln\left(\frac{1.26\times10^{23}}{4.84\times10^{17}}\right) = \ln(2.6\times10^5) = 12.5
$$

$$
\Delta t = 1.97\times10^{-5} \times 12.5 = 246\,\mu\text{s}
$$

This corresponds to an excess path length of $c\Delta t = 74$ km. The Shapiro delay was first measured in 1964 and confirms GR to $\sim 0.1\%$ precision.

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- **Previous:** [8.3 - Covariant Relativistic Dynamics](8.3---Covariant-Relativistic-Dynamics)
- **Next:** [8.5 - Differential Geometry - Manifolds & Metrics](8.5---Differential-Geometry---Manifolds-&-Metrics) — the mathematical machinery for curved spacetime
- **Geodesic equation:** [8.6 - Covariant Derivative & Christoffel Symbols](8.6---Covariant-Derivative-&-Christoffel-Symbols)
- **Curvature formalism:** [8.7 - Geodesics & Curvature - Riemann & Ricci Tensors](8.7---Geodesics-&-Curvature---Riemann-&-Ricci-Tensors)
- **Tensor foundations:** [2.8 - SVD & Tensors](2.8---SVD-&-Tensors)

### External References
1. **Carroll, S.** (1997). arXiv:gr-qc/9712019. Chapter 4: Gravitation (Equivalence Principle).
2. **Susskind, L.** *The Theoretical Minimum: General Relativity*. Lectures 1–3.
3. **Misner, Thorne & Wheeler** (1973). *Gravitation*. Chapter 1: Geometrodynamics in Brief.
4. **Will, C.M.** (2014). "The Confrontation between GR and Experiment." *Living Reviews in Relativity*, 17, 4.
5. **Pound, R.V. & Rebka, G.A.** (1959). "Gravitational Red-Shift in Nuclear Resonance." *Phys. Rev. Lett.* 3, 439.

---

*Next: [8.5 - Differential Geometry - Manifolds & Metrics](8.5---Differential-Geometry---Manifolds-&-Metrics) →*



---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.4.E1 — Gravitational Redshift: Pound-Rebka Experiment

**Problem:** In the 1959 Pound-Rebka experiment, gamma rays ($E = 14.4$ keV from $^{57}$Fe) were emitted at the bottom of a tower of height $h = 22.5$ m at Harvard. Compute the predicted fractional frequency shift and compare with the measured value.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Gravitational redshift formula (weak field).**

For a photon climbing out of a gravitational potential, the fractional frequency shift is:

$$
\frac{\Delta f}{f} = \frac{f_{\text{top}} - f_{\text{bottom}}}{f_{\text{bottom}}} = -\frac{\Delta\Phi}{c^2} = -\frac{gh}{c^2}
$$

where $\Delta\Phi = gh$ is the gravitational potential difference (positive upward), and the negative sign indicates a **redshift** (frequency decreases as photon climbs).

**Step 2: Compute the predicted shift.**

$$
\frac{\Delta f}{f} = -\frac{gh}{c^2} = -\frac{9.81 \times 22.5}{(3\times10^8)^2}
$$

$$
= -\frac{220.7}{9\times10^{16}} = -2.45\times10^{-15}
$$

**Step 3: Compare with experiment.**

The measured value (Pound & Rebka, 1960; refined by Pound & Snider, 1965):

$$
\left(\frac{\Delta f}{f}\right)_{\text{measured}} = (-2.57 \pm 0.26)\times10^{-15}
$$

Agreement with GR prediction: within 1% (Pound-Snider achieved 1% precision).

**Step 4: Derivation from the equivalence principle.**

By the equivalence principle, a uniform gravitational field $g$ is equivalent to a uniformly accelerating frame. In the accelerating frame, during the time $\Delta t = h/c$ it takes light to cross the tower, the receiver has gained velocity:

$$
\Delta v = g\Delta t = \frac{gh}{c}
$$

By the (first-order) Doppler effect:

$$
\frac{\Delta f}{f} = -\frac{\Delta v}{c} = -\frac{gh}{c^2}
$$

This is Einstein's original argument (1907) — the equivalence principle directly predicts gravitational redshift without any knowledge of the full field equations.

**Step 5: Energy interpretation.**

A photon of energy $E = hf$ climbing height $h$ in gravity "loses" potential energy $E \cdot gh/c^2$:

$$
E_{\text{top}} = E_{\text{bottom}}\left(1 - \frac{gh}{c^2}\right) \implies f_{\text{top}} = f_{\text{bottom}}\left(1 - \frac{gh}{c^2}\right)
$$

If photons did not redshift, one could build a perpetual motion machine: convert mass to photons at the bottom, send them up, convert back to mass at the top (gaining potential energy for free). The redshift is required by energy conservation.

</details>

---

### Example 8.4.E2 — Proper Acceleration in Rindler Coordinates

**Problem:** An observer undergoes constant proper acceleration $a$ in Minkowski spacetime. (a) Derive the Rindler metric. (b) Show that the metric has a coordinate singularity (Rindler horizon). (c) Compute the proper acceleration of a static observer at coordinate position $\xi$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**(a) Derivation of the Rindler metric.**

**Step 1:** From Example 8.3.E4, the worldline of a uniformly accelerating observer is:

$$
T(\tau) = \frac{c}{a}\sinh\left(\frac{a\tau}{c}\right), \qquad X(\tau) = \frac{c^2}{a}\cosh\left(\frac{a\tau}{c}\right)
$$

(shifted so $X(0) = c^2/a$, $T(0) = 0$).

**Step 2:** Define Rindler coordinates $(\eta, \xi)$ by:

$$
T = \frac{\xi}{c}\sinh\left(\frac{a\eta}{c}\right), \qquad X = \xi\cosh\left(\frac{a\eta}{c}\right)
$$

where $\eta$ is the Rindler time (proportional to proper time of the fiducial observer at $\xi = c^2/a$) and $\xi \gt  0$ is the spatial coordinate.

**Step 3:** Compute the metric. Take differentials:

$$
dT = \frac{1}{c}\sinh\left(\frac{a\eta}{c}\right)d\xi + \frac{a\xi}{c^2}\cosh\left(\frac{a\eta}{c}\right)d\eta
$$

$$
dX = \cosh\left(\frac{a\eta}{c}\right)d\xi + \frac{a\xi}{c}\sinh\left(\frac{a\eta}{c}\right)d\eta
$$

**Step 4:** Compute $ds^2 = -c^2 dT^2 + dX^2$:

$$
-c^2 dT^2 = -\sinh^2\left(\frac{a\eta}{c}\right)d\xi^2 - \frac{a^2\xi^2}{c^2}\cosh^2\left(\frac{a\eta}{c}\right)d\eta^2 - 2\frac{a\xi}{c}\sinh\cosh\, d\xi\,d\eta
$$

$$
dX^2 = \cosh^2\left(\frac{a\eta}{c}\right)d\xi^2 + \frac{a^2\xi^2}{c^2}\sinh^2\left(\frac{a\eta}{c}\right)d\eta^2 + 2\frac{a\xi}{c}\sinh\cosh\, d\xi\,d\eta
$$

Adding (cross terms cancel, and using $\cosh^2 - \sinh^2 = 1$):

$$
ds^2 = (\cosh^2 - \sinh^2)d\xi^2 + \frac{a^2\xi^2}{c^2}(\sinh^2 - \cosh^2)d\eta^2
$$

Wait — let me redo this more carefully. Actually:

$$
ds^2 = -c^2 dT^2 + dX^2 = d\xi^2 - \frac{a^2\xi^2}{c^2}d\eta^2
$$

Hmm, let me use the standard form. Define $\rho = \xi$ and use $\eta$ with dimensions of time. The standard Rindler metric is:

$$
\boxed{ds^2 = -\frac{a^2\xi^2}{c^4}\,c^2 d\eta^2 + d\xi^2 = -\left(\frac{a\xi}{c^2}\right)^2 c^2 d\eta^2 + d\xi^2}
$$

Or more cleanly, with $g_{00} = -(a\xi/c^2)^2$:

$$
ds^2 = -\left(1 + \frac{a\xi'}{c^2}\right)^2 c^2 dt^2 + d\xi'^2
$$

where $\xi' = \xi - c^2/a$ measures distance from the fiducial observer.

**(b) Rindler horizon.**

The metric component $g_{00} = -(a\xi/c^2)^2$ vanishes at $\xi = 0$. This is the **Rindler horizon** — a null surface that the accelerating observer can never receive signals from. Events behind the Rindler horizon ($\xi \lt  0$ in the original Minkowski coordinates: $X \lt  0$) are causally disconnected from the accelerating observer.

This is the flat-spacetime analogue of a black hole horizon. The Unruh effect (quantum fields in Rindler spacetime appear thermal at temperature $T = \hbar a/(2\pi k_B c)$) is the flat-space analogue of Hawking radiation.

**(c) Proper acceleration at position $\xi$.**

A static observer at constant $\xi$ has 4-velocity $U^\mu = (c/\sqrt{|g_{00}|}, 0) = (c^3/(a\xi), 0)$ (normalized so $g_{\mu\nu}U^\mu U^\nu = -c^2$).

The proper acceleration is:

$$
\alpha(\xi) = \frac{c^2}{\xi} \cdot \frac{c^2}{a\xi} \cdot a = \frac{c^4}{a\xi^2} \cdot a
$$

Actually, for the metric $ds^2 = -(a\xi/c^2)^2 c^2 d\eta^2 + d\xi^2$, the proper acceleration of a static observer at $\xi$ is:

$$
\alpha = \frac{c^4}{a\xi^2} \cdot \frac{\partial_\xi g_{00}}{2|g_{00}|^{1/2}} = \frac{c^2}{\xi}
$$

More directly: the proper acceleration of a static observer in a static metric $ds^2 = -e^{2\Phi}c^2 dt^2 + d\xi^2$ is $\alpha = c^2 \partial_\xi\Phi$. Here $e^{2\Phi} = (a\xi/c^2)^2$, so $\Phi = \ln(a\xi/c^2)$ and:

$$
\alpha = c^2\frac{\partial\Phi}{\partial\xi} = c^2 \cdot \frac{1}{\xi} = \frac{c^2}{\xi}
$$

At the fiducial position $\xi_0 = c^2/a$: $\alpha = c^2/(c^2/a) = a$. ✓

Observers closer to the horizon ($\xi \to 0$) need increasingly large proper acceleration to remain static — they must "fight harder" against the effective gravity. This mirrors the infinite blueshift/acceleration at a black hole horizon.

</details>

---

### Example 8.4.E3 — Tidal Forces in Free Fall: Geodesic Deviation

**Problem:** Two freely falling particles are separated by a small distance $\xi$ in the radial direction near Earth's surface. Compute the tidal acceleration (relative acceleration) between them using Newtonian gravity, then show how this connects to spacetime curvature.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Newtonian tidal force.**

Particle 1 at radius $r$ from Earth's center: $a_1 = -GM/r^2$ (toward center).

Particle 2 at radius $r + \xi$: $a_2 = -GM/(r+\xi)^2$.

Relative acceleration (tidal acceleration):

$$
\Delta a = a_2 - a_1 = -GM\left[\frac{1}{(r+\xi)^2} - \frac{1}{r^2}\right]
$$

For $\xi \ll r$, Taylor expand:

$$
\frac{1}{(r+\xi)^2} \approx \frac{1}{r^2}\left(1 - \frac{2\xi}{r}\right)
$$

$$
\Delta a \approx -GM\left[\frac{1}{r^2} - \frac{2\xi}{r^3} - \frac{1}{r^2}\right] = \frac{2GM\xi}{r^3}
$$

The tidal acceleration is **stretching** (positive = particles move apart) in the radial direction.

**Step 2: Numerical value near Earth's surface.**

$$
\Delta a = \frac{2GM_\oplus}{R_\oplus^3}\xi = \frac{2 \times 6.674\times10^{-11} \times 5.97\times10^{24}}{(6.37\times10^6)^3}\xi
$$

$$
= \frac{7.96\times10^{14}}{2.58\times10^{20}}\xi = 3.08\times10^{-6}\xi\,\text{s}^{-2}
$$

For $\xi = 1$ m: $\Delta a = 3.08\times10^{-6}$ m/s² — tiny but measurable with precision instruments.

**Step 3: Connection to curvature (geodesic deviation equation).**

In GR, the relative acceleration of nearby geodesics is governed by the **geodesic deviation equation**:

$$
\frac{D^2\xi^\mu}{d\tau^2} = -R^\mu{}_{\nu\alpha\beta}U^\nu\xi^\alpha U^\beta
$$

where $\xi^\mu$ is the separation vector, $U^\mu$ is the 4-velocity, and $R^\mu{}_{\nu\alpha\beta}$ is the Riemann curvature tensor.

For slow motion ($U^\mu \approx (c, 0, 0, 0)$) and radial separation ($\xi^\mu = (0, \xi, 0, 0)$):

$$
\frac{d^2\xi^r}{dt^2} = -R^r{}_{trt}\,c^2\,\xi
$$

The relevant Riemann component for the Schwarzschild metric (weak field):

$$
R^r{}_{trt} = -\frac{2GM}{c^2 r^3}
$$

Therefore:

$$
\frac{d^2\xi^r}{dt^2} = -\left(-\frac{2GM}{c^2 r^3}\right)c^2\xi = \frac{2GM}{r^3}\xi
$$

This exactly reproduces the Newtonian tidal acceleration! **Tidal forces ARE curvature** — this is the physical content of the Riemann tensor. A single freely falling particle feels no gravity (equivalence principle), but two nearby particles detect curvature through their relative acceleration.

**Step 4: Transverse tidal force.**

For particles separated in the $\theta$-direction (transverse to radial):

$$
\frac{d^2\xi^\theta}{dt^2} = -R^\theta{}_{t\theta t}\,c^2\,\xi^\theta
$$

$$
R^\theta{}_{t\theta t} = \frac{GM}{c^2 r^3}
$$

$$
\frac{d^2\xi^\theta}{dt^2} = -\frac{GM}{r^3}\xi^\theta
$$

The transverse tidal force is **compressive** (negative = particles pushed together) and half the magnitude of the radial stretching. This is why a freely falling body near a black hole is stretched radially and compressed laterally — "spaghettification."

</details>




---

## 📘 9. Appendix: Extended Derivations & Special Cases

### Appendix 9.1 — The Equivalence Principle: Historical Development and Precise Formulations

**Einstein's elevator thought experiment (1907).**

Einstein's key insight: an observer in a closed box cannot distinguish between:
1. Being at rest in a uniform gravitational field $g$, and
2. Being in empty space, accelerating upward at $a = g$.

**Consequence 1 (gravitational redshift):** Light emitted from the floor of the accelerating elevator is Doppler-shifted when it reaches the ceiling (the ceiling is moving away). By equivalence, light climbing out of a gravitational field must also be redshifted.

**Consequence 2 (light bending):** A horizontal light beam in the accelerating elevator follows a curved path (the elevator moves upward while the light crosses). By equivalence, light must bend in a gravitational field.

**Consequence 3 (universality of free fall):** In the accelerating elevator, all objects "fall" at the same rate (they are actually stationary while the floor accelerates toward them). By equivalence, all objects fall at the same rate in gravity — regardless of composition. This is the **Weak Equivalence Principle** (WEP), tested to $10^{-15}$ precision by the MICROSCOPE satellite (2017).

**Three levels of the equivalence principle:**

| Level | Statement | Tested to |
|-------|-----------|-----------|
| **Weak (WEP)** | Inertial mass = gravitational mass; all bodies fall alike | $10^{-15}$ (MICROSCOPE) |
| **Einstein (EEP)** | WEP + local non-gravitational experiments are independent of position and velocity | $10^{-7}$ (Hughes-Drever) |
| **Strong (SEP)** | EEP + gravitational self-energy also falls alike (no Nordtvedt effect) | $10^{-13}$ (lunar laser ranging) |

**Mathematical formulation:** At any point $p$ in a curved spacetime, there exist coordinates (Riemann normal coordinates) such that:

$$
g_{\mu\nu}(p) = \eta_{\mu\nu}, \qquad \Gamma^\alpha_{\mu\nu}(p) = 0
$$

The metric looks flat and the connection vanishes at $p$ — gravity is "transformed away" locally. But the **curvature** $R^\alpha{}_{\beta\mu\nu}(p) \neq 0$ in general — tidal forces cannot be eliminated. This is the precise statement: gravity is geometry, and the equivalence principle says the geometry is locally flat.

---

### Appendix 9.2 — Local Inertial Frames and Riemann Normal Coordinates

**Theorem:** At any point $p$ on a (pseudo-)Riemannian manifold, there exist coordinates $\{x^\mu\}$ (called **Riemann normal coordinates** or **locally inertial coordinates**) such that:

$$
g_{\mu\nu}(p) = \eta_{\mu\nu}, \qquad \partial_\rho g_{\mu\nu}(p) = 0 \quad (\text{equivalently, } \Gamma^\alpha_{\mu\nu}(p) = 0)
$$

**Construction:** Choose an orthonormal basis $\{e_\mu\}$ at $p$ (so $g(e_\mu, e_\nu) = \eta_{\mu\nu}$). For any point $q$ near $p$, there is a unique geodesic from $p$ to $q$. If this geodesic has initial tangent vector $V^\mu e_\mu$ at $p$ and affine parameter length 1, assign coordinates $x^\mu(q) = V^\mu$.

**Proof that $\Gamma^\alpha_{\mu\nu}(p) = 0$:** In these coordinates, geodesics through $p$ are straight lines $x^\mu(\lambda) = V^\mu\lambda$. The geodesic equation at $p$:

$$
\frac{d^2 x^\alpha}{d\lambda^2}\bigg|_p + \Gamma^\alpha_{\mu\nu}(p)\frac{dx^\mu}{d\lambda}\frac{dx^\nu}{d\lambda}\bigg|_p = 0
$$

Since $x^\mu = V^\mu\lambda$: $d^2x^\alpha/d\lambda^2 = 0$ and $dx^\mu/d\lambda = V^\mu$. So:

$$
\Gamma^\alpha_{\mu\nu}(p)V^\mu V^\nu = 0 \quad \text{for all } V^\mu
$$

Since this holds for arbitrary $V^\mu$, and $\Gamma^\alpha_{\mu\nu}$ is symmetric in $(\mu,\nu)$:

$$
\Gamma^\alpha_{\mu\nu}(p) = 0 \qquad \blacksquare
$$

**What cannot be eliminated:** The second derivatives $\partial_\rho\partial_\sigma g_{\mu\nu}(p)$ cannot all be set to zero — they contain the Riemann tensor:

$$
R_{\mu\nu\rho\sigma}(p) = \frac{1}{2}(\partial_\rho\partial_\nu g_{\mu\sigma} + \partial_\sigma\partial_\mu g_{\nu\rho} - \partial_\sigma\partial_\nu g_{\mu\rho} - \partial_\rho\partial_\mu g_{\nu\sigma})\bigg|_p
$$

This is the mathematical content of the statement "gravity cannot be completely transformed away" — curvature (tidal forces) is a genuine, coordinate-independent feature of the geometry.

**Counting degrees of freedom:** In $n$ dimensions, $g_{\mu\nu}$ has $n(n+1)/2$ independent components. The first derivatives $\partial_\rho g_{\mu\nu}$ have $n^2(n+1)/2$ components, and the Christoffel symbols (which can all be set to zero) have $n^2(n+1)/2$ components — exactly matching. The second derivatives have $n^2(n+1)^2/4$ components, but the Riemann tensor has only $n^2(n^2-1)/12$ independent components. The remaining second derivatives can be set to zero by further coordinate choice. In 4D: Riemann has 20 independent components.

**References:** Carroll (arXiv:gr-qc/9712019) §2.4; Wald, *General Relativity* §3.2; MTW §11.6.

