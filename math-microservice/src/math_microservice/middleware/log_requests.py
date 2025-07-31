# src/math_microservice/middleware/log_requests.py
from fastapi import Request, Response
from fastapi.background import BackgroundTasks
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from ..models.request_log import RequestLog
from ..core.config import settings

from starlette.responses import Response as StarletteResponse
from starlette.types import Message
import json

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

    response_body_chunks = []

    async def receive_with_buffering() -> Message:
        # Clone the request stream to avoid consuming it
        body_bytes = await request.body()
        return {"type": "http.request", "body": body_bytes, "more_body": False}

    request = Request(request.scope, receive=receive_with_buffering)

    # Intercept the response and buffer it
    original_response = await call_next(request)
    async for chunk in original_response.body_iterator:
        response_body_chunks.append(chunk)

    # Join all chunks into a single body
    full_body = b"".join(response_body_chunks)

    try:
        resp_json = json.loads(full_body.decode())
    except Exception:
        resp_json = {}

    # 3. Recreate the response object (so it can still be sent to the client)
    response = StarletteResponse(
        content=full_body,
        status_code=original_response.status_code,
        headers=dict(original_response.headers),
        media_type=original_response.media_type
    )


    # 4. schedule *your* save_request_log (which makes its own session)
    background = BackgroundTasks()
    background.add_task(save_request_log, request.url.path, body, resp_json)
    response.background = background

    return response
