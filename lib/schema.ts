// 外国語が通じる医療機関DB のデータ型（strategy-phase5-20261030.md §5）
// 値はすべて公的データ由来。推測で埋めない（不明は null）。

export type Lang = "en" | "ko" | "zh-hant" | "zh-hans" | "vi" | "pt";

/** 言語ごとの対応の確かさ（一覧は ◎ から並べる） */
export type Tier = "A" | "B" | "C" | "D"; // A=◎ 受入可能×通訳/スタッフ, B=○ 電話通訳, C=△ 翻訳機, D=― 記載のみ

export interface Hours {
  day: "mon" | "tue" | "wed" | "thu" | "fri" | "sat" | "sun" | "hol";
  open: string; // "09:00"
  close: string; // "12:30"
}

export interface Facility {
  id: string; // 当サイトの施設ID
  mhlwId: string | null; // 医療情報ネットの施設ID
  d5Id: string | null; // 厚労省「外国人患者を受け入れる医療機関」リストの行
  kind: "hospital" | "clinic" | "dental" | "midwife";
  nameJa: string;
  nameKana: string | null;
  nameRomaji: string | null;
  nameLocal: Partial<Record<Lang, string>>; // 公式の外国語名がある場合のみ
  prefCode: string; // 2桁
  cityCode: string; // 全国地方公共団体コード（6桁）
  addressJa: string;
  lat: number | null;
  lng: number | null;
  depts: string[]; // 診療科コード（dict の kind=dept）
  hours: Hours[];
  emergencyLevel: "none" | "primary" | "secondary" | "tertiary" | null;
  onlineConsult: boolean | null;
  payments: string[]; // dict の kind=payment
  phone: string | null;
  sourceMhlwDate: string | null; // データの時点（YYYY-MM-DD）
  sourceD5Date: string | null;
  updatedAt: string;
  changedFields: string[]; // 前回取得からの差分
}

export interface FacilityLanguage {
  facilityId: string;
  lang: Lang;
  status: "accepted" | "consult" | null; // 受入可能 / 要相談
  method: "staff" | "interpreter" | "phone_interp" | "device" | "unspecified";
  tier: Tier; // status と method から機械的に決める
  hours: Hours[];
  phoneForeign: string | null;
  bookingRequired: boolean | null;
  source: "mhlw" | "d5" | "both";
}

/** 定型の値の訳。出典URLの無い訳は使わない */
export interface DictEntry {
  kind: "dept" | "weekday" | "emergency" | "payment" | "status" | "method" | "booking" | "pref" | "city";
  valueJa: string;
  lang: Lang;
  text: string;
  sourceUrl: string;
}

/** ページを作るか・検索に出すか（§4-2 の基準） */
export interface PageRule {
  lang: Lang;
  prefCode: string;
  cityCode: string | null;
  dept: string | null;
  countByTier: Record<Tier, number>;
  indexable: boolean; // 目安：◎○ が3件以上
}
