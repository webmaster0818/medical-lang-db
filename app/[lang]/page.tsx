import Link from "next/link";
import { areasByPref, facilitiesFor, placeName, prefName, type SiteLang } from "@/lib/data";
import { ui } from "@/lib/ui";
import { TierLegend } from "@/components/TierBadge";

export default async function Home({ params }: { params: Promise<{ lang: string }> }) {
  const { lang } = (await params) as { lang: SiteLang };
  const t = ui(lang);
  const groups = areasByPref();
  return (
    <div className="space-y-8">
      <section>
        <h1 className="font-display text-3xl font-semibold leading-tight sm:text-4xl">{t.tagline}</h1>
        <p className="mt-3 rounded border-l-4 border-accent bg-white px-4 py-3 font-bold">{t.emergency}</p>
      </section>
      <section>
        <h2 className="mb-3 text-xl font-bold">{t.searchByArea}</h2>
        <nav className="mb-6 flex flex-wrap gap-x-3 gap-y-1 text-sm">
          {groups.map((g) => (
            <a key={g[0].prefCode} href={`#${g[0].prefSlug}`}>
              {prefName(g[0], lang)}
            </a>
          ))}
        </nav>
        <div className="space-y-6">
          {groups.map((g) => (
            <section key={g[0].prefCode} id={g[0].prefSlug}>
              <h3 className="mb-2 text-lg font-bold">{prefName(g[0], lang)}</h3>
              <ul className="grid gap-2 sm:grid-cols-2">
                {g.map((a) => (
                  <li key={a.cityCode}>
                    <Link
                      href={`/${lang}/${a.prefSlug}/${a.citySlug}/`}
                      className="block rounded border border-line bg-white p-4 no-underline hover:border-ink"
                    >
                      <span className="font-bold">{placeName(a, lang)}</span>
                      <span className="block text-sm text-ink/70">
                        {t.count(facilitiesFor(lang, a.cityCode).length)}
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            </section>
          ))}
        </div>
      </section>
      <section>
        <h2 className="mb-3 text-xl font-bold">{t.howToRead}</h2>
        <TierLegend lang={lang} />
      </section>
    </div>
  );
}
