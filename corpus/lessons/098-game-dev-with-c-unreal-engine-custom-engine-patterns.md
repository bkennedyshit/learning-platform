---
title: "09.8 — Game Dev with C++: Unreal Engine & Custom Engine Patterns"
subject: "C++"
catalog: advanced
audience_tier: higher-education
chapter: "9.8"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | [LEARNING_PATH](LEARNING_PATH) | Part of [09 - Learning Index](09---Learning-Index)*

# 09.8 — Game Dev with C++: Unreal Engine & Custom Engine Patterns

> *"Loaded with features, Unreal Engine is the most powerful game engine in the world. But power without understanding is just complexity."* — Tim Sweeney

> *"If you want to make a game, use an engine. If you want to make an engine, make a game."* — John Carmack

This chapter bridges everything you've learned into game development — both within Unreal Engine's opinionated C++ framework and in custom engine architectures using Entity Component Systems and Data-Oriented Design.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Write Unreal Engine C++ classes with proper UPROPERTY/UFUNCTION macros.
2. Understand the UObject system: garbage collection, reflection, serialization.
3. Design Blueprint-friendly C++ classes for designer iteration.
4. Implement the AActor lifecycle (BeginPlay, Tick, EndPlay, destruction).
5. Build an Entity Component System (ECS) from scratch.
6. Apply Data-Oriented Design principles to game systems.
7. Choose between Unreal's framework and custom engine approaches for different projects.

---

## 🖼️ Visual Anchor — Unreal Engine C++ Architecture

![cpp__2.8-fig1](cpp__2.8-fig1.svg)

---

## 📚 1. Concepts & Definitions

### Definition 09.8.1 — The UObject System

Unreal Engine doesn't use standard C++. It layers a **reflection system** on top via macros:

| Macro | Purpose |
|-------|---------|
| `UCLASS()` | Marks a class for UE reflection (GC, serialization, Blueprints) |
| `UPROPERTY()` | Marks a member variable (visible to GC, editor, Blueprints) |
| `UFUNCTION()` | Marks a function (callable from Blueprints, replication) |
| `USTRUCT()` | Marks a struct for reflection (no GC, but serializable) |
| `UENUM()` | Marks an enum for Blueprint/editor exposure |

```cpp
UCLASS(Blueprintable)
class MYGAME_API APlayerCharacter : public ACharacter {
    GENERATED_BODY()

public:
    APlayerCharacter();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float MaxHealth = 100.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
    float CurrentHealth;

    UFUNCTION(BlueprintCallable, Category = "Combat")
    void TakeDamage(float Amount);

    UFUNCTION(BlueprintImplementableEvent)
    void OnDeath();  // Implemented in Blueprint, called from C++

protected:
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaTime) override;
};
```

### Definition 09.8.2 — Unreal's Garbage Collection

UObject-derived classes are **garbage collected** — but not like Python/Java:

- GC runs periodically (configurable, typically every 60 seconds or on demand)
- Objects are collected when **no UPROPERTY references** point to them
- Raw C++ pointers (`UObject*`) are NOT tracked — only `UPROPERTY()` pointers
- `TWeakObjectPtr`, `TSoftObjectPtr` for non-owning references

```cpp
UPROPERTY()
UStaticMeshComponent* MeshComp;  // GC-tracked: object won't be collected

UObject* RawPtr = NewObject<UObject>();  // NOT tracked! Can dangle!

// SAFE patterns:
UPROPERTY()
TObjectPtr<AActor> SafeRef;  // C++20-style, GC-tracked

TWeakObjectPtr<AActor> WeakRef;  // Non-owning, auto-nulls when collected
if (WeakRef.IsValid()) { WeakRef->DoSomething(); }
```

### Definition 09.8.3 — AActor Lifecycle

```
Constructor → PostInitializeComponents → BeginPlay → Tick (every frame) → EndPlay → Destroyed
```

| Phase | When | Use For |
|-------|------|---------|
| Constructor | Object creation (CDO + instances) | Set defaults, create components |
| PostInitializeComponents | After all components initialized | Cross-component setup |
| BeginPlay | Game starts or actor spawned | Runtime initialization, find references |
| Tick | Every frame | Game logic, movement, AI |
| EndPlay | Actor removed from world | Cleanup, save state |
| Destroyed / ~destructor | Memory freed | (Rarely override — GC handles) |

### Definition 09.8.4 — Entity Component System (ECS)

ECS separates data (Components) from logic (Systems) and identity (Entities):

| Concept | What It Is | Example |
|---------|-----------|---------|
| **Entity** | Just an ID (integer) | Entity #42 |
| **Component** | Pure data (no logic) | `Position{x, y, z}`, `Health{current, max}` |
| **System** | Logic that operates on components | `MovementSystem` processes all entities with Position + Velocity |

```cpp
// Components are plain data
struct Position { float x, y, z; };
struct Velocity { float vx, vy, vz; };
struct Health { float current, max; };
struct Sprite { TextureID texture; int frame; };

// Systems are functions that process component arrays
void movement_system(std::span<Position> pos, std::span<const Velocity> vel, float dt) {
    for (size_t i = 0; i < pos.size(); ++i) {
        pos[i].x += vel[i].vx * dt;
        pos[i].y += vel[i].vy * dt;
        pos[i].z += vel[i].vz * dt;
    }
}
```

### Definition 09.8.5 — Data-Oriented Design (DOD)

DOD is a philosophy: **design your data layout for the hardware, not for human mental models.**

| OOP Thinking | DOD Thinking |
|-------------|-------------|
| "A Player has health, position, inventory" | "The physics system needs all positions contiguous" |
| Inheritance hierarchies | Flat component arrays |
| Virtual dispatch | Batch processing by type |
| Encapsulation | Data locality |

See [09.7 - Performance - SIMD, Memory Layout & Cache Optimization](09.7---Performance---SIMD,-Memory-Layout-&-Cache-Optimization) for the performance rationale.

---

## 🧩 2. Mental Models

### Model 2.8.1 — "Unreal C++ ≠ Standard C++"

Unreal has its own:
- **String types:** `FString`, `FName`, `FText` (not `std::string`)
- **Containers:** `TArray`, `TMap`, `TSet` (not `std::vector`, `std::map`)
- **Smart pointers:** `TSharedPtr`, `TUniquePtr` (for non-UObject types)
- **Memory:** `NewObject<T>()`, not `new T()` (for UObjects)
- **Casting:** `Cast<T>()`, not `dynamic_cast<T*>()` (faster, UObject-aware)

This is intentional — Unreal predates modern C++ and needs reflection/GC integration.

### Model 2.8.2 — "Blueprint = Visual Scripting Layer on C++"

The ideal workflow:
1. **C++ programmers** create base classes with `UPROPERTY`/`UFUNCTION` exposed
2. **Designers** create Blueprint subclasses, override events, tweak values
3. **Hot path** stays in C++; **iteration** happens in Blueprints

```
C++ Base Class (AWeapon)
    ├── UPROPERTY: Damage, FireRate, Range
    ├── UFUNCTION: Fire(), Reload()
    └── BlueprintImplementableEvent: OnFire(), OnReload()

Blueprint: BP_Shotgun (inherits AWeapon)
    ├── Damage = 80, FireRate = 0.5, Range = 10
    └── OnFire: Play sound + spawn particles (visual scripting)
```

### Model 2.8.3 — "ECS = Database for Game State"

Think of ECS as a relational database:
- **Entities** = row IDs
- **Components** = columns
- **Systems** = queries (SELECT Position, Velocity WHERE has_both)
- **Archetypes** = tables (groups of entities with the same component set)

This is why ECS is cache-friendly: systems iterate contiguous arrays of the same type, not scattered objects with mixed data.

---

## 🔑 3. Mechanics

### 3.1 — Unreal Engine: Creating a C++ Actor

```cpp
// MyProjectile.h
#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "MyProjectile.generated.h"  // MUST be last include

UCLASS()
class MYGAME_API AMyProjectile : public AActor {
    GENERATED_BODY()

public:
    AMyProjectile();

    UPROPERTY(VisibleAnywhere)
    USphereComponent* CollisionComp;

    UPROPERTY(VisibleAnywhere)
    UProjectileMovementComponent* MovementComp;

    UPROPERTY(EditDefaultsOnly, Category = "Damage")
    float Damage = 25.0f;

    UPROPERTY(EditDefaultsOnly, Category = "Damage")
    float Speed = 3000.0f;

    UFUNCTION()
    void OnHit(UPrimitiveComponent* HitComp, AActor* OtherActor,
               UPrimitiveComponent* OtherComp, FVector NormalImpulse,
               const FHitResult& Hit);

protected:
    virtual void BeginPlay() override;
};
```

```cpp
// MyProjectile.cpp
#include "MyProjectile.h"
#include "Components/SphereComponent.h"
#include "GameFramework/ProjectileMovementComponent.h"

AMyProjectile::AMyProjectile() {
    // Create components in constructor
    CollisionComp = CreateDefaultSubobject<USphereComponent>(TEXT("SphereComp"));
    CollisionComp->InitSphereRadius(15.0f);
    CollisionComp->SetCollisionProfileName(TEXT("Projectile"));
    SetRootComponent(CollisionComp);

    // Bind hit event
    CollisionComp->OnComponentHit.AddDynamic(this, &AMyProjectile::OnHit);

    // Movement component
    MovementComp = CreateDefaultSubobject<UProjectileMovementComponent>(TEXT("MovementComp"));
    MovementComp->InitialSpeed = Speed;
    MovementComp->MaxSpeed = Speed;
    MovementComp->bRotationFollowsVelocity = true;

    // Auto-destroy after 3 seconds
    InitialLifeSpan = 3.0f;
}

void AMyProjectile::BeginPlay() {
    Super::BeginPlay();
}

void AMyProjectile::OnHit(UPrimitiveComponent* HitComp, AActor* OtherActor,
                           UPrimitiveComponent* OtherComp, FVector NormalImpulse,
                           const FHitResult& Hit) {
    if (OtherActor && OtherActor != GetOwner()) {
        // Apply damage
        UGameplayStatics::ApplyDamage(OtherActor, Damage, GetInstigatorController(),
                                       this, UDamageType::StaticClass());
        Destroy();
    }
}
```

### 3.2 — Unreal: Blueprint/C++ Interop Patterns

```cpp
// Pattern 1: C++ function callable from Blueprint
UFUNCTION(BlueprintCallable, Category = "Inventory")
bool AddItem(FName ItemID, int32 Quantity);

// Pattern 2: Blueprint can override C++ behavior
UFUNCTION(BlueprintNativeEvent, Category = "Combat")
float CalculateDamage(float BaseDamage, AActor* Target);
// C++ provides default implementation:
float AMyCharacter::CalculateDamage_Implementation(float BaseDamage, AActor* Target) {
    return BaseDamage * DamageMultiplier;
}
// Blueprint can override with custom logic

// Pattern 3: C++ calls Blueprint-only function
UFUNCTION(BlueprintImplementableEvent, Category = "UI")
void OnLevelUp(int32 NewLevel);
// No C++ implementation — Blueprint MUST implement this

// Pattern 4: Multicast delegate (event dispatcher)
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnHealthChanged, float, NewHealth);

UPROPERTY(BlueprintAssignable, Category = "Events")
FOnHealthChanged OnHealthChanged;

// Fire from C++:
OnHealthChanged.Broadcast(CurrentHealth);
// Blueprint can bind to this event in the Event Graph
```

### 3.3 — Custom ECS Implementation

```cpp
#include <vector>
#include <unordered_map>
#include <typeindex>
#include <any>
#include <bitset>

using Entity = uint32_t;
constexpr size_t MAX_COMPONENTS = 64;
using ComponentMask = std::bitset<MAX_COMPONENTS>;

class World {
    Entity next_entity_ = 0;
    std::unordered_map<std::type_index, size_t> component_ids_;
    std::unordered_map<std::type_index, std::vector<std::byte>> pools_;
    std::vector<ComponentMask> entity_masks_;
    size_t next_component_id_ = 0;

    template<typename T>
    size_t get_component_id() {
        auto key = std::type_index(typeid(T));
        if (auto it = component_ids_.find(key); it != component_ids_.end()) {
            return it->second;
        }
        size_t id = next_component_id_++;
        component_ids_[key] = id;
        pools_[key].resize(0);
        return id;
    }

public:
    Entity create_entity() {
        Entity e = next_entity_++;
        entity_masks_.emplace_back();
        return e;
    }

    template<typename T>
    void add_component(Entity e, T component) {
        size_t id = get_component_id<T>();
        auto key = std::type_index(typeid(T));
        auto& pool = pools_[key];

        // Ensure pool is large enough
        size_t needed = (e + 1) * sizeof(T);
        if (pool.size() < needed) pool.resize(needed);

        // Place component
        new (&pool[e * sizeof(T)]) T(std::move(component));
        entity_masks_[e].set(id);
    }

    template<typename T>
    T* get_component(Entity e) {
        size_t id = get_component_id<T>();
        if (!entity_masks_[e].test(id)) return nullptr;
        auto key = std::type_index(typeid(T));
        return reinterpret_cast<T*>(&pools_[key][e * sizeof(T)]);
    }

    template<typename... Components, typename Func>
    void for_each(Func&& func) {
        ComponentMask required;
        (required.set(get_component_id<Components>()), ...);

        for (Entity e = 0; e < next_entity_; ++e) {
            if ((entity_masks_[e] & required) == required) {
                func(e, *get_component<Components>(e)...);
            }
        }
    }
};

// Usage:
World world;
Entity player = world.create_entity();
world.add_component(player, Position{0, 0, 0});
world.add_component(player, Velocity{1, 0, 0});
world.add_component(player, Health{100, 100});

// System: update all entities with Position + Velocity
world.for_each<Position, Velocity>([dt](Entity e, Position& pos, Velocity& vel) {
    pos.x += vel.vx * dt;
    pos.y += vel.vy * dt;
    pos.z += vel.vz * dt;
});
```

### 3.4 — Game Loop Architecture

```cpp
#include <chrono>

class GameLoop {
    static constexpr double FIXED_DT = 1.0 / 60.0;  // 60 Hz physics
    double accumulator_ = 0.0;

public:
    void run() {
        auto previous = std::chrono::high_resolution_clock::now();

        while (running_) {
            auto current = std::chrono::high_resolution_clock::now();
            double frame_time = std::chrono::duration<double>(current - previous).count();
            previous = current;

            // Cap frame time to prevent spiral of death
            frame_time = std::min(frame_time, 0.25);
            accumulator_ += frame_time;

            // Process input (once per frame)
            process_input();

            // Fixed timestep physics (deterministic)
            while (accumulator_ >= FIXED_DT) {
                update_physics(FIXED_DT);
                accumulator_ -= FIXED_DT;
            }

            // Variable timestep rendering (interpolated)
            double alpha = accumulator_ / FIXED_DT;
            render(alpha);  // Interpolate between previous and current state
        }
    }
};
```


---

## ✍️ 4. Worked Examples

### Example 09.8.1 — Unreal: Ability System Component

<details>
<summary>Create a C++ ability system that designers can extend via Blueprints</summary>

```cpp
// AbilityBase.h
UCLASS(Abstract, Blueprintable)
class MYGAME_API UAbilityBase : public UObject {
    GENERATED_BODY()

public:
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Ability")
    FName AbilityName;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Ability")
    float Cooldown = 1.0f;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Ability")
    float ManaCost = 10.0f;

    UFUNCTION(BlueprintNativeEvent, Category = "Ability")
    bool CanActivate(AActor* Owner) const;

    UFUNCTION(BlueprintNativeEvent, Category = "Ability")
    void Activate(AActor* Owner);

    // Default C++ implementations:
    bool CanActivate_Implementation(AActor* Owner) const {
        return GetWorld()->GetTimeSeconds() - LastActivationTime >= Cooldown;
    }

    void Activate_Implementation(AActor* Owner) {
        LastActivationTime = GetWorld()->GetTimeSeconds();
    }

private:
    float LastActivationTime = -999.0f;
};

// AbilityComponent.h
UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class MYGAME_API UAbilityComponent : public UActorComponent {
    GENERATED_BODY()

    UPROPERTY()
    TArray<UAbilityBase*> Abilities;

public:
    UFUNCTION(BlueprintCallable, Category = "Abilities")
    void GrantAbility(TSubclassOf<UAbilityBase> AbilityClass) {
        UAbilityBase* NewAbility = NewObject<UAbilityBase>(this, AbilityClass);
        Abilities.Add(NewAbility);
    }

    UFUNCTION(BlueprintCallable, Category = "Abilities")
    bool TryActivateAbility(FName Name) {
        for (auto* Ability : Abilities) {
            if (Ability->AbilityName == Name && Ability->CanActivate(GetOwner())) {
                Ability->Activate(GetOwner());
                return true;
            }
        }
        return false;
    }
};
```

Designers create Blueprint subclasses of `UAbilityBase` (e.g., BP_Fireball, BP_Heal) and override `Activate` with visual scripting for particles, sounds, and animations.

</details>

### Example 09.8.2 — Custom Engine: Archetype-Based ECS

<details>
<summary>Build a production-quality archetype ECS with cache-friendly iteration</summary>

```cpp
#include <vector>
#include <unordered_map>
#include <typeindex>
#include <memory>
#include <cassert>

// Archetype: a unique combination of component types
// All entities with the same components are stored together
struct Archetype {
    std::vector<std::type_index> component_types;
    std::unordered_map<std::type_index, std::vector<std::byte>> columns;
    std::vector<uint32_t> entities;  // Entity IDs in this archetype
    size_t count = 0;

    template<typename T>
    T* get_column() {
        auto it = columns.find(typeid(T));
        if (it == columns.end()) return nullptr;
        return reinterpret_cast<T*>(it->second.data());
    }

    template<typename T>
    void ensure_column(size_t capacity) {
        auto& col = columns[typeid(T)];
        col.resize(capacity * sizeof(T));
    }
};

class ArchetypeWorld {
    std::vector<std::unique_ptr<Archetype>> archetypes_;
    std::unordered_map<uint32_t, size_t> entity_archetype_;  // entity → archetype index
    std::unordered_map<uint32_t, size_t> entity_row_;        // entity → row in archetype
    uint32_t next_entity_ = 0;

public:
    template<typename... Components>
    uint32_t spawn(Components... components) {
        uint32_t entity = next_entity_++;

        // Find or create archetype for this component combination
        Archetype* arch = find_or_create_archetype<Components...>();
        size_t row = arch->count++;

        // Store entity
        arch->entities.push_back(entity);
        entity_archetype_[entity] = archetype_index(arch);
        entity_row_[entity] = row;

        // Place components
        (place_component(arch, row, std::move(components)), ...);
        return entity;
    }

    // Iterate all entities matching a component query
    template<typename... Components, typename Func>
    void query(Func&& func) {
        for (auto& arch : archetypes_) {
            // Check if archetype has all required components
            bool has_all = (arch->columns.contains(typeid(Components)) && ...);
            if (!has_all) continue;

            // Get typed pointers to each column
            auto columns = std::tuple{arch->get_column<Components>()...};

            // Iterate rows (cache-friendly: contiguous arrays)
            for (size_t i = 0; i < arch->count; ++i) {
                func(std::get<decltype(arch->get_column<Components>())>(columns)[i]...);
            }
        }
    }
};

// Usage:
ArchetypeWorld world;

// Spawn 10000 enemies (all in same archetype → contiguous memory)
for (int i = 0; i < 10000; ++i) {
    world.spawn(
        Position{rand_float(), rand_float(), 0},
        Velocity{rand_float() * 2 - 1, rand_float() * 2 - 1, 0},
        Health{100.0f, 100.0f},
        Sprite{enemy_texture, 0}
    );
}

// Movement system: processes all entities with Position + Velocity
world.query<Position, Velocity>([dt](Position& pos, Velocity& vel) {
    pos.x += vel.vx * dt;
    pos.y += vel.vy * dt;
    pos.z += vel.vz * dt;
});
// This iterates contiguous float arrays — auto-vectorizes with SIMD!
```

</details>

### Example 09.8.3 — Unreal vs Custom Engine Decision Matrix

<details>
<summary>When to use Unreal Engine vs building custom</summary>

| Factor | Use Unreal | Build Custom |
|--------|-----------|-------------|
| **Team size** | 2+ people, need collaboration | Solo or tiny team |
| **Timeline** | Ship in < 2 years | Learning project, long-term |
| **3D quality** | AAA visuals needed | Stylized or 2D |
| **Platforms** | Console + PC + Mobile | PC only (initially) |
| **Genre** | FPS, TPS, open world, RPG | Puzzle, roguelike, simulation |
| **Performance** | "Good enough" for most games | Need every microsecond (sim, HFT) |
| **Control** | Accept UE's architecture | Need custom memory, threading, rendering |
| **Revenue** | 5% royalty after $1M | No royalties |

**Hybrid approach:** Use Unreal for rendering/physics/networking, but implement game logic with ECS patterns inside Unreal's framework (using `UActorComponent` as the bridge).

</details>

---

## 💻 5. Code Patterns & Idioms

### Pattern 2.8.1 — Unreal: Component-Based Actor Design

```cpp
// GOOD: Composition via components (Unreal's preferred pattern)
UCLASS()
class AMyCharacter : public ACharacter {
    GENERATED_BODY()

    UPROPERTY(VisibleAnywhere)
    UHealthComponent* HealthComp;

    UPROPERTY(VisibleAnywhere)
    UInventoryComponent* InventoryComp;

    UPROPERTY(VisibleAnywhere)
    UAbilityComponent* AbilityComp;

public:
    AMyCharacter() {
        HealthComp = CreateDefaultSubobject<UHealthComponent>(TEXT("Health"));
        InventoryComp = CreateDefaultSubobject<UInventoryComponent>(TEXT("Inventory"));
        AbilityComp = CreateDefaultSubobject<UAbilityComponent>(TEXT("Abilities"));
    }
};

// BAD: Deep inheritance (fragile, hard to reuse)
// class AMyCharacter : public ADamageableMovableInventoryCharacter { ... }
```

### Pattern 2.8.2 — Command Pattern for Input/Replay

```cpp
// Commands are serializable actions (enables replay, undo, networking)
struct Command {
    virtual ~Command() = default;
    virtual void execute(GameState& state) = 0;
    virtual void undo(GameState& state) = 0;
};

struct MoveCommand : Command {
    uint32_t entity_id;
    Vec3 direction;
    float distance;
    Vec3 previous_position;  // For undo

    void execute(GameState& state) override {
        auto& pos = state.get_position(entity_id);
        previous_position = pos;
        pos += direction * distance;
    }

    void undo(GameState& state) override {
        state.get_position(entity_id) = previous_position;
    }
};

// Command buffer enables:
// 1. Replay: save all commands, replay them
// 2. Networking: send commands to server
// 3. Undo: pop last command and call undo()
class CommandBuffer {
    std::vector<std::unique_ptr<Command>> history_;
public:
    void execute(std::unique_ptr<Command> cmd, GameState& state) {
        cmd->execute(state);
        history_.push_back(std::move(cmd));
    }
    void undo(GameState& state) {
        if (!history_.empty()) {
            history_.back()->undo(state);
            history_.pop_back();
        }
    }
};
```

### Pattern 2.8.3 — Object Pooling (Avoid Runtime Allocation)

```cpp
template<typename T, size_t MaxObjects = 1024>
class ObjectPool {
    std::array<std::aligned_storage_t<sizeof(T), alignof(T)>, MaxObjects> storage_;
    std::vector<size_t> free_indices_;
    std::bitset<MaxObjects> active_;

public:
    ObjectPool() {
        free_indices_.reserve(MaxObjects);
        for (size_t i = MaxObjects; i > 0; --i) {
            free_indices_.push_back(i - 1);
        }
    }

    template<typename... Args>
    T* acquire(Args&&... args) {
        if (free_indices_.empty()) return nullptr;
        size_t idx = free_indices_.back();
        free_indices_.pop_back();
        active_.set(idx);
        return new (&storage_[idx]) T(std::forward<Args>(args)...);
    }

    void release(T* obj) {
        size_t idx = (reinterpret_cast<std::byte*>(obj) -
                      reinterpret_cast<std::byte*>(&storage_[0])) / sizeof(storage_[0]);
        obj->~T();
        active_.reset(idx);
        free_indices_.push_back(idx);
    }

    // Iterate active objects
    template<typename Func>
    void for_each_active(Func&& func) {
        for (size_t i = 0; i < MaxObjects; ++i) {
            if (active_.test(i)) {
                func(*reinterpret_cast<T*>(&storage_[i]));
            }
        }
    }
};

// Usage: bullets never allocate at runtime
ObjectPool<Bullet, 4096> bullet_pool;
auto* b = bullet_pool.acquire(pos, vel, damage);
// ... on hit:
bullet_pool.release(b);
```

---

## ⚠️ 6. Gotchas & Anti-Patterns

### Gotcha 2.8.1 — Raw Pointers to UObjects

```cpp
// BUG: Raw pointer not tracked by GC — can dangle!
AActor* CachedTarget;  // If target is destroyed, this becomes garbage

// FIX: Use UPROPERTY or TWeakObjectPtr
UPROPERTY()
AActor* SafeTarget;  // GC-tracked

TWeakObjectPtr<AActor> WeakTarget;  // Auto-nulls when target is GC'd
if (WeakTarget.IsValid()) { /* safe to use */ }
```

### Gotcha 2.8.2 — Unreal Constructor vs BeginPlay

```cpp
// BUG: Trying to find other actors in constructor
AMyActor::AMyActor() {
    // GetWorld() returns nullptr here!
    // FindActorOfClass() will crash!
    auto* Player = GetWorld()->GetFirstPlayerController();  // CRASH
}

// FIX: Use BeginPlay for runtime queries
void AMyActor::BeginPlay() {
    Super::BeginPlay();
    auto* Player = GetWorld()->GetFirstPlayerController();  // Safe
}
```

### Gotcha 2.8.3 — Tick Performance in Unreal

```cpp
// BAD: Ticking 10000 actors every frame
// Each Tick has overhead: virtual call + UObject machinery

// GOOD: Disable tick on actors that don't need it
AMyActor::AMyActor() {
    PrimaryActorTick.bCanEverTick = false;  // Disable tick
}

// BETTER: Use timers for periodic work
GetWorldTimerManager().SetTimer(TimerHandle, this,
    &AMyActor::CheckForEnemies, 0.5f, true);  // Every 0.5s, not every frame

// BEST: Batch process with a manager actor
// One manager ticks and processes all entities in a tight loop
```

### Gotcha 2.8.4 — ECS: Component Access Patterns

```cpp
// BAD: Random access pattern (cache-hostile)
for (Entity e : all_entities) {
    if (has<Position>(e) && has<Velocity>(e)) {
        auto& pos = get<Position>(e);  // Potential cache miss
        auto& vel = get<Velocity>(e);  // Another potential cache miss
        pos.x += vel.vx * dt;
    }
}

// GOOD: Archetype iteration (cache-friendly)
// All entities with same components stored contiguously
for (auto& archetype : archetypes_with<Position, Velocity>()) {
    auto* positions = archetype.get_array<Position>();
    auto* velocities = archetype.get_array<Velocity>();
    for (size_t i = 0; i < archetype.count(); ++i) {
        positions[i].x += velocities[i].vx * dt;  // Sequential access
    }
}
```

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- **Previous:** [09.7 - Performance - SIMD, Memory Layout & Cache Optimization](09.7---Performance---SIMD,-Memory-Layout-&-Cache-Optimization)
- **Performance patterns:** [09.7 - Performance - SIMD, Memory Layout & Cache Optimization](09.7---Performance---SIMD,-Memory-Layout-&-Cache-Optimization) (SoA, cache optimization)
- **Engine architecture:** [28.5 - Game Engine Architectures - Unity & Unreal](28.5---Game-Engine-Architectures---Unity-&-Unreal)
- **Game design patterns:** [Track 04 Game_Dev](Track-04-Game_Dev)
- **Python game scripting:** [08.3 - OOP, Data Models & Pythonic Idioms](08.3---OOP,-Data-Models-&-Pythonic-Idioms) (comparison)

### External Resources
- [Unreal Engine C++ Documentation](https://docs.unrealengine.com/en-US/programming-with-cplusplus-in-unreal-engine/)
- [Unreal Engine API Reference](https://docs.unrealengine.com/en-US/API/)
- [Game Engine Architecture (Jason Gregory)](https://www.gameenginebook.com/) — The definitive book
- [Data-Oriented Design (Richard Fabian)](https://www.dataorienteddesign.com/dodbook/)
- [EnTT (ECS library)](https://github.com/skypjack/entt) — Production C++ ECS
- [CppCon: "Data-Oriented Design in Practice"](https://www.youtube.com/results?search_query=cppcon+data+oriented+design)
- [TheCherno: Game Engine Series](https://www.youtube.com/playlist?list=PLlrATfBNZ98dC-V-N3m0Go4deliWHPFR-)
- [GDC Vault: Overwatch ECS](https://www.youtube.com/results?search_query=gdc+overwatch+ecs)

---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — UFUNCTION Reflection Internals

**Problem:** Understand how Unreal's reflection system (UHT — Unreal Header Tool) works under the hood. Implement a simplified version showing how `UFUNCTION`, `UPROPERTY`, and `UCLASS` macros generate metadata.

<details>
<summary>🔍 Full step-by-step solution</summary>

```cpp
// ═══════════════════════════════════════════════════════════════
// What UFUNCTION/UPROPERTY actually expand to (simplified)
// ═══════════════════════════════════════════════════════════════

// When you write:
UCLASS()
class AMyActor : public AActor {
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float Health = 100.0f;

    UFUNCTION(BlueprintCallable, Category = "Combat")
    void TakeDamage(float Amount);
};

// The Unreal Header Tool (UHT) generates a .generated.h file containing:
// 1. Static metadata structs describing every reflected member
// 2. Thunk functions for Blueprint VM to call your C++ functions
// 3. Registration code that runs at startup

// ═══════════════════════════════════════════════════════════════
// Simplified recreation of the reflection system
// ═══════════════════════════════════════════════════════════════

#include <string>
#include <vector>
#include <unordered_map>
#include <functional>
#include <any>
#include <typeindex>

// Property metadata (like UProperty)
struct PropertyInfo {
    std::string name;
    std::string type_name;
    size_t offset;          // Byte offset within the object
    size_t size;
    bool is_editable;       // EditAnywhere
    bool is_blueprint_visible;  // BlueprintReadWrite
    std::string category;
};

// Function metadata (like UFunction)
struct FunctionInfo {
    std::string name;
    std::string category;
    bool is_blueprint_callable;
    // Thunk: type-erased function pointer that the scripting VM calls
    std::function<void(void* object, void* params)> thunk;
};

// Class metadata (like UClass)
struct ClassInfo {
    std::string name;
    std::string parent_name;
    size_t object_size;
    std::vector<PropertyInfo> properties;
    std::vector<FunctionInfo> functions;
    std::function<void*()> constructor;  // Default object factory
};

// Global registry (like UClass static registry)
class ReflectionRegistry {
    std::unordered_map<std::string, ClassInfo> classes_;
    static ReflectionRegistry& instance() {
        static ReflectionRegistry reg;
        return reg;
    }
public:
    static void register_class(ClassInfo info) {
        instance().classes_[info.name] = std::move(info);
    }
    static const ClassInfo* find_class(const std::string& name) {
        auto it = instance().classes_.find(name);
        return it != instance().classes_.end() ? &it->second : nullptr;
    }
};

// ═══════════════════════════════════════════════════════════════
// How Unreal's generated code actually works (real UE5 pattern)
// ═══════════════════════════════════════════════════════════════

// For UFUNCTION(BlueprintCallable) void TakeDamage(float Amount):
// UHT generates a "thunk" function:
/*
DEFINE_FUNCTION(AMyActor::execTakeDamage) {
    P_GET_PROPERTY(FFloatProperty, Z_Param_Amount);
    P_FINISH;  // End of parameter parsing

    P_THIS->TakeDamage(Z_Param_Amount);
}
*/
// This thunk is what the Blueprint VM calls. It:
// 1. Reads parameters from the Blueprint stack (P_GET_PROPERTY)
// 2. Calls your actual C++ function
// 3. Pushes return value back to Blueprint stack (if any)

// For UPROPERTY(EditAnywhere) float Health:
// UHT generates metadata that tells the editor:
// - Name: "Health"
// - Type: Float
// - Offset: offsetof(AMyActor, Health)
// - Flags: CPF_Edit | CPF_BlueprintVisible
// The editor uses this to create property widgets without knowing the C++ type

// ═══════════════════════════════════════════════════════════════
// The GENERATED_BODY() macro expands to:
// ═══════════════════════════════════════════════════════════════
/*
#define GENERATED_BODY() \
    friend struct Z_Construct_UClass_AMyActor_Statics; \
    static UClass* StaticClass(); \
    void* operator new(size_t Size, EInternal InternalOnly, UObject* Outer, ...); \
    // ... more internal machinery
*/

// At startup, Unreal calls Z_Construct_UClass_AMyActor() which:
// 1. Creates the UClass object for AMyActor
// 2. Registers all UPROPERTY metadata (name, type, offset, flags)
// 3. Registers all UFUNCTION metadata (name, thunk pointer, flags)
// 4. Links to parent class (AActor)
// 5. Stores the CDO (Class Default Object) — a template instance
```

**Key insight:** Unreal's reflection is entirely code-generated at compile time by UHT. There's no runtime parsing or dynamic type creation. The "magic" is just a code generator that reads your macros and produces static metadata tables.

</details>

### Example 8.2 — Replication Graph for Multiplayer

**Problem:** Implement a relevancy-based replication system where the server only sends entity updates to clients that can actually see them, reducing bandwidth by 80%+.

<details>
<summary>🔍 Full step-by-step solution</summary>

```cpp
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <bitset>
#include <cmath>
#include <fmt/core.h>

// ═══════════════════════════════════════════════════════════════
// Replication Graph: Unreal's system for efficient net relevancy
// ═══════════════════════════════════════════════════════════════

// In a 100-player battle royale with 10,000 replicated actors:
// Naive: send ALL 10,000 actors to ALL 100 clients = 1,000,000 updates/tick
// Replication Graph: send only RELEVANT actors = ~50,000 updates/tick (20x reduction)

struct NetConnection {
    uint32_t client_id;
    float view_x, view_y, view_z;
    float view_distance;
};

struct ReplicatedActor {
    uint32_t actor_id;
    float x, y, z;
    uint32_t relevancy_group;  // Spatial grid cell
    bool is_always_relevant;   // e.g., game state, player controller
    bool is_dormant;           // Not changed recently — skip
    uint64_t last_replicated_frame;
};

// Spatial grid for fast relevancy queries
class SpatialGrid {
    static constexpr float CELL_SIZE = 500.0f;  // 5m cells
    std::unordered_map<uint64_t, std::vector<uint32_t>> cells_;

    uint64_t cell_key(float x, float y) const {
        int cx = static_cast<int>(x / CELL_SIZE);
        int cy = static_cast<int>(y / CELL_SIZE);
        return (static_cast<uint64_t>(cx) << 32) | static_cast<uint32_t>(cy);
    }

public:
    void insert(uint32_t actor_id, float x, float y) {
        cells_[cell_key(x, y)].push_back(actor_id);
    }

    // Get all actors in cells within radius
    std::vector<uint32_t> query_radius(float x, float y, float radius) const {
        std::vector<uint32_t> result;
        int cell_radius = static_cast<int>(radius / CELL_SIZE) + 1;
        int cx = static_cast<int>(x / CELL_SIZE);
        int cy = static_cast<int>(y / CELL_SIZE);

        for (int dx = -cell_radius; dx <= cell_radius; ++dx) {
            for (int dy = -cell_radius; dy <= cell_radius; ++dy) {
                uint64_t key = (static_cast<uint64_t>(cx + dx) << 32) |
                               static_cast<uint32_t>(cy + dy);
                auto it = cells_.find(key);
                if (it != cells_.end()) {
                    result.insert(result.end(),
                        it->second.begin(), it->second.end());
                }
            }
        }
        return result;
    }

    void clear() { cells_.clear(); }
};

class ReplicationGraph {
    std::vector<ReplicatedActor> actors_;
    std::vector<NetConnection> connections_;
    SpatialGrid grid_;
    uint64_t current_frame_ = 0;

    // Priority: how urgently does this client need this actor's update?
    float compute_priority(const NetConnection& conn,
                          const ReplicatedActor& actor) const {
        if (actor.is_always_relevant) return 1000.0f;
        if (actor.is_dormant) return 0.0f;

        float dx = actor.x - conn.view_x;
        float dy = actor.y - conn.view_y;
        float dist = std::sqrt(dx * dx + dy * dy);

        // Closer = higher priority, stale = higher priority
        float distance_factor = 1.0f - (dist / conn.view_distance);
        float staleness = static_cast<float>(
            current_frame_ - actor.last_replicated_frame);

        return distance_factor * 10.0f + staleness * 0.5f;
    }

public:
    // Called every server tick (e.g., 30Hz)
    void gather_and_replicate(int max_actors_per_client) {
        ++current_frame_;

        // Rebuild spatial grid
        grid_.clear();
        for (auto& actor : actors_) {
            if (!actor.is_dormant) {
                grid_.insert(actor.actor_id, actor.x, actor.y);
            }
        }

        // For each client connection:
        for (auto& conn : connections_) {
            // 1. Get potentially relevant actors (spatial query)
            auto candidates = grid_.query_radius(
                conn.view_x, conn.view_y, conn.view_distance);

            // 2. Add always-relevant actors
            for (auto& actor : actors_) {
                if (actor.is_always_relevant) {
                    candidates.push_back(actor.actor_id);
                }
            }

            // 3. Prioritize and take top N
            struct PrioritizedActor {
                uint32_t id;
                float priority;
            };
            std::vector<PrioritizedActor> prioritized;
            for (uint32_t id : candidates) {
                float p = compute_priority(conn, actors_[id]);
                if (p > 0) prioritized.push_back({id, p});
            }

            std::partial_sort(prioritized.begin(),
                prioritized.begin() + std::min(
                    static_cast<int>(prioritized.size()), max_actors_per_client),
                prioritized.end(),
                [](const auto& a, const auto& b) {
                    return a.priority > b.priority;
                });

            // 4. Replicate top-priority actors to this client
            int count = std::min(static_cast<int>(prioritized.size()),
                                 max_actors_per_client);
            for (int i = 0; i < count; ++i) {
                replicate_actor_to_client(conn, actors_[prioritized[i].id]);
            }
        }
    }

    void replicate_actor_to_client(const NetConnection& conn,
                                   ReplicatedActor& actor) {
        // Serialize changed properties and send to client
        actor.last_replicated_frame = current_frame_;
        // ... network send ...
    }
};
```

</details>

### Example 8.3 — Niagara Particle System vs Custom GPU Compute

**Problem:** Compare Unreal's Niagara particle system with a custom compute shader approach for simulating 1 million particles with inter-particle forces.

<details>
<summary>🔍 Full step-by-step solution</summary>

```cpp
// ═══════════════════════════════════════════════════════════════
// APPROACH 1: Unreal Niagara (Blueprint/Script-driven)
// ═══════════════════════════════════════════════════════════════

// Niagara Module Script (HLSL-like, runs on GPU):
/*
// NiagaraModule_CustomForce.ush
void SimulateParticleForce(
    in float3 Position,
    in float3 Velocity,
    in float DeltaTime,
    in float3 AttractorPosition,
    in float AttractorStrength,
    out float3 OutVelocity)
{
    float3 ToAttractor = AttractorPosition - Position;
    float Distance = length(ToAttractor);
    float3 Force = normalize(ToAttractor) * AttractorStrength / (Distance * Distance + 1.0);
    OutVelocity = Velocity + Force * DeltaTime;
}
*/

// C++ setup for Niagara system:
// In your Actor's BeginPlay:
/*
UPROPERTY(EditAnywhere)
UNiagaraSystem* ParticleSystemAsset;

void AParticleActor::BeginPlay() {
    Super::BeginPlay();
    NiagaraComp = UNiagaraFunctionLibrary::SpawnSystemAtLocation(
        GetWorld(), ParticleSystemAsset, GetActorLocation());

    // Set parameters from C++
    NiagaraComp->SetVariableFloat(FName("AttractorStrength"), 500.0f);
    NiagaraComp->SetVariableVec3(FName("AttractorPosition"), FVector(0, 0, 100));
}
*/

// ═══════════════════════════════════════════════════════════════
// APPROACH 2: Custom Compute Shader (full control)
// ═══════════════════════════════════════════════════════════════

// ComputeShader.usf (Unreal Shader File):
/*
#include "/Engine/Private/Common.ush"

RWStructuredBuffer<float4> Positions;   // xyz = pos, w = mass
RWStructuredBuffer<float4> Velocities;  // xyz = vel, w = lifetime

float DeltaTime;
float3 AttractorPos;
float AttractorStrength;
uint NumParticles;

[numthreads(256, 1, 1)]
void MainCS(uint3 ThreadId : SV_DispatchThreadID) {
    uint idx = ThreadId.x;
    if (idx >= NumParticles) return;

    float3 pos = Positions[idx].xyz;
    float3 vel = Velocities[idx].xyz;
    float mass = Positions[idx].w;

    // Gravity toward attractor
    float3 toAttractor = AttractorPos - pos;
    float dist = length(toAttractor);
    float3 force = normalize(toAttractor) * AttractorStrength / (dist * dist + 1.0);

    // N-body: interact with nearby particles (simplified: grid-based)
    // In production, use spatial hashing on GPU

    // Euler integration
    vel += (force / mass) * DeltaTime;
    pos += vel * DeltaTime;

    // Damping
    vel *= 0.999;

    Positions[idx] = float4(pos, mass);
    Velocities[idx] = float4(vel, Velocities[idx].w - DeltaTime);
}
*/

// C++ dispatch code:
/*
class FParticleComputeShader : public FGlobalShader {
    DECLARE_GLOBAL_SHADER(FParticleComputeShader);
    SHADER_USE_PARAMETER_STRUCT(FParticleComputeShader, FGlobalShader);

    BEGIN_SHADER_PARAMETER_STRUCT(FParameters, )
        SHADER_PARAMETER_UAV(RWStructuredBuffer<FVector4f>, Positions)
        SHADER_PARAMETER_UAV(RWStructuredBuffer<FVector4f>, Velocities)
        SHADER_PARAMETER(float, DeltaTime)
        SHADER_PARAMETER(FVector3f, AttractorPos)
        SHADER_PARAMETER(float, AttractorStrength)
        SHADER_PARAMETER(uint32, NumParticles)
    END_SHADER_PARAMETER_STRUCT()
};

void DispatchParticleCompute(FRHICommandListImmediate& RHICmdList,
                             uint32 NumParticles, float DeltaTime) {
    FParticleComputeShader::FParameters Params;
    Params.Positions = PositionBufferUAV;
    Params.Velocities = VelocityBufferUAV;
    Params.DeltaTime = DeltaTime;
    Params.NumParticles = NumParticles;

    uint32 GroupCount = FMath::DivideAndRoundUp(NumParticles, 256u);
    FComputeShaderUtils::Dispatch(RHICmdList, Shader, Params, FIntVector(GroupCount, 1, 1));
}
*/

// ═══════════════════════════════════════════════════════════════
// Decision: Niagara vs Custom Compute
// ═══════════════════════════════════════════════════════════════

// | Factor              | Niagara              | Custom Compute       |
// |---------------------|----------------------|----------------------|
// | Setup time          | Minutes (visual)     | Days (shader code)   |
// | Artist iteration    | Excellent            | None (code only)     |
// | Performance ceiling | Good (1M particles)  | Maximum (10M+)       |
// | Inter-particle sim  | Limited              | Full control         |
// | Rendering           | Built-in (ribbons,   | Must write renderer  |
// |                     | meshes, sprites)     |                      |
// | Debugging           | Visual debugger      | RenderDoc/PIX        |
// | Portability         | UE only              | Any engine           |

// Recommendation:
// - Use Niagara for: VFX, environmental particles, anything artists touch
// - Use Custom Compute for: physics simulation, fluid dynamics, cloth,
//   anything needing inter-particle forces or custom algorithms
```

</details>



---

## 📘 9. Appendix: Extended Derivations & Special Cases

### 9.1 Unreal's Garbage Collector — How It Works

**Unreal Engine uses a mark-and-sweep garbage collector for UObjects.** Unlike C#/Java's GC, Unreal's GC is deterministic, runs on the game thread, and is designed for real-time applications.

#### The GC Algorithm

```
Phase 1: MARK (find all reachable objects)
├── Start from "root set" (objects explicitly kept alive)
│   ├── Objects referenced by UPROPERTY() members
│   ├── Objects in the global UObject array
│   ├── Objects added to root set via AddToRoot()
│   └── Objects referenced from the stack (conservative scan)
├── Traverse all UPROPERTY() pointers recursively
│   └── Mark each reachable object as "alive"
└── Any unmarked object is garbage

Phase 2: SWEEP (destroy unreachable objects)
├── Iterate all UObjects
├── Destroy unmarked objects (call destructor, free memory)
└── Compact the UObject array (fill holes)
```

#### GC Performance Characteristics

```cpp
// GC runs periodically (default: every 60 seconds, or when memory pressure)
// Typical GC pause: 1-5ms for 100,000 UObjects
// Worst case: 20ms+ for millions of UObjects (causes frame hitch!)

// ═══════════════════════════════════════════════════════════════
// How to avoid GC hitches:
// ═══════════════════════════════════════════════════════════════

// 1. Reduce UObject count (use structs for small data)
// BAD: 10,000 UObjects for inventory items
UCLASS()
class UInventoryItem : public UObject { /* ... */ };

// GOOD: Use USTRUCT (not GC-tracked, much cheaper)
USTRUCT(BlueprintType)
struct FInventoryItem {
    GENERATED_BODY()
    UPROPERTY() FName ItemID;
    UPROPERTY() int32 Quantity;
};

// 2. Object pooling (reuse instead of create/destroy)
UCLASS()
class ABulletPool : public AActor {
    UPROPERTY()
    TArray<ABullet*> Pool;

    ABullet* Acquire() {
        if (Pool.Num() > 0) {
            ABullet* B = Pool.Pop();
            B->SetActorHiddenInGame(false);
            return B;
        }
        return GetWorld()->SpawnActor<ABullet>();
    }

    void Release(ABullet* B) {
        B->SetActorHiddenInGame(true);
        Pool.Add(B);
    }
};

// 3. Incremental GC (UE5): spreads work across multiple frames
// Set in DefaultEngine.ini:
// [/Script/Engine.GarbageCollectionSettings]
// gc.MaxObjectsNotConsideredByGC=1000000
// gc.TimeBetweenPurgingPendingKillObjects=60
// gc.IncrementalBeginDestroyEnabled=true
```

#### UPROPERTY and GC Roots

```cpp
// UPROPERTY() is the ONLY way to tell GC about a reference:
UCLASS()
class AMyActor : public AActor {
    UPROPERTY()  // GC-tracked: object won't be collected while AMyActor lives
    UTexture2D* Texture;

    UTexture2D* DangerousTexture;  // NOT tracked! GC may collect this!
    // If GC runs and nothing else references DangerousTexture → dangling pointer!
};

// TWeakObjectPtr: safe reference that auto-nulls when object is GC'd
TWeakObjectPtr<AActor> WeakRef = SomeActor;
// Later:
if (WeakRef.IsValid()) {
    WeakRef->DoSomething();  // Safe
}
// If SomeActor was GC'd, WeakRef.IsValid() returns false
```

### 9.2 Pipeline State Object (PSO) Precaching

**PSO (Pipeline State Object) represents the complete GPU pipeline configuration** — shaders, blend state, rasterizer state, depth-stencil state, vertex layout, render target formats. Creating a PSO is expensive (can take 10-100ms). If a new PSO is needed mid-frame, you get a visible hitch.

#### The Problem

```
Frame 1-100: Player in forest (uses forest shaders, PSOs already cached)
Frame 101: Player enters cave (new materials → new PSOs needed)
           GPU stalls for 50ms compiling new PSOs → VISIBLE HITCH
```

#### Unreal's PSO Precaching System

```cpp
// ═══════════════════════════════════════════════════════════════
// Step 1: Record PSOs during development/testing
// ═══════════════════════════════════════════════════════════════

// In DefaultEngine.ini:
// [/Script/Engine.RendererSettings]
// r.ShaderPipelineCache.Enabled=1
// r.ShaderPipelineCache.LogPSO=1
// r.ShaderPipelineCache.SaveBoundPSOLog=1

// Play through the entire game → generates .upipelinecache file
// This file records every PSO combination encountered

// ═══════════════════════════════════════════════════════════════
// Step 2: Precache at load time
// ═══════════════════════════════════════════════════════════════

// Unreal automatically loads the .upipelinecache on startup and
// compiles all recorded PSOs in the background during loading screen.

// For streaming levels, precache when level starts loading:
/*
void AMyGameMode::PreloadLevel(FName LevelName) {
    // Trigger PSO precaching for the target level's materials
    FShaderPipelineCache::SetBatchMode(FShaderPipelineCache::BatchMode::Background);

    // Load level's PSO cache
    FString CachePath = FPaths::ProjectSavedDir() / TEXT("PSOCache") / LevelName.ToString();
    FShaderPipelineCache::OpenPipelineFileCache(CachePath, GMaxRHIShaderPlatform);
}
*/

// ═══════════════════════════════════════════════════════════════
// Step 3: Custom PSO precaching for procedural content
// ═══════════════════════════════════════════════════════════════

// For procedurally generated materials (can't pre-record):
/*
void PrecacheMaterialPSOs(UMaterialInterface* Material) {
    // Get all mesh types this material might be used with
    TArray<FVertexFactoryType*> VertexFactories;
    VertexFactories.Add(FLocalVertexFactory::StaticType);
    VertexFactories.Add(FGPUSkinVertexFactory::StaticType);

    // Request PSO compilation for each combination
    for (auto* VF : VertexFactories) {
        Material->PrecachePSOs(VF, PSOPrecacheParams);
    }
}
*/
```

#### PSO Precaching Best Practices

| Strategy | When to Use | Hitch Risk |
|----------|-------------|------------|
| Recorded cache (.upipelinecache) | Shipping builds | Low (if testing was thorough) |
| Background compilation | Loading screens | None (async) |
| Bundled PSO cache | DLC/patches | Low |
| Runtime precache on level stream | Open world | Medium (if too late) |
| Placeholder shader while compiling | Any | None (visual pop-in instead of hitch) |

### 9.3 Custom Engine Architecture — The Game Loop

**Every game engine, from Unreal to a 500-line hobby engine, follows the same fundamental loop.** Understanding this architecture is essential for building or extending any engine.

```cpp
// The canonical game loop structure:
class Engine {
    bool running_ = true;
    double accumulator_ = 0.0;
    static constexpr double FIXED_DT = 1.0 / 60.0;  // 60Hz physics

public:
    void run() {
        initialize();

        auto previous_time = Clock::now();

        while (running_) {
            auto current_time = Clock::now();
            double frame_time = seconds(current_time - previous_time);
            previous_time = current_time;

            // Cap frame time to prevent spiral of death
            if (frame_time > 0.25) frame_time = 0.25;

            // ═══════════════════════════════════════════════════
            // Phase 1: INPUT (poll hardware, generate events)
            // ═══════════════════════════════════════════════════
            poll_input();

            // ═══════════════════════════════════════════════════
            // Phase 2: FIXED UPDATE (deterministic physics/logic)
            // Runs at fixed rate regardless of frame rate
            // ═══════════════════════════════════════════════════
            accumulator_ += frame_time;
            while (accumulator_ >= FIXED_DT) {
                fixed_update(FIXED_DT);  // Physics, networking, game logic
                accumulator_ -= FIXED_DT;
            }

            // ═══════════════════════════════════════════════════
            // Phase 3: VARIABLE UPDATE (frame-rate dependent)
            // ═══════════════════════════════════════════════════
            double alpha = accumulator_ / FIXED_DT;  // Interpolation factor
            update(frame_time, alpha);  // Animation, particles, camera

            // ═══════════════════════════════════════════════════
            // Phase 4: RENDER (submit draw calls to GPU)
            // ═══════════════════════════════════════════════════
            render(alpha);  // Interpolate between physics states for smooth visuals

            // ═══════════════════════════════════════════════════
            // Phase 5: PRESENT (swap buffers, wait for vsync)
            // ═══════════════════════════════════════════════════
            present();
        }

        shutdown();
    }

private:
    void fixed_update(double dt) {
        // Deterministic: same input → same output (important for networking)
        physics_system_.step(dt);
        game_logic_system_.update(dt);
        network_system_.tick(dt);
    }

    void update(double dt, double alpha) {
        // Non-deterministic: visual-only updates
        animation_system_.update(dt);
        particle_system_.update(dt);
        audio_system_.update(dt);
        camera_system_.update(dt, alpha);
    }

    void render(double alpha) {
        // Interpolate positions: visual_pos = lerp(prev_pos, curr_pos, alpha)
        // This gives smooth motion even when physics runs at lower rate
        renderer_.begin_frame();
        renderer_.render_scene(scene_, alpha);
        ui_system_.render();
        renderer_.end_frame();
    }
};
```

**Why fixed timestep matters:**
- Physics is deterministic (same input → same output) — essential for networking
- No "tunneling" (fast objects passing through walls at low FPS)
- Consistent game feel regardless of hardware
- Replay systems work perfectly (just replay inputs)

**Why interpolation matters:**
- Physics at 60Hz, rendering at 144Hz → without interpolation, objects "stutter"
- `alpha` = how far between the last two physics states we are
- `visual_pos = prev_pos + (curr_pos - prev_pos) * alpha` → butter-smooth motion

---

*This is the final chapter of Track 02. Return to [Subject_Plan](Subject_Plan) or [LEARNING_PATH](LEARNING_PATH) for next steps.*