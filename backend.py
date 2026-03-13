# backend.py
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import tempfile
import pandas as pd
import threading
import time
import random
from openai_config import openai_api_call  # RAG 기반 LLM 호출 함수

app = FastAPI()

# --- 정적 파일 경로 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

# --- In-Memory DB ---
PERSONAS = []
URLS = []
DISCUSSIONS = []

# --- 메인 페이지 ---
@app.get("/")
async def root():
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"detail": "index.html not found"}, status_code=404)

# --- 페르소나/URL 등록 ---
@app.post("/register")
async def register(persona: str = Form(...), persona_desc: str = Form(...), url: str = Form(...)):
    if persona not in [p['name'] for p in PERSONAS]:
        PERSONAS.append({"name": persona, "desc": persona_desc})
    if url not in URLS:
        URLS.append(url)
    return {"personas": PERSONAS, "urls": URLS}

# --- 자동 토론 생성 ---
def auto_discussion():
    while True:
        if PERSONAS and URLS:
            persona = random.choice(PERSONAS)
            url = random.choice(URLS)
            # RAG 기반 분석 호출
            msg = openai_api_call(persona['name'], persona['desc'], url)
            DISCUSSIONS.append(msg)
            # 최근 50개만 유지
            if len(DISCUSSIONS) > 50:
                DISCUSSIONS.pop(0)
        time.sleep(random.randint(20, 60))

threading.Thread(target=auto_discussion, daemon=True).start()

# --- 토론 불러오기 ---
@app.get("/discussions")
async def get_discussions():
    return {"discussions": DISCUSSIONS}

# --- 데이터 분석 / 콘텐츠 분석 ---
@app.get("/analysis")
async def analysis():
    if not URLS or not PERSONAS:
        return JSONResponse({"detail": "No URLs or Personas registered"}, status_code=400)
    
    # 예시 분석
    data_analysis = f"[AI DATA 분석] {', '.join(URLS)} 분석 완료"
    content_analysis = f"[사람 CONTENT 분석] {', '.join([p['name'] for p in PERSONAS])} 시각 반영"
    return {"data_analysis": data_analysis, "content_analysis": content_analysis}

# --- Excel 다운로드 ---
@app.get("/download_raw")
async def download_raw():
    tmp_file = os.path.join(tempfile.gettempdir(), "raw_data.xlsx")
    df = pd.DataFrame({
        "Persona": [p['name'] for p in PERSONAS],
        "Persona_Desc": [p['desc'] for p in PERSONAS],
        "URLs": [', '.join(URLS)]
    })
    df.to_excel(tmp_file, index=False)
    return FileResponse(tmp_file, filename="raw_data.xlsx")
