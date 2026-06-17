---
title: "29.3 — Locomotion & Comfort Design"
subject: "VR"
catalog: advanced
audience_tier: higher-education
chapter: "29.3"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 29.3 — Locomotion & Comfort Design

> *"VR comfort is not optional polish — it is the difference between an app users recommend and an app users vomit on."*

---

## 🎯 Learning Objectives

1. Identify the **causes of simulator sickness** (vestibular-visual mismatch, vection, FoV).
2. Implement **teleport**, **smooth**, **arm-swing**, and **dash** locomotion correctly.
3. Apply **dynamic FoV vignette** during artificial motion.
4. Design **snap-turn** vs **smooth-turn** correctly.
5. Recognize **redirected walking** for room-scale.
6. Hit **frame-rate discipline** (90+ Hz native; 72 Hz minimum on Quest 3 with reprojection).
7. Apply **VAC** (vergence-accommodation conflict) mitigation patterns.

---

## 🖼️ Visual Anchor

![vrapp__24.3-fig1](vrapp__24.3-fig1.svg)

> *Picture / video reference (external):*
> - 📺 [Meta Comfort & Best Practices docs](https://developers.meta.com/horizon/resources/oculus-best-practices/)
> - 📺 [Oculus Locomotion design talks (free recordings)](https://developers.meta.com/horizon/resources/)
> - 📺 [GameDev.tv VR locomotion modules](https://www.gamedev.tv/)

---

## 📚 1. Why People Get Sick in VR

The **vestibular system** (inner ear) tells the brain about acceleration. The **visual system** tells the brain about motion through the world. When they disagree (you "see" running but feel still), the brain calls food poisoning.

Sensitivity varies wildly by user — and by experience exposure ("VR legs"). Design for the most sensitive 10% if you're building for general audiences.

---

## 🚶 2. Locomotion Patterns

| Type | How | Comfort | Typical use |
|---|---|---|---|
| **Stand-only / room-scale** | Walk physically | Highest | Arch-viz at human scale |
| **Teleport (point + click)** | Discrete jumps | High | Most consumer VR |
| **Dash** | Fast linear blink | Medium-high | Action games |
| **Smooth locomotion** | Joystick walk | Variable | Hardcore VR users |
| **Arm-swing** | Swing arms to walk | Medium | Fitness, gentler than smooth |
| **Vehicle / cockpit** | Motion in a vehicle frame | High | Sim racing, cockpits |
| **Redirected walking** | Subtly rotate world to keep room-bounded | High (when subtle) | Research / large-room |

---

## 🎯 3. Implementation Notes

### Teleport
- Show parabolic arc + valid landing target.
- Snap-fade transition (~150 ms) reduces vection.
- Disallow targets > 30° from current heading (forces snap-turn for big rotations).

### Smooth locomotion
- **Always pair with comfort vignette** — a circular mask that narrows FoV during motion.
- Provide an **off** toggle for users who don't need it.
- Cap speed; avoid abrupt acceleration (jerk = death).

### Snap-turn
- 30° default; 45° / 90° options.
- Snap-fade (~50 ms) preferred over smooth-rotate for sensitive users.

### Comfort vignette
- Activate during smooth locomotion + smooth-turn.
- Inner radius 0.5–0.7, outer 0.9, fade smoothly.
- Color match scene background to avoid hard frame.

---

## 🎚️ 4. Frame-Rate Discipline

| Headset | Native | Floor (with reprojection) |
|---|---|---|
| Quest 3 / 3S | 90 / 120 Hz | 72 Hz reprojection (avoid) |
| Vision Pro | 90 / 96 / 100 Hz | always native |
| Index 2 | 120 / 144 Hz | 90 Hz fallback |

**Cardinal rule:** if you can't sustain native frame rate, reduce visual fidelity (LOD, draw distance, post-FX) before allowing reprojection. Reprojection artifacts on hand-held content cause sickness.

---

## 👁️ 5. VAC Mitigation in VR (vs AR)

VR headsets have a **fixed focal plane** (typically 1.5–2 m). Content too close (< 0.5 m) or far causes vergence-accommodation conflict → eye strain.

Patterns:
- Place UI 1–2 m from the user.
- Avoid forcing close-range reading.
- Use **dynamic-focal-plane** displays (varifocal Vision Pro variants forthcoming) when available.

---

## 🛠️ 6. Worked Example (skeleton) — Bulletproof Locomotion Stack

1. Default: room-scale + teleport + 30° snap-turn.
2. Power-user toggle: smooth locomotion + smooth-turn with comfort vignette.
3. Always: snap-fade transitions; FoV vignette on artificial motion.
4. Sit/stand toggle for sit-only users.
5. Persistent comfort settings per user profile.

---

## 🔗 7. Cross-links & Further Reading

### Internal
- [29.2 - Immersive App Architectures - OpenXR, WebXR, Unity XR, Unreal XR](29.2---Immersive-App-Architectures---OpenXR,-WebXR,-Unity-XR,-Unreal-XR)
- [29.6 - Architectural Visualization in VR - Revit, IFC, USD to Quest & Vision Pro](29.6---Architectural-Visualization-in-VR---Revit,-IFC,-USD-to-Quest-&-Vision-Pro) — arch walkthrough comfort
- [13.5 - Sensor Fusion - Accelerometers & Gyroscopes](13.5---Sensor-Fusion---Accelerometers-&-Gyroscopes)
- [Subject_Plan](Subject_Plan) — vestibular system

### External
- [Meta Comfort & Best Practices](https://developers.meta.com/horizon/resources/oculus-best-practices/)
- [Apple Human Interface Guidelines for visionOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos)

---

## ⚠️ 8. Common Misconceptions

- **"VR sickness goes away with practice."** Mostly true — but design for first-timers because they decide whether they ever come back.
- **"Smooth locomotion is the realistic option."** Realism ≠ comfort. Many users prefer teleport.
- **"Vignette ruins immersion."** Done well, users don't notice; without it, they get sick.
- **"Frame rate doesn't matter as long as it doesn't stutter."** It does — sustained ≥90 Hz is the comfort baseline.
