"""
담당: 고객사 리서치팀
역할: 고객사 리서치 + KT B2B 상품 추천 Gradio UI
"""
import gradio as gr
from customer_research.researcher import search_company, search_company_news
from customer_research.profiler import build_profile
from customer_research.recommender import recommend_products


def run_research_and_recommend(company_name: str) -> tuple[str, str]:
    """고객사 분석 + KT B2B 상품 추천을 동시에 실행합니다."""
    company_name = company_name.strip()
    if not company_name:
        return "고객사명을 입력해주세요.", ""

    # 1. 고객사 정보 수집
    results = search_company(company_name)
    news = search_company_news(company_name)

    # 2. 고객사 프로파일 생성
    profile = build_profile(company_name, results, news)
    analysis = profile.summary or "분석 결과가 없습니다."

    # 3. KT B2B 상품 추천
    recommendation = recommend_products(company_name, analysis)

    return analysis, recommendation


def create_ui() -> gr.Blocks:
    with gr.Blocks() as demo:
        gr.Markdown(
            "## 고객사 리서치 + KT B2B 상품 추천\n"
            "고객사명을 입력하면 최신 동향을 분석하고, 적합한 KT B2B 상품을 추천합니다."
        )

        company_input = gr.Textbox(
            label="고객사명",
            placeholder="예: 삼성전자",
        )
        run_btn = gr.Button("분석 + 추천 시작", variant="primary")

        with gr.Row():
            with gr.Column():
                gr.Markdown("### 고객사 분석")
                analysis_output = gr.Markdown(label="고객사 분석 결과")
            with gr.Column():
                gr.Markdown("### KT B2B 추천 상품")
                recommendation_output = gr.Markdown(label="추천 결과")

        run_btn.click(
            fn=run_research_and_recommend,
            inputs=company_input,
            outputs=[analysis_output, recommendation_output],
        )

    return demo


if __name__ == "__main__":
    create_ui().launch()
