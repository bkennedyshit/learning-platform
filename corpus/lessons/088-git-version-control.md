---
title: "08.8 — Git & Version Control"
subject: "Python"
catalog: advanced
audience_tier: higher-education
chapter: "8.8"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 08.8 — Git & Version Control

> *"I'm an egotistical bastard, and I name all my projects after myself. First Linux, now Git."* — Linus Torvalds

Git is not a "save button with history." It's a content-addressable filesystem with a DAG of snapshots on top. Understanding the object model (blobs, trees, commits) transforms Git from a mysterious incantation machine into a predictable tool.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Explain Git's object model: blobs, trees, commits, and refs.
2. Use branching, merging, and rebasing with confidence.
3. Resolve merge conflicts systematically.
4. Write meaningful commit messages following conventional commits.
5. Use `git bisect`, `git reflog`, and `git stash` for debugging and recovery.
6. Implement a professional branching strategy (trunk-based or GitFlow).

---

## 🖼️ Visual Anchor — Git DAG & Working Areas

![python__1.8-fig1](python__1.8-fig1.svg)

---

## 📚 1. Definitions / Concepts

### Definition 08.8.1 — Git Object Model

Git stores four types of objects, all content-addressed by SHA-1 hash:

| Object | Contains | Analogy |
|--------|----------|---------|
| **blob** | File contents (no name!) | A file's data |
| **tree** | List of (mode, name, hash) entries | A directory listing |
| **commit** | Tree hash + parent(s) + author + message | A snapshot with metadata |
| **tag** | Points to a commit with annotation | A named bookmark |

### Definition 08.8.2 — The Three Areas

1. **Working directory**: Your actual files on disk
2. **Staging area (index)**: What will go into the next commit (`git add`)
3. **Repository (.git/)**: The complete history (commits, objects, refs)

### Definition 08.8.3 — Refs and HEAD

- **Branch**: A movable pointer to a commit (e.g., `main` → `abc123`)
- **HEAD**: Points to the current branch (or directly to a commit in "detached" state)
- **Tag**: An immutable pointer to a specific commit

---

## 📐 2. Mental Models / Principles

### Principle 1.8.1 — Commits Are Snapshots, Not Diffs

Each commit stores a complete snapshot (tree) of your project. Git computes diffs on-the-fly when you ask for them. This is why operations like `checkout` and `bisect` are fast — Git doesn't replay history.

### Principle 1.8.2 — Branches Are Cheap

A branch is literally a 41-byte file containing a commit hash. Creating a branch is O(1). Use branches liberally: one per feature, one per bugfix.

### Principle 1.8.3 — The Golden Rule of Rebasing

**Never rebase commits that have been pushed to a shared branch.** Rebasing rewrites history (creates new commit hashes). If others have based work on the old commits, you'll create divergent histories.

---

## 🔑 3. Mechanics

### 3.1 — Essential Workflow

```bash
# Feature branch workflow
git checkout -b feature/auth-system
# ... make changes ...
git add -p                    # Stage interactively (review each hunk)
git commit -m "feat: add JWT authentication middleware"
git push -u origin feature/auth-system
# Create PR, get review, merge

# Keeping up with main
git fetch origin
git rebase origin/main        # Replay your commits on top of latest main
# OR: git merge origin/main   # Create a merge commit (preserves history)
```

### 3.2 — Recovery and Debugging

```bash
# Undo last commit (keep changes staged)
git reset --soft HEAD~1

# Find which commit introduced a bug
git bisect start
git bisect bad                # Current commit is broken
git bisect good v1.0.0        # This tag was working
# Git binary-searches; you test each commit and say good/bad

# Recover "lost" commits
git reflog                    # Shows ALL ref movements (even after reset)
git checkout <hash>           # Recover any commit from reflog

# Stash work-in-progress
git stash push -m "WIP: auth refactor"
git stash list
git stash pop                 # Apply and remove
```

### 3.3 — Conventional Commits

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`

```bash
git commit -m "feat(api): add rate limiting to /users endpoint"
git commit -m "fix(auth): handle expired JWT tokens gracefully"
git commit -m "perf(db): add index on users.email column"
```

---

## ✍️ 4. Derivations & Worked Examples

### Example 08.8.1 — Resolving a Merge Conflict

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```bash
# Conflict markers in file:
<<<<<<< HEAD
def authenticate(token: str) -> User:
    return verify_jwt(token)
=======
def authenticate(token: str) -> User | None:
    try:
        return verify_jwt(token)
    except ExpiredTokenError:
        return None
>>>>>>> feature/graceful-auth

# Resolution: Choose the better version (or combine)
def authenticate(token: str) -> User | None:
    try:
        return verify_jwt(token)
    except ExpiredTokenError:
        return None

# Then:
git add src/auth.py
git commit  # Completes the merge
```

</details>

---

## 💻 5. Code Patterns & Idioms

### Pattern 1.8.1 — .gitignore for Python Projects

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/
*.egg

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local

# Testing
.coverage
htmlcov/
.pytest_cache/
.mypy_cache/
```

### Pattern 1.8.2 — Git Hooks with Python

```python
#!/usr/bin/env python3
"""pre-commit hook: run ruff check before allowing commit."""
import subprocess
import sys

result = subprocess.run(["ruff", "check", "."], capture_output=True, text=True)
if result.returncode != 0:
    print("❌ Ruff check failed:\n", result.stdout, file=sys.stderr)
    sys.exit(1)
print("✓ Ruff check passed")
```

---

## ⚠️ 6. Gotchas & Anti-Patterns

### Gotcha 1.8.1 — Committing Secrets

Never commit `.env` files, API keys, or credentials. Use `.gitignore` and `git-secrets` or `trufflehog` to scan for accidental leaks.

### Gotcha 1.8.2 — Giant Binary Files

Git stores full copies of binary files. Use Git LFS for large assets (models, datasets, images).

---

## 🧮 7. Hands-On Lab

```bash
python _practice/scripts/1.8_git_vcs.py --out _practice/1.8_lab_report.md
```

Validates your Git installation, checks configuration, and walks through a branching exercise.

---

## 🔗 8. Cross-links & Further Reading

- Previous: [08.7 - Shell, Terminal & Cross-Platform CLI](08.7---Shell,-Terminal-&-Cross-Platform-CLI)
- Next: [08.9 - Docker & Containers](08.9---Docker-&-Containers)
- [Pro Git (free book)](https://git-scm.com/book/en/v2)
- [Think Like a Git](https://think-like-a-git.net/)
- [Conventional Commits](https://www.conventionalcommits.org/)



---

## 🧠 9. Extended Worked Examples & Deep Dives

### Example 9.1 — Rebase vs Merge: The Religious War Settled with Concrete Examples

**Problem:** Your team is split between "always rebase" and "always merge" camps. Demonstrate both workflows on the same scenario, show the resulting history graphs, and provide a definitive decision framework.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: The Scenario

```bash
# Main branch has progressed while you worked on feature/auth:
#
# main:         A --- B --- C --- D --- E  (team commits)
#                \
# feature/auth:  F --- G --- H  (your commits)
#
# You need to integrate main's changes before merging your feature.
```

#### Step 2: The Merge Approach

```bash
# Merge main INTO your feature branch
git checkout feature/auth
git merge main

# Result: creates a merge commit M
#
# main:         A --- B --- C --- D --- E
#                \                       \
# feature/auth:  F --- G --- H --------- M  (merge commit)
#
# Then merge feature into main (creates another merge commit):
git checkout main
git merge feature/auth

# Final history:
# main: A --- B --- C --- D --- E ----------- N  (merge commit)
#         \                       \           /
#          F --- G --- H --------- M --------
```

**Merge Pros:**
- Complete history preservation (every commit exactly as it happened)
- Non-destructive (never rewrites existing commits)
- Safe for shared branches (no force-push needed)
- Merge commits mark integration points (useful for `git bisect`)

**Merge Cons:**
- "Spaghetti history" with many branches and merge commits
- `git log` becomes hard to read (interleaved commits from multiple branches)
- Merge commits add noise (especially for trivial integrations)

#### Step 3: The Rebase Approach

```bash
# Rebase your feature ON TOP OF main
git checkout feature/auth
git rebase main

# Result: your commits are REPLAYED on top of main's latest
#
# main:         A --- B --- C --- D --- E
#                                        \
# feature/auth:                           F' --- G' --- H'  (new commits!)
#
# Note: F', G', H' are NEW commits (different SHA) with same changes as F, G, H
# The original F, G, H still exist but are unreachable (garbage collected later)

# Then fast-forward merge (no merge commit needed!):
git checkout main
git merge feature/auth  # Fast-forward: just moves main pointer to H'

# Final history:
# main: A --- B --- C --- D --- E --- F' --- G' --- H'
#
# Perfectly linear! Reads like a story.
```

**Rebase Pros:**
- Clean, linear history (easy to read, easy to bisect)
- No merge commits cluttering the log
- Each commit is a logical unit of work
- `git log --oneline` tells a clear story

**Rebase Cons:**
- Rewrites history (changes commit SHAs)
- DANGEROUS on shared branches (others' work gets orphaned)
- Conflicts must be resolved per-commit (not once like merge)
- Requires force-push if branch was already pushed

#### Step 4: The Definitive Decision Framework

```bash
# RULE 1: Never rebase commits that others have based work on.
#          If the branch is shared (others have pulled it), use merge.

# RULE 2: Rebase YOUR local/feature branches onto main before merging.
#          This gives linear history without merge commits.

# RULE 3: Use merge for long-lived branches (release branches, main).
#          Merge commits document when integrations happened.

# The "Rebase + Merge" Workflow (best of both worlds):
git checkout feature/auth
git fetch origin
git rebase origin/main        # Linearize your work on top of latest main
# Resolve any conflicts commit-by-commit
git push --force-with-lease   # Safe force-push (see Appendix 10.2)
# Create PR → squash-merge or regular merge into main
```

#### Step 5: Interactive Rebase for Cleaning Up Before PR

```bash
# Before creating a PR, clean up your commit history:
git rebase -i HEAD~5  # Interactive rebase last 5 commits

# Editor opens with:
# pick abc1234 WIP: start auth module
# pick def5678 fix typo
# pick ghi9012 add login endpoint
# pick jkl3456 fix tests
# pick mno7890 add logout endpoint

# Rewrite to:
# pick abc1234 WIP: start auth module
# squash def5678 fix typo              ← squash into previous
# pick ghi9012 add login endpoint
# squash jkl3456 fix tests             ← squash into previous
# pick mno7890 add logout endpoint

# Result: 3 clean commits instead of 5 messy ones
# "add auth module" / "add login endpoint" / "add logout endpoint"
```

**Final Answer:**

```bash
# The pragmatic workflow:
# 1. Create feature branch from main
# 2. Make commits (messy is fine during development)
# 3. Before PR: git rebase -i to clean up commits
# 4. Before PR: git rebase origin/main to linearize
# 5. Push with --force-with-lease (safe force push)
# 6. PR review → merge (or squash-merge for single-commit features)
#
# Result: main has clean, linear history with meaningful commits.
```

</details>

### Example 9.2 — Reflog Rescue Patterns: Recovering from Git Disasters

**Problem:** You accidentally ran `git reset --hard`, `git rebase` went wrong, or you deleted a branch with unmerged work. Use `git reflog` to recover seemingly lost commits.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Understanding the Reflog

```bash
# The reflog records every time a ref (branch tip, HEAD) changes.
# It's a LOCAL safety net — not shared with remotes.
# Entries expire after 90 days (reachable) or 30 days (unreachable).

git reflog
# Output:
# abc1234 HEAD@{0}: reset: moving to HEAD~3
# def5678 HEAD@{1}: commit: add payment processing
# ghi9012 HEAD@{2}: commit: add user authentication
# jkl3456 HEAD@{3}: commit: initial project setup
# mno7890 HEAD@{4}: checkout: moving from main to feature/payments

# Each entry shows: SHA, position, action, description
# HEAD@{N} means "where HEAD was N moves ago"
```

#### Step 2: Rescue — Undo Accidental reset --hard

```bash
# DISASTER: You ran git reset --hard HEAD~3 and lost 3 commits
# The commits still exist! They're just unreachable from any branch.

# Step 1: Find the lost commit in reflog
git reflog
# abc1234 HEAD@{0}: reset: moving to HEAD~3    ← current (after reset)
# def5678 HEAD@{1}: commit: add payment processing  ← LOST commit!

# Step 2: Recover by resetting back
git reset --hard def5678
# Or create a new branch pointing to the lost commit:
git branch recovered-work def5678
```

#### Step 3: Rescue — Rebase Gone Wrong

```bash
# DISASTER: Rebase created a mess with conflicts, you want to undo it entirely

# During rebase (before completing):
git rebase --abort  # Cleanly undoes the in-progress rebase

# After rebase completed (already finished):
# Find the pre-rebase state in reflog
git reflog
# abc1234 HEAD@{0}: rebase (finish): ...
# def5678 HEAD@{1}: rebase (pick): ...
# ghi9012 HEAD@{2}: rebase (start): checkout main
# jkl3456 HEAD@{3}: commit: my last commit before rebase  ← HERE!

# Reset to pre-rebase state:
git reset --hard jkl3456
# Or use ORIG_HEAD (set automatically before rebase):
git reset --hard ORIG_HEAD
```

#### Step 4: Rescue — Deleted Branch with Unmerged Work

```bash
# DISASTER: git branch -D feature/important (force-deleted unmerged branch)

# The commits still exist for 30 days (unreachable reflog expiry)
# Find the branch tip:
git reflog | grep "feature/important"
# Or search all reflogs:
git log --walk-reflogs --oneline | grep "important"

# If you know a commit message:
git log --all --oneline | grep "the commit message"
# Won't work if truly unreachable. Use:
git fsck --unreachable --no-reflogs | grep commit
# Lists all unreachable commits

# Recreate the branch:
git branch feature/important abc1234  # Point new branch at found SHA
```

#### Step 5: Rescue — Recover a Specific File from History

```bash
# You deleted a file 20 commits ago and need it back:
# Find when it was deleted:
git log --diff-filter=D --summary -- path/to/file.py
# Shows the commit that deleted it

# Restore from the commit BEFORE deletion:
git checkout abc1234^ -- path/to/file.py
# abc1234^ means "parent of abc1234" (the commit before deletion)

# Or restore from any specific commit:
git show def5678:path/to/file.py > path/to/file.py
```

**Final Answer:**

```bash
# Reflog rescue cheat sheet:
#
# Lost commits (reset --hard):  git reflog → git reset --hard SHA
# Bad rebase:                   git reset --hard ORIG_HEAD
# Deleted branch:               git reflog → git branch name SHA
# Lost file:                    git log --diff-filter=D -- file
#                               git checkout SHA^ -- file
#
# PREVENTION:
# - Use git stash before risky operations
# - Use --force-with-lease instead of --force
# - Create a backup branch: git branch backup-before-rebase
# - Reflog expires! Recover within 30 days.
```

</details>

### Example 9.3 — Submodules vs Subtrees: Managing External Dependencies in Git

**Problem:** Your project depends on an internal shared library that lives in a separate repository. Compare `git submodule` and `git subtree` for managing this dependency, showing the full workflow for each.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: The Scenario

```bash
# Your project: app-repo (main application)
# Shared library: lib-repo (used by multiple projects)
# Goal: include lib-repo's code in app-repo while tracking upstream changes
```

#### Step 2: Git Submodules Workflow

```bash
# === ADDING a submodule ===
cd app-repo
git submodule add https://github.com/org/lib-repo.git libs/shared
git commit -m "Add shared library as submodule"

# This creates:
# - .gitmodules file (tracks submodule URL and path)
# - libs/shared/ directory (checked out at a specific commit)
# - A special entry in the git tree (pointer to lib-repo commit SHA)

# === CLONING a repo with submodules ===
git clone --recurse-submodules https://github.com/org/app-repo.git
# Or after clone:
git submodule update --init --recursive

# === UPDATING to latest upstream ===
cd libs/shared
git fetch origin
git checkout main
git pull
cd ../..
git add libs/shared
git commit -m "Update shared library to latest"

# === TEAM MEMBER pulls your update ===
git pull
git submodule update --init --recursive  # MUST run this!
# Without this, libs/shared stays at the old commit
```

#### Step 3: Git Subtrees Workflow

```bash
# === ADDING a subtree ===
cd app-repo
git subtree add --prefix=libs/shared https://github.com/org/lib-repo.git main --squash
git commit -m "Add shared library as subtree"

# This COPIES the entire lib-repo history (or squashes it) into app-repo.
# No .gitmodules, no special git entries — just regular files and commits.

# === CLONING — nothing special needed! ===
git clone https://github.com/org/app-repo.git
# libs/shared/ is already there, just regular files

# === UPDATING to latest upstream ===
git subtree pull --prefix=libs/shared https://github.com/org/lib-repo.git main --squash
# Creates a merge commit incorporating upstream changes

# === PUSHING changes back to lib-repo (contributing upstream) ===
git subtree push --prefix=libs/shared https://github.com/org/lib-repo.git feature/fix
```

#### Step 4: Comparison

```bash
# | Criterion              | Submodules              | Subtrees              |
# |------------------------|-------------------------|-----------------------|
# | Clone complexity       | Need --recurse flag     | Just git clone        |
# | Team friction          | HIGH (forget update)    | LOW (just works)      |
# | Repo size              | Small (pointer only)    | Larger (full copy)    |
# | History                | Separate repo history   | Merged into main repo |
# | Upstream contribution  | Easy (cd into submod)   | git subtree push      |
# | CI/CD                  | Extra init step needed  | No extra steps        |
# | Nested dependencies    | Recursive submodules    | Manual                |
# | Pinning to version     | Exact commit SHA        | Merge commit          |
# | Removing dependency    | git rm + .gitmodules    | git rm (just files)   |
```

#### Step 5: Recommendation

```bash
# Use SUBMODULES when:
# - You need exact version pinning (security-critical deps)
# - The dependency is large and you don't want it in your repo
# - You frequently contribute back to the dependency
# - Your team is git-savvy (won't forget submodule update)

# Use SUBTREES when:
# - You want zero friction for team members (just clone and go)
# - The dependency is small-to-medium
# - You rarely need to push changes back upstream
# - CI/CD simplicity matters (no extra init steps)
# - You want the code to "just be there" in your repo

# Use NEITHER when:
# - The dependency is a proper package → use package manager (pip, npm)
# - You only need a few files → just copy them (with attribution)
```

**Final Answer:**

```bash
# Modern recommendation (2025):
# 1. First choice: Package manager (pip/uv for Python, npm for JS)
# 2. Second choice: git subtree (simpler, less team friction)
# 3. Third choice: git submodule (when you need exact pinning + upstream contrib)
#
# The #1 problem with submodules: team members forget to run
# `git submodule update --init --recursive` after pulling.
# This causes "missing files" bugs that waste hours.
```

</details>

---

## 📘 10. Appendix: Extended Derivations & Special Cases

### 10.1 Git Internals: Objects, Packfiles, and the DAG

Understanding Git's internal data model explains why operations like `rebase` create new commits, why `reflog` can recover "deleted" work, and why Git is so fast.

**The Four Object Types:**

Git's entire data model consists of four object types, stored as compressed files in `.git/objects/`:

```bash
# 1. BLOB — file contents (no filename, no metadata, just bytes)
echo "hello" | git hash-object --stdin -w
# Creates: .git/objects/ce/013625030ba8dba906f756967f9e9ca394464a
# SHA-1 hash of: "blob 6\0hello\n"

# 2. TREE — directory listing (maps names → blobs/trees + permissions)
git cat-file -p HEAD^{tree}
# 100644 blob abc123    README.md
# 040000 tree def456    src/
# 100755 blob ghi789    deploy.sh

# 3. COMMIT — snapshot pointer + metadata
git cat-file -p HEAD
# tree abc123def456...        ← points to root tree
# parent 789abc...            ← points to parent commit(s)
# author Name <email> timestamp
# committer Name <email> timestamp
#
# Commit message here

# 4. TAG — named pointer to a commit (annotated tags only)
git cat-file -p v1.0
# object abc123...            ← points to a commit
# type commit
# tag v1.0
# tagger Name <email> timestamp
#
# Release notes here
```

**The DAG (Directed Acyclic Graph):**

Commits form a DAG where each commit points to its parent(s):

```bash
# Linear history:
# A ← B ← C ← D  (each points to parent via "parent" field)
#                ↑
#              main (branch = pointer to commit)

# Merge creates a commit with TWO parents:
# A ← B ← C ← D ← F  (merge commit F has parents D and E)
#      ↑           ↗
#      └── E ──────

# Rebase creates NEW commits (different SHA) with same diffs:
# Original: A ← B ← C
# Rebased:  A ← D ← E ← B' ← C'  (B' and C' are new objects)
```

**Why Rebase Changes SHAs:**

A commit's SHA is computed from: tree hash + parent hash + author + committer + message. When you rebase, the parent changes (new base), so the SHA must change. This is why rebased commits are "new" commits — they're literally different objects.

**Packfiles (Performance Optimization):**

Loose objects (one file per object) are inefficient for large repos. Git periodically packs objects into `.git/objects/pack/` files:

```bash
# Trigger manual packing:
git gc

# Packfile format:
# - Objects stored as deltas (only differences from a base object)
# - A 1MB file that changed one line stores only the delta (~100 bytes)
# - Index file (.idx) enables O(1) lookup by SHA
# - Typical compression: 10-100x for source code repos

# View pack contents:
git verify-pack -v .git/objects/pack/pack-*.idx | head -20
```

### 10.2 How git push --force-with-lease Works

`--force-with-lease` is the safe alternative to `--force`. It prevents overwriting others' work by checking that the remote ref hasn't moved since you last fetched.

**The Problem with --force:**

```bash
# Timeline:
# 1. You fetch: origin/main = commit A
# 2. You rebase your branch (rewrites history)
# 3. Meanwhile, Alice pushes commit B to origin/main
# 4. You run: git push --force origin main
# 5. DISASTER: Alice's commit B is GONE from origin/main
```

**How --force-with-lease Prevents This:**

```bash
# git push --force-with-lease origin main
#
# Internally, this sends to the server:
# "Update main to SHA_NEW, but ONLY IF it currently points to SHA_EXPECTED"
#
# SHA_EXPECTED = what you last fetched (stored in .git/refs/remotes/origin/main)
#
# If someone pushed between your fetch and push:
# - Server's main ≠ SHA_EXPECTED
# - Push REJECTED with error: "stale info"
# - Your push fails safely — no data loss

# The safe workflow:
git fetch origin                    # Update your knowledge of remote state
git rebase origin/main              # Rebase on latest
git push --force-with-lease origin feature/my-branch  # Safe force push
```

**Edge Case — Stale Lease:**

```bash
# If you run `git fetch` but don't look at what changed,
# --force-with-lease uses the FETCHED state as the lease.
# This means: if you fetch Alice's work but don't integrate it,
# --force-with-lease will still overwrite it!

# Best practice: always rebase on the fetched state before force-pushing.
# This ensures you've incorporated any new remote commits.
```

**The Explicit Lease Form:**

```bash
# You can specify exactly what SHA you expect:
git push --force-with-lease=main:abc1234 origin main
# "Push to main, but only if it currently points to abc1234"
# This is the most explicit and safest form.
```

---



### 10.3 The Git Staging Area (Index) — Why It Exists

The staging area (index) is Git's most misunderstood feature. It sits between the working directory and the repository, acting as a "draft commit" that you build incrementally.

**Why Not Just Commit the Working Directory?**

Without staging, every commit would include ALL modified files. The staging area lets you:

1. **Commit partial changes:** You modified 5 files but only 2 are related to the current fix. Stage only those 2.

2. **Review before committing:** `git diff --staged` shows exactly what will be committed. `git diff` shows what's NOT staged. This separation enables careful review.

3. **Build commits incrementally:** Stage hunks (`git add -p`) to split a large change into logical commits.

```bash
# The three trees:
# Working Directory → (git add) → Staging Area (Index) → (git commit) → Repository
#
# git add file.py      — copy working dir version to staging
# git reset file.py    — copy repository version to staging (unstage)
# git checkout file.py — copy staging version to working dir (discard changes)
# git commit           — snapshot staging area as new commit

# Partial staging (interactive):
git add -p file.py
# Shows each hunk (chunk of changes) and asks:
# Stage this hunk [y,n,q,a,d,s,e,?]?
# y = stage this hunk
# n = skip this hunk
# s = split into smaller hunks
# e = manually edit the hunk
```

**The Index File Format:**

The staging area is stored in `.git/index` — a binary file containing:
- File paths and their blob SHAs (content hashes)
- File metadata (timestamps, permissions, size)
- Conflict markers during merge

```bash
# Inspect the index:
git ls-files --stage
# 100644 abc123 0    src/main.py    (stage 0 = normal)
# 100644 def456 1    src/conflict.py (stage 1 = base version during conflict)
# 100644 ghi789 2    src/conflict.py (stage 2 = ours)
# 100644 jkl012 3    src/conflict.py (stage 3 = theirs)
```

**Performance Optimization:**

Git uses the index's cached file metadata (mtime, size) to quickly determine which files have changed without reading their contents. This is why `git status` is fast even in large repositories — it compares filesystem metadata against the index rather than computing SHA-1 hashes of every file.

---



### 10.4 Git Hooks — Automating Quality Gates

Git hooks are scripts that run automatically at specific points in the Git workflow. They enforce code quality without relying on developer discipline.

**Client-Side Hooks (in `.git/hooks/` or managed by tools):**

```bash
# pre-commit: Runs before commit is created
# Use for: linting, formatting, type checking, secret detection
#!/usr/bin/env bash
set -euo pipefail

echo "Running pre-commit checks..."

# Format code
ruff format --check .

# Lint
ruff check .

# Type check (only changed files for speed)
changed_py=$(git diff --cached --name-only --diff-filter=ACM -- '*.py')
if [ -n "$changed_py" ](--n-"$changed_py"-); then
    mypy $changed_py
fi

# Detect secrets
if command -v detect-secrets &>/dev/null; then
    git diff --cached --name-only | xargs detect-secrets scan --baseline .secrets.baseline
fi

echo "✅ All checks passed"
```

```bash
# commit-msg: Validate commit message format
#!/usr/bin/env bash
commit_msg=$(cat "$1")

# Enforce conventional commits format
if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|test|chore|ci)(\(.+\))?: .{1,72}$"; then
    echo "❌ Commit message must follow Conventional Commits format:"
    echo "   type(scope): description"
    echo "   Examples: feat(auth): add OAuth2 login"
    echo "             fix: resolve null pointer in parser"
    exit 1
fi
```

```bash
# pre-push: Runs before push (last chance to catch issues)
#!/usr/bin/env bash
set -euo pipefail

echo "Running tests before push..."
uv run pytest tests/ -x --tb=short -q

echo "✅ Tests passed, pushing..."
```

**Managing Hooks with pre-commit framework:**

```bash
# .pre-commit-config.yaml (managed by https://pre-commit.com)
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: [--maxkb=500]

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
```

```bash
# Install hooks:
pip install pre-commit
pre-commit install          # Installs pre-commit hook
pre-commit install --hook-type commit-msg  # Installs commit-msg hook

# Run on all files (first time or CI):
pre-commit run --all-files

# Skip hooks when needed (emergency hotfix):
git commit --no-verify -m "hotfix: critical production fix"
```

**Server-Side Hooks (on the remote):**

```bash
# pre-receive: Runs on server before accepting a push
# Use for: branch protection, commit signing verification, CI gate
# GitHub/GitLab implement these as "branch protection rules" in the UI

# update: Runs once per branch being updated
# Use for: per-branch policies (e.g., require linear history on main)
```

**Key Insight:** Hooks run locally and can be bypassed with `--no-verify`. For mandatory enforcement, use server-side hooks or CI/CD pipeline checks (GitHub Actions, GitLab CI). Client-side hooks are a convenience for catching issues early, not a security boundary.

---
