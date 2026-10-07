#!/bin/bash
# export_pdf.sh — 提案 HTML → PDF + 逐页导出图片验收
# 用法: bash scripts/export_pdf.sh <提案.html> [输出名.pdf]
# 依赖: Google Chrome（headless）、poppler（pdftoppm，macOS: brew install poppler）
set -e
HTML="$1"
OUT="${2:-$(dirname "$HTML")/proposal.pdf}"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -x "$CHROME" ] || CHROME="$(command -v google-chrome || command -v chromium || command -v chromium-browser)"
[ -n "$CHROME" ] || { echo "找不到 Chrome"; exit 1; }

"$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$OUT" "file://$(cd "$(dirname "$HTML")" && pwd)/$(basename "$HTML")"

# ⛔ 命令不报错 ≠ 排版没崩 —— 必须逐页看图
CHECK_DIR="$(dirname "$OUT")/pdf-check"
mkdir -p "$CHECK_DIR"
pdftoppm -r 96 -png "$OUT" "$CHECK_DIR/page"
echo "✓ PDF: $OUT"
echo "✓ 逐页验收图: $CHECK_DIR/page-*.png （请逐页打开看一遍）"
