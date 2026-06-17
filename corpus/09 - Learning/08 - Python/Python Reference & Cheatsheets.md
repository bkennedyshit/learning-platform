---
date: 2026-05-26
title: "Python Reference & Cheatsheets"
tags: [learning, python]
status: reference
type: reference
---

# Python Reference & Cheatsheets

> **Quick access to Python fundamentals, syntax, and visual cheatsheets**

---

## 📸 Visual Cheatsheets

### Control Flow & Exceptions
![Control Flow & Exceptions](file:///D:/python%20learning/control_flow_exceptions.png)

### Class Definitions
![Class Definitions](file:///D:/python%20learning/definitions_classes.png)

### File I/O, Lambda & Comprehensions
![File I/O, Lambda & Comprehensions](file:///D:/python%20learning/file_io_lambda_comprehensions.png)

### Literals Cheatsheet
![Literals Cheatsheet](file:///D:/python%20learning/literals_cheatsheet.png)

### Modules & Packages
![Modules & Packages](file:///D:/python%20learning/modules_and_packages.png)

---

## 📚 Quick Reference Guide

**For technical assessments & daily use**

---

## Data Types

```python
# Strings
name = "Billy"
name = 'Billy'
multiline = """Multiple
lines"""

# Numbers
integer = 42
floating = 3.14
negative = -10

# Boolean
is_active = True
is_done = False

# None (null equivalent)
empty = None
```

---

## Data Structures

### Lists (ordered, mutable)
```python
# Create
my_list = [1, 2, 3, 4, 5]
empty_list = []

# Access
first = my_list[0]       # 1
last = my_list[-1]       # 5
slice = my_list[1:3]     # [2, 3]

# Modify
my_list.append(6)        # Add to end
my_list.insert(0, 0)     # Insert at index
my_list.remove(3)        # Remove first occurrence of value
my_list.pop()            # Remove & return last
my_list.pop(0)           # Remove & return at index

# Common operations
len(my_list)             # Length
my_list.sort()           # Sort in place
sorted(my_list)          # Return sorted copy
my_list.reverse()        # Reverse in place
3 in my_list             # Check membership
my_list.index(3)         # Find index of value
my_list.count(3)         # Count occurrences
```

### Dictionaries (key-value, mutable)
```python
# Create
my_dict = {"name": "Billy", "age": 33}
empty_dict = {}

# Access
name = my_dict["name"]           # Raises KeyError if missing
name = my_dict.get("name")       # Returns None if missing
name = my_dict.get("name", "default")  # Returns default if missing

# Modify
my_dict["city"] = "Plains"       # Add/update
del my_dict["age"]               # Delete key
my_dict.pop("age")               # Remove & return value

# Common operations
my_dict.keys()                   # All keys
my_dict.values()                 # All values
my_dict.items()                  # Key-value pairs as tuples
"name" in my_dict                # Check if key exists
my_dict.update({"new": "value"}) # Merge another dict
```

### Sets (unordered, unique values)
```python
# Create
my_set = {1, 2, 3}
empty_set = set()  # NOT {} (that's a dict)

# Modify
my_set.add(4)               # Add element
my_set.remove(2)            # Remove (raises error if missing)
my_set.discard(2)           # Remove (no error if missing)

# Set operations
set1 | set2                 # Union
set1 & set2                 # Intersection
set1 - set2                 # Difference
set1 ^ set2                 # Symmetric difference
```

### Tuples (ordered, immutable)
```python
# Create
my_tuple = (1, 2, 3)
single = (1,)               # Need comma for single element

# Access (same as list)
first = my_tuple[0]
```

---

## Control Flow

### If/Else
```python
if condition:
    # do something
elif other_condition:
    # do something else
else:
    # default

# Ternary
result = "yes" if condition else "no"
```

### Loops
```python
# For loop
for item in my_list:
    print(item)

for i in range(5):          # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 5):       # 2, 3, 4
    print(i)

for i, item in enumerate(my_list):  # Index and value
    print(i, item)

for key, value in my_dict.items():
    print(key, value)

# While loop
while condition:
    # do something
    if should_stop:
        break
    if should_skip:
        continue
```

### List Comprehensions
```python
# Basic
squares = [x**2 for x in range(10)]

# With condition
evens = [x for x in range(10) if x % 2 == 0]

# Dict comprehension
squared = {x: x**2 for x in range(5)}

# Set comprehension
unique = {x for x in my_list}
```

---

## Functions

```python
# Basic function
def greet(name):
    return f"Hello, {name}"

# Default arguments
def greet(name="World"):
    return f"Hello, {name}"

# Multiple return values
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers)

minimum, maximum, total = get_stats([1, 2, 3])

# *args (variable positional arguments)
def sum_all(*args):
    return sum(args)

# **kwargs (variable keyword arguments)
def make_dict(**kwargs):
    return kwargs

# Lambda (anonymous function)
square = lambda x: x**2
sorted_list = sorted(my_list, key=lambda x: x["name"])
```

---

## Classes

```python
class Person:
    # Class variable (shared by all instances)
    species = "Human"
    
    # Constructor
    def __init__(self, name, age):
        self.name = name      # Instance variable
        self.age = age
    
    # Instance method
    def greet(self):
        return f"Hi, I'm {self.name}"
    
    # String representation
    def __str__(self):
        return f"Person({self.name}, {self.age})"
    
    # Class method
    @classmethod
    def create_anonymous(cls):
        return cls("Anonymous", 0)
    
    # Static method
    @staticmethod
    def is_adult(age):
        return age >= 18

# Inheritance
class Employee(Person):
    def __init__(self, name, age, job):
        super().__init__(name, age)
        self.job = job
```

---

## String Methods

```python
s = "Hello World"

s.lower()           # "hello world"
s.upper()           # "HELLO WORLD"
s.strip()           # Remove whitespace from ends
s.split(" ")        # ["Hello", "World"]
s.replace("o", "0") # "Hell0 W0rld"
s.startswith("H")   # True
s.endswith("d")     # True
s.find("o")         # 4 (index of first occurrence)
s.count("o")        # 2
"lo" in s           # True

# Join
", ".join(["a", "b", "c"])  # "a, b, c"

# F-strings (formatting)
name = "Billy"
age = 33
f"Name: {name}, Age: {age}"
f"Padded: {age:05d}"        # "00033"
f"Float: {3.14159:.2f}"     # "3.14"
```

---

## File I/O

```python
# Read entire file
with open("file.txt", "r") as f:
    content = f.read()

# Read lines
with open("file.txt", "r") as f:
    lines = f.readlines()

# Read line by line
with open("file.txt", "r") as f:
    for line in f:
        print(line.strip())

# Write
with open("file.txt", "w") as f:
    f.write("Hello\n")
    f.writelines(["Line 1\n", "Line 2\n"])

# Append
with open("file.txt", "a") as f:
    f.write("Appended line\n")
```

---

## Error Handling

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Can't divide by zero")
except Exception as e:
    print(f"Error: {e}")
else:
    print("No error occurred")
finally:
    print("Always runs")

# Raise exception
raise ValueError("Invalid input")
```

---

## Common Algorithms

### Sorting
```python
# Built-in sort (in place)
my_list.sort()
my_list.sort(reverse=True)
my_list.sort(key=lambda x: x["name"])

# Sorted (returns new list)
sorted_list = sorted(my_list)
```

### Searching
```python
# Linear search
def linear_search(arr, target):
    for i, item in enumerate(arr):
        if item == target:
            return i
    return -1

# Binary search (requires sorted array)
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

---

## 📂 Additional Resources

**Source Location:** `D:\python learning\`

**Other Cheatsheets Available:**
- [Bash Quick Reference](D:\python learning\cheatsheets\Bash Quick Reference.md)
- [CSS Quick Reference](D:\python learning\cheatsheets\CSS Quick Reference.md)
- [Git Quick Reference](D:\python learning\cheatsheets\Git Quick Reference.md)
- [HTML Quick Reference](D:\python learning\cheatsheets\HTML Quick Reference.md)
- [JavaScript Quick Reference](D:\python learning\cheatsheets\JavaScript Quick Reference.md)
- [SQL Quick Reference](D:\python learning\cheatsheets\SQL Quick Reference.md)
- [TypeScript Quick Reference](D:\python learning\cheatsheets\TypeScript Quick Reference.md)

**Practice Examples:** `D:\python learning\learning\examples\`

---

## Related Notes
- [[08.13 - Algorithms & Data Structures in Python]] - Same Python folder
- [[08.1 - Setup, Tooling & Project Structure]] - Same Python folder
- [[08.10 - Operating Systems Essentials]] - Same Python folder
- [[08.11 - Computer Networks Essentials]] - Same Python folder
- [[08.12 - Computer Architecture - Performance Intuition]] - Same Python folder
