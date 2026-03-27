"""
담당: 고객사 리서치팀
역할: 수집된 정보를 LLM으로 분석하여 고객사 프로파일 생성
"""
from shared.llm import get_llm
from shared.models import CustomerProfile
from langchain.schema import HumanMessage


def build_profile(company_name: str, raw_results: list[dict], news: list[dict] = None) -> CustomerProfile:
    """검색 결과를 분석하여 고객사 프로파일을 생성합니다."""
    llm = get_llm(temperature=0.3)

    context = "\n\n".join(
        f"제목: {r.get('title', '')}\n내용: {r.get('body', '')}"
        for r in raw_results[:8]
    )

    news_context = ""
    if news:
        news_context = "\n[최신 뉴스]\n" + "\n".join(
            f"- {n.get('title', '')}" for n in news
        )

    prompt = f"""다음은 '{company_name}'에 대한 정보입니다.
아래 항목을 분석해서 정리해주세요:

1. 기업 개요 (업종, 주요 사업)
2. 현재 주요 과제 및 니즈
3. 최근 이슈/동향 (bullet point)
4. 미팅 시 활용할 수 있는 인사이트

---
{context}
{news_context}
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    # TODO: 응답 파싱으로 각 필드 세분화
    return CustomerProfile(
        company_name=company_name,
        summary=response.content,
        recent_news=[n.get("title", "") for n in (news or [])],
    )
