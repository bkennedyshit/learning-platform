import { describe, expect, it } from 'vitest';
import { NextRequest } from 'next/server';
import { proxy } from '../proxy';
import { getLesson } from '../lib/manifest';

const LEGACY_REDIRECTS = [
  [
    '/415-past-tenses-pass%C3%A9-compos%C3%A9-imparfait-plus-que-parfait',
    '/415-past-tenses-passe-compose-imparfait-plus-que-parfait',
  ],
  [
    '/308-from-electronics-to-robotics-i%C2%B2c-spi-uart-can-sensors-actuators',
    '/308-from-electronics-to-robotics-i2c-spi-uart-can-sensors-actuators',
  ],
  [
    '/37.3---Kanji-%E2%80%94-System-Overview-&-First-100-(JLPT-N5)',
    '/373-kanji-system-overview-first-100-jlpt-n5',
  ],
] as const;

describe('legacy lesson redirects', () => {
  it.each(LEGACY_REDIRECTS)('redirects %s directly to its canonical ASCII route', (legacyPath, canonicalPath) => {
    const response = proxy(new NextRequest(`https://learning.nepa-ai.com${legacyPath}`));

    expect(response.status).toBe(308);
    expect(response.headers.get('location')).toBe(`https://learning.nepa-ai.com${canonicalPath}`);
  });

  it.each(LEGACY_REDIRECTS)('%s redirects to a published lesson', (_legacyPath, canonicalPath) => {
    expect(getLesson(canonicalPath.slice(1))).toBeDefined();
  });
});
