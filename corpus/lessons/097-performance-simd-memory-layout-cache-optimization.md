---
title: "09.7 — Performance: SIMD, Memory Layout & Cache Optimization"
subject: "C++"
catalog: advanced
audience_tier: higher-education
chapter: "9.7"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | [LEARNING_PATH](LEARNING_PATH) | Part of [09 - Learning Index](09---Learning-Index)*

# 09.7 — Performance: SIMD, Memory Layout & Cache Optimization

> *"The cheapest, fastest, and most reliable components of a computer system are those that aren't there."* — Gordon Bell

> *"Low-level programming is good for the programmer's soul."* — John Carmack

Performance in C++ isn't about micro-optimizing individual lines — it's about understanding how your data flows through the hardware. A cache miss costs 100+ cycles. A branch misprediction costs 15+ cycles. SIMD processes 4–16 elements in the time of one. This chapter teaches you to think like the hardware.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Explain the memory hierarchy (registers → L1 → L2 → L3 → RAM) and its performance implications.
2. Design cache-friendly data layouts (SoA vs AoS, hot/cold splitting).
3. Use SIMD intrinsics and compiler auto-vectorization for data-parallel computation.
4. Profile code with perf, VTune, or Tracy and identify bottlenecks.
5. Apply `constexpr` and `consteval` to move computation to compile time.
6. Avoid common performance anti-patterns (virtual calls in hot loops, cache thrashing, false sharing).

---

## 🖼️ Visual Anchor — Memory Hierarchy & Data Layout

![cpp__2.7-fig1](cpp__2.7-fig1.svg)

---

## 📚 1. Concepts & Definitions

### Definition 09.7.1 — The Memory Hierarchy

| Level | Size | Latency | Bandwidth |
|-------|------|---------|-----------|
| Registers | ~1 KB | 0 cycles | — |
| L1 Cache | 32–64 KB | ~4 cycles | ~1 TB/s |
| L2 Cache | 256 KB–1 MB | ~12 cycles | ~500 GB/s |
| L3 Cache | 4–64 MB | ~40 cycles | ~200 GB/s |
| RAM (DDR5) | 16–128 GB | ~100 cycles | ~50 GB/s |
| SSD | 1–4 TB | ~10,000 cycles | ~7 GB/s |

**Key insight:** L1 cache is ~25x faster than RAM. Your #1 optimization goal is keeping hot data in cache.

### Definition 09.7.2 — Cache Lines

Memory is loaded in **cache lines** (typically 64 bytes). When you access one byte, the CPU loads the entire 64-byte line. This means:

- Sequential access is fast (prefetcher predicts next line)
- Random access is slow (each access may miss cache)
- Small, contiguous data structures win

```cpp
// FAST: Sequential access (prefetcher loves this)
std::vector<float> positions(10000);
for (float& p : positions) p += 1.0f;  // ~1 cycle per element

// SLOW: Random access (cache miss per access)
std::vector<float*> pointers(10000);  // Pointers to scattered heap locations
for (float* p : pointers) *p += 1.0f;  // ~100 cycles per element
```

### Definition 09.7.3 — AoS vs SoA

**Array of Structures (AoS):** Traditional OOP layout.
**Structure of Arrays (SoA):** Data-oriented layout.

```cpp
// AoS — each entity is a contiguous block
struct Entity_AoS {
    Vec3 position;    // 12 bytes
    Vec3 velocity;    // 12 bytes
    float health;     // 4 bytes
    uint32_t flags;   // 4 bytes
    std::string name; // 32 bytes (!)
};  // 64 bytes per entity

std::vector<Entity_AoS> entities(10000);
// Updating positions loads ALL fields into cache (wastes bandwidth)

// SoA — each field is a contiguous array
struct Entities_SoA {
    std::vector<Vec3> positions;     // All positions contiguous
    std::vector<Vec3> velocities;    // All velocities contiguous
    std::vector<float> healths;
    std::vector<uint32_t> flags;
    std::vector<std::string> names;  // Cold data, rarely accessed
};
// Updating positions only loads positions + velocities (cache-efficient)
```

### Definition 09.7.4 — SIMD (Single Instruction, Multiple Data)

SIMD processes multiple data elements with a single instruction:

| ISA | Register Width | Floats per Op | Available On |
|-----|---------------|---------------|-------------|
| SSE | 128-bit | 4 × float | All x86-64 |
| AVX2 | 256-bit | 8 × float | Most modern x86 |
| AVX-512 | 512-bit | 16 × float | Server CPUs, some desktop |
| NEON | 128-bit | 4 × float | All ARM (Apple Silicon, mobile) |

```cpp
// Scalar: 1 add per cycle
for (int i = 0; i < N; ++i) c[i] = a[i] + b[i];

// SIMD (AVX2): 8 adds per cycle
for (int i = 0; i < N; i += 8) {
    __m256 va = _mm256_load_ps(&a[i]);
    __m256 vb = _mm256_load_ps(&b[i]);
    __m256 vc = _mm256_add_ps(va, vb);
    _mm256_store_ps(&c[i], vc);
}
```

### Definition 09.7.5 — Branch Prediction

Modern CPUs predict which way branches will go. Mispredictions cost ~15 cycles:

```cpp
// UNPREDICTABLE branch (50/50 random) — slow
for (int x : data) {
    if (x > threshold) sum += x;  // Mispredicts ~50% of the time
}

// FIX: Sort data first (branch becomes predictable)
std::sort(data.begin(), data.end());
for (int x : data) {
    if (x > threshold) sum += x;  // Always false, then always true
}

// BETTER FIX: Branchless (SIMD or arithmetic)
for (int x : data) {
    sum += x * (x > threshold);  // No branch at all
}
```

---

## 🧩 2. Mental Models

### Model 2.7.1 — "The Warehouse Analogy"

Think of memory as a warehouse:
- **Registers** = items in your hands (instant access)
- **L1 cache** = items on your desk (reach over)
- **L2 cache** = items on the shelf behind you (turn around)
- **L3 cache** = items in the same room (walk a few steps)
- **RAM** = items in the warehouse (walk to the back)
- **Disk** = items in another building (drive there)

Your goal: keep the items you need on your desk. The CPU's prefetcher is like an assistant who watches what you're grabbing and pre-fetches the next items — but only if your access pattern is predictable (sequential).

### Model 2.7.2 — "Optimize for the Common Case"

Profile first, optimize second. The 90/10 rule: 90% of execution time is spent in 10% of the code. Find that 10% with a profiler, then:

1. **Algorithmic improvement** (O(n²) → O(n log n)) — biggest wins
2. **Data layout** (cache-friendly structures) — 2–10x improvement
3. **SIMD** — 4–16x for data-parallel code
4. **Micro-optimization** (branchless, instruction scheduling) — 10–50% improvement

### Model 2.7.3 — "Hot/Cold Data Splitting"

Separate frequently-accessed ("hot") data from rarely-accessed ("cold") data:

```cpp
// BAD: Cold data pollutes cache lines with hot data
struct Entity {
    Vec3 position;       // Hot: accessed every frame
    Vec3 velocity;       // Hot: accessed every frame
    std::string name;    // Cold: accessed only in UI
    std::string model;   // Cold: accessed only on spawn
    int creation_time;   // Cold: accessed only in debug
};

// GOOD: Split hot and cold
struct EntityHot {
    Vec3 position;
    Vec3 velocity;
    uint32_t cold_index;  // Index into cold storage
};

struct EntityCold {
    std::string name;
    std::string model;
    int creation_time;
};

std::vector<EntityHot> hot_data;   // Tight loop iterates this
std::vector<EntityCold> cold_data; // Accessed only when needed
```

---

## 🔑 3. Mechanics

### 3.1 — Compiler Auto-Vectorization

The compiler can auto-vectorize simple loops if you help it:

```cpp
// Compiler WILL auto-vectorize this (simple, no dependencies):
void add_arrays(float* __restrict__ dst,
                const float* __restrict__ a,
                const float* __restrict__ b, size_t n) {
    for (size_t i = 0; i < n; ++i) {
        dst[i] = a[i] + b[i];
    }
}
// __restrict__ tells compiler pointers don't alias (critical for vectorization)

// Compiler will NOT auto-vectorize this (loop-carried dependency):
void running_sum(float* data, size_t n) {
    for (size_t i = 1; i < n; ++i) {
        data[i] += data[i - 1];  // Each iteration depends on previous
    }
}

// Check vectorization with compiler flags:
// GCC/Clang: -O2 -ftree-vectorize -fopt-info-vec-optimized
// MSVC: /O2 /Qvec-report:2
```

### 3.2 — Manual SIMD with Intrinsics

```cpp
#include <immintrin.h>  // AVX2 intrinsics

// Dot product of two float arrays (AVX2 — 8 floats at a time)
float dot_product_avx2(const float* a, const float* b, size_t n) {
    __m256 sum = _mm256_setzero_ps();

    size_t i = 0;
    for (; i + 8 <= n; i += 8) {
        __m256 va = _mm256_loadu_ps(&a[i]);
        __m256 vb = _mm256_loadu_ps(&b[i]);
        sum = _mm256_fmadd_ps(va, vb, sum);  // sum += a * b (fused multiply-add)
    }

    // Horizontal sum of 8 floats in sum register
    __m128 hi = _mm256_extractf128_ps(sum, 1);
    __m128 lo = _mm256_castps256_ps128(sum);
    __m128 s = _mm_add_ps(hi, lo);
    s = _mm_hadd_ps(s, s);
    s = _mm_hadd_ps(s, s);
    float result = _mm_cvtss_f32(s);

    // Handle remaining elements
    for (; i < n; ++i) result += a[i] * b[i];
    return result;
}
```

### 3.3 — `constexpr` and Compile-Time Computation

```cpp
// Move computation to compile time — zero runtime cost
constexpr int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i) result *= i;
    return result;
}

constexpr int fact_10 = factorial(10);  // Computed at compile time: 3628800

// Compile-time lookup tables
constexpr auto make_sin_table() {
    std::array<float, 360> table{};
    for (int i = 0; i < 360; ++i) {
        table[i] = static_cast<float>(
            std::sin(i * 3.14159265358979 / 180.0));
    }
    return table;
}
constexpr auto sin_table = make_sin_table();  // Embedded in binary, zero runtime cost

// consteval (C++20): MUST be compile-time
consteval int compile_time_only(int x) { return x * x; }
// compile_time_only(runtime_var);  // ERROR: must be constexpr argument
```

### 3.4 — Profiling with perf and Tracy

```bash
# Linux: perf stat (high-level counters)
perf stat ./my_game
# Shows: cycles, instructions, cache-misses, branch-misses

# Linux: perf record + report (sampling profiler)
perf record -g ./my_game
perf report  # Interactive flamegraph

# Cross-platform: Tracy profiler (game-industry standard)
# Add to code:
#include <tracy/Tracy.hpp>

void update_physics() {
    ZoneScoped;  // Tracy: marks this function for profiling
    for (auto& entity : entities) {
        ZoneScopedN("entity_update");
        entity.update(dt);
    }
}
```

### 3.5 — Benchmarking with Google Benchmark

```cpp
#include <benchmark/benchmark.h>

static void BM_VectorPushBack(benchmark::State& state) {
    for (auto _ : state) {
        std::vector<int> v;
        for (int i = 0; i < state.range(0); ++i) {
            v.push_back(i);
        }
        benchmark::DoNotOptimize(v.data());
    }
}
BENCHMARK(BM_VectorPushBack)->Range(8, 1 << 20);

static void BM_VectorReserved(benchmark::State& state) {
    for (auto _ : state) {
        std::vector<int> v;
        v.reserve(state.range(0));
        for (int i = 0; i < state.range(0); ++i) {
            v.push_back(i);
        }
        benchmark::DoNotOptimize(v.data());
    }
}
BENCHMARK(BM_VectorReserved)->Range(8, 1 << 20);

BENCHMARK_MAIN();
```


---

## ✍️ 4. Worked Examples

### Example 09.7.1 — AoS vs SoA Performance Comparison

<details>
<summary>Measure the cache performance difference between AoS and SoA layouts</summary>

```cpp
#include <vector>
#include <chrono>
#include <fmt/core.h>

// AoS layout
struct ParticleAoS {
    float x, y, z;       // Position
    float vx, vy, vz;   // Velocity
    float r, g, b, a;   // Color (cold — not used in physics)
    float lifetime;      // Cold
    uint32_t flags;      // Cold
};

// SoA layout
struct ParticlesSoA {
    std::vector<float> x, y, z;
    std::vector<float> vx, vy, vz;
    // Cold data separate:
    std::vector<float> r, g, b, a;
    std::vector<float> lifetime;
    std::vector<uint32_t> flags;

    void resize(size_t n) {
        x.resize(n); y.resize(n); z.resize(n);
        vx.resize(n); vy.resize(n); vz.resize(n);
        r.resize(n); g.resize(n); b.resize(n); a.resize(n);
        lifetime.resize(n); flags.resize(n);
    }
};

void update_aos(std::vector<ParticleAoS>& particles, float dt) {
    for (auto& p : particles) {
        p.x += p.vx * dt;  // Loads entire 48-byte struct into cache
        p.y += p.vy * dt;  // Even though we only need 24 bytes
        p.z += p.vz * dt;
    }
}

void update_soa(ParticlesSoA& p, float dt) {
    const size_t n = p.x.size();
    for (size_t i = 0; i < n; ++i) {
        p.x[i] += p.vx[i] * dt;  // Only position + velocity in cache
        p.y[i] += p.vy[i] * dt;  // Auto-vectorizes beautifully
        p.z[i] += p.vz[i] * dt;
    }
}

// Typical result with 1M particles:
// AoS: 4.2 ms per frame
// SoA: 0.8 ms per frame (5x faster — cache efficiency + auto-vectorization)
```

</details>

### Example 09.7.2 — Branchless Min/Max and Clamping

<details>
<summary>Eliminate branches in hot-path math operations</summary>

```cpp
#include <immintrin.h>

// Scalar branchless clamp
inline float clamp_branchless(float x, float lo, float hi) {
    // Uses conditional moves (cmov) — no branch prediction needed
    x = x < lo ? lo : x;
    x = x > hi ? hi : x;
    return x;
    // Compiler generates: vmaxss + vminss (branchless SSE instructions)
}

// SIMD clamp (8 floats at once)
inline __m256 clamp_avx2(__m256 x, __m256 lo, __m256 hi) {
    return _mm256_min_ps(_mm256_max_ps(x, lo), hi);
}

// Branchless absolute value
inline float abs_branchless(float x) {
    // Clear sign bit with bitwise AND
    uint32_t bits;
    std::memcpy(&bits, &x, 4);
    bits &= 0x7FFFFFFF;
    std::memcpy(&x, &bits, 4);
    return x;
}

// Branchless selection (like ternary but no branch)
inline int select(bool condition, int a, int b) {
    return b + (a - b) * condition;  // condition is 0 or 1
}
```

</details>

### Example 09.7.3 — Memory Pool Allocator

<details>
<summary>Build a fixed-size pool allocator for game entities</summary>

```cpp
#include <array>
#include <cstddef>
#include <cassert>

template<typename T, size_t PoolSize>
class PoolAllocator {
    union Slot {
        T object;
        Slot* next_free;
        Slot() {}
        ~Slot() {}
    };

    std::array<Slot, PoolSize> pool_;
    Slot* free_list_ = nullptr;
    size_t allocated_ = 0;

public:
    PoolAllocator() {
        // Build free list
        for (size_t i = 0; i < PoolSize - 1; ++i) {
            pool_[i].next_free = &pool_[i + 1];
        }
        pool_[PoolSize - 1].next_free = nullptr;
        free_list_ = &pool_[0];
    }

    template<typename... Args>
    T* allocate(Args&&... args) {
        assert(free_list_ && "Pool exhausted");
        Slot* slot = free_list_;
        free_list_ = slot->next_free;
        ++allocated_;
        return new (&slot->object) T(std::forward<Args>(args)...);
    }

    void deallocate(T* ptr) {
        ptr->~T();
        auto* slot = reinterpret_cast<Slot*>(ptr);
        slot->next_free = free_list_;
        free_list_ = slot;
        --allocated_;
    }

    size_t allocated() const { return allocated_; }
    size_t capacity() const { return PoolSize; }
};

// Usage: O(1) allocation, zero fragmentation, cache-friendly
PoolAllocator<Bullet, 4096> bullet_pool;
auto* b = bullet_pool.allocate(position, velocity, damage);
// ... use bullet ...
bullet_pool.deallocate(b);
```

</details>

---

## 💻 5. Code Patterns & Idioms

### Pattern 2.7.1 — Prefetching Hints

```cpp
#include <xmmintrin.h>  // _mm_prefetch

void process_with_prefetch(const float* data, size_t n) {
    constexpr size_t PREFETCH_DISTANCE = 16;  // 16 floats = 1 cache line ahead

    for (size_t i = 0; i < n; ++i) {
        // Tell CPU to load data[i + 16] into L1 cache now
        if (i + PREFETCH_DISTANCE < n) {
            _mm_prefetch(&data[i + PREFETCH_DISTANCE], _MM_HINT_T0);
        }
        process(data[i]);
    }
}
```

### Pattern 2.7.2 — Compile-Time Dispatch with `if constexpr`

```cpp
template<bool UseSIMD>
void update_positions(float* x, float* y, const float* vx, const float* vy,
                      float dt, size_t n) {
    if constexpr (UseSIMD) {
        __m256 vdt = _mm256_set1_ps(dt);
        for (size_t i = 0; i < n; i += 8) {
            __m256 px = _mm256_load_ps(&x[i]);
            __m256 py = _mm256_load_ps(&y[i]);
            __m256 dx = _mm256_load_ps(&vx[i]);
            __m256 dy = _mm256_load_ps(&vy[i]);
            _mm256_store_ps(&x[i], _mm256_fmadd_ps(dx, vdt, px));
            _mm256_store_ps(&y[i], _mm256_fmadd_ps(dy, vdt, py));
        }
    } else {
        for (size_t i = 0; i < n; ++i) {
            x[i] += vx[i] * dt;
            y[i] += vy[i] * dt;
        }
    }
}
```

---

## ⚠️ 6. Gotchas & Anti-Patterns

### Gotcha 2.7.1 — Premature Optimization

```cpp
// DON'T: Optimize without profiling
// "I'll use a linked list because insert is O(1)"
std::list<Entity> entities;  // Cache-hostile! Every node is a separate allocation

// DO: Profile first, then optimize the actual bottleneck
std::vector<Entity> entities;  // Almost always faster due to cache locality
// Even O(n) operations on vector beat O(1) on list for n < 10000
```

### Gotcha 2.7.2 — Virtual Calls in Hot Loops

```cpp
// SLOW: Virtual dispatch in tight loop (indirect call + possible cache miss)
for (auto& entity : entities) {
    entity->update(dt);  // vtable lookup every iteration
}

// FAST: Sort by type, batch process (or use SoA + no virtuals)
for (auto& enemy : enemies) enemy.update(dt);    // Direct call, inlineable
for (auto& bullet : bullets) bullet.update(dt);  // Direct call, inlineable
```

### Gotcha 2.7.3 — Unaligned SIMD Access

```cpp
// CRASH or SLOW: Unaligned load with aligned instruction
float data[100];  // May not be 32-byte aligned
__m256 v = _mm256_load_ps(data);  // Requires 32-byte alignment!

// FIX: Use unaligned load (slightly slower but safe)
__m256 v = _mm256_loadu_ps(data);

// BEST: Align your data
alignas(32) float data[100];  // Guaranteed 32-byte aligned
__m256 v = _mm256_load_ps(data);  // Fast aligned load
```

### Gotcha 2.7.4 — Benchmarking Optimized-Away Code

```cpp
// BUG: Compiler removes the entire loop (result unused)
for (int i = 0; i < 1000000; ++i) {
    int result = expensive_computation(i);
}

// FIX: Use benchmark::DoNotOptimize or volatile
for (int i = 0; i < 1000000; ++i) {
    int result = expensive_computation(i);
    benchmark::DoNotOptimize(result);  // Prevents dead code elimination
}
```

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- **Previous:** [09.6 - Concurrency - Threads, Atomics, std__async, Coroutines](09.6---Concurrency---Threads,-Atomics,-std__async,-Coroutines)
- **Next:** [09.8 - Game Dev with C++ - Unreal Engine & Custom Engine Patterns](09.8---Game-Dev-with-C++---Unreal-Engine-&-Custom-Engine-Patterns)
- **CPU architecture:** [1.12 - Computer Architecture & How Code Becomes Execution](1.12---Computer-Architecture-&-How-Code-Becomes-Execution)
- **Game engine data patterns:** [09.8 - Game Dev with C++ - Unreal Engine & Custom Engine Patterns](09.8---Game-Dev-with-C++---Unreal-Engine-&-Custom-Engine-Patterns)
- **False sharing (concurrency):** [09.6 - Concurrency - Threads, Atomics, std__async, Coroutines](09.6---Concurrency---Threads,-Atomics,-std__async,-Coroutines)

### External Resources
- [What Every Programmer Should Know About Memory (Drepper)](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf)
- [Data-Oriented Design (Richard Fabian)](https://www.dataorienteddesign.com/dodbook/)
- [Agner Fog's Optimization Manuals](https://www.agner.org/optimize/)
- [CppCon: "Data-Oriented Design in C++"](https://www.youtube.com/results?search_query=cppcon+data+oriented+design)
- [Compiler Explorer](https://godbolt.org) — Verify vectorization and assembly output
- [Intel Intrinsics Guide](https://www.intel.com/content/www/us/en/docs/intrinsics-guide/index.html)
- [Tracy Profiler](https://github.com/wolfpld/tracy)

---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — AVX2 SIMD: Processing 8 Floats Simultaneously

**Problem:** Implement a particle position update that processes 8 particles per instruction using AVX2 intrinsics. Compare with scalar code and auto-vectorized code.

<details>
<summary>🔍 Full step-by-step solution</summary>

```cpp
#include <immintrin.h>  // AVX2 intrinsics
#include <vector>
#include <chrono>
#include <cassert>
#include <fmt/core.h>

// SoA layout for SIMD-friendly access
struct ParticleSystem {
    std::vector<float> pos_x, pos_y, pos_z;
    std::vector<float> vel_x, vel_y, vel_z;
    std::vector<float> acc_x, acc_y, acc_z;
    size_t count;

    void resize(size_t n) {
        // Ensure 32-byte alignment for AVX2
        count = (n + 7) & ~7;  // Round up to multiple of 8
        pos_x.resize(count); pos_y.resize(count); pos_z.resize(count);
        vel_x.resize(count); vel_y.resize(count); vel_z.resize(count);
        acc_x.resize(count); acc_y.resize(count); acc_z.resize(count);
    }
};

// Version 1: Scalar (baseline)
void update_scalar(ParticleSystem& ps, float dt) {
    for (size_t i = 0; i < ps.count; ++i) {
        ps.vel_x[i] += ps.acc_x[i] * dt;
        ps.vel_y[i] += ps.acc_y[i] * dt;
        ps.vel_z[i] += ps.acc_z[i] * dt;
        ps.pos_x[i] += ps.vel_x[i] * dt;
        ps.pos_y[i] += ps.vel_y[i] * dt;
        ps.pos_z[i] += ps.vel_z[i] * dt;
    }
}

// Version 2: AVX2 intrinsics (8 particles per iteration)
void update_avx2(ParticleSystem& ps, float dt) {
    __m256 vdt = _mm256_set1_ps(dt);  // Broadcast dt to all 8 lanes
    size_t n = ps.count;

    for (size_t i = 0; i < n; i += 8) {
        // Load 8 velocities and 8 accelerations
        __m256 vx = _mm256_loadu_ps(&ps.vel_x[i]);
        __m256 vy = _mm256_loadu_ps(&ps.vel_y[i]);
        __m256 vz = _mm256_loadu_ps(&ps.vel_z[i]);
        __m256 ax = _mm256_loadu_ps(&ps.acc_x[i]);
        __m256 ay = _mm256_loadu_ps(&ps.acc_y[i]);
        __m256 az = _mm256_loadu_ps(&ps.acc_z[i]);

        // vel += acc * dt (FMA: fused multiply-add, single instruction)
        vx = _mm256_fmadd_ps(ax, vdt, vx);
        vy = _mm256_fmadd_ps(ay, vdt, vy);
        vz = _mm256_fmadd_ps(az, vdt, vz);

        // Store updated velocities
        _mm256_storeu_ps(&ps.vel_x[i], vx);
        _mm256_storeu_ps(&ps.vel_y[i], vy);
        _mm256_storeu_ps(&ps.vel_z[i], vz);

        // Load positions
        __m256 px = _mm256_loadu_ps(&ps.pos_x[i]);
        __m256 py = _mm256_loadu_ps(&ps.pos_y[i]);
        __m256 pz = _mm256_loadu_ps(&ps.pos_z[i]);

        // pos += vel * dt
        px = _mm256_fmadd_ps(vx, vdt, px);
        py = _mm256_fmadd_ps(vy, vdt, py);
        pz = _mm256_fmadd_ps(vz, vdt, pz);

        // Store updated positions
        _mm256_storeu_ps(&ps.pos_x[i], px);
        _mm256_storeu_ps(&ps.pos_y[i], py);
        _mm256_storeu_ps(&ps.pos_z[i], pz);
    }
}

// Version 3: Let the compiler auto-vectorize (with hints)
void update_autovec(ParticleSystem& ps, float dt) {
    float* __restrict__ px = ps.pos_x.data();
    float* __restrict__ py = ps.pos_y.data();
    float* __restrict__ pz = ps.pos_z.data();
    float* __restrict__ vx = ps.vel_x.data();
    float* __restrict__ vy = ps.vel_y.data();
    float* __restrict__ vz = ps.vel_z.data();
    const float* __restrict__ ax = ps.acc_x.data();
    const float* __restrict__ ay = ps.acc_y.data();
    const float* __restrict__ az = ps.acc_z.data();
    const size_t n = ps.count;

    // __restrict__ tells compiler arrays don't overlap → can vectorize
    for (size_t i = 0; i < n; ++i) {
        vx[i] += ax[i] * dt;
        vy[i] += ay[i] * dt;
        vz[i] += az[i] * dt;
        px[i] += vx[i] * dt;
        py[i] += vy[i] * dt;
        pz[i] += vz[i] * dt;
    }
}

void benchmark() {
    ParticleSystem ps;
    ps.resize(1'000'000);
    // Initialize with random data...

    auto time_it = [&](auto func, const char* name) {
        auto start = std::chrono::high_resolution_clock::now();
        for (int frame = 0; frame < 100; ++frame) func(ps, 0.016f);
        auto end = std::chrono::high_resolution_clock::now();
        auto ms = std::chrono::duration<double, std::milli>(end - start).count();
        fmt::print("{:20s}: {:.2f} ms/100frames\n", name, ms);
    };

    time_it(update_scalar, "Scalar");
    time_it(update_avx2, "AVX2 intrinsics");
    time_it(update_autovec, "Auto-vectorized");
    // Typical results (1M particles, 100 frames):
    // Scalar:           85 ms
    // AVX2 intrinsics:  12 ms (7x speedup)
    // Auto-vectorized:  13 ms (6.5x — compiler does well with __restrict__)
}
```

**Key takeaway:** With proper SoA layout and `__restrict__`, the compiler's auto-vectorizer produces code nearly as good as hand-written intrinsics. Use intrinsics only when the compiler fails (complex algorithms, gather/scatter, shuffles).

</details>

### Example 8.2 — Cache-Oblivious Matrix Transpose

**Problem:** Transpose a large matrix (4096x4096) efficiently. A naive implementation thrashes the cache because it reads columns (stride = N). Use a cache-oblivious recursive approach.

<details>
<summary>🔍 Full step-by-step solution</summary>

```cpp
#include <vector>
#include <algorithm>
#include <chrono>
#include <fmt/core.h>

// Naive transpose: reads column-wise (cache-hostile for large N)
void transpose_naive(float* dst, const float* src, int N) {
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            dst[j * N + i] = src[i * N + j];
            // src access: sequential (good)
            // dst access: stride N (BAD — cache miss every element for large N)
        }
    }
}

// Cache-oblivious recursive transpose
// Divides the matrix into quadrants until they fit in cache
void transpose_recursive(float* dst, const float* src,
                         int N,  // Full matrix dimension
                         int rs, int cs,  // Start row/col in src
                         int rd, int cd,  // Start row/col in dst
                         int size) {      // Current block size
    constexpr int BLOCK_THRESHOLD = 32;  // Base case: 32x32 fits in L1

    if (size <= BLOCK_THRESHOLD) {
        // Base case: small enough to transpose directly (fits in cache)
        for (int i = 0; i < size; ++i) {
            for (int j = 0; j < size; ++j) {
                dst[(rd + j) * N + (cd + i)] = src[(rs + i) * N + (cs + j)];
            }
        }
        return;
    }

    int half = size / 2;

    // Divide into 4 quadrants and recurse
    // Top-left → Top-left
    transpose_recursive(dst, src, N, rs, cs, rd, cd, half);
    // Top-right → Bottom-left
    transpose_recursive(dst, src, N, rs, cs + half, rd + half, cd, half);
    // Bottom-left → Top-right
    transpose_recursive(dst, src, N, rs + half, cs, rd, cd + half, half);
    // Bottom-right → Bottom-right
    transpose_recursive(dst, src, N, rs + half, cs + half, rd + half, cd + half, half);
}

// Tiled transpose (cache-aware alternative)
void transpose_tiled(float* dst, const float* src, int N) {
    constexpr int TILE = 32;  // Tile size tuned to L1 cache
    for (int i = 0; i < N; i += TILE) {
        for (int j = 0; j < N; j += TILE) {
            // Transpose one tile
            for (int ti = i; ti < std::min(i + TILE, N); ++ti) {
                for (int tj = j; tj < std::min(j + TILE, N); ++tj) {
                    dst[tj * N + ti] = src[ti * N + tj];
                }
            }
        }
    }
}

void benchmark_transpose() {
    constexpr int N = 4096;
    std::vector<float> src(N * N), dst(N * N);
    // Fill src...

    auto time_it = [&](auto func, const char* name) {
        auto start = std::chrono::high_resolution_clock::now();
        func(dst.data(), src.data(), N);
        auto end = std::chrono::high_resolution_clock::now();
        auto ms = std::chrono::duration<double, std::milli>(end - start).count();
        fmt::print("{:25s}: {:.2f} ms\n", name, ms);
    };

    time_it(transpose_naive, "Naive");
    time_it([](float* d, const float* s, int n) {
        transpose_recursive(d, s, n, 0, 0, 0, 0, n);
    }, "Cache-oblivious recursive");
    time_it(transpose_tiled, "Tiled (32x32)");

    // Typical results (4096x4096 floats = 64MB):
    // Naive:                    45 ms (constant cache misses)
    // Cache-oblivious:          12 ms (3.7x faster)
    // Tiled:                    11 ms (4x faster, but tuned to specific cache)
}
```

**Cache-oblivious vs cache-aware:**
- Cache-aware (tiled): You choose the tile size based on known cache size. Optimal for one machine.
- Cache-oblivious (recursive): Works well on ANY cache hierarchy without tuning. Slightly more overhead from recursion but portable.

</details>

### Example 8.3 — Profile-Guided Optimization (PGO) Workflow

**Problem:** Your game engine's release build is 15% slower than it could be. Use PGO to let the compiler optimize based on actual runtime behavior.

<details>
<summary>🔍 Full step-by-step solution</summary>

```bash
#!/bin/bash
# PGO workflow: instrument → profile → optimize

PROJECT_DIR=$(pwd)
BUILD_DIR="${PROJECT_DIR}/build-pgo"

# ═══════════════════════════════════════════════════════════════
# Step 1: Instrumented build (adds profiling counters)
# ═══════════════════════════════════════════════════════════════
echo "=== Step 1: Building instrumented binary ==="

cmake -B "${BUILD_DIR}/instrument" -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_CXX_FLAGS="-fprofile-generate=${BUILD_DIR}/profiles" \
    -DCMAKE_EXE_LINKER_FLAGS="-fprofile-generate=${BUILD_DIR}/profiles"

cmake --build "${BUILD_DIR}/instrument"

# ═══════════════════════════════════════════════════════════════
# Step 2: Run representative workload (generates .profraw files)
# ═══════════════════════════════════════════════════════════════
echo "=== Step 2: Running profiling workload ==="

# Run your game/app with typical usage patterns:
"${BUILD_DIR}/instrument/game_engine" --benchmark --scene=city --frames=1000
"${BUILD_DIR}/instrument/game_engine" --benchmark --scene=indoor --frames=1000
"${BUILD_DIR}/instrument/game_engine" --benchmark --scene=particles --frames=500

# For Clang: merge profile data
llvm-profdata merge -output="${BUILD_DIR}/profiles/merged.profdata" \
    "${BUILD_DIR}/profiles/"*.profraw

# ═══════════════════════════════════════════════════════════════
# Step 3: Optimized build using profile data
# ═══════════════════════════════════════════════════════════════
echo "=== Step 3: Building PGO-optimized binary ==="

cmake -B "${BUILD_DIR}/optimized" -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_CXX_FLAGS="-fprofile-use=${BUILD_DIR}/profiles/merged.profdata" \
    -DCMAKE_EXE_LINKER_FLAGS="-fprofile-use=${BUILD_DIR}/profiles/merged.profdata"

cmake --build "${BUILD_DIR}/optimized"

echo "=== Done! PGO binary at: ${BUILD_DIR}/optimized/game_engine ==="
```

```cmake
# CMake integration for PGO (CMakeLists.txt)
option(PGO_GENERATE "Build with PGO instrumentation" OFF)
option(PGO_USE "Build with PGO optimization" OFF)

if(PGO_GENERATE)
    set(PGO_DIR "${CMAKE_BINARY_DIR}/pgo-profiles")
    file(MAKE_DIRECTORY ${PGO_DIR})
    add_compile_options(-fprofile-generate=${PGO_DIR})
    add_link_options(-fprofile-generate=${PGO_DIR})
elseif(PGO_USE)
    set(PGO_DIR "${CMAKE_SOURCE_DIR}/pgo-profiles")
    if(EXISTS "${PGO_DIR}/merged.profdata")
        add_compile_options(-fprofile-use=${PGO_DIR}/merged.profdata)
        add_link_options(-fprofile-use=${PGO_DIR}/merged.profdata)
    else()
        message(WARNING "PGO profile data not found at ${PGO_DIR}")
    endif()
endif()
```

**What PGO optimizes:**

| Optimization | How PGO Helps | Typical Gain |
|-------------|---------------|--------------|
| Branch prediction hints | Knows which branches are taken 99% of the time | 5-10% |
| Function inlining | Inlines hot functions, avoids inlining cold ones | 3-8% |
| Code layout | Places hot code together (fewer I-cache misses) | 5-15% |
| Loop unrolling | Knows actual iteration counts | 2-5% |
| Virtual call devirtualization | Knows which derived type is used most | 3-10% |
| Register allocation | Prioritizes registers for hot variables | 2-5% |

**Total typical improvement: 10-25% for CPU-bound applications.**

</details>



---

## 📘 9. Appendix: Extended Derivations & Special Cases

### 9.1 Branch Prediction — How CPUs Guess and How to Help

**Modern CPUs execute instructions speculatively.** When encountering a branch (if/else, loop condition), the CPU guesses which path will be taken and starts executing it. A misprediction costs 15-20 cycles (the pipeline must be flushed and restarted).

#### How Branch Predictors Work

Modern predictors (like Intel's TAGE predictor) maintain a history table:
- **Static prediction:** Forward branches (if) predicted not-taken; backward branches (loops) predicted taken
- **Dynamic prediction:** Records the last N outcomes of each branch and predicts based on pattern

```cpp
// PREDICTABLE: branch follows a pattern (always true, or alternating)
for (int i = 0; i < N; ++i) {
    if (i < N - 1) { /* taken 99.99% of the time — predictor learns this */ }
}

// UNPREDICTABLE: random 50/50 branch (worst case for predictor)
for (int i = 0; i < N; ++i) {
    if (data[i] > 128) { /* random data → 50% taken → constant mispredictions */ }
}
```

#### Techniques to Eliminate Branches

```cpp
// 1. Sort data to make branches predictable
std::sort(data.begin(), data.end());
// Now: all values < 128 come first (branch always not-taken)
// Then: all values >= 128 (branch always taken)
// Misprediction only at the transition point!

// 2. Branchless conditional with arithmetic
// Branchy:
int result = (x > 0) ? x : -x;  // Branch!
// Branchless:
int mask = x >> 31;  // All 1s if negative, all 0s if positive
int result = (x ^ mask) - mask;  // Absolute value without branch

// 3. CMOV (conditional move) — compiler hint
int min_branchless(int a, int b) {
    return a < b ? a : b;
    // Compiler generates: cmp + cmovl (no branch, just conditional register move)
}

// 4. Lookup tables instead of switch statements
// Branchy:
int category(int score) {
    if (score >= 90) return 4;
    if (score >= 80) return 3;
    if (score >= 70) return 2;
    if (score >= 60) return 1;
    return 0;
}
// Branchless (precomputed table):
static const int category_table[101] = { /* precomputed */ };
int category_fast(int score) { return category_table[std::clamp(score, 0, 100)]; }

// 5. __builtin_expect (GCC/Clang) — hint to compiler
if (__builtin_expect(error_occurred, 0)) {  // "this is unlikely"
    handle_error();  // Compiler places this code out-of-line (cold path)
}
// C++20: [likely](likely) and [unlikely](unlikely) attributes
if (error_occurred) [unlikely](unlikely) {
    handle_error();
}
```

#### Measuring Branch Mispredictions

```bash
# Linux perf:
perf stat -e branches,branch-misses ./my_program
# Output: 1,234,567 branch-misses (2.3% of all branches)
# Target: < 1% misprediction rate for hot loops

# Intel VTune:
vtune -collect uarch-exploration ./my_program
```

### 9.2 Memory Prefetching — Hiding Latency

**L1 cache hit: ~4 cycles. L2: ~12 cycles. L3: ~40 cycles. Main memory: ~200 cycles.** Prefetching tells the CPU to start loading data before you need it, hiding the latency.

#### Hardware Prefetcher

Modern CPUs automatically detect sequential and strided access patterns:
```cpp
// Hardware prefetcher handles this automatically:
for (int i = 0; i < N; ++i) {
    sum += data[i];  // Sequential access → HW prefetcher kicks in after ~2 misses
}

// Hardware prefetcher CANNOT handle:
for (int i = 0; i < N; ++i) {
    sum += data[indices[i]];  // Random access → no pattern to detect
}
```

#### Software Prefetching

```cpp
#include <xmmintrin.h>  // _mm_prefetch

// Prefetch hints:
// _MM_HINT_T0: Prefetch into L1 (use soon)
// _MM_HINT_T1: Prefetch into L2 (use later)
// _MM_HINT_T2: Prefetch into L3 (use much later)
// _MM_HINT_NTA: Non-temporal (use once, don't pollute cache)

// Pattern: prefetch N iterations ahead
void process_linked_list(Node* head) {
    Node* current = head;
    while (current) {
        // Prefetch the node we'll need 3 iterations from now
        Node* lookahead = current->next;
        if (lookahead) lookahead = lookahead->next;
        if (lookahead) lookahead = lookahead->next;
        if (lookahead) _mm_prefetch(lookahead, _MM_HINT_T0);

        process(current->data);
        current = current->next;
    }
}

// Pattern: prefetch for random access (hash table probing)
void lookup_batch(const HashTable& ht, const Key* keys, Value* results, int n) {
    constexpr int PREFETCH_DISTANCE = 8;

    // Phase 1: Compute hashes and prefetch buckets
    std::array<size_t, PREFETCH_DISTANCE> hashes;
    for (int i = 0; i < std::min(n, PREFETCH_DISTANCE); ++i) {
        hashes[i] = hash(keys[i]);
        _mm_prefetch(&ht.buckets[hashes[i] % ht.capacity], _MM_HINT_T0);
    }

    // Phase 2: Process with prefetching pipeline
    for (int i = 0; i < n; ++i) {
        // Use previously prefetched data
        results[i] = ht.buckets[hashes[i % PREFETCH_DISTANCE] % ht.capacity].value;

        // Prefetch for future iteration
        if (i + PREFETCH_DISTANCE < n) {
            hashes[i % PREFETCH_DISTANCE] = hash(keys[i + PREFETCH_DISTANCE]);
            _mm_prefetch(&ht.buckets[hashes[i % PREFETCH_DISTANCE] % ht.capacity],
                        _MM_HINT_T0);
        }
    }
}
```

#### When Prefetching Helps vs Hurts

| Scenario | Prefetch Useful? | Why |
|----------|-----------------|-----|
| Sequential array | ❌ No | HW prefetcher handles it |
| Linked list traversal | ✅ Yes | Pointer chasing defeats HW prefetcher |
| Hash table lookup | ✅ Yes | Random access pattern |
| Binary tree traversal | ✅ Yes | Pointer chasing |
| Small arrays (< L1) | ❌ No | Already in cache |
| Streaming (use-once) | ⚠️ Use NTA | Avoid polluting cache |

### 9.3 The Memory Hierarchy — Numbers Every Programmer Should Know

```
┌─────────────────────────────────────────────────────────────┐
│ Register         │  < 1 cycle  │  ~1 KB    │ Per-core      │
├──────────────────┼─────────────┼───────────┼───────────────┤
│ L1 Cache         │  4 cycles   │  32-48 KB │ Per-core      │
├──────────────────┼─────────────┼───────────┼───────────────┤
│ L2 Cache         │  12 cycles  │  256 KB-1MB│ Per-core     │
├──────────────────┼─────────────┼───────────┼───────────────┤
│ L3 Cache         │  40 cycles  │  8-64 MB  │ Shared        │
├──────────────────┼─────────────┼───────────┼───────────────┤
│ Main Memory      │  200 cycles │  16-128 GB│ Shared        │
├──────────────────┼─────────────┼───────────┼───────────────┤
│ NVMe SSD         │  ~25,000 cy │  1-4 TB   │ Shared        │
├──────────────────┼─────────────┼───────────┼───────────────┤
│ Network (1Gbps)  │  ~500,000 cy│  ∞        │ External      │
└──────────────────┴─────────────┴───────────┴───────────────┘
```

**Cache line size: 64 bytes** (on x86). Every memory access loads an entire 64-byte line. This means:
- Accessing `array[0]` also loads `array[1]` through `array[15]` (for 4-byte ints)
- Struct members within the same 64 bytes are "free" to access together
- False sharing occurs when two threads write to different variables in the same cache line

**Bandwidth vs Latency:**
- L1 bandwidth: ~1 TB/s (can feed AVX2 at full speed)
- Main memory bandwidth: ~50 GB/s (DDR5 dual-channel)
- A single core can saturate memory bandwidth with sequential access
- Random access is latency-bound, not bandwidth-bound

---

*Next: [09.8 - Game Dev with C++ - Unreal Engine & Custom Engine Patterns](09.8---Game-Dev-with-C++---Unreal-Engine-&-Custom-Engine-Patterns) →*