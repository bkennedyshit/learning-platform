---
title: "Xr Interaction"
subject: "scripts"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# 9.7 — XR Interaction Patterns & UX Heuristics

*Reference companion to [28.7 - Spatial Computing & Interaction Design](28.7---Spatial-Computing-&-Interaction-Design)*

---

## 1. Interaction Pattern Catalog

### 1.1 Ray Casting (Far-Field)

**When:** Target is beyond arm's reach (> 0.7m)
**How:** Controller/hand emits a visible ray; intersection with scene geometry determines target.

**Implementation checklist:**
- [ ] Ray origin: controller tip or between thumb/index for hand tracking
- [ ] Ray visualization: thin line (1–2mm) with endpoint reticle
- [ ] Haptic pulse on hover (0.1 amplitude, 10ms)
- [ ] Curved ray (parabolic) for teleportation targeting
- [ ] Sticky ray: once locked on target, small movements don't break selection

**Anti-patterns:**
- ❌ Invisible ray (user can't aim)
- ❌ Ray from head/eye (conflicts with gaze interaction)
- ❌ No hover feedback (user doesn't know what's selectable)

### 1.2 Direct Grab (Near-Field)

**When:** Object is within arm's reach
**How:** Hand/controller overlaps object collider; grip button or pinch gesture initiates grab.

**Grab types:**
| Type | Behavior | Use Case |
|------|----------|----------|
| **Snap** | Object jumps to predefined grip pose | Tools, weapons |
| **Direct** | Object maintains relative offset from hand | Inspection, placement |
| **Distance** | Object pulled toward hand from afar | Hybrid ray+grab |

**Implementation:**
```
onGripPress:
  if (overlapping interactable):
    attach object to hand
    disable object physics
    play haptic (0.3, 50ms)
    
onGripRelease:
  detach object
  apply hand velocity to object (throw)
  re-enable physics
```

### 1.3 Poke / Push (UI Buttons)

**When:** Flat UI surfaces (menus, keyboards)
**How:** Fingertip or controller tip crosses button surface plane.

**Requirements:**
- Button depth: 1–2cm travel before activation
- Visual depression animation
- Audio click feedback
- Haptic pulse at activation point
- Prevent accidental activation: require 0.5cm penetration minimum

### 1.4 Two-Handed Manipulation

**When:** Scaling, rotating large objects
**How:** Both hands grab simultaneously; relative hand movement maps to transform.

**Mapping:**
- **Distance between hands** → uniform scale
- **Midpoint** → object position
- **Rotation between hands** → object rotation (around midpoint)

---

## 2. Locomotion Patterns

### 2.1 Teleportation (Recommended Default)

```javascript
// WebXR teleportation implementation sketch
function updateTeleport(frame, refSpace, inputSource) {
    if (!inputSource.gamepad.buttons[4].pressed) return; // thumbstick click

    // Cast parabolic arc from controller
    const pose = frame.getPose(inputSource.targetRaySpace, refSpace);
    const origin = pose.transform.position;
    const direction = getForwardFromMatrix(pose.transform.matrix);

    const arc = computeParabolicArc(origin, direction, gravity, maxDistance);
    const hitPoint = raycastArc(arc, navMesh);

    if (hitPoint) {
        renderTeleportArc(arc, hitPoint);  // visual feedback
        renderDestinationMarker(hitPoint);

        if (inputSource.gamepad.buttons[4].released) {
            // Instant teleport (no smooth transition)
            setPlayerPosition(hitPoint);
            fadeFromBlack(200); // brief fade to reduce disorientation
        }
    }
}
```

**Best practices:**
- Show destination marker with orientation indicator
- Fade-to-black transition (100–200ms) reduces disorientation
- Restrict to navigation mesh (prevent teleporting through walls)
- Optional: show ghost avatar at destination before confirming

### 2.2 Continuous Movement with Comfort Vignette

```csharp
// Unity: Dynamic FOV restriction during movement
public class ComfortVignette : MonoBehaviour
{
    [SerializeField] private Material vignetteMaterial;
    [SerializeField] private float restrictedFOV = 60f;
    [SerializeField] private float transitionSpeed = 8f;

    private float currentRestriction = 0f;

    void Update()
    {
        float speed = playerRigidbody.velocity.magnitude;
        float targetRestriction = Mathf.Clamp01(speed / maxSpeed);

        currentRestriction = Mathf.Lerp(currentRestriction, targetRestriction,
            Time.deltaTime * transitionSpeed);

        vignetteMaterial.SetFloat("_VignetteIntensity", currentRestriction);
    }
}
```

---

## 3. UX Heuristics for Spatial Interfaces

### 3.1 The 10 Spatial Design Principles

1. **Respect the body:** Place interactions within comfortable reach zones
2. **Leverage proprioception:** Users know where their hands are without looking
3. **Provide spatial audio cues:** Sound localization aids attention direction
4. **Maintain stable references:** At least one element should be world-anchored
5. **Minimize cognitive load:** Max 3–5 interactive elements visible simultaneously
6. **Use progressive disclosure:** Reveal complexity on demand (hover → expand)
7. **Ensure reversibility:** Every action should be undoable (grab → release returns object)
8. **Communicate affordances:** Interactable objects should look interactable (glow, outline)
9. **Respect personal space:** UI elements should not be closer than 0.5m to the face
10. **Design for accessibility:** Support multiple input modalities (controller, hand, gaze+dwell)

### 3.2 Comfort Guidelines (Quantified)

| Parameter | Comfortable | Acceptable | Avoid |
|-----------|-------------|------------|-------|
| Frame rate | ≥ 90 Hz | 72 Hz | < 60 Hz |
| Motion-to-photon | < 20 ms | < 30 ms | > 50 ms |
| Text distance | 1–3 m | 0.5–5 m | < 0.3 m |
| Button size | > 4 cm | > 2 cm | < 1 cm |
| UI vertical range | -30° to +20° | -45° to +30° | > 45° up |
| Locomotion speed | < 2 m/s | < 4 m/s | > 6 m/s |
| Rotation speed | Snap (45°) | < 60°/s smooth | > 120°/s |

### 3.3 Hand Tracking Gesture Library

| Gesture | Detection | Action |
|---------|-----------|--------|
| **Pinch** | Thumb-index distance < 2cm | Select / grab |
| **Point** | Index extended, others curled | Ray cast direction |
| **Open palm** | All fingers extended, palm facing user | Menu summon |
| **Fist** | All fingers curled | Dismiss / cancel |
| **Thumbs up** | Thumb extended upward | Confirm / approve |
| **Two-finger pinch** | Both hands pinching | Scale / zoom |

---

## 4. OpenXR Reference Space Hierarchy

```
XR_REFERENCE_SPACE_TYPE_VIEW
  └── Attached to head (HMD). Moves with user.
      Use: Head-locked UI (sparingly)

XR_REFERENCE_SPACE_TYPE_LOCAL
  └── Origin at initial head position. Seated experiences.
      Use: Cockpit games, seated productivity

XR_REFERENCE_SPACE_TYPE_STAGE
  └── Origin at floor center of play area. Room-scale.
      Use: Standing/walking experiences, room-scale VR

XR_REFERENCE_SPACE_TYPE_UNBOUNDED (extension)
  └── Large-scale tracking (AR, warehouse-scale)
      Use: AR applications, large venue VR
```

---

## 5. Performance Checklist for XR Applications

- [ ] **Single-pass stereo rendering** enabled (halves vertex processing)
- [ ] **Foveated rendering** active (reduces peripheral fragment cost by 50%)
- [ ] **Late-latching** for head pose (reduces motion-to-photon by 1 frame)
- [ ] **Reprojection** configured as safety net (ASW/ATW/SpaceWarp)
- [ ] **Draw calls** < 100 (mobile) / < 2000 (PC)
- [ ] **Overdraw** < 2x average
- [ ] **Texture compression** (ASTC on mobile, BC7 on PC)
- [ ] **Occlusion culling** enabled for architectural scenes
- [ ] **LOD system** with 3+ levels per complex object
- [ ] **Fixed foveated rendering** tier 2+ on Quest


---

## Related Notes
- [9.4_shader_examples](9.4_shader_examples) - Shared review/3d/reference focus
- [9.5_engine_skeletons](9.5_engine_skeletons) - Shared review/3d/reference focus
- [29.2 - Immersive App Architectures - OpenXR, WebXR, Unity XR, Unreal XR](29.2---Immersive-App-Architectures---OpenXR,-WebXR,-Unity-XR,-Unreal-XR) - Shared openxr/webxr focus
- [LEARNING_PATH](LEARNING_PATH) - Shared openxr/webxr focus
