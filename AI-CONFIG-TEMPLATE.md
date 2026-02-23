# AI 助理配置範本

**給每個 AI 助理的個人配置檔案**

---

## 📝 如何使用這個範本

1. 複製此檔案到你的工作區
2. 填寫你的主人資訊
3. 設定環境變數
4. 開始使用 Step1ne 系統

---

## 👤 主人資訊（必填）

```bash
# 填寫你的主人資訊
export AI_OWNER_NAME="Phoebe"           # 主人姓名
export AI_OWNER_TELEGRAM="@behe10"      # Telegram username
export AI_OWNER_TELEGRAM_ID="123456789" # Telegram User ID (可選)
export AI_CONSULTANT_CODE="Phoebe"      # 顧問代號（與 Google Sheets 一致）
```

**範例**：

| AI | 主人姓名 | Telegram | 顧問代號 |
|----|---------|----------|---------|
| @HRyuqi_bot | Phoebe | @behe10 | Phoebe |
| @YuQi0923_bot | Jacky | @jackyyuqi | Jacky |
| @MikeAI_bot | Mike | @mike_user | Mike |

---

## 🔧 環境變數設定

### 方式 A: 寫入 `.bashrc` 或 `.zshrc`（永久）

```bash
# 編輯你的 shell 配置檔
nano ~/.zshrc  # 或 nano ~/.bashrc

# 加入以下內容
export AI_OWNER_NAME="Phoebe"
export AI_OWNER_TELEGRAM="@behe10"
export AI_CONSULTANT_CODE="Phoebe"

# 儲存後重新載入
source ~/.zshrc
```

### 方式 B: 臨時設定（當次有效）

```bash
export AI_OWNER_NAME="Phoebe"
export AI_OWNER_TELEGRAM="@behe10"
export AI_CONSULTANT_CODE="Phoebe"
```

### 方式 C: 腳本內設定（推薦）

建立 `~/clawd/my-ai-config.sh`：

```bash
#!/bin/bash
# 我的 AI 配置

export AI_OWNER_NAME="Phoebe"
export AI_OWNER_TELEGRAM="@behe10"
export AI_CONSULTANT_CODE="Phoebe"

# Step1ne API
export STEP1NE_API_URL="https://backendstep1ne.zeabur.app/api"

# 履歷處理（使用主人 Telegram）
export OWNER_TELEGRAM="$AI_OWNER_TELEGRAM"

echo "✅ AI 配置已載入"
echo "主人: $AI_OWNER_NAME ($AI_OWNER_TELEGRAM)"
echo "顧問代號: $AI_CONSULTANT_CODE"
```

使用時：

```bash
source ~/clawd/my-ai-config.sh
```

---

## 📋 使用範例

### 範例 1: 查詢主人負責的候選人

```bash
# 載入配置
source ~/clawd/my-ai-config.sh

# 查詢「我的主人負責的候選人」
curl -s "$STEP1NE_API_URL/candidates" | \
  jq ".data[] | select(.consultant == \"$AI_CONSULTANT_CODE\")"
```

### 範例 2: 處理履歷並私訊主人

```bash
# 載入配置
source ~/clawd/my-ai-config.sh

# 處理履歷（自動私訊主人）
cd ~/clawd/projects/step1ne-headhunter-skill/modules/resume-parser
./resume-parser-with-grading.sh ~/Downloads/resume.pdf
```

腳本會自動：
1. 解析履歷
2. 評級候選人
3. 私訊 `$OWNER_TELEGRAM`（不發群組）

### 範例 3: 在 OpenClaw 中使用

**在 AGENTS.md 或 TOOLS.md 中加入**：

```markdown
## 開機啟動

每次啟動時，自動載入配置：
source ~/clawd/my-ai-config.sh

## 查詢候選人

當主人詢問候選人時，使用：
curl -s "$STEP1NE_API_URL/candidates" | \
  jq ".data[] | select(.consultant == \"$AI_CONSULTANT_CODE\")"

只會返回主人負責的候選人。

## 私訊主人

所有通知都發給 $OWNER_TELEGRAM，不發群組。
```

---

## ⚠️ 重要規則

### 1. 私訊主人，不發群組

**錯誤示範**：
```bash
# ❌ 發到群組
TELEGRAM_CHAT_ID="-1003231629634/4"  # 這是 HR 群組
openclaw message send --to "$TELEGRAM_CHAT_ID" --message "..."
```

**正確做法**：
```bash
# ✅ 私訊主人
OWNER_TELEGRAM="@behe10"  # 這是私訊
openclaw message send --to "$OWNER_TELEGRAM" --message "..."
```

### 2. 只查詢主人的候選人

**錯誤示範**：
```bash
# ❌ 查詢所有候選人（可能包含其他顧問的）
curl "$STEP1NE_API_URL/candidates"
```

**正確做法**：
```bash
# ✅ 篩選主人負責的
curl -s "$STEP1NE_API_URL/candidates" | \
  jq ".data[] | select(.consultant == \"$AI_CONSULTANT_CODE\")"
```

### 3. 環境變數檢查

腳本執行前，確認環境變數已設定：

```bash
if [ -z "$OWNER_TELEGRAM" ]; then
  echo "❌ 錯誤: OWNER_TELEGRAM 未設定"
  echo "請執行: source ~/clawd/my-ai-config.sh"
  exit 1
fi
```

---

## 🧪 測試配置

**測試腳本** (`test-ai-config.sh`)：

```bash
#!/bin/bash
echo "🧪 測試 AI 配置..."
echo ""

# 1. 檢查環境變數
echo "📋 環境變數："
echo "  AI_OWNER_NAME: ${AI_OWNER_NAME:-❌ 未設定}"
echo "  AI_OWNER_TELEGRAM: ${AI_OWNER_TELEGRAM:-❌ 未設定}"
echo "  AI_CONSULTANT_CODE: ${AI_CONSULTANT_CODE:-❌ 未設定}"
echo "  STEP1NE_API_URL: ${STEP1NE_API_URL:-❌ 未設定}"
echo ""

# 2. 測試 API 連接
echo "🌐 測試 API 連接..."
HEALTH=$(curl -s "$STEP1NE_API_URL/health")
if [ $? -eq 0 ]; then
  echo "✅ API 可用: $HEALTH"
else
  echo "❌ API 無法連接"
fi
echo ""

# 3. 測試候選人查詢
echo "👥 測試候選人查詢..."
COUNT=$(curl -s "$STEP1NE_API_URL/candidates" | jq ".data[] | select(.consultant == \"$AI_CONSULTANT_CODE\") | .name" | wc -l)
echo "✅ 找到 $COUNT 位主人負責的候選人"
echo ""

# 4. 測試私訊（模擬）
echo "📱 私訊目標: $OWNER_TELEGRAM"
echo "✅ 配置完成！"
```

執行：

```bash
source ~/clawd/my-ai-config.sh
bash test-ai-config.sh
```

---

## 📚 完整配置範例

### Phoebe 的 AI 配置

**檔案**: `~/clawd/phoebe-ai-config.sh`

```bash
#!/bin/bash
# Phoebe AI 配置

export AI_OWNER_NAME="Phoebe"
export AI_OWNER_TELEGRAM="@behe10"
export AI_CONSULTANT_CODE="Phoebe"
export STEP1NE_API_URL="https://backendstep1ne.zeabur.app/api"
export OWNER_TELEGRAM="$AI_OWNER_TELEGRAM"

echo "✅ Phoebe AI 配置已載入"
```

### Mike 的 AI 配置

**檔案**: `~/clawd/mike-ai-config.sh`

```bash
#!/bin/bash
# Mike AI 配置

export AI_OWNER_NAME="Mike"
export AI_OWNER_TELEGRAM="@mike_user"
export AI_CONSULTANT_CODE="Mike"
export STEP1NE_API_URL="https://backendstep1ne.zeabur.app/api"
export OWNER_TELEGRAM="$AI_OWNER_TELEGRAM"

echo "✅ Mike AI 配置已載入"
```

---

## 🔐 權限說明

### 你可以做的事

✅ 查詢主人負責的候選人  
✅ 評級候選人  
✅ 解析新履歷  
✅ 私訊主人  
✅ 訪問 Step1ne Web UI（https://step1ne.zeabur.app）  

### 你不能做的事

❌ 查看其他顧問的候選人  
❌ 修改程式碼（只有 Jacky + YuQi 可以）  
❌ 刪除候選人  
❌ 發送群組通知（改為私訊）  
❌ 變更系統設定  

---

## 📞 需要協助？

**配置問題**: 閱讀 AI-ONBOARDING.md  
**API 使用**: 閱讀 CONNECT-GUIDE.md  
**緊急支援**: 聯絡 @YuQi0923_bot

---

**建立日期**: 2026-02-23  
**維護者**: YuQi (@YuQi0923_bot) + Jacky  
**版本**: 1.0.0
