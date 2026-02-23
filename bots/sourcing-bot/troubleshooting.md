# Sourcing Bot 故障排除指南 🔧

**目的**: 快速診斷並解決常見問題  
**適用對象**: Sourcing Bot 運行中遇到問題時參考

---

## 📋 目錄

1. [搜尋相關問題](#1-搜尋相關問題)
2. [AI 配對問題](#2-ai-配對問題)
3. [資料匯入問題](#3-資料匯入問題)
4. [通知問題](#4-通知問題)
5. [Cron 問題](#5-cron-問題)
6. [效能問題](#6-效能問題)

---

## 1. 搜尋相關問題

### 問題 1.1: 找不到候選人（搜尋結果為 0）

**症狀**：
```
LinkedIn 搜尋: 0 位候選人
GitHub 搜尋: 0 位候選人
```

**可能原因 & 解決方案**：

#### 原因 A: 搜尋關鍵字錯誤

**診斷**：
```bash
# 檢查關鍵字配置
cat config/search-keywords.json
```

**解決方案**：
1. 使用更通用的關鍵字
   - ❌ ".NET Core Engineer"（太具體）
   - ✅ "Backend Engineer"（通用）

2. 增加同義詞
   ```json
   {
     "AI工程師": {
       "primary": ["AI Engineer"],
       "synonyms": ["Machine Learning Engineer", "ML Engineer", "Data Scientist"]
     }
   }
   ```

3. 使用英文關鍵字
   - ❌ "人工智慧工程師"
   - ✅ "AI Engineer"

#### 原因 B: 搜尋管道問題

**診斷**：
```bash
# 測試 LinkedIn 搜尋
bash workflows/linkedin-search.sh "Engineer" "Python"

# 測試 GitHub 搜尋
bash workflows/github-search.sh "Engineer" "Python"
```

**解決方案**：
- 如果 LinkedIn 失敗 → 檢查網路連接
- 如果 GitHub 失敗 → 檢查 GitHub Token

#### 原因 C: 地區限制太嚴格

**診斷**：
```bash
# 檢查是否限制為 Taiwan
grep "location" workflows/linkedin-search.sh
```

**解決方案**：
- 擴大地區範圍（Taiwan → Asia）
- 移除地區限制（全球搜尋）

---

### 問題 1.2: 搜尋到的候選人品質很差

**症狀**：
```
找到 20 位候選人，但 AI 配對分數都低於 40 分
```

**可能原因 & 解決方案**：

#### 原因 A: 職缺 JD 太嚴格

**診斷**：
```bash
# 檢查職缺 JD
gog sheets read \
  1QPaeOm-slNVFCeM8Q3gg3DawKjzp2tYwyfquvdHlZFE \
  "step1ne 職缺管理!A2:E100" | grep "招募中"
```

**解決方案**：
1. **簡化技能要求**
   - ❌ 要求 10 個技能（Python, TensorFlow, PyTorch, Keras, Scikit-learn...）
   - ✅ 只要求 3 個核心技能（Python, TensorFlow, Docker）

2. **降低年資要求**
   - ❌ 要求 5 年+
   - ✅ 要求 3 年+

3. **放寬學歷要求**
   - ❌ 只接受碩士
   - ✅ 學士即可

#### 原因 B: 搜尋關鍵字與 JD 不匹配

**範例**：
- JD 要求：Python, TensorFlow, Docker
- 搜尋關鍵字：Machine Learning, AI（太廣泛）
- 結果：找到很多 Data Scientist，但不會 Docker

**解決方案**：
- 搜尋關鍵字與 JD 技能保持一致
- 至少包含 2 個 JD 核心技能

---

### 問題 1.3: GitHub 搜尋技能推斷失敗

**症狀**：
```
所有候選人的 skills 欄位都是空陣列 []
```

**可能原因 & 解決方案**：

#### 原因 A: GitHub Token 未設定

**診斷**：
```bash
echo $GITHUB_TOKEN
```

**解決方案**：
```bash
# 設定 GitHub Token
export GITHUB_TOKEN="ghp_xxx..."

# 永久設定（加入 .zshrc 或 .bashrc）
echo 'export GITHUB_TOKEN="ghp_xxx..."' >> ~/.zshrc
source ~/.zshrc
```

#### 原因 B: GitHub API 速率限制

**診斷**：
```bash
# 檢查 API 限額
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/rate_limit
```

**解決方案**：
- 等待速率限制重置（1 小時後）
- 使用有 Token 的請求（5000 requests/hour）
- 減少搜尋頻率

---

## 2. AI 配對問題

### 問題 2.1: 所有候選人分數都很低（<50 分）

**症狀**：
```
AI 配對結果:
- P0: 0 位
- P1: 0 位
- P2: 2 位
- 未達標: 18 位
```

**可能原因 & 解決方案**：

#### 原因 A: 配對門檻太高

**診斷**：
```bash
# 檢查配對門檻
grep "MIN_SCORE_THRESHOLD" ../../modules/ai-matcher/ai_matcher_v3.py
```

**解決方案**：
```python
# 修改 ai_matcher_v3.py
MIN_SCORE_THRESHOLD = 40  # 從 50 降低到 40
```

#### 原因 B: 技能匹配權重過高

**診斷**：
```bash
# 檢查權重配置
grep -A 5 "權重" ../../modules/ai-matcher/ai_matcher_v3.py
```

**解決方案**：
```python
# 調整權重（降低技能，提高年資和穩定度）
WEIGHTS = {
    'skills': 0.30,      # 從 40% 降低到 30%
    'experience': 0.35,  # 從 30% 提高到 35%
    'stability': 0.25,   # 從 20% 提高到 25%
    'education': 0.10    # 維持 10%
}
```

---

### 問題 2.2: P0/P1 候選人太少（<3 位）

**症狀**：
```
找到 20 位候選人，但只有 2 位 P1，0 位 P0
```

**可能原因 & 解決方案**：

#### 解決方案 1: 降低 P0/P1 分數門檻

```python
# 修改 ai_matcher_v3.py
GRADE_THRESHOLDS = {
    'P0': 80,  # 從 90 降低到 80
    'P1': 60,  # 從 70 降低到 60
    'P2': 40   # 從 50 降低到 40
}
```

#### 解決方案 2: 增加搜尋數量

```bash
# 修改 auto-sourcing.sh
LINKEDIN_LIMIT=30  # 從 15 增加到 30
GITHUB_LIMIT=20    # 從 10 增加到 20
```

#### 解決方案 3: 優化搜尋關鍵字

- 使用更精準的關鍵字（減少噪音）
- 增加同義詞（擴大覆蓋範圍）

---

## 3. 資料匯入問題

### 問題 3.1: Google Sheets 寫入失敗

**症狀**：
```
Error: Unable to write to Google Sheets
```

**可能原因 & 解決方案**：

#### 原因 A: OAuth 認證過期

**診斷**：
```bash
gog auth list
```

**解決方案**：
```bash
# 重新認證
gog auth add aijessie88@step1ne.com
```

#### 原因 B: Sheet 權限不足

**診斷**：
- 檢查 `aijessie88@step1ne.com` 是否有履歷池 v2 的編輯權限

**解決方案**：
1. 開啟 Google Sheets
2. 點擊「共用」
3. 確認 `aijessie88@step1ne.com` 有「編輯者」權限

#### 原因 C: Sheet ID 錯誤

**診斷**：
```bash
# 檢查 Sheet ID
grep "SHEET_ID" workflows/auto-sourcing.sh
```

**解決方案**：
```bash
# 正確的 Sheet ID
SHEET_ID="1PunpaDAFBPBL_I76AiRYGXKaXDZvMl1c262SEtxRk6Q"
```

---

### 問題 3.2: 重複候選人被匯入

**症狀**：
```
同一個候選人在履歷池中出現 2 次以上
```

**可能原因 & 解決方案**：

#### 原因 A: 去重邏輯失效

**診斷**：
```bash
# 檢查去重邏輯
grep -A 20 "去重檢查" workflows/auto-sourcing.sh
```

**解決方案**：
```bash
# 改進去重邏輯（比對 3 個欄位）
# 1. Email
# 2. Phone
# 3. GitHub URL 或 LinkedIn URL
```

#### 原因 B: 候選人資訊略有不同

**範例**：
- 第一次：Email = "lee@gmail.com"
- 第二次：Email = "lee@company.com"（不同 Email）

**解決方案**：
- 使用姓名 + 公司 + 職位進行模糊比對
- 人工定期檢查並合併重複候選人

---

## 4. 通知問題

### 問題 4.1: Telegram 通知沒收到

**症狀**：
```
Sourcing Bot 執行完成，但 Topic 304 沒收到通知
```

**可能原因 & 解決方案**：

#### 原因 A: Bot 權限不足

**診斷**：
```bash
# 手動發送測試訊息
openclaw message send \
  --target "-1003231629634" \
  --thread-id 304 \
  --message "測試訊息"
```

**解決方案**：
1. 確認 Bot 已加入群組
2. 確認 Bot 有發送訊息權限
3. 確認 Topic 304 存在且未關閉

#### 原因 B: 通知腳本執行失敗

**診斷**：
```bash
# 檢查腳本日誌
grep "Telegram 通知" /tmp/sourcing-bot.log
```

**解決方案**：
- 檢查 `openclaw message send` 指令是否正確
- 確認 `--target` 和 `--thread-id` 參數正確

---

### 問題 4.2: 通知格式錯亂

**症狀**：
```
Telegram 訊息顯示為一整行，沒有換行和 Emoji
```

**可能原因 & 解決方案**：

#### 原因 A: 換行符號問題

**解決方案**：
```bash
# 使用 $'\n' 而不是 \n
MESSAGE="履歷池自動收集執行完成"$'\n'$'\n'"搜尋職缺："
```

#### 原因 B: Emoji 顯示問題

**解決方案**：
```bash
# 確保使用 UTF-8 編碼
export LC_ALL=en_US.UTF-8
```

---

## 5. Cron 問題

### 問題 5.1: Cron 沒有按時執行

**症狀**：
```
應該 09:00 執行，但沒有執行
```

**可能原因 & 解決方案**：

#### 原因 A: Cron 狀態為 error

**診斷**：
```bash
openclaw cron list | grep "履歷池自動累積"
```

**解決方案**：
```bash
# 手動執行一次（重置狀態）
openclaw cron run 058e25d3
```

#### 原因 B: Gateway 沒有運行

**診斷**：
```bash
openclaw status
```

**解決方案**：
```bash
# 啟動 Gateway
openclaw gateway start
```

---

### 問題 5.2: Cron 執行失敗

**症狀**：
```
Cron 狀態為 error，無法執行
```

**可能原因 & 解決方案**：

#### 診斷步驟

```bash
# 1. 查看 Cron 日誌
openclaw cron logs 058e25d3 --limit 1

# 2. 手動執行腳本
bash workflows/auto-sourcing.sh --test --verbose

# 3. 檢查錯誤訊息
tail -f /tmp/sourcing-bot.log
```

#### 常見錯誤

| 錯誤訊息 | 可能原因 | 解決方案 |
|---------|---------|---------|
| `command not found` | 腳本路徑錯誤 | 檢查 Cron 的 `--command` 參數 |
| `Permission denied` | 沒有執行權限 | `chmod +x workflows/*.sh` |
| `OAuth token expired` | 認證過期 | `gog auth add` |
| `API rate limit exceeded` | GitHub API 超過限額 | 等待 1 小時或減少頻率 |

---

## 6. 效能問題

### 問題 6.1: 執行時間過長（>10 分鐘）

**症狀**：
```
Sourcing Bot 執行超過 10 分鐘仍未完成
```

**可能原因 & 解決方案**：

#### 原因 A: 搜尋候選人數量過多

**解決方案**：
```bash
# 減少搜尋數量
LINKEDIN_LIMIT=10  # 從 30 減少到 10
GITHUB_LIMIT=8     # 從 20 減少到 8
```

#### 原因 B: AI 配對運算過慢

**解決方案**：
- 簡化配對邏輯（減少比對維度）
- 過濾掉明顯不符合的候選人

#### 原因 C: 網路速度過慢

**解決方案**：
- 檢查網路連接
- 使用本地快取機制

---

### 問題 6.2: 重複率過高（>30%）

**症狀**：
```
找到 30 位候選人，但 20 位都是重複的
```

**可能原因 & 解決方案**：

#### 原因 A: 搜尋關鍵字太固定

**解決方案**：
- 每次隨機選擇不同職缺
- 使用多種關鍵字組合

#### 原因 B: 搜尋範圍太小

**解決方案**：
- 擴大地區範圍（Taiwan → Asia）
- 增加搜尋管道（LinkedIn + GitHub + 104）

---

## 🆘 仍然無法解決？

### 診斷工具

```bash
# 完整的診斷腳本
cd /Users/user/clawd/projects/step1ne-headhunter-skill/bots/sourcing-bot

# 1. 檢查環境
echo "=== 環境檢查 ==="
openclaw version
openclaw status
gog auth list
echo $GITHUB_TOKEN

# 2. 測試搜尋
echo "=== 搜尋測試 ==="
bash workflows/linkedin-search.sh "Engineer" "Python" > /tmp/test-linkedin.json
bash workflows/github-search.sh "Engineer" "Python" > /tmp/test-github.json
echo "LinkedIn: $(cat /tmp/test-linkedin.json | jq length) 位"
echo "GitHub: $(cat /tmp/test-github.json | jq length) 位"

# 3. 測試配對
echo "=== 配對測試 ==="
python3 ../../modules/ai-matcher/ai_matcher_v3.py \
  --candidates /tmp/test-linkedin.json \
  --job-requirements "Python,TensorFlow" \
  --min-years 3

# 4. 測試匯入
echo "=== 匯入測試 ==="
gog sheets read \
  1PunpaDAFBPBL_I76AiRYGXKaXDZvMl1c262SEtxRk6Q \
  "履歷池v2!A:A" | tail -5
```

### 聯繫支援

如果以上所有方法都無法解決，請：

1. **收集診斷資訊**：
   - OpenClaw 版本
   - 錯誤訊息（完整日誌）
   - 最近一次成功執行的時間

2. **查閱相關文檔**：
   - [TRAINING.md](TRAINING.md)
   - [docs/OPENCLAW-INTEGRATION.md](../../docs/OPENCLAW-INTEGRATION.md)
   - [modules/ai-matcher/README.md](../../modules/ai-matcher/README.md)

3. **GitHub Issues**：
   - 前往 https://github.com/jacky6658/step1ne-headhunter-skill/issues
   - 提交詳細的問題報告

---

**最後更新**: 2026-02-23  
**版本**: v1.0.0  
**維護者**: YuQi AI Assistant
