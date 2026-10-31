#!/usr/bin/env python3
"""医療情報ネット（parse.py の出力）と D-5 を突き合わせ、施設×言語の tier（◎○△―）を付けて出力する。
使い方: build.py <out_dir> <d5.xlsx> <d5_sheet> <addr_kw>
出力: <out_dir>/merged_facility.json, merged_facility_language.json, match_d5.json, stats.json, facilities.csv
"""
import json, sys, os, re, csv, collections
sys.path.insert(0, os.path.dirname(__file__))
import d5 as D5

OVERCLAIM_N = 4  # 「受入可能」を4言語以上に付け、翻訳機ありの施設は、人の対応の裏付けがない言語を△に下げる（判定ルール R3）
HUMAN_KW = re.compile(r'通訳|スタッフ|ネイティブ|医師|看護師|職員|話せ')
SITE_LANG = {  # サイトの言語版 ← 話す言語。中国語の2版は、北京語(zh)を両方に、台湾語・広東語を繁体字版に出す
    'en': ['en'], 'ko': ['ko'], 'zh-hans': ['zh'], 'zh-hant': ['zh', 'zh-tw', 'yue'], 'vi': ['vi'], 'pt': ['pt']}
TIER_ORDER = {'◎': 0, '○': 1, '△': 2, '―': 3}
D5_SOURCE = dict(  # D-5 の版（2026-10-30 確認）
    title='外国人患者を受け入れる医療機関の情報を取りまとめたリスト（厚生労働省・観光庁）',
    page='https://www.mhlw.go.jp/stf/newpage_05774.html', file='https://www.mhlw.go.jp/content/10800000/001753496.xlsx',
    published='2026-06-30', last_partial_update='2026-09-30（一部変更：北海道・京都府・広島県）。東京都は2026-08-06の一部変更に含まれる',
    file_last_modified='2026-09-30T01:00:44Z', downloaded='2026-10-29', size_bytes=1935477)


def readjsonl(p):
    return [json.loads(l) for l in open(p)]


def match(F, D):
    by_tel = collections.defaultdict(list); by_name = collections.defaultdict(list)
    for f in F:
        for t in (f.get('phone'), ):
            if t: by_tel[D5.norm_tel(t)].append(f)
        by_name[D5.norm_name(f['name_ja'])].append(f)
    res = []
    for d in D:
        nt, nn = D5.norm_tel(d['tel']), D5.norm_name(d['d5_name'])
        cand_t = by_tel.get(nt, []); cand_n = by_name.get(nn, [])
        both = [f for f in cand_t if f in cand_n]
        if both: m, how = both[0], 'name+tel'
        elif len(cand_n) == 1: m, how = cand_n[0], 'name'
        elif len(cand_t) == 1: m, how = cand_t[0], 'tel'
        else:
            # 名称の部分一致（法人名の付け外しの違い）＋住所の番地一致
            part = [f for f in F if (nn and (nn in D5.norm_name(f['name_ja']) or D5.norm_name(f['name_ja']) in nn))]
            m, how = (part[0], 'name-partial') if len(part) == 1 else (None, None)
        res.append(dict(d5=d, facility_id=m['id'] if m else None, how=how))
    return res


def tier_for(fac, nl, d, lang):
    """1施設×1言語の tier と根拠。nl=医療情報ネットの言語行（無ければ None）、d=D-5 の行（無ければ None）"""
    basis = []
    meth = (d or {}).get('methods', {})
    def d_has(key):
        m = meth.get(key)
        return bool(m) and lang in m['langs']
    # 人の欄（通訳者・コーディネーター・専門部署）でも、本文がタブレット・電話通訳・提携の通訳サービスなら遠隔通訳として扱う
    # 専門部署の有無は、その言語を話せるかの裏付けにしない。コーディネーターは言語が明記された場合だけ数える
    # v2（tomomi-2 指摘4）：人の欄でも翻訳機の記述（device_all）なら人の対応にしない（△・出典D5）
    human_ok = lambda k: d_has(k) and not meth[k]['remote'] and not meth[k]['device_all'] and (k == 'interpreter' or meth[k]['langs_explicit'])
    d_human = human_ok('interpreter') or human_ok('coordinator')
    # v2（tomomi-2 指摘1・4）：遠隔通訳は「人の遠隔通訳と明確な語」があれば翻訳機の記述と並んでいても○。それ以外は翻訳機の記述（device_all）がない場合だけ。
    # 「その他」欄は、人の遠隔通訳と明確な語がある場合だけ数える
    rem = lambda k: d_has(k) and (meth[k]['remote_strong'] or (meth[k]['remote'] and not meth[k]['device_all']))
    # 遠隔通訳の欄そのものは、本文が言語と時間だけでも遠隔通訳（従来どおり）。翻訳機だけが書かれている場合を除く
    rem_col = d_has('remote') and (meth['remote']['remote_strong'] or not meth['remote']['device_all'])
    d_remote = any(rem(k) for k in ('interpreter', 'coordinator', 'dept')) or rem_col or (d_has('other') and meth['other']['remote_strong'])
    # 2026-10-31：翻訳機の記述は D-5 の全ての欄から拾い、判定語も増やした（device_all）。遠隔通訳・人の対応の判定は従来の語のまま
    d_device = any(meth.get(k, {}).get('device_all') and lang in meth[k]['langs'] for k in ('dept', 'coordinator', 'interpreter', 'remote', 'other'))
    # 2026-10-31：「対話可能な医師による対応：EN」のように、医師がその言語で対応すると書かれた言語は人の対応として◎
    d_doctor = any(lang in m.get('doctor_langs', []) for m in meth.values())
    d_listed = bool(d) and lang in d['langs']
    n_status = (nl or {}).get('status')
    n_device = fac.get('translation_device') == '可能' if fac else False
    accepted_n = fac.get('_accepted_n', 0) if fac else 0
    note = ' '.join(filter(None, [(nl or {}).get('note'), (nl or {}).get('phone_note'), (fac or {}).get('foreign_support_note')]))
    # 自由記述に、その言語名と人の対応（通訳・スタッフ等）が両方書かれている場合だけ「人の対応の記載」とみなす
    n_human_note = bool(HUMAN_KW.search(note)) and lang in D5.langs_in(note) and not re.search(r'翻訳機|タブレット|電話通訳|遠隔', note)
    n_lang_detail = bool(nl and (nl.get('phone_foreign') or nl.get('hours') or nl.get('days')))

    if d_human: basis.append('D5:医療通訳者/コーディネーター'); return '◎', basis
    if d_doctor: basis.append('D5:その言語で対応する医師'); return '◎', basis
    if n_status == 'accepted':
        overclaim = accepted_n >= OVERCLAIM_N and n_device
        if not overclaim:
            basis.append('ナビイ:受入可能'); return '◎', basis
        if n_human_note:
            basis.append('ナビイ:受入可能＋人の対応の記載'); return '◎', basis
        basis.append(f'ナビイ:受入可能だが{accepted_n}言語に付け翻訳機あり')
    if d_listed and not meth:
        basis.append('D5:対応外国語に掲載（方法の記載なし）'); return '◎', basis
    if d_remote: basis.append('D5:遠隔通訳'); return '○', basis
    if n_status == 'accepted':  # 多言語に付けた受入可能
        return '△', basis + ['翻訳機前提とみなす']
    if n_device or d_device:
        basis.append('翻訳機あり（' + '・'.join(x for x, ok in (('ナビイ', n_device), ('D5', d_device)) if ok) + '）'); return '△', basis
    basis.append('記載のみ'); return '―', basis


def main():
    out, xlsx, sheet, kw = sys.argv[1:5]
    F = readjsonl(os.path.join(out, 'facility.jsonl'))
    L = readjsonl(os.path.join(out, 'facility_language.jsonl'))
    D = D5.load(xlsx, sheet, kw)
    byF = {f['id']: f for f in F}
    nlang = collections.defaultdict(dict)
    for x in L: nlang[x['facility_id']][x['lang']] = x
    for f in F: f['_accepted_n'] = sum(1 for x in nlang[f['id']].values() if x['status'] == 'accepted')

    M = match(F, D)
    d_by_f = {m['facility_id']: m['d5'] for m in M if m['facility_id']}
    d5_only = []
    for m in M:  # D-5 内の重複（同じ電話番号の別表記。例：Ａｏｉ歯科医院／アオイ歯科医院）は1件にまとめる
        if m['facility_id']: continue
        d = m['d5']; key = D5.norm_tel(d['tel'])  # 住所は表記ゆれが大きい（「4-15-21」と「4丁目１５－２１」）ため電話番号で判定
        dup = next((x for x in d5_only if x['_key'] == key), None)
        if dup:
            dup.setdefault('aliases', []).append(d['d5_name']); continue
        d['_key'] = key; d5_only.append(d)

    rows = []
    keys = set()
    for fid, f in byF.items():
        langs = set(nlang[fid]) | set((d_by_f.get(fid) or {}).get('langs', []))
        for lg in sorted(langs):
            nl = nlang[fid].get(lg); d = d_by_f.get(fid)
            t, b = tier_for(f, nl, d, lg)
            rows.append(dict(facility_id=fid, lang=lg, tier=t, basis=b,
                             status=(nl or {}).get('status'), booking=(nl or {}).get('booking'),
                             phone_foreign=(nl or {}).get('phone_foreign'), days=(nl or {}).get('days'), hours=(nl or {}).get('hours'),
                             depts_kbn=(nl or {}).get('depts_kbn'), depts=(nl or {}).get('depts'), note=(nl or {}).get('note'),
                             source='both' if (nl and d and lg in d['langs']) else ('mhlw' if nl else 'd5')))
    # D-5 にだけある施設（医療情報ネット側に無い）も行として残す
    for d in d5_only:
        for lg in d['langs']:
            t, b = tier_for(None, None, d, lg)
            rows.append(dict(facility_id='d5:' + D5.norm_tel(d['tel']), name=d['d5_name'], aliases=d.get('aliases', []), address=d['address'],
                             tel=d['tel'], lang=lg, tier=t, basis=b, source='d5', page='一覧のみ（厚労省リストのみ）',
                             translation_device_sources=['d5'] if any(m.get('device_all') for m in d['methods'].values()) else []))

    # 施設側に D-5 の情報を足す
    for fid, f in byF.items():
        d = d_by_f.get(fid)
        d_dev = [dict(field=k, text=m['text']) for k, m in ((d or {}).get('methods') or {}).items() if m.get('device_all')]
        f['translation_device_sources'] = [x for x, ok in (('mhlw', f.get('translation_device') == '可能'), ('d5', bool(d_dev))) if ok]
        f['translation_device_d5'] = d_dev or None
        f['d5'] = None if not d else dict(name=d['d5_name'], name_en=d['d5_name_en'], cards=d['cards'], h24=d['h24'], jmip=d['jmip'],
                                          category=d['category'], emergency=d['emergency'], hours=d['hours'])
        f['langs_tier'] = {r['lang']: r['tier'] for r in rows if r['facility_id'] == fid}
        f.pop('_accepted_n', None)

    json.dump(list(byF.values()), open(os.path.join(out, 'merged_facility.json'), 'w'), ensure_ascii=False, indent=1)
    json.dump(rows, open(os.path.join(out, 'merged_facility_language.json'), 'w'), ensure_ascii=False, indent=1)
    json.dump([dict(d5_name=m['d5']['d5_name'], tel=m['d5']['tel'], facility_id=m['facility_id'], how=m['how'],
                    mhlw_name=byF[m['facility_id']]['name_ja'] if m['facility_id'] else None) for m in M],
              open(os.path.join(out, 'match_d5.json'), 'w'), ensure_ascii=False, indent=1)

    # 集計
    fl_langs = {fid for fid, v in nlang.items() if v}
    st = dict(
        facilities=len(F), by_kind=collections.Counter(f['kikan_kbn'] for f in F),
        with_foreign_lang_mhlw=len(fl_langs),
        d5_source=D5_SOURCE,
        d5_rows=len(D), d5_matched=sum(1 for m in M if m['facility_id']), d5_only=[dict(name=d['d5_name'], aliases=d.get('aliases', []), tel=d['tel']) for d in d5_only],
        match_how=collections.Counter(m['how'] for m in M if m['how']),
        mhlw_only=len(fl_langs - set(d_by_f)), both=len(fl_langs & set(d_by_f)),
        d5_matched_but_no_mhlw_lang=[byF[f]['name_ja'] for f in d_by_f if f not in fl_langs],
    )
    tl = collections.defaultdict(collections.Counter)
    for r in rows: tl[r['lang']][r['tier']] += 1
    st['tier_by_spoken_lang'] = {k: dict(v) for k, v in sorted(tl.items(), key=lambda x: -sum(x[1].values()))}
    site = {}
    for sl, spoken in SITE_LANG.items():
        best = {}
        for r in rows:
            if r['lang'] in spoken:
                cur = best.get(r['facility_id'])
                if cur is None or TIER_ORDER[r['tier']] < TIER_ORDER[cur]: best[r['facility_id']] = r['tier']
        site[sl] = dict(collections.Counter(best.values()))
    st['tier_by_site_lang'] = site
    json.dump(st, open(os.path.join(out, 'stats.json'), 'w'), ensure_ascii=False, indent=1)

    with open(os.path.join(out, 'facilities.csv'), 'w', newline='') as fp:
        w = csv.writer(fp)
        w.writerow(['id', '種別', '名称', '英語名', '住所', '電話', '最終更新日', '翻訳機', 'D5掲載', 'JMIP', '拠点',
                    'en', 'ko', 'zh', 'zh-tw', 'yue', 'vi', 'pt', 'その他の言語'])
        for f in byF.values():
            lt = f['langs_tier']
            w.writerow([f['id'], f['kikan_kbn'], f['name_ja'], f['name_en'], f['address_ja'], f['phone'], f['source_mhlw_updated'],
                        f['translation_device'], '○' if f['d5'] else '', '○' if f['jmip'] else '', '○' if f['hub_selected'] else '',
                        *[lt.get(k, '') for k in ('en', 'ko', 'zh', 'zh-tw', 'yue', 'vi', 'pt')],
                        ' '.join(f'{k}{v}' for k, v in lt.items() if k not in ('en', 'ko', 'zh', 'zh-tw', 'yue', 'vi', 'pt'))])
    print(json.dumps({k: v for k, v in st.items() if k not in ('tier_by_spoken_lang',)}, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
