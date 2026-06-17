---
title: "README — 31 - Holographics"
subject: "Holographics"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: subject-readme
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# 31 - Holographics — Subject Hub

> One-page subject hub. Lists chapters, source reading materials, **video / picture references stored outside the repo (linked by URL)**, and placeholders for generated study aids.
> Master practice guide: [HOW_TO_USE_PRACTICE](HOW_TO_USE_PRACTICE).

> **Asset storage convention.**
> - **SVG diagrams** → `../_svgs/holo__<chapter>-fig<n>.svg`.
> - **Pictures, photos of real holograms, scope traces, video walkthroughs, papers** are NOT in this repo. Reference them by **URL**.

---

## 🚀 Quick start

```bash
cd "C:/Obsidian Vault/Bill's Vault/05-Knowledge_Foundation/09 - Learning/31 - Holographics"
# Drill scripts (NumPy diffraction propagators, PyTorch CGH solvers) — to be added
```

For hands-on without an SLM: simulate everything in NumPy / PyTorch. For real displays: **Looking Glass Portrait/Go ($499–$899)** is the cheapest 2026 entry point to commodity light-field hardware.

---

## 📜 Chapter index

- [31.1 - Optics Foundations - Interference, Diffraction, Coherence, Fourier Optics](31.1---Optics-Foundations---Interference,-Diffraction,-Coherence,-Fourier-Optics)
- [31.2 - Classical Holography - Gabor, Denisyuk, Transmission & Reflection](31.2---Classical-Holography---Gabor,-Denisyuk,-Transmission-&-Reflection)
- [31.3 - Computer-Generated Holography - Algorithms, FFT, Neural CGH](31.3---Computer-Generated-Holography---Algorithms,-FFT,-Neural-CGH)
- [31.4 - Spatial Light Modulators & Holographic Displays - LCoS, DMD, Metasurfaces](31.4---Spatial-Light-Modulators-&-Holographic-Displays---LCoS,-DMD,-Metasurfaces)
- [31.5 - Light-Field Displays & Volumetric Capture - Looking Glass, NeRF, 3D Gaussian Splatting](31.5---Light-Field-Displays-&-Volumetric-Capture---Looking-Glass,-NeRF,-3D-Gaussian-Splatting)
- [31.6 - Holographic AR - HoloLens, Magic Leap, Waveguides & the Marketing-vs-Physics Gap](31.6---Holographic-AR---HoloLens,-Magic-Leap,-Waveguides-&-the-Marketing-vs-Physics-Gap)
- [31.7 - Holography in Architecture & Engineering Visualization](31.7---Holography-in-Architecture-&-Engineering-Visualization)
- [31.8 - The Systems Stack - From Photons to Pixels to Products](31.8---The-Systems-Stack---From-Photons-to-Pixels-to-Products)

---

## 🎬 Video & Picture References (external — open in browser)

### 📺 Video Channels & Courses

| Channel / Course | Track Use | Link |
|---|---|---|
| **MIT MAS.450 — Holographic Imaging** | Definitive free holography course | [ocw.mit.edu](https://ocw.mit.edu/courses/mas-450-holographic-imaging-spring-2003/pages/syllabus) |
| **Stanford EE 367 — Computational Imaging & Display** | Computational imaging, holography, light fields | [stanford.edu/class/ee367](https://stanford.edu/class/ee367/) |
| **First Principles of Computer Vision (Shree Nayar, Columbia)** | Free playlist incl. wave optics | [fpcv.cs.columbia.edu](https://fpcv.cs.columbia.edu/) |
| **MIT Tensor Holography project page** | Real-time photoreal CGH with deep learning | [cgh.csail.mit.edu](https://cgh.csail.mit.edu/) |
| **Stanford Wetzstein Lab** | Computational imaging and display research | [computationalimaging.org](https://www.computationalimaging.org/) |
| **Looking Glass Factory** | Practical holographic / light-field displays | [lookingglassfactory.com](https://lookingglassfactory.com/) |
| **HOLOEYE Photonics** | SLM-driven holographic displays | [holoeye.com](https://holoeye.com/) |
| **VR/AR Wiki** | Practical AR display + waveguide reference | [vrarwiki.com](https://vrarwiki.com/) |

### 🖼️ Picture / Diagram Reference Sources

| Source | Use | Link |
|---|---|---|
| **MIT MAS.450 lecture slides** | Recording geometries, hologram types | OCW |
| **Tensor Holography paper figures** | Neural CGH pipeline | [cgh.csail.mit.edu](https://cgh.csail.mit.edu/) |
| **Looking Glass HLD product photos** | Hololuminescent display form factors | [lookingglassfactory.com/hld-overview](https://lookingglassfactory.com/hld-overview) |
| **HoloLens 2 hardware page (Microsoft)** | Waveguide diagrams, AR optics | [learn.microsoft.com/en-us/hololens/hololens2-hardware](https://learn.microsoft.com/en-us/hololens/hololens2-hardware) |
| **Magic Leap 2 docs** | Waveguide AR, MRTK | [developer-docs.magicleap.cloud](https://developer-docs.magicleap.cloud/) |
| **VR/AR Wiki — Waveguide article** | Side-by-side waveguide tech comparisons | [vrarwiki.com/wiki/Waveguide](https://vrarwiki.com/wiki/Waveguide) |
| **HOLOEYE SLM SDK docs** | Real SLM driving | [holoeye.com](https://holoeye.com/spatial-light-modulators/slm-software/slm-display-sdk/) |

### 📚 Open-Source / Free Books & Papers

| Title | Author / Provider | Link |
|---|---|---|
| MIT MAS.450 lecture notes & syllabus | Bove (MIT) | [ocw.mit.edu](https://ocw.mit.edu/courses/mas-450-holographic-imaging-spring-2003/pages/syllabus) |
| Tensor Holography (Shi, Li, Kim, Matusik) | MIT CSAIL | [cgh.csail.mit.edu](https://cgh.csail.mit.edu/) |
| HoloGen open-source CUDA CGH framework | University of Cambridge | [Cambridge repository](https://www.repository.cam.ac.uk/items/6881fbcc-03e0-4e6c-9c1f-7fa78eda35cd) |
| Stanford EE 367 lecture notes | Wetzstein (Stanford) | [stanford.edu/class/ee367](https://stanford.edu/class/ee367/) |
| Looking Glass Factory documentation | Looking Glass | [docs.lookingglassfactory.com](https://docs.lookingglassfactory.com/) |
| arXiv physics.optics + cs.GR pre-prints | Open | [arxiv.org](https://arxiv.org/list/physics.optics/recent) |
| Fairy Lights in Femtoseconds (Ochiai et al., aerial volumetric displays) | arXiv | [arXiv 1506.06668](https://arxiv.org/abs/1506.06668) |
| Sub-second volumetric 3D printing by holographic light fields (Nature 2026) | Nature | [Nature 2026 article](https://www.nature.com/articles/s41586-026-10114-5) |

---

## 🧰 Generated study aids

### 🎙️ Audio overviews
- [ ] TODO: NotebookLM audio of Subject_Plan

### 🧠 Mind maps
- [ ] TODO: NotebookLM mind-map URL

### ❓ Quizzes
- [ ] TODO: NotebookLM-generated quiz

### 📊 Reports & summaries
- [ ] TODO: 2026 holographic display landscape briefing doc

### 🃏 Flash cards
- [ ] TODO: Anki / Obsidian SR deck (Fourier-optics, hologram types, SLM types)

### 🎬 Video overviews
- [ ] TODO: personal Loom of CGH simulation runs

### 📋 Data tables
- [ ] TODO: comparison matrix (Looking Glass HLD / Sony Spatial Reality / Leia / Hologrify / Voxon)

---

## 🔗 Cross-links

- Syllabus & curriculum mindmap: [Subject_Plan](Subject_Plan)
- Visual roadmap: [LEARNING_PATH](LEARNING_PATH)
- Optics prereq: [Subject_Plan](Subject_Plan)
- 3D side: [Subject_Plan](Subject_Plan) (asset pipelines), [Subject_Plan](Subject_Plan) (rendering math)
- VR sibling: [Subject_Plan](Subject_Plan) (the headset-based alternative)
- Master Learning index: [00 - 09 - Learning Index](00---09---Learning-Index)
- Master practice guide: [HOW_TO_USE_PRACTICE](HOW_TO_USE_PRACTICE)
