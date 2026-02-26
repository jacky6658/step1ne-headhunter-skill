# 🎯 人才智能爬蟲系統 - 整合指南

**版本**：1.0  
**最後更新**：2026-02-26  
**作者**：YuQi AI (Jacky-aibot)  
**系統**：Step1ne 獵頭自動化系統

---

## 📌 快速導航

- [系統架構](#系統架構) - 5 個模組如何協作
- [安裝 & 環境設定](#安裝--環境設定)
- [使用指南](#使用指南) - 快速開始
- [API 整合點](#api-整合點) - 連接到後端
- [Cron 自動化](#cron-自動化) - 週期執行
- [故障排除](#故障排除)
- [與現有系統銜接](#與現有系統銜接)

---

## 🏗️ 系統架構

### 核心模組

```
輸入：職缺清單
  ↓
┌─────────────────────────────────────────┐
│ 1️⃣  unified-scraper-v4-enhanced.py    │
│   • 產業感知並行爬蟲                      │
│   • 支援 GitHub + LinkedIn               │
│   • Layer 1/2 優先級分離                 │
│   • SQLite 增量快取                      │
└─────────────────────────────────────────┘
  ↓ 輸出：候選人列表 (JSON)
┌─────────────────────────────────────────┐
│ 2️⃣  candidate-scoring-system-v2.py    │
│   • 6 維度評分引擎                        │
│   • 技能 + 經驗 + 地點 + 訊號 + 公司 + 產業 │
│   • 產業遷移能力矩陣                      │
│   • 輸出 S/A+/A/B/C 等級                 │
└─────────────────────────────────────────┘
  ↓ 輸出：評分結果 (JSON)
┌─────────────────────────────────────────┐
│ 3️⃣  industry-migration-analyzer.py    │
│   • 3 維度遷移分析                        │
│   • 技能可轉移性 + 產業相似度 + 學習準備度 │
│   • 跨產業人才評估                       │
└─────────────────────────────────────────┘
  ↓ 輸出：遷移能力報告 (JSON)
┌─────────────────────────────────────────┐
│ 4️⃣  search-plan-executor.py           │
│   • 端到端流程協調器                      │
│   • 調用 1-3 號模組                      │
│   • 生成最終推薦人選                      │
│   • 輸出 JSON + HTML                     │
└─────────────────────────────────────────┘
  ↓ 輸出：推薦清單 + 分析報告
┌─────────────────────────────────────────┐
│ 5️⃣  industry-analytics-dashboard.py   │
│   • 儀表板可視化                          │
│   • Chart.js 即時圖表                    │
│   • 產業分布 + 技能分布 + 評級分布        │
│   • 生成 HTML 網頁版本                    │
└─────────────────────────────────────────┘
  ↓ 輸出：HTML 儀表板 + JSON 報告
```

### 數據流向

```
職缺資料
  ↓
GitHub/LinkedIn API
  ↓
unified-scraper-v4 (爬蟲)
  ↓ [候選人數據]
candidate-scoring-system-v2 (評分)
  ↓ [評分結果]
search-plan-executor (協調)
  ├→ Top 3 推薦
  ├→ JSON 報告
  └→ industry-analytics-dashboard (儀表板)
      ↓
      HTML 儀表板 + 統計數據
```

### 模組依賴

```
unified-scraper-v4-enhanced.py
  └─ 依賴：requests, json, sqlite3, concurrent.futures
  
candidate-scoring-system-v2.py
  └─ 依賴：dataclasses, json, typing
  
industry-migration-analyzer.py
  └─ 依賴：dataclasses, json, typing, statistics
  
search-plan-executor.py
  └─ 依賴：上述 3 個模組 + json
  
industry-analytics-dashboard.py
  └─ 依賴：json, dataclasses, datetime, collections
```

---

## 📦 安裝 & 環境設定

### 前置要求

```bash
# Python 3.8+
python3 --version

# 必要庫
pip install requests

# 可選（用於加強功能）
pip install pandas
pip install jinja2
```

### 環境變數設定

**第 1 步：創建 `.env.example`**

```bash
cat > /Users/user/clawd/hr-tools/.env.example << 'EOF'
# ==================== GitHub API ====================
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_ORG=optional_organization

# ==================== LinkedIn (可選) ====================
LINKEDIN_EMAIL=your_linkedin_email
LINKEDIN_PASSWORD=your_linkedin_password

# ==================== Google Sheets ====================
GOOGLE_SHEET_ID=1PunpaDAFBPBL_I76AiRYGXKaXDZvMl1c262SEtxRk6Q

# ==================== Telegram 通知 (可選) ====================
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# ==================== 爬蟲設定 ====================
SCRAPER_WORKERS=3  # 並行 worker 數（推薦 2-5）
SCRAPER_TIMEOUT=30  # 超時秒數
SCRAPER_RETRY=3  # 重試次數

# ==================== 評分權重 ====================
SCORE_SKILL_WEIGHT=0.25
SCORE_EXPERIENCE_WEIGHT=0.20
SCORE_LOCATION_WEIGHT=0.15
SCORE_SIGNAL_WEIGHT=0.15
SCORE_COMPANY_WEIGHT=0.15
SCORE_INDUSTRY_WEIGHT=0.10
EOF
```

**第 2 步：複製並填入實際值**

```bash
cp /Users/user/clawd/hr-tools/.env.example \
   /Users/user/clawd/hr-tools/.env

# 編輯 .env 檔案
nano /Users/user/clawd/hr-tools/.env
```

**第 3 步：載入環境變數**

```bash
# 在執行爬蟲前執行
source /Users/user/clawd/hr-tools/.env
```

### 檔案位置

```
爬蟲腳本位置：
/Users/user/clawd/hr-tools/

├── unified-scraper-v4-enhanced.py
├── candidate-scoring-system-v2.py
├── industry-migration-analyzer.py
├── search-plan-executor.py
├── industry-analytics-dashboard.py
├── automated-recruiting-pipeline.sh
├── .env                            ← 環境變數
└── .env.example

輸出位置：
/tmp/recruiting-pipeline/

├── reports/                        ← HTML + JSON 報告
│   ├── analytics-dashboard.html
│   ├── analytics-report.json
│   └── recommendations.json
│
└── logs/                          ← 執行日誌
    └── pipeline-20260226.log
```

---

## 🚀 使用指南

### 方式 A：快速測試（單職缺）

```bash
cd /Users/user/clawd/hr-tools

# 執行完整流程（爬蟲 → 評分 → 推薦 → 儀表板）
python3 search-plan-executor.py \
  --job-id 1 \
  --job-title "AI工程師" \
  --industry "internet" \
  --required-skills "Python,AI,機器學習"
```

**預期輸出：**
```
✅ 搜尋 AI 工程師...
✅ 找到 25 位候選人
✅ 評分中...
✅ 生成推薦 Top 3
✅ 儀表板已保存至：/tmp/recruiting-pipeline/reports/
```

### 方式 B：批量搜尋（多職缺）

```bash
# 執行 automated-recruiting-pipeline.sh
bash /Users/user/clawd/hr-tools/automated-recruiting-pipeline.sh layer1

# 或指定層級
bash /Users/user/clawd/hr-tools/automated-recruiting-pipeline.sh layer2
```

### 方式 C：單模組使用

**只執行爬蟲：**
```bash
python3 -c "
from unified_scraper_v4_enhanced import SearchPlanExecutor
executor = SearchPlanExecutor()
results = executor.search_candidates(
    job_title='全端工程師',
    required_skills=['JavaScript', 'React']
)
print(results)
"
```

**只執行評分：**
```bash
python3 -c "
from candidate_scoring_system_v2 import CandidateScoringEngine
engine = CandidateScoringEngine()
score = engine.evaluate_candidate(candidate_dict, job_requirement_dict)
print(f'評分: {score.composite_rating}')
"
```

**只生成儀表板：**
```bash
python3 -c "
from industry_analytics_dashboard import AnalyticsDashboard
dashboard = AnalyticsDashboard()
dashboard.generate_dashboard(candidates_data, jobs_data)
"
```

---

## 🔗 API 整合點

### 與 Step1ne 後端連接

**基本配置：**
```python
# 在爬蟲中設定 API 端點
API_BASE_URL = "https://backendstep1ne.zeabur.app"

# 或本地開發
API_BASE_URL = "http://localhost:3001"
```

### 1️⃣ 獲取職缺清單

```bash
curl -X GET "https://backendstep1ne.zeabur.app/api/jobs" \
  -H "Content-Type: application/json"
```

**回應範例：**
```json
{
  "jobs": [
    {
      "id": 1,
      "title": "AI工程師",
      "industry": "internet",
      "required_skills": ["Python", "AI"],
      "experience_years": 3,
      "salary_range": "80k-120k"
    }
  ]
}
```

### 2️⃣ 批量導入候選人

```bash
curl -X POST "https://backendstep1ne.zeabur.app/api/candidates" \
  -H "Content-Type: application/json" \
  -d '{
    "candidates": [
      {
        "name": "陳宥樺",
        "email": "chen@example.com",
        "skills": ["Python", "Go"],
        "experience_years": 5,
        "source": "github",
        "github_url": "https://github.com/user",
        "talent_level": "A+",
        "migration_potential": 85
      }
    ]
  }'
```

### 3️⃣ 更新候選人備註（儲存爬蟲結果）

```bash
curl -X PUT "https://backendstep1ne.zeabur.app/api/candidates/1" \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "GitHub Issue #123 已聯繫，待回覆"
  }'
```

### 4️⃣ 批量更新評級與評分

```python
# 在 search-plan-executor.py 中
import requests

for recommendation in top_recommendations:
    candidate_id = recommendation['id']
    score_data = {
        'talent_level': recommendation['talent_level'],
        'overall_score': recommendation['overall_score'],
        'migration_potential': recommendation['migration_potential'],
        'strengths': recommendation['strengths'],
        'notes': f"推薦於 {datetime.now().isoformat()}"
    }
    
    response = requests.put(
        f"{API_BASE_URL}/api/candidates/{candidate_id}",
        json=score_data
    )
    
    if response.status_code == 200:
        print(f"✅ 候選人 {candidate_id} 已更新")
```

---

## ⏰ Cron 自動化

### 自動排程設定

**編輯 crontab：**
```bash
crontab -e
```

**加入以下排程：**

```cron
# ==================== Layer 1 搜尋（P0 職缺 - 每週一早上） ====================
0 8 * * 1 source /Users/user/clawd/hr-tools/.env && bash /Users/user/clawd/hr-tools/automated-recruiting-pipeline.sh layer1 >> /tmp/recruiting-pipeline/logs/cron-layer1.log 2>&1

# ==================== Layer 2 搜尋（P1 職缺 - 每週一上午） ====================
0 9 * * 1 source /Users/user/clawd/hr-tools/.env && bash /Users/user/clawd/hr-tools/automated-recruiting-pipeline.sh layer2 >> /tmp/recruiting-pipeline/logs/cron-layer2.log 2>&1

# ==================== 遷移分析（每週五下午） ====================
0 17 * * 5 source /Users/user/clawd/hr-tools/.env && python3 /Users/user/clawd/hr-tools/industry-migration-analyzer.py >> /tmp/recruiting-pipeline/logs/cron-migration.log 2>&1

# ==================== 儀表板生成（每日凌晨） ====================
0 2 * * * source /Users/user/clawd/hr-tools/.env && python3 /Users/user/clawd/hr-tools/industry-analytics-dashboard.py >> /tmp/recruiting-pipeline/logs/cron-dashboard.log 2>&1

# ==================== Telegram 通知（週日報告） ====================
0 20 * * 0 source /Users/user/clawd/hr-tools/.env && bash /Users/user/clawd/hr-tools/send-weekly-report.sh >> /tmp/recruiting-pipeline/logs/cron-telegram.log 2>&1
```

### 驗證 Cron

```bash
# 查看已設定的 cron jobs
crontab -l

# 測試 Layer 1 搜尋（手動執行）
source /Users/user/clawd/hr-tools/.env && \
bash /Users/user/clawd/hr-tools/automated-recruiting-pipeline.sh layer1

# 檢查日誌
tail -f /tmp/recruiting-pipeline/logs/cron-layer1.log
```

---

## 🐛 故障排除

### ❌ 問題：爬蟲找不到候選人

**症狀：**
```
✅ 搜尋 AI 工程師...
❌ 找到 0 位候選人
```

**排查步驟：**

1. **檢查 GitHub Token**
   ```bash
   curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
   # 應返回 200 OK
   ```

2. **檢查關鍵字映射**
   ```bash
   grep -i "AI工程師" /Users/user/clawd/hr-tools/unified-scraper-v4-enhanced.py
   # 確認有 "AI Engineer" 映射
   ```

3. **手動測試爬蟲**
   ```bash
   python3 -c "
   from unified_scraper_v4_enhanced import GitHubScraper
   scraper = GitHubScraper('YOUR_TOKEN')
   results = scraper.search_repositories(
       keywords=['AI', 'Engineer'],
       language='python'
   )
   print(len(results))
   "
   ```

---

### ❌ 問題：評分結果都是 0 分

**症狀：**
```json
{
  "candidates": [
    {"name": "John", "overall_score": 0}
  ]
}
```

**排查步驟：**

1. **檢查候選人 JSON 格式**
   ```python
   # 確保包含必要欄位
   required_fields = [
       'name', 'skills', 'experience_years', 
       'source_industry', 'company_level'
   ]
   ```

2. **驗證評分引擎**
   ```bash
   python3 -c "
   from candidate_scoring_system_v2 import CandidateScoringEngine
   engine = CandidateScoringEngine()
   
   test_candidate = {
       'name': 'Test',
       'skills': ['Python'],
       'experience_years': 5,
       'source_industry': 'internet',
       'company_level': 'large'
   }
   
   score = engine.evaluate_candidate(test_candidate, {})
   print(f'Score: {score.overall_score}')
   "
   ```

---

### ❌ 問題：HTML 儀表板空白

**症狀：**
- 打開 `analytics-dashboard.html` 但圖表不顯示

**排查步驟：**

1. **檢查 Chart.js CDN**
   ```bash
   # 確認檔案中有 CDN 連結
   grep "chart.js" /tmp/recruiting-pipeline/reports/analytics-dashboard.html
   ```

2. **檢查瀏覽器主控台**
   - 打開 DevTools (F12)
   - 查看 Console 標籤有無錯誤
   - 查看 Network 標籤 Chart.js 是否載入

3. **重新生成儀表板**
   ```bash
   python3 /Users/user/clawd/hr-tools/industry-analytics-dashboard.py
   ```

---

### ❌ 問題：Cron 沒有執行

**症狀：**
```bash
crontab -l  # 有設定但沒有執行
tail -f /tmp/recruiting-pipeline/logs/cron-layer1.log  # 無日誌
```

**排查步驟：**

1. **檢查 cron 服務**
   ```bash
   # macOS
   launchctl list | grep cron
   
   # 重啟 cron
   sudo launchctl start com.vixie.cron
   ```

2. **檢查環境變數**
   ```bash
   # Cron 環境可能不同，需要完整路徑
   0 8 * * 1 /usr/bin/python3 /Users/user/clawd/hr-tools/script.py
   ```

3. **增加 verbose 日誌**
   ```bash
   # 在 cron 命令末尾加上
   >> /tmp/recruiting-pipeline/logs/cron-debug.log 2>&1
   
   # 然後檢查
   tail /tmp/recruiting-pipeline/logs/cron-debug.log
   ```

---

## 🔄 與現有系統銜接

### 與 WORKFLOW_AUTO.md 整合

**在 WORKFLOW_AUTO.md 中加入新 Cron 項目：**

```markdown
### ✅ 產業智能人才搜尋（新增）

#### Layer 1 搜尋（P0 職缺）
- **Cron 時間**：每週一 08:00
- **Cron ID**：`[待生成]`
- **功能**：
  - 爬取所有 P0 職缺的候選人
  - 評分 + 推薦 Top 3
  - 生成 HTML 儀表板
- **輸出**：/tmp/recruiting-pipeline/reports/
- **狀態**：運行中 ✅

#### Layer 2 搜尋（P1 職缺）
- **Cron 時間**：每週一 09:00
- **功能**：同上（P1 職缺）
- **狀態**：運行中 ✅

#### 遷移分析（每週五）
- **Cron 時間**：每週五 17:00
- **功能**：
  - 跨產業人才評估
  - 技能遷移能力分析
- **輸出**：/tmp/recruiting-pipeline/reports/migration-analysis.json
- **狀態**：運行中 ✅
```

### 與 Step1ne 前端整合

**在 Step1ne 前端中加入按鈕：**

```javascript
// 顯示最新儀表板
<button onClick={() => window.open('/reports/analytics-dashboard.html')}>
  📊 查看智能評分儀表板
</button>

// 導入推薦人選
<button onClick={() => importRecommendations(recommendationData)}>
  📥 導入推薦人選
</button>
```

### 與 Telegram 群組整合

**在每週日 20:00 發送報告：**

```bash
# send-weekly-report.sh
cat > /Users/user/clawd/hr-tools/send-weekly-report.sh << 'EOF'
#!/bin/bash

source /Users/user/clawd/hr-tools/.env

REPORT_FILE="/tmp/recruiting-pipeline/reports/analytics-report.json"
MESSAGE="📊 本週人才搜尋成果\n\n"
MESSAGE+=$(cat $REPORT_FILE | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f\"✅ 總候選人：{data['summary']['total_candidates']}\")
print(f\"✅ 職缺數：{data['summary']['total_jobs']}\")
print(f\"✅ 遷移潛力：{data['summary']['avg_migration_potential']:.0f}/100\")
")

curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=${TELEGRAM_CHAT_ID}&text=${MESSAGE}"
EOF

chmod +x /Users/user/clawd/hr-tools/send-weekly-report.sh
```

---

## 📊 性能指標

### 預期執行時間

| 操作 | 手動執行 | 備註 |
|------|---------|------|
| 爬蟲（1 職缺） | 5-10 分鐘 | 取決於 API 限制 |
| 評分（100 人） | 30 秒 | 純計算，無網路 I/O |
| 遷移分析 | 1-2 分鐘 | 複雜度 O(n²) |
| 儀表板生成 | 10 秒 | HTML 組合 |
| **完整流程** | **7-15 分鐘** | 並行 2-3 workers |

### 優化建議

```python
# 並行爬蟲（加速 2-3 倍）
workers = 3  # 可調整至 2-5

# SQLite 快取（同職缺重複執行時避免重爬）
USE_CACHE = True

# 批量 API 呼叫（減少網路往返）
BATCH_SIZE = 50  # 每批 50 筆候選人評分

# 增量更新（只爬取新職缺）
INCREMENTAL = True
```

---

## 📚 相關資源

- [爬蟲模組文檔](../README-TALENT-SOURCING.md)
- [SKILL.md](../../SKILL.md) - 獵頭技能完整定義
- [WORKFLOW_AUTO.md](../../WORKFLOW_AUTO.md) - 自動化流程總覽
- [Step1ne API 文檔](https://backendstep1ne.zeabur.app/api/guide)

---

## 🆘 獲取幫助

有問題？

1. **檢查日誌**
   ```bash
   tail -f /tmp/recruiting-pipeline/logs/pipeline-*.log
   ```

2. **提交 Issue**
   ```
   GitHub：https://github.com/jacky6658/step1ne-headhunter-skill/issues
   ```

3. **聯繫 YuQi**
   ```
   Telegram：@YuQi0923_bot
   ```

---

**Happy Recruiting! 🎯**
