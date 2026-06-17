import type { Track, SubjectDetail, ChapterContent, DrillResponse } from "./types";

export async function fetchTracks(): Promise<Track[]> {
  const res = await fetch("/api/tracks");
  if (!res.ok) throw new Error(`Failed to fetch tracks: ${res.status}`);
  return res.json();
}

export async function fetchSubject(subjectId: string): Promise<SubjectDetail> {
  const res = await fetch(`/api/subject/${subjectId}`);
  if (!res.ok) throw new Error(`Failed to fetch subject ${subjectId}: ${res.status}`);
  return res.json();
}

export async function fetchChapter(subjectId: string, chapterNum: string): Promise<ChapterContent> {
  const res = await fetch(`/api/chapter/${subjectId}/${chapterNum}`);
  if (!res.ok) throw new Error(`Failed to fetch chapter ${chapterNum}: ${res.status}`);
  return res.json();
}

export async function postDrill(
  subjectId: string,
  chapterNum: string,
  count: number = 8,
  seed: number | null = null
): Promise<DrillResponse> {
  const res = await fetch("/api/drill", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ subject_id: subjectId, chapter_num: chapterNum, count, seed }),
  });
  if (!res.ok) throw new Error(`Failed to generate drill: ${res.status}`);
  return res.json();
}
