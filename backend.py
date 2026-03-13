from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import os
import tempfile
import asyncio

app = FastAPI()

# --- 정적 파일 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

# --- 메인 페이지 ---
@app.get("/")
async def root():
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"detail": "index.html not found"}, status_code=404)

# --- 라운드별 토론 데이터 저장 (메모리, 후에 Excel로) ---
rounds_data = []

# --- 페르소나 + URL 입력 시 자동 토론 ---
@app.post("/talk")
async def talk(persona: str = Form(...), urls: str = Form(...)):
    """
    persona: '애플 팬, Gen Z, 디자인 중시' 등 자유 입력
    urls: 'apple.com, samsung.com' 콤마 구분
    """
    url_list = [u.strip() for u in urls.split(",") if u.strip()]
    new_round = []
    summary = f"요약: {persona} 시각에서 {len(url_list)}개 URL 토론 시작"
    
    # 간단 예시 발화 (실제 LLM 연동 가능)
    for url in url_list:
        new_round.append({
            "url": url,
            "persona": persona,
            "comment": f"{persona} 시각에서 {url} 분석: 핵심 포인트 논의",
            "insight": "디자인/가격/UX 등 관점에서 비교 가능"
        })
    rounds_data.append(new_round)
    return {"summary": summary, "round": new_round}

# --- Excel 다운로드 ---
@app.get("/download_raw")
async def download_raw():
    tmp_file = os.path.join(tempfile.gettempdir(), "raw_data.xlsx")
    all_rows = []
    for r, round_ in enumerate(rounds_data, 1):
        for entry in round_:
            all_rows.append({
                "Round": r,
                "URL": entry["url"],
                "Persona": entry["persona"],
                "Comment": entry["comment"],
                "Insight": entry["insight"]
            })
    df = pd.DataFrame(all_rows)
    df.to_excel(tmp_file, index=False)
    return FileResponse(tmp_file, filename="raw_data.xlsx")
