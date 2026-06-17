---
title: "26.4 — 3D Game Patterns: Transforms, Animation, Physics"
subject: "Game Dev"
catalog: advanced
audience_tier: higher-education
chapter: "26.4"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 26.4 — 3D Game Patterns: Transforms, Animation, Physics

> *"The first 90 percent of the code accounts for the first 90 percent of the development time. The remaining 10 percent of the code accounts for the other 90 percent of the development time."* — Tom Cargill (applied to 3D game physics by every engine programmer ever)

3D game programming is where linear algebra meets real-time constraints. Transform hierarchies, quaternion rotations, skeletal animation blending, and rigid body physics are the core systems. Your architecture/3D background is a massive advantage here — you already think in spatial terms. This chapter bridges that intuition to game engine implementation.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Implement **TRS (Translation-Rotation-Scale) transform hierarchies** with parent-child relationships.
2. Use **quaternions** for rotation (avoiding gimbal lock) in game contexts.
3. Implement **skeletal animation** with bone hierarchies and skinning.
4. Build **animation blend trees** for smooth locomotion transitions.
5. Implement **raycasting** for selection, shooting, and ground detection.
6. Understand the **3D physics pipeline** (broad phase → narrow phase → solver).
7. Implement **character controllers** that interact with physics without being fully simulated.

---

## 🖼️ Visual Anchor — Transform Hierarchy & Skeletal Animation

![gamedev__4.4-fig1](gamedev__4.4-fig1.svg)

---

## 📚 1. Concepts & Definitions

### Definition 26.4.1 — Transform (TRS Matrix)

A **transform** encodes an object's position, rotation, and scale in a 4×4 homogeneous matrix:

$$
M = T \cdot R \cdot S = \begin{pmatrix} R_{00}s_x & R_{01}s_y & R_{02}s_z & t_x \\ R_{10}s_x & R_{11}s_y & R_{12}s_z & t_y \\ R_{20}s_x & R_{21}s_y & R_{22}s_z & t_z \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

**World transform** of a child = Parent.WorldMatrix × Child.LocalMatrix. This is why transform hierarchies exist: moving a parent moves all children.

### Definition 26.4.2 — Quaternion Rotation

A **quaternion** $q = w + xi + yj + zk$ represents a rotation of angle $\theta$ around axis $\hat{n}$:

$$
q = \cos\frac{\theta}{2} + \sin\frac{\theta}{2}(n_x i + n_y j + n_z k)
$$

**Why quaternions over Euler angles:**
- No gimbal lock
- Smooth interpolation (SLERP)
- Compact (4 floats vs 3×3 matrix)
- Composable: $q_{\text{combined}} = q_2 \cdot q_1$

### Definition 26.4.3 — Skeletal Animation

A **skeleton** is a hierarchy of bones (transforms). Each bone stores a local transform relative to its parent. **Skinning** deforms mesh vertices based on bone transforms:

$$
v_{\text{world}} = \sum_{i=0}^{n} w_i \cdot M_{\text{bone}_i} \cdot M_{\text{bind}_i}^{-1} \cdot v_{\text{bind}}
$$

Where $w_i$ = bone weight (sum to 1.0), $M_{\text{bone}_i}$ = current bone world transform, $M_{\text{bind}_i}^{-1}$ = inverse bind pose.

### Definition 26.4.4 — Raycast

A **raycast** tests a ray (origin + direction) against scene geometry, returning the first hit point, normal, and object:

$$
P(t) = \text{origin} + t \cdot \text{direction}, \quad t \geq 0
$$

Uses: shooting, ground detection, line-of-sight, mouse picking, IK foot placement.

### Definition 26.4.5 — Rigid Body Dynamics

A **rigid body** is a physics-simulated object with mass, velocity, and angular velocity. The physics engine applies:

$$
F = ma \implies a = \frac{F}{m}, \quad v_{n+1} = v_n + a \cdot \Delta t, \quad x_{n+1} = x_n + v_{n+1} \cdot \Delta t
$$

For rotation: $\tau = I\alpha$ where $\tau$ = torque, $I$ = inertia tensor, $\alpha$ = angular acceleration.

---

## 🧩 2. Mental Models / Architecture

### Model 2.1 — Transform Hierarchy as Scene Graph

```
World Root
├── Player (pos: 0,0,0)
│   ├── Body (pos: 0,1,0 local)
│   │   ├── Head (pos: 0,0.5,0 local)
│   │   │   └── Camera (pos: 0,0.2,0.1 local)
│   │   ├── LeftArm (pos: -0.3,0.3,0 local)
│   │   │   └── LeftHand
│   │   │       └── Weapon (attached)
│   │   └── RightArm
│   └── Shadow (billboard, always flat)
├── Environment
│   ├── Terrain
│   └── Buildings[]
└── NPCs[]
```

Moving "Player" moves everything underneath. Rotating "Body" rotates arms, head, weapon — but not the shadow.

### Model 2.2 — Animation State Machine

```
                    ┌─────────┐
         speed>0.1  │         │  speed<0.1
    ┌──────────────→│  Walk   │←──────────────┐
    │               │ (blend) │               │
┌───┴───┐           └────┬────┘           ┌───┴───┐
│ Idle  │                │ speed>5        │ Idle  │
└───────┘                ▼                └───────┘
                    ┌─────────┐
                    │   Run   │
                    │ (blend) │
                    └────┬────┘
                         │ jump_trigger
                         ▼
                    ┌─────────┐
                    │  Jump   │──→ grounded → Idle/Walk
                    └─────────┘
```

**Blend trees** interpolate between animations based on parameters (speed, direction) rather than hard transitions.

### Model 2.3 — Physics Object Categories

| Type | Simulated? | Moves? | Use Case |
|------|-----------|--------|----------|
| **Static** | No | No | Terrain, walls, buildings |
| **Dynamic** | Yes | Yes | Crates, ragdolls, projectiles |
| **Kinematic** | No (manual) | Yes | Moving platforms, elevators |
| **Character Controller** | Partial | Yes | Player (custom movement + collision) |
| **Trigger** | No | No | Zones (damage, dialogue, checkpoint) |

---

## 🔑 3. Mechanics

### Mechanic 3.1 — Character Controller (Not a Rigid Body)

Players should NOT be full rigid bodies (they'd slide on slopes, bounce off walls, tumble). Instead, use a **character controller** — a capsule that sweeps through the world:

1. Apply input → desired velocity
2. **Sweep** capsule along desired direction
3. If hit: **slide** along surface (project velocity onto surface tangent)
4. Apply gravity separately (grounded check via short downward raycast)
5. Handle slopes: walk up gentle slopes, slide down steep ones

### Mechanic 3.2 — Animation Blending

**1D Blend Tree:** Interpolate between animations based on one parameter:
- Speed 0 → Idle
- Speed 0–3 → Lerp(Idle, Walk, speed/3)
- Speed 3–8 → Lerp(Walk, Run, (speed-3)/5)

**2D Blend Tree:** Two parameters (speed + direction):
- Uses Cartesian or polar coordinates
- Gradient band interpolation between surrounding samples

**Additive Blending:** Layer animations on top of base:
- Base: locomotion (full body)
- Additive: breathing (chest only, masked)
- Additive: aim offset (upper body, masked)

### Mechanic 3.3 — Inverse Kinematics (IK)

**IK** solves "where should the bones be so the end effector reaches this target?" Used for:
- Foot placement on uneven terrain
- Hand reaching for objects
- Head/eye look-at
- VR hand tracking → arm pose

**Two-bone IK** (arm/leg): analytical solution using law of cosines.
**FABRIK** (multi-bone chains): iterative, fast, handles constraints.

---

## 💻 4. Code Patterns & Examples

### 26.1 C# — Unity Character Controller

```csharp
[RequireComponent(typeof(CharacterController))]
public class FPSController : MonoBehaviour
{
    [SerializeField] private float walkSpeed = 5f;
    [SerializeField] private float runSpeed = 9f;
    [SerializeField] private float jumpForce = 7f;
    [SerializeField] private float gravity = -20f;
    [SerializeField] private float groundCheckDist = 0.2f;
    [SerializeField] private LayerMask groundMask;
    
    private CharacterController cc;
    private Vector3 velocity;
    private bool isGrounded;
    private Transform cameraTransform;
    
    void Start()
    {
        cc = GetComponent<CharacterController>();
        cameraTransform = Camera.main.transform;
    }
    
    void Update()
    {
        // Ground check (spherecast from feet)
        isGrounded = Physics.CheckSphere(
            transform.position + Vector3.down * (cc.height / 2f),
            groundCheckDist, groundMask);
        
        if (isGrounded && velocity.y < 0)
            velocity.y = -2f; // Small downward force to stay grounded
        
        // Movement input (relative to camera facing)
        float h = Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");
        Vector3 moveDir = cameraTransform.right * h + cameraTransform.forward * v;
        moveDir.y = 0;
        moveDir.Normalize();
        
        float speed = Input.GetKey(KeyCode.LeftShift) ? runSpeed : walkSpeed;
        cc.Move(moveDir * speed * Time.deltaTime);
        
        // Jump
        if (Input.GetButtonDown("Jump") && isGrounded)
            velocity.y = jumpForce;
        
        // Gravity
        velocity.y += gravity * Time.deltaTime;
        cc.Move(velocity * Time.deltaTime);
    }
}
```

### 26.2 C++ — Unreal: Raycasting for Interaction

```cpp
void AMyCharacter::PerformInteractionRaycast()
{
    FVector Start = CameraComponent->GetComponentLocation();
    FVector End = Start + CameraComponent->GetForwardVector() * InteractionRange;
    
    FHitResult HitResult;
    FCollisionQueryParams Params;
    Params.AddIgnoredActor(this);
    
    bool bHit = GetWorld()->LineTraceSingleByChannel(
        HitResult, Start, End, ECC_Visibility, Params);
    
    if (bHit)
    {
        AActor* HitActor = HitResult.GetActor();
        if (IInteractable* Interactable = Cast<IInteractable>(HitActor))
        {
            // Show interaction prompt
            ShowPrompt(Interactable->GetInteractionText());
            
            if (bInteractPressed)
                Interactable->Interact(this);
        }
        
        // Debug visualization
        DrawDebugLine(GetWorld(), Start, HitResult.ImpactPoint,
            FColor::Green, false, 0.1f);
        DrawDebugSphere(GetWorld(), HitResult.ImpactPoint, 5.f,
            8, FColor::Red, false, 0.1f);
    }
}
```

### 26.3 C# — Animation Blend Tree Controller

```csharp
public class LocomotionAnimator : MonoBehaviour
{
    private Animator animator;
    private static readonly int SpeedHash = Animator.StringToHash("Speed");
    private static readonly int DirectionHash = Animator.StringToHash("Direction");
    private static readonly int IsGroundedHash = Animator.StringToHash("IsGrounded");
    private static readonly int JumpHash = Animator.StringToHash("Jump");
    
    private float currentSpeed;
    private float speedSmoothVelocity;
    
    void Update()
    {
        // Smooth speed parameter (prevents animation snapping)
        float targetSpeed = new Vector2(Input.GetAxis("Horizontal"),
            Input.GetAxis("Vertical")).magnitude;
        
        currentSpeed = Mathf.SmoothDamp(
            currentSpeed, targetSpeed, ref speedSmoothVelocity, 0.1f);
        
        animator.SetFloat(SpeedHash, currentSpeed);
        animator.SetFloat(DirectionHash, Input.GetAxis("Horizontal"));
        animator.SetBool(IsGroundedHash, controller.isGrounded);
        
        if (Input.GetButtonDown("Jump"))
            animator.SetTrigger(JumpHash);
    }
}
```

---

## 🧮 5. Worked Examples

### Example 26.4.1 — Compute World Transform of Nested Object

**Problem:** A weapon is attached to a character's right hand. The character is at world position (5, 0, 3), rotated 90° around Y. The hand bone is at local offset (0.3, 1.2, 0.1) from the character root. The weapon has local offset (0, 0, 0.5) from the hand. What is the weapon's world position?

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1: Character world matrix**

Rotation 90° around Y:

$$
R_Y(90°) = \begin{pmatrix} 0 & 0 & 1 \\ 0 & 1 & 0 \\ -1 & 0 & 0 \end{pmatrix}
$$

Character world position: $(5, 0, 3)$

**Step 2: Hand world position**

Hand local offset: $(0.3, 1.2, 0.1)$

Apply character rotation to hand offset:

$$
R_Y \cdot \begin{pmatrix}0.3\\1.2\\0.1\end{pmatrix} = \begin{pmatrix}0 \cdot 0.3 + 0 \cdot 1.2 + 1 \cdot 0.1\\0 \cdot 0.3 + 1 \cdot 1.2 + 0 \cdot 0.1\\-1 \cdot 0.3 + 0 \cdot 1.2 + 0 \cdot 0.1\end{pmatrix} = \begin{pmatrix}0.1\\1.2\\-0.3\end{pmatrix}
$$

Hand world position: $(5 + 0.1, 0 + 1.2, 3 + (-0.3)) = (5.1, 1.2, 2.7)$

**Step 3: Weapon world position**

Weapon local offset from hand: $(0, 0, 0.5)$

Apply character rotation (hand inherits parent rotation):

$$
R_Y \cdot \begin{pmatrix}0\\0\\0.5\end{pmatrix} = \begin{pmatrix}0.5\\0\\0\end{pmatrix}
$$

Weapon world position: $(5.1 + 0.5, 1.2 + 0, 2.7 + 0) = (5.6, 1.2, 2.7)$

**Verification:** The weapon points in the character's local +Z direction, which after 90° Y rotation becomes world +X. The 0.5 offset in local Z correctly becomes 0.5 in world X. ✓

</details>

### Example 26.4.2 — SLERP for Smooth Rotation

**Problem:** A turret must rotate from facing North (0°) to facing East (90°) over 2 seconds. Implement quaternion SLERP to avoid gimbal lock and ensure constant angular velocity.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```csharp
public class TurretRotation : MonoBehaviour
{
    private Quaternion startRot;
    private Quaternion endRot;
    private float duration = 2f;
    private float elapsed = 0f;
    private bool isRotating = false;
    
    public void RotateToTarget(Vector3 targetDirection)
    {
        startRot = transform.rotation;
        endRot = Quaternion.LookRotation(targetDirection, Vector3.up);
        elapsed = 0f;
        isRotating = true;
    }
    
    void Update()
    {
        if (!isRotating) return;
        
        elapsed += Time.deltaTime;
        float t = Mathf.Clamp01(elapsed / duration);
        
        // SLERP: Spherical Linear Interpolation
        // Constant angular velocity (unlike Lerp which slows at endpoints)
        transform.rotation = Quaternion.Slerp(startRot, endRot, t);
        
        if (t >= 1f) isRotating = false;
    }
}
```

**Why SLERP over Euler interpolation:**

Euler: Interpolating (0,0,0) → (0,90,0) works fine. But (0,89,0) → (0,91,0) might flip through (180,91,180) due to gimbal lock near ±90° pitch.

SLERP: Always takes the shortest arc on the unit quaternion hypersphere. Constant angular velocity. No singularities.

$$
\text{slerp}(q_0, q_1, t) = q_0 \cdot \frac{\sin((1-t)\theta)}{\sin\theta} + q_1 \cdot \frac{\sin(t\theta)}{\sin\theta}
$$

Where $\theta = \arccos(q_0 \cdot q_1)$ (dot product of quaternions).

</details>

---

## ⚠️ 6. Gotchas & Anti-Patterns

### ❌ Anti-Pattern: Euler Angles for Runtime Rotation

Store and manipulate rotations as quaternions. Convert to Euler only for inspector display. Euler angles suffer from gimbal lock, order-dependence (XYZ vs ZYX), and discontinuities.

### ❌ Anti-Pattern: Scaling in Transform Hierarchies

Non-uniform scale in parent transforms causes **shear** in children. Physics engines don't support sheared colliders. Rule: only apply scale at leaf nodes, or use uniform scale only.

### ❌ Anti-Pattern: Moving Rigidbodies via Transform

```csharp
// BAD: teleports the physics body, breaks collision detection
transform.position = newPos;

// GOOD: use physics API
rb.MovePosition(newPos);        // Kinematic
rb.AddForce(force);             // Dynamic
rb.velocity = desiredVelocity;  // Direct (use sparingly)
```

### ❌ Anti-Pattern: Raycasting Every Frame for Everything

Raycasts are expensive (traverse BVH tree). Cache results, use layer masks to limit checks, and spread expensive queries across frames.

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- **Previous:** [26.3 - 2D Game Patterns - Sprites, Tilemaps, Physics](26.3---2D-Game-Patterns---Sprites,-Tilemaps,-Physics)
- **Next:** [26.5 - Save Systems & Serialization](26.5---Save-Systems-&-Serialization)
- **Quaternion math:** [28.2 - Quaternions & Rotations](28.2---Quaternions-&-Rotations) — full derivation and proofs
- **3D fundamentals:** [28.1 - 3D Math Fundamentals](28.1---3D-Math-Fundamentals) — vectors, matrices, coordinate systems
- **Rigid body math:** [26.7 - Rigid Body Dynamics & Euler Angles](26.7---Rigid-Body-Dynamics-&-Euler-Angles) (math track)
- **Engine architecture:** [28.5 - Game Engine Architectures - Unity & Unreal](28.5---Game-Engine-Architectures---Unity-&-Unreal)

### External Resources
- **Game Engine Architecture** (Jason Gregory) — Chapter 11: Animation Systems
- **Real-Time Collision Detection** (Christer Ericson) — GJK, EPA, BVH
- **Sebastian Lague: "Procedural Animation"** — IK and procedural motion
- **GDC: "Animation Bootcamp"** — annual talks on animation systems
- **Jolt Physics** (github.com/jrouwe/JoltPhysics) — modern C++ physics engine, excellent code to study

### Practice
- `_practice/scripts/4.4_transforms.py` — matrix multiplication and quaternion exercises



---

## 🔬 8. Advanced Topics — Skeletal Animation, Physics Constraints & Ragdoll Systems

### 8.1 — Skeletal Animation: Matrix Palette Skinning

Skeletal animation deforms a mesh by transforming each vertex according to a weighted blend of bone matrices. The GPU performs this transformation using a **matrix palette** — an array of bone matrices uploaded as a uniform buffer.

#### The Skinning Pipeline

1. **Bind Pose (T-pose):** The mesh is authored in a reference pose. Each bone has an **inverse bind matrix** $B_i^{-1}$ that transforms vertices from model space to bone-local space.

2. **Animation Pose:** At runtime, each bone has a **world matrix** $W_i$ representing its current animated position.

3. **Final Bone Matrix:** The matrix that transforms a vertex from bind pose to animated pose:

$$
M_i = W_i \cdot B_i^{-1}
$$

4. **Vertex Skinning:** Each vertex is influenced by up to 4 bones with weights $w_j$ (summing to 1):

$$
v' = \sum_{j=0}^{3} w_j \cdot M_{bone_j} \cdot v
$$

#### GPU Implementation (Vertex Shader)

```cpp
// HLSL vertex shader for matrix palette skinning
cbuffer BoneMatrices : register(b1)
{
    float4x4 bones[256];  // Matrix palette (max 256 bones)
};

struct VertexInput
{
    float3 position : POSITION;
    float3 normal : NORMAL;
    float2 uv : TEXCOORD0;
    uint4 boneIndices : BLENDINDICES;  // Which 4 bones affect this vertex
    float4 boneWeights : BLENDWEIGHT;  // How much each bone contributes
};

struct VertexOutput
{
    float4 position : SV_POSITION;
    float3 worldNormal : NORMAL;
    float2 uv : TEXCOORD0;
};

VertexOutput VS_Skinned(VertexInput input)
{
    VertexOutput output;
    
    // Compute skinned position (blend of 4 bone transforms)
    float4 skinnedPos = float4(0, 0, 0, 0);
    float3 skinnedNormal = float3(0, 0, 0);
    
    for (int i = 0; i < 4; i++)
    {
        float weight = input.boneWeights[i];
        if (weight <= 0.0) continue;
        
        uint boneIdx = input.boneIndices[i];
        float4x4 boneMatrix = bones[boneIdx];
        
        skinnedPos += weight * mul(boneMatrix, float4(input.position, 1.0));
        skinnedNormal += weight * mul((float3x3)boneMatrix, input.normal);
    }
    
    output.position = mul(viewProjection, skinnedPos);
    output.worldNormal = normalize(skinnedNormal);
    output.uv = input.uv;
    
    return output;
}
```

#### Dual Quaternion Skinning (DQS)

Standard linear blend skinning (LBS) suffers from **volume loss** at joints (the "candy wrapper" artifact when twisting). Dual quaternion skinning preserves volume:

```cpp
// Dual quaternion skinning — preserves volume during twists
struct DualQuat
{
    float4 real;  // Rotation quaternion
    float4 dual;  // Translation encoded as dual part
};

float4 DQS_SkinPosition(float3 pos, uint4 indices, float4 weights, 
                          StructuredBuffer<DualQuat> boneDQs)
{
    // Blend dual quaternions (with antipodality check)
    DualQuat blended;
    blended.real = float4(0, 0, 0, 0);
    blended.dual = float4(0, 0, 0, 0);
    
    // Ensure all quaternions are in the same hemisphere
    float sign0 = 1.0;
    DualQuat dq0 = boneDQs[indices[0]];
    
    for (int i = 0; i < 4; i++)
    {
        float w = weights[i];
        if (w <= 0.0) continue;
        
        DualQuat dq = boneDQs[indices[i]];
        
        // Antipodality: flip if dot product with first bone is negative
        float sign = (dot(dq.real, dq0.real) < 0.0) ? -1.0 : 1.0;
        
        blended.real += w * sign * dq.real;
        blended.dual += w * sign * dq.dual;
    }
    
    // Normalize the blended dual quaternion
    float len = length(blended.real);
    blended.real /= len;
    blended.dual /= len;
    
    // Transform position using dual quaternion
    float3 t = 2.0 * (blended.real.w * blended.dual.xyz - blended.dual.w * blended.real.xyz 
                       + cross(blended.real.xyz, blended.dual.xyz));
    float3 rotated = pos + 2.0 * cross(blended.real.xyz, cross(blended.real.xyz, pos) 
                                         + blended.real.w * pos);
    
    return float4(rotated + t, 1.0);
}
```

#### Animation Blending

Multiple animations are blended using a **blend tree** (1D, 2D, or direct):

```csharp
// 1D blend: walk speed controls blend between idle/walk/run
public class AnimationBlender
{
    // Each bone's final pose = weighted sum of animation poses
    public BonePose BlendPoses(BonePose[] posesA, BonePose[] posesB, float alpha)
    {
        var result = new BonePose[posesA.Length];
        
        for (int i = 0; i < posesA.Length; i++)
        {
            result[i].localPosition = Vector3.Lerp(posesA[i].localPosition, 
                                                    posesB[i].localPosition, alpha);
            result[i].localRotation = Quaternion.Slerp(posesA[i].localRotation, 
                                                        posesB[i].localRotation, alpha);
            result[i].localScale = Vector3.Lerp(posesA[i].localScale, 
                                                 posesB[i].localScale, alpha);
        }
        
        return result;
    }
    
    // Additive blending: layer an animation ON TOP of a base
    // Used for: breathing on top of any pose, hit reactions, aim offsets
    public BonePose[] AdditiveBlend(BonePose[] basePose, BonePose[] additivePose, float weight)
    {
        var result = new BonePose[basePose.Length];
        
        for (int i = 0; i < basePose.Length; i++)
        {
            // Additive = base + (additive - reference) * weight
            // Where reference is the first frame of the additive clip
            Quaternion additiveRot = Quaternion.Slerp(
                Quaternion.identity, additivePose[i].localRotation, weight);
            
            result[i].localRotation = basePose[i].localRotation * additiveRot;
            result[i].localPosition = basePose[i].localPosition + 
                                       additivePose[i].localPosition * weight;
        }
        
        return result;
    }
}
```

---

### 8.2 — Physics Constraints: Hinge, Ball-Joint & Slider

Physics constraints restrict the relative motion between two rigid bodies. They are the building blocks of ragdolls, vehicles, doors, and mechanical systems.

#### Constraint Formulation

A constraint is a function $C(x)$ that must equal zero:

$$
C(x) = 0 \quad \text{(equality constraint, e.g., hinge)}
$$

$$
C(x) \geq 0 \quad \text{(inequality constraint, e.g., contact)}
$$

The constraint solver computes impulses (or position corrections) to satisfy these constraints each frame.

#### Hinge Joint (Revolute)

Allows rotation around a single axis. Constrains 5 degrees of freedom (3 translation + 2 rotation), leaving 1 rotational DOF free.

```csharp
public class HingeConstraint
{
    public Rigidbody bodyA, bodyB;
    public Vector3 anchorA, anchorB;  // Local-space anchor points
    public Vector3 axisA;             // Hinge axis in bodyA's local space
    
    // Optional limits
    public float minAngle = -90f;
    public float maxAngle = 90f;
    public bool useLimits = true;
    
    // Optional motor
    public float motorSpeed = 0f;      // Target angular velocity (rad/s)
    public float maxMotorTorque = 100f;
    public bool useMotor = false;
    
    public void SolvePositionConstraint()
    {
        // 1. Point constraint: anchor points must coincide in world space
        Vector3 worldAnchorA = bodyA.transform.TransformPoint(anchorA);
        Vector3 worldAnchorB = bodyB.transform.TransformPoint(anchorB);
        
        Vector3 error = worldAnchorB - worldAnchorA;
        
        // Apply position correction (split between bodies based on mass ratio)
        float totalInvMass = 1f / bodyA.mass + 1f / bodyB.mass;
        Vector3 correction = error / totalInvMass;
        
        bodyA.position += correction / bodyA.mass;
        bodyB.position -= correction / bodyB.mass;
        
        // 2. Axis alignment: hinge axes must be parallel
        Vector3 worldAxisA = bodyA.transform.TransformDirection(axisA);
        Vector3 worldAxisB = bodyB.transform.TransformDirection(axisA); // Same axis
        
        Vector3 axisCross = Vector3.Cross(worldAxisA, worldAxisB);
        // Apply angular correction to align axes...
    }
    
    public void SolveVelocityConstraint(float dt)
    {
        if (useMotor)
        {
            // Compute current angular velocity difference along hinge axis
            Vector3 worldAxis = bodyA.transform.TransformDirection(axisA);
            float relativeAngVel = Vector3.Dot(bodyB.angularVelocity - bodyA.angularVelocity, worldAxis);
            
            // Motor impulse to reach target speed
            float motorImpulse = (motorSpeed - relativeAngVel) * GetEffectiveMass();
            motorImpulse = Mathf.Clamp(motorImpulse, -maxMotorTorque * dt, maxMotorTorque * dt);
            
            bodyA.angularVelocity -= worldAxis * motorImpulse / bodyA.inertiaTensor.magnitude;
            bodyB.angularVelocity += worldAxis * motorImpulse / bodyB.inertiaTensor.magnitude;
        }
    }
}
```

#### Ball-and-Socket Joint (Spherical)

Allows rotation around all 3 axes. Constrains only 3 translational DOFs — the anchor points must coincide.

```csharp
public class BallSocketConstraint
{
    public Rigidbody bodyA, bodyB;
    public Vector3 localAnchorA, localAnchorB;
    
    // Optional cone limit (restricts rotation to a cone)
    public float coneAngleLimit = 45f;  // degrees
    public Vector3 coneTwistAxis;       // Axis of the cone in bodyA space
    
    public void Solve(float dt)
    {
        // Position constraint: anchors must meet
        Vector3 worldA = bodyA.transform.TransformPoint(localAnchorA);
        Vector3 worldB = bodyB.transform.TransformPoint(localAnchorB);
        
        Vector3 error = worldB - worldA;
        
        // Baumgarte stabilization: add bias to prevent drift
        float beta = 0.2f; // Stabilization factor (0.1 - 0.3 typical)
        Vector3 bias = (beta / dt) * error;
        
        // Compute effective mass (Jacobian * inverse mass matrix * Jacobian^T)
        // For point constraint, this is simply sum of inverse masses
        // plus angular contribution from lever arms
        Vector3 rA = worldA - bodyA.worldCenterOfMass;
        Vector3 rB = worldB - bodyB.worldCenterOfMass;
        
        // Apply impulse to satisfy constraint...
    }
}
```

#### Slider Joint (Prismatic)

Allows translation along a single axis. Constrains 5 DOFs (2 translation + 3 rotation), leaving 1 translational DOF free.

```csharp
public class SliderConstraint
{
    public Rigidbody bodyA, bodyB;
    public Vector3 slideAxis;  // Local to bodyA
    public float minDistance = 0f;
    public float maxDistance = 5f;
    
    // Spring-damper for soft limits
    public float springStiffness = 1000f;
    public float damping = 50f;
    
    public void Solve(float dt)
    {
        Vector3 worldAxis = bodyA.transform.TransformDirection(slideAxis).normalized;
        
        // Current separation along slide axis
        Vector3 separation = bodyB.position - bodyA.position;
        float currentDistance = Vector3.Dot(separation, worldAxis);
        
        // Enforce limits
        if (currentDistance < minDistance)
        {
            float penetration = minDistance - currentDistance;
            ApplyLinearImpulse(worldAxis, penetration, dt);
        }
        else if (currentDistance > maxDistance)
        {
            float penetration = currentDistance - maxDistance;
            ApplyLinearImpulse(-worldAxis, penetration, dt);
        }
        
        // Constrain lateral movement (perpendicular to slide axis)
        Vector3 lateralError = separation - worldAxis * currentDistance;
        ApplyPositionCorrection(lateralError, dt);
        
        // Constrain all rotation (bodies cannot rotate relative to each other)
        Quaternion relativeRot = Quaternion.Inverse(bodyA.rotation) * bodyB.rotation;
        // Convert to axis-angle and apply angular correction...
    }
}
```

---

### 8.3 — Ragdoll Setup & Configuration

A ragdoll is a collection of rigid bodies (one per bone) connected by constraints that approximate human joint limits.

#### Ragdoll Bone Hierarchy

```yaml
# Typical humanoid ragdoll configuration
ragdoll:
  pelvis:
    shape: capsule(radius=0.12, height=0.25)
    mass: 15.0
    children:
      spine:
        joint: hinge(axis=X, min=-30, max=60)
        shape: capsule(radius=0.1, height=0.3)
        mass: 12.0
        children:
          chest:
            joint: hinge(axis=X, min=-30, max=30)
            shape: capsule(radius=0.12, height=0.25)
            mass: 10.0
            children:
              head:
                joint: ball_socket(cone=40)
                shape: sphere(radius=0.1)
                mass: 5.0
              left_upper_arm:
                joint: ball_socket(cone=90)
                shape: capsule(radius=0.05, height=0.28)
                mass: 3.0
                children:
                  left_forearm:
                    joint: hinge(axis=Y, min=0, max=150)
                    shape: capsule(radius=0.04, height=0.25)
                    mass: 2.0
              right_upper_arm:
                joint: ball_socket(cone=90)
                shape: capsule(radius=0.05, height=0.28)
                mass: 3.0
                children:
                  right_forearm:
                    joint: hinge(axis=Y, min=0, max=150)
                    shape: capsule(radius=0.04, height=0.25)
                    mass: 2.0
      left_thigh:
        joint: ball_socket(cone=80, twist=45)
        shape: capsule(radius=0.07, height=0.4)
        mass: 8.0
        children:
          left_shin:
            joint: hinge(axis=X, min=-140, max=0)
            shape: capsule(radius=0.05, height=0.38)
            mass: 5.0
      right_thigh:
        joint: ball_socket(cone=80, twist=45)
        shape: capsule(radius=0.07, height=0.4)
        mass: 8.0
        children:
          right_shin:
            joint: hinge(axis=X, min=-140, max=0)
            shape: capsule(radius=0.05, height=0.38)
            mass: 5.0
```

#### Animation-to-Ragdoll Transition (Blend)

```csharp
public class RagdollController : MonoBehaviour
{
    private Rigidbody[] ragdollBodies;
    private Collider[] ragdollColliders;
    private Animator animator;
    
    private bool isRagdoll = false;
    private float blendWeight = 0f;  // 0 = animation, 1 = ragdoll
    private float blendSpeed = 5f;
    
    public void ActivateRagdoll(Vector3 impactForce, Vector3 impactPoint)
    {
        isRagdoll = true;
        animator.enabled = false;
        
        foreach (var rb in ragdollBodies)
        {
            rb.isKinematic = false;
            // Transfer animation velocity to ragdoll
            rb.velocity = animator.velocity;
            rb.angularVelocity = animator.angularVelocity;
        }
        
        // Apply impact force to nearest body
        Rigidbody nearestBody = FindNearestBody(impactPoint);
        nearestBody.AddForceAtPosition(impactForce, impactPoint, ForceMode.Impulse);
    }
    
    public void DeactivateRagdoll()
    {
        // Blend from ragdoll pose back to animation (get-up animation)
        StartCoroutine(BlendToAnimation());
    }
    
    private IEnumerator BlendToAnimation()
    {
        // Store ragdoll pose
        var ragdollPose = CaptureCurrentPose();
        
        animator.enabled = true;
        animator.Play("GetUp");
        
        float elapsed = 0f;
        float blendDuration = 0.5f;
        
        while (elapsed < blendDuration)
        {
            elapsed += Time.deltaTime;
            float t = elapsed / blendDuration;
            
            // Blend each bone from ragdoll pose toward animation pose
            for (int i = 0; i < ragdollBodies.Length; i++)
            {
                Transform bone = ragdollBodies[i].transform;
                bone.position = Vector3.Lerp(ragdollPose[i].position, 
                                              GetAnimatedPosition(i), t);
                bone.rotation = Quaternion.Slerp(ragdollPose[i].rotation, 
                                                  GetAnimatedRotation(i), t);
            }
            
            yield return null;
        }
        
        // Fully animated now
        foreach (var rb in ragdollBodies)
            rb.isKinematic = true;
        
        isRagdoll = false;
    }
}
```

---

## 📎 9. Appendix — Mathematical Foundations

### Appendix 9.A — Quaternion SLERP vs. NLERP

Quaternion interpolation is essential for smooth rotation blending in animation and physics.

#### SLERP (Spherical Linear Interpolation)

SLERP traces a great arc on the 4D unit hypersphere, producing constant angular velocity:

$$
\text{slerp}(q_0, q_1, t) = \frac{\sin((1-t)\theta)}{\sin\theta} q_0 + \frac{\sin(t\theta)}{\sin\theta} q_1
$$

where $\theta = \arccos(q_0 \cdot q_1)$ is the angle between quaternions.

**Derivation:**

Given two unit quaternions $q_0$ and $q_1$ on the unit hypersphere $S^3$, we want to find the quaternion at parameter $t \in [0,1]$ along the shortest great arc.

The angle between them:

$$
\cos\theta = q_0 \cdot q_1 = q_{0w}q_{1w} + q_{0x}q_{1x} + q_{0y}q_{1y} + q_{0z}q_{1z}
$$

The interpolated quaternion must satisfy:
1. $\text{slerp}(q_0, q_1, 0) = q_0$
2. $\text{slerp}(q_0, q_1, 1) = q_1$
3. $|\text{slerp}(q_0, q_1, t)| = 1$ (remains on unit sphere)
4. Constant angular velocity: $\frac{d\theta}{dt} = \text{const}$

By analogy with linear interpolation on a circle (where $\text{lerp}$ on a circle uses $\sin$):

$$
\text{slerp}(q_0, q_1, t) = \frac{\sin((1-t)\theta)}{\sin\theta} q_0 + \frac{\sin(t\theta)}{\sin\theta} q_1
$$

**Edge cases:**
- When $\theta \approx 0$ (quaternions nearly identical): $\sin\theta \approx 0$, causing division by zero. Fall back to LERP + normalize.
- When $q_0 \cdot q_1 < 0$: quaternions are in opposite hemispheres. Negate one to take the short path: $q_1 \leftarrow -q_1$.

#### NLERP (Normalized Linear Interpolation)

NLERP simply linearly interpolates and renormalizes:

$$
\text{nlerp}(q_0, q_1, t) = \frac{(1-t)q_0 + t \cdot q_1}{|(1-t)q_0 + t \cdot q_1|}
$$

**Properties:**
- NOT constant angular velocity (accelerates in the middle, decelerates at ends)
- Commutative: $\text{nlerp}(a, b, t) = \text{nlerp}(b, a, 1-t)$
- Much cheaper to compute (no trig functions)
- Torque-minimal (shortest path in Euclidean sense, not angular sense)

#### Comparison

| Property | SLERP | NLERP |
|----------|-------|-------|
| Constant angular velocity | ✅ | ❌ |
| Computational cost | High (acos, sin, division) | Low (add, multiply, normalize) |
| Commutative | ✅ | ✅ |
| Shortest path | ✅ (great arc) | ✅ (chord, then project) |
| Use case | Cinematic cameras, precise timing | Animation blending, physics |

**When to use which:**
- **SLERP:** When constant rotation speed matters (camera interpolation, cutscenes, turret tracking)
- **NLERP:** When blending many quaternions (animation blend trees — cheaper and visually indistinguishable for small angles)

For animation blending where $\theta < 90°$ (typical), the difference between SLERP and NLERP is < 1° — imperceptible to players.

---

### Appendix 9.B — Impulse-Based vs. Constraint Solvers

Physics engines use two main approaches to resolve constraints (contacts, joints):

#### Impulse-Based (Sequential Impulse / PGS)

Used by: Box2D, Bullet Physics, PhysX, Jolt

The **Projected Gauss-Seidel (PGS)** method iteratively applies impulses to satisfy constraints one at a time, repeating until convergence:

**Algorithm:**

```
for iteration in 1..maxIterations:
    for each constraint C:
        // Compute constraint velocity error
        Cdot = J * v  (Jacobian times velocity vector)
        
        // Compute impulse magnitude
        lambda = -effectiveMass * (Cdot + bias)
        
        // Clamp impulse (e.g., contacts can only push, not pull)
        oldAccumulated = accumulatedImpulse[C]
        accumulatedImpulse[C] = clamp(oldAccumulated + lambda, min, max)
        lambda = accumulatedImpulse[C] - oldAccumulated
        
        // Apply impulse to bodies
        v_A -= invMass_A * J_A^T * lambda
        v_B += invMass_B * J_B^T * lambda
```

**Key insight:** Accumulated impulse clamping (Erin Catto's innovation in Box2D) ensures convergence even with conflicting constraints. Without it, individual impulses can oscillate.

**Convergence:** PGS converges linearly. More iterations = more accurate constraint satisfaction. Typical games use 4-8 velocity iterations + 2-4 position iterations.

**Effective Mass for a Contact Constraint:**

For a contact between bodies A and B at point $p$ with normal $\hat{n}$:

$$
m_{eff} = \frac{1}{\frac{1}{m_A} + \frac{1}{m_B} + \frac{(r_A \times \hat{n})^2}{I_A} + \frac{(r_B \times \hat{n})^2}{I_B}}
$$

where $r_A, r_B$ are vectors from each body's center of mass to the contact point.

#### Direct Solver (Featherstone / Reduced Coordinates)

Used by: MuJoCo, some robotics simulators

Instead of iterating, directly solve the full constraint system as a matrix equation:

$$
\begin{bmatrix} M & J^T \\ J & 0 \end{bmatrix} \begin{bmatrix} \dot{v} \\ \lambda \end{bmatrix} = \begin{bmatrix} f_{ext} \\ -\dot{C} \end{bmatrix}
$$

where $M$ is the mass matrix, $J$ is the constraint Jacobian, $\lambda$ are constraint forces.

**Advantages:** Exact solution in one step, no iteration count tuning.
**Disadvantages:** $O(n^3)$ for dense systems (impractical for games with thousands of contacts). Sparse solvers help but are still more expensive than PGS for typical game scenarios.

#### Comparison

| Aspect | PGS (Sequential Impulse) | Direct Solver |
|--------|-------------------------|---------------|
| Accuracy | Approximate (iteration-dependent) | Exact |
| Performance | O(iterations × constraints) | O(n³) dense, O(n) sparse chains |
| Stability | Good with warm-starting | Excellent |
| Stacking | Requires many iterations | Perfect |
| Implementation | Simple | Complex (sparse matrix factorization) |
| Used in games | ✅ (Box2D, PhysX, Jolt) | ❌ (too expensive for general use) |
| Used in robotics | ❌ | ✅ (MuJoCo, Drake) |

**Warm-Starting:** PGS converges much faster if initialized with the previous frame's impulses (warm-starting). Since constraints change slowly frame-to-frame, last frame's solution is a good initial guess. This reduces required iterations from 20+ to 4-8 for stable results.

---

