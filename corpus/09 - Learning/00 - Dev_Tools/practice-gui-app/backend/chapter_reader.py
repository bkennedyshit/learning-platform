"""Dynamic curriculum discovery — walks the Learning tree to find all tracks/subjects/chapters."""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import frontmatter

CHAPTER_RE = re.compile(r"^(\d+\.\d+)\s*-\s*(.+)\.md$")
SCRIPT_RE = re.compile(r"^(\d+\.\d+)_.+\.py$")

MATH_TRACK = "07 - Math and Physics"
OTHER_TRACKS = [
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

# Custom slug overrides for tracks whose folder prefix collides with another folder.
# Where a folder is not in this dict, we fall back to the "track-NN" auto-pattern.
SLUG_OVERRIDES: dict[str, str] = {
    "01- Python": "python",
    "02 - C++": "cpp",
    "03 - C hash": "csharp",
    "04 - Game_Dev": "gamedev",
    "05 - AI_Experiments": "aiexp",
    "05 - JavaScript": "js",
    "06 - Game Design": "gamedesign",
    "06 - TypeScript": "ts",
    "07 - SQL": "sql",
    "14 - Rust": "rust",
    "15 - Biology": "bio",
    "16 - Chemistry": "chem",
}


@dataclass
class ChapterInfo:
    num: str
    title: str
    filename: str
    script_filename: str | None = None


@dataclass
class Subject:
    id: str
    track: str
    subject_name: str
    path: Path
    chapters: list[ChapterInfo] = field(default_factory=list)


_cache: list[Subject] | None = None


def _discover_chapters(subject_dir: Path) -> list[ChapterInfo]:
    """Glob chapter .md files and match them to practice scripts."""
    scripts_dir = subject_dir / "_practice" / "scripts"
    script_map: dict[str, str] = {}
    if scripts_dir.exists():
        for f in scripts_dir.iterdir():
            m = SCRIPT_RE.match(f.name)
            if m:
                script_map[m.group(1)] = f.name

    chapters: list[ChapterInfo] = []
    for f in sorted(subject_dir.iterdir()):
        m = CHAPTER_RE.match(f.name)
        if m:
            num, title = m.group(1), m.group(2)
            chapters.append(ChapterInfo(
                num=num,
                title=title,
                filename=f.name,
                script_filename=script_map.get(num),
            ))
    return chapters


def discover_subjects(learning_root: Path) -> list[Subject]:
    """Walk the curriculum tree and return all subjects."""
    subjects: list[Subject] = []

    # Math track — 12 sub-subjects
    math_dir = learning_root / MATH_TRACK
    if math_dir.exists():
        for child in sorted(math_dir.iterdir()):
            if child.is_dir() and (child / "Subject_Plan.md").exists():
                # Extract the two-digit number from folder name like "02 - Linear Algebra..."
                num_match = re.match(r"^(\d+)", child.name)
                if num_match:
                    num = num_match.group(1)
                    sid = f"math-{num}"
                    subjects.append(Subject(
                        id=sid,
                        track=MATH_TRACK,
                        subject_name=child.name,
                        path=child,
                        chapters=_discover_chapters(child),
                    ))

    # Other tracks — each is its own subject
    for track_name in OTHER_TRACKS:
        track_dir = learning_root / track_name
        if track_dir.exists() and (track_dir / "Subject_Plan.md").exists():
            if track_name in SLUG_OVERRIDES:
                sid = SLUG_OVERRIDES[track_name]
            else:
                num_match = re.match(r"^(\d+)", track_name)
                num = num_match.group(1) if num_match else track_name[:2]
                sid = f"track-{num}"
            subjects.append(Subject(
                id=sid,
                track=track_name,
                subject_name=track_name,
                path=track_dir,
                chapters=_discover_chapters(track_dir),
            ))

    return subjects


def get_subjects(learning_root: Path) -> list[Subject]:
    """Return cached subjects list, discovering on first call."""
    global _cache
    if _cache is None:
        _cache = discover_subjects(learning_root)
    return _cache


def refresh(learning_root: Path) -> list[Subject]:
    """Force re-discovery (for dev hot-reload)."""
    global _cache
    _cache = None
    return get_subjects(learning_root)


def get_subject_by_id(learning_root: Path, subject_id: str) -> Subject | None:
    """Lookup a single subject by its slug id."""
    for s in get_subjects(learning_root):
        if s.id == subject_id:
            return s
    return None


def read_chapter(subject: Subject, chapter_num: str) -> dict[str, Any] | None:
    """Read a chapter markdown file and return its content + frontmatter."""
    chapter = next((c for c in subject.chapters if c.num == chapter_num), None)
    if chapter is None:
        return None
    filepath = subject.path / chapter.filename
    if not filepath.exists():
        return None
    raw = filepath.read_text(encoding="utf-8")
    post = frontmatter.loads(raw)
    return {
        "num": chapter.num,
        "title": chapter.title,
        "markdown": raw,
        "frontmatter": dict(post.metadata),
    }
