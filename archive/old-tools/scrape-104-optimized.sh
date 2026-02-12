#!/bin/bash
# 104 優化版爬蟲

KEYWORD="${1:-後端工程師}"
LIMIT="${2:-5}"

echo "🔍 搜尋: $KEYWORD (限 $LIMIT 筆)" >&2

# 步驟 1：搜尋職缺
agent-browser open "https://www.104.com.tw/jobs/search/?keyword=$KEYWORD" >&2
agent-browser wait --load networkidle >&2

JOBS=$(agent-browser eval "Array.from(document.querySelectorAll('a[href*=\"/job/\"]')).slice(0, $LIMIT).map(a => ({url: a.href, title: a.textContent.trim()})).filter(j => j.title.length > 5)")

# 處理每個職缺
echo "$JOBS" | jq -c '.[]' | while read -r job; do
    URL=$(echo "$job" | jq -r '.url')
    JOB_TITLE=$(echo "$job" | jq -r '.title')
    
    echo "  📄 $JOB_TITLE" >&2
    
    # 訪問職缺頁面
    agent-browser open "$URL" >&2
    agent-browser wait --load networkidle --timeout 5000 >&2
    
    # 從標題解析：公司｜地點
    TITLE=$(agent-browser eval "document.title" | tr -d '"')
    
    # 用 Python 解析標題（避免 bash 編碼問題）
    COMPANY=$(python3 -c "parts='$TITLE'.split('｜'); print(parts[1] if len(parts) > 1 else 'N/A')" 2>/dev/null || echo "N/A")
    LOCATION=$(python3 -c "parts='$TITLE'.split('｜'); print(parts[2].split('－')[0] if len(parts) > 2 else 'N/A')" 2>/dev/null || echo "N/A")
    
    # 提取薪資（簡化版，避免複雜正則）
    SALARY=$(agent-browser eval "document.body.innerText.split('\\n').find(line => line.includes('月薪') || line.includes('年薪') || line.includes('待遇')) || '面議'" | head -c 80 | sed 's/"//g')
    
    # 提取公司頁面連結
    COMPANY_URL=$(agent-browser eval "document.querySelector('a[href*=\"/company/\"]') ? document.querySelector('a[href*=\"/company/\"]').href : null" | tr -d '"')
    
    PHONE="待查"
    EMAIL="待查"
    WEBSITE="待查"
    
    # 訪問公司頁面
    if [[ -n "$COMPANY_URL" && "$COMPANY_URL" != "null" ]]; then
        echo "    🏢 訪問: $COMPANY" >&2
        agent-browser open "$COMPANY_URL" >&2
        agent-browser wait --load networkidle --timeout 5000 >&2
        
        # 提取聯絡資訊（簡化正則）
        PHONE=$(agent-browser eval "document.body.innerText.match(/[0-9]{2,4}[-\s]?[0-9]{3,4}[-\s]?[0-9]{3,4}/) ? document.body.innerText.match(/[0-9]{2,4}[-\s]?[0-9]{3,4}[-\s]?[0-9]{3,4}/)[0] : null" | tr -d '"')
        [[ "$PHONE" == "null" || -z "$PHONE" ]] && PHONE="待查"
        
        EMAIL=$(agent-browser eval "document.body.innerText.match(/[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/) ? document.body.innerText.match(/[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/)[0] : null" | tr -d '"')
        [[ "$EMAIL" == "null" || -z "$EMAIL" ]] && EMAIL="待查"
        
        # 找官網連結（非 104.com.tw）
        WEBSITE=$(agent-browser eval "Array.from(document.querySelectorAll('a[href]')).find(a => a.href.startsWith('http') && !a.href.includes('104.com.tw') && !a.href.includes('javascript')) ?.href || null" | tr -d '"')
        [[ "$WEBSITE" == "null" || -z "$WEBSITE" ]] && WEBSITE="待查"
        
        echo "    ✓ $COMPANY | $PHONE | $EMAIL" >&2
    fi
    
    # 輸出 JSON
    jq -n \
        --arg company "$COMPANY" \
        --arg job_title "$JOB_TITLE" \
        --arg location "$LOCATION" \
        --arg salary "$SALARY" \
        --arg url "$URL" \
        --arg phone "$PHONE" \
        --arg email "$EMAIL" \
        --arg website "$WEBSITE" \
        '{company: $company, job_title: $job_title, location: $location, salary: $salary, url: $url, phone: $phone, email: $email, website: $website}'
    
done | jq -s '.'

agent-browser close >&2
echo "✅ 完成" >&2
