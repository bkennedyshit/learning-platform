import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import SafeSvg from "../components/SafeSvg";
import { recheckSvg } from "../lib/safeSvg";
import { normalizeTurnResponse } from "../lib/agentClient";

const CLEAN_SVG =
  '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">' +
  '<rect x="10" y="10" width="80" height="80" fill="#4c8bf5"/><text x="20" y="55">A</text></svg>';

const MALICIOUS_SVG =
  '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" onload="alert(1)">' +
  '<script>alert(2)</script><foreignObject><iframe src="http://evil"></iframe></foreignObject></svg>';

describe("SafeSvg / recheckSvg", () => {
  it("accepts a clean allowlisted SVG", () => {
    const result = recheckSvg(CLEAN_SVG);
    expect(result.ok).toBe(true);
    expect(result.sanitized).toContain("<svg");
  });

  it("rejects SVG with scripts, event handlers, and foreignObject", () => {
    const result = recheckSvg(MALICIOUS_SVG);
    expect(result.ok).toBe(false);
    expect(result.violations.length).toBeGreaterThan(0);
  });

  it("renders a clean SVG as an <img>, never as raw markup", () => {
    render(<SafeSvg source={CLEAN_SVG} altText="clean diagram" />);
    const img = screen.getByTestId("safe-svg") as HTMLImageElement;
    expect(img.tagName).toBe("IMG");
    expect(img.getAttribute("src")?.startsWith("data:image/svg+xml")).toBe(true);
  });

  it("shows a fallback (no <img>) for malicious SVG", () => {
    render(<SafeSvg source={MALICIOUS_SVG} altText="unsafe diagram" />);
    expect(screen.getByTestId("safe-svg-rejected")).toBeTruthy();
    expect(screen.queryByTestId("safe-svg")).toBeNull();
  });
});

describe("normalizeTurnResponse", () => {
  it("fills safe defaults for a missing/partial payload", () => {
    const view = normalizeTurnResponse(undefined);
    expect(view.turns).toEqual([]);
    expect(view.toolSummaries).toEqual([]);
    expect(view.citations).toEqual([]);
    expect(view.artifacts).toEqual([]);
    expect(view.whyNext).toBe("");
    expect(view.plan).toBeUndefined();
  });

  it("passes through well-formed fields and drops malformed ones", () => {
    const view = normalizeTurnResponse({
      turns: [{ id: "t1", sessionId: "s1", index: 0, author: "agent", content: "hi", createdAt: "2026-09-01T00:00:00.000Z" }],
      toolSummaries: [{ toolName: "tutor.explain", ok: true, summary: "Explained" }, { bogus: true }],
      citations: [{ lessonId: "L1", passageId: "p1" }, { nope: 1 }],
      whyNext: "because"
    });
    expect(view.turns).toHaveLength(1);
    expect(view.toolSummaries).toHaveLength(1);
    expect(view.citations).toHaveLength(1);
    expect(view.whyNext).toBe("because");
  });
});
