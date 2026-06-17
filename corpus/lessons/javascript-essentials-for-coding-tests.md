---
title: "JavaScript Essentials for Coding Tests"
subject: "JavaScript"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: learning-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# JavaScript Essentials for Coding Tests

**Master modern JavaScript for interviews and practical development**

---

## 1. Variables & Data Types

### Variable Declarations
```javascript
// const - use by default (can't reassign)
const name = "Billy";
const PI = 3.14159;

// let - use when you need to reassign (block scoped)
let counter = 0;
counter++;

// var - AVOID (function scoped, hoisting issues)
var oldWay = "deprecated";
```

### Primitive Types
```javascript
// String
const name = "Billy";
const name2 = 'Billy';
const template = `Hello ${name}`; // Template literal (best)

// Number (no int/float distinction)
const integer = 42;
const floating = 3.14;
const negative = -10;

// Boolean
const isActive = true;
const isDone = false;

// Null & Undefined
let empty;              // undefined (not assigned)
let nothing = null;     // null (intentionally empty)

// Symbol (unique identifier)
const id = Symbol('id');

// BigInt (large integers)
const huge = 9007199254740991n;
```

### Type Checking
```javascript
typeof "hello"          // "string"
typeof 42              // "number"
typeof true            // "boolean"
typeof undefined       // "undefined"
typeof null            // "object" (known bug!)
typeof {}              // "object"
typeof []              // "object" (arrays are objects!)
Array.isArray([])      // true (proper array check)
```

---

## 2. Arrays - Essential for Coding Tests

### Creation & Basic Operations
```javascript
const arr = [1, 2, 3, 4, 5];
const empty = [];
const mixed = [1, "two", true, null];

// Access
arr[0]                  // 1 (first)
arr[arr.length - 1]     // 5 (last)
arr.at(-1)              // 5 (last, modern way)
arr.at(-2)              // 4 (second to last)

// Modify
arr.push(6)             // Add to end → [1,2,3,4,5,6]
arr.pop()               // Remove from end → returns 6
arr.unshift(0)          // Add to front → [0,1,2,3,4,5]
arr.shift()             // Remove from front → returns 0
arr[2] = 99             // Direct assignment → [1,2,99,4,5]

// Slicing (doesn't mutate)
arr.slice(1, 3)         // [2,3] (index 1 to 2)
arr.slice(2)            // [3,4,5] (index 2 to end)
arr.slice(-2)           // [4,5] (last 2)

// Splicing (MUTATES array)
arr.splice(2, 1)        // Remove 1 at index 2 → returns [3]
arr.splice(1, 0, 99)    // Insert 99 at index 1 → []
arr.splice(1, 2, 'a', 'b') // Replace 2 items with 'a', 'b'
```

### Array Methods (Most Important for Tests!)
```javascript
const nums = [1, 2, 3, 4, 5];

// map - Transform each element (RETURNS NEW ARRAY)
const doubled = nums.map(x => x * 2);
// [2, 4, 6, 8, 10]

// filter - Keep matching elements (RETURNS NEW ARRAY)
const evens = nums.filter(x => x % 2 === 0);
// [2, 4]

// reduce - Accumulate to single value
const sum = nums.reduce((acc, curr) => acc + curr, 0);
// 15

// forEach - Execute function on each (NO RETURN)
nums.forEach(x => console.log(x));

// find - First matching element
const found = nums.find(x => x > 3);
// 4

// findIndex - Index of first match
const idx = nums.findIndex(x => x > 3);
// 3

// some - Returns true if ANY match
const hasEven = nums.some(x => x % 2 === 0);
// true

// every - Returns true if ALL match
const allPositive = nums.every(x => x > 0);
// true

// includes - Check if value exists
nums.includes(3);       // true

// indexOf - Get index of value
nums.indexOf(3);        // 2 (or -1 if not found)

// sort - Sort in place (MUTATES!)
nums.sort((a, b) => a - b);  // Ascending
nums.sort((a, b) => b - a);  // Descending

// reverse - Reverse in place (MUTATES!)
nums.reverse();

// concat - Combine arrays (doesn't mutate)
const combined = nums.concat([6, 7, 8]);

// join - Convert to string
nums.join(", ");        // "1, 2, 3, 4, 5"

// flat - Flatten nested arrays
const nested = [1, [2, [3, 4]]];
nested.flat();          // [1, 2, [3, 4]]
nested.flat(2);         // [1, 2, 3, 4] (depth 2)
```

### Array Destructuring
```javascript
const [first, second, ...rest] = [1, 2, 3, 4, 5];
// first = 1, second = 2, rest = [3, 4, 5]

// Swap variables
let a = 1, b = 2;
[a, b] = [b, a];  // a = 2, b = 1
```

---

## 3. Objects

### Creation & Access
```javascript
const person = {
    name: "Billy",
    age: 33,
    city: "Plains"
};

// Access
person.name             // "Billy" (dot notation)
person["name"]          // "Billy" (bracket notation)
const key = "name";
person[key]             // "Billy" (dynamic key)

// Modify
person.job = "Engineer";   // Add property
person.age = 34;           // Update property
delete person.city;        // Remove property
```

### Object Methods
```javascript
const obj = { name: "Billy", age: 33 };

Object.keys(obj)           // ["name", "age"]
Object.values(obj)         // ["Billy", 33]
Object.entries(obj)        // ["name", "Billy"], ["age", 33]("name",-"Billy"],-["age",-33)

"name" in obj              // true (check if key exists)
obj.hasOwnProperty("name") // true

// Copy (shallow)
const copy = Object.assign({}, obj);
const copy2 = { ...obj };  // Spread (preferred)

// Merge objects
const merged = { ...obj, city: "Plains", age: 34 };
```

### Object Destructuring
```javascript
const { name, age } = person;
// name = "Billy", age = 33

// Rename
const { name: n, age: a } = person;

// Default values
const { job = "Unknown" } = person;

// Rest
const { name, ...otherProps } = person;
```

---

## 4. Strings

### Common String Operations
```javascript
const str = "Hello World";

// Properties
str.length              // 11

// Case
str.toLowerCase()       // "hello world"
str.toUpperCase()       // "HELLO WORLD"

// Trim whitespace
"  hello  ".trim()      // "hello"
"  hello  ".trimStart() // "hello  "
"  hello  ".trimEnd()   // "  hello"

// Substring
str.slice(0, 5)         // "Hello"
str.slice(6)            // "World"
str.slice(-5)           // "World" (last 5)
str.substring(0, 5)     // "Hello" (similar to slice)

// Split & Join
str.split(" ")          // ["Hello", "World"]
str.split("")           // ["H", "e", "l", "l", "o", " ", "W", "o", "r", "l", "d"]
["Hello", "World"].join(" ")  // "Hello World"

// Search
str.includes("World")   // true
str.startsWith("Hello") // true
str.endsWith("World")   // true
str.indexOf("World")    // 6 (or -1 if not found)

// Replace
str.replace("World", "JS")      // "Hello JS" (first occurrence)
str.replaceAll("l", "L")        // "HeLLo WorLd" (all occurrences)

// Repeat
"ha".repeat(3)          // "hahaha"

// Pad
"5".padStart(3, "0")    // "005"
"5".padEnd(3, "0")      // "500"

// Template literals (BEST for building strings)
const name = "Billy";
const age = 33;
const msg = `My name is ${name} and I'm ${age} years old.`;
```

### Common String Patterns
```javascript
// Reverse string
const reversed = str.split("").reverse().join("");

// Check palindrome
const isPalindrome = str === str.split("").reverse().join("");

// Count vowels
const vowelCount = str.toLowerCase().split("").filter(c => "aeiou".includes(c)).length;

// First non-repeating character
function firstUniqChar(s) {
    const counts = {};
    for (const char of s) counts[char] = (counts[char] || 0) + 1;
    for (const char of s) if (counts[char] === 1) return char;
    return null;
}
```

---

## 5. Functions

### Function Declarations
```javascript
// Function declaration (hoisted)
function add(a, b) {
    return a + b;
}

// Function expression
const add = function(a, b) {
    return a + b;
};

// Arrow function (preferred for short functions)
const add = (a, b) => a + b;
const double = x => x * 2;  // Single param, no parens
const greet = () => "Hello"; // No params

// Arrow with block body
const add = (a, b) => {
    const result = a + b;
    return result;
};
```

### Parameters
```javascript
// Default parameters
function greet(name = "Guest") {
    return `Hello ${name}`;
}

// Rest parameters (collect into array)
function sum(...numbers) {
    return numbers.reduce((acc, n) => acc + n, 0);
}
sum(1, 2, 3, 4);  // 10

// Spread (expand array into args)
const nums = [1, 2, 3];
sum(...nums);  // 6
```

### Higher-Order Functions (Functions as arguments)
```javascript
// Functions can accept functions
function doTwice(fn, value) {
    return fn(fn(value));
}
doTwice(x => x * 2, 5);  // 20

// Functions can return functions
function multiplier(factor) {
    return x => x * factor;
}
const double = multiplier(2);
double(5);  // 10
```

---

## 6. Control Flow

### Conditionals
```javascript
// if/else
if (age >= 18) {
    console.log("Adult");
} else if (age >= 13) {
    console.log("Teen");
} else {
    console.log("Child");
}

// Ternary operator
const status = age >= 18 ? "Adult" : "Minor";

// Nullish coalescing (?? - only null/undefined)
const value = maybeNull ?? "default";

// Optional chaining (?. - safe property access)
const city = user?.address?.city;

// Logical OR (|| - any falsy value)
const name = input || "Guest";

// Switch (rarely used)
switch (color) {
    case "red":
        console.log("Stop");
        break;
    case "yellow":
        console.log("Slow");
        break;
    default:
        console.log("Go");
}
```

### Loops
```javascript
// for loop
for (let i = 0; i < 5; i++) {
    console.log(i);
}

// for...of (values) - USE FOR ARRAYS
for (const item of arr) {
    console.log(item);
}

// for...in (keys) - USE FOR OBJECTS
for (const key in obj) {
    console.log(key, obj[key]);
}

// while
let i = 0;
while (i < 5) {
    console.log(i);
    i++;
}

// do...while (runs at least once)
do {
    console.log(i);
    i++;
} while (i < 5);

// break & continue
for (let i = 0; i < 10; i++) {
    if (i === 3) continue;  // Skip 3
    if (i === 7) break;     // Stop at 7
    console.log(i);
}
```

---

## 7. Async JavaScript (CRITICAL for Modern Dev)

### Promises
```javascript
// Create promise
const promise = new Promise((resolve, reject) => {
    setTimeout(() => {
        resolve("Success!");
        // or reject("Error!");
    }, 1000);
});

// Use promise
promise
    .then(result => console.log(result))
    .catch(error => console.error(error))
    .finally(() => console.log("Done"));
```

### Async/Await (PREFERRED)
```javascript
// Async function always returns promise
async function fetchUser(id) {
    try {
        const response = await fetch(`/api/users/${id}`);
        const user = await response.json();
        return user;
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

// Use it
const user = await fetchUser(1);

// Multiple async operations in parallel
const [users, posts] = await Promise.all([
    fetchUsers(),
    fetchPosts()
]);
```

### Common Async Patterns
```javascript
// Delay
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
await delay(1000);  // Wait 1 second

// Retry logic
async function fetchWithRetry(url, retries = 3) {
    for (let i = 0; i < retries; i++) {
        try {
            return await fetch(url);
        } catch (err) {
            if (i === retries - 1) throw err;
            await delay(1000 * (i + 1));
        }
    }
}

// Promise.race (first to complete)
const result = await Promise.race([
    fetchData(),
    delay(5000).then(() => { throw new Error("Timeout"); })
]);
```

---

## 8. DOM Manipulation (Browser Only)

### Selecting Elements
```javascript
// Single element
const el = document.getElementById('myId');
const el = document.querySelector('.myClass');
const el = document.querySelector('#myId');

// Multiple elements (returns NodeList)
const els = document.querySelectorAll('.myClass');
const els = document.getElementsByClassName('myClass');
const els = document.getElementsByTagName('div');
```

### Modifying Elements
```javascript
// Content
el.textContent = "New text";
el.innerHTML = "<strong>HTML</strong>";

// Attributes
el.getAttribute('href');
el.setAttribute('href', '/new');
el.removeAttribute('disabled');

// Classes
el.classList.add('active');
el.classList.remove('hidden');
el.classList.toggle('selected');
el.classList.contains('active');

// Styles
el.style.color = 'red';
el.style.backgroundColor = 'blue';
```

### Creating & Adding Elements
```javascript
// Create
const div = document.createElement('div');
div.textContent = "Hello";
div.className = "message";

// Add to DOM
parent.appendChild(div);
parent.insertBefore(div, sibling);
parent.replaceChild(newEl, oldEl);
parent.removeChild(div);

// Modern way
parent.append(div);           // Add as last child
parent.prepend(div);          // Add as first child
el.before(newEl);             // Insert before
el.after(newEl);              // Insert after
el.remove();                  // Remove self
```

### Event Handling
```javascript
// Add event listener
button.addEventListener('click', (e) => {
    console.log('Clicked!', e.target);
});

// Common events: click, dblclick, mouseenter, mouseleave,
// keydown, keyup, submit, change, input, focus, blur

// Remove listener
function handler(e) { console.log(e); }
button.addEventListener('click', handler);
button.removeEventListener('click', handler);

// Event object
button.addEventListener('click', (e) => {
    e.preventDefault();     // Stop default action
    e.stopPropagation();    // Stop bubbling
    e.target;               // Element that triggered
    e.currentTarget;        // Element listener is on
});
```

---

## 9. ES6+ Features (Modern JavaScript)

### Destructuring
```javascript
// Array
const [a, b, ...rest] = [1, 2, 3, 4];

// Object
const { name, age, ...other } = person;

// Nested
const { address: { city } } = person;

// Function params
function greet({ name, age }) {
    return `${name} is ${age}`;
}
```

### Spread & Rest
```javascript
// Spread array
const arr1 = [1, 2];
const arr2 = [...arr1, 3, 4];  // [1, 2, 3, 4]

// Spread object
const obj2 = { ...obj1, newProp: "value" };

// Rest (collect)
function sum(...nums) {
    return nums.reduce((a, b) => a + b);
}
```

### Shorthand Properties
```javascript
const name = "Billy";
const age = 33;

// Shorthand
const person = { name, age };  // Same as { name: name, age: age }

// Method shorthand
const obj = {
    greet() {  // Same as greet: function() {}
        return "Hello";
    }
};
```

### Template Literals
```javascript
const name = "Billy";
const age = 33;
const msg = `My name is ${name}.
I am ${age} years old.`;  // Multi-line allowed
```

---

## 10. Common Coding Test Patterns

### Two Pointer Technique
```javascript
// Reverse string
function reverse(s) {
    const arr = s.split("");
    let left = 0, right = arr.length - 1;
    while (left < right) {
        [arr[left], arr[right]] = [arr[right], arr[left]];
        left++;
        right--;
    }
    return arr.join("");
}

// Two sum (sorted array)
function twoSum(arr, target) {
    let left = 0, right = arr.length - 1;
    while (left < right) {
        const sum = arr[left] + arr[right];
        if (sum === target) return [left, right];
        if (sum < target) left++;
        else right--;
    }
    return null;
}
```

### Hash Map Pattern
```javascript
// Two sum (unsorted)
function twoSum(nums, target) {
    const map = new Map();
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        if (map.has(complement)) {
            return [map.get(complement), i];
        }
        map.set(nums[i], i);
    }
    return null;
}

// Count occurrences
function countOccurrences(arr) {
    const counts = {};
    for (const item of arr) {
        counts[item] = (counts[item] || 0) + 1;
    }
    return counts;
}
```

### Sliding Window
```javascript
// Max sum of k consecutive elements
function maxSum(arr, k) {
    let windowSum = 0;
    for (let i = 0; i < k; i++) {
        windowSum += arr[i];
    }
    
    let maxSum = windowSum;
    for (let i = k; i < arr.length; i++) {
        windowSum = windowSum - arr[i - k] + arr[i];
        maxSum = Math.max(maxSum, windowSum);
    }
    return maxSum;
}
```

---

## Quick JavaScript Tips for Tests

1. **Use const by default**, let when needed, never var
2. **Array methods are your friend**: map, filter, reduce, find, some, every
3. **Template literals** for string building (`` instead of +)
4. **Arrow functions** for short callbacks: `arr.map(x => x * 2)`
5. **Destructuring** to extract values: `const {name, age} = person`
6. **Spread operator** to copy/merge: `[...arr]`, `{...obj}`
7. **Optional chaining** for safe access: `user?.address?.city`
8. **Array.isArray()** to check if array (typeof returns "object")
9. **Use === not ==** (strict equality, avoids type coercion)
10. **Math.floor() for integer division**: `Math.floor(5/2)` = 2
11. **Sort needs comparator** for numbers: `arr.sort((a, b) => a - b)`
12. **Check array length** before accessing: `if (arr.length > 0)`
13. **Use for...of for arrays**, for...in for objects
14. **async/await** is cleaner than promise chains
15. **Try/catch** for error handling in async functions

---

## Related Notes

- [Python Lists & Tuples](Python-Lists-&-Tuples) - Similar array operations
- [Common Algorithms for Coding Tests](Common-Algorithms-for-Coding-Tests) - Language-agnostic patterns
- [TypeScript Essentials for Coding Tests](TypeScript-Essentials-for-Coding-Tests) - JavaScript with types
- [Working with APIs in Python](Working-with-APIs-in-Python) - Similar async patterns
- [VS Code Shortcuts & Productivity](VS-Code-Shortcuts-&-Productivity) - JavaScript debugging

---

**Use this note when:**
- Preparing for JavaScript coding interviews
- Need quick syntax reference for ES6+ features
- Working with arrays and need method reminder
- Building web applications with DOM manipulation
- Learning async/await patterns
