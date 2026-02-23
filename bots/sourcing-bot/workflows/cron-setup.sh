#!/bin/bash
# cron-setup.sh - 自動設定 Sourcing Bot Cron Jobs
# 功能：一鍵設定每天 3 次的自動搜尋
# 版本：v1.0.0
# 最後更新：2026-02-23

set -e

# 配置
BOT_ROOT="/Users/user/clawd/projects/step1ne-headhunter-skill/bots/sourcing-bot"
AUTO_SOURCING_SCRIPT="${BOT_ROOT}/workflows/auto-sourcing.sh"

echo "=== Sourcing Bot Cron 設定 ==="
echo ""

# 檢查腳本是否存在
if [ ! -f "$AUTO_SOURCING_SCRIPT" ]; then
  echo "錯誤：找不到 auto-sourcing.sh"
  echo "路徑：$AUTO_SOURCING_SCRIPT"
  exit 1
fi

# 檢查腳本是否可執行
if [ ! -x "$AUTO_SOURCING_SCRIPT" ]; then
  echo "設定執行權限..."
  chmod +x "$AUTO_SOURCING_SCRIPT"
fi

# 檢查現有 Cron
echo "檢查現有 Cron..."
EXISTING_CRONS=$(openclaw cron list | grep "履歷池自動累積" || true)

if [ -n "$EXISTING_CRONS" ]; then
  echo ""
  echo "發現現有的 Sourcing Bot Cron："
  echo "$EXISTING_CRONS"
  echo ""
  read -p "是否刪除現有 Cron 並重新建立？(y/N) " -n 1 -r
  echo ""
  
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 刪除現有 Cron
    echo "刪除現有 Cron..."
    echo "$EXISTING_CRONS" | awk '{print $1}' | while read -r CRON_ID; do
      openclaw cron delete "$CRON_ID"
      echo "  ✓ 已刪除 $CRON_ID"
    done
  else
    echo "取消操作"
    exit 0
  fi
fi

# 創建新的 Cron Jobs
echo ""
echo "創建新的 Cron Jobs..."

# Cron 1: 早上 09:00
echo "  → 創建早上 09:00 的 Cron..."
CRON1_ID=$(openclaw cron add \
  --label "履歷池自動累積-早上" \
  --schedule "0 9 * * *" \
  --command "bash $AUTO_SOURCING_SCRIPT" \
  | grep -oE '[a-f0-9-]{36}' | head -1)
echo "  ✓ Cron ID: $CRON1_ID"

# Cron 2: 下午 14:00
echo "  → 創建下午 14:00 的 Cron..."
CRON2_ID=$(openclaw cron add \
  --label "履歷池自動累積-下午" \
  --schedule "0 14 * * *" \
  --command "bash $AUTO_SOURCING_SCRIPT" \
  | grep -oE '[a-f0-9-]{36}' | head -1)
echo "  ✓ Cron ID: $CRON2_ID"

# Cron 3: 晚上 20:00
echo "  → 創建晚上 20:00 的 Cron..."
CRON3_ID=$(openclaw cron add \
  --label "履歷池自動累積-晚上" \
  --schedule "0 20 * * *" \
  --command "bash $AUTO_SOURCING_SCRIPT" \
  | grep -oE '[a-f0-9-]{36}' | head -1)
echo "  ✓ Cron ID: $CRON3_ID"

echo ""
echo "=== 設定完成 ==="
echo ""
echo "已創建 3 個 Cron Jobs："
echo "  • 早上 09:00: $CRON1_ID"
echo "  • 下午 14:00: $CRON2_ID"
echo "  • 晚上 20:00: $CRON3_ID"
echo ""
echo "查看 Cron 狀態："
echo "  openclaw cron list | grep '履歷池自動累積'"
echo ""
echo "手動執行測試："
echo "  openclaw cron run $CRON1_ID"
echo ""
