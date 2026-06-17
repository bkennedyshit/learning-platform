from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from sympy import Eq, Rational, Symbol, expand, simplify, solve

Tier = Literal["easy", "medium", "hard", "exam"]


@dataclass(frozen=True)
class GeneratedProblem:
    subject: str
    tier: Tier
    problem: str
    solution: str


Generator = Callable[[Tier], GeneratedProblem]


def generate_problem(subject: str, tier: Tier) -> GeneratedProblem:
    normalized_subject = subject.strip().lower()
    generator = GENERATORS.get(normalized_subject)

    if generator is None:
        supported = ", ".join(sorted(GENERATORS))
        raise UnsupportedSubjectError(
            f"Unsupported subject '{subject}'. Supported subjects: {supported}."
        )

    return generator(tier)


class UnsupportedSubjectError(ValueError):
    pass


def supported_subjects() -> list[str]:
    return sorted(GENERATORS)


def generate_arithmetic(tier: Tier) -> GeneratedProblem:
    if tier == "easy":
        left = 18
        right = 27
        result = left + right
        return GeneratedProblem(
            subject="arithmetic",
            tier=tier,
            problem=f"Compute: {left} + {right}",
            solution=str(result),
        )

    if tier == "medium":
        left = 14
        right = 6
        offset = 19
        result = left * right - offset
        return GeneratedProblem(
            subject="arithmetic",
            tier=tier,
            problem=f"Compute: {left} * {right} - {offset}",
            solution=str(result),
        )

    if tier == "hard":
        result = simplify(Rational(3, 4) + Rational(5, 6))
        return GeneratedProblem(
            subject="arithmetic",
            tier=tier,
            problem="Compute: 3/4 + 5/6",
            solution=str(result),
        )

    result = simplify(Rational(7, 8) * Rational(2, 3) + Rational(5, 12))
    return GeneratedProblem(
        subject="arithmetic",
        tier=tier,
        problem="Compute: (7/8) * (2/3) + 5/12",
        solution=str(result),
    )


def generate_algebra(tier: Tier) -> GeneratedProblem:
    x = Symbol("x")

    if tier == "easy":
        equation = Eq(2 * x + 3, 11)
        solution = solve(equation, x)[0]
        return GeneratedProblem(
            subject="algebra",
            tier=tier,
            problem=f"Solve for x: {_format_equation(equation)}",
            solution=f"x = {solution}",
        )

    if tier == "medium":
        equation = Eq(3 * (x - 4) + 2, 20)
        solution = solve(equation, x)[0]
        return GeneratedProblem(
            subject="algebra",
            tier=tier,
            problem=f"Solve for x: {_format_equation(equation)}",
            solution=f"x = {solution}",
        )

    if tier == "hard":
        expression = expand((x - 3) * (x + 5))
        roots = solve(Eq(expression, 0), x)
        solution = ", ".join(f"x = {root}" for root in roots)
        return GeneratedProblem(
            subject="algebra",
            tier=tier,
            problem=f"Solve for x: {_format_equation(Eq(expression, 0))}",
            solution=solution,
        )

    y = 2 * x + 1
    expression = simplify(Rational(1, 2) * y + 3)
    equation = Eq(expression, 10)
    solution = solve(equation, x)[0]
    return GeneratedProblem(
        subject="algebra",
        tier=tier,
        problem=f"If y = 2*x + 1, solve for x: {_format_equation(equation)}",
        solution=f"x = {solution}",
    )


def _format_equation(equation: Eq) -> str:
    return f"{equation.lhs} = {equation.rhs}"


GENERATORS: dict[str, Generator] = {
    "algebra": generate_algebra,
    "arithmetic": generate_arithmetic,
}
