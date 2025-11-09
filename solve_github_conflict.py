#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys

def run_command(cmd, description):
    print(f"🔄 {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description}: {result.stderr}")
        return False

def main():
    print("🔧 حل مشکل تداخل گیت‌هاب...")
    
    print("\n📋 گزینه‌های موجود:")
    print("1. ادغام تغییرات (توصیه شده)")
    print("2. بازنویسی ریپوی ریموت")
    print("3. ایجاد branch جدید")
    
    choice = input("\n🎯 گزینه مورد نظر را انتخاب کنید (1/2/3): ").strip()
    
    if choice == "1":
        # ادغام تغییرات
        if run_command("git pull origin main --allow-unrelated-histories", "دریافت تغییرات از ریموت"):
            if run_command("git push -u origin main", "Push کردن تغییرات"):
                print("🎉 موفقیت! تغییرات ادغام و push شدند.")
            else:
                print("❌ خطا در push. ممکن است نیاز به resolve conflict داشته باشید.")
    elif choice == "2":
        # بازنویسی
        confirm = input("⚠️  آیا مطمئن هستید؟ این کار تاریخچه ریموت را بازنویسی می‌کند (y/n): ")
        if confirm.lower() == 'y':
            if run_command("git push -f origin main", "بازنویسی ریپوی ریموت"):
                print("🎉 ریپوی ریموت با موفقیت بازنویسی شد.")
    elif choice == "3":
        # ایجاد branch جدید
        branch_name = input("نام branch جدید (پیشنهاد: tetrashop-main): ").strip() or "tetrashop-main"
        if run_command(f"git checkout -b {branch_name}", f"ایجاد branch {branch_name}"):
            if run_command(f"git push -u origin {branch_name}", f"Push کردن {branch_name}"):
                print(f"🎉 branch {branch_name} با موفقیت ایجاد و push شد.")
    else:
        print("❌ گزینه نامعتبر")

if __name__ == "__main__":
    main()
