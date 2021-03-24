#!/bin/bash
echo "🧪 تست سرور Tetrashop API"

# اجرای سرور در پس‌زمینه
python simple_api_server.py &
SERVER_PID=$!
echo "📡 سرور راه‌اندازی شد (PID: $SERVER_PID)"

# صبر کردن برای راه‌افتادن سرور
sleep 2

echo ""
echo "🔍 تست سلامت API:"
curl -s http://localhost:8000/api/health | python -m json.tool

echo ""
echo "🔍 تست صفحه اصلی:"
curl -s http://localhost:8000/ | python -m json.tool

echo ""
echo "🔍 تست ایجاد سشن:"
curl -s -X POST http://localhost:8000/api/v1/sessions/create \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "context": {"test": true}}' | python -m json.tool

echo ""
echo "⏹️  متوقف کردن سرور..."
kill $SERVER_PID
