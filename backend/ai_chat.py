import json
import os
import time

from dotenv import load_dotenv, find_dotenv
from google import genai


# -----------------------------
# Load .env
# -----------------------------
dotenv_path = find_dotenv()
print("Dotenv path:", dotenv_path)

load_dotenv(dotenv_path, override=True)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

print("Gemini API key loaded successfully.")


# -----------------------------
# Configure Gemini
# -----------------------------
client = genai.Client(api_key=api_key)


SYSTEM_PROMPT = (
    "You are BizTwin, a friendly business analyst for a small business owner. "
    "You are given the business's real, computed numbers as JSON. "
    "Answer the question using ONLY those numbers. "
    "Never invent numbers or make assumptions. "
    "Keep answers concise but useful. Explain what the numbers mean for the business and provide one practical insight or suggestion when relevant."
)


def answer_question(question: str, analytics: dict) -> str:

    prompt = f"""
{SYSTEM_PROMPT}

Business Data:
{json.dumps(analytics, indent=2)}

Question:
{question}
"""

    print("Calling Gemini...")

    for attempt in range(3):

        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )

            if response.text:
                print("Gemini responded successfully.")

                return response.text.strip()

            print("Gemini returned empty response.")

        except Exception as e:

            error = str(e)

            print(f"Gemini attempt {attempt + 1} failed:")
            print(error)

            # Retry temporary server overload errors
            if "503" in error and attempt < 2:
                print("Gemini busy. Retrying in 3 seconds...")
                time.sleep(3)
                continue

            break

    print("Using fallback response.")
    return _fallback_answer(analytics)


def _fallback_answer(a: dict) -> str:
    return (
        f"(Offline summary) Revenue is {a['revenue']:.2f}, "
        f"expenses are {a['expenses']:.2f}, "
        f"profit is {a['profit']:.2f}, "
        f"margin is {a['margin']:.1f}%."
    )