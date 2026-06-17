---
title: "Python Functions Essentials"
subject: "02_Functions"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: code-reference
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# Python Functions Essentials

## Basic Function
```python
# Define
def greet(name):
    return f"Hello, {name}!"

# Call
message = greet("Billy")
```

## Multiple Parameters
```python
def calculate(a, b, operation="add"):
    if operation == "add":
        return a + b
    elif operation == "multiply":
        return a * b
    return None

# Call
result = calculate(5, 3)              # 8
result = calculate(5, 3, "multiply")  # 15
```

## Return Values
```python
# Single value
def add(a, b):
    return a + b

# Multiple values (returns tuple)
def min_max(numbers):
    return min(numbers), max(numbers)

min_val, max_val = min_max([1, 2, 3, 4, 5])

# Early return
def is_even(n):
    if n % 2 == 0:
        return True
    return False

# Or simpler
def is_even(n):
    return n % 2 == 0
```

## Default Parameters
```python
def power(base, exponent=2):
    return base ** exponent

power(5)      # 25 (default exponent=2)
power(5, 3)   # 125
```

## *args and **kwargs
```python
# *args - variable number of positional arguments
def sum_all(*args):
    return sum(args)

sum_all(1, 2, 3, 4, 5)  # 15

# **kwargs - variable number of keyword arguments
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Billy", age=30, sport="BMX")

# Both together
def flexible(*args, **kwargs):
    print(f"Args: {args}")
    print(f"Kwargs: {kwargs}")

flexible(1, 2, 3, name="Billy", age=30)
```

## Lambda Functions (One-liners)
```python
# Regular function
def square(x):
    return x ** 2

# Lambda equivalent
square = lambda x: x ** 2

# Common use: with map/filter/sorted
numbers = [1, 2, 3, 4, 5]

# Map
squared = list(map(lambda x: x ** 2, numbers))

# Filter
evens = list(filter(lambda x: x % 2 == 0, numbers))

# Sorted with custom key
names = ["Billy", "Alex", "Christopher"]
sorted_names = sorted(names, key=lambda x: len(x))
```

## Type Hints (Optional but Pro)
```python
def add(a: int, b: int) -> int:
    return a + b

def greet(name: str) -> str:
    return f"Hello, {name}!"

from typing import List, Dict, Optional

def process_numbers(nums: List[int]) -> Dict[str, int]:
    return {
        "sum": sum(nums),
        "max": max(nums)
    }

def find_user(user_id: int) -> Optional[Dict]:
    # Returns dict or None
    if user_id in users:
        return users[user_id]
    return None
```

## Scope
```python
x = 10  # Global

def test():
    x = 5  # Local
    print(x)  # 5

test()
print(x)  # 10

# Modify global
def modify_global():
    global x
    x = 20

modify_global()
print(x)  # 20
```

## Common Patterns
```python
# Validation function
def validate_email(email):
    return "@" in email and "." in email

# Transform function
def normalize_name(name):
    return name.strip().title()

# Predicate function (returns bool)
def is_adult(age):
    return age >= 18

# Factory function
def create_user(name, age):
    return {
        "name": name,
        "age": age,
        "created_at": datetime.now()
    }

# Helper function
def safe_divide(a, b):
    return a / b if b != 0 else 0
```

## Recursion Basics
```python
# Factorial
def factorial(n):
    if n <= 1:  # Base case
        return 1
    return n * factorial(n - 1)  # Recursive case

# Fibonacci
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

# Sum list recursively
def sum_list(numbers):
    if not numbers:
        return 0
    return numbers[0] + sum_list(numbers[1:])
```

## Quick Tips for Tests
- Keep functions small and focused (one job)
- Use descriptive names (`calculate_total` not `calc`)
- Return early to avoid nested if/else
- Use type hints to show you know modern Python
- Lambda for simple one-liners with map/filter/sorted
- Don't forget the `return` statement!
- Functions without `return` return `None`

---

## Related Notes
- [Python Variables & Data Types](Python-Variables-&-Data-Types)
- [Python Control Flow](Python-Control-Flow)
- [Lambda Functions Deep Dive](Lambda-Functions-Deep-Dive)
- [Recursion Patterns](Recursion-Patterns)
- [Function Decorators](Function-Decorators)
- [Type Hints & Annotations](Type-Hints-&-Annotations)
