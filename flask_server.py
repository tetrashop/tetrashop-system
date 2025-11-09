from flask import Flask, request, jsonify
import json
import time
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "✅ تتراشاپ با Flask فعال است!",
        "status": "active",
        "version": "1.0.0"
    })

@app.route('/api/v1/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": time.time()
    })

@app.route('/api/v1/sessions/create', methods=['POST'])
def create_session():
    data = request.get_json()
    user_id = data.get('user_id', 'unknown')
    context = data.get('context', {})
    
    session_id = f"session_{int(time.time())}_{user_id}"
    
    session_data = {
        "session_id": session_id,
        "user_id": user_id,
        "context": context,
        "created_at": time.time(),
        "status": "active"
    }
    
    os.makedirs("data/sessions", exist_ok=True)
    with open(f"data/sessions/{session_id}.json", "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)
    
    return jsonify({
        "session_id": session_id,
        "status": "created",
        "timestamp": time.time()
    })

if __name__ == '__main__':
    print("🚀 سرور Flask در حال راه‌اندازی...")
    print("🌐 آدرس: http://localhost:8000")
    app.run(host='0.0.0.0', port=8000, debug=False)
