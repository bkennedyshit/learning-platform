---
title: "Spatial Computing Interaction Design"
subject: "VR & 3D Engineering"
catalog: advanced
audience_tier: higher-education
chapter: "28.7"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 28.7 — Spatial Computing & Interaction Design

> *"The best interface is no interface — it's the world itself."* — Golden Krishna (adapted for spatial computing)

Spatial computing dissolves the boundary between digital information and physical space. Unlike screen-based interfaces where users point and click, XR interactions are embodied: users reach, grab, gaze, gesture, and walk through information. This chapter covers the interaction design principles, input modalities, and technical frameworks (OpenXR, WebXR) that make spatial interfaces intuitive, comfortable, and performant.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Describe the **OpenXR** runtime architecture and its role as a cross-platform XR abstraction.
2. Implement **ray-based** and **direct manipulation** interaction patterns.
3. Design interactions that respect **ergonomic constraints** (arm fatigue, field of view, vestibular comfort).
4. Implement **hand tracking** input processing (pinch detection, gesture recognition).
5. Apply **Fitts' Law** adapted for 3D spatial targeting.
6. Build **WebXR** experiences using the WebXR Device API.
7. Design **locomotion systems** that minimize motion sickness (teleportation, continuous with vignette).
8. Apply **spatial UI** principles: world-locked, head-locked, and body-locked interface placement.

---

## 🖼️ Visual Anchor — XR Interaction Modalities

![track-09__9.7-fig1](track-09__9.7-fig1.svg)

---

## 📚 1. Definitions

### Definition 28.7.1 — OpenXR

**OpenXR** is a royalty-free, open standard (Khronos Group) providing a unified API for XR applications across headsets (Quest, Vive, WMR, Apple Vision Pro). It abstracts:
- **Session management** (create, begin, end, destroy)
- **Reference spaces** (LOCAL, STAGE, VIEW)
- **Input/action system** (bindings mapped to device-specific controls)
- **Composition layers** (projection, quad, cylinder layers)

### Definition 28.7.2 — WebXR Device API

**WebXR** is a W3C standard enabling XR experiences in web browsers:
- `navigator.xr.requestSession('immersive-vr')` — enter VR
- `XRFrame.getViewerPose(referenceSpace)` — get head position
- `XRInputSource` — controllers and hand tracking
- Renders via WebGL/WebGPU to `XRWebGLLayer`

### Definition 28.7.3 — Degrees of Freedom (DoF)

- **3-DoF:** Rotation only (head orientation). No positional tracking. (e.g., Cardboard)
- **6-DoF:** Rotation + translation (head position tracked). Required for room-scale VR.
- **6-DoF controllers:** Each hand has independent position + orientation tracking.
- **Hand tracking:** 26 joints per hand, each with 6-DoF pose.

### Definition 28.7.4 — Fitts' Law (3D Adaptation)

The time $T$ to acquire a target of width $W$ at distance $D$ in 3D:

$$
T = a + b \cdot \log_2\left(\frac{D}{W} + 1\right)
$$

In VR, $D$ is the 3D Euclidean distance from hand/ray origin to target center, and $W$ is the target's solid angle (apparent size). Depth perception uncertainty adds ~30% to acquisition time compared to 2D.

### Definition 28.7.5 — Locomotion Techniques

| Technique | Comfort | Immersion | Use Case |
|-----------|---------|-----------|----------|
| **Teleportation** | High | Medium | Room-scale, seated |
| **Continuous (smooth)** | Low | High | Experienced users, FPS |
| **Arm-swing** | Medium | High | Active experiences |
| **Redirect walking** | High | High | Large tracked spaces |
| **Snap turn** | High | Medium | Seated, cable management |

### Definition 28.7.6 — Spatial UI Placement Strategies

- **World-locked:** UI attached to a fixed world position (e.g., control panel on a wall). Stable, but user must navigate to it.
- **Head-locked:** UI follows head rotation (HUD). Causes discomfort — avoid except for brief notifications.
- **Body-locked (tag-along):** UI loosely follows the user with damping. Comfortable, always accessible.
- **Hand-anchored:** UI attached to wrist/palm. Natural for menus (like checking a watch).

### Definition 28.7.7 — Vestibular-Ocular Conflict

Motion sickness in VR occurs when visual motion (optic flow) does not match vestibular (inner ear) signals. The brain interprets the mismatch as poisoning and triggers nausea. Mitigation:
- Maintain 90+ FPS (visual latency < 20 ms)
- Reduce peripheral optic flow (vignette during locomotion)
- Provide a stable reference frame (cockpit, nose)
- Never move the camera without user input



---

## 📐 2. Axioms / Postulates

### Axiom 28.7.A1 — The Comfort Imperative

No interaction technique, however efficient, is acceptable if it causes user discomfort. Comfort always takes priority over immersion or efficiency in VR design.

### Axiom 28.7.A2 — Direct Manipulation Is the Default

When an object is within arm's reach, users expect to interact with it directly (grab, push, rotate) rather than through indirect mechanisms. Violating this expectation breaks presence.

### Axiom 28.7.A3 — Proprioception Accuracy

Users can localize their hand position to within ~2 cm without visual feedback (proprioception). UI elements smaller than this threshold require visual guidance (highlights, snap zones) for reliable interaction.

---

## 🛡️ 3. Lemmas

### Lemma 28.7.1 — Ray-Sphere Intersection for Target Selection

A ray $\mathbf{r}(t) = \mathbf{o} + t\hat{\mathbf{d}}$ intersects a sphere of radius $r$ centered at $\mathbf{c}$ when:

$$
t = -(\hat{\mathbf{d}} \cdot \mathbf{L}) \pm \sqrt{(\hat{\mathbf{d}} \cdot \mathbf{L})^2 - |\mathbf{L}|^2 + r^2}
$$

where $\mathbf{L} = \mathbf{o} - \mathbf{c}$. A hit occurs when the discriminant $\geq 0$ and $t > 0$.

**Proof.** Substitute the ray equation into the sphere equation $|\mathbf{r}(t) - \mathbf{c}|^2 = r^2$:

$$
|\mathbf{o} + t\hat{\mathbf{d}} - \mathbf{c}|^2 = r^2
$$

$$
|\mathbf{L} + t\hat{\mathbf{d}}|^2 = r^2
$$

$$
|\hat{\mathbf{d}}|^2 t^2 + 2(\hat{\mathbf{d}} \cdot \mathbf{L})t + |\mathbf{L}|^2 - r^2 = 0
$$

Since $|\hat{\mathbf{d}}| = 1$: $t^2 + 2(\hat{\mathbf{d}} \cdot \mathbf{L})t + (|\mathbf{L}|^2 - r^2) = 0$.

By the quadratic formula: $t = -(\hat{\mathbf{d}} \cdot \mathbf{L}) \pm \sqrt{(\hat{\mathbf{d}} \cdot \mathbf{L})^2 - |\mathbf{L}|^2 + r^2}$. $\blacksquare$

### Lemma 28.7.2 — Minimum Button Size from Visual Angle

For a button to subtend at least $\alpha$ degrees at distance $d$:

$$
W_{\min} = 2d \tan(\alpha/2)
$$

At $d = 1$ m and $\alpha = 2°$ (comfortable targeting): $W_{\min} = 2 \times 1 \times \tan(1°) = 2 \times 0.01745 = 0.035$ m $= 3.5$ cm.

### Lemma 28.7.3 — Pinch Detection Threshold

Hand tracking pinch is detected when the distance between thumb tip and index finger tip falls below a threshold $\delta$:

$$
\text{isPinching} = |\mathbf{p}_{\text{thumb}} - \mathbf{p}_{\text{index}}| < \delta
$$

Typical $\delta = 2\text{–}3$ cm. Hysteresis (different thresholds for pinch start vs. release) prevents flickering.

---

## 👑 4. Theorems

### Theorem 28.7.1 — Fitts' Law Predicts Selection Time in VR

For ray-based selection of a target with angular size $\omega$ (radians) at angular distance $\theta$ from the ray's current direction:

$$
T = a + b \cdot \log_2\left(\frac{\theta}{\omega} + 1\right)
$$

Empirically: $a \approx 200$ ms, $b \approx 150$ ms for controller ray interaction. Hand tracking adds ~50 ms due to tracking latency and reduced precision.

### Theorem 28.7.2 — Vection Reduction via Peripheral Restriction

Restricting the field of view during locomotion (dynamic vignette) reduces vection (illusory self-motion) proportionally to the solid angle removed. Reducing FOV from 100° to 60° during movement reduces reported discomfort by ~60% (Fernandes & Feiner, 2016).

### Theorem 28.7.3 — Motion-to-Photon Latency Budget

Total motion-to-photon latency must be $\leq 20$ ms to avoid perceptible lag:

$$
t_{\text{total}} = t_{\text{tracking}} + t_{\text{game}} + t_{\text{render}} + t_{\text{compositor}} + t_{\text{display}}
$$

Typical breakdown: tracking (2 ms) + game logic (4 ms) + render (6 ms) + compositor (2 ms) + display scanout (3 ms) = 17 ms.

---

## ✍️ 5. Proofs / Derivations

### 5.1 Derivation of Angular Size for UI Placement

**Goal:** Determine the physical size of a UI panel that subtends a desired angular width.

**Given:** User at distance $d$ from panel. Desired angular width $\alpha$ (degrees).

**Step 1:** The panel width $W$ and distance $d$ relate via:

$$
\tan(\alpha/2) = \frac{W/2}{d}
$$

**Step 2:** Solve for $W$:

$$
W = 2d \tan(\alpha/2)
$$

**Step 3:** For small angles ($\alpha < 20°$), $\tan(\alpha/2) \approx \alpha/2$ (in radians):

$$
W \approx d \cdot \alpha_{\text{rad}} = d \cdot \frac{\alpha_{\text{deg}} \cdot \pi}{180}
$$

**Example:** A menu at $d = 1.5$ m subtending $30°$:

$$
W = 2 \times 1.5 \times \tan(15°) = 3 \times 0.2679 = 0.804 \text{ m} \approx 80 \text{ cm}
$$

### 5.2 Derivation of Comfortable Interaction Zone

**Goal:** Define the volume where sustained hand interaction is comfortable.

**Constraints (ergonomic research):**
- Elbow angle: 70°–120° (avoid full extension or tight flexion)
- Shoulder elevation: < 30° above horizontal (avoid "gorilla arm")
- Wrist deviation: < 15° from neutral

**Step 1:** With arm length $L_{\text{arm}} \approx 0.6$ m and the above constraints, the comfortable reach envelope is approximately:

- **Radial distance from shoulder:** 0.25–0.5 m
- **Vertical range:** chest height ± 0.3 m (avoid above shoulders)
- **Lateral range:** ± 0.4 m from body center

**Step 2:** This defines an approximate ellipsoidal volume:

$$
V_{\text{comfort}} \approx \frac{4}{3}\pi (0.4)(0.3)(0.25) \approx 0.126 \text{ m}^3
$$

UI elements requiring sustained interaction should be placed within this volume. $\blacksquare$



---

## 💻 6. Code Examples

### 6.1 WebXR: Basic Immersive Session

```javascript
// WebXR session initialization
async function startVR() {
    if (!navigator.xr) {
        console.error('WebXR not supported');
        return;
    }

    const session = await navigator.xr.requestSession('immersive-vr', {
        requiredFeatures: ['local-floor'],
        optionalFeatures: ['hand-tracking']
    });

    const gl = canvas.getContext('webgl2', { xrCompatible: true });
    const glLayer = new XRWebGLLayer(session, gl);
    session.updateRenderState({ baseLayer: glLayer });

    const refSpace = await session.requestReferenceSpace('local-floor');

    session.requestAnimationFrame(function onFrame(time, frame) {
        session.requestAnimationFrame(onFrame);

        const pose = frame.getViewerPose(refSpace);
        if (!pose) return;

        gl.bindFramebuffer(gl.FRAMEBUFFER, glLayer.framebuffer);

        for (const view of pose.views) {
            const viewport = glLayer.getViewport(view);
            gl.viewport(viewport.x, viewport.y, viewport.width, viewport.height);

            // view.transform.matrix — 4x4 view matrix (Float32Array)
            // view.projectionMatrix — 4x4 projection matrix
            renderScene(view.transform.inverse.matrix, view.projectionMatrix);
        }
    });
}
```

### 6.2 WebXR: Controller Ray Interaction

```javascript
function processInput(frame, refSpace) {
    for (const source of frame.session.inputSources) {
        if (source.targetRayMode === 'tracked-pointer') {
            const rayPose = frame.getPose(source.targetRaySpace, refSpace);
            if (!rayPose) continue;

            const origin = rayPose.transform.position;
            const direction = new Float32Array([-rayPose.transform.matrix[8],
                                                 -rayPose.transform.matrix[9],
                                                 -rayPose.transform.matrix[10]]);

            // Ray-cast against scene objects
            const hit = raycast(
                [origin.x, origin.y, origin.z],
                direction,
                sceneObjects
            );

            if (hit && source.gamepad?.buttons[0]?.pressed) {
                selectObject(hit.object);
            }
        }
    }
}
```

### 6.3 Unity C#: XR Grab Interactable

```csharp
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

[RequireComponent(typeof(XRGrabInteractable))]
public class GrabbableObject : MonoBehaviour
{
    private XRGrabInteractable grabInteractable;
    private Vector3 originalScale;

    void Awake()
    {
        grabInteractable = GetComponent<XRGrabInteractable>();
        originalScale = transform.localScale;

        grabInteractable.selectEntered.AddListener(OnGrab);
        grabInteractable.selectExited.AddListener(OnRelease);
    }

    private void OnGrab(SelectEnterEventArgs args)
    {
        // Haptic feedback on grab
        if (args.interactorObject is XRBaseControllerInteractor controller)
        {
            controller.SendHapticImpulse(0.5f, 0.1f);
        }
        // Visual feedback
        GetComponent<Renderer>().material.SetFloat("_Outline", 1f);
    }

    private void OnRelease(SelectExitEventArgs args)
    {
        GetComponent<Renderer>().material.SetFloat("_Outline", 0f);
    }
}
```

### 6.4 OpenXR C: Action-Based Input

```cpp
// OpenXR action creation and polling (simplified)
XrActionSet actionSet;
XrAction grabAction, triggerAction, poseAction;

void CreateActions(XrInstance instance, XrSession session) {
    // Create action set
    XrActionSetCreateInfo setInfo{XR_TYPE_ACTION_SET_CREATE_INFO};
    strcpy(setInfo.actionSetName, "gameplay");
    strcpy(setInfo.localizedActionSetName, "Gameplay");
    xrCreateActionSet(instance, &setInfo, &actionSet);

    // Create grab action (boolean)
    XrActionCreateInfo grabInfo{XR_TYPE_ACTION_CREATE_INFO};
    grabInfo.actionType = XR_ACTION_TYPE_BOOLEAN_INPUT;
    strcpy(grabInfo.actionName, "grab");
    strcpy(grabInfo.localizedActionName, "Grab Object");
    grabInfo.countSubactionPaths = 2;
    XrPath handPaths[2]; // /user/hand/left, /user/hand/right
    grabInfo.subactionPaths = handPaths;
    xrCreateAction(actionSet, &grabInfo, &grabAction);

    // Suggest bindings for specific controllers
    XrActionSuggestedBinding bindings[] = {
        {grabAction, squeezePath_left},
        {grabAction, squeezePath_right},
    };
    // ... attach to session and sync each frame
}

void PollInput(XrSession session, XrSpace handSpace) {
    XrActionStateBoolean grabState{XR_TYPE_ACTION_STATE_BOOLEAN};
    XrActionStateGetInfo getInfo{XR_TYPE_ACTION_STATE_GET_INFO};
    getInfo.action = grabAction;
    xrGetActionStateBoolean(session, &getInfo, &grabState);

    if (grabState.isActive && grabState.currentState) {
        // Hand is squeezing — perform grab logic
    }
}
```

---

## 🧮 7. Worked Examples

### Example 28.7.1 — Calculating UI Panel Size for Readability

**Problem:** A text panel must be readable at 2m distance. Minimum text height = 1° visual angle. Panel should display 20 lines of text with 1.5× line spacing. What panel dimensions are needed?

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1:** Text height from visual angle:

$$
h_{\text{char}} = 2d \tan(\alpha/2) = 2 \times 2 \times \tan(0.5°) = 4 \times 0.00873 = 0.0349 \text{ m} \approx 3.5 \text{ cm}
$$

**Step 2:** Panel height for 20 lines at 1.5× spacing:

$$
H = 20 \times h_{\text{char}} \times 1.5 = 20 \times 0.035 \times 1.5 = 1.05 \text{ m}
$$

**Step 3:** Panel width (assuming ~40 characters per line, character aspect ratio 0.6):

$$
W = 40 \times h_{\text{char}} \times 0.6 = 40 \times 0.035 \times 0.6 = 0.84 \text{ m}
$$

**Result:** Panel dimensions ≈ 84 cm × 105 cm at 2m distance. This is large — consider reducing distance to 1.2m or using scrolling.

</details>

### Example 28.7.2 — Fitts' Law: Comparing Button Sizes

**Problem:** Two button designs: (A) 3cm at 50cm distance, (B) 6cm at 100cm distance. Which is faster to select?

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Fitts' Index of Difficulty:**

$$
ID = \log_2\left(\frac{D}{W} + 1\right)
$$

**Button A:** $ID_A = \log_2(50/3 + 1) = \log_2(17.67) = 4.14$ bits

**Button B:** $ID_B = \log_2(100/6 + 1) = \log_2(17.67) = 4.14$ bits

They have identical difficulty — the ratio $D/W$ is the same. Fitts' Law depends on the ratio, not absolute values.

**However:** In VR, depth perception adds uncertainty. Button A at 50cm is within direct manipulation range (hand can reach it), while Button B at 100cm requires ray casting. Direct manipulation is typically 100–200ms faster due to proprioceptive feedback.

**Recommendation:** Button A is faster in practice due to interaction modality advantage.

</details>

### Example 28.7.3 — Motion-to-Photon Latency Audit

**Problem:** A VR app measures: tracking = 3ms, game logic = 6ms, render = 8ms, compositor = 2ms, display = 4ms. Is it within budget? What should be optimized?

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Total:** $3 + 6 + 8 + 2 + 4 = 23$ ms

**Budget:** ≤ 20 ms. **Over budget by 3 ms.**

**Analysis:**
- Tracking (3ms): Hardware-limited, cannot reduce
- Game logic (6ms): Above typical 4ms budget — profile for hot spots
- Render (8ms): Above 6ms target — reduce draw calls, simplify shaders
- Compositor (2ms): Normal
- Display (4ms): Hardware-limited (panel scanout time)

**Optimization priority:**
1. **Render (8→6ms):** Enable single-pass stereo instancing (saves ~2ms), reduce overdraw
2. **Game logic (6→4ms):** Move physics to fixed timestep, reduce per-frame allocations

**After optimization:** $3 + 4 + 6 + 2 + 4 = 19$ ms ✓

</details>

---

## 🔗 8. Cross-links & Further Reading

### Internal Links
- **Previous:** [28.6 - AEC to VR Pipelines - BIM Data](28.6---AEC-to-VR-Pipelines---BIM-Data) — spatial interaction with BIM models
- **Quaternions for tracking:** [28.2 - Quaternions & Rotations](28.2---Quaternions-&-Rotations) — head/hand orientation representation
- **Rendering budget:** [28.3 - Graphics Rendering Pipeline](28.3---Graphics-Rendering-Pipeline) — frame time constraints
- **Engine XR systems:** [28.5 - Game Engine Architectures - Unity & Unreal](28.5---Game-Engine-Architectures---Unity-&-Unreal) — XR Interaction Toolkit, OpenXR plugin
- **Geodesics:** [8.7 - Geodesics & Curvature](8.7---Geodesics-&-Curvature) — curved UI surfaces in spatial computing

### External Resources
- **OpenXR Specification** — khronos.org/openxr
- **WebXR Device API** — immersive-web.github.io/webxr
- **Meta Quest Design Guidelines** — developer.oculus.com/design
- **Apple visionOS HIG** — developer.apple.com/design/human-interface-guidelines/spatial-computing
- **Designing for Mixed Reality** (Microsoft) — learn.microsoft.com/windows/mixed-reality/design
- **Fernandes & Feiner (2016):** "Combating VR Sickness through Subtle Dynamic FOV Modification"

### Practice
- [9.7_xr_interaction.md](9.7_xr_interaction.md) — WebXR/OpenXR interaction patterns and UX heuristics



---

## 📎 Appendix: Advanced Spatial Computing Topics

### A.1 Hand Tracking Joint Model (OpenXR)

The OpenXR hand tracking extension defines 26 joints per hand:

```
XR_HAND_JOINT_PALM = 0
XR_HAND_JOINT_WRIST = 1
XR_HAND_JOINT_THUMB_METACARPAL = 2
XR_HAND_JOINT_THUMB_PROXIMAL = 3
XR_HAND_JOINT_THUMB_DISTAL = 4
XR_HAND_JOINT_THUMB_TIP = 5
XR_HAND_JOINT_INDEX_METACARPAL = 6
XR_HAND_JOINT_INDEX_PROXIMAL = 7
XR_HAND_JOINT_INDEX_INTERMEDIATE = 8
XR_HAND_JOINT_INDEX_DISTAL = 9
XR_HAND_JOINT_INDEX_TIP = 10
... (middle, ring, little follow same pattern)
XR_HAND_JOINT_LITTLE_TIP = 25
```

Each joint provides:
- `XrPosef` (position + orientation quaternion)
- `float radius` (joint sphere radius for collision)
- `XrHandJointVelocityEXT` (linear + angular velocity)

### A.2 Gesture Recognition Pipeline

```python
# Simplified gesture recognition from hand joint data
import numpy as np

def detect_pinch(thumb_tip, index_tip, threshold=0.025):
    """Detect pinch gesture from joint positions."""
    distance = np.linalg.norm(thumb_tip - index_tip)
    return distance < threshold

def detect_point(joints):
    """Detect pointing gesture: index extended, others curled."""
    index_extended = is_finger_extended(joints, 'index')
    middle_curled = not is_finger_extended(joints, 'middle')
    ring_curled = not is_finger_extended(joints, 'ring')
    little_curled = not is_finger_extended(joints, 'little')
    return index_extended and middle_curled and ring_curled and little_curled

def is_finger_extended(joints, finger):
    """Check if finger is extended by comparing joint angles."""
    # Angle between proximal-intermediate and intermediate-distal segments
    proximal = joints[f'{finger}_proximal']
    intermediate = joints[f'{finger}_intermediate']
    distal = joints[f'{finger}_distal']
    tip = joints[f'{finger}_tip']

    v1 = intermediate - proximal
    v2 = tip - intermediate
    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    angle = np.arccos(np.clip(cos_angle, -1, 1))

    return angle < np.radians(30)  # Less than 30° bend = extended

def get_pinch_point(thumb_tip, index_tip):
    """Get the interaction point (midpoint between thumb and index)."""
    return (thumb_tip + index_tip) / 2.0
```

### A.3 Spatial Audio Integration

Spatial audio is critical for presence and interaction feedback in VR:

**HRTF (Head-Related Transfer Function):**
- Models how sound reaches each ear differently based on source direction
- Provides elevation and front/back disambiguation
- Personalized HRTFs improve localization accuracy by ~30%

**Implementation priorities:**
1. **UI feedback sounds:** Spatialized at interaction point (button click, grab)
2. **Ambient soundscape:** Non-spatialized background (room tone)
3. **Object sounds:** Spatialized at object position (machinery, water)
4. **Occlusion:** Reduce high frequencies for sounds behind walls
5. **Reverb zones:** Match acoustic properties to room geometry

### A.4 Eye Tracking and Foveated Rendering

**Fixed Foveated Rendering (FFR):**
- Reduces resolution in peripheral vision (where acuity is low)
- No eye tracking required — assumes center gaze
- Quest 2: 3 tiers (Low/Medium/High reduction)
- Performance gain: 20–40% fragment shader savings

**Dynamic Foveated Rendering (DFR):**
- Uses eye tracking to determine gaze point
- Full resolution only in foveal region (~5° central)
- Aggressive reduction in periphery (>30° from gaze)
- Performance gain: 50–70% fragment savings
- Requires: eye tracking hardware (Quest Pro, Apple Vision Pro, PSVR2)

### A.5 Passthrough and Mixed Reality

**Video Passthrough Architecture:**
- Cameras capture real world → distortion correction → compositing with virtual content → display
- Latency: additional 5–10ms for camera processing
- Resolution: limited by camera sensor (Quest 3: 4MP per eye)

**Spatial Anchors:**
```csharp
// Unity AR Foundation: Place virtual object at real-world position
async void PlaceAnchor(Vector3 worldPosition, Quaternion rotation)
{
    var anchor = new GameObject("Anchor");
    anchor.transform.SetPositionAndRotation(worldPosition, rotation);
    var arAnchor = anchor.AddComponent<ARAnchor>();

    // Persist across sessions (cloud anchors)
    await anchorManager.TrySaveAnchorAsync(arAnchor);
}
```

### A.6 Accessibility in XR

**Input alternatives:**
- Controller → Hand tracking → Gaze+dwell → Voice → Switch input
- Every interaction must have at least 2 input paths

**Visual accessibility:**
- Minimum contrast ratio 4.5:1 for text
- Color-blind safe palettes (avoid red/green only indicators)
- Scalable text (user-adjustable size)
- High-contrast mode option

**Physical accessibility:**
- Seated mode for all experiences
- One-handed operation mode
- Adjustable interaction distances
- Reduced motion options (disable smooth locomotion)

**Cognitive accessibility:**
- Clear, consistent interaction patterns
- Undo/redo for all actions
- Progress indicators for multi-step tasks
- Optional tutorials and hints

### A.7 Multiplayer Spatial Presence

**Avatar representation levels:**
1. **Floating hands + head:** Minimal (3 tracked points)
2. **Upper body IK:** Estimated from HMD + 2 controllers
3. **Full body IK:** Requires additional trackers (hip, feet)
4. **Photorealistic codec avatar:** ML-based face/body reconstruction

**Network requirements for co-presence:**
- Pose update rate: 72–90 Hz (match display refresh)
- Latency: < 100ms for comfortable interaction
- Bandwidth: ~50 KB/s per avatar (compressed poses)
- Prediction: extrapolate 1–2 frames to hide network jitter




---

## 🧠 9. Extended Worked Examples & Deep Dives

### Example 28.1 — OpenXR Action Binding: Controller Trigger → Grab Event

**Problem:** Trace the complete data flow from a user squeezing the right controller trigger to a "grab" action firing in an OpenXR application. Show every API struct, binding path, and state transition with exact field values.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Define the Action Set and Action

At application startup, we create an action set and a float-input action:

```cpp
// Create action set
XrActionSetCreateInfo actionSetInfo{XR_TYPE_ACTION_SET_CREATE_INFO};
strcpy(actionSetInfo.actionSetName, "gameplay");
strcpy(actionSetInfo.localizedActionSetName, "Gameplay");
actionSetInfo.priority = 0;
XrActionSet gameplaySet;
xrCreateActionSet(instance, &actionSetInfo, &gameplaySet);

// Create grab action (float type for analog trigger)
XrActionCreateInfo grabInfo{XR_TYPE_ACTION_CREATE_INFO};
grabInfo.actionType = XR_ACTION_TYPE_FLOAT_INPUT;
strcpy(grabInfo.actionName, "grab_object");
strcpy(grabInfo.localizedActionName, "Grab Object");
grabInfo.countSubactionPaths = 2;
XrPath handPaths[2];
xrStringToPath(instance, "/user/hand/left", &handPaths[0]);
xrStringToPath(instance, "/user/hand/right", &handPaths[1]);
grabInfo.subactionPaths = handPaths;
XrAction grabAction;
xrCreateAction(gameplaySet, &grabInfo, &grabAction);
```

#### Step 2: Suggest interaction profile bindings

We bind the grab action to the trigger on supported controllers:

```cpp
// Binding for Meta Quest Touch Pro
XrPath triggerPath;
xrStringToPath(instance, "/user/hand/right/input/squeeze/value", &triggerPath);

XrActionSuggestedBinding binding;
binding.action = grabAction;
binding.binding = triggerPath;

XrInteractionProfileSuggestedBinding profileBinding{
    XR_TYPE_INTERACTION_PROFILE_SUGGESTED_BINDING};
XrPath profilePath;
xrStringToPath(instance,
    "/interaction_profiles/oculus/touch_controller", &profilePath);
profileBinding.interactionProfile = profilePath;
profileBinding.suggestedBindings = &binding;
profileBinding.countSuggestedBindings = 1;
xrSuggestInteractionProfileBindings(instance, &profileBinding);
```

The binding path hierarchy:
- `/user/hand/right` — the subaction path (which hand)
- `/input/squeeze/value` — the component path (analog squeeze axis, range $[0.0, 1.0]$)

#### Step 3: Attach action set to session and sync

```cpp
// Attach to session (once, after session creation)
XrSessionActionSetsAttachInfo attachInfo{XR_TYPE_SESSION_ACTION_SETS_ATTACH_INFO};
attachInfo.countActionSets = 1;
attachInfo.actionSets = &gameplaySet;
xrAttachSessionActionSets(session, &attachInfo);

// Per-frame: sync actions
XrActiveActionSet activeSet{gameplaySet, XR_NULL_PATH};
XrActionsSyncInfo syncInfo{XR_TYPE_ACTIONS_SYNC_INFO};
syncInfo.countActiveActionSets = 1;
syncInfo.activeActionSets = &activeSet;
xrSyncActions(session, &syncInfo);
```

#### Step 4: Read the action state and apply threshold

```cpp
XrActionStateGetInfo getInfo{XR_TYPE_ACTION_STATE_GET_INFO};
getInfo.action = grabAction;
getInfo.subactionPath = handPaths[1]; // right hand

XrActionStateFloat grabState{XR_TYPE_ACTION_STATE_FLOAT};
xrGetActionStateFloat(session, &getInfo, &grabState);

// State fields after user squeezes trigger to 80%:
// grabState.isActive = XR_TRUE (binding is active)
// grabState.currentState = 0.80f (analog value)
// grabState.changedSinceLastSync = XR_TRUE
// grabState.lastChangeTime = 48372947261 (XrTime in nanoseconds)

const float GRAB_THRESHOLD = 0.7f;
bool isGrabbing = grabState.isActive &&
                  (grabState.currentState > GRAB_THRESHOLD);
```

#### Step 5: Complete data flow summary

$$
\text{Hardware} \xrightarrow{\text{USB/BT}} \text{Runtime} \xrightarrow{\text{xrSyncActions}} \text{Action State} \xrightarrow{\text{threshold}} \text{Game Event}
$$

| Stage | Latency | Data |
|-------|---------|------|
| Sensor ADC → firmware | ~1 ms | 12-bit analog sample |
| Firmware → Runtime (USB) | ~4 ms | HID report, normalized float |
| `xrSyncActions()` | ~0.1 ms | Copies to action state buffer |
| `xrGetActionStateFloat()` | ~0.01 ms | Returns `currentState = 0.80` |
| Threshold comparison | ~0 ms | `0.80 > 0.70` → grab = true |

**Final Answer:**

$$
t_{\text{trigger-to-grab}} \approx 5 \text{ ms (hardware + runtime)}, \quad \text{total motion-to-photon} \approx 20 \text{ ms}
$$

The action system decouples hardware specifics from game logic — the same `grabAction` works across Quest, Index, and WMR controllers via different interaction profile bindings.

</details>

### Example 28.2 — Fitts's Law for Hand-Tracking UI Button Placement

**Problem:** A VR menu button has width $W = 4$ cm and is placed at distance $D = 30$ cm from the user's resting hand position. Using Fitts's Law, compute the expected movement time. Then determine the minimum button size needed to achieve a target selection time of 400 ms, given empirical constants $a = 50$ ms, $b = 150$ ms/bit for hand tracking input.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: State Fitts's Law (Shannon formulation)

$$
MT = a + b \cdot \text{ID}
$$

where the Index of Difficulty is:

$$
\text{ID} = \log_2\left(\frac{2D}{W}\right)
$$

$MT$ = movement time (ms), $a$ = intercept (device start-up time), $b$ = slope (information processing rate), $D$ = distance to target center, $W$ = target width along movement axis.

#### Step 2: Compute ID for the given button

$$
\text{ID} = \log_2\left(\frac{2 \times 30}{4}\right) = \log_2(15) = \frac{\ln 15}{\ln 2} = \frac{2.708}{0.693} = 3.907 \text{ bits}
$$

#### Step 3: Compute movement time

$$
MT = 50 + 150 \times 3.907 = 50 + 586.1 = 636.1 \text{ ms}
$$

This is above the 400 ms target — the button is either too small or too far away.

#### Step 4: Solve for minimum button width at 400 ms target

Set $MT = 400$ and solve for $W$:

$$
400 = 50 + 150 \cdot \log_2\left(\frac{2 \times 30}{W}\right)
$$

$$
350 = 150 \cdot \log_2\left(\frac{60}{W}\right)
$$

$$
\log_2\left(\frac{60}{W}\right) = \frac{350}{150} = 2.333 \text{ bits}
$$

$$
\frac{60}{W} = 2^{2.333} = e^{2.333 \times 0.693} = e^{1.617} = 5.038
$$

$$
W = \frac{60}{5.038} = 11.91 \text{ cm}
$$

#### Step 5: Practical interpretation and design recommendation

A 11.9 cm button at 30 cm distance achieves 400 ms selection time. This is very large — nearly palm-sized. The alternatives:

**Option A:** Reduce distance. At $D = 15$ cm with $W = 4$ cm:

$$
\text{ID} = \log_2\left(\frac{30}{4}\right) = \log_2(7.5) = 2.907 \text{ bits}
$$

$$
MT = 50 + 150 \times 2.907 = 486 \text{ ms}
$$

Still above 400 ms, but closer.

**Option B:** Increase button size to 6 cm at $D = 15$ cm:

$$
\text{ID} = \log_2\left(\frac{30}{6}\right) = \log_2(5) = 2.322 \text{ bits}
$$

$$
MT = 50 + 150 \times 2.322 = 398 \text{ ms} \approx 400 \text{ ms ✓}
$$

#### Step 6: Account for hand-tracking noise

Hand tracking adds positional jitter of $\sigma \approx 3$ mm. The effective target width shrinks:

$$
W_{\text{eff}} = W - 2\sigma = 60 - 6 = 54 \text{ mm} = 5.4 \text{ cm}
$$

Recalculating Option B with noise:

$$
\text{ID} = \log_2\left(\frac{30}{5.4}\right) = \log_2(5.556) = 2.474 \text{ bits}
$$

$$
MT = 50 + 150 \times 2.474 = 421 \text{ ms}
$$

Still close to target. Add a 3 mm "magnetic snap" zone to compensate.

**Final Answer:**

$$
MT = 50 + 150 \cdot \log_2\left(\frac{2D}{W}\right) \text{ ms}
$$

$$
\text{Original config (4 cm at 30 cm): } MT = 636 \text{ ms (too slow)}
$$

$$
\text{Recommended: } W = 6 \text{ cm at } D = 15 \text{ cm} \implies MT \approx 400 \text{ ms ✓}
$$

Design rule: for hand-tracking UIs, place primary actions within 15–20 cm of rest position with minimum 5 cm hit targets.

</details>

---
