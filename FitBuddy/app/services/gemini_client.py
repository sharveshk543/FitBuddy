from typing import Optional

from google import genai

from app.config import settings


_client = None


def get_gemini_client():
    """
    Return a configured Gemini client.

    Returns None when AI is disabled or when no API key
    is configured. This allows FitBuddy to run in demo mode.
    """

    global _client

    if not settings.AI_ENABLED:
        return None

    if not settings.GEMINI_API_KEY:
        return None

    if _client is None:
        _client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    return _client