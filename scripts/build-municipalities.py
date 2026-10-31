#!/usr/bin/env python3
"""市区町村の URL 名（slug）の表を作る。data/geo/municipalities.json

出典：日本郵便「郵便番号データ（ローマ字）」KEN_ALL_ROME.CSV
  https://www.post.japanpost.jp/service/search/zipcode/download/roman-zip.html
slug は URL に使うだけで、画面の地名には使わない（画面の地名は辞書の「実測」行、無ければ日本語）。

使い方：python3 scripts/build-municipalities.py <KEN_ALL_ROME.CSV（cp932）>
slug の決め方：
  - 種別の語（SHI/KU/CHO/MACHI/MURA/SON）と「〜GUN」を外す（SHINJUKU KU → shinjuku）
  - 政令市の区は市と区をつなぐ（OSAKA SHI KITA KU → osaka-kita）
  - 同じ都道府県の中でぶつかったら、区・市が1つだけならそれを短いまま、ほかは種別の語を残す（toshima／toshima-mura）。それでもぶつかれば郡名を前に付ける
  - 一度決めた slug は変えない（KEEP に固定。公開済みの URL を守るため）
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "geo" / "municipalities.json"
KIND = {"SHI", "KU", "CHO", "MACHI", "MURA", "SON"}
# 公開済みの URL
KEEP = {("東京都", "新宿区"): ("tokyo", "shinjuku")}


def words(s: str) -> list[str]:
    return [w for w in re.split(r"\s+", s.strip()) if w]


def short(rome: str) -> str:
    w = words(rome)
    if len(w) >= 2 and w[1] == "GUN":  # 〜郡 〜町
        w = w[2:]
    parts, cur = [], []
    for x in w:
        if x in KIND:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(x)
    if cur:
        parts.append("".join(cur))
    return "-".join(p.lower() for p in parts if p)


def full(rome: str, keep_gun: bool = False) -> str:
    w = words(rome)
    if len(w) >= 2 and w[1] == "GUN":
        w = [w[0]] + w[2:] if keep_gun else w[2:]
    return "-".join(x.lower() for x in w)


def main() -> int:
    src = sys.argv[1]
    seen = {}
    with open(src, encoding="cp932") as f:
        for row in csv.reader(f):
            pref_ja, city_ja, pref_ro, city_ro = row[1], row[2].replace("　", ""), row[4], row[5]
            seen.setdefault((pref_ja, city_ja), (pref_ro, city_ro))
    out, used = [], {}
    for (pref_ja, city_ja), (pref_ro, city_ro) in seen.items():
        pref_slug = words(pref_ro)[0].lower()
        if (pref_ja, city_ja) in KEEP:
            pref_slug, slug = KEEP[(pref_ja, city_ja)]
        else:
            slug = short(city_ro)
        out.append({"prefJa": pref_ja, "cityJa": city_ja, "prefSlug": pref_slug, "citySlug": slug, "rome": city_ro})
        used.setdefault((pref_slug, slug), []).append(out[-1])
    rank = lambda x: 0 if words(x["rome"])[-1] in ("KU", "SHI") else 1
    for (_, _), xs in used.items():
        if len(xs) > 1:
            # 区・市が1つだけなら、それは短い名前のまま（豊島区 toshima／利島村 toshima-mura）
            top = [x for x in xs if rank(x) == 0]
            for x in xs:
                if (x["prefJa"], x["cityJa"]) in KEEP or (len(top) == 1 and x is top[0]):
                    continue
                x["citySlug"] = full(x["rome"])
    # それでもぶつかる町村（例：北海道の檜山郡江差町と枝幸郡枝幸町）は郡名を前に付ける
    again = {}
    for x in out:
        again.setdefault((x["prefSlug"], x["citySlug"]), []).append(x)
    for xs in again.values():
        if len(xs) > 1:
            for x in xs:
                x["citySlug"] = full(x["rome"], keep_gun=True)
    dup = {}
    for x in out:
        dup.setdefault((x["prefSlug"], x["citySlug"]), []).append(x["cityJa"])
    bad = {k: v for k, v in dup.items() if len(v) > 1}
    if bad:
        raise SystemExit(f"slug が重複しています: {bad}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=0)
    print(len(out), "municipalities")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
