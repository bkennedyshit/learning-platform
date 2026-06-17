---
date: 2026-01-24
title: Python Dictionaries & Sets
mission: Quick reference for dict/set operations and common patterns for coding tests
status: active-reference
tags: [python, dictionaries, sets, data-structures, coding-test]
type: code-reference
---

# Python Dictionaries & Sets

## Dictionary Basics
```python
# Create
person = {
    "name": "Billy",
    "age": 30,
    "rider": True
}

# Or
empty = {}
also_empty = dict()

# Access
name = person["name"]  # KeyError if not exists
name = person.get("name")  # Returns None if not exists
name = person.get("name", "Unknown")  # Default value

# Add/Update
person["height"] = 5.10
person.update({"city": "NEPA", "sport": "BMX"})

# Remove
del person["age"]
popped = person.pop("rider")  # Remove and return
person.clear()  # Remove all
```

## Dictionary Methods
```python
# Get keys, values, items
person.keys()    # dict_keys(['name', 'age'])
person.values()  # dict_values(['Billy', 30])
person.items()   # dict_items([('name', 'Billy'), ('age', 30)])

# Check existence
"name" in person  # Check key exists

# Loop through
for key in person:
    print(key, person[key])

for key, value in person.items():
    print(f"{key}: {value}")
```

## Dict Comprehensions
```python
# Basic
squares = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# From two lists
keys = ['a', 'b', 'c']
values = [1, 2, 3]
d = {k: v for k, v in zip(keys, values)}

# With condition
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}

# Swap keys/values
inverted = {v: k for k, v in original.items()}
```

## Sets (Unique Items Only)
```python
# Create
numbers = {1, 2, 3, 4, 5}
empty = set()  # NOT {} - that's a dict!

# From list (removes duplicates)
unique = set([1, 2, 2, 3, 3, 3])  # {1, 2, 3}

# Add/Remove
numbers.add(6)
numbers.remove(3)  # Error if not exists
numbers.discard(3)  # No error if not exists
popped = numbers.pop()  # Remove random item
```

## Set Operations
```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Union (all items)
a | b  # or a.union(b)
# {1, 2, 3, 4, 5, 6}

# Intersection (common items)
a & b  # or a.intersection(b)
# {3, 4}

# Difference (in a but not b)
a - b  # or a.difference(b)
# {1, 2}

# Symmetric difference (not in both)
a ^ b  # or a.symmetric_difference(b)
# {1, 2, 5, 6}

# Check membership
3 in a  # Super fast lookup!
```

## Quick Tips for Tests
- Use dict when you need key-value pairs (most common)
- Use set when you need unique items or fast lookups
- Sets are FAST for checking if item exists
- Can't have duplicate keys in dict (last value wins)
- Dict keys must be immutable (str, int, tuple OK; list NOT OK)
- Use `.get()` to avoid KeyError
- Dict comp > for loop for creating dicts

## Common Patterns
```python
# Count occurrences
counts = {}
for item in items:
    counts[item] = counts.get(item, 0) + 1

# Or use Counter
from collections import Counter
counts = Counter(items)

# Group by property
groups = {}
for item in items:
    key = item['category']
    if key not in groups:
        groups[key] = []
    groups[key].append(item)

# Or use defaultdict
from collections import defaultdict
groups = defaultdict(list)
for item in items:
    groups[item['category']].append(item)
```

---

## Related Notes
- [[Python Lists & Tuples]]
- [[Python Variables & Data Types]]
- [[Python Collections Module]]
- [[Dict Comprehensions Deep Dive]]
- [[Set Operations for Coding Tests]]
