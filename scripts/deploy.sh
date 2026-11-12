#!/bin/bash
# 方式B：ビルド → noindex 全数確認 → deploy リポへ同期 → push
# functions/（問い合わせの受信）は deploy リポにだけあるので、rsync --delete で消さない
set -euo pipefail
cd "$(dirname "$0")/.."
DEPLOY="$(cd ../medical-lang-db-deploy && pwd)"
npm run build
total=$(find out -name '*.html' | wc -l | tr -d ' ')
# ページ数が増えると $(find …) を grep に渡す形は Argument list too long で落ちる（T14 で発生）→ -exec … + で分けて渡す
noidx=$(find out -name '*.html' -exec grep -l 'name="robots" content="noindex' {} + | wc -l | tr -d ' ')
echo "noindex $noidx / $total"
if [ "$noidx" != "$total" ]; then echo "noindex が無いページがあります。止めます"; exit 1; fi
# index.txt（画面遷移用のデータ）は送らない。CF Pages は1デプロイ2万ファイルまでで、23区で超えた（2026-11-03）。無くても通常のページ読み込みになるだけ
# 注意：--delete-excluded は P フィルタがあっても .git と functions/ を消す（11/3 の試行で確認）。使わない
rsync -a --delete --exclude .git --exclude functions --exclude '__next*.txt' --exclude 'index.txt' out/ "$DEPLOY/"
# 前回までに送った index.txt は除外ルールのせいで rsync では消えないので、ここで消す（.git の中は触らない）
find "$DEPLOY" -path "$DEPLOY/.git" -prune -o -type f -name index.txt -print -delete | wc -l | xargs echo "index.txt removed:"
# 2026-11-12 分割配置：Workers Paid（11/6）後も 20,777 ファイルの T14 から本体ビルドが失敗し続けた（ログは MediaXAI 口座のみ）。
#   ページを本体＋分割先（tomomi の CF 口座の medilingo-s1, s2 …・pages.dev）に分け、どれも LIMIT 以下に保つ。
#   本体の functions/[[path]].js が同じ式（crc32 % N）で分割先から取って返す。詳細は scripts/shard.py
SHARDS="$(cd .. && pwd)/medical-lang-db-shards"
N=$(python3 scripts/shard.py "$DEPLOY" "$SHARDS")
CF_TOKEN=$(cat "$HOME/.openclaw/workspace/secrets/cf-pages-token.txt"); CF_ACC=$(cat "$HOME/.openclaw/workspace/secrets/cf-account-id.txt")
for ((s=1; s<N; s++)); do
  proj="medilingo-s$s"
  code=$(curl -s -o /dev/null -w '%{http_code}' -H "Authorization: Bearer $CF_TOKEN" "https://api.cloudflare.com/client/v4/accounts/$CF_ACC/pages/projects/$proj")
  if [ "$code" = "404" ]; then
    curl -s -X POST -H "Authorization: Bearer $CF_TOKEN" -H "Content-Type: application/json" \
      -d "{\"name\":\"$proj\",\"production_branch\":\"main\"}" "https://api.cloudflare.com/client/v4/accounts/$CF_ACC/pages/projects" | grep -q '"success":true' || { echo "$proj を作れませんでした"; exit 1; }
  fi
  # wrangler はリポの外（分割先ディレクトリ）から実行する。Next.js リポ内で動かすと設定を書き換える（memory: wrangler-project-create-rewrites-nextjs）
  (cd "$SHARDS/s$s" && CLOUDFLARE_API_TOKEN="$CF_TOKEN" CLOUDFLARE_ACCOUNT_ID="$CF_ACC" npx -y wrangler@3 pages deploy . --project-name "$proj" --branch main --commit-dirty=true) | tail -3
  m=$(find "$SHARDS/s$s" -type f | wc -l | tr -d ' ')
  echo "shard s$s: $m files"
  if [ "$m" -gt 19000 ]; then echo "分割先 s$s が2万に近いので止めます（shard.py の LIMIT を下げる）"; exit 1; fi
done
n=$(find "$DEPLOY" -path "$DEPLOY/.git" -prune -o -type f -print | wc -l | tr -d ' ')
echo "main files $n (shards $N)"
if [ "$n" -gt 19000 ]; then echo "本体が2万に近いので止めます（shard.py の LIMIT を下げる）"; exit 1; fi
cd "$DEPLOY"
git add -A
git commit -qm "${1:-Update}" || { echo "変更なし"; exit 0; }
git push -q origin HEAD:main
git log --oneline -1
