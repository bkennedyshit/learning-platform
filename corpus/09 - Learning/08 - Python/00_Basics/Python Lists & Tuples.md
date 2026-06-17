---
date: 2026-01-24
title: Python Lists & Tuples
mission: Quick reference for list/tuple operations, slicing, and common patterns for coding tests
status: active-reference
tags: [python, lists, tuples, data-structures, coding-test]
type: code-reference
---

# Python Lists & Tuples

## List Basics
```python
# Create lists
numbers = [1, 2, 3, 4, 5]
mixed = [1, "two", 3.0, True]
empty = []
also_empty = list()

# Access elements
first = numbers[0]
last = numbers[-1]
second_to_last = numbers[-2]

# Slicing
first_three = numbers[0:3]  # or numbers[:3]
last_two = numbers[-2:]
middle = numbers[1:4]
every_other = numbers[::2]
reversed_list = numbers[::-1]
```

## Adding/Removing
```python
# Add items
numbers.append(6)  # Add to end
numbers.insert(0, 0)  # Insert at index
numbers.extend([7, 8, 9])  # Add multiple

# Remove items
numbers.remove(3)  # Remove first occurrence of value
popped = numbers.pop()  # Remove and return last item
popped_index = numbers.pop(0)  # Remove and return at index
del numbers[1]  # Delete at index
numbers.clear()  # Remove all items
```

## Common Operations
```python
# Length
len(numbers)

# Check if exists
3 in numbers  # Returns True/False

# Count occurrences
numbers.count(3)

# Find index
index = numbers.index(3)  # First occurrence

# Sort
numbers.sort()  # In-place
sorted_list = sorted(numbers)  # Returns new list
numbers.sort(reverse=True)  # Descending

# Reverse
numbers.reverse()  # In-place
reversed_list = numbers[::-1]  # Returns new

# Min/Max/Sum
min(numbers)
max(numbers)
sum(numbers)
```

## List Comprehensions (USE THESE!)
```python
# Basic
squares = [x**2 for x in range(10)]

# With condition
evens = [x for x in numbers if x % 2 == 0]

# Transform
names_upper = [name.upper() for name in names]

# Nested (2D)
matrix = [[i*j for j in range(5)] for i in range(5)]
```

## Tuples (Immutable Lists)
```python
# Create
coords = (10, 20)
single = (1,)  # Note the comma!

# Unpack
x, y = coords

# Can't modify!
# coords[0] = 5  # ERROR!

# Use when data shouldn't change
# Slightly faster than lists
# Can be dict keys
```

## Quick Tips for Tests
- List comp > for loop (shows you know Python)
- Use `enumerate()` when you need index: `for i, item in enumerate(list)`
- Use `zip()` to combine lists: `for a, b in zip(list1, list2)`
- Slicing returns new list, doesn't modify original
- Negative indices count from end

---

## Related Notes
- [[Python Variables & Data Types]]
- [[Python Dictionaries & Sets]]
- [[Python Loops & Iteration]]
- [[List Comprehensions Deep Dive]]
- [[Python Sorting & Searching]]
