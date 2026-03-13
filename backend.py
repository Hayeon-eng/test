from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from parser import parse_url, parse_youtube
from analyzer import analyze_content, analyze_comments

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

comment_log = []

# 테스트 모드: 과금 없이 동작
TEST_MODE = True

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    content_type = data.get("type")
    content_input = data.get("content")
    persona = data.get("persona", {"name":"Default","trait":"neutral"})

    if content_type == "url":
        parsed = parse_url(content_input)
        combined_content = str(parsed)
    elif content_type == "youtube":
        parsed = parse_youtube(content_input)
        combined_content = parsed.get("transcript","")
    else:
        combined_content = content_input

    if TEST_MODE:
        analysis_result = analyze_content(combined_content, persona)
    else:
        analysis_result = analyze_content(combined_content, persona)

    # 댓글 분석
    comment_analysis = analyze_comments(comment_log)

    return JSONResponse({
        "parsed": combined_content,
        "analysis": analysis_result,
        "comments": comment_analysis
    })

@app.post("/comment")
async def add_comment(request: Request):
    data = await request.json()
    comment = data.get("comment")
    if comment:
        comment_log.append(comment)
    comment_analysis = analyze_comments(comment_log)
    return JSONResponse({"comments": comment_analysis})
