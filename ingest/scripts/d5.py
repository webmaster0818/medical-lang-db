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
# 2026-10-31 追加（tomomi-2 決定）：D-5 全国38シートの記述から、翻訳機・翻訳アプリを指す語を足す。
# DEVICE（旧）は遠隔通訳・人の対応の判定に従来どおり使い（○・◎は動かさない）、DEVICE_ALL は「翻訳機あり」の判定だけに使う
DEVICE_ADD = re.compile(r'翻訳端末|端末の利用|翻訳ソフト|通訳ソフト|翻訳ツール|通訳ツール|多言語ツール|多言語対応ツール|コミュニケーションツール|'
                        r'機械翻訳|機械通訳|機械・アプリ|自動翻訳|AI翻訳|AI通訳|AIを用いた|\(AI\)翻訳|翻訳エディタ|'
                        r'通訳アプリ|通約アプリ|アプリ翻訳|アプリを使|アプリにて|アプリによる|アプリで|アプリの|スマートフォンアプリ|アプリケーション|外国語アプリ|専用アプリ|翻訳系アプリ|'
                        r'Goo?gle翻訳|Goole翻訳|DeepL|ChatGPT|VoiceTra|Voice Tra|ボイストラ|POCKETALK|POKETALK|POCKTALK|pocketalk|Buddycom翻訳|ドコツー|Talk-Trans|'
                        r'スマホ翻訳|スマホ通訳|スマートフォン翻訳|スマートフォンによる|スマホによる翻訳|スマホを利用した翻訳|スマートフォン通訳|iPhone内アプリ|'
                        r'音声通訳|通訳機|翻訳期|翻訳機器|通訳機器|翻訳タブレット|翻訳用タブレット|タブレット(端末)?(を利用した|による|を使用した|の)?(機械)?翻訳|'
                        r'タブレットによる翻訳|ipad通訳|iPad通訳|iPad翻訳|iPadの翻訳|ipad\(VoiceTra\)|医療翻訳ツール', re.I)
# 否定の書き方（「翻訳機なし」「使用していません」等）は翻訳機ありにしない
DEVICE_NEG = re.compile(r'(翻訳機|翻訳器|翻訳|アプリ|端末|ツール|ポケトーク)(は|を|の)?(なし|無し|ありません|ない|不可|使用していません|使用しておりません|利用していません|未導入|未設置|導入していません)')
# 医師がその言語で対応する記述（「対話可能な医師による対応:EN」「英語を話せる医師による外来」等）
DOCTOR = re.compile(r'(対話可能な|対応可能な|話せる|が話せる|の話せる)?(歯科)?医師(等|及び|と)?(による|が|の|対応|常駐|が常勤|外来)')
DOCTOR_STOP = re.compile(r'翻訳|端末|アプリ|機械|タブレット|職員|事務員|スタッフ|ボランティア|通訳可能な|ツール|電話')

MANY = re.compile(r'(\d{2,})言語|多言語')
REMOTE = re.compile(r'タブレット|テレビ電話|ビデオ通話|電話通訳|遠隔|オンライン通訳|通訳サービス|提携|メディフォン|mediphone', re.I)


def langs_in(s):
    s = unicodedata.normalize('NFKC', str(s or ''))
    out = []
    for pat, code in LANG:
        if re.search(pat, s) and code not in out: out.append(code)
    return out


def doctor_langs(t):
    """医師がその言語で対応する記述から言語を取り出す。言語名は医師の語の前後（他の方法の語まで）に書かれたものだけを数える"""
    t = unicodedata.normalize('NFKC', str(t or ''))
    out = []
    for m in DOCTOR.finditer(t):
        if not re.search(r'話せる|対話可能|対応可能|による対応|による外来|医師対応|医師が対応|医師の対応|診察医師|診療医師|英語対応|常駐|常勤|医師による通訳|医師の一部', t[max(0, m.start()-12):m.end()+8]):
            continue
        before = re.split(r'[、,\n]|翻訳|端末|アプリ|職員|スタッフ', t[max(0, m.start()-12):m.start()])[-1]
        after = t[m.end():m.end()+40]
        stop = DOCTOR_STOP.search(after)
        if stop: after = after[:stop.start()]
        for x in langs_in(before) + langs_in(after):
            if x not in out: out.append(x)
    return out


def device_all(t):
    t = unicodedata.normalize('NFKC', str(t or ''))
    if DEVICE_NEG.search(t): return False
    return bool(DEVICE.search(t) or DEVICE_ADD.search(t))


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
                                 device=bool(DEVICE.search(t)), device_all=device_all(t), device_neg=bool(DEVICE_NEG.search(unicodedata.normalize('NFKC', t))),
                                 doctor_langs=doctor_langs(t), remote=bool(REMOTE.search(t)), many=bool(MANY.search(t)))
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
