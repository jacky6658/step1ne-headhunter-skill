#!/usr/bin/env python3
"""
LinkedIn 公開個人檔案爬蟲
策略：透過 Google 搜尋 LinkedIn 個人檔案 → 爬取公開資訊
"""

import sys
import json
import re
import time
from urllib.parse import quote_plus
import subprocess

def google_search_linkedin(keywords, location="Taiwan", max_results=20):
    """使用 Google 搜尋 LinkedIn 個人檔案"""
    
    # 建立搜尋查詢
    query = f"{keywords} {location} site:linkedin.com/in"
    
    print(f"🔍 Google 搜尋：{query}", file=sys.stderr)
    
    # 使用 Brave Search API（已設定）
    try:
        from web_search import web_search
        results = web_search(query, count=min(max_results, 10))
        
        linkedin_urls = []
        for result in results.get('results', []):
            url = result.get('url', '')
            if 'linkedin.com/in/' in url:
                linkedin_urls.append(url)
        
        return linkedin_urls
    except:
        # Fallback：使用 curl + Google
        encoded_query = quote_plus(query)
        url = f"https://www.google.com/search?q={encoded_query}&num={max_results}"
        
        try:
            result = subprocess.run(
                ['curl', '-s', '-A', 'Mozilla/5.0', url],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # 簡單解析 Google 結果頁
            html = result.stdout
            linkedin_urls = re.findall(r'https://[a-z]+\.linkedin\.com/in/[^"&<>\s]+', html)
            
            # 去重
            linkedin_urls = list(set(linkedin_urls))[:max_results]
            
            return linkedin_urls
        except Exception as e:
            print(f"❌ 搜尋失敗：{e}", file=sys.stderr)
            return []

def extract_linkedin_info(url):
    """從 LinkedIn 公開頁面提取資訊（簡化版）"""
    
    # LinkedIn 公開頁面格式：linkedin.com/in/username
    username = url.split('/in/')[-1].split('?')[0].strip('/')
    
    # 使用 web_fetch 嘗試抓取（但可能被擋）
    try:
        result = subprocess.run(
            ['curl', '-s', '-A', 'Mozilla/5.0', url],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        html = result.stdout
        
        # 簡單解析（LinkedIn 結構複雜，只能抓部分資訊）
        name_match = re.search(r'<title>([^|<]+)', html)
        name = name_match.group(1).strip() if name_match else username
        
        # 清理名稱
        name = name.replace(' - Taiwan', '').replace(' | LinkedIn', '').strip()
        
        return {
            'name': name,
            'linkedin_url': url,
            'username': username,
            'source': 'linkedin_public'
        }
    
    except Exception as e:
        print(f"⚠️  無法抓取 {url}: {e}", file=sys.stderr)
        return {
            'name': username,
            'linkedin_url': url,
            'username': username,
            'source': 'linkedin_public'
        }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='LinkedIn 公開個人檔案搜尋')
    parser.add_argument('--keywords', required=True, help='搜尋關鍵字（職位 + 技能）')
    parser.add_argument('--location', default='Taiwan', help='地點')
    parser.add_argument('--max-results', type=int, default=20, help='最大結果數')
    parser.add_argument('--output', default=None, help='輸出檔案')
    
    args = parser.parse_args()
    
    # 搜尋 LinkedIn URLs
    linkedin_urls = google_search_linkedin(
        args.keywords,
        args.location,
        args.max_results
    )
    
    print(f"✅ 找到 {len(linkedin_urls)} 個 LinkedIn 個人檔案", file=sys.stderr)
    
    # 提取資訊
    candidates = []
    for url in linkedin_urls:
        info = extract_linkedin_info(url)
        candidates.append(info)
        time.sleep(1)  # 避免被擋
    
    # 輸出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(candidates, f, ensure_ascii=False, indent=2)
        print(f"💾 結果已存至 {args.output}", file=sys.stderr)
    else:
        print(json.dumps(candidates, ensure_ascii=False, indent=2))
    
    print(f"\n✅ 完成：{len(candidates)} 位候選人", file=sys.stderr)

if __name__ == '__main__':
    main()
