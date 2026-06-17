#!/usr/bin/env python3
"""
10.1_optimization.py — Practice problem generator for Chapter 10.1
(Statistical Learning & Optimization).

Generates randomized drill problems across 6 archetypes:
  1. Compute gradient of a polynomial loss function
  2. One step of SGD on a quadratic
  3. Momentum update computation
  4. Adam update with bias correction
  5. Convergence rate calculation (iterations to epsilon)
  6. Softmax + cross-entropy gradient

Usage:
  python 10.1_optimization.py
  python 10.1_optimization.py --count 12 --seed 42
  python 10.1_optimization.py --count 12 --seed 42 --out /tmp/_101.md
  python 10.1_optimization.py --demo

Exit code 0 on success.
"""
from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from pathlib import Path

import numpy as np

try:
    import sympy as sp
    HAS_SYMPY = True
except ImportError:
    HAS_SYMPY = False


@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str

    def render(self, idx: int) -> str:
        return (
            f"### Problem {idx} — {self.archetype}\n\n"
            f"{self.statement_md}\n\n"
            "?\n\n"
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )


# ---------------------------------------------------------------------------
# Archetype 1: Compute gradient of polynomial loss
# ---------------------------------------------------------------------------
def gen_gradient(rng: random.Random) -> Problem:
    a = rng.randint(1, 5)
    b = rng.randint(1, 5)
    c = rng.randint(-3, 3)
    # f(x,y) = a*x^2 + b*y^2 + c*x*y
    stmt = (
        f"Compute the gradient $\\nabla f$ for $f(x,y) = {a}x^2 + {b}y^2 + {c}xy$. "
        f"Evaluate at $(x,y) = (2, -1)$."
    )
    # df/dx = 2a*x + c*y, df/dy = 2b*y + c*x
    gx = 2*a*2 + c*(-1)
    gy = 2*b*(-1) + c*2
    sol = (
        f"$\\frac{{\\partial f}}{{\\partial x}} = {2*a}x + {c}y$, "
        f"$\\frac{{\\partial f}}{{\\partial y}} = {2*b}y + {c}x$.\n\n"
        f"At $(2, -1)$: $\\nabla f = ({2*a}\\cdot2 + {c}\\cdot(-1),\\; {2*b}\\cdot(-1) + {c}\\cdot2) = ({gx}, {gy})$."
    )
    return Problem("Gradient computation", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 2: One step of SGD
# ---------------------------------------------------------------------------
def gen_sgd_step(rng: random.Random) -> Problem:
    x0 = rng.randint(-5, 5)
    y0 = rng.randint(-5, 5)
    lr = rng.choice([0.01, 0.05, 0.1])
    a, b = rng.randint(1, 4), rng.randint(1, 4)
    # f = a*x^2 + b*y^2
    gx = 2*a*x0
    gy = 2*b*y0
    x1 = x0 - lr*gx
    y1 = y0 - lr*gy
    stmt = (
        f"Perform one SGD step on $f(x,y) = {a}x^2 + {b}y^2$ "
        f"starting at $\\theta_0 = ({x0}, {y0})$ with learning rate $\\eta = {lr}$."
    )
    sol = (
        f"$\\nabla f = ({2*a}x, {2*b}y) = ({gx}, {gy})$ at $({x0},{y0})$.\n\n"
        f"$\\theta_1 = ({x0}, {y0}) - {lr}({gx}, {gy}) = ({x1:.4f}, {y1:.4f})$.\n\n"
        f"Loss decreased from $f(\\theta_0) = {a*x0**2 + b*y0**2}$ to "
        f"$f(\\theta_1) = {a*x1**2 + b*y1**2:.4f}$."
    )
    return Problem("SGD step", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 3: Momentum update
# ---------------------------------------------------------------------------
def gen_momentum(rng: random.Random) -> Problem:
    beta = rng.choice([0.9, 0.95, 0.99])
    v_prev = round(rng.uniform(-2, 2), 2)
    g = round(rng.uniform(-3, 3), 2)
    lr = 0.01
    v_new = beta * v_prev + g
    theta_update = -lr * v_new
    stmt = (
        f"Given momentum $\\beta = {beta}$, previous velocity $v_{{t-1}} = {v_prev}$, "
        f"current gradient $g_t = {g}$, and $\\eta = {lr}$. "
        "Compute the new velocity $v_t$ and the parameter update $\\Delta\\theta$."
    )
    sol = (
        f"$v_t = \\beta v_{{t-1}} + g_t = {beta} \\cdot {v_prev} + {g} = "
        f"{beta*v_prev:.4f} + {g} = {v_new:.4f}$.\n\n"
        f"$\\Delta\\theta = -\\eta v_t = -{lr} \\cdot {v_new:.4f} = {theta_update:.6f}$."
    )
    return Problem("Momentum update", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 4: Adam update with bias correction
# ---------------------------------------------------------------------------
def gen_adam_step(rng: random.Random) -> Problem:
    t = rng.randint(1, 5)
    g = round(rng.uniform(-4, 4), 2)
    beta1, beta2 = 0.9, 0.999
    lr, eps = 0.001, 1e-8
    # Assume m_{t-1}=0, v_{t-1}=0 for simplicity at t=1
    m = (1 - beta1) * g
    v = (1 - beta2) * g**2
    m_hat = m / (1 - beta1**t)
    v_hat = v / (1 - beta2**t)
    update = lr * m_hat / (np.sqrt(v_hat) + eps)
    stmt = (
        f"At step $t={t}$ of Adam with $g_t = {g}$, $m_{{t-1}}=0$, $v_{{t-1}}=0$, "
        f"$\\beta_1={beta1}$, $\\beta_2={beta2}$, $\\eta={lr}$. "
        "Compute $\\hat{{m}}_t$, $\\hat{{v}}_t$, and the parameter update."
    )
    sol = (
        f"$m_t = (1-{beta1}) \\cdot {g} = {m:.4f}$\n\n"
        f"$v_t = (1-{beta2}) \\cdot {g}^2 = {v:.6f}$\n\n"
        f"$\\hat{{m}}_t = {m:.4f} / (1 - {beta1}^{{{t}}}) = {m:.4f}/{1-beta1**t:.6f} = {m_hat:.6f}$\n\n"
        f"$\\hat{{v}}_t = {v:.6f} / (1 - {beta2}^{{{t}}}) = {v_hat:.6f}$\n\n"
        f"$\\Delta\\theta = -{lr} \\cdot {m_hat:.4f} / (\\sqrt{{{v_hat:.6f}}} + 10^{{-8}}) = {-update:.6f}$"
    )
    return Problem("Adam update", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 5: Convergence iterations
# ---------------------------------------------------------------------------
def gen_convergence(rng: random.Random) -> Problem:
    L = rng.choice([10, 50, 100, 500])
    mu = rng.choice([0.1, 0.5, 1, 2])
    if mu >= L:
        mu = 1
    kappa = L / mu
    eps = rng.choice([1e-4, 1e-6, 1e-8])
    T = int(np.ceil(kappa * np.log(1/eps)))
    stmt = (
        f"For a $\\mu={mu}$-strongly convex, $L={L}$-smooth function, "
        f"how many GD iterations (with $\\eta=1/L$) are needed to achieve "
        f"$f(x_T) - f(x^*) \\leq {eps} \\cdot [f(x_0) - f(x^*)]$?"
    )
    sol = (
        f"Condition number $\\kappa = L/\\mu = {L}/{mu} = {kappa:.1f}$.\n\n"
        f"From Theorem 23.1.2: $T \\geq \\kappa \\ln(1/\\epsilon) = {kappa:.1f} \\cdot \\ln({1/eps:.0e}) = "
        f"{kappa:.1f} \\cdot {np.log(1/eps):.2f} = {kappa*np.log(1/eps):.1f}$.\n\n"
        f"**Answer:** $T \\geq {T}$ iterations."
    )
    return Problem("Convergence rate", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 6: Softmax gradient
# ---------------------------------------------------------------------------
def gen_softmax_grad(rng: random.Random) -> Problem:
    K = 3
    logits = [round(rng.uniform(-2, 2), 1) for _ in range(K)]
    target_class = rng.randint(0, K-1)
    z = np.array(logits)
    exp_z = np.exp(z - z.max())
    softmax = exp_z / exp_z.sum()
    y = np.zeros(K)
    y[target_class] = 1.0
    grad = softmax - y
    stmt = (
        f"Given logits $z = ({logits[0]}, {logits[1]}, {logits[2]})$ and true class $c={target_class}$, "
        "compute the softmax probabilities and the gradient $\\partial\\mathcal{{L}}/\\partial z$ "
        "for cross-entropy loss."
    )
    sm_str = ", ".join(f"{s:.4f}" for s in softmax)
    gr_str = ", ".join(f"{g:.4f}" for g in grad)
    sol = (
        f"Softmax: $\\hat{{y}} = \\text{{softmax}}(z) = ({sm_str})$.\n\n"
        f"One-hot target: $y = ({', '.join(str(int(v)) for v in y)})$.\n\n"
        f"Gradient: $\\nabla_z\\mathcal{{L}} = \\hat{{y}} - y = ({gr_str})$."
    )
    return Problem("Softmax + CE gradient", stmt, sol)


# ---------------------------------------------------------------------------
# Demo mode: run optimizers on Rosenbrock
# ---------------------------------------------------------------------------
def run_demo():
    print("=" * 60)
    print("DEMO: Optimizer comparison on Rosenbrock f(x,y)=(1-x)²+100(y-x²)²")
    print("=" * 60)

    def rosenbrock_grad(theta):
        x, y = theta
        dx = -2*(1-x) - 400*x*(y - x**2)
        dy = 200*(y - x**2)
        return np.array([dx, dy])

    def rosenbrock(theta):
        x, y = theta
        return (1-x)**2 + 100*(y-x**2)**2

    theta0 = np.array([-1.0, 1.0])
    print(f"\nStarting point: {theta0}, f={rosenbrock(theta0):.2f}")

    # SGD
    theta = theta0.copy()
    for i in range(10000):
        theta -= 0.0001 * rosenbrock_grad(theta)
    print(f"SGD (10k steps, lr=1e-4):      θ=({theta[0]:.4f}, {theta[1]:.4f}), f={rosenbrock(theta):.6f}")

    # Momentum
    theta = theta0.copy()
    v = np.zeros(2)
    for i in range(10000):
        v = 0.9*v + rosenbrock_grad(theta)
        theta -= 0.0001 * v
    print(f"Momentum (10k, β=0.9):         θ=({theta[0]:.4f}, {theta[1]:.4f}), f={rosenbrock(theta):.6f}")

    # Adam
    theta = theta0.copy()
    m, v = np.zeros(2), np.zeros(2)
    for t in range(1, 10001):
        g = rosenbrock_grad(theta)
        m = 0.9*m + 0.1*g
        v = 0.999*v + 0.001*g**2
        mh = m/(1-0.9**t)
        vh = v/(1-0.999**t)
        theta -= 0.001 * mh/(np.sqrt(vh)+1e-8)
    print(f"Adam (10k, lr=1e-3):           θ=({theta[0]:.4f}, {theta[1]:.4f}), f={rosenbrock(theta):.6f}")
    print(f"\nOptimum: (1.0, 1.0), f=0.0")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
GENERATORS = [gen_gradient, gen_sgd_step, gen_momentum, gen_adam_step, gen_convergence, gen_softmax_grad]


def main():
    parser = argparse.ArgumentParser(description="10.1 Optimization practice problems")
    parser.add_argument("--count", type=int, default=12, help="Number of problems")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--out", type=str, default=None, help="Output markdown file")
    parser.add_argument("--demo", action="store_true", help="Run optimizer demo")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return

    rng = random.Random(args.seed)
    problems = []
    for i in range(args.count):
        gen = rng.choice(GENERATORS)
        problems.append(gen(rng))

    lines = [
        "---",
        "tags: [review/ai, optimization, sgd, adam, gradient-descent]",
        f"generated: true",
        "---",
        "",
        "# 10.1 Optimization — Practice Problems",
        "",
    ]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i))
        lines.append("")

    output = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Wrote {len(problems)} problems to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()
