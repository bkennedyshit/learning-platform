---
date: 2026-01-24
title: Python Variables & Data Types
mission: Quick reference for variable assignment, type conversions, and basic data types for coding tests
status: active-reference
tags: [python, basics, variables, data-types, coding-test]
type: code-reference
---

# Python Variables & Data Types

## Variable Assignment
```python
# Basic assignment
name = "Billy"
age = 30
height = 5.10
is_rider = True

# Multiple assignment
x, y, z = 1, 2, 3

# Same value to multiple variables
a = b = c = 0
```

## Data Types
```python
# String
text = "vibe coding"
multiline = """multiple
lines here"""

# Integer
count = 42

# Float
price = 19.99

# Boolean
active = True

# None
result = None

# Check type
type(variable)  # Returns <class 'type'>
```

## Type Conversion
```python
# String to int
num = int("42")

# String to float
price = float("19.99")

# Int to string
text = str(42)

# Float to int (truncates)
whole = int(3.99)  # Returns 3

# String to list
chars = list("hello")  # ['h', 'e', 'l', 'l', 'o']
```

## String Basics
```python
# Concatenation
full_name = first + " " + last

# f-strings (use these!)
message = f"Hello {name}, you are {age} years old"

# Common methods
text.lower()
text.upper()
text.strip()  # Remove whitespace
text.split()  # Split into list
text.replace("old", "new")

# Check contents
"sub" in text  # Returns True/False
text.startswith("prefix")
text.endswith("suffix")
```

## Quick Tips for Tests
- Use f-strings for formatting (cleaner than .format() or %)
- `type()` to check what you're working with
- `str()` everything when debugging/printing
- Python is dynamically typed - variables can change types

---

## Related Notes
- [[Python Lists & Tuples]]
- [[Python Dictionaries & Sets]]
- [[Python String Manipulation]]
- [[Python Type Checking]]
