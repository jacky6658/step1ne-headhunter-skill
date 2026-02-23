# 履歷匯入標準流程

**最後更新**：2026-02-23  
**版本**：1.0  
**狀態**：🔒 強制執行（所有 AI Bot 必須遵守）

---

## ⚠️ 重要規則

**所有履歷匯入都必須按照此標準流程，無一例外！**

---

## 📋 履歷池 20 個欄位（固定順序）

```
1.  姓名
2.  Email
3.  電話
4.  地點
5.  目前職位
6.  總年資(年)
7.  轉職次數
8.  平均任職(月)
9.  最近gap(月)
10. 技能
11. 學歷
12. 來源
13. 工作經歷JSON
14. 離職原因
15. 穩定性評分
16. 學歷JSON
17. DISC/Big Five
18. 狀態
19. 獵頭顧問
20. 備註
```

**分隔符號**：`|`（管線符號，不是逗號）

---

## ✅ 標準匯入流程

### 步驟 1：準備 JSON 資料

**檔案格式**：`candidate-name.json`

```json
{
  "name": "廖家賢 (Salt)",
  "email": "heymrs4lt@gmail.com",
  "phone": "",
  "location": "台北市",
  "currentPosition": "Tech Researcher",
  "totalYears": 2,
  "jobChanges": 2,
  "avgTenure": 12,
  "recentGap": 0,
  "skills": "資訊安全、Penetration Test、Python、CTF、密碼學、零知識證明、區塊鏈",
  "education": "國立臺北科技大學資訊安全碩士（2023-2025在學中）",
  "source": "LinkedIn",
  "workHistory": "Turing Space (2024/9-12) Tech Researcher; 前韌體工程師/R&D/FAE (~2024/9)",
  "leaveReason": "尋求更好發展機會",
  "stabilityScore": 85,
  "educationDetail": "北科大資安碩士（2023-2025在學中）",
  "personality": "",
  "status": "新進",
  "consultant": "Jacky",
  "notes": "資安碩士is1ab實驗室，專長滲透測試/CTF/密碼學。證照：iPAS資安初級。LinkedIn: https://www.linkedin.com/in/heymrsalt"
}
```

### 步驟 2：執行匯入腳本

```bash
cd /Users/user/clawd/projects/step1ne-headhunter-skill/skills/headhunter

# 匯入履歷
./scripts/import-resume-to-pool.sh candidate-name.json
```

### 步驟 3：驗證結果

腳本會自動：
1. ✅ 檢查資料完整性
2. ✅ 驗證必填欄位
3. ✅ 檢查換行符號（避免錯位）
4. ✅ 使用 `update` 而非 `append`（精確定位）
5. ✅ 匯入後自動驗證（顯示匯入結果）

---

## ❌ 常見錯誤與解決方案

### 錯誤 1：資料錯位到其他欄位

**原因**：使用 `append` + 逗號分隔 + JSON 內有換行

**解決**：
- ✅ 使用 `update` + 指定範圍（如 `A248`）
- ✅ 使用 `|` 分隔符號
- ✅ 簡化 JSON 欄位（避免複雜轉義）

### 錯誤 2：資料分散到多行

**原因**：資料內有換行符號

**解決**：
```bash
# 檢查資料行數
echo "$DATA" | wc -l
# 必須是 1 行
```

### 錯誤 3：JSON 轉義錯誤

**原因**：JSON 欄位包含 `"` 或 `,` 被錯誤解析

**解決**：
- ✅ 工作經歷JSON 欄位：使用純文字描述（非 JSON 格式）
  - ❌ 錯誤：`[{"company":"XX","title":"YY"}]`
  - ✅ 正確：`XX公司 (2024/9-12) YY職位; 前公司 ZZ職位`
- ✅ 學歷JSON 欄位：同樣用純文字

---

## 🔧 工具位置

### 匯入腳本
```bash
/Users/user/clawd/projects/step1ne-headhunter-skill/skills/headhunter/scripts/import-resume-to-pool.sh
```

### 使用說明
```bash
./import-resume-to-pool.sh --help
```

### 測試範例
```bash
./import-resume-to-pool.sh examples/liao-chiahsien.json
```

---

## 📊 Google Sheets 資訊

- **Sheet ID**：`1PunpaDAFBPBL_I76AiRYGXKaXDZvMl1c262SEtxRk6Q`
- **分頁名稱**：履歷池v2
- **帳號**：aijessie88@step1ne.com
- **網址**：https://docs.google.com/spreadsheets/d/1PunpaDAFBPBL_I76AiRYGXKaXDZvMl1c262SEtxRk6Q

---

## 🎓 關鍵教訓（2026-02-23）

### 廖家賢履歷匯入事件

**錯誤過程**：
1. ❌ 第一次：使用 `|` 分隔 + `append` → 資料錯位（236-248行）
2. ❌ 第二次：使用 `,` 分隔 + `append` → 資料分散（C248-279欄）
3. ✅ 第三次：使用 `|` 分隔 + `update A248` → **成功**

**成功關鍵**：
```bash
# 準備資料（單行，| 分隔，簡化 JSON）
DATA="姓名|email||地點|職位|2|2|12|0|技能|學歷|來源|工作簡述|離職原因|85|學歷詳情||新進|Jacky|備註"

# 使用 update 指定精確位置（而非 append）
gog sheets update "$SHEET_ID" "履歷池v2!A248" "$DATA" --account "$ACCOUNT"
```

**Jacky 要求**：
> "以後都給我這樣做，獵頭模組要給我更新"

---

## 🚀 快速參考

### 完整匯入指令（一行版）

```bash
# 1. 準備資料（20 個欄位，用 | 分隔）
DATA="姓名|email|電話|地點|職位|年資|轉職次數|平均任職|gap|技能|學歷|來源|工作經歷|離職原因|穩定性|學歷詳情|性格|狀態|顧問|備註"

# 2. 找到下一個空行
ROW=$(gog sheets get "1PunpaDAFBPBL_I76AiRYGXKaXDZvMl1c262SEtxRk6Q" "履歷池v2!A:A" --account "aijessie88@step1ne.com" 2>&1 | grep -v "^$" | wc -l | tr -d ' ')
NEXT_ROW=$((ROW + 1))

# 3. 匯入（使用 update）
gog sheets update "1PunpaDAFBPBL_I76AiRYGXKaXDZvMl1c262SEtxRk6Q" "履歷池v2!A${NEXT_ROW}" "$DATA" --account "aijessie88@step1ne.com"

# 4. 驗證結果
gog sheets get "1PunpaDAFBPBL_I76AiRYGXKaXDZvMl1c262SEtxRk6Q" "履歷池v2!A${NEXT_ROW}:T${NEXT_ROW}" --account "aijessie88@step1ne.com"
```

---

## ✅ 檢查清單

匯入前必檢查：

- [ ] 資料準備完整（20 個欄位）
- [ ] 使用 `|` 分隔符號
- [ ] 資料是單行（無換行符號）
- [ ] 工作經歷JSON 欄位簡化（純文字描述）
- [ ] 必填欄位已填寫（姓名、Email、職位）
- [ ] 使用 `update` 而非 `append`
- [ ] 指定精確範圍（如 `A248`）
- [ ] 匯入後驗證結果

---

## 🔄 版本歷史

| 版本 | 日期 | 變更內容 |
|------|------|---------|
| 1.0 | 2026-02-23 | 初版建立（基於廖家賢履歷匯入事件） |

---

**維護者**：Step1ne Team  
**聯絡人**：Jacky Chen  
**最後更新**：2026-02-23 23:22
