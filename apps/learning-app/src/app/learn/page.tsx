import Link from "next/link";
import { getSubjects } from "../../lib/manifest";

interface Props {
  searchParams: Promise<{ catalog?: string }>;
}

export default async function LearnHome({ searchParams }: Props) {
  const { catalog } = await searchParams;
  const all = getSubjects();
  const subjects = catalog ? all.filter((s) => s.catalog === catalog) : all;
  const totalLessons = subjects.reduce((n, s) => n + s.lessonCount, 0);

  return (
    <main style={{ maxWidth: 1200, margin: "0 auto", padding: "3rem 2rem" }}>
      <header style={{ marginBottom: "2.5rem", display: "flex", justifyContent: "space-between", alignItems: "flex-end", flexWrap: "wrap", gap: "1rem" }}>
        <div>
          <Link href="/" style={{ fontSize: "0.9rem", color: "var(--text-muted)" }}>← Home</Link>
          <h1 style={{ fontSize: "2.5rem", marginTop: "0.5rem" }}>
            {catalog === "k12" ? "K-12 Curriculum" : catalog === "advanced" ? "Advanced & Higher Ed" : "Explore the Catalog"}
          </h1>
          <p style={{ color: "var(--text-secondary)" }}>{subjects.length} subjects · {totalLessons} lessons</p>
        </div>
        <div style={{ display: "flex", gap: "0.5rem" }}>
          <Link href="/learn" className="btn-secondary" style={{ padding: "0.5rem 1rem" }}>All</Link>
          <Link href="/learn?catalog=k12" className="btn-secondary" style={{ padding: "0.5rem 1rem" }}>K-12</Link>
          <Link href="/learn?catalog=advanced" className="btn-secondary" style={{ padding: "0.5rem 1rem" }}>Advanced</Link>
          <Link href="/tools" className="btn-secondary" style={{ padding: "0.5rem 1rem" }}>🧮 Tools</Link>
        </div>
      </header>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", gap: "1.25rem" }}>
        {subjects.map((s) => (
          <Link key={s.slug} href={`/learn/${s.slug}`} style={{ textDecoration: "none", color: "inherit" }}>
            <div className="glass-panel" style={{ height: "100%", padding: "1.5rem", display: "flex", flexDirection: "column", gap: "0.75rem" }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.8rem", color: "var(--text-muted)" }}>
                <span>{s.catalog}</span>
                <span>{s.lessonCount} lessons</span>
              </div>
              <h2 style={{ fontSize: "1.25rem" }}>{s.name}</h2>
            </div>
          </Link>
        ))}
      </div>
    </main>
  );
}
