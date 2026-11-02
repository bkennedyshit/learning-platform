/**
 * Client-side SVG allowlist recheck. This is the second half of a defence in
 * depth: the server sanitizes model-authored SVG, and this re-validates at the
 * rendering boundary before the browser ever sees it. It never inserts raw
 * markup — callers render the returned string via an <img> data URL only.
 */

const ALLOWED_ELEMENTS = new Set([
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

const ALLOWED_ATTRS = new Set([
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

export interface SvgRecheckResult {
  ok: boolean;
  sanitized?: string;
  violations: string[];
}

function hasDangerousValue(value: string): boolean {
  const v = value.toLowerCase();
  if (v.includes("javascript:") || v.includes("expression(") || v.includes("@import")) return true;
  if (v.includes("data:") || v.includes("http://") || v.includes("https://")) return true;
  const urlMatch = v.match(/url\(\s*['"]?([^)]*)/);
  if (urlMatch && urlMatch[1] !== undefined && !urlMatch[1].trim().startsWith("#")) return true;
  return false;
}

/**
 * Re-validate an (already server-sanitized) SVG string against a strict
 * element/attribute allowlist using the browser DOMParser. Returns the
 * serialized safe SVG when it passes, or a list of violations when it does not.
 */
export function recheckSvg(source: string, maxBytes = 100_000): SvgRecheckResult {
  const violations: string[] = [];
  if (typeof source !== "string" || source.trim().length === 0) {
    return { ok: false, violations: ["empty source"] };
  }
  if (new Blob([source]).size > maxBytes) {
    return { ok: false, violations: ["document exceeds byte limit"] };
  }
  if (/<!DOCTYPE/i.test(source) || /<!ENTITY/i.test(source)) {
    violations.push("doctype/entities are not allowed");
  }

  const parser = new DOMParser();
  const doc = parser.parseFromString(source, "image/svg+xml");

  if (doc.getElementsByTagName("parsererror").length > 0) {
    return { ok: false, violations: ["malformed SVG"] };
  }

  const root = doc.documentElement;
  if (!root || root.tagName !== "svg") {
    return { ok: false, violations: [`root element must be <svg>, found <${root?.tagName ?? "none"}>`] };
  }

  const walk = (el: Element): void => {
    if (!ALLOWED_ELEMENTS.has(el.tagName)) {
      violations.push(`element <${el.tagName}> is not allowed`);
    }
    for (const attr of Array.from(el.attributes)) {
      const name = attr.name.toLowerCase();
      if (name.startsWith("on")) {
        violations.push(`event attribute ${attr.name} is not allowed`);
        continue;
      }
      if (name === "href" || name === "xlink:href" || name.endsWith(":href")) {
        violations.push(`reference attribute ${attr.name} is not allowed`);
        continue;
      }
      if (name === "xmlns" || name === "xmlns:xlink") {
        if (attr.value !== "http://www.w3.org/2000/svg" && name === "xmlns") {
          violations.push("xmlns namespace is not allowed");
        }
        continue;
      }
      if (!ALLOWED_ATTRS.has(name)) {
        violations.push(`attribute ${attr.name} is not allowed`);
        continue;
      }
      if (hasDangerousValue(attr.value)) {
        violations.push(`attribute ${attr.name} has an unsafe value`);
      }
    }
    for (const child of Array.from(el.children)) {
      walk(child);
    }
  };
  walk(root);

  if (violations.length > 0) {
    return { ok: false, violations: [...new Set(violations)] };
  }
  return { ok: true, sanitized: new XMLSerializer().serializeToString(root), violations: [] };
}

/** Build an <img>-safe data URL from sanitized SVG. */
export function svgDataUrl(sanitized: string): string {
  return `data:image/svg+xml;utf8,${encodeURIComponent(sanitized)}`;
}
