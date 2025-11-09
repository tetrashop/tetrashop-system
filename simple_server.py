from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time

class SimpleAPIHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        print(f"GET request for {self.path}")
        
        if self.path == '/api/health' or self.path == '/api/v1/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "service": "Tetrashop API",
                "timestamp": time.time()
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "message": "Tetrashop API is running!",
                "endpoints": ["/api/health", "/api/v1/sessions/create"]
            }
            self.wfile.write(json.dumps(response).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())
    
    def do_POST(self):
        if self.path == '/api/v1/sessions/create':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "success",
                "session_id": f"session_{int(time.time())}",
                "message": "Session created"
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())

def run_server():
    server = HTTPServer(('localhost', 8000), SimpleAPIHandler)
    print('🚀 Server running on http://localhost:8000')
    server.serve_forever()

if __name__ == '__main__':
    run_server()
