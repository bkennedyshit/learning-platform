import { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getSubjectBySlug, getAllSubjectSlugs, type SubjectLessonRef } from "../../../lib/manifest";
import { SITE_URL } from "../../../lib/site";

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
    alternates: { canonical: `${SITE_URL}/subject/${subject.slug}` },
    // A hub whose lessons are all still in development has nothing to index yet.
    ...(subject.indexable ? {} : { robots: { index: false, follow: true } }),
  };
}

function LessonList({ items, offset = 0 }: { items: SubjectLessonRef[]; offset?: number }) {
  return (
    <ol style={{ listStyle: 'none', display: 'grid', gap: '0.75rem', padding: 0 }}>
      {items.map((lesson, i) => (
        <li key={lesson.slug}>
          <Link href={`/${lesson.slug}`} style={{ color: 'inherit' }}>
            <div className="glass-panel" style={{ display: 'flex', alignItems: 'center', gap: '1rem', padding: '1rem 1.25rem' }}>
              <span className="badge">{lesson.chapter || offset + i + 1}</span>
              <span style={{ fontSize: '1.1rem' }}>{lesson.title}</span>
            </div>
          </Link>
        </li>
      ))}
    </ol>
  );
}

export default async function SubjectPage({ params }: Props) {
  const { slug } = await params;
  const subject = getSubjectBySlug(slug);
  if (!subject) {
    notFound();
  }

  const ready = subject.lessons.filter((l) => l.indexable);
  const inDevelopment = subject.lessons.filter((l) => !l.indexable);

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

      {ready.length > 0 && (
        <section aria-labelledby="lessons-heading">
          <h2 id="lessons-heading">Lessons</h2>
          <LessonList items={ready} />
        </section>
      )}

      {inDevelopment.length > 0 && (
        <section aria-labelledby="in-development-heading" style={{ marginTop: ready.length ? '2.5rem' : 0 }}>
          <h2 id="in-development-heading">In development</h2>
          <p>These lesson outlines are still being written.</p>
          <LessonList items={inDevelopment} />
        </section>
      )}
    </main>
  );
}

export function generateStaticParams() {
  return getAllSubjectSlugs().map((slug) => ({ slug }));
}
