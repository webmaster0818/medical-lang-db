import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { AREAS, LANGS, TIER_RANK, deptName, facilitiesFor, facility, mhlwUrl, type Day, type SiteLang } from "@/lib/data";
import { LANG_NAME_EN, UI } from "@/lib/ui";
import { TierBadge } from "@/components/TierBadge";
import { OpenNow } from "@/components/OpenNow";

type P = { lang: string; id: string };
const DAYS: Day[] = ["mon", "tue", "wed", "thu", "fri", "sat", "sun", "hol"];

export function generateStaticParams() {
  return LANGS.flatMap((lang) => facilitiesFor(lang).map((f) => ({ lang, id: f.id })));
}

export async function generateMetadata({ params }: { params: Promise<P> }): Promise<Metadata> {
  const { lang, id } = await params;
  const f = facility(id);
  if (!f) return {};
  const s = f.site[lang as SiteLang]!;
  return {
    title: `${f.nameEn ?? f.nameJa} – English support, hours and phone`,
    // 「―」（要相談で翻訳機なし）の施設ページは検索に出さない（strategy §4-2）
    robots: s.tier === "D" ? { index: false, follow: true } : undefined,
  };
}

export default async function ClinicPage({ params }: { params: Promise<P> }) {
  const p = await params;
  const lang = p.lang as SiteLang;
  const f = facility(p.id);
  if (!f || !f.site[lang]) notFound();
  const t = UI[lang as "en"];
  const s = f.site[lang]!;
  const a = AREAS.find((x) => x.cityCode === f.cityCode)!;
  const grouped = f.depts.filter((d) => d.groups.length);
  const others = f.depts.filter((d) => !d.groups.length);
  const langs = Object.entries(f.spoken).sort((x, y) => TIER_RANK[x[1].tier] - TIER_RANK[y[1].tier]);
  return (
    <article className="space-y-6">
      <nav className="text-sm text-ink/60">
        <Link href={`/${lang}/`}>Home</Link> › Tokyo › <Link href={`/${lang}/${a.prefSlug}/${a.citySlug}/`}>Shinjuku</Link>
      </nav>
      <header>
        <div className="flex flex-wrap items-center gap-2">
          <TierBadge tier={s.tier} />
          <span className="text-sm text-ink/60">{t.kind[f.kind]}</span>
          <OpenNow hours={f.depts.map((d) => d.hours)} open={t.openNow} closed={t.closedNow} />
        </div>
        <h1 className="mt-2 font-display text-3xl font-semibold">{f.nameEn ?? f.nameJa}</h1>
        <p className="text-ink/70" lang="ja">
          {f.nameJa}
        </p>
      </header>

      <section className="grid gap-3 sm:grid-cols-2">
        <div className="rounded border border-line bg-white p-4">
          <h2 className="text-sm font-bold text-ink/60">{t.phoneForeign}</h2>
          {s.phoneForeign ? (
            <a href={`tel:${s.phoneForeign}`} className="text-xl font-bold">
              {s.phoneForeign}
            </a>
          ) : (
            <p className="text-ink/60">—</p>
          )}
          {f.phone && (
            <p className="mt-2 text-sm">
              {t.phone}: <a href={`tel:${f.phone}`}>{f.phone}</a>
            </p>
          )}
          <p className="mt-2 text-sm font-bold">
            {s.booking === true ? t.bookingRequired : s.booking === false ? t.bookingNotRequired : null}
          </p>
        </div>
        <div className="rounded border border-line bg-white p-4">
          <h2 className="text-sm font-bold text-ink/60">{t.address}</h2>
          {f.addressEn && <p>{f.addressEn}</p>}
          <p className="mt-2 text-sm text-ink/60">{t.showDriver}</p>
          <p className="text-lg font-bold" lang="ja">
            {f.addressJa}
          </p>
          {f.lat && f.lng && (
            <a className="mt-2 inline-block text-sm" href={`https://www.google.com/maps/search/?api=1&query=${f.lat},${f.lng}`}>
              Google Maps
            </a>
          )}
        </div>
      </section>

      <section>
        <h2 className="mb-2 text-lg font-bold">{t.languages}</h2>
        <ul className="grid gap-2">
          {langs.map(([code, l]) => (
            <li key={code} className="flex flex-wrap items-center gap-2 text-sm">
              <span className="w-40 font-bold">{LANG_NAME_EN[code] ?? code}</span>
              <TierBadge tier={l.tier} />
            </li>
          ))}
        </ul>
        {f.translationDevice && <p className="mt-2 text-sm">✓ {t.translationDevice}</p>}
      </section>

      <section>
        <h2 className="mb-2 text-lg font-bold">{t.departments}</h2>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[560px] border-collapse text-sm">
            <thead>
              <tr className="border-b border-line text-left">
                <th className="py-2 pr-2"></th>
                {DAYS.map((d) => (
                  <th key={d} className="px-1 py-2">
                    {t.day[d]}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[...grouped, ...others].map((d) => (
                <tr key={d.ja} className="border-b border-line/60 align-top">
                  <th className="py-2 pr-2 text-left font-bold">
                    {d.groups.length ? deptName(d.groups[0], lang) : null}
                    <span className="block font-normal text-ink/60" lang="ja">
                      {d.ja}
                    </span>
                  </th>
                  {DAYS.map((day) => (
                    <td key={day} className="px-1 py-2 whitespace-nowrap">
                      {(d.hours[day] ?? []).map((h) => (
                        <span key={h} className="block">
                          {h.replace("-", "–")}
                        </span>
                      ))}
                      {!d.hours[day] && <span className="text-ink/30">—</span>}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="mt-1 text-xs text-ink/60">{t.holidays}</p>
      </section>

      <section>
        <h2 className="mb-2 text-lg font-bold">{t.payments}</h2>
        <p>{f.cards.length ? f.cards.join(", ") : t.cashOnly}</p>
      </section>

      <section className="rounded border border-line bg-white/60 p-4 text-sm">
        <h2 className="mb-1 font-bold">{t.sources}</h2>
        <ul className="list-disc pl-5">
          <li>
            <a href={mhlwUrl(f.id)}>Medical Information Net (Ministry of Health, Labour and Welfare)</a>
            {f.updated && ` — ${t.lastUpdated}: ${f.updated}`}
          </li>
          {f.d5 && <li>List of medical institutions accepting foreign patients (Ministry of Health, Labour and Welfare)</li>}
          {f.url && (
            <li>
              {t.website}: <a href={f.url}>{f.url}</a>
            </li>
          )}
        </ul>
      </section>
    </article>
  );
}
