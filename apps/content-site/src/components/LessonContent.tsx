"use client";

import { useEffect, useRef } from "react";

export default function LessonContent({ html }: { html: string }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const blocks = Array.from(
      el.querySelectorAll<HTMLElement>('pre.mermaid:not([data-processed="true"])')
    );
    if (blocks.length === 0) return;

    let cancelled = false;
    (async () => {
      try {
        const mermaid = (await import("mermaid")).default;
        mermaid.initialize({ startOnLoad: false, theme: "neutral", securityLevel: "loose" });
        if (cancelled) return;
        await mermaid.run({ nodes: blocks });
      } catch {
        /* leave the mermaid source as a code block on failure */
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [html]);

  return (
    <div
      ref={ref}
      className="lesson-content"
      style={{ fontSize: "1.0625rem", lineHeight: 1.8 }}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
