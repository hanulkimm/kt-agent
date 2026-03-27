import os
from dotenv import load_dotenv

load_dotenv()

# LLM
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMB_MODEL_NAME", "text-embedding-3-small")

# 검색 API (필요 시 사용)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# 데이터 경로
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
KT_PRODUCTS_DIR = os.path.join(DATA_DIR, "kt-products")
FAISS_INDEX_DIR = os.path.join(BASE_DIR, "faiss_index")
