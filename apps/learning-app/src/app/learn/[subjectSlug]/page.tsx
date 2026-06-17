import Link from "next/link";
import { notFound } from "next/navigation";
import { getSubjectBySlug, getAllSubjectSlugs } from "../../../lib/manifest";

interface Props {
  params: Promise<{ subjectSlug: string }>;
}

export default async function SubjectPage({ params }: Props) {
  const { subjectSlug } = await params;
  const subject = getSubjectBySlug(subjectSlug);
  if (!subject) notFound();

  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: "3rem 2rem" }}>
      <Link href="/learn" style={{ fontSize: "0.9rem", color: "var(--text-muted)" }}>← All subjects</Link>
      <header style={{ margin: "0.5rem 0 2rem" }}>
        <h1 style={{ fontSize: "2.25rem" }}>{subject.name}</h1>
        <p style={{ color: "var(--text-secondary)" }}>{subject.catalog} · {subject.lessonCount} lessons</p>
      </header>

      <ol style={{ listStyle: "none", display: "grid", gap: "0.75rem", padding: 0, margin: 0 }}>
        {subject.lessons.map((lesson, i) => (
          <li key={lesson.slug}>
            <Link href={`/learn/${subject.slug}/${lesson.slug}`} style={{ textDecoration: "none", color: "inherit" }}>
              <div className="glass-panel" style={{ display: "flex", alignItems: "center", gap: "1rem", padding: "1rem 1.25rem" }}>
                <span style={{
                  minWidth: 36, height: 36, borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center",
                  background: "var(--bg-tertiary)", color: "var(--accent-primary)", fontWeight: 600, fontSize: "0.85rem"
                }}>{lesson.chapter || i + 1}</span>
                <span style={{ fontSize: "1.05rem" }}>{lesson.title}</span>
              </div>
            </Link>
          </li>
        ))}
      </ol>
    </main>
  );
}

export function generateStaticParams() {
  return getAllSubjectSlugs().map((subjectSlug) => ({ subjectSlug }));
}
