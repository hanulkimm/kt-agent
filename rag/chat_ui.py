"""
담당: RAG팀
역할: KT 상품 탐색기 - 3탭 UI (카탈로그 / 니즈 탐색 / Q&A)
"""
import gradio as gr
from rag.chatbot import chat_stream, chat


# ── 상품 정의 (보유 브로슈어 8개) ────────────────────────────────────────────
PRODUCTS = [
    {
        "id": "cloudflex",
        "name": "KT cloudflex",
        "category": "클라우드",
        "emoji": "☁️",
        "tagline": "퍼블릭 클라우드 플랫폼",
        "rag_query": "KT cloudflex의 주요 기능, 특징, 요금제, 적합한 고객을 설명해줘",
    },
    {
        "id": "gpuaas",
        "name": "K GPUaaS",
        "category": "AI · GPU",
        "emoji": "🖥️",
        "tagline": "GPU 기반 AI 인프라 서비스",
        "rag_query": "K GPUaaS의 주요 기능, 스펙, 활용 사례, 적합한 고객을 설명해줘",
    },
    {
        "id": "ki_studio",
        "name": "K intelligence Studio",
        "category": "AI",
        "emoji": "🤖",
        "tagline": "AI 개발 · 운영 통합 플랫폼",
        "rag_query": "K intelligence Studio Cloud의 주요 기능, 특징, 적합한 고객을 설명해줘",
    },
    {
        "id": "5g_biz",
        "name": "KT 5G 업무망",
        "category": "5G · 네트워크",
        "emoji": "📡",
        "tagline": "기업 전용 5G 사설망",
        "rag_query": "KT 5G 업무망의 주요 기능, 특징, 도입 효과, 적합한 고객을 설명해줘",
    },
    {
        "id": "giga_office",
        "name": "KT GiGA Office",
        "category": "커뮤니케이션",
        "emoji": "🏢",
        "tagline": "기업 통합 커뮤니케이션",
        "rag_query": "KT GiGA Office의 주요 기능, 특징, 적합한 고객을 설명해줘",
    },
    {
        "id": "giga_energy",
        "name": "KT GiGA energy trade",
        "category": "비즈니스 솔루션",
        "emoji": "⚡",
        "tagline": "에너지 거래 플랫폼",
        "rag_query": "KT GiGA energy trade의 주요 기능, 특징, 도입 효과를 설명해줘",
    },
    {
        "id": "kornet",
        "name": "KT Kornet",
        "category": "인터넷 · 전용회선",
        "emoji": "🌐",
        "tagline": "기업 전용 인터넷 회선",
        "rag_query": "KT Kornet의 주요 기능, 특징, 속도, 적합한 고객을 설명해줘",
    },
    {
        "id": "secure_utm",
        "name": "KT Secure UTM",
        "category": "보안",
        "emoji": "🔒",
        "tagline": "통합 보안 위협 관리",
        "rag_query": "KT Secure UTM의 주요 기능, 보안 항목, 적합한 고객을 설명해줘",
    },
]

# KT 전체 상품 카테고리 (참고용 — 브로슈어 없는 상품 포함)
KT_FULL_CATALOG = {
    "AI · 빅데이터": ["AI Contact Center", "AI Robot", "AI Space", "K intelligence Studio ✅", "K GPUaaS ✅", "BigData 잘나가게"],
    "클라우드 · IDC": ["KT cloudflex ✅", "Managed Private Cloud", "IDC 코로케이션"],
    "인터넷 · 전용회선": ["KT Kornet ✅", "GiGA인터넷 기업형", "광전용회선"],
    "5G · 네트워크": ["KT 5G 업무망 ✅", "5G 스마트팩토리", "기업 5G"],
    "커뮤니케이션": ["KT GiGA Office ✅", "070 인터넷전화", "비즈메카"],
    "보안 · 안전": ["KT Secure UTM ✅", "DDoS 방어", "망분리 솔루션"],
    "비즈니스 솔루션": ["KT GiGA energy trade ✅", "콜센터 솔루션", "스마트 오피스"],
}

NEED_CHIPS = [
    ("🔒 보안", "사이버 보안 위협과 해킹을 막고 싶어요"),
    ("☁️ 클라우드", "온프레미스 서버를 클라우드로 이전하고 싶어요"),
    ("🤖 AI · GPU", "AI 모델 학습과 추론 인프라가 필요해요"),
    ("📡 5G 네트워크", "빠르고 안정적인 기업 전용 네트워크가 필요해요"),
    ("🏢 업무 협업", "임직원 커뮤니케이션과 협업 도구가 필요해요"),
    ("⚡ 에너지 관리", "에너지 사용량을 모니터링하고 절감하고 싶어요"),
]

# ── CSS ──────────────────────────────────────────────────────────────────────
CSS = """
body, .gradio-container {
    background: #f5f5f7 !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display",
                 "Helvetica Neue", sans-serif !important;
}

/* 헤더 */
.hero {
    background: linear-gradient(160deg, #1d1d1f 0%, #2d2d2f 100%);
    border-radius: 20px;
    padding: 40px 40px 32px;
    margin-bottom: 24px;
    text-align: center;
}
.hero h1 { font-size: 2.2rem; font-weight: 700; color: #f5f5f7;
           letter-spacing: -0.5px; margin: 0 0 8px 0; }
.hero p  { font-size: 1rem; color: #a1a1a6; margin: 0; }
.hero .badge {
    display: inline-block;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    color: #a1a1a6; font-size: 0.72rem;
    padding: 4px 12px; border-radius: 20px;
    margin-bottom: 14px; letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* 상품 카드 */
.product-card {
    background: #ffffff !important;
    border: 1.5px solid #e5e5ea !important;
    border-radius: 16px !important;
    padding: 20px 16px !important;
    text-align: left !important;
    font-size: 0.88rem !important;
    color: #1d1d1f !important;
    min-height: 110px !important;
    box-shadow: 0 1px 8px rgba(0,0,0,0.05) !important;
    transition: all 0.18s ease !important;
    white-space: pre-wrap !important;
    line-height: 1.6 !important;
}
.product-card:hover {
    border-color: #1d1d1f !important;
    box-shadow: 0 6px 24px rgba(0,0,0,0.12) !important;
    transform: translateY(-2px) !important;
}

/* 상세 패널 */
.detail-box {
    background: #ffffff;
    border-radius: 16px;
    border: 1.5px solid #e5e5ea;
    padding: 24px;
    min-height: 300px;
}

/* 니즈 탐색 */
.search-box {
    background: #ffffff;
    border-radius: 18px;
    padding: 28px 24px;
    border: 1.5px solid #e5e5ea;
    box-shadow: 0 1px 8px rgba(0,0,0,0.05);
}
.chip-btn {
    background: #f5f5f7 !important;
    border: 1.5px solid #e5e5ea !important;
    border-radius: 20px !important;
    padding: 6px 16px !important;
    font-size: 0.82rem !important;
    color: #1d1d1f !important;
    transition: all 0.15s !important;
}
.chip-btn:hover {
    background: #1d1d1f !important;
    color: #f5f5f7 !important;
    border-color: #1d1d1f !important;
}

/* Q&A 채팅 버블 */
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
#submit-btn {
    background: #1d1d1f !important; color: #f5f5f7 !important;
    border: none !important; border-radius: 12px !important;
    font-size: 0.9rem !important; font-weight: 500 !important;
}
#submit-btn:hover { opacity: 0.82 !important; }
.example-set .example {
    background: #ffffff !important; border: 1.5px solid #e5e5ea !important;
    border-radius: 12px !important; color: #1d1d1f !important;
    font-size: 0.85rem !important;
}
.example-set .example:hover {
    background: #1d1d1f !important; color: #f5f5f7 !important;
    border-color: #1d1d1f !important;
}

/* 탭 */
.tab-nav button { font-size: 0.9rem !important; font-weight: 500 !important; }

/* 전체 카탈로그 표 */
.catalog-table { font-size: 0.85rem; line-height: 1.8; }

/* 스크롤바 */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #d2d2d7; border-radius: 10px; }
"""

HERO_HTML = """
<div class="hero">
    <div class="badge">KT Enterprise</div>
    <h1>상품 탐색기</h1>
    <p>KT 상품을 찾고, 이해하고, 비교하세요</p>
</div>
"""


# ── 헬퍼 함수 ────────────────────────────────────────────────────────────────

def _card_label(p: dict) -> str:
    return f"{p['emoji']}  {p['name']}\n{p['category']}  ·  {p['tagline']}"


def get_product_detail(product_id: str) -> str:
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return "❌ 상품 정보를 찾을 수 없습니다."
    result = chat(product["rag_query"], [])
    answer = result.get("answer", "")
    sources = result.get("sources", [])
    if sources:
        answer += f"\n\n📄 **출처**: {' · '.join(sources)}"
    return f"## {product['emoji']} {product['name']}\n\n{answer}"


def search_by_need(need: str) -> str:
    if not need.strip():
        return ""
    query = (
        f"고객 니즈: \"{need}\"\n"
        "이 니즈에 적합한 KT 상품을 1~3개 추천하고, "
        "각 상품명과 함께 왜 적합한지 이유를 구체적으로 설명해줘."
    )
    result = chat(query, [])
    return result.get("answer", "")


def build_full_catalog_md() -> str:
    lines = ["## KT 전체 상품 카탈로그\n", "✅ = 브로슈어 보유 (클릭해서 탐색 가능)\n"]
    for category, products in KT_FULL_CATALOG.items():
        lines.append(f"\n**{category}**")
        for prod in products:
            lines.append(f"- {prod}")
    return "\n".join(lines)


def respond(message: str, history: list):
    if not message.strip():
        yield ""
        return
    yield from chat_stream(message, history)


# ── UI 생성 ──────────────────────────────────────────────────────────────────

def create_ui() -> gr.Blocks:
    with gr.Blocks(title="KT 상품 탐색기") as demo:
        gr.HTML(f"<style>{CSS}</style>")
        gr.HTML(HERO_HTML)

        with gr.Tabs():

            # ── Tab 1: 상품 카탈로그 ─────────────────────────────────────
            with gr.Tab("📦  상품 카탈로그"):
                with gr.Row():
                    # 왼쪽: 상품 카드 그리드
                    with gr.Column(scale=6):
                        gr.Markdown("### 브로슈어 보유 상품")
                        gr.Markdown("카드를 클릭하면 상품 상세 정보를 확인할 수 있습니다.")

                        card_btns = []
                        for row_start in range(0, len(PRODUCTS), 4):
                            with gr.Row():
                                for p in PRODUCTS[row_start : row_start + 4]:
                                    btn = gr.Button(
                                        _card_label(p),
                                        elem_classes="product-card",
                                    )
                                    card_btns.append((btn, p["id"]))

                    # 오른쪽: 상세 패널
                    with gr.Column(scale=4):
                        with gr.Group(elem_classes="detail-box"):
                            gr.Markdown("#### 상품 상세")
                            detail_md = gr.Markdown(
                                "← 왼쪽 카드를 클릭하면\n상세 정보가 여기에 표시됩니다."
                            )

                # 카드 클릭 → 상세 패널 업데이트
                for btn, pid in card_btns:
                    btn.click(
                        fn=lambda p=pid: get_product_detail(p),
                        outputs=detail_md,
                        show_progress="minimal",
                    )

                gr.Markdown("---")

                # KT 전체 카탈로그 참고
                with gr.Accordion("📋 KT 전체 상품 카탈로그 보기 (참고용)", open=False):
                    gr.Markdown(build_full_catalog_md(), elem_classes="catalog-table")

            # ── Tab 2: 니즈 탐색 ─────────────────────────────────────────
            with gr.Tab("🔍  니즈 탐색"):
                with gr.Column(elem_classes="search-box"):
                    gr.Markdown("### 어떤 것이 필요하세요?")
                    gr.Markdown(
                        "고객 상황이나 필요한 것을 자유롭게 입력하면 "
                        "적합한 KT 상품을 추천해드립니다."
                    )

                    need_input = gr.Textbox(
                        placeholder="예: 재택근무 보안이 걱정돼요 / AI 모델 학습 서버가 필요해요",
                        label="",
                        lines=2,
                    )

                    # 빠른 선택 칩 (2행 × 3개)
                    gr.Markdown("**빠른 선택**")
                    chip_btns = []
                    for row_start in range(0, len(NEED_CHIPS), 3):
                        with gr.Row():
                            for label, query in NEED_CHIPS[row_start : row_start + 3]:
                                cb = gr.Button(label, elem_classes="chip-btn", size="sm")
                                chip_btns.append((cb, query))

                    search_btn = gr.Button("탐색하기  →", variant="primary", size="lg")

                result_md = gr.Markdown(visible=False)

                def run_search(need: str):
                    answer = search_by_need(need)
                    if answer:
                        return gr.update(value=answer, visible=True)
                    return gr.update(visible=False)

                search_btn.click(fn=run_search, inputs=need_input, outputs=result_md)
                need_input.submit(fn=run_search, inputs=need_input, outputs=result_md)

                for cb, query in chip_btns:
                    cb.click(fn=lambda q=query: q, outputs=need_input).then(
                        fn=run_search, inputs=need_input, outputs=result_md
                    )

            # ── Tab 3: Q&A ───────────────────────────────────────────────
            with gr.Tab("💬  상품 Q&A"):
                gr.Markdown("### 상품에 대해 자유롭게 질문하세요")
                gr.Markdown("구체적인 스펙, 요금, 비교, 도입 방법 등 무엇이든 물어보세요.")
                gr.ChatInterface(
                    fn=respond,
                    submit_btn="전송",
                    examples=[
                        "KT cloudflex가 뭐야?",
                        "5G 업무망이랑 Kornet 차이가 뭐야?",
                        "보안 제품 뭐가 있어?",
                        "AI 개발 환경을 위한 상품 추천해줘",
                        "GPU 서비스 가격 알려줘",
                    ],
                )

    return demo


if __name__ == "__main__":
    create_ui().launch()
