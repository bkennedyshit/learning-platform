"use client";

import React, { useMemo } from "react";
import { recheckSvg, svgDataUrl } from "../lib/safeSvg";

export interface SafeSvgProps {
  /** Server-sanitized SVG source. Re-checked client-side before rendering. */
  source: string;
  altText: string;
  className?: string;
}

/**
 * Renders untrusted SVG safely. Never uses dangerouslySetInnerHTML: the source
 * is re-validated against a strict allowlist and, only if it passes, rendered
 * as an <img> pointing at a data URL. Rejected content shows a fallback notice.
 */
export default function SafeSvg({ source, altText, className }: SafeSvgProps): React.JSX.Element {
  const result = useMemo(() => recheckSvg(source), [source]);

  if (!result.ok || !result.sanitized) {
    return (
      <div className={className} role="img" aria-label={altText} data-testid="safe-svg-rejected">
        <p style={{ fontSize: "0.85rem", color: "var(--text-secondary, #888)" }}>
          Visual could not be displayed safely.
        </p>
      </div>
    );
  }

  return (
    <img
      className={className}
      src={svgDataUrl(result.sanitized)}
      alt={altText}
      data-testid="safe-svg"
      style={{ maxWidth: "100%", height: "auto" }}
    />
  );
}
