from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
import sys

class TetrashopAPIHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        print(f"📥 GET request: {self.path}")
        
        if self.path == '/api/health' or self.path == '/api/v1/health':
            self.send_success_response({
                "status": "healthy", 
                "service": "Tetrashop API",
                "timestamp": time.time(),
                "version": "1.0.0"
            })
        elif self.path == '/':
            self.send_success_response({
                "message": "Tetrashop Adaptive System API",
                "endpoints": {
                    "health": "/api/health",
                    "create_session": "POST /api/v1/sessions/create"
                }
            })
        else:
            self.send_error_response(404, "Endpoint not found")
    
    def do_POST(self):
        print(f"📥 POST request: {self.path}")
        content_length = int(self.headers.get('Content-Length', 0))
        
        if self.path == '/api/v1/sessions/create':
            try:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                session_id = f"session_{int(time.time())}_{data.get('user_id', 'anonymous')}"
                
                self.send_success_response({
                    "status": "success",
                    "session_id": session_id,
                    "user_id": data.get('user_id'),
                    "created_at": time.time(),
                    "message": "Session created successfully"
                })
            except Exception as e:
                self.send_error_response(400, f"Invalid JSON: {str(e)}")
        else:
            self.send_error_response(404, "Endpoint not found")
    
    def send_success_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def send_error_response(self, code, message):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"error": message, "code": code}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, TetrashopAPIHandler)
    print(f'🚀 Tetrashop API Server running on http://localhost:{port}')
    print('📊 Available endpoints:')
    print('   GET  /api/health')
    print('   POST /api/v1/sessions/create')
    print('   GET  /')
    print('⏹️  Press Ctrl+C to stop the server')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n🛑 Server stopped')
        httpd.shutdown()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
