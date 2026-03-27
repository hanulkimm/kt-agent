"""
담당: RAG팀
역할: KT 제품 RAG 챗봇 Gradio UI (스트리밍 + 멀티턴)
"""
import gradio as gr
from rag.chatbot import chat_stream


def respond(message: str, history: list):
    """스트리밍 응답 생성기. Gradio가 yield된 값을 실시간으로 표시합니다."""
    if not message.strip():
        yield ""
        return
    yield from chat_stream(message, history)


def create_ui() -> gr.Blocks:
    with gr.Blocks() as demo:
        gr.Markdown("## KT 제품 문서 챗봇")
        gr.Markdown("KT 제품 브로슈어를 기반으로 질문에 답변합니다. 이전 대화를 기억합니다.")
        gr.ChatInterface(
            fn=respond,
            examples=[
                "KT cloudflex가 뭐야?",
                "5G 업무망 특징이 뭐야?",
                "GPU 서비스 관련 제품 알려줘",
                "보안 관련 제품 뭐가 있어?",
            ],
        )
    return demo


if __name__ == "__main__":
    create_ui().launch()
