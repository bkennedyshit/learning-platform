"use client";

import React, { useEffect, useRef, useState } from "react";
import Link from "next/link";

type Surface = "bowl" | "ellipse" | "doubleWell";

const SURFACES: Record<Surface, { label: string; f: (x: number, y: number) => number }> = {
  bowl: { label: "Bowl  x² + y²", f: (x, y) => x * x + y * y },
  ellipse: { label: "Ellipse  x² + 8y²", f: (x, y) => x * x + 8 * y * y },
  doubleWell: { label: "Double well  (x²−1)² + y²", f: (x, y) => (x * x - 1) ** 2 + y * y },
};

const grad = (f: (x: number, y: number) => number, x: number, y: number, h = 1e-4) => [
  (f(x + h, y) - f(x - h, y)) / (2 * h),
  (f(x, y + h) - f(x, y - h)) / (2 * h),
];

export default function GradientDescent() {
  const ref = useRef<HTMLCanvasElement>(null);
  const [surface, setSurface] = useState<Surface>("doubleWell");
  const [lr, setLr] = useState(0.05);
  const [startX, setStartX] = useState(-1.8);
  const [startY, setStartY] = useState(1.8);
  const [steps, setSteps] = useState(40);

  useEffect(() => {
    const cv = ref.current; if (!cv) return;
    const ctx = cv.getContext("2d"); if (!ctx) return;
    const W = cv.width, H = cv.height;
    const R = 2.5;
    const f = SURFACES[surface].f;
    const sx = (x: number) => ((x + R) / (2 * R)) * W;
    const sy = (y: number) => H - ((y + R) / (2 * R)) * H;

    // heatmap (low loss = dark indigo, high = bright)
    let max = 0;
    for (let x = -R; x <= R; x += R / 20) for (let y = -R; y <= R; y += R / 20) max = Math.max(max, f(x, y));
    const cell = 4;
    for (let px = 0; px < W; px += cell) {
      for (let py = 0; py < H; py += cell) {
        const x = (px / W) * 2 * R - R;
        const y = R - (py / H) * 2 * R;
        const t = Math.min(1, f(x, y) / max);
        const r = Math.round(20 + t * 120), g = Math.round(20 + t * 60), b = Math.round(60 + t * 180);
        ctx.fillStyle = `rgb(${r},${g},${b})`;
        ctx.fillRect(px, py, cell, cell);
      }
    }

    // gradient descent path
    let x = startX, y = startY;
    ctx.strokeStyle = "#fbbf24"; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(sx(x), sy(y));
    const pts: [number, number][] = [[x, y]];
    for (let i = 0; i < steps; i++) {
      const [gx, gy] = grad(f, x, y);
      x -= lr * gx; y -= lr * gy;
      if (!isFinite(x) || !isFinite(y) || Math.abs(x) > 10 || Math.abs(y) > 10) break;
      pts.push([x, y]);
      ctx.lineTo(sx(x), sy(y));
    }
    ctx.stroke();
    pts.forEach(([px, py], i) => {
      ctx.fillStyle = i === 0 ? "#f87171" : i === pts.length - 1 ? "#34d399" : "#fbbf24";
      ctx.beginPath(); ctx.arc(sx(px), sy(py), i === 0 || i === pts.length - 1 ? 6 : 2.5, 0, Math.PI * 2); ctx.fill();
    });

    const final = pts[pts.length - 1];
    ctx.fillStyle = "#fff"; ctx.font = "13px sans-serif";
    ctx.fillText(`start (${startX.toFixed(1)}, ${startY.toFixed(1)})  →  end (${final[0].toFixed(2)}, ${final[1].toFixed(2)})  loss=${f(final[0], final[1]).toFixed(3)}`, 12, H - 12);
  }, [surface, lr, startX, startY, steps]);

  return (
    <main style={{ maxWidth: 1000, margin: "0 auto", padding: "2.5rem 1.5rem" }}>
      <Link href="/tools" style={{ color: "var(--text-muted)", fontSize: ".9rem" }}>← All tools</Link>
      <h1 style={{ margin: ".5rem 0 .25rem" }}>Gradient Descent</h1>
      <p style={{ color: "var(--text-secondary)", marginBottom: "1.5rem" }}>Watch gradient descent roll down a loss landscape. Tune the learning rate and start point.</p>

      <div style={{ display: "flex", gap: 8, marginBottom: "1rem", flexWrap: "wrap" }}>
        {(Object.keys(SURFACES) as Surface[]).map((s) => (
          <button key={s} onClick={() => setSurface(s)} style={{ ...btn, background: surface === s ? "var(--accent-primary)" : "var(--bg-tertiary)", color: surface === s ? "#fff" : "inherit" }}>
            {SURFACES[s].label}
          </button>
        ))}
      </div>

      <div style={{ display: "flex", flexWrap: "wrap", gap: 16, marginBottom: "1rem" }}>
        <Slider label={`learning rate = ${lr.toFixed(3)}`} min={0.001} max={0.3} step={0.001} value={lr} onChange={setLr} />
        <Slider label={`steps = ${steps}`} min={1} max={200} step={1} value={steps} onChange={(v) => setSteps(Math.round(v))} />
        <Slider label={`start x = ${startX.toFixed(1)}`} min={-2.4} max={2.4} step={0.1} value={startX} onChange={setStartX} />
        <Slider label={`start y = ${startY.toFixed(1)}`} min={-2.4} max={2.4} step={0.1} value={startY} onChange={setStartY} />
      </div>

      <canvas ref={ref} width={920} height={520} style={{ width: "100%", borderRadius: 12, border: "1px solid var(--border-color)" }} />
      <p style={{ color: "var(--text-muted)", fontSize: ".85rem", marginTop: ".75rem" }}>
        <span style={{ color: "#f87171" }}>●</span> start &nbsp; <span style={{ color: "#fbbf24" }}>●</span> steps &nbsp; <span style={{ color: "#34d399" }}>●</span> end. Try a high learning rate to watch it overshoot, or the double-well to land in different minima from different starts.
      </p>
    </main>
  );
}

function Slider({ label, min, max, step, value, onChange }: { label: string; min: number; max: number; step: number; value: number; onChange: (v: number) => void }) {
  return (
    <label style={{ display: "flex", flexDirection: "column", gap: 4, minWidth: 200 }}>
      <span style={{ color: "var(--text-muted)", fontSize: ".85rem" }}>{label}</span>
      <input type="range" min={min} max={max} step={step} value={value} onChange={(e) => onChange(parseFloat(e.target.value))} />
    </label>
  );
}

const btn: React.CSSProperties = { padding: "0.5rem 1rem", borderRadius: 8, border: "1px solid var(--border-color)", cursor: "pointer", fontWeight: 600 };
