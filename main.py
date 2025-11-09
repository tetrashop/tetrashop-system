from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
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
        "environment": "development",
        "debug": True
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
    
    # ذخیره در فایل
    os.makedirs("data/sessions", exist_ok=True)
    with open(f"data/sessions/{session_id}.json", "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)
    
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
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
