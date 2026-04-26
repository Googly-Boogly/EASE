import logging
import logging.config
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from src.auth import require_api_key
from src.config import settings
from src.routers import actions, ease, election, environment, safety
from src.routers import health as health_router
from src.routers import tasks as tasks_router

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": '{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","message":"%(message)s"}',
        }
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "json"},
    },
    "root": {"level": "INFO", "handlers": ["console"]},
})

_log = logging.getLogger("ease")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not settings.llm_api_key:
        raise RuntimeError(
            "LLM_API_KEY is not set. Copy .env.example to .env and fill in your key."
        )
    if settings.llm_provider not in ("anthropic", "openai", "google"):
        raise RuntimeError(
            f"LLM_PROVIDER must be 'anthropic', 'openai', or 'google', "
            f"got '{settings.llm_provider}'"
        )

    if settings.database_url:
        from src.database import close_db, init_db
        try:
            await init_db()
            _log.info("Database tables ready")
        except Exception as exc:
            _log.warning(f"Database init failed — continuing without DB logging: {exc}")

    yield

    if settings.database_url:
        from src.database import close_db
        await close_db()


app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    lifespan=lifespan,
)

if settings.database_url:
    from src.middleware import RequestLoggingMiddleware
    app.add_middleware(RequestLoggingMiddleware)

# /health is public — no auth required
app.include_router(health_router.router)

# All API routes require authentication (disabled when API_KEY is empty)
_auth = [Depends(require_api_key)]
app.include_router(environment.router, dependencies=_auth)
app.include_router(actions.router, dependencies=_auth)
app.include_router(safety.router, dependencies=_auth)
app.include_router(election.router, dependencies=_auth)
app.include_router(ease.router, dependencies=_auth)
app.include_router(tasks_router.router, dependencies=_auth)
