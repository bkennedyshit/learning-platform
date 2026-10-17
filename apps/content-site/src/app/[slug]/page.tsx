import { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getLesson, getAllLessonSlugs } from "../../lib/manifest";
import { SITE_URL } from "../../lib/site";
import LessonContent from "../../components/LessonContent";

interface Props {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const lesson = getLesson(slug);

  if (!lesson) {
    return { title: "Lesson Not Found" };
  }

  const canonicalUrl = `${SITE_URL}/${lesson.slug}`;

  return {
    title: `${lesson.title} - Learning Platform`,
    description: lesson.description ?? `Study ${lesson.title} from the ${lesson.subject} subject.`,
    alternates: {
      canonical: canonicalUrl,
    },
    // Index-promotion gate: unfinished lessons stay reachable and pass link
    // equity, but are kept out of the index until they are rewritten.
    ...(lesson.indexable ? {} : { robots: { index: false, follow: true } }),
  };
}

export default async function LessonPage({ params }: Props) {
  const { slug } = await params;
  const lesson = getLesson(slug);

  if (!lesson) {
    notFound();
  }

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: lesson.title,
    author: { "@type": "Organization", name: "Learning Platform" },
    url: `${SITE_URL}/${lesson.slug}`,
    publisher: { "@type": "Organization", name: "Learning Platform" },
    isAccessibleForFree: lesson.openSource,
  };

  const prevLesson = lesson.prevSlug ? getLesson(lesson.prevSlug) : null;
  const nextLesson = lesson.nextSlug ? getLesson(lesson.nextSlug) : null;
  const relatedLessons = lesson.relatedSlugs
    .map((s) => getLesson(s))
    .filter((l): l is NonNullable<typeof l> => Boolean(l));

  return (
    <main className="container" style={{ padding: '4rem 2rem' }}>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

      <nav style={{ marginBottom: '1.5rem' }}>
        <Link href={`/subject/${lesson.subjectSlug}`} className="btn btn-outline">
          &larr; {lesson.subject}
        </Link>
      </nav>

      <article className="glass-panel" style={{ marginBottom: '2rem' }}>
        <header style={{ marginBottom: '2rem', borderBottom: '1px solid var(--border)', paddingBottom: '1rem' }}>
          <div className="meta-info">
            <span className="badge">Catalog: {lesson.catalog}</span>
            <span className="badge">Audience Tier: {lesson.audienceTier}</span>
            <span className="badge">Subject: {lesson.subject}</span>
          </div>
          <h1 style={{ marginTop: '1rem' }}>{lesson.title}</h1>
        </header>

        <LessonContent html={lesson.html} />

        <div className="license-info" style={{ marginTop: '2rem' }}>
          <p>
            This content is published under the Platform Open Source License.{' '}
            <strong>Attribution: </strong> Learning Platform Contributors.
          </p>
        </div>
      </article>

      <nav className="nav-links">
        {prevLesson ? (
          <Link href={`/${prevLesson.slug}`} className="btn btn-outline" style={{ marginRight: 'auto' }}>
            &larr; Previous: {prevLesson.title}
          </Link>
        ) : (
          <div style={{ marginRight: 'auto' }}></div>
        )}

        {nextLesson ? (
          <Link href={`/${nextLesson.slug}`} className="btn">
            Next: {nextLesson.title} &rarr;
          </Link>
        ) : (
          <div></div>
        )}
      </nav>

      <nav aria-labelledby="related-lessons-heading" className="glass-panel" style={{ marginTop: '2rem' }}>
        <h2 id="related-lessons-heading" style={{ marginTop: 0 }}>More in {lesson.subject}</h2>
        {relatedLessons.length > 0 && (
          <ul>
            {relatedLessons.map((related) => (
              <li key={related.slug}>
                <Link href={`/${related.slug}`}>{related.title}</Link>
              </li>
            ))}
          </ul>
        )}
        <p style={{ marginBottom: 0 }}>
          <Link href={`/subject/${lesson.subjectSlug}`}>All {lesson.subject} lessons</Link>
        </p>
      </nav>
    </main>
  );
}

export function generateStaticParams() {
  return getAllLessonSlugs().map((slug) => ({ slug }));
}
