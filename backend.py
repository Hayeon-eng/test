from fastapi import FastAPI, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import json, os, asyncio, random, time

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

URL_FILE = os.path.join(BASE_DIR, "urls.json")
PERSONA_FILE = os.path.join(BASE_DIR, "personas.json")

# --- 파일 초기화 ---
for f in [URL_FILE, PERSONA_FILE]:
    if not os.path.exists(f):
        with open(f, "w") as fp:
            json.dump([], fp)

# --- 메인 페이지 ---
@app.get("/")
async def root():
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"detail": "index.html not found"}, status_code=404)

# --- 등록 API ---
@app.post("/register_url")
async def register_url(url: str = Form(...)):
    with open(URL_FILE, "r+") as fp:
        data = json.load(fp)
        if url not in data:
            data.append(url)
            fp.seek(0)
            json.dump(data, fp, ensure_ascii=False, indent=2)
            fp.truncate()
    return {"urls": data}

@app.post("/register_persona")
async def register_persona(name: str = Form(...), description: str = Form(...)):
    with open(PERSONA_FILE, "r+") as fp:
        data = json.load(fp)
        if not any(p["name"] == name for p in data):
            data.append({"name": name, "description": description})
            fp.seek(0)
            json.dump(data, fp, ensure_ascii=False, indent=2)
            fp.truncate()
    return {"personas": data}

# --- 리스트 조회 ---
@app.get("/get_data")
async def get_data():
    with open(URL_FILE) as f:
        urls = json.load(f)
    with open(PERSONA_FILE) as f:
        personas = json.load(f)
    return {"urls": urls, "personas": personas}

# --- WebSocket 자동 토론 ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for conn in self.active_connections:
            await conn.send_json(message)

manager = ConnectionManager()

async def mock_rag_analysis(persona, url):
    """Mock RAG: Data 분석(AI) + Content 분석(사람 관점)"""
    data_analysis = f"[AI DATA 분석] {persona['name']} 관점에서 {url} 분석 완료"
    content_analysis = f"[사람 CONTENT 분석] {persona['description']} 반영"
    return {"data": data_analysis, "content": content_analysis}

async def generate_mock_discussion():
    while True:
        await asyncio.sleep(random.randint(20,60))
        # Load personas & urls
        with open(PERSONA_FILE) as f:
            personas = json.load(f)
        with open(URL_FILE) as f:
            urls = json.load(f)
        if not personas or not urls:
            continue
        persona = random.choice(personas)
        url = random.choice(urls)
        analysis = await mock_rag_analysis(persona, url)
        message = {
            "persona": persona["name"],
            "url": url,
            "data_analysis": analysis["data"],
            "content_analysis": analysis["content"],
            "discussion": f"{persona['name']}가 {url}에 대해 의견 제시 중..."
        }
        await manager.broadcast(message)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # dummy to keep connection
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# --- 서버 시작 시 자동 토론 태스크 ---
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(generate_mock_discussion())
