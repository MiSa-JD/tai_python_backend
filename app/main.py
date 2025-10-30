from fastapi import FastAPI

from .classes.responses import SearchResultOutput
from .classes.requests import SearchRequest
from .ai.graph_builder import app as pipeline
import json


def create_app() -> FastAPI:
    """Factory to build the FastAPI application."""
    app = FastAPI(title="AiBackend API")

    @app.get("/ping")
    async def ping() -> dict[str, str]:
        """Health-check endpoint used by dev notebooks and monitoring."""
        return {"status": "ok"}

    @app.post("/api/request")
    async def searchAndDecorate(data: SearchRequest) -> SearchResultOutput:
        keyword = data.keyword

        initial_state = {"keyword": keyword}

        output = await pipeline.ainvoke(initial_state)

        # tmp = SearchResultOutput(
        #     keyword=data.keyword,
        #     description="요약",
        #     content="LLM의 답변",
        #     tags=["태그1", "태그2"],
        #     category="카테고리",
        #     refered=["링크1", "링크2"],
        # )
        get_summarize = json.loads(output["summarize_and_classify"])

        tmp = SearchResultOutput(
            keyword=output["keyword"],
            description=get_summarize["summarize"],
            content=output["trend_analysis"]["answer"],
            tags=get_summarize["tags"],
            category=get_summarize["category"],
            refered=output["trend_analysis"]["link"],
        )
        return tmp

    return app


app = create_app()

print("*" * 52)
print("FastAPI is running on http://localhost:8000")
print("Checkout Swagger page on http://localhost:8000/docs")
print("*" * 52)
