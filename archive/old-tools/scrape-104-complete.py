#!/usr/bin/env python3
"""
104 完整爬蟲：職缺搜尋 + 公司聯絡方式
"""

import subprocess
import json
import sys
import re
from datetime import datetime

def run(cmd):
    """執行指令並返回結果"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def log(msg, file="/tmp/104-complete.log"):
    """寫入日誌"""
    with open(file, 'a', encoding='utf-8') as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def search_jobs(keyword, limit=20):
    """搜尋職缺"""
    log(f"搜尋: {keyword} (限 {limit} 筆)")
    
    # 開啟搜尋頁面
    run(f'agent-browser open "https://www.104.com.tw/jobs/search/?keyword={keyword}"')
    run('agent-browser wait --load networkidle')
    
    # 提取職缺
    js = f"Array.from(document.querySelectorAll('a[href*=\"/job/\"]')).slice(0, {limit}).map(a => ({{url: a.href, title: a.textContent.trim()}})).filter(j => j.title.length > 5)"
    result = run(f"agent-browser eval '{js}'")
    
    try:
        jobs = json.loads(result)
        log(f"✓ 找到 {len(jobs)} 個職缺")
        return jobs
    except:
        log("✗ 解析失敗")
        return []

def get_job_detail(job_url):
    """從職缺頁面取得公司資訊"""
    log(f"訪問職缺: {job_url}")
    
    run(f"agent-browser open '{job_url}'")
    run('agent-browser wait --load networkidle --timeout 5000')
    
    # 提取公司名稱、地點、薪資、公司連結
    js = """
(function(){
  const get = (sel) => {
    const el = document.querySelector(sel);
    return el ? el.textContent.trim() : null;
  };
  const getHref = (sel) => {
    const el = document.querySelector(sel);
    return el ? el.href : null;
  };
  return {
    company: get('a[href*="/company/"]') || get('.company-name'),
    location: get('[data-qa="job-location"]') || get('.job-location'),
    salary: get('[data-qa="job-salary"]') || get('.job-salary'),
    company_url: getHref('a[href*="/company/"]')
  };
})()
"""
    result = run(f"agent-browser eval '{js}'")
    
    try:
        return json.loads(result)
    except:
        log("✗ 無法解析職缺資訊")
        return None

def get_company_contact(company_url):
    """從公司頁面取得聯絡方式"""
    if not company_url:
        return {"phone": None, "email": None, "website": None}
    
    log(f"訪問公司頁面: {company_url}")
    
    run(f"agent-browser open '{company_url}'")
    run('agent-browser wait --load networkidle --timeout 5000')
    
    # 提取電話、Email、官網
    js = """
(function(){
  const text = document.body.textContent;
  const phoneMatch = text.match(/(\\d{2,4}[-\\s]?\\d{3,4}[-\\s]?\\d{3,4})/);
  const emailMatch = text.match(/([\\w\\.-]+@[\\w\\.-]+\\.\\w+)/);
  
  const websiteEl = document.querySelector('a[href*="http"]:not([href*="104.com.tw"])');
  
  return {
    phone: phoneMatch ? phoneMatch[1] : null,
    email: emailMatch ? emailMatch[1] : null,
    website: websiteEl ? websiteEl.href : null
  };
})()
"""
    result = run(f"agent-browser eval '{js}'")
    
    try:
        return json.loads(result)
    except:
        log("✗ 無法解析公司聯絡方式")
        return {"phone": None, "email": None, "website": None}

def main():
    keyword = sys.argv[1] if len(sys.argv) > 1 else "後端工程師"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    
    log("=" * 50)
    log(f"開始搜尋: {keyword}")
    
    # 步驟 1：搜尋職缺
    jobs = search_jobs(keyword, limit)
    
    if not jobs:
        print("[]")
        run('agent-browser close')
        return
    
    # 步驟 2：爬取每個職缺的詳細資訊
    results = []
    
    for idx, job in enumerate(jobs, 1):
        log(f"--- 處理 {idx}/{len(jobs)}: {job['title'][:50]} ---")
        
        # 取得職缺資訊
        detail = get_job_detail(job['url'])
        if not detail:
            continue
        
        # 取得公司聯絡方式
        contact = get_company_contact(detail.get('company_url'))
        
        # 整合結果
        results.append({
            "company": detail.get('company', 'N/A'),
            "job_title": job['title'],
            "location": detail.get('location', 'N/A'),
            "salary": detail.get('salary', 'N/A'),
            "url": job['url'],
            "phone": contact.get('phone') or "待查",
            "email": contact.get('email') or "待查",
            "website": contact.get('website') or "待查"
        })
        
        log(f"✓ 完成: {detail.get('company')} | Phone: {contact.get('phone') or '無'} | Email: {contact.get('email') or '無'}")
    
    run('agent-browser close')
    
    log(f"=" * 50)
    log(f"完成！共 {len(results)} 筆")
    
    # 輸出 JSON
    print(json.dumps(results, ensure_ascii=False, indent=2))
    
    # 備份
    backup = f"/tmp/104-complete-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(backup, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    log(f"備份: {backup}")

if __name__ == "__main__":
    main()
