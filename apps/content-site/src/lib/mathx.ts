// Safe math expression evaluator (no eval/Function). Supports:
//   numbers, variable x, + - * / ^, unary minus, parentheses,
//   functions: sin cos tan asin acos atan sinh cosh tanh exp ln log sqrt abs sign,
//   constants: pi, e
// Compile once, evaluate many times for different x.

type Token = { t: "num" | "op" | "lp" | "rp" | "fn" | "var"; v: string };

const FUNCS: Record<string, (a: number) => number> = {
  sin: Math.sin, cos: Math.cos, tan: Math.tan,
  asin: Math.asin, acos: Math.acos, atan: Math.atan,
  sinh: Math.sinh, cosh: Math.cosh, tanh: Math.tanh,
  exp: Math.exp, ln: Math.log, log: Math.log10, sqrt: Math.sqrt,
  abs: Math.abs, sign: Math.sign,
};
const PREC: Record<string, number> = { "+": 2, "-": 2, "*": 3, "/": 3, "^": 4 };
const RIGHT = new Set(["^"]);

function tokenize(src: string): Token[] {
  const s = src.replace(/\s+/g, "");
  const out: Token[] = [];
  let i = 0;
  while (i < s.length) {
    const c = s[i];
    if (/[0-9.]/.test(c)) {
      let j = i + 1;
      while (j < s.length && /[0-9.]/.test(s[j])) j++;
      out.push({ t: "num", v: s.slice(i, j) });
      i = j;
    } else if (/[a-zA-Z]/.test(c)) {
      let j = i + 1;
      while (j < s.length && /[a-zA-Z0-9]/.test(s[j])) j++;
      const name = s.slice(i, j);
      if (name in FUNCS) out.push({ t: "fn", v: name });
      else if (name === "pi") out.push({ t: "num", v: String(Math.PI) });
      else if (name === "e") out.push({ t: "num", v: String(Math.E) });
      else if (name === "x") out.push({ t: "var", v: "x" });
      else throw new Error(`Unknown name: ${name}`);
      i = j;
    } else if ("+-*/^".includes(c)) {
      out.push({ t: "op", v: c });
      i++;
    } else if (c === "(") { out.push({ t: "lp", v: c }); i++; }
    else if (c === ")") { out.push({ t: "rp", v: c }); i++; }
    else throw new Error(`Unexpected character: ${c}`);
  }
  return out;
}

// Shunting-yard -> RPN, with unary-minus handling.
function toRPN(tokens: Token[]): Token[] {
  const out: Token[] = [];
  const stack: Token[] = [];
  let prev: Token | null = null;
  for (const tok of tokens) {
    if (tok.t === "num" || tok.t === "var") {
      out.push(tok);
    } else if (tok.t === "fn") {
      stack.push(tok);
    } else if (tok.t === "op") {
      // unary minus: '-' at start or after op/lp -> 'u'
      if (tok.v === "-" && (prev === null || prev.t === "op" || prev.t === "lp")) {
        stack.push({ t: "op", v: "u" });
      } else {
        while (
          stack.length &&
          stack[stack.length - 1].t === "op" &&
          (stack[stack.length - 1].v === "u" ||
            (RIGHT.has(tok.v)
              ? PREC[stack[stack.length - 1].v] > PREC[tok.v]
              : PREC[stack[stack.length - 1].v] >= PREC[tok.v]))
        ) {
          out.push(stack.pop()!);
        }
        stack.push(tok);
      }
    } else if (tok.t === "lp") {
      stack.push(tok);
    } else if (tok.t === "rp") {
      while (stack.length && stack[stack.length - 1].t !== "lp") out.push(stack.pop()!);
      if (!stack.length) throw new Error("Mismatched parentheses");
      stack.pop(); // remove lp
      if (stack.length && stack[stack.length - 1].t === "fn") out.push(stack.pop()!);
    }
    prev = tok;
  }
  while (stack.length) {
    const s = stack.pop()!;
    if (s.t === "lp") throw new Error("Mismatched parentheses");
    out.push(s);
  }
  return out;
}

export interface CompiledFn {
  eval: (x: number) => number;
}

export function compile(expr: string): CompiledFn {
  const rpn = toRPN(tokenize(expr));
  return {
    eval(x: number): number {
      const st: number[] = [];
      for (const tok of rpn) {
        if (tok.t === "num") st.push(parseFloat(tok.v));
        else if (tok.t === "var") st.push(x);
        else if (tok.t === "fn") st.push(FUNCS[tok.v](st.pop()!));
        else if (tok.t === "op") {
          if (tok.v === "u") { st.push(-st.pop()!); continue; }
          const b = st.pop()!;
          const a = st.pop()!;
          switch (tok.v) {
            case "+": st.push(a + b); break;
            case "-": st.push(a - b); break;
            case "*": st.push(a * b); break;
            case "/": st.push(a / b); break;
            case "^": st.push(Math.pow(a, b)); break;
          }
        }
      }
      return st.pop()!;
    },
  };
}

// Central-difference numerical derivative.
export function numDeriv(f: (x: number) => number, x: number, h = 1e-5): number {
  return (f(x + h) - f(x - h)) / (2 * h);
}
