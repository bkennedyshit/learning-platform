---
date: 2026-05-26
type: subject-readme
tags: [practice, refresher, drills, source-materials, study-aids, electronics, embedded, microcontrollers, motherboards]
title: "README — 30 - Electronics"
---

# 30 - Electronics — Subject Hub

> One-page subject hub. Lists chapters, source reading materials, **video / picture references stored outside the repo**, and placeholders for generated study aids.
> Master practice guide: [[../HOW_TO_USE_PRACTICE|HOW_TO_USE_PRACTICE]].

> **Asset storage convention.**
> - **SVG diagrams** (text, in-vault) → `../_svgs/elec__<chapter>-fig<n>.svg`.
> - **Pictures, screenshots, oscilloscope traces, datasheets, videos** are NOT committed to this repo. Reference them by **URL** in this README and chapter notes.

---

## 🚀 Quick start

```bash
cd "C:/Obsidian Vault/Bill's Vault/05-Knowledge_Foundation/09 - Learning/30 - Electronics"
# Drill scripts (LTspice batch runners, MicroPython examples) — to be added
```

For hands-on simulation without hardware, use [Wokwi](https://wokwi.com/) (browser sim for Arduino / ESP32 / RP2040) or LTspice for analog circuits.

---

## 📜 Chapter index

- [[30.1 - Electrical Fundamentals - Charge, Current, Voltage, Ohm & Kirchhoff]]
- [[30.2 - Passive Components - Resistors, Capacitors, Inductors, Transformers]]
- [[30.3 - Semiconductors - Diodes, BJTs, MOSFETs, Op-Amps]]
- [[30.4 - Digital Logic & Boolean Algebra - Gates, Flip-Flops, FSMs]]
- [[30.5 - Microcontrollers & Embedded Systems - Arduino, ESP32, RP2040, STM32]]
- [[30.6 - Motherboards & Computer Architecture - CPU, RAM, Chipset, PCIe, UEFI]]
- [[30.7 - Power Electronics & Motor Drivers - PWM, H-Bridges, BLDC, Regulators]]
- [[30.8 - From Electronics to Robotics - I2C, SPI, UART, CAN, Sensors & Actuators]]

---

## 🎬 Video & Picture References (external — open in browser)

### 📺 Video Channels & Courses

| Channel / Course | Track Use | Link |
|---|---|---|
| **MIT 6.002 — Circuits and Electronics** | Foundational EE | [ocw.mit.edu/6-002](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) |
| **MIT 6.004 — Computation Structures** | Digital → CPU architecture | [ocw.mit.edu/6-004](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) |
| **EEVblog (Dave Jones)** | Practical electronics, instrumentation | [@EEVblog](https://www.youtube.com/@EEVblog) |
| **Ben Eater** | Build a CPU on breadboards (digital logic gold) | [@BenEater](https://www.youtube.com/@BenEater) |
| **GreatScott!** | Hobby → engineering bridge | [@greatscottlab](https://www.youtube.com/@greatscottlab) |
| **W2AEW** | RF + scope technique | [@w2aew](https://www.youtube.com/@w2aew) |
| **The Signal Path** | Advanced instrumentation, scopes | [@TheSignalPathBlog](https://www.youtube.com/@TheSignalPathBlog) |
| **DigiKey YouTube** | Practical electronics quick-bites | [@digikey](https://www.youtube.com/@digikey) |
| **Microchip Makes / SparkFun / Adafruit YouTube** | Tutorials per chip / breakout | various |
| **Altium Education (free PCB curriculum)** | PCB design from scratch | [education.altium.com](https://education.altium.com/) |
| **Coursera — Foundations of Embedded Software Design** | Embedded fundamentals | [coursera.org](https://www.coursera.org/learn/foundations-of-embedded-software-design) |
| **Coursera — Introduction to Chip Design with Open-Source EDA Tools** | RTL → silicon flow | [coursera.org](https://www.coursera.org/learn/introduction-to-chip-design-with-open-source-eda-tools) |

### 🖼️ Picture / Diagram Reference Sources

| Source | What it gives you | Link |
|---|---|---|
| **Lessons in Electric Circuits (Kuphaldt)** | Schematics, waveforms, pedagogy art | [allaboutcircuits.com/textbook](https://www.allaboutcircuits.com/textbook/) |
| **TI / NXP / STMicro / Microchip datasheets** | Authoritative pinouts, internal block diagrams | manufacturer sites |
| **Adafruit Learning System** | Beautifully illustrated tutorials | [learn.adafruit.com](https://learn.adafruit.com/) |
| **SparkFun Tutorials** | Annotated wiring diagrams | [learn.sparkfun.com](https://learn.sparkfun.com/) |
| **Arm Cortex-M reference manuals** | Architecture diagrams | [developer.arm.com](https://developer.arm.com/) |
| **Open Circuits (Schlaepfer & Oskay)** | Component cross-section photos | [openocircuits.com](https://opencircuits.com/) (preview / book) |
| **Wikichip** | CPU die shots + microarchitecture | [en.wikichip.org](https://en.wikichip.org/) |

### 📚 Open-Source / Free Books

| Title | Author / Provider | Link |
|---|---|---|
| Lessons in Electric Circuits (6 volumes) | Tony Kuphaldt | [allaboutcircuits.com/textbook](https://www.allaboutcircuits.com/textbook/) |
| Foundations of Analog and Digital Electronic Circuits (6.002 companion) | Agarwal & Lang | [ocw.mit.edu/6-002](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) |
| Embedded-Systems-Fundamentals (Arm University) | Arm | [github.com/arm-university/Embedded-Systems-Fundamentals](https://github.com/arm-university/Embedded-Systems-Fundamentals) |
| KiCad documentation | KiCad project | [docs.kicad.org](https://docs.kicad.org/) |
| MicroPython documentation | MicroPython project | [docs.micropython.org](https://docs.micropython.org/) |
| ESP-IDF Programming Guide | Espressif | [docs.espressif.com/projects/esp-idf](https://docs.espressif.com/projects/esp-idf/en/latest/) |
| Raspberry Pi Pico (RP2040) C SDK & Examples | Raspberry Pi Foundation | [github.com/raspberrypi/pico-sdk](https://github.com/raspberrypi/pico-sdk) |
| ARM Cortex-M technical reference manuals | Arm | [developer.arm.com](https://developer.arm.com/) |
| Computer Organization and Design — companion slides (free) | Patterson & Hennessy | publisher / university course pages |

---

## 🧰 Generated study aids

### 🎙️ Audio overviews & podcasts (NotebookLM)
- [ ] TODO: NotebookLM audio of the Subject_Plan

### 🧠 Mind maps
- [ ] TODO: NotebookLM mind-map URL

### ❓ Quizzes
- [ ] TODO: NotebookLM-generated quiz

### 📊 Reports & summaries
- [ ] TODO: NotebookLM "Briefing Doc"

### 🃏 Flash cards
- [ ] TODO: Anki / Obsidian SR deck

### 🎬 Video overviews
- [ ] TODO: personal Loom of breadboard builds

### 📋 Data tables
- [ ] TODO: comparison matrix (Arduino vs ESP32 vs RP2040 vs STM32 — flash, RAM, ADC, peripherals, price)

---

## 🔗 Cross-links

- Syllabus & curriculum mindmap: [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/30 - Electronics/Subject_Plan]]
- Visual roadmap: [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/30 - Electronics/LEARNING_PATH]]
- Direct downstream: [[../32 - Robotics/Subject_Plan|32 - Robotics]]
- Hardware-side of holographic displays: [[../31 - Holographics/Subject_Plan]]
- VR hardware understanding: [[../29 - VR/Subject_Plan]]
- Foundations: [[../07 - Math and Physics/07 - Electrodynamics & Classical Field Theory/Subject_Plan]]
- Master Learning index: [[00 - 09 - Learning Index]]
- Master practice guide: [[../HOW_TO_USE_PRACTICE]]
