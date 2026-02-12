# Step1ne 獵頭顧問 AI 技能庫

完整的獵頭工作自動化工具集，包含爬蟲、履歷管理、客戶開發等核心功能。

---

## 🚀 快速開始

### 核心工具（推薦使用）

#### 1️⃣ **BD 客戶穩定爬蟲** ⭐ NEW
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
├── tools/                       # 🛠️ 工具腳本
│   ├── scraper-stable/         # ⭐ 穩定爬蟲（主力）
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

- Python 3.8+
- gog CLI（Google Sheets 操作）
- agent-browser（網頁自動化）
- OpenClaw（可選，用於整合）

安裝指南：[docs/INSTALL.md](docs/INSTALL.md)

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
