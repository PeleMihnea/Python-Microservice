from fastapi import FastAPI
from .api.v1.endpoints import router as math_router
from .core.config import settings
from .middleware.log_requests import log_requests_middleware
import os

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


    app.middleware("http")(log_requests_middleware)
    # mount your math endpoints under /api/v1
    app.include_router(math_router, prefix="/api/v1")

    return app
