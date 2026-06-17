---
date: 2026-01-24
title: Python Loops & Iteration
mission: Quick reference for for/while loops, iteration patterns, and loop control for coding tests
status: active-reference
tags: [python, loops, iteration, for, while, coding-test]
type: code-reference
---

# Python Loops & Iteration

## For Loops
```python
# Iterate over list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Iterate over range
for i in range(5):  # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 10):  # 2 to 9
    print(i)

for i in range(0, 10, 2):  # 0, 2, 4, 6, 8 (step=2)
    print(i)

# Iterate over string
for char in "Python":
    print(char)
```

## Enumerate (Get Index + Value)
```python
# BAD
for i in range(len(fruits)):
    print(i, fruits[i])

# GOOD
for index, fruit in enumerate(fruits):
    print(index, fruit)

# Start index at 1
for index, fruit in enumerate(fruits, start=1):
    print(index, fruit)
```

## Zip (Iterate Multiple Lists)
```python
names = ["Billy", "Alex", "Chris"]
ages = [30, 25, 28]

for name, age in zip(names, ages):
    print(f"{name} is {age} years old")

# Unequal lengths - stops at shortest
# Use zip_longest from itertools for all items
```

## Dictionary Iteration
```python
person = {"name": "Billy", "age": 30, "sport": "BMX"}

# Keys only
for key in person:
    print(key)

# Keys explicitly
for key in person.keys():
    print(key)

# Values only
for value in person.values():
    print(value)

# Key-value pairs (BEST)
for key, value in person.items():
    print(f"{key}: {value}")
```

## While Loops
```python
# Basic while
count = 0
while count < 5:
    print(count)
    count += 1

# While with condition
user_input = ""
while user_input != "quit":
    user_input = input("Enter command: ")

# Infinite loop (use with break)
while True:
    data = get_data()
    if data == "stop":
        break
    process(data)
```

## Loop Control
```python
# Break - exit loop
for i in range(10):
    if i == 5:
        break  # Stop loop at 5
    print(i)  # 0, 1, 2, 3, 4

# Continue - skip to next iteration
for i in range(10):
    if i % 2 == 0:
        continue  # Skip even numbers
    print(i)  # 1, 3, 5, 7, 9

# Else - runs if loop completes without break
for i in range(5):
    if i == 10:
        break
else:
    print("Loop completed")  # This runs
```

## Nested Loops
```python
# 2D iteration
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

for row in matrix:
    for item in row:
        print(item, end=" ")
    print()  # New line

# With indices
for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        print(f"[{i}][{j}] = {matrix[i][j]}")
```

## List Comprehensions (Loop Alternative)
```python
# Instead of:
squares = []
for x in range(10):
    squares.append(x ** 2)

# Use:
squares = [x ** 2 for x in range(10)]

# With condition
evens = [x for x in range(10) if x % 2 == 0]

# Transform
names_upper = [name.upper() for name in names]

# Nested comprehension
matrix = [[i*j for j in range(5)] for i in range(5)]
```

## Common Iteration Patterns
```python
# Iterate with index and value
for i, item in enumerate(items):
    print(f"Item {i}: {item}")

# Reverse iteration
for item in reversed(items):
    print(item)

# Sorted iteration (doesn't modify original)
for item in sorted(items):
    print(item)

# Iterate in chunks
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

for chunk in chunks(data, 3):
    print(chunk)

# Iterate with previous value
for i, item in enumerate(items):
    if i > 0:
        prev = items[i - 1]
        print(f"Prev: {prev}, Current: {item}")
```

## Iterator Functions
```python
# Map - apply function to all items
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))

# Filter - keep only matching items
evens = list(filter(lambda x: x % 2 == 0, numbers))

# Any - True if any item matches
has_even = any(x % 2 == 0 for x in numbers)

# All - True if all items match
all_positive = all(x > 0 for x in numbers)

# Sum with generator
total = sum(x ** 2 for x in numbers)
```

## Quick Tips for Tests
- Use `enumerate()` when you need index + value
- Use `zip()` to iterate multiple lists together
- List comprehension > for loop (cleaner, faster)
- Use `break` to exit early, `continue` to skip
- `range(len(list))` is usually code smell - use `enumerate()`
- Remember `for...else` for "not found" patterns
- `while True` + `break` is fine for event loops

## Performance Tips
```python
# BAD - creates list in memory
for i in range(1000000):
    process(i)

# GOOD - generator, no memory overhead
for i in range(1000000):  # range() is already a generator in Python 3
    process(i)

# Comprehension vs loop - comprehension is faster
squares = [x**2 for x in range(1000)]  # Fast
# vs
squares = []
for x in range(1000):
    squares.append(x**2)  # Slower
```

---

## Related Notes
- [[Python Lists & Tuples]]
- [[Python Dictionaries & Sets]]
- [[List Comprehensions Deep Dive]]
- [[Generator Expressions]]
- [[Python Control Flow]]
- [[Iteration Patterns for Coding Tests]]
