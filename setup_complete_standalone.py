#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time

class TetrashopSetup:
    """سیستم راه‌اندازی کامل تتراشاپ"""
    
    def __init__(self):
        self.setup_log = []
        self.start_time = time.time()
    
    def log(self, message):
        """ثبت لاگ"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.setup_log.append(log_entry)
        print(log_entry)
    
    def run_command(self, command, description):
        """اجرای دستور"""
        self.log(f"🔄 {description}...")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"✅ {description} - موفق")
                return True
            else:
                self.log(f"⚠️ {description} - هشدار: {result.stderr}")
                return True  # ادامه دهد حتی با خطا
        except Exception as e:
            self.log(f"⚠️ {description} - هشدار: {e}")
            return True
    
    def install_dependencies(self):
        """نصب وابستگی‌ها"""
        self.log("📦 نصب وابستگی‌های پایتون...")
        
        commands = [
            "pip install --upgrade pip",
            "pip install -r requirements.txt",
            "pip install fastapi uvicorn pydantic"
        ]
        
        for cmd in commands:
            self.run_command(cmd, "نصب بسته‌ها")
    
    def create_directory_structure(self):
        """ایجاد ساختار دایرکتوری"""
        self.log("📁 ایجاد ساختار دایرکتوری...")
        
        directories = [
            'data/sessions',
            'data/knowledge',
            'logs/api',
            'logs/deployment',
            'config',
            'scripts',
            'monitoring'
        ]
        
        for dir_path in directories:
            os.makedirs(dir_path, exist_ok=True)
            self.log(f"   📂 ایجاد {dir_path}")
    
    def create_config_files(self):
        """ایجاد فایل‌های کانفیگ"""
        self.log("⚙️ ایجاد فایل‌های پیکربندی...")
        
        # فایل اصلی کانفیگ
        config_content = '''
import os

class Config:
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # API Settings
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'tetrashop-dev-key')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./data/tetrashop.db')
    
    # URLs
    BASE_URL = f"http://{API_HOST}:{API_PORT}" if ENVIRONMENT == 'development' else 'https://tetrashop.com'

config = Config()
'''
        
        with open('config/__init__.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        # فایل environment
        env_content = '''
# تنظیمات محیط
ENVIRONMENT=development
DEBUG=True

# دیتابیس
DATABASE_URL=sqlite:///./data/tetrashop.db

# امنیت
SECRET_KEY=your-secret-key-here

# API
API_HOST=0.0.0.0
API_PORT=8000
'''
        
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
    
    def create_main_app(self):
        """ایجاد اپلیکیشن اصلی FastAPI"""
        self.log("🚀 ایجاد اپلیکیشن FastAPI...")
        
        app_content = '''
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from config import config
import time
import json
import os

app = FastAPI(
    title="Tetrashop API",
    description="سیستم هوشمند تتراشاپ",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# مدل‌های داده
class SessionCreate(BaseModel):
    user_id: str
    context: dict = {}

class SessionResponse(BaseModel):
    session_id: str
    status: str
    created_at: float

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: float

# routes
@app.get("/")
async def root():
    return {
        "message": "خوش آمدید به تتراشاپ! 🚀",
        "version": "1.0.0",
        "status": "فعال"
    }

@app.get("/api/v1/health")
async def health_check():
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=time.time()
    )

@app.get("/api/v1/status")
async def status():
    return {
        "status": "فعال",
        "environment": config.ENVIRONMENT,
        "debug": config.DEBUG
    }

@app.post("/api/v1/sessions/create")
async def create_session(session: SessionCreate):
    session_id = f"session_{int(time.time())}_{session.user_id}"
    
    # ذخیره سشن
    session_data = {
        "session_id": session_id,
        "user_id": session.user_id,
        "context": session.context,
        "created_at": time.time(),
        "status": "active"
    }
    
    # ذخیره در فایل (در حالت واقعی از دیتابیس استفاده کنید)
    os.makedirs("data/sessions", exist_ok=True)
    with open(f"data/sessions/{session_id}.json", "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False)
    
    return SessionResponse(
        session_id=session_id,
        status="created",
        created_at=time.time()
    )

@app.get("/api/v1/sessions/{session_id}")
async def get_session(session_id: str):
    session_file = f"data/sessions/{session_id}.json"
    
    if not os.path.exists(session_file):
        raise HTTPException(status_code=404, detail="Session not found")
    
    with open(session_file, "r", encoding="utf-8") as f:
        session_data = json.load(f)
    
    return session_data

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=config.DEBUG
    )
'''
        
        with open('main.py', 'w', encoding='utf-8') as f:
            f.write(app_content)
    
    def setup_complete(self):
        """تکمیل راه‌اندازی"""
        end_time = time.time()
        duration = end_time - self.start_time
        
        self.log("🎉 راه‌اندازی تتراشاپ با موفقیت کامل شد!")
        self.log(f"⏱️ زمان اجرا: {duration:.2f} ثانیه")
        
        # نمایش اطلاعات دسترسی
        print("\n" + "="*50)
        print("🚀 تتراشاپ آماده است!")
        print("="*50)
        print("📊 اطلاعات دسترسی:")
        print("   🌐 آدرس API: http://localhost:8000")
        print("   🔧 وضعیت سیستم: http://localhost:8000/api/v1/health")
        print("   📚 مستندات: http://localhost:8000/docs")
        print("\n🎯 دستورات راه‌اندازی:")
        print("   python main.py")
        print("   یا")
        print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        print("="*50)
        
        # ذخیره گزارش
        with open("logs/setup.log", "w", encoding="utf-8") as f:
            f.write("\n".join(self.setup_log))
    
    def run_setup(self):
        """اجرای کامل راه‌اندازی"""
        self.log("🚀 شروع راه‌اندازی تتراشاپ...")
        
        steps = [
            self.install_dependencies,
            self.create_directory_structure,
            self.create_config_files,
            self.create_main_app,
            self.setup_complete
        ]
        
        for step in steps:
            try:
                step()
            except Exception as e:
                self.log(f"⚠️ خطا در مرحله {step.__name__}: {e}")
                continue

if __name__ == "__main__":
    setup = TetrashopSetup()
    setup.run_setup()
