# 🎯 人才智能爬蟲系統 - 快速參考

**位置**：`/Users/user/clawd/hr-tools/`

---

## 📂 包含的 5 個模組

| 檔案 | 功能 | 輸入 | 輸出 |
|------|------|------|------|
| `unified-scraper-v4-enhanced.py` | 產業感知並行爬蟲 | 職缺 + 技能 | 候選人 JSON |
| `candidate-scoring-system-v2.py` | 6 維度評分引擎 | 候選人 | 評分 (S/A+/A/B) |
| `industry-migration-analyzer.py` | 遷移能力分析 | 候選人 + 職缺 | 遷移潛力評分 |
| `search-plan-executor.py` | 端到端協調器 | 職缺列表 | 推薦清單 |
| `industry-analytics-dashboard.py` | 可視化儀表板 | 評分結果 | HTML + JSON |

---

## 🚀 快速開始（3 步驟）

### 1️⃣ 環境設定

```bash
# 複製環境檔案模板
cp /Users/user/clawd/hr-tools/.env.example \
   /Users/user/clawd/hr-tools/.env

# 編輯 .env，填入 API tokens
nano /Users/user/clawd/hr-tools/.env

# 載入環境變數
source /Users/user/clawd/hr-tools/.env
```

### 2️⃣ 執行爬蟲

```bash
cd /Users/user/clawd/hr-tools

# 完整流程（推薦）
python3 search-plan-executor.py \
  --job-title "AI工程師" \
  --industry "internet" \
  --required-skills "Python,機器學習"

# 或使用自動化腳本
bash automated-recruiting-pipeline.sh layer1
```

### 3️⃣ 查看結果

```bash
# HTML 儀表板
open /tmp/recruiting-pipeline/reports/analytics-dashboard.html

# JSON 報告
cat /tmp/recruiting-pipeline/reports/analytics-report.json

# 日誌檔案
tail /tmp/recruiting-pipeline/logs/pipeline-*.log
```

---

## 🔧 常見操作

### 只執行爬蟲

```bash
python3 unified-scraper-v4-enhanced.py \
  --job-id 1 \
  --keywords "Python,Go,Kubernetes"
```

### 只執行評分

```bash
python3 -c "
from candidate_scoring_system_v2 import CandidateScoringEngine
engine = CandidateScoringEngine()
# ... 評分代碼
"
```

### 產生儀表板

```bash
python3 industry-analytics-dashboard.py \
  --input /tmp/recruiting-pipeline/reports/analytics-report.json \
  --output /tmp/recruiting-pipeline/reports/analytics-dashboard.html
```

---

## ⏰ 自動化排程

```bash
# 查看 Cron 設定
crontab -l

# 編輯 Cron
crontab -e

# 預設排程：
# 週一 08:00 - Layer 1 搜尋 (P0 職缺)
# 週一 09:00 - Layer 2 搜尋 (P1 職缺)
# 週五 17:00 - 遷移能力分析
```

詳細設定見 → [INTEGRATION-GUIDE.md](INTEGRATION-GUIDE.md#cron-自動化)

---

## 📍 檔案位置

```
爬蟲腳本：
/Users/user/clawd/hr-tools/

輸出報告：
/tmp/recruiting-pipeline/reports/
  ├─ analytics-dashboard.html  ← 開啟這個看儀表板
  ├─ analytics-report.json
  └─ recommendations.json

日誌：
/tmp/recruiting-pipeline/logs/
  ├─ pipeline-YYYYMMDD.log
  ├─ cron-layer1.log
  ├─ cron-layer2.log
  └─ cron-migration.log
```

---

## 🐛 出問題怎麼辦

| 問題 | 解法 |
|------|------|
| 找不到候選人 | ✓ 檢查 GitHub Token / 關鍵字映射 |
| 評分都是 0 | ✓ 檢查候選人 JSON 格式 |
| HTML 空白 | ✓ 檢查 Chart.js CDN 連線 |
| Cron 沒執行 | ✓ 檢查環境變數 + 完整路徑 |

詳細排除步驟見 → [INTEGRATION-GUIDE.md](INTEGRATION-GUIDE.md#-故障排除)

---

## 📚 完整文檔

想深入了解？看 → [INTEGRATION-GUIDE.md](INTEGRATION-GUIDE.md)

內容包括：
- ✅ 系統架構與數據流
- ✅ API 整合點
- ✅ Cron 自動化設定
- ✅ 與現有系統銜接
- ✅ 性能優化

---

## 📞 需要幫助

- **GitHub Issues**：https://github.com/jacky6658/step1ne-headhunter-skill/issues
- **Telegram**：@YuQi0923_bot
- **郵件**：step1nework016@gmail.com

---

**Happy Recruiting! 🎯**
