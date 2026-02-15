from src.config import settings


async def call_llm(system_prompt: str, user_prompt: str) -> str:
    """Call the configured LLM provider and return the response text.

    The provider is selected via the ``LLM_PROVIDER`` environment variable
    (or ``settings.llm_provider``).  Supported values: anthropic, openai, google.

    Args:
        system_prompt: Instructions for the LLM's role and output format.
        user_prompt: The user-facing request content.

    Returns:
        The raw text response from the LLM.
    """
    provider = settings.llm_provider

    if provider == "anthropic":
        return await _call_anthropic(system_prompt, user_prompt)
    elif provider == "openai":
        return await _call_openai(system_prompt, user_prompt)
    elif provider == "google":
        return await _call_google(system_prompt, user_prompt)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider!r}")


async def _call_anthropic(system_prompt: str, user_prompt: str) -> str:
    import anthropic

    client = anthropic.AsyncAnthropic(api_key=settings.llm_api_key)
    message = await client.messages.create(
        model=settings.llm_model,
        max_tokens=200000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return message.content[0].text


async def _call_openai(system_prompt: str, user_prompt: str) -> str:
    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=settings.llm_api_key)

    response = await client.responses.create(
        model=settings.llm_model,
        reasoning={"effort": "low"},
        instructions=system_prompt,
        input=user_prompt,
    )

    return response.output_text


async def _call_google(system_prompt: str, user_prompt: str) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=settings.llm_api_key)
    response = await client.aio.models.generate_content(
        model=settings.llm_model,
        contents=user_prompt,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    return response.text
