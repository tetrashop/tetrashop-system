from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
import json
import time

def handler(request, response):
    try:
        if request.method == 'POST':
            # شبیه‌سازی دریافت داده
            user_id = "test_user"
            
            data = {
                "session_id": f"session_{int(time.time())}",
                "user_id": user_id,
                "created_at": time.time(),
                "status": "created",
                "message": "سشن با موفقیت ایجاد شد"
            }
            
            response.status(HTTPStatus.OK)
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            response.send(json.dumps(data, ensure_ascii=False))
            
        else:
            response.status(HTTPStatus.METHOD_NOT_ALLOWED)
            response.send(json.dumps({"error": "فقط متد POST مجاز است"}))
            
    except Exception as e:
        response.status(HTTPStatus.BAD_REQUEST)
        response.send(json.dumps({"error": str(e)}))
