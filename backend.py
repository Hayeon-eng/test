from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import shutil

# 1️⃣ FastAPI 앱 선언
app = FastAPI()

# 2️⃣ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3️⃣ static/frontend.html 준비
if not os.path.exists("static"):
    os.makedirs("static")
shutil.copy("frontend.html", "static/frontend.html")

# 4️⃣ 정적 파일 마운트
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# 5️⃣ 기존 API 라우터
from parser import parse_url, parse_youtube
from analyzer import analyze_content

comments_store = []

@app.post("/analyze")
async def analyze(data: dict):
    result = analyze_content(data)
    return {"analysis": result, "comments": comments_store}

@app.post("/comment")
async def add_comment(data: dict):
    comment = data.get("comment", "")
    # 간단 분석 placeholder
    comments_store.append({
        "summary": comment[:50],
        "keywords": ["example"],
        "sentiment": "neutral"
    })
    return {"comments": comments_store}

@app.get("/download_raw")
async def download_raw():
    import pandas as pd
    from fastapi.responses import FileResponse
    df = pd.DataFrame(comments_store)
    df.to_excel("comments.xlsx", index=False)
    return FileResponse("comments.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename="comments.xlsx")
