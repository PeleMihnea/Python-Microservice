# src/math_microservice/scripts/test_db.py
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from math_microservice.core.config import settings

async def test_connection():
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    async with engine.connect() as conn:
          # wrap raw SQL in sqlalchemy.text()
        result = await conn.execute(text("SELECT version();"))
          # version = await conn.scalar(text("SELECT version();"))
        version = result.scalar_one()
        print("Postgres version:", version)
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_connection())
