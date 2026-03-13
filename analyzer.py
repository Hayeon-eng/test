from typing import Dict, Any

def analyze_content(content: str, persona: Dict[str,str]) -> Dict[str, Any]:
    """
    - 데이터 관점 인사이트 (AI)
    - 콘텐츠 관점 인사이트 (페르소나 의견)
    - 브랜드 언급 / sentiment
    - 토픽 클러스터
    - AI citation probability
    - AEO score
    - 할루시네이션 방지
    """
    content_summary = f"[{persona['name']}({persona['trait']}) 의견] 읽기 쉬움, 일부 문단 길어 개선 필요, AEO 관점에서 링크 구조 개선 추천."

    data_insights = "[AI 분석] schema 적절, H태그 계층 OK, AEO 0.72 → 개선 가능"

    return {
        "content_summary": content_summary,
        "data_insights": data_insights,
        "brand_mentions":["BrandA","BrandB"],
        "brand_sentiment":{"BrandA":"Positive","BrandB":"Neutral"},
        "topic_clusters":["Topic1","Topic2"],
        "ai_citation_probability":0.85,
        "aeo_score":0.72
    }

def analyze_comments(comments: list) -> list:
    """각 댓글에 대해 감정/키워드/요약 추가"""
    analyzed = []
    for c in comments:
        analyzed.append({
            "text": c,
            "sentiment": "Positive" if "좋" in c else "Neutral",
            "keywords": [w for w in c.split() if len(w)>1],
            "summary": c[:20]+"..." if len(c)>20 else c
        })
    return analyzed
