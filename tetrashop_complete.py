#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
import os
import sys

class TetrashopAPIHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        print(f"📥 GET {self.path}")
        
        # روت اصلی
        if self.path == '/':
            self.send_json_response(200, {
                "message": "🎉 تتراشاپ فعال است!",
                "status": "active",
                "version": "1.0.0",
                "endpoints": {
                    "health": "/api/v1/health",
                    "status": "/api/v1/status", 
                    "create_session": "/api/v1/sessions/create",
                    "get_session": "/api/v1/sessions/{id}"
                }
            })
        
        # سلامت سیستم
        elif self.path == '/api/v1/health':
            self.send_json_response(200, {
                "status": "healthy",
                "timestamp": time.time(),
                "environment": "production"
            })
        
        # وضعیت سیستم
        elif self.path == '/api/v1/status':
            self.send_json_response(200, {
                "status": "فعال",
                "environment": "development",
                "debug": True,
                "uptime": time.time(),
                "version": "1.0.0"
            })
        
        # دریافت اطلاعات سشن
        elif self.path.startswith('/api/v1/sessions/'):
            session_id = self.path.split('/')[-1]
            if session_id != 'create':  # جلوگیری از تداخل با POST
                self.get_session(session_id)
            else:
                self.send_error(404, "Use POST method for creation")
        
        else:
            self.send_error(404, f"Endpoint not found: {self.path}")
    
    def do_POST(self):
        print(f"📥 POST {self.path}")
        
        # ایجاد سشن جدید
        if self.path == '/api/v1/sessions/create':
            self.create_session()
        else:
            self.send_error(404, f"Endpoint not found: {self.path}")
    
    def send_json_response(self, code, data):
        """ارسال پاسخ JSON"""
        self.send_response(code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
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
                "status": "active",
                "metadata": {
                    "ip": self.client_address[0],
                    "user_agent": self.headers.get('User-Agent', 'unknown')
                }
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
                "timestamp": time.time(),
                "message": "سشن با موفقیت ایجاد شد"
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
                self.send_json_response(404, {
                    "error": "Session not found",
                    "session_id": session_id
                })
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
        """لاگ‌های زیبا"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {format % args}")

def run_server(port=8080):
    print("🚀 شروع سرور کامل تتراشاپ...")
    print(f"🌐 آدرس: http://localhost:{port}")
    print("📋 Endpoint های موجود:")
    print("   GET  /")
    print("   GET  /api/v1/health")
    print("   GET  /api/v1/status")
    print("   POST /api/v1/sessions/create")
    print("   GET  /api/v1/sessions/{session_id}")
    print("🛑 برای توقف: Ctrl+C")
    print("-" * 50)
    
    try:
        server = HTTPServer(('0.0.0.0', port), TetrashopAPIHandler)
        print(f"✅ سرور روی پورت {port} راه‌اندازی شد")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 سرور متوقف شد")
    except Exception as e:
        print(f"❌ خطا در راه‌اندازی سرور: {e}")

if __name__ == "__main__":
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except:
            pass
    
    run_server(port)
