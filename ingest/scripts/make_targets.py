#!/usr/bin/env python3
"""医療情報ネットのオープンデータCSV（施設票）から、取得対象の一覧を作る。
ID(13桁) = 都道府県コード(2) + 機関区分(1) + kikanCd(10)。詳細URLは S2430/initialize?kikanCd=..&kikanKbn=..&prefCd=..
使い方: make_targets.py <csv_dir> <out.json> [pref_code] [city_code]
"""
import csv, json, sys, os
FILES = ['01-1_hospital_facility_info_20260601.csv', '02-1_clinic_facility_info_20260601.csv', '03-1_dental_facility_info_20260601.csv']
src, out = sys.argv[1], sys.argv[2]
pref = sys.argv[3] if len(sys.argv) > 3 else None
city = sys.argv[4] if len(sys.argv) > 4 else None
rows = []
for f in FILES:
    for r in csv.DictReader(open(os.path.join(src, f), encoding='utf-8-sig')):
        if pref and r['都道府県コード'] != pref: continue
        if city and r['市区町村コード'] != city: continue
        i = r['ID']
        assert len(i) == 13 and i[:2] == r['都道府県コード'] and i[2] == r['機関区分'], i
        rows.append(dict(id=i, pref=i[:2], kbn=i[2], kikanCd=i[3:], name=r['正式名称'],
                         city_code=r['都道府県コード'] + r['市区町村コード'], csv=f.split('_2026')[0]))
json.dump(rows, open(out, 'w'), ensure_ascii=False, indent=0)
print(len(rows), 'targets ->', out)
