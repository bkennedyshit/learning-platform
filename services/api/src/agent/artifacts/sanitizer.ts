import { SaxesParser, type SaxesTagPlain } from "saxes";

/**
 * Server-side SVG and Mermaid sanitizers. Model-authored diagram sources are
 * untrusted. These functions never execute or fetch anything: they parse with
 * a strict allowlist and reject anything unsafe or pathological.
 */

export interface SanitizeLimits {
  maxBytes: number;
  maxNodes: number;
  maxDepth: number;
  /** Max length of a single path-like attribute value (`d`, `points`). */
  maxPathLength: number;
  /** Max width/height/viewBox dimension. */
  maxDimension: number;
}

export const DEFAULT_SVG_LIMITS: SanitizeLimits = {
  maxBytes: 100_000,
  maxNodes: 2_000,
  maxDepth: 32,
  maxPathLength: 20_000,
  maxDimension: 4_096
};

export interface SanitizeResult {
  ok: boolean;
  /** Present only when ok is true. */
  sanitized?: string;
  violations: string[];
  stats: { bytes: number; nodes: number; depth: number };
}

const ALLOWED_SVG_ELEMENTS = new Set([
  "svg",
  "g",
  "path",
  "rect",
  "circle",
  "ellipse",
  "line",
  "polyline",
  "polygon",
  "text",
  "tspan",
  "title",
  "desc",
  "defs",
  "linearGradient",
  "radialGradient",
  "stop",
  "marker"
]);

const ALLOWED_SVG_ATTRS = new Set([
  "id",
  "class",
  "d",
  "x",
  "y",
  "cx",
  "cy",
  "r",
  "rx",
  "ry",
  "x1",
  "y1",
  "x2",
  "y2",
  "points",
  "width",
  "height",
  "viewbox",
  "fill",
  "fill-opacity",
  "fill-rule",
  "stroke",
  "stroke-width",
  "stroke-linecap",
  "stroke-linejoin",
  "stroke-dasharray",
  "stroke-opacity",
  "opacity",
  "transform",
  "font-size",
  "font-family",
  "font-weight",
  "font-style",
  "text-anchor",
  "dominant-baseline",
  "dx",
  "dy",
  "offset",
  "stop-color",
  "stop-opacity",
  "gradientunits",
  "gradienttransform",
  "spreadmethod",
  "markerwidth",
  "markerheight",
  "markerunits",
  "orient",
  "refx",
  "refy",
  "preserveaspectratio",
  "xmlns",
  "version",
  "role",
  "aria-label",
  "aria-hidden"
]);

const PATH_LIKE_ATTRS = new Set(["d", "points"]);

function hasDangerousValue(value: string): boolean {
  const v = value.toLowerCase();
  if (v.includes("javascript:") || v.includes("expression(") || v.includes("@import")) {
    return true;
  }
  if (v.includes("data:") || v.includes("http://") || v.includes("https://")) {
    return true;
  }
  // Only internal url(#id) references are allowed.
  const urlMatch = v.match(/url\(\s*['"]?([^)]*)/);
  if (urlMatch && urlMatch[1] !== undefined && !urlMatch[1].trim().startsWith("#")) {
    return true;
  }
  return false;
}

function escapeXml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

export function sanitizeSvg(source: string, limits: SanitizeLimits = DEFAULT_SVG_LIMITS): SanitizeResult {
  const violations: string[] = [];
  const bytes = Buffer.byteLength(source, "utf8");
  let nodes = 0;
  let depth = 0;
  let maxDepth = 0;
  let rootSeen = false;
  const out: string[] = [];

  const stats = () => ({ bytes, nodes, depth: maxDepth });

  if (bytes > limits.maxBytes) {
    return { ok: false, violations: [`document exceeds maxBytes (${bytes} > ${limits.maxBytes})`], stats: stats() };
  }
  if (/<!DOCTYPE/i.test(source)) {
    violations.push("doctype is not allowed");
  }
  if (/<!ENTITY/i.test(source) || /&(?!(amp|lt|gt|quot|apos);)[a-z0-9#]+;/i.test(source)) {
    violations.push("custom or non-standard entities are not allowed");
  }

  const parser = new SaxesParser({ xmlns: false, fragment: false, position: true });

  parser.on("error", (err) => {
    violations.push(`parse error: ${err.message}`);
  });
  parser.on("doctype", () => {
    violations.push("doctype is not allowed");
  });
  parser.on("processinginstruction", () => {
    violations.push("processing instructions are not allowed");
  });
  parser.on("cdata", () => {
    violations.push("CDATA sections are not allowed");
  });

  parser.on("opentag", (tag: SaxesTagPlain) => {
    const name = tag.name;
    nodes += 1;
    if (nodes > limits.maxNodes) {
      violations.push(`document exceeds maxNodes (${limits.maxNodes})`);
    }
    if (!rootSeen) {
      rootSeen = true;
      if (name !== "svg") {
        violations.push(`root element must be <svg>, found <${name}>`);
      }
    }
    // SVG element names are case-sensitive (e.g. linearGradient); match exactly.
    if (!ALLOWED_SVG_ELEMENTS.has(name)) {
      violations.push(`element <${name}> is not allowed`);
      // Still track depth so structure stays balanced for reporting.
    }

    const attrPairs: string[] = [];
    for (const [rawAttr, value] of Object.entries(tag.attributes)) {
      const attr = rawAttr.toLowerCase();
      if (attr.startsWith("on")) {
        violations.push(`event attribute ${rawAttr} is not allowed`);
        continue;
      }
      if (attr === "href" || attr === "xlink:href" || attr.endsWith(":href")) {
        violations.push(`external reference attribute ${rawAttr} is not allowed`);
        continue;
      }
      if (attr === "xmlns") {
        // Only the SVG namespace declaration is permitted.
        if (value !== "http://www.w3.org/2000/svg") {
          violations.push("xmlns namespace is not allowed");
          continue;
        }
        attrPairs.push(`${rawAttr}="${escapeXml(value)}"`);
        continue;
      }
      if (!ALLOWED_SVG_ATTRS.has(attr)) {
        violations.push(`attribute ${rawAttr} is not allowed`);
        continue;
      }
      if (hasDangerousValue(value)) {
        violations.push(`attribute ${rawAttr} has an unsafe value`);
        continue;
      }
      if (PATH_LIKE_ATTRS.has(attr) && value.length > limits.maxPathLength) {
        violations.push(`attribute ${rawAttr} exceeds maxPathLength`);
        continue;
      }
      if ((attr === "width" || attr === "height") && exceedsDimension(value, limits.maxDimension)) {
        violations.push(`attribute ${rawAttr} exceeds maxDimension`);
        continue;
      }
      if (attr === "viewbox" && viewBoxExceeds(value, limits.maxDimension)) {
        violations.push("viewBox exceeds maxDimension or is malformed");
        continue;
      }
      attrPairs.push(`${rawAttr}="${escapeXml(value)}"`);
    }

    const attrText = attrPairs.length ? ` ${attrPairs.join(" ")}` : "";
    if (tag.isSelfClosing) {
      out.push(`<${name}${attrText}/>`);
    } else {
      out.push(`<${name}${attrText}>`);
      depth += 1;
      maxDepth = Math.max(maxDepth, depth);
      if (depth > limits.maxDepth) {
        violations.push(`document exceeds maxDepth (${limits.maxDepth})`);
      }
    }
  });

  parser.on("closetag", (tag: SaxesTagPlain) => {
    if (tag.isSelfClosing) {
      return;
    }
    out.push(`</${tag.name}>`);
    depth -= 1;
  });

  parser.on("text", (text: string) => {
    out.push(escapeXml(text));
  });

  try {
    parser.write(source).close();
  } catch (err) {
    violations.push(`fatal parse error: ${(err as Error).message}`);
  }

  if (violations.length > 0) {
    return { ok: false, violations: [...new Set(violations)], stats: stats() };
  }
  return { ok: true, sanitized: out.join(""), violations: [], stats: stats() };
}

function exceedsDimension(value: string, max: number): boolean {
  const numeric = Number.parseFloat(value);
  return Number.isFinite(numeric) && numeric > max;
}

function viewBoxExceeds(value: string, max: number): boolean {
  const parts = value.trim().split(/[\s,]+/).map(Number);
  if (parts.length !== 4 || parts.some((n) => !Number.isFinite(n))) {
    return true;
  }
  const width = parts[2] ?? 0;
  const height = parts[3] ?? 0;
  return width > max || height > max || width <= 0 || height <= 0;
}

/* ------------------------------- Mermaid -------------------------------- */

export const ALLOWED_MERMAID_TYPES = [
  "graph",
  "flowchart",
  "sequenceDiagram",
  "stateDiagram",
  "stateDiagram-v2",
  "classDiagram",
  "erDiagram"
] as const;

export interface MermaidSanitizeResult {
  ok: boolean;
  sanitized?: string;
  diagramType?: string;
  violations: string[];
}

export function sanitizeMermaid(source: string, maxBytes = 50_000): MermaidSanitizeResult {
  const violations: string[] = [];

  if (Buffer.byteLength(source, "utf8") > maxBytes) {
    return { ok: false, violations: [`diagram exceeds maxBytes (${maxBytes})`] };
  }

  const lines = source.split(/\r?\n/);
  const firstMeaningful = lines.find((l) => l.trim().length > 0 && !l.trim().startsWith("%%"));
  const diagramType = firstMeaningful?.trim().split(/\s+/)[0] ?? "";

  if (!ALLOWED_MERMAID_TYPES.some((t) => diagramType === t)) {
    violations.push(`diagram type "${diagramType}" is not allowed`);
  }

  const lower = source.toLowerCase();
  if (/\bclick\b/.test(lower)) {
    violations.push("click interactions are not allowed");
  }
  if (source.includes("%%{")) {
    violations.push("mermaid directives (%%{ ... }%%) are not allowed");
  }
  if (/<[a-z!/]/i.test(source)) {
    violations.push("raw HTML is not allowed");
  }
  if (lower.includes("href") || lower.includes("javascript:") || lower.includes("script")) {
    violations.push("links/scripts are not allowed");
  }

  if (violations.length > 0) {
    return { ok: false, ...(diagramType ? { diagramType } : {}), violations };
  }
  return { ok: true, sanitized: source, diagramType, violations: [] };
}
