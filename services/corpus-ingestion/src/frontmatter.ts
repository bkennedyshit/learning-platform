import type { AudienceTier, CatalogKey } from "@learning-platform/corpus-types";

export interface ParsedLessonMarkdown {
  frontmatter: LessonFrontmatterFields;
  body: string;
}

export interface LessonFrontmatterFields {
  title: string;
  subject: string;
  catalog: CatalogKey;
  audienceTier: AudienceTier;
  chapter: string;
  previous?: string;
  next?: string;
  objectives: string[];
  epigraph?: string;
  crossLinks: string[];
  openSource: boolean;
}

type RawFrontmatter = Record<string, string | string[] | boolean>;

export function parseLessonMarkdown(markdown: string): ParsedLessonMarkdown {
  const normalized = markdown.replace(/\r\n/g, "\n");
  if (!normalized.startsWith("---\n")) {
    throw new Error("Lesson markdown must start with frontmatter.");
  }

  const end = normalized.indexOf("\n---\n", 4);
  if (end === -1) {
    throw new Error("Lesson frontmatter must be closed with ---.");
  }

  const frontmatterText = normalized.slice(4, end);
  const body = normalized.slice(end + 5).trim();

  return {
    frontmatter: normalizeFrontmatter(parseYamlSubset(frontmatterText)),
    body
  };
}

function parseYamlSubset(source: string): RawFrontmatter {
  const result: RawFrontmatter = {};
  const lines = source.split("\n");
  let index = 0;

  while (index < lines.length) {
    const line = lines[index] ?? "";
    index += 1;

    if (!line.trim()) {
      continue;
    }

    const match = /^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$/.exec(line);
    if (!match) {
      throw new Error(`Invalid frontmatter line: ${line}`);
    }

    const key = match[1];
    const value = match[2] ?? "";
    if (!key) {
      throw new Error(`Invalid frontmatter line: ${line}`);
    }

    if (value === undefined || value.length === 0) {
      const values: string[] = [];
      while (index < lines.length && /^\s+-\s+/.test(lines[index] ?? "")) {
        values.push(unquote((lines[index] ?? "").replace(/^\s+-\s+/, "")));
        index += 1;
      }
      result[toCamelKey(key)] = values;
      continue;
    }

    result[toCamelKey(key)] = parseScalar(value);
  }

  return result;
}

function normalizeFrontmatter(raw: RawFrontmatter): LessonFrontmatterFields {
  const title = requireString(raw.title, "title");
  const subject = requireString(raw.subject, "subject");
  const catalog = requireCatalog(raw.catalog);
  const audienceTier = requireAudienceTier(raw.audienceTier);
  const chapter = requireString(raw.chapter, "chapter");

  return {
    title,
    subject,
    catalog,
    audienceTier,
    chapter,
    previous: optionalString(raw.previous),
    next: optionalString(raw.next),
    objectives: requireStringArray(raw.objectives, "objectives"),
    epigraph: optionalString(raw.epigraph),
    crossLinks: optionalStringArray(raw.crossLinks),
    openSource: Boolean(raw.openSource)
  };
}

function parseScalar(value: string): string | boolean | string[] {
  const trimmed = value.trim();
  if (trimmed === "true") {
    return true;
  }
  if (trimmed === "false") {
    return false;
  }
  if (trimmed.startsWith("[") && trimmed.endsWith("]")) {
    const inner = trimmed.slice(1, -1).trim();
    return inner ? inner.split(",").map((item) => unquote(item.trim())) : [];
  }
  return unquote(trimmed);
}

function requireString(value: unknown, key: string): string {
  if (typeof value !== "string" || value.trim().length === 0) {
    throw new Error(`Frontmatter field ${key} is required.`);
  }
  return value.trim();
}

function optionalString(value: unknown): string | undefined {
  return typeof value === "string" && value.trim().length > 0 ? value.trim() : undefined;
}

function requireStringArray(value: unknown, key: string): string[] {
  if (!Array.isArray(value) || value.length === 0 || value.some((item) => typeof item !== "string")) {
    throw new Error(`Frontmatter field ${key} must be a non-empty string array.`);
  }
  return value.map((item) => item.trim());
}

function optionalStringArray(value: unknown): string[] {
  if (!value) {
    return [];
  }
  if (!Array.isArray(value) || value.some((item) => typeof item !== "string")) {
    throw new Error("Frontmatter field crossLinks must be a string array when present.");
  }
  return value.map((item) => item.trim()).filter(Boolean);
}

function requireCatalog(value: unknown): CatalogKey {
  if (value === "k12" || value === "advanced") {
    return value;
  }
  throw new Error("Frontmatter field catalog must be k12 or advanced.");
}

function requireAudienceTier(value: unknown): AudienceTier {
  if (
    value === "k-5" ||
    value === "6-8" ||
    value === "9-12" ||
    value === "higher-education" ||
    value === "advanced-personal"
  ) {
    return value;
  }
  throw new Error("Frontmatter field audienceTier is invalid.");
}

function toCamelKey(key: string): string {
  return key.replace(/[_-]([a-z])/g, (_match, letter: string) => letter.toUpperCase());
}

function unquote(value: string): string {
  return value.replace(/^["']|["']$/g, "");
}
