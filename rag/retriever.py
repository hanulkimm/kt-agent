"""
담당: RAG팀
역할: Hybrid Search (BM25 + FAISS)
      - Flashrank 리랭커는 한국어 문서에서 역효과 → 제거
      - BM25(키워드) 40% + FAISS(의미) 60% 앙상블
"""
from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from typing import List
from rag.indexer import load_index


def get_hybrid_retriever(k: int = 5) -> EnsembleRetriever:
    """BM25 + FAISS 앙상블 리트리버를 반환합니다."""
    vectorstore = load_index()

    faiss_retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    all_docs = list(vectorstore.docstore._dict.values())
    bm25_retriever = BM25Retriever.from_documents(all_docs, k=k)

    return EnsembleRetriever(
        retrievers=[bm25_retriever, faiss_retriever],
        weights=[0.4, 0.6],
    )


def retrieve(query: str, k: int = 5) -> List[Document]:
    """질문과 관련된 KT 제품 문서를 Hybrid Search로 검색합니다."""
    return get_hybrid_retriever(k=k).invoke(query)
