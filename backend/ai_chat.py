"""AI Business Chat via Fireworks AI. Falls back gracefully with no API key."""
import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

FIREWORKS_URL = "https://api.fireworks.ai/inference/v1/chat/completions"

SYSTEM_PROMPT = (
    "You are BizTwin, a friendly business analyst for a small business owner. "
    "You are given the business's real, computed numbers as JSON. "
    "Answer the question using ONLY those numbers. Never invent or estimate "
    "figures that are not in the data. Keep answers short (2-4 sentences), "
    "plain-English, and always cite the specific numbers you used."
)


def answer_question(question: str, analytics: dict) -> str:
    api_key = os.getenv("FIREWORKS_API_KEY")
    if not api_key:
        return _fallback_answer(analytics)

    payload = {
        "model": os.getenv(
            "FIREWORKS_MODEL",
            "accounts/fireworks/models/llama-v3p1-8b-instruct",
        ),
        "max_tokens": 400,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Business data (JSON):\n{json.dumps(analytics)}\n\n"
                    f"Question: {question}"
                ),
            },
        ],
    }
    try:
        resp = requests.post(
            FIREWORKS_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["choices"]<a href="" class="citation-link" target="_blank" style="vertical-align: super; font-size: 0.8em; margin-left: 3px;">[0]</a>["message"]["content"].strip()
    except requests.RequestException:
        return _fallback_answer(analytics)


def _fallback_answer(a: dict) -> str:
    """Deterministic answer from real data — used if the AI is unreachable."""
    return (
        f"(Offline summary) Revenue is {a['revenue']:.2f}, cost of goods "
        f"{a['cogs']:.2f}, expenses {a['expenses']:.2f}, giving a profit of "
        f"{a['profit']:.2f} ({a['margin']:.1f}% margin)."
    )
