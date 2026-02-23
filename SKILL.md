# Step1ne 獵頭顧問完整技能包

## 📚 這是什麼？

一個完整的 AI 獵頭顧問系統，包含：
- 🛠️ 8 個自動化工具
- 📋 8 個核心功能 Prompts
- 🤖 完整的 BD 客戶開發流程
- 📊 HR 總覽看板（Web 版）
- 🔄 定時任務自動化

**適用對象**：任何 AI Bot（YuQi、Claude、GPT、Gemini 等）

---

## 🧠 模組化架構（2026-02-23 更新）

本技能包採用**模組化架構**，分為三大層級：

### 📦 核心模組（modules/）
可獨立使用的 AI 智慧模組：
- **talent-grading** - 人才評級系統（S/A+/A/B/C）
- **ai-matcher** - AI 配對系統（P0/P1/P2）
- **resume-parser** - 履歷解析與自動歸檔
- **dedup-engine** - 候選人去重引擎
- **learning-engine** - AI 學習系統
- **github-talent-search** - GitHub 人才搜尋
- **linkedin-search** - LinkedIn 爬蟲
- **multi-channel-sourcing** - 多管道整合搜尋

### 📚 訓練文檔（training/）
給新顧問與 AI Bot 的學習資源：
- **PHOEBE-AI-GUIDE.md** - 新顧問訓練指南
- **HEADHUNTER-AI-MODULES.md** - 模組化學習機制
- **ai-collaboration-101.md** - AI 協作基礎（待建立）
- **grading-practice.md** - 評級實戰練習（待建立）
- **search-strategy.md** - 搜尋策略最佳實踐（待建立）

### ⚙️ 自動化流程（workflows/）
端到端的業務流程：
- **auto-collect-candidates.sh** - 自動搜尋候選人
- **auto-bd-send.sh** - 自動發送 BD 信

詳細說明請參考各資料夾的 `README.md`。

---

## 🚀 快速開始

### 1. 安裝工具

```bash
# Clone 此 repo
cd ~/clawd
git clone https://github.com/jacky6658/step1ne-headhunter-skill.git

# 設定執行權限
cd step1ne-headhunter-skill/tools
chmod +x *.sh

# 安裝 gog CLI（Gmail/Google Sheets）
brew install steipete/tap/gogcli

# 授權 Google 帳號
gog auth add aijessie88@step1ne.com --services gmail,drive,sheets
```

### 2. 閱讀技能書

AI Bot 應該依序閱讀：

1. **SKILL.md**（本檔案）- 技能總覽
2. **docs/INSTALL.md** - 完整安裝指南
3. **skills/headhunter/SKILL.md** - 8 個核心功能
4. **skills/headhunter/references/prompts.md** - Prompt 模板
5. **docs/教學-如何教Bot執行定時BD爬蟲.md** - 自動化教學

### 3. 測試工具

```bash
cd ~/clawd/step1ne-headhunter-skill/tools

# 測試 BD 開發信
./bd-outreach.sh preview "測試公司" "您好"

# 測試 JD 管理
./jd-manager.sh list

# 測試完整 BD 流程
./bd-automation.sh auto "AI工程師" 3
```

---

## 📁 目錄結構

```
step1ne-headhunter-skill/
├── SKILL.md                           # 本檔案（技能入口）
├── README.md                          # 快速說明
├── tools/                             # 工具腳本
│   ├── bd-automation.sh               # BD 自動化主流程
│   ├── bd-outreach.sh                 # BD 寄信工具
│   ├── jd-manager.sh                  # JD 管理工具
│   ├── resume-pool.sh                 # 履歷池管理
│   ├── start-dashboard.sh             # 啟動看板
│   ├── scraper-104.py                 # 104 爬蟲
│   ├── fetch-104-website-final.py     # 提取公司網站
│   ├── scrape-contact-from-website.sh # 爬取聯絡方式
│   └── Step1ne公司簡介.pdf             # BD 信附件
├── skills/                            # 技能庫
│   └── headhunter/
│       ├── SKILL.md                   # 8 個核心功能
│       ├── references/
│       │   ├── prompts.md             # Prompt 模板
│       │   ├── email-templates.md     # 郵件模板
│       │   └── workflow.md            # 工作流程
│       └── scripts/                   # 輔助腳本
├── dashboard/                         # Web 看板（Next.js）
│   ├── app/
│   ├── public/
│   └── package.json
├── api/                               # API 服務（Node.js）
│   ├── api-server.js
│   └── package.json
├── docs/                              # 文件
│   ├── INSTALL.md                     # 安裝指南
│   ├── README-JD管理.md
│   ├── README-履歷池.md
│   ├── README-總覽看板.md
│   ├── CRON-BD定時任務規劃.md
│   ├── 教學-如何教Bot執行定時BD爬蟲.md
│   └── 2026-02-10-獵頭專案進度總結.md
└── data/                              # 資料範例
    └── .gitkeep
```

---

## 🎯 核心功能（8 個）

### 1. 人設建立 (Persona Creator)
**功能**：根據 JD 生成候選人畫像
**Prompt**: `skills/headhunter/references/prompts.md#persona`

### 2. 人才搜尋 (Talent Search)
**功能**：在 GitHub/LinkedIn/104 搜尋候選人
**工具**: `scraper-104.py`, `github-talent-search.py`

### 3. 履歷配對分析 (Match Analysis)
**功能**：計算候選人與 JD 的匹配度
**Prompt**: `skills/headhunter/references/prompts.md#match-analysis`

### 4. Outreach 文案 (Outreach Composer)
**功能**：生成個性化招募訊息
**Prompt**: `skills/headhunter/references/prompts.md#outreach`

### 5. 面試準備 (Interview Prep)
**功能**：生成面試問題與評估表
**Prompt**: `skills/headhunter/references/prompts.md#interview`

### 6. JD 生成器 (JD Generator)
**功能**：根據需求生成職缺描述
**工具**: `jd-manager.sh add`
**Prompt**: `skills/headhunter/references/prompts.md#jd-generator`

### 7. 進度總結 (Progress Summary)
**功能**：生成每日/每週進度報告
**Prompt**: `skills/headhunter/references/prompts.md#summary`

### 8. 推薦信 (Recommendation Email)
**功能**：生成候選人推薦信給客戶
**工具**: `bd-outreach.sh send`
**模板**: `skills/headhunter/references/email-templates.md#recommendation`

---

## 🤖 自動化流程

### A. BD 客戶開發
**觸發**：手動或定時（每 1 小時）

```bash
./tools/bd-automation.sh auto "AI工程師" 10
```

**流程**：
1. 搜尋 104 招聘公司 → 找到 10 家
2. 提取公司網站 → 爬取聯絡方式
3. 過濾有效 Email → 準備寄信清單
4. 整理到 Google Sheets → BD客戶開發表
5. 批量寄送合作邀請信 → 間隔 30 秒
6. 回報結果到 Telegram → Topic 364

**資料流**：
```
104 搜尋 → JSON 檔案 → Google Sheets → Gmail 發信 → Telegram 通知
```

### B. 履歷進件自動檢查
**觸發**：定時（每 1 小時）

**流程**：
1. 掃描 `inbox/` 資料夾
2. 檢查 Gmail 收件匣（關鍵字：應徵）
3. 提取履歷資訊
4. 執行配對分析（與所有 JD）
5. 發送通知到 Telegram Topic 4

### C. JD 管理
**手動操作**：

```bash
# 新增職缺
./tools/jd-manager.sh add "AI工程師" "AIJob" "技術部" 2 "80k-120k" "Python、TensorFlow" "3年" "大學" "台北" "招募中"

# 搜尋職缺
./tools/jd-manager.sh search "AI"

# 更新狀態
./tools/jd-manager.sh update 3 "已成交"
```

---

## 📊 Google Sheets 整合

### 需要的 Sheets（3 個）

1. **step1ne 職缺管理**
   - Sheet ID: `1QPaeOm-slNVFCeM8Q3gg3DawKjzp2tYwyfquvdHlZFE`
   - 欄位：職位、客戶公司、部門、人數、薪資、技能、經驗、學歷、地點、狀態、日期

2. **履歷池索引**
   - Sheet ID: `1PunpaDAFBPBL_I76AiRYGXKaXDZvMl1c262SEtxRk6Q`
   - 欄位：姓名、職位、技能、經驗、學歷、履歷連結、來源、狀態、日期

3. **BD客戶開發表**
   - Sheet ID: `1bkI7_cCh_Bs4qVa3HlXiy0CFzmItZlA-DYGHSPS4InE`
   - 欄位：公司名稱、電話、Email、網址、職缺、來源、狀態、日期、負責顧問、備註

**授權設定**：
```bash
gog auth add aiagentg888@gmail.com --services drive,sheets
```

---

## 🔧 定時任務設定

### 使用 OpenClaw Cron

AI Bot 可以使用 `cron` tool 建立定時任務：

#### 1. BD 客戶開發（每 1 小時）
```javascript
{
  "name": "BD 客戶開發定時爬蟲",
  "schedule": {"kind": "every", "everyMs": 3600000},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "執行 ~/clawd/step1ne-headhunter-skill/tools/bd-automation.sh auto \"<關鍵字>\" 10"
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "-1003231629634/364"
  }
}
```

#### 2. 履歷進件檢查（每 1 小時）
```javascript
{
  "name": "履歷進件自動檢查",
  "schedule": {"kind": "every", "everyMs": 3600000},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "掃描 inbox/ 和 Gmail，若有新履歷則執行配對分析並通知"
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "-1003231629634/4"
  }
}
```

詳細規劃：`docs/CRON-BD定時任務規劃.md`

---

## 🎓 學習路徑（給 AI Bot）

### 第一次使用

1. **閱讀 SKILL.md**（本檔案）
2. **執行安裝**（`docs/INSTALL.md`）
3. **手動測試所有工具**（確保能正常運作）
4. **閱讀 Prompt 模板**（`skills/headhunter/references/prompts.md`）
5. **執行一次完整 BD 流程**（手動）
6. **設定定時任務**（自動化）

### 第二次使用（已熟悉）

1. **檢查 Google Sheets 授權**
2. **檢查 Gmail 授權**
3. **直接執行自動化流程**

### 教其他 Bot

使用 `docs/教學-如何教Bot執行定時BD爬蟲.md`

---

## 📞 Telegram 整合

### 群組與 Topics

- **HR AI招募自動化** (`-1003231629634`)
  - Topic 4: 履歷進件
  - Topic 304: 履歷池
  - Topic 364: 開發（BD）

### 發送訊息

使用 OpenClaw `message` tool：

```javascript
message({
  action: "send",
  channel: "telegram",
  to: "-1003231629634/364",
  message: "✅ BD 客戶開發完成\n• 找到 10 家公司\n• 已寄信 5 家"
})
```

---

## 🧪 測試清單

在正式使用前，確認：

- [ ] gog CLI 已安裝
- [ ] Google 帳號已授權（gmail, drive, sheets）
- [ ] 所有 .sh 檔案可執行
- [ ] Step1ne公司簡介.pdf 存在
- [ ] bd-outreach.sh 預覽成功
- [ ] bd-automation.sh auto 可完整執行
- [ ] jd-manager.sh list 可正常執行
- [ ] Telegram 群組與 Topics 已建立
- [ ] 手動執行 BD 流程至少 1 次成功

---

## 🐛 常見問題

### Q1: 找不到 gog 指令
```bash
brew install steipete/tap/gogcli
```

### Q2: Gmail 授權失敗
```bash
gog auth add aijessie88@step1ne.com --services gmail
# 會開啟瀏覽器登入
```

### Q3: Google Sheets 寫入失敗
```bash
gog auth add aiagentg888@gmail.com --services drive,sheets
```

### Q4: 爬蟲找不到公司
- 檢查 agent-browser 是否已安裝
- 檢查網路連線
- 104 網站可能改版（需更新爬蟲）

### Q5: Telegram 訊息發送失敗
- 檢查 Topic ID 是否正確
- 檢查 Bot 是否在群組中
- 檢查 Bot 是否有發言權限

---

## 🔄 更新與維護

### 從 openclaw-backup 同步最新版本

```bash
cd ~/clawd/step1ne-headhunter-skill

# 同步工具腳本
cp ~/clawd/hr-tools/*.sh ./tools/
cp ~/clawd/hr-tools/*.py ./tools/
cp ~/clawd/hr-tools/*.pdf ./tools/

# 同步技能庫
cp -r ~/clawd/skills/headhunter/* ./skills/headhunter/

# 同步文件
cp ~/clawd/hr-tools/README*.md ./docs/
cp ~/clawd/hr-tools/INSTALL.md ./docs/
cp ~/clawd/hr-tools/*.md ./docs/

# 提交更新
git add .
git commit -m "sync: 同步最新版本 $(date +%Y-%m-%d)"
git push
```

### 自動同步（可選）

在 openclaw-backup 的每日備份後觸發同步。

---

## 📈 成效追蹤

### 建議指標

1. **BD 開發**
   - 每週搜尋公司數
   - 每週寄信數
   - 回覆率
   - 轉換率（成功合作數）

2. **履歷配對**
   - 每週進件數
   - 配對成功率（≥90%）
   - 推薦數
   - 面試數

3. **成交**
   - 每月成交數
   - 平均成交週期
   - 客戶滿意度

---

## 📚 延伸閱讀

- [完整指南](https://jacky6658.github.io/aijob-presentations/headhunter-full-guide.html)
- [員工手冊](https://jacky6658.github.io/aijob-presentations/step1ne-operations-manual.html)
- [OpenClaw 文件](https://docs.openclaw.ai)
- [ClawHub 技能市集](https://clawhub.com)

---

## 🤝 貢獻

如果你在使用過程中發現問題或有改進建議：
1. 提交 Issue
2. 或直接發 PR

---

## 📄 授權

MIT License

---

**建立日期**: 2026-02-10
**維護者**: YuQi (@YuQi0923_bot)
**版本**: 1.0.0
