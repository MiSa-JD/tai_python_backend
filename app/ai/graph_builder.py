from langgraph.graph import StateGraph
from typing import Annotated
import operator
from app.ai.graph_def import (
    entry_node,
    collect_sources,
    embed_and_store,
    retrieve_from_vdb,
    validate_relevance,
    summarize_news_individual,
    analyze_join_node,
    analyze_trend_reason,
    classify_and_package,
)
from app.classes.ai import GraphState

WAIT = "__wait__"

workflow = StateGraph(GraphState)

workflow.add_node("entry_node", entry_node)
workflow.add_node("collect_sources", collect_sources)
workflow.add_node("embed_and_store", embed_and_store)
workflow.add_node("retrieve_from_vdb", retrieve_from_vdb)
workflow.add_node("validate_relevance", validate_relevance)
workflow.add_node("summarize_news_individual", summarize_news_individual)
workflow.add_node("analyze_join_node", analyze_join_node)
workflow.add_node("analyze_trend_reason", analyze_trend_reason)
workflow.add_node("classify_and_package", classify_and_package)

# workflow.add_edge("collect_sources", "retrieve_from_vdb")
# # workflow.add_edge("embed_and_store", "retrieve_from_vdb")
# workflow.add_edge("retrieve_from_vdb", "embed_and_store")

# workflow.add_edge("embed_and_store", "validate_relevance")
# workflow.add_edge("validate_relevance", "summarize_news_individual")
# workflow.add_edge("summarize_news_individual", "analyze_trend_reason")
# workflow.add_edge("analyze_trend_reason", "classify_and_package")

# 시작 -> 크롤링 -> 요약 -> 조인 노드
workflow.add_edge("entry_node", "collect_sources")
workflow.add_edge("collect_sources", "summarize_news_individual")
workflow.add_edge("summarize_news_individual", "analyze_join_node")

# 크롤링 -> 임베딩
workflow.add_edge("collect_sources", "embed_and_store")

# 시작 -> vdb 검색 -> 연관성 확인 -> 조인 노드
workflow.add_edge("entry_node", "retrieve_from_vdb")
workflow.add_edge("retrieve_from_vdb", "validate_relevance")
workflow.add_edge("validate_relevance", "analyze_join_node")

# 조인 노드 -> 최종 분석 -> 요약 및 태그
# 조인노드 체크
workflow.add_node(WAIT, lambda state: state)
workflow.add_conditional_edges(
    "analyze_join_node",
    lambda state: "analyze_trend_reason" if state.get("ready_for_analysis") else WAIT,
    {"analyze_trend_reason": "analyze_trend_reason", WAIT: WAIT},
)
# workflow.add_edge(WAIT, "analyze_join_node")
workflow.add_edge("analyze_trend_reason", "classify_and_package")

workflow.set_entry_point("entry_node")
workflow.set_finish_point("classify_and_package")

app = workflow.compile()

print("build graph")
print("=== LangGraph Ready ===")
