---
title: "30.4 — Digital Logic & Boolean Algebra: Gates, Flip-Flops, FSMs"
subject: "Electronics"
catalog: advanced
audience_tier: higher-education
chapter: "30.4"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 30.4 — Digital Logic & Boolean Algebra: Gates, Flip-Flops, FSMs

> *"A CPU is a finite state machine the size of a small city. Master a 4-bit counter and you've already learned the pattern."*

---

## 🎯 Learning Objectives

1. Apply Boolean algebra and **De Morgan's laws** to simplify logic expressions.
2. Convert any logic to **NAND-only** or **NOR-only** form.
3. Reduce a 3- or 4-variable truth table with a **Karnaugh map**.
4. Recognize and use AND, OR, NOT, NAND, NOR, XOR, XNOR gates and their CMOS implementations.
5. Distinguish **combinational** from **sequential** logic.
6. Use SR latches, D latches, D/JK/T flip-flops; build registers, counters, shift registers.
7. Design a **Moore** or **Mealy** finite state machine on paper and code it on a microcontroller or FPGA.

---

## 🖼️ Visual Anchor

![elec__21.4-fig1](elec__21.4-fig1.svg)

---

## 📚 1. Boolean Algebra Cheat Sheet

| Identity | |
|---|---|
| $A + 0 = A$, $A \cdot 1 = A$ | identity |
| $A + 1 = 1$, $A \cdot 0 = 0$ | annihilation |
| $A + A = A$, $A \cdot A = A$ | idempotent |
| $A + \bar A = 1$, $A \cdot \bar A = 0$ | complement |
| $\overline{A + B} = \bar A \cdot \bar B$ | **De Morgan** |
| $\overline{A \cdot B} = \bar A + \bar B$ | **De Morgan** |

**Functional completeness:** {NAND} alone, or {NOR} alone, can express any Boolean function. CMOS uses NAND/NOR as primitives.

---

## 🛠️ 2. Combinational Building Blocks

| Block | Inputs / Outputs | Use |
|---|---|---|
| Multiplexer (MUX) | $2^n$ data, $n$ select, 1 out | bus selection |
| Demultiplexer (DEMUX) | 1 in, $n$ select, $2^n$ out | broadcast |
| Encoder | $2^n$ in, $n$ out | priority encoding |
| Decoder | $n$ in, $2^n$ out | address decoding |
| Adder | full adder = sum + carry | arithmetic |
| Comparator | $A$, $B$ → $A<B$, $A=B$, $A>B$ | branching logic |
| Tri-state buffer | enable + data → bus or hi-Z | shared buses |

---

## 🔁 3. Sequential Logic

State is added by **feedback** + a clock.

| Element | Behavior |
|---|---|
| SR latch | Set/Reset; level-sensitive, prone to invalid state |
| D latch | output follows D when enable high |
| **D flip-flop (DFF)** | output captures D on clock edge — the workhorse |
| JK flip-flop | toggle, set, reset depending on J/K |
| T flip-flop | toggle on clock edge if T=1 |

**Registers** = N parallel DFFs. **Counters** = registers + adder + feedback.

---

## 🤖 4. Finite State Machines

A FSM is $(S, \Sigma, \delta, s_0, F)$:
- $S$ — set of states
- $\Sigma$ — input alphabet
- $\delta : S \times \Sigma \to S$ — transition function
- $s_0$ — initial state
- $F$ — output function

**Moore** — output depends only on state. **Mealy** — output depends on state + input.

### Design steps
1. Sketch the state diagram.
2. Encode states (binary, one-hot, gray).
3. Build the **next-state table** and **output table**.
4. Implement next-state logic with combinational gates / DFFs (or in HDL: Verilog / VHDL / SystemVerilog / Chisel).
5. Reset logic: synchronous vs asynchronous reset.

### Example: vending machine
States: $\{\mathrm{IDLE}, \mathrm{COIN5}, \mathrm{COIN10}, \mathrm{COIN15}, \mathrm{DISPENSE}\}$. Inputs: 5¢, 10¢. Output: dispense if total ≥ 15¢.

---

## 🛠️ 5. Worked Example (skeleton) — 4-bit Synchronous Counter

- 4 D flip-flops sharing a clock.
- Combinational logic generates next count from current count.
- T flip-flops simplify: $T_n = Q_0 \cdot Q_1 \cdot \ldots \cdot Q_{n-1}$.
- Add an enable + sync reset.

Implement:
- On a microcontroller (any language): 4 GPIO outputs + a timer.
- On an FPGA in Verilog: 12 lines of code.
- On breadboard with 74HC74 (DFF) + 74HC08 (AND).

---

## 🔗 6. Cross-links & Further Reading

### Internal
- [30.3 - Semiconductors - Diodes, BJTs, MOSFETs, Op-Amps](30.3---Semiconductors---Diodes,-BJTs,-MOSFETs,-Op-Amps) — CMOS implements gates
- [30.5 - Microcontrollers & Embedded Systems - Arduino, ESP32, RP2040, STM32](30.5---Microcontrollers-&-Embedded-Systems---Arduino,-ESP32,-RP2040,-STM32) — what runs sequential logic at scale
- [30.6 - Motherboards & Computer Architecture - CPU, RAM, Chipset, PCIe, UEFI](30.6---Motherboards-&-Computer-Architecture---CPU,-RAM,-Chipset,-PCIe,-UEFI) — the CPU is a giant FSM

### External
- [MIT 6.004 lectures + handouts](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/)
- [nand2tetris — free curriculum building a computer from NAND](https://www.nand2tetris.org/)
- [Ben Eater — 8-bit CPU + 6502](https://www.youtube.com/@BenEater)
- [Yosys + nextpnr — open-source FPGA toolchain](https://yosyshq.net/yosys/)

---

## ⚠️ 7. Common Misconceptions

- **"NAND vs NOR — pick one."** Either is functionally complete. Most modern CMOS uses both (NAND in series, NOR in parallel) for area/speed tradeoffs.
- **"Latches and flip-flops are the same."** Latches are level-sensitive (transparent while enable high); flip-flops capture only on the clock edge. Latches are mostly avoided in synthesizable RTL.
- **"Synchronous reset is always best."** Synchronous reset is preferred for clean simulation, but asynchronous reset is required for power-on-reset before the clock is stable.
- **"FPGAs and microcontrollers are interchangeable."** FPGAs run hardware in parallel; microcontrollers run software sequentially. Pick by latency / parallelism need.
