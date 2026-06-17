---
title: "TypeScript Essentials for Coding Tests"
subject: "TypeScript"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: learning-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# TypeScript Essentials for Coding Tests

**JavaScript + Types = Better Code**

---

## 1. Basic Types

### Primitives
```typescript
// String
let name: string = "Billy";
let message: string = `Hello ${name}`;

// Number (int, float, all same)
let age: number = 33;
let price: number = 9.99;
let hex: number = 0xff;

// Boolean
let isActive: boolean = true;
let isDone: boolean = false;

// Null & Undefined
let empty: null = null;
let notSet: undefined = undefined;

// Any (escape hatch - AVOID)
let anything: any = "can be anything";
anything = 42;  // No error

// Unknown (safer than any)
let userInput: unknown = getUserInput();
// Must check type before using
if (typeof userInput === "string") {
    console.log(userInput.toUpperCase());  // OK
}

// Void (no return value)
function logMessage(msg: string): void {
    console.log(msg);
    // No return
}

// Never (never returns)
function throwError(msg: string): never {
    throw new Error(msg);
}

function infiniteLoop(): never {
    while (true) {}
}
```

### Arrays
```typescript
// Two syntaxes (same thing)
let numbers: number[] = [1, 2, 3];
let names: Array<string> = ["Billy", "Alex"];

// Mixed types (union)
let mixed: (string | number)[] = [1, "two", 3];

// Readonly
let readOnly: readonly number[] = [1, 2, 3];
// readOnly.push(4);  // ERROR!
```

### Tuples (Fixed-length arrays with typed positions)
```typescript
// Tuple
let person: [string, number] = ["Billy", 33];
let point: [number, number] = [10, 20];

// Access
let name = person[0];  // string
let age = person[1];   // number

// Optional elements
let optional: [string, number?] = ["Billy"];

// Rest
let rest: [string, ...number[]] = ["Billy", 1, 2, 3];
```

---

## 2. Type Inference

### Let TypeScript Infer
```typescript
// TypeScript infers types automatically
let name = "Billy";        // inferred as string
let age = 33;              // inferred as number
let isActive = true;       // inferred as boolean

// Inferred from function return
function getUser() {
    return { name: "Billy", age: 33 };
}
const user = getUser();  // inferred as { name: string, age: number }

// Best practice: Let TS infer when obvious
let numbers = [1, 2, 3];  // inferred as number[]

// Explicit when needed
let items: string[] = [];  // Can't infer from empty array
```

---

## 3. Objects & Interfaces

### Object Types
```typescript
// Inline type
let person: { name: string; age: number } = {
    name: "Billy",
    age: 33
};

// Optional properties
let user: { name: string; email?: string } = {
    name: "Billy"
    // email is optional
};

// Readonly properties
let config: { readonly apiKey: string } = {
    apiKey: "secret"
};
// config.apiKey = "new";  // ERROR!
```

### Interfaces (Preferred for Objects)
```typescript
interface Person {
    name: string;
    age: number;
    email?: string;           // Optional
    readonly id: number;      // Can't modify after creation
}

const person: Person = {
    name: "Billy",
    age: 33,
    id: 1
};

// person.id = 2;  // ERROR! readonly

// Index signatures (dynamic keys)
interface StringMap {
    [key: string]: string;
}

const colors: StringMap = {
    red: "#ff0000",
    blue: "#0000ff"
};
```

### Extending Interfaces
```typescript
interface Person {
    name: string;
    age: number;
}

interface Employee extends Person {
    job: string;
    salary: number;
}

const employee: Employee = {
    name: "Billy",
    age: 33,
    job: "Engineer",
    salary: 100000
};

// Multiple inheritance
interface Developer extends Person, Employee {
    languages: string[];
}
```

### Type Aliases (Alternative to Interfaces)
```typescript
// Similar to interface
type Person = {
    name: string;
    age: number;
};

// Can do things interfaces can't
type ID = string | number;  // Union
type Point = [number, number];  // Tuple
type Callback = (data: string) => void;  // Function

// Intersection (combine types)
type Employee = Person & {
    job: string;
};
```

### Interface vs Type
```typescript
// Use Interface for:
// - Object shapes
// - Classes
// - When you might extend later

// Use Type for:
// - Unions
// - Tuples
// - Function types
// - Computed properties
```

---

## 4. Functions

### Function Types
```typescript
// Function declaration
function add(a: number, b: number): number {
    return a + b;
}

// Arrow function
const add = (a: number, b: number): number => a + b;

// Function expression
const add: (a: number, b: number) => number = (a, b) => a + b;

// Type alias for function
type AddFn = (a: number, b: number) => number;
const add: AddFn = (a, b) => a + b;
```

### Parameters
```typescript
// Optional parameters (must be last)
function greet(name: string, greeting?: string): string {
    return `${greeting || "Hello"}, ${name}`;
}

// Default parameters
function greet(name: string, greeting: string = "Hello"): string {
    return `${greeting}, ${name}`;
}

// Rest parameters
function sum(...numbers: number[]): number {
    return numbers.reduce((a, b) => a + b, 0);
}

// Destructured parameters
function printPerson({ name, age }: { name: string; age: number }) {
    console.log(`${name} is ${age}`);
}

// Or with interface
interface Person { name: string; age: number; }
function printPerson({ name, age }: Person) {
    console.log(`${name} is ${age}`);
}
```

### Return Types
```typescript
// Explicit return type
function getUser(): { name: string; age: number } {
    return { name: "Billy", age: 33 };
}

// Inferred return type (preferred when obvious)
function getUser() {
    return { name: "Billy", age: 33 };
}

// Void (no return)
function log(msg: string): void {
    console.log(msg);
}

// Never (never returns)
function error(msg: string): never {
    throw new Error(msg);
}
```

---

## 5. Union & Literal Types

### Union Types (OR)
```typescript
// Can be string OR number
let id: string | number;
id = "abc123";  // OK
id = 42;        // OK
// id = true;   // ERROR!

// Function with union param
function printId(id: string | number) {
    console.log(id);
}

// Union with null
let name: string | null = null;
name = "Billy";
```

### Type Narrowing (Checking Union Types)
```typescript
function printId(id: string | number) {
    if (typeof id === "string") {
        // TypeScript knows id is string here
        console.log(id.toUpperCase());
    } else {
        // TypeScript knows id is number here
        console.log(id * 2);
    }
}

// Array check
function process(value: string | string[]) {
    if (Array.isArray(value)) {
        value.forEach(s => console.log(s));  // string[]
    } else {
        console.log(value.toUpperCase());    // string
    }
}

// Null check
function greet(name: string | null) {
    if (name === null) {
        console.log("Hello, Guest");
    } else {
        console.log(`Hello, ${name}`);
    }
}
```

### Literal Types (Exact Values)
```typescript
// String literals
type Direction = "north" | "south" | "east" | "west";
let dir: Direction = "north";  // OK
// dir = "up";  // ERROR! Must be one of the 4

// Number literals
type DiceRoll = 1 | 2 | 3 | 4 | 5 | 6;
let roll: DiceRoll = 4;  // OK

// Boolean literal (rare)
type AlwaysTrue = true;

// Combined with union
type Status = "loading" | "success" | "error";
type Response = { status: Status; data?: any };
```

---

## 6. Generics (Type Variables)

### Generic Functions
```typescript
// Generic function (works with any type)
function identity<T>(arg: T): T {
    return arg;
}

identity<string>("hello");  // Explicit type
identity(42);               // Inferred as number

// Generic array function
function firstElement<T>(arr: T[]): T | undefined {
    return arr[0];
}

const first = firstElement([1, 2, 3]);  // number | undefined
const first2 = firstElement(["a", "b"]); // string | undefined

// Multiple type parameters
function pair<K, V>(key: K, value: V): [K, V] {
    return [key, value];
}

pair<string, number>("age", 33);  // [string, number]
pair("name", "Billy");             // Inferred
```

### Generic Interfaces
```typescript
interface Box<T> {
    value: T;
}

let stringBox: Box<string> = { value: "hello" };
let numberBox: Box<number> = { value: 42 };

// Generic with multiple types
interface Pair<K, V> {
    key: K;
    value: V;
}

let pair: Pair<string, number> = { key: "age", value: 33 };

// Response type example
interface ApiResponse<T> {
    data: T;
    status: number;
    error?: string;
}

const userResponse: ApiResponse<User> = {
    data: { name: "Billy", age: 33 },
    status: 200
};
```

### Generic Constraints
```typescript
// Constraint: T must have length property
function getLength<T extends { length: number }>(item: T): number {
    return item.length;
}

getLength("hello");      // OK (string has length)
getLength([1, 2, 3]);    // OK (array has length)
// getLength(42);        // ERROR! number has no length

// Constraint: T must be object
function merge<T extends object, U extends object>(obj1: T, obj2: U) {
    return { ...obj1, ...obj2 };
}

// Constraint: K must be key of T
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

const person = { name: "Billy", age: 33 };
getProperty(person, "name");  // OK
// getProperty(person, "job");  // ERROR! "job" not in person
```

---

## 7. Type Guards & Type Predicates

### typeof (Primitive Types)
```typescript
function process(value: string | number) {
    if (typeof value === "string") {
        return value.toUpperCase();
    }
    return value * 2;
}
```

### instanceof (Class Instances)
```typescript
class Dog {
    bark() { console.log("Woof!"); }
}

class Cat {
    meow() { console.log("Meow!"); }
}

function makeSound(animal: Dog | Cat) {
    if (animal instanceof Dog) {
        animal.bark();
    } else {
        animal.meow();
    }
}
```

### in (Property Checking)
```typescript
interface Bird {
    fly(): void;
}

interface Fish {
    swim(): void;
}

function move(animal: Bird | Fish) {
    if ("fly" in animal) {
        animal.fly();
    } else {
        animal.swim();
    }
}
```

### Custom Type Guards (Type Predicates)
```typescript
interface Cat { meow(): void; }
interface Dog { bark(): void; }

// Type predicate: pet is Dog
function isDog(pet: Cat | Dog): pet is Dog {
    return (pet as Dog).bark !== undefined;
}

function makeSound(pet: Cat | Dog) {
    if (isDog(pet)) {
        pet.bark();  // TypeScript knows it's Dog
    } else {
        pet.meow();  // TypeScript knows it's Cat
    }
}

// Another example
function isString(value: unknown): value is string {
    return typeof value === "string";
}

function process(value: unknown) {
    if (isString(value)) {
        console.log(value.toUpperCase());  // value is string
    }
}
```

---

## 8. Utility Types (Built-in Type Helpers)

### Partial (Make all properties optional)
```typescript
interface User {
    name: string;
    age: number;
    email: string;
}

// All properties become optional
type PartialUser = Partial<User>;
// { name?: string; age?: number; email?: string }

function updateUser(user: User, updates: Partial<User>) {
    return { ...user, ...updates };
}

updateUser(user, { age: 34 });  // Only update age
```

### Required (Make all properties required)
```typescript
interface User {
    name?: string;
    age?: number;
}

type RequiredUser = Required<User>;
// { name: string; age: number }
```

### Readonly (Make all properties readonly)
```typescript
interface User {
    name: string;
    age: number;
}

type ReadonlyUser = Readonly<User>;
const user: ReadonlyUser = { name: "Billy", age: 33 };
// user.age = 34;  // ERROR!
```

### Pick (Select specific properties)
```typescript
interface User {
    id: number;
    name: string;
    age: number;
    email: string;
}

// Only pick id and name
type UserPreview = Pick<User, "id" | "name">;
// { id: number; name: string }
```

### Omit (Remove specific properties)
```typescript
interface User {
    id: number;
    name: string;
    age: number;
    password: string;
}

// Remove password
type PublicUser = Omit<User, "password">;
// { id: number; name: string; age: number }
```

### Record (Create object type with specific keys)
```typescript
// Keys are strings, values are numbers
type Scores = Record<string, number>;
const scores: Scores = {
    math: 95,
    english: 87
};

// Keys are specific strings
type Roles = Record<"admin" | "user" | "guest", boolean>;
const permissions: Roles = {
    admin: true,
    user: true,
    guest: false
};
```

### ReturnType (Extract function return type)
```typescript
function getUser() {
    return { name: "Billy", age: 33 };
}

type User = ReturnType<typeof getUser>;
// { name: string; age: number }
```

### Parameters (Extract function parameter types)
```typescript
function greet(name: string, age: number) {
    return `Hello ${name}, age ${age}`;
}

type GreetParams = Parameters<typeof greet>;
// [string, number]
```

---

## 9. Enums

### Numeric Enums
```typescript
enum Direction {
    Up,      // 0
    Down,    // 1
    Left,    // 2
    Right    // 3
}

let dir: Direction = Direction.Up;

// Custom values
enum Status {
    Pending = 1,
    Approved = 2,
    Rejected = 3
}
```

### String Enums (Preferred)
```typescript
enum Direction {
    Up = "UP",
    Down = "DOWN",
    Left = "LEFT",
    Right = "RIGHT"
}

let dir: Direction = Direction.Up;  // "UP"

// Better for debugging (shows string, not number)
console.log(Direction.Up);  // "UP" instead of 0
```

### Const Enums (Inlined at compile time)
```typescript
const enum Direction {
    Up = "UP",
    Down = "DOWN"
}

// More performant, but can't be iterated
```

---

## 10. Classes with TypeScript

### Basic Class
```typescript
class Person {
    // Properties (public by default)
    name: string;
    age: number;
    
    constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
    }
    
    greet(): string {
        return `Hello, I'm ${this.name}`;
    }
}

const person = new Person("Billy", 33);
```

### Access Modifiers
```typescript
class Person {
    public name: string;      // Accessible everywhere (default)
    private age: number;      // Only inside class
    protected id: number;     // Inside class and subclasses
    readonly created: Date;   // Can't be modified after init
    
    constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
        this.id = Math.random();
        this.created = new Date();
    }
    
    // Private method
    private getAge(): number {
        return this.age;
    }
}

// Shorthand (same as above)
class Person {
    readonly created = new Date();
    
    constructor(
        public name: string,
        private age: number,
        protected id: number
    ) {}
}
```

### Inheritance
```typescript
class Animal {
    constructor(public name: string) {}
    
    move(distance: number): void {
        console.log(`${this.name} moved ${distance}m`);
    }
}

class Dog extends Animal {
    constructor(name: string, public breed: string) {
        super(name);  // Call parent constructor
    }
    
    bark(): void {
        console.log("Woof!");
    }
    
    // Override parent method
    move(distance: number): void {
        console.log("Running...");
        super.move(distance);
    }
}
```

### Abstract Classes
```typescript
abstract class Shape {
    abstract area(): number;  // Must be implemented by subclass
    
    describe(): string {
        return `Area is ${this.area()}`;
    }
}

class Circle extends Shape {
    constructor(public radius: number) {
        super();
    }
    
    area(): number {
        return Math.PI * this.radius ** 2;
    }
}

// const shape = new Shape();  // ERROR! Can't instantiate abstract
const circle = new Circle(5);
```

### Implementing Interfaces
```typescript
interface Drawable {
    draw(): void;
}

interface Resizable {
    resize(scale: number): void;
}

class Rectangle implements Drawable, Resizable {
    constructor(public width: number, public height: number) {}
    
    draw(): void {
        console.log("Drawing rectangle");
    }
    
    resize(scale: number): void {
        this.width *= scale;
        this.height *= scale;
    }
}
```

---

## Quick TypeScript Tips for Tests

1. **Let TypeScript infer** when obvious, explicit when needed
2. **Use interfaces** for object shapes
3. **Use type aliases** for unions, tuples, function types
4. **Generics** make functions/classes reusable with type safety
5. **Utility types** (Partial, Pick, Omit) save time
6. **Type guards** (`typeof`, `instanceof`, `in`) narrow types
7. **Strict null checks**: use `string | null` for nullable values
8. **Optional chaining**: `user?.address?.city`
9. **Nullish coalescing**: `value ?? default`
10. **const enums** for better performance
11. **Readonly** for immutable data
12. **never** for functions that never return
13. **unknown** safer than `any`
14. **Type predicates** (`pet is Dog`) for custom guards
15. **ReturnType** to extract function return types

---

## Common TypeScript Patterns for Tests

### Type-Safe API Response
```typescript
interface ApiResponse<T> {
    data: T;
    status: number;
    error?: string;
}

async function fetchUser(id: number): Promise<ApiResponse<User>> {
    const response = await fetch(`/api/users/${id}`);
    return response.json();
}
```

### Discriminated Unions (Tagged Union)
```typescript
interface Loading {
    type: "loading";
}

interface Success {
    type: "success";
    data: string;
}

interface Error {
    type: "error";
    error: string;
}

type State = Loading | Success | Error;

function handleState(state: State) {
    switch (state.type) {
        case "loading":
            console.log("Loading...");
            break;
        case "success":
            console.log(state.data);  // TypeScript knows data exists
            break;
        case "error":
            console.log(state.error);  // TypeScript knows error exists
            break;
    }
}
```

### Builder Pattern
```typescript
class QueryBuilder {
    private query = "";
    
    select(fields: string[]): this {
        this.query += `SELECT ${fields.join(", ")}`;
        return this;
    }
    
    from(table: string): this {
        this.query += ` FROM ${table}`;
        return this;
    }
    
    where(condition: string): this {
        this.query += ` WHERE ${condition}`;
        return this;
    }
    
    build(): string {
        return this.query;
    }
}

const query = new QueryBuilder()
    .select(["name", "age"])
    .from("users")
    .where("age > 18")
    .build();
```

---

## Related Notes

- [JavaScript Essentials for Coding Tests](JavaScript-Essentials-for-Coding-Tests) - JavaScript fundamentals
- [Python Variables & Data Types](Python-Variables-&-Data-Types) - Similar type concepts
- [Common Algorithms for Coding Tests](Common-Algorithms-for-Coding-Tests) - Language-agnostic patterns
- [VS Code Shortcuts & Productivity](VS-Code-Shortcuts-&-Productivity) - TypeScript debugging

---

**Use this note when:**
- Preparing for TypeScript coding interviews
- Adding type safety to JavaScript projects
- Need quick reference for generics and utility types
- Working with React/Angular/Node.js TypeScript projects
- Learning type system and type guards
