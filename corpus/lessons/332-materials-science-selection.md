---
title: "33.2 — Materials Science & Selection"
subject: "Mechanical Engineering & Fabrication"
catalog: advanced
audience_tier: higher-education
chapter: "33.2"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 33.2 — Materials Science & Selection

> *"Good engineering is knowing what to leave out. Good materials selection is knowing what to stop adding."*

Materials selection is a design decision masquerading as a technical detail. Getting it wrong means parts that corrode, crack, deform, or fail prematurely. Getting it right — choosing exactly the properties you need at the minimum weight, cost, and complexity — is one of the highest-leverage decisions in a design.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Describe the four crystal structures (BCC, FCC, HCP, amorphous) and link each to ductility/hardness.
2. Apply the **Hall-Petch relation** to predict strength change with grain size.
3. Use an **Ashby chart** (strength vs density) to identify candidate materials for a given performance index.
4. Explain five heat treatment processes (annealing, quench & temper, precipitation hardening, case hardening, normalising).
5. Select appropriate materials for: robot structural frames, 3D printed enclosures, bearing seats, outdoor electronics, and high-temperature environments.
6. Read a material **datasheet** and extract yield strength, UTS, elongation, Young's modulus, and density.

---

## 🖼️ Visual Anchor

![mech__34.2-fig1](mech__34.2-fig1.svg)

---

## 📚 1. Atomic Structure & Crystal Lattices

The macroscopic properties of materials emerge from atomic arrangement. Engineering metals crystallise into one of three main structures:

### 1.1 Body-Centred Cubic (BCC)

- Atoms at 8 corners + 1 in centre of unit cell
- **Examples:** α-iron (room temperature), chromium, tungsten, molybdenum
- **Properties:** harder, stronger, magnetic (for iron), lower ductility than FCC
- **Slip systems:** 48 (complex slip — tougher at high rates)

### 1.2 Face-Centred Cubic (FCC)

- Atoms at 8 corners + 1 on each of 6 faces
- **Examples:** aluminium, copper, nickel, austenitic stainless steel (304/316), gold, silver
- **Properties:** highly ductile, good formability, non-magnetic (most FCC metals)
- **Slip systems:** 12 (easy slip — deforms smoothly)
- **Why Al is easy to machine:** FCC + no iron phase → chips cleanly without work hardening as badly as steel

### 1.3 Hexagonal Close-Packed (HCP)

- **Examples:** titanium (low temp), magnesium, zinc, cobalt
- **Properties:** limited ductility (fewer slip systems: 3–6), strong, lightweight
- **Titanium note:** above 882°C Ti transforms from HCP (α-Ti) to BCC (β-Ti). Ti-6Al-4V ("grade 5") is a two-phase α+β alloy.

### 1.4 Amorphous (Non-Crystalline)

- No long-range order — atoms arranged like a frozen liquid
- **Examples:** glass, most polymers, metallic glasses (Zr-based)
- **Properties:** isotropic, no grain boundaries → can be transparent, tailored properties

---

## 📚 2. Mechanical Properties — What to Look For on a Datasheet

| Property | Symbol | Units | What it measures |
|----------|--------|-------|-----------------|
| Young's modulus (stiffness) | E | GPa | Resistance to elastic deformation |
| Yield strength | σ_y | MPa | Stress at which plastic deformation starts |
| Ultimate tensile strength | UTS / σ_u | MPa | Maximum stress before fracture |
| Elongation at break | ε_f | % | Ductility — how much stretch before failure |
| Fracture toughness | K_IC | MPa√m | Resistance to crack propagation |
| Hardness | HV, HRC, HRB | — | Resistance to surface indentation |
| Fatigue limit (S_e) | — | MPa | Stress below which fatigue failure won't occur (in some materials) |
| Density | ρ | g/cm³ or kg/m³ | Weight per volume |

### Reading a datasheet: Al 6061-T6 example

```
Young's modulus E:     68.9 GPa
Yield strength σ_y:    276 MPa
UTS σ_u:               310 MPa
Elongation:            12–17%
Density ρ:             2.70 g/cm³
Hardness:              95 HB
Machinability:         Excellent
Weldability:           Good (but strength decreases in HAZ)
Anodising:             Excellent
```

**Specific strength** = σ_y / ρ = 276/2.70 = 102 MPa/(g/cm³) — aluminium's key advantage over steel for weight-critical parts.

---

## 📚 3. The Hall-Petch Relation

Grain boundaries act as barriers to dislocation motion (slip). More boundaries → harder to deform → higher yield strength.

**Hall-Petch equation:**
$$\sigma_y = \sigma_0 + k_y \cdot d^{-1/2}$$

Where:
- σ_y = yield strength
- σ_0 = friction stress (lattice resistance to dislocation motion)
- k_y = strengthening coefficient (material-dependent)
- d = average grain diameter

**Implication:** Fine-grained microstructure → higher strength. Achieved by:
- Rapid cooling (quenching)
- Cold working (deforms grains, creates dislocations)
- Microalloying (grain growth inhibitors, e.g. Ti, V in HSLA steel)

**Limit:** Below about 10–20nm grain size, Hall-Petch inverts (inverse Hall-Petch). Dislocations can no longer pile up — different deformation mechanism takes over.

---

## 📚 4. Heat Treatment

### 4.1 Annealing
- **Process:** Heat above recrystallisation temperature → hold → slow cool (furnace)
- **Result:** Coarse grains → soft, ductile, easy to machine/form
- **Use:** Before cold-forming operations; to relieve residual stress after welding

### 4.2 Quench & Temper (Steel)
- **Quench:** Heat above critical temperature (austenite phase) → rapid cool in water/oil/air → martensite forms (hard, brittle)
- **Temper:** Reheat to 150–650°C → hold → air cool → dissolves some martensite → reduces brittleness, improves toughness
- **Result:** High strength + acceptable toughness
- **Example:** 4140 steel — normalised: 415 MPa yield; Q&T at 540°C: 750 MPa yield

### 4.3 Precipitation Hardening (Age Hardening)
- Primarily aluminium alloys (2024, 6061, 7075) and some stainless steels (17-4 PH)
- **Process:** Solution treat → quench → age at elevated temperature
- **Result:** Fine precipitates pin dislocations → very high yield strength
- **7075-T6:** σ_y = 503 MPa, ρ = 2.81 g/cm³ → specific strength 179 MPa/(g/cm³)
- **Why "T6"?** T = thermally treated; 6 = solution heat treat + artificial age

### 4.4 Case Hardening (Carburising/Nitriding)
- Hard outer shell, tough inner core
- **Carburising:** Heat steel in carbon-rich atmosphere → diffuse C into surface → quench
- **Nitriding:** Ammonia atmosphere, lower temp — no quench needed
- **Use:** Gear teeth, bearing races, cam lobes — high surface hardness + fatigue resistance

### 4.5 Normalising
- Heat above critical temp → air cool (faster than annealing, slower than quench)
- **Result:** Fine pearlite microstructure — moderate strength, better than annealed
- **Use:** Structural steel, after casting, before machining

---

## 📚 5. Ashby Material Selection Charts

The Ashby methodology (developed at Cambridge, now CES EduPack) uses log-log charts to identify optimal materials for specific design objectives.

### 5.1 Performance Index

For a given function + constraint + objective, derive a **material index** M. The slope of index lines on the Ashby chart identifies the optimal material class.

**Common indices:**

| Function | Objective | Constraint | Index |
|---------|----------|-----------|-------|
| Tie (tensile) | Min weight | Fixed stiffness | E/ρ |
| Beam (bending) | Min weight | Fixed stiffness | E^(1/2)/ρ |
| Beam (bending) | Min weight | Fixed strength | σ_y^(2/3)/ρ |
| Panel (buckling) | Min weight | Fixed load | E^(1/3)/ρ |
| Shaft (torsion) | Min weight | Fixed strength | σ_y^(2/3)/ρ |
| Any | Max temp limit | Fixed structure | T_max |

### 5.2 Reading the Strength-Density Chart

On an Ashby chart with log(σ_y) vs log(ρ):
- Diagonal lines of slope 1 = constant specific strength (σ_y/ρ)
- Materials above a given line are better for specific strength
- Best performers: CFRP, Ti alloys, high-strength Al alloys, spring steels
- Worst: lead, gold (dense, not strong)

---

## 📚 6. Engineering Materials — Reference Tables

### 6.1 Aluminium Alloys (most useful for makers)

| Alloy | Condition | σ_y (MPa) | σ_u (MPa) | Density | Notes |
|-------|-----------|----------|----------|---------|-------|
| 6061 | T6 | 276 | 310 | 2.70 | General purpose, weldable, good anodising |
| 7075 | T6 | 503 | 572 | 2.81 | Highest strength Al, poor weldability |
| 5052 | H32 | 193 | 228 | 2.68 | Sheet metal, weldable, marine use |
| 2024 | T3 | 345 | 483 | 2.78 | Aerospace structural, poor weld |
| 6063 | T5 | 145 | 186 | 2.70 | Extrusions, anodising (T-slot profiles) |

### 6.2 Stainless Steels

| Grade | Type | σ_y (MPa) | Notes |
|-------|------|----------|-------|
| 304 | Austenitic | 215 | Most common, non-magnetic, weldable |
| 316 | Austenitic | 205 | Marine/food grade, better corrosion resistance |
| 17-4 PH | Precip hardening | 1100+ | High strength SS, H900 condition |
| 440C | Martensitic | 620 | Hardened: high hardness (HRC 60), bearing quality |

### 6.3 Engineering Plastics (for 3D printing and injection moulding)

| Material | σ_y (MPa) | T_max (°C) | FDM? | Notes |
|---------|----------|-----------|------|-------|
| PLA | 50–60 | 55–60 | ✅ | Brittle, not outdoor. Great for prototypes |
| PETG | 45–55 | 70–80 | ✅ | Good for enclosures, food-safe possible |
| ASA | 40–50 | 90–100 | ✅ | UV stable, outdoor electronics |
| ABS | 40 | 80–100 | ✅ (hard) | Acetone smooth, shrinks — warping |
| Nylon (PA12) | 55 | 120 | ✅ (hard) | Excellent fatigue, hygroscopic |
| PEEK | 100 | 250 | ⚠️ | Needs 350°C nozzle, high-performance |

---

## 🛠️ 7. Worked Example — Robot Arm Link Material Selection

**Problem:** Design a 200mm link for a 6-DOF robot arm. Requirements:
- Carry 5N at end (with arm horizontal) → σ_bending ≈ 20 MPa at root
- Minimum weight (battery-powered robot)
- Machinable or 3D printable (prototype phase)
- Budget: make 3 prototypes

**Apply Ashby methodology:**
1. **Function:** beam in bending
2. **Objective:** minimum mass
3. **Index:** σ_y^(2/3) / ρ (strength-limited beam)
4. **Screening constraints:** available material, ≥ 30 MPa yield, machinable or printable

**Candidates ranked by σ_y^(2/3)/ρ:**
- CFRP: ~150 — winner but cost/fabrication complexity too high for prototypes
- Al 7075-T6: 503^(2/3)/2.81 = 62.6 — excellent
- Al 6061-T6: 276^(2/3)/2.70 = 43.6 — good and cheap
- PETG print: 55^(2/3)/1.27 = 22.0 — acceptable for prototype at low load
- Mild steel: 250^(2/3)/7.85 = 8.0 — worst specific strength

**Decision:** 
- Iteration 1: PETG printed (hours, ≈$2 material)
- Iteration 2: Al 6061-T6 CNC machined (validate geometry, ~$50 stock + machining)
- Final: Al 7075-T6 if fatigue loading or weight critical

---

## ⚠️ 8. Common Misconceptions

1. **"Steel is stronger than aluminium."** By yield strength per unit volume, yes. Per unit mass, aluminium alloys (6061, 7075) have comparable or higher specific strength to many structural steels.

2. **"T6 means tempered."** No — T6 is an aluminium temper designation: solution heat treated + artificially aged. Tempering is a steel term.

3. **"I can weld 7075."** 7075 is generally considered non-weldable due to hot cracking and severe HAZ strength loss. 6061 is weldable but loses ~40% yield strength in the heat-affected zone. Design joints away from high-stress areas.

4. **"3D printed nylon is as strong as machined nylon."** FDM nylon is anisotropic — typically 30–50% weaker in the Z (layer) direction vs injection-moulded. Design part orientation so load is parallel to layer lines.

5. **"Hardness = toughness."** Completely opposite. Higher hardness (e.g. hardened 440C steel) = more brittle. Toughness (area under the stress-strain curve) requires both strength AND ductility. A hard but brittle part fails catastrophically without warning.

6. **"PETG is safe for outdoor electronics."** PETG has limited UV resistance (yellows, becomes brittle over years). Use ASA or UV-stable PETG formulations for long-term outdoor use.

---

## 🔗 9. Cross-links & Further Reading

### Internal
- [33.3 - Manufacturing Processes & DFM](33.3---Manufacturing-Processes-&-DFM) — what processes work for each material
- [33.5 - 3D Printing & Additive Manufacturing](33.5---3D-Printing-&-Additive-Manufacturing) — polymer material properties in depth
- [33.6 - Tolerancing, Fits & Assemblies](33.6---Tolerancing,-Fits-&-Assemblies) — material affects thermal expansion and fit performance

### External
- [CES EduPack (free student edition)](https://www.grantadesign.com/education/ces-edupack/) — Ashby charts software
- [MatWeb — free material properties database](https://www.matweb.com/)
- [ASM Handbook (library access)](https://www.asminternational.org/asm-international/asmi-online)
- [MIT OCW 3.091 Solid-State Chemistry](https://ocw.mit.edu/courses/3-091sc-introduction-to-solid-state-chemistry-fall-2010/) — crystal structure and bonding
- [Ashby "Materials: Engineering, Science, Processing and Design" — textbook](https://www.elsevier.com/books/materials/ashby/978-0-08-102376-1)

---

*Prev: [33.1 - Engineering Drawing & GD&T](33.1---Engineering-Drawing-&-GD&T) | Next: [33.3 - Manufacturing Processes & DFM](33.3---Manufacturing-Processes-&-DFM)*
