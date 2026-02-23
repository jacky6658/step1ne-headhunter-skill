# Step1ne 權限管理

**誰可以做什麼**

---

## 🔐 權限等級

### 1️⃣ **系統管理員**（修改程式碼）

**人員**:
- Jacky
- User (系統維護者)

**權限**:
- ✅ 修改程式碼
- ✅ 推送到 GitHub
- ✅ 部署到 Zeabur
- ✅ 變更系統設定
- ✅ 新增/刪除用戶
- ✅ 查看所有候選人
- ✅ 修改資料庫（Google Sheets）

**倉庫**:
- https://github.com/jacky6658/step1ne-headhunter-system
- https://github.com/jacky6658/step1ne-headhunter-skill

**工具**:
```bash
# 推送程式碼
cd ~/clawd/projects/step1ne-headhunter-system
git add -A
git commit -m "..."
git push origin main

# 部署到 Zeabur（自動）
# GitHub push 後 Zeabur 自動部署
```

---

### 2️⃣ **獵頭顧問**（使用系統）

**人員**:
- Jacky
- Phoebe
- Mike（未來）
- 其他顧問

**權限**:
- ✅ 訪問 Web UI（https://step1ne.zeabur.app）
- ✅ 查看自己負責的候選人
- ✅ 查看候選人詳情
- ✅ 查看評級結果
- ❌ 修改候選人狀態（需透過 Google Sheets）
- ❌ 修改程式碼
- ❌ 查看其他顧問的候選人

**帳號**:
| 用戶 | Username | 角色 | 查看範圍 |
|------|----------|------|---------|
| Admin | admin | ADMIN | 所有候選人 |
| Jacky | jacky | REVIEWER | Jacky 的候選人 |
| Phoebe | phoebe | REVIEWER | Phoebe 的候選人 |

**工具**:
- Web UI: https://step1ne.zeabur.app
- Google Sheets: https://docs.google.com/spreadsheets/d/1PunpaDAFBPBL_I76AiRYGXKaXDZvMl1c262SEtxRk6Q

---

### 3️⃣ **AI 助理**（API 訪問）

**AI**:
- @YuQi0923_bot (Jacky 的 AI)
- @HRyuqi_bot (Phoebe 的 AI)
- @MikeAI_bot (Mike 的 AI，未來)
- 其他新 AI

**權限**:
- ✅ 呼叫 Step1ne API
- ✅ 查詢主人負責的候選人
- ✅ 評級候選人
- ✅ 解析新履歷
- ✅ 私訊主人
- ❌ 修改程式碼
- ❌ 查看其他顧問的候選人
- ❌ 發送群組通知（改為私訊）

**API Endpoint**:
```
https://backendstep1ne.zeabur.app/api
```

**使用方式**:
閱讀 `AI-ONBOARDING.md` 和 `AI-CONFIG-TEMPLATE.md`

---

## 📋 權限對照表

| 操作 | 系統管理員 | 獵頭顧問 | AI 助理 |
|------|----------|---------|--------|
| 修改程式碼 | ✅ | ❌ | ❌ |
| 推送 GitHub | ✅ | ❌ | ❌ |
| 部署 Zeabur | ✅ | ❌ | ❌ |
| 新增用戶 | ✅ | ❌ | ❌ |
| 查看所有候選人 | ✅ | ❌ (只看自己的) | ❌ (只看主人的) |
| 查看候選人詳情 | ✅ | ✅ | ✅ |
| 評級候選人 | ✅ | ✅ | ✅ |
| 修改候選人狀態 | ✅ (Google Sheets) | ✅ (Google Sheets) | ❌ |
| 呼叫 API | ✅ | ✅ | ✅ |
| 解析履歷 | ✅ | ✅ | ✅ |
| 私訊主人 | ✅ | N/A | ✅ |
| 發送群組通知 | ✅ | N/A | ❌ (改為私訊) |

---

## 🔒 程式碼訪問控制

### GitHub 倉庫權限

**step1ne-headhunter-system** (前端 + 後端):
- Owner: jacky6658
- Collaborators: 
  - Jacky (Write 權限)
  - User (Maintain 權限)

**step1ne-headhunter-skill** (AI 模組):
- Owner: jacky6658
- Collaborators:
  - Jacky (Write 權限)
  - User (Maintain 權限)

**其他人**: ❌ 無訪問權限

### 新增 Collaborator（如果需要）

**步驟**:
1. GitHub → Repository → Settings → Collaborators
2. Add people → 輸入 GitHub username
3. 選擇權限等級：
   - **Write**: 可推送程式碼
   - **Read**: 只能查看
4. 對方接受邀請

**注意**: 目前只有 Jacky + User 可以修改程式碼。

---

## 📊 資料訪問控制

### Google Sheets（履歷池v2）

**Sheet ID**: `1PunpaDAFBPBL_I76AiRYGXKaXDZvMl1c262SEtxRk6Q`

**權限**:
| 用戶 | Email | 權限 |
|------|-------|------|
| Jacky | jacky@step1ne.com | Editor |
| Phoebe | phoebe@step1ne.com | Editor |
| API 服務帳號 | aijessie88@step1ne.com | Editor |
| 其他 | - | Viewer (連結分享) |

**修改權限**:
Google Sheets → Share → Add people

---

## 🚨 安全規則

### 1. 程式碼修改

**誰可以修改**: 只有 Jacky + User

**流程**:
```bash
# 1. 本地修改
cd ~/clawd/projects/step1ne-headhunter-system
# ... 修改程式碼 ...

# 2. 測試
npm run build  # 前端測試
cd server && npm start  # 後端測試

# 3. Commit + Push
git add -A
git commit -m "feat: ..."
git push origin main

# 4. Zeabur 自動部署（1-2 分鐘）
```

**其他人**: ❌ 不能推送程式碼

---

### 2. API 使用

**誰可以使用**: 所有 AI 助理

**限制**:
- 唯讀 API（除了評級功能）
- 快取 30 分鐘
- 只能查詢主人負責的候選人（AI 助理）

**無需認證**: 目前 API 為公開（只讀模式）

**未來**: 可能加入 API Token 認證

---

### 3. 群組通知 ⚠️ 重要變更

**舊規則** (已廢除):
```bash
# ❌ 不再使用
發送到 HR AI招募自動化群組 (-1003231629634)
```

**新規則** (2026-02-23 起):
```bash
# ✅ 私訊主人
AI 處理完履歷 → 私訊主人（@username 或 USER_ID）
不發送到群組
```

**實作**:
```bash
# 錯誤示範
TELEGRAM_CHAT_ID="-1003231629634/4"  # 群組

# 正確做法
OWNER_TELEGRAM="@behe10"  # 私訊 Phoebe
OWNER_TELEGRAM="@jackyyuqi"  # 私訊 Jacky
```

---

## 🆕 新增 AI 助理

### 流程

**步驟 1**: 確認需求
- AI 的主人是誰？
- 需要哪些權限？

**步驟 2**: 建立配置檔
```bash
# 複製範本
cp ~/clawd/projects/step1ne-headhunter-skill/AI-CONFIG-TEMPLATE.md \
   ~/clawd/new-ai-config.sh

# 編輯配置
nano ~/clawd/new-ai-config.sh

# 填寫主人資訊
export AI_OWNER_NAME="Mike"
export AI_OWNER_TELEGRAM="@mike_user"
export AI_CONSULTANT_CODE="Mike"
```

**步驟 3**: AI 閱讀文檔
- AI-ONBOARDING.md (必讀)
- CONNECT-GUIDE.md (API 使用)
- AI-CONFIG-TEMPLATE.md (配置範本)

**步驟 4**: 測試
```bash
source ~/clawd/new-ai-config.sh
curl "$STEP1NE_API_URL/health"
```

**步驟 5**: 開始使用

**無需**: 修改程式碼或系統設定

---

## 🆕 新增獵頭顧問帳號

### 流程

**步驟 1**: 修改後端程式碼（需要管理員）

編輯 `step1ne-headhunter-system/server/server.js`:

```javascript
const users = [
  // ... 現有用戶 ...
  {
    id: '4',  // 新 ID
    username: 'mike',
    name: 'Mike',
    email: 'mike@step1ne.com',
    role: 'REVIEWER',  // 顧問角色
    consultant: 'Mike'
  }
];
```

**步驟 2**: 推送到 GitHub

```bash
git add server/server.js
git commit -m "feat: Add Mike account"
git push origin main
```

**步驟 3**: 等待 Zeabur 部署（1-2 分鐘）

**步驟 4**: 新用戶可登入

訪問 https://step1ne.zeabur.app → 選擇「Mike」

---

## 📞 權限申請

**如果需要更高權限**:
1. 聯絡 Jacky (@jackyyuqi)
2. 說明需求與原因
3. 等待審核

**一般情況**: AI 助理不需要額外權限。

---

## 🔄 定期審查

**每季度檢查**:
- [ ] 檢查 GitHub Collaborators
- [ ] 檢查 Google Sheets 權限
- [ ] 檢查 API 使用情況
- [ ] 檢查用戶帳號（移除離職人員）
- [ ] 更新此文檔

---

**建立日期**: 2026-02-23  
**維護者**: Jacky + User  
**版本**: 1.0.0
