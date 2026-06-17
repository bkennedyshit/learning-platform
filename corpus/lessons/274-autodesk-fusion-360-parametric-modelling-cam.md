---
title: "27.4 — Autodesk Fusion 360: Parametric Modelling & CAM"
subject: "3D Modelling"
catalog: advanced
audience_tier: higher-education
chapter: "27.4"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 27.4 — Autodesk Fusion 360: Parametric Modelling & CAM

> *"Fusion 360 is the maker's Swiss Army Knife of 2026 — CAD + CAM + CAE + PCB in one tool, with cloud sync."*
> — paraphrased from [CAD Software Hub 2026 buyer's guide](https://www.cadsoftwarehub.com/blog/the-best-3d-cad-software-of-2026-free-paid/) (rephrased for compliance)

Fusion replaces architecture's Revit-style "draw a wall" intuition with a **timeline of features** — sketch, extrude, fillet, hole, pattern. This is the core of mechanical-engineering CAD and the dialect every other parametric tool (SolidWorks, Inventor, Onshape, FreeCAD) speaks.

---

## 🎯 Learning Objectives

1. Read and edit a Fusion **timeline** (the parametric feature history).
2. Author a parametric part: **sketch → constraint → extrude → fillet → hole → pattern**.
3. Build a multi-component assembly with **joints** (rigid, revolute, slider, pin-slot, planar, cylindrical, ball).
4. Use **parameters & equations** to drive design intent (one variable changes 30 dimensions).
5. Run a basic **simulation** (static stress) and a **CAM toolpath** (2D pocket, 3D adaptive clearing).
6. Round-trip Fusion ↔ SolidWorks / Inventor / STEP / IGES for cross-tool collaboration.

---

## 🖼️ Visual Anchor

![3dmod__20.3-fig1](3dmod__20.3-fig1.svg)

> *Picture / video reference (external):*
> - 📺 [Fusion 360 Learning Hub (Autodesk official)](https://www.autodesk.com/products/fusion-360/learn)
> - 📺 [Fusion 360 Tutorials — Lars Christensen on YouTube](https://www.youtube.com/@LarsChristensen)
> - 📺 [Product Design Online — Fusion 360 for Beginners](https://www.youtube.com/@ProductDesignOnline)
> - 📖 [SolidWorks vs Fusion 360 — which fits your workflow (2026)](https://gaugehow.com/cad/solidworks-vs-fusion-360)

---

## 📚 1. The Mental Model — Timeline-Based Parametric CAD

```
Sketch → Feature → Feature → Feature → ... → Body
   ↓        ↓
constraints  parameters
```

- Every operation appends to the **timeline** at the bottom.
- Click any node to **roll back** and edit — downstream features re-evaluate.
- This is *fundamentally different* from Revit's database-of-elements model.

### Sketching discipline
1. Pick a plane (origin XY/XZ/YZ or a face).
2. Draw with **constraints** first, **dimensions** last.
3. Goal: a fully-defined sketch (everything black) — under-defined sketches are how parametric drift starts.

### Common feature types
- Extrude / Revolve / Sweep / Loft
- Hole (with thread spec)
- Fillet / Chamfer
- Shell (hollow out a solid)
- Pattern (rectangular, circular, path)
- Boolean (combine: join / cut / intersect)

---

## 🔧 2. Parameters & Equations

```
Width      = 100 mm
Height     = Width / 2
Hole_Spacing = Width / 4
PinRadius  = if(Width > 80 mm; 5 mm; 3 mm)
```

The **Parameters dialog** is the equivalent of Revit's "Family Parameters" — it's where the design intent lives. A well-parameterized part adapts to any size class.

---

## 🔗 3. Assemblies & Joints

Fusion uses **components** (top-level "things") containing **bodies** (geometry). Joints connect components:

| Joint type | Degrees of freedom | Example |
|---|---|---|
| Rigid | 0 | Welded bracket |
| Revolute | 1 (rotation) | Door hinge |
| Slider | 1 (translation) | Drawer rail |
| Cylindrical | 2 | Piston in cylinder |
| Pin-slot | 2 | Cam follower |
| Planar | 3 | Object on a table |
| Ball | 3 (rotation) | Ball joint |

**As-built** (joint origin from chosen face/edge) is almost always what you want.

---

## ⚙️ 4. CAM, CAE, PCB — the Integrated Workspaces

| Workspace | What it does | When you use it |
|---|---|---|
| **DESIGN** | Parametric CAD | Always |
| **GENERATIVE DESIGN** | Cloud topology optimization | Lightweight brackets etc. |
| **RENDER** | Photoreal product viz | Marketing |
| **ANIMATION** | Exploded views, mechanism playback | Documentation |
| **SIMULATION** | FEA: static stress, modal, thermal | Validation |
| **MANUFACTURE (CAM)** | 2/3-axis mill, lathe, additive | Toolpath generation |
| **DRAWING** | 2D drawing creation | Shop drawings |
| **PCB** | Electronics, schematic + layout | Embedded products |

The integration is the killer feature: change a CAD dimension and the toolpath updates automatically.

---

## 🛠️ 5. Worked Example (skeleton) — A Parametric Mounting Bracket

1. New component "Bracket".
2. Sketch on XY plane: rectangle 100×60 with 4 corner holes.
3. Extrude 5 mm.
4. Add fillets 3 mm on outer edges.
5. Promote `width=100`, `depth=60`, `thickness=5`, `hole_d=4` to user parameters.
6. Pattern the holes by `width/4` spacing.
7. Static stress simulation with a 100 N load on one edge, fixed constraint on holes.
8. Generate a 2D drawing (top view + iso) for shop.
9. Export STEP for SolidWorks colleagues; export STL for 3D print.

---

## 🔗 6. Cross-links & Further Reading

### Internal
- [27.1 - 3D Modelling Foundations & Coordinate Systems](27.1---3D-Modelling-Foundations-&-Coordinate-Systems) — B-rep representation
- [27.7 - SolidWorks - Mechanical CAD, Assemblies & Simulation](27.7---SolidWorks---Mechanical-CAD,-Assemblies-&-Simulation) — the engineering-grade sibling
- [27.8 - Pipelines, Interop & Productization - From Architecture to Business](27.8---Pipelines,-Interop-&-Productization---From-Architecture-to-Business) — STEP/IGES exchange
- [22.4 - Actuators & Motor Control](22.4---Actuators-&-Motor-Control) — designing mechanical parts for robots in Fusion

### External
- [Fusion 360 Learning Hub](https://www.autodesk.com/products/fusion-360/learn)
- [Fusion 360 Personal Use comparison](https://www.autodesk.com/products/fusion-360/personal)
- [SolidWorks vs Fusion 360 — sourceCAD comparison](https://sourcecad.com/solidworks-vs-fusion-360-which-one-should-you-learn/)
- [CAD Software Hub — Best 3D CAD software of 2026](https://www.cadsoftwarehub.com/blog/the-best-3d-cad-software-of-2026-free-paid/)

---

## ⚠️ 7. Common Misconceptions

- **"Fusion is just a smaller SolidWorks."** Fusion's cloud-first data model + integrated CAM/PCB are different design choices, not a subset.
- **"Direct modelling and parametric modelling are the same."** Direct mode bypasses the timeline. Useful for cleanup; dangerous for design intent.
- **"Joints in Fusion = mates in SolidWorks."** Similar concept, different mechanic. Joints in Fusion attach by snap-points; SolidWorks mates by face pairs.
- **"Generative Design = AI replacement for engineers."** It's a topology-optimization solver — powerful for brackets, useless for things needing aesthetic / manufacturing constraints not captured in load cases.
