from http.server import BaseHTTPRequestHandler
import json
import time

def handler(request, response):
    return response.json({
        "status": "healthy",
        "timestamp": time.time(),
        "platform": "Vercel",
        "message": "✅ سیستم تتراشاپ سالم است"
    })
