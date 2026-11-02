import assert from "node:assert/strict";
import test from "node:test";
import { mkdtempSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { VerticalFixture } from "./fixture.js";
import {
  CatalogLoadError,
  chunkPassages,
  htmlToPlainText,
  loadCatalogIntoFixture,
  manifestLessonToFixture,
  parseCatalogManifest
} from "./catalog.js";

function miniManifest() {
  return {
    subjects: [
      {
        slug: "photosynthesis-unit",
        name: "Photosynthesis Unit",
        catalog: "k12",
        lessonCount: 2,
        lessons: [
          { slug: "light-reactions", title: "Light Reactions", chapter: "1" },
          { slug: "calvin-cycle", title: "The Calvin Cycle", chapter: "2" }
        ]
      }
    ],
    lessons: {
      "light-reactions": {
        slug: "light-reactions",
        title: "Light Reactions",
        chapter: "1",
        subject: "Photosynthesis Unit",
        subjectSlug: "photosynthesis-unit",
        html: "<h1>Light Reactions</h1><p>Chlorophyll absorbs photons in the thylakoid membrane. This excites electrons that drive ATP synthesis.</p>",
        prevSlug: null,
        nextSlug: "calvin-cycle"
      },
      "calvin-cycle": {
        slug: "calvin-cycle",
        title: "The Calvin Cycle",
        chapter: "2",
        subject: "Photosynthesis Unit",
        subjectSlug: "photosynthesis-unit",
        html: "<p>The Calvin cycle fixes carbon dioxide into glucose using ATP and NADPH produced by the light reactions.</p>",
        prevSlug: "light-reactions",
        nextSlug: null
      }
    }
  };
}

test("htmlToPlainText strips tags and decodes entities", () => {
  const text = htmlToPlainText("<p>a&nbsp;&amp; b</p><div>c</div>");
  assert.equal(text, "a & b c");
});

test("chunkPassages produces deterministic ids", () => {
  const passages = chunkPassages("my-slug", "One sentence. Two sentence. Three sentence.");
  assert.ok(passages.length >= 1);
  assert.equal(passages[0]?.id, "my-slug#p0");
});

test("manifestLessonToFixture derives passages, concept, and prerequisite chain", () => {
  const { lesson, concept } = manifestLessonToFixture("calvin-cycle", miniManifest().lessons["calvin-cycle"]);
  assert.equal(lesson.id, "calvin-cycle");
  assert.equal(lesson.slug, "calvin-cycle");
  assert.deepEqual(lesson.prerequisiteLessonIds, ["light-reactions"]);
  assert.ok(lesson.passages.length >= 1);
  assert.equal(concept.id, "concept:calvin-cycle");
});

test("parseCatalogManifest rejects malformed shapes", () => {
  assert.throws(() => parseCatalogManifest({}), CatalogLoadError);
  assert.throws(() => parseCatalogManifest({ lessons: [] }), CatalogLoadError);
  assert.throws(() => parseCatalogManifest({ lessons: { x: { slug: "x" } } }), CatalogLoadError);
});

test("parseCatalogManifest enforces maxLessons", () => {
  const lessons: Record<string, unknown> = {};
  for (let i = 0; i < 5; i++) {
    lessons[`l${i}`] = { slug: `l${i}`, title: `L${i}`, html: "<p>x</p>" };
  }
  assert.throws(
    () => parseCatalogManifest({ lessons }, { maxBytes: 1e9, maxLessons: 2, maxPassagesPerLesson: 4, maxPassageChars: 100 }),
    CatalogLoadError
  );
});

test("loadCatalogIntoFixture registers real catalog lessons resolvable by slug", () => {
  const dir = mkdtempSync(path.join(tmpdir(), "catalog-"));
  const file = path.join(dir, "content.json");
  writeFileSync(file, JSON.stringify(miniManifest()), "utf8");
  try {
    const fixture = new VerticalFixture();
    const seedCount = fixture.lessonCount;
    const registered = loadCatalogIntoFixture(fixture, file);
    assert.equal(registered, 2);
    assert.equal(fixture.lessonCount, seedCount + 2);

    // Resolvable by the public catalog slug (what the UI passes).
    const lesson = fixture.getLesson("calvin-cycle");
    assert.ok(lesson);
    assert.equal(lesson?.title, "The Calvin Cycle");

    // Prerequisite chain resolves across slugs.
    const prereqs = fixture.getPrerequisites("calvin-cycle");
    assert.equal(prereqs[0]?.slug, "light-reactions");

    // Grounded search returns citations for a non-seed lesson.
    const hits = fixture.search("Calvin cycle carbon", "calvin-cycle");
    assert.ok(hits.length > 0);
    assert.equal(hits[0]?.lessonId, "calvin-cycle");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("loadCatalogIntoFixture rejects a relative path", () => {
  const fixture = new VerticalFixture();
  assert.throws(() => loadCatalogIntoFixture(fixture, "relative/content.json"), CatalogLoadError);
});
