import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import LessonPage, { generateMetadata } from '../app/[slug]/page';
import sitemap from '../app/sitemap';
import { lessons, subjects, getAllLessonSlugs } from '../lib/manifest';

vi.mock('next/link', () => {
  return {
    default: ({ children, href }: any) => {
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

  it('sitemap enumerates home + subjects + all lessons', async () => {
    const sm = await sitemap();
    expect(sm.length).toBe(1 + subjects.length + getAllLessonSlugs().length);

    const urls = sm.map((s) => s.url);
    expect(urls).toContain(`https://platform.example.com/${sampleLesson.slug}`);
    expect(urls).toContain(`https://platform.example.com/subject/${subjects[0].slug}`);
  });

  it('metadata is present for lessons', async () => {
    const params = Promise.resolve({ slug: sampleLesson.slug });
    const meta = await generateMetadata({ params });

    expect(meta.title).toBe(`${sampleLesson.title} - Learning Platform`);
    expect(meta.description).toContain(sampleLesson.subject);
    expect(meta.alternates?.canonical).toBe(`https://platform.example.com/${sampleLesson.slug}`);
  });
});
