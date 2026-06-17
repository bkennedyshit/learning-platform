---
title: "15.8 — Virtual Machines, Bytecode & JIT"
subject: "Compilers & Language Design"
catalog: advanced
audience_tier: higher-education
chapter: "15.8"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 15.8 — Virtual Machines, Bytecode & JIT

> *"A virtual machine is just a computer that exists in software. All the same trade-offs apply — and a few new ones."*

**Virtual machines (VMs)** are software interpreters that execute a portable **bytecode** format instead of native machine code. The bytecode is produced by a compiler and the VM executes it instruction by instruction (or compiles it to native code on the fly — JIT). This chapter explains:

- Why Python, Java, JavaScript, and Lua chose VMs over direct compilation
- How the CPython bytecode VM works internally
- How JIT compilation works (the V8 tier architecture)
- The four main garbage collection strategies
- Why WebAssembly is the future of portable, safe, high-performance computing

---

## 🎯 Learning Objectives

1. Explain the trade-offs between **ahead-of-time (AOT) compilation**, **interpretation**, and **JIT compilation**.
2. Implement a minimal **stack-based bytecode VM** in Python.
3. Use `dis.dis()` to inspect **CPython bytecode** for any function.
4. Understand CPython's **specializing adaptive interpreter** (Python 3.11+).
5. Explain V8's JIT tier architecture: Ignition → Sparkplug → Maglev → TurboFan.
6. Compare **mark-sweep**, **generational**, **reference counting**, and **RAII** garbage collection.
7. Explain what makes **WebAssembly** safe, fast, and portable.

---

## 🖼️ Visual Anchor

![comp__29.8-fig1](comp__29.8-fig1.svg)

---

## 📚 1. Interpreter vs AOT vs JIT

| Strategy | How | Startup | Peak perf | Portability |
|---|---|---|---|---|
| **Interpreted** | Execute AST or bytecode directly | Instant | Low | High (one binary) |
| **AOT Compilation** | Compile to native code before run | Slow (compile step) | Highest | Low (per-arch binary) |
| **JIT Compilation** | Compile hot paths to native at runtime | Fast | Near-native | High (one bytecode binary) |

### Why Python Chose Interpretation

CPython's design priorities: developer experience, embedding simplicity, and reference implementation clarity. The cost of interpretation (roughly 100× slower than C for tight numeric loops) is acceptable for most scripting workloads. For performance-critical code, extension modules (NumPy, etc.) call native C/Fortran directly.

### Why Java / JVM Chose JIT

Java needed portability ("write once, run anywhere") but also acceptable performance. The JVM JIT (HotSpot) monitors runtime behavior (which methods are hot, which types are actually used) and compiles with profile data — something AOT can't do. Java server code often reaches 80–90% of equivalent C++ performance after warmup.

---

## 📚 2. Bytecode Design

### Stack-Based vs Register-Based VMs

**Stack-based** (CPython, JVM, WebAssembly):
- Instructions implicitly reference the top of the stack
- Compact encoding (no register field needed)
- Simple interpreter: push/pop operations
- Example: `LOAD_CONST 3; LOAD_CONST 4; BINARY_OP +` → result 7 on stack

**Register-based** (Lua 5, Dalvik/ART, .NET CLR, Cranelift):
- Instructions explicitly name source and destination registers
- Fewer instructions than stack-based (per high-level operation)
- Each instruction is wider (needs register fields)
- Example: `ADD r0, r1, r2` → r0 = r1 + r2

Lua switched from stack-based to register-based in Lua 5 and measured a ~30% performance improvement. Android switched from Dalvik (register-based) to ART (also register-based but with better AOT).

---

## 📚 3. A Minimal Stack VM in Python

```python
from enum import IntEnum, auto
from dataclasses import dataclass

class Op(IntEnum):
    LOAD_CONST = auto()   # push constant
    LOAD_NAME  = auto()   # push variable
    STORE_NAME = auto()   # pop → store in variable
    BINARY_ADD = auto()   # pop two, push sum
    BINARY_MUL = auto()   # pop two, push product
    PRINT      = auto()   # pop and print
    HALT       = auto()   # stop

@dataclass
class Instruction:
    op: Op
    arg: object = None

class StackVM:
    def __init__(self):
        self.stack: list = []
        self.env:   dict = {}

    def run(self, code: list[Instruction]):
        ip = 0  # instruction pointer
        while ip < len(code):
            instr = code[ip]
            match instr.op:
                case Op.LOAD_CONST:
                    self.stack.append(instr.arg)
                case Op.LOAD_NAME:
                    self.stack.append(self.env[instr.arg])
                case Op.STORE_NAME:
                    self.env[instr.arg] = self.stack.pop()
                case Op.BINARY_ADD:
                    b = self.stack.pop(); a = self.stack.pop()
                    self.stack.append(a + b)
                case Op.BINARY_MUL:
                    b = self.stack.pop(); a = self.stack.pop()
                    self.stack.append(a * b)
                case Op.PRINT:
                    print(self.stack.pop())
                case Op.HALT:
                    return
            ip += 1

# Program: x = 3; print(x + 4 * 2)
program = [
    Instruction(Op.LOAD_CONST, 3),
    Instruction(Op.STORE_NAME, 'x'),
    Instruction(Op.LOAD_NAME,  'x'),
    Instruction(Op.LOAD_CONST, 4),
    Instruction(Op.LOAD_CONST, 2),
    Instruction(Op.BINARY_MUL),
    Instruction(Op.BINARY_ADD),
    Instruction(Op.PRINT),
    Instruction(Op.HALT),
]
vm = StackVM()
vm.run(program)  # prints: 11
```

This is **essentially CPython's eval loop** — a giant `switch` over opcodes. The performance bottleneck is exactly this dispatch loop.

---

## 📚 4. CPython Bytecode in Depth

### Inspecting Bytecode with `dis`

```python
import dis

def example(x, y):
    if x > y:
        return x
    return y + 1

dis.dis(example)
```

Output (Python 3.12):
```
  2           0 RESUME                   0

  3           2 LOAD_FAST                0 (x)
              4 LOAD_FAST                1 (y)
              6 COMPARE_OP               4 (>)
             10 POP_JUMP_IF_FALSE       18 (to 46)

  4          12 LOAD_FAST                0 (x)
             14 RETURN_VALUE

  5     >>   16 LOAD_FAST                1 (y)
             18 LOAD_CONST               1 (1)
             20 BINARY_OP               0 (+)
             24 RETURN_VALUE
```

Key CPython instructions:
| Opcode | Meaning |
|---|---|
| `LOAD_FAST n` | Push local variable n onto stack |
| `STORE_FAST n` | Pop stack → store in local n |
| `LOAD_CONST n` | Push constant from co_consts[n] |
| `BINARY_OP n` | Pop two, apply operator n, push result |
| `COMPARE_OP n` | Pop two, compare with operator n, push bool |
| `POP_JUMP_IF_FALSE` | Pop bool; if False, jump to target |
| `CALL n` | Call function with n arguments |
| `RETURN_VALUE` | Return top of stack |

### The Specializing Adaptive Interpreter (Python 3.11+)

CPython 3.11 introduced a **micro-JIT** technique: the interpreter rewrites hot bytecode instructions in-place to faster "specialized" variants:

- `LOAD_FAST` → `LOAD_FAST__LOAD_FAST` (combine two loads into one operation for common patterns)
- `BINARY_OP` → `BINARY_OP_ADD_INT` (skip type dispatch when type is known to be `int`)
- `CALL` → `CALL_PY_EXACT_ARGS` (skip argument checking for known Python functions)

This is a form of **inline caching**: the type feedback from previous executions is used to specialize future ones. If the specialization assumption is violated (the type changes), the instruction deoptimizes back to the generic form.

---

## 📚 5. JIT Compilation — V8's Tier Architecture

**Google V8** (used in Chrome and Node.js) has evolved to a 4-tier JIT architecture:

### Tier 0: Ignition (Bytecode Interpreter)

V8 first compiles JavaScript to a register-based bytecode and executes it with the **Ignition** interpreter. Startup is fast, memory usage is low, and the interpreter **collects type feedback** (what types does `+` actually see?).

### Tier 1: Sparkplug (Baseline JIT)

When a function is called enough times, **Sparkplug** compiles the bytecode to native code **very quickly** — essentially a one-to-one translation with no optimization. This eliminates interpreter overhead without the compile cost of a real optimizer.

### Tier 2: Maglev (Mid-Tier Optimizing JIT) (V8 2023+)

**Maglev** is a new SSA-based mid-tier compiler. It performs real optimizations (inlining, type specialization) but compiles faster than TurboFan. It targets the sweet spot between Sparkplug's speed and TurboFan's quality.

### Tier 3: TurboFan (Optimizing JIT)

**TurboFan** is V8's full optimizing compiler using a **Sea of Nodes IR** (nodes represent both control and data flow). It performs aggressive optimizations: inlining, escape analysis, loop peeling, deoptimization guards.

### Deoptimization

When a JIT-compiled function receives input that violates its type assumptions (e.g., an `int` function receives a `float`), it **deoptimizes** — throws away the native code and falls back to the interpreter. This is why JavaScript type stability matters for performance.

### Implementing a Toy JIT (copy-and-patch)

Python 3.13 implements the **copy-and-patch JIT** (PEP 744), which is the same technique V8's Sparkplug uses:

1. For each bytecode pattern, store a pre-compiled native code template with **holes** (undefined references).
2. When compiling a function, **copy** the template and **patch** the holes with actual addresses/values.
3. No real optimization — just a fast 1:1 translation from bytecode to native.

This gives ~1.5–3× speedup over pure bytecode interpretation with minimal compile time.

---

## 📚 6. Garbage Collection Strategies

All VM-based runtimes need automatic memory management. The four main strategies:

### Mark-Sweep (JVM G1, Ruby)

1. **Mark phase**: starting from roots (stack, globals), recursively mark all reachable objects.
2. **Sweep phase**: scan the heap; free any unmarked object.
3. Optionally **compact**: move live objects together to eliminate fragmentation.

```python
def mark_sweep(roots: list, heap: dict):
    marked = set()
    # Mark phase
    worklist = list(roots)
    while worklist:
        obj = worklist.pop()
        if id(obj) not in marked:
            marked.add(id(obj))
            worklist.extend(get_children(obj))
    # Sweep phase
    for addr, obj in list(heap.items()):
        if addr not in marked:
            del heap[addr]   # free
```

**Stop-the-world**: the classic implementation pauses all threads during GC. Modern collectors (G1, ZGC) do most work concurrently.

### Generational GC (CPython 3.x, HotSpot)

Most objects die young (the **generational hypothesis**). Split the heap into generations:
- **Gen 0 (nursery)**: newly created objects — collected frequently and cheaply.
- **Gen 1**: objects that survived one collection.
- **Gen 2**: long-lived objects — collected rarely.

When Gen 0 is full, collect only Gen 0. Most garbage is found there. Surviving objects are promoted to Gen 1. This makes common-case GC very fast.

### Reference Counting (CPython's primary GC, Swift ARC, Rust's `Rc`)

Every object has a **reference count**. When it reaches zero, free immediately.

```python
class RefCounted:
    def __init__(self, value):
        self.value = value
        self._refcount = 1

    def incref(self):
        self._refcount += 1

    def decref(self):
        self._refcount -= 1
        if self._refcount == 0:
            self._destroy()
```

**Pros**: deterministic destruction (important for file handles, locks), no stop-the-world pauses, no GC thread needed.

**Cons**: cycles are not collected (reference cycle: A → B → A; neither reaches zero). CPython adds a **cycle detector** (the generational GC) on top of refcounting to handle cycles.

**ARC (Automatic Reference Counting)** in Swift and Rust's `Rc<T>` are compile-time-inserted versions of this pattern.

### RAII / Ownership (Rust)

Rust's approach: **no garbage collector at all**. The borrow checker (see [15.4](15.4---Type-Systems-&-Type-Checking)) tracks ownership statically. When an owner goes out of scope, the compiler inserts a destructor call (the `Drop` trait).

```rust
{
    let v = Vec::new();       // allocate
    v.push(1);
    v.push(2);
}   // ← compiler inserts `drop(v)` here — free at scope exit
```

No runtime overhead, no GC pauses, deterministic destruction. Cost: the borrow checker rules must be obeyed at compile time.

---

## 📚 7. WebAssembly (Wasm)

**WebAssembly** is a binary instruction format for a stack-based virtual machine. It was designed as a compilation target for C, C++, Rust, Go, and others, initially for the browser but increasingly for server-side use (WASI, edge computing).

### Why Wasm Is Safe

- **No arbitrary memory access**: pointers are checked against linear memory bounds.
- **No system calls**: all I/O goes through imports (controlled by the host).
- **Typed**: every function has an explicit type signature checked at load time.
- **Sandboxed**: Wasm modules cannot access memory outside their linear memory region.
- **No undefined behavior**: unlike C, Wasm traps (aborts) on integer overflow and out-of-bounds access.

### Wasm Stack Machine

```wasm
;; Function: add(i32, i32) -> i32
(func $add (param $x i32) (param $y i32) (result i32)
  local.get $x     ;; push x
  local.get $y     ;; push y
  i32.add          ;; pop two, push sum
)
```

### Wasm Performance

V8 compiles Wasm to native code **at load time** using a streaming compiler. Wasm typically runs at 1.0–1.5× the speed of equivalent native code (some overhead from bounds-checking and memory model constraints).

### WASI — WebAssembly System Interface

WASI provides a standard API for system-level operations (file I/O, networking, clocks) in a sandboxed way. Combined with the component model (typed interfaces between Wasm modules), WASI is enabling Wasm as a universal plugin format and edge compute substrate.

---

## 📚 8. Comparing Language Runtime Strategies

| Language | Primary runtime model | GC strategy |
|---|---|---|
| **Python** | Bytecode VM (CPython) | Refcount + cycle detector |
| **Java** | Bytecode (JVM) + JIT | Generational (G1, ZGC, Shenandoah) |
| **JavaScript** | Bytecode + JIT tiers (V8) | Generational mark-sweep |
| **C#/.NET** | Bytecode (CLR) + JIT | Generational mark-sweep (GC) |
| **Rust** | AOT native | RAII / no GC |
| **C/C++** | AOT native | Manual (no GC) |
| **Go** | AOT native + goroutines | Concurrent mark-sweep |
| **Lua** | Bytecode VM | Incremental mark-sweep |
| **WebAssembly** | Stack VM + JIT (host) | Host-provided (or RAII) |

---

## 🔗 9. Cross-links & Further Reading

### Internal
- [15.5 - Intermediate Representations & IR Design](15.5---Intermediate-Representations-&-IR-Design) — the IR that VMs and JITs use internally
- [15.7 - Optimization Passes](15.7---Optimization-Passes) — JIT applies many of the same passes as AOT compilers
- [1.4 - Concurrency - asyncio, threading, multiprocessing & the GIL](1.4---Concurrency---asyncio,-threading,-multiprocessing-&-the-GIL) — Python's GIL and memory model
- [Subject_Plan](Subject_Plan) — ML runtimes (XLA, TVM, TorchScript)

### External
- [Crafting Interpreters — Part III (A Bytecode Virtual Machine)](https://craftinginterpreters.com/a-bytecode-virtual-machine.html)
- [CPython dis module](https://docs.python.org/3/library/dis.html)
- [CPython Developer Guide — Design of CPython's compiler](https://devguide.python.org/internals/compiler/)
- [V8 blog — Understanding V8's bytecode](https://v8.dev/blog/ignition-interpreter)
- [V8 blog — Maglev](https://v8.dev/blog/maglev)
- [PEP 744 — JIT Compilation](https://peps.python.org/pep-0744/)
- [WebAssembly specification](https://webassembly.github.io/spec/)
- [WASI preview 2 documentation](https://github.com/WebAssembly/WASI)
- [Lua 5 VM paper (Ierusalimschy)](https://www.lua.org/doc/jucs05.pdf)

---

## ⚠️ 10. Common Misconceptions

- **"CPython is slow because of the interpreter."** The interpreter loop itself is fast; the cost is Python's dynamic type dispatch on every operation (every `+` checks the types of both operands at runtime). PyPy mitigates this with JIT compilation; CPython 3.11+ mitigates it with specialization.
- **"JIT always makes things faster."** JIT has warmup cost. Short-lived programs (scripts) may exit before the JIT fires. Compile-time PGO (via Bolt or FDO) is often more effective for batch-processing programs.
- **"Reference counting is a GC strategy."** It is *an* automatic memory management strategy, but not what most people mean by "GC" (which implies a tracing algorithm). Refcounting can coexist with a tracing GC (as in CPython: refcounting for most objects, cycle detector for cycles).
- **"WebAssembly is only for the browser."** Originally yes, but WASI and the component model are making Wasm a server-side and edge compute platform. Fermyon Spin, Cloudflare Workers, and WasmEdge all run Wasm server-side.
- **"Python's GIL means Python can't use multiple cores."** The GIL prevents *Python bytecode threads* from running in parallel. But: (a) C extension code releases the GIL; (b) multiprocessing bypasses the GIL; (c) Python 3.13 experimental free-threaded mode removes the GIL entirely.

---

*Back to: [README](README) — Subject Hub | [Subject_Plan](Subject_Plan) — Full curriculum | [LEARNING_PATH](LEARNING_PATH) — Roadmap*
