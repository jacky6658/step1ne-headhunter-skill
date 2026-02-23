#!/usr/bin/env python3
"""
批量匹配腳本 - Batch Matcher
一個職缺 vs 多個候選人的批量匹配

輸入：公司畫像 + 候選人畫像資料夾
輸出：批量匹配報告（JSON）
"""

import json
import argparse
import os
from typing import Dict, List
from match_personas import PersonaMatcher

def batch_match(company_persona_path: str, candidates_folder: str) -> List[Dict]:
    """
    批量匹配
    
    Args:
        company_persona_path: 公司畫像檔案路徑
        candidates_folder: 候選人畫像資料夾路徑
        
    Returns:
        匹配報告列表（按總分排序）
    """
    # 讀取公司畫像
    with open(company_persona_path, 'r', encoding='utf-8') as f:
        company_persona = json.load(f)
    
    # 初始化匹配器
    matcher = PersonaMatcher()
    
    # 批量匹配
    reports = []
    
    for filename in os.listdir(candidates_folder):
        if not filename.endswith('.json'):
            continue
        
        candidate_path = os.path.join(candidates_folder, filename)
        
        try:
            # 讀取候選人畫像
            with open(candidate_path, 'r', encoding='utf-8') as f:
                candidate_persona = json.load(f)
            
            # 執行匹配
            report = matcher.match(candidate_persona, company_persona)
            reports.append(report)
            
            print(f"✓ {report['candidateName']} - {report['總分']}分 ({report['等級']})")
        
        except Exception as e:
            print(f"✗ {filename} - 匹配失敗: {e}")
    
    # 按總分排序（降序）
    reports.sort(key=lambda x: x['總分'], reverse=True)
    
    return reports


def generate_summary(reports: List[Dict]) -> Dict:
    """
    生成摘要統計
    
    Args:
        reports: 匹配報告列表
        
    Returns:
        摘要統計
    """
    total_candidates = len(reports)
    
    # 等級統計
    grade_counts = {}
    for report in reports:
        grade = report['等級']
        grade_counts[grade] = grade_counts.get(grade, 0) + 1
    
    # Top 5 推薦
    top_5 = reports[:5]
    
    # 平均分
    avg_score = sum(r['總分'] for r in reports) / total_candidates if total_candidates > 0 else 0
    
    return {
        "總候選人數": total_candidates,
        "等級分布": grade_counts,
        "平均分": round(avg_score, 1),
        "Top5推薦": [
            {
                "姓名": r['candidateName'],
                "總分": r['總分'],
                "等級": r['等級'],
                "優先級": r['推薦優先級']
            }
            for r in top_5
        ]
    }


def main():
    parser = argparse.ArgumentParser(description="批量匹配（一個職缺 vs 多個候選人）")
    parser.add_argument("--company", required=True, help="公司畫像 JSON 檔案")
    parser.add_argument("--candidates", required=True, help="候選人畫像資料夾")
    parser.add_argument("--output", required=True, help="輸出批量匹配報告 JSON 檔案")
    
    args = parser.parse_args()
    
    print(f"🔍 開始批量匹配...")
    print(f"   公司畫像：{args.company}")
    print(f"   候選人資料夾：{args.candidates}")
    print()
    
    # 執行批量匹配
    reports = batch_match(args.company, args.candidates)
    
    # 生成摘要
    summary = generate_summary(reports)
    
    # 組合完整報告
    batch_report = {
        "摘要": summary,
        "詳細匹配報告": reports
    }
    
    # 輸出結果
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(batch_report, f, ensure_ascii=False, indent=2)
    
    print()
    print(f"✅ 批量匹配完成！")
    print(f"   總候選人數：{summary['總候選人數']}")
    print(f"   平均分：{summary['平均分']}")
    print(f"   等級分布：{summary['等級分布']}")
    print()
    print(f"📊 Top 5 推薦：")
    for i, candidate in enumerate(summary['Top5推薦'], 1):
        print(f"   {i}. {candidate['姓名']} - {candidate['總分']}分 ({candidate['等級']}級)")
    print()
    print(f"📄 完整報告已儲存：{args.output}")


if __name__ == "__main__":
    main()
