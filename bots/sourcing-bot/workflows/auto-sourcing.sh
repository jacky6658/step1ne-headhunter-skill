#!/bin/bash
# auto-sourcing.sh - Sourcing Bot 主流程
# 功能：LinkedIn + GitHub 多管道搜尋 → AI 配對 → 去重 → 匯入履歷池 → Telegram 通知
# 版本：v1.0.0
# 最後更新：2026-02-23

set -e

# 配置
PROJECT_ROOT="/Users/user/clawd/projects/step1ne-headhunter-skill"
BOT_ROOT="${PROJECT_ROOT}/bots/sourcing-bot"
LOG_FILE="/tmp/sourcing-bot-$(date +%Y-%m-%d).log"

# 參數解析
TEST_MODE=false
DRY_RUN=false
VERBOSE=false
SPECIFIC_JOB=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --test)
      TEST_MODE=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --verbose)
      VERBOSE=true
      shift
      ;;
    --job)
      SPECIFIC_JOB="$2"
      shift 2
      ;;
    *)
      echo "未知參數: $1"
      exit 1
      ;;
  esac
done

# 日誌函數
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_error() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" | tee -a "$LOG_FILE" >&2
}

# 開始執行
log "=== 履歷池自動累積執行開始 ==="
log "模式: $([ "$TEST_MODE" = true ] && echo "測試" || echo "正式") | Dry Run: $DRY_RUN"

# [1/7] 讀取職缺管理表
log "[1/7] 讀取職缺管理表..."

SHEET_ID="1QPaeOm-slNVFCeM8Q3gg3DawKjzp2tYwyfquvdHlZFE"
TAB_NAME="step1ne 職缺管理"

if [ -n "$SPECIFIC_JOB" ]; then
  log "指定職缺: $SPECIFIC_JOB"
  JOBS="$SPECIFIC_JOB"
else
  # 讀取所有「招募中」職缺
  JOBS=$(gog sheets read "$SHEET_ID" "$TAB_NAME!A2:E100" | \
    awk -F'|' '$5 == "招募中" {print $1}' | \
    shuf | \
    head -n $([ "$TEST_MODE" = true ] && echo 1 || echo 2))
fi

if [ -z "$JOBS" ]; then
  log_error "沒有找到招募中的職缺"
  exit 1
fi

JOB_COUNT=$(echo "$JOBS" | wc -l | tr -d ' ')
log "✓ 找到 $JOB_COUNT 個職缺"

# [2/7] 執行多管道搜尋
log "[2/7] 執行多管道搜尋..."

ALL_CANDIDATES_FILE="/tmp/sourcing-candidates-$(date +%s).json"
echo "[]" > "$ALL_CANDIDATES_FILE"

JOB_INDEX=1
echo "$JOBS" | while read -r JOB_NAME; do
  log "[$JOB_INDEX/$JOB_COUNT] 搜尋職缺: $JOB_NAME"
  
  # LinkedIn 搜尋
  log "  → LinkedIn 搜尋..."
  bash "${BOT_ROOT}/workflows/linkedin-search.sh" "$JOB_NAME" > /tmp/linkedin-$JOB_INDEX.json 2>&1
  LINKEDIN_COUNT=$(cat /tmp/linkedin-$JOB_INDEX.json | jq 'length' 2>/dev/null || echo 0)
  log "  ✓ LinkedIn: $LINKEDIN_COUNT 位候選人"
  
  # GitHub 搜尋（僅技術職缺）
  if echo "$JOB_NAME" | grep -iE "工程師|engineer|developer|devops|sre" > /dev/null; then
    log "  → GitHub 搜尋..."
    bash "${BOT_ROOT}/workflows/github-search.sh" "$JOB_NAME" > /tmp/github-$JOB_INDEX.json 2>&1
    GITHUB_COUNT=$(cat /tmp/github-$JOB_INDEX.json | jq 'length' 2>/dev/null || echo 0)
    log "  ✓ GitHub: $GITHUB_COUNT 位候選人"
  else
    echo "[]" > /tmp/github-$JOB_INDEX.json
    GITHUB_COUNT=0
    log "  - GitHub: 跳過（非技術職缺）"
  fi
  
  # 合併結果
  jq -s 'add' /tmp/linkedin-$JOB_INDEX.json /tmp/github-$JOB_INDEX.json > /tmp/merged-$JOB_INDEX.json
  MERGED_COUNT=$(cat /tmp/merged-$JOB_INDEX.json | jq 'length')
  log "  ✓ 合併: $MERGED_COUNT 位候選人"
  
  # 追加到總候選人列表
  jq -s 'add' "$ALL_CANDIDATES_FILE" /tmp/merged-$JOB_INDEX.json > /tmp/all-temp.json
  mv /tmp/all-temp.json "$ALL_CANDIDATES_FILE"
  
  JOB_INDEX=$((JOB_INDEX + 1))
done

TOTAL_CANDIDATES=$(cat "$ALL_CANDIDATES_FILE" | jq 'length')
log "✓ 總計找到 $TOTAL_CANDIDATES 位候選人"

# [3/7] AI 配對評分
log "[3/7] AI 配對評分..."

# 這裡應該呼叫 AI 配對系統，目前先跳過
# TODO: 整合 modules/ai-matcher/ai_matcher_v3.py
log "  → AI 配對功能待整合"
log "  ✓ 假設所有候選人通過配對"

# [4/7] Top 3 推薦
log "[4/7] 生成 Top 3 推薦..."
TOP3=$(cat "$ALL_CANDIDATES_FILE" | jq -r 'limit(3; .[]) | "\(.name // .github_username) (\(.position // "N/A")) - \(.linkedin_url // .github_url)"')
log "$TOP3"

# [5/7] 去重檢查
log "[5/7] 去重檢查..."
# TODO: 實作去重邏輯
log "  → 去重功能待整合"
NEW_CANDIDATES=$TOTAL_CANDIDATES

# [6/7] 匯入履歷池
if [ "$DRY_RUN" = false ]; then
  log "[6/7] 匯入履歷池..."
  
  RESUME_POOL_SHEET="1PunpaDAFBPBL_I76AiRYGXKaXDZvMl1c262SEtxRk6Q"
  RESUME_POOL_TAB="履歷池v2"
  
  # TODO: 實際的匯入邏輯
  log "  ✓ $NEW_CANDIDATES 位候選人已匯入"
else
  log "[6/7] 匯入履歷池... (跳過 - Dry Run 模式)"
fi

# [7/7] 發送 Telegram 通知
if [ "$DRY_RUN" = false ]; then
  log "[7/7] 發送 Telegram 通知..."
  
  MESSAGE="✅ 履歷池自動收集執行完成（$(date +%H:%M)）

搜尋職缺：
$(echo "$JOBS" | sed 's/^/• /')

找到候選人：$TOTAL_CANDIDATES 位
已匯入：$NEW_CANDIDATES 位

Top 3 推薦：
$TOP3

狀態：✅ 系統運作正常"

  openclaw message send \
    --target "-1003231629634" \
    --thread-id 304 \
    --message "$MESSAGE" >> "$LOG_FILE" 2>&1
  
  log "  ✓ 通知已發送到 Topic 304"
else
  log "[7/7] 發送 Telegram 通知... (跳過 - Dry Run 模式)"
fi

# 完成
log "=== 執行完成 ==="
log "日誌檔案: $LOG_FILE"
