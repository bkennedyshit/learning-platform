---
title: "08.13 — Algorithms & Data Structures in Python"
subject: "Python"
catalog: advanced
audience_tier: higher-education
chapter: "8.13"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 08.13 — Algorithms & Data Structures in Python

> *"Bad programmers worry about the code. Good programmers worry about data structures and their relationships."* — Linus Torvalds

Algorithms are not just interview fodder. They're the foundation of every optimizer, every search engine, every ML training loop. Understanding time/space complexity lets you predict whether your code will finish in seconds or centuries.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Analyze time and space complexity using Big-O notation rigorously.
2. Implement and analyze: sorting (merge, quick, heap), searching (binary, hash), graph algorithms (BFS, DFS, Dijkstra).
3. Apply dynamic programming to optimization problems.
4. Use Python's built-in data structures optimally (dict=hash table, list=dynamic array, heapq=min-heap).
5. Recognize algorithm patterns: sliding window, two pointers, divide & conquer, greedy.
6. Connect algorithms to ML: gradient descent as optimization, attention as matrix multiplication.

---

## 🖼️ Visual Anchor — Algorithm Complexity Growth Rates

![python__1.13-fig1](python__1.13-fig1.svg)

---

## 📚 1. Definitions / Concepts

### Definition 08.13.1 — Big-O Notation

$f(n) = O(g(n))$ means there exist constants $c > 0$ and $n_0$ such that $f(n) \leq c \cdot g(n)$ for all $n \geq n_0$.

Informally: $O(g(n))$ is the **upper bound** on growth rate, ignoring constants and lower-order terms.

| Complexity | Name | Example | n=10⁶ operations |
|-----------|------|---------|-------------------|
| $O(1)$ | Constant | Hash lookup | 1 |
| $O(\log n)$ | Logarithmic | Binary search | 20 |
| $O(n)$ | Linear | Array scan | 10⁶ |
| $O(n \log n)$ | Linearithmic | Merge sort | 2×10⁷ |
| $O(n^2)$ | Quadratic | Nested loops | 10¹² ❌ |
| $O(2^n)$ | Exponential | Brute force subsets | ∞ ❌ |

### Definition 08.13.2 — Abstract Data Types vs Implementations

| ADT | Operations | Python Implementation | Complexity |
|-----|-----------|----------------------|-----------|
| Stack | push, pop, peek | `list` (append/pop) | O(1) |
| Queue | enqueue, dequeue | `collections.deque` | O(1) |
| Priority Queue | insert, extract-min | `heapq` | O(log n) |
| Hash Map | get, set, delete | `dict` | O(1) average |
| Set | add, remove, contains | `set` | O(1) average |
| Sorted Container | insert, search, range | `sortedcontainers.SortedList` | O(log n) |

### Definition 08.13.3 — Graph Representations

```python
# Adjacency list (preferred for sparse graphs)
graph: dict[str, list[str]] = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["D", "E"],
    "D": [],
    "E": [],
}

# Adjacency matrix (preferred for dense graphs, GPU operations)
import numpy as np
adj_matrix = np.array([
    [0, 1, 1, 0, 0],  # A
    [0, 0, 0, 1, 0],  # B
    [0, 0, 0, 1, 1],  # C
    [0, 0, 0, 0, 0],  # D
    [0, 0, 0, 0, 0],  # E
])
```

---

## 📐 2. Mental Models / Principles

### Principle 1.13.1 — The Algorithm Design Paradigms

| Paradigm | When to Use | Example |
|----------|-------------|---------|
| **Divide & Conquer** | Problem splits into independent subproblems | Merge sort, FFT |
| **Dynamic Programming** | Overlapping subproblems + optimal substructure | Shortest path, sequence alignment |
| **Greedy** | Local optimal choice leads to global optimal | Huffman coding, Dijkstra |
| **Backtracking** | Explore all possibilities, prune invalid | N-Queens, Sudoku |
| **Two Pointers** | Sorted array, find pairs/subarrays | Two-sum (sorted), container with most water |
| **Sliding Window** | Contiguous subarray/substring optimization | Max sum subarray, longest substring |

### Principle 1.13.2 — Python's Built-in Complexity Guarantees

```python
# list operations
lst[i]           # O(1) — random access
lst.append(x)    # O(1) amortized
lst.insert(0, x) # O(n) — shifts everything
lst.pop()        # O(1) — from end
lst.pop(0)       # O(n) — from front
x in lst         # O(n) — linear scan
sorted(lst)      # O(n log n) — Timsort

# dict operations
d[key]           # O(1) average
d[key] = val     # O(1) average
key in d         # O(1) average
del d[key]       # O(1) average

# set operations
s.add(x)         # O(1) average
x in s           # O(1) average
s & t            # O(min(len(s), len(t)))
s | t            # O(len(s) + len(t))
```

### Principle 1.13.3 — Connection to ML

- **Gradient descent** = greedy optimization on a loss landscape
- **Attention mechanism** = $O(n^2)$ pairwise comparison (why transformers are expensive)
- **KD-trees / LSH** = approximate nearest neighbor for embeddings
- **Dynamic programming** = Viterbi algorithm (sequence models), beam search (LLM decoding)
- **Graph algorithms** = computation graphs, neural architecture search

---

## 🔑 3. Mechanics

### 3.1 — Sorting Algorithms

```python
def merge_sort(arr: list[int]) -> list[int]:
    """O(n log n) time, O(n) space — stable, predictable."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left: list[int], right: list[int]) -> list[int]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Python's built-in: Timsort (hybrid merge+insertion sort)
# Always use sorted() or list.sort() in production — it's optimized in C
```

### 3.2 — Graph Algorithms

```python
from collections import deque
import heapq

def bfs(graph: dict[str, list[str]], start: str) -> list[str]:
    """Breadth-first search — shortest path in unweighted graphs."""
    visited = set()
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        queue.extend(graph.get(node, []))
    return order

def dijkstra(graph: dict[str, list[tuple[str, float]]], start: str) -> dict[str, float]:
    """Shortest path in weighted graphs — O((V+E) log V) with min-heap."""
    dist: dict[str, float] = {start: 0}
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, float('inf')):
            continue
        for v, weight in graph.get(u, []):
            new_dist = d + weight
            if new_dist < dist.get(v, float('inf')):
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))
    return dist
```

### 3.3 — Dynamic Programming

```python
def longest_common_subsequence(s1: str, s2: str) -> int:
    """Classic DP — O(mn) time and space."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

# Space-optimized (only need previous row):
def lcs_optimized(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                curr[j] = prev[j-1] + 1
            else:
                curr[j] = max(prev[j], curr[j-1])
        prev = curr
    return prev[n]
```

---

## ✍️ 4. Derivations & Worked Examples

### Example 08.13.1 — Two Sum (Hash Map Pattern)

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```python
def two_sum(nums: list[int], target: int) -> tuple[int, int]:
    """Find indices of two numbers that sum to target. O(n) time, O(n) space."""
    seen: dict[int, int] = {}  # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    raise ValueError("No solution")

# Why O(n): Single pass, dict lookup is O(1)
# Why not sort+two-pointers: That's O(n log n) and loses original indices
```

</details>

### Example 08.13.2 — Binary Search (Divide & Conquer)

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```python
import bisect

def binary_search(arr: list[int], target: int) -> int:
    """Return index of target, or -1 if not found. O(log n)."""
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

# In production, use bisect module:
idx = bisect.bisect_left(arr, target)
found = idx < len(arr) and arr[idx] == target
```

</details>

### Example 08.13.3 — Sliding Window Maximum

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```python
from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """Maximum in each window of size k. O(n) using monotonic deque."""
    dq: deque[int] = deque()  # Stores indices, front = max
    result = []
    for i, num in enumerate(nums):
        # Remove elements outside window
        while dq and dq[0] <= i - k:
            dq.popleft()
        # Remove smaller elements (they'll never be the max)
        while dq and nums[dq[-1]] <= num:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

</details>

---

## 💻 5. Code Patterns & Idioms

### Pattern 1.13.1 — Memoization with `@cache`

```python
from functools import cache

@cache
def fib(n: int) -> int:
    if n < 2: return n
    return fib(n-1) + fib(n-2)

# Converts O(2^n) recursive to O(n) with memoization
```

### Pattern 1.13.2 — Topological Sort (DAG ordering)

```python
from collections import deque

def topological_sort(graph: dict[str, list[str]]) -> list[str]:
    """Kahn's algorithm — O(V+E). Used in: build systems, task scheduling, computation graphs."""
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] = in_degree.get(neighbor, 0) + 1

    queue = deque(node for node, deg in in_degree.items() if deg == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return order
```

---

## ⚠️ 6. Gotchas & Anti-Patterns

### Gotcha 1.13.1 — Python Recursion Limit

Python's default recursion limit is 1000. Deep recursion (e.g., DFS on large graphs) will hit `RecursionError`. Use iterative approaches with explicit stacks for production code.

```python
import sys
sys.setrecursionlimit(10000)  # Temporary fix, not a solution
# Better: convert to iterative with explicit stack
```

### Gotcha 1.13.2 — list.index() Is O(n)

```python
# BAD: O(n) lookup in a loop = O(n²) total
for item in items:
    idx = other_list.index(item)  # O(n) each time!

# GOOD: Build a dict first = O(n) total
index_map = {v: i for i, v in enumerate(other_list)}
for item in items:
    idx = index_map[item]  # O(1) each time
```

---

## 🧮 7. Hands-On Lab

```bash
python _practice/scripts/1.13_algorithms.py --count 20 --seed 42
```

Generates algorithm problems across all paradigms with SymPy-verified solutions. Mirrors the math drill format.

---

## 🔗 8. Cross-links & Further Reading

- Previous: [08.12 - Computer Architecture - Performance Intuition](08.12---Computer-Architecture---Performance-Intuition)
- Next: [08.14 - Concurrency Models & Patterns](08.14---Concurrency-Models-&-Patterns)
- Existing: [Common Algorithms for Coding Tests](Common-Algorithms-for-Coding-Tests)
- Math: [08.1 - Real Numbers, Sequences & Limits](08.1---Real-Numbers,-Sequences-&-Limits) (Big-O uses limits)
- ML connection: [23.5 - Transformer Architectures & LLMs](23.5---Transformer-Architectures-&-LLMs) (attention is O(n²))
- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/9780262046305/)
- [MIT 6.006 (Erik Demaine, free on OCW)](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/)



---

## 🧠 9. Extended Worked Examples & Deep Dives

### Example 9.1 — Heap-Based Dijkstra: Full Implementation with Priority Queue

**Problem:** Implement Dijkstra's shortest path algorithm using a min-heap priority queue. Handle edge cases (disconnected graphs, negative weights detection), and analyze the time complexity step by step.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: The Algorithm

Dijkstra's algorithm finds the shortest path from a source vertex to all other vertices in a weighted graph with non-negative edge weights.

**Invariant:** At each step, the vertex with the smallest tentative distance is finalized — its distance cannot be improved.

**Time Complexity:**

$$
O((V + E) \log V)
$$

where $V$ = vertices, $E$ = edges. The $\log V$ factor comes from heap operations (insert and extract-min).

#### Step 2: Implementation

```python
import heapq
from collections import defaultdict
from typing import Optional


def dijkstra(
    graph: dict[str, list[tuple[str, float]]],
    source: str,
) -> tuple[dict[str, float], dict[str, Optional[str]]]:
    """
    Dijkstra's shortest path algorithm using a min-heap.
    
    Args:
        graph: Adjacency list. graph[u] = [(v, weight), ...]
        source: Starting vertex.
    
    Returns:
        distances: Shortest distance from source to each vertex.
        predecessors: Previous vertex on shortest path (for path reconstruction).
    
    Time: O((V + E) log V)
    Space: O(V) for distances + O(V + E) for graph
    """
    # Initialize distances to infinity, source to 0
    distances: dict[str, float] = defaultdict(lambda: float("inf"))
    distances[source] = 0.0
    
    # Track predecessors for path reconstruction
    predecessors: dict[str, Optional[str]] = {source: None}
    
    # Min-heap: (distance, vertex)
    # Python's heapq is a min-heap — smallest element popped first
    heap: list[tuple[float, str]] = [(0.0, source)]
    
    # Set of finalized vertices (their shortest distance is confirmed)
    finalized: set[str] = set()
    
    while heap:
        # Extract vertex with smallest tentative distance
        current_dist, u = heapq.heappop(heap)
        
        # Skip if already finalized (we may have duplicate entries in heap)
        if u in finalized:
            continue
        
        # Finalize this vertex
        finalized.add(u)
        
        # Relax all edges from u
        for v, weight in graph.get(u, []):
            if v in finalized:
                continue  # Already found shortest path to v
            
            # Check for negative weights (Dijkstra doesn't handle them)
            if weight < 0:
                raise ValueError(
                    f"Negative edge weight ({u} → {v}, weight={weight}). "
                    "Use Bellman-Ford instead."
                )
            
            new_dist = current_dist + weight
            
            if new_dist < distances[v]:
                # Found a shorter path to v
                distances[v] = new_dist
                predecessors[v] = u
                heapq.heappush(heap, (new_dist, v))
                # Note: we don't remove the old entry — we just skip it
                # when popped (the "lazy deletion" pattern)
    
    return dict(distances), predecessors


def reconstruct_path(
    predecessors: dict[str, Optional[str]],
    source: str,
    target: str,
) -> Optional[list[str]]:
    """Reconstruct shortest path from source to target."""
    if target not in predecessors:
        return None  # Target unreachable
    
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = predecessors[current]
    
    path.reverse()
    
    # Verify path starts at source
    if path[0] != source:
        return None
    
    return path
```

#### Step 3: Testing

```python
def test_dijkstra():
    # Example graph:
    #     A --1-- B --2-- C
    #     |       |       |
    #     4       1       3
    #     |       |       |
    #     D --5-- E --1-- F
    
    graph = {
        "A": [("B", 1), ("D", 4)],
        "B": [("A", 1), ("C", 2), ("E", 1)],
        "C": [("B", 2), ("F", 3)],
        "D": [("A", 4), ("E", 5)],
        "E": [("B", 1), ("D", 5), ("F", 1)],
        "F": [("C", 3), ("E", 1)],
    }
    
    distances, predecessors = dijkstra(graph, "A")
    
    assert distances["A"] == 0
    assert distances["B"] == 1   # A → B
    assert distances["C"] == 3   # A → B → C
    assert distances["D"] == 4   # A → D
    assert distances["E"] == 2   # A → B → E
    assert distances["F"] == 3   # A → B → E → F
    
    path = reconstruct_path(predecessors, "A", "F")
    assert path == ["A", "B", "E", "F"]
    
    # Disconnected vertex
    graph["Z"] = []  # Isolated vertex
    distances, _ = dijkstra(graph, "A")
    assert distances.get("Z", float("inf")) == float("inf")
    
    print("✅ All Dijkstra tests passed")

test_dijkstra()
```

#### Step 4: Why the Heap Matters

```python
# Without heap (naive implementation): O(V²)
#   - Each iteration scans ALL vertices to find minimum → O(V) per iteration
#   - V iterations → O(V²) total
#   - Better for dense graphs (E ≈ V²)

# With binary heap: O((V + E) log V)
#   - Extract-min: O(log V)
#   - Decrease-key (via lazy deletion): O(log V) per edge relaxation
#   - Total: O(V log V + E log V) = O((V + E) log V)
#   - Better for sparse graphs (E ≈ V)

# With Fibonacci heap: O(V log V + E)  [theoretical, rarely used in practice]
#   - Decrease-key: O(1) amortized
#   - But constant factors are large; binary heap wins for practical sizes
```

**Final Answer:**

```python
# Dijkstra's algorithm key points:
# 1. Only works with non-negative edge weights
# 2. Greedy: finalizes closest unvisited vertex each step
# 3. Use heapq with lazy deletion (skip already-finalized vertices)
# 4. Time: O((V+E) log V) with binary heap
# 5. For negative weights: use Bellman-Ford O(VE) or SPFA
# 6. For unweighted graphs: use BFS O(V+E) — simpler and faster
```

</details>

### Example 9.2 — LRU Cache: The Classic Interview Problem (O(1) Everything)

**Problem:** Implement an LRU (Least Recently Used) cache with O(1) `get` and O(1) `put` operations. This is LeetCode #146 and one of the most common system design interview questions.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Data Structure Choice

```python
# Requirements:
# - get(key): O(1) lookup + mark as recently used
# - put(key, value): O(1) insert + evict LRU if at capacity
#
# We need TWO data structures working together:
# 1. Hash map (dict): O(1) lookup by key
# 2. Doubly-linked list: O(1) insertion/deletion at both ends
#
# The dict maps key → node in the linked list
# The linked list maintains access order (head = LRU, tail = MRU)
```

#### Step 2: Implementation from Scratch

```python
class DLLNode:
    """Doubly-linked list node."""
    __slots__ = ("key", "value", "prev", "next")
    
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev: "DLLNode | None" = None
        self.next: "DLLNode | None" = None


class LRUCache:
    """
    LRU Cache with O(1) get and put.
    
    Internal structure:
    head ←→ node1 ←→ node2 ←→ ... ←→ nodeN ←→ tail
    (LRU)                                      (MRU)
    
    head and tail are sentinel nodes (simplify edge cases).
    """
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: dict[int, DLLNode] = {}
        
        # Sentinel nodes (avoid null checks)
        self.head = DLLNode()  # Dummy head (LRU side)
        self.tail = DLLNode()  # Dummy tail (MRU side)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def get(self, key: int) -> int:
        """
        Get value by key. Returns -1 if not found.
        Moves accessed node to tail (most recently used).
        Time: O(1)
        """
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        # Move to tail (mark as most recently used)
        self._remove(node)
        self._add_to_tail(node)
        return node.value
    
    def put(self, key: int, value: int) -> None:
        """
        Insert or update key-value pair.
        If at capacity, evict LRU (node after head sentinel).
        Time: O(1)
        """
        if key in self.cache:
            # Update existing: remove old position, will re-add at tail
            node = self.cache[key]
            self._remove(node)
            node.value = value
            self._add_to_tail(node)
        else:
            # New entry
            if len(self.cache) >= self.capacity:
                # Evict LRU (node right after head sentinel)
                lru_node = self.head.next
                self._remove(lru_node)
                del self.cache[lru_node.key]
            
            # Insert new node at tail (most recently used)
            new_node = DLLNode(key, value)
            self._add_to_tail(new_node)
            self.cache[key] = new_node
    
    def _remove(self, node: DLLNode) -> None:
        """Remove node from its current position. O(1)."""
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add_to_tail(self, node: DLLNode) -> None:
        """Add node just before tail sentinel (MRU position). O(1)."""
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node


# Test:
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
assert cache.get(1) == 1       # Returns 1, marks key 1 as MRU
cache.put(3, 3)                # Evicts key 2 (LRU)
assert cache.get(2) == -1      # Key 2 was evicted
cache.put(4, 4)                # Evicts key 1 (now LRU since 3 was just added)
assert cache.get(1) == -1      # Key 1 was evicted
assert cache.get(3) == 3       # Key 3 still present
assert cache.get(4) == 4       # Key 4 still present
print("✅ LRU Cache tests passed")
```

#### Step 3: Python Shortcut with OrderedDict

```python
from collections import OrderedDict

class LRUCacheSimple(OrderedDict):
    """
    LRU Cache using OrderedDict (Python 3.7+).
    OrderedDict maintains insertion order AND supports move_to_end().
    """
    
    def __init__(self, capacity: int):
        super().__init__()
        self.capacity = capacity
    
    def get(self, key: int) -> int:
        if key not in self:
            return -1
        self.move_to_end(key)  # Mark as MRU
        return self[key]
    
    def put(self, key: int, value: int) -> None:
        if key in self:
            self.move_to_end(key)
        self[key] = value
        if len(self) > self.capacity:
            self.popitem(last=False)  # Remove first item (LRU)
```

**Final Answer:**

```python
# LRU Cache implementation notes:
# - Interview: implement with dict + doubly-linked list (shows understanding)
# - Production: use collections.OrderedDict or functools.lru_cache
# - Key insight: dict gives O(1) lookup, DLL gives O(1) reordering
# - Sentinel nodes eliminate edge cases (empty list, single element)
# - Thread-safe version: add a threading.Lock around get/put
```

</details>

### Example 9.3 — Top-K Elements: Heap vs QuickSelect vs Counting

**Problem:** Find the K largest elements from an unsorted array of N elements. Implement three approaches and analyze when each is optimal.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Approach 1 — Min-Heap of Size K

```python
import heapq
from typing import List

def top_k_heap(nums: List[int], k: int) -> List[int]:
    """
    Maintain a min-heap of size K.
    The heap always contains the K largest elements seen so far.
    The root (minimum of the heap) is the K-th largest overall.
    
    Time: O(N log K)
    Space: O(K)
    """
    if k >= len(nums):
        return sorted(nums, reverse=True)
    
    # Build initial heap with first K elements
    heap = nums[:k]
    heapq.heapify(heap)  # O(K)
    
    # Process remaining elements
    for num in nums[k:]:
        if num > heap[0]:  # Larger than current K-th largest
            heapq.heapreplace(heap, num)  # Pop min, push new — O(log K)
    
    # Heap contains K largest elements (unordered)
    return sorted(heap, reverse=True)  # O(K log K) to sort final result


# Python shortcut:
def top_k_nlargest(nums: List[int], k: int) -> List[int]:
    """heapq.nlargest uses the same algorithm internally."""
    return heapq.nlargest(k, nums)
```

#### Step 2: Approach 2 — QuickSelect (Average O(N))

```python
import random

def top_k_quickselect(nums: List[int], k: int) -> List[int]:
    """
    Partition-based selection (Hoare's QuickSelect).
    Find the K-th largest element, then collect all elements >= it.
    
    Time: O(N) average, O(N²) worst case
    Space: O(1) (in-place partitioning)
    """
    if k >= len(nums):
        return sorted(nums, reverse=True)
    
    # Find the K-th largest element
    target_idx = k - 1  # 0-indexed position in sorted-descending order
    
    def partition(left: int, right: int, pivot_idx: int) -> int:
        """Lomuto partition scheme. Returns final position of pivot."""
        pivot_val = nums[pivot_idx]
        # Move pivot to end
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
        store_idx = left
        
        for i in range(left, right):
            if nums[i] > pivot_val:  # Descending order
                nums[store_idx], nums[i] = nums[i], nums[store_idx]
                store_idx += 1
        
        nums[store_idx], nums[right] = nums[right], nums[store_idx]
        return store_idx
    
    def quickselect(left: int, right: int) -> None:
        """Recursively partition until target_idx is in correct position."""
        if left >= right:
            return
        
        # Random pivot (avoids O(N²) on sorted input)
        pivot_idx = random.randint(left, right)
        final_pos = partition(left, right, pivot_idx)
        
        if final_pos == target_idx:
            return
        elif final_pos < target_idx:
            quickselect(final_pos + 1, right)
        else:
            quickselect(left, final_pos - 1)
    
    nums_copy = nums.copy()  # Don't modify original
    quickselect(0, len(nums_copy) - 1)
    
    # After quickselect, elements at indices 0..k-1 are the K largest (unordered)
    return sorted(nums_copy[:k], reverse=True)
```

#### Step 3: Approach 3 — Counting Sort (O(N) for bounded integers)

```python
def top_k_counting(nums: List[int], k: int, max_val: int = 10**6) -> List[int]:
    """
    Counting sort approach for bounded integer values.
    
    Time: O(N + max_val)
    Space: O(max_val)
    Best when: values are bounded and K is large relative to N.
    """
    # Count occurrences
    counts = [0] * (max_val + 1)
    for num in nums:
        counts[num] += 1
    
    # Collect top K by scanning from largest to smallest
    result = []
    remaining = k
    for val in range(max_val, -1, -1):
        if counts[val] > 0:
            take = min(counts[val], remaining)
            result.extend([val] * take)
            remaining -= take
            if remaining == 0:
                break
    
    return result
```

#### Step 4: Comparison

```python
# | Approach      | Time (avg)  | Time (worst) | Space  | Best when           |
# |---------------|-------------|--------------|--------|---------------------|
# | Min-heap      | O(N log K)  | O(N log K)   | O(K)   | K << N, streaming   |
# | QuickSelect   | O(N)        | O(N²)        | O(N)   | K ≈ N/2, in-memory  |
# | Counting sort | O(N + M)    | O(N + M)     | O(M)   | Bounded integers    |
# | Full sort     | O(N log N)  | O(N log N)   | O(N)   | Need sorted output  |
#
# M = range of values (max_val)
# 
# Practical choice:
# - K < 100 and N > 10000: heap (heapq.nlargest)
# - K ≈ N/2: quickselect
# - Bounded small integers: counting sort
# - Need exact sorted top-K: heap then sort result
```

**Final Answer:**

```python
# In Python, just use:
import heapq
result = heapq.nlargest(k, nums)  # O(N log K), handles all cases well

# For interviews, know all three approaches and their tradeoffs.
# The heap approach is almost always the best practical choice because:
# 1. O(K) space (works for streaming data)
# 2. Guaranteed O(N log K) (no worst case)
# 3. One line in Python (heapq.nlargest)
```

</details>

---

## 📘 10. Appendix: Extended Derivations & Special Cases

### 10.1 Amortized Analysis — Why append() Is O(1) Despite Occasional O(N) Resizing

Python's `list.append()` is advertised as O(1), but occasionally it triggers a reallocation that copies the entire array. Amortized analysis proves the average cost is still O(1).

**The Resizing Strategy:**

CPython's list uses a growth factor of approximately 08.125 (it over-allocates by ~12.5%):

```python
# From CPython source (Objects/listobject.c):
# new_allocated = (size_t)newsize + (newsize >> 3) + (newsize < 9 ? 3 : 6)
# 
# This means: when the list needs to grow, it allocates ~12.5% extra space.
# Growth sequence: 0, 4, 8, 16, 24, 32, 40, 52, 64, 76, ...
```

**Amortized Analysis (Aggregate Method):**

Consider N append operations starting from an empty list. Let's count the total number of element copies:

- Append 1-4: no resize (initial allocation = 4)
- Append 5: resize to 8, copy 4 elements
- Append 9: resize to 16, copy 8 elements
- Append 17: resize to 24, copy 16 elements
- ...

Total copies after N appends (with growth factor $\alpha$):

$$
\text{Total copies} = \sum_{i=0}^{\log_\alpha N} \alpha^i = \frac{\alpha^{\log_\alpha N + 1} - 1}{\alpha - 1} = \frac{\alpha \cdot N - 1}{\alpha - 1} = O(N)
$$

Since N appends cause O(N) total copies, the **amortized cost per append is O(1)**.

**The Banker's Method (Intuitive Explanation):**

Think of each append as "paying" 3 coins:
- 1 coin for the actual insertion
- 2 coins saved for future copying (one for itself, one for an older element)

When a resize happens, the saved coins pay for all the copies. The account never goes negative, proving O(1) amortized cost.

**Practical Implication:**

```python
# This is O(N) total, not O(N²):
result = []
for i in range(1_000_000):
    result.append(i)  # Each append is O(1) amortized

# This is O(N²) — DON'T do this:
result = []
for i in range(1_000_000):
    result = result + [i]  # Creates new list each time! O(N) per iteration
```

### 10.2 Competitive Programming Python Idioms

Python is slower than C++ for competitive programming, but its expressiveness compensates. These idioms maximize speed within Python's constraints.

**Fast I/O:**

```python
import sys
input = sys.stdin.readline  # 3-5x faster than builtin input()

# For bulk reading:
data = sys.stdin.read().split()
idx = 0
def next_int():
    global idx
    idx += 1
    return int(data[idx - 1])

# Fast output:
output = []
output.append(str(result))
sys.stdout.write("\n".join(output))
```

**Common Patterns:**

```python
from collections import defaultdict, deque, Counter
from heapq import heappush, heappop, heapify
from itertools import accumulate, combinations, permutations
from functools import lru_cache
from bisect import bisect_left, bisect_right, insort
import math

# Prefix sums (O(1) range queries after O(N) preprocessing)
arr = [3, 1, 4, 1, 5, 9]
prefix = list(accumulate(arr, initial=0))
# Sum of arr[i:j] = prefix[j] - prefix[i]

# Binary search on answer (monotonic predicate)
def binary_search_answer(lo: int, hi: int, predicate) -> int:
    """Find smallest x in [lo, hi] where predicate(x) is True."""
    while lo < hi:
        mid = (lo + hi) // 2
        if predicate(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

# BFS template
def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    dist = {start: 0}
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)
    return dist

# DFS with recursion limit increase
sys.setrecursionlimit(300_000)

# Memoized recursion (top-down DP)
@lru_cache(maxsize=None)
def dp(state):
    # base cases
    # recursive cases
    pass

# Bit manipulation
# Count set bits: bin(x).count('1') or x.bit_count() (Python 3.10+)
# Lowest set bit: x & (-x)
# Clear lowest set bit: x & (x - 1)
# All subsets of a bitmask:
def subsets(mask):
    sub = mask
    while sub:
        yield sub
        sub = (sub - 1) & mask
    yield 0
```

**Python-Specific Speed Tips:**

```python
# 1. Use local variables (LOAD_FAST vs LOAD_GLOBAL)
def solve():
    # Move everything inside a function — local lookups are faster
    n = int(input())
    ...

# 2. Avoid attribute lookups in loops
append = result.append  # Cache the method reference
for x in data:
    append(x)  # Faster than result.append(x)

# 3. Use array module for typed arrays (less overhead than list)
from array import array
arr = array('i', [0] * n)  # int32 array, no Python object overhead

# 4. PyPy compatibility: avoid numpy (not available), use plain Python
# PyPy is 5-50x faster than CPython for loop-heavy code
```

---
