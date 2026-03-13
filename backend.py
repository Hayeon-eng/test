from fastapi import FastAPI
from analyzer.insight_engine import *

app = FastAPI()


@app.post("/analyze")
def analyze(data: dict):

    text = data["text"]

    brands = brand_mentions(text)
    topics = topic_clusters(text)
    sentiment = brand_sentiment(text)
    citation = citation_probability(text)
    aeo = aeo_score(text)

    data_insight, content_insight = generate_insight()

    return {
        "data_perspective": data_insight,
        "content_perspective": content_insight,
        "brand_mentions": brands,
        "topic_clusters": topics,
        "brand_sentiment": sentiment,
        "citation_probability": citation,
        "aeo_score": aeo
    }
