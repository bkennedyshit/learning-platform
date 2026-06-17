/**
 * 5.4_oop_fp_patterns.js — Practice script for Chapter 5.4
 * OOP and Functional Programming pattern exercises.
 *
 * Usage:
 *   node 5.4_oop_fp_patterns.js
 *   bun 5.4_oop_fp_patterns.js
 */

// ============================================================
// EXERCISE 1: Implement pipe() and compose()
// ============================================================
console.log("═══ Exercise 1: pipe() and compose() ═══\n");

const pipe = (...fns) => (x) => fns.reduce((acc, fn) => fn(acc), x);
const compose = (...fns) => (x) => fns.reduceRight((acc, fn) => fn(acc), x);

// Test functions
const double = (x) => x * 2;
const addOne = (x) => x + 1;
const square = (x) => x ** 2;

const piped = pipe(double, addOne, square); // (5*2 + 1)^2 = 121
const composed = compose(square, addOne, double); // same: square(addOne(double(5)))

console.log("  pipe(double, addOne, square)(5):", piped(5));
console.log("  compose(square, addOne, double)(5):", composed(5));
console.log("  Both should equal 121\n");

// ============================================================
// EXERCISE 2: Currying
// ============================================================
console.log("═══ Exercise 2: Generic curry() ═══\n");

function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    return (...moreArgs) => curried(...args, ...moreArgs);
  };
}

const add = curry((a, b, c) => a + b + c);
console.log("  add(1)(2)(3):", add(1)(2)(3));
console.log("  add(1, 2)(3):", add(1, 2)(3));
console.log("  add(1)(2, 3):", add(1)(2, 3));
console.log("  add(1, 2, 3):", add(1, 2, 3));
console.log("  All should equal 6\n");

// Practical currying
const formatCurrency = curry((symbol, decimals, value) =>
  `${symbol}${value.toFixed(decimals)}`
);
const usd = formatCurrency("$", 2);
const btc = formatCurrency("₿", 8);
console.log("  usd(42.5):", usd(42.5));
console.log("  btc(0.00123):", btc(0.00123));
console.log();

// ============================================================
// EXERCISE 3: Composition over Inheritance
// ============================================================
console.log("═══ Exercise 3: Composition Pattern ═══\n");

// Behavior factories
const withPosition = (state) => ({
  move(dx, dy) { state.x += dx; state.y += dy; },
  getPosition() { return { x: state.x, y: state.y }; },
});

const withHealth = (state) => ({
  takeDamage(amount) { state.hp = Math.max(0, state.hp - amount); },
  heal(amount) { state.hp = Math.min(state.maxHp, state.hp + amount); },
  isAlive() { return state.hp > 0; },
  getHealth() { return `${state.hp}/${state.maxHp}`; },
});

const withAttack = (state) => ({
  attack(target) {
    const damage = state.attackPower;
    target.takeDamage(damage);
    return `${state.name} attacks for ${damage} damage!`;
  },
});

// Compose entities
function createWarrior(name) {
  const state = { name, x: 0, y: 0, hp: 100, maxHp: 100, attackPower: 25 };
  return { name, ...withPosition(state), ...withHealth(state), ...withAttack(state) };
}

function createHealer(name) {
  const state = { name, x: 0, y: 0, hp: 60, maxHp: 60, healPower: 30 };
  return {
    name,
    ...withPosition(state),
    ...withHealth(state),
    healTarget(target) {
      target.heal(state.healPower);
      return `${state.name} heals for ${state.healPower}!`;
    },
  };
}

const warrior = createWarrior("Conan");
const healer = createHealer("Elara");

warrior.move(5, 3);
console.log("  Warrior position:", warrior.getPosition());
console.log("  Warrior health:", warrior.getHealth());

warrior.takeDamage(40);
console.log("  After 40 damage:", warrior.getHealth());

console.log(" ", healer.healTarget(warrior));
console.log("  After heal:", warrior.getHealth());
console.log("  Warrior alive?", warrior.isAlive());
console.log();

// ============================================================
// EXERCISE 4: Immutable update patterns
// ============================================================
console.log("═══ Exercise 4: Immutable Updates ═══\n");

const state = {
  user: { name: "Bill", scores: [85, 92, 78] },
  settings: { theme: "dark", fontSize: 14 },
};

// Add a score immutably
const withNewScore = {
  ...state,
  user: { ...state.user, scores: [...state.user.scores, 95] },
};

// Update theme immutably
const withNewTheme = {
  ...state,
  settings: { ...state.settings, theme: "light" },
};

console.log("  Original scores:", state.user.scores);
console.log("  New scores:", withNewScore.user.scores);
console.log("  Original unchanged?", state.user.scores.length === 3);
console.log();
console.log("  Original theme:", state.settings.theme);
console.log("  New theme:", withNewTheme.settings.theme);
console.log("  Original unchanged?", state.settings.theme === "dark");
console.log();

// ES2023 non-mutating array methods
const nums = [3, 1, 4, 1, 5];
console.log("  Original:", nums);
console.log("  toSorted():", nums.toSorted((a, b) => a - b));
console.log("  toReversed():", nums.toReversed());
console.log("  with(2, 99):", nums.with(2, 99));
console.log("  Original still:", nums);
console.log();

// ============================================================
// EXERCISE 5: Event Emitter (Observer Pattern)
// ============================================================
console.log("═══ Exercise 5: Observer Pattern ═══\n");

class EventEmitter {
  #listeners = new Map();

  on(event, callback) {
    if (!this.#listeners.has(event)) this.#listeners.set(event, new Set());
    this.#listeners.get(event).add(callback);
    return () => this.#listeners.get(event).delete(callback);
  }

  emit(event, ...args) {
    this.#listeners.get(event)?.forEach((cb) => cb(...args));
  }
}

const bus = new EventEmitter();
const unsub = bus.on("message", (msg) => console.log(`  Received: ${msg}`));
bus.on("message", (msg) => console.log(`  Also got: ${msg}`));

bus.emit("message", "Hello!");
unsub(); // Unsubscribe first listener
bus.emit("message", "Second message (only one listener now)");
console.log();

// ============================================================
// EXERCISE 6: Build a pipeline processor
// ============================================================
console.log("═══ Exercise 6: Data Pipeline ═══\n");

const users = [
  { name: "  Bill Kennedy  ", email: "BILL@Example.COM", age: 35, active: true },
  { name: "Jane Doe", email: "jane@test.com", age: 17, active: true },
  { name: "Bob Smith", email: "BOB@work.org", age: 42, active: false },
  { name: "  Alice  ", email: "alice@dev.io", age: 28, active: true },
];

// Build a pipeline using pipe
const processUsers = pipe(
  (users) => users.filter((u) => u.active),
  (users) => users.filter((u) => u.age >= 18),
  (users) => users.map((u) => ({ ...u, name: u.name.trim() })),
  (users) => users.map((u) => ({ ...u, email: u.email.toLowerCase() })),
  (users) => users.map((u) => ({ ...u, slug: u.name.toLowerCase().replace(/\s+/g, "-") })),
);

const processed = processUsers(users);
console.log("  Processed users:");
processed.forEach((u) => console.log(`    ${u.slug} (${u.email})`));
console.log(`\n  Input: ${users.length} users → Output: ${processed.length} users`);
console.log("  (Filtered: inactive Bob, underage Jane)\n");
