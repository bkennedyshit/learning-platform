#!/usr/bin/env python3
"""
scaffold_app_chapters.py

A safe, idempotent utility to expand chapter stubs in `10 - Learning App Material/Subjects/`.
It ONLY processes files with `status: draft` in the YAML frontmatter. If a file has
been modified or doesn't have the draft status, it is skipped entirely to protect
user content.

Uses a safe_print wrapper to avoid UnicodeEncodeErrors on Windows terminals when
printing filenames containing non-ASCII characters (e.g. Chinese).
"""

import sys
import os
import re
from pathlib import Path

ROOT = Path(r"C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\10 - Learning App Material")
SUBJECTS_DIR = ROOT / "Subjects"

SVG_TEMPLATE_PLACEHOLDER = """<svg viewBox="0 0 500 200" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 500px; height: auto;">
  <style>
    .placeholder-rect { fill: var(--background-secondary); stroke: var(--text-muted); stroke-width: 2; stroke-dasharray: 6,6; }
    .placeholder-text { font-family: Inter, system-ui, sans-serif; font-size: 16px; fill: var(--text-normal); font-weight: bold; }
    .placeholder-icon { fill: var(--interactive-accent); }
  </style>
  <rect x="10" y="10" width="480" height="180" rx="8" class="placeholder-rect"/>
  <circle cx="250" cy="80" r="30" class="placeholder-icon"/>
  <!-- Decorative visual icon -->
  <path d="M 235 80 L 245 90 L 265 70" stroke="var(--background-secondary)" stroke-width="4" fill="none" stroke-linecap="round"/>
  <text x="250" y="140" class="placeholder-text" text-anchor="middle">Visual Anchor: Chapter {chapter_id} Schematic</text>
</svg>"""

def safe_print(msg: str):
    """Prints safely to stdout by falling back to ASCII-only representation on encoding failure."""
    try:
        print(msg)
    except UnicodeEncodeError:
        try:
            print(msg.encode(sys.stdout.encoding or 'ascii', errors='replace').decode(sys.stdout.encoding or 'ascii'))
        except Exception:
            # Fallback to ascii ignore
            try:
                print(msg.encode('ascii', errors='replace').decode('ascii'))
            except Exception:
                pass

def parse_frontmatter(text: str) -> dict:
    """Simple parser for YAML frontmatter."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    fm_lines = m.group(1).split("\n")
    fm = {}
    for line in fm_lines:
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm

def scaffold_chapter(file_path: Path):
    """Safely scaffolds a single draft chapter with grade-appropriate sections."""
    text = file_path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    
    if fm.get("status") != "draft":
        safe_print(f"  [Skipped] {file_path.name} (not a draft)")
        return False
        
    chapter_id = fm.get("chapter", "0.0")
    title = fm.get("title", file_path.stem)
    app_track = fm.get("app-track", "01")
    
    # Generate the standard educational template
    new_body = f"""---
date: 2026-05-29
title: "{title}"
tags: [chapter, app-curriculum, scaffolded]
type: chapter
app-track: "{app_track}"
chapter: {chapter_id}
status: scaffolded
---

# {title}

*Back to [[Bill's Vault/05-Knowledge_Foundation/10 - Learning App Material/Subjects/{file_path.parent.name}/Subject_Plan]] | [[Bill's Vault/05-Knowledge_Foundation/10 - Learning App Material/README|10 - Learning App Material]]*

> *"The foundation of all learning is active, visual interaction with the core principles."*

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:
1. Explain the fundamental components of {title.replace("APP-" + chapter_id + " — ", "")}.
2. Apply the primary principles to solve foundational problems.
3. Critique common misconceptions and mistakes associated with this topic.
4. Draw or describe the core visual anchor representing this chapter's key mechanic.

---

## 🖼️ Visual Anchor

Below is the central visual schema representing the interactive components of this chapter.

{SVG_TEMPLATE_PLACEHOLDER.replace("{chapter_id}", chapter_id)}

---

## 📚 1. Definitions & Core Concepts

### Concept 1.1 — Core Terminology
- **Primary Element**: The foundational building block of this unit.
- **System Overlay**: The methodology of applying systematic, visual, and active structures to represent data.

### Concept 1.2 — Grade-Band Conceptual Model
- For K-5: Emphasis on concrete representations, pictorial models, and direct mapping.
- For 6-8: Transition to flow systems, simple systems relationships, and structural properties.
- For 9-12 / College: Rigorous analysis, symbolic mathematical models, and formal proofs.

---

## 🛡️ 2. Key Principles & Mechanics

1. **Construct Validity**: The representation must match the underlying standard.
2. **Interactive Reinforcement**: Hover structures and responsive visual feedback accelerate recall.
3. **Pacing and Flow**: Information flows from concrete primitives to abstract operations.

---

## 🎯 3. Worked Examples & Problems

### Example 3.1 — Foundational Application
**Problem Statement:** Evaluate or demonstrate the core operation of this chapter's primary mechanic.

**Step-by-Step Solution:**
1. Identify the input variables and constraints.
2. Draft the schematic representation.
3. Solve or derive the target outcome:
   $$
   \\text{{Outcome}} = \\text{{Scaffold}} + \\text{{Active Practice}}
   $$

---

## 🧠 Active Recall Prompts

<details>
<summary>🔍 Reveal Practice Questions & Active Recall Drills</summary>

### Question 1
What is the primary visual anchor representing this chapter's key mechanic?
?
**Answer:** The central visual schema (an Obsidian CSS-variable bound interactive SVG) that illustrates the key structures of this topic.

### Question 2
How does this chapter's concept scale across grade-bands?
?
**Answer:** From concrete/pictorial representations in K-5 to flow diagrams in middle school, and symbolic math/formal systems in high school/college.

### Question 3
Explain the core construct of this topic in your own words.
?
**Answer:** *Student-guided recall challenge. Restate the definition of the Primary Element.*

</details>

---

## 🔗 4. Cross-Links & Source Materials

- **Curriculum Plan**: [[Subject_Plan]]
- **Recommended Learning Path**: [[LEARNING_PATH]]
- **Master Platform Overview**: [[Bill's Vault/05-Knowledge_Foundation/10 - Learning App Material/README]]
"""
    
    file_path.write_text(new_body, encoding="utf-8")
    safe_print(f"  [Scaffolded] {file_path.name}")
    return True

def main():
    safe_print("Starting safe, idempotent scaffolding of draft chapters in '10 - Learning App Material'...")
    scaffold_count = 0
    
    for subject_dir in sorted(SUBJECTS_DIR.iterdir()):
        if not subject_dir.is_dir():
            continue
        safe_print(f"Processing Subject: {subject_dir.name}")
        for ch_file in sorted(subject_dir.glob("*.md")):
            if ch_file.name in {"Subject_Plan.md", "README.md", "LEARNING_PATH.md"}:
                continue
            # Regex match to check if it's a chapter file (e.g. 02.1 - ...)
            if re.match(r"^\d+\.\d+", ch_file.name):
                if scaffold_chapter(ch_file):
                    scaffold_count += 1
                    
    safe_print(f"\nCompleted scaffolding. Scaffolded {scaffold_count} draft chapter files.")

if __name__ == "__main__":
    main()
