---
date: 2026-01-24
title: Python File I/O Essentials
mission: Quick reference for reading/writing files, handling paths, and file operations for coding tests
status: active-reference
tags: [python, file-io, reading, writing, paths, coding-test]
type: code-reference
---

# Python File I/O Essentials

## Reading Files
```python
# Read entire file
with open("file.txt", "r") as f:
    content = f.read()

# Read lines as list
with open("file.txt", "r") as f:
    lines = f.readlines()  # ['line1\n', 'line2\n', ...]

# Iterate over lines (BEST for large files)
with open("file.txt", "r") as f:
    for line in f:
        print(line.strip())  # Remove \n

# Read specific number of characters
with open("file.txt", "r") as f:
    chunk = f.read(100)  # First 100 characters
```

## Writing Files
```python
# Write (overwrites file)
with open("file.txt", "w") as f:
    f.write("Hello World\n")
    f.write("Second line\n")

# Append (adds to end)
with open("file.txt", "a") as f:
    f.write("New line\n")

# Write multiple lines
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
with open("file.txt", "w") as f:
    f.writelines(lines)

# Or use loop
with open("file.txt", "w") as f:
    for item in items:
        f.write(f"{item}\n")
```

## File Modes
```python
"r"   # Read (default) - error if file doesn't exist
"w"   # Write - creates new or overwrites
"a"   # Append - creates new or adds to end
"r+"  # Read and write
"w+"  # Write and read (overwrites)
"a+"  # Append and read

"rb"  # Read binary
"wb"  # Write binary
```

## Context Manager (with statement)
```python
# ALWAYS use 'with' - auto closes file
with open("file.txt", "r") as f:
    data = f.read()
# File automatically closed here

# BAD - have to remember to close
f = open("file.txt", "r")
data = f.read()
f.close()  # Easy to forget!
```

## Check if File Exists
```python
import os

# Check if file exists
if os.path.exists("file.txt"):
    print("File exists")

# Check if it's a file (not directory)
if os.path.isfile("file.txt"):
    print("It's a file")

# Check if it's a directory
if os.path.isdir("folder"):
    print("It's a directory")
```

## Working with Paths
```python
import os

# Join paths (works on Windows/Linux/Mac)
path = os.path.join("folder", "subfolder", "file.txt")

# Get current directory
current = os.getcwd()

# Get absolute path
abs_path = os.path.abspath("file.txt")

# Get filename from path
filename = os.path.basename("/path/to/file.txt")  # "file.txt"

# Get directory from path
directory = os.path.dirname("/path/to/file.txt")  # "/path/to"

# Split extension
name, ext = os.path.splitext("file.txt")  # "file", ".txt"
```

## Working with Directories
```python
import os

# List files in directory
files = os.listdir(".")  # Current directory
files = os.listdir("/path/to/folder")

# Create directory
os.mkdir("new_folder")

# Create nested directories
os.makedirs("parent/child/grandchild")

# Remove directory (must be empty)
os.rmdir("folder")

# Remove file
os.remove("file.txt")

# Rename/move file
os.rename("old.txt", "new.txt")
```

## Reading CSV
```python
import csv

# Read CSV
with open("data.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)  # ['col1', 'col2', 'col3']

# Read CSV as dict
with open("data.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["column_name"])
```

## Writing CSV
```python
import csv

# Write CSV
data = [
    ["Name", "Age", "City"],
    ["Billy", "30", "NEPA"],
    ["Alex", "25", "NYC"]
]

with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)

# Write dict to CSV
data = [
    {"name": "Billy", "age": 30},
    {"name": "Alex", "age": 25}
]

with open("output.csv", "w", newline="") as f:
    fieldnames = ["name", "age"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
```

## Reading JSON
```python
import json

# Read JSON file
with open("data.json", "r") as f:
    data = json.load(f)

# Parse JSON string
json_string = '{"name": "Billy", "age": 30}'
data = json.loads(json_string)
```

## Writing JSON
```python
import json

data = {
    "name": "Billy",
    "age": 30,
    "hobbies": ["BMX", "coding", "gaming"]
}

# Write JSON file
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# Convert to JSON string
json_string = json.dumps(data, indent=2)
```

## Common Patterns
```python
# Read file and process lines
def count_words(filename):
    with open(filename, "r") as f:
        return sum(len(line.split()) for line in f)

# Read file into list (remove newlines)
def read_lines(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f]

# Read file and filter
def read_numbers(filename):
    with open(filename, "r") as f:
        return [int(line.strip()) for line in f if line.strip().isdigit()]

# Write list to file
def write_list(filename, items):
    with open(filename, "w") as f:
        for item in items:
            f.write(f"{item}\n")

# Copy file
def copy_file(source, dest):
    with open(source, "r") as src:
        with open(dest, "w") as dst:
            dst.write(src.read())
```

## Error Handling
```python
# Handle file not found
try:
    with open("file.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("File doesn't exist")

# Handle any I/O error
try:
    with open("file.txt", "r") as f:
        content = f.read()
except IOError as e:
    print(f"Error reading file: {e}")

# Check before reading
import os
if os.path.exists("file.txt"):
    with open("file.txt", "r") as f:
        content = f.read()
else:
    print("File not found")
```

## Quick Tips for Tests
- ALWAYS use `with open()` - auto closes files
- Use `"r"` for reading, `"w"` for writing, `"a"` for appending
- `.read()` for entire file, `.readlines()` for list, iterate for large files
- `os.path.join()` for cross-platform paths
- `json.load()` for files, `json.loads()` for strings
- `.strip()` to remove newlines when reading lines
- Remember `newline=""` when writing CSV files

## Common Test Scenarios
```python
# Count lines in file
def count_lines(filename):
    with open(filename, "r") as f:
        return sum(1 for line in f)

# Find word in file
def word_in_file(filename, word):
    with open(filename, "r") as f:
        return any(word in line for line in f)

# Reverse file lines
def reverse_file(input_file, output_file):
    with open(input_file, "r") as f:
        lines = f.readlines()
    with open(output_file, "w") as f:
        f.writelines(reversed(lines))
```

---

## Related Notes
- [[Python String Manipulation]]
- [[Working with JSON]]
- [[CSV Data Processing]]
- [[Path Operations]]
- [[Error Handling in Python]]
