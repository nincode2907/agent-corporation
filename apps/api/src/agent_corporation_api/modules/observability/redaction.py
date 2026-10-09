from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any


SECRET_FIELD = re.compile(
    r"(?:password|passwd|secret|token|api[_-]?key|authorization|cookie|credential|private[_-]?key)",
    re.IGNORECASE,
)
SECRET_TEXT = re.compile(
    r"(?i)(\b(?:bearer|password|passwd|api[_-]?key|access[_-]?token|refresh[_-]?token|secret)\b\s*[:= ]\s*)([^\s,;]+)"
)
USAGE_FIELDS = frozenset({"input_tokens", "output_tokens", "prompt_tokens", "completion_tokens",
                         "total_tokens", "cached_tokens", "cache_tokens", "reasoning_tokens"})


def redact_text(value: str) -> str:
    return SECRET_TEXT.sub(r"\1[REDACTED]", value)


def redact_structure(value: Any, field_name: str | None = None) -> Any:
    # Numeric usage counters are measurements, never authentication credentials.
    if field_name in USAGE_FIELDS and (value is None or (type(value) is int and value >= 0)):
        return value
    if field_name and SECRET_FIELD.search(field_name):
        return "[REDACTED]"
    if isinstance(value, Mapping):
        return {str(key): redact_structure(item, str(key)) for key, item in value.items()}
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [redact_structure(item) for item in value]
    return value
