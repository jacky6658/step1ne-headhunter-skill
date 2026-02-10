#!/bin/bash
# 簡化版 104 爬蟲（純 bash）

KEYWORD="${1:-後端工程師}"
LIMIT="${2:-5}"

echo "🔍 搜尋: $KEYWORD (限制 $LIMIT 筆)" >&2

# 開啟搜尋頁面
agent-browser open "https://www.104.com.tw/jobs/search/?keyword=$KEYWORD" >&2
agent-browser wait --load networkidle >&2

# 提取職缺連結和標題（輸出JSON）
agent-browser eval "Array.from(document.querySelectorAll('a[href*=\"/job/\"]')).slice(0, $LIMIT).map(a => ({url: a.href, title: a.textContent.trim()})).filter(j => j.title.length > 5)"

agent-browser close >&2
