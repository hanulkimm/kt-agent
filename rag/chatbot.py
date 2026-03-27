"""
담당: RAG팀
역할: RAG 기반 챗봇 체인 구성
"""
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from shared.llm import get_llm
from rag.indexer import load_index


def get_rag_chain() -> RetrievalQA:
    """RAG 체인을 생성하여 반환합니다."""
    llm = get_llm(temperature=0.0)
    vectorstore = load_index()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )
    return chain


def chat(query: str) -> dict:
    """질문을 받아 RAG 응답을 반환합니다."""
    chain = get_rag_chain()
    result = chain.invoke({"query": query})
    return {
        "answer": result["result"],
        "sources": [doc.metadata for doc in result["source_documents"]],
    }
