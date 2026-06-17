---
title: "15.4 — Type Systems & Type Checking"
subject: "Compilers & Language Design"
catalog: advanced
audience_tier: higher-education
chapter: "15.4"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 15.4 — Type Systems & Type Checking

> *"A type system is a tractable syntactic method for proving the absence of certain program behaviors by classifying phrases according to the kinds of values they compute."* — Benjamin Pierce, *Types and Programming Languages*

Types are not just annotations for documentation. A sound type system is a **proof system**: if the type checker accepts your program, it has proved the absence of an entire class of bugs — no wrong-type operations, no null pointer dereferences (in some systems), no use-after-free (Rust). Understanding how type systems work explains why TypeScript catches some bugs but not others, why Rust's borrow checker exists, and why Python's type hints are optional.

---

## 🎯 Learning Objectives

1. Distinguish **static vs dynamic**, **strong vs weak**, **nominal vs structural**, and **manifest vs inferred** typing.
2. Explain **Hindley-Milner type inference** and trace **unification** through a simple example.
3. Implement a **miniature bidirectional type-checker** in Python.
4. Explain **subtyping** (Liskov), **covariance**, **contravariance**, and **invariance**.
5. Explain how **generics** work in TypeScript (erasure), Java (erasure), and Rust (monomorphisation).
6. Explain Rust's **borrow checker** as a type-system extension.

---

## 🖼️ Visual Anchor

![comp__29.4-fig1](comp__29.4-fig1.svg)

---

## 📚 1. The Type System Axes

### Static vs Dynamic

| | Static | Dynamic |
|---|---|---|
| When types checked | Compile time | Runtime |
| Examples | C, C++, Rust, Java, TypeScript, Go | Python, JavaScript, Ruby, Lua |
| Benefit | Catch bugs early; enable optimization | Faster prototyping |
| Cost | More annotation burden (mitigated by inference) | Runtime type errors |

Python 3 type hints are *optional* static annotations that a separate checker (mypy, pyright) validates — the runtime is still dynamic.

### Strong vs Weak

- **Strong**: the language enforces types at runtime. Python: `"3" + 3` → `TypeError`.
- **Weak**: implicit coercions across types. C: `void*` can be cast to anything. JavaScript: `"3" + 3` → `"33"`.

### Nominal vs Structural

- **Nominal**: two types are the same only if they have the same name/declaration. Java: two classes with identical fields are not interchangeable without explicit inheritance.
- **Structural**: two types are compatible if their *shapes* match. TypeScript: `{name: string}` is compatible with any type that has a `name: string` field.

```typescript
// TypeScript — structural (duck typing at compile time)
interface Named { name: string }
function greet(x: Named) { return `Hello, ${x.name}`; }
greet({ name: "Bill", age: 30 });  // OK — has 'name', extra field ignored
```

### Manifest vs Inferred

- **Manifest**: types must be written explicitly. Java: `int x = 3;`
- **Inferred**: compiler deduces types. Rust: `let x = 3;` → `x: i32` inferred.

Hindley-Milner provides *complete* type inference for ML-family languages (Haskell, OCaml, F#). TypeScript uses a more practical but incomplete inference.

---

## 📚 2. Type Representations

Types themselves are data structures in the compiler:

```python
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

class Type:
    pass

@dataclass(frozen=True)
class TInt(Type):
    pass   # singleton

@dataclass(frozen=True)
class TFloat(Type):
    pass

@dataclass(frozen=True)
class TBool(Type):
    pass

@dataclass(frozen=True)
class TStr(Type):
    pass

@dataclass(frozen=True)
class TFun(Type):
    param_types: tuple
    return_type: Type

@dataclass
class TVar(Type):
    """A type variable — filled during inference."""
    name: str
    instance: Optional[Type] = None   # None = still unresolved

@dataclass(frozen=True)
class TList(Type):
    elem_type: Type

@dataclass(frozen=True)
class TOptional(Type):
    inner_type: Type

# Singletons
INT   = TInt()
FLOAT = TFloat()
BOOL  = TBool()
STR   = TStr()
```

---

## 📚 3. Hindley-Milner Type Inference

The **Hindley-Milner (HM)** algorithm (1978) infers types for a lambda-calculus-based language *without any type annotations*. It is the foundation for Haskell, OCaml, F#, Rust (partially), and TypeScript's inference.

### Core Idea

Assign a **fresh type variable** to each unknown type. As the expression is traversed, generate **type constraints** (equations). **Unification** solves the equations.

### Unification Algorithm

Two types **unify** if they can be made identical by substituting type variables:

- `TInt` and `TInt` → trivially equal ✓
- `TVar('α')` and `TInt` → substitute `α := int` ✓
- `TFun(TInt, TVar('β'))` and `TFun(TVar('α'), TFloat)` → `α := int, β := float` ✓
- `TInt` and `TFloat` → FAIL — type error ✗

```python
def unify(t1: Type, t2: Type, subst: dict) -> dict:
    """
    Robinson's unification algorithm.
    Returns substitution (dict of TVar→Type).
    Raises TypeError on conflict.
    """
    t1 = apply_subst(t1, subst)
    t2 = apply_subst(t2, subst)

    if t1 == t2:
        return subst  # already equal

    if isinstance(t1, TVar):
        if occurs_in(t1, t2):
            raise TypeError(f"Recursive type: {t1} in {t2}")
        return {**subst, t1.name: t2}

    if isinstance(t2, TVar):
        return unify(t2, t1, subst)   # swap and try again

    if type(t1) != type(t2):
        raise TypeError(f"Type mismatch: {t1} vs {t2}")

    # Both same constructor — unify field by field
    if isinstance(t1, TFun):
        s = subst
        for p1, p2 in zip(t1.param_types, t2.param_types):
            s = unify(p1, p2, s)
        return unify(t1.return_type, t2.return_type, s)

    if isinstance(t1, TList):
        return unify(t1.elem_type, t2.elem_type, subst)

    raise TypeError(f"Cannot unify {t1} and {t2}")

def apply_subst(t: Type, subst: dict) -> Type:
    """Apply substitution to a type."""
    if isinstance(t, TVar):
        if t.name in subst:
            return apply_subst(subst[t.name], subst)  # chain
        return t
    if isinstance(t, TFun):
        return TFun(
            tuple(apply_subst(p, subst) for p in t.param_types),
            apply_subst(t.return_type, subst))
    if isinstance(t, TList):
        return TList(apply_subst(t.elem_type, subst))
    return t  # TInt, TFloat, etc.

def occurs_in(var: TVar, t: Type) -> bool:
    """Check if 'var' appears in 't' (prevents infinite types)."""
    t = apply_subst(t, {})
    if isinstance(t, TVar):
        return t.name == var.name
    if isinstance(t, TFun):
        return any(occurs_in(var, p) for p in t.param_types) or occurs_in(var, t.return_type)
    if isinstance(t, TList):
        return occurs_in(var, t.elem_type)
    return False
```

### Worked Example: Infer type of `let f x = x + 1`

1. Assign `x` a fresh type variable: `α`
2. `+` has type `int → int → int`
3. Left operand of `+` is `x : α` → constrain `α = int`
4. Right operand is `1 : int` → consistent
5. Result of `+` is `int`
6. Therefore `f : int → int`

No annotation needed. The constraint propagated backwards through the call.

---

## 📚 4. A Miniature Bidirectional Type-Checker

**Bidirectional type-checking** (Pierce & Turner) is a simpler alternative to full HM inference that works well for languages with some annotations:

- **Infer mode**: compute the type of an expression bottom-up.
- **Check mode**: verify an expression has an expected type (given by context).

```python
_var_counter = 0
def fresh_var() -> TVar:
    global _var_counter
    _var_counter += 1
    return TVar(f"t{_var_counter}")

class TypeChecker:
    def __init__(self):
        self.env: dict[str, Type] = {
            'print':    TFun((STR,), TInt()),    # simplified
            '__add__':  TFun((INT, INT), INT),
        }
        self.subst: dict = {}

    def infer(self, node) -> Type:
        from ast_nodes import Num, Str, Name, BinOp, Call, FuncDef

        if isinstance(node, Num):
            return FLOAT if '.' in str(node.value) else INT

        if isinstance(node, Str):
            return STR

        if isinstance(node, Name):
            if node.id not in self.env:
                raise TypeError(f"Unbound variable: {node.id!r}")
            return self.env[node.id]

        if isinstance(node, BinOp):
            lt = self.infer(node.left)
            rt = self.infer(node.right)
            if node.op in ('+', '-', '*', '/'):
                self.subst = unify(lt, INT, self.subst)
                self.subst = unify(rt, INT, self.subst)
                return INT
            if node.op in ('==', '<', '>'):
                self.subst = unify(lt, rt, self.subst)
                return BOOL

        if isinstance(node, Call):
            ft = self.infer(node.func)
            if not isinstance(ft, TFun):
                raise TypeError(f"Not callable: {ft}")
            if len(node.args) != len(ft.param_types):
                raise TypeError("Wrong number of arguments")
            for arg, param_t in zip(node.args, ft.param_types):
                at = self.infer(arg)
                self.subst = unify(at, param_t, self.subst)
            return ft.return_type

        raise TypeError(f"Cannot infer type for {node}")
```

---

## 📚 5. Subtyping and the Liskov Substitution Principle

**Subtyping** (written `S <: T`) means: anywhere a `T` is expected, an `S` may be used safely.

### Liskov Substitution Principle (LSP)

> If `S <: T`, then objects of type `S` must behave in all the ways that objects of type `T` are expected to behave. — Barbara Liskov, 1987

This is the theoretical basis for polymorphism in OO languages. `Dog <: Animal` means a `Dog` can appear wherever an `Animal` is expected.

### Variance in Generic Types

The big gotcha:

| Variance | Definition | Example |
|---|---|---|
| **Covariant** | If `S <: T` then `F<S> <: F<T>` | `IEnumerable<Dog> <: IEnumerable<Animal>` (read-only) |
| **Contravariant** | If `S <: T` then `F<T> <: F<S>` | `Action<Animal> <: Action<Dog>` (write-only) |
| **Invariant** | Neither direction holds | `List<Dog>` is NOT `<:` `List<Animal>` |

**Why is `List<Dog>` not a `List<Animal>`?** Because `List` is both readable (covariant use) and writable (contravariant use). If `List<Dog> <: List<Animal>`, you could add a `Cat` to a `List<Dog>` via the `List<Animal>` reference — type safety violated.

```typescript
// TypeScript: read-only arrays are covariant
const dogs: Dog[] = [new Dog()];
const animals: readonly Animal[] = dogs;  // OK (covariant for readonly)
animals[0].breathe();  // works — Dog is an Animal

// Mutable arrays: TypeScript is unsound here (allows this but is wrong)
const mutableAnimals: Animal[] = dogs;    // TypeScript allows but is incorrect per theory
mutableAnimals.push(new Cat());           // Cat in a Dog array — 💥 at runtime
```

Rust solves this with **lifetime variance** — a whole chapter in the Rust reference.

---

## 📚 6. Generics: Erasure vs Monomorphisation

### Type Erasure (Java, TypeScript)

Generic type parameters are erased at compile time. One compiled function exists for all type instantiations.

```java
// Java — erased to:
// List add(List list, Object item) { list.add(item); return list; }
<T> List<T> add(List<T> list, T item) {
    list.add(item);
    return list;
}
```

**Pros**: small binary, simpler runtime.
**Cons**: no specialization (e.g., can't use `int` without boxing it to `Integer`), runtime type info lost (can't do `instanceof T`).

### Monomorphisation (Rust, C++)

A separate compiled function is generated for each concrete type instantiation.

```rust
// Rust — compiler generates:
// fn id_i32(x: i32) -> i32 { x }
// fn id_f64(x: f64) -> f64 { x }
// fn id_String(x: String) -> String { x }
fn id<T>(x: T) -> T { x }
```

**Pros**: full specialization, SIMD/intrinsic per type, no boxing.
**Cons**: larger binary (can be mitigated with LTO + dead-code elimination).

---

## 📚 7. Rust's Borrow Checker as a Type System

The borrow checker is **not magic** — it is a type-level analysis over **lifetimes** (which are type variables with constraints):

- Every reference `&'a T` has a lifetime `'a` — a type variable describing how long the reference is valid.
- Constraint: `'a` must not outlive the thing it points to.
- The borrow checker is an **inference + constraint-solving pass** over the MIR (Mid-level IR).

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

The `'a` annotation tells the compiler: "the returned reference lives at most as long as *both* inputs". This is a lifetime constraint expressed in the type signature.

Key rules:
1. At any point in time, you can have *either* one mutable reference `&mut T` *or* any number of immutable references `&T` — not both.
2. References must always be valid (no dangling pointers — enforced by lifetime constraints).

This is equivalent to a linear type system plus region analysis — academic type theory made practical.

---

## 🔗 8. Cross-links & Further Reading

### Internal
- [15.3 - Abstract Syntax Trees & Semantic Analysis](15.3---Abstract-Syntax-Trees-&-Semantic-Analysis) — the AST that the type checker walks
- [15.5 - Intermediate Representations & IR Design](15.5---Intermediate-Representations-&-IR-Design) — after type-checking, lowering to IR
- [Subject_Plan](Subject_Plan) — TypeScript structural type system in depth
- [Subject_Plan](Subject_Plan) — Rust borrow checker and lifetime system

### External
- [Types and Programming Languages — Benjamin Pierce](https://www.cis.upenn.edu/~bcpierce/tapl/)
- [Write You a Haskell — Type Inference chapter](http://dev.stephendiehl.com/fun/006_hindley_milner.html)
- [Stanford CS143 — Lectures 8–12 (Type Checking)](https://online.stanford.edu/courses/cs143-compilers)
- [TypeScript Deep Dive — Type System](https://basarat.gitbook.io/typescript/)
- [Rust Reference — Lifetime Variance](https://doc.rust-lang.org/reference/subtyping.html)
- [Bidirectional Type Checking — Pierce & Turner (1998)](https://www.cs.cmu.edu/~fp/courses/15312-f04/handouts/15-bidirectional.pdf)

---

## ⚠️ 9. Common Misconceptions

- **"TypeScript is safe."** TypeScript's type system is unsound by design (it prioritises developer experience over soundness). Several constructs (`any`, type assertions, mutable array covariance) allow type errors at runtime.
- **"Generics in Java and Rust work the same way."** They don't. Java erases type parameters; Rust monomorphises. This is why Java generics can't use primitive types directly (must use `Integer`, not `int`) and why Rust generics compile to multiple specialised functions.
- **"Type inference means you don't need to understand types."** Inference deduces types; the type *system* still constrains what is valid. Understanding the rules tells you *why* the inferred type is what it is, and what to change when it's wrong.
- **"Python's type hints are checked at runtime."** They are not — they are metadata annotations. `mypy` checks them offline. At runtime, Python ignores them entirely.

---

*Next: [15.5 - Intermediate Representations & IR Design](15.5---Intermediate-Representations-&-IR-Design) — From verified AST to machine-neutral code.*
