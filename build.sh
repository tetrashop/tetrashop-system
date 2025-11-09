#!/bin/bash
echo "🔨 ساخت پروژه تتراشاپ برای Vercel..."

# ایجاد دایرکتوری‌های لازم
mkdir -p api

# کپی فایل‌های پایتون
cp *.py api/ 2>/dev/null || true

# ایجاد فایل‌های ضروری
if [ ! -f "package.json" ]; then
    echo '{"name": "tetrashop", "version": "1.0.0"}' > package.json
fi

echo "✅ ساخت کامل شد"
