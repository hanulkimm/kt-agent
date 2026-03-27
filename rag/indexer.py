"""
담당: RAG팀
역할: data/kt-products/ 의 PDF 브로슈어를 읽어서 FAISS 벡터 인덱스로 변환
"""
import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from shared.config import KT_PRODUCTS_DIR, FAISS_INDEX_DIR
from shared.llm import get_embeddings


def build_index() -> FAISS:
    """kt-products/ 폴더의 PDF를 로드하고 FAISS 인덱스를 생성합니다."""
    docs = []
    pdf_files = [f for f in os.listdir(KT_PRODUCTS_DIR) if f.endswith(".pdf")]

    print(f"PDF 파일 {len(pdf_files)}개 로드 중...")
    for filename in pdf_files:
        path = os.path.join(KT_PRODUCTS_DIR, filename)
        loader = PyMuPDFLoader(path)
        loaded = loader.load()
        # 파일명을 메타데이터에 저장 (출처 표시용)
        for doc in loaded:
            doc.metadata["source_file"] = filename
        docs.extend(loaded)
        print(f"  완료: {filename} ({len(loaded)}페이지)")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " "],
    )
    chunks = splitter.split_documents(docs)
    print(f"\n총 {len(chunks)}개 청크 생성 완료")

    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    os.makedirs(FAISS_INDEX_DIR, exist_ok=True)
    vectorstore.save_local(FAISS_INDEX_DIR)
    print(f"인덱스 저장 완료: {FAISS_INDEX_DIR}")
    return vectorstore


def load_index() -> FAISS:
    """저장된 FAISS 인덱스를 로드합니다."""
    if not os.path.exists(FAISS_INDEX_DIR):
        print("인덱스가 없습니다. 먼저 build_index()를 실행하세요.")
        return build_index()
    return FAISS.load_local(FAISS_INDEX_DIR, get_embeddings(), allow_dangerous_deserialization=True)


if __name__ == "__main__":
    build_index()
