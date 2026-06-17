---
title: "27.3 — Advanced Revit: Families, Adaptive Components & Dynamo"
subject: "3D Modelling"
catalog: advanced
audience_tier: higher-education
chapter: "27.3"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 27.3 — Advanced Revit: Families, Adaptive Components & Dynamo

> *"Most architects plateau at competent Revit modeler. The few who master adaptive components + Dynamo become the BIM coordinators, the computational designers, and the consultants — and the difference is usually about 60–80 hours of focused practice."*

---

## 🎯 Learning Objectives

1. Author a **parametric loadable family** with constraints, formula-driven parameters, type catalogs, and shared parameters.
2. Build **adaptive components** that conform to non-orthogonal hosts — curtain panels, freeform façades, structural truss generators.
3. Read a **Dynamo graph** fluently and write your own — including CPython 3 script nodes (Dynamo 3.5).
4. Apply Dynamo to four canonical workflows:
   - Bulk parameter editing
   - Linking Revit data to / from Excel
   - Driving geometry from external data (image maps, CSV, GIS)
   - Geometry-aware QA (clash, list-by-rule, tag-by-rule).
5. Decide when to drop Dynamo and write a **Revit add-in** in C# instead (or use the Revit API via PyRevit).

---

## 🖼️ Visual Anchor

![3dmod__20.2-fig1](3dmod__20.2-fig1.svg)

> *Picture / video reference (external):*
> - 📺 [Dynamo and Curtain Panels: A Wild Brick Pattern Workflow in Revit (AU class)](https://www.autodesk.com/autodesk-university/class/Dynamo-Curtain-Panels-Wild-Brick-Pattern-Workflow-Revit-2022)
> - 📺 [Conceptual Structural Design Using Revit Adaptive Components and Dynamo (AU class)](https://www.autodesk.com/autodesk-university/class/Conceptual-Structural-Design-Using-Revit-Adaptive-Components-and-Dynamo-2017)
> - 📺 [Make your Revit Families smart and adaptive (AU class)](https://www.autodesk.com/autodesk-university/zh-hans/forge-content/au_class-urn:adsk.content:content:6baa6b2f-3f3a-4b02-bde1-4be524b412ad)
> - 📺 [Aussie BIM Guru — Adaptive Components & Dynamo playlists](https://www.youtube.com/@AussieBIMGuru)

---

## 📚 1. Parametric Family Authoring — Beyond the Tutorial

### 1.1 Reference Planes vs Reference Lines
- **Reference Planes** = parametric scaffolding. Constrain geometry to them, never to raw geometry.
- **Reference Lines** = the same, but rotatable. Use for hinged / kinematic families (doors, articulated arms).

### 1.2 Parameter taxonomy

| Parameter Type | Where | Use case |
|---|---|---|
| **Family parameter** | Inside the family only | Internal driver |
| **Shared parameter** | Lives in shared-params .txt | Survives export, schedules, IFC |
| **Project parameter** | Project-wide, not in family | "Cost code" tags etc. |
| **Global parameter** | Project-level, drives multiple families | Building-wide drivers |

### 1.3 Formula-driven parameters

```
Width = if(Length > 3000 mm, 1200 mm, 900 mm)
Cost  = Width * Height * Material_Cost_per_m2
```

Formulas use Revit-flavoured expressions (case-sensitive parameter names, units must match).

### 1.4 Type Catalogs

A `.txt` sidecar to your `.rfa` that lets one family yield many types — instead of saving 50 size-variants, ship one family + one type catalog. Critical for manufacturer libraries.

---

## 🧩 2. Adaptive Components

Adaptive Components let you place a family by clicking N points; the family deforms to fit. Used for:

- **Curtain panel by pattern** — non-orthogonal façades.
- **Adaptive structural members** — trusses that span any 4-point boundary.
- **Site-conditional families** — railings on sloped paths, etc.

### Workflow
1. Family template: *Generic Model Adaptive*.
2. Place adaptive points (up to ~12 in practice).
3. Reference geometry to those points — usually via reference lines + hosted reference planes.
4. Save → load into a project → place by clicking the same N points on a divided surface, edge, or grid.

### Common pattern: divided surface façade
1. Conceptual mass with a curved surface.
2. Apply a **divided surface** (UV grid, possibly distorted by hosted points / attractors).
3. Load adaptive panel family → assign as the panel of the divided surface.
4. Drive panel parameters by attractor distance with **Dynamo**.

---

## 🧠 3. Dynamo 3.5 (with Revit 2026.1)

Dynamo is Revit's visual programming environment — the bridge between BIM data and arbitrary computation. With Revit 2026.1 it ships with **Dynamo 3.5**, which upgraded Python nodes to **CPython 3** (away from IronPython 2.7) — meaning you can finally use modern Python libraries.

> Source: [What's New in Revit 2026.1 — Dynamo 3.5 highlights](https://www.autodesk.com/blogs/aec/2025/05/22/whats-new-in-revit-2026-1/) — content rephrased for compliance.

### 3.1 Anatomy of a Dynamo graph

```
[Element.Selection] → [Element.Parameters] → [List.Filter] → [Element.SetParameter]
        ↓                                                         ↑
  Revit elements                                          Edited values
```

- **Nodes** = functions; **Wires** = data; **Lists** = the universal collection type.
- Yellow node = warning; Red = error. Read both; skipping warnings causes silent data loss.

### 3.2 Four canonical workflow patterns

1. **Bulk parameter edit**
   `All Elements of Category → SetParameterByName` — change 5,000 wall fire ratings in one click.
2. **Excel ↔ Revit round-trip**
   `Data.ImportExcel` / `Data.ExportExcel` — schedule data goes to client in Excel, comes back, gets re-applied.
3. **Geometry from external data**
   CSV → Points → Adaptive Component placement — façade driven by a gradient image, GIS data, energy analysis output.
4. **Rule-based QA**
   Walk the project, find every wall whose fire rating doesn't match its category → return a coloured 3D view + a CSV report.

### 3.3 CPython 3 script node

```python
# Inputs[0] is a list of Revit elements
# OUT must be assigned

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import BuiltInParameter

elements = IN[0]
out = []
for e in elements:
    p = e.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)
    out.append(p.AsString() if p else None)
OUT = out
```

---

## 🛠️ 4. When to Drop Dynamo and Write an Add-in

| Need | Tool |
|---|---|
| One-off task, < 30 elements | Just do it manually. |
| Repeating task on one project | Dynamo player + saved graph. |
| Repeating task across projects | Dynamo package. |
| Heavy logic, UI, large datasets | **Revit API in C#** (Visual Studio + Autodesk template) or **PyRevit** (Python add-in framework). |
| Distributed to multiple offices | C# add-in signed + installer. |

---

## 🔗 5. Cross-links & Further Reading

### Internal
- [27.2 - Autodesk Revit Fundamentals](27.2---Autodesk-Revit-Fundamentals) — fundamentals you need first
- [27.8 - Pipelines, Interop & Productization - From Architecture to Business](27.8---Pipelines,-Interop-&-Productization---From-Architecture-to-Business) — selling Dynamo packages and Revit add-ins
- [08.2 - Core Language - Syntax, Types, Control Flow & Functions](08.2---Core-Language---Syntax,-Types,-Control-Flow-&-Functions) — Python skills for Dynamo CPython
- [Subject_Plan](Subject_Plan) — C# foundations for the Revit API

### External
- [Aussie BIM Guru — Dynamo playlist](https://www.youtube.com/@AussieBIMGuru)
- [BIM Pure Productions](https://www.youtube.com/@BIMPure)
- [Autodesk University — Adaptive components + Dynamo classes](https://www.autodesk.com/autodesk-university)
- [Dynamo Forum (community)](https://forum.dynamobim.com/)
- [PyRevit](https://github.com/pyrevitlabs/pyRevit) — Python add-in framework for Revit
- [The Building Coder (Jeremy Tammik)](https://thebuildingcoder.typepad.com/) — canonical Revit API blog

---

## ⚠️ 6. Common Misconceptions

- **"Dynamo is slow on big models."** It is — for bulk operations on >10k elements use the Revit API via PyRevit or C#.
- **"Adaptive components fix all curved geometry problems."** They handle parameter-driven placement; for true freeform you still need Rhino.Inside.Revit or Speckle bridges.
- **"Type catalogs are for door manufacturers only."** Use them anywhere a family has many size variants — saves ~80% load times.
