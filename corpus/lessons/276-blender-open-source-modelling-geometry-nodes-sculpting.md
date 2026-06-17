---
title: "27.6 — Blender: Open-Source Modelling, Geometry Nodes & Sculpting"
subject: "3D Modelling"
catalog: advanced
audience_tier: higher-education
chapter: "27.6"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 27.6 — Blender: Open-Source Modelling, Geometry Nodes & Sculpting

> *Blender 4.x has crossed a threshold: it is no longer the "free alternative" — it is the production tool of choice for an increasing number of studios, and Geometry Nodes have made procedural workflows accessible without a Houdini license.*

This chapter focuses on the Blender 4.4 skill set most useful to a Revit-trained architect: modelling polish, arch-viz rendering with Cycles, and procedural environments / facade systems via Geometry Nodes.

---

## 🎯 Learning Objectives

1. Navigate Blender 4.4: viewport, outliner, properties, modifier stack, shader editor, geometry node editor.
2. Model a hero asset using Blender's modelling tools (extrude, bevel, loop cut, knife, subdivision surface).
3. Sculpt + retopologize a high-poly to a clean low-poly mesh.
4. Build a **shader graph** in the Shading workspace (Principled BSDF + textures + procedural noise).
5. Render with **Cycles** (path-traced) and **EEVEE Next** (real-time).
6. Author a **Geometry Nodes** graph that procedurally generates a building facade or scatter system.
7. Script a Geometry Nodes graph from **Python (`bpy`)** for repeatable studio tooling.

---

## 🖼️ Visual Anchor

![3dmod__20.4-fig1](3dmod__20.4-fig1.svg)

> *Picture / video reference (external):*
> - 📺 [Blender 4.4 Manual](https://docs.blender.org/manual/en/latest/) — definitive reference
> - 📺 [Geometry Nodes from Scratch (Blender Studio, Simon Thommes)](https://studio.blender.org/training/geometry-nodes-from-scratch/)
> - 📺 [Blender Guru — Donut Tutorial 4.x](https://www.youtube.com/@blenderguru)
> - 📺 [CG Cookie — ASSEMBLE: Procedural Modeling with Geometry Nodes](https://cgcookie.com/courses/assemble-introduction-to-procedural-modeling-with-geometry-nodes-in-blender)
> - 📖 [Geo Nodes Guide (community)](https://geonodesguide.com/)
> - 📖 [Beginner's Guide to Geometry Nodes in Blender 2026 (cg-wire)](https://blog.cg-wire.com/blender-scripting-geometry-nodes/)

---

## 📚 1. The Blender Mental Model

Blender's "everything is a node graph" approach is its strength once you adapt:

- **Outliner** — scene graph (collections, objects).
- **Properties panel** — per-object settings (modifiers, constraints, materials).
- **Modifier stack** — non-destructive operations on geometry.
- **Shader editor** — material node graph.
- **Geometry Nodes editor** — procedural geometry node graph.
- **Compositor** — post-process node graph.

Render engines:
- **Cycles** — path-traced, photoreal, GPU-accelerated.
- **EEVEE Next** — real-time rasterizer with screen-space effects (Blender 4.x).
- **Hydra delegate** — render via OpenUSD-compatible renderer (e.g., Karma, Storm).

---

## 🪨 2. Sculpting + Retopology Loop

1. **Sculpt** in Dyntopo / Multires for hi-detail organic forms.
2. Use **VDB Remesh** (Volume → Mesh) to get a uniform grid.
3. **Retopologize** with Quad Remesher (built-in QuadriFlow, or paid plugin) → clean low-poly.
4. Bake **normal / AO / curvature** maps from hi → low.
5. Texture the low-poly via the Shading workspace.

---

## 🎨 3. Shaders — Principled BSDF Cheat Sheet

| Input | Use |
|---|---|
| Base Color | Diffuse texture |
| Metallic | 0 (dielectric) or 1 (metal) — never in between |
| Roughness | 0 (mirror) → 1 (matte) |
| Normal | Connect Normal Map node |
| Subsurface | For skin, wax, marble |
| Transmission | For glass / water (Roughness controls frosted-ness) |
| Emission | For lightbulbs, screens |

For arch-viz, layer textures via **Mix Shader** or **Color → Mapping → Image Texture** chains. Use **UV-driven** textures for buildings, **Object/Generated** coordinates for procedural rocks/foliage.

---

## 🌐 4. Geometry Nodes — Procedural Architecture

Geometry Nodes is a node-based programming language for geometry. Inputs come in, geometry comes out.

```
[Input: Curve (the building footprint)]
  ↓
[Curve to Mesh]  ←  [Profile: rectangle 300×100 mm]
  ↓
[Extrude Mesh]  (height = building_levels × 3.5 m)
  ↓
[Distribute Points on Faces]  → [Instance on Points: window_panel]
  ↓
[Output Geometry]
```

Common patterns:
- **Scatter** (rocks/trees on terrain).
- **Modular building** (parts assembled by rules).
- **Curtain wall generator** (panel, mullion, transom).
- **Foliage system** (procedural growth).

### 4.1 Scripting Geometry Nodes from Python (`bpy`)

```python
import bpy

# Get or create a Geometry Nodes group
mod = obj.modifiers.new("GN", "NODES")
ng = bpy.data.node_groups.new("MyTree", "GeometryNodeTree")
mod.node_group = ng

# Add nodes
n_in  = ng.nodes.new("NodeGroupInput")
n_out = ng.nodes.new("NodeGroupOutput")
n_cube = ng.nodes.new("GeometryNodeMeshCube")

# Wire them
ng.links.new(n_cube.outputs["Mesh"], n_out.inputs[0])
```

Reference: [How to Script Geometry Nodes in Blender with Python (2026, cg-wire)](https://blog.cg-wire.com/blender-scripting-geometry-nodes-2/) — content rephrased for compliance.

---

## 🏛️ 5. Arch-Viz Pipeline in Blender

1. Import IFC via **BlenderBIM** add-in (open-source) or USD/Speckle.
2. Re-light with HDRI dome + sun.
3. Material override → Cycles principled.
4. Render with Cycles GPU; denoise via OptiX/OIDN.
5. Export glTF/USD for Unity/Unreal or Vision Pro / Quest 3.

---

## 🛠️ 6. Worked Example (skeleton) — Procedural Façade

1. Curve = building footprint.
2. Geometry Nodes graph generates floor levels (extruded curve).
3. On each floor, scatter a window-panel instance every X mm.
4. Driver: a global `floor_count` parameter changes building height live.
5. Bake when finalized; export to glTF.

---

## 🔗 7. Cross-links & Further Reading

### Internal
- [27.5 - Maya & 3ds Max - DCC, Animation & Arch-Viz Rendering](27.5---Maya-&-3ds-Max---DCC,-Animation-&-Arch-Viz-Rendering) — paid DCC siblings
- [27.8 - Pipelines, Interop & Productization - From Architecture to Business](27.8---Pipelines,-Interop-&-Productization---From-Architecture-to-Business) — selling Blender add-ons / asset packs
- [08.6 - The Standard Library & Ecosystem Tour](08.6---The-Standard-Library-&-Ecosystem-Tour) — Python skills you'll need for `bpy`

### External
- [Blender 4.4 Manual](https://docs.blender.org/manual/en/latest/)
- [Blender Studio (free training)](https://studio.blender.org/training/)
- [Geometry Nodes from Scratch (Blender Studio)](https://studio.blender.org/training/geometry-nodes-from-scratch/)
- [BlenderBIM (open-source IFC support)](https://blenderbim.org/)
- [Speckle Blender Connector](https://www.speckle.systems/connectors/blender)

---

## ⚠️ 8. Common Misconceptions

- **"Blender's hotkeys are the worst."** They are dense but consistent. After ~30 hours they become muscle memory. Do not remap until then.
- **"Cycles is too slow."** With a modern GPU + OptiX denoiser + adaptive sampling, Cycles is competitive for arch-viz hero shots.
- **"Geometry Nodes is just modifiers with extra steps."** Modifiers are linear; Geometry Nodes is a programming language with attributes, fields, and selection logic.
- **"Blender can't do production."** It can — Spider-Man: Across the Spider-Verse, Wonder Woman, several Pixar shorts have used Blender. The bottleneck is studio inertia, not capability.
