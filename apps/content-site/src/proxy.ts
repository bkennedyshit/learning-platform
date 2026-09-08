import { NextResponse, type NextRequest } from "next/server";

const LEGACY_LESSON_PATHS = new Map([
  [
    "/415-past-tenses-passé-composé-imparfait-plus-que-parfait",
    "/415-past-tenses-passe-compose-imparfait-plus-que-parfait",
  ],
  [
    "/308-from-electronics-to-robotics-i²c-spi-uart-can-sensors-actuators",
    "/308-from-electronics-to-robotics-i2c-spi-uart-can-sensors-actuators",
  ],
  [
    "/225-serial-verbs-把-被-resultative-complements",
    "/225-serial-verbs-resultative-complements",
  ],
  [
    "/37.3---Kanji-—-System-Overview-&-First-100-(JLPT-N5)",
    "/373-kanji-system-overview-first-100-jlpt-n5",
  ],
]);

export function proxy(request: NextRequest) {
  let pathname = request.nextUrl.pathname;
  try {
    pathname = decodeURIComponent(pathname);
  } catch {
    return NextResponse.next();
  }

  const destination = LEGACY_LESSON_PATHS.get(pathname);
  if (!destination) return NextResponse.next();

  return NextResponse.redirect(new URL(destination, request.url), 308);
}

export const config = {
  matcher: "/((?!api|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt|lesson-assets).*)",
};
