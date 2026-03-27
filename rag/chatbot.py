"""
담당: RAG팀
역할: KT 제품 브로슈어 기반 RAG 챗봇 (LangChain LCEL 방식)
"""
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from typing import List
from shared.llm import get_llm
from rag.indexer import load_index


PROMPT_TEMPLATE = """당신은 KT 제품 전문 상담 어시스턴트입니다.
아래 제공된 KT 제품 브로슈어 내용을 바탕으로 고객의 질문에 답변하세요.

규칙:
- 브로슈어에 없는 내용은 "해당 정보는 자료에서 확인되지 않습니다"라고 답하세요.
- 답변은 명확하고 간결하게 작성하세요.
- 관련 제품명을 반드시 언급하세요.

[참고 자료]
{context}

[질문]
{question}

[답변]"""

PROMPT = PromptTemplate(
    template=PROMPT_TEMPLATE,
    input_variables=["context", "question"],
)


def _format_docs(docs: List[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def chat(query: str) -> dict:
    """질문을 받아 KT 제품 기반 RAG 응답을 반환합니다."""
    vectorstore = load_index()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    llm = get_llm(temperature=0.0)

    # 문서 검색
    docs = retriever.invoke(query)

    # LCEL 체인
    chain = (
        {"context": lambda _: _format_docs(docs), "question": RunnablePassthrough()}
        | PROMPT
        | llm
        | StrOutputParser()
    )

    answer = chain.invoke(query)

    # 출처 파일명 중복 제거
    sources = list({
        doc.metadata.get("source_file", "알 수 없음")
        for doc in docs
    })

    return {
        "answer": answer,
        "sources": sources,
    }
