from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
import pandas as pd
import asyncio
import random
import time

app = FastAPI()

# --- CORS 허용 ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# --- 정적 파일 경로 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

# --- 인메모리 DB (테스트용) ---
PERSONAS = []
URLS = []
CHAT_LOG = []

# --- 메인 페이지 ---
@app.get("/")
async def root():
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"detail": "index.html not found"}, status_code=404)

# --- 페르소나 & URL 등록 ---
@app.post("/register")
async def register(persona: str = Form(...), persona_desc: str = Form(...), urls: str = Form(...)):
    urls_list = [u.strip() for u in urls.split(",") if u.strip() != ""]
    
    # 중복 제거
    for u in urls_list:
        if u not in URLS:
            URLS.append(u)
    if persona not in PERSONAS:
        PERSONAS.append({"persona": persona, "desc": persona_desc})
    return {"status": "ok", "personas": PERSONAS, "urls": URLS}

# --- 자동 토론 시뮬레이션 ---
async def auto_talk():
    while True:
        if PERSONAS and URLS:
            # 랜덤 페르소나, URL 선택
            persona = random.choice(PERSONAS)
            url = random.choice(URLS)
            msg = f"{persona['persona']} 관점: {url} 관련 이렇게 생각함. 인사이트: {random.choice(['디자인 좋아요', '가격 대비 효율적', '사용자 경험 개선 필요'])}"
            CHAT_LOG.append(msg)
            if len(CHAT_LOG) > 50:
                CHAT_LOG.pop(0)
        await asyncio.sleep(random.randint(20,60))

# --- 서버 시작시 자동 토론 백그라운드 ---
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(auto_talk())

# --- 토론 로그 조회 ---
@app.get("/chat_log")
async def get_chat_log():
    return {"chat_log": CHAT_LOG}

# --- 분석 ---
@app.get("/analyze")
async def analyze():
    # Data 분석: AI 기반 URL 분석
    data_summary = [f"[AI DATA 분석] {url} 관련 인사이트: {random.choice(['트렌디', '가격 경쟁력 있음', 'UI/UX 개선 필요'])}" for url in URLS]
    # Content 분석: 사람 관점
    content_summary = [f"[사람 CONTENT 분석] {p['persona']} ({p['desc']}) 관점 시사점: {random.choice(['흥미롭다', '경쟁사 대비 강점 있음', '개선 필요'])}" for p in PERSONAS]
    return {"data_summary": data_summary, "content_summary": content_summary}
