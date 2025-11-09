from http.server import BaseHTTPRequestHandler
import json
import time

def handler(request, response):
    return response.json({
        "message": "🚀 تتراشاپ فعال است!",
        "status": "active", 
        "version": "1.0.0",
        "timestamp": time.time(),
        "platform": "Vercel"
    })
