---
title: "13.2 — Type System: Primitives, Unions, Intersections, Generics"
subject: "TypeScript"
catalog: advanced
audience_tier: higher-education
chapter: "13.2"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 13.2 — Type System: Primitives, Unions, Intersections, Generics

> *"Types are not about preventing you from writing code. They're about giving you confidence that the code you wrote does what you think it does."* — **Anders Hejlsberg**, creator of TypeScript

The type system is TypeScript's entire reason for existing. This isn't just "adding annotations to JavaScript" — it's a complete language for describing the shape of data at compile time. Once you internalize structural typing and learn to think in unions and generics, you'll wonder how you ever wrote JavaScript without it.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Use all primitive types, literal types, and special types (`unknown`, `never`, `void`, `any`).
2. Compose types with unions (`|`) and intersections (`&`) and explain them as set operations.
3. Write generic functions and types with constraints, defaults, and inference.
4. Narrow types using type guards, discriminated unions, and control flow analysis.
5. Apply built-in utility types (`Partial`, `Required`, `Pick`, `Omit`, `Record`, `Readonly`).
6. Distinguish `type` aliases from `interface` declarations and choose correctly.
7. Explain structural typing vs nominal typing and why TypeScript chose structural.

---

## 🖼️ Visual Anchor — TypeScript Type Hierarchy

![ts__6.2-fig1](ts__6.2-fig1.svg)

---

## 📚 1. Concepts & Definitions

### Definition 13.2.1 — Structural Typing

TypeScript uses **structural typing** (aka "duck typing" at compile time). Two types are compatible if their structures match — names don't matter.

```ts
interface Point2D {
  x: number;
  y: number;
}

interface Coordinate {
  x: number;
  y: number;
}

// These are THE SAME TYPE to TypeScript — same structure
const p: Point2D = { x: 1, y: 2 };
const c: Coordinate = p; // ✅ No error — structures match
```

**Python parallel:** This is exactly like Python's `Protocol` — if it has the right methods/attributes, it satisfies the type. Unlike Java/C# where you must explicitly `implements InterfaceName`.

### Definition 13.2.2 — Primitive Types

```ts
// The 7 primitive types
const str: string = "hello";
const num: number = 42;           // no int/float distinction
const big: bigint = 9007199254740993n;
const bool: boolean = true;
const sym: symbol = Symbol("id");
const nul: null = null;
const undef: undefined = undefined;
```

### Definition 13.2.3 — Literal Types

A **literal type** is a type that represents exactly one value:

```ts
const direction: "north" | "south" | "east" | "west" = "north";
const httpStatus: 200 | 404 | 500 = 200;
const isTrue: true = true;

// `const` assertions create literal types
const config = { port: 3000, host: "localhost" } as const;
// type: { readonly port: 3000; readonly host: "localhost" }
// Without `as const`: { port: number; host: string }
```

### Definition 13.2.4 — Special Types

| Type | Meaning | Use Case |
|------|---------|----------|
| `any` | Opts out of type checking entirely | Migration from JS (avoid in new code) |
| `unknown` | "I don't know what this is — check before using" | Safe alternative to `any` |
| `never` | "This can never happen" | Exhaustive checks, impossible states |
| `void` | "This function doesn't return a meaningful value" | Callbacks, event handlers |

```ts
// unknown: must narrow before use
function processInput(input: unknown): string {
  if (typeof input === "string") return input.toUpperCase();
  if (typeof input === "number") return input.toFixed(2);
  throw new Error(`Unexpected input: ${input}`);
}

// never: exhaustive switch
type Shape = "circle" | "square" | "triangle";
function getArea(shape: Shape): number {
  switch (shape) {
    case "circle": return Math.PI * 4;
    case "square": return 16;
    case "triangle": return 8;
    default:
      const _exhaustive: never = shape; // Error if we miss a case
      throw new Error(`Unknown shape: ${_exhaustive}`);
  }
}
```

### Definition 13.2.5 — Union Types (`|`)

A union type means "this value is ONE OF these types":

```ts
type StringOrNumber = string | number;
type Status = "loading" | "success" | "error";
type MaybeUser = User | null;

function format(value: string | number): string {
  // Must narrow before using type-specific methods
  if (typeof value === "string") {
    return value.toUpperCase(); // TS knows it's string here
  }
  return value.toFixed(2); // TS knows it's number here
}
```

### Definition 13.2.6 — Intersection Types (`&`)

An intersection type means "this value has ALL of these types combined":

```ts
type Timestamped = { createdAt: Date; updatedAt: Date };
type SoftDeletable = { deletedAt: Date | null };

type User = {
  id: string;
  name: string;
  email: string;
};

// User AND Timestamped AND SoftDeletable — has all properties
type PersistedUser = User & Timestamped & SoftDeletable;

const user: PersistedUser = {
  id: "1",
  name: "Bill",
  email: "bill@example.com",
  createdAt: new Date(),
  updatedAt: new Date(),
  deletedAt: null,
};
```

### Definition 13.2.7 — Type Aliases vs Interfaces

```ts
// Type alias — can represent ANY type
type ID = string | number;
type Pair<T> = [T, T];
type Callback = (error: Error | null, data: unknown) => void;

// Interface — specifically for object shapes (extendable)
interface Animal {
  name: string;
  sound(): string;
}

interface Dog extends Animal {
  breed: string;
  fetch(): void;
}
```

**When to use which:**
- **`interface`** for object shapes that might be extended (API contracts, class implementations)
- **`type`** for everything else (unions, tuples, mapped types, primitives)
- In practice: pick one and be consistent. Most modern TS codebases prefer `type` for everything.

---

## 🧩 2. Mental Models

### Model 6.2.1 — Types as Sets

The most powerful mental model for TypeScript's type system: **every type is a set of possible values**.

```
string    = the set of all possible strings
number    = the set of all possible numbers
"hello"   = a set with exactly one member: the string "hello"
never     = the empty set (no values)
unknown   = the universal set (all values)

Union (|)        = set UNION         (A ∪ B)
Intersection (&) = set INTERSECTION  (A ∩ B)
```

This explains why:
- `string | number` is WIDER than `string` (more values in the set)
- `string & number` is `never` (no value is both a string AND a number)
- `"hello" | "world"` is NARROWER than `string` (only 2 values vs infinite)
- Every type is a subset of `unknown` (universal set)
- `never` is a subset of every type (empty set is subset of everything)

### Model 6.2.2 — Narrowing as Set Reduction

When you write a type guard, you're **reducing the set** of possible values:

```ts
function process(value: string | number | null) {
  // Here: value ∈ {all strings} ∪ {all numbers} ∪ {null}

  if (value === null) return "nothing";
  // Here: value ∈ {all strings} ∪ {all numbers}  (null eliminated)

  if (typeof value === "string") {
    // Here: value ∈ {all strings}  (number eliminated)
    return value.toUpperCase();
  }

  // Here: value ∈ {all numbers}  (string eliminated)
  return value.toFixed(2);
}
```

### Model 6.2.3 — Generics as Type Parameters (Functions for Types)

Generics are **functions at the type level**. Just as a regular function takes a value and returns a value, a generic takes a type and returns a type.

```ts
// Regular function: value → value
function identity(x: number): number { return x; }

// Generic function: type → type (parameterized)
function identity<T>(x: T): T { return x; }

// Python parallel:
// def identity(x: T) -> T: return x  (TypeVar)
```

### Model 6.2.4 — Structural Compatibility Direction

TypeScript allows a value to be assigned to a variable if the value has **at least** the required properties (it can have more):

```ts
interface HasName { name: string }

const user = { name: "Bill", age: 35, email: "bill@x.com" };
const named: HasName = user; // ✅ user has 'name' (plus extras — that's fine)

// But NOT the other way:
// const full: typeof user = named; // ❌ named might not have age/email
```

This is "width subtyping" — wider objects (more properties) are subtypes of narrower ones.


---

## 🔑 3. Mechanics

### 3.1 — Type Annotations & Inference

TypeScript infers types when it can. Add explicit annotations at **boundaries** (function parameters, return types, exported values):

```ts
// TS infers: const x: number
const x = 42;

// TS infers: const arr: number[]
const arr = [1, 2, 3];

// TS infers return type: number
function double(n: number) {
  return n * 2;
}

// ALWAYS annotate function parameters (TS cannot infer them)
function greet(name: string): string {
  return `Hello, ${name}`;
}

// Annotate when inference is too wide
const status = "loading"; // inferred: string (too wide!)
const status2 = "loading" as const; // inferred: "loading" (literal)
const status3: "loading" | "done" = "loading"; // explicit union
```

### 3.2 — Object Types

```ts
// Inline object type
function createUser(opts: { name: string; email: string; age?: number }) {
  // age is optional (age?: number means age: number | undefined)
  return { id: crypto.randomUUID(), ...opts };
}

// Named interface (preferred for reuse)
interface Config {
  readonly host: string;    // cannot be reassigned after creation
  port: number;
  debug?: boolean;          // optional
  [key: string]: unknown;   // index signature: allows extra properties
}

// Readonly utility (makes ALL properties readonly)
type FrozenConfig = Readonly<Config>;
```

### 3.3 — Array & Tuple Types

```ts
// Arrays (two equivalent syntaxes)
const nums: number[] = [1, 2, 3];
const strs: Array<string> = ["a", "b", "c"];

// Readonly arrays (cannot push, pop, splice)
const frozen: readonly number[] = [1, 2, 3];
// frozen.push(4); // Error: Property 'push' does not exist on readonly number[]

// Tuples (fixed-length, typed by position)
type Point = [x: number, y: number];           // labeled tuple
type HttpResult = [status: number, body: string];
type RGB = [red: number, green: number, blue: number];

const origin: Point = [0, 0];
const response: HttpResult = [200, '{"ok": true}'];

// Variadic tuples (rest elements)
type StringAndNumbers = [string, ...number[]];
const data: StringAndNumbers = ["header", 1, 2, 3, 4];
```

### 3.4 — Generics

```ts
// Generic function — T is inferred from the argument
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

const n = first([1, 2, 3]);       // T inferred as number → n: number | undefined
const s = first(["a", "b"]);     // T inferred as string → s: string | undefined

// Generic with constraint
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: "Bill", age: 35 };
const name = getProperty(user, "name"); // type: string
const age = getProperty(user, "age");   // type: number
// getProperty(user, "email");          // Error: "email" not in keyof user

// Generic interface
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  create(item: Omit<T, "id">): Promise<T>;
  update(id: string, patch: Partial<T>): Promise<T>;
  delete(id: string): Promise<void>;
}

// Generic with default
interface PaginatedResponse<T, M = { total: number; page: number }> {
  data: T[];
  meta: M;
}
```

### 3.5 — Type Narrowing

TypeScript's control flow analysis automatically narrows types:

```ts
// typeof guards
function stringify(value: unknown): string {
  if (typeof value === "string") return value;
  if (typeof value === "number") return value.toString();
  if (typeof value === "boolean") return value ? "true" : "false";
  if (value === null) return "null";
  if (value === undefined) return "undefined";
  return JSON.stringify(value);
}

// instanceof guards
function formatError(err: unknown): string {
  if (err instanceof Error) return err.message;
  if (typeof err === "string") return err;
  return "Unknown error";
}

// in operator
interface Fish { swim(): void }
interface Bird { fly(): void }

function move(animal: Fish | Bird) {
  if ("swim" in animal) {
    animal.swim(); // TS knows it's Fish
  } else {
    animal.fly();  // TS knows it's Bird
  }
}

// Discriminated unions (THE most important pattern in TS)
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

function handleResult(result: Result<string>) {
  if (result.success) {
    console.log(result.data);   // TS knows data exists
  } else {
    console.error(result.error); // TS knows error exists
  }
}

// Custom type guard (user-defined)
function isString(value: unknown): value is string {
  return typeof value === "string";
}

// Assertion function (throws if not valid)
function assertDefined<T>(value: T | null | undefined, msg?: string): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(msg ?? "Value is null/undefined");
  }
}
```

### 3.6 — Utility Types (Built-in)

```ts
interface User {
  id: string;
  name: string;
  email: string;
  age: number;
  role: "admin" | "user";
}

// Partial<T> — all properties optional
type UserUpdate = Partial<User>;
// { id?: string; name?: string; email?: string; age?: number; role?: ... }

// Required<T> — all properties required
type StrictUser = Required<User>;

// Pick<T, K> — select specific properties
type UserPreview = Pick<User, "id" | "name">;
// { id: string; name: string }

// Omit<T, K> — remove specific properties
type CreateUser = Omit<User, "id">;
// { name: string; email: string; age: number; role: ... }

// Record<K, V> — object with keys K and values V
type UserMap = Record<string, User>;
const users: UserMap = { "1": { id: "1", name: "Bill", email: "b@x.com", age: 35, role: "admin" } };

// Readonly<T> — all properties readonly
type FrozenUser = Readonly<User>;

// ReturnType<T> — extract return type of a function
function createUser() { return { id: "1", name: "Bill" }; }
type CreatedUser = ReturnType<typeof createUser>;
// { id: string; name: string }

// Parameters<T> — extract parameter types as tuple
type CreateUserParams = Parameters<typeof createUser>;
// []

// Awaited<T> — unwrap Promise
type UserData = Awaited<Promise<User>>; // User

// NonNullable<T> — remove null and undefined
type DefiniteUser = NonNullable<User | null | undefined>; // User

// Extract / Exclude — filter union members
type AdminOrUser = Extract<User["role"], "admin" | "moderator">; // "admin"
type NotAdmin = Exclude<User["role"], "admin">; // "user"
```

### 3.7 — Enums vs Union Types

```ts
// ❌ Numeric enums (avoid — they have weird reverse-mapping behavior)
enum Direction {
  Up,    // 0
  Down,  // 1
  Left,  // 2
  Right, // 3
}

// ✅ String enums (acceptable, but unions are usually better)
enum HttpMethod {
  GET = "GET",
  POST = "POST",
  PUT = "PUT",
  DELETE = "DELETE",
}

// ✅✅ Union types (preferred in modern TS)
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";

// Why unions > enums:
// 1. No runtime code generated (enums emit JS objects)
// 2. Better type inference
// 3. Work with template literal types
// 4. No import needed — just use the string
```

### 3.8 — `satisfies` Operator (TS 5.0+)

```ts
type ColorMap = Record<string, [number, number, number] | string>;

// Without satisfies: loses specific key information
const colors1: ColorMap = {
  red: [255, 0, 0],
  green: "#00ff00",
};
// colors1.red is [number, number, number] | string — too wide!

// With satisfies: validates AND preserves narrow type
const colors2 = {
  red: [255, 0, 0],
  green: "#00ff00",
} satisfies ColorMap;
// colors2.red is [number, number, number] — narrow!
// colors2.green is string — narrow!
// colors2.blue // Error: property doesn't exist (caught!)
```


---

## 💻 4. Code Patterns & Examples

### Pattern 6.2.1 — Discriminated Union for State Management

```ts
// The "tagged union" pattern — TypeScript's answer to algebraic data types
type AsyncState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

function renderState<T>(state: AsyncState<T>): string {
  switch (state.status) {
    case "idle":
      return "Ready to fetch";
    case "loading":
      return "Loading...";
    case "success":
      return `Got data: ${JSON.stringify(state.data)}`;
    case "error":
      return `Error: ${state.error.message}`;
  }
  // No default needed — TS knows all cases are covered (exhaustive)
}

// Usage:
let userState: AsyncState<User> = { status: "idle" };
userState = { status: "loading" };
userState = { status: "success", data: { id: "1", name: "Bill", email: "b@x.com", age: 35, role: "admin" } };
```

### Pattern 6.2.2 — Generic Constraint Patterns

```ts
// Constraint: T must have a 'length' property
function longest<T extends { length: number }>(a: T, b: T): T {
  return a.length >= b.length ? a : b;
}

longest("hello", "hi");       // ✅ strings have length
longest([1, 2, 3], [1]);      // ✅ arrays have length
// longest(10, 20);            // ❌ numbers don't have length

// Constraint: K must be a key of T
function pluck<T, K extends keyof T>(items: T[], key: K): T[K][] {
  return items.map(item => item[key]);
}

const users = [
  { name: "Bill", age: 35 },
  { name: "Alice", age: 28 },
];
const names = pluck(users, "name"); // string[]
const ages = pluck(users, "age");   // number[]

// Constraint: T must be constructable
function createInstance<T>(ctor: new (...args: any[]) => T, ...args: any[]): T {
  return new ctor(...args);
}
```

### Pattern 6.2.3 — Builder Pattern with Generics

```ts
// Type-safe builder that tracks which fields have been set
interface QueryBuilder<T extends Record<string, unknown>> {
  select<K extends keyof T>(...keys: K[]): QueryBuilder<Pick<T, K>>;
  where(predicate: (item: T) => boolean): QueryBuilder<T>;
  orderBy(key: keyof T, direction?: "asc" | "desc"): QueryBuilder<T>;
  execute(): Promise<T[]>;
}

// Usage shows how generics flow through method chains:
declare const db: QueryBuilder<User>;
const result = await db
  .select("name", "email")  // QueryBuilder<Pick<User, "name" | "email">>
  .where(u => u.name.startsWith("B"))
  .orderBy("name", "asc")
  .execute(); // Promise<{ name: string; email: string }[]>
```

### Pattern 6.2.4 — Function Overloads

```ts
// When a function has different return types based on input types
function createElement(tag: "a"): HTMLAnchorElement;
function createElement(tag: "canvas"): HTMLCanvasElement;
function createElement(tag: "div"): HTMLDivElement;
function createElement(tag: string): HTMLElement;
function createElement(tag: string): HTMLElement {
  return document.createElement(tag);
}

const link = createElement("a");     // HTMLAnchorElement
const canvas = createElement("canvas"); // HTMLCanvasElement
const div = createElement("div");    // HTMLDivElement
const span = createElement("span");  // HTMLElement (fallback)
```

---

## 🧮 5. Worked Examples

### Example 13.2.1 — Type a Configuration System

**Task:** Create a type-safe configuration system where each config key has a specific value type.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```ts
// Define the config schema as a type
interface AppConfig {
  port: number;
  host: string;
  debug: boolean;
  logLevel: "error" | "warn" | "info" | "debug";
  database: {
    url: string;
    pool: number;
    ssl: boolean;
  };
}

// Type-safe getter that returns the correct type for each key
function getConfig<K extends keyof AppConfig>(key: K): AppConfig[K] {
  return config[key];
}

// Type-safe setter
function setConfig<K extends keyof AppConfig>(key: K, value: AppConfig[K]): void {
  config[key] = value;
}

// Deep config access with dot notation (advanced)
type DotPath<T, Prefix extends string = ""> = T extends object
  ? { [K in keyof T & string]:
      | `${Prefix}${K}`
      | DotPath<T[K], `${Prefix}${K}.`>
    }[keyof T & string]
  : never;

type ConfigPath = DotPath<AppConfig>;
// "port" | "host" | "debug" | "logLevel" | "database" | "database.url" | "database.pool" | "database.ssl"

const config: AppConfig = {
  port: 3000,
  host: "localhost",
  debug: true,
  logLevel: "info",
  database: { url: "postgres://...", pool: 10, ssl: true },
};

const port = getConfig("port");       // number
const level = getConfig("logLevel");  // "error" | "warn" | "info" | "debug"
setConfig("port", 8080);             // ✅
// setConfig("port", "8080");         // ❌ Error: string not assignable to number
```

</details>

### Example 13.2.2 — Implement a Type-Safe Event Emitter

**Task:** Build an event emitter where each event name maps to a specific payload type.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```ts
// Define event map
interface AppEvents {
  "user:login": { userId: string; timestamp: number };
  "user:logout": { userId: string };
  "error": { code: number; message: string };
  "data:sync": { table: string; count: number };
}

// Type-safe event emitter
class TypedEmitter<Events extends Record<string, unknown>> {
  private listeners = new Map<keyof Events, Set<Function>>();

  on<E extends keyof Events>(event: E, handler: (payload: Events[E]) => void): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(handler);
  }

  off<E extends keyof Events>(event: E, handler: (payload: Events[E]) => void): void {
    this.listeners.get(event)?.delete(handler);
  }

  emit<E extends keyof Events>(event: E, payload: Events[E]): void {
    this.listeners.get(event)?.forEach(handler => handler(payload));
  }
}

// Usage:
const bus = new TypedEmitter<AppEvents>();

bus.on("user:login", (payload) => {
  // payload is { userId: string; timestamp: number } — fully typed!
  console.log(`User ${payload.userId} logged in at ${payload.timestamp}`);
});

bus.emit("user:login", { userId: "123", timestamp: Date.now() }); // ✅
// bus.emit("user:login", { userId: 123 }); // ❌ Error: number not assignable to string
// bus.emit("unknown:event", {});           // ❌ Error: not in AppEvents
```

</details>

### Example 13.2.3 — Generic Result Type with Error Handling

**Task:** Implement a `Result<T, E>` type that forces callers to handle errors.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```ts
// Discriminated union Result type
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

// Constructor helpers
function Ok<T>(value: T): Result<T, never> {
  return { ok: true, value };
}

function Err<E>(error: E): Result<never, E> {
  return { ok: false, error };
}

// Usage in a function that can fail
interface ValidationError {
  field: string;
  message: string;
}

function parseAge(input: string): Result<number, ValidationError> {
  const num = Number(input);
  if (isNaN(num)) {
    return Err({ field: "age", message: "Not a valid number" });
  }
  if (num < 0 || num > 150) {
    return Err({ field: "age", message: "Age must be 0-150" });
  }
  return Ok(num);
}

// Caller MUST handle both cases
const result = parseAge("35");
if (result.ok) {
  console.log(`Age: ${result.value}`); // value: number
} else {
  console.error(`${result.error.field}: ${result.error.message}`);
}

// Chaining Results (map/flatMap pattern)
function mapResult<T, U, E>(result: Result<T, E>, fn: (value: T) => U): Result<U, E> {
  if (result.ok) return Ok(fn(result.value));
  return result;
}

const doubled = mapResult(parseAge("35"), age => age * 2);
```

</details>

### Example 13.2.4 — Type-Safe API Client

**Task:** Create an API client where routes are typed and responses are inferred.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```ts
// Define API schema
interface ApiRoutes {
  "GET /users": { response: User[]; params: never };
  "GET /users/:id": { response: User; params: { id: string } };
  "POST /users": { response: User; params: never; body: Omit<User, "id"> };
  "PUT /users/:id": { response: User; params: { id: string }; body: Partial<User> };
  "DELETE /users/:id": { response: void; params: { id: string } };
}

// Extract method and path
type ApiMethod = "GET" | "POST" | "PUT" | "DELETE";

// Type-safe fetch wrapper
async function apiCall<R extends keyof ApiRoutes>(
  route: R,
  ...args: ApiRoutes[R] extends { body: infer B }
    ? [options: { params?: ApiRoutes[R]["params"]; body: B }]
    : ApiRoutes[R]["params"] extends never
      ? []
      : [options: { params: ApiRoutes[R]["params"] }]
): Promise<ApiRoutes[R]["response"]> {
  // Implementation would parse route, substitute params, fetch
  throw new Error("Not implemented");
}

// Usage — fully type-safe:
const users = await apiCall("GET /users");                    // User[]
const user = await apiCall("GET /users/:id", { params: { id: "1" } }); // User
const created = await apiCall("POST /users", {
  body: { name: "Bill", email: "b@x.com", age: 35, role: "user" }
}); // User
```

</details>

---

## ⚠️ 6. Gotchas & Anti-Patterns

### Gotcha 6.2.1 — `any` Escapes

```ts
// ❌ Using 'any' to silence errors
function processData(data: any) {
  return data.foo.bar.baz; // No error — but will crash at runtime!
}

// ✅ Use 'unknown' and narrow
function processData(data: unknown) {
  if (typeof data === "object" && data !== null && "foo" in data) {
    // Now safely access properties
  }
}

// ❌ Type assertion to silence errors
const value = someFunction() as any as SpecificType; // "double assertion" — code smell

// ✅ Proper narrowing or runtime validation
import { z } from "zod";
const schema = z.object({ name: z.string(), age: z.number() });
const value = schema.parse(someFunction()); // Validated at runtime, typed at compile time
```

### Gotcha 6.2.2 — Object Literal Excess Property Checking

```ts
interface Point { x: number; y: number }

// Direct assignment: excess properties ARE checked
// const p: Point = { x: 1, y: 2, z: 3 }; // ❌ Error: 'z' does not exist

// Variable assignment: excess properties are NOT checked
const obj = { x: 1, y: 2, z: 3 };
const p: Point = obj; // ✅ No error! (structural typing allows extra props)

// This is intentional — structural typing means "at least these properties"
// Excess property checking on literals is a special convenience check
```

### Gotcha 6.2.3 — Mutable Array Inference

```ts
// TS infers mutable arrays as wide types
const arr = [1, "hello", true]; // type: (string | number | boolean)[]

// If you want a tuple:
const tuple = [1, "hello", true] as const; // type: readonly [1, "hello", true]

// Common mistake with object arrays:
const statuses = ["loading", "success", "error"]; // string[] — NOT the union!
type Status = (typeof statuses)[number]; // string — useless!

// Fix: use as const
const statuses = ["loading", "success", "error"] as const;
type Status = (typeof statuses)[number]; // "loading" | "success" | "error" ✅
```

### Gotcha 6.2.4 — Generic Inference Failures

```ts
// TS can't always infer generics from context
function merge<T>(a: Partial<T>, b: Partial<T>): T {
  return { ...a, ...b } as T;
}

// This fails — TS can't infer T from two Partial<T> arguments
// const result = merge({ name: "Bill" }, { age: 35 }); // T = { name: string } | { age: number } — wrong!

// Fix: provide the generic explicitly
interface User { name: string; age: number }
const result = merge<User>({ name: "Bill" }, { age: 35 }); // ✅
```

### Gotcha 6.2.5 — `readonly` is Shallow

```ts
interface Config {
  readonly settings: {
    theme: string;
    fontSize: number;
  };
}

const config: Config = { settings: { theme: "dark", fontSize: 14 } };
// config.settings = { ... }; // ❌ Error: readonly
config.settings.theme = "light"; // ✅ No error! Nested mutation allowed!

// Fix: use Readonly recursively or use as const
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};
```

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- **Previous:** [13.1 - Setup, Compilation & Project Structure](13.1---Setup,-Compilation-&-Project-Structure)
- **Next:** [13.3 - Advanced Types - Conditional, Mapped, Template Literal Types](13.3---Advanced-Types---Conditional,-Mapped,-Template-Literal-Types)
- **Python OOP comparison:** [08.3 - OOP, Data Models & Pythonic Idioms](08.3---OOP,-Data-Models-&-Pythonic-Idioms) — structural typing ≈ Python protocols
- **React with TS:** [13.7 - Frontend with TypeScript - React, Vue, Svelte, SolidJS](13.7---Frontend-with-TypeScript---React,-Vue,-Svelte,-SolidJS)

### External Resources
- [TypeScript Handbook — Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)
- [TypeScript Handbook — Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)
- [TypeScript Handbook — Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html)
- [Total TypeScript — Generics Tutorial](https://www.totaltypescript.com/tutorials/beginners-typescript)
- [Matt Pocock — Utility Types You Need to Know](https://www.mattpocock.com/)
- [type-challenges — Easy Level](https://github.com/type-challenges/type-challenges)

---

*Last updated: 2026-05-24*



---

## 🏗️ 8. Advanced Type System Patterns & Exhaustiveness

### 8.1 — Full Discriminated Union Exhaustiveness with `never`

The `never` type is TypeScript's "bottom type" — it represents a value that can never exist. This makes it the perfect tool for compile-time exhaustiveness checking.

#### The Exhaustive Switch Pattern

```ts
// Helper: throws at runtime if called, errors at compile time if reachable
function assertNever(value: never, message?: string): never {
  throw new Error(message ?? `Unexpected value: ${JSON.stringify(value)}`);
}

type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rectangle":
      return shape.width * shape.height;
    case "triangle":
      return 0.5 * shape.base * shape.height;
    default:
      // If you add a new shape variant and forget to handle it,
      // TypeScript errors HERE at compile time:
      // "Argument of type '{ kind: "pentagon"; ... }' is not assignable to parameter of type 'never'"
      return assertNever(shape);
  }
}
```

#### Exhaustiveness in Reducers

```ts
type Action =
  | { type: "INCREMENT"; amount: number }
  | { type: "DECREMENT"; amount: number }
  | { type: "RESET" }
  | { type: "SET"; value: number };

interface State {
  count: number;
  lastAction: Action["type"];
}

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "INCREMENT":
      return { count: state.count + action.amount, lastAction: "INCREMENT" };
    case "DECREMENT":
      return { count: state.count - action.amount, lastAction: "DECREMENT" };
    case "RESET":
      return { count: 0, lastAction: "RESET" };
    case "SET":
      return { count: action.value, lastAction: "SET" };
    default:
      return assertNever(action);
  }
}
```

#### Exhaustive Object Maps (Alternative to Switch)

```ts
// Instead of switch, use a const object with satisfies
const AREA_CALCULATORS = {
  circle: (s: Extract<Shape, { kind: "circle" }>) => Math.PI * s.radius ** 2,
  rectangle: (s: Extract<Shape, { kind: "rectangle" }>) => s.width * s.height,
  triangle: (s: Extract<Shape, { kind: "triangle" }>) => 0.5 * s.base * s.height,
} satisfies Record<Shape["kind"], (s: any) => number>;

// If you add a new Shape variant, TypeScript errors on the `satisfies` line
// because the new key is missing from the object.

function area2(shape: Shape): number {
  return AREA_CALCULATORS[shape.kind](shape as any);
}
```

### 8.2 — Mapped Types with Key Remapping

TypeScript 4.1+ allows you to transform keys during mapping using the `as` clause:

```ts
// Basic key remapping: prefix all keys
type Prefixed<T, P extends string> = {
  [K in keyof T as `${P}${Capitalize<string & K>}`]: T[K];
};

interface User {
  name: string;
  age: number;
  email: string;
}

type PrefixedUser = Prefixed<User, "user">;
// { userName: string; userAge: number; userEmail: string }
```

#### Filtering Keys with Remapping

```ts
// Remove keys whose values are functions
type DataOnly<T> = {
  [K in keyof T as T[K] extends Function ? never : K]: T[K];
};

interface UserService {
  name: string;
  age: number;
  greet(): string;
  save(): Promise<void>;
}

type UserData = DataOnly<UserService>;
// { name: string; age: number }
```

#### Event Handler Type Generation

```ts
// Generate event handler types from an event map
type EventHandlers<Events extends Record<string, unknown>> = {
  [K in keyof Events as `on${Capitalize<string & K>}`]: (payload: Events[K]) => void;
};

interface AppEvents {
  login: { userId: string };
  logout: { reason: string };
  error: { code: number; message: string };
}

type Handlers = EventHandlers<AppEvents>;
// {
//   onLogin: (payload: { userId: string }) => void;
//   onLogout: (payload: { reason: string }) => void;
//   onError: (payload: { code: number; message: string }) => void;
// }
```

#### Getter/Setter Generation

```ts
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

type Setters<T> = {
  [K in keyof T as `set${Capitalize<string & K>}`]: (value: T[K]) => void;
};

type WithAccessors<T> = T & Getters<T> & Setters<T>;

type UserWithAccessors = WithAccessors<{ name: string; age: number }>;
// {
//   name: string; age: number;
//   getName: () => string; getAge: () => number;
//   setName: (value: string) => void; setAge: (value: number) => void;
// }
```

### 8.3 — The `satisfies` Operator: Type Checking Without Widening

`satisfies` (TS 4.9+) validates that an expression matches a type without changing the inferred type. This is crucial when you want both type safety AND narrow literal inference.

```ts
// WITHOUT satisfies — type is widened
const palette: Record<string, string | number[]> = {
  red: "#ff0000",
  green: [0, 255, 0],
  blue: "#0000ff",
};
palette.red.toUpperCase(); // ❌ Error: string | number[] has no toUpperCase

// WITH satisfies — validated but not widened
const palette2 = {
  red: "#ff0000",
  green: [0, 255, 0],
  blue: "#0000ff",
} satisfies Record<string, string | number[]>;

palette2.red.toUpperCase();  // ✅ TypeScript knows red is string
palette2.green.map(x => x);  // ✅ TypeScript knows green is number[]
```

#### `satisfies` Gotchas

```ts
// Gotcha 1: satisfies doesn't prevent excess properties
const config = {
  port: 3000,
  host: "localhost",
  typo: true, // ❌ You might expect an error, but satisfies allows excess props!
} satisfies { port: number; host: string };

// Fix: use a type annotation for strict shape checking
const config2: { port: number; host: string } = {
  port: 3000,
  host: "localhost",
  // typo: true, // ✅ Error: excess property
};

// Gotcha 2: satisfies with as const
const routes = {
  home: "/",
  about: "/about",
  users: "/users",
} as const satisfies Record<string, `/${string}`>;
// ✅ Both: literal types preserved AND validated against the pattern

// Gotcha 3: satisfies doesn't narrow in control flow
function process(input: unknown) {
  const validated = input satisfies string; // ❌ This doesn't narrow!
  // satisfies is for declarations, not runtime narrowing
}
```

### 8.4 — Branded/Nominal Types via Intersection

TypeScript is structurally typed, but sometimes you need nominal typing (two types with the same shape should NOT be interchangeable):

```ts
// The "brand" pattern: intersect with a unique symbol
declare const __brand: unique symbol;
type Brand<T, B extends string> = T & { readonly [__brand]: B };

// Create branded types
type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;
type Email = Brand<string, "Email">;

// Constructor functions that validate
function UserId(id: string): UserId {
  if (!id.startsWith("usr_")) throw new Error("Invalid user ID");
  return id as UserId;
}

function Email(email: string): Email {
  if (!email.includes("@")) throw new Error("Invalid email");
  return email as Email;
}

// Now these are NOT interchangeable despite both being strings:
function getUser(id: UserId): void { /* ... */ }
function getOrder(id: OrderId): void { /* ... */ }

const userId = UserId("usr_123");
const orderId = "ord_456" as OrderId;

getUser(userId);   // ✅
// getUser(orderId); // ❌ Error: OrderId not assignable to UserId
// getUser("raw");   // ❌ Error: string not assignable to UserId
```

---

## 📎 9. Appendix — Deep Dives & Theory

### Appendix A — Type-Level Set Theory

TypeScript's type system is a set-theoretic type system. Understanding the set theory behind it clarifies many confusing behaviors.

#### Types as Sets of Values

| Type | Set of Values |
|------|--------------|
| `never` | ∅ (empty set) |
| `unknown` | Universal set (all values) |
| `string` | Set of all strings |
| `"hello"` | Singleton set `{"hello"}` |
| `string \| number` | Union of string set and number set |
| `string & number` | Intersection (= `never`, since no value is both) |

#### Union = Set Union (OR)

```ts
type A = string | number;
// A value of type A can be ANY member of {all strings} ∪ {all numbers}
// This WIDENS the set — more values are allowed
```

#### Intersection = Set Intersection (AND)

```ts
type B = { name: string } & { age: number };
// A value of type B must be in BOTH sets simultaneously
// This NARROWS the set — fewer values qualify
// Result: { name: string; age: number }
```

#### The Counterintuitive Part: Intersection ADDS Properties

For object types, intersection means the value must satisfy BOTH constraints. Since objects can have extra properties (structural typing), the result has MORE required properties:

```ts
type HasName = { name: string };
type HasAge = { age: number };
type Person = HasName & HasAge;
// Person = { name: string; age: number }
// The intersection ADDS requirements (narrows the set of valid objects)
```

#### Narrowing = Moving Down the Set Hierarchy

```ts
function process(x: string | number) {
  // x is in the set: {all strings} ∪ {all numbers}

  if (typeof x === "string") {
    // x is now in the set: {all strings}
    // We've NARROWED from the union to a subset
    x.toUpperCase(); // ✅
  }
}
```

#### Distributive Conditional Types and Set Operations

```ts
// Conditional types distribute over unions:
type ToArray<T> = T extends any ? T[] : never;
type Result = ToArray<string | number>;
// Distributes: (string extends any ? string[] : never) | (number extends any ? number[] : never)
// = string[] | number[]
// NOT (string | number)[]

// This is set-theoretic: map a function over each element of the union
```

### Appendix B — Structural vs Nominal Typing Tradeoffs

#### Structural Typing (TypeScript's Default)

**Rule:** Two types are compatible if they have the same structure (shape), regardless of name.

```ts
interface Point2D { x: number; y: number }
interface Vector2D { x: number; y: number }

const p: Point2D = { x: 1, y: 2 };
const v: Vector2D = p; // ✅ Same shape = compatible
```

**Advantages:**
- Works naturally with JavaScript's duck typing
- No need to explicitly implement interfaces
- Third-party types are automatically compatible
- Enables powerful generic programming

**Disadvantages:**
- Accidental compatibility (a `UserId` string is assignable to an `OrderId` string)
- No way to distinguish semantically different types with the same shape
- Can't prevent misuse of similarly-shaped but logically different values

#### Nominal Typing (Simulated via Brands)

**Rule:** Two types are compatible only if they have the same declared name/brand.

```ts
type Meters = number & { readonly __brand: "Meters" };
type Feet = number & { readonly __brand: "Feet" };

function addMeters(a: Meters, b: Meters): Meters {
  return (a + b) as Meters;
}

const m = 5 as Meters;
const f = 16 as Feet;
addMeters(m, m); // ✅
// addMeters(m, f); // ❌ Feet not assignable to Meters
```

**When to use nominal typing:**
- Domain-driven design with value objects (Money, Distance, Temperature)
- IDs that should never be mixed (UserId vs OrderId vs SessionId)
- Units of measurement
- Security boundaries (sanitized HTML vs raw HTML)

#### The `unique symbol` Pattern (Zero Runtime Cost)

```ts
// Each branded type gets a unique phantom property
declare const MetersBrand: unique symbol;
declare const FeetBrand: unique symbol;

type Meters = number & { readonly [MetersBrand]: typeof MetersBrand };
type Feet = number & { readonly [FeetBrand]: typeof FeetBrand };

// The brand property doesn't exist at runtime — it's purely a compile-time check
// typeof MetersBrand is unique, so Meters and Feet are never compatible
```

### Appendix C — Variance in TypeScript

Variance describes how subtyping of complex types relates to subtyping of their components.

```ts
// Covariant (output position): if Dog extends Animal, then Array<Dog> extends Array<Animal>
type Producer<T> = () => T; // T in output position = covariant

// Contravariant (input position): if Dog extends Animal, then Handler<Animal> extends Handler<Dog>
type Consumer<T> = (value: T) => void; // T in input position = contravariant

// Invariant (both positions): neither direction works
type Mutable<T> = { value: T; set(v: T): void }; // T in both = invariant

// TypeScript 4.7+ explicit variance annotations:
type Producer2<out T> = () => T;        // Covariant
type Consumer2<in T> = (value: T) => void; // Contravariant
type Invariant2<in out T> = { get(): T; set(v: T): void };
```

#### Why This Matters: Function Parameter Bivariance

```ts
// TypeScript has a historical quirk: method parameters are BIVARIANT by default
// (both covariant and contravariant — unsound but practical)

interface Animal { name: string }
interface Dog extends Animal { breed: string }

// With --strictFunctionTypes (included in --strict):
type AnimalHandler = (animal: Animal) => void;
type DogHandler = (dog: Dog) => void;

// Function syntax: contravariant (correct)
let handler: AnimalHandler = (a: Animal) => console.log(a.name);
// handler = ((d: Dog) => console.log(d.breed)) as DogHandler; // ❌ Error (correct!)

// Method syntax: bivariant (unsound but allowed for compatibility)
interface EventMap {
  click(e: MouseEvent): void;  // Method syntax — bivariant
}
```

### Appendix D — The `infer` Keyword Deep Dive

`infer` declares a type variable inside a conditional type's `extends` clause:

```ts
// Extract return type
type ReturnOf<T> = T extends (...args: any[]) => infer R ? R : never;

// Extract promise value
type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;

// Extract array element
type ElementOf<T> = T extends (infer E)[] ? E : never;

// Multiple infer positions
type FirstAndRest<T extends any[]> =
  T extends [infer First, ...infer Rest] ? { first: First; rest: Rest } : never;

type Test = FirstAndRest<[1, 2, 3]>; // { first: 1; rest: [2, 3] }

// Infer in template literal types
type ExtractRouteParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractRouteParams<Rest>
    : T extends `${string}:${infer Param}`
      ? Param
      : never;

type Params = ExtractRouteParams<"/users/:userId/posts/:postId">;
// "userId" | "postId"
```

---

*Last updated: 2026-05-24*
