import type { Day, SiteLang, TierCode } from "./data";
import strings from "@/data/ui/strings.json";

// 画面の文言。言語は UI に文言を足したものだけが書き出される（lib/data.ts の LANGS）。
// 診療科・地名・言語名は辞書（data/dict）から引くので、ここには書かない
const EN = {
  siteName: "MediLingo Japan",
  tagline: "Hospitals and clinics in Japan with support in your language",
  tier: {
    A: { mark: "◎", label: "Accepts this language", desc: "The facility reports it can see patients in this language, or has a medical interpreter or coordinator for it." },
    B: { mark: "○", label: "Phone or video interpreter", desc: "Support in this language is through a phone or video interpreting service." },
    C: { mark: "△", label: "Translation device", desc: "The facility has a translation device and relies on it for this language." },
    D: { mark: "―", label: "Contact before visiting", desc: "The language is listed, but no interpreter or translation device is recorded. Please contact the facility before visiting." },
  } as Record<TierCode, { mark: string; label: string; desc: string }>,
  kind: { hospital: "Hospital", clinic: "Clinic", dental: "Dental clinic" },
  day: { mon: "Mon", tue: "Tue", wed: "Wed", thu: "Thu", fri: "Fri", sat: "Sat", sun: "Sun", hol: "Hol" } as Record<Day, string>,
  openNow: "Open now",
  closedNow: "Closed now",
  bookingRequired: "Appointment required",
  bookingNotRequired: "Walk-ins accepted",
  phone: "Phone",
  phoneForeign: "Phone for foreign patients",
  address: "Address",
  showDriver: "Show this to a taxi driver",
  departments: "Departments and hours",
  otherDepts: "Other departments (Japanese names)",
  payments: "Cards and e-money",
  cashOnly: "No cards or e-money reported",
  translationDevice: "Translation device available",
  languages: "Languages",
  sources: "Sources",
  lastUpdated: "Last updated by the facility",
  disclaimer:
    "Information is reported by each facility to the Ministry of Health, Labour and Welfare. Hours and language support can change. Please call before you visit.",
  emergency: "Emergency in Japan: call 119 (the ambulance is free; treatment is not)",
  byDept: "By department",
  allFacilities: "All facilities",
  count: (n: number) => `${n} facilities`,
  website: "Website",
  holidays: "Hol = national holidays",
  home: "Home",
  searchByArea: "Search by area",
  howToRead: "How to read the language support levels",
  listedFirst: "Listed from the highest support level (◎ first).",
  srcMhlwNet: "Medical Information Net (Ministry of Health, Labour and Welfare)",
  srcD5: "List of medical institutions accepting foreign patients (Ministry of Health, Labour and Welfare)",
  cityH1: (place: string) => `Hospitals and clinics with English support in ${place}`,
  cityTitle: (place: string, n: number) => `Hospitals and clinics with English support in ${place} (${n})`,
  cityDesc: (place: string, n: number) =>
    `${n} hospitals, clinics and dental clinics in ${place} that list English support, with hours, appointment rules and phone numbers.`,
  deptH1: (dept: string, place: string) => `${dept} with English support in ${place}`,
  deptTitle: (dept: string, place: string, n: number) => `${dept} with English support in ${place} (${n})`,
  clinicTitle: (name: string) => `${name} – English support, hours and phone`,
};

export type UIStrings = typeof EN;

type Raw = Record<string, string>;
const fill = (s: string, v: Record<string, string | number>) => s.replace(/\{(\w+)\}/g, (_, k) => String(v[k]));

// data/ui/strings.json（英語以外の画面の文言。出典のない訳は2台で突き合わせてから使う）から組み立てる
function build(lang: SiteLang, r: Raw): UIStrings {
  const tier = (k: TierCode) => ({ mark: EN.tier[k].mark, label: r[`tier${k}`], desc: r[`tier${k}desc`] });
  return {
    ...EN,
    tagline: r.tagline,
    tier: { A: tier("A"), B: tier("B"), C: tier("C"), D: tier("D") },
    kind: { hospital: r.hospital, clinic: r.clinic, dental: r.dental },
    day: { ...cldrWeekdays(lang), hol: r.hol },
    openNow: r.openNow,
    closedNow: r.closedNow,
    bookingRequired: r.bookingRequired,
    bookingNotRequired: r.bookingNotRequired,
    phone: r.phone,
    phoneForeign: r.phoneForeign,
    address: r.address,
    showDriver: r.showDriver,
    departments: r.departments,
    otherDepts: r.otherDepts,
    payments: r.payments,
    cashOnly: r.cashOnly,
    translationDevice: r.translationDevice,
    languages: r.languages,
    sources: r.sources,
    lastUpdated: r.lastUpdated,
    disclaimer: r.disclaimer,
    emergency: r.emergency,
    byDept: r.byDept,
    allFacilities: r.allFacilities,
    count: (n) => fill(r.count, { n }),
    website: r.website,
    holidays: r.holidays,
    home: r.home,
    searchByArea: r.searchByArea,
    howToRead: r.howToRead,
    listedFirst: r.listedFirst,
    srcMhlwNet: r.srcMhlwNet,
    srcD5: r.srcD5,
    cityH1: (place) => fill(r.cityH1, { place }),
    cityTitle: (place, n) => fill(r.cityTitle, { place, n }),
    cityDesc: (place, n) => fill(r.cityDesc, { place, n }),
    deptH1: (dept, place) => fill(r.deptH1, { dept, place }),
    deptTitle: (dept, place, n) => fill(r.deptTitle, { dept, place, n }),
    clinicTitle: (name) => fill(r.clinicTitle, { name }),
  };
}


export function ui(lang: SiteLang): UIStrings {
  const t = UI[lang];
  if (!t) throw new Error(`UI strings missing for ${lang}`);
  return t;
}

/** サイトの言語コード → BCP 47（Intl に渡す）。pt は在日ブラジル人向けなので pt-BR */
export const BCP47: Record<SiteLang, string> = {
  en: "en",
  ko: "ko",
  "zh-hant": "zh-Hant",
  "zh-hans": "zh-Hans",
  vi: "vi",
  pt: "pt-BR",
};

/** 月〜日の短い表記を Unicode CLDR（Intl）から取る。祝日は CLDR に無いので UI 側で持つ */
export function cldrWeekdays(lang: SiteLang): Record<Exclude<Day, "hol">, string> {
  const f = new Intl.DateTimeFormat(BCP47[lang], { weekday: "short", timeZone: "UTC" });
  const keys = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"] as const;
  // 2026-01-05 は月曜
  return Object.fromEntries(keys.map((k, i) => [k, f.format(new Date(Date.UTC(2026, 0, 5 + i)))])) as Record<
    Exclude<Day, "hol">,
    string
  >;
}

export const LANG_NAME_EN: Record<string, string> = {
  en: "English", ko: "Korean", zh: "Chinese (Mandarin)", "zh-tw": "Taiwanese", yue: "Cantonese", vi: "Vietnamese", pt: "Portuguese",
  es: "Spanish", fr: "French", de: "German", ru: "Russian", th: "Thai", my: "Burmese", tl: "Tagalog", id: "Indonesian",
  ne: "Nepali", it: "Italian", ar: "Arabic", hi: "Hindi", mn: "Mongolian", ms: "Malay", si: "Sinhala", bn: "Bengali",
  ur: "Urdu", fa: "Persian", tr: "Turkish", km: "Khmer", lo: "Lao", uk: "Ukrainian", pl: "Polish", nl: "Dutch",
};

// 医療情報ネットの言語コード → CLDR のコード（台湾語＝閩南語）
const CLDR_CODE: Record<string, string> = { "zh-tw": "nan", tl: "fil" };

/** 施設が対応する言語の名前。英語は従来の表記、他言語は Unicode CLDR の言語名 */
export function langName(code: string, lang: SiteLang): string {
  if (lang === "en") return LANG_NAME_EN[code] ?? code;
  return new Intl.DisplayNames([BCP47[lang]], { type: "language", fallback: "code" }).of(CLDR_CODE[code] ?? code) ?? code;
}

// BCP47 を使うので末尾で組み立てる
const RAW = strings as Record<string, Raw>;
export const UI: Partial<Record<SiteLang, UIStrings>> = {
  en: EN,
  ...Object.fromEntries((Object.keys(RAW) as SiteLang[]).map((l) => [l, build(l, RAW[l])])),
};

/** 本番に書き出す言語。訳の突き合わせが済んだら足す（PREVIEW_ALL_LANGS=1 で全言語を書き出して確認できる） */
export const READY: SiteLang[] = ["en", "ko", "zh-hant", "zh-hans", "vi", "pt"];

/** 言語切り替えに出す自称（Unicode CLDR） */
export function autonym(lang: SiteLang): string {
  return new Intl.DisplayNames([BCP47[lang]], { type: "language" }).of(BCP47[lang]) ?? lang;
}
