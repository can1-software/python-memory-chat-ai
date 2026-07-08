from app.config import AI_PROVIDER
from app.services import gemini_service


class AIServiceError(Exception):
    pass


def _get_last_user_message(messages: list[dict]) -> str:
    for message in reversed(messages):
        if message["role"] == "user":
            return message["content"]
    return ""


def _get_memory_value(memories_text: str, key: str) -> str | None:
    prefix = f"- {key}:"
    for line in memories_text.splitlines():
        if line.strip().startswith(prefix):
            return line.split(":", 1)[1].strip()
    return None


def _generate_mock_response(messages: list[dict], memories_text: str = "") -> str:
    user_message = _get_last_user_message(messages)
    lowered = user_message.lower()

    if "adım ne" in lowered or "adim ne" in lowered:
        name = _get_memory_value(memories_text, "name")
        if name:
            return f"Adın {name}."

    return f"Bu bir test AI cevabıdır. Mesajını aldım: {user_message}"


def _generate_gemini_response(messages: list[dict], memories_text: str = "") -> str:
    try:
        return gemini_service.generate_response(messages, memories_text=memories_text)
    except Exception as e:
        print("AI PROVIDER ERROR:", repr(e))
        raise AIServiceError("Gemini request failed.") from e


def generate_ai_response(messages: list[dict], memories_text: str = "") -> str:
    if AI_PROVIDER == "mock":
        return _generate_mock_response(messages, memories_text=memories_text)

    if AI_PROVIDER == "gemini":
        return _generate_gemini_response(messages, memories_text=memories_text)

    print("AI PROVIDER ERROR:", f"Unsupported AI_PROVIDER: {AI_PROVIDER}")
    raise AIServiceError(f"Unsupported AI_PROVIDER: {AI_PROVIDER}")
