# 匿名履歷生成系統

## 📋 概述

**統一範本保證**：所有 AI Bot（YQ1/YQ2/YQ3）生成的匿名履歷都使用同一個範本，確保格式 100% 一致。

## 🎯 用途

給客戶公司篩選候選人時使用，保護候選人隱私的同時提供完整資訊。

## 📂 檔案結構

```
skills/headhunter/
├── templates/
│   ├── anonymous-resume-template.md  ← 統一範本（所有 Bot 共用）
│   └── README-ANONYMOUS-RESUME.md   ← 本說明文件
├── scripts/
│   └── anonymize-resume.py          ← 匿名化腳本
└── examples/
    ├── candidate-sample.json        ← 候選人資料範例
    └── job-sample.json              ← 職缺資料範例
```

## 🚀 快速開始

### 方法 1：使用 Python 腳本

```bash
cd /Users/user/clawd/projects/step1ne-headhunter-skill/skills/headhunter

# 生成匿名履歷
python scripts/anonymize-resume.py \
  examples/candidate-sample.json \
  examples/job-sample.json \
  "Jacky Chen"

# 輸出：anonymous-resume-1.md
```

### 方法 2：API 呼叫（系統整合後）

```bash
# POST /api/candidates/:id/anonymous-resume/pdf
curl -X POST http://localhost:3001/api/candidates/123/anonymous-resume/pdf \
  -H "Content-Type: application/json" \
  -d '{
    "jobId": "job-456",
    "consultantName": "Jacky Chen"
  }'

# 回傳：PDF 檔案下載
```

## 📝 範本變數說明

### 必填變數（26 個）

| 類別 | 變數名稱 | 範例 |
|------|---------|------|
| **基本** | RECOMMENDATION_DATE | 2024-02-15 |
| | CLIENT_COMPANY | 創樂科技有限公司 |
| | JOB_TITLE | Product Manager |
| | CANDIDATE_CODE | Abeni |
| **個人** | BIRTH_YEAR | 1992 |
| | AGE | 34 |
| | LANGUAGE_SKILLS | Chinese: Native, English: IELTS 5.0 |
| | MARITAL_STATUS | Single |
| | NATIONALITY | Taiwan Citizen |
| | RESIDENCE | Taipei City |
| **學歷** | EDUCATION | 東南科技大學 / 工管系 / 2013/6 |
| **專業** | SUMMARY | 遊戲產業 PM 經驗 2+ 年... |
| | SKILLS | 專案管理工具：Jira、Confluence... |
| | WORK_EXPERIENCE | （格式化工作經歷） |
| **薪資** | PREVIOUS_SALARY | 年薪約 100 萬 |
| | CURRENT_SALARY | 年薪約 72 萬 |
| | EXPECTED_SALARY | 月薪 7.5萬 up |
| | ON_BOARD_DATE | One month notice period |
| **推薦** | RECOMMENDATION_REASON | 此候選人目前在遊戲公司... |
| | MATCH_ANALYSIS | ✅ PM 經驗... |
| | CONSULTANT_NAME | Jacky Chen |

### 選填變數（4 個）

| 變數 | 說明 |
|------|------|
| CERTIFICATIONS | 證照（無則填「無」） |
| OTHER_INFO | 其他資訊（無則填「無」） |
| SALARY_NOTE | 薪資備註（可留空） |
| SUGGESTIONS | 建議（可留空） |

## 🔒 匿名化規則

### 1. 人選姓名 → 代號

**選項 A：英文代號**（推薦）
```
Abeni, Sarah, Kevin, David, Emily...
```

**選項 B：職位代號**
```
PM-2026-001, BE-2026-002, FE-2026-003...
```

### 2. 公司名稱 → 匿名化

| 原始 | 匿名化 | 保留資訊 |
|------|--------|---------|
| 遊戲橘子 | 某遊戲科技公司 | 網路服務業，30-100人 ✅ |
| PChome | 某知名電商平台 | 電子商務，500-1000人 ✅ |
| 街口支付 | 某金融科技公司 | FinTech，100-500人 ✅ |

**為什麼保留產業和規模？**
- 客戶需要評估候選人背景（大公司 vs 新創）
- 產業經驗很重要（金融業 vs 遊戲業）
- 不會洩露候選人身份（同產業公司很多）

### 3. 學校名稱 → 保留

**原則**：學校名稱保留（公開資訊）

```
台灣大學 ✅
成功大學 ✅
東南科技大學 ✅
```

## 🎨 格式規範

### 工作經歷格式

```
某遊戲科技公司（網路服務業，30-100人）

任職期間：2025年10月 ~ 現在（在職中）

職稱：PM（專案經理）

工作內容：
• 負責撲克 APP 產品規劃（含 X-Poker、GGClub 等產品研究）
• 規劃功能設計：大廳功能、桌檯功能、俱樂部系統
• 撰寫產品規格文件（PRD）：詳細玩法規則、功能需求、操作流程

成就/專案：
• 完成 X-Poker APP 完整產品規劃（大廳、俱樂部、桌檯三大模組）

離職原因：仍在職（尋求更好的發展機會）
```

### 匹配度分析格式

```
✅ Product Manager 經驗（目前職位）
✅ 遊戲產業經驗（撲克 APP）
✅ 撰寫 PRD（產品規格文件）
✅ 跨部門協作能力
✅ 10+ 年工作經驗
```

## ✅ 品質檢查清單

生成前必檢查：

- [ ] 所有 `{{變數}}` 都已替換
- [ ] 公司名稱已匿名化
- [ ] 候選人代號已生成
- [ ] 工作經歷格式一致
- [ ] 保密聲明存在（頁首）
- [ ] 推薦顧問簽名（頁尾）
- [ ] 推薦理由與匹配度分析已填寫
- [ ] 薪資資訊完整
- [ ] 格式符合範本

## 🔧 整合指南

### Backend API（Node.js）

```javascript
// server/anonymousResumeService.js
const { exec } = require('child_process');
const path = require('path');

async function generateAnonymousResume(candidateId, jobId, consultantName) {
  const scriptPath = path.join(__dirname, 
    '../../step1ne-headhunter-skill/skills/headhunter/scripts/anonymize-resume.py');
  
  const candidateFile = `/tmp/candidate-${candidateId}.json`;
  const jobFile = `/tmp/job-${jobId}.json`;
  
  // 1. 準備資料檔案
  await writeCandidateData(candidateId, candidateFile);
  await writeJobData(jobId, jobFile);
  
  // 2. 呼叫 Python 腳本
  return new Promise((resolve, reject) => {
    exec(
      `python3 "${scriptPath}" "${candidateFile}" "${jobFile}" "${consultantName}"`,
      (error, stdout, stderr) => {
        if (error) {
          reject(error);
        } else {
          resolve(stdout);
        }
      }
    );
  });
}
```

### Frontend（React）

```tsx
// 下載匿名履歷 PDF
const handleDownloadAnonymousResume = async (candidateId: number, jobId: number) => {
  try {
    const response = await fetch(
      `/api/candidates/${candidateId}/anonymous-resume/pdf`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          jobId, 
          consultantName: 'Jacky Chen' 
        })
      }
    );
    
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `anonymous-resume-${candidateId}.pdf`;
    a.click();
  } catch (error) {
    console.error('下載失敗', error);
  }
};
```

## 🧪 測試

```bash
# 測試範例
cd /Users/user/clawd/projects/step1ne-headhunter-skill/skills/headhunter

python scripts/anonymize-resume.py \
  examples/candidate-sample.json \
  examples/job-sample.json \
  "Jacky Chen"

# 檢查輸出
cat anonymous-resume-1.md

# 預期：
# - 公司名稱已匿名化（遊戲橘子 → 某遊戲科技公司）
# - 人選代號已生成（Abeni 或 PM-2026-001）
# - 格式完全符合範本
```

## 📊 版本控制

| 版本 | 日期 | 變更內容 |
|------|------|---------|
| 1.0 | 2026-02-23 | 初版建立，基於 Abeni 範例 PDF |

## 🔗 相關文件

- `anonymous-resume-template.md` - 完整範本（含變數說明）
- `anonymize-resume.py` - Python 實作
- `candidate-sample.json` - 候選人資料範例
- `job-sample.json` - 職缺資料範例

## 💡 重要提醒

**統一範本保證**：

所有 AI Bot（YQ1/YQ2/YQ3）生成的匿名履歷都必須使用 `anonymous-resume-template.md`，確保：

1. ✅ 格式 100% 一致
2. ✅ 品牌形象統一
3. ✅ 客戶體驗一致
4. ✅ 匿名化規則統一

**禁止**：
- ❌ 自行修改範本格式
- ❌ 使用其他範本
- ❌ 遺漏保密聲明
- ❌ 遺漏推薦理由

## 🆘 常見問題

### Q1：如何新增公司匿名化規則？

編輯 `anonymize-resume.py`：

```python
COMPANY_ANONYMIZATION = {
    '遊戲橘子': '某遊戲科技公司',
    'PChome': '某知名電商平台',
    # 新增：
    '你的公司': '某XX公司',
}
```

### Q2：如何自訂候選人代號？

```python
# 選項 A：使用英文代號（預設）
candidate_code = generate_candidate_code(candidate_data, use_job_code=False)
# 輸出：Abeni

# 選項 B：使用職位代號
candidate_code = generate_candidate_code(candidate_data, use_job_code=True)
# 輸出：PM-2026-001
```

### Q3：為什麼要保留公司規模和產業？

幫助客戶評估候選人背景，同時不洩露身份：
- 某遊戲科技公司（30-100人）← 台灣有數百家
- 某金融機構（1000+人）← 無法精確判斷是哪一家

### Q4：PDF 生成功能在哪裡？

明天（2026-02-24）會實作：
- Backend: `POST /api/candidates/:id/anonymous-resume/pdf`
- Frontend: 「📄 匿名履歷」按鈕

---

**建立日期**：2026-02-23  
**維護者**：Step1ne Team  
**聯絡人**：Jacky Chen
