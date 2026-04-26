import functools
from pathlib import Path

import yaml

_PROMPTS_DIR = Path(__file__).parent.parent.parent / "prompts"


@functools.lru_cache(maxsize=None)
def _load_file(filename: str) -> dict:
    """Load and cache a YAML prompt file. Each file is read once per process."""
    with (_PROMPTS_DIR / filename).open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_prompt(filename: str, key: str) -> str:
    """Return a named prompt string from a YAML file in the prompts/ directory."""
    return _load_file(filename)[key]
