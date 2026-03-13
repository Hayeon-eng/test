# backend.py
from fastapi import FastAPI, Form
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

# --- 페르소나 입력 & URL 등록 ---
# 토론 라운드별 무한 발화용
ROUNDS = []

@app.post("/add_topic")
async def add_topic(persona: str = Form(...), persona_desc: str = Form(...), urls: str = Form(...)):
    # urls는 쉼표로 구분
    topic = {
        "persona": persona,
        "description": persona_desc,
        "urls": [u.strip() for u in urls.split(",")],
        "rounds": []
    }
    ROUNDS.append(topic)
    return {"status": "ok", "topics": len(ROUNDS)}

# --- 토론 시뮬레이션 ---
@app.get("/simulate_rounds")
async def simulate_rounds():
    results = []
    for topic in ROUNDS:
        data_analysis = f"[AI DATA 분석] {topic['persona']} 관점에서 {', '.join(topic['urls'])} 분석 결과"
        content_analysis = f"[사람 CONTENT 분석] {topic['description']} 반영, 콘텐츠 시사점"
        # 라운드별 발화 예시
        discussion = [
            f"{topic['persona']}: 나는 {topic['urls'][0]} 관련해서 이렇게 생각함",
            f"다른 참가자: 근데 나는 {topic['urls'][0]} 이렇게 평가함, 너랑 다름",
            f"{topic['persona']}: 아, 그럴 수 있네. 그렇지만 {topic['urls'][1]} 보면…"
        ]
        topic["rounds"].append({
            "data": data_analysis,
            "content": content_analysis,
            "discussion": discussion
        })
        results.append(topic["rounds"][-1])
    return {"results": results}

# --- Excel 다운로드 ---
@app.get("/download_raw")
async def download_raw():
    tmp_file = os.path.join(tempfile.gettempdir(), "raw_data.xlsx")
    data = []
    for topic in ROUNDS:
        for r in topic["rounds"]:
            data.append({
                "Persona": topic["persona"],
                "Persona_desc": topic["description"],
                "URLs": ", ".join(topic["urls"]),
                "Data_summary": r["data"],
                "Content_summary": r["content"]
            })
    df = pd.DataFrame(data)
    df.to_excel(tmp_file, index=False)
    return FileResponse(tmp_file, filename="raw_data.xlsx")
