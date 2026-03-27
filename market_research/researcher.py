"""
담당: 시장 동향팀
역할: 웹 검색으로 시장 동향 수집
"""
from duckduckgo_search import DDGS
from shared.models import MarketReport


def search_market_trends(topic: str, max_results: int = 10) -> list[dict]:
    """DuckDuckGo로 시장 동향 기사를 검색합니다."""
    with DDGS() as ddgs:
        results = list(ddgs.text(f"{topic} 시장 동향 2024 2025", max_results=max_results))
    return results


def build_report(topic: str) -> MarketReport:
    """검색 결과를 기반으로 MarketReport 객체를 반환합니다."""
    results = search_market_trends(topic)

    # TODO: summarizer.py의 summarize() 호출로 요약 추가
    return MarketReport(
        topic=topic,
        sources=[r.get("href", "") for r in results],
    )
