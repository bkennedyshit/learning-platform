---
title: "Rocket Equation & Propulsion Systems"
subject: "Aerospace Engineering & Orbital Mechanics"
catalog: advanced
audience_tier: higher-education
chapter: "10.4"
type: chapter-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 10.4 — Rocket Equation & Propulsion Systems

> *"In order to go to the planets, it is necessary to overcome the force of gravity of the Earth. The means to do this is a rocket."*
> — **Konstantin Tsiolkovsky**, *Exploration of Outer Space by Means of Rocket Devices* (1903)

The rocket equation is the fundamental constraint of spaceflight: every kilogram of payload demands exponentially more propellant as mission ΔV increases. This chapter derives the Tsiolkovsky equation from first principles, analyzes multi-stage rockets, and surveys propulsion technologies from chemical engines to ion drives.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Derive the **Tsiolkovsky rocket equation** from conservation of linear momentum.
2. Define and compute **specific impulse** $I_{sp}$, **thrust** $F$, and **mass flow rate** $\dot{m}$.
3. Calculate **mass ratios** and **structural coefficients** for single and multi-stage rockets.
4. Optimize **staging** for minimum total mass given a required ΔV.
5. Compare propulsion technologies: chemical, electric, nuclear thermal.
6. Apply the rocket equation to real vehicles (Saturn V, Falcon 9, ion thrusters).

---

## 🖼️ Visual Anchor — Rocket Staging & Mass Fractions

![math-10__10.4-fig1](math-10__10.4-fig1.svg)

---

## 📚 1. Definitions

### Definition 10.4.1 — Thrust

**Thrust** $F$ is the force produced by a rocket engine, equal to the rate of momentum ejection:

$$
F = \dot{m}\,v_e + (p_e - p_a)A_e
$$

where:
- $\dot{m}$ = mass flow rate of propellant (kg/s)
- $v_e$ = exhaust velocity relative to the rocket (m/s)
- $p_e$ = exhaust pressure at nozzle exit
- $p_a$ = ambient pressure
- $A_e$ = nozzle exit area

In vacuum ($p_a = 0$) or for an ideally expanded nozzle ($p_e = p_a$): $F = \dot{m}\,v_e$.

### Definition 10.4.2 — Effective Exhaust Velocity

The **effective exhaust velocity** $v_e$ (or $c$) accounts for both momentum and pressure thrust:

$$
v_e = \frac{F}{\dot{m}}
$$

### Definition 10.4.3 — Specific Impulse

**Specific impulse** $I_{sp}$ is the thrust per unit weight flow rate of propellant — a measure of propellant efficiency:

$$
I_{sp} = \frac{F}{\dot{m}\,g_0} = \frac{v_e}{g_0}
$$

where $g_0 = 9.80665$ m/s² is standard gravity. Units: seconds.

| Propulsion Type | $I_{sp}$ (s) | $v_e$ (km/s) |
|:---:|:---:|:---:|
| Solid rocket | 250–290 | 2.5–2.8 |
| Bipropellant (LOX/RP-1) | 300–350 | 2.9–3.4 |
| Bipropellant (LOX/LH₂) | 420–460 | 4.1–4.5 |
| Nuclear thermal | 800–1000 | 7.8–9.8 |
| Ion thruster | 1500–5000 | 15–49 |
| Hall thruster | 1500–3000 | 15–29 |

### Definition 10.4.4 — Mass Ratio

The **mass ratio** $R$ of a rocket stage is:

$$
R = \frac{m_0}{m_f} = \frac{m_s + m_p + m_L}{m_s + m_L}
$$

where:
- $m_0$ = initial mass (structure + propellant + payload)
- $m_f$ = final mass (structure + payload, propellant expended)
- $m_s$ = structural mass of the stage
- $m_p$ = propellant mass
- $m_L$ = payload mass (everything above this stage)

### Definition 10.4.5 — Structural Coefficient

The **structural coefficient** (or structural fraction) $\epsilon$ of a stage is:

$$
\epsilon = \frac{m_s}{m_s + m_p}
$$

This represents the fraction of the stage's "wet" mass (excluding payload) that is structure. Typical values: $\epsilon \approx 0.06$–$0.12$ for modern rockets.

### Definition 10.4.6 — Payload Ratio

The **payload ratio** $\lambda$ of a stage is:

$$
\lambda = \frac{m_L}{m_s + m_p} = \frac{m_L}{m_0 - m_L}
$$

### Definition 10.4.7 — Propellant Mass Fraction

The **propellant mass fraction** $\zeta$ is:

$$
\zeta = \frac{m_p}{m_0} = 1 - \frac{1}{R}
$$

### Definition 10.4.8 — Total Impulse

The **total impulse** $I_t$ is the integral of thrust over the burn time:

$$
I_t = \int_0^{t_b} F\,dt = F \cdot t_b \quad \text{(for constant thrust)}
$$

$$
I_t = I_{sp}\,g_0\,m_p
$$




---

## 📐 2. Axioms / Postulates

### Axiom 10.4.A1 — Conservation of Linear Momentum

In the absence of external forces, the total momentum of the rocket + exhaust system is conserved:

$$
\frac{d}{dt}(m\mathbf{v} + \mathbf{p}_{\text{exhaust}}) = \mathbf{F}_{\text{external}}
$$

For a rocket in free space (no gravity, no drag): $\mathbf{F}_{\text{external}} = \mathbf{0}$.

### Axiom 10.4.A2 — Constant Exhaust Velocity

The effective exhaust velocity $v_e$ is assumed constant during a burn. This is a good approximation for chemical rockets operating at steady state.

### Axiom 10.4.A3 — Instantaneous Mass Ejection (for Impulsive Burns)

For short burns relative to the orbital period, the gravitational and drag losses are negligible, and the rocket equation gives the ideal ΔV directly.

---

## 🛡️ 3. Lemmas

### Lemma 10.4.1 — Differential Momentum Balance

**Statement:** For a rocket of instantaneous mass $m$ ejecting propellant at rate $\dot{m}$ with exhaust velocity $v_e$ (relative to rocket), in the absence of external forces:

$$
m\frac{dv}{dt} = \dot{m}\,v_e = F
$$

where $\dot{m} = -dm/dt > 0$ is the mass flow rate (positive).

<details>
<summary>🔍 Derivation</summary>

At time $t$: rocket has mass $m$, velocity $v$.
At time $t + dt$: rocket has mass $m + dm$ (where $dm \lt  0$), velocity $v + dv$.
Ejected mass $(-dm)$ has velocity $v - v_e$ in the inertial frame.

Conservation of momentum:

$$
mv = (m + dm)(v + dv) + (-dm)(v - v_e)
$$

Expand:

$$
mv = mv + m\,dv + v\,dm + dm\,dv - v\,dm + v_e\,dm
$$

Cancel $mv$ and $v\,dm$ terms, neglect $dm\,dv$ (second order):

$$
0 = m\,dv + v_e\,dm
$$

$$
m\,dv = -v_e\,dm
$$

Since $\dot{m} = -dm/dt$:

$$
m\frac{dv}{dt} = v_e\dot{m} = F
$$

$\blacksquare$

</details>

### Lemma 10.4.2 — Gravity Loss

**Statement:** For a vertical ascent against gravity, the effective ΔV is reduced by the gravity loss:

$$
\Delta V_{\text{actual}} = v_e\ln\frac{m_0}{m_f} - g_0 t_b - \int_0^{t_b}\frac{1}{2}\rho v^2 C_D A/m\,dt
$$

The gravity loss $\Delta V_g = g_0 t_b$ (for vertical flight) motivates high thrust-to-weight ratios for launch vehicles.

### Lemma 10.4.3 — Relationship Between Mass Ratio and Structural Coefficient

**Statement:** The mass ratio of a single stage can be expressed as:

$$
R = \frac{m_0}{m_f} = \frac{1 + \lambda}{\epsilon + \lambda}
$$

where $\epsilon$ is the structural coefficient and $\lambda$ is the payload ratio.

<details>
<summary>🔍 Derivation</summary>

Let the stage have structural mass $m_s$, propellant $m_p$, payload $m_L$.

$$
m_0 = m_s + m_p + m_L, \quad m_f = m_s + m_L
$$

$$
R = \frac{m_s + m_p + m_L}{m_s + m_L}
$$

Divide numerator and denominator by $(m_s + m_p)$:

$$
R = \frac{1 + \lambda}{\frac{m_s}{m_s+m_p} + \frac{m_L}{m_s+m_p}} = \frac{1 + \lambda}{\epsilon + \lambda}
$$

$\blacksquare$

</details>




---

## 👑 4. Theorems

### Theorem 10.4.1 — Tsiolkovsky Rocket Equation

For a rocket with constant effective exhaust velocity $v_e$, the achievable velocity change is:

$$
\Delta V = v_e \ln\frac{m_0}{m_f} = v_e \ln R = I_{sp}\,g_0\,\ln R
$$

Equivalently, the required mass ratio for a given ΔV is:

$$
R = \frac{m_0}{m_f} = e^{\Delta V/v_e}
$$

This exponential relationship is the fundamental constraint of rocketry.

### Theorem 10.4.2 — Multi-Stage Rocket Equation

For an $N$-stage rocket where each stage $i$ has exhaust velocity $v_{e,i}$ and mass ratio $R_i$:

$$
\Delta V_{\text{total}} = \sum_{i=1}^N v_{e,i}\ln R_i
$$

The overall mass ratio is the product:

$$
\frac{m_{0,\text{total}}}{m_L} = \prod_{i=1}^N R_i \cdot \frac{1}{\lambda_{\text{overall}}}
$$

### Theorem 10.4.3 — Optimal Staging (Equal Structural Coefficients)

For an $N$-stage rocket where all stages have the same $v_e$ and structural coefficient $\epsilon$, the minimum total mass for a given ΔV and payload $m_L$ is achieved when all stages have **equal mass ratios**:

$$
R_i = R^* = e^{\Delta V/(Nv_e)} \quad \text{for all } i
$$

The payload ratio for each stage is then:

$$
\lambda_i = \frac{1 - \epsilon R^*}{R^* - 1}
$$

And the overall payload fraction:

$$
\frac{m_L}{m_0} = \left(\frac{\lambda^*}{1+\lambda^*}\right)^N
$$

### Theorem 10.4.4 — Single-Stage-to-Orbit (SSTO) Feasibility Criterion

A single stage can achieve orbit (ΔV ≈ 9.5 km/s including losses) only if:

$$
\epsilon < 1 - e^{-\Delta V/v_e} = 1 - \frac{1}{R}
$$

For LOX/LH₂ ($v_e \approx 4.4$ km/s): $R = e^{9.5/4.4} = e^{2.16} = 8.67$, requiring $\epsilon < 0.885$. This is easily met structurally ($\epsilon \approx 0.10$), but the payload fraction is:

$$
\lambda = \frac{1 - \epsilon R}{R - 1} = \frac{1 - 0.10 \times 8.67}{7.67} = \frac{0.133}{7.67} = 0.017
$$

Only 1.7% payload — marginally feasible but impractical for most missions.

### Theorem 10.4.5 — Thrust-to-Weight Ratio Requirement

For a rocket to lift off vertically:

$$
\frac{F}{m_0 g_0} > 1 \quad \Longleftrightarrow \quad \frac{\dot{m}\,v_e}{m_0 g_0} > 1
$$

Typical values: 1.2–1.8 for launch vehicles. Higher T/W reduces gravity losses.

---

## ✍️ 5. Proofs / Derivations

### 5.1 Derivation of the Tsiolkovsky Rocket Equation

**Goal:** Derive $\Delta V = v_e\ln(m_0/m_f)$ from conservation of momentum.

**Step 1: Set up the differential equation.**

From Lemma 10.4.1, in free space:

$$
m\,dv = -v_e\,dm
$$

**Step 2: Separate variables.**

$$
dv = -v_e\frac{dm}{m}
$$

**Step 3: Integrate from initial state $(v_0, m_0)$ to final state $(v_f, m_f)$.**

$$
\int_{v_0}^{v_f} dv = -v_e\int_{m_0}^{m_f}\frac{dm}{m}
$$

$$
v_f - v_0 = -v_e[\ln m]_{m_0}^{m_f} = -v_e(\ln m_f - \ln m_0) = v_e\ln\frac{m_0}{m_f}
$$

**Step 4: Define ΔV:**

$$
\Delta V = v_f - v_0 = v_e\ln\frac{m_0}{m_f} = v_e\ln R
$$

**Step 5: Express in terms of specific impulse:**

Since $v_e = I_{sp}\,g_0$:

$$
\Delta V = I_{sp}\,g_0\,\ln R
$$

$\blacksquare$

### 5.2 Derivation of the Optimal Staging Condition

**Goal:** For $N$ identical stages (same $v_e$, same $\epsilon$), prove that equal mass ratios minimize total mass.

**Step 1: Define the problem.**

Total ΔV constraint: $\sum_{i=1}^N v_e\ln R_i = \Delta V_{\text{req}}$.

Minimize total initial mass $m_0$ for fixed payload $m_L$.

**Step 2: Express total mass in terms of stage ratios.**

For stage $i$ with payload ratio $\lambda_i$ and mass ratio $R_i$:

$$
R_i = \frac{1+\lambda_i}{\epsilon + \lambda_i}
$$

The mass of stage $i$ (structure + propellant) is $m_{s,i} + m_{p,i}$, and its payload is everything above it.

The overall mass ratio from payload to total:

$$
\frac{m_0}{m_L} = \prod_{i=1}^N \frac{1+\lambda_i}{\lambda_i} = \prod_{i=1}^N \frac{R_i}{\lambda_i/(1+\lambda_i-\epsilon R_i)...}
$$

More directly: for each stage, $m_{0,i}/m_{L,i} = R_i/(\epsilon + \lambda_i) \times (1+\lambda_i)$... 

Let's use Lagrange multipliers on the simpler formulation.

**Step 3: Lagrange multiplier approach.**

Minimize $f = \sum_{i=1}^N \ln R_i$ (which is $\ln\prod R_i$, proportional to total mass) subject to $g = \sum_{i=1}^N \ln R_i = \Delta V/v_e$ ... 

Actually, the constraint IS the objective in this form. Let me reformulate.

The correct formulation: each stage's mass ratio determines how much "overhead" it adds. The total initial mass is:

$$
m_0 = m_L \prod_{i=1}^N \frac{R_i}{1 - \epsilon(R_i - 1)/(1-\epsilon)}
$$

For the simplified case where we define $\Pi_i = R_i$ and the constraint is $\sum \ln R_i = \Delta V/v_e$:

By the AM-GM inequality (or Lagrange multipliers), the product $\prod R_i$ is minimized when all $R_i$ are equal, given a fixed sum of $\ln R_i$. But we want to minimize total mass, which involves the product of terms like $R_i/(1-\epsilon(R_i-1))$.

**Step 4: Simplified proof for identical stages.**

For identical stages with the same $\epsilon$ and $v_e$, define $x_i = \ln R_i$ so $\sum x_i = \Delta V/v_e$.

The payload fraction of stage $i$ is:

$$
\frac{m_{L,i}}{m_{0,i}} = \frac{\lambda_i}{1+\lambda_i} = 1 - \frac{R_i(1-\epsilon)}{1} \cdot \frac{1}{R_i} = \frac{1 - \epsilon R_i}{1 - \epsilon}... 
$$

Let me use the cleaner approach. The overall payload fraction is:

$$
\frac{m_L}{m_0} = \prod_{i=1}^N \frac{1 - \epsilon_i R_i}{R_i(1-\epsilon_i)} \cdot R_i = \prod_{i=1}^N \frac{1-\epsilon R_i}{1-\epsilon}
$$

Wait — more carefully. For stage $i$: $m_{0,i} = m_{s,i} + m_{p,i} + m_{L,i}$ and $m_{f,i} = m_{s,i} + m_{L,i}$. The payload of stage $i$ is $m_{L,i} = m_{0,i+1}$ (the entire rocket above).

$$
\frac{m_{L,i}}{m_{0,i}} = \frac{m_f - m_s}{m_0} = \frac{m_0/R_i - \epsilon(m_0 - m_{L,i})}{m_0}
$$

This gets circular. The standard result (see Curtis Ch. 11) is proven by Lagrange multipliers on:

Maximize $\prod_{i=1}^N (1 - \epsilon e^{x_i})$ subject to $\sum x_i = \Delta V/v_e$.

Taking the log and using Lagrange multipliers: $\frac{\partial}{\partial x_i}\ln(1-\epsilon e^{x_i}) = \lambda$ for all $i$.

$$
\frac{-\epsilon e^{x_i}}{1-\epsilon e^{x_i}} = \lambda \quad \forall i
$$

This requires $e^{x_i}$ = same for all $i$, i.e., $R_i = R^*$ for all $i$.

Therefore $R^* = e^{\Delta V/(Nv_e)}$. $\blacksquare$

### 5.3 Derivation of Thrust from Momentum Flux

**Goal:** Derive $F = \dot{m}v_e$ from control volume analysis.

**Step 1:** Consider a control volume enclosing the rocket engine. Apply the momentum theorem:

$$
F = \frac{d}{dt}(m_{\text{exhaust}} v_{\text{exhaust}}) = \dot{m}_e v_e
$$

**Step 2:** For a rocket nozzle with exit pressure $p_e$ different from ambient $p_a$, the pressure force on the exit plane contributes:

$$
F = \dot{m}v_e + (p_e - p_a)A_e
$$

**Step 3:** Define effective exhaust velocity to absorb the pressure term:

$$
c = v_e + \frac{(p_e - p_a)A_e}{\dot{m}} \implies F = \dot{m}\,c
$$

In vacuum: $F = \dot{m}v_e + p_e A_e$. $\blacksquare$

### 5.4 Derivation of Payload Fraction for N-Stage Rocket

**Goal:** Express overall payload fraction in terms of $N$, $\epsilon$, and $\Delta V/v_e$.

For $N$ identical stages with equal mass ratios $R^* = e^{\Delta V/(Nv_e)}$:

Each stage's payload ratio:

$$
\lambda^* = \frac{1 - \epsilon R^*}{R^* - 1}
$$

(From $R = (1+\lambda)/(\epsilon+\lambda)$, solve for $\lambda$: $\lambda(R-1) = 1 - \epsilon R$, so $\lambda = (1-\epsilon R)/(R-1)$.)

The payload fraction of each stage:

$$
\frac{m_{L,i}}{m_{0,i}} = \frac{\lambda}{1+\lambda} = \frac{1-\epsilon R^*}{R^* - 1 + 1 - \epsilon R^*} = \frac{1-\epsilon R^*}{R^*(1-\epsilon)}
$$

Overall payload fraction (product of $N$ identical stages):

$$
\frac{m_L}{m_0} = \left(\frac{1-\epsilon R^*}{R^*(1-\epsilon)}\right)^N
$$

$\blacksquare$




---

## 🧮 6. Worked Examples

### Example 10.4.1 — Saturn V First Stage Mass Ratio

**Given:** Saturn V S-IC (first stage):
- Propellant mass: $m_p = 2{,}077{,}000$ kg (LOX/RP-1)
- Structural mass: $m_s = 131{,}000$ kg
- Payload (everything above): $m_L = 688{,}000$ kg (S-II + S-IVB + spacecraft)
- $I_{sp} = 263$ s (sea level)

**Find:** Mass ratio, structural coefficient, and ΔV contribution.

**Solution:**

Step 1: Initial and final masses:

$$
m_0 = m_s + m_p + m_L = 131000 + 2077000 + 688000 = 2{,}896{,}000 \text{ kg}
$$

$$
m_f = m_s + m_L = 131000 + 688000 = 819{,}000 \text{ kg}
$$

Step 2: Mass ratio:

$$
R = \frac{m_0}{m_f} = \frac{2896000}{819000} = 3.536
$$

Step 3: Structural coefficient:

$$
\epsilon = \frac{m_s}{m_s + m_p} = \frac{131000}{131000 + 2077000} = \frac{131000}{2208000} = 0.0593
$$

Step 4: ΔV contribution:

$$
\Delta V_1 = I_{sp}\,g_0\,\ln R = 263 \times 9.807 \times \ln(3.536) = 2579 \times 1.264 = 3260 \text{ m/s} = 3.26 \text{ km/s}
$$

**Note:** Actual ΔV delivered is less due to gravity loss (~1.5 km/s) and drag loss (~0.1 km/s) during the ~150 s burn.

---

### Example 10.4.2 — Required Propellant for LEO-to-GEO Transfer

**Given:** Spacecraft dry mass $m_f = 2000$ kg. Required ΔV = 3.9 km/s (Hohmann, from Example 10.3.1). Engine: bipropellant with $I_{sp} = 320$ s.

**Find:** Required propellant mass.

**Solution:**

Step 1: Effective exhaust velocity:

$$
v_e = I_{sp}\,g_0 = 320 \times 9.807 = 3138 \text{ m/s} = 3.138 \text{ km/s}
$$

Step 2: Mass ratio from rocket equation:

$$
R = e^{\Delta V/v_e} = e^{3.9/3.138} = e^{1.243} = 3.466
$$

Step 3: Initial mass:

$$
m_0 = R \cdot m_f = 3.466 \times 2000 = 6932 \text{ kg}
$$

Step 4: Propellant mass:

$$
m_p = m_0 - m_f = 6932 - 2000 = 4932 \text{ kg}
$$

**Propellant mass fraction:** $\zeta = m_p/m_0 = 4932/6932 = 0.711$ (71.1% of the spacecraft is propellant!).

---

### Example 10.4.3 — Ion Thruster for Deep Space Mission

**Given:** Ion thruster with $I_{sp} = 3000$ s. Spacecraft initial mass $m_0 = 1000$ kg. Available ΔV = 10 km/s.

**Find:** Final mass and propellant consumed.

**Solution:**

Step 1: Exhaust velocity:

$$
v_e = 3000 \times 9.807 = 29{,}421 \text{ m/s} = 29.42 \text{ km/s}
$$

Step 2: Mass ratio:

$$
R = e^{10/29.42} = e^{0.340} = 1.405
$$

Step 3: Final mass:

$$
m_f = m_0/R = 1000/1.405 = 712 \text{ kg}
$$

Step 4: Propellant consumed:

$$
m_p = 1000 - 712 = 288 \text{ kg}
$$

**Comparison:** A chemical engine ($I_{sp} = 320$ s, $v_e = 3.14$ km/s) would need:

$$
R = e^{10/3.14} = e^{3.18} = 24.1 \implies m_p = 1000(1 - 1/24.1) = 958 \text{ kg}
$$

The ion thruster uses 70% less propellant! Trade-off: much lower thrust, requiring months/years of continuous thrusting.

---

### Example 10.4.4 — Two-Stage Optimization

**Given:** Required ΔV = 9.5 km/s (LEO insertion including losses). Both stages use LOX/LH₂ ($I_{sp} = 450$ s, $v_e = 4.414$ km/s). Structural coefficient $\epsilon = 0.10$. Payload $m_L = 5000$ kg.

**Find:** Optimal stage mass ratios and total liftoff mass.

**Solution:**

Step 1: Optimal mass ratio (equal for both stages):

$$
R^* = e^{\Delta V/(2v_e)} = e^{9.5/(2\times4.414)} = e^{1.076} = 2.933
$$

Step 2: Check feasibility: need $\epsilon R^* < 1$:

$$
\epsilon R^* = 0.10 \times 2.933 = 0.293 < 1 \quad \checkmark
$$

Step 3: Payload ratio per stage:

$$
\lambda^* = \frac{1 - \epsilon R^*}{R^* - 1} = \frac{1 - 0.293}{1.933} = \frac{0.707}{1.933} = 0.3658
$$

Step 4: Payload fraction per stage:

$$
\frac{m_{L,i}}{m_{0,i}} = \frac{\lambda}{1+\lambda} = \frac{0.3658}{1.3658} = 0.2678
$$

Step 5: Overall payload fraction:

$$
\frac{m_L}{m_0} = (0.2678)^2 = 0.0717
$$

Step 6: Total liftoff mass:

$$
m_0 = \frac{m_L}{0.0717} = \frac{5000}{0.0717} = 69{,}700 \text{ kg}
$$

Step 7: Stage breakdown:
- Stage 2 initial mass: $m_{0,2} = m_L/0.2678 = 5000/0.2678 = 18{,}670$ kg
- Stage 2 propellant: $m_{p,2} = m_{0,2}(1-1/R^*) = 18670(1-0.341) = 12{,}300$ kg
- Stage 1 initial mass: $m_{0,1} = m_0 = 69{,}700$ kg
- Stage 1 propellant: $m_{p,1} = (69700-18670)(1-0.341) = 51030 \times 0.659 = 33{,}630$ kg

---

### Example 10.4.5 — Comparison: 1, 2, and 3 Stages

**Given:** Same parameters as Example 10.4.4 ($\Delta V = 9.5$ km/s, $v_e = 4.414$ km/s, $\epsilon = 0.10$, $m_L = 5000$ kg).

**Find:** Total liftoff mass for 1, 2, and 3 stages.

| Stages $N$ | $R^*$ | $\epsilon R^*$ | Payload fraction | $m_0$ (kg) |
|:---:|:---:|:---:|:---:|:---:|
| 1 | $e^{2.152} = 8.60$ | 0.860 | $(1-0.860)/(8.60\times0.9) = 0.0181$ | 276,000 |
| 2 | $e^{1.076} = 2.93$ | 0.293 | $(0.2678)^2 = 0.0717$ | 69,700 |
| 3 | $e^{0.717} = 2.05$ | 0.205 | $(0.3878)^3 = 0.0583$ | 85,800 |

Wait — let me recalculate $N=3$:

$R^* = e^{9.5/(3\times4.414)} = e^{0.717} = 2.049$

$\lambda = (1-0.10\times2.049)/(2.049-1) = 0.795/1.049 = 0.758$

Payload fraction per stage: $0.758/1.758 = 0.431$

Overall: $0.431^3 = 0.0801$

$m_0 = 5000/0.0801 = 62{,}400$ kg

Corrected table:

| Stages $N$ | $R^*$ | Overall payload fraction | $m_0$ (kg) |
|:---:|:---:|:---:|:---:|
| 1 | 8.60 | 0.0181 | 276,000 |
| 2 | 2.93 | 0.0717 | 69,700 |
| 3 | 2.05 | 0.0801 | 62,400 |

Diminishing returns: going from 1→2 stages saves 75% of mass; 2→3 stages saves only 10%.

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links

- [10.3 - Orbital Maneuvers - Hohmann Transfers](10.3---Orbital-Maneuvers---Hohmann-Transfers) — ΔV requirements that drive propellant budgets
- [10.5 - Atmospheric Flight Dynamics](10.5---Atmospheric-Flight-Dynamics) — Drag and gravity losses during ascent
- [10.7 - Interplanetary Trajectories - Patched Conics](10.7---Interplanetary-Trajectories---Patched-Conics) — High-ΔV missions requiring staging
- [4.4 - Central Forces & Keplerian Orbits](4.4---Central-Forces-&-Keplerian-Orbits) — Energy framework for orbit changes

### Authoritative External Sources

| Source | Description |
|--------|-------------|
| Curtis, H.D. *Orbital Mechanics for Engineering Students*, Ch. 11 | Rocket dynamics and staging |
| Sutton & Biblarz, *Rocket Propulsion Elements*, 9th ed. (Wiley, 2017) | Definitive propulsion textbook |
| MIT OCW 16.512 — Rocket Propulsion | Nozzle theory, combustion, performance |
| NASA SP-8012 through SP-8120 | Design criteria monographs |
| Humble, Henry & Larson, *Space Propulsion Analysis and Design* (McGraw-Hill) | Systems-level propulsion design |




---

## 📎 Appendix — Extended Topics

### A.1 Nozzle Theory and Exhaust Velocity

The exhaust velocity from a converging-diverging (de Laval) nozzle is derived from isentropic flow:

$$
v_e = \sqrt{\frac{2\gamma}{\gamma-1}\frac{R_u T_c}{M_w}\left[1 - \left(\frac{p_e}{p_c}\right)^{(\gamma-1)/\gamma}\right]}
$$

where:
- $\gamma$ = ratio of specific heats of exhaust gas
- $R_u$ = universal gas constant (8314 J/kmol·K)
- $T_c$ = combustion chamber temperature (K)
- $M_w$ = molecular weight of exhaust (kg/kmol)
- $p_e/p_c$ = exit-to-chamber pressure ratio

**Key insight:** High $v_e$ requires high $T_c$ and low $M_w$. This is why hydrogen ($M_w = 2$) gives the highest $I_{sp}$ among chemical propellants, despite lower energy density than hydrocarbons.

### A.2 Electric Propulsion Fundamentals

For ion thrusters, the exhaust velocity is determined by the accelerating voltage $V_a$:

$$
v_e = \sqrt{\frac{2qV_a}{m_i}}
$$

where $q$ is the ion charge and $m_i$ is the ion mass. For xenon ions ($m_i = 131$ amu, $q = e$):

$$
v_e = \sqrt{\frac{2(1.602\times10^{-19})V_a}{131\times1.661\times10^{-27}}} = 1209\sqrt{V_a} \text{ m/s}
$$

At $V_a = 1000$ V: $v_e = 38{,}200$ m/s ($I_{sp} = 3900$ s).

**Thrust limitation:** $F = \dot{m}v_e = P_{\text{elec}}\eta/(v_e/2)$ where $\eta$ is efficiency. High $v_e$ means low thrust for given power:

$$
F = \frac{2\eta P}{v_e}
$$

A 10 kW ion thruster with $\eta = 0.7$ and $v_e = 30$ km/s produces only $F = 2(0.7)(10000)/30000 = 0.47$ N.

### A.3 Gravity and Drag Losses (Detailed)

The ideal ΔV from the rocket equation must be augmented by losses:

$$
\Delta V_{\text{ideal}} = \Delta V_{\text{orbit}} + \Delta V_{\text{gravity}} + \Delta V_{\text{drag}} + \Delta V_{\text{steering}}
$$

Typical values for LEO insertion:
- Orbital velocity: 7.8 km/s
- Gravity loss: 1.0–1.5 km/s
- Drag loss: 0.1–0.3 km/s
- Steering loss: 0.1–0.2 km/s
- **Total ideal ΔV needed: 9.0–9.8 km/s**

**Gravity loss** for vertical ascent with constant thrust-to-weight $T/W$:

$$
\Delta V_g = g_0 t_b = g_0 \frac{m_p}{\dot{m}} = \frac{g_0 m_p v_e}{F} = \frac{v_e}{T/W_0}\left(1 - \frac{1}{R}\right)
$$

This shows why high $T/W$ (> 1.3) is critical for launch vehicles.

### Example 10.4.6 — Falcon 9 First Stage Analysis

**Given (approximate):**
- Propellant: LOX/RP-1, $I_{sp} = 282$ s (sea level), 311 s (vacuum)
- Stage mass (dry): 22,200 kg
- Propellant mass: 395,700 kg
- Payload to stage (2nd stage + fairing + payload): ~130,000 kg
- 9 Merlin 1D engines, total thrust: 7,607 kN (sea level)

**Analysis:**

Structural coefficient: $\epsilon = 22200/(22200+395700) = 0.053$ (excellent!)

Mass ratio: $R = (22200+395700+130000)/(22200+130000) = 547900/152200 = 3.60$

ΔV contribution (vacuum): $\Delta V = 311\times9.807\times\ln(3.60) = 3049\times1.281 = 3906$ m/s

Thrust-to-weight at liftoff: $T/W = 7607000/(547900\times9.807) = 1.415$

Burn time: $t_b = m_p/\dot{m} = 395700/(7607000/(311\times9.807)) = 395700/2494 = 159$ s

Gravity loss (estimated): $\Delta V_g \approx g_0 t_b \times 0.8 = 9.807\times159\times0.8 = 1247$ m/s (factor 0.8 for non-vertical trajectory)

Net ΔV delivered: $\approx 3906 - 1247 - 200 = 2459$ m/s




### A.4 Comparison of Propulsion Technologies

| Technology | $I_{sp}$ (s) | Thrust (N) | T/W | Application |
|:---:|:---:|:---:|:---:|:---:|
| Solid (SRB) | 250–290 | 10⁶–10⁷ | 100+ | Boosters, missiles |
| LOX/RP-1 | 300–350 | 10⁵–10⁷ | 50–100 | First stages (Falcon 9, Atlas) |
| LOX/LH₂ | 420–460 | 10⁴–10⁶ | 30–70 | Upper stages (Centaur, SSME) |
| N₂O₄/MMH | 310–340 | 10–10⁵ | 10–50 | Spacecraft propulsion |
| Nuclear thermal | 800–1000 | 10⁴–10⁵ | 3–10 | Interplanetary (NERVA concept) |
| Ion (Xe) | 1500–5000 | 0.01–1 | 10⁻⁴ | Deep space (Dawn, Starlink) |
| Hall thruster | 1500–3000 | 0.01–5 | 10⁻³ | Station-keeping, orbit raising |
| Pulsed plasma | 500–2000 | 10⁻⁶–10⁻³ | 10⁻⁵ | CubeSat propulsion |

### A.5 The Tyranny of the Rocket Equation

The exponential nature of the rocket equation creates severe constraints:

For $\Delta V/v_e = 1$: $R = e^1 = 2.72$ (63% propellant)
For $\Delta V/v_e = 2$: $R = e^2 = 7.39$ (86% propellant)
For $\Delta V/v_e = 3$: $R = e^3 = 20.1$ (95% propellant)
For $\Delta V/v_e = 4$: $R = e^4 = 54.6$ (98.2% propellant)

This exponential growth explains why:
- Single-stage-to-orbit is barely feasible (payload < 2%)
- Multi-staging is essential for high-ΔV missions
- High-$I_{sp}$ propulsion (even with low thrust) is transformative for deep space
- In-space refueling could revolutionize space architecture

### A.6 Propellant Budget Example — Mars Mission

A crewed Mars mission requires approximately:

| Phase | ΔV (km/s) |
|-------|:---------:|
| LEO departure | 3.6 |
| Mars orbit insertion | 2.1 |
| Mars surface descent | 4.1 |
| Mars ascent | 4.1 |
| Mars departure | 2.1 |
| Earth orbit insertion | 3.6 |
| **Total** | **19.6** |

With LOX/LH₂ ($v_e = 4.4$ km/s): $R = e^{19.6/4.4} = e^{4.45} = 85.6$

For a 50-ton payload: $m_0 = 85.6\times50 = 4280$ tons — clearly impractical without staging, aerobraking, or ISRU (in-situ resource utilization).

With nuclear thermal ($v_e = 9.0$ km/s): $R = e^{19.6/9.0} = e^{2.18} = 8.85$, $m_0 = 443$ tons — much more feasible.

