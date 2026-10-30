import Link from "next/link";
import { deptLabel, type SiteFacility, type SiteLang } from "@/lib/data";
import { ui } from "@/lib/ui";
import { TierBadge } from "./TierBadge";
import { OpenNow } from "./OpenNow";

export function FacilityCard({ f, lang }: { f: SiteFacility; lang: SiteLang }) {
  const t = ui(lang);
  const s = f.site[lang]!;
  const groups = [...new Set(f.depts.flatMap((d) => d.groups))];
  return (
    <li className="rounded border border-line bg-white p-4">
      <div className="flex flex-wrap items-center gap-2">
        <TierBadge tier={s.tier} lang={lang} />
        <span className="text-xs text-ink/60">{t.kind[f.kind]}</span>
        <OpenNow hours={f.depts.map((d) => d.hours)} open={t.openNow} closed={t.closedNow} />
      </div>
      <h3 className="mt-2 text-lg font-bold">
        <Link href={`/${lang}/clinic/${f.id}/`}>{f.nameEn ?? f.nameJa}</Link>
      </h3>
      <p className="text-sm text-ink/70" lang="ja">
        {f.nameJa}
      </p>
      {groups.length > 0 && (
        <p className="mt-2 text-sm">{groups.map((g) => deptLabel(g, lang)).join(" · ")}</p>
      )}
      <p className="mt-1 text-sm text-ink/70">
        {s.booking === true ? t.bookingRequired : s.booking === false ? t.bookingNotRequired : null}
      </p>
    </li>
  );
}
