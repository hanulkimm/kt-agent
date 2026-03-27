"""
KT 리서치 에이전트 FastAPI 서버
"""
import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from rag.chatbot import chat_stream, chat, is_rag_failure, web_search_stream
from customer_research.researcher import search_company, search_company_news
from customer_research.profiler import build_profile
from customer_research.recommender import recommend_products
from market_research.researcher import search_market_by_product_and_industry, INDUSTRY_KEYWORDS
from market_research.summarizer import generate_market_report

app = FastAPI(title="KT 리서치 에이전트")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"


# ── 요청 모델 ──────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    history: List[dict] = []

class ProductRequest(BaseModel):
    product_id: str
    rag_query: str

class WebSearchRequest(BaseModel):
    query: str

class CustomerRequest(BaseModel):
    company_name: str

class MarketRequest(BaseModel):
    product_name: str
    industry: str


# ── 유틸 ───────────────────────────────────────────────────────────────────

def sse(data: dict) -> str:
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


# ── RAG / 상품 Q&A ─────────────────────────────────────────────────────────

@app.post("/api/chat/stream")
def api_chat_stream(req: ChatRequest):
    def generate():
        final_content = ""
        try:
            for chunk in chat_stream(req.message, req.history):
                final_content = chunk
                yield sse({"type": "token", "content": chunk})
            if is_rag_failure(final_content):
                yield sse({"type": "rag_failed"})
        except Exception as e:
            yield sse({"type": "error", "content": str(e)})
        finally:
            yield sse({"type": "done"})
    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/api/chat/websearch")
def api_websearch(req: WebSearchRequest):
    def generate():
        try:
            for chunk in web_search_stream(req.query):
                yield sse({"type": "token", "content": chunk})
        except Exception as e:
            yield sse({"type": "error", "content": str(e)})
        finally:
            yield sse({"type": "done"})
    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/api/product/detail")
def api_product_detail(req: ProductRequest):
    result = chat(req.rag_query, [])
    return {"answer": result["answer"], "sources": result["sources"]}


# ── 고객사 리서치 ──────────────────────────────────────────────────────────

@app.post("/api/customer/stream")
def api_customer_stream(req: CustomerRequest):
    def generate():
        try:
            yield sse({"type": "progress", "msg": "🔍 고객사 정보 검색 중...", "step": 1, "total": 3})
            results = search_company(req.company_name)
            news = search_company_news(req.company_name)

            yield sse({"type": "progress", "msg": "🧠 기업 현황 분석 중...", "step": 2, "total": 3})
            profile = build_profile(req.company_name, results, news)

            yield sse({"type": "progress", "msg": "💡 KT 상품 추천 생성 중...", "step": 3, "total": 3})
            recommendation = recommend_products(req.company_name, profile.summary or "")

            yield sse({
                "type": "result",
                "analysis": profile.summary or "",
                "recommendation": recommendation,
            })
        except Exception as e:
            yield sse({"type": "error", "content": str(e)})
        finally:
            yield sse({"type": "done"})
    return StreamingResponse(generate(), media_type="text/event-stream")


# ── 시장 동향 리서치 ───────────────────────────────────────────────────────

@app.get("/api/market/industries")
def api_industries():
    return {"industries": list(INDUSTRY_KEYWORDS.keys())}


@app.post("/api/market/stream")
def api_market_stream(req: MarketRequest):
    def generate():
        try:
            yield sse({"type": "progress", "msg": "🔍 시장 정보 검색 중...", "step": 1, "total": 2})
            results = search_market_by_product_and_industry(req.product_name, req.industry)

            yield sse({"type": "progress", "msg": "📊 보고서 생성 중...", "step": 2, "total": 2})
            report = generate_market_report(req.product_name, req.industry, results)

            yield sse({"type": "result", "report": report.model_dump()})
        except Exception as e:
            yield sse({"type": "error", "content": str(e)})
        finally:
            yield sse({"type": "done"})
    return StreamingResponse(generate(), media_type="text/event-stream")


# ── 프론트엔드 ─────────────────────────────────────────────────────────────

@app.get("/")
def serve_index():
    return FileResponse(FRONTEND_DIR / "index.html")

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
