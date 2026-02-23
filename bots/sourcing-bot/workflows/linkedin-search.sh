#!/bin/bash
# linkedin-search.sh - LinkedIn 公開搜尋
# 功能：從 LinkedIn 搜尋候選人（不需要付費帳號）
# 版本：v1.0.0
# 最後更新：2026-02-23

set -e

# 參數
JOB_TITLE="${1:-Engineer}"
KEYWORDS="${2:-}"
LOCATION="${3:-Taiwan}"
LIMIT="${4:-15}"

# 配置
PROJECT_ROOT="/Users/user/clawd/projects/step1ne-headhunter-skill"
SEARCH_SCRIPT="${PROJECT_ROOT}/tools/google-linkedin-search.sh"

# 檢查依賴
if [ ! -f "$SEARCH_SCRIPT" ]; then
  echo "錯誤：找不到 LinkedIn 搜尋腳本" >&2
  echo "路徑：$SEARCH_SCRIPT" >&2
  exit 1
fi

# 構建搜尋關鍵字
SEARCH_QUERY="$JOB_TITLE"
if [ -n "$KEYWORDS" ]; then
  SEARCH_QUERY="$SEARCH_QUERY $KEYWORDS"
fi

# 執行搜尋
bash "$SEARCH_SCRIPT" \
  --query "$SEARCH_QUERY" \
  --location "$LOCATION" \
  --limit "$LIMIT" \
  --output json

# 如果上述腳本不存在，使用備用的 Python 腳本
if [ $? -ne 0 ]; then
  PYTHON_SCRIPT="${PROJECT_ROOT}/modules/linkedin-search/scraper-linkedin-public.py"
  if [ -f "$PYTHON_SCRIPT" ]; then
    python3 "$PYTHON_SCRIPT" \
      --query "$SEARCH_QUERY" \
      --location "$LOCATION" \
      --limit "$LIMIT"
  else
    # 最後的備用方案：返回空結果
    echo "[]"
  fi
fi
