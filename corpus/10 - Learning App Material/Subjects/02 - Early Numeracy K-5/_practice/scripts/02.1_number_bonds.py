#!/usr/bin/env python3
"""
02.1_number_bonds.py

An interactive, visual-first terminal practice script for K-1 learners to master
Number Bonds and Ten-Frame Subitizing.
Generates an Obsidian-ready practice sheet `_practice/02.1_drills.md` containing the drills.
"""

import argparse
import random
import os
import sys
from datetime import datetime

from pathlib import Path

def draw_ascii_ten_frame(dots: int) -> str:
    """Returns a highly legible, text-based 2x5 grid representing a Ten-Frame."""
    row1 = ["*"] * min(5, dots) + ["."] * (5 - min(5, dots))
    row2 = ["*"] * max(0, min(5, dots - 5)) + ["."] * (5 - max(0, min(5, dots - 5)))
    frame = f"  [ {' '.join(row1)} ]\n  [ {' '.join(row2)} ]"
    return frame

def generate_drill_card(mode: str, seed: int) -> tuple[str, str, str]:
    """Generates a question, answer, and visual representation based on the mode."""
    random.seed(seed)
    if mode == "bond-10":
        whole = 10
        part1 = random.randint(1, 9)
        part2 = whole - part1
        frame = draw_ascii_ten_frame(part1)
        question = f"We have {part1} dots in our Ten-Frame.\n{frame}\nHow many MORE dots do we need to make a WHOLE of 10?"
        answer = str(part2)
        explanation = f"Ten-Frame check: {part1} dots present, {part2} empty cells. Since {part1} + {part2} = 10, the missing part is {part2}."
    elif mode == "bond-20":
        whole = 20
        part1 = random.randint(5, 15)
        part2 = whole - part1
        frame = draw_ascii_ten_frame(part1) if part1 <= 10 else draw_ascii_ten_frame(10) + "\n" + draw_ascii_ten_frame(part1 - 10)
        question = f"We have {part1} dots in our Ten-Frames.\n{frame}\nHow many MORE dots do we need to make a WHOLE of 20?"
        answer = str(part2)
        explanation = f"Since {part1} + {part2} = 20, the missing part is {part2}."
    else:  # double
        num = random.randint(1, 10)
        ans = num * 2
        question = f"What is DOUBLE {num}? (Or: {num} + {num} = ?)"
        answer = str(ans)
        explanation = f"Doubling means adding the number to itself: {num} + {num} = {ans}."
    return question, answer, explanation

def main():
    parser = argparse.ArgumentParser(description="Practice K-1 Number Bonds & Ten-Frames.")
    parser.add_argument("--count", type=int, default=8, help="Number of questions to generate")
    parser.add_argument("--mode", choices=["bond-10", "bond-20", "double", "mix"], default="bond-10", help="Practice mode")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive CLI mode")
    args = parser.parse_args()

    # Seed initialization
    seed = args.seed if args.seed is not None else random.randint(1000, 9999)
    random.seed(seed)

    modes = ["bond-10", "bond-20", "double"] if args.mode == "mix" else [args.mode]
    
    questions = []
    for i in range(args.count):
        q_mode = random.choice(modes)
        q, a, exp = generate_drill_card(q_mode, seed + i)
        questions.append((q, a, exp))

    # Absolute path to subject practice folder
    subject_dir = Path(__file__).resolve().parents[2]
    practice_dir = subject_dir / "_practice"
    practice_dir.mkdir(exist_ok=True)
    
    # Save the drills to a file in Obsidian flashcard format
    date_str = datetime.now().strftime("%Y-%m-%d")
    drill_file = practice_dir / f"{date_str}_Early_Numeracy_Drills.md"
    
    markdown_content = f"""# Early Numeracy Practice: {date_str}
---
#review/math/numeracy

## Chapter 02.1 — Number Bonds to 10 and 20 (Seed: {seed})

> Solve each problem. For Ten-Frame drills, count the asterisks (*) and find the number needed to fill the frames.
"""
    
    for idx, (q, a, exp) in enumerate(questions):
        markdown_content += f"""
### 📝 Question {idx + 1}
{q}

?

**Answer:**
`{a}`

**Explanation:**
{exp}
---
"""
    
    drill_file.write_text(markdown_content, encoding="utf-8")
    
    print(f"==================================================")
    print(f"K-1 Early Numeracy Practice (Mode: {args.mode.upper()})")
    print(f"==================================================")
    print(f"Generated {args.count} practice questions.")
    print(f"Saved to: {drill_file}")
    print(f"==================================================")

    if args.interactive:
        correct_count = 0
        print("\n--- Running Interactive CLI Mode ---")
        for idx, (q, a, exp) in enumerate(questions):
            print(f"\nQuestion {idx + 1}:")
            print(q)
            try:
                user_ans = input("Your answer: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nExiting practice.")
                sys.exit(0)
            
            if user_ans == a:
                print("Correct! Excellent job!")
                correct_count += 1
            else:
                print(f"Oops! The correct answer was: {a}")
                print(f"Explanation: {exp}")
        print(f"\nPractice complete! Your score: {correct_count}/{args.count}")

if __name__ == "__main__":
    main()
