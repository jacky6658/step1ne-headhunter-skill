# LinkedIn 履歷處理完整流程

**版本**：1.0.0  
**最後更新**：2026-02-24  
**適用對象**：所有獵頭顧問的 AI bot

---

## 📋 **目錄**

1. [履歷處理流程總覽](#履歷處理流程總覽)
2. [LinkedIn 履歷結構（4 區塊）](#linkedin-履歷結構)
3. [步驟 1：收到履歷 PDF](#步驟1收到履歷pdf)
4. [步驟 2：上傳到 Google Drive](#步驟2上傳到google-drive)
5. [步驟 3：深度解析履歷](#步驟3深度解析履歷)
6. [步驟 4：搜尋履歷池](#步驟4搜尋履歷池)
7. [步驟 5：更新或新增候選人](#步驟5更新或新增候選人)
8. [步驟 6：AI 配對與推薦](#步驟6ai-配對與推薦)
9. [步驟 7：生成匿名履歷](#步驟7生成匿名履歷)
10. [其他獵頭顧問 AI bot 使用流程](#其他獵頭顧問使用流程)
11. [常見問題 Q&A](#常見問題)

---

## 📊 **履歷處理流程總覽**

```
收到 LinkedIn PDF
    ↓
上傳到 Google Drive（資料夾 ID: 16IOJW0jR2mBgzBnc5QI_jEHcRBw3VnKj）
    ↓
AI 深度解析（4 區塊：簡介、聯絡方式、工作經歷、學歷）
    ↓
搜尋履歷池（LinkedIn URL / 姓名）
    ↓
找到 → 更新資料 + 補充履歷連結
找不到 → 新增候選人（21 欄位）
    ↓
前端自動同步（30 秒）
    ↓
AI 配對職缺（技能、年資、學歷、穩定度）
    ↓
生成匿名履歷（POST /api/candidates/:id/anonymous-resume）
    ↓
發送給客戶
```

---

## 📄 **LinkedIn 履歷結構**

### **4 個區塊（必須深度解析）**

#### **圖1 - 簡介**
- **內容**：完整自我介紹、職業亮點、成就摘要
- **用途**：了解候選人的核心優勢與特色
- **範例**：
  ```
  30年工程文件管理經驗，專精 PLM/PDM 系統管理。
  曾主導 ISO 9001/13485 內稽專案，熟悉國際品質標準。
  ```

#### **圖2 - 聯絡方式與技能**
- **內容**：LinkedIn URL、熱門技能清單、聯絡方式
- **用途**：提取技能關鍵字、建立聯繫管道
- **範例**：
  ```
  LinkedIn: linkedin.com/in/maggie-chen-472b79137
  熱門技能: PLM, PDM, MAX, ISO9001, ISO13485, Microsoft Office, 
           Photoshop, CorelDRAW, Illustrator, AutoCAD, PCB Layout
  ```

#### **圖3 - 工作經歷**
- **內容**：詳細職責、專案經驗、任職時間
- **用途**：計算穩定度評分、提取核心能力
- **範例**：
  ```
  Pivot International (1995-now, 30年)
  - 工程文件管理師
  - 系統講師
  - Change Approver
  - ISO 內稽人員
  
  八動股份 (1993-1994, 1年)
  - 業務助理
  ```

#### **圖4 - 學歷**
- **內容**：學校、科系、年份
- **用途**：學歷背景評分（博士100分、碩士85分、學士70分）
- **範例**：
  ```
  學士學位
  ```

---

## 🚀 **步驟 1：收到履歷 PDF**

### **來源管道**
1. **Telegram 直接上傳**
2. **Gmail 附件**（自動監控）
3. **手動下載後上傳**

### **檔案命名規則**
```
格式：{姓名}-{應徵公司}.pdf
範例：Maggie Chen-Pivot.pdf
```

**重要**：應徵公司由 AI 與獵頭顧問互動確認（不要猜測）

---

## 📁 **步驟 2：上傳到 Google Drive**

### **Google Drive 設定**
- **資料夾名稱**：履歷庫
- **資料夾 ID**：`16IOJW0jR2mBgzBnc5QI_jEHcRBw3VnKj`
- **資料夾 URL**：https://drive.google.com/drive/folders/16IOJW0jR2mBgzBnc5QI_jEHcRBw3VnKj
- **帳號**：aijessie88@step1ne.com

### **上傳指令**
```bash
gog drive upload \
  --account aijessie88@step1ne.com \
  --parent-id 16IOJW0jR2mBgzBnc5QI_jEHcRBw3VnKj \
  --file "/path/to/Maggie Chen-Pivot.pdf"
```

### **取得 File ID**
```bash
# 上傳成功後會返回 File ID
FILE_ID="12YJ5jPHykfQsmXb4uP9I4ybLQKreRKbP"

# 生成嵌入式預覽 URL
PREVIEW_URL="https://drive.google.com/file/d/${FILE_ID}/preview"
```

---

## 🧠 **步驟 3：深度解析履歷**

### **解析目標（21 個欄位）**

| 欄位 | 來源 | 範例 |
|------|------|------|
| 姓名 | 圖1/圖2 | Maggie Chen |
| Email/LinkedIn | 圖2 | LinkedIn: maggie-chen-472b79137 |
| 電話 | 圖2 | （如有） |
| 地點 | 圖1/圖2 | 新北市 |
| 目前職位 | 圖3（最近一份工作） | 工程文件管理師/PLM&PDM系統管理師 |
| 總年資(年) | 圖3（加總） | 30 |
| 轉職次數 | 圖3（公司數量-1） | 1 |
| 平均任職(月) | 圖3（總月數/公司數） | 360 |
| 最近gap(月) | 圖3（計算間隔） | 0 |
| 技能 | 圖2 | PLM, PDM, MAX, ISO9001, ISO13485, ... |
| 學歷 | 圖4 | 學士 |
| 來源 | 系統 | Gmail / LinkedIn / GitHub |
| 工作經歷 | 圖3（結構化） | Pivot 30年 + 八動 1年 |
| 離職原因 | 圖3（如有） |  |
| 穩定性評分 | 計算 | 95 |
| 學歷JSON | 圖4（JSON） |  |
| DISC/Big Five | （待評估） |  |
| 狀態 | 預設 | 待審核 |
| 獵頭顧問 | 系統 | Jacky / Phoebe |
| 備註 | （如有） | 2026-02-24 |
| 履歷連結 | Google Drive | https://drive.google.com/.../preview |

### **穩定度評分計算**
```python
穩定度評分 = (100 - 轉職次數 × 10) × 0.4
           + (平均任職月數 / 12) × 5 × 0.3
           + (100 - 最近gap月數 × 5) × 0.3

範圍：0-100 分
等級：
  A 級：≥ 80 分
  B 級：60-79 分
  C 級：40-59 分
  D 級：20-39 分
  F 級：< 20 分
```

**Maggie Chen 範例**：
```
穩定度 = (100 - 1×10) × 0.4 + (360/12) × 5 × 0.3 + (100 - 0×5) × 0.3
       = 90 × 0.4 + 30 × 5 × 0.3 + 100 × 0.3
       = 36 + 45 + 30
       = 111（上限100） → 95 分（A 級）
```

---

## 🔍 **步驟 4：搜尋履歷池**

### **搜尋策略（優先順序）**

#### **1. LinkedIn URL 搜尋（最優先）**
```bash
# 從履歷池搜尋（B 欄 = Email/LinkedIn）
SEARCH_RESULT=$(gog sheets get "$SHEET_ID" "履歷池v2!B:B" --account "$ACCOUNT" | grep -n "maggie-chen-472b79137")

# 如果找到 → 取得行號
if [ -n "$SEARCH_RESULT" ]; then
  ROW=$(echo "$SEARCH_RESULT" | cut -d: -f1)
  echo "找到現有候選人：Row $ROW"
fi
```

#### **2. 姓名搜尋（次選）**
```bash
# 如果 LinkedIn 找不到，改用姓名
SEARCH_RESULT=$(gog sheets get "$SHEET_ID" "履歷池v2!A:A" --account "$ACCOUNT" | grep -n "Maggie Chen")
```

**注意**：姓名可能重複，需要進一步確認（比對技能、公司等）

---

## ✍️ **步驟 5：更新或新增候選人**

### **5A. 找到現有候選人 → 更新流程**

**更新策略**：補充詳細資料，保留原負責顧問

**需要更新的欄位**：
- D 欄（地點）
- E 欄（目前職位）
- G 欄（轉職次數）
- H 欄（平均任職）
- J 欄（技能）- **使用逗號分隔，絕對不用 `|`**
- M 欄（工作經歷）
- O 欄（穩定性評分）
- U 欄（履歷連結）

**更新指令**（使用 `--values-json`）：
```bash
# ✅ 正確方式：使用 --values-json
gog sheets update "$SHEET_ID" "履歷池v2!J2" \
  --values-json '[["PLM, PDM, MAX, ISO9001, ISO13485, ..."]]' \
  --account "$ACCOUNT"

# ❌ 錯誤方式：直接傳字串（逗號會被當成換行）
gog sheets update "$SHEET_ID" "履歷池v2!J2" "PLM, PDM, MAX, ..."  # 會炸！
```

**重要規則**：
1. ✅ **絕對不要在資料內使用 `|` 符號**（gog sheets 的欄位分隔符）
2. ✅ 技能用逗號分隔：`PLM, PDM, MAX`
3. ✅ 工作經歷用分號分隔：`公司A; 公司B`
4. ✅ 所有更新都用 `--values-json '[["data"]]'`

### **5B. 找不到候選人 → 新增流程**

**新增指令**（21 個欄位）：
```bash
# 使用專用腳本（推薦）
/Users/user/clawd/projects/step1ne-headhunter-skill/skills/headhunter/scripts/import-resume-to-pool.sh

# 或手動新增（確保欄位數量正確）
DATA="姓名|Email|電話|地點|職位|總年資|轉職次數|平均任職|最近gap|技能|學歷|來源|工作經歷|離職原因|穩定性評分|學歷JSON|DISC|狀態|獵頭顧問|備註|履歷連結"

gog sheets append "$SHEET_ID" "履歷池v2!A:U" \
  --values-json "[$(echo "$DATA" | sed 's/|/","/g' | sed 's/^/["/' | sed 's/$/"]/')] \
  --account "$ACCOUNT"
```

**負責顧問規則**：
- Jacky 傳送的履歷 → 顧問 = "Jacky"
- Phoebe 傳送的履歷 → 顧問 = "Phoebe"
- 系統自動匯入 → 顧問 = ""（未指派）

---

## 🎯 **步驟 6：AI 配對與推薦**

### **配對流程（Phoebe 的 AI bot 使用 Jacky 新增的履歷）**

```
【情境】Phoebe 要推薦 Maggie Chen 給「律准聯合 - BIM工程師」職缺

1. Phoebe AI bot → 搜尋履歷池
   ↓
   curl "https://step1ne.zeabur.app/api/candidates?search=Maggie Chen"
   ↓
2. 取得候選人資料（包含 resumeLink）
   ↓
   {
     "id": "2",
     "name": "Maggie Chen",
     "resumeLink": "https://drive.google.com/file/d/12YJ5jPHykfQsmXb4uP9I4ybLQKreRKbP/preview",
     "skills": ["PLM", "PDM", "MAX", ...],
     "years": 30,
     "stabilityScore": 95
   }
   ↓
3. 下載 Google Drive PDF（可選）
   ↓
   wget "https://drive.google.com/uc?export=download&id=12YJ5jPHykfQsmXb4uP9I4ybLQKreRKbP" \
     -O "Maggie Chen.pdf"
   ↓
4. AI 配對分析（4 維度）
   ↓
   - 技能匹配度（35%）：BIM 相關技能 vs Maggie 的技能
   - 成長潛力（25%）：年資 30 年（經驗豐富）
   - 文化適配度（25%）：穩定性 95 分（A 級）
   - 動機契合度（15%）：待評估
   ↓
5. 生成配對報告
   ↓
   {
     "matchScore": 75.3,
     "grade": "B",  // P0/P1/P2
     "recommendation": "推薦",
     "reasons": [
       "30 年工程管理經驗（符合資深要求）",
       "熟悉 PLM/PDM 系統（與 BIM 有相關性）",
       "穩定性極高（95 分，A 級）"
     ],
     "concerns": [
       "技能需轉換（PLM → BIM）",
       "需確認學習意願"
     ]
   }
```

### **配對評分公式（方案A權重）**
```python
總分 = 技能匹配度(35%) + 成長潛力(25%) + 文化適配度(25%) + 動機契合度(15%)

等級：
  P0（強烈推薦）：≥ 80 分
  P1（推薦）：60-79 分
  P2（備選）：40-59 分
  REJECT（不推薦）：< 40 分
```

---

## 📝 **步驟 7：生成匿名履歷**

### **API 呼叫**
```bash
# 生成候選人 2（Maggie Chen）的匿名履歷，針對職缺 47
curl -X POST "https://backendstep1ne.zeabur.app/api/candidates/2/anonymous-resume?jobId=47" \
  -H "Content-Type: application/json" \
  -o "Maggie_Chen_anonymous.md"
```

### **匿名化規則**
- **真實姓名** → **候選人代號**（Michael / Sarah / David）
- **真實公司** → **匿名公司**（知名遊戲公司 / AI科技公司）
- **聯絡方式** → **移除**
- **保留技能、經歷、學歷**

### **輸出格式**
```markdown
# 候選人檔案：Michael

## 基本資料
- 候選人代號：Michael
- 目前職位：工程文件管理師/PLM系統管理師
- 總年資：30 年
- 期望地點：新北市
- 工作穩定性：A 級（95 分）

## 核心技能
- PLM/PDM 系統管理
- ISO 9001/13485 品質管理
- 工程文件管理
- ...

## 工作經歷
### 知名製造業集團（30 年）
- 工程文件管理師
- 系統講師
- Change Approver
- ISO 內稽人員

### 知名企業（1 年）
- 業務助理

## 學歷背景
- 學士學位

## 匹配分析
- 技能匹配度：75%
- 推薦等級：B（P1 推薦）
```

---

## 👥 **其他獵頭顧問使用流程**

### **情境：Phoebe 的 AI bot 要使用 Jacky 新增的履歷**

#### **前提條件**
- ✅ 履歷池是**共享的**（所有獵頭顧問都能查詢）
- ✅ resumeLink（U 欄）是**公開的**（Google Drive 權限設定）
- ✅ API 有**權限過濾**（REVIEWER 只能看自己的 + 未指派的）

#### **Phoebe AI bot 操作流程**
```bash
# 1. 搜尋候選人
curl "https://backendstep1ne.zeabur.app/api/candidates?search=Maggie Chen&userRole=REVIEWER&consultant=Phoebe"

# 2. 取得候選人資料（包含 resumeLink）
{
  "id": "2",
  "name": "Maggie Chen",
  "consultant": "Jacky",  // 注意：這是 Jacky 的候選人
  "resumeLink": "https://drive.google.com/.../preview"
}

# 3. 下載 PDF（如需深度分析）
wget "https://drive.google.com/uc?export=download&id=..." -O "Maggie_Chen.pdf"

# 4. AI 配對（使用 Phoebe 的職缺）
curl -X POST "https://backendstep1ne.zeabur.app/api/ai-matching" \
  -d '{"candidateId": "2", "jobId": "50", "consultant": "Phoebe"}'

# 5. 生成匿名履歷（針對 Phoebe 的客戶）
curl -X POST "https://backendstep1ne.zeabur.app/api/candidates/2/anonymous-resume?jobId=50"

# 6. 發送給客戶
# （Phoebe AI bot 自動寄送）
```

#### **權限說明**
- ✅ **查詢**：所有獵頭都能查詢履歷池（技能搜尋、姓名搜尋）
- ✅ **讀取**：都能讀取 resumeLink（Google Drive 公開）
- ❌ **修改**：只有負責顧問能修改候選人資料
- ❌ **指派**：不能強制更改負責顧問

---

## ❓ **常見問題**

### **Q1：如果候選人已經在履歷池中，要重新上傳履歷嗎？**
**A**：是的！流程：
1. 搜尋履歷池（找到 Row X）
2. 上傳新的 PDF 到 Google Drive
3. 更新 U 欄（履歷連結）
4. 補充詳細資料（如果有新資訊）

---

### **Q2：GitHub 來源的候選人沒有 PDF 履歷怎麼辦？**
**A**：選項：
- **選項 A**：主動邀請候選人提供履歷（LinkedIn 訊息）
- **選項 B**：用 GitHub Profile 當作履歷（README.md + Repos）
- **選項 C**：標記「僅技能配對」（不做完整評級）

---

### **Q3：如果 LinkedIn 履歷不是 4 區塊結構怎麼辦？**
**A**：
1. **簡化履歷**：盡可能提取資訊（姓名、技能、經歷）
2. **標記「資料不完整」**：備註欄記錄
3. **主動聯繫候選人**：請求完整履歷

---

### **Q4：穩定度評分為 0 或異常怎麼辦？**
**A**：檢查：
1. 工作經歷是否解析正確？
2. 轉職次數、任職時間是否計算錯誤？
3. 如果資料缺失，手動補充或標記「待評估」

---

### **Q5：履歷連結（U 欄）無法開啟？**
**A**：檢查：
1. File ID 是否正確？
2. Google Drive 權限是否設定為「知道連結的人可以檢視」？
3. 使用 `/preview` 而非 `/view`（嵌入式預覽）

---

## 📚 **相關文檔**

- [履歷池管理](/Users/user/clawd/projects/step1ne-headhunter-skill/docs/README-履歷池.md)
- [Google Drive 組織架構](/Users/user/clawd/projects/step1ne-headhunter-skill/GOOGLE-DRIVE-ORGANIZATION.md)
- [AI 配對系統](/Users/user/clawd/projects/step1ne-headhunter-skill/docs/OPENCLAW-INTEGRATION.md)
- [Bot 履歷上傳指南](/Users/user/clawd/projects/step1ne-headhunter-skill/docs/BOT-RESUME-UPLOAD-GUIDE.md)

---

## 📝 **更新日誌**

- **2026-02-24**：首次建立（v1.0.0）
- 包含完整的 LinkedIn 履歷處理流程（7 步驟）
- 新增其他獵頭顧問使用流程
- 新增常見問題 Q&A
