from langchain_openai import ChatOpenAI
from shared.config import OPENAI_API_KEY, OPENAI_MODEL


def get_llm(temperature: float = 0.0) -> ChatOpenAI:
    """공통 LLM 인스턴스 반환. 모든 모듈에서 이 함수를 사용하세요."""
    return ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=temperature,
        api_key=OPENAI_API_KEY,
    )
