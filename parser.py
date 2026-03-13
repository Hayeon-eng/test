import requests
from bs4 import BeautifulSoup
import json
import re

def parse_url(url: str):
    """웹페이지 meta, H태그, schema 추출"""
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Failed to fetch URL"}
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    meta = {m.get("name") or m.get("property"): m.get("content") 
            for m in soup.find_all("meta") if m.get("content")}
    
    htags = {f"h{i}": [tag.get_text(strip=True) for tag in soup.find_all(f"h{i}")] 
             for i in range(1,7)}
    
    schema = []
    for s in soup.find_all("script", type="application/ld+json"):
        if s.string:
            try:
                schema.append(json.loads(s.string))
            except:
                continue
    
    return {
        "meta": meta,
        "htags": htags,
        "schema": schema
    }

def parse_youtube(url: str):
    """YouTube transcript placeholder"""
    video_id = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    if not video_id:
        return {"error": "Invalid YouTube URL"}
    video_id = video_id.group(1)
    # 실제 환경에서는 YouTube API 연동 필요
    transcript = f"[유튜브 {video_id} transcript placeholder]"
    return {"transcript": transcript}
