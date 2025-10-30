from langgraph.graph import StateGraph
from app.ai.graph_def import (
    collect_sources,
    embed_and_store,
    retrieve_from_vdb,
    validate_relevance,
    summarize_news_individual,
    analyze_trend_reason,
    classify_and_package,
)

workflow = StateGraph(dict)  # dict 대신 위에서 정의한 State 모델 사용 권장

workflow.add_node("collect_sources", collect_sources)
workflow.add_node("embed_and_store", embed_and_store)
workflow.add_node("retrieve_from_vdb", retrieve_from_vdb)
workflow.add_node("validate_relevance", validate_relevance)
workflow.add_node("summarize_news_individual", summarize_news_individual)
workflow.add_node("analyze_trend_reason", analyze_trend_reason)
workflow.add_node("classify_and_package", classify_and_package)

workflow.add_edge("collect_sources", "retrieve_from_vdb")
# workflow.add_edge("embed_and_store", "retrieve_from_vdb")
workflow.add_edge("retrieve_from_vdb", "embed_and_store")

workflow.add_edge("embed_and_store", "validate_relevance")
workflow.add_edge("validate_relevance", "summarize_news_individual")
workflow.add_edge("summarize_news_individual", "analyze_trend_reason")
workflow.add_edge("analyze_trend_reason", "classify_and_package")

workflow.set_entry_point("collect_sources")
workflow.set_finish_point("classify_and_package")

app = workflow.compile()
