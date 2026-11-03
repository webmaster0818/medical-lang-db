#!/bin/bash
# 方式B：ビルド → noindex 全数確認 → deploy リポへ同期 → push
# functions/（問い合わせの受信）は deploy リポにだけあるので、rsync --delete で消さない
set -euo pipefail
cd "$(dirname "$0")/.."
DEPLOY="$(cd ../medical-lang-db-deploy && pwd)"
npm run build
total=$(find out -name '*.html' | wc -l | tr -d ' ')
noidx=$(grep -l 'name="robots" content="noindex' $(find out -name '*.html') | wc -l | tr -d ' ')
echo "noindex $noidx / $total"
if [ "$noidx" != "$total" ]; then echo "noindex が無いページがあります。止めます"; exit 1; fi
# index.txt（画面遷移用のデータ）は送らない。CF Pages は1デプロイ2万ファイルまでで、23区で超えた（2026-11-03）。無くても通常のページ読み込みになるだけ
# 注意：--delete-excluded は P フィルタがあっても .git と functions/ を消す（11/3 の試行で確認）。使わない
rsync -a --delete --exclude .git --exclude functions --exclude '__next*.txt' --exclude 'index.txt' out/ "$DEPLOY/"
# 前回までに送った index.txt は除外ルールのせいで rsync では消えないので、ここで消す（.git の中は触らない）
find "$DEPLOY" -path "$DEPLOY/.git" -prune -o -type f -name index.txt -print -delete | wc -l | xargs echo "index.txt removed:"
n=$(find "$DEPLOY" -path "$DEPLOY/.git" -prune -o -type f -print | wc -l | tr -d ' ')
echo "files $n"
if [ "$n" -gt 19500 ]; then echo "CF Pages の2万ファイル上限に近いので止めます"; exit 1; fi
cd "$DEPLOY"
git add -A
git commit -qm "${1:-Update}" || { echo "変更なし"; exit 0; }
git push -q origin HEAD:main
git log --oneline -1
