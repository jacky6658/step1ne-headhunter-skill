# Step1ne 獵頭顧問 AI 技能庫

完整的獵頭工作自動化工具集，包含爬蟲、履歷管理、客戶開發等核心功能。

---

## 🚀 快速開始

### 核心工具（推薦使用）

#### 🎯 **人才智能爬蟲系統** ⭐ NEWEST (2026-02-26)
產業感知並行爬蟲 + 6 維評分系統 + 遷移能力分析 + 智能儀表板

📁 位置：[`scripts/talent-sourcing/`](scripts/talent-sourcing/)  
📖 快速參考：[README](docs/talent-sourcing/README-TALENT-SOURCING.md)  
📖 完整指南：[INTEGRATION-GUIDE](docs/talent-sourcing/INTEGRATION-GUIDE.md)

```bash
# 快速開始
cd /Users/user/clawd/hr-tools
source .env

# 執行完整人才搜尋流程
python3 search-plan-executor.py \
  --job-title "AI工程師" \
  --industry "internet" \
  --required-skills "Python,機器學習"

# 查看結果
open /tmp/recruiting-pipeline/reports/analytics-dashboard.html
```

**特色：**
- ✅ 並行爬蟲（2-5 workers，5-10 分鐘搜尋 100+ 候選人）
- ✅ 6 維評分系統（技能 + 經驗 + 地點 + 訊號 + 公司 + 產業）
- ✅ 產業遷移能力矩陣（跨產業人才評估）
- ✅ HTML 互動儀表板（Chart.js 圖表 + 表格）
- ✅ 自動 Cron 排程（週期自動執行）
- ✅ 50 倍效率提升（6+ 小時 → 7 分鐘）

---

#### 1️⃣ **BD 客戶穩定爬蟲** ⭐ STABLE
自動抓取公司聯絡資訊（電話、Email），穩定可靠，100% 測試通過。

📁 位置：[`tools/scraper-stable/`](tools/scraper-stable/)  
📖 文檔：[README](tools/scraper-stable/README.md)

```bash
cd tools/scraper-stable
cp config.example.json config.json
# 編輯 config.json
bash run-scraper.sh start
```

**特色：**
- ✅ 斷點續爬（隨時暫停/繼續）
- ✅ 自動重試（失敗最多3次）
- ✅ 實時進度報告
- ✅ 100% 成功率實測

---

#### 2️⃣ **履歷池管理**
自動處理履歷進件、匹配職缺、通知顧問。

📖 文檔：[docs/README-履歷池.md](docs/README-履歷池.md)

---

#### 3️⃣ **JD 職缺管理**
職缺的新增、搜尋、統計。

📖 文檔：[docs/README-JD管理.md](docs/README-JD管理.md)

---

#### 4️⃣ **BD 自動化**
客戶開發郵件自動化。

📖 文檔：[docs/README-BD自動化.md](docs/README-BD自動化.md)

---

## 📂 檔案結構

```
step1ne-headhunter-skill/
├── README.md                    # 👈 你在這裡
├── SKILL.md                     # OpenClaw 技能定義
├── PHOEBE-AI-GUIDE.md          # 新手上手指南
│
├── scripts/                     # 📜 Python 爬蟲腳本
│   ├── talent-sourcing/        # ⭐⭐⭐ 人才智能爬蟲系統 (NEW)
│   │   ├── unified-scraper-v4-enhanced.py        # 產業感知並行爬蟲
│   │   ├── candidate-scoring-system-v2.py        # 6D 評分系統
│   │   ├── industry-migration-analyzer.py        # 遷移能力分析
│   │   ├── search-plan-executor.py               # 端到端協調器
│   │   └── industry-analytics-dashboard.py       # 儀表板生成
│   │
│   ├── auto-resume-filing.sh   # 履歷自動歸檔
│   └── other-scripts/
│
├── tools/                       # 🛠️ Bash 工具
│   ├── scraper-stable/         # ⭐ 穩定爬蟲（BD 客戶）
│   │   ├── main.py
│   │   ├── config.example.json
│   │   ├── run-scraper.sh
│   │   └── README.md
│   │
│   ├── bd-automation.sh        # BD 全自動化
│   ├── bd-outreach.sh          # BD 郵件發送
│   ├── jd-manager.sh           # JD 管理
│   ├── resume-pool.sh          # 履歷池
│   └── start-dashboard.sh      # 總覽看板
│
├── docs/                        # 📚 文檔
│   ├── INSTALL.md              # 環境安裝
│   ├── talent-sourcing/        # ⭐ 人才爬蟲文檔
│   │   ├── README-TALENT-SOURCING.md       # 快速參考
│   │   └── INTEGRATION-GUIDE.md            # 完整整合指南
│   │
│   ├── README-履歷池.md
│   ├── README-JD管理.md
│   ├── README-BD自動化.md
│   └── README-總覽看板.md
│
├── skills/                      # 技能腳本（舊版）
│   └── headhunter/
│
└── archive/                     # 📦 舊版工具
    └── old-tools/
```

---

## 📖 完整文檔

### 新手入門
- [安裝指南](docs/INSTALL.md) - 環境設置、依賴安裝
- [Phoebe AI 上手指南](PHOEBE-AI-GUIDE.md) - 3天快速上手

### 功能文檔
- [履歷池管理](docs/README-履歷池.md) - 履歷進件、匹配、通知
- [JD 職缺管理](docs/README-JD管理.md) - 職缺 CRUD、搜尋
- [BD 自動化](docs/README-BD自動化.md) - 客戶開發郵件
- [總覽看板](docs/README-總覽看板.md) - Pipeline 視覺化

### 進階
- [CRON 定時任務規劃](docs/CRON-BD定時任務規劃.md)
- [教學：如何教 Bot 執行定時 BD 爬蟲](docs/教學-如何教Bot執行定時BD爬蟲.md)

### AI 整合（內部使用）
- [**OpenClaw AI 連接指南**](docs/OPENCLAW-INTEGRATION.md) ⭐ NEW
  - 如何讓 AI 助理（YuQi、Phoebe）連接 Step1ne 系統
  - API 端點說明、認證方式、使用範例
  - 人才評級系統整合
  - 完整的故障排除指南

---

## 🎯 使用場景

### 場景 1：開發新客戶
```bash
# 1. 抓取公司聯絡資訊
cd tools/scraper-stable
bash run-scraper.sh start 50

# 2. 自動發送 BD 郵件
bash ../bd-outreach.sh
```

### 場景 2：處理履歷
```bash
# 自動匹配職缺並通知
bash tools/resume-pool.sh
```

### 場景 3：管理職缺
```bash
# 列出所有職缺
bash tools/jd-manager.sh list

# 搜尋特定職缺
bash tools/jd-manager.sh search "工程師"
```

---

## ⚙️ 系統需求

### 後端 / 爬蟲 / 自動化工具
- Python 3.8+
- gog CLI（Google Sheets 操作）
- agent-browser（網頁自動化）
- OpenClaw（可選，用於整合）

安裝指南：[docs/INSTALL.md](docs/INSTALL.md)

### 前端系統（AI 配對、看板、PDF 匯出）
- Node.js 18+
- React 18+
- **jsPDF + jspdf-autotable**（PDF 生成）⭐ **重要！**

完整前端依賴清單：[docs/FRONTEND-DEPENDENCIES.md](docs/FRONTEND-DEPENDENCIES.md)

---

## 📊 實測數據

**BD 爬蟲（2026-02-12）：**
- 處理速度：12 秒/家
- 成功率：100%（65/65）
- 247 家預計：約 50 分鐘

---

## 🤝 貢獻

歡迎提交 Issue 或 Pull Request！

---

## 📝 更新日誌

### 2026-02-26 ⭐ MAJOR UPDATE
- ✅ **人才智能爬蟲系統 v1.0** 發布
  - ✅ `unified-scraper-v4-enhanced.py` - 產業感知並行爬蟲 (15 KB)
  - ✅ `candidate-scoring-system-v2.py` - 6D 評分系統 (19 KB)
  - ✅ `industry-migration-analyzer.py` - 遷移能力分析 (13 KB)
  - ✅ `search-plan-executor.py` - 端到端協調器 (12 KB)
  - ✅ `industry-analytics-dashboard.py` - 智能儀表板 (17 KB)
- ✅ 完整整合文檔（INTEGRATION-GUIDE.md）
- ✅ Cron 自動化排程方案
- ✅ 50 倍效率提升（6+ 小時 → 7 分鐘）

### 2026-02-12
- ✅ 新增 `scraper-stable` 穩定爬蟲系統
- ✅ 整理倉庫結構
- ✅ 更新 README

### 2026-02-11
- ✅ 初版發布

---

## 📄 授權

MIT License

---

## 👥 作者

Jacky Chen x YuQi 🦞

**聯絡方式：** jacky051285@yahoo.com.tw
