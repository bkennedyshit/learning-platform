/**
 * Client-side Mermaid source validation, mirroring the server sanitizer. Only
 * an allowlisted set of diagram types is permitted, and interactive/link/HTML/
 * directive constructs are rejected before Mermaid is ever initialized.
 */

export const ALLOWED_MERMAID_TYPES = [
  "graph",
  "flowchart",
  "sequenceDiagram",
  "stateDiagram",
  "stateDiagram-v2",
  "classDiagram",
  "erDiagram"
] as const;

export interface MermaidValidation {
  ok: boolean;
  diagramType?: string;
  violations: string[];
}

export function validateMermaid(source: string, maxBytes = 50_000): MermaidValidation {
  const violations: string[] = [];
  if (typeof source !== "string" || source.trim().length === 0) {
    return { ok: false, violations: ["empty source"] };
  }
  if (new Blob([source]).size > maxBytes) {
    return { ok: false, violations: ["diagram exceeds byte limit"] };
  }

  const lines = source.split(/\r?\n/);
  const firstMeaningful = lines.find((l) => l.trim().length > 0 && !l.trim().startsWith("%%"));
  const diagramType = firstMeaningful?.trim().split(/\s+/)[0] ?? "";

  if (!ALLOWED_MERMAID_TYPES.some((t) => diagramType === t)) {
    violations.push(`diagram type "${diagramType}" is not allowed`);
  }

  const lower = source.toLowerCase();
  if (/\bclick\b/.test(lower)) violations.push("click interactions are not allowed");
  if (source.includes("%%{")) violations.push("mermaid directives are not allowed");
  if (/<[a-z!/]/i.test(source)) violations.push("raw HTML is not allowed");
  if (lower.includes("href") || lower.includes("javascript:") || lower.includes("script")) {
    violations.push("links/scripts are not allowed");
  }

  if (violations.length > 0) {
    return { ok: false, ...(diagramType ? { diagramType } : {}), violations };
  }
  return { ok: true, diagramType, violations: [] };
}
