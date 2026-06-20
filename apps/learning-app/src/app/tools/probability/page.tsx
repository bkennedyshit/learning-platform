"use client";

import React, { useEffect, useRef, useState } from "react";
import Link from "next/link";

type Dist = "normal" | "binomial" | "poisson";

function logFact(n: number): number {
  let s = 0;
  for (let i = 2; i <= n; i++) s += Math.log(i);
  return s;
}
const choose = (n: number, k: number) => Math.exp(logFact(n) - logFact(k) - logFact(n - k));
const normalPdf = (x: number, mu: number, sd: number) =>
  Math.exp(-((x - mu) ** 2) / (2 * sd * sd)) / (sd * Math.sqrt(2 * Math.PI));
const binomPmf = (k: number, n: number, p: number) => choose(n, k) * p ** k * (1 - p) ** (n - k);
const poissonPmf = (k: number, l: number) => Math.exp(k * Math.log(l) - l - logFact(k));

export default function ProbabilityStudio() {
  const ref = useRef<HTMLCanvasElement>(null);
  const [dist, setDist] = useState<Dist>("normal");
  const [mu, setMu] = useState(0);
  const [sd, setSd] = useState(1);
  const [n, setN] = useState(20);
  const [p, setP] = useState(0.5);
  const [lambda, setLambda] = useState(4);

  const stats =
    dist === "normal" ? { mean: mu, varc: sd * sd } :
    dist === "binomial" ? { mean: n * p, varc: n * p * (1 - p) } :
    { mean: lambda, varc: lambda };

  useEffect(() => {
    const cv = ref.current; if (!cv) return;
    const ctx = cv.getContext("2d"); if (!ctx) return;
    const W = cv.width, H = cv.height, pad = 40;
    ctx.fillStyle = "#0b1020"; ctx.fillRect(0, 0, W, H);
    ctx.strokeStyle = "rgba(255,255,255,0.3)";
    ctx.beginPath(); ctx.moveTo(pad, H - pad); ctx.lineTo(W - 10, H - pad); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(pad, 10); ctx.lineTo(pad, H - pad); ctx.stroke();

    if (dist === "normal") {
      const xmin = mu - 4 * sd, xmax = mu + 4 * sd;
      const peak = normalPdf(mu, mu, sd);
      ctx.strokeStyle = "#6366f1"; ctx.lineWidth = 2; ctx.beginPath();
      for (let px = 0; px <= W - pad - 10; px++) {
        const x = xmin + (px / (W - pad - 10)) * (xmax - xmin);
        const y = normalPdf(x, mu, sd) / peak;
        const cx = pad + px, cy = (H - pad) - y * (H - pad - 20);
        px === 0 ? ctx.moveTo(cx, cy) : ctx.lineTo(cx, cy);
      }
      ctx.stroke();
    } else {
      const N = dist === "binomial" ? n : Math.ceil(lambda + 4 * Math.sqrt(lambda)) + 1;
      const pmf = (k: number) => (dist === "binomial" ? binomPmf(k, n, p) : poissonPmf(k, lambda));
      let peak = 0;
      for (let k = 0; k <= N; k++) peak = Math.max(peak, pmf(k));
      const bw = (W - pad - 10) / (N + 1);
      ctx.fillStyle = "#6366f1";
      for (let k = 0; k <= N; k++) {
        const h = (pmf(k) / peak) * (H - pad - 20);
        ctx.fillRect(pad + k * bw + 2, (H - pad) - h, Math.max(1, bw - 4), h);
      }
    }
  }, [dist, mu, sd, n, p, lambda]);

  return (
    <main style={{ maxWidth: 1000, margin: "0 auto", padding: "2.5rem 1.5rem" }}>
      <Link href="/tools" style={{ color: "var(--text-muted)", fontSize: ".9rem" }}>← All tools</Link>
      <h1 style={{ margin: ".5rem 0 .25rem" }}>Probability Studio</h1>
      <p style={{ color: "var(--text-secondary)", marginBottom: "1.5rem" }}>Explore distributions: PDF / PMF with live mean and variance.</p>

      <div style={{ display: "flex", gap: 8, marginBottom: "1rem" }}>
        {(["normal", "binomial", "poisson"] as Dist[]).map((d) => (
          <button key={d} onClick={() => setDist(d)} style={{ ...btn, background: dist === d ? "var(--accent-primary)" : "var(--bg-tertiary)", color: dist === d ? "#fff" : "inherit" }}>
            {d[0].toUpperCase() + d.slice(1)}
          </button>
        ))}
      </div>

      <div style={{ display: "flex", flexWrap: "wrap", gap: 16, marginBottom: "1rem" }}>
        {dist === "normal" && <>
          <Slider label={`μ = ${mu.toFixed(1)}`} min={-5} max={5} step={0.1} value={mu} onChange={setMu} />
          <Slider label={`σ = ${sd.toFixed(1)}`} min={0.2} max={4} step={0.1} value={sd} onChange={setSd} />
        </>}
        {dist === "binomial" && <>
          <Slider label={`n = ${n}`} min={1} max={50} step={1} value={n} onChange={(v) => setN(Math.round(v))} />
          <Slider label={`p = ${p.toFixed(2)}`} min={0} max={1} step={0.01} value={p} onChange={setP} />
        </>}
        {dist === "poisson" && <Slider label={`λ = ${lambda.toFixed(1)}`} min={0.5} max={20} step={0.1} value={lambda} onChange={setLambda} />}
      </div>

      <canvas ref={ref} width={920} height={420} style={{ width: "100%", borderRadius: 12, border: "1px solid var(--border-color)" }} />

      <div className="glass-panel" style={{ padding: "1rem 1.25rem", marginTop: "1rem", display: "flex", gap: "2rem" }}>
        <span>Mean μ = <b>{stats.mean.toFixed(3)}</b></span>
        <span>Variance σ² = <b>{stats.varc.toFixed(3)}</b></span>
        <span>Std σ = <b>{Math.sqrt(stats.varc).toFixed(3)}</b></span>
      </div>
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
