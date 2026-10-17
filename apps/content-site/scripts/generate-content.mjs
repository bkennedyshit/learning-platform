// Generate content-site data from the recovered corpus.
//
// Reads corpus/lessons/*.md (single clean frontmatter block after recovery),
// keeps teachable lesson types, groups by subject, renders markdown + KaTeX math
// to HTML, resolves image/SVG assets into public/lesson-assets, and writes
// src/generated/content.json consumed by the site.
//
// Run from apps/content-site:  node scripts/generate-content.mjs

import { readdir, readFile, mkdir, writeFile, copyFile, stat } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { marked } from "marked";
import markedKatex from "marked-katex-extension";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const appDir = path.resolve(__dirname, "..");
const corpusRoot = path.resolve(appDir, "../../corpus");
const lessonsDir = path.resolve(corpusRoot, "lessons");
const outFile = path.resolve(appDir, "src/generated/content.json");
const assetsOutDir = path.resolve(appDir, "public/lesson-assets");

const LESSON_TYPES = new Set(["chapter", "chapter-note", "experiment-chapter"]);

marked.use(markedKatex({ throwOnError: false, strict: "ignore", nonStandard: true, output: "html" }));
marked.setOptions({ gfm: true, breaks: false });

// Emit ```mermaid fenced blocks as <pre class="mermaid"> so the client can
// render them as diagrams; all other code blocks render normally.
function escapeHtml(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
marked.use({
  renderer: {
    code(token) {
      const text = typeof token === "string" ? token : token.text;
      const rawLang = typeof token === "string" ? arguments[1] : token.lang;
      const lang = (rawLang || "").trim().split(/\s+/)[0];
      if (lang === "mermaid") {
        return `<pre class="mermaid">${escapeHtml(text)}</pre>`;
      }
      const cls = lang ? ` class="language-${lang}"` : "";
      return `<pre><code${cls}>${escapeHtml(text)}\n</code></pre>`;
    },
  },
});

// ---- Asset index: basename(lower) -> absolute path -------------------------
const IMG_EXT = new Set([".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp"]);
const assetIndex = new Map();

async function indexAssets(dir) {
  let entries;
  try {
    entries = await readdir(dir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      await indexAssets(full);
    } else if (IMG_EXT.has(path.extname(e.name).toLowerCase())) {
      const key = e.name.toLowerCase();
      if (!assetIndex.has(key)) assetIndex.set(key, full);
    }
  }
}

const copiedAssets = new Set();
const skippedAssets = new Set();
async function resolveAsset(ref) {
  // ref may be a path or bare filename, possibly URL-encoded.
  const base = decodeURIComponent(ref.split("/").pop().split("\\").pop()).trim();
  const hit = assetIndex.get(base.toLowerCase());
  if (!hit) return null;
  if (skippedAssets.has(base)) return null;
  // Drop SVG placeholders that rely on Obsidian theme CSS variables — those
  // vars are undefined on the web, so every fill resolves to black (a black box).
  if (base.toLowerCase().endsWith(".svg")) {
    const txt = await readFile(hit, "utf8");
    if (txt.includes("var(--")) {
      skippedAssets.add(base);
      return null;
    }
  }
  if (!copiedAssets.has(base)) {
    await mkdir(assetsOutDir, { recursive: true });
    await copyFile(hit, path.join(assetsOutDir, base));
    copiedAssets.add(base);
  }
  return `/lesson-assets/${base}`;
}

// Rewrite markdown image refs to resolved public paths; drop unresolved ones.
async function rewriteImages(md) {
  const imgRe = /!\[([^\]]*)\]\(([^)]+)\)/g;
  let out = "";
  let last = 0;
  let m;
  while ((m = imgRe.exec(md)) !== null) {
    out += md.slice(last, m.index);
    last = imgRe.lastIndex;
    const resolved = await resolveAsset(m[2]);
    out += resolved ? `![${m[1]}](${resolved})` : ""; // drop if asset missing
  }
  out += md.slice(last);
  return out;
}

// Strip Obsidian callout markers ("> [!info]+ Title" -> "> Title") and the
// internal Subject_Plan/Index backlinks that point nowhere on the site.
function cleanMarkdown(md) {
  return md
    .replace(/^>\s*\[!(\w+)\][-+]?\s*/gm, "> ")
    .replace(/^\*Back to \[.*$/gm, "")
    .replace(/\[\[[^\]]*\]\]/g, ""); // any leftover raw wikilinks
}

function slugify(s) {
  return String(s)
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/&/g, " and ")
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/[\s_-]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function cleanSubject(s) {
  if (!s) return null;
  if (s.startsWith("_")) return null;
  const noise = new Set([
    "scripts", "Code Snippets", "Learning", "Learning App Material",
    "Math and Physics", "practice-gui-app", "2 & HTTP", "Grade Band Pipelines",
    "99_Snippets",
  ]);
  if (noise.has(s)) return null;
  const name = s.replace(/^\d+[_-]\s*/, "").replace(/_/g, " ").trim();
  return name || null;
}

function orderKey(file, chapter) {
  const mApp = /^app-(\d+)/.exec(file);
  if (mApp) return Number(mApp[1]);
  const mNum = /^(\d+)(?:-(\d+))?-/.exec(file);
  if (mNum) return Number(mNum[1]) * 1000 + (mNum[2] ? Number(mNum[2]) : 0);
  const ch = Number(String(chapter).replace(/[^\d.]/g, ""));
  return Number.isFinite(ch) ? ch * 100000 : 9e9;
}

function parseFrontmatter(raw) {
  const c = raw.replace(/\r\n/g, "\n");
  if (!c.startsWith("---\n")) return null;
  const end = c.indexOf("\n---\n", 4);
  if (end === -1) return null;
  const block = c.slice(4, end);
  const body = c.slice(end + 5).replace(/^\n+/, "");
  const fm = {};
  for (const line of block.split("\n")) {
    const m = /^([A-Za-z_][A-Za-z0-9_-]*):[ \t]*(.*)$/.exec(line);
    if (m && m[2] !== "") fm[m[1]] = m[2].trim().replace(/^["']|["']$/g, "");
  }
  return { fm, body };
}

// ---- Index-promotion gate ----------------------------------------------------
// A lesson is only offered to search engines (robots index + sitemap) when it
// is finished content. Everything below is derived from the corpus itself:
//
//  * placeholder - the authoring stub markers ("Ready for expansion" chapter
//                  goal and "TODO: Expand/Add" sections) are still present.
//  * scaffold    - the body is the generic grade-band template that was
//                  generated for every chapter before real content was written
//                  ("Primary Element: The foundational building block of this
//                  unit" + "System Overlay"). These pages are near-identical
//                  across subjects, which is exactly what Google reports as
//                  "Crawled - currently not indexed".
//  * thin        - fewer than MIN_INDEXABLE_WORDS words of rendered prose.
//
// Non-indexable lessons are still published and linked (noindex,follow) so
// readers can use them; they rejoin the sitemap automatically once rewritten.
const MIN_INDEXABLE_WORDS = 400;

function htmlToText(html) {
  return html
    .replace(/<(script|style|math)\b[\s\S]*?<\/\1>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&[a-z#0-9]+;/gi, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function countWords(text) {
  return text.split(/\s+/).filter((w) => /[A-Za-z0-9\u00C0-\uFFFF]/.test(w)).length;
}

function assessLesson(html) {
  const text = htmlToText(html);
  const wordCount = countWords(text);
  const placeholder = /Ready for expansion/i.test(text) || /TODO:\s*(Expand|Add)\b/i.test(text);
  const scaffold =
    /The foundational building block of this unit/i.test(text) && /System Overlay/i.test(text);
  let noindexReason = null;
  if (placeholder) noindexReason = "placeholder";
  else if (scaffold) noindexReason = "scaffold";
  else if (wordCount < MIN_INDEXABLE_WORDS) noindexReason = "thin";
  return { wordCount, indexable: noindexReason === null, noindexReason };
}

// Meta description from the lesson's own first substantial paragraph, so each
// page has a distinct snippet instead of one templated sentence site-wide.
function extractDescription(html) {
  for (const m of html.matchAll(/<p>([\s\S]*?)<\/p>/g)) {
    const text = htmlToText(m[1]);
    if (text.length < 60) continue;
    if (/^(Chapter goal|By the end of this chapter)/i.test(text)) continue;
    if (text.length <= 160) return text;
    const cut = text.slice(0, 157);
    return `${cut.slice(0, cut.lastIndexOf(" ") > 100 ? cut.lastIndexOf(" ") : 157)}…`;
  }
  return null;
}

// ---- Local link resolution ---------------------------------------------------
// Corpus lessons cross-reference each other with Obsidian-style relative links
// ("2.6---Eigenvalues-Eigenvectors-&-Diagonalization", "Subject_Plan",
// "README"). Rendered verbatim they resolve to /<target> on the site and 404.
// Each is rewritten to the canonical lesson route, to the subject hub for
// subject-plan style documents, or reduced to plain text when nothing public
// corresponds to it.
function safeDecode(value) {
  try {
    return decodeURIComponent(value);
  } catch {
    return value;
  }
}

function decodeEntities(s) {
  return s.replace(/&amp;/g, "&").replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, "<").replace(/&gt;/g, ">");
}

function looseKey(value, ampersand = "") {
  return String(value)
    .replace(/\.md$/i, "")
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/&/g, ampersand)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "");
}

function stripChapterPrefix(value) {
  return String(value).replace(/^\s*(?:app-)?\d+(?:\.\d+)*\s*[—–:\-\s]+/i, "");
}

const SUBJECT_DOC_KEYS = new Set(["subjectplan", "learningpath", "readme"]);

function addUnique(map, key, value) {
  if (!key) return;
  if (!map.has(key)) map.set(key, value);
  else if (map.get(key) !== value) map.set(key, null); // ambiguous -> never used
}

function buildLinkIndex(sources) {
  const exact = new Map();
  const body = new Map();
  for (const s of sources) {
    const heading = (/^#\s+(.+)$/m.exec(s.body)?.[1] ?? "").replace(/[*_`]/g, "");
    const names = [s.file, s.slug, s.fm.title || "", heading].filter(Boolean);
    for (const name of names) {
      addUnique(exact, looseKey(name), s.slug);
      addUnique(exact, looseKey(name, "and"), s.slug);
      const bodyKey = looseKey(stripChapterPrefix(name));
      if (bodyKey.length >= 10) addUnique(body, bodyKey, s.slug);
    }
  }
  return { exact, body };
}

function resolveLocalTarget(target, index, subjectSlug) {
  const basename = target.replace(/\\/g, "/").replace(/\/+$/, "").split("/").pop();
  if (!basename) return null;
  const key = looseKey(basename);
  if (SUBJECT_DOC_KEYS.has(key)) return `/subject/${subjectSlug}`;
  const exact = index.exact.get(key) ?? index.exact.get(looseKey(basename, "and"));
  if (exact) return `/${exact}`;
  const bodyKey = looseKey(stripChapterPrefix(basename));
  const byBody = bodyKey.length >= 10 ? index.body.get(bodyKey) : null;
  return byBody ? `/${byBody}` : null;
}

const linkStats = { rewritten: 0, toHub: 0, unlinked: 0 };

function rewriteLocalLinks(html, index, subjectSlug) {
  return html.replace(/<a href="([^"]*)"([^>]*)>([\s\S]*?)<\/a>/g, (full, rawHref, attrs, inner) => {
    const href = decodeEntities(rawHref);
    if (/^(?:[a-z][a-z0-9+.-]*:|\/\/|#|\/)/i.test(href)) return full;
    const suffixAt = href.search(/[?#]/);
    const target = safeDecode(suffixAt === -1 ? href : href.slice(0, suffixAt));
    const fragment = suffixAt === -1 ? "" : href.slice(suffixAt);
    const resolved = resolveLocalTarget(target, index, subjectSlug);
    if (!resolved) {
      linkStats.unlinked++;
      return inner;
    }
    if (resolved.startsWith("/subject/")) linkStats.toHub++;
    else linkStats.rewritten++;
    return `<a href="${resolved}${fragment.startsWith("#") ? fragment : ""}"${attrs}>${inner}</a>`;
  });
}

function assertInternalLinks(subjects, lessons) {
  const known = new Set(["/", "/resources", "/tools"]);
  for (const s of subjects) known.add(`/subject/${s.slug}`);
  for (const slug of Object.keys(lessons)) known.add(`/${slug}`);
  const bad = [];
  for (const l of Object.values(lessons)) {
    for (const m of l.html.matchAll(/<a\b[^>]*\bhref="([^"]*)"/g)) {
      const href = decodeEntities(m[1]);
      if (/^(?:[a-z][a-z0-9+.-]*:|\/\/|#)/i.test(href)) continue;
      const p = href.split(/[?#]/)[0];
      if (!known.has(p)) bad.push(`${l.slug} -> ${href}`);
    }
  }
  if (bad.length) {
    throw new Error(`Unresolved internal lesson links (${bad.length}):\n${bad.slice(0, 20).join("\n")}`);
  }
}

// C# and C++ both slugify to "c"; give them distinct, readable hub URLs.
const SUBJECT_SLUG_OVERRIDES = new Map([
  ["C#", "c-sharp"],
  ["C++", "cpp"],
]);
const subjectSlugFor = (name) => SUBJECT_SLUG_OVERRIDES.get(name) ?? slugify(name);

const RELATED_LESSON_COUNT = 4;

// ---- Main ------------------------------------------------------------------
await indexAssets(corpusRoot);
console.log(`Indexed ${assetIndex.size} asset files.`);

const files = (await readdir(lessonsDir)).filter((f) => f.endsWith(".md"));
const sources = [];
let skipped = 0;

// Pass 1: select teachable lessons so every final route is known before any
// cross-reference is rewritten.
for (const file of files) {
  const raw = await readFile(path.join(lessonsDir, file), "utf8");
  const parsed = parseFrontmatter(raw);
  if (!parsed) { skipped++; continue; }
  const { fm, body } = parsed;

  // Keep only teachable lessons. Files with no type default to "chapter";
  // files with an explicit non-lesson type (subject-plan, learning-path,
  // readme, index, note, ...) are excluded.
  const type = fm.type || "chapter";
  if (!LESSON_TYPES.has(type)) { skipped++; continue; }

  const subjectName = cleanSubject(fm.subject);
  if (!subjectName) { skipped++; continue; }

  sources.push({ file, fm, body, subjectName, slug: slugify(file.replace(/\.md$/, "")) });
}

const slugOwners = new Map();
for (const s of sources) {
  if (slugOwners.has(s.slug)) {
    throw new Error(`Duplicate lesson slug "${s.slug}" from ${slugOwners.get(s.slug)} and ${s.file}`);
  }
  slugOwners.set(s.slug, s.file);
}
const linkIndex = buildLinkIndex(sources);

// Pass 2: render, fix cross-references, and assess index eligibility.
const lessonsBySubject = new Map();
for (const { file, fm, body, subjectName, slug } of sources) {
  const cleaned = cleanMarkdown(body);
  const withImages = await rewriteImages(cleaned);
  const html = rewriteLocalLinks(marked.parse(withImages), linkIndex, subjectSlugFor(subjectName));
  const assessment = assessLesson(html);

  const lesson = {
    slug,
    title: fm.title || slug,
    chapter: fm.chapter || "",
    catalog: fm.catalog === "advanced" ? "advanced" : "k12",
    audienceTier: fm.audience_tier || (fm.catalog === "advanced" ? "higher-education" : "9-12"),
    openSource: true,
    order: orderKey(file, fm.chapter),
    description: extractDescription(html),
    ...assessment,
    html,
  };

  if (!lessonsBySubject.has(subjectName)) lessonsBySubject.set(subjectName, []);
  lessonsBySubject.get(subjectName).push(lesson);
}

// Nearest indexable siblings in course order, excluding the lesson itself and
// its prev/next (already linked separately).
function relatedFor(list, i) {
  const exclude = new Set([list[i].slug, list[i - 1]?.slug, list[i + 1]?.slug]);
  return list
    .map((l, j) => ({ l, d: Math.abs(j - i), j }))
    .filter(({ l }) => l.indexable && !exclude.has(l.slug))
    .sort((a, b) => a.d - b.d || a.j - b.j)
    .slice(0, RELATED_LESSON_COUNT)
    .sort((a, b) => a.j - b.j)
    .map(({ l }) => l.slug);
}

const subjects = [];
const lessons = {};
const subjectSlugOwners = new Map();

for (const [name, list] of [...lessonsBySubject.entries()].sort((a, b) => a[0].localeCompare(b[0]))) {
  list.sort((a, b) => a.order - b.order || a.title.localeCompare(b.title));
  const subjectSlug = subjectSlugFor(name);
  if (subjectSlugOwners.has(subjectSlug)) {
    throw new Error(`Duplicate subject slug "${subjectSlug}" for "${subjectSlugOwners.get(subjectSlug)}" and "${name}"`);
  }
  subjectSlugOwners.set(subjectSlug, name);
  const catalog = list.some((l) => l.catalog === "advanced") ? "advanced" : "k12";

  list.forEach((l, i) => {
    lessons[l.slug] = {
      slug: l.slug,
      title: l.title,
      chapter: l.chapter,
      subject: name,
      subjectSlug,
      catalog: l.catalog,
      audienceTier: l.audienceTier,
      openSource: l.openSource,
      description: l.description,
      wordCount: l.wordCount,
      indexable: l.indexable,
      noindexReason: l.noindexReason,
      html: l.html,
      prevSlug: i > 0 ? list[i - 1].slug : null,
      nextSlug: i < list.length - 1 ? list[i + 1].slug : null,
      relatedSlugs: relatedFor(list, i),
    };
  });

  const indexableLessonCount = list.filter((l) => l.indexable).length;
  subjects.push({
    slug: subjectSlug,
    name,
    catalog,
    lessonCount: list.length,
    indexableLessonCount,
    indexable: indexableLessonCount > 0,
    lessons: list.map((l) => ({ slug: l.slug, title: l.title, chapter: l.chapter, indexable: l.indexable })),
  });
}

assertInternalLinks(subjects, lessons);

await mkdir(path.dirname(outFile), { recursive: true });
await writeFile(outFile, JSON.stringify({ subjects, lessons }, null, 0), "utf8");

const all = Object.values(lessons);
const byReason = (r) => all.filter((l) => l.noindexReason === r).length;
console.log(`Subjects: ${subjects.length} (indexable hubs: ${subjects.filter((s) => s.indexable).length})`);
console.log(`Lessons kept: ${all.length}  (skipped non-lessons: ${skipped})`);
console.log(
  `Index gate: ${all.filter((l) => l.indexable).length} indexable, ` +
    `${all.length - all.filter((l) => l.indexable).length} noindex ` +
    `(placeholder ${byReason("placeholder")}, scaffold ${byReason("scaffold")}, thin <${MIN_INDEXABLE_WORDS}w ${byReason("thin")})`
);
console.log(
  `Local links: ${linkStats.rewritten} -> lessons, ${linkStats.toHub} -> subject hubs, ${linkStats.unlinked} unlinked (no public target)`
);
console.log(`Assets copied to public/lesson-assets: ${copiedAssets.size}`);
console.log(`Output: ${path.relative(appDir, outFile)}`);
