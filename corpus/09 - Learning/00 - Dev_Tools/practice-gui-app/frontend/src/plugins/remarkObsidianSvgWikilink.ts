/**
 * Remark plugin that converts Obsidian-style SVG wikilinks
 * `![[filename.svg|width]]` or `![[filename.svg]]`
 * into standard markdown image nodes pointing at /svgs/{filename}.
 *
 * v1.2: filenames are now globally unique (prefixed with subject_id during
 * the centralization migration), so the URL is just /svgs/<filename>.
 */
import { visit } from "unist-util-visit";
import type { Plugin } from "unified";
import type { Root, PhrasingContent } from "mdast";

const WIKILINK_RE = /!\[\[([^|\]]+\.svg)(?:\|(\d+))?\]\]/g;

interface ImageWithData {
  type: "image";
  url: string;
  alt: string;
  title: null;
  data?: { hProperties: { width: number } };
}

const remarkObsidianSvgWikilink: Plugin<[], Root> = () => {
  return (tree) => {
    visit(tree, "text", (node, index, parent) => {
      if (index === undefined || !parent) return;
      const { value } = node;
      const matches = [...value.matchAll(WIKILINK_RE)];
      if (matches.length === 0) return;

      const children: PhrasingContent[] = [];
      let lastEnd = 0;

      for (const match of matches) {
        const start = match.index!;
        if (start > lastEnd) {
          children.push({ type: "text", value: value.slice(lastEnd, start) });
        }
        const filename = match[1];
        const width = match[2];
        const img: ImageWithData = {
          type: "image",
          url: `/svgs/${filename}`,
          alt: filename,
          title: null,
        };
        if (width) {
          img.data = { hProperties: { width: Number(width) } };
        }
        children.push(img as unknown as PhrasingContent);
        lastEnd = start + match[0].length;
      }

      if (lastEnd < value.length) {
        children.push({ type: "text", value: value.slice(lastEnd) });
      }

      parent.children.splice(index, 1, ...children);
    });
  };
};

export { remarkObsidianSvgWikilink };
export default remarkObsidianSvgWikilink;
