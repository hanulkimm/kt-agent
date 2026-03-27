"""
담당: RAG팀
역할: KT 제품 RAG 챗봇 Gradio UI (Apple 스타일)
"""
import gradio as gr
from rag.chatbot import chat_stream


CSS = """
/* ── 전체 배경 ── */
body, .gradio-container {
    background: #f5f5f7 !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", sans-serif !important;
}

/* ── 히어로 헤더 ── */
.hero {
    background: linear-gradient(160deg, #1d1d1f 0%, #2d2d2f 100%);
    border-radius: 20px;
    padding: 48px 40px 40px;
    margin-bottom: 24px;
    text-align: center;
}
.hero h1 {
    font-size: 2.4rem;
    font-weight: 700;
    color: #f5f5f7;
    letter-spacing: -0.5px;
    margin: 0 0 10px 0;
}
.hero p {
    font-size: 1.05rem;
    color: #a1a1a6;
    margin: 0;
    font-weight: 400;
}
.hero .badge {
    display: inline-block;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    color: #a1a1a6;
    font-size: 0.75rem;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 16px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ── 채팅 영역 카드 ── */
.chat-card {
    background: #ffffff;
    border-radius: 18px;
    box-shadow: 0 2px 20px rgba(0,0,0,0.07);
    overflow: hidden;
}

/* ── 메시지 버블 ── */
.message.user {
    background: #1d1d1f !important;
    color: #f5f5f7 !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 12px 16px !important;
    font-size: 0.95rem !important;
}
.message.bot {
    background: #ffffff !important;
    color: #1d1d1f !important;
    border: 1px solid #e5e5ea !important;
    border-radius: 18px 18px 18px 4px !important;
    padding: 12px 16px !important;
    font-size: 0.95rem !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05) !important;
}

/* ── 입력창 ── */
.message-input-stretch textarea {
    border-radius: 14px !important;
    border: 1.5px solid #d2d2d7 !important;
    background: #ffffff !important;
    font-size: 0.95rem !important;
    padding: 12px 16px !important;
    transition: border-color 0.2s !important;
    box-shadow: none !important;
}
.message-input-stretch textarea:focus {
    border-color: #1d1d1f !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(29,29,31,0.08) !important;
}

/* ── 전송 버튼 ── */
#submit-btn {
    background: #1d1d1f !important;
    color: #f5f5f7 !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    padding: 10px 22px !important;
    transition: opacity 0.15s !important;
}
#submit-btn:hover { opacity: 0.82 !important; }

/* ── 예시 버튼 ── */
.example-set .example {
    background: #ffffff !important;
    border: 1.5px solid #e5e5ea !important;
    border-radius: 12px !important;
    color: #1d1d1f !important;
    font-size: 0.85rem !important;
    padding: 8px 14px !important;
    transition: all 0.15s !important;
}
.example-set .example:hover {
    background: #1d1d1f !important;
    color: #f5f5f7 !important;
    border-color: #1d1d1f !important;
}

/* ── 기능 뱃지 행 ── */
.feature-row {
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 20px;
}
.feature-chip {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    color: #a1a1a6;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.78rem;
}

/* ── 스크롤바 ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #d2d2d7; border-radius: 10px; }
"""

HERO_HTML = """
<div class="hero">
    <div class="badge">KT Enterprise AI</div>
    <h1>제품 상담 어시스턴트</h1>
    <p>KT 제품 브로슈어를 기반으로 정확한 정보를 제공합니다</p>
    <div class="feature-row">
        <span class="feature-chip">Hybrid Search</span>
        <span class="feature-chip">AI Reranking</span>
        <span class="feature-chip">멀티턴 대화</span>
        <span class="feature-chip">출처 페이지 표시</span>
    </div>
</div>
"""


def respond(message: str, history: list):
    if not message.strip():
        yield ""
        return
    yield from chat_stream(message, history)


def create_ui() -> gr.Blocks:
    with gr.Blocks(title="KT 제품 상담 어시스턴트") as demo:
        gr.HTML(f"<style>{CSS}</style>")
        gr.HTML(HERO_HTML)

        with gr.Group(elem_classes="chat-card"):
            gr.ChatInterface(
                fn=respond,
                submit_btn="전송",
                examples=[
                    "KT cloudflex가 뭐야?",
                    "5G 업무망 특징이 뭐야?",
                    "GPU 서비스 관련 제품 알려줘",
                    "보안 관련 제품 뭐가 있어?",
                    "KT Kornet과 GiGA Office 차이점은?",
                ],
            )
    return demo


if __name__ == "__main__":
    create_ui().launch()
