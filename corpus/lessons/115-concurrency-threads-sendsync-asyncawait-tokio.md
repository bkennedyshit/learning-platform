---
title: "11.5 — Concurrency: Threads, Send/Sync, async/await & Tokio"
subject: "Rust"
catalog: advanced
audience_tier: higher-education
chapter: "11.5"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 11.5 — Concurrency: Threads, Send/Sync, async/await & Tokio

> *"Fearless concurrency is Rust's killer feature. The type system prevents data races at compile time — not with runtime locks you might forget, but with types you can't circumvent."* — Niko Matsakis

You know Python's GIL problem ([08.4 - Concurrency - asyncio, threading, multiprocessing & the GIL](08.4---Concurrency---asyncio,-threading,-multiprocessing-&-the-GIL)): threads exist but can't run Python bytecode in parallel. You need `multiprocessing` for true parallelism, paying serialization costs. Rust has **no GIL**. Threads run in true parallel. And the ownership system guarantees at compile time that you won't have data races.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Spawn OS threads and share data safely with `Arc<Mutex<T>>`.
2. Explain `Send` and `Sync` marker traits and why they prevent data races.
3. Use channels (`mpsc`, `crossbeam`) for message passing.
4. Write async code with `async/await` and the Tokio runtime.
5. Choose between threads vs async for a given workload.
6. Contrast Rust's concurrency model with Python's GIL-constrained model.

---

## 🖼️ Visual Anchor — Rust Concurrency Model vs Python

![rust__14.5-fig1](rust__14.5-fig1.svg)

---

## 📚 1. Concepts

### Concept 14.5.1 — No GIL, True Parallelism

| Feature | Python | Rust |
|---------|--------|------|
| Threads run in parallel | ❌ (GIL) | ✅ |
| Data race prevention | Runtime (locks you might forget) | Compile time (type system) |
| Shared mutable state | Possible (and dangerous) | Requires `Arc<Mutex<T>>` (enforced) |
| Async model | Single-threaded event loop | Multi-threaded work-stealing (Tokio) |
| CPU parallelism | `multiprocessing` (separate processes) | `std::thread` (shared memory) |

### Concept 14.5.2 — Send and Sync (The Magic Traits)

These two marker traits are the foundation of Rust's fearless concurrency:

```rust
// Send: A type can be TRANSFERRED to another thread
// (ownership can cross thread boundaries)
unsafe trait Send {}

// Sync: A type can be SHARED between threads via references
// (multiple threads can hold &T simultaneously)
unsafe trait Sync {}
```

**Key relationships:**
- `T: Send` → you can move `T` into another thread
- `T: Sync` → `&T` is `Send` (you can share references across threads)
- Most types are `Send + Sync` automatically
- `Rc<T>` is NOT Send (reference counting isn't atomic)
- `Arc<T>` IS Send + Sync (atomic reference counting)
- `Cell<T>` / `RefCell<T>` are NOT Sync (interior mutability without synchronization)
- `Mutex<T>` IS Sync (provides synchronized interior mutability)

```rust
use std::thread;

fn must_be_send<T: Send>(_: T) {}
fn must_be_sync<T: Sync>(_: &T) {}

fn main() {
    let s = String::from("hello");
    must_be_send(s);  // ✅ String is Send

    let rc = std::rc::Rc::new(42);
    // must_be_send(rc);  // ❌ COMPILE ERROR: Rc<i32> is not Send

    let arc = std::sync::Arc::new(42);
    must_be_send(arc.clone());  // ✅ Arc<i32> is Send
    must_be_sync(&arc);         // ✅ Arc<i32> is Sync
}
```

### Concept 14.5.3 — Why Data Races Are Impossible

A data race requires three conditions simultaneously:
1. Two or more threads access the same memory
2. At least one access is a write
3. No synchronization

Rust's ownership system prevents this at compile time:
- **Ownership**: Only one thread can own mutable data (move semantics)
- **Borrowing**: `&mut T` is exclusive — can't exist alongside any other reference
- **Send/Sync**: The compiler rejects code that would share non-thread-safe types

```rust
use std::thread;

fn main() {
    let mut data = vec![1, 2, 3];

    // ❌ COMPILE ERROR: can't borrow `data` as mutable in multiple threads
    // thread::spawn(|| {
    //     data.push(4);  // Would need &mut data
    // });
    // data.push(5);      // Also needs &mut data — conflict!

    // ✅ Move ownership to the thread:
    thread::spawn(move || {
        data.push(4);  // Thread owns data exclusively
        println!("{data:?}");
    });
    // data is no longer accessible here — moved into thread
}
```

---

## 📐 2. Mental Models

### Model 14.5.1 — Python GIL vs Rust Ownership (The Contrast)

**Python's approach**: "Let all threads access everything, but serialize execution with the GIL."
- Result: Threads can't run Python in parallel. You get concurrency but not parallelism.
- For CPU work: Must use `multiprocessing` (separate address spaces, serialization overhead).

**Rust's approach**: "Let threads run in true parallel, but enforce at compile time that shared data is properly synchronized."
- Result: True parallelism with zero-cost safety guarantees.
- No runtime overhead for the safety checks — they happen at compile time.

### Model 14.5.2 — Channels as Typed Pipes

Think of channels as **typed Unix pipes** between threads:

```
Thread A ──── [mpsc::Sender<Message>] ────→ [mpsc::Receiver<Message>] ──── Thread B
              (can be cloned for              (single consumer)
               multiple producers)
```

### Model 14.5.3 — async/await as Cooperative Multitasking

- **Threads**: OS schedules them preemptively (can interrupt at any point)
- **async tasks**: You yield control explicitly at `.await` points (cooperative)

```
Thread 1:  [Task A runs] → [.await → yields] → [Task B runs] → [.await → yields] → [Task A resumes]
Thread 2:  [Task C runs] → [.await → yields] → [Task D runs] → ...
```

Tokio's work-stealing scheduler distributes tasks across a thread pool.

---

## 🔑 3. Mechanics

### 3.1 — Spawning Threads

```rust
use std::thread;
use std::time::Duration;

fn main() {
    // Spawn a thread — must move data in (can't borrow from parent)
    let data = vec![1, 2, 3, 4, 5];

    let handle = thread::spawn(move || {
        // `move` transfers ownership of `data` into this closure
        let sum: i32 = data.iter().sum();
        println!("Sum: {sum}");
        sum  // Return value from thread
    });

    // Wait for thread to finish and get its return value
    let result = handle.join().unwrap();  // Result<i32, Box<dyn Any>>
    println!("Thread returned: {result}");
}
```

### 3.2 — Shared State with Arc<Mutex<T>>

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    // Arc: atomic reference counting (thread-safe Rc)
    // Mutex: mutual exclusion (only one thread can access at a time)
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);  // Clone the Arc (cheap: increments refcount)
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();  // Acquire lock
            *num += 1;
            // Lock automatically released when `num` goes out of scope (RAII)
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Final count: {}", *counter.lock().unwrap());  // 10
}
```

### 3.3 — Message Passing with Channels

```rust
use std::sync::mpsc;  // Multi-Producer, Single-Consumer
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    // Multiple producers (clone the sender)
    for i in 0..5 {
        let tx = tx.clone();
        thread::spawn(move || {
            tx.send(format!("Message from thread {i}")).unwrap();
        });
    }
    drop(tx);  // Drop original sender so rx.iter() terminates

    // Single consumer
    for msg in rx {
        println!("Received: {msg}");
    }
}
```

### 3.4 — async/await with Tokio

```rust
use tokio;

#[tokio::main]  // Sets up the Tokio runtime
async fn main() {
    // Spawn concurrent tasks
    let task1 = tokio::spawn(async {
        tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
        "Task 1 done"
    });

    let task2 = tokio::spawn(async {
        tokio::time::sleep(tokio::time::Duration::from_millis(500)).await;
        "Task 2 done"
    });

    // Await both (they run concurrently)
    let (r1, r2) = tokio::join!(task1, task2);
    println!("{}", r1.unwrap());
    println!("{}", r2.unwrap());
}
```

### 3.5 — Async HTTP Client (Real-World Pattern)

```rust
use reqwest;
use tokio;
use anyhow::Result;

#[tokio::main]
async fn main() -> Result<()> {
    let urls = vec![
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/1",
    ];

    // Fetch all URLs concurrently (like asyncio.gather in Python)
    let mut tasks = vec![];
    for url in urls {
        tasks.push(tokio::spawn(async move {
            let resp = reqwest::get(url).await?;
            let status = resp.status();
            Ok::<_, reqwest::Error>(format!("{url} -> {status}"))
        }));
    }

    for task in tasks {
        match task.await? {
            Ok(result) => println!("{result}"),
            Err(e) => eprintln!("Request failed: {e}"),
        }
    }

    Ok(())
}
```

### 3.6 — Tokio Channels (Async Message Passing)

```rust
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    // Bounded channel (backpressure when full)
    let (tx, mut rx) = mpsc::channel::<String>(32);

    // Producer task
    let producer = tokio::spawn(async move {
        for i in 0..10 {
            tx.send(format!("item {i}")).await.unwrap();
            tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
        }
    });

    // Consumer task
    let consumer = tokio::spawn(async move {
        while let Some(msg) = rx.recv().await {
            println!("Processing: {msg}");
        }
    });

    let _ = tokio::join!(producer, consumer);
}
```

### 3.7 — Scoped Threads (Borrowing from Parent)

```rust
use std::thread;

fn main() {
    let mut data = vec![1, 2, 3, 4, 5, 6, 7, 8];

    // Scoped threads CAN borrow from the parent stack
    // (guaranteed to finish before the scope exits)
    thread::scope(|s| {
        let (left, right) = data.split_at_mut(4);

        s.spawn(|| {
            for item in left.iter_mut() {
                *item *= 2;
            }
        });

        s.spawn(|| {
            for item in right.iter_mut() {
                *item *= 3;
            }
        });
    });
    // Both threads guaranteed finished here

    println!("{data:?}");  // [2, 4, 6, 8, 15, 18, 21, 24]
}
```

### 3.8 — When to Use Threads vs Async

| Workload | Use | Why |
|----------|-----|-----|
| CPU-bound computation | `std::thread` or `rayon` | True parallelism, no executor overhead |
| Many network connections | `tokio` async | Thousands of tasks on few threads |
| File I/O | `tokio::fs` or `spawn_blocking` | Don't block the async executor |
| Mixed CPU + I/O | Async + `spawn_blocking` | Async for I/O, blocking pool for CPU |
| Simple parallelism | `rayon` (data parallelism) | `.par_iter()` — parallel iterators |

```rust
// rayon: parallel iterators (dead simple)
use rayon::prelude::*;

fn main() {
    let numbers: Vec<u64> = (0..1_000_000).collect();

    // Sequential
    let sum_seq: u64 = numbers.iter().map(|&n| n * n).sum();

    // Parallel (just change .iter() to .par_iter())
    let sum_par: u64 = numbers.par_iter().map(|&n| n * n).sum();

    assert_eq!(sum_seq, sum_par);
}
```

---

## 💡 4. Worked Examples

### Example 11.5.1 — Parallel Web Scraper

```rust
use reqwest;
use tokio;
use tokio::sync::Semaphore;
use std::sync::Arc;
use anyhow::Result;

struct Scraper {
    client: reqwest::Client,
    semaphore: Arc<Semaphore>,  // Limit concurrent requests
}

impl Scraper {
    fn new(max_concurrent: usize) -> Self {
        Self {
            client: reqwest::Client::new(),
            semaphore: Arc::new(Semaphore::new(max_concurrent)),
        }
    }

    async fn fetch(&self, url: &str) -> Result<String> {
        let _permit = self.semaphore.acquire().await?;  // Rate limiting
        let response = self.client.get(url).send().await?;
        let body = response.text().await?;
        Ok(body)
    }

    async fn fetch_all(&self, urls: Vec<String>) -> Vec<Result<String>> {
        let mut tasks = vec![];

        for url in urls {
            let client = self.client.clone();
            let sem = self.semaphore.clone();
            tasks.push(tokio::spawn(async move {
                let _permit = sem.acquire().await.unwrap();
                let resp = client.get(&url).send().await?;
                Ok::<_, anyhow::Error>(resp.text().await?)
            }));
        }

        let mut results = vec![];
        for task in tasks {
            results.push(task.await.unwrap());
        }
        results
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    let scraper = Scraper::new(10);  // Max 10 concurrent requests
    let urls: Vec<String> = (0..100)
        .map(|i| format!("https://httpbin.org/get?id={i}"))
        .collect();

    let results = scraper.fetch_all(urls).await;
    let successes = results.iter().filter(|r| r.is_ok()).count();
    println!("Fetched {successes}/100 successfully");
    Ok(())
}
```

### Example 11.5.2 — Thread Pool with Work Stealing

```rust
use std::sync::{Arc, Mutex};
use std::thread;
use std::collections::VecDeque;

type Job = Box<dyn FnOnce() + Send + 'static>;

struct ThreadPool {
    workers: Vec<thread::JoinHandle<()>>,
    sender: std::sync::mpsc::Sender<Job>,
}

impl ThreadPool {
    fn new(size: usize) -> Self {
        let (sender, receiver) = std::sync::mpsc::channel::<Job>();
        let receiver = Arc::new(Mutex::new(receiver));
        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            let receiver = Arc::clone(&receiver);
            workers.push(thread::spawn(move || {
                loop {
                    let job = receiver.lock().unwrap().recv();
                    match job {
                        Ok(job) => {
                            println!("Worker {id} executing job");
                            job();
                        }
                        Err(_) => {
                            println!("Worker {id} shutting down");
                            break;
                        }
                    }
                }
            }));
        }

        ThreadPool { workers, sender }
    }

    fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        self.sender.send(Box::new(f)).unwrap();
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        drop(self.sender.clone());  // Signal workers to stop
        // Note: proper implementation would use a separate shutdown signal
    }
}
```

### Example 11.5.3 — Actor Pattern with Tokio

```rust
use tokio::sync::{mpsc, oneshot};

// Messages the actor can receive
enum ActorMessage {
    GetCount { respond_to: oneshot::Sender<u64> },
    Increment { amount: u64 },
    Reset,
}

// The actor
struct CounterActor {
    count: u64,
    receiver: mpsc::Receiver<ActorMessage>,
}

impl CounterActor {
    fn new(receiver: mpsc::Receiver<ActorMessage>) -> Self {
        Self { count: 0, receiver }
    }

    async fn run(&mut self) {
        while let Some(msg) = self.receiver.recv().await {
            match msg {
                ActorMessage::GetCount { respond_to } => {
                    let _ = respond_to.send(self.count);
                }
                ActorMessage::Increment { amount } => {
                    self.count += amount;
                }
                ActorMessage::Reset => {
                    self.count = 0;
                }
            }
        }
    }
}

// Handle for interacting with the actor
#[derive(Clone)]
struct CounterHandle {
    sender: mpsc::Sender<ActorMessage>,
}

impl CounterHandle {
    fn new() -> Self {
        let (sender, receiver) = mpsc::channel(32);
        let mut actor = CounterActor::new(receiver);
        tokio::spawn(async move { actor.run().await });
        Self { sender }
    }

    async fn get_count(&self) -> u64 {
        let (tx, rx) = oneshot::channel();
        self.sender.send(ActorMessage::GetCount { respond_to: tx }).await.unwrap();
        rx.await.unwrap()
    }

    async fn increment(&self, amount: u64) {
        self.sender.send(ActorMessage::Increment { amount }).await.unwrap();
    }
}

#[tokio::main]
async fn main() {
    let counter = CounterHandle::new();

    // Multiple tasks can safely interact with the actor
    let mut tasks = vec![];
    for _ in 0..100 {
        let counter = counter.clone();
        tasks.push(tokio::spawn(async move {
            counter.increment(1).await;
        }));
    }

    for task in tasks {
        task.await.unwrap();
    }

    println!("Final count: {}", counter.get_count().await);  // 100
}
```

---

## ⚠️ 5. Gotchas & Common Mistakes

### Gotcha 14.5.1 — Don't Block the Async Runtime

```rust
// BAD: Blocking call inside async context
async fn bad_example() {
    std::thread::sleep(Duration::from_secs(5));  // Blocks the entire executor thread!
    std::fs::read_to_string("big_file.txt");     // Also blocking!
}

// GOOD: Use async equivalents or spawn_blocking
async fn good_example() {
    tokio::time::sleep(Duration::from_secs(5)).await;  // Yields to other tasks
    tokio::fs::read_to_string("big_file.txt").await;   // Async file I/O

    // For CPU-heavy work or unavoidable blocking:
    let result = tokio::task::spawn_blocking(|| {
        expensive_computation()  // Runs on a dedicated blocking thread pool
    }).await.unwrap();
}
```

### Gotcha 14.5.2 — Mutex Poisoning

```rust
use std::sync::Mutex;

let data = Mutex::new(vec![1, 2, 3]);

// If a thread panics while holding the lock, the mutex is "poisoned"
// Subsequent lock() calls return Err(PoisonError)
let result = data.lock();
match result {
    Ok(guard) => println!("{guard:?}"),
    Err(poisoned) => {
        // You can still access the data (it might be in an inconsistent state)
        let guard = poisoned.into_inner();
        println!("Recovered: {guard:?}");
    }
}

// In practice, most code just unwraps (panic propagation is usually fine):
let guard = data.lock().unwrap();

// Or use parking_lot::Mutex which doesn't have poisoning:
// use parking_lot::Mutex;  // No poisoning, slightly faster
```

### Gotcha 14.5.3 — Deadlocks (Rust Prevents Data Races, Not Deadlocks)

```rust
// Rust's type system prevents DATA RACES but NOT DEADLOCKS
// You can still deadlock with multiple mutexes:

use std::sync::{Arc, Mutex};

let a = Arc::new(Mutex::new(1));
let b = Arc::new(Mutex::new(2));

// Thread 1: locks a, then b
// Thread 2: locks b, then a
// → DEADLOCK (neither can proceed)

// Prevention: always acquire locks in the same order
// Or use try_lock() with timeout
```

### Gotcha 14.5.4 — async fn Returns a Future (Not a Value)

```rust
// Calling an async fn does NOT execute it — it returns a Future
async fn compute() -> i32 { 42 }

fn main() {
    let future = compute();  // Nothing happens yet!
    // future is a Future<Output = i32>, not an i32

    // Must .await it (inside async context) or block on it:
    let rt = tokio::runtime::Runtime::new().unwrap();
    let result = rt.block_on(future);  // NOW it executes
    println!("{result}");
}
```

---

## 🔗 6. Cross-Links

- **Next**: [11.6 - Memory - Box, Rc, Arc, RefCell, Mutex](11.6---Memory---Box,-Rc,-Arc,-RefCell,-Mutex) — Deep dive into Arc, Mutex, and when to use each
- **Python contrast**: [08.4 - Concurrency - asyncio, threading, multiprocessing & the GIL](08.4---Concurrency---asyncio,-threading,-multiprocessing-&-the-GIL) — The GIL problem Rust solves
- **Ownership foundation**: [11.2 - Ownership, Borrowing & Lifetimes](11.2---Ownership,-Borrowing-&-Lifetimes) — Why Send/Sync work
- **Production async**: [11.8 - Production Rust - WebAssembly, FFI, Embedded & Game Dev (Bevy)](11.8---Production-Rust---WebAssembly,-FFI,-Embedded-&-Game-Dev-(Bevy)) — Async in web servers

---

## 📖 7. References

- [The Rust Book, Ch. 16: Fearless Concurrency](https://doc.rust-lang.org/book/ch16-00-concurrency.html)
- [Rust Atomics and Locks (Mara Bos) — Free online](https://marabos.nl/atomics/)
- [Tokio Tutorial](https://tokio.rs/tokio/tutorial)
- [Jon Gjengset: "Crust of Rust: Send, Sync, and their implementors"](https://www.youtube.com/watch?v=yOezcP-XaIw)
- [Alice Ryhl: "Actors with Tokio"](https://ryhl.io/blog/actors-with-tokio/)


---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — Tokio spawn vs spawn_blocking vs spawn_local

**Problem:** You have three types of work: CPU-heavy computation, blocking file I/O, and async network I/O. Demonstrate the correct Tokio primitive for each and explain what happens if you use the wrong one.

<details>
<summary>🔍 Full step-by-step solution</summary>

```rust
use tokio::time::{sleep, Duration, Instant};
use std::thread;

// ============================================================
// tokio::spawn — for async tasks (non-blocking, Send + 'static)
// ============================================================
// Runs on the multi-threaded runtime's worker threads.
// The task is moved between threads (requires Send).
// NEVER block inside a spawned task.

async fn network_io_task(url: String) -> Result<String, reqwest::Error> {
    // ✅ CORRECT: async I/O yields at .await points
    let response = reqwest::get(&url).await?;
    let body = response.text().await?;
    Ok(body)
}

// ============================================================
// tokio::task::spawn_blocking — for blocking/CPU work
// ============================================================
// Runs on a SEPARATE thread pool (default: 512 threads).
// Does NOT block the async executor's worker threads.
// Use for: file I/O, CPU computation, calling sync libraries.

async fn cpu_heavy_task(data: Vec<u8>) -> Vec<u8> {
    // ✅ CORRECT: CPU work on blocking thread pool
    tokio::task::spawn_blocking(move || {
        // This runs on a dedicated blocking thread
        // It's OK to spend seconds here without yielding
        let mut result = data;
        for _ in 0..1000 {
            result = result.iter().map(|b| b.wrapping_mul(7).wrapping_add(3)).collect();
        }
        result
    })
    .await
    .expect("blocking task panicked")
}

async fn blocking_file_io(path: String) -> std::io::Result<String> {
    // ✅ CORRECT: std::fs is blocking — use spawn_blocking
    tokio::task::spawn_blocking(move || {
        std::fs::read_to_string(&path)
    })
    .await
    .expect("blocking task panicked")
}

// Alternative: use tokio::fs which wraps spawn_blocking internally
async fn async_file_io(path: &str) -> std::io::Result<String> {
    tokio::fs::read_to_string(path).await
    // Internally: spawn_blocking(|| std::fs::read_to_string(path))
}

// ============================================================
// tokio::task::spawn_local — for !Send futures (single-threaded)
// ============================================================
// Runs on the CURRENT thread only (never moved to another thread).
// Use for: Rc, RefCell, or other !Send types in async code.
// Requires a LocalSet.

use std::rc::Rc;
use std::cell::RefCell;

async fn local_task_demo() {
    let local = tokio::task::LocalSet::new();
    
    local.run_until(async {
        let shared_state = Rc::new(RefCell::new(Vec::new()));
        
        // spawn_local: task stays on this thread (Rc is !Send)
        let state = shared_state.clone();
        tokio::task::spawn_local(async move {
            state.borrow_mut().push("from local task");
            sleep(Duration::from_millis(10)).await;
            state.borrow_mut().push("after sleep");
        }).await.unwrap();
        
        println!("State: {:?}", shared_state.borrow());
    }).await;
}

// ============================================================
// WHAT HAPPENS IF YOU USE THE WRONG ONE
// ============================================================

async fn bad_blocking_in_async() {
    // ❌ BAD: Blocking the async executor thread
    // This prevents ALL other tasks on this thread from making progress!
    thread::sleep(Duration::from_secs(5));  // Blocks executor!
    std::fs::read_to_string("big_file.txt"); // Also blocks!
    
    // Symptoms:
    // - Other tasks appear to "hang"
    // - Timeouts fire unexpectedly
    // - Throughput drops to near-zero
    // - tokio-console shows "blocked" worker threads
}

async fn bad_spawn_with_rc() {
    let data = Rc::new(42);
    // ❌ COMPILE ERROR: Rc is !Send, can't use with tokio::spawn
    // tokio::spawn(async move {
    //     println!("{}", data);
    // });
    // error: `Rc<i32>` cannot be sent between threads safely
    
    // ✅ Fix: use Arc instead of Rc for cross-thread sharing
    let data = std::sync::Arc::new(42);
    tokio::spawn(async move {
        println!("{}", data);
    }).await.unwrap();
}

// ============================================================
// COMPLETE EXAMPLE: Mixing all three correctly
// ============================================================

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let start = Instant::now();
    
    // Launch concurrent tasks of different types
    let network = tokio::spawn(async {
        // Async network I/O — yields at .await
        sleep(Duration::from_millis(100)).await;
        "network done".to_string()
    });
    
    let cpu = tokio::task::spawn_blocking(|| {
        // CPU-heavy work — runs on blocking pool
        let mut sum: u64 = 0;
        for i in 0..10_000_000 {
            sum = sum.wrapping_add(i);
        }
        format!("cpu done: {sum}")
    });
    
    let file = tokio::task::spawn_blocking(|| {
        // Blocking file I/O — runs on blocking pool
        thread::sleep(Duration::from_millis(50));  // Simulated
        "file done".to_string()
    });
    
    // Await all concurrently
    let (net_result, cpu_result, file_result) = tokio::join!(network, cpu, file);
    
    println!("{}", net_result?);
    println!("{}", cpu_result?);
    println!("{}", file_result?);
    println!("Total time: {:?}", start.elapsed());
    // ~100ms (not 150ms+ — they ran concurrently!)
    
    Ok(())
}
```

</details>

### Example 8.2 — Channel Patterns: mpsc, oneshot, broadcast, watch

**Problem:** Implement a task coordination system using all four Tokio channel types. Show when each is appropriate and how they compose.

<details>
<summary>🔍 Full step-by-step solution</summary>

```rust
use tokio::sync::{mpsc, oneshot, broadcast, watch};
use tokio::time::{sleep, Duration};

// ============================================================
// mpsc — Multi-Producer, Single-Consumer (work queue)
// ============================================================
// Use for: task queues, event streams, actor mailboxes
// Bounded: backpressure when full (sender.send().await blocks)
// Unbounded: no backpressure (can OOM if consumer is slow)

async fn mpsc_demo() {
    let (tx, mut rx) = mpsc::channel::<String>(32);  // Buffer size 32
    
    // Multiple producers
    for i in 0..5 {
        let tx = tx.clone();
        tokio::spawn(async move {
            tx.send(format!("message from producer {i}")).await.unwrap();
        });
    }
    drop(tx);  // Drop original sender so rx knows when all producers are done
    
    // Single consumer
    while let Some(msg) = rx.recv().await {
        println!("Received: {msg}");
    }
    println!("All producers finished");
}

// ============================================================
// oneshot — Single-Producer, Single-Consumer, Single-Message
// ============================================================
// Use for: request-response patterns, task completion signals
// Sending consumes the sender (can only send once)

async fn oneshot_demo() {
    // Pattern: spawn a task and get its result via oneshot
    let (tx, rx) = oneshot::channel::<u64>();
    
    tokio::spawn(async move {
        // Do expensive work
        sleep(Duration::from_millis(100)).await;
        let result = 42 * 42;
        tx.send(result).unwrap();  // Send result back
    });
    
    // Wait for the result
    let answer = rx.await.unwrap();
    println!("Got answer: {answer}");
}

// Pattern: Request-response in an actor
struct DbActor {
    rx: mpsc::Receiver<DbRequest>,
}

struct DbRequest {
    query: String,
    respond_to: oneshot::Sender<Vec<String>>,
}

impl DbActor {
    async fn run(&mut self) {
        while let Some(req) = self.rx.recv().await {
            let results = vec![format!("result for: {}", req.query)];
            let _ = req.respond_to.send(results);
        }
    }
}

async fn query_actor(tx: &mpsc::Sender<DbRequest>, query: &str) -> Vec<String> {
    let (resp_tx, resp_rx) = oneshot::channel();
    tx.send(DbRequest {
        query: query.to_string(),
        respond_to: resp_tx,
    }).await.unwrap();
    resp_rx.await.unwrap()
}

// ============================================================
// broadcast — Multi-Producer, Multi-Consumer (pub/sub)
// ============================================================
// Use for: event broadcasting, pub/sub, notifications
// Every subscriber gets every message (fan-out)
// Slow subscribers get Lagged error (messages dropped)

async fn broadcast_demo() {
    let (tx, _) = broadcast::channel::<String>(16);
    
    // Multiple subscribers
    let mut rx1 = tx.subscribe();
    let mut rx2 = tx.subscribe();
    
    // Publisher
    tokio::spawn(async move {
        for i in 0..5 {
            tx.send(format!("event {i}")).unwrap();
            sleep(Duration::from_millis(10)).await;
        }
    });
    
    // Subscriber 1
    let sub1 = tokio::spawn(async move {
        let mut count = 0;
        while let Ok(msg) = rx1.recv().await {
            println!("Sub1: {msg}");
            count += 1;
        }
        count
    });
    
    // Subscriber 2 (slower)
    let sub2 = tokio::spawn(async move {
        let mut count = 0;
        while let Ok(msg) = rx2.recv().await {
            println!("Sub2: {msg}");
            sleep(Duration::from_millis(20)).await;  // Slow consumer
            count += 1;
        }
        count
    });
    
    // Both subscribers receive all messages independently
}

// ============================================================
// watch — Single-Producer, Multi-Consumer (latest value)
// ============================================================
// Use for: configuration updates, state broadcasting, shutdown signals
// Subscribers only see the LATEST value (not a queue)
// No backpressure — old values are overwritten

async fn watch_demo() {
    #[derive(Clone, Debug)]
    struct AppConfig {
        max_connections: u32,
        log_level: String,
    }
    
    let (tx, rx) = watch::channel(AppConfig {
        max_connections: 100,
        log_level: "info".to_string(),
    });
    
    // Worker tasks subscribe to config changes
    for i in 0..3 {
        let mut rx = rx.clone();
        tokio::spawn(async move {
            loop {
                // Wait for config to change
                rx.changed().await.unwrap();
                let config = rx.borrow().clone();
                println!("Worker {i}: config updated to {:?}", config);
            }
        });
    }
    
    // Config updater
    sleep(Duration::from_millis(100)).await;
    tx.send(AppConfig {
        max_connections: 200,
        log_level: "debug".to_string(),
    }).unwrap();
    
    sleep(Duration::from_millis(100)).await;
}

// ============================================================
// GRACEFUL SHUTDOWN with watch channel
// ============================================================
async fn graceful_shutdown_demo() {
    let (shutdown_tx, shutdown_rx) = watch::channel(false);
    
    // Worker tasks check the shutdown signal
    for i in 0..5 {
        let mut rx = shutdown_rx.clone();
        tokio::spawn(async move {
            loop {
                tokio::select! {
                    _ = rx.changed() => {
                        if *rx.borrow() {
                            println!("Worker {i} shutting down gracefully");
                            return;
                        }
                    }
                    _ = sleep(Duration::from_millis(100)) => {
                        println!("Worker {i} doing work...");
                    }
                }
            }
        });
    }
    
    // Let workers run for a bit
    sleep(Duration::from_millis(500)).await;
    
    // Signal shutdown
    println!("Sending shutdown signal...");
    shutdown_tx.send(true).unwrap();
    
    sleep(Duration::from_millis(100)).await;
    println!("All workers stopped");
}
```

</details>

### Example 8.3 — Rayon for Data Parallelism: Parallel Iterators

**Problem:** Process a large dataset using all CPU cores with minimal code changes. Compare sequential vs parallel performance and show rayon's work-stealing scheduler in action.

<details>
<summary>🔍 Full step-by-step solution</summary>

```rust
use rayon::prelude::*;
use std::time::Instant;

// ============================================================
// BASIC: par_iter() — drop-in replacement for iter()
// ============================================================

fn parallel_map_filter() {
    let data: Vec<u64> = (0..10_000_000).collect();
    
    // Sequential
    let start = Instant::now();
    let seq_result: Vec<u64> = data.iter()
        .filter(|&&x| x % 3 == 0)
        .map(|&x| x * x)
        .collect();
    println!("Sequential: {:?} ({} results)", start.elapsed(), seq_result.len());
    
    // Parallel (just change .iter() to .par_iter())
    let start = Instant::now();
    let par_result: Vec<u64> = data.par_iter()
        .filter(|&&x| x % 3 == 0)
        .map(|&x| x * x)
        .collect();
    println!("Parallel:   {:?} ({} results)", start.elapsed(), par_result.len());
    
    // Typical speedup: 4-8x on 8-core machine
    assert_eq!(seq_result.len(), par_result.len());
}

// ============================================================
// REDUCE: Parallel aggregation
// ============================================================

fn parallel_reduce() {
    let data: Vec<f64> = (0..10_000_000).map(|i| i as f64 * 0.001).collect();
    
    // par_iter().sum() — uses parallel reduction
    let sum: f64 = data.par_iter().sum();
    
    // Custom reduction with reduce()
    let (min, max) = data.par_iter()
        .cloned()
        .reduce(
            || (f64::INFINITY, f64::NEG_INFINITY),  // Identity element
            |(min_a, max_a), (min_b, max_b)| {
                (min_a.min(min_b), max_a.max(max_b))
            },
        );
    // Note: reduce() requires an associative operation
    // (a ⊕ b) ⊕ c == a ⊕ (b ⊕ c)
    
    println!("Sum: {sum:.2}, Min: {min:.4}, Max: {max:.4}");
}

// ============================================================
// PARALLEL SORT
// ============================================================

fn parallel_sort() {
    let mut data: Vec<u64> = (0..10_000_000).rev().collect();
    
    let start = Instant::now();
    data.par_sort_unstable();  // Parallel quicksort
    println!("Parallel sort: {:?}", start.elapsed());
    
    // Also available:
    // par_sort()           — stable parallel sort
    // par_sort_by()        — custom comparator
    // par_sort_by_key()    — sort by extracted key
}

// ============================================================
// PARALLEL CHUNKS: Process independent slices
// ============================================================

fn parallel_chunks() {
    let mut image: Vec<u8> = vec![0; 1920 * 1080 * 4];  // RGBA image
    
    // Process each row in parallel
    image.par_chunks_mut(1920 * 4)  // Each chunk = one row
        .enumerate()
        .for_each(|(y, row)| {
            for x in 0..1920 {
                let offset = x * 4;
                row[offset] = (x % 256) as u8;      // R
                row[offset + 1] = (y % 256) as u8;  // G
                row[offset + 2] = 128;               // B
                row[offset + 3] = 255;               // A
            }
        });
    
    println!("Image processed: {} bytes", image.len());
}

// ============================================================
// CUSTOM THREAD POOL (control parallelism)
// ============================================================

fn custom_pool() {
    // Create a pool with specific thread count
    let pool = rayon::ThreadPoolBuilder::new()
        .num_threads(4)  // Limit to 4 threads
        .thread_name(|i| format!("worker-{i}"))
        .build()
        .unwrap();
    
    // Run work on the custom pool
    pool.install(|| {
        let result: u64 = (0..1_000_000u64)
            .into_par_iter()
            .map(|x| x * x)
            .sum();
        println!("Result: {result}");
    });
}

// ============================================================
// WHEN NOT TO USE RAYON
// ============================================================
// 
// ❌ Small datasets (< 10,000 elements): overhead > benefit
// ❌ I/O-bound work: use tokio instead
// ❌ Work with side effects that need ordering: par_iter is unordered
// ❌ Inside async code: rayon blocks the thread (use spawn_blocking)
//
// ✅ CPU-bound computation on large datasets
// ✅ Image/video processing
// ✅ Scientific computing
// ✅ Sorting large collections
// ✅ Map-reduce operations
```

</details>

### Example 8.4 — Select! Macro: Racing Concurrent Operations

**Problem:** Implement a service that handles multiple event sources simultaneously: incoming requests, a periodic health check timer, and a shutdown signal. Use `tokio::select!` to multiplex.

<details>
<summary>🔍 Full step-by-step solution</summary>

```rust
use tokio::sync::{mpsc, watch};
use tokio::time::{interval, Duration, Instant};

#[derive(Debug)]
enum Request {
    Query(String),
    Status,
}

#[derive(Debug)]
struct Response {
    data: String,
    latency_ms: u64,
}

async fn service_loop(
    mut requests: mpsc::Receiver<Request>,
    mut shutdown: watch::Receiver<bool>,
    health_interval: Duration,
) {
    let mut health_ticker = interval(health_interval);
    let mut request_count: u64 = 0;
    let mut healthy = true;
    let start = Instant::now();
    
    loop {
        // select! races multiple futures — first one to complete wins
        tokio::select! {
            // Branch 1: Incoming request
            Some(request) = requests.recv() => {
                request_count += 1;
                match request {
                    Request::Query(q) => {
                        println!("[{:?}] Processing query: {q}", start.elapsed());
                        // Simulate async processing
                        tokio::time::sleep(Duration::from_millis(10)).await;
                    }
                    Request::Status => {
                        println!("[{:?}] Status: {} requests, healthy={healthy}",
                            start.elapsed(), request_count);
                    }
                }
            }
            
            // Branch 2: Health check timer
            _ = health_ticker.tick() => {
                // Periodic health check
                healthy = check_health().await;
                if !healthy {
                    eprintln!("[{:?}] ⚠️  Health check FAILED", start.elapsed());
                }
            }
            
            // Branch 3: Shutdown signal
            Ok(()) = shutdown.changed() => {
                if *shutdown.borrow() {
                    println!("[{:?}] Shutdown signal received", start.elapsed());
                    println!("Processed {request_count} requests total");
                    break;  // Exit the loop
                }
            }
            
            // Branch 4: All senders dropped (channel closed)
            else => {
                println!("All request senders dropped, shutting down");
                break;
            }
        }
    }
    
    println!("Service loop exited cleanly");
}

async fn check_health() -> bool {
    // Simulate health check (e.g., ping database)
    tokio::time::sleep(Duration::from_millis(5)).await;
    true
}

#[tokio::main]
async fn main() {
    let (req_tx, req_rx) = mpsc::channel(100);
    let (shutdown_tx, shutdown_rx) = watch::channel(false);
    
    // Start the service
    let service = tokio::spawn(service_loop(
        req_rx,
        shutdown_rx,
        Duration::from_millis(500),
    ));
    
    // Send some requests
    for i in 0..10 {
        req_tx.send(Request::Query(format!("SELECT * FROM t{i}"))).await.unwrap();
        tokio::time::sleep(Duration::from_millis(50)).await;
    }
    req_tx.send(Request::Status).await.unwrap();
    
    // Shutdown after 1 second
    tokio::time::sleep(Duration::from_secs(1)).await;
    shutdown_tx.send(true).unwrap();
    
    service.await.unwrap();
}
```

</details>


---

## 📘 9. Appendix: Extended Derivations & Special Cases

### 9.1 Pin and the Future Trait: How async/await Actually Works

Every `async fn` or `async {}` block is compiled into a **state machine** that implements the `Future` trait. Understanding this machinery explains why `Pin` exists and why async code has unique constraints.

**The Future trait:**

```rust
pub trait Future {
    type Output;
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}

pub enum Poll<T> {
    Ready(T),    // Future completed, here's the value
    Pending,     // Not ready yet, will wake you via cx.waker()
}
```

**How the compiler transforms async fn:**

```rust
// What you write:
async fn fetch_data(url: &str) -> String {
    let response = reqwest::get(url).await;  // Suspend point 1
    let body = response.unwrap().text().await;  // Suspend point 2
    body.unwrap()
}

// What the compiler generates (conceptually):
enum FetchDataFuture<'a> {
    // State 0: Before first .await
    Start { url: &'a str },
    // State 1: Waiting for reqwest::get() to complete
    WaitingForGet { url: &'a str, get_future: ReqwestGetFuture },
    // State 2: Waiting for .text() to complete
    WaitingForText { response: Response, text_future: TextFuture },
    // State 3: Completed
    Done,
}

impl<'a> Future for FetchDataFuture<'a> {
    type Output = String;
    
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<String> {
        // State machine: advance through states based on sub-future readiness
        loop {
            match self.get_mut_state() {
                State::Start { url } => {
                    let get_future = reqwest::get(url);
                    self.transition_to(State::WaitingForGet { url, get_future });
                }
                State::WaitingForGet { get_future, .. } => {
                    match Pin::new(get_future).poll(cx) {
                        Poll::Ready(response) => {
                            let text_future = response.unwrap().text();
                            self.transition_to(State::WaitingForText { text_future });
                        }
                        Poll::Pending => return Poll::Pending,
                    }
                }
                State::WaitingForText { text_future, .. } => {
                    match Pin::new(text_future).poll(cx) {
                        Poll::Ready(body) => return Poll::Ready(body.unwrap()),
                        Poll::Pending => return Poll::Pending,
                    }
                }
                State::Done => panic!("polled after completion"),
            }
        }
    }
}
```

**Why Pin is necessary:**

The generated state machine struct may contain **self-references**. For example, if you have:

```rust
async fn example() {
    let data = vec![1, 2, 3];
    let reference = &data;  // reference points to data (same struct!)
    some_async_op().await;
    println!("{:?}", reference);  // reference must still be valid after .await
}
```

The compiled state machine stores both `data` and `reference` as fields. If the struct is moved in memory, `reference` becomes a dangling pointer. `Pin` prevents the struct from being moved after it's been polled, ensuring self-references remain valid.

**Practical implications:**

1. You rarely interact with `Pin` directly — `async/await` handles it
2. When implementing `Future` manually, you must use `Pin<&mut Self>`
3. `Box::pin(future)` creates a pinned, heap-allocated future
4. `tokio::pin!(future)` pins a future on the stack (for use in `select!`)

---

### 9.2 Tokio Runtime Architecture: The Multi-Threaded Work-Stealing Scheduler

Tokio's runtime is a sophisticated system with multiple components working together:

**Architecture overview:**

```
┌─────────────────────────────────────────────────────────┐
│                    Tokio Runtime                          │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────┐   │
│  │         Worker Thread Pool (N threads)            │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐           │   │
│  │  │Worker 0 │ │Worker 1 │ │Worker 2 │ ...        │   │
│  │  │[local Q]│ │[local Q]│ │[local Q]│            │   │
│  │  └────┬────┘ └────┬────┘ └────┬────┘            │   │
│  │       │            │            │                 │   │
│  │       └────────────┼────────────┘                 │   │
│  │                    │ (work stealing)              │   │
│  │              ┌─────┴─────┐                        │   │
│  │              │ Global Q  │                        │   │
│  │              └───────────┘                        │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │       Blocking Thread Pool (up to 512)            │   │
│  │  (for spawn_blocking tasks)                       │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │              I/O Driver (epoll/kqueue/IOCP)       │   │
│  │  (monitors file descriptors, wakes tasks)         │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Timer Driver                         │   │
│  │  (manages sleep/timeout/interval futures)         │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Work-stealing scheduler:**

Each worker thread has a **local run queue** (LIFO for cache locality). When a worker's queue is empty, it **steals** tasks from other workers' queues (FIFO to steal oldest/coldest tasks). This balances load automatically without a central coordinator.

```rust
// Configure the runtime explicitly:
let runtime = tokio::runtime::Builder::new_multi_thread()
    .worker_threads(4)              // Number of worker threads
    .max_blocking_threads(128)      // Max blocking pool size
    .thread_name("my-worker")       // Thread naming
    .thread_stack_size(3 * 1024 * 1024)  // 3MB stack per thread
    .enable_all()                   // Enable I/O and timer drivers
    .build()
    .unwrap();

// Single-threaded runtime (for testing or !Send futures):
let rt = tokio::runtime::Builder::new_current_thread()
    .enable_all()
    .build()
    .unwrap();
```

**Task scheduling details:**

1. `tokio::spawn(future)` places the task on the **current worker's local queue**
2. If the local queue is full, tasks overflow to the **global queue**
3. Idle workers check: local queue → global queue → steal from others
4. `.await` points are **yield points** — the scheduler can switch tasks
5. Tasks are **not preempted** between yield points (cooperative scheduling)

**The "budget" system:**

Tokio implements a **cooperative budget** to prevent starvation. Each task gets a budget of ~128 operations. If a task does many `.await`s without yielding to the scheduler (e.g., a tight loop of channel receives), Tokio forces a yield after the budget is exhausted:

```rust
// This won't starve other tasks even though it loops:
async fn greedy_task(mut rx: mpsc::Receiver<i32>) {
    loop {
        // After ~128 recv() calls, Tokio forces a yield
        // to let other tasks run
        match rx.recv().await {
            Some(val) => process(val),
            None => break,
        }
    }
}
```

---

### 9.3 Send, Sync, and Auto-Trait Propagation

`Send` and `Sync` are **auto-traits** — the compiler automatically implements them for types whose fields are all `Send`/`Sync`. Understanding propagation rules is essential for async code.

**Auto-trait rules:**

```rust
// A struct is Send if ALL its fields are Send:
struct MyStruct {
    a: String,      // Send ✅
    b: Vec<u8>,     // Send ✅
    c: Arc<i32>,    // Send ✅
}
// → MyStruct is automatically Send ✅

struct NotSend {
    a: String,      // Send ✅
    b: Rc<i32>,     // Send ❌ (Rc uses non-atomic refcount)
}
// → NotSend is NOT Send ❌ (one non-Send field poisons the whole struct)
```

**The async gotcha — holding non-Send across .await:**

```rust
use std::rc::Rc;

async fn problematic() {
    let data = Rc::new(42);  // Rc is !Send
    
    some_async_op().await;   // ← Suspend point
    
    println!("{data}");      // data is held across .await
    // The generated Future struct contains `data: Rc<i32>`
    // → The Future is !Send → can't use with tokio::spawn()
}

// tokio::spawn requires Send:
// tokio::spawn(problematic());  // ❌ COMPILE ERROR: future is not Send

// Fix 1: Drop before .await
async fn fixed_drop() {
    {
        let data = Rc::new(42);
        println!("{data}");
    }  // data dropped here
    some_async_op().await;  // Future no longer holds Rc
}

// Fix 2: Use Arc instead
async fn fixed_arc() {
    let data = std::sync::Arc::new(42);  // Arc is Send
    some_async_op().await;
    println!("{data}");  // ✅ Future is Send
}
```

**Negative impls (opt-out):**

Some types explicitly opt OUT of Send/Sync:

```rust
// In std library (simplified):
impl<T> !Send for Rc<T> {}       // Rc is explicitly !Send
impl<T> !Sync for Cell<T> {}     // Cell is explicitly !Sync
impl<T> !Sync for RefCell<T> {}  // RefCell is explicitly !Sync

// Raw pointers are !Send and !Sync by default:
// *const T: !Send, !Sync
// *mut T: !Send, !Sync

// You can opt back in with unsafe:
struct MyWrapper(*mut u8);
unsafe impl Send for MyWrapper {}  // "I promise this is safe to send"
unsafe impl Sync for MyWrapper {}  // "I promise this is safe to share"
```

---

### 9.4 Structured Concurrency and Cancellation Safety

**Structured concurrency** means that spawned tasks have a clear parent-child relationship and are guaranteed to complete (or be cancelled) before the parent exits. Tokio provides tools for this:

**JoinSet — structured task group:**

```rust
use tokio::task::JoinSet;

async fn structured_concurrency() -> Vec<String> {
    let mut set = JoinSet::new();
    
    for i in 0..10 {
        set.spawn(async move {
            tokio::time::sleep(Duration::from_millis(i * 100)).await;
            format!("task {i} done")
        });
    }
    
    let mut results = Vec::new();
    while let Some(result) = set.join_next().await {
        results.push(result.unwrap());
    }
    // ALL tasks guaranteed complete here
    results
}

// If the JoinSet is dropped, all tasks are CANCELLED (aborted)
```

**Cancellation safety:**

When a future is dropped (cancelled), it stops executing at its current `.await` point. This can leave state inconsistent if the future was in the middle of a multi-step operation:

```rust
// ❌ NOT cancellation-safe:
async fn transfer(from: &mut Account, to: &mut Account, amount: u64) {
    from.balance -= amount;        // Step 1: debit
    save_to_db(from).await;        // ← If cancelled HERE...
    to.balance += amount;          // Step 2: credit (never runs!)
    save_to_db(to).await;
}
// If cancelled between the two saves, money disappears!

// ✅ Cancellation-safe version:
async fn transfer_safe(from: &mut Account, to: &mut Account, amount: u64) {
    // Compute the new state atomically
    let new_from = from.balance - amount;
    let new_to = to.balance + amount;
    
    // Apply atomically (single .await point)
    save_both_to_db(from.id, new_from, to.id, new_to).await;
    
    // Update local state only after persistence succeeds
    from.balance = new_from;
    to.balance = new_to;
}
```

**Rules for cancellation safety:**
1. Don't hold locks across `.await` points
2. Don't partially mutate state across `.await` points
3. Use transactions for multi-step operations
4. Document whether your async functions are cancellation-safe

---
