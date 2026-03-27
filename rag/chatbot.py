"""
담당: RAG팀
역할: RAG 기반 챗봇 체인 구성
"""
from langchain_core.messages import HumanMessage
from shared.llm import get_llm
from rag.indexer import load_index


def chat(query: str) -> dict:
    """질문을 받아 RAG 응답을 반환합니다."""
    llm = get_llm(temperature=0.0)
    vectorstore = load_index()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    docs = retriever.invoke(query)
    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""다음 문서 내용을 참고하여 질문에 답변해주세요.

[문서 내용]
{context}

[질문]
{query}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return {
        "answer": response.content,
        "sources": [doc.metadata for doc in docs],
    }
