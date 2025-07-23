from fastapi import FastAPI
from .api.v1.endpoints import router as math_router
from .core.config import settings

def create_app() -> FastAPI:
    """
    Application factory: constructs and configures the FastAPI instance.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/docs",
        openapi_url="/openapi.json",
    )

    # mount your math endpoints under /api/v1
    app.include_router(math_router, prefix="/api/v1")

    # you could also attach event handlers, middleware, etc. here
    # e.g. app.add_middleware(...)

    return app
