"""Red-flag to green-flag analysis powered by Jev."""

from __future__ import annotations

from langchain_typesafe import Score

from jev_experiment.classifier import get_classifier

FLAG_SCORE = Score(
    instructions=(
        "Rate this situation, message, or behavior on a red-flag to green-flag scale. "
        "Consider emotional safety, respect, honesty, consistency, and whether this "
        "is healthy or concerning in a relationship or social context."
    ),
    criteria=[
        "Major red flag — toxic, manipulative, unsafe, or extremely concerning.",
        "Red flag — clearly problematic or worth serious concern.",
        "Mixed / yellow — some good signs, some concerning signs.",
        "Green flag — mostly positive, respectful, and healthy.",
        "Major green flag — very positive, trustworthy, and reassuring.",
    ],
)

LABELS = [
    (0, 18, "RUN bestie 🚩", "it's giving exit"),
    (18, 38, "major ick", "no cap that's sus"),
    (38, 58, "mixed vibes", "50/50 energy"),
    (58, 78, "lowkey valid", "mostly based"),
    (78, 101, "green flag era 💚", "W behavior"),
]


def _label_for_percent(percent: float) -> tuple[str, str]:
    for low, high, title, subtitle in LABELS:
        if low <= percent < high:
            return title, subtitle
    return LABELS[-1][2], LABELS[-1][3]


def analyze(text: str) -> dict:
    """Return a red→green flag score for the given text."""
    response = get_classifier().invoke(
        {
            "state": text.strip(),
            "questions": {"flag": FLAG_SCORE},
        }
    )
    answer = response.scores["flag"]
    max_level = max(answer.legend.keys())
    percent = round((answer.score / max_level) * 100, 1)
    percent = max(0.0, min(100.0, percent))
    title, subtitle = _label_for_percent(percent)

    return {
        "percent": percent,
        "score": round(answer.score, 2),
        "max_score": max_level,
        "label": title,
        "vibe": subtitle,
        "confidence": round(answer.confidence, 2),
        "probabilities": {str(k): round(v, 3) for k, v in answer.probabilities.items()},
        "legend": {str(k): str(v) for k, v in answer.legend.items()},
    }
