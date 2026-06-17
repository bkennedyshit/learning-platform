"""Practice GUI App — FastAPI backend (v1.2 multi-subject, central SVGs)."""

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .chapter_reader import get_subjects, get_subject_by_id, read_chapter, refresh
from .drill_runner import run_drill

LEARNING_ROOT = Path(
    os.environ.get(
        "LEARNING_ROOT",
        r"C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\09 - Learning",
    )
)
CENTRAL_SVGS = LEARNING_ROOT / "_svgs"

app = FastAPI(title="Practice GUI", version="1.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single static mount for all SVGs (filenames are prefixed with subject_id).
if CENTRAL_SVGS.exists():
    app.mount("/svgs", StaticFiles(directory=str(CENTRAL_SVGS)), name="svgs")


class DrillRequest(BaseModel):
    subject_id: str
    chapter_num: str
    count: int = 8
    seed: int | None = None


@app.get("/api/tracks")
def list_tracks():
    """Return the curriculum tree grouped by track."""
    subjects = get_subjects(LEARNING_ROOT)
    tracks: dict[str, list[dict]] = {}
    for s in subjects:
        tracks.setdefault(s.track, []).append({
            "id": s.id,
            "name": s.subject_name,
            "chapter_count": len(s.chapters),
        })
    return [{"track": track, "subjects": subs} for track, subs in tracks.items()]


@app.get("/api/subject/{subject_id}")
def get_subject(subject_id: str):
    """Return full subject metadata + chapter list."""
    subject = get_subject_by_id(LEARNING_ROOT, subject_id)
    if subject is None:
        raise HTTPException(status_code=404, detail=f"Subject {subject_id} not found")
    return {
        "id": subject.id,
        "track": subject.track,
        "name": subject.subject_name,
        "chapters": [
            {
                "num": c.num,
                "title": c.title,
                "filename": c.filename,
                "script_filename": c.script_filename,
            }
            for c in subject.chapters
        ],
    }


@app.get("/api/chapter/{subject_id}/{chapter_num}")
def get_chapter(subject_id: str, chapter_num: str):
    """Return chapter markdown content + frontmatter."""
    subject = get_subject_by_id(LEARNING_ROOT, subject_id)
    if subject is None:
        raise HTTPException(status_code=404, detail=f"Subject {subject_id} not found")
    result = read_chapter(subject, chapter_num)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Chapter {chapter_num} not found in {subject_id}")
    return result


@app.post("/api/drill")
def generate_drill(req: DrillRequest):
    """Generate drill problems for a specific chapter."""
    subject = get_subject_by_id(LEARNING_ROOT, req.subject_id)
    if subject is None:
        raise HTTPException(status_code=404, detail=f"Subject {req.subject_id} not found")
    chapter = next((c for c in subject.chapters if c.num == req.chapter_num), None)
    if chapter is None:
        raise HTTPException(status_code=404, detail=f"Chapter {req.chapter_num} not found")
    if chapter.script_filename is None:
        raise HTTPException(status_code=404, detail=f"No drill script for chapter {req.chapter_num}")
    script_path = subject.path / "_practice" / "scripts" / chapter.script_filename
    if not script_path.exists():
        raise HTTPException(status_code=404, detail=f"Script {chapter.script_filename} not found on disk")
    result = run_drill(script_path, req.count, req.seed)
    return {"subject_id": req.subject_id, "chapter_num": req.chapter_num, "seed": result["seed"], "markdown": result["markdown"]}


@app.post("/api/refresh")
def refresh_cache():
    """Force re-discovery of the curriculum tree (dev utility)."""
    subjects = refresh(LEARNING_ROOT)
    return {"subjects_count": len(subjects), "total_chapters": sum(len(s.chapters) for s in subjects)}
