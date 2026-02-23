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
        計算學歷分數 (20%)
        
        Args:
            education: 教育背景陣列
            
        Returns:
            0-20 分
        """
        if not education:
            return 8  # 無學歷資料給基礎分
        
        # 取最高學歷
        degrees = {
            '博士': 20,
            'PhD': 20,
            'Ph.D.': 20,
            'Doctor': 20,
            '碩士': 18,
            'Master': 18,
            'MBA': 18,
            '學士': 15,
            'Bachelor': 15,
            '大學': 15,
            '專科': 10,
            'Associate': 10,
            '高中': 8,
            'High School': 8
        }
        
        max_score = 8  # 預設分數
        
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
                    max_score = min(max_score + 2, 20)  # 名校加 2 分，上限 20
                    break
        
        return max_score
    
    def calculate_experience_score(self, total_years: float) -> float:
        """
        計算工作年資分數 (20%)
        
        Args:
            total_years: 總工作年資
            
        Returns:
            0-20 分
        """
        if total_years >= 10:
            return 20
        elif total_years >= 7:
            return 18
        elif total_years >= 5:
            return 15
        elif total_years >= 3:
            return 12
        elif total_years >= 1:
            return 10
        elif total_years >= 0.5:
            return 8  # 半年以上
        else:
            return 5  # 社會新鮮人
    
    def calculate_skills_score(self, skills: List[str]) -> float:
        """
        計算技能廣度分數 (20%)
        
        Args:
            skills: 技能列表
            
        Returns:
            0-20 分
        """
        skill_count = len(skills)
        
        if skill_count >= 10:
            return 20
        elif skill_count >= 7:
            return 18
        elif skill_count >= 5:
            return 15
        elif skill_count >= 3:
            return 12
        elif skill_count >= 1:
            return 10
        else:
            return 5  # 無技能資料
    
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
        計算職涯發展軌跡分數 (10%)
        
        Args:
            work_history: 工作經歷陣列
            
        Returns:
            0-10 分
        """
        if not work_history or len(work_history) < 2:
            return 7  # 單一工作或無資料給中間分
        
        # 分析職位變化
        positions = [job.get('position', '') for job in work_history]
        
        # 晉升關鍵字
        promotion_keywords = {
            'senior': 2,
            '資深': 2,
            'lead': 2,
            '主管': 2,
            'manager': 3,
            '經理': 3,
            'director': 4,
            '總監': 4,
            'VP': 5,
            'CTO': 5,
            'CEO': 5
        }
        
        # 計算職位等級變化
        scores = []
        for pos in positions:
            pos_score = 0
            for keyword, score in promotion_keywords.items():
                if keyword.lower() in pos.lower():
                    pos_score = max(pos_score, score)
            scores.append(pos_score)
        
        if len(scores) >= 2:
            # 持續晉升
            if all(scores[i] <= scores[i+1] for i in range(len(scores)-1)):
                return 10
            # 有晉升但不連續
            elif scores[-1] > scores[0]:
                return 8
            # 平行發展
            elif scores[-1] == scores[0]:
                return 7
            # 向下發展
            else:
                return 5
        
        return 7
    
    def calculate_special_bonus(self, 
                                education: List[Dict],
                                work_history: List[Dict],
                                skills: List[str],
                                candidate_data: Dict) -> float:
        """
        計算特殊加分 (10%)
        
        Args:
            education: 教育背景
            work_history: 工作經歷
            skills: 技能列表
            candidate_data: 候選人完整資料
            
        Returns:
            0-10 分
        """
        bonus = 0
        
        # 1. 名校畢業 (+3)
        prestigious_schools = [
            '台灣大學', '清華大學', '交通大學', '成功大學', '政治大學',
            'Harvard', 'Stanford', 'MIT', 'Cambridge', 'Oxford'
        ]
        for edu in education:
            school = edu.get('school', '')
            if any(p in school for p in prestigious_schools):
                bonus += 3
                break
        
        # 2. 大廠經驗 (+3)
        big_companies = [
            'Google', 'Microsoft', 'Apple', 'Amazon', 'Meta', 'Tesla',
            'TSMC', '台積電', 'MediaTek', '聯發科', 'HTC', 'ASUS', '華碩'
        ]
        for job in work_history:
            company = job.get('company', '')
            if any(big in company for big in big_companies):
                bonus += 3
                break
        
        # 3. 領域專家 (+2) - 超過 5 年同領域經驗
        if len(work_history) >= 3:
            # 簡化判斷：假設同領域
            bonus += 2
        
        # 4. 開源貢獻 (+2) - GitHub stars > 100
        github_url = candidate_data.get('github_url', '')
        if github_url and 'github.com' in github_url:
            bonus += 2
        
        # 5. 技術社群活躍 (+1)
        linkedin_url = candidate_data.get('linkedin_url', '')
        if linkedin_url and 'linkedin.com' in linkedin_url:
            bonus += 1
        
        # 6. 多語能力 (+1)
        languages = candidate_data.get('languages', [])
        if len(languages) >= 2:
            bonus += 1
        
        return min(bonus, 10)  # 上限 10 分
    
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
