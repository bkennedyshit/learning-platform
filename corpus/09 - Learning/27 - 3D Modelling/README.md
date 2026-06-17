---
date: 2026-05-26
type: subject-readme
tags: [practice, refresher, drills, source-materials, study-aids, 3d-modelling, revit, blender, maya, fusion-360, solidworks]
title: "README — 27 - 3D Modelling"
---

# 27 - 3D Modelling — Subject Hub

> One-page subject hub. Lists chapters, source reading materials, **video / picture references stored outside the repo (linked by URL)**, and placeholders for generated study aids.
> Master practice guide: [[../HOW_TO_USE_PRACTICE|HOW_TO_USE_PRACTICE]].

> **Asset storage convention.**
> - **SVG diagrams** (small, theme-responsive, in-vault) → `../_svgs/3dmod__<chapter>-fig<n>.svg` and embedded inline via `![[3dmod__20.x-figN.svg]]`.
> - **Pictures, screenshots, videos, course recordings** are NOT committed to this repo. They live on YouTube, Autodesk University, official docs, or in your local "C:/Obsidian Vault/Bill's Vault/_assets/" sidecar (gitignored). Reference them by **URL** in this README and in chapter notes.

---

## 🚀 Quick start

From a terminal in this folder:

```bash
cd "C:/Obsidian Vault/Bill's Vault/05-Knowledge_Foundation/09 - Learning/27 - 3D Modelling"
# (Drill scripts to be added — Dynamo Python, Blender bpy, USD validation)
python "_practice/scripts/<chapter>_<topic>.py" --count 8 --seed 42
```

---

## 📜 Chapter index

- [[27.1 - 3D Modelling Foundations & Coordinate Systems]]
- [[27.2 - Autodesk Revit Fundamentals]]
- [[27.3 - Advanced Revit - Families, Adaptive Components & Dynamo]]
- [[27.4 - Autodesk Fusion 360 - Parametric Modelling & CAM]]
- [[27.5 - Maya & 3ds Max - DCC, Animation & Arch-Viz Rendering]]
- [[27.6 - Blender - Open-Source Modelling, Geometry Nodes & Sculpting]]
- [[27.7 - SolidWorks - Mechanical CAD, Assemblies & Simulation]]
- [[27.8 - Pipelines, Interop & Productization - From Architecture to Business]]

---

## 🎬 Video & Picture References (external — open in browser)

> These are the open-source / pro-grade media that supplement the chapter notes. Pictures and videos are **not** stored in this repo; they live on YouTube, official docs, GitHub, etc.

### 📺 Video Channels & Playlists

| Channel / Course | Track Use | Link |
|---|---|---|
| **Autodesk University (free recordings)** | Revit advanced, Dynamo, BIM | [autodesk.com/autodesk-university](https://www.autodesk.com/autodesk-university) |
| **BIM Pure Productions** | Practical Revit families & Dynamo | [@BIMPure](https://www.youtube.com/@BIMPure) |
| **Aussie BIM Guru** | Advanced Revit, Dynamo, Forge | [@AussieBIMGuru](https://www.youtube.com/@AussieBIMGuru) |
| **Blender Guru — Donut 4.x** | Blender from zero | [@blenderguru](https://www.youtube.com/@blenderguru) |
| **CG Cookie — Blender Fundamentals** | Free Blender curriculum | [cgcookie.com](https://cgcookie.com/) |
| **CG Cookie — ASSEMBLE (Geometry Nodes)** | Procedural modelling with Geometry Nodes | [cgcookie.com/courses/assemble](https://cgcookie.com/courses/assemble-introduction-to-procedural-modeling-with-geometry-nodes-in-blender) |
| **Maya Learning Channel** | Maya official tutorials | [@MayaHowTos](https://www.youtube.com/@MayaHowTos) |
| **3ds Max Learning Channel** | 3ds Max + V-Ray + arch-viz | [@3dsMaxHowTos](https://www.youtube.com/@3dsMaxHowTos) |
| **MySolidWorks Training (free)** | SolidWorks fundamentals | [my.solidworks.com/training](https://my.solidworks.com/training) |
| **GoEngineer YouTube** | SolidWorks tips & advanced | [@GoEngineer](https://www.youtube.com/@GoEngineer) |
| **Fusion 360 Learning Hub** | Fusion 360 free path | [autodesk.com/fusion-360/learn](https://www.autodesk.com/products/fusion-360/learn) |
| **Speckle tutorials** | Revit ↔ Blender data round-trip | [speckle.systems/tutorials](https://speckle.systems/tutorials) |

### 🖼️ Picture / Diagram Reference Sources

| Source | What it gives you | Link |
|---|---|---|
| **Blender 4.4 Manual (figures)** | Blender UI, geometry node graphs, render examples | [docs.blender.org/manual](https://docs.blender.org/manual/en/latest/) |
| **OpenUSD docs** | USD composition / stage diagrams | [openusd.org](https://openusd.org/release/) |
| **buildingSMART IFC docs** | IFC class diagrams, schema visuals | [ifc43-docs.standards.buildingsmart.org](https://ifc43-docs.standards.buildingsmart.org/) |
| **Khronos glTF spec figures** | glTF binary layout, PBR pipeline | [github.com/KhronosGroup/glTF](https://github.com/KhronosGroup/glTF) |
| **Speckle architecture diagrams** | AEC data flow, connector topology | [docs.speckle.systems](https://docs.speckle.systems/) |
| **Pixar USD whitepaper figures** | Asset structure, layer composition | [openusd.org/release/intro.html](https://openusd.org/release/intro.html) |

### 📚 Open-Source / Free Books

| Title | Author / Provider | Link |
|---|---|---|
| Blender 4.4 Reference Manual | Blender Foundation | [docs.blender.org/manual](https://docs.blender.org/manual/en/latest/) |
| Geometry Nodes from Scratch | Simon Thommes (Blender Studio) | [studio.blender.org](https://studio.blender.org/training/geometry-nodes-from-scratch/) |
| Real-Time Rendering, 4th ed. (free chapters) | Akenine-Möller, Haines, Hoffman, et al. | [realtimerendering.com](https://www.realtimerendering.com/) |
| The Architecture of Open Source Applications — Blender | aosabook.org | [aosabook.org](https://aosabook.org/en/) |
| OpenUSD Tutorials (Pixar) | Pixar | [openusd.org/release/tut_usd_tutorials.html](https://openusd.org/release/tut_usd_tutorials.html) |
| Khronos glTF 2.0 Specification | Khronos Group | [github.com/KhronosGroup/glTF](https://github.com/KhronosGroup/glTF) |
| buildingSMART IFC 4.3 Documentation | buildingSMART International | [ifc43-docs.standards.buildingsmart.org](https://ifc43-docs.standards.buildingsmart.org/) |
| Mastering Autodesk Revit (companion site) | Sybex / Eric Wing | publisher site (paid book — many chapter previews free) |

---

## 🧰 Generated study aids

### 🎙️ Audio overviews & podcasts (NotebookLM)
- [ ] TODO: paste the NotebookLM "Audio Overview" link

### 🧠 Mind maps
- [ ] TODO: NotebookLM mind-map URL or screenshot

### ❓ Quizzes
- [ ] TODO: NotebookLM-generated quiz

### 📊 Reports & summaries
- [ ] TODO: NotebookLM "Briefing Doc" or "Study Guide"

### 🃏 Flash cards
- [ ] TODO: deck export (Anki, Obsidian SR)

### 🎬 Video overviews
- [ ] TODO: YouTube / Loom personal recording of your own modelling reels

### 📋 Data tables
- [ ] TODO: comparison matrix (Revit vs Fusion vs Maya vs Blender vs SolidWorks features)

---

## 🔗 Cross-links

- Syllabus & curriculum mindmap: [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/27 - 3D Modelling/Subject_Plan]]
- Visual roadmap: [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/27 - 3D Modelling/LEARNING_PATH]]
- Foundational VR/3D engineering math: [[../28 - VR & 3D Engineering/Subject_Plan]]
- Downstream applied VR: [[../29 - VR/Subject_Plan]]
- Robotics URDF / mech-CAD ties: [[../32 - Robotics/Subject_Plan]]
- Holographic asset workflow: [[../31 - Holographics/Subject_Plan]]
- Master Learning index: [[00 - 09 - Learning Index]]
- Master practice guide: [[../HOW_TO_USE_PRACTICE]]
