---
title: "08.10 — Operating Systems Essentials"
subject: "Python"
catalog: advanced
audience_tier: higher-education
chapter: "8.1"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 08.10 — Operating Systems Essentials

> *"An operating system is a collection of things that don't fit into a language. There shouldn't be one."* — Dan Ingalls

Your Python process doesn't run in a vacuum. It runs on an OS that manages memory, schedules CPU time, handles I/O, and enforces isolation. Understanding these mechanisms explains why `fork()` is dangerous with threads, why `mmap` is fast, and why your ML training saturates at 80% GPU utilization.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Explain process creation (`fork`/`exec`), lifecycle, and inter-process communication.
2. Understand virtual memory, page tables, and why `mmap` matters for large files.
3. Explain how the scheduler allocates CPU time and what "context switch" costs.
4. Navigate the filesystem abstraction (inodes, file descriptors, VFS).
5. Use Python's `os`, `signal`, and `resource` modules for OS interaction.
6. Diagnose performance issues caused by OS-level bottlenecks.

---

## 🖼️ Visual Anchor — OS Layer Architecture

![python__1.10-fig1](python__1.10-fig1.svg)

---

## 📚 1. Definitions / Concepts

### Definition 08.10.1 — Process

A **process** is an instance of a running program with its own:
- Virtual address space (code, heap, stack)
- File descriptor table
- PID (process ID)
- Scheduling state (running, ready, blocked, zombie)

### Definition 08.10.2 — Virtual Memory

Each process sees a contiguous address space (0 to 2⁶⁴). The OS + MMU translates virtual addresses to physical RAM pages (typically 4KB). Benefits:
- Isolation: processes can't access each other's memory
- Overcommit: allocate more virtual memory than physical RAM
- Memory-mapped files: treat files as arrays in memory

### Definition 08.10.3 — System Call

A **syscall** is the interface between user space and kernel space. When Python calls `open()`, it ultimately invokes the `open` syscall, which traps into the kernel to perform the actual file operation.

### Definition 08.10.4 — File Descriptor

An integer handle to an open resource (file, socket, pipe). Every process starts with:
- fd 0: stdin
- fd 1: stdout
- fd 2: stderr

---

## 📐 2. Mental Models / Principles

### Principle 1.10.1 — Everything Is a File (Unix)

In Unix, files, directories, devices, sockets, and pipes are all accessed through the same `open/read/write/close` interface. This uniformity is why pipes and redirection work so naturally.

### Principle 1.10.2 — Context Switches Are Expensive

When the OS switches between processes, it must:
1. Save all CPU registers
2. Flush TLB (translation lookaside buffer)
3. Restore the new process's state

Cost: ~1-10 microseconds. This is why thousands of threads are expensive but thousands of async tasks (single thread) are cheap.

### Principle 1.10.3 — Memory Hierarchy Awareness

| Level | Size | Latency | Python Relevance |
|-------|------|---------|-----------------|
| L1 cache | 64KB | ~1ns | Hot loop variables |
| L2 cache | 256KB | ~4ns | Small data structures |
| L3 cache | 8-32MB | ~12ns | Working set |
| RAM | 16-128GB | ~100ns | Most Python objects |
| SSD | TB | ~100μs | File I/O |
| Network | ∞ | ~1ms+ | API calls |

---

## 🔑 3. Mechanics

### 3.1 — Process Management from Python

```python
import os
import signal
import subprocess

# Current process info
print(f"PID: {os.getpid()}")
print(f"Parent PID: {os.getppid()}")
print(f"User: {os.getuid()}" if hasattr(os, 'getuid') else "Windows")

# Fork (Unix only) — creates a copy of the current process
if hasattr(os, 'fork'):
    pid = os.fork()
    if pid == 0:
        print("I am the child")
        os._exit(0)
    else:
        os.waitpid(pid, 0)
        print(f"Child {pid} finished")

# Signal handling
def handle_sigterm(signum, frame):
    print("Graceful shutdown...")
    cleanup()
    raise SystemExit(0)

signal.signal(signal.SIGTERM, handle_sigterm)
```

### 3.2 — Memory-Mapped Files

```python
import mmap
from pathlib import Path

# Read a large file without loading it all into RAM
path = Path("large_dataset.bin")
with open(path, "rb") as f:
    with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
        # Access like a bytearray — OS pages in data on demand
        header = mm[:1024]
        # Seek to specific offset without reading everything
        chunk = mm[1_000_000:1_001_000]
```

### 3.3 — Resource Limits

```python
import resource  # Unix only

# Check memory usage
usage = resource.getrusage(resource.RUSAGE_SELF)
print(f"Max RSS: {usage.ru_maxrss / 1024:.1f} MB")

# Set limits (prevent runaway processes)
# Limit to 4GB RAM
resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))
```

---

## ✍️ 4. Derivations & Worked Examples

### Example 08.10.1 — Diagnosing a Memory Leak

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```python
import tracemalloc
import gc

tracemalloc.start()

# ... run your code ...

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("Top 10 memory allocations:")
for stat in top_stats[:10]:
    print(stat)

# Force garbage collection and check for uncollectable cycles
gc.collect()
print(f"Uncollectable: {gc.garbage}")
```

</details>

---

## 💻 5. Code Patterns & Idioms

### Pattern 1.10.1 — Graceful Shutdown

```python
import signal
import asyncio

async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()

    def shutdown(sig):
        stop.set_result(sig)

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, shutdown, sig)

    await stop  # Wait for signal
    # Cleanup...
```

---

## ⚠️ 6. Gotchas & Anti-Patterns

### Gotcha 1.10.1 — fork() + threads = Deadlock

Never `fork()` in a multithreaded process. The child inherits only the calling thread, but mutexes held by other threads remain locked forever. Use `multiprocessing` with `spawn` start method on all platforms.

---

## 🧮 7. Hands-On Lab

```bash
python _practice/scripts/1.10_os_essentials.py --out _practice/1.10_lab_report.md
```

Reports your system's CPU count, memory, filesystem type, and process limits.

---

## 🔗 8. Cross-links & Further Reading

- Previous: [08.9 - Docker & Containers](08.9---Docker-&-Containers)
- Next: [08.11 - Computer Networks Essentials](08.11---Computer-Networks-Essentials)
- Concurrency implications: [08.4 - Concurrency - asyncio, threading, multiprocessing & the GIL](08.4---Concurrency---asyncio,-threading,-multiprocessing-&-the-GIL)
- [OSTEP: Operating Systems: Three Easy Pieces (free)](https://pages.cs.wisc.edu/~remzi/OSTEP/)
- [The Linux Programming Interface (Kerrisk)](https://man7.org/tlpi/)



---

## 🧠 9. Extended Worked Examples & Deep Dives

### Example 9.1 — Process Tree Walkthrough: From Boot to Your Python Script

**Problem:** Trace the complete process hierarchy from system boot to your running Python script. Explain PID 1, process creation via `fork()`/`exec()`, and demonstrate how to inspect the process tree programmatically.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: The Boot Sequence (Linux)

```bash
# 1. BIOS/UEFI → bootloader (GRUB) → kernel
# 2. Kernel initializes hardware, mounts root filesystem
# 3. Kernel starts PID 1: the init system (systemd on modern Linux)
# 4. systemd reads unit files, starts services in dependency order
# 5. systemd starts login managers, SSH daemon, etc.
# 6. User logs in → shell process spawned
# 7. User runs command → shell forks + execs the command

# The process tree:
# PID 1: systemd
# ├── PID 500: sshd (SSH daemon)
# │   └── PID 1200: sshd (per-connection)
# │       └── PID 1201: bash (user shell)
# │           └── PID 1500: python train.py (your script)
# │               ├── PID 1501: python (multiprocessing worker 1)
# │               └── PID 1502: python (multiprocessing worker 2)
# ├── PID 600: postgres
# ├── PID 700: nginx
# └── PID 800: docker daemon
```

#### Step 2: fork() and exec() — How Processes Are Created

```python
import os
import sys

def demonstrate_fork():
    """
    fork() creates an EXACT COPY of the current process.
    The child gets PID 0 from fork(), parent gets child's PID.
    After fork, both processes execute the same code — you use
    the return value to distinguish parent from child.
    """
    print(f"Before fork: PID={os.getpid()}")

    pid = os.fork()  # Returns TWICE: once in parent, once in child

    if pid == 0:
        # CHILD process (fork returned 0)
        print(f"  Child: PID={os.getpid()}, Parent PID={os.getppid()}")
        # Child typically calls exec() to replace itself with a new program
        os.execvp("echo", ["echo", "Hello from child!"])
        # exec() NEVER returns (replaces entire process image)
    else:
        # PARENT process (fork returned child's PID)
        print(f"  Parent: PID={os.getpid()}, Child PID={pid}")
        # Wait for child to finish (prevent zombie)
        _, status = os.waitpid(pid, 0)
        print(f"  Child exited with status: {os.WEXITSTATUS(status)}")

# demonstrate_fork()  # Only works on Unix (not Windows)
```

#### Step 3: Inspecting the Process Tree from Python

```python
import psutil  # pip install psutil

def print_process_tree(pid: int = 1, indent: int = 0):
    """Recursively print the process tree starting from a PID."""
    try:
        proc = psutil.Process(pid)
        name = proc.name()
        cmdline = " ".join(proc.cmdline()[:3])  # First 3 args
        print(f"{'  ' * indent}PID {pid}: {name} [{cmdline}]")

        for child in proc.children():
            print_process_tree(child.pid, indent + 1)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass


def inspect_current_process():
    """Show detailed info about the current Python process."""
    proc = psutil.Process()

    print(f"PID: {proc.pid}")
    print(f"Parent PID: {proc.ppid()}")
    print(f"Name: {proc.name()}")
    print(f"Status: {proc.status()}")
    print(f"CPU%: {proc.cpu_percent(interval=0.1)}")
    print(f"Memory: {proc.memory_info().rss / 1024 / 1024:.1f} MB")
    print(f"Threads: {proc.num_threads()}")
    print(f"Open files: {len(proc.open_files())}")
    print(f"Connections: {len(proc.net_connections())}")
    print(f"Created: {proc.create_time()}")

    # Walk up to PID 1
    print("\nAncestry:")
    current = proc
    while current.pid != 0:
        print(f"  PID {current.pid}: {current.name()}")
        try:
            current = current.parent()
            if current is None:
                break
        except psutil.NoSuchProcess:
            break

inspect_current_process()
```

#### Step 4: Zombie and Orphan Processes

```python
import os
import time

def create_zombie():
    """
    A zombie is a child that has exited but whose parent hasn't
    called wait() yet. The kernel keeps the exit status in the
    process table until the parent reads it.
    """
    pid = os.fork()
    if pid == 0:
        # Child exits immediately
        sys.exit(0)
    else:
        # Parent sleeps without calling wait()
        # During this time, child is a ZOMBIE (state: Z)
        time.sleep(60)
        # To see: ps aux | grep Z
        os.waitpid(pid, 0)  # Reap the zombie


def create_orphan():
    """
    An orphan is a child whose parent has exited.
    PID 1 (systemd/init) adopts orphans and reaps them.
    """
    pid = os.fork()
    if pid == 0:
        # Child: parent will exit, we become orphan
        time.sleep(5)
        print(f"Orphan: my new parent is PID {os.getppid()}")
        # Will print PID 1 (adopted by init/systemd)
    else:
        # Parent exits immediately, abandoning child
        sys.exit(0)
```

**Final Answer:**

```python
# Process lifecycle:
# 1. fork() — create copy of current process
# 2. exec() — replace process image with new program
# 3. Running — process executes
# 4. Exit — process calls exit(), becomes zombie until parent waits
# 5. Reap — parent calls wait(), kernel removes process table entry
#
# Key commands:
# ps aux                — list all processes
# pstree -p            — show process tree with PIDs
# top / htop           — interactive process monitor
# kill -SIGTERM <pid>  — graceful shutdown request
# kill -SIGKILL <pid>  — force kill (cannot be caught)
```

</details>

### Example 9.2 — Signal Handling in Python: Graceful Shutdown Patterns

**Problem:** Your Python service needs to handle SIGTERM (from `docker stop` or Kubernetes pod termination) gracefully: finish current work, flush buffers, close connections, then exit. Demonstrate proper signal handling for both synchronous and asyncio applications.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Understanding Signals

```python
import signal
import sys
import time

# Common signals:
# SIGINT (2)   — Ctrl+C in terminal. Default: terminate.
# SIGTERM (15) — Polite shutdown request (docker stop, kill <pid>). Default: terminate.
# SIGKILL (9)  — Force kill. CANNOT be caught or ignored. Kernel terminates immediately.
# SIGHUP (1)   — Terminal hangup. Often used to reload config.
# SIGUSR1 (10) — User-defined. Often used for log rotation or debug dumps.

# Key rule: SIGKILL cannot be handled. Your graceful shutdown must complete
# before the SIGKILL timeout (docker stop gives 10s by default).
```

#### Step 2: Synchronous Signal Handling

```python
import signal
import sys
import time
import threading
from typing import Any

class GracefulShutdown:
    """
    Signal handler for graceful shutdown of synchronous services.
    """

    def __init__(self, timeout: float = 10.0):
        self.shutdown_requested = False
        self.timeout = timeout
        self._original_handlers: dict[int, Any] = {}

    def __enter__(self):
        """Register signal handlers."""
        for sig in (signal.SIGINT, signal.SIGTERM):
            self._original_handlers[sig] = signal.getsignal(sig)
            signal.signal(sig, self._handle_signal)
        return self

    def __exit__(self, *args):
        """Restore original handlers."""
        for sig, handler in self._original_handlers.items():
            signal.signal(sig, handler)

    def _handle_signal(self, signum: int, frame):
        """Called when signal received."""
        sig_name = signal.Signals(signum).name
        print(f"\n⚠️ Received {sig_name} — initiating graceful shutdown...")
        self.shutdown_requested = True

        # If second signal received, force exit
        signal.signal(signum, lambda s, f: sys.exit(128 + signum))

    @property
    def should_continue(self) -> bool:
        """Check in your main loop."""
        return not self.shutdown_requested


# Usage:
def worker_loop():
    """Example: process items from a queue."""
    with GracefulShutdown() as shutdown:
        while shutdown.should_continue:
            # Process one item (keep iterations short for responsiveness)
            item = get_next_item(timeout=08.0)
            if item:
                process_item(item)  # Should complete within a few seconds

        # Graceful cleanup
        print("Flushing buffers...")
        flush_all_buffers()
        print("Closing connections...")
        close_all_connections()
        print("✅ Clean shutdown complete")
```

#### Step 3: Asyncio Signal Handling

```python
import asyncio
import signal
import functools


async def async_worker():
    """Async service with proper signal handling."""

    shutdown_event = asyncio.Event()

    def handle_signal(sig: signal.Signals):
        print(f"\n⚠️ Received {sig.name} — shutting down...")
        shutdown_event.set()

    # Register signal handlers with the event loop
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            sig,
            functools.partial(handle_signal, sig)
        )

    # Main service loop
    print("Service running... (Ctrl+C to stop)")
    try:
        while not shutdown_event.is_set():
            # Do work with a timeout so we check shutdown_event periodically
            try:
                await asyncio.wait_for(do_async_work(), timeout=08.0)
            except asyncio.TimeoutError:
                continue  # Check shutdown_event again
    finally:
        # Graceful cleanup (async-safe)
        print("Cleaning up...")
        await close_async_connections()
        print("✅ Async shutdown complete")


async def do_async_work():
    """Placeholder for actual async work."""
    await asyncio.sleep(0.5)


async def close_async_connections():
    """Placeholder for cleanup."""
    await asyncio.sleep(0.1)


# asyncio.run(async_worker())
```

#### Step 4: Docker + Kubernetes Integration

```python
# Docker sends SIGTERM on `docker stop`, then SIGKILL after timeout (default 10s).
# Kubernetes sends SIGTERM on pod termination, then SIGKILL after terminationGracePeriodSeconds (default 30s).

# CRITICAL: Your process must be PID 1 in the container to receive signals!

# WRONG (shell form — bash is PID 1, Python doesn't get signals):
# CMD python app.py

# CORRECT (exec form — Python is PID 1, receives signals directly):
# CMD ["python", "-m", "app"]

# Or use exec in shell form:
# CMD exec python -m app
```

#### Step 5: SIGHUP for Config Reload

```python
import signal
import json
from pathlib import Path

_config: dict = {}

def load_config():
    """Load configuration from file."""
    global _config
    config_path = Path("/etc/myapp/config.json")
    _config = json.loads(config_path.read_text())
    print(f"Config loaded: {len(_config)} keys")

def handle_sighup(signum, frame):
    """Reload config on SIGHUP (sent by: kill -HUP <pid>)."""
    print("Received SIGHUP — reloading configuration...")
    load_config()

# Register
signal.signal(signal.SIGHUP, handle_sighup)
load_config()  # Initial load

# Now: kill -HUP $(pidof python) triggers config reload without restart
```

**Final Answer:**

```python
# Signal handling checklist:
# 1. Handle SIGTERM for graceful shutdown (docker stop, k8s termination)
# 2. Handle SIGINT for Ctrl+C (same logic as SIGTERM usually)
# 3. Use exec form CMD in Dockerfile (process must be PID 1)
# 4. Keep shutdown fast (< 10s for Docker, < 30s for Kubernetes)
# 5. Second signal = force exit (user is impatient)
# 6. SIGHUP for config reload (optional, common pattern)
# 7. NEVER try to catch SIGKILL — it's impossible
```

</details>

### Example 9.3 — fork vs spawn: Python Multiprocessing Start Methods

**Problem:** Python's `multiprocessing` module has three start methods: `fork`, `spawn`, and `forkserver`. Explain the differences, demonstrate the bugs that `fork` causes with threads and CUDA, and show how to choose correctly.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: The Three Start Methods

```python
import multiprocessing as mp

# Check/set the start method (must be done ONCE, before creating processes):
# mp.set_start_method("spawn")  # or "fork" or "forkserver"
print(mp.get_start_method())  # Default: "fork" on Linux, "spawn" on Windows/macOS

# FORK: Copy parent process (fast, shares memory initially via COW)
# SPAWN: Start fresh Python interpreter, import module, run target function
# FORKSERVER: Fork from a clean server process (compromise between fork and spawn)
```

#### Step 2: Why fork() Is Dangerous with Threads

```python
import threading
import multiprocessing as mp
import time

# The DEADLY scenario: fork() with active threads
lock = threading.Lock()

def background_thread():
    """Thread that holds a lock periodically."""
    while True:
        with lock:
            time.sleep(0.01)  # Holds lock briefly

def child_work():
    """This function runs in the forked child process."""
    # DEADLOCK! The lock was held by the background thread at fork time.
    # fork() copies the lock in its LOCKED state, but the thread that
    # would unlock it doesn't exist in the child.
    with lock:  # Hangs forever
        print("Child acquired lock")

# Start background thread
t = threading.Thread(target=background_thread, daemon=True)
t.start()

# Fork a child process — DANGEROUS
# If fork happens while background_thread holds the lock:
# → Child inherits locked mutex
# → No thread exists in child to unlock it
# → child_work() deadlocks

# p = mp.Process(target=child_work)
# p.start()  # May deadlock!
```

#### Step 3: Why fork() Is Dangerous with CUDA

```python
# CUDA maintains internal state (GPU context, memory allocations).
# fork() copies the process but NOT the GPU context.
# Result: child process has stale CUDA state → crash or silent corruption.

import torch

def train_worker(gpu_id):
    """Worker that uses GPU."""
    # If parent already initialized CUDA before fork:
    # RuntimeError: Cannot re-initialize CUDA in forked subprocess.
    device = torch.device(f"cuda:{gpu_id}")
    tensor = torch.randn(1000, 1000, device=device)
    return tensor.sum().item()

# WRONG: Initialize CUDA in parent, then fork
# model = torch.nn.Linear(10, 10).cuda()  # Initializes CUDA context
# mp.set_start_method("fork")
# pool = mp.Pool(4)  # Children inherit broken CUDA state!

# CORRECT: Use spawn (fresh CUDA initialization per child)
# mp.set_start_method("spawn")
# pool = mp.Pool(4)  # Each child initializes its own CUDA context
```

#### Step 4: Comparison Table

```python
# | Property           | fork              | spawn             | forkserver        |
# |--------------------|-------------------|-------------------|-------------------|
# | Speed              | Fast (~1ms)       | Slow (~100ms)     | Medium (~10ms)    |
# | Memory             | COW (shared)      | Fresh copy        | Fresh copy        |
# | Thread-safe        | NO                | YES               | YES               |
# | CUDA-safe          | NO                | YES               | YES               |
# | Inherits state     | Everything        | Nothing (re-import)| Nothing          |
# | Pickling required  | No                | Yes (args+target) | Yes              |
# | Default on Linux   | YES               | No                | No               |
# | Default on macOS   | No                | YES (since 3.8)   | No               |
# | Default on Windows | N/A (no fork)     | YES               | N/A              |
```

#### Step 5: Best Practice

```python
import multiprocessing as mp

# At the TOP of your main script (before any imports that use threads/CUDA):
if __name__ == "__main__":
    mp.set_start_method("spawn")  # Safe default for all platforms

    # Now safe to use multiprocessing with threads, CUDA, etc.
    from my_app import main
    main()

# Alternative: use context manager for per-pool control
def safe_parallel():
    ctx = mp.get_context("spawn")  # Doesn't affect global setting
    with ctx.Pool(4) as pool:
        results = pool.map(cpu_work, data)
    return results
```

**Final Answer:**

```python
# Start method decision:
# - Always use "spawn" if you use: threads, CUDA/GPU, or any C extension
#   that maintains internal state (OpenSSL, database drivers, etc.)
# - Use "fork" ONLY for pure-Python CPU work with no threads
#   (and only on Linux where it's the default)
# - Use "forkserver" as a compromise: safe like spawn, faster for
#   repeated process creation (the server process is forked once, cleanly)
#
# Rule of thumb: set_start_method("spawn") and forget about it.
# The 100ms startup cost is negligible for real workloads.
```

</details>

---

## 📘 10. Appendix: Extended Derivations & Special Cases

### 10.1 io_uring vs epoll vs kqueue — Modern I/O Multiplexing

I/O multiplexing allows a single thread to monitor thousands of file descriptors (sockets, files, pipes) for readiness. This is the foundation of all high-performance network servers (nginx, Node.js, asyncio).

**The Evolution:**

1. **select() (1983):** Original Unix. Limited to 1024 file descriptors. O(n) scanning.
2. **poll() (1997):** Removes FD limit. Still O(n) scanning per call.
3. **epoll (Linux 2002):** O(1) per event. Kernel maintains interest list.
4. **kqueue (BSD/macOS 2000):** Similar to epoll. Used on macOS, FreeBSD.
5. **io_uring (Linux 2019):** Asynchronous I/O with shared ring buffers. Zero syscall overhead for submissions.

**epoll (Linux — used by asyncio on Linux):**

```python
# Conceptual epoll workflow (asyncio uses this internally):
# 1. Create epoll instance: epoll_fd = epoll_create1(0)
# 2. Register interest: epoll_ctl(epoll_fd, EPOLL_CTL_ADD, socket_fd, events)
# 3. Wait for events: events = epoll_wait(epoll_fd, max_events, timeout)
# 4. Process ready FDs from returned events
#
# Key advantage: epoll_wait returns ONLY ready FDs (not all registered FDs)
# For 10,000 connections with 5 active: returns 5 events, not 10,000

import selectors  # Python's cross-platform abstraction over epoll/kqueue/select

sel = selectors.DefaultSelector()  # Uses epoll on Linux, kqueue on macOS

def accept_connection(sock):
    conn, addr = sock.accept()
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, data=handle_client)

def handle_client(conn):
    data = conn.recv(1024)
    if data:
        conn.sendall(data)  # Echo
    else:
        sel.unregister(conn)
        conn.close()

# Event loop (simplified asyncio):
# while True:
#     events = sel.select(timeout=08.0)
#     for key, mask in events:
#         callback = key.data
#         callback(key.fileobj)
```

**io_uring (Linux 5.1+ — the future):**

io_uring eliminates syscall overhead entirely by using shared memory ring buffers between userspace and kernel:

```python
# Traditional I/O: each read/write = 1 syscall (context switch to kernel)
# io_uring: batch submissions via shared memory, no syscalls needed

# The two rings:
# Submission Queue (SQ): userspace writes I/O requests here
# Completion Queue (CQ): kernel writes completed results here
#
# Workflow:
# 1. Write SQE (submission queue entry) to SQ ring buffer
# 2. Optionally: submit multiple SQEs before notifying kernel
# 3. Kernel processes SQEs asynchronously
# 4. Kernel writes CQEs (completion queue entries) to CQ ring buffer
# 5. Userspace reads CQEs — no syscall needed!

# Python access via liburing bindings or uvloop (uses io_uring when available)
# uvloop (used by many async frameworks) automatically uses io_uring on Linux 5.1+
```

**Performance Comparison (10,000 concurrent connections, echo server):**

| Mechanism | Requests/sec | Syscalls/req | Latency (p99) |
|-----------|-------------|--------------|---------------|
| select | 15,000 | 2 | 12ms |
| epoll | 180,000 | 1 | 0.8ms |
| io_uring | 350,000 | 0.1 (batched) | 0.3ms |

### 10.2 Linux Capabilities — Fine-Grained Privilege Control

Traditional Unix has a binary privilege model: root (UID 0) can do everything, non-root can do almost nothing. Linux capabilities split root's powers into ~40 individual capabilities that can be granted independently.

**Why This Matters for Containers:**

Docker containers run as root by default, but with a reduced capability set. Understanding capabilities explains why some operations fail in containers and how to grant minimal privileges.

**Common Capabilities:**

```bash
# CAP_NET_BIND_SERVICE — Bind to ports < 1024 (needed for port 80/443)
# CAP_NET_RAW          — Use raw sockets (needed for ping, tcpdump)
# CAP_SYS_PTRACE       — Trace processes (needed for strace, debuggers)
# CAP_SYS_ADMIN        — Catch-all admin (mount, namespace creation, etc.)
# CAP_DAC_OVERRIDE     — Bypass file permission checks
# CAP_CHOWN            — Change file ownership
# CAP_SETUID/SETGID    — Change process UID/GID

# Docker default capabilities (subset of root):
# CAP_CHOWN, CAP_DAC_OVERRIDE, CAP_FSETID, CAP_FOWNER,
# CAP_MKNOD, CAP_NET_RAW, CAP_SETGID, CAP_SETUID,
# CAP_SETFCAP, CAP_SETPCAP, CAP_NET_BIND_SERVICE,
# CAP_SYS_CHROOT, CAP_KILL, CAP_AUDIT_WRITE
```

**Practical Example — Running a Web Server on Port 80 Without Root:**

```bash
# Option 1: Grant only the needed capability
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE my-app
# Container can bind port 80 but has NO other root privileges

# Option 2: Use a non-root user with capability on the binary
# In Dockerfile:
# RUN setcap 'cap_net_bind_service=+ep' /usr/local/bin/python3
# USER appuser
# Now Python can bind port 80 even as non-root

# Option 3: Just use port > 1024 and let the reverse proxy handle 80
# (Simplest and most common approach)
```

**Python Capability Inspection:**

```python
import os
import struct
from pathlib import Path

def get_process_capabilities(pid: int = None) -> dict:
    """Read capabilities of a process from /proc."""
    pid = pid or os.getpid()
    status = Path(f"/proc/{pid}/status").read_text()
    
    caps = {}
    for line in status.splitlines():
        if line.startswith("Cap"):
            key, value = line.split(":\t")
            caps[key] = int(value, 16)
    
    return caps

# In a Docker container:
# caps = get_process_capabilities()
# print(f"Effective: {caps.get('CapEff', 0):016x}")
# print(f"Permitted: {caps.get('CapPrm', 0):016x}")
```

---



### 10.3 cgroups (Control Groups) — How Docker Limits Resources

cgroups are a Linux kernel feature that limits, accounts for, and isolates resource usage (CPU, memory, I/O, network) of process groups. Docker uses cgroups to enforce `--memory`, `--cpus`, and other resource limits.

**cgroups v2 Hierarchy:**

```bash
# cgroups organize processes into a tree:
# /sys/fs/cgroup/
# ├── system.slice/          (system services)
# │   ├── docker.service/    (Docker daemon)
# │   └── sshd.service/
# ├── user.slice/            (user sessions)
# └── docker/                (containers)
#     ├── container_abc123/  (each container gets its own cgroup)
#     │   ├── memory.max     (memory limit)
#     │   ├── cpu.max        (CPU limit)
#     │   └── cgroup.procs   (PIDs in this cgroup)
#     └── container_def456/

# Docker translates flags to cgroup settings:
# --memory=512m  → memory.max = 536870912
# --cpus=08.5     → cpu.max = "150000 100000" (150ms per 100ms period)
# --pids-limit=100 → pids.max = 100
```

**Python Interaction with cgroups:**

```python
from pathlib import Path

def get_container_memory_limit() -> int:
    """Detect memory limit when running inside a container."""
    # cgroups v2
    cgroup_v2 = Path("/sys/fs/cgroup/memory.max")
    if cgroup_v2.exists():
        value = cgroup_v2.read_text().strip()
        if value == "max":
            return -1  # No limit
        return int(value)

    # cgroups v1 (older systems)
    cgroup_v1 = Path("/sys/fs/cgroup/memory/memory.limit_in_bytes")
    if cgroup_v1.exists():
        return int(cgroup_v1.read_text().strip())

    return -1  # Not in a container or no limit


def get_available_cpus() -> float:
    """Detect CPU limit in container (respects --cpus flag)."""
    cpu_max = Path("/sys/fs/cgroup/cpu.max")
    if cpu_max.exists():
        parts = cpu_max.read_text().strip().split()
        if parts[0] == "max":
            import os
            return float(os.cpu_count() or 1)
        quota = int(parts[0])
        period = int(parts[1])
        return quota / period  # e.g., 150000/100000 = 08.5 CPUs

    import os
    return float(os.cpu_count() or 1)

# This matters for: setting worker counts, thread pool sizes, batch sizes
# multiprocessing.cpu_count() returns HOST CPUs, not container limit!
# Use this function instead for container-aware resource allocation.
```

---
