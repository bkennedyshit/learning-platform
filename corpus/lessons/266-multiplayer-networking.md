---
title: "26.6 — Multiplayer & Networking"
subject: "Game Dev"
catalog: advanced
audience_tier: higher-education
chapter: "26.6"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 26.6 — Multiplayer & Networking

> *"The internet is a lie. Every multiplayer game you've ever played is an elaborate illusion designed to hide the fact that information cannot travel faster than light."* — Glenn Fiedler

Networking is the hardest problem in game development. You're fighting physics itself — the speed of light imposes minimum latency, packets get lost, arrive out of order, or arrive too late to be useful. This chapter covers the full spectrum: from client-server architecture to rollback netcode, from snapshot interpolation to lag compensation. Every technique is a trade-off between responsiveness, consistency, and bandwidth.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Implement a **client-server architecture** with authoritative server state.
2. Implement **client-side prediction** with server reconciliation.
3. Build **rollback netcode** for fighting/action games.
4. Implement **snapshot interpolation** for smooth remote entity display.
5. Design **lag compensation** (server-side rewind) for hit detection.
6. Choose between **TCP and UDP** and implement reliable UDP when needed.
7. Optimize **bandwidth** with delta compression, quantization, and interest management.

---

## 🖼️ Visual Anchor — Network Models Comparison

![gamedev__4.6-fig1](gamedev__4.6-fig1.svg)

---

## 📚 1. Concepts & Definitions

### Definition 26.6.1 — Latency (Ping)

**Latency** is the round-trip time (RTT) for a packet to travel from client to server and back:

$$
\text{RTT} = t_{\text{send}} + t_{\text{process}} + t_{\text{return}}
$$

Typical values: LAN = 1-5ms, same region = 20-50ms, cross-continent = 100-200ms, intercontinental = 200-400ms.

**One-way latency** (what matters for game feel) ≈ RTT/2.

### Definition 26.6.2 — Network Models

| Model | Authority | Latency Feel | Consistency | Bandwidth |
|-------|-----------|-------------|-------------|-----------|
| **Lockstep** | All peers | High (wait for slowest) | Perfect | Low (inputs only) |
| **Client-Server (authoritative)** | Server | Medium (RTT/2) | Strong | Medium |
| **Client Prediction + Reconciliation** | Server | Low (immediate local) | Eventual | Medium |
| **Rollback** | Speculative | Zero (predict remote) | Corrected | Low |
| **Snapshot Interpolation** | Server | High (buffered) | Smooth | High |

### Definition 26.6.3 — Client-Side Prediction

The client **immediately** applies its own input locally (prediction), then waits for server confirmation. If the server agrees, nothing changes. If the server disagrees (due to another player's action), the client **reconciles** by snapping to the server state and re-applying unacknowledged inputs.

### Definition 26.6.4 — Rollback Netcode

**Rollback** predicts remote players' inputs (usually: "same as last frame") and simulates forward. When actual remote input arrives:
1. If prediction was correct → no correction needed
2. If prediction was wrong → **rollback** game state to the frame of the input, apply correct input, **resimulate** all frames up to present

### Definition 26.6.5 — Snapshot Interpolation

The server sends full world state **snapshots** at a fixed rate (e.g., 20 Hz). Clients render entities by interpolating between the two most recent snapshots, introducing a deliberate delay (typically 100ms) to ensure smooth motion even with packet loss.

### Definition 26.6.6 — Lag Compensation (Server Rewind)

When a player shoots, the server **rewinds** the world state to what that player saw at the time they fired (accounting for their latency). This ensures hits feel fair to the shooter, even at high ping.

---

## 🧩 2. Mental Models / Architecture

### Model 2.1 — Client-Server with Prediction

```
Client (Player A):                    Server:                    Client (Player B):
                                      
Frame 10: Input "move right"          
  → Apply locally (predict)           
  → Send input to server ──────────→  Frame 12: Receive A's input
                                        → Validate & apply
                                        → Broadcast state ──────→ Frame 14: Receive state
                                                                   → Interpolate B's view of A
Frame 13: Receive server state        
  → Compare with prediction           
  → If mismatch: snap + replay        
```

### Model 2.2 — Rollback Timeline

```
Frame:    1    2    3    4    5    6    7    8
Local:    L1   L2   L3   L4   L5   L6   L7   L8
Remote:   R1   R2   ?    ?    ?    ?    ?    ?   (predicted as R2)
                    ↑
                    Actual R3 arrives at frame 7!
                    
Rollback: rewind to frame 3
          apply actual R3
          resimulate frames 3→7 with correct inputs
          if state differs from prediction → visual correction
```

### Model 2.3 — Bandwidth Budget

For a 16-player game at 60 tick rate:
- Per-entity state: ~32 bytes (position, rotation, velocity)
- Full snapshot: 16 × 32 = 512 bytes
- At 60 Hz: 512 × 60 = 30.7 KB/s per client
- 16 clients: 491 KB/s server upload

**Optimizations:**
- Delta compression: send only changes → 60-80% reduction
- Quantization: float32 → int16 for positions → 50% reduction
- Interest management: only send nearby entities → 70% reduction
- Reduced tick rate for distant entities → further reduction

---

## 🔑 3. Mechanics

### Mechanic 3.1 — Reliable UDP

Games use UDP (no head-of-line blocking, no retransmission delay) but need reliability for some messages:

| Channel | Reliability | Ordering | Use Case |
|---------|------------|----------|----------|
| **Unreliable** | None | None | Position updates (stale data useless) |
| **Unreliable Sequenced** | None | Drop old | Rotation, animation state |
| **Reliable Unordered** | Retransmit | None | Chat, item pickup |
| **Reliable Ordered** | Retransmit | Strict | RPC calls, state changes |

Implement reliability on top of UDP with sequence numbers and ACK bitmasks.

### Mechanic 3.2 — Input Delay vs Rollback Trade-off

**Input delay** (add N frames of delay to local input):
- Pro: No mispredictions, no visual corrections
- Con: Feels sluggish (N × 16.67ms at 60 FPS)
- Best for: RTS, turn-based, high-latency scenarios

**Rollback** (predict and correct):
- Pro: Zero input latency for local player
- Con: Visual corrections ("teleporting") on misprediction
- Best for: Fighting games, fast-paced action, low-latency scenarios

**Hybrid:** Use 1-2 frames of input delay + rollback. Reduces misprediction frequency while keeping latency low.

### Mechanic 3.3 — Jitter Buffer

Network packets don't arrive at uniform intervals. A **jitter buffer** smooths this:

```
Packet arrival times: 16ms, 14ms, 22ms, 8ms, 35ms, 12ms
Without buffer: render stutters on late packets
With 50ms buffer: always have 2-3 packets queued, smooth playback
```

Trade-off: larger buffer = smoother but more latency.

---

## 💻 4. Code Patterns & Examples

### 26.1 C# — Client-Side Prediction with Reconciliation

```csharp
public class NetworkedPlayer : MonoBehaviour
{
    private Queue<InputPayload> pendingInputs = new();
    private int lastAcknowledgedInput = -1;
    private Vector3 serverPosition;
    
    struct InputPayload
    {
        public int sequenceNumber;
        public Vector2 moveDirection;
        public float deltaTime;
    }
    
    void Update()
    {
        if (!isLocalPlayer) return;
        
        // 1. Capture input
        var input = new InputPayload
        {
            sequenceNumber = nextSequence++,
            moveDirection = new Vector2(Input.GetAxis("Horizontal"), Input.GetAxis("Vertical")),
            deltaTime = Time.deltaTime
        };
        
        // 2. Apply locally (prediction)
        ApplyInput(input);
        
        // 3. Send to server
        pendingInputs.Enqueue(input);
        SendInputToServer(input);
    }
    
    // Called when server state arrives
    public void OnServerStateReceived(Vector3 pos, int lastProcessedInput)
    {
        serverPosition = pos;
        lastAcknowledgedInput = lastProcessedInput;
        
        // 4. Remove acknowledged inputs
        while (pendingInputs.Count > 0 && 
               pendingInputs.Peek().sequenceNumber <= lastAcknowledgedInput)
        {
            pendingInputs.Dequeue();
        }
        
        // 5. Reconciliation: if server disagrees, correct
        if (Vector3.Distance(transform.position, serverPosition) > 0.01f)
        {
            // Snap to server position
            transform.position = serverPosition;
            
            // Re-apply all unacknowledged inputs
            foreach (var input in pendingInputs)
            {
                ApplyInput(input);
            }
        }
    }
    
    private void ApplyInput(InputPayload input)
    {
        Vector3 move = new Vector3(input.moveDirection.x, 0, input.moveDirection.y);
        transform.position += move.normalized * moveSpeed * input.deltaTime;
    }
}
```

### 26.2 Python — Rollback Netcode Core

```python
from dataclasses import dataclass, field
from copy import deepcopy

@dataclass
class GameState:
    positions: dict[int, tuple[float, float]] = field(default_factory=dict)
    velocities: dict[int, tuple[float, float]] = field(default_factory=dict)

@dataclass
class Input:
    player_id: int
    frame: int
    dx: float
    dy: float

class RollbackNetcode:
    def __init__(self, num_players: int, max_rollback_frames: int = 8):
        self.num_players = num_players
        self.max_rollback = max_rollback_frames
        self.current_frame = 0
        
        # State history for rollback
        self.state_history: list[GameState] = []
        
        # Input history: frame → {player_id → Input}
        self.confirmed_inputs: dict[int, dict[int, Input]] = {}
        self.predicted_inputs: dict[int, dict[int, Input]] = {}
        
        # Current state
        self.state = GameState()
    
    def advance_frame(self, local_input: Input, remote_inputs: dict[int, Input]):
        """Advance simulation by one frame."""
        # Save state for potential rollback
        self.state_history.append(deepcopy(self.state))
        if len(self.state_history) > self.max_rollback:
            self.state_history.pop(0)
        
        # Store confirmed local input
        frame = self.current_frame
        if frame not in self.confirmed_inputs:
            self.confirmed_inputs[frame] = {}
        self.confirmed_inputs[frame][local_input.player_id] = local_input
        
        # For remote players: use confirmed if available, else predict
        all_inputs = {local_input.player_id: local_input}
        for pid in range(self.num_players):
            if pid == local_input.player_id:
                continue
            if pid in remote_inputs:
                all_inputs[pid] = remote_inputs[pid]
                self.confirmed_inputs.setdefault(frame, {})[pid] = remote_inputs[pid]
            else:
                # Predict: repeat last known input
                predicted = self._predict_input(pid, frame)
                all_inputs[pid] = predicted
                self.predicted_inputs.setdefault(frame, {})[pid] = predicted
        
        # Simulate
        self._simulate(self.state, all_inputs)
        self.current_frame += 1
    
    def on_remote_input_received(self, remote_input: Input):
        """Handle late-arriving remote input — may trigger rollback."""
        frame = remote_input.frame
        pid = remote_input.player_id
        
        # Check if we predicted this frame
        if frame in self.predicted_inputs and pid in self.predicted_inputs[frame]:
            predicted = self.predicted_inputs[frame][pid]
            
            if predicted.dx != remote_input.dx or predicted.dy != remote_input.dy:
                # Misprediction! Rollback and resimulate
                self._rollback(frame, remote_input)
    
    def _rollback(self, to_frame: int, corrected_input: Input):
        """Rollback to frame, apply correction, resimulate to present."""
        frames_back = self.current_frame - to_frame
        if frames_back > len(self.state_history):
            return  # Too far back, can't rollback
        
        # Restore old state
        self.state = deepcopy(self.state_history[-(frames_back)])
        
        # Update confirmed inputs
        self.confirmed_inputs.setdefault(to_frame, {})[corrected_input.player_id] = corrected_input
        
        # Resimulate from to_frame to current
        for f in range(to_frame, self.current_frame):
            inputs = self.confirmed_inputs.get(f, {})
            # Fill missing with predictions
            for pid in range(self.num_players):
                if pid not in inputs:
                    inputs[pid] = self._predict_input(pid, f)
            self._simulate(self.state, inputs)
    
    def _simulate(self, state: GameState, inputs: dict[int, Input]):
        """One frame of deterministic simulation."""
        speed = 5.0
        dt = 1.0 / 60.0
        for pid, inp in inputs.items():
            px, py = state.positions.get(pid, (0.0, 0.0))
            state.positions[pid] = (px + inp.dx * speed * dt, py + inp.dy * speed * dt)
    
    def _predict_input(self, player_id: int, frame: int) -> Input:
        """Predict: assume same input as last confirmed frame."""
        for f in range(frame - 1, max(frame - 10, -1), -1):
            if f in self.confirmed_inputs and player_id in self.confirmed_inputs[f]:
                last = self.confirmed_inputs[f][player_id]
                return Input(player_id, frame, last.dx, last.dy)
        return Input(player_id, frame, 0.0, 0.0)  # Default: no input
```

### 26.3 C++ — Snapshot Interpolation

```cpp
struct EntitySnapshot {
    uint32_t entityId;
    FVector Position;
    FQuat Rotation;
    float Timestamp;
};

struct WorldSnapshot {
    float serverTime;
    TArray<EntitySnapshot> entities;
};

class SnapshotInterpolator {
    static constexpr float INTERP_DELAY = 0.1f; // 100ms buffer
    TArray<WorldSnapshot> snapshotBuffer;
    
public:
    void OnSnapshotReceived(const WorldSnapshot& snapshot) {
        snapshotBuffer.Add(snapshot);
        // Keep last 2 seconds of snapshots
        while (snapshotBuffer.Num() > 40) // 20 Hz × 2s
            snapshotBuffer.RemoveAt(0);
    }
    
    EntitySnapshot InterpolateEntity(uint32_t entityId, float clientTime) {
        float renderTime = clientTime - INTERP_DELAY;
        
        // Find bracketing snapshots
        const WorldSnapshot* from = nullptr;
        const WorldSnapshot* to = nullptr;
        
        for (int i = 0; i < snapshotBuffer.Num() - 1; i++) {
            if (snapshotBuffer[i].serverTime <= renderTime &&
                snapshotBuffer[i + 1].serverTime >= renderTime) {
                from = &snapshotBuffer[i];
                to = &snapshotBuffer[i + 1];
                break;
            }
        }
        
        if (!from || !to) {
            // Extrapolate or use latest
            return GetLatestSnapshot(entityId);
        }
        
        // Interpolation factor
        float t = (renderTime - from->serverTime) / 
                  (to->serverTime - from->serverTime);
        t = FMath::Clamp(t, 0.f, 1.f);
        
        // Find entity in both snapshots
        auto fromEntity = FindEntity(*from, entityId);
        auto toEntity = FindEntity(*to, entityId);
        
        EntitySnapshot result;
        result.entityId = entityId;
        result.Position = FMath::Lerp(fromEntity.Position, toEntity.Position, t);
        result.Rotation = FQuat::Slerp(fromEntity.Rotation, toEntity.Rotation, t);
        return result;
    }
};
```

---

## 🧮 5. Worked Examples

### Example 26.6.1 — Calculate Required Bandwidth

**Problem:** A 10-player FPS sends snapshots at 20 Hz. Each player has: position (3×float32), rotation (4×float16), health (uint8), weapon_id (uint8), animation_state (uint8). Calculate server upload bandwidth with and without delta compression.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Per-entity payload:**
- Position: 3 × 4 bytes = 12 bytes
- Rotation (quaternion, half-precision): 4 × 2 bytes = 8 bytes
- Health: 1 byte
- Weapon ID: 1 byte
- Animation state: 1 byte
- **Total per entity: 23 bytes**

**Full snapshot (all 10 players):**
- 10 × 23 = 230 bytes payload
- Header (sequence, timestamp, ack): ~12 bytes
- UDP/IP overhead: 28 bytes
- **Total packet: 270 bytes**

**Server upload (to each client):**
- Each client receives snapshots of 9 other players (not self)
- 9 × 23 + 12 + 28 = 247 bytes per packet
- At 20 Hz: 247 × 20 = 4,940 bytes/s = **26.8 KB/s per client**
- 10 clients: 48 KB/s total server upload

**With delta compression:**
- Most frames, players barely move (< 1 unit)
- Delta: encode difference from previous snapshot
- Position delta fits in 3 × int16 = 6 bytes (vs 12)
- Rotation delta: 3 × int8 = 3 bytes (vs 8, small angle changes)
- Unchanged fields: 1 bit flag = skip
- **Average delta per entity: ~10 bytes** (57% reduction)
- Server upload: ~22 KB/s total

**With interest management (only nearby players):**
- Average visible players: 4 (of 9)
- Further 55% reduction: ~10 KB/s total

</details>

### Example 26.6.2 — Implement Lag Compensation for Shooting

**Problem:** Player A (100ms ping) shoots at Player B. By the time the server receives the shot, Player B has moved. How does the server determine if the shot hit?

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Server-side rewind algorithm:**

```
1. Player A fires at client time T_a
2. Packet arrives at server at time T_server = T_a + RTT/2
3. Server knows A's one-way latency: L_a = RTT_a / 2 = 50ms
4. Server rewinds world state to: T_server - L_a = what A saw when they fired
5. Perform raycast against rewound positions
6. If hit: apply damage at current time
7. If miss: inform A (no hit marker)
```

```csharp
public class LagCompensation
{
    // Store position history for all players
    private Dictionary<int, List<(float time, Vector3 pos, Collider hitbox)>> history = new();
    
    public bool ProcessShot(int shooterId, Vector3 origin, Vector3 direction, float clientTime)
    {
        float serverTime = NetworkTime.time;
        float shooterLatency = GetPlayerLatency(shooterId);
        float rewindTime = serverTime - shooterLatency;
        
        // Rewind all other players to what shooter saw
        var originalPositions = new Dictionary<int, Vector3>();
        foreach (var (playerId, positions) in history)
        {
            if (playerId == shooterId) continue;
            
            // Find position at rewind time (interpolate between samples)
            var rewoundPos = InterpolateHistory(positions, rewindTime);
            originalPositions[playerId] = GetPlayerTransform(playerId).position;
            GetPlayerTransform(playerId).position = rewoundPos;
        }
        
        // Perform raycast in rewound state
        bool hit = Physics.Raycast(origin, direction, out RaycastHit hitInfo, 100f);
        
        // Restore positions
        foreach (var (playerId, pos) in originalPositions)
            GetPlayerTransform(playerId).position = pos;
        
        return hit;
    }
}
```

**Trade-off:** Lag compensation makes shooting feel fair for the shooter but can feel unfair for the target ("I was behind cover!"). Most games accept this trade-off because the shooter's experience matters more for game feel.

</details>

---

## ⚠️ 6. Gotchas & Anti-Patterns

### ❌ Anti-Pattern: TCP for Real-Time Game State

TCP's head-of-line blocking means one lost packet delays ALL subsequent packets. A 50ms retransmission timeout at 60 FPS = 3 frames of stutter. Use UDP for game state, TCP only for non-time-critical data (chat, login).

### ❌ Anti-Pattern: Trusting the Client

```
// BAD: client says "I have 999 health"
// Server blindly accepts → cheating

// GOOD: server is authoritative
// Client sends inputs only, server simulates and validates
```

### ❌ Anti-Pattern: Sending Full State Every Frame

Delta compression reduces bandwidth 50-80%. Only send what changed since the last acknowledged snapshot.

### ❌ Anti-Pattern: No Packet Loss Handling

UDP packets WILL be lost (1-5% typical). Your netcode must handle:
- Missing snapshots (interpolate between available ones)
- Missing inputs (predict, then correct on arrival)
- Duplicate packets (sequence numbers for dedup)

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- **Previous:** [26.5 - Save Systems & Serialization](26.5---Save-Systems-&-Serialization)
- **Next:** [26.7 - Performance & Optimization](26.7---Performance-&-Optimization)
- **Network fundamentals:** [08.11 - Computer Networks Essentials](08.11---Computer-Networks-Essentials) — TCP/UDP, sockets
- **Serialization:** [26.5 - Save Systems & Serialization](26.5---Save-Systems-&-Serialization) — efficient data encoding
- **Determinism:** [26.1 - Game Loop & Architecture](26.1---Game-Loop-&-Architecture) — fixed timestep for lockstep

### External Resources
- **Gaffer On Games** (gafferongames.com) — Glenn Fiedler's definitive networking articles
- **GDC: "Overwatch Gameplay Architecture and Netcode"** — Blizzard's ECS + netcode
- **GDC: "It IS Rocket Science! The Physics of Rocket League"** — rollback in practice
- **GGPO** (ggpo.net) — open-source rollback netcode library
- **Valve Developer Wiki: "Source Multiplayer Networking"** — snapshot interpolation, lag compensation
- **Gabriel Gambetta: "Fast-Paced Multiplayer"** — interactive visual tutorials

### Practice
- `_practice/scripts/4.6_netcode_sim.py` — simulate latency, packet loss, and rollback



---

## 🔬 8. Advanced Topics — Rollback Netcode, Lag Compensation & Client Prediction

### 8.1 — Rollback Netcode (GGPO / Confirmed Frame) Full Pipeline

Rollback netcode eliminates input delay by **predicting** remote players' inputs and **rolling back** the simulation when predictions are wrong. This is the gold standard for fighting games and fast-paced competitive games.

#### Core Concept

Instead of waiting for remote inputs (adding latency), the game:
1. **Predicts** remote inputs (usually: "same as last frame")
2. **Simulates forward** immediately with predicted inputs
3. When actual remote inputs arrive, **compares** prediction to reality
4. If wrong: **rolls back** to the last confirmed frame, **re-simulates** forward with correct inputs

```csharp
public class RollbackNetcodeSystem
{
    private const int MAX_ROLLBACK_FRAMES = 8;  // Max frames we can roll back
    private const int INPUT_DELAY = 2;           // Local input delay (frames)
    
    // Ring buffer of game states for rollback
    private GameState[] stateBuffer = new GameState[MAX_ROLLBACK_FRAMES + 1];
    
    // Input history for all players
    private PlayerInput[,] inputHistory; // [frame, playerIndex]
    private bool[,] inputConfirmed;      // Has this input been confirmed by network?
    
    private int confirmedFrame = 0;      // Last frame where ALL inputs are confirmed
    private int currentFrame = 0;        // Current simulation frame (may be ahead)
    
    public void Update()
    {
        // 1. Read local input and send to remote
        PlayerInput localInput = ReadLocalInput();
        SendInputToRemote(localInput, currentFrame + INPUT_DELAY);
        
        // Store local input (confirmed immediately)
        inputHistory[currentFrame + INPUT_DELAY, localPlayerIndex] = localInput;
        inputConfirmed[currentFrame + INPUT_DELAY, localPlayerIndex] = true;
        
        // 2. Receive remote inputs
        ReceiveRemoteInputs();
        
        // 3. Check if we need to rollback
        int rollbackTo = FindEarliestMisprediction();
        
        if (rollbackTo >= 0 && rollbackTo < currentFrame)
        {
            // ROLLBACK: restore state and re-simulate
            Rollback(rollbackTo);
        }
        
        // 4. Advance simulation
        AdvanceFrame();
        
        // 5. Update confirmed frame
        UpdateConfirmedFrame();
    }
    
    private int FindEarliestMisprediction()
    {
        // Check all frames between confirmedFrame and currentFrame
        for (int f = confirmedFrame + 1; f <= currentFrame; f++)
        {
            for (int p = 0; p < playerCount; p++)
            {
                if (p == localPlayerIndex) continue;
                
                if (inputConfirmed[f, p] && 
                    inputHistory[f, p] != predictedInputs[f, p])
                {
                    return f; // Misprediction found at this frame
                }
            }
        }
        return -1; // No misprediction
    }
    
    private void Rollback(int targetFrame)
    {
        // Restore game state to the target frame
        GameState savedState = stateBuffer[targetFrame % stateBuffer.Length];
        RestoreGameState(savedState);
        
        // Re-simulate from targetFrame to currentFrame with corrected inputs
        int framesToResimulate = currentFrame - targetFrame;
        
        for (int f = targetFrame; f < currentFrame; f++)
        {
            // Use confirmed inputs where available, predictions otherwise
            PlayerInput[] frameInputs = GetBestInputsForFrame(f);
            SimulateFrame(frameInputs);
            
            // Save state for future rollbacks
            stateBuffer[(f + 1) % stateBuffer.Length] = CaptureGameState();
        }
    }
    
    private void AdvanceFrame()
    {
        // Predict remote inputs (default: repeat last known input)
        for (int p = 0; p < playerCount; p++)
        {
            if (p == localPlayerIndex) continue;
            
            if (!inputConfirmed[currentFrame + 1, p])
            {
                // Prediction: same as last confirmed input
                predictedInputs[currentFrame + 1, p] = GetLastConfirmedInput(p);
            }
        }
        
        PlayerInput[] inputs = GetBestInputsForFrame(currentFrame + 1);
        SimulateFrame(inputs);
        currentFrame++;
        
        // Save state
        stateBuffer[currentFrame % stateBuffer.Length] = CaptureGameState();
    }
    
    private void UpdateConfirmedFrame()
    {
        // Advance confirmed frame as far as all inputs are confirmed
        while (confirmedFrame < currentFrame)
        {
            int nextFrame = confirmedFrame + 1;
            bool allConfirmed = true;
            
            for (int p = 0; p < playerCount; p++)
            {
                if (!inputConfirmed[nextFrame, p])
                {
                    allConfirmed = false;
                    break;
                }
            }
            
            if (!allConfirmed) break;
            confirmedFrame = nextFrame;
        }
        
        // If we're too far ahead of confirmed frame, slow down
        // (prevents unbounded rollback depth)
        if (currentFrame - confirmedFrame >= MAX_ROLLBACK_FRAMES)
        {
            // Stall: don't advance until we get more confirmed inputs
            // This manifests as a brief freeze for the local player
        }
    }
}
```

#### Input Encoding for Network Transmission

```csharp
// Compact input encoding — minimize bandwidth
[Flags]
public enum InputFlags : ushort
{
    None = 0,
    Up = 1 << 0,
    Down = 1 << 1,
    Left = 1 << 2,
    Right = 1 << 3,
    Jump = 1 << 4,
    Attack = 1 << 5,
    Block = 1 << 6,
    Special1 = 1 << 7,
    Special2 = 1 << 8,
    // 7 bits remaining for future use
}

public struct NetworkInputPacket
{
    public uint frame;           // 4 bytes — which frame this input is for
    public InputFlags flags;     // 2 bytes — button states
    public byte analogX;         // 1 byte — analog stick X (0-255, 128 = center)
    public byte analogY;         // 1 byte — analog stick Y
    // Total: 8 bytes per input per frame
    
    // Send multiple frames in one packet (redundancy against packet loss)
    public static byte[] EncodePacket(NetworkInputPacket[] inputs)
    {
        // Header: count (1 byte) + inputs (8 bytes each)
        byte[] packet = new byte[1 + inputs.Length * 8];
        packet[0] = (byte)inputs.Length;
        
        for (int i = 0; i < inputs.Length; i++)
        {
            int offset = 1 + i * 8;
            BitConverter.GetBytes(inputs[i].frame).CopyTo(packet, offset);
            BitConverter.GetBytes((ushort)inputs[i].flags).CopyTo(packet, offset + 4);
            packet[offset + 6] = inputs[i].analogX;
            packet[offset + 7] = inputs[i].analogY;
        }
        
        return packet;
    }
}
```

#### Rollback-Friendly Game State Requirements

For rollback to work, the game state must be:
1. **Fully capturable:** Every piece of simulation state can be saved to a buffer
2. **Fully restorable:** State can be loaded from buffer, producing identical simulation
3. **Deterministic:** Same inputs + same state = same next state (no random without seeded RNG)
4. **Fast to copy:** State snapshot must complete in < 1ms (limits state size)

```csharp
// Example: compact game state for a fighting game
public struct FightingGameState
{
    // Per-player state (2 players)
    public PlayerState player1;
    public PlayerState player2;
    
    // Global state
    public int frameNumber;
    public uint rngSeed;  // Deterministic RNG state
    
    // Total size: ~256 bytes (fast to copy)
}

public struct PlayerState
{
    public Fixed16_16 posX, posY;     // Fixed-point position (deterministic)
    public Fixed16_16 velX, velY;     // Fixed-point velocity
    public short health;
    public short meter;
    public byte currentAnimation;
    public byte animationFrame;
    public byte hitstun;              // Frames of hitstun remaining
    public byte blockstun;
    public byte state;                // Standing, crouching, airborne, etc.
    public byte facingRight;          // 0 or 1
    // Pad to 32 bytes for alignment
}
```

---

### 8.2 — Lag Compensation & Rewind

In server-authoritative shooters, the server must compensate for network latency when validating hits. When a player fires, the server **rewinds** other players' positions to where they were when the shooter saw them.

```csharp
public class LagCompensationSystem
{
    // History buffer: store positions for the last N ticks
    private const int HISTORY_LENGTH = 32; // ~500ms at 64 tick
    
    private struct PositionRecord
    {
        public Vector3 position;
        public Quaternion rotation;
        public Bounds hitbox;
        public float timestamp;
    }
    
    // Per-entity position history
    private Dictionary<int, PositionRecord[]> entityHistory = new();
    
    // Called each server tick: record all entity positions
    public void RecordPositions(float serverTime)
    {
        int index = (int)(serverTime * tickRate) % HISTORY_LENGTH;
        
        foreach (var entity in allEntities)
        {
            entityHistory[entity.Id][index] = new PositionRecord
            {
                position = entity.Position,
                rotation = entity.Rotation,
                hitbox = entity.GetWorldHitbox(),
                timestamp = serverTime
            };
        }
    }
    
    // Validate a hit: rewind targets to where they were when shooter fired
    public HitResult ValidateShot(int shooterId, Vector3 shotOrigin, 
                                   Vector3 shotDirection, float clientTimestamp)
    {
        // 1. Calculate the server time when the client saw the world
        float clientRTT = GetPlayerRTT(shooterId);
        float rewindTime = clientTimestamp; // Client tells us when they fired
        
        // Clamp rewind to prevent abuse (max 250ms rewind)
        float maxRewind = 0.25f;
        float serverTime = GetServerTime();
        rewindTime = Mathf.Max(rewindTime, serverTime - maxRewind);
        
        // 2. Rewind all potential targets to that timestamp
        var rewindPositions = new Dictionary<int, PositionRecord>();
        
        foreach (var target in allEntities)
        {
            if (target.Id == shooterId) continue;
            rewindPositions[target.Id] = InterpolateHistory(target.Id, rewindTime);
        }
        
        // 3. Perform raycast against rewound hitboxes
        HitResult bestHit = null;
        float bestDistance = float.MaxValue;
        
        foreach (var (targetId, record) in rewindPositions)
        {
            if (RayIntersectsOBB(shotOrigin, shotDirection, record.hitbox, 
                                  record.position, record.rotation, out float dist))
            {
                if (dist < bestDistance)
                {
                    bestDistance = dist;
                    bestHit = new HitResult
                    {
                        targetId = targetId,
                        hitPoint = shotOrigin + shotDirection * dist,
                        distance = dist
                    };
                }
            }
        }
        
        return bestHit;
    }
    
    private PositionRecord InterpolateHistory(int entityId, float targetTime)
    {
        var history = entityHistory[entityId];
        
        // Find the two records bracketing targetTime
        PositionRecord before = default, after = default;
        bool found = false;
        
        for (int i = 0; i < HISTORY_LENGTH - 1; i++)
        {
            int idx = (currentIndex - i + HISTORY_LENGTH) % HISTORY_LENGTH;
            int prevIdx = (idx - 1 + HISTORY_LENGTH) % HISTORY_LENGTH;
            
            if (history[prevIdx].timestamp <= targetTime && 
                history[idx].timestamp >= targetTime)
            {
                before = history[prevIdx];
                after = history[idx];
                found = true;
                break;
            }
        }
        
        if (!found) return history[currentIndex]; // Fallback to latest
        
        // Interpolate between the two records
        float t = (targetTime - before.timestamp) / (after.timestamp - before.timestamp);
        return new PositionRecord
        {
            position = Vector3.Lerp(before.position, after.position, t),
            rotation = Quaternion.Slerp(before.rotation, after.rotation, t),
            timestamp = targetTime
        };
    }
}
```

---

### 8.3 — Client-Side Prediction & Server Reconciliation

The client predicts its own movement locally (zero latency feel) while the server remains authoritative. When the server's confirmed state differs from the client's prediction, the client corrects smoothly.

```csharp
public class ClientPrediction
{
    // Circular buffer of predicted states and the inputs that produced them
    private struct PredictionEntry
    {
        public uint tick;
        public PlayerInput input;
        public PlayerState predictedState;
    }
    
    private PredictionEntry[] predictionBuffer = new PredictionEntry[128];
    private uint lastConfirmedTick = 0;
    private PlayerState lastConfirmedState;
    
    // Called each client frame
    public PlayerState PredictMovement(PlayerInput input, uint currentTick)
    {
        // Store prediction
        int bufIdx = (int)(currentTick % predictionBuffer.Length);
        
        PlayerState predicted = SimulateMovement(GetCurrentState(), input);
        
        predictionBuffer[bufIdx] = new PredictionEntry
        {
            tick = currentTick,
            input = input,
            predictedState = predicted
        };
        
        return predicted; // Apply immediately to local player
    }
    
    // Called when server sends authoritative state
    public void OnServerStateReceived(uint serverTick, PlayerState serverState)
    {
        lastConfirmedTick = serverTick;
        lastConfirmedState = serverState;
        
        // Compare server state to what we predicted for that tick
        int bufIdx = (int)(serverTick % predictionBuffer.Length);
        PlayerState ourPrediction = predictionBuffer[bufIdx].predictedState;
        
        float posError = Vector3.Distance(serverState.position, ourPrediction.position);
        
        if (posError > RECONCILIATION_THRESHOLD) // e.g., 0.01 units
        {
            // Misprediction! Reconcile.
            Reconcile(serverTick, serverState);
        }
    }
    
    private void Reconcile(uint fromTick, PlayerState correctState)
    {
        // Start from the server's confirmed state
        PlayerState state = correctState;
        
        // Re-simulate all ticks from fromTick to current tick using stored inputs
        uint currentTick = GetCurrentTick();
        
        for (uint tick = fromTick + 1; tick <= currentTick; tick++)
        {
            int bufIdx = (int)(tick % predictionBuffer.Length);
            PlayerInput input = predictionBuffer[bufIdx].input;
            
            state = SimulateMovement(state, input);
            
            // Update prediction buffer with corrected state
            predictionBuffer[bufIdx].predictedState = state;
        }
        
        // Apply corrected state (optionally smooth over a few frames to avoid snap)
        ApplyCorrectedState(state);
    }
    
    // Smooth correction to avoid visual snapping
    private Vector3 correctionOffset = Vector3.zero;
    
    private void ApplyCorrectedState(PlayerState corrected)
    {
        Vector3 currentVisual = GetCurrentVisualPosition();
        Vector3 correctedPos = corrected.position;
        
        // Instead of snapping, store the offset and lerp it to zero
        correctionOffset = currentVisual - correctedPos;
        
        // Over the next N frames, reduce correctionOffset to zero
        // Visual position = actual position + correctionOffset
        // This produces smooth correction without jarring snaps
    }
    
    void LateUpdate()
    {
        // Decay correction offset
        correctionOffset = Vector3.Lerp(correctionOffset, Vector3.zero, 
                                         Time.deltaTime * CORRECTION_SPEED);
        
        // Visual position = simulation position + smoothing offset
        transform.position = simulationPosition + correctionOffset;
    }
}
```

---

## 📎 9. Appendix — Mathematical Foundations

### Appendix 9.A — Network Topology Tradeoffs: Relay vs. P2P vs. Dedicated Server

#### Peer-to-Peer (Full Mesh)

Each player connects directly to every other player.

**Connection count:** $\frac{N(N-1)}{2}$ for $N$ players.

**Latency between players $i$ and $j$:** Direct RTT $= L_{ij}$

**Bandwidth per player:** Must send input to $N-1$ peers and receive from $N-1$ peers.

$$
\text{BW}_{player} = (N-1) \cdot \text{input\_size} \cdot \text{tick\_rate}
$$

**Advantages:** Lowest possible latency (direct path), no server cost.
**Disadvantages:** NAT traversal required, scales poorly ($O(N^2)$ connections), cheating easy (each client has full state), one player's bad connection affects everyone.

**Best for:** 2-player fighting games, small co-op (2-4 players).

#### Client-Server (Dedicated)

One authoritative server, all clients connect to it.

**Connection count:** $N$ (one per client).

**Latency for player $i$'s action to reach player $j$:** $L_i + L_j$ (through server).

**Server bandwidth:**

$$
\text{BW}_{server} = N \cdot \text{state\_size} \cdot \text{tick\_rate}
$$

**Advantages:** Authoritative (anti-cheat), scales linearly, one bad client doesn't affect others, consistent experience.
**Disadvantages:** Server cost, added latency (client→server→client), single point of failure.

**Best for:** Competitive FPS (CS2, Valorant), MMOs, any game where cheating matters.

#### Relay Server

Clients connect to a relay that forwards packets without simulation. Combines P2P latency characteristics with NAT traversal simplicity.

**Latency:** $L_i + L_j$ (similar to dedicated, but no processing delay).

**Advantages:** No NAT issues, simple server (just forwards packets), clients still simulate.
**Disadvantages:** Still requires server infrastructure, no authority (cheating possible), relay adds small latency vs. direct P2P.

**Best for:** Casual multiplayer, games where latency matters but cheating doesn't (co-op PvE).

#### Comparison Matrix

| Aspect | P2P (Full Mesh) | Dedicated Server | Relay |
|--------|-----------------|-----------------|-------|
| Min latency | $L_{ij}$ (direct) | $L_i + L_j$ | $L_i + L_j + \epsilon$ |
| Authority | None (trust all) | Server | None |
| Anti-cheat | ❌ | ✅ | ❌ |
| NAT traversal | Required (STUN/TURN) | Not needed (server has public IP) | Not needed |
| Server cost | $0 | $$$ (compute + bandwidth) | $ (bandwidth only) |
| Max players | 4-8 (practical) | 64-128+ | 8-16 |
| Scalability | $O(N^2)$ | $O(N)$ | $O(N)$ |

---

### Appendix 9.B — Deterministic vs. Snapshot Synchronization

Two fundamental approaches to keeping multiple game instances in sync:

#### Deterministic Lockstep

**Principle:** All clients run the same simulation. Only **inputs** are transmitted. If the simulation is deterministic, all clients will compute identical states.

**Data transmitted per frame:**

$$
\text{bandwidth} = N_{players} \cdot \text{input\_size} \cdot \text{tick\_rate}
$$

For a fighting game: $2 \times 8 \text{ bytes} \times 60 \text{ Hz} = 960 \text{ bytes/sec}$ — trivial.

**Requirements:**
- Perfectly deterministic simulation (fixed-point math, deterministic iteration order)
- All clients must simulate at the same rate
- Input delay = network RTT (or rollback to hide it)
- Desync detection via periodic state checksums

**Advantages:**
- Minimal bandwidth (only inputs)
- Scales to many entities (RTS with 1000 units — only player commands sent)
- Replays are trivial (just store inputs)

**Disadvantages:**
- Determinism is HARD (floating-point, hash maps, multithreading all break it)
- Late joiners must simulate from frame 0 (or receive full state snapshot)
- One desync = game over (no recovery without full state transfer)

#### Snapshot Interpolation

**Principle:** The server simulates authoritatively and broadcasts **state snapshots** to all clients. Clients interpolate between received snapshots for smooth visuals.

**Data transmitted per snapshot:**

$$
\text{bandwidth} = N_{entities} \cdot \text{entity\_state\_size} \cdot \text{snapshot\_rate}
$$

For an FPS with 20 players: $20 \times 48 \text{ bytes} \times 20 \text{ Hz} = 19.2 \text{ KB/sec}$ per client.

**Delta Compression:** Only send what changed since the last acknowledged snapshot:

$$
\text{delta\_size} = \sum_{i \in \text{changed}} \text{size}(entity_i)
$$

Typically reduces bandwidth by 50-80%.

**Client-Side Interpolation:**

Clients render the world at a time slightly in the past (interpolation delay, typically 2-3 snapshots behind):

$$
t_{render} = t_{current} - \text{interp\_delay}
$$

$$
\text{state}_{render} = \text{lerp}(\text{snapshot}_{k}, \text{snapshot}_{k+1}, \alpha)
$$

where $\alpha = \frac{t_{render} - t_k}{t_{k+1} - t_k}$

**Advantages:**
- No determinism requirement (server is authoritative)
- Late joiners get current state immediately
- Robust to desyncs (server always correct)
- Works with non-deterministic systems (floating-point, random events)

**Disadvantages:**
- Higher bandwidth (full state vs. just inputs)
- Interpolation adds visual latency
- Scales poorly with entity count (1000 entities × 48 bytes × 20 Hz = 960 KB/sec)

#### Decision Guide

| Game Type | Recommended Approach |
|-----------|---------------------|
| Fighting games (2P) | Deterministic + Rollback (GGPO) |
| RTS (many units, few players) | Deterministic Lockstep |
| FPS (few players, fast action) | Snapshot + Client Prediction + Lag Compensation |
| MMO (many players, large world) | Snapshot + Interest Management (only send nearby entities) |
| Turn-based | Either (latency doesn't matter) |
| Racing | Snapshot + Extrapolation (predict forward for smooth visuals) |

---

