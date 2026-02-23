#!/bin/bash
# 標準履歷匯入腳本 - 強制使用正確格式
# 用途：將履歷匯入到履歷池v2（確保 20 個欄位正確對應）

SHEET_ID="1PunpaDAFBPBL_I76AiRYGXKaXDZvMl1c262SEtxRk6Q"
ACCOUNT="aijessie88@step1ne.com"

# 顏色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}📋 Step1ne 履歷池匯入工具${NC}"
echo "========================================"
echo ""

# 使用說明
if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    echo "用法："
    echo "  $0 <JSON檔案>"
    echo ""
    echo "JSON 檔案格式："
    echo '{'
    echo '  "name": "候選人姓名",'
    echo '  "email": "email@example.com",'
    echo '  "phone": "電話（選填）",'
    echo '  "location": "地點",'
    echo '  "currentPosition": "目前職位",'
    echo '  "totalYears": 2,'
    echo '  "jobChanges": 2,'
    echo '  "avgTenure": 12,'
    echo '  "recentGap": 0,'
    echo '  "skills": "技能1、技能2、技能3",'
    echo '  "education": "學歷",'
    echo '  "source": "LinkedIn/GitHub/推薦",'
    echo '  "workHistory": "工作經歷簡述（非JSON）",'
    echo '  "leaveReason": "離職原因",'
    echo '  "stabilityScore": 85,'
    echo '  "educationDetail": "學歷詳情",'
    echo '  "personality": "DISC/Big Five（選填）",'
    echo '  "status": "新進/面試中/已推薦",'
    echo '  "consultant": "Jacky/Phoebe",'
    echo '  "notes": "備註"'
    echo '}'
    exit 0
fi

# 檢查參數
if [ -z "$1" ]; then
    echo -e "${RED}❌ 錯誤：請提供 JSON 檔案${NC}"
    echo "用法：$0 <JSON檔案>"
    echo "或執行：$0 --help 查看說明"
    exit 1
fi

JSON_FILE="$1"

# 檢查檔案存在
if [ ! -f "$JSON_FILE" ]; then
    echo -e "${RED}❌ 錯誤：檔案不存在 - $JSON_FILE${NC}"
    exit 1
fi

# 解析 JSON（使用 jq）
if ! command -v jq &> /dev/null; then
    echo -e "${RED}❌ 錯誤：需要安裝 jq${NC}"
    echo "安裝指令：brew install jq"
    exit 1
fi

echo "📖 讀取候選人資料..."

# 讀取 JSON 欄位
NAME=$(jq -r '.name // ""' "$JSON_FILE")
EMAIL=$(jq -r '.email // ""' "$JSON_FILE")
PHONE=$(jq -r '.phone // ""' "$JSON_FILE")
LOCATION=$(jq -r '.location // ""' "$JSON_FILE")
POSITION=$(jq -r '.currentPosition // ""' "$JSON_FILE")
YEARS=$(jq -r '.totalYears // 0' "$JSON_FILE")
CHANGES=$(jq -r '.jobChanges // 0' "$JSON_FILE")
AVG_TENURE=$(jq -r '.avgTenure // 0' "$JSON_FILE")
GAP=$(jq -r '.recentGap // 0' "$JSON_FILE")
SKILLS=$(jq -r '.skills // ""' "$JSON_FILE")
EDUCATION=$(jq -r '.education // ""' "$JSON_FILE")
SOURCE=$(jq -r '.source // "LinkedIn"' "$JSON_FILE")
WORK_HISTORY=$(jq -r '.workHistory // ""' "$JSON_FILE")
LEAVE_REASON=$(jq -r '.leaveReason // ""' "$JSON_FILE")
STABILITY=$(jq -r '.stabilityScore // 0' "$JSON_FILE")
EDU_DETAIL=$(jq -r '.educationDetail // ""' "$JSON_FILE")
PERSONALITY=$(jq -r '.personality // ""' "$JSON_FILE")
STATUS=$(jq -r '.status // "新進"' "$JSON_FILE")
CONSULTANT=$(jq -r '.consultant // "Jacky"' "$JSON_FILE")
NOTES=$(jq -r '.notes // ""' "$JSON_FILE")

# 驗證必填欄位
if [ -z "$NAME" ]; then
    echo -e "${RED}❌ 錯誤：姓名為必填欄位${NC}"
    exit 1
fi

echo ""
echo "👤 候選人資訊："
echo "   姓名：$NAME"
echo "   Email：$EMAIL"
echo "   職位：$POSITION"
echo "   年資：${YEARS}年"
echo "   技能：${SKILLS:0:50}..."
echo ""

# 準備資料（用 | 分隔，20 個欄位）
# 姓名|Email|電話|地點|目前職位|總年資(年)|轉職次數|平均任職(月)|最近gap(月)|技能|學歷|來源|工作經歷JSON|離職原因|穩定性評分|學歷JSON|DISC/Big Five|狀態|獵頭顧問|備註
DATA="$NAME|$EMAIL|$PHONE|$LOCATION|$POSITION|$YEARS|$CHANGES|$AVG_TENURE|$GAP|$SKILLS|$EDUCATION|$SOURCE|$WORK_HISTORY|$LEAVE_REASON|$STABILITY|$EDU_DETAIL|$PERSONALITY|$STATUS|$CONSULTANT|$NOTES"

# 檢查資料是否有換行（會導致匯入錯誤）
LINE_COUNT=$(echo "$DATA" | wc -l | tr -d ' ')
if [ "$LINE_COUNT" != "1" ]; then
    echo -e "${RED}❌ 錯誤：資料包含換行符號（$LINE_COUNT 行）${NC}"
    echo "請檢查 JSON 檔案中的資料是否有換行"
    exit 1
fi

# 詢問確認
echo -e "${YELLOW}⚠️  請確認資料無誤，即將匯入到履歷池v2${NC}"
read -p "是否繼續？(y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 取消匯入"
    exit 0
fi

echo ""
echo "🔄 匯入中..."

# 先找到下一個空行（避免覆蓋現有資料）
# 簡單做法：直接 append 到最後
ROW=$(gog sheets get "$SHEET_ID" "履歷池v2!A:A" --account "$ACCOUNT" 2>&1 | grep -v "^$" | wc -l | tr -d ' ')
NEXT_ROW=$((ROW + 1))

echo "📍 將匯入到第 $NEXT_ROW 行..."

# 使用 update 而非 append（避免錯位）
gog sheets update "$SHEET_ID" "履歷池v2!A${NEXT_ROW}" "$DATA" --account "$ACCOUNT"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ 履歷匯入成功！${NC}"
    echo ""
    echo "📊 匯入資訊："
    echo "   位置：履歷池v2 第 $NEXT_ROW 行"
    echo "   欄位：20 個（A-T）"
    echo "   Sheet：https://docs.google.com/spreadsheets/d/$SHEET_ID"
    echo ""
    
    # 驗證匯入結果
    echo "🔍 驗證匯入結果..."
    gog sheets get "$SHEET_ID" "履歷池v2!A${NEXT_ROW}:T${NEXT_ROW}" --account "$ACCOUNT"
    
    echo ""
    echo -e "${GREEN}✅ 所有欄位已正確匯入！${NC}"
else
    echo ""
    echo -e "${RED}❌ 匯入失敗${NC}"
    exit 1
fi
