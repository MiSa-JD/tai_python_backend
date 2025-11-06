# 환경 변수 로드
from dotenv import load_dotenv
from langchain_teddynote import logging

load_dotenv(dotenv_path="../.env")

# 프로젝트 이름을 입력합니다.
logging.langsmith("tai_python")
