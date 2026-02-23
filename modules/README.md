# Step1ne AI 模組庫

## 📦 模組總覽

本資料夾包含可獨立使用的 AI 智慧模組，支援獵頭顧問的核心業務流程。

---

## 🧠 核心模組清單

| 模組 | 功能 | 輸入 | 輸出 | 狀態 |
|------|------|------|------|------|
| **talent-grading** | 人才綜合評級 | 候選人履歷 | S/A+/A/B/C | ⏳ 開發中 |
| **ai-matcher** | 職缺配對分析 | JD + 候選人 | P0/P1/P2 + 分數 | ✅ 運行中 |
| **resume-parser** | 履歷解析歸檔 | PDF 履歷 | 結構化 JSON | ✅ 運行中 |
| **dedup-engine** | 候選人去重 | 候選人清單 | 去重後清單 | ✅ 運行中 |
| **learning-engine** | AI 學習系統 | 歷史資料 | 優化建議 | ✅ 運行中 |
| **github-talent-search** | GitHub 搜尋 | 技能關鍵字 | 候選人清單 | ✅ 運行中 |
| **linkedin-search** | LinkedIn 爬蟲 | 職位關鍵字 | 候選人清單 | ✅ 運行中 |
| **multi-channel-sourcing** | 多管道整合 | 職缺 JD | 整合候選人清單 | ✅ 運行中 |

---

## 🔧 使用指南

### 快速啟動

每個模組資料夾包含：
- `README.md` - 詳細使用說明
- `*.py` 或 `*.sh` - 可執行腳本
- `examples/` - 範例輸入/輸出（部分模組）

### 範例流程

**情境：找到候選人後進行評級**

```bash
# 1. 解析履歷
cd modules/resume-parser
./auto-resume-filing.sh

# 2. 評級候選人
cd ../talent-grading
python grading-logic.py --resume candidate.json

# 3. 配對職缺
cd ../ai-matcher
python ai_matcher_v2.py --jd jd.json --candidate candidate.json
```

---

## 📊 模組依賴關係

```
multi-channel-sourcing
  ├── github-talent-search
  ├── linkedin-search
  └── dedup-engine
  
ai-matcher
  ├── dedup-engine
  └── learning-engine
  
talent-grading
  └── resume-parser (資料來源)
```

---

## 🆕 新增模組

### 開發指南

1. **建立模組資料夾**
   ```bash
   mkdir modules/your-module-name
   cd modules/your-module-name
   ```

2. **建立 README.md**
   - 功能說明
   - 使用方式
   - 輸入/輸出格式
   - 範例

3. **實作核心邏輯**
   - Python 腳本（推薦）或 Shell 腳本
   - 清楚的參數說明
   - 錯誤處理

4. **測試與文檔**
   - 單元測試（可選）
   - 範例輸入/輸出
   - 更新此 README.md

---

## 🔍 模組詳細說明

### 1. talent-grading（人才評級系統）

**評級標準**：S/A+/A/B/C（90-100/80-89/70-79/60-69/<60）

**6 大維度**：
1. 學歷背景 (20%)
2. 工作年資 (20%)
3. 技能廣度 (20%)
4. 工作穩定性 (20%)
5. 職涯發展軌跡 (10%)
6. 特殊加分 (10%)

**詳見**：`talent-grading/README.md`

---

### 2. ai-matcher（AI 配對系統）

**評級標準**：P0/P1/P2（80+/60-79/40-59）

**配對因素**：
1. 技能匹配 (40%)
2. 年資匹配 (20%)
3. 學歷匹配 (15%)
4. 工作穩定性 (15%)
5. 產業經驗 (10%)

**詳見**：`ai-matcher/README.md`

---

### 3. resume-parser（履歷解析）

**監控來源**：
- Gmail 收件匣（關鍵字：應徵、履歷）
- Telegram Topic 4（履歷進件）⚠️ 待整合

**輸出格式**：
- 20 欄位結構化 JSON
- 自動計算穩定度評分
- 匯入 Google Sheets 履歷池

**詳見**：`resume-parser/README.md`

---

### 4. dedup-engine（去重引擎）

**去重邏輯**：
- Email 完全比對
- 姓名 + 電話模糊比對
- GitHub URL 比對
- LinkedIn URL 比對

**使用**：
```python
from dedup_engine import deduplicate_candidates
unique_candidates = deduplicate_candidates(candidate_list)
```

---

### 5. learning-engine（學習引擎）

**功能**：
- 記錄配對成功/失敗案例
- 分析配對因素權重
- 優化配對演算法

**資料來源**：
- 配對歷史記錄
- 面試結果回饋
- 最終錄取結果

---

### 6-8. 搜尋模組

**github-talent-search**：
- 搜尋 GitHub 活躍開發者
- 技能推斷（分析 repos）
- 聯絡方式提取

**linkedin-search**：
- LinkedIn 公開搜尋
- 職位與技能匹配
- 公司與產業過濾

**multi-channel-sourcing**：
- 整合 GitHub + LinkedIn + CakeResume
- 自動去重
- 統一輸出格式

---

## 🚀 開發路線圖

### 已完成
- ✅ ai-matcher v2（穩定度權重整合）
- ✅ resume-parser（Gmail 監控）
- ✅ dedup-engine（Email + 姓名去重）
- ✅ multi-channel-sourcing（三管道整合）

### 進行中
- 🔄 talent-grading（評分邏輯實作）
- 🔄 resume-parser（Telegram 整合）

### 規劃中
- 📋 ai-matcher v3（加入文化匹配）
- 📋 skill-recommender（技能推薦系統）
- 📋 salary-estimator（薪資評估模組）

---

## 📞 支援

**問題回報**：GitHub Issues  
**技術討論**：Telegram @YuQi0923_bot  
**貢獻指南**：提交 PR

---

**最後更新**：2026-02-23  
**維護者**：YuQi (@YuQi0923_bot)
