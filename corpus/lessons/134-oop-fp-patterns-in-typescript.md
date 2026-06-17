---
title: "13.4 — OOP & FP Patterns in TypeScript"
subject: "TypeScript"
catalog: advanced
audience_tier: higher-education
chapter: "13.4"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 13.4 — OOP & FP Patterns in TypeScript

> *"TypeScript is uniquely positioned — it has classes for when you need them, but its type system is powerful enough to make functional patterns first-class citizens."* — **Daniel Rosenwasser**, TypeScript Program Manager

TypeScript doesn't force you into one paradigm. You get Java-style classes with access modifiers AND Haskell-style algebraic data types via discriminated unions. The best TypeScript code uses **both** — classes for stateful services, functional patterns for data transformation. This chapter teaches you when to reach for each.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Write TypeScript classes with proper access modifiers, abstract classes, and `implements`.
2. Use discriminated unions as TypeScript's algebraic data types (ADTs).
3. Implement functional patterns: pipe, compose, Option/Result monads.
4. Apply the Strategy, Observer, and Repository patterns with full type safety.
5. Understand Effect.ts fundamentals for advanced functional error handling.
6. Choose between classes, functions, and objects for different architectural needs.
7. Compare Python OOP patterns with TypeScript equivalents.

---

## 🖼️ Visual Anchor — OOP vs FP Decision Tree

![ts__6.4-fig1](ts__6.4-fig1.svg)

---

## 📚 1. Concepts & Definitions

### Definition 13.4.1 — Classes in TypeScript

TypeScript classes add **access modifiers**, **abstract classes**, and **parameter properties** to JavaScript classes:

```ts
abstract class Shape {
  // Abstract: must be implemented by subclasses
  abstract area(): number;
  abstract perimeter(): number;

  // Concrete method shared by all shapes
  describe(): string {
    return `${this.constructor.name}: area=${this.area().toFixed(2)}`;
  }
}

class Circle extends Shape {
  // Parameter property: declares AND assigns in constructor
  constructor(private readonly radius: number) {
    super();
  }

  area(): number {
    return Math.PI * this.radius ** 2;
  }

  perimeter(): number {
    return 2 * Math.PI * this.radius;
  }
}

class Rectangle extends Shape {
  constructor(
    private readonly width: number,
    private readonly height: number
  ) {
    super();
  }

  area(): number { return this.width * this.height; }
  perimeter(): number { return 2 * (this.width + this.height); }
}
```

### Definition 13.4.2 — Access Modifiers

| Modifier | Access | Python Equivalent |
|----------|--------|-------------------|
| `public` (default) | Anywhere | No prefix |
| `private` | Only within the class | `__name` (name mangling) |
| `protected` | Class + subclasses | `_name` (convention) |
| `readonly` | Set once (constructor only) | No direct equivalent |

```ts
class BankAccount {
  private balance: number = 0;           // Only this class can access
  protected readonly accountId: string;  // Subclasses can read, nobody can write
  public owner: string;                  // Anyone can access

  constructor(owner: string, accountId: string) {
    this.owner = owner;
    this.accountId = accountId;
  }

  // Private method — internal implementation detail
  private validateAmount(amount: number): void {
    if (amount <= 0) throw new Error("Amount must be positive");
  }

  deposit(amount: number): void {
    this.validateAmount(amount);
    this.balance += amount;
  }

  getBalance(): number {
    return this.balance;
  }
}
```

### Definition 13.4.3 — Interfaces as Contracts (`implements`)

```ts
// Interface defines the contract
interface Serializable {
  serialize(): string;
  deserialize(data: string): void;
}

interface Cacheable {
  cacheKey(): string;
  ttl(): number; // seconds
}

// Class implements multiple interfaces
class UserProfile implements Serializable, Cacheable {
  constructor(
    public readonly id: string,
    public name: string,
    public email: string
  ) {}

  serialize(): string {
    return JSON.stringify({ id: this.id, name: this.name, email: this.email });
  }

  deserialize(data: string): void {
    const parsed = JSON.parse(data);
    this.name = parsed.name;
    this.email = parsed.email;
  }

  cacheKey(): string {
    return `user:${this.id}`;
  }

  ttl(): number {
    return 3600; // 1 hour
  }
}
```

**Python comparison:** `implements` in TS ≈ inheriting from a `Protocol` or `ABC` in Python. But TS checks it at compile time with zero runtime cost.

### Definition 13.4.4 — Discriminated Unions (Algebraic Data Types)

The **most important pattern in TypeScript**. Instead of class hierarchies, model variants as a union with a discriminant field:

```ts
// Instead of class hierarchy:
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number }
  | { kind: "rectangle"; width: number; height: number };

// Pattern match with switch
function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle": return Math.PI * shape.radius ** 2;
    case "square": return shape.side ** 2;
    case "rectangle": return shape.width * shape.height;
  }
}

// Adding a new variant? The compiler tells you everywhere you need to handle it.
// This is BETTER than class inheritance for most data modeling.
```

### Definition 13.4.5 — The Option/Maybe Pattern

Represent "might not exist" explicitly instead of using `null`:

```ts
type Option<T> = { _tag: "Some"; value: T } | { _tag: "None" };

const Some = <T>(value: T): Option<T> => ({ _tag: "Some", value });
const None: Option<never> = { _tag: "None" };

function map<T, U>(opt: Option<T>, fn: (value: T) => U): Option<U> {
  return opt._tag === "Some" ? Some(fn(opt.value)) : None;
}

function flatMap<T, U>(opt: Option<T>, fn: (value: T) => Option<U>): Option<U> {
  return opt._tag === "Some" ? fn(opt.value) : None;
}

function getOrElse<T>(opt: Option<T>, defaultValue: T): T {
  return opt._tag === "Some" ? opt.value : defaultValue;
}

// Usage:
function findUser(id: string): Option<User> {
  const user = db.get(id);
  return user ? Some(user) : None;
}

const userName = getOrElse(
  map(findUser("123"), u => u.name),
  "Unknown"
);
```

---

## 🧩 2. Mental Models

### Model 6.4.1 — When to Use Classes vs Functions vs Objects

| Use Case | Pattern | Why |
|----------|---------|-----|
| Stateful service (DB connection, cache) | Class | Encapsulates mutable state + lifecycle |
| Data transformation pipeline | Functions + pipe | Composable, testable, no hidden state |
| Configuration / constants | Plain object + `as const` | Simple, no overhead |
| Multiple variants of a concept | Discriminated union | Exhaustive checking, no inheritance |
| Dependency injection | Interface + class | Testable, swappable implementations |
| Event handling | Class (EventEmitter) | Manages listener lifecycle |

### Model 6.4.2 — Composition Over Inheritance (TS Edition)

```ts
// ❌ Inheritance hierarchy (fragile, rigid)
class Animal { move() {} }
class Dog extends Animal { bark() {} }
class SwimmingDog extends Dog { swim() {} }
class FlyingDog extends Dog { fly() {} } // ???
class SwimmingFlyingDog extends ??? {} // Diamond problem!

// ✅ Composition with interfaces
interface Movable { move(): void }
interface Swimmer { swim(): void }
interface Flyer { fly(): void }
interface Barker { bark(): void }

// Compose behaviors
type Dog = Movable & Barker;
type AquaDog = Dog & Swimmer;
type SuperDog = Dog & Swimmer & Flyer;

// Implementation via factory functions (no class needed)
function createDog(name: string): Dog {
  return {
    move() { console.log(`${name} runs`) },
    bark() { console.log(`${name} barks`) },
  };
}
```

### Model 6.4.3 — Python ↔ TypeScript OOP Comparison

| Python | TypeScript | Notes |
|--------|-----------|-------|
| `class Foo:` | `class Foo {}` | Same concept |
| `@dataclass` | `class` with parameter properties | TS has no built-in dataclass |
| `Protocol` | `interface` | Structural typing in both |
| `ABC` + `@abstractmethod` | `abstract class` | Nominal in both |
| `__init__` | `constructor` | Same role |
| `_private` (convention) | `private` (enforced) | TS enforces at compile time |
| `@property` | `get`/`set` accessors | Same concept |
| Multiple inheritance | `implements` multiple interfaces | TS avoids diamond problem |
| `match/case` (3.10+) | `switch` on discriminant | TS has exhaustive checking |

---

## 🔑 3. Mechanics

### 3.1 — Functional Composition: `pipe` and `compose`

```ts
// pipe: left-to-right composition (most readable)
function pipe<A, B>(a: A, ab: (a: A) => B): B;
function pipe<A, B, C>(a: A, ab: (a: A) => B, bc: (b: B) => C): C;
function pipe<A, B, C, D>(a: A, ab: (a: A) => B, bc: (b: B) => C, cd: (c: C) => D): D;
function pipe(initial: unknown, ...fns: Function[]): unknown {
  return fns.reduce((acc, fn) => fn(acc), initial);
}

// Usage:
const result = pipe(
  " Hello, World! ",
  (s: string) => s.trim(),
  (s: string) => s.toLowerCase(),
  (s: string) => s.replace(/\s+/g, "-"),
);
// "hello,-world!"

// Real-world: data transformation pipeline
interface RawOrder {
  items: { sku: string; qty: number; price_cents: number }[];
  customer_email: string;
  shipping_address: string;
}

const processOrder = (raw: RawOrder) => pipe(
  raw,
  validateOrder,
  calculateTotals,
  applyDiscounts,
  formatForPayment,
);
```

### 3.2 — The Result Monad (Functional Error Handling)

```ts
type Result<T, E = Error> =
  | { _tag: "Ok"; value: T }
  | { _tag: "Err"; error: E };

const Ok = <T>(value: T): Result<T, never> => ({ _tag: "Ok", value });
const Err = <E>(error: E): Result<never, E> => ({ _tag: "Err", error });

// Functor: transform the success value
function mapResult<T, U, E>(result: Result<T, E>, fn: (t: T) => U): Result<U, E> {
  return result._tag === "Ok" ? Ok(fn(result.value)) : result;
}

// Monad: chain operations that might fail
function flatMapResult<T, U, E>(result: Result<T, E>, fn: (t: T) => Result<U, E>): Result<U, E> {
  return result._tag === "Ok" ? fn(result.value) : result;
}

// Usage: composable error handling without try/catch
function parseJSON(input: string): Result<unknown, Error> {
  try { return Ok(JSON.parse(input)); }
  catch (e) { return Err(e instanceof Error ? e : new Error(String(e))); }
}

function validateAge(data: unknown): Result<number, Error> {
  if (typeof data !== "object" || data === null || !("age" in data)) {
    return Err(new Error("Missing age field"));
  }
  const age = (data as any).age;
  if (typeof age !== "number" || age < 0 || age > 150) {
    return Err(new Error("Invalid age"));
  }
  return Ok(age);
}

// Chain them:
const age = flatMapResult(parseJSON('{"age": 35}'), validateAge);
// Result<number, Error> — either Ok(35) or Err(...)
```

### 3.3 — Effect.ts Introduction

Effect.ts is a library for building robust, composable TypeScript applications with typed errors, dependency injection, and concurrency:

```ts
import { Effect, pipe } from "effect";

// Effect<Success, Error, Requirements>
// An effect that produces a string, might fail with Error, needs no dependencies
const program: Effect.Effect<string, Error, never> = pipe(
  Effect.tryPromise({
    try: () => fetch("https://api.example.com/user"),
    catch: (e) => new Error(`Fetch failed: ${e}`),
  }),
  Effect.flatMap((response) =>
    Effect.tryPromise({
      try: () => response.json() as Promise<{ name: string }>,
      catch: () => new Error("JSON parse failed"),
    })
  ),
  Effect.map((data) => data.name),
);

// Run the effect
Effect.runPromise(program).then(console.log).catch(console.error);
```

Key Effect.ts concepts:
- **Typed errors:** The error channel is part of the type signature
- **Dependency injection:** Requirements are tracked in the type
- **Composability:** Effects compose like Promises but with more safety
- **Concurrency:** Built-in fiber-based concurrency

### 3.4 — Design Patterns in TypeScript

```ts
// Strategy Pattern — swap algorithms at runtime
interface SortStrategy<T> {
  sort(items: T[]): T[];
}

class QuickSort<T> implements SortStrategy<T> {
  sort(items: T[]): T[] { /* ... */ return items; }
}

class MergeSort<T> implements SortStrategy<T> {
  sort(items: T[]): T[] { /* ... */ return items; }
}

class Sorter<T> {
  constructor(private strategy: SortStrategy<T>) {}

  setStrategy(strategy: SortStrategy<T>): void {
    this.strategy = strategy;
  }

  sort(items: T[]): T[] {
    return this.strategy.sort(items);
  }
}

// Repository Pattern — abstract data access
interface Repository<T extends { id: string }> {
  findById(id: string): Promise<T | null>;
  findAll(filter?: Partial<T>): Promise<T[]>;
  create(item: Omit<T, "id">): Promise<T>;
  update(id: string, patch: Partial<Omit<T, "id">>): Promise<T>;
  delete(id: string): Promise<void>;
}

// Concrete implementation
class PostgresUserRepo implements Repository<User> {
  constructor(private db: DatabaseClient) {}

  async findById(id: string): Promise<User | null> {
    return this.db.query("SELECT * FROM users WHERE id = $1", [id]);
  }
  // ... other methods
}

// In tests, swap with in-memory implementation
class InMemoryUserRepo implements Repository<User> {
  private store = new Map<string, User>();
  // ... implement with Map operations
}
```


---

## 💻 4. Code Patterns & Examples

### Pattern 6.4.1 — Discriminated Union State Machine

```ts
// Model a finite state machine with types
type ConnectionState =
  | { status: "disconnected" }
  | { status: "connecting"; attempt: number }
  | { status: "connected"; socket: WebSocket; connectedAt: Date }
  | { status: "error"; error: Error; lastAttempt: Date };

type ConnectionEvent =
  | { type: "CONNECT" }
  | { type: "CONNECTED"; socket: WebSocket }
  | { type: "DISCONNECT" }
  | { type: "ERROR"; error: Error };

function transition(state: ConnectionState, event: ConnectionEvent): ConnectionState {
  switch (state.status) {
    case "disconnected":
      if (event.type === "CONNECT") {
        return { status: "connecting", attempt: 1 };
      }
      return state;

    case "connecting":
      if (event.type === "CONNECTED") {
        return { status: "connected", socket: event.socket, connectedAt: new Date() };
      }
      if (event.type === "ERROR") {
        return { status: "error", error: event.error, lastAttempt: new Date() };
      }
      return state;

    case "connected":
      if (event.type === "DISCONNECT") {
        state.socket.close();
        return { status: "disconnected" };
      }
      if (event.type === "ERROR") {
        return { status: "error", error: event.error, lastAttempt: new Date() };
      }
      return state;

    case "error":
      if (event.type === "CONNECT") {
        return { status: "connecting", attempt: 1 };
      }
      return state;
  }
}
```

### Pattern 6.4.2 — Dependency Injection with Interfaces

```ts
// Define service interfaces
interface Logger {
  info(msg: string): void;
  error(msg: string, err?: Error): void;
}

interface UserRepository {
  findById(id: string): Promise<User | null>;
  save(user: User): Promise<void>;
}

interface EmailService {
  send(to: string, subject: string, body: string): Promise<void>;
}

// Service that depends on abstractions, not implementations
class UserService {
  constructor(
    private readonly users: UserRepository,
    private readonly email: EmailService,
    private readonly logger: Logger,
  ) {}

  async registerUser(name: string, email: string): Promise<User> {
    this.logger.info(`Registering user: ${email}`);

    const user: User = {
      id: crypto.randomUUID(),
      name,
      email,
      role: "user",
    };

    await this.users.save(user);
    await this.email.send(email, "Welcome!", `Hi ${name}, welcome aboard!`);

    return user;
  }
}

// In production: real implementations
// In tests: mock implementations (easy to swap because of interfaces)
```

---

## 🧮 5. Worked Examples

### Example 13.4.1 — Build a Type-Safe Event System with Discriminated Unions

**Task:** Create an event system where each event type has a specific payload, and handlers are type-safe.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```ts
// Step 1: Define events as a discriminated union
type AppEvent =
  | { type: "USER_LOGIN"; payload: { userId: string; timestamp: number } }
  | { type: "USER_LOGOUT"; payload: { userId: string } }
  | { type: "ITEM_ADDED"; payload: { itemId: string; quantity: number } }
  | { type: "ORDER_PLACED"; payload: { orderId: string; total: number } };

// Step 2: Extract event types and payloads
type EventType = AppEvent["type"];
type EventPayload<T extends EventType> = Extract<AppEvent, { type: T }>["payload"];

// Step 3: Type-safe event bus
class EventBus {
  private handlers = new Map<string, Set<Function>>();

  on<T extends EventType>(
    type: T,
    handler: (payload: EventPayload<T>) => void
  ): () => void {
    if (!this.handlers.has(type)) {
      this.handlers.set(type, new Set());
    }
    this.handlers.get(type)!.add(handler);

    // Return unsubscribe function
    return () => { this.handlers.get(type)?.delete(handler); };
  }

  emit<T extends EventType>(type: T, payload: EventPayload<T>): void {
    this.handlers.get(type)?.forEach(handler => handler(payload));
  }
}

// Usage:
const bus = new EventBus();

bus.on("USER_LOGIN", (payload) => {
  // payload is { userId: string; timestamp: number } — fully typed!
  console.log(`User ${payload.userId} logged in`);
});

bus.emit("USER_LOGIN", { userId: "123", timestamp: Date.now() }); // ✅
// bus.emit("USER_LOGIN", { userId: 123 }); // ❌ number not assignable to string
```

</details>

### Example 13.4.2 — Implement a Functional Pipeline with Error Handling

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```ts
// Result type with chainable methods
class ResultWrapper<T, E> {
  private constructor(private readonly inner: Result<T, E>) {}

  static ok<T>(value: T): ResultWrapper<T, never> {
    return new ResultWrapper({ _tag: "Ok", value });
  }

  static err<E>(error: E): ResultWrapper<never, E> {
    return new ResultWrapper({ _tag: "Err", error });
  }

  map<U>(fn: (value: T) => U): ResultWrapper<U, E> {
    if (this.inner._tag === "Ok") {
      return ResultWrapper.ok(fn(this.inner.value));
    }
    return this as unknown as ResultWrapper<U, E>;
  }

  flatMap<U, E2>(fn: (value: T) => ResultWrapper<U, E2>): ResultWrapper<U, E | E2> {
    if (this.inner._tag === "Ok") {
      return fn(this.inner.value) as ResultWrapper<U, E | E2>;
    }
    return this as unknown as ResultWrapper<U, E | E2>;
  }

  getOrElse(defaultValue: T): T {
    return this.inner._tag === "Ok" ? this.inner.value : defaultValue;
  }

  match<U>(handlers: { ok: (value: T) => U; err: (error: E) => U }): U {
    return this.inner._tag === "Ok"
      ? handlers.ok(this.inner.value)
      : handlers.err(this.inner.error);
  }
}

// Usage: composable validation pipeline
type ValidationError = { field: string; message: string };

function validateName(input: string): ResultWrapper<string, ValidationError> {
  if (input.length < 2) return ResultWrapper.err({ field: "name", message: "Too short" });
  if (input.length > 50) return ResultWrapper.err({ field: "name", message: "Too long" });
  return ResultWrapper.ok(input.trim());
}

function validateEmail(input: string): ResultWrapper<string, ValidationError> {
  if (!input.includes("@")) return ResultWrapper.err({ field: "email", message: "Invalid" });
  return ResultWrapper.ok(input.toLowerCase().trim());
}

const name = validateName("Bill")
  .map(n => n.toUpperCase())
  .match({
    ok: (n) => `Valid: ${n}`,
    err: (e) => `Error in ${e.field}: ${e.message}`,
  });
```

</details>

### Example 13.4.3 — Convert a Python Class to TypeScript

**Task:** Translate this Python class to idiomatic TypeScript.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

Python original:
```python
from dataclasses import dataclass, field
from typing import Protocol

class Drawable(Protocol):
    def draw(self, surface: "Surface") -> None: ...
    def bounds(self) -> tuple[int, int, int, int]: ...

@dataclass
class Sprite:
    x: float
    y: float
    width: float
    height: float
    _texture: str = field(repr=False)

    def draw(self, surface: "Surface") -> None:
        surface.blit(self._texture, (self.x, self.y))

    def bounds(self) -> tuple[int, int, int, int]:
        return (int(self.x), int(self.y), int(self.width), int(self.height))

    def move(self, dx: float, dy: float) -> "Sprite":
        return Sprite(self.x + dx, self.y + dy, self.width, self.height, self._texture)
```

TypeScript equivalent:
```ts
// Protocol → interface (structural typing)
interface Drawable {
  draw(surface: Surface): void;
  bounds(): [number, number, number, number];
}

// @dataclass → class with parameter properties
class Sprite implements Drawable {
  constructor(
    public readonly x: number,
    public readonly y: number,
    public readonly width: number,
    public readonly height: number,
    private readonly texture: string,
  ) {}

  draw(surface: Surface): void {
    surface.blit(this.texture, [this.x, this.y]);
  }

  bounds(): [number, number, number, number] {
    return [Math.floor(this.x), Math.floor(this.y),
            Math.floor(this.width), Math.floor(this.height)];
  }

  // Immutable update (like dataclasses.replace)
  move(dx: number, dy: number): Sprite {
    return new Sprite(this.x + dx, this.y + dy, this.width, this.height, this.texture);
  }

  // toString equivalent of __repr__
  toString(): string {
    return `Sprite(${this.x}, ${this.y}, ${this.width}×${this.height})`;
  }
}
```

Key differences:
- Python `Protocol` → TS `interface` (both structural)
- Python `@dataclass(frozen=True)` → TS `readonly` properties + return new instance
- Python `field(repr=False)` → TS `private` (excluded from external access)
- Python tuple return → TS tuple type `[number, number, number, number]`

</details>

---

## ⚠️ 6. Gotchas & Anti-Patterns

### Gotcha 6.4.1 — Class `private` vs `#private`

```ts
class Example {
  private tsPrivate = "visible at runtime";  // TypeScript-only (erased)
  #jsPrivate = "truly private";              // JavaScript private field (runtime enforced)
}

const e = new Example();
// e.tsPrivate;  // TS error, but (e as any).tsPrivate works at runtime!
// e.#jsPrivate; // Both TS error AND runtime error — truly private

// Recommendation: Use #private for security-sensitive fields,
// private for everything else (better debugging, same safety in typed code)
```

### Gotcha 6.4.2 — `this` in Class Methods

```ts
class Timer {
  private count = 0;

  // ❌ Loses `this` when passed as callback
  increment() {
    this.count++; // `this` might be undefined!
  }

  // ✅ Arrow function preserves `this`
  incrementSafe = () => {
    this.count++;
  };

  // ✅ Or bind in constructor
  constructor() {
    this.increment = this.increment.bind(this);
  }
}

const timer = new Timer();
setTimeout(timer.increment, 100);     // ❌ `this` is undefined
setTimeout(timer.incrementSafe, 100); // ✅ works
```

### Gotcha 6.4.3 — Overusing Classes (Java Brain)

```ts
// ❌ Java-style: class for everything
class StringUtils {
  static capitalize(s: string): string {
    return s.charAt(0).toUpperCase() + s.slice(1);
  }
  static trim(s: string): string {
    return s.trim();
  }
}
StringUtils.capitalize("hello");

// ✅ TypeScript-style: just use functions
export function capitalize(s: string): string {
  return s.charAt(0).toUpperCase() + s.slice(1);
}
// import { capitalize } from "./string-utils";
// capitalize("hello");

// Classes are for STATE. If there's no state, use functions.
```

### Gotcha 6.4.4 — Inheritance Depth

```ts
// ❌ Deep inheritance (fragile, hard to understand)
class Entity { }
class LivingEntity extends Entity { }
class Character extends LivingEntity { }
class Player extends Character { }
class AdminPlayer extends Player { }

// ✅ Flat composition
interface Entity { id: string; position: Vector2 }
interface Living { health: number; damage(amount: number): void }
interface Controllable { handleInput(input: Input): void }
interface Admin { permissions: Set<string> }

type Player = Entity & Living & Controllable;
type AdminPlayer = Player & Admin;
```

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- **Previous:** [13.3 - Advanced Types - Conditional, Mapped, Template Literal Types](13.3---Advanced-Types---Conditional,-Mapped,-Template-Literal-Types)
- **Next:** [13.5 - Async, Promises & Async Generators](13.5---Async,-Promises-&-Async-Generators)
- **Python OOP:** [08.3 - OOP, Data Models & Pythonic Idioms](08.3---OOP,-Data-Models-&-Pythonic-Idioms) — direct comparison
- **React patterns:** [13.7 - Frontend with TypeScript - React, Vue, Svelte, SolidJS](13.7---Frontend-with-TypeScript---React,-Vue,-Svelte,-SolidJS)

### External Resources
- [TypeScript Handbook — Classes](https://www.typescriptlang.org/docs/handbook/2/classes.html)
- [Effect.ts Documentation](https://effect.website/docs/introduction)
- [Total TypeScript — Discriminated Unions](https://www.totaltypescript.com/discriminated-unions-are-a-devs-best-friend)
- [Patterns.dev — Design Patterns in TypeScript](https://www.patterns.dev/)
- [fp-ts](https://gcanti.github.io/fp-ts/) — Functional programming library (predecessor to Effect)

---

*Last updated: 2026-05-24*



---

## 🏗️ 8. Effect.ts, fp-ts & Production Functional Patterns

### 8.1 — Effect.ts: The Modern FP Framework for TypeScript

Effect is a comprehensive framework for building type-safe, composable applications. It provides structured concurrency, dependency injection, error handling, and resource management — all with full type inference.

#### Core Concept: The Effect Type

```ts
import { Effect, pipe } from "effect";

// Effect<Success, Error, Requirements>
// - Success: what the effect produces on success
// - Error: what errors it can fail with (typed!)
// - Requirements: what services/dependencies it needs

// A simple effect that can fail with a string error
const divide = (a: number, b: number): Effect.Effect<number, string> =>
  b === 0
    ? Effect.fail("Division by zero")
    : Effect.succeed(a / b);

// Composing effects with pipe
const program = pipe(
  divide(10, 2),
  Effect.map(result => result * 2),
  Effect.flatMap(doubled => divide(doubled, 3)),
  Effect.catchAll(error => Effect.succeed(-1)), // Handle all errors
);

// Running the effect
Effect.runPromise(program).then(console.log); // 3.333...
```

#### Typed Errors: Know Exactly What Can Fail

```ts
import { Effect, Data } from "effect";

// Define error types as tagged classes
class NetworkError extends Data.TaggedError("NetworkError")<{
  url: string;
  status: number;
}> {}

class ParseError extends Data.TaggedError("ParseError")<{
  message: string;
  input: string;
}> {}

class ValidationError extends Data.TaggedError("ValidationError")<{
  field: string;
  reason: string;
}> {}

// Functions declare their error types
const fetchUser = (id: string): Effect.Effect<User, NetworkError> =>
  Effect.tryPromise({
    try: () => fetch(`/api/users/${id}`).then(r => {
      if (!r.ok) throw { url: `/api/users/${id}`, status: r.status };
      return r.json();
    }),
    catch: (e) => new NetworkError(e as any),
  });

const parseUser = (data: unknown): Effect.Effect<User, ParseError> =>
  Effect.try({
    try: () => userSchema.parse(data),
    catch: (e) => new ParseError({ message: String(e), input: JSON.stringify(data) }),
  });

// Composed effect has UNION of all possible errors
const getUser = (id: string) => pipe(
  fetchUser(id),
  Effect.flatMap(parseUser),
);
// Type: Effect<User, NetworkError | ParseError>

// Handle specific errors
const safeGetUser = pipe(
  getUser("123"),
  Effect.catchTag("NetworkError", (e) =>
    Effect.succeed({ id: "offline", name: "Offline User" } as User)
  ),
  // Remaining error type: ParseError (NetworkError was handled)
);
```

#### Dependency Injection with Layers

```ts
import { Effect, Context, Layer } from "effect";

// Define service interfaces
class Database extends Context.Tag("Database")<
  Database,
  {
    query: (sql: string) => Effect.Effect<unknown[], Error>;
    execute: (sql: string) => Effect.Effect<void, Error>;
  }
>() {}

class Logger extends Context.Tag("Logger")<
  Logger,
  {
    info: (msg: string) => Effect.Effect<void>;
    error: (msg: string) => Effect.Effect<void>;
  }
>() {}

// Use services in your program
const getAllUsers = Effect.gen(function* () {
  const db = yield* Database;
  const logger = yield* Logger;

  yield* logger.info("Fetching all users");
  const rows = yield* db.query("SELECT * FROM users");
  yield* logger.info(`Found ${rows.length} users`);

  return rows as User[];
});
// Type: Effect<User[], Error, Database | Logger>
// The third type parameter tracks ALL required dependencies!

// Provide implementations via Layers
const DatabaseLive = Layer.succeed(Database, {
  query: (sql) => Effect.tryPromise(() => pool.query(sql).then(r => r.rows)),
  execute: (sql) => Effect.tryPromise(() => pool.query(sql).then(() => {})),
});

const LoggerLive = Layer.succeed(Logger, {
  info: (msg) => Effect.sync(() => console.log(`[INFO] ${msg}`)),
  error: (msg) => Effect.sync(() => console.error(`[ERROR] ${msg}`)),
});

// Compose layers and run
const AppLayer = Layer.merge(DatabaseLive, LoggerLive);

Effect.runPromise(
  getAllUsers.pipe(Effect.provide(AppLayer))
);
```

### 8.2 — fp-ts vs Effect Comparison

| Feature | fp-ts | Effect |
|---------|-------|--------|
| Error typing | `Either<E, A>` | `Effect<A, E, R>` |
| Dependency injection | `Reader<R, A>` | Built-in (third type param) |
| Async | `TaskEither<E, A>` | Built-in (all effects are async-capable) |
| Resource management | Manual | `Effect.acquireRelease` |
| Concurrency | Limited | Full structured concurrency |
| Bundle size | Tree-shakeable | Larger but comprehensive |
| Learning curve | Steep (Haskell-like) | Moderate (generator syntax) |
| Ecosystem | Mature, stable | Growing rapidly |
| Maintenance | Maintenance mode | Actively developed |

#### fp-ts Style (pipe-heavy, Haskell-inspired)

```ts
import { pipe } from "fp-ts/function";
import * as TE from "fp-ts/TaskEither";
import * as E from "fp-ts/Either";
import * as A from "fp-ts/Array";

const fetchUsers: TE.TaskEither<Error, User[]> = pipe(
  TE.tryCatch(
    () => fetch("/api/users").then(r => r.json()),
    (e) => new Error(String(e))
  ),
  TE.map((data: unknown[]) => data as User[]),
  TE.chain((users) =>
    pipe(
      users,
      A.filter(u => u.age > 18),
      (filtered) => TE.right(filtered)
    )
  )
);
```

#### Effect Style (generator syntax, more ergonomic)

```ts
import { Effect } from "effect";

const fetchUsers = Effect.gen(function* () {
  const response = yield* Effect.tryPromise(() => fetch("/api/users"));
  const data = yield* Effect.tryPromise(() => response.json());
  const users = data as User[];
  return users.filter(u => u.age > 18);
});
```

### 8.3 — Result/Either Monads: Production Patterns

```ts
// Lightweight Result type (no framework dependency)
type Result<T, E = Error> =
  | { readonly _tag: "Ok"; readonly value: T }
  | { readonly _tag: "Err"; readonly error: E };

const Ok = <T>(value: T): Result<T, never> => ({ _tag: "Ok", value });
const Err = <E>(error: E): Result<never, E> => ({ _tag: "Err", error });

// Functor: map over the success value
function map<T, U, E>(result: Result<T, E>, f: (value: T) => U): Result<U, E> {
  return result._tag === "Ok" ? Ok(f(result.value)) : result;
}

// Monad: chain/flatMap (sequence dependent operations)
function flatMap<T, U, E, F>(
  result: Result<T, E>,
  f: (value: T) => Result<U, F>
): Result<U, E | F> {
  return result._tag === "Ok" ? f(result.value) : result;
}

// Applicative: combine multiple Results
function zip<A, B, E>(
  a: Result<A, E>,
  b: Result<B, E>
): Result<[A, B], E> {
  if (a._tag === "Err") return a;
  if (b._tag === "Err") return b;
  return Ok([a.value, b.value]);
}

// Collect all errors (not just first)
function zipAll<T, E>(results: Result<T, E>[]): Result<T[], E[]> {
  const errors: E[] = [];
  const values: T[] = [];

  for (const r of results) {
    if (r._tag === "Err") errors.push(r.error);
    else values.push(r.value);
  }

  return errors.length > 0 ? Err(errors) : Ok(values);
}
```

### 8.4 — Pipe and Flow Operators

```ts
// pipe: apply functions left-to-right to a value
function pipe<A>(a: A): A;
function pipe<A, B>(a: A, ab: (a: A) => B): B;
function pipe<A, B, C>(a: A, ab: (a: A) => B, bc: (b: B) => C): C;
function pipe<A, B, C, D>(a: A, ab: (a: A) => B, bc: (b: B) => C, cd: (c: C) => D): D;
function pipe(a: unknown, ...fns: Function[]): unknown {
  return fns.reduce((acc, fn) => fn(acc), a);
}

// flow: compose functions into a new function (point-free)
function flow<A, B>(ab: (a: A) => B): (a: A) => B;
function flow<A, B, C>(ab: (a: A) => B, bc: (b: B) => C): (a: A) => C;
function flow<A, B, C, D>(ab: (a: A) => B, bc: (b: B) => C, cd: (c: C) => D): (a: A) => D;
function flow(...fns: Function[]): Function {
  return (a: unknown) => fns.reduce((acc, fn) => fn(acc), a);
}

// Usage:
const processUser = flow(
  (id: string) => fetchUser(id),
  (user) => validateUser(user),
  (validUser) => enrichWithPermissions(validUser),
  (enriched) => serializeForAPI(enriched),
);

// TC39 Pipeline Operator (Stage 2) — future syntax:
// const result = userId |> fetchUser(%) |> validateUser(%) |> serialize(%);
```

---

## 📎 9. Appendix — Deep Dives & Theory

### Appendix A — Lawful Functor, Monad & Applicative

In category theory, these abstractions have **laws** that implementations must satisfy. Violating these laws leads to subtle bugs in composed code.

#### Functor Laws

A Functor provides `map: (fa: F<A>, f: A => B) => F<B>` and must satisfy:

```ts
// Law 1: Identity — mapping the identity function does nothing
// map(fa, x => x) === fa
map(Ok(42), x => x); // Must equal Ok(42)

// Law 2: Composition — mapping f then g equals mapping (g ∘ f)
// map(map(fa, f), g) === map(fa, x => g(f(x)))
const f = (x: number) => x + 1;
const g = (x: number) => x * 2;
map(map(Ok(5), f), g);        // Ok(12)
map(Ok(5), x => g(f(x)));     // Ok(12) — must be equal
```

#### Monad Laws

A Monad provides `flatMap: (fa: F<A>, f: A => F<B>) => F<B>` and `of: (a: A) => F<A>`:

```ts
// Law 1: Left Identity — of(a) flatMap f === f(a)
flatMap(Ok(5), x => Ok(x + 1)); // Must equal Ok(6)

// Law 2: Right Identity — fa flatMap of === fa
flatMap(Ok(5), Ok);              // Must equal Ok(5)

// Law 3: Associativity — (fa flatMap f) flatMap g === fa flatMap (a => f(a) flatMap g)
const f2 = (x: number) => Ok(x + 1);
const g2 = (x: number) => Ok(x * 2);
flatMap(flatMap(Ok(5), f2), g2);           // Ok(12)
flatMap(Ok(5), x => flatMap(f2(x), g2));   // Ok(12) — must be equal
```

#### Applicative Laws

An Applicative provides `ap: (fab: F<A => B>, fa: F<A>) => F<B>`:

```ts
// Law 1: Identity — ap(of(id), v) === v
// Law 2: Composition — ap(ap(ap(of(compose), u), v), w) === ap(u, ap(v, w))
// Law 3: Homomorphism — ap(of(f), of(x)) === of(f(x))
// Law 4: Interchange — ap(u, of(y)) === ap(of(f => f(y)), u)
```

#### Why Laws Matter in Practice

```ts
// If map violates identity law, refactoring breaks:
// Before refactoring:
const result1 = pipe(
  fetchData(),
  map(x => x),        // "no-op" — should be removable
  map(transform),
);

// After refactoring (removing identity map):
const result2 = pipe(
  fetchData(),
  map(transform),
);
// If identity law holds: result1 === result2 (safe to refactor)
// If identity law is violated: result1 !== result2 (refactoring introduces bugs!)
```

### Appendix B — Tagless Final Encoding

Tagless final is a pattern for writing programs that are polymorphic over their interpreter. Instead of building an AST (initial encoding), you write programs against an interface (final encoding).

```ts
// Step 1: Define the "algebra" (interface of operations)
interface ConsoleAlg<F extends URIS> {
  log: (msg: string) => Kind<F, void>;
  readLine: Kind<F, string>;
}

interface MathAlg<F extends URIS> {
  add: (a: number, b: number) => Kind<F, number>;
  multiply: (a: number, b: number) => Kind<F, number>;
}

// Step 2: Write programs against the algebra (polymorphic over F)
function program<F extends URIS>(
  M: Monad<F>,
  C: ConsoleAlg<F>,
  Math: MathAlg<F>
): Kind<F, void> {
  return pipe(
    C.log("Enter a number:"),
    M.chain(() => C.readLine),
    M.chain((input) => Math.add(Number(input), 10)),
    M.chain((result) => C.log(`Result: ${result}`)),
  );
}

// Step 3: Provide different interpreters

// Production interpreter (real IO)
const ConsoleIO: ConsoleAlg<"IO"> = {
  log: (msg) => IO(() => console.log(msg)),
  readLine: IO(() => prompt("") ?? ""),
};

// Test interpreter (pure, deterministic)
const ConsoleMock: ConsoleAlg<"State"> = {
  log: (msg) => State(s => [undefined, { ...s, output: [...s.output, msg] }]),
  readLine: State(s => [s.input.shift() ?? "", s]),
};

// Same program, different behaviors — no code change needed!
```

### Appendix C — Algebraic Data Types in TypeScript

TypeScript's discriminated unions are **sum types** (OR), and interfaces/intersections are **product types** (AND). Together they form Algebraic Data Types (ADTs).

```ts
// Product type (AND): all fields must be present
type Point = { x: number; y: number }; // x AND y
// Cardinality: |number| × |number| (product of possibilities)

// Sum type (OR): exactly one variant
type Shape =
  | { tag: "circle"; radius: number }
  | { tag: "rect"; width: number; height: number };
// Cardinality: |number| + (|number| × |number|) (sum of possibilities)

// The "algebra" in ADT:
// Product types multiply cardinalities
// Sum types add cardinalities
// This is why they're called "algebraic"!

// Recursive ADTs (like linked lists, trees):
type List<A> =
  | { tag: "Nil" }
  | { tag: "Cons"; head: A; tail: List<A> };

type Tree<A> =
  | { tag: "Leaf"; value: A }
  | { tag: "Branch"; left: Tree<A>; right: Tree<A> };

// Pattern matching via exhaustive switch:
function sum(list: List<number>): number {
  switch (list.tag) {
    case "Nil": return 0;
    case "Cons": return list.head + sum(list.tail);
  }
}

function depth<A>(tree: Tree<A>): number {
  switch (tree.tag) {
    case "Leaf": return 1;
    case "Branch": return 1 + Math.max(depth(tree.left), depth(tree.right));
  }
}
```

---

*Last updated: 2026-05-24*
