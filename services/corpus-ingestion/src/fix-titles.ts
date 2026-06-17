import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const lessonsDir = path.resolve(__dirname, "../../../corpus/lessons");

async function fixTitles() {
  const files = await readdir(lessonsDir);
  for (const file of files) {
    if (!file.endsWith(".md")) continue;
    const filePath = path.join(lessonsDir, file);
    let content = await readFile(filePath, "utf8");
    
    let title = file.replace(/\.md$/, "");
    title = title.replace(/^\d+-\d+-/, "").replace(/^\d+-/, "");
    title = title.split("-").map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(" ");

    // Check if there is frontmatter
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (frontmatterMatch) {
      let fm = frontmatterMatch[1];
      let needsUpdate = false;

      if (!fm.includes("title:")) { fm = `title: "${title}"\n${fm}`; needsUpdate = true; }
      if (!fm.includes("subject:")) { fm += `\nsubject: "unknown"`; needsUpdate = true; }
      if (!fm.includes("catalog:")) { fm += `\ncatalog: "k12"`; needsUpdate = true; }
      if (!fm.includes("audience_tier:") && !fm.includes("audienceTier:")) { fm += `\naudience_tier: "9-12"`; needsUpdate = true; }
      if (!fm.includes("chapter:")) { fm += `\nchapter: "Chapter 1"`; needsUpdate = true; }
      if (!fm.includes("objectives:")) { fm += `\nobjectives:\n  - "Understand the concepts"\n  - "Apply the theory"`; needsUpdate = true; }
      if (!fm.includes("open_source:") && !fm.includes("openSource:")) { fm += `\nopen_source: true`; needsUpdate = true; }

      if (needsUpdate) {
        content = content.replace(frontmatterMatch[1], fm);
        await writeFile(filePath, content, "utf8");
        console.log(`Updated frontmatter for ${file}`);
      }
    } else {
      // Add frontmatter block
      content = `---
title: "${title}"
subject: "unknown"
catalog: "k12"
audience_tier: "9-12"
chapter: "Chapter 1"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---
${content}`;
      await writeFile(filePath, content, "utf8");
      console.log(`Added frontmatter block to ${file}`);
    }
  }
}

fixTitles().catch(console.error);
