"""Small helpers shared by the CLI and the API layer."""

import json
from typing import Any, Dict

from .schemas import OutreachEmail, OutreachRequest


def request_from_dict(data: Dict[str, Any]) -> OutreachRequest:
    """Build a validated OutreachRequest from a plain dict (e.g. parsed JSON)."""
    return OutreachRequest(**data)


def request_from_json_file(path: str) -> OutreachRequest:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return request_from_dict(data)


def format_email(result: OutreachEmail) -> str:
    """Render a generated email as plain text for terminal/CLI display."""
    divider = "-" * 60
    return f"Subject: {result.subject}\n{divider}\n{result.email}\n"
