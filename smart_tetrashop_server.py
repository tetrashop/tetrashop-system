#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
from pathlib import Path
import sys
import socket

class SmartTetrashopHandler(BaseHTTPRequestHandler):
    """سرور هوشمند با مدیریت خودکار خطاها"""
    
    def do_GET(self):
        try:
            if self.path == '/':
                self._send_json(200, {
                    "message": "🚀 تتراشاپ هوشمند فعال!", 
                    "status": "active",
                    "version": "3.0.0"
                })
            
            elif self.path == '/health':
                self._send_json(200, {
                    "status": "excellent", 
                    "timestamp": time.time()
                })
            
            elif self.path == '/status':
                self._send_json(200, {
                    "status": "فعال و پایدار",
                    "environment": "production", 
                    "performance": "عالی"
                })
            
            elif self.path.startswith('/session/'):
                session_id = self.path.split('/')[-1]
                if session_id:
                    self._get_session(session_id)
                else:
                    self._send_json(400, {"error": "شناسه سشن لازم است"})
            else:
                self._send_json(404, {"error": "مسیر پیدا نشد"})
                
        except Exception as e:
            self._send_json(500, {"error": "خطای داخلی", "details": str(e)})
    
    def do_POST(self):
        try:
            if self.path == '/session/create':
                self._create_session()
            else:
                self._send_json(404, {"error": "مسیر پیدا نشد"})
        except Exception as e:
            self._send_json(500, {"error": "خطای داخلی", "details": str(e)})
    
    def _send_json(self, code, data):
        """ارسال پاسخ JSON"""
        self.send_response(code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    def _create_session(self):
        """ایجاد سشن جدید"""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self._send_json(400, {"error": "داده‌ای ارسال نشده"})
            return
        
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        user_id = data.get('user_id', 'مهمان')
        context = data.get('context', {})
        
        session_id = f"smart_session_{int(time.time())}_{user_id}"
        
        # ایجاد خودکار پوشه‌ها
        Path("data/sessions").mkdir(parents=True, exist_ok=True)
        
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "context": context,
            "created_at": time.time(),
            "status": "فعال",
            "server": "هوشمند 3.0"
        }
        
        # ذخیره فایل
        with open(f"data/sessions/{session_id}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        self._send_json(200, {
            "session_id": session_id,
            "status": "ایجاد شد",
            "message": "سشن با موفقیت ساخته شد",
            "timestamp": time.time()
        })
    
    def _get_session(self, session_id):
        """دریافت اطلاعات سشن"""
        session_file = f"data/sessions/{session_id}.json"
        
        if not Path(session_file).exists():
            self._send_json(404, {"error": "سشن پیدا نشد", "session_id": session_id})
            return
        
        with open(session_file, "r", encoding="utf-8") as f:
            session_data = json.load(f)
        
        self._send_json(200, session_data)
    
    def log_message(self, format, *args):
        """لاگ‌های تمیز"""
        print(f"[{time.strftime('%H:%M:%S')}] 📡 {format % args}")

def find_available_port(start_port=8080, max_attempts=10):
    """پیدا کردن پورت آزاد"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                return port
        except OSError:
            continue
    return start_port  # اگر همه پورت‌ها заняت بودند، از پورت شروع استفاده کن

def run_smart_server():
    """راه‌اندازی سرور هوشمند"""
    port = find_available_port(8080)
    
    print(f"🚀 سرور تتراشاپ هوشمند راه‌اندازی شد!")
    print(f"🌐 آدرس: http://localhost:{port}")
    print("📊 وضعیت: فعال | خطا: هیچ")
    print("🛑 برای توقف: Ctrl+C")
    print("-" * 50)
    
    try:
        server = HTTPServer(('0.0.0.0', port), SmartTetrashopHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 سرور متوقف شد")
    except Exception as e:
        print(f"❌ خطا: {e}")

if __name__ == "__main__":
    run_smart_server()
