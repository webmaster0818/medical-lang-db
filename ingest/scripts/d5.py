#!/usr/bin/env python3
"""厚労省「外国人患者を受け入れる医療機関」リスト（D-5, Excel）を読み、言語ごとの対応方法に分解する。
列（東京都シートで確認）: 2 医療機関名 / 3 英語名 / 5 住所 / 7 電話 / 12 対応診療科と対応外国語 / 13-19 カード / 20 その他キャッシュレス
  / 21 24時間365日 / 23 JMIP / 25 拠点（カテゴリー1・2）/ 26 種別 / 27 救急医療体制
  / 28-29 専門部署(○)と言語・日時 / 30-31 医療コーディネーター / 32-33 医療通訳者 / 34-35 遠隔通訳 / 36-37 その他の言語サポート
"""
import re, unicodedata, openpyxl

# D-5 の言語表記 → 内部コード。「中国語」「ZH」は北京語（普通話）として zh を返し、簡体・繁体の両方に効かせる
LANG = [
    (r'\bEN\b|英語', 'en'), (r'\bKO\b|韓国語|朝鮮語', 'ko'), (r'台湾語', 'zh-tw'), (r'広東語', 'yue'),
    (r'\bZH\b|中国語|北京語|普通話', 'zh'), (r'\bVI\b|ベトナム語', 'vi'), (r'\bPT\b|ポルトガル語', 'pt'),
    (r'\bES\b|スペイン語|西語', 'es'), (r'\bFR\b|フランス語|仏語', 'fr'), (r'\bDE\b|ドイツ語|独語', 'de'),
    (r'\bTH\b|タイ語', 'th'), (r'\bTL\b|タガログ語|ダガログ語|フィリピン語', 'tl'), (r'\bNE\b|ネパール語', 'ne'),
    (r'\bID\b|インドネシア語', 'id'), (r'\bMY\b|ミャンマー語|ビルマ', 'my'), (r'\bRU\b|ロシア語', 'ru'),
    (r'\bIT\b|イタリア語', 'it'), (r'\bMN\b|モンゴル語', 'mn'), (r'\bBN\b|ベンガル語', 'bn'), (r'\bHI\b|ヒンディー語', 'hi'),
    (r'\bAR\b|アラビア語', 'ar'), (r'\bTR\b|トルコ語', 'tr'), (r'\bSI\b|シンハラ語', 'si'), (r'\bUR\b|ウルドゥ', 'ur'),
    (r'\bKM\b|クメール', 'km'), (r'\bMS\b|マレー語', 'ms'), (r'ウクライナ語', 'uk'), (r'ペルシア語|ペルシャ語', 'fa'),
]
DEVICE = re.compile(r'翻訳機|翻訳システム|KOTOBAL|ポケトーク|音声翻訳|多言語対応音声|翻訳アプリ|VoiceBiz|翻訳器', re.I)
MANY = re.compile(r'(\d{2,})言語|多言語')
REMOTE = re.compile(r'タブレット|テレビ電話|ビデオ通話|電話通訳|遠隔|オンライン通訳|通訳サービス|提携|メディフォン|mediphone', re.I)


def langs_in(s):
    s = unicodedata.normalize('NFKC', str(s or ''))
    out = []
    for pat, code in LANG:
        if re.search(pat, s) and code not in out: out.append(code)
    return out


def norm_name(s):
    s = unicodedata.normalize('NFKC', str(s or ''))
    s = re.sub(r'(医療法人社団|医療法人財団|医療法人|社会医療法人|社会福祉法人|一般社団法人|公益社団法人|一般財団法人|公益財団法人|'
               r'地方独立行政法人|独立行政法人|国立研究開発法人|特定医療法人|東京都立病院機構|国立健康危機管理研究機構|地域医療機能推進機構|'
               r'[^\s]{1,8}会(?=[^\s]))', '', s)
    s = re.sub(r'[\s・　\-－()（）]', '', s)
    return s.lower()


def norm_tel(s):
    d = re.sub(r'\D', '', unicodedata.normalize('NFKC', str(s or '')))
    return d[-10:] if len(d) >= 10 else d


def load(xlsx, sheet='13.東京都', addr_kw=None):
    ws = openpyxl.load_workbook(xlsx, read_only=True)[sheet]
    res = []
    for r in list(ws.iter_rows(values_only=True))[3:]:
        if not r or not r[2]: continue
        if addr_kw and addr_kw not in str(r[5] or ''): continue
        langs = langs_in(r[12])
        meth = {}
        for key, flag, txt in (('dept', 28, 29), ('coordinator', 30, 31), ('interpreter', 32, 33), ('remote', 34, 35), ('other', 36, 37)):
            if r[flag] or r[txt]:
                t = str(r[txt] or '')
                tl = langs_in(t)
                meth[key] = dict(text=t.strip() or None, langs=tl or langs, langs_explicit=bool(tl),
                                 device=bool(DEVICE.search(t)), remote=bool(REMOTE.search(t)), many=bool(MANY.search(t)))
        for m in meth.values():  # 対応言語の列が空でも、方法の欄に書かれた言語は対応言語に含める
            for x in m['langs']:
                if x not in langs: langs.append(x)
        cards = [n for n, i in (('VISA', 13), ('Mastercard', 14), ('AMEX', 15), ('Diners', 16), ('JCB', 17), ('UnionPay', 18)) if r[i]]
        res.append(dict(
            d5_name=str(r[2]).strip(), d5_name_en=(str(r[3]).strip() if r[3] else None), address=str(r[5] or '').strip(),
            tel=str(r[7] or '').strip(), hours=str(r[8] or '').strip() or None, depts_langs=str(r[12] or '').strip(),
            langs=langs, cards=cards, cashless_other=(str(r[20]).strip() if r[20] else None),
            h24=bool(r[21]), jmip=bool(r[23]), category=(str(r[25]).strip() if r[25] else None),
            kind=(str(r[26]).strip() if r[26] else None), emergency=(str(r[27]).strip() if r[27] else None), methods=meth))
    return res
