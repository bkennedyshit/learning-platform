---
title: "30.3 — Semiconductors: Diodes, BJTs, MOSFETs, Op-Amps"
subject: "Electronics"
catalog: advanced
audience_tier: higher-education
chapter: "30.3"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 30.3 — Semiconductors: Diodes, BJTs, MOSFETs, Op-Amps

> *"A transistor is a current-controlled valve. An op-amp is a transistor pyramid pretending to be infinity."*

---

## 🎯 Learning Objectives

1. Explain p-n junction physics intuitively (depletion region, forward / reverse bias).
2. Use a **diode** for rectification, clamping, and protection.
3. Bias and use a **BJT** as a switch and as a small-signal amplifier (CE, CC, CB topologies).
4. Bias and use a **MOSFET** as a switch and amplifier; understand $V_{GS(th)}$, $R_{DS(on)}$.
5. Apply the two **op-amp golden rules** (no input current, no input voltage difference under negative feedback) to non-inverting, inverting, summing, integrator, differentiator topologies.
6. Recognize device datasheet parameters that matter (max $V$, max $I$, dissipation, switching time).

---

## 🖼️ Visual Anchor

![elec__21.3-fig1](elec__21.3-fig1.svg)

---

## 📚 1. Diodes

The p-n junction conducts when forward-biased (V_F ≈ 0.6–0.7 V for Si, 0.2–0.3 V for Schottky), blocks reverse.

Key uses:
- **Rectification** — half-wave + full-wave (bridge) rectifiers in power supplies.
- **Clamping / clipping** — limit voltages.
- **Flyback protection** — across inductive loads (motors, relays). Diode anode to motor−, cathode to motor+.
- **LEDs** — diodes that emit light; need a current-limiting resistor.

LED resistor: $R = (V_{\text{supply}} - V_F) / I_F$. For a 2 V LED at 10 mA from 5 V: $R = 300\,\Omega$.

---

## 🔧 2. BJTs — The Current-Controlled Valve

NPN small-signal (e.g., 2N2222):
- Three terminals: **B**ase, **C**ollector, **E**mitter.
- Forward-active rule: $I_C = \beta I_B$, $V_{BE} \approx 0.7$ V.
- $\beta$ (current gain) typical 100–300.

### As a switch (saturation mode)
1. Choose $I_C$ from your load (e.g., 100 mA for a relay coil).
2. Pick $I_B = I_C / \beta$ × safety factor (~10×): say 10 mA.
3. $R_B = (V_{\text{drive}} - V_{BE}) / I_B$.
4. Add a flyback diode if driving inductive load.

### Three topologies (small signal)
| Topology | Voltage gain | Input Z | Output Z | Use |
|---|---|---|---|---|
| Common-emitter (CE) | high (-) | medium | medium | classic amp |
| Common-collector (CC, "emitter follower") | ≈ 1 | high | low | impedance buffer |
| Common-base (CB) | high | low | high | RF |

---

## ⚡ 3. MOSFETs — Voltage-Controlled Switches Used Everywhere

Logic-level N-channel MOSFETs (e.g., IRLZ44N, AO3400) dominate modern switching:
- Three terminals: **G**ate, **D**rain, **S**ource.
- Gate is high-impedance (capacitive) → no static current.
- $V_{GS(th)}$ — threshold; below this, off. Above, drain-source channel opens.
- $R_{DS(on)}$ — on-resistance when fully on; minimize for low loss.

For switching a 5 A load:
- Pick a MOSFET with $V_{GS(th)}$ < your drive voltage − margin.
- Pick $R_{DS(on)}$ such that $P = I^2 R_{DS(on)}$ is well within the package thermal limit.

---

## ➗ 4. Op-Amps — The Near-Ideal Block

Two golden rules under **negative feedback**:
1. No current flows into the inputs ($I_+ = I_- = 0$).
2. The two inputs are at the same voltage ($V_+ = V_-$).

### Standard topologies

| Topology | Gain | Notes |
|---|---|---|
| Non-inverting | $1 + R_f/R_g$ | High input Z; gain ≥ 1 |
| Inverting | $-R_f/R_{\text{in}}$ | Low input Z = $R_{\text{in}}$ |
| Voltage follower | $1$ | Buffer; impedance match |
| Summing (inverting) | $-\sum (R_f/R_i)v_i$ | Audio mixer math |
| Integrator | $-\frac{1}{RC}\int v\,dt$ | Caution: drift |
| Differentiator | $-RC\frac{dv}{dt}$ | Caution: noise gain |
| Comparator / Schmitt | step | Open-loop or with positive feedback for hysteresis |

---

## 🛠️ 5. Worked Example (skeleton) — BJT Switch for an LED

- LED forward voltage 2 V, want $I_F = 20$ mA from a 5 V rail.
- Microcontroller drives BJT base via $R_B$.
- $R_C = (5 - 2 - V_{CE,\mathrm{sat}}) / 0.020 \approx 145\,\Omega$ (use 150 Ω E12).
- $I_B \approx I_C / \beta_{\min} \approx 0.020/100 = 200\,\mu\mathrm{A}$. Drive 10× = 2 mA → $R_B = (3.3 - 0.7)/0.002 = 1.3\,\mathrm{k\Omega}$ from a 3.3 V GPIO. Pick 1 kΩ for safety margin.

---

## 🔗 6. Cross-links & Further Reading

### Internal
- [30.2 - Passive Components - Resistors, Capacitors, Inductors, Transformers](30.2---Passive-Components---Resistors,-Capacitors,-Inductors,-Transformers)
- [30.4 - Digital Logic & Boolean Algebra - Gates, Flip-Flops, FSMs](30.4---Digital-Logic-&-Boolean-Algebra---Gates,-Flip-Flops,-FSMs) — gates are MOSFET pairs
- [30.7 - Power Electronics & Motor Drivers - PWM, H-Bridges, BLDC, Regulators](30.7---Power-Electronics-&-Motor-Drivers---PWM,-H-Bridges,-BLDC,-Regulators) — power MOSFETs in action

### External
- [MIT 6.002 — semiconductor lectures](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/)
- [The Art of Electronics — op-amp & transistor chapters (paid book, sample chapters online)](https://artofelectronics.net/)
- [Khan Academy — semiconductor & op-amp playlists](https://www.khanacademy.org/science/electrical-engineering)

---

## ⚠️ 7. Common Misconceptions

- **"Op-amps are ideal."** Real ones have offset, slew rate, finite gain-bandwidth, input bias current. Read the datasheet.
- **"BJTs are voltage-controlled."** They're current-controlled (well, charge-controlled). MOSFETs are voltage-controlled.
- **"A diode is a one-way wire."** It's also a 0.7 V drop, an exponential I-V curve, has reverse-recovery time, and breaks down past $V_R$.
- **"Logic-level MOSFET = always works at 3.3 V."** Some "logic-level" parts still need 4.5 V to fully turn on. Check $R_{DS(on)}$ vs $V_{GS}$ on the datasheet.
