"""
담당: 시장 동향팀
역할: 웹 검색으로 시장 동향 수집
"""
from ddgs import DDGS
from shared.models import MarketReport


INDUSTRY_KEYWORDS = {
    "IT/소프트웨어": ["IT 소프트웨어 시장", "SaaS 클라우드"],
    "반도체/전자": ["반도체 전자부품 시장", "메모리 파운드리"],
    "통신/네트워크": ["통신 네트워크 시장", "5G 6G 인프라"],
    "금융/핀테크": ["핀테크 금융 디지털", "인터넷은행 결제"],
    "의료/헬스케어": ["디지털헬스 의료기기 시장", "바이오 제약"],
    "제조/자동차": ["스마트제조 자동차 시장", "전기차 모빌리티"],
    "유통/이커머스": ["이커머스 유통 시장", "온라인쇼핑 물류"],
    "에너지/환경": ["신재생에너지 탄소중립 시장", "ESG 그린"],
    "식품/음료": ["식품 음료 시장", "푸드테크 HMR"],
    "교육/에듀테크": ["에듀테크 교육 시장", "이러닝 AI교육"],
    "부동산/건설": ["부동산 건설 시장", "스마트시티 건축"],
    "미디어/엔터테인먼트": ["미디어 콘텐츠 시장", "OTT 엔터테인먼트"],
}


def search_market_trends(topic: str, max_results: int = 10) -> list[dict]:
    """DuckDuckGo로 시장 동향 기사를 검색합니다."""
    with DDGS() as ddgs:
        results = list(ddgs.text(f"{topic} 시장 동향 2024 2025", max_results=max_results))
    return results


def search_market_by_product_and_industry(
    product_name: str,
    industry: str,
    max_results: int = 8,
) -> list[dict]:
    """상품명과 산업군을 조합해 시장 동향을 다각도로 검색합니다."""
    industry_hint = INDUSTRY_KEYWORDS.get(industry, [industry])

    queries = [
        f"{product_name} {industry} 시장 동향 2024 2025",
        f"{product_name} 시장 규모 성장률 전망",
        f"{industry} {industry_hint[0]} 트렌드 경쟁 현황",
        f"{product_name} 수요 고객 니즈 문제점",
    ]

    seen_urls: set[str] = set()
    all_results: list[dict] = []

    with DDGS() as ddgs:
        for query in queries:
            try:
                hits = list(ddgs.text(query, max_results=max_results))
                for hit in hits:
                    url = hit.get("href", "")
                    if url not in seen_urls:
                        seen_urls.add(url)
                        all_results.append(hit)
            except Exception:
                continue

    return all_results


def build_report(topic: str) -> MarketReport:
    """검색 결과를 기반으로 MarketReport 객체를 반환합니다."""
    results = search_market_trends(topic)
    return MarketReport(
        topic=topic,
        sources=[r.get("href", "") for r in results],
    )
