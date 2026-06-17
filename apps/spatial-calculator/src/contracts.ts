export type SpatialExpressionKind = "surface" | "curve";

export type LoadExpressionMessage = {
  source: "learning-platform";
  type: "spatial-calculator.loadExpression";
  payload: {
    id?: string;
    title?: string;
    expression: string;
    kind?: SpatialExpressionKind;
    domain?: {
      min: number;
      max: number;
      steps?: number;
    };
  };
};

export type ReadyMessage = {
  source: "spatial-calculator";
  type: "spatial-calculator.ready";
};

export type SpatialCalculatorMessage = LoadExpressionMessage;

export function isLoadExpressionMessage(
  value: unknown,
): value is LoadExpressionMessage {
  if (!value || typeof value !== "object") {
    return false;
  }

  const message = value as Partial<LoadExpressionMessage>;
  const payload = message.payload as Partial<LoadExpressionMessage["payload"]> | undefined;

  return (
    message.source === "learning-platform" &&
    message.type === "spatial-calculator.loadExpression" &&
    !!payload &&
    typeof payload.expression === "string" &&
    payload.expression.trim().length > 0
  );
}
