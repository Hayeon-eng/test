# backend.py
from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import os
import tempfile

app = FastAPI()

# --- 정적 파일 경로 (index.html 포함) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

# --- 메인 페이지 ---
@app.get("/")
async def root():
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"detail": "index.html not found"}, status_code=404)

# --- 페르소나 입력 & 분석 ---
@app.post("/analyze")
async def analyze(persona: str = Form(...), content: str = Form(...)):
    # 여기에 실제 분석 로직 적용 가능
    # 현재는 간단 예시: 입력 내용 요약 + 3줄 인사이트
    summary = f"요약: '{content[:50]}...' (총 {len(content)}자)"
    insights = [
        f"1️⃣ {persona} 시각에서 핵심 포인트 확인",
        "2️⃣ 데이터 기반 인사이트 생성",
        "3️⃣ AEO 최적화 가능 포인트 제안"
    ]
    return {"summary": summary, "insights": insights}

# --- Excel 다운로드 ---
@app.get("/download_raw")
async def download_raw():
    # Render 안전한 tmp 폴더 사용
    tmp_file = os.path.join(tempfile.gettempdir(), "raw_data.xlsx")
    
    # 예시 데이터
    df = pd.DataFrame({
        "Persona": ["샘플 페르소나"],
        "Content": ["샘플 콘텐츠"],
        "Summary": ["샘플 요약"]
    })
    df.to_excel(tmp_file, index=False)
    return FileResponse(tmp_file, filename="raw_data.xlsx")
