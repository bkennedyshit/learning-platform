# Content Site Image Hosting Notes

Updated 2026-06-21.

## Current state

The content-site homepage currently uses remote Unsplash URLs for the visual refresh. No homepage `.jpg`, `.png`, `.webp`, or `.avif` assets were committed for that work.

The URLs live in:
- `apps/content-site/src/app/page.tsx`
  - `SUBJECT_IMAGES`
  - `HERO_IMAGES`
- `apps/content-site/src/app/globals.css`
  - `.hero` background image
  - `.tip-card__top` background image

This is acceptable short term, but it means the homepage depends on Unsplash availability, their CDN behavior, and their terms around remote image delivery.

## Intended direction

Move production homepage/category imagery to Cloudflare-hosted assets before meaningful traffic.

Preferred setup:
- Store canonical assets in Cloudflare R2 or Cloudflare Images.
- Serve through a stable asset domain, for example `https://assets.example.com/learning/...`.
- Use optimized formats such as `.webp` or `.avif`, with sensible fallback only if needed.
- Keep source/original files outside Git unless they are small, intentional, and needed for reproducible builds.

Example final URLs:

```txt
https://assets.example.com/learning/home/hero-classroom.webp
https://assets.example.com/learning/home/math.webp
https://assets.example.com/learning/home/science.webp
https://assets.example.com/learning/home/code.webp
https://assets.example.com/learning/home/humanities.webp
```

## Code cleanup to do when migrating

When replacing Unsplash:
- Move the homepage image map out of `page.tsx` into a small config module, likely `apps/content-site/src/lib/homeImages.ts`.
- Replace CSS background URLs in `globals.css` with CSS variables or class-specific values fed from the same config if practical.
- Keep image naming semantic by use case, not by random source filename.
- Verify desktop and mobile after replacing URLs because crop/framing will change.

## Git hygiene

Local image staging folders are ignored:
- `_image-staging/`
- `image-staging/`
- `apps/*/public/_image-staging/`

Use those for temporary downloads, exports, compression tests, and Cloudflare upload prep. Do not commit raw batches or throwaway exports.

If an image should be permanently tracked in Git, put it in a deliberate production path and commit it intentionally.
