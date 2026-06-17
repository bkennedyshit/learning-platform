#!/usr/bin/env python3
"""
centralize_app_svgs.py

Migrate every per-subject `_svgs/` folder inside `10 - Learning App Material/Subjects/`
into a single global `10 - Learning App Material/_svgs/` folder.
Prefixes every file with its `app-[subject_id]` slug to prevent collisions:

    Subjects/02 - Early Numeracy K-5/_svgs/02.1-fig1.svg
        ->  _svgs/app-02__02.1-fig1.svg

Also rewrites every chapter's `![[<old_name>]]` wikilink to point at the new global
filename, and removes the now-empty per-subject `_svgs/` folders.
"""

from __future__ import annotations

import sys
import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(r"C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\10 - Learning App Material")
SUBJECTS_DIR = ROOT / "Subjects"
CENTRAL_SVGS = ROOT / "_svgs"

# Match a chapter leading number-prefix
LEADING_NUM = re.compile(r"^(\d+)")

def safe_print(msg: str):
    """Prints safely to stdout by falling back to ASCII-only representation on encoding failure."""
    try:
        print(msg)
    except UnicodeEncodeError:
        try:
            print(msg.encode(sys.stdout.encoding or 'ascii', errors='replace').decode(sys.stdout.encoding or 'ascii'))
        except Exception:
            try:
                print(msg.encode('ascii', errors='replace').decode('ascii'))
            except Exception:
                pass

def subject_id_for(subject_dir: Path) -> str:
    """Return the app-NN slug for a subject directory."""
    m = LEADING_NUM.match(subject_dir.name)
    if not m:
        raise ValueError(f"Cannot derive subject_id from folder: {subject_dir}")
    return f"app-{m.group(1).zfill(2)}"

def find_subject_dirs() -> list[Path]:
    """Every directory under Subjects/ containing a Subject_Plan.md."""
    dirs: list[Path] = []
    if SUBJECTS_DIR.is_dir():
        for child in sorted(SUBJECTS_DIR.iterdir()):
            if child.is_dir() and (child / "Subject_Plan.md").exists():
                dirs.append(child)
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

    rename_log: list[tuple[Path, str, str]] = []

    subject_dirs = find_subject_dirs()
    safe_print("Starting centralization of K-12 App SVG files...")
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
            # If a file already has the prefix, leave it alone
            if old_name.startswith(f"{sid}__"):
                rename_map[old_name] = old_name
                continue
            new_name = f"{sid}__{old_name}"
            rename_map[old_name] = new_name
            target = CENTRAL_SVGS / new_name
            
            if target.exists() and not args.dry_run:
                total_skips += 1
                continue
                
            if not args.dry_run:
                shutil.move(str(svg), str(target))
                
            rename_log.append((subject_dir.relative_to(ROOT), old_name, new_name))
            total_moves += 1

        # Rewrite all chapter .md files in subject_dir
        for md in sorted(subject_dir.glob("*.md")):
            if md.name in {"Subject_Plan.md", "README.md", "LEARNING_PATH.md"}:
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
    safe_print(f"\nCompleted: {verb} {total_moves} SVG files into {CENTRAL_SVGS.name}/")
    safe_print(f"Skipped {total_skips} already-migrated files")
    safe_print(f"Rewrote {total_chapter_rewrites} wikilinks across {chapter_count} chapter files")
    safe_print("")
    if rename_log[:8]:
        safe_print("Sample renames:")
        for sub_rel, old, new in rename_log[:8]:
            safe_print(f"  {sub_rel}/_svgs/{old}  ->  _svgs/{new}")
        if len(rename_log) > 8:
            safe_print(f"  ... and {len(rename_log) - 8} more")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
