---
title: "15.6 — Code Generation & Backends"
subject: "Compilers & Language Design"
catalog: advanced
audience_tier: higher-education
chapter: "15.6"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 15.6 — Code Generation & Backends

> *"The back end is where beauty meets physics. You can't violate the ISA. The registers are finite. The memory hierarchy is real."*

The **code generation** phase translates machine-neutral IR into actual machine instructions. It has three main sub-problems:

1. **Instruction selection** — which machine instructions express each IR operation?
2. **Register allocation** — how do we map unlimited virtual registers to a finite set of physical registers?
3. **Instruction scheduling** — in what order should we emit instructions to keep the CPU pipeline full?

After this chapter, `clang -O2 int add(int x, int y) { return x+y; }` will be fully explicable.

---

## 🎯 Learning Objectives

1. Explain the three phases of a compiler back-end: instruction selection, register allocation, scheduling.
2. Understand **CISC vs RISC** instruction set design trade-offs.
3. Trace **register allocation by graph colouring** for a small example.
4. Memorise the **System V AMD64 calling convention** (x86-64 Linux/macOS).
5. Read assembly output from `clang` / `gcc` for simple functions.
6. Use **Compiler Explorer (godbolt.org)** to inspect assembly interactively.
7. Understand what **spilling** is and when it happens.

---

## 🖼️ Visual Anchor

![comp-15__fig4](comp-15__fig4.svg)

---

## 📚 1. Instruction Selection

**Instruction selection** maps IR instructions to target machine instructions. This is harder than it sounds: modern CPUs have complex instructions that do more than one thing.

### Tree Pattern Matching

The most principled approach is **tree pattern matching** (Aho-Corasick style). Each machine instruction is described as a tree pattern over IR operations. The selector finds the covering of the IR tree with the highest-weight (fewest instructions) set of patterns.

```
IR tree:           Machine pattern:
  STORE             LEA  rax, [rbx + rcx*4]   (scaled index addressing)
    ADD              matches:
      rbx            STORE(ADD(base, MUL(index, 4)), value)
      MUL
        rcx
        4
    value
```

LLVM uses a **Directed Acyclic Graph (DAG)** form of the IR and a table-driven pattern matcher (SelectionDAG). More modern backends use MLIR's instruction selection framework.

### CISC vs RISC

| Property | CISC (x86-64) | RISC (ARM64, RISC-V) |
|---|---|---|
| Instruction variety | Hundreds, varying size | ~60 fixed-size instructions |
| Operand encoding | Memory operands in many instructions | Load/store only — no memory in ALU ops |
| Instruction width | 1–15 bytes | 4 bytes (fixed) |
| Code density | Higher | Lower (but SIMD helps) |
| JIT compilation | Harder (variable width) | Easier (fixed width, predictable) |

RISC CPUs are dominant in mobile (ARM64) and are growing in server (AWS Graviton, Apple M-series). Understanding this explains why mobile code is structured differently.

---

## 📚 2. Register Allocation — Graph Colouring

After instruction selection, the code has unlimited **virtual registers** (`%0`, `%1`, ...). Physical registers are finite (x86-64 has 16 general-purpose integer registers). Register allocation assigns physicals to virtuals.

### Liveness Intervals

First, compute how long each virtual register is **live** (from its definition to its last use):

```
Instruction:   t1 = x + y    t2 = t1 * 2    t3 = t1 + z    result = t2 + t3
Live ranges:   t1:  [1, 3]   t2:  [2, 4]    t3:  [3, 4]
```

Two virtual registers **interfere** if their live ranges overlap — they cannot share a physical register.

### The Interference Graph

Nodes = virtual registers. Edge between `tA` and `tB` if they interfere.

**Register allocation = graph k-colouring** where k = number of available physical registers.

```python
def colour_graph(graph: dict, k: int) -> dict:
    """
    Simplified Chaitin-Briggs register allocation by graph colouring.
    Returns a mapping {virtual_reg: physical_reg} or raises if spilling needed.
    """
    colours = {}   # virtual → physical
    stack = []

    # Phase 1: simplify — push nodes with degree < k
    remaining = set(graph.keys())
    while remaining:
        candidates = [n for n in remaining if len([m for m in graph[n] if m in remaining]) < k]
        if candidates:
            node = candidates[0]
            remaining.remove(node)
            stack.append(node)
        else:
            # No candidates — must spill one node
            spill = max(remaining, key=lambda n: len(graph[n]))  # spill highest-degree
            remaining.remove(spill)
            colours[spill] = 'SPILL'
            return colours   # restart with spilled node replaced

    # Phase 2: rebuild — assign colours
    while stack:
        node = stack.pop()
        used = {colours[m] for m in graph[node] if m in colours and colours[m] != 'SPILL'}
        for c in range(k):
            if c not in used:
                colours[node] = c
                break
        else:
            colours[node] = 'SPILL'

    return colours
```

### When Spilling Occurs

If a register cannot be coloured, it is **spilled**: its value is stored to a stack slot (memory) whenever it is defined, and reloaded every time it is used. Spilling is correct but slow (each access is a memory load/store).

The register allocator tries to **minimise spills** by choosing the right nodes to remove first (heuristic: spill the node with the longest live range or lowest usage frequency).

---

## 📚 3. Calling Conventions

A **calling convention** specifies how function calls work at the machine level: which registers hold arguments, which hold the return value, which registers the caller must save, and how the stack is laid out.

### System V AMD64 ABI (Linux, macOS)

This is the calling convention for x86-64 programs on Linux and macOS.

**Integer / pointer arguments** (left to right):
| Argument # | Register |
|---|---|
| 1st | `rdi` |
| 2nd | `rsi` |
| 3rd | `rdx` |
| 4th | `rcx` |
| 5th | `r8` |
| 6th | `r9` |
| 7th+ | Stack (pushed right to left) |

**Floating-point arguments**: `xmm0`–`xmm7`

**Return values**: `rax` (integer), `xmm0` (float/double), `rdx:rax` (128-bit)

**Caller-saved (scratch) registers** — the called function may overwrite these:
`rax, rcx, rdx, rsi, rdi, r8, r9, r10, r11`

**Callee-saved registers** — the called function must restore these if it uses them:
`rbx, rbp, r12, r13, r14, r15`

**Stack alignment**: must be 16-byte aligned before a `CALL` instruction.

**Red zone**: leaf functions (no sub-calls) may use the 128 bytes *below* `rsp` without adjusting the stack pointer. Kernel handlers clobber this — don't use in signal handlers.

### Windows x64 ABI (different!)

Windows uses `rcx, rdx, r8, r9` for the first four arguments, and requires a **shadow space** (32 bytes) on the stack even when the function takes ≤4 arguments. This is a common source of bugs in cross-platform assembly code.

---

## 📚 4. Worked Example — Assembly for `int add(int x, int y)`

C source:
```c
int add(int x, int y) {
    return x + y;
}
```

Compiling with `clang -O2 -S` (or [godbolt.org](https://godbolt.org)) gives:

```asm
add:                          # function label (mangled for C linkage)
    lea    eax, [rdi + rsi]   # eax = x (edi) + y (esi)
    ret                       # return value in eax
```

Line-by-line:
- `rdi` = first integer arg = `x`; `esi`/`rsi` = second integer arg = `y`
- `lea eax, [rdi + rsi]` — "load effective address" computes `rdi + rsi` without touching flags, result in `eax` (lower 32 bits of `rax`). The compiler uses `lea` instead of `add` when it can because `lea` doesn't modify flags.
- `ret` — return; return value is in `rax`/`eax` per System V ABI.

Total: **2 instructions** at O2. The call overhead (push/pop, setup) is entirely the *caller's* cost.

### Unoptimised (`-O0`) vs Optimised (`-O2`)

At `-O0`, Clang generates:
```asm
add:
    push   rbp
    mov    rbp, rsp
    mov    dword ptr [rbp - 4],  edi    ; spill x to stack
    mov    dword ptr [rbp - 8],  esi    ; spill y to stack
    mov    eax, dword ptr [rbp - 4]     ; reload x
    add    eax, dword ptr [rbp - 8]     ; add y
    pop    rbp
    ret
```

8 instructions vs 2 — the debug frame (rbp setup, spills) is removed entirely by `-O2`.

---

## 📚 5. Instruction Scheduling

After register allocation, the instructions are reordered to avoid **pipeline stalls**:

- Modern CPUs are superscalar (execute multiple instructions per cycle) and out-of-order, but compilers can still help by placing independent instructions before dependent ones.
- **Data hazard**: instruction B needs the result of instruction A — must wait.
- **List scheduling**: build a dependency graph, then emit instructions using a topological sort that prioritises long dependency chains.

Example:
```asm
; Original (dependent — stall between mul and add)
mul rax, rbx     ; latency 3 cycles
add rcx, rax     ; must wait for mul

; After scheduling (independent work fills the gap)
mul rax, rbx
mov rdx, [rbp-8]  ; independent load — execute while mul runs
add rcx, rax
```

---

## 📚 6. ELF Object Files and the Linker

After assembly, the compiler produces an **ELF object file** (`.o` on Linux, `.obj` on Windows). The **linker** combines multiple object files into an executable:

- Resolves **symbol references**: `call add` in `main.o` is linked to the actual `add` symbol defined in `add.o`.
- Assigns **virtual addresses** to sections (`.text`, `.data`, `.bss`, `.rodata`).
- Produces **relocation entries**: absolute addresses that must be patched after loading.

```bash
# Compile to object file
clang -c -O2 add.c -o add.o

# Link to executable
clang add.o main.o -o prog

# Inspect object symbols
nm add.o

# Disassemble
objdump -d add.o
```

---

## 🔗 7. Cross-links & Further Reading

### Internal
- [15.5 - Intermediate Representations & IR Design](15.5---Intermediate-Representations-&-IR-Design) — the IR that this pass consumes
- [15.7 - Optimization Passes](15.7---Optimization-Passes) — passes that run before or after instruction selection
- [Subject_Plan](Subject_Plan) — understanding C++ compilation

### External
- [Compiler Explorer — godbolt.org](https://godbolt.org/) — interactive source → assembly view
- [System V AMD64 ABI Specification](https://gitlab.com/x86-psABIs/x86-64-ABI)
- [LLVM — Kaleidoscope Ch. 6–7 (Extending with Codegen)](https://llvm.org/docs/tutorial/)
- [Matt Godbolt — What Has My Compiler Done for Me Lately? (CppCon)](https://www.youtube.com/watch?v=bSkpMdDe4g4)
- [CS:APP — Chapter 3 (Machine-Level Representation of Programs)](https://csapp.cs.cmu.edu/)
- [Agner Fog's microarchitecture guide](https://agner.org/optimize/) — latency/throughput tables for x86 instructions

---

## ⚠️ 8. Common Misconceptions

- **"Register allocation is just a greedy assignment."** Greedy works for simple cases. But Chaitin's proof that register allocation is NP-complete means production allocators use heuristics (LLVM uses Linear Scan for speed, graph colouring for quality, with a configurable choice).
- **"More registers = always better."** Above ~32 registers, the benefit diminishes because the register file access time increases and code size grows (larger register operand fields).
- **"Calling conventions are universal."** They are not. Linux/macOS (System V), Windows (Microsoft), ARM64 Linux, ARM64 Apple Silicon, and WebAssembly all have different conventions. Cross-language FFI bugs are often calling convention mismatches.
- **"lea is for addresses only."** `lea` is commonly used for arithmetic on integers because it can compute `base + index*scale + offset` in one instruction without touching flags. It's a multiply-add unit masquerading as an address instruction.

---

*Next: [15.7 - Optimization Passes](15.7---Optimization-Passes) — Teaching the compiler to make your code faster.*
