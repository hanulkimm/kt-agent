"""
담당: 시장 동향팀
역할: 시장 동향 리서치 Gradio UI
"""
import gradio as gr
from market_research.researcher import (
    INDUSTRY_KEYWORDS,
    search_market_trends,
    search_market_by_product_and_industry,
)
from market_research.summarizer import summarize, generate_market_report

INDUSTRIES = list(INDUSTRY_KEYWORDS.keys())


def _format_report(report) -> str:
    lines = []

    lines.append(f"# 시장 동향 보고서")
    lines.append(f"**상품명:** {report.product_name}  |  **산업군:** {report.industry}\n")

    if report.market_overview:
        lines.append("## 1. 시장 개요")
        lines.append(report.market_overview)
        lines.append("")

    if report.key_trends:
        lines.append("## 2. 주요 트렌드")
        for t in report.key_trends:
            lines.append(f"- {t}")
        lines.append("")

    if report.competitive_landscape:
        lines.append("## 3. 경쟁 환경")
        lines.append(report.competitive_landscape)
        lines.append("")

    if report.opportunities:
        lines.append("## 4. 기회 요인")
        for o in report.opportunities:
            lines.append(f"- {o}")
        lines.append("")

    if report.threats:
        lines.append("## 5. 위협 및 리스크")
        for th in report.threats:
            lines.append(f"- {th}")
        lines.append("")

    if report.summary:
        lines.append("## 6. 시사점 및 전략적 제언")
        lines.append(report.summary)
        lines.append("")

    if report.sources:
        lines.append("## 참고 출처")
        for src in report.sources[:10]:
            lines.append(f"- {src}")

    return "\n".join(lines)


def run_research(product_name: str, industry: str) -> str:
    if not product_name.strip():
        return "상품명을 입력해주세요."
    if not industry:
        return "산업군을 선택해주세요."

    results = search_market_by_product_and_industry(product_name.strip(), industry)
    if not results:
        return "검색 결과가 없습니다. 다른 키워드나 산업군을 시도해보세요."

    report = generate_market_report(product_name.strip(), industry, results)
    return _format_report(report)


def create_ui() -> gr.Blocks:
    with gr.Blocks() as demo:
        gr.Markdown("## 시장 동향 리서치\n상품명과 산업군을 입력하면 AI가 시장 동향 보고서를 생성합니다.")

        with gr.Row():
            product_input = gr.Textbox(
                label="상품명",
                placeholder="예: AI 화상회의 솔루션",
                scale=2,
            )
            industry_input = gr.Dropdown(
                label="산업군",
                choices=INDUSTRIES,
                value=INDUSTRIES[0],
                scale=1,
            )

        run_btn = gr.Button("보고서 생성", variant="primary")
        output = gr.Markdown(label="시장 동향 보고서")

        run_btn.click(
            fn=run_research,
            inputs=[product_input, industry_input],
            outputs=output,
        )

    return demo


if __name__ == "__main__":
    create_ui().launch()
