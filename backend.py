from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import os, tempfile, asyncio, random, time
from threading import Thread

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

# 입력값 저장
personas = []
urls = []
debate_history = []

# --- AI 분석 함수 ---
def analyze_content(persona, content, url_list):
    # 실제 LLM API 호출 부분을 여기서 대체 가능
    data_summary = f"[AI DATA 분석] {persona} 관점에서 {', '.join(url_list)} 분석 결과"
    content_summary = f"[사람 CONTENT 분석] {persona} 특성 반영, 콘텐츠 시사점"
    return data_summary, content_summary

# --- 자동 토론 시뮬레이션 ---
async def run_debate():
    while True:
        if not personas or not urls:
            await asyncio.sleep(5)
            continue

        persona = random.choice(personas)
        url = random.choice(urls)
        # 단순 시뮬레이션 예시
        statement = f"{persona} 생각: {url} 관련하여 이런 의견 있음"
        counter = f"다른 참가자: {url} 이렇게 평가함, 너랑 다름"
        debate_history.append({"statement": statement, "counter": counter})
        # 20~60초마다
        await asyncio.sleep(random.randint(20, 60))

# --- 백그라운드 데몬 시작 ---
def start_debate_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_debate())

Thread(target=start_debate_loop, daemon=True).start()

# --- 메인 페이지 ---
@app.get("/")
async def root():
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"detail": "index.html not found"}, status_code=404)

# --- 페르소나 & URL 입력 ---
@app.post("/add")
async def add_persona_url(persona: str = Form(...), url: str = Form(...)):
    if persona not in personas:
        personas.append(persona)
    if url not in urls:
        urls.append(url)
    return {"personas": personas, "urls": urls}

# --- 분석 ---
@app.post("/analyze")
async def analyze(persona: str = Form(...), content: str = Form(...)):
    data_summary, content_summary = analyze_content(persona, content, urls)
    return {
        "data_summary": data_summary,
        "content_summary": content_summary,
        "debate_history": debate_history[-10:]  # 최신 10개만
    }

# --- Excel 다운로드 ---
@app.get("/download_raw")
async def download_raw():
    tmp_file = os.path.join(tempfile.gettempdir(), "raw_data.xlsx")
    df = pd.DataFrame({
        "Persona": personas,
        "URL": urls,
        "Debate": [d['statement'] + ' / ' + d['counter'] for d in debate_history]
    })
    df.to_excel(tmp_file, index=False)
    return FileResponse(tmp_file, filename="raw_data.xlsx")
