# 履歷解析系統 (Resume Parser)

## 功能

自動監控履歷進件（Gmail + Telegram），解析 PDF 履歷，結構化資料並匯入履歷池。

## 核心檔案

- `auto-resume-filing.sh` - 自動歸檔腳本

## 使用方式

### 手動執行
```bash
cd ~/clawd/projects/step1ne-headhunter-skill/modules/resume-parser
./auto-resume-filing.sh
```

### 自動執行（Cron）
每小時自動執行，監控：
- Gmail 收件匣（關鍵字：應徵、履歷、求職）
- Telegram 上傳（Topic 4: 履歷進件）

## 解析流程

```
1. 掃描 Gmail inbox
   ↓
2. 下載 PDF 附件
   ↓
3. 提取文字（PyPDF2）
   ↓
4. 結構化資料（JSON）
   ├─ 姓名、Email、電話
   ├─ 工作經歷（陣列）
   ├─ 教育背景（陣列）
   ├─ 技能清單
   └─ 穩定度評分
   ↓
5. 匯入履歷池（Google Sheets）
   ↓
6. Telegram 通知（Topic 304）
```

## 支援格式

- ✅ PDF（優先）
- ✅ DOCX（待測試）
- ❌ 圖片（需 OCR）

## 資料欄位（20 欄）

| 欄位 | 範例 | 說明 |
|------|------|------|
| 姓名 | 張大明 | A 欄 |
| Email | test@example.com | B 欄 |
| 電話 | 0912-345-678 | C 欄 |
| 職位 | 前端工程師 | D 欄 |
| 技能 | React, TypeScript, Node.js | H 欄 |
| 年資 | 5.5 | I 欄 |
| ... | ... | ... |

## 已知限制

⚠️ **Telegram PDF 監控未整合** - 目前只監控 Gmail

## 待改進

- [ ] 整合 Telegram PDF 上傳監控
- [ ] 支援 DOCX 格式
- [ ] OCR 圖片履歷
- [ ] AI 自動分類（技術/非技術/管理）

## 相關模組

- `talent-grading` - 自動評級
- `ai-matcher` - 自動配對推薦

## Cron Job

**ID**: `b6769222`  
**排程**: 每小時  
**狀態**: ✅ 運行中
