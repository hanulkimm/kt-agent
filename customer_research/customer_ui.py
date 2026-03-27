"""
담당: 고객사 리서치팀
역할: 고객사 리서치 Gradio UI
"""
import gradio as gr
from customer_research.researcher import search_company, search_company_news
from customer_research.profiler import build_profile


def run_research(company_name: str) -> str:
    if not company_name.strip():
        return "고객사명을 입력해주세요."
    results = search_company(company_name)
    news = search_company_news(company_name)
    profile = build_profile(company_name, results, news)
    return profile.summary or "분석 결과가 없습니다."


def create_ui() -> gr.Blocks:
    with gr.Blocks() as demo:
        gr.Markdown("## 고객사 리서치")
        company_input = gr.Textbox(label="고객사명", placeholder="예: 삼성전자")
        run_btn = gr.Button("리서치 시작")
        output = gr.Textbox(label="분석 결과", lines=15)
        run_btn.click(fn=run_research, inputs=company_input, outputs=output)
    return demo


if __name__ == "__main__":
    create_ui().launch()
