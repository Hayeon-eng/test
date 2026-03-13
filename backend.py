from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os, json, tempfile, random, time
import asyncio

app = FastAPI()

# CORS 허용 (프론트에서 바로 접근 가능하게)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 데이터 파일
PERSONAS_FILE = os.path.join(BASE_DIR, "personas.json")
URLS_FILE = os.path.join(BASE_DIR, "urls.json")

# --- 초기 데이터 로딩 ---
if not os.path.exists(PERSONAS_FILE):
    personas = []
    with open(PERSONAS_FILE, "w") as f:
        json.dump(personas, f)
else:
    with open(PERSONAS_FILE, "r") as f:
        personas = json.load(f)

if not os.path.exists(URLS_FILE):
    urls = []
    with open(URLS_FILE, "w") as f:
        json.dump(urls, f)
else:
    with open(URLS_FILE, "r") as f:
        urls = json.load(f)

# 토론 상태
discussion_log = []

# --- 유틸 ---
def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def mock_rag(persona, url):
    # 테스트용 Mock 인사이트 생성
    statements = [
        f"{persona['name']} 시각에서 {url}는 혁신적이라고 생각함.",
        f"{persona['name']}는 {url}의 디자인이 마음에 든다고 평가함.",
        f"{persona['name']}는 {url}의 기능보다 브랜드 충성도가 중요하다고 느낌.",
        f"{persona['name']}는 {url}에 대해 다른 의견이 있지만, 일부는 동의함."
    ]
    return random.choice(statements)

async def auto_discussion():
    while True:
        await asyncio.sleep(20)  # 20초마다 자동 토론
        if not personas or not urls:
            continue
        p = random.choice(personas)
        u = random.choice(urls)
        msg = mock_rag(p, u)
        discussion_log.append({"persona": p["name"], "url": u, "message": msg})
        # 최근 50개만 유지
        if len(discussion_log) > 50:
            discussion_log.pop(0)

# --- 프론트 노출 ---
@app.get("/")
async def root():
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"detail": "index.html not found"}, status_code=404)

# --- 페르소나 등록 ---
@app.post("/add_persona")
async def add_persona(name: str = Form(...), description: str = Form(...)):
    global personas
    if any(p["name"] == name for p in personas):
        return {"status": "exist"}
    persona = {"name": name, "description": description}
    personas.append(persona)
    save_json(PERSONAS_FILE, personas)
    return {"status": "ok", "persona": persona}

# --- URL 등록 ---
@app.post("/add_url")
async def add_url(url: str = Form(...)):
    global urls
    if url in urls:
        return {"status": "exist"}
    urls.append(url)
    save_json(URLS_FILE, urls)
    return {"status": "ok", "url": url}

# --- 현재 상태 반환 (토론 + 등록 데이터) ---
@app.get("/state")
async def state():
    return {
        "personas": personas,
        "urls": urls,
        "discussion_log": discussion_log[-20:]  # 최근 20개
    }

# --- Excel 다운로드 ---
@app.get("/download_raw")
async def download_raw():
    import pandas as pd
    tmp_file = os.path.join(tempfile.gettempdir(), "raw_data.xlsx")
    df = pd.DataFrame(discussion_log)
    df.to_excel(tmp_file, index=False)
    return FileResponse(tmp_file, filename="raw_data.xlsx")

# --- 자동 토론 시작 ---
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(auto_discussion())
