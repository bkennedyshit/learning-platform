---
title: "32.4 — Actuators & Motor Control: Servos, BLDC, Steppers, Torque Control"
subject: "Robotics"
catalog: advanced
audience_tier: higher-education
chapter: "32.4"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 32.4 — Actuators & Motor Control: Servos, BLDC, Steppers, Torque Control

> *"Pick the wrong actuator and the rest of your robot is wallpaper. Pick the right one and a four-line PID loop is enough."*

---

## 🎯 Learning Objectives

1. Pick between hobby servo, geared DC + encoder, BLDC + FOC, stepper, harmonic-drive joint, and direct-drive torque motor for a given task.
2. Tune a PID **position** + **velocity** loop and recognize wind-up.
3. Implement **Field-Oriented Control (FOC)** for BLDC at a conceptual level (Clarke + Park transforms, current loops).
4. Drive a stepper in **closed-loop** mode (TMC2209/2240) and understand microstepping.
5. Distinguish **position**, **velocity**, **torque**, **impedance**, and **admittance** control.
6. Recognize 2026 capable open-source motor stacks: **SimpleFOC**, **ODrive**, **VESC**.

---

## 🖼️ Visual Anchor

> *Picture / video reference (external):*
> - 📺 [SimpleFOC project + tutorials](https://www.simplefoc.com/)
> - 📺 [ODrive Robotics — tutorials](https://docs.odriverobotics.com/)
> - 📺 [VESC project](https://vesc-project.com/)
> - 📺 [Skyentific — direct-drive robot teardowns](https://www.youtube.com/@Skyentific)

---

## 📚 1. Actuator Comparison

| Actuator | Pros | Cons | Use |
|---|---|---|---|
| Hobby servo (SG90, MG996R, DS3225) | Cheap, simple PWM | Limited torque, no torque feedback | Educational arms, eyes/grippers |
| Smart serial servo (Dynamixel, Feetech STS) | Position / velocity / torque modes; daisy-chain | Pricier | Educational humanoids, manipulators |
| Geared DC + encoder | Torque, configurable | Backlash, larger electronics | Wheels, low-cost arms |
| Stepper motor + driver | Open-loop position | Torque drops at speed; can skip steps | 3D printers, CNC, low-DOF arms |
| **BLDC + ESC / FOC** | High power-density, quiet, efficient | Driver complexity | Drones, e-bikes, modern joints |
| **Quasi-direct-drive (low-ratio + BLDC)** | High-bandwidth torque, backdrivable | Heavy, expensive | Quadrupeds, humanoids (MIT Cheetah, Unitree G1) |
| Harmonic / strain-wave drive | High ratio, zero backlash | Expensive, fragile | Industrial arms (UR, Franka) |
| Hydraulic | Massive force/weight | Hot, leaky, energy-hungry | Atlas (legacy), heavy industry |

---

## 📐 2. Control Hierarchy

```
        ┌─────────────────────────┐
high →  │   Trajectory / motion   │   m / rad
        │     planning            │
        └─────────────────────────┘
                ↓
        ┌─────────────────────────┐
        │   Position loop (P/PD)  │   ωref
        └─────────────────────────┘
                ↓
        ┌─────────────────────────┐
        │   Velocity loop (PI)    │   τref
        └─────────────────────────┘
                ↓
        ┌─────────────────────────┐
        │   Torque / current loop │   Vref
low  →  │   (FOC inner loop)      │
        └─────────────────────────┘
                ↓
              Motor
```

**Cascade tuning rule:** inner loop ~10× faster than the outer.

---

## ⚡ 3. Field-Oriented Control (FOC) for BLDC

A BLDC has 3 stator phases. FOC transforms the 3-phase current into a 2-axis "rotor frame" using:

- **Clarke transform** (3-phase abc → 2-phase αβ stator).
- **Park transform** (αβ stator → dq rotor frame, parameterized by rotor angle).

In the rotor frame:
- $i_d$ — flux-producing current (drive to 0 for non-salient PMSM at low speed).
- $i_q$ — torque-producing current.
- Torque ∝ $i_q$.

Two PI loops regulate $i_d, i_q$ to references; an outer velocity / position loop generates $i_q^{ref}$.

**Open-source implementations:** SimpleFOC (Arduino-grade), ODrive (high performance), VESC (e-bikes/e-skates).

---

## 🪜 4. Steppers in Closed Loop

Modern stepper drivers (TMC2209, TMC2240, TMC5160) include:
- 256× microstepping.
- StealthChop (silent) + SpreadCycle (high-load) modes.
- StallGuard for sensorless homing.
- Optional encoder feedback for closed-loop position.

A stepper with closed-loop encoder + StallGuard rivals a small BLDC for many low-speed positioning tasks at a fraction of the complexity.

---

## 💪 5. Beyond PID — Modern Control Modes

| Mode | What it does | When |
|---|---|---|
| **Position control** | Track $q_{des}$ | Pre-defined trajectories |
| **Velocity control** | Track $\dot q_{des}$ | Wheels, conveyors |
| **Torque control** | Track $\tau_{des}$ | Force tasks, contact |
| **Impedance control** | Specify $K, B$ around $q_{des}$ — soft like a spring | Human contact, polishing |
| **Admittance control** | Inverse of impedance — input = force, output = motion | Cooperative tasks |
| **MPC** | Model predictive: solve optimization each step | Quadrupeds, humanoids |
| **Whole-body control (WBC)** | Optimize all joints subject to contact + dynamics | Atlas, Optimus, Digit |

---

## 🛠️ 6. Worked Example (skeleton) — BLDC Drive with SimpleFOC

1. Hardware: gimbal-grade BLDC, AS5048A magnetic encoder (SPI), DRV8302 3-phase driver, ESP32 / STM32.
2. Wire driver + encoder; align rotor zero.
3. Initialize SimpleFOC: `motor.controller = MotionControlType::angle;`
4. Loop: `motor.move(target_angle); motor.loopFOC();`
5. Outer position loop, inner current loops happen inside the library.

---

## 🔗 7. Cross-links & Further Reading

### Internal
- [32.2 - Forward & Inverse Kinematics](32.2---Forward-&-Inverse-Kinematics) — joints' job description
- [32.7 - Manipulation & Grasping - MoveIt, GraspNet, Whole-body Control](32.7---Manipulation-&-Grasping---MoveIt,-GraspNet,-Whole-body-Control)
- [21.7 - Power Electronics & Motor Drivers - PWM, H-Bridges, BLDC, Regulators](21.7---Power-Electronics-&-Motor-Drivers---PWM,-H-Bridges,-BLDC,-Regulators)
- [Subject_Plan](Subject_Plan)

### External
- [SimpleFOC](https://www.simplefoc.com/)
- [ODrive Robotics](https://odriverobotics.com/)
- [VESC](https://vesc-project.com/)
- [Trinamic / ADI TMC datasheets](https://www.analog.com/en/products/tmc2209-la.html)
- [TI Motor Lab notes](https://www.ti.com/motor-drivers/overview.html)

---

## ⚠️ 8. Common Misconceptions

- **"PID is enough for everything."** It's enough for many things — but contact-rich + underactuated tasks need impedance / MPC / WBC.
- **"More gain = faster response."** And more oscillation, more saturation, and more chance of mechanical destruction.
- **"BLDC and stepper are interchangeable."** Different control + cost + thermal profiles. Steppers are torque-limited at speed; BLDCs are torque-limited by current.
- **"Direct-drive is exotic."** In 2026 quasi-direct-drive (1:6–1:9 ratio + low-cogging BLDC) is standard for legged robots — Unitree G1, Boston Dynamics electric Atlas, MIT Cheetah descendants.
