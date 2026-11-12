#!/usr/bin/env python3
"""deploy リポのページを「本体＋分割先プロジェクト」に振り分ける（2026-11-12）。

なぜ：CF Pages は1デプロイあたりのファイル数に上限があり、T14（20,777ファイル）から本体のビルドが
失敗し続けた（11/6〜。Workers Paid に切り替えた後も失敗。ログは MediaXAI の口座にしか無い）。
施設を全国に広げると約9万ページになるので、ページを複数の Pages プロジェクトに分けて置き、
本体の Pages Function（functions/[[path]].js）が該当する分割先から取ってきて返す。

振り分け：言語ディレクトリ配下の HTML を、ファイルパスの crc32 % N で決める。0 は本体に残す。
  JS 側（functions/[[path]].js）も同じ式で決めるので、両方を必ずこのスクリプトから生成する。
  N は本体・分割先とも 1 つあたり LIMIT ファイル以下になるように決める。

使い方：python3 scripts/shard.py <deployディレクトリ> <分割先の出力ディレクトリ>
出力：分割先ディレクトリに s1/ s2/ … を作り、最後の行に N を出す（deploy.sh が読む）
"""
import math
import os
import shutil
import sys
import zlib

LIMIT = 15000          # 1プロジェクトあたりの目安（上限2万に余裕を残す）
PREFIX = "medilingo-s"  # 分割先の Pages プロジェクト名（tomomi の CF 口座・pages.dev）

deploy, outdir = sys.argv[1], sys.argv[2]
langs = sorted(d for d in os.listdir(deploy)
               if os.path.isdir(os.path.join(deploy, d)) and not d.startswith(("_", ".")) and d not in ("functions", "404"))

pages = []
for lang in langs:
    for root, _, files in os.walk(os.path.join(deploy, lang)):
        for f in files:
            if f.endswith(".html"):
                pages.append(os.path.relpath(os.path.join(root, f), deploy))

total = sum(len(fs) for r, _, fs in os.walk(deploy) if "/.git" not in r + "/")
n = max(1, math.ceil(total / LIMIT))

if os.path.isdir(outdir):
    shutil.rmtree(outdir)
os.makedirs(outdir)
moved = [0] * n
for rel in pages:
    s = zlib.crc32(rel.encode()) % n
    if s == 0:
        continue
    dst = os.path.join(outdir, f"s{s}", rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.move(os.path.join(deploy, rel), dst)
    moved[s] += 1

# 分割先を直接開かれても検索に載らないように（本体の Function はこのヘッダーを外して返す）
for s in range(1, n):
    os.makedirs(os.path.join(outdir, f"s{s}"), exist_ok=True)
    with open(os.path.join(outdir, f"s{s}", "_headers"), "w") as fh:
        fh.write("/*\n  X-Robots-Tag: noindex\n")

fn_dir = os.path.join(deploy, "functions")
os.makedirs(fn_dir, exist_ok=True)
with open(os.path.join(fn_dir, "[[path]].js"), "w") as fh:
    fh.write(f"""// 生成ファイル：scripts/shard.py が毎回書き出す。手で直さない（振り分けの式が deploy 側とずれる）
const N = {n};
const HOST = (s) => `https://{PREFIX}${{s}}.pages.dev`;
const T = (() => {{ const t = []; for (let i = 0; i < 256; i++) {{ let c = i; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t.push(c >>> 0); }} return t; }})();
function crc32(str) {{ const b = new TextEncoder().encode(str); let c = 0xffffffff; for (const x of b) c = T[(c ^ x) & 0xff] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; }}
export async function onRequest(ctx) {{
  const url = new URL(ctx.request.url);
  let p = decodeURIComponent(url.pathname);
  if (N <= 1 || p.startsWith("/_next/") || p.startsWith("/api/")) return ctx.next();
  const last = p.split("/").pop();
  const isFile = last.includes(".");
  const key = (p.endsWith("/") ? p + "index.html" : isFile ? p : p + "/index.html").slice(1);
  if (!key.endsWith(".html")) return ctx.next();
  const s = crc32(key) % N;
  if (s === 0) return ctx.next();
  if (!p.endsWith("/") && !isFile) return Response.redirect(url.origin + url.pathname + "/" + url.search, 308);
  const r = await fetch(HOST(s) + url.pathname + url.search, {{ headers: {{ accept: ctx.request.headers.get("accept") || "text/html" }} }});
  if (r.status === 404) return ctx.next();
  const h = new Headers(r.headers);
  h.delete("x-robots-tag");
  return new Response(r.body, {{ status: r.status, headers: h }});
}}
""")
import json
with open(os.path.join(deploy, "_routes.json"), "w") as fh:
    json.dump({"version": 1, "include": [f"/{l}/*" for l in langs] + ["/api/*"], "exclude": ["/_next/*"]}, fh)

print(f"total files {total} / shards {n} / moved {moved[1:]} / main pages {len(pages) - sum(moved)}", file=sys.stderr)
print(n)
