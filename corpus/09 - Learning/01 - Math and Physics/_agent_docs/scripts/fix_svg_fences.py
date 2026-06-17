#!/usr/bin/env python3
"""
fix_svg_fences.py

Strips ```svg ... ``` and ```xml ... ``` code-fence wrappers from around
inline <svg>...</svg> blocks so that Obsidian renders them as actual SVG
diagrams instead of literal code text.

Idempotent: safe to re-run.

Usage:
    python fix_svg_fences.py                # process the entire 07 - Math and Physics tree
    python fix_svg_fences.py --dry-run      # preview without writing
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


# Match a ```svg or ```xml fence followed by a single <svg>...</svg> block
# followed by a closing ``` fence.  Non-greedy on the SVG body so we don't
# swallow multiple SVG blocks in one match.
SVG_FENCE_PATTERN = re.compile(
    r"```(?:svg|xml)\s*\n(<svg[\s\S]*?</svg>)\s*\n```",
    re.MULTILINE,
)


def process_file(path: Path, dry_run: bool) -> int:
    """Return number of SVG fences stripped from this file (0 if none)."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return 0
    new_text, count = SVG_FENCE_PATTERN.subn(r"\1", text)
    if count > 0 and not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=r"C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\09 - Learning\07 - Math and Physics",
        help="Root directory to recurse",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview only, do not write")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        print(f"ERROR: root does not exist: {root}")
        return 1

    modified_files: list[tuple[Path, int]] = []
    total = 0
    for md_file in root.rglob("*.md"):
        # Skip _agent_docs (those contain intentional ```xml templates for reference)
        if "_agent_docs" in md_file.parts:
            continue
        n = process_file(md_file, args.dry_run)
        if n > 0:
            modified_files.append((md_file, n))
            total += n

    verb = "Would strip" if args.dry_run else "Stripped"
    print(f"\n{verb} {total} SVG code-fence wrappers across {len(modified_files)} files\n")
    for p, n in sorted(modified_files):
        rel = p.relative_to(root)
        print(f"  {n:2d} x  {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
