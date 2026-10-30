#!/usr/bin/env python3
"""医療情報ネット 施設詳細HTML（data/raw/<id>.html.gz）から、strategy §5 の facility / facility_language を取り出す。
- 再取得は不要（保存済みHTMLだけを読む）。項目を足すときはこのスクリプトだけ直して流し直す
- 出力: <out_dir>/facility.jsonl, facility_language.jsonl, sections.jsonl（全セクションの項目名→値。取りこぼし確認用）
使い方: parse.py <targets.json> <raw_dir> <out_dir> [<opendata_dir>]
"""
import json, sys, os, re, gzip, csv, html as H
from bs4 import BeautifulSoup
sys.path.insert(0, os.path.dirname(__file__))
import d5 as D5

WEEK = ['月', '火', '水', '木', '金', '土', '日', '祝']
LANG_CODE = {  # 医療情報ネットの言語名 → 話す言語のコード（北京語=zh・台湾語=zh-tw・広東語=yue。サイトの簡体/繁体とは別に持つ）
    '英語': 'en', '韓国語': 'ko', '韓国・朝鮮語': 'ko', '北京語': 'zh', '台湾語': 'zh-tw', '広東語': 'yue', 'ベトナム語': 'vi',
    'ポルトガル語': 'pt', 'タイ語': 'th', 'タガログ語': 'tl', 'ミャンマー語': 'my', 'ベンガル語': 'bn', 'フランス語': 'fr',
    'ドイツ語': 'de', 'ロシア語': 'ru', 'イタリア語': 'it', 'スペイン語': 'es', 'インドネシア語': 'id', 'トルコ語': 'tr',
    'マレー語': 'ms', 'ヒンディー語': 'hi', 'ネパール語': 'ne', 'シンハラ語': 'si', 'その他': 'other',
}


def txt(el):
    if el is None: return ''
    for tip in el.select('.tooltipBlock, .yougoKaisetsuText'): tip.decompose()
    s = el.get_text(' ', strip=True).replace('\xa0', ' ')
    return re.sub(r'\s+', ' ', s).strip()


def val(s):
    s = (s or '').strip()
    return None if re.fullmatch(r'[-\s　]*', s) else s


def sections(soup):
    """セクション名 → {項目名: 値} と、セクションの要素を返す"""
    out = {}; els = {}
    for item in soup.select('div.item'):
        h = item.select_one('.acTitle')
        if not h: continue
        name = re.sub(r'\s+', ' ', h.get_text(strip=True))
        det = item.select_one('div.details')
        if det is None: continue
        kv = out.setdefault(name, {}); els.setdefault(name, []).append(det)
        for tr in det.select('tr'):
            lab = tr.select_one('label.ptn1ItemName, label.ptn2ItemName')
            if lab is None: continue
            td = tr.find('td')
            k = re.sub(r'\s+', ' ', lab.get_text(strip=True)); v = txt(td)
            if k in kv and kv[k] != v: kv[k] = kv[k] + ' / ' + v
            else: kv[k] = v
        for tb in det.select('table.ptn6Item'):  # 2列の項目一覧（該当するものだけ並ぶ）
            items = [txt(td) for td in tb.select('td')]
            kv.setdefault('_list', []).extend([x for x in items if val(x)])
    return out, els


def lang_blocks(soup):
    res = []
    for blk in soup.select('div.ptn9DataArea'):
        d = {}
        for tb in blk.select('table'):
            lab = tb.select_one('label.ptn1ItemName'); td = tb.find('td')
            if lab is None: continue
            d[re.sub(r'\s+', ' ', lab.get_text(strip=True))] = txt(td)
        if d.get('対応可能な外国語名'): res.append(d)
    return res


def dept_hours(els):
    """診療科目ごとの曜日×時間（表パターン3）"""
    res = []
    for det in els:
        for area in det.select('div.ptn3DataArea'):
            h3 = area.find('h3'); name = h3.get_text(strip=True).lstrip('◆') if h3 else ''
            ann = txt(area.select_one('.annotation'))
            rows = {}
            for tr in area.select('tr'):
                th = tr.select_one('th.ptn3ItemName')
                if th is None: continue
                k = txt(th); tds = [txt(td) for td in tr.find_all('td')]
                if len(tds) == 8: rows[k] = dict(zip(WEEK, [val(x) for x in tds]))
            flags = dict(re.findall(r'(初診時予約|予約外診察|入院患者受入|女性医師外来診察)：\s*(\S+?)[、）]', ann))
            res.append(dict(dept=name, flags=flags, **rows))
    return res


def last_updated(t):
    m = re.search(r'最終更新日：\s*(?:<[^>]+>\s*)*(\d{4}/\d{1,2}/\d{1,2})', t)
    return m.group(1) if m else None


def norm_days(s):
    s = val(s)
    return [w for w in WEEK + ['祝日'] if s and w in s.split()] if s else []


def parse_one(path, tg, od):
    t = gzip.open(path).read().decode('utf-8', 'replace')
    soup = BeautifulSoup(t, 'lxml')
    sec, els = sections(soup)
    g = lambda s, k: val(sec.get(s, {}).get(k))
    langs = lang_blocks(soup)
    device = g('多言語音声翻訳機器を利用した対応', '多言語音声翻訳機器を利用した対応')
    f = dict(
        id=tg['id'], mhlw_id=tg['id'], kikan_kbn={'1': 'hospital', '2': 'clinic', '3': 'dental'}[tg['kbn']],
        name_ja=g('施設詳細', '正式名称') or tg['name'], name_kana=g('施設詳細', '正式名称（フリガナ）'),
        name_en=g('施設詳細', '英語表記（ローマ字表記）'),
        postal=g('所在地詳細', '郵便番号'), address_ja=g('所在地詳細', '所在地'), address_en=g('所在地詳細', '英語表記'),
        pref_code=tg['pref'], city_code=tg.get('city_code'),
        phone=g('電話番号・FAX番号', '案内用電話番号') or g('電話番号・FAX番号', '電話番号'),
        phone_night=g('電話番号・FAX番号', '夜間・休日の案内用電話番号'),
        url=g('案内用ホームページアドレス', '案内用ホームページアドレス'),
        dept_hours=dept_hours(els.get('診療科目・診療日、診療時間、外来受付時間、予約診療の有無', [])),
        emergency=[k for k, v in sec.get('救急医療機関', {}).items() if k != '_list' and val(v) in ('該当', '有り', '可能')] + sec.get('救急医療機関', {}).get('_list', []),
        online_consult=g('オンライン診療実施の有無及びその内容', 'オンライン診療実施の有無') or g('オンライン診療実施の有無及びその内容', 'オンライン診療'),
        cashless=dict(
            any=g('電子決済サービスの有無', '電子決済サービスへの対応'),
            credit=g('対応可能な決済サービス', 'クレジットカード決済'), debit=g('対応可能な決済サービス', 'デビットカード決済'),
            other=g('対応可能な決済サービス', 'その他電子決済'),
            brands=sec.get('決済サービス名称', {}).get('_list', [])),
        translation_device=device,
        foreign_dept_contact=g('外国人の患者の受入れ体制 外国人患者受入れに関する連絡調整の担当部署', '外国人患者受入れに関する連絡調整の担当部署'),
        hub_selected='外国人患者を受け入れる拠点的な医療機関への選出' in sec.get('その他の院内サービス等', {}).get('_list', []),
        jmip=any('JMIP' in x for x in sec.get('その他の院内サービス等', {}).get('_list', [])),
        foreign_support=g('外国人の患者の受入れに関するサポート体制の整備', '外国人の患者に対するサポート体制'),
        foreign_support_note=g('外国人の患者の受入れに関するサポート体制の整備', '特記事項（外国人の患者に対するサポート体制）'),
        foreign_dept_phone=g('外国人の患者の受入れ体制 外国人患者受入れに関する連絡調整の担当部署', '担当部署の電話番号'),
        self_pay_ratio=g('外国人の患者の受入れ体制 自費診療時の金額等について', '自費診療時の金額 診療報酬点数の割合（数値）') or g('外国人の患者の受入れ体制 自費診療時の金額等について', '自費診療時の金額 診療報酬点数の割合'),
        english_certificate=g('外国人の患者の受入れ体制 自費診療時の金額等について', '英文診断書の発行 区分'),
        designations=sec.get('保険医療機関、公費負担医療機関及びその他の病院の種類', {}).get('_list', []) or sec.get('保険医療機関、公費負担医療機関及びその他の診療所の種類', {}).get('_list', []),
        source_mhlw_updated=last_updated(t),
    )
    if od and tg['id'] in od:
        f['lat'], f['lng'] = od[tg['id']]
    fl = []
    for b in langs:
        name = b.get('対応可能な外国語名')
        if name in LANG_CODE: codes = [LANG_CODE[name]]
        else:  # 「その他」欄は自由記述（例：モンゴル語，ヒンディー語…）。言語名を拾えたものだけ行にする
            codes = D5.langs_in(name) if val(name) else []
            if val(name) and not codes: codes = ['other']
        for code in codes:
          fl.append(dict(
            facility_id=tg['id'], lang_ja=name, lang=code,
            status_ja=val(b.get('対応可否区分')),
            status={'受入可能': 'accepted', '要相談': 'consult'}.get(val(b.get('対応可否区分')) or '', None),
            days_kbn=val(b.get('対応可能曜日区分')), hours_kbn=val(b.get('対応可能時間帯区分')),
            days=norm_days(b.get('対応可能な曜日')), hours=val(b.get('対応可能時間帯')),
            depts_kbn=val(b.get('対応可能な診療科目')), depts=(val(b.get('対応可能な診療科目名')) or '').split() or None,
            phone_foreign=val(b.get('対応可能な電話番号')), phone_note=val(b.get('対応可能な電話番号備考')),
            booking=val(b.get('予約')), booking_note=val(b.get('予約備考')), note=val(b.get('特記事項')),
            level=val(b.get('会話のレベル')) or val(b.get('対応可能レベル')),
            translation_device=device, source='mhlw'))
    return f, fl, dict(id=tg['id'], sections={k: v for k, v in sec.items()})


def main():
    targets, raw, out = sys.argv[1:4]
    odd = sys.argv[4] if len(sys.argv) > 4 else None
    od = {}
    if odd:
        for fn in os.listdir(odd):
            if fn.endswith('facility_info_20260601.csv'):
                for r in csv.DictReader(open(os.path.join(odd, fn), encoding='utf-8-sig')):
                    od[r['ID']] = (r['所在地座標（緯度）'], r['所在地座標（経度）'])
    os.makedirs(out, exist_ok=True)
    F = open(os.path.join(out, 'facility.jsonl'), 'w'); L = open(os.path.join(out, 'facility_language.jsonl'), 'w')
    S = open(os.path.join(out, 'sections.jsonl'), 'w')
    n = miss = 0
    for tg in json.load(open(targets)):
        p = os.path.join(raw, tg['id'] + '.html.gz')
        if not os.path.exists(p): miss += 1; continue
        f, fl, s = parse_one(p, tg, od)
        F.write(json.dumps(f, ensure_ascii=False) + '\n')
        for x in fl: L.write(json.dumps(x, ensure_ascii=False) + '\n')
        S.write(json.dumps(s, ensure_ascii=False) + '\n'); n += 1
    print('parsed', n, 'missing', miss)


if __name__ == '__main__':
    main()
