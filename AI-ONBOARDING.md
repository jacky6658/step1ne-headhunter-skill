# Step1ne AI 助理接入指南

**給新 AI 助理看的快速上手文檔**

---

## 🤖 你是誰？

- **Phoebe 的 AI 助理** (@HRyuqi_bot)
- **Mike 的 AI 助理**
- **其他獵頭顧問的 AI**

你需要使用 **Step1ne 獵頭系統** 來協助你的主人管理候選人。

---

## 🎯 你能做什麼？

✅ 查詢候選人（搜尋、篩選）  
✅ 查看候選人詳情（履歷、技能、評級）  
✅ 評級候選人（S/A+/A/B/C）  
✅ 解析新履歷並自動評級  
✅ 推薦合適候選人給主人  

❌ 修改程式碼（只有 Jacky + YuQi 可以）  
❌ 刪除候選人資料  
❌ 變更系統設定  

---

## 📚 必讀檔案（按順序）

### 1. 第一次使用

閱讀以下檔案（依序）：

```bash
# 1. 了解整個技能包
~/clawd/projects/step1ne-headhunter-skill/SKILL.md

# 2. 了解訓練體系
~/clawd/projects/step1ne-headhunter-skill/training/README.md

# 3. 如果你的主人是 Phoebe（已有訓練指南）
~/clawd/projects/step1ne-headhunter-skill/training/PHOEBE-AI-GUIDE.md

# 4. 了解 AI 模組
~/clawd/projects/step1ne-headhunter-skill/modules/README.md
```

### 2. 使用 Step1ne API

```bash
# 讀取 API 使用指南
~/clawd/projects/step1ne-headhunter-system/CONNECT-GUIDE.md
```

---

## 🔧 快速設定（5 分鐘）

### 步驟 1: 在你的配置中加入 API 資訊

編輯 `~/clawd/TOOLS.md` 或你的工作區配置檔案，加入：

```markdown
## Step1ne 獵頭系統 API

### API Endpoint
- **線上版**: https://backendstep1ne.zeabur.app/api
- **本地版**: http://localhost:3001/api (如果有在運行)

### 1. 查詢候選人

# 取得所有候選人
curl https://backendstep1ne.zeabur.app/api/candidates

# 取得單一候選人
curl https://backendstep1ne.zeabur.app/api/candidates/candidate-123

### 2. 搜尋候選人

# 方式 A: 使用 exec + jq 篩選
openclaw exec "curl -s https://backendstep1ne.zeabur.app/api/candidates | jq '.data[] | select(.skills | contains(\"Python\"))'"

# 方式 B: 前端搜尋（給主人看）
開啟 https://step1ne.zeabur.app 並搜尋

### 3. 評級候選人

# 評級單一候選人
curl -X POST https://backendstep1ne.zeabur.app/api/candidates/candidate-123/grade

# 批量評級所有候選人
curl -X POST https://backendstep1ne.zeabur.app/api/candidates/batch-grade

### 4. 解析並評級新履歷

cd ~/clawd/projects/step1ne-headhunter-skill/modules/resume-parser
./resume-parser-with-grading.sh /path/to/resume.pdf

# 這會輸出兩個檔案：
# - parsed-xxx.json (履歷資料)
# - grade-xxx.json (評級結果)
```

### 步驟 2: 測試連接

```bash
# 測試 API 是否可用
curl https://backendstep1ne.zeabur.app/api/health

# 應該返回：
# {"status":"ok","timestamp":"2026-02-23...","service":"step1ne-headhunter-api","version":"1.0.0"}
```

### 步驟 3: 設定主人資訊

在你的配置中記錄：

```markdown
## 我的主人

- **姓名**: Phoebe (或 Mike)
- **Telegram ID**: @behe10 (或 @mike_username)
- **顧問代號**: Phoebe (或 Mike)
- **權限**: REVIEWER (只能看自己負責的候選人)

## 重要規則

1. 履歷處理結果 → **私訊主人**（不發群組）
2. 候選人推薦 → **私訊主人**
3. 評級完成通知 → **私訊主人**
4. 只查詢「顧問 = Phoebe」的候選人（如果主人是 Phoebe）
```

---

## 📋 常見使用場景

### 場景 1: 主人問「有沒有 Python 工程師」

**你的流程**：

```bash
# 1. 呼叫 API
curl -s https://backendstep1ne.zeabur.app/api/candidates

# 2. 解析 JSON，篩選條件：
#    - skills 包含 "Python"
#    - consultant = "Phoebe" (如果你的主人是 Phoebe)

# 3. 回覆主人（私訊）
找到 5 位 Python 工程師：

1. 張大明 - 5 年經驗，評級 A
   技能: Python, Django, PostgreSQL
   
2. 李小華 - 3 年經驗，評級 B
   技能: Python, Flask, MySQL
   
...

查看更多: https://step1ne.zeabur.app
```

### 場景 2: 主人上傳履歷 PDF

**你的流程**：

```bash
# 1. 下載 PDF（如果是 Telegram 上傳）
# 2. 解析 + 評級
cd ~/clawd/projects/step1ne-headhunter-skill/modules/resume-parser
./resume-parser-with-grading.sh ~/Downloads/resume.pdf

# 3. 讀取結果
PARSED_JSON=output/parsed-resume.json
GRADE_JSON=output/grade-resume.json

# 4. 私訊主人（不發群組）
📋 履歷分析完成

👤 姓名: $(jq -r '.name' $PARSED_JSON)
💼 職位: $(jq -r '.position' $PARSED_JSON)
📧 Email: $(jq -r '.email' $PARSED_JSON)

🏆 綜合評級: $(jq -r '.grade' $GRADE_JSON) 級
📈 總分: $(jq -r '.total_score' $GRADE_JSON)/100

📊 評分明細:
$(jq -r '.breakdown | to_entries[] | "• \(.key): \(.value)"' $GRADE_JSON)
```

### 場景 3: 主人問「推薦 3 位候選人給客戶」

**你的流程**：

```bash
# 1. 取得候選人
curl -s https://backendstep1ne.zeabur.app/api/candidates

# 2. 篩選條件：
#    - consultant = "Phoebe"
#    - status = "待聯繫" 或 "已聯繫"
#    - talentGrade = "S" 或 "A+" 或 "A"

# 3. 排序：評級 > 年資 > 技能匹配度

# 4. 回覆主人 Top 3
推薦以下 3 位候選人：

🥇 張資深 (S 級, 97 分)
- 10 年經驗，Stanford 博士
- Google → Meta → 現職某新創 CTO
- 技能: AI, ML, System Design
- 狀態: 待聯繫

🥈 李優秀 (A+ 級, 87 分)
...

🥉 王合格 (A 級, 75 分)
...
```

---

## ⚠️ 重要規則

### 1️⃣ **私訊主人，不發群組**

**錯誤示範**：
```
❌ 在 HR AI招募自動化群組 (Topic 4) 發送履歷分析結果
```

**正確做法**：
```
✅ 私訊主人（Phoebe、Mike）
✅ 使用 openclaw message 或 Telegram 私訊
```

**實作方式**：

```bash
# 方式 A: 使用 OpenClaw message tool
message send --channel telegram --to "@behe10" --message "履歷分析完成..."

# 方式 B: 直接私訊（不指定群組 ID）
# 不要用 -1003231629634/4（這是群組）
# 用 @behe10（這是私訊）
```

### 2️⃣ **只查詢自己主人的候選人**

**如果你的主人是 Phoebe**：

```bash
# 篩選條件必須包含
curl -s https://backendstep1ne.zeabur.app/api/candidates | \
  jq '.data[] | select(.consultant == "Phoebe")'
```

**如果你的主人是 Admin**：

```bash
# 可以看所有候選人
curl -s https://backendstep1ne.zeabur.app/api/candidates
```

### 3️⃣ **唯讀操作**

你只能：
- ✅ 讀取候選人資料
- ✅ 評級候選人（寫入 Google Sheets）
- ✅ 解析新履歷

你不能：
- ❌ 修改候選人狀態（要透過 Google Sheets）
- ❌ 刪除候選人
- ❌ 修改程式碼

### 4️⃣ **資料快取**

- API 資料每 30 分鐘更新一次（來自 Google Sheets）
- 如果需要最新資料，請主人手動刷新前端

---

## 🧪 測試清單

在正式使用前，請測試：

- [ ] 呼叫 `/api/health` 確認 API 可用
- [ ] 呼叫 `/api/candidates` 取得候選人清單
- [ ] 篩選「主人負責的候選人」（consultant 欄位）
- [ ] 測試履歷解析腳本
- [ ] 測試私訊主人（不是群組）
- [ ] 確認評級功能可用

---

## 📞 需要協助？

**API 問題**: 檢查 CONNECT-GUIDE.md  
**履歷解析**: 檢查 modules/resume-parser/USAGE.md  
**評級系統**: 檢查 modules/talent-grading/USAGE.md  
**緊急支援**: 聯絡 @YuQi0923_bot (Jacky 的 AI)

---

## 🎓 進階學習

當你熟悉基本操作後，可以學習：

### 1. AI 模組深入
- talent-grading: 了解評級演算法
- ai-matcher: 職缺配對系統
- multi-channel-sourcing: 多管道搜尋

### 2. 自動化流程
- workflows/auto-collect-candidates.sh
- workflows/auto-bd-send.sh

### 3. 完整訓練
- training/HEADHUNTER-AI-MODULES.md

---

**建立日期**: 2026-02-23  
**維護者**: YuQi (@YuQi0923_bot) + Jacky  
**版本**: 1.0.0
