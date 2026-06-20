"use client";

import React, { useState } from "react";
import Link from "next/link";

type M = number[][];

const make = (r: number, c: number, fill = 0): M =>
  Array.from({ length: r }, () => Array.from({ length: c }, () => fill));

function mul(a: M, b: M): M {
  const r = a.length, n = a[0].length, c = b[0].length;
  if (b.length !== n) throw new Error("A columns must equal B rows for A×B.");
  const out = make(r, c);
  for (let i = 0; i < r; i++)
    for (let j = 0; j < c; j++)
      for (let k = 0; k < n; k++) out[i][j] += a[i][k] * b[k][j];
  return out;
}
const addSub = (a: M, b: M, s: 1 | -1): M => {
  if (a.length !== b.length || a[0].length !== b[0].length) throw new Error("A and B must have the same dimensions.");
  return a.map((row, i) => row.map((v, j) => v + s * b[i][j]));
};
const T = (a: M): M => a[0].map((_, j) => a.map((row) => row[j]));

function det(a: M): number {
  const n = a.length;
  if (n !== a[0].length) throw new Error("Determinant requires a square matrix.");
  const m = a.map((r) => r.slice());
  let d = 1;
  for (let i = 0; i < n; i++) {
    let p = i;
    while (p < n && Math.abs(m[p][i]) < 1e-12) p++;
    if (p === n) return 0;
    if (p !== i) { [m[i], m[p]] = [m[p], m[i]]; d = -d; }
    d *= m[i][i];
    for (let k = i + 1; k < n; k++) {
      const f = m[k][i] / m[i][i];
      for (let j = i; j < n; j++) m[k][j] -= f * m[i][j];
    }
  }
  return d;
}

function inverse(a: M): M {
  const n = a.length;
  if (n !== a[0].length) throw new Error("Inverse requires a square matrix.");
  const m = a.map((r, i) => [...r, ...Array.from({ length: n }, (_, j) => (i === j ? 1 : 0))]);
  for (let i = 0; i < n; i++) {
    let p = i;
    while (p < n && Math.abs(m[p][i]) < 1e-12) p++;
    if (p === n) throw new Error("Matrix is singular (no inverse).");
    [m[i], m[p]] = [m[p], m[i]];
    const piv = m[i][i];
    for (let j = 0; j < 2 * n; j++) m[i][j] /= piv;
    for (let k = 0; k < n; k++) {
      if (k === i) continue;
      const f = m[k][i];
      for (let j = 0; j < 2 * n; j++) m[k][j] -= f * m[i][j];
    }
  }
  return m.map((r) => r.slice(n));
}

const fmt = (v: number) => (Math.abs(v) < 1e-10 ? 0 : Math.round(v * 1000) / 1000);

function Grid({ m, onChange, editable }: { m: M; onChange?: (r: number, c: number, v: number) => void; editable?: boolean }) {
  return (
    <div style={{ display: "inline-grid", gridTemplateColumns: `repeat(${m[0].length}, 1fr)`, gap: 6 }}>
      {m.map((row, i) =>
        row.map((v, j) =>
          editable ? (
            <input
              key={`${i}-${j}`}
              type="number"
              value={v}
              onChange={(e) => onChange?.(i, j, parseFloat(e.target.value) || 0)}
              style={{ width: 64, padding: "0.4rem", textAlign: "center", background: "var(--bg-tertiary)", border: "1px solid var(--border-color)", borderRadius: 6, color: "inherit" }}
            />
          ) : (
            <div key={`${i}-${j}`} style={{ width: 64, padding: "0.4rem", textAlign: "center", background: "var(--bg-tertiary)", border: "1px solid var(--border-color)", borderRadius: 6 }}>
              {fmt(v)}
            </div>
          )
        )
      )}
    </div>
  );
}

export default function MatrixCalculator() {
  const [a, setA] = useState<M>([[1, 2], [3, 4]]);
  const [b, setB] = useState<M>([[5, 6], [7, 8]]);
  const [result, setResult] = useState<M | null>(null);
  const [scalar, setScalarResult] = useState<number | null>(null);
  const [error, setError] = useState("");

  const resize = (which: "a" | "b", r: number, c: number) => {
    const cur = which === "a" ? a : b;
    const next = make(r, c);
    for (let i = 0; i < r; i++) for (let j = 0; j < c; j++) next[i][j] = cur[i]?.[j] ?? 0;
    which === "a" ? setA(next) : setB(next);
  };
  const edit = (which: "a" | "b") => (i: number, j: number, v: number) => {
    const cur = (which === "a" ? a : b).map((r) => r.slice());
    cur[i][j] = v;
    which === "a" ? setA(cur) : setB(cur);
  };

  const run = (op: () => M | number) => {
    setError(""); setResult(null); setScalarResult(null);
    try {
      const out = op();
      if (typeof out === "number") setScalarResult(out);
      else setResult(out);
    } catch (e) { setError((e as Error).message); }
  };

  const Dim = ({ which, m }: { which: "a" | "b"; m: M }) => (
    <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 10 }}>
      <span style={{ color: "var(--text-muted)", fontSize: ".85rem" }}>size</span>
      <select value={m.length} onChange={(e) => resize(which, +e.target.value, m[0].length)} style={sel}>
        {[1, 2, 3, 4].map((n) => <option key={n} value={n}>{n}</option>)}
      </select>
      <span>×</span>
      <select value={m[0].length} onChange={(e) => resize(which, m.length, +e.target.value)} style={sel}>
        {[1, 2, 3, 4].map((n) => <option key={n} value={n}>{n}</option>)}
      </select>
    </div>
  );

  return (
    <main style={{ maxWidth: 1000, margin: "0 auto", padding: "2.5rem 1.5rem" }}>
      <Link href="/tools" style={{ color: "var(--text-muted)", fontSize: ".9rem" }}>← All tools</Link>
      <h1 style={{ margin: ".5rem 0 .25rem" }}>Matrix Commander</h1>
      <p style={{ color: "var(--text-secondary)", marginBottom: "2rem" }}>Linear algebra: add, subtract, multiply, transpose, determinant, inverse.</p>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "2rem", marginBottom: "1.5rem" }}>
        <div className="glass-panel" style={{ padding: "1.25rem" }}>
          <h3 style={{ marginTop: 0 }}>Matrix A</h3>
          <Dim which="a" m={a} />
          <Grid m={a} editable onChange={edit("a")} />
        </div>
        <div className="glass-panel" style={{ padding: "1.25rem" }}>
          <h3 style={{ marginTop: 0 }}>Matrix B</h3>
          <Dim which="b" m={b} />
          <Grid m={b} editable onChange={edit("b")} />
        </div>
      </div>

      <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: "1.5rem" }}>
        <button style={btn} onClick={() => run(() => addSub(a, b, 1))}>A + B</button>
        <button style={btn} onClick={() => run(() => addSub(a, b, -1))}>A − B</button>
        <button style={btn} onClick={() => run(() => mul(a, b))}>A × B</button>
        <button style={btn} onClick={() => run(() => T(a))}>Aᵀ</button>
        <button style={btn} onClick={() => run(() => det(a))}>det(A)</button>
        <button style={btn} onClick={() => run(() => inverse(a))}>A⁻¹</button>
      </div>

      {error && <div style={{ color: "#f87171", marginBottom: "1rem" }}>{error}</div>}
      {(result || scalar !== null) && (
        <div className="glass-panel" style={{ padding: "1.25rem" }}>
          <h3 style={{ marginTop: 0 }}>Result</h3>
          {scalar !== null ? <div style={{ fontSize: "1.5rem" }}>{fmt(scalar)}</div> : <Grid m={result!} />}
        </div>
      )}
    </main>
  );
}

const btn: React.CSSProperties = { padding: "0.6rem 1.1rem", borderRadius: 8, border: "1px solid var(--border-color)", background: "var(--bg-tertiary)", color: "inherit", cursor: "pointer", fontWeight: 600 };
const sel: React.CSSProperties = { padding: "0.3rem", background: "var(--bg-tertiary)", border: "1px solid var(--border-color)", borderRadius: 6, color: "inherit" };
