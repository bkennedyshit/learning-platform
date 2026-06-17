#!/usr/bin/env python3
"""
centralize_svgs.py

Migrate every per-subject _svgs/ folder into a single vault-wide
`09 - Learning/_svgs/` folder. To avoid filename collisions (math chapter 8.1
vs track-08 chapter 8.1 etc.), prefix every file with its subject_id slug:

    01 - Mathematical Foundations & Calculus/_svgs/1.1-fig1.svg
        ->  _svgs/math-01__1.1-fig1.svg

    08 - App Architectures & Frameworks/_svgs/8.1-fig1.svg
        ->  _svgs/track-08__8.1-fig1.svg

Also rewrites every chapter's `![[<old_name>]]` wikilink to point at the
new global filename, and removes the now-empty per-subject _svgs/ folders.

Idempotent: chapters whose wikilinks already use the prefixed names are
left untouched; per-subject _svgs/ folders that are missing are skipped.

Subject_id slug rules match the GUI backend (chapter_reader.py):
  - Math sub-subject "01 - Mathematical..." -> "math-01"
  - Math sub-subject "12 - Solid..." -> "math-12"
  - Other tracks: take the leading "NN" -> "track-NN"

Usage:
    python centralize_svgs.py --dry-run     # preview only
    python centralize_svgs.py               # actually move files
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(r"C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\09 - Learning")

MATH_TRACK = "07 - Math and Physics"
OTHER_TRACKS = [
    "08 - App Architectures & Frameworks",
    "09 - VR & 3D Engineering",
    "10 - AI & Machine Learning Systems",
    "11 - Neuroscience & Computational Cognition",
    "12 - Behavioral Psychology & Reinforcement Learning",
    "13 - Biomechanics & Human-Computer Interface (HCI)",
]

CENTRAL_SVGS = ROOT / "_svgs"

# Match a chapter or non-chapter folder leading number-prefix
LEADING_NUM = re.compile(r"^(\d+)")


def subject_id_for(subject_dir: Path) -> str:
    """Return the GUI subject_id slug for a subject directory."""
    rel = subject_dir.relative_to(ROOT).parts
    if rel[0] == MATH_TRACK:
        # Math sub-subject like "02 - Linear Algebra & Matrix Theory"
        m = LEADING_NUM.match(subject_dir.name)
        if not m:
            raise ValueError(f"Cannot derive subject_id from math sub-folder: {subject_dir}")
        return f"math-{m.group(1).zfill(2)}"
    # Top-level non-math track like "08 - App Architectures..."
    m = LEADING_NUM.match(rel[0])
    if not m:
        raise ValueError(f"Cannot derive subject_id from top-level: {subject_dir}")
    return f"track-{m.group(1).zfill(2)}"


def find_subject_dirs() -> list[Path]:
    """Every directory containing both a Subject_Plan.md and an _svgs/ folder."""
    dirs: list[Path] = []
    math_dir = ROOT / MATH_TRACK
    if math_dir.is_dir():
        for child in sorted(math_dir.iterdir()):
            if child.is_dir() and (child / "Subject_Plan.md").exists():
                dirs.append(child)
    for name in OTHER_TRACKS:
        p = ROOT / name
        if p.is_dir() and (p / "Subject_Plan.md").exists():
            dirs.append(p)
    return dirs


def update_wikilinks(chapter_text: str, mapping: dict[str, str]) -> tuple[str, int]:
    """Replace `![[old.svg|...]]` references with `![[new.svg|...]]`.
    Returns (new_text, replacement_count).
    """
    if not mapping:
        return chapter_text, 0
    count = 0

    def _sub(match: re.Match) -> str:
        nonlocal count
        old = match.group(1)
        rest = match.group(2) or ""  # |width or empty
        if old in mapping:
            count += 1
            return f"![[{mapping[old]}{rest}]]"
        return match.group(0)

    pattern = re.compile(r"!\[\[([^|\]]+\.svg)(\|[^\]]+)?\]\]")
    new_text = pattern.sub(_sub, chapter_text)
    return new_text, count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview file moves and wikilink rewrites without doing anything")
    args = parser.parse_args()

    if not args.dry_run:
        CENTRAL_SVGS.mkdir(exist_ok=True)

    total_moves = 0
    total_skips = 0
    total_chapter_rewrites = 0
    chapter_count = 0

    # name_map[subject_id][old_filename] = new_filename
    rename_log: list[tuple[Path, str, str]] = []

    subject_dirs = find_subject_dirs()
    for subject_dir in subject_dirs:
        sid = subject_id_for(subject_dir)
        local_svgs = subject_dir / "_svgs"
        if not local_svgs.is_dir():
            continue

        # Build map of old -> new filenames for this subject
        rename_map: dict[str, str] = {}
        for svg in sorted(local_svgs.iterdir()):
            if svg.suffix.lower() != ".svg":
                continue
            old_name = svg.name
            # If a file already has the subject_id prefix, leave it alone (idempotent re-run)
            if old_name.startswith(f"{sid}__"):
                rename_map[old_name] = old_name
                continue
            new_name = f"{sid}__{old_name}"
            rename_map[old_name] = new_name
            target = CENTRAL_SVGS / new_name
            if target.exists() and not args.dry_run:
                # Already migrated; skip
                total_skips += 1
                continue
            if not args.dry_run:
                shutil.move(str(svg), str(target))
            rename_log.append((subject_dir.relative_to(ROOT), old_name, new_name))
            total_moves += 1

        # Rewrite all chapter .md files in subject_dir
        for md in sorted(subject_dir.glob("*.md")):
            if md.name in {"Subject_Plan.md", "README.md"}:
                continue
            text = md.read_text(encoding="utf-8")
            new_text, n = update_wikilinks(text, rename_map)
            if n > 0:
                if not args.dry_run:
                    md.write_text(new_text, encoding="utf-8")
                total_chapter_rewrites += n
                chapter_count += 1

        # Remove now-empty subject _svgs/ folder
        if not args.dry_run and local_svgs.exists():
            try:
                if not any(local_svgs.iterdir()):
                    local_svgs.rmdir()
            except OSError:
                pass

    verb = "Would migrate" if args.dry_run else "Migrated"
    print(f"\n{verb} {total_moves} SVG files into {CENTRAL_SVGS.relative_to(ROOT)}/")
    print(f"{'Would skip' if args.dry_run else 'Skipped'} {total_skips} already-migrated files")
    print(f"{'Would rewrite' if args.dry_run else 'Rewrote'} {total_chapter_rewrites} wikilinks across {chapter_count} chapter files")
    print()
    if rename_log[:8]:
        print("Sample renames:")
        for sub_rel, old, new in rename_log[:8]:
            print(f"  {sub_rel}/_svgs/{old}  ->  _svgs/{new}")
        if len(rename_log) > 8:
            print(f"  ... and {len(rename_log) - 8} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
