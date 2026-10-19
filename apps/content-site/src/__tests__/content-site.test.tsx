import { describe, it, expect, vi, afterEach } from 'vitest';
import { render, screen, cleanup } from '@testing-library/react';
import LessonPage, { generateMetadata } from '../app/[slug]/page';
import SubjectPage, { generateMetadata as generateSubjectMetadata } from '../app/subject/[slug]/page';
import sitemap from '../app/sitemap';
import { lessons, subjects, getLesson } from '../lib/manifest';
import { SITE_URL } from '../lib/site';

afterEach(() => cleanup());

vi.mock('next/link', () => {
  return {
    default: ({ children, href }: { children: React.ReactNode; href: string }) => {
      return <a href={href}>{children}</a>;
    },
  };
});

const sampleLesson = lessons[0];

describe('Content Site - generated corpus content', () => {
  it('loads a substantial catalog from the corpus', () => {
    expect(subjects.length).toBeGreaterThan(20);
    expect(lessons.length).toBeGreaterThan(100);
  });

  it('server-rendered lesson page shows title, metadata, and content', async () => {
    const params = Promise.resolve({ slug: sampleLesson.slug });
    const jsx = await LessonPage({ params });
    render(jsx);

    expect(screen.getAllByText(sampleLesson.title).length).toBeGreaterThan(0);
    expect(screen.getByText(`Catalog: ${sampleLesson.catalog}`)).toBeDefined();
    expect(screen.getByText(`Subject: ${sampleLesson.subject}`)).toBeDefined();
    expect(sampleLesson.html.length).toBeGreaterThan(0);
  });

  it('sitemap lists home, resources, indexable hubs and indexable lessons only', async () => {
    const sm = await sitemap();
    const indexableLessons = lessons.filter((l) => l.indexable);
    const indexableSubjects = subjects.filter((s) => s.indexable);
    expect(sm.length).toBe(1 + 2 + indexableSubjects.length + indexableLessons.length);

    const urls = sm.map((s) => s.url);
    expect(new Set(urls).size).toBe(urls.length);
    expect(urls).toContain(`${SITE_URL}/${indexableLessons[0].slug}`);
    expect(urls).toContain(`${SITE_URL}/subject/${indexableSubjects[0].slug}`);
    for (const l of lessons.filter((x) => !x.indexable)) {
      expect(urls).not.toContain(`${SITE_URL}/${l.slug}`);
    }
    for (const s of subjects.filter((x) => !x.indexable)) {
      expect(urls).not.toContain(`${SITE_URL}/subject/${s.slug}`);
    }
  });

  it('sitemap never fabricates lastModified for lessons or hubs', async () => {
    const sm = await sitemap();
    for (const entry of sm) {
      if (entry.url.includes('/resources')) {
        expect(entry.lastModified).toMatch(/^\d{4}-\d{2}-\d{2}$/);
      } else {
        expect(entry.lastModified).toBeUndefined();
      }
    }
  });

  it('metadata is present for lessons', async () => {
    const params = Promise.resolve({ slug: sampleLesson.slug });
    const meta = await generateMetadata({ params });

    expect(meta.title).toBe(`${sampleLesson.title} - Learning Platform`);
    expect(meta.description).toBeTruthy();
    expect(meta.alternates?.canonical).toBe(`${SITE_URL}/${sampleLesson.slug}`);
  });
});

describe('Content Site - index-promotion gate', () => {
  it('flags every authoring stub and scaffold lesson as noindex', () => {
    for (const l of lessons) {
      const isStub = /Ready for expansion/i.test(l.html) || /TODO:\s*(Expand|Add)/i.test(l.html);
      const isScaffold = /The foundational building block of this unit/i.test(l.html);
      if (isStub || isScaffold) expect(l.indexable, l.slug).toBe(false);
      if (l.indexable) expect(l.wordCount, l.slug).toBeGreaterThanOrEqual(400);
    }
    expect(lessons.some((l) => l.indexable)).toBe(true);
    expect(lessons.some((l) => !l.indexable)).toBe(true);
  });

  it('emits robots noindex,follow for gated lessons and none for indexable ones', async () => {
    const gated = lessons.find((l) => !l.indexable)!;
    const open = lessons.find((l) => l.indexable)!;
    const gatedMeta = await generateMetadata({ params: Promise.resolve({ slug: gated.slug }) });
    const openMeta = await generateMetadata({ params: Promise.resolve({ slug: open.slug }) });
    expect(gatedMeta.robots).toEqual({ index: false, follow: true });
    expect(openMeta.robots).toBeUndefined();
  });

  it('emits robots noindex,follow for hubs with no indexable lessons', async () => {
    const empty = subjects.find((s) => !s.indexable);
    const full = subjects.find((s) => s.indexable)!;
    if (empty) {
      const meta = await generateSubjectMetadata({ params: Promise.resolve({ slug: empty.slug }) });
      expect(meta.robots).toEqual({ index: false, follow: true });
    }
    const meta = await generateSubjectMetadata({ params: Promise.resolve({ slug: full.slug }) });
    expect(meta.robots).toBeUndefined();
  });
});

describe('Content Site - internal linking', () => {
  const knownPaths = new Set([
    '/', '/resources', '/tools',
    ...subjects.map((s) => `/subject/${s.slug}`),
    ...lessons.map((l) => `/${l.slug}`),
  ]);

  it('lesson bodies contain no relative or dangling internal links', () => {
    for (const l of lessons) {
      for (const m of l.html.matchAll(/<a\b[^>]*\bhref="([^"]*)"/g)) {
        const href = m[1];
        if (/^(https?:|mailto:|#)/.test(href)) continue;
        expect(href.startsWith('/'), `${l.slug}: ${href}`).toBe(true);
        expect(knownPaths.has(href.split(/[?#]/)[0]), `${l.slug}: ${href}`).toBe(true);
      }
    }
  });

  it('subject slugs are unique', () => {
    expect(new Set(subjects.map((s) => s.slug)).size).toBe(subjects.length);
  });

  it('every hub lists all of its lessons, every lesson belongs to its hub', () => {
    for (const s of subjects) {
      const expected = lessons.filter((l) => l.subjectSlug === s.slug).map((l) => l.slug).sort();
      expect(s.lessons.map((l) => l.slug).sort()).toEqual(expected);
    }
  });

  it('hub page links to every indexable lesson', async () => {
    const subject = subjects.find((s) => s.indexable)!;
    render(await SubjectPage({ params: Promise.resolve({ slug: subject.slug }) }));
    const hrefs = screen.getAllByRole('link').map((a) => a.getAttribute('href'));
    for (const l of subject.lessons.filter((x) => x.indexable)) {
      expect(hrefs).toContain(`/${l.slug}`);
    }
  });

  it('lesson page links to its hub, prev/next and related lessons in the same subject', async () => {
    const lesson = lessons.find((l) => l.indexable && l.prevSlug && l.nextSlug && l.relatedSlugs.length)!;
    render(await LessonPage({ params: Promise.resolve({ slug: lesson.slug }) }));
    const hrefs = screen.getAllByRole('link').map((a) => a.getAttribute('href'));
    expect(hrefs).toContain(`/subject/${lesson.subjectSlug}`);
    expect(hrefs).toContain(`/${lesson.prevSlug}`);
    expect(hrefs).toContain(`/${lesson.nextSlug}`);
    for (const r of lesson.relatedSlugs) {
      expect(hrefs).toContain(`/${r}`);
      expect(getLesson(r)!.subjectSlug).toBe(lesson.subjectSlug);
      expect(getLesson(r)!.indexable).toBe(true);
    }
  });
});


// Rewrite batches (see .kiro/learning-content-rewrite): each rewritten lesson
// must stay promoted through the existing gate and keep its teaching structure.
describe('Content Site - rewrite batch: Algebra I', () => {
  const batch = [
    '141-the-language-of-algebra',
    '142-linear-equations',
    '143-linear-inequalities',
    '144-functions-relations',
    '145-linear-functions-graphing',
    '146-systems-of-equations',
    '147-exponents-polynomials',
    '148-factoring-quadratics',
  ];

  it('keeps the chapter order, subject, tier, and prev/next chain', () => {
    const hub = subjects.find((s) => s.slug === 'algebra-i')!;
    expect(hub.lessons.map((l) => l.slug)).toEqual(batch);
    batch.forEach((slug, i) => {
      const l = getLesson(slug)!;
      expect(l.subject).toBe('Algebra I');
      expect(l.audienceTier).toBe('9-12');
      expect(l.chapter).toBe(`14.${i + 1}`);
      expect(l.prevSlug).toBe(batch[i - 1] ?? null);
      expect(l.nextSlug).toBe(batch[i + 1] ?? null);
    });
  });

  it('every lesson is indexable, substantial, and free of scaffold residue', () => {
    for (const slug of batch) {
      const l = getLesson(slug)!;
      expect(l.indexable, slug).toBe(true);
      expect(l.wordCount, slug).toBeGreaterThanOrEqual(500);
      expect(l.html, slug).not.toMatch(/System Overlay|foundational building block|Ready for expansion|TODO/i);
    }
  });

  it('every lesson has worked examples, misconceptions, practice, an answer key, and a hub link', () => {
    for (const slug of batch) {
      const html = getLesson(slug)!.html;
      expect(html.match(/<h3[^>]*>Example \d/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      expect(html, slug).toMatch(/<h2[^>]*>Common misconceptions/);
      expect(html, slug).toMatch(/<h2[^>]*>Practice<\/h2>/);
      expect(html, slug).toMatch(/<summary>Answer key/);
      expect(html, slug).toContain('href="/subject/algebra-i"');
    }
  });

  it('the Algebra I hub is indexable and listed in the sitemap', async () => {
    const urls = (await sitemap()).map((s) => s.url);
    expect(subjects.find((s) => s.slug === 'algebra-i')!.indexable).toBe(true);
    expect(urls).toContain(`${SITE_URL}/subject/algebra-i`);
    for (const slug of batch) expect(urls).toContain(`${SITE_URL}/${slug}`);
  });
});


describe('Content Site - rewrite batch: Algebra II & Pre-Calculus', () => {
  const hubSlug = 'algebra-ii-and-pre-calculus';
  const batch: Array<[string, string]> = [
    ['161-polynomial-functions', '16.1 - Polynomial Functions'],
    ['162-rational-functions', '16.2 - Rational Functions'],
    ['163-exponential-logarithmic-functions', '16.3 - Exponential & Logarithmic Functions'],
    ['164-trigonometry-the-unit-circle', '16.4 - Trigonometry — The Unit Circle'],
    ['165-trig-identities-equations', '16.5 - Trig Identities & Equations'],
    ['166-conic-sections', '16.6 - Conic Sections'],
    ['167-sequences-series-the-binomial-theorem', '16.7 - Sequences, Series & the Binomial Theorem'],
    ['168-limits-introduction-to-calculus', '16.8 - Limits & Introduction to Calculus'],
  ];
  const slugs = batch.map(([slug]) => slug);

  it('keeps slugs, titles, chapter order, subject, tier, and the prev/next chain', () => {
    const hub = subjects.find((s) => s.slug === hubSlug)!;
    expect(hub.lessons.map((l) => l.slug)).toEqual(slugs);
    batch.forEach(([slug, title], i) => {
      const l = getLesson(slug)!;
      expect(l.title).toBe(title);
      expect(l.subject).toBe('Algebra II & Pre-Calculus');
      expect(l.audienceTier).toBe('9-12');
      expect(l.chapter).toBe(`16.${i + 1}`);
      expect(l.prevSlug).toBe(slugs[i - 1] ?? null);
      expect(l.nextSlug).toBe(slugs[i + 1] ?? null);
    });
  });

  it('every lesson is indexable, substantial, and free of scaffold residue', () => {
    for (const slug of slugs) {
      const l = getLesson(slug)!;
      expect(l.indexable, slug).toBe(true);
      expect(l.wordCount, slug).toBeGreaterThanOrEqual(500);
      expect(l.html, slug).not.toMatch(/System Overlay|foundational building block|Ready for expansion|TODO|katex-error/i);
    }
  });

  it('every lesson has worked examples, misconceptions, 3+ practice tasks, an answer key, and a hub link', () => {
    for (const slug of slugs) {
      const html = getLesson(slug)!.html;
      expect(html.match(/<h3[^>]*>Example \d/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      expect(html, slug).toMatch(/<h2[^>]*>Common misconceptions/);
      const practice = html.split(/<h2[^>]*>Practice<\/h2>/)[1]?.split('<details>')[0] ?? '';
      expect(practice.match(/<li>/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(3);
      expect(html, slug).toMatch(/<summary>Answer key/);
      expect(html, slug).toContain(`href="/subject/${hubSlug}"`);
    }
  });

  it('the Algebra II & Pre-Calculus hub is indexable and listed in the sitemap', async () => {
    const urls = (await sitemap()).map((s) => s.url);
    expect(subjects.find((s) => s.slug === hubSlug)!.indexable).toBe(true);
    expect(urls).toContain(`${SITE_URL}/subject/${hubSlug}`);
    for (const slug of slugs) expect(urls).toContain(`${SITE_URL}/${slug}`);
  });
});


describe('Content Site - rewrite batch: Geometry', () => {
  const hubSlug = 'geometry';
  const batch: Array<[string, string]> = [
    ['151-foundations-of-geometry', '15.1 - Foundations of Geometry'],
    ['152-reasoning-proof', '15.2 - Reasoning & Proof'],
    ['153-parallel-perpendicular-lines', '15.3 - Parallel & Perpendicular Lines'],
    ['154-triangles', '15.4 - Triangles'],
    ['155-similarity-proportions', '15.5 - Similarity & Proportions'],
    ['156-right-triangles-trigonometry', '15.6 - Right Triangles & Trigonometry'],
    ['157-circles', '15.7 - Circles'],
    ['158-area-volume-coordinate-geometry', '15.8 - Area, Volume & Coordinate Geometry'],
  ];
  const slugs = batch.map(([slug]) => slug);

  it('keeps slugs, titles, chapter order, subject, tier, and the prev/next chain', () => {
    const hub = subjects.find((s) => s.slug === hubSlug)!;
    expect(hub.lessons.map((l) => l.slug)).toEqual(slugs);
    batch.forEach(([slug, title], i) => {
      const l = getLesson(slug)!;
      expect(l.title).toBe(title);
      expect(l.subject).toBe('Geometry');
      expect(l.audienceTier).toBe('9-12');
      expect(l.chapter).toBe(`15.${i + 1}`);
      expect(l.prevSlug).toBe(slugs[i - 1] ?? null);
      expect(l.nextSlug).toBe(slugs[i + 1] ?? null);
    });
  });

  it('every lesson is indexable, substantial, and free of scaffold residue', () => {
    for (const slug of slugs) {
      const l = getLesson(slug)!;
      expect(l.indexable, slug).toBe(true);
      expect(l.wordCount, slug).toBeGreaterThanOrEqual(500);
      expect(l.html, slug).not.toMatch(/System Overlay|foundational building block|Ready for expansion|TODO|katex-error/i);
    }
  });

  it('every lesson has worked examples, 2+ misconceptions, 3+ practice tasks, an answer key, and a hub link', () => {
    for (const slug of slugs) {
      const html = getLesson(slug)!.html;
      expect(html.match(/<h3[^>]*>Example \d/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      const misconceptions = html.split(/<h2[^>]*>Common misconceptions/)[1]?.split('<h2')[0] ?? '';
      expect(misconceptions.match(/<li>/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      const practice = html.split(/<h2[^>]*>Practice<\/h2>/)[1]?.split('<details>')[0] ?? '';
      expect(practice.match(/<li>/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(3);
      expect(html, slug).toMatch(/<summary>Answer key/);
      expect(html, slug).toContain(`href="/subject/${hubSlug}"`);
    }
  });

  it('the Geometry hub is indexable and listed in the sitemap', async () => {
    const urls = (await sitemap()).map((s) => s.url);
    expect(subjects.find((s) => s.slug === hubSlug)!.indexable).toBe(true);
    expect(urls).toContain(`${SITE_URL}/subject/${hubSlug}`);
    for (const slug of slugs) expect(urls).toContain(`${SITE_URL}/${slug}`);
  });
});


describe('Content Site - rewrite batch: Pre-Algebra', () => {
  const hubSlug = 'pre-algebra';
  const batch: Array<[string, string]> = [
    ['131-ratios-rates-proportions', '13.1 - Ratios, Rates & Proportions'],
    ['132-the-number-system', '13.2 - The Number System'],
    ['133-fractions-decimals-percent', '13.3 - Fractions, Decimals & Percent'],
    ['134-expressions-variables', '13.4 - Expressions & Variables'],
    ['135-equations-inequalities', '13.5 - Equations & Inequalities'],
    ['136-geometry-foundations', '13.6 - Geometry Foundations'],
    ['137-statistics-data', '13.7 - Statistics & Data'],
    ['138-probability-intro', '13.8 - Probability Intro'],
  ];
  const slugs = batch.map(([slug]) => slug);

  it('keeps slugs, titles, chapter order, subject, tier, and the prev/next chain', () => {
    const hub = subjects.find((s) => s.slug === hubSlug)!;
    expect(hub.lessons.map((l) => l.slug)).toEqual(slugs);
    batch.forEach(([slug, title], i) => {
      const l = getLesson(slug)!;
      expect(l.title).toBe(title);
      expect(l.subject).toBe('Pre-Algebra');
      expect(l.audienceTier).toBe('9-12');
      expect(l.chapter).toBe(`13.${i + 1}`);
      expect(l.prevSlug).toBe(slugs[i - 1] ?? null);
      expect(l.nextSlug).toBe(slugs[i + 1] ?? null);
    });
  });

  it('every lesson is indexable, substantial, and free of scaffold residue', () => {
    for (const slug of slugs) {
      const l = getLesson(slug)!;
      expect(l.indexable, slug).toBe(true);
      expect(l.wordCount, slug).toBeGreaterThanOrEqual(500);
      expect(l.html, slug).not.toMatch(/System Overlay|foundational building block|Ready for expansion|TODO|katex-error/i);
    }
  });

  it('every lesson has worked examples, 2+ misconceptions, 3+ practice tasks, an answer key, and a hub link', () => {
    for (const slug of slugs) {
      const html = getLesson(slug)!.html;
      expect(html.match(/<h3[^>]*>Example \d/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      const misconceptions = html.split(/<h2[^>]*>Common misconceptions/)[1]?.split('<h2')[0] ?? '';
      expect(misconceptions.match(/<li>/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      const practice = html.split(/<h2[^>]*>Practice<\/h2>/)[1]?.split('<details>')[0] ?? '';
      expect(practice.match(/<li>/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(3);
      expect(html, slug).toMatch(/<summary>Answer key/);
      expect(html, slug).toContain(`href="/subject/${hubSlug}"`);
    }
  });

  it('the Pre-Algebra hub is indexable and listed in the sitemap', async () => {
    const urls = (await sitemap()).map((s) => s.url);
    expect(subjects.find((s) => s.slug === hubSlug)!.indexable).toBe(true);
    expect(urls).toContain(`${SITE_URL}/subject/${hubSlug}`);
    for (const slug of slugs) expect(urls).toContain(`${SITE_URL}/${slug}`);
  });
});



describe('Content Site - rewrite batch: Statistics & Probability', () => {
  const hubSlug = 'statistics-and-probability';
  const batch: Array<[string, string]> = [
    ['171-exploring-data-1-variable', '17.1 - Exploring Data (1-Variable)'],
    ['172-exploring-data-2-variable', '17.2 - Exploring Data (2-Variable)'],
    ['173-sampling-experimental-design', '17.3 - Sampling & Experimental Design'],
    ['174-probability', '17.4 - Probability'],
    ['175-discrete-random-variables', '17.5 - Discrete Random Variables'],
    ['176-normal-distribution-sampling-distributions', '17.6 - Normal Distribution & Sampling Distributions'],
    ['177-confidence-intervals', '17.7 - Confidence Intervals'],
    ['178-significance-tests', '17.8 - Significance Tests'],
  ];
  const slugs = batch.map(([slug]) => slug);

  it('keeps slugs, titles, chapter order, subject, tier, and the prev/next chain', () => {
    const hub = subjects.find((s) => s.slug === hubSlug)!;
    expect(hub.lessons.map((l) => l.slug)).toEqual(slugs);
    batch.forEach(([slug, title], i) => {
      const l = getLesson(slug)!;
      expect(l.title).toBe(title);
      expect(l.subject).toBe('Statistics & Probability');
      expect(l.audienceTier).toBe('9-12');
      expect(l.chapter).toBe(`17.${i + 1}`);
      expect(l.prevSlug).toBe(slugs[i - 1] ?? null);
      expect(l.nextSlug).toBe(slugs[i + 1] ?? null);
    });
  });

  it('every lesson is indexable, substantial, and free of scaffold residue', () => {
    for (const slug of slugs) {
      const l = getLesson(slug)!;
      expect(l.indexable, slug).toBe(true);
      expect(l.wordCount, slug).toBeGreaterThanOrEqual(500);
      expect(l.html, slug).not.toMatch(/System Overlay|foundational building block|Ready for expansion|TODO|katex-error/i);
    }
  });

  it('every lesson has worked examples, 2+ misconceptions, 3+ practice tasks, an answer key, and a hub link', () => {
    for (const slug of slugs) {
      const html = getLesson(slug)!.html;
      expect(html.match(/<h3[^>]*>Example \d/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      const misconceptions = html.split(/<h2[^>]*>Common misconceptions/)[1]?.split('<h2')[0] ?? '';
      expect(misconceptions.match(/<li>/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      const practice = html.split(/<h2[^>]*>Practice<\/h2>/)[1]?.split('<details>')[0] ?? '';
      expect(practice.match(/<li>/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(3);
      expect(html, slug).toMatch(/<summary>Answer key/);
      expect(html, slug).toContain(`href="/subject/${hubSlug}"`);
    }
  });

  it('the Statistics & Probability hub is indexable and listed in the sitemap', async () => {
    const urls = (await sitemap()).map((s) => s.url);
    expect(subjects.find((s) => s.slug === hubSlug)!.indexable).toBe(true);
    expect(urls).toContain(`${SITE_URL}/subject/${hubSlug}`);
    for (const slug of slugs) expect(urls).toContain(`${SITE_URL}/${slug}`);
  });
});


describe('Content Site - rewrite batch: Early Numeracy K-5', () => {
  const hubSlug = 'early-numeracy-k-5';
  const batch: Array<[string, string]> = [
    ['app-021-number-sense-counting', 'APP-02.1 — Number Sense & Counting'],
    ['app-022-addition-subtraction', 'APP-02.2 — Addition & Subtraction'],
    ['app-023-multiplication-division', 'APP-02.3 — Multiplication & Division'],
    ['app-024-fractions-concepts-operations', 'APP-02.4 — Fractions — Concepts & Operations'],
    ['app-025-fractions-advanced-operations', 'APP-02.5 — Fractions — Advanced Operations'],
    ['app-026-decimals-place-value', 'APP-02.6 — Decimals & Place Value'],
    ['app-027-measurement-data', 'APP-02.7 — Measurement & Data'],
    ['app-028-geometry-coordinate-plane', 'APP-02.8 — Geometry & Coordinate Plane'],
  ];
  const slugs = batch.map(([slug]) => slug);

  it('keeps slugs, titles, chapter order, subject, tier, and the prev/next chain', () => {
    const hub = subjects.find((s) => s.slug === hubSlug)!;
    expect(hub.lessons.map((l) => l.slug)).toEqual(slugs);
    batch.forEach(([slug, title], i) => {
      const l = getLesson(slug)!;
      expect(l.title).toBe(title);
      expect(l.subject).toBe('Early Numeracy K-5');
      expect(l.audienceTier).toBe('9-12');
      expect(l.chapter).toBe(`2.${i + 1}`);
      expect(l.prevSlug).toBe(slugs[i - 1] ?? null);
      expect(l.nextSlug).toBe(slugs[i + 1] ?? null);
    });
  });

  it('every lesson is indexable, substantial, and free of scaffold residue', () => {
    for (const slug of slugs) {
      const l = getLesson(slug)!;
      expect(l.indexable, slug).toBe(true);
      expect(l.wordCount, slug).toBeGreaterThanOrEqual(500);
      expect(l.html, slug).not.toMatch(/System Overlay|foundational building block|Ready for expansion|TODO|katex-error|Visual Anchor/i);
    }
  });

  it('every lesson has worked examples, 2+ misconceptions, 3+ practice tasks, an answer key, an adult note, and a hub link', () => {
    for (const slug of slugs) {
      const html = getLesson(slug)!.html;
      expect(html.match(/<h3[^>]*>Example \d/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      const misconceptions = html.split(/<h2[^>]*>Common misconceptions/)[1]?.split('<h2')[0] ?? '';
      expect(misconceptions.match(/<li>/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      const practice = html.split(/<h2[^>]*>Practice<\/h2>/)[1]?.split('<details>')[0] ?? '';
      expect(practice.match(/<li>/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(3);
      expect(html, slug).toMatch(/<summary>Answer key/);
      expect(html, slug).toMatch(/Adult note/);
      expect(html, slug).toContain(`href="/subject/${hubSlug}"`);
    }
  });

  it('the Early Numeracy K-5 hub is indexable and listed in the sitemap', async () => {
    const urls = (await sitemap()).map((s) => s.url);
    expect(subjects.find((s) => s.slug === hubSlug)!.indexable).toBe(true);
    expect(urls).toContain(`${SITE_URL}/subject/${hubSlug}`);
    for (const slug of slugs) expect(urls).toContain(`${SITE_URL}/${slug}`);
  });
});



describe('Content Site - rewrite batch: Physical Science K-8', () => {
  const hubSlug = 'physical-science-k-8';
  const batch: Array<[string, string]> = [
    ['app-041-forces-motion-foundations', 'APP-04.1 — Forces & Motion — Foundations'],
    ['app-042-energy-forms-transfers', 'APP-04.2 — Energy — Forms & Transfers'],
    ['app-043-waves-light-sound', 'APP-04.3 — Waves — Light & Sound'],
    ['app-044-matter-properties-states', 'APP-04.4 — Matter — Properties & States'],
    ['app-045-forces-motion-newtons-laws', 'APP-04.5 — Forces & Motion — Newtons Laws'],
    ['app-046-atoms-elements-the-periodic-table', 'APP-04.6 — Atoms, Elements & the Periodic Table'],
    ['app-047-chemical-reactions', 'APP-04.7 — Chemical Reactions'],
    ['app-048-electricity-magnetism', 'APP-04.8 — Electricity & Magnetism'],
  ];
  const slugs = batch.map(([slug]) => slug);

  it('keeps slugs, titles, chapter order, subject, tier, and the prev/next chain', () => {
    const hub = subjects.find((s) => s.slug === hubSlug)!;
    expect(hub.lessons.map((l) => l.slug)).toEqual(slugs);
    batch.forEach(([slug, title], i) => {
      const l = getLesson(slug)!;
      expect(l.title).toBe(title);
      expect(l.subject).toBe('Physical Science K-8');
      expect(l.audienceTier).toBe('9-12');
      expect(l.chapter).toBe(`4.${i + 1}`);
      expect(l.prevSlug).toBe(slugs[i - 1] ?? null);
      expect(l.nextSlug).toBe(slugs[i + 1] ?? null);
    });
  });

  it('every lesson is indexable, substantial, and free of scaffold residue', () => {
    for (const slug of slugs) {
      const l = getLesson(slug)!;
      expect(l.indexable, slug).toBe(true);
      expect(l.wordCount, slug).toBeGreaterThanOrEqual(500);
      expect(l.html, slug).not.toMatch(/System Overlay|foundational building block|Ready for expansion|TODO|katex-error|Visual Anchor/i);
    }
  });

  it('every lesson has worked examples, 2+ misconceptions, 3+ practice tasks, an answer key, a safety note, sources, and nav links', () => {
    for (const [i, slug] of slugs.entries()) {
      const html = getLesson(slug)!.html;
      expect(html.match(/<h3[^>]*>Example \d/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      const misconceptions = html.split(/<h2[^>]*>Common misconceptions/)[1]?.split('<h2')[0] ?? '';
      expect(misconceptions.match(/<li>/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      const practice = html.split(/<h2[^>]*>Practice<\/h2>/)[1]?.split('<details>')[0] ?? '';
      expect(practice.match(/<li>/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(3);
      expect(html, slug).toMatch(/<summary>Answer key/);
      expect(html, slug).toMatch(/Safety note/);
      expect(html, slug).toMatch(/<h2[^>]*>Sources<\/h2>/);
      expect(html, slug).toContain(`href="/subject/${hubSlug}"`);
      if (i > 0) expect(html, slug).toContain(`href="/${slugs[i - 1]}"`);
      if (i < slugs.length - 1) expect(html, slug).toContain(`href="/${slugs[i + 1]}"`);
    }
  });

  it('the Physical Science K-8 hub is indexable and listed in the sitemap', async () => {
    const urls = (await sitemap()).map((s) => s.url);
    expect(subjects.find((s) => s.slug === hubSlug)!.indexable).toBe(true);
    expect(urls).toContain(`${SITE_URL}/subject/${hubSlug}`);
    for (const slug of slugs) expect(urls).toContain(`${SITE_URL}/${slug}`);
  });
});


describe('Content Site - rewrite batch: Earth Science', () => {
  const hubSlug = 'earth-science';
  const batch: Array<[string, string]> = [
    ['211-earth-as-a-system', '21.1 - Earth as a System'],
    ['212-plate-tectonics', '21.2 - Plate Tectonics'],
    ['213-rocks-minerals-the-rock-cycle', '21.3 - Rocks, Minerals & the Rock Cycle'],
    ['214-the-water-cycle-oceans', '21.4 - The Water Cycle & Oceans'],
    ['215-weather-atmosphere', '21.5 - Weather & Atmosphere'],
    ['216-the-solar-system-universe', '21.6 - The Solar System & Universe'],
    ['217-earths-history', '21.7 - Earths History'],
    ['218-human-impact-environmental-science', '21.8 - Human Impact & Environmental Science'],
  ];
  const slugs = batch.map(([slug]) => slug);

  it('keeps slugs, titles, chapter order, subject, tier, and the prev/next chain', () => {
    const hub = subjects.find((s) => s.slug === hubSlug)!;
    expect(hub.lessons.map((l) => l.slug)).toEqual(slugs);
    batch.forEach(([slug, title], i) => {
      const l = getLesson(slug)!;
      expect(l.title).toBe(title);
      expect(l.subject).toBe('Earth Science');
      expect(l.catalog).toBe('k12');
      expect(l.audienceTier).toBe('9-12');
      expect(l.chapter).toBe(`21.${i + 1}`);
      expect(l.prevSlug).toBe(slugs[i - 1] ?? null);
      expect(l.nextSlug).toBe(slugs[i + 1] ?? null);
    });
  });

  it('every lesson is indexable, substantial, and free of scaffold residue', () => {
    for (const slug of slugs) {
      const l = getLesson(slug)!;
      expect(l.indexable, slug).toBe(true);
      expect(l.wordCount, slug).toBeGreaterThanOrEqual(500);
      expect(l.html, slug).not.toMatch(/System Overlay|foundational building block|Ready for expansion|TODO|katex-error|Visual Anchor|Primary Element/i);
    }
  });

  it('every lesson has worked examples, 2+ misconceptions, 3+ practice tasks, an answer key, a safety note, sources, and nav links', () => {
    for (const [i, slug] of slugs.entries()) {
      const html = getLesson(slug)!.html;
      expect(html.match(/<h3[^>]*>Example \d/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      const misconceptions = html.split(/<h2[^>]*>Common misconceptions/)[1]?.split('<h2')[0] ?? '';
      expect(misconceptions.match(/<li>/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      const practice = html.split(/<h2[^>]*>Practice<\/h2>/)[1]?.split('<details>')[0] ?? '';
      expect(practice.match(/<li>/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(3);
      expect(html, slug).toMatch(/<summary>Answer key/);
      expect(html, slug).toMatch(/Safety note/);
      expect(html, slug).toMatch(/<h2[^>]*>Sources<\/h2>/);
      expect(html, slug).toContain(`href="/subject/${hubSlug}"`);
      if (i > 0) expect(html, slug).toContain(`href="/${slugs[i - 1]}"`);
      if (i < slugs.length - 1) expect(html, slug).toContain(`href="/${slugs[i + 1]}"`);
    }
  });

  it('the Earth Science hub is indexable and listed in the sitemap', async () => {
    const urls = (await sitemap()).map((s) => s.url);
    expect(subjects.find((s) => s.slug === hubSlug)!.indexable).toBe(true);
    expect(urls).toContain(`${SITE_URL}/subject/${hubSlug}`);
    for (const slug of slugs) expect(urls).toContain(`${SITE_URL}/${slug}`);
  });
});


describe('Content Site - rewrite batch: Life Science K-8', () => {
  const hubSlug = 'life-science-k-8';
  const batch: Array<[string, string]> = [
    ['app-031-living-vs-non-living-basic-needs', 'APP-03.1 — Living vs Non-Living & Basic Needs'],
    ['app-032-plants-structure-function-life-cycles', 'APP-03.2 — Plants — Structure, Function & Life Cycles'],
    ['app-033-animals-behavior-adaptations-life-cycles', 'APP-03.3 — Animals — Behavior, Adaptations & Life Cycles'],
    ['app-034-ecosystems-food-webs', 'APP-03.4 — Ecosystems & Food Webs'],
    ['app-035-cells-the-basic-unit-of-life', 'APP-03.5 — Cells — The Basic Unit of Life'],
    ['app-036-genetics-heredity', 'APP-03.6 — Genetics & Heredity'],
    ['app-037-evolution-natural-selection', 'APP-03.7 — Evolution & Natural Selection'],
    ['app-038-human-body-systems', 'APP-03.8 — Human Body Systems'],
  ];
  const slugs = batch.map(([slug]) => slug);

  it('keeps slugs, titles, chapter order, subject, tier, and the prev/next chain', () => {
    const hub = subjects.find((s) => s.slug === hubSlug)!;
    expect(hub.lessons.map((l) => l.slug)).toEqual(slugs);
    batch.forEach(([slug, title], i) => {
      const l = getLesson(slug)!;
      expect(l.title).toBe(title);
      expect(l.subject).toBe('Life Science K-8');
      expect(l.catalog).toBe('k12');
      expect(l.audienceTier).toBe('9-12');
      expect(l.chapter).toBe(`3.${i + 1}`);
      expect(l.prevSlug).toBe(slugs[i - 1] ?? null);
      expect(l.nextSlug).toBe(slugs[i + 1] ?? null);
    });
  });

  it('every lesson is indexable, substantial, and free of scaffold residue', () => {
    for (const slug of slugs) {
      const l = getLesson(slug)!;
      expect(l.indexable, slug).toBe(true);
      expect(l.wordCount, slug).toBeGreaterThanOrEqual(500);
      expect(l.html, slug).not.toMatch(/System Overlay|foundational building block|Ready for expansion|TODO|katex-error|Visual Anchor|Primary Element|Subject_Plan|LEARNING_PATH/i);
    }
  });

  it('every lesson has worked examples, 2+ misconceptions, 3+ practice tasks, an answer key, a safety note, sources, and nav links', () => {
    for (const [i, slug] of slugs.entries()) {
      const html = getLesson(slug)!.html;
      expect(html.match(/<h3[^>]*>Example \d/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      const misconceptions = html.split(/<h2[^>]*>Common misconceptions/)[1]?.split('<h2')[0] ?? '';
      expect(misconceptions.match(/<li>/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      const practice = html.split(/<h2[^>]*>Practice<\/h2>/)[1]?.split('<details>')[0] ?? '';
      expect(practice.match(/<li>/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(3);
      expect(html, slug).toMatch(/<summary>Answer key/);
      expect(html, slug).toMatch(/Safety note/);
      expect(html, slug).toMatch(/<h2[^>]*>Prerequisites<\/h2>/);
      expect(html, slug).toMatch(/<h2[^>]*>Sources<\/h2>/);
      expect(html, slug).toContain(`href="/subject/${hubSlug}"`);
      if (i > 0) expect(html, slug).toContain(`href="/${slugs[i - 1]}"`);
      if (i < slugs.length - 1) expect(html, slug).toContain(`href="/${slugs[i + 1]}"`);
    }
  });

  it('the Life Science K-8 hub is indexable and listed in the sitemap', async () => {
    const urls = (await sitemap()).map((s) => s.url);
    expect(subjects.find((s) => s.slug === hubSlug)!.indexable).toBe(true);
    expect(urls).toContain(`${SITE_URL}/subject/${hubSlug}`);
    for (const slug of slugs) expect(urls).toContain(`${SITE_URL}/${slug}`);
  });
});



describe('Content Site - rewrite batch: Early Literacy & Writing', () => {
  const hubSlug = 'early-literacy-and-writing';
  const batch: Array<[string, string]> = [
    ['app-011-phonemic-awareness-the-alphabet', 'APP-01.1 — Phonemic Awareness & the Alphabet'],
    ['app-012-phonics-blending-decoding', 'APP-01.2 — Phonics — Blending & Decoding'],
    ['app-013-fluency-word-recognition', 'APP-01.3 — Fluency & Word Recognition'],
    ['app-014-vocabulary-word-study', 'APP-01.4 — Vocabulary & Word Study'],
    ['app-015-reading-comprehension-narrative-text', 'APP-01.5 — Reading Comprehension — Narrative Text'],
    ['app-016-reading-comprehension-informational-text', 'APP-01.6 — Reading Comprehension — Informational Text'],
    ['app-017-writing-sentences-to-paragraphs', 'APP-01.7 — Writing — Sentences to Paragraphs'],
    ['app-018-writing-essays-research', 'APP-01.8 — Writing — Essays & Research'],
  ];
  const slugs = batch.map(([slug]) => slug);

  it('keeps slugs, titles, chapter order, subject, tier, and the prev/next chain', () => {
    const hub = subjects.find((s) => s.slug === hubSlug)!;
    expect(hub.lessons.map((l) => l.slug)).toEqual(slugs);
    batch.forEach(([slug, title], i) => {
      const l = getLesson(slug)!;
      expect(l.title).toBe(title);
      expect(l.subject).toBe('Early Literacy & Writing');
      expect(l.catalog).toBe('k12');
      expect(l.audienceTier).toBe('9-12');
      expect(l.chapter).toBe(`1.${i + 1}`);
      expect(l.prevSlug).toBe(slugs[i - 1] ?? null);
      expect(l.nextSlug).toBe(slugs[i + 1] ?? null);
    });
  });

  it('every lesson is indexable, substantial, and free of scaffold residue', () => {
    for (const slug of slugs) {
      const l = getLesson(slug)!;
      expect(l.indexable, slug).toBe(true);
      expect(l.wordCount, slug).toBeGreaterThanOrEqual(500);
      expect(l.html, slug).not.toMatch(/System Overlay|foundational building block|Ready for expansion|TODO|katex-error|Visual Anchor|Primary Element|Subject_Plan|LEARNING_PATH/i);
    }
  });

  it('every lesson has prerequisites, objectives, 2+ examples, 2+ misconceptions, 3+ practice tasks, an answer key, an adult or safety note, sources, and nav links', () => {
    for (const [i, slug] of slugs.entries()) {
      const html = getLesson(slug)!.html;
      expect(html, slug).toMatch(/<h2[^>]*>Prerequisites<\/h2>/);
      expect(html, slug).toMatch(/<h2[^>]*>Learning objectives<\/h2>/);
      expect(html.match(/<h3[^>]*>Example \d/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      const misconceptions = html.split(/<h2[^>]*>Common misconceptions/)[1]?.split('<h2')[0] ?? '';
      expect(misconceptions.match(/<li>/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      const practice = html.split(/<h2[^>]*>Practice<\/h2>/)[1]?.split('<details>')[0] ?? '';
      expect(practice.match(/<li>/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(3);
      expect(html, slug).toMatch(/<summary>Answer key/);
      expect(html, slug).toMatch(/Adult note|Safety note/);
      expect(html, slug).toMatch(/<h2[^>]*>Sources<\/h2>/);
      expect(html, slug).toContain(`href="/subject/${hubSlug}"`);
      if (i > 0) expect(html, slug).toContain(`href="/${slugs[i - 1]}"`);
      if (i < slugs.length - 1) expect(html, slug).toContain(`href="/${slugs[i + 1]}"`);
    }
  });

  it('the writing lessons include a scoring rubric', () => {
    for (const slug of ['app-017-writing-sentences-to-paragraphs', 'app-018-writing-essays-research']) {
      expect(getLesson(slug)!.html, slug).toMatch(/<strong>(Paragraph|Essay) rubric<\/strong>/);
    }
  });

  it('the Early Literacy & Writing hub is indexable and listed in the sitemap', async () => {
    const urls = (await sitemap()).map((s) => s.url);
    expect(subjects.find((s) => s.slug === hubSlug)!.indexable).toBe(true);
    expect(urls).toContain(`${SITE_URL}/subject/${hubSlug}`);
    for (const slug of slugs) expect(urls).toContain(`${SITE_URL}/${slug}`);
  });
});


describe('Content Site - rewrite batch: Research Writing & Academic Literacy', () => {
  const hubSlug = 'research-writing-and-academic-literacy';
  const batch: Array<[string, string]> = [
    ['app-121-the-writing-process', 'APP-12.1 — The Writing Process'],
    ['app-122-thesis-argument-construction', 'APP-12.2 — Thesis & Argument Construction'],
    ['app-123-evidence-analysis-integration', 'APP-12.3 — Evidence, Analysis & Integration'],
    ['app-124-research-skills-source-evaluation', 'APP-12.4 — Research Skills & Source Evaluation'],
    ['app-125-citation-documentation', 'APP-12.5 — Citation & Documentation'],
    ['app-126-essay-structures-genres', 'APP-12.6 — Essay Structures & Genres'],
    ['app-127-disciplinary-writing', 'APP-12.7 — Disciplinary Writing'],
    ['app-128-advanced-rhetoric-style', 'APP-12.8 — Advanced Rhetoric & Style'],
  ];
  const slugs = batch.map(([slug]) => slug);

  it('keeps slugs, titles, chapter order, subject, tier, and the prev/next chain', () => {
    const hub = subjects.find((s) => s.slug === hubSlug)!;
    expect(hub.lessons.map((l) => l.slug)).toEqual(slugs);
    batch.forEach(([slug, title], i) => {
      const l = getLesson(slug)!;
      expect(l.title).toBe(title);
      expect(l.subject).toBe('Research Writing & Academic Literacy');
      expect(l.catalog).toBe('k12');
      expect(l.audienceTier).toBe('9-12');
      expect(l.chapter).toBe(`12.${i + 1}`);
      expect(l.prevSlug).toBe(slugs[i - 1] ?? null);
      expect(l.nextSlug).toBe(slugs[i + 1] ?? null);
    });
  });

  it('every lesson is indexable, substantial, and free of scaffold residue', () => {
    for (const slug of slugs) {
      const l = getLesson(slug)!;
      expect(l.indexable, slug).toBe(true);
      expect(l.wordCount, slug).toBeGreaterThanOrEqual(500);
      expect(l.html, slug).not.toMatch(/System Overlay|foundational building block|Ready for expansion|TODO|katex-error|Visual Anchor|Primary Element|Subject_Plan|LEARNING_PATH/i);
    }
  });

  it('every lesson has prerequisites, objectives, 2+ examples, 2+ misconceptions, 3+ practice tasks, an answer key with a rubric, an integrity note, sources, and nav links', () => {
    for (const [i, slug] of slugs.entries()) {
      const html = getLesson(slug)!.html;
      expect(html, slug).toMatch(/<h2[^>]*>Prerequisites<\/h2>/);
      expect(html, slug).toMatch(/<h2[^>]*>Learning objectives<\/h2>/);
      expect(html.match(/<h3[^>]*>Example \d/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      const misconceptions = html.split(/<h2[^>]*>Common misconceptions/)[1]?.split('<h2')[0] ?? '';
      expect(misconceptions.match(/<li>/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(2);
      const practice = html.split(/<h2[^>]*>Practice<\/h2>/)[1]?.split('<details>')[0] ?? '';
      expect(practice.match(/<li>/g)?.length ?? 0, slug).toBeGreaterThanOrEqual(3);
      const answerKey = html.split(/<summary>Answer key/)[1]?.split('</details>')[0] ?? '';
      expect(answerKey, slug).toMatch(/<strong>[^<]*rubric[^<]*<\/strong>/i);
      expect(html, slug).toMatch(/(Academic integrity|Safety and integrity) note/);
      expect(html, slug).toMatch(/<h2[^>]*>Sources<\/h2>/);
      expect(html, slug).toContain(`href="/subject/${hubSlug}"`);
      if (i > 0) expect(html, slug).toContain(`href="/${slugs[i - 1]}"`);
      if (i < slugs.length - 1) expect(html, slug).toContain(`href="/${slugs[i + 1]}"`);
    }
  });

  it('internal lesson links in the batch resolve to indexable lessons', () => {
    for (const slug of slugs) {
      for (const [, href] of getLesson(slug)!.html.matchAll(/href="\/([^"#?]+)"/g)) {
        if (href.startsWith('subject/')) {
          expect(subjects.some((s) => `subject/${s.slug}` === href), `${slug} -> ${href}`).toBe(true);
        } else {
          expect(getLesson(href)?.indexable, `${slug} -> ${href}`).toBe(true);
        }
      }
    }
  });

  it('the Research Writing & Academic Literacy hub is indexable and listed in the sitemap', async () => {
    const urls = (await sitemap()).map((s) => s.url);
    expect(subjects.find((s) => s.slug === hubSlug)!.indexable).toBe(true);
    expect(urls).toContain(`${SITE_URL}/subject/${hubSlug}`);
    for (const slug of slugs) expect(urls).toContain(`${SITE_URL}/${slug}`);
  });
});
