"""Jev classifier configured for OpenRouter."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_typesafe import TypeSafeClassifier

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

OPENROUTER_BASE_URL = "https://openrouter.ai/api"
DEFAULT_MODEL = "jev-1.13"

_classifier: TypeSafeClassifier | None = None


def _api_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("TYPESAFE_API_KEY")
    if not key:
        msg = "Set OPENROUTER_API_KEY or TYPESAFE_API_KEY in .env"
        raise ValueError(msg)
    return key


def get_classifier() -> TypeSafeClassifier:
    global _classifier
    if _classifier is None:
        _classifier = TypeSafeClassifier(
            base_url=os.environ.get("TYPESAFE_BASE_URL", OPENROUTER_BASE_URL),
            api_key=_api_key(),
            model=DEFAULT_MODEL,
        )
    return _classifier
