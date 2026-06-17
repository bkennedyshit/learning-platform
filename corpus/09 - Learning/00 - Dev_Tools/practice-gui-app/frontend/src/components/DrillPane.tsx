import { useEffect, useRef, useState } from "react";
import type { DrillResponse } from "../types";
import { postDrill } from "../api";
import MarkdownRenderer from "./MarkdownRenderer";

interface Props {
  subjectId: string | null;
  chapterNum: string | null;
  trigger: number;
}

export default function DrillPane({ subjectId, chapterNum, trigger }: Props) {
  const [drill, setDrill] = useState<DrillResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [seedInput, setSeedInput] = useState("");
  const [copied, setCopied] = useState(false);
  const prevTrigger = useRef(0);

  const generate = (sid: string, num: string, seed: number | null = null) => {
    setLoading(true);
    postDrill(sid, num, 8, seed)
      .then(setDrill)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    if (trigger > prevTrigger.current && subjectId && chapterNum) {
      prevTrigger.current = trigger;
      generate(subjectId, chapterNum, null);
    }
  }, [trigger, subjectId, chapterNum]);

  const copySeed = () => {
    if (drill) {
      navigator.clipboard.writeText(String(drill.seed));
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    }
  };

  if (!subjectId || !chapterNum) {
    return (
      <div className="h-full flex items-center justify-center text-gh-muted p-6">
        Select a chapter to get started.
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col overflow-hidden">
      <header className="px-6 py-3 border-b border-gh-border bg-gh-panel shrink-0 space-y-2">
        <div className="flex items-center gap-2">
          <input
            type="number"
            placeholder="Seed (optional)"
            value={seedInput}
            onChange={(e) => setSeedInput(e.target.value)}
            className="w-32 px-2 py-1 rounded bg-gh-bg border border-gh-border text-sm text-gh-text placeholder:text-gh-muted"
          />
          <button
            onClick={() => generate(subjectId, chapterNum, seedInput ? Number(seedInput) : null)}
            className="px-3 py-1 rounded bg-gh-accent text-white text-sm font-medium hover:bg-gh-accent/80 transition-colors"
          >
            Generate
          </button>
          {drill && (
            <>
              <span className="text-xs text-gh-muted ml-auto font-mono">
                seed: {drill.seed}
              </span>
              <button
                onClick={copySeed}
                className="text-xs text-gh-accent hover:underline"
              >
                {copied ? "Copied!" : "Copy"}
              </button>
            </>
          )}
        </div>
      </header>
      <div className="flex-1 overflow-y-auto p-6">
        {loading && <p className="text-gh-muted">Generating problems…</p>}
        {!loading && !drill && (
          <p className="text-gh-muted">Click &ldquo;Drill me&rdquo; to generate practice problems.</p>
        )}
        {!loading && drill && (
          <>
            <MarkdownRenderer markdown={drill.markdown} />
            <div className="mt-6">
              <button
                onClick={() => generate(subjectId, chapterNum, null)}
                className="px-4 py-2 rounded bg-gh-border text-gh-text text-sm font-medium hover:bg-gh-border/70 transition-colors"
              >
                New problems
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
