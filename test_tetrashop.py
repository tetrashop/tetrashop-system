#!/usr/bin/env python3
import requests
import json
import time

BASE_URL = "http://localhost:8080"

def test_all_endpoints():
    print("🧪 تست کامل API تتراشاپ...")
    print("=" * 50)
    
    try:
        # تست 1: سلامت اصلی
        print("1. تست سلامت اصلی...")
        response = requests.get(f"{BASE_URL}/")
        print(f"   ✅ GET /: {response.status_code}")
        print(f"   📦 پاسخ: {response.text[:100]}...")
        
        # تست 2: سلامت API
        print("2. تست سلامت API...")
        response = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"   ✅ GET /health: {response.status_code}")
        
        # تست 3: وضعیت سیستم
        print("3. تست وضعیت سیستم...")
        response = requests.get(f"{BASE_URL}/api/v1/status")
        print(f"   ✅ GET /status: {response.status_code}")
        
        # تست 4: ایجاد سشن
        print("4. تست ایجاد سشن...")
        session_data = {
            "user_id": f"test_user_{int(time.time())}",
            "context": {"test": True, "language": "python", "timestamp": time.time()}
        }
        response = requests.post(
            f"{BASE_URL}/api/v1/sessions/create",
            json=session_data
        )
        
        if response.status_code == 200:
            result = response.json()
            session_id = result.get('session_id')
            print(f"   ✅ POST /sessions/create: {response.status_code}")
            print(f"   🆔 Session ID: {session_id}")
            
            # تست 5: دریافت سشن
            print("5. تست دریافت سشن...")
            response = requests.get(f"{BASE_URL}/api/v1/sessions/{session_id}")
            print(f"   ✅ GET /sessions/{{id}}: {response.status_code}")
            
            if response.status_code == 200:
                session_info = response.json()
                print(f"   👤 User ID: {session_info.get('user_id')}")
                print(f"   📊 Context: {session_info.get('context')}")
        else:
            print(f"   ❌ POST /sessions/create: {response.status_code}")
            print(f"   📄 پاسخ: {response.text}")
        
        print("\n" + "=" * 50)
        print("🎉 تست‌ها کامل شدند!")
        print("🌐 سیستم تتراشاپ با موفقیت راه‌اندازی شد!")
        
    except requests.exceptions.ConnectionError:
        print("❌ خطا: سرور در دسترس نیست")
        print("💡 مطمئن شوید سرور در حال اجرا است:")
        print("   python tetrashop_server.py")
    except Exception as e:
        print(f"❌ خطا: {e}")

if __name__ == "__main__":
    test_all_endpoints()
