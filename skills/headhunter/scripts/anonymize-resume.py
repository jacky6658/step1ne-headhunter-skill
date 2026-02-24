#!/usr/bin/env python3
"""
Step1ne 匿名履歷生成器

用途：將候選人資料套用統一範本，生成匿名化履歷
確保所有 AI Bot 生成的格式完全一致
"""

import json
import sys
import os
import random
from datetime import datetime

# 英文代號池（隨機生成用）
CANDIDATE_CODES = [
    'Abeni', 'Sarah', 'Kevin', 'David', 'Emily', 'Michael', 'Jessica', 'Daniel',
    'Sophia', 'James', 'Olivia', 'William', 'Emma', 'Alexander', 'Isabella',
    'Benjamin', 'Mia', 'Lucas', 'Charlotte', 'Henry', 'Amelia', 'Sebastian'
]

# 公司匿名化對照表
COMPANY_ANONYMIZATION = {
    # 遊戲產業
    '遊戲橘子': '某遊戲科技公司',
    '雷亞遊戲': '某遊戲科技公司',
    '智冠': '某遊戲科技公司',
    '創樂': '某網路服務公司',
    
    # 電商平台
    'PChome': '某知名電商平台',
    'momo': '某知名電商平台',
    '蝦皮': '某知名電商平台',
    
    # 金融科技
    '街口': '某金融科技公司',
    '玉山銀行': '某金融機構',
    '國泰': '某金融機構',
    
    # 製造業
    '鴻海': '某製造業集團',
    '台積電': '某半導體公司',
    '聯發科': '某半導體公司',
    
    # 外商
    'Google': '某外商科技公司',
    'Microsoft': '某外商科技公司',
    'Meta': '某外商科技公司',
}

# 產業關鍵字匹配
INDUSTRY_KEYWORDS = {
    '遊戲': '某遊戲科技公司',
    '電商': '某知名電商平台',
    '金融': '某金融科技公司',
    '製造': '某製造業集團',
    '軟體': '某網路服務公司',
    '外商': '某外商科技公司',
    '半導體': '某半導體公司',
    'FinTech': '某金融科技公司',
}


def generate_candidate_code(candidate_data, use_job_code=False):
    """
    生成候選人代號
    
    Args:
        candidate_data: 候選人資料
        use_job_code: 是否使用職位代號（PM-2026-001）而非英文代號
    
    Returns:
        候選人代號字串
    """
    if use_job_code:
        # 職位代號模式
        job_title = candidate_data.get('currentJobTitle', 'PM')
        year = datetime.now().year
        
        # 職能代號對照
        job_code_map = {
            'Product Manager': 'PM',
            'Backend Engineer': 'BE',
            'Frontend Engineer': 'FE',
            'Full Stack': 'FS',
            'Data Analyst': 'DA',
            'Data Engineer': 'DE',
            'QA Engineer': 'QA',
            'DevOps': 'DO',
        }
        
        code = 'PM'  # 預設
        for title, abbr in job_code_map.items():
            if title.lower() in job_title.lower():
                code = abbr
                break
        
        # 序號（從資料中取得或隨機）
        seq = candidate_data.get('id', random.randint(1, 999))
        return f"{code}-{year}-{seq:03d}"
    else:
        # 英文代號模式（隨機選擇）
        return random.choice(CANDIDATE_CODES)


def anonymize_company(company_name, industry='', size=''):
    """
    匿名化公司名稱
    
    Args:
        company_name: 原始公司名稱
        industry: 產業類型
        size: 公司規模
    
    Returns:
        匿名化後的公司描述
    """
    # 1. 先查對照表（精確匹配）
    for key, anonymous_name in COMPANY_ANONYMIZATION.items():
        if key in company_name:
            if industry and size:
                return f"{anonymous_name}（{industry}，{size}）"
            return anonymous_name
    
    # 2. 根據產業關鍵字匹配
    for keyword, anonymous_name in INDUSTRY_KEYWORDS.items():
        if keyword in company_name or keyword in industry:
            if industry and size:
                return f"{anonymous_name}（{industry}，{size}）"
            return anonymous_name
    
    # 3. 預設
    if industry and size:
        return f"某科技公司（{industry}，{size}）"
    return "某科技公司"


def format_work_experience(work_history):
    """
    格式化工作經歷（匿名化 + 統一格式）
    
    Args:
        work_history: 工作經歷列表
    
    Returns:
        格式化後的工作經歷字串
    """
    # 如果 work_history 是字串，轉換為簡單陣列格式
    if isinstance(work_history, str):
        work_history = [{
            'company': '前公司',
            'title': work_history,
            'startDate': '',
            'endDate': '現在',
            'duties': [work_history],
            'achievements': []
        }]
    
    formatted = []
    
    for job in work_history:
        # 匿名化公司名稱
        company = anonymize_company(
            job.get('company', ''),
            job.get('industry', ''),
            job.get('size', '')
        )
        
        # 任職期間
        start = job.get('startDate', '')
        end = job.get('endDate', '現在')
        status = '在職中' if end == '現在' else ''
        period = f"{start} ~ {end}"
        if status:
            period += f"（{status}）"
        
        # 職稱
        title = job.get('title', '')
        
        # 工作內容（bullet points）
        duties = job.get('duties', [])
        duties_text = '\n'.join([f"• {duty}" for duty in duties])
        
        # 成就/專案
        achievements = job.get('achievements', [])
        achievements_text = '\n'.join([f"• {ach}" for ach in achievements])
        
        # 離職原因
        reason = job.get('leaveReason', '')
        
        # 組合
        job_block = f"""{company}

任職期間：{period}

職稱：{title}

工作內容：
{duties_text}

成就/專案：
{achievements_text}

離職原因：{reason}
"""
        formatted.append(job_block)
    
    return '\n───────────────────────────────────────────────────────────────────────\n\n'.join(formatted)


def calculate_age(birth_year):
    """計算年齡"""
    current_year = datetime.now().year
    return current_year - int(birth_year)


def generate_anonymous_resume(candidate_data, job_data, consultant_name='Jacky Chen'):
    """
    生成匿名履歷（套用統一範本）
    
    Args:
        candidate_data: 候選人資料（dict）
        job_data: 職缺資料（dict）
        consultant_name: 推薦顧問姓名
    
    Returns:
        匿名履歷字串（Markdown 格式）
    """
    # 讀取範本
    template_path = os.path.join(
        os.path.dirname(__file__),
        '../templates/anonymous-resume-template.md'
    )
    
    with open(template_path, 'r', encoding='utf-8') as f:
        # 跳過前面的說明，只取範本部分
        content = f.read()
        # 找到 "## 完整範本" 後的內容
        template_start = content.find('```\n═══════')
        template_end = content.rfind('```')
        template = content[template_start + 4:template_end]
    
    # 生成候選人代號
    candidate_code = generate_candidate_code(candidate_data, use_job_code=False)
    
    # 替換變數
    resume = template
    
    # 基本資訊
    resume = resume.replace('{{RECOMMENDATION_DATE}}', datetime.now().strftime('%Y-%m-%d'))
    
    # 處理 company（可能是字串或物件）
    company = job_data.get('company', '')
    if isinstance(company, dict):
        company_name = company.get('name', '目標公司')
    else:
        company_name = company or '目標公司'
    resume = resume.replace('{{CLIENT_COMPANY}}', company_name)
    
    resume = resume.replace('{{JOB_TITLE}}', job_data.get('title', ''))
    resume = resume.replace('{{CANDIDATE_CODE}}', candidate_code)
    
    # Personal Particulars
    birth_year = candidate_data.get('birthYear', '1990')
    resume = resume.replace('{{BIRTH_YEAR}}', str(birth_year))
    resume = resume.replace('{{AGE}}', str(calculate_age(birth_year)))
    resume = resume.replace('{{LANGUAGE_SKILLS}}', candidate_data.get('languageSkills', 'Chinese: Native speaker'))
    resume = resume.replace('{{MARITAL_STATUS}}', candidate_data.get('maritalStatus', 'Single'))
    resume = resume.replace('{{NATIONALITY}}', candidate_data.get('nationality', 'Taiwan Citizen'))
    resume = resume.replace('{{RESIDENCE}}', candidate_data.get('residence', 'Taipei City'))
    
    # 教育背景
    resume = resume.replace('{{EDUCATION}}', candidate_data.get('education', ''))
    
    # Summary & Skills
    resume = resume.replace('{{SUMMARY}}', candidate_data.get('summary', ''))
    resume = resume.replace('{{SKILLS}}', candidate_data.get('skills', ''))
    
    # 工作經歷（匿名化）
    work_experience = format_work_experience(candidate_data.get('workHistory', []))
    resume = resume.replace('{{WORK_EXPERIENCE}}', work_experience)
    
    # 證照 & 其他
    resume = resume.replace('{{CERTIFICATIONS}}', candidate_data.get('certifications', '無'))
    resume = resume.replace('{{OTHER_INFO}}', candidate_data.get('otherInfo', '無'))
    
    # 薪資結構
    resume = resume.replace('{{PREVIOUS_SALARY}}', candidate_data.get('previousSalary', ''))
    resume = resume.replace('{{CURRENT_SALARY}}', candidate_data.get('currentSalary', ''))
    resume = resume.replace('{{EXPECTED_SALARY}}', candidate_data.get('expectedSalary', ''))
    resume = resume.replace('{{SALARY_NOTE}}', candidate_data.get('salaryNote', ''))
    resume = resume.replace('{{ON_BOARD_DATE}}', candidate_data.get('onBoardDate', 'One month notice period'))
    
    # 獵頭附加價值
    resume = resume.replace('{{RECOMMENDATION_REASON}}', candidate_data.get('recommendationReason', ''))
    resume = resume.replace('{{MATCH_ANALYSIS}}', candidate_data.get('matchAnalysis', ''))
    resume = resume.replace('{{SUGGESTIONS}}', candidate_data.get('suggestions', ''))
    resume = resume.replace('{{CONSULTANT_NAME}}', consultant_name)
    
    return resume


def main():
    """命令列介面"""
    if len(sys.argv) < 3:
        print("使用方式：python anonymize-resume.py <candidate.json> <job.json> [consultant_name]")
        print("\n範例：")
        print("  python anonymize-resume.py candidate-001.json job-pm.json 'Jacky Chen'")
        sys.exit(1)
    
    candidate_file = sys.argv[1]
    job_file = sys.argv[2]
    consultant_name = sys.argv[3] if len(sys.argv) > 3 else 'Jacky Chen'
    
    # 讀取資料
    with open(candidate_file, 'r', encoding='utf-8') as f:
        candidate_data = json.load(f)
    
    with open(job_file, 'r', encoding='utf-8') as f:
        job_data = json.load(f)
    
    # 生成匿名履歷
    resume = generate_anonymous_resume(candidate_data, job_data, consultant_name)
    
    # 輸出
    output_file = f"anonymous-resume-{candidate_data.get('id', 'unknown')}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(resume)
    
    print(f"✅ 匿名履歷已生成：{output_file}")
    print(f"📋 候選人代號：{generate_candidate_code(candidate_data)}")


if __name__ == '__main__':
    main()
