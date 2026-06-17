---
title: "26.2 — Gameplay Programming: Input, State, AI"
subject: "Game Dev"
catalog: advanced
audience_tier: higher-education
chapter: "26.2"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 26.2 — Gameplay Programming: Input, State, AI

> *"A game is a series of interesting decisions."* — Sid Meier

Gameplay programming is where engine architecture meets player experience. This chapter covers the three pillars of interactive systems: how you read player intent (input), how you manage complex entity behavior (state machines), and how you create the illusion of intelligence (game AI). These patterns apply whether you're building a Stardew Valley NPC schedule, a VR combat system, or a multiplayer arena.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Implement an **input abstraction layer** that decouples hardware from game actions.
2. Design and implement **Finite State Machines (FSMs)** for player and NPC behavior.
3. Implement **Hierarchical State Machines (HSMs)** for complex character controllers.
4. Build a **Behavior Tree** with selector, sequence, and decorator nodes.
5. Implement **A* pathfinding** with navigation meshes.
6. Design a **Utility AI** system for NPC decision-making.
7. Apply the **Command pattern** for input replay, undo, and network synchronization.

---

## 🖼️ Visual Anchor — FSM vs Behavior Tree

![gamedev__4.2-fig1](gamedev__4.2-fig1.svg)

---

## 📚 1. Concepts & Definitions

### Definition 26.2.1 — Input Action Mapping

An **input action** is a semantic game event (Jump, Attack, MoveRight) decoupled from the physical input that triggers it. This abstraction enables:
- Rebindable controls
- Multiple input devices (keyboard, gamepad, VR controller)
- Input replay for debugging and networking
- Accessibility remapping

### Definition 26.2.2 — Finite State Machine (FSM)

A **Finite State Machine** is a computational model with:
- A finite set of **states** $S = \{s_1, s_2, \ldots, s_n\}$
- A set of **transitions** $T \subseteq S \times \text{Condition} \times S$
- Exactly **one active state** at any time
- **Entry/Exit actions** executed on state transitions

Formally: $\text{FSM} = (S, s_0, T, A_{\text{enter}}, A_{\text{exit}}, A_{\text{update}})$

### Definition 26.2.3 — Behavior Tree (BT)

A **Behavior Tree** is a directed acyclic graph (tree) that models decision-making through composable nodes:

| Node Type | Symbol | Behavior |
|-----------|--------|----------|
| **Selector** | `?` | Try children left-to-right, return first SUCCESS |
| **Sequence** | `→` | Run children left-to-right, fail on first FAILURE |
| **Decorator** | `◇` | Modify child result (invert, repeat, cooldown) |
| **Leaf/Action** | `□` | Execute concrete behavior, return SUCCESS/FAILURE/RUNNING |
| **Condition** | `◯` | Check world state, return SUCCESS/FAILURE |

Each tick, the tree is evaluated from root. Nodes return one of: `SUCCESS`, `FAILURE`, `RUNNING`.

### Definition 26.2.4 — A* Pathfinding

**A*** is a best-first graph search algorithm that finds the shortest path from start to goal using a heuristic:

$$
f(n) = g(n) + h(n)
$$

Where:
- $g(n)$ = actual cost from start to node $n$
- $h(n)$ = heuristic estimate from $n$ to goal (must be admissible: $h(n) \leq$ true cost)
- $f(n)$ = estimated total cost through $n$

### Definition 26.2.5 — Command Pattern

The **Command pattern** encapsulates an action as an object, enabling:
- **Undo/Redo:** Each command stores enough state to reverse itself
- **Input replay:** Record command stream, replay for deterministic reproduction
- **Network sync:** Serialize commands, send to server/peers
- **AI:** AI systems emit the same command objects as player input

---

## 🧩 2. Mental Models / Architecture

### Model 2.1 — Input Pipeline

```
Hardware → OS Events → Raw Input Layer → Action Mapping → Game Systems
                                              ↓
                                    Input Buffer (for replay/network)
```

**Key insight:** The game logic layer never sees "keyboard key W pressed." It sees "MoveForward action with magnitude 1.0." This makes the same code work for keyboard, gamepad analog stick, and VR thumbstick.

### Model 2.2 — State Machine Hierarchy

For a complex character controller, nest FSMs:

```
TopLevel FSM:
├── Grounded (sub-FSM)
│   ├── Idle
│   ├── Walk
│   ├── Run
│   └── Crouch
├── Airborne (sub-FSM)
│   ├── Jump
│   ├── Fall
│   └── WallSlide
└── Combat (sub-FSM)
    ├── Attack
    ├── Block
    └── Dodge
```

Each sub-FSM handles its own transitions internally. The top-level FSM handles transitions between major behavioral modes.

### Model 2.3 — AI Decision Hierarchy

```
Strategic (what to do)     → Utility AI / Goal-Oriented Action Planning
Tactical (how to do it)    → Behavior Trees
Reactive (moment-to-moment) → Steering Behaviors / FSM
```

---

## 🔑 3. Mechanics

### Mechanic 3.1 — Input Buffering

Fighting games and action games use **input buffering** to make controls feel responsive:

```
Frame:  1  2  3  4  5  6  7  8
Input:  .  .  J  .  .  .  .  .    (J = Jump pressed on frame 3)
Buffer: .  .  J  J  J  J  .  .    (buffer window = 4 frames)
State:  attack_recovery...........  (can't jump until frame 5)
Result: .  .  .  .  J! .  .  .    (buffered jump executes on frame 5)
```

Without buffering, the player must press Jump on the exact frame they become actionable. With a 4-frame buffer, they have a ~67ms window (at 60 FPS).

### Mechanic 3.2 — Coyote Time

**Coyote time** gives the player a grace period to jump after leaving a platform edge:

```
Platform edge:  frame 10
Coyote window:  frames 10-16 (6 frames = 100ms)
Player presses jump on frame 13: ALLOWED (still "grounded" for coyote purposes)
```

This makes platforming feel fair without the player noticing the assist.

### Mechanic 3.3 — Navigation Mesh (NavMesh)

A **NavMesh** is a simplified polygon mesh representing walkable surfaces:

1. **Bake:** Generate convex polygons from level geometry (automated in Unity/Unreal)
2. **Query:** A* pathfinding on the polygon graph (nodes = polygon centers, edges = shared edges)
3. **Funnel:** String-pulling algorithm smooths the path through polygon portals
4. **Steering:** Agent follows smoothed path with local avoidance (RVO)

---

## 💻 4. Code Patterns & Examples

### 26.1 C# — Generic FSM Framework

```csharp
public abstract class State<T> where T : class
{
    protected T owner;
    protected StateMachine<T> machine;
    
    public void Init(T owner, StateMachine<T> machine)
    {
        this.owner = owner;
        this.machine = machine;
    }
    
    public virtual void Enter() { }
    public virtual void Update(float dt) { }
    public virtual void FixedUpdate(float fixedDt) { }
    public virtual void Exit() { }
}

public class StateMachine<T> where T : class
{
    public State<T> CurrentState { get; private set; }
    private T owner;
    
    public StateMachine(T owner, State<T> initialState)
    {
        this.owner = owner;
        TransitionTo(initialState);
    }
    
    public void TransitionTo(State<T> newState)
    {
        CurrentState?.Exit();
        CurrentState = newState;
        CurrentState.Init(owner, this);
        CurrentState.Enter();
    }
    
    public void Update(float dt) => CurrentState?.Update(dt);
    public void FixedUpdate(float fixedDt) => CurrentState?.FixedUpdate(fixedDt);
}

// Usage: Player states
public class IdleState : State<PlayerController>
{
    public override void Update(float dt)
    {
        if (owner.Input.MoveAxis.magnitude > 0.1f)
            machine.TransitionTo(new RunState());
        if (owner.Input.JumpPressed)
            machine.TransitionTo(new JumpState());
    }
}
```

### 26.2 C++ — Behavior Tree (Unreal-style)

```cpp
// Node base class
enum class BTStatus { Success, Failure, Running };

class BTNode {
public:
    virtual ~BTNode() = default;
    virtual BTStatus Tick(float dt) = 0;
};

// Selector: try children until one succeeds
class Selector : public BTNode {
    std::vector<std::unique_ptr<BTNode>> children;
    size_t runningIndex = 0;
public:
    void AddChild(std::unique_ptr<BTNode> child) {
        children.push_back(std::move(child));
    }
    
    BTStatus Tick(float dt) override {
        for (size_t i = runningIndex; i < children.size(); ++i) {
            BTStatus status = children[i]->Tick(dt);
            if (status == BTStatus::Running) {
                runningIndex = i;
                return BTStatus::Running;
            }
            if (status == BTStatus::Success) {
                runningIndex = 0;
                return BTStatus::Success;
            }
        }
        runningIndex = 0;
        return BTStatus::Failure;
    }
};

// Sequence: run children until one fails
class Sequence : public BTNode {
    std::vector<std::unique_ptr<BTNode>> children;
    size_t runningIndex = 0;
public:
    void AddChild(std::unique_ptr<BTNode> child) {
        children.push_back(std::move(child));
    }
    
    BTStatus Tick(float dt) override {
        for (size_t i = runningIndex; i < children.size(); ++i) {
            BTStatus status = children[i]->Tick(dt);
            if (status == BTStatus::Running) {
                runningIndex = i;
                return BTStatus::Running;
            }
            if (status == BTStatus::Failure) {
                runningIndex = 0;
                return BTStatus::Failure;
            }
        }
        runningIndex = 0;
        return BTStatus::Success;
    }
};

// Leaf: concrete action
class MoveToTarget : public BTNode {
    AIAgent* agent;
    float arrivalDist;
public:
    MoveToTarget(AIAgent* a, float dist) : agent(a), arrivalDist(dist) {}
    
    BTStatus Tick(float dt) override {
        if (!agent->HasTarget()) return BTStatus::Failure;
        if (agent->DistToTarget() < arrivalDist) return BTStatus::Success;
        agent->MoveToward(agent->GetTarget(), dt);
        return BTStatus::Running;
    }
};
```

### 26.3 Python — A* Pathfinding

```python
import heapq
from dataclasses import dataclass, field
from typing import Optional

@dataclass(order=True)
class Node:
    f_cost: float
    position: tuple = field(compare=False)
    g_cost: float = field(compare=False)
    parent: Optional['Node'] = field(default=None, compare=False)

def heuristic(a: tuple, b: tuple) -> float:
    """Manhattan distance for grid, Euclidean for navmesh."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid: list[list[int]], start: tuple, goal: tuple) -> list[tuple]:
    """A* on a 2D grid. 0 = walkable, 1 = blocked."""
    rows, cols = len(grid), len(grid[0])
    directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
    
    open_set = [Node(f_cost=0, position=start, g_cost=0)]
    visited = set()
    
    while open_set:
        current = heapq.heappop(open_set)
        
        if current.position == goal:
            # Reconstruct path
            path = []
            node = current
            while node:
                path.append(node.position)
                node = node.parent
            return path[::-1]
        
        if current.position in visited:
            continue
        visited.add(current.position)
        
        for dx, dy in directions:
            nx, ny = current.position[0] + dx, current.position[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
                if (nx, ny) in visited:
                    continue
                # Diagonal costs sqrt(2), cardinal costs 1
                move_cost = 1.414 if dx != 0 and dy != 0 else 1.0
                g = current.g_cost + move_cost
                h = heuristic((nx, ny), goal)
                heapq.heappush(open_set, Node(
                    f_cost=g + h,
                    position=(nx, ny),
                    g_cost=g,
                    parent=current
                ))
    
    return []  # No path found

# Example usage
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0],
]
path = a_star(grid, (0, 0), (4, 4))
print(f"Path: {path}")  # [(0,0), (1,0), (2,0), (2,1), (2,2), (3,2), (3,3), (4,4)]
```

### 26.4 GDScript — Input Action System (Godot)

```gdscript
extends CharacterBody2D

# Input actions defined in Project Settings → Input Map
const SPEED = 200.0
const JUMP_VELOCITY = -400.0
const COYOTE_TIME = 0.1  # seconds
const JUMP_BUFFER_TIME = 0.1

var coyote_timer: float = 0.0
var jump_buffer_timer: float = 0.0
var was_on_floor: bool = false

func _physics_process(delta: float) -> void:
    # Coyote time tracking
    if is_on_floor():
        coyote_timer = COYOTE_TIME
        was_on_floor = true
    elif was_on_floor:
        coyote_timer -= delta
        if coyote_timer <= 0:
            was_on_floor = false
    
    # Jump buffer
    if Input.is_action_just_pressed("jump"):
        jump_buffer_timer = JUMP_BUFFER_TIME
    elif jump_buffer_timer > 0:
        jump_buffer_timer -= delta
    
    # Apply gravity
    if not is_on_floor():
        velocity.y += ProjectSettings.get_setting(
            "physics/2d/default_gravity") * delta
    
    # Jump (with coyote time + buffer)
    if jump_buffer_timer > 0 and (is_on_floor() or coyote_timer > 0):
        velocity.y = JUMP_VELOCITY
        jump_buffer_timer = 0
        coyote_timer = 0
    
    # Horizontal movement
    var direction := Input.get_axis("move_left", "move_right")
    velocity.x = direction * SPEED if direction else move_toward(velocity.x, 0, SPEED)
    
    move_and_slide()
```

---

## 🧮 5. Worked Examples

### Example 26.2.1 — Design an NPC Schedule System (Stardew Valley Style)

**Problem:** Design a system where NPCs follow daily schedules (wake up, go to work, eat lunch, socialize, sleep) with interrupts for player interaction and weather changes.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Architecture: Utility AI + Schedule Table**

```csharp
[System.Serializable]
public struct ScheduleEntry
{
    public float startHour;    // 0-24
    public string location;    // NavMesh destination
    public string animation;   // idle, working, eating
    public string dialogue;    // context-appropriate lines
}

public class NPCScheduleAI : MonoBehaviour
{
    [SerializeField] private ScheduleEntry[] weekdaySchedule;
    [SerializeField] private ScheduleEntry[] weekendSchedule;
    [SerializeField] private ScheduleEntry[] rainySchedule;
    
    private StateMachine<NPCScheduleAI> fsm;
    private NavMeshAgent agent;
    
    private ScheduleEntry[] GetTodaySchedule()
    {
        if (WeatherSystem.IsRaining) return rainySchedule;
        if (TimeSystem.IsWeekend) return weekendSchedule;
        return weekdaySchedule;
    }
    
    private ScheduleEntry GetCurrentEntry()
    {
        var schedule = GetTodaySchedule();
        float hour = TimeSystem.CurrentHour;
        // Find last entry whose startHour <= current hour
        for (int i = schedule.Length - 1; i >= 0; i--)
            if (hour >= schedule[i].startHour) return schedule[i];
        return schedule[0];
    }
    
    void Update()
    {
        var entry = GetCurrentEntry();
        
        // If not at destination, walk there
        if (!IsAtLocation(entry.location))
            agent.SetDestination(GetLocationPosition(entry.location));
        else
            PlayAnimation(entry.animation);
    }
    
    // Interrupt system: player interaction takes priority
    public void OnPlayerInteract()
    {
        fsm.TransitionTo(new TalkingToPlayerState());
        // Returns to schedule after conversation ends
    }
}
```

**Key design decisions:**
1. Schedule is data-driven (ScriptableObject or JSON) — designers edit without code
2. Weather/day-of-week variants give NPCs personality
3. Interrupt system uses FSM priority — player interaction overrides schedule
4. NavMesh handles pathfinding automatically
5. Time system broadcasts events; NPCs react

</details>

### Example 26.2.2 — Command Pattern for Networked Input

**Problem:** Implement a command system that records player inputs for replay and can be serialized for network transmission.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```csharp
// Base command interface
public interface ICommand
{
    int Frame { get; }
    void Execute(GameState state);
    void Undo(GameState state);
    byte[] Serialize();
}

// Concrete command
public struct MoveCommand : ICommand
{
    public int Frame { get; }
    public Vector2 Direction { get; }
    public int EntityId { get; }
    
    private Vector2 previousPosition; // for undo
    
    public MoveCommand(int frame, int entityId, Vector2 dir)
    {
        Frame = frame;
        EntityId = entityId;
        Direction = dir;
        previousPosition = default;
    }
    
    public void Execute(GameState state)
    {
        var entity = state.GetEntity(EntityId);
        previousPosition = entity.Position;
        entity.Position += Direction * entity.Speed * GameState.FIXED_DT;
    }
    
    public void Undo(GameState state)
    {
        state.GetEntity(EntityId).Position = previousPosition;
    }
    
    public byte[] Serialize()
    {
        // 4 bytes frame + 4 bytes entityId + 8 bytes direction = 16 bytes
        var buffer = new byte[16];
        BitConverter.GetBytes(Frame).CopyTo(buffer, 0);
        BitConverter.GetBytes(EntityId).CopyTo(buffer, 4);
        BitConverter.GetBytes(Direction.x).CopyTo(buffer, 8);
        BitConverter.GetBytes(Direction.y).CopyTo(buffer, 12);
        return buffer;
    }
}

// Command buffer for replay/network
public class CommandBuffer
{
    private List<ICommand> history = new();
    private int currentFrame = 0;
    
    public void Record(ICommand cmd)
    {
        history.Add(cmd);
        cmd.Execute(GameState.Current);
    }
    
    // Rollback for netcode
    public void RollbackTo(int frame)
    {
        for (int i = history.Count - 1; i >= 0; i--)
        {
            if (history[i].Frame >= frame)
                history[i].Undo(GameState.Current);
            else break;
        }
    }
    
    // Re-simulate with corrected inputs
    public void Resimulate(int fromFrame, List<ICommand> correctedInputs)
    {
        RollbackTo(fromFrame);
        foreach (var cmd in correctedInputs)
            cmd.Execute(GameState.Current);
    }
}
```

This pattern is the foundation of rollback netcode (Chapter 26.6).

</details>

### Example 26.2.3 — Utility AI for Enemy Decision-Making

**Problem:** An enemy NPC must choose between: patrol, chase player, flee (low health), call for help, or use health potion. Design a Utility AI system.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```python
from dataclasses import dataclass
from typing import Callable

@dataclass
class Action:
    name: str
    score_fn: Callable[['AIContext'], float]
    execute_fn: Callable[['AIContext'], None]

@dataclass
class AIContext:
    health_pct: float          # 0.0 - 1.0
    dist_to_player: float      # meters
    has_potion: bool
    allies_nearby: int
    player_health_pct: float
    is_player_visible: bool

def score_patrol(ctx: AIContext) -> float:
    """High when nothing interesting is happening."""
    if ctx.is_player_visible: return 0.0
    return 0.5

def score_chase(ctx: AIContext) -> float:
    """High when player is visible and we're healthy."""
    if not ctx.is_player_visible: return 0.0
    health_factor = ctx.health_pct  # 0-1
    distance_factor = max(0, 1.0 - ctx.dist_to_player / 20.0)  # closer = higher
    return health_factor * distance_factor * 0.9

def score_flee(ctx: AIContext) -> float:
    """High when health is critical."""
    if ctx.health_pct > 0.3: return 0.0
    danger = 1.0 - ctx.health_pct  # lower health = higher score
    return danger * 0.95  # Almost always wins when health is low

def score_call_help(ctx: AIContext) -> float:
    """High when outnumbered and allies exist nearby."""
    if ctx.allies_nearby == 0: return 0.0
    if ctx.health_pct > 0.5: return 0.2
    return (1.0 - ctx.health_pct) * 0.7

def score_use_potion(ctx: AIContext) -> float:
    """High when damaged and have a potion."""
    if not ctx.has_potion: return 0.0
    if ctx.health_pct > 0.7: return 0.0
    return (1.0 - ctx.health_pct) * 0.85

class UtilityAI:
    def __init__(self):
        self.actions: list[Action] = []
    
    def add_action(self, name: str, score_fn, execute_fn):
        self.actions.append(Action(name, score_fn, execute_fn))
    
    def decide(self, context: AIContext) -> Action:
        """Pick the action with the highest utility score."""
        scored = [(a, a.score_fn(context)) for a in self.actions]
        scored.sort(key=lambda x: x[1], reverse=True)
        best_action, best_score = scored[0]
        return best_action

# Setup
ai = UtilityAI()
ai.add_action("patrol", score_patrol, lambda ctx: print("Patrolling..."))
ai.add_action("chase", score_chase, lambda ctx: print("Chasing player!"))
ai.add_action("flee", score_flee, lambda ctx: print("Fleeing!"))
ai.add_action("call_help", score_call_help, lambda ctx: print("Calling allies!"))
ai.add_action("use_potion", score_use_potion, lambda ctx: print("Drinking potion!"))

# Test scenarios
ctx_healthy = AIContext(0.9, 10.0, True, 2, 0.8, True)
print(ai.decide(ctx_healthy).name)  # "chase"

ctx_wounded = AIContext(0.2, 5.0, True, 0, 0.8, True)
print(ai.decide(ctx_wounded).name)  # "flee"

ctx_wounded_potion = AIContext(0.2, 15.0, True, 0, 0.8, False)
print(ai.decide(ctx_wounded_potion).name)  # "flee" (no potion, far from player)
```

**Why Utility AI over Behavior Trees here:**
- Smooth transitions (no hard-coded priority)
- Easy to tune (adjust score curves)
- Emergent behavior from score interactions
- Scales to many actions without deep tree nesting

</details>

---

## ⚠️ 6. Gotchas & Anti-Patterns

### ❌ Anti-Pattern: String-Based Input Checks

```csharp
// BAD: typo-prone, no compile-time safety, allocation per call
if (Input.GetButtonDown("Junp")) { }  // silent failure

// GOOD: Unity's new Input System with generated C# class
if (controls.Player.Jump.WasPressedThisFrame()) { }
```

### ❌ Anti-Pattern: Transition Spaghetti

An FSM with N states can have up to $N(N-1)$ transitions. Beyond ~8 states, the transition graph becomes unmaintainable. Solutions:
- **Hierarchical FSM:** Group related states, reduce cross-group transitions
- **Behavior Tree:** Composable, no explicit transitions
- **Pushdown Automaton:** Stack-based states (push combat, pop back to exploration)

### ❌ Anti-Pattern: Pathfinding Every Frame

A* is expensive ($O(E \log V)$ where $E$ = edges, $V$ = vertices). Don't recalculate every frame:
- Cache paths, recalculate only when destination changes or path is blocked
- Use hierarchical pathfinding (coarse grid → fine grid)
- Spread computation across frames (coroutines / async)

### ❌ Anti-Pattern: AI That Cheats Visibly

NPCs that clearly know things they shouldn't (player position through walls, inventory contents) break immersion. Use perception systems:
- **Line of sight** (raycast)
- **Hearing radius** (distance + noise level)
- **Memory decay** (last known position ages)

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- **Previous:** [26.1 - Game Loop & Architecture](26.1---Game-Loop-&-Architecture)
- **Next:** [26.3 - 2D Game Patterns - Sprites, Tilemaps, Physics](26.3---2D-Game-Patterns---Sprites,-Tilemaps,-Physics)
- **Pathfinding algorithms:** [08.13 - Algorithms & Data Structures in Python](08.13---Algorithms-&-Data-Structures-in-Python) — graph algorithms, priority queues
- **State machines in engines:** [28.5 - Game Engine Architectures - Unity & Unreal](28.5---Game-Engine-Architectures---Unity-&-Unreal) — Unity Animator, Unreal BT
- **Math for steering:** [28.1 - 3D Math Fundamentals](28.1---3D-Math-Fundamentals) — vector operations for seek/flee/arrive

### External Resources
- **Game AI Pro** (gameaipro.com) — free chapters on BTs, utility AI, pathfinding
- **AI Game Programming Wisdom** series — classic reference
- **Sebastian Lague: "A* Pathfinding"** (YouTube) — visual explanation
- **Unreal Engine: Behavior Tree Quick Start** — official docs
- **GDC: "Building a Better Centaur: AI at Massive Scale"** — Halo Infinite AI

### Practice
- `_practice/scripts/4.2_state_machines.py` — FSM simulator with visualization



---

## 🔬 8. Advanced Topics — Behavior Trees, GOAP & Steering Behaviors

### 8.1 — Behavior Trees vs. HFSM vs. GOAP: Complete Comparison

Game AI decision-making architectures range from simple (FSM) to highly flexible (GOAP). Each has distinct tradeoffs in expressiveness, performance, and designer-friendliness.

#### Hierarchical Finite State Machine (HFSM)

An HFSM nests state machines inside states, allowing complex behaviors without exponential transition explosion.

```csharp
// HFSM Implementation with hierarchical states
public abstract class HFSMState
{
    public string Name { get; }
    protected HFSMState parentState;
    protected HFSMState activeSubState;
    protected List<Transition> transitions = new();
    
    public virtual void Enter() { activeSubState?.Enter(); }
    public virtual void Exit() { activeSubState?.Exit(); }
    
    public virtual void Update(float dt)
    {
        // Check transitions at this level first
        foreach (var t in transitions)
        {
            if (t.Condition())
            {
                parentState?.ChangeSubState(t.Target);
                return;
            }
        }
        // Then update active sub-state
        activeSubState?.Update(dt);
    }
    
    protected void ChangeSubState(HFSMState newState)
    {
        activeSubState?.Exit();
        activeSubState = newState;
        activeSubState?.Enter();
    }
}

// Example: Combat AI
// Root: [Patrol] ←→ [Combat] ←→ [Flee]
//   Combat substates: [Approach] → [Attack] → [Retreat] → [Approach]
//   Patrol substates: [Wander] → [Investigate] → [Wander]
public class CombatState : HFSMState
{
    private HFSMState approachState, attackState, retreatState;
    
    public override void Enter()
    {
        // Start in approach sub-state
        activeSubState = approachState;
        activeSubState.Enter();
    }
}
```

**Strengths:** Intuitive for designers, visual debugging, predictable behavior.
**Weaknesses:** Transition explosion for complex AI, rigid (hard to add new behaviors without rewiring transitions), poor at handling interrupts gracefully.

#### Behavior Trees (BT)

Behavior Trees use a tree of nodes evaluated top-to-bottom, left-to-right. They compose complex behaviors from simple building blocks.

**Node Types:**
- **Composite:** Sequence (AND), Selector (OR), Parallel
- **Decorator:** Inverter, Repeater, Cooldown, Conditional Guard
- **Leaf:** Action (do something), Condition (check something)

```csharp
// Core BT node types
public enum NodeStatus { Running, Success, Failure }

public abstract class BTNode
{
    public abstract NodeStatus Tick(Blackboard bb, float dt);
}

// Sequence: runs children left-to-right, fails on first failure
public class Sequence : BTNode
{
    private List<BTNode> children;
    private int currentChild = 0;
    
    public override NodeStatus Tick(Blackboard bb, float dt)
    {
        while (currentChild < children.Count)
        {
            var status = children[currentChild].Tick(bb, dt);
            
            if (status == NodeStatus.Running)
                return NodeStatus.Running; // Resume here next frame
            
            if (status == NodeStatus.Failure)
            {
                currentChild = 0; // Reset for next evaluation
                return NodeStatus.Failure;
            }
            
            currentChild++; // Success → move to next child
        }
        
        currentChild = 0;
        return NodeStatus.Success; // All children succeeded
    }
}

// Selector: runs children left-to-right, succeeds on first success
public class Selector : BTNode
{
    private List<BTNode> children;
    private int currentChild = 0;
    
    public override NodeStatus Tick(Blackboard bb, float dt)
    {
        while (currentChild < children.Count)
        {
            var status = children[currentChild].Tick(bb, dt);
            
            if (status == NodeStatus.Running)
                return NodeStatus.Running;
            
            if (status == NodeStatus.Success)
            {
                currentChild = 0;
                return NodeStatus.Success;
            }
            
            currentChild++; // Failure → try next child
        }
        
        currentChild = 0;
        return NodeStatus.Failure; // All children failed
    }
}

// Decorator: Cooldown (prevents re-evaluation for N seconds)
public class Cooldown : BTNode
{
    private BTNode child;
    private float cooldownTime;
    private float lastSuccessTime = float.NegativeInfinity;
    
    public override NodeStatus Tick(Blackboard bb, float dt)
    {
        if (Time.time - lastSuccessTime < cooldownTime)
            return NodeStatus.Failure; // Still on cooldown
        
        var status = child.Tick(bb, dt);
        if (status == NodeStatus.Success)
            lastSuccessTime = Time.time;
        return status;
    }
}

// Leaf: Action node
public class MoveToTarget : BTNode
{
    public override NodeStatus Tick(Blackboard bb, float dt)
    {
        Vector3 target = bb.Get<Vector3>("targetPosition");
        Vector3 current = bb.Get<Vector3>("myPosition");
        
        float distance = Vector3.Distance(current, target);
        
        if (distance < 1.0f)
            return NodeStatus.Success;
        
        // Move toward target
        Vector3 direction = (target - current).normalized;
        bb.Set("desiredVelocity", direction * bb.Get<float>("moveSpeed"));
        return NodeStatus.Running;
    }
}
```

**Complete BT Example — Guard AI:**

```yaml
# Pseudocode tree structure
Selector (Root):
  ├── Sequence (Combat):
  │   ├── Condition: HasTarget?
  │   ├── Selector (Engage):
  │   │   ├── Sequence (Melee):
  │   │   │   ├── Condition: TargetInMeleeRange?
  │   │   │   └── Action: MeleeAttack
  │   │   └── Sequence (Ranged):
  │   │       ├── Condition: HasAmmo?
  │   │       ├── Action: AimAtTarget
  │   │       └── Action: Shoot
  │   └── Action: MoveToTarget
  ├── Sequence (Investigate):
  │   ├── Condition: HeardNoise?
  │   ├── Action: MoveToNoiseSource
  │   └── Action: LookAround
  └── Sequence (Patrol):
      ├── Action: MoveToNextWaypoint
      └── Action: WaitAtWaypoint(3s)
```

**Strengths:** Modular, composable, easy to extend, visual editors (Unreal BT, NodeCanvas).
**Weaknesses:** Reactive only (re-evaluates from root each tick unless using "running" state), no planning ahead, can be expensive for deep trees.

#### Goal-Oriented Action Planning (GOAP)

GOAP treats AI as a planning problem. The agent has a **world state** (set of boolean/numeric facts), **goals** (desired world state), and **actions** (preconditions + effects). A planner searches for a sequence of actions that transforms the current state into the goal state.

```csharp
// GOAP Core Types
public struct WorldState
{
    // Bit-packed boolean facts for fast comparison
    public ulong flags;
    public ulong careMask; // Which bits matter for this state/goal
    
    public bool Satisfies(WorldState goal)
    {
        // Check only the bits the goal cares about
        return (flags & goal.careMask) == (goal.flags & goal.careMask);
    }
    
    public int Difference(WorldState other)
    {
        // Count differing bits (heuristic for A*)
        ulong diff = (flags ^ other.flags) & other.careMask;
        return BitCount(diff);
    }
}

public class GOAPAction
{
    public string Name;
    public float Cost;
    public WorldState Preconditions;  // Required state to execute
    public WorldState Effects;         // State changes after execution
    
    // Runtime validation (e.g., "is there actually ammo nearby?")
    public Func<bool> ProceduralPrecondition;
    
    public WorldState ApplyEffects(WorldState current)
    {
        // Set effect bits, clear non-effect bits as needed
        ulong result = current.flags;
        result |= (Effects.flags & Effects.careMask);           // Set true effects
        result &= ~(~Effects.flags & Effects.careMask);         // Clear false effects
        return new WorldState { flags = result, careMask = current.careMask };
    }
}

// GOAP Planner using backward A* search
public class GOAPPlanner
{
    public List<GOAPAction> Plan(WorldState current, WorldState goal, List<GOAPAction> available)
    {
        // A* search backward from goal to current state
        var openSet = new PriorityQueue<PlanNode, float>();
        var closedSet = new HashSet<ulong>();
        
        openSet.Enqueue(new PlanNode(goal, null, null, 0), 0);
        
        while (openSet.Count > 0)
        {
            var node = openSet.Dequeue();
            
            if (current.Satisfies(node.State))
            {
                // Found a path — reconstruct action sequence
                return ReconstructPlan(node);
            }
            
            if (closedSet.Contains(node.State.flags))
                continue;
            closedSet.Add(node.State.flags);
            
            foreach (var action in available)
            {
                // Can this action's effects satisfy any of our unsatisfied preconditions?
                if (!ActionContributes(action, node.State))
                    continue;
                
                if (action.ProceduralPrecondition != null && !action.ProceduralPrecondition())
                    continue;
                
                // Apply action backward: what state do we need BEFORE this action?
                WorldState requiredState = ComputeRequiredState(node.State, action);
                float newCost = node.Cost + action.Cost;
                float heuristic = requiredState.Difference(current);
                
                openSet.Enqueue(
                    new PlanNode(requiredState, action, node, newCost),
                    newCost + heuristic
                );
            }
        }
        
        return null; // No valid plan found
    }
}
```

**Example GOAP Setup — Survival AI:**

```csharp
// Actions available to the agent
var actions = new List<GOAPAction>
{
    new GOAPAction {
        Name = "PickUpAxe",
        Cost = 2,
        Preconditions = State("nearAxe=true"),
        Effects = State("hasAxe=true")
    },
    new GOAPAction {
        Name = "ChopTree",
        Cost = 4,
        Preconditions = State("hasAxe=true, nearTree=true"),
        Effects = State("hasWood=true")
    },
    new GOAPAction {
        Name = "BuildFire",
        Cost = 3,
        Preconditions = State("hasWood=true"),
        Effects = State("hasFire=true")
    },
    new GOAPAction {
        Name = "CookFood",
        Cost = 2,
        Preconditions = State("hasFire=true, hasRawFood=true"),
        Effects = State("hasCookedFood=true")
    },
    new GOAPAction {
        Name = "Eat",
        Cost = 1,
        Preconditions = State("hasCookedFood=true"),
        Effects = State("isHungry=false")
    }
};

// Goal: not hungry
WorldState goal = State("isHungry=false");

// Planner finds: PickUpAxe → ChopTree → BuildFire → CookFood → Eat
var plan = planner.Plan(currentState, goal, actions);
```

**Strengths:** Emergent behavior, easy to add new actions without rewiring, handles complex multi-step goals, used in F.E.A.R., Shadow of Mordor, Tomb Raider.
**Weaknesses:** Planning is expensive (A* search each time goal changes), harder to debug (why did it choose THAT plan?), requires careful cost tuning.

#### Master Comparison Table

| Criterion | HFSM | Behavior Tree | GOAP |
|-----------|------|---------------|------|
| Complexity to implement | Low | Medium | High |
| Designer-friendliness | ★★★★☆ | ★★★★★ | ★★★☆☆ |
| Emergent behavior | ❌ | ❌ | ✅ |
| Scalability (adding behaviors) | Poor (transition explosion) | Good (add subtrees) | Excellent (add actions) |
| Performance | O(1) per tick | O(tree depth) per tick | O(A* search) on replan |
| Debugging | Easy (current state visible) | Medium (tree visualization) | Hard (plan inspection) |
| Best for | Simple enemies, UI | Most game AI | Complex NPCs, sandbox games |
| Real-world examples | Pac-Man ghosts, Doom | Halo, Unreal AI | F.E.A.R., Shadow of Mordor |

---

### 8.2 — NavMesh Queries & Pathfinding Integration

Navigation meshes (NavMeshes) represent walkable surfaces as a connected graph of convex polygons. Pathfinding on NavMeshes is faster and more natural than grid-based A*.

#### NavMesh Query Pipeline

```csharp
// Unity NavMesh query pipeline
public class NavMeshPathfinder
{
    // 1. Find nearest point on NavMesh (snap world position to walkable surface)
    public Vector3 SnapToNavMesh(Vector3 worldPos, float maxDistance = 10f)
    {
        if (NavMesh.SamplePosition(worldPos, out NavMeshHit hit, maxDistance, NavMesh.AllAreas))
            return hit.position;
        return worldPos; // Fallback
    }
    
    // 2. Calculate path
    public NavMeshPath CalculatePath(Vector3 start, Vector3 end)
    {
        var path = new NavMeshPath();
        Vector3 snappedStart = SnapToNavMesh(start);
        Vector3 snappedEnd = SnapToNavMesh(end);
        
        NavMesh.CalculatePath(snappedStart, snappedEnd, NavMesh.AllAreas, path);
        return path;
    }
    
    // 3. String-pulling (funnel algorithm) for smooth paths
    // Unity does this internally, but here's the concept:
    public List<Vector3> FunnelSmooth(NavMeshPath rawPath)
    {
        // The funnel algorithm finds the shortest path through a corridor
        // of NavMesh polygons, producing smooth waypoints at portal edges
        var smoothed = new List<Vector3>();
        
        // Raw path gives polygon corridor
        // Funnel narrows the corridor to find optimal waypoints
        // Result: minimal waypoints, no unnecessary zigzag
        
        return smoothed;
    }
    
    // 4. Area cost queries (avoid water, prefer roads)
    public void SetAreaCosts(NavMeshAgent agent)
    {
        agent.SetAreaCost(NavMesh.GetAreaFromName("Road"), 1.0f);    // Prefer
        agent.SetAreaCost(NavMesh.GetAreaFromName("Grass"), 2.0f);   // Acceptable
        agent.SetAreaCost(NavMesh.GetAreaFromName("Swamp"), 5.0f);   // Avoid
        agent.SetAreaCost(NavMesh.GetAreaFromName("Lava"), 100.0f);  // Emergency only
    }
}
```

#### Hierarchical Pathfinding (HPA*)

For large worlds, pathfinding on the full NavMesh is expensive. HPA* (Hierarchical Pathfinding A*) divides the world into clusters and pre-computes inter-cluster paths:

```
Level 2 (Coarse):  [Region A] ——→ [Region B] ——→ [Region C]
Level 1 (Medium):  [Cluster 1] → [Cluster 2] → [Cluster 5] → [Cluster 6]
Level 0 (Fine):    [Poly 1] → [Poly 2] → ... → [Poly N]  (only within current cluster)
```

This reduces A* search space from thousands of polygons to dozens of clusters, then refines locally.

---

### 8.3 — Reynolds Steering Behaviors

Craig Reynolds' steering behaviors (1987) produce natural-looking movement by combining simple force vectors. Each behavior outputs a **steering force** that is summed and applied to the agent's velocity.

```csharp
public class SteeringAgent
{
    public Vector3 Position;
    public Vector3 Velocity;
    public float MaxSpeed = 5f;
    public float MaxForce = 10f;
    public float Mass = 1f;
    
    public void ApplySteering(Vector3 steeringForce, float dt)
    {
        // Truncate to max force
        steeringForce = Vector3.ClampMagnitude(steeringForce, MaxForce);
        
        // F = ma → a = F/m
        Vector3 acceleration = steeringForce / Mass;
        
        // Euler integration
        Velocity += acceleration * dt;
        Velocity = Vector3.ClampMagnitude(Velocity, MaxSpeed);
        Position += Velocity * dt;
    }
    
    // --- Individual Behaviors ---
    
    // SEEK: steer toward target at max speed
    public Vector3 Seek(Vector3 target)
    {
        Vector3 desired = (target - Position).normalized * MaxSpeed;
        return desired - Velocity; // Steering = desired - current
    }
    
    // FLEE: steer away from target
    public Vector3 Flee(Vector3 threat)
    {
        Vector3 desired = (Position - threat).normalized * MaxSpeed;
        return desired - Velocity;
    }
    
    // ARRIVE: seek with deceleration near target
    public Vector3 Arrive(Vector3 target, float slowRadius = 5f)
    {
        Vector3 toTarget = target - Position;
        float distance = toTarget.magnitude;
        
        if (distance < 0.1f)
            return -Velocity; // Brake
        
        // Ramp speed down within slow radius
        float desiredSpeed = (distance < slowRadius)
            ? MaxSpeed * (distance / slowRadius)
            : MaxSpeed;
        
        Vector3 desired = toTarget.normalized * desiredSpeed;
        return desired - Velocity;
    }
    
    // PURSUIT: predict target's future position
    public Vector3 Pursuit(SteeringAgent target)
    {
        Vector3 toTarget = target.Position - Position;
        float lookAheadTime = toTarget.magnitude / (MaxSpeed + target.Velocity.magnitude);
        
        Vector3 predictedPos = target.Position + target.Velocity * lookAheadTime;
        return Seek(predictedPos);
    }
    
    // EVADE: flee from predicted position
    public Vector3 Evade(SteeringAgent pursuer)
    {
        Vector3 toPursuer = pursuer.Position - Position;
        float lookAheadTime = toPursuer.magnitude / (MaxSpeed + pursuer.Velocity.magnitude);
        
        Vector3 predictedPos = pursuer.Position + pursuer.Velocity * lookAheadTime;
        return Flee(predictedPos);
    }
    
    // WANDER: smooth random movement
    private float wanderAngle = 0f;
    public Vector3 Wander(float circleDistance = 2f, float circleRadius = 1f, float jitter = 0.3f)
    {
        wanderAngle += (Random.value - 0.5f) * jitter;
        
        Vector3 circleCenter = Velocity.normalized * circleDistance;
        Vector3 displacement = new Vector3(
            Mathf.Cos(wanderAngle) * circleRadius,
            0,
            Mathf.Sin(wanderAngle) * circleRadius
        );
        
        return circleCenter + displacement;
    }
    
    // OBSTACLE AVOIDANCE: raycast ahead, steer away
    public Vector3 ObstacleAvoidance(float detectionLength = 5f)
    {
        Vector3 ahead = Position + Velocity.normalized * detectionLength;
        
        if (Physics.Raycast(Position, Velocity.normalized, out RaycastHit hit, detectionLength))
        {
            // Steer perpendicular to obstacle surface
            Vector3 avoidForce = (ahead - hit.point).normalized * MaxForce;
            return avoidForce;
        }
        
        return Vector3.zero;
    }
    
    // SEPARATION: avoid crowding neighbors (flocking)
    public Vector3 Separation(List<SteeringAgent> neighbors, float desiredSeparation = 2f)
    {
        Vector3 force = Vector3.zero;
        int count = 0;
        
        foreach (var other in neighbors)
        {
            float dist = Vector3.Distance(Position, other.Position);
            if (dist > 0 && dist < desiredSeparation)
            {
                Vector3 away = (Position - other.Position).normalized / dist; // Weight by proximity
                force += away;
                count++;
            }
        }
        
        if (count > 0)
            force /= count;
        
        return force;
    }
    
    // COHESION: steer toward center of neighbors (flocking)
    public Vector3 Cohesion(List<SteeringAgent> neighbors)
    {
        Vector3 center = Vector3.zero;
        int count = 0;
        
        foreach (var other in neighbors)
        {
            center += other.Position;
            count++;
        }
        
        if (count == 0) return Vector3.zero;
        
        center /= count;
        return Seek(center);
    }
    
    // ALIGNMENT: match heading of neighbors (flocking)
    public Vector3 Alignment(List<SteeringAgent> neighbors)
    {
        Vector3 avgVelocity = Vector3.zero;
        int count = 0;
        
        foreach (var other in neighbors)
        {
            avgVelocity += other.Velocity;
            count++;
        }
        
        if (count == 0) return Vector3.zero;
        
        avgVelocity /= count;
        return avgVelocity.normalized * MaxSpeed - Velocity;
    }
}

// Combining behaviors with priority and weighting
public Vector3 CalculateSteering(SteeringAgent agent, List<SteeringAgent> flock)
{
    Vector3 steering = Vector3.zero;
    
    // Priority-based: higher priority behaviors consume force budget first
    float remainingForce = agent.MaxForce;
    
    // 1. Obstacle avoidance (highest priority)
    Vector3 avoidance = agent.ObstacleAvoidance();
    steering += ClampAndConsume(avoidance, ref remainingForce);
    
    // 2. Separation (don't overlap)
    Vector3 separation = agent.Separation(flock) * 1.5f;
    steering += ClampAndConsume(separation, ref remainingForce);
    
    // 3. Cohesion + Alignment (flocking)
    Vector3 cohesion = agent.Cohesion(flock) * 1.0f;
    Vector3 alignment = agent.Alignment(flock) * 1.0f;
    steering += ClampAndConsume(cohesion + alignment, ref remainingForce);
    
    // 4. Seek/Wander (lowest priority, uses remaining budget)
    Vector3 wander = agent.Wander();
    steering += ClampAndConsume(wander, ref remainingForce);
    
    return steering;
}
```

---

## 📎 9. Appendix — Mathematical Foundations

### Appendix 9.A — A* Heuristic Admissibility Proof

**Theorem:** A* with an admissible heuristic $h(n)$ always finds the optimal (shortest) path.

**Definition:** A heuristic $h(n)$ is **admissible** if it never overestimates the true cost to reach the goal:

$$
h(n) \leq h^*(n) \quad \forall n
$$

where $h^*(n)$ is the true optimal cost from node $n$ to the goal.

**Proof (by contradiction):**

Assume A* terminates with a suboptimal path of cost $C_{sub} > C^*$ (where $C^*$ is the optimal cost).

Let $n$ be any node on the optimal path that is still in the open set when A* terminates. Such a node must exist because A* only terminates when the goal is dequeued, and if the optimal path hasn't been fully explored, at least one of its nodes remains open.

The $f$-value of $n$ is:

$$
f(n) = g(n) + h(n)
$$

Since $n$ is on the optimal path, $g(n)$ is the true cost from start to $n$ along the optimal path, and:

$$
g(n) + h^*(n) = C^*
$$

Since $h$ is admissible ($h(n) \leq h^*(n)$):

$$
f(n) = g(n) + h(n) \leq g(n) + h^*(n) = C^*
$$

But A* selected the goal with cost $C_{sub}$ before selecting $n$. This means:

$$
C_{sub} \leq f(n) \leq C^*
$$

This contradicts our assumption that $C_{sub} > C^*$. Therefore, A* must find the optimal path. $\blacksquare$

**Common Admissible Heuristics for Grid Pathfinding:**

| Heuristic | Formula | Admissible for |
|-----------|---------|----------------|
| Manhattan | $\|x_1 - x_2\| + \|y_1 - y_2\|$ | 4-directional movement |
| Euclidean | $\sqrt{(x_1-x_2)^2 + (y_1-y_2)^2}$ | Any-angle movement |
| Chebyshev | $\max(\|x_1-x_2\|, \|y_1-y_2\|)$ | 8-directional (uniform cost) |
| Octile | $\max(\|dx\|,\|dy\|) + (\sqrt{2}-1)\min(\|dx\|,\|dy\|)$ | 8-directional (diagonal = √2) |

**Consistency (Monotonicity):** A stronger property than admissibility. $h$ is consistent if:

$$
h(n) \leq c(n, n') + h(n') \quad \forall \text{ edges } (n, n')
$$

Consistent heuristics guarantee that A* never re-expands a node (closed set is final). All consistent heuristics are admissible, but not vice versa.

---

### Appendix 9.B — Goal-Oriented Action Planning Solver: Formal Specification

GOAP can be formalized as a **planning problem** in the STRIPS tradition:

**Definition:** A GOAP problem is a tuple $\langle S, A, s_0, G \rangle$ where:
- $S$ is the set of all possible world states (bit vectors of length $n$)
- $A$ is the set of available actions
- $s_0 \in S$ is the initial state
- $G \subseteq S$ is the set of goal states

Each action $a \in A$ is defined by:
- $\text{pre}(a) \subseteq \{0,1\}^n$ — precondition mask and values
- $\text{eff}(a) \subseteq \{0,1\}^n$ — effect mask and values
- $\text{cost}(a) \in \mathbb{R}^+$ — action cost

**State Transition:**

$$
\text{apply}(s, a) = (s \land \lnot \text{eff\_mask}(a)) \lor (\text{eff\_values}(a) \land \text{eff\_mask}(a))
$$

**Backward Search (Regressive Planning):**

Starting from goal $G$, we search backward asking "what action could have produced this state?" For each action $a$ whose effects satisfy some unsatisfied goal condition:

$$
\text{regress}(G, a) = (G \setminus \text{eff}(a)) \cup \text{pre}(a)
$$

The regressed state represents what must be true *before* action $a$ executes for the goal to be achievable.

**Heuristic for GOAP A*:**

The simplest admissible heuristic counts unsatisfied goal conditions:

$$
h(s) = |\{i : s_i \neq G_i \land G_i \text{ is specified}\}|
$$

This is admissible because each action can satisfy at most all remaining conditions (cost ≥ 1 per action minimum). A tighter heuristic uses the minimum-cost action that satisfies each unsatisfied condition:

$$
h(s) = \sum_{i \in \text{unsatisfied}} \min_{a : \text{eff}(a) \text{ satisfies } i} \text{cost}(a)
$$

This is still admissible (relaxation: assumes actions don't interfere with each other) and provides much better search guidance.

**Complexity:** GOAP planning is NP-hard in general (reducible to STRIPS planning). However, game AI typically has:
- Small state spaces (10-30 boolean facts)
- Few actions (10-50)
- Short plans (3-8 actions)

This makes A* search tractable in practice (< 1ms for typical game AI).

---

