# backend.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import shutil
import pandas as pd
from fastapi.responses import FileResponse

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

# ---------------------------
# 5️⃣ 댓글 + 데이터 저장
comments_store = []

# ---------------------------
# 6️⃣ 분석 API (placeholder)
def analyze_content(data):
    """
    data: {
        "type": "text" | "url" | "youtube",
        "content": "...",
        "persona": {"name": "...", "personality": "..."}
    }
    """
    content = data.get("content","")
    persona = data.get("persona",{})
    # 더미 분석
    analysis = {
        "data_insight": f"Data perspective analysis for {content[:30]}...",
        "content_insight": f"{persona.get('name','AI')} thinks: This content is engaging and persona-aware.",
        "AEO_score": 0.85,
        "brand_sentiment": "neutral",
        "AI_citation_prob": 0.42,
        "topics": ["example_topic1","example_topic2"]
    }
    return analysis

# ---------------------------
# 7️⃣ API 라우터
@app.post("/analyze")
async def analyze(data: dict):
    result = analyze_content(data)
    return {"analysis": result, "comments": comments_store}

@app.post("/comment")
async def add_comment(data: dict):
    comment = data.get("comment", "")
    comments_store.append({
        "summary": comment[:50],
        "keywords": ["example_keyword"],
        "sentiment": "neutral",
        "full_comment": comment
    })
    return {"comments": comments_store}

@app.get("/download_raw")
async def download_raw():
    df = pd.DataFrame(comments_store)
    df.to_excel("comments.xlsx", index=False)
    return FileResponse(
        "comments.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="comments.xlsx"
    )
