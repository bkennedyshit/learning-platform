---
title: "08.5 — Testing, Debugging & Logging"
subject: "Python"
catalog: advanced
audience_tier: higher-education
chapter: "8.5"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 08.5 — Testing, Debugging & Logging

> *"Beware of bugs in the above code; I have only proved it correct, not tested it."* — Donald Knuth

Testing is not a chore bolted onto development — it's the primary mechanism by which you gain confidence that your code does what you think it does. This chapter covers the full professional testing stack: unit tests, property-based testing, mocking, coverage, structured logging, and systematic debugging.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Write pytest tests with fixtures, parametrize, and markers.
2. Use `hypothesis` for property-based testing that finds edge cases you'd never think of.
3. Mock external dependencies cleanly without over-mocking.
4. Configure structured logging with `structlog` for production observability.
5. Debug systematically using `pdb`, `debugpy`, and post-mortem analysis.
6. Achieve meaningful coverage without chasing 100% as a vanity metric.

---

## 🖼️ Visual Anchor — Testing Pyramid & Feedback Loop

![python__1.5-fig1](python__1.5-fig1.svg)

---

## 📚 1. Definitions / Concepts

### Definition 08.5.1 — Test Fixture

A **fixture** is a function that provides test data or sets up/tears down test state. In pytest, fixtures are declared with `@pytest.fixture` and injected by name:

```python
import pytest
from pathlib import Path

@pytest.fixture
def config_file(tmp_path: Path) -> Path:
    """Create a temporary config file."""
    cfg = tmp_path / "config.toml"
    cfg.write_text('[database]\nurl = "sqlite:///test.db"\n')
    return cfg

def test_load_config(config_file: Path):
    config = load_config(config_file)
    assert config["database"]["url"] == "sqlite:///test.db"
```

### Definition 08.5.2 — Property-Based Testing

Instead of writing specific input/output pairs, you describe **properties** that must hold for all valid inputs. The testing framework generates hundreds of random inputs:

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_is_idempotent(xs: list[int]):
    """Sorting twice gives the same result as sorting once."""
    assert sorted(sorted(xs)) == sorted(xs)

@given(st.lists(st.integers(), min_size=1))
def test_max_in_sorted(xs: list[int]):
    """Max element is last in sorted list."""
    assert sorted(xs)[-1] == max(xs)
```

### Definition 08.5.3 — Structured Logging

**Structured logging** emits log events as key-value pairs (typically JSON) rather than free-form strings. This makes logs machine-parseable for aggregation and alerting:

```python
import structlog

log = structlog.get_logger()
log.info("request_processed", method="GET", path="/api/users", duration_ms=42, status=200)
# Output: {"event": "request_processed", "method": "GET", "path": "/api/users", ...}
```

---

## 📐 2. Mental Models / Principles

### Principle 1.5.1 — The Testing Pyramid

- **Unit tests** (70%): Fast, isolated, test one function/class. Run in milliseconds.
- **Integration tests** (20%): Test component interactions (DB, API, filesystem).
- **End-to-end tests** (10%): Test the full system. Slow, brittle, but catch integration gaps.

### Principle 1.5.2 — Test Behavior, Not Implementation

```python
# BAD: Tests implementation details (fragile)
def test_cache_uses_dict():
    cache = Cache()
    assert isinstance(cache._store, dict)  # Breaks if you change internal structure

# GOOD: Tests behavior (stable)
def test_cache_returns_stored_value():
    cache = Cache()
    cache.set("key", "value")
    assert cache.get("key") == "value"
```

### Principle 1.5.3 — Logging Levels as Contracts

| Level | Meaning | Who reads it |
|-------|---------|-------------|
| `DEBUG` | Detailed diagnostic info | Developer during debugging |
| `INFO` | Normal operation milestones | Ops team monitoring |
| `WARNING` | Unexpected but handled | Ops team (potential issue) |
| `ERROR` | Operation failed | On-call engineer (needs attention) |
| `CRITICAL` | System is broken | Everyone (wake people up) |

---

## 🔑 3. Mechanics

### 3.1 — pytest Power Features

```python
import pytest

# Parametrize: run same test with multiple inputs
@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("", 0),
    ("a" * 1000, 1000),
])
def test_string_length(input: str, expected: int):
    assert len(input) == expected

# Fixtures with scope
@pytest.fixture(scope="session")
def db_connection():
    """One connection for entire test session."""
    conn = create_connection()
    yield conn
    conn.close()

# Expecting exceptions
def test_division_by_zero():
    with pytest.raises(ZeroDivisionError, match="division by zero"):
        1 / 0

# Markers for conditional skipping
@pytest.mark.skipif(sys.platform == "win32", reason="Unix-only test")
def test_unix_permissions():
    ...
```

### 3.2 — Mocking (unittest.mock)

```python
from unittest.mock import patch, MagicMock, AsyncMock

# Patch an external dependency
@patch("my_module.httpx.get")
def test_fetch_data(mock_get: MagicMock):
    mock_get.return_value.json.return_value = {"status": "ok"}
    result = fetch_data("https://api.example.com")
    assert result == {"status": "ok"}
    mock_get.assert_called_once_with("https://api.example.com")

# Async mock
@patch("my_module.client.get", new_callable=AsyncMock)
async def test_async_fetch(mock_get: AsyncMock):
    mock_get.return_value.text = "response"
    result = await async_fetch("/path")
    assert result == "response"
```

### 3.3 — Debugging Toolkit

```python
# --- pdb (built-in debugger) ---
# Insert breakpoint anywhere:
breakpoint()  # Drops into pdb at this line (Python 3.7+)

# pdb commands:
# n (next), s (step into), c (continue), p expr (print), l (list code)
# pp vars() (pretty-print locals), w (where/stack trace)

# --- Post-mortem debugging ---
# Run with: python -m pdb script.py
# Or in code:
import pdb
try:
    buggy_function()
except Exception:
    pdb.post_mortem()  # Inspect state at crash point

# --- debugpy (VS Code remote debugging) ---
import debugpy
debugpy.listen(5678)
debugpy.wait_for_client()  # Pause until VS Code attaches
breakpoint()
```

### 3.4 — Structured Logging Setup

```python
import structlog
import logging

# Configure structlog for development (pretty) and production (JSON)
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer()  # Switch to JSONRenderer() in prod
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)

log = structlog.get_logger()

# Bind context that persists across calls
log = log.bind(user_id="bill", session="abc123")
log.info("page_viewed", path="/dashboard")
log.warning("rate_limit_approaching", current=95, max=100)
```

---

## ✍️ 4. Derivations & Worked Examples

### Example 08.5.1 — Testing an Async API Client

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```python
import pytest
import httpx
from unittest.mock import AsyncMock, patch

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)

    async def get_user(self, user_id: int) -> dict:
        resp = await self.client.get(f"/users/{user_id}")
        resp.raise_for_status()
        return resp.json()

@pytest.fixture
def api_client():
    return APIClient("https://api.example.com")

@pytest.mark.asyncio
async def test_get_user_success(api_client):
    mock_response = AsyncMock()
    mock_response.json.return_value = {"id": 1, "name": "Bill"}
    mock_response.raise_for_status = lambda: None

    with patch.object(api_client.client, "get", return_value=mock_response) as mock_get:
        user = await api_client.get_user(1)
        assert user == {"id": 1, "name": "Bill"}
        mock_get.assert_called_once_with("/users/1")

@pytest.mark.asyncio
async def test_get_user_not_found(api_client):
    with patch.object(api_client.client, "get") as mock_get:
        mock_get.return_value.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found", request=None, response=None
        )
        with pytest.raises(httpx.HTTPStatusError):
            await api_client.get_user(999)
```

</details>

---

## 💻 5. Code Patterns & Idioms

### Pattern 1.5.1 — conftest.py Fixture Hierarchy

```python
# tests/conftest.py — shared across all tests
@pytest.fixture(scope="session")
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

# tests/api/conftest.py — shared within api/ tests only
@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    return TestClient(app)
```

### Pattern 1.5.2 — Hypothesis Strategies for Domain Objects

```python
from hypothesis import given, strategies as st

# Custom strategy for your domain
vectors = st.tuples(st.floats(min_value=-1e6, max_value=1e6, allow_nan=False), 
                    st.floats(min_value=-1e6, max_value=1e6, allow_nan=False))

@given(vectors, vectors)
def test_dot_product_commutative(v1, v2):
    assert abs(dot(v1, v2) - dot(v2, v1)) < 1e-10
```

---

## ⚠️ 6. Gotchas & Anti-Patterns

### Gotcha 1.5.1 — Over-Mocking

If you mock everything, you're testing that your mocks work, not your code. Mock at boundaries (network, DB, filesystem), not internal functions.

### Gotcha 1.5.2 — Tests That Pass But Don't Test Anything

```python
# BAD: Always passes regardless of implementation
def test_process():
    result = process(data)
    assert result is not None  # Meaningless assertion
```

---

## 🧮 7. Hands-On Lab

```bash
python _practice/scripts/1.5_testing.py --demo
```

The script creates a sample project, writes tests with intentional bugs, and guides you through the red-green-refactor cycle.

---

## 🔗 8. Cross-links & Further Reading

- Previous: [08.4 - Concurrency - asyncio, threading, multiprocessing & the GIL](08.4---Concurrency---asyncio,-threading,-multiprocessing-&-the-GIL)
- Next: [08.6 - The Standard Library & Ecosystem Tour](08.6---The-Standard-Library-&-Ecosystem-Tour)
- Existing reference: [Python Error Handling](Python-Error-Handling), [Debugging Strategies for Coding Tests](Debugging-Strategies-for-Coding-Tests)
- [pytest documentation](https://docs.pytest.org/)
- [Hypothesis documentation](https://hypothesis.readthedocs.io/)
- [structlog documentation](https://www.structlog.org/)



---

## 🧠 9. Extended Worked Examples & Deep Dives

### Example 9.1 — Hypothesis Stateful Testing: Finding Bugs in a Stateful Cache

**Problem:** You've built an LRU cache with `get`, `put`, and `delete` operations. Unit tests pass, but you suspect edge cases around eviction ordering and concurrent-like interleaving. Use Hypothesis stateful testing to automatically generate sequences of operations that expose bugs.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: The Implementation Under Test

```python
from collections import OrderedDict
from typing import Optional, Any


class LRUCache:
    """Least Recently Used cache with fixed capacity."""

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._store: OrderedDict[str, Any] = OrderedDict()

    def get(self, key: str) -> Optional[Any]:
        """Get value and mark as recently used."""
        if key not in self._store:
            return None
        self._store.move_to_end(key)  # Mark as recently used
        return self._store[key]

    def put(self, key: str, value: Any) -> None:
        """Insert or update. Evicts LRU item if at capacity."""
        if key in self._store:
            self._store.move_to_end(key)
            self._store[key] = value
        else:
            if len(self._store) >= self.capacity:
                self._store.popitem(last=False)  # Evict LRU (first item)
            self._store[key] = value

    def delete(self, key: str) -> bool:
        """Remove key. Returns True if key existed."""
        if key in self._store:
            del self._store[key]
            return True
        return False

    def __len__(self) -> int:
        return len(self._store)
```

#### Step 2: The Stateful Test (Hypothesis RuleBasedStateMachine)

```python
from hypothesis import settings, given, note
from hypothesis.stateful import (
    RuleBasedStateMachine,
    rule,
    invariant,
    initialize,
    precondition,
    Bundle,
)
from hypothesis import strategies as st


class LRUCacheStateMachine(RuleBasedStateMachine):
    """
    Hypothesis generates random sequences of operations and checks
    invariants after each step. It shrinks failing sequences to minimal
    reproducing examples.
    """

    def __init__(self):
        super().__init__()
        self.capacity = 0
        self.cache: Optional[LRUCache] = None
        # Model: a simple dict that tracks what SHOULD be in the cache
        self.model: dict[str, Any] = {}
        self.access_order: list[str] = []  # Track LRU ordering

    @initialize(capacity=st.integers(min_value=1, max_value=5))
    def create_cache(self, capacity: int):
        """Initialize with random capacity (small for faster exploration)."""
        self.capacity = capacity
        self.cache = LRUCache(capacity)
        self.model = {}
        self.access_order = []

    def _touch(self, key: str):
        """Update our model's access order."""
        if key in self.access_order:
            self.access_order.remove(key)
        self.access_order.append(key)

    def _evict_lru(self):
        """Evict least recently used from model."""
        if len(self.model) >= self.capacity:
            lru_key = self.access_order[0]
            del self.model[lru_key]
            self.access_order.pop(0)

    @rule(key=st.text(min_size=1, max_size=3), value=st.integers())
    def put(self, key: str, value: int):
        """Put a key-value pair."""
        if key in self.model:
            # Update existing — no eviction needed
            self.model[key] = value
            self._touch(key)
        else:
            # New key — may need eviction
            self._evict_lru()
            self.model[key] = value
            self._touch(key)

        self.cache.put(key, value)

    @rule(key=st.text(min_size=1, max_size=3))
    def get(self, key: str):
        """Get a key and verify against model."""
        result = self.cache.get(key)
        expected = self.model.get(key)
        assert result == expected, (
            f"get({key!r}): got {result}, expected {expected}"
        )
        if key in self.model:
            self._touch(key)

    @rule(key=st.text(min_size=1, max_size=3))
    def delete(self, key: str):
        """Delete a key."""
        result = self.cache.delete(key)
        expected = key in self.model
        assert result == expected
        if key in self.model:
            del self.model[key]
            self.access_order.remove(key)

    @invariant()
    def size_invariant(self):
        """Cache size must never exceed capacity."""
        assert len(self.cache) <= self.capacity

    @invariant()
    def model_agreement(self):
        """Cache contents must match our model."""
        assert len(self.cache) == len(self.model)


# Run the stateful test:
# Hypothesis will generate hundreds of random operation sequences
TestLRUCache = LRUCacheStateMachine.TestCase
TestLRUCache.settings = settings(max_examples=500, stateful_step_count=50)
```

#### Step 3: Running and Interpreting Results

```bash
# Run with pytest:
pytest test_lru_stateful.py -v

# If a bug is found, Hypothesis prints the MINIMAL failing sequence:
# Falsifying example:
#   state = LRUCacheStateMachine()
#   state.create_cache(capacity=2)
#   state.put(key='a', value=1)
#   state.put(key='b', value=2)
#   state.put(key='a', value=3)  # Update existing
#   state.put(key='c', value=4)  # Should evict 'b' (LRU), not 'a'
#   state.get(key='a')           # Should return 3
#   state.teardown()
```

#### Step 4: Why This Catches Bugs Unit Tests Miss

Stateful testing explores the **state space** — combinations of operations that a human wouldn't think to test:
- Put same key multiple times, then evict
- Delete a key, re-insert it, check eviction order
- Fill cache, get all items (refreshing LRU), then insert new item
- Sequences of 30+ operations with interleaved gets/puts/deletes

**Final Answer:**

```python
# Hypothesis stateful testing workflow:
# 1. Define a RuleBasedStateMachine with @rule methods for each operation
# 2. Maintain a "model" (simple reference implementation) alongside the SUT
# 3. Define @invariant methods that must hold after every step
# 4. Hypothesis generates random sequences, checks invariants, shrinks failures
# 5. Result: minimal reproducing sequence for any bug found
#
# Best for: caches, queues, state machines, databases, protocol implementations
```

</details>

### Example 9.2 — pytest Fixtures with Scope Hierarchy and Dependency Injection

**Problem:** Design a test suite for a web application that needs: a database (session-scoped, expensive to create), a clean schema per test module, and fresh test data per test function. Show the full fixture hierarchy with proper scoping, teardown, and parametrization.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: The Fixture Scope Hierarchy

```python
# conftest.py — shared fixtures for the entire test suite
import pytest
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

# Scope hierarchy (from broadest to narrowest):
# session > package > module > class > function (default)
#
# A fixture is created ONCE per scope unit and shared by all tests in that scope.
# Teardown happens when the scope exits.
```

#### Step 2: Session-Scoped Database Engine

```python
@pytest.fixture(scope="session")
def db_engine():
    """
    Create database engine ONCE for the entire test session.
    Scope=session means this fixture is created once and reused
    across ALL test files.
    
    Cost: ~2s to create (connection pool, schema validation)
    """
    engine = create_engine(
        "postgresql://test:test@localhost:5432/test_db",
        pool_size=5,
        echo=False,
    )
    
    # Setup: create all tables
    from app.models import Base
    Base.metadata.create_all(engine)
    
    yield engine
    
    # Teardown: drop all tables (runs once at end of entire test session)
    Base.metadata.drop_all(engine)
    engine.dispose()
```

#### Step 3: Module-Scoped Schema Reset

```python
@pytest.fixture(scope="module")
def clean_schema(db_engine):
    """
    Truncate all tables at the start of each test MODULE.
    Scope=module means this runs once per test file.
    
    This depends on db_engine (session-scoped) — pytest handles
    the scope hierarchy automatically.
    """
    with db_engine.connect() as conn:
        # Truncate all tables (faster than drop/recreate)
        conn.execute(text("""
            DO $$ 
            DECLARE t text;
            BEGIN
                FOR t IN SELECT tablename FROM pg_tables 
                         WHERE schemaname = 'public'
                LOOP
                    EXECUTE 'TRUNCATE TABLE ' || t || ' CASCADE';
                END LOOP;
            END $$;
        """))
        conn.commit()
    
    yield  # Tests in this module run here
    
    # No teardown needed — next module will truncate again
```

#### Step 4: Function-Scoped Transaction Rollback

```python
@pytest.fixture()
def db_session(db_engine, clean_schema) -> Generator[Session, None, None]:
    """
    Provide a database session that ROLLS BACK after each test.
    Scope=function (default) means each test gets a fresh session.
    
    Pattern: wrap each test in a transaction, rollback at end.
    This is MUCH faster than truncating tables per test.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    
    yield session
    
    # Teardown: rollback everything this test did
    session.close()
    transaction.rollback()
    connection.close()
```

#### Step 5: Fixture Factories and Parametrization

```python
@pytest.fixture
def user_factory(db_session):
    """
    Factory fixture — returns a callable that creates users.
    Avoids creating users that aren't needed by a specific test.
    """
    from app.models import User
    
    created_users = []
    
    def _create_user(name: str = "test_user", email: str = None, role: str = "user"):
        email = email or f"{name}@test.com"
        user = User(name=name, email=email, role=role)
        db_session.add(user)
        db_session.flush()  # Assign ID without committing
        created_users.append(user)
        return user
    
    yield _create_user
    
    # No cleanup needed — transaction rollback handles it


@pytest.fixture(params=["admin", "user", "guest"])
def user_with_role(request, user_factory):
    """
    Parametrized fixture — test runs 3 times, once per role.
    `request.param` contains the current parameter value.
    """
    return user_factory(name=f"test_{request.param}", role=request.param)
```

#### Step 6: Using the Fixtures in Tests

```python
# tests/test_permissions.py

def test_admin_can_delete_users(db_session, user_factory):
    """Each fixture parameter is injected by name."""
    admin = user_factory("admin", role="admin")
    target = user_factory("victim", role="user")
    
    from app.services import delete_user
    result = delete_user(db_session, admin, target.id)
    
    assert result.success is True
    assert db_session.query(User).get(target.id) is None


def test_role_permissions(user_with_role, db_session):
    """Runs 3 times (admin, user, guest) due to parametrized fixture."""
    from app.services import get_permissions
    
    perms = get_permissions(user_with_role)
    
    if user_with_role.role == "admin":
        assert "delete_users" in perms
    elif user_with_role.role == "user":
        assert "delete_users" not in perms
        assert "read_own_data" in perms
    else:
        assert perms == {"read_public"}


class TestUserAPI:
    """Class-scoped fixtures shared across methods."""
    
    @pytest.fixture(autouse=True)
    def setup_api_client(self, db_session, user_factory):
        """autouse=True means this runs for every test in the class."""
        self.admin = user_factory("admin", role="admin")
        self.client = TestClient(app)
        self.client.headers["Authorization"] = f"Bearer {self.admin.token}"
    
    def test_list_users(self):
        response = self.client.get("/api/users")
        assert response.status_code == 200
    
    def test_create_user(self):
        response = self.client.post("/api/users", json={"name": "new"})
        assert response.status_code == 201
```

**Final Answer:**

```python
# Fixture scope hierarchy best practices:
# 
# session:  Database engine, Docker containers, expensive shared resources
# module:   Schema resets, test data seeding for a group of related tests
# class:    Shared setup for a test class (use sparingly)
# function: Transaction rollback, fresh state per test (DEFAULT — prefer this)
#
# Key patterns:
# - Factory fixtures (return callables, not objects)
# - Transaction rollback (fast isolation without truncation)
# - Parametrized fixtures (test matrix generation)
# - autouse=True (implicit setup for all tests in scope)
```

</details>

### Example 9.3 — Coverage Thresholds in CI: Enforcing Quality Gates

**Problem:** Set up pytest-cov with per-package coverage thresholds, branch coverage, and CI integration that fails the build if coverage drops below targets. Handle the common pitfalls: coverage of untested files, dynamic imports, and multiprocessing.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Configuration in pyproject.toml

```bash
# pyproject.toml
[tool.pytest.ini_options]
addopts = [
    "--cov=src/",
    "--cov-branch",           # Measure branch coverage (if/else both paths)
    "--cov-report=term-missing:skip-covered",  # Show only uncovered files
    "--cov-report=xml:coverage.xml",           # For CI upload
    "--cov-report=html:htmlcov/",              # Local browsing
    "--cov-fail-under=85",    # FAIL if total coverage < 85%
]
testpaths = ["tests"]

[tool.coverage.run]
source = ["src"]
branch = true
# Include files that are never imported during tests:
omit = [
    "src/*/migrations/*",
    "src/*/conftest.py",
    "src/__main__.py",
]
# Handle multiprocessing coverage:
concurrency = ["multiprocessing", "thread"]
parallel = true

[tool.coverage.report]
# Per-module minimum thresholds:
fail_under = 85
show_missing = true
skip_covered = true
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.",
    "@overload",
    "raise NotImplementedError",
    "\\.\\.\\.",  # Ellipsis in abstract methods
]

[tool.coverage.html]
directory = "htmlcov"
```

#### Step 2: Per-Package Thresholds (Advanced)

```python
# scripts/check_coverage.py
"""
Enforce per-package coverage thresholds beyond what pytest-cov supports.
Run after pytest: python scripts/check_coverage.py
"""
import json
import sys
from pathlib import Path

# Define per-package minimum coverage
THRESHOLDS = {
    "src/core/": 95,        # Core business logic — high bar
    "src/api/": 85,         # API routes — moderate
    "src/workers/": 75,     # Background workers — lower (hard to test)
    "src/utils/": 90,       # Utilities — should be well-tested
}

def check_thresholds():
    # Read coverage JSON report
    coverage_file = Path("coverage.json")
    if not coverage_file.exists():
        print("ERROR: Run pytest --cov-report=json first")
        sys.exit(1)

    data = json.loads(coverage_file.read_text())
    files = data["files"]
    
    failures = []
    
    for package, min_coverage in THRESHOLDS.items():
        # Aggregate coverage for files in this package
        package_files = {
            path: info for path, info in files.items()
            if path.startswith(package)
        }
        
        if not package_files:
            print(f"WARNING: No files found for {package}")
            continue
        
        total_statements = sum(
            f["summary"]["num_statements"] for f in package_files.values()
        )
        covered_statements = sum(
            f["summary"]["covered_lines"] for f in package_files.values()
        )
        
        if total_statements == 0:
            continue
            
        coverage_pct = (covered_statements / total_statements) * 100
        
        status = "✅" if coverage_pct >= min_coverage else "❌"
        print(f"{status} {package:30s}: {coverage_pct:.1f}% (min: {min_coverage}%)")
        
        if coverage_pct < min_coverage:
            failures.append((package, coverage_pct, min_coverage))
    
    if failures:
        print(f"\n❌ {len(failures)} package(s) below threshold!")
        sys.exit(1)
    else:
        print("\n✅ All packages meet coverage thresholds")

if __name__ == "__main__":
    check_thresholds()
```

#### Step 3: CI Pipeline Integration

```bash
# .github/workflows/test.yml (excerpt)
# - name: Run tests with coverage
#   run: |
#     uv run pytest --cov-report=json
#     uv run python scripts/check_coverage.py
#
# - name: Upload coverage to Codecov
#   uses: codecov/codecov-action@v4
#   with:
#     files: coverage.xml
#     fail_ci_if_error: true
#
# - name: Coverage comment on PR
#   uses: orgoro/coverage@v3
#   with:
#     coverageFile: coverage.xml
#     thresholdAll: 85
```

**Final Answer:**

```python
# Coverage enforcement strategy:
# 1. Global minimum (--cov-fail-under=85) catches overall regression
# 2. Per-package thresholds (custom script) enforce higher bars for critical code
# 3. Branch coverage (--cov-branch) catches untested if/else paths
# 4. CI integration prevents merging PRs that reduce coverage
# 5. Exclude patterns (TYPE_CHECKING, overloads) avoid false negatives
#
# Anti-patterns to avoid:
# - 100% coverage target (leads to testing implementation details)
# - Covering only happy paths (branch coverage catches this)
# - Ignoring coverage of error handling code
```

</details>

---

## 📘 10. Appendix: Extended Derivations & Special Cases

### 10.1 Mutation Testing with mutmut — Beyond Line Coverage

Line coverage tells you which code was *executed* during tests. It does NOT tell you whether your tests would *catch a bug* in that code. Mutation testing fills this gap by systematically introducing bugs and checking if tests fail.

**How Mutation Testing Works:**

1. **Mutant generation:** The tool modifies your source code in small ways (mutations):
   - Replace `>` with `>=` (boundary mutation)
   - Replace `+` with `-` (arithmetic mutation)
   - Replace `True` with `False` (boolean mutation)
   - Remove a function call (statement deletion)
   - Replace `return x` with `return None`

2. **Test execution:** For each mutant, run the test suite.

3. **Classification:**
   - **Killed:** Tests fail → your tests caught the bug ✅
   - **Survived:** Tests pass → your tests missed this bug ❌
   - **Timeout:** Tests hang → likely an infinite loop mutation (killed)
   - **Incompetent:** Mutation causes import error (ignored)

**Using mutmut:**

```bash
# Install
pip install mutmut

# Run mutation testing on a specific module
mutmut run --paths-to-mutate=src/core/pricing.py --tests-dir=tests/

# View results
mutmut results
# Survived mutants (your tests didn't catch these):
# --- src/core/pricing.py:42 ---
# -    if discount > 0.5:
# +    if discount >= 0.5:
#     (Mutant #17 SURVIVED — boundary condition not tested!)

# Show specific mutant
mutmut show 17

# Apply a mutant to inspect it manually
mutmut apply 17
# ... inspect the code, write a test that catches it ...
mutmut revert
```

**Interpreting Mutation Score:**

$$
\text{Mutation Score} = \frac{\text{Killed Mutants}}{\text{Total Mutants - Incompetent Mutants}} \times 100\%
$$

- **> 80%:** Good test suite
- **> 90%:** Excellent — most bugs would be caught
- **< 60%:** Tests are superficial — high risk of undetected bugs

**Performance Considerations:**

Mutation testing is expensive: for a module with 100 possible mutations and a test suite that takes 5 seconds, you need 100 × 5s = ~8 minutes. Strategies to manage this:

```bash
# Only mutate changed files (CI optimization)
mutmut run --paths-to-mutate=$(git diff --name-only main -- 'src/*.py')

# Use incremental mode (skip already-killed mutants)
mutmut run --use-coverage  # Only mutate lines covered by tests

# Parallelize
mutmut run --runners=4
```

### 10.2 Property-Based vs Example-Based Testing — A Rigorous Comparison

**Example-based testing** (traditional): You choose specific inputs and assert specific outputs.

**Property-based testing** (Hypothesis): You describe *properties* that must hold for ALL valid inputs, and the framework generates hundreds of random inputs to test those properties.

**When Properties Are Superior:**

| Scenario | Example-based | Property-based |
|----------|--------------|----------------|
| Encode/decode roundtrip | Test 3-5 examples | Test ALL valid inputs |
| Sorting algorithm | Check [3,1,2]→[1,2,3] | Check: output sorted, same elements, same length |
| Serialization | Test known JSON | Test: deserialize(serialize(x)) == x for all x |
| Math functions | Test sin(0)=0, sin(π/2)=1 | Test: -1 ≤ sin(x) ≤ 1 for all x |
| Parser | Test 5 valid inputs | Test: parse(format(ast)) == ast for all valid ASTs |

**The Hypothesis Shrinking Advantage:**

When Hypothesis finds a failing input, it automatically **shrinks** it to the minimal reproducing case:

```python
from hypothesis import given
from hypothesis import strategies as st

@given(st.lists(st.integers()))
def test_sort_is_idempotent(xs):
    """Sorting twice gives same result as sorting once."""
    assert sorted(sorted(xs)) == sorted(xs)

@given(st.text())
def test_encode_decode_roundtrip(s):
    """UTF-8 encode/decode is lossless for all valid strings."""
    assert s.encode("utf-8").decode("utf-8") == s

@given(st.dictionaries(st.text(), st.integers()))
def test_json_roundtrip(d):
    """JSON serialization roundtrip preserves data."""
    import json
    assert json.loads(json.dumps(d)) == d
```

If `test_json_roundtrip` fails (e.g., for NaN values), Hypothesis reports the **smallest** failing dict, not the random 50-key monster it first found.

**Combining Both Approaches:**

The optimal strategy uses both:
- **Example-based:** Known edge cases, regression tests, documentation-as-tests
- **Property-based:** Invariants, roundtrips, algebraic laws, "for all valid inputs"

```python
# Example-based: specific known edge case
def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

# Property-based: algebraic law
@given(st.floats(allow_nan=False, allow_infinity=False), 
       st.floats(min_value=0.001, allow_nan=False, allow_infinity=False))
def test_division_multiplication_inverse(a, b):
    """a / b * b ≈ a (within floating point tolerance)."""
    result = divide(a, b) * b
    assert abs(result - a) < 1e-10 * max(abs(a), 1)
```

---
