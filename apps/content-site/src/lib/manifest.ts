import { readFileSync } from "node:fs";
import path from "node:path";

export interface SubjectLessonRef {
  slug: string;
  title: string;
  chapter: string;
  indexable: boolean;
}

export interface SubjectSummary {
  slug: string;
  name: string;
  catalog: string;
  lessonCount: number;
  /** Lessons that pass the index-promotion gate (see generate-content.mjs). */
  indexableLessonCount: number;
  /** A hub is indexable only when it links to at least one indexable lesson. */
  indexable: boolean;
  lessons: SubjectLessonRef[];
}

export type NoindexReason = "placeholder" | "scaffold" | "thin";

export interface ManifestLesson {
  slug: string;
  title: string;
  chapter: string;
  subject: string;
  subjectSlug: string;
  catalog: string;
  audienceTier: string;
  openSource: boolean;
  /** First substantial paragraph of the lesson, used as the meta description. */
  description: string | null;
  wordCount: number;
  /** Passed the index-promotion gate: robots index + listed in the sitemap. */
  indexable: boolean;
  noindexReason: NoindexReason | null;
  html: string;
  prevSlug: string | null;
  nextSlug: string | null;
  /** Nearby indexable lessons in the same subject (excludes prev/next). */
  relatedSlugs: string[];
}

interface ContentData {
  subjects: SubjectSummary[];
  lessons: Record<string, ManifestLesson>;
}

const data = JSON.parse(
  readFileSync(path.join(process.cwd(), "src/generated/content.json"), "utf8")
) as ContentData;

export const subjects: SubjectSummary[] = data.subjects;
export const lessonsBySlug: Record<string, ManifestLesson> = data.lessons;
export const lessons: ManifestLesson[] = Object.values(data.lessons);

export function getSubjects(): SubjectSummary[] {
  return subjects;
}

export function getSubjectBySlug(slug: string): SubjectSummary | undefined {
  return subjects.find((s) => s.slug === slug);
}

export function getLesson(slug: string): ManifestLesson | undefined {
  return lessonsBySlug[slug];
}

export function getAllLessonSlugs(): string[] {
  return Object.keys(lessonsBySlug);
}

/** Lessons that should be offered to search engines (sitemap + index). */
export function getIndexableLessonSlugs(): string[] {
  return lessons.filter((l) => l.indexable).map((l) => l.slug);
}

export function getAllSubjectSlugs(): string[] {
  return subjects.map((s) => s.slug);
}

export function getIndexableSubjectSlugs(): string[] {
  return subjects.filter((s) => s.indexable).map((s) => s.slug);
}

// Back-compat: some callers expect the full lesson list.
export async function getManifestLessons(): Promise<ManifestLesson[]> {
  return lessons;
}
