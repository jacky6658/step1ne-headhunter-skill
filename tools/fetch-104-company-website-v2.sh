#!/bin/bash
# 從 104 公司頁面抓取官網 v2

SHEET_ID="1bkI7_cCh_Bs4qVa3HlXiy0CFzmItZlA-DYGHSPS4InE"
ACCOUNT="aijessie88@step1ne.com"

# 讀取公司名單（含現有的 104 公司頁面欄位）
data=$(gog sheets get "$SHEET_ID" "A2:F17" --account "$ACCOUNT" --json)

row=2
echo "$data" | jq -r '.values[] | @json' | while read -r line; do
    company=$(echo "$line" | jq -r '.[0]')
    col_e=$(echo "$line" | jq -r '.[4]')  # 第5欄（104公司頁面）
    
    echo "[$row] $company"
    
    # 如果第5欄已經有 104 公司頁面連結，直接用它
    if [[ "$col_e" =~ ^https://www\.104\.com\.tw/company/ ]]; then
        company_url="$col_e"
        echo "  → 使用現有連結: $company_url"
    else
        # 否則搜尋
        echo "  → 搜尋中..."
        agent-browser open "https://www.104.com.tw/company/search/?keyword=${company}" 2>/dev/null
        agent-browser wait --load networkidle --timeout 10000 2>/dev/null
        
        # 找到包含公司名稱的連結
        company_url=$(agent-browser eval "
            Array.from(document.querySelectorAll('a[href*=\"/company/\"]'))
                .find(a => a.textContent.includes('$company'))?.href || null
        " 2>/dev/null | tr -d '"')
    fi
    
    if [ -z "$company_url" ] || [ "$company_url" = "null" ]; then
        echo "  ✗ 找不到公司頁面"
        continue
    fi
    
    # 進入公司頁面
    agent-browser open "$company_url" 2>/dev/null
    agent-browser wait --load networkidle --timeout 10000 2>/dev/null
    
    # 抓取公司網址
    website=$(agent-browser eval "
        const rows = Array.from(document.querySelectorAll('tr, div'));
        for (const row of rows) {
            const text = row.textContent;
            if (text.includes('公司網址') || text.includes('公司網站')) {
                const link = row.querySelector('a[href^=\"http\"]');
                if (link) return link.href;
            }
        }
        return null;
    " 2>/dev/null | tr -d '"')
    
    if [ -z "$website" ] || [ "$website" = "null" ]; then
        echo "  ✗ 找不到官網"
        website="暫不提供"
    else
        echo "  ✓ $website"
    fi
    
    # 更新到 Sheet D 欄
    gog sheets update "$SHEET_ID" "D$row" "$website" --account "$ACCOUNT" >/dev/null 2>&1
    
    sleep 2
done

agent-browser close 2>/dev/null
echo "✅ 完成"
