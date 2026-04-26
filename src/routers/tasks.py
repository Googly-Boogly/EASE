from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.auth import require_api_key

router = APIRouter(prefix="/api/v1", tags=["tasks"])


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: dict | None = None
    error: str | None = None


@router.get("/tasks/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(
    task_id: str,
    _: None = Depends(require_api_key),
) -> TaskStatusResponse:
    from celery.result import AsyncResult
    from src.workers import celery_app

    result = AsyncResult(task_id, app=celery_app)

    if result.state == "PENDING":
        return TaskStatusResponse(task_id=task_id, status="pending")
    elif result.state == "STARTED":
        return TaskStatusResponse(task_id=task_id, status="running")
    elif result.state == "SUCCESS":
        return TaskStatusResponse(task_id=task_id, status="completed", result=result.result)
    elif result.state == "FAILURE":
        return TaskStatusResponse(task_id=task_id, status="failed", error=str(result.result))
    else:
        return TaskStatusResponse(task_id=task_id, status=result.state.lower())
