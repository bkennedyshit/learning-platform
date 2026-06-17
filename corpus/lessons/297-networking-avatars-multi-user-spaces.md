---
title: "29.7 — Networking, Avatars & Multi-User Spaces"
subject: "VR"
catalog: advanced
audience_tier: higher-education
chapter: "29.7"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 29.7 — Networking, Avatars & Multi-User Spaces

> *"Spatial computing backends must synchronize sub‑20 ms hand-tracking data, persist spatial anchors across sessions, and stream passthrough video with imperceptible latency."*
> — paraphrased from [supercraft — VR/AR Spatial Computing Game Backends 2026](https://gsb.supercraft.host/blog/vr-ar-spatial-computing-game-backends/) (rephrased for compliance)

---

## 🎯 Learning Objectives

1. Compare backends: **Photon Fusion / Quantum**, **Mirror**, **Netcode for GameObjects**, **Microsoft Mesh**, **Spatial.io**, **VRChat / Resonite**, **Hubs**.
2. Understand **state synchronization**: client prediction, server reconciliation, snapshot interpolation, delta compression.
3. Synchronize **hand + body tracking** at 60–90 Hz with bandwidth budgets.
4. Implement **avatar IK** driven by 3 inputs (head + 2 hands) and optionally trackers.
5. Use **spatial audio** + **voice chat** (Photon Voice, Vivox, Discord SDK).
6. Build **persistent spaces** with anchors, save/load state, cross-session continuity.
7. Connect to ROS 2 / DDS-style messaging where multi-robot + multi-user scenes converge.

---

## 🖼️ Visual Anchor

> *Picture / video reference (external):*
> - 📺 [Photon Engine — Fusion docs](https://doc.photonengine.com/fusion/)
> - 📺 [Mirror Networking docs](https://mirror-networking.com/)
> - 📺 [Microsoft Mesh dev docs](https://learn.microsoft.com/en-us/mesh/)
> - 📺 [Spatial.io developer hub](https://spatial.io/developers)
> - 📺 [Mozilla Hubs source](https://github.com/mozilla/hubs)

---

## 📚 1. Backend Selection

| Backend | Best at | License |
|---|---|---|
| **Photon Fusion** | High-tick-rate Unity multiplayer (sports, action) | Paid (with free tier) |
| **Photon Quantum** | Deterministic simulation; rollback | Paid |
| **Mirror** | Open-source Unity multiplayer | Free, MIT |
| **Netcode for GameObjects** | Unity official | Free |
| **Unreal Replication** | Built-in to UE | Engine license |
| **Microsoft Mesh** | Enterprise multi-user MR + Teams integration | Microsoft cloud |
| **Spatial.io** | Web + Quest / Vision Pro social spaces | Free + paid tiers |
| **Mozilla Hubs** | Browser-first social; open-source | MPL |
| **VRChat SDK / Resonite** | Social VR worlds | Platform-tied |

For arch-viz multi-user demos: **Mirror or Netcode + Photon Voice** is the practical free-to-cheap default.

---

## 🔁 2. Sync Pattern

```
Client A:
  read tracking 90 Hz
  local prediction
  send delta to server every 30–60 Hz

Server:
  authoritative state
  rebroadcast at 30 Hz to all clients

Client B:
  receive snapshots
  interpolate between last 2
  reconcile if local prediction diverges
```

For arch-viz (mostly cosmetic), interpolation + last-write-wins is enough. For action / sports, you'll want full prediction + reconciliation.

---

## 📊 3. Bandwidth Budgets

| Stream | ~Bytes/frame | At 30 Hz |
|---|---|---|
| Head pose | 28 (vec3 + quat) | ~6.7 kbps |
| 2× hand poses (26 joints each) | ~1500 | ~360 kbps |
| Body pose (16 joints) | ~500 | ~120 kbps |
| Voice (Opus 24 kbps) | – | ~24 kbps |
| Misc events | – | < 10 kbps |

→ ~500 kbps per active user is comfortable; under 1 Mbps even with full body + voice.

Tricks: quantize joint orientations to 16-bit, send only **changed** joints, drop hand tracking when hidden.

---

## 🦾 4. Avatar IK Patterns

For 3-input IK (HMD + 2 controllers):
- Solve neck + spine from head pose.
- Solve shoulders + arms from hands.
- Procedurally drive legs (locomotion-driven step animation).
- Add **mirror correction** so users see their own avatar correctly.

Tools: **Final IK** (Unity, paid), **VRIK**, **Unreal Control Rig**, **Animation Rigging package** (Unity free).

---

## 🔊 5. Spatial Audio + Voice

- **Spatial audio**: HRTF-convolved per source. Vision Pro + Quest + Index all support OpenAL Soft / Steam Audio / engine-native.
- **Voice**: Photon Voice, Vivox, Discord SDK. End-to-end latency target < 200 ms.
- **Lip sync**: Oculus Lipsync (Unity), or VLM-based mouth-shape inference for higher quality.

---

## 🛠️ 6. Worked Example (skeleton) — 4-User Co-Located Arch Walkthrough

1. Mirror or Netcode for GameObjects, Unity XR Toolkit.
2. Each user spawns an avatar prefab with VRIK + 16-joint body.
3. Spatial anchor shared via Quest Cloud Anchors → all users see the same model in the same physical place.
4. Photon Voice for chat.
5. Persistent room state (door opens, materials toggled) saved to Mirror server / Firebase / Speckle.
6. Browser viewer (Hubs / @react-three/xr) joins as observer.

---

## 🔗 7. Cross-links & Further Reading

### Internal
- [29.4 - Hand, Eye & Body Tracking - Inputs Beyond Controllers](29.4---Hand,-Eye-&-Body-Tracking---Inputs-Beyond-Controllers)
- [29.5 - Mixed Reality & Passthrough Pipelines](29.5---Mixed-Reality-&-Passthrough-Pipelines)
- [29.6 - Architectural Visualization in VR - Revit, IFC, USD to Quest & Vision Pro](29.6---Architectural-Visualization-in-VR---Revit,-IFC,-USD-to-Quest-&-Vision-Pro)
- [29.8 - VR as a Business - Productization, Distribution, Monetization](29.8---VR-as-a-Business---Productization,-Distribution,-Monetization)
- [22.5 - ROS 2 & Middleware - Nodes, Topics, Services, Actions, DDS](22.5---ROS-2-&-Middleware---Nodes,-Topics,-Services,-Actions,-DDS)

### External
- [Photon Fusion docs](https://doc.photonengine.com/fusion/)
- [Mirror Networking](https://mirror-networking.com/)
- [Netcode for GameObjects](https://docs-multiplayer.unity3d.com/)
- [Microsoft Mesh](https://learn.microsoft.com/en-us/mesh/)
- [Spatial.io developers](https://spatial.io/developers)
- [Mozilla Hubs](https://github.com/mozilla/hubs)
- [supercraft 2026 — VR/AR backends](https://gsb.supercraft.host/blog/vr-ar-spatial-computing-game-backends/)

---

## ⚠️ 8. Common Misconceptions

- **"Multi-user is just multiplayer."** Add tracking + spatial audio + occlusion + persistent anchors — much more.
- **"P2P scales fine."** Up to ~4 users; beyond, central authority + interest management is required.
- **"Voice is solved."** Latency, echo, and spatial-audio quality vary widely; test exhaustively.
- **"Servers are expensive."** Photon-style cloud + small dedicated VPS handle most arch-viz scales for $50–$200/month.
