#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
from pathlib import Path

class StableHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        paths = {
            '/': {'message': '🚀 تتراشاپ فعال!', 'status': 'active'},
            '/health': {'status': 'healthy', 'timestamp': time.time()},
            '/status': {'status': 'فعال', 'environment': 'production'}
        }
        
        if self.path in paths:
            self.send_json(200, paths[self.path])
        else:
            self.send_json(404, {'error': 'پیدا نشد'})
    
    def do_POST(self):
        if self.path == '/sessions/create':
            self.create_session()
        else:
            self.send_json(404, {'error': 'پیدا نشد'})
    
    def send_json(self, code, data):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    def create_session(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(length).decode())
            
            user_id = data.get('user_id', 'guest')
            session_id = f"session_{int(time.time())}_{user_id}"
            
            # ایجاد خودکار پوشه
            Path("data/sessions").mkdir(parents=True, exist_ok=True)
            
            session_data = {
                "session_id": session_id,
                "user_id": user_id,
                "created_at": time.time()
            }
            
            with open(f"data/sessions/{session_id}.json", "w", encoding="utf-8") as f:
                json.dump(session_data, f, ensure_ascii=False)
            
            self.send_json(200, {
                "session_id": session_id,
                "status": "created"
            })
        except:
            self.send_json(400, {'error': 'داده نامعتبر'})

print("🌐 سرور پایدار راه‌اندازی شد: http://localhost:8080")
HTTPServer(('0.0.0.0', 8080), StableHandler).serve_forever()
