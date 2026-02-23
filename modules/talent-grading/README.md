# 人才評級系統 (Talent Grading)

## 功能

綜合評估候選人整體素質，評級為 S/A+/A/B/C。

## 核心檔案

- `grading-logic.py` - 評分邏輯（待實作）
- `TALENT-GRADING-RULES.md` - 完整評級規則

## 評級標準

| 等級 | 分數 | 說明 |
|------|------|------|
| S | 90-100 | 頂尖人才（稀缺） |
| A+ | 80-89 | 優秀人才（強力推薦） |
| A | 70-79 | 合格人才（可推薦） |
| B | 60-69 | 基本合格（需評估） |
| C | <60 | 需補強（謹慎推薦） |

## 6 大評分維度

1. **學歷背景** (20%) - 學位等級
2. **工作年資** (20%) - 總年資與經驗
3. **技能廣度** (20%) - 技能數量與深度
4. **工作穩定性** (20%) - 穩定度評分
5. **職涯發展軌跡** (10%) - 晉升/平行/停滯
6. **特殊加分** (10%) - 名校/大廠/開源/語言

## 使用方式

```bash
python grading-logic.py \
  --resume "候選人履歷.json" \
  --output grade-result.json
```

## 邊緣案例處理

詳見 `edge-cases.md`：
- 社會新鮮人（0 年經驗）
- 只有一份工作（無法計算穩定性）
- 職涯空窗期處理

## 資料流

```
Bot 上傳履歷
  ↓
Backend API (/api/candidates)
  ↓
grading-logic.py (計算評級)
  ↓
Google Sheets (Column U: 綜合評級)
  ↓
Frontend 顯示
```

## 狀態

⏳ **待實作** - 評分邏輯程式碼開發中

## 相關文檔

- `TALENT-GRADING-RULES.md` - 完整規則說明
- `training/grading-practice.md` - 實戰練習
