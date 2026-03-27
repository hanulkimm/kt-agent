"""
담당: RAG팀
역할: data/ 폴더의 문서를 읽어서 FAISS 벡터 인덱스로 변환
"""
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from shared.config import DATA_DIR, FAISS_INDEX_DIR, OPENAI_API_KEY
import os


def build_index(pdf_dir: str = None) -> FAISS:
    """PDF 문서를 로드하고 FAISS 인덱스를 생성합니다."""
    pdf_dir = pdf_dir or os.path.join(DATA_DIR, "pdf")

    # TODO: 문서 로드
    docs = []
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            loader = PyMuPDFLoader(os.path.join(pdf_dir, filename))
            docs.extend(loader.load())

    # TODO: 청크 분할
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    # TODO: 임베딩 및 인덱스 저장
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(FAISS_INDEX_DIR)

    print(f"인덱스 생성 완료: {len(chunks)}개 청크")
    return vectorstore


def load_index() -> FAISS:
    """저장된 FAISS 인덱스를 로드합니다."""
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    return FAISS.load_local(FAISS_INDEX_DIR, embeddings, allow_dangerous_deserialization=True)


if __name__ == "__main__":
    build_index()
