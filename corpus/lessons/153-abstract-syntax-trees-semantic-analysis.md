---
title: "15.3 — Abstract Syntax Trees & Semantic Analysis"
subject: "Compilers & Language Design"
catalog: advanced
audience_tier: higher-education
chapter: "15.3"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 15.3 — Abstract Syntax Trees & Semantic Analysis

> *"The AST is the truth. Syntax is just the notation humans prefer."*

The parse tree captures everything the parser saw, including parentheses, commas, and semicolons. The **Abstract Syntax Tree** strips away the punctuation and keeps only the **semantically relevant structure**. Then semantic analysis walks the AST to answer: *does this program make sense?* Not syntactically — semantically. Are names defined before use? Are types compatible? Does every path through a function return a value?

---

## 🎯 Learning Objectives

1. Design an **AST node hierarchy** using Python dataclasses.
2. Implement the **Visitor pattern** for AST traversal.
3. Build a **symbol table** with nested scopes and shadowing.
4. Implement **name resolution** — binding every identifier to its declaration.
5. Understand the sequence of semantic passes (name resolution → type checking → flow analysis).
6. Use Python's built-in **`ast` module** to inspect real Python ASTs.

---

## 🖼️ Visual Anchor

![comp__29.3-fig1](comp__29.3-fig1.svg)

---

## 📚 1. AST Node Design

The best AST design in Python uses **`dataclasses`** (or `NamedTuple`) for each node kind, grouped under a common base class. In Rust and C#, you would use an `enum` with per-variant data.

```python
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

# Base class (marker only — no data)
class ASTNode:
    pass

# --- Expressions ---
@dataclass
class Num(ASTNode):
    value: float

@dataclass
class Str(ASTNode):
    value: str

@dataclass
class Name(ASTNode):          # variable reference
    id: str
    decl: Optional[object] = field(default=None, repr=False)  # filled by resolver

@dataclass
class BinOp(ASTNode):
    op: str
    left: ASTNode
    right: ASTNode

@dataclass
class UnaryOp(ASTNode):
    op: str
    operand: ASTNode

@dataclass
class Call(ASTNode):
    func: ASTNode
    args: list[ASTNode]

# --- Statements ---
@dataclass
class Assign(ASTNode):
    target: Name
    value: ASTNode

@dataclass
class If(ASTNode):
    test: ASTNode
    then_body: list[ASTNode]
    else_body: list[ASTNode]

@dataclass
class While(ASTNode):
    test: ASTNode
    body: list[ASTNode]

@dataclass
class Return(ASTNode):
    value: Optional[ASTNode]

@dataclass
class FuncDef(ASTNode):
    name: str
    params: list[str]
    body: list[ASTNode]
    return_type: Optional[str] = None

@dataclass
class Module(ASTNode):
    stmts: list[ASTNode]
```

### Parse tree vs AST — concrete example

For `(3 + 4)`:
- **Parse tree** includes: `factor` node → `'('` leaf → `expr` subtree → `')'` leaf
- **AST**: just `BinOp('+', Num(3), Num(4))` — parentheses are gone, their *effect* (grouping) is already represented by the tree structure.

---

## 📚 2. The Visitor Pattern

The **Visitor pattern** separates *what you do with a node* from *what the node is*. Each pass (name resolution, type checking, code generation) is a separate Visitor class. Nodes never need to change.

```python
class ASTVisitor:
    """Base visitor — dispatch to visit_NodeType or generic_visit."""

    def visit(self, node: ASTNode):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node: ASTNode):
        """Default: visit all children."""
        for field_name, value in node.__dataclass_fields__.items():
            child = getattr(node, field_name)
            if isinstance(child, ASTNode):
                self.visit(child)
            elif isinstance(child, list):
                for item in child:
                    if isinstance(item, ASTNode):
                        self.visit(item)
```

### Example: Pretty-Printer Visitor

```python
class Printer(ASTVisitor):
    def __init__(self):
        self.indent = 0

    def _pad(self): return "  " * self.indent

    def visit_Num(self, node):    print(f"{self._pad()}Num({node.value})")
    def visit_Str(self, node):    print(f"{self._pad()}Str({node.value!r})")
    def visit_Name(self, node):   print(f"{self._pad()}Name({node.id!r})")

    def visit_BinOp(self, node):
        print(f"{self._pad()}BinOp({node.op!r})")
        self.indent += 1
        self.visit(node.left)
        self.visit(node.right)
        self.indent -= 1

    def visit_FuncDef(self, node):
        print(f"{self._pad()}FuncDef({node.name!r}, params={node.params})")
        self.indent += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent -= 1
```

### Alternative: Pattern Matching (Python 3.10+, Rust)

```python
def eval_expr(node: ASTNode, env: dict) -> float:
    match node:
        case Num(value=v): return v
        case Name(id=name): return env[name]
        case BinOp(op='+', left=l, right=r): return eval_expr(l, env) + eval_expr(r, env)
        case BinOp(op='*', left=l, right=r): return eval_expr(l, env) * eval_expr(r, env)
        case _: raise ValueError(f"Unknown node: {node}")
```

Pattern matching is often cleaner for interpreters; visitor dispatch is better when passes need shared state.

---

## 📚 3. Symbol Tables & Scope

A **symbol table** maps **names** (identifiers) to their **declarations** (what kind of thing they are, and their type). A **scope** is a region of the program where a set of names are visible.

### Scope Stack

```python
@dataclass
class Symbol:
    name: str
    kind: str           # 'var', 'param', 'func', 'class'
    type_: Optional[str] = None
    is_defined: bool = False

class SymbolTable:
    """Single scope — link parent for nesting."""
    def __init__(self, name: str, parent: Optional['SymbolTable'] = None):
        self.name = name
        self.parent = parent
        self._symbols: dict[str, Symbol] = {}

    def define(self, sym: Symbol):
        if sym.name in self._symbols:
            raise NameError(f"Name {sym.name!r} already defined in scope {self.name!r}")
        self._symbols[sym.name] = sym

    def lookup(self, name: str) -> Symbol:
        """Search this scope, then parent chain."""
        if name in self._symbols:
            return self._symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        raise NameError(f"Name {name!r} is not defined")

    def lookup_local(self, name: str) -> Optional[Symbol]:
        """Only this scope — for 'already declared' checks."""
        return self._symbols.get(name)
```

### Scope Lifetime

Scopes are managed as a **stack** during the semantic pass:

```python
class ScopeManager:
    def __init__(self):
        self.current = SymbolTable("global")

    def enter_scope(self, name: str):
        self.current = SymbolTable(name, parent=self.current)

    def exit_scope(self):
        self.current = self.current.parent

    def define(self, sym: Symbol):
        self.current.define(sym)

    def lookup(self, name: str) -> Symbol:
        return self.current.lookup(name)
```

---

## 📚 4. Name Resolution Pass

Name resolution walks the AST and binds every `Name` node to its declaration in the symbol table. It also catches use-before-define errors.

```python
class NameResolver(ASTVisitor):
    def __init__(self):
        self.scopes = ScopeManager()
        self.errors: list[str] = []

    def visit_Module(self, node):
        # First pass: hoist function definitions
        for stmt in node.stmts:
            if isinstance(stmt, FuncDef):
                sym = Symbol(stmt.name, 'func')
                self.scopes.define(sym)
        # Second pass: resolve bodies
        for stmt in node.stmts:
            self.visit(stmt)

    def visit_FuncDef(self, node):
        self.scopes.enter_scope(f"func:{node.name}")
        for param in node.params:
            self.scopes.define(Symbol(param, 'param', is_defined=True))
        for stmt in node.body:
            self.visit(stmt)
        self.scopes.exit_scope()

    def visit_Assign(self, node):
        # RHS first (can't use LHS name in own initializer)
        self.visit(node.value)
        # Define LHS
        try:
            sym = Symbol(node.target.id, 'var', is_defined=True)
            self.scopes.define(sym)
            node.target.decl = sym
        except NameError as e:
            # Already defined — update
            sym = self.scopes.lookup(node.target.id)
            node.target.decl = sym

    def visit_Name(self, node):
        try:
            sym = self.scopes.lookup(node.id)
            node.decl = sym
        except NameError:
            self.errors.append(f"Undefined name: {node.id!r}")

    def visit_If(self, node):
        self.visit(node.test)
        self.scopes.enter_scope("if:then")
        for stmt in node.then_body: self.visit(stmt)
        self.scopes.exit_scope()
        if node.else_body:
            self.scopes.enter_scope("if:else")
            for stmt in node.else_body: self.visit(stmt)
            self.scopes.exit_scope()
```

---

## 📚 5. Using Python's Built-In `ast` Module

Python's compiler exposes its own AST through the `ast` module. This is one of the most powerful tools for AI code tooling:

```python
import ast

source = """
def add(x, y):
    return x + y

result = add(3, 4)
"""

tree = ast.parse(source)
print(ast.dump(tree, indent=2))
```

Output (simplified):
```
Module(
  body=[
    FunctionDef(
      name='add',
      args=arguments(args=[arg(arg='x'), arg(arg='y')]),
      body=[
        Return(
          value=BinOp(
            left=Name(id='x', ctx=Load()),
            op=Add(),
            right=Name(id='y', ctx=Load())))]),
    Assign(
      targets=[Name(id='result', ctx=Store())],
      value=Call(
        func=Name(id='add', ctx=Load()),
        args=[Constant(value=3), Constant(value=4)]))])
```

### Practical: Count All Function Calls in a File

```python
class CallCollector(ast.NodeVisitor):
    def __init__(self):
        self.calls: list[str] = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.calls.append(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.calls.append(f"{ast.unparse(node.func.value)}.{node.func.attr}")
        self.generic_visit(node)

collector = CallCollector()
collector.visit(tree)
print(collector.calls)   # ['add']
```

### Practical: AST Transformer — Replace All `print` with `logging.info`

```python
class PrintToLog(ast.NodeTransformer):
    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, ast.Name) and node.func.id == 'print':
            node.func = ast.Attribute(
                value=ast.Name(id='logging', ctx=ast.Load()),
                attr='info',
                ctx=ast.Load())
        return node

modified = PrintToLog().visit(tree)
ast.fix_missing_locations(modified)
print(ast.unparse(modified))
```

This is exactly the kind of AST-walking transformation that powers **Pylint**, **mypy**, **Black**, and **AI-based linters**.

---

## 📚 6. The Semantic Analysis Pipeline

A production compiler runs multiple passes over the AST, each checking a different property:

### Pass 1: Name Resolution
- Every `Name` node is linked to its declaration in the symbol table
- Errors: undefined name, redefinition of the same name in the same scope

### Pass 2: Type Checking
- Every expression node is annotated with its inferred type
- Errors: type mismatch (adding a string to an integer), wrong number of arguments
- See [15.4](15.4---Type-Systems-&-Type-Checking) for full detail

### Pass 3: Control-Flow Analysis
- **Definite assignment**: every variable is definitely assigned on every path before use
- **Return checking**: every function path that claims to return a value actually does

```python
def check_returns(func: FuncDef) -> bool:
    """Every path through function body returns a value."""
    def stmt_returns(stmt) -> bool:
        if isinstance(stmt, Return):
            return stmt.value is not None
        if isinstance(stmt, If):
            then_ret = any(stmt_returns(s) for s in stmt.then_body)
            else_ret = any(stmt_returns(s) for s in stmt.else_body) if stmt.else_body else False
            return then_ret and else_ret
        return False
    return any(stmt_returns(s) for s in func.body)
```

### Pass 4: Borrow Checking (Rust only)
- The Rust compiler's most famous pass
- Checks that no two mutable references coexist
- Implemented as a constraint-solving pass over the annotated AST / MIR (Mid-level IR)
- See [15.5](15.5---Intermediate-Representations-&-IR-Design) for more on MIR

---

## 📚 7. Worked Example — Full Pipeline

Let us trace `def add(x, y): return x + y` through the front-end pipeline:

**Step 1 — Tokens (from Lexer):**
```
DEF "def" | IDENT "add" | LPAREN | IDENT "x" | COMMA | IDENT "y" | RPAREN | COLON | RETURN "return" | IDENT "x" | PLUS | IDENT "y" | EOF
```

**Step 2 — AST (from Parser):**
```python
FuncDef(
    name='add',
    params=['x', 'y'],
    body=[
        Return(value=BinOp('+', Name('x'), Name('y')))
    ]
)
```

**Step 3 — After Name Resolution:**
```python
FuncDef(
    name='add',   # sym: Symbol('add', 'func') in global scope
    params=['x', 'y'],
    body=[
        Return(value=BinOp('+',
            Name('x', decl=Symbol('x', 'param')),   # ← linked!
            Name('y', decl=Symbol('y', 'param'))    # ← linked!
        ))
    ]
)
```

**Step 4 — After Type Checking (with annotation):**
```python
BinOp('+',
    Name('x', type_=int),   # inferred from context or annotation
    Name('y', type_=int),
    type_=int               # result type
)
```

**Step 5 — Annotated AST feeds IR generation** → see [15.5](15.5---Intermediate-Representations-&-IR-Design)

---

## 🔗 8. Cross-links & Further Reading

### Internal
- [15.2 - Parsers & Grammars](15.2---Parsers-&-Grammars) — how the AST is built
- [15.4 - Type Systems & Type Checking](15.4---Type-Systems-&-Type-Checking) — next pass on the AST
- [15.5 - Intermediate Representations & IR Design](15.5---Intermediate-Representations-&-IR-Design) — what the AST is lowered to
- [1.4 - Concurrency - asyncio, threading, multiprocessing & the GIL](1.4---Concurrency---asyncio,-threading,-multiprocessing-&-the-GIL) — Python internals

### External
- [Python ast module docs](https://docs.python.org/3/library/ast.html)
- [Green Tree Snakes — The Missing Python AST docs](https://greentreesnakes.com/)
- [astexplorer.net](https://astexplorer.net/) — interactive AST explorer (JS/TS/Python/Go/Rust/CSS)
- [Crafting Interpreters — Ch. 5 (Representing Code)](https://craftinginterpreters.com/representing-code.html)
- [Crafting Interpreters — Ch. 11 (Resolving and Binding)](https://craftinginterpreters.com/resolving-and-binding.html)

---

## ⚠️ 9. Common Misconceptions

- **"The AST is the same as the parse tree."** The parse tree faithfully mirrors the grammar, including all syntactic markers. The AST removes them, keeping only the semantic structure. Parentheses disappear; their effect is captured by nesting.
- **"Name resolution and type checking are the same pass."** In simple interpreters they can be merged, but production compilers separate them because they have different error classes and need different data.
- **"Python's `ast` module gives me the same AST my code builds."** Not exactly — Python's AST nodes differ from the AST you design for your own language. But using `ast` is the fastest way to get AST intuition for Python programs.
- **"Visitor pattern requires a base `accept` method."** In Python, dispatch by class name (`f'visit_{type(node).__name__}'`) achieves double dispatch without modifying the node classes. The classic Gang-of-Four visitor requires `accept`, but the Python idiom is cleaner.

---

*Next: [15.4 - Type Systems & Type Checking](15.4---Type-Systems-&-Type-Checking) — Adding the type layer to the AST.*
