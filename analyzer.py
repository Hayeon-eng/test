from typing import Dict, Any

def analyze_content(content: str, persona: Dict[str,str]) -> Dict[str, Any]:
    """
    - 데이터 관점 인사이트
    - 콘텐츠 관점 인사이트
    - 브랜드 언급 / sentiment
    - 토픽 클러스터
    - AI citation probability
    - AEO score
    - 댓글 감정/키워드/요약
    - 할루시네이션 방지
    """
    prompt = f"""
    Persona: {persona['name']} ({persona['trait']})
    Analyze content strictly without hallucination.
    Provide:
    1. Data insights (schema/meta/Htags)
    2. Content summary (human-like)
    3. Brand mentions & sentiment
    4. Topic clusters
    5. AI citation probability
    6. AEO score
    """

    # 테스트 모드 / 과금 없이 동작
    result = {
        "data_insights": "[TEST] Schema/Meta/Htags 분석 예시",
        "content_summary": "[TEST] 사람 말하듯 요약 예시",
        "brand_mentions": ["BrandA", "BrandB"],
        "brand_sentiment": {"BrandA": "Positive", "BrandB": "Neutral"},
        "topic_clusters": ["Topic1", "Topic2"],
        "ai_citation_probability": 0.85,
        "aeo_score": 0.75
    }
    return result

def analyze_comments(comments: list) -> list:
    """
    각 댓글에 대해 감정/키워드/요약 추가
    """
    analyzed = []
    for c in comments:
        analyzed.append({
            "text": c,
            "sentiment": "Positive" if "좋" in c else "Neutral",
            "keywords": [w for w in c.split() if len(w)>1],
            "summary": c[:20] + "..." if len(c)>20 else c
        })
    return analyzed
