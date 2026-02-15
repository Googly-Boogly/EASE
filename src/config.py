from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_title: str = "EASE Framework API"
    api_version: str = "2.0"

    llm_provider: str = "anthropic"
    llm_model: str = "claude-sonnet-4-20250514"
    llm_api_key: str = ""

    default_min_actions: int = 5
    default_safety_threshold: float = 3.0
    default_weights: dict[str, float] = {
        "goal_achievement": 0.30,
        "safety_rating": 0.40,
        "risk_level": 0.20,
        "resource_efficiency": 0.10,
    }

    model_config = {"env_file": ".env"}


settings = Settings()
