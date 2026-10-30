import Link from "next/link";
import { AREAS, facilitiesFor, type SiteLang } from "@/lib/data";
import { UI } from "@/lib/ui";
import { TierLegend } from "@/components/TierBadge";

export default async function Home({ params }: { params: Promise<{ lang: string }> }) {
  const { lang } = (await params) as { lang: SiteLang };
  const t = UI[lang as "en"];
  return (
    <div className="space-y-8">
      <section>
        <h1 className="font-display text-3xl font-semibold leading-tight sm:text-4xl">{t.tagline}</h1>
        <p className="mt-3 rounded border-l-4 border-accent bg-white px-4 py-3 font-bold">{t.emergency}</p>
      </section>
      <section>
        <h2 className="mb-3 text-xl font-bold">Search by area</h2>
        <ul className="grid gap-2 sm:grid-cols-2">
          {AREAS.map((a) => (
            <li key={a.cityCode}>
              <Link
                href={`/${lang}/${a.prefSlug}/${a.citySlug}/`}
                className="block rounded border border-line bg-white p-4 no-underline hover:border-ink"
              >
                <span className="font-bold">Shinjuku City, Tokyo</span>
                <span className="block text-sm text-ink/70">
                  {facilitiesFor(lang, a.cityCode).length} {t.facilities}
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </section>
      <section>
        <h2 className="mb-3 text-xl font-bold">How to read the language support levels</h2>
        <TierLegend />
      </section>
    </div>
  );
}
