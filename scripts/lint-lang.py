#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""訳の綴り検査（taro-2 / 2026-11-01。npm run build の前に自動で回す）
1) ポルトガル語にスペイン語だけの綴りが混ざっていないか
2) 簡体字の欄に繁体字だけの字／繁体字の欄に簡体字だけの字が混ざっていないか
3) 韓国語・ベトナム語の欄に日本語の文字が混ざっていないか
使い方: python3 lint_lang.py <JSONファイル...>   終了コード 0=問題なし / 1=あり
"""
import json, sys, re

# 簡体字と繁体字で字が違うものだけを対にする（同じ字は入れない）
PAIRS = [
    ("医","醫"),("疗","療"),("诊","診"),("脑","腦"),("脏","臟"),("胆","膽"),("学","學"),
    ("体","體"),("妇","婦"),("产","產"),("儿","兒"),("内","內"),("伤","傷"),("镜","鏡"),
    ("护","護"),("药","藥"),("检","檢"),("验","驗"),("济","濟"),("泻","瀉"),("滨","濱"),
    ("县","縣"),("华","華"),("汉","漢"),("东","東"),("车","車"),("门","門"),("风","風"),
    ("马","馬"),("齿","齒"),("龙","龍"),("义","義"),("节","節"),("丰","豐"),("云","雲"),
    ("几","幾"),("击","擊"),("区","區"),("历","歷"),("旧","舊"),("归","歸"),("书","書"),
    ("乐","樂"),("习","習"),("乡","鄉"),("长","長"),("鸟","鳥"),("岛","島"),("国","國"),
    ("园","園"),("图","圖"),("团","團"),("关","關"),("观","觀"),("广","廣"),("汤","湯"),
    ("泽","澤"),("爱","愛"),("实","實"),("樱","櫻"),("发","發"),("湾","灣"),("丽","麗"),
]
SIMP = {a for a, b in PAIRS}
TRAD = {b for a, b in PAIRS}
# ポルトガル語に現れたらスペイン語混入の疑い
PT_BAD = [("ía", "スペイン語の -ía（ポルトガル語は -ia）"),
          ("ugia", "スペイン語系の cirugia（ポルトガル語は cirurgia）"),
          ("ugía", "同上"),
          ("ología", "スペイン語の -ología（ポルトガル語は -ologia）"),
          (" y ", "スペイン語の y（ポルトガル語は e）")]
JP = re.compile(r'[぀-ヿ]')          # ひらがな・カタカナ
JPK = re.compile(r'[一-鿿]')         # 漢字（ko・vi には出ない想定）


def rows(obj):
    """{ja: {lang: {text}}} 形式と [{value_ja,lang,text}] 形式の両方を読む"""
    if isinstance(obj, dict) and obj and all(isinstance(v, dict) and all(isinstance(x, str) for x in v.values()) for v in obj.values()):
        # data/ui/strings.json：{lang: {key: text}}
        for lg, m in obj.items():
            for k, t in m.items():
                yield k, lg, t
        return
    if isinstance(obj, list):
        for x in obj:
            yield x.get("value_ja", "?"), x.get("lang", "?"), x.get("text", "")
    else:
        for ja, m in obj.items():
            if str(ja).startswith("_"):
                continue
            for lg, v in (m or {}).items():
                if isinstance(v, dict):
                    yield ja, lg, v.get("text", "")


# 画面でわざと日本語のまま見せる固有名（利用者が日本の画面で探せるように）
JA_PROPER = ["医療情報ネット"]


def main(paths):
    bad = []
    for p in paths:
        for ja, lg, t in rows(json.load(open(p))):
            if not t:
                continue
            for name in JA_PROPER:
                t = t.replace(name, "")
            if lg == "pt":
                for pat, why in PT_BAD:
                    if pat in t:
                        bad.append((p, ja, lg, t, why)); break
            elif lg == "zh-hans":
                x = [c for c in t if c in TRAD]
                if x:
                    bad.append((p, ja, lg, t, "繁体字だけの字: " + "".join(x)))
            elif lg == "zh-hant":
                x = [c for c in t if c in SIMP]
                if x:
                    bad.append((p, ja, lg, t, "簡体字だけの字: " + "".join(x)))
            elif lg in ("ko", "vi"):
                x = JP.findall(t) + JPK.findall(t)
                if x:
                    bad.append((p, ja, lg, t, "日本語の文字: " + "".join(x)))
    for p, ja, lg, t, why in bad:
        print("NG %-26s %-14s %-8s %-30s %s" % (p.split("/")[-1], ja, lg, t[:30], why))
    print("検査 %d ファイル / NG %d 件" % (len(paths), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
