---
title: "33.5 — 3D Printing & Additive Manufacturing"
subject: "Mechanical Engineering & Fabrication"
catalog: advanced
audience_tier: higher-education
chapter: "33.5"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 33.5 — 3D Printing & Additive Manufacturing

> *"The printer doesn't know physics. Your design has to teach it."*

---

## 🎯 Learning Objectives

1. Describe the FDM, SLA/MSLA, SLS, and DMLS processes at a technical level including key parameters.
2. Select print orientation, layer height, infill pattern, and wall count for a given functional part.
3. Diagnose and fix 8 common FDM print failures.
4. Install heat-set threaded inserts correctly and explain why they beat printed threads.
5. Apply tolerance compensation for FDM holes and mating parts.
6. Describe the full post-processing pipeline: support removal → sanding → priming → finishing.

---

## 🖼️ Visual Anchor

![mech__34.5-fig1](mech__34.5-fig1.svg)

---

## 📚 1. FDM — Fused Deposition Modelling

### 1.1 How FDM Works

A thermoplastic filament (1.75mm or 2.85mm diameter) is fed through a heated nozzle (hotend), melted, and extruded onto a heated build plate in layers from bottom to top. The previous layer is the foundation for the next.

**Key FDM components:**
- **Hotend:** Heats filament to 200–320°C depending on material
- **Cold end:** Motor drives filament into hotend (direct drive or bowden)
- **Build plate:** Heated 50–120°C; glass, PEI, or spring steel surfaces
- **Motion system:** Cartesian (X, Y gantry + Z bed) or CoreXY (fast, high-quality)
- **Part cooling fan:** Critical for bridging and overhangs — too little and prints droop; too much and layer adhesion suffers

### 1.2 FDM Materials Reference

| Material | Nozzle °C | Bed °C | Enclosure? | Key properties |
|---------|----------|--------|-----------|----------------|
| PLA | 195–220 | 55–65 | No | Easy, brittle, not UV stable, T_max ~55°C |
| PETG | 230–250 | 70–85 | Recommended | Tougher than PLA, slight flex, food-safe options |
| ASA | 240–260 | 90–110 | Yes | UV stable, outdoor electronics, ABS-like ease |
| ABS | 230–250 | 95–110 | Yes | Acetone smooth, strong, warps without enclosure |
| TPU (95A) | 220–240 | 40–60 | No | Flexible, excellent wear/impact resistance |
| Nylon (PA12) | 250–270 | 70–90 | Yes | Best fatigue resistance, hygroscopic (dry before use!) |
| PC | 260–300 | 100–120 | Yes | Very tough, heat resistant to 110°C |
| PEEK | 360–400 | 110–120 | Yes | Medical/aerospace grade, requires all-metal hotend |

### 1.3 FDM Process Parameters

**Layer height:**
- Draft / coarse: 0.3mm (4× speed of fine, visible lines)
- Standard: 0.2mm (balanced speed/quality)
- Fine: 0.1mm (smooth surfaces, slow)
- Ultra: 0.05mm (resin-like quality, very slow, tolerance sensitive)

**Rule:** Layer height must be ≤ 75% of nozzle diameter. With 0.4mm nozzle: max layer = 0.3mm.

**Infill patterns and uses:**
| Pattern | Best use | Structural efficiency |
|---------|---------|----------------------|
| Grid | General purpose | Medium |
| Gyroid | Flexible parts, isotropy | High (all directions) |
| Honeycomb | Lightweight structures | High (in-plane) |
| Lightning | Cosmetic/display parts | Low (just enough) |
| Cubic (3D) | High-stress solid parts | Very high |

**Infill percentage:**
- 5–15%: Cosmetic, display only
- 20–40%: General functional parts
- 50–80%: High-load, structural
- 100%: Maximum strength, dense, slow; only for small critical features

**Wall count (perimeters):**
- 2 walls: Decorative
- 3–4 walls: Standard functional
- 5+ walls: High-stress structural (consider solid infill too)

---

## 📚 2. SLA/MSLA — Stereolithography

### 2.1 How SLA/MSLA Works

A UV light source (laser for SLA, LCD screen for MSLA/resin printers) cures photopolymer resin layer by layer. The build plate rises (bottom-up printers: FEP film + LCD from below; top-down: laser from above).

**Process characteristics:**
- **Layer height:** 0.025–0.1mm (much finer than FDM)
- **XY resolution:** 35–80 microns for consumer MSLA (depends on LCD pixel size)
- **Surface finish:** Ra 0.5–2.0 µm (excellent detail, smooth curves)
- **Build volume:** Smaller than FDM (typically 130×80×165mm for consumer)
- **Material:** Photopolymer resin — brittle unless "tough" or "ABS-like" formulations

### 2.2 Resin Post-Processing (Non-Negotiable)

1. **Rinse:** Submerge in IPA or Resin Wash for 2–5 minutes, agitate
2. **Air dry:** 10–15 minutes until no liquid resin on surface
3. **UV cure:** UV lamp 30–60 seconds each face (or dedicated cure station)
4. **Mechanical support removal:** Cutters/flush cutters for supports, light sanding

**Critical:** Uncured resin is toxic. Wear nitrile gloves, work in ventilated area.

### 2.3 When to Use SLA vs FDM

| Use SLA when | Use FDM when |
|-------------|-------------|
| Fine details (miniatures, jewelry, dental) | Large parts (bed size limited for SLA) |
| Smooth surfaces needed without post-processing | Tough functional parts (PETG/ASA/Nylon) |
| Miniature enclosures with text/logos | Flexible parts (TPU not available in resin) |
| Mould masters for silicone casting | Long prints overnight (resin more hands-on) |

---

## 📚 3. SLS — Selective Laser Sintering

### 3.1 Process

A CO₂ laser sinters (partially fuses) nylon powder (PA12, PA11, TPU) layer by layer. Unfused powder acts as self-supporting material — **no support structures required**.

**Key advantages over FDM:**
- No support structures → complex internal channels, interlocking parts, living hinges
- Isotropic mechanical properties (nearly)
- Wide range of PA formulations

**Typical applications:**
- Functional end-use parts in nylon
- Complex assemblies that would need supports in FDM
- Medical devices, prosthetics
- Short-run production (100s of units)

**Key limitation:** Surface finish is rougher than FDM (Ra 8–15 µm, sandblasting improves this). Cannot use non-sintered powder in other areas (dedicated powder handling system).

---

## 📚 4. DMLS/SLM — Metal Additive Manufacturing

### 4.1 Process Variants

| Name | Stands for | Key difference |
|------|-----------|---------------|
| DMLS | Direct Metal Laser Sintering | Partial melting of powder |
| SLM | Selective Laser Melting | Full melting of powder |
| EBM | Electron Beam Melting | In vacuum, Ti/Co-Cr |
| WAAM | Wire Arc Additive Manufacturing | MIG welding-based, large parts |

### 4.2 Metal AM Properties

- **Achievable materials:** 316L SS, 17-4 PH SS, Ti-6Al-4V, AlSi10Mg, Inconel 718, CoCr
- **As-built properties:** Often equal or superior to wrought for fatigue/tensile
- **Post-processing required:**
  - Support removal (supports machined or ground)
  - Stress relief heat treatment (mandatory for most alloys)
  - HIP (Hot Isostatic Pressing) for safety-critical parts (closes porosity)
  - CNC machining of critical surfaces (±0.1mm as-built → ±0.025mm after CNC)

---

## 📚 5. Print Failure Diagnosis & Fix

| Failure | Cause | Fix |
|---------|-------|-----|
| **Stringing** | Too hot, too fast travel, retraction low | Reduce temp by 5°C; increase retraction 0.5mm; enable Z-hop |
| **Layer separation** | Too cold, printing too fast, poor adhesion | Increase temp 5°C; reduce speed 20%; clean bed |
| **Elephant foot** | First layer squished too much | Increase nozzle height slightly; reduce first layer squish |
| **Warping** | Bed too cold, no adhesion, no enclosure | Increase bed temp; use glue stick; print with brim; add enclosure for ABS |
| **Under-extrusion** | Partial clog, low temp, high speed | Cold pull to clear; check PTFE tube; calibrate E-steps |
| **Over-extrusion** | E-steps too high, flow too high | Calibrate extruder; reduce flow in slicer to 95% |
| **Gaps in top layers** | Not enough top layers, infill too sparse | Add top layers (minimum 5 for 0.2mm); increase infill |
| **Blobbing / zits** | Pressure in nozzle at travel moves | Enable seam hiding; adjust pressure advance; reduce outer wall speed |

---

## 📚 6. Heat-Set Inserts — The Right Way to Add Threads

**Why:** FDM printed threads have very low shear strength. Pull-out force of M3 printed thread: ~50–100N. Heat-set insert: 500–1000N.

**Types:** M2, M3, M4, M5, M6 brass inserts (standard: Ruthex, CNC Kitchen design)

**Installation:**
1. Design hole in CAD: insert OD + 0.1–0.2mm (e.g. M3 insert Ø4.0mm → hole Ø4.2mm)
2. Print hole slightly undersized (FDM shrinks holes ~0.2mm → effective Ø4.0mm is about right)
3. Set soldering iron to 180–220°C
4. Place insert on hole, press straight down with iron tip inside insert
5. Press until flush with surface or slightly below
6. Let cool 30 seconds before threading

**Common mistake:** Pressing too fast → insert tilts. Go slow, apply light pressure, let heat soak.

---

## ⚠️ 7. Common Misconceptions

1. **"Higher infill = stronger part."** Above ~40% infill, the main strength gains come from wall count and top/bottom layers, not more infill. A 40% infill with 5 walls is stronger than 80% infill with 2 walls for most loading.

2. **"I can print threads for M3 bolts."** Don't. Heat-set inserts are the answer — see Section 6. Printed threads strip under surprisingly light torque.

3. **"Support material always goes where there's overhang."** Smart support placement avoids supports on vertical surfaces, inside bore holes, and cosmetic faces. Use tree supports or manually disable unnecessary support regions.

4. **"My SLA print is done when I take it off the plate."** No — uncured resin is tacky, dimensionally inaccurate (swollen by IPA), and toxic until post-cured under UV. Skip post-cure and your part will be soft, sticky, and off-dimension.

5. **"Nylon is the same as Nylon."** PA12 (SLS, standard FDM), PA6 (stronger, more moisture absorption), PA11 (flexible, bio-based), nylon-CF (carbon-reinforced, stiffer). Each behaves differently and requires specific storage/drying.

6. **"3D printed parts are dimensionally accurate out of the box."** FDM holes print ~0.2–0.3mm undersized. Outer dimensions are typically within 0.2–0.5mm. For fit-critical features, measure first print and adjust CAD dimensions accordingly.

---

## 🔗 8. Cross-links & Further Reading

### Internal
- [33.6 - Tolerancing, Fits & Assemblies](33.6---Tolerancing,-Fits-&-Assemblies) — tolerance compensation for 3D printed parts
- [33.3 - Manufacturing Processes & DFM](33.3---Manufacturing-Processes-&-DFM) — when to choose 3D printing vs other processes
- [33.8 - Mechatronics & CAD-to-Fabrication Pipeline](33.8---Mechatronics-&-CAD-to-Fabrication-Pipeline) — integrating printed parts into assemblies

### External
- [PrusaSlicer documentation](https://help.prusa3d.com/) — comprehensive slicer reference
- [CNC Kitchen YouTube](https://www.youtube.com/@CNCKitchen) — scientific 3D printing tests
- [3D Printing Nerd YouTube](https://www.youtube.com/@3DPrintingNerd) — material reviews
- [Teaching Tech calibration guide](https://teachingtechyt.github.io/calibration.html) — systematic printer calibration
- [Formlabs Guide to SLA Printing](https://formlabs.com/blog/ultimate-guide-to-stereolithography-sla-3d-printing/) — SLA deep dive

---

*Prev: [33.4 - CNC Machining & G-Code](33.4---CNC-Machining-&-G-Code) | Next: [33.6 - Tolerancing, Fits & Assemblies](33.6---Tolerancing,-Fits-&-Assemblies)*
