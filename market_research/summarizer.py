"""
담당: 시장 동향팀
역할: 수집된 시장 정보를 LLM으로 요약 및 인사이트 추출
"""
from shared.llm import get_llm
from shared.models import MarketReport
from langchain.schema import HumanMessage


def summarize(topic: str, raw_results: list[dict]) -> MarketReport:
    """검색 결과를 LLM으로 요약하여 MarketReport로 반환합니다."""
    llm = get_llm(temperature=0.3)

    # 검색 결과 텍스트 합치기
    context = "\n\n".join(
        f"제목: {r.get('title', '')}\n내용: {r.get('body', '')}"
        for r in raw_results[:8]
    )

    prompt = f"""다음은 '{topic}'에 관한 최신 뉴스/기사입니다.
아래 형식으로 정리해주세요:

1. 핵심 요약 (3~5문장)
2. 주요 트렌드 (bullet point 3~5개)

---
{context}
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    # TODO: 응답을 파싱해서 key_trends 분리
    return MarketReport(
        topic=topic,
        summary=response.content,
        sources=[r.get("href", "") for r in raw_results],
    )
