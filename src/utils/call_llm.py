import asyncio

from tenacity import AsyncRetrying, stop_after_attempt, wait_exponential

from src.config import settings

# ---------------------------------------------------------------------------
# Module-level client singletons — created once, reused across requests
# ---------------------------------------------------------------------------

_clients: dict = {}


def _get_anthropic_client():
    if "anthropic" not in _clients:
        import anthropic
        _clients["anthropic"] = anthropic.AsyncAnthropic(api_key=settings.llm_api_key)
    return _clients["anthropic"]


def _get_openai_client():
    if "openai" not in _clients:
        from openai import AsyncOpenAI
        _clients["openai"] = AsyncOpenAI(api_key=settings.llm_api_key)
    return _clients["openai"]


def _get_google_client():
    if "google" not in _clients:
        from google import genai
        _clients["google"] = genai.Client(api_key=settings.llm_api_key)
    return _clients["google"]


# ---------------------------------------------------------------------------
# Provider implementations
# ---------------------------------------------------------------------------

async def _call_anthropic(system_prompt: str, user_prompt: str) -> str:
    client = _get_anthropic_client()
    message = await client.messages.create(
        model=settings.llm_model,
        max_tokens=settings.llm_max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
        timeout=settings.llm_timeout_seconds,
    )
    return message.content[0].text


async def _call_openai(system_prompt: str, user_prompt: str) -> str:
    client = _get_openai_client()
    response = await client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=settings.llm_max_tokens,
        timeout=settings.llm_timeout_seconds,
    )
    return response.choices[0].message.content


async def _call_google(system_prompt: str, user_prompt: str) -> str:
    from google.genai import types
    client = _get_google_client()
    response = await asyncio.wait_for(
        client.aio.models.generate_content(
            model=settings.llm_model,
            contents=user_prompt,
            config=types.GenerateContentConfig(system_instruction=system_prompt),
        ),
        timeout=settings.llm_timeout_seconds,
    )
    return response.text


# ---------------------------------------------------------------------------
# Public interface — retries with exponential backoff
# ---------------------------------------------------------------------------

async def call_llm(system_prompt: str, user_prompt: str) -> str:
    """Call the configured LLM provider and return the response text.

    Retries up to ``settings.llm_max_retries`` times with exponential backoff
    on any exception. Provider selected via ``settings.llm_provider``.
    """
    async for attempt in AsyncRetrying(
        stop=stop_after_attempt(settings.llm_max_retries),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    ):
        with attempt:
            provider = settings.llm_provider
            if provider == "anthropic":
                return await _call_anthropic(system_prompt, user_prompt)
            elif provider == "openai":
                return await _call_openai(system_prompt, user_prompt)
            elif provider == "google":
                return await _call_google(system_prompt, user_prompt)
            else:
                raise ValueError(f"Unsupported LLM provider: {provider!r}")
