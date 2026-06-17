---
title: "10.8 — Production Patterns: DI, Save Systems, Addressables"
subject: "C#"
catalog: advanced
audience_tier: higher-education
chapter: "10.8"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 10.8 — Production Patterns: DI, Save Systems, Addressables

> *"A game that can't save isn't a game. A game that corrupts saves is worse than no game at all."* — Brackeys

This chapter covers the unglamorous but essential systems that separate a prototype from a shippable product. Dependency injection makes your code testable and modular. Save systems preserve player progress without corruption. Addressables manage memory and enable downloadable content. Together, they form the production backbone of any serious Unity project.

---

## 🎯 Learning Objectives

1. Implement dependency injection using VContainer (or Zenject).
2. Design a versioned, corruption-resistant save system.
3. Use Unity Addressables for async asset loading and memory management.
4. Write unit tests and integration tests for game systems.
5. Set up CI/CD for automated Unity builds.
6. Apply the Service Locator pattern as a lightweight DI alternative.

---

## 🖼️ Visual Anchor — Production Architecture

![csharp__3.8-fig1](csharp__3.8-fig1.svg)

---

## 📚 1. Concepts

### Concept 3.8.1 — Dependency Injection (DI)

DI means: **don't create your dependencies, receive them from outside.**

```csharp
// ❌ Without DI: tight coupling, untestable
public class ShopSystem : MonoBehaviour
{
    void BuyItem(string itemId)
    {
        var price = ItemDatabase.Instance.GetPrice(itemId);     // Singleton!
        if (PlayerWallet.Instance.Gold >= price)                // Singleton!
        {
            PlayerWallet.Instance.Spend(price);                 // Singleton!
            PlayerInventory.Instance.Add(itemId);               // Singleton!
            AudioManager.Instance.Play("purchase");             // Singleton!
        }
    }
    // How do you unit test this? You can't mock any dependency.
}

// ✓ With DI: decoupled, testable, swappable
public class ShopSystem
{
    private readonly IItemDatabase _items;
    private readonly IWallet _wallet;
    private readonly IInventory _inventory;
    private readonly IAudioService _audio;

    public ShopSystem(IItemDatabase items, IWallet wallet,
                      IInventory inventory, IAudioService audio)
    {
        _items = items;
        _wallet = wallet;
        _inventory = inventory;
        _audio = audio;
    }

    public bool TryBuyItem(string itemId)
    {
        var price = _items.GetPrice(itemId);
        if (_wallet.Gold < price) return false;

        _wallet.Spend(price);
        _inventory.Add(itemId);
        _audio.Play("purchase");
        return true;
    }
}

// Test: inject mocks
[Test]
public void BuyItem_DeductsGold()
{
    var wallet = new MockWallet(startGold: 100);
    var shop = new ShopSystem(mockItems, wallet, mockInventory, mockAudio);

    shop.TryBuyItem("parsnip_seed");

    Assert.AreEqual(80, wallet.Gold);  // Price was 20
}
```

### Concept 3.8.2 — VContainer (Recommended DI for Unity)

```csharp
using VContainer;
using VContainer.Unity;

// Lifetime scope: defines what gets injected where
public class GameLifetimeScope : LifetimeScope
{
    [SerializeField] private ItemDatabase itemDatabase;
    [SerializeField] private AudioSettings audioSettings;

    protected override void Configure(IContainerBuilder builder)
    {
        // Register interfaces → implementations
        builder.Register<IWallet, PlayerWallet>(Lifetime.Singleton);
        builder.Register<IInventory, PlayerInventory>(Lifetime.Singleton);
        builder.Register<IAudioService, UnityAudioService>(Lifetime.Singleton);
        builder.Register<ISaveService, JsonSaveService>(Lifetime.Singleton);
        builder.Register<ShopSystem>(Lifetime.Singleton);

        // Register ScriptableObjects as instances
        builder.RegisterInstance<IItemDatabase>(itemDatabase);
        builder.RegisterInstance(audioSettings);

        // Register MonoBehaviours from scene
        builder.RegisterComponentInHierarchy<PlayerController>();

        // Entry point (replaces MonoBehaviour lifecycle)
        builder.RegisterEntryPoint<GameInitializer>();
    }
}

// Entry point: runs after all dependencies are resolved
public class GameInitializer : IStartable, ITickable
{
    private readonly ISaveService _save;
    private readonly IWallet _wallet;

    [Inject]
    public GameInitializer(ISaveService save, IWallet wallet)
    {
        _save = save;
        _wallet = wallet;
    }

    public void Start()
    {
        var data = _save.Load();
        _wallet.SetGold(data?.Gold ?? 0);
    }

    public void Tick()
    {
        // Runs every frame (like Update but without MonoBehaviour)
    }
}
```


---

## 🔑 2. Mechanics — Save Systems

### 2.1 — Save System Architecture

```csharp
// Versioned save data (supports migration between game versions)
[Serializable]
public class SaveData
{
    public int Version = 1;
    public string PlayerId;
    public DateTime LastSaved;

    // Game state
    public PlayerSaveData Player;
    public FarmSaveData Farm;
    public InventorySaveData Inventory;
    public QuestSaveData Quests;
    public RelationshipSaveData Relationships;
}

[Serializable]
public class PlayerSaveData
{
    public float X, Y;
    public int Gold;
    public int Day;
    public Season CurrentSeason;
    public int Year;
}

[Serializable]
public class FarmSaveData
{
    public List<CropSaveEntry> Crops;
    public List<BuildingSaveEntry> Buildings;
    public bool[] WateredTiles;  // Bitfield for 64x64 farm
}

[Serializable]
public struct CropSaveEntry
{
    public int TileX, TileY;
    public string CropId;
    public float Growth;
    public int DayPlanted;
}
```

### 2.2 — Robust Save/Load Implementation

```csharp
public interface ISaveService
{
    Task SaveAsync(SaveData data, CancellationToken ct = default);
    Task<SaveData?> LoadAsync(CancellationToken ct = default);
    bool SaveExists(int slot);
    void DeleteSave(int slot);
}

public class JsonSaveService : ISaveService
{
    private readonly string _basePath;
    private readonly JsonSerializerOptions _jsonOptions;

    public JsonSaveService()
    {
        _basePath = Path.Combine(Application.persistentDataPath, "saves");
        Directory.CreateDirectory(_basePath);

        _jsonOptions = new JsonSerializerOptions
        {
            WriteIndented = true,
            Converters = { new Vector2IntConverter(), new ColorConverter() }
        };
    }

    public async Task SaveAsync(SaveData data, CancellationToken ct = default)
    {
        data.LastSaved = DateTime.UtcNow;
        var json = JsonSerializer.Serialize(data, _jsonOptions);

        var savePath = GetSavePath(data.PlayerId);
        var tempPath = savePath + ".tmp";
        var backupPath = savePath + ".bak";

        // 1. Write to temp file
        await File.WriteAllTextAsync(tempPath, json, ct);

        // 2. Verify temp file is valid (re-read and deserialize)
        var verification = await File.ReadAllTextAsync(tempPath, ct);
        var verified = JsonSerializer.Deserialize<SaveData>(verification, _jsonOptions);
        if (verified?.PlayerId != data.PlayerId)
            throw new SaveCorruptionException("Verification failed");

        // 3. Backup existing save
        if (File.Exists(savePath))
            File.Copy(savePath, backupPath, overwrite: true);

        // 4. Atomic rename (temp → save)
        File.Move(tempPath, savePath, overwrite: true);
    }

    public async Task<SaveData?> LoadAsync(CancellationToken ct = default)
    {
        var savePath = GetSavePath("default");
        if (!File.Exists(savePath))
        {
            // Try backup
            var backupPath = savePath + ".bak";
            if (File.Exists(backupPath))
                savePath = backupPath;
            else
                return null;
        }

        var json = await File.ReadAllTextAsync(savePath, ct);
        var data = JsonSerializer.Deserialize<SaveData>(json, _jsonOptions);

        // Version migration
        if (data is not null)
            data = MigrateSave(data);

        return data;
    }

    private SaveData MigrateSave(SaveData data)
    {
        // Version 1 → 2: Added relationships
        if (data.Version < 2)
        {
            data.Relationships = new RelationshipSaveData();
            data.Version = 2;
        }
        // Version 2 → 3: Changed crop format
        if (data.Version < 3)
        {
            // Migration logic...
            data.Version = 3;
        }
        return data;
    }

    private string GetSavePath(string id) => Path.Combine(_basePath, $"{id}.json");
    public bool SaveExists(int slot) => File.Exists(GetSavePath($"slot_{slot}"));
    public void DeleteSave(int slot) => File.Delete(GetSavePath($"slot_{slot}"));
}
```

### 2.3 — ISaveable Pattern (Each System Saves Itself)

```csharp
public interface ISaveable
{
    string SaveId { get; }
    object CaptureState();
    void RestoreState(object state);
}

// Each system implements ISaveable
public class PlayerInventory : MonoBehaviour, ISaveable
{
    public string SaveId => "player_inventory";

    public object CaptureState() => new InventorySaveData
    {
        Items = _slots.Select(s => new ItemEntry(s.ItemId, s.Count)).ToList()
    };

    public void RestoreState(object state)
    {
        if (state is InventorySaveData data)
        {
            ClearAll();
            foreach (var item in data.Items)
                Add(item.ItemId, item.Count);
        }
    }
}

// Save coordinator collects all ISaveable components
public class SaveCoordinator
{
    private readonly ISaveService _saveService;
    private readonly List<ISaveable> _saveables = new();

    public void Register(ISaveable saveable) => _saveables.Add(saveable);

    public async Task SaveGameAsync(CancellationToken ct = default)
    {
        var data = new SaveData();
        var states = new Dictionary<string, object>();

        foreach (var saveable in _saveables)
            states[saveable.SaveId] = saveable.CaptureState();

        data.States = states;
        await _saveService.SaveAsync(data, ct);
    }

    public async Task LoadGameAsync(CancellationToken ct = default)
    {
        var data = await _saveService.LoadAsync(ct);
        if (data?.States is null) return;

        foreach (var saveable in _saveables)
        {
            if (data.States.TryGetValue(saveable.SaveId, out var state))
                saveable.RestoreState(state);
        }
    }
}
```


---

## 🔑 3. Mechanics — Addressables

### 10.1 — What Are Addressables?

Addressables replace `Resources.Load()` with an async, reference-counted asset loading system:

| Old Way (Resources) | Addressables |
|---------------------|-------------|
| `Resources.Load<Sprite>("crops/parsnip")` | `Addressables.LoadAssetAsync<Sprite>("crops/parsnip")` |
| Loads synchronously (freezes game) | Loads asynchronously |
| Everything in Resources folder ships in build | Only referenced assets ship |
| No memory management | Reference-counted, explicit release |
| No remote loading | Can load from CDN (DLC!) |

### 10.2 — Basic Usage

```csharp
using UnityEngine.AddressableAssets;
using UnityEngine.ResourceManagement.AsyncOperations;

public class CropVisualLoader : MonoBehaviour
{
    private AsyncOperationHandle<Sprite> _spriteHandle;

    public async UniTask LoadCropSprite(string cropId)
    {
        // Load by address (set in Addressables Groups window)
        _spriteHandle = Addressables.LoadAssetAsync<Sprite>($"crops/{cropId}");
        var sprite = await _spriteHandle.ToUniTask();

        GetComponent<SpriteRenderer>().sprite = sprite;
    }

    void OnDestroy()
    {
        // MUST release when done — reference counted!
        if (_spriteHandle.IsValid())
            Addressables.Release(_spriteHandle);
    }
}

// Load multiple assets
public async UniTask<IList<CropDefinition>> LoadAllCropsAsync()
{
    var handle = Addressables.LoadAssetsAsync<CropDefinition>("crops", null);
    var crops = await handle.ToUniTask();
    return crops;
}

// Instantiate prefab by address
public async UniTask SpawnNPC(string npcId, Vector3 position)
{
    var handle = Addressables.InstantiateAsync($"npcs/{npcId}", position, Quaternion.identity);
    var npc = await handle.ToUniTask();
    // handle is auto-released when npc is destroyed (if using Addressables.InstantiateAsync)
}
```

### 10.3 — Seasonal Content with Addressables (DLC Pattern)

```csharp
public class SeasonalContentManager
{
    private readonly Dictionary<Season, AsyncOperationHandle> _loadedSeasons = new();

    public async UniTask LoadSeasonContent(Season season)
    {
        // Unload previous season
        if (_loadedSeasons.TryGetValue(_currentSeason, out var oldHandle))
        {
            Addressables.Release(oldHandle);
            _loadedSeasons.Remove(_currentSeason);
        }

        // Load new season's asset bundle (could be remote!)
        var label = $"season_{season.ToString().ToLower()}";
        var handle = Addressables.LoadAssetsAsync<Object>(label, null);
        await handle.ToUniTask();

        _loadedSeasons[season] = handle;
    }
}
```

---

## 🔑 4. Mechanics — Testing

### 4.1 — Unit Tests (NUnit + Unity Test Framework)

```csharp
using NUnit.Framework;

[TestFixture]
public class InventoryTests
{
    private Inventory<CropItem> _inventory;

    [SetUp]
    public void Setup()
    {
        _inventory = new Inventory<CropItem>(capacity: 24);
    }

    [Test]
    public void Add_SingleItem_OccupiesOneSlot()
    {
        var parsnip = new CropItem("parsnip", "Parsnip", 64, 35f);

        bool added = _inventory.TryAdd(parsnip, 1);

        Assert.That(added, Is.True);
        Assert.That(_inventory.UsedSlots, Is.EqualTo(1));
    }

    [Test]
    public void Add_BeyondCapacity_ReturnsFalse()
    {
        for (int i = 0; i < 24; i++)
            _inventory.TryAdd(new CropItem($"item_{i}", $"Item {i}", 1, 10f));

        var overflow = new CropItem("extra", "Extra", 1, 10f);
        Assert.That(_inventory.TryAdd(overflow), Is.False);
    }

    [Test]
    public void Add_Stackable_StacksInSameSlot()
    {
        var parsnip = new CropItem("parsnip", "Parsnip", 64, 35f);

        _inventory.TryAdd(parsnip, 10);
        _inventory.TryAdd(parsnip, 5);

        Assert.That(_inventory.UsedSlots, Is.EqualTo(1));
        Assert.That(_inventory.TotalCount("parsnip"), Is.EqualTo(15));
    }
}

// Mock for DI testing
public class MockWallet : IWallet
{
    public int Gold { get; private set; }
    public MockWallet(int startGold) => Gold = startGold;
    public void Spend(int amount) => Gold -= amount;
    public void Add(int amount) => Gold += amount;
}
```

### 4.2 — Play Mode Tests (Integration)

```csharp
using UnityEngine.TestTools;
using System.Collections;

public class FarmIntegrationTests
{
    [UnityTest]
    public IEnumerator PlantingCrop_ShowsVisual_AfterOneFrame()
    {
        // Arrange
        var farm = new GameObject().AddComponent<FarmGrid>();
        var cropDef = ScriptableObject.CreateInstance<CropDefinition>();
        cropDef.cropName = "TestCrop";

        // Act
        farm.PlantCrop(new Vector2Int(0, 0), cropDef);
        yield return null;  // Wait one frame

        // Assert
        var visual = GameObject.Find("CropVisual_0_0");
        Assert.That(visual, Is.Not.Null);

        // Cleanup
        Object.Destroy(farm.gameObject);
    }
}
```

---

## 🔑 5. Mechanics — CI/CD

### 5.1 — GameCI (GitHub Actions for Unity)

```yaml
# .github/workflows/build.yml
name: Unity Build

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: game-ci/unity-test-runner@v4
        with:
          projectPath: .
          testMode: all
          unityVersion: 6000.0.0f1

  build:
    needs: test
    runs-on: ubuntu-latest
    strategy:
      matrix:
        targetPlatform: [StandaloneWindows64, StandaloneLinux64]
    steps:
      - uses: actions/checkout@v4
      - uses: game-ci/unity-builder@v4
        with:
          targetPlatform: ${{ matrix.targetPlatform }}
          unityVersion: 6000.0.0f1
      - uses: actions/upload-artifact@v4
        with:
          name: Build-${{ matrix.targetPlatform }}
          path: build/${{ matrix.targetPlatform }}
```

---

## ⚠️ 6. Gotchas

### Gotcha 3.8.1 — Addressables Memory Leaks
```csharp
// ❌ Loading without releasing = memory leak
async void LoadSprite()
{
    var sprite = await Addressables.LoadAssetAsync<Sprite>("my_sprite").Task;
    // sprite is loaded but handle is lost — can never release!
}

// ✓ Keep the handle, release when done
private AsyncOperationHandle<Sprite> _handle;
async void LoadSprite()
{
    _handle = Addressables.LoadAssetAsync<Sprite>("my_sprite");
    var sprite = await _handle.Task;
}
void OnDestroy() => Addressables.Release(_handle);
```

### Gotcha 3.8.2 — Save Corruption on Crash
```csharp
// ❌ Writing directly to save file — crash mid-write = corrupted
File.WriteAllText(savePath, json);  // Power loss here = partial file!

// ✓ Write-to-temp + atomic rename (shown in 2.2 above)
// ✓ Keep .bak backup of previous valid save
// ✓ Verify after write (re-read and deserialize)
```

### Gotcha 3.8.3 — DI Container Overhead
```csharp
// ❌ Resolving from container in Update (reflection overhead)
void Update()
{
    var service = container.Resolve<IMyService>();  // Slow!
}

// ✓ Inject once in constructor/Awake, use cached reference
private readonly IMyService _service;
public MySystem(IMyService service) => _service = service;
void Update() => _service.DoThing();  // Fast: direct call
```

### Gotcha 3.8.4 — Serialization Pitfalls
```csharp
// ❌ Renaming a field breaks deserialization of old saves
[Serializable] public class OldSave { public int playerGold; }
[Serializable] public class NewSave { public int gold; }  // Old saves lose gold!

// ✓ Use [JsonPropertyName] or version migration
[Serializable] public class SaveData
{
    [JsonPropertyName("playerGold")]  // Maps old name to new field
    public int Gold { get; set; }
}
```

---

## 🔗 7. Cross-References

- **Previous**: [10.7 - Networking & Multiplayer - Mirror, Photon & Unity Netcode](10.7---Networking-&-Multiplayer---Mirror,-Photon-&-Unity-Netcode)
- **Track Start**: [Subject_Plan](Subject_Plan)
- **Design Patterns**: [10.3 - OOP & Design Patterns](10.3---OOP-&-Design-Patterns) — Observer, Factory used here
- **Async Loading**: [10.4 - Async, Await, Tasks & Threading](10.4---Async,-Await,-Tasks-&-Threading) — UniTask for Addressables
- **Memory**: [10.5 - Memory Management & Performance](10.5---Memory-Management-&-Performance) — Asset memory management
- **Unity Lifecycle**: [10.6 - Unity Specifics - MonoBehaviour, Coroutines, ScriptableObjects, ECS](10.6---Unity-Specifics---MonoBehaviour,-Coroutines,-ScriptableObjects,-ECS)

---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — VContainer DI Patterns for Unity

**Problem:** Your Unity game has complex dependency graphs (services depending on other services). Manual wiring in MonoBehaviours creates brittle, untestable code. Use VContainer (lightweight DI for Unity) to manage object lifetimes and dependencies.

<details>
<summary>🔍 Full step-by-step solution</summary>

```csharp
using VContainer;
using VContainer.Unity;

// ═══════════════════════════════════════════════════════════════
// LIFETIME SCOPE: Defines what gets created and how long it lives
// ═══════════════════════════════════════════════════════════════

// Root scope (lives for entire application)
public class RootLifetimeScope : LifetimeScope
{
    protected override void Configure(IContainerBuilder builder)
    {
        // Singletons: One instance for the entire game
        builder.Register<ISaveService, LocalSaveService>(Lifetime.Singleton);
        builder.Register<IAudioService, FmodAudioService>(Lifetime.Singleton);
        builder.Register<IAnalyticsService, UnityAnalyticsService>(Lifetime.Singleton);
        builder.Register<GameSettings>(Lifetime.Singleton);
        
        // Register ScriptableObject instances
        builder.RegisterInstance(Resources.Load<GameConfig>("GameConfig"));
    }
}

// Scene scope (lives for one scene, inherits from root)
public class GameplayLifetimeScope : LifetimeScope
{
    [SerializeField] private PlayerController _playerPrefab;

    protected override void Configure(IContainerBuilder builder)
    {
        // Scoped: One instance per scene
        builder.Register<IInventoryService, InventoryService>(Lifetime.Scoped);
        builder.Register<ICombatService, CombatService>(Lifetime.Scoped);
        builder.Register<IQuestService, QuestService>(Lifetime.Scoped);
        
        // Transient: New instance every time it's requested
        builder.Register<DamageCalculator>(Lifetime.Transient);

        // Register MonoBehaviours that exist in the scene
        builder.RegisterComponentInHierarchy<UIManager>();
        builder.RegisterComponentInHierarchy<CameraController>();

        // Register prefabs for factory creation
        builder.RegisterFactory<PlayerController>(container =>
        {
            return () =>
            {
                var player = Instantiate(_playerPrefab);
                container.InjectGameObject(player.gameObject);
                return player;
            };
        }, Lifetime.Scoped);

        // Entry point: VContainer calls IStartable.Start() after injection
        builder.RegisterEntryPoint<GameplayInitializer>();
    }
}

// ═══════════════════════════════════════════════════════════════
// SERVICES: Constructor injection (no [SerializeField] needed)
// ═══════════════════════════════════════════════════════════════

public interface IInventoryService
{
    bool AddItem(string itemId, int quantity);
    bool RemoveItem(string itemId, int quantity);
    IReadOnlyList<InventorySlot> GetSlots();
}

public class InventoryService : IInventoryService
{
    private readonly ISaveService _saveService;
    private readonly GameConfig _config;
    private readonly List<InventorySlot> _slots;

    // VContainer injects these automatically via constructor
    public InventoryService(ISaveService saveService, GameConfig config)
    {
        _saveService = saveService;
        _config = config;
        _slots = new List<InventorySlot>(config.MaxInventorySlots);
    }

    public bool AddItem(string itemId, int quantity)
    {
        // ... implementation ...
        _saveService.MarkDirty(); // Auto-save trigger
        return true;
    }

    public bool RemoveItem(string itemId, int quantity) { /* ... */ return true; }
    public IReadOnlyList<InventorySlot> GetSlots() => _slots;
}

// ═══════════════════════════════════════════════════════════════
// MONOBEHAVIOUR INJECTION: For components that must be in scene
// ═══════════════════════════════════════════════════════════════

public class PlayerController : MonoBehaviour
{
    // [Inject] attribute for MonoBehaviour method injection
    private ICombatService _combat;
    private IInventoryService _inventory;
    private IAudioService _audio;

    [Inject]
    public void Construct(ICombatService combat, IInventoryService inventory, IAudioService audio)
    {
        _combat = combat;
        _inventory = inventory;
        _audio = audio;
    }

    private void Update()
    {
        if (Input.GetButtonDown("Attack"))
            _combat.PerformAttack(transform.position, transform.forward);
    }
}

// ═══════════════════════════════════════════════════════════════
// ENTRY POINT: Game initialization without MonoBehaviour
// ═══════════════════════════════════════════════════════════════

public class GameplayInitializer : IStartable, ITickable, IDisposable
{
    private readonly IInventoryService _inventory;
    private readonly ISaveService _save;

    public GameplayInitializer(IInventoryService inventory, ISaveService save)
    {
        _inventory = inventory;
        _save = save;
    }

    public void Start()
    {
        // Called once after all injection is complete
        _save.LoadAsync().Forget();
    }

    public void Tick()
    {
        // Called every frame (like Update but without MonoBehaviour)
    }

    public void Dispose()
    {
        // Cleanup when scope is destroyed
        _save.SaveAsync().Forget();
    }
}
```

</details>

### Example 8.2 — Save System with Versioning and Migration

**Problem:** Your game needs a save system that handles: schema changes between updates, corruption recovery, multiple save slots, and cross-platform compatibility.

<details>
<summary>🔍 Full step-by-step solution</summary>

```csharp
using MessagePack;
using System.IO;
using System.IO.Compression;

// ═══════════════════════════════════════════════════════════════
// SAVE DATA SCHEMA: Versioned, evolvable
// ═══════════════════════════════════════════════════════════════

[MessagePackObject]
public class SaveFile
{
    [Key(0)] public int Version { get; set; } = SaveMigrator.CurrentVersion;
    [Key(1)] public DateTime SavedAt { get; set; }
    [Key(2)] public string PlayerId { get; set; } = "";
    [Key(3)] public PlayerSaveData Player { get; set; } = new();
    [Key(4)] public WorldSaveData World { get; set; } = new();
    [Key(5)] public List<QuestSaveData> Quests { get; set; } = new();
    [Key(6)] public Dictionary<string, int> Flags { get; set; } = new();
}

[MessagePackObject]
public class PlayerSaveData
{
    [Key(0)] public float PositionX { get; set; }
    [Key(1)] public float PositionY { get; set; }
    [Key(2)] public float PositionZ { get; set; }
    [Key(3)] public int Health { get; set; } = 100;
    [Key(4)] public int MaxHealth { get; set; } = 100;
    [Key(5)] public List<InventoryItemData> Inventory { get; set; } = new();
    [Key(6)] public int Gold { get; set; }
    [Key(7)] public int Level { get; set; } = 1;
    [Key(8)] public int Experience { get; set; }
    // V3 addition:
    [Key(9)] public Dictionary<string, int> Skills { get; set; } = new();
}

// ═══════════════════════════════════════════════════════════════
// MIGRATION SYSTEM: Upgrade old saves to current schema
// ═══════════════════════════════════════════════════════════════

public static class SaveMigrator
{
    public const int CurrentVersion = 3;

    public static SaveFile Migrate(SaveFile save)
    {
        while (save.Version < CurrentVersion)
        {
            save = save.Version switch
            {
                1 => MigrateV1ToV2(save),
                2 => MigrateV2ToV3(save),
                _ => throw new InvalidOperationException($"Unknown save version: {save.Version}")
            };
        }
        return save;
    }

    private static SaveFile MigrateV1ToV2(SaveFile save)
    {
        // V2 added: MaxHealth field, Gold field
        save.Player.MaxHealth = 100; // Default for old saves
        save.Player.Gold = 0;
        save.Version = 2;
        return save;
    }

    private static SaveFile MigrateV2ToV3(SaveFile save)
    {
        // V3 added: Skills dictionary
        save.Player.Skills = new Dictionary<string, int>
        {
            ["mining"] = 1,
            ["farming"] = 1,
            ["combat"] = save.Player.Level // Derive from existing data
        };
        save.Version = 3;
        return save;
    }
}

// ═══════════════════════════════════════════════════════════════
// SAVE SERVICE: Handles I/O, compression, corruption recovery
// ═══════════════════════════════════════════════════════════════

public interface ISaveService
{
    UniTask SaveAsync(SaveFile data, int slot = 0);
    UniTask<SaveFile?> LoadAsync(int slot = 0);
    UniTask<SaveFile[]> GetAllSaveSlotsAsync();
    void MarkDirty();
}

public class LocalSaveService : ISaveService, IDisposable
{
    private readonly string _basePath;
    private bool _isDirty;
    private SaveFile _currentSave;
    private CancellationTokenSource _autoSaveCts;

    public LocalSaveService()
    {
        _basePath = Path.Combine(Application.persistentDataPath, "saves");
        Directory.CreateDirectory(_basePath);
        StartAutoSave();
    }

    public async UniTask SaveAsync(SaveFile data, int slot = 0)
    {
        data.SavedAt = DateTime.UtcNow;
        string path = GetSlotPath(slot);
        string backupPath = path + ".bak";

        // 1. Write to temp file first (atomic write pattern)
        string tempPath = path + ".tmp";
        byte[] serialized = MessagePackSerializer.Serialize(data);
        byte[] compressed = Compress(serialized);

        await File.WriteAllBytesAsync(tempPath, compressed);

        // 2. Backup existing save
        if (File.Exists(path))
            File.Copy(path, backupPath, overwrite: true);

        // 3. Atomic rename (prevents corruption on crash)
        File.Move(tempPath, path, overwrite: true);

        _isDirty = false;
        _currentSave = data;
    }

    public async UniTask<SaveFile?> LoadAsync(int slot = 0)
    {
        string path = GetSlotPath(slot);
        string backupPath = path + ".bak";

        // Try primary save first
        var save = await TryLoadFile(path);
        if (save != null)
        {
            _currentSave = SaveMigrator.Migrate(save);
            return _currentSave;
        }

        // Primary corrupted — try backup
        save = await TryLoadFile(backupPath);
        if (save != null)
        {
            Debug.LogWarning("Primary save corrupted, loaded backup");
            _currentSave = SaveMigrator.Migrate(save);
            await SaveAsync(_currentSave, slot); // Repair primary
            return _currentSave;
        }

        // Both corrupted — return null (new game)
        Debug.LogError("All save files corrupted");
        return null;
    }

    private async UniTask<SaveFile?> TryLoadFile(string path)
    {
        if (!File.Exists(path)) return null;
        try
        {
            byte[] compressed = await File.ReadAllBytesAsync(path);
            byte[] decompressed = Decompress(compressed);
            return MessagePackSerializer.Deserialize<SaveFile>(decompressed);
        }
        catch (Exception ex)
        {
            Debug.LogError($"Failed to load {path}: {ex.Message}");
            return null;
        }
    }

    private static byte[] Compress(byte[] data)
    {
        using var output = new MemoryStream();
        using (var gzip = new GZipStream(output, CompressionLevel.Fastest))
            gzip.Write(data);
        return output.ToArray();
    }

    private static byte[] Decompress(byte[] data)
    {
        using var input = new MemoryStream(data);
        using var gzip = new GZipStream(input, CompressionMode.Decompress);
        using var output = new MemoryStream();
        gzip.CopyTo(output);
        return output.ToArray();
    }

    private string GetSlotPath(int slot) => Path.Combine(_basePath, $"save_{slot}.dat");

    public void MarkDirty() => _isDirty = true;

    private void StartAutoSave()
    {
        _autoSaveCts = new CancellationTokenSource();
        AutoSaveLoop(_autoSaveCts.Token).Forget();
    }

    private async UniTaskVoid AutoSaveLoop(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            await UniTask.Delay(60_000, cancellationToken: ct); // Every 60 seconds
            if (_isDirty && _currentSave != null)
                await SaveAsync(_currentSave);
        }
    }

    public void Dispose() => _autoSaveCts?.Cancel();

    public async UniTask<SaveFile[]> GetAllSaveSlotsAsync()
    {
        var saves = new List<SaveFile>();
        for (int i = 0; i < 5; i++)
        {
            var save = await TryLoadFile(GetSlotPath(i));
            if (save != null) saves.Add(save);
        }
        return saves.ToArray();
    }
}
```

</details>

### Example 8.3 — Addressables Remote Content Workflow

**Problem:** You want to ship a small initial build and download additional content (levels, characters, events) from a CDN without requiring app store updates.

<details>
<summary>🔍 Full step-by-step solution</summary>

```csharp
using UnityEngine.AddressableAssets;
using UnityEngine.AddressableAssets.ResourceLocators;
using UnityEngine.ResourceManagement.AsyncOperations;

// ═══════════════════════════════════════════════════════════════
// CONTENT UPDATE CHECKER: Download new content on game start
// ═══════════════════════════════════════════════════════════════

public class ContentUpdateManager : MonoBehaviour
{
    [SerializeField] private string _catalogUrl = "https://cdn.mygame.com/catalog.json";
    
    public event Action<float> OnDownloadProgress;
    public event Action<long> OnDownloadSizeKnown;
    public event Action OnUpdateComplete;

    public async UniTask CheckForUpdatesAsync(CancellationToken ct)
    {
        // 1. Check if remote catalog has changed
        var checkHandle = Addressables.CheckForCatalogUpdates(false);
        await checkHandle.WithCancellation(ct);

        List<string> catalogsToUpdate = checkHandle.Result;
        Addressables.Release(checkHandle);

        if (catalogsToUpdate.Count == 0)
        {
            Debug.Log("Content is up to date");
            OnUpdateComplete?.Invoke();
            return;
        }

        // 2. Update catalogs
        var updateHandle = Addressables.UpdateCatalogs(catalogsToUpdate, false);
        await updateHandle.WithCancellation(ct);
        Addressables.Release(updateHandle);

        // 3. Calculate download size
        var sizeHandle = Addressables.GetDownloadSizeAsync("remote_content");
        await sizeHandle.WithCancellation(ct);
        long downloadSize = sizeHandle.Result;
        Addressables.Release(sizeHandle);

        if (downloadSize > 0)
        {
            OnDownloadSizeKnown?.Invoke(downloadSize);
            await DownloadContentAsync(ct);
        }

        OnUpdateComplete?.Invoke();
    }

    private async UniTask DownloadContentAsync(CancellationToken ct)
    {
        var downloadHandle = Addressables.DownloadDependenciesAsync("remote_content", false);

        // Report progress
        while (!downloadHandle.IsDone)
        {
            OnDownloadProgress?.Invoke(downloadHandle.PercentComplete);
            await UniTask.Yield(ct);
        }

        if (downloadHandle.Status == AsyncOperationStatus.Failed)
            Debug.LogError($"Download failed: {downloadHandle.OperationException}");

        Addressables.Release(downloadHandle);
    }
}

// ═══════════════════════════════════════════════════════════════
// ADDRESSABLE ASSET LOADER: Type-safe loading with caching
// ═══════════════════════════════════════════════════════════════

public class AssetLoader : IDisposable
{
    private readonly Dictionary<string, AsyncOperationHandle> _loadedAssets = new();

    public async UniTask<T> LoadAsync<T>(string address, CancellationToken ct) where T : Object
    {
        if (_loadedAssets.TryGetValue(address, out var existing))
            return (T)existing.Result;

        var handle = Addressables.LoadAssetAsync<T>(address);
        await handle.WithCancellation(ct);

        if (handle.Status == AsyncOperationStatus.Succeeded)
        {
            _loadedAssets[address] = handle;
            return handle.Result;
        }

        throw new InvalidOperationException($"Failed to load asset: {address}");
    }

    public void Release(string address)
    {
        if (_loadedAssets.TryGetValue(address, out var handle))
        {
            Addressables.Release(handle);
            _loadedAssets.Remove(address);
        }
    }

    public void Dispose()
    {
        foreach (var handle in _loadedAssets.Values)
            Addressables.Release(handle);
        _loadedAssets.Clear();
    }
}
```

#### Build & Deploy Pipeline

```bash
# 1. Build Addressable content
# Unity Editor: Window → Asset Management → Addressables → Build → New Build

# 2. Upload bundles to CDN
# Output: Library/com.unity.addressables/aa/[platform]/
aws s3 sync ./ServerData/ s3://my-game-cdn/addressables/ --cache-control "max-age=3600"

# 3. Update catalog URL in AddressableAssetSettings
# Remote.LoadPath: https://cdn.mygame.com/addressables/[BuildTarget]

# 4. For content updates (no new app build needed):
# Unity Editor: Build → Update a Previous Build
# This generates a content_state.bin diff — only changed bundles are rebuilt
```

</details>

### Example 8.4 — CI/CD with Unity Cloud Build

<details>
<summary>🔍 Full step-by-step solution</summary>

```yaml
# .github/workflows/unity-build.yml
# GitHub Actions + GameCI for Unity builds
name: Unity Build Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          lfs: true
      
      - uses: game-ci/unity-test-runner@v4
        with:
          projectPath: .
          testMode: all
          artifactsPath: test-results
          githubToken: ${{ secrets.GITHUB_TOKEN }}
          unityVersion: 6000.0.0f1
      
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: test-results

  build:
    needs: test
    runs-on: ubuntu-latest
    strategy:
      matrix:
        targetPlatform:
          - StandaloneWindows64
          - StandaloneLinux64
          - WebGL
    steps:
      - uses: actions/checkout@v4
        with:
          lfs: true
      
      - uses: game-ci/unity-builder@v4
        with:
          projectPath: .
          targetPlatform: ${{ matrix.targetPlatform }}
          unityVersion: 6000.0.0f1
          buildMethod: BuildScript.PerformBuild
        env:
          UNITY_LICENSE: ${{ secrets.UNITY_LICENSE }}
      
      - uses: actions/upload-artifact@v4
        with:
          name: build-${{ matrix.targetPlatform }}
          path: build/${{ matrix.targetPlatform }}

  deploy-server:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build-StandaloneLinux64
      
      - name: Deploy to game server
        run: |
          # Build Docker image and push to registry
          docker build -t my-game-server:${{ github.sha }} .
          docker push my-game-server:${{ github.sha }}
          # Update Kubernetes deployment
          kubectl set image deployment/game-server \
            server=my-game-server:${{ github.sha }}
```

```csharp
// Assets/Editor/BuildScript.cs — Custom build method for CI
using UnityEditor;
using UnityEditor.Build.Reporting;

public static class BuildScript
{
    public static void PerformBuild()
    {
        var options = new BuildPlayerOptions
        {
            scenes = EditorBuildSettings.scenes
                .Where(s => s.enabled)
                .Select(s => s.path)
                .ToArray(),
            locationPathName = GetBuildPath(),
            target = EditorUserBuildSettings.activeBuildTarget,
            options = BuildOptions.CompressWithLz4HC
        };

        var report = BuildPipeline.BuildPlayer(options);
        
        if (report.summary.result != BuildResult.Succeeded)
        {
            EditorApplication.Exit(1);
        }
    }

    private static string GetBuildPath()
    {
        var target = EditorUserBuildSettings.activeBuildTarget;
        var ext = target == BuildTarget.StandaloneWindows64 ? ".exe" : "";
        return $"build/{target}/Game{ext}";
    }
}
```

</details>

---

## 📖 9. Appendix: Extended Derivations & Special Cases

### Appendix 9.1 — Zenject Deprecation Rationale and VContainer Migration

#### Why Zenject Was Deprecated

Zenject (Extenject) was the dominant Unity DI framework for years but has issues:

1. **Abandoned maintenance**: No updates since 2021, growing incompatibilities with new Unity versions
2. **Heavy reflection usage**: Slow injection, IL2CPP stripping issues
3. **Complex API**: Installers, Facades, SubContainers — over-engineered for most games
4. **Memory overhead**: Large object graphs, circular dependency detection at runtime
5. **Unity 6 incompatibility**: Breaking changes in serialization and assembly loading

#### VContainer Advantages

| Feature | Zenject | VContainer |
|---------|---------|------------|
| Injection speed | ~10ms (reflection) | ~0.5ms (code gen) |
| IL2CPP compatible | Partial (needs link.xml) | Full |
| Memory overhead | High | Minimal |
| API complexity | High (Installers, Facades) | Low (one Configure method) |
| Unity 6 support | ❌ | ✅ |
| Source generator | ❌ | ✅ (optional) |
| Active development | ❌ | ✅ |

#### Migration Cheat Sheet

```csharp
// ZENJECT:
public class GameInstaller : MonoInstaller
{
    public override void InstallBindings()
    {
        Container.Bind<IPlayerService>().To<PlayerService>().AsSingle();
        Container.Bind<IEnemyFactory>().To<EnemyFactory>().AsSingle();
        Container.BindInterfacesAndSelfTo<GameManager>().AsSingle();
    }
}

// VCONTAINER EQUIVALENT:
public class GameLifetimeScope : LifetimeScope
{
    protected override void Configure(IContainerBuilder builder)
    {
        builder.Register<IPlayerService, PlayerService>(Lifetime.Singleton);
        builder.Register<IEnemyFactory, EnemyFactory>(Lifetime.Singleton);
        builder.Register<GameManager>(Lifetime.Singleton).AsImplementedInterfaces().AsSelf();
    }
}

// ZENJECT [Inject]:
public class Enemy : MonoBehaviour
{
    [Inject] private IPlayerService _playerService;
}

// VCONTAINER [Inject]:
public class Enemy : MonoBehaviour
{
    private IPlayerService _playerService;
    
    [Inject]
    public void Construct(IPlayerService playerService)
    {
        _playerService = playerService;
    }
}
```

### Appendix 9.2 — Multiplayer Server Hosting Options

#### Unity Game Server Hosting (Multiplay)

```
Pricing: Pay-per-use (server hours + bandwidth)
Regions: 15+ global regions
Scaling: Auto-scale based on player demand
Integration: Native Unity Dashboard, matchmaker included

Workflow:
1. Build dedicated server (Linux headless)
2. Upload build to Multiplay
3. Configure fleet (min/max servers, regions)
4. Matchmaker allocates servers on demand
5. Players connect via allocated server IP:port

Best for: Unity-native projects, teams wanting managed infrastructure
```

#### Edgegap (Distributed Edge Computing)

```
Pricing: Per-deployment minute + bandwidth
Regions: 500+ edge locations (closest to players)
Scaling: Instant deployment (<3 seconds cold start)
Integration: REST API, Unity SDK

Workflow:
1. Containerize game server (Docker)
2. Push image to Edgegap registry
3. API call to deploy: POST /v1/deploy
4. Server spins up at edge location nearest to requesting players
5. Returns IP:port for client connection
6. Auto-terminates when empty (cost savings)

Best for: Latency-sensitive games, global player base, cost optimization
```

#### Self-Hosted (AWS/GCP/Azure)

```
Pricing: EC2/Compute instances + bandwidth
Control: Full (but you manage everything)
Scaling: Manual or auto-scaling groups

Typical setup:
- Matchmaker: Lambda/Cloud Function (serverless)
- Game servers: EC2 Spot instances (70% cheaper)
- Database: DynamoDB/Firestore (player data)
- CDN: CloudFront/Cloud CDN (asset delivery)

Best for: Teams with DevOps expertise, custom requirements, cost control at scale
```

#### Comparison Matrix

| Feature | Unity Multiplay | Edgegap | Self-Hosted |
|---------|:-:|:-:|:-:|
| Setup complexity | Low | Medium | High |
| Latency optimization | Good | Best | Manual |
| Cost at 100 CCU | ~$50/mo | ~$30/mo | ~$20/mo |
| Cost at 10K CCU | ~$2000/mo | ~$1500/mo | ~$800/mo |
| Auto-scaling | ✅ | ✅ | Manual/ASG |
| Cold start time | ~30s | ~3s | ~60s |
| DDoS protection | Included | Included | Extra cost |
| Custom server logic | Full | Full | Full |

### Appendix 9.3 — Build Size Optimization Checklist

```
Pre-build:
□ Remove unused packages from Package Manager
□ Remove unused assets from project (use Asset Hunter Pro)
□ Set texture compression per-platform (ASTC for mobile, BC7 for PC)
□ Set audio compression (Vorbis for music, ADPCM for SFX)
□ Enable mesh compression in import settings
□ Remove unused shader variants (shader stripping)

Build settings:
□ IL2CPP backend (not Mono) for release
□ Managed Stripping Level: High
□ Strip Engine Code: enabled
□ Compress build: LZ4HC
□ Disable development build flag

Addressables:
□ Move non-essential assets to remote groups
□ Enable bundle compression (LZ4)
□ Pack assets by label (load only what's needed)
□ Disable "Include in Build" for remote groups

Post-build analysis:
□ Check Editor.log for "Build Report" section
□ Use "Build Report Inspector" package for visual breakdown
□ Identify largest assets and optimize or move to remote

Typical results:
- Unoptimized Unity build: 500 MB - 2 GB
- Optimized (local only): 100 - 300 MB
- Optimized (with remote content): 50 - 100 MB initial download
```

---

## 🔄 Maintenance
- **Created**: 2026-05-24
- **Last Updated**: 2026-05-24
