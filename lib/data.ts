import facilitiesShinjuku from "@/data/site/facilities-13104.json";
import departments from "@/data/site/departments.json";
import dictionary from "@/data/dict/dictionary.json";
import { UI } from "./ui";

export type SiteLang = "en" | "ko" | "zh-hant" | "zh-hans" | "vi" | "pt";
export type TierCode = "A" | "B" | "C" | "D";
export type Day = "mon" | "tue" | "wed" | "thu" | "fri" | "sat" | "sun" | "hol";

export interface LangSupport {
  tier: TierCode;
  status: "accepted" | "consult" | null;
  booking: boolean | null;
  phoneForeign: string | null;
  days: Day[];
  depts: string[] | null;
  source: "mhlw" | "d5" | "both";
  basis: string[];
  spoken?: string;
}

export interface SiteFacility {
  id: string;
  kind: "hospital" | "clinic" | "dental";
  nameJa: string;
  nameEn: string | null;
  addressJa: string;
  addressEn: string | null;
  postal: string | null;
  prefCode: string;
  cityCode: string;
  phone: string | null;
  url: string | null;
  lat: number | null;
  lng: number | null;
  updated: string | null;
  translationDevice: boolean;
  cards: string[];
  emergencyJa: string[];
  jmip: boolean;
  d5: { h24: boolean | null; category: string | null; cards: string[] | null } | null;
  depts: { ja: string; groups: string[]; hours: Partial<Record<Day, string[]>> }[];
  spoken: Record<string, LangSupport>;
  site: Partial<Record<SiteLang, LangSupport>>;
}

export const ALL_LANGS: SiteLang[] = ["en", "ko", "zh-hant", "zh-hans", "vi", "pt"];
// 画面の文言（lib/ui.ts）がそろった言語だけを書き出す
export const LANGS: SiteLang[] = ALL_LANGS.filter((l) => UI[l]);
export const TIER_RANK: Record<TierCode, number> = { A: 0, B: 1, C: 2, D: 3 };

export interface Area {
  prefCode: string;
  prefSlug: string;
  cityCode: string;
  citySlug: string;
  prefJa: string;
  cityJa: string;
}
export const AREAS: Area[] = [{ prefCode: "13", prefSlug: "tokyo", cityCode: "13104", citySlug: "shinjuku", prefJa: "東京都", cityJa: "新宿区" }];

const ALL = facilitiesShinjuku as unknown as SiteFacility[];

export function facilitiesFor(lang: SiteLang, cityCode?: string): SiteFacility[] {
  return ALL.filter((f) => f.site[lang] && (!cityCode || f.cityCode === cityCode)).sort(
    (a, b) =>
      TIER_RANK[a.site[lang]!.tier] - TIER_RANK[b.site[lang]!.tier] ||
      ["hospital", "clinic", "dental"].indexOf(a.kind) - ["hospital", "clinic", "dental"].indexOf(b.kind) ||
      (a.nameEn ?? a.nameJa).localeCompare(b.nameEn ?? b.nameJa),
  );
}

export function facility(id: string): SiteFacility | undefined {
  return ALL.find((f) => f.id === id);
}

type DeptDict = Record<string, Partial<Record<SiteLang, { text: string; src: string }>>>;
const DEPTS = departments as DeptDict;

// 辞書の訳は出典の表記のまま持ち、表示のときだけ頭文字をそろえる
function titleCase(s: string) {
  return s.replace(/\b[a-z]/g, (c) => c.toUpperCase());
}

export function deptName(ja: string, lang: SiteLang): string | null {
  const t = DEPTS[ja]?.[lang]?.text;
  return t ? (lang === "en" ? titleCase(t) : t) : null;
}

/** 辞書に訳が無い診療科は日本語のまま出す（出典のない訳はしない） */
export function deptLabel(ja: string, lang: SiteLang): string {
  return deptName(ja, lang) ?? ja;
}

type DictRow = { kind: string; value_ja: string; lang: string; text: string; status: string };
const DICT = dictionary as DictRow[];

/** 地名（「東京都新宿区」の表記）。辞書で「実測」の訳だけを使い、無ければ日本語 */
export function placeName(a: Area, lang: SiteLang): string {
  const r = DICT.find((x) => (x.kind === "ward" || x.kind === "city") && x.value_ja === a.cityJa && x.lang === lang && x.status === "実測" && x.text);
  return r?.text ?? `${a.prefJa}${a.cityJa}`;
}

export function deptSlug(ja: string): string {
  return (DEPTS[ja]?.en?.text ?? ja).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

export function deptGroups(): string[] {
  return Object.keys(DEPTS).filter((ja) => DEPTS[ja].en);
}

export function deptFromSlug(slug: string): string | undefined {
  return deptGroups().find((ja) => deptSlug(ja) === slug);
}

export function inGroup(f: SiteFacility, groupJa: string): boolean {
  return f.depts.some((d) => d.groups.includes(groupJa));
}

/** 検索に出す基準（strategy §4-2）：◎○が3施設以上 */
export function indexable(list: SiteFacility[], lang: SiteLang): boolean {
  return list.filter((f) => TIER_RANK[f.site[lang]!.tier] <= 1).length >= 3;
}

/** ID（13桁）＝都道府県2桁＋区分1桁＋kikanCd 10桁 */
export function mhlwUrl(id: string): string {
  return `https://www.iryou.teikyouseido.mhlw.go.jp/znk-web/juminkanja/S2430/initialize?kikanCd=${id.slice(3)}&kikanKbn=${id[2]}&prefCd=${id.slice(0, 2)}`;
}
