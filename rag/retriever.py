"""
담당: RAG팀
역할: FAISS 인덱스에서 관련 문서 검색
"""
from langchain_core.documents import Document
from typing import List
from rag.indexer import load_index


def retrieve(query: str, k: int = 5) -> List[Document]:
    """쿼리와 관련된 KT 제품 문서 청크를 반환합니다."""
    vectorstore = load_index()
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return retriever.invoke(query)
