---
date: 2026-01-24
title: Python Error Handling
mission: Quick reference for try/except, raising exceptions, and debugging for coding tests
status: active-reference
tags: [python, error-handling, exceptions, debugging, try-except, coding-test]
type: code-reference
---

# Python Error Handling

## Basic Try/Except
```python
# Catch any error
try:
    result = 10 / 0
except:
    print("An error occurred")

# Catch specific error (BETTER)
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Can't divide by zero")

# Multiple exceptions
try:
    value = int("not a number")
except ValueError:
    print("Invalid number")
except TypeError:
    print("Wrong type")
```

## Common Exception Types
```python
# ValueError - invalid value
int("abc")  # ValueError

# TypeError - wrong type
"2" + 2  # TypeError

# KeyError - dict key doesn't exist
d = {"a": 1}
d["b"]  # KeyError

# IndexError - list index out of range
lst = [1, 2, 3]
lst[10]  # IndexError

# FileNotFoundError - file doesn't exist
open("nonexistent.txt")  # FileNotFoundError

# ZeroDivisionError - divide by zero
10 / 0  # ZeroDivisionError

# AttributeError - attribute doesn't exist
"string".nonexistent_method()  # AttributeError
```

## Exception with Variable
```python
# Capture exception details
try:
    result = int("abc")
except ValueError as e:
    print(f"Error: {e}")
    # Error: invalid literal for int() with base 10: 'abc'
```

## Multiple Exceptions, One Handler
```python
# Catch multiple exception types
try:
    # Some code
    pass
except (ValueError, TypeError) as e:
    print(f"Value or Type error: {e}")
```

## Try/Except/Else/Finally
```python
try:
    file = open("file.txt", "r")
    content = file.read()
except FileNotFoundError:
    print("File not found")
else:
    # Runs if NO exception
    print("File read successfully")
finally:
    # ALWAYS runs (cleanup code)
    if 'file' in locals():
        file.close()
```

## Raising Exceptions
```python
# Raise exception
def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age seems invalid")
    return True

# Raise with custom message
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero!")
    return a / b

# Re-raise exception
try:
    # Some code
    pass
except Exception as e:
    print(f"Logging error: {e}")
    raise  # Re-raise the same exception
```

## Custom Exceptions
```python
# Create custom exception
class InvalidEmailError(Exception):
    pass

def validate_email(email):
    if "@" not in email:
        raise InvalidEmailError("Email must contain @")
    return True

# Use it
try:
    validate_email("notanemail")
except InvalidEmailError as e:
    print(f"Email error: {e}")
```

## Defensive Programming
```python
# Check before operating
def safe_divide(a, b):
    if b == 0:
        return 0  # Or return None, or raise exception
    return a / b

# Validate input
def process_user(user):
    if not user:
        return None
    if not isinstance(user, dict):
        raise TypeError("User must be a dict")
    return user.get("name", "Unknown")

# Use get() for dicts
value = data.get("key", default_value)  # No KeyError

# Check if key exists
if "key" in data:
    value = data["key"]
```

## Common Patterns
```python
# Try to convert, use default if fails
def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

# Read file with fallback
def read_file(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

# Retry logic
def fetch_data(max_retries=3):
    for attempt in range(max_retries):
        try:
            return api_call()
        except ConnectionError:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
```

## Assert Statements
```python
# Assert for debugging (removed in production)
def calculate_average(numbers):
    assert len(numbers) > 0, "List cannot be empty"
    return sum(numbers) / len(numbers)

# Raises AssertionError if condition False
assert x > 0, "X must be positive"
```

## Context Managers for Cleanup
```python
# File automatically closes even if error occurs
try:
    with open("file.txt", "r") as f:
        content = f.read()
        process(content)
except Exception as e:
    print(f"Error: {e}")
# File is closed here regardless
```

## Debugging Tips
```python
# Print debugging
def debug_function(data):
    print(f"DEBUG: data = {data}")
    print(f"DEBUG: type = {type(data)}")
    result = process(data)
    print(f"DEBUG: result = {result}")
    return result

# Check variable types
print(f"Type: {type(variable)}")
print(f"Value: {variable}")
print(f"Dir: {dir(variable)}")  # Available methods

# Interactive debugging
import pdb
pdb.set_trace()  # Pauses execution, interactive prompt
```

## Validation Functions
```python
# Validate and convert
def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        raise ValueError(f"Cannot convert {value} to int")

# Validate range
def validate_range(value, min_val, max_val):
    if not min_val <= value <= max_val:
        raise ValueError(f"Value {value} must be between {min_val} and {max_val}")
    return value

# Validate type
def require_string(value):
    if not isinstance(value, str):
        raise TypeError(f"Expected string, got {type(value)}")
    return value
```

## Quick Tips for Tests
- Catch specific exceptions, not generic `except:`
- Use `try/except/else/finally` for cleanup
- `raise` for validation errors
- `assert` for debugging assumptions
- Check types with `isinstance()`
- Use `.get()` for dicts to avoid KeyError
- Validate input at function entry
- Return default values instead of exceptions when appropriate

## Common Test Scenarios
```python
# Safe list access
def get_item(lst, index, default=None):
    try:
        return lst[index]
    except IndexError:
        return default

# Safe dict access with type conversion
def get_int(data, key, default=0):
    try:
        return int(data[key])
    except (KeyError, ValueError, TypeError):
        return default

# Validate and process
def process_age(age_str):
    try:
        age = int(age_str)
        if age < 0 or age > 150:
            raise ValueError("Invalid age range")
        return age
    except ValueError as e:
        print(f"Error: {e}")
        return None
```

---

## Related Notes
- [[Python Functions Essentials]]
- [[Python File IO Essentials]]
- [[Debugging Strategies]]
- [[Defensive Programming]]
- [[Custom Exceptions]]
