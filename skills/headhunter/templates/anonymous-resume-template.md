# Step1ne 匿名履歷範本（統一格式）

**重要**：所有 AI Bot 生成的匿名履歷都必須使用此範本，確保格式一致性。

---

## 完整範本

```
═══════════════════════════════════════════════════════════════════════
◈ STEP1NE

本資料由德仁管理顧問有限公司，提供致客戶進行工作職位媒合之使用，
不得轉交第二人，保護人選個資。相關授權文件已由人選提供致德仁管理顧問有限公司。

推薦日期：{{RECOMMENDATION_DATE}}
企業：{{CLIENT_COMPANY}}
職位：{{JOB_TITLE}}
人選：{{CANDIDATE_CODE}}
═══════════════════════════════════════════════════════════════════════

Personal Particulars

Candidate        {{CANDIDATE_CODE}}

Date of Birth    {{BIRTH_YEAR}}

Age              {{AGE}}

Language         {{LANGUAGE_SKILLS}}

Marital status   {{MARITAL_STATUS}}

Nationality      {{NATIONALITY}}

Residence        {{RESIDENCE}}

───────────────────────────────────────────────────────────────────────

Educational Background

學校 / 科系 / 畢業年度(月)
{{EDUCATION}}

───────────────────────────────────────────────────────────────────────

Summary 及個人特質、優勢

{{SUMMARY}}

───────────────────────────────────────────────────────────────────────

Skills

{{SKILLS}}

───────────────────────────────────────────────────────────────────────

Career Background / Achievement

{{WORK_EXPERIENCE}}

───────────────────────────────────────────────────────────────────────

Certifications

{{CERTIFICATIONS}}

───────────────────────────────────────────────────────────────────────

Other Information

{{OTHER_INFO}}

───────────────────────────────────────────────────────────────────────

Remuneration Package

項目              金額

Previous Package  {{PREVIOUS_SALARY}}

Current Package   {{CURRENT_SALARY}}

期待薪資          {{EXPECTED_SALARY}}

備註：{{SALARY_NOTE}}

On Board Date: {{ON_BOARD_DATE}}

───────────────────────────────────────────────────────────────────────

備註說明（給 {{CLIENT_COMPANY}} HR）

【推薦理由】
{{RECOMMENDATION_REASON}}

【匹配度分析】
{{MATCH_ANALYSIS}}

【建議】
{{SUGGESTIONS}}

推薦顧問：{{CONSULTANT_NAME}} (Step1ne)

═══════════════════════════════════════════════════════════════════════
```

---

## 變數說明

### 基本資訊（頁首）
| 變數 | 說明 | 範例 | 必填 |
|------|------|------|------|
| `RECOMMENDATION_DATE` | 推薦日期 | 2024-02-15 | ✅ |
| `CLIENT_COMPANY` | 客戶公司名稱 | 創樂科技有限公司 | ✅ |
| `JOB_TITLE` | 推薦職位 | Product Manager | ✅ |
| `CANDIDATE_CODE` | 候選人代號 | Abeni / PM-2026-001 | ✅ |

### Personal Particulars
| 變數 | 說明 | 範例 | 必填 |
|------|------|------|------|
| `BIRTH_YEAR` | 出生年 | 1992 | ✅ |
| `AGE` | 年齡 | 34 | ✅ |
| `LANGUAGE_SKILLS` | 語言能力 | Chinese: Native speaker，English: IELTS 5.0 | ✅ |
| `MARITAL_STATUS` | 婚姻狀態 | Single / Married | ✅ |
| `NATIONALITY` | 國籍 | Taiwan Citizen | ✅ |
| `RESIDENCE` | 居住地 | Taipei City | ✅ |

### 教育背景
| 變數 | 說明 | 範例 | 必填 |
|------|------|------|------|
| `EDUCATION` | 學校/科系/畢業年月 | 東南科技大學 / 工業工程與管理系 / 2013/6 | ✅ |

### Summary & Skills
| 變數 | 說明 | 範例 | 必填 |
|------|------|------|------|
| `SUMMARY` | 個人特質、優勢 | 遊戲產業 PM 經驗 2+ 年，目前負責撲克 APP 產品規劃... | ✅ |
| `SKILLS` | 技能列表 | 專案管理工具：Jira、Confluence<br>應用撰寫規劃書與產品規格文件（PRD）... | ✅ |

### 工作經歷
| 變數 | 說明 | 格式 | 必填 |
|------|------|------|------|
| `WORK_EXPERIENCE` | 工作經歷（多份） | 見「工作經歷格式」 | ✅ |

### 證照 & 其他
| 變數 | 說明 | 範例 | 必填 |
|------|------|------|------|
| `CERTIFICATIONS` | 證照列表 | PMP、TOEIC 850 | ❌ |
| `OTHER_INFO` | 其他資訊 | 可立即到職 | ❌ |

### 薪資結構
| 變數 | 說明 | 範例 | 必填 |
|------|------|------|------|
| `PREVIOUS_SALARY` | 前一份薪資 | 年薪約 100 萬（月薪 80-90K） | ✅ |
| `CURRENT_SALARY` | 現職薪資 | 年薪約 72 萬（轉職過渡期） | ✅ |
| `EXPECTED_SALARY` | 期待薪資 | 月薪 7.5 萬 up，年薪 120~150 萬 | ✅ |
| `SALARY_NOTE` | 薪資備註 | 候選人因轉職至遊戲產業累積相關經驗... | ❌ |
| `ON_BOARD_DATE` | 可到職日 | One month notice period | ✅ |

### 獵頭附加價值
| 變數 | 說明 | 範例 | 必填 |
|------|------|------|------|
| `RECOMMENDATION_REASON` | 推薦理由 | 此候選人目前在遊戲公司擔任 PM... | ✅ |
| `MATCH_ANALYSIS` | 匹配度分析 | ✅ Product Manager 經驗<br>✅ 遊戲產業經驗... | ✅ |
| `SUGGESTIONS` | 建議 | 候選人希望先了解詳細工作內容... | ❌ |
| `CONSULTANT_NAME` | 推薦顧問 | Jacky Chen | ✅ |

---

## 工作經歷格式（標準）

**每份工作必須包含以下結構**：

```
某遊戲科技公司（網路服務業，30-100人）

任職期間：2025年10月 ~ 現在（在職中）

職稱：PM（專案經理）

工作內容：
• 負責撲克 APP 產品規劃（含 X-Poker、GGClub 等產品研究）
• 規劃功能設計：大廳功能、桌檯功能、俱樂部系統
• 撰寫產品規格文件（PRD）：詳細玩法規則、功能需求、操作流程
• 規劃動畫觸發系統（Loading 畫面、互動動畫）
• 跨部門協作（RD / 美術 / 動畫），確保開發可行性

成就/專案：
• 完成 X-Poker APP 完整產品規劃（大廳、俱樂部、桌檯三大模組）

離職原因：仍在職（尋求更好的發展機會）
```

**重點**：
- 公司名稱**必須匿名化**（某遊戲科技公司）
- 保留產業類型和規模（網路服務業，30-100人）← 幫助客戶評估
- 工作內容用 bullet points（•）
- 成就/專案獨立列出

---

## 匿名化規則（強制執行）

### 1. 人選姓名匿名化

**代號命名規則**：
```
選項 A：英文代號（隨機生成）
- Abeni
- Sarah
- Kevin
- David

選項 B：職位代號（按序號）
- PM-2026-001
- BE-2026-002
- FE-2026-003
- DA-2026-004

職能代號對照表：
PM = Product Manager
BE = Backend Engineer
FE = Frontend Engineer
FS = Full Stack Engineer
DA = Data Analyst
DE = Data Engineer
QA = QA Engineer
DO = DevOps Engineer
```

**建議**：使用選項 A（英文代號）較自然

---

### 2. 公司名稱匿名化

**匿名化對照表**：

| 產業類型 | 原始公司名稱 | 匿名化後 | 保留資訊 |
|---------|------------|---------|---------|
| **遊戲產業** | 遊戲橘子 | 某遊戲科技公司 | 網路服務業，30-100人 |
| **科技新創** | 創樂科技 | 某網路服務公司 | 網路相關，30-100人 |
| **電商平台** | PChome | 某知名電商平台 | 電子商務，500-1000人 |
| **金融科技** | 街口支付 | 某金融科技公司 | FinTech，100-500人 |
| **製造業** | 鴻海精密 | 某製造業集團 | 電子製造，10000+人 |
| **外商科技** | Google Taiwan | 某外商科技公司 | 軟體開發，1000-5000人 |

**匿名化原則**：
1. ✅ 保留產業類型（遊戲、電商、金融、製造）
2. ✅ 保留公司規模（30-100人、500-1000人）
3. ✅ 保留業務性質（網路服務、電子製造）
4. ❌ 移除公司品牌名稱（遊戲橘子 → 某遊戲科技公司）

**為什麼保留這些資訊？**
- 客戶需要評估候選人的背景（大公司 vs 新創）
- 產業經驗很重要（金融業 vs 遊戲業）
- 不會洩露候選人身份（台灣有數百家遊戲公司）

---

### 3. 學校名稱處理

**原則**：可保留或部分匿名

| 學校類型 | 原始 | 選項 A（保留） | 選項 B（匿名） |
|---------|------|--------------|--------------|
| 台清交成 | 台灣大學 | 台灣大學 | 國立頂尖大學 |
| 國立大學 | 成功大學 | 成功大學 | 國立大學 |
| 私立名校 | 輔仁大學 | 輔仁大學 | 私立大學 |
| 科技大學 | 東南科技大學 | 東南科技大學 | 科技大學 |

**建議**：保留學校名稱（選項 A），因為：
- 學歷是公開資訊
- 幫助客戶評估候選人背景
- 不會洩露候選人身份（同校同系每年上百人）

---

## 範例填充

### SUMMARY 範例
```
遊戲產業 PM 經驗 2+ 年，目前負責撲克 APP 產品規劃
⦿ 熟悉產品從 0-1 完整流程，曾獨立交付 9-10 個包網平台專案
⦿ 產品規劃能力強：擅長競品分析、功能設計、PRD 撰寫
⦿ 跨部門協作經驗豐富：與 RD、美術、動畫團隊密切合作
⦿ 技術理解能力佳：熟悉 API 串接、上架流程（Apple/Google）
⦿ 團隊管理經驗：曾管理 RD/PM/QA 團隊，能有效分配工作優先順序
⦿ 執行力強，條理分明，能將產品需求轉化為可執行的規格文件
⦿ 了解遊戲產業趨勢，對撲克類遊戲有深入研究（大廳、俱樂部、桌檯功能架構）
```

### SKILLS 範例
```
專案管理工具：Jira、Confluence
應用撰寫規劃書與產品規格文件（PRD）
執行專案與控管時程
跨部門溝通與協調
原型設計工具：Mockflowe、Axure
使用者流程設計（Wireframe）
辦公室應用：Excel、Outlook、PowerPoint、Word
ChatGPT、Google Workspace
```

### MATCH_ANALYSIS 範例
```
✅ Product Manager 經驗（目前職位）
✅ 遊戲產業經驗（撲克 APP）
✅ 撰寫 PRD（產品規格文件）
✅ 跨部門協作能力
✅ 10+ 年工作經驗
```

---

## 使用指南（給 AI Bot）

### 步驟 1：讀取候選人資料
```python
candidate = get_candidate_data(candidate_id)
```

### 步驟 2：套用範本
```python
template = read_file('templates/anonymous-resume-template.md')
```

### 步驟 3：匿名化處理
```python
# 生成候選人代號
candidate_code = generate_candidate_code(candidate)  # 例：Abeni 或 PM-2026-001

# 匿名化公司名稱
work_experience = anonymize_companies(candidate.work_experience)
# 例：遊戲橘子 → 某遊戲科技公司（網路服務業，30-100人）
```

### 步驟 4：變數替換
```python
resume = template.replace('{{CANDIDATE_CODE}}', candidate_code)
resume = resume.replace('{{BIRTH_YEAR}}', candidate.birth_year)
resume = resume.replace('{{AGE}}', calculate_age(candidate.birth_year))
# ... 替換所有變數
```

### 步驟 5：生成 PDF
```python
pdf = generate_pdf(resume)
return pdf
```

---

## 匿名化函數範例（Python）

```python
def anonymize_company_name(company_name, industry, size):
    """
    匿名化公司名稱
    
    Args:
        company_name: 原始公司名稱（如：遊戲橘子）
        industry: 產業類型（如：網路服務業）
        size: 公司規模（如：30-100人）
    
    Returns:
        匿名化後的公司描述
    """
    # 產業關鍵字對照表
    industry_map = {
        '遊戲': '某遊戲科技公司',
        '電商': '某知名電商平台',
        '金融': '某金融科技公司',
        '製造': '某製造業集團',
        '軟體': '某網路服務公司',
        '外商': '某外商科技公司'
    }
    
    # 根據公司名稱或產業判斷
    for keyword, anonymous_name in industry_map.items():
        if keyword in company_name or keyword in industry:
            return f"{anonymous_name}（{industry}，{size}）"
    
    # 預設
    return f"某科技公司（{industry}，{size}）"

# 使用範例
result = anonymize_company_name('遊戲橘子', '網路服務業', '30-100人')
# 輸出：某遊戲科技公司（網路服務業，30-100人）
```

---

## 品質檢查清單（生成前必檢查）

- [ ] 所有 `{{變數}}` 都已替換（無遺漏）
- [ ] 公司名稱已匿名化（無真實公司名）
- [ ] 候選人代號已生成（無真實姓名）
- [ ] 工作經歷格式一致（bullet points）
- [ ] 保密聲明存在（頁首）
- [ ] 推薦顧問簽名（頁尾）
- [ ] 推薦理由與匹配度分析已填寫
- [ ] 薪資資訊完整（Previous/Current/期待）
- [ ] 格式符合範本（分隔線、排版）

---

## 版本歷史

| 版本 | 日期 | 變更內容 |
|------|------|---------|
| 1.0 | 2026-02-23 | 初版建立（基於 Abeni 範例 PDF） |

---

**重要提醒**：此範本為 Step1ne 官方標準格式，所有 AI Bot（YQ1/YQ2/YQ3）生成的匿名履歷都必須遵循此範本，確保品牌一致性和專業度。
