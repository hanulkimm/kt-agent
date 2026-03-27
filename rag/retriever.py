"""
담당: RAG팀
역할: Hybrid Search (BM25 + FAISS) + Reranking
"""
from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.document_compressors.flashrank_rerank import FlashrankRerank
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from typing import List
from rag.indexer import load_index


def get_hybrid_retriever(k: int = 10):
    """BM25 + FAISS 앙상블 리트리버를 반환합니다."""
    vectorstore = load_index()

    # FAISS 벡터 검색
    faiss_retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    # BM25 키워드 검색 (인덱스에서 전체 문서 추출)
    all_docs = list(vectorstore.docstore._dict.values())
    bm25_retriever = BM25Retriever.from_documents(all_docs, k=k)

    # 앙상블: BM25 40% + FAISS 60%
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, faiss_retriever],
        weights=[0.4, 0.6],
    )
    return ensemble_retriever


def get_reranked_retriever(k_fetch: int = 10, k_final: int = 5):
    """Hybrid Search 후 Flashrank로 재순위화하는 리트리버를 반환합니다."""
    ensemble_retriever = get_hybrid_retriever(k=k_fetch)

    reranker = FlashrankRerank(top_n=k_final)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=reranker,
        base_retriever=ensemble_retriever,
    )
    return compression_retriever


def retrieve(query: str, k: int = 5) -> List[Document]:
    """질문과 관련된 KT 제품 문서를 Hybrid + Reranking으로 검색합니다."""
    retriever = get_reranked_retriever(k_fetch=10, k_final=k)
    return retriever.invoke(query)
