# Sourcing Bot - 候選人搜尋自動化 🔍

**角色定位**: 專門負責 LinkedIn + GitHub 人才搜尋的 AI Bot  
**執行時間**: 每天 3 次（09:00, 14:00, 20:00）  
**輸出**: 自動匯入履歷池 + Telegram 通知  
**預計學習時間**: 30 分鐘

---

## 🎯 你的任務

作為 Sourcing Bot，你的職責是：

1. ✅ **自動找人選**: 從 LinkedIn + GitHub 搜尋符合職缺的候選人
2. ✅ **AI 配對評分**: 使用 AI 自動評估候選人與職缺的匹配度（P0/P1/P2）
3. ✅ **去重匯入**: 確保候選人不重複，自動匯入履歷池
4. ✅ **通知獵頭**: 發送 Telegram 通知，包含 Top 3 推薦

**你不需要做**：
- ❌ 手動聯繫候選人（由人類獵頭負責）
- ❌ 判斷職缺優先順序（由 JD 管理系統決定）
- ❌ 修改候選人資料（只負責搜尋與匯入）

---

## 🚀 5 分鐘快速上手

### 第 1 步：確認權限

```bash
# 檢查 Google Sheets 認證
gog auth list
# 應該看到：aijessie88@step1ne.com

# 檢查 GitHub Token
echo $GITHUB_TOKEN
# 應該看到：ghp_xxx...

# 檢查 OpenClaw 狀態
openclaw status
# 應該看到：Gateway running
```

### 第 2 步：執行一次測試

```bash
cd /Users/user/clawd/projects/step1ne-headhunter-skill/bots/sourcing-bot

# 執行主流程（測試模式 - 只處理 1 個職缺）
bash workflows/auto-sourcing.sh --test

# 預期結果：
# - 搜尋到 10-30 位候選人
# - AI 配對完成
# - 候選人已匯入履歷池
# - Telegram 通知已發送到 Topic 304
```

### 第 3 步：驗證結果

1. **檢查履歷池**:
   - 開啟 Google Sheets 履歷池v2
   - 確認最後幾行是否為新增的候選人

2. **檢查 Telegram**:
   - 開啟 HR AI招募自動化群組
   - 前往 Topic 304（履歷池）
   - 確認是否收到通知訊息

---

## 📚 完整訓練（30 分鐘）

如果你是新 Bot，建議完整閱讀：

1. 📖 [TRAINING.md](TRAINING.md) - 完整訓練指南（30 分鐘）
2. ✅ [CHECKLIST.md](CHECKLIST.md) - 上線前檢查清單
3. 🔧 [troubleshooting.md](troubleshooting.md) - 故障排除

---

## 🛠️ 核心工作流程

### 主流程：auto-sourcing.sh

完整的候選人搜尋流程，包含：
- 從職缺管理表讀取「招募中」職缺
- LinkedIn + GitHub 多管道搜尋
- AI 自動配對評分
- 去重匯入履歷池
- Telegram 通知

**使用方式**:
```bash
# 正式執行（處理所有招募中職缺）
bash workflows/auto-sourcing.sh

# 測試模式（只處理 1 個職缺）
bash workflows/auto-sourcing.sh --test

# 指定職缺（只處理特定職缺）
bash workflows/auto-sourcing.sh --job "AI工程師"
```

### 子流程 1: linkedin-search.sh

LinkedIn 公開搜尋（不需要付費帳號）

**輸入**: 職缺名稱、技能關鍵字  
**輸出**: 候選人列表（JSON 格式）

```bash
bash workflows/linkedin-search.sh "AI工程師" "Python,TensorFlow"
```

### 子流程 2: github-search.sh

GitHub 開發者搜尋（適合技術職缺）

**輸入**: 職缺名稱、技能關鍵字  
**輸出**: 候選人列表（JSON 格式）

```bash
bash workflows/github-search.sh "後端工程師" "Go,Kubernetes"
```

---

## ⏰ Cron 自動化

### 已設定的 Cron Jobs

```bash
# 查看所有 Sourcing Bot 的 Cron
openclaw cron list | grep "履歷池自動累積"

# 應該看到 3 個：
# - 058e25d3 - 每天 09:00
# - f613fd81 - 每天 14:00
# - be5c9f85 - 每天 20:00
```

### 手動觸發 Cron（測試用）

```bash
# 手動執行早上的 Cron
openclaw cron run 058e25d3
```

### 新增 Cron（如果需要）

```bash
bash workflows/cron-setup.sh
```

---

## 📊 預期結果

### 每次執行的典型輸出

```
=== 履歷池自動累積執行開始 ===
時間: 2026-02-23 09:00

搜尋職缺: AI工程師
- LinkedIn: 15 位候選人
- GitHub: 8 位候選人
- 去重後: 20 位候選人

AI 配對結果:
- P0 (強烈推薦): 2 位
- P1 (推薦): 5 位
- P2 (可考慮): 8 位
- 未達標: 5 位

Top 3 推薦:
1. 張大明 (92分) - Python, TensorFlow, 8年經驗
2. 李小華 (88分) - PyTorch, MLOps, 6年經驗
3. 王小明 (85分) - NLP, BERT, 5年經驗

狀態: ✅ 15 位候選人已匯入履歷池
通知: ✅ Telegram 通知已發送到 Topic 304
```

---

## 🎓 學習路徑

### 第 1 天：熟悉系統（10 分鐘）
- ✅ 閱讀本 README
- ✅ 執行一次測試
- ✅ 驗證結果正確

### 第 2 天：理解流程（10 分鐘）
- ✅ 閱讀 TRAINING.md
- ✅ 理解每個腳本的作用
- ✅ 查看 examples/ 範例檔案

### 第 3 天：獨立運作（10 分鐘）
- ✅ 完成 CHECKLIST.md
- ✅ 監控第一次自動執行
- ✅ 處理可能的錯誤

**恭喜！你現在可以獨立運作了 🎉**

---

## 🆘 需要幫助？

### 常見問題

**Q: 找不到候選人怎麼辦？**
A: 檢查搜尋關鍵字是否正確，參考 [troubleshooting.md](troubleshooting.md)

**Q: AI 配對分數都很低？**
A: 檢查職缺 JD 是否過於嚴格，可能需要調整門檻

**Q: Telegram 通知沒收到？**
A: 檢查 Bot 權限，確認可以發送訊息到 Topic 304

### 相關文檔

- 系統連接問題 → [docs/OPENCLAW-INTEGRATION.md](../../docs/OPENCLAW-INTEGRATION.md)
- 模組使用問題 → [training/HEADHUNTER-AI-MODULES.md](../../training/HEADHUNTER-AI-MODULES.md)
- AI 配對邏輯 → [modules/ai-matcher/README.md](../../modules/ai-matcher/README.md)

---

## 📈 效能指標

**目標 KPI**:
- 每次執行找到 10-30 位候選人
- P0+P1 候選人佔比 > 30%
- 去重率 < 20%（代表有找到新人）
- 執行時間 < 5 分鐘

**監控方式**:
```bash
# 查看最近 10 次執行日誌
openclaw cron logs 058e25d3 --limit 10
```

---

## 🔗 相關資源

- **倉庫**: https://github.com/jacky6658/step1ne-headhunter-skill
- **系統**: https://step1ne.zeabur.app
- **履歷池**: [Google Sheets](https://docs.google.com/spreadsheets/d/1PunpaDAFBPBL_I76AiRYGXKaXDZvMl1c262SEtxRk6Q)
- **職缺管理**: [Google Sheets](https://docs.google.com/spreadsheets/d/1QPaeOm-slNVFCeM8Q3gg3DawKjzp2tYwyfquvdHlZFE)

---

**最後更新**: 2026-02-23  
**版本**: v1.0.0  
**維護者**: YuQi AI Assistant
