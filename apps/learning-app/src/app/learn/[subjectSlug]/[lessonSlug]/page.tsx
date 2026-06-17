import { notFound } from "next/navigation";
import { getLesson, getSubjectBySlug, getAllLessonSlugs } from "../../../../lib/manifest";
import LessonClient from "./LessonClient";

interface Props {
  params: Promise<{ subjectSlug: string; lessonSlug: string }>;
}

const PROGRAMMING = /python|javascript|typescript|c\+\+|c#|rust|sql|programming|frontend|backend|devops|compiler|game dev|algorithm|web/i;

export default async function LessonPage({ params }: Props) {
  const { subjectSlug, lessonSlug } = await params;
  const lesson = getLesson(lessonSlug);
  const subject = getSubjectBySlug(subjectSlug);
  if (!lesson || !subject) notFound();

  const idx = subject.lessons.findIndex((l) => l.slug === lessonSlug);
  const progress = subject.lessonCount ? Math.round(((idx + 1) / subject.lessonCount) * 100) : 0;
  const upNext = subject.lessons
    .slice(idx + 1, idx + 4)
    .map((l) => ({ slug: l.slug, title: l.title, subjectSlug: subject.slug }));

  const next = lesson.nextSlug ? getLesson(lesson.nextSlug) : null;
  const nextHref = next ? `/learn/${next.subjectSlug}/${next.slug}` : `/learn/${subject.slug}`;
  const nextStepName = next ? next.title : "Subject complete";

  // Plain text for the Listen stage (strip rendered HTML tags).
  const textContent = lesson.html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();

  return (
    <LessonClient
      title={lesson.title}
      htmlContent={lesson.html}
      textContent={textContent}
      isProgramming={PROGRAMMING.test(lesson.subject)}
      nextHref={nextHref}
      nextStepName={nextStepName}
      nav={{
        currentSubject: { name: subject.name, slug: subject.slug, progress },
        upNext,
        catalogs: [
          { href: "/learn?catalog=k12", name: "K-12 Catalog" },
          { href: "/learn?catalog=advanced", name: "Advanced Track" },
        ],
      }}
    />
  );
}

export function generateStaticParams() {
  return getAllLessonSlugs().map((lessonSlug) => {
    const lesson = getLesson(lessonSlug)!;
    return { subjectSlug: lesson.subjectSlug, lessonSlug };
  });
}
