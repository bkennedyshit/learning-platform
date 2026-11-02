/**
 * Real browser PNG export for sanitized SVG/plot artifacts.
 *
 * Security: the SVG is re-checked against the strict allowlist (the same
 * defence-in-depth used for rendering) BEFORE it is ever handed to an <img> or
 * canvas. Nothing is inserted as raw markup. If the browser cannot rasterize
 * (no canvas/2D context, or the image fails to load), the caller receives an
 * explicit `fallback: true` result rather than a silent failure — the server
 * placeholder PNG stays honestly labeled.
 */

import { recheckSvg, svgDataUrl } from "./safeSvg";

/** Upper bound on either raster dimension to avoid pathological canvases. */
export const PNG_MAX_DIMENSION = 2048;
/** SVG spec default intrinsic size when none is declared. */
const SVG_DEFAULT_WIDTH = 300;
const SVG_DEFAULT_HEIGHT = 150;

export interface BoundedDimensions {
  width: number;
  height: number;
}

function parseLength(value: string | undefined): number | undefined {
  if (!value) return undefined;
  const match = value.trim().match(/^([0-9]*\.?[0-9]+)\s*(px)?$/i);
  if (!match) return undefined;
  const n = Number(match[1]);
  return Number.isFinite(n) && n > 0 ? n : undefined;
}

/**
 * Determine a bounded raster size from a (sanitized) SVG string. Prefers the
 * explicit width/height, falls back to the viewBox aspect ratio, then to the
 * SVG default. The result is clamped to [1, max] on both axes while preserving
 * aspect ratio.
 */
export function computeBoundedDimensions(source: string, max = PNG_MAX_DIMENSION): BoundedDimensions {
  const widthAttr = source.match(/\bwidth\s*=\s*["']([^"']+)["']/i)?.[1];
  const heightAttr = source.match(/\bheight\s*=\s*["']([^"']+)["']/i)?.[1];
  let width = parseLength(widthAttr);
  let height = parseLength(heightAttr);

  if (width === undefined || height === undefined) {
    const viewBox = source.match(/\bviewBox\s*=\s*["']([^"']+)["']/i)?.[1];
    if (viewBox) {
      const parts = viewBox.trim().split(/[\s,]+/).map(Number);
      if (parts.length === 4 && parts.every((n) => Number.isFinite(n))) {
        const vbW = parts[2];
        const vbH = parts[3];
        if (vbW > 0 && vbH > 0) {
          width = width ?? vbW;
          height = height ?? vbH;
        }
      }
    }
  }

  width = width ?? SVG_DEFAULT_WIDTH;
  height = height ?? SVG_DEFAULT_HEIGHT;

  // Clamp preserving aspect ratio.
  const scale = Math.min(1, max / width, max / height);
  return {
    width: Math.max(1, Math.round(width * scale)),
    height: Math.max(1, Math.round(height * scale))
  };
}

export interface PngRenderResult {
  ok: boolean;
  dataUri?: string;
  width?: number;
  height?: number;
  /** True when no real raster was produced (rejected SVG or unavailable tooling). */
  fallback: boolean;
  reason?: string;
}

export interface RenderDeps {
  /** Injectable for tests. Defaults to `new Image()`. */
  createImage?: () => HTMLImageElement;
  /** Injectable for tests. Defaults to a detached <canvas>. */
  createCanvas?: (width: number, height: number) => HTMLCanvasElement;
}

export interface RenderOptions {
  maxDimension?: number;
}

function defaultCreateImage(): HTMLImageElement {
  return new Image();
}

function defaultCreateCanvas(width: number, height: number): HTMLCanvasElement {
  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  return canvas;
}

/**
 * Render a sanitized SVG string to a PNG data URI using a bounded canvas.
 * Always resolves (never rejects); failures return `fallback: true`.
 */
export async function renderSvgToPng(
  source: string,
  options: RenderOptions = {},
  deps: RenderDeps = {}
): Promise<PngRenderResult> {
  // 1. Re-check the SVG at the export boundary.
  const recheck = recheckSvg(source);
  if (!recheck.ok || !recheck.sanitized) {
    return { ok: false, fallback: true, reason: "SVG failed re-validation" };
  }
  const sanitized: string = recheck.sanitized;

  // 2. Ensure raster tooling exists (guards SSR and jsdom-without-canvas).
  const createImage = deps.createImage ?? (typeof Image !== "undefined" ? defaultCreateImage : undefined);
  const createCanvas =
    deps.createCanvas ?? (typeof document !== "undefined" ? defaultCreateCanvas : undefined);
  if (!createImage || !createCanvas) {
    return { ok: false, fallback: true, reason: "Canvas rendering is unavailable" };
  }

  const { width, height } = computeBoundedDimensions(sanitized, options.maxDimension ?? PNG_MAX_DIMENSION);
  const canvas = createCanvas(width, height);
  const ctx = canvas.getContext?.("2d");
  if (!ctx) {
    return { ok: false, fallback: true, reason: "2D context is unavailable" };
  }

  return await new Promise<PngRenderResult>((resolve) => {
    const img = createImage();
    img.onload = () => {
      try {
        ctx.drawImage(img, 0, 0, width, height);
        const dataUri = canvas.toDataURL("image/png");
        if (typeof dataUri === "string" && dataUri.startsWith("data:image/png")) {
          resolve({ ok: true, dataUri, width, height, fallback: false });
        } else {
          resolve({ ok: false, fallback: true, reason: "Canvas produced no PNG output" });
        }
      } catch {
        resolve({ ok: false, fallback: true, reason: "Canvas export failed (tainted or blocked)" });
      }
    };
    img.onerror = () => {
      resolve({ ok: false, fallback: true, reason: "SVG image failed to load" });
    };
    // Assign last so handlers are attached first.
    img.src = svgDataUrl(sanitized);
  });
}

/**
 * Trigger a browser download of a data URI. No-op (returns false) outside a
 * browser document. Kept separate so rendering logic stays testable.
 */
export function downloadDataUri(dataUri: string, filename: string): boolean {
  if (typeof document === "undefined") return false;
  const anchor = document.createElement("a");
  anchor.href = dataUri;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  return true;
}
