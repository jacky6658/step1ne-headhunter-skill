# Step1ne 前端系統依賴清單

本文檔記錄 Step1ne Headhunter System 前端所需的所有 npm 依賴。

**目標**：讓任何 AI Bot 都知道需要安裝哪些套件來完整使用 Step1ne 系統。

---

## 📦 核心依賴

### React 框架
```bash
npm install react react-dom
```

### 路由與狀態管理
```bash
npm install react-router-dom
```

### UI 組件庫
```bash
npm install lucide-react  # Icon 圖示庫
```

### CSS 框架
```bash
npm install tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

---

## 📄 PDF 生成（重要！）

**用途**：匯出 AI 配對報告為專業 PDF 文件

```bash
npm install jspdf jspdf-autotable
```

### 為什麼需要 jsPDF？

**使用場景**：
1. 獵頭顧問完成 AI 配對後
2. 點擊「匯出 PDF 報告」按鈕
3. 系統生成包含以下內容的專業 PDF：
   - 封面頁（職缺、公司資訊）
   - 配對摘要（統計卡片 + Top 5 表格）
   - 每個候選人詳細報告（分數、亮點、風險、建議）
   - 頁碼與專業排版

**檔案位置**：
- 工具函數：`utils/pdfGenerator.ts`
- 使用範例：`pages/AIMatchingPage.tsx`

**生成的 PDF 包含**：
- ✅ 彩色統計卡片
- ✅ 專業表格（autotable）
- ✅ 自動分頁
- ✅ 頁碼
- ✅ 中文支援

**檔名格式**：
```
Step1ne_配對報告_{職缺名稱}_{日期}.pdf

範例：
Step1ne_配對報告_AI工程師_2026-02-23.pdf
```

### 程式碼範例

```typescript
import { generateMatchingReportPDF } from '../utils/pdfGenerator';

// 生成 PDF 報告
generateMatchingReportPDF({
  jobTitle: 'AI工程師',
  companyName: 'AIJob內部',
  summary: matchResults.summary,
  matches: matchResults.matches
});
```

---

## 🔧 開發工具

### 建構工具
```bash
npm install vite @vitejs/plugin-react -D
```

### TypeScript 支援
```bash
npm install typescript @types/react @types/react-dom -D
```

---

## 📊 完整安裝指令

**一次安裝所有依賴**：

```bash
cd /path/to/step1ne-headhunter-system

# 生產依賴
npm install react react-dom react-router-dom lucide-react jspdf jspdf-autotable

# 開發依賴
npm install -D vite @vitejs/plugin-react typescript @types/react @types/react-dom tailwindcss postcss autoprefixer

# 初始化 Tailwind CSS
npx tailwindcss init -p
```

---

## 🤖 AI Bot 整合注意事項

### 當 AI Bot 需要使用 Step1ne 系統時

**步驟 1：檢查環境**
```bash
# 確認 Node.js 已安裝
node --version  # 需要 v18+

# 確認 npm 已安裝
npm --version
```

**步驟 2：安裝依賴**
```bash
cd step1ne-headhunter-system
npm install
```

**步驟 3：啟動系統**
```bash
# 前端
npm run dev

# 後端（另一個終端）
cd server
npm run dev
```

**步驟 4：驗證 PDF 功能**
- 訪問 http://localhost:3000/
- 進入「AI 配對推薦」頁面
- 完成配對後點擊「匯出 PDF 報告」
- 確認 PDF 正常下載

---

## 🔍 依賴說明

| 套件 | 版本 | 用途 | 必需？ |
|------|------|------|--------|
| `react` | ^18.0.0 | UI 框架 | ✅ 必需 |
| `react-dom` | ^18.0.0 | React DOM 渲染 | ✅ 必需 |
| `react-router-dom` | ^6.0.0 | 路由管理 | ✅ 必需 |
| `lucide-react` | ^0.x | Icon 圖示 | ✅ 必需 |
| `jspdf` | ^2.x | PDF 生成核心 | ✅ 必需（匯出功能）|
| `jspdf-autotable` | ^3.x | PDF 表格支援 | ✅ 必需（匯出功能）|
| `tailwindcss` | ^3.x | CSS 框架 | ✅ 必需 |
| `vite` | ^6.x | 建構工具 | ✅ 必需（開發）|
| `typescript` | ^5.x | 類型檢查 | ⚠️ 建議 |

---

## ❗ 常見問題

### Q1: 為什麼需要 jspdf-autotable？

**A**: `jspdf` 只提供基本的 PDF 生成功能，`jspdf-autotable` 提供專業的表格繪製功能，用於：
- Top 5 推薦表格
- 維度評分表格
- 自動分頁處理

沒有它，PDF 中的表格會變成純文字，排版會很糟糕。

### Q2: 可以使用其他 PDF 庫嗎（如 pdfmake）？

**A**: 可以，但需要重寫 `utils/pdfGenerator.ts`。目前選擇 jsPDF 是因為：
- ✅ 輕量（打包後約 200KB）
- ✅ 中文支援較好
- ✅ autotable 插件成熟
- ✅ 文檔完善

### Q3: PDF 中文顯示有問題？

**A**: jsPDF 預設不支援中文字體。目前使用瀏覽器預設字體，在大多數環境下可正常顯示。

**如需完美中文支援**：
```typescript
// 需要額外載入中文字體檔案
import NotoSansTC from './fonts/NotoSansTC-Regular.ttf';
doc.addFileToVFS("NotoSansTC.ttf", NotoSansTC);
doc.addFont("NotoSansTC.ttf", "NotoSansTC", "normal");
doc.setFont("NotoSansTC");
```

---

## 🔄 版本更新記錄

### 2026-02-23
- ✅ 新增 jsPDF 依賴（PDF 生成功能）
- ✅ 建立 FRONTEND-DEPENDENCIES.md 文檔

### 2026-02-23
- ✅ 初版系統建立
- ✅ React + Vite + Tailwind CSS 架構

---

## 📚 延伸閱讀

- [jsPDF 官方文檔](https://github.com/parallax/jsPDF)
- [jsPDF-AutoTable 文檔](https://github.com/simonbengtsson/jsPDF-AutoTable)
- [Step1ne API 文檔](../step1ne-headhunter-system/docs/API.md)
- [Bot 整合範例](../step1ne-headhunter-system/docs/bot-examples/)

---

## 🤝 貢獻

發現缺少依賴？歡迎提交 Pull Request 更新此文檔！

---

**維護者**：Jacky Chen x YuQi 🦞  
**最後更新**：2026-02-23
