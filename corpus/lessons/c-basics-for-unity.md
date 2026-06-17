---
title: "C# Basics for Unity"
subject: "C#"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: code-reference
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# C# Basics for Unity

## Basic Syntax
```csharp
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    void Start()
    {
        Debug.Log("Game Started!");
    }
}
```

## Variables & Data Types
```csharp
// Basic types
int health = 100;
float speed = 5.5f;          // Note the 'f'!
double bigNumber = 123.456;
bool isAlive = true;
string playerName = "Billy";
char grade = 'A';

// Unity-specific types
Vector3 position = new Vector3(0, 0, 0);
Color playerColor = Color.red;
GameObject player;
Transform playerTransform;

// Nullable types
int? maybeNumber = null;
if(maybeNumber.HasValue)
{
    int value = maybeNumber.Value;
}

// Var (type inference)
var score = 100;             // int
var name = "Billy";          // string
```

## Access Modifiers
```csharp
public class Player : MonoBehaviour
{
    public int health = 100;           // Visible in Inspector
    private int score = 0;             // Only in this class
    protected float speed = 5f;        // This class + derived classes
    
    [SerializeField] private int coins;  // Private but shows in Inspector
    [HideInInspector] public int hidden; // Public but not in Inspector
}
```

## Properties (Getters/Setters)
```csharp
public class Player : MonoBehaviour
{
    private int health;
    
    // Full property
    public int Health
    {
        get { return health; }
        set 
        { 
            health = Mathf.Clamp(value, 0, 100);
        }
    }
    
    // Auto-property (C# 3.0+)
    public int Score { get; set; }
    
    // Read-only property
    public bool IsAlive { get { return health > 0; } }
    
    // Or with expression body (C# 6.0+)
    public bool IsDead => health <= 0;
}
```

## Methods
```csharp
// Basic method
void TakeDamage(int amount)
{
    health -= amount;
}

// Return value
int GetHealth()
{
    return health;
}

// Optional parameters
void Heal(int amount = 10)
{
    health += amount;
}

// Expression body (C# 6.0+)
int DoubleScore(int score) => score * 2;

// Ref parameter (modifies original)
void ModifyValue(ref int value)
{
    value *= 2;
}

// Out parameter (returns multiple values)
void GetPosition(out float x, out float y)
{
    x = transform.position.x;
    y = transform.position.y;
}

// Usage
float posX, posY;
GetPosition(out posX, out posY);
```

## Unity Lifecycle Methods
```csharp
public class PlayerController : MonoBehaviour
{
    // Called when script first loaded
    void Awake()
    {
        // Initialize before anything else
    }
    
    // Called on first frame (after Awake)
    void Start()
    {
        // Initialize game objects
    }
    
    // Called every frame
    void Update()
    {
        // Handle input, game logic
    }
    
    // Called at fixed intervals (physics)
    void FixedUpdate()
    {
        // Physics calculations
    }
    
    // Called after all Updates
    void LateUpdate()
    {
        // Camera follow, final adjustments
    }
    
    // Called when object destroyed
    void OnDestroy()
    {
        // Cleanup
    }
}
```

## Control Flow
```csharp
// If/else
if(health > 50)
{
    Debug.Log("Healthy");
}
else if(health > 0)
{
    Debug.Log("Hurt");
}
else
{
    Debug.Log("Dead");
}

// Ternary
string status = (health > 0) ? "Alive" : "Dead";

// Switch
switch(currentState)
{
    case GameState.Menu:
        ShowMenu();
        break;
    case GameState.Playing:
        UpdateGame();
        break;
    case GameState.GameOver:
        ShowGameOver();
        break;
    default:
        break;
}

// For loop
for(int i = 0; i < 10; i++)
{
    Debug.Log(i);
}

// Foreach
foreach(GameObject enemy in enemies)
{
    enemy.SetActive(false);
}

// While
while(isPlaying)
{
    UpdateGame();
}
```

## Collections
```csharp
// List (dynamic array - MOST COMMON)
List<GameObject> enemies = new List<GameObject>();
enemies.Add(newEnemy);
enemies.Remove(enemy);
enemies.Count;
enemies.Clear();

// Array (fixed size)
GameObject[] players = new GameObject[4];
players[0] = player1;

// Dictionary (key-value pairs)
Dictionary<string, int> scores = new Dictionary<string, int>();
scores.Add("Billy", 100);
scores["Alex"] = 95;
scores.ContainsKey("Billy");
scores.Remove("Billy");

// HashSet (unique values)
HashSet<int> uniqueIds = new HashSet<int>();
uniqueIds.Add(1);
uniqueIds.Add(1);  // Won't add duplicate
```

## Strings
```csharp
string name = "Billy";

// Concatenation
string greeting = "Hello " + name;
greeting += "!";

// String interpolation (C# 6.0+) - USE THIS!
string message = $"Hello {name}, score: {score}";
string calc = $"2 + 2 = {2 + 2}";

// Methods
name.Length;
name.ToUpper();
name.ToLower();
name.Contains("ill");
name.StartsWith("Bi");
name.Substring(0, 4);
name.Replace("Billy", "William");
name.Split(' ');
```

## Classes & Inheritance
```csharp
// Base class
public class Entity : MonoBehaviour
{
    protected int health;
    protected float speed;
    
    public virtual void TakeDamage(int amount)
    {
        health -= amount;
    }
}

// Derived class
public class Player : Entity
{
    public override void TakeDamage(int amount)
    {
        base.TakeDamage(amount);  // Call parent method
        Debug.Log("Player hurt!");
    }
}

// Abstract class (can't instantiate)
public abstract class Weapon : MonoBehaviour
{
    public abstract void Fire();  // Must implement in derived class
}

public class Gun : Weapon
{
    public override void Fire()
    {
        // Fire gun
    }
}
```

## Coroutines (Unity-specific!)
```csharp
// Start coroutine
StartCoroutine(FadeOut());

// Coroutine definition
IEnumerator FadeOut()
{
    float alpha = 1f;
    
    while(alpha > 0)
    {
        alpha -= Time.deltaTime;
        // Update UI alpha
        yield return null;  // Wait one frame
    }
}

// Wait for seconds
IEnumerator DelayedAction()
{
    yield return new WaitForSeconds(2f);
    Debug.Log("2 seconds passed");
}

// Stop coroutine
StopCoroutine(FadeOut());
StopAllCoroutines();
```

## Unity Component Access
```csharp
public class PlayerController : MonoBehaviour
{
    // Get component on same GameObject
    Rigidbody rb;
    
    void Start()
    {
        rb = GetComponent<Rigidbody>();
        
        // Or in child
        Transform childTransform = GetComponentInChildren<Transform>();
        
        // Or in parent
        Canvas canvas = GetComponentInParent<Canvas>();
    }
    
    // Find GameObject by name
    GameObject player = GameObject.Find("Player");
    
    // Find by tag
    GameObject enemy = GameObject.FindGameObjectWithTag("Enemy");
    GameObject[] enemies = GameObject.FindGameObjectsWithTag("Enemy");
    
    // Find component
    PlayerController controller = FindObjectOfType<PlayerController>();
}
```

## Events & Delegates
```csharp
// Delegate (function reference)
public delegate void OnHealthChanged(int newHealth);
public OnHealthChanged healthChangedCallback;

// Call delegate
if(healthChangedCallback != null)
{
    healthChangedCallback(health);
}

// C# events (safer delegates)
public event OnHealthChanged OnHealthChangedEvent;

// Subscribe to event
void Start()
{
    player.OnHealthChangedEvent += HandleHealthChanged;
}

void HandleHealthChanged(int newHealth)
{
    Debug.Log($"Health: {newHealth}");
}

// UnityEvents (show in Inspector)
using UnityEngine.Events;

public class Player : MonoBehaviour
{
    public UnityEvent onDeath;
    
    void Die()
    {
        onDeath.Invoke();  // Trigger event
    }
}
```

## Input Handling
```csharp
void Update()
{
    // Old Input System
    if(Input.GetKeyDown(KeyCode.Space))
    {
        Jump();
    }
    
    // Mouse
    if(Input.GetMouseButtonDown(0))  // Left click
    {
        Shoot();
    }
    
    // Axes
    float horizontal = Input.GetAxis("Horizontal");  // -1 to 1
    float vertical = Input.GetAxis("Vertical");
    
    // Raw (no smoothing)
    float h = Input.GetAxisRaw("Horizontal");  // -1, 0, or 1
}
```

## Instantiate & Destroy
```csharp
// Instantiate (spawn object)
public GameObject bulletPrefab;

void Shoot()
{
    GameObject bullet = Instantiate(bulletPrefab);
    
    // With position and rotation
    Instantiate(bulletPrefab, transform.position, transform.rotation);
    
    // As child
    Instantiate(bulletPrefab, transform);
}

// Destroy
Destroy(gameObject);          // Destroy this GameObject
Destroy(gameObject, 2f);      // Destroy after 2 seconds
Destroy(GetComponent<Rigidbody>());  // Destroy component only
```

## Null Checking (Unity Objects)
```csharp
// WRONG (for Unity objects)
if(gameObject != null) { }

// CORRECT
if(gameObject == null) { }

// Null-conditional operator
transform?.Rotate(Vector3.up);  // Only if not null

// Null-coalescing operator
GameObject obj = target ?? defaultTarget;
```

## LINQ (Query Collections)
```csharp
using System.Linq;

List<int> numbers = new List<int> { 1, 2, 3, 4, 5 };

// Filter
var evens = numbers.Where(n => n % 2 == 0);

// Transform
var doubled = numbers.Select(n => n * 2);

// Find first
var first = numbers.FirstOrDefault(n => n > 3);  // 4

// Any/All
bool hasEven = numbers.Any(n => n % 2 == 0);
bool allPositive = numbers.All(n => n > 0);

// Order
var ordered = numbers.OrderBy(n => n);
var reversed = numbers.OrderByDescending(n => n);
```

## Quick Unity Tips
- Use `[SerializeField]` for private fields in Inspector
- `Time.deltaTime` for frame-rate independent movement
- `Mathf.Clamp()` to limit values
- `Vector3.Lerp()` for smooth movement
- Use coroutines for timed actions
- Cache component references in `Start()`/`Awake()`
- Avoid `Find()` in `Update()` - very slow!
- Use object pooling instead of Instantiate/Destroy spam

## Common Unity Patterns
```csharp
// Singleton
public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }
    
    void Awake()
    {
        if(Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }
}

// Movement
void Update()
{
    float h = Input.GetAxis("Horizontal");
    float v = Input.GetAxis("Vertical");
    
    Vector3 movement = new Vector3(h, 0, v) * speed * Time.deltaTime;
    transform.Translate(movement);
}

// Smooth follow camera
void LateUpdate()
{
    Vector3 targetPosition = target.position + offset;
    transform.position = Vector3.Lerp(transform.position, targetPosition, smoothSpeed);
}
```

---

## Related Notes
- [Unity Basics](Unity-Basics)
- [C# Advanced Features](C#-Advanced-Features)
- [Unity Component Patterns](Unity-Component-Patterns)
- [Unity Performance Tips](Unity-Performance-Tips)
- [C# for Game Dev](C#-for-Game-Dev)
