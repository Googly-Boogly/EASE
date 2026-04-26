import asyncio
import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.config import settings

logger = logging.getLogger("ease")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.monotonic()
        status_code = 500
        error_message = None

        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        except Exception as exc:
            error_message = str(exc)
            raise
        finally:
            duration_ms = round((time.monotonic() - start) * 1000, 2)
            logger.info(
                "request completed",
                extra={
                    "endpoint": request.url.path,
                    "method": request.method,
                    "status_code": status_code,
                    "duration_ms": duration_ms,
                },
            )
            asyncio.create_task(
                _write_log(
                    endpoint=str(request.url.path),
                    method=request.method,
                    status_code=status_code,
                    duration_ms=duration_ms,
                    error_message=error_message,
                )
            )


async def _write_log(
    endpoint: str,
    method: str,
    status_code: int,
    duration_ms: float,
    error_message: str | None = None,
) -> None:
    try:
        from src.database import RequestLog, get_session_factory
        async with get_session_factory()() as session:
            log = RequestLog(
                endpoint=endpoint,
                method=method,
                status_code=status_code,
                duration_ms=duration_ms,
                llm_provider=settings.llm_provider,
                error_message=error_message,
            )
            session.add(log)
            await session.commit()
    except Exception:
        pass  # never let logging failures surface to callers
