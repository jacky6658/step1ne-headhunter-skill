#!/bin/bash
# github-search.sh - GitHub 開發者搜尋
# 功能：從 GitHub 搜尋技術人才
# 版本：v1.0.0
# 最後更新：2026-02-23

set -e

# 參數
JOB_TITLE="${1:-Engineer}"
KEYWORDS="${2:-}"
LOCATION="${3:-Taiwan}"
LIMIT="${4:-10}"

# 配置
PROJECT_ROOT="/Users/user/clawd/projects/step1ne-headhunter-skill"
PYTHON_SCRIPT="${PROJECT_ROOT}/skills/headhunter/scripts/github-talent-search.py"

# 檢查 GitHub Token
if [ -z "$GITHUB_TOKEN" ]; then
  echo "警告：GITHUB_TOKEN 未設定，技能推斷可能失敗" >&2
fi

# 檢查依賴
if [ ! -f "$PYTHON_SCRIPT" ]; then
  # 備用路徑
  PYTHON_SCRIPT="${PROJECT_ROOT}/modules/github-talent-search/github-talent-search.py"
  
  if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "錯誤：找不到 GitHub 搜尋腳本" >&2
    echo "路徑：$PYTHON_SCRIPT" >&2
    echo "[]"
    exit 0
  fi
fi

# 構建搜尋關鍵字
SEARCH_QUERY="$JOB_TITLE"
if [ -n "$KEYWORDS" ]; then
  SEARCH_QUERY="$SEARCH_QUERY $KEYWORDS"
fi

# 執行搜尋
python3 "$PYTHON_SCRIPT" \
  --query "$SEARCH_QUERY" \
  --location "$LOCATION" \
  --limit "$LIMIT" \
  2>/dev/null || echo "[]"
