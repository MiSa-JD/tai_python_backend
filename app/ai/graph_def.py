from langchain.schema import Document
from app.classes.responses import SearchResult
from app.crawler.crawling import news_crawling
from app.ai.rag_functions import embed_documents, search_documents
from app.ai.llm_caller import validator_llm, analyst_llm, classifier_llm, summarizer_llm
import json

# 상태 정의
State = {
    "keyword": str,  # 분석 대상 키워드
    "raw_documents": [
        SearchResult
    ],  # 크롤링/뉴스 등 원문 문서들 (content, link, source 등)
    "embedded_documents": [dict],  # 임베딩 후 VDB에 저장된 문서 메타
    "retrieved_documents": [Document],  # VDB에서 keyword 기반으로 가져온 후보 문서들
    "validated_documents": [
        Document
    ],  # 키워드와 실제로 관련 있다고 LLM이 yes 준 문서들
    "news_summaries": [str],  # 뉴스 개별 요약 결과들
    "trend_analysis": dict,  # 트렌드 원인 분석 (LLM 결과: answer + link[])
    "summarize_and_classify": dict,  # 최종 JSON (keyword, description, content, tags, category, refered)
}


# 노드 정의
# 데이터 수집 부분
def collect_sources(state):
    print(f"데이터 수집 중: {state['keyword']}")
    # 1) keyword로 외부 소스 크롤링
    fetched_docs = news_crawling(state["keyword"])
    # 2) 결과를 [{"keyword": ..., "link": ..., "content": ...}, ...] 형태로 수집
    state["raw_documents"] = fetched_docs
    return state


# 데이터 임베딩
def embed_and_store(state):
    print("수집한 문서 임베딩 중")
    # 문서별 embedding 계산 -> VDB에 저장
    raws = state.get("raw_documents", [])
    if len(raws) == 0:
        return state
    docs = embed_documents(raws)
    # 저장 후, vector_id 등 메타 정리
    # 저장 결과 출력
    state["embedded_documents"] = docs
    return state


# VDB에서 Retrieve
def retrieve_from_vdb(state):
    print("데이터 검색 중")
    retrieved = search_documents(state["keyword"])
    state["retrieved_documents"] = (
        retrieved  # 예: [{"content":..., "link":..., ...}, ...]
    )
    return state


# 각 문서 검증
def validate_relevance(state):
    print("각 문서 검증")
    validated = []
    if len(state.get("retrieved_documents", [])) == 0:
        return state
    for doc in state["retrieved_documents"]:
        raw = validator_llm(keyword=state["keyword"], prompt=doc.page_content)
        judgment = json.loads(raw)
        if judgment["validation"] == "yes":
            validated.append(
                Document(
                    page_content=doc.page_content,
                    metadata={**doc.metadata, "reason": judgment["reason"]},
                )
            )
    state["validated_documents"] = validated
    return state


# 원문 요약
def summarize_news_individual(state):
    print("원문 요약 중")
    summaries = []
    for doc in state.get("raw_documents", []):
        summary = summarizer_llm(doc["content"])
        summaries.append({"link": doc["link"], "summary": summary})
    state["news_summaries"] = summaries
    return state


# 분석 및 이유 작성
def analyze_trend_reason(state):
    print("결론 요약본 생성 중")
    raw = analyst_llm(
        keyword=state["keyword"],
        docs=state.get("validated_documents", []),
        summaries=state.get("news_summaries", []),
    )
    trend_json = json.loads(raw)
    state["trend_analysis"] = trend_json  # {"answer": "...", "link": ["...", "..."]}
    return state


# 태그, 카테고리 붙이기
def classify_and_package(state):
    print("태그, 카테고리 붙이는 중 ")
    packaged = classifier_llm(
        prompt=state["trend_analysis"]["answer"],
    )
    state["summarize_and_classify"] = packaged
    return state
