# 人才評級系統 - 使用指南

## 🚀 快速開始

### 安裝需求

```bash
# Python 3.6+
python3 --version

# 無需額外套件（純 Python 標準庫）
```

### 基本使用

```bash
cd /path/to/step1ne-headhunter-skill/modules/talent-grading

# 評級單一候選人
python3 grading-logic.py --resume candidate.json

# 儲存結果到檔案
python3 grading-logic.py --resume candidate.json --output result.json
```

---

## 📋 輸入格式

候選人履歷 JSON 格式：

```json
{
  "name": "候選人姓名",
  "email": "test@example.com",
  "phone": "0912-345-678",
  "position": "目前職位",
  
  "education": [
    {
      "degree": "學士 | 碩士 | 博士",
      "school": "學校名稱",
      "major": "主修科系",
      "start": "2018-09",
      "end": "2022-06"
    }
  ],
  
  "work_history": [
    {
      "company": "公司名稱",
      "position": "職位名稱",
      "start": "2022-07",
      "end": "現在 | 2024-02",
      "duration": 28,
      "current": true
    }
  ],
  
  "total_years": 5.5,
  "job_changes": 3,
  "skills": "Python, React, Docker, AWS, PostgreSQL",
  "stability": 75,
  
  "github_url": "https://github.com/username",
  "linkedin_url": "https://linkedin.com/in/username",
  "languages": ["中文", "英文"]
}
```

### 必填欄位

| 欄位 | 類型 | 說明 |
|------|------|------|
| `name` | string | 候選人姓名 |
| `education` | array | 教育背景（可空陣列） |
| `work_history` | array | 工作經歷（可空陣列） |
| `total_years` | number | 總工作年資 |
| `skills` | string | 技能列表（逗號分隔） |
| `stability` | number | 穩定度評分（20-100） |

### 選填欄位

| 欄位 | 類型 | 說明 |
|------|------|------|
| `email` | string | Email |
| `phone` | string | 電話 |
| `position` | string | 目前職位 |
| `github_url` | string | GitHub 連結 |
| `linkedin_url` | string | LinkedIn 連結 |
| `languages` | array | 語言能力 |

---

## 📊 輸出格式

### Console 輸出

```
==================================================
📊 人才評級結果
==================================================

候選人：張小明
職位：軟體工程師

🏆 綜合評級：A 級
📈 總分：75/100

📋 各維度分數：
  • 學歷背景 (20%): 15/20
  • 工作年資 (20%): 15/20
  • 技能廣度 (20%): 15/20
  • 工作穩定性 (20%): 18/20
  • 職涯發展軌跡 (10%): 7/10
  • 特殊加分 (10%): 5/10

✅ 結果已儲存至：result.json

==================================================
```

### JSON 輸出

```json
{
  "grade": "A",
  "total_score": 75,
  "dimension_scores": {
    "education": 15,
    "experience": 15,
    "skills": 15,
    "stability": 18,
    "trajectory": 7,
    "bonus": 5
  },
  "breakdown": {
    "學歷背景 (20%)": "15/20",
    "工作年資 (20%)": "15/20",
    "技能廣度 (20%)": "15/20",
    "工作穩定性 (20%)": "18/20",
    "職涯發展軌跡 (10%)": "7/10",
    "特殊加分 (10%)": "5/10"
  },
  "timestamp": "2026-02-23T19:45:00.123456"
}
```

---

## 🧪 測試範例

倉庫內建 3 個測試範例：

### 1. 社會新鮮人（B 級預期）

```bash
python3 grading-logic.py --resume examples/fresh-graduate.json
```

**特點**：
- 台大資工碩士應屆畢業生
- 無工作經驗
- 6 個技能
- 名校加分

**預期結果**：B 級（60-69 分）

---

### 2. 資深工程師（A+ 級預期）

```bash
python3 grading-logic.py --resume examples/senior-engineer.json
```

**特點**：
- 交大資工學士
- 8.5 年工作經驗
- 15 個技能
- 持續晉升（Junior → Engineer → Senior）
- 穩定度 75

**預期結果**：A+ 級（80-89 分）

---

### 3. 頂尖人才（S 級預期）

```bash
python3 grading-logic.py --resume examples/top-talent.json
```

**特點**：
- Stanford 博士 + 台大碩士
- 11.5 年工作經驗
- Google/Meta/Microsoft 大廠經驗
- 18 個技能
- 持續晉升（Engineer → Senior → Staff）
- 穩定度 88

**預期結果**：S 級（90-100 分）

---

## 🔧 進階使用

### 批量評級

```bash
# 批量處理資料夾內所有履歷
for file in candidates/*.json; do
  python3 grading-logic.py --resume "$file" --output "results/$(basename $file)"
done
```

### 整合到 Pipeline

```python
# Python 整合範例
from grading_logic import TalentGrader
import json

# 讀取候選人資料
with open('candidate.json', 'r') as f:
    candidate = json.load(f)

# 評級
grader = TalentGrader()
result = grader.grade_candidate(candidate)

# 使用結果
print(f"評級：{result['grade']}")
print(f"分數：{result['total_score']}")
```

### 與後端 API 整合

```bash
# 呼叫評級 API
curl -X POST http://localhost:3001/api/grade \
  -H "Content-Type: application/json" \
  -d @candidate.json
```

---

## 📖 評級邏輯說明

### 6 大評分維度

| 維度 | 權重 | 分數範圍 | 說明 |
|------|------|---------|------|
| **學歷背景** | 20% | 0-20 分 | 學位等級 + 名校加分 |
| **工作年資** | 20% | 0-20 分 | 總年資（10年+ 滿分） |
| **技能廣度** | 20% | 0-20 分 | 技能數量（10+ 滿分） |
| **工作穩定性** | 20% | 0-20 分 | 穩定度評分映射 |
| **職涯發展軌跡** | 10% | 0-10 分 | 晉升/平行/停滯 |
| **特殊加分** | 10% | 0-10 分 | 名校/大廠/開源/語言 |

### 評級對應表

| 等級 | 分數範圍 | 說明 |
|------|---------|------|
| S | 90-100 | 頂尖人才（稀缺） |
| A+ | 80-89 | 優秀人才（強力推薦） |
| A | 70-79 | 合格人才（可推薦） |
| B | 60-69 | 基本合格（需評估） |
| C | <60 | 需補強（謹慎推薦） |

---

## 🐛 常見問題

### Q1: 社會新鮮人評級太低？

A: 社會新鮮人預期為 B 級（60-69 分）。如果學歷優秀（名校碩博士）+ 技能豐富 + 開源貢獻，可達 A 級。

### Q2: 如何處理自由工作者？

A: 自由工作者的穩定性根據「持續接案時長」評分：
- 持續 3 年+ → 15/20
- 1-3 年 → 12/20
- <1 年 → 10/20

### Q3: 跨領域轉職如何評分？

A: 累計總年資，技能評估「可轉移技能」。詳見 `edge-cases.md`。

### Q4: 為什麼頂尖人才只有 97 分不是滿分？

A: 職涯軌跡維度（10%）中，Staff Engineer 給 7/10。如果是 VP/CTO 級別可達滿分。

---

## 📚 相關文檔

- **README.md** - 模組總覽
- **TALENT-GRADING-RULES.md** - 完整評級規則
- **edge-cases.md** - 邊緣案例處理
- **grading-logic.py** - 原始碼

---

**最後更新**：2026-02-23  
**維護者**：YuQi (@YuQi0923_bot)
