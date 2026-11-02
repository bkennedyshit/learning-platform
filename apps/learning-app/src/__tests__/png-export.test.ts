import { describe, it, expect, vi } from "vitest";
import {
  computeBoundedDimensions,
  renderSvgToPng,
  PNG_MAX_DIMENSION,
  type RenderDeps
} from "../lib/pngExport";

const CLEAN_SVG =
  '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="80" viewBox="0 0 100 80">' +
  '<rect x="10" y="10" width="80" height="60" fill="#4c8bf5"/><text x="20" y="45">A</text></svg>';

const MALICIOUS_SVG =
  '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" onload="alert(1)">' +
  '<script>alert(2)</script></svg>';

/** A fake <img> whose src assignment synchronously fires onload or onerror. */
function fakeImageFactory(mode: "load" | "error"): () => HTMLImageElement {
  return () => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const img: any = {};
    Object.defineProperty(img, "src", {
      set() {
        queueMicrotask(() => {
          if (mode === "load") img.onload?.(new Event("load"));
          else img.onerror?.(new Event("error"));
        });
      }
    });
    return img as HTMLImageElement;
  };
}

function fakeCanvasFactory(opts: {
  withContext?: boolean;
  toDataUri?: string;
  throwOnDraw?: boolean;
}): (w: number, h: number) => HTMLCanvasElement {
  return (width: number, height: number) => {
    const ctx = {
      drawImage: () => {
        if (opts.throwOnDraw) throw new Error("tainted");
      }
    };
    return {
      width,
      height,
      getContext: () => (opts.withContext === false ? null : ctx),
      toDataURL: () => opts.toDataUri ?? "data:image/png;base64,MOCKPNG"
    } as unknown as HTMLCanvasElement;
  };
}

describe("computeBoundedDimensions", () => {
  it("uses explicit width/height", () => {
    expect(computeBoundedDimensions(CLEAN_SVG)).toEqual({ width: 100, height: 80 });
  });

  it("falls back to viewBox when width/height are absent", () => {
    const svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 20"></svg>';
    expect(computeBoundedDimensions(svg)).toEqual({ width: 40, height: 20 });
  });

  it("clamps to the max dimension preserving aspect ratio", () => {
    const svg = `<svg width="${PNG_MAX_DIMENSION * 2}" height="${PNG_MAX_DIMENSION}"></svg>`;
    const dims = computeBoundedDimensions(svg);
    expect(dims.width).toBe(PNG_MAX_DIMENSION);
    expect(dims.height).toBe(PNG_MAX_DIMENSION / 2);
  });

  it("uses SVG defaults when nothing is declared", () => {
    expect(computeBoundedDimensions("<svg></svg>")).toEqual({ width: 300, height: 150 });
  });
});

describe("renderSvgToPng", () => {
  it("rasterizes a clean SVG to a PNG data URI", async () => {
    const deps: RenderDeps = {
      createImage: fakeImageFactory("load"),
      createCanvas: fakeCanvasFactory({ toDataUri: "data:image/png;base64,REAL" })
    };
    const result = await renderSvgToPng(CLEAN_SVG, {}, deps);
    expect(result.ok).toBe(true);
    expect(result.fallback).toBe(false);
    expect(result.dataUri).toBe("data:image/png;base64,REAL");
    expect(result.width).toBe(100);
    expect(result.height).toBe(80);
  });

  it("rejects a malicious SVG and reports a fallback (never rasterizes it)", async () => {
    const createImage = vi.fn(fakeImageFactory("load"));
    const result = await renderSvgToPng(MALICIOUS_SVG, {}, { createImage, createCanvas: fakeCanvasFactory({}) });
    expect(result.ok).toBe(false);
    expect(result.fallback).toBe(true);
    // The image element must never be constructed for rejected SVG.
    expect(createImage).not.toHaveBeenCalled();
  });

  it("falls back when the 2D context is unavailable", async () => {
    const result = await renderSvgToPng(
      CLEAN_SVG,
      {},
      { createImage: fakeImageFactory("load"), createCanvas: fakeCanvasFactory({ withContext: false }) }
    );
    expect(result.ok).toBe(false);
    expect(result.fallback).toBe(true);
    expect(result.reason).toMatch(/context/i);
  });

  it("falls back when the image fails to load", async () => {
    const result = await renderSvgToPng(
      CLEAN_SVG,
      {},
      { createImage: fakeImageFactory("error"), createCanvas: fakeCanvasFactory({}) }
    );
    expect(result.ok).toBe(false);
    expect(result.fallback).toBe(true);
    expect(result.reason).toMatch(/load/i);
  });

  it("falls back when canvas export throws (tainted canvas)", async () => {
    const result = await renderSvgToPng(
      CLEAN_SVG,
      {},
      { createImage: fakeImageFactory("load"), createCanvas: fakeCanvasFactory({ throwOnDraw: true }) }
    );
    expect(result.ok).toBe(false);
    expect(result.fallback).toBe(true);
  });
});
