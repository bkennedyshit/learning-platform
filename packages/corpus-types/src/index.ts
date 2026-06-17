export type EntityId = string;

export type CatalogKey = "k12" | "advanced";

export interface Catalog {
  id: EntityId;
  key: CatalogKey;
  name: string;
  description?: string;
}

export type AudienceTier =
  | "k-5"
  | "6-8"
  | "9-12"
  | "higher-education"
  | "advanced-personal";

export interface Subject {
  id: EntityId;
  catalogId: EntityId;
  name: string;
  slug: string;
  audienceTier: AudienceTier;
  isProgramming: boolean;
  generatorSupported: boolean;
}

export interface LessonFrontmatter {
  chapter: string;
  previousLessonId?: EntityId;
  nextLessonId?: EntityId;
  objectives: string[];
  epigraph?: string;
  crossLinkIds: EntityId[];
}

export interface Lesson {
  id: EntityId;
  subjectId: EntityId;
  audienceTier: AudienceTier;
  slug: string;
  title: string;
  frontmatter: LessonFrontmatter;
  bodyRef: string;
  openSource: boolean;
  updatedAt: string;
}

export interface CrossLink {
  lessonId: EntityId;
  targetLessonId: EntityId;
}

export interface LessonChunk {
  id: EntityId;
  lessonId: EntityId;
  chunkIndex: number;
  text: string;
}

export interface LearningPath {
  id: EntityId;
  catalogId: EntityId;
  name: string;
  slug: string;
  audienceTier: AudienceTier;
  isPurchasable: boolean;
}

export type PathItemKind = "subject" | "lesson";

export interface PathItem {
  id: EntityId;
  pathId: EntityId;
  position: number;
  kind: PathItemKind;
  subjectId?: EntityId;
  lessonId?: EntityId;
}

export type PracticeProblemTier = "easy" | "medium" | "hard" | "exam";

export type PracticeProblemSource = "authored" | "generated";

export interface PracticeProblem {
  id: EntityId;
  subjectId: EntityId;
  lessonId?: EntityId;
  tier: PracticeProblemTier;
  prompt: string;
  solution: string;
  source: PracticeProblemSource;
}

export interface PathEnrollment {
  id: EntityId;
  accountId: EntityId;
  pathId: EntityId;
  currentPosition: number;
  completedCount: number;
}
