import assert from "node:assert/strict";
import test from "node:test";
import { sanitizeMermaid, sanitizeSvg, DEFAULT_SVG_LIMITS } from "./sanitizer.js";

test("accepts a clean labeled SVG and returns sanitized source", () => {
  const svg =
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="unit circle">' +
    '<circle cx="50" cy="50" r="40" fill="none" stroke="black" stroke-width="2"/>' +
    '<text x="50" y="55" text-anchor="middle" font-size="10">r</text></svg>';
  const result = sanitizeSvg(svg);
  assert.equal(result.ok, true, result.violations.join("; "));
  assert.ok(result.sanitized?.includes("<circle"));
  assert.ok(!result.sanitized?.includes("script"));
});

test("rejects <script> inside SVG", () => {
  const result = sanitizeSvg('<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>');
  assert.equal(result.ok, false);
  assert.ok(result.violations.some((v) => v.includes("<script>")));
});

test("rejects event handler attributes", () => {
  const result = sanitizeSvg('<svg xmlns="http://www.w3.org/2000/svg" onload="evil()"></svg>');
  assert.equal(result.ok, false);
  assert.ok(result.violations.some((v) => v.includes("event attribute")));
});

test("rejects foreignObject", () => {
  const result = sanitizeSvg(
    '<svg xmlns="http://www.w3.org/2000/svg"><foreignObject><div>x</div></foreignObject></svg>'
  );
  assert.equal(result.ok, false);
  assert.ok(result.violations.some((v) => v.includes("foreignObject")));
});

test("rejects external references via href and url()", () => {
  const hrefResult = sanitizeSvg(
    '<svg xmlns="http://www.w3.org/2000/svg"><use href="http://evil.example/x.svg"/></svg>'
  );
  assert.equal(hrefResult.ok, false);
  assert.ok(hrefResult.violations.some((v) => v.includes("external reference")));

  const urlResult = sanitizeSvg(
    '<svg xmlns="http://www.w3.org/2000/svg"><rect fill="url(http://evil.example/x)"/></svg>'
  );
  assert.equal(urlResult.ok, false);
  assert.ok(urlResult.violations.some((v) => v.includes("unsafe value")));

  // Internal url(#id) references remain allowed.
  const internal = sanitizeSvg(
    '<svg xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g"><stop offset="0" stop-color="red"/></linearGradient></defs><rect fill="url(#g)" width="10" height="10"/></svg>'
  );
  assert.equal(internal.ok, true, internal.violations.join("; "));
});

test("rejects animation elements", () => {
  const result = sanitizeSvg(
    '<svg xmlns="http://www.w3.org/2000/svg"><rect width="10" height="10"><animate attributeName="x" to="100"/></rect></svg>'
  );
  assert.equal(result.ok, false);
  assert.ok(result.violations.some((v) => v.includes("<animate>")));
});

test("rejects doctype and entities", () => {
  const doctype = sanitizeSvg('<!DOCTYPE svg><svg xmlns="http://www.w3.org/2000/svg"></svg>');
  assert.equal(doctype.ok, false);
  assert.ok(doctype.violations.some((v) => v.includes("doctype")));

  const entity = sanitizeSvg(
    '<!DOCTYPE svg [<!ENTITY x "boom">]><svg xmlns="http://www.w3.org/2000/svg"><text>&x;</text></svg>'
  );
  assert.equal(entity.ok, false);
});

test("enforces byte and node limits", () => {
  const bytes = sanitizeSvg('<svg xmlns="http://www.w3.org/2000/svg"></svg>', {
    ...DEFAULT_SVG_LIMITS,
    maxBytes: 10
  });
  assert.equal(bytes.ok, false);
  assert.ok(bytes.violations.some((v) => v.includes("maxBytes")));

  const manyNodes = `<svg xmlns="http://www.w3.org/2000/svg">${"<rect/>".repeat(20)}</svg>`;
  const nodes = sanitizeSvg(manyNodes, { ...DEFAULT_SVG_LIMITS, maxNodes: 5 });
  assert.equal(nodes.ok, false);
  assert.ok(nodes.violations.some((v) => v.includes("maxNodes")));
});

test("enforces viewBox dimension limits", () => {
  const result = sanitizeSvg('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 999999 10"></svg>');
  assert.equal(result.ok, false);
  assert.ok(result.violations.some((v) => v.includes("viewBox")));
});

test("mermaid: accepts allowlisted flowchart, rejects click/directives/html", () => {
  const ok = sanitizeMermaid("flowchart TD\n A[Start] --> B[End]");
  assert.equal(ok.ok, true, ok.violations.join("; "));
  assert.equal(ok.diagramType, "flowchart");

  const click = sanitizeMermaid('flowchart TD\n A --> B\n click A "http://evil.example"');
  assert.equal(click.ok, false);
  assert.ok(click.violations.some((v) => v.includes("click")));

  const directive = sanitizeMermaid('%%{init: {"theme":"dark"}}%%\nflowchart TD\n A --> B');
  assert.equal(directive.ok, false);
  assert.ok(directive.violations.some((v) => v.includes("directive")));

  const html = sanitizeMermaid("flowchart TD\n A --> B\n B --> C<script>alert(1)</script>");
  assert.equal(html.ok, false);

  const badType = sanitizeMermaid("gitGraph\n commit");
  assert.equal(badType.ok, false);
  assert.ok(badType.violations.some((v) => v.includes("not allowed")));
});
