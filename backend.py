# backend.py
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import os
import tempfile

app = FastAPI()

# --- 정적 파일 경로 ---
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
async def analyze(persona: str = Form(...), urls: str = Form(...)):
    """
    persona: 사용자 정의 페르소나 설명
    urls: 분석할 사이트 URL들을 쉼표(,)로 구분
    """
    url_list = [u.strip() for u in urls.split(",") if u.strip()]

    # --- Data 분석 (AI 관점) ---
    data_summary = f"[AI 분석] {len(url_list)}개 URL 패턴과 페르소나 '{persona}' 시각 분석"
    data_insights = [
        f"1️⃣ 주요 URL 트렌드 및 패턴 도출",
        "2️⃣ 잠재적 리스크/기회 식별",
        "3️⃣ AEO 최적화 가능 포인트 제안"
    ]

    # --- Content 분석 (사람 관점) ---
    content_summary = f"[사람 분석] 페르소나 '{persona}' 관점에서 콘텐츠 평가"
    content_insights = [
        "1️⃣ 주관적 의견과 반박 포인트 포함",
        "2️⃣ 메시지 전달력 및 설득력 분석",
        "3️⃣ UX/UI 개선 및 전략적 제안"
    ]

    # --- 토론 시뮬레이션 ---
    discussion = []
    for url in url_list:
        discussion.append({
            "persona": persona,
            "url": url,
            "statement": f"[AI] {url}에 대한 데이터 기반 의견 제시",
            "content_perspective": f"[사람] '{persona}' 시각에서 콘텐츠 평가 및 반박"
        })
        discussion.append({
            "persona": persona,
            "url": url,
            "statement": f"[AI] 이전 의견에 대한 논리적 추가/반박",
            "content_perspective": f"[사람] 추가 의견 및 반박"
        })

    return {
        "data_analysis": {
            "summary": data_summary,
            "insights": data_insights
        },
        "content_analysis": {
            "summary": content_summary,
            "insights": content_insights
        },
        "discussion": discussion
    }

# --- Excel 다운로드 ---
@app.get("/download_raw")
async def download_raw():
    tmp_file = os.path.join(tempfile.gettempdir(), "raw_data.xlsx")
    df = pd.DataFrame({
        "Persona": ["샘플 페르소나"],
        "URLs": ["https://example.com"],
        "Data_Summary": ["샘플 데이터 분석 요약"],
        "Content_Summary": ["샘플 콘텐츠 분석 요약"]
    })
    df.to_excel(tmp_file, index=False)
    return FileResponse(tmp_file, filename="raw_data.xlsx")
