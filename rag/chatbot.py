"""
담당: RAG팀
역할: KT 제품 브로슈어 기반 RAG 챗봇
      - 멀티턴 대화 지원
      - Hybrid Search (BM25 + FAISS) + Reranking
      - 스트리밍 응답
      - 페이지 번호 출처 표시
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage
from typing import List, Generator
from shared.llm import get_llm
from rag.retriever import get_hybrid_retriever


# 이전 대화를 고려해 검색용 독립 질문으로 재구성하는 프롬프트
CONDENSE_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "아래 대화 히스토리와 후속 질문을 보고, 후속 질문을 대화 맥락을 반영한 독립적인 질문으로 재구성하세요. "
     "재구성된 질문만 출력하세요."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# 최종 답변 생성 프롬프트
QA_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     """당신은 KT 제품 전문 상담 어시스턴트입니다.
아래 제공된 KT 제품 브로슈어 내용을 바탕으로 고객의 질문에 답변하세요.

규칙:
- 브로슈어에 없는 내용은 "해당 정보는 자료에서 확인되지 않습니다"라고 답하세요.
- 답변은 명확하고 간결하게 작성하세요.
- 관련 제품명을 반드시 언급하세요.
- 이전 대화 내용을 참고하여 맥락에 맞게 답변하세요.

[참고 자료]
{context}"""),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])


def _format_docs(docs: List[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


RAG_FAILURE_PHRASES = ["자료에서 확인되지 않습니다", "해당 정보는 자료에서"]

def is_rag_failure(answer: str) -> bool:
    return any(phrase in answer for phrase in RAG_FAILURE_PHRASES)

def _format_sources(docs: List[Document]) -> List[str]:
    """출처 파일명만 반환합니다 (중복 제거)."""
    seen = set()
    sources = []
    for doc in docs:
        filename = doc.metadata.get("source_file", "알 수 없음")
        if filename not in seen:
            seen.add(filename)
            sources.append(filename)
    return sources


def _to_lc_messages(history: list) -> list:
    """Gradio history → LangChain 메시지 리스트 변환.
    dict, ChatMessage 객체 등 Gradio 버전별 형식을 모두 처리합니다.
    """
    messages = []
    for item in history:
        if isinstance(item, dict):
            role = item.get("role", "")
            content = item.get("content", "")
        elif hasattr(item, "role"):          # Gradio ChatMessage 객체
            role = item.role
            content = item.content or ""
        else:
            continue

        if role == "user" and content:
            messages.append(HumanMessage(content=content))
        elif role == "assistant" and content:
            messages.append(AIMessage(content=content))

    return messages


def _get_search_query(query: str, chat_history: list, llm) -> str:
    """히스토리가 있으면 독립 질문으로 재구성합니다."""
    if not chat_history:
        return query
    condense_chain = CONDENSE_PROMPT | llm | StrOutputParser()
    return condense_chain.invoke({"input": query, "chat_history": chat_history})


def chat(query: str, history: list = None) -> dict:
    """질문과 대화 히스토리를 받아 RAG 응답을 반환합니다."""
    history = history or []
    chat_history = _to_lc_messages(history)
    llm = get_llm(temperature=0.0)

    # 1단계: 질문 재구성
    search_query = _get_search_query(query, chat_history, llm)

    # 2단계: Hybrid Search + Reranking
    retriever = get_hybrid_retriever(k=5)
    docs = retriever.invoke(search_query)

    # 3단계: 답변 생성
    qa_chain = QA_PROMPT | llm | StrOutputParser()
    answer = qa_chain.invoke({
        "input": query,
        "chat_history": chat_history,
        "context": _format_docs(docs),
    })

    return {
        "answer": answer,
        "sources": _format_sources(docs),
    }


def web_search_stream(query: str) -> Generator[str, None, None]:
    """DuckDuckGo 검색 후 LLM으로 요약해 스트리밍합니다."""
    from ddgs import DDGS

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
    except Exception:
        results = []

    if not results:
        yield "웹에서도 관련 정보를 찾을 수 없었습니다."
        return

    context = "\n\n".join(
        f"제목: {r['title']}\n내용: {r['body']}\n출처: {r.get('href', '')}"
        for r in results
    )

    WEB_PROMPT = ChatPromptTemplate.from_messages([
        ("system",
         """아래 웹 검색 결과를 참고하여 사용자의 질문에 답변하세요.
웹 검색 결과 기반의 답변임을 첫 줄에 명시하세요.
KT 기업 서비스와 관련된 내용을 중심으로 간결하게 정리하세요.

[웹 검색 결과]
{context}"""),
        ("human", "{question}"),
    ])

    llm = get_llm(temperature=0.0)
    chain = WEB_PROMPT | llm | StrOutputParser()
    accumulated = ""
    for chunk in chain.stream({"question": query, "context": context}):
        accumulated += chunk
        yield accumulated


def chat_stream(query: str, history: list = None) -> Generator[str, None, None]:
    """스트리밍 응답을 생성합니다. Gradio에서 글자 단위로 출력됩니다."""
    history = history or []
    chat_history = _to_lc_messages(history)
    llm = get_llm(temperature=0.0)

    # 1단계: 질문 재구성
    search_query = _get_search_query(query, chat_history, llm)

    # 2단계: Hybrid Search + Reranking
    retriever = get_hybrid_retriever(k=5)
    docs = retriever.invoke(search_query)

    # 3단계: 스트리밍 답변 생성
    qa_chain = QA_PROMPT | llm | StrOutputParser()
    accumulated = ""
    for chunk in qa_chain.stream({
        "input": query,
        "chat_history": chat_history,
        "context": _format_docs(docs),
    }):
        accumulated += chunk
        yield accumulated

    # 마지막에 출처 추가
    sources = _format_sources(docs)
    if sources:
        yield accumulated + f"\n\n📄 **참고 자료:** {', '.join(sources)}"
