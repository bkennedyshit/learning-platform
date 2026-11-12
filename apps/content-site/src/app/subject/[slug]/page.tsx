import { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getSubjectBySlug, getAllSubjectSlugs, type SubjectLessonRef } from "../../../lib/manifest";
import { SITE_URL } from "../../../lib/site";

interface Props {
  params: Promise<{ slug: string }>;
}

const studyGuides: Record<string, { summary: string; steps: string[] }> = {
  cybersecurity: {
    summary: "Learn to threat-model a web app, review access controls and dependencies, and apply the same checks to cloud deployments and AI features.",
    steps: [
      "Start with Threat Modeling Fundamentals. Draw a small web app with a browser, API, and database. Mark where credentials and user data cross a boundary.",
      "Use the application security and identity lessons to review one sensitive API action. Write down who can request it, what permission the server checks, and what you expect when the check fails.",
      "Use the supply chain, network, and cloud lessons to extend your review to deployment. If the app uses a model, use the AI security lesson to review what data and actions the model can access.",
    ],
  },
  "databases-and-storage-engines": {
    summary: "Follow a database operation from disk pages and indexes through transactions, recovery, query execution, and replication.",
    steps: [
      "Start with Storage Engine Fundamentals, then compare B-trees and LSM trees. Pick a workload with a mix of inserts and range reads and list which operations you need to measure.",
      "Read the transaction, recovery, and concurrency lessons together. Sketch two transactions updating the same row, then describe what each transaction should see before and after a commit.",
      "Continue to Query Processing and Distributed Databases. Use a query plan to locate the work on one node before investigating how replicas and network delays affect the result.",
    ],
  },
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const subject = getSubjectBySlug(slug);
  if (!subject) {
    return { title: "Subject Not Found" };
  }
  return {
    title: `${subject.name} - Learning Platform`,
    description: studyGuides[subject.slug]?.summary ?? `Browse ${subject.lessonCount} lessons in ${subject.name}.`,
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
  const studyGuide = studyGuides[subject.slug];

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
        {studyGuide && <p>{studyGuide.summary}</p>}
      </header>

      {studyGuide && (
        <section aria-labelledby="study-path-heading" className="glass-panel" style={{ marginBottom: '2rem' }}>
          <h2 id="study-path-heading">How to work through this subject</h2>
          <ol>
            {studyGuide.steps.map((step) => <li key={step}>{step}</li>)}
          </ol>
        </section>
      )}

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
