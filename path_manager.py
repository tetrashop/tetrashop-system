#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

class PathManager:
    """مدیریت هوشمند مسیرها و ایجاد خودکار پوشه‌ها"""
    
    def __init__(self, base_dir=None):
        self.base_dir = base_dir or os.getcwd()
        self.ensure_directory(self.base_dir)
    
    def ensure_directory(self, path):
        """ایجاد پوشه اگر وجود ندارد"""
        Path(path).mkdir(parents=True, exist_ok=True)
        return path
    
    def get_full_path(self, relative_path):
        """دریافت مسیر کامل و ایجاد پوشه‌های لازم"""
        full_path = os.path.join(self.base_dir, relative_path)
        
        # ایجاد پوشه والد اگر وجود ندارد
        parent_dir = os.path.dirname(full_path)
        self.ensure_directory(parent_dir)
        
        return full_path
    
    def create_file(self, relative_path, content, encoding='utf-8'):
        """ایجاد فایل با مدیریت خودکار مسیر"""
        full_path = self.get_full_path(relative_path)
        
        try:
            with open(full_path, 'w', encoding=encoding) as f:
                f.write(content)
            print(f"✅ فایل ایجاد شد: {full_path}")
            return True
        except Exception as e:
            print(f"❌ خطا در ایجاد فایل {full_path}: {e}")
            return False
    
    def read_file(self, relative_path, encoding='utf-8'):
        """خواندن فایل با مدیریت خطا"""
        full_path = self.get_full_path(relative_path)
        
        try:
            with open(full_path, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            print(f"❌ خطا در خواندن فایل {full_path}: {e}")
            return None

# نمونه جهانی
path_mgr = PathManager()

def create_file_safe(relative_path, content):
    """تابع سریع برای ایجاد فایل"""
    return path_mgr.create_file(relative_path, content)

def get_path(relative_path):
    """دریافت مسیر کامل"""
    return path_mgr.get_full_path(relative_path)

# تست سیستم
if __name__ == "__main__":
    print("🧪 تست سیستم مدیریت مسیرها...")
    
    # تست ایجاد پوشه‌ها
    test_path = get_path("test/sub1/sub2/test_file.txt")
    print(f"📁 مسیر تست: {test_path}")
    
    # تست ایجاد فایل
    success = create_file_safe("test/sub1/sub2/test.txt", "این یک تست است!")
    print(f"🎯 نتیجه تست: {'موفق' if success else 'ناموفق'}")
