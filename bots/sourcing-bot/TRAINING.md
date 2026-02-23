# Sourcing Bot 完整訓練指南 📚

**預計學習時間**: 30 分鐘  
**前置技能**: 基本的 OpenClaw 使用經驗  
**完成後**: 你可以獨立運作 Sourcing Bot

---

## 📋 目錄

1. [系統架構](#1-系統架構)
2. [工作流程詳解](#2-工作流程詳解)
3. [腳本使用指南](#3-腳本使用指南)
4. [AI 配對系統](#4-ai-配對系統)
5. [Cron 設定](#5-cron-設定)
6. [監控與優化](#6-監控與優化)
7. [故障排除](#7-故障排除)

---

## 1. 系統架構

### 1.1 Sourcing Bot 在整體系統中的位置

```
┌─────────────────────────────────────────────┐
│          Step1ne 獵頭系統                    │
│                                              │
│  ┌────────────┐  ┌────────────┐            │
│  │ JD 管理    │  │ 履歷池 v2  │            │
│  │ (職缺)     │  │ (250人)    │            │
│  └─────┬──────┘  └──────▲─────┘            │
│        │                 │                  │
│        │ 讀取職缺        │ 匯入候選人        │
│        │                 │                  │
│  ┌─────▼─────────────────┴─────┐           │
│  │   Sourcing Bot (你)          │ ◄──┐     │
│  │  • LinkedIn 搜尋             │    │     │
│  │  • GitHub 搜尋               │    │     │
│  │  • AI 配對評分               │    │     │
│  │  • 去重匯入                  │    │     │
│  └─────────────┬────────────────┘    │     │
│                │                      │     │
│                │ Telegram 通知        │     │
│                ▼                      │     │
│  ┌────────────────────────┐          │     │
│  │  HR AI招募自動化群組    │          │     │
│  │  Topic 304 (履歷池)     │          │     │
│  └────────────────────────┘          │     │
└──────────────────────────────────────┼─────┘
                                       │
                            OpenClaw Cron (每天3次)
```

### 1.2 核心元件

| 元件 | 說明 | 位置 |
|------|------|------|
| **JD 管理表** | 職缺列表 | Google Sheets (1QPaeOm-slNVFCeM8Q3gg3DawKjzp2tYwyfquvdHlZFE) |
| **履歷池 v2** | 候選人資料庫 | Google Sheets (1PunpaDAFBPBL_I76AiRYGXKaXDZvMl1c262SEtxRk6Q) |
| **LinkedIn 搜尋** | 公開搜尋 | workflows/linkedin-search.sh |
| **GitHub 搜尋** | 開發者搜尋 | workflows/github-search.sh |
| **AI 配對系統** | 評分與排序 | modules/ai-matcher/ai_matcher_v3.py |
| **主流程** | 整合所有步驟 | workflows/auto-sourcing.sh |

---

## 2. 工作流程詳解

### 2.1 完整流程圖

```
開始
 │
 ▼
1. 讀取 JD 管理表
   ├─ 篩選「招募中」職缺
   └─ 隨機選 2 個職缺（避免搜尋管道過載）
 │
 ▼
2. 執行多管道搜尋
   ├─ LinkedIn 搜尋（10-15人）
   ├─ GitHub 搜尋（5-10人）
   └─ 合併結果（15-25人）
 │
 ▼
3. AI 自動配對評分
   ├─ 技能匹配度（40%）
   ├─ 年資匹配度（30%）
   ├─ 穩定度評分（20%）
   └─ 學歷背景（10%）
 │
 ▼
4. 分類與排序
   ├─ P0: 90+ 分（強烈推薦）
   ├─ P1: 70-89 分（推薦）
   ├─ P2: 50-69 分（可考慮）
   └─ 未達標: <50 分（不匯入）
 │
 ▼
5. 去重檢查
   ├─ 與履歷池比對（Email, Phone, GitHub URL）
   └─ 過濾重複候選人
 │
 ▼
6. 匯入履歷池
   ├─ 寫入 Google Sheets
   └─ 記錄來源、日期、負責顧問
 │
 ▼
7. 發送 Telegram 通知
   ├─ 職缺名稱
   ├─ 搜尋管道統計
   ├─ 分類統計（P0/P1/P2）
   ├─ Top 3 推薦（姓名、分數、連結）
   └─ 已匯入行數
 │
 ▼
結束
```

### 2.2 每日執行時間規劃

| 時間 | Cron ID | 職缺數量 | 預期結果 |
|------|---------|---------|---------|
| 09:00 | 058e25d3 | 2 個 | 15-30 位候選人 |
| 14:00 | f613fd81 | 2 個 | 15-30 位候選人 |
| 20:00 | be5c9f85 | 2 個 | 15-30 位候選人 |

**每日累計**: 45-90 位新候選人（去重後約 30-50 位）

---

## 3. 腳本使用指南

### 3.1 主流程：auto-sourcing.sh

**完整的候選人搜尋自動化**

#### 基本用法

```bash
cd /Users/user/clawd/projects/step1ne-headhunter-skill/bots/sourcing-bot

# 正式執行（處理 2 個隨機職缺）
bash workflows/auto-sourcing.sh

# 測試模式（只處理 1 個職缺）
bash workflows/auto-sourcing.sh --test

# 指定職缺（只處理特定職缺）
bash workflows/auto-sourcing.sh --job "AI工程師"

# 詳細模式（顯示所有日誌）
bash workflows/auto-sourcing.sh --verbose
```

#### 參數說明

| 參數 | 說明 | 範例 |
|------|------|------|
| `--test` | 測試模式（1 個職缺） | `bash auto-sourcing.sh --test` |
| `--job "職缺名稱"` | 指定職缺 | `bash auto-sourcing.sh --job "AI工程師"` |
| `--verbose` | 詳細日誌 | `bash auto-sourcing.sh --verbose` |
| `--dry-run` | 不匯入履歷池 | `bash auto-sourcing.sh --dry-run` |

#### 輸出範例

```
=== 履歷池自動累積執行開始 ===
時間: 2026-02-23 09:00:15

[1/7] 讀取職缺管理表...
✓ 找到 12 個招募中的職缺
✓ 隨機選擇 2 個職缺：AI工程師、後端工程師

[2/7] 搜尋職缺 1: AI工程師
  → LinkedIn 搜尋: 15 位候選人
  → GitHub 搜尋: 8 位候選人
  → 合併: 23 位候選人

[3/7] AI 配對評分...
  → P0 (90+ 分): 2 位
  → P1 (70-89 分): 5 位
  → P2 (50-69 分): 8 位
  → 未達標 (<50 分): 8 位

[4/7] Top 3 推薦:
  1. 張大明 (92分) - Python, TensorFlow, 8年
  2. 李小華 (88分) - PyTorch, MLOps, 6年
  3. 王小明 (85分) - NLP, BERT, 5年

[5/7] 去重檢查...
  → 重複候選人: 3 位
  → 新候選人: 12 位

[6/7] 匯入履歷池...
  ✓ 12 位候選人已匯入（行號: 251-262）

[7/7] 發送 Telegram 通知...
  ✓ 通知已發送到 Topic 304

=== 執行完成 ===
總耗時: 3 分 42 秒
```

### 3.2 子流程 1: linkedin-search.sh

**LinkedIn 公開搜尋**（不需要付費帳號）

#### 基本用法

```bash
cd workflows

# 基本搜尋
bash linkedin-search.sh "AI工程師" "Python,TensorFlow"

# 指定地區
bash linkedin-search.sh "後端工程師" "Go,Kubernetes" "Taiwan"

# 限制結果數量
bash linkedin-search.sh "前端工程師" "React,TypeScript" "Taiwan" 20
```

#### 參數說明

```bash
linkedin-search.sh <職位名稱> <技能關鍵字> [地區] [限制數量]
```

| 參數 | 必填 | 說明 | 預設值 |
|------|------|------|--------|
| 職位名稱 | ✅ | 搜尋的職位 | - |
| 技能關鍵字 | ✅ | 逗號分隔 | - |
| 地區 | ❌ | 搜尋地區 | Taiwan |
| 限制數量 | ❌ | 最多返回幾人 | 15 |

#### 輸出格式（JSON）

```json
[
  {
    "name": "張大明",
    "position": "Senior AI Engineer",
    "company": "Google Taiwan",
    "location": "台北市",
    "linkedin_url": "https://linkedin.com/in/xxx",
    "skills": ["Python", "TensorFlow", "MLOps"],
    "years_of_experience": 8,
    "matched_keywords": ["Python", "TensorFlow"]
  }
]
```

### 3.3 子流程 2: github-search.sh

**GitHub 開發者搜尋**（適合技術職缺）

#### 基本用法

```bash
cd workflows

# 基本搜尋
bash github-search.sh "後端工程師" "Go,Kubernetes"

# 指定地區
bash github-search.sh "DevOps 工程師" "Docker,AWS" "Taiwan"

# 限制結果數量
bash github-search.sh "全端工程師" "React,Node.js" "Taiwan" 10
```

#### 技能推斷邏輯

GitHub 搜尋會自動分析候選人的：
1. **Top 10 Repositories** 的程式語言
2. **Repository Topics** 標籤
3. **Repository Description** 關鍵字

**範例**：
- Repo 語言 = Python → 推斷技能: Python
- Repo topic = "machine-learning" → 推斷技能: ML
- Repo description = "Kubernetes cluster" → 推斷技能: Kubernetes

#### 輸出格式（JSON）

```json
[
  {
    "name": "李小華",
    "github_username": "lee-dev",
    "github_url": "https://github.com/lee-dev",
    "location": "Taipei, Taiwan",
    "bio": "Backend Engineer @ TechCorp",
    "skills": ["Go", "Kubernetes", "PostgreSQL"],
    "top_languages": {
      "Go": 45,
      "Python": 30,
      "Shell": 25
    },
    "public_repos": 42,
    "followers": 128
  }
]
```

---

## 4. AI 配對系統

### 4.1 評分邏輯

AI 配對系統（`ai_matcher_v3.py`）使用 **4 維度評分**：

| 維度 | 權重 | 說明 |
|------|------|------|
| 技能匹配度 | 40% | 候選人技能與職缺 JD 的重疊率 |
| 年資匹配度 | 30% | 工作年資是否符合職缺要求 |
| 穩定度評分 | 20% | 工作穩定性（離職頻率、任職時長）|
| 學歷背景 | 10% | 學歷是否符合職缺要求 |

### 4.2 評分公式

```
總分 = 技能匹配 × 40% + 年資匹配 × 30% + 穩定度 × 20% + 學歷 × 10%
```

#### 技能匹配度計算

```python
技能匹配度 = (匹配技能數 / 職缺要求技能數) × 100

# 範例
職缺要求: Python, TensorFlow, Docker (3個)
候選人技能: Python, TensorFlow, Kubernetes, AWS (4個)
匹配技能: Python, TensorFlow (2個)
技能匹配度 = (2 / 3) × 100 = 66.7 分
```

#### 年資匹配度計算

```python
if 候選人年資 >= 職缺要求年資:
    年資匹配度 = 100
elif 候選人年資 >= 職缺要求年資 × 0.7:
    年資匹配度 = 80
else:
    年資匹配度 = 60

# 範例
職缺要求: 3年+
候選人年資: 5年
年資匹配度 = 100 分
```

### 4.3 分級標準

| 等級 | 分數 | 說明 | 行動建議 |
|------|------|------|---------|
| P0 | 90-100 | 完美匹配 | 立即聯繫 |
| P1 | 70-89 | 高度匹配 | 優先聯繫 |
| P2 | 50-69 | 基本匹配 | 可考慮 |
| 未達標 | <50 | 不匹配 | 不匯入 |

### 4.4 調整配對門檻

如果找到的候選人太少，可以調整配對門檻：

**修改檔案**: `modules/ai-matcher/ai_matcher_v3.py`

```python
# 找到這一行
MIN_SCORE_THRESHOLD = 50  # 預設門檻

# 降低門檻（會找到更多候選人，但品質較低）
MIN_SCORE_THRESHOLD = 40

# 提高門檻（只找高品質候選人，但數量較少）
MIN_SCORE_THRESHOLD = 60
```

---

## 5. Cron 設定

### 5.1 已設定的 Cron Jobs

```bash
# 查看所有 Sourcing Bot 的 Cron
openclaw cron list | grep "履歷池自動累積"
```

**輸出**：
```
058e25d3 - 履歷池自動累積-早上 (每天 09:00) - ok
f613fd81 - 履歷池自動累積-下午 (每天 14:00) - ok
be5c9f85 - 履歷池自動累積-晚上 (每天 20:00) - ok
```

### 5.2 手動執行 Cron（測試用）

```bash
# 執行早上的 Cron
openclaw cron run 058e25d3

# 執行下午的 Cron
openclaw cron run f613fd81

# 執行晚上的 Cron
openclaw cron run be5c9f85
```

### 5.3 查看 Cron 執行日誌

```bash
# 查看最近 10 次執行
openclaw cron logs 058e25d3 --limit 10

# 查看最近 1 次執行的詳細日誌
openclaw cron logs 058e25d3 --limit 1 --verbose
```

### 5.4 新增 Cron（如果需要）

使用自動設定腳本：

```bash
cd /Users/user/clawd/projects/step1ne-headhunter-skill/bots/sourcing-bot
bash workflows/cron-setup.sh
```

或手動新增：

```bash
openclaw cron add \
  --label "履歷池自動累積-早上" \
  --schedule "0 9 * * *" \
  --command "bash /Users/user/clawd/projects/step1ne-headhunter-skill/bots/sourcing-bot/workflows/auto-sourcing.sh"
```

### 5.5 暫停/恢復 Cron

```bash
# 暫停 Cron
openclaw cron pause 058e25d3

# 恢復 Cron
openclaw cron resume 058e25d3

# 刪除 Cron
openclaw cron delete 058e25d3
```

---

## 6. 監控與優化

### 6.1 監控指標

**每日監控**：
- 執行次數：3 次（09:00, 14:00, 20:00）
- 找到候選人數：45-90 位
- 去重後匯入：30-50 位
- P0+P1 比例：> 30%

**每週監控**：
- 累計新增候選人：200-350 位
- 重複率：< 20%
- Cron 失敗次數：0 次

### 6.2 效能優化

#### 問題 1: 找到的候選人太少

**診斷**：
```bash
# 檢查搜尋關鍵字
cat config/search-keywords.json

# 檢查 AI 配對門檻
grep "MIN_SCORE_THRESHOLD" ../../modules/ai-matcher/ai_matcher_v3.py
```

**解決方案**：
- 放寬搜尋關鍵字（增加同義詞）
- 降低 AI 配對門檻（50 → 40）
- 增加搜尋管道（LinkedIn + GitHub + 履歷池）

#### 問題 2: 重複率太高（>30%）

**診斷**：
```bash
# 檢查去重邏輯
grep -A 10 "去重檢查" workflows/auto-sourcing.sh
```

**解決方案**：
- 改變搜尋關鍵字（避免總是搜尋相同的人）
- 增加職缺多樣性（不要總是搜尋熱門職缺）
- 擴大搜尋範圍（不限台灣，包含海外）

#### 問題 3: P0+P1 比例太低（<20%）

**診斷**：
```bash
# 檢查職缺 JD 是否過於嚴格
gog sheets read <SHEET_ID> <TAB> --range "A2:E100" | grep "招募中"
```

**解決方案**：
- 簡化職缺 JD（減少必要技能數量）
- 降低年資要求（3年+ → 1年+）
- 調整權重（技能 40% → 50%，年資 30% → 20%）

### 6.3 優化搜尋關鍵字

**編輯檔案**: `config/search-keywords.json`

```json
{
  "AI工程師": {
    "primary": ["AI Engineer", "Machine Learning Engineer", "ML Engineer"],
    "skills": ["Python", "TensorFlow", "PyTorch", "Scikit-learn"],
    "synonyms": ["Data Scientist", "Deep Learning Engineer"]
  },
  "後端工程師": {
    "primary": ["Backend Engineer", "Backend Developer", "Server Engineer"],
    "skills": ["Go", "Python", "Java", "Node.js", "PostgreSQL"],
    "synonyms": ["API Developer", "Backend Architect"]
  }
}
```

---

## 7. 故障排除

詳細的故障排除指南請參考：[troubleshooting.md](troubleshooting.md)

### 7.1 常見問題快速參考

| 問題 | 可能原因 | 快速解決 |
|------|---------|---------|
| 找不到候選人 | 搜尋關鍵字錯誤 | 檢查 `config/search-keywords.json` |
| AI 配對分數都很低 | JD 太嚴格 | 降低配對門檻或簡化 JD |
| Telegram 通知沒收到 | Bot 權限不足 | 檢查 Bot 是否可發送到 Topic 304 |
| Google Sheets 寫入失敗 | OAuth 過期 | 重新執行 `gog auth add` |
| GitHub 搜尋失敗 | Token 無效 | 檢查 `$GITHUB_TOKEN` |

### 7.2 執行失敗時的檢查步驟

```bash
# 1. 檢查 OpenClaw 狀態
openclaw status

# 2. 檢查 Google Sheets 認證
gog auth list

# 3. 檢查 GitHub Token
echo $GITHUB_TOKEN

# 4. 手動執行測試
bash workflows/auto-sourcing.sh --test --verbose

# 5. 查看詳細日誌
tail -f /tmp/sourcing-bot.log
```

---

## 🎉 恭喜！訓練完成

完成這份訓練指南後，你應該已經掌握：

- ✅ Sourcing Bot 的系統架構
- ✅ 完整的工作流程
- ✅ 所有腳本的使用方式
- ✅ AI 配對系統的評分邏輯
- ✅ Cron 自動化設定
- ✅ 監控與優化方法
- ✅ 故障排除技巧

**下一步**：完成 [CHECKLIST.md](CHECKLIST.md)，確認所有項目後即可上線！

---

**最後更新**: 2026-02-23  
**版本**: v1.0.0  
**維護者**: YuQi AI Assistant
