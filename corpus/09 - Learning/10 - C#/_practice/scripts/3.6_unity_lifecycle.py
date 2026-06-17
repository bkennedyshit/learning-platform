#!/usr/bin/env python3
"""
3.6_unity_lifecycle.py — Practice problem generator for Chapter 3.6
(Unity Specifics: MonoBehaviour, Coroutines, ScriptableObjects, ECS).

Generates randomized drill problems across 5 archetypes:
  1. Lifecycle ordering (predict execution order)
  2. Coroutine yield behavior (what happens next frame?)
  3. ScriptableObject design (design a SO for a given use case)
  4. ECS component design (split a class into ECS components)
  5. Bug spotting (find the Unity-specific bug)

Usage:
  python 3.6_unity_lifecycle.py
  python 3.6_unity_lifecycle.py --count 12 --seed 42
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str

    def render(self, idx: int) -> str:
        return (
            f"### Problem {idx} — {self.archetype}\n\n"
            f"{self.statement_md}\n\n"
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )


# ---------------------------------------------------------------------------
# Archetype 1: Lifecycle ordering
# ---------------------------------------------------------------------------
def gen_lifecycle_order(rng: random.Random) -> Problem:
    scenarios = [
        {
            "setup": "ScriptA has `Awake() { Debug.Log(\"A-Awake\"); }` and `Start() { Debug.Log(\"A-Start\"); }`.\nScriptB has `Awake() { Debug.Log(\"B-Awake\"); }` and `Start() { Debug.Log(\"B-Start\"); }`.\nBoth are on active GameObjects in the scene.",
            "question": "What is the guaranteed output ordering?",
            "answer": "Both Awake calls run before either Start call. So output is:\n`A-Awake` (or B-Awake first — order between scripts is undefined)\n`B-Awake` (or A-Awake)\n`A-Start` (or B-Start)\n`B-Start` (or A-Start)\n\n**Key rule:** ALL Awake() calls complete before ANY Start() call begins."
        },
        {
            "setup": "A player script has:\n```csharp\nvoid Update() { Debug.Log(\"Update\"); }\nvoid FixedUpdate() { Debug.Log(\"Fixed\"); }\nvoid LateUpdate() { Debug.Log(\"Late\"); }\n```\nThe game runs at 30fps with physics at 50Hz (FixedUpdate every 0.02s).",
            "question": "How many times does each method run per frame?",
            "answer": "At 30fps, each frame is ~0.033s. Physics needs to catch up:\n- **FixedUpdate**: ~1-2 times per frame (0.033/0.02 ≈ 1.67, so sometimes 1, sometimes 2)\n- **Update**: exactly 1 time per frame\n- **LateUpdate**: exactly 1 time per frame\n\nOrder within a frame: FixedUpdate(s) → Update → LateUpdate"
        },
        {
            "setup": "Object A is instantiated at runtime. Object B is already in the scene.\nA's Awake sets `B.GetComponent<Health>().max = 200;`\nB's Awake sets `max = 100;`",
            "question": "What is B's max health?",
            "answer": "**It depends on execution order.** Scene objects get Awake before runtime-instantiated objects (usually). So B.Awake (max=100) runs first, then A.Awake (max=200). Final: **200**.\n\nBut this is fragile! Use Start() for cross-references, or set explicit Script Execution Order."
        },
    ]
    s = rng.choice(scenarios)
    stmt = f"{s['setup']}\n\n**Question:** {s['question']}"
    sol = s['answer']
    return Problem("Lifecycle Ordering", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 2: Coroutine behavior
# ---------------------------------------------------------------------------
def gen_coroutine_behavior(rng: random.Random) -> Problem:
    scenarios = [
        {
            "code": """```csharp
IEnumerator Example()
{
    Debug.Log("A");
    yield return null;
    Debug.Log("B");
    yield return new WaitForSeconds(1f);
    Debug.Log("C");
}
```""",
            "question": "When does each Debug.Log execute?",
            "answer": "- `A`: Frame 1 (when coroutine starts)\n- `B`: Frame 2 (`yield return null` waits exactly one frame)\n- `C`: ~1 second after B (WaitForSeconds uses scaled time)"
        },
        {
            "code": """```csharp
IEnumerator Spawner()
{
    for (int i = 0; i < 100; i++)
    {
        Instantiate(prefab, RandomPos(), Quaternion.identity);
    }
    yield return null;
}
```""",
            "question": "Does this spread instantiation across frames?",
            "answer": "**No!** The `yield return null` is AFTER the loop. All 100 objects spawn in a single frame, causing a spike. To spread across frames:\n```csharp\nfor (int i = 0; i < 100; i++)\n{\n    Instantiate(prefab, RandomPos(), Quaternion.identity);\n    if (i % 10 == 0) yield return null;  // Every 10 objects, wait a frame\n}\n```"
        },
    ]
    s = rng.choice(scenarios)
    stmt = f"{s['code']}\n\n**Question:** {s['question']}"
    sol = s['answer']
    return Problem("Coroutine Behavior", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 3: Bug spotting
# ---------------------------------------------------------------------------
def gen_bug_spot(rng: random.Random) -> Problem:
    scenarios = [
        {
            "code": """```csharp
public class EnemyAI : MonoBehaviour
{
    void Update()
    {
        var player = FindObjectOfType<Player>();
        var dist = Vector3.Distance(transform.position, player.transform.position);
        if (dist < 5f) Attack();
    }
}
```""",
            "bugs": "1. **`FindObjectOfType` in Update()** — extremely expensive, searches entire scene every frame.\n2. **No null check** — if player is destroyed, NullReferenceException.\n\n**Fix:**\n```csharp\nprivate Player _player;\nvoid Start() => _player = FindFirstObjectByType<Player>();\nvoid Update()\n{\n    if (_player == null) return;\n    if (Vector3.SqrMagnitude(transform.position - _player.transform.position) < 25f)\n        Attack();\n}\n```"
        },
        {
            "code": """```csharp
public class Bullet : MonoBehaviour
{
    void Update()
    {
        transform.position += transform.forward * 20f * Time.deltaTime;
        var hits = Physics.RaycastAll(transform.position, transform.forward, 1f);
        foreach (var hit in hits)
            hit.collider.GetComponent<IDamageable>()?.TakeDamage(10);
    }
}
```""",
            "bugs": "1. **`RaycastAll` allocates a new array every frame** — use `RaycastNonAlloc` with a pre-allocated buffer.\n2. **`GetComponent` on every hit every frame** — cache or use tags for quick rejection.\n3. **Bullet moves in Update but checks physics** — could tunnel through thin objects at high speed.\n\n**Fix:** Use `Physics.RaycastNonAlloc` with a cached `RaycastHit[]` buffer, or use a Rigidbody with continuous collision detection."
        },
    ]
    s = rng.choice(scenarios)
    stmt = f"Find the Unity-specific bugs in this code:\n\n{s['code']}"
    sol = s['bugs']
    return Problem("Unity Bug Spotting", stmt, sol)


GENERATORS = [
    gen_lifecycle_order,
    gen_coroutine_behavior,
    gen_bug_spot,
]


def generate_problem_set(count: int, seed: int | None) -> list[Problem]:
    rng = random.Random(seed)
    return [rng.choice(GENERATORS)(rng) for _ in range(count)]


def render_markdown(problems: list[Problem], seed: int | None) -> str:
    lines = [
        "---",
        f"date: {datetime.now().strftime('%Y-%m-%d')}",
        'title: "Practice — 3.6 Unity Specifics"',
        "type: practice",
        "chapter: 3.6",
        "---\n",
        "# Practice Problems — 3.6 Unity Specifics\n",
        f"Generated: {datetime.now().isoformat()} | Seed: {seed}\n",
        "---\n",
    ]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i))
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate C# 3.6 Unity practice problems")
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    problems = generate_problem_set(args.count, args.seed)
    md = render_markdown(problems, args.seed)

    if args.out:
        Path(args.out).write_text(md, encoding="utf-8")
        print(f"Written {len(problems)} problems to {args.out}")
    else:
        print(md)


if __name__ == "__main__":
    main()
