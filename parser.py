import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import json

def parse_url(url: str):
    """웹페이지 메타, H태그, 스키마 추출"""
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Failed to fetch URL"}

    soup = BeautifulSoup(response.text, "html.parser")
    meta = {m.get("name") or m.get("property"): m.get("content") for m in soup.find_all("meta") if m.get("content")}
    htags = {f"h{i}": [tag.get_text(strip=True) for tag in soup.find_all(f"h{i}")] for i in range(1,7)}
    
    # JSON-LD schema
    schema = [json.loads(s.string) for s in soup.find_all("script", type="application/ld+json") if s.string]

    return {
        "meta": meta,
        "htags": htags,
        "schema": schema
    }

def parse_youtube(url: str):
    """간단한 YouTube transcript 추출 (외부 API/라이브러리 필요시 확장 가능)"""
    video_id = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    if not video_id:
        return {"error": "Invalid YouTube URL"}
    video_id = video_id.group(1)
    
    # 실제 환경에서는 YouTube API 연동 필요
    transcript = f"[유튜브 {video_id} transcript placeholder]"
    return {"transcript": transcript}
