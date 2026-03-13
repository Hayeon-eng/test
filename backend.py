from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import asyncio, json, os, random, time
from typing import List

app = FastAPI()

# --- 정적 파일 서빙 ---
app.mount("/", StaticFiles(directory=".", html=True), name="static")

# --- 파일 경로 ---
PERSONAS_FILE = "personas.json"
URLS_FILE = "urls.json"

# --- 메모리 저장 ---
personas = []
urls = []
discussions = []

# --- 초기 JSON 로드 ---
if os.path.exists(PERSONAS_FILE):
    with open(PERSONAS_FILE, "r", encoding="utf-8") as f:
        personas = json.load(f)

if os.path.exists(URLS_FILE):
    with open(URLS_FILE, "r", encoding="utf-8") as f:
        urls = json.load(f)

# --- Helper: Mock LLM 분석 (RAG 테스트용) ---
def analyze_url_with_persona(persona: dict, url: str):
    # 실제 RAG 대신 mock 분석
    data_analysis = f"[AI DATA 분석] {persona['name']} 관점에서 {url} 분석 결과"
    content_analysis = f"[사람 CONTENT 분석] {persona['description']} 반영, 콘텐츠 시사점"
    return data_analysis, content_analysis

# --- Helper: 토론 생성 ---
def generate_discussion():
    if not personas or not urls:
        return
    p1, p2 = random.sample(personas, 2) if len(personas) > 1 else (personas[0], personas[0])
    url = random.choice(urls)
    msg1 = f"{p1['name']}: 나는 {url} 관련해서 이렇게 생각함"
    msg2 = f"{p2['name']}: 근데 나는 {url} 이렇게 평가함, 너랑 달라"
    msg3 = f"{p1['name']}: 아, 그럴 수 있네. 하지만 {url} 보면…"
    discussions.extend([msg1, msg2, msg3])
    # 최대 100개 유지
    if len(discussions) > 100:
        discussions[:] = discussions[-100:]

# --- 자동 토론 task ---
async def auto_discuss():
    while True:
        generate_discussion()
        await asyncio.sleep(random.randint(20,60))

# --- FastAPI startup 이벤트 ---
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(auto_discuss())

# --- API: 페르소나 등록 ---
@app.post("/add_persona")
async def add_persona(name: str = Form(...), description: str = Form(...)):
    for p in personas:
        if p['name'] == name:
            return {"detail": "이미 등록된 페르소나입니다."}
    persona = {"name": name, "description": description}
    personas.append(persona)
    with open(PERSONAS_FILE, "w", encoding="utf-8") as f:
        json.dump(personas, f, ensure_ascii=False, indent=2)
    return {"detail": "등록 완료", "persona": persona}

# --- API: URL 등록 ---
@app.post("/add_url")
async def add_url(url: str = Form(...)):
    if url in urls:
        return {"detail": "이미 등록된 URL입니다."}
    urls.append(url)
    with open(URLS_FILE, "w", encoding="utf-8") as f:
        json.dump(urls, f, ensure_ascii=False, indent=2)
    return {"detail": "등록 완료", "url": url}

# --- API: 현재 상태 ---
@app.get("/state")
async def state():
    # 분석 결과 포함
    data_results = []
    content_results = []
    for p in personas:
        for u in urls:
            d, c = analyze_url_with_persona(p, u)
            data_results.append(d)
            content_results.append(c)
    return {
        "personas": personas,
        "urls": urls,
        "discussions": discussions[-20:],  # 최근 20개만
        "data_analysis": data_results,
        "content_analysis": content_results
    }
