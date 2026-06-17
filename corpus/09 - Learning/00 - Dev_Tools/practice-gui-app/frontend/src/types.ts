export interface ChapterMeta {
  num: string;
  title: string;
  filename: string;
  script_filename: string | null;
}

export interface SubjectSummary {
  id: string;
  name: string;
  chapter_count: number;
}

export interface Track {
  track: string;
  subjects: SubjectSummary[];
}

export interface SubjectDetail {
  id: string;
  track: string;
  name: string;
  chapters: ChapterMeta[];
}

export interface ChapterContent {
  num: string;
  title: string;
  markdown: string;
  frontmatter: Record<string, unknown>;
}

export interface DrillResponse {
  subject_id: string;
  chapter_num: string;
  seed: number;
  markdown: string;
}
