import type { ParsedLessonMarkdown } from "./frontmatter.js";

export interface SubjectCatalogMap {
  getCatalogForSubject(subject: string): string | undefined;
}

export function validateLessonCatalogMapping(
  lesson: ParsedLessonMarkdown,
  subjectCatalogMap: SubjectCatalogMap
): void {
  const expectedCatalog = subjectCatalogMap.getCatalogForSubject(lesson.frontmatter.subject);

  if (!expectedCatalog) {
    throw new Error(`Unknown subject: ${lesson.frontmatter.subject}`);
  }

  if (expectedCatalog !== lesson.frontmatter.catalog) {
    throw new Error(
      `Subject ${lesson.frontmatter.subject} belongs to catalog ${expectedCatalog}, not ${lesson.frontmatter.catalog}.`
    );
  }
}
