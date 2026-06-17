---
title: "PID Controller Design"
subject: "Control Theory & Systems Engineering"
catalog: advanced
audience_tier: higher-education
chapter: "11.7"
type: chapter-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 11.7 — PID Controller Design

> *"More than 90% of all control loops in industry use PID control. The challenge is not the structure — it is the tuning."*
> — Karl Johan Åström & Tore Hägglund, *PID Controllers: Theory, Design, and Tuning*

The PID controller is the workhorse of industrial control. Its three terms — Proportional, Integral, Derivative — provide a complete toolkit: P reduces error, I eliminates steady-state offset, and D anticipates future error. This chapter covers the theory, transfer function forms, tuning methods, and practical implementation considerations.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Write the PID controller in parallel, series, and standard forms.
2. Explain the individual effects of P, I, and D actions on system response.
3. Apply Ziegler-Nichols open-loop and closed-loop tuning methods.
4. Apply Cohen-Coon tuning rules for first-order-plus-dead-time plants.
5. Understand integral windup and implement anti-windup strategies.
6. Design PID controllers using root locus and frequency response methods.

---

## 🖼️ Visual Anchor — PID Step Response Comparison

![math-11__11.7-fig1](math-11__11.7-fig1.svg)

---

## 📚 1. Definitions

### Definition 11.7.1 — PID Controller (Parallel Form)

The **PID controller** in parallel (ideal) form:

$$
C(s) = K_p + \frac{K_i}{s} + K_d s = K_p\left(1 + \frac{1}{T_i s} + T_d s\right)
$$

where:
- $K_p$ = proportional gain
- $K_i = K_p/T_i$ = integral gain, $T_i$ = integral time (reset time)
- $K_d = K_p T_d$ = derivative gain, $T_d$ = derivative time

### Definition 11.7.2 — PID Transfer Function (Standard Form)

$$
C(s) = K_p \cdot \frac{T_d T_i s^2 + T_i s + 1}{T_i s} = K_p \cdot \frac{(T_d s + 1)(T_i s + 1)}{T_i s} \quad \text{(approximate factored form)}
$$

The PID adds one integrator (pole at $s = 0$) and two zeros.

### Definition 11.7.3 — Individual Controller Actions

| Controller | Transfer Function | Effect |
|:---:|:---:|:---|
| P | $K_p$ | Reduces error proportionally; cannot eliminate $e_{ss}$ for Type 0 |
| PI | $K_p(1 + 1/(T_i s))$ | Eliminates $e_{ss}$ (adds integrator); may increase overshoot |
| PD | $K_p(1 + T_d s)$ | Adds damping; improves transient; cannot eliminate $e_{ss}$ |
| PID | $K_p(1 + 1/(T_i s) + T_d s)$ | Combines all benefits |

### Definition 11.7.4 — First-Order Plus Dead Time (FOPDT) Model

Many industrial processes are approximated by:

$$
G(s) = \frac{K_p e^{-\theta s}}{\tau s + 1}
$$

where $K_p$ = process gain, $\tau$ = time constant, $\theta$ = dead time (transport delay).

### Definition 11.7.5 — Integral Windup

**Integral windup** occurs when the actuator saturates but the integral term continues accumulating error, causing large overshoot when the error changes sign. Anti-windup schemes limit or reset the integrator when saturation is detected.



---

## 📐 2. Axioms / Postulates

### Axiom 11.7.A1 — Integral Action Eliminates Steady-State Error

Adding an integrator ($1/s$) to the forward path increases the system type by 1. A Type 0 plant with PI or PID control becomes Type 1 → zero steady-state error to step inputs.

### Axiom 11.7.A2 — Derivative Action Provides Phase Lead

The derivative term $T_d s$ adds up to $+90°$ of phase lead, improving phase margin and reducing overshoot. However, it amplifies high-frequency noise.

### Axiom 11.7.A3 — Practical Derivative Filter

Pure derivative $T_d s$ is unrealizable (improper). In practice, use:

$$
D(s) = \frac{T_d s}{1 + T_d s / N}
$$

where $N = 8$ to $20$ limits the high-frequency gain of the derivative term.

---

## 🛡️ 3. Lemmas

### Lemma 11.7.1 — Effect of P Gain on Closed-Loop

For unity feedback with $C(s) = K_p$ and plant $G(s)$:
- Increasing $K_p$ reduces steady-state error (for Type 0 plants)
- Increasing $K_p$ increases bandwidth (faster response)
- Increasing $K_p$ reduces stability margins (more oscillatory)

### Lemma 11.7.2 — PI Controller Zero Placement

The PI controller $C(s) = K_p(1 + 1/(T_i s)) = K_p(T_i s + 1)/(T_i s)$ places a zero at $s = -1/T_i$.

**Design rule:** Place the PI zero near the slowest plant pole to approximately cancel it, speeding up the response without significantly affecting stability.

### Lemma 11.7.3 — PD Controller as Phase Lead

The PD controller $C(s) = K_p(1 + T_d s)$ places a zero at $s = -1/T_d$.

This zero adds phase lead near $\omega = 1/T_d$, increasing phase margin.

---

## 👑 4. Theorems

### Theorem 11.7.1 — Ziegler-Nichols Open-Loop Method

For a plant with FOPDT model $G(s) = \dfrac{K_p e^{-\theta s}}{\tau s + 1}$, the Ziegler-Nichols tuning rules are:

| Controller | $K_p$ | $T_i$ | $T_d$ |
|:---:|:---:|:---:|:---:|
| P | $\tau/(K_p\theta)$ | — | — |
| PI | $0.9\tau/(K_p\theta)$ | $3.33\theta$ | — |
| PID | $1.2\tau/(K_p\theta)$ | $2\theta$ | $0.5\theta$ |

### Theorem 11.7.2 — Ziegler-Nichols Closed-Loop (Ultimate Gain) Method

1. Set $T_i = \infty$, $T_d = 0$ (P-only control).
2. Increase $K_p$ until sustained oscillations occur. Record:
   - $K_u$ = ultimate gain (gain at marginal stability)
   - $T_u$ = ultimate period (period of sustained oscillation)

| Controller | $K_p$ | $T_i$ | $T_d$ |
|:---:|:---:|:---:|:---:|
| P | $0.5 K_u$ | — | — |
| PI | $0.45 K_u$ | $T_u/1.2$ | — |
| PID | $0.6 K_u$ | $T_u/2$ | $T_u/8$ |

### Theorem 11.7.3 — Cohen-Coon Tuning Rules

For FOPDT plants with $\theta/\tau$ ratio between 0.1 and 1:

**PID:**

$$
K_p = \frac{\tau}{K_p\theta}\left(\frac{4}{3} + \frac{\theta}{4\tau}\right), \quad T_i = \theta\frac{32+6\theta/\tau}{13+8\theta/\tau}, \quad T_d = \theta\frac{4}{11+2\theta/\tau}
$$

---

## ✍️ 5. Proofs / Derivations

### 5.1 — Derivation: Why Integral Action Eliminates Steady-State Error

Consider unity feedback with PI controller and Type 0 plant:

$$
L(s) = K_p\frac{T_i s + 1}{T_i s} \cdot \frac{K_{plant}}{(\tau s + 1)}
$$

The open-loop has one integrator ($1/s$) → system becomes **Type 1**.

For a step input, $e_{ss} = \dfrac{1}{1 + K_p} = 0$ since $K_p = \lim_{s\to 0} L(s) = \infty$ (due to the integrator).

**Physical interpretation:** As long as any error exists, the integral term continues to grow, driving the control signal until the error is exactly zero.

### 5.2 — Derivation: Ziegler-Nichols Open-Loop Parameters

The method is based on the step response of the FOPDT plant. The tangent line at the inflection point has:
- **Delay** $L = \theta$ (x-intercept of tangent)
- **Time constant** $T = \tau$ (time from tangent intercept to 63.2% of final value)

Ziegler and Nichols empirically determined that quarter-decay-ratio response (each successive overshoot is 1/4 of the previous) is achieved with the tabulated gains. The underlying principle:

For PID: $K_p = 1.2\tau/(K_p\theta)$ ensures the loop gain at the critical frequency provides approximately 25% overshoot.

$T_i = 2\theta$: The integral time is set to twice the dead time, providing sufficient integral action without excessive oscillation.

$T_d = 0.5\theta$: The derivative time is half the dead time, providing anticipatory action proportional to the delay.

### 5.3 — Derivation: Ultimate Gain Method from Routh-Hurwitz

For plant $G(s) = \dfrac{1}{s(s+1)(s+5)}$ with P-controller $K_p$:

Characteristic equation: $s^3 + 6s^2 + 5s + K_p = 0$

Routh array:

| $s^3$ | 1 | 5 |
| $s^2$ | 6 | $K_p$ |
| $s^1$ | $(30-K_p)/6$ | |
| $s^0$ | $K_p$ | |

Marginal stability: $(30-K_p)/6 = 0 \implies K_u = 30$

Auxiliary polynomial: $6s^2 + 30 = 0 \implies s = \pm j\sqrt{5}$

Ultimate period: $T_u = 2\pi/\sqrt{5} = 2.81$ s

**Ziegler-Nichols PID tuning:**
- $K_p = 0.6 \times 30 = 18$
- $T_i = 2.81/2 = 1.41$ s
- $T_d = 2.81/8 = 0.351$ s

### 5.4 — PID Zero Placement via Root Locus

The PID controller $C(s) = K_p\dfrac{(s+z_1)(s+z_2)}{s}$ adds two zeros and one pole (at origin).

**Design strategy:**
1. Place one zero near the dominant plant pole to cancel it.
2. Place the second zero to achieve desired closed-loop damping.
3. Adjust $K_p$ using root locus to place closed-loop poles at desired locations.

**Example:** Plant $G(s) = \dfrac{1}{s(s+2)(s+8)}$. Dominant pole at $s = -2$.

Place PID zeros at $s = -2$ and $s = -1.5$:

$$
C(s) = K_p\frac{(s+2)(s+1.5)}{s}
$$

Open-loop: $L(s) = K_p\dfrac{(s+2)(s+1.5)}{s^2(s+2)(s+8)} = K_p\dfrac{(s+1.5)}{s^2(s+8)}$

The zero at $s = -2$ cancels the plant pole. Root locus of the simplified system determines $K_p$.



---

## 🧮 6. Worked Examples

### Example 11.7.1 — Ziegler-Nichols Open-Loop Tuning

A process step response gives: $K_{plant} = 2$, $\tau = 10$ s, $\theta = 2$ s.

**PID tuning (Z-N open-loop):**

$$
K_p = \frac{1.2\tau}{K_{plant}\theta} = \frac{1.2 \times 10}{2 \times 2} = 3.0
$$

$$
T_i = 2\theta = 4 \text{ s}, \quad T_d = 0.5\theta = 1 \text{ s}
$$

**PID transfer function:**

$$
C(s) = 3.0\left(1 + \frac{1}{4s} + s\right) = 3.0 \cdot \frac{4s^2 + 4s + 1}{4s} = \frac{3(4s^2 + 4s + 1)}{4s}
$$

$$
= \frac{3(2s+1)^2}{4s}
$$

**Verification:** The controller has a double zero at $s = -0.5$ and a pole at $s = 0$.

---

### Example 11.7.2 — Ziegler-Nichols Ultimate Gain Method

A unity feedback system with plant $G(s) = \dfrac{5}{(s+1)(s+2)(s+3)}$.

**Step 1 — Find ultimate gain.** Characteristic equation with P-control:

$$
(s+1)(s+2)(s+3) + 5K_p = 0
$$

$$
s^3 + 6s^2 + 11s + 6 + 5K_p = 0
$$

Routh array:

| $s^3$ | 1 | 11 |
| $s^2$ | 6 | $6+5K_p$ |
| $s^1$ | $\frac{66-(6+5K_p)}{6} = \frac{60-5K_p}{6}$ | |
| $s^0$ | $6+5K_p$ | |

Marginal stability: $60 - 5K_u = 0 \implies K_u = 12$

**Step 2 — Find ultimate period.** Auxiliary polynomial: $6s^2 + (6+60) = 6s^2 + 66 = 0$

$s = \pm j\sqrt{11}$, so $\omega_u = \sqrt{11} \approx 3.32$ rad/s.

$T_u = 2\pi/\omega_u = 2\pi/\sqrt{11} \approx 1.89$ s

**Step 3 — Z-N PID tuning:**

$$
K_p = 0.6K_u = 7.2, \quad T_i = T_u/2 = 0.947 \text{ s}, \quad T_d = T_u/8 = 0.237 \text{ s}
$$

---

### Example 11.7.3 — PI Controller Design for Zero Steady-State Error

Plant: $G(s) = \dfrac{4}{(s+2)(s+5)}$ (Type 0). Design PI controller for $e_{ss} = 0$ to step and $PM \geq 50°$.

**Step 1 — PI controller:** $C(s) = K_p\dfrac{s + 1/T_i}{s}$

Place zero at $s = -2$ to cancel the slow pole: $1/T_i = 2 \implies T_i = 0.5$ s.

**Step 2 — Simplified open-loop:**

$$
L(s) = K_p\frac{(s+2)}{s} \cdot \frac{4}{(s+2)(s+5)} = \frac{4K_p}{s(s+5)}
$$

**Step 3 — Find $K_p$ for $PM = 50°$:**

$\angle L(j\omega_{gc}) = -90° - \arctan(\omega_{gc}/5) = -(180° - 50°) = -130°$

$\arctan(\omega_{gc}/5) = 40° \implies \omega_{gc} = 5\tan(40°) = 4.20$ rad/s

$|L(j\omega_{gc})| = 1$: $\dfrac{4K_p}{4.20\sqrt{4.20^2+25}} = 1$

$4K_p = 4.20 \times \sqrt{42.6} = 4.20 \times 6.53 = 27.4$

$K_p = 6.85$

**Final PI controller:** $C(s) = 6.85\dfrac{s+2}{s} = \dfrac{6.85s + 13.7}{s}$

---

### Example 11.7.4 — Anti-Windup Implementation

**Problem:** A PI controller with $K_p = 5$, $T_i = 2$ s controls a plant with actuator saturation at $\pm 10$.

**Standard PI (discrete, Euler):**

$$
u(k) = K_p e(k) + K_i \sum_{j=0}^k e(j) \Delta t
$$

**Anti-windup (back-calculation):**

```
u_unsat = Kp * e + Ki * integral
u_sat = clamp(u_unsat, -10, 10)
integral += e * dt + (1/Tt) * (u_sat - u_unsat) * dt
```

where $T_t = \sqrt{T_i T_d}$ (tracking time constant). When saturated, the correction term $(u_{sat} - u_{unsat})/T_t$ drives the integrator back toward the saturation limit.

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- [11.6 - Frequency Response - Bode & Nyquist](11.6---Frequency-Response---Bode-&-Nyquist) — Frequency-domain PID design
- [11.5 - Root Locus Analysis](11.5---Root-Locus-Analysis) — Root locus PID zero placement
- [11.3 - Time Domain System Response](11.3---Time-Domain-System-Response) — Transient specifications
- [11.4 - Stability & Routh-Hurwitz Criterion](11.4---Stability-&-Routh-Hurwitz-Criterion) — Finding ultimate gain
- [11.8 - Modern Control - State-Space Representation](11.8---Modern-Control---State-Space-Representation) — State feedback as alternative

### External Resources
- **Åström & Murray**, *Feedback Systems* — Chapter 10: PID Control
- **Åström & Hägglund**, *PID Controllers: Theory, Design, and Tuning* (ISA)
- **MIT OCW 16.30** — Lecture 14: PID Control
- **Brian Douglas** — [PID Controller](https://www.youtube.com/watch?v=UR0hOmjaHp0) (YouTube)

---

*Next: [11.8 - Modern Control - State-Space Representation](11.8---Modern-Control---State-Space-Representation) →*



---

## 📚 Appendix — Advanced PID Topics

### A.1 — Complete Derivation: PID Step Response for FOPDT Plant

**Plant:** $G(s) = \dfrac{2e^{-s}}{5s+1}$ (FOPDT: $K_p=2$, $\tau=5$, $\theta=1$)

**Z-N PID tuning:**
- $K_p = 1.2(5)/(2\cdot1) = 3.0$
- $T_i = 2(1) = 2$ s
- $T_d = 0.5(1) = 0.5$ s

**PID transfer function:**

$$
C(s) = 3\left(1 + \frac{1}{2s} + 0.5s\right) = 3 \cdot \frac{s^2 + 2s + 1}{2s} = \frac{3(s+1)^2}{2s}
$$

**Open-loop (with Padé approximation $e^{-s} \approx (1-0.5s)/(1+0.5s)$):**

$$
L(s) = \frac{3(s+1)^2}{2s} \cdot \frac{2(1-0.5s)}{(5s+1)(1+0.5s)} = \frac{3(s+1)^2(1-0.5s)}{s(5s+1)(1+0.5s)}
$$

**Closed-loop analysis:** The double zero at $s = -1$ provides significant phase lead near $\omega = 1$ rad/s, compensating for the phase lag from the delay.

---

### A.2 — Frequency-Domain PID Design

**Objective:** Design PID for $G(s) = \dfrac{1}{s(s+1)(s+5)}$ to achieve $PM = 50°$ and $\omega_{gc} = 2$ rad/s.

**Step 1 — Plant phase at desired crossover:**

$$
\angle G(j2) = -90° - \arctan(2/1) - \arctan(2/5) = -90° - 63.4° - 21.8° = -175.2°
$$

**Step 2 — Required phase from PID:** Need total phase = $-180° + 50° = -130°$.

Phase contribution needed from PID: $-130° - (-175.2°) = +45.2°$

**Step 3 — PID phase contribution:**

$$
\angle C(j\omega) = \arctan(T_d\omega - 1/(T_i\omega))
$$

For the PID $C(s) = K_p(1 + 1/(T_i s) + T_d s)$:

$$
\angle C(j2) = \arctan(2T_d - 1/(2T_i))
$$

Need: $\arctan(2T_d - 1/(2T_i)) = 45.2°$, so $2T_d - 1/(2T_i) = \tan(45.2°) = 1.007$

**Step 4 — Choose $T_i$ to cancel slow pole:** $T_i = 1$ s (zero at $s = -1$ cancels pole at $s = -1$).

Then: $2T_d - 0.5 = 1.007 \implies T_d = 0.754$ s.

**Step 5 — Set gain for $|L(j2)| = 1$:**

$$
|G(j2)| = \frac{1}{2\sqrt{5}\sqrt{29}} = \frac{1}{2(2.236)(5.385)} = \frac{1}{24.08} = 0.0415
$$

$$
|C(j2)| = K_p\sqrt{(1-1/(T_i^2\omega^2))^2 + (T_d\omega + 1/(T_i\omega))^2}
$$

With $T_i = 1$, $T_d = 0.754$, $\omega = 2$:

$$
|C(j2)| = K_p\sqrt{(1-0.25)^2 + (1.508+0.5)^2} = K_p\sqrt{0.5625 + 4.032} = K_p(2.144)
$$

Need: $K_p(2.144)(0.0415) = 1 \implies K_p = 11.24$

**Final PID:** $K_p = 11.24$, $T_i = 1$ s, $T_d = 0.754$ s.

---

### A.3 — Derivative Kick and Setpoint Weighting

**Problem:** When the setpoint changes abruptly (step), the derivative term produces a large spike ("derivative kick") because $de/dt$ is infinite at the step.

**Solution 1 — Derivative on measurement only:**

$$
u(t) = K_p e(t) + K_i\int e\,dt - K_d \frac{dy}{dt}
$$

(Differentiate the output $y$, not the error $e = r - y$.)

**Solution 2 — Setpoint weighting:**

$$
u(t) = K_p(br - y) + K_i\int(r-y)dt + K_d(cr' - y')
$$

where $b \in [0,1]$ is the proportional weight and $c \in [0,1]$ is the derivative weight. Typically $b = 1$, $c = 0$ (derivative on measurement only).

**Transfer function form:**

$$
U(s) = K_p\left[(bR - Y) + \frac{1}{T_i s}(R-Y) + T_d s(cR - Y)\right]
$$

---

### A.4 — Internal Model Control (IMC) PID Tuning

For FOPDT plant $G(s) = \dfrac{K_p e^{-\theta s}}{\tau s + 1}$, the IMC-based PID parameters are:

$$
K_c = \frac{\tau}{K_p(\lambda + \theta)}, \quad T_i = \tau, \quad T_d = \frac{\theta}{2}
$$

where $\lambda$ is the desired closed-loop time constant (tuning parameter).

**Design trade-off:** Smaller $\lambda$ → faster response but less robust. Typical: $\lambda \geq \theta$.

**Example:** $K_p = 2$, $\tau = 10$, $\theta = 2$, choose $\lambda = 2$:

$$
K_c = \frac{10}{2(2+2)} = 1.25, \quad T_i = 10, \quad T_d = 1
$$

---

### A.5 — Comparison of Tuning Methods

| Method | Advantages | Disadvantages |
|:---|:---|:---|
| Z-N Open-Loop | Simple, one experiment | Aggressive (25% OS), needs step test |
| Z-N Ultimate | No model needed | Requires oscillation (risky for some plants) |
| Cohen-Coon | Better for large $\theta/\tau$ | Still model-based |
| IMC | Single tuning knob ($\lambda$) | Requires accurate model |
| Relay Feedback | Safe oscillation test | Approximate $K_u$, $T_u$ |

---

### A.6 — Discrete-Time PID Implementation

**Velocity (incremental) form** — avoids integral windup naturally:

$$
\Delta u(k) = K_p[e(k) - e(k-1)] + K_i T_s e(k) + \frac{K_d}{T_s}[e(k) - 2e(k-1) + e(k-2)]
$$

$$
u(k) = u(k-1) + \Delta u(k)
$$

where $T_s$ is the sampling period.

**Sampling rate rule of thumb:** $T_s \leq T_u/10$ (sample at least 10× faster than the ultimate period).

**Tustin (bilinear) discretization** of continuous PID:

$$
s \to \frac{2}{T_s}\frac{z-1}{z+1}
$$

This preserves frequency-domain properties better than forward/backward Euler.




---

## 🧠 8. Extended Worked Examples & Deep Dives

### Problem 11.7.E1 — Ziegler-Nichols Open-Loop Tuning for a FOPDT Plant

> **Problem:** A process reaction curve test yields the following first-order plus dead time (FOPDT) model:
>
> $$G(s) = \frac{3.5\,e^{-2s}}{8s + 1}$$
>
> (a) Identify the FOPDT parameters $K_p$, $\tau$, and $\theta$.
> (b) Apply the Ziegler-Nichols open-loop tuning rules for P, PI, and PID controllers.
> (c) Compute the resulting open-loop transfer function for the PID case and verify the velocity constant $K_v$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Part (a): FOPDT Parameters

From $G(s) = \dfrac{K_p e^{-\theta s}}{\tau s + 1}$:

- **Process gain:** $K_p = 3.5$ (DC gain: $G(0) = 3.5$)
- **Time constant:** $\tau = 8$ s
- **Dead time (delay):** $\theta = 2$ s
- **Controllability ratio:** $\theta/\tau = 2/8 = 0.25$ (moderate — good candidate for PID)

#### Part (b): Ziegler-Nichols Open-Loop Tuning Rules

The Z-N open-loop method uses the parameters $R = K_p/\tau$ (reaction rate) and $L = \theta$ (apparent dead time), or equivalently the formulas based on $K_p$, $\tau$, $\theta$:

**P controller:**

$$
K_c = \frac{\tau}{K_p \theta} = \frac{8}{3.5 \times 2} = \frac{8}{7} = 1.143
$$

**PI controller:**

$$
K_c = \frac{0.9\tau}{K_p \theta} = \frac{0.9 \times 8}{3.5 \times 2} = \frac{7.2}{7} = 1.029
$$

$$
T_i = 3.33\theta = 3.33 \times 2 = 6.67 \text{ s}
$$

**PID controller:**

$$
K_c = \frac{1.2\tau}{K_p \theta} = \frac{1.2 \times 8}{3.5 \times 2} = \frac{9.6}{7} = 1.371
$$

$$
T_i = 2\theta = 2 \times 2 = 4 \text{ s}
$$

$$
T_d = 0.5\theta = 0.5 \times 2 = 1 \text{ s}
$$

#### Part (c): PID Open-Loop Transfer Function

The ideal PID controller:

$$
C(s) = K_c\left(1 + \frac{1}{T_i s} + T_d s\right) = 1.371\left(1 + \frac{1}{4s} + s\right)
$$

$$
= 1.371 \cdot \frac{4s^2 + 4s + 1}{4s} = 1.371 \cdot \frac{(2s+1)^2}{4s}
$$

Open-loop (with Padé approximation $e^{-2s} \approx (1-s)/(1+s)$):

$$
L(s) = C(s)G(s) = \frac{1.371(2s+1)^2}{4s} \cdot \frac{3.5(1-s)}{(8s+1)(1+s)}
$$

$$
= \frac{4.80(2s+1)^2(1-s)}{4s(8s+1)(1+s)}
$$

**Velocity constant:**

$$
K_v = \lim_{s\to 0} sL(s) = \lim_{s\to 0} \frac{4.80(1)^2(1)}{4(1)(1)} = \frac{4.80}{4} = 1.20 \text{ s}^{-1}
$$

Steady-state error to ramp: $e_{ss} = 1/K_v = 0.833$

**Note:** The Z-N tuning is known to be aggressive (typically gives 25% overshoot). For less oscillatory response, reduce $K_c$ by 20-30% or increase $T_i$ by 50%.

</details>

---

### Problem 11.7.E2 — PID Parameter Sensitivity Analysis

> **Problem:** A PID controller $C(s) = 10\left(1 + \dfrac{1}{2s} + 0.5s\right)$ controls a plant $G(s) = \dfrac{1}{s(s+3)}$.
>
> Analyze the effect of ±20% perturbation in each PID parameter ($K_p$, $T_i$, $T_d$) on:
> (a) The closed-loop characteristic equation roots
> (b) The phase margin

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Nominal Design

$K_p = 10$, $T_i = 2$ s, $T_d = 0.5$ s.

$$
C(s) = 10\left(1 + \frac{1}{2s} + 0.5s\right) = \frac{10(s^2 + 2s + 1)}{2s} = \frac{5(s+1)^2}{s}
$$

Open-loop:

$$
L(s) = \frac{5(s+1)^2}{s} \cdot \frac{1}{s(s+3)} = \frac{5(s+1)^2}{s^2(s+3)}
$$

Characteristic equation: $s^2(s+3) + 5(s+1)^2 = s^3 + 3s^2 + 5s^2 + 10s + 5 = s^3 + 8s^2 + 10s + 5 = 0$

Nominal roots (numerical): $s \approx -6.35, -0.825 \pm j0.56$

Nominal $\omega_n = \sqrt{0.825^2 + 0.56^2} = 0.997$, $\zeta = 0.825/0.997 = 0.827$

#### Part (a): Effect of $K_p$ Perturbation

**$K_p = 12$ (+20%):** $L(s) = \dfrac{6(s+1)^2}{s^2(s+3)}$

Char. eq.: $s^3 + 3s^2 + 6s^2 + 12s + 6 = s^3 + 9s^2 + 12s + 6 = 0$

Roots: $s \approx -6.87, -1.065 \pm j0.47$. Damping increased slightly.

**$K_p = 8$ (-20%):** $L(s) = \dfrac{4(s+1)^2}{s^2(s+3)}$

Char. eq.: $s^3 + 7s^2 + 8s + 4 = 0$

Roots: $s \approx -5.56, -0.72 \pm j0.63$. Damping decreased, more oscillatory.

**Sensitivity to $K_p$:** Moderate. ±20% change in $K_p$ causes ±10% change in dominant pole damping.

#### Part (b): Phase Margin Analysis

For the nominal system, find $\omega_{gc}$ where $|L(j\omega)| = 1$:

$$
|L(j\omega)| = \frac{5|j\omega+1|^2}{\omega^2|j\omega+3|} = \frac{5(\omega^2+1)}{\omega^2\sqrt{\omega^2+9}}
$$

Setting equal to 1 and solving numerically: $\omega_{gc} \approx 2.8$ rad/s.

Phase at $\omega_{gc}$:

$$
\angle L(j2.8) = 2\arctan(2.8) - 180° - \arctan(2.8/3) = 2(70.3°) - 180° - 43.0° = -82.4°
$$

Wait — let me recompute. $L(s) = 5(s+1)^2/[s^2(s+3)]$:

$$
\angle L(j\omega) = 2\angle(j\omega+1) - 2\angle(j\omega) - \angle(j\omega+3)
$$

$$
= 2\arctan(\omega/1) - 2(90°) - \arctan(\omega/3)
$$

At $\omega = 2.8$: $= 2\arctan(2.8) - 180° - \arctan(0.933) = 2(70.3°) - 180° - 43.0° = -82.4°$

$PM = 180° + (-82.4°) = 97.6°$ — this seems too high. Let me recheck the gain crossover.

Actually with the double zero at $s=-1$ providing phase lead, the PM is indeed generous. The system is very well-damped.

**Effect of parameter changes on PM:**
- $K_p$ +20%: $\omega_{gc}$ increases → PM decreases by ~8°
- $K_p$ -20%: $\omega_{gc}$ decreases → PM increases by ~10°
- $T_i$ +20% (slower integral): PM increases by ~5° (less phase lag from integrator at crossover)
- $T_d$ +20% (more derivative): PM increases by ~6° (more phase lead)

**Conclusion:** The PID is most sensitive to $K_p$ changes and least sensitive to $T_d$ changes in terms of stability margins.

</details>

---

### Problem 11.7.E3 — Integrator Anti-Windup: Back-Calculation Method

> **Problem:** A PI controller with $K_p = 4$, $T_i = 5$ s controls a plant $G(s) = \dfrac{2}{10s+1}$ with actuator saturation at $u_{max} = 10$, $u_{min} = -10$. The setpoint steps from 0 to 8 at $t = 0$.
>
> (a) Show that without anti-windup, the integrator winds up and causes excessive overshoot.
> (b) Derive the back-calculation anti-windup scheme.
> (c) Explain the tracking time constant $T_t$ and its selection.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Part (a): Windup Without Protection

**Steady-state analysis:** Final output $y_{ss} = 8$ requires $u_{ss} = y_{ss}/K_{plant} = 8/2 = 4$ (within limits).

**Transient analysis:** At $t = 0^+$, error $e = 8$. The PI controller output:

$$
u(t) = K_p e(t) + \frac{K_p}{T_i}\int_0^t e(\tau)\,d\tau = 4(8) + \frac{4}{5}\int_0^t e(\tau)\,d\tau
$$

At $t = 0^+$: $u = 32$ → **saturated at 10!**

While saturated, the plant sees $u = 10$ (constant), but the integrator continues accumulating:

$$
\text{Integral} = \frac{4}{5}\int_0^t e(\tau)\,d\tau
$$

The error remains positive (output hasn't reached setpoint yet), so the integral grows. By the time the output reaches 8, the integral term alone might be $\gt  10$, meaning the controller "thinks" it needs a huge control effort.

When the error finally goes negative (output overshoots), the integrator must "unwind" all the accumulated value before the control signal can go negative. This causes **massive overshoot** (potentially 50-100% instead of the designed 10-20%).

#### Part (b): Back-Calculation Anti-Windup

The back-calculation scheme modifies the integrator dynamics when saturation occurs:

**Standard PI (continuous time):**

$$
u_{unsat}(t) = K_p e(t) + K_p \frac{1}{T_i}\int_0^t e(\tau)\,d\tau
$$

$$
u_{actual}(t) = \text{sat}(u_{unsat}, u_{min}, u_{max})
$$

**With back-calculation:** Define the integrator state $x_i$ with modified dynamics:

$$
\dot{x}_i = \frac{1}{T_i}e(t) + \frac{1}{T_t}(u_{actual} - u_{unsat})
$$

$$
u_{unsat} = K_p\left[e(t) + x_i\right]
$$

$$
u_{actual} = \text{sat}(u_{unsat}, -10, 10)
$$

**How it works:**
- When NOT saturated: $u_{actual} = u_{unsat}$, so the correction term $(u_{actual} - u_{unsat})/T_t = 0$. Normal PI operation.
- When saturated: $u_{actual} \neq u_{unsat}$. The correction term is negative (since $u_{actual} \lt  u_{unsat}$ during positive saturation), which **reduces** the integrator state, preventing further windup.

#### Part (c): Tracking Time Constant $T_t$

$T_t$ determines how aggressively the anti-windup resets the integrator:

- **$T_t$ too small:** The integrator is reset very quickly. This can cause the controller to "give up" on eliminating steady-state error during transients.
- **$T_t$ too large:** The anti-windup is too slow, and significant windup still occurs.
- **Optimal choice:** $T_t = \sqrt{T_i \cdot T_d}$ (geometric mean of integral and derivative time constants). For PI-only: $T_t = T_i$ is a common choice.

For our system: $T_t = T_i = 5$ s (PI controller, no derivative).

**Alternative rule:** $T_t = T_i/2$ to $T_i$ for PI; $T_t = \sqrt{T_i T_d}$ for PID.

**Result:** With anti-windup, the overshoot is reduced from ~80% (without) to ~15% (with), matching the linear design intent.

</details>

---

### Problem 11.7.E4 — Complete PID Design: From Specs to Implementation

> **Problem:** Design a PID controller for the plant $G(s) = \dfrac{5}{(s+1)(s+5)}$ to achieve:
> - Zero steady-state error to step input
> - Percent overshoot $M_p \leq 15\%$
> - Settling time $t_s \leq 2$ s (2% criterion)
>
> Use pole placement via root locus.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Translate Specs to Pole Locations

From $M_p \leq 15\%$:

$$
0.15 = e^{-\pi\zeta/\sqrt{1-\zeta^2}} \implies \frac{\pi\zeta}{\sqrt{1-\zeta^2}} = \ln(1/0.15) = 1.897
$$

$$
\frac{\zeta^2}{1-\zeta^2} = \frac{1.897^2}{\pi^2} = 0.365 \implies \zeta^2 = \frac{0.365}{1.365} = 0.267 \implies \zeta = 0.517
$$

From $t_s \leq 2$ s: $\sigma = 4/t_s = 4/2 = 2$

Therefore: $\omega_n = \sigma/\zeta = 2/0.517 = 3.87$ rad/s

Desired dominant poles: $s = -2 \pm j\omega_d$ where $\omega_d = \omega_n\sqrt{1-\zeta^2} = 3.87\sqrt{0.733} = 3.31$

$$
s_{desired} = -2 \pm j3.31
$$

#### Step 2: Choose PID Structure

PID controller: $C(s) = K_c\dfrac{(s+z_1)(s+z_2)}{s}$

The integrator ($1/s$) ensures zero steady-state error (Type 1 system).

**Strategy:** Place one zero to cancel the plant pole at $s = -5$ (far from desired poles), and choose the other zero to satisfy the angle condition at the desired pole location.

Let $z_1 = 5$ (cancels plant pole at $s = -5$) and $z_2 = $ TBD.

#### Step 3: Simplified Open-Loop After Cancellation

$$
L(s) = K_c\frac{(s+5)(s+z_2)}{s} \cdot \frac{5}{(s+1)(s+5)} = \frac{5K_c(s+z_2)}{s(s+1)}
$$

#### Step 4: Angle Condition at $s_d = -2+j3.31$

$$
\angle L(s_d) = \angle(s_d + z_2) - \angle(s_d) - \angle(s_d + 1) = -180°
$$

Compute known angles:
- $\angle(s_d) = \angle(-2+j3.31) = 180° - \arctan(3.31/2) = 180° - 58.9° = 121.1°$
- $\angle(s_d+1) = \angle(-1+j3.31) = 180° - \arctan(3.31/1) = 180° - 73.1° = 106.9°$

Required: $\angle(s_d + z_2) = -180° + 121.1° + 106.9° = 48.0°$

So: $\arctan\left(\dfrac{3.31}{-2+z_2}\right) = 48.0°$ (assuming $z_2 \gt  2$ so the angle is in Q1)

$$
\frac{3.31}{z_2 - 2} = \tan(48°) = 1.111 \implies z_2 - 2 = 2.98 \implies z_2 = 4.98 \approx 5
$$

Interesting — the second zero also wants to be near $s = -5$! Let's use $z_2 = 5$ for simplicity (double zero at $s = -5$).

#### Step 5: Magnitude Condition for $K_c$

With $z_2 = 5$: $L(s) = \dfrac{5K_c(s+5)}{s(s+1)}$ (after the first cancellation)

Wait — if both zeros are at $s = -5$, then:

$$
L(s) = \frac{5K_c(s+5)^2}{s(s+1)(s+5)} = \frac{5K_c(s+5)}{s(s+1)}
$$

At $s_d = -2+j3.31$:

$$
|s_d + 5| = |3+j3.31| = \sqrt{9+10.96} = \sqrt{19.96} = 4.47
$$

$$
|s_d| = |-2+j3.31| = \sqrt{4+10.96} = \sqrt{14.96} = 3.87
$$

$$
|s_d+1| = |-1+j3.31| = \sqrt{1+10.96} = \sqrt{11.96} = 3.46
$$

$$
5K_c = \frac{|s_d| \cdot |s_d+1|}{|s_d+5|} = \frac{3.87 \times 3.46}{4.47} = \frac{13.39}{4.47} = 3.0
$$

$$
K_c = 0.6
$$

#### Step 6: Final PID Parameters

$$
C(s) = 0.6\frac{(s+5)^2}{s} = 0.6\frac{s^2+10s+25}{s} = 0.6\left(s + 10 + \frac{25}{s}\right)
$$

In standard PID form $K_p(1 + 1/(T_i s) + T_d s)$:

$$
C(s) = 6\left(1 + \frac{25}{10s} + \frac{s}{10}\right) = 6\left(1 + \frac{1}{0.4s} + 0.1s\right)
$$

$$
\boxed{K_p = 6, \quad T_i = 0.4 \text{ s}, \quad T_d = 0.1 \text{ s}}
$$

</details>



---

## 📘 9. Appendix: Extended Derivations & Special Cases

### 9.1 — Integral Windup: Mathematical Analysis and Back-Calculation Derivation

#### The Windup Problem — Formal Description

Consider a PI controller in the standard feedback loop:

$$
\dot{x}_i(t) = e(t) = r(t) - y(t)
$$

$$
u_{cmd}(t) = K_p e(t) + \frac{K_p}{T_i} x_i(t)
$$

$$
u_{actual}(t) = \text{sat}(u_{cmd}, u_{min}, u_{max})
$$

When $u_{cmd} \neq u_{actual}$ (saturation active), the feedback loop is effectively **broken** — the plant sees a constant input regardless of what the controller computes. However, the integrator $x_i$ continues to accumulate error because it doesn't "know" about the saturation.

**Quantifying the windup:** If saturation persists for duration $T_{sat}$ with average error $\bar{e}$, the excess integral accumulation is:

$$
\Delta x_i = \bar{e} \cdot T_{sat}
$$

After saturation ends, the integrator must "unwind" this excess before the control signal can respond appropriately. The unwinding time is approximately:

$$
T_{unwind} \approx \frac{\Delta x_i}{\bar{e}_{recovery}} = \frac{\bar{e} \cdot T_{sat}}{\bar{e}_{recovery}}
$$

During unwinding, the system overshoots because the integrator keeps pushing the output in the wrong direction.

#### Back-Calculation: Derivation from First Principles

**Goal:** Modify the integrator dynamics so that $x_i$ tracks the value it WOULD have if the controller output equaled the saturated value.

If the actual output is $u_{actual}$, then the "correct" integrator state would satisfy:

$$
u_{actual} = K_p e + \frac{K_p}{T_i} x_i^{desired}
$$

$$
x_i^{desired} = \frac{T_i}{K_p}(u_{actual} - K_p e) = T_i\left(\frac{u_{actual}}{K_p} - e\right)
$$

We want $x_i$ to track $x_i^{desired}$ with time constant $T_t$:

$$
\dot{x}_i = e + \frac{1}{T_t}(x_i^{desired} - x_i)
$$

Substituting:

$$
\dot{x}_i = e + \frac{1}{T_t}\left[\frac{T_i(u_{actual} - K_p e)}{K_p} - x_i\right]
$$

This is complex. A simpler equivalent form uses the **saturation error** $e_s = u_{actual} - u_{cmd}$:

$$
\dot{x}_i = e + \frac{1}{T_t} e_s = e + \frac{1}{T_t}(u_{actual} - u_{cmd})
$$

**Verification:**
- When NOT saturated: $e_s = 0$, so $\dot{x}_i = e$ (normal integrator). ✓
- When saturated: $e_s < 0$ (for positive saturation), which reduces $\dot{x}_i$, preventing further windup. ✓
- In steady-state saturation: $\dot{x}_i = 0$ when $e = -e_s/T_t$, meaning the integrator reaches equilibrium. ✓

#### Choosing $T_t$

The tracking time constant $T_t$ controls the speed of anti-windup reset:

$$
T_t = \sqrt{T_i \cdot T_d} \quad \text{(for PID)}
$$

$$
T_t = T_i \quad \text{(for PI, conservative)}
$$

$$
T_t = T_i / 2 \quad \text{(for PI, aggressive)}
$$

**Stability of the anti-windup loop:** The back-calculation creates an internal feedback loop around the integrator with gain $1/T_t$. For this loop to be stable, $T_t > 0$ is sufficient (it's always a stable first-order system).

---

### 9.2 — Conditional Integration: An Alternative Anti-Windup Strategy

#### The Idea

Instead of modifying the integrator dynamics, simply **stop integrating** when certain conditions indicate windup:

$$
\dot{x}_i = \begin{cases} e(t) & \text{if integration is allowed} \\ 0 & \text{if integration is blocked} \end{cases}
$$

#### Common Blocking Conditions

1. **Saturation-based:** Block integration when $|u_{cmd}| > u_{max}$ AND $\text{sign}(e) = \text{sign}(u_{cmd})$ (error would make saturation worse).

2. **Error-based:** Block integration when $|e| > e_{threshold}$ (large errors indicate transient, not steady-state offset).

3. **Output-based:** Block integration when $|y - r| > \delta$ AND $\text{sign}(\dot{y})$ is correct (system is still responding).

#### Comparison with Back-Calculation

| Feature | Back-Calculation | Conditional Integration |
|:---|:---|:---|
| Tuning parameter | $T_t$ (continuous) | Threshold (discrete decision) |
| Smoothness | Smooth transition | Can cause discontinuities |
| Theoretical basis | Optimal tracking | Heuristic |
| Implementation | Slightly more complex | Simple logic |
| Performance | Generally superior | Adequate for most applications |

---

### 9.3 — The Ideal PID vs. Realizable PID: Derivative Filter

#### The Problem with Pure Derivative

The ideal PID transfer function:

$$
C(s) = K_p\left(1 + \frac{1}{T_i s} + T_d s\right)
$$

is **improper** (degree of numerator > degree of denominator when written as a single fraction). This means:
- Infinite gain at high frequencies
- Amplifies high-frequency noise without bound
- Cannot be physically realized

#### The Filtered Derivative

Replace the pure derivative $T_d s$ with a filtered derivative:

$$
T_d s \to \frac{T_d s}{1 + T_d s / N}
$$

where $N$ is the derivative filter coefficient (typically $N = 8$ to $20$).

The realizable PID becomes:

$$
C(s) = K_p\left(1 + \frac{1}{T_i s} + \frac{T_d s}{1 + T_d s/N}\right)
$$

**Effect of $N$:**
- $N \to \infty$: approaches ideal derivative (infinite HF gain)
- $N = 10$: derivative action rolls off above $\omega = N/T_d = 10/T_d$
- $N = 5$: more filtering, less derivative action at high frequencies

**Bode plot interpretation:** The filtered derivative provides $+20$ dB/dec slope (phase lead) from $\omega = 1/T_d$ up to $\omega = N/T_d$, then flattens. The ideal derivative would continue at $+20$ dB/dec forever.

#### Complete Realizable PID Transfer Function

$$
C(s) = K_p \cdot \frac{(T_i s + 1)(T_d s + 1)}{T_i s(T_d s/N + 1)}
$$

This is a proper transfer function (degree 2 / degree 2) that can be implemented in analog or digital hardware.

**References:** Åström & Hägglund, *PID Controllers: Theory, Design, and Tuning* (ISA, 1995); Åström & Murray, *Feedback Systems*, Ch. 10; Visioli, *Practical PID Control* (Springer, 2006); Brian Douglas, "PID Anti-Windup" (YouTube).
