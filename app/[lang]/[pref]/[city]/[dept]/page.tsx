import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { AREAS, LANGS, deptFromSlug, deptGroups, deptName, deptSlug, facilitiesFor, inGroup, indexable, type SiteLang } from "@/lib/data";
import { UI } from "@/lib/ui";
import { FacilityCard } from "@/components/FacilityCard";

type P = { lang: string; pref: string; city: string; dept: string };

export function generateStaticParams() {
  return LANGS.flatMap((lang) =>
    AREAS.flatMap((a) =>
      deptGroups()
        .filter((g) => facilitiesFor(lang, a.cityCode).some((f) => inGroup(f, g)))
        .map((g) => ({ lang, pref: a.prefSlug, city: a.citySlug, dept: deptSlug(g) })),
    ),
  );
}

function load(p: P) {
  const a = AREAS.find((x) => x.prefSlug === p.pref && x.citySlug === p.city);
  const g = deptFromSlug(p.dept);
  if (!a || !g) return null;
  const lang = p.lang as SiteLang;
  return { a, g, lang, list: facilitiesFor(lang, a.cityCode).filter((f) => inGroup(f, g)) };
}

export async function generateMetadata({ params }: { params: Promise<P> }): Promise<Metadata> {
  const d = load(await params);
  if (!d) return {};
  const name = deptName(d.g, d.lang);
  return {
    title: `English-speaking ${name} in Shinjuku City, Tokyo (${d.list.length})`,
    // ◎○が3施設に満たない組み合わせは検索に出さない（strategy §4-2）
    robots: indexable(d.list, d.lang) ? undefined : { index: false, follow: true },
  };
}

export default async function DeptPage({ params }: { params: Promise<P> }) {
  const d = load(await params);
  if (!d) notFound();
  const { a, g, lang, list } = d;
  const t = UI[lang as "en"];
  const name = deptName(g, lang);
  return (
    <div className="space-y-6">
      <nav className="text-sm text-ink/60">
        <Link href={`/${lang}/`}>Home</Link> › Tokyo › <Link href={`/${lang}/${a.prefSlug}/${a.citySlug}/`}>Shinjuku</Link> › {name}
      </nav>
      <h1 className="font-display text-3xl font-semibold">English-speaking {name} in Shinjuku City, Tokyo</h1>
      <p>
        {list.length} {t.facilities}.
      </p>
      <ul className="grid gap-3">
        {list.map((f) => (
          <FacilityCard key={f.id} f={f} lang={lang} />
        ))}
      </ul>
    </div>
  );
}
