from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
import json
import time

def handler(request, response):
    response.status(HTTPStatus.OK)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    
    data = {
        "status": "healthy",
        "timestamp": time.time(),
        "message": "✅ سیستم تتراشاپ سالم است"
    }
    
    response.send(json.dumps(data, ensure_ascii=False))
