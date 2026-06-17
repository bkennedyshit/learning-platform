---
title: "30.8 — From Electronics to Robotics: I²C, SPI, UART, CAN, Sensors & Actuators"
subject: "Electronics"
catalog: advanced
audience_tier: higher-education
chapter: "30.8"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 30.8 — From Electronics to Robotics: I²C, SPI, UART, CAN, Sensors & Actuators

> *"This is the chapter where 'electronics' becomes 'a robot'. Pick the right bus and the right sensor; the rest is software."*

This is the **capstone** of Track 30 and the **bridge** to [Track 32 - Robotics](Subject_Plan). Everything you've learned — passive components, transistors, digital logic, microcontrollers, motherboards, motor drivers — comes together when you connect a sensor to an MCU, decide on a protocol, and close the control loop.

---

## 🎯 Learning Objectives

1. Pick the right bus (UART, I²C, SPI, CAN, USB, Ethernet) for a given speed / distance / topology / robustness need.
2. Use **UART** for point-to-point text/binary streams; understand baud, framing, flow control.
3. Use **I²C** for low-speed multi-device buses; understand addressing, clock stretching, pull-ups.
4. Use **SPI** for high-speed master-multi-slave; understand modes (CPOL/CPHA), MISO/MOSI/SCLK/CS.
5. Use **CAN / CAN FD** for differential, robust, multi-master networks (automotive, industrial robots).
6. Connect canonical sensors (IMU, encoder, LiDAR, camera, ToF, GPS) and actuators (servo, DC motor, BLDC, stepper, solenoid).
7. Hand off from a microcontroller to a Linux SBC (Raspberry Pi, Jetson) — the **last mile** before ROS 2.

---

## 🖼️ Visual Anchor

> *Picture / video reference (external):*
> - 📺 [SparkFun Tutorials — I²C, SPI, UART, CAN](https://learn.sparkfun.com/)
> - 📺 [Adafruit — sensor breakout tutorials](https://learn.adafruit.com/)
> - 📖 [NXP CAN application notes (free PDFs)](https://www.nxp.com/docs/en/application-note/AN1798.pdf)

---

## 📚 1. Bus Protocol Comparison

| Bus | Wires | Topology | Speed (typ) | Distance | Notes |
|---|---|---|---|---|---|
| **UART** | 2 (TX, RX) + GND | point-to-point | 9600–115200 baud (up to ~12 Mbps) | < 30 cm raw, > 1 km via RS-485 | Asynchronous, no clock |
| **I²C** | 2 (SDA, SCL) + GND, pull-ups | multi-drop, addressed | 100 kHz / 400 kHz / 1 MHz / 3.4 MHz | < 30 cm | Up to 127 devices |
| **SPI** | 4 (MOSI, MISO, SCLK, CS) | master + N slaves (one CS each) | up to 50+ MHz | < 30 cm | Full-duplex, fast |
| **CAN / CAN FD** | 2 (CAN_H, CAN_L) differential | multi-master, multi-drop | 1 Mbps (CAN), 5–10 Mbps (CAN FD) | up to 40 m at 1 Mbps | Robust, automotive |
| **USB 2.0/3.x** | differential pair | host-device | 12 Mbps – 20 Gbps | up to 5 m | Hot-plug, complex stack |
| **Ethernet** | 4 pairs | switched | 100 Mbps – 10+ Gbps | 100 m on Cat5e/6 | TCP/UDP/ROS 2 / DDS |

### Quick decision tree
- 1 sensor, simple? → **UART** or **I²C**.
- Many sensors, low speed? → **I²C**.
- High speed (LCD, ADC, flash)? → **SPI**.
- Long wire, noisy environment, multiple nodes? → **CAN**.
- Lots of data, modular software stack? → **Ethernet** + ROS 2 / DDS.

---

## 🔄 2. UART — Asynchronous Serial

```
Idle:  HIGH
Frame: START(0) D0 D1 D2 D3 D4 D5 D6 D7 [PARITY] STOP(1)
```

- Baud rate must match on both ends.
- 8-N-1 (8 data, no parity, 1 stop) is the universal default.
- Add **RS-485** transceivers for differential, long-distance, multi-drop UART.

---

## 🔁 3. I²C — Two-Wire Multi-Device

```
SCL ────────────────_/¯¯_/¯¯_/¯¯_/¯¯ ...
SDA ──── START [ADDR R/W] ACK [DATA] ACK ... STOP
```

- Pull SDA + SCL high with 4.7 kΩ resistors.
- 7-bit (or 10-bit) address + R/W bit.
- Master drives SCL; slave can stretch (hold SCL low) to slow master.
- Common chips: BME280 (sensor), MPU-6050 (IMU), SSD1306 (OLED), DS3231 (RTC).

---

## ⚡ 4. SPI — Fast Full-Duplex

```
SCLK   _/¯\_/¯\_/¯\_ ...
MOSI    D7  D6  D5  ...
MISO    d7  d6  d5  ...
CS    ¯¯¯____________________¯¯¯
```

- **Modes** (CPOL, CPHA): 0/1/2/3 — must match between master and slave.
- One CS line per slave.
- Common: SD card, ADXL345 accelerometer, ENC28J60 Ethernet, NRF24L01 radio, displays.

---

## 🚗 5. CAN / CAN FD — Differential, Multi-Master

- Two wires (CAN_H, CAN_L) twisted pair, terminated 120 Ω each end.
- Each frame has an arbitration ID; bus arbitration is **non-destructive** (lower ID wins).
- **CAN FD** raises max payload from 8 to 64 bytes and data-phase up to ~10 Mbps.
- Dominant in automotive (OBD-II), industrial robots, drones (DroneCAN / Cyphal).
- ESP32, STM32, RP2040 (via external transceiver) all support CAN.

---

## 🛰️ 6. Canonical Sensors

| Sensor | Bus | Use |
|---|---|---|
| MPU-6050 / ICM-20948 / BNO055 (IMU) | I²C | Orientation, motion |
| BME280 / BMP388 | I²C / SPI | Temperature, humidity, pressure |
| VL53L0X / VL53L4CD (ToF) | I²C | Range 4 cm – 4 m |
| HC-SR04 (ultrasonic) | GPIO trig/echo | Range 2 cm – 4 m |
| AMT102 / quadrature encoders | GPIO | Motor position / speed |
| RPLIDAR A1 / A2 / A3 | UART | 2D LiDAR |
| Intel RealSense / OAK-D | USB | Depth + RGB |
| OV5640 / Arducam | DVP / MIPI / SPI | Camera |
| u-blox NEO-M8/M9 | UART / I²C | GPS |

---

## ⚙️ 7. Canonical Actuators

| Actuator | Drive | Use |
|---|---|---|
| Hobby servo (SG90, MG996R) | PWM 50 Hz | 0°–180° angle |
| Brushed DC motor | H-bridge + PWM | Wheels, gripper |
| Stepper motor | A4988 / DRV8825 / TMC2209 | Open-loop position |
| BLDC motor + ESC | 3-phase | Drones, e-bikes |
| Solenoid / relay | MOSFET + flyback diode | On/off |
| Linear actuator | H-bridge | Push/pull |

---

## 🛠️ 8. Worked Example (skeleton) — Two-Wheeled Robot Bridge

Goal: ESP32 reads IMU + encoders, drives two motors, and streams telemetry to a Raspberry Pi over UART for ROS 2 ingestion.

1. **Hardware** — ESP32 + dual-motor driver (DRV8833 or TB6612) + 2× geared DC motors + quadrature encoders + MPU-6050 IMU.
2. **Firmware** —
   - Read IMU over I²C at 200 Hz.
   - Read encoder pulses on GPIO interrupts.
   - PID per motor for velocity control.
   - Stream `[t, ωx, ωy, ωz, ax, ay, az, enc_left, enc_right]` over UART at 115200 baud.
3. **Pi side** —
   - Python serial reader → ROS 2 publisher → `/imu/data`, `/odom_raw`.
   - Combine in robot_localization (EKF) for fused odometry.
4. **Hand-off** — feeds [32 - Robotics](Subject_Plan) (Nav2, SLAM).

---

## 🔗 9. Cross-links & Further Reading

### Internal
- All previous chapters 21.1–30.7 — this is the integration chapter
- [32 - Robotics](Subject_Plan) — the next track picks up here
- [22.5 - ROS 2 & Middleware](22.5---ROS-2-&-Middleware) — what runs on the Pi side
- [22.3 - Sensors & Perception](22.3---Sensors-&-Perception) — sensor processing in depth

### External
- [SparkFun protocol tutorials](https://learn.sparkfun.com/tutorials)
- [Adafruit Learning System](https://learn.adafruit.com/)
- [NXP CAN application notes](https://www.nxp.com/docs/en/application-note/AN1798.pdf)
- [DroneCAN / Cyphal specs](https://opencyphal.org/)
- [robot_localization (ROS 2 EKF)](https://docs.ros.org/en/jazzy/p/robot_localization/)

---

## ⚠️ 10. Common Misconceptions

- **"USB is just plug-and-play."** Real USB stacks include enumeration, descriptors, classes, endpoints. Embedded USB is non-trivial; UART-over-USB-CDC is the easy path.
- **"I²C scales forever."** The bus is capacitance-limited; > ~30 cm or > ~10 devices and you'll see pull-up + edge-rate problems.
- **"SPI is always faster than I²C."** Yes, but pin count is 4× higher and topology is harder. Pick by need.
- **"CAN is automotive-only."** It's used everywhere robust, multi-node, mid-speed networking is needed — robotics, industrial, agriculture, marine.
- **"Just send raw bytes."** Without framing (length + CRC + sequence), serial corrupts silently. Use a frame format (COBS, SLIP, MAVLink, or DDS over Ethernet).

---

*Track 30 capstone complete. Continue to [32 - Robotics](Subject_Plan) — where electronics + control + perception become a robot.*
