# Step1ne Bot 訓練中心 🤖

**目的**: 為專門任務的 AI Bot 提供完整訓練文檔與工作流程  
**適用對象**: 新 Bot、替代 Bot、升級現有 Bot

---

## 🎯 Bot 訓練哲學

每個 Bot 都是**專門化的 AI 助理**，負責單一明確的任務：
- ✅ **職責清晰**：只做一件事，做到最好
- ✅ **獨立運作**：完成訓練後可以獨立執行任務
- ✅ **標準化流程**：所有 Bot 使用相同的訓練架構
- ✅ **可替換性**：Bot 失效時可以快速訓練替代者

---

## 🤖 可用的 Bot

### 1. Sourcing Bot 🔍

**職責**: LinkedIn + GitHub 人才搜尋自動化  
**執行時間**: 每天 3 次（09:00, 14:00, 20:00）  
**訓練時間**: 30 分鐘  
**狀態**: ✅ 已完成訓練文檔

**主要功能**:
- 從 LinkedIn 公開搜尋候選人（不需付費帳號）
- 從 GitHub 搜尋技術人才（技能自動推斷）
- AI 自動配對評分（P0/P1/P2）
- 去重後匯入履歷池
- Telegram 通知獵頭

**文檔**: [sourcing-bot/](sourcing-bot/)

**快速開始**:
```bash
cd sourcing-bot
cat README.md
```

---

### 2. BD Bot 📧 (規劃中)

**職責**: BD 客戶開發郵件自動化  
**執行時間**: 每天 2 次（09:30, 14:30）  
**訓練時間**: 20 分鐘  
**狀態**: ⏳ 規劃中

**主要功能**:
- 自動從 BD客戶開發表讀取「待寄信」狀態的公司
- 生成個性化 BD 郵件
- 自動發送郵件
- 更新狀態為「已寄信」
- 7 天後自動發送追蹤信

**文檔**: 🚧 待建立

---

### 3. Resume Bot 📄 (規劃中)

**職責**: 履歷自動解析與歸檔  
**執行時間**: 每小時  
**訓練時間**: 15 分鐘  
**狀態**: ⏳ 規劃中

**主要功能**:
- 監控 Gmail inbox 新履歷（aijessie88@step1ne.com）
- 監控 Telegram PDF 上傳（Topic 4）
- 自動解析履歷（PDF → 結構化資料）
- 匯入履歷池
- 發送 Telegram 通知

**文檔**: 🚧 待建立

---

## 📚 訓練流程

### 標準訓練流程（30 分鐘）

```
第 1 步：閱讀 README.md（5 分鐘）
  ↓
第 2 步：完成 TRAINING.md（20 分鐘）
  ↓
第 3 步：執行 CHECKLIST.md（5 分鐘）
  ↓
第 4 步：通過測試 → 上線！
```

### 每個 Bot 的標準資料夾結構

```
bots/<bot-name>/
├── README.md               # 快速開始（5 分鐘）
├── TRAINING.md             # 完整訓練（30 分鐘）
├── CHECKLIST.md            # 上線前檢查清單
├── troubleshooting.md      # 故障排除指南
│
├── workflows/              # 工作流程腳本
│   ├── main-workflow.sh
│   ├── sub-workflow-1.sh
│   └── cron-setup.sh
│
├── examples/               # 使用範例
│   ├── sample-input.json
│   ├── sample-output.json
│   └── sample-cron.txt
│
└── config/                 # 配置檔
    ├── config.example.json
    └── keywords.json
```

---

## 🎓 Bot 訓練最佳實踐

### 1. 先測試，再上線

```bash
# 永遠先執行測試模式
bash workflows/main-workflow.sh --test

# 確認無誤後才執行正式模式
bash workflows/main-workflow.sh
```

### 2. 完整閱讀文檔

- ✅ README.md（快速開始）
- ✅ TRAINING.md（完整訓練）
- ✅ CHECKLIST.md（上線前檢查）
- ✅ troubleshooting.md（故障排除）

### 3. 理解你的職責

**你的任務**：
- ✅ 執行指定的自動化工作流程
- ✅ 處理錯誤並記錄日誌
- ✅ 發送通知給人類獵頭

**你不需要做**：
- ❌ 超出職責範圍的任務
- ❌ 修改其他 Bot 的配置
- ❌ 人類決策（只負責執行）

### 4. 監控與優化

**每日監控**：
- 檢查 Cron 是否按時執行
- 檢查執行結果是否正常
- 檢查通知是否成功發送

**每週優化**：
- 調整搜尋關鍵字
- 優化 AI 配對門檻
- 改進通知格式

---

## 🆘 需要幫助？

### 訓練相關問題

**新 Bot 不知道從何開始？**
1. 選擇要訓練的 Bot（例：Sourcing Bot）
2. 進入該 Bot 的資料夾
3. 閱讀 README.md
4. 完成 TRAINING.md
5. 執行 CHECKLIST.md

**訓練過程中遇到問題？**
1. 查看該 Bot 的 troubleshooting.md
2. 查看系統文檔：[docs/OPENCLAW-INTEGRATION.md](../docs/OPENCLAW-INTEGRATION.md)
3. 查看模組文檔：[training/HEADHUNTER-AI-MODULES.md](../training/HEADHUNTER-AI-MODULES.md)

### 系統連接問題

**OpenClaw 連接失敗？**
- 參考：[docs/OPENCLAW-INTEGRATION.md](../docs/OPENCLAW-INTEGRATION.md)

**Google Sheets 認證過期？**
```bash
gog auth add aijessie88@step1ne.com
```

**GitHub Token 未設定？**
```bash
export GITHUB_TOKEN="ghp_xxx..."
```

### 執行問題

**Cron 沒有按時執行？**
```bash
# 檢查 Cron 狀態
openclaw cron list | grep "<Bot 名稱>"

# 手動執行測試
openclaw cron run <CRON_ID>
```

**執行失敗？**
1. 查看日誌：`tail -f /tmp/<bot-name>.log`
2. 查看 troubleshooting.md
3. 手動執行腳本：`bash workflows/main-workflow.sh --test --verbose`

---

## 📈 Bot 效能指標

### Sourcing Bot
- 每次執行找到 10-30 位候選人
- P0+P1 候選人佔比 > 30%
- 去重率 < 20%
- 執行時間 < 5 分鐘

### BD Bot（規劃中）
- 每次執行發送 10-20 封郵件
- 郵件發送成功率 > 95%
- 執行時間 < 3 分鐘

### Resume Bot（規劃中）
- 每小時處理 5-10 份履歷
- 解析成功率 > 90%
- 執行時間 < 2 分鐘

---

## 🔗 相關資源

### 系統文檔
- [OpenClaw 連接指南](../docs/OPENCLAW-INTEGRATION.md)
- [AI 模組使用手冊](../training/HEADHUNTER-AI-MODULES.md)
- [新手上手指南](../training/PHOEBE-AI-GUIDE.md)

### 模組文檔
- [AI 配對系統](../modules/ai-matcher/README.md)
- [人才評級系統](../modules/talent-grading/README.md)
- [履歷解析器](../modules/resume-parser/README.md)

### GitHub 倉庫
- **技能倉庫**: https://github.com/jacky6658/step1ne-headhunter-skill
- **系統倉庫**: https://github.com/jacky6658/step1ne-headhunter-system

---

## 💡 設計理念

### 為什麼需要專門的 Bot？

**問題**：
- 單一 AI 助理負責所有任務 → 職責過重、容易出錯
- Cron 任務失敗時難以追蹤原因
- 更換 AI 助理時需要重新訓練所有任務

**解決方案**：
- 每個 Bot 專注單一任務 → 職責清晰、易於維護
- 獨立的訓練文檔 → 可快速訓練替代 Bot
- 標準化的架構 → 所有 Bot 使用相同的訓練流程

### 為什麼需要訓練文檔？

**問題**：
- AI 助理沒有長期記憶 → 每次重啟都會忘記
- 口頭指示容易遺漏細節 → 導致執行錯誤
- 經驗無法傳承 → 新 Bot 需要重新學習

**解決方案**：
- 完整的訓練文檔 → AI 可以自學
- 標準化的檢查清單 → 確保所有步驟都完成
- 故障排除指南 → 常見問題有解決方案

---

**最後更新**: 2026-02-23  
**版本**: v1.0.0  
**維護者**: YuQi AI Assistant
