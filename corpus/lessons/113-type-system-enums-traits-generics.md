---
title: "11.3 — Type System: Enums, Traits & Generics"
subject: "Rust"
catalog: advanced
audience_tier: higher-education
chapter: "11.3"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 11.3 — Type System: Enums, Traits & Generics

> *"Rust's type system is designed to make illegal states unrepresentable."* — Niko Matsakis

Python uses duck typing — if it quacks, it's a duck. Rust uses **static dispatch** — the compiler knows exactly what type everything is, generates specialized code for each concrete type, and catches type errors before your code ever runs. The result: zero runtime overhead for abstraction.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Model domains with enums (algebraic data types / tagged unions).
2. Use exhaustive pattern matching (`match`, `if let`, `while let`).
3. Define and implement traits (Rust's interface system).
4. Write generic functions and structs with trait bounds.
5. Understand monomorphization vs. dynamic dispatch (trait objects).
6. Use associated types, default implementations, and supertraits.

---

## 🖼️ Visual Anchor — Rust Type System Architecture

![rust__14.3-fig1](rust__14.3-fig1.svg)

---

## 📚 1. Concepts

### Concept 14.3.1 — Enums (Algebraic Data Types)

Rust enums are **tagged unions** — each variant can hold different data. This is fundamentally different from C/Python enums (which are just named integers):

```rust
// Python enum: just named constants
// class Direction(Enum):
//     North = 1
//     South = 2

// Rust enum: each variant can hold different data
enum Message {
    Quit,                          // No data (unit variant)
    Move { x: i32, y: i32 },      // Named fields (struct variant)
    Write(String),                 // Unnamed field (tuple variant)
    ChangeColor(u8, u8, u8),      // Multiple unnamed fields
}

// The compiler knows the exact size: max(variant sizes) + discriminant tag
```

### Concept 14.3.2 — Pattern Matching

`match` is exhaustive — you must handle every variant:

```rust
fn process_message(msg: Message) {
    match msg {
        Message::Quit => {
            println!("Quitting");
        }
        Message::Move { x, y } => {
            println!("Moving to ({x}, {y})");
        }
        Message::Write(text) => {
            println!("Writing: {text}");
        }
        Message::ChangeColor(r, g, b) => {
            println!("Color: #{r:02x}{g:02x}{b:02x}");
        }
    }
}
```

**Exhaustiveness is a superpower.** When you add a new variant to an enum, the compiler tells you every place in your codebase that needs updating. Python's `match` (3.10+) doesn't enforce this.

### Concept 14.3.3 — Option<T> and the Billion-Dollar Mistake

Rust has no `null`. Instead, optional values are encoded in the type system:

```rust
enum Option<T> {
    Some(T),    // Value present
    None,       // Value absent
}

fn find_user(id: u64) -> Option<User> {
    if id == 1 {
        Some(User { name: String::from("Bill") })
    } else {
        None  // No null pointer — the TYPE tells you it might be absent
    }
}

fn main() {
    let user = find_user(1);
    // user.name;  // ❌ Can't access directly — must handle None
    match user {
        Some(u) => println!("Found: {}", u.name),
        None => println!("User not found"),
    }

    // Or use if let for single-variant matching:
    if let Some(u) = find_user(1) {
        println!("Found: {}", u.name);
    }
}
```

### Concept 14.3.4 — Traits (Interfaces + Default Implementations)

Traits define shared behavior:

```rust
trait Drawable {
    // Required method (no body — implementors must provide)
    fn draw(&self, x: f32, y: f32);

    // Default method (implementors can override)
    fn bounding_box(&self) -> (f32, f32, f32, f32) {
        (0.0, 0.0, 100.0, 100.0)  // Default implementation
    }

    // Associated constant
    const MAX_SIZE: f32 = 1024.0;
}

struct Circle {
    radius: f32,
    center: (f32, f32),
}

impl Drawable for Circle {
    fn draw(&self, x: f32, y: f32) {
        println!("Drawing circle at ({x}, {y}) with radius {}", self.radius);
    }

    fn bounding_box(&self) -> (f32, f32, f32, f32) {
        let (cx, cy) = self.center;
        (cx - self.radius, cy - self.radius,
         cx + self.radius, cy + self.radius)
    }
}
```

### Concept 14.3.5 — Generics

```rust
// Generic function — works for any type T that implements PartialOrd
fn largest<T: PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];
    for item in &list[1..] {
        if item > largest {
            largest = item;
        }
    }
    largest
}

// Generic struct
struct Point<T> {
    x: T,
    y: T,
}

// Generic impl
impl<T: std::fmt::Display> Point<T> {
    fn print(&self) {
        println!("({}, {})", self.x, self.y);
    }
}

// Multiple type parameters
struct Pair<K, V> {
    key: K,
    value: V,
}
```

### Concept 14.3.6 — Monomorphization (Zero-Cost Generics)

When you write generic code, the compiler generates **specialized versions** for each concrete type used:

```rust
fn add<T: std::ops::Add<Output = T>>(a: T, b: T) -> T {
    a + b
}

fn main() {
    add(1i32, 2i32);     // Compiler generates: fn add_i32(a: i32, b: i32) -> i32
    add(1.0f64, 2.0f64); // Compiler generates: fn add_f64(a: f64, b: f64) -> f64
}
```

**This is why Rust generics have zero runtime cost** — by the time the binary runs, all generic code has been replaced with concrete, specialized machine code. No vtable lookup, no type erasure.

---

## 📐 2. Mental Models

### Model 14.3.1 — Enums as State Machines

Enums naturally model state machines where each state carries different data:

```rust
enum ConnectionState {
    Disconnected,
    Connecting { address: String, attempt: u32 },
    Connected { socket: TcpStream, latency_ms: u32 },
    Error { message: String, retries_left: u32 },
}

// The type system PREVENTS you from accessing socket when disconnected
// No runtime checks needed — illegal states are unrepresentable
```

### Model 14.3.2 — Traits as Capabilities

Think of traits as **capabilities** you can attach to types:

```rust
// A type that implements Display can be printed with {}
// A type that implements Clone can be duplicated
// A type that implements Send can be sent to another thread
// A type that implements Iterator can be used in for loops

// Trait bounds = "this function requires these capabilities"
fn process<T: Clone + Display + Send>(item: T) {
    let backup = item.clone();  // Requires Clone
    println!("{item}");          // Requires Display
    send_to_thread(item);       // Requires Send
}
```

### Model 14.3.3 — Static vs Dynamic Dispatch

```rust
// STATIC DISPATCH (generics) — resolved at compile time
fn draw_static(item: &impl Drawable) {
    item.draw(0.0, 0.0);
    // Compiler knows exact type → direct function call → FAST
}

// DYNAMIC DISPATCH (trait objects) — resolved at runtime
fn draw_dynamic(item: &dyn Drawable) {
    item.draw(0.0, 0.0);
    // Compiler doesn't know type → vtable lookup → slight overhead
}

// When to use which:
// Static: performance-critical code, when types are known at compile time
// Dynamic: heterogeneous collections, plugin systems, when you need type erasure
```

---

## 🔑 3. Mechanics

### 3.1 — Advanced Pattern Matching

```rust
fn classify_number(n: i32) -> &'static str {
    match n {
        0 => "zero",
        1..=9 => "single digit",
        10 | 20 | 30 => "round tens",
        n if n < 0 => "negative",       // Guard clause
        n if n % 2 == 0 => "even",
        _ => "odd",                      // Catch-all
    }
}

// Destructuring nested structures
struct Point { x: f64, y: f64 }
enum Shape {
    Circle { center: Point, radius: f64 },
    Rect { top_left: Point, bottom_right: Point },
}

fn area(shape: &Shape) -> f64 {
    match shape {
        Shape::Circle { radius, .. } => std::f64::consts::PI * radius * radius,
        Shape::Rect {
            top_left: Point { x: x1, y: y1 },
            bottom_right: Point { x: x2, y: y2 },
        } => (x2 - x1).abs() * (y2 - y1).abs(),
    }
}

// if let / while let for single-variant matching
fn process_queue(queue: &mut VecDeque<Message>) {
    while let Some(msg) = queue.pop_front() {
        handle(msg);
    }
}

// let-else (Rust 1.65+) — early return on pattern mismatch
fn get_count(data: &HashMap<String, Value>) -> u64 {
    let Some(Value::Number(n)) = data.get("count") else {
        return 0;  // Early return if pattern doesn't match
    };
    n.as_u64().unwrap_or(0)
}
```

### 3.2 — Trait Bounds (Multiple Syntaxes)

```rust
// Syntax 1: Inline bound
fn print_item<T: Display + Debug>(item: T) {
    println!("{item} (debug: {item:?})");
}

// Syntax 2: where clause (cleaner for complex bounds)
fn complex_function<T, U>(t: T, u: U) -> String
where
    T: Display + Clone + Send + 'static,
    U: IntoIterator<Item = T>,
{
    format!("{t}")
}

// Syntax 3: impl Trait (in argument position — sugar for generics)
fn print_anything(item: &impl Display) {
    println!("{item}");
}

// Syntax 4: impl Trait (in return position — opaque type)
fn make_adder(x: i32) -> impl Fn(i32) -> i32 {
    move |y| x + y  // Returns a closure — caller doesn't know the exact type
}
```

### 3.3 — Associated Types vs Generic Parameters

```rust
// Generic trait: Iterator could yield different types for same implementor
// (Not what we want — a Vec<i32> iterator always yields i32)
trait BadIterator<T> {
    fn next(&mut self) -> Option<T>;
}

// Associated type: each implementor specifies ONE concrete type
trait Iterator {
    type Item;  // Associated type — determined by the implementor
    fn next(&mut self) -> Option<Self::Item>;
}

impl Iterator for Counter {
    type Item = u32;  // Counter always yields u32
    fn next(&mut self) -> Option<u32> {
        self.count += 1;
        if self.count <= 5 { Some(self.count) } else { None }
    }
}

// Rule of thumb:
// - Use associated types when there's ONE natural choice per implementor
// - Use generic parameters when the same type could implement the trait multiple ways
```

### 3.4 — Trait Objects and Object Safety

```rust
// Trait objects: &dyn Trait or Box<dyn Trait>
// Enable heterogeneous collections:
fn draw_all(shapes: &[Box<dyn Drawable>]) {
    for shape in shapes {
        shape.draw(0.0, 0.0);  // Dynamic dispatch via vtable
    }
}

fn main() {
    let shapes: Vec<Box<dyn Drawable>> = vec![
        Box::new(Circle { radius: 5.0, center: (0.0, 0.0) }),
        Box::new(Rectangle { width: 10.0, height: 20.0 }),
    ];
    draw_all(&shapes);
}

// OBJECT SAFETY: A trait is object-safe if:
// 1. It doesn't have methods that return Self
// 2. It doesn't have generic methods
// 3. It doesn't require Sized

// ❌ NOT object-safe:
trait Cloneable {
    fn clone(&self) -> Self;  // Returns Self — can't use as dyn Cloneable
}

// ✅ Object-safe:
trait Drawable {
    fn draw(&self, x: f32, y: f32);  // &self, no Self in return, no generics
}
```

### 3.5 — Supertraits and Trait Inheritance

```rust
// Supertrait: Display requires that implementors also implement fmt::Debug
trait PrettyPrint: std::fmt::Display + std::fmt::Debug {
    fn pretty(&self) -> String {
        format!("[PRETTY] {self}")  // Can use Display because it's a supertrait
    }
}

// Implementors must implement ALL supertraits:
struct Name(String);

impl std::fmt::Display for Name {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl std::fmt::Debug for Name {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "Name({:?})", self.0)
    }
}

impl PrettyPrint for Name {}  // Gets default pretty() implementation
```

### 3.6 — Derive Macros (Auto-Implementing Traits)

```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Player {
    name: String,
    score: u32,
    level: u8,
}

// derive generates implementations automatically:
// Debug  → can use {:?} formatting
// Clone  → can call .clone()
// PartialEq/Eq → can use == and !=
// Hash   → can use as HashMap key

// Common derives:
// #[derive(Debug)]           — Almost always
// #[derive(Clone)]           — When you need copies
// #[derive(PartialEq, Eq)]   — When you need equality
// #[derive(Hash)]            — When used as map keys
// #[derive(Default)]         — When you need a zero/empty value
// #[derive(serde::Serialize, serde::Deserialize)]  — JSON/TOML/etc
```

---

## 💡 4. Worked Examples

### Example 11.3.1 — Modeling a Game Entity System

```rust
use std::collections::HashMap;

#[derive(Debug, Clone)]
enum Component {
    Position { x: f32, y: f32 },
    Velocity { dx: f32, dy: f32 },
    Health { current: u32, max: u32 },
    Sprite { texture_id: u32, width: u32, height: u32 },
    Collider { radius: f32 },
}

type EntityId = u64;

struct World {
    next_id: EntityId,
    entities: HashMap<EntityId, Vec<Component>>,
}

impl World {
    fn new() -> Self {
        World { next_id: 0, entities: HashMap::new() }
    }

    fn spawn(&mut self, components: Vec<Component>) -> EntityId {
        let id = self.next_id;
        self.next_id += 1;
        self.entities.insert(id, components);
        id
    }

    fn get_position(&self, id: EntityId) -> Option<(f32, f32)> {
        self.entities.get(&id)?.iter().find_map(|c| {
            if let Component::Position { x, y } = c {
                Some((*x, *y))
            } else {
                None
            }
        })
    }
}

fn main() {
    let mut world = World::new();
    let player = world.spawn(vec![
        Component::Position { x: 0.0, y: 0.0 },
        Component::Velocity { dx: 1.0, dy: 0.0 },
        Component::Health { current: 100, max: 100 },
        Component::Sprite { texture_id: 1, width: 64, height: 64 },
    ]);

    if let Some((x, y)) = world.get_position(player) {
        println!("Player at ({x}, {y})");
    }
}
```

### Example 11.3.2 — Trait-Based Plugin System

```rust
trait Plugin: Send + Sync {
    fn name(&self) -> &str;
    fn on_startup(&mut self) {}
    fn on_update(&mut self, delta_time: f32);
    fn on_shutdown(&mut self) {}
}

struct PhysicsPlugin {
    gravity: f32,
}

impl Plugin for PhysicsPlugin {
    fn name(&self) -> &str { "Physics" }

    fn on_update(&mut self, dt: f32) {
        println!("Physics step: gravity={}, dt={dt}", self.gravity);
    }
}

struct AudioPlugin {
    volume: f32,
}

impl Plugin for AudioPlugin {
    fn name(&self) -> &str { "Audio" }

    fn on_update(&mut self, _dt: f32) {
        println!("Audio mix at volume {}", self.volume);
    }
}

struct App {
    plugins: Vec<Box<dyn Plugin>>,
}

impl App {
    fn new() -> Self { App { plugins: vec![] } }

    fn add_plugin(&mut self, plugin: Box<dyn Plugin>) {
        println!("Registered plugin: {}", plugin.name());
        self.plugins.push(plugin);
    }

    fn run(&mut self) {
        for plugin in &mut self.plugins {
            plugin.on_startup();
        }
        // Game loop
        for _ in 0..3 {
            for plugin in &mut self.plugins {
                plugin.on_update(0.016);
            }
        }
        for plugin in &mut self.plugins {
            plugin.on_shutdown();
        }
    }
}
```

### Example 11.3.3 — Generic Data Pipeline

```rust
trait Transform {
    type Input;
    type Output;
    fn transform(&self, input: Self::Input) -> Self::Output;
}

struct Uppercase;
impl Transform for Uppercase {
    type Input = String;
    type Output = String;
    fn transform(&self, input: String) -> String {
        input.to_uppercase()
    }
}

struct ParseInt;
impl Transform for ParseInt {
    type Input = String;
    type Output = Result<i64, std::num::ParseIntError>;
    fn transform(&self, input: String) -> Self::Output {
        input.trim().parse()
    }
}

// Chain transforms with generics
struct Chain<A, B> {
    first: A,
    second: B,
}

impl<A, B> Transform for Chain<A, B>
where
    A: Transform,
    B: Transform<Input = A::Output>,
{
    type Input = A::Input;
    type Output = B::Output;

    fn transform(&self, input: Self::Input) -> Self::Output {
        let intermediate = self.first.transform(input);
        self.second.transform(intermediate)
    }
}
```

---

## ⚠️ 5. Gotchas & Common Mistakes

### Gotcha 14.3.1 — Enum Size Optimization

```rust
// Rust optimizes enum layout. Option<&T> is the SAME size as &T
// because references can never be null, so None uses the null bit pattern.
use std::mem::size_of;

assert_eq!(size_of::<&str>(), size_of::<Option<&str>>());  // Both 16 bytes!
assert_eq!(size_of::<Box<i32>>(), size_of::<Option<Box<i32>>>());  // Both 8 bytes!

// But Option<i32> is LARGER than i32 (needs space for discriminant):
assert_eq!(size_of::<i32>(), 4);
assert_eq!(size_of::<Option<i32>>(), 8);  // 4 bytes data + 4 bytes tag
```

### Gotcha 14.3.2 — Orphan Rule

You can only implement a trait for a type if **either the trait or the type is defined in your crate**:

```rust
// ✅ Your trait, foreign type:
trait MyTrait { fn foo(&self); }
impl MyTrait for Vec<i32> { fn foo(&self) {} }

// ✅ Foreign trait, your type:
struct MyType;
impl std::fmt::Display for MyType {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "MyType")
    }
}

// ❌ Foreign trait, foreign type:
// impl std::fmt::Display for Vec<i32> { ... }  // COMPILE ERROR

// Workaround: Newtype pattern (see Chapter 11.7)
struct Wrapper(Vec<i32>);
impl std::fmt::Display for Wrapper {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "[{}]", self.0.iter().map(|n| n.to_string()).collect::<Vec<_>>().join(", "))
    }
}
```

### Gotcha 14.3.3 — Trait Object Limitations

```rust
// Can't use generics in trait object methods:
trait Serializer {
    fn serialize<T: serde::Serialize>(&self, value: &T) -> Vec<u8>;
    // ❌ Can't make Box<dyn Serializer> — generic method not object-safe
}

// Fix: Use associated types or concrete types:
trait Serializer {
    fn serialize(&self, value: &dyn erased_serde::Serialize) -> Vec<u8>;
    // ✅ Object-safe — no generics in method signature
}
```

### Gotcha 14.3.4 — `impl Trait` in Return Position

```rust
// impl Trait in return position = opaque type (caller can't name it)
fn make_iter() -> impl Iterator<Item = i32> {
    (0..10).filter(|x| x % 2 == 0)
    // Caller knows it's an Iterator<Item = i32> but not the exact type
}

// ⚠️ All return paths must return the SAME concrete type:
fn make_iter_bad(ascending: bool) -> impl Iterator<Item = i32> {
    if ascending {
        (0..10).into_iter()  // This is std::ops::Range<i32>
    } else {
        (0..10).rev()        // ❌ This is Rev<Range<i32>> — different type!
    }
}

// Fix: Use Box<dyn Iterator> for heterogeneous returns:
fn make_iter_fixed(ascending: bool) -> Box<dyn Iterator<Item = i32>> {
    if ascending {
        Box::new(0..10)
    } else {
        Box::new((0..10).rev())
    }
}
```

---

## 🔗 6. Cross-Links

- **Next**: [11.4 - Error Handling - Result, Option, ? Operator](11.4---Error-Handling---Result,-Option,-?-Operator) — Result<T,E> is just an enum!
- **Patterns chapter**: [11.7 - Idiomatic Rust - Patterns, Anti-patterns & Performance](11.7---Idiomatic-Rust---Patterns,-Anti-patterns-&-Performance) — Newtype, Builder, Typestate
- **Python protocols**: [08.3 - OOP, Data Models & Pythonic Idioms](08.3---OOP,-Data-Models-&-Pythonic-Idioms) — Traits are Rust's version of Python's Protocol
- **Game dev ECS**: [11.8 - Production Rust - WebAssembly, FFI, Embedded & Game Dev (Bevy)](11.8---Production-Rust---WebAssembly,-FFI,-Embedded-&-Game-Dev-(Bevy)) — Bevy uses traits extensively

---

## 📖 7. References

- [The Rust Book, Ch. 6: Enums and Pattern Matching](https://doc.rust-lang.org/book/ch06-00-enums.html)
- [The Rust Book, Ch. 10: Generic Types, Traits, and Lifetimes](https://doc.rust-lang.org/book/ch10-00-generics.html)
- [The Rust Book, Ch. 17: Object-Oriented Features](https://doc.rust-lang.org/book/ch17-00-oop.html)
- [Jon Gjengset: "Crust of Rust: Dispatch and Fat Pointers"](https://www.youtube.com/watch?v=xcygqF5LVmM)
- [Rust by Example: Traits](https://doc.rust-lang.org/rust-by-example/trait.html)


---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — Generic Associated Types (GATs) with a Streaming Iterator

**Problem:** Implement a `StreamingIterator` trait where `next()` returns a reference that borrows from the iterator itself (not possible with the standard `Iterator` trait). This is the motivating example for GATs (stabilized in Rust 1.65).

<details>
<summary>🔍 Full step-by-step solution</summary>

```rust
// === THE PROBLEM WITH STANDARD ITERATOR ===
// Standard Iterator: type Item is fixed, can't borrow from self
// trait Iterator {
//     type Item;
//     fn next(&mut self) -> Option<Self::Item>;
// }
// 
// You CAN'T do: type Item = &'??? [u8];
// because there's no lifetime to tie it to &mut self.

// === GATs SOLVE THIS ===
// GAT = Generic Associated Type: associated type with its own generic parameters

trait StreamingIterator {
    type Item<'a> where Self: 'a;  // ← GAT: Item is parameterized by lifetime
    
    fn next(&mut self) -> Option<Self::Item<'_>>;
    //                                     ^^^ borrows from self
}

// === EXAMPLE: Windows iterator that yields overlapping slices ===
struct WindowsIter<'data> {
    data: &'data [u8],
    window_size: usize,
    position: usize,
}

impl<'data> WindowsIter<'data> {
    fn new(data: &'data [u8], window_size: usize) -> Self {
        WindowsIter { data, window_size, position: 0 }
    }
}

impl<'data> StreamingIterator for WindowsIter<'data> {
    type Item<'a> = &'a [u8] where Self: 'a;
    
    fn next(&mut self) -> Option<Self::Item<'_>> {
        if self.position + self.window_size <= self.data.len() {
            let window = &self.data[self.position..self.position + self.window_size];
            self.position += 1;
            Some(window)
        } else {
            None
        }
    }
}

// === MORE POWERFUL EXAMPLE: Lending iterator over mutable data ===
trait LendingIterator {
    type Item<'a> where Self: 'a;
    
    fn next(&mut self) -> Option<Self::Item<'_>>;
    
    // GATs enable higher-kinded-type-like patterns:
    fn for_each(mut self, mut f: impl FnMut(Self::Item<'_>))
    where
        Self: Sized,
    {
        while let Some(item) = self.next() {
            f(item);
        }
    }
}

// Mutable chunks iterator — yields &mut [T] slices from a Vec
struct MutChunks<'a, T> {
    data: &'a mut [T],
    chunk_size: usize,
}

impl<'a, T> LendingIterator for MutChunks<'a, T> {
    type Item<'item> = &'item mut [T] where Self: 'item;
    
    fn next(&mut self) -> Option<Self::Item<'_>> {
        if self.data.is_empty() {
            return None;
        }
        let chunk_size = self.chunk_size.min(self.data.len());
        // split_at_mut gives us two non-overlapping mutable slices
        let (chunk, rest) = std::mem::take(&mut self.data).split_at_mut(chunk_size);
        self.data = rest;
        Some(chunk)
    }
}

fn demo_gats() {
    let data: Vec<u8> = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    let mut iter = WindowsIter::new(&data, 3);
    
    while let Some(window) = iter.next() {
        println!("Window: {:?}", window);
    }
    // Output:
    // Window: [1, 2, 3]
    // Window: [2, 3, 4]
    // Window: [3, 4, 5]
    // ... etc
    
    // Mutable chunks:
    let mut data = vec![1, 2, 3, 4, 5, 6, 7, 8];
    let mut chunks = MutChunks { data: &mut data, chunk_size: 3 };
    
    chunks.for_each(|chunk| {
        for item in chunk.iter_mut() {
            *item *= 2;
        }
    });
    
    println!("After doubling: {:?}", data);
    // [2, 4, 6, 8, 10, 12, 14, 16]
}


// === WHY THIS MATTERS ===
// Before GATs, you had to choose between:
// 1. Collecting into owned data (allocation overhead)
// 2. Unsafe code with raw pointers
// 3. Callback-based APIs (less ergonomic)
//
// GATs enable zero-copy streaming APIs that are fully safe.
// Real-world uses:
// - Database cursors that yield rows borrowing from a buffer
// - Parser combinators that yield AST nodes borrowing from input
// - Network protocol decoders that yield frames from a read buffer
```

</details>

### Example 8.2 — Trait Objects vs Static Dispatch: Performance Comparison

**Problem:** Measure the actual performance difference between static dispatch (generics/monomorphization) and dynamic dispatch (trait objects/vtables). Demonstrate when each is appropriate.

<details>
<summary>🔍 Full step-by-step solution</summary>

```rust
// === SETUP: A trait with multiple implementations ===
trait Shape {
    fn area(&self) -> f64;
    fn perimeter(&self) -> f64;
}

#[derive(Clone)]
struct Circle { radius: f64 }
#[derive(Clone)]
struct Rectangle { width: f64, height: f64 }
#[derive(Clone)]
struct Triangle { a: f64, b: f64, c: f64 }

impl Shape for Circle {
    fn area(&self) -> f64 { std::f64::consts::PI * self.radius * self.radius }
    fn perimeter(&self) -> f64 { 2.0 * std::f64::consts::PI * self.radius }
}

impl Shape for Rectangle {
    fn area(&self) -> f64 { self.width * self.height }
    fn perimeter(&self) -> f64 { 2.0 * (self.width + self.height) }
}

impl Shape for Triangle {
    fn area(&self) -> f64 {
        let s = (self.a + self.b + self.c) / 2.0;
        (s * (s - self.a) * (s - self.b) * (s - self.c)).sqrt()
    }
    fn perimeter(&self) -> f64 { self.a + self.b + self.c }
}

// === STATIC DISPATCH (monomorphization) ===
// The compiler generates a specialized version for each concrete type.
fn total_area_static<S: Shape>(shapes: &[S]) -> f64 {
    shapes.iter().map(|s| s.area()).sum()
}
// Compiler generates:
// fn total_area_static_Circle(shapes: &[Circle]) -> f64 { ... }
// fn total_area_static_Rectangle(shapes: &[Rectangle]) -> f64 { ... }
// Each call is a direct function call — no indirection.

// === DYNAMIC DISPATCH (trait objects) ===
// Single function, uses vtable lookup at runtime.
fn total_area_dynamic(shapes: &[Box<dyn Shape>]) -> f64 {
    shapes.iter().map(|s| s.area()).sum()
}
// Each s.area() call:
// 1. Load vtable pointer from the fat pointer (8 bytes)
// 2. Index into vtable to find area() function pointer
// 3. Call through the function pointer
// Cost: ~2-5ns per call (cache miss on vtable = much worse)

// === ENUM DISPATCH (closed set, zero overhead) ===
#[derive(Clone)]
enum AnyShape {
    Circle(Circle),
    Rectangle(Rectangle),
    Triangle(Triangle),
}

impl AnyShape {
    fn area(&self) -> f64 {
        match self {
            AnyShape::Circle(c) => c.area(),
            AnyShape::Rectangle(r) => r.area(),
            AnyShape::Triangle(t) => t.area(),
        }
    }
}

fn total_area_enum(shapes: &[AnyShape]) -> f64 {
    shapes.iter().map(|s| s.area()).sum()
}
// Match compiles to a jump table or branch sequence.
// No pointer indirection — data is inline in the enum.
// Cache-friendly: all shapes stored contiguously in memory.

// === BENCHMARK RESULTS (typical, 1M shapes) ===
// Static dispatch (homogeneous Vec<Circle>):  ~1.2ms
// Enum dispatch (heterogeneous):              ~2.5ms
// Dynamic dispatch (Vec<Box<dyn Shape>>):     ~4.8ms
//
// The 2x difference between enum and dyn comes from:
// 1. Cache misses (Box puts each shape on a separate heap allocation)
// 2. Vtable indirection (prevents inlining)
// 3. Branch prediction (enum match is predictable; vtable call is not)

// === WHEN TO USE EACH ===
// 
// Static dispatch (generics):
//   ✅ Maximum performance (inlining, vectorization)
//   ✅ Zero runtime cost
//   ❌ Code bloat (each instantiation duplicates code)
//   ❌ Can't store heterogeneous collections
//   Use for: hot loops, numeric code, library APIs
//
// Enum dispatch:
//   ✅ Near-zero overhead (no heap allocation, cache-friendly)
//   ✅ Exhaustive matching (compiler catches missing variants)
//   ❌ Closed set (can't add variants without modifying the enum)
//   Use for: known set of types, state machines, AST nodes
//
// Dynamic dispatch (dyn Trait):
//   ✅ Open set (new types can be added without changing existing code)
//   ✅ Smaller binary (single function, not monomorphized)
//   ❌ Heap allocation per object (Box<dyn Trait>)
//   ❌ Vtable overhead (~2-5ns per call)
//   ❌ Prevents inlining and auto-vectorization
//   Use for: plugin systems, heterogeneous collections, type erasure

// === HYBRID: Enum for hot path, dyn for cold path ===
enum FastShape {
    Circle(Circle),
    Rectangle(Rectangle),
    // Fallback for rare/custom shapes:
    Other(Box<dyn Shape>),
}

impl FastShape {
    fn area(&self) -> f64 {
        match self {
            FastShape::Circle(c) => c.area(),        // Inlined
            FastShape::Rectangle(r) => r.area(),     // Inlined
            FastShape::Other(s) => s.area(),         // Dynamic (rare)
        }
    }
}
```

</details>

### Example 8.3 — Phantom Types for Compile-Time Unit Safety

**Problem:** Build a dimensional analysis system where the compiler prevents adding meters to seconds, multiplying incompatible units, or passing raw numbers where typed quantities are expected — all at zero runtime cost.

<details>
<summary>🔍 Full step-by-step solution</summary>

```rust
use std::marker::PhantomData;
use std::ops::{Add, Mul, Div};

// === UNIT MARKER TYPES (zero-sized, exist only at compile time) ===
struct Meters;
struct Seconds;
struct Kilograms;
struct MetersPerSecond;
struct MetersPerSecondSquared;
struct Newtons;

// === THE QUANTITY TYPE: value + phantom unit ===
#[derive(Debug, Clone, Copy, PartialEq, PartialOrd)]
struct Quantity<Unit> {
    value: f64,
    _unit: PhantomData<Unit>,
}

impl<U> Quantity<U> {
    fn new(value: f64) -> Self {
        Quantity { value, _unit: PhantomData }
    }
    
    fn raw(&self) -> f64 {
        self.value
    }
}

// === ADDITION: Only same units can be added ===
impl<U> Add for Quantity<U> {
    type Output = Self;
    fn add(self, rhs: Self) -> Self {
        Quantity::new(self.value + rhs.value)
    }
}

// === TYPE ALIASES for ergonomics ===
type Distance = Quantity<Meters>;
type Duration = Quantity<Seconds>;
type Mass = Quantity<Kilograms>;
type Speed = Quantity<MetersPerSecond>;
type Acceleration = Quantity<MetersPerSecondSquared>;
type Force = Quantity<Newtons>;

// === DIVISION: Distance / Duration = Speed ===
impl Div<Duration> for Distance {
    type Output = Speed;
    fn div(self, rhs: Duration) -> Speed {
        Quantity::new(self.value / rhs.value)
    }
}

// === Speed / Duration = Acceleration ===
impl Div<Duration> for Speed {
    type Output = Acceleration;
    fn div(self, rhs: Duration) -> Acceleration {
        Quantity::new(self.value / rhs.value)
    }
}

// === Mass * Acceleration = Force (F = ma) ===
impl Mul<Acceleration> for Mass {
    type Output = Force;
    fn mul(self, rhs: Acceleration) -> Force {
        Quantity::new(self.value * rhs.value)
    }
}

// === Constructor helpers ===
fn meters(v: f64) -> Distance { Quantity::new(v) }
fn seconds(v: f64) -> Duration { Quantity::new(v) }
fn kg(v: f64) -> Mass { Quantity::new(v) }

// === Display with units ===
impl std::fmt::Display for Distance {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{:.2} m", self.value)
    }
}
impl std::fmt::Display for Duration {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{:.2} s", self.value)
    }
}
impl std::fmt::Display for Speed {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{:.2} m/s", self.value)
    }
}
impl std::fmt::Display for Force {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{:.2} N", self.value)
    }
}

fn main() {
    let distance = meters(100.0);
    let time = seconds(9.58);  // Usain Bolt's 100m record
    
    let speed: Speed = distance / time;
    println!("Speed: {speed}");  // 10.44 m/s
    
    let mass = kg(86.0);  // Bolt's mass
    let accel: Acceleration = speed / seconds(3.0);  // Rough acceleration phase
    let force: Force = mass * accel;
    println!("Force: {force}");  // ~299.56 N
    
    // ✅ Same units can be added:
    let total_distance = meters(100.0) + meters(200.0);
    println!("Total: {total_distance}");  // 300.00 m
    
    // ❌ COMPILE ERROR: can't add meters to seconds
    // let nonsense = meters(5.0) + seconds(3.0);
    // error[E0308]: mismatched types
    //   expected `Quantity<Meters>`, found `Quantity<Seconds>`
    
    // ❌ COMPILE ERROR: can't divide seconds by meters (undefined unit)
    // let what = seconds(5.0) / meters(3.0);
    // error: no implementation for `Quantity<Seconds> / Quantity<Meters>`
}

// === ZERO RUNTIME COST ===
// PhantomData<Unit> is zero-sized.
// Quantity<Meters> has the exact same memory layout as f64.
// All type checking happens at compile time — the generated assembly
// is identical to raw f64 arithmetic.
//
// std::mem::size_of::<Quantity<Meters>>() == 8  (same as f64)
// std::mem::size_of::<PhantomData<Meters>>() == 0
```

</details>

### Example 8.4 — Typestate Pattern: TCP Connection State Machine

**Problem:** Model a TCP connection that can only be used in valid states. `connect()` should only be callable on a closed connection, `send()`/`recv()` only on an established connection, and `close()` transitions back to closed. Invalid transitions should be compile errors.

<details>
<summary>🔍 Full step-by-step solution</summary>

```rust
use std::marker::PhantomData;

// === STATE TYPES (zero-sized markers) ===
mod state {
    pub struct Closed;
    pub struct Listening;
    pub struct Established;
    pub struct TimeWait;
}

// === THE CONNECTION TYPE (parameterized by state) ===
struct TcpConnection<State> {
    local_addr: String,
    remote_addr: Option<String>,
    buffer: Vec<u8>,
    _state: PhantomData<State>,
}

// === METHODS AVAILABLE IN ALL STATES ===
impl<S> TcpConnection<S> {
    pub fn local_addr(&self) -> &str {
        &self.local_addr
    }
    
    pub fn remote_addr(&self) -> Option<&str> {
        self.remote_addr.as_deref()
    }
}

// === METHODS ONLY ON CLOSED CONNECTIONS ===
impl TcpConnection<state::Closed> {
    /// Create a new closed connection
    pub fn new(addr: &str) -> Self {
        TcpConnection {
            local_addr: addr.to_string(),
            remote_addr: None,
            buffer: Vec::new(),
            _state: PhantomData,
        }
    }
    
    /// Connect to a remote address → transitions to Established
    pub fn connect(self, remote: &str) -> Result<TcpConnection<state::Established>, String> {
        println!("Connecting {} → {}", self.local_addr, remote);
        // Simulate connection (in real code: actual TCP handshake)
        Ok(TcpConnection {
            local_addr: self.local_addr,
            remote_addr: Some(remote.to_string()),
            buffer: self.buffer,
            _state: PhantomData,
        })
    }
    
    /// Listen for incoming connections → transitions to Listening
    pub fn listen(self) -> TcpConnection<state::Listening> {
        println!("Listening on {}", self.local_addr);
        TcpConnection {
            local_addr: self.local_addr,
            remote_addr: None,
            buffer: self.buffer,
            _state: PhantomData,
        }
    }
}

// === METHODS ONLY ON LISTENING CONNECTIONS ===
impl TcpConnection<state::Listening> {
    /// Accept an incoming connection → transitions to Established
    pub fn accept(self) -> Result<TcpConnection<state::Established>, String> {
        let remote = "192.168.1.100:54321".to_string();  // Simulated
        println!("Accepted connection from {remote}");
        Ok(TcpConnection {
            local_addr: self.local_addr,
            remote_addr: Some(remote),
            buffer: self.buffer,
            _state: PhantomData,
        })
    }
}

// === METHODS ONLY ON ESTABLISHED CONNECTIONS ===
impl TcpConnection<state::Established> {
    /// Send data (only possible when connected)
    pub fn send(&mut self, data: &[u8]) -> Result<usize, String> {
        println!("Sending {} bytes to {:?}", data.len(), self.remote_addr);
        Ok(data.len())
    }
    
    /// Receive data (only possible when connected)
    pub fn recv(&mut self, buf: &mut [u8]) -> Result<usize, String> {
        let bytes_read = buf.len().min(5);  // Simulated
        buf[..bytes_read].copy_from_slice(b"hello"[..bytes_read].as_ref());
        Ok(bytes_read)
    }
    
    /// Close the connection → transitions to TimeWait
    pub fn close(self) -> TcpConnection<state::TimeWait> {
        println!("Closing connection to {:?}", self.remote_addr);
        TcpConnection {
            local_addr: self.local_addr,
            remote_addr: self.remote_addr,
            buffer: self.buffer,
            _state: PhantomData,
        }
    }
}

// === METHODS ONLY ON TIME_WAIT ===
impl TcpConnection<state::TimeWait> {
    /// Wait for timeout, then transition back to Closed
    pub fn wait_timeout(self) -> TcpConnection<state::Closed> {
        println!("TIME_WAIT expired, connection fully closed");
        TcpConnection {
            local_addr: self.local_addr,
            remote_addr: None,
            buffer: Vec::new(),
            _state: PhantomData,
        }
    }
}

fn main() -> Result<(), String> {
    // Create a closed connection
    let conn = TcpConnection::<state::Closed>::new("0.0.0.0:8080");
    
    // Connect (Closed → Established)
    let mut conn = conn.connect("93.184.216.34:80")?;
    
    // Send and receive (only available in Established state)
    conn.send(b"GET / HTTP/1.1\r\n\r\n")?;
    let mut buf = [0u8; 1024];
    let n = conn.recv(&mut buf)?;
    println!("Received: {:?}", &buf[..n]);
    
    // Close (Established → TimeWait)
    let conn = conn.close();
    
    // Wait (TimeWait → Closed)
    let _conn = conn.wait_timeout();
    
    // ❌ COMPILE ERRORS for invalid transitions:
    // conn.send(b"data");     // Error: no method `send` on TcpConnection<Closed>
    // conn.connect("...");    // Error: no method `connect` on TcpConnection<Established>
    // conn.accept();          // Error: no method `accept` on TcpConnection<Established>
    
    Ok(())
}
```

</details>

### Example 8.5 — Const Generics for Fixed-Size Linear Algebra

**Problem:** Implement a compile-time-checked matrix type where dimensions are part of the type. Matrix multiplication `A * B` should only compile when A's columns equal B's rows, enforced entirely by the type system.

<details>
<summary>🔍 Full step-by-step solution</summary>

```rust
use std::ops::{Add, Mul, Index};

/// A matrix with compile-time dimensions.
/// Matrix<f64, 3, 4> is a 3×4 matrix (3 rows, 4 columns).
#[derive(Debug, Clone)]
struct Matrix<T, const ROWS: usize, const COLS: usize> {
    data: [[T; COLS]; ROWS],
}

impl<T: Default + Copy, const R: usize, const C: usize> Matrix<T, R, C> {
    /// Create a zero matrix
    fn zeros() -> Self
    where
        T: Default + Copy,
    {
        Matrix {
            data: [[T::default(); C]; R],
        }
    }
    
    /// Create from a 2D array
    fn from_array(data: [[T; C]; R]) -> Self {
        Matrix { data }
    }
    
    /// Transpose: Matrix<T, R, C> → Matrix<T, C, R>
    fn transpose(&self) -> Matrix<T, C, R>
    where
        T: Copy + Default,
    {
        let mut result = Matrix::<T, C, R>::zeros();
        for i in 0..R {
            for j in 0..C {
                result.data[j][i] = self.data[i][j];
            }
        }
        result
    }
}

// Index access
impl<T, const R: usize, const C: usize> Index<(usize, usize)> for Matrix<T, R, C> {
    type Output = T;
    fn index(&self, (row, col): (usize, usize)) -> &T {
        &self.data[row][col]
    }
}

// === ADDITION: Only matrices of SAME dimensions can be added ===
impl<T, const R: usize, const C: usize> Add for Matrix<T, R, C>
where
    T: Add<Output = T> + Copy + Default,
{
    type Output = Self;
    
    fn add(self, rhs: Self) -> Self {
        let mut result = Self::zeros();
        for i in 0..R {
            for j in 0..C {
                result.data[i][j] = self.data[i][j] + rhs.data[i][j];
            }
        }
        result
    }
}

// === MULTIPLICATION: Matrix<R,K> * Matrix<K,C> = Matrix<R,C> ===
// The shared dimension K must match — enforced by the type system!
impl<T, const R: usize, const K: usize, const C: usize> Mul<Matrix<T, K, C>>
    for Matrix<T, R, K>
where
    T: Mul<Output = T> + Add<Output = T> + Copy + Default,
{
    type Output = Matrix<T, R, C>;
    
    fn mul(self, rhs: Matrix<T, K, C>) -> Matrix<T, R, C> {
        let mut result = Matrix::<T, R, C>::zeros();
        for i in 0..R {
            for j in 0..C {
                let mut sum = T::default();
                for k in 0..K {
                    sum = sum + self.data[i][k] * rhs.data[k][j];
                }
                result.data[i][j] = sum;
            }
        }
        result
    }
}

// === DISPLAY ===
impl<T: std::fmt::Display, const R: usize, const C: usize> std::fmt::Display
    for Matrix<T, R, C>
{
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        for row in &self.data {
            write!(f, "[")?;
            for (j, val) in row.iter().enumerate() {
                if j > 0 { write!(f, ", ")?; }
                write!(f, "{val:>6.2}")?;
            }
            writeln!(f, "]")?;
        }
        Ok(())
    }
}

fn main() {
    // 2×3 matrix
    let a: Matrix<f64, 2, 3> = Matrix::from_array([
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
    ]);
    
    // 3×2 matrix
    let b: Matrix<f64, 3, 2> = Matrix::from_array([
        [7.0, 8.0],
        [9.0, 10.0],
        [11.0, 12.0],
    ]);
    
    // ✅ A(2×3) * B(3×2) = C(2×2) — dimensions match!
    let c: Matrix<f64, 2, 2> = a * b;
    println!("A × B =\n{c}");
    // [ 58.00,  64.00]
    // [139.00, 154.00]
    
    // ❌ COMPILE ERROR: dimensions don't match
    // let d: Matrix<f64, 2, 3> = Matrix::from_array([[1.0; 3]; 2]);
    // let e: Matrix<f64, 2, 3> = Matrix::from_array([[1.0; 3]; 2]);
    // let f = d * e;  // Error: Matrix<2,3> * Matrix<2,3> — K=3 ≠ 2
    
    // ✅ Addition: same dimensions required
    let x: Matrix<f64, 2, 2> = Matrix::from_array([1.0, 2.0], [3.0, 4.0](1.0,-2.0],-[3.0,-4.0));
    let y: Matrix<f64, 2, 2> = Matrix::from_array([5.0, 6.0], [7.0, 8.0](5.0,-6.0],-[7.0,-8.0));
    let sum = x + y;
    println!("X + Y =\n{sum}");
    
    // ❌ COMPILE ERROR: can't add different dimensions
    // let bad = a + b;  // Matrix<2,3> + Matrix<3,2> — nope!
}
```

</details>


---

## 📘 9. Appendix: Extended Derivations & Special Cases

### 9.1 The Typestate Pattern: Formal Foundations and Advanced Applications

The typestate pattern encodes a finite state machine into the type system such that invalid state transitions become compile-time errors. The key insight is that **zero-sized types** (ZSTs) used as generic parameters add no runtime cost — they exist purely for the compiler's type checker.

**Formal structure:**

Given a state machine with states S = {S₁, S₂, ..., Sₙ} and transitions T ⊆ S × S:
1. Define each state as a ZST: `struct S1; struct S2; ...`
2. Define the stateful type as `struct Machine<State> { ..., _state: PhantomData<State> }`
3. For each transition (Sᵢ, Sⱼ) ∈ T, implement a method on `Machine<Sᵢ>` that consumes `self` and returns `Machine<Sⱼ>`

**Why `self` is consumed (not `&mut self`):**

The transition method takes `self` by value, which **destroys** the old state. This is critical — after calling `conn.connect()`, the variable `conn` of type `TcpConnection<Closed>` no longer exists. You can't accidentally use a connection in the wrong state because the old value is gone.

**Combining typestate with Result for fallible transitions:**

```rust
impl Connection<Connecting> {
    fn complete(self) -> Result<Connection<Connected>, Connection<Failed>> {
        // On success: transition to Connected
        // On failure: transition to Failed (not back to Connecting!)
        // The caller MUST handle both cases.
    }
}
```

**Limitations of typestate:**

1. **State explosion**: If you have N states and M independent dimensions, you get N^M type combinations. Use trait bounds instead of enumerating all combinations.
2. **Dynamic state**: If the state is determined at runtime (e.g., from a config file), you can't use typestate. Use an enum instead.
3. **Collections**: You can't have a `Vec<Connection<???>>` with mixed states. Use an enum wrapper or trait object.

**Advanced: Typestate with trait bounds instead of concrete types:**

```rust
trait ConnectionState {}
trait CanSend: ConnectionState {}
trait CanReceive: ConnectionState {}

struct Established;
impl ConnectionState for Established {}
impl CanSend for Established {}
impl CanReceive for Established {}

struct HalfClosed;
impl ConnectionState for HalfClosed {}
impl CanReceive for HalfClosed {}
// HalfClosed does NOT implement CanSend

impl<S: CanSend> Connection<S> {
    fn send(&mut self, data: &[u8]) { /* ... */ }
}

impl<S: CanReceive> Connection<S> {
    fn recv(&mut self) -> Vec<u8> { /* ... */ vec![] }
}
```

This scales better than individual `impl` blocks for each state.

---

### 9.2 Const Generics: Current Capabilities and Limitations

Const generics (stabilized incrementally from Rust 1.51) allow types and functions to be parameterized by **constant values** (not just types). This enables compile-time-checked dimensions, fixed-size buffers, and more.

**What's stable (as of Rust 1.82+):**

```rust
// Const generic parameters of integral types
struct Array<T, const N: usize> {
    data: [T; N],
}

// Const generics in function signatures
fn first_n<const N: usize>(slice: &[u8]) -> [u8; N] {
    let mut arr = [0u8; N];
    arr.copy_from_slice(&slice[..N]);
    arr
}

// Const generics with default values
struct Buffer<const SIZE: usize = 4096> {
    data: [u8; SIZE],
    len: usize,
}
```

**What's NOT yet stable (nightly only):**

```rust
// Generic const expressions (feature: generic_const_exprs)
// fn concat<const A: usize, const B: usize>(
//     a: [u8; A], b: [u8; B]
// ) -> [u8; A + B] { ... }  // A + B in type position — unstable

// Const generics of non-integral types
// struct Tagged<const TAG: &'static str> { ... }  // Not yet stable

// Complex const expressions in where clauses
// where [(); N - 1]:  // "N >= 1" expressed as const constraint — unstable
```

**Workarounds for unstable features:**

```rust
// Instead of [u8; A + B], use a trait to compute the output size:
trait ArrayConcat<const A: usize, const B: usize> {
    type Output;
    fn concat(a: [u8; A], b: [u8; B]) -> Self::Output;
}

// Or use typenum crate for type-level arithmetic:
// use typenum::{U3, U4, Sum, Unsigned};
// type Seven = Sum<U3, U4>;  // Compile-time: 3 + 4 = 7
```

**Performance implications:**

Const generics enable the compiler to:
1. **Unroll loops** with known bounds (`for i in 0..N` where N is const)
2. **Eliminate bounds checks** when array sizes are known
3. **Vectorize** operations on fixed-size arrays (SIMD)
4. **Inline** small fixed-size operations that would be function calls with runtime sizes

```rust
// This compiles to a single SIMD instruction on x86_64:
fn dot_product_4(a: [f32; 4], b: [f32; 4]) -> f32 {
    a.iter().zip(b.iter()).map(|(x, y)| x * y).sum()
}
// The compiler knows it's exactly 4 elements → uses _mm_dp_ps or similar
```

---

### 9.3 The Orphan Rule, Coherence, and Workarounds

**The orphan rule** states: you can implement a trait for a type only if **either the trait or the type is defined in your crate**. This prevents two crates from providing conflicting implementations of the same trait for the same type.

**Why it exists (coherence):**

Without the orphan rule, two crates could both implement `Display for Vec<i32>`. When a third crate uses both, which implementation wins? The compiler can't decide — this is the "coherence" problem. The orphan rule makes coherence decidable.

**The precise rule (RFC 2451, "re-rebalancing coherence"):**

An impl `impl<T> Trait for Type` is allowed if:
1. `Trait` is defined in the current crate, OR
2. `Type` is defined in the current crate, OR
3. `Type` is a "fundamental" type (`&T`, `&mut T`, `Box<T>`) wrapping a local type

Additionally, the "covered" rule: if `Trait` is foreign, at least one type parameter must be a local type that "covers" (appears before) any type parameters that are also foreign.

```rust
// ✅ Local trait, foreign type:
trait MyTrait { fn foo(&self); }
impl MyTrait for Vec<i32> { fn foo(&self) {} }

// ✅ Foreign trait, local type:
struct MyType;
impl std::fmt::Display for MyType { /* ... */ }

// ✅ Foreign trait, fundamental type wrapping local type:
impl std::fmt::Display for &MyType { /* ... */ }

// ❌ Foreign trait, foreign type:
// impl std::fmt::Display for Vec<i32> { }  // ORPHAN RULE VIOLATION

// ❌ Foreign trait, foreign type with local type parameter:
// impl<T> From<Vec<T>> for HashMap<String, T> { }  // Still violates orphan rule
```

**Workaround 1: Newtype pattern**

```rust
struct DisplayVec(Vec<i32>);

impl std::fmt::Display for DisplayVec {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "[{}]", self.0.iter()
            .map(|n| n.to_string())
            .collect::<Vec<_>>()
            .join(", "))
    }
}

// Use Deref to make the newtype transparent:
impl std::ops::Deref for DisplayVec {
    type Target = Vec<i32>;
    fn deref(&self) -> &Vec<i32> { &self.0 }
}
```

**Workaround 2: Extension trait**

```rust
// Define a new trait with the methods you want:
trait VecExt<T> {
    fn display_joined(&self, sep: &str) -> String;
}

impl<T: std::fmt::Display> VecExt<T> for Vec<T> {
    fn display_joined(&self, sep: &str) -> String {
        self.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(sep)
    }
}

// Now any code that imports VecExt can call .display_joined() on Vec<T>
```

**Workaround 3: Wrapper trait with blanket impl**

```rust
// If you control the trait, provide a blanket impl via a helper trait:
trait AsDisplay {
    fn as_display(&self) -> impl std::fmt::Display + '_;
}

impl<T: std::fmt::Debug> AsDisplay for Vec<T> {
    fn as_display(&self) -> impl std::fmt::Display + '_ {
        struct VecDisplay<'a, T>(&'a Vec<T>);
        impl<T: std::fmt::Debug> std::fmt::Display for VecDisplay<'_, T> {
            fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
                write!(f, "{:?}", self.0)
            }
        }
        VecDisplay(self)
    }
}
```

---

### 9.4 Object Safety: The Complete Rules

A trait is **object-safe** (can be used as `dyn Trait`) if ALL of its methods satisfy these rules:

1. **No `Self` in return position**: Methods can't return `Self` (the compiler doesn't know the concrete type behind `dyn Trait`, so it can't determine the return size).

2. **No generic type parameters**: Methods can't have `<T>` parameters (the vtable has a fixed number of entries; generics would require infinite entries).

3. **Receiver must be a valid receiver type**: `self`, `&self`, `&mut self`, `Box<Self>`, `Rc<Self>`, `Arc<Self>`, `Pin<&Self>`, `Pin<&mut Self>`.

4. **No `where Self: Sized` bound on the trait itself** (but individual methods can have it to opt out of object safety).

```rust
// ❌ NOT object-safe (returns Self):
trait Clonable {
    fn clone(&self) -> Self;
}

// ✅ Object-safe workaround:
trait CloneBox {
    fn clone_box(&self) -> Box<dyn CloneBox>;
}

impl<T: Clone + 'static> CloneBox for T {
    fn clone_box(&self) -> Box<dyn CloneBox> {
        Box::new(self.clone())
    }
}

// ❌ NOT object-safe (generic method):
trait Serializer {
    fn serialize<T: serde::Serialize>(&self, value: &T) -> Vec<u8>;
}

// ✅ Object-safe: use type erasure
trait Serializer {
    fn serialize_erased(&self, value: &dyn erased_serde::Serialize) -> Vec<u8>;
}

// Opt individual methods out of object safety:
trait MixedTrait {
    fn object_safe_method(&self) -> i32;
    
    fn not_object_safe(&self) -> Self where Self: Sized;
    // ^^^^^^^^^^^^^^^^ This method is excluded from the vtable.
    // You can still use `dyn MixedTrait`, but can't call this method on it.
}
```

---
