# Step1ne 獵頭系統 - 人才評級規則文檔

**最後更新**：2026-02-23  
**版本**：v1.0

---

## 📊 一、工作穩定性評分（Stability Score）

### 基本計算公式

```javascript
穩定度 = 基礎分 + 年資加分 - 離職次數扣分 + 最後離職間隔加分

基礎分：40 分
年資加分：總年資 × 2
離職次數扣分：離職次數 × 3
最後離職間隔加分：間隔月數 × 0.5
```

---

### 特殊案例處理

#### 案例 1：社會新鮮人（年資 < 1 年）

**判斷條件**：`candidate.years < 1`

**處理方式**：
- 給予預設分數：**70 分（B級）**
- 理由：沒有負面記錄，給予信任基礎分

**範例**：
```
姓名：李小華
年資：0.5 年（剛畢業）
離職次數：0
穩定度：70 分（B級）✅
```

---

#### 案例 2：只有一份工作且仍在職（離職次數 = 0）

**判斷條件**：`candidate.jobChanges === 0`

**處理方式**：
- 公式：`40 + (年資 × 3)`（年資加權提高）
- 上限：95 分
- 理由：從未離職是最穩定的表現

**範例**：
```
姓名：王大明
年資：5 年
離職次數：0（仍在第一份工作）
穩定度：40 + (5 × 3) = 55 分 → 升級為 70 分（B級）✅
```

**改進公式**（更合理）：
```javascript
if (jobChanges === 0) {
  score = Math.min(70 + (years * 5), 95);
  // 3年：85分 (A級)
  // 5年：95分 (A級)
}
```

---

#### 案例 3：一般候選人（有離職記錄）

**判斷條件**：`candidate.jobChanges > 0`

**處理方式**：
- 使用標準公式
- 範圍：20-100 分

**範例**：
```
姓名：陳宥樺
年資：9.7 年
離職次數：5
最後離職間隔：1 個月
穩定度：40 + 19.4 - 15 + 0.5 = 44.9 分（C級）✅
```

---

### 完整計算邏輯（JavaScript）

```javascript
function calculateStabilityScore(candidate) {
  const { years, jobChanges, lastGap } = candidate;
  
  // 特殊案例 1：社會新鮮人
  if (years < 1) {
    return {
      score: 70,
      grade: 'B',
      reason: '社會新鮮人（預設評分）'
    };
  }
  
  // 特殊案例 2：只有一份工作
  if (jobChanges === 0) {
    const score = Math.min(70 + (years * 5), 95);
    return {
      score: Math.round(score),
      grade: getGrade(score),
      reason: '從未離職（高穩定度）'
    };
  }
  
  // 一般計算
  let score = 40;
  score += years * 2;
  score -= jobChanges * 3;
  score += (lastGap || 0) * 0.5;
  
  // 限制範圍 20-100
  score = Math.max(20, Math.min(score, 100));
  
  return {
    score: Math.round(score),
    grade: getGrade(score),
    reason: '標準計算'
  };
}

function getGrade(score) {
  if (score >= 80) return 'A';
  if (score >= 60) return 'B';
  if (score >= 40) return 'C';
  if (score >= 20) return 'D';
  return 'F';
}
```

---

## 🎯 二、綜合評級（Talent Grade）

### 評分維度（6個，總分100）

**權重分配（方案A - 業界趨勢導向）**：

```javascript
const TALENT_GRADE_WEIGHTS = {
  skills: 25,        // 技能匹配度（業界最重視 - 能否快速上手）
  trajectory: 25,    // 職涯發展軌跡（成就與發展潛力）
  stability: 20,     // 工作穩定性（留任率）
  experience: 15,    // 工作年資（經驗基礎）
  education: 10,     // 學歷背景（門檻要求）
  bonus: 5          // 特殊加分（軟實力）
};
```

**設計原則**：
- ✅ 符合 2024-2025 業界招募趨勢
- ✅ 強調技能與職涯成就（企業最看重）
- ✅ 保留彈性（不同職缺可調整權重）

---

#### 1. 學歷背景（10%）

| 學歷 | 得分 |
|------|------|
| 博士 | 10 |
| 碩士 | 9 |
| 學士 | 7.5 |
| 專科 | 6 |
| 高中/其他 | 5 |

**判斷邏輯**：
```javascript
function getEducationScore(education) {
  const text = education.toLowerCase();
  if (text.includes('博士') || text.includes('phd') || text.includes('doctor')) return 10;
  if (text.includes('碩士') || text.includes('master')) return 9;
  if (text.includes('學士') || text.includes('bachelor')) return 7.5;
  if (text.includes('專科') || text.includes('college')) return 6;
  return 5; // 高中或其他
}
```

---

#### 2. 工作年資（15%）

| 年資 | 得分 |
|------|------|
| 10年+ | 15 |
| 7-10年 | 12.5 |
| 5-7年 | 11 |
| 3-5年 | 9 |
| 1-3年 | 6 |
| <1年 | 3.5 |

**計算邏輯**：
```javascript
function getExperienceScore(years) {
  if (years >= 10) return 15;
  if (years >= 7) return 12.5;
  if (years >= 5) return 11;
  if (years >= 3) return 9;
  if (years >= 1) return 6;
  return 3.5;
}
```

---

#### 3. 技能匹配度（25%）

**評分邏輯**：

```javascript
function getSkillScore(skills) {
  if (!skills) return 5;
  
  // 分隔符號：逗號、頓號、|、空格等
  const skillList = skills.split(/[,，、|\s]+/).filter(s => s.length > 0);
  const count = skillList.length;
  
  // 基礎分：技能數量 (每個 1.5 分)
  let score = Math.min(count * 1.5, 15);
  
  // 加分項：深度技能關鍵字
  const advancedKeywords = [
    'architect', '架構', 'lead', 'senior', '資深',
    'expert', '專家', 'advanced', '進階'
  ];
  const hasAdvancedSkills = advancedKeywords.some(kw => 
    skills.toLowerCase().includes(kw)
  );
  if (hasAdvancedSkills) score += 5;
  
  // 加分項：認證/證照
  const certKeywords = ['aws', 'gcp', 'azure', 'pmp', 'cissp', '證照', 'certified'];
  const hasCertification = certKeywords.some(kw => 
    skills.toLowerCase().includes(kw)
  );
  if (hasCertification) score += 5;
  
  // 上限 25 分
  return Math.min(score, 25);
}
```

**範例**：
- `"Python, Java, React"` → 3個技能 → 4.5分
- `"Python, Java, React, AWS, Docker, Kubernetes"` → 6個技能 → 9分
- `"Senior Architect, Python, AWS Certified, Kubernetes, Docker, CI/CD"` → 6個 + 資深 + 認證 → 19分

---

#### 4. 工作穩定性（20%）

直接使用「工作穩定性評分」：
```javascript
function getStabilityComponentScore(stabilityScore) {
  // 穩定度 0-100 分 → 轉換為 0-20 分
  return (stabilityScore / 100) * 20;
}
```

**範例**：
- 穩定度 70 分 → 14 分
- 穩定度 44 分 → 8.8 分
- 穩定度 95 分 → 19 分

---

#### 5. 職涯發展軌跡（25%）

**需要判斷職位晉升/平級/降級**

##### A. 職位層級定義表

```javascript
const JOB_LEVELS = {
  // 高階管理（9-10）
  'CEO': 10, 'CTO': 10, 'CFO': 10, 'COO': 10,
  '執行長': 10, '技術長': 10, '財務長': 10, '營運長': 10,
  
  '總經理': 9, 'VP': 9, '副總': 9, 'Vice President': 9,
  'General Manager': 9,
  
  // 中階管理（7-8）
  '協理': 8, '總監': 8, 'Director': 8,
  '經理': 7, 'Manager': 7, '部門主管': 7, 'Department Head': 7,
  
  // 基層管理（5-6）
  '副理': 6, '組長': 6, 'Team Lead': 6, 'Lead': 6,
  '主管': 6, 'Supervisor': 6,
  '資深專員': 6, 'Senior Specialist': 6,  // ✅ 新增
  
  // 資深技術職（6-8）
  'Principal Engineer': 8, '首席工程師': 8, 'Chief Engineer': 8,
  'Staff Engineer': 7, 'Architect': 7, '架構師': 7,
  '資深工程師': 6, 'Senior Engineer': 6, 'Senior Developer': 6,
  'Senior': 6,
  
  // 一般技術職（4-5）
  '工程師': 5, 'Engineer': 5, '開發': 5, 'Developer': 5,
  '專員': 5, 'Specialist': 5, 'Analyst': 5, '分析師': 5,
  
  // 初階職位（2-4）
  '初級工程師': 4, 'Junior Engineer': 4, 'Junior Developer': 4,
  'Junior': 4,
  '助理': 3, 'Assistant': 3, '助理專員': 3,
  '實習生': 2, 'Intern': 2, '工讀生': 2,
  
  // 預設
  '未知': 5
};

function getJobLevel(title) {
  if (!title) return 5;
  
  const titleLower = title.toLowerCase().trim();
  
  // 1. 精確匹配（不區分大小寫）
  for (const [keyword, level] of Object.entries(JOB_LEVELS)) {
    if (titleLower === keyword.toLowerCase()) {
      return level;
    }
  }
  
  // 2. 模糊匹配（包含關鍵字，優先匹配長關鍵字）
  // 按關鍵字長度排序，避免誤判
  const sortedLevels = Object.entries(JOB_LEVELS)
    .sort((a, b) => b[0].length - a[0].length);
  
  for (const [keyword, level] of sortedLevels) {
    if (titleLower.includes(keyword.toLowerCase())) {
      return level;
    }
  }
  
  // 3. AI 輔助判斷（保留，未來可接入 LLM）
  // 處理企業自訂職稱，例如：
  // "技術副總" → 應判斷為 9 級（VP）
  // "資料科學家" → 應判斷為 5 級（專員）
  // "團隊負責人" → 應判斷為 6 級（Team Lead）
  
  return 5; // 預設中等
}

/**
 * AI 增強版職位層級判斷（企業職稱差異處理）
 * 
 * 使用情境：當職稱表無法匹配時，使用 AI 推斷
 */
async function getJobLevelWithAI(title, company = '') {
  // 先嘗試標準匹配
  const standardLevel = getJobLevel(title);
  if (standardLevel !== 5 || !title) {
    return standardLevel;
  }
  
  // 如果標準匹配失敗，使用 AI 推斷
  const prompt = `
你是人資專家。請根據職位名稱判斷職位層級（1-10級）。

職位：${title}
${company ? `公司：${company}` : ''}

參考標準：
- 10級：CEO、CTO、執行長
- 9級：總經理、VP、副總
- 8級：協理、總監
- 7級：經理、Manager
- 6級：資深專員、Team Lead、資深工程師
- 5級：專員、工程師（預設）
- 4級：初級工程師、Junior
- 3級：助理
- 2級：實習生

只回傳數字，不要其他文字。
`;
  
  // 這裡可以接入 Claude/GPT API
  // const level = await callLLM(prompt);
  // return parseInt(level);
  
  return 5; // 降級方案：返回預設值
}
```

##### B. 職涯軌跡分析

```javascript
function analyzeCareerTrajectory(workHistory) {
  if (!workHistory || workHistory.length < 2) {
    return { score: 12.5, type: 'insufficient_data' }; // 預設給一半分數
  }
  
  // 按時間排序（最新 → 最舊）
  const sorted = [...workHistory].sort((a, b) => 
    new Date(b.start) - new Date(a.start)
  );
  
  let score = 0;
  let promotions = 0;
  let lateral = 0;
  let demotions = 0;
  
  for (let i = 0; i < sorted.length - 1; i++) {
    const current = sorted[i];      // 較新的工作
    const previous = sorted[i + 1]; // 較舊的工作
    
    const currentLevel = getJobLevel(current.title);
    const previousLevel = getJobLevel(previous.title);
    
    const diff = currentLevel - previousLevel;
    
    if (diff >= 3) {
      // 跨級晉升（3+ 級，例：工程師 → 總監）
      promotions++;
      score += 25;
    } else if (diff === 2) {
      // 明顯晉升（跨 2 級）
      promotions++;
      score += 20;
    } else if (diff === 1) {
      // 小幅晉升
      promotions++;
      score += 15;
    } else if (diff === 0) {
      // 平級轉換（可能換跑道或公司）
      lateral++;
      score += 10;
    } else if (diff === -1) {
      // 小幅降級（可能策略性選擇）
      demotions++;
      score += 5;
    } else {
      // 明顯降級（-2 級以上）
      demotions++;
      score += 0;
    }
  }
  
  // 加權處理：晉升次數越多，加分越高
  if (promotions >= 3) score += 5;  // 持續晉升獎勵
  if (demotions === 0) score += 3;  // 無降級獎勵
  
  // 限制在 0-25 分
  score = Math.max(0, Math.min(score, 25));
  
  return {
    score,
    promotions,
    lateral,
    demotions,
    type: promotions >= 2 ? 'fast_growing' :
          promotions > lateral ? 'growing' : 
          demotions > 0 ? 'mixed' : 'stable'
  };
}
```

**範例**：
```
工作經歷：
1. 資深工程師（6級）2023-2026
2. 工程師（5級）2020-2023
3. 初級工程師（4級）2018-2020

分析：
- 2020: 4→5 晉升 +15分
- 2023: 5→6 晉升 +15分
- 無降級獎勵 +3分
- 總分：25分（上限，fast_growing）✅
```

```
工作經歷：
1. 總監（8級）2022-2026
2. 專員（5級）2018-2022

分析：
- 2022: 5→8 跨級晉升（3級）+25分
- 總分：25分（上限，fast_growing）✅
```

---

#### 6. 特殊加分（5%）

**軟實力加分項**：

```javascript
function getSpecialBonusScore(candidate) {
  let score = 0;
  const skills = (candidate.skills || '').toLowerCase();
  const notes = (candidate.notes || '').toLowerCase();
  const combined = skills + ' ' + notes;
  
  // 語言能力（+2分）
  const languageKeywords = [
    '英文', 'english', '雙語', 'bilingual', 'trilingual',
    'toeic', 'ielts', 'toefl', 'celpip'
  ];
  if (languageKeywords.some(kw => combined.includes(kw))) {
    score += 2;
  }
  
  // 軟實力關鍵字（+2分）
  const softSkillKeywords = [
    '溝通', 'communication', '領導', 'leadership',
    '團隊合作', 'teamwork', '問題解決', 'problem solving',
    '批判性思維', 'critical thinking', '適應力', 'adaptability'
  ];
  if (softSkillKeywords.some(kw => combined.includes(kw))) {
    score += 2;
  }
  
  // 特殊成就（+1分）
  const achievementKeywords = [
    '獲獎', 'award', '專利', 'patent', '出版', 'publication',
    '演講', 'speaker', 'conference'
  ];
  if (achievementKeywords.some(kw => combined.includes(kw))) {
    score += 1;
  }
  
  return Math.min(score, 5);
}
```

**範例**：
- 雙語 + 團隊領導經驗 + 專利 = 5分 ✅
- 英文流利 = 2分
- 溝通能力強 = 2分
- 無特殊加分項 = 0分

---

### 綜合評級計算（完整）

```javascript
function calculateTalentGrade(candidate) {
  const scores = {
    education: getEducationScore(candidate.education),          // 10%
    experience: getExperienceScore(candidate.years),           // 15%
    skills: getSkillScore(candidate.skills),                   // 25%
    stability: getStabilityComponentScore(candidate.stabilityScore), // 20%
    trajectory: analyzeCareerTrajectory(candidate.workHistory).score, // 25%
    bonus: getSpecialBonusScore(candidate)                     // 5%
  };
  
  const total = Object.values(scores).reduce((a, b) => a + b, 0);
  
  return {
    total: Math.round(total * 10) / 10,  // 保留一位小數
    grade: getTalentGrade(total),
    breakdown: scores,
    weights: {
      education: '10%',
      experience: '15%',
      skills: '25%',
      stability: '20%',
      trajectory: '25%',
      bonus: '5%'
    }
  };
}

function getTalentGrade(score) {
  if (score >= 90) return 'S';   // 頂尖人才（稀缺）（90-100分）
  if (score >= 80) return 'A+';  // 優秀人才（強力推薦）（80-89分）
  if (score >= 70) return 'A';   // 合格人才（可推薦）（70-79分）
  if (score >= 60) return 'B';   // 基本合格（需評估）（60-69分）
  return 'C';                     // 需補強（謹慎推薦）（<60分）
}
```

---

### 完整範例驗證

#### 案例 1：資深技術人才（王大明）

**候選人資料**：
```
姓名：王大明
學歷：碩士（計算機科學）
年資：8 年
離職次數：1 次（穩定度 78 分）
技能：Python, TensorFlow, PyTorch, AWS Certified, Docker, Kubernetes, CI/CD
工作經歷：
  1. 資深 AI 工程師（6級）2021-2026
  2. AI 工程師（5級）2018-2021
  3. 初級工程師（4級）2016-2018
備註：雙語能力、技術演講者
```

**評分計算**：
```
學歷（碩士）：         9分   (10%)
年資（8年）：          12.5分 (15%)
技能（7個+認證）：      19分   (25%)
穩定度（78分）：       15.6分 (20%)
職涯軌跡（2次晉升）：   25分   (25%)
特殊加分（雙語+演講）：  3分   (5%)
───────────────────────────
總分：84.1 分 → A+ 級（優秀人才）✅
```

---

#### 案例 2：社會新鮮人（李小華）

**候選人資料**：
```
姓名：李小華
學歷：學士（資訊管理）
年資：0.5 年（剛畢業）
離職次數：0 次（穩定度 70 分，預設）
技能：JavaScript, React, HTML, CSS
工作經歷：
  1. 前端工程師（5級）2025-2026（第一份工作）
備註：無
```

**評分計算**：
```
學歷（學士）：         7.5分  (10%)
年資（<1年）：         3.5分  (15%)
技能（4個基礎）：       6分    (25%)
穩定度（70分預設）：   14分   (20%)
職涯軌跡（無法評估）：  12.5分 (25%, 預設一半)
特殊加分（無）：       0分    (5%)
───────────────────────────
總分：43.5 分 → C 級（需培訓）
```

**評價**：合理，社會新鮮人確實需要培訓。

---

#### 案例 3：高階管理人才（陳總監）

**候選人資料**：
```
姓名：陳總監
學歷：博士（企業管理）
年資：15 年
離職次數：2 次（穩定度 88 分）
技能：策略規劃, 團隊管理, P&L, 數位轉型, AI Strategy, Leadership, 雙語
工作經歷：
  1. 總監（8級）2020-2026
  2. 資深經理（7級）2015-2020
  3. 經理（7級）2010-2015
  4. 專員（5級）2008-2010
備註：PMP 認證、國際演講者、獲獎
```

**評分計算**：
```
學歷（博士）：         10分   (10%)
年資（15年）：         15分   (15%)
技能（7個+管理）：      21分   (25%)
穩定度（88分）：       17.6分 (20%)
職涯軌跡（專員→總監）： 25分   (25%)
特殊加分（全滿）：      5分    (5%)
───────────────────────────
總分：93.6 分 → S 級（頂尖人才）✅
```

**評價**：完美！高階人才應得高分。

---

## 🤖 三、AI 判斷指引

### 如何讓 AI 正確判斷工作經歷？

#### 提供給 AI 的 Prompt 範本

```
你是一位專業的人資分析師。請根據以下工作經歷分析候選人的職涯發展軌跡：

【候選人資料】
姓名：{name}
工作經歷（按時間順序，最新在前）：
{workHistory.map(job => `
- ${job.title} @ ${job.company} (${job.start} - ${job.end}, ${job.duration_months}個月)
`).join('\n')}

【分析任務】
1. 判斷每次工作轉換是「晉升」、「平級」還是「降級」
2. 使用職位層級表進行判斷
3. 輸出 JSON 格式：
{
  "trajectory_type": "growing | stable | mixed | declining",
  "promotions": 2,
  "lateral_moves": 1,
  "demotions": 0,
  "score": 10,
  "explanation": "候選人從初級工程師晉升至資深工程師，展現持續成長。"
}

【職位層級參考】
- CEO/CTO/總經理：10級
- VP/副總/協理：8-9級
- 總監/經理：7-8級
- 資深工程師/Lead：6級
- 工程師/專員：5級
- 初級工程師：4級
- 助理：3級
```

---

## 📝 四、實作檢查清單

### Google Sheets 修改
- [ ] 新增 U 欄：綜合評級 (S/A+/A/B/C)
- [ ] 新增 V 欄：綜合評級分數 (0-100)
- [ ] 新增 W 欄：工作穩定性原因（選填）

### 後端 API
- [ ] 實作 `calculateStabilityScore()` 函數
- [ ] 實作 `calculateTalentGrade()` 函數
- [ ] POST /api/candidates 支援自動計算評級
- [ ] GET /api/candidates 返回評級欄位

### 前端顯示
- [ ] 候選人總表新增「綜合評級」欄位
- [ ] 工作穩定性改名（穩定度 → 工作穩定性）
- [ ] 加上欄位說明提示（ⓘ 圖示）

---

**文檔版本記錄**：
- v1.0 (2026-02-23): 初版，定義完整評級規則
