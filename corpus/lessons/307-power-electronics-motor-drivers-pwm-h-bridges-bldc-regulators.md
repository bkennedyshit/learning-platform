---
title: "30.7 — Power Electronics & Motor Drivers: PWM, H-Bridges, BLDC, Regulators"
subject: "Electronics"
catalog: advanced
audience_tier: higher-education
chapter: "30.7"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 30.7 — Power Electronics & Motor Drivers: PWM, H-Bridges, BLDC, Regulators

> *"Signal electronics moves bits. Power electronics moves joules. Mix them up and your robot catches fire."*

---

## 🎯 Learning Objectives

1. Generate and reason about **PWM** (frequency, duty cycle, dead time).
2. Drive a brushed DC motor with an **H-bridge** (DRV8871, L298N, or discrete MOSFETs).
3. Drive a **brushless DC (BLDC) motor** with an **ESC** + 3-phase commutation.
4. Distinguish **linear regulators** (LDO, e.g., AMS1117) from **switching regulators** (buck, boost, buck-boost).
5. Pick a **regulator topology** for a given V_in/V_out/I_out and efficiency target.
6. Specify a **battery** (LiPo, Li-ion, LiFePO₄, lead-acid) and its **BMS** (battery management system).
7. Design **protection** (fuse, TVS, reverse-polarity diode/MOSFET, inrush limiter).

---

## 🖼️ Visual Anchor

> *Picture / video reference (external):*
> - 📺 [Texas Instruments — Motor Driver Training (free)](https://www.ti.com/motor-drivers/overview.html)
> - 📺 [GreatScott — H-bridge & BLDC explained](https://www.youtube.com/@greatscottlab)
> - 📺 [EEVblog — switching regulator deep-dives](https://www.youtube.com/@EEVblog)

---

## 📚 1. PWM Fundamentals

```
1.0 ┌─────┐    ┌─────┐    ┌─────┐
    │     │    │     │    │     │
    │     │    │     │    │     │
0.0 ┘     └────┘     └────┘     └────  time
    ←T→
```

- **Period $T$** → frequency $f = 1/T$.
- **Duty cycle $D \in [0,1]$** → average voltage = $D \cdot V_{\text{rail}}$.
- Higher $f$ means smaller filter caps but more switching loss.

Typical PWM frequencies:
- DC motors: 10–30 kHz (above audible).
- BLDC ESC: 8–24 kHz on each phase.
- LED dimming: 200 Hz–10 kHz.
- SMPS: 100 kHz–2+ MHz.

---

## 🔄 2. H-Bridge for Brushed DC Motors

```
        +V
         │
    ┌────┼────┐
    │    │    │
   [Q1] [Q2]
    │    │    │
    ├────M────┤        (M = motor)
    │    │    │
   [Q3] [Q4]
    │    │    │
    └────┼────┘
         │
        GND
```

- Q1 + Q4 on → forward.
- Q2 + Q3 on → reverse.
- All off → coast.
- Q3 + Q4 on (or Q1 + Q2) → brake (motor short).

**Never** turn Q1 + Q3 on simultaneously — that's a "shoot-through" short. Add **dead time** between switching transitions.

Integrated chips (DRV8871, BTS7960, TB6612FNG) bake this in with a logic interface.

---

## 🌀 3. BLDC + ESC

A brushless DC motor has 3 phases (U, V, W). To spin it, you cycle through 6 commutation states:

| Step | U | V | W |
|---|---|---|---|
| 1 | + | 0 | − |
| 2 | + | − | 0 |
| 3 | 0 | − | + |
| 4 | − | 0 | + |
| 5 | − | + | 0 |
| 6 | 0 | + | − |

Position feedback options:
- **Hall sensors** — 3 digital signals → step.
- **Sensorless** — read back-EMF on the floating phase.
- **Encoder** — quadrature for closed loop.

Modern algorithms:
- **Trapezoidal commutation** — simple, audible.
- **FOC / vector control** — quiet, efficient, the gold standard.

ESCs (electronic speed controllers) implement all this on a small board for you (drones, e-bikes, RC cars). Open-source firmware: **SimpleFOC**, **ODrive**, **VESC**.

---

## ⚙️ 4. Voltage Regulators

### 4.1 Linear (LDO)
- $V_{\text{out}} < V_{\text{in}}$, dissipates the difference as heat.
- Efficiency $\approx V_{\text{out}}/V_{\text{in}}$.
- Quiet, simple. Bad for big drops or high current.
- Examples: AMS1117 (3.3 V), LM7805 (5 V), LP5907 (low-noise).

### 4.2 Switching (SMPS)
- **Buck** ($V_{\text{out}} < V_{\text{in}}$): efficient step-down — 90%+.
- **Boost** ($V_{\text{out}} > V_{\text{in}}$): step-up.
- **Buck-boost / SEPIC**: either direction.
- Examples: MP1584 (buck), TPS61021 (boost), LMR43630 (modern integrated buck).

Trade-off: SMPS noisy → for sensitive analog (op-amps, ADC reference) cascade SMPS → LDO.

---

## 🔋 5. Battery Chemistries

| Chemistry | Nominal cell V | Energy density | Notes |
|---|---|---|---|
| Lead-acid | 2.0 V | low | Cheap, heavy, OK for solar |
| Ni-MH | 1.2 V | medium | Tolerant, declining usage |
| **Li-ion (NMC, NCA)** | 3.6–3.7 V | high | Phones, laptops, EVs |
| **LiPo** (Li-polymer) | 3.7 V | high | Drones, RC — needs care |
| **LiFePO₄ (LFP)** | 3.2 V | medium | Long cycle life, safer |
| Solid-state Li (emerging) | ~3.7 V | very high | 2026 — shipping in select EVs |

Always include a **BMS** (cell balancing, over/under-voltage cutoff) for multi-cell Li packs. Always **fuse** the pack output.

---

## 🛡️ 6. Protection Circuits

- **Fuse** at battery output.
- **Reverse-polarity** P-MOSFET (loss: a few mV) or Schottky diode (loss: 0.3 V).
- **TVS diode** across input for ESD / surge.
- **Inrush limiter** (NTC, soft-start) for big input caps.
- **Crowbar / OVP** circuits for catastrophic over-voltage.

---

## 🛠️ 7. Worked Example (skeleton) — Drive a 12 V DC Motor from a 3.3 V MCU

1. Pick a brushed gear motor: 12 V, ~1 A stall.
2. Pick H-bridge: DRV8871 (single-channel, 3.6 A peak, PWM input from 3.3 V).
3. Wire: 12 V battery → H-bridge VM; bridge OUT1/OUT2 → motor; IN1/IN2 from MCU PWM.
4. PWM at 20 kHz, duty 0–100%.
5. Add 100 µF bulk + 0.1 µF decoupling on VM.
6. Read motor current via the chip's IPROPI pin (or a shunt + op-amp) for current control.

---

## 🔗 8. Cross-links & Further Reading

### Internal
- [30.3 - Semiconductors - Diodes, BJTs, MOSFETs, Op-Amps](30.3---Semiconductors---Diodes,-BJTs,-MOSFETs,-Op-Amps) — power MOSFETs in detail
- [30.5 - Microcontrollers & Embedded Systems - Arduino, ESP32, RP2040, STM32](30.5---Microcontrollers-&-Embedded-Systems---Arduino,-ESP32,-RP2040,-STM32) — generating PWM
- [30.8 - From Electronics to Robotics - I2C, SPI, UART, CAN, Sensors & Actuators](30.8---From-Electronics-to-Robotics---I2C,-SPI,-UART,-CAN,-Sensors-&-Actuators) — closing the control loop
- [22.4 - Actuators & Motor Control](22.4---Actuators-&-Motor-Control) — robotics-side torque/velocity control

### External
- [Texas Instruments — Motor Driver training & app notes](https://www.ti.com/motor-drivers/overview.html)
- [SimpleFOC project](https://www.simplefoc.com/) — open-source FOC for makers
- [ODrive Robotics](https://odriverobotics.com/) — open-source servo + BLDC
- [VESC project](https://vesc-project.com/) — open-source motor controller (e-bikes, e-skates)

---

## ⚠️ 9. Common Misconceptions

- **"Higher PWM frequency is always better."** Switching loss + EMI + dead-time error scale with frequency. There is an optimum.
- **"LDO is fine; it's only a few hundred mA."** From 12 V to 3.3 V at 500 mA in an LDO dissipates ~4.4 W — a thermal disaster on a small SOT-223.
- **"BLDC ESCs and brushed-motor drivers are interchangeable."** Different topology, different commutation logic. Mismatch will kill the motor or the driver.
- **"Lithium batteries are robust."** They're not — over-charge, over-discharge, puncture, or thermal runaway can fire them. Use a BMS, always.
