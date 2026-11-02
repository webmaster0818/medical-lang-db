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
rsync -a --delete --exclude .git --exclude functions --exclude '__next*.txt' out/ "$DEPLOY/"
cd "$DEPLOY"
git add -A
git commit -qm "${1:-Update}" || { echo "変更なし"; exit 0; }
git push -q origin HEAD:main
git log --oneline -1
