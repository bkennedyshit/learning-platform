import { MetadataRoute } from 'next';
import { getIndexableLessonSlugs, getIndexableSubjectSlugs } from '../lib/manifest';
import { SITE_URL } from '../lib/site';

// lastModified is only emitted where a real content date exists. Resource
// pages carry the date of their last content commit; lessons and subject hubs
// have no per-page content date (no frontmatter dates, and the whole corpus
// arrived in one bulk import commit), so lastmod is omitted rather than
// fabricated from the build time.
const RESOURCES_LAST_MODIFIED = '2026-10-01'; // f81e10c: affiliate offer + disclosure

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = SITE_URL;

  // Only hubs and lessons that pass the index-promotion gate are listed;
  // everything else is served with robots noindex,follow.
  const subjectUrls = getIndexableSubjectSlugs().map((slug) => ({
    url: `${baseUrl}/subject/${slug}`,
    changeFrequency: 'weekly' as const,
    priority: 0.7,
  }));

  const lessonUrls = getIndexableLessonSlugs().map((slug) => ({
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
      lastModified: RESOURCES_LAST_MODIFIED,
      changeFrequency: 'monthly',
      priority: 0.6,
    },
    {
      url: `${baseUrl}/resources/mobile-connectivity-for-students-and-remote-learning`,
      lastModified: RESOURCES_LAST_MODIFIED,
      changeFrequency: 'monthly',
      priority: 0.6,
    },
    ...subjectUrls,
    ...lessonUrls,
  ];
}
