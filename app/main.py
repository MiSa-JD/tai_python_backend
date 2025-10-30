from fastapi import FastAPI

from .classes.responses import SearchResultOutput
from .classes.requests import SearchRequest
from app.crawling import news_crawling


def create_app() -> FastAPI:
    """Factory to build the FastAPI application."""
    app = FastAPI(title="AiBackend API")

    @app.get("/ping")
    async def ping() -> dict[str, str]:
        """Health-check endpoint used by dev notebooks and monitoring."""
        return {"status": "ok"}

    @app.post("/api/request")
    async def searchAndDecorate(data: SearchRequest) -> SearchResultOutput:
        newses = news_crawling(data.keyword)

        for news in newses:
            print ("Keyword:", news['keyword'])
            print("Url:", news['url'])
            print("Title:", news['title'])
            print("Content:", news['content'])
            print("-" * 80)

        tmp = SearchResultOutput(
            keyword=data.keyword,
            description="요약",
            content="LLM의 답변",
            tags=["태그1", "태그2"],
            category="카테고리",
            refered=["링크1", "링크2"],
        )
        return tmp

    return app


app = create_app()
