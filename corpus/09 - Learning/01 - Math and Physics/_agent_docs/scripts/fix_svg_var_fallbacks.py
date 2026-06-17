#!/usr/bin/env python3
"""
fix_svg_var_fallbacks.py

Add explicit fallback colors to every `var(--name)` call inside SVG files.
This makes diagrams render correctly when Obsidian embeds them via <img>
(which doesn't propagate host-page CSS variables).

CSS spec: `var(--name, fallback)` uses the fallback only when --name is not
defined.  When Obsidian inlines the SVG into its DOM (older versions, or
plugins), the host theme's variables still win because they're defined on
ancestor elements.  When Obsidian uses an <img> tag, the fallback kicks in.

Idempotent: a `var(--name)` already containing a fallback is left alone.

Targets (run on both, default):
  09 - Learning/_svgs/                                  (193+ chapter SVGs)
  08 - AET_Knowledge_Base/math-vault/svgs/              (user's existing 9 SVGs)

Usage:
    python fix_svg_var_fallbacks.py             # process both folders
    python fix_svg_var_fallbacks.py --dry-run   # preview only
    python fix_svg_var_fallbacks.py --root <dir>  # process a single folder
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

# Mapping: CSS variable name -> dark-theme fallback color (GitHub-dark palette,
# same family Obsidian's default dark theme produces, also matches Bill's
# existing math-vault SVGs).
FALLBACKS = {
    "text-normal": "#c9d1d9",
    "text-muted": "#8b949e",
    "interactive-accent": "#58a6ff",
    "text-accent": "#79c0ff",
    "background-primary": "#0d1117",
    "background-secondary": "#161b22",
    "background-modifier-border": "#30363d",
    "h1-color": "#f0f6fc",
}

# Match `var(--name)` with NO existing fallback.  Captures the variable name.
# Negative lookahead would be ideal but is risky cross-engine; simpler to use
# a permissive match and inspect the captured group.
VAR_PATTERN = re.compile(r"var\(\s*--([a-zA-Z0-9_-]+)\s*\)")


def patch_text(text: str) -> tuple[str, int]:
    """Replace `var(--x)` with `var(--x, FALLBACK)` for known variables."""
    count = 0

    def _sub(match: re.Match) -> str:
        nonlocal count
        name = match.group(1)
        if name in FALLBACKS:
            count += 1
            return f"var(--{name}, {FALLBACKS[name]})"
        # Unknown variable — leave alone (don't invent fallbacks)
        return match.group(0)

    new_text = VAR_PATTERN.sub(_sub, text)
    return new_text, count


def process_dir(root: Path, dry_run: bool) -> tuple[int, int]:
    """Returns (files_modified, total_replacements)."""
    files_modified = 0
    total = 0
    if not root.is_dir():
        return 0, 0
    for svg in sorted(root.iterdir()):
        if svg.suffix.lower() != ".svg":
            continue
        text = svg.read_text(encoding="utf-8")
        new_text, n = patch_text(text)
        if n > 0:
            if not dry_run:
                svg.write_text(new_text, encoding="utf-8")
            files_modified += 1
            total += n
            print(f"  {n:3d}  {svg.name}")
    return files_modified, total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--root", type=Path, default=None,
                        help="If given, process only this directory.")
    args = parser.parse_args()

    if args.root:
        roots = [args.root]
    else:
        roots = [
            Path(r"C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\09 - Learning\_svgs"),
            Path(r"C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\08 - AET_Knowledge_Base\math-vault\svgs"),
        ]

    grand_files = 0
    grand_total = 0
    for r in roots:
        print(f"\n[{r}]")
        f, t = process_dir(r, args.dry_run)
        grand_files += f
        grand_total += t

    verb = "Would patch" if args.dry_run else "Patched"
    print(f"\n{verb} {grand_total} var() references across {grand_files} SVG files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
