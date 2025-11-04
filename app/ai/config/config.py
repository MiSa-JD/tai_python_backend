from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_upstage import UpstageEmbeddings
from langchain_chroma import Chroma

# 스플리터 정의
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)

# 임베딩 모델 설정
vstore = Chroma(
    collection_name="knowledge_base",
    embedding_function=UpstageEmbeddings(model="embedding-query"),
    persist_directory="../chroma",
)

# 검색자
retriever = vstore.as_retriever(
    search_type="mmr", search_kwargs={"k": 4, "fetch_k": 20, "lambda_mult": 0.5}
)

# 연관 되어있는 것으로 볼 범위
THRESHOLD = 1.55

print("configurate RAG settings")
