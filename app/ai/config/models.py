from langchain_upstage import ChatUpstage

# 분석 모델
llm_analize = ChatUpstage(
    model="solar-mini",
    temperature=0.7,
)

# 검증 모델
llm_validate = ChatUpstage(model="solar-pro2", temperature=0.7)

llm_summarize = ChatUpstage(model="solar-mini", temperature=0.7)

llm_classify = ChatUpstage(model="solar-mini", temperature=0.7)

print("select models")
