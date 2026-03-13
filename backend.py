from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import tempfile
import pandas as pd
import random
import time
import threading

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

# --- 저장된 페르소나/URL ---
personas_urls = []

# --- 자동 토론 로그 ---
discussion_log = []

# --- RAG 모킹 분석 ---
def mock_rag_analysis(persona, urls):
    data_analysis = f"[AI DATA 분석] {persona} 관점에서 " + ", ".join(urls) + " 분석 결과"
    content_analysis = f"[사람 CONTENT 분석] {persona} 특성을 반영한 콘텐츠 시사점"
    return data_analysis, content_analysis

# --- 자동 토론 생성 ---
def auto_discussion():
    while True:
        time.sleep(random.randint(20,60))
        if personas_urls:
            entry = random.choice(personas_urls)
            persona, url = entry["persona"], random.choice(entry["urls"])
            message = f"{persona}가 {url} 관련 의견: '{random.choice(['좋다', '좀 아쉽다', '관심 있음', '추천'])}'"
            discussion_log.append(message)
            # 최대 50개로 제한
            if len(discussion_log) > 50:
                discussion_log.pop(0)

threading.Thread(target=auto_discussion, daemon=True).start()

# --- 메인 페이지 ---
@app.get("/")
async def root():
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"detail": "index.html not found"}, status_code=404)

# --- 페르소나/URL 등록 ---
@app.post("/register")
async def register(persona: str = Form(...), urls: str = Form(...)):
    urls_list = [u.strip() for u in urls.split(",") if u.strip()]
    # 중복 체크
    for entry in personas_urls:
        if entry["persona"] == persona:
            for u in urls_list:
                if u not in entry["urls"]:
                    entry["urls"].append(u)
            break
    else:
        personas_urls.append({"persona": persona, "urls": urls_list})
    return {"status":"ok", "personas_urls": personas_urls}

# --- 분석 ---
@app.get("/analyze")
async def analyze():
    results = []
    for entry in personas_urls:
        persona, urls = entry["persona"], entry["urls"]
        data_analysis, content_analysis = mock_rag_analysis(persona, urls)
        results.append({
            "persona": persona,
            "urls": urls,
            "data_analysis": data_analysis,
            "content_analysis": content_analysis
        })
    return {"results": results, "discussion_log": discussion_log}

# --- Excel 다운로드 ---
@app.get("/download_raw")
async def download_raw():
    tmp_file = os.path.join(tempfile.gettempdir(), "raw_data.xlsx")
    df = pd.DataFrame([
        {"Persona": e["persona"], "URLs": ", ".join(e["urls"])} for e in personas_urls
    ])
    df.to_excel(tmp_file, index=False)
    return FileResponse(tmp_file, filename="raw_data.xlsx")
