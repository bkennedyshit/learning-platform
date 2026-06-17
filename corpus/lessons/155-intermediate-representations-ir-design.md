---
title: "15.5 — Intermediate Representations & IR Design"
subject: "Compilers & Language Design"
catalog: advanced
audience_tier: higher-education
chapter: "15.5"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 15.5 — Intermediate Representations & IR Design

> *"A good IR is like a good API: it's the right granularity of abstraction for the passes that consume it. Too high-level and you can't optimize. Too low-level and you can't reason."*

An **Intermediate Representation (IR)** is a data structure that lives between the high-level AST and the final machine code. A well-designed IR:

- Strips away language-specific syntax while preserving semantics
- Is easy for optimisation passes to analyse and transform
- Is portable (multiple targets can be generated from one IR)
- Is typed (so errors are caught before codegen)

This chapter covers the principal IR forms: **three-address code**, **Static Single Assignment (SSA)** form, **control-flow graphs (CFG)**, and **LLVM IR** — the industrial-strength IR behind Clang, Rust, Swift, Zig, and many other compilers.

---

## 🎯 Learning Objectives

1. Explain **three-address code** and convert a simple expression to it.
2. Explain **SSA form** — why each variable is defined exactly once.
3. Understand **phi nodes** and why they're needed at join points.
4. Draw a **control-flow graph** for an if/else and a loop.
5. Read and write basic **LLVM IR** (types, functions, basic blocks, instructions).
6. Use `clang -emit-llvm` to inspect real IR for C/C++ code.
7. Understand what **dataflow analysis** is and how it uses the CFG.

---

## 🖼️ Visual Anchor

![comp-15__fig3](comp-15__fig3.svg)

---

## 📚 1. Three-Address Code (TAC)

The simplest widely-used IR form. Every instruction has **at most three addresses** (operands): a result and at most two inputs.

### Form

```
result = operand₁ op operand₂   (binary)
result = op operand₁             (unary)
result = operand₁                (copy)
goto L                           (unconditional jump)
if t goto L                      (conditional jump)
result = call f(a₁, ..., aₙ)    (function call)
param a                          (push arg for upcoming call)
```

### Worked Example: `z = x + y * 2 - 1`

```
t1 = y * 2
t2 = x + t1
t3 = t2 - 1
z  = t3
```

Each temporary `tN` is a **virtual register** — an infinite-capacity register that the register allocator will later map to physical hardware registers.

### Python TAC Generator

```python
class TACGen:
    def __init__(self):
        self.instrs: list[str] = []
        self._count = 0

    def _fresh(self) -> str:
        self._count += 1
        return f"t{self._count}"

    def gen(self, node) -> str:
        from ast_nodes import Num, Name, BinOp, UnaryOp

        if isinstance(node, Num):
            t = self._fresh()
            self.instrs.append(f"{t} = {node.value}")
            return t
        if isinstance(node, Name):
            return node.id   # variable names are already "addresses"
        if isinstance(node, BinOp):
            l = self.gen(node.left)
            r = self.gen(node.right)
            t = self._fresh()
            self.instrs.append(f"{t} = {l} {node.op} {r}")
            return t
        if isinstance(node, UnaryOp):
            operand = self.gen(node.operand)
            t = self._fresh()
            self.instrs.append(f"{t} = {node.op}{operand}")
            return t
        raise ValueError(f"Unknown node: {node}")

# TAC for: z = x + y * 2
gen = TACGen()
result = gen.gen(assign.value)
gen.instrs.append(f"z = {result}")
for instr in gen.instrs:
    print(instr)
# t1 = y * 2
# t2 = x + t1
# z = t2
```

---

## 📚 2. Control-Flow Graphs (CFG)

A **CFG** models the *flow of control* through a function:

- **Nodes** are **basic blocks** — maximal sequences of straight-line code (no branches in the middle, one entry, one exit).
- **Edges** represent possible control transfers (unconditional jumps, conditional branches, fall-throughs).

### Basic Block Properties

A basic block:
- Starts at a **leader**: the function entry, any jump target, or any instruction following a branch.
- Ends at a **branch**, **jump**, or **return**.
- All instructions in a basic block execute in sequence if the block is entered.

### Building a CFG

```python
@dataclass
class BasicBlock:
    label: str
    instrs: list[str]
    succs: list['BasicBlock']
    preds: list['BasicBlock']

def build_cfg(tac_instrs: list[str]) -> list[BasicBlock]:
    """Split TAC into basic blocks and link them."""
    # Pass 1: find leaders
    leaders = {0}
    for i, instr in enumerate(tac_instrs):
        if instr.startswith(('goto ', 'if ')):
            # the target label is a leader
            target = instr.split()[-1]
            for j, other in enumerate(tac_instrs):
                if other == f"{target}:":
                    leaders.add(j)
            if i + 1 < len(tac_instrs):
                leaders.add(i + 1)   # instruction after a branch is a leader

    # Pass 2: create blocks
    sorted_leaders = sorted(leaders)
    blocks = {}
    for idx, start in enumerate(sorted_leaders):
        end = sorted_leaders[idx + 1] if idx + 1 < len(sorted_leaders) else len(tac_instrs)
        label = f"B{idx}"
        instrs = tac_instrs[start:end]
        blocks[start] = BasicBlock(label, instrs, [], [])
    return list(blocks.values())
```

---

## 📚 3. SSA Form — Static Single Assignment

### The Problem with TAC

In plain TAC, a variable can be assigned multiple times:

```
x = 1         # definition 1
x = x + 1     # definition 2 — reuses 'x'
```

This creates **def-use chains** that are hard to track. Which definition of `x` does each use refer to?

### SSA Solution: One Definition Per Variable

In SSA, every variable has exactly **one static definition**. Multiple assignments are renamed:

```
x₁ = 1         # x version 1
x₂ = x₁ + 1   # x version 2 — new name
```

### The Phi Node Problem

When control flow **merges** (after an if/else), two different definitions of the same original variable might be live. SSA introduces the **φ (phi) function**:

```
if condition goto then, else
then:
    x₁ = 1
    goto merge
else:
    x₂ = 2
    goto merge
merge:
    x₃ = φ(x₁, x₂)   ← "pick x₁ if came from then, x₂ if came from else"
```

The phi function is *not* a real instruction — it is a theoretical construct that the register allocator resolves into parallel copies or branch targets during code generation.

### SSA Properties That Enable Optimization

- **Immediate reach**: because each variable is defined once, every use can be linked back to its unique definition in O(1).
- **Sparse representation**: you only need def-use and use-def chains, not full dataflow computation.
- **Enables**: global value numbering (GVN), constant propagation, dead code elimination, and many other passes that are much harder without SSA.

---

## 📚 4. LLVM IR — Industrial Strength

**LLVM IR** is the IR used by Clang, Rust, Swift, Zig, Julia, and many others. It is:

- **Typed**: every value has an explicit LLVM type (`i32`, `f64`, `ptr`, `<4 x float>` for SIMD, etc.)
- **SSA**: every virtual register is defined once
- **Infinite virtual registers**: `%0`, `%1`, ... — the register allocator handles the rest
- **Target-neutral**: the same IR runs through any LLVM backend (x86, ARM, RISC-V, Wasm)

### LLVM IR Syntax

```llvm
; define a function
define i32 @add(i32 %x, i32 %y) {
entry:
  %0 = add i32 %x, %y     ; %0 = x + y
  ret i32 %0               ; return %0
}
```

| Part | Meaning |
|---|---|
| `define i32 @add(...)` | Function definition, returns `i32` |
| `i32 %x, i32 %y` | Parameters with types and SSA names |
| `entry:` | First basic block (required label) |
| `%0 = add i32 %x, %y` | SSA assignment: `%0` is defined once |
| `ret i32 %0` | Return instruction, must end every basic block |

### Real IR: if/else with Phi Node

C source:
```c
int max(int a, int b) {
    if (a > b) return a;
    else return b;
}
```

LLVM IR (simplified):
```llvm
define i32 @max(i32 %a, i32 %b) {
entry:
  %cmp = icmp sgt i32 %a, %b    ; signed greater-than comparison
  br i1 %cmp, label %then, label %else

then:
  br label %merge

else:
  br label %merge

merge:
  %result = phi i32 [ %a, %then ], [ %b, %else ]
  ret i32 %result
}
```

The `phi` instruction selects `%a` if control came from `%then`, or `%b` if it came from `%else`.

### Generating LLVM IR from Your Own Compiler

```bash
# Emit LLVM IR for a C file:
clang -O0 -emit-llvm -S -o output.ll input.c

# Emit with optimisations (see the difference):
clang -O2 -emit-llvm -S -o output_opt.ll input.c

# For Rust:
rustc --emit=llvm-ir input.rs

# Visualise the CFG:
opt -dot-cfg output.ll && dot -Tpng .add.dot -o add.png
```

---

## 📚 5. Dataflow Analysis

**Dataflow analysis** is the family of algorithms that compute facts about variables at each program point, using the CFG structure.

### The Framework

Every dataflow problem defines:
- A **lattice** of facts (e.g., "variable X is definitely defined" = TOP, "possibly undefined" = BOTTOM)
- A **transfer function** for each instruction: how the instruction transforms the incoming facts
- A **meet** operation: how facts are merged at join points

The analysis propagates facts around the CFG until a **fixed point** is reached.

### Common Analyses

| Analysis | Direction | Use |
|---|---|---|
| **Reaching definitions** | Forward | Which definition of X reaches this use? |
| **Liveness analysis** | Backward | Is variable X live (read later) at this point? |
| **Available expressions** | Forward | Is expression `a+b` already computed at this point? |
| **Definite assignment** | Forward | Is X definitely assigned on all paths? |
| **Interval analysis** | Forward | What range of values can X hold? |

### Liveness Analysis Example

```python
def liveness(blocks: list[BasicBlock]):
    """
    Compute LIVE_IN and LIVE_OUT for each block.
    A variable is live-out at block B if it is used in a
    successor before being redefined.
    """
    for b in blocks:
        b.live_in = set()
        b.live_out = set()

    changed = True
    while changed:
        changed = False
        for b in reversed(blocks):   # backward pass
            new_out = set()
            for s in b.succs:
                new_out |= s.live_in
            new_in = (b.use_set | (new_out - b.def_set))
            if new_in != b.live_in or new_out != b.live_out:
                b.live_in = new_in
                b.live_out = new_out
                changed = True
```

Liveness is used by the register allocator (see [15.6](15.6---Code-Generation-&-Backends)) and by dead-code elimination (see [15.7](15.7---Optimization-Passes)).

---

## 📚 6. MLIR — Multi-Level IR

**MLIR** (Multi-Level IR) is the 2024–2026 architectural evolution of LLVM. Instead of one fixed IR, MLIR provides a *framework* for defining custom IR **dialects** at multiple abstraction levels:

| Dialect | Abstraction level |
|---|---|
| `tensor` dialect | High-level tensor operations (ML frameworks) |
| `linalg` dialect | Linear algebra (matrix multiply, convolution) |
| `affine` dialect | Loop nests with affine indexing |
| `llvm` dialect | Maps 1:1 to LLVM IR |
| `wasm` dialect | WebAssembly bytecode |

Each dialect can be **progressively lowered** to more concrete dialects, and each lowering step can apply optimizations appropriate to that level. This is the architecture behind Google's XLA (ML compilation), Intel's MLIR for FPGAs, and hardware compiler backends.

---

## 🔗 7. Cross-links & Further Reading

### Internal
- [15.4 - Type Systems & Type Checking](15.4---Type-Systems-&-Type-Checking) — the type-checked AST that IR is lowered from
- [15.6 - Code Generation & Backends](15.6---Code-Generation-&-Backends) — what LLVM IR is lowered into
- [15.7 - Optimization Passes](15.7---Optimization-Passes) — passes that run on the IR

### External
- [LLVM Language Reference Manual](https://llvm.org/docs/LangRef.html)
- [LLVM Kaleidoscope Tutorial — Ch. 3 (Code Generation to LLVM IR)](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl03.html)
- [Cornell CS 6120 — SSA and Dataflow lectures](https://www.cs.cornell.edu/courses/cs6120/2020fa/lesson/)
- [MLIR project documentation](https://mlir.llvm.org/)
- [Bril — Teaching IR](https://capra.cs.cornell.edu/bril/)
- [Crafting Interpreters — Ch. 14 (Chunks of Bytecode)](https://craftinginterpreters.com/chunks-of-bytecode.html)

---

## ⚠️ 8. Common Misconceptions

- **"SSA means the variable is constant."** No — SSA means each *name* is assigned once. Multiple names (x₁, x₂, ...) can represent the same logical variable at different points. They may hold different values.
- **"Phi nodes are real instructions."** Conceptually yes, physically no. The register allocator inserts parallel copies and branch-target moves to implement phi semantics in real machine code.
- **"LLVM IR is assembly."** LLVM IR is higher-level than assembly: it has types, infinite virtual registers, and structured control flow. It is also more portable — the same IR can target x86, ARM, or Wasm.
- **"I only need LLVM IR if I write a compiler."** Not true — `opt -analyze` and `clang -emit-llvm` are powerful debugging tools. If a Rust function isn't being optimized the way you expect, reading its LLVM IR (`rustc --emit=llvm-ir`) is often the most direct diagnosis.

---

*Next: [15.6 - Code Generation & Backends](15.6---Code-Generation-&-Backends) — From IR to real machine instructions.*
