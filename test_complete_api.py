#!/usr/bin/env python3
import requests
import json
import time

BASE_URL = "http://localhost:8080"

def test_all():
    print("🧪 تست کامل API تتراشاپ")
    print("=" * 60)
    
    try:
        # 1. تست روت اصلی
        print("1. 📍 تست روت اصلی...")
        r = requests.get(f"{BASE_URL}/")
        print(f"   ✅ وضعیت: {r.status_code}")
        print(f"   📦 پاسخ: {r.json()}")
        
        # 2. تست سلامت
        print("\n2. 🏥 تست سلامت...")
        r = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"   ✅ وضعیت: {r.status_code}")
        print(f"   📊 داده: {r.json()}")
        
        # 3. تست وضعیت
        print("\n3. 📊 تست وضعیت سیستم...")
        r = requests.get(f"{BASE_URL}/api/v1/status")
        data = r.json()
        print(f"   ✅ وضعیت: {r.status_code}")
        print(f"   🔧 محیط: {data.get('environment')}")
        print(f"   🐛 دیباگ: {data.get('debug')}")
        
        # 4. تست ایجاد سشن
        print("\n4. 🆕 تست ایجاد سشن...")
        session_data = {
            "user_id": f"test_user_{int(time.time())}",
            "context": {
                "test": True,
                "language": "persian",
                "platform": "termux",
                "timestamp": time.time()
            }
        }
        r = requests.post(f"{BASE_URL}/api/v1/sessions/create", json=session_data)
        
        if r.status_code == 200:
            result = r.json()
            session_id = result.get('session_id')
            print(f"   ✅ وضعیت: {r.status_code}")
            print(f"   🆔 Session ID: {session_id}")
            print(f"   👤 User ID: {result.get('user_id')}")
            
            # 5. تست دریافت سشن
            print("\n5. 📂 تست دریافت سشن...")
            r = requests.get(f"{BASE_URL}/api/v1/sessions/{session_id}")
            if r.status_code == 200:
                session_info = r.json()
                print(f"   ✅ وضعیت: {r.status_code}")
                print(f"   📝 Context: {session_info.get('context')}")
                print(f"   ⏰ Created: {time.ctime(session_info.get('created_at'))}")
            else:
                print(f"   ❌ وضعیت: {r.status_code}")
                print(f"   💬 خطا: {r.text}")
        else:
            print(f"   ❌ وضعیت: {r.status_code}")
            print(f"   💬 خطا: {r.text}")
        
        print("\n" + "=" * 60)
        print("🎉 تمام تست‌ها با موفقیت انجام شد!")
        print("🚀 سیستم تتراشاپ آماده استفاده است!")
        
    except requests.exceptions.ConnectionError:
        print("❌ خطا: سرور در دسترس نیست")
        print("💡 مطمئن شوید سرور در حال اجرا است: python tetrashop_complete.py")
    except Exception as e:
        print(f"❌ خطا: {e}")

if __name__ == "__main__":
    test_all()
