# src/math_microservice/middleware/log_requests.py
from fastapi import Request, Response
from fastapi.background import BackgroundTasks
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from ..models.request_log import RequestLog
from ..core.config import settings

# build your engine with a sane pool timeout
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True,
)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def save_request_log(
    path: str,
    payload: dict,
    response_body: dict,
):
    """Open-&-close its *own* session, so FastAPI DI never has to run here."""
    async with AsyncSessionLocal() as session:
        log = RequestLog(path=path, payload=payload, response=response_body)
        session.add(log)
        await session.commit()

async def log_requests_middleware(request: Request, call_next):
    # 1. read & buffer the JSON body
    try:
        body = await request.json()
    except Exception:
        body = {}

    # 2. call the real handler
    response: Response = await call_next(request)

    # 3. capture JSON response-body safely
    try:
        resp = response.body()
    except Exception:
        resp = {}

    # 4. schedule *your* save_request_log (which makes its own session)
    background = BackgroundTasks()
    background.add_task(save_request_log, request.url.path, body, resp)
    response.background = background

    return response
