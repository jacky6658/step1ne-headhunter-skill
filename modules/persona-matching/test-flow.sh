#!/bin/bash
# 測試人才畫像 + 公司畫像匹配完整流程

echo "=== Persona Matching System 測試流程 ==="
echo ""

# 切換到模組目錄
cd "$(dirname "$0")"

# 建立輸出目錄
mkdir -p output

echo "📋 步驟 1/4: 生成候選人畫像..."
python3 generate-candidate-persona.py \
  --resume examples/test-candidate-resume.json \
  --output output/candidate-persona.json

echo ""
echo "🏢 步驟 2/4: 生成公司畫像..."
python3 generate-company-persona.py \
  --job examples/test-job.json \
  --company examples/test-company.json \
  --output output/company-persona.json

echo ""
echo "🎯 步驟 3/4: 執行匹配分析..."
python3 match-personas.py \
  --candidate output/candidate-persona.json \
  --company output/company-persona.json \
  --output output/match-report.json

echo ""
echo "📊 步驟 4/4: 查看匹配結果..."
echo ""
cat output/match-report.json | python3 -m json.tool | grep -A 5 "總分\|等級\|推薦優先級"

echo ""
echo "✅ 測試完成！完整報告已儲存在 output/ 資料夾"
echo ""
echo "查看詳細報告："
echo "  cat output/match-report.json | python3 -m json.tool"
