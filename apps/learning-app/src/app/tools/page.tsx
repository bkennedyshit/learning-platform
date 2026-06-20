import Link from "next/link";

const TOOLS = [
  { slug: "matrix", emoji: "🔢", name: "Matrix Commander", desc: "Add, multiply, transpose, determinant, and inverse of matrices.", tag: "Linear Algebra" },
  { slug: "calculus", emoji: "📈", name: "Calculus Visualizer", desc: "Plot f(x), its derivative, and the tangent line at any point.", tag: "Calculus" },
  { slug: "probability", emoji: "🎲", name: "Probability Studio", desc: "Normal, binomial, and Poisson distributions with live stats.", tag: "Statistics" },
  { slug: "gradient-descent", emoji: "🏔️", name: "Gradient Descent", desc: "Watch optimization roll down a loss landscape.", tag: "Machine Learning" },
];

export const metadata = { title: "Tools & Calculators | Aura" };

export default function ToolsHub() {
  return (
    <main style={{ maxWidth: 1000, margin: "0 auto", padding: "3rem 1.5rem" }}>
      <Link href="/" style={{ color: "var(--text-muted)", fontSize: ".9rem" }}>← Home</Link>
      <h1 style={{ margin: ".5rem 0 .25rem", fontSize: "2.5rem" }}>Interactive Tools</h1>
      <p style={{ color: "var(--text-secondary)", marginBottom: "2.5rem" }}>
        Hands-on calculators and visualizers to explore the math behind the lessons.
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", gap: "1.25rem" }}>
        {TOOLS.map((t) => (
          <Link key={t.slug} href={`/tools/${t.slug}`} className="glass-panel" style={{ padding: "1.5rem", display: "flex", flexDirection: "column", gap: ".6rem", color: "inherit", textDecoration: "none" }}>
            <div style={{ fontSize: "2rem" }}>{t.emoji}</div>
            <span style={{ fontSize: ".75rem", color: "var(--accent-primary)", fontWeight: 600, textTransform: "uppercase", letterSpacing: ".05em" }}>{t.tag}</span>
            <h3 style={{ margin: 0, fontSize: "1.25rem" }}>{t.name}</h3>
            <p style={{ margin: 0, color: "var(--text-secondary)", fontSize: ".9rem", lineHeight: 1.5 }}>{t.desc}</p>
          </Link>
        ))}
      </div>
    </main>
  );
}
