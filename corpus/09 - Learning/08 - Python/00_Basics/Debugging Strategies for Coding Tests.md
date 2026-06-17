---
date: 2026-01-24
title: Debugging Strategies for Coding Tests
mission: Practical debugging techniques and troubleshooting approaches for coding interviews
status: active-reference
tags: [debugging, troubleshooting, coding-test, python, strategies]
type: code-reference
---

# Debugging Strategies for Coding Tests

## Print Debugging (Fast & Effective)
```python
# Basic print
def buggy_function(data):
    print(f"DEBUG: Input data = {data}")
    result = process(data)
    print(f"DEBUG: Result = {result}")
    return result

# Print type
print(f"Type: {type(variable)}")
print(f"Value: {variable}")

# Print with context
print(f"At line 42: x={x}, y={y}, sum={x+y}")

# Separator for clarity
print("="*50)
print("DEBUG START")
print(variable)
print("DEBUG END")
print("="*50)
```

## Common Bugs & Solutions

### Off-by-One Errors
```python
# BAD - misses last item
for i in range(len(items)):  # Should be range(len(items)+1) or just iterate items

# GOOD
for item in items:
    process(item)

# Or if you need index
for i, item in enumerate(items):
    print(f"Item {i}: {item}")
```

### Type Errors
```python
# Check types
if not isinstance(value, str):
    raise TypeError(f"Expected str, got {type(value)}")

# Debug types
def debug_types(data):
    print(f"Type: {type(data)}")
    if isinstance(data, list):
        print(f"Length: {len(data)}")
        if data:
            print(f"First item type: {type(data[0])}")
```

### None vs Empty
```python
# Wrong - None vs empty string/list
if result:  # This fails for empty list []
    process(result)

# Correct - explicit check
if result is not None:
    process(result)

# Or
if len(result) > 0:
    process(result)
```

### Mutable Default Arguments (GOTCHA!)
```python
# BAD - list is shared across calls!
def append_to(item, list=[]):
    list.append(item)
    return list

print(append_to(1))  # [1]
print(append_to(2))  # [1, 2] - NOT [2]!

# GOOD
def append_to(item, list=None):
    if list is None:
        list = []
    list.append(item)
    return list
```

## Systematic Debugging Process

### 1. Reproduce the Bug
```python
# Create minimal test case
def test_bug():
    input_data = [1, 2, 3]
    expected = 6
    actual = sum_list(input_data)
    print(f"Expected: {expected}, Got: {actual}")
    assert actual == expected, f"Failed: {actual} != {expected}"
```

### 2. Isolate the Problem
```python
# Binary search for bug location
def complex_function(data):
    print("A: Starting")
    result1 = step1(data)
    print(f"B: After step1: {result1}")
    result2 = step2(result1)
    print(f"C: After step2: {result2}")
    result3 = step3(result2)
    print(f"D: After step3: {result3}")
    return result3
```

### 3. Check Assumptions
```python
# Verify input assumptions
def process_data(data):
    assert isinstance(data, list), "Data must be list"
    assert len(data) > 0, "Data cannot be empty"
    assert all(isinstance(x, int) for x in data), "All items must be ints"
    
    # Now process
    return sum(data)
```

## Common Problem Patterns

### Index Out of Range
```python
# Check bounds
def safe_access(lst, index):
    if 0 <= index < len(lst):
        return lst[index]
    return None

# Or use try/except
def safe_access(lst, index):
    try:
        return lst[index]
    except IndexError:
        return None
```

### Infinite Loops
```python
# Add safety counter
def find_value(items, target, max_iterations=1000):
    i = 0
    iterations = 0
    
    while i < len(items):
        iterations += 1
        if iterations > max_iterations:
            raise RuntimeError(f"Exceeded max iterations: {max_iterations}")
        
        if items[i] == target:
            return i
        i += 1
    
    return -1

# Or add debug counter
while condition:
    iteration_count += 1
    if iteration_count % 100 == 0:
        print(f"Iteration {iteration_count}")
```

### String/List Slicing Confusion
```python
# Test slicing separately
text = "Python"
print(f"text[:3] = {text[:3]}")      # "Pyt"
print(f"text[3:] = {text[3:]}")      # "hon"
print(f"text[-1] = {text[-1]}")      # "n"
print(f"text[::-1] = {text[::-1]}")  # "nohtyP"

# Common mistake: forgetting slicing creates new object
original = [1, 2, 3]
sliced = original[:2]
sliced.append(4)
print(original)  # Still [1, 2, 3] - not modified!
```

### Variable Scope Issues
```python
# Global vs local
x = 10

def test():
    x = 5  # This is local x
    print(f"Inside: {x}")

test()  # Prints 5
print(f"Outside: {x}")  # Still 10

# If you need to modify global
def test2():
    global x
    x = 5

test2()
print(x)  # Now 5
```

## Interactive Debugging

### Python Debugger (pdb)
```python
import pdb

def buggy_function(data):
    result = process_step1(data)
    pdb.set_trace()  # Execution stops here
    result = process_step2(result)
    return result

# Common pdb commands:
# n (next) - next line
# s (step) - step into function
# c (continue) - continue execution
# p variable - print variable
# l - list source code
# q - quit debugger
```

### Assert for Testing
```python
# Use asserts to verify assumptions
def divide(a, b):
    assert b != 0, "Cannot divide by zero"
    return a / b

# Test invariants
def binary_search(arr, target):
    assert arr == sorted(arr), "Array must be sorted"
    # ... search logic
```

## Logging (Better than Print for Production)
```python
import logging

logging.basicConfig(level=logging.DEBUG)

def process_data(data):
    logging.debug(f"Processing data: {data}")
    result = transform(data)
    logging.info(f"Transformed to: {result}")
    return result

# Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## Testing Edge Cases
```python
def test_function(func):
    # Empty input
    assert func([]) == expected_for_empty
    
    # Single item
    assert func([1]) == expected_for_one
    
    # Two items
    assert func([1, 2]) == expected_for_two
    
    # Duplicates
    assert func([1, 1, 1]) == expected_for_duplicates
    
    # Negative numbers
    assert func([-1, -2]) == expected_for_negatives
    
    # Large numbers
    assert func([1000000]) == expected_for_large
    
    # Mixed
    assert func([-5, 0, 5]) == expected_for_mixed
```

## Quick Debug Checklist
```
□ Print input values
□ Print variable types
□ Check for None values
□ Verify list/string not empty
□ Check loop conditions
□ Test with simple input first
□ Test edge cases (empty, one item, negative)
□ Verify function returns something
□ Check variable scope (global vs local)
□ Look for off-by-one errors
□ Check mutable default arguments
□ Verify comparisons (== vs is)
□ Check indentation (Python!)
```

## Common Interview Debugging Scenarios
```python
# 1. Fix the IndexError
def get_last(items):
    # Bug: fails on empty list
    # return items[-1]
    # Fix:
    return items[-1] if items else None

# 2. Fix the infinite loop
def count_down(n):
    # Bug: infinite if n <= 0
    # while n > 0:
    #     print(n)
    # Fix:
    while n > 0:
        print(n)
        n -= 1

# 3. Fix the mutable default
def add_item(item, list=None):
    if list is None:
        list = []
    list.append(item)
    return list

# 4. Fix the variable scope
total = 0
def add_to_total(n):
    global total
    total += n
    return total

# 5. Fix the type error
def process(value):
    # Ensure value is string
    if not isinstance(value, str):
        value = str(value)
    return value.upper()
```

## Pro Tips for Coding Tests
- **Start simple**: Test with easiest case first
- **Print everything**: Types, values, intermediate results
- **One change at a time**: Don't fix multiple things simultaneously
- **Test edge cases**: Empty, one item, negative, duplicates
- **Read error messages**: They tell you line number and error type
- **Rubber duck debugging**: Explain code line-by-line out loud
- **Use descriptive variable names**: Makes bugs obvious
- **Write tests first**: Know what correct output looks like

---

## Related Notes
- [[Python Error Handling]]
- [[Python Functions Essentials]]
- [[Common Algorithms for Coding Tests]]
- [[Testing Patterns]]
- [[Python Debugging Tools]]
