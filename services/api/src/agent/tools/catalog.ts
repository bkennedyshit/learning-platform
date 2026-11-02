import { readFileSync, statSync } from "node:fs";
import path from "node:path";
import type { FixtureConcept, FixtureLesson, VerticalFixture } from "./fixture.js";

/**
 * Safe loader that grounds the agent in the real generated catalog
 * (`content.json`) instead of only the two seed lessons.
 *
 * Trust boundary: the file path is supplied by service configuration
 * (`AGENT_CATALOG_PATH`), is required to be absolute, and is NEVER taken from
 * model output, tool input, or request bodies. The generated HTML is treated as
 * reviewed/trusted content (the same corpus the static site renders), so we
 * only convert it to plain text for grounding — we never execute it.
 */

/** Shape of a lesson entry inside the generated `content.json`. */
export interface CatalogManifestLesson {
  slug: string;
  title: string;
  chapter?: string;
  subject?: string;
  subjectSlug?: string;
  html: string;
  prevSlug?: string | null;
  nextSlug?: string | null;
}

export interface CatalogManifest {
  subjects?: unknown;
  lessons: Record<string, CatalogManifestLesson>;
}

export interface CatalogLoadLimits {
  /** Hard cap on the on-disk manifest size (defends against pathological files). */
  maxBytes: number;
  /** Hard cap on how many lessons we will register. */
  maxLessons: number;
  /** Max passages produced per lesson. */
  maxPassagesPerLesson: number;
  /** Max characters retained per passage chunk. */
  maxPassageChars: number;
}

export const DEFAULT_CATALOG_LIMITS: CatalogLoadLimits = {
  // The real generated content.json is ~120MB; allow generous headroom.
  maxBytes: 256 * 1024 * 1024,
  maxLessons: 5_000,
  maxPassagesPerLesson: 12,
  maxPassageChars: 600
};

export class CatalogLoadError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "CatalogLoadError";
  }
}

const PROGRAMMING =
  /python|javascript|typescript|c\+\+|c#|rust|sql|programming|frontend|backend|devops|compiler|game dev|algorithm|web/i;

const NAMED_ENTITIES: Record<string, string> = {
  amp: "&",
  lt: "<",
  gt: ">",
  quot: '"',
  apos: "'",
  nbsp: " ",
  "#39": "'",
  "#x27": "'",
  "#x2F": "/",
  "#47": "/"
};

/** Convert trusted generated HTML to normalized plain text (never executed). */
export function htmlToPlainText(html: string): string {
  return html
    // Drop whole script/style blocks defensively even though the corpus is trusted.
    .replace(/<(script|style)[\s\S]*?<\/\1>/gi, " ")
    // Turn block boundaries into spaces so words do not run together.
    .replace(/<\/(p|div|li|h[1-6]|br|tr|section|article)>/gi, " ")
    .replace(/<br\s*\/?>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&([a-z0-9#x]+);/gi, (whole, code: string) => {
      const key = code.toLowerCase();
      if (key in NAMED_ENTITIES) return NAMED_ENTITIES[key] as string;
      const num = /^#x([0-9a-f]+)$/i.exec(code);
      if (num) return String.fromCodePoint(parseInt(num[1] as string, 16));
      const dec = /^#(\d+)$/.exec(code);
      if (dec) return String.fromCodePoint(parseInt(dec[1] as string, 10));
      return " ";
    })
    .replace(/\s+/g, " ")
    .trim();
}

/**
 * Produce deterministic passage chunks with stable ids of the form
 * `${slug}#p{n}`. Chunking splits on sentence boundaries and greedily packs up
 * to {@link CatalogLoadLimits.maxPassageChars} characters per chunk so citations
 * point at meaningful, reproducible spans.
 */
export function chunkPassages(
  slug: string,
  text: string,
  limits: CatalogLoadLimits = DEFAULT_CATALOG_LIMITS
): Array<{ id: string; text: string }> {
  if (!text) return [];
  const sentences = text.match(/[^.!?]+[.!?]+|\S[^.!?]*$/g) ?? [text];
  const chunks: string[] = [];
  let current = "";
  for (const raw of sentences) {
    const sentence = raw.trim();
    if (!sentence) continue;
    if (current.length === 0) {
      current = sentence;
    } else if (current.length + 1 + sentence.length <= limits.maxPassageChars) {
      current = `${current} ${sentence}`;
    } else {
      chunks.push(current);
      current = sentence;
    }
    if (chunks.length >= limits.maxPassagesPerLesson) break;
  }
  if (current && chunks.length < limits.maxPassagesPerLesson) {
    chunks.push(current);
  }
  return chunks
    .slice(0, limits.maxPassagesPerLesson)
    .map((chunk, index) => ({ id: `${slug}#p${index}`, text: chunk.slice(0, limits.maxPassageChars) }));
}

/** Deterministic concept id derived from a lesson slug. */
export function conceptIdForLesson(slug: string): string {
  return `concept:${slug}`;
}

/**
 * Convert one manifest lesson into a {@link FixtureLesson} plus its derived
 * {@link FixtureConcept}. Prerequisite references use the previous lesson slug
 * (the fixture resolves references by id or slug), and next/prev chaining mirrors
 * the catalog ordering.
 */
export function manifestLessonToFixture(
  slug: string,
  lesson: CatalogManifestLesson,
  limits: CatalogLoadLimits = DEFAULT_CATALOG_LIMITS
): { lesson: FixtureLesson; concept: FixtureConcept } {
  const text = htmlToPlainText(lesson.html ?? "");
  const passages = chunkPassages(slug, text, limits);
  const conceptId = conceptIdForLesson(slug);
  const subjectId = lesson.subjectSlug || lesson.subject || "catalog";
  const prerequisiteLessonIds = lesson.prevSlug ? [lesson.prevSlug] : [];
  const fixtureLesson: FixtureLesson = {
    id: slug,
    subjectId,
    slug,
    title: lesson.title || slug,
    body: text,
    conceptIds: [conceptId],
    prerequisiteLessonIds,
    passages,
    isProgrammingSubject: PROGRAMMING.test(lesson.subject || subjectId)
  };
  const concept: FixtureConcept = {
    id: conceptId,
    name: lesson.title || slug,
    summary: passages[0]?.text ?? text.slice(0, limits.maxPassageChars)
  };
  return { lesson: fixtureLesson, concept };
}

/** Validate the parsed manifest shape and lesson count. Throws on invalid input. */
export function parseCatalogManifest(raw: unknown, limits: CatalogLoadLimits = DEFAULT_CATALOG_LIMITS): CatalogManifest {
  if (!raw || typeof raw !== "object") {
    throw new CatalogLoadError("catalog manifest must be a JSON object");
  }
  const lessons = (raw as { lessons?: unknown }).lessons;
  if (!lessons || typeof lessons !== "object" || Array.isArray(lessons)) {
    throw new CatalogLoadError("catalog manifest must have a `lessons` object keyed by slug");
  }
  const entries = Object.entries(lessons as Record<string, unknown>);
  if (entries.length === 0) {
    throw new CatalogLoadError("catalog manifest contains no lessons");
  }
  if (entries.length > limits.maxLessons) {
    throw new CatalogLoadError(`catalog manifest exceeds maxLessons (${entries.length} > ${limits.maxLessons})`);
  }
  for (const [slug, value] of entries) {
    if (!value || typeof value !== "object") {
      throw new CatalogLoadError(`lesson ${slug} is not an object`);
    }
    const l = value as Record<string, unknown>;
    if (typeof l.slug !== "string" || typeof l.title !== "string" || typeof l.html !== "string") {
      throw new CatalogLoadError(`lesson ${slug} is missing string slug/title/html`);
    }
  }
  return raw as CatalogManifest;
}

/** Register every manifest lesson into the fixture. Returns the number registered. */
export function registerCatalog(
  fixture: VerticalFixture,
  manifest: CatalogManifest,
  limits: CatalogLoadLimits = DEFAULT_CATALOG_LIMITS
): number {
  let count = 0;
  for (const [slug, lesson] of Object.entries(manifest.lessons)) {
    const { lesson: fixtureLesson, concept } = manifestLessonToFixture(slug, lesson, limits);
    fixture.registerConcept(concept);
    fixture.registerLesson(fixtureLesson);
    count += 1;
  }
  return count;
}

/**
 * Read, validate, and register a catalog manifest from an absolute file path.
 * The path must be absolute service configuration; a relative path is rejected
 * so model/UI input can never redirect the loader.
 */
export function loadCatalogIntoFixture(
  fixture: VerticalFixture,
  absolutePath: string,
  limits: CatalogLoadLimits = DEFAULT_CATALOG_LIMITS
): number {
  if (!path.isAbsolute(absolutePath)) {
    throw new CatalogLoadError(`AGENT_CATALOG_PATH must be an absolute path, received: ${absolutePath}`);
  }
  let stats;
  try {
    stats = statSync(absolutePath);
  } catch (err) {
    throw new CatalogLoadError(`cannot read catalog at ${absolutePath}: ${(err as Error).message}`);
  }
  if (!stats.isFile()) {
    throw new CatalogLoadError(`AGENT_CATALOG_PATH is not a file: ${absolutePath}`);
  }
  if (stats.size > limits.maxBytes) {
    throw new CatalogLoadError(`catalog file exceeds maxBytes (${stats.size} > ${limits.maxBytes})`);
  }
  let parsed: unknown;
  try {
    parsed = JSON.parse(readFileSync(absolutePath, "utf8"));
  } catch (err) {
    throw new CatalogLoadError(`catalog at ${absolutePath} is not valid JSON: ${(err as Error).message}`);
  }
  const manifest = parseCatalogManifest(parsed, limits);
  return registerCatalog(fixture, manifest, limits);
}
