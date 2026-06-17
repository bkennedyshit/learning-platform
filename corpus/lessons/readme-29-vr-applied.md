---
title: "README — 29 - VR (Applied)"
subject: "VR"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: subject-readme
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# 29 - VR (Applied) — Subject Hub

> One-page subject hub. Lists chapters, source reading materials, **video / picture references stored outside the repo (linked by URL)**, and placeholders for generated study aids.
> Master practice guide: [HOW_TO_USE_PRACTICE](HOW_TO_USE_PRACTICE).

> **Asset storage convention.**
> - **SVG diagrams** → `../_svgs/vrapp__<chapter>-fig<n>.svg`.
> - **Pictures, screenshots, demo videos, headset photos, comparison galleries** are NOT in this repo. Reference them by **URL**.

> **Relationship to [Track 28 - VR & 3D Engineering](Subject_Plan).** Track 09 is the **foundations** layer — math, shaders, engine internals, BIM-to-VR data plumbing. Track 29 is the **applied / business** layer — hardware ecosystems, app architectures, UX subsystems, vertical pipelines, and product/monetization. Read 09 before 24.

---

## 🚀 Quick start

```bash
cd "C:/Obsidian Vault/Bill's Vault/05-Knowledge_Foundation/09 - Learning/29 - VR"
# Hello-world projects (Unity XR Toolkit, Unreal XR, A-Frame WebXR, RealityKit) — to be added in _practice/
```

For hands-on practice the cheapest path is **Quest 3S ($299) + free Unity / Unreal**. Vision Pro ($3,499) for the premium spatial-computing path. Browser-only WebXR works on any Quest with no install.

---

## 📜 Chapter index

- [29.1 - VR Hardware Ecosystems & Standards](29.1---VR-Hardware-Ecosystems-&-Standards)
- [29.2 - Immersive App Architectures - OpenXR, WebXR, Unity XR, Unreal XR](29.2---Immersive-App-Architectures---OpenXR,-WebXR,-Unity-XR,-Unreal-XR)
- [29.3 - Locomotion & Comfort Design](29.3---Locomotion-&-Comfort-Design)
- [29.4 - Hand, Eye & Body Tracking - Inputs Beyond Controllers](29.4---Hand,-Eye-&-Body-Tracking---Inputs-Beyond-Controllers)
- [29.5 - Mixed Reality & Passthrough Pipelines](29.5---Mixed-Reality-&-Passthrough-Pipelines)
- [29.6 - Architectural Visualization in VR - Revit, IFC, USD to Quest & Vision Pro](29.6---Architectural-Visualization-in-VR---Revit,-IFC,-USD-to-Quest-&-Vision-Pro)
- [29.7 - Networking, Avatars & Multi-User Spaces](29.7---Networking,-Avatars-&-Multi-User-Spaces)
- [29.8 - VR as a Business - Productization, Distribution, Monetization](29.8---VR-as-a-Business---Productization,-Distribution,-Monetization)

---

## 🎬 Video & Picture References (external — open in browser)

### 📺 Video Channels & Courses

| Channel / Course | Track Use | Link |
|---|---|---|
| **Meta Horizon Developer YouTube + docs** | Quest dev | [developers.meta.com/horizon](https://developers.meta.com/horizon/) |
| **Apple visionOS dev videos (WWDC sessions)** | Vision Pro dev | [developer.apple.com/visionos](https://developer.apple.com/visionos/) |
| **Khronos OpenXR talks** | Cross-platform standard | [khronos.org/openxr](https://www.khronos.org/openxr/) |
| **Valem Tutorials** | Practical Unity VR | [@ValemTutorials](https://www.youtube.com/@ValemTutorials) |
| **Justin P Barnett** | Unity XR Toolkit | [@JustinPBarnett](https://www.youtube.com/@JustinPBarnett) |
| **Black Mesh / VR with Andrew** | Unreal Engine VR | [@VRwithAndrew](https://www.youtube.com/@VRwithAndrew) |
| **Cas and Chary VR** | Hardware reviews + dev news | [@CasandCharyVR](https://www.youtube.com/@CasandCharyVR) |
| **MRTV (Mixed Reality TV)** | Headset reviews + interviews | [@MRTV](https://www.youtube.com/@MRTV) |
| **Karl Guttag's KGOnTech (blog)** | Deep-dive headset optics | [kguttag.com](https://kguttag.com/) |
| **Unreal Engine VR Templates videos (Epic)** | Unreal XR | [unrealengine.com/learn](https://www.unrealengine.com/en-US/onlinelearning-courses) |
| **GameDev.tv VR courses** | Unity-focused | [gamedev.tv](https://www.gamedev.tv/) |
| **The Construct (XR / robotics overlap)** | XR dev community | [theconstruct.ai](https://www.theconstruct.ai/) |

### 🖼️ Picture / Diagram Reference Sources

| Source | Use | Link |
|---|---|---|
| **Apple visionOS docs** | App architecture, RealityKit / SwiftUI diagrams | [developer.apple.com/visionos](https://developer.apple.com/visionos/) |
| **Meta Horizon developer hub** | OpenXR architecture, hand-tracking joint diagrams | [developers.meta.com/horizon](https://developers.meta.com/horizon/) |
| **Khronos OpenXR overview pages** | Action-binding model, runtime architecture | [khronos.org/openxr](https://www.khronos.org/openxr/) |
| **Unity XR Interaction Toolkit docs** | Controller + hands + locomotion samples | [docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit](https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest/) |
| **WebXR samples** | Live demos with screenshots | [immersive-web.github.io/webxr-samples](https://immersive-web.github.io/webxr-samples/) |
| **Speckle (arch-viz pipelines)** | Revit↔Unity flow | [speckle.systems](https://speckle.systems/) |

### 📚 Open-Source / Free Books, Specs & Tutorials

| Title | Author / Provider | Link |
|---|---|---|
| OpenXR 1.1 Specification | Khronos | [khronos.org/openxr](https://www.khronos.org/openxr/) |
| Meta OpenXR SDK + 19 native samples | Meta | [github.com/meta-quest/Meta-OpenXR-SDK](https://github.com/meta-quest/Meta-OpenXR-SDK) |
| WebXR Device API Spec | W3C | [immersive-web.github.io/webxr](https://immersive-web.github.io/webxr/) |
| Unity XR Interaction Toolkit | Unity | [docs.unity3d.com](https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest/) |
| Unreal Engine VR Template & docs | Epic | [docs.unrealengine.com](https://docs.unrealengine.com/) |
| visionOS / RealityKit / ARKit docs | Apple | [developer.apple.com/visionos](https://developer.apple.com/visionos/) |
| @react-three/xr + @react-three/fiber | pmndrs | [github.com/pmndrs/react-three-xr](https://github.com/pmndrs/react-three-xr) |
| A-Frame docs | Open source | [aframe.io](https://aframe.io/) |
| Mozilla Hubs source | Mozilla / community | [github.com/mozilla/hubs](https://github.com/mozilla/hubs) |
| Photon Fusion / Mirror / Netcode for GameObjects | Various | manufacturer docs |
| Microsoft Mesh dev docs | Microsoft | [learn.microsoft.com/mesh](https://learn.microsoft.com/en-us/mesh/) |

### 📊 2026 Industry Snapshot

| Source | Use |
|---|---|
| [framesixty — Virtual Reality Development Guide 2026](https://framesixty.com/virtual-reality-development-guide/) | Industry overview |
| [supercraft — VR/AR Spatial Computing Backends 2026](https://gsb.supercraft.host/blog/vr-ar-spatial-computing-game-backends/) | Backend architecture |
| [tech-insider — Vision Pro 2 vs Quest 3S 2026](https://tech-insider.org/apple-vision-pro-2-vs-meta-quest-3s-2026/) | Comparison |
| [Cubix — Vision Pro vs Quest 3 dev guide](https://www.cubix.co/blog/building-apps-for-apple-vision-pro-and-meta-quest-3/) | Dev comparison |
| [alibaba lifetips — Vision Pro vs Quest 3 for Architecture](https://lifetips.alibaba.com/tech-efficiency/vision-pro-vs-quest-for-architecture) | Arch-viz angle |

---

## 🧰 Generated study aids

### 🎙️ Audio overviews
- [ ] TODO: NotebookLM audio of Subject_Plan

### 🧠 Mind maps
- [ ] TODO: NotebookLM mind-map

### ❓ Quizzes
- [ ] TODO: NotebookLM-generated quiz

### 📊 Reports & summaries
- [ ] TODO: 2026 VR/MR landscape briefing

### 🃏 Flash cards
- [ ] TODO: Anki / Obsidian SR (OpenXR vocab, hand-joint indices, comfort principles)

### 🎬 Video overviews
- [ ] TODO: personal Loom of your VR demos

### 📋 Data tables
- [ ] TODO: comparison matrix (Quest 3 / Quest 3S / Vision Pro / Vision Pro 2 / Index 2 / Pico 5 / Vive Focus Vision)

---

## 🔗 Cross-links

- Syllabus & curriculum mindmap: [Subject_Plan](Subject_Plan)
- Visual roadmap: [LEARNING_PATH](LEARNING_PATH)
- Foundational VR / 3D engineering: [Subject_Plan](Subject_Plan)
- Asset pipelines: [Subject_Plan](Subject_Plan)
- Sibling tech: [Subject_Plan](Subject_Plan)
- AI side: [Subject_Plan](Subject_Plan)
- Master Learning index: [00 - 09 - Learning Index](00---09---Learning-Index)
- Master practice guide: [HOW_TO_USE_PRACTICE](HOW_TO_USE_PRACTICE)
