#!/bin/bash
# 104 最終版爬蟲 - 確保能拿到電話和 Email

KEYWORD="${1:-後端工程師}"
LIMIT="${2:-5}"

echo "🔍 搜尋: $KEYWORD (限 $LIMIT 筆)" >&2

# 搜尋職缺
agent-browser open "https://www.104.com.tw/jobs/search/?keyword=$KEYWORD" >&2
agent-browser wait --load networkidle >&2

JOBS=$(agent-browser eval "Array.from(document.querySelectorAll('a[href*=\"/job/\"]')).slice(0, $LIMIT).map(a => ({url: a.href, title: a.textContent.trim()})).filter(j => j.title.length > 5)")

# 處理每個職缺
echo "$JOBS" | jq -c '.[]' | while read -r job; do
    JOB_URL=$(echo "$job" | jq -r '.url')
    JOB_TITLE=$(echo "$job" | jq -r '.title')
    
    echo "  📄 $JOB_TITLE" >&2
    
    # 訪問職缺頁面
    agent-browser open "$JOB_URL" >&2
    agent-browser wait --load networkidle --timeout 5000 >&2
    
    # 從標題解析
    TITLE=$(agent-browser eval "document.title" | tr -d '"')
    COMPANY=$(python3 -c "parts='$TITLE'.split('｜'); print(parts[1] if len(parts) > 1 else 'N/A')" 2>/dev/null || echo "N/A")
    LOCATION=$(python3 -c "parts='$TITLE'.split('｜'); print(parts[2].split('－')[0] if len(parts) > 2 else 'N/A')" 2>/dev/null || echo "N/A")
    
    # 取得公司頁面連結
    COMPANY_URL=$(agent-browser eval "document.querySelector('a[href*=\"/company/\"]') ? document.querySelector('a[href*=\"/company/\"]').href : null" | tr -d '"')
    
    PHONE="待查"
    EMAIL="待查"
    WEBSITE="待查"
    
    # 步驟 1：訪問 104 公司頁面
    if [[ -n "$COMPANY_URL" && "$COMPANY_URL" != "null" ]]; then
        echo "    🏢 104公司頁面: $COMPANY" >&2
        agent-browser open "$COMPANY_URL" >&2
        agent-browser wait --load networkidle --timeout 5000 >&2
        
        # 提取電話
        PHONE=$(agent-browser eval "document.body.innerText.match(/[0-9]{2,4}[-\s]?[0-9]{3,4}[-\s]?[0-9]{3,4}/) ? document.body.innerText.match(/[0-9]{2,4}[-\s]?[0-9]{3,4}[-\s]?[0-9]{3,4}/)[0] : null" | tr -d '"')
        [[ "$PHONE" == "null" || -z "$PHONE" ]] && PHONE="待查"
        
        # 提取 Email（104 通常沒有）
        EMAIL=$(agent-browser eval "document.body.innerText.match(/[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/) ? document.body.innerText.match(/[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/)[0] : null" | tr -d '"')
        [[ "$EMAIL" == "null" || -z "$EMAIL" ]] && EMAIL="待查"
        
        # 找公司官網
        WEBSITE=$(agent-browser eval "Array.from(document.querySelectorAll('a[href]')).find(a => a.href.startsWith('http') && !a.href.includes('104.com.tw') && !a.href.includes('javascript') && !a.href.includes('onelink')) ?.href || null" | tr -d '"')
        [[ "$WEBSITE" == "null" || -z "$WEBSITE" ]] && WEBSITE="待查"
        
        echo "    ├─ Phone: $PHONE" >&2
        echo "    ├─ Email: $EMAIL" >&2
        echo "    └─ Website: $WEBSITE" >&2
    fi
    
    # 步驟 2：如果沒有 Email，去爬公司官網
    if [[ "$EMAIL" == "待查" && "$WEBSITE" != "待查" && "$WEBSITE" != "null" ]]; then
        echo "    🌐 爬取公司官網尋找 Email..." >&2
        
        # 嘗試首頁
        agent-browser open "$WEBSITE" >&2
        agent-browser wait --load networkidle --timeout 5000 >&2
        
        EMAIL_FROM_SITE=$(agent-browser eval "document.body.innerText.match(/[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/) ? document.body.innerText.match(/[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/)[0] : null" | tr -d '"')
        
        if [[ -n "$EMAIL_FROM_SITE" && "$EMAIL_FROM_SITE" != "null" ]]; then
            EMAIL="$EMAIL_FROM_SITE"
            echo "    ✓ 找到 Email: $EMAIL" >&2
        else
            # 嘗試「聯絡我們」頁面
            CONTACT_URL="${WEBSITE%/}/contact"
            agent-browser open "$CONTACT_URL" >&2 2>/dev/null
            agent-browser wait --load networkidle --timeout 3000 >&2 2>/dev/null
            
            EMAIL_FROM_CONTACT=$(agent-browser eval "document.body.innerText.match(/[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/) ? document.body.innerText.match(/[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/)[0] : null" 2>/dev/null | tr -d '"')
            
            if [[ -n "$EMAIL_FROM_CONTACT" && "$EMAIL_FROM_CONTACT" != "null" ]]; then
                EMAIL="$EMAIL_FROM_CONTACT"
                echo "    ✓ 從聯絡頁面找到 Email: $EMAIL" >&2
            else
                echo "    ✗ 官網未找到 Email" >&2
            fi
        fi
    fi
    
    # 輸出 JSON（新格式）
    jq -n \
        --arg company "$COMPANY" \
        --arg phone "$PHONE" \
        --arg email "$EMAIL" \
        --arg website "$WEBSITE" \
        --arg company_url "$COMPANY_URL" \
        --arg job_title "$JOB_TITLE" \
        --arg job_url "$JOB_URL" \
        --arg location "$LOCATION" \
        '{
            company: $company,
            phone: $phone,
            email: $email,
            website: $website,
            company_url: $company_url,
            job_title: $job_title,
            job_url: $job_url,
            location: $location,
            source: "104",
            status: "待聯繫",
            date: (now | strftime("%Y-%m-%d"))
        }'
    
done | jq -s '.'

agent-browser close >&2
echo "✅ 完成" >&2
