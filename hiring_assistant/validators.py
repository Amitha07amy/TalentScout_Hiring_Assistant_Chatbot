from __future__ import annotations

import re
from typing import List


EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_RE = re.compile(r"^\+?[0-9\-\s()]{7,20}$")


def is_exit_intent(text: str) -> bool:
    keywords = {"exit", "quit", "bye", "goodbye", "end", "stop"}
    lowered = text.strip().lower()
    return lowered in keywords or any(f" {k}" in f" {lowered} " for k in keywords)


def valid_email(text: str) -> bool:
    return bool(EMAIL_RE.match(text.strip()))


def valid_phone(text: str) -> bool:
    return bool(PHONE_RE.match(text.strip()))


def valid_experience(text: str) -> bool:
    text = text.strip().lower().replace("years", "").replace("year", "")
    text = text.strip()
    try:
        value = float(text)
    except ValueError:
        return False
    return 0 <= value <= 50


def parse_tech_stack(text: str) -> List[str]:
    raw = [item.strip() for item in text.split(",")]
    cleaned: List[str] = []
    for item in raw:
        if not item:
            continue
        # Handles inputs like "Programming : Python"
        if ":" in item:
            item = item.split(":")[-1].strip()
        # Simplify labels like "AWS (basic)" -> "AWS"
        item = re.sub(r"\s*\([^)]*\)\s*$", "", item).strip()
        if item:
            cleaned.append(item)

    deduped: List[str] = []
    seen = set()
    for item in cleaned:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    return deduped
