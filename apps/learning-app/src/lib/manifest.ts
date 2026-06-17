import { readFileSync } from "node:fs";
import path from "node:path";

export interface SubjectLessonRef {
  slug: string;
  title: string;
  chapter: string;
}

export interface SubjectSummary {
  slug: string;
  name: string;
  catalog: string;
  lessonCount: number;
  lessons: SubjectLessonRef[];
}

export interface ManifestLesson {
  slug: string;
  title: string;
  chapter: string;
  subject: string;
  subjectSlug: string;
  catalog: string;
  audienceTier: string;
  openSource: boolean;
  html: string;
  prevSlug: string | null;
  nextSlug: string | null;
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

export function getAllSubjectSlugs(): string[] {
  return subjects.map((s) => s.slug);
}

// Back-compat: some callers expect the full lesson list.
export async function getManifestLessons(): Promise<ManifestLesson[]> {
  return lessons;
}
