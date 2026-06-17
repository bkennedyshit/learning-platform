#!/usr/bin/env python3
"""
6.0_design_exercises.py — Design exercise generator for Track 06 (Game Design Theory).

Generates randomized game design prompts across 8 archetypes matching the 8 chapters:
  1. MDA Decomposition (analyze a game through MDA)
  2. Core Loop Design (design a loop for a constraint)
  3. Balance Challenge (fix a broken system)
  4. Level Design (create a beat chart or spatial layout)
  5. Narrative Design (environmental storytelling or structure)
  6. Juice Design (add feedback layers to an action)
  7. Playtest Plan (design a hypothesis-driven test)
  8. Monetization Audit (evaluate ethical alignment)

Usage:
  python 6.0_design_exercises.py
  python 6.0_design_exercises.py --count 8 --seed 42
  python 6.0_design_exercises.py --count 8 --seed 42 --out /tmp/_gd_exercises.md

Exit code 0 on success.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class DesignPrompt:
    archetype: str
    chapter: str
    prompt: str
    constraints: list[str]
    evaluation_criteria: list[str]

    def render(self, idx: int) -> str:
        constraints_md = "\n".join(f"- {c}" for c in self.constraints)
        criteria_md = "\n".join(f"- {c}" for c in self.evaluation_criteria)
        return (
            f"### Exercise {idx} — {self.archetype}\n"
            f"*Chapter: {self.chapter}*\n\n"
            f"**Prompt:** {self.prompt}\n\n"
            f"**Constraints:**\n{constraints_md}\n\n"
            f"**Evaluate your solution against:**\n{criteria_md}\n\n"
            "<details>\n<summary>Hints</summary>\n\n"
            f"Review [[{self.chapter}]] for frameworks. "
            "Write your solution on paper first, then compare to chapter examples.\n\n"
            "</details>\n"
        )


# --- Archetype generators ---

GENRES = ["roguelite", "farming sim", "BMX trick game", "VR puzzle game",
          "deckbuilder", "metroidvania", "rhythm game", "survival crafting",
          "racing game", "tower defense", "fighting game", "idle game"]

AESTHETICS = ["Challenge", "Discovery", "Expression", "Fellowship",
              "Fantasy", "Narrative", "Sensation", "Submission"]

MECHANICS = ["double jump", "time rewind", "grappling hook", "gravity flip",
             "teleportation", "wall running", "shape-shifting", "combo chains",
             "resource crafting", "stealth", "rhythm-based attacks", "deck building"]

PROBLEMS = ["players quit at the midpoint", "one strategy dominates all others",
            "new players can't learn the controls", "the game feels 'floaty'",
            "multiplayer matches are too one-sided", "progression feels meaningless",
            "players hoard resources and never spend them", "the tutorial is boring"]


def gen_mda(rng: random.Random) -> DesignPrompt:
    genre = rng.choice(GENRES)
    target = rng.sample(AESTHETICS, 2)
    return DesignPrompt(
        archetype="MDA Decomposition",
        chapter="6.1 - Player Psychology & Motivation - The MDA Framework",
        prompt=f"Design a {genre} that targets the aesthetics of **{target[0]}** and **{target[1]}**. "
               "Trace the full MDA chain: what mechanics produce what dynamics to create those feelings?",
        constraints=[
            "Maximum 5 core mechanics",
            "Each mechanic must connect to at least one target aesthetic",
            "Identify one mechanic that, if removed, breaks the aesthetic chain",
        ],
        evaluation_criteria=[
            "Is the MDA chain traceable? (Mechanic → Dynamic → Aesthetic)",
            "Are both target aesthetics served by the mechanics?",
            "Is the mechanic set minimal (no unnecessary additions)?",
            "Would a player actually FEEL the target aesthetics?",
        ],
    )


def gen_core_loop(rng: random.Random) -> DesignPrompt:
    genre = rng.choice(GENRES)
    mechanic = rng.choice(MECHANICS)
    return DesignPrompt(
        archetype="Core Loop Design",
        chapter="6.2 - Core Mechanics & Systems Design",
        prompt=f"Design a core loop for a {genre} whose central mechanic is **{mechanic}**. "
               "Define the Action → Feedback → Reward cycle. Then add one meta-loop.",
        constraints=[
            "The core loop must complete in under 60 seconds",
            "The core verb must feel good WITHOUT any progression system",
            "The meta-loop must use a different timescale (minutes vs. seconds)",
        ],
        evaluation_criteria=[
            "Is the core loop intrinsically fun (would you play it with no rewards)?",
            "Is feedback immediate and multi-channel (visual + audio minimum)?",
            "Does the meta-loop add direction without replacing core fun?",
            "Can you describe the experience in one sentence?",
        ],
    )


def gen_balance(rng: random.Random) -> DesignPrompt:
    problem = rng.choice(PROBLEMS)
    genre = rng.choice(GENRES)
    return DesignPrompt(
        archetype="Balance & Dynamics Fix",
        chapter="6.3 - Dynamics, Balance & Feedback Loops",
        prompt=f"Your {genre} has a problem: **{problem}**. "
               "Diagnose the feedback loop causing this and propose 2 solutions "
               "(one using positive feedback, one using negative feedback).",
        constraints=[
            "Solutions must not reduce depth or remove player agency",
            "At least one solution must be invisible to the player",
            "Explain WHY the problem occurs using feedback loop theory",
        ],
        evaluation_criteria=[
            "Is the root cause correctly identified (not just symptoms)?",
            "Do solutions address the cause, not just mask the symptom?",
            "Are solutions testable (how would you verify they work)?",
            "Do solutions preserve what's fun about the game?",
        ],
    )


def gen_level_design(rng: random.Random) -> DesignPrompt:
    mechanic = rng.choice(MECHANICS)
    context = rng.choice(["a tutorial level", "a mid-game challenge", "a final boss arena",
                          "a hub world", "a VR escape room", "a speedrun-friendly level"])
    return DesignPrompt(
        archetype="Level Design & Pacing",
        chapter="6.4 - Level Design & Spatial Pacing",
        prompt=f"Design {context} that teaches and tests **{mechanic}** using Nintendo's "
               "4-step method (introduce, develop, twist, conclude). Create a beat chart.",
        constraints=[
            "No text tutorials or UI prompts allowed",
            "Must include at least one rest beat",
            "The twist must combine the mechanic with a previously-learned skill",
            "Total duration: 3-5 minutes of gameplay",
        ],
        evaluation_criteria=[
            "Does the level teach without words?",
            "Is the pacing curve visible in the beat chart (tension/release)?",
            "Is the twist genuinely surprising while using established mechanics?",
            "Would a new player succeed on their first attempt (with effort)?",
        ],
    )


def gen_narrative(rng: random.Random) -> DesignPrompt:
    scenario = rng.choice([
        "a civilization that collapsed due to hubris",
        "two factions that were once allies but now war",
        "a scientist who made a terrible discovery",
        "a community that thrives despite harsh conditions",
        "a hero who failed and the world moved on without them",
    ])
    method = rng.choice(["environmental storytelling only (no text/dialogue)",
                         "emergent narrative systems",
                         "a hub-and-spoke structure with 4 self-contained stories"])
    return DesignPrompt(
        archetype="Narrative & Worldbuilding",
        chapter="6.5 - Narrative & Worldbuilding",
        prompt=f"Tell the story of **{scenario}** using **{method}**. "
               "Design the specific elements (objects, systems, or structure) that communicate this narrative.",
        constraints=[
            "No exposition dumps or narrator voice",
            "The player must be able to miss the story (it rewards attention, not force-feeds)",
            "The narrative must not conflict with gameplay (no ludonarrative dissonance)",
        ],
        evaluation_criteria=[
            "Can a player understand the core story from environmental cues alone?",
            "Does the narrative reward deeper investigation?",
            "Is there ludonarrative harmony (gameplay reinforces story)?",
            "Would players discuss/theorize about this story with others?",
        ],
    )


def gen_juice(rng: random.Random) -> DesignPrompt:
    action = rng.choice(["a sword slash", "a BMX trick landing", "picking up a collectible",
                         "opening a treasure chest", "a critical hit", "a perfect dodge",
                         "leveling up", "a combo finisher", "breaking through a wall"])
    return DesignPrompt(
        archetype="Juice & Game Feel",
        chapter="6.6 - Aesthetics, Juice & Game Feel",
        prompt=f"Design the complete juice stack for **{action}**. "
               "Specify all 5 layers: input response, animation, screen effects, audio, and particles.",
        constraints=[
            "Input response must occur within 1 frame (16ms)",
            "Audio must include at least 2 layered sounds",
            "Must include at least one element that varies each time (prevents repetition fatigue)",
            "Must be describable without seeing it (your words should evoke the feeling)",
        ],
        evaluation_criteria=[
            "Does the juice communicate the ACTION clearly (what happened)?",
            "Does the juice communicate the IMPORTANCE (how significant was it)?",
            "Is there variation to prevent sensory fatigue?",
            "Would this feel good on the 100th time, not just the 1st?",
        ],
    )


def gen_playtest(rng: random.Random) -> DesignPrompt:
    hypothesis = rng.choice([
        "players will understand the crafting system without a tutorial",
        "the boss fight feels fair despite high difficulty",
        "players prefer the new control scheme over the old one",
        "the level communicates its critical path through lighting alone",
        "the combo system creates interesting risk/reward decisions",
    ])
    return DesignPrompt(
        archetype="Playtest Design",
        chapter="6.7 - Playtesting & Iteration",
        prompt=f"Design a playtest to validate: **\"{hypothesis}\"**. "
               "Include hypothesis, method, success/failure criteria, and analysis plan.",
        constraints=[
            "Sample size: 5 players (realistic for indie dev)",
            "No helping players during the test",
            "Must include both quantitative metric AND qualitative observation",
            "Must define what 'failure' looks like BEFORE testing",
        ],
        evaluation_criteria=[
            "Is the hypothesis specific and falsifiable?",
            "Would the test actually reveal if the hypothesis is wrong?",
            "Are success/failure criteria concrete (numbers, not feelings)?",
            "Is the analysis plan actionable (what do you DO with the results)?",
        ],
    )


def gen_monetization(rng: random.Random) -> DesignPrompt:
    genre = rng.choice(GENRES)
    model = rng.choice(["free-to-play", "premium with DLC", "subscription-based"])
    return DesignPrompt(
        archetype="Monetization Design",
        chapter="6.8 - Monetization & Live Ops",
        prompt=f"Design a **{model}** monetization system for a {genre}. "
               "Ensure it passes both the Respect Test and the Autonomy Test.",
        constraints=[
            "No loot boxes or randomized purchases",
            "Free/base players must have the complete gameplay experience",
            "No artificial friction (energy systems, wait timers)",
            "Must be sustainable for a 5-person indie team",
        ],
        evaluation_criteria=[
            "Does spending feel GOOD (not obligatory)?",
            "Would a non-spending player recommend the game to friends?",
            "Is revenue sustainable without exploiting whales?",
            "Does the model align developer incentives with player happiness?",
        ],
    )


ARCHETYPES = [gen_mda, gen_core_loop, gen_balance, gen_level_design,
              gen_narrative, gen_juice, gen_playtest, gen_monetization]


def build_exercises(count: int, rng: random.Random) -> list[DesignPrompt]:
    exercises = []
    for i in range(count):
        gen = ARCHETYPES[i % len(ARCHETYPES)]
        exercises.append(gen(rng))
    return exercises


def render_markdown(exercises: list[DesignPrompt], seed: int) -> str:
    header = (
        "---\n"
        "tags: [game-design, practice, design-exercises, \"review/gamedesign\"]\n"
        "type: practice\n"
        f"generated: {datetime.now().isoformat(timespec='seconds')}\n"
        f"seed: {seed}\n"
        "---\n\n"
        "*Back to [[../Subject_Plan|Subject Plan]] | "
        "Part of [[../../09 - Learning Index|Learning Index]]*\n\n"
        "# Track 06 — Game Design: Practice Exercises\n\n"
        "> Auto-generated by `scripts/6.0_design_exercises.py`.\n\n"
        "**House rule:** Write your solution on paper or in a separate note before "
        "checking the chapter for comparison. Design is a muscle — train it.\n\n"
        "---\n\n"
    )
    body = "\n\n---\n\n".join(ex.render(i + 1) for i, ex in enumerate(exercises))
    return header + body + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n\n")[0])
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "6.0_design_drills.md")

    exercises = build_exercises(args.count, rng)
    md = render_markdown(exercises, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(exercises)} exercises (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()
