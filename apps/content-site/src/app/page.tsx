import Link from "next/link";
import { getSubjects } from "../lib/manifest";

export default async function Home() {
  const subjects = getSubjects();
  const totalLessons = subjects.reduce((sum, s) => sum + s.lessonCount, 0);

  return (
    <main className="container" style={{ padding: '4rem 2rem' }}>
      <header style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h1>Learning Platform Library</h1>
        <p style={{ color: 'var(--muted)', fontSize: '1.125rem', marginTop: '1rem' }}>
          {subjects.length} subjects · {totalLessons} open-source lessons
        </p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1.5rem' }}>
        {subjects.map((subject) => (
          <Link key={subject.slug} href={`/subject/${subject.slug}`} style={{ color: 'inherit' }}>
            <div className="glass-panel" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                <span className="badge">{subject.catalog}</span>
                <span className="badge">{subject.lessonCount} lessons</span>
              </div>
              <h2 style={{ fontSize: '1.35rem', marginTop: 'auto' }}>{subject.name}</h2>
            </div>
          </Link>
        ))}
      </div>
    </main>
  );
}
