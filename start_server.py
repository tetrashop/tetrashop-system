#!/usr/bin/env python3
import subprocess
import sys
import os

def check_port(port=8000):
    """بررسی آیا پورت در حال استفاده است"""
    try:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    except:
        return False

def main():
    print("🚀 راه‌اندازی سرور تتراشاپ...")
    
    # بررسی پورت
    if check_port():
        print("⚠️  پورت 8000 در حال استفاده است. ممکن است سرور قبلاً در حال اجرا باشد.")
        response = input("آیا می‌خواهید ادامه دهید؟ (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # نصب وابستگی‌ها
    print("📦 بررسی وابستگی‌ها...")
    try:
        import fastapi
        import uvicorn
        print("✅ وابستگی‌ها نصب هستند")
    except ImportError:
        print("📥 در حال نصب وابستگی‌ها...")
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "pydantic"])
    
    # راه‌اندازی سرور
    print("🌐 شروع سرور در http://localhost:8000")
    print("📚 مستندات: http://localhost:8000/docs")
    print("🛑 برای توقف: Ctrl+C")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n🛑 سرور متوقف شد")
    except Exception as e:
        print(f"❌ خطا: {e}")

if __name__ == "__main__":
    main()
