import { describe, it, expect } from 'vitest';
import { compactMathHtml, countMath, hasUncompactedMath } from '../../scripts/compact-math.mjs';
import { lessons } from '../lib/manifest';

const NS = 'http://www.w3.org/1998/Math/MathML';
const inline =
  `<span class="katex"><math xmlns="${NS}"><semantics><mrow><mi>x</mi></mrow>` +
  `<annotation encoding="application/x-tex">x</annotation></semantics></math></span>`;
const block =
  `<span class="katex"><math xmlns="${NS}" display="block"><semantics><mrow><mo stretchy="false">(</mo><mi>y</mi><mo stretchy="false">)</mo></mrow>` +
  `<annotation encoding="application/x-tex">(y)</annotation></semantics></math></span>`;

describe('compactMathHtml', () => {
  it('removes the redundant xmlns and the unstyled katex shell, nothing else', () => {
    const out = compactMathHtml(`<p>See ${inline} and:</p>\n<p>${block}</p>`);
    expect(out).toBe(
      '<p>See <math><semantics><mrow><mi>x</mi></mrow><annotation encoding="application/x-tex">x</annotation></semantics></math> and:</p>\n' +
        '<p><math display="block"><semantics><mrow><mo stretchy="false">(</mo><mi>y</mi><mo stretchy="false">)</mo></mrow>' +
        '<annotation encoding="application/x-tex">(y)</annotation></semantics></math></p>',
    );
  });

  it('keeps the TeX annotation, display mode and presentation attributes', () => {
    const out = compactMathHtml(block);
    expect(out).toContain('display="block"');
    expect(out).toContain('stretchy="false"');
    expect(out).toContain('<annotation encoding="application/x-tex">(y)</annotation>');
  });

  it('is idempotent and leaves non-math markup alone', () => {
    const doc = `<h2>Title</h2><p>Plain <span class="other">text</span></p>${inline}`;
    const once = compactMathHtml(doc);
    expect(compactMathHtml(once)).toBe(once);
    expect(once).toContain('<span class="other">text</span>');
  });

  it('does not touch code samples that merely mention math markup', () => {
    const code = '<pre><code>&lt;math xmlns="x"&gt;&lt;/math&gt;</code></pre>';
    expect(compactMathHtml(code)).toBe(code);
  });

  it('preserves the equation count', () => {
    const doc = `${inline}${block}${inline}`;
    expect(countMath(compactMathHtml(doc))).toBe(countMath(doc));
    expect(countMath(doc)).toBe(3);
  });
});

describe('generated lesson math', () => {
  const withMath = lessons.filter((l) => l.html.includes('<math'));

  it('has math to check', () => {
    expect(withMath.length).toBeGreaterThan(50);
  });

  it('carries no redundant xmlns or katex shell', () => {
    for (const l of lessons) expect(hasUncompactedMath(l.html), l.slug).toBe(false);
  });

  it('keeps one TeX annotation and one semantics wrapper per equation', () => {
    for (const l of withMath) {
      const n = countMath(l.html);
      expect((l.html.match(/<annotation encoding="application\/x-tex">/g) ?? []).length, l.slug).toBe(n);
      expect((l.html.match(/<semantics>/g) ?? []).length, l.slug).toBe(n);
    }
  });

  it('parses every equation into the MathML namespace without an explicit xmlns', () => {
    // Sample across the catalog, including the largest lesson.
    const biggest = [...withMath].sort((a, b) => b.html.length - a.html.length)[0];
    const sample = [biggest, ...withMath.filter((_, i) => i % 25 === 0)];
    for (const l of sample) {
      const host = document.createElement('div');
      host.innerHTML = l.html;
      const maths = [...host.querySelectorAll('math')];
      expect(maths.length, l.slug).toBe(countMath(l.html));
      for (const m of maths) {
        expect(m.namespaceURI, l.slug).toBe(NS);
        expect(m.querySelector('annotation')?.getAttribute('encoding'), l.slug).toBe('application/x-tex');
      }
    }
  });
});
