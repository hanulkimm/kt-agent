"""
담당: RAG팀
역할: RAG 챗봇 Gradio UI
"""
import gradio as gr
from rag.chatbot import chat


def respond(message: str, history: list) -> str:
    result = chat(message)
    return result["answer"]


def create_ui() -> gr.Blocks:
    with gr.Blocks() as demo:
        gr.Markdown("## 문서 기반 챗봇")
        gr.ChatInterface(fn=respond)
    return demo


if __name__ == "__main__":
    create_ui().launch()
