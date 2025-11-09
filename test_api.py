#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 تست API تتراشاپ...")
    
    try:
        # تست سلامت
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ GET /: {response.status_code} - {response.json()}")
        
        # تست سلامت API
        response = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"✅ GET /health: {response.status_code} - {response.json()}")
        
        # تست وضعیت
        response = requests.get(f"{BASE_URL}/api/v1/status")
        print(f"✅ GET /status: {response.status_code} - {response.json()}")
        
        # تست ایجاد سشن
        session_data = {
            "user_id": "test_user_python",
            "context": {"test": True, "language": "python"}
        }
        response = requests.post(
            f"{BASE_URL}/api/v1/sessions/create",
            json=session_data
        )
        result = response.json()
        print(f"✅ POST /sessions/create: {response.status_code} - {result}")
        
        # تست دریافت سشن
        if 'session_id' in result:
            session_id = result['session_id']
            response = requests.get(f"{BASE_URL}/api/v1/sessions/{session_id}")
            print(f"✅ GET /sessions/{{id}}: {response.status_code} - {response.json()}")
        
        print("\n🎉 تمام تست‌ها موفقیت‌آمیز بودند!")
        
    except Exception as e:
        print(f"❌ خطا در تست API: {e}")
        print("⚠️  مطمئن شوید سرور در حال اجرا است: python simple_server.py")

if __name__ == "__main__":
    test_api()
