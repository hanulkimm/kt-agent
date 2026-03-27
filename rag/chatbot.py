"""
담당: RAG팀
역할: KT 제품 브로슈어 기반 RAG 챗봇 (멀티턴 대화 지원)
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage
from typing import List
from shared.llm import get_llm
from rag.indexer import load_index


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


def _to_lc_messages(history: list) -> list:
    """Gradio history (list of [user, assistant]) → LangChain 메시지 리스트 변환"""
    messages = []
    for user_msg, ai_msg in history:
        if user_msg:
            messages.append(HumanMessage(content=user_msg))
        if ai_msg:
            messages.append(AIMessage(content=ai_msg))
    return messages


def chat(query: str, history: list = None) -> dict:
    """
    질문과 대화 히스토리를 받아 RAG 응답을 반환합니다.

    Args:
        query: 현재 사용자 질문
        history: Gradio history 형식 [[user, assistant], ...]
    """
    history = history or []
    chat_history = _to_lc_messages(history)

    vectorstore = load_index()
    llm = get_llm(temperature=0.0)

    # 1단계: 히스토리가 있으면 독립 질문으로 재구성 (검색 품질 향상)
    if chat_history:
        condense_chain = CONDENSE_PROMPT | llm | StrOutputParser()
        search_query = condense_chain.invoke({
            "input": query,
            "chat_history": chat_history,
        })
    else:
        search_query = query

    # 2단계: 재구성된 질문으로 문서 검색
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(search_query)

    # 3단계: 히스토리 + 문서 + 질문으로 최종 답변 생성
    qa_chain = QA_PROMPT | llm | StrOutputParser()
    answer = qa_chain.invoke({
        "input": query,
        "chat_history": chat_history,
        "context": _format_docs(docs),
    })

    sources = list({
        doc.metadata.get("source_file", "알 수 없음")
        for doc in docs
    })

    return {
        "answer": answer,
        "sources": sources,
    }
