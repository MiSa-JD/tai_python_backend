from fastapi import FastAPI


def create_app() -> FastAPI:
    """Factory to build the FastAPI application."""
    app = FastAPI(title="AiBackend API")

    @app.get("/ping")
    async def ping() -> dict[str, str]:
        """Health-check endpoint used by dev notebooks and monitoring."""
        return {"status": "ok"}

    @app.get("/items/{item_id}")
    async def read_item(item_id: int, q: str | None = None) -> dict[str, int | str | None]:
        """Return sample payload to illustrate path and query parameters."""
        return {"item_id": item_id, "q": q}

    return app


app = create_app()
