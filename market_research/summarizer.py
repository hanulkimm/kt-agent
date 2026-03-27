"""
담당: 시장 동향팀
역할: 수집된 시장 정보를 LLM으로 요약 및 인사이트 추출
"""
import re
from shared.llm import get_llm
from shared.models import MarketReport
from langchain_core.messages import HumanMessage


def summarize(topic: str, raw_results: list[dict]) -> MarketReport:
    """검색 결과를 LLM으로 요약하여 MarketReport로 반환합니다."""
    llm = get_llm(temperature=0.3)

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

    return MarketReport(
        topic=topic,
        summary=response.content,
        sources=[r.get("href", "") for r in raw_results],
    )


def generate_market_report(
    product_name: str,
    industry: str,
    raw_results: list[dict],
) -> MarketReport:
    """상품명과 산업군 기반으로 구조화된 시장 동향 보고서를 생성합니다."""
    llm = get_llm(temperature=0.3)

    context = "\n\n".join(
        f"[{i+1}] 제목: {r.get('title', '')}\n내용: {r.get('body', '')}"
        for i, r in enumerate(raw_results[:12])
    )

    prompt = f"""당신은 전문 시장 조사 애널리스트입니다.
아래 수집된 최신 뉴스·기사를 바탕으로, '{product_name}' 상품의 '{industry}' 산업 내 시장 동향 보고서를 작성하세요.

반드시 다음 섹션 형식을 지켜 작성하세요 (각 섹션 제목은 그대로 사용):

## 1. 시장 개요
(시장 규모, 성장률, 전반적인 시장 상황을 3~5문장으로 서술)

## 2. 주요 트렌드
- (트렌드 1)
- (트렌드 2)
- (트렌드 3)
- (트렌드 4, 필요시)
- (트렌드 5, 필요시)

## 3. 경쟁 환경
(주요 경쟁사, 시장 점유율 구도, 차별화 요소를 3~4문장으로 서술)

## 4. 기회 요인
- (기회 1)
- (기회 2)
- (기회 3)

## 5. 위협 및 리스크
- (위협 1)
- (위협 2)
- (위협 3)

## 6. 시사점 및 전략적 제언
('{product_name}'을 판매·제안할 때 활용할 수 있는 핵심 인사이트 3~5문장)

---
[참고 기사]
{context}
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content

    # 섹션별 파싱
    def extract_section(text: str, header: str) -> str:
        pattern = rf"## {re.escape(header)}\n(.*?)(?=\n## |\Z)"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ""

    def extract_bullets(text: str) -> list[str]:
        lines = [ln.lstrip("-•* ").strip() for ln in text.splitlines() if ln.strip().startswith(("-", "•", "*"))]
        return [ln for ln in lines if ln]

    market_overview = extract_section(content, "1. 시장 개요")
    trends_raw = extract_section(content, "2. 주요 트렌드")
    key_trends = extract_bullets(trends_raw)
    competitive_landscape = extract_section(content, "3. 경쟁 환경")
    opp_raw = extract_section(content, "4. 기회 요인")
    opportunities = extract_bullets(opp_raw)
    threat_raw = extract_section(content, "5. 위협 및 리스크")
    threats = extract_bullets(threat_raw)
    summary = extract_section(content, "6. 시사점 및 전략적 제언")

    return MarketReport(
        topic=f"{product_name} / {industry}",
        product_name=product_name,
        industry=industry,
        market_overview=market_overview,
        key_trends=key_trends,
        competitive_landscape=competitive_landscape,
        opportunities=opportunities,
        threats=threats,
        summary=summary or content,
        sources=[r.get("href", "") for r in raw_results if r.get("href")],
    )
