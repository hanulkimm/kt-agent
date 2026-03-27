"""
KT 상품 탐색기 FastAPI 서버
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

app = FastAPI(title="KT 상품 탐색기")

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
    history: List[dict] = []   # [{"role": "user"|"assistant", "content": "..."}]

class ProductRequest(BaseModel):
    product_id: str
    rag_query: str

class WebSearchRequest(BaseModel):
    query: str


# ── API 엔드포인트 ──────────────────────────────────────────────────────────

@app.post("/api/chat/stream")
def api_chat_stream(req: ChatRequest):
    """스트리밍 채팅 (SSE). RAG 실패 시 rag_failed 이벤트 전송."""
    def generate():
        final_content = ""
        try:
            for chunk in chat_stream(req.message, req.history):
                final_content = chunk
                data = json.dumps({"type": "token", "content": chunk}, ensure_ascii=False)
                yield f"data: {data}\n\n"

            if is_rag_failure(final_content):
                yield f"data: {json.dumps({'type': 'rag_failed'})}\n\n"

        except Exception as e:
            err = json.dumps({"type": "error", "content": str(e)}, ensure_ascii=False)
            yield f"data: {err}\n\n"
        finally:
            yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/api/chat/websearch")
def api_websearch(req: WebSearchRequest):
    """웹 검색 후 LLM 요약 스트리밍 (SSE)."""
    def generate():
        try:
            for chunk in web_search_stream(req.query):
                data = json.dumps({"type": "token", "content": chunk}, ensure_ascii=False)
                yield f"data: {data}\n\n"
        except Exception as e:
            err = json.dumps({"type": "error", "content": str(e)}, ensure_ascii=False)
            yield f"data: {err}\n\n"
        finally:
            yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/api/product/detail")
def api_product_detail(req: ProductRequest):
    """상품 상세 정보 (RAG)"""
    result = chat(req.rag_query, [])
    return {"answer": result["answer"], "sources": result["sources"]}


# ── 정적 파일 & 프론트엔드 ──────────────────────────────────────────────────

@app.get("/")
def serve_index():
    return FileResponse(FRONTEND_DIR / "index.html")

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
