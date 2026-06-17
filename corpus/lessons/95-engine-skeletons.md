---
title: "Engine Skeletons"
subject: "scripts"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# 9.5 — Engine Skeletons: Unity C# & Unreal C++ Templates

*Reference companion to [28.5 - Game Engine Architectures - Unity & Unreal](28.5---Game-Engine-Architectures---Unity-&-Unreal)*

---

## 1. Unity MonoBehaviour — Full Lifecycle Template

```csharp
using UnityEngine;

/// <summary>
/// Template demonstrating the complete MonoBehaviour lifecycle.
/// Attach to any GameObject to observe execution order in Console.
/// </summary>
public class LifecycleDemo : MonoBehaviour
{
    // === INITIALIZATION PHASE ===

    void Awake()
    {
        // Called ONCE when script instance loads (scene load or Instantiate)
        // Order: before any Start() calls
        // Use: GetComponent references, self-initialization
        Debug.Log($"[{name}] Awake - frame {Time.frameCount}");
    }

    void OnEnable()
    {
        // Called each time the GameObject/component becomes active
        // Use: subscribe to events, register callbacks
        Debug.Log($"[{name}] OnEnable");
    }

    void Start()
    {
        // Called ONCE before the first Update, AFTER all Awake() calls
        // Use: cross-object references, initialization depending on other objects
        Debug.Log($"[{name}] Start - frame {Time.frameCount}");
    }

    // === PHYSICS PHASE (fixed timestep, 0-N times per frame) ===

    void FixedUpdate()
    {
        // Called at fixed intervals (default 50Hz = 0.02s)
        // Use: Rigidbody forces, physics queries
        // Time.fixedDeltaTime is constant
    }

    void OnCollisionEnter(Collision collision)
    {
        // Called by physics engine when collision begins
    }

    void OnTriggerEnter(Collider other)
    {
        // Called when entering a trigger volume
    }

    // === GAME LOGIC PHASE (once per frame) ===

    void Update()
    {
        // Called once per frame (variable timestep)
        // Use: input, game logic, non-physics movement
        // Time.deltaTime = time since last frame
    }

    void LateUpdate()
    {
        // Called after ALL Update() calls complete
        // Use: camera follow, procedural animation, anything that
        //      depends on other objects' Update results
    }

    // === RENDERING PHASE ===

    void OnBecameVisible() { /* Renderer entered camera frustum */ }
    void OnBecameInvisible() { /* Renderer left all camera frustums */ }
    void OnRenderObject() { /* Called after camera renders the scene */ }

    // === CLEANUP PHASE ===

    void OnDisable()
    {
        // Called when GameObject/component becomes inactive
        // Use: unsubscribe events, pause logic
        Debug.Log($"[{name}] OnDisable");
    }

    void OnDestroy()
    {
        // Called when the object is destroyed (scene unload or Destroy())
        // Use: final cleanup, save state
        Debug.Log($"[{name}] OnDestroy");
    }

    void OnApplicationQuit()
    {
        // Called on all objects before the application exits
    }
}
```

---

## 2. Unity ScriptableObject — Data Container

```csharp
using UnityEngine;

[CreateAssetMenu(fileName = "WeaponData", menuName = "Game/Weapon Data")]
public class WeaponData : ScriptableObject
{
    public string weaponName;
    public float damage = 10f;
    public float fireRate = 0.5f;
    public float range = 50f;
    public GameObject projectilePrefab;
    public AudioClip fireSound;
}
```

**Usage:** Create instances in Project window. Reference from MonoBehaviours. Shared across all instances (no per-object memory duplication).

---

## 3. Unreal C++ — AActor Full Lifecycle

```cpp
// LifecycleActor.h
#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "LifecycleActor.generated.h"

UCLASS()
class MYGAME_API ALifecycleActor : public AActor
{
    GENERATED_BODY()

public:
    ALifecycleActor();

    // === PROPERTIES (exposed to editor/blueprints) ===
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Config")
    float MoveSpeed = 300.f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class UStaticMeshComponent* MeshComp;

protected:
    // === LIFECYCLE ===
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaTime) override;
    virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

    // === EVENTS ===
    UFUNCTION()
    void OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor,
        UPrimitiveComponent* OtherComp, int32 OtherBodyIndex,
        bool bFromSweep, const FHitResult& SweepResult);
};

// LifecycleActor.cpp
#include "LifecycleActor.h"
#include "Components/StaticMeshComponent.h"

ALifecycleActor::ALifecycleActor()
{
    // Constructor: set defaults, create components
    // NO gameplay logic here (runs for CDO too)
    PrimaryActorTick.bCanEverTick = true;

    MeshComp = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
    RootComponent = MeshComp;
}

void ALifecycleActor::BeginPlay()
{
    Super::BeginPlay(); // Always call Super
    UE_LOG(LogTemp, Log, TEXT("BeginPlay: %s at %s"),
        *GetName(), *GetActorLocation().ToString());

    // Safe to access other actors, game state, etc.
    MeshComp->OnComponentBeginOverlap.AddDynamic(this, &ALifecycleActor::OnOverlapBegin);
}

void ALifecycleActor::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
    // Per-frame logic
    AddActorLocalOffset(FVector(MoveSpeed * DeltaTime, 0, 0));
}

void ALifecycleActor::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    UE_LOG(LogTemp, Log, TEXT("EndPlay: %s, Reason: %d"), *GetName(), (int32)EndPlayReason);
    Super::EndPlay(EndPlayReason);
}

void ALifecycleActor::OnOverlapBegin(UPrimitiveComponent* OverlappedComp,
    AActor* OtherActor, UPrimitiveComponent* OtherComp,
    int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
    UE_LOG(LogTemp, Log, TEXT("Overlap with: %s"), *OtherActor->GetName());
}
```

---

## 4. Blueprint vs C++ Decision Matrix

| Scenario | Recommendation | Reason |
|----------|---------------|--------|
| UI button callbacks | Blueprint | Designer-friendly, rare execution |
| AI behavior trees | Blueprint + C++ nodes | Visual flow + performant leaf nodes |
| 10,000 projectiles/frame | C++ only | Hot path, needs SIMD/cache efficiency |
| Material parameter tweaking | Blueprint | Iteration speed, no recompile |
| Networking replication | C++ | Complex, needs precise control |
| VR interaction system | C++ core + BP events | Performance + designer extensibility |

---

## 5. Unity DOTS/ECS Minimal Example

```csharp
using Unity.Entities;
using Unity.Mathematics;
using Unity.Transforms;

// Component (pure data, no methods)
public struct MoveSpeed : IComponentData
{
    public float Value;
}

// System (logic operating on components)
public partial struct MoveSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        float dt = SystemAPI.Time.DeltaTime;

        foreach (var (transform, speed) in
            SystemAPI.Query<RefRW<LocalTransform>, RefRO<MoveSpeed>>())
        {
            transform.ValueRW.Position += new float3(0, 0, speed.ValueRO.Value * dt);
        }
    }
}
```

**Key differences from MonoBehaviour:**
- No inheritance, no virtual calls
- Data is contiguous in memory (cache-friendly)
- System processes ALL matching entities in one tight loop
- Burst compiler generates SIMD-optimized native code


---

## Related Notes
- [9.4_shader_examples](9.4_shader_examples) - Shared review/3d/reference focus
- [9.7_xr_interaction](9.7_xr_interaction) - Shared review/3d/reference focus
- [Subject_Plan](Subject_Plan) - Shared unreal/unity focus
- [_IMPORT_TO_OBSIDIAN](_IMPORT_TO_OBSIDIAN) - Related reference topic
