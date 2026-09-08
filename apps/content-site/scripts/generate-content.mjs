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

// ---- Main ------------------------------------------------------------------
await indexAssets(corpusRoot);
console.log(`Indexed ${assetIndex.size} asset files.`);

const files = (await readdir(lessonsDir)).filter((f) => f.endsWith(".md"));
const lessonsBySubject = new Map();
let kept = 0;
let skipped = 0;

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

  const slug = slugify(file.replace(/\.md$/, ""));
  const cleaned = cleanMarkdown(body);
  const withImages = await rewriteImages(cleaned);
  const html = marked.parse(withImages);

  const lesson = {
    slug,
    title: fm.title || slug,
    chapter: fm.chapter || "",
    catalog: fm.catalog === "advanced" ? "advanced" : "k12",
    audienceTier: fm.audience_tier || (fm.catalog === "advanced" ? "higher-education" : "9-12"),
    openSource: true,
    order: orderKey(file, fm.chapter),
    html,
  };

  if (!lessonsBySubject.has(subjectName)) lessonsBySubject.set(subjectName, []);
  lessonsBySubject.get(subjectName).push(lesson);
  kept++;
}

const subjects = [];
const lessons = {};

for (const [name, list] of [...lessonsBySubject.entries()].sort((a, b) => a[0].localeCompare(b[0]))) {
  list.sort((a, b) => a.order - b.order || a.title.localeCompare(b.title));
  const subjectSlug = slugify(name);
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
      html: l.html,
      prevSlug: i > 0 ? list[i - 1].slug : null,
      nextSlug: i < list.length - 1 ? list[i + 1].slug : null,
    };
  });

  subjects.push({
    slug: subjectSlug,
    name,
    catalog,
    lessonCount: list.length,
    lessons: list.map((l) => ({ slug: l.slug, title: l.title, chapter: l.chapter })),
  });
}

await mkdir(path.dirname(outFile), { recursive: true });
await writeFile(outFile, JSON.stringify({ subjects, lessons }, null, 0), "utf8");

console.log(`Subjects: ${subjects.length}`);
console.log(`Lessons kept: ${Object.keys(lessons).length}  (skipped non-lessons: ${skipped})`);
console.log(`Assets copied to public/lesson-assets: ${copiedAssets.size}`);
console.log(`Output: ${path.relative(appDir, outFile)}`);
