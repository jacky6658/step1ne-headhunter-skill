# BD 客戶穩定爬蟲系統

## 功能特色

✅ **穩定可靠**
- 多層重試機制（每家最多3次）
- 失敗自動跳過，不影響後續處理
- 失敗率>70%自動暫停

✅ **斷點續爬**
- 隨時可暫停/繼續
- 進度自動保存
- 不會重複處理已完成的公司

✅ **實時監控**
- 每5家回報進度
- 詳細日誌記錄
- 可隨時查看狀態

✅ **數據驗證**
- 檢查電話/Email格式
- 避免重複資料
- 自動使用現有資料補充

## 快速開始

### 1. 安裝依賴

需要已安裝：
- Python 3
- gog CLI（Google Sheets 操作）
- agent-browser（網頁自動化）

### 2. 配置

複製配置範例：
```bash
cp config.example.json config.json
```

編輯 `config.json`：
```json
{
  "sheet_id": "你的Google Sheet ID",
  "gog_account": "你的Google帳號",
  "delay_min": 8,
  "delay_max": 15,
  "max_retries": 3,
  "batch_report_size": 5
}
```

### 3. 準備資料

建立待處理清單 `/tmp/companies-from-70.json`：
```json
[
  {
    "row": 70,
    "company": "公司名稱",
    "phone": "待查",
    "email": "待查"
  }
]
```

### 4. 執行

**開始爬蟲：**
```bash
bash run-scraper.sh start [數量]
```

**繼續執行：**
```bash
bash run-scraper.sh resume
```

**查看狀態：**
```bash
bash run-scraper.sh status
```

**查看日誌：**
```bash
bash run-scraper.sh log
```

**重置進度：**
```bash
bash run-scraper.sh reset
```

## 工作原理

### 流程

1. **104 站內搜尋** → 找到公司頁面
2. **訪問公司頁面** → 提取電話、Email
3. **數據驗證** → 檢查格式
4. **更新 Google Sheet** → 儲存結果
5. **隨機延遲** → 防反爬蟲

### 進度記錄

系統會自動記錄進度到 `progress.json`：
```json
{
  "processed": [70, 71, 72],
  "success": [70, 71],
  "failed": [72],
  "total_processed": 3,
  "total_success": 2,
  "total_failed": 1
}
```

### 日誌檔案

所有執行細節記錄在 `scraper.log`：
```
[2026-02-12 11:02:00] [INFO] 開始處理 247 家公司
[2026-02-12 11:02:00] [INFO] [1/247] 中鹿營造股份有限公司
[2026-02-12 11:02:00] [INFO] 處理: 中鹿營造股份有限公司 (Row 70)
[2026-02-12 11:02:05] [INFO]   ✅ 找到: https://www.104.com.tw/company/xxxxx
[2026-02-12 11:02:10] [INFO]   📞 電話: 02-12345678
[2026-02-12 11:02:10] [INFO]   📧 Email: contact@example.com
[2026-02-12 11:02:12] [INFO]   Sheet更新: Updated 2 cells
```

## 性能指標

**實測數據（2026-02-12）：**
- 平均速度：12 秒/家
- 成功率：100%（65/65）
- 247 家預計：約 50 分鐘

## 安全機制

✅ **防反爬蟲**
- 隨機延遲 8-15 秒
- 失敗重試間隔 5 秒
- 失敗率過高自動暫停

✅ **錯誤處理**
- 單家失敗不影響整體
- 詳細錯誤日誌
- 進度自動保存

✅ **數據驗證**
- 電話格式：0X-XXXXXXX
- Email 格式：標準 RFC 5322

## 常見問題

**Q: 如何暫停爬蟲？**
A: 按 Ctrl+C 或刪除進程

**Q: 如何從特定行開始？**
A: 修改待處理清單，只包含需要的公司

**Q: 失敗的公司會重試嗎？**
A: 會自動重試3次，仍失敗則跳過

**Q: 如何查看成功率？**
A: 執行 `bash run-scraper.sh status`

## 更新日誌

### v1.0 (2026-02-12)
- ✅ 初版發布
- ✅ 穩定運行測試通過
- ✅ 100% 成功率（65 家測試）

## 授權

MIT License

## 作者

Jacky Chen x YuQi 🦞
