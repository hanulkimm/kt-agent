"""
담당: 고객사 리서치팀
역할: 고객사 프로파일 기반 KT B2B 상품 추천
"""
import json
from langchain_core.messages import HumanMessage
from shared.llm import get_llm
from customer_research.kt_products import KT_B2B_PRODUCTS


def recommend_products(company_name: str, company_summary: str) -> str:
    """고객사 분석 내용을 바탕으로 KT B2B 상품을 추천합니다."""
    llm = get_llm(temperature=0.2)

    catalog_text = "\n".join(
        f"[{p['id']}] {p['name']} ({p['category']})\n"
        f"  설명: {p['description']}\n"
        f"  활용사례: {', '.join(p['use_cases'])}"
        for p in KT_B2B_PRODUCTS
    )

    prompt = f"""당신은 KT B2B 영업 전문가입니다.
아래 고객사 분석 내용을 읽고, KT B2B 상품 카탈로그에서 이 고객사에 가장 적합한 상품을 추천해주세요.

## 고객사: {company_name}
{company_summary}

## KT B2B 상품 카탈로그
{catalog_text}

## 지시사항
- 고객사의 현황, 과제, 전략 방향과 연결되는 상품을 3~5개 선정하세요.
- 반드시 아래 JSON 배열 형식으로만 응답하세요 (마크다운 코드블록 없이 순수 JSON):

[
  {{
    "product_id": "상품 id",
    "product_name": "상품명",
    "reason": "이 고객사에 추천하는 구체적인 이유 (고객사 상황과 연결하여 2~3문장)",
    "talking_point": "영업 미팅에서 꺼낼 핵심 한 마디"
  }}
]
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    raw = response.content.strip()

    # JSON 파싱 시도
    try:
        # 코드블록 제거
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        recommendations = json.loads(raw.strip())
    except json.JSONDecodeError:
        # 파싱 실패 시 원문 반환
        return raw

    return _format_recommendations(company_name, recommendations)


def _format_recommendations(company_name: str, recommendations: list[dict]) -> str:
    # product_id → url 조회용 맵
    url_map = {p["id"]: p.get("url", "") for p in KT_B2B_PRODUCTS}

    lines = [f"## {company_name}을(를) 위한 KT B2B 추천 상품\n"]

    for i, rec in enumerate(recommendations, 1):
        pid = rec.get("product_id", "")
        name = rec.get("product_name", "")
        url = url_map.get(pid, "")
        title = f"[{name}]({url})" if url else name

        lines.append(f"### {i}. {title}")
        lines.append(f"**추천 이유:** {rec.get('reason', '')}")
        lines.append(f"**핵심 멘트:** _{rec.get('talking_point', '')}_")
        lines.append("")

    return "\n".join(lines)
