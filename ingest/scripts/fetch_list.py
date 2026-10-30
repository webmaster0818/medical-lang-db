#!/usr/bin/env python3
"""全国取得の第1段：医療情報ネットの「外国語で探す」検索結果から、外国語対応の施設ID（kikanCd・区分・都道府県）を集める。
- 言語×都道府県ごとに 1ページ20件を最後のページまで取る（件数の指定は効かない）
- 取得済みのページ（data/list/<lang>_<pref>_<page>.html.gz）は飛ばす＝止めても続きから再開できる
- 1本ずつ、応答のあと GAP 秒待つ。--window 22-6 で夜間だけ動かす
- 出力：data/list_ids.json（ID→対応言語の一覧）。第2段は fetch.py にこのIDを渡して施設詳細を取る
使い方: fetch_list.py <out_dir> [--langs 0001,0002,...] [--prefs 01,...,47] [--gap 6] [--window 22-6]
※第1週（新宿区のみ）では実行しない。全国の取得は tomomi-2 の確認後
"""
import os, re, sys, time, gzip, json, argparse, datetime, urllib.request, urllib.parse
LANGS = {'0001': '英語', '0002': '広東語', '0003': '北京語', '0004': '台湾語', '0005': '韓国・朝鮮語', '0006': 'タイ語',
         '0007': 'タガログ語', '0008': 'ミャンマー語', '0009': 'ベトナム語', '0010': 'ベンガル語', '0011': 'フランス語',
         '0012': 'ポルトガル語', '0013': 'ドイツ語', '0014': 'ロシア語', '0015': 'イタリア語', '0016': 'スペイン語',
         '0017': 'インドネシア語', '0018': 'トルコ語', '0019': 'マレー語', '0020': 'ヒンディー語', '0021': 'ネパール語',
         '0022': 'シンハラ語', '9999': 'その他'}
URL = ('https://www.iryou.teikyouseido.mhlw.go.jp/znk-web/juminkanja/S2400/initialize?sc=30-04-1-{lang}&st=30-2&sjk=3'
       '&pref={pref}&kkn=1,2,3,4&page={page}&size=20')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36'

ap = argparse.ArgumentParser()
ap.add_argument('out'); ap.add_argument('--langs', default=','.join(LANGS)); ap.add_argument('--prefs', default=','.join(f'{i:02d}' for i in range(1, 48)))
ap.add_argument('--gap', type=float, default=6.0); ap.add_argument('--window', default=None)
a = ap.parse_args()
d = os.path.join(a.out, 'list'); os.makedirs(d, exist_ok=True)
log = open(os.path.join(a.out, 'list_log.tsv'), 'a')


def in_window():
    if not a.window: return True
    s, e = map(int, a.window.split('-')); h = datetime.datetime.now().hour
    return (s <= h < e) if s < e else (h >= s or h < e)


def get(lang, pref, page):
    p = os.path.join(d, f'{lang}_{pref}_{page}.html.gz')
    if os.path.exists(p): return gzip.open(p).read().decode('utf-8', 'replace'), False
    while not in_window(): time.sleep(300)
    t0 = time.time()
    req = urllib.request.Request(URL.format(lang=lang, pref=pref, page=page), headers={'User-Agent': UA, 'Accept-Language': 'ja'})
    with urllib.request.urlopen(req, timeout=60) as r: body = r.read()
    log.write(f'{datetime.datetime.now().isoformat(timespec="seconds")}\t{lang}\t{pref}\t{page}\t{len(body)}\t{time.time()-t0:.1f}\n'); log.flush()
    with gzip.open(p + '.tmp', 'wb') as g: g.write(body)
    os.rename(p + '.tmp', p)
    return body.decode('utf-8', 'replace'), True


def total_of(t):
    m = re.search(r'([\d,]+)\s*件中', t)
    return int(m.group(1).replace(',', '')) if m else 0


ids = {}
for lang in a.langs.split(','):
    for pref in a.prefs.split(','):
        page = 1
        while True:
            t, fetched = get(lang, pref, page)
            for pc, cd, kbn in set(re.findall(r'S2430/initialize\?prefCd=(\d\d)&(?:amp;)?kikanCd=([A-Z0-9]+)&(?:amp;)?kikanKbn=(\d)', t)):
                i = pc + kbn + cd
                ids.setdefault(i, dict(pref=pc, kbn=kbn, kikanCd=cd, id=i, langs=[]))
                if LANGS[lang] not in ids[i]['langs']: ids[i]['langs'].append(LANGS[lang])
            if fetched: time.sleep(a.gap)
            if page * 20 >= total_of(t) or page > 400: break
            page += 1
json.dump(list(ids.values()), open(os.path.join(a.out, 'list_ids.json'), 'w'), ensure_ascii=False)
print(len(ids), 'facilities')
