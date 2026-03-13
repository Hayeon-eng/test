from fastapi import FastAPI, WebSocket, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import asyncio, random, os, tempfile, pandas as pd

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

# --- 페르소나 & URL 저장 ---
personas = []
urls = []

# --- 토론 로그 ---
discussion_log = []

# --- WebSocket 연결 ---
connected_websockets = []

# --- 메인 페이지 ---
@app.get("/")
async def root():
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"detail": "index.html not found"}, status_code=404)

# --- 페르소나 입력 ---
@app.post("/add_persona")
async def add_persona(persona: str = Form(...)):
    if persona not in personas:
        personas.append(persona)
    return {"personas": personas}

# --- URL 입력 ---
@app.post("/add_url")
async def add_url(url: str = Form(...)):
    if url not in urls:
        urls.append(url)
    return {"urls": urls}

# --- Data/Content 분석 + 토론 라운드 ---
async def generate_round():
    while True:
        if not personas or not urls:
            await asyncio.sleep(5)
            continue
        
        persona = random.choice(personas)
        url = random.choice(urls)
        
        # --- 샘플 분석 ---
        data_analysis = f"[AI DATA 분석] {persona} 관점에서 {url} 분석 완료"
        content_analysis = f"[사람 CONTENT 분석] {persona} 관점에서 시사점 요약"
        
        # --- 샘플 토론 발화 ---
        prev = discussion_log[-1]["text"] if discussion_log else ""
        debate_text = f"{persona}: {url} 관련, 내 의견은 '{prev} + 새로운 인사이트' 입니다."
        
        round_data = {
            "persona": persona,
            "url": url,
            "data_analysis": data_analysis,
            "content_analysis": content_analysis,
            "text": debate_text
        }
        discussion_log.append(round_data)
        
        # --- WebSocket 브로드캐스트 ---
        for ws in connected_websockets:
            await ws.send_json(round_data)
        
        await asyncio.sleep(random.randint(20, 60))  # 20~60초 간격

# --- WebSocket 연결 ---
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    connected_websockets.append(ws)
    
    # 접속 시 기존 로그 전송
    for msg in discussion_log:
        await ws.send_json(msg)
    
    try:
        while True:
            await ws.receive_text()  # 클라이언트 유지용
    except:
        connected_websockets.remove(ws)

# --- Excel 다운로드 ---
@app.get("/download_raw")
async def download_raw():
    tmp_file = os.path.join(tempfile.gettempdir(), "raw_data.xlsx")
    df = pd.DataFrame({
        "Persona": personas or ["샘플 페르소나"],
        "URL": urls or ["샘플 URL"],
        "Discussion": [d["text"] for d in discussion_log] or ["샘플 토론"]
    })
    df.to_excel(tmp_file, index=False)
    return FileResponse(tmp_file, filename="raw_data.xlsx")

# --- 백그라운드 자동 라운드 시작 ---
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(generate_round())
