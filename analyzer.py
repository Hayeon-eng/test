from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from parser import parse_url, parse_youtube
from analyzer import analyze_content, analyze_comments
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

comment_log = []
rawData = {}

# 테스트 모드 (과금 없음)
TEST_MODE = True

@app.post("/analyze")
async def analyze(request: Request):
    global rawData
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

    analysis_result = analyze_content(combined_content, persona)

    comment_analysis = analyze_comments(comment_log)

    rawData = {
        "parsed": combined_content,
        "analysis": analysis_result,
        "comments": comment_analysis
    }

    return JSONResponse(rawData)

@app.post("/comment")
async def add_comment(request: Request):
    global rawData
    data = await request.json()
    comment = data.get("comment")
    if comment:
        comment_log.append(comment)
    comment_analysis = analyze_comments(comment_log)
    rawData["comments"] = comment_analysis
    return JSONResponse({"comments": comment_analysis})

@app.get("/download_raw")
async def download_raw():
    global rawData
    # Excel 변환
    df_content = pd.DataFrame([{
        "Data_Insights": rawData.get("analysis", {}).get("data_insights",""),
        "Content_Summary": rawData.get("analysis", {}).get("content_summary",""),
        "Brand_Mentions": ",".join(rawData.get("analysis", {}).get("brand_mentions",[])),
        "AEO_Score": rawData.get("analysis", {}).get("aeo_score","")
    }])
    df_comments = pd.DataFrame(rawData.get("comments",[]))
    file_path = "raw_data.xlsx"
    with pd.ExcelWriter(file_path) as writer:
        df_content.to_excel(writer, sheet_name="Analysis", index=False)
        df_comments.to_excel(writer, sheet_name="Comments", index=False)
    return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename="raw_data.xlsx")
