from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import json, os, random, asyncio, tempfile

app = FastAPI()

# CORS 설정 (프론트에서 접근 가능하게)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSONA_FILE = os.path.join(BASE_DIR, "personas.json")
URL_FILE = os.path.join(BASE_DIR, "urls.json")

# --- 데이터 로드 ---
def load_personas():
    with open(PERSONA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_urls():
    with open(URL_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# --- Mock RAG 기반 분석 ---
def mock_analysis(persona, url):
    """실제 RAG 없이 샘플 AI 분석 생성"""
    return f"[{persona['nickname']} 관점] {url} 내용 기반 인사이트: 흥미로운 특징 발견됨."

# --- 자동 토론 상태 ---
DISCUSSIONS = []

async def auto_discussion_loop():
    while True:
        personas = load_personas()
        urls = load_urls()
        if not personas or not urls:
            await asyncio.sleep(10)
            continue
        # 랜덤 페르소나 + URL 선택
        persona = random.choice(personas)
        url = random.choice(urls)
        msg = mock_analysis(persona, url)
        DISCUSSIONS.append({"persona": persona['nickname'], "url": url, "message": msg})
        # 최대 100개 메시지 유지
        if len(DISCUSSIONS) > 100:
            DISCUSSIONS.pop(0)
        await asyncio.sleep(random.randint(20,60))  # 20~60초마다 발화

# --- 백그라운드 자동 토론 시작 ---
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(auto_discussion_loop())

# --- 토론 조회 ---
@app.get("/discussions")
async def get_discussions():
    return JSONResponse(DISCUSSIONS)

# --- 페르소나 조회/추가 ---
@app.get("/personas")
async def get_personas():
    return JSONResponse(load_personas())

@app.post("/personas")
async def add_persona(nickname: str = Form(...), description: str = Form(...)):
    personas = load_personas()
    # 중복 체크
    if any(p["nickname"] == nickname for p in personas):
        return JSONResponse({"detail": "이미 존재하는 페르소나"}, status_code=400)
    personas.append({"nickname": nickname, "description": description})
    with open(PERSONA_FILE, "w", encoding="utf-8") as f:
        json.dump(personas, f, ensure_ascii=False, indent=2)
    return JSONResponse({"detail": "등록 완료"})

# --- URL 조회/추가 ---
@app.get("/urls")
async def get_urls():
    return JSONResponse(load_urls())

@app.post("/urls")
async def add_url(url: str = Form(...)):
    urls = load_urls()
    if url in urls:
        return JSONResponse({"detail": "이미 존재하는 URL"}, status_code=400)
    urls.append(url)
    with open(URL_FILE, "w", encoding="utf-8") as f:
        json.dump(urls, f, ensure_ascii=False, indent=2)
    return JSONResponse({"detail": "URL 등록 완료"})

# --- Excel 다운로드 ---
@app.get("/download_raw")
async def download_raw():
    import pandas as pd
    tmp_file = os.path.join(tempfile.gettempdir(), "raw_data.xlsx")
    df = pd.DataFrame({
        "Persona": [d["persona"] for d in DISCUSSIONS],
        "URL": [d["url"] for d in DISCUSSIONS],
        "Message": [d["message"] for d in DISCUSSIONS]
    })
    df.to_excel(tmp_file, index=False)
    return FileResponse(tmp_file, filename="raw_data.xlsx")
