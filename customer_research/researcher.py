"""
담당: 고객사 리서치팀
역할: 고객사 관련 정보 웹 검색 수집
"""
from duckduckgo_search import DDGS


def search_company(company_name: str, max_results: int = 10) -> list[dict]:
    """고객사 관련 최신 뉴스/정보를 검색합니다."""
    with DDGS() as ddgs:
        results = list(ddgs.text(f"{company_name} 기업 현황 사업 전략 2024 2025", max_results=max_results))
    return results


def search_company_news(company_name: str, max_results: int = 5) -> list[dict]:
    """고객사 최신 뉴스를 검색합니다."""
    with DDGS() as ddgs:
        results = list(ddgs.news(company_name, max_results=max_results))
    return results
