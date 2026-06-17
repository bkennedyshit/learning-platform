#!/usr/bin/env python3
"""
generate_readmes.py — write/refresh a README.md inside every subject and track
folder under 09 - Learning. Each README is a one-page subject hub:

  1. Quick start for running drill scripts
  2. Available drill scripts (with copy-paste commands)
  3. Chapter index (with [[wikilinks]])
  4. Source Materials & References  (extracted verbatim from Subject_Plan §2)
  5. Generated Study Aids  (placeholder sections for NotebookLM artifacts:
     audio overviews, mind maps, quizzes, reports, flash cards,
     video overviews, data tables — to be filled in over time)
  6. Cross-links

Idempotent: re-run any time chapters, scripts, Subject_Plan content, or the
artifacts list change.
"""

from __future__ import annotations

import re
from pathlib import Path
from textwrap import dedent

ROOT = Path(r"C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\09 - Learning")

MATH_ROOT = ROOT / "07 - Math and Physics"

TRACK_FOLDERS = [
    "01- Python",
    "02 - C++",
    "03 - C hash",
    "04 - Game_Dev",
    "05 - AI_Experiments",
    "05 - JavaScript",
    "06 - Game Design",
    "06 - TypeScript",
    "07 - SQL",
    "08 - App Architectures & Frameworks",
    "09 - VR & 3D Engineering",
    "10 - AI & Machine Learning Systems",
    "11 - Neuroscience & Computational Cognition",
    "12 - Behavioral Psychology & Reinforcement Learning",
    "13 - Biomechanics & Human-Computer Interface (HCI)",
    "14 - Rust",
    "15 - Biology",
    "16 - Chemistry",
]


# --------------------------------------------------------------------------
# Discovery
# --------------------------------------------------------------------------
def find_subject_folders() -> list[Path]:
    folders: list[Path] = []
    for p in sorted(MATH_ROOT.iterdir()):
        if p.is_dir() and (p / "Subject_Plan.md").exists():
            folders.append(p)
    for name in TRACK_FOLDERS:
        p = ROOT / name
        if p.is_dir() and (p / "Subject_Plan.md").exists():
            folders.append(p)
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
        if md.name.lower().startswith("readme"):
            continue
        chapters.append(md)
    return chapters


def chapter_for_script(script: Path, chapters: list[Path]) -> str | None:
    stem = script.stem
    chapter_num = stem.split("_", 1)[0]
    for ch in chapters:
        if ch.name.startswith(chapter_num + " "):
            return ch.stem
    return None


def relative_howto(subject: Path) -> str:
    parts = subject.relative_to(ROOT).parts
    depth = len(parts)
    return "../" * depth + "HOW_TO_USE_PRACTICE.md"


# --------------------------------------------------------------------------
# Subject_Plan section extraction
# --------------------------------------------------------------------------
# Match an H2 line whose first chunk after the "## " starts the second
# numbered section.  Examples that should match:
#   "## 📚 2. Premium Free Learning Catalog"
#   "## 🏗️ 2. Architectural Deep Dives"
#   "## 📚 2. Web-Verified Authoritative Learning Catalog"
#   "## 📚 2. Core Subjects"
H2_PATTERN = re.compile(r"^##\s+\S+\s+(\d+)\.\s+(.+?)\s*$", re.MULTILINE)


def extract_section_2(plan_text: str) -> tuple[str, str] | None:
    """Return (heading_title, body_markdown) for whichever H2 starts with '2.',
    or None if the plan doesn't follow the convention."""
    matches = list(H2_PATTERN.finditer(plan_text))
    if not matches:
        return None
    section_2 = next((m for m in matches if m.group(1) == "2"), None)
    section_3 = next((m for m in matches if m.group(1) == "3"), None)
    if section_2 is None:
        return None
    start = section_2.end()
    end = section_3.start() if section_3 else len(plan_text)
    body = plan_text[start:end].strip()
    title = section_2.group(2).strip()
    return title, body


# --------------------------------------------------------------------------
# Render
# --------------------------------------------------------------------------
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

    ### 📋 Data tables

    - [ ] TODO: structured data extracted from the chapters (CSV / Markdown table)
    """
)


def render_readme(subject: Path) -> str:
    chapters = list_chapters(subject)
    scripts = list_drill_scripts(subject)
    subject_name = subject.name
    howto_link = relative_howto(subject)
    plan_path = subject / "Subject_Plan.md"
    plan_text = plan_path.read_text(encoding="utf-8") if plan_path.exists() else ""
    section_2 = extract_section_2(plan_text)

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
        chapter_rows.append("- _(no chapter notes yet)_")

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
            "`## 📚 2. ...` heading convention. Edit Subject_Plan or this README "
            "by hand to populate the resource list._"
        )

    # ---- Final markdown --------------------------------------------------
    body = dedent(
        f"""\
        ---
        date: 2026-05-24
        type: subject-readme
        tags: [practice, refresher, drills, source-materials, study-aids]
        title: "README — {subject_name}"
        ---

        # {subject_name} — Subject Hub

        > One-page subject hub. Lists chapters, drill commands, source reading
        > materials, and placeholders for generated study aids (NotebookLM artifacts:
        > audio overviews, mind maps, quizzes, flash cards, etc.).
        > Master practice guide: [[{howto_link.replace('.md','')}|HOW_TO_USE_PRACTICE]].

        ---

        ## 🚀 Quick start

        From a terminal in this folder:

        ```bash
        cd "{subject.as_posix()}"
        python "_practice/scripts/<chapter>_<topic>.py" --count 8 --seed 42
        ```

        Output lands at `_practice/<chapter>_drills.md`. Open in Obsidian Reading
        view, do the problems on paper, click **Show solution** to verify.

        ---

        ## 📜 Chapter index

        """
    )
    body += "\n".join(chapter_rows) + "\n\n---\n\n"

    body += dedent(
        """\
        ## 🎯 Drill scripts

        | Script | Chapter | Sample command |
        |---|---|---|
        """
    )
    body += "\n".join(script_rows) + "\n\n---\n\n"

    body += dedent(
        """\
        ## 📚 Source materials & references

        """
    )
    body += source_block + "\n\n---\n\n"

    body += dedent(
        """\
        ## 🧰 Generated study aids

        """
    )
    body += STUDY_AIDS_PLACEHOLDER + "\n---\n\n"

    body += dedent(
        f"""\
        ## 🔗 Cross-links

        - Syllabus & curriculum mindmap: [[Subject_Plan]]
        - Master Learning index: [[00 - 09 - Learning Index]]
        - Master practice guide: [[{howto_link.replace('.md','')}]]
        - Practice GUI app vision: [[../00 - Dev_Tools/PRACTICE_GUI_APP_VISION]]
        """
    )
    return body


def main() -> int:
    subjects = find_subject_folders()
    written: list[Path] = []
    for subject in subjects:
        readme = subject / "README.md"
        readme.write_text(render_readme(subject), encoding="utf-8")
        written.append(readme)

    print(f"Wrote {len(written)} README.md files:\n")
    for p in written:
        rel = p.relative_to(ROOT)
        print(f"  - {rel}  ({p.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
