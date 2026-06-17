---
date: 2026-01-24
title: Python String Manipulation
mission: Quick reference for string operations, formatting, and common patterns for coding tests
status: active-reference
tags: [python, strings, manipulation, formatting, coding-test]
type: code-reference
---

# Python String Manipulation

## String Creation & Formatting
```python
# F-strings (BEST - use these!)
name = "Billy"
age = 30
message = f"I'm {name}, {age} years old"
calc = f"2 + 2 = {2 + 2}"

# Format method
message = "I'm {}, {} years old".format(name, age)
message = "I'm {name}, {age} years old".format(name=name, age=age)

# Old style (don't use unless legacy code)
message = "I'm %s, %d years old" % (name, age)
```

## Common Methods
```python
text = "  Hello World  "

# Case
text.lower()           # "  hello world  "
text.upper()           # "  HELLO WORLD  "
text.capitalize()      # "  hello world  "
text.title()           # "  Hello World  "

# Whitespace
text.strip()           # "Hello World"
text.lstrip()          # "Hello World  "
text.rstrip()          # "  Hello World"

# Split & Join
words = text.split()   # ['Hello', 'World']
"_".join(words)        # "Hello_World"
",".join(['a','b'])    # "a,b"

# Replace
text.replace("World", "Python")  # "  Hello Python  "
```

## Checking & Searching
```python
text = "Hello World"

# Contains
"World" in text        # True
"world" in text        # False (case sensitive!)

# Starts/Ends with
text.startswith("Hello")  # True
text.endswith("World")    # True

# Find position
text.find("World")     # Returns 6 (index)
text.find("xyz")       # Returns -1 (not found)
text.index("World")    # Returns 6 (raises error if not found)

# Count
text.count("l")        # 3
```

## String Validation
```python
# Check type
"123".isdigit()        # True
"abc".isalpha()        # True
"abc123".isalnum()     # True
"   ".isspace()        # True
"Hello World".istitle() # True
"HELLO".isupper()      # True
"hello".islower()      # True
```

## Slicing & Indexing
```python
text = "Python"

# Access
text[0]                # 'P'
text[-1]               # 'n'

# Slicing
text[0:3]              # 'Pyt'
text[:3]               # 'Pyt'
text[3:]               # 'hon'
text[-3:]              # 'hon'
text[::-1]             # 'nohtyP' (reverse!)

# Every nth character
text[::2]              # 'Pto'
```

## String Building
```python
# BAD - creates new string each time!
result = ""
for word in words:
    result += word + " "

# GOOD - use join
result = " ".join(words)

# GOOD - use list then join
parts = []
for word in words:
    parts.append(word.upper())
result = " ".join(parts)

# BEST - list comp + join
result = " ".join([word.upper() for word in words])
```

## Common Patterns
```python
# Reverse string
reversed_text = text[::-1]

# Remove all whitespace
no_spaces = "".join(text.split())

# Palindrome check
is_palindrome = text == text[::-1]

# Count vowels
vowels = "aeiou"
count = sum(1 for char in text.lower() if char in vowels)

# Remove duplicates (keeping order)
seen = set()
unique = "".join([c for c in text if c not in seen and not seen.add(c)])
```

## Multi-line Strings
```python
# Triple quotes
long_text = """This is
a multi-line
string"""

# Join lines
lines = [
    "First line",
    "Second line",
    "Third line"
]
text = "\n".join(lines)
```

## Quick Tips for Tests
- Use f-strings for formatting (shows modern Python knowledge)
- Strings are immutable - methods return new strings
- Use `.join()` for building strings from lists (WAY faster than +=)
- Remember `[::-1]` for reverse
- `in` is case-sensitive
- String methods don't modify original, they return new strings

---

## Related Notes
- [[Python Variables & Data Types]]
- [[Python Lists & Tuples]]
- [[String Algorithms]]
- [[Regular Expressions Basics]]
- [[Python Input & Output]]
