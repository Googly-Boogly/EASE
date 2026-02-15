from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import settings
from src.routers import environment, actions, safety, election, ease


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
    yield


app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    lifespan=lifespan,
)

app.include_router(environment.router)
app.include_router(actions.router)
app.include_router(safety.router)
app.include_router(election.router)
app.include_router(ease.router)
