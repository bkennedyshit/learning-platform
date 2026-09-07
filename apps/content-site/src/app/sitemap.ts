import { MetadataRoute } from 'next';
import { getSubjects, getAllLessonSlugs } from '../lib/manifest';
import { SITE_URL } from '../lib/site';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = SITE_URL;

  const subjectUrls = getSubjects().map((subject) => ({
    url: `${baseUrl}/subject/${subject.slug}`,
    changeFrequency: 'weekly' as const,
    priority: 0.7,
  }));

  const lessonUrls = getAllLessonSlugs().map((slug) => ({
    url: `${baseUrl}/${slug}`,
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }));

  return [
    {
      url: baseUrl,
      changeFrequency: 'daily',
      priority: 1,
    },
    {
      url: `${baseUrl}/resources`,
      lastModified: '2026-09-07',
      changeFrequency: 'monthly',
      priority: 0.6,
    },
    {
      url: `${baseUrl}/resources/mobile-connectivity-for-students-and-remote-learning`,
      lastModified: '2026-09-07',
      changeFrequency: 'monthly',
      priority: 0.6,
    },
    ...subjectUrls,
    ...lessonUrls,
  ];
}
