export type SurfaceEvaluator = (x: number, y: number) => number;

const supportedExpressions: Record<string, SurfaceEvaluator> = {
  "sin(x) * cos(y)": (x, y) => Math.sin(x) * Math.cos(y),
  "x^2 - y^2": (x, y) => x * x - y * y,
  "sin(r) / r": (x, y) => {
    const r = Math.hypot(x, y);
    return r === 0 ? 1 : Math.sin(r) / r;
  },
  "cos(x*y)": (x, y) => Math.cos(x * y),
};

const fallbackExpression: SurfaceEvaluator = supportedExpressions["sin(x) * cos(y)"] as SurfaceEvaluator;

export function createSurfaceEvaluator(expression: string): SurfaceEvaluator {
  const normalized = normalizeExpression(expression);
  return supportedExpressions[normalized] ?? fallbackExpression;
}

export function getSupportedExpressions(): string[] {
  return Object.keys(supportedExpressions);
}

function normalizeExpression(expression: string): string {
  return expression.trim().replace(/\s+/g, " ");
}
