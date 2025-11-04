import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .classes.responses import SearchResultOutput
from .classes.requests import SearchRequest
from .ai.graph_builder import app as pipeline


def create_app() -> FastAPI:
    """Factory to build the FastAPI application."""
    app = FastAPI(title="AiBackend API")

    origin_env = os.getenv("FASTAPI_ALLOWED_ORIGINS", "")
    allowed_origins = allowed_origins = [
        origin.strip() for origin in origin_env.split(",") if origin.strip()
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/ping")
    async def ping() -> dict[str, str]:
        """Health-check endpoint used by dev notebooks and monitoring."""
        return {"status": "ok"}

    @app.post("/api/request")
    async def searchAndDecorate(data: SearchRequest) -> SearchResultOutput:
        keyword = data.keyword
        initial_state = {"keyword": keyword}

        start = time.perf_counter()
        output = await pipeline.ainvoke(initial_state)
        elapsed = time.perf_counter() - start
        print(f"Pipeline finished in {elapsed} seconds (keyword={keyword})")

        get_summarize = output["summarize_and_classify"]

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
