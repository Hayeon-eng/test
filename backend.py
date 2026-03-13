from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sqlite3
import pandas as pd
from datetime import datetime
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 초기화
DB_FILE = "comments.db"
if not os.path.exists(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""CREATE TABLE comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    persona TEXT,
                    comment TEXT,
                    analysis TEXT,
                    timestamp TEXT
                )""")
    conn.commit()
    conn.close()

# 정적파일
app.mount("/static", StaticFiles(directory=".", html=False), name="static")

@app.get("/")
async def root():
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))

# 댓글/URL 저장
@app.post("/analyze")
async def analyze(data: dict):
    url = data.get("url")
    persona = data.get("persona")
    comment = data.get("comment", "")

    # 여기서 분석 → AI 시뮬레이션
    content_insight = f"[{persona}] 이 URL 콘텐츠는 읽기 쉽게 구조화 되어있고, 주요 포인트가 명확합니다."
    data_insight = "데이터 측면에서는 meta, schema, htag 등 AEO 관점 최적화 필요."
    analysis = f"콘텐츠 인사이트:\n{content_insight}\n\n데이터 인사이트:\n{data_insight}"

    # DB 저장
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO comments (url, persona, comment, analysis, timestamp) VALUES (?, ?, ?, ?, ?)",
              (url, persona, comment, analysis, datetime.now().isoformat()))
    conn.commit()
    conn.close()

    return JSONResponse({"analysis": analysis})

# 댓글 조회
@app.get("/comments")
async def get_comments():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, url, persona, comment, analysis, timestamp FROM comments ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    comments = [{"id": r[0], "url": r[1], "persona": r[2], "comment": r[3], "analysis": r[4], "timestamp": r[5]} for r in rows]
    return JSONResponse(comments)

# RAW 다운로드 (엑셀)
@app.get("/download_raw")
async def download_raw():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM comments", conn)
    conn.close()
    file_path = "comments.xlsx"
    df.to_excel(file_path, index=False)
    return FileResponse(file_path, filename="comments.xlsx")
