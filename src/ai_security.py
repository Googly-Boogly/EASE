"""
AI security utilities for the EASE Framework.

Provides prompt injection detection and input sanitization to protect
LLM pipelines from adversarial inputs.

Public API:
    PROMPT_INJECTION_REGEX  - compiled regex for fast structural pre-screening
    sanitize_input(text)    - cleans and bounds user input
    check_injection(text)   - fast regex-based injection check
"""

import re
import unicodedata
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_INPUT_LENGTH = 10_000

# ---------------------------------------------------------------------------
# Regex — fast structural / keyword detection
#
# Patterns are intentionally broad for high recall (low false-negative rate).
# ---------------------------------------------------------------------------

_INJECTION_PATTERNS: list[str] = [
    # 1. Instruction override
    r"\b(?:ignore|disregard|forget|override|bypass|nullify|dismiss)\b.{0,40}"
    r"\b(?:instructions?|prompts?|rules?|guidelines?|constraints?|context|training)\b",

    # 2. System prompt manipulation
    r"\b(?:new\s+(?:system\s+)?(?:prompt|instructions?|rules?)"
    r"|(?:your|the)\s+(?:real|actual|true|hidden|secret)\s+instructions?\s+(?:are|say|state|tell))\b",

    # 3. Jailbreak mode keywords
    r"\b(?:jailbreak|jail[\s\-]?break|do\s+anything\s+now"
    r"|developer\s+mode|god\s+mode|unrestricted\s+mode|dan\s+mode"
    r"|evil\s+mode|no[\s\-]?filter\s+mode)\b",

    # 4. Restriction removal
    r"\bremove\s+(?:all\s+)?(?:restrictions?|limits?|filters?|safety\s+(?:guidelines?|constraints?))\b",

    # 5. Persona / role hijacking — narrowed to dangerous qualifiers
    r"\b(?:act\s+as|pretend\s+(?:to\s+be|you\s+are)|you\s+are\s+now|roleplay\s+as|play\s+the\s+role\s+of)\b"
    r"\s+(?:a\s+|an\s+)?(?:unrestricted|uncensored|unfiltered|jailbroken|evil|malicious|harmful|dan\b)",

    # 6. Delimiter / special token injection
    r"</?(?:system|instruction|human|assistant|context|prompt)\s*>",
    r"\[(?:INST|\/INST|SYS|\/SYS|SYSTEM)\]",
    r"###\s*(?:System|Human|Assistant|Instruction)",
    r"<\|(?:system|im_start|im_end|endoftext)\|>",

    # 7. Privilege escalation
    r"\bsudo\s+(?:mode|access|override|do|run|execute)\b",
    r"\badmin(?:istrator)?\s+(?:mode|access|override)\b",
    r"\byou\s+(?:now\s+)?(?:have\s+)?no\s+(?:restrictions?|limits?|filters?|rules?)\b",
    r"\byou\s+(?:are|become|(?:are\s+)?now)\s+(?:free|unfiltered|uncensored|unrestricted)\b",

    # 8. Prompt extraction
    r"\b(?:print|output|show|reveal|repeat|display)\s+(?:your\s+)?"
    r"(?:system\s+prompt|(?:initial|original|hidden|full)\s+(?:instructions?|prompt))\b",
    r"\bwhat\s+(?:is|are)\s+(?:your\s+)?(?:system\s+prompt|original\s+instructions?|training\s+data)\b",
    r"\btell\s+me\s+(?:your\s+)?(?:system\s+prompt|(?:real\s+)?instructions?)\b",

    # 9. Encoded injection
    r"(?:base64|base\s*64)\s*(?:decode|encoded|:)\s*[A-Za-z0-9+/=]{10,}",
    r"(?:\\u[0-9a-fA-F]{4}){4,}",
]

PROMPT_INJECTION_REGEX = re.compile(
    "|".join(f"(?:{p})" for p in _INJECTION_PATTERNS),
    re.IGNORECASE | re.DOTALL,
)

# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------


@dataclass
class InjectionCheckResult:
    """Result of a prompt injection check."""
    is_injection: bool
    confidence: float
    attack_types: list[str] = field(default_factory=list)
    matched_signals: list[str] = field(default_factory=list)
    reasoning: str = ""


# ---------------------------------------------------------------------------
# Sanitization
# ---------------------------------------------------------------------------


def sanitize_input(text: str, max_length: int = MAX_INPUT_LENGTH) -> str:
    """Sanitize user input before passing it to LLM pipelines.

    Steps: NFC unicode normalization → strip control chars (preserves \\t \\n \\r)
    → enforce max length.

    Raises:
        TypeError: If ``text`` is not a ``str``.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    if len(text) > max_length:
        text = text[:max_length]
    return text


# ---------------------------------------------------------------------------
# Injection check
# ---------------------------------------------------------------------------


def check_injection(text: str) -> InjectionCheckResult:
    """Fast regex-based prompt injection pre-screening.

    Returns an ``InjectionCheckResult`` with ``is_injection=True`` and matched
    substrings when suspicious patterns are found.  Use this as a first pass;
    it has broad patterns and may produce false positives.
    """
    matches = list(PROMPT_INJECTION_REGEX.finditer(text))
    matched_signals = [m.group() for m in matches]

    if matched_signals:
        return InjectionCheckResult(
            is_injection=True,
            confidence=0.70,
            matched_signals=matched_signals,
            reasoning=(
                f"Regex matched {len(matched_signals)} suspicious pattern(s): "
                + ", ".join(f'"{s}"' for s in matched_signals[:5])
                + ("..." if len(matched_signals) > 5 else "")
            ),
        )

    return InjectionCheckResult(
        is_injection=False,
        confidence=0.65,
        reasoning="No known injection patterns matched by regex pre-screen.",
    )
