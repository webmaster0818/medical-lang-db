import type { Day, SiteLang, TierCode } from "./data";

// 画面の文言（英語版）。他言語の文言は出典つきの訳がそろってから足す
export const UI = {
  en: {
    siteName: "Clinic Finder Japan",
    tagline: "Hospitals and clinics in Japan that accept patients in your language",
    tier: {
      A: { mark: "◎", label: "Staff or interpreter", desc: "The facility reports it can see patients in this language." },
      B: { mark: "○", label: "Phone or video interpreter", desc: "Support is through a remote interpreting service." },
      C: { mark: "△", label: "Translation device", desc: "Support relies on a translation device, or the facility asks you to consult first." },
      D: { mark: "―", label: "Ask before visiting", desc: "The language is listed, but the facility asks you to consult first and has no translation device." },
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
    emergency: "Emergency: call 119 (ambulance, free of charge)",
    byDept: "By department",
    allFacilities: "All facilities",
    facilities: "facilities",
    website: "Website",
    holidays: "Hol = national holidays",
  },
} satisfies Partial<Record<SiteLang, unknown>>;

export const LANG_NAME_EN: Record<string, string> = {
  en: "English", ko: "Korean", zh: "Chinese (Mandarin)", "zh-tw": "Taiwanese", yue: "Cantonese", vi: "Vietnamese", pt: "Portuguese",
  es: "Spanish", fr: "French", de: "German", ru: "Russian", th: "Thai", my: "Burmese", tl: "Tagalog", id: "Indonesian",
  ne: "Nepali", it: "Italian", ar: "Arabic", hi: "Hindi", mn: "Mongolian", ms: "Malay", si: "Sinhala", bn: "Bengali",
  ur: "Urdu", fa: "Persian", tr: "Turkish", km: "Khmer", lo: "Lao", uk: "Ukrainian", pl: "Polish", nl: "Dutch",
};
