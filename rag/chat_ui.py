"""
담당: RAG팀
역할: KT 제품 RAG 챗봇 Gradio UI
"""
import gradio as gr
from rag.chatbot import chat


def respond(message: str, history: list) -> str:
    if not message.strip():
        return ""
    result = chat(message)
    answer = result["answer"]
    sources = result["sources"]
    if sources:
        answer += f"\n\n📄 **참고 자료:** {', '.join(sources)}"
    return answer


def create_ui() -> gr.Blocks:
    with gr.Blocks() as demo:
        gr.Markdown("## KT 제품 문서 챗봇")
        gr.Markdown("KT 제품 브로슈어를 기반으로 질문에 답변합니다.")
        gr.ChatInterface(
            fn=respond,
            examples=[
                "KT cloudflex가 뭐야?",
                "5G 업무망 특징이 뭐야?",
                "GPU 서비스 관련 제품 알려줘",
            ],
        )
    return demo


if __name__ == "__main__":
    create_ui().launch()
