---
title: "15.7 — Optimization Passes"
subject: "Compilers & Language Design"
catalog: advanced
audience_tier: higher-education
chapter: "15.7"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 15.7 — Optimization Passes

> *"The fastest code is no code at all. The second fastest code is code that was already computed at compile time."*

Compiler optimizations transform code to run faster (or use less memory) while **preserving observable behavior**. "Preserving behavior" is the key phrase — an optimization must not change what a correct program does, even at the edge cases.

Optimizations operate on IR (the SSA/CFG form from [15.5](15.5---Intermediate-Representations-&-IR-Design)) and are organized into **passes** — each pass walks the IR and makes a specific kind of transformation. LLVM's `-O2` pipeline runs **dozens** of passes in a specific order.

---

## 🎯 Learning Objectives

1. Implement **constant folding** and **constant propagation** in a mini-IR.
2. Understand **dead code elimination** (DCE) and liveness.
3. Explain **function inlining** — when it helps, when it hurts.
4. Explain **LICM** (Loop Invariant Code Motion) and trace an example.
5. Understand **loop unrolling** and **loop vectorisation** (SIMD).
6. Understand **global value numbering (GVN)** and **common subexpression elimination (CSE)**.
7. Describe the LLVM `-O2` pass pipeline at a high level.
8. Explain **Profile-Guided Optimization (PGO)** and why it matters for JIT.

---

## 🖼️ Visual Anchor

![comp__29.7-fig1](comp__29.7-fig1.svg)

---

## 📚 1. Constant Folding and Constant Propagation

### Constant Folding

Evaluate **constant expressions at compile time** instead of runtime.

| Before | After |
|---|---|
| `t1 = 2 * 3` | `t1 = 6` |
| `t2 = t1 + 0` | `t2 = 6` (identity: x+0=x) |
| `t3 = t2 * 1` | `t3 = 6` (identity: x*1=x) |
| `t4 = t3 * 0` | `t4 = 0` (absorption: x*0=0) |
| `if (false) {...}` | block removed entirely |

```python
def fold_binop(op: str, left, right):
    """Constant fold a binary operation if both operands are known."""
    if isinstance(left, int) and isinstance(right, int):
        match op:
            case '+': return left + right
            case '-': return left - right
            case '*': return left * right
            case '/': return left // right if right != 0 else None
            case '==': return int(left == right)
            case '<':  return int(left < right)
    # Identity/absorption laws
    if op == '+' and right == 0: return left
    if op == '+' and left  == 0: return right
    if op == '*' and right == 1: return left
    if op == '*' and left  == 1: return right
    if op == '*' and (left == 0 or right == 0): return 0
    return None  # can't fold

class ConstantFoldingPass:
    def run(self, instrs: list) -> list:
        values: dict = {}   # name → known constant
        result = []
        for instr in instrs:
            if isinstance(instr, AssignInstr):
                lv = values.get(instr.left)
                rv = values.get(instr.right, instr.right)
                lv = values.get(instr.left, instr.left) if lv is None else lv
                folded = fold_binop(instr.op, lv, rv)
                if folded is not None:
                    values[instr.dest] = folded
                    result.append(CopyInstr(instr.dest, folded))
                else:
                    result.append(instr)
            else:
                result.append(instr)
        return result
```

### Constant Propagation

After folding, **substitute known constants** wherever their names are used. This can cascade — folding one expression may expose others.

```
Before:          After fold+prop:
x = 2            x = 2
y = x * 3        y = 6
z = y + 1        z = 7
return z         return 7
```

The entire function collapses to `return 7` — no runtime computation.

---

## 📚 2. Dead Code Elimination (DCE)

A statement is **dead** if its result is never used. DCE removes dead code.

### Types of Dead Code

| Type | Example |
|---|---|
| **Unused assignment** | `x = expensive()` if `x` is never read after |
| **Unreachable block** | `if (false) { ... }` after constant folding |
| **Dead function** | Functions never called (whole-program DCE = tree shaking) |

### Liveness-Based DCE

```python
class DCEPass:
    def run(self, instrs: list) -> list:
        # backward pass: mark live variables
        live = set()
        result = []
        for instr in reversed(instrs):
            if isinstance(instr, AssignInstr):
                if instr.dest not in live:
                    continue  # dead — skip
                live.discard(instr.dest)
                live.add(instr.left)
                live.add(instr.right)
            elif isinstance(instr, ReturnInstr):
                live.add(instr.value)
            result.append(instr)
        return list(reversed(result))
```

### Tree Shaking (JavaScript/TypeScript bundlers)

In bundlers (Webpack, Rollup, esbuild), DCE is called **tree shaking**: dead-exported functions are removed from the bundle. This requires knowing at bundle time which exports are imported anywhere. ESM (ES modules) with static `import`/`export` makes this tractable. CommonJS `require()` does not.

---

## 📚 3. Function Inlining

**Inlining** replaces a call site with the body of the callee, substituting arguments for parameters.

```
Before inlining:         After inlining:
result = add(3, 4)       t1 = 3 + 4     ← body of add
                         result = t1
```

After inlining, constant folding can fire:
```
t1 = 7
result = 7
```

The call overhead (push args, call instruction, return, pop) is gone entirely.

### When to Inline

| Condition | Recommendation |
|---|---|
| Callee is small (< ~20 IR instructions) | Always inline |
| Call is in a hot loop | Strong candidate |
| Callee is recursive | Never (would loop forever) |
| Inlining would cause code size explosion | Don't |
| Only one call site exists | Almost always |

### The Inlining Threshold

LLVM uses a cost model: each instruction in the callee adds "cost", and the benefit estimate considers call frequency (from PGO). The `-inline-threshold` controls the cutoff.

Over-inlining hurts the **instruction cache**: if the inlined code is larger than the original call+callee, and the callee was shared by many sites, the total code footprint grows and icache misses increase.

---

## 📚 4. LICM — Loop Invariant Code Motion

If an expression inside a loop produces the same result on every iteration, **hoist** it out of the loop.

```python
# Before LICM
for i in range(n):
    x = a * b      # 'a' and 'b' don't change in the loop → invariant
    result[i] = x + i

# After LICM
x = a * b          # hoisted outside the loop
for i in range(n):
    result[i] = x + i
```

If n = 1 000 000, this saves 999 999 multiplications.

### LICM Requirements

For an expression `e` to be hoisted from loop L:
1. All operands of `e` are **loop-invariant** (not modified inside L).
2. The block containing `e` **dominates all exits** of L (or `e` has no side effects — exceptions, memory writes).
3. `e` has no **side effects** that depend on iteration count.

### Implementation Sketch

```python
def licm(loop: Loop, cfg: CFG):
    invariant = set()
    changed = True
    while changed:
        changed = False
        for block in loop.blocks:
            for instr in block.instrs:
                if is_invariant(instr, loop, invariant):
                    invariant.add(instr.dest)
                    changed = True

    # Hoist invariant instructions to loop pre-header
    preheader = cfg.get_or_create_preheader(loop)
    for block in loop.blocks:
        to_hoist = [i for i in block.instrs if i.dest in invariant]
        for instr in to_hoist:
            block.instrs.remove(instr)
            preheader.instrs.append(instr)
```

---

## 📚 5. Loop Unrolling and Vectorisation

### Loop Unrolling

Replicate the loop body N times, reducing the branch overhead and enabling instruction scheduling across iterations:

```python
# Before unrolling (factor 4)
for i in range(n):
    a[i] = b[i] + c[i]

# After unrolling by 4
for i in range(0, n - 3, 4):
    a[i]   = b[i]   + c[i]
    a[i+1] = b[i+1] + c[i+1]
    a[i+2] = b[i+2] + c[i+2]
    a[i+3] = b[i+3] + c[i+3]
# Tail loop for remaining elements
for i in range(n - n%4, n):
    a[i] = b[i] + c[i]
```

This exposes 4 independent additions that can be issued in parallel (if the CPU has multiple ALUs) or vectorised.

### SIMD Vectorisation

A CPU's **SIMD (Single Instruction, Multiple Data)** units can process multiple values in one instruction:

- `addps xmm0, xmm1` — add four 32-bit floats in one instruction (SSE)
- `vaddps ymm0, ymm1, ymm2` — add eight 32-bit floats in one instruction (AVX)
- `vaddps zmm0, zmm1, zmm2` — add sixteen 32-bit floats in one instruction (AVX-512)

LLVM's **loop vectorizer** automatically transforms scalar loops into SIMD loops when:
- The loop has no dependencies between iterations (no read-after-write on the same index)
- The trip count is statically known or can be computed
- The data is properly aligned (or has alignment padding)

```c
// This loop will be vectorised by clang -O2:
void add_arrays(float *a, float *b, float *c, int n) {
    for (int i = 0; i < n; i++)
        a[i] = b[i] + c[i];
}
```

Assembly (AVX2, 8 floats per instruction):
```asm
.loop:
    vmovups ymm0, [rsi + rax]   ; load 8 floats from b
    vaddps  ymm0, ymm0, [rdx + rax]  ; add 8 floats from c
    vmovups [rdi + rax], ymm0   ; store 8 floats to a
    add     rax, 32             ; advance by 32 bytes (8 × 4)
    jne     .loop
```

---

## 📚 6. Global Value Numbering (GVN) and CSE

**Common Subexpression Elimination (CSE)**: if the same expression is computed multiple times, compute it once and reuse.

**Global Value Numbering (GVN)**: assign each computed value a canonical number. Two instructions with the same value number compute the same result — one can be eliminated.

```
Before:               After GVN:
t1 = a + b            t1 = a + b
t2 = a + b            t2 = t1    ← same value number as t1
t3 = t1 * t2          t3 = t1 * t1
```

GVN in SSA form is efficient because SSA's one-definition-per-name property means value numbers flow cleanly through phi nodes.

---

## 📚 7. The LLVM `-O2` Pass Pipeline

Running `opt -O2 --print-after-all` shows the complete pass pipeline. Key passes in order:

| Pass | What it does |
|---|---|
| `mem2reg` | Promote stack allocations to SSA registers (builds SSA form) |
| `instcombine` | Constant folding + algebraic simplifications (thousands of patterns) |
| `simplifycfg` | Remove unreachable blocks, merge trivial branches |
| `early-cse` | Early common subexpression elimination |
| `inline` | Function inlining (repeated) |
| `function-attrs` | Infer function attributes (readonly, noalias) |
| `gvn` | Global value numbering |
| `licm` | Loop invariant code motion |
| `loop-unroll` | Loop unrolling |
| `loop-vectorize` | SIMD vectorisation |
| `slp-vectorize` | Superword Level Parallelism (vectorise independent scalar stores) |
| `dce` | Dead code elimination |
| `aggressive-instcombine` | More pattern-based simplifications |

The pipeline runs multiple times in iterations until no more changes occur.

---

## 📚 8. Profile-Guided Optimization (PGO)

**Static optimizations** make decisions without knowing what inputs the program will actually receive. **PGO** collects runtime profiles (which functions are hot, which branches are taken) and uses them to guide optimization decisions.

### PGO Workflow

```bash
# Step 1: compile with instrumentation
clang -fprofile-instr-generate myapp.c -o myapp_instr

# Step 2: run with representative workload
./myapp_instr < typical_input.txt
# → generates myapp.profraw

# Step 3: convert profile
llvm-profdata merge -output=myapp.profdata myapp.profraw

# Step 4: recompile using profile
clang -fprofile-instr-use=myapp.profdata -O2 myapp.c -o myapp_pgo
```

PGO typically improves performance 10–30% for compute-bound programs and is standard practice for Chrome, Firefox, and other large applications.

### What PGO Improves

- **Inlining decisions**: inline hot callees, don't inline cold ones.
- **Branch layout**: put the hot (most-taken) branch first (better branch prediction and instruction cache locality).
- **Function ordering**: group hot functions together in the binary (better icache usage).
- **Loop unroll factor**: unroll more for hot loops.

---

## 🔗 9. Cross-links & Further Reading

### Internal
- [15.5 - Intermediate Representations & IR Design](15.5---Intermediate-Representations-&-IR-Design) — the IR that these passes transform
- [15.6 - Code Generation & Backends](15.6---Code-Generation-&-Backends) — after optimization, instruction selection runs
- [15.8 - Virtual Machines, Bytecode & JIT](15.8---Virtual-Machines,-Bytecode-&-JIT) — JIT applies similar passes at runtime

### External
- [LLVM Passes documentation](https://llvm.org/docs/Passes.html)
- [Cornell CS 6120 — Lesson 3 (Local Analysis & Optimization)](https://www.cs.cornell.edu/courses/cs6120/2020fa/lesson/)
- [Engineering a Compiler — Ch. 8–10 (Cooper & Torczon)](https://www.sciencedirect.com/book/9780120884780)
- [Loop Vectorization in LLVM](https://llvm.org/docs/Vectorizers.html)
- [PGO with clang](https://clang.llvm.org/docs/UsersManual.html#profile-guided-optimization)
- [Godbolt — see -O0 vs -O2 vs -O3](https://godbolt.org/)

---

## ⚠️ 10. Common Misconceptions

- **"More optimization = always better."** `-O3` can actually be slower than `-O2` if it inlines too aggressively and blows the icache. Always benchmark.
- **"The compiler can optimize away undefined behavior."** Yes — aggressively. In C/C++, if you have UB (integer overflow, null dereference, etc.), the optimizer is allowed to assume it never happens. This can silently remove bounds checks or turn security bugs into completely wrong code.
- **"LICM hoists everything out of loops."** Only expressions with no side effects and whose operands are loop-invariant. Memory writes, IO operations, and `volatile` reads are not hoisted.
- **"DCE eliminates all unused code at link time."** Only with LTO (Link-Time Optimization). Without LTO, the linker only works at the granularity of object files, not individual functions. Dead function elimination within a module happens at compile time; cross-module DCE needs LTO.

---

*Next: [15.8 - Virtual Machines, Bytecode & JIT](15.8---Virtual-Machines,-Bytecode-&-JIT) — The runtime story: how code executes without direct compilation.*
