# backend.py
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import tempfile
import random

app = FastAPI()

# --- 정적 파일 경로 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

# --- 메인 페이지 ---
@app.get("/")
async def root():
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"detail": "index.html not found"}, status_code=404)

# --- 테스트용 LLM 토론 시뮬레이션 ---
class Persona:
    def __init__(self, name, traits):
        self.name = name
        self.traits = traits

class Topic:
    def __init__(self, url, content):
        self.url = url
        self.content = content

# 메모리 기반 간단 시뮬레이션
personas = []
topics = []

def generate_insight(persona: Persona, topic: Topic):
    # 무작위 토론 인사이트 예시
    starters = [
        f"{persona.name} 생각: '{topic.url}' 관련해서 중요한 건 {random.choice(['사용자 경험', '가격 전략', '브랜드 이미지'])}이라고 봐요.",
        f"{persona.name} 의견: {topic.content[:30]}... 부분이 특히 흥미롭네요.",
        f"{persona.name} 분석: {random.choice(['장점과 단점을 모두 고려', '경쟁사와 비교', '트렌드 반영'])} 필요합니다."
    ]
    rebuttals = [
        f"{persona.name} 반박: '{topic.url}' 부분은 {random.choice(['조금 과장되었음', '데이터 부족', '다른 시각 필요'])} 같아요.",
        f"{persona.name} 의견: 전 {random.choice(['동의', '부분 동의', '다르게 생각'])}합니다."
    ]
    return starters + rebuttals

@app.post("/add_persona")
async def add_persona(name: str = Form(...), traits: str = Form(...)):
    persona = Persona(name, traits)
    personas.append(persona)
    return {"message": f"페르소나 '{name}' 추가 완료!", "traits": traits}

@app.post("/add_topic")
async def add_topic(url: str = Form(...), content: str = Form(...)):
    topic = Topic(url, content)
    topics.append(topic)
    return {"message": f"토픽 '{url}' 추가 완료!", "content": content}

@app.get("/simulate_discussion")
async def simulate_discussion():
    if not personas or not topics:
        return {"detail": "페르소나 또는 토픽이 없습니다."}
    
    discussion = []
    for topic in topics:
        for persona in personas:
            discussion.extend(generate_insight(persona, topic))
    
    return {"discussion": discussion}

# --- Excel 다운로드 (예시) ---
@app.get("/download_raw")
async def download_raw():
    tmp_file = os.path.join(tempfile.gettempdir(), "raw_data.xlsx")
    import pandas as pd
    df = pd.DataFrame({
        "Persona": [p.name for p in personas],
        "Traits": [p.traits for p in personas],
        "Topics": [t.url for t in topics],
    })
    df.to_excel(tmp_file, index=False)
    return FileResponse(tmp_file, filename="raw_data.xlsx")
