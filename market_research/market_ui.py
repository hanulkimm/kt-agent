"""
담당: 시장 동향팀
역할: 시장 동향 리서치 Gradio UI
"""
import gradio as gr
from market_research.researcher import search_market_trends
from market_research.summarizer import summarize


def run_research(topic: str) -> str:
    if not topic.strip():
        return "주제를 입력해주세요."
    results = search_market_trends(topic)
    report = summarize(topic, results)
    return report.summary or "요약 결과가 없습니다."


def create_ui() -> gr.Blocks:
    with gr.Blocks() as demo:
        gr.Markdown("## 시장 동향 리서치")
        topic_input = gr.Textbox(label="조사할 시장/주제", placeholder="예: 국내 클라우드 시장")
        run_btn = gr.Button("리서치 시작")
        output = gr.Textbox(label="리서치 결과", lines=15)
        run_btn.click(fn=run_research, inputs=topic_input, outputs=output)
    return demo


if __name__ == "__main__":
    create_ui().launch()
