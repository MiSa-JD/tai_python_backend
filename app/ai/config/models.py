from langchain_upstage import ChatUpstage
import os

analyzer = os.getenv("UPSTAGE_MODEL_ANALYZER")
validater = os.getenv("UPSTAGE_MODEL_VALIDATER")
summarizer = os.getenv("UPSTAGE_MODEL_SUMMARIZER")
classifier = os.getenv("UPSTAGE_MODEL_CLASSIFIER")

# 분석 모델
llm_analize = ChatUpstage(model=analyzer, temperature=0.7)

# 검증 모델
llm_validate = ChatUpstage(model=validater, temperature=0.7)

llm_summarize = ChatUpstage(model=summarizer, temperature=0.7)

llm_classify = ChatUpstage(model=classifier, temperature=0.7)

print("select models")
