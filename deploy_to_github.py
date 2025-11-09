#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

def run_command(command, description):
    """اجرای دستور و مدیریت خطا"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description}")
            return True
        else:
            print(f"❌ {description}: {result.stderr}")
            return False
    except Exception as e:
        print(f"💥 {description}: {e}")
        return False

def setup_github_repo():
    """تنظیمات کامل برای گیت‌هاب"""
    
    print("🚀 راه‌اندازی گیت‌هاب برای تتراشاپ...")
    
    # 1. بررسی وجود گیت
    if not run_command("git status", "بررسی وضعیت گیت"):
        print("❌ پروژه گیت‌ای نیست! ابتدا git init کنید")
        return False
    
    # 2. دریافت اطلاعات کاربر
    github_username = input("👤 نام کاربری گیت‌هاب خود را وارد کنید: ").strip()
    repo_name = input("📁 نام ریپازیتوری (پیشنهاد: tetrashop-system): ").strip() or "tetrashop-system"
    
    # 3. تنظیم remote
    print(f"🔗 تنظیم remote به آدرس: https://github.com/{github_username}/{repo_name}.git")
    
    # حذف remoteهای قدیمی
    run_command("git remote remove origin", "حذف remoteهای قدیمی")
    
    # اضافه کردن remote جدید
    remote_url = f"https://github.com/{github_username}/{repo_name}.git"
    if not run_command(f"git remote add origin {remote_url}", "اضافه کردن remote جدید"):
        return False
    
    # 4. push کردن
    print(f"📤 در حال push کردن به {remote_url}...")
    
    if run_command("git push -u origin main", "Push کردن کدها"):
        print(f"🎉 موفقیت! پروژه در آدرس زیر منتشر شد:")
        print(f"   https://github.com/{github_username}/{repo_name}")
        return True
    else:
        print("""
⚠️  push ناموفق بود. احتمالات:
   1. ریپازیتوری در گیت‌هاب وجود ندارد
   2. مشکل احراز هویت
   3. نام کاربری/ریپو اشتباه

💡 راه‌حل‌ها:
   - از طریق مرورگر به github.com بروید و ریپوی '{repo_name}' را ایجاد کنید
   - سپس دوباره این اسکریپت را اجرا کنید
   - یا از دستور زیر استفاده کنید:
        git push -u origin main
        """)
        return False

if __name__ == "__main__":
    setup_github_repo()
