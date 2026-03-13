from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import json
import os
import tempfile
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

# --- WebSocket 연결 관리 ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

# --- Load personas & urls ---
PERSONAS_FILE = os.path.join(BASE_DIR, "personas.json")
URLS_FILE = os.path.join(BASE_DIR, "urls.json")

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

personas = load_json(PERSONAS_FILE)
urls = load_json(URLS_FILE)

# --- RAG mock 분석 ---
def rag_mock_analysis(persona, url_list):
    # 데이터 분석(자동, AI mock)
    data_analysis = f"[AI DATA 분석] {persona['name']} 관점에서 {', '.join(url_list)} 분석 결과"
    # 콘텐츠 분석(사람 관점 mock)
    content_analysis = f"[사람 CONTENT 분석] {persona['description']} 기반, 콘텐츠 시사점"
    return data_analysis, content_analysis

# --- WebSocket endpoint for auto discussion ---
@app.websocket("/ws/discuss")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(random.randint(20,60))  # 20~60초마다 발화
            if not personas or not urls:
                continue
            persona = random.choice(personas)
            url = random.choice(urls)
            message = {
                "persona": persona["name"],
                "url": url,
                "comment": f"{persona['name']} 시각에서 {url} 관련 의견: {random.choice(['좋다고 생각함','아쉽다고 생각함','중립적임'])}"
            }
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# --- 메인 페이지 ---
@app.get("/")
async def root():
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"detail": "index.html not found"}, status_code=404)

# --- Persona 추가 ---
@app.post("/add_persona")
async def add_persona(name: str = Form(...), description: str = Form(...)):
    global personas
    new_persona = {"name": name, "description": description}
    if new_persona not in personas:
        personas.append(new_persona)
        save_json(PERSONAS_FILE, personas)
    return {"personas": personas}

# --- URL 추가 ---
@app.post("/add_url")
async def add_url(url: str = Form(...)):
    global urls
    if url not in urls:
        urls.append(url)
        save_json(URLS_FILE, urls)
    return {"urls": urls}

# --- 분석 결과 (mock RAG) ---
@app.post("/analyze")
async def analyze():
    results = []
    for persona in personas:
        data_res, content_res = rag_mock_analysis(persona, urls)
        results.append({
            "persona": persona["name"],
            "data_analysis": data_res,
            "content_analysis": content_res
        })
    return {"results": results}

# --- Excel 다운로드 ---
@app.get("/download_raw")
async def download_raw():
    tmp_file = os.path.join(tempfile.gettempdir(), "raw_data.xlsx")
    import pandas as pd
    df = pd.DataFrame({
        "Persona": [p["name"] for p in personas],
        "Description": [p["description"] for p in personas],
        "URLs": [", ".join(urls) for _ in personas]
    })
    df.to_excel(tmp_file, index=False)
    return FileResponse(tmp_file, filename="raw_data.xlsx")
