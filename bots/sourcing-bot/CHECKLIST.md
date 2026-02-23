# Sourcing Bot 上線前檢查清單 ✅

**目的**: 確保 Sourcing Bot 可以順利運作  
**預計時間**: 15 分鐘  
**建議**: 按順序逐項檢查，確認每項都是 ✅ 才上線

---

## 📋 Part 1: 環境準備（5 分鐘）

### 1.1 OpenClaw 基礎環境

```bash
# 檢查 OpenClaw 版本
openclaw version
```
- [ ] OpenClaw 版本 >= 2026.2.21
- [ ] Gateway 狀態為 running

```bash
# 檢查 OpenClaw 狀態
openclaw status
```
- [ ] Gateway running 顯示綠色 ✓
- [ ] RPC probe ok

### 1.2 Google Sheets 認證

```bash
# 檢查 Google 帳號認證
gog auth list
```
- [ ] 看到 `aijessie88@step1ne.com`
- [ ] 狀態為 authenticated（不是 expired）

**如果認證過期**：
```bash
gog auth add aijessie88@step1ne.com
# 按照指示完成 OAuth 流程
```

### 1.3 GitHub Token

```bash
# 檢查 GitHub Token
echo $GITHUB_TOKEN
```
- [ ] Token 存在（格式：`ghp_xxx...`）
- [ ] Token 有效（未過期）

**如果 Token 不存在或過期**：
1. 前往 GitHub Settings → Developer settings → Personal access tokens
2. 生成新 Token（勾選 `repo`, `user` 權限）
3. 設定環境變數：`export GITHUB_TOKEN="ghp_xxx..."`

### 1.4 Telegram Bot 權限

- [ ] Bot 可以發送訊息到 HR AI招募自動化群組
- [ ] Bot 可以發送訊息到 Topic 304（履歷池）
- [ ] Bot 訊息格式正確（測試過至少 1 次）

**測試方式**：
```bash
openclaw message send \
  --target "-1003231629634" \
  --thread-id 304 \
  --message "Sourcing Bot 測試訊息"
```

---

## 📋 Part 2: 權限確認（3 分鐘）

### 2.1 Google Sheets 讀取權限

```bash
# 測試讀取職缺管理表
gog sheets read \
  1QPaeOm-slNVFCeM8Q3gg3DawKjzp2tYwyfquvdHlZFE \
  "step1ne 職缺管理!A2:E10"
```
- [ ] 可以正常讀取
- [ ] 看到職缺列表

### 2.2 Google Sheets 寫入權限

```bash
# 測試寫入履歷池（測試行）
gog sheets append \
  1PunpaDAFBPBL_I76AiRYGXKaXDZvMl1c262SEtxRk6Q \
  "履歷池v2!A:T" \
  --values "測試|test@example.com|0912345678|測試工程師|||||||||||||待聯繫|測試來源|Jacky||$(date +%Y-%m-%d)"
```
- [ ] 寫入成功
- [ ] 可以在履歷池最後一行看到測試資料
- [ ] **記得刪除測試行**

### 2.3 檔案系統權限

```bash
# 檢查腳本是否可執行
cd /Users/user/clawd/projects/step1ne-headhunter-skill/bots/sourcing-bot/workflows

ls -la *.sh
```
- [ ] 所有 `.sh` 檔案都有執行權限（`-rwxr-xr-x`）

**如果沒有執行權限**：
```bash
chmod +x *.sh
```

---

## 📋 Part 3: 腳本測試（5 分鐘）

### 3.1 測試 LinkedIn 搜尋

```bash
cd /Users/user/clawd/projects/step1ne-headhunter-skill/bots/sourcing-bot/workflows

# 測試搜尋
bash linkedin-search.sh "AI工程師" "Python,TensorFlow" > /tmp/linkedin-test.json

# 檢查結果
cat /tmp/linkedin-test.json | jq length
```
- [ ] 搜尋成功（無錯誤訊息）
- [ ] 找到至少 5 位候選人
- [ ] JSON 格式正確（可以用 `jq` 解析）

### 3.2 測試 GitHub 搜尋

```bash
# 測試搜尋
bash github-search.sh "後端工程師" "Go,Kubernetes" > /tmp/github-test.json

# 檢查結果
cat /tmp/github-test.json | jq length
```
- [ ] 搜尋成功（無錯誤訊息）
- [ ] 找到至少 5 位候選人
- [ ] JSON 格式正確

### 3.3 測試主流程（重要！）

```bash
# 執行測試模式（只處理 1 個職缺，不實際匯入）
bash auto-sourcing.sh --test --dry-run
```
- [ ] 流程執行成功（無錯誤）
- [ ] 顯示搜尋結果統計
- [ ] 顯示 AI 配對分數
- [ ] 顯示 Top 3 推薦

**如果測試失敗**：
1. 查看錯誤訊息
2. 參考 [troubleshooting.md](troubleshooting.md)
3. 修復問題後重新測試

### 3.4 測試實際匯入（小心！）

```bash
# 執行實際匯入（只處理 1 個職缺）
bash auto-sourcing.sh --test
```
- [ ] 候選人成功匯入履歷池
- [ ] 可以在履歷池最後幾行看到新候選人
- [ ] Telegram 通知已發送到 Topic 304
- [ ] 通知格式正確（職缺名稱、統計、Top 3）

---

## 📋 Part 4: Cron 設定（2 分鐘）

### 4.1 檢查現有 Cron

```bash
# 查看所有 Sourcing Bot 的 Cron
openclaw cron list | grep "履歷池自動累積"
```
- [ ] 看到 3 個 Cron（早上、下午、晚上）
- [ ] 所有 Cron 狀態為 `ok`（不是 `error`）

**如果 Cron 不存在或狀態為 error**：
```bash
# 重新設定 Cron
bash workflows/cron-setup.sh
```

### 4.2 手動觸發 Cron 測試

```bash
# 手動執行早上的 Cron
openclaw cron run 058e25d3
```
- [ ] Cron 執行成功
- [ ] 候選人已匯入履歷池
- [ ] Telegram 通知已發送

### 4.3 查看 Cron 日誌

```bash
# 查看最近一次執行日誌
openclaw cron logs 058e25d3 --limit 1
```
- [ ] 日誌顯示執行成功
- [ ] 沒有錯誤訊息

---

## 📋 Part 5: 通知設定（2 分鐘）

### 5.1 檢查通知格式

**手動發送測試通知**：
```bash
openclaw message send \
  --target "-1003231629634" \
  --thread-id 304 \
  --message "✅ 履歷池自動收集執行完成（測試）

搜尋職缺：
• AI工程師：5 位 P1 候選人

Top 推薦：
1. 張大明（85分）- https://github.com/test

狀態：✅ 5 位候選人已匯入履歷池，系統運作正常"
```

- [ ] 訊息成功發送到 Topic 304
- [ ] 格式正確（Emoji、換行、連結）
- [ ] 連結可點擊

### 5.2 確認通知內容

**理想的通知應該包含**：
- [ ] 執行時間（例：20:00）
- [ ] 搜尋職缺名稱
- [ ] 分類統計（P0/P1/P2 數量）
- [ ] Top 3 推薦（姓名、分數、連結）
- [ ] 匯入狀態（已匯入行數）
- [ ] 今日累計統計

---

## 📋 Part 6: 監控設定（1 分鐘）

### 6.1 設定日誌檔案

```bash
# 建立日誌目錄
mkdir -p /tmp/sourcing-bot-logs

# 測試日誌寫入
echo "$(date): Test log" >> /tmp/sourcing-bot-logs/$(date +%Y-%m-%d).log
```
- [ ] 日誌目錄建立成功
- [ ] 可以寫入日誌檔案

### 6.2 設定錯誤通知（可選）

**如果希望 Bot 失敗時自動通知**：
```bash
# 編輯 auto-sourcing.sh
# 在腳本最後加上錯誤處理
if [ $? -ne 0 ]; then
  openclaw message send \
    --target "-1003231629634" \
    --thread-id 304 \
    --message "⚠️ Sourcing Bot 執行失敗，請檢查日誌"
fi
```
- [ ] 錯誤通知已設定
- [ ] 測試過至少 1 次

---

## 🎯 最終檢查

### 完整流程測試

```bash
# 執行完整的自動化流程（正式模式）
cd /Users/user/clawd/projects/step1ne-headhunter-skill/bots/sourcing-bot
bash workflows/auto-sourcing.sh
```

**確認以下項目全部 ✅**：
- [ ] 讀取職缺成功（隨機選 2 個）
- [ ] LinkedIn 搜尋成功
- [ ] GitHub 搜尋成功
- [ ] AI 配對評分成功
- [ ] 去重檢查成功
- [ ] 匯入履歷池成功（可在 Google Sheets 看到新候選人）
- [ ] Telegram 通知發送成功（在 Topic 304 看到訊息）
- [ ] 通知格式正確
- [ ] 連結可點擊
- [ ] 整個流程在 5 分鐘內完成

---

## ✅ 上線確認

**如果以上所有項目都是 ✅，恭喜！你可以正式上線了 🎉**

### 上線後第一週監控重點

**每日檢查**（09:30, 14:30, 20:30）：
- [ ] Cron 是否按時執行
- [ ] 找到的候選人數量是否正常（10-30 位）
- [ ] P0+P1 比例是否 > 30%
- [ ] Telegram 通知是否正常發送
- [ ] 履歷池是否正確更新

**每週檢查**（週一 10:00）：
- [ ] 累計新增候選人數量（目標：200-350 位）
- [ ] 重複率（目標：< 20%）
- [ ] Cron 失敗次數（目標：0 次）
- [ ] AI 配對品質（隨機抽查 10 位候選人）

### 遇到問題時

1. **立即停止 Cron**：
   ```bash
   openclaw cron pause 058e25d3
   openclaw cron pause f613fd81
   openclaw cron pause be5c9f85
   ```

2. **檢查日誌**：
   ```bash
   openclaw cron logs 058e25d3 --limit 5
   ```

3. **參考故障排除**：
   - 閱讀 [troubleshooting.md](troubleshooting.md)
   - 查看 [TRAINING.md](TRAINING.md) 的優化章節

4. **修復後重新測試**：
   ```bash
   bash workflows/auto-sourcing.sh --test
   ```

5. **恢復 Cron**：
   ```bash
   openclaw cron resume 058e25d3
   openclaw cron resume f613fd81
   openclaw cron resume be5c9f85
   ```

---

## 📞 需要幫助？

- **系統問題** → [docs/OPENCLAW-INTEGRATION.md](../../docs/OPENCLAW-INTEGRATION.md)
- **訓練問題** → [TRAINING.md](TRAINING.md)
- **故障排除** → [troubleshooting.md](troubleshooting.md)
- **模組問題** → [training/HEADHUNTER-AI-MODULES.md](../../training/HEADHUNTER-AI-MODULES.md)

---

**最後更新**: 2026-02-23  
**版本**: v1.0.0  
**維護者**: YuQi AI Assistant
