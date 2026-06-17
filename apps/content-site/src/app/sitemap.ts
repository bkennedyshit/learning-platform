import { MetadataRoute } from 'next';
import { getSubjects, getAllLessonSlugs } from '../lib/manifest';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://platform.example.com';

  const subjectUrls = getSubjects().map((subject) => ({
    url: `${baseUrl}/subject/${subject.slug}`,
    lastModified: new Date(),
    changeFrequency: 'weekly' as const,
    priority: 0.7,
  }));

  const lessonUrls = getAllLessonSlugs().map((slug) => ({
    url: `${baseUrl}/${slug}`,
    lastModified: new Date(),
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }));

  return [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    ...subjectUrls,
    ...lessonUrls,
  ];
}
