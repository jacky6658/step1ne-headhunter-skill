# OpenClaw AI 連接 Step1ne 獵頭系統 - 完整指南

**最後更新**: 2026-02-23  
**適用對象**: 內部 AI 助理（YuQi、Phoebe AI 等）  
**系統版本**: Step1ne v1.0.0

---

## 📋 目錄
1. [系統架構](#系統架構)
2. [環境設定](#環境設定)
3. [API 端點說明](#api-端點說明)
4. [OpenClaw 使用範例](#openclaw-使用範例)
5. [常見任務](#常見任務)
6. [人才評級系統](#人才評級系統)
7. [故障排除](#故障排除)

---

## 系統架構

### 核心元件

```
┌─────────────────────────────────────────────────────────┐
│                    OpenClaw AI 助理                      │
│  (YuQi / Phoebe / 其他 AI)                              │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ↓ HTTP API
┌─────────────────────────────────────────────────────────┐
│           Step1ne Headhunter System                      │
│  ┌─────────────┬──────────────┬───────────────────┐    │
│  │   Frontend  │   Backend    │  Grading Service  │    │
│  │   (React)   │  (Node.js)   │    (Python)       │    │
│  └─────────────┴──────────────┴───────────────────┘    │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ↓ Google Sheets API
┌─────────────────────────────────────────────────────────┐
│              Google Sheets 履歷池 v2                     │
│  Sheet ID: 1PunpaDAFBPBL_I76AiRYGXKaXDZvMl1c262SEtxRk6Q │
│  Tab: 履歷池v2 (GID: 142613837)                         │
│  Columns: A-U (21 columns, 250+ rows)                   │
└─────────────────────────────────────────────────────────┘
```

### 倉庫關係

| 倉庫 | 用途 | GitHub URL |
|------|------|------------|
| **step1ne-headhunter-system** | 前後端 UI 系統 | https://github.com/jacky6658/step1ne-headhunter-system |
| **step1ne-headhunter-skill** | AI 模組 + 訓練文檔 | https://github.com/jacky6658/step1ne-headhunter-skill |

---

## 環境設定

### 1. 系統 URL

**生產環境**：
```bash
FRONTEND_URL="https://step1ne.zeabur.app"
BACKEND_URL="https://backendstep1ne.zeabur.app"
```

**本地開發**：
```bash
FRONTEND_URL="http://localhost:3000"
BACKEND_URL="http://localhost:3001"
```

### 2. 認證資訊

**Google Sheets 帳號**：
- Email: `aijessie88@step1ne.com`
- 用途: 讀寫履歷池v2

**用戶角色**：
| 用戶 | Role | 權限 |
|------|------|------|
| Admin | ADMIN | 所有權限 |
| Jacky | REVIEWER | 查看/編輯候選人 |
| Phoebe | REVIEWER | 查看/編輯候選人 |

### 3. OpenClaw 工具配置

確保 OpenClaw 有以下工具：
```bash
# 檢查工具
openclaw tools list

# 必要工具
- exec   # 執行腳本
- web_fetch  # 呼叫 API
```

---

## API 端點說明

### Base URL
```
https://backendstep1ne.zeabur.app/api
```

### 候選人管理 API

#### 1. 取得所有候選人
```http
GET /api/candidates
```

**回應範例**：
```json
{
  "success": true,
  "data": [
    {
      "id": "1",
      "name": "張大明",
      "position": "前端工程師",
      "yearsOfExperience": "5.5年 / 3次",
      "stability": "68",
      "stabilityGrade": "B",
      "skills": "React、TypeScript、Node.js、AWS",
      "currentStatus": "待聯繫",
      "source": "GitHub",
      "consultant": "Jacky",
      "_sheetRow": 228
    }
  ],
  "count": 250
}
```

#### 2. 取得單一候選人
```http
GET /api/candidates/:id
```

#### 3. 新增候選人
```http
POST /api/candidates
Content-Type: application/json

{
  "name": "陳小華",
  "email": "chen@example.com",
  "phone": "0912345678",
  "position": "後端工程師",
  "skills": "Python、Django、PostgreSQL",
  "source": "LinkedIn",
  "consultant": "Jacky"
}
```

#### 4. 更新候選人狀態
```http
PUT /api/candidates/:id
Content-Type: application/json

{
  "currentStatus": "面試中"
}
```

#### 5. 刪除候選人
```http
DELETE /api/candidates/:id
```

#### 6. 批量更新狀態
```http
POST /api/candidates/batch-update-status
Content-Type: application/json

{
  "ids": ["1", "2", "3"],
  "status": "已聯繫"
}
```

### 用戶管理 API

#### 取得用戶列表
```http
GET /api/users
```

**回應範例**：
```json
{
  "success": true,
  "data": [
    {
      "id": "1",
      "username": "admin",
      "name": "Admin",
      "email": "admin@step1ne.com",
      "role": "ADMIN",
      "consultant": "Admin"
    }
  ],
  "count": 3
}
```

---

## OpenClaw 使用範例

### 範例 1: 查詢所有候選人

```javascript
// 使用 web_fetch 工具
const result = await web_fetch({
  url: "https://backendstep1ne.zeabur.app/api/candidates",
  extractMode: "text"
});

const data = JSON.parse(result);
console.log(`共 ${data.count} 位候選人`);
```

**OpenClaw 執行**：
```bash
# 方式 1: 使用 exec + curl
openclaw exec "curl https://backendstep1ne.zeabur.app/api/candidates"

# 方式 2: 使用 web_fetch（推薦）
# 在對話中直接請求：「查詢 step1ne 所有候選人」
```

### 範例 2: 搜尋特定技能的候選人

```bash
#!/bin/bash
# search-candidates-by-skill.sh

SKILL="Python"
BACKEND_URL="https://backendstep1ne.zeabur.app"

# 取得所有候選人
candidates=$(curl -s "${BACKEND_URL}/api/candidates")

# 使用 jq 篩選
echo "$candidates" | jq -r ".data[] | select(.skills | contains(\"$SKILL\")) | .name"
```

**OpenClaw 執行**：
```bash
openclaw exec "bash /path/to/search-candidates-by-skill.sh"
```

### 範例 3: 新增候選人

```bash
#!/bin/bash
# add-candidate.sh

BACKEND_URL="https://backendstep1ne.zeabur.app"

curl -X POST "${BACKEND_URL}/api/candidates" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "李小明",
    "email": "lee@example.com",
    "phone": "0987654321",
    "position": "DevOps 工程師",
    "yearsOfExperience": "3.5年 / 2次",
    "stability": "75",
    "stabilityGrade": "A",
    "skills": "Kubernetes、Docker、AWS、Terraform",
    "currentStatus": "待聯繫",
    "source": "GitHub",
    "consultant": "Jacky"
  }'
```

### 範例 4: 批量更新候選人狀態

```bash
#!/bin/bash
# batch-update-status.sh

BACKEND_URL="https://backendstep1ne.zeabur.app"

curl -X POST "${BACKEND_URL}/api/candidates/batch-update-status" \
  -H "Content-Type: application/json" \
  -d '{
    "ids": ["1", "2", "3"],
    "status": "已聯繫"
  }'
```

---

## 常見任務

### 任務 1: 每日候選人報告

**目標**: 生成每日候選人統計報告

```bash
#!/bin/bash
# daily-candidate-report.sh

BACKEND_URL="https://backendstep1ne.zeabur.app"

# 取得所有候選人
candidates=$(curl -s "${BACKEND_URL}/api/candidates")

# 統計各狀態候選人數量
echo "=== 每日候選人報告 ==="
echo "總數: $(echo "$candidates" | jq '.count')"
echo ""
echo "各狀態統計:"
echo "$candidates" | jq -r '.data | group_by(.currentStatus) | .[] | "\(.[0].currentStatus): \(length)位"'
echo ""
echo "各顧問統計:"
echo "$candidates" | jq -r '.data | group_by(.consultant) | .[] | "\(.[0].consultant): \(length)位"'
```

**OpenClaw Cron 設定**：
```bash
openclaw cron add \
  --label "每日候選人報告" \
  --schedule "0 9 * * *" \
  --command "bash /path/to/daily-candidate-report.sh"
```

### 任務 2: 找出待聯繫的候選人

```bash
#!/bin/bash
# find-pending-candidates.sh

BACKEND_URL="https://backendstep1ne.zeabur.app"

curl -s "${BACKEND_URL}/api/candidates" | \
  jq -r '.data[] | select(.currentStatus == "待聯繫") | 
    "[\(.id)] \(.name) - \(.position) (\(.skills))"'
```

### 任務 3: 推薦候選人給職缺

```python
#!/usr/bin/env python3
# recommend-candidates.py

import requests
import json

BACKEND_URL = "https://backendstep1ne.zeabur.app"

def recommend_candidates(required_skills, min_years=3):
    """推薦符合職缺需求的候選人"""
    
    # 取得所有候選人
    response = requests.get(f"{BACKEND_URL}/api/candidates")
    candidates = response.json()['data']
    
    # 篩選符合條件的候選人
    matches = []
    for candidate in candidates:
        # 解析年資
        years = float(candidate['yearsOfExperience'].split('年')[0])
        
        # 檢查技能匹配
        candidate_skills = candidate['skills'].split('、')
        matched_skills = [s for s in required_skills if s in candidate_skills]
        
        # 符合條件：年資足夠 + 至少匹配 2 個技能
        if years >= min_years and len(matched_skills) >= 2:
            matches.append({
                'name': candidate['name'],
                'position': candidate['position'],
                'years': years,
                'matched_skills': matched_skills,
                'score': len(matched_skills) * 10 + years * 2
            })
    
    # 按分數排序
    matches.sort(key=lambda x: x['score'], reverse=True)
    
    return matches[:5]  # 返回 Top 5

# 使用範例
if __name__ == "__main__":
    job_skills = ["Python", "Django", "PostgreSQL", "AWS"]
    recommendations = recommend_candidates(job_skills, min_years=3)
    
    print("=== 推薦候選人 ===")
    for i, candidate in enumerate(recommendations, 1):
        print(f"{i}. {candidate['name']} ({candidate['position']})")
        print(f"   年資: {candidate['years']}年")
        print(f"   匹配技能: {', '.join(candidate['matched_skills'])}")
        print(f"   評分: {candidate['score']}")
        print()
```

---

## 人才評級系統

### 評級架構

Step1ne 使用 **6 維度綜合評級系統**（總分 100）：

| 維度 | 權重 | 說明 |
|------|------|------|
| 學歷背景 | 20% | 博士/碩士/學士/專科 |
| 工作年資 | 20% | 10年+/7-9年/4-6年/1-3年/<1年 |
| 技能廣度 | 20% | 10+/7-9/4-6/1-3 個技能 |
| 工作穩定性 | 20% | 穩定度評分 80+/70-79/60-69/50-59/<50 |
| 職涯發展 | 10% | 晉升/平行/停滯/向下 |
| 特殊加分 | 10% | 名校/大廠/專家/開源/語言 |

### 評級對應

| 總分 | 評級 | 說明 |
|------|------|------|
| 90-100 | S | 頂尖人才（稀缺）|
| 80-89 | A+ | 優秀人才（強力推薦）|
| 70-79 | A | 合格人才（可推薦）|
| 60-69 | B | 基本合格（需評估）|
| <60 | C | 需補強（謹慎推薦）|

### 使用評級系統

**方式 1: 使用 Python 模組**

```python
#!/usr/bin/env python3
# grade-candidate.py

import sys
import json
sys.path.append('/path/to/step1ne-headhunter-skill/modules/talent-grading')

from grading_logic import grade_candidate

# 候選人資料
candidate = {
    "name": "張大明",
    "educationJson": '[{"degree":"碩士","school":"台大"}]',
    "workHistoryJson": '[...]',
    "skills": "Python、Java、AWS、Kubernetes",
    "stability": 72,
    "yearsOfExperience": 7.5
}

# 評分
result = grade_candidate(candidate)

print(f"評級: {result['grade']}")
print(f"總分: {result['totalScore']}")
print(f"細節: {json.dumps(result['breakdown'], indent=2)}")
```

**方式 2: 使用 CLI**

```bash
#!/bin/bash

cd /path/to/step1ne-headhunter-skill/modules/talent-grading

# 準備候選人 JSON
cat > temp_candidate.json << EOF
{
  "name": "張大明",
  "educationJson": "[{\"degree\":\"碩士\",\"school\":\"台大\"}]",
  "skills": "Python、Java、AWS、Kubernetes",
  "stability": 72,
  "yearsOfExperience": 7.5
}
EOF

# 執行評分
python3 grading-logic.py \
  --resume temp_candidate.json \
  --output result.json

# 顯示結果
cat result.json
```

**OpenClaw 整合**：

```bash
# 在 OpenClaw 中執行
openclaw exec "cd /path/to/step1ne-headhunter-skill/modules/talent-grading && python3 grading-logic.py --resume candidate.json --output result.json && cat result.json"
```

---

## 故障排除

### 問題 1: API 連接失敗

**症狀**：
```
Error: connect ECONNREFUSED
```

**解決方案**：
1. 檢查 Backend 服務是否運行
```bash
curl https://backendstep1ne.zeabur.app/api/health
```

2. 檢查網路連接
```bash
ping backendstep1ne.zeabur.app
```

3. 使用本地開發環境
```bash
cd /path/to/step1ne-headhunter-system
./start-local.sh
```

### 問題 2: Google Sheets 讀取失敗

**症狀**：
```
Error: Unable to read sheet
```

**解決方案**：
1. 檢查 OAuth 認證
```bash
gog auth list
```

2. 重新認證
```bash
gog auth add aijessie88@step1ne.com
```

3. 檢查 Sheet ID 正確
```bash
SHEET_ID="1PunpaDAFBPBL_I76AiRYGXKaXDZvMl1c262SEtxRk6Q"
```

### 問題 3: 候選人資料格式錯誤

**症狀**：
```
Error: Invalid candidate data format
```

**解決方案**：
1. 檢查必填欄位
```json
{
  "name": "必填",
  "position": "必填",
  "skills": "必填",
  "currentStatus": "必填（預設: 待聯繫）",
  "source": "必填（預設: 手動輸入）",
  "consultant": "必填（預設: Jacky）"
}
```

2. 驗證 JSON 格式
```bash
echo '{"name":"test"}' | jq .
```

### 問題 4: Zeabur 部署問題

**症狀**：
```
Build failed / Service unavailable
```

**解決方案**：
1. 檢查 Zeabur 部署狀態
   - 前往 https://zeabur.com
   - 查看 step1ne-headhunter-system 專案

2. 查看部署日誌
   - Backend logs
   - Frontend logs

3. 手動觸發重新部署
   - 推送新 commit 到 GitHub
   - Zeabur 自動重新部署

---

## 最佳實踐

### 1. API 呼叫頻率控制

```bash
# 避免過度呼叫 API，使用快取機制
CACHE_FILE="/tmp/candidates_cache.json"
CACHE_EXPIRY=1800  # 30 分鐘

if [ -f "$CACHE_FILE" ] && [ $(($(date +%s) - $(stat -f %m "$CACHE_FILE"))) -lt $CACHE_EXPIRY ]; then
    # 使用快取
    cat "$CACHE_FILE"
else
    # 呼叫 API 並更新快取
    curl -s "${BACKEND_URL}/api/candidates" > "$CACHE_FILE"
    cat "$CACHE_FILE"
fi
```

### 2. 錯誤處理

```python
import requests

def safe_api_call(url, method="GET", data=None, max_retries=3):
    """安全的 API 呼叫（含重試機制）"""
    for attempt in range(max_retries):
        try:
            if method == "GET":
                response = requests.get(url, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=10)
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                print(f"API 呼叫失敗（{max_retries} 次重試後）: {e}")
                return None
            else:
                print(f"重試中... ({attempt + 1}/{max_retries})")
                time.sleep(2 ** attempt)  # 指數退避
```

### 3. 資料驗證

```python
def validate_candidate_data(candidate):
    """驗證候選人資料完整性"""
    required_fields = ['name', 'position', 'skills', 'currentStatus', 'source', 'consultant']
    
    for field in required_fields:
        if field not in candidate or not candidate[field]:
            raise ValueError(f"缺少必填欄位: {field}")
    
    # 驗證狀態值
    valid_statuses = ['待聯繫', '已聯繫', '面試中', 'Offer', '已上職', '不合適', '封存']
    if candidate['currentStatus'] not in valid_statuses:
        raise ValueError(f"無效的狀態: {candidate['currentStatus']}")
    
    return True
```

---

## 相關資源

### 文檔
- [系統架構文檔](./ARCHITECTURE.md)
- [Bot 上傳履歷指南](./BOT-RESUME-UPLOAD-GUIDE.md)
- [API 整合文檔](./API-INTEGRATION.md)
- [人才評級系統](../modules/talent-grading/README.md)

### 訓練文檔
- [Phoebe AI 訓練指南](../training/PHOEBE-AI-GUIDE.md)
- [AI 模組使用手冊](../training/HEADHUNTER-AI-MODULES.md)

### GitHub 倉庫
- **系統**: https://github.com/jacky6658/step1ne-headhunter-system
- **技能**: https://github.com/jacky6658/step1ne-headhunter-skill

### 支援
- **內部聯繫**: Telegram @jackyyuqi (Jacky)
- **技術問題**: 在 GitHub Issues 提出

---

**最後更新**: 2026-02-23 20:08  
**版本**: v1.0.0  
**作者**: YuQi AI Assistant
