import { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getSubjectBySlug, getAllSubjectSlugs } from "../../../lib/manifest";

interface Props {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const subject = getSubjectBySlug(slug);
  if (!subject) {
    return { title: "Subject Not Found" };
  }
  return {
    title: `${subject.name} - Learning Platform`,
    description: `Browse ${subject.lessonCount} lessons in ${subject.name}.`,
    alternates: { canonical: `https://platform.example.com/subject/${subject.slug}` },
  };
}

export default async function SubjectPage({ params }: Props) {
  const { slug } = await params;
  const subject = getSubjectBySlug(slug);
  if (!subject) {
    notFound();
  }

  return (
    <main className="container" style={{ padding: '4rem 2rem' }}>
      <nav style={{ marginBottom: '1.5rem' }}>
        <Link href="/" className="btn btn-outline">&larr; All Subjects</Link>
      </nav>

      <header style={{ marginBottom: '2rem' }}>
        <div className="meta-info">
          <span className="badge">Catalog: {subject.catalog}</span>
          <span className="badge">{subject.lessonCount} lessons</span>
        </div>
        <h1 style={{ marginTop: '1rem' }}>{subject.name}</h1>
      </header>

      <ol style={{ listStyle: 'none', display: 'grid', gap: '0.75rem', padding: 0 }}>
        {subject.lessons.map((lesson, i) => (
          <li key={lesson.slug}>
            <Link href={`/${lesson.slug}`} style={{ color: 'inherit' }}>
              <div className="glass-panel" style={{ display: 'flex', alignItems: 'center', gap: '1rem', padding: '1rem 1.25rem' }}>
                <span className="badge">{lesson.chapter || i + 1}</span>
                <span style={{ fontSize: '1.1rem' }}>{lesson.title}</span>
              </div>
            </Link>
          </li>
        ))}
      </ol>
    </main>
  );
}

export function generateStaticParams() {
  return getAllSubjectSlugs().map((slug) => ({ slug }));
}
