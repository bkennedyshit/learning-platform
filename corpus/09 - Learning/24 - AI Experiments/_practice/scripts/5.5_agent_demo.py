#!/usr/bin/env python3
"""
5.5_agent_demo.py — Minimal ReAct agent experiment.

Builds a ReAct agent with tools and evaluates task completion.

Usage:
  python 5.5_agent_demo.py --demo
  python 5.5_agent_demo.py --config agent_config.yaml
  python 5.5_agent_demo.py --demo --out ./reports/agent_report.md

Runs on CPU (LLM via API). GPU optional for local model serving.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable


@dataclass
class Tool:
    name: str
    description: str
    func: Callable


@dataclass
class AgentRun:
    query: str
    steps: list[dict]
    final_answer: str
    correct: bool
    latency_s: float
    total_steps: int


class ReActAgent:
    """Minimal ReAct agent for demonstration."""

    def __init__(self, tools: list[Tool], max_steps: int = 8):
        self.tools = {t.name: t for t in tools}
        self.max_steps = max_steps

    def _system_prompt(self) -> str:
        tool_desc = "\n".join(f"  - {t.name}: {t.description}" for t in self.tools.values())
        return f"""You are a helpful assistant. You can use these tools:
{tool_desc}

Format:
Thought: <reasoning>
Action: <tool_name>(<argument>)

When done:
Thought: I have the answer.
Action: final_answer(<answer>)"""

    def run(self, query: str, llm_fn: Callable) -> AgentRun:
        """Execute agent loop."""
        steps = []
        messages = [
            {"role": "system", "content": self._system_prompt()},
            {"role": "user", "content": query},
        ]

        start = time.perf_counter()
        final_answer = ""

        for i in range(self.max_steps):
            response = llm_fn(messages)
            messages.append({"role": "assistant", "content": response})

            action_match = re.search(r"Action:\s*(\w+)\((.+?)\)", response, re.DOTALL)
            if not action_match:
                steps.append({"step": i, "type": "no_action", "content": response[:100]})
                continue

            tool_name = action_match.group(1)
            arg = action_match.group(2).strip("\"' ")

            if tool_name == "final_answer":
                final_answer = arg
                steps.append({"step": i, "type": "final", "answer": arg})
                break

            if tool_name in self.tools:
                try:
                    result = str(self.tools[tool_name].func(arg))
                except Exception as e:
                    result = f"Error: {e}"
            else:
                result = f"Unknown tool: {tool_name}"

            steps.append({"step": i, "type": "tool_call", "tool": tool_name, "arg": arg, "result": result})
            messages.append({"role": "user", "content": f"Observation: {result}"})

        elapsed = time.perf_counter() - start
        return AgentRun(
            query=query, steps=steps, final_answer=final_answer,
            correct=False, latency_s=round(elapsed, 2), total_steps=len(steps),
        )


def mock_llm(messages: list[dict]) -> str:
    """Mock LLM for demo (deterministic responses)."""
    last_msg = messages[-1]["content"]

    if "calculator" not in str(messages) or "Observation" not in last_msg:
        # First turn: reason and call tool
        if "square root" in messages[1]["content"].lower():
            return "Thought: I need to calculate the square root.\nAction: calculator(math.sqrt(144))"
        if "capital" in messages[1]["content"].lower():
            return "Thought: I need to look this up.\nAction: search(capital of France)"
        return "Thought: Let me calculate.\nAction: calculator(2+2)"

    # After observation: give final answer
    obs = last_msg.replace("Observation: ", "")
    return f"Thought: I have the answer.\nAction: final_answer({obs})"


def run_demo() -> list[AgentRun]:
    """Run demo agent evaluation."""
    tools = [
        Tool("calculator", "Evaluate math expressions", lambda expr: eval(expr, {"__builtins__": {}}, {"math": math})),
        Tool("search", "Search for information", lambda q: {"capital of France": "Paris", "capital of Japan": "Tokyo"}.get(q, "Not found")),
    ]

    agent = ReActAgent(tools, max_steps=5)

    test_cases = [
        {"query": "What is the square root of 144?", "expected": "12"},
        {"query": "What is the capital of France?", "expected": "Paris"},
        {"query": "Calculate 2+2", "expected": "4"},
    ]

    results = []
    for tc in test_cases:
        run = agent.run(tc["query"], mock_llm)
        run.correct = tc["expected"].lower() in run.final_answer.lower()
        results.append(run)
        status = "✓" if run.correct else "✗"
        print(f"  {status} '{tc['query']}' → '{run.final_answer}' (expected: {tc['expected']})")

    return results


def render_report(results: list[AgentRun]) -> str:
    """Render agent evaluation as markdown."""
    correct = sum(1 for r in results if r.correct)
    lines = [
        "---",
        "tags: [ai-experiments, agents, react, practice]",
        "chapter: 5.5",
        "type: agent-report",
        f"generated: {datetime.now().isoformat(timespec='seconds')}",
        "---\n",
        "# Agent Evaluation Report\n",
        f"> Generated by `5.5_agent_demo.py` on {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
        "## Summary\n",
        f"- Tasks: {len(results)}",
        f"- Correct: {correct}/{len(results)} ({100*correct/len(results):.0f}%)",
        f"- Avg steps: {sum(r.total_steps for r in results)/len(results):.1f}",
        f"- Avg latency: {sum(r.latency_s for r in results)/len(results):.2f}s\n",
        "## Results\n",
        "| Query | Answer | Correct | Steps | Latency |",
        "|-------|--------|---------|-------|---------|",
    ]

    for r in results:
        status = "✅" if r.correct else "❌"
        lines.append(f"| {r.query} | {r.final_answer} | {status} | {r.total_steps} | {r.latency_s}s |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="ReAct agent experiment")
    parser.add_argument("--demo", action="store_true", help="Run demo with mock LLM")
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    if args.demo:
        print("Running agent demo...")
        results = run_demo()
    else:
        print("Use --demo for quick validation.")
        return

    out_path = args.out or Path(__file__).parent.parent / "5.5_agent_report.md"
    report = render_report(results)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    print(f"\nReport saved: {out_path}")


if __name__ == "__main__":
    main()
