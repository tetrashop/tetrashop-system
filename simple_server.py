#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
import os

class TetrashopHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        print(f"📥 GET request: {self.path}")
        
        if self.path == '/':
            self.send_json_response(200, {
                "message": "✅ تتراشاپ فعال است!",
                "status": "active",
                "version": "1.0.0"
            })
            
        elif self.path == '/api/v1/health':
            self.send_json_response(200, {
                "status": "healthy",
                "timestamp": time.time()
            })
            
        elif self.path == '/api/v1/status':
            self.send_json_response(200, {
                "status": "فعال",
                "environment": "development",
                "debug": True
            })
            
        elif self.path.startswith('/api/v1/sessions/'):
            session_id = self.path.split('/')[-1]
            self.get_session(session_id)
            
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        print(f"📥 POST request: {self.path}")
        
        if self.path == '/api/v1/sessions/create':
            self.create_session()
        else:
            self.send_error(404, "Not Found")
    
    def send_json_response(self, code, data):
        """ارسال پاسخ JSON"""
        self.send_response(code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.wfile.write(response)
    
    def create_session(self):
        """ایجاد سشن جدید"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            user_id = data.get('user_id', 'unknown')
            context = data.get('context', {})
            
            session_id = f"session_{int(time.time())}_{user_id}"
            
            # ذخیره سشن
            session_data = {
                "session_id": session_id,
                "user_id": user_id,
                "context": context,
                "created_at": time.time(),
                "status": "active"
            }
            
            # ایجاد دایرکتوری
            os.makedirs("data/sessions", exist_ok=True)
            
            # ذخیره در فایل
            with open(f"data/sessions/{session_id}.json", "w", encoding="utf-8") as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            
            self.send_json_response(200, {
                "session_id": session_id,
                "status": "created",
                "user_id": user_id,
                "timestamp": time.time()
            })
            
            print(f"✅ سشن ایجاد شد: {session_id}")
            
        except Exception as e:
            self.send_json_response(400, {"error": str(e)})
            print(f"❌ خطا در ایجاد سشن: {e}")
    
    def get_session(self, session_id):
        """دریافت اطلاعات سشن"""
        try:
            session_file = f"data/sessions/{session_id}.json"
            
            if not os.path.exists(session_file):
                self.send_json_response(404, {"error": "Session not found"})
                return
            
            with open(session_file, "r", encoding="utf-8") as f:
                session_data = json.load(f)
            
            self.send_json_response(200, session_data)
            print(f"✅ اطلاعات سشن ارسال شد: {session_id}")
            
        except Exception as e:
            self.send_json_response(500, {"error": str(e)})
            print(f"❌ خطا در دریافت سشن: {e}")
    
    def do_OPTIONS(self):
        """مدیریت درخواست‌های OPTIONS برای CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """غیرفعال کردن لاگ‌های پیش‌فرض"""
        pass

def run_server():
    print("🚀 شروع سرور تتراشاپ...")
    print("🌐 آدرس: http://localhost:8000")
    print("📋 Endpoint های موجود:")
    print("   GET  /")
    print("   GET  /api/v1/health")
    print("   GET  /api/v1/status")
    print("   POST /api/v1/sessions/create")
    print("   GET  /api/v1/sessions/{session_id}")
    print("🛑 برای توقف: Ctrl+C")
    print("-" * 50)
    
    try:
        server = HTTPServer(('0.0.0.0', 8000), TetrashopHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 سرور متوقف شد")
    except Exception as e:
        print(f"❌ خطا در راه‌اندازی سرور: {e}")

if __name__ == "__main__":
    run_server()
