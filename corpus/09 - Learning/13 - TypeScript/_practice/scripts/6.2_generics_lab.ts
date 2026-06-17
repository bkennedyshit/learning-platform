/**
 * 6.2_generics_lab.ts — Hands-on TypeScript generics exercises.
 *
 * Instructions:
 *   1. Replace every `any` and `unknown` with proper types.
 *   2. Run: bun run 6.2_generics_lab.ts (or: npx tsx 6.2_generics_lab.ts)
 *   3. All assertions should pass with zero type errors.
 *
 * Chapter: 6.2 — Type System: Primitives, Unions, Intersections, Generics
 */

// ============================================================
// Exercise 1: Generic identity function
// ============================================================
// TODO: Make this generic so it preserves the input type
function identity(value: any): any {
  return value;
}

// These should work without type assertions:
// const str: string = identity("hello");
// const num: number = identity(42);

// ============================================================
// Exercise 2: Generic array utilities
// ============================================================
// TODO: Type these functions properly with generics

function first(arr: any[]): any {
  return arr[0];
}

function last(arr: any[]): any {
  return arr[arr.length - 1];
}

function unique(arr: any[]): any[] {
  return [...new Set(arr)];
}

// ============================================================
// Exercise 3: Constrained generics
// ============================================================
// TODO: Add a constraint so T must have a 'length' property

function longest(a: any, b: any): any {
  return a.length >= b.length ? a : b;
}

// Should work:
// longest("hello", "hi");       // string
// longest([1,2,3], [1]);        // number[]

// Should NOT work (uncomment to verify):
// longest(10, 20);              // Error: number has no 'length'

// ============================================================
// Exercise 4: keyof and indexed access
// ============================================================
// TODO: Type this so the return type matches the property type

function getProperty(obj: any, key: any): any {
  return obj[key];
}

// Should infer:
// const name: string = getProperty({ name: "Bill", age: 35 }, "name");
// const age: number = getProperty({ name: "Bill", age: 35 }, "age");

// ============================================================
// Exercise 5: Generic interface
// ============================================================
// TODO: Define a generic Repository<T> interface with these methods:
//   findById(id: string): Promise<T | null>
//   findAll(): Promise<T[]>
//   create(item: Omit<T, "id">): Promise<T>
//   delete(id: string): Promise<void>

// interface Repository<T> { ... }

// ============================================================
// Exercise 6: Discriminated union + generic
// ============================================================
// TODO: Define Result<T, E> as a discriminated union and implement:
//   Ok(value) → { ok: true, value: T }
//   Err(error) → { ok: false, error: E }
//   map(result, fn) → transforms the value if Ok

// type Result<T, E = Error> = ...
// function Ok<T>(value: T): Result<T, never> { ... }
// function Err<E>(error: E): Result<never, E> { ... }
// function map<T, U, E>(result: Result<T, E>, fn: (t: T) => U): Result<U, E> { ... }

// ============================================================
// Self-check: Uncomment and verify no errors
// ============================================================
/*
const r1 = Ok(42);
const r2 = map(r1, n => n.toString());  // Result<string, never>
const r3 = Err(new Error("oops"));
const r4 = map(r3, n => n.toString());  // Result<string, Error> (still Err)
*/

console.log("✅ All exercises complete — now replace the 'any' types!");
