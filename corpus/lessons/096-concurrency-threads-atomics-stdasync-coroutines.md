---
title: "09.6 — Concurrency: Threads, Atomics, std::async, Coroutines"
subject: "C++"
catalog: advanced
audience_tier: higher-education
chapter: "9.6"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | [LEARNING_PATH](LEARNING_PATH) | Part of [09 - Learning Index](09---Learning-Index)*

# 09.6 — Concurrency: Threads, Atomics, std::async, Coroutines

> *"If you think it's simple, then you have misunderstood the problem."* — Bjarne Stroustrup (on concurrency)

C++ gives you **real parallelism** — no GIL, no interpreter overhead, direct access to hardware threads. But with great power comes great responsibility: data races are undefined behavior, and debugging concurrent code is notoriously difficult. This chapter builds from basic threading through lock-free programming to C++20 coroutines.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Create and manage threads with `std::thread` and `std::jthread` (C++20).
2. Protect shared data with mutexes, lock guards, and condition variables.
3. Use atomics and understand the C++ memory model (acquire/release semantics).
4. Launch asynchronous tasks with `std::async` and retrieve results via futures.
5. Write coroutines with `co_await`, `co_yield`, and `co_return` (C++20).
6. Design thread-safe data structures and avoid common pitfalls (deadlocks, races, false sharing).

---

## 🖼️ Visual Anchor — C++ Concurrency Model

![cpp__2.6-fig1](cpp__2.6-fig1.svg)

---

## 📚 1. Concepts & Definitions

### Definition 09.6.1 — Threads vs Python's GIL

| Feature | Python (CPython) | C++ |
|---------|-----------------|-----|
| True parallelism | ❌ (GIL blocks) | ✅ (real OS threads) |
| Thread creation | `threading.Thread` | `std::thread` / `std::jthread` |
| Shared memory | Yes (but GIL serializes) | Yes (must synchronize manually) |
| Data race | Impossible (GIL) | **Undefined behavior** |
| Async I/O | `asyncio` (cooperative) | Coroutines (cooperative) |

**Key insight:** In Python, threads can't cause data races because the GIL serializes access. In C++, **you** are responsible for synchronization. A data race = UB = anything can happen.

### Definition 09.6.2 — `std::thread` and `std::jthread`

```cpp
#include <thread>

// std::thread — basic thread (must join or detach manually)
void worker(int id) {
    fmt::print("Thread {} running\n", id);
}
std::thread t(worker, 42);
t.join();  // Wait for completion (MUST call join or detach before destruction)

// std::jthread (C++20) — auto-joins on destruction + supports cancellation
std::jthread jt([](std::stop_token token) {
    while (!token.stop_requested()) {
        // Do work...
        std::this_thread::sleep_for(std::chrono::milliseconds(16));
    }
});
// jt automatically joins when it goes out of scope
// jt.request_stop();  // Cooperative cancellation
```

### Definition 09.6.3 — Mutex & Lock Guards

```cpp
#include <mutex>

std::mutex mtx;
std::vector<int> shared_data;

void safe_push(int value) {
    std::lock_guard<std::mutex> lock(mtx);  // RAII: locks on construction
    shared_data.push_back(value);
}  // Automatically unlocks here (even on exception)

// C++17: std::scoped_lock (locks multiple mutexes without deadlock)
std::mutex mtx_a, mtx_b;
void transfer() {
    std::scoped_lock lock(mtx_a, mtx_b);  // Deadlock-free multi-lock
    // ... modify both protected resources ...
}
```

### Definition 09.6.4 — Atomics

**Atomic operations** are indivisible — no other thread can observe them half-done:

```cpp
#include <atomic>

std::atomic<int> counter{0};

// These are thread-safe WITHOUT a mutex:
counter.fetch_add(1);           // Atomic increment
counter.store(42);              // Atomic write
int val = counter.load();       // Atomic read
bool ok = counter.compare_exchange_strong(val, 100);  // CAS

// Atomic flag (simplest synchronization primitive)
std::atomic_flag ready = ATOMIC_FLAG_INIT;
ready.test_and_set();  // Set flag, return previous value
ready.clear();         // Clear flag
```

### Definition 09.6.5 — Coroutines (C++20)

Coroutines are functions that can **suspend** and **resume** execution. Unlike threads, they don't require OS scheduling — they're cooperative and lightweight:

```cpp
#include <coroutine>

// Generator: yields values lazily (like Python's yield)
Generator<int> fibonacci() {
    int a = 0, b = 1;
    while (true) {
        co_yield a;
        auto next = a + b;
        a = b;
        b = next;
    }
}

// Async task: suspends on I/O
Task<std::string> fetch_data(std::string url) {
    auto response = co_await async_http_get(url);  // Suspends here
    co_return response.body();
}
```

---

## 🧩 2. Mental Models

### Model 2.6.1 — "Mutex = Bathroom Lock"

A mutex is like a bathroom lock — only one person (thread) can be inside at a time. Everyone else waits in line. Simple, correct, but creates a bottleneck if many threads need access.

### Model 2.6.2 — "Atomics = Instant Transactions"

Atomics are like database transactions that always succeed instantly. No waiting, no locking — but limited to simple operations (read, write, increment, compare-and-swap).

### Model 2.6.3 — "Coroutines = Bookmark in a Book"

A coroutine is like reading a book and placing a bookmark. You can put it down (`co_await`), do something else, and pick it back up exactly where you left off. No new thread needed — just one reader switching between multiple books.

### Model 2.6.4 — Python Comparison Table

| Python | C++ | Notes |
|--------|-----|-------|
| `threading.Thread` | `std::jthread` | C++ has real parallelism |
| `threading.Lock` | `std::mutex` + `lock_guard` | Same concept, RAII in C++ |
| `asyncio.run()` | Custom event loop | C++ doesn't ship one (use libraries) |
| `async def` / `await` | `co_await` / `co_return` | Similar syntax, different runtime |
| `multiprocessing` | Not needed | C++ threads ARE parallel |
| GIL | Doesn't exist | You handle synchronization |

See [08.4 - Concurrency - asyncio, threading, multiprocessing & the GIL](08.4---Concurrency---asyncio,-threading,-multiprocessing-&-the-GIL) for the Python side.


---

## 🔑 3. Mechanics

### 3.1 — Thread Creation & Management

```cpp
#include <thread>
#include <vector>
#include <fmt/core.h>

// Launch threads with any callable
void parallel_work() {
    auto task = [](int id, int iterations) {
        for (int i = 0; i < iterations; ++i) {
            // Compute...
        }
        fmt::print("Thread {} done\n", id);
    };

    // Launch N threads
    const int num_threads = std::thread::hardware_concurrency();
    std::vector<std::jthread> threads;
    threads.reserve(num_threads);

    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back(task, i, 1000);
    }
    // All threads auto-join when vector is destroyed
}

// Passing data to threads
struct WorkItem { int id; std::string payload; };

void process(WorkItem item) {
    fmt::print("Processing {}: {}\n", item.id, item.payload);
}

// CAREFUL: std::thread copies arguments by default
WorkItem work{1, "data"};
std::jthread t(process, work);  // work is COPIED into the thread

// To pass by reference, use std::ref:
std::jthread t2([](WorkItem& w) { w.payload = "modified"; }, std::ref(work));
```

### 3.2 — Condition Variables (Producer-Consumer)

```cpp
#include <mutex>
#include <condition_variable>
#include <queue>

template<typename T>
class ThreadSafeQueue {
    std::queue<T> queue_;
    mutable std::mutex mtx_;
    std::condition_variable cv_;

public:
    void push(T value) {
        {
            std::lock_guard lock(mtx_);
            queue_.push(std::move(value));
        }
        cv_.notify_one();  // Wake one waiting consumer
    }

    T pop() {
        std::unique_lock lock(mtx_);
        cv_.wait(lock, [this] { return !queue_.empty(); });  // Sleep until data
        T value = std::move(queue_.front());
        queue_.pop();
        return value;
    }

    bool try_pop(T& value, std::chrono::milliseconds timeout) {
        std::unique_lock lock(mtx_);
        if (!cv_.wait_for(lock, timeout, [this] { return !queue_.empty(); })) {
            return false;  // Timed out
        }
        value = std::move(queue_.front());
        queue_.pop();
        return true;
    }

    size_t size() const {
        std::lock_guard lock(mtx_);
        return queue_.size();
    }
};

// Usage:
ThreadSafeQueue<std::function<void()>> task_queue;

// Producer
task_queue.push([] { fmt::print("Task executed\n"); });

// Consumer (in another thread)
auto task = task_queue.pop();  // Blocks until task available
task();
```

### 3.3 — `std::async` and Futures

```cpp
#include <future>

// Launch async task — returns a future
std::future<int> result = std::async(std::launch::async, [] {
    std::this_thread::sleep_for(std::chrono::seconds(1));
    return 42;
});

// Do other work while task runs...
fmt::print("Waiting for result...\n");
int value = result.get();  // Blocks until ready, returns 42

// Launch policies:
// std::launch::async    — guaranteed new thread
// std::launch::deferred — lazy evaluation (runs when .get() called)
// std::launch::async | std::launch::deferred — implementation chooses (default)

// Multiple async tasks
auto f1 = std::async(std::launch::async, compute_physics);
auto f2 = std::async(std::launch::async, compute_ai);
auto f3 = std::async(std::launch::async, load_assets);

// Wait for all
auto physics = f1.get();
auto ai = f2.get();
auto assets = f3.get();
```

### 3.4 — Atomics & Memory Ordering

```cpp
#include <atomic>

// Lock-free counter (no mutex needed)
class AtomicCounter {
    std::atomic<int64_t> count_{0};
public:
    void increment() { count_.fetch_add(1, std::memory_order_relaxed); }
    int64_t get() const { return count_.load(std::memory_order_relaxed); }
};

// Spinlock (busy-wait lock using atomic_flag)
class SpinLock {
    std::atomic_flag flag_ = ATOMIC_FLAG_INIT;
public:
    void lock() {
        while (flag_.test_and_set(std::memory_order_acquire)) {
            // Spin — hint to CPU we're in a spin loop
            #if defined(__cpp_lib_atomic_flag_test)
            while (flag_.test(std::memory_order_relaxed)) {}  // Spin on read
            #endif
        }
    }
    void unlock() {
        flag_.clear(std::memory_order_release);
    }
};

// Memory ordering levels (from weakest to strongest):
// memory_order_relaxed  — no ordering guarantees (just atomicity)
// memory_order_acquire  — reads after this see writes before matching release
// memory_order_release  — writes before this are visible after matching acquire
// memory_order_acq_rel  — both acquire and release
// memory_order_seq_cst  — total ordering (default, safest, slowest)
```

### 3.5 — Coroutines (C++20)

```cpp
#include <coroutine>
#include <optional>

// Simple Generator (yields values one at a time)
template<typename T>
class Generator {
public:
    struct promise_type {
        T current_value;
        std::suspend_always yield_value(T value) {
            current_value = std::move(value);
            return {};
        }
        std::suspend_always initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        Generator get_return_object() {
            return Generator{Handle::from_promise(*this)};
        }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };

    using Handle = std::coroutine_handle<promise_type>;

    explicit Generator(Handle h) : handle_(h) {}
    ~Generator() { if (handle_) handle_.destroy(); }

    // Move-only
    Generator(Generator&& o) noexcept : handle_(std::exchange(o.handle_, {})) {}
    Generator& operator=(Generator&&) = delete;

    // Iterator interface for range-for
    struct Sentinel {};
    struct Iterator {
        Handle handle;
        bool operator==(Sentinel) const { return handle.done(); }
        Iterator& operator++() { handle.resume(); return *this; }
        T& operator*() { return handle.promise().current_value; }
    };

    Iterator begin() { handle_.resume(); return {handle_}; }
    Sentinel end() { return {}; }

private:
    Handle handle_;
};

// Usage: infinite fibonacci generator
Generator<uint64_t> fibonacci() {
    uint64_t a = 0, b = 1;
    while (true) {
        co_yield a;
        auto next = a + b;
        a = b;
        b = next;
    }
}

// Take first 20 fibonacci numbers
for (auto [i, fib] : fibonacci() | std::views::enumerate | std::views::take(20)) {
    fmt::print("fib({}) = {}\n", i, fib);
}
```

### 3.6 — Thread Pool Pattern

```cpp
#include <thread>
#include <vector>
#include <queue>
#include <functional>
#include <future>
#include <mutex>
#include <condition_variable>

class ThreadPool {
    std::vector<std::jthread> workers_;
    std::queue<std::function<void()>> tasks_;
    std::mutex mtx_;
    std::condition_variable cv_;
    std::atomic<bool> stop_{false};

public:
    explicit ThreadPool(size_t num_threads = std::thread::hardware_concurrency()) {
        for (size_t i = 0; i < num_threads; ++i) {
            workers_.emplace_back([this](std::stop_token token) {
                while (!token.stop_requested()) {
                    std::function<void()> task;
                    {
                        std::unique_lock lock(mtx_);
                        cv_.wait(lock, [&] {
                            return stop_ || !tasks_.empty();
                        });
                        if (stop_ && tasks_.empty()) return;
                        task = std::move(tasks_.front());
                        tasks_.pop();
                    }
                    task();
                }
            });
        }
    }

    template<typename F>
    auto submit(F&& func) -> std::future<std::invoke_result_t<F>> {
        using R = std::invoke_result_t<F>;
        auto task = std::make_shared<std::packaged_task<R()>>(std::forward<F>(func));
        auto future = task->get_future();
        {
            std::lock_guard lock(mtx_);
            tasks_.push([task]() { (*task)(); });
        }
        cv_.notify_one();
        return future;
    }

    ~ThreadPool() {
        stop_ = true;
        cv_.notify_all();
    }
};

// Usage:
ThreadPool pool(8);
auto f1 = pool.submit([] { return expensive_computation(); });
auto f2 = pool.submit([] { return load_texture("wall.png"); });
auto result = f1.get();  // Block until done
```


---

## ✍️ 4. Worked Examples

### Example 09.6.1 — Parallel Image Processing

<details>
<summary>Process image tiles in parallel using a thread pool</summary>

```cpp
#include <vector>
#include <future>
#include <cmath>

struct Pixel { uint8_t r, g, b, a; };
struct Image {
    std::vector<Pixel> data;
    int width, height;
    Pixel& at(int x, int y) { return data[y * width + x]; }
};

void apply_blur_tile(Image& img, int start_y, int end_y) {
    for (int y = start_y; y < end_y; ++y) {
        for (int x = 1; x < img.width - 1; ++x) {
            // Simple box blur (3x3 kernel)
            int r = 0, g = 0, b = 0;
            for (int dy = -1; dy <= 1; ++dy) {
                for (int dx = -1; dx <= 1; ++dx) {
                    auto& p = img.at(x + dx, y + dy);
                    r += p.r; g += p.g; b += p.b;
                }
            }
            auto& out = img.at(x, y);
            out.r = r / 9; out.g = g / 9; out.b = b / 9;
        }
    }
}

void parallel_blur(Image& img, ThreadPool& pool) {
    const int num_tiles = std::thread::hardware_concurrency();
    const int tile_height = img.height / num_tiles;

    std::vector<std::future<void>> futures;
    for (int i = 0; i < num_tiles; ++i) {
        int start_y = std::max(1, i * tile_height);
        int end_y = (i == num_tiles - 1) ? img.height - 1 : (i + 1) * tile_height;
        futures.push_back(pool.submit([&img, start_y, end_y] {
            apply_blur_tile(img, start_y, end_y);
        }));
    }
    for (auto& f : futures) f.get();  // Wait for all tiles
}
```

</details>

### Example 09.6.2 — Lock-Free Single-Producer Single-Consumer Queue

<details>
<summary>Build a wait-free SPSC queue using atomics</summary>

```cpp
#include <atomic>
#include <array>
#include <optional>

template<typename T, size_t Capacity>
class SPSCQueue {
    static_assert((Capacity & (Capacity - 1)) == 0, "Capacity must be power of 2");

    std::array<T, Capacity> buffer_;
    alignas(64) std::atomic<size_t> head_{0};  // Written by consumer
    alignas(64) std::atomic<size_t> tail_{0};  // Written by producer
    // alignas(64) prevents false sharing between head and tail

public:
    bool push(const T& value) {
        const size_t tail = tail_.load(std::memory_order_relaxed);
        const size_t next_tail = (tail + 1) & (Capacity - 1);

        if (next_tail == head_.load(std::memory_order_acquire)) {
            return false;  // Full
        }

        buffer_[tail] = value;
        tail_.store(next_tail, std::memory_order_release);
        return true;
    }

    std::optional<T> pop() {
        const size_t head = head_.load(std::memory_order_relaxed);

        if (head == tail_.load(std::memory_order_acquire)) {
            return std::nullopt;  // Empty
        }

        T value = std::move(buffer_[head]);
        head_.store((head + 1) & (Capacity - 1), std::memory_order_release);
        return value;
    }
};

// Usage: audio thread (producer) → render thread (consumer)
SPSCQueue<AudioEvent, 1024> audio_events;
// Producer: audio_events.push(event);
// Consumer: if (auto e = audio_events.pop()) process(*e);
```

</details>

### Example 09.6.3 — Game Loop with Async Asset Loading

<details>
<summary>Load assets asynchronously while the game loop continues</summary>

```cpp
#include <future>
#include <unordered_map>
#include <string>

class AssetManager {
    std::unordered_map<std::string, std::shared_ptr<Texture>> loaded_;
    std::unordered_map<std::string, std::future<std::shared_ptr<Texture>>> pending_;

public:
    void request_texture(const std::string& path) {
        if (loaded_.contains(path) || pending_.contains(path)) return;

        pending_[path] = std::async(std::launch::async, [path] {
            // Load from disk (slow, runs on background thread)
            auto data = read_file(path);
            auto tex = std::make_shared<Texture>(decode_png(data));
            return tex;
        });
    }

    // Call every frame to check for completed loads
    void poll() {
        for (auto it = pending_.begin(); it != pending_.end(); ) {
            auto& [path, future] = *it;
            if (future.wait_for(std::chrono::seconds(0)) == std::future_status::ready) {
                loaded_[path] = future.get();
                it = pending_.erase(it);
            } else {
                ++it;
            }
        }
    }

    std::shared_ptr<Texture> get(const std::string& path) {
        auto it = loaded_.find(path);
        return (it != loaded_.end()) ? it->second : nullptr;
    }
};
```

</details>

---

## 💻 5. Code Patterns & Idioms

### Pattern 2.6.1 — Double-Checked Locking (Singleton)

```cpp
class AudioEngine {
    static std::atomic<AudioEngine*> instance_;
    static std::mutex mtx_;

public:
    static AudioEngine& get() {
        auto* p = instance_.load(std::memory_order_acquire);
        if (!p) {
            std::lock_guard lock(mtx_);
            p = instance_.load(std::memory_order_relaxed);
            if (!p) {
                p = new AudioEngine();
                instance_.store(p, std::memory_order_release);
            }
        }
        return *p;
    }
};

// BETTER: Use Meyers' Singleton (thread-safe since C++11)
class AudioEngine {
public:
    static AudioEngine& get() {
        static AudioEngine instance;  // Thread-safe initialization guaranteed
        return instance;
    }
};
```

### Pattern 2.6.2 — Read-Write Lock (Shared Mutex)

```cpp
#include <shared_mutex>

class GameWorld {
    mutable std::shared_mutex mtx_;
    std::vector<Entity> entities_;

public:
    // Multiple readers can hold shared lock simultaneously
    Entity get_entity(size_t id) const {
        std::shared_lock lock(mtx_);  // Shared (read) access
        return entities_[id];
    }

    size_t entity_count() const {
        std::shared_lock lock(mtx_);
        return entities_.size();
    }

    // Only one writer at a time (exclusive lock)
    void add_entity(Entity e) {
        std::unique_lock lock(mtx_);  // Exclusive (write) access
        entities_.push_back(std::move(e));
    }
};
```

---

## ⚠️ 6. Gotchas & Anti-Patterns

### Gotcha 2.6.1 — Data Race = Undefined Behavior

```cpp
int counter = 0;  // Non-atomic, shared between threads

// BUG: Data race — undefined behavior!
std::jthread t1([&] { for (int i = 0; i < 1000000; ++i) ++counter; });
std::jthread t2([&] { for (int i = 0; i < 1000000; ++i) ++counter; });
// counter might be 1500000, 2000000, or your program might crash

// FIX: Use atomic
std::atomic<int> counter{0};
// Or use a mutex (if operation is complex)
```

### Gotcha 2.6.2 — Deadlock from Lock Ordering

```cpp
std::mutex mtx_a, mtx_b;

// Thread 1:
void thread1() {
    std::lock_guard lock_a(mtx_a);  // Locks A first
    std::lock_guard lock_b(mtx_b);  // Then B
}

// Thread 2:
void thread2() {
    std::lock_guard lock_b(mtx_b);  // Locks B first
    std::lock_guard lock_a(mtx_a);  // Then A — DEADLOCK!
}

// FIX: Use std::scoped_lock (locks both atomically, deadlock-free)
void safe() {
    std::scoped_lock lock(mtx_a, mtx_b);  // Order doesn't matter
}
```

### Gotcha 2.6.3 — False Sharing

```cpp
// BUG: Two atomics on the same cache line — threads thrash each other
struct Counters {
    std::atomic<int> counter_a;  // Same 64-byte cache line!
    std::atomic<int> counter_b;  // Writes to A invalidate B's cache
};

// FIX: Align to cache line boundaries
struct Counters {
    alignas(64) std::atomic<int> counter_a;  // Own cache line
    alignas(64) std::atomic<int> counter_b;  // Own cache line
};
```

### Gotcha 2.6.4 — Forgetting to Join/Detach `std::thread`

```cpp
void bad() {
    std::thread t([] { /* work */ });
    // BUG: t destroyed without join() or detach() → std::terminate()!
}

// FIX: Use std::jthread (auto-joins) or always join/detach
void good() {
    std::jthread t([] { /* work */ });
    // Automatically joins on destruction
}
```

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- **Previous:** [09.5 - Standard Template Library - Containers, Algorithms, Iterators, Ranges](09.5---Standard-Template-Library---Containers,-Algorithms,-Iterators,-Ranges)
- **Next:** [09.7 - Performance - SIMD, Memory Layout & Cache Optimization](09.7---Performance---SIMD,-Memory-Layout-&-Cache-Optimization)
- **Python concurrency comparison:** [08.4 - Concurrency - asyncio, threading, multiprocessing & the GIL](08.4---Concurrency---asyncio,-threading,-multiprocessing-&-the-GIL)
- **Cache lines & false sharing:** [09.7 - Performance - SIMD, Memory Layout & Cache Optimization](09.7---Performance---SIMD,-Memory-Layout-&-Cache-Optimization)
- **Hardware context:** [1.12 - Computer Architecture & How Code Becomes Execution](1.12---Computer-Architecture-&-How-Code-Becomes-Execution)

### External Resources
- [C++ Concurrency in Action (Anthony Williams)](https://www.manning.com/books/c-plus-plus-concurrency-in-action-second-edition)
- [cppreference: Thread support](https://en.cppreference.com/w/cpp/thread)
- [cppreference: Coroutines](https://en.cppreference.com/w/cpp/language/coroutines)
- [CppCon: "Back to Basics: Concurrency"](https://www.youtube.com/results?search_query=cppcon+back+to+basics+concurrency)
- [Herb Sutter: "Lock-Free Programming"](https://www.youtube.com/results?search_query=herb+sutter+lock+free)
- [C++ Core Guidelines: Concurrency](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-concurrency)

---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — `std::jthread` + `stop_token` — Cooperative Cancellation

**Problem:** Implement a background worker that can be cleanly cancelled without data races, dangling references, or forced termination.

<details>
<summary>🔍 Full step-by-step solution</summary>

```cpp
#include <thread>
#include <stop_token>
#include <chrono>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <fmt/core.h>

// std::jthread (C++20) improvements over std::thread:
// 1. Auto-joins on destruction (no more std::terminate)
// 2. Built-in stop_token for cooperative cancellation
// 3. stop_callback for cleanup notifications

class BackgroundProcessor {
    std::queue<std::function<void()>> tasks_;
    std::mutex mtx_;
    std::condition_variable_any cv_;  // _any works with stop_token
    std::jthread worker_;

    void run(std::stop_token stop) {
        while (!stop.stop_requested()) {
            std::function<void()> task;
            {
                std::unique_lock lock(mtx_);
                // condition_variable_any::wait integrates with stop_token!
                bool got_work = cv_.wait(lock, stop, [this] {
                    return !tasks_.empty();
                });
                if (!got_work) break;  // stop was requested
                task = std::move(tasks_.front());
                tasks_.pop();
            }
            task();
        }
        fmt::print("Worker: clean shutdown\n");
    }

public:
    BackgroundProcessor()
        : worker_([this](std::stop_token st) { run(st); }) {}

    void submit(std::function<void()> task) {
        {
            std::lock_guard lock(mtx_);
            tasks_.push(std::move(task));
        }
        cv_.notify_one();
    }

    // Destructor: jthread requests stop + joins automatically
    ~BackgroundProcessor() {
        // worker_.request_stop() called implicitly by jthread destructor
        // Then join() is called — no manual cleanup needed!
        cv_.notify_all();  // Wake worker so it can see stop request
    }
};

// stop_callback: register cleanup when stop is requested
void with_callback() {
    std::jthread worker([](std::stop_token st) {
        // Register callback that fires when stop is requested
        std::stop_callback cleanup(st, [] {
            fmt::print("Cleanup: releasing resources\n");
        });

        while (!st.stop_requested()) {
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
            fmt::print("Working...\n");
        }
    });

    std::this_thread::sleep_for(std::chrono::seconds(1));
    worker.request_stop();  // Triggers callback + sets stop flag
    // worker auto-joins here
}

// Comparison with old std::thread approach:
void old_way() {
    std::atomic<bool> should_stop{false};  // Manual flag
    std::thread t([&should_stop] {
        while (!should_stop.load()) { /* work */ }
    });
    should_stop = true;
    t.join();  // MUST remember to join or detach!
}
```

</details>

### Example 8.2 — `std::atomic<std::shared_ptr>` in C++20

**Problem:** Multiple threads need to read and occasionally update a shared configuration object. Use C++20's `std::atomic<std::shared_ptr<T>>` for lock-free read access with safe updates.

<details>
<summary>🔍 Full step-by-step solution</summary>

```cpp
#include <atomic>
#include <memory>
#include <thread>
#include <vector>
#include <string>
#include <fmt/core.h>

// The problem: sharing a config that's read frequently, updated rarely
struct GameConfig {
    float gravity = 9.81f;
    int max_entities = 10000;
    std::string level_name = "default";
    float render_distance = 1000.0f;
};

// C++20: std::atomic<std::shared_ptr<T>> — lock-free reads!
class ConfigManager {
    std::atomic<std::shared_ptr<const GameConfig>> config_;

public:
    ConfigManager()
        : config_(std::make_shared<const GameConfig>()) {}

    // READ: Lock-free, wait-free on most platforms
    // Multiple threads can call this simultaneously with zero contention
    std::shared_ptr<const GameConfig> get() const {
        return config_.load(std::memory_order_acquire);
    }

    // WRITE: Atomically swaps the entire config
    // Readers with old shared_ptr keep it alive until they're done
    void update(std::shared_ptr<const GameConfig> new_config) {
        config_.store(std::move(new_config), std::memory_order_release);
    }

    // Read-modify-write with compare_exchange
    void modify(std::function<GameConfig(const GameConfig&)> modifier) {
        auto old_config = config_.load(std::memory_order_relaxed);
        while (true) {
            auto new_config = std::make_shared<const GameConfig>(
                modifier(*old_config));
            if (config_.compare_exchange_weak(old_config, new_config,
                    std::memory_order_release, std::memory_order_relaxed)) {
                break;
            }
            // old_config updated by compare_exchange_weak on failure
        }
    }
};

void demo() {
    ConfigManager mgr;

    // Reader threads (hot path — zero locks)
    std::vector<std::jthread> readers;
    for (int i = 0; i < 8; ++i) {
        readers.emplace_back([&mgr](std::stop_token st) {
            while (!st.stop_requested()) {
                auto cfg = mgr.get();  // Lock-free atomic load
                float g = cfg->gravity;  // Use config...
                // cfg keeps the config alive even if another thread updates it
            }
        });
    }

    // Writer thread (rare updates)
    std::jthread writer([&mgr](std::stop_token st) {
        while (!st.stop_requested()) {
            std::this_thread::sleep_for(std::chrono::seconds(5));
            mgr.modify([](const GameConfig& old) {
                GameConfig updated = old;
                updated.render_distance += 100.0f;
                return updated;
            });
        }
    });

    std::this_thread::sleep_for(std::chrono::seconds(10));
}

// Pre-C++20 alternative (requires mutex for writes):
// std::shared_mutex mtx;
// std::shared_ptr<const GameConfig> config;
// Read: shared_lock + copy shared_ptr
// Write: unique_lock + swap shared_ptr
// C++20 atomic<shared_ptr> eliminates the mutex entirely for reads!
```

</details>

### Example 8.3 — Coroutines with Asio — Async TCP Server

**Problem:** Build an async TCP echo server using C++20 coroutines with Boost.Asio. Handle multiple concurrent connections without threads.

<details>
<summary>🔍 Full step-by-step solution</summary>

```cpp
#include <boost/asio.hpp>
#include <boost/asio/co_spawn.hpp>
#include <boost/asio/detached.hpp>
#include <boost/asio/use_awaitable.hpp>
#include <fmt/core.h>

namespace asio = boost::asio;
using tcp = asio::ip::tcp;

// A coroutine that handles one client connection
asio::awaitable<void> handle_client(tcp::socket socket) {
    auto endpoint = socket.remote_endpoint();
    fmt::print("Client connected: {}:{}\n",
        endpoint.address().to_string(), endpoint.port());

    try {
        char buffer[1024];
        while (true) {
            // co_await suspends this coroutine until data arrives
            // The event loop can handle other connections meanwhile
            std::size_t n = co_await socket.async_read_some(
                asio::buffer(buffer), asio::use_awaitable);

            // Echo back
            co_await asio::async_write(socket,
                asio::buffer(buffer, n), asio::use_awaitable);
        }
    } catch (const std::exception& e) {
        fmt::print("Client disconnected: {}\n", e.what());
    }
}

// A coroutine that accepts new connections
asio::awaitable<void> listener(tcp::acceptor acceptor) {
    while (true) {
        // co_await suspends until a new connection arrives
        tcp::socket socket = co_await acceptor.async_accept(asio::use_awaitable);

        // Spawn a new coroutine for this client (non-blocking)
        asio::co_spawn(acceptor.get_executor(),
            handle_client(std::move(socket)), asio::detached);
    }
}

int main() {
    asio::io_context ctx;

    tcp::acceptor acceptor(ctx, {tcp::v4(), 8080});
    fmt::print("Server listening on port 8080\n");

    // Spawn the listener coroutine
    asio::co_spawn(ctx, listener(std::move(acceptor)), asio::detached);

    // Run the event loop (single-threaded, handles thousands of connections)
    ctx.run();
}

// How coroutines work under the hood:
// 1. co_await suspends the function, saving its state to the heap
// 2. Control returns to the event loop (io_context::run)
// 3. When the I/O completes, the event loop resumes the coroutine
// 4. The coroutine continues from where it left off
//
// This is cooperative multitasking: no threads, no locks, no races
// One thread can handle 10,000+ concurrent connections (like Node.js)
```

</details>



---

## 📘 9. Appendix: Extended Derivations & Special Cases

### 9.1 Memory Ordering — Acquire/Release/SeqCst Intuition

**Memory ordering is the most misunderstood topic in concurrent C++.** The hardware reorders memory operations for performance. Memory orderings tell the compiler and CPU what reorderings are forbidden.

#### The Problem: Why Ordering Matters

```cpp
// Thread 1:                    // Thread 2:
data = 42;          // (A)      if (ready.load()) {       // (C)
ready.store(true);  // (B)          assert(data == 42);   // (D)
                                }
```

Without ordering guarantees, Thread 2 might see `ready == true` but `data == 0` because:
1. The CPU reordered store (A) after store (B)
2. Or Thread 2's CPU hasn't seen store (A) yet despite seeing (B)

#### The Three Main Orderings

**`memory_order_relaxed`** — No ordering guarantees. Only atomicity.
```cpp
// Use for: counters, statistics, progress indicators
// Thread 1 increments, Thread 2 reads — don't care about other variables
std::atomic<int> counter{0};
counter.fetch_add(1, std::memory_order_relaxed);  // Just atomic, no fence
```

**`memory_order_acquire` / `memory_order_release`** — The workhorse pair.
```cpp
// RELEASE store: all writes BEFORE this store are visible to anyone
// who does an ACQUIRE load of this same atomic and sees this value.
//
// Think of it as: release PUBLISHES, acquire SUBSCRIBES

std::atomic<bool> ready{false};
int data = 0;

// Producer (release):
data = 42;                                    // Happens-before the store
ready.store(true, std::memory_order_release); // PUBLISH point

// Consumer (acquire):
while (!ready.load(std::memory_order_acquire)) {}  // SUBSCRIBE point
assert(data == 42);  // GUARANTEED: sees all writes before the release store
```

**`memory_order_seq_cst`** — The default. Total order across all threads.
```cpp
// All seq_cst operations appear in a single global order that all threads agree on.
// Most expensive, but easiest to reason about.
// This is the DEFAULT if you don't specify an ordering.

std::atomic<int> x{0}, y{0};

// Thread 1:
x.store(1);  // seq_cst by default

// Thread 2:
y.store(1);  // seq_cst by default

// Thread 3:
if (x.load() == 1 && y.load() == 0) {
    // If we see x=1, y=0, then ALL threads agree x was stored before y
}
```

#### When to Use Each

| Ordering | Use Case | Cost (x86) | Cost (ARM) |
|----------|----------|------------|------------|
| `relaxed` | Counters, statistics | Free | Free |
| `acquire/release` | Producer-consumer, publish data | Free (x86 has strong model) | Fence instructions |
| `seq_cst` | When you need total order | MFENCE on stores | Full barrier |

**On x86:** acquire/release are free (x86 has a strong memory model — stores are never reordered with other stores). Only seq_cst adds an MFENCE instruction.

**On ARM/RISC-V:** All orderings stronger than relaxed require explicit fence instructions (dmb, fence).

### 9.2 CAS-Based Lock-Free Queue (Multi-Producer Multi-Consumer)

**A lock-free MPMC queue allows multiple threads to enqueue and dequeue simultaneously without any mutex.** This is the gold standard for inter-thread communication in game engines and audio systems.

```cpp
#include <atomic>
#include <optional>
#include <vector>
#include <cassert>

// Michael-Scott lock-free queue (simplified, bounded)
template<typename T, size_t Capacity>
class LockFreeQueue {
    struct Cell {
        std::atomic<size_t> sequence;
        T data;
    };

    std::vector<Cell> buffer_;
    alignas(64) std::atomic<size_t> enqueue_pos_{0};
    alignas(64) std::atomic<size_t> dequeue_pos_{0};
    // alignas(64): prevent false sharing between producer and consumer

public:
    LockFreeQueue() : buffer_(Capacity) {
        for (size_t i = 0; i < Capacity; ++i) {
            buffer_[i].sequence.store(i, std::memory_order_relaxed);
        }
    }

    bool try_push(const T& value) {
        size_t pos = enqueue_pos_.load(std::memory_order_relaxed);
        while (true) {
            Cell& cell = buffer_[pos % Capacity];
            size_t seq = cell.sequence.load(std::memory_order_acquire);
            intptr_t diff = static_cast<intptr_t>(seq) - static_cast<intptr_t>(pos);

            if (diff == 0) {
                // Cell is ready for writing
                if (enqueue_pos_.compare_exchange_weak(pos, pos + 1,
                        std::memory_order_relaxed)) {
                    // Won the race — write data
                    cell.data = value;
                    cell.sequence.store(pos + 1, std::memory_order_release);
                    return true;
                }
            } else if (diff < 0) {
                // Queue is full
                return false;
            } else {
                // Another thread advanced enqueue_pos — retry
                pos = enqueue_pos_.load(std::memory_order_relaxed);
            }
        }
    }

    std::optional<T> try_pop() {
        size_t pos = dequeue_pos_.load(std::memory_order_relaxed);
        while (true) {
            Cell& cell = buffer_[pos % Capacity];
            size_t seq = cell.sequence.load(std::memory_order_acquire);
            intptr_t diff = static_cast<intptr_t>(seq) - static_cast<intptr_t>(pos + 1);

            if (diff == 0) {
                // Cell has data ready
                if (dequeue_pos_.compare_exchange_weak(pos, pos + 1,
                        std::memory_order_relaxed)) {
                    T value = std::move(cell.data);
                    cell.sequence.store(pos + Capacity, std::memory_order_release);
                    return value;
                }
            } else if (diff < 0) {
                // Queue is empty
                return std::nullopt;
            } else {
                pos = dequeue_pos_.load(std::memory_order_relaxed);
            }
        }
    }
};

// Usage: game engine audio thread communication
// Main thread produces audio commands, audio thread consumes them
LockFreeQueue<AudioCommand, 4096> audio_queue;

// Main thread (producer):
audio_queue.try_push(AudioCommand::PlaySound("explosion.wav"));

// Audio thread (consumer):
if (auto cmd = audio_queue.try_pop()) {
    process_audio_command(*cmd);
}
```

**Why lock-free matters for games:**
- Mutex lock/unlock: ~25ns best case, unbounded worst case (thread sleeping)
- CAS operation: ~5-15ns, bounded retry (no sleeping, no context switch)
- For audio (5ms budget per buffer): a mutex stall can cause audible glitches
- For rendering (16ms budget): lock contention causes frame drops

### 9.3 Coroutine Internals — How the Compiler Transforms Your Code

**A coroutine is a function that can suspend and resume.** The compiler transforms it into a state machine with heap-allocated frame storage.

```cpp
// What you write:
task<int> compute() {
    int a = co_await async_read();
    int b = co_await async_read();
    co_return a + b;
}

// What the compiler generates (conceptual):
struct compute_frame {
    // Promise object (controls coroutine behavior)
    task<int>::promise_type promise;

    // Suspension state
    int suspend_point = 0;  // Which co_await are we at?

    // Local variables (must survive across suspensions)
    int a, b;

    // The state machine
    void resume() {
        switch (suspend_point) {
            case 0: goto start;
            case 1: goto after_first_await;
            case 2: goto after_second_await;
        }
        start:
            // co_await async_read() — first
            suspend_point = 1;
            if (!async_read_awaiter.await_ready()) {
                async_read_awaiter.await_suspend(handle);
                return;  // Suspend!
            }
        after_first_await:
            a = async_read_awaiter.await_resume();

            // co_await async_read() — second
            suspend_point = 2;
            if (!async_read_awaiter.await_ready()) {
                async_read_awaiter.await_suspend(handle);
                return;  // Suspend!
            }
        after_second_await:
            b = async_read_awaiter.await_resume();

            promise.return_value(a + b);
    }
};
```

**Key insight:** The coroutine frame is heap-allocated (like a closure), and `resume()` is called each time the coroutine is continued. The compiler's optimizer can often elide the heap allocation (HALO — Heap Allocation eLision Optimization) when the coroutine's lifetime is bounded.

---

*Next: [09.7 - Performance - SIMD, Memory Layout & Cache Optimization](09.7---Performance---SIMD,-Memory-Layout-&-Cache-Optimization) →*