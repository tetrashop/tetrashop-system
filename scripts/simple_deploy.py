#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time

def run_setup():
    print("🚀 شروع دیپلوی تتراشاپ...")
    
    # بررسی وجود فایل‌های لازم
    required_files = ['requirements.txt', 'setup_complete_standalone.py']
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ فایل {file} یافت نشد!")
            return False
    
    # نصب وابستگی‌ها
    print("📦 نصب وابستگی‌ها...")
    os.system("pip install -r requirements.txt")
    
    # اجرای راه‌اندازی
    print("🔧 راه‌اندازی سیستم...")
    os.system("python setup_complete_standalone.py")
    
    print("🎉 دیپلوی کامل شد!")
    print("\n📋 دستورات:")
    print("   python main.py")
    print("   یا")
    print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    
    return True

if __name__ == "__main__":
    success = run_setup()
    sys.exit(0 if success else 1)
