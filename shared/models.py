from pydantic import BaseModel
from typing import Optional


class CustomerProfile(BaseModel):
    """고객사 프로파일 데이터 모델"""
    company_name: str
    industry: Optional[str] = None
    summary: Optional[str] = None
    key_challenges: Optional[list[str]] = None
    recent_news: Optional[list[str]] = None


class MarketReport(BaseModel):
    """시장 동향 리포트 데이터 모델"""
    topic: str
    product_name: Optional[str] = None
    industry: Optional[str] = None
    market_overview: Optional[str] = None
    summary: Optional[str] = None
    key_trends: Optional[list[str]] = None
    competitive_landscape: Optional[str] = None
    opportunities: Optional[list[str]] = None
    threats: Optional[list[str]] = None
    sources: Optional[list[str]] = None


class ChatMessage(BaseModel):
    """챗봇 메시지 모델"""
    role: str  # "user" | "assistant"
    content: str
