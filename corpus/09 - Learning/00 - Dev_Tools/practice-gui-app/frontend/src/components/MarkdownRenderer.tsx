import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import remarkGfm from "remark-gfm";
import rehypeKatex from "rehype-katex";
import { remarkObsidianSvgWikilink } from "../plugins/remarkObsidianSvgWikilink";
import type { Components } from "react-markdown";
import type { PluggableList } from "unified";

interface Props {
  markdown: string;
}

const components: Components = {
  img: ({ node: _node, src, alt, ...rest }) => (
    <img src={src} alt={alt ?? ""} className="my-4 mx-auto" {...rest} />
  ),
};

const remarkPlugins: PluggableList = [remarkGfm, remarkMath, remarkObsidianSvgWikilink];

export default function MarkdownRenderer({ markdown }: Props) {
  return (
    <div className="prose font-serif">
      <ReactMarkdown
        remarkPlugins={remarkPlugins}
        rehypePlugins={[[rehypeKatex, { strict: false }]]}
        components={components}
      >
        {markdown}
      </ReactMarkdown>
    </div>
  );
}
