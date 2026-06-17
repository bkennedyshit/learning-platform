---
title: "30.1 — Electrical Fundamentals: Charge, Current, Voltage, Ohm & Kirchhoff"
subject: "Electronics"
catalog: advanced
audience_tier: higher-education
chapter: "30.1"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 30.1 — Electrical Fundamentals: Charge, Current, Voltage, Ohm & Kirchhoff

> *"Voltage pushes, current flows, resistance opposes. That sentence — said correctly — gets you 60% of EE."*

---

## 🎯 Learning Objectives

1. Define **charge** ($q$, coulombs), **current** ($i = dq/dt$, amperes), **voltage** ($v$, joules per coulomb), and **resistance** ($R$, ohms) from first principles.
2. State and apply **Ohm's law** ($V = IR$).
3. State and apply **Kirchhoff's Voltage Law (KVL)** and **Kirchhoff's Current Law (KCL)**.
4. Solve a multi-loop DC circuit by **mesh analysis** and **nodal analysis**.
5. Compute series + parallel resistor combinations; build voltage and current dividers.
6. Calculate **power** ($P = VI = I^2R = V^2/R$) and recognize when a resistor will exceed its rating.

---

## 🖼️ Visual Anchor

![elec__21.1-fig1](elec__21.1-fig1.svg)

---

## 📚 1. Definitions

### Definition 30.1.1 — Charge ($q$)
The conserved property of matter that produces electromagnetic interactions. Unit: **coulomb (C)**. Electron charge $e \approx 1.602\times10^{-19}\,\mathrm{C}$.

### Definition 30.1.2 — Current ($i$)
$$ i = \frac{dq}{dt} $$
Rate of charge flow. Unit: **ampere (A)** = 1 C/s. Conventional current flows from + to − (opposite to electron flow).

### Definition 30.1.3 — Voltage / Potential Difference ($v$)
Energy per unit charge. Unit: **volt (V)** = 1 J/C. A 9 V battery delivers 9 J to every coulomb that passes through it.

### Definition 30.1.4 — Resistance ($R$)
$$ R = \frac{V}{I} $$
Unit: **ohm (Ω)**. Property of materials that opposes current flow.

### Definition 30.1.5 — Power ($P$)
$$ P = VI = I^2 R = \frac{V^2}{R} $$
Unit: **watt (W)** = 1 J/s.

---

## 📐 2. The Two Laws

### Ohm's Law
For an ohmic device: $V = IR$. Most resistors. NOT diodes or transistors (non-linear).

### Kirchhoff's Voltage Law (KVL)
The algebraic sum of voltage drops around any closed loop is **zero**:
$$ \sum_{\text{loop}} v_k = 0 $$

### Kirchhoff's Current Law (KCL)
The algebraic sum of currents entering a node is **zero**:
$$ \sum_{\text{node}} i_k = 0 $$

---

## 🔧 3. Series, Parallel, Dividers

| Configuration | Formula |
|---|---|
| Resistors in series | $R_{\text{tot}} = R_1 + R_2 + \dots$ |
| Resistors in parallel | $\frac{1}{R_{\text{tot}}} = \frac{1}{R_1} + \frac{1}{R_2} + \dots$ |
| **Voltage divider** | $V_{\text{out}} = V_{\text{in}} \cdot \frac{R_2}{R_1 + R_2}$ |
| **Current divider** | $I_1 = I_{\text{tot}} \cdot \frac{R_2}{R_1 + R_2}$ |

---

## 🛠️ 4. Worked Example — Voltage Divider

**Problem:** A 9 V battery, $R_1 = 6\,\mathrm{k\Omega}$, $R_2 = 3\,\mathrm{k\Omega}$ in series. What is $V_{\text{out}}$ across $R_2$, and what is the current?

$$
V_{\text{out}} = 9 \cdot \frac{3000}{6000+3000} = 3\,\mathrm{V}
$$
$$
I = \frac{9}{6000+3000} = 1\,\mathrm{mA}
$$
$$
P_{R_1} = I^2 R_1 = (10^{-3})^2 \cdot 6000 = 6\,\mathrm{mW}
$$

A standard 1/4 W resistor handles this comfortably.

---

## 🛠️ 5. Mesh & Nodal Analysis (preview)

**Mesh** — assign a current to each loop, write KVL per loop, solve linear system.
**Nodal** — pick a reference (ground), assign $V$ to each other node, write KCL per node, solve.

For circuits with $n$ nodes and $b$ branches: $n - 1$ KCL equations and $b - n + 1$ KVL equations are independent.

> Full worked examples: see MIT 6.002 Lecture 4 + All About Circuits Vol. 1 Ch. 6.

---

## 🔗 6. Cross-links & Further Reading

### Internal
- [30.2 - Passive Components - Resistors, Capacitors, Inductors, Transformers](30.2---Passive-Components---Resistors,-Capacitors,-Inductors,-Transformers) — what circuits *do* over time
- [Subject_Plan](Subject_Plan) — the Maxwell-equation foundations

### External
- [MIT 6.002 — Circuits and Electronics (free)](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/)
- [Lessons in Electric Circuits — Vol. 1 DC](https://www.allaboutcircuits.com/textbook/direct-current/)
- [Khan Academy — Circuit analysis](https://www.khanacademy.org/science/electrical-engineering/ee-circuit-analysis-topic)
- [EEVblog Fundamentals Friday playlist](https://www.youtube.com/@EEVblog)

---

## ⚠️ 7. Common Misconceptions

- **"Voltage flows."** Voltage doesn't flow; it's a *difference* between two points. Current flows.
- **"More voltage = more current."** Only if R stays the same. A short circuit has tiny R; a small voltage produces enormous current.
- **"Ground is zero."** Ground is just a *reference node* you chose. Other circuits may have a different "ground."
- **"Series adds, parallel divides."** Resistors yes; capacitors and inductors invert this — see next chapter.
