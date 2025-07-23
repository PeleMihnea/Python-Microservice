# src/math_microservice/api/v1/__init__.py
from fastapi import APIRouter
from .endpoints import router as math_router

router = APIRouter()
router.include_router(math_router, prefix="", tags=["math"])
