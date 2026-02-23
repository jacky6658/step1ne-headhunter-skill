#!/usr/bin/env python3
"""
Step1ne 人才評級系統 - 評分邏輯
Talent Grading System - Grading Logic

評級標準：S (90-100) / A+ (80-89) / A (70-79) / B (60-69) / C (<60)
"""

import json
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional


class TalentGrader:
    """人才評級引擎"""
    
    # 評級對應表
    GRADE_MAPPING = {
        'S': (90, 100),
        'A+': (80, 89),
        'A': (70, 79),
        'B': (60, 69),
        'C': (0, 59)
    }
    
    def __init__(self):
        self.total_score = 0
        self.dimension_scores = {}
    
    def calculate_education_score(self, education: List[Dict]) -> float:
        """
        計算學歷分數 (10%) - 方案 A
        
        Args:
            education: 教育背景陣列
            
        Returns:
            0-10 分
        """
        if not education:
            return 5  # 無學歷資料給基礎分
        
        # 取最高學歷（分數範圍調整為 0-10）
        degrees = {
            '博士': 10,
            'PhD': 10,
            'Ph.D.': 10,
            'Doctor': 10,
            '碩士': 9,
            'Master': 9,
            'MBA': 9,
            '學士': 7.5,
            'Bachelor': 7.5,
            '大學': 7.5,
            '專科': 6,
            'Associate': 6,
            '高中': 5,
            'High School': 5
        }
        
        max_score = 5  # 預設分數
        
        for edu in education:
            degree = edu.get('degree', '')
            for keyword, score in degrees.items():
                if keyword in degree:
                    max_score = max(max_score, score)
        
        # 名校加分（台清交成政、國外 Top 50）
        prestigious_schools = [
            '台灣大學', '清華大學', '交通大學', '成功大學', '政治大學',
            'National Taiwan University', 'NTU',
            'Harvard', 'Stanford', 'MIT', 'Cambridge', 'Oxford'
        ]
        
        for edu in education:
            school = edu.get('school', '')
            for prestigious in prestigious_schools:
                if prestigious in school:
                    max_score = min(max_score + 1, 10)  # 名校加 1 分，上限 10
                    break
        
        return max_score
    
    def calculate_experience_score(self, total_years: float) -> float:
        """
        計算工作年資分數 (15%) - 方案 A
        
        Args:
            total_years: 總工作年資
            
        Returns:
            0-15 分
        """
        if total_years >= 10:
            return 15
        elif total_years >= 7:
            return 12.5
        elif total_years >= 5:
            return 11
        elif total_years >= 3:
            return 9
        elif total_years >= 1:
            return 6
        elif total_years >= 0.5:
            return 4  # 半年以上
        else:
            return 3.5  # 社會新鮮人
    
    def calculate_skills_score(self, skills: List[str]) -> float:
        """
        計算技能匹配度分數 (25%) - 方案 A
        技能數量 + 深度關鍵字 + 認證
        
        Args:
            skills: 技能列表
            
        Returns:
            0-25 分
        """
        if not skills:
            return 5  # 無技能資料
        
        skill_count = len(skills)
        
        # 基礎分：技能數量（每個 1.5 分，上限 15 分）
        base_score = min(skill_count * 1.5, 15)
        
        # 深度關鍵字加分（+5 分）
        advanced_keywords = [
            'architect', '架構', 'lead', 'senior', '資深',
            'expert', '專家', 'advanced', '進階'
        ]
        skills_text = ' '.join(skills).lower()
        has_advanced = any(kw in skills_text for kw in advanced_keywords)
        advanced_bonus = 5 if has_advanced else 0
        
        # 認證加分（+5 分）
        cert_keywords = ['aws', 'gcp', 'azure', 'pmp', 'cissp', '證照', 'certified', 'certification']
        has_cert = any(kw in skills_text for kw in cert_keywords)
        cert_bonus = 5 if has_cert else 0
        
        total = base_score + advanced_bonus + cert_bonus
        return min(total, 25)  # 上限 25 分
    
    def calculate_stability_score(self, stability: int) -> float:
        """
        計算工作穩定性分數 (20%)
        
        Args:
            stability: 穩定度評分 (20-100)
            
        Returns:
            0-20 分
        """
        # 穩定度評分已經是 20-100 的範圍
        # 直接映射到 0-20 分
        if stability >= 80:
            return 20
        elif stability >= 70:
            return 18
        elif stability >= 60:
            return 15
        elif stability >= 50:
            return 12
        elif stability >= 40:
            return 10
        else:
            return 8  # 穩定度較低給基礎分
    
    def calculate_career_trajectory_score(self, work_history: List[Dict]) -> float:
        """
        計算職涯發展軌跡分數 (25%) - 方案 A
        晉升記錄 + 職位層級變化
        
        Args:
            work_history: 工作經歷陣列
            
        Returns:
            0-25 分
        """
        if not work_history or len(work_history) < 2:
            return 12.5  # 單一工作或無資料給一半分
        
        # 分析職位變化
        positions = [job.get('position', '') for job in work_history]
        
        # 職位層級對應表（擴充版本）
        level_keywords = {
            'CEO': 10, 'CTO': 10, 'CFO': 10, 'COO': 10,
            '執行長': 10, '技術長': 10, '財務長': 10, '營運長': 10,
            '總經理': 9, 'VP': 9, '副總': 9, 'Vice President': 9,
            '協理': 8, '總監': 8, 'Director': 8,
            '經理': 7, 'Manager': 7, '部門主管': 7,
            '副理': 6, '組長': 6, 'Team Lead': 6, 'Lead': 6,
            '資深': 6, 'Senior': 6, '主管': 6,
            '工程師': 5, 'Engineer': 5, '專員': 5, '開發': 5,
            'Junior': 4, '初級': 4,
            '助理': 3, 'Assistant': 3,
            '實習': 2, 'Intern': 2
        }
        
        # 計算每個職位的等級
        def get_level(position):
            pos_lower = position.lower()
            for keyword, level in sorted(level_keywords.items(), key=lambda x: -len(x[0])):
                if keyword.lower() in pos_lower:
                    return level
            return 5  # 預設等級
        
        levels = [get_level(pos) for pos in positions]
        
        # 分析晉升軌跡
        score = 0
        promotions = 0
        lateral = 0
        demotions = 0
        
        for i in range(len(levels) - 1):
            diff = levels[i] - levels[i+1]  # 反向（最新 - 較舊）
            
            if diff >= 3:
                promotions += 1
                score += 25  # 跨級晉升
            elif diff == 2:
                promotions += 1
                score += 20  # 明顯晉升
            elif diff == 1:
                promotions += 1
                score += 15  # 小幅晉升
            elif diff == 0:
                lateral += 1
                score += 10  # 平級
            elif diff == -1:
                demotions += 1
                score += 5  # 小幅降級
            else:
                demotions += 1
                score += 0  # 明顯降級
        
        # 額外加分
        if promotions >= 3:
            score += 5  # 持續晉升獎勵
        if demotions == 0:
            score += 3  # 無降級獎勵
        
        return min(score, 25)  # 上限 25 分
    
    def calculate_special_bonus(self, 
                                education: List[Dict],
                                work_history: List[Dict],
                                skills: List[str],
                                candidate_data: Dict) -> float:
        """
        計算特殊加分 (5%) - 方案 A
        語言能力 + 軟實力 + 成就
        
        Args:
            education: 教育背景
            work_history: 工作經歷
            skills: 技能列表
            candidate_data: 候選人完整資料
            
        Returns:
            0-5 分
        """
        bonus = 0
        
        # 1. 語言能力 (+2)
        language_keywords = [
            '英文', 'english', '雙語', 'bilingual', 'trilingual',
            'toeic', 'ielts', 'toefl', 'celpip'
        ]
        skills_text = ' '.join(skills).lower() if skills else ''
        notes = candidate_data.get('notes', '').lower()
        combined = skills_text + ' ' + notes
        
        if any(kw in combined for kw in language_keywords):
            bonus += 2
        
        # 2. 軟實力 (+2)
        soft_skill_keywords = [
            '溝通', 'communication', '領導', 'leadership',
            '團隊合作', 'teamwork', '問題解決', 'problem solving',
            '批判性思維', 'critical thinking'
        ]
        if any(kw in combined for kw in soft_skill_keywords):
            bonus += 2
        
        # 3. 特殊成就 (+1)
        achievement_keywords = [
            '獲獎', 'award', '專利', 'patent', '出版', 'publication',
            '演講', 'speaker', 'conference'
        ]
        if any(kw in combined for kw in achievement_keywords):
            bonus += 1
        
        return min(bonus, 5)  # 上限 5 分
    
    def grade_candidate(self, candidate_data: Dict) -> Dict[str, Any]:
        """
        綜合評級候選人
        
        Args:
            candidate_data: 候選人完整資料
            
        Returns:
            評級結果（包含總分、等級、各維度分數）
        """
        # 提取資料
        education = candidate_data.get('education', [])
        if isinstance(education, str):
            try:
                education = json.loads(education)
            except:
                education = []
        
        work_history = candidate_data.get('work_history', [])
        if isinstance(work_history, str):
            try:
                work_history = json.loads(work_history)
            except:
                work_history = []
        
        skills_raw = candidate_data.get('skills', '')
        if isinstance(skills_raw, str):
            skills = [s.strip() for s in skills_raw.split(',') if s.strip()]
        else:
            skills = skills_raw if isinstance(skills_raw, list) else []
        
        total_years = float(candidate_data.get('total_years', 0))
        stability = int(candidate_data.get('stability', 50))
        
        # 計算各維度分數
        education_score = self.calculate_education_score(education)
        experience_score = self.calculate_experience_score(total_years)
        skills_score = self.calculate_skills_score(skills)
        stability_score = self.calculate_stability_score(stability)
        trajectory_score = self.calculate_career_trajectory_score(work_history)
        bonus_score = self.calculate_special_bonus(
            education, work_history, skills, candidate_data
        )
        
        # 加總
        total = (
            education_score +
            experience_score +
            skills_score +
            stability_score +
            trajectory_score +
            bonus_score
        )
        
        # 判定等級
        grade = 'C'
        for g, (min_score, max_score) in self.GRADE_MAPPING.items():
            if min_score <= total <= max_score:
                grade = g
                break
        
        # 儲存結果
        self.total_score = total
        self.dimension_scores = {
            'education': education_score,
            'experience': experience_score,
            'skills': skills_score,
            'stability': stability_score,
            'trajectory': trajectory_score,
            'bonus': bonus_score
        }
        
        return {
            'grade': grade,
            'total_score': round(total, 1),
            'dimension_scores': self.dimension_scores,
            'breakdown': {
                '學歷背景 (20%)': f"{education_score}/20",
                '工作年資 (20%)': f"{experience_score}/20",
                '技能廣度 (20%)': f"{skills_score}/20",
                '工作穩定性 (20%)': f"{stability_score}/20",
                '職涯發展軌跡 (10%)': f"{trajectory_score}/10",
                '特殊加分 (10%)': f"{bonus_score}/10"
            },
            'timestamp': datetime.now().isoformat()
        }


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description='Step1ne 人才評級系統'
    )
    parser.add_argument(
        '--resume',
        required=True,
        help='候選人履歷 JSON 檔案路徑'
    )
    parser.add_argument(
        '--output',
        help='輸出結果 JSON 檔案路徑（可選）'
    )
    
    args = parser.parse_args()
    
    # 讀取履歷資料
    with open(args.resume, 'r', encoding='utf-8') as f:
        candidate_data = json.load(f)
    
    # 評級
    grader = TalentGrader()
    result = grader.grade_candidate(candidate_data)
    
    # 輸出結果
    print("\n" + "="*50)
    print(f"📊 人才評級結果")
    print("="*50)
    print(f"\n候選人：{candidate_data.get('name', 'Unknown')}")
    print(f"職位：{candidate_data.get('position', 'Unknown')}")
    print(f"\n🏆 綜合評級：{result['grade']} 級")
    print(f"📈 總分：{result['total_score']}/100")
    print("\n📋 各維度分數：")
    for dim, score in result['breakdown'].items():
        print(f"  • {dim}: {score}")
    
    # 儲存到檔案
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 結果已儲存至：{args.output}")
    
    print("\n" + "="*50 + "\n")
    
    return result


if __name__ == '__main__':
    main()
