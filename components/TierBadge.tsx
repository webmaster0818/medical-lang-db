import type { SiteLang, TierCode } from "@/lib/data";
import { ui } from "@/lib/ui";

const COLOR: Record<TierCode, string> = {
  A: "bg-tier-a",
  B: "bg-tier-b",
  C: "bg-tier-c",
  D: "bg-tier-d",
};

export function TierBadge({ tier, lang }: { tier: TierCode; lang: SiteLang }) {
  const t = ui(lang).tier[tier];
  return (
    <span className={`inline-flex items-center gap-1 rounded px-2 py-0.5 text-xs font-bold text-white ${COLOR[tier]}`}>
      <span aria-hidden>{t.mark}</span>
      {t.label}
    </span>
  );
}

export function TierLegend({ lang }: { lang: SiteLang }) {
  const tiers: TierCode[] = ["A", "B", "C", "D"];
  return (
    <dl className="grid gap-2 text-sm sm:grid-cols-2">
      {tiers.map((k) => (
        <div key={k} className="flex flex-col gap-1 rounded border border-line bg-white/60 p-3">
          <dt>
            <TierBadge tier={k} lang={lang} />
          </dt>
          <dd className="text-ink/80">{ui(lang).tier[k].desc}</dd>
        </div>
      ))}
    </dl>
  );
}
