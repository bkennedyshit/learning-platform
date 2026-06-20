"use client";

import React, { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { compile, numDeriv } from "../../../lib/mathx";

export default function CalculusVisualizer() {
  const ref = useRef<HTMLCanvasElement>(null);
  const [expr, setExpr] = useState("x^2");
  const [x0, setX0] = useState(1);
  const [showDeriv, setShowDeriv] = useState(true);
  const [showTangent, setShowTangent] = useState(true);
  const [error, setError] = useState("");
  const [readout, setReadout] = useState<{ fx: number; dfx: number } | null>(null);

  useEffect(() => {
    const cv = ref.current;
    if (!cv) return;
    const ctx = cv.getContext("2d");
    if (!ctx) return;

    const W = cv.width, H = cv.height;
    const xmin = -10, xmax = 10, ymin = -10, ymax = 10;
    const sx = (x: number) => ((x - xmin) / (xmax - xmin)) * W;
    const sy = (y: number) => H - ((y - ymin) / (ymax - ymin)) * H;

    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = "#0b1020";
    ctx.fillRect(0, 0, W, H);

    // grid
    ctx.strokeStyle = "rgba(255,255,255,0.07)";
    ctx.lineWidth = 1;
    for (let g = xmin; g <= xmax; g++) {
      ctx.beginPath(); ctx.moveTo(sx(g), 0); ctx.lineTo(sx(g), H); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(0, sy(g)); ctx.lineTo(W, sy(g)); ctx.stroke();
    }
    // axes
    ctx.strokeStyle = "rgba(255,255,255,0.35)";
    ctx.beginPath(); ctx.moveTo(sx(0), 0); ctx.lineTo(sx(0), H); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0, sy(0)); ctx.lineTo(W, sy(0)); ctx.stroke();

    let f: (x: number) => number;
    try {
      const c = compile(expr);
      f = (x) => c.eval(x);
      setError("");
    } catch (e) {
      setError((e as Error).message);
      return;
    }

    const plot = (g: (x: number) => number, color: string) => {
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      let started = false;
      for (let px = 0; px <= W; px++) {
        const x = xmin + (px / W) * (xmax - xmin);
        const y = g(x);
        if (!isFinite(y)) { started = false; continue; }
        const py = sy(y);
        if (py < -1e4 || py > H + 1e4) { started = false; continue; }
        if (!started) { ctx.moveTo(px, py); started = true; } else ctx.lineTo(px, py);
      }
      ctx.stroke();
    };

    plot(f, "#6366f1"); // f(x)
    if (showDeriv) plot((x) => numDeriv(f, x), "#ec4899"); // f'(x)

    // tangent at x0
    try {
      const fx = f(x0);
      const dfx = numDeriv(f, x0);
      setReadout({ fx, dfx });
      if (showTangent && isFinite(fx) && isFinite(dfx)) {
        const tan = (x: number) => fx + dfx * (x - x0);
        ctx.strokeStyle = "#22d3ee";
        ctx.lineWidth = 2;
        ctx.setLineDash([6, 4]);
        ctx.beginPath();
        ctx.moveTo(sx(xmin), sy(tan(xmin)));
        ctx.lineTo(sx(xmax), sy(tan(xmax)));
        ctx.stroke();
        ctx.setLineDash([]);
        // point
        ctx.fillStyle = "#22d3ee";
        ctx.beginPath(); ctx.arc(sx(x0), sy(fx), 5, 0, Math.PI * 2); ctx.fill();
      }
    } catch { /* ignore */ }
  }, [expr, x0, showDeriv, showTangent]);

  return (
    <main style={{ maxWidth: 1000, margin: "0 auto", padding: "2.5rem 1.5rem" }}>
      <Link href="/tools" style={{ color: "var(--text-muted)", fontSize: ".9rem" }}>← All tools</Link>
      <h1 style={{ margin: ".5rem 0 .25rem" }}>Calculus Visualizer</h1>
      <p style={{ color: "var(--text-secondary)", marginBottom: "1.5rem" }}>Plot f(x), its derivative f′(x), and the tangent line at a point.</p>

      <div style={{ display: "flex", flexWrap: "wrap", gap: 12, alignItems: "center", marginBottom: "1rem" }}>
        <label>f(x) = <input value={expr} onChange={(e) => setExpr(e.target.value)} style={inp} placeholder="e.g. sin(x), x^3-2*x" /></label>
        <label style={chk}><input type="checkbox" checked={showDeriv} onChange={(e) => setShowDeriv(e.target.checked)} /> <span style={{ color: "#ec4899" }}>f′(x)</span></label>
        <label style={chk}><input type="checkbox" checked={showTangent} onChange={(e) => setShowTangent(e.target.checked)} /> <span style={{ color: "#22d3ee" }}>tangent</span></label>
      </div>
      <div style={{ display: "flex", gap: 12, alignItems: "center", marginBottom: "1rem" }}>
        <span style={{ color: "var(--text-muted)" }}>x₀ = {x0.toFixed(2)}</span>
        <input type="range" min={-10} max={10} step={0.1} value={x0} onChange={(e) => setX0(parseFloat(e.target.value))} style={{ flex: 1 }} />
      </div>

      {error && <div style={{ color: "#f87171", marginBottom: "1rem" }}>{error}</div>}

      <canvas ref={ref} width={920} height={520} style={{ width: "100%", borderRadius: 12, border: "1px solid var(--border-color)" }} />

      {readout && !error && (
        <div className="glass-panel" style={{ padding: "1rem 1.25rem", marginTop: "1rem", display: "flex", gap: "2rem" }}>
          <span><span style={{ color: "#6366f1" }}>f(x₀)</span> = {fmt(readout.fx)}</span>
          <span><span style={{ color: "#ec4899" }}>f′(x₀)</span> = {fmt(readout.dfx)} <span style={{ color: "var(--text-muted)" }}>(slope of tangent)</span></span>
        </div>
      )}
    </main>
  );
}

const fmt = (v: number) => (isFinite(v) ? Math.round(v * 1000) / 1000 : "—");
const inp: React.CSSProperties = { padding: "0.5rem", background: "var(--bg-tertiary)", border: "1px solid var(--border-color)", borderRadius: 6, color: "inherit", marginLeft: 6, minWidth: 220 };
const chk: React.CSSProperties = { display: "inline-flex", alignItems: "center", gap: 6 };
