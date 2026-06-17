---
title: "Python Conditionals & Logic"
subject: "01_Control Flow"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: code-reference
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# Python Conditionals & Logic

## Basic If/Elif/Else
```python
age = 30

if age < 18:
    print("Minor")
elif age < 65:
    print("Adult")
else:
    print("Senior")
```

## Comparison Operators
```python
# Equality
x == y   # Equal to
x != y   # Not equal to

# Comparison
x < y    # Less than
x > y    # Greater than
x <= y   # Less than or equal
x >= y   # Greater than or equal

# Identity
x is y   # Same object
x is not y

# Membership
item in list
item not in list
```

## Boolean Logic
```python
# AND - both must be True
if age >= 18 and age < 65:
    print("Working age")

# OR - at least one must be True
if day == "Saturday" or day == "Sunday":
    print("Weekend")

# NOT - inverse
if not is_raining:
    print("Go outside")

# Combining
if (age >= 18 and age < 65) or is_student:
    print("Active")
```

## Truthy and Falsy Values
```python
# Falsy values (evaluate to False)
False
None
0
0.0
""       # Empty string
[]       # Empty list
{}       # Empty dict
()       # Empty tuple
set()    # Empty set

# Everything else is Truthy

# Check if list has items
if items:  # Better than: if len(items) > 0
    print("Has items")

# Check if string is empty
if not text:  # Better than: if text == ""
    print("Empty string")

# Check if value exists
if value:  # Better than: if value is not None
    print("Has value")
```

## Ternary Operator (One-liner If)
```python
# Instead of:
if age >= 18:
    status = "Adult"
else:
    status = "Minor"

# Use:
status = "Adult" if age >= 18 else "Minor"

# Nested ternary (try to avoid - hard to read)
status = "Senior" if age >= 65 else "Adult" if age >= 18 else "Minor"
```

## Multiple Conditions
```python
# Check multiple values (OR)
if x == 1 or x == 2 or x == 3:
    print("One, two, or three")

# Better - use 'in'
if x in [1, 2, 3]:
    print("One, two, or three")

# Even better for many values
if x in {1, 2, 3}:  # Set - faster lookup
    print("One, two, or three")

# Check range
if 18 <= age < 65:
    print("Working age")
```

## Match/Case (Python 3.10+)
```python
# Like switch/case in other languages
command = "start"

match command:
    case "start":
        print("Starting...")
    case "stop":
        print("Stopping...")
    case "pause":
        print("Pausing...")
    case _:  # Default
        print("Unknown command")

# With conditions
match age:
    case age if age < 18:
        print("Minor")
    case age if age < 65:
        print("Adult")
    case _:
        print("Senior")
```

## Guard Clauses (Early Return)
```python
# BAD - nested if
def process_user(user):
    if user is not None:
        if user.is_active:
            if user.has_permission:
                # Do stuff
                return result
    return None

# GOOD - guard clauses
def process_user(user):
    if user is None:
        return None
    if not user.is_active:
        return None
    if not user.has_permission:
        return None
    
    # Do stuff
    return result
```

## Conditional Expressions
```python
# Get value or default
name = user_input or "Anonymous"
count = items.get("count") or 0

# Chain with and
result = valid and process_data()  # Only calls process_data if valid=True

# Short-circuit evaluation
if user and user.is_active:  # Won't check is_active if user is None
    print("Active user")
```

## Common Patterns
```python
# Check if in range
def is_valid_age(age):
    return 0 <= age <= 150

# Check type
if isinstance(value, str):
    print("It's a string")

if isinstance(value, (int, float)):
    print("It's a number")

# Check multiple conditions
def can_vote(age, is_citizen):
    return age >= 18 and is_citizen

# Validate input
def validate_email(email):
    if not email:
        return False
    if "@" not in email:
        return False
    if "." not in email:
        return False
    return True

# Or simpler
def validate_email(email):
    return email and "@" in email and "." in email
```

## None Checking
```python
# Check if None
if value is None:
    print("No value")

# Check if NOT None
if value is not None:
    print("Has value")

# Get value or default
result = value if value is not None else default

# Or use get with dict
result = data.get("key", default_value)
```

## Quick Tips for Tests
- Use `in` for checking multiple values
- Use truthy/falsy instead of explicit comparisons
- Guard clauses > nested ifs
- `is` for None checks, `==` for value checks
- Ternary operator for simple if/else
- Use `any()` and `all()` for list conditions
- Short-circuit evaluation with `and`/`or`

## Common Test Scenarios
```python
# Palindrome check
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

# Even/odd
def is_even(n):
    return n % 2 == 0

# Prime check (basic)
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# FizzBuzz logic
def fizzbuzz(n):
    if n % 15 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)
```

---

## Related Notes
- [Python Variables & Data Types](Python-Variables-&-Data-Types)
- [Python Functions Essentials](Python-Functions-Essentials)
- [Python Loops & Iteration](Python-Loops-&-Iteration)
- [Boolean Logic Deep Dive](Boolean-Logic-Deep-Dive)
- [Guard Clauses Pattern](Guard-Clauses-Pattern)
