// Lossless size reduction for the MathML that marked-katex-extension emits.
//
// Every equation is rendered as
//   <span class="katex"><math xmlns="http://www.w3.org/1998/Math/MathML" ...>...</math></span>
// and the lesson HTML ships twice per page (once as DOM, once inside the RSC
// flight payload where each "<" costs six bytes as \u003c), so per-equation
// overhead is multiplied. Two parts of that markup carry no information:
//
//  * The xmlns attribute. The HTML parser places <math> in the MathML
//    namespace by itself; the attribute is only needed for XML/XHTML parsing.
//  * The <span class="katex"> shell. No stylesheet here targets it (KaTeX CSS
//    is not loaded; math is native MathML), and the one layout rule that did
//    (.katex:has(> math[display="block"])) duplicated the math[display="block"]
//    rule in globals.css.
//
// The <semantics>/<annotation encoding="application/x-tex"> TeX source and all
// presentation attributes (stretchy, mathvariant, display, ...) are preserved,
// so rendering, text selection, copy-as-TeX and assistive-technology behavior
// are unchanged.

const MATHML_XMLNS_ON_MATH = /<math xmlns="http:\/\/www\.w3\.org\/1998\/Math\/MathML"/g;
const KATEX_SHELL = /<span class="katex">(<math\b[^>]*>[\s\S]*?<\/math>)<\/span>/g;

export function compactMathHtml(html) {
  return html.replace(KATEX_SHELL, "$1").replace(MATHML_XMLNS_ON_MATH, "<math");
}

export function countMath(html) {
  return (html.match(/<math\b/g) || []).length;
}

/** True when markup still has the redundant parts (used to detect KaTeX output drift). */
export function hasUncompactedMath(html) {
  return /<math xmlns="http:\/\/www\.w3\.org\/1998\/Math\/MathML"/.test(html) || /<span class="katex">/.test(html);
}
