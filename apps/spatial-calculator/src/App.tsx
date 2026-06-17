import { useEffect, useMemo, useRef, useState } from "react";
import { createSurfaceEvaluator, getSupportedExpressions } from "./expression";
import { isLoadExpressionMessage } from "./contracts";
import { createSpatialScene, type SpatialScene } from "./threeScene";
import "./styles.css";

type WebXrStatus = "checking" | "available" | "unavailable";

type ExpressionState = {
  title: string;
  expression: string;
  domain: number;
  steps: number;
};

const initialExpression: ExpressionState = {
  title: "Surface preview",
  expression: "sin(x) * cos(y)",
  domain: 3.2,
  steps: 48,
};

export function App() {
  const mountRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<SpatialScene | null>(null);
  const [expression, setExpression] = useState<ExpressionState>(initialExpression);
  const [xrStatus, setXrStatus] = useState<WebXrStatus>("checking");
  const options = useMemo(() => getSupportedExpressions(), []);

  useEffect(() => {
    const mount = mountRef.current;
    if (!mount) {
      return;
    }

    const spatialScene = createSpatialScene();
    sceneRef.current = spatialScene;
    mount.appendChild(spatialScene.element);

    if (window.parent && window.parent !== window) {
      window.parent.postMessage(
        {
          source: "spatial-calculator",
          type: "spatial-calculator.ready",
        },
        "*",
      );
    }

    return () => {
      spatialScene.dispose();
      sceneRef.current = null;
    };
  }, []);

  useEffect(() => {
    sceneRef.current?.setSurface(
      createSurfaceEvaluator(expression.expression),
      expression.domain,
      expression.steps,
    );
  }, [expression]);

  useEffect(() => {
    let cancelled = false;

    async function detectWebXr() {
      const xr = navigator.xr;
      if (!xr?.isSessionSupported) {
        setXrStatus("unavailable");
        return;
      }

      try {
        const immersiveVr = await xr.isSessionSupported("immersive-vr");
        if (!cancelled) {
          setXrStatus(immersiveVr ? "available" : "unavailable");
        }
      } catch {
        if (!cancelled) {
          setXrStatus("unavailable");
        }
      }
    }

    void detectWebXr();

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    function onMessage(event: MessageEvent<unknown>) {
      if (!isLoadExpressionMessage(event.data)) {
        return;
      }

      const { title, expression: nextExpression, domain } = event.data.payload;
      setExpression({
        title: title ?? "Loaded expression",
        expression: nextExpression,
        domain: domain?.max ?? initialExpression.domain,
        steps: domain?.steps ?? initialExpression.steps,
      });
    }

    window.addEventListener("message", onMessage);
    return () => window.removeEventListener("message", onMessage);
  }, []);

  return (
    <main className="calculatorShell">
      <section className="viewer" aria-label="3D expression visualization">
        <div ref={mountRef} className="viewerCanvas" />
        <div className="hud">
          <span>{expression.title}</span>
          <strong>{expression.expression}</strong>
        </div>
      </section>

      <aside className="panel" aria-label="Spatial calculator controls">
        <div>
          <h1>Spatial Calculator</h1>
          <p>3D browser visualization</p>
        </div>

        <label>
          Expression
          <select
            value={options.includes(expression.expression) ? expression.expression : ""}
            onChange={(event) =>
              setExpression((current) => ({
                ...current,
                title: "Surface preview",
                expression: event.target.value,
              }))
            }
          >
            {!options.includes(expression.expression) && (
              <option value="">{expression.expression}</option>
            )}
            {options.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </label>

        <label>
          Domain
          <input
            type="range"
            min="1"
            max="6"
            step="0.2"
            value={expression.domain}
            onChange={(event) =>
              setExpression((current) => ({
                ...current,
                domain: Number(event.target.value),
              }))
            }
          />
          <span>{expression.domain.toFixed(1)}</span>
        </label>

        <label>
          Detail
          <input
            type="range"
            min="12"
            max="96"
            step="12"
            value={expression.steps}
            onChange={(event) =>
              setExpression((current) => ({
                ...current,
                steps: Number(event.target.value),
              }))
            }
          />
          <span>{expression.steps} samples</span>
        </label>

        <div className="statusRow">
          <span>WebXR</span>
          <strong data-status={xrStatus}>{formatXrStatus(xrStatus)}</strong>
        </div>
      </aside>
    </main>
  );
}

function formatXrStatus(status: WebXrStatus): string {
  if (status === "available") {
    return "available";
  }

  if (status === "checking") {
    return "checking";
  }

  return "browser-only";
}
