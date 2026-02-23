#!/bin/bash
# 履歷解析 + 自動評級整合腳本
# 用途：解析履歷後自動評級

set -e

RESUME_PARSER="/Users/user/clawd/projects/step1nehrai/hr-tools/resume-parser-v2.py"
GRADING_LOGIC="/Users/user/clawd/projects/step1ne-headhunter-skill/modules/talent-grading/grading-logic.py"

# 檢查參數
if [ -z "$1" ]; then
  echo "❌ 用法: $0 <履歷PDF檔案>"
  exit 1
fi

RESUME_FILE="$1"
OUTPUT_DIR="${2:-./output}"
mkdir -p "$OUTPUT_DIR"

echo "📄 開始處理履歷: $RESUME_FILE"
echo ""

# 1. 解析履歷
echo "🔍 步驟 1: 解析履歷資料..."
PARSED_JSON="$OUTPUT_DIR/parsed-$(basename "$RESUME_FILE" .pdf).json"
python3 "$RESUME_PARSER" "$RESUME_FILE" --output "$PARSED_JSON"

if [ ! -f "$PARSED_JSON" ]; then
  echo "❌ 履歷解析失敗"
  exit 1
fi

echo "✅ 履歷解析完成: $PARSED_JSON"
echo ""

# 2. 評級候選人
echo "📊 步驟 2: 評級候選人..."
GRADE_JSON="$OUTPUT_DIR/grade-$(basename "$RESUME_FILE" .pdf).json"
python3 "$GRADING_LOGIC" --resume "$PARSED_JSON" --output "$GRADE_JSON"

if [ ! -f "$GRADE_JSON" ]; then
  echo "❌ 評級失敗"
  exit 1
fi

# 讀取評級結果
GRADE=$(jq -r '.grade' "$GRADE_JSON")
SCORE=$(jq -r '.total_score' "$GRADE_JSON")

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 處理完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "候選人: $(jq -r '.name' "$PARSED_JSON")"
echo "職位: $(jq -r '.position' "$PARSED_JSON")"
echo "Email: $(jq -r '.email' "$PARSED_JSON")"
echo ""
echo "🏆 綜合評級: $GRADE 級"
echo "📈 總分: $SCORE/100"
echo ""
echo "📂 輸出檔案:"
echo "  • 履歷資料: $PARSED_JSON"
echo "  • 評級結果: $GRADE_JSON"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 3. 可選：發送 Telegram 通知
if [ ! -z "$TELEGRAM_CHAT_ID" ]; then
  echo ""
  echo "📱 發送 Telegram 通知..."
  
  MESSAGE="📋 新履歷進件

👤 姓名: $(jq -r '.name' "$PARSED_JSON")
💼 職位: $(jq -r '.position' "$PARSED_JSON")
📧 Email: $(jq -r '.email' "$PARSED_JSON")

🏆 綜合評級: $GRADE 級
📈 總分: $SCORE/100

📊 評分明細:
$(jq -r '.breakdown | to_entries[] | "• \(.key): \(.value)"' "$GRADE_JSON")

⏰ 時間: $(date '+%Y-%m-%d %H:%M:%S')"

  # 使用 OpenClaw message tool 或 curl Telegram API
  # openclaw message send --channel telegram --to "$TELEGRAM_CHAT_ID" --message "$MESSAGE"
fi
