import random
import re

BRANDS = ["samsung","apple","google","xiaomi"]

TOPICS = [
    "camera",
    "battery",
    "performance",
    "AI features",
    "price",
    "design"
]

POSITIVE = ["good","great","best","strong","impressive"]
NEGATIVE = ["bad","poor","weak","issue","problem"]


def brand_mentions(text):

    text = text.lower()

    result = {}

    for b in BRANDS:
        result[b] = text.count(b)

    return result


def topic_clusters(text):

    text = text.lower()

    clusters = {}

    for t in TOPICS:
        clusters[t] = text.count(t)

    return clusters


def brand_sentiment(text):

    text = text.lower()

    sentiment = {}

    for brand in BRANDS:

        score = 0

        for p in POSITIVE:
            if p in text:
                score += 1

        for n in NEGATIVE:
            if n in text:
                score -= 1

        sentiment[brand] = score

    return sentiment


def citation_probability(text):

    score = 50

    if "?" in text:
        score += 10

    if len(text) > 2000:
        score += 10

    if "how" in text or "why" in text:
        score += 10

    score += random.randint(-5,5)

    return max(0,min(score,100))


def aeo_score(text):

    score = 40

    topics = topic_clusters(text)

    if max(topics.values()) > 5:
        score += 15

    if "FAQ" in text:
        score += 10

    if "review" in text:
        score += 10

    score += random.randint(-5,5)

    return max(0,min(score,100))


def generate_insight():

    data_insight = """
현재 콘텐츠 데이터 구조는 스펙 중심 메타데이터에 편향되어 있다.
AI 검색 환경에서는 use-case 기반 entity가 더 중요한 신호로 작동한다.
camera나 battery 같은 topic entity는 있지만 상황 기반 데이터가 부족하다.
그래서 AI가 콘텐츠를 해석할 때 경험보다는 사양 중심으로 요약될 가능성이 높다.
"""

    content_insight = """
콘텐츠 흐름이 리뷰어 중심 구조로 만들어져 있다.
대부분 카메라 → 성능 → 가격 순서로 설명된다.
하지만 소비자 의사결정은 배터리 체감이나 발열 같은 실제 경험 요소가 더 중요하다.
콘텐츠 구조가 소비자 decision journey와 약간 어긋나 있다.
"""

    return data_insight, content_insight
