from fastapi import APIRouter
from sqlalchemy import text

from src.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict:
    result: dict = {
        "status": "healthy",
        "database": "disabled",
        "redis": "ok",
        "llm_provider": settings.llm_provider,
    }

    if settings.database_url:
        try:
            from src.database import get_session_factory
            async with get_session_factory()() as session:
                await session.execute(text("SELECT 1"))
            result["database"] = "ok"
        except Exception as exc:
            result["database"] = f"error: {exc}"
            result["status"] = "degraded"

    try:
        import redis.asyncio as aioredis
        r = aioredis.from_url(settings.redis_url, socket_connect_timeout=2)
        await r.ping()
        await r.aclose()
    except Exception as exc:
        result["redis"] = f"error: {exc}"
        result["status"] = "degraded"

    return result
