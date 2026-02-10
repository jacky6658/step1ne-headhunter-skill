#!/usr/bin/env python3
"""從 104 公司頁面抓取官網 - 最終版"""

import subprocess
import json
import re
import time

SHEET_ID = "1bkI7_cCh_Bs4qVa3HlXiy0CFzmItZlA-DYGHSPS4InE"
ACCOUNT = "aijessie88@step1ne.com"

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def get_company_keyword(company_name):
    """提取公司英文關鍵字"""
    # 移除「股份有限公司」等後綴
    name = re.sub(r'(股份有限公司|有限公司|科技|集團|企業團)', '', company_name)
    
    # 常見公司名稱對應
    mapping = {
        '東豐': 'dftech',
        '康統': 'kenkone',
        '和運': 'easyrent',
        '詮欣': 'coxoc',
        '台泥': 'tcc',
        '怡利': 'ili',
        '矽格': 'sigurd',
        '綠創': 'greenon',
        '宜鼎': 'innodisk',
        '怡凡得': 'ibase',
        '醫知彼': 'deeplobe',
        '杜浦': 'douper',
        '昕力': 'synergy',
        '承映': 'acelink',
        '智影': 'ivisual',
        '緯穎': 'wiwynn'
    }
    
    for key, val in mapping.items():
        if key in company_name:
            return val
    
    return None

def fetch_website_from_104(company_id):
    """從 104 公司頁面抓取官網"""
    url = f"https://www.104.com.tw/company/{company_id}"
    
    run(f'agent-browser open "{url}"')
    run('agent-browser wait --load networkidle --timeout 8000')
    
    # 方法1：用公司關鍵字找連結
    keyword = get_company_keyword("")  # 暫時不用
    
    # 方法2：找所有外部連結，排除常見平台
    js = """
        Array.from(document.querySelectorAll('a[href^="http"]'))
            .map(a => a.href)
            .filter(href => 
                !href.includes('104.com.tw') &&
                !href.includes('onelink.me') &&
                !href.includes('google.com') &&
                !href.includes('translate') &&
                !href.includes('facebook') &&
                !href.includes('linkedin') &&
                href.match(/^https?:\\/\\/www\\.[a-z0-9-]+\\.[a-z]{2,}/)
            )[0] || null
    """
    
    website = run(f"agent-browser eval '{js}'").strip('"')
    
    if website and website != 'null':
        return website
    
    return "暫不提供"

def main():
    print("開始抓取...")
    
    # 讀取公司列表
    data = run(f'gog sheets get {SHEET_ID} "A2:F17" --account {ACCOUNT} --json')
    rows = json.loads(data).get('values', [])
    
    for idx, row in enumerate(rows, start=2):
        company = row[0] if len(row) > 0 else ""
        col_e = row[4] if len(row) > 4 else ""  # 104 公司頁面
        
        if not company:
            continue
        
        print(f"\n[{idx}] {company}")
        
        # 從第5欄提取公司 ID
        if col_e and '/company/' in col_e:
            company_id = col_e.split('/company/')[1].split('?')[0].split('#')[0]
        else:
            print("  ✗ 無 104 公司 ID")
            continue
        
        try:
            website = fetch_website_from_104(company_id)
            print(f"  ✓ {website}")
            
            # 更新
            run(f'gog sheets update {SHEET_ID} "D{idx}" "{website}" --account {ACCOUNT}')
            
        except Exception as e:
            print(f"  ✗ 錯誤: {e}")
        
        time.sleep(2)
    
    run('agent-browser close')
    print("\n✅ 完成")

if __name__ == "__main__":
    main()
