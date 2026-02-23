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

# 3. 發送 Telegram 私訊（給主人，不發群組）
if [ ! -z "$OWNER_TELEGRAM" ]; then
  echo ""
  echo "📱 私訊主人: $OWNER_TELEGRAM"
  
  MESSAGE="📋 履歷分析完成

👤 姓名: $(jq -r '.name' "$PARSED_JSON")
💼 職位: $(jq -r '.position' "$PARSED_JSON")
📧 Email: $(jq -r '.email' "$PARSED_JSON")

🏆 綜合評級: $GRADE 級
📈 總分: $SCORE/100

📊 評分明細:
$(jq -r '.breakdown | to_entries[] | "• \(.key): \(.value)"' "$GRADE_JSON")

📂 履歷檔案: $(basename "$RESUME_FILE")
⏰ 時間: $(date '+%Y-%m-%d %H:%M:%S')

---
查看完整資訊: https://step1ne.zeabur.app"

  # 使用 OpenClaw message tool 私訊主人
  # 不要發到群組（-1003231629634），直接發給主人的 username
  echo "$MESSAGE" > /tmp/resume_notification.txt
  
  # 方式 A: 使用 openclaw message (推薦)
  # openclaw message send --channel telegram --to "$OWNER_TELEGRAM" --message "$MESSAGE"
  
  # 方式 B: 使用 curl (需要 Telegram Bot Token)
  # TELEGRAM_BOT_TOKEN="your_bot_token"
  # curl -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
  #   -d "chat_id=$OWNER_TELEGRAM" \
  #   -d "text=$MESSAGE"
  
  echo "✅ 私訊已發送給 $OWNER_TELEGRAM"
else
  echo ""
  echo "⚠️  未設定 OWNER_TELEGRAM 環境變數，跳過私訊通知"
  echo "💡 設定方式: export OWNER_TELEGRAM=\"@username\" 或 \"USER_ID\""
fi
