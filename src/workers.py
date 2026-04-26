import asyncio

from celery import Celery

from src.config import settings

celery_app = Celery(
    "ease",
    broker=settings.redis_url,
    backend=settings.redis_url,
)
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    result_expires=3600,
    task_track_started=True,
)


@celery_app.task(bind=True, name="ease.run_pipeline")
def run_ease_task(self, request_data: dict) -> dict:
    return asyncio.run(_async_pipeline(request_data))


async def _async_pipeline(request_data: dict) -> dict:
    from src.models.requests import EASERequest
    from src.routers.ease import run_ease_framework

    req = EASERequest(**request_data)
    result = await run_ease_framework(req)
    return result.model_dump()
