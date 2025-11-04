from langchain.schema import Document
from app.classes.ai import GraphState
from app.crawler.crawling import news_crawling
from app.ai.rag_functions import embed_documents, search_documents
from app.ai.llm_caller import validator_llm, analyst_llm, classifier_llm, summarizer_llm
import json


# 노드 정의
# 진입 노드
async def entry_node(state: GraphState) -> GraphState:
    print(f"과정 시작: {state['keyword']} | ")
    return {}


# 데이터 수집 부분
async def collect_sources(state: GraphState) -> GraphState:
    print(f"데이터 수집 중: {state['keyword']} | ")
    # 1) keyword로 외부 소스 크롤링
    fetched_docs = await news_crawling(state["keyword"])
    # 2) 결과를 [{"keyword": ..., "link": ..., "content": ...}, ...] 형태로 수집
    return {"raw_documents": fetched_docs}


# 데이터 임베딩
async def embed_and_store(state: GraphState) -> GraphState:
    print(f"수집한 문서 임베딩 중: {state['keyword']} | ")
    # 문서별 embedding 계산 -> VDB에 저장
    raws = state.get("raw_documents", [])
    if len(raws) == 0:
        return {}
    docs = await embed_documents(raws)
    # 저장 후, vector_id 등 메타 정리
    # 저장 결과 출력
    print(f"** 검색어: '{state['keyword']}' 임베딩 성공 **\n")
    return {"embedded_documents": docs}


# VDB에서 Retrieve
async def retrieve_from_vdb(state: GraphState) -> GraphState:
    print(f"데이터 검색 중: {state['keyword']} | ")
    retrieved = await search_documents(state["keyword"])

    return {"retrieved_documents": retrieved}


# 각 문서 검증
async def validate_relevance(state: GraphState) -> GraphState:
    print(f"각 문서 검증: {state['keyword']} | ")
    validated = []
    if len(state.get("retrieved_documents", [])) == 0:
        return {
            "completed": {**state.get("completed", {}), "validation": True},
        }
    for doc in state["retrieved_documents"]:
        raw = await validator_llm(keyword=state["keyword"], prompt=doc.page_content)
        if raw.find("```json") != -1:
            raw = raw.replace("```json", "")
        if raw.find("```") != -1:
            raw = raw.replace("```", "")
        try:
            judgment = json.loads(raw)
        except json.JSONDecodeError:
            print("검증자가 json 형식으로 대답하지 않았습니다!!: %r", raw)
            continue
        if judgment["validation"] == "yes":
            validated.append(
                Document(
                    page_content=doc.page_content,
                    metadata={**doc.metadata, "reason": judgment["reason"]},
                )
            )
    print(f"** 검색어: '{state['keyword']}' RAG 프로세스 완료 **\n")
    return {
        "validated_documents": validated,
        "completed": {**state.get("completed", {}), "validation": True},
    }


# 원문 요약
async def summarize_news_individual(state: GraphState) -> GraphState:
    print(f"원문 요약 중: {state['keyword']} | ")
    summaries = []
    for doc in state.get("raw_documents", []):
        summary = await summarizer_llm(doc["content"])
        summaries.append({"link": doc["link"], "summary": summary})
    print(f"** 검색어: '{state['keyword']}' 크롤링 프로세스 완료 **\n")
    return {
        "news_summaries": summaries,
        "completed": {**state.get("completed", {}), "news": True},
    }


async def analyze_join_node(state: GraphState) -> GraphState:
    print(f"조인 노드 도착: {state['keyword']} | ")
    # 결과가 모두 준비 됐을 때 return, 아닐때는??
    completed = state.get("completed", {})
    ready = completed.get("news") and completed.get("validation")
    if completed.get("news") and not completed.get("validation"):
        print("검증자 기다리는 중...")
    if not completed.get("news") and completed.get("validation"):
        print("요약자 기다리는 중...")
    return {"ready_for_analysis": ready}


async def wait_node(state):
    return state


# 분석 및 이유 작성
async def analyze_trend_reason(state: GraphState) -> GraphState:
    print(f"결론 요약본 생성 중: {state['keyword']} | ")
    raw = await analyst_llm(
        keyword=state["keyword"],
        docs=state.get("validated_documents", []),
        summaries=state.get("news_summaries", []),
    )
    if raw.find("```json") != -1:
        raw = raw.replace("```json", "")
    if raw.find("```") != -1:
        raw = raw.replace("```", "")
    try:
        trend_json = json.loads(raw)
    except json.JSONDecodeError:
        return await analyze_trend_reason(state=state)
    return {"trend_analysis": trend_json}


# 태그, 카테고리 붙이기
async def classify_and_package(state: GraphState) -> GraphState:
    print(f"태그, 카테고리 붙이는 중 {state['keyword']} | ")
    packaged = await classifier_llm(
        prompt=state["trend_analysis"].get("answer", ""),
    )
    if packaged.find("```json") != -1 or packaged.find("```") != -1:
        packaged = packaged.replace("```json", "").replace("```", "")
    try:
        packaged_json = json.loads(packaged)
    except json.JSONDecodeError:
        return await classify_and_package(state)

    print(f"**** 조사 완료: '{state['keyword']}' ****\n")
    return {"summarize_and_classify": packaged_json}


print("define state and nodes")
