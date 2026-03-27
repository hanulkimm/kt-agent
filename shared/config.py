import os
from dotenv import load_dotenv

load_dotenv()

# LLM
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# 검색 API (필요 시 사용)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# 데이터 경로
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
FAISS_INDEX_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "faiss_index")
