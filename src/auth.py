from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from src.config import settings

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def require_api_key(api_key: str | None = Security(_api_key_header)) -> None:
    """FastAPI dependency — validates X-API-Key header.

    Auth is disabled when API_KEY setting is empty (default), allowing
    unrestricted local development.
    """
    if not settings.api_key:
        return
    if api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
