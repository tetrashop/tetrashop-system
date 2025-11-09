from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
import json

def handler(request, response):
    try:
        response.status(HTTPStatus.OK)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        response.headers['Access-Control-Allow-Origin'] = '*'
        
        data = {
            "message": "🚀 تتراشاپ API فعال است!",
            "status": "active",
            "version": "1.0.0",
            "endpoints": [
                "/api/health",
                "/api/session"
            ]
        }
        
        response.send(json.dumps(data, ensure_ascii=False))
        
    except Exception as e:
        response.status(HTTPStatus.INTERNAL_SERVER_ERROR)
        response.send(json.dumps({"error": str(e)}))
