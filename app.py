"""
메인 앱: 세 모듈을 Gradio 탭으로 통합
팀원들이 각자 UI 파일(chat_ui.py, market_ui.py, customer_ui.py)을 완성하면
이 파일에서 자동으로 통합됩니다.
"""
import gradio as gr
from rag.chat_ui import create_ui as rag_ui
from market_research.market_ui import create_ui as market_ui
from customer_research.customer_ui import create_ui as customer_ui


with gr.Blocks(title="선제안 고객 미팅 리서치 에이전트") as app:
    gr.Markdown("# 선제안 고객 미팅 리서치 에이전트")

    with gr.Tabs():
        with gr.TabItem("문서 챗봇 (RAG)"):
            rag_ui().render()

        with gr.TabItem("시장 동향 리서치"):
            market_ui().render()

        with gr.TabItem("고객사 리서치"):
            customer_ui().render()


if __name__ == "__main__":
    app.launch()
