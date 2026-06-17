---
date: 2026-05-24
type: subject-readme
tags: [practice, refresher, drills, source-materials, study-aids]
title: "README — 28 - VR & 3D Engineering"
---

# 28 - VR & 3D Engineering — Subject Hub

> One-page subject hub. Lists chapters, drill commands, source reading
> materials, and placeholders for generated study aids (NotebookLM artifacts:
> audio overviews, mind maps, quizzes, flash cards, etc.).
> Master practice guide: [[../HOW_TO_USE_PRACTICE|HOW_TO_USE_PRACTICE]].

---

## 🚀 Quick start

From a terminal in this folder:

```bash
cd "C:/Obsidian Vault/Bill's Vault/05-Knowledge_Foundation/09 - Learning/28 - VR & 3D Engineering"
python "_practice/scripts/<chapter>_<topic>.py" --count 8 --seed 42
```

Output lands at `_practice/<chapter>_drills.md`. Open in Obsidian Reading
view, do the problems on paper, click **Show solution** to verify.

---

## 📜 Chapter index

- [[28.1 - 3D Math Fundamentals]]
- [[28.2 - Quaternions & Rotations]]
- [[28.3 - Graphics Rendering Pipeline]]
- [[28.4 - Shader Programming - GLSL & HLSL]]
- [[28.5 - Game Engine Architectures - Unity & Unreal]]
- [[28.6 - AEC to VR Pipelines - BIM Data]]
- [[28.7 - Spatial Computing & Interaction Design]]

---

## 🎯 Drill scripts

| Script | Chapter | Sample command |
|---|---|---|
| 9.1_3d_math.py | [[28.1 - 3D Math Fundamentals]] | `python "_practice/scripts/9.1_3d_math.py" --count 8 --seed 42` |
| 9.2_quaternions.py | [[28.2 - Quaternions & Rotations]] | `python "_practice/scripts/9.2_quaternions.py" --count 8 --seed 42` |
| 9.3_pipeline.py | [[28.3 - Graphics Rendering Pipeline]] | `python "_practice/scripts/9.3_pipeline.py" --count 8 --seed 42` |
| 9.6_bim_to_vr.py | [[28.6 - AEC to VR Pipelines - BIM Data]] | `python "_practice/scripts/9.6_bim_to_vr.py" --count 8 --seed 42` |

---

## 📚 Source materials & references

_Pulled verbatim from `Subject_Plan.md §2 — Core Subjects`. Source of truth is the Subject_Plan; this section is a convenience copy._

### A. 3D Math & Quaternions
*   **Linear Algebra for 3D:** Translation, Rotation, and Scaling matrices (TRS).
*   **Coordinate Spaces:** Object Space $\to$ World Space $\to$ Camera/View Space $\to$ Clip/Screen Space.
*   **Quaternions:** Why we use them (avoiding Gimbal Lock), Slerp (Spherical Linear Interpolation), and quaternion multiplication.

### B. The Graphics Pipeline & Shaders
*   **The Pipeline:** Vertex Shader $\to$ Rasterization $\to$ Fragment/Pixel Shader.
*   **Shading Models:** Lambertian reflectance, Phong, PBR (Physically Based Rendering).
*   **Compute Shaders:** Utilizing the GPU for non-rendering calculations (e.g., fluid simulations, particle systems).

### C. Engine Architectures
*   **Unity (C#):** MonoBehaviour lifecycle, ScriptableObjects, Data-Oriented Technology Stack (DOTS) / ECS.
*   **Unreal (C++):** UObject hierarchy, Actor lifecycles, Blueprints vs C++, Lumen/Nanite concepts.

### D. AEC to VR Pipelines
*   **Data Translation:** Moving from CAD/BIM (Revit, Rhino) to real-time engines.
*   **Optimization:** Mesh decimation, draw call reduction, baking lighting for VR performance (targeting 90+ FPS).
*   **Metadata Integration:** Retaining BIM properties inside the VR environment.

---

---

## 🧰 Generated study aids

> **Status:** placeholder. Drop links to NotebookLM-generated artifacts here as
> you create them. Each subsection currently has a single TODO bullet — replace
> or append `[[wikilinks]]` and external URLs once the artifact exists.

### 🎙️ Audio overviews & podcasts (NotebookLM)

- [ ] TODO: paste the NotebookLM "Audio Overview" link or attach the `.mp3`/`.m4a` file

### 🧠 Mind maps

- [ ] TODO: NotebookLM mind-map URL or screenshot

### ❓ Quizzes

- [ ] TODO: NotebookLM-generated quiz (paste questions or link)

### 📊 Reports & summaries

- [ ] TODO: NotebookLM "Briefing Doc" or "Study Guide" output

### 🃏 Flash cards

- [ ] TODO: deck export (Anki, Obsidian SR, NotebookLM cards)

### 🎬 Video overviews

- [ ] TODO: YouTube / loom / personal recording link

### 📋 Data tables

- [ ] TODO: structured data extracted from the chapters (CSV / Markdown table)

---

## 🔗 Cross-links

- Syllabus & curriculum mindmap: [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/28 - VR & 3D Engineering/Subject_Plan]]
- Master Learning index: [[00 - 09 - Learning Index]]
- Master practice guide: [[../HOW_TO_USE_PRACTICE]]
- Practice GUI app vision: [[../00 - Dev_Tools/PRACTICE_GUI_APP_VISION]]
