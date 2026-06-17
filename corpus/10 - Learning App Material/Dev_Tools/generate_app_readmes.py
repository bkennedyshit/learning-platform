#!/usr/bin/env python3
"""
generate_app_readmes.py

Write/refresh a README.md inside every subject folder under `10 - Learning App Material/Subjects/`.
Each README serves as a one-page subject hub containing:
  1. Quick start for practice scripts
  2. Active drill scripts table with sample commands
  3. Complete chapter index
  4. Free Learning Catalog (extracted verbatim from Subject_Plan §2)
  5. Placeholders for study aids (NotebookLM, flashcards, quizzes)
"""

from __future__ import annotations

import re
from pathlib import Path
from textwrap import dedent

ROOT = Path(r"C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\10 - Learning App Material")
SUBJECTS_DIR = ROOT / "Subjects"

def find_subject_folders() -> list[Path]:
    folders: list[Path] = []
    if SUBJECTS_DIR.is_dir():
        for child in sorted(SUBJECTS_DIR.iterdir()):
            if child.is_dir() and (child / "Subject_Plan.md").exists():
                folders.append(child)
    return folders

def list_drill_scripts(subject: Path) -> list[Path]:
    scripts_dir = subject / "_practice" / "scripts"
    if not scripts_dir.is_dir():
        return []
    return sorted(p for p in scripts_dir.iterdir() if p.suffix == ".py")

def list_chapters(subject: Path) -> list[Path]:
    chapters: list[Path] = []
    for md in sorted(subject.glob("*.md")):
        if md.name in {"Subject_Plan.md", "README.md", "LEARNING_PATH.md"}:
            continue
        # Make sure it matches a chapter filename pattern (e.g. 02.1 - ...)
        if re.match(r"^\d+\.\d+", md.name):
            chapters.append(md)
    return chapters

def chapter_for_script(script: Path, chapters: list[Path]) -> str | None:
    stem = script.stem
    chapter_num = stem.split("_", 1)[0]
    for ch in chapters:
        if ch.name.startswith(chapter_num + " "):
            return ch.stem
    return None

H2_PATTERN = re.compile(r"^##\s+(\S+\s+)?(\d+)\.\s+(.+?)\s*$", re.MULTILINE)

def extract_section_2(plan_text: str) -> tuple[str, str] | None:
    """Return (heading_title, body_markdown) for whichever H2 starts with '2.',
    or None if the plan doesn't follow the convention."""
    matches = list(H2_PATTERN.finditer(plan_text))
    if not matches:
        return None
    section_2 = next((m for m in matches if m.group(2) == "2"), None)
    section_3 = next((m for m in matches if m.group(2) == "3"), None)
    if section_2 is None:
        return None
    start = section_2.end()
    end = section_3.start() if section_3 else len(plan_text)
    body = plan_text[start:end].strip()
    title = section_2.group(3).strip()
    return title, body

STUDY_AIDS_PLACEHOLDER = dedent(
    """\
    > **Status:** placeholder. Drop links to NotebookLM-generated artifacts here as
    > you create them. Each subsection currently has a single TODO bullet — replace
    > or append `[[wikilinks]]` and external URLs once the artifact exists.

    ### 🎙️ Audio overviews & podcasts (NotebookLM)

    - [ ] TODO: paste the NotebookLM "Audio Overview" link or attach the `.mp3`/`.m4a` file

    ### 🧠 Mind maps

    - [ ] TODO: NotebookLM mind-map URL or screenshot

    ### ❓ Quizzes

    - [ ] TODO: NotebookLM-generated quiz (paste questions or link)

    ### 📊 Reports & summaries

    - [ ] TODO: NotebookLM "Briefing Doc" or "Study Guide" output

    ### 🃏 Flash cards

    - [ ] TODO: deck export (Anki, Obsidian SR, NotebookLM cards)

    ### 🎬 Video overviews

    - [ ] TODO: YouTube / loom / personal recording link
    """
)

def render_readme(subject: Path) -> str:
    chapters = list_chapters(subject)
    scripts = list_drill_scripts(subject)
    subject_name = subject.name
    plan_path = subject / "Subject_Plan.md"
    plan_text = plan_path.read_text(encoding="utf-8") if plan_path.exists() else ""
    section_2 = extract_section_2(plan_text)

    # Deriving track code from name
    track_match = re.match(r"^(\d+)", subject_name)
    app_track = track_match.group(1) if track_match else "01"

    # ---- Drill script table ----------------------------------------------
    script_rows: list[str] = []
    for script in scripts:
        ch_stem = chapter_for_script(script, chapters)
        ch_link = f"[[{ch_stem}]]" if ch_stem else "—"
        rel = script.relative_to(subject).as_posix()
        cmd = f'`python "{rel}" --count 8 --seed 42`'
        script_rows.append(f"| {script.name} | {ch_link} | {cmd} |")
    if not script_rows:
        script_rows.append("| _(no drill scripts in this subject yet)_ | — | — |")

    # ---- Chapter index ---------------------------------------------------
    chapter_rows: list[str] = []
    for ch in chapters:
        chapter_rows.append(f"- [[{ch.stem}]]")
    if not chapter_rows:
        chapter_rows.append("- _(no chapter notes scaffolded yet)_")

    # ---- Source materials block -----------------------------------------
    if section_2 is not None:
        title, body = section_2
        source_block = (
            f"_Pulled verbatim from `Subject_Plan.md §2 — {title}`. Source of truth "
            f"is the Subject_Plan; this section is a convenience copy._\n\n"
            f"{body}"
        )
    else:
        source_block = (
            "_The `Subject_Plan.md` for this subject does not follow the standard "
            "`## 2. ...` heading convention. Edit Subject_Plan or this README "
            "by hand to populate the resource list._"
        )

    # ---- Final markdown --------------------------------------------------
    body = dedent(
        f"""\
        ---
        date: 2026-05-29
        type: readme
        tags: [app-curriculum, practice, syllabus, index, readme]
        title: "README — {subject_name}"
        app-track: "{app_track}"
        ---

        # {subject_name} — Subject Hub

        *Part of [[Bill's Vault/05-Knowledge_Foundation/10 - Learning App Material/README|10 - Learning App Material]]*

        > One-page subject hub. Lists chapters, practice scripts, free authoritative catalogs, and generated study aids.

        ---

        ## 🚀 Practice Quick Start

        From a terminal in this subject's folder:

        ```bash
        cd "Subjects/{subject.name}"
        python "_practice/scripts/<script_name>.py" --count 8
        ```

        ---

        ## 📜 Chapter Index

        """
    )
    body += "\n".join(chapter_rows) + "\n\n---\n\n"

    body += dedent(
        """\
        ## 🎯 Practice & Drill Scripts

        ## 🎯 Practice & Drill Scripts

        | Script | Chapter | Sample Command |
        |---|---|---|
        """
    )
    body += "\n".join(script_rows) + "\n\n---\n\n"

    body += dedent(
        """\
        ## 📚 Authoritative Catalogs & Sources

        """
    )
    body += source_block + "\n\n---\n\n"

    body += dedent(
        """\
        ## 🧰 Generated Study Aids (NotebookLM)

        """
    )
    body += STUDY_AIDS_PLACEHOLDER + "\n---\n\n"

    body += dedent(
        f"""\
        ## 🔗 Cross-Links

        - Full Curriculum Plan: [[Subject_Plan]]
        - Active Learning Roadmap: [[LEARNING_PATH]]
        - Master App Delivery Platform: [[Bill's Vault/05-Knowledge_Foundation/10 - Learning App Material/README]]
        """
    )
    return body

def main() -> int:
    subjects = find_subject_folders()
    written: list[Path] = []
    print("Starting compilation of K-12 App Subject README hubs...")
    for subject in subjects:
        readme = subject / "README.md"
        readme.write_text(render_readme(subject), encoding="utf-8")
        written.append(readme)

    print(f"\nCompleted: Wrote {len(written)} README.md files:")
    for p in written:
        rel = p.relative_to(ROOT)
        print(f"  - {rel}  ({p.stat().st_size:,} bytes)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
