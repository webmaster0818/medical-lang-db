#!/usr/bin/env python3
"""ingest/ の取得結果と data/dict/ の辞書から、ページ生成用の data/site/*.json を作る。

- 外国語の欄がある施設だけを出す（外国語なしの施設はサイトに載せない）
- 診療科は辞書にある19科（親の科）にまとめる。辞書にない科名は日本語のまま「その他」に入れ、訳さない
- 支払方法はブランドの商標名に直す
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ING = ROOT / "ingest" / "data" / "out"
OUT = ROOT / "data" / "site"

SITE_LANGS = {
    "en": ["en"],
    "ko": ["ko"],
    "zh-hans": ["zh"],
    "zh-hant": ["zh", "zh-tw", "yue"],
    "vi": ["vi"],
    "pt": ["pt"],
}
TIER_ORDER = {"◎": 0, "○": 1, "△": 2, "―": 3}
TIER_CODE = {"◎": "A", "○": "B", "△": "C", "―": "D"}
DAYS = [("月", "mon"), ("火", "tue"), ("水", "wed"), ("木", "thu"), ("金", "fri"), ("土", "sat"), ("日", "sun"), ("祝", "hol")]
KIND = {"hospital": "hospital", "clinic": "clinic", "dental": "dental"}

# 親の科へのまとめ（訳ではなく分類。表示は親の科の訳＋元の日本語の科名）
EXACT = {
    "耳鼻いんこう科": "耳鼻咽喉科",
    "脳神経内科": "神経内科",
    "胃腸内科": "消化器内科",
    "内視鏡内科": "消化器内科",
    "肝臓内科": "消化器内科",
    "美容皮膚科": "皮膚科",
    "小児外科": "外科",
}
# 親の科の下位・旧称にあたる科（taro-2 の分類案 2026-11-01。訳ではなく分類）
SUB = {
    "アレルギー科": ["内科"],
    "リウマチ科": ["内科"],
    "睡眠時無呼吸外来": ["内科"],
    "男性泌尿器科": ["泌尿器科"],
    "腎臓・泌尿器科": ["泌尿器科", "内科"],
    "乳腺科": ["外科"],
    "内分泌外科（甲状腺外科）": ["外科"],
    "児童精神科": ["精神科"],
    "老年精神科": ["精神科"],
    "神経科": ["精神科"],
    "小児眼科": ["眼科", "小児科"],
    "小児皮膚科": ["皮膚科", "小児科"],
    "気管食道・耳鼻いんこう科": ["耳鼻咽喉科"],
    "頭頸部・耳鼻いんこう科": ["耳鼻咽喉科"],
}
# 診療科ではない欄（「該当なし」の意味）
NOT_DEPT = {"標榜科目以外"}


def dept_group(ja: str, groups: set) -> list:
    if ja == "産婦人科":  # 産科・婦人科のページに載せる（産婦人科の訳は施設ページの科名に使う）
        return ["産科", "婦人科"]
    if ja in groups:
        return [ja]
    if ja in EXACT:
        return [EXACT[ja]]
    if ja in SUB:
        return [g for g in SUB[ja] if g in groups]
    if "歯科" in ja:
        return ["歯科"]
    if ja == "美容外科":
        return []
    if ja.endswith("内科"):
        if "循環器" in ja:
            return ["循環器内科"]
        if "呼吸器" in ja:
            return ["呼吸器内科"]
        if "消化器" in ja:
            return ["消化器内科"]
        return ["内科"]
    if ja.endswith("外科") and "形成" not in ja and "整形" not in ja and "脳神経" not in ja:
        return ["外科"]
    return []


BRANDS = [
    ("ＶＩＳＡ", "Visa"),
    ("Ｍａｓｔｅｒ", "Mastercard"),
    ("ＪＣＢ", "JCB"),
    ("Ａｍｅｒｉｃａｎ Ｅｘｐｒｅｓｓ", "American Express"),
    ("Ｄｉｎｅｒｓ", "Diners Club"),
    ("ＤＩＳＣＯＶＥＲ", "Discover"),
    ("中国銀聯", "UnionPay"),
    ("交通系電子マネー", "Suica"),
    ("iＤ", "iD"),
    ("QUICPay", "QUICPay"),
    ("Ｅｄｙ", "Edy"),
]


def cards(brands: list) -> list:
    out = []
    for b in brands:
        for key, name in BRANDS:
            if b.startswith(key) and name not in out:
                out.append(name)
    return out


def hours_of(h: dict) -> dict:
    src = h.get("診療時間") or h.get("外来受付時間") or {}
    out = {}
    for ja, en in DAYS:
        v = src.get(ja)
        if v:
            out[en] = [re.sub(r"\b0(\d):", r"\1:", s.strip()) for s in re.split(r"[ 　,、]+", v) if re.match(r"\d", s.strip())]
    return out


def main():
    fac = json.load(open(ING / "merged_facility.json"))
    rows = json.load(open(ING / "merged_facility_language.json"))
    dic = json.load(open(ROOT / "data" / "dict" / "dictionary.json"))

    # ポルトガル語にスペイン語の綴りが混ざっていないか（出典の誤記：kifjp の Psiquiatría、厚労省の Neurocirugia）
    es = [r for r in dic if r["lang"] == "pt" and r["text"] and re.search(r"ía\b|cirugia|ología|\by\b", r["text"])]
    if es:
        raise SystemExit("ポルトガル語にスペイン語の綴りがあります: " + ", ".join(f"{r['value_ja']}={r['text']}" for r in es))

    dept_dict = {}
    for r in dic:
        if r["kind"] == "department" and r["text"]:
            dept_dict.setdefault(r["value_ja"], {})[r["lang"]] = {"text": r["text"], "src": r["source_url"]}
    # 親の科は英語の訳（JNTO・東京都）がある科だけ。産婦人科は英語の訳がないため産科＋婦人科に分ける
    groups = {k for k, v in dept_dict.items() if "en" in v}

    by_fac = {}
    for r in rows:
        by_fac.setdefault(r["facility_id"], []).append(r)

    out = []
    for f in fac:
        lrows = by_fac.get(f["id"])
        if not lrows:
            continue
        depts = []
        seen = set()
        for h in f["dept_hours"]:
            # 1つの欄に複数の科が入っていることがある（「総合診療科、渡航者医療センター、感染症科…」）
            for ja in [x.strip() for x in re.split(r"[、，,]", h["dept"]) if x.strip()]:
                if ja in seen or ja in NOT_DEPT:
                    continue
                seen.add(ja)
                depts.append({"ja": ja, "groups": dept_group(ja, groups), "hours": hours_of(h)})
        spoken = {}
        # 同じ言語に医療情報ネットの行と D-5 の行が別にある場合は、良い方の tier を採る
        for r in sorted(lrows, key=lambda r: TIER_ORDER[r["tier"]], reverse=True):
            prev = spoken.get(r["lang"])
            spoken[r["lang"]] = {
                "tier": TIER_CODE[r["tier"]],
                "status": r.get("status"),
                "booking": {"要予約": True, "予約不要": False}.get(r.get("booking")),
                "phoneForeign": r.get("phone_foreign"),
                "days": [en for ja, en in DAYS if ja in (r.get("days") or [])],
                "depts": r.get("depts"),
                "source": r["source"],
                "basis": r["basis"],
            }
            if prev:  # 良い方の行に無い項目（電話・予約など）は、もう一方の行から補う
                cur = spoken[r["lang"]]
                for k in ("status", "booking", "phoneForeign", "days", "depts"):
                    if cur[k] in (None, []) and prev[k] not in (None, []):
                        cur[k] = prev[k]
                cur["source"] = "both"
                cur["basis"] = prev["basis"] + cur["basis"]
        site = {}
        for sl, langs in SITE_LANGS.items():
            best = None
            for l in langs:
                if l in spoken and (best is None or spoken[l]["tier"] < best["tier"]):
                    best = dict(spoken[l], spoken=l)
            if best:
                site[sl] = best
        d5 = f.get("d5")
        out.append({
            "id": f["id"],
            "kind": KIND[f["kikan_kbn"]],
            "nameJa": f["name_ja"],
            "nameEn": f["name_en"],
            "addressJa": f["address_ja"],
            "addressEn": f["address_en"],
            "postal": f["postal"],
            "prefCode": f["pref_code"],
            "cityCode": f["city_code"],
            "phone": f["phone"],
            "url": f["url"],
            "lat": float(f["lat"]) if f.get("lat") else None,
            "lng": float(f["lng"]) if f.get("lng") else None,
            "updated": f["source_mhlw_updated"],
            "translationDevice": bool(f.get("translation_device_sources")),
            # 翻訳機の出典（mhlw=医療情報ネット／d5=厚労省の受入医療機関リスト）。画面では出典ごとに示す
            "translationDeviceSources": f.get("translation_device_sources") or [],
            "cards": cards(f["cashless"]["brands"]),
            "emergencyJa": f["emergency"],
            "jmip": f["jmip"],
            "d5": {"h24": d5.get("h24"), "category": d5.get("category"), "cards": d5.get("cards")} if d5 else None,
            "depts": depts,
            "spoken": spoken,
            "site": site,
        })

    # 地域：住所の先頭（都道府県＋市区町村）を data/geo/municipalities.json（日本郵便）と突き合わせ、URL 名を決める
    muni = json.load(open(ROOT / "data" / "geo" / "municipalities.json"))
    muni.sort(key=lambda m: -len(m["prefJa"] + m["cityJa"]))
    areas = {}
    for x in out:
        m = next((m for m in muni if x["addressJa"].startswith(m["prefJa"] + m["cityJa"])), None)
        if not m:
            raise SystemExit(f"市区町村が分かりません: {x['id']} {x['addressJa']}")
        a = areas.setdefault(x["cityCode"], {"prefCode": x["prefCode"], "prefSlug": m["prefSlug"], "cityCode": x["cityCode"],
                                             "citySlug": m["citySlug"], "prefJa": m["prefJa"], "cityJa": m["cityJa"]})
        if a["cityJa"] != m["cityJa"]:
            raise SystemExit(f"同じ市区町村コードで名前が違います: {x['cityCode']} {a['cityJa']} / {m['cityJa']}")

    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(OUT / "facilities.json", "w"), ensure_ascii=False)
    json.dump(sorted(areas.values(), key=lambda a: a["cityCode"]), open(OUT / "areas.json", "w"), ensure_ascii=False, indent=1)
    print(len(areas), "areas")
    json.dump({k: v for k, v in dept_dict.items()}, open(OUT / "departments.json", "w"), ensure_ascii=False, indent=1)
    print(len(out), "facilities")
    for sl in SITE_LANGS:
        c = {}
        for x in out:
            if sl in x["site"]:
                c[x["site"][sl]["tier"]] = c.get(x["site"][sl]["tier"], 0) + 1
        print(sl, dict(sorted(c.items())))


if __name__ == "__main__":
    main()
