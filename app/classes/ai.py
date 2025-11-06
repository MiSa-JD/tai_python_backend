from langchain.schema import Document
from app.classes.responses import SearchResult
from typing import TypedDict, Annotated
import operator


class GraphState(TypedDict, total=False):
    keyword: str
    raw_documents: list[SearchResult]
    retrieved_documents: list[Document]
    validated_documents: list[Document]
    news_summaries: list[dict]
    completed: Annotated[dict[str, bool], operator.or_]
    trend_analysis: dict
    ready_for_analysis: bool
    summarize_and_classify: dict
