---
title: "Game Engine Architectures Unity Unreal"
subject: "VR & 3D Engineering"
catalog: advanced
audience_tier: higher-education
chapter: "28.5"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 28.5 — Game Engine Architectures: Unity & Unreal

> *"The engine is not the game. The engine is the machine that makes the game possible."* — Tim Sweeney

Game engines are the runtime frameworks that orchestrate rendering, physics, audio, input, networking, and scripting into a coherent interactive experience. This chapter dissects the two dominant engines — Unity (C#) and Unreal Engine (C++) — comparing their object models, lifecycle systems, rendering architectures, and performance paradigms. Understanding engine internals is essential for VR development where frame budgets are measured in single-digit milliseconds.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Describe the **Unity MonoBehaviour lifecycle** (Awake → OnEnable → Start → Update → LateUpdate → OnDisable → OnDestroy).
2. Describe the **Unreal Actor/Component lifecycle** (Constructor → BeginPlay → Tick → EndPlay → Destroyed).
3. Compare **inheritance-based** (Unreal UObject) vs. **component-based** (Unity GameObject+Components) architectures.
4. Explain **Entity Component System (ECS)** / DOTS in Unity and its performance advantages.
5. Differentiate Unreal's **Blueprint visual scripting** from C++ and identify when each is appropriate.
6. Describe rendering architectures: Unity's **URP/HDRP** vs. Unreal's **Lumen/Nanite**.
7. Identify VR-specific engine features: single-pass stereo, foveated rendering, late-latching.

---

## 🖼️ Visual Anchor — Engine Architecture Comparison

![track-09__9.5-fig1](track-09__9.5-fig1.svg)

---

## 📚 1. Definitions

### Definition 28.5.1 — Game Loop

The **game loop** is the core execution cycle of any real-time application:

```
while (running) {
    processInput();
    update(deltaTime);
    render();
}
```

Each iteration produces one frame. For VR at 90 Hz, the entire loop must complete in $\leq 11.1$ ms.

### Definition 28.5.2 — Unity MonoBehaviour Lifecycle

A `MonoBehaviour` is Unity's base class for user scripts attached to GameObjects. Its lifecycle methods execute in this order:

1. **Awake()** — Called once when the script instance is loaded (before Start). Use for self-initialization.
2. **OnEnable()** — Called each time the object becomes active.
3. **Start()** — Called once before the first Update, after all Awake calls. Use for cross-references.
4. **FixedUpdate()** — Called at fixed time intervals (default 0.02s). Use for physics.
5. **Update()** — Called once per frame. Use for game logic, input.
6. **LateUpdate()** — Called after all Update calls. Use for camera follow, post-processing logic.
7. **OnDisable()** — Called when the object becomes inactive.
8. **OnDestroy()** — Called when the object is destroyed.

### Definition 28.5.3 — Unreal Actor Lifecycle

An `AActor` is Unreal's base class for objects placed in the world:

1. **Constructor** — Called during object creation (CDO and instances). Set defaults only; no gameplay logic.
2. **PostInitializeComponents()** — All components initialized.
3. **BeginPlay()** — Called when the game starts or the actor is spawned. Equivalent to Unity's Start.
4. **Tick(float DeltaTime)** — Called every frame (if ticking enabled). Equivalent to Update.
5. **EndPlay(EEndPlayReason)** — Called when removed from world or level unloads.
6. **Destroyed()** / destructor — Final cleanup.

### Definition 28.5.4 — Entity Component System (ECS)

**ECS** separates data (Components) from behavior (Systems) and identity (Entities):
- **Entity:** A lightweight ID (integer) with no data or behavior.
- **Component:** Pure data struct (e.g., `Position { float3 value; }`).
- **System:** Logic that iterates over entities with specific component combinations.

Advantages: cache-friendly memory layout (struct-of-arrays), trivial parallelization, no virtual dispatch overhead.

### Definition 28.5.5 — Unreal Blueprint vs. C++

| Aspect | Blueprint | C++ |
|--------|-----------|-----|
| Speed | ~10x slower (VM interpreted) | Native compiled |
| Iteration | Hot-reload, visual | Requires recompile |
| Use case | Prototyping, designers, simple logic | Performance-critical, core systems |
| Debugging | Visual flow, breakpoints on nodes | Traditional debugger (VS, Rider) |
| Interop | Can call C++ functions via `UFUNCTION()` | Exposes to BP via macros |

### Definition 28.5.6 — Nanite (Unreal Engine 5)

**Nanite** is a virtualized geometry system that streams and renders film-quality meshes (millions of polygons) in real-time. It uses:
- Hierarchical LOD clusters
- GPU-driven rendering (visibility buffer)
- Software rasterization for small triangles
- No manual LOD authoring required

### Definition 28.5.7 — Lumen (Unreal Engine 5)

**Lumen** is a fully dynamic global illumination and reflections system. It combines:
- Screen-space traces
- Surface cache (simplified scene representation)
- Hardware ray tracing (optional, for quality)
- No baked lightmaps required for dynamic scenes



---

## 📐 2. Axioms / Postulates

### Axiom 28.5.A1 — Frame Budget Constraint

For VR at 90 Hz: total frame time $\leq 11.1$ ms. This includes:
- CPU game logic + draw call submission: ~4 ms
- GPU rendering: ~7 ms
- Any frame exceeding budget causes **reprojection** (ASW/ATW), which introduces artifacts.

### Axiom 28.5.A2 — Composition Over Inheritance

Modern engine design favors attaching behavior via components rather than deep inheritance hierarchies. This enables:
- Mixing capabilities without diamond inheritance problems
- Runtime addition/removal of behaviors
- Better cache utilization (ECS)

### Axiom 28.5.A3 — Deterministic Physics Requires Fixed Timestep

Physics simulations must run at a fixed timestep (e.g., 50 Hz) independent of frame rate to ensure deterministic, stable results. Variable-timestep physics leads to tunneling, jitter, and non-reproducible behavior.

---

## 🛡️ 3. Lemmas

### Lemma 28.5.1 — Unity's Execution Order Guarantees

Within a single frame, Unity guarantees: all `FixedUpdate` calls (0 or more) → all `Update` calls → all `LateUpdate` calls. Between scripts of the same priority, execution order is undefined unless explicitly set via Script Execution Order settings.

### Lemma 28.5.2 — Unreal's Garbage Collection

Unreal uses a mark-and-sweep garbage collector for `UObject`-derived classes. Objects are only collected when no `UPROPERTY()` references point to them. Raw C++ pointers (`UObject*` without `UPROPERTY()`) are invisible to GC and can become dangling.

---

## 👑 4. Theorems

### Theorem 28.5.1 — ECS Performance Advantage

For $N$ entities with $k$ components each, ECS with struct-of-arrays layout achieves $O(N)$ cache-line-optimal iteration, while OOP with scattered heap allocations averages $O(N \cdot k)$ cache misses due to pointer chasing.

### Theorem 28.5.2 — Draw Call Batching Reduces CPU Overhead

Combining $n$ objects sharing the same material into a single draw call reduces CPU-GPU synchronization from $O(n)$ to $O(1)$. Unity's SRP Batcher and Unreal's instanced static meshes implement this automatically for qualifying objects.

---

## ✍️ 5. Proofs / Derivations

### 5.1 Derivation of Frame Budget Allocation

**Given:** 90 Hz target → 11.11 ms per frame.

**CPU-GPU parallelism:** The CPU prepares frame $N+1$ while the GPU renders frame $N$. Therefore:

$$
t_{\text{frame}} = \max(t_{\text{CPU}}, t_{\text{GPU}})
$$

Both must independently be $\leq 11.11$ ms. If either exceeds the budget, frames are dropped.

**Typical VR allocation:**
- Input sampling + game logic: 2 ms
- Animation + physics: 1.5 ms
- Culling + draw call submission: 1.5 ms
- GPU vertex processing: 1.5 ms
- GPU fragment processing: 4 ms
- Post-processing + lens distortion: 1 ms
- **Total GPU:** 6.5 ms (within budget)

### 5.2 Why MonoBehaviour Update Order Matters for Cameras

**Problem:** If the camera's `Update()` runs before the player's `Update()`, the camera follows the player's previous-frame position, causing one frame of lag.

**Solution:** Camera logic in `LateUpdate()` guarantees it executes after all `Update()` calls, seeing the current frame's player position.

**Formal guarantee:** Unity's execution order: Physics → Update (all scripts) → LateUpdate (all scripts) → Render. Therefore `LateUpdate` always sees the results of the current frame's `Update`.

---

## 💻 6. Code Examples

### 6.1 Unity C#: Complete MonoBehaviour

```csharp
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    [SerializeField] private float moveSpeed = 5f;
    [SerializeField] private float rotSpeed = 120f;

    private Rigidbody rb;
    private Vector3 moveInput;

    void Awake()
    {
        // Self-initialization (no cross-references)
        rb = GetComponent<Rigidbody>();
    }

    void Start()
    {
        // Cross-references safe here
        Debug.Log($"Player initialized at {transform.position}");
    }

    void Update()
    {
        // Input polling (every frame)
        float h = Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");
        moveInput = new Vector3(h, 0, v).normalized;

        // Rotation
        if (h != 0)
            transform.Rotate(Vector3.up, h * rotSpeed * Time.deltaTime);
    }

    void FixedUpdate()
    {
        // Physics movement (fixed timestep)
        Vector3 move = transform.forward * moveInput.z * moveSpeed;
        rb.MovePosition(rb.position + move * Time.fixedDeltaTime);
    }

    void OnDestroy()
    {
        Debug.Log("Player destroyed");
    }
}
```

### 6.2 Unreal C++: Actor with Component

```cpp
// MyProjectile.h
#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "MyProjectile.generated.h"

UCLASS()
class AMyProjectile : public AActor
{
    GENERATED_BODY()

public:
    AMyProjectile();

    UPROPERTY(VisibleAnywhere)
    class USphereComponent* CollisionComp;

    UPROPERTY(VisibleAnywhere)
    class UProjectileMovementComponent* MovementComp;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Speed = 3000.f;

protected:
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaTime) override;

    UFUNCTION()
    void OnHit(UPrimitiveComponent* HitComp, AActor* OtherActor,
               UPrimitiveComponent* OtherComp, FVector NormalImpulse,
               const FHitResult& Hit);
};

// MyProjectile.cpp
#include "MyProjectile.h"
#include "Components/SphereComponent.h"
#include "GameFramework/ProjectileMovementComponent.h"

AMyProjectile::AMyProjectile()
{
    PrimaryActorTick.bCanEverTick = true;

    CollisionComp = CreateDefaultSubobject<USphereComponent>(TEXT("Sphere"));
    CollisionComp->InitSphereRadius(15.f);
    CollisionComp->OnComponentHit.AddDynamic(this, &AMyProjectile::OnHit);
    RootComponent = CollisionComp;

    MovementComp = CreateDefaultSubobject<UProjectileMovementComponent>(TEXT("Movement"));
    MovementComp->InitialSpeed = Speed;
    MovementComp->MaxSpeed = Speed;
    MovementComp->bRotationFollowsVelocity = true;

    InitialLifeSpan = 3.f; // auto-destroy after 3 seconds
}

void AMyProjectile::BeginPlay()
{
    Super::BeginPlay();
    UE_LOG(LogTemp, Log, TEXT("Projectile spawned at %s"), *GetActorLocation().ToString());
}

void AMyProjectile::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
}

void AMyProjectile::OnHit(UPrimitiveComponent* HitComp, AActor* OtherActor,
    UPrimitiveComponent* OtherComp, FVector NormalImpulse, const FHitResult& Hit)
{
    if (OtherActor && OtherActor != this)
    {
        Destroy();
    }
}
```

---

## 🧮 7. Worked Examples

### Example 28.5.1 — Unity: Smooth Camera Follow in LateUpdate

**Problem:** Implement a camera that smoothly follows a target with damping, avoiding one-frame lag.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```csharp
public class SmoothFollow : MonoBehaviour
{
    [SerializeField] private Transform target;
    [SerializeField] private Vector3 offset = new Vector3(0, 5, -10);
    [SerializeField] private float smoothTime = 0.3f;

    private Vector3 velocity = Vector3.zero;

    void LateUpdate()
    {
        // LateUpdate ensures target has already moved this frame
        Vector3 desiredPos = target.position + target.rotation * offset;
        transform.position = Vector3.SmoothDamp(
            transform.position, desiredPos, ref velocity, smoothTime);
        transform.LookAt(target.position + Vector3.up * 1.5f);
    }
}
```

**Why LateUpdate:** The target's `Update()` moves it first. `LateUpdate()` then positions the camera at the new location. If we used `Update()`, execution order between scripts is undefined — the camera might see stale position data.

</details>

### Example 28.5.2 — Unreal: Blueprint vs C++ Performance

**Problem:** A system needs to process 10,000 actors per frame. Compare Blueprint vs C++ Tick cost.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Blueprint Tick:** Each Blueprint node invocation has ~10x overhead vs native C++ due to the VM interpreter, reflection system, and garbage collection pressure.

Measured: Blueprint Tick for simple math = ~0.005 ms/actor.
10,000 actors × 0.005 ms = **50 ms** (far exceeds 11.1 ms budget).

**C++ Tick:** Native function call = ~0.0003 ms/actor.
10,000 actors × 0.0003 ms = **3 ms** (within budget).

**Solution:** Move hot-path logic to C++. Use Blueprints for:
- One-time setup (BeginPlay)
- Event-driven logic (OnHit, OnOverlap)
- Designer-facing parameters
- Prototyping before C++ migration

</details>

### Example 28.5.3 — ECS vs OOP Memory Layout

**Problem:** 100,000 entities with Position and Velocity components. Compare cache performance.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**OOP (scattered):** Each entity is a heap-allocated object with pointers to components:
```
Entity* → [vtable_ptr | pos_ptr → Position{x,y,z} | vel_ptr → Velocity{x,y,z}]
```
Iterating requires 2 pointer dereferences per entity. Cache line (64 bytes) holds ~5 Position structs but pointer chasing causes random access patterns.

**ECS (struct-of-arrays):**
```
Position[]: [x0,y0,z0, x1,y1,z1, x2,y2,z2, ...]  // contiguous
Velocity[]: [vx0,vy0,vz0, vx1,vy1,vz1, ...]       // contiguous
```
Linear iteration: CPU prefetcher predicts access pattern. Each cache line holds ~5 consecutive Position structs, all used immediately.

**Measured speedup:** 5–20x for iteration-heavy systems (physics, particle updates) due to:
- No pointer chasing (0 cache misses vs ~2 per entity)
- SIMD vectorization possible on contiguous arrays
- Trivial parallelization (split array ranges across threads)

</details>

---

## 🔗 8. Cross-links & Further Reading

### Internal Links
- **Previous:** [28.4 - Shader Programming - GLSL & HLSL](28.4---Shader-Programming---GLSL-&-HLSL) — engine shader integration
- **Next:** [28.6 - AEC to VR Pipelines - BIM Data](28.6---AEC-to-VR-Pipelines---BIM-Data) — using engines for architectural visualization
- **Quaternions in engines:** [28.2 - Quaternions & Rotations](28.2---Quaternions-&-Rotations) — Unity Quaternion, Unreal FQuat
- **Pipeline:** [28.3 - Graphics Rendering Pipeline](28.3---Graphics-Rendering-Pipeline) — what the engine's renderer executes

### External Resources
- **Unity Manual:** docs.unity3d.com — MonoBehaviour lifecycle, DOTS documentation
- **Unreal Documentation:** docs.unrealengine.com — Actor lifecycle, Nanite/Lumen
- **Game Programming Patterns** (Robert Nystrom) — free online book
- **Data-Oriented Design** (Richard Fabian) — ECS philosophy
- **GDC Talks:** "Parallelizing the Naughty Dog Engine" (2015)

### Practice
- [9.5_engine_skeletons.md](9.5_engine_skeletons.md) — minimal Unity/Unreal script templates



---

## 📎 Appendix: Engine Internals Deep Dive

### A.1 Unity Rendering Pipeline Comparison

| Feature | Built-in | URP | HDRP |
|---------|----------|-----|------|
| Target | Legacy | Mobile, VR, mid-range | High-end PC, console |
| Rendering | Forward (multi-pass) | Forward (single-pass) | Deferred + Forward |
| Lighting | Per-object, 8 lights max | Per-object, 8 lights | Tiled/Clustered, unlimited |
| Shadows | Shadow maps | Cascaded shadow maps | Contact shadows, PCSS |
| GI | Baked lightmaps | Baked + Light Probes | SSGI, Screen-space GI |
| VR Support | Multi-pass stereo | Single-pass instanced | Single-pass instanced |
| Shader Model | ShaderLab + CG | ShaderLab + HLSL | ShaderLab + HLSL |
| SRP Batcher | No | Yes | Yes |
| Custom passes | Limited | Render Features | Custom Passes |

### A.2 Unreal Engine Subsystem Architecture

```
UEngine (GEngine)
├── UGameEngine / UEditorEngine
├── UWorld
│   ├── ULevel (persistent + streaming)
│   │   ├── AActor[]
│   │   │   ├── UActorComponent[]
│   │   │   │   ├── USceneComponent (transform hierarchy)
│   │   │   │   ├── UStaticMeshComponent
│   │   │   │   ├── USkeletalMeshComponent
│   │   │   │   └── UPrimitiveComponent (rendering + collision)
│   │   │   └── Controller (AI or Player)
│   │   └── AWorldSettings
│   ├── UGameInstance (persists across levels)
│   └── AGameModeBase (rules, spawning)
├── Subsystems
│   ├── Rendering (FSceneRenderer → Deferred/Mobile)
│   ├── Physics (Chaos / PhysX)
│   ├── Audio (MetaSounds)
│   ├── Networking (Replication)
│   └── Input (Enhanced Input System)
└── Asset Management (FAssetManager, Streaming)
```

### A.3 Memory Management Patterns

**Unity:**
- Managed heap (C# GC) — allocations trigger GC pauses
- **Best practice:** Pool objects, avoid per-frame allocations
- `NativeArray<T>` for unmanaged, cache-friendly data (DOTS)
- `Addressables` for async asset loading

**Unreal:**
- `UObject` GC (mark-and-sweep, incremental)
- `UPROPERTY()` macro registers references for GC
- `TSharedPtr` / `TWeakPtr` for non-UObject shared ownership
- `FMemory::Malloc` for raw allocations (manual lifetime)
- Object pooling via `UObjectPool` or custom implementations

### A.4 VR-Specific Engine Features

**Unity XR:**
```csharp
// Single-pass instanced stereo (URP)
// Automatically enabled in XR settings
// Shader must handle:
// unity_StereoEyeIndex — 0 (left) or 1 (right)
// UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX(input)

// Late-latching (reduces motion-to-photon)
// Enabled via: XR Plugin Management → Oculus → Late Latching
```

**Unreal VR:**
```cpp
// Enable instanced stereo in Project Settings
// Engine → Rendering → VR → Instanced Stereo = true
// Mobile Multi-View = true (for Quest)

// Access HMD data
IHeadMountedDisplay* HMD = GEngine->XRSystem->GetHMDDevice();
FQuat HMDOrientation;
FVector HMDPosition;
HMD->GetCurrentPose(IXRTrackingSystem::HMDDeviceId, HMDOrientation, HMDPosition);
```

### A.5 Profiling Workflow

**Unity:**
1. Window → Analysis → Profiler (CPU, GPU, Memory)
2. Frame Debugger (draw call inspection)
3. `Profiler.BeginSample("MyCode")` / `EndSample()` for custom markers
4. Memory Profiler package for heap snapshots

**Unreal:**
1. `stat unit` — frame time breakdown (Game, Draw, GPU)
2. `stat scenerendering` — detailed render stats
3. `profilegpu` — GPU profiler with timeline
4. Unreal Insights — comprehensive trace-based profiler
5. RenderDoc integration for draw-call-level GPU debugging

### A.6 Asset Streaming and Level Design

**Unity Addressables:**
```csharp
// Async load asset by address
var handle = Addressables.LoadAssetAsync<GameObject>("Prefabs/Building_A");
handle.Completed += (op) => {
    Instantiate(op.Result, spawnPoint.position, Quaternion.identity);
};

// Scene streaming
Addressables.LoadSceneAsync("Scenes/Floor_2", LoadSceneMode.Additive);
```

**Unreal World Partition (UE5):**
- Automatic spatial streaming based on player position
- No manual level streaming setup required
- Grid-based cell loading with configurable radius
- Data layers for conditional content (e.g., day/night variants)

### A.7 Physics Engine Comparison

| Feature | Unity (PhysX) | Unreal (Chaos) |
|---------|---------------|----------------|
| Solver | Iterative PGS | Position-based (XPBD) |
| Destruction | Limited (3rd party) | Built-in (Chaos Destruction) |
| Cloth | Cloth component | Chaos Cloth |
| Vehicles | Wheel colliders | Chaos Vehicles |
| Determinism | Non-deterministic | Deterministic mode available |
| Fixed step | 50 Hz default | 30 Hz default (configurable) |
| VR note | Keep physics simple | Same — physics is expensive |



### A.8 Serialization and Save Systems

**Unity (JsonUtility + ScriptableObjects):**
```csharp
[System.Serializable]
public class SaveData
{
    public Vector3 playerPosition;
    public Quaternion playerRotation;
    public List<string> collectedItems;
    public float playTime;
}

public void Save()
{
    var data = new SaveData {
        playerPosition = player.transform.position,
        playerRotation = player.transform.rotation,
        collectedItems = inventory.GetItemIds(),
        playTime = Time.time
    };
    string json = JsonUtility.ToJson(data, prettyPrint: true);
    File.WriteAllText(Application.persistentDataPath + "/save.json", json);
}
```

**Unreal (USaveGame):**
```cpp
UCLASS()
class UMySaveGame : public USaveGame
{
    GENERATED_BODY()
public:
    UPROPERTY()
    FVector PlayerLocation;

    UPROPERTY()
    FRotator PlayerRotation;

    UPROPERTY()
    TArray<FString> CollectedItems;
};

// Save
UMySaveGame* SaveInstance = Cast<UMySaveGame>(
    UGameplayStatics::CreateSaveGameObject(UMySaveGame::StaticClass()));
SaveInstance->PlayerLocation = GetActorLocation();
UGameplayStatics::SaveGameToSlot(SaveInstance, TEXT("Slot1"), 0);

// Load
UMySaveGame* LoadedGame = Cast<UMySaveGame>(
    UGameplayStatics::LoadGameFromSlot(TEXT("Slot1"), 0));
```

### A.9 Animation Systems

**Unity Animator Controller:**
- State machine with transitions (conditions on parameters)
- Blend trees for locomotion (speed → walk/run blend)
- Avatar masks for partial-body animation
- IK (Inverse Kinematics) for hand/foot placement

**Unreal Animation Blueprint:**
- Event graph (logic) + Anim graph (blending)
- State machines with automatic transitions
- Montages for one-shot animations (attacks, emotes)
- Control Rig for procedural animation
- Full-body IK for VR avatar embodiment

### A.10 Networking Architecture Comparison

| Aspect | Unity (Netcode for GameObjects) | Unreal (Replication) |
|--------|-------------------------------|---------------------|
| Model | Client-authoritative or server | Server-authoritative |
| Sync | NetworkVariable + RPC | UPROPERTY(Replicated) + RPC |
| Ownership | Per-object ownership | Actor ownership |
| Prediction | Manual implementation | Built-in prediction framework |
| Bandwidth | Manual optimization | Automatic relevancy + priority |
| VR multiplayer | Photon/Mirror more common | Built-in, well-tested |

### A.11 Build and Deployment Pipeline

**Unity → Quest 2:**
1. Switch platform to Android
2. Set XR Plugin: Oculus
3. Configure quality settings (URP, fixed foveated rendering)
4. Build APK → `adb install` or App Lab submission
5. Profile with OVR Metrics Tool overlay

**Unreal → Quest 2:**
1. Target platform: Android (ASTC)
2. Enable Mobile Multi-View, Mobile HDR off
3. Configure Vulkan renderer
4. Package → deploy via Meta Quest Developer Hub
5. Profile with RenderDoc for Quest

**Key differences:**
- Unity: faster iteration, smaller APK size (~100–500 MB)
- Unreal: better visual quality defaults, larger APK (~500 MB–2 GB)
- Both: require aggressive optimization for standalone VR




---

## 🧠 9. Extended Worked Examples & Deep Dives

### Example 28.1 — Unity DOTS ECS Chunk-Data Layout Walkthrough

**Problem:** You have 10,000 particles each with `Position` (float3, 12 bytes), `Velocity` (float3, 12 bytes), and `Lifetime` (float, 4 bytes). Walk through exactly how Unity ECS stores these in memory chunks, compute entities per chunk, and compare cache performance against the traditional GameObject approach.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Compute archetype size per entity

In Unity DOTS, all entities sharing the same set of component types form an **archetype**. Each archetype stores data in 16 KB chunks (16,384 bytes). Within a chunk, components are stored in **Structure of Arrays (SoA)** layout — all `Position` values contiguous, then all `Velocity` values, then all `Lifetime` values.

Per-entity storage:

$$
\text{bytes/entity} = \underbrace{12}_{\text{Position}} + \underbrace{12}_{\text{Velocity}} + \underbrace{4}_{\text{Lifetime}} + \underbrace{4}_{\text{Entity ID}} = 32 \text{ bytes}
$$

(Unity adds a 4-byte Entity reference per entity in each chunk for internal bookkeeping.)

#### Step 2: Compute entities per chunk

Chunk usable capacity is approximately 16,128 bytes (16 KB minus chunk header ~256 bytes for metadata):

$$
\text{entities/chunk} = \left\lfloor \frac{16128}{32} \right\rfloor = 504 \text{ entities}
$$

#### Step 3: Compute total chunks needed

$$
\text{chunks} = \left\lceil \frac{10000}{504} \right\rceil = \lceil 19.84 \rceil = 20 \text{ chunks}
$$

Total memory: $20 \times 16384 = 327,680$ bytes $\approx 320$ KB.

#### Step 4: Cache line analysis for a system reading Position + Velocity

A typical L1 cache line is 64 bytes. When iterating positions in the SoA layout:

$$
\text{positions per cache line} = \frac{64}{12} = 5.33 \implies 5 \text{ positions per fetch}
$$

For 504 entities in one chunk, reading all positions requires:

$$
\lceil 504 / 5 \rceil = 101 \text{ cache line fetches for Position}
$$

$$
\lceil 504 / 5 \rceil = 101 \text{ cache line fetches for Velocity}
$$

Total: 202 cache fetches for a full chunk. All sequential — **zero cache misses** after the first fetch per array (hardware prefetcher handles linear access perfectly).

#### Step 5: Compare with GameObject + MonoBehaviour

In the traditional model, each particle is a `GameObject` with a `MonoBehaviour` script. The data layout is **Array of Structures (AoS)** scattered across the managed heap:

- Each `GameObject`: ~200 bytes (Transform, name, layer, tag, component list pointers)
- Each `MonoBehaviour`: ~80 bytes overhead + your fields
- Transform component: separate native allocation (~128 bytes)

Per-particle effective memory: $\approx 400+$ bytes (vs. 32 bytes in ECS).

Cache behavior: iterating 10,000 GameObjects requires pointer-chasing through the component list. Each `GetComponent<T>()` call is a hash lookup. Memory is non-contiguous — **every entity access is a potential cache miss**.

$$
\text{Cache miss ratio (estimated):} \quad \text{ECS} \approx 0.2\% \quad \text{vs.} \quad \text{GameObject} \approx 40\text{–}60\%
$$

**Final Answer:**

$$
\text{ECS: } 20 \text{ chunks} \times 16\text{KB} = 320\text{ KB, sequential access, } \sim\!0\% \text{ cache miss}
$$

$$
\text{GameObject: } \sim\!4\text{ MB scattered, pointer-chasing, } \sim\!50\% \text{ cache miss}
$$

For 10,000 particles, ECS is approximately **10–50× faster** in iteration due to memory layout alone.

</details>

### Example 28.2 — Unreal AActor Lifecycle Hand-Trace

**Problem:** Trace the complete lifecycle of a custom `AProjectile` actor in Unreal Engine 5 from spawn to destruction, identifying every engine callback in order with its purpose and thread context.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Spawn — `UWorld::SpawnActor<AProjectile>()`

The engine calls these in strict order on the **Game Thread**:

1. **`AProjectile::AProjectile()` (Constructor)** — C++ object allocation. Set default property values and create subobjects (`CreateDefaultSubobject<T>`). NO gameplay logic here — the world doesn't exist yet from this actor's perspective.

2. **`PostInitProperties()`** — Called after all UPROPERTY values are loaded from the CDO (Class Default Object). Safe to read serialized data.

3. **`PostActorCreated()`** — Called only for dynamically spawned actors (not placed in level). One-time setup that differs from level-placed instances.

4. **`OnConstruction(Transform)`** — The "construction script" equivalent in C++. Called after transform is set. Runs in editor too — keep it deterministic.

5. **`PostInitializeComponents()`** — All actor components have been registered and initialized. Safe to cache component pointers.

6. **`BeginPlay()`** — The actor is fully in the world. Start gameplay logic, timers, bind delegates. This is where you:
   - Initialize velocity: `ProjectileMovement->Velocity = GetActorForwardVector() * Speed;`
   - Bind overlap events: `CollisionComp->OnComponentBeginOverlap.AddDynamic(this, &AProjectile::OnHit);`
   - Start lifetime timer: `SetLifeSpan(5.0f);`

#### Step 2: Per-Frame Update Loop

Each frame, in order:

7. **`Tick(float DeltaTime)`** — Called every frame (if `PrimaryActorTick.bCanEverTick = true`). For a projectile, the `UProjectileMovementComponent` handles movement in its own tick, so the actor tick might just check distance traveled.

   Frame time budget at 90 FPS (VR): $\frac{1000}{90} = 11.11$ ms total. Actor tick should consume < 0.01 ms.

8. **Physics substep** (if enabled) — `Chaos` solver updates collision at fixed rate (e.g., 60 Hz). Overlap/hit events are queued.

9. **`OnComponentBeginOverlap` / `NotifyHit`** — Dispatched after physics. The projectile detects it hit a wall or enemy.

#### Step 3: Destruction Sequence

When `Destroy()` is called (or `LifeSpan` expires):

10. **`EndPlay(EEndPlayReason::Destroyed)`** — Cleanup gameplay state. Unbind delegates, stop audio, notify game mode of projectile removal. The actor is still valid here.

11. **`OnDestroyed` delegate broadcast** — External listeners (e.g., spawner tracking active projectile count) receive notification.

12. **`BeginDestroy()`** — Engine begins GC teardown. Do NOT access other UObjects here — they may already be gone.

13. **`IsReadyForFinishDestroy()`** — Engine polls until async resources (textures, audio) finish unloading.

14. **`FinishDestroy()`** — Final C++ destructor-equivalent. Memory is reclaimed. Object is gone.

#### Step 4: Thread safety summary

| Callback | Thread | Safe to access world? |
|----------|--------|----------------------|
| Constructor | Game Thread | ❌ No world context |
| BeginPlay | Game Thread | ✅ Full access |
| Tick | Game Thread | ✅ Full access |
| Physics callbacks | Game Thread (deferred) | ✅ Full access |
| EndPlay | Game Thread | ✅ Actor still valid |
| BeginDestroy | Game Thread | ⚠️ Other objects may be gone |
| FinishDestroy | Game Thread | ❌ Do not access anything |

**Final Answer:**

$$
\text{Lifecycle: Constructor} \to \text{PostInit} \to \text{BeginPlay} \to [\text{Tick}]^N \to \text{EndPlay} \to \text{BeginDestroy} \to \text{FinishDestroy}
$$

Total callbacks per actor lifetime: 6 guaranteed + $N$ ticks where $N = \text{lifetime} \times \text{FPS}$. For a 5-second projectile at 90 FPS: $N = 450$ tick calls.

</details>

---
