#!/usr/bin/env python3
"""
migrate_svgs_to_files.py

Walk every chapter `.md` file under 09 - Learning, extract every inline
<svg>...</svg> block into a separate `.svg` file in a sibling `_svgs/`
folder, and replace the inline block in the chapter with an Obsidian
wikilink reference like  ![[1.1-fig1.svg|600]]

Width hint comes from the SVG's `style="...max-width:Npx..."` attribute,
defaulting to 600 if absent.

Idempotent: chapters that no longer contain inline <svg> are skipped.
Skips _agent_docs/, _examples/, _practice/, _svgs/, and the
SVG_TEMPLATES.md / AGENT_MANUAL.md reference files.

Usage:
    python migrate_svgs_to_files.py --dry-run       # preview only
    python migrate_svgs_to_files.py                 # write changes
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(r"C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\09 - Learning")

# Folder names that contain reference / generated material we should not touch
SKIP_DIR_PARTS = {"_agent_docs", "_examples", "_practice", "_svgs"}

# Filenames to never process
SKIP_FILES = {"SVG_TEMPLATES.md", "AGENT_MANUAL.md"}

# Match a complete <svg ...> ... </svg> block (single or multi-line, non-greedy)
SVG_PATTERN = re.compile(r"<svg\b[^>]*>[\s\S]*?</svg>", re.MULTILINE)

# Extract the first max-width:Npx hint from the SVG's outer style attribute
WIDTH_PATTERN = re.compile(r"max-width:\s*(\d+)\s*px", re.IGNORECASE)


def chapter_num_from_filename(fname: str) -> str:
    """'1.1 - Limits & Continuity.md' -> '1.1', falls back to filename stem."""
    m = re.match(r"^(\d+\.\d+)", fname)
    return m.group(1) if m else Path(fname).stem


def extract_width(svg_text: str) -> int:
    """Return the first max-width:Npx hint, defaulting to 600."""
    m = WIDTH_PATTERN.search(svg_text)
    return int(m.group(1)) if m else 600


def looks_like_chapter_note(md: Path) -> bool:
    """A chapter file starts with a number-dot-number prefix."""
    return bool(re.match(r"^\d+\.\d+", md.name))


def process_chapter(md: Path, dry_run: bool) -> tuple[int, list[str]]:
    """Extract every inline <svg>...</svg> from `md`. Returns (count, filenames)."""
    text = md.read_text(encoding="utf-8")
    matches = list(SVG_PATTERN.finditer(text))
    if not matches:
        return 0, []

    chapter_num = chapter_num_from_filename(md.name)
    svgs_dir = md.parent / "_svgs"
    new_text = text
    filenames: list[str] = []

    # Iterate from last to first so earlier-position spans stay valid as we splice.
    for back_i, match in enumerate(reversed(matches)):
        forward_idx = len(matches) - back_i  # 1-based forward index
        svg_content = match.group(0)
        width = extract_width(svg_content)
        svg_filename = f"{chapter_num}-fig{forward_idx}.svg"
        wikilink = f"![[{svg_filename}|{width}]]"

        if not dry_run:
            svgs_dir.mkdir(exist_ok=True)
            (svgs_dir / svg_filename).write_text(svg_content, encoding="utf-8")

        start, end = match.span()
        new_text = new_text[:start] + wikilink + new_text[end:]
        filenames.append(svg_filename)

    if not dry_run:
        md.write_text(new_text, encoding="utf-8")

    return len(matches), filenames[::-1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would happen without writing.")
    parser.add_argument("--root", default=str(ROOT),
                        help="Root directory to recurse (default: 09 - Learning).")
    args = parser.parse_args()

    root = Path(args.root)
    total_svgs = 0
    total_chapters = 0

    for md in root.rglob("*.md"):
        if md.name in SKIP_FILES:
            continue
        if any(part in SKIP_DIR_PARTS for part in md.parts):
            continue
        if not looks_like_chapter_note(md):
            continue

        count, names = process_chapter(md, args.dry_run)
        if count > 0:
            total_svgs += count
            total_chapters += 1
            rel = md.relative_to(root)
            print(f"  {count:2d}x  {rel}")
            for n in names:
                print(f"        -> _svgs/{n}")

    verb = "Would extract" if args.dry_run else "Extracted"
    print(f"\n{verb} {total_svgs} SVGs from {total_chapters} chapter files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
