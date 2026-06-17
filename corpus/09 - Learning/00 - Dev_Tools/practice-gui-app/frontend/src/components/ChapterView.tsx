import { useEffect, useState } from "react";
import type { ChapterContent } from "../types";
import { fetchChapter } from "../api";
import MarkdownRenderer from "./MarkdownRenderer";

interface Props {
  subjectId: string;
  chapterNum: string;
  onDrill: () => void;
}

export default function ChapterView({ subjectId, chapterNum, onDrill }: Props) {
  const [content, setContent] = useState<ChapterContent | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetchChapter(subjectId, chapterNum)
      .then(setContent)
      .finally(() => setLoading(false));
  }, [subjectId, chapterNum]);

  if (loading) {
    return <div className="p-6 text-gh-muted">Loading chapter…</div>;
  }
  if (!content) {
    return <div className="p-6 text-gh-muted">Select a chapter from the sidebar.</div>;
  }

  return (
    <div className="h-full flex flex-col overflow-hidden">
      <header className="flex items-center justify-between px-6 py-3 border-b border-gh-border bg-gh-panel shrink-0">
        <h1 className="text-base font-semibold truncate">
          {content.num} — {content.title}
        </h1>
        <button
          onClick={onDrill}
          className="px-4 py-1.5 rounded bg-gh-accent text-white text-sm font-medium hover:bg-gh-accent/80 transition-colors"
        >
          Drill me
        </button>
      </header>
      <div className="flex-1 overflow-y-auto p-6">
        <MarkdownRenderer markdown={content.markdown} />
      </div>
    </div>
  );
}
