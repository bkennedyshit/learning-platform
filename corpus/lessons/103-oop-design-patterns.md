---
title: "10.3 — OOP & Design Patterns"
subject: "C#"
catalog: advanced
audience_tier: higher-education
chapter: "10.3"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 10.3 — OOP & Design Patterns

> *"Favor object composition over class inheritance."* — Gang of Four, *Design Patterns* (1994)

Python's OOP is protocol-based and duck-typed. C#'s OOP is interface-based and statically checked. The patterns are the same — Observer, State, Command, Factory — but C# gives you compile-time guarantees that Python can only approximate with `Protocol` and mypy. This chapter teaches you to architect game systems that are testable, extensible, and don't collapse into spaghetti at 10,000 lines.

---

## 🎯 Learning Objectives

1. Design with interfaces and composition instead of deep inheritance.
2. Apply SOLID principles in game contexts.
3. Implement Observer (event bus), Command (undo/redo), State Machine, Factory, and Strategy patterns.
4. Use C# events, delegates, and `Action`/`Func` for decoupled communication.
5. Understand when inheritance IS appropriate (template method, polymorphic collections).

---

## 🖼️ Visual Anchor — Composition vs Inheritance

![csharp__3.3-fig1](csharp__3.3-fig1.svg)

---

## 📚 1. Concepts

### Concept 3.3.1 — Interfaces (C#'s Protocol)

```csharp
// Python Protocol equivalent — but enforced at compile time
public interface IDamageable
{
    float CurrentHealth { get; }
    float MaxHealth { get; }
    void TakeDamage(float amount, DamageType type);
    event Action<float>? OnHealthChanged;
}

public interface IInteractable
{
    string InteractionPrompt { get; }
    void Interact(PlayerController player);
    bool CanInteract(PlayerController player);
}

// A class can implement multiple interfaces (no diamond problem)
public class CropPlot : MonoBehaviour, IDamageable, IInteractable, ISaveable
{
    // Must implement ALL members from ALL interfaces
}
```

**Key difference from Python:** In Python, any object with the right methods satisfies a `Protocol`. In C#, you must explicitly declare `class Foo : IBar`. The compiler then guarantees you've implemented everything.

### Concept 3.3.2 — Abstract Classes vs Interfaces

| Feature | Interface | Abstract Class |
|---------|-----------|----------------|
| Multiple inheritance | ✓ (implement many) | ✗ (inherit one) |
| Fields/state | ✗ (no instance fields) | ✓ |
| Constructor | ✗ | ✓ |
| Default implementation | ✓ (C# 8+) | ✓ |
| Access modifiers | Public only (until C# 11) | Any |
| Use when | Defining a capability/contract | Sharing implementation + contract |

```csharp
// Abstract class: shared implementation
public abstract class BaseEnemy : MonoBehaviour, IDamageable
{
    [SerializeField] protected float maxHealth = 100f;
    public float CurrentHealth { get; protected set; }
    public float MaxHealth => maxHealth;
    public event Action<float>? OnHealthChanged;

    // Template Method pattern: subclasses override specific behavior
    public void TakeDamage(float amount, DamageType type)
    {
        float modified = CalculateResistance(amount, type);  // Hook
        CurrentHealth -= modified;
        OnHealthChanged?.Invoke(CurrentHealth);
        if (CurrentHealth <= 0) Die();
    }

    protected abstract float CalculateResistance(float amount, DamageType type);
    protected abstract void Die();
}

// Concrete: only implements the varying parts
public class SlimeEnemy : BaseEnemy
{
    protected override float CalculateResistance(float amount, DamageType type)
        => type == DamageType.Fire ? amount * 2f : amount * 0.5f;

    protected override void Die()
    {
        SpawnSlimeBalls(3);
        Destroy(gameObject);
    }
}
```

### Concept 3.3.3 — SOLID Principles for Games

| Principle | Game Example |
|-----------|-------------|
| **S**ingle Responsibility | `PlayerMovement` handles movement. `PlayerInventory` handles items. Not one god-class `Player`. |
| **O**pen/Closed | New crop types via ScriptableObjects, not modifying `CropSystem` code. |
| **L**iskov Substitution | Any `IDamageable` can be damaged — whether it's a player, enemy, or destructible prop. |
| **I**nterface Segregation | `IInteractable` is separate from `IDamageable`. A sign post is interactable but not damageable. |
| **D**ependency Inversion | `CropSystem` depends on `IWeatherService`, not `ConcreteWeatherManager`. Testable. |

---

## 📐 2. Mental Models

### Model 3.3.1 — The Composition Checklist

Before creating an inheritance hierarchy, ask:
1. **Is-a or Has-a?** A Slime IS-A enemy (inheritance OK). A Player HAS-A inventory (composition).
2. **Will it change independently?** Movement and combat evolve separately → separate components.
3. **Do I need polymorphic collections?** `List<IEnemy>` → interface. `List<BaseEnemy>` → abstract class.
4. **More than 2 levels deep?** Stop. Flatten with interfaces + composition.

### Model 3.3.2 — Events as Decoupling Glue

```
┌──────────────┐     event      ┌──────────────┐
│ CropSystem   │ ──────────────▶│ UI Manager   │
│              │  OnCropHarvest  │ (updates HUD)│
└──────────────┘                └──────────────┘
       │ event                         ▲
       │ OnCropHarvest                 │ event
       ▼                               │ OnCropHarvest
┌──────────────┐                ┌──────────────┐
│ Audio System │                │ Achievement  │
│ (plays SFX)  │                │ Tracker      │
└──────────────┘                └──────────────┘
```

The `CropSystem` doesn't know about UI, audio, or achievements. It just fires an event. Anyone can subscribe.


---

## 🔑 3. Mechanics — Design Patterns for Games

### 10.1 — Observer Pattern (Event Bus)

```csharp
// C# events with delegates
public class GameEvents
{
    // Singleton event bus (or use DI)
    public static GameEvents Instance { get; } = new();

    // Typed events
    public event Action<CropData, Vector2Int>? OnCropHarvested;
    public event Action<int>? OnGoldChanged;
    public event Action<Season>? OnSeasonChanged;
    public event Action<TimeSpan>? OnDayEnded;

    // Fire methods (encapsulate invocation)
    public void CropHarvested(CropData crop, Vector2Int tile)
        => OnCropHarvested?.Invoke(crop, tile);

    public void GoldChanged(int newAmount)
        => OnGoldChanged?.Invoke(newAmount);
}

// Subscriber (UI)
public class GoldDisplay : MonoBehaviour
{
    [SerializeField] private TMP_Text goldText;

    void OnEnable() => GameEvents.Instance.OnGoldChanged += UpdateDisplay;
    void OnDisable() => GameEvents.Instance.OnGoldChanged -= UpdateDisplay;

    private void UpdateDisplay(int gold) => goldText.text = $"{gold:N0}g";
}
```

### 10.2 — Command Pattern (Undo/Redo)

```csharp
public interface ICommand
{
    void Execute();
    void Undo();
    string Description { get; }
}

public class PlaceCropCommand : ICommand
{
    private readonly FarmGrid _grid;
    private readonly Vector2Int _position;
    private readonly CropData _crop;
    private CropData? _previousCrop;

    public string Description => $"Plant {_crop.Name} at {_position}";

    public PlaceCropCommand(FarmGrid grid, Vector2Int pos, CropData crop)
    {
        _grid = grid;
        _position = pos;
        _crop = crop;
    }

    public void Execute()
    {
        _previousCrop = _grid.GetCropAt(_position);
        _grid.PlaceCrop(_position, _crop);
    }

    public void Undo()
    {
        if (_previousCrop is not null)
            _grid.PlaceCrop(_position, _previousCrop);
        else
            _grid.ClearTile(_position);
    }
}

public class CommandHistory
{
    private readonly Stack<ICommand> _undoStack = new();
    private readonly Stack<ICommand> _redoStack = new();

    public void Execute(ICommand cmd)
    {
        cmd.Execute();
        _undoStack.Push(cmd);
        _redoStack.Clear();  // New action invalidates redo history
    }

    public void Undo()
    {
        if (_undoStack.TryPop(out var cmd))
        {
            cmd.Undo();
            _redoStack.Push(cmd);
        }
    }

    public void Redo()
    {
        if (_redoStack.TryPop(out var cmd))
        {
            cmd.Execute();
            _undoStack.Push(cmd);
        }
    }
}
```

### 10.3 — State Machine Pattern

```csharp
public interface IState
{
    void Enter();
    void Update(float deltaTime);
    void Exit();
}

public class StateMachine
{
    private IState? _current;
    private readonly Dictionary<Type, IState> _states = new();

    public void Register<T>(T state) where T : IState
        => _states[typeof(T)] = state;

    public void TransitionTo<T>() where T : IState
    {
        _current?.Exit();
        _current = _states[typeof(T)];
        _current.Enter();
    }

    public void Update(float dt) => _current?.Update(dt);
}

// Player states
public class IdleState : IState
{
    private readonly PlayerController _player;
    private readonly StateMachine _sm;

    public IdleState(PlayerController player, StateMachine sm)
    {
        _player = player;
        _sm = sm;
    }

    public void Enter() => _player.Animator.Play("Idle");

    public void Update(float dt)
    {
        if (_player.MoveInput.sqrMagnitude > 0.01f)
            _sm.TransitionTo<WalkingState>();
        if (_player.AttackPressed)
            _sm.TransitionTo<AttackingState>();
    }

    public void Exit() { }
}
```

### 10.4 — Factory Pattern (ScriptableObject-Driven)

```csharp
// Abstract product
public interface IProjectile
{
    void Launch(Vector3 origin, Vector3 direction, float speed);
}

// Factory using ScriptableObject definitions
[CreateAssetMenu(menuName = "Game/Projectile Definition")]
public class ProjectileDefinition : ScriptableObject
{
    public GameObject prefab;
    public float speed = 10f;
    public float damage = 25f;
    public float lifetime = 5f;
    public AudioClip launchSound;
}

public class ProjectileFactory : MonoBehaviour
{
    [SerializeField] private ProjectileDefinition[] definitions;
    private Dictionary<string, ProjectileDefinition> _lookup;

    void Awake()
    {
        _lookup = definitions.ToDictionary(d => d.name);
    }

    public GameObject Create(string type, Vector3 position, Quaternion rotation)
    {
        if (!_lookup.TryGetValue(type, out var def))
            throw new ArgumentException($"Unknown projectile: {type}");

        var go = Instantiate(def.prefab, position, rotation);
        var proj = go.GetComponent<Projectile>();
        proj.Initialize(def.speed, def.damage, def.lifetime);
        return go;
    }
}
```

### 10.5 — Strategy Pattern (Interchangeable Algorithms)

```csharp
// Strategy interface
public interface IPathfinding
{
    List<Vector2Int> FindPath(Vector2Int start, Vector2Int end, IGrid grid);
}

// Concrete strategies
public class AStarPathfinding : IPathfinding
{
    public List<Vector2Int> FindPath(Vector2Int start, Vector2Int end, IGrid grid)
    {
        // A* implementation...
        return path;
    }
}

public class DijkstraPathfinding : IPathfinding
{
    public List<Vector2Int> FindPath(Vector2Int start, Vector2Int end, IGrid grid)
    {
        // Dijkstra implementation (when you need shortest path to ALL nodes)
        return path;
    }
}

// Context: NPC uses whichever strategy is injected
public class NPCMovement : MonoBehaviour
{
    private IPathfinding _pathfinder;

    public void SetPathfinder(IPathfinding pathfinder) => _pathfinder = pathfinder;

    public void MoveTo(Vector2Int target)
    {
        var path = _pathfinder.FindPath(CurrentTile, target, GameGrid.Instance);
        StartCoroutine(FollowPath(path));
    }
}
```


---

## 🔑 4. Mechanics — Delegates & Events

### 4.1 — Delegates (Function Pointers)

```csharp
// Python comparison: Callable[[int, int], float]
// C# has built-in delegate types:
Action                    // void ()
Action<T>                 // void (T)
Action<T1, T2>           // void (T1, T2)
Func<TResult>            // TResult ()
Func<T, TResult>         // TResult (T)
Predicate<T>             // bool (T) — alias for Func<T, bool>

// Usage: passing behavior as parameter
public void ProcessItems(List<Item> items, Func<Item, bool> filter, Action<Item> process)
{
    foreach (var item in items)
    {
        if (filter(item))
            process(item);
    }
}

// Call with lambdas
ProcessItems(inventory,
    filter: i => i.Value > 100,
    process: i => Console.WriteLine($"Valuable: {i.Name}")
);
```

### 4.2 — Events (Safe Delegates)

```csharp
public class HealthSystem : MonoBehaviour
{
    // event keyword prevents external code from invoking or replacing
    public event Action<float, float>? OnHealthChanged;  // (current, max)
    public event Action? OnDeath;

    private float _health;
    public float Health
    {
        get => _health;
        private set
        {
            _health = Mathf.Clamp(value, 0, MaxHealth);
            OnHealthChanged?.Invoke(_health, MaxHealth);
            if (_health <= 0) OnDeath?.Invoke();
        }
    }

    public float MaxHealth { get; private set; }

    // External code can subscribe but NOT invoke:
    // healthSystem.OnDeath += HandleDeath;  ✓
    // healthSystem.OnDeath?.Invoke();       ✗ Compile error
    // healthSystem.OnDeath = null;          ✗ Compile error
}
```

---

## ✍️ 5. Worked Examples

### Example 10.3.1 — Complete Interaction System

```csharp
// Interface segregation: not everything is interactable the same way
public interface IInteractable
{
    string GetPrompt(PlayerController player);
    bool CanInteract(PlayerController player);
    void Interact(PlayerController player);
}

public interface IHoverable
{
    void OnHoverEnter();
    void OnHoverExit();
}

// Chest: interactable + hoverable
public class TreasureChest : MonoBehaviour, IInteractable, IHoverable
{
    [SerializeField] private LootTable lootTable;
    [SerializeField] private SpriteRenderer spriteRenderer;
    private bool _isOpened;

    public string GetPrompt(PlayerController player)
        => _isOpened ? "" : "Open Chest";

    public bool CanInteract(PlayerController player)
        => !_isOpened;

    public void Interact(PlayerController player)
    {
        _isOpened = true;
        var loot = lootTable.Roll();
        player.Inventory.TryAdd(loot);
        spriteRenderer.sprite = openedSprite;
        GameEvents.Instance.ChestOpened(transform.position, loot);
    }

    public void OnHoverEnter() => spriteRenderer.color = Color.yellow;
    public void OnHoverExit() => spriteRenderer.color = Color.white;
}

// Interaction detector (uses interfaces, doesn't know concrete types)
public class InteractionDetector : MonoBehaviour
{
    [SerializeField] private float range = 2f;
    [SerializeField] private LayerMask interactableLayer;

    private IInteractable? _current;
    private IHoverable? _currentHover;

    void Update()
    {
        var hit = Physics2D.OverlapCircle(transform.position, range, interactableLayer);

        var newInteractable = hit?.GetComponent<IInteractable>();
        if (newInteractable != _current)
        {
            (_currentHover as IHoverable)?.OnHoverExit();
            _current = newInteractable;
            _currentHover = hit?.GetComponent<IHoverable>();
            _currentHover?.OnHoverEnter();
        }

        if (Input.GetKeyDown(KeyCode.E) && _current?.CanInteract(GetComponent<PlayerController>()) == true)
        {
            _current.Interact(GetComponent<PlayerController>());
        }
    }
}
```

---

## ⚠️ 6. Gotchas

### Gotcha 3.3.1 — Event Memory Leaks
```csharp
// ❌ Subscribing without unsubscribing = memory leak
void OnEnable() => GameEvents.Instance.OnGoldChanged += UpdateUI;
// If you forget OnDisable, the destroyed object stays in memory!

// ✓ Always pair subscribe/unsubscribe
void OnEnable() => GameEvents.Instance.OnGoldChanged += UpdateUI;
void OnDisable() => GameEvents.Instance.OnGoldChanged -= UpdateUI;
```

### Gotcha 3.3.2 — Virtual Method Calls in Constructor
```csharp
// ❌ DANGEROUS: virtual call in constructor
public class Base
{
    public Base() { Initialize(); }  // Calls DERIVED override before derived ctor runs!
    protected virtual void Initialize() { }
}

// ✓ Use two-phase initialization or factory methods
public static T Create<T>() where T : Base, new()
{
    var obj = new T();
    obj.Initialize();
    return obj;
}
```

### Gotcha 3.3.3 — God Objects
```csharp
// ❌ One class doing everything
public class GameManager : MonoBehaviour
{
    // Manages: spawning, scoring, UI, audio, saving, input, camera...
    // 2000 lines, untestable, everyone depends on it
}

// ✓ Split by responsibility, communicate via events/interfaces
public class SpawnSystem : MonoBehaviour { }
public class ScoreSystem : MonoBehaviour { }
public class SaveSystem : MonoBehaviour { }
// Each is independently testable and replaceable
```

### Gotcha 3.3.4 — Overusing Singletons
```csharp
// ❌ Singletons everywhere = hidden dependencies, untestable
AudioManager.Instance.Play("click");
SaveManager.Instance.Save();
UIManager.Instance.ShowPopup("...");

// ✓ Inject dependencies (see Chapter 10.8)
public class ShopUI : MonoBehaviour
{
    private IAudioService _audio;
    private ISaveService _save;

    public void Initialize(IAudioService audio, ISaveService save)
    {
        _audio = audio;
        _save = save;
    }
}
```

---

## 🔗 7. Cross-References

- **Next**: [10.4 - Async, Await, Tasks & Threading](10.4---Async,-Await,-Tasks-&-Threading) — Async patterns
- **Previous**: [10.2 - Core Language - Types, Generics & LINQ](10.2---Core-Language---Types,-Generics-&-LINQ)
- **Python OOP**: [08.3 - OOP, Data Models & Pythonic Idioms](08.3---OOP,-Data-Models-&-Pythonic-Idioms) — Protocol vs Interface
- **Unity Specifics**: [10.6 - Unity Specifics - MonoBehaviour, Coroutines, ScriptableObjects, ECS](10.6---Unity-Specifics---MonoBehaviour,-Coroutines,-ScriptableObjects,-ECS) — MonoBehaviour lifecycle
- **Production DI**: [10.8 - Production Patterns - DI, Save Systems, Addressables](10.8---Production-Patterns---DI,-Save-Systems,-Addressables) — Dependency injection

---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — SOLID Principles with Unity Examples

**Problem:** You're building a Unity game and your MonoBehaviours are becoming god classes with 500+ lines. Apply SOLID principles to create maintainable, testable game architecture.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### S — Single Responsibility Principle

```csharp
// ❌ BAD: PlayerController does EVERYTHING
public class PlayerController : MonoBehaviour
{
    public float health;
    public void TakeDamage(float amount) { /* ... */ }
    public void Move(Vector2 input) { /* ... */ }
    public void Attack() { /* ... */ }
    public void SaveToFile() { /* ... */ }
    public void PlayFootstepSound() { /* ... */ }
    public void UpdateUI() { /* ... */ }
    // 500 more lines...
}

// ✅ GOOD: Each class has ONE reason to change
public class PlayerHealth : MonoBehaviour
{
    [SerializeField] private float _maxHealth = 100f;
    private float _currentHealth;
    
    public event Action<float, float> OnHealthChanged; // current, max
    public event Action OnDied;
    
    public void TakeDamage(float amount)
    {
        _currentHealth = Mathf.Max(0, _currentHealth - amount);
        OnHealthChanged?.Invoke(_currentHealth, _maxHealth);
        if (_currentHealth <= 0) OnDied?.Invoke();
    }
}

public class PlayerMovement : MonoBehaviour
{
    [SerializeField] private float _speed = 5f;
    private Rigidbody2D _rb;
    
    public void Move(Vector2 input)
    {
        _rb.velocity = input * _speed;
    }
}

public class PlayerCombat : MonoBehaviour
{
    [SerializeField] private float _attackDamage = 10f;
    [SerializeField] private float _attackRange = 1.5f;
    
    public void Attack(IDamageable target)
    {
        target.TakeDamage(_attackDamage);
    }
}
```

#### O — Open/Closed Principle

```csharp
// ❌ BAD: Adding new item types requires modifying existing code
public class ItemUser
{
    public void UseItem(Item item)
    {
        switch (item.Type)
        {
            case "potion": /* heal */ break;
            case "bomb": /* explode */ break;
            case "scroll": /* cast spell */ break;
            // Every new item type = modify this switch
        }
    }
}

// ✅ GOOD: Open for extension, closed for modification
public interface IUsable
{
    void Use(PlayerContext context);
}

public class HealthPotion : IUsable
{
    public int HealAmount { get; init; } = 50;
    public void Use(PlayerContext context)
    {
        context.Health.Heal(HealAmount);
        context.Inventory.RemoveItem(this);
    }
}

public class TeleportScroll : IUsable
{
    public Vector3 Destination { get; init; }
    public void Use(PlayerContext context)
    {
        context.Movement.TeleportTo(Destination);
        context.Inventory.RemoveItem(this);
    }
}

// Adding new items = new class, ZERO changes to existing code
public class InvisibilityCloak : IUsable
{
    public float Duration { get; init; } = 10f;
    public void Use(PlayerContext context)
    {
        context.StatusEffects.Apply(new InvisibleEffect(Duration));
    }
}
```

#### L — Liskov Substitution Principle

```csharp
// ❌ BAD: Square violates LSP when substituted for Rectangle
public class Rectangle
{
    public virtual float Width { get; set; }
    public virtual float Height { get; set; }
    public float Area => Width * Height;
}

public class Square : Rectangle
{
    public override float Width
    {
        set { base.Width = value; base.Height = value; } // Surprise!
    }
}

// ✅ GOOD: Use interfaces that make sense for all implementations
public interface IShape
{
    float Area { get; }
    float Perimeter { get; }
    bool ContainsPoint(Vector2 point);
}

public readonly struct Circle : IShape
{
    public float Radius { get; init; }
    public float Area => Mathf.PI * Radius * Radius;
    public float Perimeter => 2 * Mathf.PI * Radius;
    public bool ContainsPoint(Vector2 point) => point.magnitude <= Radius;
}

public readonly struct Rect : IShape
{
    public float Width { get; init; }
    public float Height { get; init; }
    public float Area => Width * Height;
    public float Perimeter => 2 * (Width + Height);
    public bool ContainsPoint(Vector2 p) => 
        p.x >= 0 && p.x <= Width && p.y >= 0 && p.y <= Height;
}
```

#### I — Interface Segregation Principle

```csharp
// ❌ BAD: Fat interface forces empty implementations
public interface IEntity
{
    void Move(Vector3 direction);
    void TakeDamage(float amount);
    void Attack(IEntity target);
    void OpenInventory();
    void Speak(string dialogue);
}

// A tree is an IEntity but can't move, attack, or speak!
public class Tree : IEntity
{
    public void Move(Vector3 d) { } // Empty — violates ISP
    public void TakeDamage(float amount) { /* chop */ }
    public void Attack(IEntity target) { } // Trees don't attack
    public void OpenInventory() { } // Trees have no inventory
    public void Speak(string d) { } // Trees don't talk
}

// ✅ GOOD: Small, focused interfaces
public interface IDamageable { void TakeDamage(float amount); }
public interface IMovable { void Move(Vector3 direction); }
public interface IAttacker { void Attack(IDamageable target); }
public interface IInteractable { void Interact(PlayerContext player); }

public class Tree : IDamageable, IInteractable
{
    public void TakeDamage(float amount) { /* chop */ }
    public void Interact(PlayerContext player) { /* gather wood */ }
}

public class Enemy : IDamageable, IMovable, IAttacker
{
    public void TakeDamage(float amount) { /* hurt */ }
    public void Move(Vector3 direction) { /* patrol */ }
    public void Attack(IDamageable target) { /* swing */ }
}
```

#### D — Dependency Inversion Principle

```csharp
// ❌ BAD: High-level module depends on low-level implementation
public class GameSaver
{
    private readonly JsonFileWriter _writer = new(); // Concrete dependency!
    
    public void Save(GameState state)
    {
        _writer.WriteJson("save.json", state); // Can't test without filesystem
    }
}

// ✅ GOOD: Depend on abstractions, inject implementations
public interface ISaveStorage
{
    Task SaveAsync(string key, byte[] data);
    Task<byte[]> LoadAsync(string key);
}

public class GameSaver
{
    private readonly ISaveStorage _storage; // Abstraction!
    
    public GameSaver(ISaveStorage storage) => _storage = storage;
    
    public async Task SaveAsync(GameState state)
    {
        var data = MessagePackSerializer.Serialize(state);
        await _storage.SaveAsync("autosave", data);
    }
}

// Swap implementations without changing GameSaver:
public class LocalFileSaveStorage : ISaveStorage { /* ... */ }
public class CloudSaveStorage : ISaveStorage { /* ... */ }
public class InMemorySaveStorage : ISaveStorage { /* For unit tests */ }
```

</details>

### Example 8.2 — Mediator Pattern for Game Events

**Problem:** Your game systems need to communicate (combat → UI, combat → audio, combat → particles) but direct references create spaghetti dependencies. Use the Mediator pattern to decouple everything.

<details>
<summary>🔍 Full step-by-step solution</summary>

```csharp
// ═══════════════════════════════════════════════════════════════
// EVENT DEFINITIONS — Simple data carriers
// ═══════════════════════════════════════════════════════════════
public interface IGameEvent { }

public readonly struct DamageDealtEvent : IGameEvent
{
    public readonly GameObject Source;
    public readonly GameObject Target;
    public readonly float Amount;
    public readonly DamageType Type;
    public readonly Vector3 HitPoint;
    
    public DamageDealtEvent(GameObject source, GameObject target, 
        float amount, DamageType type, Vector3 hitPoint)
    {
        Source = source; Target = target; Amount = amount;
        Type = type; HitPoint = hitPoint;
    }
}

public readonly struct EnemyDiedEvent : IGameEvent
{
    public readonly GameObject Enemy;
    public readonly int XpReward;
    public readonly Vector3 Position;
    
    public EnemyDiedEvent(GameObject enemy, int xp, Vector3 pos)
    {
        Enemy = enemy; XpReward = xp; Position = pos;
    }
}

public readonly struct ItemPickedUpEvent : IGameEvent
{
    public readonly string ItemId;
    public readonly int Quantity;
    
    public ItemPickedUpEvent(string itemId, int quantity)
    {
        ItemId = itemId; Quantity = quantity;
    }
}

// ═══════════════════════════════════════════════════════════════
// MEDIATOR — Central event bus (ScriptableObject-based for Unity)
// ═══════════════════════════════════════════════════════════════
[CreateAssetMenu(menuName = "Events/Game Event Bus")]
public class GameEventBus : ScriptableObject
{
    private readonly Dictionary<Type, List<Delegate>> _handlers = new();

    public void Subscribe<T>(Action<T> handler) where T : struct, IGameEvent
    {
        var type = typeof(T);
        if (!_handlers.ContainsKey(type))
            _handlers[type] = new List<Delegate>();
        _handlers[type].Add(handler);
    }

    public void Unsubscribe<T>(Action<T> handler) where T : struct, IGameEvent
    {
        var type = typeof(T);
        if (_handlers.TryGetValue(type, out var list))
            list.Remove(handler);
    }

    public void Publish<T>(T evt) where T : struct, IGameEvent
    {
        if (_handlers.TryGetValue(typeof(T), out var list))
        {
            // Iterate backwards to allow unsubscription during handling
            for (int i = list.Count - 1; i >= 0; i--)
            {
                ((Action<T>)list[i]).Invoke(evt);
            }
        }
    }

    // Clear all subscriptions (important for scene transitions)
    public void Clear() => _handlers.Clear();
}

// ═══════════════════════════════════════════════════════════════
// PUBLISHERS — Fire events, don't know who listens
// ═══════════════════════════════════════════════════════════════
public class CombatSystem : MonoBehaviour
{
    [SerializeField] private GameEventBus _eventBus;

    public void DealDamage(GameObject source, GameObject target, 
        float amount, DamageType type, Vector3 hitPoint)
    {
        // Apply damage...
        var health = target.GetComponent<Health>();
        health.Reduce(amount);

        // Publish event — don't care who handles it
        _eventBus.Publish(new DamageDealtEvent(source, target, amount, type, hitPoint));

        if (health.IsDead)
        {
            var enemy = target.GetComponent<EnemyData>();
            _eventBus.Publish(new EnemyDiedEvent(target, enemy.XpReward, target.transform.position));
        }
    }
}

// ═══════════════════════════════════════════════════════════════
// SUBSCRIBERS — React to events, don't know who publishes
// ═══════════════════════════════════════════════════════════════
public class DamageNumberUI : MonoBehaviour
{
    [SerializeField] private GameEventBus _eventBus;
    [SerializeField] private GameObject _damageNumberPrefab;

    private void OnEnable() => _eventBus.Subscribe<DamageDealtEvent>(OnDamageDealt);
    private void OnDisable() => _eventBus.Unsubscribe<DamageDealtEvent>(OnDamageDealt);

    private void OnDamageDealt(DamageDealtEvent evt)
    {
        var popup = Instantiate(_damageNumberPrefab, evt.HitPoint, Quaternion.identity);
        popup.GetComponent<DamageNumber>().Setup(evt.Amount, evt.Type);
    }
}

public class AudioManager : MonoBehaviour
{
    [SerializeField] private GameEventBus _eventBus;

    private void OnEnable()
    {
        _eventBus.Subscribe<DamageDealtEvent>(OnDamage);
        _eventBus.Subscribe<EnemyDiedEvent>(OnEnemyDied);
    }

    private void OnDisable()
    {
        _eventBus.Unsubscribe<DamageDealtEvent>(OnDamage);
        _eventBus.Unsubscribe<EnemyDiedEvent>(OnEnemyDied);
    }

    private void OnDamage(DamageDealtEvent evt)
    {
        var clip = evt.Type switch
        {
            DamageType.Physical => _hitSounds.Random(),
            DamageType.Fire => _fireSounds.Random(),
            DamageType.Ice => _iceSounds.Random(),
            _ => _defaultHit
        };
        AudioSource.PlayClipAtPoint(clip, evt.HitPoint);
    }

    private void OnEnemyDied(EnemyDiedEvent evt)
    {
        AudioSource.PlayClipAtPoint(_deathSound, evt.Position);
    }
}

public class XpSystem : MonoBehaviour
{
    [SerializeField] private GameEventBus _eventBus;
    private int _totalXp;

    private void OnEnable() => _eventBus.Subscribe<EnemyDiedEvent>(OnEnemyDied);
    private void OnDisable() => _eventBus.Unsubscribe<EnemyDiedEvent>(OnEnemyDied);

    private void OnEnemyDied(EnemyDiedEvent evt)
    {
        _totalXp += evt.XpReward;
        CheckLevelUp();
    }
}
```

**Benefits:**
- CombatSystem doesn't reference UI, Audio, or XP systems
- Adding new reactions = new subscriber, zero changes to existing code
- Easy to test: publish events, verify handlers called
- ScriptableObject event bus survives scene loads

</details>

### Example 8.3 — Observer Pattern: C# Events vs UniRx

**Problem:** You need reactive data binding for your game UI. Compare native C# events, Unity Events, and UniRx (Reactive Extensions for Unity).

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Approach 1: Native C# Events

```csharp
public class PlayerStats
{
    private int _gold;
    public int Gold
    {
        get => _gold;
        set
        {
            if (_gold == value) return;
            var old = _gold;
            _gold = value;
            OnGoldChanged?.Invoke(old, value);
        }
    }
    
    public event Action<int, int> OnGoldChanged; // old, new
}

// Subscriber
public class GoldUI : MonoBehaviour
{
    [SerializeField] private TMP_Text _goldText;
    private PlayerStats _stats;

    private void OnEnable() => _stats.OnGoldChanged += UpdateDisplay;
    private void OnDisable() => _stats.OnGoldChanged -= UpdateDisplay;

    private void UpdateDisplay(int oldVal, int newVal)
    {
        _goldText.text = $"{newVal:N0}";
        // Animate if increased
        if (newVal > oldVal) PlayGoldGainAnimation(newVal - oldVal);
    }
}
```

**Pros:** Zero allocation, fastest, built into language.
**Cons:** Manual subscribe/unsubscribe (memory leak risk), no composition.

#### Approach 2: UniRx (Reactive Extensions)

```csharp
using UniRx;

public class PlayerStats : MonoBehaviour
{
    // ReactiveProperty: observable + current value
    public ReactiveProperty<int> Gold { get; } = new(0);
    public ReactiveProperty<float> Health { get; } = new(100f);
    public ReactiveProperty<int> Level { get; } = new(1);
}

// Subscriber — Declarative, composable, auto-disposes
public class PlayerUI : MonoBehaviour
{
    [SerializeField] private TMP_Text _goldText;
    [SerializeField] private TMP_Text _healthText;
    [SerializeField] private Slider _healthBar;
    [SerializeField] private PlayerStats _stats;

    private void Start()
    {
        // Auto-updates UI when value changes, auto-disposes on destroy
        _stats.Gold
            .Subscribe(gold => _goldText.text = $"{gold:N0}")
            .AddTo(this); // Dispose when this MonoBehaviour is destroyed

        // Combine multiple streams
        _stats.Health
            .CombineLatest(_stats.Level, (hp, lvl) => (hp, maxHp: lvl * 100f))
            .Subscribe(pair =>
            {
                _healthBar.value = pair.hp / pair.maxHp;
                _healthText.text = $"{pair.hp:F0}/{pair.maxHp:F0}";
            })
            .AddTo(this);

        // Throttle rapid changes (e.g., damage numbers)
        _stats.Health
            .Pairwise() // Gives (previous, current)
            .Where(pair => pair.Current < pair.Previous) // Only damage
            .ThrottleFirst(TimeSpan.FromSeconds(0.1f)) // Max 10/sec
            .Subscribe(pair => SpawnDamageNumber(pair.Previous - pair.Current))
            .AddTo(this);

        // React to specific thresholds
        _stats.Health
            .Where(hp => hp <= 20f)
            .First() // Only trigger once
            .Subscribe(_ => ShowLowHealthWarning())
            .AddTo(this);
    }
}
```

**Pros:** Composable operators (throttle, combine, filter), auto-disposal, declarative.
**Cons:** Learning curve, allocation overhead, dependency on UniRx package.

#### Approach 3: R3 (Modern Replacement for UniRx)

```csharp
using R3;

public class PlayerStats : MonoBehaviour
{
    // R3 uses ReactiveProperty<T> with better performance than UniRx
    public ReactiveProperty<int> Gold { get; } = new(0);
    
    // ReadOnlyReactiveProperty for derived values
    public ReadOnlyReactiveProperty<string> GoldDisplay { get; }
    
    public PlayerStats()
    {
        GoldDisplay = Gold
            .Select(g => $"{g:N0} G")
            .ToReadOnlyReactiveProperty();
    }
}

// R3 advantages over UniRx:
// - Zero-allocation in many cases (struct-based observers)
// - Better Unity integration (PlayerLoopTiming)
// - Supports async/await natively
// - Active development (UniRx is maintenance-only)
```

#### Decision Matrix

| Feature | C# Events | UniRx | R3 |
|---------|:---------:|:-----:|:--:|
| Allocations | Zero | Medium | Low |
| Composition | ❌ | ★★★★★ | ★★★★★ |
| Auto-dispose | ❌ | ✅ | ✅ |
| Learning curve | Low | High | Medium |
| Unity support | Native | Package | Package |
| Async support | ❌ | Limited | ✅ |
| Active development | N/A | ❌ | ✅ |

**Recommendation:** Use C# events for simple cases (< 3 subscribers, no composition needed). Use R3 for complex UI binding, stream processing, and reactive game systems.

</details>

---

## 📖 9. Appendix: Extended Derivations & Special Cases

### Appendix 9.1 — Covariance and Contravariance in Delegates

#### The Problem

```csharp
// Why can't I assign Action<Base> to Action<Derived>?
// Why CAN I assign Func<Derived> to Func<Base>?

class Animal { }
class Dog : Animal { }

// COVARIANT (out) — Return types
Func<Dog> getDog = () => new Dog();
Func<Animal> getAnimal = getDog;  // ✅ Legal! Dog IS-A Animal
// If you expect "something that gives me an Animal", 
// "something that gives me a Dog" is fine (Dog is more specific)

// CONTRAVARIANT (in) — Parameter types
Action<Animal> feedAnimal = (animal) => Console.WriteLine("Fed!");
Action<Dog> feedDog = feedAnimal;  // ✅ Legal! Reversed direction
// If you expect "something that can handle a Dog",
// "something that can handle ANY Animal" is fine (more general)
```

#### Why This Matters for Event Systems

```csharp
// Game event hierarchy
public interface IGameEvent { }
public interface ICombatEvent : IGameEvent { }
public struct DamageEvent : ICombatEvent { public float Amount; }
public struct HealEvent : ICombatEvent { public float Amount; }

// Contravariant event handler interface
public interface IEventHandler<in TEvent> where TEvent : IGameEvent
{
    void Handle(TEvent evt);
}

// A general handler can be used where a specific handler is expected
public class LoggingHandler : IEventHandler<IGameEvent>
{
    public void Handle(IGameEvent evt) => Debug.Log($"Event: {evt}");
}

// This works because of contravariance:
IEventHandler<IGameEvent> logger = new LoggingHandler();
IEventHandler<DamageEvent> damageLogger = logger; // ✅ Contravariance!
// "Something that handles any IGameEvent" can certainly handle DamageEvent
```

#### Variance in Generic Interfaces (Complete Rules)

```csharp
// COVARIANT (out T) — T appears only in OUTPUT positions
interface IProducer<out T>
{
    T Get();                    // ✅ Return type
    IEnumerable<T> GetAll();   // ✅ Return type (nested covariance)
    // void Set(T item);       // ❌ COMPILE ERROR: can't use T as input
}

// CONTRAVARIANT (in T) — T appears only in INPUT positions
interface IConsumer<in T>
{
    void Process(T item);      // ✅ Parameter type
    void ProcessAll(IEnumerable<T> items); // ✅ Parameter type
    // T Get();                // ❌ COMPILE ERROR: can't use T as output
}

// INVARIANT (no modifier) — T in both positions
interface IRepository<T>       // Neither in nor out
{
    T Get(int id);             // T as output
    void Save(T item);        // T as input
    // Cannot be variant — used in both directions
}
```

### Appendix 9.2 — Sealed Classes and JIT Optimizations

#### Why `sealed` Matters for Performance

```csharp
// UNSEALED class — JIT must use virtual dispatch
public class Enemy
{
    public virtual void Update() { /* base logic */ }
}

// When JIT compiles a call to enemy.Update():
// 1. Load vtable pointer from object header
// 2. Index into vtable to find method address
// 3. Indirect call through pointer
// Cost: ~2-5ns overhead per call (cache miss can be 50ns+)

// SEALED class — JIT can DEVIRTUALIZE
public sealed class Goblin : Enemy
{
    public override void Update() { /* goblin logic */ }
}

// When JIT sees: goblin.Update() where goblin is typed as Goblin (sealed):
// 1. Knows no further overrides exist
// 2. Replaces virtual call with DIRECT call
// 3. Can even INLINE the method body
// Cost: 0ns overhead (same as non-virtual call)
```

#### Benchmarks

```csharp
// BenchmarkDotNet results (1 million calls):
// | Method          | Mean     | Allocated |
// |-----------------|----------|-----------|
// | VirtualCall     | 4.2 ns   | 0 B       |
// | SealedCall      | 1.1 ns   | 0 B       |  ← 4x faster
// | DirectCall      | 1.0 ns   | 0 B       |
// | InterfaceCall   | 5.8 ns   | 0 B       |

// In a game loop processing 10,000 entities at 60fps:
// Virtual: 10000 * 4.2ns = 42μs per frame
// Sealed:  10000 * 1.1ns = 11μs per frame
// Savings: 31μs per frame (meaningful in a 16.6ms budget!)
```

#### When to Seal

```csharp
// SEAL by default, unseal when you need inheritance
// (Opposite of Java's default, same as Kotlin's default)

public sealed class PlayerMovement : MonoBehaviour { }  // No one inherits this
public sealed class InventorySlot { }                   // Data class, final
public sealed class DamageCalculator { }                // Utility, no extension

// DON'T seal when you design for inheritance:
public abstract class BaseWeapon { }  // Intended to be extended
public class MeleeWeapon : BaseWeapon { }  // Could seal this leaf class
```

#### Sealed + Interface = Best of Both Worlds

```csharp
// Interface for polymorphism (testability, DI)
public interface IInventoryService
{
    void AddItem(string itemId, int quantity);
    bool RemoveItem(string itemId, int quantity);
}

// Sealed implementation for performance
public sealed class InventoryService : IInventoryService
{
    // JIT devirtualizes calls when concrete type is known
    public void AddItem(string itemId, int quantity) { /* ... */ }
    public bool RemoveItem(string itemId, int quantity) { /* ... */ }
}

// In hot paths, use concrete type:
private readonly InventoryService _inventory; // Sealed → devirtualized

// In DI/testing, use interface:
public GameManager(IInventoryService inventory) { /* ... */ }
```

### Appendix 9.3 — The State Pattern vs Enum State Machines

```csharp
// ═══════════════════════════════════════════════════════════════
// APPROACH 1: Enum + Switch (Simple, good for < 5 states)
// ═══════════════════════════════════════════════════════════════
public enum PlayerState { Idle, Running, Jumping, Attacking, Dead }

public class SimpleStateMachine : MonoBehaviour
{
    private PlayerState _state = PlayerState.Idle;

    private void Update()
    {
        switch (_state)
        {
            case PlayerState.Idle:
                if (Input.GetAxis("Horizontal") != 0) _state = PlayerState.Running;
                if (Input.GetButtonDown("Jump")) _state = PlayerState.Jumping;
                break;
            case PlayerState.Running:
                Move();
                if (Input.GetAxis("Horizontal") == 0) _state = PlayerState.Idle;
                break;
            // Gets unwieldy with 10+ states...
        }
    }
}

// ═══════════════════════════════════════════════════════════════
// APPROACH 2: State Pattern (Scalable, good for 5+ states)
// ═══════════════════════════════════════════════════════════════
public interface IPlayerState
{
    void Enter(PlayerController player);
    void Update(PlayerController player);
    void Exit(PlayerController player);
}

public sealed class IdleState : IPlayerState
{
    public void Enter(PlayerController player)
    {
        player.Animator.Play("Idle");
    }

    public void Update(PlayerController player)
    {
        if (player.Input.Movement.magnitude > 0.1f)
            player.ChangeState(new RunningState());
        if (player.Input.JumpPressed)
            player.ChangeState(new JumpingState());
    }

    public void Exit(PlayerController player) { }
}

public sealed class JumpingState : IPlayerState
{
    private float _jumpTimer;

    public void Enter(PlayerController player)
    {
        player.Animator.Play("Jump");
        player.Rigidbody.AddForce(Vector2.up * player.JumpForce, ForceMode2D.Impulse);
        _jumpTimer = 0f;
    }

    public void Update(PlayerController player)
    {
        _jumpTimer += Time.deltaTime;
        if (player.IsGrounded && _jumpTimer > 0.1f)
            player.ChangeState(new IdleState());
    }

    public void Exit(PlayerController player) { }
}

public class PlayerController : MonoBehaviour
{
    private IPlayerState _currentState;

    public void ChangeState(IPlayerState newState)
    {
        _currentState?.Exit(this);
        _currentState = newState;
        _currentState.Enter(this);
    }

    private void Update() => _currentState?.Update(this);
}
```

---

## 🔄 Maintenance
- **Created**: 2026-05-24
- **Last Updated**: 2026-05-24
