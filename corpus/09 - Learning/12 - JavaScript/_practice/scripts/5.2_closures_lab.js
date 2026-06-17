/**
 * 5.2_closures_lab.js — Practice script for Chapter 5.2
 * Exercises on closures, prototypes, and this binding.
 *
 * Usage:
 *   node 5.2_closures_lab.js
 *   bun 5.2_closures_lab.js
 */

// ============================================================
// EXERCISE 1: Implement `once(fn)` — function only executes once
// ============================================================
function once(fn) {
  // TODO: Your implementation here
  // Hint: Use a closure to track whether fn has been called
  let called = false;
  let result;
  return function (...args) {
    if (!called) {
      called = true;
      result = fn.apply(this, args);
    }
    return result;
  };
}

// Test
const init = once(() => { console.log("  Initialized!"); return 42; });
console.log("Exercise 1: once()");
console.log("  First call:", init());   // "Initialized!" → 42
console.log("  Second call:", init());  // → 42 (no log)
console.log("  Third call:", init());   // → 42 (no log)
console.log();

// ============================================================
// EXERCISE 2: Implement `memoize(fn)` — cache results
// ============================================================
function memoize(fn) {
  const cache = new Map();
  return function (...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      console.log(`  [cache hit] args=${key}`);
      return cache.get(key);
    }
    console.log(`  [computing] args=${key}`);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

// Test
const slowSquare = memoize((n) => n ** 2);
console.log("Exercise 2: memoize()");
console.log("  Result:", slowSquare(5));  // [computing] → 25
console.log("  Result:", slowSquare(5));  // [cache hit] → 25
console.log("  Result:", slowSquare(7));  // [computing] → 49
console.log();

// ============================================================
// EXERCISE 3: Predict the output (this binding)
// ============================================================
console.log("Exercise 3: Predict `this` binding");

const obj = {
  name: "Bill",
  greet() { return `Hello, ${this.name}`; },
  greetArrow: () => `Hello, ${typeof this !== "undefined" ? this?.name : "undefined"}`,
  delayedGreet() {
    return new Promise((resolve) => {
      setTimeout(() => resolve(`Delayed: ${this.name}`), 10);
    });
  },
};

console.log("  obj.greet():", obj.greet());
console.log("  obj.greetArrow():", obj.greetArrow());

const { greet } = obj;
// console.log("  destructured greet():", greet()); // What happens? (uncomment to test)

const boundGreet = obj.greet.bind({ name: "William" });
console.log("  boundGreet():", boundGreet());

obj.delayedGreet().then((msg) => {
  console.log(" ", msg);
  console.log();
  runExercise4();
});

// ============================================================
// EXERCISE 4: The classic for-loop closure problem
// ============================================================
function runExercise4() {
  console.log("Exercise 4: for-loop closures");

  // With var (broken)
  console.log("  With var (all same value):");
  const results = [];
  for (var i = 0; i < 3; i++) {
    results.push(() => i);
  }
  console.log("   ", results.map((fn) => fn())); // [3, 3, 3]

  // With let (fixed)
  console.log("  With let (correct values):");
  const results2 = [];
  for (let j = 0; j < 3; j++) {
    results2.push(() => j);
  }
  console.log("   ", results2.map((fn) => fn())); // [0, 1, 2]

  console.log();
  runExercise5();
}

// ============================================================
// EXERCISE 5: Prototype chain tracing
// ============================================================
function runExercise5() {
  console.log("Exercise 5: Prototype chain");

  function Animal(name) { this.name = name; }
  Animal.prototype.speak = function () { return `${this.name} speaks`; };

  function Dog(name, breed) {
    Animal.call(this, name);
    this.breed = breed;
  }
  Dog.prototype = Object.create(Animal.prototype);
  Dog.prototype.constructor = Dog;
  Dog.prototype.bark = function () { return `${this.name} barks!`; };

  const rex = new Dog("Rex", "Shepherd");

  console.log("  rex.bark():", rex.bark());
  console.log("  rex.speak():", rex.speak());
  console.log("  rex instanceof Dog:", rex instanceof Dog);
  console.log("  rex instanceof Animal:", rex instanceof Animal);
  console.log("  rex.hasOwnProperty('name'):", rex.hasOwnProperty("name"));
  console.log("  rex.hasOwnProperty('bark'):", rex.hasOwnProperty("bark"));
  console.log("  Object.getPrototypeOf(rex) === Dog.prototype:", Object.getPrototypeOf(rex) === Dog.prototype);

  // Chain visualization
  console.log("\n  Prototype chain:");
  let proto = rex;
  let chain = "rex";
  while ((proto = Object.getPrototypeOf(proto)) !== null) {
    const name = proto.constructor?.name ?? "null";
    chain += ` → ${name}.prototype`;
  }
  chain += " → null";
  console.log(`  ${chain}`);
}
