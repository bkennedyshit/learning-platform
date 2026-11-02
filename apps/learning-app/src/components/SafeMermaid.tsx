"use client";

import React, { useEffect, useMemo, useRef, useState } from "react";
import { validateMermaid } from "../lib/safeMermaid";

export interface SafeMermaidProps {
  source: string;
  altText: string;
  className?: string;
}

/**
 * Renders agent-authored Mermaid safely. The source is validated against the
 * allowlist first; only then is Mermaid initialized with `securityLevel:
 * "strict"` and `htmlLabels: false` and asked to render. The rendered output is
 * Mermaid-generated (not raw model markup) from validated source.
 */
export default function SafeMermaid({ source, altText, className }: SafeMermaidProps): React.JSX.Element {
  const ref = useRef<HTMLDivElement>(null);
  // Validation is pure/derived — never a setState inside the effect.
  const validation = useMemo(() => validateMermaid(source), [source]);
  const [renderError, setRenderError] = useState<string | null>(null);

  useEffect(() => {
    if (!validation.ok) return;

    let cancelled = false;
    (async () => {
      try {
        const mermaid = (await import("mermaid")).default;
        mermaid.initialize({
          startOnLoad: false,
          securityLevel: "strict",
          htmlLabels: false,
          flowchart: { htmlLabels: false },
          theme: "dark"
        });
        const id = `safe-mermaid-${Math.random().toString(36).slice(2)}`;
        const { svg } = await mermaid.render(id, source);
        if (!cancelled && ref.current) {
          ref.current.innerHTML = svg;
          setRenderError(null);
        }
      } catch {
        if (!cancelled) setRenderError("Diagram could not be rendered.");
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [source, validation.ok]);

  const error = !validation.ok ? "Diagram could not be displayed safely." : renderError;

  if (error) {
    return (
      <div className={className} role="img" aria-label={altText} data-testid="safe-mermaid-rejected">
        <p style={{ fontSize: "0.85rem", color: "var(--text-secondary, #888)" }}>{error}</p>
      </div>
    );
  }

  return <div className={className} ref={ref} role="img" aria-label={altText} data-testid="safe-mermaid" />;
}
