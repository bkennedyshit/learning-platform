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
