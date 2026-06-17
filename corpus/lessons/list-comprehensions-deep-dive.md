---
title: "List Comprehensions Deep Dive"
subject: "00_Basics"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: code-reference
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# List Comprehensions Deep Dive

## Basic List Comprehension
```python
# Instead of this:
squares = []
for x in range(10):
    squares.append(x ** 2)

# Do this:
squares = [x ** 2 for x in range(10)]
```

## Structure
```python
# Basic syntax
[expression for item in iterable]

# With condition
[expression for item in iterable if condition]

# With else (ternary)
[true_expr if condition else false_expr for item in iterable]
```

## Common Patterns
```python
# Transform items
names = ["billy", "alex", "chris"]
uppercase = [name.upper() for name in names]

# Filter items
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = [x for x in numbers if x % 2 == 0]

# Transform and filter
positive_doubles = [x * 2 for x in numbers if x > 0]

# With ternary
labels = ["even" if x % 2 == 0 else "odd" for x in numbers]

# Multiple conditions (AND)
divisible = [x for x in range(100) if x % 3 == 0 if x % 5 == 0]

# Multiple conditions (OR) - use single if
divisible = [x for x in range(100) if x % 3 == 0 or x % 5 == 0]
```

## Nested Comprehensions
```python
# Flatten 2D list
matrix = [1, 2, 3], [4, 5, 6], [7, 8, 9](1,-2,-3],-[4,-5,-6],-[7,-8,-9)
flattened = [item for row in matrix for item in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Create 2D list
matrix = [[i * j for j in range(5)] for i in range(5)]

# Cartesian product
colors = ["red", "blue"]
sizes = ["S", "M", "L"]
combinations = [(color, size) for color in colors for size in sizes]
# [('red', 'S'), ('red', 'M'), ('red', 'L'), ('blue', 'S'), ...]
```

## Working with Strings
```python
# String to list of characters
word = "python"
chars = [c for c in word]

# Filter vowels
vowels = [c for c in word if c in "aeiou"]

# Transform characters
uppercase_chars = [c.upper() for c in word]

# String from list
sentence = "hello world"
words = [word.upper() for word in sentence.split()]
result = " ".join(words)  # "HELLO WORLD"
```

## Working with Multiple Lists
```python
# Zip two lists
names = ["Billy", "Alex"]
ages = [30, 25]
people = [f"{name} is {age}" for name, age in zip(names, ages)]

# Combine lists
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = [x + y for x, y in zip(list1, list2)]
# [5, 7, 9]
```

## Dict Comprehensions
```python
# Create dict from lists
keys = ["a", "b", "c"]
values = [1, 2, 3]
d = {k: v for k, v in zip(keys, values)}

# Transform dict
prices = {"apple": 0.50, "banana": 0.30}
doubled = {item: price * 2 for item, price in prices.items()}

# Filter dict
expensive = {item: price for item, price in prices.items() if price > 0.40}

# Swap keys and values
inverted = {v: k for k, v in original.items()}

# Create from range
squares_dict = {x: x ** 2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

## Set Comprehensions
```python
# Create set (removes duplicates)
numbers = [1, 2, 2, 3, 3, 3, 4, 5]
unique_squares = {x ** 2 for x in numbers}

# Filter into set
evens = {x for x in range(20) if x % 2 == 0}
```

## Generator Expressions
```python
# Like list comp but doesn't create list in memory
# Use parentheses instead of brackets
gen = (x ** 2 for x in range(1000000))

# Use with sum, max, min, any, all
total = sum(x ** 2 for x in range(100))
max_val = max(x for x in numbers if x > 0)
has_even = any(x % 2 == 0 for x in numbers)
all_positive = all(x > 0 for x in numbers)

# Convert to list when needed
squares_list = list(x ** 2 for x in range(10))
```

## Advanced Patterns
```python
# Nested dict comprehension
matrix = [1, 2], [3, 4](1,-2],-[3,-4)
indexed = {i: {j: val for j, val in enumerate(row)} 
           for i, row in enumerate(matrix)}

# Conditional dict values
numbers = [1, 2, 3, 4, 5]
categorized = {x: "even" if x % 2 == 0 else "odd" for x in numbers}

# Multiple transformations
words = ["hello", "world", "python"]
formatted = [word.upper().strip() for word in words if len(word) > 4]

# Enumerate in comprehension
indexed_list = [(i, val * 2) for i, val in enumerate(range(5))]
```

## When to Use vs. Not Use
```python
# GOOD - simple, readable
squares = [x ** 2 for x in range(10)]
evens = [x for x in numbers if x % 2 == 0]

# BAD - too complex, use regular loop
# If you need multiple lines or complex logic
result = []
for item in items:
    if complex_condition(item):
        processed = complex_processing(item)
        if another_condition(processed):
            result.append(processed)

# GOOD alternative for complex logic
def process_item(item):
    if complex_condition(item):
        processed = complex_processing(item)
        if another_condition(processed):
            return processed
    return None

result = [x for x in (process_item(item) for item in items) if x is not None]
```

## Common Test Scenarios
```python
# Get unique words from text
text = "the quick brown fox jumps over the lazy dog"
unique_words = {word for word in text.split()}

# Count character frequencies
from collections import Counter
text = "hello world"
freq = Counter(c for c in text if c.isalpha())

# Filter files by extension
files = ["file1.txt", "file2.py", "file3.txt", "file4.md"]
txt_files = [f for f in files if f.endswith(".txt")]

# Extract numbers from mixed list
mixed = [1, "two", 3, "four", 5]
numbers = [x for x in mixed if isinstance(x, int)]

# Create lookup dict
users = [{"id": 1, "name": "Billy"}, {"id": 2, "name": "Alex"}]
lookup = {user["id"]: user["name"] for user in users}

# Flatten nested structure
nested = [1, 2], [3, 4], [5](1,-2],-[3,-4],-[5)
flat = [item for sublist in nested for item in sublist]

# Matrix transpose
matrix = [1, 2, 3], [4, 5, 6](1,-2,-3],-[4,-5,-6)
transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
```

## Performance Tips
```python
# List comp faster than map + lambda
squares = [x ** 2 for x in range(1000)]  # Faster
squares = list(map(lambda x: x ** 2, range(1000)))  # Slower

# Generator for large data (memory efficient)
# Don't do this for huge datasets:
huge_list = [expensive_operation(x) for x in range(1000000)]

# Do this instead:
huge_gen = (expensive_operation(x) for x in range(1000000))
for item in huge_gen:
    process(item)

# Or use built-in functions with generator
total = sum(expensive_operation(x) for x in range(1000000))
```

## Quick Tips for Tests
- List comp > for loop for simple transformations
- Use generator expressions with `sum()`, `any()`, `all()`
- Dict comp for creating/transforming dicts
- Set comp for unique values
- Keep it simple - if too complex, use regular loop
- Comprehensions are Pythonic and impress interviewers

---

## Related Notes
- [Python Lists & Tuples](Python-Lists-&-Tuples)
- [Python Dictionaries & Sets](Python-Dictionaries-&-Sets)
- [Python Loops & Iteration](Python-Loops-&-Iteration)
- [Generator Expressions](Generator-Expressions)
- [Python Performance Tips](Python-Performance-Tips)
