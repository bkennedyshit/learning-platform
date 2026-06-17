---
title: "Rust Practice Scripts"
subject: "scripts"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: readme
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# Rust Practice Scripts

## Scripts

### `14.2_ownership_drills.py`
Generates randomized ownership/borrowing/lifetime drill problems as Markdown.
Each problem presents a Rust snippet and asks whether it compiles.

```bash
python 14.2_ownership_drills.py                    # 12 problems, random seed
python 14.2_ownership_drills.py --count 20 --seed 42
python 14.2_ownership_drills.py --out drills.md    # Write to file
```

### `rust_lab_runner.py`
Compiles and runs Rust exercise files, generating pass/fail reports.
Expects `cargo` on PATH.

```bash
# Single file
python rust_lab_runner.py --file solution.rs --expect-compile
python rust_lab_runner.py --file broken.rs --expect-fail

# Directory (ok_*.rs should compile, err_*.rs should fail)
python rust_lab_runner.py --dir exercises/ --report report.md
```

## Exercise Naming Convention

Place exercise files in `exercises/`:
- `ok_move_basics.rs` — should compile successfully
- `err_double_borrow.rs` — should fail to compile (tests understanding)

## Requirements

- Python 3.10+
- Rust toolchain (`rustup`, `cargo`) on PATH
- No additional Python packages needed
