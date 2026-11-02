/**
 * A tiny, safe arithmetic evaluator (no `eval`). Supports +, -, *, /, unary
 * minus, and parentheses over decimal numbers. Rejects anything else. Used by
 * the "explore with a calculator" workflow to keep model-derived expressions
 * from ever reaching a real evaluator or the shell.
 */

type Token = { type: "num"; value: number } | { type: "op"; value: string } | { type: "paren"; value: "(" | ")" };

const PRECEDENCE: Record<string, number> = { "+": 1, "-": 1, "*": 2, "/": 2 };

export class CalculatorError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "CalculatorError";
  }
}

function tokenize(expression: string): Token[] {
  const tokens: Token[] = [];
  let i = 0;
  while (i < expression.length) {
    const ch = expression[i]!;
    if (/\s/.test(ch)) {
      i += 1;
      continue;
    }
    if (/[0-9.]/.test(ch)) {
      let num = "";
      while (i < expression.length && /[0-9.]/.test(expression[i]!)) {
        num += expression[i];
        i += 1;
      }
      const value = Number(num);
      if (!Number.isFinite(value)) {
        throw new CalculatorError(`Invalid number: ${num}`);
      }
      tokens.push({ type: "num", value });
      continue;
    }
    if (ch === "+" || ch === "-" || ch === "*" || ch === "/") {
      tokens.push({ type: "op", value: ch });
      i += 1;
      continue;
    }
    if (ch === "(" || ch === ")") {
      tokens.push({ type: "paren", value: ch });
      i += 1;
      continue;
    }
    throw new CalculatorError(`Unexpected character: ${ch}`);
  }
  return tokens;
}

/** Evaluate via shunting-yard to RPN then fold. */
export function safeEvaluate(expression: string): number {
  const tokens = tokenize(expression);
  const output: Token[] = [];
  const ops: Token[] = [];
  let prev: Token | undefined;

  for (const token of tokens) {
    if (token.type === "num") {
      output.push(token);
    } else if (token.type === "op") {
      // Unary minus/plus: treat as (0 - x).
      const isUnary = !prev || (prev.type === "op") || (prev.type === "paren" && prev.value === "(");
      if (isUnary && (token.value === "-" || token.value === "+")) {
        output.push({ type: "num", value: 0 });
      }
      while (
        ops.length > 0 &&
        ops[ops.length - 1]!.type === "op" &&
        PRECEDENCE[(ops[ops.length - 1] as { value: string }).value]! >= PRECEDENCE[token.value]!
      ) {
        output.push(ops.pop()!);
      }
      ops.push(token);
    } else if (token.value === "(") {
      ops.push(token);
    } else {
      while (ops.length > 0 && !(ops[ops.length - 1]!.type === "paren")) {
        output.push(ops.pop()!);
      }
      if (ops.length === 0) {
        throw new CalculatorError("Mismatched parentheses");
      }
      ops.pop();
    }
    prev = token;
  }
  while (ops.length > 0) {
    const op = ops.pop()!;
    if (op.type === "paren") {
      throw new CalculatorError("Mismatched parentheses");
    }
    output.push(op);
  }

  const stack: number[] = [];
  for (const token of output) {
    if (token.type === "num") {
      stack.push(token.value);
      continue;
    }
    const b = stack.pop();
    const a = stack.pop();
    if (a === undefined || b === undefined) {
      throw new CalculatorError("Malformed expression");
    }
    switch (token.value) {
      case "+":
        stack.push(a + b);
        break;
      case "-":
        stack.push(a - b);
        break;
      case "*":
        stack.push(a * b);
        break;
      case "/":
        if (b === 0) {
          throw new CalculatorError("Division by zero");
        }
        stack.push(a / b);
        break;
      default:
        throw new CalculatorError(`Unknown operator ${token.value}`);
    }
  }
  if (stack.length !== 1 || stack[0] === undefined) {
    throw new CalculatorError("Malformed expression");
  }
  return stack[0];
}
