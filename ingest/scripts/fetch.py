#!/usr/bin/env python3
"""医療情報ネット 施設詳細ページの取得（1本ずつ・間隔を空ける・再開可能）。
- 取得済み（data/raw/<id>.html.gz が存在）は飛ばすので、止めても同じコマンドで続きから再開できる
- 応答のあと必ず GAP 秒待つ（既定 6 秒）。同時接続は 1 本
- 失敗（HTTP 200 以外・本文に施設名が無い）は data/fetch_log.tsv に記録し、MAX_FAIL 連続で停止
- 夜間だけ動かす場合は --window 22-6 のように指定（範囲外ならその時刻まで待つ）
使い方: fetch.py <targets.json> <raw_dir> [--gap 6] [--window 22-6] [--limit N]
"""
import json, sys, os, time, gzip, urllib.request, argparse, datetime
ap = argparse.ArgumentParser()
ap.add_argument('targets'); ap.add_argument('raw')
ap.add_argument('--gap', type=float, default=6.0)
ap.add_argument('--window', default=None)
ap.add_argument('--limit', type=int, default=0)
ap.add_argument('--max-fail', type=int, default=5)
a = ap.parse_args()
BASE = 'https://www.iryou.teikyouseido.mhlw.go.jp/znk-web/juminkanja/S2430/initialize?kikanCd={kikanCd}&kikanKbn={kbn}&prefCd={pref}'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36'
log = open(os.path.join(os.path.dirname(a.raw.rstrip('/')), 'fetch_log.tsv'), 'a')

def in_window():
    if not a.window: return True
    s, e = map(int, a.window.split('-')); h = datetime.datetime.now().hour
    return (s <= h < e) if s < e else (h >= s or h < e)

T = json.load(open(a.targets)); done = 0; fails = 0
GONE = os.path.join(os.path.dirname(a.raw.rstrip('/')), 'gone.txt')  # 200 だが施設詳細の無いページ（廃止・休止とみられる）
gone = set(open(GONE).read().split()) if os.path.exists(GONE) else set()
for t in T:
    p = os.path.join(a.raw, t['id'] + '.html.gz')
    if os.path.exists(p) or t['id'] in gone: continue
    while not in_window(): time.sleep(300)
    url = BASE.format(**t); t0 = time.time()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'ja'})
        with urllib.request.urlopen(req, timeout=60) as r:
            code = r.status; body = r.read()
    except Exception as ex:
        code = getattr(ex, 'code', 0); body = b''
    dt = time.time() - t0
    ok = code == 200 and len(body) > 50000 and '施設詳細'.encode() in body
    log.write('\t'.join(map(str, [datetime.datetime.now().isoformat(timespec='seconds'), t['id'], code, len(body), f'{dt:.1f}', 'ok' if ok else 'NG'])) + '\n'); log.flush()
    if ok:
        with gzip.open(p + '.tmp', 'wb') as g: g.write(body)
        os.rename(p + '.tmp', p); fails = 0; done += 1
    elif code == 200 and len(body) < 80000 and '施設詳細'.encode() not in body:
        open(GONE, 'a').write(t['id'] + '\n'); gone.add(t['id']); fails = 0   # 掲載が無い施設。失敗に数えない
    else:
        fails += 1
        if fails >= a.max_fail:
            print('連続失敗で停止', t['id'], code); sys.exit(2)
        time.sleep(60)  # 失敗時は長めに待つ
    if a.limit and done >= a.limit: break
    time.sleep(a.gap)
print('done', done)
