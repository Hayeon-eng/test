# openai_config.py
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")  # Render 환경 변수 사용

def openai_api_call(persona_name, persona_desc, url):
    """
    RAG 기반 LLM 호출 예시
    persona_name: 이름
    persona_desc: 특성
    url: 분석 URL
    """
    prompt = f"""
    페르소나: {persona_name} ({persona_desc})
    URL: {url}
    해당 URL 콘텐츠를 분석하고, 페르소나 시각에서 의견, 반박, 토론 형태로 한 문단 생성
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role":"user","content":prompt}],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[Error LLM 호출]: {str(e)}"
