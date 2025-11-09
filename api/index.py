from http.server import BaseHTTPRequestHandler
import json

def handler(request, response):
    return response.json({
        "message": "🚀 تتراشاپ - سیستم هوشمند مدیریت مخازن",
        "status": "active",
        "version": "1.0.0",
        "platform": "Vercel",
        "endpoints": {
            "GET /api/health": "بررسی سلامت سیستم",
            "POST /api/session/create": "ایجاد سشن جدید",
            "GET /api/": "اطلاعات سیستم"
        },
        "repository": "https://github.com/tetrashop/tetrashop-system"
    })
