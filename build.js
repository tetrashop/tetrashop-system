const fs = require('fs');
const path = require('path');

console.log('🚀 ساختن پروژه تتراشاپ برای Vercel...');

// ایجاد پوشه dist
const distDir = path.join(__dirname, 'dist');
if (!fs.existsSync(distDir)) {
  fs.mkdirSync(distDir, { recursive: true });
}

// کپی index.html
const indexSource = path.join(__dirname, 'index.html');
const indexDest = path.join(distDir, 'index.html');

if (fs.existsSync(indexSource)) {
  fs.copyFileSync(indexSource, indexDest);
  console.log('✅ index.html کپی شد');
} else {
  // ایجاد index.html پیش‌فرض
  const defaultHtml = `
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تتراشاپ - سیستم هوشمند</title>
    <style>
        body {
            font-family: 'Vazirmatn', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 50px;
        }
        h1 { font-size: 3rem; margin-bottom: 20px; }
        p { font-size: 1.2rem; opacity: 0.9; }
        .status { 
            background: #10b981; 
            padding: 10px 20px; 
            border-radius: 20px; 
            display: inline-block;
            margin-top: 20px;
        }
    </style>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css">
</head>
<body>
    <h1>🚀 تتراشاپ</h1>
    <p>سیستم هوشمند مدیریت مخازن - مستقر شده روی Vercel</p>
    <div class="status">✅ سیستم فعال</div>
    
    <script>
        // تست API
        fetch('/api/')
            .then(r => r.json())
            .then(data => {
                console.log('API Response:', data);
            })
            .catch(err => {
                console.log('API Error:', err);
            });
    </script>
</body>
</html>`;
  
  fs.writeFileSync(indexDest, defaultHtml);
  console.log('✅ index.html پیش‌فرض ایجاد شد');
}

console.log('🎯 ساخت کامل شد!');
