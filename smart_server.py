#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
import socket
import sys

class SmartTetrashopHandler(BaseHTTPRequestHandler):
    """سرور هوشمند تتراشاپ"""
    
    def do_GET(self):
        if self.path == '/':
            self._send_json(200, {
                "message": "🚀 تتراشاپ هوشمند فعال!", 
                "status": "active",
                "version": "4.0.0",
                "github": "https://github.com/tetrashop/tetrashop-system"
            })
        elif self.path == '/health':
            self._send_json(200, {"status": "healthy", "timestamp": time.time()})
        elif self.path == '/status':
            self._send_json(200, {"status": "فعال", "environment": "production"})
        elif self.path.startswith('/session/'):
            session_id = self.path.split('/')[-1]
            if session_id:
                self._get_session(session_id)
        else:
            self._send_json(404, {"error": "مسیر پیدا نشد"})
    
    def do_POST(self):
        if self.path == '/session/create':
            self._create_session()
        else:
            self._send_json(404, {"error": "مسیر پیدا نشد"})
    
    def _send_json(self, code, data):
        self.send_response(code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    def _create_session(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(length).decode())
            
            user_id = data.get('user_id', 'مهمان')
            session_id = f"session_{int(time.time())}_{user_id}"
            
            import os
            os.makedirs("data/sessions", exist_ok=True)
            
            session_data = {
                "session_id": session_id,
                "user_id": user_id,
                "created_at": time.time(),
                "status": "فعال"
            }
            
            with open(f"data/sessions/{session_id}.json", "w", encoding="utf-8") as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            
            self._send_json(200, {
                "session_id": session_id,
                "status": "ایجاد شد",
                "message": "سشن با موفقیت ساخته شد"
            })
        except Exception as e:
            self._send_json(400, {"error": str(e)})
    
    def _get_session(self, session_id):
        import os
        session_file = f"data/sessions/{session_id}.json"
        
        if not os.path.exists(session_file):
            self._send_json(404, {"error": "سشن پیدا نشد"})
            return
        
        with open(session_file, "r", encoding="utf-8") as f:
            session_data = json.load(f)
        
        self._send_json(200, session_data)
    
    def log_message(self, format, *args):
        print(f"[{time.strftime('%H:%M:%S')}] {format % args}")

def find_available_port(start_port=8000):
    """پیدا کردن پورت آزاد"""
    for port in range(start_port, start_port + 10):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                return port
        except OSError:
            continue
    return start_port

def main():
    port = find_available_port(8000)
    
    print(f"🚀 سرور تتراشاپ هوشمند راه‌اندازی شد!")
    print(f"🌐 آدرس: http://localhost:{port}")
    print(f"📚 مستندات: https://github.com/tetrashop/tetrashop-system")
    print("🛑 برای توقف: Ctrl+C")
    print("-" * 50)
    
    try:
        server = HTTPServer(('0.0.0.0', port), SmartTetrashopHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 سرور متوقف شد")

if __name__ == "__main__":
    main()
