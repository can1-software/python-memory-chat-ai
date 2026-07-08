from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY, GEMINI_MODEL

SYSTEM_PROMPT = (
    "You are a helpful AI assistant. Give clear and concise answers. "
    "If the user writes in Turkish, answer in Turkish. "
    "If the user writes in English, you may answer in English."
)


class GeminiServiceError(Exception):
    pass


def _get_client() -> genai.Client:
    if not GEMINI_API_KEY:
        raise GeminiServiceError("GEMINI_API_KEY is not set.")
    return genai.Client(api_key=GEMINI_API_KEY)


def generate_response(messages: list[dict]) -> str:
    """Send recent chat messages to Gemini and return assistant text."""
    contents = []
    for message in messages:
        role = "user" if message["role"] == "user" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part(text=message["content"])],
            )
        )

    try:
        client = _get_client()
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )

        text = response.text
        if not text:
            raise GeminiServiceError("Gemini returned an empty response.")

        return text.strip()
    except GeminiServiceError:
        raise
    except Exception as e:
        raise GeminiServiceError("Gemini request failed.") from e
