import Link from "next/link";
import { getSubjects } from "../lib/manifest";

const CATALOG_LABELS: Record<string, string> = {
  advanced: "Advanced / Higher-Ed",
  k12: "K-12",
};

const DONATION_URL = "https://www.paypal.com/ncp/payment/CBYSHV6MWPPCY";

const SUBJECT_IMAGES = {
  code: "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=900&q=80",
  science: "https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&w=900&q=80",
  math: "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=900&q=80",
  engineering: "https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&w=900&q=80",
  humanities: "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=900&q=80",
  arts: "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=900&q=80",
  language: "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=900&q=80",
  business: "https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=900&q=80",
  space: "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?auto=format&fit=crop&w=900&q=80",
  default: "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=900&q=80",
};

const HERO_IMAGES = [
  {
    label: "Interactive math",
    image: SUBJECT_IMAGES.math,
  },
  {
    label: "Lab science",
    image: SUBJECT_IMAGES.science,
  },
  {
    label: "Software systems",
    image: SUBJECT_IMAGES.code,
  },
  {
    label: "Humanities",
    image: SUBJECT_IMAGES.humanities,
  },
];

function getSubjectImage(name: string, slug: string) {
  const value = `${name} ${slug}`.toLowerCase();
  if (/(python|javascript|typescript|rust|sql|cloud|cyber|database|devops|compiler|app|system|network|ai|machine)/.test(value)) return SUBJECT_IMAGES.code;
  if (/(biology|chemistry|anatomy|neuroscience|psychology|earth|life|physical|thermo|quantum|relativity|electro)/.test(value)) return SUBJECT_IMAGES.science;
  if (/(algebra|calculus|geometry|statistics|probability|differential|linear|mathematical|discrete)/.test(value)) return SUBJECT_IMAGES.math;
  if (/(engineering|robotics|mechanics|aerospace|fabrication|electronics|hci|vr|3d|control|signal|fluid|solid)/.test(value)) return SUBJECT_IMAGES.engineering;
  if (/(history|civics|government|economics|sociology|ethics|philosophy|english|writing|geography)/.test(value)) return SUBJECT_IMAGES.humanities;
  if (/(art|music|game|sound|design)/.test(value)) return SUBJECT_IMAGES.arts;
  if (/(spanish|french|italian|japanese|latin|mandarin|language|literacy)/.test(value)) return SUBJECT_IMAGES.language;
  if (/(finance|business|entrepreneurship|investing)/.test(value)) return SUBJECT_IMAGES.business;
  if (/(orbital|space|holographics)/.test(value)) return SUBJECT_IMAGES.space;
  return SUBJECT_IMAGES.default;
}

export default async function Home() {
  const subjects = getSubjects();
  const totalLessons = subjects.reduce((sum, s) => sum + s.lessonCount, 0);
  const advanced = subjects.filter((s) => s.catalog === "advanced");
  const k12 = subjects.filter((s) => s.catalog === "k12");

  const Card = ({ s }: { s: (typeof subjects)[number] }) => (
    <Link href={`/subject/${s.slug}`} className="subject-card">
      <span
        className="subject-card__image"
        style={{ backgroundImage: `url(${getSubjectImage(s.name, s.slug)})` }}
        aria-hidden
      />
      <div className="subject-card__top">
        <span className="badge">{CATALOG_LABELS[s.catalog] ?? s.catalog}</span>
        <span className="subject-card__count">{s.lessonCount}</span>
      </div>
      <h3 className="subject-card__title">{s.name}</h3>
      <span className="subject-card__cta">Start learning →</span>
    </Link>
  );

  return (
    <main>
      <header className="site-nav">
        <Link href="/" className="site-nav__brand">
          <span className="site-nav__logo" aria-hidden>LP</span>
          <span>Learning Platform</span>
        </Link>
        <nav className="site-nav__links" aria-label="Primary">
          <a href="#advanced">Advanced</a>
          <a href="#k12">K-12</a>
          <a href="#support" className="site-nav__donate">Donate</a>
        </nav>
      </header>

      {/* Hero */}
      <section className="hero">
        <div className="container hero__inner">
          <div className="hero__copy">
            <span className="hero__eyebrow">Open learning library</span>
            <h1 className="hero__title">
              Serious lessons with the energy of a great classroom.
            </h1>
            <p className="hero__sub">
              {subjects.length} subjects and {totalLessons.toLocaleString()} lessons across math, science,
              engineering, languages, code, and the humanities, built for focused study instead of filler.
            </p>
            <div className="hero__actions">
              <a href="#catalog" className="btn">Browse the catalog</a>
              <a href="#support" className="btn btn-outline">Fund the library</a>
            </div>
          </div>
          <div className="hero__media" aria-label="Learning categories">
            {HERO_IMAGES.map((item) => (
              <div
                className="hero-tile"
                key={item.label}
                style={{ backgroundImage: `url(${item.image})` }}
              >
                <span>{item.label}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="stats-strip" aria-label="Catalog summary">
        <div className="container stats-strip__inner">
          <div><strong>{subjects.length}</strong><span>subjects</span></div>
          <div><strong>{totalLessons.toLocaleString()}</strong><span>lessons</span></div>
          <div><strong>{advanced.length}</strong><span>advanced tracks</span></div>
          <div><strong>{k12.length}</strong><span>K-12 paths</span></div>
        </div>
      </section>

      {/* Catalog */}
      <section id="catalog" className="container section">
        <div className="section__head" id="advanced">
          <h2>Advanced &amp; Higher Education</h2>
          <p>{advanced.length} subjects</p>
        </div>
        <div className="subject-grid">
          {advanced.map((s) => <Card key={`${s.catalog}-${s.slug}-${s.name}`} s={s} />)}
        </div>

        <div className="section__head" id="k12" style={{ marginTop: "3.5rem" }}>
          <h2>K-12</h2>
          <p>{k12.length} subjects</p>
        </div>
        <div className="subject-grid">
          {k12.map((s) => <Card key={`${s.catalog}-${s.slug}-${s.name}`} s={s} />)}
        </div>
      </section>

      <section id="support" className="support-section">
        <div className="container support-section__inner">
          <div>
            <span className="hero__eyebrow">Keep it open</span>
            <h2>Tip the library. Sponsor the next batch of lessons.</h2>
            <p>
              A cleaner donation surface makes the site feel alive and gives supporters a clear place to help
              pay for content generation, review, hosting, and better learning tools.
            </p>
          </div>
          <div className="tip-card" aria-label="Donation options">
            <div className="tip-card__top">
              <span>Tip jar</span>
              <strong>Open access fund</strong>
            </div>
            <div className="tip-card__amounts">
              <a href={DONATION_URL}>$5</a>
              <a href={DONATION_URL}>$15</a>
              <a href={DONATION_URL}>$50</a>
            </div>
            <a className="tip-card__button" href={DONATION_URL}>
              Donate or sponsor
            </a>
          </div>
        </div>
      </section>
    </main>
  );
}
