import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { AREAS, LANGS, deptGroups, deptLabel, deptSlug, facilitiesFor, inGroup, placeName, type SiteLang } from "@/lib/data";
import { ui } from "@/lib/ui";
import { robots } from "@/lib/robots";
import { FacilityCard } from "@/components/FacilityCard";

type P = { lang: string; pref: string; city: string };

export function generateStaticParams() {
  return LANGS.flatMap((lang) => AREAS.map((a) => ({ lang, pref: a.prefSlug, city: a.citySlug })));
}

function area(p: P) {
  return AREAS.find((a) => a.prefSlug === p.pref && a.citySlug === p.city);
}

export async function generateMetadata({ params }: { params: Promise<P> }): Promise<Metadata> {
  const p = await params;
  const a = area(p);
  if (!a) return {};
  const lang = p.lang as SiteLang;
  const t = ui(lang);
  const place = placeName(a, lang);
  const n = facilitiesFor(lang, a.cityCode).length;
  return { title: t.cityTitle(place, n), description: t.cityDesc(place, n), robots: robots() };
}

export default async function CityPage({ params }: { params: Promise<P> }) {
  const p = await params;
  const lang = p.lang as SiteLang;
  const a = area(p);
  if (!a) notFound();
  const t = ui(lang);
  const place = placeName(a, lang);
  const list = facilitiesFor(lang, a.cityCode);
  const depts = deptGroups()
    .map((g) => ({ g, n: list.filter((f) => inGroup(f, g)).length }))
    .filter((d) => d.n > 0)
    .sort((x, y) => y.n - x.n);
  return (
    <div className="space-y-6">
      <nav className="text-sm text-ink/60">
        <Link href={`/${lang}/`}>{t.home}</Link> › {place}
      </nav>
      <h1 className="font-display text-3xl font-semibold">{t.cityH1(place)}</h1>
      <p>
        <span className="font-bold">{t.count(list.length)}</span>
        <span className="block text-sm text-ink/70">{t.listedFirst}</span>
      </p>
      <section>
        <h2 className="mb-2 text-lg font-bold">{t.byDept}</h2>
        <ul className="flex flex-wrap gap-2">
          {depts.map(({ g, n }) => (
            <li key={g}>
              <Link
                href={`/${lang}/${a.prefSlug}/${a.citySlug}/${deptSlug(g)}/`}
                className="inline-block rounded-full border border-line bg-white px-3 py-1 text-sm no-underline hover:border-ink"
              >
                {deptLabel(g, lang)} <span className="text-ink/50">{n}</span>
              </Link>
            </li>
          ))}
        </ul>
      </section>
      <section>
        <h2 className="mb-2 text-lg font-bold">{t.allFacilities}</h2>
        <ul className="grid gap-3">
          {list.map((f) => (
            <FacilityCard key={f.id} f={f} lang={lang} />
          ))}
        </ul>
      </section>
    </div>
  );
}
