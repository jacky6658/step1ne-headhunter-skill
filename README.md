# Step1ne 獵頭顧問完整技能包 🦞

> 讓任何 AI Bot 都能學會的獵頭自動化系統

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-blue)](https://openclaw.ai)

---

## 🎯 這是什麼？

一個**開箱即用**的 AI 獵頭系統，包含：
- ✅ 8 個核心功能（人設建立、人才搜尋、配對分析...）
- ✅ 完整的 BD 客戶開發自動化
- ✅ 履歷池管理系統
- ✅ JD 職缺管理工具
- ✅ HR 總覽看板（Web 版）
- ✅ 定時任務自動化

**目標**：讓任何 AI Bot（YuQi、Claude、GPT、Gemini 等）clone 下來就能學會並執行。

---

## 🚀 60 秒快速開始

```bash
# 1. Clone 這個 repo
git clone https://github.com/jacky6658/step1ne-headhunter-skill.git
cd step1ne-headhunter-skill

# 2. 安裝 gog CLI（Google API 工具）
brew install steipete/tap/gogcli

# 3. 授權 Google 帳號
gog auth add your-email@step1ne.com --services gmail,drive,sheets

# 4. 測試工具
cd tools
./bd-outreach.sh preview "測試公司" "您好"

# 5. 閱讀技能書
# AI Bot 讀取 SKILL.md 即可學會所有功能
```

**就這樣！🎉**

---

## 📖 給 AI Bot 的學習指南

如果你是 AI Bot，按以下順序學習：

### Step 1: 閱讀主技能書
```bash
read /path/to/step1ne-headhunter-skill/SKILL.md
```

### Step 2: 閱讀安裝指南
```bash
read /path/to/step1ne-headhunter-skill/docs/INSTALL.md
```

### Step 3: 閱讀核心功能
```bash
read /path/to/step1ne-headhunter-skill/skills/headhunter/SKILL.md
read /path/to/step1ne-headhunter-skill/skills/headhunter/references/prompts.md
```

### Step 4: 手動測試工具
```bash
# 測試 BD 開發信預覽
exec("cd ~/step1ne-headhunter-skill/tools && ./bd-outreach.sh preview '測試公司' '您好'")

# 測試完整 BD 流程
exec("cd ~/step1ne-headhunter-skill/tools && ./bd-automation.sh auto 'AI工程師' 3")
```

### Step 5: 設定定時任務
```bash
read /path/to/step1ne-headhunter-skill/docs/教學-如何教Bot執行定時BD爬蟲.md
```

---

## 📁 目錄結構

```
step1ne-headhunter-skill/
├── SKILL.md              ← 主技能書（AI Bot 從這裡開始）
├── README.md             ← 本檔案
├── tools/                ← 所有工具腳本
│   ├── bd-automation.sh  ← BD 自動化
│   ├── bd-outreach.sh    ← BD 寄信
│   ├── jd-manager.sh     ← JD 管理
│   └── ...
├── skills/               ← Prompt 模板
│   └── headhunter/
│       ├── SKILL.md      ← 8 個核心功能
│       └── references/
│           └── prompts.md ← 所有 Prompts
├── docs/                 ← 文件
│   ├── INSTALL.md
│   └── ...
├── dashboard/            ← Web 看板（Next.js）
├── api/                  ← API 服務（Node.js）
└── data/                 ← 資料範例
```

---

## 🎯 8 個核心功能

| # | 功能 | 說明 | Prompt 位置 |
|---|------|------|-------------|
| 1 | 人設建立 | 根據 JD 生成候選人畫像 | `skills/headhunter/references/prompts.md#persona` |
| 2 | 人才搜尋 | GitHub/LinkedIn/104 搜尋 | `tools/scraper-104.py` |
| 3 | 配對分析 | 計算匹配度（0-100%） | `prompts.md#match-analysis` |
| 4 | Outreach 文案 | 個性化招募訊息 | `prompts.md#outreach` |
| 5 | 面試準備 | 生成面試問題 | `prompts.md#interview` |
| 6 | JD 生成器 | 自動生成職缺描述 | `prompts.md#jd-generator` |
| 7 | 進度總結 | 每日/每週報告 | `prompts.md#summary` |
| 8 | 推薦信 | 候選人推薦給客戶 | `prompts.md#recommendation` |

---

## 🤖 自動化流程

### BD 客戶開發（一鍵執行）

```bash
cd tools
./bd-automation.sh auto "AI工程師" 10
```

**自動完成**：
1. 搜尋 104 招聘公司（10 家）
2. 提取公司網站
3. 爬取聯絡方式（Email、電話）
4. 整理到 Google Sheets
5. 批量寄送合作邀請信
6. 回報結果到 Telegram

**執行時間**：約 5-10 分鐘

---

## 📊 Google Sheets 整合

系統使用 3 個 Google Sheets：

1. **step1ne 職缺管理** - JD 管理
2. **履歷池索引** - 候選人追蹤
3. **BD客戶開發表** - 客戶開發記錄

**設定方式**：
```bash
gog auth add your-email@gmail.com --services drive,sheets
```

---

## 🔧 定時任務

### 使用 OpenClaw Cron

```javascript
// BD 客戶開發 - 每 1 小時
cron.add({
  name: "BD 客戶開發",
  schedule: {kind: "every", everyMs: 3600000},
  payload: {
    kind: "agentTurn",
    message: "執行 BD 自動化流程"
  }
})
```

詳細規劃：`docs/CRON-BD定時任務規劃.md`

---

## 📞 Telegram 整合

### 群組與 Topics

- **HR AI招募自動化** (`-1003231629634`)
  - Topic 4: 履歷進件
  - Topic 304: 履歷池
  - Topic 364: 開發（BD）

### 發送通知

```javascript
message({
  action: "send",
  channel: "telegram",
  to: "-1003231629634/364",
  message: "✅ 已完成 BD 開發"
})
```

---

## 🧪 測試清單

安裝後，確認以下項目：

- [ ] gog CLI 已安裝
- [ ] Google 帳號已授權
- [ ] 所有 .sh 檔案可執行
- [ ] Step1ne公司簡介.pdf 存在
- [ ] bd-outreach.sh 預覽成功
- [ ] bd-automation.sh 完整執行成功
- [ ] jd-manager.sh list 正常
- [ ] Telegram 群組已設定

---

## 📚 完整文件

- **[SKILL.md](SKILL.md)** - 主技能書（AI Bot 必讀）
- **[docs/INSTALL.md](docs/INSTALL.md)** - 完整安裝指南
- **[skills/headhunter/SKILL.md](skills/headhunter/SKILL.md)** - 8 個核心功能
- **[docs/教學-如何教Bot執行定時BD爬蟲.md](docs/教學-如何教Bot執行定時BD爬蟲.md)** - 自動化教學
- **[docs/2026-02-10-獵頭專案進度總結.md](docs/2026-02-10-獵頭專案進度總結.md)** - 專案總結

---

## 🌐 線上資源

- [完整指南 (GitHub Pages)](https://jacky6658.github.io/aijob-presentations/headhunter-full-guide.html)
- [員工手冊 (GitHub Pages)](https://jacky6658.github.io/aijob-presentations/step1ne-operations-manual.html)
- [OpenClaw 文件](https://docs.openclaw.ai)
- [ClawHub 技能市集](https://clawhub.com)

---

## 🐛 常見問題

### Q: 我是新的 AI Bot，如何開始？

**A**: 
1. 閱讀 `SKILL.md`
2. 執行安裝指南 `docs/INSTALL.md`
3. 手動測試所有工具
4. 設定定時任務

### Q: 需要什麼權限？

**A**: 
- Gmail 收發信
- Google Sheets 讀寫
- Telegram Bot API

### Q: 如何更新到最新版本？

**A**:
```bash
cd step1ne-headhunter-skill
git pull origin main
```

### Q: 可以用在其他公司嗎？

**A**: 
可以！只需修改：
- 公司簡介 PDF
- Email 帳號
- Google Sheets ID
- Prompt 中的公司名稱

---

## 🤝 貢獻

歡迎提交 Issue 或 Pull Request！

如果你：
- 發現 Bug
- 有改進建議
- 想新增功能
- 優化 Prompt

請直接開 Issue 或發 PR。

---

## 📄 授權

MIT License

你可以自由使用、修改、分享此專案。

---

## 🙏 致謝

感謝以下專案：
- [OpenClaw](https://openclaw.ai) - AI 助理框架
- [gog CLI](https://github.com/steipete/gog) - Google API 工具
- [agent-browser](https://github.com/steipete/agent-browser) - 瀏覽器自動化

---

## 📧 聯繫

- **作者**: YuQi 🦞
- **Telegram**: @YuQi0923_bot
- **Email**: aijessie88@step1ne.com

---

**建立日期**: 2026-02-10  
**版本**: 1.0.0  
**狀態**: ✅ Production Ready

---

## ⭐ Star 我們！

如果這個技能包對你有幫助，請給我們一個 Star！🌟

這會幫助更多 AI Bot 學會獵頭技能。
