---
title: "26.3 — 2D Game Patterns: Sprites, Tilemaps, Physics"
subject: "Game Dev"
catalog: advanced
audience_tier: higher-education
chapter: "26.3"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 26.3 — 2D Game Patterns: Sprites, Tilemaps, Physics

> *"I spent four years making Stardew Valley by myself. The most important thing I learned is that scope is everything. Start small, finish something, then expand."* — Eric "ConcernedApe" Barone

2D games are not simpler than 3D — they're differently complex. Tile-based worlds, sprite animation, pixel-perfect collision, and 2D physics each have deep implementation patterns. This chapter covers the systems you need for a Stardew Valley-style farming sim, a platformer, or a top-down action game. Your architecture background gives you an advantage here: think of tilemaps as floor plans and sprite sheets as material libraries.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Implement a **tilemap system** with multiple layers (ground, objects, collision).
2. Design **sprite animation** systems with state-driven frame selection.
3. Implement **AABB and circle collision detection** with spatial partitioning.
4. Build a **2D physics system** with gravity, friction, and one-way platforms.
5. Implement **pixel-perfect collision** for precise hitboxes.
6. Design a **camera system** with smooth follow, bounds clamping, and screen shake.
7. Understand **draw order** (Z-sorting, painter's algorithm) for correct layering.

---

## 🖼️ Visual Anchor — Tilemap & Collision Systems

![gamedev__4.3-fig1](gamedev__4.3-fig1.svg)

---

## 📚 1. Concepts & Definitions

### Definition 26.3.1 — Tilemap

A **tilemap** is a 2D grid where each cell references a tile from a tileset (sprite atlas). The world is composed by placing tile IDs in a 2D array:

```
int[,] groundLayer = {
    {1, 1, 1, 2, 2},  // 1=grass, 2=water
    {1, 3, 3, 3, 2},  // 3=path
    {1, 1, 1, 3, 1},
};
```

**Advantages:** Memory-efficient (store IDs not full sprites), enables procedural generation, trivial serialization, automatic collision from tile properties.

### Definition 26.3.2 — Sprite Sheet (Texture Atlas)

A **sprite sheet** packs multiple animation frames into a single texture. The renderer samples a sub-rectangle per frame:

$$
\text{UV}(frame) = \left(\frac{frame \mod cols}{cols}, \frac{\lfloor frame / cols \rfloor}{rows}\right)
$$

**Why single texture:** Reduces draw calls (batch all sprites using same atlas), reduces GPU state changes, enables GPU instancing.

### Definition 26.3.3 — AABB (Axis-Aligned Bounding Box)

An **AABB** is the simplest collision shape — a rectangle aligned to world axes:

$$
\text{overlap} = (A_{\max}.x > B_{\min}.x) \land (A_{\min}.x < B_{\max}.x) \land (A_{\max}.y > B_{\min}.y) \land (A_{\min}.y < B_{\max}.y)
$$

Cost: $O(1)$ per pair. Used as broad-phase before expensive narrow-phase checks.

### Definition 26.3.4 — Spatial Hashing

**Spatial hashing** divides the world into a grid of cells. Each entity is inserted into the cell(s) it overlaps. Collision checks only test entities in the same or adjacent cells:

$$
\text{cell}(x, y) = \left(\lfloor x / \text{cellSize} \rfloor, \lfloor y / \text{cellSize} \rfloor\right)
$$

Reduces collision checks from $O(n^2)$ to $O(n \cdot k)$ where $k$ = average entities per cell.

### Definition 26.3.5 — Swept AABB (Continuous Collision)

**Swept collision** detects collisions that occur *between* frames (tunneling prevention). Instead of testing static positions, test the moving AABB against static geometry:

$$
t_{\text{entry}} = \max(t_{x,\text{entry}}, t_{y,\text{entry}})
$$
$$
t_{\text{exit}} = \min(t_{x,\text{exit}}, t_{y,\text{exit}})
$$

Collision occurs if $t_{\text{entry}} < t_{\text{exit}}$ and $0 \leq t_{\text{entry}} \leq 1$.

---

## 🧩 2. Mental Models / Architecture

### Model 2.1 — Tilemap Layer Stack

```
Layer 4: UI / HUD (screen-space, always on top)
Layer 3: Entities (player, NPCs, items — Y-sorted)
Layer 2: Objects (trees, buildings — Y-sorted with entities)
Layer 1: Ground decoration (flowers, puddles)
Layer 0: Ground terrain (grass, dirt, water)
```

**Y-sorting:** Entities and objects sort by their Y position (feet). Objects with lower Y (further from camera) draw first. This creates correct depth without true 3D.

### Model 2.2 — 2D Physics Pipeline

```
1. Apply forces (gravity, input impulse)
2. Integrate velocity → tentative position
3. Broad phase (spatial hash → candidate pairs)
4. Narrow phase (AABB/circle test → contact manifold)
5. Resolve collisions (push out + adjust velocity)
6. Commit final position
```

### Model 2.3 — Tile Properties System

Each tile type carries metadata beyond its visual:

```json
{
  "id": 7,
  "name": "water_shallow",
  "sprite_index": 23,
  "collision": "none",
  "movement_cost": 3.0,
  "can_fish": true,
  "footstep_sound": "splash",
  "particle_effect": "ripple"
}
```

This data-driven approach means designers add gameplay properties without code changes.

---

## 🔑 3. Mechanics

### Mechanic 3.1 — Autotiling (Bitmasking)

**Autotiling** automatically selects the correct tile sprite based on neighboring tiles. A 4-bit bitmask encodes which neighbors match:

```
Bit layout (cardinal):
  [N]
[W] X [E]
  [S]

Bitmask = N*8 + E*4 + S*2 + W*1
```

For a 4-bit mask: 16 possible tile variants (inner corners, edges, full). For 8-bit (including diagonals): 47 unique variants (Wang tiles reduce this).

### Mechanic 3.2 — One-Way Platforms

Platforms the player can jump through from below but stand on from above:

```
Collision rule:
  if (player.velocity.y > 0)        // moving down
    AND (player.bottom <= platform.top)  // was above
    AND (player.bottom + dy > platform.top)  // would pass through
  → resolve collision (stand on platform)
  else → ignore (pass through)
```

### Mechanic 3.3 — Sub-Pixel Movement

At low speeds, integer pixel positions cause stuttering. Accumulate fractional movement:

```python
# Store position as float, render at rounded integer
self.x += velocity_x * dt  # float accumulation
self.y += velocity_y * dt
render_x = round(self.x)   # snap to pixel for rendering
render_y = round(self.y)
```

---

## 💻 4. Code Patterns & Examples

### 26.1 C# — Unity Tilemap with Custom Collision

```csharp
using UnityEngine;
using UnityEngine.Tilemaps;

public class TileWorldManager : MonoBehaviour
{
    [SerializeField] private Tilemap groundLayer;
    [SerializeField] private Tilemap collisionLayer;
    [SerializeField] private TileBase[] tileSet;
    
    private int[,] worldData;
    private int width, height;
    
    public void GenerateWorld(int w, int h, int seed)
    {
        width = w; height = h;
        worldData = new int[w, h];
        var rng = new System.Random(seed);
        
        for (int x = 0; x < w; x++)
        for (int y = 0; y < h; y++)
        {
            // Simple noise-based terrain
            float noise = Mathf.PerlinNoise(x * 0.1f + seed, y * 0.1f);
            worldData[x, y] = noise > 0.6f ? 2 : (noise > 0.3f ? 1 : 0);
            
            var pos = new Vector3Int(x, y, 0);
            groundLayer.SetTile(pos, tileSet[worldData[x, y]]);
            
            // Water tiles get collision
            if (worldData[x, y] == 2)
                collisionLayer.SetTile(pos, tileSet[3]); // collision tile
        }
    }
    
    public bool IsWalkable(Vector2Int tilePos)
    {
        if (tilePos.x < 0 || tilePos.x >= width) return false;
        if (tilePos.y < 0 || tilePos.y >= height) return false;
        return worldData[tilePos.x, tilePos.y] != 2; // not water
    }
    
    public Vector2Int WorldToTile(Vector2 worldPos)
    {
        var cellPos = groundLayer.WorldToCell(worldPos);
        return new Vector2Int(cellPos.x, cellPos.y);
    }
}
```

### 26.2 Python — Spatial Hash for Broad-Phase Collision

```python
from collections import defaultdict
from dataclasses import dataclass

@dataclass
class AABB:
    x: float
    y: float
    w: float
    h: float
    entity_id: int
    
    @property
    def min_x(self): return self.x
    @property
    def max_x(self): return self.x + self.w
    @property
    def min_y(self): return self.y
    @property
    def max_y(self): return self.y + self.h

class SpatialHash:
    def __init__(self, cell_size: float = 64.0):
        self.cell_size = cell_size
        self.cells: dict[tuple, list[AABB]] = defaultdict(list)
    
    def _get_cells(self, aabb: AABB) -> list[tuple]:
        """Get all cells this AABB overlaps."""
        min_cx = int(aabb.min_x // self.cell_size)
        max_cx = int(aabb.max_x // self.cell_size)
        min_cy = int(aabb.min_y // self.cell_size)
        max_cy = int(aabb.max_y // self.cell_size)
        return [(cx, cy) 
                for cx in range(min_cx, max_cx + 1)
                for cy in range(min_cy, max_cy + 1)]
    
    def clear(self):
        self.cells.clear()
    
    def insert(self, aabb: AABB):
        for cell in self._get_cells(aabb):
            self.cells[cell].append(aabb)
    
    def query(self, aabb: AABB) -> set[int]:
        """Return entity IDs that might collide with this AABB."""
        candidates = set()
        for cell in self._get_cells(aabb):
            for other in self.cells[cell]:
                if other.entity_id != aabb.entity_id:
                    if self._aabb_overlap(aabb, other):
                        candidates.add(other.entity_id)
        return candidates
    
    @staticmethod
    def _aabb_overlap(a: AABB, b: AABB) -> bool:
        return (a.max_x > b.min_x and a.min_x < b.max_x and
                a.max_y > b.min_y and a.min_y < b.max_y)

# Usage: rebuild every frame
spatial = SpatialHash(cell_size=64)
spatial.clear()
for entity in all_entities:
    spatial.insert(entity.aabb)

# Query for player collisions
colliding = spatial.query(player.aabb)
```

### 26.3 GDScript — Sprite Animation Controller

```gdscript
extends AnimatedSprite2D

enum State { IDLE, WALK, RUN, ATTACK, HURT }

var current_state: State = State.IDLE
var facing: Vector2 = Vector2.DOWN

# Direction suffixes for 4-directional sprites
const DIR_SUFFIX = {
    Vector2.DOWN: "_down",
    Vector2.UP: "_up",
    Vector2.LEFT: "_left",
    Vector2.RIGHT: "_right"
}

func update_animation(velocity: Vector2, new_state: State) -> void:
    # Update facing direction (only when moving)
    if velocity.length() > 0.1:
        # Snap to cardinal direction
        if abs(velocity.x) > abs(velocity.y):
            facing = Vector2.RIGHT if velocity.x > 0 else Vector2.LEFT
        else:
            facing = Vector2.DOWN if velocity.y > 0 else Vector2.UP
    
    current_state = new_state
    var anim_name = _get_anim_name()
    
    if animation != anim_name:
        play(anim_name)

func _get_anim_name() -> String:
    var suffix = DIR_SUFFIX.get(facing, "_down")
    match current_state:
        State.IDLE: return "idle" + suffix
        State.WALK: return "walk" + suffix
        State.RUN: return "run" + suffix
        State.ATTACK: return "attack" + suffix
        State.HURT: return "hurt" + suffix
    return "idle_down"
```

---

## 🧮 5. Worked Examples

### Example 26.3.1 — Implement Autotiling with Bitmask

**Problem:** Given a boolean grid (land/water), compute the correct tile variant for each water cell using 4-bit cardinal bitmask.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```python
def compute_autotile_index(grid: list[list[bool]], x: int, y: int) -> int:
    """
    Compute 4-bit bitmask for tile at (x,y).
    Bit 3 (8): North neighbor is same type
    Bit 2 (4): East neighbor is same type
    Bit 1 (2): South neighbor is same type
    Bit 0 (1): West neighbor is same type
    """
    rows, cols = len(grid), len(grid[0])
    tile_type = grid[y][x]
    
    def same(nx, ny):
        if 0 <= nx < cols and 0 <= ny < rows:
            return grid[ny][nx] == tile_type
        return False  # Out of bounds = different
    
    bitmask = 0
    if same(x, y - 1): bitmask |= 8   # North
    if same(x + 1, y): bitmask |= 4   # East
    if same(x, y + 1): bitmask |= 2   # South
    if same(x - 1, y): bitmask |= 1   # West
    
    return bitmask  # 0-15, maps to sprite sheet index

# Example: 5x5 grid with water (True) island
grid = [
    [False, False, False, False, False],
    [False, True,  True,  True,  False],
    [False, True,  True,  True,  False],
    [False, True,  True,  True,  False],
    [False, False, False, False, False],
]

# Center tile (2,2): all neighbors are water
assert compute_autotile_index(grid, 2, 2) == 15  # 1111 = full interior

# Top-left water (1,1): East and South are water, North and West are land
assert compute_autotile_index(grid, 1, 1) == 6   # 0110 = corner piece

# Top-center (2,1): East, South, West are water, North is land
assert compute_autotile_index(grid, 2, 1) == 7   # 0111 = top edge
```

The bitmask value (0–15) directly indexes into a 16-tile sprite strip in your tileset.

</details>

### Example 26.3.2 — Swept AABB Collision Detection

**Problem:** A bullet moves 500 pixels/frame. At 32px wide, it can pass through a 16px wall. Implement swept AABB to detect the collision.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```python
def swept_aabb(mover: AABB, vel: tuple, static: AABB) -> tuple[float, tuple]:
    """
    Returns (time_of_impact, normal) for moving AABB vs static AABB.
    time_of_impact in [0, 1] means collision this frame.
    Returns (1.0, (0,0)) if no collision.
    """
    vx, vy = vel
    
    # Compute entry and exit distances
    if vx > 0:
        x_entry = static.min_x - mover.max_x
        x_exit = static.max_x - mover.min_x
    else:
        x_entry = static.max_x - mover.min_x
        x_exit = static.min_x - mover.max_x
    
    if vy > 0:
        y_entry = static.min_y - mover.max_y
        y_exit = static.max_y - mover.min_y
    else:
        y_entry = static.max_y - mover.min_y
        y_exit = static.min_y - mover.max_y
    
    # Compute entry and exit times
    if vx == 0:
        tx_entry = float('-inf')
        tx_exit = float('inf')
    else:
        tx_entry = x_entry / vx
        tx_exit = x_exit / vx
    
    if vy == 0:
        ty_entry = float('-inf')
        ty_exit = float('inf')
    else:
        ty_entry = y_entry / vy
        ty_exit = y_exit / vy
    
    # Find the latest entry and earliest exit
    t_entry = max(tx_entry, ty_entry)
    t_exit = min(tx_exit, ty_exit)
    
    # No collision conditions
    if t_entry > t_exit or t_entry > 1.0 or t_entry < 0.0:
        return (1.0, (0, 0))
    
    # Determine collision normal
    if tx_entry > ty_entry:
        normal = (-1, 0) if vx > 0 else (1, 0)
    else:
        normal = (0, -1) if vy > 0 else (0, 1)
    
    return (t_entry, normal)

# Test: bullet at (0, 100) moving right at 500px/frame
# Wall at x=200, 16px wide
bullet = AABB(0, 100, 32, 8, entity_id=1)
wall = AABB(200, 0, 16, 300, entity_id=2)
velocity = (500, 0)

t, normal = swept_aabb(bullet, velocity, wall)
# t = (200 - 32) / 500 = 0.336 → collision at 33.6% through the frame
# normal = (-1, 0) → hit from the left
print(f"Impact at t={t:.3f}, normal={normal}")

# Resolve: move bullet to contact point
bullet.x += velocity[0] * t
# Remaining time: slide along surface or stop
```

Without swept collision, the bullet would teleport from x=0 to x=500, completely skipping the 16px wall.

</details>

### Example 26.3.3 — Camera System with Bounds and Smoothing

**Problem:** Implement a 2D camera that smoothly follows the player, clamps to world bounds, and supports screen shake.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```csharp
public class Camera2DController : MonoBehaviour
{
    [SerializeField] private Transform target;
    [SerializeField] private float smoothSpeed = 5f;
    [SerializeField] private Vector2 offset = new(0, 1);
    
    // World bounds (set from tilemap size)
    [SerializeField] private Rect worldBounds = new(0, 0, 100, 75);
    
    // Screen shake
    private float shakeIntensity;
    private float shakeDuration;
    private float shakeTimer;
    
    private Camera cam;
    private float halfHeight, halfWidth;
    
    void Start()
    {
        cam = GetComponent<Camera>();
        halfHeight = cam.orthographicSize;
        halfWidth = halfHeight * cam.aspect;
    }
    
    void LateUpdate()
    {
        if (!target) return;
        
        // Smooth follow
        Vector2 desiredPos = (Vector2)target.position + offset;
        Vector2 smoothed = Vector2.Lerp(
            transform.position, desiredPos, smoothSpeed * Time.deltaTime);
        
        // Clamp to world bounds
        float clampedX = Mathf.Clamp(smoothed.x, 
            worldBounds.xMin + halfWidth, worldBounds.xMax - halfWidth);
        float clampedY = Mathf.Clamp(smoothed.y, 
            worldBounds.yMin + halfHeight, worldBounds.yMax - halfHeight);
        
        Vector3 finalPos = new(clampedX, clampedY, transform.position.z);
        
        // Apply screen shake
        if (shakeTimer > 0)
        {
            shakeTimer -= Time.deltaTime;
            float decay = shakeTimer / shakeDuration;
            Vector2 shakeOffset = Random.insideUnitCircle * shakeIntensity * decay;
            finalPos += (Vector3)shakeOffset;
        }
        
        transform.position = finalPos;
    }
    
    public void Shake(float intensity, float duration)
    {
        shakeIntensity = intensity;
        shakeDuration = duration;
        shakeTimer = duration;
    }
}
```

</details>

---

## ⚠️ 6. Gotchas & Anti-Patterns

### ❌ Anti-Pattern: One Giant Tilemap

Don't put everything on one layer. Separate ground, objects, and collision into distinct tilemaps. This enables independent Z-ordering, selective collision, and efficient culling.

### ❌ Anti-Pattern: Per-Pixel Collision for Everything

Pixel-perfect collision is expensive ($O(w \times h)$ per pair). Use it only for final hit confirmation after AABB broad-phase passes. Most games use simplified collision shapes (circles, capsules, boxes).

### ❌ Anti-Pattern: Hardcoded Tile Size

```csharp
// BAD: magic numbers everywhere
int tileX = (int)(worldX / 16);

// GOOD: configurable constant
public const int TILE_SIZE = 16;
int tileX = (int)(worldX / TILE_SIZE);
```

### ❌ Anti-Pattern: Rendering Off-Screen Tiles

Only render tiles visible to the camera. For a 1920×1080 screen with 16px tiles, that's 120×68 = 8,160 tiles. A 1000×1000 world has 1,000,000 tiles — rendering all of them wastes 99% of GPU time.

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- **Previous:** [26.2 - Gameplay Programming - Input, State, AI](26.2---Gameplay-Programming---Input,-State,-AI)
- **Next:** [26.4 - 3D Game Patterns - Transforms, Animation, Physics](26.4---3D-Game-Patterns---Transforms,-Animation,-Physics)
- **Physics math:** [26.4 - Classical Mechanics & Dynamical Systems](26.4---Classical-Mechanics-&-Dynamical-Systems) (math track) — Newtonian mechanics
- **Spatial data structures:** [08.13 - Algorithms & Data Structures in Python](08.13---Algorithms-&-Data-Structures-in-Python) — hash maps, trees

### External Resources
- **Celeste & TowerFall Physics** — Maddy Thorson's devlog on 2D platformer physics
- **Sebastian Lague: "Procedural Landmass Generation"** — noise-based terrain
- **Brackeys: "2D Movement in Unity"** — practical Unity tilemap tutorials
- **Red Blob Games** (redblobgames.com) — interactive articles on grids, pathfinding, hex maps
- **Kenney.nl** — free tileset assets for prototyping

### Practice
- `_practice/scripts/4.3_tilemap_collision.py` — spatial hash + swept AABB implementation



---

## 🔬 8. Advanced Topics — Tilemap Collision, Sprite Atlasing, 2D Lighting & Pixel-Perfect Cameras

### 8.1 — Tilemap Collision Detection Systems

Tilemap collision is fundamentally different from general-purpose physics. Because tiles are axis-aligned and uniformly sized, we can exploit this structure for O(1) lookups and swept resolution.

#### Direct Tile Lookup (No Broadphase Needed)

```csharp
public class TilemapCollider
{
    private readonly int[,] tileData;  // 0 = empty, 1+ = solid tile type
    private readonly int tileSize;      // Pixels per tile (e.g., 16)
    private readonly int mapWidth, mapHeight;
    
    // Convert world position to tile coordinate
    public (int x, int y) WorldToTile(float worldX, float worldY)
    {
        return (
            Mathf.FloorToInt(worldX / tileSize),
            Mathf.FloorToInt(worldY / tileSize)
        );
    }
    
    // Check if a tile is solid
    public bool IsSolid(int tileX, int tileY)
    {
        if (tileX < 0 || tileX >= mapWidth || tileY < 0 || tileY >= mapHeight)
            return true; // Out of bounds = solid (prevents falling off map)
        return tileData[tileX, tileY] > 0;
    }
    
    // Get all tiles overlapping an AABB
    public List<(int x, int y)> GetOverlappingTiles(Rect aabb)
    {
        var tiles = new List<(int, int)>();
        
        int minTX = Mathf.FloorToInt(aabb.xMin / tileSize);
        int maxTX = Mathf.FloorToInt(aabb.xMax / tileSize);
        int minTY = Mathf.FloorToInt(aabb.yMin / tileSize);
        int maxTY = Mathf.FloorToInt(aabb.yMax / tileSize);
        
        for (int ty = minTY; ty <= maxTY; ty++)
            for (int tx = minTX; tx <= maxTX; tx++)
                if (IsSolid(tx, ty))
                    tiles.Add((tx, ty));
        
        return tiles;
    }
}
```

#### Swept AABB vs. Tilemap (Continuous Collision Detection)

Discrete collision (check overlap after moving) causes tunneling at high speeds. Swept collision finds the exact time of impact:

```csharp
public struct SweptResult
{
    public float time;        // 0..1, fraction of movement before collision
    public Vector2 normal;    // Surface normal at collision point
}

public class SweptTilemapCollision
{
    private TilemapCollider tilemap;
    
    // Swept AABB against a single tile (treated as static AABB)
    public SweptResult SweptAABB(Rect movingBox, Vector2 velocity, Rect staticBox)
    {
        // Find entry and exit times for each axis
        float xInvEntry, yInvEntry, xInvExit, yInvExit;
        
        if (velocity.x > 0)
        {
            xInvEntry = staticBox.xMin - movingBox.xMax;
            xInvExit = staticBox.xMax - movingBox.xMin;
        }
        else
        {
            xInvEntry = staticBox.xMax - movingBox.xMin;
            xInvExit = staticBox.xMin - movingBox.xMax;
        }
        
        if (velocity.y > 0)
        {
            yInvEntry = staticBox.yMin - movingBox.yMax;
            yInvExit = staticBox.yMax - movingBox.yMin;
        }
        else
        {
            yInvEntry = staticBox.yMax - movingBox.yMin;
            yInvExit = staticBox.yMin - movingBox.yMax;
        }
        
        // Convert to time
        float xEntry, yEntry, xExit, yExit;
        
        if (velocity.x == 0) { xEntry = float.NegativeInfinity; xExit = float.PositiveInfinity; }
        else { xEntry = xInvEntry / velocity.x; xExit = xInvExit / velocity.x; }
        
        if (velocity.y == 0) { yEntry = float.NegativeInfinity; yExit = float.PositiveInfinity; }
        else { yEntry = yInvEntry / velocity.y; yExit = yInvExit / velocity.y; }
        
        float entryTime = Mathf.Max(xEntry, yEntry);
        float exitTime = Mathf.Min(xExit, yExit);
        
        // No collision conditions
        if (entryTime > exitTime || (xEntry < 0 && yEntry < 0) || xEntry > 1 || yEntry > 1)
            return new SweptResult { time = 1.0f, normal = Vector2.zero };
        
        // Determine collision normal
        Vector2 normal;
        if (xEntry > yEntry)
            normal = velocity.x < 0 ? Vector2.right : Vector2.left;
        else
            normal = velocity.y < 0 ? Vector2.up : Vector2.down;
        
        return new SweptResult { time = entryTime, normal = normal };
    }
    
    // Full tilemap sweep: test against all potentially overlapping tiles
    public SweptResult SweepAgainstTilemap(Rect playerBox, Vector2 velocity)
    {
        // Expand search area by velocity to find all candidate tiles
        Rect broadphase = new Rect(
            Mathf.Min(playerBox.x, playerBox.x + velocity.x),
            Mathf.Min(playerBox.y, playerBox.y + velocity.y),
            playerBox.width + Mathf.Abs(velocity.x),
            playerBox.height + Mathf.Abs(velocity.y)
        );
        
        var candidates = tilemap.GetOverlappingTiles(broadphase);
        
        SweptResult nearest = new SweptResult { time = 1.0f, normal = Vector2.zero };
        
        foreach (var (tx, ty) in candidates)
        {
            Rect tileRect = new Rect(
                tx * tilemap.tileSize, ty * tilemap.tileSize,
                tilemap.tileSize, tilemap.tileSize
            );
            
            SweptResult result = SweptAABB(playerBox, velocity, tileRect);
            if (result.time < nearest.time)
                nearest = result;
        }
        
        return nearest;
    }
    
    // Resolve movement with sliding
    public Vector2 MoveAndSlide(Rect playerBox, Vector2 velocity, int maxIterations = 3)
    {
        Vector2 totalMovement = Vector2.zero;
        Vector2 remainingVel = velocity;
        
        for (int i = 0; i < maxIterations && remainingVel.sqrMagnitude > 0.0001f; i++)
        {
            SweptResult hit = SweepAgainstTilemap(playerBox, remainingVel);
            
            // Move to collision point
            Vector2 movement = remainingVel * hit.time;
            totalMovement += movement;
            playerBox.position += movement;
            
            if (hit.time >= 1.0f)
                break; // No collision, full movement applied
            
            // Slide: remove velocity component along collision normal
            float remainingTime = 1.0f - hit.time;
            float dot = Vector2.Dot(remainingVel, hit.normal);
            remainingVel = (remainingVel - hit.normal * dot) * remainingTime;
        }
        
        return totalMovement;
    }
}
```

#### One-Way Platforms (Drop-Through)

```csharp
// One-way platforms only collide when player is moving downward
// and player's feet are above the platform top
public bool ShouldCollideWithPlatform(Rect playerBox, Vector2 velocity, Rect platformBox)
{
    // Only block if moving down
    if (velocity.y >= 0) return false;
    
    // Only block if player's bottom is above platform's top (within tolerance)
    float tolerance = 2f; // pixels
    if (playerBox.yMin < platformBox.yMax - tolerance) return false;
    
    // Allow drop-through if player presses down
    if (Input.GetKey(KeyCode.S) || Input.GetKey(KeyCode.DownArrow)) return false;
    
    return true;
}
```

---

### 8.2 — Sprite Atlasing & Texture Packing

Sprite atlasing combines multiple small textures into one large texture to minimize draw calls and GPU state changes.

#### Why Atlas?

Each unique texture requires a separate draw call (or at minimum a texture bind). For a 2D game with 200 unique sprites:
- **Without atlas:** 200 draw calls per frame (GPU state thrashing)
- **With atlas:** 1-4 draw calls (batch all sprites using same atlas)

#### Packing Algorithms

**MaxRects Algorithm** (industry standard, used by TexturePacker, Unity):

```python
class MaxRectsAtlasPacker:
    """MaxRects bin packing algorithm for sprite atlasing."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Start with one free rectangle covering the entire atlas
        self.free_rects: list[Rect] = [Rect(0, 0, width, height)]
        self.used_rects: list[Rect] = []
    
    def insert(self, sprite_width: int, sprite_height: int) -> Rect | None:
        """Find best position for a sprite using Best Short Side Fit."""
        best_rect = None
        best_short_side = float('inf')
        best_long_side = float('inf')
        
        for free in self.free_rects:
            # Try normal orientation
            if sprite_width <= free.w and sprite_height <= free.h:
                leftover_x = free.w - sprite_width
                leftover_y = free.h - sprite_height
                short_side = min(leftover_x, leftover_y)
                long_side = max(leftover_x, leftover_y)
                
                if short_side < best_short_side or \
                   (short_side == best_short_side and long_side < best_long_side):
                    best_rect = Rect(free.x, free.y, sprite_width, sprite_height)
                    best_short_side = short_side
                    best_long_side = long_side
            
            # Try rotated (90 degrees)
            if sprite_height <= free.w and sprite_width <= free.h:
                leftover_x = free.w - sprite_height
                leftover_y = free.h - sprite_width
                short_side = min(leftover_x, leftover_y)
                long_side = max(leftover_x, leftover_y)
                
                if short_side < best_short_side or \
                   (short_side == best_short_side and long_side < best_long_side):
                    best_rect = Rect(free.x, free.y, sprite_height, sprite_width)
                    best_rect.rotated = True
                    best_short_side = short_side
                    best_long_side = long_side
        
        if best_rect is None:
            return None  # Doesn't fit
        
        # Split free rectangles around the placed sprite
        self._split_free_rects(best_rect)
        self.used_rects.append(best_rect)
        return best_rect
    
    def _split_free_rects(self, placed: Rect):
        """Split overlapping free rects and remove fully covered ones."""
        new_free = []
        
        for free in self.free_rects:
            if not self._intersects(free, placed):
                new_free.append(free)
                continue
            
            # Generate up to 4 new free rects from the split
            # Left remainder
            if placed.x > free.x:
                new_free.append(Rect(free.x, free.y, placed.x - free.x, free.h))
            # Right remainder
            if placed.x + placed.w < free.x + free.w:
                new_free.append(Rect(placed.x + placed.w, free.y,
                                     (free.x + free.w) - (placed.x + placed.w), free.h))
            # Bottom remainder
            if placed.y > free.y:
                new_free.append(Rect(free.x, free.y, free.w, placed.y - free.y))
            # Top remainder
            if placed.y + placed.h < free.y + free.h:
                new_free.append(Rect(free.x, placed.y + placed.h,
                                     free.w, (free.y + free.h) - (placed.y + placed.h)))
        
        self.free_rects = new_free
        self._prune_contained_rects()
```

#### UV Coordinate Calculation

After packing, each sprite's UV coordinates map into the atlas:

```csharp
public struct AtlasSprite
{
    public Rect pixelRect;      // Position in atlas (pixels)
    public Vector2 atlasSize;   // Total atlas dimensions
    
    // Convert pixel rect to UV coordinates (0..1)
    public Vector4 GetUVs()
    {
        return new Vector4(
            pixelRect.x / atlasSize.x,           // u_min
            pixelRect.y / atlasSize.y,           // v_min
            (pixelRect.x + pixelRect.width) / atlasSize.x,   // u_max
            (pixelRect.y + pixelRect.height) / atlasSize.y   // v_max
        );
    }
}
```

#### Padding & Bleeding

Without padding between sprites, texture filtering (bilinear/trilinear) samples neighboring sprites at edges, causing visible seams. Solutions:
- **1-2px transparent padding** between sprites
- **Edge extrusion:** Duplicate the outermost pixel row outward (prevents color bleeding)
- **Half-texel inset:** Shrink UVs by 0.5/atlasSize on each edge

---

### 8.3 — 2D Lighting with Normal-Mapped Sprites

Normal maps encode surface direction per-pixel, enabling dynamic lighting on flat 2D sprites. Each pixel's RGB channels encode the normal vector:

- R = X component (left/right)
- G = Y component (up/down)  
- B = Z component (toward camera, usually dominant)

```csharp
// Unity Shader Graph equivalent in code (URP 2D Renderer)
// This is the core lighting calculation for normal-mapped 2D sprites
Shader "Custom/2D_NormalMapped"
{
    Properties
    {
        _MainTex ("Sprite", 2D) = "white" {}
        _NormalMap ("Normal Map", 2D) = "bump" {}
    }
    
    // Vertex/Fragment shader for 2D normal-mapped lighting
    // (Simplified — production would use Unity's 2D Light system)
}
```

```csharp
// Setting up 2D lights with normal maps in Unity URP
public class Setup2DLighting : MonoBehaviour
{
    void ConfigureSprite()
    {
        var renderer = GetComponent<SpriteRenderer>();
        
        // Material must use a 2D lit shader
        renderer.material = new Material(Shader.Find("Universal Render Pipeline/2D/Sprite-Lit-Default"));
        
        // Assign normal map to the sprite's material
        Texture2D normalMap = Resources.Load<Texture2D>("Sprites/player_normal");
        renderer.material.SetTexture("_NormalMap", normalMap);
    }
}
```

**Generating Normal Maps for 2D Art:**
1. **Hand-painted:** Artists paint normals directly (tools: Sprite Illuminator, Laigter)
2. **Auto-generated:** Derive from height/depth information (emboss filter approach)
3. **3D render:** Render a 3D model's normal pass, use as 2D sprite normal map

**Light Types for 2D:**
- **Point Light 2D:** Radial falloff, good for torches, explosions
- **Spot Light 2D:** Cone-shaped, good for flashlights
- **Global Light 2D:** Ambient fill, day/night cycles
- **Freeform Light 2D:** Custom polygon shape (Unity-specific)

---

### 8.4 — Pixel-Perfect Camera Systems

Pixel art requires exact integer positioning to avoid sub-pixel rendering artifacts (shimmering, uneven pixel sizes).

```csharp
public class PixelPerfectCamera : MonoBehaviour
{
    [SerializeField] private int referenceResolutionX = 320;  // Game's native resolution
    [SerializeField] private int referenceResolutionY = 180;
    [SerializeField] private int pixelsPerUnit = 16;          // Must match sprite import settings
    
    private Camera cam;
    private int scaleFactor;
    
    void Start()
    {
        cam = GetComponent<Camera>();
        CalculateOrthoSize();
    }
    
    void CalculateOrthoSize()
    {
        int screenHeight = Screen.height;
        int screenWidth = Screen.width;
        
        // Find largest integer scale that fits the screen
        int scaleX = screenWidth / referenceResolutionX;
        int scaleY = screenHeight / referenceResolutionY;
        scaleFactor = Mathf.Max(1, Mathf.Min(scaleX, scaleY));
        
        // Set orthographic size so that one game pixel = scaleFactor screen pixels
        // orthoSize = (screenHeight / scaleFactor) / (2 * pixelsPerUnit)
        cam.orthographicSize = (screenHeight / (float)scaleFactor) / (2f * pixelsPerUnit);
    }
    
    void LateUpdate()
    {
        // Snap camera position to pixel grid
        Vector3 pos = transform.position;
        float pixelSize = 1f / pixelsPerUnit;
        
        pos.x = Mathf.Round(pos.x / pixelSize) * pixelSize;
        pos.y = Mathf.Round(pos.y / pixelSize) * pixelSize;
        
        transform.position = pos;
    }
    
    // For sub-pixel smooth scrolling: render to low-res RT, then upscale
    private RenderTexture lowResRT;
    
    void SetupSubPixelSmoothing()
    {
        lowResRT = new RenderTexture(referenceResolutionX, referenceResolutionY, 0)
        {
            filterMode = FilterMode.Point,  // No bilinear filtering!
            autoGenerateMips = false
        };
        cam.targetTexture = lowResRT;
        
        // A second camera renders the RT to screen at integer scale
        // This allows smooth camera movement without pixel shimmering
    }
}
```

**Common Pixel-Perfect Pitfalls:**
1. **Non-integer sprite positions:** Sprites at (10.5, 3.7) render with uneven pixels
2. **Wrong filter mode:** Bilinear filtering blurs pixel art — always use Point filtering
3. **Rotation:** Rotating pixel art by non-90° angles destroys the pixel grid
4. **Non-integer camera zoom:** Zoom must be exact integer multiples of native resolution
5. **UI scaling:** UI elements must also snap to the pixel grid

---

## 📎 9. Appendix — Mathematical Foundations

### Appendix 9.A — Separating Axis Theorem (SAT) Collision Algorithm

The **Separating Axis Theorem** states: two convex shapes do NOT overlap if and only if there exists an axis along which their projections do not overlap.

**Formal Statement:**

Two convex sets $A$ and $B$ in $\mathbb{R}^n$ are disjoint if and only if there exists a hyperplane $H$ separating them:

$$
\exists \hat{n}, d : \quad \forall a \in A,\ a \cdot \hat{n} \leq d \quad \text{and} \quad \forall b \in B,\ b \cdot \hat{n} \geq d
$$

For 2D convex polygons, the potential separating axes are the **edge normals** of both polygons. For two polygons with $m$ and $n$ edges respectively, we test $m + n$ axes.

**Algorithm:**

```python
def sat_collision(poly_a: list[Vec2], poly_b: list[Vec2]) -> tuple[bool, Vec2, float]:
    """
    SAT collision test between two convex polygons.
    Returns (colliding, mtv_axis, mtv_depth) where MTV = Minimum Translation Vector.
    """
    min_overlap = float('inf')
    mtv_axis = Vec2(0, 0)
    
    # Test all edge normals from both polygons
    for polygon in [poly_a, poly_b]:
        for i in range(len(polygon)):
            # Edge vector
            edge = polygon[(i + 1) % len(polygon)] - polygon[i]
            
            # Normal (perpendicular) — the potential separating axis
            axis = Vec2(-edge.y, edge.x).normalized()
            
            # Project both polygons onto this axis
            min_a, max_a = project_polygon(poly_a, axis)
            min_b, max_b = project_polygon(poly_b, axis)
            
            # Check for gap (separation)
            overlap = min(max_a, max_b) - max(min_a, min_b)
            
            if overlap <= 0:
                return (False, Vec2(0, 0), 0)  # Separating axis found — no collision
            
            # Track minimum overlap for MTV
            if overlap < min_overlap:
                min_overlap = overlap
                mtv_axis = axis
    
    # Ensure MTV pushes A away from B
    center_diff = centroid(poly_b) - centroid(poly_a)
    if center_diff.dot(mtv_axis) < 0:
        mtv_axis = -mtv_axis
    
    return (True, mtv_axis, min_overlap)


def project_polygon(polygon: list[Vec2], axis: Vec2) -> tuple[float, float]:
    """Project all vertices onto axis, return min and max scalar projections."""
    projections = [v.dot(axis) for v in polygon]
    return min(projections), max(projections)
```

**Complexity:** $O(m + n)$ axes to test, each requiring $O(m + n)$ projections. Total: $O((m+n)^2)$.

For AABBs (axis-aligned bounding boxes), SAT reduces to 2 axis tests (x and y), giving $O(1)$ collision detection — which is why AABB checks are used as broadphase.

**SAT for Circles:**

Circles have infinite edge normals, but only one axis matters: the axis from the circle center to the nearest vertex of the polygon.

$$
\hat{n}_{circle} = \frac{v_{nearest} - c_{circle}}{|v_{nearest} - c_{circle}|}
$$

Test this axis plus all polygon edge normals.

---

### Appendix 9.B — Quadtree vs. Uniform Grid: Spatial Index Tradeoffs

Spatial indexing accelerates collision broadphase by quickly finding nearby objects without testing all pairs ($O(n^2)$).

#### Uniform Grid

Divide the world into fixed-size cells. Each cell stores a list of objects overlapping it.

```python
class UniformGrid:
    def __init__(self, world_width: float, world_height: float, cell_size: float):
        self.cell_size = cell_size
        self.cols = int(world_width / cell_size) + 1
        self.rows = int(world_height / cell_size) + 1
        self.cells: list[list[int]] = [[] for _ in range(self.cols * self.rows)]
    
    def _cell_index(self, x: float, y: float) -> int:
        col = int(x / self.cell_size)
        row = int(y / self.cell_size)
        return row * self.cols + col
    
    def insert(self, obj_id: int, aabb: Rect):
        """Insert object into all cells it overlaps."""
        min_col = int(aabb.x / self.cell_size)
        max_col = int((aabb.x + aabb.w) / self.cell_size)
        min_row = int(aabb.y / self.cell_size)
        max_row = int((aabb.y + aabb.h) / self.cell_size)
        
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                idx = row * self.cols + col
                if 0 <= idx < len(self.cells):
                    self.cells[idx].append(obj_id)
    
    def query(self, aabb: Rect) -> set[int]:
        """Find all objects potentially overlapping the query AABB."""
        results = set()
        min_col = int(aabb.x / self.cell_size)
        max_col = int((aabb.x + aabb.w) / self.cell_size)
        min_row = int(aabb.y / self.cell_size)
        max_row = int((aabb.y + aabb.h) / self.cell_size)
        
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                idx = row * self.cols + col
                if 0 <= idx < len(self.cells):
                    results.update(self.cells[idx])
        
        return results
    
    def clear(self):
        """Clear all cells (call each frame before re-inserting)."""
        for cell in self.cells:
            cell.clear()
```

#### Quadtree

Recursively subdivides space into 4 quadrants. Only subdivides when a node exceeds a capacity threshold.

```python
class QuadTree:
    MAX_OBJECTS = 8
    MAX_DEPTH = 6
    
    def __init__(self, bounds: Rect, depth: int = 0):
        self.bounds = bounds
        self.depth = depth
        self.objects: list[tuple[int, Rect]] = []  # (id, aabb)
        self.children: list[QuadTree] | None = None  # NW, NE, SW, SE
    
    def _subdivide(self):
        hw = self.bounds.w / 2
        hh = self.bounds.h / 2
        x, y = self.bounds.x, self.bounds.y
        d = self.depth + 1
        
        self.children = [
            QuadTree(Rect(x, y + hh, hw, hh), d),      # NW
            QuadTree(Rect(x + hw, y + hh, hw, hh), d),  # NE
            QuadTree(Rect(x, y, hw, hh), d),             # SW
            QuadTree(Rect(x + hw, y, hw, hh), d),        # SE
        ]
    
    def insert(self, obj_id: int, aabb: Rect):
        if self.children is not None:
            for child in self.children:
                if child.bounds.intersects(aabb):
                    child.insert(obj_id, aabb)
            return
        
        self.objects.append((obj_id, aabb))
        
        if len(self.objects) > self.MAX_OBJECTS and self.depth < self.MAX_DEPTH:
            self._subdivide()
            for oid, oaabb in self.objects:
                for child in self.children:
                    if child.bounds.intersects(oaabb):
                        child.insert(oid, oaabb)
            self.objects.clear()
    
    def query(self, area: Rect) -> set[int]:
        results = set()
        
        if not self.bounds.intersects(area):
            return results
        
        for obj_id, aabb in self.objects:
            if area.intersects(aabb):
                results.add(obj_id)
        
        if self.children is not None:
            for child in self.children:
                results.update(child.query(area))
        
        return results
```

#### Comparison Table

| Criterion | Uniform Grid | Quadtree |
|-----------|-------------|----------|
| Insert cost | O(1) | O(log n) amortized |
| Query cost | O(1) per cell | O(log n + k) |
| Memory | Fixed (cells × pointer) | Dynamic (grows with objects) |
| Best distribution | Uniform density | Non-uniform (clustered) |
| Worst case | Sparse world wastes memory | Deep recursion with overlapping objects |
| Rebuild cost | O(n) clear + reinsert | O(n log n) rebuild |
| Implementation | Simple | Moderate |
| Used by | Box2D, most 2D engines | Large open worlds, RTS games |

**Rule of Thumb:**
- **Uniform grid** when objects are roughly evenly distributed and world size is bounded (platformers, shooters, puzzle games)
- **Quadtree** when objects cluster heavily in certain areas (RTS with armies, open-world with cities)
- **Spatial hash** (variant of grid with hash map instead of array) when world is unbounded or very sparse

**Cell Size Selection for Uniform Grid:**

The optimal cell size is approximately the size of the largest common object:

$$
\text{cell\_size} \approx 2 \times \text{max\_object\_radius}
$$

Too small → objects span many cells (expensive insert). Too large → many objects per cell (expensive query). The sweet spot minimizes total work:

$$
\text{total\_work} = n \cdot \text{cells\_per\_object} + \text{queries} \cdot \text{objects\_per\_cell}
$$

---

