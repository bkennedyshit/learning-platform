import Link from "next/link";
import { getSubjects } from "../lib/manifest";

const CATALOG_LABELS: Record<string, string> = {
  advanced: "Advanced / Higher-Ed",
  k12: "K-12",
};

export default async function Home() {
  const subjects = getSubjects();
  const totalLessons = subjects.reduce((sum, s) => sum + s.lessonCount, 0);
  const advanced = subjects.filter((s) => s.catalog === "advanced");
  const k12 = subjects.filter((s) => s.catalog === "k12");

  const Card = ({ s }: { s: (typeof subjects)[number] }) => (
    <Link key={s.slug} href={`/subject/${s.slug}`} className="subject-card">
      <div className="subject-card__top">
        <span className="badge">{CATALOG_LABELS[s.catalog] ?? s.catalog}</span>
        <span className="subject-card__count">{s.lessonCount}</span>
      </div>
      <h3 className="subject-card__title">{s.name}</h3>
      <span className="subject-card__cta">Start learning →</span>
    </Link>
  );

  return (
    <main>
      {/* Hero */}
      <section className="hero">
        <div className="hero__glow" aria-hidden />
        <div className="container hero__inner">
          <span className="hero__eyebrow">✦ Open learning library</span>
          <h1 className="hero__title">
            Learn anything,<br />
            <span className="hero__accent">grounded in real material.</span>
          </h1>
          <p className="hero__sub">
            {subjects.length} subjects · {totalLessons.toLocaleString()} lessons across math, science,
            engineering, languages, and code — with an AI tutor that answers only from the lesson.
          </p>
          <div className="hero__actions">
            <a href="#catalog" className="btn">Browse the catalog</a>
            <a href="#advanced" className="btn btn-outline">Advanced tracks</a>
          </div>
        </div>
      </section>

      {/* Catalog */}
      <section id="catalog" className="container section">
        <div className="section__head" id="advanced">
          <h2>Advanced &amp; Higher Education</h2>
          <p>{advanced.length} subjects</p>
        </div>
        <div className="subject-grid">
          {advanced.map((s) => <Card key={s.slug} s={s} />)}
        </div>

        <div className="section__head" id="k12" style={{ marginTop: "3.5rem" }}>
          <h2>K-12</h2>
          <p>{k12.length} subjects</p>
        </div>
        <div className="subject-grid">
          {k12.map((s) => <Card key={s.slug} s={s} />)}
        </div>
      </section>
    </main>
  );
}
