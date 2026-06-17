---
title: "Common Algorithms for Coding Tests"
subject: "00_Basics"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: code-reference
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# Common Algorithms for Coding Tests

## Sorting Algorithms

### Built-in Sort (USE THIS!)
```python
# Sort list in-place
numbers = [3, 1, 4, 1, 5, 9]
numbers.sort()  # Modifies original
numbers.sort(reverse=True)  # Descending

# Return new sorted list
sorted_numbers = sorted(numbers)

# Sort by custom key
names = ["Billy", "Alex", "Christopher"]
sorted_names = sorted(names, key=len)  # Sort by length

# Sort dict items by value
scores = {"Billy": 95, "Alex": 87, "Chris": 92}
sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

### Bubble Sort (Know the concept)
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
```

## Searching Algorithms

### Linear Search
```python
def linear_search(arr, target):
    for i, item in enumerate(arr):
        if item == target:
            return i
    return -1

# Or just use 'in'
if target in arr:
    index = arr.index(target)
```

### Binary Search (Sorted arrays only!)
```python
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

# Or use bisect module
import bisect
index = bisect.bisect_left(arr, target)
```

## Two Pointer Technique
```python
# Find pair that sums to target (sorted array)
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    
    while left < right:
        current_sum = arr[left] + arr[right]
        
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return None

# Reverse string/list
def reverse_in_place(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr

# Check palindrome
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
```

## Sliding Window
```python
# Maximum sum of k consecutive elements
def max_sum_subarray(arr, k):
    if len(arr) < k:
        return None
    
    # Calculate first window
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    # Slide the window
    for i in range(len(arr) - k):
        window_sum = window_sum - arr[i] + arr[i + k]
        max_sum = max(max_sum, window_sum)
    
    return max_sum

# Longest substring without repeating chars
def longest_unique_substring(s):
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

## Hash Map Patterns
```python
# Two sum (unsorted array)
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return None

# First non-repeating character
def first_unique_char(s):
    counts = {}
    for char in s:
        counts[char] = counts.get(char, 0) + 1
    
    for i, char in enumerate(s):
        if counts[char] == 1:
            return i
    return -1

# Group anagrams
def group_anagrams(words):
    groups = {}
    for word in words:
        key = "".join(sorted(word))
        if key not in groups:
            groups[key] = []
        groups[key].append(word)
    return list(groups.values())
```

## Array Manipulation
```python
# Rotate array right by k
def rotate_array(arr, k):
    k = k % len(arr)  # Handle k > len
    return arr[-k:] + arr[:-k]

# Remove duplicates from sorted array
def remove_duplicates(arr):
    if not arr:
        return 0
    
    write_idx = 1
    for i in range(1, len(arr)):
        if arr[i] != arr[i-1]:
            arr[write_idx] = arr[i]
            write_idx += 1
    
    return write_idx

# Or simple (creates new array)
def remove_duplicates_simple(arr):
    return list(dict.fromkeys(arr))  # Preserves order
```

## Recursion Patterns
```python
# Factorial
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Fibonacci
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

# Fibonacci with memoization (BETTER!)
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]

# Sum array recursively
def sum_array(arr):
    if not arr:
        return 0
    return arr[0] + sum_array(arr[1:])
```

## String Algorithms
```python
# Reverse words in string
def reverse_words(s):
    return " ".join(s.split()[::-1])

# Check if strings are anagrams
def are_anagrams(s1, s2):
    return sorted(s1) == sorted(s2)

# Or with Counter
from collections import Counter
def are_anagrams(s1, s2):
    return Counter(s1) == Counter(s2)

# Count substring occurrences
def count_substring(string, substring):
    count = 0
    start = 0
    while True:
        start = string.find(substring, start)
        if start == -1:
            break
        count += 1
        start += 1
    return count
```

## Linked List Patterns (If needed)
```python
# Node class
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Reverse linked list
def reverse_linked_list(head):
    prev = None
    current = head
    
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    
    return prev

# Find middle of linked list
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

## Dynamic Programming Basics
```python
# Climbing stairs (Fibonacci pattern)
def climb_stairs(n):
    if n <= 2:
        return n
    
    prev, curr = 1, 2
    for i in range(3, n + 1):
        prev, curr = curr, prev + curr
    
    return curr

# Maximum subarray sum (Kadane's algorithm)
def max_subarray(nums):
    max_sum = current_sum = nums[0]
    
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

## Quick Tips for Tests
- Use built-in `sorted()` unless they ask for specific algorithm
- Hash maps (dicts) solve most "find/count/group" problems
- Two pointers for sorted arrays or palindromes
- Sliding window for subarray/substring problems
- Recursion + memoization for repeated calculations
- `any()` and `all()` for boolean checks on iterables
- List comprehensions > loops when possible

## Common Test Problems
```python
# FizzBuzz
def fizzbuzz(n):
    for i in range(1, n + 1):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)

# Valid parentheses
def is_valid_parentheses(s):
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in pairs.values():
            stack.append(char)
        elif char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
    
    return len(stack) == 0

# Find missing number (1 to n)
def missing_number(nums):
    n = len(nums) + 1
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(nums)
    return expected_sum - actual_sum
```

---

## Related Notes
- [Python Lists & Tuples](Python-Lists-&-Tuples)
- [Python Dictionaries & Sets](Python-Dictionaries-&-Sets)
- [Python Loops & Iteration](Python-Loops-&-Iteration)
- [Recursion Patterns](Recursion-Patterns)
- [Time Complexity Basics](Time-Complexity-Basics)
- [Big O Notation](Big-O-Notation)
