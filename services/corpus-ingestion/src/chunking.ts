export interface LessonChunkInput {
  lessonId: string;
  body: string;
  maxCharacters?: number;
  overlapCharacters?: number;
}

export interface PreparedLessonChunk {
  lessonId: string;
  chunkIndex: number;
  text: string;
}

export function chunkLessonBody(input: LessonChunkInput): PreparedLessonChunk[] {
  const maxCharacters = input.maxCharacters ?? 2200;
  const overlapCharacters = input.overlapCharacters ?? 200;
  const sections = splitByHeadings(input.body);
  const chunks: PreparedLessonChunk[] = [];
  let buffer = "";

  for (const section of sections) {
    if (`${buffer}\n\n${section}`.trim().length <= maxCharacters) {
      buffer = `${buffer}\n\n${section}`.trim();
      continue;
    }

    if (buffer) {
      chunks.push(toChunk(input.lessonId, chunks.length, buffer));
      buffer = tail(buffer, overlapCharacters);
    }

    if (section.length > maxCharacters) {
      for (const part of splitLongText(section, maxCharacters, overlapCharacters)) {
        chunks.push(toChunk(input.lessonId, chunks.length, part));
      }
      buffer = "";
      continue;
    }

    buffer = `${buffer}\n\n${section}`.trim();
  }

  if (buffer) {
    chunks.push(toChunk(input.lessonId, chunks.length, buffer));
  }

  return chunks;
}

function splitByHeadings(body: string): string[] {
  const lines = body.split("\n");
  const sections: string[] = [];
  let current: string[] = [];

  for (const line of lines) {
    if (/^#{1,6}\s+/.test(line) && current.length > 0) {
      sections.push(current.join("\n").trim());
      current = [line];
      continue;
    }

    current.push(line);
  }

  if (current.length > 0) {
    sections.push(current.join("\n").trim());
  }

  return sections.filter(Boolean);
}

function splitLongText(text: string, maxCharacters: number, overlapCharacters: number): string[] {
  const chunks: string[] = [];
  let start = 0;

  while (start < text.length) {
    chunks.push(text.slice(start, start + maxCharacters).trim());
    start += maxCharacters - overlapCharacters;
  }

  return chunks.filter(Boolean);
}

function toChunk(lessonId: string, chunkIndex: number, text: string): PreparedLessonChunk {
  return { lessonId, chunkIndex, text };
}

function tail(text: string, characters: number): string {
  return text.slice(Math.max(0, text.length - characters));
}
