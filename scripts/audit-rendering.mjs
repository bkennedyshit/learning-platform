// Static rendering audit over generated lesson content.
// Flags likely-broken rendering across all lessons without eyeballing each page.
//
// Run:  node scripts/audit-rendering.mjs

import { readFileSync, readdirSync, existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");
const contentFile = path.join(root, "apps/content-site/src/generated/content.json");
const assetsDir = path.join(root, "apps/content-site/public/lesson-assets");

const { subjects, lessons } = JSON.parse(readFileSync(contentFile, "utf8"));
const assetSet = new Set(existsSync(assetsDir) ? readdirSync(assetsDir) : []);

const all = Object.values(lessons);
const flags = {
  leftoverDollar: [],     // unrendered inline math ($...$)
  rawLatexCmd: [],        // literal \frac \begin \theta etc. in text
  altDelims: [],          // literal \( \) \[ \] left in output
  rawWikilink: [],        // [[ ]] leftovers
  rawCallout: [],         // [!info] leftovers
  brokenImg: [],          // <img src=/lesson-assets/X> with missing file
  emptyish: [],           // suspiciously short content
  mermaid: [],            // has mermaid diagram(s)
};

function scrub(html) {
  // Remove code blocks, inline code, and rendered katex so we only inspect prose.
  return html
    .replace(/<pre[\s\S]*?<\/pre>/g, " ")
    .replace(/<code[\s\S]*?<\/code>/g, " ")
    .replace(/<span class="katex[\s\S]*?<\/span><\/span>/g, " ");
}

for (const l of all) {
  const html = l.html || "";
  const bare = scrub(html);

  // Only count $ that looks like math: $ followed by backslash/letter/paren,
  // or a $ pair around non-space — not currency like $5 or $1.2M.
  const mathDollars = (bare.match(/\$\s*[\\A-Za-z(]/g) || []).length;
  if (mathDollars > 0) flags.leftoverDollar.push([l.slug, mathDollars]);

  if (/\\(frac|begin\{|sum|int|theta|alpha|sqrt|partial|mathbf|cdot|nabla)\b/.test(bare))
    flags.rawLatexCmd.push(l.slug);

  if (/\\\(|\\\)|\\\[|\\\]/.test(bare)) flags.altDelims.push(l.slug);
  if (/\[\[[^\]]+\]\]/.test(bare)) flags.rawWikilink.push(l.slug);
  if (/\[!\w+\]/.test(bare)) flags.rawCallout.push(l.slug);

  for (const m of html.matchAll(/<img[^>]+src="\/lesson-assets\/([^"]+)"/g)) {
    const name = decodeURIComponent(m[1]);
    if (!assetSet.has(name)) flags.brokenImg.push([l.slug, name]);
  }

  const textLen = bare.replace(/<[^>]+>/g, "").trim().length;
  if (textLen < 400) flags.emptyish.push([l.slug, textLen]);

  if (/<pre class="mermaid">/.test(html)) flags.mermaid.push(l.slug);
}

const N = all.length;
console.log(`\n=== Rendering Audit — ${N} lessons / ${subjects.length} subjects ===\n`);
const line = (label, arr) => console.log(`${label.padEnd(26)} ${String(arr.length).padStart(4)}`);
line("leftover $ (unrendered)", flags.leftoverDollar);
line("raw LaTeX commands", flags.rawLatexCmd);
line("alt delimiters \\( \\[", flags.altDelims);
line("raw wikilinks [[ ]]", flags.rawWikilink);
line("raw callouts [!x]", flags.rawCallout);
line("broken image refs", flags.brokenImg);
line("short/empty (<400 chars)", flags.emptyish);
line("lessons with mermaid", flags.mermaid);

const sample = (label, arr, n = 12) => {
  if (!arr.length) return;
  console.log(`\n--- ${label} (first ${Math.min(n, arr.length)}) ---`);
  for (const x of arr.slice(0, n)) console.log("  " + (Array.isArray(x) ? x.join("  ") : x));
};
sample("leftover $", flags.leftoverDollar);
sample("raw LaTeX commands", flags.rawLatexCmd);
sample("alt delimiters", flags.altDelims);
sample("raw wikilinks", flags.rawWikilink);
sample("raw callouts", flags.rawCallout);
sample("broken images", flags.brokenImg);
sample("short/empty", flags.emptyish);
